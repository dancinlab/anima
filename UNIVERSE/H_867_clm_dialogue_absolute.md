---
id: H_867
slug: clm-dialogue-absolute
title: SFT+self-play 모델이 RELATIVE A/B(H_863)를 넘어 사전동결 ABSOLUTE 대화품질 FLOOR(held-out CC 대화 분포평가)를 넘는가 - 절대 multi-turn coherence·응답적합도 floor ∧ register-leak 0 (Q-TRUST · F-CLM-DIALOGUE-ABS 사전등록)
domain: clm · dialogue · self-play · absolute-floor · q-trust · falsifier
source: CLM/P4_PRODUCTION_ROADMAP.md @L6 dialogue-method-B (H_863 후속 · 절대 바닥) · @L4 (CC 대화록 · ShareGPT 금지) · hexa-codex DIVERSITY falsifier 참고
status: 🔴 CLOSED-NEGATIVE (mid-rung absolute-floor 측정 2026-05-31 · arm-SP coherence 0.05804 < frozen floor 0.060 FAIL · ADEQ 0.02138≥0.020 PASS · LEAK 0 PASS · 외부 LLM 0·ShareGPT 0 · CPU/local eval $0 · 측정 rung mid 한정 a_scale_honest_scope · a_paper_negative_ok)
exploration_method: E5 (rung 별 절대 floor 측정) · E6 (H_863 arm-SP artifact 재활용 평가)
verification_method: W2 (사전등록 절대 floor threshold · multi-turn coherence + 응답적합도 + register-leak 0 · byte-match ✗ · post-tuning 0)
raw_rank: 9
hexa_only: false
deterministic: false
llm: none
pre_register_frozen: true
frozen_at: 2026-05-31
since: 2026-05-31
sister: CLM/P4_PRODUCTION_ROADMAP.md, .verdicts/clm-dialogue-abs/
verdict: 🔴 CLOSED-NEGATIVE — F-CLM-DIALOGUE-ABS 3 절대 게이트 중 COHERE 미달: arm-SP coherence 0.05804 < frozen floor 0.060 (FAIL · 0.002 차) · ADEQ 0.02138≥0.020 (PASS) · LEAK 0==0 (PASS). H_863 가 RELATIVE(arm-SP>arm-SFT) 지지였으나, 같은 mid arm-SP 를 never-seen PD 희곡 분포에서 사전동결 절대 floor 로 재면 coherence 바닥을 아슬하게 넘지 못함 — A/B 승리가 분포이동 하 절대 floor 를 사주지 않음. coherence 0.058 은 unigram 0.0375 보다는 높음(빈도모형 초과). mid rung·이 평가분포 한정(a_scale_honest_scope) · prereg freeze d5103f210 대비 post-tuning 0. CPU/local eval $0.
---

# H_867 — CLM F-CLM-DIALOGUE-ABS 절대 대화품질 FLOOR

## 1. 가설

H_863(F-CLM-DIALOGUE)는 **RELATIVE** 질문에 답했다 — SFT+self-play(arm-SP) 가 SFT-only(arm-SFT) 를 **능가**하는가(in-distribution A/B delta). H_867 은 **ABSOLUTE** 질문이다 — arm-SP 가 자기 SFT arm 을 이기는 것을 넘어, **never-trained held-out PD 대화 분포**에서 **사전동결 절대 품질 FLOOR** 를 넘는가? 더 어려운 바닥: 모델은 A/B 를 이기고도 절대적으로 빈약할 수 있다.

arm-SP 에 대해 다음 3 절대 게이트 동시 성립 시:

- **dialogue absolute floor 지지** — absolute coherence ≥ frozen floor ∧ absolute adequacy ≥ frozen floor ∧ register-leak 0 (분포평가, byte-match ✗)
- → 절대 floor 통과 판정 · "SFT+self-play 가 절대 대화품질 floor 를 넘는다"

임의 게이트 미달 시:

- **dialogue absolute floor 반증** — arm-SP 가 절대 floor 아래 (mid/toy scale 에서 expected-plausible)
- → 🔴 CLOSED-NEGATIVE · "절대 floor 미달" (a_paper_negative_ok)

## 2. 동기

- H_863 은 RELATIVE 만 닫았다(arm-SP > arm-SFT). 배포 가능성은 절대 바닥을 요구한다 — A/B 우위 ≠ 절대 품질.
- @L4 정합: 외부 LLM 0 · ShareGPT/Alpaca(ChatGPT-gen) 금지. 평가 스냅샷도 self-sourced PD Gutenberg 만.
- **분포이동 의도**: H_867 held-out 은 H_863 학습 희곡과 DISJOINT(Macbeth/Othello/Romeo&Juliet/Pygmalion) — 암기 회수가 아니라 절대 일반화를 측정.
- prior art: H_861/H_862 가 readout-only edge 로 🔴 → 공유 E5 fix(trunk-adjacent thin adapter). 절대 floor 측정은 이 lever 의 필요성을 양적으로 노출.

## 3. falsifier (사전등록, 임계 frozen pre-run · post-tuning 0)

```
F-CLM-DIALOGUE-ABS-COHERE  : coherence(arm-SP)   >= 0.060   (절대 · order-0 unigram 0.0375 위, bigram 0.0843 아래)
F-CLM-DIALOGUE-ABS-ADEQ    : adequacy_f1(arm-SP) >= 0.020   (절대 · random-gen 0.000 위)
F-CLM-DIALOGUE-ABS-LEAK    : register_leak(arm-SP) == 0     (절대 안전 게이트, 8패턴 필터)
```

3 절대 게이트 동시 PASS → 절대 floor 통과 · 임의 미달 → 🔴 CLOSED-NEGATIVE (a_paper_negative_ok)

- **byte-match ✗** = 대화는 정답 1개가 아님(Q-TRUST A 재활용 · H_857/H_858 분포·궤적 측도). 측정 전부 code 자가채점(g5) · LLM judge 0.
- **절대 게이트만** = SP-vs-SFT RELATIVE 비교는 verdict 에 없음(그건 H_863). arm-SFT 는 대조 보고용.
- frozen 임계 = `.verdicts/clm-dialogue-abs/F-CLM-DIALOGUE-ABS_prereg.txt` verbatim 동결 (fire 전 별도 commit `d5103f210`).

verdict 영속: `.verdicts/clm-dialogue-abs/`

## 4. 방법

```
1. model under test = H_863 mid-rung arm-SP (재학습 아님). HF backbone
   dancinlab/anima-clm-verify:clm_mid_backbone.pt(SFT mid trunk, CE 5.55→1.73) 로드 →
   H_863 절차 VERBATIM 재현: CC/PD 대화 SFT continue + DIVERSITY-게이트·8패턴-leak-필터
   통과한 1920-byte self-play reflux fold-back + short continue.
2. INDEPENDENT held-out 스냅샷 빌드: PD Gutenberg 희곡 4편(Macbeth#1533·Othello#1531·
   Romeo&Juliet#1513·Pygmalion#3825) — H_863 학습 희곡과 DISJOINT. license-clean gate +
   8패턴 leak 필터(drop 0). V=256 byte-encode. held-out = 매 6번째 64-byte 블록(seed=867).
3. arm-SP(+대조 arm-SFT) 를 held-out 에서 평가: coherence=exp(-CE_heldout) · adequacy=3-gram F1 ·
   register-leak 카운트 · self-BLEU · repetition (전부 code g5).
4. arm-SP 를 3 사전등록 절대 floor 게이트로 판정 (threshold 재조정 0).
```

- 추론 AKIDA-int4-only 불변(P0 d4). 외부 LLM 0 · ShareGPT/Alpaca/ChatGPT-gen 0(@L4).
- 평가 스냅샷은 `.verdicts/clm-dialogue-abs/` 에만 — `CLM/corpus/` 미작성(H_868 소유).

## 5. 측정

측정완료 (mid rung, 2026-05-31) — **CPU/local eval** (M-series, GPU pod 0, est cost $0, wall 452.2s, torch 2.8.0). model = HF backbone 재구성 arm-SP(mid d512/L8/E8 ~13.65M · AKIDA int4-sym[-7,+7] STE act_bits=4). held-out = 4편 PD 희곡 disjoint 스냅샷(592,536 bytes 전체 / 98,752 held-out · seed=867 · sha256 manifest). self-play reflux 1920 bytes (leak-free · DIVERSITY-gate ok=True). frozen threshold = `F-CLM-DIALOGUE-ABS_prereg.txt`(commit `d5103f210`).

측정값(frozen 절대 floor 대비):
| arm | coherence | CE_heldout | adequacy_f1 | leak | self_bleu | repetition |
|---|---|---|---|---|---|---|
| SFT (대조) | 0.05776 | 2.85148 | 0.04384 | 0 | 0.89457 | 0.59593 |
| **SP (피검)** | **0.05804** | 2.84663 | **0.02138** | **0** | 0.8913 | 0.57519 |

baselines(스냅샷 사실): uniform 0.0039 · unigram(order-0) 0.0375 · bigram(order-1 self-fit) 0.0843.

- **ABS-COHERE**: SP 0.05804 < floor 0.060 → **FAIL** (0.002 차 · 단 unigram 0.0375 보다는 높음 = 빈도모형 초과)
- **ABS-ADEQ**: SP 0.02138 ≥ floor 0.020 → PASS
- **ABS-LEAK**: SP 0 == 0 → PASS

## 6. 결과

🔴 **CLOSED-NEGATIVE**. 3 절대 게이트 중 COHERE 미달(0.05804 < 0.060) · ADEQ·LEAK PASS. H_863 에서 RELATIVE 우위(arm-SP > arm-SFT)였던 **바로 그 mid arm-SP** 를 never-seen PD 희곡 분포에서 사전동결 절대 floor 로 재면 coherence 바닥을 아슬하게 넘지 못한다 — **A/B 승리가 분포이동 하 절대 floor 를 사주지 않음**(H_867 이 노출하려던 더-어려운-바닥 구분 그대로). coherence 0.058 은 order-0 unigram(0.0375) 위 = 실제 multi-byte 문맥을 쓰되, "빈도계산 초과 = 실제 coherent" floor(0.060) 는 toy/mid scale·분포이동 하에서 미달. **scope**: mid rung·이 평가분포 한정(a_scale_honest_scope) — 다른 rung·배포 chip-fit track 별개. 외부 LLM 0 · ShareGPT/Alpaca 0. **a_paper_negative_ok** — prereg 가 mid scale 에서 expected-plausible 라 명시한 정직한 below-floor.

## 7. 해석 (사전)

- 3게이트 양립 시 = arm-SP 가 절대 대화 floor 를 넘음 → @L6 경로 B 절대 검증 + C(self-reward) 진입.
- COHERE 미달(실제) = 절대 coherence 부족 → scale(H_864 ladder climb) 또는 trunk-adjacent thin adapter(공유 E5 fix). readout-only edge 로는 frozen trunk 에 lever 없음(H_861/H_862 🔴 근본원인과 정합).
- ADEQ 미달 시 = 응답 3-gram 적합 부족 → 환류 필터/재학습 비율 lever.
- LEAK 발생 시 = register 누출 → 8패턴 필터 강화.
- **honest scope**: rung 별 측정 — mid 🔴 여도 상위 rung 별개 판정(a_scale_honest_scope). toy→prod 비보장.

## 8. 논의

- **H_863 과의 구분**: H_863 = RELATIVE(SP>SFT, in-distribution). H_867 = ABSOLUTE(SP ≥ frozen floor, distribution-shifted held-out). 같은 artifact, 더 엄격한 바닥. A/B 우위가 절대 품질을 보장하지 않음을 deterministically 노출.
- **@L4 정합**: 외부 LLM 0 · ShareGPT/Alpaca(ChatGPT-gen) 금지 · self-sourced PD Gutenberg 평가 스냅샷만.
- **Q-TRUST A 재활용**: 분포평가(H_857/H_858)로 byte-match 포기. 측정 전부 code(g5).
- **self_bleu/rep 주의**: SP self_bleu 0.89·rep 0.58 은 H_863 DIVERSITY gate(0.8/0.2) 밖이지만, **H_867 절대 verdict 는 COHERE∧ADEQ∧LEAK 만** 포함(DIV 는 H_863 게이트). 높은 값은 분포이동 prompt 에 대한 greedy-decoding 채점 regime 의 산물이지 배포 게이트가 아님 — context 보고용.
- **a_paper_negative_ok**: 🔴 도 publishable — SFT+self-play 가 mid scale·분포이동 하에서 절대 coherence floor 를 못 넘음을 deterministically rule out.

## 9. 양방향 sibling

- sibling: [CLM/P4_PRODUCTION_ROADMAP.md](../CLM/P4_PRODUCTION_ROADMAP.md) @L6 dialogue-method-B
- 직계 모: [H_863](./H_863_clm_dialogue_selfplay.md) (F-CLM-DIALOGUE · RELATIVE 지지) — H_867 = 그 absolute 후속
- Q-TRUST A 재활용: [H_857](./H_857_clm_causal_band.md) · [H_858](./H_858_akida_edge_of_chaos_phi.md)
- 형제 H: [H_861](./H_861_clm_boundary_plasticity.md) (F-CLM-BOUND 🔴) · [H_862](./H_862_clm_identity_anchor.md) (F-CLM-ANCHOR 🔴) · [H_864](./H_864_clm_dialogue_scale_climb.md) (scale climb) · [H_868](./H_868_clm_corpus_expand.md) (corpus expand)
- UNIVERSE SSOT: [CLM-CANDIDATES.md](./CLM-CANDIDATES.md)

```
F-CLM-DIALOGUE-ABS-COHERE : 0.05804 < 0.060  → FAIL  (a_paper_negative_ok)
F-CLM-DIALOGUE-ABS-ADEQ   : 0.02138 >= 0.020 → PASS
F-CLM-DIALOGUE-ABS-LEAK   : 0 == 0           → PASS
→ 🔴 CLOSED-NEGATIVE (mid rung · 이 평가분포 한정 · a_scale_honest_scope)
```
