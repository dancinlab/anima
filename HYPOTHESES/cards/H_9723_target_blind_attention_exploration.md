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
🟠 **DIRECTIONAL·약신호 — $0 gradient-replay 실행(2026-07-17 · summer 303M · 사전등록 pre-screen)**

### 🟠 $0 gradient-replay = WEAK (노이즈 탐색 = 0.8% 개체 advantage · 훈련축적 미결)
카드 사전등록 pre-screen 실행: base penultimate + 극성값(2-class·store 실task) + attention logit 에 iid 영평균 노이즈(σ) + end-task 주소 gradient 를 정답슬롯 vs 같은-극성으로 8000-draw 평균:

| σ | 정답슬롯 \|g\| / 같은극성 \|g\| (advantage) |
|---|---|
| 0.5 | 1.008 |
| 1.0 | 1.009 |
| 2.0 | 1.006 |

**판정(DIRECTIONAL·약신호)**: 노이즈 탐색은 정답 개체슬롯에 **0.8% advantage**(ratio ~1.008) — H_9722 contrast 의 **정확히 0(1.000)과 대조**되는 **non-zero REINFORCE** 신호(노이즈가 가끔 정답슬롯 읽어 end-CE 개선→강화 축적). BUT 0.8% 는 극복대상 ~63% birthday 충돌 대비 **무시할 수준** ⟹ 훈련서 이 미세신호가 축적돼 주소를 세울지는 미결이나 **우선순위 낮음**(약한 씨앗). 카드 KILL조건('평균정렬 TOST-0')과 PASS 사이의 경계 = **약-DIRECTIONAL**.
**비교(EA 무감독 3-lens)**: sharp-init(basis 밖)=KILL · value-contrast(극성≠개체·advantage 정확히 0)=KILL · **noise-explore(advantage 0.8%)=약신호** — 셋 중 유일하게 non-zero 지만 실용역치 아래. 여전히 값이 극성(2-class)이라 개체정보를 못 나르는 근본한계는 공유([[binding-wall-operator-alive-fact-written-not-bound]]).
**남은 것**: 이 약신호가 훈련서 축적되는지는 학습 fire(annealing schedule)만 답함 — H_9720(disjoint lane·pre-screen PASS)과 묶어 저비용 병행 후보. **distinct-from-kills:** 직접감독/커리큘럼 아님=기대 slot 선호 정확히 0 · entropy/annealing/WTA/sparsemax 와 달리 sharpness 설치 안 함
