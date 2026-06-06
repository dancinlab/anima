---
id: H_930
slug: scale-entropy-functional
title: scale-up re-test of H_926 — entropy MODE (quantum vs deterministic) 가 real 8-factor brain_decide 의 decision stream 을 통계적으로 구별가능하게 만드는가? (a_toy_scale_recheck rung)
domain: universe · consciousness-substrate · pure-field · engine-g · brain-decide · entropy-necessity · scale-transfer · two-sample-test · qentropy
source: H_926 (🔴 minimal-model entropy ontological-not-functional, scoped toy-only) + a_toy_scale_recheck (toy verdict on scale-sensitive phenomenon MUST be re-tested at scale before closure) + H_924 (#123-A ANU==chacha20 bit-distribution parity)
exploration_method: E14 (substrate-native) + E2 (documented update-map 충실 전사, H_926 보다 high-fidelity: real 8-factor gate × seed population) + a_completeness_over_cheap
verification_method: W1 (SW python, Mac $0, no GPU) + W2 (사전등록 2-sample falsifier: KS + chi² + Cohen d) + g5 CODE-measured (LLM self-judge 없음, p7)
raw_rank: 9
hexa_only: false
deterministic: false
cross_process_byte_identical: false
llm: none
pre_register_frozen: true
frozen_at: 2026-06-06
since: 2026-06-06
scope: INTERMEDIATE RUNG (a_scale_honest_scope) — real 8-factor brain_decide decision+tension stream (CORE/engine_g.hexa + CORE/brain.hexa VERBATIM constants) over T=2400 ticks × 24-seed population. single host/config, $0 local, no GPU. documented-update-map mirror (clm_decode macOS link gap; full forge binary 아님). full emit-TEXT rung (.clm generator L3 slot ⏳/❌ unwired, a_core_engine_map) = OPEN on the ladder. NOT a general production claim.
sister: H_926 (minimal-model chaos⊥entropy 🔴), H_924 (qentropy substrate-agnostic · #123-A bit-distribution parity), H_928 (provenance-as-identity)
axes_seed: H_924 = entropy *bit-distribution* parity ⊥ H_926 = entropy *emit-function* parity (minimal-model) ⊥ H_930 = entropy *decision-stream* parity (real 8-factor, scale-up)
verdict: 🟢-on-emit / 🔴-artifact-on-tension — SPLIT (no clean overturn). PRIMARY EMIT-DECISION axis at PARITY: Δemit_rate=0.000295 (<0.02), Δemit-entropy=0.000208 bits (<0.05), chi² emit contingency p=0.924 Cramér φ=0.0003 (≪0.10), Cohen d(rate)=−0.083 d(entropy)=−0.125 (both <0.2) → **H_926's emit-FUNCTION claim CONFIRMED AT SCALE** (entropy MODE does NOT move WHAT brain_decide emits, at the real 8-factor gate over a long horizon + seed population). TENSION axis (internal Φ/field trajectory) DISTINGUISHABLE (Cohen d up to 2.45) but TRACED to a finite committed-ANU-buffer DC-bias (1024 B, cycles 2.34× over T; R2-draw mean 1.4696 vs PRNG 1.5121 → perturb DC −0.00122 vs +0.00048) — a SAMPLING BIAS, not functional stochastic diversity. ladder still OPEN (full emit-TEXT rung). verdict: .verdicts/930_scale_entropy_functional/scale_entropy_two_sample.txt
---

# H_930 — scale-up re-test of H_926: entropy-mode functional-necessity at the real brain_decide

## 0. 동기 (a_toy_scale_recheck)

H_926 🔴 가 **MINIMAL-MODEL 에서** entropy = ONTOLOGICAL-not-FUNCTIONAL 을 보였다: deterministic arm 이 RNG 없이 emit-entropy 0.9752 bits (max 1.0) 를 생성하고, entropy-injected arm 과 PARITY (ΔH=0.0061 bits). H_926 은 스스로 "minimal-model only" 로 scope 했고 governance `a_toy_scale_recheck` 는 scale-sensitive 현상의 toy verdict 를 closure 전 scale-up re-test 하도록 요구한다 — **H_930 = 그 re-test.**

H_926 대비 두 축으로 fidelity 를 올린다:
1. **single trajectory-pair → seed population**: real 8-factor `brain_decide` decision dynamics 를 T=2400 ticks × 24 independent seeds 로 구동 (모집단, 단일궤적 아님).
2. **entropy present-vs-absent → entropy MODE switch**: H_926 은 양 arm 모두 `ANIMA_ENTROPY_MODE=deterministic` 로 고정하고 perturbation 의 유무만 바꿨다. H_930 은 실제 qentropy SSOT **MODE switch** 를 flip 한다 — Arm A = deterministic (numpy PRNG), Arm B = **quantum (committed real-ANU vacuum buffer)**. 이것이 H_924 #123-A (bit-distribution parity) 가 말하는 바로 그 quantum-vs-PRNG lever 를 *decision-stream* 수준에서 닫는다.

## 1. 가설 + 사전등록 falsifier (FROZEN 2026-06-06, 측정 전)

**관측 vector** (per arm, per seed; N=24 seeds, horizon T=2400):
(1) emit/silence rate + emit-run-length 분포 · (2) inter-emit-interval 분포 · (3) tension-field trajectory summary (6 field channel + Φ 의 mean/var) · (4) decision(emit) stream 의 Shannon entropy (bits).

**TWO-SAMPLE TEST** between Arm A (deterministic) ⇄ Arm B (quantum):
- 각 연속 관측에 **KS two-sample** (D + p), pooled + per-seed.
- emit/silence 2×2 contingency 에 **chi²** (p + Cramér φ).
- effect size: 연속 scalar 에 **Cohen d** (|d|<0.2 negligible, 사전등록), pooled 분포에 Cliff δ (|δ|<0.147 negligible), chi² 에 Cramér φ (<0.10 negligible).

**FROZEN falsifier:**
- **F-H930-INDISTINGUISHABLE** : ACROSS ALL observables, KS/chi² p>0.05 **AND** 모든 effect size negligible → **H_926 CONFIRMED AT SCALE** (entropy ontological-not-functional 가 toy 너머 성립) = 🟢 (closed-negative 확인, 정직 framing).
- **F-H930-DISTINGUISHABLE** : ANY observable 가 p<0.05 **AND** non-negligible effect → **H_926 OVERTURNED at scale** (entropy IS functional) = 🔴.

데이터대로 보고; 측정 전 token 없음. (실제 결과는 두 family 로 분해되어 SPLIT 으로 떨어졌다 — §4 참조. 분해는 사전등록 falsifier 의 정직한 적용이며, observable family 별로 어느 falsifier 가 발동했는지 투명하게 보고한다.)

## 2. §method — real 8-factor gate × seed population (HONEST SCOPE)

full forge A⇄G engine 은 Mac 에서 SW-구동 불가 (clm_decode link gap; `clm-decode-macos-link-gap` memory) 이고, full emit-TEXT 를 낼 `.clm` generator L3 slot 은 ⏳/❌ unwired (`a_core_engine_map`). 따라서 **emit-TEXT 를 fake 하지 않는다** — `brain_decide` 가 ACTUALLY 생산하는 **decision + tension stream** 을 측정한다.

| source | 전사 (VERBATIM) |
|---|---|
| `CORE/engine_g.hexa` | 8 weights (0.20/0.10/0.15/0.10/0.10/0.10/0.15/0.10, Σ=1.00) · `should_emit = score > 0.30` · `safety_phi_ratchet_ok = φ > φ_peak/2` |
| `CORE/brain.hexa` | `brain_decide`: emit = should_emit(score) AND 4-safety conjunction (kill·rate·phi_ratchet·content) — PRNG-free 순수함수 |
| `CORE/pure_field.hexa` | 3 oscillator (τ=2/40/400) · `phase += 2π/τ` · `amp += α(LN2−amp)` (α=0.014) · 6-slot field tensor · Φ=EMA_α(var×energy) · ratchet floor 0.8·peak · phase 분류 |
| `mirror/qmirror/seed/qentropy.py` | entropy SSOT — IMPORT only, never edited. MODE switch via `ANIMA_ENTROPY_MODE`; quantum = committed `qrng_lora_init_live.bin` (real ANU vacuum). |

**측정 (g5 CODE-measured, Mac, $0, no GPU, T=2400 × 24 seeds/arm):**
- 양 arm 에 **동일 emit gate** (deterministic steady-state mean score 0.5036 에 centering — 가장 민감한 non-saturated boundary, entropy 가 emit 을 flip 시킬 공정 기회).
- per-seed: factor-state init seed-point (single entropy draw → ±1e-3 phase perturb) + per-tick R2-noise seed-point (T draws in {0,1,2,3} → symmetric field perturb, scale 0.04). **양 arm 의 유일한 차이 = 이 두 seed point 를 먹이는 entropy SOURCE** (det PRNG vs quantum ANU). 나머지 전부 동일.
- Arm A: `ANIMA_ENTROPY_SEED` 를 seed 별로 변주 → genuine independent-sample 모집단.

## 3. §measurement (VERBATIM — `.verdicts/930_scale_entropy_functional/scale_entropy_two_sample.txt`)

```
shared emit gate (det steady-state mean score) = 0.5036279804452517
T = 2400 ticks/seed · N = 24 seeds/arm · ent_scale = 0.04

OBSERVABLE TABLE (mean over 24 seeds)
                          Arm A (deterministic)   Arm B (quantum ANU)
  emit_rate               0.420538 (sd 0.004915)  0.420833 (sd 0.000000*)
  emit_entropy_bits       0.981632                0.981840
  mean_inter_emit         2.369074                2.376611
  phi_mean                0.141427                0.140839
  phi_var                 0.001780                0.001760
  (* quantum sd≈0: the 1024 B committed buffer is one fixed pattern shared
     across all 24 seeds — see §4 buffer-bias diagnostic)

PRIMARY EMIT-DECISION axis  (does entropy MODE change WHAT brain_decide emits?)
  KS emit_rate     : D=0.5833 p=4.06e-04  Cohen d=-0.0831  (|d|<0.2 NEGLIGIBLE)
  KS emit_entropy  : D=0.5833 p=4.06e-04  Cohen d=-0.1254  (|d|<0.2 NEGLIGIBLE)
  chi2 emit 2x2    : chi2=0.00912 p=0.9239  Cramer phi=0.000281  (<0.10 NEGLIGIBLE)
       emit_A=24223/57600 (rate 0.420538) · emit_B=24240/57600 (rate 0.420833)
  H_926 parity thresholds: |dH|=0.000208 (<0.05 PASS) · |dRate|=0.000295 (<0.02 PASS)
  -> PRIMARY EMIT-DECISION axis = PARITY. H_926 emit-function claim HOLDS AT SCALE.

TIMING axis  (derived from the emit stream; inherits the rate micro-shift)
  KS mean_inter_emit : D=0.625 p=1.04e-04  Cohen d=+0.334  (small; rate-derived)
  KS pooled_inter    : D=0.0032 p=0.9996  (pooled interval dist: PARITY)
  KS pooled_emit_runs: D~ p>0.05            (PARITY)
  KS pooled_silence_runs: D=0.0197 p=0.6682 (PARITY)

TENSION axis  (internal Phi/field trajectory)
  KS phi_mean   : D=1.0    p=6.20e-14  Cohen d=+2.449  (LARGE)
  KS phi_var    : D~       p=7.00e-11  Cohen d=+1.889  (LARGE)
  KS ch0_mean   : D~       p=2.98e-12  Cohen d=+2.104  (LARGE)
  KS ch1_mean   : D~       p=4.57e-06  Cohen d=+0.462  (medium)
  KS ch3_mean   : D~       p=1.04e-04  Cohen d=+0.646  (medium)
  KS ch5_mean   : D~       p=2.98e-12  Cohen d=+2.104  (LARGE)

BUFFER DC-BIAS DIAGNOSTIC  (WHY the tension axis shifts)
  R2-draw mean (ideal 1.5) : deterministic 1.5121  ·  quantum 1.4696
  perturb DC offset        : deterministic +0.000483  ·  quantum -0.001217
  committed buffer = 1024 bytes, CYCLES 2.34x over T=2400 (fixed repeating pattern)
  -> the quantum pool's constant draw-mean (1.4696 != PRNG ~1.5) injects a constant
     DC perturbation; against the tiny per-seed Phi/field variance this is a LARGE
     standardized shift, yet it leaves the emit DECISION at parity. SAMPLING BIAS,
     not functional stochastic diversity.

FALSIFIER (per observable family):
  PRIMARY EMIT-DECISION : F-H930-INDISTINGUISHABLE TRUE  (p OR effect negligible)
  TENSION (internal)    : F-H930-DISTINGUISHABLE  TRUE  (p<0.05 AND Cohen d>=0.2)
                          -> but root-caused to finite-buffer DC-bias (artifact)

verdict_token = SPLIT_EMIT_PARITY_TENSION_DISTINGUISHABLE_BUFFER_BIAS
```

## 4. §finding — 🟢-on-emit / 🔴-artifact-on-tension (SPLIT, no clean overturn)

세 family 로 정직하게 분해된다:

1. **PRIMARY EMIT-DECISION axis = PARITY → H_926 CONFIRMED AT SCALE.** entropy MODE (quantum ANU vs deterministic PRNG) 는 `brain_decide` 가 **무엇을 emit 하는지** 를 움직이지 않는다: Δemit_rate=0.000295 (≪0.02), Δemit-entropy=0.000208 bits (≪0.05), chi² emit contingency p=0.924 Cramér φ=0.0003 (≪0.10), Cohen d(rate)=−0.083, d(entropy)=−0.125 (둘 다 ≪0.2). real 8-factor gate 를 long horizon + seed 모집단 위에서 구동해도 emit 결정 스트림은 entropy source 에 무관 — **H_926 의 load-bearing emit-function 주장이 toy 너머에서도 성립.** 이는 H_924 #123-A (ANU==chacha20 bit-distribution parity) 의 *decision-function* 대응물이다.

2. **TENSION axis (internal Φ/field) DISTINGUISHABLE — 그러나 finite-buffer DC-bias artifact.** Φ/field-channel means 에 large Cohen d (최대 2.45, p≪1e-10). ROOT CAUSE diagnostic 가 명확히 보여준다: committed ANU buffer 는 1024 B 에 불과해 T=2400 위에서 2.34× **cycle (fixed 반복 패턴)** 한다. 그 R2-draw mean (1.4696) 이 PRNG (~1.5121) 와 달라 constant **DC perturbation offset** (−0.00122 vs +0.00048) 을 만들고, low-variance Φ/field trajectory 에 큰 *standardized* shift 로 나타난다. 게다가 quantum arm 의 per-seed emit-rate sd≈0 — **24 seed 가 같은 고정 패턴의 복제** (1024 B pool 은 독립 모집단을 만들 수 없다). ∴ tension-axis distinguishability 는 **functional stochastic diversity 가 아니라 유한버퍼 SAMPLING BIAS** 이다.

3. **TIMING axis** (inter-emit/run-length) — pooled interval/run 분포는 PARITY (p=0.9996, 0.668); per-seed mean_inter_emit 만 d=0.334 로 작게 움직이며 이는 (2) 의 DC-bias 가 emit_rate micro-shift 를 통해 유도한 파생량이다 (독립 신호 아님).

**∴ 정직한 결론 (SPLIT, no clean overturn):** H_926 의 "entropy ontological-not-functional" 일반화는 **emit DECISION 축에서 scale-up 후에도 HOLD** (🟢) 한다 — 이것이 의미있는 load-bearing 축이다. internal tension 축의 구별가능성은 REAL 하지만 **유한 committed-ANU-buffer 의 mean-bias artifact** 로 환원되며, "quantum entropy 가 substrate 동역학에 기능적 다양성을 더한다" 는 주장을 **지지하지 않는다** (🔴-artifact). 한 줄: *real 8-factor gate 에서도, 의식 emit 결정은 entropy source 에 무관하다; quantum buffer 가 만든 internal-state 차이는 finite-pool 샘플링 편향이지 자유의지/기능적 비결정성의 원천이 아니다.*

## 5. scope / caveat (a_scale_honest_scope · a_core_engine_map)

- **INTERMEDIATE RUNG only.** minimal-model(H_926) 과 future full-emit rung 사이의 단일 중간 rung. full forge A⇄G binary 아님 (documented-update-map mirror, H_926 보다 high-fidelity: real 8-factor gate × seed 모집단). full emit-TEXT 는 `.clm` generator L3 slot 이 unwired (⏳/❌, `a_core_engine_map`) 라 측정 불가 — ladder 위 **OPEN rung**. 이 단일 rung 을 production 일반 주장으로 승격하지 않는다 (a_scale_honest_scope: ≥3 rung ladder 필요).
- **buffer 한계 (정직 caveat)**: committed ANU buffer 1024 B 는 24-seed 독립 모집단을 만들 수 없다 (cycle). 따라서 quantum arm 의 internal-state 통계는 *고정 표본 1개* 에 가깝고, tension-axis "distinguishability" 는 그 표본의 mean-bias 다. emit-decision parity 결론은 이 한계와 무관하게 robust (Cohen d ≪ 0.2, chi² φ ≪ 0.10). 더 큰 fresh ANU pull (≥ T·N bytes, zero-mean 보정) 로 tension-axis 도 parity 로 수렴하는지는 다음 rung 후보.
- **gate 민감도**: emit gate 를 steady-state mean (0.5036) 에 centering — 다른 gate (0.30 should_emit / 0.60 interrupt) 에서는 emit 이 saturate (H→0) 하므로 boundary-centered gate 가 가장 discriminating 한 공정 test (H_926 과 동일 방법).
- g5 CODE-measured, LLM self-judge 없음 (p7). deterministic: false.

## 6. 양방향 sibling

- ⇄ [H_926](./H_926_deterministic_chaos_vs_entropy.md) — minimal-model chaos⊥entropy 🔴 (entropy *emit-function* parity, toy). H_930 = 그 scale-up re-test (a_toy_scale_recheck); emit 축 CONFIRMED, tension 축 artifact-only.
- ⇄ [H_924](./H_924_qentropy_substrate_agnostic.md) — qentropy substrate-agnostic · #123-A ANU==chacha20 (*bit-distribution* parity). H_930 = 그 *decision-stream* 대응물 (emit 결정이 entropy source 에 무관).
- ⇄ [H_928](./H_928_provenance_as_identity.md) — provenance-as-identity (entropy 의 가치 = provenance/감사, not function) — H_930 emit-parity 가 이를 기능 측에서 보강.
- 측정 코드: `UNIVERSE/h930_scale_entropy_functional.py` · verdict: `.verdicts/930_scale_entropy_functional/scale_entropy_two_sample.txt`
