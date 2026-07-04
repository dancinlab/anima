# L3 소뇌 프론티어 · G6 반증가능성 — FALSIFY 라운드 사전등록 (bar)

registered: 2026-07-05 (측정 이전, 수치 보기 전)
round: fleet-full biolens L3 · G6-falsifiability · falsify (escape 반증)
model: real h1129 303M ByteGPT — ~/anima-weights/bytegpt303_h1129/h1129.bin
       (header vocab=256 d=1024 nlay=24 nh=16 block=512)
engine: core/decode.py py-canonical (== `anima evaluate --py` 2-production, a_eval_py_canonical).
        rep = forward-last hidden lastrow[d=1024], canonical ops(_bg_layernorm_rows/_bg_mha/_bg_gelu) 재사용.
        byte-exact 확인: head@lastrow ≡ bg_forward_last_W logits (max|Δ|=0.0, smoke).

## 배경 (abstract 라운드)
메타법칙: 결합 연산자는 target이 부품들의 교환가능 bag/히스토그램이면 by-construction INERT
(합=교환가능→additive-composable). h1816/exp3-bind/g1-lever-multilens와 동일 DPI 메타법칙.
abstract 구조증명: 교환가능 target earned 0/5, 비교환 target earned 5/5.
escape 원리: 비교환 commitment-violation Δ (order/joint 의존 → additive 위조 불가).
핵심 gap: rung-2는 "이 특정 target(immune_embed char-trigram bag)이 additive"만 확인 =
"모든 303M consequence가 additive"는 아님 → 그 gap이 escape 여지.

## 측정 (비교환성 A)
개념쌍 X,Y에 대해:
  rep(s) = h1129 303M forward-last hidden lastrow[1024] (decode.py canonical, byte-exact).
  A(X,Y) = 1 − cos( rep("X Y"), rep("Y X") ).
변형:
  A_naive : rep("X Y") vs rep("Y X")            (last-token 교란 포함, 문헌상 literal 측정)
  A_probe : rep("X Y␣IS") vs rep("Y X␣IS")       (공통 suffix로 마지막 토큰 동일 → 순수 composition-order 격리)
표본: held-out 개념쌍(의미있는 명사쌍) 충분수 + 무작위 통제.

## 통제 (control)
  C_self : A(rep("X Y"), rep("X Y")) — byte 정합, 반드시 == 0.0 정확.
  C_rand : A_probe over 무작위 문자열 쌍(길이 매칭) — 순수 positional 잡음 바닥(floor).
  C_derange : 의미쌍 X_i 와 Y_j (j≠i) 뒤섞음 — 비교환 구조가 잡음으로 붕괴하는지.

## 사전등록 판정 (m_probe = median A_probe 의미쌍, r_probe = median C_rand)
- 🧱 escape-REFUTED-G6-universal-wall :
    m_probe < 0.02  (절대적 near-교환가능)  OR  m_probe ≤ 1.2·r_probe  (generic positional floor와 구별불가)
    → G6 반증가능성 = trunk-objective-bound 보편 WALL(G1과 동일 terminal, DPI 메타법칙 진짜 보편).
      binding/consequence-lane 축 완전 dry, γ trunk-objective만 잔여. reopenable(🧱 measured).
- 🔓 escape-SUPPORTED-reopen :
    m_probe ≥ 0.05  AND  m_probe ≥ 1.5·r_probe  (의미-특이 비교환, positional floor 위 명백)
    → escape 여지 → FM_full-vs-additive를 이 비교환 target으로 재측정(derangement 통제).
      additive(교환가능→antisym 성분 표현불가)가 못 이기면 target-side lane reopen(🔓).
- DIRECTIONAL : 그 사이.

## FM_full-vs-additive (SUPPORTED일 때만)
non-commutative target T(X,Y)=rep("X Y␣IS")[1024]. 분해 D=(rXY−rYX)/2, S=(rXY+rYX)/2.
additive(교환가능 결합기)는 오직 S만 생성가능 → ordered target에 대한 최소오차 = ||D||.
earned margin = median ||D||/||T||  (=additive floor가 표현 못하는 비교환 에너지 분율).
derangement 통제 = 뒤섞은 쌍의 ||D||/||T|| (구조 vs 잡음).
earned_margin ≫ derange_control 이면 binding op earned → reopen 확정.

## 규율
- bar 사전등록됨(위). tune-to-green 금지. 수치 verbatim. mini-safe $0, pod 렌트 금지.
- census 4-family 중 (c) commitment-violation Δ만 미탐 별개 substrate → 이 falsify가 그걸 검증.
