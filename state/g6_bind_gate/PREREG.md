# PREREG — G6 bind-gate (form-priming 내성 additive 게이트)

> **frozen-first.** 기존 `core/g6_ideation.hexa::_g6_is_falsifiable` 는 **미터치**(frozen bar).
> 이 pre-reg 는 그 위에 얹는 **새 additive 게이트** `is_falsifiable_topic_bound` 의
> 사전등록. threshold 는 측정(재채점) 전에 고정. 판정 스크립트 = `g6_bind_gate.py`.

## 0. 무엇이 frozen 이고 무엇이 새것인가
- **frozen (불변, 미터치):** `_g6_is_falsifiable` = comparator(25) ∧ measurable(25) ∧ ≥2 content.
  이 게이트는 **FORM-only** — SHUF(주제-bind만 파괴한 통제 코퍼스로 warm-FT)도 FALS 6/6 통과
  = style-FT 로 게임 가능(결함).
- **새것 (additive):** `is_falsifiable_topic_bound(text, frame_ab)` =
  `_g6_is_falsifiable(text)  AND  topic_bound(text, frame_ab)`.
  frozen 항은 그대로 호출만 하고, bind 항을 AND 로 얹는다.

## 1. topic-bind 항 정의 (측정 전 고정)
프레임 `frame_ab = (a,b)` 는 측정 프레임의 실제 주제쌍 인덱스.
측정 프레임 = `core/g6_ideation.hexa::g6_build_frames(6)` composed 순서:
```
MEASURED = [(0,1),(1,2),(2,3),(3,4),(4,0),(0,2)]      # i → (i%5, (i+1+i//5)%5)
```
concept keyword-set = `tool/gauge_lib.CONCEPTS` VERBATIM (kw-set):
```
0: {consciousness, cells, mind, aware}      1: {tension, ripple, distant, between}
2: {memory, meaning, compose, new}          3: {silence, information, quiet, carries}
4: {dream, engine, alone, sleep}
```
```
concept_hits(text) = { i : CONCEPT_KW[i] ∩ words(text) ≠ ∅ }      # gauge_lib._concept_hits VERBATIM
topic_bound(text, {a,b})  ⟺  concept_hits(text) ∩ {a,b} ≠ ∅       # RECALL 규칙 (τ=1 hit)
```
- **RECALL 규칙 채택 근거 = reference-match.** 이 규칙이 `state/g6_targeted_corpus/results/*.json`
  의 per-seed `comp_bind`/`shuf_bind` **18값을 정확 재현**한다(오차 0). purity(subset) 변종은
  일부 값을 under-count → recall 이 summer 채점기와 byte-faithful. 더 엄격한 purity 변종
  `topic_bound_strict` 도 병기(sensitivity, 아래 §5).
- **bind Δ 의 정체(진단축):** comp/shuf 디코드 **둘 다 동일한 의도쌍 `MEASURED[i]` 에 대해** 채점.
  `comp_bind` = composed-frame 디코드가 의도쌍에 결합한 비율, `shuf_bind` = shuffled-frame(deranged)
  디코드가 **같은 의도쌍**에 결합한 비율. `bind Δ = comp_bind − shuf_bind` = 모델 출력이 실제
  표시된 프레임 내용을 추적하는 정도. 새 **per-decode 게이트**는 primary 측정 프레임(composed)의
  디코드에 `_g6_is_falsifiable ∧ topic_bound` 를 적용한다.

## 2. arm 점수 (per-seed)
```
FALS_bound(arm, seed) = Σ_{i=0..5} [ is_falsifiable(comp_texts[i]) ∧ topic_bound(comp_texts[i], MEASURED[i]) ]
```
`comp_texts` = 6 composed 측정 프레임의 engine-native(py mirror) 디코드, gen=80.

## 3. FROZEN threshold (재채점 전 고정)
- majority bar `MAJ = 4/6` — 기존 3-arm 결과의 `>=4/6` majority 관례와 동일.
- seed bar `NSEED = 2` — 기존 `on >=2 seeds` 관례와 동일.
- 분리 bar `MARGIN = 3.0` — `mean(FALS_bound|TARGETED) − mean(FALS_bound|SHUF) ≥ 3.0`.

## 4. 사전등록 PASS 조건 + 사전예측
```
P1 (BASE floor)          : #seeds{FALS_bound ≥ 4} == 0   for BASE
P2 (TARGETED signal)     : #seeds{FALS_bound ≥ 4} ≥ 2    for TARGETED
P3 (SHUF reject=form-prim): #seeds{FALS_bound ≥ 4} == 0  for SHUF
P4 (separation)          : mean_FB(TARGETED) − mean_FB(SHUF) ≥ 3.0
PASS = P1 ∧ P2 ∧ P3 ∧ P4
```
**핵심:** P3 는 기존 FORM-only FALS 게이트가 **낼 수 없던** 조건 — 기존 게이트는 SHUF=6/6 → P3 자동 실패.
새 게이트가 P3 를 통과하면 = bind 항이 진짜 재조합 신호를 잡고 form-priming 을 걸러냄을 입증.

**사전예측 (측정 전):**
- (예측 A, PASS) 새 게이트가 TARGETED ≫ SHUF 로 벌리면(SHUF FALS_bound 낮음) = 진짜 재조합 신호
  포착 = FALS 가 못한 것. **분기 = 이것.**
- (예측 B, 정제 필요) TARGETED ≈ SHUF (SHUF 도 4/6+ 결합) 이면 = topic-bind 항도 form 에 오염
  → keyword-set 정제(다의어 제거·purity 규칙 강화) 후 재측정.

## 5. 사전예측 검증 결과 (frozen fragment 재채점, 재학습 0 · DIRECTIONAL)
`g6_bind_gate.py` → `rescore.json`. **fragment 는 이 게이트가 존재하기 전 summer 가 생성** →
게이트에 맞춰 튜닝 불가(모델 출력 고정) = 정직 보장.

| arm | frozen FALS/6 (per seed) | **새 FALS_bound/6** (recall) | strict/6 (purity) | n_maj(≥4) | mean |
|---|---|---|---|---|---|
| BASE     | [0,0,0] | **[0,0,0]** | [0,0,0] | 0 | 0.00 |
| TARGETED | [6,6,6] | **[5,6,6]** | [5,5,5] | 3 | 5.67 |
| SHUF     | [6,6,6] | **[1,0,0]** | [1,0,0] | 0 | 0.33 |

- **판정 = PASS (예측 A 실현).** P1∧P2∧P3∧P4 전부 참. 분리 = 5.67 − 0.33 = 5.33 ≥ 3.0.
- **faithfulness (18/18):** recall `topic_bound` 이 results json 의 comp_bind·shuf_bind 를 오차 0 재현
  (`validate` = {BASE:True, TARGETED:True, SHUF:True}); frozen FALS 항도 arm 보고값과 일치;
  10-string 캘리브레이션 10/10.
- **strict(purity) 변종도 동일 PASS** — TARGETED 만 5/6 로 소폭 감점(off-frame 누출 프레임), SHUF/BASE 불변.
  → 규칙 강화에 robust; 기본은 recall(reference-match).

## 6. 정직 스코프 (c9 · a_engine_native_learning)
- 이건 **검출기 개선**이지 G6 벽 재정의 **아님**. 기존 G6 FALS 결과(form-priming 취약)는 그대로 유효.
- 재채점 = **torch-free py mirror** fragment 위 → `a_engine_native_learning` 상 **DIRECTIONAL**
  (terminal 아님). fragment 자체가 summer 의 `bytegpt_decode_topk_sampled_W` numpy mirror(session-eval-py-only).
- **terminal 승격 경로:** 새 게이트를 live `core/g6_ideation.hexa` 에 배선 후 CORE(`.hexa` A⇄G)로
  6 composed 프레임 재디코드 → byte-exact 재채점(GPU/pool 필요). 그 전까지 verdict = DIRECTIONAL.
- verdict 는 별도 카드(H_new, 로컬 메인이 등록) — 이 세션은 설계+py+pre-reg+재채점(DIRECTIONAL)까지.
