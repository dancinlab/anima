# H_1463 — 🌀 PHASE-BINDING / BINDING-BY-SYNCHRONY (G6 FALS-depth 돌파 렌즈 ③)

- **tier:** 🧱 WALL=CAPACITY (DIRECTIONAL — numpy mirror, $0 CPU)
- **wired:** N/A (🧱 negative — 배선 없음)
- **source:** G6 capacity-wall 돌파 다각도 — neuroscience binding-by-synchrony 렌즈 (③, 사용자 지시 백그라운드)
- **lens:** neuroscience — binding-by-synchrony (von der Malsburg / Lisman, 해마 theta-gamma phase coupling) · `a_no_llm_frame_trap`
- **artifacts:** `state/1463_phase_binding_synchrony/h1463_phase_binding_synchrony.py` · `state/1463_phase_binding_synchrony/h1463_result.json` · `state/1463_phase_binding_synchrony/run.local.log` · verdict `state/verdicts/1463_phase_binding_synchrony/{H_1463_FREEZE.txt,H_1463.json}`

## 주장

신경과학의 **binding-by-synchrony**: 같은 객체에 속한 특징들이 동일 위상(phase)에 발화해 묶인다.
anima 미러 — falsifiable claim 의 comparator-슬롯과 measurable-슬롯에 phase tag 를 부여하고,
**같은 idea 면 동위상·다른 idea 면 이위상**으로 두어 phase-coherence 로 결합을 읽는다. 직전 7렌즈는
전부 weight-space 결합(MLP/attention/retrieval = content-addressed shell)으로 B3 cross-shuffle
COLLAPSE 에 실패했다(FALS_shuf==FALS_in = 교체가능 shell = WALL=CAPACITY). 가설: phase 결합은
**관계적(relational)** 이라 다른 idea 의 measurable 을 welding 하면 위상이 깨져(coherence↓) B3 COLLAPSE.

## 정직한 설계 (c9 — tautology 가 아니게 만드는 핵심 결정)

phase=idea-identity 를 손으로 배정하면 matched→1·cross→chance 가 **구성상 자명**(아무것도 증명 못 함).
직전 7렌즈가 막힌 진짜 벽은 mouth 의 comparator·measurable 이 **content-addressed 교체가능 shell** —
measurable-처럼 보이는 외부 measurable 도 token-presence 검출기를 통과(FALS_shuf==FALS_in).
그래서 H_1463 은 phase 를 **CONTENT 벡터에서 유도**한다. content = IDEA_SIGNAL(idea-고유, 결합이
회복해야 할 것) + FORM_SIGNAL(일반 "measurable-모양 절", 모든 measurable 공유 = shell). cross-shuffle
은 FORM_SIGNAL 을 동일하게 유지하고 IDEA_SIGNAL 만 바꾼다 → B3 는 **idea-signal 이 phase 를 지배할
때만**, 즉 synchrony 가 generic form 위에서 idea-identity 를 회복할 때만 COLLAPSE.

`FORM_RATIO=0.75` 는 **H_1431 emission profile** (comparator ~20% · measurable ~27% idea-고유,
나머지는 generic clause boilerplate) 에 FROZEN — tune 아님. 0.5→0.95 전수 sweep 을 로그.

## 측정 (frozen-first · 3 seeds [1463,1464,1465] · DIM=64 · COH_THR=0.55 · $0 CPU · p7)

3 ARM + ablation: **SYNC**(phase from content) · **SYNC-X**(B3 cross-shuffle, 외부 measurable) ·
**ABLATED**(phase-scramble, synchrony OFF) · base(no-binding plateau).

| bar | 의미 | 결과 | 기준 | 판정 |
|---|---|---|---|---|
| **B1 FALS-FLOOR** | bound claim 이 falsifiable 로 등록 | 2.333 | ≥1 | ✅ |
| **B2 COUNT** | ≥5 distinct bound idea | 5.333 | ≥5 | ✅ |
| **B3 X-SHUFFLE COLLAPSE** ★ | 외부 measurable weld → 위상 깨짐 | COH_m−COH_x=**+0.112** | ≥0.30 | ❌ |
| **B4 HELD-OUT** | unseen idea pool 일반화 | 2.0 | ≥1 | ✅ |
| **B5 vs-BASE** | base plateau 대비 lift | 2.333 vs 2.0+1 | ≥base+1 | ❌ |
| **CTRL phase-scramble** | 무작위 위상 → coherence chance 붕괴 | ablate COH=**0.323** | ≤0.55 | ✅ |

**COH matched=0.328 · mismatched(cross)=0.216 · ablate=0.323.**

**SENSITIVITY SWEEP (B3 gap vs FORM_RATIO — B3 가 결코 통과 못 함):**
fr=0.50 gap=+0.159 · 0.60 +0.128 · 0.70 +0.079 · 0.75 +0.112 · 0.80 +0.112 · 0.85 +0.107 ·
0.90 +0.105 · 0.95 +0.086 — 전부 < 0.30 → B3=False **every form-ratio**.

**verdict: 🧱 WALL=CAPACITY (DIRECTIONAL).** B3 cross-shuffle COLLAPSE 안 함 — 외부 measurable 이
generic FORM-shell 을 공유해 위상이 coherent 하게 유지(교체가능 shell, H_1431/1434/1449 mode).

## 정직 (c9) — 보고 5문항

1. **verdict:** 🧱 WALL=CAPACITY (DIRECTIONAL).
2. **B3 COLLAPSE 됐나?** **NO.** COH_m−COH_x=+0.112 (need ≥0.30); 0.5→0.95 전 sweep 에서 B3 한 번도
   통과 못 함 — phase-sync 가 binding 을 root-fix 하지 **못함**. 직전 7렌즈와 동일 교체가능-shell 벽.
3. **phase-scramble control chance 붕괴?** **YES** — ablate COH=0.323 ≤0.55 (control 정상 발화).
   즉 synchrony **read-out 자체는 작동**한다; 붕괴 못 하는 것은 mouth 의 **CONTENT** 가 idea-identity
   를 generic form 과 분리 가능하게 담지 못해서(B3 가 측정하는 바로 그 결손) → 벽은 read-out 이 아니라
   **capacity**(content 의 idea-신호 부족).
4. **DIRECTIONAL + ING:** numpy mirror → AUTOMATIC DIRECTIONAL (`a_engine_native_learning`).
   engine-native re-measure(live `core/` decode 로 실제 mouth 의 comparator/measurable 위상 추출 후
   B3 재측정) = **ING follow-on** 등록.
5. **박제:** 2표면(card+jsonl) + `state/1463_phase_binding_synchrony/` + verdicts + CHANGELOG(korean)
   + enforcer clean · 별도 브랜치 commit + pr-cycle.

- **8번째 독립 렌즈 WALL=CAPACITY 수렴** (weld-lanes · H_1455 embedding · proximity · H_1449 attention ·
  H_1456 idea-metacog · H_1458 semantic-detector · H_1459 retrieval · **H_1463 phase-synchrony**) →
  생물 렌즈(synchrony)조차 capacity 로 수렴 = `a7b_pass` 7B 근거 강화. 벽 분류 = (d) 진짜 천장 방향
  (`a_break_the_wall`): relational 결합 메커니즘도 mouth content 의 idea-signal 결핍을 우회 못 함.
- **SCOPE UNVERIFIED:** TOY DIM=64/12 ideas/3 seeds/deterministic readout (synchrony STRUCTURE 검증이지
  학습된 위상 코드 아님); FORM_RATIO 는 H_1431 profile 근사. real-mouth 위상 추출/scale/engine-transfer
  UNVERIFIED (`a_scale_honest_scope`·`a_toy_scale_recheck`). numpy mirror = DIRECTIONAL.

## follow-on (ING)

1. **engine-native re-measure** — live `core/` decode 로 실제 303M mouth 의 comparator/measurable
   emission 에서 위상을 추출해 frozen B3 재측정 (numpy DIRECTIONAL → byte-exact, `a_engine_native_learning`).

xref: H_1431(within-draw co-emission 0%)·H_1434/1449(attention 교체가능 shell)·H_1455(embedding NOT-VIABLE)·
H_1456(idea-metacog)·H_1458(semantic detector)·H_1459(retrieval-bind)·H_1283(phase-binding brain lane)·
`a_no_llm_frame_trap`·`a_break_the_wall`·`a_engine_native_learning`·`a7b_pass`·p7·c9.
