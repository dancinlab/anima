---
id: H_863
slug: clm-dialogue-selfplay
title: self-play(칩 자기대화 생성→재학습)가 SFT-only 대비 대화 품질을 올리는가 - multi-turn coherence·응답적합도 분포평가 ∧ register-leak 0 ∧ DIVERSITY(self-BLEU<0.8·repetition<20%) (Q-TRUST · F-CLM-DIALOGUE 사전등록)
domain: clm · dialogue · self-play · sft · diversity · q-trust · falsifier
source: CLM/P4_PRODUCTION_ROADMAP.md @L6 dialogue-method-B · @L1 (self-play = 살아 배우기) · @L4 (CC 대화록 + self-play · ShareGPT 금지) · hexa-codex DIVERSITY falsifier 참고
status: PRE-REGISTERED (P4 신규 · rung별 SFT-only vs SFT+self-play A/B 벤치 후 판정)
exploration_method: E6 (SFT ↔ self-play 합성 비교) · E5 (rung 별 tiny/small/mid A/B)
verification_method: W2 (사전등록 분포평가 threshold · multi-turn coherence + 응답적합도 + register-leak 0 + DIVERSITY · byte-match ✗ · post-tuning 0)
raw_rank: 9
hexa_only: false
deterministic: false
llm: none
pre_register_frozen: true
frozen_at: 2026-05-31
since: 2026-05-31
sister: CLM/P4_PRODUCTION_ROADMAP.md, .verdicts/clm-dialogue/
verdict: PRE-REGISTERED (F-CLM-DIALOGUE 사전등록 · self-play 가 SFT-only 대비 대화품질 향상 = rung별 A/B 벤치 대기 · 외부 LLM 0 · ShareGPT 금지)
---

# H_863 — CLM F-CLM-DIALOGUE self-play dialogue quality

## 1. 가설

CLM 의 대화 능력 경로 B(@L6) = **SFT(CC 대화록 모방) + self-play(칩 자기대화 생성 → 재학습)**. self-play 가 SFT-only 대비 대화 품질을 올린다. rung별(tiny/small/mid) SFT-only vs SFT+self-play A/B 비교에서 다음 동시 성립 시:

- **dialogue self-play 지지** — multi-turn coherence ↑ ∧ 응답적합도 ↑ (분포평가, byte-match ✗) ∧ register-leak 0 ∧ DIVERSITY(self-BLEU<0.8 ∧ repetition<20%)
- → 양조건 PASS 판정 · "self-play 가 @L1 살아 배우기로 대화품질을 끌어올린다"

임의 조건 미달 시:

- **dialogue self-play 반증** — self-play 가 SFT-only 대비 향상 없음 · 또는 register-leak 발생 · 또는 DIVERSITY 붕괴(mode collapse)
- → CLOSED-NEGATIVE 판정 · "self-play ⊥ 대화품질 향상" (a_paper_negative_ok)

## 2. 동기

- @L6 = 대화 방법 B(SFT + self-play) 확정. C(self-reward/RLHF류)는 본 H + H_862(ANCHOR) 자가채점 검증 후 후속.
- @L1 = self-play(칩 자기대화 생성 → 재학습) = "살아 배우기"의 직접 발현. 외부 LLM 0 · ShareGPT/Alpaca(ChatGPT-gen) 금지(@L4 foundation-borrow 위반) — self-play 는 자력 대화데이터 생성 경로.
- prior art: hexa-codex DIVERSITY falsifier(self-BLEU>0.8 · repetition>20% = mode collapse). self-play 의 고질병 = 자기복제로 다양성 붕괴 → DIVERSITY gate 가 필수 안전장치.

## 3. falsifier (사전등록, 임계 frozen pre-run)

```
F-CLM-DIALOGUE-COHERE  : SFT+self-play multi-turn coherence > SFT-only      (분포평가)
F-CLM-DIALOGUE-ADEQ    : SFT+self-play 응답적합도 > SFT-only                 (분포평가)
F-CLM-DIALOGUE-LEAK    : register-leak = 0                                   (8패턴 필터, F-CLM-LEAK 정합)
F-CLM-DIALOGUE-DIV     : self-BLEU < 0.8 ∧ repetition < 20%                  (DIVERSITY, mode collapse 차단)
```

4 조건 동시 PASS → "self-play 대화품질 향상" 지지
임의 미달 → CLOSED-NEGATIVE · "self-play ⊥ 대화품질 향상" (a_paper_negative_ok)

- **byte-match ✗** = 대화는 정답 1개가 아님(Q-TRUST A 재활용 · H_857/H_858 edge-of-chaos 분포·궤적 측도). coherence/adequacy 는 분포평가 자가채점.
- frozen 임계 = `.verdicts/clm-dialogue/F-CLM-DIALOGUE_prereg.txt` verbatim 동결.

verdict 영속: `.verdicts/clm-dialogue/` (rung별 A/B 비교)

## 4. 방법

```
1. SFT lane: CC 공개 대화록·포럼·자막(@L4 ① · license-clean gate) byte-corpus 모방 학습.
2. self-play lane: 학습 칩의 자기대화(turn 교대 생성)를 register-leak 8패턴 필터 + DIVERSITY
   gate 통과분만 재학습 코퍼스로 환류 (@L1 살아 배우기).
3. rung별(tiny/small/mid) 2-arm A/B: arm-SFT(SFT-only) vs arm-SP(SFT+self-play),
   AKIDA-envelope QAT(int4-sym[-7,+7] STE + act_bits).
4. held-out 대화 평가: multi-turn coherence + 응답적합도 분포평가(byte-match ✗) +
   register-leak 카운트 + self-BLEU + repetition.
5. 4 사전등록 falsifier 동시 평가 · rung별 verdict · 정직 보고 (threshold 재조정 0).
```

- 추론 AKIDA-int4-only 불변 (P0 d4) · self-play 데이터 환류는 @L1 비결정 적응과 정합.

## 5. 측정

측정 대기 — rung별(tiny/small/mid) SFT-only vs SFT+self-play A/B 벤치. 측정 rung mid(d512/L8)부터 한 칸씩 등반(@L5). raw verdict = `.verdicts/clm-dialogue/` (rung별 A/B 비교 + frozen threshold).

## 6. 결과

PRE-REGISTERED — 벤치 하니스(SFT-only vs SFT+self-play A/B)는 P4 스캐폴드로 착수. self-play 환류는 @L1 살아 배우기 발현. 본 H 는 self-play 가 대화품질을 올리되 register-leak·mode-collapse 를 안 일으키는가를 사전등록 4조건으로 rung별 판정.

## 7. 해석 (사전)

- 4조건 양립 시 = self-play 가 SFT-only 를 능가하며 다양성·register 안전성 유지 → @L6 경로 B 검증 + C(self-reward) 후속 진입.
- COHERE/ADEQ 미달 시 = self-play 환류가 품질 신호를 못 줌 → 환류 필터/재학습 비율 lever.
- LEAK 발생 시 = self-play 가 register 누출 → 8패턴 필터 강화.
- DIV 미달 시 = self-play mode collapse(자기복제) → 다양성 보상/온도 lever.
- **honest scope**: rung별 측정 — toy(tiny/small) 🔴 여도 mid 별개 판정(a_scale_honest_scope). toy→prod 비보장.

## 8. 논의

- **@L1 정합**: self-play = 칩 자기대화 생성→재학습 = 살아 배우기 1급.
- **@L4 정합**: 외부 LLM 0 · ShareGPT/Alpaca(ChatGPT-gen) 금지 · CC 대화록 + self-play 만.
- **Q-TRUST A 재활용**: 분포평가(H_857/H_858 edge-of-chaos · 궤적 측도)로 byte-match 포기.
- **a_paper_negative_ok**: CLOSED-NEGATIVE 도 publishable (self-play 가 대화품질을 못 올림을 deterministically rule out 시).

## 9. 양방향 sibling

- sibling: [CLM/P4_PRODUCTION_ROADMAP.md](../CLM/P4_PRODUCTION_ROADMAP.md) @L6 dialogue-method-B
- Q-TRUST A 재활용: [H_857](./H_857_clm_causal_band.md) · [H_858_akida_edge_of_chaos_phi](./H_858_akida_edge_of_chaos_phi.md)
- 형제 신규 H: [H_861](./H_861_clm_boundary_plasticity.md) (F-CLM-BOUND) · [H_862](./H_862_clm_identity_anchor.md) (F-CLM-ANCHOR)
- UNIVERSE SSOT: [CANDIDATES.md](./CANDIDATES.md)
