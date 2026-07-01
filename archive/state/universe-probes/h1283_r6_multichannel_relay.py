#!/usr/bin/env python3
# H_1283 R6 — THALAMUS / MULTI-CHANNEL PARALLEL RELAY
# slug: 1283_thalamus_global_workspace  (R6 — append-only; does NOT overwrite R1..R5)
# lens: missing-brain-structure ladder (neuro, c15) — NOT an LLM recipe (a_no_llm_frame_trap)
#
# THE WALL (c16 / a_break_the_wall): H_1283 is 🧱 closed-negative across R1..R5.
# Root cause the wall exposed (verbatim from the card): "a single broadcast channel
# is itself a low-dim cut that caps faithful-IIT4 Φ." R5 terminal: dense all-pairs
# coupling did NOT robustly clear AND the SHUFFLE control fired (the all-pairs
# intra-thalamic cross-coupling let ANY permutation inject equivalent recurrence
# variance → lift was variance, not structure).
#
# R6 ANGLE (attacks the root cause directly): instead of ONE shared relay stage
# (broadcast R1 / coalition R2 / sparse-reentrant R3-R4 / dense all-pairs R5 — ALL
# route through a single relay stage with channel cross-mixing), install N
# INDEPENDENT PARALLEL RELAY CHANNELS — one private relay path per RING EDGE
# (module pair). Each channel is its OWN reciprocal leaky loop coupling exactly its
# two endpoint modules, with NO intra-thalamic cross-coupling between channels.
#   Biological lens (a_no_llm_frame_trap, c15): the thalamus is MANY parallel
#   nuclei / topographic relays, NOT one bus. Distributed parallel relays mean
#   there is NO single low-dim cut to cap Φ, and — critically — because the
#   channels are DISJOINT (no cross-mixing), permuting the channel→pair assignment
#   (the SHUFFLE control) genuinely DESTROYS the parallel-relay structure rather
#   than re-injecting the same shared variance (the exact artifact that fired in R5,
#   where any all-pairs permutation kept the same mean-over-all-others recurrence).
#
# ARM A (direct ring)        — byte-identical to R1..R5 (same draws/order). MUST
#                              reproduce ARM_A Φ = 0.78038 / 0.611741 / 0.825326.
# ARM B (multichannel)       — ring KEPT + N_EDGE independent parallel relay
#                              channels, each coupling ONE ring edge's two modules
#                              reciprocally; channels DISJOINT (no cross-mixing).
# SHUFFLE control (mc_shuffle)— same N_EDGE channels, but the channel→edge
#                              assignment is PERMUTED by a fixed derangement (same
#                              edge count, scrambled which pair each channel serves).
#
# Φ = FAITHFUL IIT4 ONLY (a_phi_iit4_tool): exact MIP-EI via the stdlib engine
# hexa-lang/stdlib/consciousness/iit4/faithful_phi.hexa (n=4). numpy NEVER computes
# Φ — it only emits the per-module salience trajectory; the engine computes Φ.
# numpy = DIRECTIONAL mirror only (a_engine_native_learning). $0 CPU, seeds [7,8,9].
#
# FROZEN BARS (see H_1283_R6_FREEZE.txt — frozen BEFORE scoring; bars IDENTICAL to
# the prior rounds, NOT moved = no tune-to-green, c9/p7): GREEN iff
#   c1 COHERENCE   B.coh ≥ A.coh on EVERY seed
#   c2 PRIMARY  Φ  faithful ΔΦ ≥ +0.02 on EVERY seed [7,8,9]   (the +0.02 bar)
#   c3 NO-COLLAPSE B.coh < 0.999 on ≥1 seed (relays integrate, not collapse-clone)
#   c4 SHUFFLE     mc_shuffle ΔΦ < +0.02 on ≥1 seed that ARM B GREENs (the lift
#                  must COLLAPSE under permuted channel→pair wiring → structure, not
#                  variance). If shuffle reproduces the lift → honest 🧱 (as R5).
# GREEN = c1 AND c2 AND c3 AND c4. Else RED / 🧱 (closed-negative, c9; bar NOT moved).

import os, sys, json, subprocess, tempfile
import numpy as np

SEEDS   = [7, 8, 9]
N_MOD   = 4          # {A, G, mitosis, memory}
DIM     = 8          # per-module state vector dim
T       = 64         # ticks
GAIN    = 0.30       # per-module update gain (identical both arms)
LEAK    = 0.55       # state self-retention (identical both arms)
NBINS   = 8          # IIT4 MI estimator bins
W_NBR   = 0.5        # ring coupling weight (identical both arms)
W_IN    = 0.5        # private-input weight (identical both arms)
W_RELAY = 0.5        # parallel-relay coupling weight — FROZEN at 0.5, the SAME
                     # value carried since R3 (p7: NOT swept after seeing results).

MARGIN_COH = 0.05    # (reported; c1 uses ≥ A, the prior-round sanity form)
MARGIN_PHI = 0.02    # the +0.02 Φ bar R1 missed by 0.0009 — UNCHANGED
DEGEN_CAP  = 0.999

HEXA = "/Users/mini/.hx/bin/hexa"
HEXA_ROOT = "/Users/mini/dancinlab/hexa-lang"
FAITHFUL = HEXA_ROOT + "/stdlib/consciousness/iit4/faithful_phi.hexa"

# fixed ring adjacency (SAME as R1..R5): A↔G, G↔mitosis, mitosis↔memory, memory↔A
RING = [[1, 3], [0, 2], [1, 3], [2, 0]]
# ring EDGES (undirected, each appears once) — these define the N parallel channels.
# edge e connects modules EDGES[e] = (lo, hi). Four edges for the 4-cycle ring.
EDGES = [(0, 1), (1, 2), (2, 3), (3, 0)]   # A-G, G-mitosis, mitosis-memory, memory-A
N_EDGE = len(EDGES)


def mean_pairwise_cosine(states):
    sims = []
    for i in range(N_MOD):
        for j in range(i + 1, N_MOD):
            a, b = states[i], states[j]
            na, nb = np.linalg.norm(a), np.linalg.norm(b)
            sims.append(0.0 if (na < 1e-9 or nb < 1e-9)
                        else float(np.dot(a, b) / (na * nb)))
    return float(np.mean(sims))


def run_arm(seed, mode):
    """mode in {'direct', 'multichannel', 'mc_shuffle'}. Returns (coherence, traj).

    'direct'       — ARM A: fixed ring, each module reads only direct neighbours
                     (byte-identical to R1..R5: same rng draw order).
    'multichannel' — ARM B: ring KEPT + N_EDGE INDEPENDENT PARALLEL relay channels.
                     Channel e has its OWN leaky state rc[e] (dim DIM) and couples
                     ONLY the two modules of EDGES[e], reciprocally:
                       cortex→thalamus: rc[e] integrates the MEAN of its two
                         endpoint modules' PRE-update states (one-tick reciprocal
                         delay), with NO cross-coupling to any other channel;
                       thalamus→cortex: rc[e] re-injects into BOTH its endpoint
                         modules.
                     Channels are DISJOINT — no intra-thalamic mixing — so there is
                     NO single shared relay stage to act as a low-dim MIP cut, and
                     no all-pairs cross term for a permutation to re-inject (R5's
                     shuffle artifact source is structurally absent).
    'mc_shuffle'   — SHUFFLE control: same N_EDGE channels and same per-channel
                     mechanism, but the channel→edge assignment is PERMUTED by a
                     fixed derangement: channel e now serves EDGES[perm[e]] instead
                     of EDGES[e]. Same edge count, scrambled which pair each parallel
                     channel binds. If the lift is the structured parallel-relay
                     topology, this must DESTROY it.
    """
    rng = np.random.default_rng(seed)
    # ----- DRAWS 1..3 byte-identical to R1..R5 (so ARM A is unchanged) -----
    states = rng.standard_normal((N_MOD, DIM)) * 0.5          # draw 1
    inputs = rng.standard_normal((N_MOD, T, DIM)) * 0.8       # draw 2
    # draw 3 in R3/R5 was relay (N_MOD, DIM). Here we instead draw the parallel
    # channel states (N_EDGE, DIM). ARM A never touches the relay draw, so its path
    # depends only on draws 1 and 2 → byte-identical to R1..R5. The channel states
    # are drawn from the SAME stream AFTER inputs (used only in ARM B / shuffle).
    rc = rng.standard_normal((N_EDGE, DIM)) * 0.5             # draw 3 (parallel chans)

    # SHUFFLE derangement: fixed cyclic shift of channel→edge assignment (no fixed
    # point — no channel serves its own structured edge). Specified in the FREEZE.
    perm = (np.roll(np.arange(N_EDGE), 1)).tolist()  # [N-1,0,1,...] cyclic shift

    def edge_of(e):
        if mode == "mc_shuffle":
            return EDGES[perm[e]]
        return EDGES[e]

    # precompute, per module i, the list of channels that re-inject into it.
    chans_into = [[] for _ in range(N_MOD)]
    for e in range(N_EDGE):
        lo, hi = edge_of(e)
        chans_into[lo].append(e)
        chans_into[hi].append(e)

    coh_acc = []
    traj = np.zeros((N_MOD, T))
    for t in range(T):
        new = states.copy()
        if mode == "direct":
            for i in range(N_MOD):
                nbr = np.mean([states[k] for k in RING[i]], axis=0)
                new[i] = LEAK * states[i] + GAIN * (W_NBR * nbr + W_IN * inputs[i, t])
        else:  # 'multichannel' or 'mc_shuffle'
            # thalamus→cortex: each module receives the MEAN of the channels that
            # re-inject into it (a module on 2 ring edges hears 2 private channels).
            for i in range(N_MOD):
                nbr = np.mean([states[k] for k in RING[i]], axis=0)
                ch_list = chans_into[i]
                relay_in = (np.mean([rc[e] for e in ch_list], axis=0)
                            if ch_list else np.zeros(DIM))
                new[i] = (LEAK * states[i]
                          + GAIN * (W_NBR * nbr
                                    + W_IN * inputs[i, t]
                                    + W_RELAY * relay_in))
            # cortex→thalamus: each channel integrates ONLY its two endpoint modules'
            # PRE-update states (one-tick reciprocal delay). NO cross-channel term —
            # the parallel channels are independent (the whole point vs R3/R5).
            new_rc = rc.copy()
            for e in range(N_EDGE):
                lo, hi = edge_of(e)
                pair_mean = 0.5 * (states[lo] + states[hi])
                new_rc[e] = LEAK * rc[e] + GAIN * (W_NBR * pair_mean)
            rc = new_rc
        states = new
        for i in range(N_MOD):
            traj[i, t] = float(np.dot(states[i], states[i]))
        if t >= T // 2:
            coh_acc.append(mean_pairwise_cosine(states))
    return float(np.mean(coh_acc)), traj


def faithful_phi(traj, tag):
    """Faithful IIT4 Φ over the n=4 module trajectories via the stdlib EXACT engine
    (hexa run). numpy NEVER computes Φ — it only emits the trajectory here."""
    n, dim = traj.shape
    flat = traj.flatten()
    lines = ['import "stdlib/consciousness/iit4/faithful_phi.hexa"', "", "fn main() {",
             f"    let state = farr_zeros({n * dim})"]
    for idx, val in enumerate(flat):
        lines.append(f"    let _ = farr_set(state, {idx}, {val:.10f})")
    lines.append(f"    let phi = iit4_faithful_phi(state, {n}, {dim}, {NBINS})")
    lines.append('    println("PHI=" + phi.to_string())')
    lines.append("    let _ = farr_free(state)")
    lines.append("}")
    src = "\n".join(lines)
    with tempfile.NamedTemporaryFile("w", suffix=".hexa", delete=False,
                                     dir=HEXA_ROOT) as f:
        path = f.name
        f.write(src)
    try:
        out = subprocess.run([HEXA, "run", os.path.basename(path)],
                             cwd=HEXA_ROOT, capture_output=True, text=True, timeout=300)
        blob = out.stdout + "\n" + out.stderr
        for ln in blob.splitlines():
            if ln.strip().startswith("PHI="):
                return float(ln.strip().split("=", 1)[1])
        print(f"[phi {tag}] no PHI line:\n{blob[:1500]}", file=sys.stderr)
        return None
    finally:
        try:
            os.remove(path)
        except OSError:
            pass


def main():
    print("H_1283 R6 — THALAMUS / MULTI-CHANNEL PARALLEL RELAY")
    print(f"modules={N_MOD} dim={DIM} ticks={T} seeds={SEEDS}  "
          f"channels={N_EDGE} (one per ring edge)  W_relay={W_RELAY}")
    print("ARM A = direct ring   ·   ARM B = ring + N independent parallel relay channels "
          "(disjoint, no intra-thalamic cross-coupling)")
    print("PRIMARY bar = faithful IIT4 ΔΦ ≥ +0.02 EVERY seed   ·   SHUFFLE control pre-registered")
    print("=" * 72)

    per_seed = {}
    for seed in SEEDS:
        cohA, trajA = run_arm(seed, "direct")
        cohB, trajB = run_arm(seed, "multichannel")
        cohSh, trajSh = run_arm(seed, "mc_shuffle")
        per_seed[seed] = {"cohA": cohA, "cohB": cohB, "cohSh": cohSh,
                          "trajA": trajA, "trajB": trajB, "trajSh": trajSh}

    print("FAITHFUL IIT4 Φ (exact MIP-EI, ALL seeds) — ARM A vs MULTICHANNEL ARM B:")
    phi_all = {}
    for seed in SEEDS:
        phiA = faithful_phi(per_seed[seed]["trajA"], f"A_s{seed}")
        phiB = faithful_phi(per_seed[seed]["trajB"], f"B_s{seed}")
        dphi = (phiB - phiA) if (phiA is not None and phiB is not None) else None
        phi_all[seed] = {"A": phiA, "B": phiB, "delta": dphi}
        print(f"  seed {seed}: ARM_A Φ={phiA}  MULTICHANNEL Φ={phiB}  ΔΦ={dphi}")

    c1 = all(per_seed[s]["cohB"] >= per_seed[s]["cohA"] for s in SEEDS)
    c2 = all(phi_all[s]["delta"] is not None and phi_all[s]["delta"] >= MARGIN_PHI
             for s in SEEDS)
    c3 = any(per_seed[s]["cohB"] < DEGEN_CAP for s in SEEDS)

    print("-" * 72)
    print("SHUFFLE CONTROL (mc_shuffle — permuted channel→edge assignment, same edge count):")
    phi_shuf = {}
    green_seeds = [s for s in SEEDS if phi_all[s]["delta"] is not None
                   and phi_all[s]["delta"] >= MARGIN_PHI]
    shuf_check_seeds = green_seeds if green_seeds else SEEDS
    for seed in shuf_check_seeds:
        phiSh = faithful_phi(per_seed[seed]["trajSh"], f"Sh_s{seed}")
        phiA = phi_all[seed]["A"]
        dphiSh = (phiSh - phiA) if (phiSh is not None and phiA is not None) else None
        phi_shuf[seed] = {"shuffle": phiSh, "A": phiA, "delta": dphiSh}
        print(f"  seed {seed}: ARM_A Φ={phiA}  SHUFFLE Φ={phiSh}  ΔΦ_shuf={dphiSh}")
    if green_seeds:
        c4 = any(phi_shuf[s]["delta"] is not None and phi_shuf[s]["delta"] < MARGIN_PHI
                 for s in green_seeds)
    else:
        c4 = True  # no ARM-B GREEN seed → C is moot (c2 already fails)

    print("-" * 72)
    print("COHERENCE (sanity c1 + no-collapse c3):")
    for seed in SEEDS:
        ps = per_seed[seed]
        print(f"  seed {seed}: ARM_A coh={ps['cohA']:+.4f}  MULTICHANNEL coh={ps['cohB']:+.4f}  "
              f"Δcoh={ps['cohB'] - ps['cohA']:+.4f}  SHUFFLE coh={ps['cohSh']:+.4f}")

    green = c1 and c2 and c3 and c4
    verdict = "GREEN" if green else "RED"

    print("=" * 72)
    print(f"c1 coherence (B≥A every seed): {'PASS' if c1 else 'FAIL'}")
    print(f"c2 PRIMARY Φ (B≥A+{MARGIN_PHI} faithful IIT4 EVERY seed): {'PASS' if c2 else 'FAIL'}")
    for s in SEEDS:
        d = phi_all[s]["delta"]
        ok = (d is not None and d >= MARGIN_PHI)
        print(f"     seed {s}: ΔΦ={d}  {'≥' if ok else '<'} +{MARGIN_PHI}  {'PASS' if ok else 'FAIL'}")
    print(f"c3 not-degenerate (B coh < {DEGEN_CAP} ≥1 seed): {'PASS' if c3 else 'FAIL'}")
    print(f"c4 shuffle control (perm ΔΦ < +{MARGIN_PHI} on ≥1 ARM-B-GREEN seed): "
          f"{'PASS' if c4 else 'FAIL'}")
    print(f"VERDICT: {verdict}")

    result = {
        "id": "H_1283_R6", "slug": "1283_thalamus_global_workspace",
        "round": 6, "arm_b": "multi-channel parallel relay (N independent disjoint channels, one per ring edge)",
        "rubric": "Φ-primary 3-seed robust bar + pre-registered channel-assignment shuffle control",
        "verdict": verdict,
        "seeds": SEEDS,
        "n_channels": N_EDGE,
        "w_relay": W_RELAY,
        "phi_faithful_iit4": {str(s): phi_all[s] for s in SEEDS},
        "shuffle_control": {str(s): phi_shuf[s] for s in phi_shuf},
        "coherence": {str(s): {"A": per_seed[s]["cohA"], "B": per_seed[s]["cohB"],
                               "shuffle": per_seed[s]["cohSh"],
                               "delta": per_seed[s]["cohB"] - per_seed[s]["cohA"]}
                      for s in SEEDS},
        "bars": {"c1_coh_sanity": c1, "c2_phi_primary": c2,
                 "c3_not_degenerate": c3, "c4_shuffle": c4},
        "margins": {"phi_primary": MARGIN_PHI, "coh_report": MARGIN_COH, "degen_cap": DEGEN_CAP},
        "phi_engine": "hexa-lang/stdlib/consciousness/iit4/faithful_phi.hexa (exact MIP-EI, n=4)",
    }
    print("\nRESULT_JSON=" + json.dumps(result))
    return result


if __name__ == "__main__":
    main()
