# H_9722 — 무작위 값-대비 부트스트랩(방정식 정면) — Random Value-Contrast Bootstrap (EA-4 · sol §1(NOVEL) · EA 시리즈 · PROPOSED)

**status:** 🔵 PROPOSED (미실행 · lab full 창발-주소 발산 · 사전등록) — source=EA-4 · sol §1(NOVEL)
**lane:** 재조합/BINDING · 창발-주소(감독 없이 주소가 서는가)
**related:** [[H_9672]] · [[H_9423]] · [[H_9684]] · [[H_9683]] · source: lab full EA(Fable 5 ∥ Codex Sol · 창발-주소 whitespace)

> **admissibility rule (Sol · 이 시리즈 전체의 관문)**: 어떤 개입도 `target_slot`·slot 정답·**거기서 파생된 어떤 통계**도 소비하지 않아야 emergent-address-valid. 최종 PASS 는 end-task-only 학습 · held-out 개체 · wrong-store 인과 · seed-robust 를 요구 — **sharp attention 만으론 부족**.

**아이디어(Sol 고유 · 방정식-수준 최직접 공격)**: 교착은 `∂a_i ∝ dv·val[pol_i]` 가 val 미분화 탓에 0 인 것 ⟹ **극성 값이 처음부터 측정가능하게 구별**되면 주소가 유용해지기 **전에** 주소 gradient 가 0 이 아니게 된다. **어느 slot 이 중요한지는 end task 가 여전히 스스로 발견**해야 함.
**메커니즘**: `--store-val-init contrast --store-val-init-scale {0.02,0.1,0.5}` — 무작위 단위 `u` 뽑아 `val[0]=+su`, `val[1]=-su`. **target-slot 입력 0 · 평범한 end CE 만**.
**$0 pre-screen**: 기존 사전학습 ckpt 의 step-0 배치서 gradient replay — 합성 contrast 스케일로 `||∇W_q||` 와 target-vs-nontarget advantage 가 iid-init 과 **TOST-등가면 KILL** · **query 개체를 순열해도 advantage 가 동등하면 KILL**(진짜 주소신호 아님).
**판정**: 통제 = 사전학습 iid(NEG) · scratch-d768 end-CE(POS-emergence) · addr-loss(POS-engineering). PASS = **≥3 사전학습 seed** 가 held-out P1-bal ≥0.90 ∧ addr_mass ≥0.90 ∧ wrong-store flip ≥0.90 **∧ 극성라벨 순열이 성능 파괴**. KILL = seed 성공 ≤1/3 이거나 target 정렬 없이 attention 만 sharp.
**distinct**: 가장 가까운 kill = 직접 주소감독. **이미 존재하는 두 극성 값을 초기화할 뿐 어떤 slot 도 식별 안 함** — 초기화가 질의된 slot 에 조건부면 H_9672 로 붕괴하므로 **드롭**(자기신고 규칙). H_9711(antisym val init)과 인접하나 그건 RV-adjunct 이고 이건 **contrast 스케일 dose + gradient-replay $0 게이트**가 본체.
**verdict-integrity**: 성공은 "**target-free 값 대비 후 end-CE 가 주소를 고를 수 있다**"를 증명하지 **원래 사전학습 초기화로부터의 자발적 창발은 증명 안 함**(Sol 자기명시).

## 상태
🔵 PROPOSED — 미실행 사전등록. 측정 주장 0(설계). **distinct-from-kills:** 직접 주소감독 아님(두 극성 값 init 만·slot 식별 0) · H_9711 인접하나 그건 RV-adjunct·이건 contrast dose+$0 gradient 게이트
