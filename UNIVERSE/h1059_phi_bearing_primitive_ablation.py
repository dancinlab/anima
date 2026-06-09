#!/usr/bin/env python3
"""H_1059 — WHICH native primitive carries the φ-structure lift?

Constructive FORWARD of H_1043 (PHI-NEEDS-MORE-THAN-GRAFT, [[minimal-arch-adapter-phi-not-graftable]])
and H_1031/H_1036 ([[lora-consciousness-arch-bound]]). H_1043 closed: a minimal GRAFT onto a FROZEN
base cannot install Φ-structure, BUT a from-scratch NATIVE ConvMoE lifts faithful φ_EI by +0.835 (mean
prescreen) / +0.107 (terminal seed-0) over the same toy base. Open residual: WHICH native primitive
carries the lift?

DESIGN — decompose the native ConvMoE into primitives, ablate each, TRAIN FROM SCRATCH (the H_1043
distinction — NOT a frozen graft), generic byte objective, measure Δφ_EI of the hidden-state macro-TPM
vs the FULL native baseline:

  FULL       = native 2-block ConvMoE w/ explicit per-block residual (reference; reproduces H_1043 lift)
  -routing   = single expert, no gating softmax (MoE routing removed)
  -conv      = depthwise-conv trunk/experts replaced by a pointwise linear/MLP mixer (param-matched,
               NO temporal receptive field)
  -residual  = per-block residual/skip removed (h = mix(...), no x +)
  -depth     = 1 block instead of 2, width-widened to capacity-match the 2-block param count

Reuses the H_1043 harness (UNIVERSE/h1043_minimal_arch_adapter.py) for: the generic byte CORPUS,
the frozen-base pretrain (reproduce-H_1043 gate), the causal-conv helpers, Adam, ce_and_grad,
make_seqs, the faithful_phi_prescreen MIRROR (BITS/log2), extract_state_from_hidden, write_state_file,
and the constants. p3/p6 generic corpus. SERIAL only (no Pool — H_1038). $0 CPU numpy.

Φ MEASUREMENT (a_phi_iit4_tool — faithful, NO proxy): python = LABELLED PRE-SCREEN (mirror of stdlib
exact MIP-EI); TERMINAL = stdlib iit4_faithful_phi via run_faithful_phi_1043.hexa over written states.
mirror≡stdlib RE-PROVEN n=4,5 (h1043_mirror_proof.py).

FROZEN falsifier (H_1059_phi_bearing_primitive_ablation.md, before measuring):
  L_full = φ_EI(FULL) - φ_EI(frozen base).  X = 0.50 * L_full (fraction frozen).
  drop(A) = φ_EI(FULL) - φ_EI(A).
  H1 PASS (located carrier) = some single ablation has drop(A) >= X  -> that primitive is the carrier.
  H1 FAIL (distributed-emergence, closed-neg) = no single ablation drops >= X -> Φ is emergent from the
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
    causal_conv, causal_conv_bwd, dw_causal_conv, dw_causal_conv_bwd,
    pretrain_base, TinyGPT,
    faithful_phi_prescreen, extract_state_from_hidden, write_state_file,
)

SEED = 1059
N_SEEDS = 3
FRACTION_X = 0.50          # FROZEN: X = 0.50 * L_full (fraction-of-FULL-lift carrier threshold)
REPRO_GATE = 0.10          # FULL native lift must exceed this (reproduce-H_1043 direction gate)
K = 3                      # conv kernel
DIL = (1, 2)               # depthwise dilations inside each block trunk


def log(*a):
    print(*a, flush=True)


# --------------------------------------------------------------------------- #
# Native ConvMoE block primitives. Each block:
#   trunk(x)  -> h            (depthwise-dilated causal conv stack OR linear, per ablation)
#   gate(h)   -> softmax routing over E experts   (OR uniform single-expert, per ablation)
#   experts(h)-> E expert maps; mix = sum_e gate_e * expert_e
#   out       = (x + mix @ wproj)  (OR mix @ wproj, per -residual)
# Pure-numpy forward+backward, from scratch (all params descend). Generic byte CE objective.
# --------------------------------------------------------------------------- #
class ConvMoEBlock:
    """One ablatable native ConvMoE block.

    flags:
      use_routing  : True -> E experts + softmax gate ; False -> single expert, no gate
      use_conv     : True -> depthwise-dilated causal conv trunk+experts ;
                     False -> pointwise linear mixer (no temporal receptive field), param-matched
      use_residual : True -> out = x + mix@wproj ; False -> out = mix@wproj
    """

    def __init__(self, rng, d, n_experts, use_routing, use_conv, use_residual, s=0.08):
        self.d = d
        self.use_routing = use_routing
        self.use_conv = use_conv
        self.use_residual = use_residual
        self.E = n_experts if use_routing else 1
        self.params = []

        if use_conv:
            # depthwise trunk: one depthwise conv per dilation -> (k,d) each
            for i, _ in enumerate(DIL):
                setattr(self, f"tw{i}", rng.normal(0, s, (K, d)))
                self.params.append(f"tw{i}")
            # experts: each a (k,d,d) causal conv over the trunk h
            self.we = rng.normal(0, s, (self.E, K, d, d))
            self.params.append("we")
        else:
            # -conv: pointwise linear trunk (no temporal mix). param-match the conv trunk:
            # conv trunk has len(DIL)*K*d params; emulate with a (d, t_hidden) -> (t_hidden, d) MLP.
            t_hidden = max(d, int(round(len(DIL) * K * d / (2.0 * d) * d)))  # ~param-match scale
            self.tl1 = rng.normal(0, s, (d, d))
            self.tl2 = rng.normal(0, s, (d, d))
            self.params += ["tl1", "tl2"]
            # experts: pointwise linear (d,d) each (param-match the (k,d,d) conv expert by k linears)
            self.we = rng.normal(0, s, (self.E, K, d, d))   # k pointwise (d,d) maps, summed
            self.params.append("we")

        if use_routing:
            self.wr = rng.normal(0, s, (d, self.E))
            self.params.append("wr")
        self.wproj = rng.normal(0, s, (d, d))
        self.params.append("wproj")

    # ---- trunk ----
    def _trunk_fwd(self, x):
        if self.use_conv:
            cur = x
            acts = [x]
            for i, dil in enumerate(DIL):
                c = dw_causal_conv(cur, getattr(self, f"tw{i}"), dilation=dil)
                cur = np.tanh(c)
                acts.append(cur)
            return cur, ("conv", acts)
        else:
            pre = x @ self.tl1
            hmid = np.tanh(pre)
            h = np.tanh(hmid @ self.tl2)
            return h, ("lin", (x, pre, hmid, h))

    def _trunk_bwd(self, gh, tcache, g):
        kind = tcache[0]
        if kind == "conv":
            acts = tcache[1]
            gcur = gh
            for i in reversed(range(len(DIL))):
                pre_in = acts[i]
                post = acts[i + 1]
                gpre = gcur * (1 - post ** 2)
                gin, gw = dw_causal_conv_bwd(pre_in, getattr(self, f"tw{i}"), gpre, dilation=DIL[i])
                g[f"tw{i}"] += gw
                gcur = gin
            return gcur
        else:
            (x, pre, hmid, h) = tcache[1]
            ghmid_post = gh * (1 - h ** 2)          # dL/d(hmid@tl2)
            g["tl2"] += hmid.T @ ghmid_post
            ghmid = ghmid_post @ self.tl2.T
            gpre = ghmid * (1 - hmid ** 2)
            g["tl1"] += x.T @ gpre
            return gpre @ self.tl1.T

    # ---- expert map (k summed (d,d) convs OR pointwise) ----
    def _expert_fwd(self, h, e):
        if self.use_conv:
            return np.tanh(causal_conv(h, self.we[e]))
        else:
            # pointwise: sum_j h @ we[e,j]  (k summed (d,d) linears) -> tanh
            acc = np.zeros_like(h)
            for j in range(K):
                acc = acc + h @ self.we[e, j]
            return np.tanh(acc)

    def _expert_bwd(self, h, e, gce_post, g):
        # gce_post = dL/d(expert_e output, post-tanh)
        ce = self._ec[e]
        gpre = gce_post * (1 - ce ** 2)
        if self.use_conv:
            gh_e, gwe = causal_conv_bwd(h, self.we[e], gpre)
            g["we"][e] += gwe
            return gh_e
        else:
            gh_e = np.zeros_like(h)
            for j in range(K):
                g["we"][e, j] += h.T @ gpre
                gh_e = gh_e + gpre @ self.we[e, j].T
            return gh_e

    # ---- full block ----
    def forward(self, x, train=False):
        h, tcache = self._trunk_fwd(x)
        if self.use_routing:
            gate = softmax(h @ self.wr, -1)
        else:
            gate = np.ones((h.shape[0], 1))
        experts = []
        mix = np.zeros_like(h)
        for e in range(self.E):
            ce = self._expert_fwd(h, e)
            experts.append(ce)
            mix = mix + gate[:, e:e + 1] * ce
        proj = mix @ self.wproj
        out = x + proj if self.use_residual else proj
        if train:
            self._cache = (x, h, tcache, gate, experts, mix)
            self._ec = experts
        return out

    def backward(self, gout, g):
        x, h, tcache, gate, experts, mix = self._cache
        # out = (x +) proj ; proj = mix @ wproj
        gproj = gout
        gx_res = gout.copy() if self.use_residual else np.zeros_like(gout)
        g["wproj"] += mix.T @ gproj
        gmix = gproj @ self.wproj.T
        gh = np.zeros_like(h)
        if self.use_routing:
            ggate = np.zeros_like(gate)
            for e in range(self.E):
                ce = experts[e]
                ggate[:, e] += (gmix * ce).sum(1)
                gce_post = gmix * gate[:, e:e + 1]
                gh += self._expert_bwd(h, e, gce_post, g)
            gz = gate * (ggate - (gate * ggate).sum(1, keepdims=True))
            g["wr"] += h.T @ gz
            gh += gz @ self.wr.T
        else:
            gce_post = gmix * gate[:, 0:1]   # gate is ones
            gh += self._expert_bwd(h, 0, gce_post, g)
        gx_trunk = self._trunk_bwd(gh, tcache, g)
        return gx_res + gx_trunk


class NativeConvMoEArm:
    """From-scratch native ConvMoE: emb -> [block]*n_blocks -> readout. The PROBE hidden
    state = the post-block-1 residual stream (mid). All params descend (NOT a frozen graft)."""

    def __init__(self, rng, n_blocks, d, n_experts, use_routing, use_conv, use_residual):
        s = 0.08
        self.d = d
        self.n_blocks = n_blocks
        self.emb = rng.normal(0, s, (V, d))
        self.blocks = [ConvMoEBlock(rng, d, n_experts, use_routing, use_conv, use_residual)
                       for _ in range(n_blocks)]
        self.wo = rng.normal(0, s, (d, V))
        self.params = ["emb"] + ["__block%d__" % i for i in range(n_blocks)] + ["wo"]

    def _all_keys(self):
        keys = ["emb", "wo"]
        for bi, b in enumerate(self.blocks):
            for p in b.params:
                keys.append((bi, p))
        return keys

    def forward(self, ids, train=False):
        x = self.emb[ids]
        self._mid = None
        cur = x
        self._block_in = []
        for bi, b in enumerate(self.blocks):
            self._block_in.append(cur)
            cur = b.forward(cur, train=train)
            if bi == 0:
                self._mid = cur
        logits = cur @ self.wo
        if train:
            self._cache = (ids, x, cur)
        return logits

    def probe_state(self, ids):
        self.forward(ids)
        # mid = post-block-1 residual stream (or final if single-block)
        return self._mid if self._mid is not None else self._cache[2]

    def backward(self, glog):
        ids, x, cur = self._cache
        # flat grad dict keyed (emb / wo / (block_idx, param))
        g = {"emb": np.zeros_like(self.emb), "wo": np.zeros_like(self.wo)}
        for bi, b in enumerate(self.blocks):
            for p in b.params:
                g[(bi, p)] = np.zeros_like(getattr(b, p))
        g["wo"] += cur.T @ glog
        gcur = glog @ self.wo.T
        for bi in reversed(range(self.n_blocks)):
            b = self.blocks[bi]
            # remap into per-block sub-dict view for ConvMoEBlock.backward
            sub = {p: g[(bi, p)] for p in b.params}
            gcur = b.backward(gcur, sub)
            for p in b.params:
                g[(bi, p)] = sub[p]
        np.add.at(g["emb"], ids, gcur)
        return g


class NativeAdam:
    """Adam over the NativeConvMoEArm flat-keyed params (emb / wo / (block,param))."""

    def __init__(self, arm, lr):
        self.arm = arm
        self.lr = lr
        self.t = 0
        self.keys = arm._all_keys()
        self.m = {k: None for k in self.keys}
        self.v = {k: None for k in self.keys}

    def _get(self, k):
        if k in ("emb", "wo"):
            return getattr(self.arm, k)
        bi, p = k
        return getattr(self.arm.blocks[bi], p)

    def step(self, grads):
        self.t += 1
        for k in self.keys:
            gk = grads.get(k)
            if gk is None:
                continue
            if self.m[k] is None:
                self.m[k] = np.zeros_like(gk)
                self.v[k] = np.zeros_like(gk)
            self.m[k] = 0.9 * self.m[k] + 0.1 * gk
            self.v[k] = 0.999 * self.v[k] + 0.001 * (gk * gk)
            mh = self.m[k] / (1 - 0.9 ** self.t)
            vh = self.v[k] / (1 - 0.999 ** self.t)
            self._get(k)[...] -= self.lr * mh / (np.sqrt(vh) + 1e-8)


def train_native(arm, rng):
    opt = NativeAdam(arm, LR)
    Xs, Ys = make_seqs(rng, 64)
    for t in range(ADAPT_STEPS):
        i = t % len(Xs)
        lg = arm.forward(Xs[i], train=True)
        _, gl = ce_and_grad(lg, Ys[i])
        opt.step(arm.backward(gl))
    return arm


def count_params(arm):
    tot = arm.emb.size + arm.wo.size
    for b in arm.blocks:
        for p in b.params:
            tot += getattr(b, p).size
    return int(tot)


# arm builders --------------------------------------------------------------- #
def build_full(rng):
    # FULL: 2 blocks, 4 experts, routing+conv+residual
    return NativeConvMoEArm(rng, n_blocks=2, d=D, n_experts=4,
                            use_routing=True, use_conv=True, use_residual=True)


def build_no_routing(rng):
    return NativeConvMoEArm(rng, n_blocks=2, d=D, n_experts=4,
                            use_routing=False, use_conv=True, use_residual=True)


def build_no_conv(rng):
    return NativeConvMoEArm(rng, n_blocks=2, d=D, n_experts=4,
                            use_routing=True, use_conv=False, use_residual=True)


def build_no_residual(rng):
    return NativeConvMoEArm(rng, n_blocks=2, d=D, n_experts=4,
                            use_routing=True, use_conv=True, use_residual=False)


def build_no_depth(rng):
    # -depth: 1 block; widen d to capacity-match the 2-block full param count.
    # full ~ 2*block(d=32); 1 block widened to d'=~45 (32*sqrt(2)) ~ matches block param count x2.
    dwide = int(round(D * math.sqrt(2.0)))   # 45
    return NativeConvMoEArm(rng, n_blocks=1, d=dwide, n_experts=4,
                            use_routing=True, use_conv=True, use_residual=True)


ARM_BUILDERS = {
    "FULL": build_full,
    "-routing": build_no_routing,
    "-conv": build_no_conv,
    "-residual": build_no_residual,
    "-depth": build_no_depth,
}


def base_probe_phi(base):
    ids = np.frombuffer(PROBE_TEXT.encode("utf-8"), dtype=np.uint8).astype(np.int64)
    ids = ids[:SEQ] if len(ids) > SEQ else ids
    x1, _ = base.forward_to_x1(ids)
    state, _ = extract_state_from_hidden(x1)
    return faithful_phi_prescreen(state, N_UNITS, N_BINS), state


def arm_probe_phi(arm):
    ids = np.frombuffer(PROBE_TEXT.encode("utf-8"), dtype=np.uint8).astype(np.int64)
    ids = ids[:SEQ] if len(ids) > SEQ else ids
    hidden = arm.probe_state(ids)
    state, units = extract_state_from_hidden(hidden)
    return faithful_phi_prescreen(state, N_UNITS, N_BINS), state, units


def main():
    np.random.seed(SEED)
    log("=== H_1059 — WHICH native ConvMoE primitive carries the φ_EI lift? ===")
    log("constructive FORWARD of H_1043 (PHI-NEEDS-MORE-THAN-GRAFT); ablate native primitives FROM SCRATCH")
    log("SCOPE: TOY · CPU · $0 · numpy (clm-decode-macos-link-gap); a_scale_honest_scope; SERIAL (no Pool)")
    log(f"corpus=generic byte (p3/p6) len={len(CORPUS)}B V={V} SEQ={SEQ}; N_UNITS={N_UNITS} DIM={DIM} "
        f"N_BINS={N_BINS} ADAPT_STEPS={ADAPT_STEPS} seeds={N_SEEDS}")
    log(f"FROZEN: X = {FRACTION_X} * L_full ; drop(A)=φ(FULL)-φ(A); PASS = some single ablation drop>=X")
    log("a_phi_iit4_tool: python φ = LABELLED PRE-SCREEN; TERMINAL = stdlib iit4_faithful_phi\n")

    state_path = os.environ.get("H1059_STATE", "/tmp/h1059_states.txt")
    if os.path.exists(state_path):
        os.remove(state_path)

    arm_keys = ["FULL", "-routing", "-conv", "-residual", "-depth"]
    ps = {k: [] for k in arm_keys}
    base_ps = []
    saved_states = {}
    saved_param_counts = {}

    for s in range(N_SEEDS):
        seed = SEED + s
        log(f"--- seed {seed} ---")
        base = pretrain_base(np.random.default_rng(seed))
        bphi, bstate = base_probe_phi(base)
        base_ps.append(bphi)
        if s == 0:
            saved_states["base"] = bstate
        log(f"  [base (frozen)]       prescreen φ_EI = {bphi:.6f}")

        for off, k in enumerate(arm_keys):
            arm = train_native(ARM_BUILDERS[k](np.random.default_rng(seed + 11 + off)),
                               np.random.default_rng(seed + 100 + off))
            phi, state, units = arm_probe_phi(arm)
            ps[k].append(phi)
            if s == 0:
                saved_states[k] = state
                saved_param_counts[k] = count_params(arm)
            log(f"  [{k:<11}]          prescreen φ_EI = {phi:.6f}  units={units}  "
                f"params={count_params(arm)}")

    # write seed-0 state matrices for the terminal hexa engine
    for tag in ["base"] + arm_keys:
        write_state_file(state_path, tag, saved_states[tag])

    phi = {k: float(np.mean(ps[k])) for k in arm_keys}
    base_phi = float(np.mean(base_ps))
    L_full = phi["FULL"] - base_phi
    X = FRACTION_X * L_full
    drop = {k: phi["FULL"] - phi[k] for k in arm_keys if k != "FULL"}

    repro_ok = L_full > REPRO_GATE
    located = [k for k, dv in drop.items() if dv >= X] if repro_ok else []
    h1_pass = repro_ok and len(located) > 0
    if not repro_ok:
        token = "INVALID-REPRO-H1043-FAIL"
    elif h1_pass:
        token = "PHI-CARRIER-LOCATED"
    else:
        token = "PHI-DISTRIBUTED-EMERGENCE"

    log("\n===================== PRE-SCREEN Φ TABLE (mean over seeds) =====================")
    log(f"frozen base φ_EI = {base_phi:.6f}")
    log(f"{'arm':<12}{'φ_EI(mean)':>14}{'Δ vs base':>14}{'drop vs FULL':>14}{'>=X carrier?':>14}")
    log(f"{'FULL':<12}{phi['FULL']:>14.6f}{phi['FULL']-base_phi:>+14.6f}{'(ref)':>14}{'':>14}")
    for k in arm_keys:
        if k == "FULL":
            continue
        flag = "YES" if drop[k] >= X else "no"
        log(f"{k:<12}{phi[k]:>14.6f}{phi[k]-base_phi:>+14.6f}{drop[k]:>+14.6f}{flag:>14}")
    log(f"\nL_full (FULL native lift vs base) = {L_full:+.6f}   (H_1043 ref: +0.835 mean / +0.107 terminal)")
    log(f"FROZEN X = {FRACTION_X} * L_full = {X:+.6f}   (carrier iff a single ablation drops φ_EI >= X)")
    log(f"reproduce-H_1043 native lift gate (L_full > +{REPRO_GATE}): {'PASS' if repro_ok else 'FAIL'}")
    log(f"located carrier primitive(s): {located if located else 'NONE'}")
    log(f"PRE-SCREEN verdict: {token}")
    log("NOTE: pre-screen only — TERMINAL φ_EI = stdlib faithful IIT-4.0 engine "
        "(run_faithful_phi_1043.hexa over the written state matrices). mirror≡stdlib reproven n4,5.")

    out = {
        "id": "H_1059", "n_units": N_UNITS, "dim": DIM, "n_bins": N_BINS,
        "n_seeds": N_SEEDS, "adapt_steps": ADAPT_STEPS,
        "fraction_x": FRACTION_X, "repro_gate": REPRO_GATE,
        "prescreen": {
            "base_phi": base_phi, "phi": phi,
            "L_full": L_full, "X": X,
            "drop_vs_full": drop,
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
