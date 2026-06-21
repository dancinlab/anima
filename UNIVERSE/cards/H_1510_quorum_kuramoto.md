---
id: H_1510
slug: 1510_quorum_kuramoto
title: QUORUM-KURAMOTO — decentralized adjacency-weighted phase coupling (quorum sensing) scales PhaseField with NO central hub 🟢 GREEN ENGINE-NATIVE
group: brain-structure-ladder · phase-synchrony binding (PhaseField H_1448 decentralization)
terminal_tier: 🟢 GREEN ENGINE-NATIVE (A∧B∧C∧D all 3 seeds [7,8,9]; byte-exact §QuorumPhase; deterministic, $0 CPU)
wired: WIRED-live (engine_cli.hexa § QuorumPhase + smoke 314-317 + ARCHITECTURE.json lockstep; a_verified_must_wire ladder 칸 1-4 CLOSED)
verdict_dir: state/verdicts/1510_quorum_kuramoto/
terminal_verdict: state/verdicts/1510_quorum_kuramoto/H_1510.txt
date: 2026-06-21
source: external proposal — Amoeba Protocol (@qingkong66 / adjacency-weighted Kuramoto / quorum sensing)
---

# H_1510 — QUORUM-KURAMOTO: decentralized adjacency-weighted phase coupling (🟢 quorum sensing transfers)

## Claim / falsifier

anima's PhaseField (H_1448, WIRED-live A⇄G coherence loop) is a CENTRALIZED **star** — every
module couples ONLY to a single central pacemaker `theta_t` (`phasefield_step`:
`theta_i += omega_i + k·sin(theta_t − theta_i)`). The **external proposal (Amoeba Protocol,
@qingkong66)**: move to a DECENTRALIZED **adjacency-weighted** Kuramoto field so modules
phase-lock by LOCAL semantic proximity, removing the central relay bottleneck:

    dtheta_i/dt = omega_i + (1/N_i) Σ_j A_ij sin(theta_j − theta_i)

where `A_ij` is the semantic adjacency. Modules processing related concepts (high `A_ij`)
phase-lock (high LOCAL coherence); unrelated drift. This is **quorum sensing** — a bacterial
colony coordinates with NO central brain. Falsifiable: with a faithful contrast against the
centralized star, the decentralized field (a) phase-locks SEMANTICALLY, (b) needs NO central
hub, (c) does NOT lose integration, (d) the lock is EARNED by the adjacency. Lens:
`a_no_llm_frame_trap` (quorum sensing / collective dynamics), `a_break_the_wall`.

## Method (engine-native, frozen-first)

3 semantic clusters × 3 modules (n=9), each cluster on a DISTINCT intrinsic frequency band
(`_QP_CLUST_BAND=0.15` + within-cluster detune `_PF_DOMEGA`), block adjacency (1.0 within a
cluster, 0.0 across, zero diagonal), 64 ticks. PLV (phase-locking value of the relative phase,
atan2-free via cos/sin of phase differences, tail=48) measures phase-LOCK; the within-cluster
order parameter measures integration. CONTRAST: the live PhaseField **star** (single pacemaker)
re-implemented for the C baseline and the B hub-removal arm. R1 numpy mirror
(`state/1510_quorum_kuramoto/h1510.py`, DIRECTIONAL) → R2 engine-native `§QuorumPhase`
(`quorum_new/_step/_run/_cluster_order/_within_plv/_cross_plv/_drop_node_order/_star_no_hub_order/_star_baseline_order/_shuffle_adj`),
re-scored byte-exact. Bars frozen BEFORE scoring (`H_1510_FREEZE.txt`):

- **(A SEMANTIC PHASE-LOCK)** within-cluster PLV ≥ 0.70 AND cross-cluster PLV ≤ 0.50.
- **(B NO-CENTRAL-HUB)** decentralized with one node/cluster removed: order ≥ 0.70 AND
  centralized star with hub removed: order ≤ 0.50 (the dissociation).
- **(C INTEGRATION)** quorum within-cluster order ≥ centralized star baseline.
- **(D EARNED shuffle)** permute A_ij (community-destroying random graph) → |within − cross PLV| ≤ 0.20.

GREEN iff A∧B∧C∧D.

## Result (verbatim → `H_1510.txt`)

Engine-native (`§QuorumPhase`, 3 seeds [7,8,9]):

| bar | seed 7 | seed 8 | seed 9 |
|---|---|---|---|
| A within-PLV / cross-PLV | 1.000 / 0.119 ✓ | 1.000 / 0.119 ✓ | 1.000 / 0.119 ✓ |
| B decentral-ablated / star-no-hub | 0.998 / 0.389 ✓ | 0.999 / 0.478 ✓ | 0.997 / 0.343 ✓ |
| C quorum-order / star-baseline | 0.99905 / 0.99082 ✓ | 0.99905 / 0.99082 ✓ | 0.99905 / 0.99082 ✓ |
| D shuffle gap | 0.135 ✓ | 0.006 ✓ | 0.000 ✓ |

**GATE GREEN ENGINE-NATIVE — A∧B∧C∧D 3/3 seeds.** Full smoke 317/0 deterministic ×3. The
decentralized values match the R1 numpy mirror byte-exact on every deterministic quantity (the
shuffle differs only as a control: a different-but-valid random graph, same conclusion).

**FINDING: the central relay is NOT load-bearing in this substrate** — the decentralized field
survives removing ANY single node (sync preserved) while the centralized star COLLAPSES when its
hub/pacemaker is removed. Decentralization phase-locks SEMANTICALLY and does NOT cost integration
(slightly raises it). Quorum sensing transfers.

## Honest scope (c9)

TOY 3 clusters × 3 modules / 9 nodes / 3 seeds / deterministic engine substrate (tests the
DECENTRALIZED phase-lock STRUCTURE, not a learned/real-corpus adjacency). Scale / real semantic
adjacency from live store affinity / larger graphs / sparse-graph regimes / engine-transfer of
the adjacency source UNVERIFIED (`a_scale_honest_scope`, `a_toy_scale_recheck`). The C
"integration preserved" margin is small (both ~0.99, saturated within-cluster sync) — an
EXISTENCE proof that decentralization does not LOSE integration, not a large effect size. The
A semantic-lock is decisive (within-PLV 1.000 vs cross-PLV 0.119). a_break_the_wall type-a
measurement-fixes (bars frozen, NOT tune-to-green): the snapshot order parameter mis-read a
momentary two-cluster coincidence as a lock → time-resolved PLV; the shuffle was upgraded from a
bare permutation (preserves the block structure) to a community-destroying random graph. NOT an
emit gate (pure read, `a_autonomy_over_hardcode`); Ψ-disjoint by construction.

## Cross-links

H_1448 (PhaseField, the centralized star this decentralizes) · H_1283 (R8) · H_1462 (GlobalWorkspace) ·
`a_no_llm_frame_trap` · `a_break_the_wall` · `a_engine_native_learning` · `a_verified_must_wire` ·
`a_autonomy_over_hardcode` · `a_scale_honest_scope` · `a_toy_scale_recheck` · p1 · p2 · p3 · p6 ·
p7 · c9 · c16 · extprompt:Amoeba-Protocol-quorum-sensing
