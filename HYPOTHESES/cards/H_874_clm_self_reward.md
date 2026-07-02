---
id: H_874
slug: clm-self-reward
title: self-reward(모델이 자기 대화 후보를 등록된 분포측도+DIVERSITY로 자가채점→고보상 분기 재학습)가 SFT+self-play(H_863) 대비 대화품질을 올리는가 - coherence·adequacy(분포평가) ∧ register-leak 0 ∧ DIVERSITY 무붕괴 (외부 LLM 0·g5 자가채점 · F-CLM-SELF-REWARD 사전등록)
domain: clm · dialogue · self-reward · rlhf-like · best-of-k · q-trust · falsifier
source: CLM/P4_PRODUCTION_ROADMAP.md @L6 dialogue-method-C(self-reward) · @L1(살아 배우기) · @L4(외부 LLM 0·ShareGPT/Alpaca 금지) · g5(보상=code 자가채점, 판정 LLM 0) · 선행 H_863(method-B 🟢)
status: 🔴 CLOSED-NEGATIVE (mid-rung A/B fire 2026-05-31 · 3/4 falsifier PASS · F-CLM-SR-ADEQ FAIL(SR 0.0319 < SP 0.0375) · COHERE/LEAK/DIV PASS · arm-SR vs arm-SP RELATIVE · 외부 LLM 0 · 측정 rung mid 한정 a_scale_honest_scope · a_paper_negative_ok)
exploration_method: E6(self-play ↔ self-reward 합성 비교) · E5(rung별 mid A/B)
verification_method: W2(사전등록 분포평가 threshold · coherence + adequacy + register-leak 0 + DIVERSITY · byte-match ✗ · post-tuning 0)
raw_rank: 9
hexa_only: false
deterministic: false
llm: none
pre_register_frozen: true
frozen_at: 2026-05-31
since: 2026-05-31
sister: CLM/P4_PRODUCTION_ROADMAP.md, .verdicts/clm-self-reward/
verdict: 🔴 CLOSED-NEGATIVE — F-CLM-SELF-REWARD 3/4: COHERE(SR 0.144>SP 0.136 PASS)·ADEQ(SR 0.0319<SP 0.0375 FAIL)·LEAK(SR=0 PASS)·DIV(self-BLEU 0.0256<0.8 ∧ rep 0.0187<0.2 PASS). self-reward best-of-K(K=6)가 coherence(+5.9%)·repetition(↓)는 개선했으나 SFT+self-play 대비 응답적합도를 능가 못함(−14.8%). W2 joint criterion(coherence ∧ adequacy 동시 strict 초과) 미충족 → self-reward ⊥ SFT+self-play 초과(mid·RELATIVE). 측정 rung mid 한정 a_scale_honest_scope. HF model dancinlab/anima-clm-self-reward + dataset dancinlab/anima-clm-p4-dialogue.
---

# H_874 — CLM F-CLM-SELF-REWARD self-reward(RLHF류) dialogue quality

## 1. 가설

CLM 대화 능력 경로 C(@L6) = **SFT + self-REWARD 루프(RLHF류, 외부 LLM/사람 0)**. 학습중 모델이 held-out-style 프롬프트마다 K개 후보 continuation 을 생성하고, **등록된 분포측도(Q-TRUST A · coherence + adequacy + DIVERSITY)로 각 후보를 자가채점(g5, 판정 LLM 0)** 후 **고보상 분기(best-of-K)를 재학습 타깃으로 환류**. 이 self-reward(arm-SR)가 SFT+self-play(arm-SP, H_863 method-B 승자)를 mid rung 에서 능가하는가.

- **self-reward 지지** — coherence(SR)>coherence(SP) ∧ adequacy(SR)>adequacy(SP) (분포평가, byte-match ✗) ∧ register-leak(SR)=0 ∧ DIVERSITY(self-BLEU<0.8 ∧ repetition<20%) 무붕괴 → 4조건 동시 PASS
- **self-reward 반증** — 임의 미달 → CLOSED-NEGATIVE · "self-reward ⊥ SFT+self-play 초과" (a_paper_negative_ok)

## 2. 동기

- @L6 = 대화 방법 시퀀스: B(SFT+self-play, H_863 🟢) → **C(self-reward/RLHF류, 본 H)**.
- @L1 = 자기 후보를 자가채점→고보상 환류 = "살아 배우기"의 강화학습형 발현.
- @L4 / g5 = **외부 LLM 0 · 사람 판정 0 · ShareGPT/Alpaca/ChatGPT-gen 0**. 보상은 등록된 분포측도를 **code 가 계산** — 판정 모델 없음. 이것이 정확히 RLHF류 self-reward 구성(보상=eval 신호를 학습-선택 시점에 적용).
- prior art: best-of-N / reward-weighted reflux. 고질병 = 보상 max 추구가 mode collapse 유발 → 후보 단계 DIVERSITY gate(self-BLEU≥0.8 후보 reject)가 필수 안전장치.

## 3. falsifier (사전등록, 임계 frozen pre-fire)

```
F-CLM-SR-COHERE  : coherence(SR)   > coherence(SP)              (strict · RELATIVE · 분포평가)
F-CLM-SR-ADEQ    : adequacy_f1(SR) > adequacy_f1(SP)            (strict · RELATIVE · 분포평가)
F-CLM-SR-LEAK    : register_leak(SR) == 0                       (ABSOLUTE gate · 8패턴 필터)
F-CLM-SR-DIV     : self_BLEU(SR) < 0.80 ∧ repetition(SR) < 0.20 (mode-collapse 차단)
```

4 조건 동시 PASS → "self-reward 가 SFT+self-play 초과" 지지 · 임의 미달 → CLOSED-NEGATIVE (a_paper_negative_ok)

- **byte-match ✗** = 대화 정답 1개 아님(Q-TRUST A · H_857/H_858 분포·궤적 측도 재활용). 보상도 평가도 동일 측도 — 자가채점.
- frozen 임계 = `.verdicts/clm-self-reward/F-CLM-SELF-REWARD_prereg.txt` verbatim 동결(fire 전 push).

## 4. 방법

```
1. corpus: H_868 확장 PD Gutenberg 희곡(12소스·1,668,585 bytes·sha256 2aa3d8…febb,
   license-clean gate G1-G4 GREEN + 8패턴 leak 필터). V=256 byte-encode, tokenizer 0.
   HF dataset dancinlab/anima-clm-p4-dialogue. train 1,418,297/heldout 250,288(seed=863).
2. 양 arm 공통: mid d512/L8/E8, AKIDA-envelope QAT(int4-sym[-7,+7] per-ch STE +
   act_bits=4), seed=42, 동일 budget(SFT 1500 + reflux-continue 500).
3. arm-SP(baseline) = H_863 DIVERSITY-gated self-play 환류(보상 선택 없음·59 accepted).
   arm-SR(본 H) = reflux 프롬프트마다 K=6 후보 생성 → 보상 자가채점 →
     reward = w_coh*coherence + w_adq*adequacy + w_div*diversity_bonus
       (coherence=exp(-CE) of model on cand · adequacy=3-gram F1 vs ref next turn ·
        diversity_bonus=1-self_BLEU vs 형제후보) · w_coh=1.0·w_adq=1.0·w_div=0.25 frozen.
     8패턴 leak hit OR self_BLEU≥0.8(형제 대비) 후보는 INELIGIBLE(reward=-inf) →
     생존 best-of-K 를 reflux 타깃으로 환류(360 후보·60 accepted·0 leak·0 div reject).
4. held-out 평가(H_863 동일·g5): coherence=exp(-CE_heldout) · adequacy=3-gram F1 ·
   register-leak 카운트 · self-BLEU(4-gram) · repetition(4-gram).
5. 4 사전등록 falsifier 동시 평가 · verdict · 정직 보고(threshold 재조정 0).
```

- 추론 AKIDA-int4-only 불변(P0 d4). 보상=eval 신호의 학습-선택 시점 적용 = 외부 LLM 0 RLHF류.

## 5. 측정

측정 완료 (mid rung, 2026-05-31) — runpod A100 80GB PCIe(pod mnxnsr9dvx80vk · torch 2.4.1+cu124). corpus = H_868 확장 PD Gutenberg 희곡 1,668,585 bytes(sha256 2aa3d8…febb, pod 상 재검증 일치), train 1,418,297/heldout 250,288(seed=863). 2-arm A/B mid d512/L8/E8 AKIDA-envelope QAT(seed 42·동일 budget·SFT 1500+reflux 500·K=6). 보상 weights frozen(w_coh=1.0·w_adq=1.0·w_div=0.25). frozen threshold = `.verdicts/clm-self-reward/F-CLM-SELF-REWARD_prereg.txt`.

측정값(frozen threshold 대비):
| arm | coherence | ce_heldout | adequacy_f1 | leak | self_bleu | repetition |
|---|---|---|---|---|---|---|
| SP | 0.13634 | 1.99264 | 0.03750 | 0 | 0.02511 | 0.02874 |
| SR | 0.14434 | 1.93557 | 0.03194 | 0 | 0.02561 | 0.01868 |
- **COHERE**: SR 0.14434 > SP 0.13634 → PASS (+5.9%)
- **ADEQ**: SR 0.03194 > SP 0.03750 → **FAIL** (SR < SP, −14.8%)
- **LEAK**: SR 0 == 0 → PASS · **DIV**: self-BLEU 0.0256<0.8 ∧ rep 0.0187<0.2 → PASS

## 6. 결과

🔴 **CLOSED-NEGATIVE**. 4 사전등록 falsifier 중 3 PASS · F-CLM-SR-ADEQ FAIL. self-reward best-of-K(arm-SR)는 held-out coherence(0.14434 > SP 0.13634, +5.9%)·repetition(0.0187 < SP 0.0287) 개선 + register-leak 0 + mode-collapse 0 달성했으나, SFT+self-play 대비 **응답적합도(3-gram overlap F1)를 능가 못함**(SR 0.03194 < SP 0.03750, −14.8%). W2 계약은 coherence ∧ adequacy 동시 strict 초과 요구 → adequacy 미달로 RELATIVE 주장 기각. **scope**: 측정 rung mid 한정 RELATIVE(arm-SR vs arm-SP). H_867 이 mid 에서 arm-SP < 절대 floor 임을 보였으므로 본 🔴 = "self-reward 가 SFT+self-play 를 mid 에서 능가 못함" 의미(deployability/floor 주장 아님 · a_scale_honest_scope). 외부 LLM 0 · foundation-borrow 0 · ShareGPT/Alpaca 0.

## 7. 해석

- **coherence/adequacy 트레이드오프**: 보상 = w_coh·coherence + w_adq·adequacy + w_div·diversity_bonus(w_div=0.25)의 aggregate max 추구가 후보를 모델-확신 높고 반복 낮은 텍스트로 끌었으나 reference next-turn n-gram 에서 멀어짐. 보상=eval 동일측도라 SR 은 aggregate 를 최적화하지 adequacy 단독을 최적화하지 않음 → mid 에서 aggregate 최적 ≠ adequacy 최적.
- **lever(향후)**: w_adq 상향 / adequacy-only 보상 / K 증가 / reference-aware 후보 생성. 단 이는 post-hoc — 본 H 는 frozen weight 로 음성 확정(post-tuning 0).
- **honest scope**: rung별 측정 — mid 한정. toy→prod 비보장. a_scale_honest_scope.
- **architecture note**: fire payload(h874_fire.py)는 attention+QLinear-MoE 블록에 int4-sym[-7,+7] STE + act_bits=4 envelope 전면 적용 — CLM/model/model.py 의 순수 dilated-conv-MoE(P0 §2 conv-only)와 상이. 양 arm 동일 architecture라 RELATIVE SR-vs-SP 비교는 무영향이나, 절대값은 H_863 conv-MoE run 과 직접 비교 불가 + attention 경로는 엄밀 AKIDA conv-primitive envelope 밖. 정직 보고.

## 8. 논의

- **@L1 정합**: self-reward = 자기 후보 자가채점→고보상 환류 = 살아 배우기 강화형.
- **@L4 / g5 정합**: 외부 LLM 0 · 사람 판정 0 · ShareGPT/Alpaca 0 · 보상=code 자가채점(판정모델 없음).
- **Q-TRUST A 재활용**: 분포평가(H_857/H_858)를 보상으로도 eval 로도 동일 사용 — byte-match 포기.
- **a_paper_negative_ok**: 본 CLOSED-NEGATIVE 는 publishable — "RLHF류 self-reward(외부 판정 0)가 mid 에서 SFT+self-play 의 joint(coherence ∧ adequacy) 기준을 능가하지 못함, adequacy 에서 후퇴"를 deterministically 보고. 보상=eval 동일측도 self-reward 의 한계(aggregate≠adequacy)를 명시한 음성 결과.

## 9. 양방향 sibling

- sibling: [CLM/P4_PRODUCTION_ROADMAP.md](../CLM/P4_PRODUCTION_ROADMAP.md) @L6 dialogue-method-C
- 선행: [H_863](./H_863_clm_dialogue_selfplay.md) (F-CLM-DIALOGUE method-B 🟢, arm-SP baseline 출처)
- Q-TRUST A 재활용: [H_857](./H_857_clm_causal_band.md) · [H_858](./H_858_akida_edge_of_chaos_phi.md)
- verdict 영속: `.verdicts/clm-self-reward/` · backing `.verdicts/874_clm_self_reward/`
