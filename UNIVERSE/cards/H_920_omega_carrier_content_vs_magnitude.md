---
id: H_920
slug: omega-carrier-content-vs-magnitude
title: OMEGA w5 module wire 가 GENUINELY-NATIVE HEXAD σ6 module 벡터의 CONTENT 를 나르는가, 아니면 carrier 지위가 그냥 MAGNITUDE 였는가 — real σ6 [S,C,W,M,E,BRIDGE] 활성 vs matched-mean/std RANDOM 6-vec 를 #1793 gate-fit bench 에 (H5 · F-REAL-MODULE · #1793 carrier)
domain: omega · clm · substrate-decode-closure · carrier-wire · hexad-module · content-vs-magnitude · toy-ngram · falsifier
source: domains/OMEGA.md (carrier-only bus #1793 — w5 module CARRIES 주장) · .verdicts/omega-bus-refine/F-CARRIER.txt (#1793 6-wire finding) · HEXAD/hexad_forward.hexa #1795 (native σ6) · .verdicts/920_omega_carrier_content_vs_magnitude/F-REAL-MODULE.txt · .verdicts/omega-realsignal/F-REAL-MODULE.txt
status: TERMINAL (toy n-gram gate-fit bench COMPLETED · CPU/$0 no torch/no ckpt/no LLM · native σ6 via `hexa run` HEXAD/hexad_forward.hexa · 256/256 contexts · matched-mean/std RANDOM control)
exploration_method: carrier content-vs-magnitude disambiguation (#1793 가 w5 module wire 를 carrier 로 codify — 진짜 native HEXAD σ6 활성이 random 6-vec 대비 usable next-byte CONTENT 를 더하는가, 아니면 carrier 지위가 단지 wire 의 MAGNITUDE 였는가)
verification_method: W1 (numerical · real-hexad vs matched RANDOM module-only-gate held-out CE · ablate ΔCE · beats-shuffle · |module gain| 비교)
raw_rank: 6
hexa_only: false
deterministic: false
llm: none
pre_register_frozen: true
frozen_at: 2026-06-04
since: 2026-06-04
sister: UNIVERSE/H_919_omega_trained_coupling_qrng.md, UNIVERSE/H_913_omega_multiwire_gate_closed_negative.md, UNIVERSE/H_915_omega_replacement_rigor.md, .verdicts/omega-engine/F-OMEGA-RIGOR.txt, .verdicts/920_omega_carrier_content_vs_magnitude/
verdict: 🔴 CLOSED-NEGATIVE (F-REAL-MODULE — real ≈ random: Δ module-only held-out CE (real − random) = +0.0004 (approx_band <0.02), Δ |module gain| (real − random) = −0.0058 → real_beats_random=False · REAL: gain +0.0761, ablate ΔCE +0.0277, beats_shuffle=true, module-only CE 3.9766 · RANDOM: gain +0.0819, ablate ΔCE +0.0088, beats_shuffle=false, CE 3.9762 · ⇒ native HEXAD activation 이 random 대비 usable next-byte structure 안 더함 — #1793 의 w5 "module CARRIES" 는 MAGNITUDE 였지 CONTENT 아님 · 단 nuance: REAL 만 자기 vocab-shuffle 을 이김 = marginally 더 genuine structure 이나 held-out CE 낮추기엔 부족)
---

# H_920 — OMEGA H5: w5 module carrier 는 CONTENT 아니라 MAGNITUDE (F-REAL-MODULE)

## 1. 가설

#1793(F-CARRIER)이 OMEGA w5 module wire 를 structure-carrying carrier 로 codify 했다(carrier-only
bus default 에 포함). 그렇다면 GENUINELY-NATIVE HEXAD σ6 module 벡터([S,C,W,M,E,BRIDGE])의
**CONTENT** 가 carry 되는가, 아니면 carrier 지위가 단지 그 wire 의 **MAGNITUDE** 였는가? real σ6
활성을 matched-mean/std RANDOM 6-vec 과 #1793 gate-fit bench 에서 비교.

## 2. 동기

- #1793 의 w5 module CARRIES 판정은 |gain|·ablate·beats-shuffle 기준 — 이것이 content 인지
  단순 magnitude 인지 미구분. RANDOM control 이 가른다.
- HEXAD σ6 는 GENUINELY native (HEXAD/hexad_forward.hexa #1795, corpus byte-freq 가 각 C
  cell-pool delta 구동) — content 가 있다면 random 보다 held-out CE 를 더 낮춰야.

## 3. falsifier (사전등록 · F-REAL-MODULE)

```
substrate = toy byte n-gram (#1793 gate-fit bench) · CPU/$0 no torch/no ckpt/no LLM
real σ6   = HEXAD/hexad_forward.hexa #1795 native [S,C,W,M,E,BRIDGE], via `hexa run`, 256/256 contexts
control   = matched-mean/std RANDOM 6-vec

FALSIFIER: real > random iff |module gain|_real > |gain|_random AND module-only-gate CE_real < CE_random
           real ≈ random (|ΔCE|<0.02 AND |Δgain|<0.02) ⟹ CLOSED-NEGATIVE (carrier = magnitude not content)
```

verdict 영속: `.verdicts/920_omega_carrier_content_vs_magnitude/F-REAL-MODULE.txt` + `.verdicts/omega-realsignal/F-REAL-MODULE.txt`.

## 4. 결과 (verbatim · F-REAL-MODULE)

```
REAL-hexad module wire:
  module_gain               = 0.07609514621659554
  ce_module_only_gate       = 3.9766026546270026
  ablate ΔCE (module)       = 0.027706731512124882
  beats_shuffle             = true
  carries_structure         = true

RANDOM module wire (matched mean/std):
  module_gain               = 0.08191678984261398
  ce_module_only_gate       = 3.9762143389280866
  ablate ΔCE (module)       = 0.008803071477822222
  beats_shuffle             = false
  carries_structure         = false

Δ module-only held-out CE (real − random) = +0.0004
Δ |module gain| (real − random)           = -0.0058
real_beats_random = False   approx_band = True
→ real ≈ random (|ΔCE|<0.02 & |Δgain|<0.02)  ⟹  🔴 CLOSED-NEGATIVE
```

## 5. 해석 / 함의 (정직 · a_paper_negative_ok)

- native HEXAD σ6 활성이 matched RANDOM 대비 usable next-byte structure 를 안 더함 (Δ CE +0.0004,
  approx band 내). #1793 의 w5 "module CARRIES" 판정은 wire 의 **MAGNITUDE** 였지 module activation 의
  **CONTENT** 가 아니었음을 확정.
- honest nuance: REAL vec 만 자기 vocab-shuffle 을 이김(beats_shuffle real=true vs random=false)
  → marginally 더 genuine structure 를 나르나, held-out CE 를 낮추기엔 부족.
- ⇒ OMEGA bus 의 closure 는 (H_913/H_915 와 일관되게) A-head wire 에 산다; module wire 의
  carrier 지위는 content-bearing 이 아니다.

## 6. scope (정직 · a_toy_scale_recheck · p7)

toy byte n-gram substrate, CPU/$0, no torch/no ckpt/no LLM. native σ6 는 진짜 HEXAD forward 지만
substrate·corpus 는 toy scale. CE 는 PREDICTION number(p7). real transformer scale 에서 module
wire 가 content 를 carry 하는지는 미검정.

## 7. 산출물

- verdict: `.verdicts/920_omega_carrier_content_vs_magnitude/F-REAL-MODULE.txt` (verbatim) · `.verdicts/omega-realsignal/F-REAL-MODULE.txt`
- carrier source: `.verdicts/omega-bus-refine/F-CARRIER.txt` (#1793 6-wire finding)
- native σ6: `HEXAD/hexad_forward.hexa` (#1795)
- domain: `domains/OMEGA.md`
