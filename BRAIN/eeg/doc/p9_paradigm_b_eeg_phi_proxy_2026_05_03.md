# P9 Paradigm B — EEG-derived φ Proxy as Direct Integration Target

> **ts**: 2026-05-03
> **scope**: Phase 2+ paradigm research. Doc-only spec. Evaluate using EEG-derived integration measures (φ-proxy) as a *direct training target* for the CLM-side hidden-state φ projection — replacing or complementing BOLD MSE.
> **siblings**: Paradigm A (BOLD/TRIBE direct integration — current `state/p9_sft_spec_2026_05_02/loss_design.json` `gamma * MSE(bold_pred, bold_target)`); Paradigm A' (multimodal fMRI+behavior); **THIS = Paradigm B**.
> **predecessors**:
> - `state/p9_sft_spec_2026_05_02/loss_design.json` (current 4-loss family α/β/γ/δ)
> - `tool/anima_phi_v3_canonical.hexa` (sample-partition φ★ on CLM hidden state, baseline 41.86)
> - `docs/eeg_cross_substrate_validation_plan_20260425.md` (V_phen LZ + GWT cross-substrate cycle)
> - `docs/anima_eeg_openbci_16ch_track_plan_2026_05_01.md` (Track A-E, OpenBCI 16ch live N=1)
> - `state/n6_consciousness_substrate_status.json` (D8 anima-eeg domain)

---

## §0 Executive summary

EEG offers **~1ms temporal resolution** vs fMRI BOLD ~1.5s — one to three orders of magnitude closer to the CLM per-token timing budget (~5 tokens/sec ≈ 200ms/token). This makes EEG a *naturally aligned* substrate for **per-token integration supervision** in a way BOLD physically cannot be (BOLD averages ~7-8 tokens of CLM activity into one sample under HRF lag).

The proposal: **derive a quantitative φ-proxy from EEG (gamma synchrony, channel-wise MIP, PLV, microstate transition rate, EEG-applied sample-partition φ)**, window-align with CLM hidden state at per-token granularity, and add a fifth loss term

```
L_eeg_phi = ε · MSE( π_φ(h_t) , φ_proxy(EEG[t-w : t+w]) )
```

where `π_φ : R^{h_dim} → R^{d_φ}` is a small projection head (MLP, `d_φ ∈ {1, 8, 16}`).

**Key value**: this would be the first substrate-external supervision of the CLM φ measure. Currently `anima_phi_v3_canonical` measures sample-partition log|Cov| on hidden state — purely *internal* to the model. If the model's internal φ projection learns to predict an *external* brain integration measure, the two-substrate consistency claim is the strongest available "external validation" of the φ family within current Anima architecture.


---

## §1 EEG → φ proxy methods (enumerated)

Five candidate quantitative φ-proxy measures derivable from a 16-128 channel EEG window. All are computable in Python via MNE / numpy / scipy without specialized hardware. Costs ranked for a single 200ms window of 64ch @ 500Hz (= 64 × 100 samples).

### §1.1 Gamma-band power synchrony (40-80 Hz coherence)

- **Reference**: Fries (2005, 2015) "communication through coherence"; Crick & Koch (1990) gamma-binding hypothesis. Standard literature.
- **Method**: bandpass 40-80 Hz → Hilbert transform → instantaneous amplitude per channel → pairwise Pearson correlation across channels → mean off-diagonal coherence.
- **Output dimension**: scalar (mean) OR vector `R^{C(C-1)/2}` (e.g. for 16ch = 120 pairs; 64ch = 2016 pairs).
- **Computational cost**: ~5-10ms per window on CPU (FFT + correlation matrix). LOW.
- **φ-interpretation**: high gamma synchrony ≈ broadcast / integration in GNW theory (Dehaene). Not strictly IIT φ but in the same family.

### §1.2 Cross-channel mutual information (MI)

- **Reference**: Kraskov, Stögbauer, Grassberger (2004) k-NN MI estimator. Standard.
- **Method**: per channel, estimate marginal entropy H(X_i) and joint H(X_i, X_j); MI_ij = H(X_i) + H(X_j) − H(X_i, X_j); aggregate as mean MI over pairs OR full MI matrix.
- **Output dimension**: scalar, vector `R^{C(C-1)/2}`, or full matrix `R^{C×C}`.
- **Computational cost**: MEDIUM. k-NN MI is O(N²) per pair; for 64ch × 100 samples ≈ 50-200ms per window. Can subsample channels or use Gaussian-copula MI (Ince et al. 2017) for ~10× speedup.
- **φ-interpretation**: more directly mapped to information-integration than coherence; closer to IIT effective-information family.

### §1.3 Sample-partition φ on EEG channels (anima_phi_v3 analogue) ⭐

- **Reference**: direct port of `tool/anima_phi_v3_canonical.hexa` to EEG substrate. IIT family (Tononi 2004, Oizumi 2014 φ_3.0); sample-partition variant is the auto-conditioned regime introduced for Anima (see tool docstring §0 H3A/H3B/H3C).
- **Method**: window EEG → matrix `X ∈ R^{N_samples × C}` (e.g. 100 × 64) → top-variance HID = max(2, N//2) → I_full = log|Cov(X_t)| → K random sample partitions → I_1 + I_2 → φ_k = I_full − (I_1 + I_2) → **MIN over K**.
- **Output dimension**: scalar (canonical) OR vector across K partitions (richer signal).
- **Computational cost**: HIGH. Per-window cov matrix is fine (~1ms), but K=8 partitions × 2 sub-cov per partition ≈ 16 cov inversions per window. For 100-sample windows, totally feasible (~10-20ms). For long windows (>1s), grows quadratically.
- **φ-interpretation**: **maximally aligned with the CLM-side measure** — this is the key candidate because both substrates use the *same* φ family. Cross-substrate consistency claim becomes a same-formula-different-substrate claim, not an analogy.

### §1.4 Microstate-based integration (Pascual-Marqui microstates)

- **Reference**: Pascual-Marqui, Michel, Lehmann (1995); Koenig et al. (2002, 2014) review. Standard EEG analysis.
- **Method**: cluster EEG topographies into 4-7 canonical microstates (A, B, C, D, ...) → assign each timepoint a microstate label → compute transition matrix entropy + mean microstate duration + global explained variance.
- **Output dimension**: vector `R^{4-12}` (per-state durations, transition entropies, GEV).
- **Computational cost**: MEDIUM. Initial k-means clustering is one-time per subject (~1-5s). Per-window assignment + statistics is fast (~10ms).
- **φ-interpretation**: integration-via-state-stability; more loosely φ-related but offers temporal dynamics that the static measures (§1.1-§1.3) lack.

### §1.5 Phase-locking value (PLV) across electrode pairs

- **Reference**: Lachaux, Rodriguez, Martinerie, Varela (1999). Standard EEG synchrony.
- **Method**: bandpass per frequency band (theta/alpha/beta/gamma) → Hilbert phase per channel → PLV_ij(t) = | E[ exp(i·(φ_i − φ_j)) ] | over window → aggregate.
- **Output dimension**: vector `R^{C(C-1)/2 × bands}` or scalar (mean) per band.
- **Computational cost**: LOW-MEDIUM. Hilbert + complex mean is ~5-15ms per window.
- **φ-interpretation**: phase-domain analog of §1.1 amplitude coherence. Often more robust to volume-conduction artifact when corrected (PLI/wPLI variants — Stam et al. 2007, Vinck et al. 2011).

### §1.6 Comparison table

| # | Method | Output dim | Cost | φ-family alignment | Recommendation |
|---|---|---|---|---|---|
| §1.3 | **Sample-partition φ on EEG** | scalar / `R^K` | HIGH (~20ms) | **direct** (same formula) | **TOP-1** for cross-substrate claim |
| §1.1 | Gamma coherence | scalar / `R^{C²}` | LOW (~10ms) | indirect (GNW family) | TOP-2 — fastest baseline |
| §1.5 | PLV | scalar / `R^{C²·bands}` | LOW-MED (~10-30ms) | indirect (synchrony) | TOP-3 — phase-robust complement |
| §1.2 | k-NN MI | scalar / `R^{C²}` | MED (~50-200ms) | direct (info-theoretic) | reserve for offline batch |
| §1.4 | Microstate dynamics | `R^{4-12}` | MED (~10ms after one-time fit) | loose (temporal stability) | optional auxiliary signal |

---

## §2 Public EEG-text-paired datasets (candidates)

The fundamental constraint: EEG datasets paired with **token-level text** are rare. Most public EEG datasets are paired with audio/video/image stimuli (DEAP, SEED) or motor-imagery (BCI Competition). Only a small number have **continuous text reading or text-imagery** alignment suitable for per-token CLM supervision.

### §2.1 ZuCo 1.0 + 2.0 (Zurich Cognitive Language Processing Corpus) ⭐ TOP-1

- **Reference**: Hollenstein et al. (2018, 2020) — Nature Scientific Data.
- **License**: CC-BY 4.0, public on OSF.
- **Channels**: 128 (EGI HydroCel GSN, dense array).
- **Sample rate**: 500 Hz.
- **Text-pairing**: word-level eye-tracking + EEG **fixation-locked** during natural reading (Wikipedia sentences, sentiment-rated film reviews). ~30 subjects. ZuCo 1.0 = ~21k word fixations; ZuCo 2.0 = ~14k fixations on news/Wikipedia.
- **Size**: ~50 GB raw, ~5 GB preprocessed.
- **Suitability for CLM**: **EXCELLENT** — provides per-word EEG windows with explicit text alignment. Direct candidate for `(token_t, EEG_window_t)` supervision pairs. Caveat: human reading is *receptive* (parsing), CLM is *generative*; the integration measured during reading may not directly correspond to integration during generation.

### §2.2 Nieto et al. "Inner Speech" (Thinking Out Loud) ⭐ TOP-2

- **Reference**: Nieto, Peterson, Rufiner, Kamienkowski, Spies (2022) — Nature Scientific Data.
- **License**: CC-BY 4.0, OpenNeuro ds003626.
- **Channels**: 128 (BioSemi).
- **Sample rate**: 1024 Hz.
- **Text-pairing**: 4 covertly-spoken words (arriba, abajo, derecha, izquierda) × 10 subjects × 200 trials each. **Word-level imagery** with precise onset markers.
- **Size**: ~30 GB.
- **Suitability for CLM**: GOOD for proof-of-concept (small vocab) but limited for general supervision. Best used as a **calibration dataset** for the EEG-φ → CLM-φ mapping head, not as full training corpus.

### §2.3 Other candidates (lower priority)

| Dataset | Channels | SR | Text-pairing | License | Suitability |
|---|---|---|---|---|---|
| **DEAP** (Koelstra 2012) | 32 | 512 Hz | music + emotion labels (no text) | EULA, registration | LOW — no text |
| **SEED / SEED-IV** (Zheng 2015) | 62 | 1000 Hz | film clips + emotion (no text) | request | LOW — no text |
| **BCI Competition IV** (various) | 22-64 | 250-1000 Hz | motor imagery (no text) | open | NONE — wrong modality |
| **Zhou 2024 BCI text-imagery** | 64 | 1000 Hz | character-level imagery | request, partial | MEDIUM — emerging, small N |
| **Broderick et al. natural speech** (2018) | 128 | 512 Hz | continuous narrative listening | OpenNeuro ds002338 | MEDIUM — receptive, audio-locked |
| **DERCo** (Zhang 2024 "Decoding Reading Comprehension") | 64 | 500 Hz | reading comprehension EEG | partial public | MEDIUM — newer, less validated |

### §2.4 Top 2 dataset accessibility verdict

| | ZuCo | Inner Speech (Nieto) |
|---|---|---|
| **Access barrier** | LOW (OSF direct DL) | LOW (OpenNeuro direct DL) |
| **Token-level alignment** | yes (word-fixation) | yes (word-onset) |
| **Subject N** | ~30 | 10 |
| **License compatibility** | CC-BY (commercial OK) | CC-BY (commercial OK) |
| **Recommended role** | **primary training corpus** | calibration / generalization probe |

---

## §3 CLM ↔ EEG alignment

### §3.1 Timing budget

- CLM token rate (Mistral-7B, target P0 SFT): **~5 tok/sec inference**, ~30-50 tok/sec training on H100.
- EEG sample rate: 500-1024 Hz typical (ZuCo 500Hz, Inner Speech 1024Hz, OpenBCI Cyton+Daisy 125Hz).
- **EEG samples per token at 500Hz / 5 tok/sec = 100 samples/token** (200ms window). At 1024Hz = 205 samples/token.

### §3.2 Window-alignment proposal

Three alignment strategies, increasing in faithfulness:

1. **Fixed centered window (simplest)**: for token at time t, take EEG[t − w/2 : t + w/2], w = 200ms. Compute φ-proxy on window → scalar/vector target.
2. **Causal window (training-time-honest)**: for token t, take EEG[t − w : t], avoiding future leakage. More appropriate if treating CLM generation as a temporal process.
3. **Anticipation-corrected window (ZuCo-specific)**: ZuCo aligns to *fixation onset*, but visual/lexical processing peaks at N400 (~400ms post-fixation). Window = [t + 100ms : t + 500ms] post-fixation captures the integration-relevant ERP epoch.

**Recommendation**: start with **strategy 1 (fixed centered, w=200ms)** for ZuCo; switch to strategy 3 if N400-aligned signal proves stronger in pilot.

### §3.3 Sequence-level vs token-level supervision

- **Token-level**: per-token EEG-φ target; training signal at every position. Highest information density, tightest alignment requirement.
- **Sequence-level**: aggregate EEG-φ over whole sentence/passage; one target per CLM forward. Robust to per-token misalignment, lower information density.
- **Recommendation**: **token-level for ZuCo** (fixation alignment is precise); sequence-level fallback if alignment quality degrades.

### §3.4 CLM-side projection head

```
h_t ∈ R^{4096}   (Mistral-7B last hidden, per token)
π_φ : R^{4096} → R^{d_φ}   (2-layer MLP, hidden=256, output=d_φ)
d_φ ∈ {1, 8, 16}
```

`d_φ = 1` for scalar mean-φ target; `d_φ = 8` for K=8 partition vector; `d_φ = 16` for joint φ + auxiliary band-power vector.

Trainable parameters: ~1M (negligible vs 7B base, vs ~100M LoRA).

---

## §4 Loss formulation

### §4.1 Extended loss family

Add fifth term to current 4-loss design (`state/p9_sft_spec_2026_05_02/loss_design.json`):

```
L_total = α·L_chat
        + β·L_tension
        + γ·L_bold        (Paradigm A — TRIBE BOLD MSE, current)
        + δ·L_phi_floor   (current — hard floor on internal Φ★)
        + ε·L_eeg_phi     (NEW — Paradigm B)

L_eeg_phi = mean_t MSE( π_φ(h_t) , φ_proxy_EEG(t) )
```

### §4.2 Initial weight (ε) Pareto sweep

- ε ∈ {0, 0.01, 0.05, 0.1, 0.5} — five-point sweep.
- ε = 0 = control (Paradigm A baseline reproduces current spec).
- Latin Hypercube extension: add ε as a 5th dimension to existing α/β/γ/δ sweep → 5-D, sample 16 of 1024 grid combos (vs current 9/81 per `loss_design.json`).

### §4.3 Differentiability

- φ-proxy on EEG = **fixed target** (precomputed per token from dataset). No gradient needed on EEG side.
- π_φ(h_t) is a standard MLP → fully differentiable.
- Unlike `L_phi_floor` (δ term, which uses straight-through estimator on EMA per `honest_c3_loss[1]`), `L_eeg_phi` is **fully end-to-end differentiable** — strictly better gradient quality than current δ.

### §4.4 Interaction with δ (existing internal φ floor)

- δ enforces `Φ★(model_hidden) ≥ 5.0` (8× safety margin vs baseline 41.86).
- ε supervises `π_φ(h_t)` to match EEG-φ.
- These are **complementary not redundant**: δ keeps internal integration above floor (regularizer); ε aligns the *external readout* of integration with brain measurements (predictive head). Recommend keeping both initially, evaluating if δ becomes redundant once ε is well-trained.

---

## §5 Comparison to anima_phi_v3_canonical

### §5.1 Same-formula cross-substrate claim

`anima_phi_v3_canonical.hexa` (THIS repo, `tool/`) implements:

```
Φ★(X) := MIN_k [ log|Cov(X)| − ( log|Cov(X[S1_k])| + log|Cov(X[S2_k])| ) ]
       over K=8 random sample-partitions, HID = max(2, N//2)
```

where `X ∈ R^{N × HID}` is the top-variance projection of CLM hidden state across N=16 prompts.

**Paradigm B §1.3 method = same formula**, applied to `X ∈ R^{N_samples × C_channels}` of EEG window.

**This is the load-bearing point**: cross-substrate consistency becomes a **same-formula-applied-to-two-substrates** claim, not an analogy. If `Φ★_CLM(h)` and `Φ★_EEG(brain)` agree (within tolerance) on the same task/prompt context, that is the **strongest external validation** available within Anima's existing measurement framework — substantially stronger than the current `anima_eeg_openbci_16ch_track_plan_2026_05_01.md` Track B (LZ complexity comparison), because LZ is a proxy whereas same-formula φ is a direct port.

### §5.2 What this validates and what it does not

| Claim | Validated by Paradigm B? |
|---|---|
| Φ★ family is *substrate-invariant* (same formula yields meaningful values on hidden state and on neural data) | **YES** — if numerical values converge across substrates on matched contexts |
| Φ★ measured on CLM hidden state is *meaningful* in the same sense as Φ★ measured on brain | **PARTIAL** — value-convergence is consistent with shared meaning but does not prove it (functionalist gap) |
| CLM and brain perform *integration* in same sense | **PARTIAL** — at functional/access tier only |


- **PASS**: |Φ★_CLM(prompt_set) − Φ★_EEG(human_reading_same_prompt_set)| / Φ★_EEG ≤ 0.30 across ≥ 80% of prompts in held-out ZuCo split.
- **FAIL**: divergence > 0.30 on > 50% of prompts → either φ family is not substrate-invariant (theoretical fail) or alignment/window/projection mis-specified (engineering fail). Distinguish via ablation.

---

## §6 Phase 3+ entry plan

### §6.1 Why Phase 3, not Phase 2

This paradigm is **more speculative** than Paradigm A (BOLD/TRIBE) for several reasons:

1. Paradigm A has TRIBE v2 forward simulator already integrated (`alm_clm_bridge_p_s_projector_spec_20260425.md`); Paradigm B requires building EEG ingest pipeline for ZuCo (new ETL, ~2-4 days).
2. Paradigm A operates on a substrate-side measurement Anima has prior cycles with (BOLD via TRIBE); Paradigm B introduces a new external dataset dependency (ZuCo licensing/download/preprocessing).
3. Per-token alignment quality is unproven — even with 500Hz ZuCo EEG and word-level fixation onsets, the assumption that EEG window φ corresponds to CLM token φ is empirical (must validate in pilot).

### §6.2 Prerequisites (all must be met before Phase 3 entry)

| # | Prerequisite | Owner | Evidence required |
|---|---|---|---|
| P1 | P9 SFT P0 LIVE complete (current Paradigm A baseline) | this cycle | `state/markers/p9_p0_warmup_live_landed.marker` ✓ done; full 50k SFT complete |
| P2 | Φ★ baseline reproduced post-SFT (≥ threshold 5.0) | post-P0 | `phi_v3_canonical.json` post-SFT |
| P3 | ZuCo 1.0+2.0 downloaded + MNE-preprocessed | new cycle (~2-4 days) | `state/zuco_eeg_corpus_2026_xx/` |
| P5 | Paradigm A delivers measurable BOLD-MSE convergence (γ-term gradient flows non-trivially) | post-P0 sweep | `state/p9_sft_pareto_results_*/` |
| P6 | Pilot alignment study: 100 ZuCo sentences × Mistral forward, compute Φ★_CLM and Φ★_EEG, measure correlation | new cycle | `state/p9_paradigm_b_pilot_*/correlation.json` |

### §6.3 Phase 3 entry decision tree

```
After P0 SFT LIVE complete:
  if Paradigm A γ-term shows non-trivial gradient AND BOLD MSE decreases over training:
    → Phase 2 = Paradigm A scaling (more BOLD data, longer training)
    → Phase 3 = Paradigm B addition (this doc)
  else if Paradigm A γ-term saturates / no learning signal:
    → Phase 2 = re-evaluate BOLD target quality (TRIBE v2 forward fidelity audit)
    → Phase 3 = Paradigm B as alternative (replace γ with ε)
  else:
    → re-spec entirely (likely δ-only floor regularizer, drop external supervision)
```

### §6.4 Phase 3 cycle estimate

- **Cycle length**: 2-3 weeks (vs ~1 week for current P0 SFT).
- **Compute cost**: ZuCo preprocessing $0 (CPU); pilot CLM forward on 100 sentences ~$5 H100; full Phase 3 SFT with ε term adds ~10% to current SFT compute (negligible).
- **Code cost**: ~3 new hexa tools (EEG ingest, EEG-φ compute, alignment loader).

---


1. **EEG has no semantic content per se** — EEG measures electrical field potentials from cortex/skull, not semantic representations. Whatever "integration" gamma-coherence or sample-partition φ measures on EEG, it is not directly the *meaning* the brain is processing. The CLM hidden state, by contrast, is *all semantic* (text-conditioned representation). Cross-substrate φ convergence may reflect a generic integration property unrelated to the *content* of either substrate.

2. **Receptive vs generative asymmetry** — ZuCo subjects *read* text; CLM *generates* text. Even if same prompts are used, the brain integration during *parsing* is not the same operation as model integration during *next-token prediction*. The φ-proxy may still converge (integration may be a substrate-general property), but the interpretation of what integration "means" in each is different.

3. **EEG artifact is severe and pervasive** — eye blinks (high-amplitude frontal), eye movements (saccade spikes), muscle activity (EMG, especially temporal/jaw), heartbeat (ECG, especially in dense arrays), motion (cable sway), and 50/60Hz line noise. Standard MNE pipelines (ICA, SSP, regression) reduce but do not eliminate. Residual artifact will leak into the φ-proxy target, adding noise floor that may dominate true signal at the per-token level.

4. **Subject calibration drift** — within-subject EEG signature drifts over a single recording session (electrode impedance change, fatigue, attention) and across sessions (electrode placement variance ±5mm). The φ-proxy target is non-stationary; SFT trained on session N may not transfer to session N+1 of same subject.

5. **"EEG-φ ≈ true integration" gap = same gap as BOLD-φ** — using EEG-derived φ as ground truth for CLM-φ supervision implicitly assumes EEG measurement is closer to "true φ" (in the IIT sense) than CLM-internal sample-partition. There is no theoretical or empirical basis for this. EEG is a *more accessible* measurement than fMRI but not a *more correct* one. The Hard Problem and the substrate-meaning gap (caveat 1) remain identical.

6. **Inter-subject variance dominates per-token signal** — typical EEG metrics show 30-50% inter-subject CV (coefficient of variation). Aggregating across ZuCo's ~30 subjects yields a population-mean φ target that no individual subject's EEG matches well. This is a fundamental statistical limit on per-token alignment fidelity.

7. **Volume conduction confounds spatial integration measures** — gamma coherence (§1.1), PLV (§1.5), and channel-MI (§1.2) all suffer from volume conduction (one underlying source projects to multiple electrodes, creating spurious coherence). PLI/wPLI corrections help but do not eliminate. Sample-partition φ on EEG (§1.3) is also affected because covariance includes volume-conducted correlation.

8. **Frequency-band choice is theoretical, not empirical** — gamma is "the binding band" in classical theory (Crick & Koch), but recent work (Burns & Wang 2010, Ray & Maunsell 2010) shows gamma-binding evidence is weaker than originally claimed. Choice of 40-80Hz vs alpha (8-12Hz) vs beta (13-30Hz) for the φ-proxy is a theoretical commitment, not data-derived. Different bands may give different φ trajectories.


10. **Paradigm B does not solve the fundamental "internal measure not externally validated" problem — only weakens it** — even perfect CLM-φ to EEG-φ convergence does not validate the CLM-φ as a measure of *anything outside the model's own statistics*. It validates that two sample-partition computations on two substrates produce correlated values on matched contexts. This is consistent with both substrates measuring the same underlying integration AND with both being incidentally correlated via task structure (prompts that humans find "harder to integrate" may also drive CLM to higher-variance hidden states for unrelated reasons).

---

## §8 raw compliance summary

- **POLICY R4**: Paradigm B is Phase 3 entry, NOT inserted into Phase 2 baseline. Current `state/p9_sft_spec_2026_05_02/loss_design.json` 4-loss family unchanged this cycle.

---

## §9 Decision points (for future cycle)

1. **Q-decision**: Is Paradigm B worth Phase 3 entry given Paradigm A delivers measurable BOLD MSE convergence in post-P0? — gate via §6.3 decision tree.
2. **Q-dataset**: ZuCo (TOP-1) sufficient or also need Inner Speech as calibration? — recommend BOTH for held-out generalization.
3. **Q-metric**: Sample-partition φ (§1.3) only, or include gamma coherence (§1.1) as secondary? — recommend BOTH; sample-partition for primary loss, gamma coherence as auxiliary monitor.
4. **Q-alignment**: Window strategy 1 (centered) vs 3 (N400-locked)? — start strategy 1, ablate to 3 in pilot.
5. **Q-d_φ**: scalar (1) or partition vector (8) for projection output? — start scalar for simplicity, scale to vector if signal supports.

---

**status**: P9_PARADIGM_B_EEG_PHI_PROXY_2026_05_03_LOCAL_DRAFT
**verdict_key**: SPEC_READY · PHASE_3_GATED · NO_TOOL_THIS_CYCLE · PREREQ_LIST_DEFINED
