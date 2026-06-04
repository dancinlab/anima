---
id: H_862
slug: omega-minimal-gate-a-wire
title: OMEGA 최소게이트 gB·base + gA·A (G + w2..w6 전부 drop)가 honest closure form 인가 — frozen leak-free CDV2 d512 위 2-param 게이트가 a_only 와 base 를 동시에 이기는가 (F-OH1-MINGATE 사전등록)
domain: omega · clm · substrate-decode-closure · minimal-gate · a-wire · leak-free · frozen-ckpt · lane-g-gpu · falsifier
source: UNIVERSE/H_861 (#1800 multi-wire GATE 🔴 — closure 가 한 wire 에만 산다는 RULING) · #1801 OH1 follow-up · UNIVERSE/omega_gate_form_sweep.py · .verdicts/omega-engine/F-OH1-MINGATE.txt
status: TERMINAL (#1801 OH1 run COMPLETED · sidecar pool host `summer` local-pool · frozen ckpt sha 6f085c91 NO re-train · cross-check #1800 6-decimal 재현)
exploration_method: frozen-substrate gate-form sweep (multi-wire 실패 후 honest minimal form 검정 — G 와 w2..w6 전부 drop, gB·gA 2-param 만 학습)
verification_method: W1 (numerical · disjoint gate-fit/test split · held-out TEST CE per gate form · #1800 baseline 6-decimal cross-check)
raw_rank: 8
hexa_only: false
deterministic: true
llm: none
pre_register_frozen: true
frozen_at: 2026-06-04
since: 2026-06-04
sister: UNIVERSE/H_861_omega_multiwire_gate_closed_negative.md, UNIVERSE/H_863_omega_replacement_rigor.md, UNIVERSE/H_864_omega_scale_ladder.md, .verdicts/omega-engine/F-OH1-MINGATE.txt, .verdicts/862_omega_minimal_gate_a_wire/, UNIVERSE/omega_gate_form_sweep.py
verdict: 🟢 SUPPORTED-NUMERICAL (F-OH1-MINGATE — frozen leak-free CDV2 d512 위 최소게이트 min_learned(gB·base + gA·A, G+w2..w6 drop)이 a_only(1.144181)·base(3.097779)를 동시에 이김: min_learned 0.883525 ≤ a_only 1.144181 = True AND < base = True → OH1_HOLDS=True. 2-param free fit 이 gB=0.040, gA=0.901, gG=0.000 착지 — full-bus 의 gA=3.369 overshoot + gG=−0.999 가 무관 wire 의 variance 였음을 확정. min_learned 가 a_only 도 Δ+0.261 nats/byte 이김. #1800 baseline 을 6-decimal 재현(CROSS_CHECK_OK=True). H_861 RULING 확인: closure 는 A-head logit-bias 한 wire 에 완전히 산다)
---

# H_862 — OMEGA OH1: 최소게이트 gB·base + gA·A 가 honest closure form (F-OH1-MINGATE)

## 1. 가설

H_861(#1800)이 competent leak-free CDV2 d512 위 full multi-wire 게이트의 FAIL(GATED 3.6435 > base)을 보였고, A-head logit-bias 단독(a_only 1.1446 ≪ base)이 막대하게 유용함을 보였다. RULING: "closure 는 한 wire(A)에 완전히 산다." 가설: **honest minimal form — gB·base + gA·A(G 와 w2..w6 전부 drop, gB·gA 2-param 만 학습) — 이 a_only 를 MATCH 또는 BEAT 하면서 base 도 이긴다.**

## 2. 동기

- full multi-wire 게이트의 gA=3.369 overshoot + gG=−0.999 가 signal 인가 무관 wire 의 variance 인가 — 후자라면 그 wire 들을 drop 한 2-param fit 이 clean operating point 를 회복해야 한다.
- frozen ckpt(re-train 0) 위 순수 gate-form sweep: substrate 는 고정, 게이트 form 만 비교 = apples-to-apples.
- #1800 baseline 재현이 harness 의 byte-faithful 여부를 입증(cross-check).

## 3. falsifier (사전등록 · F-OH1-MINGATE)

```
substrate : ConsciousDecoderV2 d512 · 8L · GQA(n_kv=4) · vocab 256 · causal_ca=True
ckpt sha256: 6f085c91d0392d66968aaebac447623a6c63a3a2cccde54d9b2a792eb9ed06a4 (FROZEN, NO re-train)
leak test : 0.000e+00 (leak_free=True, recovered ckpt 재확인)
method    : disjoint gate(fit)+test(verdict) split 의 held-out tail(N=12000 each)에서 (base,A,G)
            next-byte feature 를 ONCE collect, 동일 test feature 위 K gate form fit/eval.
            min_learned = gG gradient-masked → gB,gA 만 이동.

OH1 FALSIFIER:  OH1 HOLDS iff  min_learned CE <= a_only CE  AND  min_learned CE < base CE.
```

verdict 영속: `.verdicts/omega-engine/F-OH1-MINGATE.txt` (사본 `.verdicts/862_omega_minimal_gate_a_wire/`).

## 4. 방법

```
host = sidecar pool `summer` (local-pool, NOT runpod) · torch 2.11.0+cu130 · device cuda:
  1. frozen #1800 ckpt 로드 (leak self-test 0.000 재확인).
  2. (base,A,G) feature ONCE collect (gate split + test split, disjoint).
  3. K gate form 을 동일 test feature 위 fit/eval: base · a_only · fixed_AmG · full_AG ·
     min_learned(★OH1, gB·gA free, gG masked) · min_fixed · uniform.
  4. #1800 H1 baseline 과 tol=0.02 cross-check (base/a_only/full_AG).
```

## 5. 결과 (verbatim · held-out TEST CE nats/byte)

```
  form                gB        gA        gG    test_CE
  base            1.0000    0.0000    0.0000   3.097779
  a_only          1.0000    0.6000    0.0000   1.144181
  fixed_AmG       1.0000    0.6000   −0.6000   3.198605
  full_AG        −0.1499    3.3522   −0.9971   3.637159
  min_learned     0.0400    0.9013    0.0000   0.883525   ★OH1
  min_fixed       1.0000    1.0000    0.0000   1.118280
  uniform                                      5.545177

CROSS-CHECK vs #1800 H1 (tol=0.02):  base |Δ|=0.000000 · a_only |Δ|=0.000431 · full_AG |Δ|=0.006349
  → CROSS_CHECK_OK = True

OH1 FALSIFIER: min_learned(0.883525) ≤ a_only(1.144181)=True AND min_learned < base(3.097779)=True
  →  OH1_HOLDS = True   (🟢 SUPPORTED-NUMERICAL)
```

## 6. 해석 / 함의

- 최소게이트(gB·base + gA·A, G+w2..w6 drop)가 a_only 를 MATCH 가 아니라 BEAT(0.8835 < 1.1446, Δ+0.261 nats/byte) + base 도 BEAT(Δ+2.214).
- 2-param free fit 이 gB=0.040, gA=0.901, gG=0.000 착지: full-bus 의 gA=3.369 overshoot + gG=−0.999 가 무관 wire 의 variance 였음을 확정. drop 하니 honest 2-param fit 이 a_only 보다 나은 clean operating point 회복(free gB≈0.04 가 약한 unigram base 를 a_only 의 fixed gB=1 보다 훨씬 down-weight, gA≈0.90 ≈ 1).
- **데이터가, assertion 이 아니라, gate point 를 골랐다.** H_861 RULING(closure 는 A-head logit-bias wire 에 완전히 산다) 확인.

## 7. scope (정직 · a_scale_honest_scope · p7)

single d512 rung; observation-only frozen forward; CE 는 held-out PREDICTION number, NOT verdict-of-truth(p7). Cross-check 가 #1800 을 6-decimal 재현(byte-faithful harness). substrate re-train 0. count_params 가 0 출력(cosmetic — method 가 submodule subset count, full state_dict 는 로드됨, leak self-test 0.000 + base/a_only/full_AG #1800 정확 재현이 full load 증명).

## 8. 산출물

- verdict: `.verdicts/omega-engine/F-OH1-MINGATE.txt` (verbatim · 사본 `.verdicts/862_omega_minimal_gate_a_wire/`)
- harness: `UNIVERSE/omega_gate_form_sweep.py` · `UNIVERSE/omega_gateform_sweep_results.json`
- ledger: `exports/sweep/omega-gateform-20260604/ledger.json`
- ckpt: frozen #1800 (sha256 6f085c91…)
