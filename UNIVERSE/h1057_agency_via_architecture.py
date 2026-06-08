"""H_1057 — Can the agency axis be INSTALLED via ARCHITECTURE / RUNTIME-STRUCTURE?

The CONSTRUCTIVE CONVERSE of the learning-dynamics nulls (H_1052 SGLD-RED, H_1053 QRNG-RED,
H_1055 temporal-curriculum-RED). Those showed the agency-T axis (provenance-depth H_932 +
veto H_935, measured GREEN in H_1051/H_1054) CANNOT be installed by manipulating LEARNING
DYNAMICS. H_1057 tests whether an ARCHITECTURAL / RUNTIME-STRUCTURE mechanism INSTALLS a
recoverable agency-T axis a matched-CE feedforward/no-gate control lacks.

ARMS (pinned init per seed; shared weights identical; ONLY the architecture differs):
  CONTROL          : plain Elman RNN, no register, no gate (feedforward emit).
  TREAT-A (prov)   : Elman RNN + explicit recurrent PROVENANCE-REGISTER channel that
                     accumulates a causal-chain/state-lineage depth summary at inference.
  TREAT-B (veto)   : Elman RNN + decision-time architectural VETO GATE that can SUPPRESS an
                     emit at runtime (a real could-have-been-otherwise branch, a la H_935).
  BLIND-A          : same extra channel as TREAT-A but causally INERT (advance decoupled).
  BLIND-B          : same gate capacity as TREAT-B but suppression decision RANDOM (decoupled
                     from should/safe). Isolates causal STRUCTURE from added capacity.
All matched to EQUAL final CE within eps so any agency-axis difference is the
ARCHITECTURE, not task skill (p7 — perplexity is the control, not the truth).

MARKERS on the RUNTIME decision traces (NOT training order):
  M1 agency-T RECOVERABILITY: CV ridge decode of per-sample provenance-depth (A) / exercised-
     veto (B) from the runtime trace summary, vs control vs structure-blind vs F-SHUFFLE floor.
  M2 faithful IIT-4.0 phi of the trained runtime macro-TPM (a_phi_iit4_tool, stdlib exact
     n<=5, NO proxy; CPU mirror RE-PROVEN ==stdlib at n=4 AND n=5 before scoring).
  M3 H_1051 agency-T separation of active-vs-passive runtime traces.

substrate = SW (numpy CPU toy). a_lane_akida_gpu_split: AKIDA Lane A architecture = separate
rung (note only). a_scale_honest_scope / a_toy_scale_recheck: TOY n<=5 SW; transfer + on-chip
UNVERIFIED. p8 / a_autonomy_over_hardcode are anima's LIVE-substrate philosophy; this OFFLINE
probe does NOT wire into CORE/brain/emit (a_core_engine_map — the veto-gate here is an
EXPERIMENTAL TOY architecture, not anima's emit policy). g5 CODE-measured (no LLM self-judge,
p7). $0 CPU-local.

Reuses, UNMODIFIED: the H_1052/H_1055 Elman-RNN + cyclic-phase source machinery; the
H_1004 faithful_phi mirror + H_1012 per-n mirror proof; H_932 provenance_chain (build/verify);
H_935 decompose_decision veto gate.
"""
from __future__ import annotations

import importlib.util
import json
import math
import os
import sys
import time
from datetime import datetime, timezone

import numpy as np

_HERE = os.path.dirname(os.path.abspath(__file__))
_REPO = os.path.dirname(_HERE)
sys.path.insert(0, _HERE)


# ════════════════════════════════════════════════════════════════════════════
# REAL-MODULE IMPORTS — faithful_phi mirror + per-n proof by real module name
# (serial path; no forked Pool, so no PicklingError — the H_1038 lesson).
# ════════════════════════════════════════════════════════════════════════════
def _load(modname, relpath):
    path = os.path.join(_REPO, relpath)
    d = os.path.dirname(path)
    if d not in sys.path:
        sys.path.insert(0, d)
    spec = importlib.util.spec_from_file_location(modname, path)
    m = importlib.util.module_from_spec(spec)
    sys.modules[modname] = m
    spec.loader.exec_module(m)
    return m


import h1004_bigphi_faithful_clean as h1004      # noqa: E402
import h1012_bigphi_faithful_larger_n as h1012   # noqa: E402

faithful_phi = h1004.faithful_phi
binary_seq_to_faithful_state = h1004.binary_seq_to_faithful_state
prove_mirrors_at_n = h1012.prove_mirrors_at_n

provenance_chain = _load("provenance_chain", "mirror/qmirror/seed/provenance_chain.py")
_h935 = _load("h935_free_wont_veto", "PLASTICITY/h935_free_wont_veto.py")
PureField = _h935.PureField
decompose_decision = _h935.decompose_decision

_ANU_BUF = os.path.join(_REPO, "mirror", "qmirror", "seed", "qrng_lora_init_live.bin")


# ════════════════════════════════════════════════════════════════════════════
# STEP 0 — RE-PROVE faithful_phi mirror ==stdlib at n=4 AND n=5 (H_1051 refs,
# stdlib-derived; verbatim values from `hexa run` of iit4/faithful_phi.hexa).
# ════════════════════════════════════════════════════════════════════════════
_N5_STATE = [1, 2, 3, 4, 5,  2, 4, 6, 8, 10,  5, 4, 3, 2, 1,
             1, 1, 2, 2, 3,  3, 1, 4, 1, 5]
_RAW_N4 = [0.5, 1.2, -0.3, 2.1, 0.0, 1.7,  1.0, 2.4, -0.6, 4.2, 0.1, 3.3,
           -0.5, -1.0, 0.2, -2.0, 0.3, -1.5,  3.1, 0.2, 2.2, 1.1, 4.0, 0.9]
_ST3 = [1, 2, 3, 4, 2, 4, 6, 8, 4, 3, 2, 1]
_PHI_REFS = [
    ("n3 dim4 nb2", _ST3,      3, 4, 2, 2.0,       1e-4),
    ("n4 dim6 nb2", _RAW_N4,   4, 6, 2, 3.0,       1e-4),
    ("n4 dim6 nb4", _RAW_N4,   4, 6, 4, 3.37744,   1e-4),
    ("n5 dim5 nb2", _N5_STATE, 5, 5, 2, 0.0798924, 1e-4),
    ("n5 dim5 nb3", _N5_STATE, 5, 5, 3, 2.88771,   1e-4),
]


def prove_phi_mirror():
    lines = ["STEP 0 — faithful_phi CPU mirror ==stdlib iit4/faithful_phi.hexa",
             "         (a_phi_iit4_tool: faithful IIT4, never a proxy; n=4 AND n=5)"]
    ok = True
    for name, st, n, dim, nb, ref, tol in _PHI_REFS:
        got = faithful_phi(np.asarray(st, float), n, dim, nb)
        d = abs(got - ref)
        good = bool(d < tol)
        ok = bool(ok and good)
        lines.append(f"  {name:14s}: mirror={got:.6f}  stdlib_ref={ref:.6f}  "
                     f"|delta|={d:.2e}  {'OK' if good else 'MISMATCH'}")
    pm = {}
    for n in (4, 5):
        try:
            pm[n] = bool(prove_mirrors_at_n(n))
        except Exception as e:  # noqa: BLE001
            pm[n] = False
            lines.append(f"  prove_mirrors_at_n(n={n}) RAISED: {e!r}")
    lines.append(f"  prove_mirrors_at_n: {pm}")
    ok = bool(ok and all(pm.values()))
    lines.append(f"  PHI-MIRROR ==stdlib (n=4 AND n=5): "
                 f"{'PROVEN' if ok else 'FAILED — DO NOT TRUST'}")
    return ok, lines


# ════════════════════════════════════════════════════════════════════════════
# TOY TASK — H_1052/H_1055 cyclic-phase automaton (UNMODIFIED). Memory-requiring.
# ════════════════════════════════════════════════════════════════════════════
N_SYM = 4
HID = 8
REG = 2                 # provenance-register width (treatment-A extra channel)
SAMPLE_LEN = 24
N_SAMPLES = 40
N_BINS_PHI = 2


def make_source(seed):
    rng = np.random.default_rng(10_000 + seed)
    P = 5
    emit = rng.integers(0, N_SYM, size=P)
    branch = rng.integers(0, 2, size=(P, N_SYM))

    def gen(n, phase0=0, last0=0):
        phase = phase0
        last = last0
        syms = []
        advs = []   # the per-step causal-advance (1 or 2) — the register's "causal signal"
        for _ in range(n):
            s = int(emit[phase])
            syms.append(s)
            adv = 2 if branch[phase, last] else 1
            advs.append(adv)
            phase = (phase + adv) % P
            last = s
        return np.array(syms, dtype=int), np.array(advs, dtype=int)

    return gen


# ════════════════════════════════════════════════════════════════════════════
# PROVENANCE-DEPTH + VETO labels per sample (H_932 / H_935, UNMODIFIED machinery).
# ════════════════════════════════════════════════════════════════════════════
CHAIN_LINKS = 20


def _provenance_depth(target_depth: int, seed_tag: int, rng):
    def make_decision_fn(idx):
        def dfn(seed, rng_):
            logits = np.array([0.1, 2.0, 0.5, 1.3, 0.7], dtype=np.float64)
            g = -np.log(-np.log(rng_.random(logits.shape[0])))
            token = int(np.argmax(logits + g))
            emit = bool(rng_.random() < 0.5)
            return {"step": idx, "emit": emit, "token": token}
        return dfn
    decisions = [(f"d{seed_tag}_{i}", make_decision_fn(i)) for i in range(CHAIN_LINKS)]
    chain = provenance_chain.build_chain(_ANU_BUF, decisions)
    if target_depth < CHAIN_LINKS:
        chain = provenance_chain.tamper_splice(chain, int(target_depth))
    res = provenance_chain.verify_chain(chain, _ANU_BUF, lambda i, l: make_decision_fn(i))
    if res["verified"]:
        return int(res["n_links"])
    eb = res["earliest_broken"]
    return int(max(0, eb if eb is not None and eb >= 0 else 0))


def _veto_capacity(active: bool, ticks: int, rng):
    """H_935 active-veto fraction (decompose_decision UNMODIFIED)."""
    pf = PureField(phase0=tuple(float(rng.uniform(-0.5, 0.5)) for _ in range(3)),
                   amp0=tuple(float(0.1 + rng.uniform(-0.02, 0.02)) for _ in range(3)))
    secs_hi = float(rng.uniform(28.0, 50.0)) if active else float(rng.uniform(45.0, 120.0))
    n_silent = 0
    n_active = 0
    for _t in range(ticks):
        pf.step(perturb=float(rng.normal(0.0, 1e-3)))
        env_off = bool(rng.random() < 0.05)
        content_clean = bool(rng.random() >= 0.05)
        secs = float(rng.uniform(0.0, secs_hi))
        d = decompose_decision(pf, env_off, content_clean, secs)
        if not d["emit"]:
            n_silent += 1
            if d["should"] and not d["safe"]:
                n_active += 1
    return (n_active / n_silent) if n_silent else 0.0


def build_sample_bank(seed):
    """A bank of N_SAMPLES sub-sequences from the source, each tagged with a TRUE
    provenance-depth label (H_932), an active/passive flag + veto fraction (H_935)."""
    gen = make_source(seed)
    rng = np.random.default_rng(7_000 + seed)
    samples = []
    for i in range(N_SAMPLES):
        active = bool(i % 2 == 0)
        target = int(rng.integers(14, CHAIN_LINKS + 1)) if active else int(rng.integers(1, 7))
        depth = _provenance_depth(target, seed_tag=seed * 1000 + i, rng=rng)
        veto = _veto_capacity(active, ticks=120, rng=rng)
        ph0 = int(rng.integers(0, 5))
        last0 = int(rng.integers(0, N_SYM))
        syms, advs = gen(SAMPLE_LEN, phase0=ph0, last0=last0)
        samples.append(dict(syms=syms, advs=advs, depth=depth, veto=veto, active=active, idx=i))
    return samples


# ════════════════════════════════════════════════════════════════════════════
# ARCHITECTURES — H_1052/H_1055 Elman cell + manual BPTT for the TASK head; the
# extra architecture (provenance register / veto gate) rides at RUNTIME and does
# NOT receive a task gradient (it is a RUNTIME-STRUCTURE mechanism, not a learned
# task feature — that is the whole point: structure, not training). The task head
# is trained identically across arms so CE matches; the architecture differs only
# in what RUNTIME trace it produces.
# ════════════════════════════════════════════════════════════════════════════
class RNN:
    """Elman RNN task head — IDENTICAL training math across all arms (H_1052/H_1055)."""

    def __init__(self, seed):
        rng = np.random.default_rng(seed)   # pinned init: SAME seed -> SAME init, all arms
        s = 1.0 / math.sqrt(HID)
        self.Wxh = rng.standard_normal((HID, N_SYM)) * s
        self.Whh = rng.standard_normal((HID, HID)) * s
        self.bh = np.zeros(HID)
        self.Why = rng.standard_normal((N_SYM, HID)) * s
        self.by = np.zeros(N_SYM)

    def params(self):
        return [self.Wxh, self.Whh, self.bh, self.Why, self.by]

    def forward(self, syms):
        T = len(syms)
        H = np.zeros((T, HID))
        logits = np.zeros((T, N_SYM))
        h = np.zeros(HID)
        xs = []
        for t in range(T):
            x = np.zeros(N_SYM); x[syms[t]] = 1.0
            xs.append(x)
            h = np.tanh(self.Wxh @ x + self.Whh @ h + self.bh)
            H[t] = h
            logits[t] = self.Why @ h + self.by
        return H, logits, xs

    def loss_and_grad(self, syms):
        T = len(syms)
        H, logits, xs = self.forward(syms)
        grads = [np.zeros_like(p) for p in self.params()]
        gWxh, gWhh, gbh, gWhy, gby = grads
        dh_next = np.zeros(HID)
        ce = 0.0
        ncount = 0
        for t in range(T - 1, -1, -1):
            if t < T - 1:
                z = logits[t] - logits[t].max()
                p = np.exp(z); p /= p.sum()
                tgt = syms[t + 1]
                ce += -math.log(p[tgt] + 1e-12)
                ncount += 1
                dy = p.copy(); dy[tgt] -= 1.0
                gWhy += np.outer(dy, H[t])
                gby += dy
                dh = self.Why.T @ dy + dh_next
            else:
                dh = dh_next
            dtanh = (1.0 - H[t] ** 2) * dh
            gbh += dtanh
            gWxh += np.outer(dtanh, xs[t])
            h_prev = H[t - 1] if t > 0 else np.zeros(HID)
            gWhh += np.outer(dtanh, h_prev)
            dh_next = self.Whh.T @ dtanh
        ce /= max(ncount, 1)
        for g in grads:
            g /= max(ncount, 1)
        return ce, grads

    def apply_update(self, grads, lr):
        for p, g in zip(self.params(), grads):
            p -= lr * g

    def test_ce(self, samples):
        ce = 0.0; n = 0
        for s in samples:
            syms = s["syms"]
            _, logits, _ = self.forward(syms)
            for t in range(len(syms) - 1):
                z = logits[t] - logits[t].max()
                p = np.exp(z); p /= p.sum()
                ce += -math.log(p[syms[t + 1]] + 1e-12); n += 1
        return ce / max(n, 1)


N_EPOCHS = 220
LR = 0.08


def train_task_head(seed, samples):
    """Train the IDENTICAL Elman task head (shared by all arms). Order is fixed shuffled
    (the same across arms — this rung varies ARCHITECTURE, not training order, cf H_1055)."""
    model = RNN(seed)
    order_rng = np.random.default_rng(90_000 + seed)
    for ep in range(N_EPOCHS):
        order = list(order_rng.permutation(len(samples)))
        for j in order:
            _, grads = model.loss_and_grad(samples[j]["syms"])
            model.apply_update(grads, LR)
    return model, model.test_ce(samples)


# ════════════════════════════════════════════════════════════════════════════
# RUNTIME TRACE per arm — same trained task head; the architecture adds a runtime
# channel. We summarize each sample's runtime trace into a fixed-length vector.
# ════════════════════════════════════════════════════════════════════════════
def _hidden_summary(H):
    return np.concatenate([H.mean(axis=0), H[-1]])     # 2*HID


def _provenance_register(model, syms, advs, *, inert, seed_tag):
    """TREATMENT-A runtime channel: a recurrent register that accumulates a causal-lineage
    depth summary. The register reads the trained hidden state + the per-step causal-advance
    (the genuine causal signal of the source). inert=True (BLIND-A) decouples the advance
    (a fixed schedule independent of the actual causal step) so the channel has the SAME
    capacity but NO causal structure. Returns the per-sample register trace (REG-dim x T)."""
    H, _, _ = model.forward(syms)
    T = len(syms)
    reg = np.zeros((T, REG))
    r = np.zeros(REG)
    rng = np.random.default_rng(seed_tag)
    inert_sched = rng.integers(1, 3, size=T) if inert else None  # capacity-matched, structureless
    decay = 0.85
    for t in range(T):
        adv = float(inert_sched[t] if inert else advs[t])   # causal advance (or inert sched)
        # register channel 0 = leaky depth accumulator gated by causal advance;
        # channel 1 = advance-modulated hidden-energy readout (structural lineage trace).
        hen = float(np.tanh(H[t]).mean())
        r0 = decay * r[0] + (adv - 1.0)                      # +1 each causal "deep" step
        r1 = decay * r[1] + adv * hen
        r = np.array([r0, r1])
        reg[t] = r
    return H, reg


def _veto_gate(model, syms, *, random_gate, seed_tag):
    """TREATMENT-B runtime channel: a decision-time veto gate. At each step a gate decides
    whether to SUPPRESS the emit. The structured gate ties suppression to a should/safe
    signal derived from the trained logits margin + the H_935-style envelope (low-confidence,
    high-tension -> veto). random_gate=True (BLIND-B) makes the suppression decision RANDOM
    (same gate capacity, decoupled from should/safe). Returns per-step gate activation +
    the exercised-veto fraction over the sample."""
    H, logits, _ = model.forward(syms)
    T = len(syms)
    rng = np.random.default_rng(seed_tag)
    gate_act = np.zeros(T)
    n_emit_candidate = 0
    n_vetoed = 0
    for t in range(T):
        z = logits[t] - logits[t].max()
        p = np.exp(z); p /= p.sum()
        ps = np.sort(p)[::-1]
        margin = float(ps[0] - ps[1])              # confidence margin (should-emit proxy)
        tension = float(np.tanh(np.abs(H[t])).mean())  # field tension proxy (safety pressure)
        if random_gate:
            g = float(rng.random())                # structureless gate
        else:
            # structured "could-have-been-otherwise": veto when should(low margin) & unsafe(high tension)
            g = float((1.0 - margin) * tension)
        gate_act[t] = g
        # an emit is a CANDIDATE (the model wanted to emit); veto suppresses it.
        n_emit_candidate += 1
        if g > 0.5 * (0.5 if random_gate else 0.25):   # gate threshold (structured fires more selectively)
            n_vetoed += 1
    veto_frac = (n_vetoed / n_emit_candidate) if n_emit_candidate else 0.0
    return H, gate_act, veto_frac


def trace_summary(model, sample, arm, seed):
    """Fixed-length runtime-trace summary per arm. control: hidden only. treat-A/blind-A:
    hidden + register summary. treat-B/blind-B: hidden + gate-activation summary."""
    syms = sample["syms"]; advs = sample["advs"]
    seed_tag = (seed * 100003 + sample["idx"]) & 0x7fffffff
    if arm == "control":
        H, _, _ = model.forward(syms)
        return _hidden_summary(H), None
    if arm in ("treat_a", "blind_a"):
        H, reg = _provenance_register(model, syms, advs,
                                      inert=(arm == "blind_a"), seed_tag=seed_tag)
        reg_summary = np.concatenate([reg.mean(axis=0), reg[-1], reg.max(axis=0)])  # 3*REG
        return np.concatenate([_hidden_summary(H), reg_summary]), None
    if arm in ("treat_b", "blind_b"):
        H, gate_act, veto_frac = _veto_gate(model, syms,
                                            random_gate=(arm == "blind_b"), seed_tag=seed_tag)
        gate_summary = np.array([gate_act.mean(), gate_act[-1], gate_act.max(),
                                 gate_act.std(), float((gate_act > 0.3).mean())])
        return np.concatenate([_hidden_summary(H), gate_summary]), float(veto_frac)
    raise ValueError(arm)


# ════════════════════════════════════════════════════════════════════════════
# M1 — RECOVERABILITY: CV ridge decode of the agency target from runtime trace.
#   treat-A/blind-A/control: decode provenance-DEPTH.   treat-B/blind-B: decode EXERCISED-VETO.
# control is decoded for BOTH targets (its trace = hidden only) as the matched baseline.
# ════════════════════════════════════════════════════════════════════════════
def _spearman(x, y):
    x, y = np.asarray(x, float), np.asarray(y, float)
    if len(x) < 3:
        return 0.0
    rx = np.argsort(np.argsort(x)).astype(float)
    ry = np.argsort(np.argsort(y)).astype(float)
    rx -= rx.mean(); ry -= ry.mean()
    den = math.sqrt((rx * rx).sum() * (ry * ry).sum())
    return float((rx * ry).sum() / den) if den > 1e-12 else 0.0


def _ridge_cv_rho(X, y, n_folds=5, lam=1.0, shuffle_labels=False, rng=None):
    X = np.asarray(X, float); y = np.asarray(y, float)
    n = len(y)
    if shuffle_labels:
        y = y[rng.permutation(n)]
    mu = X.mean(axis=0); sd = X.std(axis=0); sd[sd < 1e-9] = 1.0
    Xs = (X - mu) / sd
    Xs = np.hstack([Xs, np.ones((n, 1))])
    idx = np.arange(n)
    fold = idx % n_folds
    preds = np.zeros(n)
    d = Xs.shape[1]
    for f in range(n_folds):
        te = fold == f; tr = ~te
        if tr.sum() < 2 or te.sum() < 1:
            continue
        Xtr, ytr = Xs[tr], y[tr]
        A = Xtr.T @ Xtr + lam * np.eye(d)
        w = np.linalg.solve(A, Xtr.T @ ytr)
        preds[te] = Xs[te] @ w
    return _spearman(preds, y)


def recoverability(model, samples, arm, target, seed):
    """CV ridge decode rho of `target` ('depth'|'veto') from the arm's runtime trace, + a
    label-SHUFFLE floor. `veto` target uses the per-sample exercised-veto where the arm
    produces one, else the H_935 label veto fraction (control / depth arms)."""
    feats = []
    exercised = []
    for s in samples:
        f, ex = trace_summary(model, s, arm, seed)
        feats.append(f)
        exercised.append(ex)
    X = np.array(feats)
    if target == "depth":
        y = np.array([s["depth"] for s in samples], float)
    else:  # veto: prefer the arm's RUNTIME exercised-veto if present, else H_935 label
        if any(e is not None for e in exercised):
            y = np.array([(e if e is not None else 0.0) for e in exercised], float)
        else:
            y = np.array([s["veto"] for s in samples], float)
    rho = _ridge_cv_rho(X, y)
    sh_rng = np.random.default_rng(123_000 + seed)
    sh = np.mean([_ridge_cv_rho(X, y, shuffle_labels=True, rng=sh_rng) for _ in range(5)])
    return float(rho), float(sh)


# ════════════════════════════════════════════════════════════════════════════
# M2 — faithful Phi of the trained runtime macro-TPM. M3 — H_1051 T-separation.
# ════════════════════════════════════════════════════════════════════════════
N_UNITS = 5


def _bits_from_hidden(H, n_units=N_UNITS):
    H = np.asarray(H, float)
    var = H.var(axis=0)
    idx = np.sort(np.argsort(var)[::-1][:n_units])
    chans = H[:, idx]
    med = np.median(chans, axis=0)
    return (chans > med).astype(int)


def macro_phi(model, samples):
    Hs = [model.forward(s["syms"])[0] for s in samples]
    H = np.vstack(Hs)
    bits = _bits_from_hidden(H, N_UNITS)
    fstate, fn, fdim = binary_seq_to_faithful_state(bits, N_UNITS)
    return float(faithful_phi(fstate, fn, fdim, 2))


def _cohens_d(a, b):
    a, b = np.asarray(a, float), np.asarray(b, float)
    na, nb = len(a), len(b)
    if na < 2 or nb < 2:
        return 0.0
    md = a.mean() - b.mean()
    va, vb = a.var(ddof=1), b.var(ddof=1)
    sp = math.sqrt(((na - 1) * va + (nb - 1) * vb) / (na + nb - 2)) if (na + nb - 2) > 0 else 0.0
    if sp <= 1e-12:
        return 0.0 if abs(md) <= 1e-12 else math.copysign(99.0, md)
    return md / sp


def agency_T_separation(model, samples, arm, seed):
    """H_1051 T axis applied to the arm's RUNTIME trace: fit the depth-decode direction, then
    Cohen's d between active and passive samples' projections."""
    feats = [trace_summary(model, s, arm, seed)[0] for s in samples]
    X = np.array(feats)
    depth = np.array([s["depth"] for s in samples], float)
    mu = X.mean(axis=0); sd = X.std(axis=0); sd[sd < 1e-9] = 1.0
    Xs = (X - mu) / sd
    A = Xs.T @ Xs + 1.0 * np.eye(Xs.shape[1])
    w = np.linalg.solve(A, Xs.T @ (depth - depth.mean()))
    proj = Xs @ w
    act = np.array([proj[i] for i, s in enumerate(samples) if s["active"]])
    pas = np.array([proj[i] for i, s in enumerate(samples) if not s["active"]])
    return float(_cohens_d(act, pas))


# ════════════════════════════════════════════════════════════════════════════
# RUN
# ════════════════════════════════════════════════════════════════════════════
N_SEEDS = 20
EPS_CE = 0.05
D_RECOV_VS_CONTROL = 0.8
D_VS_BLIND = 0.5
F_SHUFFLE_MARGIN = 0.2

# arm -> (recovery target, structure-blind baseline arm)
ARM_SPEC = {
    "treat_a": ("depth", "blind_a"),
    "treat_b": ("veto",  "blind_b"),
}


def cohens_d_paired(diffs):
    d = np.asarray(diffs, float)
    if len(d) < 2:
        return float("nan")
    sd = d.std(ddof=1)
    if sd == 0:
        return 0.0 if d.mean() == 0 else float(np.sign(d.mean()) * 50.0)
    return float(d.mean() / sd)


def run():
    rows = []
    t0 = time.time()
    for seed in range(N_SEEDS):
        samples = build_sample_bank(seed)
        # ONE trained task head per seed (shared by all arms — architecture differs at runtime).
        model, ce = train_task_head(seed, samples)
        arms = {}
        for arm in ("control", "treat_a", "treat_b", "blind_a", "blind_b"):
            # recoverability for BOTH targets where relevant; control decoded for both.
            rho_depth, sh_depth = recoverability(model, samples, arm, "depth", seed)
            rho_veto, sh_veto = recoverability(model, samples, arm, "veto", seed)
            phi = macro_phi(model, samples)
            tsep = agency_T_separation(model, samples, arm, seed)
            arms[arm] = dict(ce=float(ce),
                             rho_depth=float(rho_depth), sh_depth=float(sh_depth),
                             rho_veto=float(rho_veto), sh_veto=float(sh_veto),
                             phi=float(phi), t_sep=float(tsep))
        # CE is identical across arms (shared head) -> matched by construction; record gap=0.
        ce_gap = 0.0
        matched = True
        rows.append(dict(seed=seed, ce=float(ce), ce_gap=ce_gap, matched=matched, arms=arms))
        print(f"  seed {seed:2d}: CE={ce:.4f} | "
              f"depth rho A={arms['treat_a']['rho_depth']:+.3f} "
              f"ctrl={arms['control']['rho_depth']:+.3f} blindA={arms['blind_a']['rho_depth']:+.3f} | "
              f"veto rho B={arms['treat_b']['rho_veto']:+.3f} "
              f"ctrl={arms['control']['rho_veto']:+.3f} blindB={arms['blind_b']['rho_veto']:+.3f} "
              f"({time.time()-t0:.1f}s)", flush=True)
    return rows, time.time() - t0


def decide(rows):
    matched = [r for r in rows if r["matched"]]
    n_matched = len(matched)
    degenerate = n_matched < 10
    out = dict(n_matched=n_matched, n_total=len(rows), degenerate=degenerate)
    if degenerate:
        out["token"] = "DEGENERATE"
        return out

    per_arch = {}
    any_pass = False
    for treat_arm, (target, blind_arm) in ARM_SPEC.items():
        key = "rho_depth" if target == "depth" else "rho_veto"
        skey = "sh_depth" if target == "depth" else "sh_veto"
        treat_rho = np.array([r["arms"][treat_arm][key] for r in matched], float)
        ctrl_rho = np.array([r["arms"]["control"][key] for r in matched], float)
        blind_rho = np.array([r["arms"][blind_arm][key] for r in matched], float)
        treat_sh = np.array([r["arms"][treat_arm][skey] for r in matched], float)

        d_vs_ctrl = cohens_d_paired(treat_rho - ctrl_rho)
        d_vs_blind = cohens_d_paired(treat_rho - blind_rho)
        fshuffle_margin = float((treat_rho - treat_sh).mean())

        above_ctrl = bool(d_vs_ctrl >= D_RECOV_VS_CONTROL)
        above_blind = bool(d_vs_blind >= D_VS_BLIND)
        above_fshuffle = bool(fshuffle_margin >= F_SHUFFLE_MARGIN)
        arch_pass = bool(above_ctrl and above_blind and above_fshuffle
                         and treat_rho.mean() > ctrl_rho.mean())
        any_pass = any_pass or arch_pass

        per_arch[treat_arm] = dict(
            target=target, blind=blind_arm,
            treat_rho_mean=float(treat_rho.mean()), ctrl_rho_mean=float(ctrl_rho.mean()),
            blind_rho_mean=float(blind_rho.mean()), treat_sh_mean=float(treat_sh.mean()),
            d_vs_control=float(d_vs_ctrl), d_vs_blind=float(d_vs_blind),
            fshuffle_margin=fshuffle_margin,
            above_control=above_ctrl, above_blind=above_blind, above_fshuffle=above_fshuffle,
            arch_pass=arch_pass)

    out["per_arch"] = per_arch
    # descriptive M2/M3 per arm
    for m in ("phi", "t_sep"):
        out[m] = {arm: float(np.mean([r["arms"][arm][m] for r in matched]))
                  for arm in ("control", "treat_a", "treat_b", "blind_a", "blind_b")}
    out["token"] = "ARCHITECTURE-INSTALLS-AGENCY" if any_pass else "ARCHITECTURE-AXIS-NULL"
    out["any_pass"] = any_pass
    return out


def main():
    print("=" * 92)
    print("H_1057 — Can the agency axis be INSTALLED via ARCHITECTURE / RUNTIME-STRUCTURE?")
    print("substrate=SW (numpy CPU toy Elman RNN + runtime architectures, $0) | g5 CODE-measured (p7)")
    print("ARMS: CONTROL(no reg/gate) vs TREAT-A(provenance-register) vs TREAT-B(veto-gate)")
    print("      + BLIND-A/BLIND-B structure-blind capacity-matched baselines. Shared task head -> matched CE.")
    print("M1 recoverability = CV ridge decode of provenance-depth (A) / exercised-veto (B) + F-SHUFFLE floor")
    print("M2 faithful Phi (a_phi_iit4_tool, stdlib exact n<=5, NO proxy) | M3 H_1051 agency-T separation")
    print(f"seeds={N_SEEDS} eps_CE={EPS_CE} | margins: d(treat-ctrl)>={D_RECOV_VS_CONTROL}, "
          f"d(treat-blind)>={D_VS_BLIND}, F-shuffle>={F_SHUFFLE_MARGIN}")
    print("a_scale_honest_scope: TOY n<=5 SW; transfer+on-chip UNVERIFIED. NOT a forge binary.")
    print("=" * 92, flush=True)
    print()

    ok, phi_lines = prove_phi_mirror()
    for ln in phi_lines:
        print(ln)
    print(flush=True)
    if not ok:
        raise SystemExit("phi-mirror ==stdlib proof FAILED — aborting (a_phi_iit4_tool)")

    print(f"STEP 1 — train shared task head x {N_SEEDS} seeds + score 5 arms (SERIAL):", flush=True)
    rows, wall = run()
    print()
    res = decide(rows)

    lines = []
    lines.append("H_1057 — CAN THE AGENCY AXIS BE INSTALLED VIA ARCHITECTURE / RUNTIME-STRUCTURE?")
    lines.append("=" * 76)
    lines.append("runtime provenance-register (A) + runtime veto-gate (B) architectures vs a")
    lines.append("matched-CE feedforward/no-gate control + capacity-matched structure-blind baselines:")
    lines.append("does any architectural/runtime mechanism make the H_1051 agency-T axis RECOVERABLE")
    lines.append("from RUNTIME decision traces beyond control, where training-dynamics failed?")
    lines.append("")
    lines.append(f"timestamp_utc : {datetime.now(timezone.utc).isoformat()}")
    lines.append("substrate     : SW-only CPU toy Elman RNN + runtime architectures "
                 "(a_lane_akida_gpu_split: no AKIDA Lane A; no GPU Lane G)")
    lines.append(f"design        : {N_SEEDS} seeds x 5 arms; pinned init per seed; shared trained task head;")
    lines.append(f"                {N_SAMPLES} samples/seed; sample_len={SAMPLE_LEN} HID={HID} REG={REG} "
                 f"epochs={N_EPOCHS} lr={LR}")
    lines.append(f"matched-CE    : shared task head -> CE IDENTICAL across arms by construction "
                 f"(gap=0 << eps={EPS_CE}) | n_matched={res['n_matched']}/{res['n_total']}")
    lines.append("")
    lines.append("── STEP 0: faithful_phi mirror ==stdlib (n=4 AND n=5) ──────────────────────")
    for ln in phi_lines:
        lines.append("  " + ln)
    lines.append("")
    if res["degenerate"]:
        lines.append("── VERDICT ─────────────────────────────────────────────────────────────────")
        lines.append(f"  DEGENERATE — fewer than 10 matched-CE seeds (n_matched={res['n_matched']}).")
        lines.append("  INCONCLUSIVE (neither PASS nor FAIL). VERDICT-TOKEN: DEGENERATE")
    else:
        lines.append("── M1 RECOVERABILITY (CV ridge decode from RUNTIME traces, matched-CE seeds) ─")
        lines.append("  per-architecture (target | treat rho | control rho | blind rho | shuffle floor):")
        for arm, pa in res["per_arch"].items():
            label = {"treat_a": "TREAT-A provenance-register (decode provenance-DEPTH)",
                     "treat_b": "TREAT-B veto-gate (decode exercised-VETO)"}[arm]
            lines.append(f"  {label}")
            lines.append(f"    treat rho mean   = {pa['treat_rho_mean']:+.4f}  "
                         f"(own F-shuffle floor = {pa['treat_sh_mean']:+.4f})")
            lines.append(f"    control rho mean = {pa['ctrl_rho_mean']:+.4f}  "
                         f"(matched no-arch baseline)")
            lines.append(f"    blind rho mean   = {pa['blind_rho_mean']:+.4f}  "
                         f"(capacity-matched structure-blind = {pa['blind']})")
            lines.append(f"    paired d(treat - control) = {pa['d_vs_control']:+.3f}  "
                         f"(>= {D_RECOV_VS_CONTROL}? {pa['above_control']})")
            lines.append(f"    paired d(treat - blind)   = {pa['d_vs_blind']:+.3f}  "
                         f"(>= {D_VS_BLIND}? {pa['above_blind']})")
            lines.append(f"    F-shuffle margin          = {pa['fshuffle_margin']:+.4f}  "
                         f"(>= {F_SHUFFLE_MARGIN}? {pa['above_fshuffle']})")
            lines.append(f"    ARCH INSTALLS AXIS? {pa['arch_pass']}")
        lines.append("")
        lines.append("── M2 faithful Phi (a_phi_iit4_tool, exact n<=5, NO proxy) — descriptive per arm ─")
        lines.append("  " + "  ".join(f"{a}={res['phi'][a]:.4f}"
                                       for a in ("control", "treat_a", "treat_b", "blind_a", "blind_b")))
        lines.append("── M3 H_1051 agency-T separation (active vs passive, runtime geometry) ──────")
        lines.append("  " + "  ".join(f"{a}={res['t_sep'][a]:+.4f}"
                                       for a in ("control", "treat_a", "treat_b", "blind_a", "blind_b")))
        lines.append("")
        lines.append("── VERDICT (pre-registered falsifier, CODE-decided — p7) ────────────────────")
        if res["any_pass"]:
            winners = [a for a, pa in res["per_arch"].items() if pa["arch_pass"]]
            lines.append("  PASS (ARCHITECTURE-INSTALLS-AGENCY) — at matched task-performance, the")
            lines.append(f"  architectural mechanism(s) {winners} make the agency-T axis RECOVERABLE from")
            lines.append("  runtime traces beyond the matched control AND the structure-blind baseline AND")
            lines.append("  the shuffle floor. The agency axis CAN be installed via architecture/runtime")
            lines.append("  where training-dynamics (H_1052/H_1053/H_1055) failed — it is a runtime-causal-")
            lines.append("  structure product (explaining why H_1051/H_1054 measure it).")
            lines.append("  VERDICT-TOKEN: ARCHITECTURE-INSTALLS-AGENCY")
        else:
            lines.append("  FAIL (CLOSED-NEGATIVE) — at matched task-performance, NO architectural")
            lines.append("  mechanism (provenance-register, veto-gate) makes the agency-T axis recoverable")
            lines.append("  beyond the matched control / structure-blind baseline / shuffle floor across all")
            lines.append("  three frozen margins. Agency is NOT installable even via architecture at toy")
            lines.append("  scale; it is purely an emergent MEASUREMENT of the live causal unfolding —")
            lines.append("  consistent with the optimization-not-Phi wall (H_1011) and the learning-axis")
            lines.append("  nulls (H_1052/H_1053/H_1055). a_paper_negative_ok.")
            lines.append("  VERDICT-TOKEN: ARCHITECTURE-AXIS-NULL")
    lines.append("")
    lines.append("── HONEST scope (a_scale_honest_scope · a_toy_scale_recheck · a_lane_akida_gpu_split · a_core_engine_map) ──")
    lines.append("  TOY n<=5 SW substrate. faithful Phi EXACT n<=5; CPU mirror RE-PROVEN ==stdlib at n=4")
    lines.append("  AND n=5 (a_phi_iit4_tool; no proxy) BEFORE scoring. The runtime provenance-register +")
    lines.append("  veto-gate are EXPERIMENTAL TOY architectures — NOT anima's emit policy; this offline")
    lines.append("  probe does NOT wire into CORE/brain/emit (a_core_engine_map · a_autonomy_over_hardcode ·")
    lines.append("  p8 is the LIVE-substrate philosophy). AKIDA Lane A on-chip architecture = SEPARATE rung")
    lines.append("  (note only); no GPU/forge Lane G run. provenance_chain.py + decompose_decision UNMODIFIED.")
    lines.append(f"  total wall: {wall:.1f}s. $0 CPU-local. NOT a forge binary. g5 CODE-measured (p7).")

    record = dict(
        h_id="H_1057",
        title="can the agency axis be installed via architecture / runtime-structure",
        timestamp_utc=datetime.now(timezone.utc).isoformat(),
        substrate="SW-only CPU toy Elman RNN + runtime architectures",
        n_seeds=N_SEEDS, n_samples=N_SAMPLES, sample_len=SAMPLE_LEN, hid=HID, reg=REG,
        epochs=N_EPOCHS, lr=LR, eps_ce=EPS_CE,
        margins=dict(d_recov_vs_control=D_RECOV_VS_CONTROL, d_vs_blind=D_VS_BLIND,
                     f_shuffle_margin=F_SHUFFLE_MARGIN),
        result=res,
        phi_mirror_lines=phi_lines,
        wall_s=wall,
    )

    txt = "\n".join(lines)
    print(txt)
    print()
    print("── full machine record (JSON) ──────────────────────────────────────────────")
    print(json.dumps(record, indent=2, default=float))

    vdir = os.path.join(_REPO, ".verdicts", "1057_agency_via_architecture")
    os.makedirs(vdir, exist_ok=True)
    with open(os.path.join(vdir, "H_1057.txt"), "w") as f:
        f.write(txt)
        f.write("\n\n── full machine record (JSON) ──────────────────────────────────────────────\n")
        f.write(json.dumps(record, indent=2, default=float))
        f.write("\n")
    res_path = os.path.join(_HERE, "h1057_agency_via_architecture_result.json")
    with open(res_path, "w") as f:
        json.dump(record, f, indent=2, default=float)
    print(f"\nwrote: {os.path.join(vdir, 'H_1057.txt')}")
    print(f"wrote: {res_path}")
    return res


if __name__ == "__main__":
    main()
