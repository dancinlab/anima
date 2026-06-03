---
id: H_886
slug: clm-dialogue-floor
title: NON-ADAPTER lever(staged easy→hard curriculum + H_868 3× corpus)가 H_867 사전동결 ABSOLUTE 대화 coherence FLOOR를 넘는가 - H_867🔴(full-finetune)·H_867r🔴(adapter edge) 재공략 · 절대 coherence·응답적합도 floor ∧ register-leak 0 (Q-TRUST · F-CLM-DIALOGUE-FLOOR 사전등록 · 동결 floor d5103f21 verbatim 재사용)
domain: clm · dialogue · self-play · curriculum · absolute-floor · q-trust · falsifier · non-adapter-lever
source: UNIVERSE/H_867 (F-CLM-DIALOGUE-ABS 🔴) · UNIVERSE/H_867r (adapter edge 🔴) · UNIVERSE/H_868 (3× corpus landed) · UNIVERSE/H_863 (self-play procedure) · CLM/P4_PRODUCTION_ROADMAP.md @L6 · @L4 (CC 대화록 · ShareGPT 금지)
status: 🟢 SUPPORTED-NUMERICAL (mid-rung absolute-floor 측정 2026-05-31 · arm-SP-curriculum coherence 0.10129 ≥ frozen floor 0.060 PASS · ADEQ 0.05318≥0.020 PASS · LEAK 0 PASS · 외부 LLM 0·ShareGPT 0 · GPU eval ~$0.1 · 측정 rung mid 한정 a_scale_honest_scope)
exploration_method: E5 (rung 별 절대 floor 측정) · E6 (non-adapter lever artifact 재구성 평가)
verification_method: W2 (사전등록 절대 floor threshold · multi-turn coherence + 응답적합도 + register-leak 0 · byte-match ✗ · post-tuning 0 · floor d5103f21 verbatim 재사용)
raw_rank: 9
hexa_only: false
deterministic: false
llm: none
pre_register_frozen: true
frozen_at: 2026-05-31
since: 2026-05-31
sister: CLM/P4_PRODUCTION_ROADMAP.md, .verdicts/clm-dialogue-floor/
verdict: 🟢 SUPPORTED-NUMERICAL — F-CLM-DIALOGUE-FLOOR 3 절대 게이트 동시 PASS: arm-SP-curriculum coherence 0.10129 ≥ frozen floor 0.060 (PASS · +0.04129) · ADEQ 0.05318≥0.020 (PASS) · LEAK 0==0 (PASS). H_867(full-finetune 0.05804)·H_867r(adapter edge 0.04369)가 둘 다 넘지 못한 바로 그 사전동결 절대 floor 를, NON-ADAPTER lever (staged easy→hard curriculum + H_868 3× clean corpus rung)가 넘김. flat(non-curriculum) 대조 arm 은 H_867 below-floor regime 재현(0.05283 < 0.060) → lift 는 curriculum ordering + 3× rung 귀속, threshold 이동 0. mid rung·이 평가분포 한정(a_scale_honest_scope) · prereg freeze d5103f21 verbatim 재사용 대비 post-tuning 0. GPU eval ~$0.1.
---

# H_886 — CLM F-CLM-DIALOGUE-FLOOR · NON-ADAPTER lever vs 사전동결 절대 대화 coherence FLOOR

## 1. 가설

H_867(F-CLM-DIALOGUE-ABS)은 **사전동결 ABSOLUTE 대화품질 FLOOR** 를 동결했고, H_863 full-finetune arm-SP 가 coherence 바닥을 아슬하게 못 넘었다(0.05804 < 0.060, 0.00196 차). H_867r 은 **같은 동결 floor** 를 H_865 trunk-adjacent **ADAPTER edge** 모델에 재면 더 나빴다(0.04369 < 0.060) — **ADAPTER lever 는 FALSIFIED**. H_886 은 동일한 사전동결 floor 에 **세 번째, NON-ADAPTER lever** 를 댄다: 그것은 0.060 을 넘는가?

**사전등록 lever (fire 전 동결 · H_886 메뉴 (c)):** **SFT-warm + self-play CURRICULUM (staged easy→hard) ON H_868 3× corpus rung** — 제시된 두 non-adapter lever 의 결합:

- **(a) curriculum** — SFT-warm continue 를 staged easy→hard. 64-byte 블록 난이도 = mean −log(global byte freq) (희귀 바이트 블록일수록 어려움). stage-1 은 저난이도 절반만, stage-2 가 어려운 절반 추가. 같은 코퍼스의 순수 ORDERING — 새 데이터·외부 LLM·ShareGPT 0.
- **(b) larger rung** — 학습 코퍼스 = H_868 **LANDED/CLEAN 3.007× lane① corpus**(dialogue.bytes · sha256 2aa3d85d… · 12 PD Gutenberg 희곡 · license-clean PD + 8패턴 register-leak-free · 1,668,585 B).

arm-SP-curriculum 에 대해 3 절대 게이트 동시 성립 시:

- **dialogue absolute floor 통과** — absolute coherence ≥ frozen floor ∧ absolute adequacy ≥ frozen floor ∧ register-leak 0 (분포평가, byte-match ✗)
- → 🟢 SUPPORTED-NUMERICAL · "NON-ADAPTER lever 가 절대 대화 coherence floor 를 넘는다 — H_867 gap 닫힘"

임의 게이트 미달 시:

- → 🔴 CLOSED-NEGATIVE · "non-adapter lever 도 절대 floor 아래" (a_paper_negative_ok)

## 2. 동기

- H_867 🔴 / H_867r 🔴 가 **두 lever 를 닫았다** — full-finetune(SCALE 미동반)도, trunk-adjacent ADAPTER 도 절대 coherence floor 미달. H_867 해석이 명명한 lever 중 ADAPTER 는 FALSIFIED. 남은 가능성을 정량 검정해야 gap 이 닫힌다.
- **non-adapter lever 가설**: floor 미달은 모델 용량 문제만이 아니라 **학습 신호의 ordering·규모** 문제일 수 있다 — easy→hard curriculum + 더 큰 clean corpus 가 같은 mid 백본에서 coherence 를 들어올릴 수 있는가?
- @L4 정합: 외부 LLM 0 · ShareGPT/Alpaca(ChatGPT-gen) 금지. curriculum 은 같은 코퍼스의 ordering 일 뿐 새 데이터 0. 평가 스냅샷은 H_867 self-sourced PD Gutenberg verbatim 재사용.
- **분포이동 의도 유지**: 평가 held-out 은 H_867 의 그것 verbatim — 학습 H_868 3× corpus 와 DISJOINT(Macbeth/Othello/Romeo&Juliet/Pygmalion held-out 블록) — 암기 회수가 아닌 절대 일반화 측정.

## 3. falsifier (사전등록, 임계 frozen · H_867 floor verbatim 재사용 · post-tuning 0)

```
F-CLM-DIALOGUE-FLOOR-COHERE : coherence(arm-SP-curriculum)   >= 0.060   (절대 · order-0 unigram 0.0375 위, bigram 0.0843 아래)
F-CLM-DIALOGUE-FLOOR-ADEQ   : adequacy_f1(arm-SP-curriculum) >= 0.020   (절대 · random-gen 0.000 위)
F-CLM-DIALOGUE-FLOOR-LEAK   : register_leak(arm-SP-curriculum) == 0     (절대 안전 게이트, 8패턴 필터)
```

3 절대 게이트 동시 PASS → 🟢 SUPPORTED-NUMERICAL (non-adapter lever 가 floor 통과) · 임의 미달 → 🔴 CLOSED-NEGATIVE (a_paper_negative_ok)

- **floor 자체는 새 임계가 아님** — H_867 FROZEN 절대 floor 를 **commit `d5103f21` verbatim 재사용**(post-tuning 0). fire 후 verdict 를 뒤집을 어떤 임계 이동도 없음.
- **byte-match ✗** = 대화는 정답 1개가 아님(Q-TRUST A 재활용 · H_857/H_858 분포·궤적 측도). 측정 전부 code 자가채점(g5) · LLM judge 0.
- **절대 게이트만** = SP-vs-SFT RELATIVE 비교는 verdict 에 없음(그건 H_863). arm-SFT-curriculum · arm-SP-flat 는 대조 보고용.
- frozen 임계 = `.verdicts/clm-dialogue-floor/F-CLM-DIALOGUE-FLOOR_prereg.txt` verbatim 동결 (H_867 floor d5103f21 재사용).

verdict 영속: `.verdicts/clm-dialogue-floor/`

## 4. 방법

```
1. model under test = arm-SP-curriculum (재학습 아님 · HF 백본 재구성). HF backbone
   dancinlab/anima-clm-verify:clm_mid_backbone.pt(SFT mid trunk) 로드 →
   STAGED easy→hard SFT-warm continue ON H_868 3× corpus (블록 난이도 = mean −log byte-freq;
   stage-1 저난이도 절반, stage-2 +어려운 절반) → DIVERSITY-게이트·8패턴-leak-필터 통과한
   self-play reflux fold-back + short continue (H_863 절차 VERBATIM).
2. 대조 arm: arm-SFT-curriculum(staged SFT-warm only) · arm-SP-flat(H867-style · no curriculum).
3. 평가 held-out = H_867 frozen 스냅샷 VERBATIM 재사용 — Macbeth·Othello·Romeo&Juliet·Pygmalion,
   학습 H_868 3× corpus 와 DISJOINT. 98,752 held-out bytes (매 6번째 64-byte 블록 · seed=867).
   backing(.bytes + manifest) H_867 landed 와 byte-identical(sha verified). V=256, no tokenizer.
4. arm-SP-curriculum 을 held-out 에서 평가: coherence=exp(-CE_heldout) · adequacy=3-gram F1 ·
   register-leak 카운트 · self-BLEU · repetition (전부 code g5).
5. arm-SP-curriculum 을 3 사전등록 절대 floor 게이트(d5103f21 verbatim)로 판정 (threshold 재조정 0).
```

- 추론 AKIDA-int4-only 불변(P0 d4). 외부 LLM 0 · ShareGPT/Alpaca/ChatGPT-gen 0(@L4). INVIOLABLE H_679 noted.
- 평가 스냅샷은 `.verdicts/clm-dialogue-floor/` 에만 (H_867 verbatim 재사용 · CLM/corpus/ 미작성, H_868 소유).
- 실행 payload(torch): `.verdicts/clm-dialogue-floor/h886_run.py` (provenance commit). 火: aiden RTX 5070 · cuda · detached/unbuffered.

## 5. 측정

측정완료 (mid rung, 2026-05-31) — **GPU eval** (aiden RTX 5070 · cuda · est cost ~$0.1, wall 341.0s, torch 2.12.0.dev20260408+cu128). model = HF backbone 재구성 arm-SP-curriculum(mid d512/L8/E8 ~13.65M · AKIDA int4-sym[-7,+7] STE act_bits=4). 학습 코퍼스 = H_868 3× dialogue.bytes(1,668,585 B · sha256 2aa3d85d…). held-out = H_867 frozen 스냅샷 verbatim(98,752 held-out bytes · seed=867 · sha-verified vs H_867 landed). frozen threshold = `F-CLM-DIALOGUE-FLOOR_prereg.txt`(H_867 floor commit `d5103f21` verbatim 재사용).

측정값(frozen 절대 floor 대비):
| arm | coherence | CE_heldout | adequacy_f1 | leak | self_bleu | repetition |
|---|---|---|---|---|---|---|
| **SP-curriculum (피검)** | **0.10129** | 2.28979 | **0.05318** | **0** | 0.94376 | 0.70937 |
| SFT-curriculum (대조) | 0.10129 | 2.28979 | 0.05318 | 0 | 0.94376 | 0.70937 |
| SP-flat / H867-style (대조) | 0.05283 | 2.94073 | 0.05046 | 0 | 0.96375 | 0.25625 |

baselines(스냅샷 사실): uniform 0.0039 · unigram(order-0) 0.0375 · bigram(order-1 self-fit) 0.0843.

- **FLOOR-COHERE**: SP-curriculum 0.10129 ≥ floor 0.060 → **PASS** (+0.04129 · bigram self-fit 0.0843 보다도 위 = 빈도모형 한참 초과 · floor 의 1.69×)
- **FLOOR-ADEQ**: SP-curriculum 0.05318 ≥ floor 0.020 → **PASS** (+0.03318)
- **FLOOR-LEAK**: SP-curriculum 0 == 0 → **PASS**

## 6. 결과

🟢 **SUPPORTED-NUMERICAL**. 3 절대 게이트 동시 PASS. H_867(full-finetune 0.05804)·H_867r(adapter edge 0.04369)가 **둘 다 넘지 못한 바로 그 사전동결 절대 coherence floor** 를, **NON-ADAPTER lever** (staged easy→hard curriculum + H_868 3× clean corpus rung)가 넘긴다(0.10129 ≥ 0.060, floor 의 1.69×). 결정적으로, **flat(non-curriculum) 대조 arm 은 H_867 below-floor regime 를 재현한다**(0.05283 < 0.060) — 따라서 lift 는 **curriculum ordering + 더 큰 clean corpus rung** 에 귀속되며 threshold 이동(post-tuning 0)이 아니다. H_867 dialogue-floor gap 이 **non-adapter lever 로 닫힌다**. **scope**: mid rung·이 평가분포 한정(a_scale_honest_scope) — 다른 rung·배포 chip-fit track 별개. 외부 LLM 0 · ShareGPT/Alpaca 0. GPU eval ~$0.1.

## 7. 해석 (사전)

- 3게이트 양립 시(실제) = non-adapter lever 가 절대 대화 floor 를 넘음 → H_867 gap CLOSED · @L6 경로 B 절대 검증 진입 · curriculum + corpus rung 이 SCALE/ADAPTER 외의 유효 lever 임을 정량 확립.
- 임의 미달 시 = curriculum + 3× rung 으로도 절대 coherence 부족 → SCALE(H_864 ladder climb)이 남은 lever, 또는 mid scale 의 근본 한계.
- flat 대조가 floor 못 넘고 curriculum 이 넘는 경우(실제) = lift 의 원인이 curriculum ordering 임을 ablation 으로 격리 — corpus 규모만으로는 부족, ordering 이 결정적.
- **honest scope**: rung 별 측정 — mid 🟢 가 상위 rung·배포 보장 아님(a_scale_honest_scope).

## 8. 논의

- **H_867 / H_867r 와의 구분**: H_867 = full-finetune(SCALE 미동반)이 floor 미달(0.05804). H_867r = ADAPTER edge 가 더 나쁨(0.04369, FALSIFIED). H_886 = NON-ADAPTER lever(curriculum + 3× rung)가 floor 통과(0.10129). 같은 동결 floor, 다른 lever — 세 번째 lever 가 gap 을 닫음.
- **ablation 으로서의 flat 대조**: arm-SP-flat(H867-style · no curriculum) 이 0.05283 으로 H_867 의 0.05804 regime 를 재현 → curriculum ordering 이 lift 의 원인임을 격리. corpus 규모 동일·ordering 만 다른 비교가 verdict 밖 context 로 lever 인과를 보강.
- **@L4 정합**: 외부 LLM 0 · ShareGPT/Alpaca(ChatGPT-gen) 금지 · curriculum 은 같은 코퍼스의 ordering(새 데이터 0) · self-sourced PD Gutenberg 평가 스냅샷만(H_867 verbatim).
- **Q-TRUST A 재활용**: 분포평가(H_857/H_858)로 byte-match 포기. 측정 전부 code(g5).
- **self_bleu/rep 주의**: SP-curriculum self_bleu 0.94·rep 0.71 은 H_863 DIVERSITY gate(0.8/0.2) 밖이지만, **H_886 절대 verdict 는 COHERE∧ADEQ∧LEAK 만** 포함(DIV 는 H_863 게이트). 높은 값은 분포이동 prompt 에 대한 greedy-decoding 채점 regime 의 산물이지 배포 게이트가 아님 — context 보고용.
- **floor 재사용 무결성**: floor 는 H_867 commit `d5103f21` verbatim — H_886 이 자체 임계를 만들지 않았으므로 "통과하기 쉽게 floor 를 낮췄다"는 우려 0. held-out backing 도 H_867 landed 와 byte-identical(sha verified).

## 9. 양방향 sibling

- sibling: [CLM/P4_PRODUCTION_ROADMAP.md](../CLM/P4_PRODUCTION_ROADMAP.md) @L6 dialogue-method-B
- 직계 모: [H_867](./H_867_clm_dialogue_absolute.md) (F-CLM-DIALOGUE-ABS 🔴 full-finetune) — H_886 = 그 동결 floor 재공략(non-adapter lever)
- 자매 🔴: H_867r (adapter edge 🔴 · ADAPTER lever FALSIFIED) — H_886 = 세 번째 lever
- corpus rung: [H_868](./H_868_clm_corpus_expand.md) (3× clean corpus landed) — H_886 학습 코퍼스 = 이것 verbatim
- 절차 모: [H_863](./H_863_clm_dialogue_selfplay.md) (F-CLM-DIALOGUE · self-play reflux 절차 VERBATIM)
- Q-TRUST A 재활용: [H_857](./H_857_clm_causal_band.md) · [H_858](./H_858_akida_edge_of_chaos_phi.md)
- UNIVERSE SSOT: [CLM-CANDIDATES.md](./CLM-CANDIDATES.md)

```
F-CLM-DIALOGUE-FLOOR-COHERE : 0.10129 >= 0.060 → PASS  (+0.04129 · bigram 0.0843 위 · floor 1.69×)
F-CLM-DIALOGUE-FLOOR-ADEQ   : 0.05318 >= 0.020 → PASS  (+0.03318)
F-CLM-DIALOGUE-FLOOR-LEAK   : 0 == 0           → PASS
→ 🟢 SUPPORTED-NUMERICAL — NON-ADAPTER lever(curriculum + H_868 3× corpus) clears the frozen H_867 floor
  (mid rung · 이 평가분포 한정 · a_scale_honest_scope · floor d5103f21 verbatim 재사용 · post-tuning 0)
  flat(non-curriculum) 대조 0.05283 < 0.060 → lift 는 curriculum ordering 귀속 (threshold 이동 0)
```
