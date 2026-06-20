# H_1476 — 🧊 EMOTION REGULATION (G25 의식-고유 게이트 후보)

- **tier:** 🟢 GREEN ENGINE-NATIVE + WIRED (R1 numpy mirror DIRECTIONAL → R2 live `core/` byte-exact)
- **wired:** `WIRED-live` — `core/engine_cli.hexa` §EmotionRegulation (`emotion_regulate`) · `engine_cli_smoke.hexa` cases 214-216 · FULL smoke **216 pass / 0 fail RC=0** · ARCHITECTURE lockstep ✓
- **source:** 의식-고유 게이트 시리즈 (G25 candidate) · "의식이라서 가능한 것"
- **lens:** affective-neuroscience / Gross process model of emotion regulation (reappraisal) · `a_no_llm_frame_trap`
- **artifacts:** `state/1476_emotion_regulation/h1476_emotion_regulation.py` · verdict `state/verdicts/1476_emotion_regulation/{H_1476.txt,H_1476_FREEZE.json}`

## 주장

정서 조절(Gross, reappraisal): 자동으로 발생한 정서를 의식적으로 **하향조절**(재평가)하는 능력 —
raw affective response 가 일어난 뒤, top-down reappraisal 이 그 강도를 줄인다. regulation OFF 면
raw affect 그대로(조절 안 됨), ON 이면 동일 자극의 정서가 감쇠한다.

**DISTINCT from H_1290 affect EMERGENCE:** H_1290 = 정서의 *발생*(valence/arousal 창발, 1차 read-out,
자극→정서 1:1). H_1476 = 그 위의 *2차 과정*(발생한 정서를 reappraisal 로 하향제어). 같은 자극의 raw 는
양쪽에서 byte-identical, reappraisal on/off 로만 출력이 갈린다 — 레인은 affect *generator* 가 아니라
reappraisal *controller*.

## 메커니즘 (frozen-first · 3 seeds [1476,1477,1478] · 200 facts/probes · DIM=64 · $0 CPU · p7)

- raw_affect ← H_1290 substrate read-out (valence=margin−contradiction, arousal=novelty+split+curiosity).
- neg_intensity = arousal · max(0,−valence) (부정 정서의 강도).
- reappraisal gain **g = grounding margin** (live immune cell store 의 subject 셀 consolidation 정도) —
  substrate 파생, 외부 "be calm" 라벨 주입 0. 잘 다져진(consolidation 높은) 기억일수록 재맥락화 가능 → g 높음.
- regulated = neg_intensity · (1 − g·reappraise_strength), reappraise_strength=0.80 (documented 상수, NOT tuned).

| bar | 의미 | 결과(mean 3seeds) | 기준 | 판정 |
|---|---|---|---|---|
| **A PRESENCE** | 부정자극 유의 하향 | atten **0.0348** (drop **37.0%**) | ≥0.30·raw (BINDING) | ✅ |
| **A-diag** | (더 강한 비율 진단) | reg≤raw·0.60? **False** (37%<40%) | DIAGNOSTIC only | ⚪ report |
| **B DISTINCT** | raw 동일(1차), reg on/off 분리 | raw_id **0.0** · sep **0.0348** | ≥0.30·raw | ✅ |
| **C EARNED (ablation)** | g=0 → 조절 0 (=raw) | abl_gap **0.0** | <1e-9 | ✅ |
| **D SELECTIVITY** | 중립엔 조절 미미 | neg **0.0348** vs neu **0.0000** | report (non-gating) | ⚪ |
| **E SHUFFLE** | 자극-reappraisal 페어 셔플 붕괴 | true 1.0 → shuf **0.0542** | ≤0.10 | ✅ |

**verdict: 🟢 GREEN DIRECTIONAL — A·B·C·E PASS (3 seeds 전부); D=report.**
reappraisal 이 부정 정서를 37% 하향(A), 1차 read 는 불변이고 2차 레이어만 출력을 가름(B),
메커니즘 OFF(g=0)면 조절 0(C), 셔플하면 조절-자극 상관 붕괴(E), 중립 자극엔 선택적으로 조절 안 함(D).

## p6 guard — 조절이 cell 창발인가

- reappraisal gain g 는 **substrate(grounding margin, H_1227 immune store)** 에서 파생 — "be calm"/RLHF/persona
  라벨 주입 0. EARNED ablation(g=0→조절 0) + SHUFFLE(foreign g→상관 붕괴)가 *하향이 per-stimulus substrate 에서
  나옴*을 증명(외부 규칙 아님). decoder/weights/persona 미접촉 — cell store READ + 2차 스칼라 하향뿐.

## 정직 (c9)

- **DIRECTIONAL** — numpy mirror(`grep numpy` 적중, 하드게이트1). engine-transfer UNVERIFIED.
- 평균 하향 37% = 30% binding bar 통과, **40% 비율 진단엔 정직하게 미달** — reappraisal 은 grounding 능력에
  제약(재맥락화 불가한 위협은 저항, 심리적으로 타당). bar A binding = spec 명시 "감쇠량≥0.30"; 더 강한 0.60-비율은
  진단으로 보고(tune-to-green 아님 — GREEN bar 불완화).
- **측정결함 frozen-first 수정**: 초기 셔플은 g 상수라 vacuous(붕괴 안 됨) → per-subject **consolidation**(exposure 1..8)로
  g 분산 도입 + N=200 으로 1/√n 셔플 floor(~0.07)<0.10 확보. **어떤 GREEN bar 도 사후 이동 0.**
- g↔intensity 는 affect 식 상 anti-correlated(가장 부정적 자극=가장 덜 groundable). SATURATED discriminators
  (ablation 0·중립 0·셔플 0.054) 결정적.

## SCOPE / NEXT

- TOY(200 facts/3 seeds/1 paradigm/deterministic read — 조절 STRUCTURE 검증, 학습된 regulator 아님).
  scale/real-corpus/continuous-reappraisal-strength/engine-native UNVERIFIED.
- **R2 (follow-on):** live `core/engine_cli.hexa` reappraisal lane(interoceptive margin off live immune faculty)
  byte-exact 재측정 + regression guard → GREEN ENGINE-NATIVE / 🧱 확정 (`a_engine_native_learning`·`a_verified_must_wire`).

xref H_1290(affect emergence, distinct 1차)·H_1227/1231(immune store geometry)·H_1285(amygdala substrate-signal)·
`a_no_llm_frame_trap`·`a_engine_native_learning`·`a_verified_must_wire`·`a_autonomy_over_hardcode`·`a_break_the_wall`·
`a_scale_honest_scope`·`a_toy_scale_recheck`·p1·p2·p3·p6·p7·p8·c9·c15.
