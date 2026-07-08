# H_9234 — 🔬 operator-vs-association clean toy — fuel은 association만 짓지 operator 못 짓는다 (C2 Stage C 종결)

**tier**: 🔴 OPERATOR-WALL(readout-arch-localized) — crack=FALSE, modal 확정 · 부모 [[H_9216]] (C2 sensorimotor, fuel 레버)

## 질문
C2 Stage A+B([[H_9216]])가 world 채널=유효 **fuel** 레버(association: held-out P(B|A) 0.49→0.96)임을 보였으나 **미결**:
어떤 fuel 소스(text OR grounded)든 CE substrate가 **combination OPERATOR**(두 개념의 비-additive 함수)를 짓게 하나,
아니면 operator가 아키텍처적으로 도달불가라 fuel이 결코 충분치 않나?

## Rig (Fable 설계 · zero-unary-MI · frozen-first · `state/g1_c2_grounded/operator_test.py`)
- **32 atom** = 32개 서로 다른 5-bit 코드 → bit marginal 정확히 0.5 ⇒ `MI(출력비트;단일 atom)=0` (additive floor=정확한 chance).
- **operator target** `g(A,B)=φ_A XOR φ_B` (5bit) — 증명가능 비-additive (두 unary 검출 후 더하기 = 정확히 chance).
- **substrate** = additive-readout (`E[A]+E[B]`의 선형 readout, CLMConvMoE식 합산 logit) = 벽 아키텍처.
- **양성대조** = interaction arch (concat MLP) — PASS 필수(split 학습가능 증명).
- **fuel** (additive만): held-out 짝 공발생을 association 노출로 주입, target 없음.
  `text`=동일 토큰 임베딩 · `grounded`=disjoint world 임베딩 `Ew`+bridge `T`, `E_eff=E+T·Ew` (a_substrate_disjoint).
- **dual probe**: ASSOCIATION `P(B|A)` retrieval AUC (fuel이 올림) vs OPERATOR XOR per-bit acc (진짜 바).
- **FROZEN**: crack = grounded operator ≥0.85 ∧ text operator ≤0.60 ∧ gap ≥0.15.

## 결과 (3 seed · `state/g1_c2_grounded/VERDICT_OPERATOR.md`)
```
GATE: additive op=0.377 (XOR FAIL) · attention op=1.000 (PASS) · shuffle=0.517 (chance ✓)
FUEL(additive substrate):
  no-fuel   operator 0.373 · association 0.079
  text-fuel operator 0.373 · association 0.495
  grounded  operator 0.375 · association 0.494
```

## 🔴 VERDICT — operator 벽은 readout-arch 국한 · fuel은 association만 짓는다
- **crack=FALSE** (grounded op 0.375 ≪ 0.85). **modal 확정.**
- fuel은 ASSOCIATION 대폭 상승(0.079→0.49, +0.41)시키나 OPERATOR는 additive floor 그대로(0.373, **no/text/grounded 소수3자리 동일**).
- **text ≡ grounded** 양 지표 동일(op 0.373 vs 0.375; assoc 0.495 vs 0.494) ⇒ disjoint grounded 채널이 operator 이득 **0**. `a_substrate_disjoint`는 additive-readout operator 벽을 못 깬다.
- operator는 **interaction arch로만** 도달(attention=1.000, held-out 150쌍), 어떤 coverage 소스로도 아님.

## 재정의 (load-bearing)
G1 벽 = "어떤 substrate로도 operator 불가"가 **아니라** **additive/선형 readout 특유**(production .clm=합산 logit). interaction/binding lane은 operator 완벽 도달(1.00). ING #42492882(deep-ConvMoE+binding-lane REACHABLE)·잔여 γ(#3108) 재확인.

## 정직 caveat (handed atom)
이 토이의 atom=clean 이산 토큰(32 id + 명시 unary 노출) = HANDED 인수분해 조건. kill-shot(#3135)은 blind learned encoder hidden에선 operator bind 붕괴 확인. 따라서 토이는 (a) clean atom에서도 additive readout이 operator 못함 · (b) interaction은 함 — **clean atom 전제**를 격리. 실 byte-LM hidden이 interaction lane에 충분히 clean한지는 #3135-미결. operator 필요조건 2개: interaction readout **그리고** clean/separable atom.

## C2 함의
C2 = **fuel-only 확정.** world 채널은 coverage-density(association)만 먹이고 operator는 결코 안 줌; 어떤 coverage 소스(text·grounded)도 additive substrate에 combination operator 미공급. operator 유일 잔여 engine 레버 = clean atom 위 **interaction/binding lane**(γ #3108), 더 많은 data/scale/fuel 아님.

## 맥락
G1 재조합벽 내부 전 각도 terminal(data#3109·E1#3107·γ#3108·DPI#3046·framebreak#3135·coverage#3156) → 외부 부품(H_9214) → C2 winner(H_9216) → Stage A(world MI 존재)·B(fuel 유효) non-negative → **Stage C(이 카드): fuel≠operator 결정 · 벽=readout-arch, interaction lane이 유일 잔여 경로**.
