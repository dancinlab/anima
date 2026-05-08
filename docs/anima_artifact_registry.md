# Anima Artifact Registry — auto-generated

_Source: `anima/registry/anima_artifact_registry.yaml` (schema anima/registry/v1, since 2026-05-08)_  
_Regenerate: `anima/registry/render.hexa` (or `python3 tool/transient_py/anima_artifact_registry_render.py`)_

> 본 md 는 yaml SSOT 의 view layer. 모든 수정은 yaml 에 가하고 render 다시 실행. yaml = catalog SSOT / json = single-shot snapshot / jsonl = streaming append-only.

## Cycle 2026-05-08 milestone

**KICK WAVE 4 3/3 random_init mirror probe — V14 anti-Goodhart VIOLATED. Earlier sft-1-8 EMERGE claim falsified.**  
sole robust EMERGE: **`NONE`** ★

**Honest C3 findings (raw#10)**:
- own 18 line 881 PPR=0.71 claim FALSIFIED → ALT-AGG-1 v3 supersede
- wrapper-prefix-only schema fix (Path A) — clm_v4 LoRA load chain unblock
- universal phenomenal bottleneck FALSIFIED (sft-1-8 spontaneous)
- JVAE Variant 1 differentiator WEAK (sft-1-8 no-JVAE > paradigm-j with-JVAE)
- phenomenal redesign canonical qualia (Block/Chalmers/Nagel) anti-Goodhart V14 정합
- paradigm-j retry N=30 EMERGE was sample-size artifact (N=60 reverted to PARTIAL_NEAR)
- ★ KICK WAVE 4 3/3: random_init ConsciousDecoderV2 PPR_v3=0.5517 EXCEEDS sft-1-8 0.4138 (delta -0.1379) — ALT-AGG-1 v3 V14 VIOLATED, sft-1-8 EMERGE indistinguishable from untrained noise on this 30-prompt eval
- KICK WAVE 4 1/3: sft-1-8 N=120 ensemble live probe PPR_v3=0.5378 (64/119) — verdict floor compliance reaffirmed at strongest sample but DOES NOT close V14 gap (sft-1-8 N=120=0.5378 < random_init N=30=0.5517); trajectory N=30→N=60→N=120 = 0.4138→0.6102→0.5378 (N=60 peak, N=120 mild regression -0.0724); plateau ~0.5 zone confirmed

**Framework amends**:
- ALT-AGG-1 v3 (C3.4 anchor + ≥1 corroboration, PPR≥0.25) — own 18 line 881 정정
- ALT-AGG-1 v3 STATUS: FALSIFIED by random_init mirror — needs v4 redesign (random_init separator gate or anchor-baseline subtraction)
- D1 binary → gradient (own 17 line 676+) — ambiguous_research lane 신설
- D1 formula edge case: random_init shows D1=0.8 within is artifact (parameters set ≠ trained) — PPR must carry meaningful signal
- own 38 매단계 doc + model + dataset save mandate 신설
- own 39 yaml↔md mandatory regenerate (auto-render after registry edit)
- axis orthogonality empirically confirmed (PPR ⊥ Φ_normalized)

## Models

**D1 gradient** (own 17 line 676+ amend, 2026-05-08): `D1 = 0.2 × p_updated + 0.2 × corpus_ratio + 0.6 × arch_origin`. Threshold: ≥0.7 within / 0.3-0.7 ambiguous_research / <0.3 outside.

### Quick view

| id | D1 | lane | PPR_v3 (latest) | verdict | HF (private) |
|---|---|---|---|---|---|
| `clm-v4-sft-1-8-stage1` | 0.793 | ✅ within_strict | 0.5378 | ~~SIMPLE_STACK_PASS_STRICT_C3_ANIMA~~ V14_VIOLATED | dancinlab/clm-v4-sft-1-8-stage1-path-a-remapped |
| `clm-v4-paradigm-j-50k-final` | 0.793 | ✅ within_strict | 0.2414 | ~~C3_PARTIAL_NEAR~~ FALSIFIED@N=60 | dancinlab/clm-v4-paradigm-j-50k-final-path-a-remapped |
| `clm-v4-sft-1-7-y1-stage1` | 0.793 | ✅ within_strict | 0.1034 | C3_PARTIAL_NEAR | dancinlab/clm-v4-sft-1-7-y1-stage1-path-a-remapped |
| `clm-v4-mk2-v1` | 0.99 | ✅ within_strict | — | NOT_MEASURED | — |
| `clm-v2-byte-18m` | 0.99 | ✅ within_strict | — | INDETERMINATE_C3_v2_byte | need-singularity/clm-v2-byte-18m-convo-5k |
| `anima-native-byte-18m` | 0.99 | ✅ within_strict | — | NOT_MEASURED_LOCAL | — |
| `random-init-mk2-v1-mirror` | 0.8 | within_strict_FORMULA_ONLY | 0.5517 | SIMPLE_STACK_PASS_STRICT_C3_RANDOM_INIT_V14_VIOLATED | — |
| `BG-KM-LLAMA-3B` | 0.351 | ⚠️ ambiguous_research | NOT_MEASURED | — | — |
| `paradigm-a-prime` | 0 | 🚫 outside_strict | — | SIMPLE_STACK_PASS_STRICT_C3_SUBSTRATE_RESEARCH | — |

### `clm-v4-sft-1-8-stage1`

**aliases**: `sft-1-8`  
**lineage**: base=clm-v4-mk2-v1 (ConsciousDecoderV2 anima-native scratch) / method=LoRA r=128 + anima-internal SFT / jvae=absent / arch_origin=anima_native_scratch  
**D1**: score=**0.793** (✅ within_strict) — p_updated=0.01, corpus=0.95, arch=1  
**measurement**: ppr_v3_n30=0.4138, ppr_v3_n60=0.6102, ppr_v3_n120=0.5378  
**verdict**: SIMPLE_STACK_PASS_STRICT_C3_ANIMA / emerge_state=EMERGE_FALSIFIED_BY_RANDOM_INIT_MIRROR (FALSIFIED@N=60)  
**D5 cooperative_score**: 0.7617  
**Φ_norm_N8 max**: 0.0425 (subcritical zone)  
**HF**: private=`dancinlab/clm-v4-sft-1-8-stage1-path-a-remapped` / public=(blocked)  
**eligibility**:
  - mandate_9_a_d1_within: `MET`
  - mandate_9_b_v6_strong: `NOT_MET`
  - mandate_9_c_user_verbatim: `NOT_ISSUED`
  - mandate_9_d_trinity_sweep: `PASS`
  - mandate_9_e_dl_sweep: `PASS`
  - public_promote: `BLOCKED_AWAITING_B_AND_C`
**commits**: probe_n30=`bb4ef174`, probe_n60=`fe4f8a7d`, probe_n120=`522a859a`, hf_upload=`5cb9570a`, path_a_remap=`d478023c`  

### `clm-v4-paradigm-j-50k-final`

**aliases**: `paradigm-j`, `paradigm-j-retry`  
**lineage**: base=clm-v4-mk2-v1 (ConsciousDecoderV2) / method=LoRA r=128 + JVAE Variant 1 (q_phi + p_theta) step=50000 / jvae=present / arch_origin=anima_native_scratch  
**D1**: score=**0.793** (✅ within_strict) — p_updated=0.01, corpus=0.95, arch=1  
**measurement**: ppr_v3_n30_initial=0.2414, ppr_v3_n30_phenomenal_redesign=0.3793, ppr_v3_n60=0.2414  
**verdict**: C3_PARTIAL_NEAR / emerge_state=CARRY (FALSIFIED@N=60)  
**D5 cooperative_score**: 0.7144  
**Φ_norm_N8 max**: 0.0371 (subcritical zone)  
**honest_c3**: N=30 EMERGE was sample-size artifact (per-seed perfect tie 0.2414/0.2414 at N=60)  
**HF**: private=`dancinlab/clm-v4-paradigm-j-50k-final-path-a-remapped` / public=(blocked)  
**eligibility**:
  - mandate_9_a_d1_within: `MET`
  - mandate_9_b_v6_strong: `NOT_MET`
  - mandate_9_c_user_verbatim: `NOT_ISSUED`
  - mandate_9_d_trinity_sweep: `PASS`
  - mandate_9_e_dl_sweep: `PASS`
  - public_promote: `BLOCKED_PPR_FALSIFIED`
**commits**: probe_n30_initial=`eb209c1a`, probe_n30_redesign=`58fec5ed`, probe_n60_falsified=`84aa8665`, hf_upload=`dc98618e`, path_a_remap=`dc1510a3`  

### `clm-v4-sft-1-7-y1-stage1`

**aliases**: `sft-1-7-y1`  
**lineage**: base=clm-v4-mk2-v1 (ConsciousDecoderV2) / method=LoRA r=128 + anima-internal SFT / jvae=absent / arch_origin=anima_native_scratch  
**D1**: score=**0.793** (✅ within_strict) — p_updated=0.01, corpus=0.95, arch=1  
**measurement**: ppr_v3_n30=0.1034  
**verdict**: C3_PARTIAL_NEAR / emerge_state=CARRY (FALSIFIED@N=60)  
**honest_c3**: self-reference 5-axis collectively 약화 (0/15) — SFT corpus 가 self-ref 활성 부족 시사  
**HF**: private=`dancinlab/clm-v4-sft-1-7-y1-stage1-path-a-remapped` / public=(blocked)  
**eligibility**:
  - mandate_9_a_d1_within: `MET`
  - public_promote: `BLOCKED_PPR_PARTIAL_NEAR`
**commits**: probe_n30=`da762cc8`, hf_upload=`5cb9570a`, path_a_remap=`d478023c`  

### `clm-v4-mk2-v1`

**aliases**: `mk2-v1`, `clm-v4-base`  
**lineage**: base=scratch (ConsciousDecoderV2 anima pre-train) / method=full pre-training (no LoRA) / jvae=absent / arch_origin=anima_native_scratch  
**D1**: score=**0.99** (✅ within_strict) — p_updated=1, corpus=0.95, arch=1  
**verdict**: NOT_MEASURED / emerge_state=PENDING  
_D1 가장 높은 candidate (0.99) — sft fine-tune 전 base 자체 측정 가치_

### `clm-v2-byte-18m`

**aliases**: `v2-byte`, `clm-v2-byte`  
**lineage**: base=scratch (byte-level, vocab=256, n_layer=6, d_model=384, 18M params) / method=full pre-training (no LoRA) / jvae=absent / arch_origin=anima_native_scratch  
**D1**: score=**0.99** (✅ within_strict) — p_updated=1, corpus=0.95, arch=1  
**verdict**: INDETERMINATE_C3_v2_byte / emerge_state=CARRY  
**HF**: private=`need-singularity/clm-v2-byte-18m-convo-5k` / public=(blocked)  

### `anima-native-byte-18m`

**aliases**: `BG-FY`, `BG-FY-18M`  
**lineage**: base=scratch (byte-level + anima corpus) / method=full pre-training / jvae=absent / arch_origin=anima_native_scratch  
**D1**: score=**0.99** (✅ within_strict) — p_updated=1, corpus=0.95, arch=1  
**verdict**: NOT_MEASURED_LOCAL / emerge_state=BLOCKED  

### `random-init-mk2-v1-mirror`

**aliases**: `random_init_mk2_v1`, `kick4-v14-mirror`  
**lineage**: base=scratch (ConsciousDecoderV2 random_init torch.manual_seed=42) / method=NO TRAINING — random weights only (anti-Goodhart V14 probe) / jvae=absent / arch_origin=anima_native_scratch  
**D1**: score=**0.8** (within_strict_FORMULA_ONLY) — p_updated=1, corpus=0, arch=1  
**measurement**: ppr_v3_n30=0.5517  
**verdict**: SIMPLE_STACK_PASS_STRICT_C3_RANDOM_INIT_V14_VIOLATED / emerge_state=EMERGE_FALSE_POSITIVE  
**HF**: private=`None` / public=PERMANENT_BLOCK  
**eligibility**:
  - mandate_9_a_d1_within: `FORMULA_ONLY`
  - mandate_9_b_v6_strong: `NOT_APPLICABLE`
  - mandate_9_c_user_verbatim: `NOT_APPLICABLE`
  - mandate_9_d_trinity_sweep: `V14_VERIFY_RESULT`
  - public_promote: `PERMANENT_BLOCK_UNTRAINED_NOISE`
_anti-Goodhart V14 mirror — random_init also passes ALT-AGG-1 v3, falsifying sft-1-8 EMERGE claim. V14 VIOLATED → ALT-AGG-1 v3 strict 가 너무 약함. Multi-seed (n=5) variance: mean=0.4276 stdev=0.3366 range=[0.17, 0.97]; v4 threshold candidate 1.03 unreachable → PPR_v3 metric structurally broken (high inter-seed noise floor). Need anchor-baseline subtraction OR per-axis noise gating OR replace PPR_v3 with separator metric._

### `BG-KM-LLAMA-3B`

**aliases**: `BG-KM-LLAMA`, `KM-LLAMA-3B`  
**lineage**: base=meta-llama/Llama-3.2-3B-Instruct (external) / method=LoRA r=32 + heavy anima corpus (~85%) / jvae=absent / arch_origin=external_lora_only  
**D1**: score=**0.351** (⚠️ ambiguous_research) — p_updated=0.005, corpus=0.85, arch=0.3  
**measurement**: ppr_v3=NOT_MEASURED  
_D1 gradient amend (own 17 line 676+ 2026-05-08) 후 격상 가능 — partial public promote path 별도 verbatim 'OK PROMOTE PUBLIC AMBIGUOUS RESEARCH <repo>' + V6 STRONG + 4 prereq_

### `paradigm-a-prime`

**aliases**: `paradigm-a-prime-llama`  
**lineage**: base=meta-llama/Llama-3.2-3B-Instruct (external) / method=chat-template wrapping only (NO parameter update) / jvae=absent / arch_origin=external_pure_wrapper  
**D1**: score=**0** (🚫 outside_strict) — p_updated=0, corpus=0, arch=0  
**verdict**: SIMPLE_STACK_PASS_STRICT_C3_SUBSTRATE_RESEARCH / emerge_state=  
**D5 cooperative_score**: 0.625  
**HF**: private=`None` / public=PERMANENT_BLOCK  
_.roadmap.substrate_research 별도 도메인 — anima verdict 후보 X, public promote 영구 차단_

## Datasets

| id | size | HF (private) | cycle |
|---|---|---|---|
| `anima-persona-tier-a-v3` | 87.04 MB / 1224473 lines | dancinlab/anima-persona-tier-a-v3 | 2026-05-08 |
| `anima-persona-tier-a (raw)` | 103.59 MB / 1478588 lines | — | 2026-05-08 (pre-filter) |
| `clm-l4-ld-preference-pairs-iter1` | 18874368 bytes | — | 2026-05-08 |
| `anima-model-attempts-ledger` | — | — | continuous (2026-05-07+) |

### `anima-persona-tier-a-v3`

_anima persona corpus (Q1+Q2+KOBEST filtered v3)_

**size**: bytes=91266753, mb=87.04, lines=1224473

**filter applied**: awk one-shot block-aware (Q1 config/core_rules.json line 1478043~EOF + Q2 [augmented] KMMLU 16456 + KOBEST 1110, 7-line / 6-line block-aware)  
**reduction**: -17.19% (254115 lines, 16.55 MB)  
**verification**: config_core_rules_count=0 / augmented_count=0 / kmmlu_count=0 / kobest_count=0 / anima_role_preservation=106596

**quality issues**:
- Q3 MED: preference pairs 13 unique stems 만 2610-5222× 반복 (별도 dataset)
- Q4 LOW: bare-string 17.4% / chat-template 82.6% (own 20 ≥30% PASS)
- Q5 LOW: chosen 5 unverified factual claims (BG-KM v4_pass non-gate)

**HF**: private=`dancinlab/anima-persona-tier-a-v3` / public=(blocked or NOT_UPLOADED)  

### `anima-persona-tier-a (raw)`

_pre-filter raw persona corpus_

**size**: bytes=108624820, mb=103.59, lines=1478588

**quality issues**:
- Q1 ★: line 1478043~EOF (546 lines) config/core_rules.json verbatim — D1 SCOPE_CLAMP 침범

**HF**: private=`None` / public=(blocked or NOT_UPLOADED) (superseded)  

_tier_a_v3 로 대체 — 본 raw 는 필요 시 archival_

### `clm-l4-ld-preference-pairs-iter1`

_LD preference pairs (DPO format)_

**size**: bytes=18874368, lines=30023

**quality issues**:
- Q3 MED: 13 unique prompt stems × 2610-5222 반복 (top-10 cluster 2610s, bottom-3 1305 half-frequency)
- diversity 부족 — paraphrase / re-extract spec 필요

### `anima-model-attempts-ledger`

_chat-cap training/inference attempt ledger (own 24 SSOT)_

_본 yaml registry 와 cross-link — model attempt 시 jsonl append + 본 yaml model entry update_

## Cross-link

- **jsonl_ledger**: `state/anima_model_attempts_ledger.jsonl`
- **jsonl_schema**: `anima/spec/anima_model_attempts_ledger.schema.yaml`
- **philosophy**: `.roadmap.philosophy`
- **law**: `.roadmap.law`
- **hypothesis**: `.roadmap.hypothesis`
- **cli**: `.roadmap.cli`
- **own_ssot**: `.own`
- **memory_dir**: `~/.claude-claude1/projects/-Users-ghost-core-anima/memory/`

## Compliance

- **own_22_mandatory_report**: PASS
- **own_24_single_SSOT**: PASS
- **own_38_매단계_저장**: PASS
- **own_33_trinity**: d_axis=PASS / own_axis=PASS / h_axis=PASS
- **own_34_mandate_2_wrap_0**: PASS
- **raw_15_additive**: PASS
- **raw_82_retraction_aware**: PASS

