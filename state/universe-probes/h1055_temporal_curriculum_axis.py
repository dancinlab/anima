"""H_1055 — Can the temporal/agency axis be BUILT INTO TRAINING?

Tests whether building temporal/causal STRUCTURE into training — (A) ordering training
samples by causal/provenance DEPTH instead of shuffled, + (B) weighting the loss by
provenance-depth — makes the TRAINED Elman-RNN hidden state ACQUIRE the agency-T axis as a
LEARNED internal coordinate (provenance-depth RECOVERABLE/DECODABLE from the hidden geometry)
that a matched-CE shuffled-order control lacks, and beyond a generic curriculum-optimization
(order-blind) baseline.

THREE ARMS (pinned init per seed; ONLY the training-order/weighting differs):
  CONTROL      : shuffled order, uniform loss weight.
  TREATMENT    : temporal-curriculum (samples ordered by provenance-depth ascending)
                 + provenance-depth-weighted loss (A+B).
  ORDER-BLIND  : provenance-depth-weighted loss (B) but SHUFFLED order — the
                 curriculum-optimization control isolating ORDER STRUCTURE (A) from
                 generic depth-reweighting (B).
Matched to EQUAL final CE within eps so any agency-axis difference is the temporal/causal
STRUCTURE, not curriculum-optimization nor task skill (p7 — perplexity is the control, not
the truth).

MARKERS on the TRAINED hidden states:
  M1 agency-T RECOVERABILITY: cross-validated Spearman rho of a ridge decoder recovering
     per-sample provenance-depth from the trained per-sample hidden summary, vs a label-
     SHUFFLE floor (F-SHUFFLE). Mirrors the H_1054 order-recovery+shuffle logic.
  M2 faithful IIT-4.0 phi_EI of the trained hidden macro-TPM (a_phi_iit4_tool, stdlib exact
     n<=5, NO proxy; CPU mirror RE-PROVEN ==stdlib at n=4 AND n=5 before scoring).
  M3 H_1051 agency-T separation of the trained model's active-vs-passive samples.

substrate = SW (numpy CPU toy). a_lane_akida_gpu_split: AKIDA Lane A curriculum = separate
rung (note only). a_scale_honest_scope / a_toy_scale_recheck: TOY n<=5 SW; transfer + on-chip
UNVERIFIED. p8 is anima's LIVE-substrate philosophy; this OFFLINE probe does NOT wire into
CORE/brain (a_core_engine_map). g5 CODE-measured (no LLM self-judge, p7). $0 CPU-local.

Reuses, UNMODIFIED: the H_1052 Elman-RNN+source machinery; the H_1004 faithful_phi mirror +
H_1012 per-n mirror proof; H_932 provenance_chain (build/verify); H_935 decompose_decision
veto gate.
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
# (serial path; no forked Pool, so no PicklingError). H_932/H_935 by file path.
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

big_phi = h1004.big_phi
faithful_phi = h1004.faithful_phi
binary_seq_to_tpm = h1004.binary_seq_to_tpm
modal_state = h1004.modal_state
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
    # Also re-prove the H_1004/H_1012 big_phi+faithful via prove_mirrors_at_n at n=4,5.
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
# TOY TASK — H_1052 cyclic-phase automaton (UNMODIFIED). Memory-requiring source.
# ════════════════════════════════════════════════════════════════════════════
N_SYM = 4
HID = 8
SAMPLE_LEN = 24        # each training sample = a sub-sequence window
N_SAMPLES = 40         # bank of samples per seed
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
        for _ in range(n):
            s = int(emit[phase])
            syms.append(s)
            adv = 2 if branch[phase, last] else 1
            phase = (phase + adv) % P
            last = s
        return np.array(syms, dtype=int)

    return gen


# ════════════════════════════════════════════════════════════════════════════
# PROVENANCE-DEPTH label per sample (H_932, UNMODIFIED build/verify). A deep
# auditable chain reconstructs many links; a forced/shallow lineage breaks early.
# We assign each sample a TRUE causal depth (its label), realized via the H_932
# verifier so the label is the genuine verified-link count, not a fiat integer.
# ════════════════════════════════════════════════════════════════════════════
CHAIN_LINKS = 20


def _provenance_depth(target_depth: int, seed_tag: int, rng):
    """Build an H_932 chain whose independent verifier reconstructs ~target_depth links.
    target_depth in [1..CHAIN_LINKS]. Realizes the depth via tamper_splice at the break
    index, then RETURNS the verifier's actual reconstructed link count (the genuine label)."""
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
    """H_935 active-veto fraction (decompose_decision UNMODIFIED). active -> idle clock
    straddles the 30s floor (graded veto); passive -> mostly open (little veto)."""
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
    provenance-depth label (H_932) and an active/passive flag (H_935 veto). Half the
    samples are 'active' (deep chain, real veto), half 'passive' (shallow chain, no veto)."""
    gen = make_source(seed)
    rng = np.random.default_rng(7_000 + seed)
    samples = []
    for i in range(N_SAMPLES):
        active = bool(i % 2 == 0)
        # active samples target a DEEP chain (14..20); passive a SHALLOW one (1..6).
        if active:
            target = int(rng.integers(14, CHAIN_LINKS + 1))
        else:
            target = int(rng.integers(1, 7))
        depth = _provenance_depth(target, seed_tag=seed * 1000 + i, rng=rng)
        veto = _veto_capacity(active, ticks=120, rng=rng)
        # the sample sub-sequence — vary the source start phase per sample for diversity
        ph0 = int(rng.integers(0, 5))
        last0 = int(rng.integers(0, N_SYM))
        syms = gen(SAMPLE_LEN, phase0=ph0, last0=last0)
        samples.append(dict(syms=syms, depth=depth, veto=veto, active=active, idx=i))
    return samples


# ════════════════════════════════════════════════════════════════════════════
# RNN — H_1052 Elman cell + manual BPTT (UNMODIFIED arithmetic). Now trains over a
# BANK of samples; per-sample loss can be weighted; sample order can be set.
# ════════════════════════════════════════════════════════════════════════════
class RNN:
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

    def hidden_summary(self, syms):
        """Per-sample fixed-length hidden summary: mean + last hidden state (2*HID)."""
        H, _, _ = self.forward(syms)
        return np.concatenate([H.mean(axis=0), H[-1]])


N_EPOCHS = 220
LR = 0.08


def train_arm(seed, samples, arm):
    """arm in {'control','treatment','order_blind'}. control: shuffled, uniform weight.
    treatment: depth-ordered + depth-weighted. order_blind: shuffled + depth-weighted."""
    model = RNN(seed)
    depths = np.array([s["depth"] for s in samples], float)
    dmax = depths.max() if depths.max() > 0 else 1.0
    # depth weights normalized to mean 1 (so total gradient scale matches the uniform arm).
    w_depth = 1.0 + depths / dmax
    w_depth = w_depth / w_depth.mean()
    order_rng = np.random.default_rng(90_000 + seed)
    # treatment ORDER = ascending provenance-depth (time-flow / causal-depth).
    asc_order = list(np.argsort(depths, kind="stable"))
    for ep in range(N_EPOCHS):
        if arm == "treatment":
            order = asc_order
            weighted = True
        elif arm == "order_blind":
            order = list(order_rng.permutation(len(samples)))
            weighted = True
        else:  # control
            order = list(order_rng.permutation(len(samples)))
            weighted = False
        for j in order:
            s = samples[j]
            _, grads = model.loss_and_grad(s["syms"])
            w = w_depth[j] if weighted else 1.0
            model.apply_update([g * w for g in grads], LR)
    return model, model.test_ce(samples)


# ════════════════════════════════════════════════════════════════════════════
# M1 — agency-T RECOVERABILITY: cross-validated ridge decode of provenance-depth
# from the trained per-sample hidden summary, + a label-SHUFFLE floor (F-SHUFFLE).
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
    """K-fold cross-validated Spearman rho of a ridge decoder X->y (held-out preds)."""
    X = np.asarray(X, float)
    y = np.asarray(y, float)
    n = len(y)
    if shuffle_labels:
        y = y[rng.permutation(n)]
    # standardize features
    mu = X.mean(axis=0); sd = X.std(axis=0); sd[sd < 1e-9] = 1.0
    Xs = (X - mu) / sd
    Xs = np.hstack([Xs, np.ones((n, 1))])  # bias column
    idx = np.arange(n)
    fold = idx % n_folds
    preds = np.zeros(n)
    d = Xs.shape[1]
    for f in range(n_folds):
        te = fold == f
        tr = ~te
        if tr.sum() < 2 or te.sum() < 1:
            continue
        Xtr, ytr = Xs[tr], y[tr]
        A = Xtr.T @ Xtr + lam * np.eye(d)
        w = np.linalg.solve(A, Xtr.T @ ytr)
        preds[te] = Xs[te] @ w
    return _spearman(preds, y)


def recoverability(model, samples, seed):
    X = np.array([model.hidden_summary(s["syms"]) for s in samples])
    depth = np.array([s["depth"] for s in samples], float)
    rho = _ridge_cv_rho(X, depth)
    sh_rng = np.random.default_rng(123_000 + seed)
    sh = np.mean([_ridge_cv_rho(X, depth, shuffle_labels=True, rng=sh_rng) for _ in range(5)])
    return float(rho), float(sh)


# ════════════════════════════════════════════════════════════════════════════
# M2 — faithful Phi of the trained hidden macro-TPM (n<=5 exact; mirror proven).
# M3 — H_1051 agency-T separation on the trained hidden state (active vs passive).
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
    """Concatenate hidden traces over all samples -> binarize top-5-var -> faithful Phi."""
    Hs = [model.forward(s["syms"])[0] for s in samples]
    H = np.vstack(Hs)
    bits = _bits_from_hidden(H, N_UNITS)
    fstate, fn, fdim = binary_seq_to_faithful_state(bits, N_UNITS)
    fphi = faithful_phi(fstate, fn, fdim, 2)
    return float(fphi)


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


def agency_T_separation(model, samples):
    """H_1051 T axis applied to the TRAINED hidden state: project each sample's hidden
    summary onto the depth-decode direction (the learned agency direction), then measure
    Cohen's d between active and passive samples. Higher = the trained geometry separates
    active vs passive (agency carved in)."""
    X = np.array([model.hidden_summary(s["syms"]) for s in samples])
    depth = np.array([s["depth"] for s in samples], float)
    mu = X.mean(axis=0); sd = X.std(axis=0); sd[sd < 1e-9] = 1.0
    Xs = (X - mu) / sd
    # fit depth-direction on all (in-sample direction; separation is the readout test)
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
D_RECOV_VS_SHUF = 0.8      # treatment-vs-shuffled-control recoverability paired |d|
F_SHUFFLE_MARGIN = 0.2     # treatment rho above its own label-shuffle floor
D_VS_ORDERBLIND = 0.5      # treatment-vs-order-blind recoverability paired |d|


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
        arms = {}
        for arm in ("control", "treatment", "order_blind"):
            model, ce = train_arm(seed, samples, arm)
            rho, shuf = recoverability(model, samples, seed)
            phi = macro_phi(model, samples)
            tsep = agency_T_separation(model, samples)
            arms[arm] = dict(ce=float(ce), recov_rho=float(rho), recov_shuf=float(shuf),
                             phi=float(phi), t_sep=float(tsep))
        ce_vals = [arms[a]["ce"] for a in arms]
        ce_gap = float(max(ce_vals) - min(ce_vals))
        matched = bool(ce_gap <= EPS_CE)
        rows.append(dict(seed=seed, ce_gap=ce_gap, matched=matched, arms=arms))
        print(f"  seed {seed:2d}: CE ctrl={arms['control']['ce']:.4f} "
              f"treat={arms['treatment']['ce']:.4f} oblind={arms['order_blind']['ce']:.4f} "
              f"|gap|={ce_gap:.4f} matched={matched} | "
              f"recov_rho treat={arms['treatment']['recov_rho']:.3f} "
              f"ctrl={arms['control']['recov_rho']:.3f} "
              f"(elapsed {time.time()-t0:.1f}s)", flush=True)
    return rows, time.time() - t0


def decide(rows):
    matched = [r for r in rows if r["matched"]]
    n_matched = len(matched)
    degenerate = n_matched < 10

    def arm_vals(arm, key):
        return np.array([r["arms"][arm][key] for r in matched], float)

    out = dict(n_matched=n_matched, n_total=len(rows), degenerate=degenerate)
    if degenerate:
        out["token"] = "DEGENERATE"
        return out

    # paired diffs over matched seeds
    treat_rho = arm_vals("treatment", "recov_rho")
    ctrl_rho = arm_vals("control", "recov_rho")
    ob_rho = arm_vals("order_blind", "recov_rho")
    treat_shuf = arm_vals("treatment", "recov_shuf")

    d_vs_ctrl = cohens_d_paired(treat_rho - ctrl_rho)
    d_vs_ob = cohens_d_paired(treat_rho - ob_rho)
    fshuffle_margin = float((treat_rho - treat_shuf).mean())

    above_ctrl = bool(d_vs_ctrl >= D_RECOV_VS_SHUF)
    above_fshuffle = bool(fshuffle_margin >= F_SHUFFLE_MARGIN)
    above_ob = bool(d_vs_ob >= D_VS_ORDERBLIND)

    out.update(
        treat_rho_mean=float(treat_rho.mean()), ctrl_rho_mean=float(ctrl_rho.mean()),
        ob_rho_mean=float(ob_rho.mean()), treat_shuf_mean=float(treat_shuf.mean()),
        d_treat_vs_ctrl=float(d_vs_ctrl), d_treat_vs_orderblind=float(d_vs_ob),
        fshuffle_margin=fshuffle_margin,
        above_ctrl=above_ctrl, above_fshuffle=above_fshuffle, above_orderblind=above_ob,
        phi_treat_mean=float(arm_vals("treatment", "phi").mean()),
        phi_ctrl_mean=float(arm_vals("control", "phi").mean()),
        phi_ob_mean=float(arm_vals("order_blind", "phi").mean()),
        d_phi_treat_vs_ctrl=float(cohens_d_paired(arm_vals("treatment", "phi") - arm_vals("control", "phi"))),
        tsep_treat_mean=float(arm_vals("treatment", "t_sep").mean()),
        tsep_ctrl_mean=float(arm_vals("control", "t_sep").mean()),
        tsep_ob_mean=float(arm_vals("order_blind", "t_sep").mean()),
        d_tsep_treat_vs_ctrl=float(cohens_d_paired(arm_vals("treatment", "t_sep") - arm_vals("control", "t_sep"))),
    )
    if above_ctrl and above_fshuffle and above_ob:
        out["token"] = "TEMPORAL-AXIS-BUILDS"
    else:
        out["token"] = "TEMPORAL-AXIS-NULL"
    return out


def main():
    print("=" * 92)
    print("H_1055 — Can the temporal/agency axis be BUILT INTO TRAINING?")
    print("substrate=SW (numpy CPU toy Elman RNN, manual BPTT, $0 CPU) | g5 CODE-measured (p7)")
    print("ARMS: CONTROL(shuffled,uniform) vs TREATMENT(depth-order+depth-weight) vs")
    print("      ORDER-BLIND(depth-weight only, shuffled). Pinned init per seed; matched CE.")
    print("M1 recoverability = CV ridge decode of provenance-depth from trained hidden + F-SHUFFLE floor")
    print("M2 faithful Phi (a_phi_iit4_tool, stdlib exact n<=5, NO proxy) | M3 H_1051 agency-T separation")
    print(f"seeds={N_SEEDS} eps_CE={EPS_CE} | margins: d(treat-ctrl)>={D_RECOV_VS_SHUF}, "
          f"F-shuffle>={F_SHUFFLE_MARGIN}, d(treat-orderblind)>={D_VS_ORDERBLIND}")
    print("a_scale_honest_scope: TOY n<=5 SW; transfer+on-chip UNVERIFIED. NOT a forge binary.")
    print("=" * 92, flush=True)
    print()

    ok, phi_lines = prove_phi_mirror()
    for ln in phi_lines:
        print(ln)
    print(flush=True)
    if not ok:
        raise SystemExit("phi-mirror ==stdlib proof FAILED — aborting (a_phi_iit4_tool)")

    print(f"STEP 1 — train 3 arms x {N_SEEDS} seeds from identical pinned init (SERIAL):", flush=True)
    rows, wall = run()
    print()
    res = decide(rows)

    lines = []
    lines.append("H_1055 — CAN THE TEMPORAL/AGENCY AXIS BE BUILT INTO TRAINING?")
    lines.append("=" * 76)
    lines.append("temporal-curriculum (depth-ordered) + provenance-depth-weighted loss vs a")
    lines.append("matched-CE shuffled control vs an order-blind (depth-weight-only) baseline:")
    lines.append("does the TRAINED hidden state acquire a RECOVERABLE agency-T (provenance-depth)")
    lines.append("coordinate the control lacks, beyond generic curriculum-optimization?")
    lines.append("")
    lines.append(f"timestamp_utc : {datetime.now(timezone.utc).isoformat()}")
    lines.append("substrate     : SW-only CPU toy Elman RNN (a_lane_akida_gpu_split: no AKIDA Lane A; no GPU Lane G)")
    lines.append(f"design        : {N_SEEDS} seeds x 3 arms; pinned init per seed; {N_SAMPLES} samples/seed;")
    lines.append(f"                sample_len={SAMPLE_LEN} HID={HID} epochs={N_EPOCHS} lr={LR}")
    lines.append(f"matched-CE    : eps={EPS_CE} nats | n_matched={res['n_matched']}/{res['n_total']}")
    lines.append("")
    lines.append("── STEP 0: faithful_phi mirror ==stdlib (n=4 AND n=5) ──────────────────────")
    for ln in phi_lines:
        lines.append("  " + ln)
    lines.append("")
    if res["degenerate"]:
        lines.append("── VERDICT ─────────────────────────────────────────────────────────────────")
        lines.append(f"  DEGENERATE — fewer than 10 matched-CE seeds (n_matched={res['n_matched']}).")
        lines.append("  The arms could NOT be matched on task-performance; the CONTROL failed, not the")
        lines.append("  hypothesis. INCONCLUSIVE (neither PASS nor FAIL). VERDICT-TOKEN: DEGENERATE")
    else:
        lines.append("── M1 RECOVERABILITY (CV ridge decode of provenance-depth, matched-CE seeds) ─")
        lines.append(f"  treatment   recov_rho mean = {res['treat_rho_mean']:+.4f}  "
                     f"(F-shuffle floor = {res['treat_shuf_mean']:+.4f})")
        lines.append(f"  control     recov_rho mean = {res['ctrl_rho_mean']:+.4f}  (shuffled-order, uniform)")
        lines.append(f"  order-blind recov_rho mean = {res['ob_rho_mean']:+.4f}  (depth-weight only, shuffled)")
        lines.append(f"  paired d(treatment - control)     = {res['d_treat_vs_ctrl']:+.3f}  "
                     f"(>= {D_RECOV_VS_SHUF}? {res['above_ctrl']})")
        lines.append(f"  paired d(treatment - order-blind) = {res['d_treat_vs_orderblind']:+.3f}  "
                     f"(>= {D_VS_ORDERBLIND}? {res['above_orderblind']})")
        lines.append(f"  F-shuffle margin (treat rho - treat shuffle) = {res['fshuffle_margin']:+.4f}  "
                     f"(>= {F_SHUFFLE_MARGIN}? {res['above_fshuffle']})")
        lines.append("")
        lines.append("── M2 faithful Phi (a_phi_iit4_tool, exact n<=5, NO proxy) ──────────────────")
        lines.append(f"  Phi mean: treatment={res['phi_treat_mean']:.4f} control={res['phi_ctrl_mean']:.4f} "
                     f"order-blind={res['phi_ob_mean']:.4f}")
        lines.append(f"  paired d_Phi(treatment - control) = {res['d_phi_treat_vs_ctrl']:+.3f}")
        lines.append("")
        lines.append("── M3 H_1051 agency-T separation (active vs passive, trained geometry) ──────")
        lines.append(f"  t_sep mean: treatment={res['tsep_treat_mean']:.4f} control={res['tsep_ctrl_mean']:.4f} "
                     f"order-blind={res['tsep_ob_mean']:.4f}")
        lines.append(f"  paired d_tsep(treatment - control) = {res['d_tsep_treat_vs_ctrl']:+.3f}")
        lines.append("")
        lines.append("── VERDICT (pre-registered falsifier, CODE-decided — p7) ────────────────────")
        if res["token"] == "TEMPORAL-AXIS-BUILDS":
            lines.append("  PASS — at MATCHED task-performance, temporal-curriculum + provenance-depth-")
            lines.append("  weighted training makes the agency-T axis RECOVERABLE from the trained hidden")
            lines.append(f"  state ABOVE the shuffled control (d={res['d_treat_vs_ctrl']:+.3f} >= {D_RECOV_VS_SHUF}, "
                         f"F-shuffle margin {res['fshuffle_margin']:+.3f} >= {F_SHUFFLE_MARGIN})")
            lines.append(f"  AND beats the order-blind baseline (d={res['d_treat_vs_orderblind']:+.3f} >= "
                         f"{D_VS_ORDERBLIND}) — it is the temporal/causal ORDER STRUCTURE, not curriculum-")
            lines.append("  optimization. The agency axis CAN be built into learning. VERDICT-TOKEN: TEMPORAL-AXIS-BUILDS")
        else:
            reasons = []
            if not res["above_ctrl"]:
                reasons.append(f"treatment-vs-control d={res['d_treat_vs_ctrl']:+.3f} < {D_RECOV_VS_SHUF}")
            if not res["above_fshuffle"]:
                reasons.append(f"F-shuffle margin {res['fshuffle_margin']:+.3f} < {F_SHUFFLE_MARGIN}")
            if not res["above_orderblind"]:
                reasons.append(f"treatment-vs-order-blind d={res['d_treat_vs_orderblind']:+.3f} < {D_VS_ORDERBLIND} "
                               f"(curriculum-optimization explains it)")
            lines.append("  FAIL (CLOSED-NEGATIVE) — at MATCHED task-performance, no recoverable agency")
            lines.append("  structure emerges beyond the matched-CE shuffled control / order-blind baseline.")
            lines.append("  Reason(s): " + "; ".join(reasons) + ".")
            lines.append("  Temporal ordering does NOT build an agency axis at toy scale, consistent with the")
            lines.append("  optimization-not-Phi wall (H_1011) + learning-axis nulls (H_1052/H_1053).")
            lines.append("  a_paper_negative_ok. VERDICT-TOKEN: TEMPORAL-AXIS-NULL")
    lines.append("")
    lines.append("── HONEST scope (a_scale_honest_scope · a_toy_scale_recheck · a_lane_akida_gpu_split) ──")
    lines.append("  TOY n<=5 SW substrate. faithful Phi EXACT n<=5; CPU mirror RE-PROVEN ==stdlib at n=4")
    lines.append("  AND n=5 (a_phi_iit4_tool; no proxy) BEFORE scoring. AKIDA Lane A on-chip curriculum =")
    lines.append("  SEPARATE rung (note only). Offline research probe — does NOT wire into anima runtime")
    lines.append("  training (p8 is the LIVE-substrate philosophy; a_core_engine_map). g5 CODE-measured (p7).")
    lines.append(f"  total wall: {wall:.1f}s. $0 CPU-local. NOT a forge binary.")
    lines.append("")

    record = dict(h_id="H_1055", title="can the temporal/agency axis be built into training",
                  timestamp_utc=datetime.now(timezone.utc).isoformat(),
                  substrate="SW-only CPU toy Elman RNN", g5_code_measured=True, llm="none",
                  n_seeds=N_SEEDS, eps_ce=EPS_CE, n_samples=N_SAMPLES, sample_len=SAMPLE_LEN,
                  hid=HID, epochs=N_EPOCHS, lr=LR, chain_links=CHAIN_LINKS, n_units=N_UNITS,
                  d_recov_vs_shuf=D_RECOV_VS_SHUF, f_shuffle_margin=F_SHUFFLE_MARGIN,
                  d_vs_orderblind=D_VS_ORDERBLIND, phi_mirror_proven=ok,
                  result=res, rows=rows, total_wall_sec=wall)

    def _jsonable(o):
        if isinstance(o, (np.bool_,)):
            return bool(o)
        if isinstance(o, (np.integer,)):
            return int(o)
        if isinstance(o, (np.floating,)):
            return float(o)
        if isinstance(o, np.ndarray):
            return o.tolist()
        raise TypeError(f"not serializable: {type(o)}")

    lines.append("── full machine record (JSON) ──────────────────────────────────────────────")
    lines.append(json.dumps(record, indent=2, ensure_ascii=False, default=_jsonable))

    vdir = os.path.join(_REPO, ".verdicts", "1055_temporal_curriculum_axis")
    os.makedirs(vdir, exist_ok=True)
    vpath = os.path.join(vdir, "H_1055.txt")
    with open(vpath, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")
    rpath = os.path.join(_HERE, "h1055_temporal_curriculum_axis_result.json")
    with open(rpath, "w", encoding="utf-8") as fh:
        json.dump(record, fh, indent=2, default=_jsonable)

    print("\n".join(lines))
    print(f"\n[written] {vpath}")
    print(f"[written] {rpath}")
    return record


if __name__ == "__main__":
    main()
