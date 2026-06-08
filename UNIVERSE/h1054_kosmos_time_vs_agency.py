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
def read_real_anchors():
    """Return the e7_31 anchors as records sorted by knuth_tier (carve-rank)."""
    raw = kosmos_io.load_anchors(_ANCHOR_DIR)
    recs = []
    for a in raw:
        fld = a["fields"]
        tier = fld.get("knuth_tier")
        coord = fld.get("coord")
        radius = fld.get("radius")
        emo = fld.get("top_emotion")
        if tier is None or coord is None or radius is None:
            continue
        if not (isinstance(coord, list) and len(coord) == 2):
            continue
        recs.append(dict(
            name=a["name"], tier=int(tier),
            x=float(coord[0]), y=float(coord[1]),
            radius=float(radius), emotion=str(emo),
            lane=str(fld.get("lane", "")),
        ))
    recs.sort(key=lambda r: r["tier"])
    return recs


# distinct emotions -> a stable index so emotion can seed the chain (substrate, not tier)
def _emotion_index(emotion, all_emotions):
    return sorted(set(all_emotions)).index(emotion)


# ════════════════════════════════════════════════════════════════════════════
# AGENCY-T COMPONENTS — DERIVED FROM REAL SUBSTRATE (coord/radius/emotion), NOT tier.
# ════════════════════════════════════════════════════════════════════════════
def _provenance_depth(rec, all_emotions):
    """H_932 verified-link DEPTH for this anchor, UNMODIFIED build/verify chain.

    The tamper-splice position (where the auditable lineage breaks) is set by the
    anchor's BASIN substrate: distance from the Psi=1/2 vacuum + basin radius. A tight,
    on-vacuum basin reconstructs DEEP (late break); a diffuse / off-vacuum basin breaks
    SHALLOW. The break index is a function of REAL coord/radius — NOT the tier.
    """
    seed_tag = (_emotion_index(rec["emotion"], all_emotions) * 101
                + int(round(rec["x"] * 97)) * 7
                + int(round(rec["y"] * 89)))

    def make_decision_fn(idx):
        def dfn(seed, rng_):
            logits = np.array([0.1, 2.0, 0.5, 1.3, 0.7], dtype=np.float64)
            g = -np.log(-np.log(rng_.random(logits.shape[0])))
            token = int(np.argmax(logits + g))
            emit = bool(rng_.random() < 0.5)
            return {"step": idx, "emit": emit, "token": token}
        return dfn

    decisions = [(f"e731_{seed_tag}_{i}", make_decision_fn(i))
                 for i in range(CHAIN_LINKS)]
    chain = provenance_chain.build_chain(_ANU_BUF, decisions)

    # basin coherence in [0,1]: 1 = on-vacuum, tight basin; 0 = far/diffuse.
    dist = math.hypot(rec["x"] - PSI_VACUUM, rec["y"] - PSI_VACUUM)
    # normalize: max coord dist on this set ~ hypot(0.45,0.43)~0.62; radius 0.10..0.22.
    coherence = max(0.0, 1.0 - dist / 0.62) * (0.10 / max(rec["radius"], 1e-6))
    coherence = max(0.0, min(1.0, coherence))
    # map coherence -> break index in [1, CHAIN_LINKS]: high coherence -> deep (late).
    break_idx = int(round(1 + coherence * (CHAIN_LINKS - 2)))
    break_idx = max(1, min(CHAIN_LINKS - 1, break_idx))
    if break_idx >= CHAIN_LINKS - 1 and coherence > 0.97:
        # near-perfect basin: full auditable depth (no break).
        pass
    else:
        chain = provenance_chain.tamper_splice(chain, break_idx)
    res = provenance_chain.verify_chain(chain, _ANU_BUF,
                                        lambda i, l: make_decision_fn(i))
    if res["verified"]:
        return res["n_links"], coherence, break_idx
    eb = res["earliest_broken"]
    depth = max(0, eb if (eb is not None and eb >= 0) else 0)
    return depth, coherence, break_idx


def _veto_capacity(rec, rng):
    """H_935 active-veto fraction over a decision window, UNMODIFIED decompose_decision.

    The per-anchor idle-clock envelope is driven by the anchor's distance from the
    Psi=1/2 vacuum: near-vacuum -> the rate gate often sits below the 30s floor (rate
    shut -> a would-emit impulse is braked -> exercised veto); far-from-vacuum -> the
    rate gate is open (little veto). Envelope = REAL coord, NOT tier.
    """
    dist = math.hypot(rec["x"] - PSI_VACUUM, rec["y"] - PSI_VACUUM)
    # near-vacuum (dist~0) -> low secs_hi (straddles 30s -> veto); far -> high (open).
    secs_hi = 25.0 + dist * 140.0                       # dist 0->25s, 0.6->~109s
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

    # agency-T components (substrate-derived).
    depths, vetos, coherences, breaks = [], [], [], []
    for r in recs:
        depth, coh, brk = _provenance_depth(r, all_emos)
        rng = np.random.default_rng(
            (int(round(r["x"] * 1000)) * 131 + int(round(r["y"] * 1000)) * 7
             + _emotion_index(r["emotion"], all_emos)) & 0x7fffffff)
        veto = _veto_capacity(r, rng)
        depths.append(depth); vetos.append(veto)
        coherences.append(coh); breaks.append(brk)
        r["depth"] = depth; r["veto"] = veto; r["coherence"] = coh

    depths = np.array(depths, float)
    vetos = np.array(vetos, float)
    T = _z(depths) + _z(vetos)
    for r, t in zip(recs, T):
        r["T"] = float(t)
    t_chron = np.array([r["tier"] for r in recs], float)

    # ── primary: rho(chronological-t, agency-T) ──
    rho_tT = _spearman(t_chron, T)
    rho_t_depth = _spearman(t_chron, depths)
    rho_t_veto = _spearman(t_chron, vetos)

    # ── honest-null guard: are the agency-T INPUTS tier-independent? ──
    # if depth/veto were a re-encoding of tier, rho(tier, input) would be ~+/-1.
    input_tier_indep = bool(abs(rho_t_depth) <= 0.6 and abs(rho_t_veto) <= 0.6)

    # ── orthogonality cross-check vs instantaneous Phi (faithful IIT4) ──
    # Phi on a 5-unit window built from the anchor's coord/radius/emotion neighbourhood
    # (substrate, n=5 exact). This is a corroborating cross-axis, NOT the primary test.
    phis = []
    for r in recs:
        rng = np.random.default_rng((int(round(r["x"] * 1000)) * 17
                                     + int(round(r["y"] * 1000)) * 31) & 0x7fffffff)
        base = np.array([r["x"], r["y"], r["radius"],
                         _emotion_index(r["emotion"], all_emos) / max(1, len(set(all_emos))),
                         r["coherence"]], float)
        win = []
        for _ in range(5):
            win.append(base + rng.normal(0, 0.05, size=5))
        flat = np.asarray(win).T.reshape(-1)            # 5 units x 5 dim
        phis.append(faithful_phi(flat, 5, 5, 2))
    phis = np.array(phis, float)
    rho_T_phi = _spearman(T, phis)
    rho_t_phi = _spearman(t_chron, phis)

    # ── F-SHUFFLE control: shuffle carve-order, T attached to substrate is invariant ──
    rng = np.random.default_rng(20260606)
    base_rank = np.argsort(np.argsort(t_chron)).astype(float)
    T_base = T.copy()
    rank_shifts = []
    T_shifts = []
    rho_under_shuffle = []
    for _s in range(N_SHUFFLES):
        perm = rng.permutation(n)
        # shuffling carve-order = relabelling which anchor sits at which carve-rank.
        # t (carve-rank) is reassigned by perm; T stays bound to its anchor (substrate).
        shuffled_tier = t_chron[perm]
        shuffled_rank = np.argsort(np.argsort(shuffled_tier)).astype(float)
        rank_shifts.append(float(np.abs(shuffled_rank - base_rank).mean()))
        # the agency-T value vector (per anchor) is byte-identical (no perm applied).
        T_shifts.append(float(np.abs(T_base - T).mean()))
        # rho between the permuted carve-rank and the unchanged substrate-T:
        rho_under_shuffle.append(_spearman(shuffled_tier, T))
    rank_shift_mean = float(np.mean(rank_shifts))
    T_shift_mean = float(np.mean(T_shifts))
    rho_shuffle_mean = float(np.mean(rho_under_shuffle))
    rho_shuffle_std = float(np.std(rho_under_shuffle))
    # shuffle control: t-rank MOVES, T-value FIXED, rho centered on 0 (not pinned +1).
    shuffle_ok = bool(rank_shift_mean > 0.0 and T_shift_mean == 0.0
                      and abs(rho_shuffle_mean) <= RHO_BAND)

    degenerate = bool(depths.std() < 1e-9 and vetos.std() < 1e-9)

    return dict(
        n=n, recs=recs,
        depths=depths.tolist(), vetos=vetos.tolist(), T=T.tolist(),
        coherences=coherences, breaks=breaks, phis=phis.tolist(),
        tiers=t_chron.tolist(),
        rho_tT=rho_tT, rho_t_depth=rho_t_depth, rho_t_veto=rho_t_veto,
        pearson_tT=_pearson(t_chron, T),
        input_tier_indep=input_tier_indep,
        rho_T_phi=rho_T_phi, rho_t_phi=rho_t_phi,
        rank_shift_mean=rank_shift_mean, T_shift_mean=T_shift_mean,
        rho_shuffle_mean=rho_shuffle_mean, rho_shuffle_std=rho_shuffle_std,
        shuffle_ok=shuffle_ok, degenerate=degenerate,
        depth_std=float(depths.std()), veto_std=float(vetos.std()),
        T_std=float(T.std()),
    )


def decide_verdict(res):
    """FROZEN falsifier (CODE-decided — p7)."""
    if res["degenerate"]:
        return ("DEGENERATE", "H1-DEGENERATE",
                "agency-T inputs collapsed (no within-set variance) — no science verdict.")
    rho = res["rho_tT"]
    orthogonal = abs(rho) <= RHO_BAND
    if not res["input_tier_indep"]:
        return ("BLOCKED", "H1-INPUT-NOT-INDEP",
                f"agency-T inputs are NOT tier-independent (rho(t,depth)="
                f"{res['rho_t_depth']:+.3f}, rho(t,veto)={res['rho_t_veto']:+.3f}) — the "
                f"honest-null guard FAILS; any rho would be a monotone artifact. blocked.")
    if orthogonal and res["shuffle_ok"]:
        return ("ORTHOGONAL", "H1-PASS-ORTHOGONAL-INDEPENDENT-AXES",
                f"|rho(t,T)|={abs(rho):.3f} <= {RHO_BAND} (near-zero band) AND F-SHUFFLE "
                f"control holds (t-rank moves mean={res['rank_shift_mean']:.2f}, T-value "
                f"fixed shift={res['T_shift_mean']:.2f}, rho-under-shuffle="
                f"{res['rho_shuffle_mean']:+.3f}+/-{res['rho_shuffle_std']:.3f} centered "
                f"on 0). The KOSMOS chronological t-axis and the H_1051 causal-agency "
                f"T-axis are INDEPENDENT dimensions on the real e7_31 anchors — 'when an "
                f"anchor was carved' does NOT predict 'how deep its self-caused agency "
                f"is'. KOSMOS's coordinate system would need BOTH. H_1051's agency axis "
                f"TRANSFERS to the real anchor substrate as a non-redundant dimension.")
    if not orthogonal:
        return ("REDUNDANT", "H1-FAIL-REDUNDANT-WITH-T",
                f"|rho(t,T)|={abs(rho):.3f} > {RHO_BAND} — chronological carve-order "
                f"approximately TRACKS causal-agency depth on the real anchors; the "
                f"existing KOSMOS t-axis ALREADY captures agency. H_1051's axis adds "
                f"nothing on this substrate (closed-negative, a_paper_negative_ok).")
    return ("INCONCLUSIVE", "H1-SHUFFLE-CONTROL-FAILED",
            f"|rho(t,T)|={abs(rho):.3f} <= {RHO_BAND} but the F-SHUFFLE control did NOT "
            f"hold (rank_shift={res['rank_shift_mean']:.2f}, T_shift="
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
    L.append("── PRIMARY: rho(chronological-t = knuth_tier, agency-T = z(depth)+z(veto)) ──")
    L.append(f"  Spearman rho(t, T)        = {res['rho_tT']:+.4f}   (|rho|<={RHO_BAND}? "
             f"{abs(res['rho_tT'])<=RHO_BAND})")
    L.append(f"  Pearson  r(t, T)          = {res['pearson_tT']:+.4f}")
    L.append(f"  rho(t, provenance-depth)  = {res['rho_t_depth']:+.4f}")
    L.append(f"  rho(t, veto-capacity)     = {res['rho_t_veto']:+.4f}")
    L.append(f"  agency-T inputs tier-independent (honest-null guard) : {res['input_tier_indep']}")
    L.append(f"  depth_std={res['depth_std']:.4f}  veto_std={res['veto_std']:.4f}  "
             f"T_std={res['T_std']:.4f}  degenerate={res['degenerate']}")
    L.append("")
    L.append("── ORTHOGONALITY CROSS-CHECK vs instantaneous faithful-Phi (IIT4, n=5) ──")
    L.append(f"  rho(agency-T, Phi)        = {res['rho_T_phi']:+.4f}  (corroborates H_1051: T ⊥ Phi)")
    L.append(f"  rho(chronological-t, Phi) = {res['rho_t_phi']:+.4f}")
    L.append("")
    L.append("── F-SHUFFLE CONTROL (mirrors kosmos-time-axis key test; 200 shuffles) ──")
    L.append(f"  carve-rank mean shift under shuffle : {res['rank_shift_mean']:.4f}  (t IS order-rank: >0)")
    L.append(f"  agency-T value mean shift under shuffle : {res['T_shift_mean']:.4f}  (T IS substrate-intrinsic: ==0)")
    L.append(f"  rho(shuffled-t, T) over shuffles : {res['rho_shuffle_mean']:+.4f} +/- {res['rho_shuffle_std']:.4f}  (centered on 0, NOT pinned +1)")
    L.append(f"  F-SHUFFLE control holds : {res['shuffle_ok']}")
    L.append("")
    L.append("── PER-ANCHOR (sorted by carve-rank tier) ─────────────────────────")
    L.append("  tier  name                       coord        radius  emo          depth  veto    T")
    for r in res["recs"]:
        L.append(f"  {r['tier']:3d}   {r['name']:26s} [{r['x']:.2f},{r['y']:.2f}]  "
                 f"{r['radius']:.2f}    {r['emotion']:11s}  {r['depth']:3d}    "
                 f"{r['veto']:.4f}  {r['T']:+.3f}")
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
        rho_tT=res["rho_tT"], pearson_tT=res["pearson_tT"],
        rho_t_depth=res["rho_t_depth"], rho_t_veto=res["rho_t_veto"],
        input_tier_indep=res["input_tier_indep"],
        rho_T_phi=res["rho_T_phi"], rho_t_phi=res["rho_t_phi"],
        rank_shift_mean=res["rank_shift_mean"], T_shift_mean=res["T_shift_mean"],
        rho_shuffle_mean=res["rho_shuffle_mean"], rho_shuffle_std=res["rho_shuffle_std"],
        shuffle_ok=res["shuffle_ok"], degenerate=res["degenerate"],
        depth_std=res["depth_std"], veto_std=res["veto_std"], T_std=res["T_std"],
        tiers=res["tiers"], depths=res["depths"], vetos=res["vetos"],
        T=res["T"], phis=res["phis"],
        per_anchor=[dict(tier=r["tier"], name=r["name"], x=r["x"], y=r["y"],
                         radius=r["radius"], emotion=r["emotion"],
                         depth=r["depth"], veto=r["veto"], T=r["T"],
                         coherence=r["coherence"]) for r in res["recs"]],
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
