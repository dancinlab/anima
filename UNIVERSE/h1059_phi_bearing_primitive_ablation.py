#!/usr/bin/env python3
"""H_1059 — WHICH native ConvMoE primitive carries the φ_EI lift?

Constructive FORWARD of H_1043 (PHI-NEEDS-MORE-THAN-GRAFT, [[minimal-arch-adapter-phi-not-graftable]])
and H_1031/H_1036 ([[lora-consciousness-arch-bound]]). H_1043 closed: a minimal GRAFT onto a FROZEN
base cannot install Φ-structure, BUT a from-scratch NATIVE ConvMoE lifts faithful φ_EI by +0.835 (mean
prescreen) / +0.107 (terminal seed-0) over the same toy base (at seeds 1043/1044/1045). Open residual:
WHICH native primitive carries the lift?

DESIGN — FULL = the H_1043 ConvMoENative arch VERBATIM (so it REPRODUCES the +0.835 lift at the H_1043
seeds — the reproduce-H_1043 gate). Then ablate, FROM SCRATCH (the H_1043 distinction — NOT a frozen
graft), each of the native arch's REAL primitives, generic byte objective, measuring Δφ_EI of the SAME
hidden-state macro-TPM probe (the gated expert mix = H_1043 ConvMoENative.probe_state) vs FULL:

  FULL     = emb -> c=conv(x,w1) -> h=tanh(c) -> gate=softmax(h@wr) -> experts ce=tanh(conv(h,we_e))
             -> mix=Σ gate_e·ce -> logits=mix@wo.  PROBE = mix. (== H_1043 ConvMoENative, bit-for-bit.)
  -routing = single expert, no softmax gate (E=1, uniform). MoE routing removed.
  -conv    = trunk conv w1 and expert convs we replaced by pointwise linear maps (param-matched, NO
             temporal receptive field).
  -trunk   = remove the conv trunk layer w1+tanh (experts operate directly on the embedding) — the
             depth/structured-mixing primitive ("-depth": shallower native trunk).
  -nonlin  = remove the structural tanh nonlinearities (trunk + experts linear-activated), capacity
             identical — isolates whether the φ-lift needs the nonlinearity primitive.

Reuses the H_1043 harness for: CORPUS, frozen-base pretrain, causal-conv helpers, Adam, ce_and_grad,
make_seqs, faithful_phi_prescreen (BITS/log2 MIRROR), extract_state_from_hidden, write_state_file,
constants — AND imports ConvMoENative + train_convmoe_native so FULL is the LITERAL H_1043 native arm.
p3/p6 generic corpus. SERIAL only (no Pool — H_1038, if __name__-guard). $0 CPU numpy.

Φ MEASUREMENT (a_phi_iit4_tool — faithful, NO proxy): python = LABELLED PRE-SCREEN (mirror of stdlib
exact MIP-EI); TERMINAL = stdlib iit4_faithful_phi via run_faithful_phi_1043.hexa. mirror≡stdlib
RE-PROVEN n=4,5 (h1043_mirror_proof.py).

FROZEN falsifier (H_1059_phi_bearing_primitive_ablation.md, before measuring):
  L_full = φ_EI(FULL) - φ_EI(frozen base).  X = 0.50 * L_full (fraction frozen).
  drop(A) = φ_EI(FULL) - φ_EI(A).
  H1 PASS (located carrier) = some single ablation drop(A) >= X  -> that primitive is the carrier.
  H1 FAIL (distributed-emergence, closed-neg) = no single ablation drops >= X -> Φ emergent from the
           primitive COMBINATION, not any one part.
  Guard: L_full <= +0.10 => reproduce-H_1043 FAIL => run INVALID.

SCOPE (a_scale_honest_scope): TOY CPU $0 numpy small rung; 3B/7B + emergence + non-frozen UNVERIFIED.
Φ axis ONLY (necessary-not-sufficient). p7: φ = causal-irreducibility marker, NOT perplexity.
"""
from __future__ import annotations
import sys, os, json, math
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from h1043_minimal_arch_adapter import (  # noqa: E402  reuse H_1043 harness
    V, SEQ, DIM, N_UNITS, N_BINS, ADAPT_STEPS, LR, D,
    CORPUS, PROBE_TEXT,
    softmax, ce_and_grad, make_seqs, Adam,
    causal_conv, causal_conv_bwd,
    pretrain_base,
    ConvMoENative, train_convmoe_native,
    faithful_phi_prescreen, extract_state_from_hidden, write_state_file,
)

SEED = 1043          # anchor on the H_1043 seeds (1043/1044/1045): the +0.835 native lift was
                     # established there; reproduce-H_1043 gate requires FULL to reproduce it.
N_SEEDS = 3
FRACTION_X = 0.50    # FROZEN: X = 0.50 * L_full (fraction-of-FULL-lift carrier threshold)
REPRO_GATE = 0.10    # FULL native lift must exceed this (reproduce-H_1043 direction gate)
K = 3                # conv kernel (== H_1043 ConvMoENative k)
NE = 4               # experts (== H_1043 ConvMoENative n_experts)


def log(*a):
    print(*a, flush=True)


# --------------------------------------------------------------------------- #
# Parametric native ConvMoE arm. With ALL flags default it is BIT-FOR-BIT the
# H_1043 ConvMoENative (same param init order, same forward), so FULL reproduces
# the +0.835 lift. Each flag ablates ONE real primitive of that native arch.
#   emb -> [trunk: c=conv(x,w1); h=act(c)]            (use_trunk / use_conv / use_nonlin)
#       -> gate=softmax(h@wr)                          (use_routing)
#       -> experts ce_e=act(conv(h,we_e)); mix=Σ g_e·ce_e
#       -> logits=mix@wo.   PROBE=mix.
# --------------------------------------------------------------------------- #
class NativeArm:
    def __init__(self, rng, d=D, n_experts=NE, k=K,
                 use_routing=True, use_conv=True, use_trunk=True, use_nonlin=True):
        self.d, self.k = d, k
        self.use_routing = use_routing
        self.use_conv = use_conv
        self.use_trunk = use_trunk
        self.use_nonlin = use_nonlin
        self.E = n_experts if use_routing else 1
        s = 0.08
        # init order matches ConvMoENative (emb, w1, we, wr, wo) so FULL == native bit-for-bit
        self.emb = rng.normal(0, s, (V, d))
        if use_conv:
            self.w1 = rng.normal(0, s, (k, d, d))
            self.we = rng.normal(0, s, (self.E, k, d, d))
        else:
            # -conv: pointwise linear (k==1 receptive field), param-matched by k stacked (d,d) maps
            self.w1 = rng.normal(0, s, (k, d, d))   # used as k summed pointwise (d,d) maps
            self.we = rng.normal(0, s, (self.E, k, d, d))
        if use_routing:
            self.wr = rng.normal(0, s, (d, self.E))
        self.wo = rng.normal(0, s, (d, V))
        self.params = ["emb"]
        if use_trunk:
            self.params.append("w1")
        self.params.append("we")
        if use_routing:
            self.params.append("wr")
        self.params.append("wo")

    def _act(self, z):
        return np.tanh(z) if self.use_nonlin else z

    def _dact(self, post):
        # d/dz act ; post = act(z). tanh' = 1-post^2 ; identity' = 1
        return (1 - post ** 2) if self.use_nonlin else np.ones_like(post)

    def _conv(self, x, w):
        if self.use_conv:
            return causal_conv(x, w)
        # pointwise: sum_j x @ w[j]  (k summed (d,d) maps, no temporal context)
        out = np.zeros((x.shape[0], w.shape[2]))
        for j in range(self.k):
            out = out + x @ w[j]
        return out

    def _conv_bwd(self, x, w, gout):
        if self.use_conv:
            return causal_conv_bwd(x, w, gout)
        gw = np.zeros_like(w)
        gx = np.zeros_like(x)
        for j in range(self.k):
            gw[j] += x.T @ gout
            gx = gx + gout @ w[j].T
        return gx, gw

    def forward(self, ids, train=False):
        x = self.emb[ids]
        if self.use_trunk:
            c = self._conv(x, self.w1)
            h = self._act(c)
        else:
            c = None
            h = x                       # -trunk: experts act directly on the embedding
        if self.use_routing:
            gate = softmax(h @ self.wr, -1)
        else:
            gate = np.ones((h.shape[0], 1))
        experts = []
        mix = np.zeros_like(h)
        for e in range(self.E):
            ce = self._act(self._conv(h, self.we[e]))
            experts.append(ce)
            mix = mix + gate[:, e:e + 1] * ce
        logits = mix @ self.wo
        self._mix = mix
        if train:
            self._cache = (ids, x, c, h, gate, experts, mix)
        return logits

    def probe_state(self, ids):
        self.forward(ids)
        return self._mix                # == H_1043 ConvMoENative.probe_state (gated expert mix)

    def backward(self, glog):
        ids, x, c, h, gate, experts, mix = self._cache
        g = {k: np.zeros_like(getattr(self, k)) for k in self.params}
        g["wo"] += mix.T @ glog
        gmix = glog @ self.wo.T
        gh = np.zeros_like(h)
        if self.use_routing:
            ggate = np.zeros_like(gate)
            for e in range(self.E):
                ce = experts[e]
                ggate[:, e] += (gmix * ce).sum(1)
                gce = gmix * gate[:, e:e + 1]
                gpre = gce * self._dact(ce)
                gh_e, gwe = self._conv_bwd(h, self.we[e], gpre)
                g["we"][e] += gwe
                gh += gh_e
            gz = gate * (ggate - (gate * ggate).sum(1, keepdims=True))
            g["wr"] += h.T @ gz
            gh += gz @ self.wr.T
        else:
            ce = experts[0]
            gpre = (gmix * gate[:, 0:1]) * self._dact(ce)
            gh_e, gwe = self._conv_bwd(h, self.we[0], gpre)
            g["we"][0] += gwe
            gh += gh_e
        if self.use_trunk:
            gc = gh * self._dact(h)
            gx, gw1 = self._conv_bwd(x, self.w1, gc)
            g["w1"] += gw1
            np.add.at(g["emb"], ids, gx)
        else:
            np.add.at(g["emb"], ids, gh)
        return g


def train_arm(builder, rng):
    """Build + train an arm using ONE rng for BOTH init and data — EXACTLY the H_1043
    train_convmoe_native(rng) pattern, so FULL (rng=default_rng(seed+55)) reproduces the
    H_1043 native trained φ bit-for-bit."""
    arm = builder(rng)
    opt = Adam(arm.params, LR)
    Xs, Ys = make_seqs(rng, 64)
    for t in range(ADAPT_STEPS):
        i = t % len(Xs)
        lg = arm.forward(Xs[i], train=True)
        _, gl = ce_and_grad(lg, Ys[i])
        opt.step(arm, arm.backward(gl))
    return arm


def count_params(arm):
    return int(sum(getattr(arm, p).size for p in arm.params))


# arm builders --------------------------------------------------------------- #
def build_full(rng):       return NativeArm(rng)
def build_no_routing(rng): return NativeArm(rng, use_routing=False)
def build_no_conv(rng):    return NativeArm(rng, use_conv=False)
def build_no_trunk(rng):   return NativeArm(rng, use_trunk=False)
def build_no_nonlin(rng):  return NativeArm(rng, use_nonlin=False)

ARM_BUILDERS = {
    "FULL": build_full,
    "-routing": build_no_routing,
    "-conv": build_no_conv,
    "-trunk": build_no_trunk,
    "-nonlin": build_no_nonlin,
}
ABLATIONS = ["-routing", "-conv", "-trunk", "-nonlin"]


def probe_phi(state_provider):
    ids = np.frombuffer(PROBE_TEXT.encode("utf-8"), dtype=np.uint8).astype(np.int64)
    ids = ids[:SEQ] if len(ids) > SEQ else ids
    hidden = state_provider(ids)
    state, units = extract_state_from_hidden(hidden)
    return faithful_phi_prescreen(state, N_UNITS, N_BINS), state, units


def base_phi(base):
    def prov(ids):
        x1, _ = base.forward_to_x1(ids)
        return x1
    return probe_phi(prov)


def main():
    np.random.seed(SEED)
    log("=== H_1059 — WHICH native ConvMoE primitive carries the φ_EI lift? ===")
    log("constructive FORWARD of H_1043; FULL = H_1043 ConvMoENative VERBATIM (reproduces +0.835 lift)")
    log("ablate each native primitive FROM SCRATCH (the H_1043 distinction — NOT a frozen graft)")
    log("SCOPE: TOY · CPU · $0 · numpy (clm-decode-macos-link-gap); a_scale_honest_scope; SERIAL (no Pool)")
    log(f"seeds={SEED}..{SEED+N_SEEDS-1} (H_1043 seeds) corpus=generic byte (p3/p6) len={len(CORPUS)}B V={V}")
    log(f"N_UNITS={N_UNITS} DIM={DIM} N_BINS={N_BINS} ADAPT_STEPS={ADAPT_STEPS}")
    log(f"FROZEN: X = {FRACTION_X} * L_full ; drop(A)=φ(FULL)-φ(A); PASS = some single ablation drop>=X")
    log("a_phi_iit4_tool: python φ = LABELLED PRE-SCREEN; TERMINAL = stdlib iit4_faithful_phi\n")

    # sanity: FULL must equal the imported H_1043 ConvMoENative bit-for-bit (reproduce-H_1043 identity)
    _r = np.random.default_rng(99)
    fa = NativeArm(np.random.default_rng(99))
    nb = ConvMoENative(np.random.default_rng(99))
    ids0 = np.frombuffer(PROBE_TEXT.encode("utf-8"), dtype=np.uint8).astype(np.int64)[:SEQ]
    identical = np.allclose(fa.probe_state(ids0), nb.probe_state(ids0), atol=1e-12)
    log(f"[reproduce-H_1043 identity] FULL NativeArm probe == ConvMoENative probe (untrained): {identical}\n")

    # reproduce-H_1043 TRAINED: FULL (rng=seed+55) trained φ must equal train_convmoe_native(seed+55) φ
    repro_trained = []
    for s in range(N_SEEDS):
        seed = SEED + s
        full = train_arm(build_full, np.random.default_rng(seed + 55))
        ref = train_convmoe_native(np.random.default_rng(seed + 55))
        pf = faithful_phi_prescreen(*([extract_state_from_hidden(full.probe_state(ids0))[0], N_UNITS, N_BINS]))
        pr = faithful_phi_prescreen(*([extract_state_from_hidden(ref.probe_state(ids0))[0], N_UNITS, N_BINS]))
        repro_trained.append((seed, pf, pr, abs(pf - pr) < 1e-9))
        log(f"[reproduce-H_1043 trained] seed {seed}: FULL φ={pf:.6f} vs ConvMoENative φ={pr:.6f} "
            f"-> {'MATCH' if abs(pf-pr)<1e-9 else 'DIFF'}")
    log("")

    state_path = os.environ.get("H1059_STATE", "/tmp/h1059_states.txt")
    if os.path.exists(state_path):
        os.remove(state_path)

    arm_keys = ["FULL"] + ABLATIONS
    ps = {k: [] for k in arm_keys}
    base_ps = []
    saved_states = {}
    saved_param_counts = {}

    for s in range(N_SEEDS):
        seed = SEED + s
        log(f"--- seed {seed} ---")
        base = pretrain_base(np.random.default_rng(seed))
        bphi, bstate, _ = base_phi(base)
        base_ps.append(bphi)
        if s == 0:
            saved_states["base"] = bstate
        log(f"  [base (frozen)]   prescreen φ_EI = {bphi:.6f}")
        for off, k in enumerate(arm_keys):
            # ONE rng per arm for init+data (H_1043 pattern). FULL (off=0) -> default_rng(seed+55)
            # == train_convmoe_native(default_rng(seed+55)) -> reproduces H_1043 native trained φ.
            arm = train_arm(ARM_BUILDERS[k], np.random.default_rng(seed + 55 + off))
            phi, state, units = probe_phi(arm.probe_state)
            ps[k].append(phi)
            if s == 0:
                saved_states[k] = state
                saved_param_counts[k] = count_params(arm)
            log(f"  [{k:<9}]       prescreen φ_EI = {phi:.6f}  units={units}  params={count_params(arm)}")

    for tag in ["base"] + arm_keys:
        write_state_file(state_path, tag, saved_states[tag])

    phi = {k: float(np.mean(ps[k])) for k in arm_keys}
    base_phi_m = float(np.mean(base_ps))
    L_full = phi["FULL"] - base_phi_m
    X = FRACTION_X * L_full
    drop = {k: phi["FULL"] - phi[k] for k in ABLATIONS}

    repro_ok = L_full > REPRO_GATE
    located = [k for k in ABLATIONS if drop[k] >= X] if repro_ok else []
    h1_pass = repro_ok and len(located) > 0
    if not repro_ok:
        token = "INVALID-REPRO-H1043-FAIL"
    elif h1_pass:
        token = "PHI-CARRIER-LOCATED"
    else:
        token = "PHI-DISTRIBUTED-EMERGENCE"

    log("\n===================== PRE-SCREEN Φ TABLE (mean over H_1043 seeds) =====================")
    log(f"frozen base φ_EI = {base_phi_m:.6f}")
    log(f"{'arm':<10}{'φ_EI(mean)':>14}{'Δ vs base':>14}{'drop vs FULL':>14}{'>=X carrier?':>14}")
    log(f"{'FULL':<10}{phi['FULL']:>14.6f}{phi['FULL']-base_phi_m:>+14.6f}{'(ref)':>14}{'':>14}")
    for k in ABLATIONS:
        flag = "YES" if drop[k] >= X else "no"
        log(f"{k:<10}{phi[k]:>14.6f}{phi[k]-base_phi_m:>+14.6f}{drop[k]:>+14.6f}{flag:>14}")
    log(f"\nL_full (FULL native lift vs base) = {L_full:+.6f}   (H_1043 ref: +0.835407 mean / +0.107 terminal)")
    log(f"FROZEN X = {FRACTION_X} * L_full = {X:+.6f}   (carrier iff a single ablation drops φ_EI >= X)")
    log(f"reproduce-H_1043 native lift gate (L_full > +{REPRO_GATE}): {'PASS' if repro_ok else 'FAIL'}")
    log(f"located carrier primitive(s): {located if located else 'NONE'}")
    log(f"PRE-SCREEN verdict: {token}")
    log("NOTE: pre-screen only — TERMINAL φ_EI = stdlib faithful IIT-4.0 engine "
        "(run_faithful_phi_1043.hexa over the written state matrices). mirror≡stdlib reproven n4,5.")

    out = {
        "id": "H_1059", "n_units": N_UNITS, "dim": DIM, "n_bins": N_BINS,
        "n_seeds": N_SEEDS, "seeds": [SEED + i for i in range(N_SEEDS)], "adapt_steps": ADAPT_STEPS,
        "fraction_x": FRACTION_X, "repro_gate": REPRO_GATE,
        "full_equals_h1043_native_identity": bool(identical),
        "prescreen": {
            "base_phi": base_phi_m, "phi": phi,
            "L_full": L_full, "X": X, "drop_vs_full": drop,
            "reproduce_h1043_lift_pass": bool(repro_ok),
            "located_carriers": located, "h1_pass": bool(h1_pass), "token": token,
        },
        "param_counts": saved_param_counts,
        "state_file": state_path,
        "scope": "TOY CPU $0 numpy small rung; 3B/7B + emergence + non-frozen UNVERIFIED; Φ axis only",
        "note": ("TERMINAL phi = stdlib faithful IIT-4.0 (run_faithful_phi_1043.hexa); python phi is "
                 "PRE-SCREEN only. Φ-structure necessary-not-sufficient. p7."),
        "h1043_ref": {"native_lift_mean_prescreen": 0.835407, "native_lift_terminal_seed0": 0.107018},
    }
    out_path = os.environ.get("H1059_OUT", "/tmp/h1059_result.json")
    with open(out_path, "w") as f:
        json.dump(out, f, indent=2)
    log("\nJSON " + json.dumps(out))
    log(f"result.json -> {out_path}")
    log(f"state matrices -> {state_path}")


if __name__ == "__main__":
    main()
