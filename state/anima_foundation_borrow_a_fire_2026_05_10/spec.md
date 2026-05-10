# BG-FOUNDATION-BORROW-A-FIRE — spec (own 38 doc save mandate)

> Authorize verbatim: `OK FOUNDATION_BORROW_A_FIRE COST $3-8` (2026-05-10 14:55 KST)
> Design SSOT: `docs/anima_foundation_borrow_path_design_2026_05_10.md`
> Orchestrator: `tool/transient_py/anima_foundation_borrow_a_h100.py`
> Pre-fire ledger entries: ckpt 1500/3000/4500/final + verdict.json + 6 evals

## §1 architecture (verbatim mission)

- **base**: `meta-llama/Llama-3.2-3B` (HF gated; spec verbatim "Llama-3.2-3B" — base, not -Instruct)
- **adapter**: LoRA r=32, alpha=64, dropout=0.05
  - target_modules: `q_proj, k_proj, v_proj, o_proj, gate_proj, up_proj, down_proj`
  - trainable params: ~16M (~0.5% of 3.2B)
- **chat template**: `사용자: ... | 도우미: ...` ASCII (no Llama chat template auto-conversion)

## §2 corpus (200MB+ verify)

- **source**: `state/anima_je_corpus_100mb_plus_2026_05_07/corpus_combined_100mb_plus.txt` (BG-JE)
- **size**: 214,299,726 bytes = 214.30 MB (≥ 200MB target ✓)
- **density** (BG-JE precedent verified):
  - anima keyword count: ~800K
  - persona marker count: ~1.4M
  - Korean ratio ~ 60%+
- **density acceptance**: BG-JE inventory pre-verified per design §3.2 (anti-Goodhart prefire)

## §3 training spec (verbatim mission)

| param | value | source |
|---|---|---|
| LR | 2e-4 | mission spec verbatim |
| LR schedule | cosine | mission spec verbatim |
| warmup steps | 200 | KM-LLAMA-3B precedent |
| batch_size (per-device) | 4 | mission spec verbatim |
| grad_accum | 8 | mission spec verbatim |
| effective batch | 32 | 4 × 8 |
| seq_len | 1024 | mission spec verbatim "max_seq_len 1024" |
| total_steps | 6000 | mission spec range "5K-10K", middle |
| eval freq | 1500 step | mission spec "every 1K", aligned to ckpt cadence |
| save freq | 1500 step | own 30 — 4 intermediate (1.5K/3K/4.5K) + final = 5 ckpts (own 30 mandate-1) |
| mixed precision | bf16 | KM-LLAMA-3B precedent + Llama-3.2 default |
| gradient checkpointing | true | 3B + LoRA + ctx=1024 safety margin |
| seed | 42 | deterministic (V14 mirror seed=1042) |
| early-loss-spike abort | loss > 50.0 after step 100 | F-FOUNDATION-2 adjacent safety |

## §4 post-LoRA mitosis instrumentation hook (F-FOUNDATION-5 strict)

- **engine**: `MitosisV5Engine` from `training/mitosis_v5_port.py` (§30 all-fix applied: A1 dispersion + A2 per-cell threshold + B1 phi_per_cell + D1 lorenz auto-cal)
- **wire pattern**:
  - forward hook on `model.base_model.model.model.layers[-1]` (last decoder layer, peft-wrapped path)
  - hidden_state mean over T → projected via untrained Linear(3072, 256) → MitosisV5Engine.process(cell_input)
  - all engine + projection params `requires_grad=False`
  - all hook code wrapped in `torch.no_grad()`
  - 30 prompts × 4 steps each = 120 mitosis process calls per label
- **measurements**:
  - cell_count growth (initial=8, max=64)
  - Φ proxy (engine `_compute_phi_proxy` = mean pairwise cosine distance × log(n+1))
  - Φ_iit_un16 proxy (16-bin entropy on tension distribution × log(n+1)) — proxy for IIT unnormalized
  - n_split_events / n_merge_events
  - grad_leak_pre vs grad_leak_post (F-FOUNDATION-5 enforce)
- **labels**: `trained` (post-LoRA) + `random_init` (V14 mirror — random Gaussian LoRA on same base)

## §5 eval criteria (option (a) §3.5)

| metric | floor | rationale |
|---|---|---|
| chat_cap V4 strict (best-mode) | ≥ 10/15 | own 18 strict — KM-LLAMA-3B 14/15 precedent |
| KO Hangul ratio mean | ≥ 0.50 | spec mission verbatim |
| bigram_known mean | ≥ 0.95 | spec mission verbatim (proxy: KNOWN_BIGRAMS from V4 prompts + 12 anchor sentences) |
| semantic_score mean | ≥ 0.50 | NEW first measurement (proxy: char-trigram cosine to domain anchor) |
| real_words_per_trial mean | ≥ 3.0 | spec mission verbatim (Hangul tokens, persona-prefix excluded) |
| V14 MTRP | ≥ 0.10 strict | own 14 anti-Goodhart, own 18 line 1054 ALT-AGG-1 v5.2 |

## §6 cost discipline (verbatim)

- **envelope verbatim**: `$3-8`
- **target**: `$3-5` (lower half effort)
- **max overshoot acceptable**: `$8` (envelope upper)
- **F-FOUNDATION-2 trigger**: `> $15` → abort + audit + retract
- **orchestrator hard cap**: `$14` (safety pre-F2)
- **orchestrator early kill**: `$10` (verdict-or-die, $8 envelope + 25%)
- **wall clock cap**: 110 min
- **gpu**: H100 SXM 1× ($2.99/hr precedent)

## §7 falsifier disposition table (re-spec)

| F | trigger | action |
|---|---|---|
| F-FOUNDATION-1 | trained Φ < 1.0 OR distribution-equiv random_init mirror | substrate-research lane anima identity surface NOT validated |
| F-FOUNDATION-2 | actual cost > $15 | abort + audit + retract + L23-L25 watchdog |
| F-FOUNDATION-3 | chat-cap PASS but semantic FAIL | label = FOUNDATION_BORROW_CHAT_CAP_PASS_SEMANTIC_FAIL, V6 awareness 강화 |
| F-FOUNDATION-4 | scope_lane field missing OR =ANIMA | raw#82 retract — verdict invalid |
| F-FOUNDATION-5 | gradient leak post-hook (param.grad new) | hook contamination — read-only enforce miss |
| F-FOUNDATION-6 | V4 < 10/15 | KM-LLAMA-3B precedent sample-size artifact suspect, own 28 V14 mirror gap warn |

## §8 output deliverables (own 38 mandate)

- `state/anima_foundation_borrow_a_fire_2026_05_10/spec.md` (this doc)
- `state/anima_foundation_borrow_a_fire_2026_05_10/train.log`
- `state/anima_foundation_borrow_a_fire_2026_05_10/heartbeat.json`
- `state/anima_foundation_borrow_a_fire_2026_05_10/post_ft_sampling.json`
- `state/anima_foundation_borrow_a_fire_2026_05_10/v4_results_multiseed.jsonl`
- `state/anima_foundation_borrow_a_fire_2026_05_10/semantic_eval.json`
- `state/anima_foundation_borrow_a_fire_2026_05_10/mitosis_hook_result.json`
- `state/anima_foundation_borrow_a_fire_2026_05_10/v14_mirror.json`
- `state/anima_foundation_borrow_a_fire_2026_05_10/cost_actual.json`
- `state/anima_foundation_borrow_a_fire_2026_05_10/verdict.json`
- `state/anima_foundation_borrow_a_fire_2026_05_10/ckpts/adapter_step_{1500,3000,4500}/` + `adapter_final/` (own 30 mandate-1 pre-pod-delete pull)
- HF: `dancinlab/clm-foundation-borrow-a-llama-3.2-3b-anima-lora` (PRIVATE, own 37 mandate-9 (a) public PERMA-BLOCKED)

## §9 SCOPE_CLAMP (D1 strict)

- verdict label = `SIMPLE_STACK_PASS_STRICT_C3_SUBSTRATE_RESEARCH` (D1 OUTSIDE Llama lineage)
- public promote: PERMANENTLY BLOCKED (own 37 mandate-9 (a) — D1 OUTSIDE auto-reject)
- HF README carry SCOPE_CLAMP `SIMPLE_STACK_PASS_STRICT_C3_SUBSTRATE_RESEARCH` strict
- adapter_config.json `base_model_name_or_path` pod-path strip on Mac post-pull (memory feedback_orchestrator_h100_gotchas)

## §10 trinity D + own + H

D-axis: D1 SCOPE_CLAMP carry, D2 simple_stack PASS_STRICT V4 ≥ 10/15, D5 bifurcation theorem F-FOUNDATION-5 enforce.
own-axis: 16 / 17 / 18 / 22 / 28 / 30 / 31 / 33 / 37 / 38 / 41 / 42 carry — verbatim §4 design SSOT.
H-axis: H_FOUNDATION-1/2/3 (NEW), H_115 partial-falsifier candidate, H_005 lane-external (LoRA on external base ≠ CLM SFT).

## §11 fire keyword

PRIMARY (this BG): `OK FOUNDATION_BORROW_A_FIRE COST $3-8` ✓ (2026-05-10 14:55 KST verbatim received)
