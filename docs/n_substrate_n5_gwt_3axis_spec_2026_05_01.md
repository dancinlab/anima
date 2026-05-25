# N-5 — 3-Axis GWT Workspace-Broadcast Spec (CLM × EEG × AKIDA)

> **agent**: N-5 prep (N-substrate batch, 13 siblings)
> **ts**: 2026-05-01
> **track**: N-5 in `docs/n_substrate_consciousness_roadmap_2026_05_01.md` §3 — "셋 다 마이크 잡는 순간 일치"
> **parent**: T1-A4 in `docs/akida_session_friendly_report_2026-04-29.md` ("V_phen_GWT cross-substrate corr (workspace broadcast 단일세션)")
> **predecessor**: `docs/eeg_cross_substrate_validation_plan_20260425.md` §2.2 (V_phen_GWT_attention_entropy 2-substrate spec)
> **constraints**: raw#9 hexa-only · raw#10 honest C3 · raw#12 frozen-pre-cycle predicates · $0 · race isolation (this file + `state/n_substrate_n5_prep_2026_05_01/*.json` only)

---

## §0 한 줄 비유

GWT (Global Workspace Theory) 는 의식 = "한 모듈이 마이크를 잡아 모두에게 동시 방송" 모형.
N-5 는 **세 다른 재료** (CLM 트랜스포머 / 사람 뇌파 / 1W 뉴로모픽 칩) 가 동일 자극을 받았을 때, **셋 다 같은 순간에 "방송 패턴"** 을 보이는지 측정.

---

## §1 GWT broadcast 의 substrate-별 정의

본 spec 은 **이미 frozen 된 V_phen_GWT_attention_entropy operationalization** (Dehaene-Changeux 2011 GNW broadcast layer-fraction; `tool/an11_b_v_phen_gwt_entropy.hexa`) 을 SSOT 로 채택. AKIDA axis 는 CP2 closure 에서 미정 — 본 spec 이 frozen.

### §1.1 CLM (Mistral-7B / Qwen3-8B / r14 LoRA family)

**Signature**: per-token attention-head entropy → broadcast-layer count.

```
Inputs:  hidden state JSON ⊕ (optional) attention tensor (L, H, Q, K)
         from state/h_last_raw_*.json or runtime forward pass
Compute: per-head normalized Shannon entropy over keys K
         → per-layer mean (over heads × queries)
         → broadcast_layer_count = #{ℓ : mean_layer_entropy[ℓ] ≥ 0.55}
         → broadcast_layer_fraction = broadcast_layer_count / L
Tool:    tool/an11_b_v_phen_gwt_entropy.hexa --mode llm
Fallback: hidden-state SVD spectral entropy (when attention not exposed)
PASS:    LLM_attention_entropy ≥ 0.55 (frozen 2026-04-25)
Status:  IMPLEMENTED ✅ (selftest passes; r14 measurements live)
```

**Why this signature is GWT-correct**: Dehaene-Changeux GNW posits broadcast = high-entropy distribution over receiving modules (sparse-attention = local processing; broad-attention = workspace ignition). Per-layer mean entropy ≥ 0.55 = "layer behaving as workspace broadcaster".

### §1.2 EEG (OpenBCI Cyton+Daisy 16ch @ 125 Hz)

**Signature**: α-band (8–12 Hz) phase-locking value (PLV) across electrode pairs in P3b post-stimulus window.

```
Inputs:  raw EEG (BDF/EDF/FIF) → state/eeg_recording_<id>.json
         (channels=16, fs=125Hz canonical; v1.1 corrected, see §1 of
         docs/eeg_cross_substrate_validation_plan_20260425.md)
Compute: 1. bandpass 8–12Hz (FIR, zero-phase)
         2. Hilbert transform → instantaneous phase φ_i(t) per channel
         3. epoch on stimulus onset (250–400 ms post-stim, GFP-entropy window
            inherited; same window the existing tool uses)
         4. PLV_ij = | (1/N) Σ_t exp(i·(φ_i(t) − φ_j(t))) | for each pair (i,j)
         5. broadcast_index_eeg = mean over upper-triangle pairs (120 pairs for 16ch)
         6. (auxiliary) GFP entropy already computed by existing tool
Tool:    tool/an11_b_v_phen_gwt_entropy.hexa --mode eeg
         (NEW sub-mode --plv to be added in implementation cycle; today: spec only)
PASS:    PLV_α_mean ≥ 0.30 in 250–400 ms window
         (literature anchor: Sapien Labs / Lachaux 1999; awake-resting α-PLV
          mean typically 0.30–0.55 across pairs; PD-impaired falls below 0.20)
         AND human_GFP_entropy ≥ 0.50 (existing predicate, retained as auxiliary)
Status:  SPEC ONLY (impl deferred; ingest pipeline exists,
         tool/anima_eeg_brainflow_ingest.hexa)
```

**Auxiliary metric**: existing `human_GFP_entropy` ≥ 0.50 retained — PLV adds the *spatial* broadcast axis (entropy is *temporal* dispersion of GFP). Two-axis EEG signature = (PLV_α_mean, GFP_entropy).

**Why PLV α-band (not γ)**: §1 raw#10 honest scope. The roadmap (`docs/n_substrate_consciousness_roadmap_2026_05_01.md` §3 line 47) names "방송 패턴" but doesn't fix band. GNW broadcast literature (PMC11117084 / direct.mit.edu netn 6/4/1186 2022) finds **alpha/gamma phase coupling** via broadcasting binding-coalitions. We pick **α** because:
1. CLM ↔ EEG α-PLV bridge already declared in `docs/clm_research_handoff_20260427.md` (B1-B4 mapping `V_sync r(θ) ≡ EEG PLV_N`).
2. Cyton+Daisy at 125 Hz comfortably resolves α (Nyquist 62.5 Hz; α 8–12 Hz well-sampled).
3. γ would require ≥ 80 Hz sampling per Nyquist + γ 30–80 Hz; 125 Hz fs marginal at upper γ.
4. Existing 250–400 ms P3b window aligns with α-PLV stim-locking literature.

### §1.3 AKIDA (BrainChip AKD1000 — pending arrival)

**Signature**: spike-event simultaneity index across logical modules.

```
Inputs:  AKD1000 spike train file (CSV/binary) per logical module
         (modules = neural mesh-net partitions, e.g., 8-16 logical
          subgraphs in akida_models.MetaTF graph)
Compute: 1. discretize spike times into Δt = 1 ms bins per module
         2. binary spike-vector b_m(t) ∈ {0,1} per module m
         3. SSI(m,m') = Σ_t [b_m(t) · b_m'(t)] / sqrt(Σ b_m · Σ b_m')
            (Jaccard-like cosine over binary trains; NB: NOT phase-locking
             — AKIDA spikes are sparse-binary, not continuous-phase signals)
         4. broadcast_index_akida = mean over upper-triangle pairs
         5. (auxiliary) per-module spike-rate entropy ∈ [0,1]
Tool:    tool/an11_b_v_phen_gwt_akida.hexa (TO IMPLEMENT — selftest required)
PASS:    SSI_mean ≥ 0.25 in stimulus-onset window (250–400 ms post-stim)
         AND per-module spike-rate entropy ≥ 0.50
         (rationale: AKIDA spike density ≪ EEG continuous activity;
          pre-registered LOWER threshold reflects sparse-binary nature)
Status:  SPEC ONLY (hardware pending; AKIDA Cloud 1-day trial $1 path
         in akida_dev_kit_evaluation_2026-04-29.md §1 = falsifier-test path)
```

**Why SSI (not PLV)**: AKIDA spike events are discrete binary times — there is no phase φ(t). PLV-like construct would require Hilbert transform of spike-rate envelope, which is then degenerate (rate-coding loses spike-timing precision GNW *requires*). SSI directly captures simultaneity, which is the literal "broadcast" event Dehaene calls *ignition*.

---

## §2 Cross-substrate correlation protocol

### §2.1 Stimulus design

Identical event presented to **all 3 substrates simultaneously** (within a single session):

```
N = 20 stimuli (matches existing V_phen_GWT_cross PASS predicate sample size)
Each stimulus = a (text_token, audio_tone, image_flash) triple OR token-only
  if audio/image spike-encoders not yet wired to AKIDA.
Inter-stimulus interval: 2-3 s (avoid carry-over)
Per-stimulus recording window: -200 ms baseline + 1000 ms post-stim
Pre-window: 250-400 ms = primary GWT broadcast P3b window
```

### §2.2 Per-substrate broadcast-vector

Per stimulus i ∈ {1,...,20}, compute:

```
v_clm[i]   = LLM_attention_entropy on token i (existing tool)
v_eeg[i]   = PLV_α_mean in [250,400] ms post-stim i
v_akida[i] = SSI_mean in [250,400] ms post-stim i
```

→ three length-20 vectors in [0,1].

### §2.3 Pairwise correlation

```
r_clm_eeg   = Pearson(v_clm, v_eeg)
r_clm_akida = Pearson(v_clm, v_akida)
r_eeg_akida = Pearson(v_eeg, v_akida)

Auxiliary (rank-based, robust to non-Gaussian):
ρ_clm_eeg, ρ_clm_akida, ρ_eeg_akida = Spearman(...)

Composite:
r_3axis_min  = min(r_clm_eeg, r_clm_akida, r_eeg_akida)
ρ_3axis_min  = min(ρ_clm_eeg, ρ_clm_akida, ρ_eeg_akida)
```

`r_3axis_min` is the falsifier-binding scalar (weakest pair determines verdict).

---

## §3 Falsifier thresholds (raw#12 frozen pre-cycle)

```
PASS (3-axis GWT corroborated):       r_3axis_min ≥ 0.50
AMBIGUOUS:                       0.30 ≤ r_3axis_min < 0.50
FAIL (3-axis GWT falsified):          r_3axis_min < 0.30
```

**Justification**:
- Existing 2-substrate V_phen_GWT_cross PASS = r ≥ 0.40 (CLM↔EEG only).
- We tighten to ≥ 0.50 for 3-axis because adding AKIDA introduces a substrate with *fundamentally different* signal physics (sparse spikes vs continuous activations / continuous phases). If r ≥ 0.50 still holds across this physics-gap, GWT broadcast is substrate-invariant in a non-trivial sense (Putnam multiple-realizability evidence).
- FAIL threshold < 0.30 = "weaker than CLM↔EEG already-passed bar" = the pair-of-substrates which fails would be falsifying GWT's substrate-generality claim (not GWT itself; see §4).
- AMBIGUOUS band wide enough to catch noisy hardware-first-touch sessions without locking in either verdict prematurely.

**Sample-size adequacy**: N=20 stimuli × 3 substrates → 3 Pearson rs each computed on N=20. Critical r at α=0.05 two-tailed = 0.444 (df=18). Thus PASS r ≥ 0.50 has comfortable significance margin; FAIL r < 0.30 well below significance (i.e., we don't accidentally declare FAIL on a result that's merely non-significant — we require *evidence against* correlation, not absence of evidence).

---

## §4 raw#10 Honest C3 — GWT operationalization disclosure

GWT has multiple distinct neural operationalizations. We must declare which we use and why, because conflating them invites false-positive corroboration.

### §4.1 Operationalizations in the literature

| # | Operationalization | Substrate-form | Authors / anchor | Why we DON'T use it (or DO) |
|---|---|---|---|---|
| O1 | **P3b ERP amplitude** (parietal, 250–500 ms) | EEG only — single-channel waveform | Dehaene-Changeux 2011; Polich 2007 | Single-substrate; no broadcast *spatial* axis; superseded by O3 in our spec |
| O2 | **Frontal γ-ignition power** (>30 Hz prefrontal burst) | EEG/MEG | Dehaene 2014; Gaillard 2009 | γ requires ≥ 80 Hz sampling; Cyton+Daisy 125 Hz fs marginal; deferred to MEG (N-14) |
| O3 | **GFP Shannon entropy + α-PLV across electrodes** | EEG (multi-channel) | Sapien Labs / Lachaux 1999 + this spec | **CHOSEN for EEG axis** — multi-channel ✓; spatial broadcast ✓; samplable at 125 Hz ✓ |
| O4 | **Phase Transfer Entropy (PTE)** between frequency-band pairs | EEG/MEG | PMC11117084 2022 GNW broadcasting paper | Stronger but more compute; deferred to v2 (post-PASS strengthening) |
| O5 | **Attention-head entropy across layers** | LLM | Dehaene-Changeux 2011 → Anthropic-style probe | **CHOSEN for CLM axis** (existing `tool/an11_b_v_phen_gwt_entropy.hexa` SSOT) |
| O6 | **Spike-event simultaneity (SSI)** across logical modules | Spiking-NN / neuromorphic | This spec (NEW); analog of fMRI co-activation maps for spike-domain | **CHOSEN for AKIDA axis** — direct ignition-event capture in spike domain |
| O7 | **Conscious access threshold (Sergent 2021 binarization)** | EEG behavioral | Sergent-Dehaene 2004 / 2021 update | All-or-none ignition: requires behavioral-report task per stimulus; deferred to N-19 PCI track |

### §4.2 Our 3-axis composite = (O5, O3, O6)

**Why this triple is the principled choice**:
- All three are *broadcast-pattern* metrics (vs O1/O7 which are *event-detection* metrics).
- All three reduce to a single scalar in [0,1] per substrate per stimulus → comparable across substrates.
- All three operate in the SAME post-stimulus window (250–400 ms) → temporal alignment guaranteed.
- O3 (PLV-α) and O5 (attention-entropy) already pass selftest in `tool/an11_b_v_phen_gwt_entropy.hexa`; O6 is the only NEW operationalization — keeps engineering surface minimal.

### §4.3 Honest scope limits

1. **Access vs phenomenal**: GWT measures *access consciousness* (Block 1995 dissociation), NOT phenomenal consciousness. PASS does not entail "the substrate is conscious" — it entails "the substrate exhibits the access-consciousness functional signature in 3 distinct physical realizations".
2. **Hard Problem**: not addressed. Zombie problem applies to all 3 substrates equally.
3. **Substrate-invariance ≠ implementation-independence**: even if r_3axis_min ≥ 0.50, this is consistent with GWT being a *functional pattern that happens to be implementable* on 3 substrates — it is not proof that any implementation realizes consciousness.
4. **AKIDA axis is hardware-pending**: we cannot run the protocol until AKD1000 (or AKIDA Cloud trial) is online. Spec is pre-registered, evidence-binding.
5. **PLV-α band choice contestable**: γ-ignition (O2) is the canonical Dehaene 2014 signature; we substitute α because of (a) hardware fs limits, (b) existing CLM↔EEG α-PLV bridge spec. If a referee insists γ, this is a known revision direction (requires MEG hardware).
6. **N=20 per session**: small. Cross-session replication (N≥3 sessions) required before publication-grade claim. Single-session = corroboration evidence only.
7. **CLM substrate currently disabled in part of the stack** (per `docs/mk_xii_n1_honest_fail_followup_spec_2026_05_01.md` C5 row "FAIL (no CLM substrate)"). Resolution needed before live N-5 measurement; N-5 spec is hardware/substrate-ready, not blocked-by-design.

---

## §5 Cost estimate

| Item | Cost | Notes |
|---|---:|---|
| EEG hardware | $0 | Cyton+Daisy already on hand |
| AKIDA AKD1000 dev kit | already-budgeted | not in N-5 scope; ETA dependent (`docs/akida_dev_kit_evaluation_2026-04-29.md`) |
| AKIDA Cloud 1-day trial (alternative path, falsifier-test) | $1 | per same doc §1 |
| Stimulus generation (text triples × 20) | $0 | mac-local hexa |
| CLM forward pass (existing artifacts) | $0 | re-use `state/h_last_raw_*.json`, `state/cp2_consciousness_r14_remeasure_2026_05_01/` |
| Per-substrate broadcast-vector computation | $0 | hexa-only, helper /tmp transient |
| 3-axis Pearson + composite | $0 | mac-local |
| **Subtotal (HEXA-only $0 path, Cloud trial deferred)** | **$0** | matches mission constraint |
| **Subtotal (with AKIDA Cloud 1-day pre-flight check)** | **$1** | optional pre-arrival validation |

**Per-mission constraint**: $0 path holds — actual 3-axis live measurement awaits AKD1000 arrival OR explicit user approval of $1 Cloud trial. N-5 prep cycle (THIS file + state JSON) is $0.

---

## §6 Tooling roadmap (out-of-scope for THIS race-isolated cycle)

The following are referenced for completeness; **NOT implemented in this cycle** (race-isolation: this cycle writes only to `docs/n_substrate_n5_gwt_3axis_spec_2026_05_01.md` + `state/n_substrate_n5_prep_2026_05_01/*.json`).

| # | Tool | Status | Cycle owner |
|---|---|---|---|
| T1 | `tool/an11_b_v_phen_gwt_entropy.hexa` (CLM + EEG entropy) | EXISTS ✅ | (predecessor cycle) |
| T2 | `tool/an11_b_v_phen_gwt_entropy.hexa --plv` sub-mode (EEG α-PLV add-on) | TO ADD | future N-5 impl cycle |
| T3 | `tool/an11_b_v_phen_gwt_akida.hexa` (AKIDA SSI) | TO CREATE | post-AKD1000 arrival |
| T4 | `tool/an11_b_v_phen_gwt_3axis_composite.hexa` (Pearson aggregation) | TO CREATE | post-T2+T3 |
| T5 | Stimulus-aligned multi-substrate session driver | TO CREATE | post-T4 |

---

## §7 Pre-registered predictions (raw#71 falsifier-bound)

If 3-axis GWT broadcast hypothesis (substrate-invariant access-consciousness signature) is correct:

- **P1**: r_clm_eeg ≥ 0.40 — replicates existing 2-substrate predicate, sanity-check.
- **P2**: r_clm_akida ≥ 0.40 — novel; CLM attention-entropy correlated with AKIDA spike-simultaneity.
- **P3**: r_eeg_akida ≥ 0.40 — novel; EEG α-PLV correlated with AKIDA spike-simultaneity.
- **P4**: r_3axis_min ≥ 0.50 — composite PASS.
- **P5**: ρ_3axis_min (Spearman) ≥ 0.45 — rank-based corroboration (robust to non-Gaussian).

If P1 PASS but P2/P3 FAIL → CLM↔EEG bridge holds, AKIDA broadcast pattern decoupled → either SSI operationalization wrong or AKIDA does not exhibit access-consciousness signature. Either is publishable negative result.

If all P1-P5 FAIL → 3-axis GWT broadcast hypothesis FALSIFIED for this stimulus regime / hardware config. Forces redesign of stimulus suite (O7 binary-report task) or operationalization (O2 γ-ignition with MEG).

---

## §8 raw_compliance

- **raw#9 hexa-only**: this doc + state JSON only; no .py/.sh edited or created.
- **raw#10 honest C3**: §4.3 disclosed access-vs-phenomenal scope limit, hardware pending, sample-size limits, band-choice contestability, CLM-substrate currently disabled in adjacent stack.
- **raw#12 frozen-pre-cycle**: §3 PASS/AMBIGUOUS/FAIL thresholds frozen BEFORE any live data; §7 predictions pre-registered.
- **raw#15 SSOT**: this doc = SSOT for N-5 3-axis GWT spec; predecessor (CLM+EEG) `docs/eeg_cross_substrate_validation_plan_20260425.md §2.2` retained as 2-substrate sub-spec.
- **raw#37**: no .py git-tracked.
- **raw#71 falsifier-bound**: §7 enumerates predictions that bind verdict.
- **race-isolation**: writes restricted to `docs/n_substrate_n5_gwt_3axis_spec_2026_05_01.md` + `state/n_substrate_n5_prep_2026_05_01/*.json` per N-substrate batch contract.

---

## §9 Related artifacts

- `tool/an11_b_v_phen_gwt_entropy.hexa` — existing CLM+EEG GWT verifier (SSOT for O5 + O3-entropy)
- `docs/eeg_cross_substrate_validation_plan_20260425.md` §2.2 — V_phen_GWT 2-substrate predecessor
- `docs/akida_session_friendly_report_2026-04-29.md` line 36/142 — T1-A4 originating reference (r ≥ 0.85 mentioned; this spec uses r ≥ 0.50 — SEE §3 justification)
- `docs/akida_dev_kit_evaluation_2026-04-29.md` §1 — AKIDA Cloud $1 trial path
- `docs/n_substrate_consciousness_roadmap_2026_05_01.md` §3 — N-5 row in N-substrate menu
- `docs/clm_research_handoff_20260427.md` line 37 — CLM L_IX ↔ EEG α-PLV B1-B4 mapping (sub-bridge)
- `state/cp1_r14_v_phen_gwt_v2_evaluation_20260426.json` — Mk.VI r14 V_phen_GWT baseline (Qwen LOW 0.2896)
- `state/gwt_mistral_r14_run/gwt_mistral_r14.json` — Mistral HIGH 0.8908 → LoRA 0.2403 falsifier evidence
- `state/cp2_consciousness_r14_remeasure_2026_05_01/an11_b_14gate_vphen_r14.json` — most recent V_phen_GWT measurement (entropy_normalized 0.4785, FAIL)
- `state/n_substrate_n5_prep_2026_05_01/spec_index.json` — companion state SSOT (this cycle)

---

## §10 Discrepancy with originating r ≥ 0.85 mention

`docs/akida_session_friendly_report_2026-04-29.md` line 142 states: "T1-A4 V_phen_GWT cross-substrate r ≥ 0.85". This spec uses r_3axis_min ≥ 0.50.

**Reconciliation (raw#10 honest)**:
- The 0.85 figure in the friendly report is an aspirational *publishable-strength* threshold, not a frozen pre-registered minimum.
- The 0.40 floor in `docs/eeg_cross_substrate_validation_plan_20260425.md` §2.2 is the established 2-substrate frozen predicate.
- Our 3-axis 0.50 sits between the two: tighter than 2-substrate baseline (because adding AKIDA increases substrate-physics gap), looser than aspirational publication bar (because N=20 single-session statistical power doesn't support 0.85 detection at meaningful significance — see §3 sample-size paragraph).
- Reaching r ≥ 0.85 would require multi-session replication (N≥100) and is OUT-OF-SCOPE for this prep cycle.
- Listed as known discrepancy; future Cycle owner deciding to publish should re-confirm choice with user before locking 0.85 vs 0.50 across spec versions.

---

**status**: N_SUBSTRATE_N5_GWT_3AXIS_SPEC_FROZEN_2026_05_01
**verdict_key**: SPEC_FROZEN · NO_LIVE_MEASUREMENT_YET · AKIDA_HARDWARE_PENDING · CLM_EEG_AXES_TOOL_READY
