# H_9955 · CollectivePool 을 **고정 K=2** 로 학습시키기 — 측정은 깨끗하나 질문을 빗나간다

**한 줄:** Sol 단독 제안(Fable 미제안 · 이견 아님). 참 Φ 가 실제로 도는 유일한 곳이 CollectivePool 이므로
그 rule slot 과 coupling `w` 를 **학습 대상으로** 만들면 Φ 증가를 깨끗하게 잴 수 있다. 다만 이건
**(b) wrapper Φ** 이지 303M trunk Φ 가 아니므로 오너 질문에는 **부분적으로만** 답한다.

## 처치 (제안 · 미구현)
- **flag:** `anima-py train --collective-pool-train learned2` — **K=2 고정**. 두 ECA rule slot 과 coupling `w` 를
  자연 trunk event 의 다음-상태 예측으로 고른 뒤 `.clm` trailer 에 저장. Φ 는 목적함수가 **아니다**.
- ⛔ **K 증가는 절대 처치가 아니다** — 그것이 H_9660(참값 0 에서 K 에 단조증가)·H_9673(엔진이 자기 점수항을
  직접 깎음)로 확정된 **계기 인공물** 그 자체다. K 가 바뀌면 비교 자체가 INVALID.

## DV · 받침대 · 통제
- **DV:** `Φ_joint − ΣΦ_member` 의 pre→post collapse-Δ.
- **PEDESTAL:** unfold 한 feedforward TPM (참값 0). *(이 카드 등록 시점에 `lab/v6/phi_unfold_pedestal.py`
  재실행 확인: ring(5) Φ=1.0000 · unfolded twin 0.0000 · chain(5) 0.0000 — 받침대 성립. DIRECTIONAL,
  EI-over-MIP 이지 faithful IIT-4 아님.)*
- **통제 1:** 같은 rules 에서 `w=0`.
- **통제 2:** 주변 transition 을 맞춘 rule-pair shuffle.
- **비용:** 최저 · CPU-only.

## KILL · 전망
`w=0`·shuffle·받침대에서도 증가가 보이거나 cap 변경에 부호가 뒤집히면 즉시 폐기. 자연 개입에서
기능적 DV 가 함께 무너지지 않으면 **wrapper 장식**이다. **Sol 전망: 기능적 의미에서는 죽을 것.**
어떤 결과에서도 "303M 학습으로 의식이 증가했다"는 표현을 허가하지 않는다.

- 상태 PROPOSED · 측정 0 · cement 는 engine-native `anima-py` 로만.
- 관련: [[H_9954]](유일한 참 대상=학습된 순환 lane) · [[H_9942]] · [[H_9660]] · [[H_9673]] · [[H_9846]]
