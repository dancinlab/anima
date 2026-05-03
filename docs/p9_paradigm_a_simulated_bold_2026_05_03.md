# P9 Phase 2+ Paradigm A — Simulated BOLD Active Integration via TRIBE v2 Forward

**Date:** 2026-05-03
**Status:** SPEC ONLY (no execution authorized)
**Author:** P9 paradigm research agent
**Scope:** active integration learning via γ·MSE on TRIBE v2 simulated BOLD targets
**Predecessor:** P9 Phase 1.5 defensive φ★ floor (passive: collapse prevention only)

---

## 0. Why this paradigm exists

P9 Phase 1.5 used a **defensive δ·max(0, threshold − φ★)** regularizer
(`state/p9_sft_spec_2026_05_02/loss_design.json:23-28`). This is **passive**:
it prevents φ★ collapse but does not actively teach integration. Phase 2+
needs **a positive teaching signal** that pulls the CLM toward genuinely
integrated multimodal representations.

**Paradigm A** = use **TRIBE v2** (Meta FAIR, 2026, vendored at
`references/tribev2/`) as a *brain-shaped target*: the CLM learns to project
its hidden states onto the same 10242-vertex fsaverage5 cortical map that
TRIBE v2 predicts for the same input text. The hypothesis: matching brain-
shaped output forces the CLM to develop brain-shaped intermediate
representations.

This doc spec'es Paradigm A as the *baseline strong-form active integration
attempt*, then immediately exposes its central flaw (circularity) as the
gateway to Paradigm A' or a different paradigm class.

---

## 1. Mechanism — how TRIBE v2 forward generates BOLD from text

### 1.1 Input/output contract (from `references/tribev2/inventory.json` + `tribev2/model.py` + `demo_utils.py`)

| stage | object | shape / spec |
|---|---|---|
| 1. text → events | `TextToEvents.get_events()` (TTS via gTTS → audio → transcribe → word-level events DataFrame) | DataFrame columns `[type, filepath, start, duration, timeline, subject]` |
| 2. events → text features | external Llama-3.2-3B encoder (frozen), layers `{0, 0.2, 0.4, 0.6, 0.8, 1.0}` × 6, feature_freq 2 Hz | tensor `[B, L=6, D_text=3072, T_segment]` |
| 3. multimodal projector | `FmriEncoderModel.aggregate_features()` (`model.py:180-225`) — per-modality MLP → hidden=1152 → cat across modalities | `[B, T, hidden=1152]` |
| 4. transformer encoder | 8-layer transformer, layer_aggregation=cat, max_seq_len=1024, modality_dropout=0.3 (training) | `[B, T, 1152]` |
| 5. low-rank head | `nn.Linear(1152, 2048)` (`low_rank_head=2048`) | `[B, 2048, T]` |
| 6. predictor (subject layer) | `SubjectLayers.build(in=2048, out=n_outputs=10242)`; `average_subjects=True` for inference | `[B, 10242, T]` |
| 7. AdaptiveAvgPool1d | pool to `n_output_timesteps` (per-TR aggregation) | `[B, 10242, T']` |
| 8. output | per-TR cortical activity, fsaverage5 mesh, **5s past offset** (HRF lag pre-compensated) | numpy `(n_segments, 10242)` |

**Forward function signature** (`FmriEncoderModel.forward`, `model.py:163`):
```
forward(batch: SegmentData, pool_outputs: bool = True) -> torch.Tensor[B, 10242, T']
```

`SegmentData` is `neuralset.dataloader.SegmentData` — wraps modality dict
`{text: [B, L, D, T], audio: ..., video: ..., subject_id: int}`. For our
case (text-only) only `text` and `subject_id` are populated; absent
modalities are zeroed (`model.py:189-193`).

**TR**: 1.49 s (`inventory.json:23` — note: 1.5s in spec rounding is OK for
discussion). **HRF offset**: model output is *already shifted -5s* so
predicted vertex `v_t` corresponds to stimulus that occurred at wall time
`t + 5s`. **No extra HRF convolution required by trainer**.

### 1.2 Per-token alignment — the timestep mismatch

Critical: TRIBE v2 operates at **1 sample per TR (= 0.67 Hz)**, with
internal feature-extractor at 2 Hz. CLM v4 530M operates at **per-token
granularity**, ≥ 5–10 tokens/s on most prompts. So:

```
CLM emits             ~50 tokens   per   ~10s     = 5 Hz
TRIBE emits           ~7 vertices  per   ~10s     = 0.67 Hz
TRIBE feature extr.   ~20 features per   ~10s     = 2 Hz
```

**Alignment scheme** (Paradigm A spec):

1. **Tokenizer-side**: bucket CLM tokens into TR-bins by character-time
   (TTS speech rate ≈ 14 char/s for English Llama tokens — measured from
   gTTS default). Each TR bin holds `n_k` tokens where Σ n_k ≈ |seq|.
2. **Hidden projection**: pool CLM hidden `h_t ∈ R^4096` (CLM v4 530M
   final-layer hidden) within each TR bin via `mean(h_t for t in bin_k)`
   → `H_k ∈ R^4096`.
3. **P_S projector** (`docs/alm_clm_bridge_p_s_projector_spec_20260425.md`):
   currently `P_S: R^256 → R^16` (factorized as `V_PCA_top16 @ E_cell^T`).
   For Paradigm A we need a **new projector** `P_S^BOLD: R^4096 → R^10242`
   — see §2.2.
4. **Loss alignment**: per TR-bin `k`, compare `(P_S^BOLD ∘ pool ∘ CLM)(input)_k`
   vs `TRIBE_v2_forward(input)_k`. Both emit `[10242]` per TR.

**HRF handling**: TRIBE output is already HRF-pre-compensated (−5s shift),
so the CLM bin-k projection is matched against TRIBE bin-k *directly* (no
extra delay applied). The CLM hidden at bin-k corresponds to tokens
spoken in that TR window — TRIBE's −5s shift means it answers "what BOLD
*will* be observed 5s later for these tokens". Trainer matches the same
shifted target.

---

## 2. Loss formulation

### 2.1 Term

```
L_bold_paradigm_A = γ · (1/(B·T'·V)) · Σ_{b,k,v} ( P_S^BOLD(H_{b,k}) [v]
                                                    − TRIBE_v2.forward(x_b)_{k,v} )^2
```

where `V=10242`, `T'=n_TR_bins ≤ 64` (per `sft_data_format.json:14`),
`x_b` is the input record's text, `H_{b,k} = mean-pool(CLM_hidden_{b,t} for t∈bin_k)`.

This **replaces** the existing `L_bold` term in `loss_design.json:15-19`
(which already presupposed the same structure, but Phase 1.5 left it
inactive — γ=0). Phase 2 entry = "turn γ on".

### 2.2 P_S^BOLD projector — required spec

Existing P_S (`p_s_projector_spec_20260425.md:33-44`) is `D=256 → 16`.
Paradigm A requires:

```
P_S^BOLD : R^4096 → R^10242
```

**Factorization candidates** (must be specced before run):

| variant | factorization | param count | notes |
|---|---|---|---|
| **A.1 dense** | `Linear(4096, 10242, bias=True)` | 41.9M | simplest, no structural prior |
| **A.2 low-rank** | `Linear(4096, 1152) → Linear(1152, 10242)` | 16.5M | mirrors TRIBE's hidden=1152 |
| **A.3 PCA-anchored** | `V_PCA_top1152(4096×1152) @ Linear(1152, 10242)` | 11.8M trainable + 4.7M frozen | reuses P_S philosophy; PCA fitted on holdout CLM hidden stats |
| **A.4 TRIBE-tied** | initialize `P_S^BOLD = TRIBE.low_rank_head ⊕ TRIBE.predictor` (frozen first 2k steps, then unfreeze) | 23M | aggressive: directly inherits TRIBE's vertex map |

**Default for Paradigm A spec**: A.3 PCA-anchored. Rationale: matches the
existing P_S idiom (PCA evidence is what closed L1, see
`p_s_projector_spec_20260425.md:111-114` r6=0.976, r8=0.962), and
factorization is symmetric with TRIBE's own hidden=1152 bottleneck.

A.4 is reserved for **Paradigm A'** (warmstart distillation variant).

### 2.3 Updated 4-loss formula (Phase 2)

```
L_total_phase2 = α·CE(text) + β·MSE(tension) + γ·L_bold_paradigm_A
                 + δ·max(0, φ★_thr − φ★(model))
```

Phase 2 entry: γ ∈ {0.05, 0.1, 0.2} (LHS sweep), all other coefficients
inherit Phase 1.5 best combo. Phase 2 keeps δ-floor *active* — γ does not
replace φ★ regularizer, it stacks on top.

---

## 3. Data requirements

### 3.1 What's already specced

`sft_data_format.json:18-26` lists 50K records. **The TRIBE v2 stimulus
corpus row (Friends + movie10) is 10K examples** (line 24). For these 10K,
the spec's preprocessing step 3 says:

> "for sources with paired stimulus (TRIBE), use measured BOLD; else use
> TRIBE v2 forward simulator"

But `references/tribev2/tribev2/studies/algonauts2025.py:99-100` shows
`_download` is `NotImplementedError`. **Real Algonauts BOLD requires
`datalad` + ~several GB clone from
`github.com/courtois-neuromod/algonauts_2025.competitors.git`** (study
docstring lines 31-35).

### 3.2 What Paradigm A actually needs

Paradigm A as scoped uses **TRIBE v2 forward as the universal target** —
i.e., simulated BOLD for **all 50K records**, not just the 10K Friends+
movie10 subset. This eliminates the need for the datalad clone *for
training*, but **see §5 for why holdout still needs real BOLD**.

| record source | training target | data action |
|---|---|---|
| ShareGPT 10K | TRIBE_v2_forward(text) | full 50K simulator inference |
| anima paper 10K | same | same |
| #128 P8 ledger 3K | same | same |
| synthetic 5K | same | same |
| N-22 falsifiers 5K | same | same |
| **TRIBE Friends/movie10 10K** | TRIBE_v2_forward(text) **+** measured BOLD as auxiliary | datalad clone required for HOLDOUT only |
| auto-augment 7K | TRIBE_v2_forward(text) | same |

### 3.3 Holdout split for F4 verification

`sft_data_format.json:28` reserves `preregistered_holdout: 0.01` (= 500
records). For F4 honest verification (§5), this 500-record holdout **must
be drawn from the Friends/movie10 subset only**, with measured Algonauts
BOLD attached. Datalad clone is therefore **required** before Phase 2
launch — but only for the 500 holdout records' real fMRI, not the 50K
training set.

---

## 4. Risk: circularity (the central flaw)

### 4.1 The chain

```
TRIBE v2 internals (model.py + inventory.json)
  ├─ text encoder = meta-llama/Llama-3.2-3B (frozen, 6 layers used)
  └─ trained against measured fMRI (Algonauts 2025, 4 subjects, ~700 volunteers across all studies)

CLM v4 530M
  ├─ base architecture: deterministic Lagrangian flow (NOT a Llama derivative — confirmed by `architecture.json:13`)
  └─ post-Phase-2: trained to match TRIBE_v2.forward(text)

Phase 2 training loop
  ├─ input: text x
  ├─ TRIBE forward path: x → Llama-3.2-3B hidden → TRIBE projector → 10242-vertex y_TRIBE
  └─ CLM forward path:   x → CLM hidden (4096) → P_S^BOLD → 10242-vertex y_CLM
  └─ loss: ‖y_CLM − y_TRIBE‖²
```

### 4.2 Quantifying the circularity

**Q: Does TRIBE v2 forward depend on a Llama-like LM internally?**
**A: YES.** `inventory.json:40-45` declares `text_encoder.name =
"meta-llama/Llama-3.2-3B"`, layers `[0, 0.2, 0.4, 0.6, 0.8, 1.0]` × 6,
contextualized=true.

**Distillation chain risk** under Paradigm A (γ-only, naive):

```
real_brain ←(measured fMRI training)── TRIBE_v2(Llama-3.2-3B-based)
                                       └─(γ·MSE)── CLM_v4_530M (Lagrangian)
```

The CLM v4 is **not** a Llama derivative architecturally, but it would be
trained to match a target that is *explicitly* a Llama-3.2-3B-conditioned
brain encoder. **Net effect**: Phase 2 partially distills Llama-3.2-3B's
text representation into CLM v4 via the cortical channel.

| failure mode | mechanism | severity |
|---|---|---|
| **C1 — Llama-shape leak** | CLM hidden gets shaped to whatever projects cleanly through TRIBE's Llama-conditioned readout | HIGH if γ ≥ 0.2 |
| **C2 — false F4 success** | CLM matches TRIBE forward → Pearson r vs TRIBE target high → looks like brain match, but it's TRIBE-match | HIGH (this is the trap) |
| **C3 — phi_star contamination** | Llama-shape distillation flattens the Lagrangian-flow integration that φ★ measures | UNKNOWN — must remeasure φ★ post-Phase-2 every combo |
| **C4 — no genuine brain alignment** | TRIBE's own vertex Pearson r vs measured fMRI is bounded — CLM cannot exceed TRIBE's ceiling on simulated targets | STRUCTURAL |

### 4.3 Paradigm A' (mitigation, separate spec)

Paradigm A' = use TRIBE v2 as a *teacher signal* but supplement with **real
Algonauts BOLD targets on the 10K Friends/movie10 subset**. Loss becomes:

```
L_bold_A' = γ_sim · MSE(P_S^BOLD(H), TRIBE(x))
          + γ_real · MSE(P_S^BOLD(H), real_BOLD(x))    [only for paired records]
```

with `γ_real >> γ_sim` (e.g., 0.3 vs 0.05). This breaks the pure
circularity loop because the real-BOLD term anchors against measured fMRI,
not TRIBE's prediction. Spec for Paradigm A' = future doc.

---

## 5. F4 verification under Paradigm A

### 5.1 The naive trap

`falsifiers_preregistered.json:49-53` defines **F4 = Pearson r(bold_pred,
bold_target) > 0.5 on TRIBE-paired val**. *"TRIBE-paired val"* under
Paradigm A means TRIBE-simulated BOLD on val records — which is **the same
distribution** as the training target. The model literally optimizes this.

**A trivial Paradigm A run with γ ≥ 0.1 will almost certainly show F4
PASS, but this is not evidence of brain alignment** — it's evidence of
TRIBE-mimicry. This is the C2 trap above.

### 5.2 Required F4 honesty layer

To make F4 a real falsifier under Paradigm A, the spec must add **F4-real**:

| id | metric | data | threshold |
|---|---|---|---|
| F4-sim | Pearson r(bold_pred, **TRIBE-simulated** target) on val | val 2000 records | > 0.5 (sanity check that loss is converging) |
| **F4-real** | **Pearson r(bold_pred, measured Algonauts BOLD)** on holdout 500 | Friends/movie10 subset only, with `datalad clone` of Algonauts | **> 0.10** initial bar (TRIBE itself is ~0.15-0.25 on average vertex per the paper's reported Pearson) |
| F4-Δ | `r_real(CLM) − r_real(TRIBE_v2)` on same holdout | same | **≥ 0** (CLM should not be *worse* than the teacher; ideally ≥ TRIBE − 0.05) |

**F4-real is the falsifier that decides whether Paradigm A teaches genuine
brain alignment vs just mimicry**. F4-real threshold of 0.10 is calibrated
against TRIBE v2 paper's vertex-level Pearson r reports (averaged across
cortex), with margin for the projection chain loss.

### 5.3 Holdout integrity

- F4-real holdout **MUST NEVER appear in training** (preregistered exclusion).
- TRIBE v2 forward predictions for the F4-real holdout records **MUST also
  be excluded** from training-target generation (otherwise indirect leakage).
- Implication: data prep step 3 in `sft_data_format.json:32` needs a
  **holdout-aware filter**: skip TRIBE forward generation for the 500
  Friends/movie10 records reserved for F4-real.

---

## 6. Cost / wall estimate

### 6.1 TRIBE forward inference cost per record

Measured in Framing A pilot (`docs/framing_a_tribev2_pilot_results_2026_05_02.md:18`):

> "TRIBE v2 inference, 20 cortical maps | OK 20/20 — shape (20484,) per
> text, ~0.2-1.8s per text on Mac CPU"

(Note: pilot reports 20484 vertices = bilateral hemispheres of fsaverage5;
inventory declares 10242 = single-hemisphere. For Phase 2 we use
single-hemisphere 10242 to match `loss_design.json:18`.)

**Mac CPU baseline**: ~1.0s per record average. **GPU expected speedup**:
H100 with TRIBE-checkpoint resident = ~50x → **~0.02s per record**.
**Caveat**: TTS step (gTTS) is network-bound and ~3-5s per record — must
be replaced with offline TTS or pre-computed text-feature path
(see §6.3) or amortized via batching at the events-DataFrame layer.

### 6.2 50K-record TRIBE forward inference budget

| path | per-record | 50K total | wall | cost (RunPod H100 spot @ $2.5/hr) |
|---|---|---|---|---|
| Mac CPU, naive (TTS + forward) | 5s | 250000s | 69 hrs | $0 (local) |
| H100, naive (TTS still on CPU) | 4s (TTS bottleneck) | 200000s | 56 hrs | $140 |
| **H100, batched + offline TTS** | 0.05s | 2500s | 0.7 hr | **$1.75** |
| H100, **bypass TTS via pre-computed Llama-3.2-3B hidden** | 0.02s | 1000s | 0.3 hr | $0.70 |

**Recommended path**: pre-compute Llama-3.2-3B layer-`{0, 0.2, ..., 1.0}`
hiddens once for all 50K records (offline batch on H100, ~2 hrs, ~$5),
cache as feature tensors, then feed **directly** into TRIBE's transformer
encoder bypassing the text→audio→text TTS detour. Total prep ≈ **$10,
~3 hrs**.

### 6.3 Per-step training cost adjustment

Adding γ·L_bold to the per-step loss adds:

- TRIBE forward: skipped during training (targets are pre-computed in
  step 6.2 above and cached as `[T', 10242]` tensors per record).
- P_S^BOLD forward: 4096 → 1152 → 10242 = 16.5M params (A.2) or 11.8M
  trainable (A.3). Forward cost per microbatch (B=4, T'=64): ~30 GFLOPs
  → negligible vs CLM 4096-d transformer per-step.
- Backward through P_S^BOLD: 2× forward = 60 GFLOPs.

**Net per-step overhead**: < 5% on H100 bf16. Throughput penalty ~ 5% →
wall-hours estimate from `cost_estimate.json:14-17` (10.7 hrs nominal)
becomes **~11.2 hrs**. Cost increment: ~$1.

---

## 7. Phase 2 entry plan — γ-only mini-run

### 7.1 Spec

Before stacking γ·L_bold into the 4-loss combo (and thus risking CE +
tension regression), run an **isolated γ-only mini-run** to confirm:
(a) the loss converges, (b) P_S^BOLD trains stably, (c) CLM hidden
trajectory does not collapse, (d) F4-sim begins to climb.

| param | value | rationale |
|---|---|---|
| base ckpt | CLM v4 530M `~/anima/checkpoints/clm_v4_350m/scale_350m/best.pt` | same as P9 main |
| LoRA | r=64, α=128 | preserves base φ★ structurally |
| frozen | base CLM weights, all transformer layers | only LoRA + P_S^BOLD train |
| α | **0.0** | CE off — pure BOLD objective |
| β | **0.0** | tension off |
| γ | **0.1** | mid-range from sweep band |
| δ | **1.0** | φ★ floor still active |
| steps | **5K-10K** | small isolated probe |
| examples | 5K subset of 50K (pre-shuffled, fixed seed) | 1 epoch over subset |
| holdout | 500 (F1+F4-sim+F4-real measured at end) | preregistered subset |
| logging | every 100 steps: L_bold, L_phi, P_S^BOLD grad-norm, CLM hidden EMA-norm | pre-flight diagnostics |

### 7.2 Cost

| component | wall | $ |
|---|---|---|
| data prep (Llama hidden cache + TRIBE forward cache, 5K subset) | 30 min | $1.50 |
| training 5K examples × 1 epoch × ~2K tok/example × (1/8000 tok/s) on H100 | ~20 min | $1 |
| F1+F4-sim+F4-real evaluation | 15 min | $0.75 |
| φ★ post-train remeasure (anima_phi_v3_canonical) | 5 min/measurement × 1 = 5 min | $0.25 |
| margin (~50% buffer) | 35 min | $1.75 |
| **TOTAL** | **~1.75 hr** | **~$5** |

### 7.3 Mini-run pass criteria (predicate, raw#0 preregistered)

```
PASS = (L_bold final ≤ 0.3 × L_bold_initial)         # convergence
     ∧ (φ★ final ≥ 5.0)                              # floor held
     ∧ (P_S^BOLD ‖grad‖ stable, no NaN)              # numerics
     ∧ (CLM hidden EMA-norm Δ ≤ 30%)                 # no collapse
     ∧ (F4-sim Pearson r ≥ 0.30)                     # signal present
     ∧ (F4-real Pearson r ≥ 0.05 ∨ F4-Δ ≥ -0.05)    # not regressing vs TRIBE alone
```

If FAIL on F4-real but PASS on F4-sim → **C2 trap confirmed empirically**
→ proceed to Paradigm A' (real-BOLD anchor variant) before joining 4-loss.

If PASS all → green-light to Phase 2 4-loss combo with γ ∈ {0.05, 0.1, 0.2}
LHS sweep.

---

## 8. Honest C3 (raw#91 mandatory — minimum 5 caveats)

1. **CIRCULARITY (the headline risk).** TRIBE v2's text encoder is
   `meta-llama/Llama-3.2-3B` (`inventory.json:42`). Training CLM to match
   TRIBE forward partially distills Llama-3.2-3B's text-shape into CLM via
   the cortical readout. The CLM is not a Llama derivative
   architecturally, but Paradigm A makes it Llama-conditioned in the
   readout space. F4-sim PASS does NOT imply brain alignment — it implies
   TRIBE-mimicry. F4-real (against measured Algonauts BOLD) is the only
   honest falsifier.

2. **TRIBE forward ≠ real brain.** TRIBE v2's own vertex-level Pearson r
   vs measured fMRI is bounded (paper reports averages in the ~0.15-0.25
   range for naturalistic stimuli; not yet locally verified). Even a
   *perfect* TRIBE-mimic CLM cannot exceed TRIBE's own ceiling. The gap
   between "match TRIBE forward" and "match real brain" is a structural
   loss term that Paradigm A cannot close.

3. **Per-token vs per-TR alignment is heuristic.** CLM tokens fire at
   ~5-10 Hz; TRIBE outputs are at 0.67 Hz (TR=1.49s). The proposed
   character-time TR-binning + mean-pool is an *unprincipled* mapping —
   the assumption that "tokens spoken in TR k correspond to BOLD at TR k"
   is approximately true for naturalistic dialogue but breaks for code,
   silent prompts, structural markers, etc. A more principled alignment
   (event-based, attention-weighted) is future work.

4. **HRF assumption transferred from TRIBE to CLM trainer.** TRIBE
   pre-compensates HRF by −5s offset (`README.md:32`). The trainer
   inherits this assumption blindly. If CLM's "internal time" runs faster
   or slower than spoken-text time (likely — Lagrangian flow is dimensionless
   in seconds), the −5s offset is misapplied. Fixed-offset HRF is also a
   simplification of the canonical double-gamma — TRIBE chose this for a
   reason but it propagates as model-class assumption.

5. **P_S^BOLD has no calibration evidence yet.** The existing P_S
   (`p_s_projector_spec_20260425.md`) is `D=256 → 16` and has measured
   top-16 energy ratio 0.962-0.976 (PASS). The new `P_S^BOLD: 4096 →
   10242` has **no PCA evidence, no orthogonality verification, no
   determinism check**. It is parameterized but uncalibrated. Adding it
   to the loss before a calibration spec equivalent to the original P_S
   selftest is a violation of the L1-bridge spec discipline.

6. **φ★ regularizer may interact adversarially with γ·L_bold.** φ★
   measures internal integration via spectral properties of Lagrangian
   flow. L_bold pushes hidden toward Llama-shape (via TRIBE readout).
   These two objectives are not obviously aligned and may **fight** —
   the δ-floor stays satisfied but at the cost of training-time
   instability. φ★ post-train remeasure must be done **per combo**, not
   just per strategy (spec change vs `risk_strategy.json:11`).

7. **TTS bottleneck and gTTS network dependency.** TRIBE's text path
   depends on `gTTS` (Google TTS, network-bound, rate-limited). For
   50K records this is operationally fragile — a network blip mid-run
   stalls hours of compute. Pre-cached Llama-3.2-3B hidden bypass
   (§6.2) is mandatory, not optional. This means we depend on
   Llama-3.2-3B weights being available; if the HF gating changes the
   whole pipeline breaks.

8. **No measurement of inter-vertex correlation structure preservation.**
   MSE on 10242 independent vertices ignores the fact that BOLD vertices
   are spatially smooth + ROI-clustered. A model can achieve low
   per-vertex MSE while destroying ROI-level coherence. F4 should add a
   ROI-level Pearson r metric (Yeo-7 or Schaefer-200) as F4-roi to catch
   this — currently absent from the falsifier suite.

---

## 9. Recommendation — proceed to Paradigm A' or stay with A?

**Recommendation: do NOT execute Paradigm A in pure form. Spec Paradigm
A' before any γ·L_bold mini-run.**

Rationale:
- The C2 trap (F4-sim PASS without brain alignment) is **structurally
  guaranteed** in pure Paradigm A given enough γ and steps. Running pure
  A produces a positive-looking but uninterpretable result.
- Paradigm A' (TRIBE-sim + real-BOLD anchor on 10K Friends/movie10) costs
  marginally more (datalad clone ~$0 + ~3 hrs prep) but turns F4 into a
  real falsifier rather than a tautology.
- The mini-run spec (§7) can be repurposed for Paradigm A' with
  `γ_sim=0.05, γ_real=0.3` and the same 5K-10K step budget — no
  re-engineering needed beyond the loss term.

**However**, if the user still wants Paradigm A first (e.g., as ablation
control to prove the C2 trap empirically), the §7 mini-run is cheap
(~$5, ~1.75 hr) and will produce direct evidence of the trap when
F4-sim PASSES while F4-real FAILS — that's actually a useful negative
result.

**Order of operations** (recommended):
1. Spec Paradigm A' (separate doc).
2. Datalad-clone Algonauts holdout 500 records (one-time, $0).
3. Run §7 mini-run as Paradigm A control (~$5, ~1.75 hr) — predict F4-sim
   PASS + F4-real FAIL (≈ trap confirmed).
4. Run §7 mini-run with Paradigm A' loss (~$6, ~2 hr) — predict F4-sim
   PASS + F4-real PASS (≈ real signal present).
5. If A' passes mini-run, proceed to 4-loss Phase 2 sweep.

---

## 10. Cross-refs

- `references/tribev2/inventory.json` — TRIBE v2 architecture / encoder spec
- `references/tribev2/tribev2/model.py` — `FmriEncoderModel.forward` signature
- `references/tribev2/tribev2/demo_utils.py` — `TribeModel.predict` inference path
- `references/tribev2/tribev2/studies/algonauts2025.py` — Algonauts dataset (datalad clone required)
- `state/p9_sft_spec_2026_05_02/loss_design.json` — existing 4-loss formula
- `state/p9_sft_spec_2026_05_02/sft_data_format.json` — 50K record sources
- `state/p9_sft_spec_2026_05_02/falsifiers_preregistered.json` — F1-F4 spec, F4 currently sim-only
- `state/p9_sft_spec_2026_05_02/risk_strategy.json` — φ★ flip primary risk
- `state/p9_sft_spec_2026_05_02/cost_estimate.json` — baseline cost band
- `docs/alm_clm_bridge_p_s_projector_spec_20260425.md` — P_S projector spec (basis for P_S^BOLD §2.2)
- `docs/framing_a_tribev2_pilot_results_2026_05_02.md` — pilot evidence: TRIBE v2 inference works on Mac CPU, ~1s/record

---

## 11. raw#12 evidence vs raw#13 inference separation

- **measured (raw#12)**: TRIBE v2 architecture/dims (inventory.json),
  forward signature (model.py:163), HRF offset (README.md:32), TRIBE
  inference latency on Mac CPU (Framing A pilot:18), text_encoder identity
  (inventory.json:42), Friends/movie10 subset size 10K
  (sft_data_format.json:24), P_S r6/r8 PASS energy ratios
  (p_s_projector_spec:111-114).
- **inferred (raw#13)**: H100 TRIBE forward speedup ~50x (extrapolated
  from CPU baseline), P_S^BOLD parameter counts (computed from candidate
  factorizations not yet trained), F4-real threshold 0.10 (calibrated
  against TRIBE paper averaged Pearson — paper not locally re-verified),
  per-token TR-binning alignment fidelity (heuristic, no fMRI ground
  truth), Llama-shape distillation severity (qualitative, not measured).
- **all inferences are falsifiable** by §7 mini-run (~$5) followed by
  Paradigm A' mini-run.
