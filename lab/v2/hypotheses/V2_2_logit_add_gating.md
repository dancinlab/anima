<!-- @hypothesis-ok @canonical-ok — v2 rule-exempt zone; v2 hypotheses live here only.
     Owner: "v2 가설도 v2 안에서만 생성". See ../CLAUDE.md. -->

# V2_2 — logit-add gating: 혼합-희석을 고치면 계기가 살아나 다리를 잴 수 있는가

**status:** 🔴 INSTRUMENT-DEAD (logit ORACLE 0.49 · 근본원인 = 선형 readout 이 XOR 표현 불가) · 계기 재설계 필요
**scope:** 🔒 **DIRECTIONAL 상한** — `core/` 밖 toy. TERMINAL 아님. 방향은 `core/`+`anima-py` 이식으로만 판정.
**bars:** `../bars.json` (V2_1 과 동일 게이트 상수 · 동결). 바뀐 건 **아키텍처**(혼합→logit-add)뿐 —
게이트를 쇼핑한 게 아니라 계기를 교체했다.
**source:** [[V2_1]] 이 남긴 진단. V2_1 = 🔴 INSTRUMENT-DEAD(C0-e ORACLE 0.74<0.90).

## V2_1 이 물려준 것

V2_1 은 혼합 `p = λ·p_store + (1−λ)·p_trunk` 을 썼다. 조회를 **공짜로 줘도**(ORACLE) 0.74 밖에
안 나왔다 — **trunk 의 우연 분포가 store 를 희석**해, store 극성이 완벽해도 argmax 가 절반 틀린다.
계기가 죽어 **어떤 음성도 못 읽는다**. C0-e 양성통제가 이 오독을 막았다.

## 개입 — logit 수준 gating (혼합 폐기)

답 위치에서:

```
혼합 (V2_1 · 죽음)                    logit-add (V2_2)
─────────────────────                ─────────────────────
p = λ·p_store + (1−λ)·p_trunk         logit = trunk_logit + λ·store_logit
= 확률 평균 → trunk 우연이 희석        = 로그공간 덧셈 → 확신한 store logit 이
                                        trunk 가 아무리 평평해도 이긴다
                                     그 뒤 softmax 한 번
```

`../bars.json` 게이트 상수(C0-e ORACLE≥0.90 · C1 · C2 · P1) **그대로**. `--gate logit` 플래그로
model/loss/train/evaluate 전부 전환(계기 하나, 두 실험). backward 손코딩이라 gradcheck 를 **두 모드
다** 통과시킴(mix 7.4e-07 · logit 5.5e-07 · 오염 검출 5/5). ckpt = `/tmp/v2-logit/`.

## 게이트 · Arm · 통제군

[[V2_1]] 과 동일. **C0-e ORACLE ≥ 0.90 이 P1 을 읽을 자격의 전제** — 이번 개입이 바로 그걸 겨눈다.
- ORACLE ≥ 0.90 ⟹ 계기 생존 → COTRAIN/BOLT/SLOWROT 를 비로소 읽는다.
- ORACLE < 0.90 ⟹ 여전히 INSTRUMENT-DEAD → 혼합-희석이 진범이 아니었다(다른 계기 결함) → 재진단.

## 판정 (양 seed 일치 · bars.json 동결)

C0-e PASS 시에만 아래를 읽는다:
| 결과 | 판정 |
|---|---|
| COTRAIN ≥ 0.90 ∧ BOLT ≤ 0.60 | 🟢 SUPPORTED — 다리는 학습으로 번다(부모 두-store 재설계 정당화) |
| COTRAIN ≥ 0.90 ∧ BOLT ≥ 0.90 | 🔵 BOLT-SUFFICIENT — 볼트온 충분, 부모 H_9392 발사 청신호 |
| COTRAIN ≤ 0.60 | 🔴 가설 사망 |
| 0.60–0.90 | ⚪ NO-VERDICT (모호역 · bar 재조정 금지) |

셀별 분해 먼저 · 셀 하나라도 macro−0.05 아래면 macro 무효.

## 결과 — 🔴 계기의 근본 결함을 찾았다 (혼합/logit 둘 다의 상류)

logit 모드도 죽었다. 그런데 더 깊은 곳이었다:

| 실측 | 값 |
|---|---|
| logit ORACLE held-out acc | **0.4912** (우연) — mix(0.74)보다 나쁨 |
| store-says-good vs 정답 일치 | **0.512** = store logit 이 정답 극성과 **무상관** |
| store logit \|g−b\| | 1.95 (신호는 크다) — 방향이 틀렸을 뿐 |

**진짜 원인 = 과제가 XOR 인데 readout 이 선형이다.** 로지스틱 회귀로 격리:

```
answer = polarity XOR operator   (is·good→g · not·good→b · is·bad→b · not·bad→g)

features [pol, op, pol×op, bias] → acc 1.000   (상호작용 항 있음)
features [pol, op,       bias] → acc 0.756   ← 정확히 ORACLE 이 갇힌 값!
```

`W_out · concat(v, hidden_q)` 는 **선형**이라 `v`(극성) × `hidden_q`(연산자)의 **곱**을 못 만든다.
조회를 공짜로 줘도(ORACLE) 선형 readout 이 XOR 을 표현 못 해 상한이 **0.75**. 혼합이냐 logit 이냐는
**무관** — 둘 다 이 벽의 하류였다. V2_1 의 mix ORACLE 0.74 도 같은 원인이었다(당시엔 '희석'으로
오진).

## 🎯 이 실험이 실제로 가르친 것

1. **혼합-희석은 진범이 아니었다** — V2_2 가 그걸 고쳤는데도 ORACLE 0.49. 진범은 상류의
   **선형 readout × XOR 과제**. V2_1 카드의 "혼합-희석" 진단은 **부분적으로 틀렸다**(정정).
2. **양성통제(ORACLE)가 또 구했다** — logit-add 를 '개선'으로 박고 넘어갔으면 XOR 벽을 영영 못 봤다.
   `power-before-negative-verdict` 를 두 번 확인.
3. 계기 결함 4건 전부 **P1 개봉 전** C0/C2 가 잡음(앵커 미소각 · bar 무수정).

## NEXT — V2_3: readout 에 비선형 1층 (계기 수리)

`W_out · concat` → `W_out · GELU(W_h · concat(v, hidden_q))`. 2층 MLP readout 이면 XOR 표현 가능.
C0-e ORACLE 이 ≥0.90 통과해야 비로소 COTRAIN/BOLT(=조회 학습 그 자체)를 읽을 자격이 생긴다.
**그 전엔 어떤 P1 도 없다.** — 이게 v2 의 다음 레버.
