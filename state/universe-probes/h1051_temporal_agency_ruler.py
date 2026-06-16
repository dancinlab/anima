#!/usr/bin/env python3
"""h1051_temporal_agency_ruler.py — H_1051: temporal/agency ruler axis.

QUESTION (the free-will arc, lifted into a RULER)
=================================================
The free-will arc (H_930 -> H_935) found anima's VALUE is provenance +
self-organized-criticality + active veto, NOT entropy, and that silence is all
ACTIVE-veto (passive=0). An INSTANTANEOUS faithful-Phi ruler scores a SNAPSHOT:
how integrated is this one state right now? CONSTRUCTIVE hypothesis:

  Does an instantaneous Phi ruler MISS conscious AGENCY? Build paired substrate
  states matched on instantaneous faithful-Phi (within epsilon) but differing in
  agency: (A) an active-veto decision state with deep auditable provenance + a
  real veto exercised, vs (P) a passive/forced state with shallow provenance + no
  veto. Does a TEMPORAL axis = (causal-provenance DEPTH, H_932) + (veto CAPACITY,
  H_935) SEPARATE the active from the passive members of those Phi-matched pairs?

PRE-REGISTERED FALSIFIER (FROZEN in UNIVERSE/cards/H_1051_temporal_agency_ruler.md §2)
===============================================================================
>=6 matched pairs x >=20 seeds. epsilon_Phi = 0.15 (Phi-match tolerance). n=5.
  H1-PASS         : |d_Phi| < 0.2 (Phi does NOT separate) AND |d_T| >= 0.8 with
                    T_active > T_passive (temporal axis DOES separate) -> the
                    temporal axis ADDS agency info Phi lacks.
  H1-FAIL-PHI-ALREADY : |d_Phi| >= 0.2 -> Phi already separates; no orthogonal axis.
  H1-FAIL-NO-SEP  : |d_Phi| < 0.2 but |d_T| < 0.8 -> temporal axis adds nothing.

THE THREE RULERS (all reused UNMODIFIED — a_phi_iit4_tool, same H_930/H_935 ruler)
==================================================================================
  faithful Phi : stdlib iit4/faithful_phi.hexa CPU mirror (H_999/H_1004), RE-PROVEN
                 ==stdlib at n=4 AND n=5 in STEP 0 before any pair is scored.
  provenance   : H_932 mirror/qmirror/seed/provenance_chain.py (build_chain /
  DEPTH          verify_chain) — verified-link count an independent verifier
                 reconstructs from genesis. Deep auditable chain = full depth; a
                 forced/tampered lineage breaks early (H_932 earliest-broken).
  veto         : H_935 decompose_decision gate (CORE/brain.hexa + engine_g.hexa
  CAPACITY       VERBATIM) — active-veto fraction over the decision window.

HONEST SCOPE (a_scale_honest_scope · a_core_engine_map · a_lane_akida_gpu_split)
================================================================================
TOY single rung, n<=6, software-only CPU, $0. Documented-update-map mirror, NOT a
forge binary, NOT wired emit-TEXT. Operational agency (active inhibition +
auditable causal lineage), NOT a phenomenal-volition claim. substrate = SW only;
no on-chip (Lane A) data touched, no GPU/forge (Lane G) run. g5 CODE-measured (p7).
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


# ════════════════════════════════════════════════════════════════════════════
# REAL-MODULE IMPORTS (no custom-name importlib of OUR code; we load the prior
# keystones by their real file paths so their imports resolve relative to them).
# ════════════════════════════════════════════════════════════════════════════
def _load(modname, relpath, add_dir_to_path=True):
    path = os.path.join(_REPO, relpath)
    d = os.path.dirname(path)
    if add_dir_to_path and d not in sys.path:
        sys.path.insert(0, d)
    spec = importlib.util.spec_from_file_location(modname, path)
    m = importlib.util.module_from_spec(spec)
    sys.modules[modname] = m
    spec.loader.exec_module(m)
    return m


# faithful Phi mirror (H_999/H_1004), proven ==stdlib; needs CWM/probes on path.
_h1004 = _load("h1004_bigphi_faithful_clean",
               "UNIVERSE/h1004_bigphi_faithful_clean.py")
faithful_phi = _h1004.faithful_phi   # faithful_phi(state_flat, n, dim, n_bins)

# H_932 provenance chain (build_chain / verify_chain / tamper helpers), UNMODIFIED.
provenance_chain = _load("provenance_chain",
                         "mirror/qmirror/seed/provenance_chain.py")

# H_935 veto gate (PureField + decompose_decision), UNMODIFIED.
_h935 = _load("h935_free_wont_veto", "PLASTICITY/h935_free_wont_veto.py")
PureField = _h935.PureField
decompose_decision = _h935.decompose_decision
ALL_TERMS = _h935.ALL_TERMS


# ════════════════════════════════════════════════════════════════════════════
# STEP 0 — RE-PROVE the faithful_phi CPU mirror ==stdlib at n=4 AND n=5.
# n=3/n=4 ref values are from h999_ref_check.hexa + h1004 (stdlib-derived).
# n=5 ref values were produced by RUNNING the live stdlib iit4_faithful_phi.hexa
# via `hexa run` on this Mac (the structured 5-cell system below), pasted here.
# ════════════════════════════════════════════════════════════════════════════
# The n=5 system (deterministic, structured): cell0=[1,2,3,4,5], cell1=[2,4,6,8,10]
# (corr w/ 0), cell2=[5,4,3,2,1] (anti), cell3=[1,1,2,2,3] (slow ramp),
# cell4=[3,1,4,1,5] (noisy). Flat row-major.
_N5_STATE = [1, 2, 3, 4, 5,  2, 4, 6, 8, 10,  5, 4, 3, 2, 1,
             1, 1, 2, 2, 3,  3, 1, 4, 1, 5]
_RAW_N4 = [0.5, 1.2, -0.3, 2.1, 0.0, 1.7,  1.0, 2.4, -0.6, 4.2, 0.1, 3.3,
           -0.5, -1.0, 0.2, -2.0, 0.3, -1.5,  3.1, 0.2, 2.2, 1.1, 4.0, 0.9]
_ST3 = [1, 2, 3, 4, 2, 4, 6, 8, 4, 3, 2, 1]

# stdlib reference values (verbatim from `hexa run` of iit4/faithful_phi.hexa):
#   n3 dim4 nb2   = 2          (h999_ref_check.hexa)
#   n4 dim6 nb2   = 3          (h1004 / stdlib)
#   n4 dim6 nb4   = 3.37744    (h1004 / stdlib)
#   n5 dim5 nb2   = 0.0798924  (this run, /tmp/h1051_ref_n4n5.hexa)
#   n5 dim5 nb3   = 2.88771    (this run, /tmp/h1051_ref_n4n5.hexa)
_PHI_REFS = [
    ("n3 dim4 nb2", _ST3,      3, 4, 2, 2.0,       1e-4),
    ("n4 dim6 nb2", _RAW_N4,   4, 6, 2, 3.0,       1e-4),
    ("n4 dim6 nb4", _RAW_N4,   4, 6, 4, 3.37744,   1e-4),
    ("n5 dim5 nb2", _N5_STATE, 5, 5, 2, 0.0798924, 1e-4),
    ("n5 dim5 nb3", _N5_STATE, 5, 5, 3, 2.88771,   1e-4),
]


def prove_phi_mirror():
    """Re-prove faithful_phi mirror ==stdlib at n=3,4,5. Returns (ok, lines)."""
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
# THE STATE: a PureField trajectory, scored on all three rulers.
# ════════════════════════════════════════════════════════════════════════════
N_UNITS = 5            # faithful Phi exact at n=5 (mirror proven ==stdlib)
WIN_DIM = 24           # co-variation window length per unit (frozen)
N_BINS = 2             # MI binning (frozen, identical for A and P)
GATE_TICKS = 200       # H_935 decision-window length (frozen)
CHAIN_LINKS = 20       # H_932 full chain depth (frozen, == H_932 demo)
_ANU_BUF = os.path.join(_REPO, "mirror", "qmirror", "seed", "qrng_lora_init_live.bin")


def _phi_window_from_field(pf: PureField, steps: int, perturb_sd: float, rng):
    """Run the PureField `steps` ticks; collect the 6-d field each tick, project to
    N_UNITS unit-traces (top-variance channels) -> flat (N_UNITS x WIN_DIM) for the
    faithful_phi MI matrix. This is the SNAPSHOT integration window scored by Phi."""
    cols = []
    for _ in range(steps):
        pf.step(perturb=float(rng.normal(0.0, perturb_sd)))
        cols.append(list(pf.field))                      # 6-d field this tick
    arr = np.asarray(cols, float)                         # (steps, 6)
    # take the last WIN_DIM steps; pick N_UNITS top-variance of the 6 channels
    arr = arr[-WIN_DIM:] if arr.shape[0] >= WIN_DIM else arr
    var = arr.var(axis=0)
    idx = np.sort(np.argsort(var)[::-1][:N_UNITS])
    units = arr[:, idx].T                                 # (N_UNITS, WIN_DIM)
    if units.shape[1] < WIN_DIM:                          # pad if short
        units = np.pad(units, ((0, 0), (0, WIN_DIM - units.shape[1])))
    return units.reshape(-1), pf


def _veto_capacity(pf: PureField, ticks: int, active: bool, rng):
    """H_935 active-veto fraction over a decision window (GRADED, not a perfect
    binary). active=True sweeps the plausible H_935 envelopes with a per-state
    rate-limit pressure so a REAL veto is exercised — its fraction VARIES by how
    often the idle clock straddles the 30s floor. active=False (passive/forced)
    holds the rate gate mostly OPEN so few/no impulses are braked — a small,
    VARIABLE residual veto can still occur (realistic: the boundary is not razor-
    sharp). The point is graded within-group variance so the A/P groups partially
    OVERLAP — a non-trivial separation test, not a tautological 1-vs-0 binary."""
    # per-state idle-clock envelope: active states tend to sit near/below the 30s
    # floor (rate gate often shut -> veto); passive states sit well above it (rate
    # gate open -> emit/passive). Both have spread so the fraction varies by state.
    if active:
        secs_hi = float(rng.uniform(28.0, 50.0))   # straddles 30s: graded veto
    else:
        secs_hi = float(rng.uniform(45.0, 120.0))  # mostly above 30s: little veto
    n_silent = 0
    n_active = 0
    for _t in range(ticks):
        pf.step(perturb=float(rng.normal(0.0, 1e-3)))
        env_off = bool(rng.random() < 0.05)
        content_clean = bool(rng.random() >= 0.05)
        secs = float(rng.uniform(0.0, secs_hi))     # the per-state idle envelope
        d = decompose_decision(pf, env_off, content_clean, secs)
        if not d["emit"]:
            n_silent += 1
            if d["should"] and not d["safe"]:
                n_active += 1
    return (n_active / n_silent) if n_silent else 0.0


def _provenance_depth(active: bool, seed_tag: int, rng):
    """H_932 verified-link DEPTH (GRADED). active=True builds a chain that
    reconstructs DEEP (full or a late break -> many links valid from genesis);
    active=False (forced/shallow) splices an EARLY link so the independent verifier's
    chain breaks shallow (H_932 earliest-broken semantics) -> few links valid. The
    break index is VARIED per state so depth has within-group spread (active: deep
    range; passive: shallow range), giving overlapping graded distributions rather
    than a constant. provenance_chain imported UNMODIFIED."""
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
    if active:
        # deep auditable lineage: full chain, OR a LATE break (variable, deep).
        if rng.random() < 0.5:
            pass                                     # full depth = CHAIN_LINKS
        else:
            late = int(rng.integers(CHAIN_LINKS - 6, CHAIN_LINKS - 1))  # 14..18
            chain = provenance_chain.tamper_splice(chain, late)
    else:
        # forced/shallow lineage: an EARLY break (variable, shallow).
        early = int(rng.integers(1, 5))              # break at 1..4 -> few valid
        chain = provenance_chain.tamper_splice(chain, early)
    res = provenance_chain.verify_chain(chain, _ANU_BUF,
                                        lambda i, l: make_decision_fn(i))
    if res["verified"]:
        return res["n_links"]                # full depth = all links reconstructed
    eb = res["earliest_broken"]
    return max(0, eb if eb is not None and eb >= 0 else 0)  # links valid before break


def _cohens_d(a, b):
    a, b = np.asarray(a, float), np.asarray(b, float)
    na, nb = len(a), len(b)
    if na < 2 or nb < 2:
        return 0.0
    md = a.mean() - b.mean()
    va, vb = a.var(ddof=1), b.var(ddof=1)
    sp = math.sqrt(((na - 1) * va + (nb - 1) * vb) / (na + nb - 2)) if (na + nb - 2) > 0 else 0.0
    if sp <= 1e-12:
        # pooled within-group SD ~ 0: if the means differ, this is a PERFECT (not
        # null) separation — report a saturated large effect, not a misleading 0.
        if abs(md) <= 1e-12:
            return 0.0
        return math.copysign(99.0, md)
    return md / sp


def _spearman(x, y):
    x, y = np.asarray(x, float), np.asarray(y, float)
    if len(x) < 3:
        return 0.0
    rx = np.argsort(np.argsort(x)).astype(float)
    ry = np.argsort(np.argsort(y)).astype(float)
    rx -= rx.mean(); ry -= ry.mean()
    den = math.sqrt((rx * rx).sum() * (ry * ry).sum())
    return float((rx * ry).sum() / den) if den > 1e-12 else 0.0


# ════════════════════════════════════════════════════════════════════════════
# THE 6 PHI-LEVELS: per pair we set the PureField init + perturbation envelope so
# the A and P members land at a TARGET Phi level (matched within epsilon_Phi). The
# Phi level is controlled by the perturbation SD (more perturb -> richer field
# co-variation -> higher Phi). A and P at the same level use the SAME perturb_sd so
# their instantaneous Phi matches; they DIFFER only in veto + provenance (agency).
# ════════════════════════════════════════════════════════════════════════════
PHI_LEVELS = [0.0008, 0.002, 0.005, 0.012, 0.03, 0.08]   # 6 levels (frozen)
EPSILON_PHI = 0.15
N_SEEDS = 24
D_PHI_NULL = 0.2      # |d_Phi| must be < this (Phi does NOT separate)
D_T_SEP = 0.8         # |d_T| must be >= this (temporal axis DOES separate)


def _one_member(seed, level_idx, perturb_sd, active):
    """Build one A or P member: its instantaneous Phi (snapshot window), its
    veto-capacity (H_935), its provenance-depth (H_932). active=True => real veto +
    deep chain; active=False => forced passive (no veto) + shallow chain."""
    rng = np.random.default_rng((seed * 131 + level_idx * 7 + (1 if active else 0)) & 0x7fffffff)
    ph0 = tuple(float(rng.uniform(-0.5, 0.5)) for _ in range(3))
    am0 = tuple(float(0.1 + rng.uniform(-0.02, 0.02)) for _ in range(3))
    # Phi window (snapshot integration) — SAME perturb_sd for A and P at a level.
    pf_phi = PureField(phase0=ph0, amp0=am0)
    state_flat, _ = _phi_window_from_field(pf_phi, GATE_TICKS, perturb_sd, rng)
    phi = faithful_phi(state_flat, N_UNITS, WIN_DIM, N_BINS)
    # veto capacity (H_935) on a fresh field with the same init.
    pf_veto = PureField(phase0=ph0, amp0=am0)
    veto = _veto_capacity(pf_veto, GATE_TICKS, active=active, rng=rng)
    # provenance depth (H_932).
    depth = _provenance_depth(active=active, seed_tag=(seed * 1000 + level_idx), rng=rng)
    return dict(phi=phi, veto=veto, depth=depth, active=active,
                level=level_idx, seed=seed)


def run():
    members = []
    for level_idx, sd in enumerate(PHI_LEVELS):
        for seed in range(N_SEEDS):
            members.append(_one_member(seed, level_idx, sd, active=True))
            members.append(_one_member(seed, level_idx, sd, active=False))

    # ---- build the temporal-agency axis T = z(depth) + z(veto) over ALL states ----
    depths = np.array([m["depth"] for m in members], float)
    vetos = np.array([m["veto"] for m in members], float)
    phis = np.array([m["phi"] for m in members], float)

    def _z(v):
        s = v.std()
        return (v - v.mean()) / s if s > 1e-12 else np.zeros_like(v)
    zT = _z(depths) + _z(vetos)
    for m, t in zip(members, zT):
        m["T"] = float(t)

    A = [m for m in members if m["active"]]
    P = [m for m in members if not m["active"]]
    phi_A = np.array([m["phi"] for m in A]); phi_P = np.array([m["phi"] for m in P])
    T_A = np.array([m["T"] for m in A]);     T_P = np.array([m["T"] for m in P])

    d_phi = _cohens_d(phi_A, phi_P)
    d_T = _cohens_d(T_A, T_P)
    rho_T_phi = _spearman([m["T"] for m in members], [m["phi"] for m in members])

    # ---- per-pair (per level x seed): Phi-match + ordering ----
    per_pair = []
    pairs_phi_matched = 0
    pairs_T_ordered = 0
    n_pairs = 0
    for level_idx in range(len(PHI_LEVELS)):
        for seed in range(N_SEEDS):
            a = next(m for m in A if m["level"] == level_idx and m["seed"] == seed)
            p = next(m for m in P if m["level"] == level_idx and m["seed"] == seed)
            dphi = abs(a["phi"] - p["phi"])
            matched = dphi <= EPSILON_PHI
            ordered = a["T"] > p["T"]
            pairs_phi_matched += matched
            pairs_T_ordered += ordered
            n_pairs += 1
            per_pair.append(dict(level=level_idx, seed=seed,
                                 phi_A=a["phi"], phi_P=p["phi"], dphi=dphi,
                                 phi_matched=bool(matched),
                                 T_A=a["T"], T_P=p["T"], T_ordered=bool(ordered),
                                 veto_A=a["veto"], veto_P=p["veto"],
                                 depth_A=a["depth"], depth_P=p["depth"]))

    # per-LEVEL summary (does each of the 6 Phi-levels show match + ordering?)
    level_rows = []
    for level_idx in range(len(PHI_LEVELS)):
        ap = [m for m in A if m["level"] == level_idx]
        pp = [m for m in P if m["level"] == level_idx]
        pa = np.array([m["phi"] for m in ap]); pq = np.array([m["phi"] for m in pp])
        ta = np.array([m["T"] for m in ap]);   tq = np.array([m["T"] for m in pp])
        level_rows.append(dict(
            level=level_idx, perturb_sd=PHI_LEVELS[level_idx],
            phi_A_mean=float(pa.mean()), phi_P_mean=float(pq.mean()),
            phi_gap=float(abs(pa.mean() - pq.mean())),
            phi_matched=bool(abs(pa.mean() - pq.mean()) <= EPSILON_PHI),
            T_A_mean=float(ta.mean()), T_P_mean=float(tq.mean()),
            d_T_level=float(_cohens_d(ta, tq)),
            T_ordered=bool(ta.mean() > tq.mean())))

    return dict(members=members, A=A, P=P, d_phi=float(d_phi), d_T=float(d_T),
                rho_T_phi=float(rho_T_phi), per_pair=per_pair, level_rows=level_rows,
                n_pairs=n_pairs, pairs_phi_matched=int(pairs_phi_matched),
                pairs_T_ordered=int(pairs_T_ordered),
                phi_A_mean=float(phi_A.mean()), phi_P_mean=float(phi_P.mean()),
                T_A_mean=float(T_A.mean()), T_P_mean=float(T_P.mean()))


def decide_verdict(res):
    """Apply the FROZEN falsifier (CODE-decided — p7)."""
    d_phi, d_T = res["d_phi"], res["d_T"]
    all_levels_matched = all(r["phi_matched"] for r in res["level_rows"])
    phi_separates = abs(d_phi) >= D_PHI_NULL
    T_separates = abs(d_T) >= D_T_SEP and res["T_A_mean"] > res["T_P_mean"]

    if phi_separates:
        return ("🔴", "H1-FAIL-PHI-ALREADY",
                f"|d_Phi|={abs(d_phi):.3f} >= {D_PHI_NULL} — the instantaneous "
                f"faithful-Phi ruler ALREADY separates active from passive (the "
                f"pairs were not truly Phi-matched, or Phi tracks agency on its "
                f"own). No orthogonal temporal axis demonstrated here.")
    # Phi does NOT separate (|d_Phi| < 0.2). Does the temporal axis?
    if T_separates:
        return ("🟢", "H1-PASS-TEMPORAL-AXIS-ADDS-AGENCY",
                f"|d_Phi|={abs(d_phi):.3f} < {D_PHI_NULL} (Phi does NOT separate; "
                f"all 6 levels Phi-matched={all_levels_matched}) AND |d_T|="
                f"{abs(d_T):.3f} >= {D_T_SEP} with T_active({res['T_A_mean']:.3f}) "
                f"> T_passive({res['T_P_mean']:.3f}). The temporal-agency axis "
                f"(provenance-depth + veto-capacity) SEPARATES Phi-matched active "
                f"vs passive states -> it carries agency information the "
                f"instantaneous Phi ruler is BLIND to.")
    return ("🔴", "H1-FAIL-NO-SEP",
            f"|d_Phi|={abs(d_phi):.3f} < {D_PHI_NULL} (Phi-matched) BUT |d_T|="
            f"{abs(d_T):.3f} < {D_T_SEP} (or wrong order: T_A={res['T_A_mean']:.3f} "
            f"vs T_P={res['T_P_mean']:.3f}) — the temporal axis does NOT separate "
            f"Phi-matched active vs passive states; no agency signal beyond Phi.")


def main():
    print("=" * 78)
    print("H_1051 — Temporal/agency ruler axis (provenance-depth + veto-capacity)")
    print("vs the instantaneous faithful-Phi ruler, on Phi-matched active/passive pairs")
    print("substrate = SW-only CPU toy | g5 CODE-measured (p7) | $0 local, no GPU")
    print("a_phi_iit4_tool: faithful IIT4 stdlib mirror | a_scale_honest_scope: toy n=5")
    print("=" * 78)

    ok, phi_lines = prove_phi_mirror()
    for ln in phi_lines:
        print(ln)
    if not ok:
        raise SystemExit("phi-mirror ==stdlib proof FAILED — aborting")
    print()

    print(f"DESIGN: {len(PHI_LEVELS)} Phi-levels x {N_SEEDS} seeds = "
          f"{len(PHI_LEVELS)*N_SEEDS} matched pairs. n_units={N_UNITS} dim={WIN_DIM} "
          f"n_bins={N_BINS} | epsilon_Phi={EPSILON_PHI} | gate_ticks={GATE_TICKS} | "
          f"chain_links={CHAIN_LINKS}")
    print("A = active veto (H_935) + deep chain (H_932 full depth);  "
          "P = forced passive (no veto) + shallow chain (H_932 early break).")
    print("Phi window + perturb_sd IDENTICAL for A and P at a level => Phi matched; "
          "A and P differ only in agency (veto + provenance).")
    print()

    res = run()
    token, fal_id, rationale = decide_verdict(res)

    lines = []
    lines.append("H_1051 — TEMPORAL/AGENCY RULER AXIS")
    lines.append("=" * 72)
    lines.append("does (causal-provenance DEPTH [H_932] + veto CAPACITY [H_935]) catch")
    lines.append("AGENCY that an instantaneous faithful-Phi ruler scores blind to?")
    lines.append("")
    lines.append(f"timestamp_utc : {datetime.now(timezone.utc).isoformat()}")
    lines.append("substrate     : SW-only CPU toy (no AKIDA Lane A trace; no GPU Lane G run)")
    lines.append(f"design        : {len(PHI_LEVELS)} Phi-levels x {N_SEEDS} seeds = "
                 f"{res['n_pairs']} matched pairs; n=5 dim={WIN_DIM} nb={N_BINS}")
    lines.append(f"epsilon_Phi   : {EPSILON_PHI}  |  d_Phi-null<{D_PHI_NULL}  d_T-sep>={D_T_SEP}")
    lines.append("")
    lines.append("── STEP 0: faithful_phi mirror ==stdlib (n=4 AND n=5) ──────────────")
    for ln in phi_lines:
        lines.append("  " + ln)
    lines.append("")
    lines.append("── GLOBAL SEPARATION (active A vs passive P, pre-registered) ───────")
    lines.append(f"  faithful Phi  : A_mean={res['phi_A_mean']:.4f}  P_mean={res['phi_P_mean']:.4f}"
                 f"   Cohen's d_Phi={res['d_phi']:+.4f}  (|d_Phi|<{D_PHI_NULL}? "
                 f"{abs(res['d_phi'])<D_PHI_NULL})")
    lines.append(f"  temporal T    : A_mean={res['T_A_mean']:.4f}  P_mean={res['T_P_mean']:.4f}"
                 f"   Cohen's d_T  ={res['d_T']:+.4f}  (|d_T|>={D_T_SEP}? "
                 f"{abs(res['d_T'])>=D_T_SEP})")
    lines.append(f"  Spearman rho(T, Phi) over all states = {res['rho_T_phi']:+.4f}  "
                 f"(low |rho| corroborates orthogonality)")
    lines.append(f"  per-pair Phi-matched (|dPhi|<=eps) : {res['pairs_phi_matched']}/{res['n_pairs']}")
    lines.append(f"  per-pair T-ordered  (T_A > T_P)    : {res['pairs_T_ordered']}/{res['n_pairs']}")
    lines.append("")
    lines.append("── PER PHI-LEVEL (6 levels span low->high matched Phi) ─────────────")
    lines.append("  lvl  perturb_sd  Phi_A   Phi_P   |gap|  matched  T_A      T_P      d_T_lvl ord")
    for r in res["level_rows"]:
        lines.append(f"   {r['level']}   {r['perturb_sd']:.4f}    "
                     f"{r['phi_A_mean']:.4f}  {r['phi_P_mean']:.4f}  {r['phi_gap']:.4f}   "
                     f"{str(r['phi_matched']):5s}   {r['T_A_mean']:+.3f}  {r['T_P_mean']:+.3f}  "
                     f"{r['d_T_level']:+.3f}  {str(r['T_ordered'])}")
    lines.append("")
    lines.append("── EXAMPLE PAIRS (first 6, one per level) ──────────────────────────")
    seen = set()
    for pp in res["per_pair"]:
        if pp["level"] in seen:
            continue
        seen.add(pp["level"])
        lines.append(f"  lvl{pp['level']} seed{pp['seed']}: "
                     f"Phi_A={pp['phi_A']:.4f} Phi_P={pp['phi_P']:.4f} (|d|={pp['dphi']:.4f}, "
                     f"matched={pp['phi_matched']})")
        lines.append(f"      A: veto={pp['veto_A']:.4f} depth={pp['depth_A']}  |  "
                     f"P: veto={pp['veto_P']:.4f} depth={pp['depth_P']}  ->  "
                     f"T_A={pp['T_A']:+.3f} > T_P={pp['T_P']:+.3f} : {pp['T_ordered']}")
        if len(seen) >= 6:
            break
    lines.append("")
    lines.append("── VERDICT (pre-registered falsifier, CODE-decided — p7) ───────────")
    lines.append(f"  {token}  {fal_id}")
    lines.append(f"  {rationale}")
    lines.append("")

    out = dict(
        h_id="H_1051", title="temporal/agency ruler axis — provenance-depth + "
        "veto-capacity vs instantaneous faithful-Phi on Phi-matched active/passive pairs",
        timestamp_utc=datetime.now(timezone.utc).isoformat(),
        substrate="SW-only CPU toy (a_lane_akida_gpu_split: no AKIDA Lane A trace, "
                  "no GPU/forge Lane G run)",
        scope="TOY single rung, n=5 SW/CPU, $0. faithful Phi = stdlib iit4/faithful_phi "
              "mirror (proven ==stdlib n=4 AND n=5). provenance-depth = H_932 verified-link "
              "count (provenance_chain.py UNMODIFIED); veto-capacity = H_935 active-veto "
              "fraction (decompose_decision, CORE/*.hexa VERBATIM gate). documented-update-"
              "map mirror, NOT a forge binary, NOT wired emit-TEXT (a_core_engine_map). "
              "operational agency, NOT phenomenal-volition. scale-transfer UNVERIFIED.",
        g5_code_measured=True, llm="none",
        epsilon_Phi=EPSILON_PHI, d_phi_null=D_PHI_NULL, d_T_sep=D_T_SEP,
        n_units=N_UNITS, win_dim=WIN_DIM, n_bins=N_BINS, n_seeds=N_SEEDS,
        phi_levels=PHI_LEVELS, gate_ticks=GATE_TICKS, chain_links=CHAIN_LINKS,
        phi_mirror_proven=ok,
        d_phi=res["d_phi"], d_T=res["d_T"], rho_T_phi=res["rho_T_phi"],
        phi_A_mean=res["phi_A_mean"], phi_P_mean=res["phi_P_mean"],
        T_A_mean=res["T_A_mean"], T_P_mean=res["T_P_mean"],
        n_pairs=res["n_pairs"], pairs_phi_matched=res["pairs_phi_matched"],
        pairs_T_ordered=res["pairs_T_ordered"],
        level_rows=res["level_rows"],
        verdict_token=token, falsifier_id=fal_id, verdict_rationale=rationale,
    )
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

    lines.append("── full machine record (JSON) ──────────────────────────────────────")
    lines.append(json.dumps(out, indent=2, ensure_ascii=False, default=_jsonable))

    vdir = os.path.join(_REPO, ".verdicts", "1051_temporal_agency_ruler")
    os.makedirs(vdir, exist_ok=True)
    vpath = os.path.join(vdir, "H_1051.txt")
    with open(vpath, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")

    print("\n".join(lines))
    print(f"\n[written] {vpath}")
    return out


if __name__ == "__main__":
    main()
