#!/usr/bin/env python3
# ============================================================================
#  H_1411 — brain-lane composition LAW: DESCRIPTIVE → PREDICTIVE.
#
#  Across 6 measured pairs (H_1404 affect×ethics, H_1405 memory×ToM,
#  H_1406 WM×PFC, H_1407 cerebellum×basal, H_1408 spatial×episodic,
#  H_1409 spatial×PFC) a LAW emerged DESCRIPTIVELY (post-hoc fit):
#
#    Composing two brain-lane faculties RAISES faithful-IIT4 Φ (Φ-LIFT) IFF the
#    composed system's min-cut MI (= Φ_composed) exceeds max(component internal
#    Φ). Equivalently: a pair Φ-composes IFF NO single part's internal
#    integration Φ exceeds the composed min-cut MI. If one component's internal
#    Φ DOMINATES (> the composed min-cut MI) → Φ-composition is BLOCKED (🧱).
#
#  This script PROMOTES the law from descriptive → PREDICTIVE: it PRE-REGISTERS
#  a verdict (LIFT vs BLOCK) for each UNTESTED pair PURELY from each component's
#  already-measured internal Φ + a frozen decision rule (see FREEZE.txt), THEN
#  measures the composed faithful-IIT4 Φ for each pair and scores HIT/MISS.
#
#  ──────────────────────────────────────────────────────────────────────────
#  REUSE, NOT REINVENT (a_phi_iit4_tool · frozen-first). This script REUSES the
#  EXACT mirror substrate machinery from the 6 landed probes VERBATIM:
#    - the same byte-trigram FNV-1a embedding (dim64),
#    - each faculty's OWN per-step feature generator (episode_features) +
#      store setup, imported as a library module from its landed probe file,
#    - the IDENTICAL H_1401 substrate-weighted leaky-arbiter coupling
#      (g = leaky integrator of the two votes; coupling = f + 0.35*g*(f-0.5)
#      applied to BOTH blocks — byte-identical to every landed probe),
#    - the SAME 4 systems (S_partA n=4, S_partB n=4, S_composed n=8,
#      S_disconnected n=8), DIM=64, STEPS=96, 3 seeds, n_bins=16 primary.
#  The Python side computes NO Φ. Φ is measured by the REAL stdlib faithful
#  IIT4 engine (exact MIP-EI, n<=8) in h1411_phi_runner.hexa.
#
#  Component internal Φ for each faculty is a FIXED property of that faculty's
#  SOLO block trajectory (independent of its partner — the solo arrays in every
#  landed probe do not depend on the other block). So component Φ is REUSED
#  verbatim from the landed results, and is also RE-EMITTED here per pair (the
#  solo block is re-generated and re-measured by the runner) so each pair is
#  fully self-contained and checkable.
#
#  $0 CPU, gradient-free, deterministic, 3 seeds. p7/c9/a_phi_iit4_tool.
# ============================================================================
import numpy as np, sys, os, importlib.util

DIM = 64
STEPS = 96
SEEDS = [5411, 5412, 5413]    # H_1411 seeds (disjoint from all landed pairs)

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))


# ── byte-trigram FNV-1a embedding (verbatim from every landed probe) ────────
def fnv_embed(s, dim=DIM):
    v = np.zeros(dim)
    bs = s.encode("utf-8")
    for i in range(len(bs) - 2):
        tri = bs[i:i+3]
        h = 2166136261
        for b in tri:
            h ^= b; h = (h * 16777619) & 0xFFFFFFFF
        v[h % dim] += 1.0
    n = np.linalg.norm(v)
    return v / n if n > 0 else v


def _load(modname, relpath):
    spec = importlib.util.spec_from_file_location(modname, os.path.join(REPO, relpath))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


# import the landed probes as libraries (each is __main__-guarded → safe to import)
M1404 = _load("h1404", "state/1404_lane_compose_phi/h1404_lane_compose_phi.py")
M1405 = _load("h1405", "state/brain-lane-compose-memory-tom/h1405_compose_phi.py")
M1407 = _load("h1407", "state/brain-lane-compose-cerebellum-basal/h1407_compose_phi.py")
M1408 = _load("h1408", "state/brain-lane-compose-spatial-episodic/h1408_compose_phi.py")
M1409 = _load("h1409", "state/brain-lane-compose-spatial-pfc/h1409_compose_phi.py")


# ── per-faculty per-tick feature SAMPLERS ───────────────────────────────────
# Each returns a callable sampler(rng) -> dict of that faculty's 4 unit values,
# plus the unit-name list. The sampler steps the faculty's OWN substrate forward
# one tick using its OWN update rule (imported verbatim). NO faculty's update
# depends on the partner — exactly as the solo blocks in every landed probe.
# This makes the SOLO block trajectory (hence its internal Φ) byte-equivalent to
# the landed measurement modulo seed; the seeds here are H_1411's own.

# Faculty REGISTRY: name -> (probe module, solo-key, unit-list attr, run_trajectories)
# Each landed probe's run_trajectories(seed) returns its 4 systems; the SOLO block
# arrays are the per-faculty trajectories we reuse. We re-pair them by driving each
# faculty's solo stream on a SHARED tick index and coupling via the verbatim arbiter.
FACULTY = {
    # name        (module, solo_key,      units_attr)
    "affect":     (M1404, "affect",       "AFFECT_UNITS"),
    "ethics":     (M1404, "ethics",       "ETHICS_UNITS"),
    "memory":     (M1405, "memory",       "MEMORY_UNITS"),
    "tom":        (M1405, "tom",          "TOM_UNITS"),
    "cerebellum": (M1407, "cerebellum",   "CEREBELLUM_UNITS"),
    "basal":      (M1407, "basal",        "BASAL_UNITS"),
    "spatial_ep": (M1408, "spatial",      "SPATIAL_UNITS"),
    "episodic":   (M1408, "episodic",     "EPISODIC_UNITS"),
    "spatial_pfc":(M1409, "spatial",      "SPATIAL_UNITS"),
    "pfc":        (M1409, "pfc",          "PFC_UNITS"),
}


def solo_block(name, seed):
    """Return (n x STEPS) SOLO trajectory for a faculty, reusing its landed probe
    run_trajectories verbatim. This IS the trajectory whose internal Φ the law
    keys on. Independent of any partner (the landed solo arrays do not couple)."""
    mod, key, _ = FACULTY[name]
    tr = mod.run_trajectories(seed)
    return np.asarray(tr[key])


def compose_pair(nameA, nameB, seed):
    """Build the COMPOSED (n=8) and DISCONNECTED (n=8) systems for an arbitrary
    pair by coupling the two faculties' SOLO per-tick streams through the
    VERBATIM H_1401 leaky arbiter (g, 0.35*g*(f-0.5)) — byte-identical coupling
    to every landed probe. DISCONNECTED = the two solo blocks stacked (no
    coupling), the EARNED control."""
    A = solo_block(nameA, seed)   # 4 x STEPS
    B = solo_block(nameB, seed)   # 4 x STEPS
    nA, T = A.shape
    nB = B.shape[0]
    T = min(T, B.shape[1])
    A = A[:, :T]; B = B[:, :T]

    # the two faculties' VOTE+CONFIDENCE per tick: vote = sign of the block's
    # leading discriminative unit (unit 0 of each block, the faculty's primary
    # margin/decision read in every landed probe); conf = |that unit - midpoint|.
    # This is the H_1401 substrate-weighted, scale-relative arbiter, NO hardcoded
    # priority (a_autonomy_over_hardcode), applied identically to any pair.
    a_lead = A[0]; b_lead = B[0]
    a_mid = float(np.median(a_lead)); b_mid = float(np.median(b_lead))
    arb_state = 0.0
    cmpA = np.zeros_like(A); cmpB = np.zeros_like(B)
    for t in range(T):
        a_vote = 1.0 if a_lead[t] > a_mid else -1.0
        a_conf = abs(a_lead[t] - a_mid)
        b_vote = 1.0 if b_lead[t] > b_mid else -1.0
        b_conf = abs(b_lead[t] - b_mid)
        denom = a_conf + b_conf + 1e-9
        arb = (a_conf * a_vote + b_conf * b_vote) / denom
        arb_state = 0.6 * arb_state + 0.4 * arb     # leaky integrator (verbatim)
        g = 0.5 * (arb_state + 1.0)                  # gate in [0,1] (verbatim)
        # COUPLING: shared arbiter signal modulates BOTH blocks (verbatim 0.35*g*(f-0.5)).
        cmpA[:, t] = A[:, t] + 0.35 * g * (A[:, t] - 0.5)
        cmpB[:, t] = B[:, t] + 0.35 * g * (B[:, t] - 0.5)

    composed = np.vstack([cmpA, cmpB])              # n=8
    disconnected = np.vstack([A, B])                # n=8 (EARNED control, no coupling)
    return A, B, composed, disconnected


# ── the UNTESTED pairs (pre-registered in FREEZE.txt) ───────────────────────
# Chosen to span the law's prediction space with KNOWN component Φ (n_bins=16,
# from the landed results): a value in parentheses is the recorded solo Φ.
#   cerebellum 3.476 (HIGH) · tom 1.975 (HIGH) · pfc 0.792 (LOW-MID) ·
#   episodic 0.507 (LOW) · affect 0.285 (LOW) · memory 0.176 (LOW) ·
#   basal 0.000 (LOW) · ethics 0.000 (LOW) · spatial 0.000/3.233 (construction-dep)
PAIRS = [
    ("cerebellum", "tom"),       # HIGH×HIGH  (3.476 × 1.975) — two-high, fresh case
    ("affect",     "basal"),     # LOW×LOW    (0.285 × 0.000) — predict LIFT
    ("tom",        "basal"),     # HIGH×LOW   (1.975 × 0.000) — dominant-high test
    ("cerebellum", "episodic"),  # HIGH×LOW   (3.476 × 0.507) — dominant-high test
    ("memory",     "ethics"),    # LOW×LOW    (0.176 × 0.000) — predict LIFT
]


def write_states(path):
    lines = []
    for (nameA, nameB) in PAIRS:
        tag = f"{nameA}__{nameB}"
        for seed in SEEDS:
            A, B, composed, disconnected = compose_pair(nameA, nameB, seed)
            for sysname, M in [(f"partA::{tag}", A), (f"partB::{tag}", B),
                               (f"composed::{tag}", composed),
                               (f"disconnected::{tag}", disconnected)]:
                n, T = M.shape
                lines.append(f"# {sysname}_s{seed} {n} {T}")
                for r in range(n):
                    lines.append(" ".join(f"{v:.6f}" for v in M[r]))
    with open(path, "w") as fh:
        fh.write("\n".join(lines) + "\n")
    print(f"wrote {path}: {len(PAIRS)} pairs x {len(SEEDS)} seeds x 4 systems")
    # degeneracy guard (c9): per-unit std for each solo block (flag constant units)
    print("--- per-unit std (degeneracy guard; near-0 std = constant unit) ---")
    for (nameA, nameB) in PAIRS:
        A = solo_block(nameA, SEEDS[0]); B = solo_block(nameB, SEEDS[0])
        sA = [float(np.std(A[r])) for r in range(A.shape[0])]
        sB = [float(np.std(B[r])) for r in range(B.shape[0])]
        print(f"  {nameA}: " + ",".join(f"{s:.4f}" for s in sA)
              + f"   |   {nameB}: " + ",".join(f"{s:.4f}" for s in sB))


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "/tmp/h1411_states.txt"
    write_states(out)
