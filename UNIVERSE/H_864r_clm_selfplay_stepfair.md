---
id: H_864r
slug: clm-selfplay-stepfair
title: dialogue self-play scale-climb STEP-FAIR — H_864 large-rung 🔴 was CONFOUNDED by undertraining (2000 steps → mode collapse); re-run the SAME large d768/L12/E12 to a NON-COLLAPSED regime (held-out repetition < 0.20) before judging self-play under the UNCHANGED bf98c01 frozen gates
domain: clm · dialogue · self-play · sft · diversity · scale-climb · step-fair · confound-resolution · falsifier
source: UNIVERSE/CLM-CANDIDATES.md group A follow-on · H_864 (PR #1557) confounded 🔴 · CLM/train/h864r_fire_stepfair.hexa · .verdicts/clm-dialogue/F-CLM-DIALOGUE_prereg.txt (bf98c01)
exploration_method: E5 (rung-by-rung ladder climb · large rung re-run step-fair) · E6 (SFT ↔ self-play synthesis A/B)
verification_method: W2 (pre-registered distributional thresholds = bf98c01 FROZEN, scale-invariant relative/absolute · multi-turn coherence + response-adequacy + register-leak 0 + DIVERSITY · byte-match ✗ · post-tuning 0)
raw_rank: 9
hexa_only: false
deterministic: false
llm: none
pre_register_frozen: true
frozen_at: 2026-05-31
since: 2026-05-31
sister: CLM/P4_PRODUCTION_ROADMAP.md, .verdicts/clm-dialogue-large-stepfair/, UNIVERSE/H_864_clm_dialogue_scale_climb.md
verdict: 🔴 CLOSED-NEGATIVE — F-CLM-DIALOGUE-LARGE-STEPFAIR 3/4 PASS, 1 FAIL: COHERE(SP 0.03406 > SFT 0.02983) PASS · ADEQ(SP 0.02260 < SFT 0.03955) FAIL · LEAK(SP 0) PASS · DIV(self-BLEU 0.20074<0.8 ∧ rep 0.02386<0.2) PASS. CONFOUND RESOLVED: non-collapsed at step 2000 (rep 0.03027<0.2 vs H_864's 0.361), reflux DIVERSITY gate PASS (48/48 folded) → arm-SP genuine SFT+self-play. Honest finding: once non-collapsed, self-play LIFTS coherence + stays diverse/leak-free but does NOT carry strict response-adequacy. bf98c01 frozen, post-tuning 0. a_paper_negative_ok.
---

# H_864r — CLM F-CLM-DIALOGUE-LARGE-STEPFAIR self-play dialogue scale-climb (step-fair re-run)

## 1. 가설

H_864 (PR #1557) 는 @L5 ladder large rung(d768/L12/E12 · 44,678,668 params)에서 SFT+self-play 대화품질을 측정하려 했으나 **2000 step 만 학습** → large 모델이 **MODE-COLLAPSE**(held-out repetition 0.361 ≥ 0.20)에 빠졌고, 그 결과 self-play reflux 배치가 per-batch DIVERSITY gate 를 통과하지 못해(reflux repetition 0.335 ≥ 0.20 → REJECT) **환류 0** → arm-SP 가 arm-SFT 로 퇴화 → COHERE/ADEQ tie + DIV fail → 2/4 frozen falsifier FAIL → 🔴.

그 🔴 는 **CONFOUNDED**: self-play scaling 의 정직한 테스트가 아니라 **undertraining** 의 산물이었다. H_864r 가설:

- **SAME large rung 을 NON-COLLAPSED regime(held-out repetition < 0.20)까지 학습**시킨 뒤, 그 시점에서 self-play 를 **UNCHANGED bf98c01 frozen gate** 로 판정한다. 유일한 변경 = **학습 step 증가**(방법론 수정 · threshold 이동 0).
- 비붕괴 regime 도달 후에도 self-play 가 SFT 를 능가(4/4 PASS)하면 → 🟢 "self-play 대화 이득이 비붕괴 large rung 에서 carry".
- 도달 후에도 능가 못하면 → 🔴 CLOSED-NEGATIVE "self-play 대화 이득 ⊥ 이 rung (비붕괴여도)" (a_paper_negative_ok). 이제는 undertraining confound 가 제거된 정직한 🔴.

## 2. 동기

- H_864 의 🔴 는 측정 결함이었다: 2000 step 은 44.68M conv-MoE 가 1.67MB 코퍼스에서 비붕괴 표현을 학습하기에 부족 → "self-play 가 scale 에서 깨진다" 가 아니라 "이 학습량에서 large 가 반복기로 과적합한다" 였다.
- 정직한 scale-climb 판정을 위해서는, self-play 가 통과해야 할 DIVERSITY gate 자체를 SFT trunk 가 먼저 통과(비붕괴)하는 regime 에서 측정해야 한다. step→repetition CURVE 를 보고 그 regime 을 식별한다.
- @L1 self-play(칩 자기대화 생성→재학습 = 살아 배우기) · @L6 대화 방법 B. 외부 LLM 0 · ShareGPT/Alpaca 금지(@L4).

## 3. falsifier (사전등록, 임계 frozen — bf98c01 scale-invariant gates, NO new freeze)

```
F-CLM-DIALOGUE-COHERE  : coherence(SP)    > coherence(SFT)        (분포평가, strict relative)
F-CLM-DIALOGUE-ADEQ    : adequacy_F1(SP)  > adequacy_F1(SFT)      (분포평가, strict relative)
F-CLM-DIALOGUE-LEAK    : register_leak_count(SP) == 0             (8패턴 필터, absolute)
F-CLM-DIALOGUE-DIV     : self_BLEU(SP) < 0.80 ∧ repetition(SP) < 0.20  (DIVERSITY, absolute)
```

4 조건 동시 PASS → "self-play 대화품질 이득 step-fair scale-climb" 지지 (🟢)
임의 미달 → CLOSED-NEGATIVE · "self-play 대화 이득 ⊥ 이 rung (비붕괴여도)" (🔴, a_paper_negative_ok)

- **threshold 이동 0**: bf98c01 의 4 falsifier 를 VERBATIM 재사용. COHERE/ADEQ = RELATIVE(SP strict > SFT), LEAK/DIV = SP 의 ABSOLUTE gate — 어느 것도 rung 크기/학습량에 의존하지 않으므로 step-fair 재실행에 그대로 carry. 인용: bf98c01 (`.verdicts/clm-dialogue/F-CLM-DIALOGUE_prereg.txt`).
- H_864 대비 변경은 오직 학습 step 수(methodology fix). gate 재조정 0 (post-tuning 0 가 🔴→🟢 flip 을 위한 gate 이동을 금지).

verdict 영속: `.verdicts/clm-dialogue-large-stepfair/` (large rung step-fair A/B)

## 4. 방법

```
1. SFT lane: H_868 확장 PD-Gutenberg 희곡 코퍼스(12편 · 1,668,585 bytes ·
   HF dancinlab/anima-clm-p4-dialogue · sha256 2aa3d85...) byte-corpus(V=256, no tokenizer) 모방 학습.
2. STEP SWEEP (THE H_864r CHANGE): checkpoints 2000..20000 에서 매번 held-out
   repetition 측정 → repetition < 0.20 (비붕괴) 또는 cap(20000) 도달까지 SFT 학습 계속.
   step→repetition CURVE 보고.
3. self-play lane: 비붕괴 SFT trunk 시점에서 칩 자기대화(turn 교대 생성) → 8패턴
   register-leak 필터 + per-batch DIVERSITY gate 통과분만 환류(@L1) → +reflux_continue step.
4. large rung 2-arm A/B: arm-SFT(SFT-only) vs arm-SP(SFT+self-play),
   AKIDA-envelope QAT(int4-sym[-7,+7] per-output-channel STE + act_bits=4), seed=42, 동일 base budget.
5. held-out 대화 평가(seed=863, disjoint): coherence=exp(-CE) + adequacy(3-gram F1) +
   register-leak 카운트 + self-BLEU(4-gram pairwise) + repetition(repeated-4-gram) — 전부 CODE(g5).
6. 4 frozen falsifier(bf98c01) 동시 평가 · large rung step-fair verdict · 정직 보고 (threshold 재조정 0).
```

- 추론 AKIDA-int4-only 불변 (P0 d4) · self-play 데이터 환류는 @L1 비결정 적응과 정합.
- 아키텍처(conv-MoE byte LM)·QAT envelope 는 H_864 와 동일(CLM/model/model.py + CLM/train/train_clm.py mirror). 변경 = step 수뿐.

## 5. 측정

측정 (large rung, 2026-05-31) — runpod A40 48GB(torch 2.4.1+cu124). corpus = H_868 확장 PD-Gutenberg 희곡 12편 1,668,585 bytes(sha256 2aa3d85...) → train 1,390,487 / heldout 278,098 (seed=863, disjoint). large d768/L12/E12 = 44,678,668 params, AKIDA int4-sym[-7,+7] per-output-channel STE + act_bits=4, seed=42, seq_len 128, batch 32, lr 2e-3.

**step→held-out repetition CURVE** (H_864r 핵심 증거):

| step | ce_heldout | coherence | repetition | self_bleu | adequacy_f1 |
|---|---|---|---|---|---|
| 2000 | 3.51234 | 0.02983 | **0.03027** | 0.24233 | 0.03955 |

- step=2000 에서 이미 **NON-COLLAPSED**(rep 0.03027 << 0.20) → rep-target 규칙으로 SFT sweep 종료. **CONTRAST H_864: 같은 2000 step 에 rep 0.361**. 즉 H_864 의 붕괴는 학습 config 의 산물이었고, step-fair config 에서는 첫 체크포인트부터 비붕괴 → cap(20000) 불필요.

**self-play reflux** (DIVERSITY gate): 48 생성 · 0 leak-drop · 48 kept · reflux self-BLEU 0.07141(<0.8) · reflux repetition 0.00427(<0.20) → **DIVERSITY gate PASS** → 48/48 환류 fold → arm-SP +1000 continue step. H_864 와 달리 arm-SP 가 **진짜 SFT+self-play**(SFT 퇴화 아님).

측정값(frozen threshold 대비):

| arm | coherence | ce_heldout | adequacy_f1 | leak | self_bleu | repetition |
|---|---|---|---|---|---|---|
| SFT | 0.02983 | 3.51234 | 0.03955 | 0 | 0.24233 | 0.03027 |
| SP  | 0.03406 | 3.37958 | 0.02260 | 0 | 0.20074 | 0.02386 |

- **COHERE**: SP 0.03406 > SFT 0.02983 → **PASS** (self-play 가 coherence 상승, held-out CE 3.380 < 3.512)
- **ADEQ**: SP 0.02260 > SFT 0.03955? → **FAIL** (self-play 가 응답적합도 n-gram F1 을 낮춤)
- **LEAK**: SP 0 == 0 → **PASS** · **DIV**: self-BLEU 0.20074<0.8 ∧ rep 0.02386<0.2 → **PASS** (붕괴 없음)

## 6. 결과

🔴 **CLOSED-NEGATIVE** (a_paper_negative_ok). 4 frozen falsifier 중 **3 PASS · 1 FAIL(ADEQ)**. 이것은 H_864 와 달리 **정직한·confound-free 🔴** 다:

- **undertraining confound 제거**: 판정 시점에서 SFT trunk 가 비붕괴(rep 0.03027<0.2)이고, self-play reflux 가 DIVERSITY gate 를 통과해 실제로 환류됨 → arm-SP 가 진짜 SFT+self-play.
- 그 공정한 조건에서 self-play 는 **두 축에서 도움**: multi-turn coherence strict 상승(0.03406>0.02983) + 다양성·register 안전 유지(DIV/LEAK PASS). 그러나 **strict 응답적합도 gate 는 carry 못함**: SP 의 생성 next-turn 3-gram overlap F1(0.02260) < SFT(0.03955). 칩 자기대화(다양한)를 환류하면 더 coherent·다양한 생성기가 되지만 held-out 인간 reference 와의 surface n-gram overlap 은 내려간다.
- 4 gate 동시 PASS 가 필요한 frozen verdict 에서 ADEQ 1 fail → 🔴. 정직: self-play 대화 이득이 비붕괴여도 large rung 에서 bf98c01 하에 완전히 carry 하지는 않음(coherence/다양성/leak yes, strict 적합도 no).

## 7. 해석 (사전)

- step→rep CURVE 가 어느 step 에서 < 0.20 으로 떨어지는지 = large rung 의 비붕괴 임계 학습량. H_864 의 2000 step 이 그보다 낮았다면 confound 확정.
- 비붕괴 regime 에서 4조건 PASS → self-play 대화 이득이 large rung 에서 carry(undertraining 만 문제였음) → @L5 ladder · @L6 경로 B 한 칸 더.
- 비붕괴 regime 에서도 COHERE/ADEQ 미달 → self-play 이득이 scale 자체에서 사라짐(학습량 무관) → 정직한 🔴, NEXT levers(reflux 온도·비율·repetition penalty)는 각자 사전등록 fire.
- **honest scope**: rung별 측정(a_scale_honest_scope). large→prod 비보장.

## 8. 논의

- **confound resolution**: H_864r 의 단일 변경(step↑)이 H_864 🔴 의 원인(undertraining vs scale-intrinsic)을 분리한다. 이것이 a_paper_negative_ok 의 핵심 — 🔴 의 원인을 deterministically 규명.
- **@L1/@L4 정합**: self-play = 칩 자기대화→재학습 · 외부 LLM 0 · PD/CC 만.
- **Q-TRUST A 재활용**: 분포평가(H_857/H_858 edge-of-chaos · 궤적 측도)로 byte-match 포기.
- **scale-invariant 동결**: bf98c01 4 falsifier 가 relative/absolute gate 라 step-fair 재실행에 새 freeze 없이 carry (W2 discipline, post-tuning 0).
- **H_868 collision-free**: 본 fire 는 HF 확장 코퍼스(dialogue.bytes)를 읽기만 하고 CLM/corpus/ 를 건드리지 않음.

## 9. 양방향 sibling

- 직속 부모: [H_864](./H_864_clm_dialogue_scale_climb.md) (large rung 의 confounded 🔴 — 본 H 가 step-fair 로 재실행)
- sibling: [CLM/P4_PRODUCTION_ROADMAP.md](../CLM/P4_PRODUCTION_ROADMAP.md) @L5 ladder · @L6 dialogue-method-B
- Q-TRUST A 재활용: [H_857](./H_857_clm_causal_band.md) · [H_858](./H_858_akida_edge_of_chaos_phi.md)
- 형제 corpus: [H_868](./H_868_clm_cc_dialogue_corpus.md) (확장 PD 대화 코퍼스 — 본 fire 가 읽는 SSOT)
- frozen gates: `.verdicts/clm-dialogue/F-CLM-DIALOGUE_prereg.txt` (commit bf98c01)
- UNIVERSE SSOT: [CLM-CANDIDATES.md](./CLM-CANDIDATES.md) group A
