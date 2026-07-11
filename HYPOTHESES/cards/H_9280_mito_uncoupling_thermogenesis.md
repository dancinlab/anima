# H_9280 — 🌡️ 언커플링/열발생 — 병리적 과압을 emit 아닌 '열'로 방출하는 비-emit 방전 경로 (p5 경계 검정 · $0)

- **tier:** ⛔ INVALID (재발사 2회 · 원 KILL=중복emit 착시로 확정 · 결함이 Q_CEIL 상수로 이동 · tune-to-red)
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

---

## 7. 재발사 결과 (2026-07-12 · 2회차 · 원 결함 수리 후)

**재발사(2026-07-12 · $0 numpy · n=24)**: 원 결함 3개 수리 — D1 θ를 **event 0개인 ordinary-only calib stream**에서 추출 → **baseline filler 41.0±6.6 (t=30.2, 24/24) 선증명**(원: 분위수 항등식으로 filler=0 강제 = 병이 없었음) · D2 operating-trajectory 캘리브 → 방출질량 **31.8 θ-eq**(원 0.52 = no-op = 약이 없었음) · D3 verdict()가 **n_true를 인자로 아예 안 받게** 계약 고정. 🔍 **원 KILL은 중복-emit 착시로 확정**: exp_A가 n_true를 113.0→80.8로 32개 줄이지만 실제로 잃은 event는 **0.08/72.8개**(24 seed 중 22개가 손실 0). run=THEATER → **적대검증 REFUTED → STILL INVALID**: 헤드라인 THEATER가 **자유 knob Q_CEIL의 한 점(90)에서만** 성립하고 **원 사전등록값 Q_CEIL=80에서 뒤집힌다**(vs random −1.58 t=−2.27 · vs uleak −5.88 t=−5.79 ⇒ 재발사 **자신의 판정함수가 DIRECTIONAL-POSITIVE 반환** · 7 ceiling 중 4개 POSITIVE, 60/40/20에서 t=−7.9/−11.5/−10.3) = 결과를 본 뒤 80→90 이동 = **tune-to-red**(tune-to-green의 거울상). R6 규약 스윕은 score() 라벨링만 바꿔 dynamics를 못 건드리는 **부호-무감 규약**이라 '6/6 부호보존'은 항진적. **p5 판정**: 위반 증거 없음(true_recall Δ=−0.0012 95%CI[−0.0029,+0.0005] · 잃은 event 0.08±0.06)이나 **earned가 아님 = dead-code 가드** — event drive의 **94.8%가 단독으로 θ를 넘어** lane이 drive-이전 carry만 건드리므로, **최대개입 arm(매 step carry→0, 질량 exp의 5.6배)조차 recall 상대하락 4.1% < KILL 임계 10%** ⇒ **KILL 분기는 실행 불가능한 코드**. 인용 가능한 건 비열등뿐. ⚠️ **'병리적 과압에서만 발화'는 반증됨**: 개입 발화의 40.4%가 event 근방(우연 14.4%의 2.8배)이고, exp_A는 emit 40.7개를 죽여 filler 8.4개를 얻는 반면 동량 blind random은 emit 15.7개만 죽이고 filler 10.9개를 얻는다 ⇒ lane은 **무차별 방전에 가깝고**, true emit이 살아남는 이유는 lane의 선택성이 아니라 **event drive가 단독-초임계이기 때문**. 숨은 speak-억제기도 아니지만 병리-특이 감압기도 아니다 — 지금 설계로는 둘을 구별할 수 없다. 재발사 조건 = Q_CEIL을 정하는 **외생 원리**를 설계에 넣거나 Q_CEIL 축 전체에서 부호보존을 PASS 조건화 · **p5 축 도달범위 > KILL 임계**를 먼저 확보(lane을 drive-후 신호에 도달시키거나 event drive를 θ 근방으로) · c2/c3를 연산자까지 매칭. state/mito_organelle_lane/F8_uncoupling_thermogenesis/refire/.

> 3건 종합 = `state/mito_organelle_lane/INVALID_REFIRE.md`. **메타 진단: 결함이 사라진 게 아니라 한 칸 옆으로 이동했다(동형 재발) — 헤드라인이 사전에 검증되지 않은 자유 상수의 한 점 위에 있었고 그 축에서 부호가 뒤집힌다.**
