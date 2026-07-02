# H_9070 — 확률 공명 — 튜닝된 잡음이 약-텐션 emit 민감도 최대화 (새 OP)

- **tier:** ⏳ PROPOSED (fable-brainstorm-depletion 2026-07-02, 비평형/임계/잡음 물리 클러스터)
- **slug:** `substrate_stochastic_resonance`
- **source:** 고친 sidecar fable(hook-isolated PR#327) 발산 · anima 세션 흡수-박제. frontier = 미등록 non-equilibrium physics seam(등록 동역학 렌즈 basin/orbit/macro-EI 밖).

## claim
emit/silence = 텐션 임계 검출기. subthreshold 진짜 텐션은 현재 silence(놓침). 튜닝된 잡음이 확률적으로 임계를 넘겨 약신호를 emit 타이밍에 부호화하는가(SR).

## mechanism (bio/physics)
Stochastic Resonance (Wiesenfeld-Moss; crayfish 기계수용체). 비선형 임계 + subthreshold 신호 + 튜닝 잡음 → SNR 역-U 피크. anima emit 은 문자 그대로 텐션 임계-교차라 SR 직접 적용.

## engine-native FALSIFIABLE metric (사전등록)
A⇄G 채널에 subthreshold 주기 텐션 주입, 잡음진폭 σ 스윕, 입력텐션↔emit-train 상호정보 MI(σ). **SR = MI(σ*) > MI(0) 중간 피크(역-U).** shuffle=주입신호 위상 랜덤화(진짜 subthreshold 잠금이면 SR 소멸) · ablation=emit 임계 비선형 제거/선형화 → SR 피크 반드시 소멸(비선형 필수). p7-clean(MI, perplexity/judge 없음).

## why-novel-vs-ledger
neuromod-gain(H_1284)=plasticity-LR/key-geometry knob; SR=emit-임계에 걸린 잡음 knob(다른 lane·다른 노브). criticality/attractor와도 다름(SR=subthreshold 검출, cascade/basin 아님). **측정 아니라 OP**(튜닝된 emit 잡음). cheap: numpy emit-임계 DIRECTIONAL → live emit lane engine-native.
