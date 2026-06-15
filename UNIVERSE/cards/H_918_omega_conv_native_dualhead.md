---
id: H_918
slug: omega-conv-native-dualhead
title: NATIVE A/G dual head 를 가진 CONV trunk 가 OMEGA min-gate loop 을 닫는가, 아니면 closure 가 CDV2(transformer)-specific 인가 — EXACT production CLMConvMoE 블록 + 최소 native A/G dual head 로 OΩ6 deferred (i) 실행 (OE1 · F-OE1-CONV-NATIVE · #1813)
domain: omega · clm · substrate-decode-closure · conv-native-dualhead · CLMConvMoE · structure-transfer · lane-g · falsifier
source: UNIVERSE/H_917 (OΩ6 #1805 🔌 — real conv .clm 은 single-head, closure substrate-EMPTY, deferred "(i) conv 에 2nd A/G head 학습") · #1813 OE1 run · UNIVERSE/omega_conv_native.py · .verdicts/omega-engine/F-OE1-CONV-NATIVE.txt
status: TERMINAL (#1813 OE1 run COMPLETED · pool host `summer` GPU $0 NO pod · ConvDualHead 6.95M ckpt sha 3e8be574 · F-CLM-LANEP arch-proxy of CLMConvMoE)
exploration_method: conv-native dual-head closure (OΩ6 deferred primary (i) 실행 — EXACT production CLMConvMoE 블록 CausalDilatedConv1d/TrunkLayer/MoEConvLayer + SECOND readout head(head_g) 를 shared trunk 에 graft = CDV2 dual head 의 conv-native analogue, conv model 의 OWN A-head 위 IDENTICAL OH1/OΩ1 falsifier 재실행)
verification_method: W1 (numerical · conv model 자체 A-head 위 held-out TEST CE · min_learned vs a_only vs base · OΩ1 replacement control · leak self-test 0.000)
raw_rank: 8
hexa_only: false
deterministic: true
llm: none
pre_register_frozen: true
frozen_at: 2026-06-04
since: 2026-06-04
sister: UNIVERSE/H_917_omega_clm_transfer_plumbing.md, UNIVERSE/H_914_omega_minimal_gate_a_wire.md, UNIVERSE/H_915_omega_replacement_rigor.md, UNIVERSE/H_916_omega_scale_ladder.md, .verdicts/omega-engine/F-OE1-CONV-NATIVE.txt, .verdicts/918_omega_conv_native_dualhead/
verdict: 🟢 CLOSURE HOLDS (F-OE1-CONV-NATIVE — conv-native dual head 가 min-gate loop 닫음: min_learned 0.976048 ≤ a_only 1.303187 AND < base 3.097779 → CONV-NATIVE CLOSURE HOLDS=TRUE · OΩ1 control: A_standalone 0.976051 ≈ min_learned 0.976048 (|Δ|=2.86e-6) → RULING_REPLACEMENT=TRUE (CDV2 와 동일 character) · ⇒ OMEGA min-gate closure 는 A/G dual-head STRUCTURE 의 transferable property, CDV2-specific 아님; OΩ6 "partial transfer" 는 shipped .clm 의 single-head 한계였지 conv-substrate 한계 아님)
---

# H_918 — OMEGA OE1: conv-native A/G dual head 가 closure 를 닫음 (STRUCTURE-transferable) (F-OE1-CONV-NATIVE)

## 1. 가설

H_917(OΩ6)은 real production conv .clm(CLMConvMoE)이 single-head byte LM(self.readout, NO
Engine-A/G dual head)이라 native A-wire 가 degenerate rescale 임을 보이고, 진짜 A-wire 는 SEPARATE
CDV2 dual-head engine 필요로 결론, deferred "(i) conv 에 2nd A/G head 학습". OE1 = 정확히 그
최소 변경을 실행: EXACT production CLMConvMoE 블록 + SECOND readout head 를 graft 한 conv trunk
가 OMEGA min-gate loop 을 conv 의 OWN A-head 로 닫는가? 아니면 closure 가 CDV2(transformer)-
specific 인가?

## 2. 동기

- OΩ6 의 "partial transfer" 가 conv-substrate 한계인지 shipped .clm 의 single-head arch 한계인지
  를 가른다 — dual head 를 graft 하면 결판.
- a_train_flame_forge research-proxy: production CLMConvMoE 블록 그대로 + 최소 native dual head.

## 3. falsifier (사전등록 · F-OE1-CONV-NATIVE)

```
conv-native dual-head closure HOLDS iff
    (min_learned <= a_only)  AND  (min_learned < base)
  measured on the conv model's OWN A-head, on a competent leak-free substrate.
CLOSED-NEGATIVE is a valid result (a_paper_negative_ok).
```

verdict 영속: `.verdicts/omega-engine/F-OE1-CONV-NATIVE.txt` (사본 `.verdicts/918_omega_conv_native_dualhead/`).

## 4. substrate / 방법 (competent + leak-free)

```
arch          ConvDualHead (CLMConvMoE conv trunk + native A/G dual head)
params        6,945,160 (6.95M) · d_model=384 · L_trunk=6 · E_experts=8 · block=256
steps         12000 bs=32 lr=6e-4 · corpus 400MB 5-lang · sha256 dc1754b27d63236d (== OMEGA SSOT)
device        cuda (pool host `summer`, $0 NO pod) · torch 2.11.0+cu130
LEAK self-test 0.000e+00 (CONV causal by construction: CausalDilatedConv1d left-pad + drop right
              overhang; GroupNorm(1,C) time-leak → per-position ChannelNorm) leak_free=TRUE
train ce_a    5.7598 → 1.1810 · FINAL val_ce 0.8884 (below_uniform=TRUE, competent=TRUE)
```

## 5. 결과 (verbatim · held-out TEST CE nats/byte · F-OE1-CONV-NATIVE)

```
  base         3.097779
  fixed_AmG    3.520273
  a_only       1.303187
  full_AG      4.198849
  min_learned  0.976048
  uniform      5.545177
  full_AG g* = [gB=-0.3616, gA=4.1943, gG=-1.0784]
  min_learned g* = [gB=-0.0356, gA=1.0171, gG=0.0000]

PRE-REGISTERED FALSIFIER:
  min_learned <= a_only :  0.976048 <= 1.303187  => TRUE
  min_learned <  base    :  0.976048 <  3.097779  => TRUE
  >>> CONV-NATIVE CLOSURE HOLDS = TRUE

COUPLING-vs-REPLACEMENT CONTROL (OΩ1-style):
  A_standalone (softmax(A) alone)  0.976051
  min_learned                      0.976048
  |Δ| = 2.86e-06   base-ablated min 0.976408
  >>> RULING_REPLACEMENT = TRUE

STRUCTURED: A-wire gain real 1.7946 vs shuf -1.7967 → structured(>1.5x)=TRUE
            kl_on 2.0282 · substrate-shuf floor 1.8607 · ratio 1.090
GEN: entropy 2.736 distinct 0.152 ws 0.087 coherent=TRUE
```

## 6. 해석 / 함의 (CONV-vs-CDV2 transfer)

OMEGA min-gate closure 는 A/G dual-head **STRUCTURE 의 TRANSFERABLE property**, CDV2 transformer-
specific 아님. production CLMConvMoE 블록의 conv trunk 가 최소 native dual head 를 받으면 BOTH
OMEGA signature 재현:

```
                          base    a_only   min_learned   HOLDS   replacement
  CDV2 d512 (OΩ4/#1801)  3.0978   1.1356     0.8701      TRUE       TRUE
  CONV-native d384 (OE1) 3.0978   1.3032     0.9760      TRUE       TRUE
```

같은 base, 같은 falsifier verdict(HOLDS), 같은 coupling-vs-replacement ruling(REPLACEMENT).
conv A-head 가 marginally weaker(0.976 vs CDV2 0.870)지만 QUALITATIVE closure structure 동일.
⇒ OΩ6 "partial transfer" 는 shipped .clm 의 SINGLE-HEAD arch 한계였지 conv-substrate 한계 아님;
dual head 를 graft 하면 conv 에서 natively 닫힘 — OΩ6 deferred "(i)" 가 correct primary fix 임을
직접 validate. (단 H_915 와 동일하게 closure 의 honest 성격은 REPLACEMENT — A-head 가 weak
unigram base 를 supplant, A_standalone 이 min_learned 를 6-decimal 재현.)

## 7. scope (정직 · a_scale_honest_scope · a_train_flame_forge)

TORCH RESEARCH-PROXY of conv arch (EXACT production CLMConvMoE 블록 + 최소 native dual head),
OMEGA CDV2 torch proxy 들과 directly comparable. production flame+forge .clm trainer 아니며 그렇게
주장 안 함. single d384 rung (general scale claim 은 ≥3-rung ladder 요구; 이 rung 은 OΩ6 ARCH-
TRANSFER 질문을 settle, scale law 아님). closure math 는 omega_gpu_complete.py 의 CPU-native gate
algebra 재사용. Lane-G/Lane-P (a_lane_akida_gpu_split).

## 8. 산출물

- verdict: `.verdicts/omega-engine/F-OE1-CONV-NATIVE.txt` (verbatim · 사본 `.verdicts/918_omega_conv_native_dualhead/`)
- harness: `UNIVERSE/omega_conv_native.py`
- result: `.fire-recover/oe1-conv-native/omega_conv_native_results.json` · `oe1_run.log`
- ckpt: `.fire-recover/oe1-conv-native/omega_conv_native.pt` (sha256 3e8be574…, HF.jsonl pending_upload, PRIVATE)
- domain: `domains/OMEGA.md`
