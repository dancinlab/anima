# H_9280 — 🌡️ 언커플링/열발생 — 병리적 과압을 emit 아닌 '열'로 방출하는 비-emit 방전 경로 (p5 경계 검정 · $0)

- **tier:** ⛔ INVALID (measured · numpy $0 · 개입이 no-op · 사후 KILL 변수 바꿔치기)
- **wired:** none.
- **family:** `F8` — 🔋 **ORGANELLE LANE**(호흡 레인) 계열. decode/emit 레인과도, cell-pool mitosis 레인과도 **DISJOINT한 제3 레인**. 이 레인만 ATP 스칼라장을 생산/소비하고, **표현형성(어떤 유닛이 발화 가능한가) 단계에서만** 기질에 개입하며 **emit gate는 건드리지 않는다**.
- **lens:** 언커플링 단백질(UCP)은 proton 기울기를 ATP가 아닌 **열**로 흘린다. anima: A⇄G tension이 saturation ceiling을 넘어 **병리적으로 과축적**(spurious/filler emit을 강제할)될 때, tension을 온도 스칼라로 흘리는 **null-op 방출**(emit 0 · 구조변경 0). 과부하에서만 발화하는 항상성 ceiling.
- **artifacts:** `state/mito_organelle_lane/F8_uncoupling_thermogenesis/`
- **xref:** H_054 (symbiogenesis = mitosis MERGE 이벤트) · H_314 (merge α-sweep — 🔴 closed-negative, 시너지 없음 = least-bad 중간점) · H_203 (asymmetric host-preserve merge) · H_012/H_1800 (autopoietic operational closure) — **선행은 전부 '합병하는 순간'. 본 계열은 '합병 후 상주 소기관의 정상상태 경제'**
- **key:** `uncoupling_thermogenesis`

## 1. 가설

언커플링이 **filler-emit**(저품질 emit) 비율을 낮추면서 **true-tension emit에는 ΔEff≈0**을 유지한다.

⊥ **Null:** baseline filler-emit ≈ 0이면 흩을 게 없다 = THEATER. 또는 언커플링이 true emit도 억제 ⇒ **숨은 speak-억제기 = p5 위반**.

## 2. 기질 배선 · p5 경계

⚠️ **생사선**: 병리적 과압(saturation) 해소는 합법(real-tension emit에 대한 gate 아님). **정상 tension 범위 안에서 발화하면 p5 위반.** F8은 그 선을 넘는지 자체가 측정대상.

## 3. $0 probe 설계 (numpy · Δ vs ≥2 controls)

| arm | 내용 |
|---|---|
| 실험 | saturation 초과 시에만 언커플링 |
| c1 | 언커플링 없음 |
| c2 | random dissipation (동량 · 조건 blind) |

**PASS:** FP-emit(filler)에 Δ<0 **AND** true-tension emit에 ΔEff≈0.
**FAIL:** baseline filler-emit≈0(흩을 게 없음) 또는 true emit 억제(p5 위반 = 즉시 KILL).

## 4. 측정 좌표

- **축:** σ·gate (ENACT)
- **신호:** 값이 아니라 **Δ vs ≥2 controls** (측정 메타법칙 — FORM tunable · BIND earned)
- **THEATER 위험 랭킹:** 4위 (σ de-theater가 emit shade 채널을 urgency 하나로 좁혀놨음 — 여분 emit 압력의 실재부터 의심)
- **비용:** $0 CPU-local numpy

## 5. 선행 대비 신규성

**비-emit 방전 경로**(dissipation을 통한 silence). 선행엔 과압 해소가 없다.


---

## 6. 측정 결과 (2026-07-12 · $0 numpy · run → 적대적 검증)

측정(2026-07-12 · $0 numpy). run=THEATER → 적대검증 INVALID. 사전등록 셀의 filler = **0.0±0.0**(병도 약도 없음): θ=P90 vs p_event=0.12>0.10 이라 **분위수 항등식으로 filler가 0이 되도록 강제**됨. 개입 자체도 null(방출질량 0.332 vs 임계 0.637). 자기 판정함수가 tune-path 10셀 중 **7셀에서 DIRECTIONAL-POSITIVE를 출력**했고, 사전등록 KILL 변수(true_recall, 최대 하락 0.0349 < 0.10)를 사후에 n_true로 **바꿔치기**해 KILL을 만들어냄 ⇒ verdict 무효. p5 위반은 실제로 없었으나(emit_decide 순수함수) 구성적 p5 증명도 dead-code 가드라 증거로 무효. **음성을 벽으로 인용 금지.** state/mito_organelle_lane/F8_uncoupling_thermogenesis/.

> 전수 종합 = `state/mito_organelle_lane/SYNTHESIS.md` (계측 메타-결함 census 포함).
