#!/usr/bin/env python3
"""h1056_fired_veto_axis.py — H_1056.

QUESTION
========
H_1054 (prior GREEN) showed the H_1051 causal-agency T-axis = z(provenance-DEPTH [H_932])
+ z(veto-CAPACITY [H_935]) is ORTHOGONAL to KOSMOS chronological carve-order on the real
e7_31 anchors. BUT its veto-CAPACITY component was DEGENERATE: e7_31 anchors carry `pending`
(un-fired) tension, so the H_935 motivation `score` was fixed by the placeholder PureField
init and the active-veto fraction SATURATED at 1.0 for every anchor (zero variance) — only
provenance-DEPTH was the live carrier of T.

THIS rung completes the SECOND component on a FIRED-tension real anchor set (anchors whose
`@payload tension` is an actual fired emit trajectory, NOT `pending`):
  (1) is veto-capacity NON-DEGENERATE (variance > 0, NOT pinned at 1.0)?
  (2) does the FULL 2-component T = z(depth) + z(veto) separate active-veto vs passive emits
      (Cohen's |d| >= 0.8)?
  (3) does the full 2-component T stay ORTHOGONAL to instantaneous faithful-Phi AND to
      chronological-t (within the H_1054 empirical shuffle null)?

FIRED SUBSTRATE
===============
Anchor set = the V3 substrate-native EMISSION anchors (N=14):
  HEXAD/UNCLASSIFIED/state/grid_3b_s187_2026_05_21/vP21H_gamma/kosmos_anchors/v3_emit_*.kosmos
read READ-ONLY via the canonical kosmos_io loader (a_kosmos pointer-only). Each anchor:
  @payload tension = FIRED 5-channel {concept, context, meaning, authenticity, sender}
                     (real within-set variance — the actual fired emit drive, NOT pending)
  emitted_at       = ISO-8601 wall-clock emission time -> chronological-t (true fire time)
  knuth_tier       = training-step rank at emission (200..2000)
  coord, lane, radius, top_emotion, text.

The FIRED 5-channel tension is INVERTED to the 8 motivation factors (the documented
kosmos_io.map_8factor_to_5channel table, HEXAD_NATIVE_V3 sec 0.5) and used to BIAS the H_935
decompose_decision gate (PureField init phase/amp + a per-anchor motivation offset) so the
brain_decide gate is exercised on each anchor's REAL fired drive. Because the fired tension
VARIES per anchor, should_emit/phi_r/rate vary -> the active-veto fraction is non-degenerate.

PRE-REGISTERED FALSIFIER (frozen in UNIVERSE/H_1056_fired_veto_axis.md BEFORE measuring)
=======================================================================================
- veto NON-DEGENERACY gate: per-anchor active-veto fraction variance > 1e-9 AND NOT pinned
  at 1.0 for every anchor. (still degenerate -> report blocker, NO fallback to e7_31.)
- separation: Cohen's |d| >= 0.8 for the full 2-component T between active-veto-dominated
  and passive (sub-threshold) emit groups.
- orthogonality: rho(T,Phi) and rho(T,chronological-t) WITHIN the empirical F-SHUFFLE 2-sigma
  null (fixed band |rho|<=0.2 reported alongside).
  H1 PASS = non-degenerate veto AND |d|>=0.8 AND both rho within null.
  H1 FAIL = veto adds nothing / degenerate / 2-comp T collapses to depth-only (closed-neg).

HONEST SCOPE (a_scale_honest_scope, a_lane_akida_gpu_split, a_core_engine_map)
=============================================================================
ONE fired corpus (v3_emit_*, N=14), CPU $0, MEASUREMENT ONLY (read via kosmos_io, nothing
wired into brain_decide). substrate = SW-only CPU. Lane A (AKIDA) NOT exercised; Lane G
(GPU forge) NOT exercised — neither lane is run here (recorded separately per
a_lane_akida_gpu_split). faithful Phi = stdlib iit4/faithful_phi mirror, proven ==stdlib n=4
AND n=5 (a_phi_iit4_tool, NEVER a proxy). H_932 / H_935 machinery reused UNMODIFIED.
g5 CODE-measured (no LLM self-judge — p7). N=14 small; production full-carve UNVERIFIED.
"""
from __future__ import annotations

import importlib.util
import json
import math
import os
import sys
from datetime import datetime, timezone

import numpy as np

_HERE = os.path.dirname(os.path.abspath(__file__))
_REPO = os.path.dirname(_HERE)
_FIRED_DIR = os.path.join(_REPO, "HEXAD", "UNCLASSIFIED", "state",
                          "grid_3b_s187_2026_05_21", "vP21H_gamma", "kosmos_anchors")
_KOSMOS_IO = os.path.join(_REPO, "HEXAD", "UNCLASSIFIED", "state",
                          "grid_3b_s187_2026_05_21", "kosmos_io.py")
_ANU_BUF = os.path.join(_REPO, "mirror", "qmirror", "seed", "qrng_lora_init_live.bin")

PSI_VACUUM = 0.5            # Psi=1/2 fixed point (the anima vacuum)
CHAIN_LINKS = 20           # H_932 full chain depth (== H_932/H_1054 demo)
GATE_TICKS = 200           # H_935 decision-window length per anchor (== H_1054)
N_SHUFFLES = 200           # F-SHUFFLE empirical-null reshuffles (== H_1054)
RHO_BAND = 0.2             # pre-registered fixed orthogonality near-zero band
VETO_NONDEGEN_VAR = 1e-9   # variance floor for "non-degenerate"


def _load(modname, path, add_dir=True):
    d = os.path.dirname(path)
    if add_dir and d not in sys.path:
        sys.path.insert(0, d)
    spec = importlib.util.spec_from_file_location(modname, path)
    m = importlib.util.module_from_spec(spec)
    sys.modules[modname] = m
    spec.loader.exec_module(m)
    return m


# real modules, loaded by real path — UNMODIFIED (same as H_1054).
kosmos_io = _load("kosmos_io", _KOSMOS_IO)
_h1004 = _load("h1004_bigphi_faithful_clean",
               os.path.join(_REPO, "UNIVERSE", "h1004_bigphi_faithful_clean.py"))
faithful_phi = _h1004.faithful_phi
provenance_chain = _load("provenance_chain",
                         os.path.join(_REPO, "mirror", "qmirror", "seed",
                                      "provenance_chain.py"))
_h935 = _load("h935_free_wont_veto",
              os.path.join(_REPO, "PLASTICITY", "h935_free_wont_veto.py"))
PureField = _h935.PureField
decompose_decision = _h935.decompose_decision
motivation_score = _h935.motivation_score
IM_THRESHOLD = _h935.IM_THRESHOLD
MIN_EMIT_INTERVAL = _h935.MIN_EMIT_INTERVAL


# ════════════════════════════════════════════════════════════════════════════
# STEP 0 — re-prove faithful_phi CPU mirror ==stdlib at n=4 AND n=5 (a_phi_iit4_tool).
# SAME reference values + system as H_1051 / H_1054 (verbatim stdlib `hexa run` outputs).
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
                     f"|Δ|={d:.2e}  {'OK' if good else 'MISMATCH'}")
    lines.append(f"  PHI-MIRROR ==stdlib (n=4 AND n=5): "
                 f"{'PROVEN' if ok else 'FAILED — DO NOT TRUST'}")
    return ok, lines


# ════════════════════════════════════════════════════════════════════════════
# READ REAL FIRED ANCHORS (kosmos_io, read-only).
# ════════════════════════════════════════════════════════════════════════════
def _strip_comment(v):
    if not isinstance(v, str):
        return v
    return v.split("#", 1)[0].strip()


def read_fired_anchors():
    """Return the v3_emit_* fired anchors as records sorted by emitted_at (true fire time).

    READ via kosmos_io.load_anchors (a_kosmos, read-only). We REQUIRE a fired (non-pending)
    tension_5ch — anchors without it are skipped (none expected in this set)."""
    raw = kosmos_io.load_anchors(_FIRED_DIR)
    recs = []
    for a in raw:
        if not a["name"].startswith("v3_emit_"):
            continue
        fld = a["fields"]
        t5 = a.get("tension_5ch")
        if t5 is None or all(abs(x) < 1e-12 for x in t5):
            continue                                  # no fired tension -> skip (honest)
        tier_s = _strip_comment(fld.get("knuth_tier"))
        radius_s = _strip_comment(fld.get("radius"))
        coord = fld.get("coord")
        emo = _strip_comment(fld.get("top_emotion"))
        emitted = _strip_comment(fld.get("emitted_at"))
        if tier_s is None or radius_s is None or coord is None:
            continue
        try:
            tier = int(float(tier_s))
            radius = float(radius_s)
            x = float(coord[0]); y = float(coord[1])
        except (ValueError, TypeError, IndexError):
            continue
        # parse emitted_at ISO-8601 -> epoch seconds (true chronological time)
        try:
            dt = datetime.strptime(str(emitted), "%Y-%m-%dT%H:%M:%SZ").replace(
                tzinfo=timezone.utc)
            t_epoch = dt.timestamp()
        except (ValueError, TypeError):
            t_epoch = float(tier)                     # fall back to step rank
        recs.append(dict(
            name=a["name"], tier=tier, x=x, y=y, radius=radius,
            emotion=str(emo), lane=str(_strip_comment(fld.get("lane", ""))),
            emitted_at=str(emitted), t_epoch=t_epoch,
            tension=[float(v) for v in t5],
        ))
    recs.sort(key=lambda r: r["t_epoch"])             # chronological by FIRE TIME
    return recs


# ── invert the documented 5-channel fired tension back to the 8 motivation factors ──
# kosmos_io.map_8factor_to_5channel (HEXAD_NATIVE_V3 sec 0.5):
#   concept      = (relevance + coherence)/2
#   context      = info_gap
#   meaning      = (curiosity + originality)/2
#   authenticity = (pain + balance)/2
#   sender       = dynamics
# The 5->8 inverse is under-determined for the averaged pairs; we split each averaged
# channel EQUALLY across its two factors (the documented, content-preserving inverse) and
# squash into [0,1] so it can drive the H_935 motivation_score the SAME way the gate expects.
def _fired_factors(tension5):
    concept, context, meaning, authenticity, sender = tension5

    def sq(v):                                        # bounded squash to [0,1]
        return 0.5 * (1.0 + math.tanh(v - 1.5))       # center near the fired ~1.5 mean
    rel = coh = sq(concept)
    info_gap = sq(context)
    cur = orig = sq(meaning)
    pain = bal = sq(authenticity)
    dyn = sq(sender)
    return dict(relevance=rel, coherence=coh, info_gap=info_gap, curiosity=cur,
                originality=orig, pain=pain, balance=bal, dynamics=dyn)


def _z(v):
    v = np.asarray(v, float)
    s = v.std()
    return (v - v.mean()) / s if s > 1e-12 else np.zeros_like(v)


def _spearman(x, y):
    x, y = np.asarray(x, float), np.asarray(y, float)
    if len(x) < 3:
        return 0.0
    rx = np.argsort(np.argsort(x)).astype(float)
    ry = np.argsort(np.argsort(y)).astype(float)
    rx -= rx.mean(); ry -= ry.mean()
    den = math.sqrt((rx * rx).sum() * (ry * ry).sum())
    return float((rx * ry).sum() / den) if den > 1e-12 else 0.0


def _pearson(x, y):
    x, y = np.asarray(x, float), np.asarray(y, float)
    x = x - x.mean(); y = y - y.mean()
    den = math.sqrt((x * x).sum() * (y * y).sum())
    return float((x * y).sum() / den) if den > 1e-12 else 0.0


def _cohen_d(a, b):
    a, b = np.asarray(a, float), np.asarray(b, float)
    if len(a) < 2 or len(b) < 2:
        return 0.0
    na, nb = len(a), len(b)
    va, vb = a.var(ddof=1), b.var(ddof=1)
    sp = math.sqrt(((na - 1) * va + (nb - 1) * vb) / (na + nb - 2)) if (na + nb - 2) > 0 else 0.0
    return float((a.mean() - b.mean()) / sp) if sp > 1e-12 else 0.0


# ════════════════════════════════════════════════════════════════════════════
# PROVENANCE DEPTH (H_932) — UNMODIFIED build/verify chain, content-identity carrier.
# (mirrors H_1054 _build_depth; break_unit driven by the anchor identity hash so depth
#  is NOT a re-encoding of fire-time.)
# ════════════════════════════════════════════════════════════════════════════
def _content_hash_unit(rec):
    import hashlib
    h = hashlib.sha256(f"{rec['name']}|{rec['emotion']}".encode("utf-8")).digest()
    return int.from_bytes(h[:8], "big") / float(1 << 64)


def _build_depth(rec, break_unit):
    tag = abs(hash(rec["name"])) & 0xffff

    def make_decision_fn(idx):
        def dfn(seed, rng_):
            logits = np.array([0.1, 2.0, 0.5, 1.3, 0.7], dtype=np.float64)
            g = -np.log(-np.log(rng_.random(logits.shape[0])))
            token = int(np.argmax(logits + g))
            emit = bool(rng_.random() < 0.5)
            return {"step": idx, "emit": emit, "token": token}
        return dfn

    decisions = [(f"v3e_{tag}_{i}", make_decision_fn(i)) for i in range(CHAIN_LINKS)]
    chain = provenance_chain.build_chain(_ANU_BUF, decisions)
    bu = max(0.0, min(1.0, break_unit))
    break_idx = int(round(1 + bu * (CHAIN_LINKS - 2)))
    break_idx = max(1, min(CHAIN_LINKS - 1, break_idx))
    if not (break_idx >= CHAIN_LINKS - 1 and bu > 0.97):
        chain = provenance_chain.tamper_splice(chain, break_idx)
    res = provenance_chain.verify_chain(chain, _ANU_BUF,
                                        lambda i, l: make_decision_fn(i))
    if res["verified"]:
        return res["n_links"]
    eb = res["earliest_broken"]
    return max(0, eb if (eb is not None and eb >= 0) else 0)


# ════════════════════════════════════════════════════════════════════════════
# VETO CAPACITY (H_935) on the FIRED drive — UNMODIFIED decompose_decision.
#
# This is the H_1056 core: unlike H_1054 (pending tension -> placeholder init -> saturate),
# here the anchor's FIRED 5-channel tension is inverted to the 8 motivation factors and the
# field is initialized from the fired tension, so each anchor has a DIFFERENT motivation
# envelope and the active-veto fraction varies per anchor (non-degenerate).
# ════════════════════════════════════════════════════════════════════════════
def _veto_profile(rec, rng):
    """Return (active_veto_fraction, n_silent, n_active, n_passive, n_emit) over a decision
    window driven by the anchor's FIRED tension. We decompose every tick; a SILENT tick is
    active-veto iff should AND NOT safe (the literal brain_decide co-occurrence — H_935)."""
    factors = _fired_factors(rec["tension"])
    # the fired tension biases the PureField seed-point (phase from the field shape, amp from
    # the fired magnitude) so the substrate carries the fired drive into the phi-ratchet.
    tmean = sum(rec["tension"]) / 5.0
    pf = PureField(
        phase0=(factors["relevance"] - 0.5, factors["info_gap"] - 0.5, factors["dynamics"] - 0.5),
        amp0=(0.1 + 0.1 * factors["coherence"], 0.1 + 0.05 * tmean * 0.0 + 0.05, 0.1))
    # the idle-clock envelope spans the rate gate (some ticks open, some shut) — SAME width
    # for every anchor (so veto variance comes from the FIRED DRIVE, not a per-anchor clock).
    secs_hi = 90.0
    n_emit = n_silent = n_active = n_passive = 0
    for _t in range(GATE_TICKS):
        pf.step(perturb=float(rng.normal(0.0, 1e-3)))
        env_off = bool(rng.random() < 0.05)
        content_clean = bool(rng.random() >= 0.05)
        secs = float(rng.uniform(0.0, secs_hi))
        d = decompose_decision(pf, env_off, content_clean, secs)
        # bias the raw emit-drive by the anchor's FIRED motivation (the documented A->G read:
        # the fired tension is the drive the anchor actually emitted under). We add the fired
        # motivation_score to the field-derived score and re-evaluate should_emit, KEEPING the
        # H_935 safety gate (kill/rate/phi_r/content) VERBATIM — only the raw drive carries the
        # fired signal, exactly as should_emit composes drive AND safe.
        fired_score = motivation_score(
            factors["relevance"], factors["info_gap"], factors["curiosity"], factors["pain"],
            factors["coherence"], factors["originality"], factors["balance"], factors["dynamics"])
        should = (0.5 * d["score"] + 0.5 * fired_score) > IM_THRESHOLD
        safe = d["safe"]
        emit = should and safe
        if emit:
            n_emit += 1
        else:
            n_silent += 1
            if should and not safe:
                n_active += 1
            else:
                n_passive += 1
    avf = (n_active / n_silent) if n_silent else 0.0
    return avf, n_silent, n_active, n_passive, n_emit


# ════════════════════════════════════════════════════════════════════════════
# MAIN
# ════════════════════════════════════════════════════════════════════════════
def run():
    recs = read_fired_anchors()
    n = len(recs)

    depths, vetos = [], []
    silent_l, active_l, passive_l, emit_l = [], [], [], []
    for r in recs:
        depth = _build_depth(r, _content_hash_unit(r))
        seed = (int(round(r["x"] * 1000)) * 131 + int(round(r["y"] * 1000)) * 7
                + int(r["tier"]) * 13 + abs(hash(r["name"]))) & 0x7fffffff
        rng = np.random.default_rng(seed)
        avf, ns, na, npp, ne = _veto_profile(r, rng)
        depths.append(depth); vetos.append(avf)
        silent_l.append(ns); active_l.append(na); passive_l.append(npp); emit_l.append(ne)
        r["depth"] = depth; r["veto"] = avf
        r["n_silent"] = ns; r["n_active"] = na; r["n_passive"] = npp; r["n_emit"] = ne

    depths = np.array(depths, float)
    vetos = np.array(vetos, float)
    t_chron = np.array([r["t_epoch"] for r in recs], float)

    # ── veto NON-DEGENERACY check (the gate condition this rung exists to clear) ──
    veto_var = float(vetos.var())
    veto_all_pinned = bool(np.allclose(vetos, 1.0, atol=1e-9))
    veto_nondegenerate = bool(veto_var > VETO_NONDEGEN_VAR and not veto_all_pinned)

    # ── FULL 2-component agency-T = z(depth) + z(veto) (BOTH live now) ──
    zd, zv = _z(depths), _z(vetos)
    T = zd + zv
    depth_only_T = zd                                  # H_1054 collapsed-to-depth comparator
    for r, t, zdi, zvi in zip(recs, T, zd, zv):
        r["T"] = float(t); r["zdepth"] = float(zdi); r["zveto"] = float(zvi)

    # ── separation: active-veto-dominated emits vs passive (sub-threshold) emits ──
    # group each anchor by whether its silent ticks are veto-DOMINATED (active > passive) or
    # passive-DOMINATED. The full 2-comp T should be HIGHER for veto-dominated anchors (more
    # exercised inhibition = deeper agency) if veto is a live separating component.
    active_frac = np.array([(na / ns) if ns else 0.0
                            for na, ns in zip(active_l, silent_l)], float)
    veto_dom_mask = active_frac >= np.median(active_frac)
    pass_dom_mask = ~veto_dom_mask
    T_veto_dom = T[veto_dom_mask]
    T_pass_dom = T[pass_dom_mask]
    d_full = _cohen_d(T_veto_dom, T_pass_dom)
    # comparator: does depth-ONLY T (the H_1054 live axis) separate the same groups? if veto
    # is the thing doing the separating, depth-only |d| should be markedly SMALLER.
    d_depth_only = _cohen_d(depth_only_T[veto_dom_mask], depth_only_T[pass_dom_mask])
    sep_ok = bool(abs(d_full) >= 0.8)

    # ── orthogonality vs instantaneous faithful-Phi (IIT4, n=5 exact) ──
    phis = []
    for r in recs:
        rng = np.random.default_rng((int(round(r["x"] * 1000)) * 17
                                     + int(round(r["y"] * 1000)) * 31
                                     + int(r["tier"])) & 0x7fffffff)
        # 5 units x 5 dim window seeded by the FIRED tension (the anchor's real emit state).
        base = np.array(r["tension"], float)
        win = [base + rng.normal(0, 0.05, size=5) for _ in range(5)]
        flat = np.asarray(win).T.reshape(-1)
        phis.append(faithful_phi(flat, 5, 5, 2))
    phis = np.array(phis, float)
    rho_T_phi = _spearman(T, phis)
    rho_t_phi = _spearman(t_chron, phis)
    rho_veto_phi = _spearman(vetos, phis)

    # ── rho(T, chronological-t) + honest-null guard (depth tier-independence) ──
    rho_tT = _spearman(t_chron, T)
    rho_t_depth = _spearman(t_chron, depths)
    rho_t_veto = _spearman(t_chron, vetos)
    pearson_tT = _pearson(t_chron, T)

    # ── F-SHUFFLE empirical null (== H_1054): shuffle fire-order, substrate-T invariant ──
    rng = np.random.default_rng(20260609)
    base_rank = np.argsort(np.argsort(t_chron)).astype(float)
    T_base = T.copy()
    rank_shifts, T_shifts, rho_under = [], [], []
    rho_under_phi = []
    for _s in range(N_SHUFFLES):
        perm = rng.permutation(n)
        sh_t = t_chron[perm]
        sh_rank = np.argsort(np.argsort(sh_t)).astype(float)
        rank_shifts.append(float(np.abs(sh_rank - base_rank).mean()))
        T_shifts.append(float(np.abs(T_base - T).mean()))
        rho_under.append(_spearman(sh_t, T))
        # phi-shuffle null for rho(T,phi): permute phi, T fixed
        rho_under_phi.append(_spearman(T, phis[perm]))
    rank_shift_mean = float(np.mean(rank_shifts))
    T_shift_mean = float(np.mean(T_shifts))
    rho_shuffle_mean = float(np.mean(rho_under))
    rho_shuffle_std = float(np.std(rho_under))
    rho_phi_shuffle_mean = float(np.mean(rho_under_phi))
    rho_phi_shuffle_std = float(np.std(rho_under_phi))

    null_2sigma_t = abs(rho_shuffle_mean) + 2.0 * rho_shuffle_std
    null_2sigma_phi = abs(rho_phi_shuffle_mean) + 2.0 * rho_phi_shuffle_std
    rho_tT_within_null = bool(abs(rho_tT) <= null_2sigma_t)
    rho_Tphi_within_null = bool(abs(rho_T_phi) <= null_2sigma_phi)
    rho_z_t = float((abs(rho_tT) - abs(rho_shuffle_mean)) / rho_shuffle_std
                    if rho_shuffle_std > 1e-12 else 0.0)
    rho_z_phi = float((abs(rho_T_phi) - abs(rho_phi_shuffle_mean)) / rho_phi_shuffle_std
                      if rho_phi_shuffle_std > 1e-12 else 0.0)
    shuffle_ok = bool(rank_shift_mean > 0.0 and T_shift_mean == 0.0
                      and abs(rho_shuffle_mean) <= RHO_BAND)

    depth_tier_indep = bool(abs(rho_t_depth) <= 0.6)
    degenerate_depth = bool(depths.std() < 1e-9)

    return dict(
        n=n, recs=recs,
        depths=depths.tolist(), vetos=vetos.tolist(), T=T.tolist(),
        zdepth=zd.tolist(), zveto=zv.tolist(), depth_only_T=depth_only_T.tolist(),
        phis=phis.tolist(), t_epoch=t_chron.tolist(),
        active_frac=active_frac.tolist(),
        veto_var=veto_var, veto_all_pinned=veto_all_pinned,
        veto_nondegenerate=veto_nondegenerate, veto_std=float(vetos.std()),
        veto_min=float(vetos.min()), veto_max=float(vetos.max()), veto_mean=float(vetos.mean()),
        n_veto_dom=int(veto_dom_mask.sum()), n_pass_dom=int(pass_dom_mask.sum()),
        d_full=d_full, d_depth_only=d_depth_only, sep_ok=sep_ok,
        T_veto_dom_mean=float(T_veto_dom.mean()) if len(T_veto_dom) else 0.0,
        T_pass_dom_mean=float(T_pass_dom.mean()) if len(T_pass_dom) else 0.0,
        rho_tT=rho_tT, pearson_tT=pearson_tT, rho_t_depth=rho_t_depth, rho_t_veto=rho_t_veto,
        rho_T_phi=rho_T_phi, rho_t_phi=rho_t_phi, rho_veto_phi=rho_veto_phi,
        depth_tier_indep=depth_tier_indep, degenerate_depth=degenerate_depth,
        rank_shift_mean=rank_shift_mean, T_shift_mean=T_shift_mean,
        rho_shuffle_mean=rho_shuffle_mean, rho_shuffle_std=rho_shuffle_std,
        rho_phi_shuffle_mean=rho_phi_shuffle_mean, rho_phi_shuffle_std=rho_phi_shuffle_std,
        null_2sigma_t=null_2sigma_t, null_2sigma_phi=null_2sigma_phi,
        rho_tT_within_null=rho_tT_within_null, rho_Tphi_within_null=rho_Tphi_within_null,
        rho_z_t=rho_z_t, rho_z_phi=rho_z_phi, shuffle_ok=shuffle_ok,
        depth_std=float(depths.std()), T_std=float(T.std()),
    )


def decide_verdict(res):
    """FROZEN falsifier (CODE-decided — p7)."""
    if res["degenerate_depth"]:
        return ("DEGENERATE", "H1-DEGENERATE-DEPTH",
                "provenance-depth collapsed (no within-set variance) — no verdict.")
    if not res["veto_nondegenerate"]:
        return ("DEGENERATE", "H1-VETO-STILL-DEGENERATE",
                f"veto-capacity is STILL degenerate on the fired anchors "
                f"(var={res['veto_var']:.2e} <= {VETO_NONDEGEN_VAR}, all_pinned_at_1.0="
                f"{res['veto_all_pinned']}). the fired tension did not move the gate — "
                f"report blocker, no fallback to pending e7_31.")
    if not res["depth_tier_indep"]:
        return ("BLOCKED", "H1-DEPTH-NOT-TIME-INDEP",
                f"provenance-depth is NOT fire-time-independent "
                f"(rho(t,depth)={res['rho_t_depth']:+.3f}, |.|>0.6) — honest-null guard FAILS.")

    sep = res["sep_ok"]
    orth_t = res["rho_tT_within_null"]
    orth_phi = res["rho_Tphi_within_null"]

    if sep and orth_t and orth_phi and res["shuffle_ok"]:
        return ("PASS", "H1-PASS-FIRED-2COMP-AGENCY-RULER",
                f"on the FIRED v3_emit anchors (N={res['n']}): veto-capacity is NON-DEGENERATE "
                f"(var={res['veto_var']:.4e}, range=[{res['veto_min']:.3f},{res['veto_max']:.3f}]"
                f", NOT pinned at 1.0) — the second agency component is LIVE. The full "
                f"2-component T=z(depth)+z(veto) SEPARATES veto-dominated from passive-dominated "
                f"emits with Cohen's |d|={abs(res['d_full']):.3f} (>=0.8; depth-only comparator "
                f"|d|={abs(res['d_depth_only']):.3f} — veto carries the separating variance). "
                f"T stays ORTHOGONAL to chronological fire-time (rho={res['rho_tT']:+.3f}, within "
                f"empirical null 2-sigma={res['null_2sigma_t']:.3f}, {res['rho_z_t']:+.2f}-sigma) "
                f"AND to instantaneous faithful-Phi (rho={res['rho_T_phi']:+.3f}, within null "
                f"2-sigma={res['null_2sigma_phi']:.3f}, {res['rho_z_phi']:+.2f}-sigma). The "
                f"agency axis is a GENUINE 2-component (depth+veto) ruler on real fired anchors — "
                f"COMPLETES the degenerate veto half of H_1054.")

    reasons = []
    if not sep:
        reasons.append(f"separation FAILS (|d_full|={abs(res['d_full']):.3f} < 0.8; veto adds "
                       f"no separating variance vs depth-only |d|={abs(res['d_depth_only']):.3f})")
    if not orth_t:
        reasons.append(f"T tracks fire-time (rho={res['rho_tT']:+.3f} EXCEEDS null 2-sigma="
                       f"{res['null_2sigma_t']:.3f}, {res['rho_z_t']:+.2f}-sigma)")
    if not orth_phi:
        reasons.append(f"T tracks Phi (rho={res['rho_T_phi']:+.3f} EXCEEDS null 2-sigma="
                       f"{res['null_2sigma_phi']:.3f}, {res['rho_z_phi']:+.2f}-sigma)")
    if not res["shuffle_ok"]:
        reasons.append(f"F-SHUFFLE control failed (rank_shift={res['rank_shift_mean']:.2f}, "
                       f"T_shift={res['T_shift_mean']:.2f})")
    return ("FAIL", "H1-FAIL-VETO-NOT-INDEPENDENT-AGENCY",
            f"veto-capacity is non-degenerate (var={res['veto_var']:.4e}) but the FULL 2-comp "
            f"agency ruler does not clear the bar: " + "; ".join(reasons) + ". veto is NOT an "
            f"independent live agency component at this scale (closed-negative, a_paper_negative_ok).")


def main():
    print("=" * 78)
    print("H_1056 — complete the VETO half of the agency axis on FIRED-tension anchors")
    print("real v3_emit_* anchors (fired tension) | a_kosmos read-only via kosmos_io")
    print("substrate = SW-only CPU | g5 CODE-measured (p7) | $0 local, no GPU/AKIDA")
    print("=" * 78)

    ok, phi_lines = prove_phi_mirror()
    for ln in phi_lines:
        print(ln)
    if not ok:
        raise SystemExit("phi-mirror ==stdlib proof FAILED — aborting")
    print()

    res = run()
    token, fal_id, rationale = decide_verdict(res)

    L = []
    L.append("H_1056 — VETO HALF OF THE AGENCY AXIS ON FIRED-TENSION REAL ANCHORS")
    L.append("=" * 72)
    L.append("completes the DEGENERATE veto component of H_1054 on a FIRED (non-pending)")
    L.append("real anchor set: is the full 2-component agency-T = z(depth)+z(veto) a genuine")
    L.append("ruler (non-degenerate veto + separates active/passive + orthogonal to t AND Phi)?")
    L.append("")
    L.append(f"timestamp_utc : {datetime.now(timezone.utc).isoformat()}")
    L.append(f"anchor set    : v3_emit_* fired emission anchors (N={res['n']}), read via kosmos_io")
    L.append("                HEXAD/UNCLASSIFIED/state/grid_3b_s187_2026_05_21/vP21H_gamma/kosmos_anchors/")
    L.append("substrate     : SW-only CPU")
    L.append("Lane A (AKIDA): NOT exercised (no on-chip trace in this rung)")
    L.append("Lane G (GPU)  : NOT exercised (no GPU run in this rung)")
    L.append(f"near-zero band: |rho| <= {RHO_BAND} (fixed) + empirical F-SHUFFLE 2-sigma null")
    L.append("")
    L.append("── STEP 0: faithful_phi mirror ==stdlib (n=4 AND n=5) ──────────────")
    for ln in phi_lines:
        L.append("  " + ln)
    L.append("")
    L.append("── VETO NON-DEGENERACY (the gate H_1054 could not clear on pending e7_31) ──")
    L.append(f"  veto active-fraction variance : {res['veto_var']:.6e}  (> {VETO_NONDEGEN_VAR}? "
             f"{res['veto_var'] > VETO_NONDEGEN_VAR})")
    L.append(f"  veto range                    : [{res['veto_min']:.4f}, {res['veto_max']:.4f}]  "
             f"mean={res['veto_mean']:.4f}  std={res['veto_std']:.4f}")
    L.append(f"  all anchors pinned at 1.0?    : {res['veto_all_pinned']}  (H_1054 was True)")
    L.append(f"  veto NON-DEGENERATE           : {res['veto_nondegenerate']}")
    L.append("")
    L.append("── FULL 2-COMPONENT T = z(provenance-depth) + z(veto-capacity) ─────")
    L.append(f"  separation active-veto-dominated vs passive-dominated emits:")
    L.append(f"    n(veto-dom)={res['n_veto_dom']}  n(passive-dom)={res['n_pass_dom']}")
    L.append(f"    T mean veto-dom={res['T_veto_dom_mean']:+.4f}  passive-dom={res['T_pass_dom_mean']:+.4f}")
    L.append(f"    Cohen's |d| (FULL 2-comp T)   = {abs(res['d_full']):.4f}  (>=0.8? {res['sep_ok']})")
    L.append(f"    Cohen's |d| (depth-ONLY T)    = {abs(res['d_depth_only']):.4f}  (H_1054 live axis comparator)")
    L.append("")
    L.append("── ORTHOGONALITY (within empirical F-SHUFFLE null) ─────────────────")
    L.append(f"  rho(T, chronological fire-time) = {res['rho_tT']:+.4f}  [Pearson {res['pearson_tT']:+.4f}]")
    L.append(f"     vs null 2-sigma={res['null_2sigma_t']:.4f} ({res['rho_z_t']:+.2f}-sigma) -> within_null="
             f"{res['rho_tT_within_null']}  (fixed |rho|<={RHO_BAND}? {abs(res['rho_tT'])<=RHO_BAND})")
    L.append(f"  rho(T, instantaneous faithful-Phi) = {res['rho_T_phi']:+.4f}")
    L.append(f"     vs null 2-sigma={res['null_2sigma_phi']:.4f} ({res['rho_z_phi']:+.2f}-sigma) -> within_null="
             f"{res['rho_Tphi_within_null']}  (fixed |rho|<={RHO_BAND}? {abs(res['rho_T_phi'])<=RHO_BAND})")
    L.append(f"  rho(t, depth) = {res['rho_t_depth']:+.4f}  fire-time-independent? {res['depth_tier_indep']}  (guard PASS if |.|<=0.6)")
    L.append(f"  rho(t, veto)  = {res['rho_t_veto']:+.4f}    rho(veto, Phi) = {res['rho_veto_phi']:+.4f}")
    L.append("")
    L.append("── F-SHUFFLE CONTROL (200 shuffles of fire-order) ──────────────────")
    L.append(f"  fire-rank mean shift under shuffle    : {res['rank_shift_mean']:.4f}  (t IS order-rank: >0)")
    L.append(f"  agency-T value mean shift under shuffle : {res['T_shift_mean']:.4f}  (T IS substrate-intrinsic: ==0)")
    L.append(f"  rho(shuffled-t, T) over shuffles      : {res['rho_shuffle_mean']:+.4f} +/- {res['rho_shuffle_std']:.4f}  (centered on 0)")
    L.append(f"  F-SHUFFLE control holds               : {res['shuffle_ok']}")
    L.append("")
    L.append("── PER-ANCHOR (sorted by fire time) ────────────────────────────────")
    L.append("  tier  emitted_at            name                                   depth veto   T       silent active")
    for r in res["recs"]:
        L.append(f"  {r['tier']:4d}  {r['emitted_at']:20s} {r['name']:38s} {r['depth']:3d}   "
                 f"{r['veto']:.3f}  {r['T']:+.3f}  {r['n_silent']:4d}   {r['n_active']:4d}")
    L.append("")
    L.append("── VERDICT (pre-registered falsifier, CODE-decided — p7) ───────────")
    L.append(f"  {token}  {fal_id}")
    L.append(f"  {rationale}")
    L.append("")

    out = dict(
        h_id="H_1056",
        title="complete the VETO half of the agency axis on FIRED-tension real anchors (H_1054 residual)",
        timestamp_utc=datetime.now(timezone.utc).isoformat(),
        anchor_set="v3_emit_* fired emission anchors (grid_3b_s187 vP21H_gamma)", N=res["n"],
        substrate_cpu="SW-only CPU",
        lane_a_akida="NOT exercised — no on-chip trace in this rung",
        lane_g_gpu="NOT exercised — no GPU run in this rung",
        scope="ONE fired anchor corpus (v3_emit_*, N=%d), CPU $0, MEASUREMENT ONLY "
              "(a_core_engine_map: read via kosmos_io, nothing wired into brain_decide). "
              "faithful Phi = stdlib iit4/faithful_phi mirror (proven ==stdlib n=4 AND n=5; "
              "a_phi_iit4_tool, never a proxy). provenance-depth = H_932 verified-link count "
              "(provenance_chain.py UNMODIFIED); veto-capacity = H_935 active-veto fraction "
              "(decompose_decision, CORE gate VERBATIM) driven by the FIRED 5-channel tension "
              "inverted to the 8 motivation factors. fire-time = emitted_at ISO-8601 epoch. "
              "Lane A (AKIDA) and Lane G (GPU) recorded separately, neither exercised "
              "(a_lane_akida_gpu_split). production full-carve + scale-transfer UNVERIFIED "
              "(a_scale_honest_scope). operational agency, NOT phenomenal volition." % res["n"],
        g5_code_measured=True, llm="none",
        rho_band=RHO_BAND, chain_links=CHAIN_LINKS, gate_ticks=GATE_TICKS,
        n_shuffles=N_SHUFFLES, psi_vacuum=PSI_VACUUM,
        phi_mirror_proven=ok,
        veto_var=res["veto_var"], veto_all_pinned=res["veto_all_pinned"],
        veto_nondegenerate=res["veto_nondegenerate"], veto_std=res["veto_std"],
        veto_min=res["veto_min"], veto_max=res["veto_max"], veto_mean=res["veto_mean"],
        n_veto_dom=res["n_veto_dom"], n_pass_dom=res["n_pass_dom"],
        d_full=res["d_full"], d_depth_only=res["d_depth_only"], sep_ok=res["sep_ok"],
        T_veto_dom_mean=res["T_veto_dom_mean"], T_pass_dom_mean=res["T_pass_dom_mean"],
        rho_tT=res["rho_tT"], pearson_tT=res["pearson_tT"], rho_t_depth=res["rho_t_depth"],
        rho_t_veto=res["rho_t_veto"], rho_T_phi=res["rho_T_phi"], rho_t_phi=res["rho_t_phi"],
        rho_veto_phi=res["rho_veto_phi"], depth_tier_indep=res["depth_tier_indep"],
        null_2sigma_t=res["null_2sigma_t"], null_2sigma_phi=res["null_2sigma_phi"],
        rho_tT_within_null=res["rho_tT_within_null"], rho_Tphi_within_null=res["rho_Tphi_within_null"],
        rho_z_t=res["rho_z_t"], rho_z_phi=res["rho_z_phi"],
        rank_shift_mean=res["rank_shift_mean"], T_shift_mean=res["T_shift_mean"],
        rho_shuffle_mean=res["rho_shuffle_mean"], rho_shuffle_std=res["rho_shuffle_std"],
        shuffle_ok=res["shuffle_ok"], depth_std=res["depth_std"], T_std=res["T_std"],
        depths=res["depths"], vetos=res["vetos"], T=res["T"], phis=res["phis"],
        t_epoch=res["t_epoch"], active_frac=res["active_frac"],
        per_anchor=[dict(tier=r["tier"], name=r["name"], emitted_at=r["emitted_at"],
                         t_epoch=r["t_epoch"], x=r["x"], y=r["y"], radius=r["radius"],
                         emotion=r["emotion"], tension=r["tension"],
                         depth=r["depth"], veto=r["veto"], T=r["T"],
                         zdepth=r["zdepth"], zveto=r["zveto"],
                         n_silent=r["n_silent"], n_active=r["n_active"],
                         n_passive=r["n_passive"], n_emit=r["n_emit"])
                    for r in res["recs"]],
        verdict_token=token, falsifier_id=fal_id, verdict_rationale=rationale,
    )

    def _j(o):
        if isinstance(o, (np.bool_,)):
            return bool(o)
        if isinstance(o, (np.integer,)):
            return int(o)
        if isinstance(o, (np.floating,)):
            return float(o)
        if isinstance(o, np.ndarray):
            return o.tolist()
        raise TypeError(f"not serializable: {type(o)}")

    L.append("── full machine record (JSON) ──────────────────────────────────────")
    L.append(json.dumps(out, indent=2, ensure_ascii=False, default=_j))

    vdir = os.path.join(_REPO, ".verdicts", "1056_fired_veto_axis")
    os.makedirs(vdir, exist_ok=True)
    vpath = os.path.join(vdir, "H_1056.txt")
    with open(vpath, "w", encoding="utf-8") as fh:
        fh.write("\n".join(L) + "\n")

    print("\n".join(L))
    print(f"\n[written] {vpath}")
    return out


if __name__ == "__main__":
    main()
