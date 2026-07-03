# G6 bind-gate — form-priming 내성 additive G6 검출기 (설계)

## 왜 (결함)
`state/g6_targeted_corpus/` 의 3-arm engine-native warm-FT 결과가 frozen G6 검출기
`_g6_is_falsifiable`(comparator ∧ measurable ∧ ≥2 content)의 **FORM-only 취약점**을 드러냈다:

| arm | frozen FALS/6 | bind Δ(comp−shuf) | 해석 |
|---|---|---|---|
| BASE (h1129 no-FT) | [0,0,0] | 0.111 | 형태·결합 둘 다 없음 |
| TARGETED (broad+g6) | [6,6,6] | 0.444 | 형태 ∧ **주제결합** |
| SHUF (broad+g6_shuf) | [6,6,6] | **0.000** | 형태만 (주제결합 파괴) |

**SHUF 는 주제-bind 만 파괴한 통제 코퍼스인데도 FALS 6/6 통과** = 반증가능 "형태"만 style-FT
로 암기하면 primary 게이트를 게임할 수 있다. 진짜 재조합 신호는 **bind Δ**(TARGETED 0.444 vs
SHUF 0.000)에 있으나 frozen FALS 는 그걸 못 잰다.

## 무엇 (설계)
frozen 게이트를 한 글자도 안 건드리고, 그 위에 **bind 항을 AND 로 얹은 새 게이트**:
```
is_falsifiable_topic_bound(text, frame_ab)  =  _g6_is_falsifiable(text)   ← frozen, 미터치
                                               AND topic_bound(text, frame_ab)   ← 새 항
```
- `_g6_is_falsifiable` = `core/g6_ideation.hexa` 의 **VERBATIM 미러**(reference copy, 수정 금지).
- `topic_bound(text,{a,b}) = concept_hits(text) ∩ {a,b} ≠ ∅` (RECALL)
  = 디코드가 프레임의 실제 주제쌍(gate concept) 중 ≥1을 `gauge_lib.CONCEPTS` keyword-set 으로 호출.
- 측정 프레임쌍 `MEASURED = g6_build_frames(6)` composed = `[(0,1),(1,2),(2,3),(3,4),(4,0),(0,2)]`.

## form-priming 내성 논리
- SHUF 모델은 반증가능 **형태**를 암기했지만(FALS=6/6), 프레임이 지정한 **실제 주제쌍**에는
  결합하지 않는다(comp_bind ≈ 0). 새 게이트의 topic-bind 항이 `concept_hits ∩ {a,b} = ∅` 을
  잡아내 → **FALS_bound(SHUF) = [1,0,0]** 로 붕괴. 형태-암기 우회가 막힌다.
- TARGETED 모델은 형태 ∧ 주제결합 둘 다 → **FALS_bound = [5,6,6]** 유지.
- BASE 는 형태 자체가 없어 FALS 항에서 이미 0 → **[0,0,0]**.
- 결과: 새 게이트가 세 arm 을 **BASE 낮음 ∧ TARGETED 높음 ∧ SHUF 낮음** 으로 분리
  (frozen FALS 는 TARGETED=SHUF=6 으로 구별 불가). → PREREG PASS.

## 기존 FALS 와의 차이
| | frozen `_g6_is_falsifiable` | 새 `is_falsifiable_topic_bound` |
|---|---|---|
| 검사 | 형태(comparator∧measurable∧content) | 형태 **AND** 프레임-주제 결합 |
| SHUF (form-priming) | 6/6 통과 (게임됨) | ≤1/6 (걸러짐) |
| TARGETED | 6/6 | 5~6/6 |
| BASE | 0/6 | 0/6 |
| frozen bar 영향 | — | **없음** (frozen 항 그대로 AND) |

## reference-match / faithfulness
- bind 규칙(recall)은 임의 선택이 아니라 `state/g6_targeted_corpus/results/*.json` 의 per-seed
  `comp_bind`/`shuf_bind` **18값을 오차 0 재현**(reverse-engineer + 검증). `g6_bind_gate.py::validate`.
- frozen FALS 미러도 arm 보고 fals 값 및 10-string 캘리브레이션(10/10)과 일치.

## 재채점 프로토콜 (재학습 0)
- 입력 = `state/g6_targeted_corpus/results/{base,targeted,shuf}.json` 의 `per_seed[*].comp_texts`
  (6 composed 측정 프레임의 gen=80 디코드 — **fragment 가 이미 json 에 담겨 있어 재디코드 불필요**).
- `python3 state/g6_bind_gate/g6_bind_gate.py` → `rescore.json` (수치 + PASS 판정).
- torch/numpy 미사용, 결정적. GPU/warm-FT 불필요.

## 정직 스코프
- **DIRECTIONAL** — py mirror fragment 재채점. terminal 아님(`a_engine_native_learning`).
- fragment 자체가 summer `bytegpt_decode_topk_sampled_W` numpy mirror(session-eval-py-only).
- **검출기 개선**이지 G6 벽 재정의 아님 — 기존 G6 FALS(form-priming) 결과 그대로 유효.

## core/ 배선 권고 (frozen 보존, additive)
자세히는 상위 보고 (e) 참조. 요지:
- `core/g6_ideation.hexa` 에 `_g6_is_falsifiable` **옆에** `_g6_topic_bound(text, a, b, known)` +
  `_g6_is_falsifiable_topic_bound(...)` 를 **새 fn 으로 추가**(기존 fn 미터치).
- `g6_score_arm` 에 `frame_pairs` 인자(측정 프레임의 `MEASURED` 인덱스쌍)를 받아 `fals` 옆에
  `fals_bound` 를 병기 리턴 — 기존 `fals` 출력은 그대로 유지(회귀 0).
- concept keyword-set 은 `gauge_lib.CONCEPTS` kw 를 hexa Map 으로 포트(이미 `_g6_concepts` 문장은 존재).

## 파일
- `g6_bind_gate.py` — 새 게이트 py 구현(frozen FALS 미러 + bind 항 + 재채점 드라이버).
- `PREREG.md` — frozen threshold · 사전예측 · 재채점 프로토콜 · 검증 결과.
- `rescore.json` — 3-arm 재채점 수치 + PASS 판정 (스크립트 산출).
