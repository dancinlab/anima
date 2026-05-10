# BG-ENGINE-A-LAYER-SLAB-SWAP — spec

**Date**: 2026-05-10
**Lineage**: §50 BG-COTRAIN-EXERCISE-CAUSAL-PROOF refined-hypothesis follow-up
**Predecessor verdict**: §50 = `CORRELATIONAL` — engine_g.{cell_pool, c_to_h, h_to_c}
ablation FALSIFIED F2; refined post-hoc hypothesis = engine_a (24-layer transformer body)
is the cotrain-exercised V14 PASS lever.
**Mission**: localize the V14 PASS lever within engine_a's 24 layers by slab-level
B↔A swap (3 slabs × 8 layers each).

## Hypothesis (testable)

H-SLAB: V14 PASS lever lives in a **specific layer slab** of engine_a (early /
middle / late). Cotrain modifies that slab's hidden_mean dynamics relative to
the BG-LA pretrain baseline; swapping that slab from A (Phase 2 cotrain) ←
B (BG-LA pretrain) flips V14 verdict from PASS to VIOLATED.

## Substrates

| Substrate | path | params | training |
|---|---|---|---|
| A | `~/.cache/anima/clm_v5_remapped/phase2_cotrain_engine_ag/ckpts/ckpt_final.pt` | 350M | BG-LB pretrain → Phase 2 chat-template cotrain (curriculum w=0.3→0.5) |
| B | `~/.cache/anima/clm_v5_remapped/bg_la_350m_pretrain/ckpts/step_12000_final.pt` | 350M | BG-LA persona-only pretrain (no chat dual loss) |

Both share `EngineAGConfig` (24 layers, d=1024, GQA 16/4, SwiGLU 2.6875, Engine G dim=64,
n_cells=16). Engine_g blocks remain untouched in this BG; only `model.layers.{i}.*`
are subject to swap.

## Slab grouping (mission spec §1)

24 layers split into 3 contiguous slabs of 8 layers each:

| Slab | Layer range | Role | Approx params/slab |
|---|---|---|---|
| **slab1** (early) | layers 0–7  | embedding-near; token-shape and low-level statistics | ~12.7M × 8 ≈ 102M |
| **slab2** (middle) | layers 8–15 | mid-depth; abstract feature mixing | ~12.7M × 8 ≈ 102M |
| **slab3** (late) | layers 16–23 | output-near; vocab-projection conditioning | ~12.7M × 8 ≈ 102M |

Per-layer tensor breakdown (`EngineABlock`):
- `norm1.weight` (1024,)
- `attn.q_proj.weight` (1024, 1024)
- `attn.k_proj.weight` (256, 1024)  ← n_kv_heads=4 × d_head=64
- `attn.v_proj.weight` (256, 1024)
- `attn.o_proj.weight` (1024, 1024)
- `norm2.weight` (1024,)
- `ffn.gate.weight` (2752, 1024)
- `ffn.up.weight`   (2752, 1024)
- `ffn.down.weight` (1024, 2752)

(See `slab_mapping.json` for the exhaustive parameter mapping.)

## Ablation conditions (mission spec §2)

| Condition | Description | swap source |
|---|---|---|
| **A0** | baseline — pristine A (no swap) | none |
| **A1** | layers 0–7 ← B's layers 0–7 | B (BG-LA pretrain) |
| **A2** | layers 8–15 ← B's layers 8–15 | B (BG-LA pretrain) |
| **A3** | layers 16–23 ← B's layers 16–23 | B (BG-LA pretrain) |

Engine G modules (`cell_pool_init`, `c_to_h`, `h_to_c`), tok_emb, norm_f, lm_head
all remain at A's cotrain values across all 4 conditions.

## V14 mirror (mission spec §3)

- V4_SEEDS = [42, 137, 271]  (3-seed budget per §50 lineage)
- N_TURNS = 200 per run  (within own 16 ~5h envelope)
- MAX_CELLS = 128
- mirror = `load_random_init(seed=s, preset="la_350m")` × 3 seeds
- prompts = `_v14_5seed_run.ALL_PROMPTS` (180 prompts cycled by `turn % len`)
- Φ metric = IIT Φ_un16 unnormalized (16-bin) + proxy Φ
- V14 PASS criterion (own 14 strict): trained > all 3 mirrors on BOTH Φ_un16 AND proxy Φ

## Verdict logic (mission spec §4)

| Outcome | Interpretation |
|---|---|
| All 3 swaps still PASS | F-SLAB-1 — V14 lever distributed across 24 layers (no specific slab signature) |
| Only A1 → VIOLATED | F-SLAB-2 — early-layer specific (embedding-near; tokenization-shape) |
| Only A2 → VIOLATED | middle-layer specific (mid-depth abstract features) |
| Only A3 → VIOLATED | late-layer specific (output-near; vocab projection) |
| Mixed (multiple → VIOLATED) | dominant-slab decision via Φ_un16 separation magnitude |

★★★★★ candidate iff a **single slab** flips V14 (locus localization).
★★★★ partial credit iff distributed (refined hypothesis preserved at body-level
but not at slab-level).

## Falsifiers

- **F-SLAB-1**: All 3 swaps preserve `V14_PASS` → V14 lever is distributed across
  all 24 layers. Refined-hypothesis preserved (engine_a body) but slab-level
  localization absent. ★★★★ partial.
- **F-SLAB-2**: A1 (early) flips to VIOLATED while A2/A3 preserve PASS → early-layer
  signature dominant. ★★★★★ candidate.
- **F-SLAB-3**: total runtime > 5h → BG aborts; partial slab results emit.

## Constraints (own/raw)

- raw#9 — `training/*.py` local-only (this script lives under `state/`, gitignored).
- raw#15 additive — A and B ckpts loaded read-only; swap is in-memory `state_dict()`-based mutation; no ckpt files modified.
- own 14 — V14 paired random_init mirror with multi-seed strict.
- own 16 — $0 local Mac CPU.
- own 22 — every metric scalar emit; verdict.md SSOT.
- own 38 — artefacts under `state/anima_engine_a_layer_slab_swap_2026_05_10/{spec.md, slab_mapping.json, ablation_per_slab.json, verdict.md}`.

## Output deliverables

| file | content |
|---|---|
| `spec.md` (this) | hypothesis + slab spec + verdict logic |
| `slab_mapping.json` | per-slab tensor key list + param-count breakdown |
| `ablation_per_slab.json` | full per-condition ablation result (A0/A1/A2/A3) |
| `verdict.md` | dominant-slab decision + honest C3 ≥7 |
| `run.py` | the executable (raw#9 local-only) |
| `run.log` | timestamped run-log |

## Time budget estimate

- 4 conditions × 1 trained run × 200 turns ≈ 4 × ~120s = 8 min trained
- 4 conditions × 3 mirrors × 200 turns ≈ 4 × 3 × ~120s = 24 min mirror
- 1× weight-load overhead (A + B + 3 random) ≈ 90s
- ckpt clone + slab-swap × 3 ≈ negligible
- **Total estimated: ~35 min** on a single Mac CPU thread (well within own 16
  $0 envelope; 200 turns is the §50 trajectory length, not 1000-turn full).
