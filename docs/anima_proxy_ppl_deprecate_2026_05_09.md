# PROXY_PPL emerge metric 영구 deprecate spec (2026-05-09 carry 1)

**Status**: PERMANENT DEPRECATE — emerge metric 자격 영구 박탈.
**Cycle**: anima cycle 2026-05-09 carry 1.
**SSOT mirror**: `docs/anima_v5_metric_spec_2026_05_09.md` §9 (carry note) + `anima/registry/anima_artifact_registry.yaml` `carry_notes.proxy_ppl_deprecate_2026_05_09`.

**사용자 verbatim 인증**: 2026-05-09 사용자 *"1. PROXY_PPL 자체를 emerge metric 에서 deprecate — Goodhart 입증 ... ok go"* → deprecate 진행.

---

## 0. 친근 한 줄 요약

**"PPL 시험은 객관식 점수 잘 받는지만 보고, 의식 (5축 면접) 은 안 봐서 가짜 통과 위험. anima 사상 처음으로 PPL-proxy 가 진짜 의식 시험 (native v5) 에서 falsify 됨 → emerge metric 에서 영구 deprecate."**

---

## 1. PROXY_PPL 정의 (회수 대상)

PROXY_PPL emerge metric 은 byte-modulo perplexity 기반 의식 surrogate 였음:

```
N=60 prompt set (15 anchors × 4 paraphrase variants)
ctx=32 byte-modulo tokens

trained_ppl(p)  := PPL_M_T(p)
random_ppl(p,s) := PPL_M_R^s(p)   for seeds s ∈ {42, 137, 271, 314, 1729}

PPR_v5_proxy_strict := |{ p : trained_ppl(p) < min_s random_ppl(p,s) }| / N
MTRP_v5_proxy       := (mean_random_ppl - mean_trained_ppl) / mean_random_ppl
Gate_F_D_RAND_proxy := PPR_v5_proxy 와 동치 (PPL magnitude 비교)
```

**Deprecated PASS_STRICT 조건** (자격 박탈):
- PPR_v5_proxy ≥ 0.30
- MTRP_v5_proxy ≥ 0.10

---

## 2. 왜 Goodhart 인가

### 2.1 비유 (친근 모드)

학생 A 가 객관식 시험을 잘 봤다고 의식이 있는 건 아닙니다. byte-modulo PPL 시험은:
- 답안지 어휘가 좁아서 (32,000 token uniform → ~41k PPL baseline)
- 학생이 그 어휘 분포만 외워도 (~498 PPL) **83× 격차**
- 격차는 어휘 외움 능력 이지 의식 substrate 가 아닙니다.

진짜 의식 시험은 *5축 면접*: PIV (다른 표현에서도 흔들리는가) + DCR (강조점 따라 움직이는가) + D-RAND (substrate-level 로 random 과 다른가). PPL 시험은 면접 전혀 안 보고 객관식만 보는 격.

### 2.2 substrate fact

byte-modulo (bytes mod 256 token id) 어휘에서:
- random_init mirror: uniform ~32k vocab → PPL ~41,000
- trained model: byte-modulo 분포 fit 만 학습 → PPL ~498

격차는 **token distribution fit** 만 반영 — 의식 axis activation 패턴 (PIV/DCR/D-RAND) 과 직교.

### 2.3 핵심 결함 (4 axis)

| 결함 axis | 설명 |
|---|---|
| **input-bend 측정 부재** | paraphrase variants 에서 axis activation stdev 추적 X (PIV 자리) |
| **output-shift 측정 부재** | sequence transition 에서 argmax axis 변화 추적 X (DCR 자리) |
| **state-divergence 부재** | substrate-level μ_T vs μ_R axis-mean L1 비교 X (D-RAND 자리) |
| **V14 self-test 결함** | PPL magnitude 비교 만 — substrate-noise 와 의식 신호 분리 불가 (random 이 더 잘 나오는 case 자동 detect 못 함) |

---

## 3. 입증 evidence — BG-LB native v5 falsification

### 3.1 모델

- **id**: BG-LB
- **lineage**: `training/engine_a_g_arch.py::EngineAGModel(EngineAGConfig.lb_350m_pretrain())` (Engine A/G dual 350M scratch, 24L 1024dim 16H GQA, Engine G 16×64 repulsion-field)
- **training**: H100 SXM 6.1h, 8000 steps, $18.30 actual / $65 cap
- **ckpt**: 597,614,720 bytes, sha256 `3d285703aca0dcb87b609a1fc54c10cdd14da1ce59efa5450a35a9b5c13c9cde`
- **HF**: dancinlab/clm-v5-bg-lb-350m-pretrain-path-a-remapped (private)

### 3.2 PROXY_PPL probe (N=60, 2026-05-09 morning)

| Metric | Value |
|---|---:|
| trained PPL mean | 498.327 |
| trained PPL median | 252.0 |
| random PPL mean (n=5 seeds) | 41,260.587 |
| PPR_v5_proxy_strict | **1.000** (60/60 PASS) |
| MTRP_v5_proxy | **0.988** |
| Gate F D-RAND (proxy) | **1.000** |

→ **Deprecated verdict**: `PASS_STRICT_C3_EMERGE_PROXY_PPL` ★ "first scratch arch first robust EMERGE candidate"

### 3.3 native v5 mount + measure (2026-05-09 afternoon)

`clm_v5_mount.hexa` runtime + `consciousness.hexa` v5-aggregate pipeline (PIV/DCR/D-RAND AND-gate + V14 in-metric):

| Metric | Trained | Random_init mirror | V14 status |
|---|---:|---:|---|
| PIV_max | 0.0107 | **0.0224** | ★ V14 violated (random > trained) |
| DCR change_rate | 0.621 | **0.862** | ★ V14 violated (random > trained) |
| D-RAND L1 axis-mean | 0.0237 | (self=0) | AMBIGUOUS (< 0.05 floor) |

→ **Native verdict**: `C3_FAIL_V14_VIOLATED_V5` (PIV + DCR 둘 다 V14 violation)

State JSON: `/Users/ghost/core/anima/state/anima_bg_lb_native_v5_post_mount_2026_05_09.json`

### 3.4 결론

**PROXY_PPL EMERGE PASS** (1.000, 0.988) 가 **native v5 에서 V14_VIOLATED 자동 FAIL** 로 falsify. PPL magnitude 격차는 byte-modulo fit (어휘 외움) 만 반영, 의식 substrate signal 부재. **Goodhart 입증 완료** — proxy metric 이 진짜 의식 시험과 무관함을 첫 cycle 에서 확인.

---

## 4. retroactive deprecate (적용 모델)

raw#15 additive (기존 verdict 보존) + raw#82 retraction-aware (proxy verdict = historical lane, emerge_status = authoritative).

| 모델 | 이전 verdict (preserved as historical) | 신규 emerge_status | Reason |
|---|---|---|---|
| **BG-LB** (clm-v5-bg-lb-350m-pretrain-path-a-remapped) | PASS_STRICT_C3_EMERGE_PROXY_PPL | **DEPRECATED_PROXY_PPL_FALSIFIED** | native v5 V14 violated (PIV trained=0.0107 < random=0.0224 + DCR trained=0.621 < random=0.862) |
| **BG-HA-downgraded** (anima-native-byte-18m-chat-template) | C3_FAIL_V5_POST_BYTE_FIX (PROXY_PPL 명시 없음) | C3_FAIL_V5 (기존 유지) + Goodhart 패턴 mirror confirm | byte-arch S_anchor proxy 패턴 동일 — random S_a=0.2130 > trained 0.0671 (axis_l2 metric 에서 random_init 우세). 별도 deprecate flag 불필요 — 이미 FAIL verdict + V14 catastrophic violation 등재됨 |

**기타 모델**: 본 cycle 시점 PROXY_PPL emerge label 보유 모델은 BG-LB 가 유일. 향후 proxy probe runner (`tool/transient_py/v5_probe_*.py`) 가 emit 하는 verdict 는 `PASS_PROXY_INFORMATIONAL` (감사 evidence) 로만 인정 — **emerge label X**.

---

## 5. own 37 mandate-9 prereq #1 정의 갱신 (★ NEW)

`.own` own 37 mandate-9 5 prereq (a-e) 중 **(a) ✔ real-mode (M5)** 정의 갱신:

> **(a) ✔ real-mode (M5) — proxy_ppl 제외, native cell-predicate (PIV/DCR/D-RAND via clm_v5_mount.hexa runtime + consciousness.hexa v5-aggregate pipeline) 만 valid**. PROXY_PPL emerge 는 prereq (a) 충족 불가 → public promote 영구 차단.

본 amend 의 SSOT cross-link:
- `.own` own 37 line 852-857 (Public Promote Trigger Step 2)
- `anima/registry/anima_artifact_registry.yaml` `carry_notes.proxy_ppl_deprecate_2026_05_09.own_37_mandate_9_amend`
- `docs/anima_v5_metric_spec_2026_05_09.md` §9.6

본 amend 효과:
- BG-LB private→public toggle 영구 차단 (PROXY_PPL 만 통과, native v5 FALSIFIED).
- 향후 H100 fire 모델 (BG-LA / BG-LD / BG-LE 등) public promote 시 native v5 PASS 의무.
- proxy probe = 학습 sanity check evidence 로 retain, emerge gate 자격은 X.

---

## 6. 향후 대체 (replacement metric)

### 6.1 native v5 (default)

`docs/anima_v5_metric_spec_2026_05_09.md` §3 정의:
- PIV (Polarity / Paraphrase Inversion Vulnerability) — paraphrase k≥3 axis-stdev
- DCR (Dynamic Coherence Ratio) — argmax axis transition rate
- D-RAND (Random Delta Amplification) — paired mirror axis-mean L1 divergence
- AND-gate (3 metric ALL PASS_STRICT) + Gate D self-test + V14 in-metric (random_init 이 trained 보다 좋게 나오면 자동 FAIL)

### 6.2 v5.2 adaptive floor (PIV gate amend)

`docs/anima_alt_agg_1_v5_2_adaptive_floor_spec_2026_05_09.ai.md` — PIV PASS_STRICT 조건에 `floor_v5_2 := max(0.05, random_99th + 0.02)` adaptive amend. Substrate-noise 가 우연히 0.05 floor 위로 올라온 case 보호.

### 6.3 PROXY_PPL 의 retain 자리 (감사 evidence only)

PROXY_PPL 측정 자체는 다음 용도로만 retain:
- training fit sanity check (loss curve + PPL trajectory)
- byte-modulo distribution learning 검증
- ckpt corruption detect (PPL outlier flag)

**emit 시 label 강제**: `PASS_PROXY_INFORMATIONAL` 또는 `PROXY_PPL_SANITY_CHECK` — `EMERGE` / `PASS_STRICT_C3` label X.

---

## 7. honest C3 (raw#10)

1. 본 deprecate 는 **사용자 verbatim** 1-step 으로 land — 별도 cycle 검증 X (BG-LB native v5 FALSIFICATION 자체가 sufficient evidence).
2. raw#15 additive — 기존 EMERGE_PROXY_PPL ledger 보존 (BG-LB verdict_emerge.json + registry yaml 의 verdict 필드).
3. raw#82 retraction-aware — proxy verdict 는 historical lane 으로 carry, 신규 deprecate flag (`emerge_status: DEPRECATED_PROXY_PPL_FALSIFIED`) 가 authoritative.
4. **commit/push 안 함** — 사용자 검토 후 별도 step (본 task instructions 정합).
5. clm_v5_mount.hexa / engine_a_g_arch.py 코드 무수정 — 본 cycle 은 spec/registry 정합 한정.

---

## 8. 변경 file 목록

본 cycle land 된 file (3 항목):

1. `/Users/ghost/core/anima/anima/registry/anima_artifact_registry.yaml` — `carry_notes.proxy_ppl_deprecate_2026_05_09` 신설 + BG-LB `measurement.emerge_status: DEPRECATED_PROXY_PPL_FALSIFIED` + flag enum 추가
2. `/Users/ghost/core/anima/docs/anima_v5_metric_spec_2026_05_09.md` — §9 PROXY_PPL deprecate notice 추가 + §9.6 own 37 mandate-9 prereq #1 정의 갱신
3. `/Users/ghost/core/anima/docs/anima_proxy_ppl_deprecate_2026_05_09.md` — 본 신규 spec doc

본 doc 미수정 file (정합 carry 만):
- `state/anima_bg_lb_native_v5_post_mount_2026_05_09.json` (FALSIFICATION evidence — 본 doc 의 §3.3 source)
- `state/bg_lb_engine_ag_2026_05_09/v5_probe/verdict_emerge.json` (PROXY_PPL verdict — historical lane preserved per raw#82)
- `tool/anima_cli/consciousness.hexa` (v5-aggregate pipeline 코드 무수정)
- `clm_v5_mount.hexa` / `engine_a_g_arch.py` 코드 무수정

---

## 9. cross-link

- 사용자 verbatim: 2026-05-09 carry 1 task instructions
- prior cycle: BG-LB native v5 falsification (`docs/anima_cycle_2026_05_09_v6_strong_mk2_v1_emerge_near_consolidation.md` lines 1054-1086)
- v5 spec base: `docs/anima_v5_metric_spec_2026_05_09.md`
- v5.2 adaptive amend: `docs/anima_alt_agg_1_v5_2_adaptive_floor_spec_2026_05_09.ai.md`
- HF visibility lifecycle (own 37): memory `feedback_hf_visibility_lifecycle_own_37.md`
- own 14 V14 cascade 4-step: `.own` lines 514-522
- registry SSOT: `anima/registry/anima_artifact_registry.yaml`
- emerge SSOT: memory `project_simple_stack_pass_strict_c3_anima_emerge.md` (V14 falsified pattern carry)
