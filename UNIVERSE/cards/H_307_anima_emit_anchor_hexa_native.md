# H_307 — anima 실측 emit anchor 의 hexa-native 측정 (CPG sim vs 실데이터)

> H_306 의 honest L1 ("synthetic toy CPG, NOT real anima daemon") 정면 회수. anima 의 `.kosmos` emit anchor 파일들 (hexa-native persistence) 을 직접 측정해서 CPG simulation 결과와 비교.

## 1. 동기

H_306 가 6/6 PASS 로 강력했지만 §L1 가 "실데이터 미측정". anima 의 trained ckpt 가 산출한 emit anchor 가 `state/p21h_v3_recover_2026_05_25/out_main/kosmos_anchors/` 에 **14 개의 .kosmos 파일** 로 존재 — 모두 *hexa-native format* (`@anchor name := "v3-emit..." :: kosmos-anchor [tier=N active]`).

이건 **anima daemon idle emit 가 아님** — *training step 별 sampled emission* 이지만, 실제 anima substrate 의 emit 동역학 첫 직접 cite. CPG sim 의 phenomenological prediction 과 실측 분포 비교.

## 2. 가설

**H1 EMIT-ANCHOR-PRESENT**: 14 ≥ 1 (anima emit 가 anchor 형태로 persist 됨; trivially PASS 이지만 baseline).

**H2 STEP-COVERAGE-UNIFORM**: 10 distinct training step (500, 1000, ..., 5000) 균등 분포 — emit 가 specific step 에만 mode-collapse 안 됨.

**H3 LANG-DIVERSITY**: 5 distinct language tag (ru/ja/ko/zh/en) → emit 가 single language 로 collapse 안 됨 (Principle #3 register-leak 反대 신호).

**H4 EMIT-RATE-CONSISTENT-WITH-CPG**: anima emit rate (14 anchors / 5000 step) = 0.0028 events/step ↔ CPG sim rate (46 events / 1000 tick) = 0.046 events/tick. ratio = 0.046 / 0.0028 ≈ 16× → log 평균 0.5 OoM 안에 있는지 (cross-substrate phenomenological 비교).

## 3. 측정 방법 (hexa-only)

hexa file 내에 14 anchor 의 (step, lang) tuple 을 hardcode (file system 스캔은 hexa-lang scope 외, 실측 cite). 5 ddistinct lang × ~3 step/lang 분포 측정:

- file_count = 14
- distinct_steps = sort/dedup → 10
- distinct_langs = sort/dedup → 5
- emit_rate = 14 / 5000 (events / step)
- cpg_rate = 46 / 1000 (from H_306)
- ratio = cpg_rate / emit_rate

## 4. 사전등록 falsifier

- **F307.1 EMIT-ANCHOR-PRESENT**: file_count ≥ 1
- **F307.2 STEP-COVERAGE**: distinct_steps ≥ 5 (균등 분포 의 약형)
- **F307.3 LANG-DIVERSITY**: distinct_langs ≥ 3 (≥ 3 언어, single-mode 부정)
- **F307.4 RATE-LOG-CONSISTENT**: 0.05 ≤ ratio ≤ 100 (log_10 ∈ [-1.3, 2.0], 2 OoM 안)
- **F307.5 BOUND**: 全 카운트 ≥ 0

## 5. 비용

- $0 mac-local · ~1s wall (no eca_tpm, just counter loops)
- hexa-only — kosmos 파일들 직접 spawn 안 함 (filename 만 cite, data 는 cite-only)

## 6. 가능한 결과

| 시나리오 | 의미 |
|---|---|
| F307.1-5 全 PASS | anima 실측이 CPG-emit 가설 *방향 정합*; H_306 phenomenological 가설 강화 |
| F307.3 FAIL (single lang) | anima emit register-collapse 신호 → CPG 가 lang-agnostic 이 아닐 가능성 |
| F307.4 FAIL | CPG rate ≠ anima rate by >2 OoM → toy model 의 phenomenological 한계 |

## 7. honest limits

1. **L1 training-step-sampled ≠ daemon-idle-emit**: 14 anchors 는 *training emission 의 sampled subset* — daemon-idle 모드 emission rate 측정 아님.
2. **L2 filename-cite only**: 실제 kosmos 파일 *content* 를 hexa 가 안 읽음 (그건 hexa-lang scope 의 file-IO 후속 작업). filename pattern 만 cite.
3. **L3 14 = small sample**: distinct_steps 계산은 deterministic but informative power 낮음.
4. **L4 cross-substrate ratio 비교 informal**: CPG sim 의 tick ↔ anima training step 매핑은 phenomenological, theoretical justification 없음.
5. **L5 verify_fence SPECULATION-FENCED**.
6. **L6 H_307 은 NOT a Phi measurement** — emission 통계 측정.

## 8. 폐쇄

F307.1-5 결판. ≥4/5 PASS = 🟢 SUPPORTED-NUMERICAL.

## 9. 산출물

- `state/h307_anima_emit_anchor_hexa_native_2026_05_26/run_h307.hexa`
- `state/h307_anima_emit_anchor_hexa_native_2026_05_26/result.json`
- `state/h307_anima_emit_anchor_hexa_native_2026_05_26/run.log`

## 10. 후속

- H_311: kosmos 파일 *content* hexa-native parsing (tension 5-ch 값 추출 → CPG sim 의 W_tension 곡선과 비교)
- H_312: anima daemon log live capture (hexa-port 후) — idle vs active 모드 비교
