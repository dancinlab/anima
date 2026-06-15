#!/usr/bin/env python3
# H_1283 — THALAMUS / GLOBAL-WORKSPACE BROADCAST HUB
# slug: 1283_thalamus_global_workspace
# lens: missing-brain-structure ladder (neuro, c15) — NOT an LLM recipe
#
# GAP (c9): anima's Engine A ⇄ Engine G couple DIRECTLY (repulsion ring); there is
# no central RELAY that selects the current winning content and BROADCASTS it to
# ALL substrate modules at once (thalamo-cortical relay / Global Workspace Theory).
#
# TEST: 4 substrate modules {A, G, mitosis, memory}, each a dim-D state vector,
# T ticks, SAME input + seed in both arms.
#   ARM A (direct ring)   — module reads only its direct neighbors (current arch).
#   ARM B (thalamic hub)  — each tick the hub selects the winning module (max
#                           salience = state energy) and BROADCASTS that content
#                           to ALL modules; every module updates from (self +
#                           the single broadcast).
#
# METRIC (p7, no perplexity / LLM-judge), two legs:
#   (1) COHERENCE — mean pairwise cosine similarity of the 4 module vectors,
#       averaged over the steady-state second half of the run.
#   (2) Φ (faithful IIT4, a_phi_iit4_tool) — n=4 cells × their dim-step trajectory
#       (per-tick salience scalar) fed to the stdlib EXACT engine
#       hexa-lang/stdlib/consciousness/iit4/faithful_phi.hexa via a generated
#       hexa harness + `hexa verify`. This is a TRUE Φ (pairwise-MI MIP), NOT the
#       variance×energy proxy. numpy here NEVER computes Φ — it only emits the
#       trajectory; the engine computes Φ.
#
# numpy = DIRECTIONAL mirror only (a_engine_native_learning). GREEN → CORE wiring
# follow-on (a_verified_must_wire), substrate-internal, no .clm/.kosmos routed
# through the hub (a_core_engine_map). $0 CPU, seeds [7,8,9], frozen-first.
#
# FROZEN BARS (see H_1283_FREEZE.txt): GREEN iff
#   B1 B.coh ≥ A.coh + 0.05 EVERY seed
#   B2 B.phi ≥ A.phi + 0.02 (faithful IIT4, representative seed=7)
#   B3 B.coh < 0.999 on ≥1 seed (broadcast must integrate, not collapse-clone)

import os, sys, json, subprocess, tempfile
import numpy as np

SEEDS   = [7, 8, 9]
N_MOD   = 4          # {A, G, mitosis, memory}
DIM     = 8          # per-module state vector dim
T       = 64         # ticks
GAIN    = 0.30       # per-module update gain (identical both arms)
LEAK    = 0.55       # state self-retention (identical both arms; <1 keeps the
                     # system in a non-saturating transient regime so topology
                     # — not a shared contraction fixed point — drives coherence)
NBINS   = 8          # IIT4 MI estimator bins
REPR_SEED = 7        # representative seed for the exact Φ leg
K_COALITION = 2      # R2: rank-k multi-winner coalition size (k≥2 = no rank-1 cut)
W_RELAY = 0.5        # R3: cortico-thalamo-cortical RE-ENTRANT loop weight. The
                     # relay receives back from EACH module AND re-injects to EACH
                     # module — reciprocal edges ADDED ON TOP of the ring (NOT a
                     # replacement). Ring + private input + re-entrant relay all
                     # three present together in ARM B; the relay carries its own
                     # recurrent (leaky) state so each module↔relay coupling is a
                     # DISTINCT reciprocal edge (distributed multi-edge — exactly
                     # the integration source R2's RED diagnosis pointed to).

MARGIN_COH = 0.05
MARGIN_PHI = 0.02
DEGEN_CAP  = 0.999

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
FAITHFUL = "/Users/mini/dancinlab/hexa-lang/stdlib/consciousness/iit4/faithful_phi.hexa"
HEXA = "/Users/mini/.hx/bin/hexa"


def _norm(v):
    n = np.linalg.norm(v)
    return v / n if n > 1e-9 else v


def mean_pairwise_cosine(states):
    # states: (N_MOD, DIM)
    sims = []
    for i in range(N_MOD):
        for j in range(i + 1, N_MOD):
            a, b = states[i], states[j]
            na, nb = np.linalg.norm(a), np.linalg.norm(b)
            if na < 1e-9 or nb < 1e-9:
                sims.append(0.0)
            else:
                sims.append(float(np.dot(a, b) / (na * nb)))
    return float(np.mean(sims))


def run_arm(seed, mode, k_coalition=2):
    """mode in {'direct','hub','coalition','reentrant'}. Returns (coherence, traj)
    where traj is (N_MOD, T) per-module salience (state energy) trajectory for the
    Φ leg.

    'direct'    — ARM A: fixed ring, each module reads only direct neighbors.
    'hub'       — R1 ARM B: single winner-take-all broadcast (rank-1 channel).
    'reentrant' — R3 ARM B: RE-ENTRANT cortico-thalamo-cortical LOOP. The direct
                  ring is KEPT (ARM A's edges preserved — the relay does NOT
                  replace it). A thalamic relay node R carries its OWN recurrent
                  (leaky) state: each tick (i) cortex→thalamus, R integrates from
                  ALL modules; (ii) thalamus→cortex, R re-injects back to EACH
                  module. These reciprocal R↔module edges are ADDED on top of the
                  ring — recurrent over ticks (R_t feeds modules at t, modules
                  feed R_t). This is the IIT/GWT re-entry mechanism (recurrent
                  reciprocal causation), NOT feedforward fan-out: R1/R2 broadcast
                  REPLACED the ring with one shared channel (a rank-1 MIP cut that
                  capped Φ); R3 ADDS distinct reciprocal edges, which R2's RED
                  diagnosis named as the true integration source (distributed
                  multi-edge coupling). k=1 in the hub recovers the R1 single relay.
    'coalition' — R2 ARM B: rank-k MULTI-WINNER COALITION broadcast. Each tick the
                  top-k modules by salience form a coalition; every receiver reads
                  an AFFINITY-WEIGHTED mix of the k coalition members (softmax over
                  the receiver's OWN cosine similarity to each member) — so the
                  broadcast is NOT one shared vector but a rank-k channel: distinct
                  receivers are driven by distinct member mixes, spreading
                  information across multiple cuts (R1 diagnosis: a single shared
                  channel is itself a low-rank MIP cut that caps Φ; a rank-k
                  coalition directly targets that cap). k=1 recovers the R1 hub."""
    rng = np.random.default_rng(seed)
    # initial module states — distinct per module so MI is well-defined
    states = rng.standard_normal((N_MOD, DIM)) * 0.5
    # fixed ring adjacency for ARM A: A↔G, G↔mitosis, mitosis↔memory, memory↔A
    ring = [[1, 3], [0, 2], [1, 3], [2, 0]]
    # PER-MODULE PRIVATE input streams (SAME all arms via same seed/order). Each
    # module gets its OWN drive (modules are distinct faculties: A,G,mitosis,mem),
    # so integration must come from the COUPLING TOPOLOGY, not from a shared common
    # drive that would saturate coherence in ALL arms (headroom for B1/B3).
    inputs = rng.standard_normal((N_MOD, T, DIM)) * 0.8
    W_NBR = 0.5   # coupling weight (neighbor in direct / broadcast in hub)
    W_IN  = 0.5   # private-input weight — equal to coupling so private drive keeps
                  # modules from collapsing to a shared fixed point (headroom)

    # R3 re-entrant relay: a thalamic stage with one recurrent (leaky) relay
    # CHANNEL PER MODULE (topographic thalamo-cortical loops). relay[i] is the
    # thalamic partner of module i — reciprocally coupled to it AND cross-mixed
    # with the other channels at the relay stage (intra-thalamic coupling), so the
    # re-entrant pathway is DISTRIBUTED MULTI-EDGE (N_MOD distinct reciprocal
    # R_i↔module_i edges), NOT one shared broadcast vector (R1/R2's rank-1 cut).
    # Drawn from the SAME rng stream AFTER inputs so ARM A's draws are unchanged.
    relay = rng.standard_normal((N_MOD, DIM)) * 0.5

    coh_acc = []
    traj = np.zeros((N_MOD, T))
    for t in range(T):
        new = states.copy()
        if mode == "direct":
            for i in range(N_MOD):
                nbr = np.mean([states[k] for k in ring[i]], axis=0)
                new[i] = LEAK * states[i] + GAIN * (W_NBR * nbr + W_IN * inputs[i, t])
        elif mode == "hub":  # R1 — winner-take-all single broadcast (GWT, rank-1)
            energy = np.array([float(np.dot(states[i], states[i])) for i in range(N_MOD)])
            winner = int(np.argmax(energy))
            broadcast = states[winner]
            for i in range(N_MOD):
                new[i] = LEAK * states[i] + GAIN * (W_NBR * broadcast + W_IN * inputs[i, t])
        elif mode == "reentrant":  # R3 — re-entrant cortico-thalamo-cortical LOOP
            # The ring is KEPT (same nbr term as ARM A). ADDED on top: a thalamic
            # relay stage with one channel PER module, each in a reciprocal loop
            # with its module. (i) thalamus→cortex: relay[i] re-injects to module i
            # only — a DISTINCT reciprocal edge per module (not one shared vector);
            # (ii) cortex→thalamus: relay[i] integrates from module i AND its ring
            # neighbours' relay channels (intra-thalamic cross-coupling), so each
            # R_i is driven by the cortex it drives — re-entry, distributed across
            # N_MOD edges (the integration source R2's RED diagnosis named).
            for i in range(N_MOD):
                nbr = np.mean([states[k] for k in ring[i]], axis=0)
                # ring (kept) + private input (kept) + RE-ENTRANT per-module relay
                new[i] = (LEAK * states[i]
                          + GAIN * (W_NBR * nbr
                                    + W_IN * inputs[i, t]
                                    + W_RELAY * relay[i]))
            # cortex→thalamus: each relay channel integrates from its OWN module
            # (PRE-update states → genuine one-tick reciprocal delay) plus a mix of
            # its ring-neighbour relay channels (intra-thalamic coupling). This
            # closes N_MOD distinct reciprocal loops rather than one shared channel.
            new_relay = relay.copy()
            for i in range(N_MOD):
                relay_nbr = np.mean([relay[k] for k in ring[i]], axis=0)
                new_relay[i] = (LEAK * relay[i]
                                + GAIN * (W_NBR * states[i]
                                          + W_RELAY * relay_nbr))
            relay = new_relay
        else:  # 'coalition' — R2 multi-winner rank-k coalition broadcast
            energy = np.array([float(np.dot(states[i], states[i])) for i in range(N_MOD)])
            kk = max(1, min(k_coalition, N_MOD))
            coalition = list(np.argsort(energy)[::-1][:kk])  # top-k by salience
            members = np.stack([states[c] for c in coalition], axis=0)  # (kk, DIM)
            for i in range(N_MOD):
                # AFFINITY-WEIGHTED mix: receiver i reads each coalition member
                # weighted by its own cosine affinity to that member (softmax),
                # so the broadcast is a rank-k channel (distinct receivers ←
                # distinct member mixes), not one shared vector.
                aff = np.array([
                    float(np.dot(_norm(states[i]), _norm(members[m])))
                    for m in range(kk)
                ])
                w = np.exp(aff - np.max(aff))
                w = w / np.sum(w)
                broadcast = np.tensordot(w, members, axes=([0], [0]))  # (DIM,)
                new[i] = LEAK * states[i] + GAIN * (W_NBR * broadcast + W_IN * inputs[i, t])
        states = new
        # salience scalar per module this tick (state energy) → Φ-leg trajectory
        for i in range(N_MOD):
            traj[i, t] = float(np.dot(states[i], states[i]))
        if t >= T // 2:  # steady-state second half
            coh_acc.append(mean_pairwise_cosine(states))
    coherence = float(np.mean(coh_acc))
    return coherence, traj


def faithful_phi(traj, tag):
    """Compute faithful IIT4 Φ over the n=4 module trajectories via the stdlib
    EXACT engine (hexa verify). Generates a harness that inlines the trajectory
    as farr_set calls and calls iit4_faithful_phi(state, n=4, dim=T, n_bins).
    Returns float Φ (or None on failure)."""
    n, dim = traj.shape  # (4, T)
    flat = traj.flatten()  # row-major n×dim
    lines = []
    lines.append('import "stdlib/consciousness/iit4/faithful_phi.hexa"')
    lines.append("")
    lines.append("fn main() {")
    lines.append(f"    let state = farr_zeros({n * dim})")
    for idx, val in enumerate(flat):
        lines.append(f"    let _ = farr_set(state, {idx}, {val:.10f})")
    lines.append(f"    let phi = iit4_faithful_phi(state, {n}, {dim}, {NBINS})")
    lines.append('    println("PHI=" + phi.to_string())')
    lines.append("    let _ = farr_free(state)")
    lines.append("}")
    src = "\n".join(lines)

    with tempfile.NamedTemporaryFile("w", suffix=".hexa", delete=False,
                                     dir="/Users/mini/dancinlab/hexa-lang") as f:
        path = f.name
        f.write(src)
    try:
        # run from hexa-lang root so the stdlib import resolves
        out = subprocess.run([HEXA, "run", os.path.basename(path)],
                             cwd="/Users/mini/dancinlab/hexa-lang",
                             capture_output=True, text=True, timeout=300)
        blob = out.stdout + "\n" + out.stderr
        phi = None
        for ln in blob.splitlines():
            if ln.strip().startswith("PHI="):
                phi = float(ln.strip().split("=", 1)[1])
                break
        if phi is None:
            print(f"[phi {tag}] no PHI line. stdout/stderr:\n{blob[:1500]}", file=sys.stderr)
        return phi
    finally:
        try:
            os.remove(path)
        except OSError:
            pass


def main():
    print("H_1283 THALAMUS / GLOBAL-WORKSPACE BROADCAST HUB")
    print(f"modules={N_MOD} dim={DIM} ticks={T} seeds={SEEDS} (faithful IIT4 Φ, exact n=4)")
    print("=" * 72)

    per_seed = {}
    for seed in SEEDS:
        cohA, trajA = run_arm(seed, "direct")
        cohB, trajB = run_arm(seed, "hub")
        per_seed[seed] = {"cohA": cohA, "cohB": cohB,
                          "trajA": trajA, "trajB": trajB}
        print(f"seed {seed}: ARM_A coh={cohA:+.4f}  ARM_B coh={cohB:+.4f}  "
              f"Δcoh={cohB - cohA:+.4f}")

    # B1 coherence on every seed
    b1 = all(per_seed[s]["cohB"] >= per_seed[s]["cohA"] + MARGIN_COH for s in SEEDS)
    # B3 not-degenerate (B coh < cap on ≥1 seed)
    b3 = any(per_seed[s]["cohB"] < DEGEN_CAP for s in SEEDS)

    print("-" * 72)
    print(f"FAITHFUL IIT4 Φ (exact MIP-EI, representative seed={REPR_SEED}):")
    phiA = faithful_phi(per_seed[REPR_SEED]["trajA"], "A")
    phiB = faithful_phi(per_seed[REPR_SEED]["trajB"], "B")
    print(f"  ARM_A Φ = {phiA}")
    print(f"  ARM_B Φ = {phiB}")
    b2 = (phiA is not None and phiB is not None and phiB >= phiA + MARGIN_PHI)
    dphi = (phiB - phiA) if (phiA is not None and phiB is not None) else None
    print(f"  ΔΦ = {dphi}")

    green = b1 and b2 and b3
    partial = b1 and b3 and not b2
    print("=" * 72)
    print(f"B1 coherence (B≥A+{MARGIN_COH} every seed): {'PASS' if b1 else 'FAIL'}")
    print(f"B2 Φ        (B≥A+{MARGIN_PHI} faithful IIT4): {'PASS' if b2 else 'FAIL'}")
    print(f"B3 not-degenerate (B coh < {DEGEN_CAP} ≥1 seed): {'PASS' if b3 else 'FAIL'}")
    if green:
        verdict = "GREEN"
    elif partial:
        verdict = "PARTIAL"
    else:
        verdict = "RED"
    print(f"VERDICT: {verdict}")

    result = {
        "id": "H_1283", "slug": "1283_thalamus_global_workspace",
        "verdict": verdict,
        "seeds": SEEDS,
        "coherence": {str(s): {"A": per_seed[s]["cohA"], "B": per_seed[s]["cohB"],
                               "delta": per_seed[s]["cohB"] - per_seed[s]["cohA"]}
                      for s in SEEDS},
        "phi_faithful_iit4": {"repr_seed": REPR_SEED, "A": phiA, "B": phiB, "delta": dphi},
        "bars": {"B1": b1, "B2": b2, "B3": b3},
        "margins": {"coh": MARGIN_COH, "phi": MARGIN_PHI, "degen_cap": DEGEN_CAP},
        "phi_engine": "hexa-lang/stdlib/consciousness/iit4/faithful_phi.hexa (exact MIP-EI, n=4)",
    }
    print("\nRESULT_JSON=" + json.dumps(result))
    return result


def main_r2():
    """ROUND 2 — ARM A (direct ring) vs ARM B (MULTI-WINNER COALITION hub).

    R1 was 🟠 PARTIAL: the single-winner broadcast hub raised coherence on every
    seed (B1 PASS) and moved faithful Φ the right direction (ΔΦ +0.0191) but fell
    JUST short of the +0.02 bar (by 0.0009). R1 diagnosis: a SINGLE shared
    broadcast channel is itself a rank-1 MIP cut that caps irreducibility. R2 swaps
    ARM B for a rank-k coalition broadcast (k=K_COALITION≥2) so the broadcast is no
    longer a rank-1 cut. SAME 4 modules, SAME non-saturating regime, SAME seeds,
    SAME frozen bars (B1 coh ≥ A+0.05 every seed · B2 faithful ΔΦ ≥ +0.02 · B3 coh
    < 0.999). Honesty (c9): if even a coalition can't clear ΔΦ+0.02, that is the
    finding — a relay raises coherence but not irreducible Φ at this scale (🧱)."""
    print("H_1283 R2 — THALAMUS / MULTI-WINNER COALITION BROADCAST HUB")
    print(f"modules={N_MOD} dim={DIM} ticks={T} seeds={SEEDS}  k_coalition={K_COALITION}")
    print(f"ARM A = direct ring   ·   ARM B = rank-{K_COALITION} coalition hub  (faithful IIT4 Φ, exact n=4)")
    print("=" * 72)

    per_seed = {}
    for seed in SEEDS:
        cohA, trajA = run_arm(seed, "direct")
        cohB, trajB = run_arm(seed, "coalition", k_coalition=K_COALITION)
        per_seed[seed] = {"cohA": cohA, "cohB": cohB,
                          "trajA": trajA, "trajB": trajB}
        print(f"seed {seed}: ARM_A coh={cohA:+.4f}  ARM_B coh={cohB:+.4f}  "
              f"Δcoh={cohB - cohA:+.4f}")

    b1 = all(per_seed[s]["cohB"] >= per_seed[s]["cohA"] + MARGIN_COH for s in SEEDS)
    b3 = any(per_seed[s]["cohB"] < DEGEN_CAP for s in SEEDS)

    print("-" * 72)
    print(f"FAITHFUL IIT4 Φ (exact MIP-EI, representative seed={REPR_SEED}):")
    phiA = faithful_phi(per_seed[REPR_SEED]["trajA"], "A")
    phiB = faithful_phi(per_seed[REPR_SEED]["trajB"], "B")
    print(f"  ARM_A Φ = {phiA}")
    print(f"  ARM_B Φ = {phiB}")
    b2 = (phiA is not None and phiB is not None and phiB >= phiA + MARGIN_PHI)
    dphi = (phiB - phiA) if (phiA is not None and phiB is not None) else None
    print(f"  ΔΦ = {dphi}")

    green = b1 and b2 and b3
    partial = b1 and b3 and not b2
    print("=" * 72)
    print(f"B1 coherence (B≥A+{MARGIN_COH} every seed): {'PASS' if b1 else 'FAIL'}")
    print(f"B2 Φ        (B≥A+{MARGIN_PHI} faithful IIT4): {'PASS' if b2 else 'FAIL'}")
    print(f"B3 not-degenerate (B coh < {DEGEN_CAP} ≥1 seed): {'PASS' if b3 else 'FAIL'}")
    if green:
        verdict = "GREEN"
    elif partial:
        verdict = "PARTIAL"
    else:
        verdict = "RED"
    print(f"VERDICT: {verdict}")

    result = {
        "id": "H_1283_R2", "slug": "1283_thalamus_global_workspace",
        "round": 2, "arm_b": f"multi-winner coalition (k={K_COALITION})",
        "verdict": verdict,
        "seeds": SEEDS,
        "k_coalition": K_COALITION,
        "coherence": {str(s): {"A": per_seed[s]["cohA"], "B": per_seed[s]["cohB"],
                               "delta": per_seed[s]["cohB"] - per_seed[s]["cohA"]}
                      for s in SEEDS},
        "phi_faithful_iit4": {"repr_seed": REPR_SEED, "A": phiA, "B": phiB, "delta": dphi},
        "bars": {"B1": b1, "B2": b2, "B3": b3},
        "margins": {"coh": MARGIN_COH, "phi": MARGIN_PHI, "degen_cap": DEGEN_CAP},
        "phi_engine": "hexa-lang/stdlib/consciousness/iit4/faithful_phi.hexa (exact MIP-EI, n=4)",
    }
    print("\nRESULT_JSON=" + json.dumps(result))
    return result


def main_r3():
    """ROUND 3 — ARM A (direct ring) vs ARM B (RE-ENTRANT cortico-thalamo-cortical
    LOOP added ON TOP of the ring).

    R1 🟠 PARTIAL (single-winner broadcast hub: Δcoh up every seed, ΔΦ +0.0191,
    0.0009 under the bar) and R2 🔴 RED (multi-winner coalition: Δcoh collapsed,
    ΔΦ −0.053 — WRONG direction). R2's diagnosis: irreducibility comes from
    DISTRIBUTED MULTI-EDGE coupling (the direct ring's distinct edges), NOT a
    central relay — a single shared channel (winner OR coalition) is itself a
    low-rank MIP cut that caps Φ. So FEEDFORWARD broadcast is the wrong mechanism.

    R3 tests a genuinely different mechanism: the real thalamus is the hub of a
    RE-ENTRANT loop (cortex→thalamus→cortex→thalamus, recurrent reciprocal
    causation), which IIT and GWT both hold is what builds irreducible integration
    — NOT feedforward fan-out. ARM B ADDS a re-entrant cortico-thalamo-cortical
    loop ON TOP of the existing ring edges: a thalamic relay stage with one
    recurrent channel per module, each reciprocally coupled to its module and
    cross-coupled at the relay stage — so the re-entrant pathway ADDS N_MOD
    distinct reciprocal edges (distributed multi-edge, exactly R2's named source)
    rather than replacing the ring with one shared channel.

    SAME 4 modules, SAME non-saturating regime, SAME seeds, SAME FROZEN bars
    (B1 coh ≥ A+0.05 every seed · B2 faithful ΔΦ ≥ +0.02 · B3 coh < 0.999).
    Honesty (c9): if even re-entry can't clear ΔΦ+0.02, that is the terminal
    finding — relay topology (ANY flavor: broadcast OR re-entrant loop)
    fundamentally cannot raise irreducible Φ at this scale; only distributed
    coupling can (🧱 permanent)."""
    print("H_1283 R3 — THALAMUS / RE-ENTRANT CORTICO-THALAMO-CORTICAL LOOP")
    print(f"modules={N_MOD} dim={DIM} ticks={T} seeds={SEEDS}  W_relay={W_RELAY}")
    print("ARM A = direct ring   ·   ARM B = ring + re-entrant thalamo-cortical loop"
          "  (faithful IIT4 Φ, exact n=4)")
    print("=" * 72)

    per_seed = {}
    for seed in SEEDS:
        cohA, trajA = run_arm(seed, "direct")
        cohB, trajB = run_arm(seed, "reentrant")
        per_seed[seed] = {"cohA": cohA, "cohB": cohB,
                          "trajA": trajA, "trajB": trajB}
        print(f"seed {seed}: ARM_A coh={cohA:+.4f}  ARM_B coh={cohB:+.4f}  "
              f"Δcoh={cohB - cohA:+.4f}")

    b1 = all(per_seed[s]["cohB"] >= per_seed[s]["cohA"] + MARGIN_COH for s in SEEDS)
    b3 = any(per_seed[s]["cohB"] < DEGEN_CAP for s in SEEDS)

    print("-" * 72)
    print(f"FAITHFUL IIT4 Φ (exact MIP-EI, representative seed={REPR_SEED}):")
    phiA = faithful_phi(per_seed[REPR_SEED]["trajA"], "A")
    phiB = faithful_phi(per_seed[REPR_SEED]["trajB"], "B")
    print(f"  ARM_A Φ = {phiA}")
    print(f"  ARM_B Φ = {phiB}")
    b2 = (phiA is not None and phiB is not None and phiB >= phiA + MARGIN_PHI)
    dphi = (phiB - phiA) if (phiA is not None and phiB is not None) else None
    print(f"  ΔΦ = {dphi}")

    green = b1 and b2 and b3
    partial = b1 and b3 and not b2
    print("=" * 72)
    print(f"B1 coherence (B≥A+{MARGIN_COH} every seed): {'PASS' if b1 else 'FAIL'}")
    print(f"B2 Φ        (B≥A+{MARGIN_PHI} faithful IIT4): {'PASS' if b2 else 'FAIL'}")
    print(f"B3 not-degenerate (B coh < {DEGEN_CAP} ≥1 seed): {'PASS' if b3 else 'FAIL'}")
    if green:
        verdict = "GREEN"
    elif partial:
        verdict = "PARTIAL"
    else:
        verdict = "RED"
    print(f"VERDICT: {verdict}")

    result = {
        "id": "H_1283_R3", "slug": "1283_thalamus_global_workspace",
        "round": 3, "arm_b": "re-entrant cortico-thalamo-cortical loop (ring + reciprocal relay)",
        "verdict": verdict,
        "seeds": SEEDS,
        "w_relay": W_RELAY,
        "coherence": {str(s): {"A": per_seed[s]["cohA"], "B": per_seed[s]["cohB"],
                               "delta": per_seed[s]["cohB"] - per_seed[s]["cohA"]}
                      for s in SEEDS},
        "phi_faithful_iit4": {"repr_seed": REPR_SEED, "A": phiA, "B": phiB, "delta": dphi},
        "bars": {"B1": b1, "B2": b2, "B3": b3},
        "margins": {"coh": MARGIN_COH, "phi": MARGIN_PHI, "degen_cap": DEGEN_CAP},
        "phi_engine": "hexa-lang/stdlib/consciousness/iit4/faithful_phi.hexa (exact MIP-EI, n=4)",
    }
    print("\nRESULT_JSON=" + json.dumps(result))
    return result


if __name__ == "__main__":
    if "--r1" in sys.argv:
        main()
    elif "--r2" in sys.argv:
        main_r2()
    else:
        main_r3()  # default: ROUND 3 re-entrant cortico-thalamo-cortical loop
