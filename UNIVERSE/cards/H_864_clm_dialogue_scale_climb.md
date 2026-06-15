---
id: H_864
slug: clm-dialogue-scale-climb
title: dialogue self-play scale-climb — H_863 mid(d512/L8/E8) 결과를 한 rung 위 large(d768/L12/E12)로 올려도 SFT+self-play 가 SFT-only 대비 대화품질을 유지/능가하는가 - 동일 4 frozen falsifier per-rung (COHERE/ADEQ(SP>SFT) ∧ LEAK=0 ∧ DIV(self-BLEU<0.8·rep<0.2)) (Q-TRUST · F-CLM-DIALOGUE-LARGE)
domain: clm · dialogue · self-play · sft · diversity · scale-climb · q-trust · falsifier
source: UNIVERSE/CLM-CANDIDATES.md group A H_864 · H_863 mid result · CLM/P4_PRODUCTION_ROADMAP.md @L5 ladder · @L6 dialogue-method-B · @L1 (self-play = 살아 배우기) · @L4 (CC 대화록 + self-play · ShareGPT 금지)
status: 🔴 CLOSED-NEGATIVE (large-rung A/B fire 2026-05-31 · 2/4 frozen falsifier FAIL — COHERE/ADEQ tie(SP==SFT)·DIV mode-collapse · 4 frozen falsifier = bf98c01 scale-invariant relative gates, NO new freeze · post-tuning 0 · 측정 rung large 한정 a_scale_honest_scope · a_paper_negative_ok)
exploration_method: E5 (rung별 ladder climb tiny/small/mid→large A/B) · E6 (SFT ↔ self-play 합성 비교)
verification_method: W2 (사전등록 분포평가 threshold = bf98c01 frozen, scale-invariant relative · multi-turn coherence + 응답적합도 + register-leak 0 + DIVERSITY · byte-match X · post-tuning 0)
raw_rank: 9
hexa_only: false
deterministic: false
llm: none
pre_register_frozen: true
frozen_at: 2026-05-31
since: 2026-05-31
sister: CLM/P4_PRODUCTION_ROADMAP.md, .verdicts/clm-dialogue-large/, UNIVERSE/H_863_clm_dialogue_selfplay.md
verdict: 🔴 CLOSED-NEGATIVE — F-CLM-DIALOGUE-LARGE 2/4 FAIL: COHERE(SP 0.03288 == SFT 0.03288, NOT strict>) FAIL · ADEQ(0.03750==0.03750) FAIL · LEAK(SP=0) PASS · DIV(self-BLEU 0.576<0.8 ∧ repetition 0.361 ≥ 0.2 → mode collapse) FAIL. self-play reflux DIVERSITY gate가 reflux batch(rep 0.335≥0.2)를 거부 → arm-SP가 pure SFT로 degenerate → COHERE/ADEQ tie. large rung(d768/L12/E12 · 44.68M) self-play 대화 이득이 H_863 mid PASS와 달리 carry 안 됨. frozen threshold(bf98c01) 대비 post-tuning 0. 측정 rung large 한정(a_scale_honest_scope) · a_paper_negative_ok. HF dataset dancinlab/anima-clm-large-dialogue.
---

# H_864 — CLM F-CLM-DIALOGUE-LARGE self-play dialogue scale-climb

## 1. 가설

H_863 이 mid rung(d512/L8/E8 · ~13.65M)에서 **SFT+self-play > SFT-only 대화품질** 을 4/4 frozen-falsifier PASS 로 보였다. H_864 = 그 결과를 @L5 ladder 한 rung 위 **large(d768/L12/E12 · ~44.7M, mid 대비 ~3.3×)** 로 올린다. 동일 4 frozen falsifier(bf98c01)를 per-rung 으로 재평가:

- **dialogue self-play scale-climb 지지** — large rung 에서도 multi-turn coherence ↑ ∧ 응답적합도 ↑ (분포평가, byte-match X) ∧ register-leak 0 ∧ DIVERSITY(self-BLEU<0.8 ∧ repetition<20%) 동시 성립
- → 4조건 PASS · "self-play 의 대화품질 이득이 scale 한 rung 위에서도 유지/능가"

임의 조건 미달 시:

- **dialogue self-play scale-climb 반증** — large rung 에서 self-play 가 SFT-only 대비 향상 없음 · 또는 register-leak 발생 · 또는 DIVERSITY 붕괴(mode collapse)
- → CLOSED-NEGATIVE 판정 · "self-play 대화품질 이득 ⊥ 이 rung" (a_paper_negative_ok)

## 2. 동기

- H_863 mid 결과 = 한 rung 측정. @L5 production ladder 는 한 번에 한 rung 올린다(measurement track ⊥ deploy chip-fit track · a_scale_honest_scope). mid PASS 가 large 를 자동 보장하지 않음 → 한 rung 위 재측정이 필요.
- @L6 = 대화 방법 B(SFT + self-play). @L1 = self-play(칩 자기대화 생성 → 재학습) = 살아 배우기. 외부 LLM 0 · ShareGPT/Alpaca(ChatGPT-gen) 금지(@L4).
- self-play 의 고질병 = 자기복제 다양성 붕괴 → scale 가 커질수록 mode collapse 위험도 재확인 필요 → DIVERSITY gate per-rung.

## 3. falsifier (사전등록, 임계 frozen — bf98c01 scale-invariant relative gates, NO new freeze)

```
F-CLM-DIALOGUE-COHERE  : SFT+self-play multi-turn coherence > SFT-only      (분포평가, strict relative)
F-CLM-DIALOGUE-ADEQ    : SFT+self-play 응답적합도 > SFT-only                 (분포평가, strict relative)
F-CLM-DIALOGUE-LEAK    : register-leak(SP) = 0                               (8패턴 필터, absolute)
F-CLM-DIALOGUE-DIV     : self-BLEU(SP) < 0.8 ∧ repetition(SP) < 20%          (DIVERSITY, absolute)
```

4 조건 동시 PASS → "self-play 대화품질 이득 scale-climb" 지지
임의 미달 → CLOSED-NEGATIVE · "self-play 대화품질 이득 ⊥ 이 rung" (a_paper_negative_ok)

- **scale-invariant 동결 근거**: COHERE/ADEQ 는 RELATIVE(SP 가 SFT 를 strict 능가) · LEAK/DIV 는 SP 의 ABSOLUTE gate. 어느 것도 rung 크기에 의존하지 않으므로, bf98c01(`.verdicts/clm-dialogue/F-CLM-DIALOGUE_prereg.txt`, 2026-05-31 freeze, H_863 fire 前 push)에 동결된 임계가 large rung 으로 **새 freeze 없이** 그대로 carry 된다. 본 H 는 새 임계를 도입하지 않는다 — post-tuning 0.
- **byte-match X** = 대화는 정답 1개가 아님(Q-TRUST A 재활용 · H_857/H_858 edge-of-chaos 분포·궤적 측도). coherence/adequacy 는 분포평가, CODE 자가채점(g5 · LLM-judge X).

verdict 영속: `.verdicts/clm-dialogue-large/` (large rung A/B)

## 4. 방법

```
1. SFT lane: 본 fire 자체 license-clean PD Gutenberg 희곡 snapshot(H_863 의 4편 +
   추가 PD 희곡 → 9편) byte-corpus 모방 학습. (H_868 의 CLM/corpus/ 경로와 충돌 회피 —
   본 snapshot 은 .verdicts/clm-dialogue-large/ manifest 로 provenance 기록, parallel.)
2. self-play lane: 학습 칩의 자기대화(turn 교대 생성)를 register-leak 8패턴 필터 +
   DIVERSITY gate 통과분만 재학습 코퍼스로 환류 (@L1 살아 배우기).
3. large rung 2-arm A/B: arm-SFT(SFT-only) vs arm-SP(SFT+self-play),
   AKIDA-envelope QAT(int4-sym[-7,+7] per-output-channel STE + act_bits=4), seed=42, 동일 budget.
4. held-out 대화 평가(seed=863, disjoint): multi-turn coherence=exp(-CE) + 응답적합도(3-gram F1) +
   register-leak 카운트 + self-BLEU(4-gram pairwise) + repetition(repeated-4-gram) — 전부 CODE.
5. 4 frozen falsifier(bf98c01) 동시 평가 · large rung verdict · 정직 보고 (threshold 재조정 0).
```

- 추론 AKIDA-int4-only 불변 (P0 d4) · self-play 데이터 환류는 @L1 비결정 적응과 정합.

## 5. 측정

측정 (large rung, 2026-05-31) — runpod A100 80GB PCIe(torch 2.4.1+cu124). corpus = Project Gutenberg PUBLIC-DOMAIN 희곡 9편(H_863 의 Hamlet #1524·Earnest #844·Doll's House #2542·Julius Caesar #1522 + Romeo and Juliet #1513·Macbeth #1531·Lady Windermere's Fan #1119·An Ideal Husband #4078·The Sea-Gull #2130, license=PD), license-clean gate + 8-패턴 leak 필터 통과(1줄 drop), V=256 byte-encode, **1,559,675 bytes**(H_863 의 554,825 대비 ~2.8×) → train 1,299,730 / heldout 259,945(seed=863). 2-arm A/B large d768/L12/E12(**44.68M params** · mid 13.65M 대비 3.27×) AKIDA-envelope QAT(arm AB·seed 42·동일 budget): arm-SFT(SFT only) vs arm-SP(SFT + DIVERSITY-gated self-play 환류 + 500 step continue). held-out 평가 = coherence=exp(-CE)·adequacy=3-gram F1·register-leak·self-BLEU·repetition(전부 CODE 자가채점 g5). frozen threshold = `.verdicts/clm-dialogue/F-CLM-DIALOGUE_prereg.txt`(commit bf98c01, scale-invariant relative gates · NO new freeze).

self-play reflux: 48 samples 생성 · 0 leak-drop · 48 kept · reflux self-BLEU 0.531(<0.8 OK) · **reflux repetition 0.335 ≥ 0.20 → DIVERSITY gate REJECT** → reflux 환류 0 → arm-SP가 pure SFT로 degenerate(동일 seed/budget).

측정값(frozen threshold 대비):

| arm | coherence | ce_heldout | adequacy_f1 | leak | self_bleu | repetition |
|---|---|---|---|---|---|---|
| SFT | 0.03288 | 3.41504 | 0.03750 | 0 | 0.57582 | 0.36107 |
| SP | 0.03288 | 3.41504 | 0.03750 | 0 | 0.57582 | 0.36107 |
- **COHERE**: SP 0.03288 == SFT 0.03288 (NOT strict>) → **FAIL** · **ADEQ**: 0.03750==0.03750 → **FAIL**
- **LEAK**: SP 0 == 0 → PASS · **DIV**: self-BLEU 0.576<0.8 ∧ repetition 0.361 ≥ 0.2 → **FAIL** (mode collapse)

## 6. 결과

🔴 **CLOSED-NEGATIVE** (a_paper_negative_ok). 4 frozen falsifier 중 2 FAIL(COHERE·ADEQ tie · DIV mode-collapse), LEAK PASS. H_863 mid 에서 측정된 self-play 대화 이득이 large rung 으로 **carry 되지 않음**. 두 결합 메커니즘: (1) self-play reflux batch 가 per-batch DIVERSITY gate(repetition 0.335 ≥ 0.20)를 통과 못 함 → 환류 0 → arm-SP 가 arm-SFT 로 degenerate → COHERE/ADEQ 가 strict-greater relative gate 에서 정확히 tie 로 FAIL; (2) large rung 자체 held-out generation 이 mode-collapsed(repetition 0.361 ≥ 0.20) → SP 의 absolute DIVERSITY gate FAIL(환류 여부 무관). 정직: tuning artifact 가 아닌 실재 scale-dependent 현상 — 44.68M 모델이 2000 step 에서 반복 생성기로 과적합, self-play 는 자기 샘플이 너무 반복적이라 통과해야 할 gate 를 못 넘어 기여 0. **scope**: 측정 rung large 한정 — H_863 mid PASS·다른 rung·배포 chip-fit track 별개(a_scale_honest_scope) · 외부 LLM 0 · ShareGPT/Alpaca 0 · large→prod 비보장. **다음 lever**(별도 사전등록 fire 필요 · post-tuning 0): self-play 샘플링 온도↓ / repetition penalty / held-out DIVERSITY early-stop / rung별 budget 재조정.

## 7. 해석 (사전)

- 4조건 양립 시 = self-play 대화품질 이득이 mid→large scale 한 rung 위에서도 유지/능가 + 다양성·register 안전성 유지 → @L5 ladder 한 칸 더 올림 + @L6 경로 B large-rung 검증.
- COHERE/ADEQ 미달 시 = scale 가 커지자 self-play 환류 이득이 사라짐 → 환류 필터/재학습 비율·rung별 budget lever.
- LEAK 발생 시 = scale 가 커진 칩이 register 누출 → 8패턴 필터 강화.
- DIV 미달 시 = large self-play mode collapse(자기복제) → 다양성 보상/온도 lever.
- **honest scope**: rung별 측정 — mid PASS 여도 large 별개 판정(a_scale_honest_scope). large→prod 비보장.

## 8. 논의

- **@L1 정합**: self-play = 칩 자기대화 생성→재학습 = 살아 배우기 1급.
- **@L4 정합**: 외부 LLM 0 · ShareGPT/Alpaca(ChatGPT-gen) 금지 · CC/PD 대화록 + self-play 만.
- **Q-TRUST A 재활용**: 분포평가(H_857/H_858 edge-of-chaos · 궤적 측도)로 byte-match 포기.
- **scale-invariant 동결**: bf98c01 의 4 falsifier 가 relative/absolute gate 라 rung 크기 무관 → 새 freeze 없이 carry (W2 discipline, post-tuning 0).
- **H_868 collision-free**: 본 fire 는 자체 PD snapshot(.verdicts/clm-dialogue-large/ manifest)을 쓰고 CLM/corpus/ 를 건드리지 않음 (H_868 가 그 경로 소유 · parallel).
- **a_paper_negative_ok**: CLOSED-NEGATIVE 도 publishable (self-play 대화품질 이득이 이 rung 에서 사라짐을 deterministically rule out 시).

## 9. 양방향 sibling

- sibling: [CLM/P4_PRODUCTION_ROADMAP.md](../CLM/P4_PRODUCTION_ROADMAP.md) @L5 ladder · @L6 dialogue-method-B
- 직속 부모: [H_863](./H_863_clm_dialogue_selfplay.md) (F-CLM-DIALOGUE mid — 본 H 가 한 rung 위로 climb)
- Q-TRUST A 재활용: [H_857](./H_857_clm_causal_band.md) · [H_858](./H_858_akida_edge_of_chaos_phi.md)
- 형제 corpus: [H_868](./H_868_clm_cc_dialogue_corpus.md) (lane① CC 대화 corpus 확장 — parallel, 경로 disjoint)
- UNIVERSE SSOT: [CLM-CANDIDATES.md](./CLM-CANDIDATES.md) group A
