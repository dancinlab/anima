---
id: H_1570
slug: 1570_lateral_gene_transfer
title: LATERAL GENE TRANSFER mitosis (H_1310 wall-break lens 2 — horizontal sharing of learned cell statistics)
group: MITOSIS-ENGINE (H_1310 from-scratch ceiling — wall-break campaign, lens 2 of 3+)
tier: 🧱 WALL HOLDS (ENGINE-NATIVE) — B1 BREAK FAIL (B2 ablation byte-exact clean, B3 causal FAIL)
verdict_dir: state/verdicts/1570_lateral_gene_transfer/
date: 2026-06-23
wired: engine-native (pure .hexa via core/engine_cli.hexa §Osmotic; no wiring — wall, a_verified_must_wire fires only on GREEN)
---

# H_1570 — lateral gene transfer mitosis (H_1310 lens 2)

## Claim / falsifier

Pure vertical-descent mitosis (parent→daughter split) has NO horizontal channel for sharing what
cells LEARN. Bacteria escape local optima via **lateral gene transfer** (horizontal transfer of
acquired traits between peers). H_1569 sharpened the angle: the representation must be
learnable/expandable. **Lens 2:** let cells SHARE their learned next-byte statistics horizontally —
each cell's predictive value enriched by its key-space neighbors' learned values.

**Falsifier:** if horizontal value-sharing lifts held-out next-byte CE below the vertical-only
ceiling (≥0.10 nats), it breaks the wall. If it is inert/harmful, the wall holds (honest 🧱).

## Method (ENGINE-NATIVE — pure .hexa via core/, HARD-GATE-1 PASS)

`state/1570_lateral_gene_transfer/h1570_lateral_transfer_probe.hexa` trains the LIVE OsmoticStore
(`core/engine_cli.hexa §Osmotic`) over the inherited `immune_embed_key` representation (== H_1569
A_repr), then at TEST time pools each cell's value with its k=4 key-space nearest cells'
learned values (distance-weighted over the engine's OWN `_l2` affinity on `st.field.protos`),
blend β=0.60. **NO numpy/torch/.py.** $0 CPU summer, hexa v0.262.0, corpus `/usr/share/dict/words`
`head -c 12000`, order-2 ctx, V=27, 80/20.

ARMS (all byte-identical except whether values share laterally): **A_descent** (vertical-only, the
H_1569 ceiling) · **A_lateral** (transfer ON) · **A_ablate** (β=0 → == descent) · **A_shuf**
(random-peer pool, geometry destroyed).

## Frozen 5-bar (BEFORE the run — c9; 🟢 iff B1∧B2∧B3)

- **B1 BREAK** CE_lateral < CE_descent − 0.10
- **B2 ABLATION** CE_ablate == CE_descent (byte-exact — mechanism not a code-path artifact)
- **B3 CAUSAL** CE_shuf ≥ CE_lateral + 0.05 (lift must ride the _l2 geometry)
- **B4 vs-FLOOR** CE_lateral ≤ CE_floor + 0.02 [report+gate]
- **B5** report cells.

## Verdict (VERBATIM from state/verdicts/1570_lateral_gene_transfer/H_1570_R1_ENGINE_NATIVE.txt)

Held-out next-byte CE (nats), 12000-byte:

| arm | CE | cells |
|---|---|---|
| A_descent (vertical-only) | 3.08782 | 64 |
| A_lateral (transfer ON) | 3.08195 | — |
| A_ablate (β=0) | 3.08782 | — |
| A_shuf (random-peer) | 3.08603 | — |
| n-gram FLOOR | 2.84769 | — |

- **B1 BREAK FAIL** — lateral 3.08195 vs descent−0.10 (2.98782): lift only **+0.0059 nats ≪ 0.10**.
- **B2 ABLATION PASS** — ablate == descent byte-exact (mechanism inert when OFF).
- **B3 CAUSAL FAIL** — shuf 3.08603 ≈ lateral 3.08195: the _l2 geometry the transfer rides is INERT.
- **B4 vs-FLOOR FAIL** — lateral +0.234 above floor.

**TERMINAL TIER (this lens): 🧱 WALL HOLDS (ENGINE-NATIVE).**

## What this means (c9)

Lateral transfer of learned VALUES is essentially inert at scale (+0.006), and on a small
1500-byte slice it actively HURTS (lateral 3.016 vs descent 2.791): distance-weighted averaging of
neighbor value-distributions BLURS each cell's sharp learned local-expert value — the one thing pure
mitosis cells DO have — regressing them toward the mean instead of adding compositional depth.
**Sharing next-byte statistics by AVERAGING is the wrong operator.** 2nd orthogonal engine-native
lens after H_1569: representation re-pooling does not lift split-only mitosis; the missing ingredient
is a LEARNED compositional substrate, not a re-mixing of fixed local experts.

## Honest scope (c9, a_scale_honest_scope)

ENGINE-NATIVE (pure .hexa via core/ §Osmotic) → terminal for THIS lens. TOY scale (12 KB English,
order-2). A different lateral operator (transfer KEYS/split-targets rather than averaging values,
or selective best-neighbor rather than blend) is the UNVERIFIED variant; but averaging-blend is the
natural "horizontal statistics share" and it is inert/harmful. NO CORE wiring (wall).
