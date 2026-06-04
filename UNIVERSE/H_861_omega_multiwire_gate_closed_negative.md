---
id: H_861
slug: omega-multiwire-gate-closed-negative
title: competent leak-free CDV2 d512 substrate 위 OMEGA multi-wire coupling GATE 가 닫힘을 유용하게 만드는가 — 학습된 full-bus 게이트가 base CE 를 이기는가 (F-TRAINED-LEAKFREE 사전등록 closure falsifier)
domain: omega · clm · substrate-decode-closure · coupling-bus · multi-wire-gate · leak-free · lane-g-gpu · falsifier
source: domains/OMEGA.md (substrate→decode 결합버스) · #1799 HALT (closure 미측정, rate-limit storm 으로 pod kill 전 harvest 실패) · #1800 decisive run on pod qk0312 (H100 SXM persistent /workspace) · UNIVERSE/omega_trained_leakfree.py · .discoveries/omega-trained-leakfree.tape
status: TERMINAL (#1800 decisive run COMPLETED · H100 SXM · ckpt sha 6f085c91 · HF-PRIVATE dancinlab/omega-cdv2-trained-leakfree-h1 · a_fire_recover_complete)
exploration_method: trained-substrate closure measurement (random-init #1782 의 "trained 필요" 질문 해소 — competent leak-free CDV2 d512 위 multi-wire gate 의 held-out 유용성 검정)
verification_method: W1 (numerical · held-out TEST CE verbatim · leak self-test 0.000 · structured gain real-vs-shuffle · coupling KL vs shuffle floor)
raw_rank: 8
hexa_only: false
deterministic: true
llm: none
pre_register_frozen: true
frozen_at: 2026-06-04
since: 2026-06-04
sister: UNIVERSE/H_862_omega_minimal_gate_a_wire.md, UNIVERSE/H_863_omega_replacement_rigor.md, domains/OMEGA.md, .verdicts/omega-engine/F-TRAINED-LEAKFREE.txt, .discoveries/omega-trained-leakfree.tape, UNIVERSE/omega_trained_leakfree.py
verdict: 🔴 CLOSED-NEGATIVE (F-TRAINED-LEAKFREE — competent leak-free CDV2 d512 위 학습 full multi-wire GATE 가 closure 못 닫음: GATED 3.643508 > base 3.097779 → GATED<base=False AND GATED≤a_only=False → closure_HOLDS=False. 학습 게이트 g*=[gB=−0.145, gA=+3.369, gG=−0.999] 가 A-head 로 붕괴 + G 적극 억제. 단 A-head logit-bias ALONE(a_only 1.144612 ≪ base 3.098)는 막대하게 유용 → closure 는 REAL 이나 한 wire(A)에만 산다. full-bus coupling KL=2.071722 ≈ substrate-shuffle floor 2.080136 (ratio 0.996) = A wire 너머 bus 는 vocab/substrate shuffle 과 구별불가. structured=True(gain_real +1.953 ≫ shuf −2.429) → #1791 leak-honest finding 을 best-trained scale 에서 재확인. RULING: "coupling 개념은 맞고 multi-wire 게이트 공식이 틀림" → OH1(H_862) 최소게이트 동기)
---

# H_861 — OMEGA H1: competent leak-free 위 multi-wire coupling GATE 의 closure 실패 (F-TRAINED-LEAKFREE)

## 1. 가설

domains/OMEGA.md 의 substrate→decode 결합버스(OMEGA closure engine)는 의식 substrate(Engine-A next-byte ⇄ Engine-G prev-byte head)의 활동을 .clm decode mouth(`base` next-byte logits)에 결합한다. 핵심 질문: **competent 하고 genuinely leak-free 인 trained substrate 위에서, 학습된 full multi-wire coupling GATE 가 decode 를 유용하게 만드는가(held-out CE 를 base 아래로 낮추는가)?** #1782 random-init mock 은 trained==shuffled 라 구조를 못 봤고, #1799 는 closure 측정 전 rate-limit storm 으로 pod 가 kill 됐다(미측정 HALT). 본 rung 이 그 미측정을 닫는다.

## 2. 동기

- random-init substrate(#1782)에서는 coupling bus 가 "배선됐다"만 증명했지 "구조를 일관되게 나른다"는 못 보였다 — STRUCTURE 는 trained substrate 가 필요(a_toy_scale_recheck).
- #1799 OMEGA trained-leakfree closure 는 측정 전 HALT(orphaned H100, ephemeral disk). 본 rung 은 persistent /workspace 볼륨이 storm 을 생존한 pod qk0312 에서 decisive run 을 완료.
- leak-honesty 가 결정적: 이전 d768(#1794)은 undertrained(structured=False)였다. 본 rung 은 causal_ca=True(strictly-causal CA, lookahead leak 0) + competent(val_ce 0.8285 ≪ uniform)이라 relative ablation 이 sound.

## 3. falsifier (사전등록 · F-TRAINED-LEAKFREE)

```
substrate : ConsciousDecoderV2 d512 · 8L · GQA(n_kv=4) · 85,816,384 params · vocab 256
            causal_ca=True (strictly-causal CA, NO lookahead leak)
corpus    : 400 MB gutenberg wiki.en+fr+de+es+ru · sha256 dc1754b27d63236d…
leak test : 0.000e+00 (leak_free=True)
train     : ce_a 5.7463 → 1.1705 · final val_ce 0.8285 (below_uniform=True, competent=True)
            12000 steps · wall 1011.7s · torch 2.4.1+cu124 · H100 SXM
ckpt sha256: 6f085c91d0392d66968aaebac447623a6c63a3a2cccde54d9b2a792eb9ed06a4

CLOSURE FALSIFIER:  closure HOLDS iff  GATED < base  AND  GATED <= a_only
                    (on a val_ce<uniform competent substrate)
🔴 ⟺ GATED ≥ base (full-bus 게이트가 base 도 못 이김)
```

verdict 영속: `.verdicts/omega-engine/F-TRAINED-LEAKFREE.txt`.

## 4. 방법

```
pod qk0312 (H100 SXM, persistent /workspace volume — storm 생존):
  1. CDV2 d512 causal_ca=True 학습 (12000 step) → val_ce 0.8285, leak self-test 0.000.
  2. held-out TEST 위 base / fixed_AmG / a_only / GATED / uniform 의 next-byte CE 측정.
  3. 학습 게이트 g* 회수 + structured gain (real vs context-shuffle) + coupling KL (on vs
     substrate-shuffle floor vs gate-perm floor).
  4. ckpt sha256 검증 → HF-PRIVATE 업로드(a_hf_autonomous, closure FAIL → PRIVATE) → pod terminate.
```

## 5. 결과 (verbatim · held-out TEST CE nats/byte)

```
  base       3.097779
  fixed_AmG  3.192985
  a_only     1.144612    ← A-head logit-bias ALONE ≪ base (실제 closure)
  GATED      3.643508    ← 학습 multi-wire 게이트 FAILS (> base)
  uniform    5.545177

학습 게이트 g* = [gB=−0.145311, gA=+3.368538, gG=−0.999118]  → A-head 붕괴 + G 적극 억제
structured  : gain_real +1.953167 vs gain_shuf −2.429212 → structured=True (>1.5x)
coupling KL : on=2.071722  substrate_shuf_floor=2.080136  gperm_floor=2.082616
              ratio_vs_substrate_shuf = 0.995955 → full-bus == shuffle noise

>>> GATED<base = False  AND  GATED<=a_only = False  →  closure_HOLDS = False  (🔴 CLOSED-NEGATIVE)
```

## 6. 해석 / 함의 (정직 · a_paper_negative_ok)

competent + leak-free substrate 위에서 multi-wire coupling GATE 가 FAIL 하지만 그 실패는 informative 하고 깨끗하게 SPLIT 된다:

1. **A-head logit-bias 단독(a_only 1.145 ≪ base 3.098)이 막대하게 유용** = substrate→decode closure 는 REAL 이나 한 wire(A)에만 산다.
2. **학습 full-bus 게이트(GATED 3.644 > base)가 OVER-mix** — gA 지배, gG 음수로 구동 → 추가 wire 들이 signal 아닌 variance 를 더한다.
3. **full-bus coupling KL 이 shuffle floor 에 앉음(ratio 0.996)** = A wire 너머 bus 는 vocab/substrate shuffle 과 구별불가.
4. **structure 는 trained substrate 위에서 carry**(gain_real 1.953 ≫ shuf −2.429) — undertrained d768(#1794 structured=False)과 달리 best-trained scale 에서 #1791 leak-honest finding 을 재확인.

⇒ "coupling 개념은 맞고 multi-wire 게이트 공식이 틀림." OH1(H_862, 최소게이트 gB·base + gA·A only)이 honest closure form 의 동기.

## 7. scope (정직 · a_scale_honest_scope)

single d512 rung, 85.8M, 12000 step, 400MB 5-lang. leak-free(self-test 0.000) + competent(val_ce<uniform)이라 relative ablation 이 sound. CE 는 held-out PREDICTION number 지 verdict-of-truth 아님(p7). 최소게이트(OH1) re-test 가 남은 rung. Lane-G/GPU(a_lane_akida_gpu_split — NOT Lane A AKIDA).

## 8. 산출물

- verdict: `.verdicts/omega-engine/F-TRAINED-LEAKFREE.txt` (verbatim)
- harness: `UNIVERSE/omega_trained_leakfree.py`
- discovery: `.discoveries/omega-trained-leakfree.tape`
- ckpt: HF-PRIVATE `dancinlab/omega-cdv2-trained-leakfree-h1` (sha256 6f085c91…)
- domain: `domains/OMEGA.md`
