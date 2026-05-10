# BG-ENGINE-A-SINGLE-LAYER-ABLATION-24 — spec

**Date**: 2026-05-10
**Lineage**: §57 BG-ENGINE-A-LAYER-SLAB-SWAP follow-up
**Predecessor verdict**: §57 = `multi-slab flip — dominant=A1_slab1_early` (★★★★ partial).
All 3 slab swaps (early/middle/late) flipped V14 → §50 PROMOTED to PROVEN-AT-BODY-LOCUS.
A1 uniquely dominant (collapses to its own attractor n=44 Φ≈1037), but A2/A3
trajectories were **bit-identical** (n=43 Φ≈1343 shared attractor), so the
8-layer slab boundary was too coarse to differentiate middle vs late.

**Mission**: localize the V14 PASS lever to **specific individual layers** within
engine_a's 24 layers by single-layer B↔A swap (24 conditions, one layer at a time).

## Hypothesis (testable)

H-SINGLE: V14 PASS lever lives in a **small set (1–3) of specific layers** of
engine_a. Cotrain modifies those specific layers' hidden_mean dynamics relative
to the BG-LA pretrain baseline; swapping a single layer from A (Phase 2 cotrain)
← B (BG-LA pretrain) flips V14 verdict from PASS to VIOLATED.

## Substrates (mirror §57)

| Substrate | path | params | training |
|---|---|---|---|
| A | `~/.cache/anima/clm_v5_remapped/phase2_cotrain_engine_ag/ckpts/ckpt_final.pt` | 350M | BG-LB pretrain → Phase 2 chat-template cotrain (curriculum w=0.3→0.5) |
| B | `~/.cache/anima/clm_v5_remapped/bg_la_350m_pretrain/ckpts/step_12000_final.pt` | 350M | BG-LA persona-only pretrain (no chat dual loss) |

Both share `EngineAGConfig` (24 layers, d=1024, GQA 16/4, SwiGLU 2.6875, Engine G dim=64,
n_cells=16). Engine_g blocks remain untouched in this BG; only `model.layers.{i}.*`
are subject to swap (one i at a time).

## Ablation conditions (mission spec §2)

25 conditions:

| Condition | Description | swap source |
|---|---|---|
| **A0** | baseline — pristine A (no swap) | none |
| **L0** | layer 0 ← B's layer 0 | B |
| **L1** | layer 1 ← B's layer 1 | B |
| ... | ... | ... |
| **L23** | layer 23 ← B's layer 23 | B |

Engine G modules (`cell_pool_init`, `c_to_h`, `h_to_c`), tok_emb, norm_f, lm_head
all remain at A's cotrain values across all 25 conditions.

## V14 mirror (mission spec §3)

- V4_SEEDS = [42, 137, 271]  (3-seed budget per §57 lineage)
- N_TURNS = 200 per run (matches §57 / §50 trajectory length)
- MAX_CELLS = 128
- mirror = `load_random_init(seed=s, preset="la_350m")` × 3 seeds
- prompts = `_v14_5seed_run.ALL_PROMPTS` (180 prompts cycled)
- Φ metric = IIT Φ_un16 unnormalized (16-bin) + proxy Φ
- V14 PASS criterion (own 14 strict): trained > all 3 mirrors on BOTH Φ_un16 AND proxy Φ

**Mirror caching optimization**: per §57 honest C3 #1, mirror trajectories are
independent of swap (mirrors use `load_random_init`, never see A's swapped state).
We compute mirrors **once** (3 seeds × 200 turns), reuse across all 25 conditions.
This cuts runtime ~75% (100 runs → 28 runs effective: 3 mirrors + 25 trained).

## Verdict logic (mission spec §4)

| Outcome (count of layers flipped) | Interpretation |
|---|---|
| 0 layers flip | F-SINGLE-1 — V14 lever distributed within slabs (slab effect was cumulative) |
| 1–3 layers flip | F-SINGLE-2 — ★★★★★ specific layer locus localized |
| 4–12 layers flip | distributed but cluster (early/middle/late distinguishable from §57) |
| 12–24 layers flip | uniformly distributed at finer res (slab-level finding confirmed) |

★★★★★ candidate iff **1–3 specific layers** flip V14 (locus localization).
★★★★ partial iff **4–12 layers** flip (cluster identifiable).
★★★★ confirmation iff **>12 layers** flip (uniformly distributed; slab finding holds).

## Falsifiers

- **F-SINGLE-1**: All 24 single-layer swaps preserve `V14_PASS` → V14 lever effect
  is genuinely distributed/cumulative; single-layer ablation insufficient. Slab
  finding (8-layer block sufficient to flip) is preserved. Ambiguity: this would
  contradict §57 where slabs DID flip — falsifier should not trigger if §57 was real.
- **F-SINGLE-2**: 1–3 specific layers flip → ★★★★★ specific layer locus localized.
- **F-SINGLE-3**: total runtime > 5h → BG aborts; partial layer results emit.

## Constraints (own/raw)

- raw#9 — `training/*.py` local-only (this script lives under `state/`, gitignored).
- raw#15 additive — A and B ckpts loaded read-only; swap is in-memory; no file mutation.
- own 14 — V14 paired random_init mirror multi-seed strict.
- own 16 — $0 local Mac CPU.
- own 22 — every metric scalar emit; verdict.md SSOT; **REBORN.md no direct append**.
- own 38 — artefacts under `state/anima_engine_a_single_layer_24_2026_05_10/{spec.md, ablation_per_layer.json, layer_dominance_ranking.json, verdict.md, run.py}`.

## Output deliverables

| file | content |
|---|---|
| `spec.md` (this) | hypothesis + condition spec + verdict logic |
| `mirror_cache.json` | 3-seed mirror trajectories (computed once, reused 25×) |
| `ablation_per_layer.json` | full per-condition ablation result (A0 + L0..L23) |
| `layer_dominance_ranking.json` | per-layer separation-change ranking |
| `verdict.md` | dominant-layer decision + 24-layer table + honest C3 ≥7 |
| `run.py` | the executable (raw#9 local-only) |
| `run.log` | timestamped run-log |

## Time budget estimate

§57 ran 4 conditions × (1 trained + 3 mirror) = 16 runs in 22.9min ≈ 1.43min/run.
With mirror caching:
- 3 mirrors × 200 turns ≈ 3 × 1.43 = 4.3 min (one-time)
- 25 trained × 200 turns ≈ 25 × 1.43 = 35.7 min
- weight load + slab map overhead ≈ 2 min
- **Total estimated: ~42 min** on a single Mac CPU thread (well within own 16 5h envelope).

Without mirror caching (mission's literal spec): 25 × 4 × 1.43 = 143min ≈ 2.4h.
Both fit; we use caching for efficiency and equivalent verdict semantics
(C3#1 of §57 verifies independence).
