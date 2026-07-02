---
id: H_1569
slug: 1569_pretrained_mitosis_split
title: PRETRAINED / INHERITED-REPRESENTATION mitosis split (H_1310 wall-break lens 3 — the user's core insight)
group: MITOSIS-ENGINE (H_1310 from-scratch ceiling — wall-break campaign, lens 3 of 3+)
tier: 🧱 WALL HOLDS (ENGINE-NATIVE) — B1 BREAK FAIL at frozen scale (B2∧B3 PASS, B4 FAIL)
verdict_dir: state/verdicts/1569_pretrained_mitosis_split/
date: 2026-06-23
wired: engine-native (pure .hexa via core/engine_cli.hexa §Osmotic; no wiring — RED/wall, a_verified_must_wire fires only on GREEN)
---

# H_1569 — inherited-representation mitosis split (H_1310 lens 3)

## Claim / falsifier

H_1310 🔴 / H_1568 🧱: from-scratch pure-mitosis split-only learning hits a LOCAL-EXPERT CEILING
above the n-gram floor because the cells partition a **fixed, lossy** feature. H_1568 (lens 1,
selection-driven evolution) pinned the bottleneck as the **representation**, not the growth rule.

**The user's core insight (lens 3, top priority):** do NOT grow from scratch over a lossy feature
— split mitosis cells over an **inherited representation** (as a pretrained model supplies), so
each daughter cell *inherits* a rich representation and specializes ("adult stem-cell division").

**Falsifier:** if giving the cells an inherited richer representation to partition lifts held-out
next-byte CE below the lossy ceiling (by ≥0.10 nats), the H_1310 wall narrows to "from-scratch
lossy-feature only." If it does not, a fixed inherited representation is insufficient (honest 🧱).

## Method (ENGINE-NATIVE — pure .hexa via core/, HARD-GATE-1 PASS)

`state/1569_pretrained_mitosis_split/h1569_pretrained_split_probe.hexa` calls the LIVE engine's
own next-byte MITOSIS LEARNER = **OsmoticStore** (`core/engine_cli.hexa §Osmotic`): a VAdaptField
key store (the engine's OWN `_vnearest_idx`/`_l2` split geometry + `engine_mitosis_tick` clonal
growth under `EngineConfig.mitosis` ON) + a parallel per-cell value table. `osmotic_learn(...)` IS
the live mitosis split. **NO numpy / torch / gauge_lib / .py mirror** (grep over `state/<slug>/*.py`
= EMPTY — no .py files at all). $0 CPU summer pool, hexa v0.262.0. Corpus = `/usr/share/dict/words`
lowercased a-z+space, `head -c 12000`, order-2 context → next symbol, 80/20 train/test (V=27).

**The ONE contrast** (all else byte-identical — value, corpus, split mechanism, cfg.mitosis, cap,
test set, CE metric): the KEY representation the cells partition.
- **A_lossy** = order-2 symbol pair → DIM=8 collinear lossy key (the H_1310 lossy feature).
- **A_repr** = `immune_embed_key(context)` DIM=64 inherited trigram-FNV representation (the engine's
  OWN high-separability encoder — the representation a pretrained trunk would hand the cells).
- **A_rand** = per-context random unit key (representation DESTROYED — B2 ablation).
- **A_shuf** = `immune_embed_key` of a DIFFERENT (permuted) context (binding broken — B3 causal).

Metric: held-out next-byte CROSS-ENTROPY (nats, p7). Comparator: exact order-2 add-1 Markov FLOOR.

## Frozen 5-bar (set BEFORE the run — c9, NO tune-to-green; verdict = 🟢 iff B1∧B2∧B3)

- **B1 WALL-BREAK** CE_repr < CE_lossy − 0.10
- **B2 ABLATION** CE_rand ≥ CE_repr + 0.10
- **B3 CAUSAL** CE_shuf ≥ CE_repr + 0.10
- **B4 vs-FLOOR** CE_repr ≤ CE_floor + 0.02 [report+gate]
- **B5 CONTROL** cells_repr vs cells_lossy [report-only]

## Verdict (read VERBATIM from state/verdicts/1569_pretrained_mitosis_split/H_1569_R1_ENGINE_NATIVE.txt)

Held-out next-byte CE (nats), 12000-byte corpus:

| arm | CE | cells |
|---|---|---|
| A_lossy (H_1310 ceiling) | 3.14342 | 6 |
| A_repr (inherited repr) | **3.08782** | 64 |
| A_rand (B2 ablation) | 3.29311 | — |
| A_shuf (B3 causal) | 3.30044 | — |
| n-gram FLOOR | 2.84769 | — |

- **B1 WALL-BREAK FAIL** — repr 3.08782 vs lossy−0.10 = 3.04342 → repr beats lossy by only
  **+0.0556 nats, UNDER the 0.10 bar**. (NOT broken.)
- **B2 ABLATION PASS** — rand 3.29311 ≥ repr+0.10 (3.18782): destroying the representation
  collapses the repr arm by +0.205 nats.
- **B3 CAUSAL PASS** — shuf 3.30044 ≥ repr+0.10: shuffling the key→context binding collapses it.
- **B4 vs-FLOOR FAIL** — repr 3.08782 vs floor+0.02 (2.86769): repr sits **+0.240 above the floor**
  (lossy was +0.296). The inherited representation NARROWS the gap to the floor but does not reach it.
- **B5** — cells: lossy 6, repr 64 (lossy collinear keys rarely exceed SPLIT_THRESH → ceiling).

**TERMINAL TIER (this lens): 🧱 WALL HOLDS (ENGINE-NATIVE)** — B1 FAIL.

> SCALE NOTE (a_toy_scale_recheck): on a small 1500-byte slice the SAME probe returned 🟢 GREEN
> (B1 PASS: repr 2.791 vs lossy 3.026, gap 0.235). At the full 12000-byte frozen scale the gap
> COLLAPSES to +0.056 < 0.10 → 🧱. The small-scale GREEN was a scale artifact (precedent
> h1464 mirror→engine flip). The 0.10 bar was frozen BEFORE either run and NOT moved (c9).

## What this means (the c9 finding — load-bearing)

Representation **does** matter (B2 ablation + B3 causal both PASS decisively — destroying or
shuffling it collapses the arm by ~0.21 nats; and repr grows 64 cells vs lossy's 6). The inherited
representation lifts mitosis a little off the lossy ceiling (gap-to-floor 0.296 → 0.240). **But the
lift (+0.056) is under the break bar because the inherited representation is still a FIXED feature
the cells partition — not a LEARNED / task-adapted one — and the trigram-FNV keys saturate the L2
split trigger at 64 cells (max_cells=512 unused), so the cells cannot tile finer.** A fixed richer
feature relocates the ceiling slightly; it does not cross it.

**The H_1310 wall is NOT yet narrowed to "from-scratch lossy only."** Single lens ≠ confident
terminal (c16). This result SHARPENS the next orthogonal lens: the representation must be
**learnable / expandable** (grow WITH the cells), not merely inherited-and-fixed → lens 2
(H_1570 lateral gene transfer — cells SHARE learned next-byte statistics) and lens 4
(H_1571 curriculum-staged split).

## Honest scope (c9, a_scale_honest_scope, a_toy_scale_recheck)

ENGINE-NATIVE (pure .hexa via core/ §Osmotic) → terminal PERMITTED for THIS lens. TOY scale (12 KB
English, order-2 context, V=27, single deterministic pass). The "inherited representation" is the
engine's hand-crafted trigram-FNV encoder, NOT a corpus-LEARNED trunk hidden state — testing a true
learned-trunk key (e.g. a 303M chat ckpt's context embedding) is the UNVERIFIED next rung if lens 2/4
also wall. NO CORE wiring (a_verified_must_wire fires only on GREEN; this is a wall).
