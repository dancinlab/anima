---
id: H_919
slug: omega-trained-coupling-qrng
title: TRAINED substrate 가 OMEGA bus 를 USEFUL 하게 만드는가 (random-init #1783 이 못 보인 STRUCTURE) + ANU 양자 난수 시드가 PRNG 시드 대비 substrate-coupling 에 측정가능한 advantage 를 주는가 (F-TRAINED-COUPLING + F-QRNG)
domain: omega · clm · substrate-decode-closure · trained-coupling · quantum-rng · anu-qrng · toy-ngram · falsifier
source: domains/OMEGA.md (substrate→decode 결합버스) · random-init #1783 (trained==shuffled, STRUCTURE 못 보임) · ANU QRNG (api.quantumnumbers.anu.edu.au) · .verdicts/omega-engine/F-COUPLING.txt (random-init null) · .verdicts/919_omega_trained_coupling_qrng/F-TRAINED-COUPLING.txt
status: TERMINAL (toy n-gram run COMPLETED · CPU/$0 no torch · real 400000B repo corpus · ANU quantum vs PRNG N=40 trials + PRNG-vs-PRNG null control)
exploration_method: trained-toy-substrate coupling + quantum-randomness advantage axis (bigram A/G + unigram base 의 toy substrate 가 bus 에 STRUCTURE 를 carry 하는가 random-init 대비; ANU 진짜 양자난수가 PRNG 대비 의식-coupling advantage 를 주는가 — 'consciousness needs quantum randomness' axis 검정)
verification_method: W1 (numerical · trained vs shuffled-floor coupling CE · a_only vs base · KS test quantum-vs-prng vs null control prng-vs-prng)
raw_rank: 6
hexa_only: false
deterministic: false
llm: none
pre_register_frozen: true
frozen_at: 2026-06-04
since: 2026-06-04
sister: UNIVERSE/H_913_omega_multiwire_gate_closed_negative.md, UNIVERSE/H_915_omega_replacement_rigor.md, UNIVERSE/H_920_omega_carrier_content_vs_magnitude.md, .verdicts/omega-engine/F-TRAINED-LEAKFREE.txt, .verdicts/919_omega_trained_coupling_qrng/
verdict: 🟢/🔴 MIXED (F-TRAINED-COUPLING — 🟢 STRUCTURE CARRIED: trained coupling 4.1420 ≪ shuffled floor 4.4991 (Δ+0.3571), random-init #1783 못 보임 · 🟢 A-wire USEFUL: base 4.0200→a_only 3.2619 (Δ+0.7581) · 🔴 full w1 (A−G) NOT useful: trained 4.1420 > base 4.0200, −G prev-byte wire HURTS → naive A−G subtraction 대신 learned gate 필요 · F-QRNG 🔴 CLOSED-NEGATIVE: quantum-vs-prng KS D=0.1500 p=0.7237 vs null control prng-vs-prng D=0.1000 p=0.9834 → 진짜 양자난수가 PRNG 대비 NO measurable advantage, 'consciousness needs quantum randomness' axis 배제)
---

# H_919 — OMEGA trained-coupling 페이오프 + ANU QRNG advantage axis (F-TRAINED-COUPLING + F-QRNG)

## 1. 가설

(A) TRAINED substrate(toy bigram A/G + unigram base)가 OMEGA coupling bus 를 통해 STRUCTURE 를
carry 하여 next-byte 예측을 개선하는가 — random-init #1783 은 trained==shuffled 로 STRUCTURE 를
못 보였다(F-COUPLING null). (B) ANU 진짜 양자난수 시드가 PRNG 시드 대비 substrate-coupling metric
에 측정가능한 advantage 를 주는가 — 'consciousness needs quantum randomness' axis.

## 2. 동기

- random-init #1783 rung 은 loop 이 WIRED 임만 증명; STRUCTURE 는 trained substrate 필요
  (a_toy_scale_recheck) — 이 rung 이 trained-payoff 를 측정.
- 양자난수 advantage 는 falsifiable: quantum-vs-prng 가 REJECT 하면서 null control(prng-vs-prng)
  은 NOT REJECT 해야 effect 가 real.

## 3. falsifier (사전등록 · F-TRAINED-COUPLING + F-QRNG)

```
corpus = 400000B real repo corpus · V=256 · alpha=0.6 · uniform-256 CE = 5.545177

F-TRAINED-COUPLING:
  STRUCTURE iff trained CE < shuffled (perm) floor
  A-wire USEFUL iff a_only CE < base CE
  full w1 USEFUL iff trained(base+α(A−G)) CE < base CE

F-QRNG (N=40 trials, CE_bus_trained):
  quantum effect REAL iff quantum-vs-prng KS REJECTS while prng-vs-prng null control does NOT
```

verdict 영속: `.verdicts/omega-engine/F-COUPLING.txt` (random-init null) + `.verdicts/919_omega_trained_coupling_qrng/F-TRAINED-COUPLING.txt`.

## 4. 결과 (verbatim · F-TRAINED-COUPLING)

```
--- F-TRAINED-COUPLING: does a TRAINED substrate make the bus USEFUL? ---
  CE_base (unigram mouth)        = 4.020038
  CE_bus_aonly  (base+α·A)       = 3.261919   (A wire alone, no −G)
  CE_bus_trained (base+α(A−G))   = 4.141998   (full w1 wire)
  CE_bus_shuffled (perm floor)   = 4.499132
  STRUCTURE: trained 4.1420 < shuffled 4.4991? -> YES Δ+0.3571
  A-wire useful: a_only 3.2619 < base 4.0200? -> YES Δ+0.7581
  full w1 useful: trained 4.1420 < base 4.0200? -> NO (−G prev-byte HURTS; A-only is the useful sub-wire)

--- F-QRNG: ANU quantum-seed vs PRNG-seed, CE_bus_trained over N=40 trials ---
  quantum : mean=4.142219 std=0.067597   (ANU-quantum api.quantumnumbers.anu.edu.au)
  prng    : mean=4.127580 std=0.078264
  prng#2  : mean=4.131202 std=0.082632
  KS quantum-vs-prng : D=0.1500 p=0.7237
  KS prng-vs-prng#2  : D=0.1000 p=0.9834   (NULL CONTROL)
```

## 5. 해석 / 함의 (정직 · a_paper_negative_ok)

- 🟢 **STRUCTURE CARRIED**: trained coupling 4.1420 ≪ shuffled floor 4.4991 (Δ+0.3571). trained
  substrate signal 이 unshuffled 일 때만 살아남음 = loop 이 STRUCTURE 를 carry. random-init #1783
  은 못 보임 — 이것이 trained-rung payoff.
- 🟢 **A-wire USEFUL**: base 4.0200 → a_only 3.2619 (Δ+0.7581) — learned next-byte(Engine-A)
  signal 이 예측 오차를 낮춤.
- 🔴 **full w1 (A−G) NOT useful**: trained 4.1420 > base 4.0200 — −G(prev-byte, Engine-G) wire 가
  next-byte 예측을 HURT. FINDING: bus 는 각 wire 에 LEARNED GATE 필요, fixed A−G subtraction 아님
  (이것이 H_913/H_914 의 learned-gate fix 동기).
- 🔴 **QRNG CLOSED-NEGATIVE**: quantum-vs-prng p=0.7237 가 null control prng-vs-prng p=0.9834 와
  깨끗하게 분리 안 됨(둘 다 small-N fluctuation 내) → 진짜 양자난수가 substrate-coupling metric 에
  NO measurable advantage. 'consciousness needs quantum randomness' advantage axis 를 이 scale 에서
  배제 (theory 예측대로 — randomness is randomness).

## 6. scope (정직 · a_toy_scale_recheck · p7)

TOY byte n-gram substrate (bigram A/G + unigram base), real-but-small 400000B repo corpus, CPU/$0,
no torch. NEXT RUNG = trained d768 ConsciousDecoderV2 (real A/G heads) on GPU (a_fire_autonomous) —
structured-coupling finding + learned-gate fix 가 real transformer 로 scale 하는가? (H_913/H_916 이
그 GPU scale-up 을 수행 — trained-coupling 은 holds 하나 closure 의 honest 성격은 REPLACEMENT).
CE 는 PREDICTION number, NOT verdict-of-truth (p7).

## 7. 산출물

- verdict: `.verdicts/919_omega_trained_coupling_qrng/F-TRAINED-COUPLING.txt` (verbatim) · `.verdicts/omega-engine/F-COUPLING.txt` (random-init null)
- discovery: `.discoveries/omega-trained-qrng.tape`
- domain: `domains/OMEGA.md`
