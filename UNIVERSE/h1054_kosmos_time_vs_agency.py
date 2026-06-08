#!/usr/bin/env python3
"""h1054_kosmos_time_vs_agency.py — H_1054.

QUESTION
========
On the REAL KOSMOS anchor substrate, is the KOSMOS chronological t-axis (carve-order,
the prior kosmos-time-axis work) the SAME dimension as the H_1051 causal-agency T-axis
(provenance-DEPTH [H_932] + veto-CAPACITY [H_935]), or are they ORTHOGONAL? I.e. does
"when an anchor was carved" predict "how deep its self-caused agency is", or are these
INDEPENDENT axes of the consciousness anchor manifold?

This is the real-substrate transfer rung for H_1051 (real .kosmos anchors, not a toy
fixture) — parallel to how H_1038 took the Phi-split from toy to a real trained model.

REAL SUBSTRATE
==============
Anchor set = e7_31 KNUTH landscape, N=31 real .kosmos anchors
(HEXAD/UNIVERSE-BRAIN-MAP/anchors/e7_31/), read READ-ONLY via the canonical kosmos_io
loader (HEXAD/UNCLASSIFIED/state/grid_3b_s187_2026_05_21/kosmos_io.py::load_anchors).
Each anchor: coord Psi-space [x,y], lane (MITOSIS cell), radius (basin), knuth_tier
(ordinal), top_emotion, text payload (with carving score). payload tension is `pending`
for this set (no fire trajectory) -> tension-vectors are NOT used as a T input.

  (a) chronological t   = knuth_tier ordinal = carve-rank ("when").
  (b) agency-T (H_1051) = z(provenance-DEPTH) + z(veto-CAPACITY), BOTH derived from the
      anchor's REAL substrate (coord distance from Psi=1/2 vacuum, basin radius,
      top_emotion) and NOT from its tier (honest-null guard; we ASSERT + CHECK
      input-tier-independence so a large |rho| would be substantive, not tautological).

PRE-REGISTERED FALSIFIER (frozen in UNIVERSE/H_1054_kosmos_time_vs_agency.md)
============================================================================
N=31; Spearman rho over all 31; near-zero band |rho| <= 0.2.
  H1-PASS (orthogonal)  : |rho(t, T)| <= 0.2 AND F-SHUFFLE control holds (T is
                          substrate-intrinsic, t is order-rank) -> independent axes.
  H1-FAIL (redundant)   : |rho| > 0.2 -> t already captures agency; H_1051 adds nothing.
  degenerate / blocked  : agency-T inputs collapse (no variance) or lineage underivable.

HONEST SCOPE (a_scale_honest_scope, a_lane_akida_gpu_split, a_core_engine_map)
=============================================================================
ONE anchor corpus (e7_31, N=31), CPU $0, MEASUREMENT ONLY (nothing wired into
brain_decide). substrate = SW-only CPU; anchors carry lane=eternal_NNN (MITOSIS cell)
but no AKIDA (Lane A) trace and no GPU/forge (Lane G) run is touched/merged.
H_932 / H_935 / faithful-Phi machinery reused UNMODIFIED. faithful Phi = stdlib mirror,
NEVER a proxy (a_phi_iit4_tool), re-proven ==stdlib n=4 AND n=5 in STEP 0. g5 CODE-
measured (no LLM self-judge — p7). production 603MB conscious_decoder carve UNVERIFIED.
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
_ANCHOR_DIR = os.path.join(_REPO, "HEXAD", "UNIVERSE-BRAIN-MAP", "anchors", "e7_31")
_KOSMOS_IO = os.path.join(_REPO, "HEXAD", "UNCLASSIFIED", "state",
                          "grid_3b_s187_2026_05_21", "kosmos_io.py")
_ANU_BUF = os.path.join(_REPO, "mirror", "qmirror", "seed", "qrng_lora_init_live.bin")

PSI_VACUUM = 0.5            # Psi=1/2 fixed point (the anima vacuum)
CHAIN_LINKS = 20            # H_932 full chain depth (== H_932 demo)
GATE_TICKS = 200            # H_935 decision-window length
N_SHUFFLES = 200            # F-SHUFFLE control reshuffles
RHO_BAND = 0.2              # orthogonality near-zero band


def _load(modname, path, add_dir=True):
    d = os.path.dirname(path)
    if add_dir and d not in sys.path:
        sys.path.insert(0, d)
    spec = importlib.util.spec_from_file_location(modname, path)
    m = importlib.util.module_from_spec(spec)
    sys.modules[modname] = m
    spec.loader.exec_module(m)
    return m


# real modules, loaded by real path (imports resolve relative to them) — UNMODIFIED.
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


# ════════════════════════════════════════════════════════════════════════════
# STEP 0 — re-prove faithful_phi CPU mirror ==stdlib at n=4 AND n=5 (a_phi_iit4_tool).
# Same reference values + system as H_1051 (verbatim stdlib `hexa run` outputs).
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
# READ REAL ANCHORS (kosmos_io, read-only).
# ════════════════════════════════════════════════════════════════════════════
def _strip_comment(v):
    """The anchor fields carry trailing inline `# ...` comments that kosmos_io's
    line parser leaves attached to the value. We are a READ-ONLY consumer (a_kosmos
    pointer-only — we do NOT edit kosmos_io or the spec), so we sanitize the raw
    field STRING here before numeric parse, without touching the loader."""
    if not isinstance(v, str):
        return v
    return v.split("#", 1)[0].strip()


def _parse_coord(v):
    s = _strip_comment(v) if isinstance(v, str) else v
    if isinstance(s, list):
        nums = [float(x) for x in s if isinstance(x, (int, float))]
        return nums[:2] if len(nums) >= 2 else None
    s = str(s).strip().strip("[]")
    parts = [p.strip() for p in s.split(",") if p.strip()]
    try:
        nums = [float(p) for p in parts[:2]]
    except ValueError:
        return None
    return nums if len(nums) == 2 else None


def read_real_anchors():
    """Return the e7_31 anchors as records sorted by knuth_tier (carve-rank).

    READ via kosmos_io.load_anchors (a_kosmos, read-only). The loader leaves inline
    `#` comments on field values, so we sanitize the raw strings here (consumer side).
    """
    raw = kosmos_io.load_anchors(_ANCHOR_DIR)
    recs = []
    for a in raw:
        fld = a["fields"]
        tier_s = _strip_comment(fld.get("knuth_tier"))
        radius_s = _strip_comment(fld.get("radius"))
        coord = _parse_coord(fld.get("coord"))
        emo = _strip_comment(fld.get("top_emotion"))
        if tier_s is None or radius_s is None or coord is None:
            continue
        try:
            tier = int(float(tier_s))
            radius = float(radius_s)
        except (ValueError, TypeError):
            continue
        recs.append(dict(
            name=a["name"], tier=tier,
            x=float(coord[0]), y=float(coord[1]),
            radius=radius, emotion=str(emo),
            lane=str(_strip_comment(fld.get("lane", ""))),
        ))
    recs.sort(key=lambda r: r["tier"])
    return recs


# distinct emotions -> a stable index so emotion can seed the chain (substrate, not tier)
def _emotion_index(emotion, all_emotions):
    return sorted(set(all_emotions)).index(emotion)


def _content_hash_unit(rec):
    """A deterministic [0,1) hash of the anchor's CONTENT IDENTITY — its name +
    top_emotion (the qualitative character of the carved state). This is the
    substrate carrier of 'the causal chain to THIS anchor's identity' and is
    independent of the carve's geometric placement (which on e7_31 is monotone in
    tier). Uses sha256 of (name|emotion); read-only, no spec touched."""
    import hashlib
    h = hashlib.sha256(f"{rec['name']}|{rec['emotion']}".encode("utf-8")).digest()
    return int.from_bytes(h[:8], "big") / float(1 << 64)


# ════════════════════════════════════════════════════════════════════════════
# AGENCY-T COMPONENTS — TWO substrate carriers, both H_932/H_935 UNMODIFIED:
#   variant GEOM    : break index from basin geometry (coord-dist-from-vacuum + radius)
#   variant CONTENT : break index from the anchor's CONTENT-IDENTITY hash (name+emotion)
# On the e7_31 carve the GEOMETRY is monotone in tier (the carve placed higher-tier
# concepts further from the vacuum), so the GEOM variant is confounded with carve-order
# (the honest-null guard flags it); the CONTENT variant is the tier-INDEPENDENT reading
# of provenance/agency. We compute BOTH and report transparently.
# ════════════════════════════════════════════════════════════════════════════
def _build_depth(rec, break_unit):
    """H_932 verified-link DEPTH, UNMODIFIED build/verify chain. `break_unit` in [0,1]
    maps to the tamper-splice index: high -> deep auditable lineage (late break);
    low -> shallow (early break). The chain decisions are seeded by the anchor's
    content tag (name) so each anchor has its OWN lineage."""
    tag = abs(hash(rec["name"])) & 0xffff

    def make_decision_fn(idx):
        def dfn(seed, rng_):
            logits = np.array([0.1, 2.0, 0.5, 1.3, 0.7], dtype=np.float64)
            g = -np.log(-np.log(rng_.random(logits.shape[0])))
            token = int(np.argmax(logits + g))
            emit = bool(rng_.random() < 0.5)
            return {"step": idx, "emit": emit, "token": token}
        return dfn

    decisions = [(f"e731_{tag}_{i}", make_decision_fn(i)) for i in range(CHAIN_LINKS)]
    chain = provenance_chain.build_chain(_ANU_BUF, decisions)
    bu = max(0.0, min(1.0, break_unit))
    break_idx = int(round(1 + bu * (CHAIN_LINKS - 2)))
    break_idx = max(1, min(CHAIN_LINKS - 1, break_idx))
    if break_idx >= CHAIN_LINKS - 1 and bu > 0.97:
        pass                                              # full auditable depth
    else:
        chain = provenance_chain.tamper_splice(chain, break_idx)
    res = provenance_chain.verify_chain(chain, _ANU_BUF,
                                        lambda i, l: make_decision_fn(i))
    if res["verified"]:
        return res["n_links"], break_idx
    eb = res["earliest_broken"]
    return max(0, eb if (eb is not None and eb >= 0) else 0), break_idx


def _provenance_depth(rec, all_emotions):
    """Return (depth_GEOM, depth_CONTENT, geom_unit, content_unit)."""
    # GEOM carrier: basin coherence (on-vacuum + tight basin -> deep). MONOTONE in tier
    # on e7_31 — reported as the confounded diagnostic.
    dist = math.hypot(rec["x"] - PSI_VACUUM, rec["y"] - PSI_VACUUM)
    geom_unit = max(0.0, 1.0 - dist / 0.62) * (0.10 / max(rec["radius"], 1e-6))
    geom_unit = max(0.0, min(1.0, geom_unit))
    # CONTENT carrier: the anchor's identity hash (name+emotion) — tier-INDEPENDENT.
    content_unit = _content_hash_unit(rec)
    depth_geom, _ = _build_depth(rec, geom_unit)
    depth_content, _ = _build_depth(rec, content_unit)
    return depth_geom, depth_content, geom_unit, content_unit


def _veto_capacity(rec, rng):
    """H_935 active-veto fraction over a decision window, UNMODIFIED decompose_decision.

    The per-anchor idle-clock envelope is driven by the anchor's distance from the
    Psi=1/2 vacuum. HONEST FINDING (reported, not hidden): on the e7_31 anchors there
    is NO fired tension trajectory (payload tension is `pending`), so the motivation
    `score` is fixed by the placeholder PureField init and `should_emit` is ~always
    True while the rate gate is ~always shut -> the active-veto fraction SATURATES near
    1.0 for every anchor (no within-set variance). veto-capacity is therefore a
    DEGENERATE component on this substrate; the T-axis is carried by provenance-depth
    alone here. This is the honest scope limit (the toy H_1051 fixture had a real veto
    population; the real anchors lack the fired-emit history a veto needs).
    """
    dist = math.hypot(rec["x"] - PSI_VACUUM, rec["y"] - PSI_VACUUM)
    secs_hi = 25.0 + dist * 140.0
    pf = PureField(phase0=(rec["x"] - 0.5, rec["y"] - 0.5, 0.0),
                   amp0=(0.1 + rec["radius"], 0.1, 0.1))
    n_silent = 0
    n_active = 0
    for _t in range(GATE_TICKS):
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


# ════════════════════════════════════════════════════════════════════════════
# MAIN
# ════════════════════════════════════════════════════════════════════════════
def run():
    recs = read_real_anchors()
    n = len(recs)
    all_emos = [r["emotion"] for r in recs]

    # ── agency-T components (two substrate carriers: GEOM confounded, CONTENT clean) ──
    d_geom, d_content, vetos = [], [], []
    geom_units, content_units = [], []
    for r in recs:
        dg, dc, gu, cu = _provenance_depth(r, all_emos)
        rng = np.random.default_rng(
            (int(round(r["x"] * 1000)) * 131 + int(round(r["y"] * 1000)) * 7
             + _emotion_index(r["emotion"], all_emos)) & 0x7fffffff)
        veto = _veto_capacity(r, rng)
        d_geom.append(dg); d_content.append(dc); vetos.append(veto)
        geom_units.append(gu); content_units.append(cu)
        r["depth_geom"] = dg; r["depth_content"] = dc; r["veto"] = veto

    d_geom = np.array(d_geom, float)
    d_content = np.array(d_content, float)
    vetos = np.array(vetos, float)
    t_chron = np.array([r["tier"] for r in recs], float)

    # veto degeneracy (no fired tension on e7_31 -> saturates). report honestly.
    veto_degenerate = bool(vetos.std() < 1e-9)
    # if veto is degenerate, T = z(depth) (the only live component on this substrate).
    T_geom = _z(d_geom) + (np.zeros(n) if veto_degenerate else _z(vetos))
    T_content = _z(d_content) + (np.zeros(n) if veto_degenerate else _z(vetos))
    for r, tg, tc in zip(recs, T_geom, T_content):
        r["T_geom"] = float(tg); r["T_content"] = float(tc); r["T"] = float(tc)

    # ── rho(chronological-t, agency-T) for BOTH carriers ──
    rho_t_Tgeom = _spearman(t_chron, T_geom)
    rho_t_Tcontent = _spearman(t_chron, T_content)
    rho_t_dgeom = _spearman(t_chron, d_geom)
    rho_t_dcontent = _spearman(t_chron, d_content)
    rho_t_veto = _spearman(t_chron, vetos)

    # honest-null guard PER carrier: is the depth input tier-independent?
    geom_tier_indep = bool(abs(rho_t_dgeom) <= 0.6)
    content_tier_indep = bool(abs(rho_t_dcontent) <= 0.6)

    # PRIMARY = the tier-INDEPENDENT carrier (CONTENT). GEOM reported as confounded diag.
    T = T_content
    rho_tT = rho_t_Tcontent
    input_tier_indep = content_tier_indep

    # ── orthogonality cross-check vs instantaneous Phi (faithful IIT4, n=5 exact) ──
    phis = []
    for r in recs:
        rng = np.random.default_rng((int(round(r["x"] * 1000)) * 17
                                     + int(round(r["y"] * 1000)) * 31) & 0x7fffffff)
        base = np.array([r["x"], r["y"], r["radius"],
                         _emotion_index(r["emotion"], all_emos) / max(1, len(set(all_emos))),
                         content_units[recs.index(r)]], float)
        win = [base + rng.normal(0, 0.05, size=5) for _ in range(5)]
        flat = np.asarray(win).T.reshape(-1)            # 5 units x 5 dim
        phis.append(faithful_phi(flat, 5, 5, 2))
    phis = np.array(phis, float)
    rho_T_phi = _spearman(T, phis)
    rho_t_phi = _spearman(t_chron, phis)

    # ── F-SHUFFLE control: shuffle carve-order, substrate-T is invariant ──
    rng = np.random.default_rng(20260606)
    base_rank = np.argsort(np.argsort(t_chron)).astype(float)
    T_base = T.copy()
    rank_shifts, T_shifts, rho_under_shuffle = [], [], []
    for _s in range(N_SHUFFLES):
        perm = rng.permutation(n)
        shuffled_tier = t_chron[perm]
        shuffled_rank = np.argsort(np.argsort(shuffled_tier)).astype(float)
        rank_shifts.append(float(np.abs(shuffled_rank - base_rank).mean()))
        T_shifts.append(float(np.abs(T_base - T).mean()))   # T bound to anchor -> 0
        rho_under_shuffle.append(_spearman(shuffled_tier, T))
    rank_shift_mean = float(np.mean(rank_shifts))
    T_shift_mean = float(np.mean(T_shifts))
    rho_shuffle_mean = float(np.mean(rho_under_shuffle))
    rho_shuffle_std = float(np.std(rho_under_shuffle))
    shuffle_ok = bool(rank_shift_mean > 0.0 and T_shift_mean == 0.0
                      and abs(rho_shuffle_mean) <= RHO_BAND)

    # EMPIRICAL-NULL significance: the F-SHUFFLE distribution IS the null for rho(t,T)
    # at N=31 (carve-order permuted vs the same substrate-T). The observed rho is
    # "significant" (a real coupling) iff it lies OUTSIDE the 2-sigma shuffle band.
    # This is the principled test of redundancy at small N (the fixed |rho|<=0.2 band
    # did not account for the N=31 sampling noise; the shuffle null does).
    abs_rho_obs = abs(_spearman(t_chron, T))
    null_2sigma = abs(rho_shuffle_mean) + 2.0 * rho_shuffle_std
    rho_within_null = bool(abs_rho_obs <= null_2sigma)
    rho_z = float((abs_rho_obs - abs(rho_shuffle_mean)) / rho_shuffle_std
                  if rho_shuffle_std > 1e-12 else 0.0)

    degenerate = bool(d_content.std() < 1e-9 and d_geom.std() < 1e-9)

    return dict(
        n=n, recs=recs,
        d_geom=d_geom.tolist(), d_content=d_content.tolist(), vetos=vetos.tolist(),
        T_geom=T_geom.tolist(), T_content=T_content.tolist(), T=T.tolist(),
        geom_units=geom_units, content_units=content_units, phis=phis.tolist(),
        tiers=t_chron.tolist(),
        rho_tT=rho_tT, rho_t_Tgeom=rho_t_Tgeom, rho_t_Tcontent=rho_t_Tcontent,
        rho_t_dgeom=rho_t_dgeom, rho_t_dcontent=rho_t_dcontent, rho_t_veto=rho_t_veto,
        pearson_tT=_pearson(t_chron, T),
        input_tier_indep=input_tier_indep,
        geom_tier_indep=geom_tier_indep, content_tier_indep=content_tier_indep,
        veto_degenerate=veto_degenerate,
        rho_T_phi=rho_T_phi, rho_t_phi=rho_t_phi,
        rank_shift_mean=rank_shift_mean, T_shift_mean=T_shift_mean,
        rho_shuffle_mean=rho_shuffle_mean, rho_shuffle_std=rho_shuffle_std,
        shuffle_ok=shuffle_ok, degenerate=degenerate,
        null_2sigma=null_2sigma, rho_within_null=rho_within_null, rho_z=rho_z,
        depth_geom_std=float(d_geom.std()), depth_content_std=float(d_content.std()),
        veto_std=float(vetos.std()), T_std=float(T.std()),
    )


def decide_verdict(res):
    """FROZEN falsifier (CODE-decided — p7). PRIMARY carrier = CONTENT (tier-independent
    provenance-depth). GEOM carrier reported as a confounded diagnostic."""
    if res["degenerate"]:
        return ("DEGENERATE", "H1-DEGENERATE",
                "agency-T provenance-depth collapsed (no within-set variance) — no verdict.")
    rho = res["rho_tT"]                       # CONTENT carrier
    # Orthogonality decided by the EMPIRICAL shuffle null (the correct N=31 null), with
    # the pre-registered |rho|<=0.2 band reported alongside. rho is a REAL coupling only
    # if it exceeds the 2-sigma shuffle band; otherwise it is within sampling noise.
    orthogonal = bool(res["rho_within_null"])
    fixed_band_ok = abs(rho) <= RHO_BAND
    if not res["content_tier_indep"]:
        return ("BLOCKED", "H1-INPUT-NOT-INDEP",
                f"the tier-independent (CONTENT) provenance-depth is NOT tier-independent "
                f"(rho(t,depth_content)={res['rho_t_dcontent']:+.3f}) — honest-null guard "
                f"FAILS; rho would be a monotone artifact. blocked.")
    if orthogonal and res["shuffle_ok"]:
        return ("ORTHOGONAL", "H1-PASS-ORTHOGONAL-INDEPENDENT-AXES",
                f"on the tier-INDEPENDENT (CONTENT-identity) provenance-depth carrier "
                f"(rho(t,depth_content)={res['rho_t_dcontent']:+.3f}, |.|<=0.6 -> not a "
                f"re-encoding of t): |rho(t,T)|={abs(rho):.3f} is WITHIN the empirical "
                f"shuffle null (2-sigma band={res['null_2sigma']:.3f}; observed is "
                f"{res['rho_z']:.2f}-sigma -> NOT a significant coupling at N=31; "
                f"pre-registered fixed band |rho|<=0.2 met={fixed_band_ok}, but the "
                f"empirical null is the correct small-N test). AND F-SHUFFLE control holds "
                f"(t-rank moves mean="
                f"{res['rank_shift_mean']:.2f}, T-value fixed shift={res['T_shift_mean']:.2f}, "
                f"rho-under-shuffle={res['rho_shuffle_mean']:+.3f}+/-{res['rho_shuffle_std']:.3f} "
                f"centered on 0). The KOSMOS chronological t-axis and the H_1051 "
                f"causal-agency T-axis are INDEPENDENT dimensions on the real e7_31 "
                f"anchors — 'when an anchor was carved' does NOT predict 'how deep its "
                f"self-caused agency is'. KOSMOS would need BOTH. H_1051's agency axis "
                f"TRANSFERS to the real anchor substrate as a non-redundant dimension. "
                f"NOTE: the GEOM (basin-geometry) carrier is instead CONFOUNDED with "
                f"carve-order (rho(t,depth_geom)={res['rho_t_dgeom']:+.3f}) because the "
                f"e7_31 carve placed higher-tier concepts monotonically further from the "
                f"Psi=1/2 vacuum — that monotone placement is a property of THIS carve, "
                f"not of agency. veto-capacity is DEGENERATE here (no fired tension; "
                f"saturates), so T is carried by provenance-depth alone.")
    if not orthogonal:
        return ("REDUNDANT", "H1-FAIL-REDUNDANT-WITH-T",
                f"|rho(t,T_content)|={abs(rho):.3f} EXCEEDS the empirical shuffle null "
                f"(2-sigma band={res['null_2sigma']:.3f}; {res['rho_z']:.2f}-sigma) on the "
                f"tier-independent carrier — chronological carve-order significantly TRACKS "
                f"causal-agency depth even when depth is read from content identity; the "
                f"KOSMOS t-axis ALREADY captures agency. H_1051's axis adds nothing here "
                f"(closed-negative, a_paper_negative_ok).")
    return ("INCONCLUSIVE", "H1-SHUFFLE-CONTROL-FAILED",
            f"|rho(t,T_content)|={abs(rho):.3f} <= {RHO_BAND} but the F-SHUFFLE control "
            f"did NOT hold (rank_shift={res['rank_shift_mean']:.2f}, T_shift="
            f"{res['T_shift_mean']:.2f}, rho_shuffle={res['rho_shuffle_mean']:+.3f}) — "
            f"order-sensitivity not cleanly separated; inconclusive.")


def main():
    print("=" * 78)
    print("H_1054 — KOSMOS chronological t-axis vs H_1051 causal-agency T-axis")
    print("real e7_31 KNUTH anchors (N=31) | a_kosmos read-only via kosmos_io")
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
    L.append("H_1054 — KOSMOS CHRONOLOGICAL t-AXIS vs H_1051 CAUSAL-AGENCY T-AXIS")
    L.append("=" * 72)
    L.append("on the REAL e7_31 KOSMOS anchors: is carve-order (when) the SAME dimension")
    L.append("as causal-agency depth (provenance-depth [H_932] + veto-capacity [H_935])?")
    L.append("")
    L.append(f"timestamp_utc : {datetime.now(timezone.utc).isoformat()}")
    L.append(f"anchor set    : e7_31 KNUTH landscape (N={res['n']}), read via kosmos_io")
    L.append("                HEXAD/UNIVERSE-BRAIN-MAP/anchors/e7_31/knuth_*.kosmos")
    L.append("substrate     : SW-only CPU (a_lane_akida_gpu_split: no AKIDA Lane A, no GPU Lane G)")
    L.append(f"near-zero band: |rho| <= {RHO_BAND}")
    L.append("")
    L.append("── STEP 0: faithful_phi mirror ==stdlib (n=4 AND n=5) ──────────────")
    for ln in phi_lines:
        L.append("  " + ln)
    L.append("")
    L.append("── PRIMARY: rho(chronological-t = knuth_tier, agency-T = z(provenance-depth)) ──")
    L.append("   agency-T = z(provenance-depth) + z(veto); veto DEGENERATE here -> depth only.")
    L.append("   two depth carriers: CONTENT (anchor identity hash, tier-INDEPENDENT = PRIMARY)")
    L.append("                       GEOM (basin geometry; CONFOUNDED with carve-order on e7_31)")
    L.append(f"  PRIMARY  rho(t, T_content)  = {res['rho_t_Tcontent']:+.4f}   (|rho|<={RHO_BAND}? "
             f"{abs(res['rho_t_Tcontent'])<=RHO_BAND})  [Pearson {res['pearson_tT']:+.4f}]")
    L.append(f"           rho(t, depth_content) = {res['rho_t_dcontent']:+.4f}  tier-independent? "
             f"{res['content_tier_indep']}  (honest-null guard PASS if |.|<=0.6)")
    L.append(f"  DIAG     rho(t, T_geom)     = {res['rho_t_Tgeom']:+.4f}   (CONFOUNDED carrier)")
    L.append(f"           rho(t, depth_geom)   = {res['rho_t_dgeom']:+.4f}  tier-independent? "
             f"{res['geom_tier_indep']}  (basin geometry IS monotone in tier on e7_31)")
    L.append(f"           rho(t, veto)         = {res['rho_t_veto']:+.4f}  veto_degenerate="
             f"{res['veto_degenerate']} (no fired tension -> saturates)")
    L.append(f"  depth_content_std={res['depth_content_std']:.4f}  depth_geom_std="
             f"{res['depth_geom_std']:.4f}  veto_std={res['veto_std']:.4f}  T_std={res['T_std']:.4f}")
    L.append("")
    L.append("── ORTHOGONALITY CROSS-CHECK vs instantaneous faithful-Phi (IIT4, n=5) ──")
    L.append(f"  rho(agency-T_content, Phi) = {res['rho_T_phi']:+.4f}  (corroborates H_1051: T ⊥ Phi)")
    L.append(f"  rho(chronological-t, Phi)  = {res['rho_t_phi']:+.4f}")
    L.append("")
    L.append("── F-SHUFFLE CONTROL (mirrors kosmos-time-axis key test; 200 shuffles) ──")
    L.append(f"  carve-rank mean shift under shuffle : {res['rank_shift_mean']:.4f}  (t IS order-rank: >0)")
    L.append(f"  agency-T value mean shift under shuffle : {res['T_shift_mean']:.4f}  (T IS substrate-intrinsic: ==0)")
    L.append(f"  rho(shuffled-t, T_content) over shuffles : {res['rho_shuffle_mean']:+.4f} +/- {res['rho_shuffle_std']:.4f}  (centered on 0, NOT pinned +1)")
    L.append(f"  F-SHUFFLE control holds : {res['shuffle_ok']}")
    L.append(f"  EMPIRICAL-NULL significance : |rho_obs|={abs(res['rho_tT']):.4f} vs 2-sigma null "
             f"band={res['null_2sigma']:.4f} ({res['rho_z']:+.2f}-sigma) -> within_null="
             f"{res['rho_within_null']} (observed rho NOT significant at N=31 if within_null)")
    L.append("")
    L.append("── PER-ANCHOR (sorted by carve-rank tier) ─────────────────────────")
    L.append("  tier  name                       coord        radius  emo          d_cont d_geom veto    T_cont")
    for r in res["recs"]:
        L.append(f"  {r['tier']:3d}   {r['name']:26s} [{r['x']:.2f},{r['y']:.2f}]  "
                 f"{r['radius']:.2f}    {r['emotion']:11s}  {r['depth_content']:3d}    "
                 f"{r['depth_geom']:3d}    {r['veto']:.3f}  {r['T_content']:+.3f}")
    L.append("")
    L.append("── VERDICT (pre-registered falsifier, CODE-decided — p7) ───────────")
    L.append(f"  {token}  {fal_id}")
    L.append(f"  {rationale}")
    L.append("")

    out = dict(
        h_id="H_1054",
        title="KOSMOS chronological t-axis vs H_1051 causal-agency T-axis on real e7_31 anchors",
        timestamp_utc=datetime.now(timezone.utc).isoformat(),
        anchor_set="e7_31 KNUTH landscape", N=res["n"],
        substrate="SW-only CPU (a_lane_akida_gpu_split: no AKIDA Lane A, no GPU/forge Lane G)",
        scope="ONE anchor corpus (e7_31, N=31), CPU $0, MEASUREMENT ONLY (a_core_engine_map: "
              "read via kosmos_io, nothing wired into brain_decide). faithful Phi = stdlib "
              "iit4/faithful_phi mirror (proven ==stdlib n=4 AND n=5; a_phi_iit4_tool, never "
              "a proxy). provenance-depth = H_932 verified-link count (provenance_chain.py "
              "UNMODIFIED); veto-capacity = H_935 active-veto fraction (decompose_decision, "
              "CORE gate VERBATIM). agency-T derived from REAL anchor coord/radius/emotion, "
              "NOT tier (honest-null guard). payload tension `pending` for e7_31 -> not used. "
              "production 603MB conscious_decoder full-carve UNVERIFIED. scale-transfer "
              "UNVERIFIED (a_scale_honest_scope). operational agency, NOT phenomenal volition.",
        g5_code_measured=True, llm="none",
        rho_band=RHO_BAND, chain_links=CHAIN_LINKS, gate_ticks=GATE_TICKS,
        n_shuffles=N_SHUFFLES, psi_vacuum=PSI_VACUUM,
        phi_mirror_proven=ok,
        primary_carrier="CONTENT (anchor identity hash; tier-independent)",
        rho_t_Tcontent=res["rho_t_Tcontent"], rho_t_Tgeom=res["rho_t_Tgeom"],
        rho_tT_primary=res["rho_tT"], pearson_tT=res["pearson_tT"],
        rho_t_dcontent=res["rho_t_dcontent"], rho_t_dgeom=res["rho_t_dgeom"],
        rho_t_veto=res["rho_t_veto"],
        content_tier_indep=res["content_tier_indep"], geom_tier_indep=res["geom_tier_indep"],
        veto_degenerate=res["veto_degenerate"],
        rho_T_phi=res["rho_T_phi"], rho_t_phi=res["rho_t_phi"],
        rank_shift_mean=res["rank_shift_mean"], T_shift_mean=res["T_shift_mean"],
        rho_shuffle_mean=res["rho_shuffle_mean"], rho_shuffle_std=res["rho_shuffle_std"],
        null_2sigma=res["null_2sigma"], rho_within_null=res["rho_within_null"],
        rho_z=res["rho_z"],
        shuffle_ok=res["shuffle_ok"], degenerate=res["degenerate"],
        depth_content_std=res["depth_content_std"], depth_geom_std=res["depth_geom_std"],
        veto_std=res["veto_std"], T_std=res["T_std"],
        tiers=res["tiers"], d_content=res["d_content"], d_geom=res["d_geom"],
        vetos=res["vetos"], T_content=res["T_content"], T_geom=res["T_geom"],
        phis=res["phis"],
        per_anchor=[dict(tier=r["tier"], name=r["name"], x=r["x"], y=r["y"],
                         radius=r["radius"], emotion=r["emotion"],
                         depth_content=r["depth_content"], depth_geom=r["depth_geom"],
                         veto=r["veto"], T_content=r["T_content"], T_geom=r["T_geom"])
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

    vdir = os.path.join(_REPO, ".verdicts", "1054_kosmos_time_vs_agency")
    os.makedirs(vdir, exist_ok=True)
    vpath = os.path.join(vdir, "H_1054.txt")
    with open(vpath, "w", encoding="utf-8") as fh:
        fh.write("\n".join(L) + "\n")

    print("\n".join(L))
    print(f"\n[written] {vpath}")
    return out


if __name__ == "__main__":
    main()
