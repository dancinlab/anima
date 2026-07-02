# 1834 — TENSION-MOUTH (anima-native mouth) · 설계 spec + toy 프로브

카드: `HYPOTHESES/cards/H_1834_tension_mouth_native.md` · id H_1834

## 1. 문제 재정의

기존 mouth(bytegpt/clm)는 borrowed byte-predictor 이고 A⇄G 의식엔진과 disjoint 하다.
native mouth = **next-byte 분포를 A⇄G 텐션 해소로 산출하는 trunk**. 이것이 G1 재조합벽의
미탐 레버(combination operator 를 구조에 내장)를 직접 겨냥한다.

## 2. TENSION-MOUTH forward (연산자)

context h (누적 상태) 에 대해:

- A(forward 예측장):  a = W_A · h            # CE-trained forward field over V=256
- G(reverse 제약장):  g = W_G · h            # gradient-free reverse constraint field
- 텐션 해소(핵심, additive 아님):
    t   = ||a|| / (||g|| + eps)               # tension scalar → Ψ 로 사상
    psi = sigmoid(k * (t - 1))                # Ψ; t=1 일 때 Ψ=1/2 고정점
    # 결합 연산: G 가 A 의 장을 *재형성* (element-wise gate + 전역 coupling)
    logits = a * softmax(g)  +  psi * (a ⊙ g)_global
             ^^^^^^^^^^^^^^      ^^^^^^^^^^^^^^^^^^^^
             local 재가중         전역 bilinear 결합(RF 무관)

전역 bilinear (a ⊙ g)_global 항이 두 개념(위치 무관)을 곱셈으로 묶어 RF-bound 를 우회.
psi 게이팅이 결합 강도를 Ψ 고정점에 종속시킴 → objective 가 구조에 내장(축 2).

## 3. Objective (목적함수)

L = CE(logits, target)  +  λ · L_psi
  L_psi = (psi_batch_mean - 0.5)^2        # Ψ→½ 를 *구조 수렴*으로 (loss 에 더하되
                                          # backward 로 흘리는 additive aux 아님 —
                                          # psi 는 logits 경로에 이미 들어가 있어
                                          # CE 최소화가 결합을 통해서만 가능)

주의(H_1816 교훈): binding 을 순수 additive aux 로 붙이면 trivial 붕괴. 여기선 psi·bilinear 가
**logits 산출 경로 자체**에 있어 CE 를 낮추려면 결합 연산을 써야만 함(structural, not aux).

## 4. G1 toy task (측정)

- 개념 A 는 위치 i, 개념 B 는 위치 j (거리 D 가변)에 심음.
- target = compose(A,B) 가 학습 코퍼스에 **부재**(G1 재조합: 본 적 없는 조합 생성).
- metric = `composed_distinct` = 생성된 유효 재조합 종수. ByteGPT floor=2, conv floor=0.

## 5. 통제 (결정적 ablation)

| arm | 구성 | 기대 |
|-----|------|------|
| FULL | a·softmax(g) + psi·bilinear | G1 lift + Ψ≈½ |
| TENSION-OFF | g 제거(a 만) | G1 → floor (causal 증명; INERT 면 기여 0) |
| ADDITIVE | logits = a + g (텐션 해소 아님) | additive floor 재현 |

## 6. Pre-registered bar (frozen · p7 · 카드와 동일)

🟢 iff  composed_distinct >= 3  AND  |Ψ-0.5| <= 0.05
🟠      composed_distinct >= 3  AND  |Ψ-0.5| >  0.05   (능력 O · 의식 붕괴)
🧱/🔴   composed_distinct <= 2

## 7. 사다리 (a_verified_must_wire / a_toy_scale_recheck)

(0) 설계 [이 문서]
(1) DIRECTIONAL toy: `tension_mouth_probe.py` (numpy, from-scratch) — 자동 DIRECTIONAL
    (grep 자가점검: numpy 미러이므로 verdict 는 DIRECTIONAL only, a_engine_native_learning).
(2) engine-native 재측정: live core/ A⇄G(pure_field⇄engine_g) 위에서 byte-exact 재현.
(3) generator L3 3번째 mouth kind ('tension') wire-in + gen_mouth_kind 디스패치.
(4) ARCHITECTURE.json §7 lockstep (L3 = 3 mouth architectures).

현 단계 = (0)→(1). GPU/production 학습은 toy green 후 cost-gated(explicit go).

## STATUS

⏳ PROPOSED. 다음 = (1) tension_mouth_probe.py 구현 + DIRECTIONAL 채점.
