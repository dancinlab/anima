# H_9724 — seed-취약(0.99/0.50)의 진원 국소화($0 인과수술) — Bridge Seed-Chimera Localization (EA-6 · sol §6(NOVEL·$0) · EA 시리즈 · PROPOSED)

**status:** 🔵 PROPOSED (미실행 · lab full 창발-주소 발산 · 사전등록) — source=EA-6 · sol §6(NOVEL·$0)
**lane:** 재조합/BINDING · 창발-주소(감독 없이 주소가 서는가)
**related:** [[H_9672]] · [[H_9423]] · [[H_9684]] · [[H_9683]] · source: lab full EA(Fable 5 ∥ Codex Sol · 창발-주소 whitespace)

> **admissibility rule (Sol · 이 시리즈 전체의 관문)**: 어떤 개입도 `target_slot`·slot 정답·**거기서 파생된 어떤 통계**도 소비하지 않아야 emergent-address-valid. 최종 PASS 는 end-task-only 학습 · held-out 개체 · wrong-store 인과 · seed-robust 를 요구 — **sharp attention 만으론 부족**.

**아이디어(Sol 고유 · $0 · 기존 ckpt 만)**: T3 의 **ORACLE 0.99(seed-7) vs 0.50(seed-11)** 분열이 **빠진 부트스트랩 원천을 국소화**할 수 있다 — `val`/readout 을 교환했을 때 성공이 **robust 한 W_q 와 독립으로** 전이되면, 진짜 씨앗 균열은 **주소 capacity 가 아니라 값 조직화**다.
**메커니즘**: `anima-py evaluate --store-component-swap {val,readout,wq,trunk} --from-seed A --to-seed B` — 기존 seed-7/11 ckpt 에 **평가 전용 인과수술**(oracle·학습 attention 양쪽서 평가).
**$0 pre-screen**: **완전 상호 component-swap 행렬**(val+readout 동시교환 포함) · 실패가 비전이거나 bridge 전체를 바꿔야만 되면 KILL.
**판정**: 통제 = 같은-seed **sham swap**(POS-validity) · 성공 bridge 전체를 실패 trunk 에(POS-upper-bound) · 무작위 매칭 텐서(NEG). **PASS-localization** = 상호 swap 이 ORACLE 성능을 **Δ≥0.40** 으로 전이 ∧ addr_mass 는 **±0.03 내** 유지. KILL-localization = W_q/trunk 가 지배하거나 swap 이 비호환으로 깨짐. **이후 어떤 창발 주장도 EA-1/2/4/5 의 ≥3-seed end-CE 시험을 여전히 요구**.
**distinct**: 가장 가까운 kill = oracle 학습·addr-loss. **이건 평가-전용 인과수술** — **학습신호 0 · 주소 설치 0**. H_9690(RV-0 $0 trailer autopsy)은 end-state 해부고 이건 **상호 chimera 전이**.
**verdict-integrity**: chimera 는 **off-manifold 가능** — sham 과 full-bridge 통제가 **작동해야만** 실패가 해석가능 · 성공은 **호환성을 국소화**하지 창발이 아님(Sol 자기명시).

## 상태
🔵 PROPOSED — 미실행 사전등록. 측정 주장 0(설계). **distinct-from-kills:** oracle 학습/addr-loss 아님=평가 전용·학습신호 0·주소 설치 0 · H_9690 end-state autopsy 와 달리 상호 chimera 전이
