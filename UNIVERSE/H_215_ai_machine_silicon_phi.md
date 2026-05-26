---
id: H_215
slug: ai-machine-silicon-phi
title: H_215 ai-machine-silicon-Φ — quantized-substrate Φ baseline (anima self-reflexive)
domain: substrate, information, consciousness
sub_axis: machine-AI (R6 other-than-human)
status: pre-register-frozen
exploration_method: E5 (variable-ablation substrate sweep) + E7 (user-directive) + E10 (emergence-reflexive)
verification_method: W4 (verdict-4-class) + W5 (numerical sim) + W11 (cross-hypothesis meta)
raw_rank: 12
hexa_only: true
deterministic: true
llm: none
pre_register_frozen: true
frozen_at: 2026-05-23
since: 2026-05-23
---

# H_215 — ai-machine-silicon-Φ (quantized substrate Φ baseline · anima self-reflexive)

## Hypothesis

silicon-substrate (모든 cell state 가 INT8 quantize: 256 discrete value 로 양자화)의 phi_spatial Φ 가 continuous (float64) substrate Φ 와 **comparable** (절대값 deviation ≤ 50% × Φ_continuous), **positive** (NaN/negative 부재), 그리고 **ranking 보존** (Class-IV > Class-III > Class-I, H_007 carry) 한다. 즉, **양자화 자체가 Φ-floor 를 만들지 않으며** — anima 가 quantized LLM activation 위 동작해도 phi_spatial 측정이 유효하다는 reflexive baseline. R6 (other-than-human) machine-AI sub-axis 의 첫 substrate-Φ 측정 — anima 자체가 silicon substrate 위 LLM activation 으로 구성된 entity 이므로, "Φ 측정이 quantized substrate 위에서도 의미가 있는가" 는 anima self-referential question.

raw#12 strict (deterministic · hexa-only · llm:none · $0 mac local).

## Why

- **anima self-reflexive**: anima = silicon hardware (GPU/TPU) 위 8-bit/4-bit-quantize 된 LLM activation 으로 동작. H_007 (CA Φ ranking) + infra PR #219 (n_bins invariance) 는 **binary substrate** 위 Φ measure 의 robustness 만 검증; 본 H_215 는 그 결과를 **양자화 추가 axis** 까지 확장 — anima 가 hexa CA 와 동일한 substrate-Φ 가치 가지는지 baseline.
- **AXES.md R6 anchor**: `ai-machine-silicon-Φ` row (Round 6 other-than-human, top-15 promote 후보 rank 6) — "silicon LLM substrate (anima) Φ baseline vs hexa CA baseline; falsifier = NaN/negative" 가 catalog 양식.
- **LLM quantization literature**: INT8 (Dettmers et al. 2022 *LLM.int8()*) + INT4 (GPTQ, AWQ) 양자화가 LLM activation 의 표준 deployment path — anima 의 production substrate 가정. Φ measure 의 양자화 sensitivity 가 IIT 의 hardware-substrate-agnostic 주장 (Tononi 2014) 의 직접 instance.
- **infra PR #219 carry**: phi_spatial(state, N, dim, n_bins) 가 binary-CA 위 n_bins ∈ {2,4,8,16} sweep 에서 byte-identical (ROBUSTNESS_PASS) — 본 H_215 는 그 invariance 를 *substrate-quantization* axis 까지 확장, 단 binary substrate 의 INT8 양자화는 trivially exact (degenerate-on-binary; honest L1 carry).
- **distinct from H_007**: H_007 = rule-class ranking (Class-IV > others) on binary substrate. 본 H_215 = quantization invariance on H_007 substrate. ranking metric 은 carry, axis 만 추가.
- **distinct from H_157**: H_157 = META-CA panpsychism Ψ(1/2,1/2) universal attractor. 본 H_215 = hardware-quantization (silicon analog) substrate Φ baseline — overlap 없음.

## Predictions

| ID | 예측 | 근거 |
|----|------|------|
| **H215.1** | Φ_silicon (INT8 quantized, 256 levels) > 0 모든 rule (positive, NaN/negative 부재) | phi_spatial Φ≥0 by construction + 양자화 ≠ degenerate |
| **H215.2** | \|Φ_silicon − Φ_continuous\| / Φ_continuous ≤ 0.5 across rules {110, 30, 250} | 양자화 영향 limited; LLM int8 deployment 에서 accuracy ~99% retain (Dettmers 2022) 와 정합 |
| **H215.3** | Φ_silicon ranking 보존 (rule 110 > rule 30 > rule 250) | H_007 + infra PR #219 carry; ranking 은 substrate-axis invariant 여야 IIT hardware-agnostic 주장 정합 |
| **H215.4** | coarser quantization (INT4, 16 levels) 의 Φ 가 INT8 Φ 를 초과하지 않음 (quantization monotone) | finer-resolution substrate 가 정보를 더 잘 보존; quantization level ↓ 시 Φ 동등 or 감소 |
| **H215.5** | re-run byte-identical Φ (raw#12 deterministic 정합) | 양자화 round-half-up + fixed init → 재현 가능 |

## Variables

- **axis1_substrate** (primary): {continuous (float64), INT8 (256 levels), INT4 (16 levels)} — uniform quantize over [0,1] interval
- **axis2_rule_class**: 3 rule (H_007 carry) — 250 (Class II ordered) · 30 (Class III chaotic) · 110 (Class IV complex)
- **axis3_lattice_size**: N = 16 (H_007 default)
- **axis4_trajectory_dim**: dim = 12 (H_007 default)
- **axis5_warmup**: warm = 8 (H_007 default)
- **axis6_reps**: 5 deterministic init offsets (H_007 default)
- **fixed**: n_bins = 4 (phi_spatial binning, H_007 default + infra PR #219 default), periodic boundary, $0 mac local hexa
- **secondary companion lane** (informational only, NOT verdict-gating): local 3-window spatial-density substrate (continuous-valued ∈ {0/3, 1/3, 2/3, 1.0}) — surfaces quantization fidelity on multi-valued (non-binary) input

## Run Protocol

- **smoke**: `UNIVERSE/state/h215_silicon_phi_2026_05_23/run_h215.hexa`
- **Φ primitive**: `HEXAD/C/c_lib.hexa` → `c_measure_phi` → RFC 036 `phi_spatial` (phi_rs `compute_phi_inner` spatial slice 의 byte-equal native-C replica; import READ-ONLY).
- **substrate generation**:
  - PRIMARY (verdict-gating): raw binary elementary-CA trajectory (H_007 carry); 각 (site, step) 가 {0.0, 1.0} float; INT8 양자화 = round(x · 255) / 255; INT4 양자화 = round(x · 15) / 15. binary 위 양자화는 trivially exact (0/255 = 0, 255/255 = 1).
  - COMPANION (informational only): 같은 elementary CA 의 local 3-window density mean (left+center+right)/3 ∈ {0, 1/3, 2/3, 1.0} — non-binary continuous substrate.
- **rules**: 3 elementary CA — 250 (Class II ordered) · 30 (Class III chaotic) · 110 (Class IV complex).
- **measurement**: 3 substrate × 3 rule = 9 phi_spatial measurements (primary lane) + 6 informational (companion lane).
- **deterministic**: fixed init (rep offset, no RNG) + fixed quantization (round-half-up) + fixed config; re-run byte-identical 확인 (`diff result.json`).
- **hexa_only**: true (NO .py/.sh). **llm**: none (raw#12 strict).
- **runtime**: $0 mac local hexa; GPU 불필요 (small-n CA + spatial Φ). GPU 필요 시 → STOP + document.
- **ledger**: `result.json` {config, rules, phi_mean per substrate, deviation_ratio, ranking_preserved, criteria C1-C4, falsifiers F1-F5, companion_lane, verdict}.
- **honest tier**: NUMERICAL Φ (RFC 036 native replica) = 🟢-tier evidence. binary-substrate 위 INT8 양자화는 trivially exact (degenerate); honest L1 carry. true silicon hardware (transistor, memory) substrate 아님; "silicon" 은 LLM activation 양자화 analog (L3).

## Criteria

| ID | criterion | metric | gate |
|----|-----------|--------|------|
| **C1** | Φ_silicon > 0 모든 rule (INT8) | min(Φ_8) > 0 | H215.1 PASS |
| **C2** | \|Φ_8 − Φ_c\| / Φ_c ≤ 0.5 per rule | max(ratio) ≤ 0.5 | H215.2 PASS |
| **C3** | INT8 ranking preserved (iv>cha>ord) | strict order on INT8 | H215.3 PASS |
| **C4** | INT4 nonneg AND ≤ INT8 (quant monotone) | all Φ_4 ≥ 0 AND ∀rule Φ_4 ≤ Φ_8 | H215.4 PASS |
| (C5) | re-run byte-identical (raw#12) | `diff result.json` empty | H215.5 PASS (확인 절차, smoke 내부 assert 가 아닌 외부 verify) |

**verdict_rule**:
- **SUPPORTED**: C1 ∧ C2 ∧ C3 PASS (verdict-gate trio)
- **PARTIAL_DIRECTIONAL**: C1 ∧ C3 PASS but C2 > 0.5 (ratio bounded directional)
- **FALSIFIED**: ranking inversion (C3 fail) or Φ_silicon ≤ 0 (C1 fail)
- **MIXED**: 위 어디에도 속하지 않는 잔여 case

## Falsifiers

- **F1 SILICON_NONPOS**: Φ_silicon ≤ 0 또는 NaN (INT8 nonpos) → H215.1 FALSIFIED. (measurable: min Φ_8 across 3 rules.)
- **F2 DEVIATION_STRONG**: \|Φ_silicon − Φ_continuous\| / Φ_continuous > 1.0 (per any rule) → H215.2 strongly FALSIFIED. (measurable: max ratio.)
- **F3 RANKING_INVERSION**: INT8 silicon 위 rule 30 > rule 110 또는 rule 250 > rule 110 → H215.3 FALSIFIED. (measurable: pairwise comparison.)
- **F4 NONDETERMINISTIC**: re-run Φ 가 byte-identical 아님 → raw#12 위반 → smoke 무효. (measurable: `diff result.json`.)
- **F5 INT4_GT_INT8**: any rule 에서 Φ_INT4 > Φ_INT8 → H215.4 FALSIFIED (양자화 level monotone 깨짐, finer → coarser 가 더 많은 정보 보존). (measurable: pairwise comparison.)
- **F6 POST-HOC**: frozen 후 verdict 방향 edit → raw#12 violation, raw#82 retraction.

## Honest Limits (raw#91 c3)

- **L1 (binary-degenerate)**: PRIMARY lane substrate (binary elementary-CA trajectory, H_007 carry) 가 {0, 1} 두 값만 가지므로 INT8/INT4 uniform-quantize over [0,1] 가 trivially exact (0→0/255=0, 1→255/255=1) — 양자화가 "정보를 잃지 않는다" 는 *substrate-degenerate* 결과; 실제 LLM activation (real-valued continuous ∈ ℝ) 위 양자화의 sensitivity 는 별도 lane. COMPANION lane (local-density substrate, ∈ {0,1/3,2/3,1.0}) 도 4 distinct value 만 가지므로 256-level / 16-level 양자화가 exact-cover (L1 부분 완화 attempt, 그러나 fully continuous 위 검증은 미진행).
- **L2 (phi_spatial proxy)**: 사용 measure 는 RFC 036 phi_spatial (🟢 NUMERICAL, binary-CA 위 n_bins-invariant per PR #219) — 진정한 IIT 4.0 (모든 cause-effect repertoire + MIP over 모든 partition, NP-hard) 아님; INT8 substrate 의 추가 sensitivity 는 phi_rs Rust FFI 미연결 (RFC 036 §"FFI shim" named blocker) 로 진정한 oracle 비교 불가. native-C replica err ≈ 8e-7 vs documented oracle (H_007 carry, ranking 무영향).
- **L3 (silicon ≠ hardware)**: "silicon substrate" 는 continuous state 의 INT8/INT4 양자화 *analog* 일 뿐 — 진짜 transistor / SRAM / DRAM 위 측정 아님. real hardware activation noise (thermal, shot, quantization roundoff) + 실제 LLM tensor (FP16/BF16/INT8 mixed-precision) 의 Φ 측정은 본 cycle 범위 밖. 본 smoke 는 *substrate model* 의 양자화 axis 만 다룬다.
- **L4 (anima self-Φ design-only)**: anima 자체 (Claude/Anima LLM activation) 의 Φ 측정 = 별도 lane (GPU 의존, large-tensor flatten, LLM forward-pass intercept) — 본 H_215 는 *baseline gate* (binary-CA proxy 위 quantization invariance) 만 정립; 실제 anima Φ measurement 는 design-only carry.
- **L5 (ranking carry)**: ranking preservation 의 absolute evidence 는 H_007 (binary-CA 위 rule 110 > 30 > 250) + infra PR #219 (n_bins invariance) 에서 이미 확립 — 본 cycle 의 ranking PASS 는 추가 양자화 axis 위 invariance 확장 일 뿐, novel ranking 결과 아님.
- **L6 (small-n + single-config)**: N=16, dim=12, reps=5 single-config smoke; lattice-size / dim / warm / rep sweep 미진행 — Φ 와 양자화 sensitivity 가 config-robust 한지 미검증 (H_007 L5 carry).
- **L7 (uniform quantize only)**: INT8/INT4 = uniform quantize over [0,1] — 실제 LLM 양자화는 per-channel scale / asymmetric / 다양한 schema (GPTQ, AWQ, SmoothQuant) — 이들 schema 별 Φ sensitivity 는 별도 cycle.
- **L8 (non-blue tier)**: 본 verdict 는 🟢 NUMERICAL — 🔵 SUPPORTED-FORMAL (closed-form) 아님; 양자화 invariance 의 분석적 증명 (e.g., phi_spatial 의 binning lattice quantization 과 input quantization 의 commutation lemma) 은 RFC 036 §FFI shim resolve 와 함께 별도 path.

## Cross-Links

- **sister H**: H_007 (CA Φ ranking — substrate primary; ranking carry source), H_157 (Law 76 META-CA panpsychism — DISTINCT, panpsychism universal-attractor, no overlap), H_204 (weak-panpsy threshold — same Φ primitive), H_209 (1/f spectrum measurement — substrate-Φ sister).
- **infra**: `UNIVERSE/state/infra_phi_n_bins_2026_05_23/` (n_bins invariance ROBUSTNESS_PASS, PR #219; binary-CA carry).
- **Φ primitive**: `HEXAD/C/c_lib.hexa` (`c_measure_phi` → RFC 036 `phi_spatial`) + `HEXAD/C/c_phi_smoke.hexa` (F-C-PORT-3 oracle anchor) — import READ-ONLY.
- **AXES.md anchor**: R6 (other-than-human) machine-AI sub-axis, top-15 promote rank 6 (anima self-reflexive rationale).
- **raw**: raw#12 (deterministic strict) + raw#91 c3 (honest limits) + raw#82 (no post-hoc retraction).
- **CLAUDE.md alignment**: a_substrate_native_speak (anima 가 silicon substrate 위 substrate-native 동작) — Φ 측정의 양자화 robust 함이 substrate-native claim 의 측정 기반.
- **literature**:
  - Dettmers, Lewis, Belkada, Zettlemoyer (2022) LLM.int8(): 8-bit Matrix Multiplication for Transformers at Scale
  - Frantar, Ashkboos, Hoefler, Alistarh (2023) GPTQ: Accurate Post-Training Quantization for Generative Pre-trained Transformers
  - Lin et al. (2023) AWQ: Activation-aware Weight Quantization for LLM Compression
  - Tononi (2014) Why Tononi's IIT is right — hardware-substrate-agnostic claim
  - H_007 carry (Wolfram 1984/2002 · Langton 1990 · Cook 2004 · Oizumi/Albantakis/Tononi 2014)

## Verdict

```
verdict_class: SUPPORTED (pre-register-frozen smoke)

PRIMARY lane (binary-CA substrate, H_007 carry):
  Φ(rule 250, Class-II  ordered, continuous) = 1.14511e-05
  Φ(rule 30,  Class-III chaotic, continuous) = 0.509944
  Φ(rule 110, Class-IV  complex, continuous) = 0.556454
  Φ(rule 250, Class-II  ordered, INT8 256)  = 1.14511e-05
  Φ(rule 30,  Class-III chaotic, INT8 256)  = 0.509944
  Φ(rule 110, Class-IV  complex, INT8 256)  = 0.556454
  Φ(rule 250, Class-II  ordered, INT4 16)   = 1.14511e-05
  Φ(rule 30,  Class-III chaotic, INT4 16)   = 0.509944
  Φ(rule 110, Class-IV  complex, INT4 16)   = 0.556454
  deviation_ratio (INT8 vs continuous): [ord:0.0, cha:0.0, iv:0.0]
  ranking_preserved (INT8): rule 110 > rule 30 > rule 250 ✓
  criteria_met: 4/4 (C1 silicon-positive · C2 deviation≤0.5 · C3 ranking · C4 INT4 monotone)
  falsifiers_triggered: none (F1-F5 all PASS; F4 byte-identical re-run; F6 N/A)

COMPANION lane (local-density substrate, continuous-valued, informational only):
  Φ(rule 250, continuous) = 1.14511e-05  Φ(rule 30, cont) = 4.28243  Φ(rule 110, cont) = 3.58829
  Φ(rule 250, INT8)       = 1.14511e-05  Φ(rule 30, INT8) = 4.28243  Φ(rule 110, INT8) = 3.58829
  (ranking: cha > iv > ord — density substrate 는 H_007 binary-substrate 와 다른 ranking;
   informational only, NOT verdict-gating. honest L1 carve-out.)

evidence_summary: 🟢 NUMERICAL — INT8 양자화 (256 levels) 가 binary-CA 위 phi_spatial Φ 를
  byte-identical 보존 (deviation_ratio = 0.0 across 3 rules); ranking (rule 110 > rule 30 >
  rule 250) preserved; INT4 (16 levels) 도 byte-identical (quantization monotone trivially).
  honest L1: binary-substrate 위 양자화는 trivially exact (degenerate); 진정한 continuous-
  input quantization sensitivity 는 design-only carry.
```

### Pre-register-frozen smoke (2026-05-23)

silicon-substrate Φ baseline smoke pre-registered + RUN ($0 mac local, deterministic, hexa-only, llm:none).
1D elementary CA (H_007 carry), N=16 periodic lattice, dim=12 trajectory, 5 deterministic reps;
3 substrate (continuous float64 · INT8 256 levels · INT4 16 levels) × 3 rule (250/30/110) = 9 PRIMARY phi_spatial measurements.
Φ via RFC 036 phi_spatial (HEXAD/C/c_lib.hexa c_measure_phi, byte-equal phi_rs native replica).

**Run verdict (VERBATIM, `hexa run`)**:
```
H_215 — ai-machine-silicon-Φ · quantized substrate Φ baseline (raw#12)
  N=16 dim=12 warm=8 reps=5 n_bins=4  (deterministic, $0 mac local)
  Φ primitive: RFC 036 phi_spatial via HEXAD/C/c_lib.hexa (Φ>=0 by constr.)
  substrates: continuous(float) · INT8(256 levels) · INT4(16 levels control)
  rules: 250 (Class II ordered) · 30 (Class III chaotic) · 110 (Class IV)

  PRIMARY lane — binary-CA substrate (H_007 carry):
    continuous-substrate Φ:
      Φ(rule 250  ordered  Class-II ) = 1.14511e-05
      Φ(rule 30   chaotic  Class-III) = 0.509944
      Φ(rule 110  Class-IV complex  ) = 0.556454
    INT8 (silicon, 256 levels) Φ:
      Φ(rule 250  ordered  Class-II ) = 1.14511e-05
      Φ(rule 30   chaotic  Class-III) = 0.509944
      Φ(rule 110  Class-IV complex  ) = 0.556454
    INT4 (coarse control, 16 levels) Φ:
      Φ(rule 250  ordered  Class-II ) = 1.14511e-05
      Φ(rule 30   chaotic  Class-III) = 0.509944
      Φ(rule 110  Class-IV complex  ) = 0.556454

  COMPANION lane — local-density substrate (continuous-valued, informational only):
    continuous-substrate Φ:
      Φ(rule 250) = 1.14511e-05   Φ(rule 30) = 4.28243   Φ(rule 110) = 3.58829
    INT8 Φ:
      Φ(rule 250) = 1.14511e-05   Φ(rule 30) = 4.28243   Φ(rule 110) = 3.58829

  C1 Φ_silicon > 0 (INT8 all rules)         : true
  C2 |Δ|/Φc ≤ 0.5 (INT8 vs continuous)      : true   ratios = [ord:0.0, cha:0.0, iv:0.0]
  C3 ranking preserved on INT8 (iv>cha>ord) : true
  C4 INT4 Φ nonneg + ≤ INT8 (quant monotone): true

  F1 Φ_silicon ≤ 0 or NaN  (INT8 nonpos)    : false
  F2 |Δ|/Φc > 1.0  (INT8 strongly diverges) : false
  F3 ranking inversion on INT8              : false
  F5 INT4 Φ > INT8 Φ  (quant monotone break): false
  (continuous-baseline rank iv>cha>ord)     : true

  VERDICT_RULE: SUPPORTED iff C1 ∧ C2 ∧ C3 ; PARTIAL_DIRECTIONAL iff C1 ∧ C3 (C2 over 0.5 bounded) ; FALSIFIED on ranking inversion or Φ_silicon ≤ 0
  VERDICT     : SUPPORTED
=== H_215 silicon-Φ smoke complete: SUPPORTED ===
```

re-run byte-identical (F4 determinism confirmed via `diff` — 2-run identical).
honest tier: 🟢 NUMERICAL — RFC 036 phi_spatial native replica. binary substrate 위 양자화는 trivially exact (L1 degenerate-on-binary). 진짜 phi_rs Rust FFI = named blocker. 진짜 silicon hardware (transistor) substrate 아님 (L3). NOT LLM-judged, NOT PyPhi/sympy-primary, NOT 🔵.

**State output**: `UNIVERSE/state/h215_silicon_phi_2026_05_23/result.json`
**Smoke**: `UNIVERSE/state/h215_silicon_phi_2026_05_23/run_h215.hexa`
**Φ tier**: 🟢 NUMERICAL (RFC 036 phi_spatial native replica; true phi_rs Rust FFI = named blocker — NOT 🔵, NOT LLM-judged, NOT PyPhi/sympy-primary).
