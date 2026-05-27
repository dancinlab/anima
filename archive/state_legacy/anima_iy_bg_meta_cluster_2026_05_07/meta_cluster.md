# BG-IY-meta — 22+ BG root-cause meta-cluster (B33)

- ledger rows: 48
- root cause buckets: 16

## Root-cause distribution (root only)

| root_cause | count | lever |
|---|---|---|
| pending | 9 | spec or fire — no analysis until evidence |
| unclassified | 7 | manual review needed |
| partial_signal | 6 | stabilize via B25 ckpt avg + B7 best-of-N ranker — already at frontier; need con |
| emergence_below_threshold | 4 | Stage1 foundation-borrow + Stage2 synthetic 1M dialogue (B16) — params×tokens bo |
| capacity_ceiling | 4 | Stage1 foundation-borrow (LoRA on Polyglot-Ko-1.3B+) — params gap is the binding |
| tooling | 4 | tooling investment; pair with model-side BG to convert to evidence |
| output_head_bottleneck | 3 | B12 MoE expert head OR B5 logit distillation from large teacher |
| persona_cycle_collapse | 2 | B19 persona-dropout-during-train (50% prefix-stripped) + B25 bifurcation-aware c |
| evaluator_strict | 2 | B30 calibration probe (BG-IY) → V_n self-impossibility 검증 |
| sft_recipe | 1 | B20 DPO on PASS/FAIL pair OR B21 KTO on V4 cell labels |
| training_dynamics | 1 | B25 SWA/EMA weight averaging across peak-then-collapse window + Lesson G best-ev |
| superseded | 1 | no follow-up; supersede chain already closed |
| seed_variance | 1 | N≥5 seed sweep before any conclusion; single-seed signal not actionable |
| scale_corpus_mismatch | 1 | rebuild corpus to params×20 ratio per Chinchilla; cheapest = 100M×100MB+ cell |
| synthesis | 1 | doc-only; pair with experimental BG to test recommendations |
| evaluator_axis_landed | 1 | evaluator validated; pivot to model-side training |

## Detailed sub-clusters

### pending / unfired_or_in_flight (n=9)
**Lever**: spec or fire — no analysis until evidence

| BG | attempt | paradigm | capacity | corpus_mb | final_class |
|---|---|---|---|---|---|
| BG-HU | 13 | combined-paradigm-r1-plus-d | PENDING |  | PENDING |
| BG-HR | 14 | capacity-scaling-100m-byte-level | 100M | 30.02 | PENDING (context cut) |
| BG-HV | 15 | nexus-4411-reality-map-ingest |  |  | PENDING (corpus assembly only) |
| BG-HW | 16 | outside-well-anchored-universe-brain-map | 18M |  | PENDING |
| BG-HX | 17 | ouroboros-cycle-automation-spec |  |  | PENDING (spec only) |
| BG-HZ | 19 | bg-hq-step500-ckpts-retrieve-v3-strict | 33.73M | 30.02 | PENDING |
| BG-IB | 21 | capacity-scaling-50m-intermediate | 50M | 30.02 | PENDING |
| BG-IC | 22 | v3-evaluator-dedicated-impl-retroeval |  |  | PENDING (spec + impl) |
| BG-ID | 23 | bg-hs-r1-replicate-early-stopping-mac-mp | 18M | 21.56 | PENDING |

### partial_signal / pass_class (n=5)
**Lever**: stabilize via B25 ckpt avg + B7 best-of-N ranker — already at frontier; need consistency lever

| BG | attempt | paradigm | capacity | corpus_mb | final_class |
|---|---|---|---|---|---|
| BG-FU | 1 | pre-train-only-tiny | 3M | 52.8 | PARTIAL_PASS_HANGUL_BUT_NOT_COHERENT |
| BG-FY | 2 | pre-train-only-corpus-ko-heavy | 18M | 246.7 | PARTIAL_PASS_NO_CONTEXT |
| BG-HA | 4 | pre-train-only-chat-template-30 | 18M | 236.96 | PARTIAL_PASS_NO_CONTEXT_v2 |
| BG-IS | 29 | v3-retroeval-extension |  |  | V3_RETROEVAL_EXTENSION_LANDED_NO_PASS_SURFACED_BG_HU_DOWNGRA |
| BG-JY | 46 | chat-template-explicit-multi-turn-corpus |  | 91.0 | CORPUS_BUILD_PASS |

### tooling / eval_or_validator_landed (n=4)
**Lever**: tooling investment; pair with model-side BG to convert to evidence

| BG | attempt | paradigm | capacity | corpus_mb | final_class |
|---|---|---|---|---|---|
| BG-IJ | 28 | v3-strict-evaluator-standalone-retry-bg- |  |  | V3_EVALUATOR_LANDED_8BG_RETROEVAL_VALIDATED |
| BG-IW | 33 | ledger-validator-fu-1234-fix |  |  | TOOLING_LEDGER_VALIDATOR_FIX_LANDED |
| BG-JF | 34 | v4-eval-tool-with-embedding-sim-and-less |  |  | V4_EVALUATOR_LANDED_18BG_RETROEVAL_VALIDATED |
| BG-JM | 38 | v5-evaluator-english-baseline-multi-turn |  |  | V5_EVALUATOR_LANDED_20BG_RETROEVAL_3CKPT_MULTI_TURN_VALIDATE |

### emergence_below_threshold / generic_fail (n=3)
**Lever**: Stage1 foundation-borrow + Stage2 synthetic 1M dialogue (B16) — params×tokens both insufficient

| BG | attempt | paradigm | capacity | corpus_mb | final_class |
|---|---|---|---|---|---|
| BG-FK (clm_v2_base) | 3 | pre-train-only-clm-v2-federated | 27.84M |  | SIMPLE_STACK_FAIL |
| BG-HT | 12 | universe-brain-map-self-knowledge-reduce | 27.78M | 6.48 | FAILED (degenerate filler collapse) |
| BG-JU | None | 500m-h100-capacity-1-order-jump-ubm-22mb | 500M | 22.645 | V5_FAIL |

### capacity_ceiling / 18m_byte_level (n=3)
**Lever**: Stage1 foundation-borrow (LoRA on Polyglot-Ko-1.3B+) — params gap is the binding constraint

| BG | attempt | paradigm | capacity | corpus_mb | final_class |
|---|---|---|---|---|---|
| BG-HJ | 6 | two-stage-loss-masked | 18M | 51.47 | FAILED |
| BG-IM | 32 | 18m-nexus-ubm-combined-corpus-byte-level | 18M | 27.575 | FAILED |
| BG-JK | 39 | 18m-curriculum-3stage-kowiki-bg-je-ubm | 18M |  | V4_FAIL_BUDGET |

### output_head_bottleneck / lmhead_insufficient (n=3)
**Lever**: B12 MoE expert head OR B5 logit distillation from large teacher

| BG | attempt | paradigm | capacity | corpus_mb | final_class |
|---|---|---|---|---|---|
| BG-JP | 42 | decoding-sweep-v58-multi-turn-bg-jd-ckpt |  |  | ARCHITECTURAL_OUTPUT_BOTTLENECK_DEEP |
| BG-JT | 43 | lm-head-only-finetune-bg-jd-mac-mps |  | 22.65 | OUTPUT_BOTTLENECK_DEEP_LMHEAD_INSUFFICIENT |
| BG-JS | 43 | lm-head-only-finetune-bg-jd-output-bottl |  | 22.65 | OUTPUT_BOTTLENECK_DEEP_LMHEAD_INSUFFICIENT |

### persona_cycle_collapse / prefix_overamplified (n=2)
**Lever**: B19 persona-dropout-during-train (50% prefix-stripped) + B25 bifurcation-aware ckpt avg

| BG | attempt | paradigm | capacity | corpus_mb | final_class |
|---|---|---|---|---|---|
| BG-HK | 7 | persona-conditioned-chat-template-80 | 27.79M | 30.02 | FAILED |
| BG-IA | 20 | early-stopping-val-loss-18m-persona-less | 18M | 30.02 | FAILED (early-stop triggered step 1200, peak step 600 compos |

### evaluator_strict / v2_v3_false_pass_caught (n=2)
**Lever**: B30 calibration probe (BG-IY) → V_n self-impossibility 검증

| BG | attempt | paradigm | capacity | corpus_mb | final_class |
|---|---|---|---|---|---|
| BG-HQ | 10 | bpe-8k-tokenizer-shift | 33.73M (with BPE) | 30.02 | FAILED (V2 surface metric false PASS — V3 needed) |
| BG-JW | 43 | 20bg-cumulative-negative-archive-final |  |  | 20BG_TOKEN_CHAT_SURFACE_PARADIGM_FINAL_NEGATIVE_ARCHIVE_LAND |

### sft_recipe / sft_only_insufficient (n=1)
**Lever**: B20 DPO on PASS/FAIL pair OR B21 KTO on V4 cell labels

| BG | attempt | paradigm | capacity | corpus_mb | final_class |
|---|---|---|---|---|---|
| BG-HF | 5 | sft-only-loss-unmasked | 27.79M | 51.47 | FAILED |

### capacity_ceiling / 18m_falsified (n=1)
**Lever**: Stage1 foundation-borrow (LoRA on Polyglot-Ko-1.3B+) — params gap is the binding constraint

| BG | attempt | paradigm | capacity | corpus_mb | final_class |
|---|---|---|---|---|---|
| BG-HL | 8 | in-context-few-shot-bg-ha | 18M |  | FALSIFIED at 18M |

### training_dynamics / peak_then_collapse (n=1)
**Lever**: B25 SWA/EMA weight averaging across peak-then-collapse window + Lesson G best-eval ckpt

| BG | attempt | paradigm | capacity | corpus_mb | final_class |
|---|---|---|---|---|---|
| BG-HP | 9 | curated-qa-dense-aug | 18M | 2.41 | FAILED (peak-then-collapse) |

### unclassified / WEAK_PARTIAL ★ (n=1)
**Lever**: manual review needed

| BG | attempt | paradigm | capacity | corpus_mb | final_class |
|---|---|---|---|---|---|
| BG-HS R1 | 11 | universe-brain-map-self-knowledge | 18M | 21.56 | WEAK_PARTIAL ★ |

### unclassified / BLOCKED_CKPT_NEVER_PERSISTED (n=1)
**Lever**: manual review needed

| BG | attempt | paradigm | capacity | corpus_mb | final_class |
|---|---|---|---|---|---|
| BG-HY | 18 | bg-hp-step500-ckpt-retrieve-v3-strict | 18M | 2.41 | BLOCKED_CKPT_NEVER_PERSISTED |

### superseded / stream_or_namespace_failure (n=1)
**Lever**: no follow-up; supersede chain already closed

| BG | attempt | paradigm | capacity | corpus_mb | final_class |
|---|---|---|---|---|---|
| BG-IA | 20 | early-stopping-val-loss-18m-persona | 18M | 30.02 | SUPERSEDED |

### seed_variance / single_seed_lucky_unreplicated (n=1)
**Lever**: N≥5 seed sweep before any conclusion; single-seed signal not actionable

| BG | attempt | paradigm | capacity | corpus_mb | final_class |
|---|---|---|---|---|---|
| BG-IE | 24 | bg-hp-rerun-with-save-at-seed-pin-lesson | 18M | 2.41 | SEED_LUCK_FAIL |

### scale_corpus_mismatch / big_model_small_corpus (n=1)
**Lever**: rebuild corpus to params×20 ratio per Chinchilla; cheapest = 100M×100MB+ cell

| BG | attempt | paradigm | capacity | corpus_mb | final_class |
|---|---|---|---|---|---|
| BG-IF | 25 | 100m-capacity-x-universe-brain-map-corpu | 100M_target_153M_actual | 6.48 | FAILED (CAPACITY_NOT_SUFFICIENT vs 18M UBM baseline) |

### unclassified / CORPUS_READY (TRAINING-READY=TRUE; DOWNSTREAM BG SEQUENTIAL) (n=1)
**Lever**: manual review needed

| BG | attempt | paradigm | capacity | corpus_mb | final_class |
|---|---|---|---|---|---|
| BG-IK | 24 | nexus-ubm-combined-corpus-assembly |  | 27.575 | CORPUS_READY (training-ready=True; downstream BG sequential) |

### unclassified / WEAK_PARTIAL_LIKE_BG-HS_R1 (n=1)
**Lever**: manual review needed

| BG | attempt | paradigm | capacity | corpus_mb | final_class |
|---|---|---|---|---|---|
| BG-IG | 27 | bpe-16k-vocab-ablation-x-universe-brain- | 18M (32.97M w/BPE 16K params) | 6.477 | WEAK_PARTIAL_LIKE_BG-HS_R1 |

### synthesis / gap_or_archive_doc (n=1)
**Lever**: doc-only; pair with experimental BG to test recommendations

| BG | attempt | paradigm | capacity | corpus_mb | final_class |
|---|---|---|---|---|---|
| BG-IT | 30 | chat-cap-gap-analysis-9-axis-synthesis |  |  | GAP_ANALYSIS_LANDED_3_HIGHEST_EV_BGS_RECOMMENDED |

### partial_signal / weak_partial_pass (n=1)
**Lever**: stabilize via B25 ckpt avg + B7 best-of-N ranker — already at frontier; need consistency lever

| BG | attempt | paradigm | capacity | corpus_mb | final_class |
|---|---|---|---|---|---|
| BG-IL | 31 | 100m-nexus-ubm-combined-corpus-byte-leve | 100M-target → 153.08M actual (ConsciousLM dual-engine inflation) | 27.575 | TRUE_PARTIAL_PASS_W_F4 |

### unclassified / CORPUS_BUILD_READY (n=1)
**Lever**: manual review needed

| BG | attempt | paradigm | capacity | corpus_mb | final_class |
|---|---|---|---|---|---|
| BG-JE | 36 | corpus-100mb-plus-kowiki-ubm-nexus-outsi |  | 204.372 | CORPUS_BUILD_READY |

### emergence_below_threshold / big_corpus_small_model (n=1)
**Lever**: Stage1 foundation-borrow + Stage2 synthetic 1M dialogue (B16) — params×tokens both insufficient

| BG | attempt | paradigm | capacity | corpus_mb | final_class |
|---|---|---|---|---|---|
| BG-JH | 37 | 100m-corpus-204mb-corpus-axis-architectu | 100M-target → 153.08M actual (ConsciousLM dual-engine inflation) | 204.372 | V4_FAIL |

### evaluator_axis_landed / multi_turn_verified (n=1)
**Lever**: evaluator validated; pivot to model-side training

| BG | attempt | paradigm | capacity | corpus_mb | final_class |
|---|---|---|---|---|---|
| BG-JN | 40 | v5-multi-turn-closure-en-baseline-philos |  |  | MULTI_TURN_VERIFIED |

### unclassified / V6_AWARENESS_PROBE_LANDED (n=1)
**Lever**: manual review needed

| BG | attempt | paradigm | capacity | corpus_mb | final_class |
|---|---|---|---|---|---|
| BG-JO | 41 | v6-awareness-probe-internal-state-method |  |  | V6_AWARENESS_PROBE_LANDED |

### unclassified / D3_LANE_EVAL_LANDED (n=1)
**Lever**: manual review needed

| BG | attempt | paradigm | capacity | corpus_mb | final_class |
|---|---|---|---|---|---|
| BG-JV | 44 | d3-substrate-coupled-lane-eval-emerge-pa |  |  | D3_LANE_EVAL_LANDED |
