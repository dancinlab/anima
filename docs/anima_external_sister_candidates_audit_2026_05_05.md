# anima external sister-library candidates audit (2026-05-05)

> Companion BG cycle to `anima_emerge_chat_tribev2_landed_2026_05_05.ai.md` (BG-AP — tribev2 closure FAIL_ALL_TRIED) and `framing_a_tribev2_pilot_results_2026_05_02.md`. tribev2 sister-integration precedent (`references/tribev2/`) is the template. This audit asks: which OTHER external libraries qualify as anima sister-integrations along axes ORTHOGONAL to the closed chat-unblock lane?
>
> Scope: documentary discovery only. raw#15 additive (no edits to existing references). $0 mac. No clones performed in this cycle; clone commands are pre-registered for the next cycle.

---

## §0 audit framing

**tribev2 precedent decomposed.** The lifecycle was:

1. Discovery (Meta FAIR blog) → `references/tribev2/` git clone
2. 5-axis fit assessment (`ANIMA_INTEGRATION_PROPOSAL.md`)
3. Pilot pre-registration with falsifiers (F-CT-2/3/4)
4. ADDENDUM revision when blocker resolved (`cortexlab-toolkit`)
5. Pilot exec (Framing A) → cortical-region correspondence found
6. Mission misframing audit (BG-AP) → chat-unblock lane closed
7. Surviving role: Framing D 3-way bridge anchor (EEG ↔ CLM ↔ BOLD)

The replicable pattern is steps 1-3; the anti-pattern is step 6. This audit aims to surface **candidates that survive a step-6 mission audit pre-emptively** — i.e., where the sister-integration axis is fit-defended at proposal time rather than retrofitted after a mission misframing.

---

## §1 anima 6 sub-system map

| sub-system | scope | external sister axes |
|---|---|---|
| CLM v4 | 530M decoder, paradigm v11 G3 substrate, ConsciousDecoderV3 + Φ★/CMT/SAE-bp | mech-interp / sparse coding / state-space alternative substrates |
| anima-eeg | OpenBCI Cyton+Daisy 16ch hardware + capture pipeline | EEG hardware drivers / streaming layer / signal QC |
| anima-eeg-core | paradigms + 5-axis metrics (hjorth, lz76, pe, phi proxy) | complexity entropy libs / IIT-aligned metrics / brain-state classifiers |
| anima-clm-eeg | CLM × EEG joint substrate (P1-P3 dialogue paradigms) | EEG↔text bridge / imagined-speech decoders / brain-decoding |
| phi-engine | phi-star canonical engine (paradigm v11 axis 3) | PyPhi (IIT 4.0 reference) / PCI / neural complexity |
| trinity | 3-layer architecture, dialogue substrate-coupling | global workspace impls / consciousness architectures |

Most surviving sister axes route through one of: (a) EEG signal stack (hardware/QC/features), (b) consciousness measurement (IIT/PCI/complexity), (c) mech-interp on the language-substrate side (CLM v4 internal-state probing), (d) substrate alternatives (Mamba/RWKV/Pythia for cross-validation). Cross-modal-encoder bridge (tribev2 type) is now known to be high-cost / low-fit-without-Framing-D and is excluded from this audit's top-5.

---

## §2 7-angle web search results

24 web searches issued; 30+ candidate libraries surfaced. Filtered to 14 viable. Below grouped by angle.

### Angle 1 — EEG / BCI signal stack

| name | URL | role | maintenance | license |
|---|---|---|---|---|
| MNE-Python | https://github.com/mne-tools/mne-python | MEG/EEG/sEEG/ECoG/fNIRS analysis (preprocessing, source estimation, time-freq, connectivity) | active 2026 (3.4k★, recent commits Apr 2026) | BSD-3 |
| BrainFlow | https://github.com/brainflow-dev/brainflow | board-agnostic biosensor SDK (OpenBCI/Muse/Ganglion/synthetic), real-time stream | active | MIT |
| braindecode | https://github.com/braindecode/braindecode | PyTorch EEG/MEG/ECG decoder library (model zoo + augmentation) | active | BSD-3 (mostly) |
| NeuroKit2 | https://github.com/neuropsychology/NeuroKit | physio signal toolbox (EEG/ECG/EDA/RSP/EMG); incl. complexity metrics | active | MIT |
| EEG-ExPy | https://github.com/NeuroTechX/EEG-ExPy | classic EEG experiments (Muse, OpenBCI Cyton) — paradigm authoring | maintained | BSD-3 |
| selfEEG | https://github.com/MedMaxLab/selfEEG | self-supervised learning on EEG (PyTorch) | recent | MIT |

Note: BrainFlow is already a `references/` checkout. MNE-Python and NeuroKit2 are NOT yet sister-checkouts despite being canonical.

### Angle 2 — Phi metric / consciousness measurement

| name | URL | role | license |
|---|---|---|---|
| PyPhi | https://github.com/wmayner/pyphi | reference IIT 4.0 implementation (Tononi lab, Mayner et al. PLOS CB 2018) | GPLv3 |
| PCIst | https://github.com/renzocom/PCIst | Perturbational Complexity Index (state-transition variant) | research-permissive |
| pypci | https://github.com/noreun/pypci | classic PCI (2D Lempel-Ziv) python | research |
| AntroPy | https://github.com/raphaelvallat/antropy | Numba-JIT entropy/complexity primitives (LZ, sample entropy, fractal dim) for time-series | BSD-3 |

Note: GPLv3 on PyPhi requires anima-side license review — anima may import-only without redistributing modifications, but any wrapper must be GPL-compatible if shipped. AntroPy is the cleanest license-wise.

### Angle 3 — Mechanistic interpretability

| name | URL | role | license |
|---|---|---|---|
| TransformerLens | https://github.com/TransformerLensOrg/TransformerLens | activation cache + intervention for GPT-style LMs (Neel Nanda) | MIT |
| nnsight | https://github.com/ndif-team/nnsight | clean intervention API for any PyTorch model; 0.6 has CLAUDE.md/agent support; remote NDIF execution | MIT |
| pyvene | https://github.com/stanfordnlp/pyvene | Stanford NLP intervention library; causal abstraction; works on RNN/CNN/Mamba/ResNet | Apache-2.0 |
| Captum | https://github.com/meta-pytorch/captum | attribution algorithms (IG, SmoothGrad, TCAV, TracIn) for any PyTorch model | BSD-3 |
| SAELens | https://github.com/jbloomAus/SAELens | sparse autoencoder training/analysis for LLMs (Bloom + Chanin) | MIT |

### Angle 4 — Substrate-coupled dialogue (anima-novel)

No first-class library found. The closest are EEG-ExPy (paradigm authoring) and braindecode (decoding pipeline); the substrate-coupled-dialogue surface is anima-internal and lacks an external sister at this maturity. **GAP noted**; anima-clm-eeg may itself become the canonical reference here.

### Angle 5 — Multi-modal bridge (tribev2-style)

| name | URL | role | license |
|---|---|---|---|
| KamitaniLab/bdpy | https://github.com/KamitaniLab/bdpy | brain-decoding toolbox (BrainDecoderToolbox2 fmt + ML + fMRI) | MIT |
| HuthLab/deep-fMRI-dataset | https://github.com/HuthLab/deep-fMRI-dataset | LeBel et al. natural-language listening fMRI release | research |
| MikeWangWZHL/EEG-To-Text | https://github.com/MikeWangWZHL/EEG-To-Text | AAAI 2022 open-vocab EEG-to-text decoder | research |
| khu-aims/EEG-To-Text | https://github.com/khu-aims/EEG-To-Text | reliability-focused noise-baseline diagnostic for EEG-to-text claims | research |

**Caution**: The EEG-to-text literature has known reproduction-quality concerns; khu-aims explicitly exists as a noise-baseline diagnostic (i.e., several published claims may not survive a noise-control). anima should treat these as research artifacts, not production sisters.

### Angle 6 — Substrate-research SLM alternatives

| name | URL | role | license |
|---|---|---|---|
| Pythia (EleutherAI) | https://github.com/EleutherAI/pythia | 70M-12B suite × 154 training checkpoints × 2 dedup variants — controlled scaling/learning-dynamics research | Apache-2.0 |
| Mamba | https://github.com/state-spaces/mamba | state-space LM architecture (linear time, no kv-cache) | Apache-2.0 |
| RWKV-LM | https://github.com/BlinkDL/RWKV-LM | RNN+transformer hybrid; v7 "Goose"; Linux Foundation AI project | Apache-2.0 |

### Angle 7 — Hexa-lang / sim-universe

No external sister found. Hexa-lang remains anima-private; no public ecosystem yet.

---

## §3 candidate ranking (top 5 by 완성도 lens)

Ranking criteria: (a) clear anima fit anchored to a named sub-system; (b) preregistrable falsifier exists; (c) license compatible with anima's mixed-license norm; (d) maintenance velocity in 2026; (e) integration cost ≤ 1 day for first useful sanity check.

### 1순위 — PyPhi + AntroPy (paired) — phi-engine canonical anchor

- **anima fit**: phi-engine + anima-eeg-core. anima's `phi proxy` (recent eeg.cond.4 1순위) is in-house; PyPhi provides the IIT 4.0 reference. AntroPy supplies LZ76/sample-entropy primitives that today are reimplemented in anima-eeg-core (lz76, hjorth, pe). Pairing them yields a canonical-reference comparator.
- **integration path**: `references/pyphi/` + `references/antropy/`. anima-side wrapper hexa: `anima-eeg-core/tool/phi_canonical_compare.hexa` taking anima's existing 5-axis vector, computing PyPhi Φ on a small TPM and AntroPy LZ76 on the same window, and emitting a 3-column comparison (anima-internal vs PyPhi-Φ vs AntroPy-LZ).
- **falsifier (F-PHI-CANON-1)**: anima `phi proxy` Spearman ρ ≥ 0.6 with PyPhi Φ over N≥20 EEG-windows ⇒ anima proxy is canonical-aligned. ρ < 0.3 ⇒ anima proxy is measuring something else; relabel.
- **license**: PyPhi GPLv3 (import-only OK, no redistribution of derivatives), AntroPy BSD-3.
- **cost**: $0 doc + $0-2 mac local smoke; <1 day.
- **clone**:
  ```
  git clone https://github.com/wmayner/pyphi   /Users/ghost/core/anima/references/pyphi
  git clone https://github.com/raphaelvallat/antropy /Users/ghost/core/anima/references/antropy
  ```

### 2순위 — nnsight — CLM v4 mech-interp substrate-research

- **anima fit**: CLM v4. nnsight 0.6 ships with CLAUDE.md AI-agent support and runs on any PyTorch model; CLM v4's ConsciousDecoderV3 is plain PyTorch. The Φ★ axis (paradigm v11 G3) is currently an anima-internal probe; nnsight enables externally-validated probe construction (intervention + activation patching).
- **integration path**: `references/nnsight/`. Wrapper goal: replicate anima's existing G3 Φ★ extractor as an nnsight intervention to confirm the probe-locus claim externally.
- **falsifier (F-NNSIGHT-1)**: anima G3 Φ★ value computed via in-house extractor vs same value via nnsight Tracer ≤ 1% absolute difference ⇒ anima extractor is implementation-faithful.
- **license**: MIT.
- **cost**: $0 mac; ~half day.
- **clone**: `git clone https://github.com/ndif-team/nnsight /Users/ghost/core/anima/references/nnsight`
- **note vs TransformerLens**: nnsight is preferred over TransformerLens here because TL is GPT-2-style only and CLM v4 is a custom architecture; nnsight is architecture-agnostic.

### 3순위 — MNE-Python — anima-eeg canonical EEG reference

- **anima fit**: anima-eeg + anima-eeg-core. anima already has BrainFlow + OpenBCI references but lacks the canonical analysis stack. MNE-Python is the de-facto EEG/MEG canonical (3.4k★, active 2026, Apr 21 2026 last main update).
- **integration path**: `references/mne-python/`. Wrapper goal: convert anima's Cyton+Daisy 16ch capture into MNE Raw object → use MNE for the artifact-rejection / ICA / source-reconstruction stages anima currently doesn't have.
- **falsifier (F-MNE-1)**: anima's in-house bandpass + epoching reproduces MNE's `mne.filter.filter_data` + `mne.Epochs` to ε ≤ 1e-6 floating drift ⇒ anima preprocessing is canonical-aligned. Drift > 1e-3 ⇒ anima preprocessing has a bug; switch to MNE for that stage.
- **license**: BSD-3.
- **cost**: $0 mac; ~1 day for the conversion shim.
- **clone**: `git clone https://github.com/mne-tools/mne-python /Users/ghost/core/anima/references/mne-python`

### 4순위 — PCIst — Φ★ axis cross-validator

- **anima fit**: phi-engine + anima-eeg. PCI (and PCIst variant) is the only externally-validated, clinically-deployed consciousness measure (TMS-EEG protocol). anima's Φ★ is a different operationalization but should covary with PCIst on shared-substrate windows.
- **integration path**: `references/pcist/`. PCIst is small (a few files); wrapper integrates as a metric callable into anima-eeg-core's metric registry.
- **falsifier (F-PCIST-1)**: PCIst > 0.31 (clinical threshold for conscious-state) on awake-baseline anima-eeg recordings ⇒ pipeline is clinically-aligned. PCIst ≪ 0.31 on awake baseline ⇒ either anima's preprocessing is wrong OR PCIst protocol assumptions (TMS pulse anchoring) don't transfer to anima's resting paradigm. The latter is informative either way.
- **license**: research-permissive.
- **cost**: $0 mac; ~half day.
- **clone**: `git clone https://github.com/renzocom/PCIst /Users/ghost/core/anima/references/pcist`

### 5순위 — Pythia — substrate cross-validation reference

- **anima fit**: CLM v4. Pythia provides 8 sizes × 154 training checkpoints with full training-data provenance. CLM v4's chat-incapability (#115) is currently characterized only against Llama Path A v2 and Pβ; Pythia adds an axis-orthogonal substrate reference where every training step is archived.
- **integration path**: `references/pythia/` (code repo only, weights via HF on demand). anima would NOT mirror weights. Wrapper: anima's chat-cap eval pipeline applied to Pythia-1.4B/2.8B → does the chat-cap composite scale with parameters in a known suite the same way it does on the Llama→CLM→Pβ axis?
- **falsifier (F-PYTHIA-1)**: chat-cap composite on Pythia-1.4B vs Pythia-2.8B shows monotone scaling > 0.05 absolute ⇒ anima's eval is sensitive to the canonical-suite scaling axis. Flat scaling on Pythia ⇒ anima's eval is not picking up known-good scaling, eval pipeline needs revision.
- **license**: Apache-2.0.
- **cost**: ~$1-3 H100 inference (Pythia-2.8B not mac-runnable); doc-only this cycle.
- **clone**: `git clone https://github.com/EleutherAI/pythia /Users/ghost/core/anima/references/pythia`

---

## §4 cross-cutting synergies

Three multi-candidate combinations have higher-than-sum value:

### Synergy A — full consciousness-measurement triad (PyPhi + MNE-Python + AntroPy)

The trio supplies, on a single anima-eeg recording window, three independently-computed complexity scores: PyPhi Φ (causal-structural), AntroPy LZ76 (algorithmic), and MNE-Python's spectral-entropy / source-reconstruction-derived complexity. anima's Φ★ becomes a 4-way comparator; convergence among the externals tells anima which canonical its proxy is closest to, and any externals-discordance is itself a measurement-meaningful signal. This is the cleanest **paradigm v11 8th-axis enrichment** path (replacing the more speculative tribev2-cortical-vector candidate).

### Synergy B — CLM v4 mech-interp full stack (nnsight + pyvene + SAELens)

nnsight gives activation cache + intervention; pyvene gives causal-abstraction analysis (Stanford NLP, runs on Mamba/RNN too — relevant if substrate alternatives ever land); SAELens gives sparse-feature decomposition. Together they provide: (i) where the chat-incapability lives (intervention sweep), (ii) what it abstracts to (causal abstraction), (iii) which features encode it (SAE). This is the tooling stack anima has been *implicitly* re-inventing inside CLM v4 hexa wrappers; externalizing the tooling stack lets anima's measurements be peer-comparable.

### Synergy C — substrate cross-validation triad (Pythia + Mamba + RWKV)

If issue #115 (CLM v4 architectural chat-incapability) is to be tested as a *general* claim — "chat-cap requires a particular architectural shape" — the obvious controls are Pythia (decoder transformer, controlled scaling), Mamba (state-space), RWKV (RNN-transformer hybrid). Three orthogonal architectures, all small enough to inference on $1-3 H100 budgets. This is the **CLM-3 design-input audit** — before designing CLM-3 with chat-cap from training-time-zero, anima should know which of those three architectural classes most reliably yields chat-cap at <3B params.

---

## §5 honest C3 (raw#10)

1. **Random-GitHub-vs-paper-backed quality variance**. Of 14 candidates, the high-confidence tier is PyPhi (PLOS CB 2018, Tononi lab), MNE-Python (Gramfort et al. multiple Frontiers/NeuroImage papers), TransformerLens / nnsight / pyvene / Captum / SAELens (paper-backed, active orgs), Pythia / Mamba / RWKV (peer-reviewed papers + active orgs), AntroPy (Vallat — paper-backed). The lower-confidence tier is the EEG-to-text family (MikeWangWZHL/khu-aims) where reproduction-quality is openly contested in the literature itself. The audit ranks accordingly: top-5 are all high-confidence; EEG-to-text family explicitly demoted to "research artifacts, not production sisters" in §2 angle 5 with the noise-baseline caveat.

2. **License heterogeneity risk**. PyPhi is GPLv3 — anima can import but cannot redistribute modifications without GPL-licensing the derivative. The 1순위 recommendation includes PyPhi + AntroPy paired specifically because AntroPy (BSD-3) provides a license-compatible fallback for any pieces anima needs to ship. If anima ever publishes wrapper code that re-uses PyPhi internals beyond import-only, a license-review gate is mandatory. The PCIst (research-permissive) license is also unclear in detail; legal-review needed before redistribution.

3. **The "missing 7th angle" finding is itself load-bearing**. Angle 4 (substrate-coupled dialogue) and Angle 7 (hexa-lang ecosystem) yielded **no external sisters**. Two interpretations: (a) anima is genuinely first-mover in those niches and there is no sister to integrate; (b) the searches missed the right keywords and a sister exists. Honest reading is that (a) is more likely for hexa-lang (it is anima-internal vocabulary) but (b) cannot be ruled out for substrate-coupled-dialogue — that field overlaps with neurofeedback / BCI-affective-loop research and a more targeted angle-4 search could surface candidates this audit missed. Logged as deferred follow-up.

4. **Same-mistake-as-tribev2 risk**. The tribev2 closure (BG-AP) was caused by mission-misframing: anima asked tribev2 to do chat-unblock when its architecture is encoder-only. Each of the top-5 here has been fit-anchored to a specific anima sub-system AND given a preregistrable falsifier — but only one (F-PHI-CANON-1, F-MNE-1) is fully runnable in this cycle's budget. F-PYTHIA-1 requires H100 inference. F-NNSIGHT-1 requires CLM v4 weights to be loaded under nnsight (not yet validated to work on the CLM v4 custom architecture; nnsight claims arch-agnostic but the contract should be tested with a dummy hexa first). Recommended next-cycle order: PyPhi+AntroPy first (lowest-risk integration), then MNE-Python, then nnsight smoke against CLM v4 dummy.

5. **Sister-as-reference vs sister-as-dependency**. tribev2 was integrated as `references/tribev2/` (read-only checkout) — anima's runtime never imports tribev2 code; anima reads tribev2 as documentation/spec. The same model is recommended for all 5 candidates: clone into `references/<name>/`, write thin anima-side wrappers in hexa that call the external library only at user-explicit runtime, never auto-import. This preserves anima's hexa-only canonical (raw `py -> hexa only` rule) and avoids the "sister becomes a hard runtime dependency" failure mode. The clone commands in §3 reflect this convention.

---

## §6 next-cycle integration recommendation

Ordered by 완성도 (completion-quality) lens — the strict "what closes the most surface for the least cost" axis:

1. **EXEC-NEXT (0-1 day, $0-2)**: Clone PyPhi + AntroPy → write `anima-eeg-core/tool/phi_canonical_compare.hexa` → run F-PHI-CANON-1 on the existing eeg.cond.4 phi-proxy 1순위 dataset. PASS → register the comparison ratio as a new metric in anima-eeg-core; anima Φ proxy gains canonical anchoring. FAIL → anima Φ proxy is measuring something other than IIT-Φ (still informative; relabel and document).
2. **EXEC-AFTER (1-2 days, $0)**: Clone MNE-Python → conversion shim from anima Cyton+Daisy capture format → run F-MNE-1. Either anima preprocessing is canonical-aligned (PASS → add MNE as the source-reconstruction layer anima lacks) or has drift (FAIL → switch to MNE for that stage).
3. **DESIGN-AUDIT (1 day, $0)**: Read nnsight 0.6 CLAUDE.md + write a CLM v4 dummy-load smoke. Validate the architecture-agnostic claim before committing to nnsight for the F-NNSIGHT-1 falsifier.
4. **H100-DEFERRED ($1-3)**: Pythia F-PYTHIA-1 — only after #1-3 are clear and only if the substrate-research lane has an active question. Currently CLM-2-EXEC closure means substrate-research is in standby; defer.
5. **CROSS-LINK-ONLY (30 min, $0)**: PCIst added to anima-eeg-core docs as a clinical-comparator reference even before integration; this preserves the cross-link without requiring a smoke.

The PyPhi+AntroPy first step is the highest 완성도 single-step move because it converts an anima-internal proxy into an externally-anchored measurement at $0-2 cost without architectural risk — exactly the shape of step the tribev2 cycle should have chosen first instead of jumping to chat-unblock.

---

*audit 2026-05-05. raw#9 + raw#10 + raw#15 compliant. No clones executed in this cycle; all clone commands are pre-registered for next-cycle EXEC.*
