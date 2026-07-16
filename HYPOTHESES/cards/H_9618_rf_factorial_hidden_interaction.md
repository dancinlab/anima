# H_9618 — RF 요인 hidden 상호작용 — RF Factorial Hidden Interaction ($0) (sol R3-S1 · R3 · PROPOSED)

**status:** 🔵 PROPOSED (미실행 · lab full 고갈-발산 R3 post-GroupNorm · 사전등록) — source=sol R3-S1
**lane:** BINDING / within-RF latent binding
**related:** [[H_9615]] · [[H_9562]] · [[H_9619]] · source: lab full R3 (sol R3-S1)

**아이디어**: 동결 303M trunk 가 **이미** within-RF key×value 상호작용을 갖고 있다(현 byte readout 이 무시할지언정).
**메커니즘**: $0 `anima-py evaluate --dump-hidden` on 균형 **2×2×2** 매니페스트: key match/mismatch × 선언 극성 ± × D≤20/D≥64. 무접촉 연산자 결정위치서 held-out 상호작용 대비 `[h_match,+ − h_match,−] − [h_mismatch,+ − h_mismatch,−]` (Cartesian-held-out stem/템플릿).
**$0 pre-screen**: byte 길이 불균등·질의 offset 상이·marginal byte 누수·stem×템플릿 중복 매니페스트 기각 · 결정적 dump parity 요구.
**판정표**: PASS = inside-RF 상호작용 norm ∧ 교차검증 극성 디코딩이 **label-permutation 과 outside-RF arm 둘 다** 초과(동결 문턱) · 양성통제=exact 반복key/local-copy. **KILL-latent** = 양성통제는 통과하나 상호작용이 mismatch·outside arm 과 TOST-등가. 통제: D≥64 · wrong-key 선언 · 극성-shuffled 선언 · 양성 exact-key.
**distinct**: 死한 margin/2AFC RF probe 와 달리 DV 가 **요인 hidden-state 상호작용**(미훈련 출력 연관 아님) · H_9562 와 달리 **CPT 0**.
**verdict-integrity**: PASS 는 *이미 존재하는 latent 상호작용*이지 상징 dereference·행동 binding 아님. KILL 은 "이 ckpt/tap 에 latent 아님"이지 **"학습불가" 절대 아님**.

## 상태
🔵 PROPOSED — 미실행 사전등록. run 시 위 판정표로. 측정 주장 0(설계). **distinct-from-kills:** margin/2AFC kill 아님(DV=요인 hidden 상호작용) · H_9562 와 달리 CPT 0 · H_9615 의 요인 변형(교차수렴).
