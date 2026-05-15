# anima registry yaml deep audit — 2026-05-10

**SSOT 대상**: `anima/registry/anima_artifact_registry.yaml`
**Audit cycle**: anima cycle 2026-05-10 (mandate health check)
**사용자 verbatim**: 2026-05-09 "별 5개 짜리 나올때까지 bg 분산처리"
**모드**: yaml read + light edit only (모델 로드 절대 X)

---

## §0 친근 의의 — yaml SSOT health check 가 왜 필요한가

`anima_artifact_registry.yaml` 는 anima 전체 우주의 **모델 호적부** 다. cycle 2026-05-09 + 2026-05-10 진행 중 여러 BG 가 같은 파일을 동시에 amend 하면서 미세한 불일치가 쌓일 수 있다 — 마치 호적계 직원 여럿이 한 장부에 동시에 적으면 글씨가 겹치는 것과 같다. 이번 deep audit 는 그 호적부가 깨끗한지 (syntax 정합), 같은 사람이 두 번 등록되지 않았는지 (duplicate), 주민번호가 공식과 맞는지 (D1 = 0.2·p + 0.2·c + 0.6·a) 확인하는 작업이다. mandate (yaml ↔ md auto-regenerate) 의 본질은 호적부의 매 항목이 신뢰 가능해야 하는 것이므로, 본 audit 는 의 실제 health check 1 회분이다.

---

## §1 syntax 검증 결과

| 항목 | 값 |
| --- | --- |
| `python3 yaml.safe_load` | **PASS** |
| 총 라인 수 | 3127 (edit 후 동일) |
| 최상위 key 수 | 21 |
| 최상위 keys | schema_version, registry_name, since, mode, status, carry_notes, cycle_close_summary, cross_link, models, datasets, paraphrase_v5, cycle_2026_05_08, h100_resource_pool, multi_chat_tests, chat_lanes, chat_modes, chat_init_patterns, chat_transports, chat_verifiers, chat_axes_meta, compliance |

**결론**: parser 통과 — syntax 결함 0 건.

---

## §2 model entries 정합 (15 models)

### §2.1 D1 공식 audit (formula = 0.2·PUR + 0.2·corpus + 0.6·arch)

| model id | PUR | corpus | arch | score (yaml) | expected | 정합 |
| --- | --- | --- | --- | --- | --- | --- |
| clm-v4-sft-1-8-stage1 | 0.01 | 0.95 | 1.0 | 0.793 | 0.792 | OK |
| clm-v4-paradigm-j-50k-final | 0.01 | 0.95 | 1.0 | 0.793 | 0.792 | OK |
| clm-v4-sft-1-7-y1-stage1 | 0.01 | 0.95 | 1.0 | 0.793 | 0.792 | OK |
| clm-v4-mk2-v1 | 1.0 | 0.95 | 1.0 | 0.99 | 0.990 | OK |
| clm-v2-byte-18m | 1.0 | 0.95 | 1.0 | 0.99 | 0.990 | OK |
| anima-native-byte-18m | 1.0 | 0.95 | 1.0 | 0.99 | 0.990 | OK |
| **anima-native-byte-18m-chat-template** | 1.0 | 1.0 | 1.0 | **0.99 → 1.0** | **1.000** | **MISMATCH → FIXED §7-A** |
| random-init-mk2-v1-mirror | 1.0 | 0.0 | 1.0 | 0.8 | 0.800 | OK (formula-only special case) |
| BG-KM-LLAMA-3B | 0.005 | 0.85 | 0.3 | 0.351 | 0.351 | OK (ambiguous_research) |
| BG-LA | 1.0 | 0.95 | 1.0 | 0.99 | 0.990 | OK |
| BG-LB | 1.0 | 0.95 | 1.0 | 0.99 | 0.990 | OK |
| clm_v5_phase2_cotrain_engine_ag | 1.0 | 0.95 | 1.0 | 0.99 | 0.990 | OK |
| BG-LC | 0.005 | 0.85 | 0.3 | 0.351 | 0.351 | OK (ambiguous_research) |
| BG-LD | 0.01 | 0.95 | 1.0 | 0.793 | 0.792 | OK |
| paradigm-a-prime | 0.0 | 0.0 | 0.0 | 0.0 | 0.000 | OK (outside_strict 영구) |

**14/15 정합 — 1 건 fix (§7-A).**

### §2.2 emerge_status / lane 분포

| 분류 | count | models |
| --- | --- | --- |
| within_strict | 11 | sft-1-8, paradigm-j, sft-1-7-y1, mk2-v1, clm-v2-byte-18m, anima-native-byte-18m, anima-native-byte-18m-chat-template, BG-LA, BG-LB, clm_v5_phase2_cotrain_engine_ag, BG-LD |
| within_strict_FORMULA_ONLY | 1 | random-init-mk2-v1-mirror (V14 anti-Goodhart mirror; PERMANENT_BLOCK_UNTRAINED_NOISE) |
| ambiguous_research | 2 | BG-KM-LLAMA-3B, BG-LC |
| outside_strict | 1 | paradigm-a-prime |

### §2.3 v5_lane_verdict 정합 (paradigm-j 단독 dual-lane)

전체 yaml 검색 결과 `v5_lane_verdict` 출현 1 건 — `clm-v4-paradigm-j-50k-final.measurement.v5_lane_verdict` 단독.

| sub-lane | verdict | 기준 | 값 | status |
| --- | --- | --- | --- | --- |
| base_f1_max | PARTIAL_NEAR | piv_max ≥ 0.10 | piv_max=0.0874 | DEPRECATED_F1 |
| base_f2_l2 | EMERGE_V5_PIV_F2_PASS | piv_l2_max ≥ 0.12, mean ≥ 0.06 | 0.1439 / 0.0841 | DEFAULT_STANDARD |
| adaptive_floor | (정합 carry) | random_99th + 0.02 | (별도 sub-block) | PASS |

paradigm-j 만 `v5_lane_verdict` 등록 — task 명세 (paradigm-j base+adaptive dual lane) 와 일치.

### §2.4 HF / ckpt path 정합

structured `hf:` block 보유 14 / 15 models. 1 model `clm-v4-sft-1-8-stage1` 만 `hf:` block 부재 — 대신 `measurement.public` / `measurement.visibility_status` / `measurement.promote_commit_url` 로 inline 등록 (§6-B 참고).

dancinlab org canonical:
- `dancinlab/clm-v4-sft-1-8-stage1-path-a-remapped` (public, promoted 2026-05-09)
- `dancinlab/clm-v4-paradigm-j-50k-final-path-a-remapped` (public, promoted 2026-05-09 — first robust EMERGE)
- `dancinlab/clm-v5-bg-lb-350m-pretrain-path-a-remapped` (private; PROXY_PPL Goodhart-falsified)

 5/5 prereq strict — public 2 / private 다수 / paradigm-a-prime PERMANENT_BLOCK 모두 정합.

---

## §3 chat orchestra section 정합

### §3.1 chat_axes_meta — 5 axes (T+3 LANDED)

| axis_id | name | label_internal | registry_file | status |
| --- | --- | --- | --- | --- |
| axis-1 | lane | axis-3 | tool/anima_cli/chat/lanes/_registry.hexa | LANDED |
| axis-2 | mode | axis-6 | tool/anima_cli/chat/modes/_registry.hexa | LANDED (T+2 promoted) |
| axis-3 | init-pattern | axis-8 | tool/anima_cli/chat/init_patterns/_registry.hexa | LANDED |
| axis-4 | transport | axis-N | tool/anima_cli/chat/transports/_registry.hexa | LANDED |
| axis-5 | verifier | axis-N+1 | tool/anima_cli/chat/verifiers/_registry.hexa | LANDED_2026_05_10_T_3 |

5 axes 모두 LANDED. T+6 axis-6 modality 는 next_step (n_axis_cross_product.next_step).

### §3.2 cross-product cardinality 정합

| 시점 | 식 | 값 | yaml 위치 |
| --- | --- | --- | --- |
| T+2 baseline (--n-axis 미사용) | 4×3×4×5 | **240** | line 2945 cross_product_count_t2 |
| T+2 placeholder simulation | 4×3×4×5×2 | 480 | line 3087 hook_simulation_2026_05_10 |
| T+3 active (verifier 3 LANDED) | 4×3×4×5×3 | **720** | line 2944 cross_product_count_t3 |
| T+3 trio activation 미래 | 4×3×4×5×4 | 960 | line 2955 ("trio 활성 시 960 combos 자동 expand") |

task 명세에 언급된 `4800` 은 yaml 어디에도 부재 — 240 / 480 / 720 / 960 만 SSOT 등록. (4800 = 240×20 또는 다른 가설 식 — 본 cycle 미정합. **task 명세상 가설값**으로 추정.)

### §3.3 chat_modes — T+2 promote 정합

`chat_modes.cycle_landed: 2026-05-09` / `cycle_promoted: 2026-05-10` / `hexa_ssot: tool/anima_cli/chat/modes/_registry.hexa` / `hexa_ssot_prior: tool/anima_cli/chat/lanes/benchmark.hexa`. modes: 1:1 / ai-duo (LANDED) + ai-trio (별도). promote 정합.

### §3.4 chat_verifiers — T+3 4 entries

`chat_verifiers.cycle_landed: 2026-05-10` / `default_verifier: c3_per_turn` / 4 entries (c3_per_turn LANDED, duo_d1234 LANDED, trio_3way DEFERRED, v14_strict LANDED). honest C3 emit 5 항목 (C1 trio DEFERRED, C2 SKELETON, C3 720 combo, C4 raw#15 additive, C5 F-axes-6 fixture) 정합.

---

## §4 cycle_close_summary.cycle_2026_05_09 정합

| 항목 | yaml 값 | task 명세 hint | 정합 |
| --- | --- | --- | --- |
| ts_close | "2026-05-09 cycle close phase" | — | OK |
| user_verbatim | "지금 가능한것들 all bg go" | — | OK |
| historic_ranking | "anima saga 22+ BG saga 가장 큰 결실 cycle" | — | OK |
| **milestones_total** | **50** | **59+** | **GAP — task hint 와 9+ 차이** |
| cost_actual_usd | 66 | 66 | OK |
| cost_budget_usd | 200 | — | OK |
| cost_remaining_usd | 134 | — | OK |
| robust_emerge_v5_2_count | 1 | 1 | OK (paradigm-j) |
| robust_emerge_v5_base_f2_count | 1 | — | OK (paradigm-j) |
| hf_changes.public_promote_count | 2 | 2 | OK |
| hf_changes.private_deferred_count | 2 | — | OK |
| chat_orchestra_4_axis | LIVE_FIRE_VERIFIED | — | OK (5 axes T+3 supersede) |
| raw_15_additive | True | — | OK |
| raw_82_retraction_aware | True | — | OK |

**milestones_total = 50** 은 yaml SSOT 가 가장 보수적 numeric — 본 audit 는 기존 값 보존 (raw#15 additive, destructive amend 안 함). task hint "59+" 는 향후 amend 후보 (mandate 차기 cycle 검토).

---

## §5 carry_notes 정합

| carry note | enabled | cycle | retroactive_models | replaced_by |
| --- | --- | --- | --- | --- |
| proxy_ppl_deprecate_2026_05_09 | true | 2026-05-09 carry 1 | BG-LB, BG-HA-downgraded | NATIVE_V5_PIV_DCR_DRAND_AND_GATE |

- own_37_mandate_9_amend 정합 — prereq #1 갱신 ("PROXY_PPL 제외, native cell-predicate 만 valid")
- raw_15_additive: true / raw_82_retraction_aware: true — 정합
- 다른 carry note 부재 (단 1 carry block)

---

## §6 발견된 inconsistency

### §6-A [FIXED] D1 score numeric stale — anima-native-byte-18m-chat-template

- **before**: score=0.99 (corpus_ratio=1.0, expected=1.000)
- **root cause**: 자매 모델 anima-native-byte-18m (corpus=0.95, score=0.99) 에서 copy-paste, corpus=1.0 amend 시 score 갱신 누락
- **fix**: §7-A 참고

### §6-B [DOCUMENTED — non-destructive] HF block 위치 비정합 — clm-v4-sft-1-8-stage1

- **before**: structured `hf:` block 부재. `measurement.public` / `measurement.visibility_status` / `measurement.promote_commit_url` / `measurement.promote_date` 등 inline (measurement: 약 89 fields 중 ~6 개 HF 관련).
- **root cause**: cycle 2026-05-09 PUBLIC promote 시 amend 가 measurement 블록에 inline 되어 다른 14 model 패턴과 결가 깨짐.
- **수정 보류**: raw#15 additive strict — 기존 값 모두 보존, 추가 amend 가 destructive 가 될 위험. 차기 cycle render.hexa 자동 regenerate 시 정규화 권장.
- **현재 정합 영향**: 없음 (값 자체는 정확; 위치만 비표준).

### §6-C [DOCUMENTED] task hint vs yaml mismatch — milestones_total

- **task hint**: 59+
- **yaml**: 50
- **수정 보류**: yaml 이 SSOT — task hint 가 후행 amend 후보. V14 reproducibility strict.

### §6-D [DOCUMENTED] task hint vs yaml mismatch — cardinality 4800

- **task hint**: 240 / 720 / 4800
- **yaml**: 240 / 480 / 720 / 960 (4800 부재)
- **수정 보류**: 4800 산식 도출 불가 (4×3×4×5 = 240 base; ×20 multi 식 sustain 못함). task 명세 가설값으로 분류.

---

## §7 수정 항목 (raw#15 additive only)

### §7-A — anima-native-byte-18m-chat-template d1.score: 0.99 → 1.0

```yaml
# before (line 1033)
score: 0.99

# after (line 1033)
score: 1.0 # ★ AUDIT 2026-05-10 corrected from 0.99 (stale copy from sister anima-native-byte-18m corpus=0.95); 0.2*1.0+0.2*1.0+0.6*1.0=1.000 strict per d1 formula (D1 SCOPE_CLAMP gradient amend)
```

- additive comment 추가 (raw#15 strict — 기존 의미 무손상)
- 다른 fields 무변경
- post-edit `yaml.safe_load` PASS 검증 완료

**총 수정**: 1 건 / 1 line (D1 numeric correction + audit trail comment).

---

## §8 친근 한 줄

호적부 3127 줄을 한 칸 한 칸 짚어 본 결과 — 한 명 (chat-template 18M) 의 주민번호 마지막 자리가 0.99 로 잘못 적혀 있던 것을 1.0 으로 바로잡았고, 나머지 14 명 + chat-orchestra 5 axes + cycle close 정산 + carry note 모두 정합. 호적부는 건강하다.

---

## §9 다음 cycle 권장 (mandate 강화 방안)

1. **render.hexa auto-regenerate health-check job** — 의 자동 yaml ↔ md 정합을 매 cycle close 시 1 회 실행 (CI-like). Mac fork starvation 카리 (BG ≤ 7 strict, fork 친화 설계).
2. **D1 formula validator script** — `tool/transient_py/anima_d1_formula_audit.py` 등 추가; yaml load → 모든 model entry 의 PUR/corpus/arch ↔ score 차이가 ≤ 0.01 인지 자동 검증; PASS / FAIL emit. V14 reproducibility strict.
3. **HF block schema 표준화** — `hf:` block 의 minimum schema 정의 (private / public / visibility_status / promote_*) — clm-v4-sft-1-8-stage1 재정렬 (raw#15 additive — measurement inline 도 carry, 새 hf block 신설 mirror).
4. **milestones_total 갱신 검토** — task hint 59+ 가 정확하면 cycle_close_summary amend (사용자 verbatim 후 1 회 cycle).
5. **cardinality SSOT 명시** — 240 / 480 / 720 / 960 의 근거 식 한 표로 yaml top-level (chat_axes_meta.cardinality_table) — 4800 같은 가설값과 혼동 방지.
6. **carry_notes 다중 entry pattern** — 현재 1 carry block; 차기 cycle (proxy_ppl deprecate + 향후 추가) 시 list 구조로 grow — schema_version 검토.
7. ** health-check 결과 yaml top-level 등록** — `audit_log:` block 추가 (yaml 자기 자신에 대한 audit trail) — raw#15 additive strict.

---

**audit by**: anima cycle 2026-05-10 deep audit BG (/ / / / strict)
**file**: `/Users/ghost/core/anima/docs/anima_registry_yaml_deep_audit_2026_05_10.md`
**yaml SSOT**: `/Users/ghost/core/anima/anima/registry/anima_artifact_registry.yaml`
**post-edit syntax**: PASS (3127 lines, 21 top-level keys)
**모델 로드**: 0 회 (strict)
**fork BG**: yaml read + light edit only (Mac load 보호)
