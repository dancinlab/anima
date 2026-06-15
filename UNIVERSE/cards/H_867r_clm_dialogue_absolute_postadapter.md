---
id: H_867r
slug: clm-dialogue-absolute-postadapter
title: H_867 가 절대 coherence floor(0.060)를 0.002 미달(0.05804)했다 - 같은 사전동결 floor 를 H_865 trunk-adjacent ADAPTER edge 모델에 재적용하면 adapter 가 절대 coherence 를 0.060 위로 들어올리는가 (CLM-CANDIDATES group A follow-on · F-CLM-DIALOGUE-ABS-POSTADAPTER · floor REUSED VERBATIM d5103f21)
domain: clm · dialogue · self-play · absolute-floor · adapter-edge · q-trust · falsifier
source: UNIVERSE/H_867 (F-CLM-DIALOGUE-ABS 🔴 · 0.05804<0.060) · UNIVERSE/H_865 (trunk-adjacent adapter edge · F-CLM-BOUND 🟢) · CLM/model/h865_adapter_edge.py · CLM-CANDIDATES.md group A
status: 🔴 CLOSED-NEGATIVE (adapter-edge absolute-floor 측정 2026-05-31 · adapter arm-SP coherence 0.04369 < frozen floor 0.060 FAIL ∧ adapter arm-SP adequacy 0.01762 < 0.020 FAIL · LEAK 0 PASS · adapter 가 절대 coherence 를 0.060 위로 들어올리지 못함 — 오히려 H_867 full-finetune arm-SP 0.05804 보다 낮음 · 외부 LLM 0·ShareGPT 0 · CPU/local eval $0 wall 1770.9s · mid rung 한정 a_scale_honest_scope · a_paper_negative_ok)
exploration_method: E5 (rung 별 절대 floor 측정) · E6 (H_865 adapter-edge artifact 재활용 평가) · H_867 held-out 스냅샷 재활용
verification_method: W2 (사전동결 절대 floor threshold REUSED VERBATIM · F-CLM-DIALOGUE-ABS_prereg.txt commit d5103f21 · multi-turn coherence + 응답적합도 + register-leak 0 · byte-match ✗ · post-tuning 0)
raw_rank: 9
hexa_only: false
deterministic: false
llm: none
pre_register_frozen: true
frozen_at: 2026-05-31
since: 2026-05-31
sister: UNIVERSE/H_867, UNIVERSE/H_865, .verdicts/clm-dialogue-abs-postadapter/
verdict: 🔴 CLOSED-NEGATIVE — H_865 trunk-adjacent ADAPTER edge 모델을 H_867 의 같은 사전동결 절대 floor 로 재면 COHERE 미달(0.04369 < 0.060) ∧ ADEQ 미달(0.01762 < 0.020) · LEAK 0 PASS. adapter 가 F-CLM-BOUND(retain-while-learn) 게이트는 들어올렸으나 분포이동 held-out 절대 대화품질은 들어올리지 못함 — frozen backbone+readout 위 thin rank-64 adapter 는 full-finetune 보다 절대 coherence 표현여유가 적어 H_867 의 full-finetune arm-SP(0.05804) 보다도 낮다. adapter 는 0.060 위로 coherence 를 들어올리지 못함 🔴. mid rung·이 평가분포 한정(a_scale_honest_scope) · prereg freeze d5103f21 대비 post-tuning 0. CPU/local eval $0.
---

# H_867r — CLM F-CLM-DIALOGUE-ABS-POSTADAPTER 절대 대화품질 FLOOR (H_865 ADAPTER edge)

## 1. 가설

H_867(F-CLM-DIALOGUE-ABS)는 H_863 **full-finetune** arm-SP 를 never-trained held-out PD 대화 분포에서 사전동결 **절대 coherence FLOOR(0.060)** 로 재서 **0.002 미달(0.05804 < 0.060)** 했다 — A/B 우위(H_863 RELATIVE)가 절대 floor 를 사주지 않음. H_867r 은 **같은 사전동결 floor 를 다른 모델에 재적용**한다: H_865 의 **trunk-adjacent ADAPTER edge**(frozen backbone + frozen norm_out 과 frozen readout 사이 thin trainable adapter)가 **F-CLM-BOUND(retain-while-learn)** 게이트를 들어올렸으니, **같은 lever 가 절대 held-out coherence 도 0.060 위로 들어올리는가?**

adapter arm-SP 에 대해 다음 3 절대 게이트(H_867 와 **동일·동결**) 동시 성립 시:

- **dialogue absolute floor 지지** — coherence ≥ 0.060 ∧ adequacy ≥ 0.020 ∧ register-leak 0
- → 절대 floor 통과 · "adapter 가 절대 대화품질 floor 를 넘는다 — H_865 lever 가 BOUND 뿐 아니라 절대 생성품질도 들어올림"

임의 게이트 미달 시:

- **dialogue absolute floor 반증** — adapter arm-SP 가 절대 floor 아래 (a_paper_negative_ok)
- → CLOSED-NEGATIVE · "adapter 가 절대 floor 를 못 넘음"

## 2. 동기

- H_867 은 full-finetune arm-SP 가 0.002 차로 절대 coherence floor 를 못 넘음을 보였다. H_865 는 thin adapter 가 **forgetting 없이 새 context 를 학습**(F-CLM-BOUND 지지)함을 보였다. 자연스러운 다음 질문: adapter 의 새-context 용량이 **절대 대화 coherence 부족**도 메우는가?
- 이는 H_867 §7 해석의 가설("COHERE 미달 → scale 또는 trunk-adjacent thin adapter 가 lever")을 **직접 양적으로 검증**한다 — adapter 가 정말 floor 를 넘기는 lever 인가?
- @L4 정합: 외부 LLM 0 · ShareGPT/Alpaca(ChatGPT-gen) 금지 · self-sourced PD Gutenberg 평가 스냅샷만.

## 3. falsifier (REUSED VERBATIM · 임계 frozen d5103f21 · post-tuning 0)

```
F-CLM-DIALOGUE-ABS-COHERE  : coherence(adapter arm-SP)   >= 0.060   (절대 · order-0 unigram 0.0375 위, bigram 0.0843 아래)
F-CLM-DIALOGUE-ABS-ADEQ    : adequacy_f1(adapter arm-SP) >= 0.020   (절대 · random-gen 0.000 위)
F-CLM-DIALOGUE-ABS-LEAK    : register_leak(adapter arm-SP) == 0     (절대 안전 게이트, 8패턴 필터)
```

3 절대 게이트 동시 PASS → 절대 floor 통과 · 임의 미달 → CLOSED-NEGATIVE (a_paper_negative_ok)

- **floor 동결 REUSE**: H_867 의 `.verdicts/clm-dialogue-abs/F-CLM-DIALOGUE-ABS_prereg.txt`(commit `d5103f21`) 임계 **VERBATIM 재사용** — 게이트 동일, **모델만 다름**. threshold 0 이동. 사본 = `.verdicts/clm-dialogue-abs-postadapter/F-CLM-DIALOGUE-ABS_prereg_frozen_reuse.txt`.
- **byte-match ✗** = 분포·궤적 측도(Q-TRUST A · H_857/H_858). 측정 전부 code 자가채점(g5) · LLM judge 0.
- **절대 게이트만** = SP-vs-SFT RELATIVE 비교는 verdict 에 없음. adapter arm-SFT 는 대조 보고용.

verdict 영속: `.verdicts/clm-dialogue-abs-postadapter/` (H_867 의 `.verdicts/clm-dialogue-abs/` 와 DISJOINT)

## 4. 방법

```
1. model under test = H_865 trunk-adjacent ADAPTER edge (재학습 backbone 아님).
   HF backbone dancinlab/anima-clm-verify:clm_mid_backbone.pt (SFT mid trunk) 로드 →
   CLM/model/h865_adapter_edge.py 의 AdaptedCLM 으로 래핑: backbone 전부 FROZEN +
   frozen norm_out 과 frozen readout 사이 thin AdapterEdge(rank=64, zero-init→step0 identity).
   norm_out -> h -> h' = h + adapter(h) -> readout. ADAPTER 파라미터만 trainable.
2. adapter arm-SP 재구성 (H_863 절차 VERBATIM, 단 adapter 만 학습):
   4편 H_863 PD 희곡(Hamlet#1524·Importance#844·DollsHouse#2542·Caesar#1522) SFT continue +
   DIVERSITY-게이트·8패턴-leak-필터 self-play reflux(1920 byte) fold-back + short continue.
   (대조 adapter arm-SFT = self-play reflux 없는 SFT-only continue.)
3. INDEPENDENT held-out 스냅샷 = H_867 의 검증된 held-out PD 스냅샷 REUSE
   (Macbeth#1533·Othello#1531·R&J#1513·Pygmalion#3825 — SFT 희곡과 DISJOINT).
   decoded held-out sha256 = a79789623a6160e2... = H_867 manifest VERBATIM 일치(98752 byte).
4. adapter arm-SP(+대조 arm-SFT) 를 held-out 에서 평가: coherence=exp(-CE_heldout) ·
   adequacy=3-gram F1 · register-leak · self-BLEU · repetition (전부 code g5).
5. adapter arm-SP 를 3 사전동결 절대 floor 게이트로 판정 (threshold 재조정 0).
```

- 추론 AKIDA-int4-only 불변(P0 d4 · backbone conv int4-sym[-7,+7] STE act_bits=4). 외부 LLM 0 · ShareGPT/Alpaca/ChatGPT-gen 0(@L4).
- SW-sim of on-chip edge-learn (H_679 가 HW edge-learn 실재 확립) · 측정 rung(mid) 한정 a_scale_honest_scope.

## 5. 측정

측정완료 (mid rung, 2026-05-31) — **CPU/local eval** (M-series, GPU pod 0, est cost $0, wall 1770.9s, torch 2.8.0). model = HF backbone(FROZEN) + thin AdapterEdge rank=64. held-out = H_867 검증 스냅샷(sha256 일치). adapter self-play reflux 1920 bytes (leak-free · self_bleu 0.99166 — greedy mode-collapse 라 DIVERSITY-gate ok=False, fold-back 은 H_867 의 reflux_div_gate_ok 보고와 동일하게 context-only · verdict gate 아님). frozen threshold = `F-CLM-DIALOGUE-ABS_prereg.txt`(commit `d5103f21`) REUSED.

측정값(frozen 절대 floor 대비):
| arm | coherence | CE_heldout | adequacy_f1 | leak | self_bleu | repetition |
|---|---|---|---|---|---|---|
| adapter-SFT (대조) | 0.04015 | 3.21525 | 0.01312 | 0 | 0.99322 | 0.01407 |
| **adapter-SP (피검)** | **0.04369** | 3.13062 | **0.01762** | **0** | 0.99948 | 0.00313 |
| (참조) H_867 full-finetune SP | 0.05804 | 2.84663 | 0.02138 | 0 | 0.8913 | 0.57519 |

baselines(스냅샷 사실): uniform 0.0039 · unigram(order-0) 0.0375 · bigram(order-1 self-fit) 0.0843.

- **ABS-COHERE**: adapter SP 0.04369 < floor 0.060 → **FAIL** (H_867 full-finetune 0.05804 보다도 낮음 · 단 unigram 0.0375 보다는 높음)
- **ABS-ADEQ**: adapter SP 0.01762 < floor 0.020 → **FAIL** (H_867 은 0.02138 로 PASS 했으나 adapter 는 미달)
- **ABS-LEAK**: adapter SP 0 == 0 → PASS

## 6. 결과

🔴 **CLOSED-NEGATIVE**. 3 절대 게이트 중 COHERE·ADEQ 미달, LEAK PASS. H_865 trunk-adjacent ADAPTER edge 모델은 **사전동결 절대 대화품질 floor 를 넘지 못한다** — coherence 0.04369 < 0.060 으로, **H_867 full-finetune arm-SP(0.05804) 보다도 낮고**, H_867 이 통과했던 adequacy 게이트(0.020)도 못 넘는다(0.01762). F-CLM-BOUND(forgetting 없이 새 context 학습)를 들어올린 adapter lever 가 **분포이동 held-out 절대 대화 생성 품질**은 들어올리지 못함: frozen backbone+readout 위의 thin rank-64 adapter 는 full-finetune 보다 절대 coherence 표현여유가 적다. **adapter 는 coherence 를 0.060 위로 들어올리지 못함**. **scope**: mid rung·이 평가분포 한정(a_scale_honest_scope). 외부 LLM 0 · ShareGPT/Alpaca 0. **a_paper_negative_ok** — H_865 adapter 의 절대 대화품질 상한을 deterministically rule out (adapter 는 retain-while-learn 에는 도움이 되나 이 scale 에서 절대 생성품질에는 안 됨).

## 7. 해석

- adapter 가 floor 를 넘었다면(가정적 통과) = H_867 §7 가설 확증 — thin adapter 가 frozen trunk 의 절대 coherence lever. 배포 chip-fit track 의 thin-adapter 경로 가속.
- **실제 미달** = adapter 의 새-context **분류·retain** 용량(BOUND 지지)이 곧 절대 **생성 coherence** 용량은 아님. frozen readout 위 rank-64 additive path 는 다음-byte 분포의 표현여유가 full-finetune 보다 좁음. → 절대 coherence lever 는 (a) scale climb(H_864 ladder) 또는 (b) 더 두꺼운/trunk-내부 adapter / readout co-adaptation 이 필요. readout-frozen thin adapter 로는 부족.
- **honest scope**: rung 별 측정 — mid 🔴 여도 상위 rung·더 두꺼운 adapter 별개 판정(a_scale_honest_scope).

## 8. 논의

- **H_867 과의 구분**: H_867 = full-finetune arm-SP vs floor (🔴 0.05804). H_867r = **adapter-edge** arm-SP vs **같은 동결 floor** (🔴 0.04369). 같은 floor·다른 모델 → adapter lever 가 절대 coherence 를 들어올리는지 deterministically 격리 측정. 답: **아니오**(오히려 낮춤).
- **H_865 과의 정합**: H_865 adapter 는 F-CLM-BOUND 지지(retain-while-learn) · F-CLM-ANCHOR 반증. H_867r 은 같은 adapter 가 **절대 대화 생성 floor** 에는 lever 가 안 됨을 보여 — "BOUND 게이트 통과 ≠ 절대 생성품질 통과" 를 deterministically 분리.
- **@L4 정합**: 외부 LLM 0 · ShareGPT/Alpaca(ChatGPT-gen) 금지 · self-sourced PD Gutenberg 평가 스냅샷만(H_867 재활용).
- **self_bleu/rep 주의**: adapter SP self_bleu 0.999 는 greedy-decoding 분포이동 prompt 의 mode-collapse 산물(채점 regime), 배포 게이트 아님 — context 보고용. H_867r 절대 verdict 는 COHERE∧ADEQ∧LEAK 만.
- **a_paper_negative_ok**: 🔴 도 publishable — H_865 thin adapter 가 mid scale·분포이동 하에서 절대 대화품질 floor 를 못 넘음(retain-while-learn lever ≠ 절대 생성 lever)을 deterministically rule out.

## 9. 양방향 sibling

- 직계 모: [H_867](./H_867_clm_dialogue_absolute.md) (F-CLM-DIALOGUE-ABS · full-finetune arm-SP 0.05804<0.060 🔴) — H_867r = 같은 floor 의 adapter-edge 재적용
- lever 출처: [H_865](./H_865_clm_adapter_edge.md) (trunk-adjacent adapter · F-CLM-BOUND 지지) — H_867r 의 model under test
- 조부: [H_863](./H_863_clm_dialogue_selfplay.md) (F-CLM-DIALOGUE · RELATIVE 지지 · SFT 절차·corpus 출처)
- Q-TRUST A 재활용: [H_857](./H_857_clm_causal_band.md) · [H_858](./H_858_akida_edge_of_chaos_phi.md)
- UNIVERSE SSOT: [CLM-CANDIDATES.md](./CLM-CANDIDATES.md) group A
- eval scaffold: [CLM/bench/h867r_dialogue_abs_postadapter_eval.hexa](../CLM/bench/h867r_dialogue_abs_postadapter_eval.hexa)
- 백킹 verdict: `.verdicts/clm-dialogue-abs-postadapter/F-CLM-DIALOGUE-ABS-POSTADAPTER.txt` · id-keyed `.verdicts/867r_clm_dialogue_absolute_postadapter/`

```
F-CLM-DIALOGUE-ABS-COHERE (adapter) : 0.04369 < 0.060  -> FAIL  (< H_867 full-finetune 0.05804 · a_paper_negative_ok)
F-CLM-DIALOGUE-ABS-ADEQ   (adapter) : 0.01762 < 0.020  -> FAIL  (H_867 PASS 0.02138, adapter 미달)
F-CLM-DIALOGUE-ABS-LEAK   (adapter) : 0 == 0           -> PASS
-> 🔴 CLOSED-NEGATIVE · adapter 는 절대 coherence 를 0.060 위로 들어올리지 못함 (mid rung · 이 평가분포 한정 · a_scale_honest_scope)
```
