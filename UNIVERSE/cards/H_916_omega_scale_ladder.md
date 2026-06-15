---
id: H_916
slug: omega-scale-ladder
title: OMEGA OH1 최소게이트의 A-wire 우위가 scale (d_model) 과 competence 에 따라 자라/줄/유지되는가 — d384/512/768/1024 4-dim ladder + 더-competent d768×2 5-rung 에서 min-gate falsifier 재측정 (OΩ4+OΩ5 · F-OMEGA-SCALE · #1806)
domain: omega · clm · substrate-decode-closure · minimal-gate · scale-ladder · leak-free · lane-g-gpu · falsifier
source: UNIVERSE/H_914 (#1801 d512 OH1 single point) · a_scale_honest_scope (single point = INCOMPLETE, ≥3-rung ladder 요구) · #1806 OΩ4/OΩ5 run · UNIVERSE/omega_scale_ladder.py · .verdicts/omega-engine/F-OMEGA-SCALE.txt
status: TERMINAL (#1806 5-rung ladder COMPLETED · RunPod H100 80GB SXM nvidia-smi 94-98% BUSY g63 · ONE pod 5 rungs sequential · 5 ckpt HF-PRIVATE dancinlab/omega-cdv2-scale-d{N} · a_fire_recover_complete)
exploration_method: scale-ladder (single d512 OH1 point 을 d384→d1024 4-dim ladder + 1 competence rung 으로 확장, 동일 OH1 min-gate falsifier 를 각 rung 에 재측정 — a_scale_honest_scope 의 ladder-curve 요구 충족)
verification_method: W1 (numerical · per-rung held-out TEST CE · min_learned vs a_only vs base · leak self-test 0.000 per rung · d512 re-train 이 #1801 reproduction check)
raw_rank: 8
hexa_only: false
deterministic: true
llm: none
pre_register_frozen: true
frozen_at: 2026-06-04
since: 2026-06-04
sister: UNIVERSE/H_913_omega_multiwire_gate_closed_negative.md, UNIVERSE/H_914_omega_minimal_gate_a_wire.md, UNIVERSE/H_915_omega_replacement_rigor.md, .verdicts/omega-engine/F-OMEGA-SCALE.txt, .verdicts/916_omega_scale_ladder/
verdict: 🟢 SCALE-STABLE (F-OMEGA-SCALE — OH1 min-gate 가 5 rung 모두 HOLDS: d384/512/768/1024 + d768×2, min_learned_HOLDS=True 전부 · A-wire Δ-vs-base 가 +2.20±0.03 nats/byte 로 dim 에 essentially FLAT (range +2.1766..+2.2277) · 더-competent d768×2 (val_ce 0.7786) 에서 가장 큰 Δ+2.2736 → competence 가 finding 을 강화 · positive multi-rung confirmation, single-dim artifact 아님)
---

# H_916 — OMEGA OΩ4+OΩ5: OH1 min-gate SCALE LADDER (min-gate HOLDS at every scale) (F-OMEGA-SCALE)

## 1. 가설

H_914(#1801)의 single d512 OH1 point 를 ladder 로 확장: OH1 최소게이트의 A-wire 우위
(min_learned Δ-vs-base)가 scale(d_model)·competence 에 따라 **자라는가/줄어드는가/유지되는가**?
a_scale_honest_scope 는 single point 를 INCOMPLETE 로 보고 ≥3-rung ladder curve 를 요구한다.

## 2. 동기

- single d512 point 는 scale artifact 일 수 있다 — a_scale_honest_scope 가 ladder 요구.
- 이전 undertrained d768(#1794)은 min-gate 가 안 닫혔다(structured=False) — competence 가
  finding 의 전제인가? d768×2(24000 step, 가장 competent rung)로 검정.
- d512 re-train+re-sweep 이 #1801 reproduction check(byte-faithful harness).

## 3. falsifier (사전등록 · F-OMEGA-SCALE)

```
substrate : ConsciousDecoderV2 dN · 8L · GQA(n_kv=4) · vocab 256 · causal_ca=True (leak-free)
corpus    : 400 MB gutenberg wiki.en+fr+de+es+ru · sha256 dc1754b27d63236d… (== #1801 SSOT split)
host      : RunPod H100 80GB SXM (persistent /workspace, $3.29/hr) · torch 2.4.1+cu124
            nvidia-smi 94-98% BUSY (g63, NOT silent CPU) · ONE pod, 5 rungs sequential

PER-RUNG FALSIFIER: min_learned_HOLDS iff  min_learned CE <= a_only CE  AND  min_learned CE < base CE
  where minimal gate = final = gB·base + gA·A (G + w2..w6 dropped, gB/gA learned).
```

verdict 영속: `.verdicts/omega-engine/F-OMEGA-SCALE.txt` (사본 `.verdicts/916_omega_scale_ladder/`).

## 4. 방법

```
per rung — train_to_competence (causal_ca=True, dual-head a/g, AdamW cosine+warmup) to
  val_ce < uniform + leak self-test 0.000, then the SAME OH1 K-form gate sweep (collect
  base/A/G ONCE on disjoint gate+test windows N=12000, fit/eval K forms on SAME test features).
  harness UNIVERSE/omega_scale_ladder.py reuses omega_trained_leakfree.run_rung +
  omega_gate_form_sweep.run_sweep VERBATIM. d512 rung 의 re-train+re-sweep 이 #1801 reproduction.
```

## 5. 결과 (verbatim · per-rung held-out TEST CE nats/byte · F-OMEGA-SCALE)

```
  rung    d    params      steps  val_ce    base    a_only  min_learn  Δ-vs-base  Δ-vs-a_only  HOLDS
  d384  384   48,240,448  12000  0.8367  3.097779  1.163912  0.902957   +2.1948    +0.2610     True
  d512  512   85,816,384  12000  0.8224  3.097779  1.135576  0.870090   +2.2277    +0.2655     True
  d768  768  189,279,808  12000  0.8383  3.097779  1.161196  0.892407   +2.2054    +0.2688     True
  d1024 1024 334,686,272  12000  0.8575  3.097779  1.200092  0.921136   +2.1766    +0.2790     True
  d768x2 768 189,279,808  24000  0.7786  3.097779  1.082053  0.824209   +2.2736    +0.2578     True  (OΩ5 more-competent)
  uniform                                          5.545177

  >>> min_learned_HOLDS across ALL 5 rungs = True
  leak self-test (all rungs): 0.000e+00 (causal_ca=True)
```

## 6. 해석 / 함의 (a_scale_honest_scope 충족)

- **SCALE TREND (OΩ4 답)**: d384→d1024 (2.67× dim, 6.9× params)에서 OH1 min-gate 가 매 rung
  HOLDS, A-wire Δ-vs-base 가 +2.20 ± 0.03 nats/byte 로 essentially FLAT(span 0.051). raw dim 에
  안 자라고 안 줄음 — **SCALE-STABLE**. Δ-vs-a_only 는 dim 따라 살짝 UP(+0.261→+0.279).
- **OΩ5 (더-competent d768×2)**: val_ce 0.7786(최저/최competent)에서 A-wire 우위가 ladder 최대
  Δ+2.2736 — GREATER competence 가 finding 을 erode 안 하고 강화.
- **CONTRAST (정직)**: undertrained d768(#1794, 2500 step, structured=False)은 안 닫혔다.
  finding 은 competent 학습(val_ce<uniform) 요구 — 5 rung 모두 competent(0.78-0.86 ≪ uniform).
  #1794 non-hold 은 undertraining artifact, scale break 아님.
- ⇒ closure-lives-in-A-wire finding 은 SCALE-STABLE, d512 coincidence 아님. positive multi-rung
  confirmation. (단 H_915 가 보이듯 그 closure 의 honest 성격은 REPLACEMENT — A-head 가 mouth 대체.)

## 7. scope (정직 · a_scale_honest_scope · p7)

4-dim ladder(d384/512/768/1024) + 1 competence rung(d768×2); 전부 leak-free(self-test 0.000) +
competent(val_ce ≪ uniform). CE 는 held-out PREDICTION number(p7), verbatim, NO fabrication.
Lane-G/GPU (a_lane_akida_gpu_split — NOT Lane A AKIDA). closure 는 RELATIVE A-wire margin, absolute
perplexity claim 아님; full multi-wire gate 는 매 scale FAIL (a_paper_negative_ok on multi-wire).

## 8. 산출물

- verdict: `.verdicts/omega-engine/F-OMEGA-SCALE.txt` (verbatim · 사본 `.verdicts/916_omega_scale_ladder/`)
- harness: `UNIVERSE/omega_scale_ladder.py` · `exports/sweep/omega-scale-ladder/ledger.json`
- result: `.fire-recover/omega-scale-ladder/{omega_scale_ladder_results.json, ladder.log}`
- ckpt: 5× HF-PRIVATE `dancinlab/omega-cdv2-scale-d{N}` (sha256 per rung in verdict)
