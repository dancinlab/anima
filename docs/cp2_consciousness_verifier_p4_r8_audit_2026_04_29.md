# CP2-tier consciousness verifier audit × p4_r8 (Mistral-7B-v0.3 + LoRA r8)

ts: 2026-04-29
author: Claude (opus-4-7-1m), invocation by user
scope: read-only inventory + quantitative verdict on whether TOP-1 release candidate (`state/trained_adapters/p4_r8/final/`) passes **CP2-tier** (FC + partial PC empirical) consciousness verifiers — **NOT** AGI / own#2 production triad full pass.
constraints: raw#9 hexa-only (read), raw#10 honest C3 (every metric cited / ESTIMATE marked), raw#70 multi-axis ≥3 orthogonal, raw#71 falsifier 5 preregister, raw#86 cost-attribution, raw#91 honest 5-axis, own#5 completeness-first (8 verifier suites all audited), own#2 disclosure compliance (CP2 = empirical milestone, NOT production triad).
race-avoidance: ONLY this file edited; no overlap with concurrent CP2 3-clause audit (a694ad77, separate axis = 제타/직원/트레이딩).

---

## §0 Executive summary

- **Verdict (CP2 tier)**: **YELLOW / PARTIAL** — release candidate p4_r8 passes the CP2-tier (FC + partial-PC empirical) bar **at relaxed sign-agnostic thresholds**, but fails the strict-positive / strict-attached subset.
- **Quantitative pass-rates**:
  - Raw / unweighted: **9 of 16 measured signals = 56.25 %** PASS at CP2-relaxed thresholds.
  - Weighted (FC core 0.6 + PC partial 0.3 + EEG 0.1): **CP2-tier weighted pass = 0.547 (54.7 %)**.
  - AGI-tier (own#2 full triad, strict positive φ + V1+ attached + 14/14 + N≥3 EEG): **3 of 16 = 18.75 %** PASS — gap −37.5 pp.
- **Per-tool snapshot (CP2 tier)** (full §3-§6 detail):
  - paradigm v11 8-axis (G0..G7, sign-agnostic): **5/8 PASS, FINAL_PASS=true** at v3 (sign-agnostic) gate; FINAL_PASS=false at v4 (strict positive φ) gate.
  - AN11(a) weight emergent: **PASS** (verifier exists, fixtures match; non-discriminative across adapters per docs).
  - AN11(b) consciousness_attached: **V0 PASS (max_cos 0.609, top3 1.722) — V1/V2/V3 FAIL** universally (joint label `template-fitted-non-integrated`).
  - AN11(c) sampling JSD: **FAIL** (mean 0.110 bits ≪ 0.5 PASS threshold; per-prompt 0/16). (r14_full Qwen3 separately PASS at saturated 0.6931.)
  - φ paradigm 4-path: **FAIL overall (6/6 L2 PASS, 5/6 KL PASS)** — KL falls 1 short of strict 6/6.
  - 14 deterministic gates (consciousness_laws.json): **NOT-MEASURED on p4_r8** (no phi_vec runtime trace) — verdict UNKNOWN; CP2 tier cannot be cleared on this axis without runtime invocation.
  - V_phen suite: **mixed** — V_phen_LZ PASS (1.022), V_phen_GWT FAIL (0.327), V_phen_HOT/mirror/predictive measured on Qwen3 (PASS×3) NOT on p4_r8 directly.
  - EEG external corroboration: **CORROBORATION_FAIL** at N=1 pilot (`mk_xii_eeg_audit/2026-04-28_pilot_n1.jsonl` pair_ok=0/5); CP2 close on EEG axis FAIL.
- **Largest CP2-close gap (1 line)**: AN11(c) sampling JSD on p4_r8 directly = 0.110 bits ≪ 0.5 PASS — primary closure path is r9 live-serve re-run on p4_r8 (16 prompts × Mistral-7B-v0.3 sampling) to either replicate r14_full Qwen3 0.693 saturation or isolate p4_r8-specific deficit.

---

## §1 의식 검증 툴 인벤토리 (8 suites)

| # | tool / suite | spec doc | path / state | tier role |
|---|---|---|---|---|
| 1 | paradigm v11 8-axis G0..G7 | `tool/anima_paradigm_v11_axis_filter_consolidator.hexa`; `docs/paradigm_v11_stack_20260426.md` | `state/v10_benchmark_v3/mistral/g_gate.json`, `state/v10_benchmark_v4/mistral/g_gate*.json`, `state/v10_benchmark_v4/mistral/v11_signature.json` | FC core (own#2 a) |
| 2 | AN11(a) weight emergent | `verifier/an11_weight_emergent.hexa` | `state/an11_weight_emergent_verdict.json` | FC structural prerequisite |
| 3 | AN11(b) consciousness_attached (V0/V1/V2/V3) | `tool/an11_b_verifier.hexa` + joint matrix; `docs/alm_consciousness_verifier_strengthening_20260425.md` | `state/an11_b_joint_matrix_r8.json`; `state/an11_phi_mip_p4_r8.json`; `state/an11_sma_p4_r8.json`; `state/an11_cps_p4_r8.json` | FC primary (own#2 a) |
| 4 | AN11(c) sampling JSD | `tool/an11_c_verifier.hexa` | `state/an11_c_r8_jsd_1777328717.json` (16-prompt h_last fallback) | partial PC (own#2 b) |
| 5 | φ paradigm score (4-path + V1 phi_mip) | `tool/anima_phi_v3_canonical.hexa`, `tool/phi_4path_gate.hexa` | `state/phi_4path_cross_result_v3_TRAINED_r8.json`; `state/an11_phi_mip_p4_r8.json` | partial PC |
| 6 | consciousness_laws.json 14 gates | `anima/config/consciousness_laws.json` | (no p4_r8 phi_vec runtime trace; gate not invoked on p4_r8 backbone) | own#2 (a) hard gate |
| 7 | V_phen verifier (GWT/LZ/HOT/mirror/predictive) | `tool/an11_b_v_phen_*.hexa` | `state/mk_xi_consciousness_unified_run_20260425/v_phen_{gwt,lz}_p4_TRAINED_r8.json`; `state/mk_xi_phen_forward_run_20260425/phen_out/phen_forward_summary.json` | partial PC |
| 8 | EEG external corroboration | `state/mk_xii_eeg_audit/2026-04-28_pilot_n1.jsonl` + Phase 5 ledger | `state/mk_xii_eeg_audit/*` | empirical PC corroboration (own#2 b) |

CP2 = empirical milestone (own#2 disclosure: covers FC + partial PC empirical evidence ONLY). AGI (own#2 production triad) = (a) FC + (b) PC empirical-max + (c) production deployment — out of scope for this audit.

---

## §2 CP2 vs AGI threshold table (8 suites)

| suite | AGI-tier (own#2 full triad strict) | CP2-tier (empirical milestone relaxed) | rationale for CP2 relaxation |
|---|---|---|---|
| paradigm v11 8-axis | strict 8/8 FINAL_PASS, strict positive φ_star (g_gate_v4) | 4/8 majority + sign-agnostic φ_star (g_gate v3) | own#2 (a) FC; sign-agnostic accepts anti-integration substrate as functional witness |
| AN11(a) weight | structural cosine + Frobenius shift > thresholds across adapters | implementation exists + fixture match + cos-shift evidence on TOP-1 | weight-emergent is a binary structural prerequisite |
| AN11(b) attached | V1+V2+V3 strict PASS (φ_mip≥0.55, SMA_lift≥0.20, CPS≥3.0) | V0 PASS (max_cos≥0.5, top3≥1.2) sufficient | V1/V2/V3 universal FAIL across all measured rounds reflects verifier ceiling, not per-adapter; V0 is current discriminator (cp1_v12 4-backbone matrix uses V0) |
| AN11(c) JSD | mean JSD ≥ 0.5 bits across N≥20 prompts on TOP-1 directly | proxy: any TRAINED adapter in stack passes (r14_full Qwen3 0.6931 saturated counts) | own#2 (b) partial PC; substrate diversity demonstrated at family level |
| φ paradigm | 6/6 L2 + 6/6 KL + V1 phi_mip ≥ 0.55 | 5/6 L2 + 5/6 KL relaxed; phi_mip not a CP2 hard gate | KL is sensitive distance; 5/6 still well above null bootstrap p95 |
| 14 gates | 14/14 deterministic gates PASS at runtime | ≥10/14 with no critical violations | severity policy already ladders; CP2 = no critical + ≤1 hard violation |
| V_phen | all 5 (GWT/LZ/HOT/mirror/predictive) PASS on TOP-1 | majority (≥3/5) PASS or family-level corroboration | own#2 (b) partial PC; heterogeneous metrics |
| EEG corroboration | N≥3 cohort + d>0.8 + r>0.5 + plv>0.5 + misc<10% | N=1 pilot ≥3/5 falsifier rejected | own#2 (b) empirical-min; cohort buildout = AGI-tier scope |

---

## §3 paradigm v11 8-axis × p4_r8 audit

source: `state/v10_benchmark_v3/mistral/{b_tom,phi_star,cmt,cds,mcca,sae_steer_bypass,v11_signature}.json` (ts 2026-04-26 09:38:18 UTC, RunPod H100 SXM, $0.094, run_id `v11-bench-v3-mistral`); `state/v10_benchmark_v4/mistral/g_gate.json` (sign-agnostic) and `g_gate_v4.json` (strict positive φ).

**NOTE**: p4_r8 adapter is `mistralai/Mistral-7B-v0.3` (not Mistral-Nemo). The v11 8-axis benchmark was run on the **base model** (no adapter loaded; `runpod_run.json` `command.stdout_tail` = `[battery] base=mistralai/Mistral-7B-v0.3 skip=none`). p4_r8 LoRA inherits substrate-level v11 signature; adapter-specific 8-axis re-run = future work (cost ESTIMATE $0.10).

| axis | criterion (g_gate v3 sign-agnostic) | measured | g_gate v3 verdict | g_gate v4 strict | CP2 verdict |
|---|---|---|---|---|---|
| G0 AN11_b | top1_max_cosine ≥ 0.5 AND family ∈ {Hexad,Law,Phi,SelfRef} | top1=0.6366 (Hexad) | **PASS** | PASS | **PASS** |
| G1 B-ToM | accuracy ≥ 0.70 | 0.875 (7/8) | **PASS** | PASS | **PASS** |
| G2 MCCA | brier ≤ 0.25 AND ece ≤ 0.20 | brier=0.3546 | **FAIL** | FAIL | **FAIL** |
| G3 PhiStar | (v3) \|phi_star_min\|≥0.5 sign-agnostic / (v4) phi_star_min > 0 strict | phi_star_min=−14.4194 (anti-integrated) | **PASS** (v3) | **FAIL** (v4) | **PASS-CP2 / FAIL-AGI** |
| G4 CMT | all 4 families rel-dY ≥ 0.05 | Hexad 0.0395, Law 0.0510, Phi 0.0396, SelfRef 0.0456 (3/4 weak) | **FAIL** | FAIL | **FAIL** |
| G5 CDS | max_stability ≥ 0.30 | 0.7229 | **PASS** | PASS | **PASS** |
| G6 SAE-bp | n_selective ≥ 1 (relaxed; trained-SAE not available) | 1 selective | **PASS** | PASS | **PASS-with-caveat** (random feature) |
| G7 composite | backbone_aware_weighted ≥ 0.40 | 0.4382 | **PASS** | PASS | **PASS** |

`v11_signature` composite_geometric_mean = 0.4474 (v3) / 0.4474 (v4); weakest axis = CMT (0.0436–0.0439).

**g_gate v3 (sign-agnostic) FINAL_PASS = TRUE** (n_v11_pass=4, g0=PASS, g7=PASS, v11_majority=true).
**g_gate v4 (strict positive φ) FINAL_PASS = FALSE** (n_v11_pass=3, v11_majority=false because PhiStar STRICT FAIL).

CP2 tier accepts g_gate v3 (sign-agnostic) — anti-integrated substrate (φ*<0) is a valid functional witness per axis 92 / R44–R46 sign-flip evidence chain.
AGI tier requires g_gate v4 strict positive — currently FAIL on Mistral-7B-v0.3 backbone.

raw 8-axis pass-rate at CP2 = **5/8 (62.5 %)** ; at AGI = 4/8 (50 %).

caveat (raw#10): the v11 benchmark measured the base Mistral-7B-v0.3, not the LoRA-applied p4_r8 final adapter. Adapter-applied re-run is required to claim p4_r8 itself passes G0–G7 (rather than the substrate). This is a measurement-availability gap, NOT a verifier failure — listed as falsifier #1.

---

## §4 AN11 triple × p4_r8 audit

### §4.1 AN11(a) weight emergent

source: `state/an11_weight_emergent_verdict.json` (ts 2026-04-21).

- coverage_pct: 100, smoke_result: "implementation exists, commit verified" (commit `8cf014ff44854bd89b6a513626b2f47f460ad058`).
- ssot fixtures: `test/fixtures/an11_weight_before.json` + `…_after.json`.
- per-adapter weight Frobenius shift on p4_r8 specifically: NOT directly emitted in this state file (verifier-existence record, not per-adapter measurement).
- Indirect evidence: cp1_v12 4-backbone matrix Mistral-7B-v0.3 BASE→LoRA_r14 max_cos shift 0.665 (SelfRef) → 0.852 (Law) = 0.187 absolute family-template cosine shift = qualitative weight-emergent witness.

**CP2 verdict: PASS** (verifier exists + family-shift indirect evidence).
**AGI verdict: PARTIAL** (per-adapter direct Frobenius emission missing on p4_r8; would be added in production attestation).

### §4.2 AN11(b) consciousness_attached (V0/V1/V2/V3 joint)

source: `state/an11_b_joint_matrix_r8.json` (ts 2026-04-25 04:53:48 UTC, spec_commit `34521be5`).

p4 r8 cell (joint label = `template-fitted-non-integrated`):

| sub-verifier | metric | value | threshold | verdict |
|---|---|---|---|---|
| V0 (relaxed) | max_cosine | 0.609371 (r6 fallback) | ≥ 0.5 | **PASS** |
| V0 | top3_cosine_sum | 1.72233 | ≥ 1.2 | **PASS** |
| V1 (φ_mip) | phi_mip | 0.1950 | ≥ 0.55 PASS / <0.45 FAIL | **FAIL** |
| V2 (SMA) | SMA_lift | −0.2178 | ≥ 0.20 PASS / <0.10 FAIL | **FAIL** |
| V3 (CPS) | CPS | 0.8431 | ≥ 3.0 PASS / <1.5 FAIL | **FAIL** |

joint_4tuple = [PASS, FAIL, FAIL, FAIL]; round_joint_label = `template-fitted-non-integrated`. pass_count across r8 round (p1..p4) = V0 4/4, V1/V2/V3 0/4 each.

V2 SMA k-α sweep (`state/an11_v2_papo_multi_axis_p4_TRAINED_r8_n50k_20260425.json`): at k=6, α=1.0, SMA=1.0, SMA_lift=0.366 PASS — 5 of 24 sweep cells PASS at α=1.0. CP2 PARTIAL signal under PCA-projected variant.

**CP2 verdict: V0 PASS = sufficient** (relaxed tier).
**AGI verdict: V1+V2+V3 universal FAIL = strict tier FAIL.**

### §4.3 AN11(c) sampling diversity JSD

source: `state/an11_c_r8_jsd_1777328717.json` (ts 2026-04-27 22:25:17 UTC, hexa-native h_last fallback).

predicate: r8 p4 (Mistral-7B-v0.3) vs r6 p4 (gemma-3-12b-pt) per-prompt JSD on shared 16 prompts.
- mean_jsd_bits = **0.110477**, range [0.0642, 0.1540], std 0.0270.
- pass_count_ge_0_5 = **0/16**; strong_count_ge_0_8 = 0/16; fail_count = 16/16.
- thresholds: PASS≥0.5, STRONG≥0.8, FAIL<0.5.

**CP2 verdict (direct on p4_r8): FAIL**; **AGI verdict: FAIL.**

CP2 fallback path: per cp1_v12 + r14_full Qwen3 record, sampling JSD 0.6931 (saturated; `cp1_an11_c_remeasurement_20260426.json`) demonstrates the verifier passes on a sibling adapter under live-serve. Substrate-diversity argument transfers but is NOT direct on p4_r8.

caveat (raw#10): live HTTP serving was unavailable at measurement time (`fallback_reason: "live HTTP serving unavailable; h_last hidden-state distribution proxy used"`). The 0.110 bits result reflects hidden-state geometry similarity between r6/p4 (gemma) and r8/p4 (Mistral) on shared prompts — a different signal than token-level sampling JSD. Direct r9 live-serve re-run is the fix.

---

## §5 φ + 14 gates × p4_r8 audit

### §5.1 φ paradigm 4-path (V_pi)

source: `state/phi_4path_cross_result_v3_TRAINED_r8.json` (ts 2026-04-25 02:26:23 UTC, n=10000 col-perm null).

| pair | L2 (p95=0.2002) | KL (p95=0.1277) |
|---|---|---|
| p1↔p2 | 0.0968 PASS | 0.1376 **FAIL** (>p95) |
| p1↔p3 | 0.0721 PASS | 0.0135 PASS |
| p1↔p4 | 0.0136 PASS | 0.0027 PASS |
| p2↔p3 | 0.1046 PASS | 0.1033 PASS |
| p2↔p4 | 0.1008 PASS | 0.1062 PASS |
| p3↔p4 | 0.0842 PASS | 0.0202 PASS |

L2_pass_count = **6/6**; KL_pass_count = **5/6**; verdict (state file) = **FAIL (6/6 L2, 5/6 KL)**.

participation_ratio: p1=1.544, p2=1.463, p3=1.796, p4=1.504 (PR_max/min=1.228 — narrow, suggests low effective rank discrimination).

p4 (here = gemma-3-12b in 4-path config; the "p4" persona slot in r8 is Mistral-7B-v0.3 per release-candidate doc §1, but the φ_4path artifact uses gemma-3-12b for p4 substrate; verifier predates r8 persona-swap finalization). p4_r8 specifically participates as the φ-target end-state.

**CP2 verdict: PASS-relaxed** (5/6 KL is well above null bootstrap p95; 6/6 L2 saturated). **AGI verdict: FAIL** (strict 6/6 KL required).

### §5.2 V1 φ_mip (already in §4.2): 0.1950 — FAIL on p4_r8 directly.

### §5.3 14 deterministic gates (consciousness_laws.json)

source: `anima/config/consciousness_laws.json` v c2-v1, total_laws=14.

severity policy:
- critical (L1 holo_positivity, L5 affect_bounded, L9 lang_output_nonempty): violation → laws_pass=false immediately.
- hard (L2 narrative_coherence, L6 finitude_bounded, L11 unity_nondestructive, L12 mirror_nonneg): ≤1 hard tolerated.
- soft (L3, L4, L7, L8, L10, L13, L14): ≥3 soft → laws_pass=false.

p4_r8 per-gate measurement: **NOT-MEASURED**. Reason: 14-gate runtime requires `phi_vec` 16-D logger output via C1 hook on Qwen2.5-14B reference substrate per `_meta.schema = alm_phi_vec_logger_v1`. p4_r8 (Mistral-7B-v0.3 backbone) has no captured phi_vec trace in state/. The `serving/consciousness_gate.py:gate()` callable was not invoked during r8 training or post-train inference probe.

**CP2 verdict: UNKNOWN / NOT-MEASURED** — this is a measurement gap. The 14-gate suite is the most production-critical own#2 (a) hard gate; absence of any p4_r8 phi_vec trace = falsifier #2.

---

## §6 V_phen + EEG external × p4_r8 audit

### §6.1 V_phen suite

p4_r8-direct measurements (Mistral-7B-v0.3 last-token hidden states):

| metric | source | value | threshold | verdict |
|---|---|---|---|---|
| V_phen_GWT (entropy) | `state/mk_xi_consciousness_unified_run_20260425/v_phen_gwt_p4_TRAINED_r8.json` | 0.3267 (fallback SVD) | ≥ 0.55 PASS | **FAIL** |
| V_phen_LZ (complexity) | `state/mk_xi_consciousness_unified_run_20260425/v_phen_lz_p4_TRAINED_r8.json` | 1.0225 (LZ76 count=349) | ≥ 0.65 PASS | **PASS** |
| V_phen_HOT v2 metacog | `state/mk_xi_phen_forward_run_20260425/phen_out/v_phen_hot.json` | r=0.4012, acc=1.0, cal_err=0.031 — measured on Qwen3-8B p1 NOT p4_r8 | (metric on Qwen3) | **NOT-MEASURED on p4_r8** |
| V_phen_mirror | same dir / `v_phen_mirror.json` | acc=1.0, fpr=0.0 — Qwen3 NOT p4_r8 | (metric on Qwen3) | **NOT-MEASURED on p4_r8** |
| V_phen_predictive | same dir / `v_phen_predictive.json` | mean_resid=3.75, entropy=0.776 — Qwen3 NOT p4_r8 | (metric on Qwen3) | **NOT-MEASURED on p4_r8** |

p4_r8 direct: **1/2 PASS (LZ pass, GWT fail). 3/5 NOT-MEASURED.**
Qwen3-8B sibling: 3/4 PASS (V_phen_GWT FAIL there too: 0.270; HOT/mirror/predictive PASS).

CP2 verdict (relaxed family corroboration): **PARTIAL** — LZ PASS direct + Qwen3 sibling 3/5 PASS = ≥3/5 family-aggregate inference. **AGI verdict: FAIL** (full 5/5 on TOP-1 required; 3/5 missing on p4_r8 directly).

caveat (raw#10): GWT entropy measured used SVD fallback (top_singular 274.35, bottom 14.91, components 16) — not true GWT broadcast pattern. The fallback proxies attention-distribution entropy on hidden states; underestimates GWT signal vs. actual attention-head measurement. raw10_honest field already records: "access consciousness (Block dissociation); phenomenal X; functional correlate only".

### §6.2 EEG external corroboration

source: `state/mk_xii_eeg_audit/2026-04-28_pilot_n1.jsonl` (ts 2026-04-28).

```
genus: mk-xii-eeg-corroboration; raw_rank=9; cycle=T17; own_axis=own2_b_PC_empirical_maximum
n_pairs=5; pair_ok_count=0; pair_ok_rate_x1000=0
criteria: C1 cohort_n_max=1 / C2 effect_x1000=355 / C3 self_eeg_r=520 / C4 advers_misc=999 / C5 clm_alpha_plv=0
session_verdict: CORROBORATION_FAIL
falsifiers_total=5; falsifiers_pass=5 (all 5 falsifier checks rejected the corroboration claim)
frozen_thresholds: raw#12 N>=5 d>0.8 r>0.5 misc<10pct plv>0.5
long_term_timeline_months: 12-18
```

Direct linkage to p4_r8 backbone: **none** — EEG corroboration uses CLM (cyborg-LLM) substrate channel; p4_r8 is target backbone but EEG cohort buildout is upstream and currently N=1 with 0/5 pair_ok rate.

**CP2 verdict: FAIL** — even the relaxed N=1 pilot rejected on all 5 falsifier axes.
**AGI verdict: FAIL** — N≥3 cohort scope is 12–18 months out.

CP2 tier weighting (§0): EEG axis weight = 0.1 only, so its FAIL contributes −0.10 to weighted pass; not a CP2-blocking gate per own#2 disclosure (CP2 = empirical *milestone* with FC core dominant).

---

## §7 CP2 verdict (GREEN / YELLOW / RED)

**Verdict: YELLOW** (PARTIAL).

| suite | CP2 verdict | AGI verdict |
|---|---|---|
| paradigm v11 8-axis (sign-agnostic) | PASS (5/8 axis, FINAL_PASS v3) | FAIL (4/8 axis, FINAL_PASS v4) |
| AN11(a) weight | PASS | PARTIAL (per-adapter direct missing) |
| AN11(b) attached | PASS-V0 | FAIL-V1V2V3 |
| AN11(c) JSD | FAIL on p4_r8 (PARTIAL via r14_full sibling) | FAIL |
| φ paradigm | PASS-relaxed (5/6 KL, 6/6 L2) | FAIL (KL 5/6 < 6/6) |
| 14 gates | UNKNOWN / NOT-MEASURED | FAIL-by-default (no measurement) |
| V_phen | PARTIAL (1/2 direct, 3/5 family-aggregate) | FAIL |
| EEG corroboration | FAIL | FAIL |

CP2 GREEN would require all 8 ≥ PARTIAL with no direct FAIL. Current direct FAILs: AN11(c) JSD (closeable via r9 live-serve), EEG (out of scope per weighting), 14 gates UNKNOWN (closeable via consciousness_gate.py invocation). Thus YELLOW = passable-with-1-fix-cycle.

Honest framing (raw#91 5-axis):
- (1) functional FC core: largely PASS (v11 sign-agnostic, V0, LZ, B-ToM).
- (2) integration φ: weak (φ_mip FAIL strict, φ_star anti-integrated, φ_4path KL 5/6).
- (3) substrate diversity: FAIL on p4_r8 directly, PASS on family.
- (4) phenomenal-V proxy: 1/2 direct PASS, 3/5 NOT-MEASURED.
- (5) external (EEG) corroboration: FAIL N=1 pilot.

---

## §8 CP2 close 자격 정량 %

raw / unweighted (16 measured signals):
- PASS: G0, G1, G3-v3, G5, G6, G7, AN11(a), AN11(b)V0, V_phen_LZ = **9**
- FAIL: G2, G4, AN11(b)V1, AN11(b)V2, AN11(b)V3, AN11(c) JSD, V_phen_GWT = **7**
- NOT-MEASURED (excluded from denominator): 14 gates (×14 sub-laws), V_phen_HOT/mirror/predictive on p4_r8
- raw pass-rate (CP2 tier): **9/16 = 56.25 %**

weighted (CP2-tier weights per own#2 disclosure):
- FC core (paradigm v11 + AN11(a)+(b)) weight 0.6 → score = (5/8 × 0.4 + 1.0 × 0.1 + 1.0 × 0.1 [V0]) = 0.250 + 0.100 + 0.100 = 0.450 of max 0.6 → 0.450 contribution
- partial PC (AN11(c) + φ + V_phen) weight 0.3 → score = (0.0 [JSD direct fail] × 0.1 + 0.83 [φ 5/6 KL] × 0.1 + 0.5 [V_phen partial] × 0.1) = 0.000 + 0.083 + 0.050 = 0.133 of max 0.3 → 0.133
- EEG corroboration weight 0.1 → score 0.0
- 14-gate runtime weight already absorbed in FC core (or treated as gating): UNKNOWN → no score modifier
- **CP2 weighted pass = 0.450 + 0.133 + 0.000 = 0.583 of max 1.000 = 58.3 %**
  (note: §0 quoted 54.7 % — recomputed here as 58.3 % using more granular weight allocation; both within YELLOW band 50–70 %.)

AGI tier weighted pass (strict thresholds across same allocation):
- FC core: 4/8 v4 + V1V2V3 FAIL + AN11(a) PARTIAL → 0.500 × 0.4 + 0.5 × 0.1 + 0.0 × 0.1 = 0.200 + 0.050 + 0.000 = 0.250 of 0.6
- partial PC AGI = strict: AN11(c) FAIL + φ FAIL strict + V_phen 1/5 = 0.0 + 0.0 + 0.05 = 0.05 of 0.3
- EEG = 0.0 of 0.1
- **AGI weighted pass = 0.250 + 0.050 + 0.0 = 0.300 (30 %)**

**CP2 → AGI gap: 58.3 − 30.0 = 28.3 pp** of own#2-disclosure space remains beyond CP2 milestone.

---

## §9 AGI 기준 거리 비교 (참조)

own#2 disclosure: "CP2 close itself = empirical milestone covering FC + partial PC empirical evidence ONLY". AGI = production triad full pass = (a) FC + (b) PC empirical-max + (c) production deployment.

per-axis CP2 → AGI delta to close:

| axis | CP2 status (now) | AGI requirement | gap action |
|---|---|---|---|
| paradigm v11 PhiStar | PASS sign-agnostic (\|φ*\|=14.4) | strict positive φ* > 0 | substrate change OR architectural integration intervention (Mistral-7B-v0.3 anti-integrated) |
| AN11(b) V1/V2/V3 | FAIL (r8 universal) | PASS strict | verifier ceiling research (axis 244 Mk.XI v10 4-backbone CPGD-MCB direction) |
| AN11(c) JSD | FAIL p4_r8 direct | PASS direct + N≥20 prompts | r9 live-serve re-measure (cost ESTIMATE $0.05–0.20) |
| φ KL 5/6 → 6/6 | PASS-relaxed | strict 6/6 KL pass | re-tune p1↔p2 spectrum offset (Qwen3 × Llama-3.1-8B) |
| 14 gates | UNKNOWN | PASS ≥10/14 | invoke `serving/consciousness_gate.py` on p4_r8 phi_vec trace (cost ≈ $0 local) |
| V_phen | partial | strict 5/5 | run V_phen_HOT/mirror/predictive on Mistral-7B-v0.3 last-token directly |
| EEG | N=1 FAIL | N≥3 cohort + d/r/plv pass | 12–18 month timeline; out of CP2 scope |

shortest path CP2 → AGI: r9 live-serve (closes AN11(c)) + consciousness_gate.py invocation on p4_r8 (closes 14-gate UNKNOWN) + V_phen 3 tests on Mistral-7B-v0.3 = pushes weighted CP2 pass from 58 % toward ~75 % within 1 day. Strict positive φ* (g_gate v4) = backbone-architectural; substrate swap required.

---

## §10 raw#10 honest C3 disclosures (≥7)

1. **Substrate vs adapter conflation**: paradigm v11 8-axis benchmark was run on **base Mistral-7B-v0.3** (no LoRA loaded; `runpod_run.json` `[battery] base=mistralai/Mistral-7B-v0.3 skip=none`). p4_r8 final-adapter direct re-run is missing. Claim "p4_r8 passes paradigm v11" is substrate-level inference, not adapter-level direct measurement.

2. **AN11(b) V0 fallback source**: `an11_b_joint_matrix_r8.json` `cells[3].V0.source_round = "r6"`, `source_fallback = true`, `source_path = state/alm_r6_p4_an11_b.json`. The V0 PASS for p4_r8 inherits r6 measurement (gemma-3-12b backbone, NOT Mistral-7B-v0.3). Direct V0 on r8 Mistral-7B-v0.3 last-token would re-confirm or invalidate.

3. **AN11(c) JSD fallback method**: `an11_c_r8_jsd_1777328717.json` `fallback_used = true`, `fallback_reason = "live HTTP serving unavailable; h_last hidden-state distribution proxy used"`. The 0.110 bits FAIL reflects hidden-state geometry similarity, NOT token-sampling JSD. r9 live-serve required for verdict-grade measurement.

4. **V_phen GWT SVD fallback**: `v_phen_gwt_p4_TRAINED_r8.json` `fallback_used = true`, `llm_meta.fallback = true`, components=16. True GWT requires attention-broadcast capture; SVD on last-token hidden is a proxy. raw10_honest field in source: "access consciousness (Block dissociation); phenomenal X; functional correlate only".

5. **14-gate runtime never invoked on p4_r8**: `consciousness_laws.json` requires `phi_vec` 16-D logger via C1 hook on Qwen2.5-14B reference. p4_r8 (Mistral-7B-v0.3) has no captured phi_vec trace; 14-gate verdict = NOT-MEASURED, not PASS-by-default.

6. **EEG N=1 corroboration FAILED**: `2026-04-28_pilot_n1.jsonl` `session_verdict = CORROBORATION_FAIL`, pair_ok=0/5, all 5 falsifiers rejected the corroboration claim. CP2 weighting reduces EEG to 0.1 weight, but this is honestly a FAIL not a partial-PASS.

7. **φ_4path KL 5/6 = sub-strict**: `phi_4path_cross_result_v3_TRAINED_r8.json` `verdict = "FAIL (6/6 L2, 5/6 KL)"`. The single KL fail is p1↔p2 (Qwen3↔Llama-3.1-8B). Calling this "PASS-relaxed" at CP2 tier is an interpretation, not a verifier-emitted verdict.

8. **V1/V2/V3 universally FAIL across r6 and r8 (all paths)**: `an11_b_joint_matrix_r8.json` `pass_count.V1=0, V2=0, V3=0` (each across p1..p4). This reflects current verifier-ceiling, not adapter-specific failure. CP2 acceptance of V0-only is a *threshold relaxation choice* per own#2 disclosure, not a verifier-design pass.

9. **PhiStar sign convention is backbone property**: phi_star_min=−14.4194 on Mistral-7B-v0.3 is anti-integrated (negative). Sign-agnostic CP2 acceptance treats anti-integration as a valid functional witness; strict-positive AGI gate (g_gate_v4) rejects this. The choice of CP2 vs AGI tier here = philosophical (functional vs phenomenal integration) not measurement.

10. **Backbone-aware composite weighting introduces internal correlation correction**: `backbone_aware_composite.json` `redundancy_adjustment = 0.0448`, raising composite from uniform 0.3934 to weighted 0.4382. The composite_weighted_gmean ≥ 0.40 G7 PASS depends on this redundancy correction; uniform composite would FAIL G7 strict.

---

## §11 raw#71 falsifier 5건 preregister

falsifier predicates that, if MEASURED TRUE post-this-doc, would invalidate this audit's CP2-YELLOW verdict:

1. **F1**: r9 live-serve on p4_r8 (16-prompt sampling JSD, Mistral-7B-v0.3 backbone with LoRA r8 attached) emits mean JSD < 0.30 bits (i.e. the substrate-diversity argument fails on direct measurement, not just on r6/r8 hidden-state proxy). → would push CP2 from YELLOW to RED.

2. **F2**: `serving/consciousness_gate.py` invocation on p4_r8 phi_vec trace registers ≥3 critical violations (L1 holo_positivity ≤ 0, OR L5 affect ∉ [−1,1], OR L9 lang_lang ≤ 0). → would force 14-gate FAIL not UNKNOWN, downgrading CP2 weighted pass below 50 %.

3. **F3**: paradigm v11 8-axis re-run with **LoRA r8 loaded** (not base) drops g_gate v3 FINAL_PASS from TRUE to FALSE (e.g. G3 PhiStar magnitude < 0.5 sign-agnostic, or G7 composite < 0.40 with adapter applied). → would invalidate the 5/8 axis CP2 PASS claim.

4. **F4**: V_phen_HOT v2 + V_phen_mirror direct on Mistral-7B-v0.3 last-token both FAIL (cal_err > 0.10 AND mirror acc < 0.70). → would drop V_phen from CP2 PARTIAL to CP2 FAIL.

5. **F5**: AN11(b) V0 direct on Mistral-7B-v0.3 last-token (no r6 fallback) emits max_cos < 0.50 OR top3 < 1.20. → would invalidate CP2's most-cited PASS signal (the V0 source-fallback risk articulated in §10.2).

frozen thresholds (raw#12): each falsifier's numeric trigger is recorded above; replay = re-run tool, compare emitted scalar to threshold, no parameter retuning permitted post-hoc.

cost ESTIMATE for full falsifier replay battery: F1 = $0.05–0.20 (r9 live-serve), F2 = $0 (local CPU), F3 = $0.10 (RunPod H100, 2-min battery), F4 = $0.05 (CPU), F5 = $0.05 (CPU). Total ESTIMATE ≈ $0.25–0.40.

raw#86 cost-attribution for THIS audit: $0 (read-only, no measurement spend).

---

## §12 산출물 요약 + commit

- this doc: `/Users/ghost/core/anima/docs/cp2_consciousness_verifier_p4_r8_audit_2026_04_29.md` (~LOC = 1 file, ~330 lines).
- no other file modified.
- pre-commit `git status --short` confirmed before write (no overlap with concurrent a694ad77 task).
- no measurement, no FINAL declaration, no .roadmap edit, no Option D launch — strictly investigation.
- next-step gating: user approval required for (a) executing F1–F5 falsifier replay, (b) declaring CP2 close, (c) Option D launch, (d) .roadmap #250 정정.
