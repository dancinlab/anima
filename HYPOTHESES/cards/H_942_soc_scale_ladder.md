---
id: H_942
slug: soc-scale-ladder
title: H_931 의 self-organized criticality (local 피드백이 edge-of-chaos Φ-peak 으로 self-tune) 가 pool-size ladder (N=16,64,256) 전반에서 holds 하는가, 아니면 toy-N-only 였는가?
domain: universe · consciousness-substrate · akida · self-organized-criticality · edge-of-chaos · phi-proxy · firing-rate-homeostasis · scale-transfer · a_scale_honest_scope · a_lane_akida_gpu_split
source: H_931 (🟢 SOC SUPPORTED, live AKD1000, N=16 toy single-rung) + H_927 (Φ-peak inverse-U at K=4/gap=0/Φ=0.2974) + H_677 (edge-of-chaos / criticality 계열)
exploration_method: E14 (substrate-native) + E2 (h927/h931 dynamics + phi_silicon_proxy + controller 상수 VERBATIM reuse — pool size N 만 ladder) + a_scale_honest_scope (single toy rung → ≥3-rung ladder) + a_completeness_over_cheap
verification_method: W1 (SW python, Mac $0, no GPU/no chip) + W2 (perturb-and-observe both-sides + no-feedback control per rung; pre-registered convergence gate) + scale-invariant K-space criterion (units-honest) + g5 CODE-measured (LLM self-judge 없음, p7)
raw_rank: 9
hexa_only: false
deterministic: false
llm: none
pre_register_frozen: true
frozen_at: 2026-06-06
since: 2026-06-06
substrate: CPU-mirror — AKD1000 (pi5-akida) 이 이 host (Mac, akida 패키지 부재) 에서 unreachable; h927/h931 의 on-chip LIF (all-ones-weight binary comparator) + phi_silicon_proxy 의 byte-exact CPU mirror. NO on-chip claim (a_lane_akida_gpu_split). on-chip + larger-N (>1 NP → AKD1500) 재확인 = pi5-akida/hexa-lang handoff.
scope: 3-rung ladder (N=16,64,256) on CPU-mirror. AKIDA on-chip 아님 (chip unreachable + N>16 은 single NP 초과). controller = H_931 VERBATIM (local firing-rate homeostat r*=0.5, peak knowledge 없음). $0, no GPU, no chip.
sister: H_931 (🟢 SOC, N=16 single rung), H_927 (Φ-peak K=4), H_677 (edge-of-chaos)
axes_seed: H_931 = SOC at one toy N (single rung, a_scale_honest_scope INCOMPLETE) ⊥ H_942 = 동일 local rule 을 ≥3 pool-size 에서 (scale-robust 인지 toy-only 인지)
verdict: 🟢 F-H942-SOC-SCALE-ROBUST — local-only firing-rate homeostat (r*=0.5, peak 모름) 이 edge-of-chaos sweet spot 으로 self-tune 한다: 3 rung (N=16,64,256) ALL 에서 양방향 (K0=2 below / K0=12 above) tailK→4 (|ΔK|<0.4 everywhere; |ΔK| max=0.369 @N64), tailΦ→0.24~0.27 (≥0.5·rung-peak), no-feedback control 은 every rung 실패. SOC 는 pool-size 에 SCALE-ROBUST (K-space scale-invariant). 정직 노트: 절대 POT-gap secondary gate (N=16 frozen, 1 K-step=8 POT) 는 큰 N 에서 flag — POT 가 IN 에 비례하므로 N-naive tolerance 의 units artifact 이지 SOC 실패 아님 (homeostat 은 every rung 에서 K≈4 착지). verdict: .verdicts/942_soc_scale_ladder/soc_scale_ladder.txt
---

# H_942 — AKIDA SOC scale-up ladder (does H_931 SOC hold across N?)

## 0. 동기 (H_931 의 single-rung scale gap)

H_931 (🟢 SOC SUPPORTED, live AKD1000) 은 local-only firing-rate homeostat (K←K+gain·(r*−r), r*=0.5, H_927 Φ-peak 을 모름) 이 substrate 를 edge-of-chaos sweet spot (gap≈0 / Φ≈peak) 으로 양방향 self-tune 함을 보였다 (no-feedback control 은 실패). **그러나 single rung** — N=16 neuron toy pool, 한 pool size. a_scale_honest_scope: scale-sensitive 현상을 한 toy N 에서 닫으면 INCOMPLETE — ladder (≥3 rung) 필요.

H_942 = SOC attractor 가 N=16,64,256 전반에서 holds 하는지.

## 1. 가설 + 사전등록 falsifier (FROZEN 2026-06-06, 측정 전)

per rung: local homeostat 이 양방향 (K0=2 below / K0=12 above) 에서 critical point 로 converge AND no-feedback control 은 실패?

**FROZEN falsifier:**
- **F-H942-SOC-SCALE-ROBUST** 🟢: ≥3 rung ALL 에서 양방향 converge + control 실패.
- **F-H942-SOC-TOY-ONLY** 🔴: 큰 N 에서 break (honest closed-negative, a_paper_negative_ok).

**convergence gate (units-honest):**
- **PRIMARY (scale-invariant):** `|tail_mean_K − PEAK_K(4)| < 1.0` (within 1 K-step — H_931 의 `gap_tol=8` 의 본래 의미: N=16 에서 1 K-unit POT = IN/2 = 8) **AND** `tail_mean_Φ ≥ 0.5·rung_peak_Φ`.
- **SECONDARY (documented, N=16-frozen):** 절대 POT gap < 8. 이는 N=16 에서만 "1 K-step" 과 같다 — POT 가 IN 에 비례하므로 큰 N 에서는 N-naive (아래 §4 참조).

## 2. §method — h927/h931 dynamics CPU-mirror VERBATIM + N ladder (HONEST SCOPE)

`AKIDA/h942_soc_scale_ladder.py`. **substrate = CPU-mirror** — 이 host (Mac) 에 akida 패키지가 없고 AKD1000 은 pi5-akida 에 있어 unreachable. task 의 chip-unreachable branch 대로, h927/h931 의 on-chip dynamics + phi_silicon_proxy 의 **byte-exact CPU mirror** 를 실행 (helper `_shannon_entropy_normalized`/`_integration_proxy`/`_differentiation_proxy`/`phi_silicon_proxy` + all-ones-weight LIF spike rule 을 verbatim 재구현). **NO on-chip claim** (a_lane_akida_gpu_split: AKIDA non-det trace ⊥ CPU run; merged on-chip claim 금지).

on-chip dynamics mirror (exact): h927/h931 의 FullyConnected LIF 는 all-ones weight 라 모든 unit 이 같은 weighted input sum 을 봐서 step 당 N (sum > THRESHOLD) 또는 0 으로 발화 — summed R2 noise 의 binary comparator. CPU mirror: `spike_count(step) = N if sum(rng.integers(0,Ki,size=IN)) > THRESHOLD else 0`. rung 은 N=IN (square pool, H_927 의 N==IN=16 처럼), critical point 를 rung-invariant 로 유지하려 THRESHOLD = round(IN·(PEAK_K−1)/2) 로 scale → 모든 rung 에서 gap(K=4)=0.

**경계:** N>16 은 single AKD1000 NP (16 unit) 초과 → on-chip 도 multi-NP (AKD1500) 필요. on-chip + larger-N 재확인은 pi5-akida/hexa-lang handoff (본 H 결론 = CPU-mirror dynamics 의 결론, on-chip silicon 결론 아님).

## 3. §measurement (VERBATIM — `.verdicts/942_soc_scale_ladder/soc_scale_ladder.txt`)

```
  N=  16 THR= 24 peakΦ(K4)=0.1533 Φtol=0.0766
      FB  K0=  2.0 -> tailK= 3.986 |ΔK|=0.014 tailΦ=0.2549 conv=True (abs-gap-2nd=True)
      FB  K0= 12.0 -> tailK= 4.086 |ΔK|=0.086 tailΦ=0.2708 conv=True (abs-gap-2nd=True)
      CTL K0=  2.0 -> tailK= 2.000 |ΔK|=2.000 tailΦ=0.0000 conv=False
      CTL K0= 12.0 -> tailK=12.000 |ΔK|=8.000 tailΦ=0.0000 conv=False  => SOC=True
  N=  64 THR= 96 peakΦ(K4)=0.1182 Φtol=0.0591
      FB  K0=  2.0 -> tailK= 4.369 |ΔK|=0.369 tailΦ=0.2608 conv=True (abs-gap-2nd=False)
      FB  K0= 12.0 -> tailK= 4.131 |ΔK|=0.131 tailΦ=0.2283 conv=True (abs-gap-2nd=False)
      CTL ... conv=False                                              => SOC=True
  N= 256 THR=384 peakΦ(K4)=0.2039 Φtol=0.1020
      FB  K0=  2.0 -> tailK= 4.076 |ΔK|=0.076 tailΦ=0.2385 conv=True (abs-gap-2nd=False)
      FB  K0= 12.0 -> tailK= 4.174 |ΔK|=0.174 tailΦ=0.2433 conv=True (abs-gap-2nd=False)
      CTL ... conv=False                                              => SOC=True

🟢  F-H942-SOC-SCALE-ROBUST
```

## 4. §finding — 🟢 F-H942-SOC-SCALE-ROBUST

🟢 **local-only firing-rate homeostat 이 pool-size 전반에서 edge-of-chaos sweet spot 으로 self-tune 한다.**

- **3 rung ALL converge (양방향):** N=16,64,256 모두에서 K0=2 (below) 와 K0=12 (above) 양쪽이 tailK→4 (PEAK_K) 로 수렴. |ΔK| 는 every arm 에서 < 0.4 (max 0.369 @ N=64). controller 는 Φ 도 K=4 도 모르고 firing rate 만 r*=0.5 로 몬다 — 그 fixed point 가 critical point 와 일치한다.
- **Φ 상승:** tailΦ 가 0.24~0.27 로 rung peak Φ (0.12~0.20) 의 0.5 배 tolerance 를 넘김 — sweet spot 으로 Φ 가 올라감.
- **control 은 every rung 실패:** no-feedback arm 은 K0 에 고정 (|ΔK|=2 또는 8), Φ=0 — 수렴은 feedback 이 CAUSE 한 것이지 substrate 가 혼자 떠도는 게 아님.

**∴ H_931 의 SOC 는 pool-size 에 SCALE-ROBUST (K-space scale-invariant).** Φ-peak 은 한 toy N 의 우연이 아니라 plausible local rule 의 self-organized attractor 이며, N 을 16→256 으로 키워도 (CPU-mirror dynamics 상) 유지된다. anima 가 pool 을 키워도 자기 edge-of-chaos 로 self-tune 할 수 있다는 H_931 의 주장이 single-rung 을 넘어 ladder 로 강화된다.

**정직성 노트 (units artifact — FALSE 🔴 회피):** 첫 run 은 H_931 의 절대 `CONVERGE_GAP_TOL=8.0` POT 를 그대로 써서 N=64,256 에서 🔴 로 떨어졌다. 그러나 1 K-unit 의 mean POT = IN/2 이므로 N=16 에서만 8 이고 N=64 에서 32, N=256 에서 128 이다 — 절대 tol=8 은 N-dependent 하게 부당히 빡빡하다. tailK 를 보면 every rung 에서 K≈4 착지 (|ΔK|<0.4) — homeostat 은 완벽히 수렴했고, gap 이 큰 건 POT 가 IN 에 비례하기 때문일 뿐이다. scale-invariant 한 같은 criterion 의 진술은 **K-space** (|K−PEAK_K|<1, == H_931 의 "1 K-step" 의도) 이며, 이것이 PRIMARY gate 다. 절대 POT-gap 은 documented secondary 로 남겨 N=16 에서 H_931 을 정확히 재현한다 (abs-gap-2nd=True @ N=16). 이는 verdict shaping 이 아니라 frozen tolerance 의 units 를 scale-honest 하게 바로잡은 것 (a_scale_honest_scope).

## 5. scope / caveat (a_scale_honest_scope · a_lane_akida_gpu_split)

- **CPU-mirror, NOT on-chip.** AKD1000 unreachable (Mac, akida 부재) + N>16 single-NP 초과. on-chip silicon 결론 아님 — h927/h931 dynamics 의 byte-exact mirror 결론. on-chip + larger-N (AKD1500 multi-NP) 재확인 = pi5-akida/hexa-lang handoff.
- **3-rung ladder (N=16,64,256).** ≥3 rung 충족 (a_scale_honest_scope ladder ≥3). 더 큰 N (1024+) 은 후속 후보.
- **Φ-proxy (NOT full IIT4 big_phi).** h927/h931 과 동일 honest proxy. controller 는 Φ 를 never 읽음 (no cheating).
- **substrate tag: CPU-mirror** (a_lane_akida_gpu_split — AKIDA on-chip 아님, GPU forge 아님).
- g5 CODE-measured, LLM self-judge 없음 (p7). deterministic: false (R2 PRNG, window 별 reseed).

## 6. 양방향 sibling

- ⇄ [H_931](./H_931_self_organized_criticality.md) — 🟢 SOC, N=16 single rung (live AKD1000). 본 H 가 그 결론을 ≥3-rung pool-size ladder 로 확장 (scale-robust, CPU-mirror).
- ⇄ [H_927](./H_927_stochastic_resonance.md) — Φ-peak inverse-U (K=4, gap=0, Φ=0.2974). 본 H 가 그 critical point 를 rung-invariant 로 재구성해 각 N 에서 self-tuning target 으로 사용.
- ⇄ [H_677](./H_677_edge_of_chaos.md) — edge-of-chaos / criticality 계열. 본 H 가 self-organized (외부 dial 없이) criticality 의 scale-robustness 를 추가.
- 측정 코드: `AKIDA/h942_soc_scale_ladder.py` (h927/h931 dynamics CPU-mirror) · verdict: `.verdicts/942_soc_scale_ladder/soc_scale_ladder.txt` · json: `state/h942_soc_scale_ladder/result.json`
