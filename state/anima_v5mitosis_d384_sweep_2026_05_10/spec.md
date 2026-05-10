# BG-V5MITOSIS-D384-SWEEP — track C cond.3 d=384 V14 mirror (own 38)

## ts
2026-05-10 (cycle 2026-05-10 §37 priority 1)

## Mission
track C cond.3 prereq for cond.5 H100 fire authorize:
- real ckpt at d=384 (NOT d=1024 Phase 2, NOT synthetic random transformer)
- max_cells=128 (cap-bound 회피, §33 max=32 cap-bound 6/6 retest)
- §30 all-fix active: A1 dispersion + A2 per-cell threshold + B1 phi_per_cell + D1 Lorenz auto-cal
- C1 callback STUB (Net2Net momentum copy 미구현, cond.5 prep)
- 1K-3K turn long-trajectory inference
- own 14 V14 mirror: trained vs 5 random_init seeds (strict)
- α V2 metric (log-log slope phi_per_cell vs n_cells)

## d=384 ckpt 결정
**FOUND**: `/Users/ghost/core/anima/state/anima_clm_v2_mitosis_cells_recovery_2026_05_09/cells64_final.pt`
- v2 mitosis cells64 ckpt (R2 download 2026-05-09)
- config: `{dim: 384, layers: 6, heads: 6, block_size: 256, batch_size: 32, steps: 50000, max_cells: 64}`
- params: ~218M (vocab 256 byte-level, 6 transformer blocks d=384)
- mitosis_status snapshot: 64 cells reached, 62 split events, 0 merges (max_cells=64 saturated)
- phi_history len 200 sampled across training, phase=combined

(미션 spec assumed cells64 = d=192, but config field shows dim=384 directly. Spec assumption was wrong; the ckpt IS d=384.)

### v2 → v5 schema delta
v2 ckpt is a **6-layer transformer** with shared tok/pos emb + dual head_a/head_g + 6 stacked
`blocks.{i}.attn / ffn.engine_a / ffn.engine_g / ln1 / ln2`. NOT cells-as-blocks (mitosis tracked
as instrumentation OVER 6 layers).

`mitosis_model_v5.MitosisModelEngine` is a different architecture: cells = transformer blocks
in PARALLEL (not stacked), aggregated via softmax(tension)-weighted readout BEFORE single
shared lm_head.

**Mapping** (maximum-fidelity load via `init_engine_from_v2()`):
- v2 `tok_emb` (256, 384) → engine.tok_emb ✓
- v2 `pos_emb` (256, 384) → engine.pos_emb ✓
- v2 `ln_f` → engine.final_ln ✓
- v2 `head_a` → tied lm_head (via tok_emb sharing — `weight_tied_lm_head=True`)
- v2 `blocks.0..5.{attn, ffn_a, ffn_g, ln1, ln2}` → engine.cells[0..5] (6 of 8 initial cells)
  - attn.c_attn.weight (1152, 384) → cell.attn.qkv.weight (bias dropped — qkv has bias=False)
  - attn.c_proj.weight (384, 384) → cell.attn.out.weight (bias dropped)
  - ffn.engine_a.{0,3} → cell.ffn_a Sequential[0,3] (with bias)
  - ffn.engine_g.{0,3} → cell.ffn_g Sequential[0,3] (with bias)
  - ln1, ln2 weight+bias copied
- engine.cells[6..7] random init (no v2 source)

This satisfies the "real d=384 ckpt" cond.3 spec to the maximum degree the v2-vs-v5 schema delta
allows. 75% of initial cells (6/8) carry trained v2 weights; embeddings + final norm 100% trained.

## Run config
- d_model=384, n_head=6, ffn_dim=1536, max_seq=256, vocab=256
- initial_cells=8, max_cells=128
- §30 all-fix: dispersion ON, per_cell_threshold ON, lorenz_auto_calibrate ON, C1 STUB
- readout_mode=a_minus_g, attention_sharing=auto, weight_tied_lm_head=True
- turns=1000 (own 14 5-seed strict; 3K turn pushed to next cycle if 1K already V14_VIOLATED)
- seeds: trained + [7, 17, 23, 41, 71]
- prompt_seed=2026 (deterministic, mode-shifting every 200 turns)
- iit_every=25, log_every=200

## Falsifier
- F-D384-1: d=384 ckpt 부재 → mission OUT_OF_SCOPE  [PASSED — ckpt found]
- F-D384-2: §30 fix가 d=384에서도 너무 aggressive (max=128 cap-bound) [tested]
- F-D384-3: trained vs random V14 separation 부재 [tested in result]

## raw / own
- raw#9: training/v5mitosis_d384_v14_mirror.py local-only (gitignored)
- raw#10: honest C3 ≥7 — v2→v5 schema delta documented; cells 6,7 random by necessity; ratchet
  + IIT phi port wired; trained ckpt is byte-level (vocab=256), so smoke is byte-pattern not
  KO chat
- raw#15: additive — v2 ckpt + mitosis_model_v5.py + mitosis_v5_port.py untouched
- own 14: V14 mirror 5-seed strict
- own 16: 0-cost ($0 local CPU)
- own 22: REBORN.md 직접 append 안함; dispatcher가 §37 slot에 receive 후 append
- own 38: doc save state/anima_v5mitosis_d384_sweep_2026_05_10/{spec.md, result.json, v14_verdict.md}
