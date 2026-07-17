# H_9719 — 일관-코드 sharp-init(정답 아닌 구별+일관성) — Sharp-Init Consistent Code (EA-1 · fable(최고통찰) · EA 시리즈 · PROPOSED)

**status:** 🔵 PROPOSED (미실행 · lab full 창발-주소 발산 · 사전등록) — source=EA-1 · fable(최고통찰)
**lane:** 재조합/BINDING · 창발-주소(감독 없이 주소가 서는가)
**related:** [[H_9672]] · [[H_9423]] · [[H_9684]] · [[H_9683]] · source: lab full EA(Fable 5 ∥ Codex Sol · 창발-주소 whitespace)

> **admissibility rule (Sol · 이 시리즈 전체의 관문)**: 어떤 개입도 `target_slot`·slot 정답·**거기서 파생된 어떤 통계**도 소비하지 않아야 emergent-address-valid. 최종 PASS 는 end-task-only 학습 · held-out 개체 · wrong-store 인과 · seed-robust 를 요구 — **sharp attention 만으론 부족**.

**아이디어(이 시리즈 최고 통찰)**: 교착이 요구하는 건 **정답이 아니라 "구별 + 일관성"** 이고 **`target_slot` 은 oracle 인공물**이다. 저온 sharp 주소 init 이 **무작위지만 일관된 injective** entity→slot commitment 를 주면 val 이 **step 0 부터 slot 별로 분화** → 주소 gradient 가 **스스로 자기강화** ⟹ **구성상 창발**(어떤 slot 도 이름 불림 없음).
**메커니즘**: `--store-att-temp τ0[:τ1@N]` · **target 없음 · 신규 loss 없음 · 신규 파라미터 0**.
**$0 pre-screen**: D0-3 pen-dump × 무작위 W_q seed 로 **충돌+일관성 census** — 충돌 ≥~40% 이거나 argmax 가 prompt-불안정이면 **KILL(발사 전)**.
**판정**: 2-seed {7,11} · 통제 = arm-C null(NEG) + addr-loss(POS-engineering) + scratch d768 인용(POS-emergence). PASS = P1-bal/flip/sharpness/consistency 게이트 · **canonical addr-gap 은 진단으로 강등**(정답 주소가 아니므로).
**distinct**: 어떤 slot 도 명명 안 함 ⟹ addr-loss(H_9672) 아님. ⚠️ **CONFLICT(명시)**: H_9692 가 temperature-annealing 을 "sharp-but-wrong 이 val 오염"으로 강등했으나 **그 강등은 감독 lane 서만 옳다** — w_addr=0 프레임엔 canonical target 이 없어 **sharp-but-permuted 가 허용**된다. K-geometry pinning 조건 하에선 H_9692 반론이 전이됨을 사전등록(반증가능한 충돌).
**verdict-integrity**: PASS = **hand-bolted store 위의 self-organized read code**(p1-p8 상한) · permuted-code PASS 는 **순열을 반드시 공개** · 1-seed 승리 = 0.9688 함정이라 **금지**.

## 상태
🔵 PROPOSED — 미실행 사전등록. 측정 주장 0(설계). **distinct-from-kills:** addr-loss(H_9672) 아님=slot 명명 0 · H_9692 강등은 감독 lane 한정(w_addr=0 서는 sharp-but-permuted 허용·조건부 전이 사전등록)

### 🛠️ $0 pre-screen 계기 착륙 + 의미론 2-정정 (VERSION 0.15.74 · 2026-07-17)
`anima-py evaluate <store-trailer ckpt> --store-addr-census <dump.npz>` 구현·착륙(engine-native · `a_experiment_engine_native`). random W_q(d→d_k) K-seed 로 개체키 `K[i]=_entity_key(key_emb,e_i)` 위 argmax-충돌을 **structureless-H pedestal** 대비 측정(`--store-census-selftest` = planted injective/collapsed 양성통제, **SELFTEST PASS** 로 계기 검증). admissible: `target_slot` 미조회(Sol 규칙).

**정정 ①(pedestal)**: 충돌 KILL 은 절대 40% 아니라 구조없는-h 대비(zero-truth arm · `phi-estimator-needs-zero-truth-pedestal`) — key-norm argmax 편향까지 흡수.
**정정 ②(의미론 · selftest 가 잡음)**: **n_slot=N_entities(CLMS 구조)에서 random W_q 는 birthday-bounded** — 고정키 위 argmax 는 어떤 h 도 ~1−1/e 충돌 아래로 못 감(injective 순열은 키-정렬 요구, random W_q 가 파괴). ⟹ **이 pre-screen 은 창발 탐지기가 아니라 COLLAPSE screen(필요조건)**: `obs≫ped`=붕괴 geometry(전부 한 슬롯)=KILL · `obs≈ped`=비붕괴(random 대비 안 나쁨)=PASS-screen(필요만·창발 확인 아님). **창발 verdict 는 오직 303M sharp-init fire**(카드 본문 `--store-att-temp`). 즉 이 $0 는 sharp-init 을 KILL 할 수는 있어도 GREEN 할 수 없다.
**발사 게이트**: store-trailer ckpt(key_emb 보유·T3류) pen-dump(`--dump-hidden`) 필요 = pool-303M · 개체풀. 계기·selftest 는 착륙, 실-dump census 는 pool-free 시 원커맨드.
