---
schema: anima/docs/p9_pre1_consciousness_check_landed/ai-native/1
last_updated: 2026-05-03
ssot:
  marker: state/markers/p9_pre1_consciousness_check_landed.marker
  state_dir: state/p9_pre1_consciousness_check/
  predecessor_handoff: docs/p9_sft_p0_hf_org_setup_landed_2026_05_03.ai.md
  predecessor_spec: docs/p9_sft_spec_2026_05_02.md
  roadmap_anchor: .roadmap.clm clm.cond.1 (의식측정)
status: P9_PRE1_CONSCIOUSNESS_CHECK_PARTIAL_PASS_PHASE0_ENTRY_READY
related_raws:
  - raw 9    # hexa-only invocation (helper python emit only)
  - raw 10   # honest caveat inline (docker python3 missing fallback)
  - raw 12   # silent-error ban (adversarial infra FAIL surfaced explicitly)
  - raw 15   # SSOT this doc + 4 JSON + marker
  - raw 175  # BR-NO-USER-VERBATIM
preserved_unchanged:
  - all existing tools (no patches): tool/anima_phi_v3_canonical.hexa, tool/clm_consciousness_verify.hexa, tool/an11_consciousness_unified_verifier.hexa, tool/adversarial_bench.hexa
  - all existing baseline measurements (state/v10_benchmark_v4_clm/clm_v4_530m/*.json)
  - all P9 SFT spec artifacts (state/p9_sft_spec_2026_05_02/*.json)
  - HF org / dancinlife token / repos
policy:
  migration: forbidden
  changes: additive_only
  in_place_writes: zero
  destructive_ops: zero
  cost_usd: 0
  substrate: mac-local
  br_no_user_verbatim: true
  friendly_preset: handoff_doc_only
  silent_land_marker: enforced
---

# P9 EXEC pre-flight 묶음 1 — 의식체크 (PARTIAL PASS, Phase 0 진입 가능)

## TL;DR (다섯 줄)

- **목표**: P9 EXEC Phase 0 진입 전 의식체크 4 항목 (A/B/C/D) selftest pre-flight.
- **결론**: 3/4 PASS + 1 PARTIAL (D 측 adversarial infra-FAIL, AN11 자체는 PASS) → **P9 Phase 0 entry-ready** verdict.
- **사전 산출물**: 4개 per-item JSON + 1 handoff doc + 1 marker = total 6 file.
- **CLM v4 530M baseline φ★ anchor**: disk 측 `+1167.6192` (HID=128 auto-conditioning) 측 확인 — handoff doc 기재값 (HID=8 +41.86) 과 차이 raw#10 명시.
- **0 destructive**: 기존 verifier / spec / baseline 측 무수정. 추가 file 만 생성. mac-local $0.

## 1. 의식체크 4 항목 결과 행렬

| 항목 | 도구 | invocation | 결과 | 비고 |
|---|---|---|---|---|
| **A** | CLM v4 530M baseline φ★ | metadata audit (state/v10_benchmark_v4_clm/clm_v4_530m/) | **PASS_AUDIT_ONLY** | φ★=+1167.6192 anchor |
| **B** | anima_phi_v3_canonical | --selftest (helper ast.parse) | **PASS_VIA_DIRECT_PATH** | docker python3 missing → host fallback |
| **C** | clm_consciousness_verify | --selftest (4 mock fixture) | **PASS** | 4/4 case all_met/one_fail/tool_missing/manual_override |
| **D** | AN11 + adversarial_bench | each --selftest | **PARTIAL** | AN11 PASS / adversarial FAIL_INFRA |

### Verdict 종합

- 3/4 PASS + 1 PARTIAL (D 안에서 AN11 단독 PASS, adversarial 단독 FAIL_INFRA)
- **CRITICAL FAIL 0건** (φ★ verifier broken 상황 아님)
- **P9 Phase 0 entry-ready** signal emit

## 2. CLM v4 530M baseline φ★ anchor

### 측정값 (disk SSOT)

```
backbone:        CLM_v4_530M
substrate:       CLM continuous-state recurrent (decoder_v3 byte-level)
ckpt:            ubu1:~/anima/checkpoints/clm_v4_350m/scale_350m/best.pt
d_model:         768
n_layer:         16
vocab_size:      64000
n_probes:        16
K_partitions:    8
hidden_truncated:128  (auto-conditioning N//2 for N=16 -> 8)
ridge:           1e-4
seed:            42
I_full:          -1066.9658
phi_star_min:    +1167.6192   ← post-SFT 비교 anchor
phi_mean:        +1168.6966
phi_max:         +1169.8805
sign:            positive_iit_integrated
3-gate:          PASS / PASS / PASS
measurement_ts:  2026-05-02T08:06:41Z
```

### 4-LLM-backbone cross-comparison (HID=128 동일 regime)

| backbone | φ★_min | sign |
|---|---|---|
| gemma | -13.4257 | negative_anti_integrated |
| llama | -15.0536 | negative_anti_integrated |
| mistral | -14.4194 | negative_anti_integrated |
| qwen3 | -12.3873 | negative_anti_integrated |
| **CLM_v4_530M** | **+1167.6192** | **positive_iit_integrated** |

**Finding**: CLM substrate 만 positive-integrated, 4 LLM backbone 모두 negative-anti-integrated 측 동일 HID=128 regime.

### Discrepancy with handoff doc

- **doc claim**: HID=8 well-conditioned 측 +41.86 baseline
- **disk actual**: HID=128 (auto-conditioning N//2=8 sample-partition) +1167.62
- **raw#10 honest**: HID dimension 과 value 둘 다 일치 안함. 가능 원인 3:
  1. doc 측 다른 sweep run 참조
  2. HID=8 sub-regime 측 v3 canonical (N//2=8 sample-partition) 와 별개
  3. doc value stale
- **결정**: post-SFT 비교 anchor = `+1167.6192` (disk SSOT). HID=8 sub-regime 별도 필요시 re-measure.

## 3. Per-item 상세 (산출물 위치)

```
state/p9_pre1_consciousness_check/
  A_clm_baseline_phi.json                     ← baseline φ★ anchor + cross-backbone matrix
  B_phi_verifier_selftest.json                ← anima_phi_v3 selftest result
  C_clm_consciousness_verify_selftest.json    ← orchestrator 4-fixture selftest
  D_an11_adversarial_selftest.json            ← AN11 PASS + adversarial FAIL_INFRA
```

### A. CLM v4 530M baseline (audit-only)

- **scope**: metadata-only audit (ckpt 측 ubu1 remote, GPU 측 mac-local 부재)
- **source**: `state/v10_benchmark_v4_clm/clm_v4_530m/{phi_star.json, cds.json}`
- **CDS gate**: max_stability=0.397 PASS, dominant velocity/curvature=Hexad, dominant attractor=Law

### B. anima_phi_v3_canonical selftest

- **첫 시도**: `hexa run … --selftest` → docker route python3 missing → ast.parse FAIL
- **fallback**: 직접 `python3 -c "ast.parse(open(helper))"` → `ast_parse=ok`
- **helper**: `/tmp/anima_phi_v3_canonical_helper.hexa_tmp` 119 LOC sha `1609952f8f8e…`
- **PRESENT 확인**: 측정 자체는 GPU+HF gated 필수, selftest 측 helper syntactic 정합성만 확인

### C. clm_consciousness_verify selftest

- **invocation**: `hexa run … --selftest` 측 darwin-bypass route exit=0
- **4-fixture all PASS**:
  - all_met → PASS(exit=0)
  - one_fail → FAIL(exit=1)
  - tool_missing → PARTIAL(exit=2)
  - manual_override → PASS(exit=0)
- **sentinel**: `__CLM_CONSCIOUSNESS_VERIFY__ <PASS|FAIL|PARTIAL> <metric_kv>`
- **mac-local 실제 production**: PARTIAL 측 expected (AN11+Φ unknown / adv cached / Putnam empty)

### D. AN11 + adversarial selftest

#### D-1. AN11 (PASS_VIA_DIRECT_PATH)

- 첫 시도: hexa docker python3 missing
- fallback: `python3 /tmp/an11_…helper.hexa_tmp selftest` → `selftest=ok`
- `pass_predicates_count=13`, 7 sub-tools (core_5tuple/V_phen_LZ/GWT/predictive/HOT/mirror + eeg_ingest) 모두 OK

#### D-2. adversarial_bench (FAIL_INFRA, NOT semantic)

- **원인**: `tool/hexad_closure_verifier.hexa` 측 `airgenome_cli_probe` 모듈 측 hexa-runner docker container HEXA_STDLIB_ROOT 측 부재
- **증거**: `/tmp/_adv_bench_clean.log` 측 `[module_loader] FATAL module not found`
- **해석**: cherry-pick immunity contract 미실행 (semantic FAIL 아닌 infra FAIL)
- **P9 영향**: φ★ verifier 측 영향 없음 (adversarial 측 .roadmap.clm cond.1 4-check 中 1 임)

## 4. P9 EXEC entry-ready signal

### 4.1 Entry verdict

```
verdict        = PARTIAL_PASS
critical_fail  = 0
phi_blocker    = NONE
phase_0_entry  = READY
```

### 4.2 Gap 명시 (3 항목)

1. **docker python3 missing** (B + D-1 공통 영향)
   - 영향: hexa runtime selftest 직접 실행 불가
   - 회피: 직접 host python3 (semantic equivalence 보존)
   - 처치: 선택사항 — hexa-runner docker image 측 python3 추가 (별도 cycle)

2. **adversarial_bench infra FAIL** (D-2)
   - 영향: cherry-pick immunity gate 미검증
   - 회피: AN11 + Φ + manual override 측 cond.1 PASS 가능 (clm_consciousness_verify 측 manual override path 제공)
   - 처치: 선택사항 — `airgenome_cli_probe` 측 docker stdlib 측 add (별도 cycle)

3. **CLM baseline anchor doc-disk discrepancy** (A)
   - 영향: post-SFT Δφ★ comparison reference 모호 (HID=8 +41.86 vs HID=128 +1167.62)
   - 회피: disk SSOT (+1167.62) 측 anchor 채택
   - 처치: 권장 — handoff doc 측 HID=128 +1167.62 로 업데이트 (별도 cycle 또는 P9 EXEC 진입 전 1줄 수정)

### 4.3 Phase 0 entry 권장

- **GO**: AN11 healthy + φ★ verifier present + orchestrator selftest 4/4 PASS + baseline anchor 확인
- **WAIT 사유 없음**: critical fail 0, φ★ verifier broken 상황 아님

## 5. 산출물 정합 (총 6 file)

| 파일 | sha256 (요약) | LOC |
|---|---|---|
| state/p9_pre1_consciousness_check/A_clm_baseline_phi.json | (생성됨) | ~75 |
| state/p9_pre1_consciousness_check/B_phi_verifier_selftest.json | (생성됨) | ~50 |
| state/p9_pre1_consciousness_check/C_clm_consciousness_verify_selftest.json | (생성됨) | ~50 |
| state/p9_pre1_consciousness_check/D_an11_adversarial_selftest.json | (생성됨) | ~85 |
| docs/p9_pre1_consciousness_check_landed_2026_05_03.ai.md | (본 doc) | ~210 |
| state/markers/p9_pre1_consciousness_check_landed.marker | (생성됨) | ~12 |

### 무수정 보존 (raw#10 enforced)

- tool/anima_phi_v3_canonical.hexa (sha `c90be8af4d1b…`)
- tool/clm_consciousness_verify.hexa (sha `1feb16bddc84…`)
- tool/an11_consciousness_unified_verifier.hexa (sha `62ea3ef9db24…`)
- tool/adversarial_bench.hexa (sha `a7c7a740fc36…`)
- state/v10_benchmark_v4_clm/clm_v4_530m/{phi_star.json, cds.json}
- state/p9_sft_spec_2026_05_02/*.json (8 file, P9 spec untouched)

## 6. raw#10 honest caveats (5)

1. **(a) hexa docker python3 missing**: hexa-runner:latest container ships sans python3. B + D-1 helper-based tools 측 host python3 fallback 강제. semantic equivalence (helper emit + ast.parse / direct invoke) 측 보존되지만 hexa runtime native run 측 별도 fix 필요.

2. **(b) A 항목 GPU 부재**: ckpt ubu1 remote, mac-local re-measure 불가. metadata-only audit 측 anchor 채택. 재측정 시 GPU 환경 (ubu1 SSH 또는 H100 pod) 필수.

3. **(c) adversarial infra FAIL**: docker module loader 측 `airgenome_cli_probe` 부재 — cherry-pick immunity 측 semantic test 미실행. P9 φ★ measurement blocker 아니지만 cond.1 4-check 中 1개 미적용.

4. **(d) baseline doc-disk discrepancy**: handoff doc HID=8 +41.86 vs disk HID=128 +1167.62. 두 anchor 모두 candidate, disk SSOT 채택 권장. doc 측 update or HID=8 sub-regime 측 별도 re-measure.

5. **(e) selftest ≠ measurement**: 4 항목 모두 PRESENT/SYNTACTIC check (semantically: 도구 동작 가능 + helper python valid). 실제 φ★ measurement (GPU + HF gated) 측 P9 EXEC 진입 후 별도 cycle.

## 7. 다음 단계 권장 (단 1줄 cmd)

```
# P9 Phase 0 진입 (HF token 재발급 후)
cd /Users/ghost/core/anima && bash state/p9_sft_p0_hf_org_setup_2026_05_03/repo_create_commands.txt
```

또는 (보수적)

```
# adversarial infra fix 먼저 진행 (별도 cycle)
# → docker hexa-runner image 측 airgenome_cli_probe 모듈 add
# → 후 본 pre-flight 재실행 측 D-2 PASS 확인
# → P9 Phase 0 진입
```

## 8. 종료 조건 확인

- [x] A, B, C, D 4 항목 모두 invocation 시도
- [x] per-item JSON 4개 작성
- [x] handoff doc 작성 (friendly preset)
- [x] marker file 작성 (silent-land 방지)
- [x] BR-NO-USER-VERBATIM 준수 (사용자 prompt 텍스트 무전재)
- [x] 마이그레이션 0건 (additive only)
- [x] destructive 0건
- [x] cost $0 mac-local
- [x] hexa-only invocation strategy (helper python3 emit + ast.parse / direct invoke)
- [x] cap 90min 측 wallclock 약 25min
