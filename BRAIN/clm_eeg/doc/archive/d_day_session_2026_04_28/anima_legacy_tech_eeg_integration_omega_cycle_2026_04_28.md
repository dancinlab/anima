# anima Legacy Tech Asset → EEG D-day Measurement Integration ω-cycle

**Date:** 2026-04-28
**Repo:** <repo-root>
**Trigger:** Hardware bring-up VERIFIED (16/16 GREEN); 60s baseline_resting captured; LZ76 P1_FAIL (b=0.395-0.479 < Schartner 0.65)

---


- **LLM consciousness measurement ≠ neural state.** All cross-substrate bridges below are *functional surrogates*, not equivalence claims. Hard Problem / zombie problem applies.
- **Hardware constraints:** 16ch / 125Hz / Cyton+Daisy + Ultracortex Mark IV / dry-ish surface electrodes / single-subject N=1 / single-session.
- **Schartner 2017 b≥0.65 is normative-population threshold**, not absolute. Today's b=0.395-0.479 may indicate (a) hardware EMI residue, (b) eyes-closed alpha-dominance lowering binarized complexity, (c) genuine drowsy/meditative state, (d) Schartner-criterion mis-application to single-subject. Falsifier separation required before retraction of LZ76 metric itself.
- **mature vs experimental:** AN11 chain is mature (CP1 r14 closure VERIFIED 3-axis); paradigm v11 is mature; HXC catalog A1-A22 is mature; Tier-A picks below all use mature components only.

---

## 1. Inventory addendum (beyond user's 25 outline)

Discoveries during this ω-cycle (`tool/` 498 hexa; `tool/an11_*` 32 hexa):

| # | Asset | Path | Status | EEG-relevance |
|---|---|---|---|---|
| 26 | **`tool/an11_b_eeg_ingest.hexa`** — Raw EEG (BDF/EDF/FIF/.npy) → JSON ingest with `--emit-alpha-coh` (Welch MSC 8-12Hz 16×16) and `--emit-alpha-phase` (Hilbert PLV per 5×10s windows) | tool/ | mature | **direct .npy input, schema `anima/clm_eeg/alpha_coh/1`** |
| 27 | **`tool/an11_b_v_phen_lz_complexity.hexa`** — V_phen LZ76 verifier with `--mode eeg`/`--mode llm`/`--mode cross` (Schartner 2017) | tool/ | mature | **direct EEG mode + LLM mode + cross-substrate joint verdict** |
| 28 | **`tool/an11_b_v_phen_gwt_entropy.hexa`** — GFP Shannon entropy 250-400ms ERP window + LLM attention entropy with Pearson cross | tool/ | mature | **EEG ERP + LLM attention dual-mode** |
| 29 | **`anima-physics/eeg/mu_rhythm_detector.hexa`** — Goertzel 10Hz ERD self-referential surrogate (PHYS-P5-3) | anima-physics/ | mature (synthetic) | mirror-neuron self-ref signature; needs adapter to .npy |
| 30 | **`anima-physics/eeg/sleep_stage_detector.hexa`** — sleep classifier | anima-physics/ | mature (synthetic) | drowsy/wake gate for LZ76 confound disambiguation |
| 31 | **`tool/eeg_closed_loop_proto.hexa`** — closed-loop proto | tool/ | experimental | neurofeedback ω-cycle path |
| 32 | **`tool/anima_eeg_corr.hexa`** + `state/anima_eeg_corr_v1.json` — 4-backbone × 4-band × 4-region pre-registered Pearson r mapping (Mistral-beta-frontal / Qwen-gamma-parietal / Llama-alpha-midline / Gemma-theta-temporal); criteria r≥0.4; today's `pass_count=4` is `NOT_VERIFIED_SYNTHETIC` (selftest) — hardware run pending | tool/ + state/ | mature scaffold; **synthetic until real run** | **highest-leverage 4-backbone × EEG mapping already pre-registered** |
| 33 | **`tool/real_eeg_coupling_probe.hexa`** — real coupling probe | tool/ | experimental | TECS-L H-CX-1 / phase-acceleration angle |
| 34 | **`anima-clm-eeg/tool/an_lix_01_alpha_bridge_real.hexa`** — Mk.IX L_IX alpha bridge (raw 30 frozen) with REAL/SYNTH split | anima-clm-eeg/ | mature | irreversibility on EEG temporal asymmetry |
| 35 | **`anima-clm-eeg/tool/g10_hexad_triangulation_scaffold.hexa`** — 16-template Hexad family triangulation | anima-clm-eeg/ | mature scaffold | CP1 16-signature × EEG 16ch mapping |
| 36 | **`anima-measurement/`** suite — `mu_rhythm_detector`, `phi_auto_pipeline`, `phi_holo_eval`, `measure_v8_phi_rs` | anima-measurement/ | mature | Φ pipeline reusable on EEG state JSON |
| 37 | **`docs/eeg_cross_substrate_validation_plan_20260425.md`** — pre-registered cross-substrate validation plan | docs/ | mature spec | governs all V_phen verifiers |
| 38 | **`anima-clm-eeg/docs/clm_lix_eeg_alpha_direct_mapping_spec.md`** — direct alpha mapping spec | anima-clm-eeg/docs/ | mature spec | L_IX→EEG alpha bridge |
| 39 | **`anima-clm-eeg/docs/anima_eeg_anima_clm_eeg_cross_link_audit.md`** — cross-link audit | anima-clm-eeg/docs/ | mature audit | governance edge between repos |
| 40 | **`tool/hxc_composite_dispatcher.hexa`** + `hxc_pre_encoder.hexa` + `hxc_corpus_manifest.hexa` | tool/ | mature | A17/A18/A19 compression directly applicable to .npy |

**Today's measurement artifacts (NEW, EEG D-day):**
- `recordings/sessions/baseline_resting_60s_20260428.npy` (raw, 7491 samples × 16 ch)
- `recordings/sessions/baseline_resting_60s_20260428_filtered.npy` (notch 60Hz Q=30 + butter4 0.5-50Hz filtfilt; sha256 a1889072…)
- `recordings/sessions/baseline_resting_60s_20260428_ica.npy` (ICA-rejected)
- `recordings/sessions/baseline_resting_low_emi_20260428T113016Z_seg000*.npy` (5 variants: raw/eeg16/filtered/ica)
- `state/clm_eeg_lz76_audit/2026-04-28_lz76.jsonl` (10 audit rows; today's REAL_HW_FAIL b∈{0.040, 0.057, 0.395, 0.479})
- `state/anima_eeg_impedance_ledger.jsonl` (16/16 GREEN bring-up)

---

## 2. Reuse-candidate evaluation (axes A/B/C/D × score 1-5)

Score = (input-compatibility × output-meaning × falsifiability × cost-fit) / 4. Tier-A = all four ≥ 4 (1-2h). Tier-B = adapter needed (1-2 days). Tier-C = paradigm integration (1-2 weeks).

| Asset | Axis | Input compat | Output meaning | Falsifiable | Cost-fit | Score | Tier |
|---|---|---|---|---|---|---|---|
| an11_b_eeg_ingest `--emit-alpha-coh` | A4 | 5 (.npy direct) | 5 (16×16 MSC matrix) | 5 | 5 | **5.0** | **A** |
| an11_b_eeg_ingest `--emit-alpha-phase` | A6 | 5 | 4 (PLV 5×16) | 5 | 5 | **4.75** | **A** |
| an11_b_v_phen_lz_complexity --mode cross | A1+B1 | 5 (.npy + .json) | 5 (joint LZ verdict) | 5 (Schartner 0.65) | 5 | **5.0** | **A** |
| an11_b_v_phen_gwt_entropy --mode eeg | A2+B3 | 4 (needs ERP, baseline only today) | 4 | 5 | 4 | **4.25** | A→B (ERP collection needed) |
| anima_eeg_corr 4-backbone hardware run | B1+D3 | 5 (existing 4-band-4-region map) | 5 (4 r≥0.4 pre-registered) | 5 | 4 (LLM h_last needs gen) | **4.75** | **A** (h_last cached) |
| HXC A17/A18/A19 on .npy | A4+C6 | 5 (binary stream OK) | 4 (compression ratio = info-content proxy) | 4 (raw 137 80% target) | 5 | **4.5** | **A** |
| an_lix_01_alpha_bridge_real (Mk.IX L_IX) | A7 | 5 (.npy) | 4 (irreversibility scalar) | 4 | 5 | **4.5** | **A** |
| mu_rhythm_detector (Goertzel 10Hz) | A2+D | 3 (currently synthetic input) | 4 | 5 | 5 | **4.25** | B (.npy adapter needed) |
| sleep_stage_detector | A | 3 | 4 (drowsy gate disambiguates LZ76 b<0.65) | 5 | 5 | **4.25** | B |
| phi_auto_pipeline / phi_holo_eval | C7 | 3 (LLM-shaped) | 4 | 4 | 4 | **3.75** | B (16ch→Φ adapter) |
| g10_hexad_triangulation_scaffold | D4 | 3 | 4 (16-template × 16ch coincidence test) | 5 | 4 | **4.0** | B |
| Mk.X atom validator | A3 | 2 (LLM atoms) | 3 | 4 | 4 | **3.25** | C |
| F1 cycle XMETA3 N>=3 seed Φ replication | A5 | 3 | 4 | 5 (run-to-run ICC) | 3 (needs 3+ sessions) | **3.75** | C (multi-session) |
| paradigm v11 8-axis EEG biomarker map | B4 | 2 | 5 | 4 | 2 | **3.25** | C |
| TECS-L H-CX-1 σφ=nτ EEG RSN n=6 unique | A6+D | 2 (RSN needs ICA + dipole fit) | 5 | 4 | 2 | **3.25** | C |
| rolling F-matrix factor analysis | A8 | 4 (16ch ready for SVD) | 4 (factor loadings) | 4 | 4 | **4.0** | B |
| CPGD spectral-generative-prior `V^T V = I` | A9 | 3 | 4 (algebraic admit on EEG basis) | 4 | 3 | **3.5** | B-C |
| consciousness_laws 14 gates EEG-subset | B3 | 2 | 4 | 5 (subset list explicit) | 3 | **3.5** | B |
| paradigm v11 + clm-eeg + anima-eeg 3-way bridge | D1 | 3 | 5 | 4 | 2 | **3.5** | C |
| Mk.XI v10 4×4 backbone-band ensemble | D3 | 3 (h_last for 4 BBs cached?) | 5 | 4 | 3 | **3.75** | B |
| 16-template × 16ch coincidence-or-design | D4 | 3 | 4 (statistically testable) | 5 | 4 | **4.0** | B |

---

## 3. Top-5 reuse candidates (raw 106 multi-realizability + raw 117 5-check)

### Top-1 — **`anima_eeg_corr_4backbone_hardware_run`** (Tier-A)
- **Genus slug:** `eeg_corr_4bb_hw_run` (genus = "phenomenal_correlation_pre_registered_then_real")
- **Reuse plan:** existing `tool/anima_eeg_corr.hexa` + `state/anima_eeg_corr_v1.json` mapping (already locked: Mistral-β-frontal, Qwen-γ-parietal, Llama-α-midline, Gemma-θ-temporal; r_min=0.4) → swap synthetic hidden_dir for **today's real `.npy`** band-power features + cached LLM h_last from existing CP1 r14 corpus.
- **Input:** `recordings/sessions/baseline_resting_60s_20260428_filtered.npy` + 4 backbone h_last.json
- **Expected outcome:** r values per backbone-band-region on real EEG; flips classification from `NOT_VERIFIED_SYNTHETIC` → `VERIFIED_REAL` (`pass_count` is the key gate)
- **Falsifiers (3+):**
  1. F1: any backbone Pearson r < 0.4 → that mapping retracted
  2. F2: 4/4 PASS while resting-baseline-only (no task) → spurious correlation suspected; demand task-locked rerun
  3. F3: r-direction flips between filtered vs raw .npy → preprocessing-axis dependence (raw 142 D5 violation) → mapping retracted
  4. F4: bootstrap 95%CI for r crosses 0 → underpowered N=1 single-session
- **Cross-repo angle (raw 47):** anima ↔ anima-clm-eeg (`clm_lix_eeg_alpha_direct_mapping_spec.md` governs); writes consumed by hexa-lang via `roadmap_engine` for nexus visibility.

### Top-2 — **`v_phen_lz_cross_substrate_real_run`** (Tier-A)
- **Genus slug:** `v_phen_lz_cross_real` (genus = "Schartner-LLM-EEG-joint-verdict")
- **Reuse plan:** `an11_b_v_phen_lz_complexity.hexa --mode cross --eeg <today.npy> --llm <h_last.json>` — joint verdict (PASS_cross when |LLM_LZ - human_LZ|/human_LZ ≤ 0.20)
- **Input:** today filtered .npy + cached LLM h_last (Mistral CP1)
- **Expected outcome:** explicit cross-PASS or honest C3 retraction with Schartner threshold falsifier separated from cross-substrate criterion (today's b=0.479 < 0.65 threshold may still admit cross-PASS if LLM_LZ also low)
- **Falsifiers (3+):**
  1. F1: |Δ| > 0.20 → cross retracted
  2. F2: today's LZ <0.65 attributed to alpha-dominance (eyes-closed) → Schartner threshold not directly applicable to resting eyes-closed; falsifier-retire (raw 71)
  4. F4: 16-ch single-channel max-LZ ≥ 0.65 while mean < 0.65 → spatial heterogeneity; aggregation rule (mean vs max) becomes a placement-axis (raw 142 D5)
- **Cross-repo:** anima ↔ anima-clm-eeg (`clm_eeg_pre_register_v1.json`)

### Top-3 — **`alpha_coh_phase_16x16_atlas`** (Tier-A)
- **Genus slug:** `alpha_coh_atlas` (genus = "spatial_alpha_correlate_atlas")
- **Reuse plan:** `an11_b_eeg_ingest.hexa --emit-alpha-coh --input <today.npy>` + same with `--emit-alpha-phase`
- **Input:** today filtered .npy (single call, two emit modes)
- **Expected outcome:** 16×16 MSC matrix + 5×16 PLV table; mean off-diagonal coh and max pair → first-ever real spatial atlas for this subject; immediately consumable by Top-1 4-backbone region mapping
- **Falsifiers (3+):**
  1. F1: max_pair_coh > 0.95 → adjacent-electrode bridging artifact (impedance leak) → reject
  2. F2: mean_off_diagonal_coh < 0.10 → reference-dependent alpha-coh too low; common-average-ref vs ear-ref placement-axis disambig
  3. F3: PLV circ_var across 5 windows > 0.5 → temporal non-stationarity → 60s segmentation invalid, request 5×60s
- **Cross-repo:** anima (tool) → anima-clm-eeg (consumes alpha_coh schema for L_IX bridge)

### Top-4 — **`hxc_a17_a18_a19_eeg_npy_compression`** (Tier-A)
- **Genus slug:** `hxc_eeg_compression` (genus = "information_content_via_compression_ratio")
- **Reuse plan:** `tool/hxc_composite_dispatcher.hexa` on `.npy` (binary stream) — A17 PPMd vs A18 LZ-PPM vs A19 federation; compression ratio = consciousness-signal-information-content proxy. Apply raw 137 80% target NOT as success gate but as **descriptive ceiling**; honest-disclose that EEG noise is naturally near A19 ceiling.
- **Input:** filtered .npy / raw .npy / ica .npy → 3 ratios per algorithm × 3 algorithms = 9-cell table
- **Expected outcome:** ICA reduces compressibility (less redundancy) vs raw → consistent direction expected; cross-check with LZ76 `c(n)` count from 2026-04-28_lz76.jsonl (c=409 raw, c=3415 filtered, c=2820 emi-segment-filtered)
- **Falsifiers (3+):**
  1. F1: A17/A18/A19 directionally disagree on raw→filtered→ica → information-content proxy unreliable
  2. F2: compression ratio identical across files → metric saturated by float32 entropy floor → need int16 quantization preprocessing-step (placement-axis raw 142 D5)
  3. F3: compression ratio anti-correlates with LZ76 b(n) → metrics measure orthogonal aspects → keep both (multi-realizability raw 106), no retraction
- **Cross-repo:** anima ↔ hexa-lang (HXC catalog canonical lives in hexa-lang)

### Top-5 — **`mk_ix_l_ix_alpha_bridge_real_eeg`** (Tier-A)
- **Genus slug:** `l_ix_alpha_real` (genus = "irreversibility_on_temporal_asymmetry")
- **Reuse plan:** `anima-clm-eeg/tool/an_lix_01_alpha_bridge_real.hexa` — already has REAL/SYNTH split; feed today's filtered .npy alpha-band; compute forward-vs-reverse correlation gap. Mk.IX L_IX `raw 30 frozen` preserved.
- **Input:** today filtered .npy (alpha-band Hilbert envelope)
- **Expected outcome:** scalar irreversibility index; baseline value for future task-locked comparisons
- **Falsifiers (3+):**
  1. F1: forward = reverse within ε=0.02 → time-symmetric → no irreversibility signature in resting-state (expected for pure noise; partial-fail for biological)
  2. F2: irreversibility > 0.2 in synthetic white-noise control → spurious; method bug
  3. F3: ICA vs filtered yields opposite signs → preprocessing-axis collapse → method retracted for this preprocessing pipeline
- **Cross-repo:** anima-clm-eeg (primary tool home) ↔ anima (input artifacts)

---

## 4. Tier-A immediate execution recommendation (1 candidate, concrete commands)

### Recommended NOW: **Top-3 alpha_coh_phase_16x16_atlas**

Rationale: pure read on existing `.npy`, no LLM compute, no h_last cache dependency, ~2 minutes. Produces the input atlas that Top-1 needs. Lowest precondition count.

```bash
# Pre-flight: verify hexa.real CLI
which hexa.real || ls -la "$HEXA_LANG/bin/hexa.real" 2>/dev/null

# Run alpha-coh emit
cd <repo-root>
"$HEXA_LANG/hexa.real" run tool/an11_b_eeg_ingest.hexa \
    --emit-alpha-coh \
    --input recordings/sessions/baseline_resting_60s_20260428_filtered.npy \
    --output state/clm_eeg_alpha_coh_60s_20260428.json

# Run alpha-phase emit
"$HEXA_LANG/hexa.real" run tool/an11_b_eeg_ingest.hexa \
    --emit-alpha-phase \
    --input recordings/sessions/baseline_resting_60s_20260428_filtered.npy \
    --output state/clm_eeg_alpha_phase_60s_20260428.json

# Sanity: peek at off-diagonal mean and max pair
python3 -c "import json; d=json.load(open('state/clm_eeg_alpha_coh_60s_20260428.json')); print('mean_offdiag', d.get('mean_offdiagonal_coh'), 'max_pair', d.get('max_pair_coh'), 'idx', d.get('max_pair_indices'))"
```

**Estimated time:** 2-5 minutes.
**Outputs feed:** Top-1 (region mapping uses 16×16 atlas) + Top-2 (alpha-band confound check on LZ).
**Falsifier auto-fired:** if max_pair_coh > 0.95 → impedance bridging alarm (Top-3 F1).

---

## 5. Cross-repo (raw 47) consolidated angle

| Repo | Role |
|---|---|
| **anima** | tool home (an11_b_eeg_ingest, anima_eeg_corr, hxc_composite_dispatcher), state (alpha_coh JSON, lz76 audit) |
| **anima-clm-eeg** | spec home (clm_lix_eeg_alpha_direct_mapping_spec, eeg_pre_register_v1), L_IX bridge tool, cross-link audit |
| **anima-physics** | mu_rhythm_detector, sleep_stage_detector (drowsy gate for LZ76 disambiguation); needs .npy adapter |
| **hexa-lang** | hexa.real CLI; HXC catalog A1-A22 canonical reference; numeric stdlib |
| **nexus** | roadmaps centralized; raw 100 ω-cycle dispatch surface |

Primary integration edge: **anima ↔ anima-clm-eeg** (already audited per `anima_eeg_anima_clm_eeg_cross_link_audit.md`).

---


**Speculative bridges (intent ≠ emergent):**
- **Mk.XI v10 4-backbone × EEG 4-band coincidence (D3):** the 4×4 mapping in `anima_eeg_corr_v1.json` is a **design intent** assignment, not an emergent structural fact. r≥0.4 PASS does not establish mechanistic coupling; it could be common-mode variance from any source. **Claim: "phenomenal correlate grounded"; truth: Pearson r ≥ 0.4 on pre-registered band-region cells.**
- **16-template × 16ch (D4):** numerical coincidence between 16 consciousness templates (Hexad/Law/Phi/SelfRef × 16-dim) and 16 EEG channels is **not** a discovered symmetry — it's a contingent hardware constraint (Cyton+Daisy = 16 ch). Treat as scaffold, not as evidence.
- **TECS-L H-CX-1 σφ=nτ resting-state n=6 unique solution (A6):** RSN literature lists 7-10 commonly-resolved networks; n=6 uniqueness is a TECS-L theoretical claim, not an EEG-empirical one at 16ch surface electrodes (RSN ICA needs ≥64ch + dipole fit + fMRI ground truth typically). **Lowered to Tier-C.**

**Mature components (no speculation):**
- AN11(a)+(b)+(c) chain (CP1 r14 closure VERIFIED 3-axis)
- HXC catalog A1-A22 (mature with PPMd/LZ-PPM well-characterized)
- LZ76 Kaspar-Schuster 1987 implementation (algorithmically sound; threshold-application is the speculative part, not the algorithm)
- an11_b_eeg_ingest --emit-alpha-coh / --emit-alpha-phase (Welch + Hilbert via scipy; standard signal processing)

---

## 7. Follow-up agent dispatch recommendation

After user approval of Top-3 immediate run, the remaining four candidates are **mutually independent** on inputs (Top-1 also depends on Top-3 atlas, but that's then sequential). Recommended dispatch (own 11 parallel-loop-mandate):

```
Phase 1 (sequential, prerequisite): Top-3 alpha_coh_phase_16x16_atlas    (2-5 min)
Phase 2 (parallel, 4-way fan-out):
   ├─ Top-1 anima_eeg_corr_4bb_hw_run      (depends on Top-3 + cached h_last; 10-30 min)
   ├─ Top-2 v_phen_lz_cross_substrate_real_run  (independent; 5-15 min)
   ├─ Top-4 hxc_a17_a18_a19_eeg_npy_compression (independent; 5-10 min)
   └─ Top-5 mk_ix_l_ix_alpha_bridge_real_eeg     (independent; 5-15 min)
```

own 5 completeness-first → no cost cap; user approval is the only gate. raw 91 honest applies to all five.

---

## 8. Roadmap-side note (raw 100 nexus kick fallback)

This ω-cycle agent is itself the raw-100 strengthening fallback path (kick infra container-no-node issue documented). Direct Agent dispatch is the working channel until kick infra is restored. Roadmap entries to update post-execution: `EEG-DDAY-2026-04-28` cluster on nexus/roadmaps/anima.json (add `phase=measurement-integration-omega`).
