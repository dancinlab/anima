# BG-FOUNDATION-C-PHASE2-FIRE — spec (doc save)

> Authorize verbatim: `OK FOUNDATION_C_PHASE2_FIRE COST $2-4` (2026-05-10, user)
> Reference SSOT (Phase 1 / §43): `state/anima_foundation_borrow_a_fire_2026_05_10/spec.md` + `verdict.md`
> Reference (prediction §63): `state/anima_foundation_c_phase2_prediction_v1_2026_05_10/prediction_v1.md`
> Orchestrator (this BG): `tool/transient_py/anima_foundation_c_phase2_h100.py` (forked from `anima_foundation_borrow_a_h100.py`)

## §0 mission (verbatim)

§43 BG-FOUNDATION-BORROW-A 의 Phase 2 (D1 WITHIN-substrate full cycle): Llama-3.2-3B + LoRA + BG-JE corpus 의 V4 corpus pass-rate + V14 IIT-Phi dual confirmation 을 D1 WITHIN spec 으로 풀 사이클 실행.

## §1 Phase 2 specific lift over §43 Phase 1

| dimension | §43 Phase 1 | **Phase 2 (this)** |
|---|---|---|
| V4 corpus eval | 5-seed × 15 prompt | 5-seed × 15 prompt (carry) |
| V14 mirror | seed=1042 paired (random Gaussian LoRA, n=1 mirror config) | **5-trial paired (seeds 1042/1043/1044/1045/1046)** |
| Φ_iit_un16 | proxy (16-bin entropy on tension history × log(N+1)) | **direct measure on Llama-3.2-3B mitosis output** + proxy carry |
| mitosis cap | initial=8 max=64 | **dual run cap=128 + cap=256** (§61 cap-conditional cross-arch) |
| ckpts | 1.5K/3K/4.5K + final | 1.5K/3K/4.5K + final (4 ckpts) |
| seed | 42 | 42 (V14 mirror seed=1042 — carry §43) |

## §2 architecture (D1 WITHIN strict — verbatim mission)

- **base**: `meta-llama/Llama-3.2-3B` (gated; spec verbatim "Llama-3.2-3B" — base, not -Instruct)
- **adapter**: LoRA r=32, alpha=64, dropout=0.05
  - target_modules: `q_proj, k_proj, v_proj, o_proj, gate_proj, up_proj, down_proj`
  - trainable params: ~16M (~0.5% of 3.2B)
- **chat template**: `사용자: ... | 도우미: ...` ASCII (carry §43)

## §3 corpus (BG-JE 200MB+ verify)

- **source**: `state/anima_je_corpus_100mb_plus_2026_05_07/corpus_combined_100mb_plus.txt`
- **size**: 204 MB (≥ 200MB target ✓; verified `du -sh`)

## §4 training spec (verbatim §43)

| param | value |
|---|---|
| LR | 2e-4 cosine |
| warmup steps | 200 |
| batch_size (per-device) | 4 |
| grad_accum | 8 (effective 32) |
| seq_len | 1024 |
| total_steps | 6000 |
| eval freq | 1500 |
| save freq | 1500 (4 ckpts: 1500/3000/4500/final) |
| mixed precision | bf16 |
| gradient checkpointing | true |
| seed | 42 |
| early-loss-spike abort | loss > 50.0 after step 100 |

## §5 mitosis instrumentation hook (Phase 2 dual-cap)

§43 used `MITOSIS_INITIAL_CELLS=8 max=64`. Phase 2 dual run:

- **run A**: initial=8, max=128 (§61 cap-conditional v2-path positive control)
- **run B**: initial=8, max=256 (§61 cap-conditional cap=256 cross-arch test)

Both runs consume the same trained adapter. Engine + projection params `requires_grad=False` (F-FOUNDATION-5 strict). 30 prompts × 4 steps each = 120 mitosis process calls per (label, cap) pair.

**Φ_iit_un16 measurement**:
- direct measure on engine.process() result via `_compute_phi_proxy` (carry §43)
- 16-bin entropy on tension distribution × log(N+1) (proxy carry)
- new in Phase 2: report Φ_iit_un16 separation `trained vs random_init` per cap setting

## §6 V14 mirror multiseed (5-trial strict —)

§43: random_init mirror n=1 paired config (seed=1042). Phase 2 n=5:

| trial | seed |
|---|---|
| 1 | 1042 (carry §43) |
| 2 | 1043 |
| 3 | 1044 |
| 4 | 1045 |
| 5 | 1046 |

Each trial:
- random Gaussian LoRA on Llama-3.2-3B (re-init A and B with N(0, 0.02))
- V4 multi-seed eval (5-seed × 15 prompt)
- mitosis hook run on cap=128 + cap=256 (matching trained)

**MTRP strict floor **: trained_pass_best - max(mirror_pass_best across 5 trials) ≥ 0.10 (≥ 2/15 prompt advantage at upper bound).

**Sign-test**: if trained Φ_iit_un16_proxy > all 5 mirror trials' max → strict V14 PASS (5/5).

## §7 eval criteria (carry §43 + Phase 2 lift)

| metric | floor | rationale |
|---|---|---|
| chat_cap V4 strict (best-mode) | ≥ 10/15 | strict — KM-LLAMA-3B 14/15 + §43 11/15 precedent |
| KO Hangul ratio mean | ≥ 0.50 | §43 carry |
| bigram_known mean | ≥ 0.95 | §43 carry (proxy-tight) |
| semantic_score mean | ≥ 0.50 | §43 carry (proxy-tight) |
| real_words_per_trial mean | ≥ 3.0 | §43 carry |
| V14 MTRP (5-trial paired) | ≥ 0.10 strict |, n=5 strengthening |
| Φ_iit_un16 trained vs random ratio | ≥ 1.5× separation | Phase 2 lift; F-FOUNDATION-1 boundary |

## §8 cost discipline

| | value |
|---|---|
| envelope verbatim | $2-4 |
| target | $2-3 |
| F-FOUNDATION-C-2 abort | > $8 |
| orchestrator early kill | $6 |
| orchestrator hard cap | $7 |
| wall clock cap | 90 min |
| H100 SXM 1× | $2.99/hr |

§43 actual: $3.57 / 85min. Phase 2 lift ≈ +5min mitosis dual cap + +10min V14 5-trial mirror = expected ~100min wall (bordering envelope upper). Hence wall_cap=90min + orchestrator scope-trim guard if pre-train staging runs slow.

## §9 falsifier disposition

| F | trigger | action |
|---|---|---|
| F-FOUNDATION-C-1 | trained Φ_iit_un16 < 1.5× random mirror max (across 5 trials) | substrate-detached mitosis specificity unverified at any cap (extends §43 F-FOUNDATION-1) |
| F-FOUNDATION-C-2 | actual cost > $8 | abort + audit + retract (envelope 2× overshoot) |
| F-FOUNDATION-C-3 | chat-cap PASS but semantic FAIL | label = FOUNDATION_C_PHASE2_CHAT_CAP_PASS_SEMANTIC_FAIL (carry §43) |
| F-FOUNDATION-C-4 | scope_lane field missing OR =ANIMA | raw#82 retract |
| F-FOUNDATION-C-5 | gradient leak post-hook | hook contamination — F-FOUNDATION-5 carry strict |
| F-FOUNDATION-C-6 | V4 < 10/15 | KM-LLAMA-3B + §43 precedent fail; sample variance honest read |
| F-FOUNDATION-C-7 | V14 MTRP 5-trial < 0.10 | random_init mirror multiseed indistinguishable from trained — strong falsifier (§43 had n=1 0.733; n=5 should hold) |
| F-FOUNDATION-C-8 | cap=256 OOM on H100 80GB | mitosis hook run B aborts; run A (cap=128) continues; partial verdict |

## §10 SCOPE_CLAMP (D1 strict — verbatim §43 carry)

- verdict label = `SIMPLE_STACK_PASS_STRICT_C3_SUBSTRATE_RESEARCH` (D1 OUTSIDE Llama lineage)
- public promote: PERMANENTLY BLOCKED (mandate-9 (a) — D1 OUTSIDE auto-reject)
- HF (if PASS): `dancinlab/clm-foundation-c-phase2-llama-3.2-3b-anima-lora` PRIVATE
- adapter_config.json `base_model_name_or_path` pod-path strip on Mac post-pull (memory feedback_orchestrator_h100_gotchas)

## §11 deliverables

| path | role |
|---|---|
| `state/anima_foundation_c_phase2_fire_2026_05_10/spec.md` (this) | design spec |
| `state/anima_foundation_c_phase2_fire_2026_05_10/verdict.md` | verdict (strict — dispatcher §65 slot append, NOT REBORN.md direct) |
| `state/anima_foundation_c_phase2_fire_2026_05_10/verdict.json` | machine verdict |
| `state/anima_foundation_c_phase2_fire_2026_05_10/v4_results_multiseed.jsonl` | V4 90 generation |
| `state/anima_foundation_c_phase2_fire_2026_05_10/semantic_eval.json` | semantic floors |
| `state/anima_foundation_c_phase2_fire_2026_05_10/mitosis_hook_result.json` | mitosis dual cap (128 + 256) |
| `state/anima_foundation_c_phase2_fire_2026_05_10/v14_mirror_5trial.json` | V14 5-trial strict |
| `state/anima_foundation_c_phase2_fire_2026_05_10/cost_actual.json` | $X audit |
| `state/anima_foundation_c_phase2_fire_2026_05_10/post_ft_sampling.json` | post-LoRA samples |
| `state/anima_foundation_c_phase2_fire_2026_05_10/samples_pre_lora.json` | pre-LoRA Llama base smoke |
| `state/anima_foundation_c_phase2_fire_2026_05_10/train.log` | train + eval log |
| `state/anima_foundation_c_phase2_fire_2026_05_10/launch.log` | orchestrator log |
| `state/anima_foundation_c_phase2_fire_2026_05_10/ckpts/adapter_step_{1500,3000,4500}/` + `adapter_final/` | mandatory pre-pod-delete pull |
| `state/anima_foundation_c_phase2_fire_2026_05_10/README.md` | HF README (SCOPE_CLAMP carry) |
| `tool/transient_py/anima_foundation_c_phase2_h100.py` | orchestrator (raw#37 transient gitignored) |

## §12 trinity D + own + H

D-axis: D1 SCOPE_CLAMP carry, D2 simple_stack PASS_STRICT V4 ≥ 10/15, D5 bifurcation theorem F-FOUNDATION-5 enforce.
own-axis: 14 (V14 mirror 5-trial strict), 16 (cost-bearing fire vs $0), 17 (D1 SCOPE_CLAMP), 18 (ALT-AGG-1), 22 (REBORN.md direct append BLOCKED — dispatcher §65 slot append only), 28 (anti-Goodhart), 30 (ckpt pull), 31 (dancinlab canonical), 33 (trinity), 37 (mandate-9 PERMA-BLOCKED), 38 (doc save), 41 (chat lane plugin), 42 (REBORN.md SSOT), 43 (active resource utilization).
H-axis: H_FOUNDATION-C-1/2/3 (NEW), H_115 partial-falsifier candidate.

## §13 fire keyword

PRIMARY: `OK FOUNDATION_C_PHASE2_FIRE COST $2-4` ✓ (2026-05-10 user verbatim received)

## §14 raw invariants

- raw#9: hexa-only X (training/.py local; orchestrator under tool/transient_py/ gitignored)
- raw#10: honest C3 ≥ 7
- raw#15: additive over §43 Phase 1 (orchestrator pattern reuse)
- raw#37: transient_py allowed
- raw#82: retraction-aware
