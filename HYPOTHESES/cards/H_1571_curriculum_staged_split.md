---
id: H_1571
slug: 1571_curriculum_staged_split
title: CURRICULUM-STAGED split mitosis (H_1310 wall-break lens 4 — staged error-curriculum cell allocation)
group: MITOSIS-ENGINE (H_1310 from-scratch ceiling — wall-break campaign, lens 4 of 4)
tier: 🧱 WALL HOLDS (ENGINE-NATIVE) — B1∧B2∧B3 all FAIL (curriculum HURTS; residual gate inert)
verdict_dir: state/verdicts/1571_curriculum_staged_split/
date: 2026-06-23
wired: engine-native (pure .hexa via core/engine_cli.hexa §Osmotic; no wiring — wall)
---

# H_1571 — curriculum-staged split mitosis (H_1310 lens 4)

## Claim / falsifier

A single online pass splits cells in arrival order — frequent/easy contexts grab cells first, rare/
hard contexts may never get one (a budget+order problem; H_1534 budget-precondition precedent).
Biology grows capacity in STAGES (critical periods). **Lens 4:** present the corpus as a
CURRICULUM — stage 1 locks coarse cells on high-frequency contexts, stage 2 splits only on the
residual-error (rare/hard) contexts early cells own poorly. Same total cells, allocated by an
error-curriculum instead of arrival order.

**Falsifier:** if staged error-curriculum allocation lifts held-out CE below the flat ceiling
(≥0.10 nats), it breaks the wall. If inert/harmful, the wall holds (honest 🧱).

## Method (ENGINE-NATIVE — pure .hexa via core/, HARD-GATE-1 PASS)

`state/1571_curriculum_staged_split/h1571_curriculum_split_probe.hexa` over the LIVE OsmoticStore
(`core/engine_cli.hexa §Osmotic`), inherited `immune_embed_key` keys, **NO numpy/torch/.py**. The
curriculum is only the ORDER + GATING of `osmotic_learn` calls — no new mechanism. $0 CPU summer,
hexa v0.262.0, corpus `head -c 12000`, order-2, V=27, 80/20.

ARMS (same training pairs; only presentation order/gating differs): **A_flat** (corpus order, the
H_1569 ceiling) · **A_curriculum** (stage-1 high-freq → stage-2 residual-error-gated split) ·
**A_ablate** (staged but residual gate OFF) · **A_shuf** (random stage assignment).

## Frozen 5-bar (BEFORE the run — c9; 🟢 iff B1∧B2∧B3)

- **B1 BREAK** CE_curriculum < CE_flat − 0.10
- **B2 ABLATION** CE_ablate ≥ CE_curriculum + 0.05 (disabling the residual gate removes the lift)
- **B3 CAUSAL** CE_shuf ≥ CE_curriculum + 0.05 (random stage order removes the lift)
- **B4 vs-FLOOR** CE_curriculum ≤ CE_floor + 0.02 [report+gate]
- **B5** report cells.

## Verdict (VERBATIM from state/verdicts/1571_curriculum_staged_split/H_1571_R1_ENGINE_NATIVE.txt)

Held-out next-byte CE (nats), 12000-byte:

| arm | CE | cells |
|---|---|---|
| A_flat (corpus-order ceiling) | 3.08782 | 64 |
| A_curriculum (staged+gate) | 3.26073 | 64 |
| A_ablate (gate OFF) | 3.26073 | 64 |
| A_shuf (random stage order) | 3.12387 | 64 |
| n-gram FLOOR | 2.84769 | — |

- **B1 BREAK FAIL** — curriculum 3.26073 is +0.173 nats **WORSE** than flat 3.08782.
- **B2 FAIL** — A_curriculum == A_ablate byte-exact → the residual-error gate is INERT; the staged
  frequency partition itself changed CE (for the worse).
- **B3 FAIL** — shuf 3.12387 BEATS curriculum 3.26073 → the curriculum order carries no useful info.
- **B4 FAIL** — curriculum +0.413 above floor.

**TERMINAL TIER (this lens): 🧱 WALL HOLDS (ENGINE-NATIVE).**

## What this means (c9) — the campaign closes confidently

Curriculum staging HURTS: early-locked coarse cells over-own the key space, so late hard contexts
collide into them rather than getting fresh cells; the residual gate is inert. Any 2-pass staging
just disturbs the flat single-pass allocation (shuffled order beats the frequency curriculum).

**This is the 3rd orthogonal engine-native lens** (after H_1569 inherited-repr, +0.056 under bar,
and H_1570 lateral-transfer, inert/harmful). With H_1568 (selection-driven evolution, DIRECTIONAL),
the H_1310 wall now has **≥3 distinct mechanism-family lenses, each ablation-clean, all failing** →
c16 multi-lens confident terminal ceiling. The bottleneck is **structural**: split-only mitosis
builds a Voronoi partition of a *fixed feature* with NO compositional depth; re-ordering, sharing, or
staging that partition cannot cross the floor a *learned* representation clears. The user's
pretrained-split insight (H_1569) is the right direction — but it requires a representation that is
LEARNED/adapted (a real pretrained trunk hidden state), not the engine's fixed trigram encoder nor
any re-allocation of fixed local experts.

## Honest scope (c9, a_scale_honest_scope)

ENGINE-NATIVE (pure .hexa via core/ §Osmotic) → terminal. TOY scale (12 KB English, order-2). The
UNVERIFIED next rung (if the wall is ever revisited): mount a TRUE corpus-LEARNED trunk hidden state
(e.g. a 303M chat ckpt context embedding) as the mitosis key — the only remaining variant of the
H_1569 insight that supplies a *learned* (not hand-crafted) representation. NO CORE wiring (wall).
