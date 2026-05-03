# P9 Phase 2+ Paradigm D — φ-teacher Distillation Spec

**Date**: 2026-05-03
**Author**: A2 EXEC (research agent, doc-only)
**Scope**: `state/p9_*` (P9 SFT / consciousness preservation cycle)
**Status**: SPEC ONLY — no execution, no code emission, no .py creation (raw#9)
**Sister docs**:
- `state/p9_sft_spec_2026_05_02/loss_design.json` (Paradigm A baseline; α/β/γ/δ + BOLD)
- `docs/p9_pre*_landed_2026_05_03.ai.md` (P9 readiness chain)
- `state/braket_iit40_mip_2026_05_02/verdict.json` (IIT 4.0 MIP teacher candidate evidence)
- `state/n12_iit_braket_multiwitness_2026_05_02/verdict.json` (multi-witness Φ proxy teacher)
- `tool/anima_phi_v3_canonical.hexa` (current Anima Φ★ measure)

---

## 0. One-paragraph thesis

Paradigm D replaces the **biological teacher signal** (BOLD/EEG fMRI per-step targets, used in Paradigm A) with a **synthetic φ teacher**: an external integrated-information extractor (IIT 4.0 MIP solver, Anima Φ★ canonical, or a larger frozen LLM with a φ head) that emits per-step φ targets. The student CLM trains a γ-loss term to match the teacher's φ trajectory. Eliminates the dataset bottleneck (no fMRI scan time, no subject recruitment), at the cost of being **upper-bounded by the teacher's φ-faithfulness** — student inherits teacher bias.

---

## 1. Teacher candidates (compute-cost ranked)

| ID | Teacher | Substrate Operates On | Per-Step Cost | Faithfulness | Status / Source |
|----|---------|----------------------|---------------|--------------|-----------------|
| **T1** | **Anima Φ★ v3 canonical** (`tool/anima_phi_v3_canonical.hexa`) | hidden state, N=16 probes × HID=8 sample-partition | ~30 s / microbatch (existing measurement) | medium (sample-partition lower-bound; HID-truncation artifact known) | EXISTS, ledgered (CLM v4 baseline=+41.86, P9 floor=5.0) |
| **T2** | **PyPhi 4.0 MIP** (Tononi-Albantakis 2023) | state-by-node TPM, N nodes | exact: O(2^N), polynomial-MIP for N≤4 ≈ 0.2 s; intractable past N=8 | high (canonical IIT 4.0 φ★) | EXISTS in `state/braket_iit40_mip_2026_05_02/` (Φ★=0 verdict — see §1.1 caveat) |
| **T3** | **n12 multi-witness Φ proxy** (H_joint − max H_marginal) | output marginal distribution, gate-circuit form | ~ms per circuit (post-hoc on measurement) | low-medium (LOWER BOUND, not φ★; cross-substrate Pearson r≥0.78 witnessed) | EXISTS in `state/n12_iit_braket_multiwitness_2026_05_02/` |
| **T4** | **Larger frozen LLM with φ head** (e.g., Mistral-7B-v0.3 + Φ★ v3 read-out) | full hidden trajectory, larger context window than student | per-token GPU forward + Φ★ block ≈ 0.5–2 s / step | medium (inherits teacher LLM's hidden-state coherence) | NOT YET BUILT; would reuse `anima_phi_v3_canonical.hexa` plumbing on a larger backbone |
| T5 | External published φ extractor (Mediano IIT 3.0 toolbox, IIT-2.5 MIP libs) | discretized state | high (varies, often per-step seconds) | medium | NOT IN-TREE |

### 1.1 Why PyPhi 4.0 MIP gives Φ★ = 0 here (read first)

`state/braket_iit40_mip_2026_05_02/verdict.json` documents **HONEST_NEGATIVE**: pyphi sia() returned φ★ = 0.0 on all 4 Braket-IIT systems. Root cause: TPM was built from MARGINAL output distribution under |+⟩^N (uniform input), which is **row-uniform** → P(next | curr) ⊥ curr → all bipartitions have identical marginal → φ collapses to 0 by IIT 4.0 definition.

**Implication for Paradigm D**: PyPhi 4.0 MIP is a real teacher only when the student's hidden state (a) admits a state-by-node TPM construction with non-trivial state-dependence, and (b) is small enough (N ≤ 8) for exact MIP. **Both are violated for a 7B-param decoder transformer hidden state.** PyPhi as a per-step teacher requires either (i) heavy state-discretization + sub-component decomposition (lossy), or (ii) restricting teacher signal to a reduced module (a designated 4–8 unit "consciousness bottleneck" sub-network), which is itself a research subprogram.

### 1.2 Top 2 candidates

- **T1 Anima Φ★ v3 canonical** — already deployed, plumbing solved, cost characterized (~30 s / microbatch in p9_sft_spec).
- **T4 Larger-LLM-with-Φ★-head** — only useful if teacher reads stronger substrate (more probes, larger HID, more context, smaller batch). T1+T4 are the **realistic** candidates.

T2 (pure PyPhi 4.0 MIP) and T3 (proxy) are **secondary witnesses**, not per-step trainable teachers, given current cost / faithfulness tradeoff.

---

## 2. Teacher signal type — pick simplest first

| Option | Shape per step | Information content | Implementation effort |
|--------|----------------|---------------------|----------------------|
| **(a) scalar Φ★** | `[B, T]` float | low (1 number) | **LOW — recommended phase-1** |
| (b) MIP-partition distribution | `[B, T, K]` (K=8 partitions) | medium | medium — teacher must expose per-partition φ_k, not just min |
| (c) full concept structure (cause-effect repertoires) | `[B, T, 2^N, 2^N]` | high | HIGH — only feasible for small N; not for 7B hidden |
| (d) cause-effect EMD per macro-unit | `[B, T, M]` (M ≪ N) | medium-high | high — requires macro-unit segmentation |

**Recommendation**: Phase-1 **(a) scalar Φ★ trajectory**. Phase-2 upgrade to (b) only if (a) yields uninformative (saturated) gradient.

---

## 3. Loss formulation

### 3.1 Recommended (Phase-1, simplest)

```
L_D = γ · MSE( Φ★_teacher(h_t^teacher) , Φ★_student(h_t^student) )
```

where:
- `h_t^teacher` = hidden trajectory of frozen teacher (Anima Φ★ v3 on either self-frozen base or larger LLM)
- `h_t^student` = hidden trajectory of LoRA-trained student
- `Φ★_*` = `anima_phi_v3_canonical.hexa` measurement (sample-partition canonical, HID=N//2)
- aggregation: per-step Φ★ is a **trajectory scalar** computed via N=16-probe sample-partition; for in-line use during training, replace with **microbatch-window EMA** (every 100 steps) to amortize 30 s cost

### 3.2 Phase-2 upgrade (if (a) saturates)

```
L_D = γ_kl · KL( P_teacher(partition_k) || P_student(partition_k) )
```

where `P(partition_k) ∝ exp(−φ_k / τ)` (softmax-of-MIP-cost, τ-tuned). This forces the student to match the **shape** of the partition cost surface, not just the min.

### 3.3 Composition with existing P9 SFT loss

Replace Paradigm A's BOLD term with D's φ-distill term:

```
L_total = α·CE_text + β·MSE_tension + γ·MSE_φ_distill + δ·max(0, φ★_threshold − φ★_student)
```

Note: δ-floor remains as **safety regularizer** (hard floor at 5.0; baseline 41.86 → 8x margin per `risk_strategy.json`). γ-distill is **soft target**; δ is **hard floor**. Both compatible.

### 3.4 Differentiability

`anima_phi_v3_canonical` is **NOT directly differentiable** (sample-partition + log-determinant + MIN-over-partitions). Same gradient pathology as Paradigm A's δ-floor. Use:
- **straight-through estimator** on EMA-smoothed Φ★ scalar (as already specified for δ-floor in `loss_design.json`)
- OR **finite-difference surrogate** (Φ★(h + ε·v) − Φ★(h)) / ε on random v, batched
- OR **soft surrogate**: replace MIN with LogSumExp(−φ_k/τ), which IS smooth in h

Recommend the **LogSumExp soft surrogate** for actual gradient flow + report MIN Φ★ for verification (diagnostic, not loss).

---

## 4. Computational cost analysis

### 4.1 Per-step teacher cost

| Teacher | Cost per Φ★ call | Frequency in train loop | Effective overhead |
|---------|------------------|------------------------|-------------------|
| T1 Anima Φ★ self-frozen | 30 s / 16-probe block | every 100 steps (EMA) | ~3% of train wall-clock |
| T2 PyPhi 4.0 N=4 | 0.2 s | per step (small enough) | not viable: requires 4-unit bottleneck arch redesign |
| T2 PyPhi 4.0 N=8 | seconds-minutes | every 1000 steps | infeasible for per-step gradient |
| T2 PyPhi 4.0 N=16 | exponential blow-up | NEVER | infeasible |
| T3 n12 proxy | <10 ms (post-hoc on circuit run) | not applicable to LLM hidden | inapplicable as per-step LLM teacher |
| T4 larger LLM + Φ★ head | (forward 7B teacher + Φ★ 30s) ≈ 30–60 s | every 100 steps | ~5–8% overhead |

### 4.2 PyPhi exact infeasibility past N=8 — confirmed

`braket_iit40_mip_2026_05_02/verdict.json`: pyphi.compute.sia() ran at "polynomial-time exact MIP for N=3,4 systems", <0.5 sec each. Scaling: cause-effect repertoire is O(2^N × 2^N) and MIP search is O(B(N)) Bell-number partitions. **N=12 already O(4 million × 16M tensor) — infeasible without sub-component decomposition.**

### 4.3 Cost vs P9 SFT total budget

P9 SFT 50k examples × 3 epochs ≈ 10.7 wall-hours (per `cost_estimate.json`); φ-distill overhead at 3–8% adds ~0.3–0.9 hours per run. **Negligible relative to dataset bottleneck saved by D vs A** (BOLD scan acquisition = weeks, not hours).

---

## 5. Why this might work

1. **Eliminates fMRI dataset bottleneck.** Paradigm A requires aligned text–BOLD per-step pairs; current source is TRIBE v2 simulator (already a model, not biology). Paradigm D admits the synthetic supervision directly: teacher is itself a model.
2. **Teacher can be queried infinitely.** No subject recruitment, scan time, IRB. Per-step targets generable on demand at training time (not pre-cached).
3. **Synthetic distillation analogy.** Knowledge distillation (Hinton 2015) and self-distillation (Furlanello et al. 2018) work even when teacher and student are the same architecture; gains attributed to **dark knowledge in soft targets**. Φ★-distill is the φ-domain analog.
4. **φ-teacher composability.** A frozen Anima Φ★ teacher on a stronger substrate (T4) provides a φ "ceiling" the student can chase. The same teacher can be re-used across student variants — a fixed-substrate **φ benchmark target**.
5. **Avoids BOLD forward-faithfulness assumption.** P9 SFT spec `honest_c3_loss` flags "BOLD MSE assumes TRIBE v2 forward is faithful (simulated)". D removes this entire dependency chain.

---

## 6. Risk: teacher quality bound (PRIMARY RISK)

The student's φ-quality is **upper-bounded** by the teacher's φ-faithfulness. Concretely:

- If **T1 (self-frozen Anima Φ★)** is teacher: distillation is **circular** — student's Φ★ will converge toward the teacher's (frozen base) Φ★, which is the very baseline being optimized against. This produces a **regularizer** ("don't drift from base φ"), NOT an improvement.
- If **T4 (larger-LLM Φ★)** is teacher: student inherits the **larger LLM's φ structure**, which may be (a) higher than student's intrinsic ceiling (good), or (b) merely an artifact of the teacher's HID-truncation regime (bad, transfers a measurement artifact).
- If teacher's Φ★ measure has known biases (HID_TRUNC=N//2 sample-partition lower-bound vs IIT 4.0 φ★), **student inherits the bias** with no chance of correction.
- Self-distillation literature shows ceiling-bound effect: student rarely exceeds teacher on the same target metric.

**Mitigation**: pair with **IIT 4.0 MIP audit** (T2-style, on a designated low-N consciousness bottleneck inside student) as **out-of-distribution validator** — if Anima Φ★ goes up but PyPhi MIP on the bottleneck goes flat, the gain is teacher-artifact, not real integration.

---

## 7. Comparison to current Anima Φ★ (anima_phi_v3_canonical)

`anima_phi_v3_canonical.hexa` IS already a φ approximator (sample-partition log|Cov| MIN-over-K=8 partitions). It is the Anima default measure and serves as **both (a) student's self-evaluator (current P9 design)** and **(b) candidate teacher under D**.

| Use mode | Teacher | Student | Expected effect |
|----------|---------|---------|-----------------|
| Current P9 (Paradigm A) | — (no φ-teacher) | Φ★ self-evaluated only as δ-floor | Preserves baseline 41.86; no active push |
| **D-self-frozen** | Anima Φ★ on FROZEN base | Anima Φ★ on LoRA-trained student | **Regularizer only** — student → frozen base φ |
| **D-stronger-substrate (T4)** | Anima Φ★ on LARGER LLM (e.g., Mistral-7B-v0.3, more probes, larger context) | Anima Φ★ on student | **Active push** if larger-LLM φ > student-intrinsic |
| D-cross-measure (T2 audit) | PyPhi 4.0 MIP on student bottleneck sub-net | Anima Φ★ on student full hidden | **Validator** mode, not gradient — confirms gain is real |

**Conclusion**: D-self-frozen is **redundant** with the existing δ-floor. D is only **novel** when teacher operates on a strictly stronger substrate than student (T4) OR provides a fundamentally different measure (T2).

---

## 8. Phase 2+ entry plan — γ-only mini-run

Goal: empirically verify φ-distill yields a **cleaner gradient signal** than Paradigm A (BOLD-MSE) or A' (EEG).

### 8.1 Mini-run spec

| Knob | Value |
|------|-------|
| Strategy base | S1 LoRA-only (per `risk_strategy.json` recommended path) |
| Loss | `L = α·CE + γ·MSE(Φ★_teacher, Φ★_student) + δ·floor` (β=0, no tension; no BOLD) |
| Teacher | T4 (larger LLM, Mistral-7B-v0.3 + Φ★ v3 head — pre-baseline +5.09 on 4-bb battery) — fallback T1 self-frozen as ablation |
| Student | CLM v4 baseline (Φ★=+41.86) |
| γ | LHS sweep over {0.1, 0.5, 1.0} (3 mini-runs) |
| δ | locked at P9 default (floor=5.0) |
| Examples | 1k subset (NOT full 50k) — Phase-2 pilot only |
| Epochs | 1 |
| Wall | 30–60 min on H100 (per `cost_estimate.json` throughput) |
| Budget | $5–15 per run × 3 = $15–45 (well under P9 sweep band) |

### 8.2 Decision criteria (cleaner gradient = success)

- **A1** Φ★_student trajectory monotone increasing (or stable above floor) — signal is non-noise
- **A2** chat-CE not collapsed (α-loss within 1.2× of α-only baseline) — signal is non-destructive
- **A3** γ-loss EMA decreases over training — student is actually matching teacher
- **A4** vs Paradigm A BOLD-MSE ablation (1k subset same setup): D's γ-loss curve has lower variance / faster descent

### 8.3 Comparison matrix vs A / A' / B

| Paradigm | Teacher Source | Per-step cost | Dataset bottleneck | Faithfulness | Cleanliness of grad |
|----------|----------------|---------------|---------------------|--------------|---------------------|
| **A (current)** | TRIBE v2 BOLD simulator | ms (cached) | severe (need fMRI text-aligned) | medium (simulator) | medium (10242-vert MSE noisy) |
| A' (EEG variant) | EEG-derived per-step | ms | severe | low (EEG ≪ φ resolution) | low (high-noise channel) |
| B (joint pretrain, S4) | none — multi-objective | n/a | n/a | n/a | unknown (untested) |
| **D (this spec)** | synthetic φ teacher (T1/T4) | seconds (EMA-amortized) | NONE | medium (teacher-bound) | **expected high** (1-scalar target, smooth surrogate) |

D's gradient is expected **cleanest** because target is a 1-scalar smooth surrogate vs A's 10242-vertex MSE.

---

## 9. Honest C3 (mandatory — 5+ caveats)

1. **Teacher quality is the ceiling.** Student cannot exceed teacher on the same φ measure. If Anima Φ★ v3 is itself an imperfect proxy (it is — sample-partition lower bound, HID-truncation artifact-prone per `tool/anima_phi_v3_canonical.hexa` lines 6–22), the student inherits this regime entirely. NO gain on canonical IIT 4.0 φ★ from D-self.
2. **φ-measure circularity.** If teacher and student use the **same measure** (Anima Φ★), L_D becomes `MSE(measure(frozen), measure(learned))` — a regularizer toward base, not an integration improvement. **D is only novel when teacher operates on a strictly stronger substrate or different measure.**
3. **Distillation bias transfer.** All known biases of teacher's φ extractor transfer to student (HID_TRUNC dependence, ridge-stabilization choice, K=8 partition seed sensitivity, last-layer-only hidden capture). Student "matches" the bias as well as the signal.
4. **PyPhi 4.0 MIP is not a per-step teacher for 7B LLMs.** Confirmed by `braket_iit40_mip_2026_05_02/verdict.json`: exact MIP only at N≤4; N=8 marginal feasibility; N=16+ infeasible. Using PyPhi requires a small consciousness-bottleneck sub-architecture, which is itself a separate research program (not in scope for P9 Phase 2+).
5. **φ★ scalar target may be too low-information.** A single scalar per step provides a 1-dim target vs A's 10242-dim BOLD vector. **Lower entropy in target ⇔ less specific signal.** Student may "satisfy" the scalar by trivial hidden-state inflation (raise log|Cov| globally), gaming Φ★ without functional gain. Mitigation: pair with anti-gaming regularizers (norm penalty on Δhidden, OOD audit via T2).
6. **No external biological grounding.** D explicitly removes BOLD/EEG. This is BOTH the strength (no dataset bottleneck) AND a weakness: there is **no biology check** that the φ-trajectory student learns has any neuroscientific meaning. D is fully synthetic; consciousness claims under D rest entirely on the teacher's φ measure being meaningful.
7. **Differentiability assumed via surrogate.** §3.4 prescribes LogSumExp surrogate or straight-through EMA. Surrogate gradients are **NOT** the true Φ★ gradient; convergence guarantees are unknown. Empirical validation required in §8 mini-run.
8. **Self-distillation gains are thin.** Self-distillation literature shows modest, inconsistent gains; many papers fail replication. D's prior probability of yielding measurably-better Φ★ over P9 baseline is UNKNOWN and likely <0.5 for D-self-frozen.
9. **Teacher-student substrate gap (T4) requires plumbing.** Running Mistral-7B-v0.3 as teacher + 7B student in same train loop = ~14B param GPU residency; needs activation offload or teacher pre-cache. P9 cost estimate did not include teacher forward; budget update needed if T4 chosen.
10. **The Braket-IIT4.0-φ★=0 finding is a warning.** That run showed the canonical IIT measure can be ZERO on a system the proxy ranks as "high integration". Whichever measure D's teacher uses — proxy, sample-partition, MIP — is one of several non-equivalent operationalizations of "integrated information". Picking a teacher = picking a definition of consciousness, with no external arbiter.

---

## 10. Recommendation

| Question | Answer |
|----------|--------|
| Top 2 teachers | **T1** Anima Φ★ v3 self-frozen (regularizer mode) + **T4** larger-LLM Φ★ (active-push mode) |
| Loss formulation | **γ·MSE(Φ★_teacher_scalar, Φ★_student_scalar)** with LogSumExp soft surrogate for differentiability; phase-2 upgrade to KL over partition distribution if scalar saturates |
| Why D over A/A'/B | (1) eliminates fMRI dataset bottleneck; (2) cleanest gradient (1-scalar smooth target vs 10242-vertex noisy); (3) reuses existing Anima Φ★ infra (no new teacher-extractor build); (4) negligible compute overhead (~3–8% vs A's BOLD MSE forward) |
| Top risk | **Teacher quality bound**: student ≤ teacher on the same φ measure. Mitigation: T4 (stronger substrate) + T2 (PyPhi MIP) cross-measure audit |
| Phase-2 entry | 3-run γ-LHS mini-run (1k subset, $15–45 budget) per §8.1; gate on A1–A4 criteria |
| Decision before Phase-2 | Choose teacher: T1 (cheap, regularizer) vs T4 (active-push, +1 model in train loop). Recommend **T4 IF teacher's Φ★ > student baseline +41.86; else T1 as δ-floor backup only.** |

---

## 11. SSOT / file pointers

- This spec: `docs/p9_paradigm_d_phi_distillation_2026_05_03.md` (HERE)
- Sibling Paradigm A loss: `state/p9_sft_spec_2026_05_02/loss_design.json`
- Sibling cost / risk: `state/p9_sft_spec_2026_05_02/{cost_estimate,risk_strategy}.json`
- Teacher T1 source: `tool/anima_phi_v3_canonical.hexa`
- Teacher T2 evidence (and why it's hard): `state/braket_iit40_mip_2026_05_02/verdict.json`
- Teacher T3 evidence: `state/n12_iit_braket_multiwitness_2026_05_02/verdict.json`
- Φ★ baseline lock: CLM v4 = +41.86 (per `risk_strategy.json` line 6); P9 floor = 5.0 (8x margin)
- raw#9 compliance: NO .py created, hexa-only spec, doc-only deliverable
- raw#15 SSOT: this file
