# H_9723 — target-맹목 attention 탐색(기대 slot 선호=정확히 0) — Target-Blind Attention Exploration (EA-5 · sol §2(NOVEL) · EA 시리즈 · PROPOSED)

**status:** 🔵 PROPOSED (미실행 · lab full 창발-주소 발산 · 사전등록) — source=EA-5 · sol §2(NOVEL)
**lane:** 재조합/BINDING · 창발-주소(감독 없이 주소가 서는가)
**related:** [[H_9672]] · [[H_9423]] · [[H_9684]] · [[H_9683]] · source: lab full EA(Fable 5 ∥ Codex Sol · 창발-주소 whitespace)

> **admissibility rule (Sol · 이 시리즈 전체의 관문)**: 어떤 개입도 `target_slot`·slot 정답·**거기서 파생된 어떤 통계**도 소비하지 않아야 emergent-address-valid. 최종 PASS 는 end-task-only 학습 · held-out 개체 · wrong-store 인과 · seed-robust 를 요구 — **sharp attention 만으론 부족**.

**아이디어(Sol 고유)**: 시간적으로 독립인 logit 탐색이 **균일-attention 고정점**을 벗어나게 해, 가끔 유용한 slot 을 읽고 그 값/판독 결과가 **평범한 주소 gradient 를 씨뿌린다**.
**메커니즘**: `--store-attn-noise-std σ --store-attn-noise-decay N` — 모든 pre-softmax slot logit 에 **iid 영평균 노이즈**를 slot 내용·`target_slot` 과 **독립**으로 더하고 **정확히 0 으로 anneal**.
**$0 pre-screen**: 저장 배치 gradient replay — 노이즈가 기대 target-minus-distractor `W_q` 갱신 정렬을 올리나 ≥10⁴ draw 평균으로 추정 · **분산만 오르고 평균 정렬이 TOST-0 이면 KILL**.
**판정**: 통제 = 무노이즈 사전학습(NEG) · scratch(POS-emergence) · addr-loss(POS-engineering) · **비-anneal 노이즈 통제**. PASS = ≥3 seed 가 **노이즈 완전 제거 후에도** P1-bal/addr_mass/flip ≥0.90 유지 **∧ 비-anneal 통제를 이김**. KILL = 노이즈 제거 시 이득 소멸 · 운좋은 seed 의존 · **균일 무작위 slot 선택으로 출력이 설명됨**.
**distinct**: 가장 가까운 kill = slot 커리큘럼/직접감독. **노이즈는 정답 slot 을 보존·선호·식별하지 않는다**(기대 선호 = **정확히 0**) — target-보존 dropout 이나 target-편향 샘플링은 **위장 감독이라 드롭**. Sol 이 명시: attention-entropy 패널티/hard·temperature annealing/WTA/sparsemax 는 **sharpness 를 직접 설치**해 무감독 주장 불가 — **노이즈만 살아남는 이유가 기대 선호 0**.
**verdict-integrity**: 이건 "**확률적으로 복원된 창발**"이지 **무섭동 창발 아님**(Sol 자기명시) · **sharp 하나 틀린 attention 은 음성**.

## 상태
🔵 PROPOSED — 미실행 사전등록. 측정 주장 0(설계). **distinct-from-kills:** 직접감독/커리큘럼 아님=기대 slot 선호 정확히 0(target-보존 dropout·편향샘플링은 위장이라 드롭) · entropy 패널티/annealing/WTA/sparsemax 와 달리 sharpness 를 설치 안 함
