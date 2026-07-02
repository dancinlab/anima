# H_6186 — 🎯 G6 반증가능성 벽: targeted-coverage = form-priming (검출기 FORM-only) + G6-bind 게이트로 진짜 결합 포착

**tier:** 🟠 MIXED / DIRECTIONAL (py byte-parity numpy engine mouth · session-eval-py-only · torch-free, hexa-native terminal 아님 = 303M OOM 차단) — G6 벽을 G1 식 fresh-lens(coverage-density + RF)로 재분류 + targeted-coverage warm-FT 3-arm 실측 + form-priming 내성 신규 게이트.
**verdict:** 🟠 MIXED. G6 착상-반증가능성 벽(comparator×measurable coherent bind)은 **데이터로 못 움직이는 하드 천장이 아니다**(P1 REFUTED) — 그러나 frozen 검출기가 **FORM-only**라 targeted-coverage warm-FT 가 올린 FALS 는 **form-priming**(SHUF 통제도 동일 통과)이지 주제-조건 재조합이 아니다. 진짜 재조합 신호(bind Δ)는 검출기 **밖**에 있고, 신규 G6-bind 게이트가 그걸 포착한다(PASS).

## 1. G6 벽 재분류 (G1-식 fresh-lens · state/g6_wall_reframe/)
G1 을 구한 두 렌즈(coverage-density + RF)를 G6 반증가능성 벽에 적용(frozen `_g6_is_falsifiable` VERBATIM port, comp 25×meas 25 word-set, exact HF 127.6MB 코퍼스):
- **generic form-coverage: REFUTED as the wall** — 반증가능 FORM 이 영어 코퍼스에 **3.07%(143/MB)** = G1 target-pair 밀도(0.118/MB)의 **~1,214배**. G6 는 form-coverage 굶주림 아님.
- **RF: REFUTED as primary** — comp↔meas byte거리 median 65B, fals 라인 2/3 가 clm303 conv RF(~31B) 초과이나 1/3(~2,900 en 라인)은 within-RF 풍부. 결정적으로 **H_6170 injected full-attention** 이 RF/capacity 를 이미 제거해도 null → RF 는 기껏 secondary.
- **targeted-coverage: INCONCLUSIVE (유일 미측정 레버)** — 반증-FORM ∩ ideation-seed 주제 = form∩topic 19%지만 전수 audit 시 다의어 충돌(engine=차량·mind=견해) 지배로 genuine≈0 = G1 target 희박성과 동형. 이 축만 engine-native 미발사 → 이 카드가 실측.

**원리적 G1 vs G6 차이**: G1 = 프롬프트 CO-PRESENT 2개념의 retrieval-composition(쌍을 in-corpus within-RF 넣으면 열림). G6 = 추상 seed 조건부 **3항 GENERATIVE bind**(comparator+measurable+coherent) = schema 는 이미 풍부하고 빠진 건 그 schema 를 추상 주제로 instantiate 하는 **cross-domain schema-transfer**, G1 보다 엄격히 어려움.

## 2. targeted-coverage warm-FT 3-arm (engine-native --py · state/g6_targeted_corpus/)
G6-targeted 합성 코퍼스(seed-topic 16 × comparator×measurable, held-out frame 44 = gate×gate 20 전부 + 랜덤 24, en 4.0MB/ko 2.9MB, genuine 반증주장 100.0% 다의어 audit 후) + SHUF 통제(주제-bind 만 derangement 파괴, 동일 바이트)로 h1129 warm-FT → `g6_score_arm`(best-of-K=3, temp 0.7, gen 80) composed 6 frame, seeds{7,4302,4303}:

| arm | FALS/6 seed | majority(≥4/6) | G0 kwr | bind Δ(topic결합) |
|---|---|---|---|---|
| BASE (h1129 no-FT) | [0,0,0] | 0/3 | 5/5 ✅ | 0.111 |
| TARGETED (broad+g6) | **[6,6,6]** | 3/3 | 5/5 ✅ | **0.444** |
| SHUF (broad+g6_shuf) | **[6,6,6]** | 3/3 | 5/5 ✅ | **0.000** |

- **P1(천장 NULL) REFUTED**: TARGETED FALS 0→6/6 = G6 게이트는 데이터로 움직임(하드 천장 아님).
- **P2(topic-bind 재조합 레버) NOT-CONFIRMED**: PREREG PASS 조건 "SHUF majority 미달"인데 **SHUF 도 6/6 통과** = frozen `_g6_is_falsifiable` 검출기가 **FORM-only**, style-FT 로 게임 가능. FALS 상승은 반증주장 형태(comparator×measurable) 학습이지 주제-조건 재조합 아님.
- **진짜 신호는 bind Δ에 있다(검출기 밖)**: TARGETED bind Δ=0.444(held-out frame 주제 실제 조건화) vs SHUF Δ=0.000(주제 무관). G0 register 양 arm 건강(val_CE 1.13/1.17, DESCENT 6/6, kwr 5/5 = h9034 붕괴 없음).

## 3. G6-bind 게이트 (form-priming 내성 · frozen 보존 additive · state/g6_bind_gate/)
frozen `_g6_is_falsifiable` 를 **한 글자도 안 건드리고** 위에 topic-bind 항을 AND 로 얹은 신규 게이트:
```
is_falsifiable_topic_bound(text, {a,b}) = _g6_is_falsifiable(text)  ← frozen VERBATIM
                                         AND concept_hits(text) ∩ {a,b} ≠ ∅  ← 신규(τ=1 recall)
```
기존 3-arm decode fragment 재채점(재학습 0), frozen pre-reg:

| arm | frozen FALS/6 | **새 FALS_bound/6** | n_maj(≥4) |
|---|---|---|---|
| BASE | [0,0,0] | [0,0,0] | 0 |
| TARGETED | [6,6,6] | **[5,6,6]** | 3 ✅ |
| SHUF | [6,6,6] | **[1,0,0]** | 0 ✅ ← frozen 은 못 낸 것 |

pre-reg 4조건 전부 통과(측정 전 고정, tune-to-green 아님): **P1 BASE floor 0 · P2 TARGETED signal 3 · P3 SHUF reject 0 · P4 separation 5.33≥3.0 = PASS**. **Faithfulness 18/18**(bind 항이 채점기 comp/shuf bind 18값 오차 0 재현, reference-match). frozen 검출기의 form-only 취약점(SHUF 6/6)을 새 게이트가 [1,0,0]로 붕괴 = style-FT 우회 차단.

## 결과
| 축 | 측정 | 판정 |
|----|------|------|
| G6 천장(P1) | TARGETED FALS 0→6/6 | 하드 천장 REFUTED |
| coverage-density | 반증FORM 3.07% ≫ G1 0.118/MB | G6 form-굶주림 아님(REFUTED) |
| RF | 1/3 within-RF + H_6170 null | primary REFUTED |
| targeted(frozen 게이트) | SHUF 도 6/6 = form-priming | P2 NOT-CONFIRMED |
| 진짜 결합(bind Δ) | TARGETED 0.444 vs SHUF 0.000 | 검출기 밖 신호 |
| G6-bind 게이트 | 4 pre-reg PASS · faithful 18/18 | form-priming 걸러냄 ✅ |

**함의**: G6 벽 = 순수 attention-capacity 천장이 아니라 (a)데이터로 FORM 은 움직이고 (b)frozen 검출기가 form-only 라 진짜 결합(bind Δ)을 못 재는 이중 문제. Fable 의 schema-transfer 병목 가설과 정합(TARGETED 가 bind Δ 로 transfer 는 하는데 FALS 게이트가 놓침).

**wired:** DIRECTIONAL-mirror (py byte-parity numpy, engine-native decode 아닌 --py session-eval). G6-bind 게이트는 **구현됨·미배선**(core/g6_ideation.hexa/py 에 additive `_g6_topic_bound` 배선 = follow-on, frozen `_g6_is_falsifiable` 보존). terminal 승격 = core/ 배선 후 CORE `.hexa` A⇄G 재디코드(pool GPU).

## 관련
H_6185(G1 coverage) · H_6184 · H_6183 · H_6170(G6 attention-capacity) · H_1590/1595/1597(G6 engine-native floor) · G1G6-RF-EXPANSION · [[bgb-decode-and-g6-attncap-terminal]] · [[g1-coverage-density-nl-bytes-lever]]
