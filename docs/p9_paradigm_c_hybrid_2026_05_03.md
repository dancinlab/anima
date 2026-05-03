# P9 Paradigm C — Hybrid (BOLD + EEG + φ★ Floor) Multi-Target Integration Learning

- **Spec ID**: `p9_paradigm_c_hybrid_2026_05_03`
- **TS (UTC)**: 2026-05-03
- **Author**: G5 (spec-only)
- **Phase**: spec_only — `exec_authorized: false`
- **Substrate refs (READ ONLY)**:
  - `state/p9_sft_spec_2026_05_02/loss_design.json` (4-term L baseline)
  - `state/p9_sft_spec_2026_05_02/falsifiers_preregistered.json` (F1–F4 v2)
  - `state/p9_sft_spec_2026_05_02/risk_strategy.json` (φ★ L1–L5 mitigation)
  - `state/p9_sft_spec_2026_05_02/hyperparameter_grid.json` (LHS-9 over 4D)
  - `state/p9_sft_spec_2026_05_02/cost_estimate.json` (S1–S4 USD bands)
- **Cross-refs (forward, may not yet exist at write time)**:
  - `docs/p9_paradigm_a_simulated_bold_2026_05_03.md` — γ_BOLD source via TRIBE v2 forward (simulated 10242-vertex fsaverage5).
  - `docs/p9_paradigm_a_prime_measured_bold_2026_05_03.md` — γ_BOLD source via measured fMRI (HCP / NSD).
  - `docs/p9_paradigm_b_eeg_phi_proxy_2026_05_03.md` — γ_EEG source via EEG φ-band proxy (PLV / wPLI features).
- **Constraints (HEXA / raw#9 / raw#91)**:
  - HEXA-only: no `.py` creation.
  - Doc-only write surface: `docs/p9_paradigm_c_hybrid_2026_05_03.md`.
  - Honest C3 mandatory (≥5 caveats; see §8).

---

## 0. Scope & Stance

Paradigm C does **not** replace A / A' / B; it composes them. Each single-target paradigm
carries one structural risk:

| Paradigm | Signal              | Primary risk                                                  |
|----------|---------------------|---------------------------------------------------------------|
| A        | simulated BOLD      | TRIBE v2 forward circularity (target ≈ what model predicts)   |
| A'       | measured BOLD       | tiny N (HCP ≤ 1k subjects), distribution shift vs chat corpus |
| B        | EEG φ-band proxy    | source-leakage; φ-proxy ≠ φ★ (different operationalisations)  |
| φ★ floor | hard-floor `δ·max(0, τ−φ★)` | non-differentiable (straight-through EMA only)         |

**Hybrid C hypothesis**: if no single signal is trustworthy, redundancy across signals + a
hard floor improves robustness *if* gradients do not destructively interfere.

This spec inherits the LoRA-only base (S1/S3 lineage) and the bf16 / H100-80GB / ZeRO-2
host envelope from `architecture.json`. **Nothing about CLM v4 530M, LoRA r=64 α=128, lr=1e-4,
epoch=3 is changed.** Only the loss surface and the staged-entry curriculum change.

---

## 1. Loss Formulation (5-Term)

### 1.1 Equation

```
L_total = α · CE(y_text_hat,    y_text_target)                           # L_chat
        + β · MSE(tension_hat,  tension_target)                          # L_tension
        + γ_BOLD · MSE(bold_hat, bold_target)                            # L_bold      (Paradigm A or A')
        + γ_EEG  · MSE(eeg_hat,  eeg_target)                             # L_eeg       (Paradigm B)
        + δ      · max(0, τ_phi − φ★_EMA(model))                         # L_phi_floor (existing)
```

### 1.2 Term-by-Term Spec

| Term         | Symbol  | Shape           | Source / projector                              | Eval cadence       | Diff?               |
|--------------|---------|-----------------|-------------------------------------------------|--------------------|---------------------|
| L_chat       | α       | scalar          | next-token CE on assistant tokens               | every step         | yes                 |
| L_tension    | β       | `[B,T]`         | mind.tension extractor (CLM v4 trajectory)      | every step         | yes                 |
| L_bold       | γ_BOLD  | `[B,T,10242]`   | TRIBE v2 forward (A) **or** measured fMRI (A') | every step         | yes                 |
| L_eeg        | γ_EEG   | `[B,T,C_eeg]`   | EEG φ-band PLV/wPLI (B); C_eeg ∈ {32, 64, 128} | every step         | yes                 |
| L_phi_floor  | δ       | scalar          | anima_phi_v3_canonical (HID=8 well-conditioned) | every 100 steps; STE on EMA | proxy gradient |

**τ_phi = 5.0** (locked; matches L3 mitigation in `risk_strategy.json`).
**φ★ baseline = 41.86** (L1 lock; CLM v4 530M G3 PASS-positive).

### 1.3 Reductions & Channels

- L_bold reduction: mean over fsaverage5 vertices, then mean over `[B,T]`.
- L_eeg reduction: mean over EEG channels (PLV scalar per channel pair *or* per-channel φ-band power), then mean over `[B,T]`.
- L_eeg target sourcing assumes **subject-paired EEG-while-reading** corpus (e.g., ZuCo, Brennan-Hale). If unavailable for the chat distribution, cross-paradigm alignment uses Paradigm B's distillation step (read its spec for details). C does **not** invent EEG data.

### 1.4 Compatibility with Phase 1 (existing 4-term)

Phase 1 = `(α, β, γ, δ)`. Phase C is `(α, β, γ_BOLD, γ_EEG, δ)`. Setting `γ_EEG = 0`
recovers Phase 1's loss exactly when γ_BOLD := γ. This means the existing 9-LHS sweep results
remain interpretable as a **γ_EEG = 0 slice** of the 5-D space — no recomputation wasted.

---

## 2. Weight Balancing Strategy

### 2.1 The dominance problem

CE is `O(log V) ≈ ln(50257) ≈ 10.8` at init; tension MSE is `O(0.1–1)`; BOLD MSE on 10242
vertices is `O(1)` per vertex but variance per vertex is `~10⁻³`; EEG PLV `[0,1]` MSE is
`~10⁻²`. Naively setting `γ_BOLD = γ_EEG = 0.3` (Phase 1 default) means **EEG term is
~30× weaker than tension and ~100× weaker than CE in raw gradient norm** — we'd be
pretending to learn EEG while actually only fitting CE.

### 2.2 Auto-scaling (PROPOSED, default for Paradigm C)

Compute per-step expected magnitude `E_k = ⟨L_k⟩` over a 200-step warmup with all γ_k=0
except CE. Then set:

```
γ_k_eff = γ_k_target · (E_CE / E_k)
```

so that each term's *initial* gradient norm contribution equals `γ_k_target · E_CE`. The
sweep then operates on `γ_k_target ∈ [0.1, 0.3, 0.5]` interpretable as "fraction of CE
gradient norm" — comparable across signals.

This is **GradNorm-lite** (Chen et al. 2018, simplified to one-shot warmup calibration; not
per-step adaptive — see §6 risk on adaptive instability).

### 2.3 LHS sweep over `(γ_BOLD_target, γ_EEG_target, δ)`

α and β are **fixed** at the Phase 1.5 best combo (presumed `lhs7` or successor; selection
deferred to Phase 1 closure). The 3-D sweep:

```
γ_BOLD_target ∈ {0.1, 0.3, 0.5}
γ_EEG_target  ∈ {0.1, 0.3, 0.5}
δ             ∈ {0.5, 1.0, 2.0}
full = 27, LHS-sampled = 9
```

LHS samples (deterministic seed=20260503):

| id    | γ_BOLD_target | γ_EEG_target | δ   |
|-------|---------------|--------------|-----|
| c1    | 0.1           | 0.5          | 1.0 |
| c2    | 0.5           | 0.1          | 0.5 |
| c3    | 0.3           | 0.3          | 2.0 |
| c4    | 0.1           | 0.1          | 1.0 |
| c5    | 0.5           | 0.5          | 2.0 |
| c6    | 0.3           | 0.5          | 0.5 |
| c7    | 0.5           | 0.3          | 1.0 |
| c8    | 0.1           | 0.3          | 2.0 |
| c9    | 0.3           | 0.1          | 0.5 |

### 2.4 Sequential activation (RECOMMENDED — Phase 2.A → 2.B → 2.C)

Auto-scaling + LHS gives a static plan. Sequential activation reduces blast radius:

- **Phase 2.A**: γ_EEG = 0; sweep `(γ_BOLD_target, δ)` only — 1 axis added vs Phase 1.
- **Phase 2.B**: lock best Phase 2.A `(γ_BOLD_target, δ)`; sweep `γ_EEG_target` alone.
- **Phase 2.C**: full 3-D Pareto on 8-pod DDP using Phase 2.A/B priors as warm-start.

Sequential is preferred because it lets us **detect F4 lift from γ_BOLD alone before
pouring γ_EEG on top** — diagnostics stay attributable.

---

## 3. Curriculum Design (γ_k Ramp)

Phase 1 ramped δ from `0 → δ_target` over the first 500 steps to let the model find a
basin before being floor-constrained. Question: should γ_BOLD / γ_EEG ramp similarly, or
stay constant?

**Decision: ramp γ_BOLD and γ_EEG using a 1000-step linear warmup.** Rationale:

1. **Convergence-of-anchors risk**: if BOLD/EEG MSE dominates from step 0, the LM head
   never gets a chance to specialise on chat text — gradients pull representations
   toward neuroimaging targets before chat coherence forms.
2. **Symmetric to δ**: δ already ramped; making γ_BOLD / γ_EEG also ramped keeps Phase 1
   chat-formation dynamics intact.
3. **Cost**: ramp is free (a scalar multiplier on already-computed losses).

Schedule:

```
γ_k(step) = γ_k_target · min(1, step / 1000)        for k ∈ {BOLD, EEG, δ}
α(step), β(step) = constant from step 0
```

α and β stay constant because chat CE and tension are the **anchor objectives** — they
must be live from step 0 to define the basin into which BOLD/EEG/φ refinement flows.

---

## 4. Computational Cost (1×H100-80GB, bf16, LoRA r=64)

### 4.1 Per-step time accounting

Phase 1 baseline (4-term L, no BOLD/EEG forward at train time because target is precomputed):
- Forward+backward CLM v4 530M with `seq=2048, micro_batch=4`: **~250 ms/step** (8000 tok/s × micro_batch=4 × seq=2048 / batch ≈ 1.0s for grad_accum=8 step; ~125ms per microbatch, 250ms with bwd).

Add Paradigm C terms:

| Component            | Per-step cost   | Notes                                                          |
|----------------------|-----------------|----------------------------------------------------------------|
| BOLD target lookup   | ~5 ms           | precomputed `[B,T,10242]` stored in shared mem; just MSE       |
| BOLD MSE             | ~3 ms           | 10242 vertices, fused kernel                                   |
| EEG target lookup    | ~2 ms           | `[B,T,128]` — small                                            |
| EEG MSE              | ~1 ms           | 128 channels                                                   |
| φ★ verifier          | ~30 s / 100 steps = **300 ms amortised**, EMA-smoothed (existing) |

**Total: ~250 ms (CLM) + 11 ms (BOLD+EEG MSE) + 3 ms amortised (φ★ amortised at every-100) = ~265 ms/step.**

Net **~6% slower** than Phase 1 — negligible.

### 4.2 Wall-time projection

Phase 1: 50k examples × 3 epochs × 2048 tokens / 8000 tok/s ≈ 38400 s = **10.7 h** per run.
Paradigm C: ×1.06 ≈ **11.3 h** per run.

LHS-9 = **~102 wall-hours = ~$255 spot ($382 on-demand)** for Phase 2.C.
Phase 2.A (sentinel, 1-pod, partial sweep ~3 combos) ≈ **~34 h ≈ $85**.
Phase 2.B (3 γ_EEG combos × 1-pod) ≈ **~34 h ≈ $85**.

**Total Phase 2.A+B+C: ~$425–650 spot, $640–975 on-demand.** Well inside the
S3 band ($1500–3000).

### 4.3 Memory

- LoRA weights: ~50 MB (unchanged).
- BOLD target tensor `[B=4, T=2048, 10242]` ≈ 4 × 2048 × 10242 × 2 (bf16) ≈ **170 MB / microbatch**.
- EEG target tensor `[B=4, T=2048, 128]` ≈ **2 MB / microbatch**.
- φ★ verifier state: bounded (~500 MB).

H100-80GB headroom is comfortable: model + activations + LoRA grads ≈ 35 GB; targets +
verifier ≈ 1 GB. **No memory blocker.**

---

## 5. F-Falsifier Integration

Paradigm C inherits F1–F4 from `falsifiers_preregistered.json` v2 — **no metric definitions
changed** (preregistration lock honoured). What changes is the *expected trajectory* of
each falsifier under the hybrid loss:

### 5.1 F1 (BLEU-1 ≥ 0.132 = 0.85 × Llama anchor)

- **Risk**: more loss terms compete with α·CE → BLEU may drop vs Phase 1.
- **Mitigation**: α stays at Phase 1 best; γ_k auto-scaled so initial gradient norm of
  each non-CE term ≤ γ_k_target × CE gradient norm. With γ_k_target ≤ 0.5, each term's
  pull is ≤ half of CE.
- **Diagnostic**: track BLEU-1 every 1000 steps; abort combo if BLEU-1 trend regresses
  > 30 % vs γ_BOLD = γ_EEG = 0 control at same step.

### 5.2 F2 (φ★ ≥ 5.0)

- **Hypothesis (key Paradigm C claim)**: γ_BOLD positive supervision reduces reliance on
  the δ floor because the BOLD signal *itself* is integration-correlated. If true,
  optimal δ in Phase 2.C may be **lower** than Phase 1's lhs7 best.
- **Test**: fit `δ_optimal = f(γ_BOLD_target)` across LHS-9 results. Negative slope
  confirms hypothesis; flat slope means δ floor is still the load-bearing protector.
- **Conservative default**: keep δ ∈ [0.5, 2.0] sweep range — do **not** drop δ below 0.5
  in Phase 2 even if hypothesis confirmed. Validation needs Phase 3 to weaken floor.

### 5.3 F3 (tension MSE < 0.1)

- **Risk (multi-task interference)**: if BOLD and EEG gradients pull representation away
  from tension trajectory, F3 regresses.
- **Mitigation**: gradient cosine-similarity monitor (§6) on `(∇L_tension, ∇L_BOLD)`
  and `(∇L_tension, ∇L_EEG)`. If cosine < −0.3 sustained over 500 steps, abort combo.

### 5.4 F4 (BOLD Pearson r > 0.5)

- **Expectation**: direct BOLD supervision should *significantly improve* F4 vs Phase 1
  (where γ was a single weak signal in a 4-term mix). Target: F4 r ≥ 0.6 in Phase 2.C
  best combo.
- **Caveat**: F4 measures BOLD reconstruction on TRIBE-paired val; if Paradigm A' (measured
  fMRI) is the γ_BOLD source, F4 must be redefined on the measured-fMRI val split (with
  preregistration audit-trail update — this is allowed since v2 already established
  precedent for ratio-based recalibration).

### 5.5 New F5 candidate (NOT preregistered — Phase 3 only)

Optional: **F5 EEG consistency** (per-channel Pearson r > 0.3 between predicted and target
EEG). NOT promoted to F1–F4 set during Phase 2 — see §8 honest C3 on EEG ground truth.

---

## 6. Risk: Gradient Interference

### 6.1 The fundamental concern

5 loss terms with independent targets can be **mutually antagonistic in the LoRA tangent
space**. If `cos(∇L_a, ∇L_b) < 0` consistently, optimisation oscillates and effective
learning rate collapses. Chen et al. 2018 (GradNorm) and Yu et al. 2020 (PCGrad) document
this exact pathology in multi-task NLP/CV settings.

### 6.2 Diagnostic protocol

Every 200 steps, compute the **6×6 gradient cosine-similarity matrix** between term pairs
in `{L_chat, L_tension, L_BOLD, L_EEG, L_phi_floor}` (the floor's STE gradient counts).
Log to `state/p9_paradigm_c_gradient_health/cos_sim.jsonl`.

Abort triggers (per combo):

| Pair                     | Trigger                                         | Action                  |
|--------------------------|-------------------------------------------------|-------------------------|
| (L_chat, L_BOLD)         | cos < −0.5 sustained 500 steps                  | reduce γ_BOLD by 0.5×   |
| (L_chat, L_EEG)          | cos < −0.5 sustained 500 steps                  | reduce γ_EEG by 0.5×    |
| (L_BOLD, L_EEG)          | cos < −0.7 sustained 500 steps                  | drop one signal; abort  |
| (L_tension, L_BOLD/EEG)  | cos < −0.3 sustained 500 steps                  | F3 risk; abort combo    |
| (L_phi_floor, any)       | floor's STE gradient anti-aligned with all      | re-tune τ_phi ramp      |

### 6.3 Mitigations beyond cosine-watch

- **PCGrad** (project conflicting gradients onto the orthogonal complement) — adds
  ~5% step cost; defer to Phase 2.C if cosine monitor flags >2 combos.
- **GradNorm adaptive** (per-step rescale of γ_k to equalise gradient norms) —
  **NOT recommended for Phase 2** because it interacts unpredictably with LoRA and the
  φ★ floor's STE gradient. Static auto-scale (§2.2) is the safer first step.

### 6.4 Why this is the top risk

Paradigm A alone has 4 terms (Phase 1 baseline) and Phase 1 lhs runs already showed
modest tension/BOLD trade-offs in early sentinels. Adding γ_EEG at non-trivial weight
**compounds the interaction surface from 6 pair to 10 pair**, with EEG being the least
calibrated signal. **Top risk: γ_EEG anti-aligns with α·CE because EEG temporal dynamics
(ms-scale) mismatch chat-token semantics (~100ms/token); the model gets stuck balancing
incompatible objectives.**

---

## 7. Phase 2 Staged Entry Plan

### 7.1 Phase 2.A — γ_BOLD only (Week 1)

- **Setup**: 1-pod sentinel (H100-80GB, RunPod spot), LoRA r=64.
- **Loss**: `α·CE + β·tension + γ_BOLD·MSE_BOLD + δ·floor` (γ_EEG = 0).
- **Sweep**: 3 combos `γ_BOLD_target ∈ {0.1, 0.3, 0.5}`, δ locked at Phase 1 best.
- **Gates**: F2 PASS (φ★ ≥ 5.0) AND F4 PASS (r > 0.5) on at least 1 of 3 combos.
- **Cost**: ~$100, wall ~3 days.
- **Decision**: go/no-go to Phase 2.B based on F2+F4. F1 (BLEU) regression > 30 % vs Phase 1 = HALT.

### 7.2 Phase 2.B — add γ_EEG (Week 2)

- **Precondition**: Phase 2.A PASSED.
- **Setup**: 1-pod sentinel, lock best Phase 2.A `(γ_BOLD_target, δ)`.
- **Loss**: full 5-term.
- **Sweep**: 3 combos `γ_EEG_target ∈ {0.1, 0.3, 0.5}`.
- **Gates**: F2, F3, F4 hold; cosine-similarity monitor (§6.2) green.
- **Cost**: ~$100, wall ~3 days.
- **Decision**: promote best `(γ_BOLD_target, γ_EEG_target, δ)` triple to Phase 2.C; if
  F3 regresses or cosine red → halt and revert to Phase 2.A best (BOLD-only) for
  Phase 2.C.

### 7.3 Phase 2.C — full Pareto on 8-pod DDP (Week 3)

- **Precondition**: Phase 2.B PASSED (or BOLD-only fallback locked).
- **Setup**: 8× H100-80GB DDP, 9-LHS combos in parallel = 9 pods (close to budget).
- **Loss**: full 5-term with auto-scaled γ_k.
- **Sweep**: LHS-9 from §2.3.
- **Selection**: `M_chat = (BLEU1 + (φ★_post / 41.86)) / 2` subject to F1+F2+F3+F4 PASS,
  same as Phase 1 selection rule.
- **Cost**: ~$300–450, wall ~12 h compute (3 days operational including verifier).

### 7.4 Total timeline & cost

- **Wall**: ~3 weeks (1+1+1).
- **Cost**: $500–650 spot, $750–975 on-demand.
- **Within S3 envelope** ($1500–3000 from `cost_estimate.json`).

---

## 8. Honest C3 (Caveats)

1. **Gradient fighting between 5 terms is the dominant unknown.** No published
   multi-task LoRA result combines 3 neuroimaging signals + chat CE simultaneously. Our
   cosine-similarity monitor + auto-scale is a heuristic, not a guarantee. PCGrad/GradNorm
   adaptive remain Phase 3 contingencies.

2. **Weight calibration via 200-step warmup is itself a heuristic.** Auto-scaled `γ_k_eff`
   reflects only the *initial* gradient regime; as training progresses, term magnitudes
   evolve at different rates. Static rescale may drift; we'd need adaptive rescale to
   stay calibrated, which we explicitly defer.

3. **BOLD and EEG datasets are non-overlapping subjects.** Even paired EEG-fMRI corpora
   (NSD-EEG, EEGfMRI-3T) cover different stimuli than our chat distribution. We are
   **distilling neural-signal structure into a model trained on text it never saw the
   subject read**. Cross-paradigm semantic alignment relies on Paradigm B's projection
   layer assumptions (defer to its spec).

4. **φ★ floor is still load-bearing.** Even if γ_BOLD positive supervision reduces δ
   need (§5.2 hypothesis), φ★ measures an integrated information proxy that BOLD/EEG do
   not directly preserve. BOLD and EEG are *correlates* of brain integration, not the
   information-theoretic quantity itself. We **cannot remove the floor** in Phase 2.

5. **F4 redefinition risk if Paradigm A' (measured fMRI) is the γ_BOLD source.** F4's
   preregistered val split is TRIBE-paired (simulated). If we switch source mid-Phase-2,
   we trigger a falsifier-definition update and an audit-trail entry — schema_history v3.
   This is permitted (cf. v2 BLEU recalibration) but should be planned, not stumbled into.

6. **EEG temporal-scale mismatch.** EEG dynamics live at ms scale; chat-token semantics at
   ~100ms/token. Aligning per-token EEG targets to model hidden states requires either
   downsampling EEG to token rate (information loss) or upsampling tokens to EEG rate
   (compute blowup). Paradigm B should specify; if it punts, Paradigm C inherits a
   blocker.

7. **Sequential activation order is partially-ordered, not total.** We chose
   γ_BOLD → γ_EEG → δ-tune because BOLD has stronger published priors on chat-relevant
   neural correlates than EEG. If Paradigm B's spec lands with an unexpectedly strong
   EEG signal-to-noise claim, the order should flip. Re-evaluate at Phase 2.A close.

8. **Cost band assumes spot pricing & no cold-HF download penalty.** Each fresh H100 cold
   start adds ~$1.50 + 25 min for model + LoRA weights download (per memory note in
   `cost_estimate.json`). LHS-9 at Phase 2.C = 9 cold starts unless we pin a warm pool;
   add $15–20 buffer.

---

## 9. Decision Summary

- **Recommended sequential activation order**: γ_BOLD (Phase 2.A) → γ_EEG (Phase 2.B) → δ-tune (Phase 2.C).
- **Recommended weight calibration**: auto-scale via 200-step warmup, then LHS-9 over `(γ_BOLD_target, γ_EEG_target, δ)` with α and β fixed at Phase 1 best.
- **Recommended curriculum**: 1000-step linear ramp on γ_BOLD, γ_EEG, δ; α and β constant from step 0.
- **Phase 2 timeline**: 3 weeks, ~$500–975 total.
- **Top risk**: gradient interference among 5 terms — especially `(L_chat, L_EEG)` antagonism due to temporal-scale mismatch. Mitigation = cosine-similarity monitor + auto-scale + sequential staging. PCGrad held in reserve for Phase 3.
- **Hard floor**: keep δ ≥ 0.5 in Phase 2 regardless of other gains; φ★ preservation is irreversible-failure-class.

---

## 10. Approvals & Locks

- **Spec authored**: 2026-05-03 by G5.
- **Exec authorisation**: not granted; Phase 2.A entry requires explicit user OK + Phase 1 closure marker.
- **Falsifier preregistration**: F1–F4 v2 inherited unchanged. F5 (EEG consistency) NOT preregistered.
- **HEXA / raw#9 compliance**: no `.py` created; doc-only write.
- **raw#91 honest C3**: 8 caveats logged in §8.
