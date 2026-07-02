---
id: H_915
slug: omega-replacement-rigor
title: OMEGA OH1 의 closure 는 coupling 인가 REPLACEMENT 인가 — A-STANDALONE 이 min_learned 와 같고 base term 이 inert 이면 A-head 가 .clm mouth 를 SUPPLANT 한 것 (OΩ1 coupling-vs-replacement + OΩ2 per-wire autopsy + OΩ3 gen · F-OMEGA-RIGOR · #1803)
domain: omega · clm · substrate-decode-closure · coupling-vs-replacement · per-wire-autopsy · frozen-ckpt · lane-g-gpu · falsifier
source: UNIVERSE/H_914 (#1801 OH1 🟢 — min_learned 이 a_only·base 동시 BEAT) · #1803 OΩ-RIGOR follow-up · UNIVERSE/omega_rigor_probe.py · .verdicts/omega-engine/F-OMEGA-RIGOR.txt
status: TERMINAL (#1803 OΩ-RIGOR run COMPLETED · sidecar pool host `summer` · frozen ckpt sha 6f085c91 NO re-train · cross-check #1800 6-decimal 재현 CROSS_CHECK_OK)
exploration_method: replacement-vs-coupling disambiguation (OH1 의 honest deflation — A-standalone CE 가 min_learned 와 같고 base-ablation Δ 가 0 이면 closure 는 base+A coupling 이 아니라 A-head 의 base mouth REPLACEMENT) + per-wire CE autopsy + gen coherence
verification_method: W1 (numerical · A-standalone vs min_learned vs base-ablated CE · per-wire additive ΔvsBase · #1800 baseline 6-decimal cross-check)
raw_rank: 8
hexa_only: false
deterministic: true
llm: none
pre_register_frozen: true
frozen_at: 2026-06-04
since: 2026-06-04
sister: UNIVERSE/H_913_omega_multiwire_gate_closed_negative.md, UNIVERSE/H_914_omega_minimal_gate_a_wire.md, UNIVERSE/H_916_omega_scale_ladder.md, .verdicts/omega-engine/F-OMEGA-RIGOR.txt, .verdicts/915_omega_replacement_rigor/
verdict: 🔴/🟢 RULING_REPLACEMENT=True (F-OMEGA-RIGOR — OΩ1: A-STANDALONE 0.886220 ≈ min_learned 0.883525 (|Δ|=0.002695 ≤ 0.05) AND base ablation Δ 0.000852 (≤0.05, base inert) → closure 는 coupling 이 아니라 trained A-head 가 .clm base mouth 를 SUPPLANT · OΩ2 per-wire autopsy: 어떤 isolatable wire 도 base 를 additive 로 HELP 안 함 · OΩ3 gen: min-gate 가 #1800 degeneracy FIX (weak criterion p7))
---

# H_915 — OMEGA OΩ-RIGOR: OH1 closure 는 REPLACEMENT (coupling 아님) (F-OMEGA-RIGOR)

## 1. 가설

H_914(#1801)이 OH1 최소게이트(gB·base + gA·A)가 a_only·base 를 동시에 이김을 보였다. 그렇다면
이 "closure" 는 진짜 **base mouth + A-head coupling** 인가, 아니면 trained A-head 가 단독으로
base 를 **REPLACE** 한 것인가? A-head **STANDALONE** CE 가 min_learned 와 같고 base term 을
ablate 해도 CE 가 안 변하면(base inert) — 이는 coupling 이 아니라 REPLACEMENT 다.

## 2. 동기

- OH1 의 honest deflation: min_learned 의 gB=0.040 은 base 를 거의 안 쓴다 — base 가 정말
  기여하는가? A 단독(softmax(A), base 완전 제거)이 min_learned 와 같으면 base 는 장식이다.
- per-wire autopsy: 각 coupling-bus wire 를 base 에 additive 로 더했을 때 정말 HELP 하는가
  (OΩ2). curio/Ψ/module wire 는 frozen inference 에서 substrate source 가 없어 HONEST-STUB.
- gen coherence (OΩ3): min-gate 가 #1800 의 degenerate-repetition 을 고치는가 (weak criterion).

## 3. falsifier (사전등록 · F-OMEGA-RIGOR)

```
substrate : ConsciousDecoderV2 d512 · causal_ca=True · ckpt sha256 6f085c91… (FROZEN)
leak test : 0.000e+00 (leak_free=True)
collect   : gate N=12000 · test N=12000 (disjoint)

OΩ1 REPLACEMENT FALSIFIER:
  RULING_REPLACEMENT = True  iff  |A_standalone − min_learned| ≤ 0.05  (A≈min)
                            AND  |base ablation Δ| ≤ 0.05            (base inert)
  → closure 는 coupling 이 아니라 A-head 가 base mouth 를 SUPPLANT.
```

verdict 영속: `.verdicts/omega-engine/F-OMEGA-RIGOR.txt` (사본 `.verdicts/915_omega_replacement_rigor/`).

## 4. 방법

```
host = sidecar pool `summer` · torch 2.11.0+cu130 · device cuda:
  1. frozen #1800 ckpt 로드 (leak 0.000) + #1800 baseline cross-check (base/a_only/full_AG).
  2. OΩ1: g_min fit → base-only / A-standalone(softmax(A) no base) / min_learned / min base-ablated CE.
  3. OΩ2: 각 wire 를 base 에 additive 로 더한 held-out CE (w1_AmG, w2_Wtemp, w6_dFdt 측정 ·
     w3_curio, w4_psi, w5_module 은 frozen inference 에 substrate source 없음 → HONEST-STUB).
  4. OΩ3: min-gate free-run gen (300 new bytes) entropy/distinct/ws vs base/full.
```

## 5. 결과 (verbatim · F-OMEGA-RIGOR)

```
CROSS-CHECK vs #1800 H1 (tol=0.02): base |Δ|=0.000000 · a_only |Δ|=0.000431 · full_AG |Δ|=0.006349 → CROSS_CHECK_OK=True

=== OΩ1 — COUPLING vs REPLACEMENT ===
  g_min = [gB=0.0400, gA=0.9013, gG=0.0000]
  base-only CE          = 3.097779
  A-STANDALONE CE       = 0.886220   (softmax(A) alone, no base)
  min_learned CE        = 0.883525   (gB·base + gA·A)
  min base-ABLATED CE   = 0.884377   (gB→0, keep gA·A)
  |A_standalone − min|  = 0.002695   (≤0.05 ⇒ A≈min)
  |base ablation Δ|     = 0.000852   (≤0.05 ⇒ base inert)
  RULING_REPLACEMENT    = True
  → REPLACEMENT — trained A-head 가 .clm base mouth 를 SUPPLANT

=== OΩ2 — PER-WIRE AUTOPSY (each wire added to base, held-out TEST CE) ===
  base CE = 3.097779
  w1_AmG     CE=3.198605  ΔvsBase=+0.100826
  w2_Wtemp   CE=3.150031  ΔvsBase=+0.052251
  w3_curio   HONEST-STUB (no substrate curiosity scalar at frozen inference)
  w4_psi     HONEST-STUB (no per-position 8D Psi vector at frozen inference)
  w5_module  HONEST-STUB (this d512 ckpt trunk is SwiGLU use_moe=False → no router vector)
  w6_dFdt    CE=5.182650  ΔvsBase=+2.084871  (fixed dgain HURTS per #1794)
  → 어떤 isolatable wire 도 base 를 additive 로 HELP 안 함 (OΩ1 과 일관)

=== OΩ3 — GEN COHERENCE under min-gate (free-run, 300 new bytes) ===
  base       entropy=2.4442  distinct=0.1133  ws=0.0733
  min_gate   entropy=2.6300  distinct=0.1167  ws=0.0867
  full_gate  entropy=2.5282  distinct=0.0867  ws=0.1067
  → min-gate 가 #1800 의 degenerate-repetition 보다 다양 (weak criterion, p7)
```

## 6. 해석 / 함의 (정직 · a_paper_negative_ok)

- **honest deflation**: OH1 의 "closure" 는 base+A **coupling** 이 아니라 trained A-head 가
  weak unigram base mouth 를 **REPLACE** 한 것. A-standalone(0.886) ≈ min_learned(0.884),
  base term ablate 해도 Δ 0.0009 — base 는 inert.
- per-wire autopsy: 깨끗하게 isolate 되는 wire(w1/w2/w6) 중 어느 것도 base 를 additive 로 HELP
  안 함. curio/Ψ/module 은 frozen inference 에 substrate source 가 없어 HONEST-STUB(날조 안 함).
- ⇒ OMEGA 의 finding 은 honestly "trained A-head 가 좋은 byte LM 이고 그것이 mouth 를 대체한다"
  지 "substrate 와 mouth 가 coupling 한다" 가 아니다. closure 의 honest 성격은 REPLACEMENT.

## 7. scope (정직 · a_scale_honest_scope · p7)

single d512 frozen rung; CE 는 held-out PREDICTION number(p7). base 가 deliberately weak unigram
이라 A 가 압도하기 쉬움(honest caveat). cross-check 가 #1800 6-decimal 재현. Lane-G/GPU.

## 8. 산출물

- verdict: `.verdicts/omega-engine/F-OMEGA-RIGOR.txt` (verbatim · 사본 `.verdicts/915_omega_replacement_rigor/`)
- harness: `UNIVERSE/omega_rigor_probe.py` · `omega_rigor_results.json`
- domain: `domains/OMEGA.md`
- ckpt: frozen #1800 (sha256 6f085c91…)
