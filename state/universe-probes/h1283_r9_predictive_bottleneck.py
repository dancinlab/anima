#!/usr/bin/env python3
# H_1283 R9 — THALAMUS / PREDICTIVE INFORMATION-BOTTLENECK RELAY
# slug: 1283_thalamus_global_workspace  (R9 — append-only; does NOT overwrite R1-R8)
# lens: thalamus as a PREDICTIVE RELAY / information bottleneck (neuro, c15) —
#       NOT an LLM recipe (a_no_llm_frame_trap).
#
# ════════════════════════════════════════════════════════════════════════
# THE WALL (R1-R5, from H_1283 card + verdict dir, do NOT repeat)
# ════════════════════════════════════════════════════════════════════════
# R1 broadcast hub (single winner)   : faithful ΔΦ +0.0191  (sub-bar by 0.0009)  🟠
# R2 coalition hub (rank-k, k=2)      : faithful ΔΦ −0.0533  (WRONG direction)    🔴
# R3 re-entrant loop (seed 7 only)    : faithful ΔΦ +0.1426  (cleared, coh bar)   🔴
# R4 re-entrant loop (Φ-primary 3-sd) : seed8 ΔΦ +0.0101 < +0.02  (NOT robust)    🔴
# R5 dense all-pairs + SHUFFLE        : not robust AND shuffle FIRED (variance)    🔴 🧱
#
# ROOT CAUSE (verbatim from the card): "a single broadcast channel is itself a
# low-dim cut that caps faithful-IIT4 Φ." The cut was low-dim AND ARBITRARY — it
# threw information away. Re-entrant/dense added EDGES but the relay still passed
# an UN-LEARNED, information-LOSSY signal.
#
# ════════════════════════════════════════════════════════════════════════
# R9 ANGLE — make the cut INFORMATION-PRESERVING (predictive bottleneck)
# ════════════════════════════════════════════════════════════════════════
# The relay's problem was that the cut threw information AWAY. Instead, the
# thalamic relay passes a LEARNED COMPRESSED PREDICTIVE CODE (information
# bottleneck): the relay learns — GRADIENT-FREE / delta-rule, exactly like the
# cerebellum forward model H_1280 — to transmit the MINIMAL code z (width
# CODE_DIM << module dim) that best PREDICTS the OTHER modules' NEXT state. So
# the channel, though narrow, is information-PRESERVING along the axis that
# matters for integration: the relay does not discard the predictively-relevant
# bits, it COMPRESSES toward them.
#
# Mechanically, the relay holds two learned linear maps (delta-rule updated each
# tick, no autograd):
#   ENCODER  E : module states (N_MOD·DIM) → code z (CODE_DIM)         [compress]
#   DECODER  D : code z (CODE_DIM)          → predicted next states     [predict]
# Each tick: (1) z = E · concat(states); (2) re-inject z back to every module via
# D (the relay's prediction biases each module's update); (3) AFTER the true next
# states are known, delta-update E,D to reduce the prediction error
# ‖D·(E·s_t) − s_{t+1}‖² (gradient-free outer-product / LMS delta rule — the SAME
# family as the cerebellum forward-model H_1280, p8 continuous, no train/infer
# split). The code z is the bottleneck; learning forces it to carry the bits that
# predict the other modules, i.e. the integration-relevant information.
#
# ARM A (direct ring)            — current arch, no relay.
# ARM B (predictive bottleneck)  — relay = LEARNED predictive code z (CODE_DIM).
# ARM C (random-projection)      — relay = SAME width CODE_DIM, but E,D are FIXED
#                                  RANDOM and NEVER learn. This is the LOAD-BEARING
#                                  control: it isolates the LEARNED PREDICTIVE CODE
#                                  from the mere fact of a narrow relay channel. If
#                                  B beats C, the lift is the learned code, not the
#                                  bottleneck width.
# SHUFFLE control                — B's predictive TARGETS are scrambled (the relay
#                                  learns to predict a permuted/rolled target tick),
#                                  so there is no coherent prediction to learn →
#                                  learning ΔΦ must collapse (else variance → 🧱).
#
# METRIC (p7, NO perplexity / LLM-judge):
#   coherence — mean pairwise cosine of the 4 module vectors, steady-state 2nd half.
#   Φ — FAITHFUL IIT4 (a_phi_iit4_tool), exact MIP-EI via `hexa run` over
#       hexa-lang/stdlib/consciousness/iit4/faithful_phi.hexa (n=4). numpy NEVER
#       computes Φ — it only emits the per-module salience trajectory; the stdlib
#       EXACT engine computes Φ.
#
# numpy = DIRECTIONAL mirror only (a_engine_native_learning). GREEN → engine-native
# realization is a FOLLOW-ON (a_verified_must_wire), NOT this round. $0 CPU,
# seeds [7,8,9], frozen-first. SAME frozen frame as R1-R5: 4 modules dim-8, 64
# ticks, SAME per-module private input + seed both arms, ONLY topology/relay differs.
#
# FROZEN BARS (see H_1283_R9_predictive_bottleneck.txt — FROZEN BEFORE SCORING):
#   GREEN iff ALL of:
#     c1 COHERENCE   B.coh ≥ A.coh on EVERY seed
#     c2 PRIMARY Φ   faithful ΔΦ(B−A) ≥ +0.02 on EVERY seed [7,8,9]
#     c3 NO-COLLAPSE B.coh < 0.999 on ≥1 seed (relay integrates, not collapse-clone)
#     c4 B ≥ C       faithful Φ(B) ≥ Φ(C) on EVERY seed (lift = learned code, not width)
#     c5 SHUFFLE     learning ΔΦ(shuffle−A) < +0.02 on ≥1 seed B GREENs (lift vanishes)
#   GREEN = c1 ∧ c2 ∧ c3 ∧ c4 ∧ c5.  Else RED/🧱 (closed-negative, c9 — bar NOT moved).

import os, sys, json, subprocess, tempfile
import numpy as np

SEEDS    = [7, 8, 9]
N_MOD    = 4          # {A, G, mitosis, memory}
DIM      = 8          # per-module state vector dim
T        = 64         # ticks
GAIN     = 0.30       # per-module update gain (identical all arms)
LEAK     = 0.55       # state self-retention (identical all arms; non-saturating)
NBINS    = 8          # IIT4 MI estimator bins

# --- predictive bottleneck relay hyperparameters (FROZEN) ---
CODE_DIM = 3          # relay code width z << N_MOD*DIM (=32). The information
                      # bottleneck: the narrow learned channel. 3 < DIM=8 < 32.
W_RELAY  = 0.5        # relay re-injection weight (== the ring/input coupling family,
                      # frozen since R3). The relay biases each module's update.
LR       = 0.05       # delta-rule learning rate (gradient-free LMS; cerebellum
                      # H_1280 family). Small enough to be a slow online adaptation.

MARGIN_COH = 0.0      # c1 sanity: B coherence ≥ A coherence (no degradation)
MARGIN_PHI = 0.02     # c2/c5 Φ bar (IDENTICAL to every prior round — NOT moved)
DEGEN_CAP  = 0.999    # c3 collapse-clone cap

HEXA     = "/Users/mini/.hx/bin/hexa"
HEXA_DIR = "/Users/mini/dancinlab/hexa-lang"
FAITHFUL = "stdlib/consciousness/iit4/faithful_phi.hexa"


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
    """mode in {'direct', 'predictive', 'randproj', 'shuffle'}.
    Returns (coherence, traj) with traj (N_MOD, T) per-module salience (energy).

    'direct'     — ARM A: fixed ring, each module reads only direct neighbours.
    'predictive' — ARM B: ring KEPT; ADD a thalamic relay carrying a LEARNED
                   CODE_DIM-wide predictive code. Each tick: encode states→z,
                   re-inject D·z to every module, then delta-update E,D toward the
                   true next states (gradient-free LMS). The narrow z is forced by
                   learning to carry the bits that PREDICT the other modules.
    'randproj'   — ARM C: identical wiring/width to B, but E,D are FIXED RANDOM and
                   NEVER updated (no learning). Isolates learned-code from width.
    'shuffle'    — control: like B but the predictive TARGET is scrambled (rolled
                   one module index), so there is no coherent prediction to learn.
    """
    rng = np.random.default_rng(seed)
    # initial module states — distinct per module (well-defined MI). Drawn FIRST so
    # ARM A's stream is byte-identical to every prior round and to arms B/C.
    states = rng.standard_normal((N_MOD, DIM)) * 0.5
    ring = [[1, 3], [0, 2], [1, 3], [2, 0]]   # A↔G↔mitosis↔memory↔A
    # PER-MODULE PRIVATE input (SAME all arms via same seed/order). Integration must
    # come from coupling topology, not a shared common drive (headroom for c1/c3).
    inputs = rng.standard_normal((N_MOD, T, DIM)) * 0.8
    W_NBR = 0.5   # neighbour coupling weight
    W_IN  = 0.5   # private-input weight (== coupling, keeps non-saturating regime)

    FLAT = N_MOD * DIM  # 32
    # Learned relay maps E (FLAT→CODE_DIM), D (CODE_DIM→FLAT). Drawn AFTER inputs so
    # ARM A's draws are byte-unchanged. Small init so the relay starts near-neutral
    # and the predictive code is BUILT by learning (B) — or stays random (C).
    E = rng.standard_normal((CODE_DIM, FLAT)) * 0.1
    D = rng.standard_normal((FLAT, CODE_DIM)) * 0.1

    coh_acc = []
    traj = np.zeros((N_MOD, T))
    for t in range(T):
        new = states.copy()
        if mode == "direct":
            for i in range(N_MOD):
                nbr = np.mean([states[k] for k in ring[i]], axis=0)
                new[i] = LEAK * states[i] + GAIN * (W_NBR * nbr + W_IN * inputs[i, t])
            states = new
        else:
            # ---- predictive / randproj / shuffle: ring + learned-code relay ----
            s_flat = states.reshape(FLAT)              # current concat state
            z = E @ s_flat                              # COMPRESS → code (bottleneck)
            pred_flat = D @ z                           # DECODE → predicted next state
            pred = pred_flat.reshape(N_MOD, DIM)        # relay's prediction per module
            for i in range(N_MOD):
                nbr = np.mean([states[k] for k in ring[i]], axis=0)
                # ring (kept) + private input (kept) + RELAY predictive re-injection.
                # The relay biases each module toward the integration-relevant code.
                new[i] = (LEAK * states[i]
                          + GAIN * (W_NBR * nbr
                                    + W_IN * inputs[i, t]
                                    + W_RELAY * pred[i]))
            states = new
            if mode == "predictive" or mode == "shuffle":
                # delta-rule (gradient-free LMS) update of E,D toward the TRUE next
                # state (the relay LEARNS the minimal code that predicts it). For
                # 'shuffle' the target is scrambled so no coherent code can form.
                target = states.copy()
                if mode == "shuffle":
                    target = np.roll(target, 1, axis=0)  # scramble predictive target
                tgt_flat = target.reshape(FLAT)
                err = tgt_flat - pred_flat               # prediction error (FLAT,)
                # D update: err outer z  (reduces ‖D z − target‖² by LMS)
                D += LR * np.outer(err, z)
                # E update: back-propagate error through D (chain, but computed as a
                # gradient-free outer product — the cerebellum forward-model delta
                # rule, H_1280: ΔE = LR · (Dᵀ err) ⊗ s_flat).
                E += LR * np.outer(D.T @ err, s_flat)
            # 'randproj' (ARM C): E,D FIXED — no update (random projection of same width)
        for i in range(N_MOD):
            traj[i, t] = float(np.dot(states[i], states[i]))
        if t >= T // 2:
            coh_acc.append(mean_pairwise_cosine(states))
    return float(np.mean(coh_acc)), traj


def faithful_phi(traj, tag):
    """Faithful IIT4 Φ over the n=4 module trajectories via the stdlib EXACT engine
    (hexa run). numpy NEVER computes Φ — it only emits the trajectory."""
    n, dim = traj.shape
    flat = traj.flatten()
    lines = ['import "stdlib/consciousness/iit4/faithful_phi.hexa"', "", "fn main() {",
             f"    let state = farr_zeros({n * dim})"]
    for idx, val in enumerate(flat):
        lines.append(f"    let _ = farr_set(state, {idx}, {val:.10f})")
    lines += [f"    let phi = iit4_faithful_phi(state, {n}, {dim}, {NBINS})",
              '    println("PHI=" + phi.to_string())',
              "    let _ = farr_free(state)", "}"]
    src = "\n".join(lines)
    with tempfile.NamedTemporaryFile("w", suffix=".hexa", delete=False, dir=HEXA_DIR) as f:
        path = f.name
        f.write(src)
    try:
        out = subprocess.run([HEXA, "run", os.path.basename(path)], cwd=HEXA_DIR,
                             capture_output=True, text=True, timeout=300)
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
    print("H_1283 R9 — THALAMUS / PREDICTIVE INFORMATION-BOTTLENECK RELAY")
    print(f"modules={N_MOD} dim={DIM} ticks={T} seeds={SEEDS}  "
          f"code_dim={CODE_DIM} (<<{N_MOD*DIM}) lr={LR} W_relay={W_RELAY}")
    print("ARM A = direct ring  ·  ARM B = LEARNED predictive bottleneck  ·  "
          "ARM C = RANDOM-projection (same width)")
    print("PRIMARY bar = faithful IIT4 ΔΦ ≥ +0.02 EVERY seed  ·  B≥C control  ·  "
          "SHUFFLE control (faithful IIT4 Φ, exact n=4)")
    print("=" * 72)

    per_seed = {}
    for seed in SEEDS:
        cohA, trajA = run_arm(seed, "direct")
        cohB, trajB = run_arm(seed, "predictive")
        cohC, trajC = run_arm(seed, "randproj")
        cohSh, trajSh = run_arm(seed, "shuffle")
        per_seed[seed] = {"cohA": cohA, "cohB": cohB, "cohC": cohC, "cohSh": cohSh,
                          "trajA": trajA, "trajB": trajB, "trajC": trajC, "trajSh": trajSh}

    # ---- PRIMARY Φ leg: faithful IIT4 on ALL 3 seeds, arms A / B / C ----
    print("FAITHFUL IIT4 Φ (exact MIP-EI, ALL seeds) — ARM A vs B (predictive) vs C (randproj):")
    phi_all = {}
    for seed in SEEDS:
        phiA = faithful_phi(per_seed[seed]["trajA"], f"A_s{seed}")
        phiB = faithful_phi(per_seed[seed]["trajB"], f"B_s{seed}")
        phiC = faithful_phi(per_seed[seed]["trajC"], f"C_s{seed}")
        dBA = (phiB - phiA) if (phiB is not None and phiA is not None) else None
        dBC = (phiB - phiC) if (phiB is not None and phiC is not None) else None
        phi_all[seed] = {"A": phiA, "B": phiB, "C": phiC, "dBA": dBA, "dBC": dBC}
        print(f"  seed {seed}: Φ_A={phiA}  Φ_B={phiB}  Φ_C={phiC}  "
              f"ΔΦ(B-A)={dBA}  ΔΦ(B-C)={dBC}")

    # ---- bars ----
    c1 = all(per_seed[s]["cohB"] >= per_seed[s]["cohA"] + MARGIN_COH for s in SEEDS)
    c2 = all(phi_all[s]["dBA"] is not None and phi_all[s]["dBA"] >= MARGIN_PHI for s in SEEDS)
    c3 = any(per_seed[s]["cohB"] < DEGEN_CAP for s in SEEDS)
    c4 = all(phi_all[s]["dBC"] is not None and phi_all[s]["dBC"] >= 0.0 for s in SEEDS)

    # ---- SHUFFLE control: faithful Φ on the scrambled-target arm ----
    print("-" * 72)
    print("SHUFFLE CONTROL (predictive target scrambled — learning ΔΦ must collapse):")
    green_seeds = [s for s in SEEDS if phi_all[s]["dBA"] is not None
                   and phi_all[s]["dBA"] >= MARGIN_PHI]
    check_seeds = green_seeds if green_seeds else SEEDS
    phi_shuf = {}
    for seed in check_seeds:
        phiSh = faithful_phi(per_seed[seed]["trajSh"], f"Sh_s{seed}")
        phiA = phi_all[seed]["A"]
        dSh = (phiSh - phiA) if (phiSh is not None and phiA is not None) else None
        phi_shuf[seed] = {"shuffle": phiSh, "A": phiA, "delta": dSh}
        print(f"  seed {seed}: Φ_A={phiA}  Φ_shuffle={phiSh}  ΔΦ_shuf={dSh}")
    if green_seeds:
        c5 = any(phi_shuf[s]["delta"] is not None and phi_shuf[s]["delta"] < MARGIN_PHI
                 for s in green_seeds)
    else:
        c5 = True  # no B-GREEN seed → c5 moot (c2 already fails)

    print("-" * 72)
    print("COHERENCE (c1 sanity + c3 no-collapse):")
    for seed in SEEDS:
        ps = per_seed[seed]
        print(f"  seed {seed}: coh_A={ps['cohA']:+.4f}  coh_B={ps['cohB']:+.4f}  "
              f"coh_C={ps['cohC']:+.4f}  Δcoh(B-A)={ps['cohB'] - ps['cohA']:+.4f}")

    green = c1 and c2 and c3 and c4 and c5
    verdict = "GREEN" if green else "RED"

    print("=" * 72)
    print(f"c1 coherence (B≥A every seed): {'PASS' if c1 else 'FAIL'}")
    print(f"c2 PRIMARY Φ (ΔΦ(B-A)≥+{MARGIN_PHI} faithful IIT4 EVERY seed): {'PASS' if c2 else 'FAIL'}")
    for s in SEEDS:
        d = phi_all[s]["dBA"]
        ok = (d is not None and d >= MARGIN_PHI)
        print(f"     seed {s}: ΔΦ(B-A)={d}  {'≥' if ok else '<'} +{MARGIN_PHI}  {'PASS' if ok else 'FAIL'}")
    print(f"c3 no-collapse (B coh < {DEGEN_CAP} ≥1 seed): {'PASS' if c3 else 'FAIL'}")
    print(f"c4 B≥C (Φ_B ≥ Φ_C every seed — lift = learned code not width): {'PASS' if c4 else 'FAIL'}")
    for s in SEEDS:
        d = phi_all[s]["dBC"]
        ok = (d is not None and d >= 0.0)
        print(f"     seed {s}: ΔΦ(B-C)={d}  {'≥' if ok else '<'} 0  {'PASS' if ok else 'FAIL'}")
    print(f"c5 SHUFFLE (scrambled-target ΔΦ < +{MARGIN_PHI} on ≥1 B-GREEN seed): {'PASS' if c5 else 'FAIL'}")
    print(f"VERDICT: {verdict}")
    print("NOTE (c9): if B does NOT beat BOTH A (c2) and C (c4) on every seed, this")
    print("is a valid closed-negative 🧱 — no wire, no tune, bar NOT moved (c16/p7).")

    result = {
        "id": "H_1283_R9", "slug": "1283_thalamus_global_workspace",
        "round": 9, "arm_b": "learned predictive information-bottleneck relay",
        "arm_c": "random-projection relay (same width, no learning)",
        "rubric": "Φ-primary 3-seed + B≥C random-projection control + shuffle control",
        "verdict": verdict,
        "seeds": SEEDS,
        "code_dim": CODE_DIM, "lr": LR, "w_relay": W_RELAY,
        "phi_faithful_iit4": {str(s): phi_all[s] for s in SEEDS},
        "shuffle_control": {str(s): phi_shuf[s] for s in phi_shuf},
        "coherence": {str(s): {"A": per_seed[s]["cohA"], "B": per_seed[s]["cohB"],
                               "C": per_seed[s]["cohC"],
                               "delta_BA": per_seed[s]["cohB"] - per_seed[s]["cohA"]}
                      for s in SEEDS},
        "bars": {"c1_coh": c1, "c2_phi_primary": c2, "c3_no_collapse": c3,
                 "c4_B_ge_C": c4, "c5_shuffle": c5},
        "margins": {"phi_primary": MARGIN_PHI, "coh": MARGIN_COH, "degen_cap": DEGEN_CAP},
        "phi_engine": "hexa-lang/stdlib/consciousness/iit4/faithful_phi.hexa (exact MIP-EI, n=4)",
    }
    print("\nRESULT_JSON=" + json.dumps(result))
    return result


if __name__ == "__main__":
    main()
