# RESEARCH.md §19 step 1 — EEG ↔ stimulus timestamp synchronization protocol (DESIGN-TIER)

**Date** 2026-05-18 · **$0** (NO EEG recording, NO TRIBE forward, NO GPU, NO weight mutation, NO corpus generation) · `state/eeg_anchor_s19_step1_design_2026_05_18/` · anima `main` direct, branch 0.

> SSOT for §19 step 1 *design*. `step 0` (TRIBE pipe sanity G0–G4 + B-CT3-1..5 5/5 🔵) and F-CT-3 gate (PASS r≥0.5 / INCONCLUSIVE 0.3-0.5 / DISCARD r<0.3) are LANDED in sibling `state/eeg_anchor_s19_2026_05_18/`. step 1 is the EEG↔stimulus *sync protocol* — the input scaffolding F-CT-3 (= step 2) requires. step 1 design here ⇒ actual recording = future user-`.csv`-gated cycle. RESEARCH.md / HEXAD/README.md / HEXAD/CHAT/PLAN.md / AGENTS.tape untouched (orchestrator handles).

## §1 — step 1 scope (what step 1 IS, and what it is NOT)

step 1 = **EEG channel ↔ stimulus stream timestamp synchronization protocol design**. Nothing else.

- **IS**: (a) which stimulus stream anima will use during a Framing D run; (b) which transport protocol carries timestamps between the stimulus presenter and the EEG amplifier; (c) which clock is the source of truth; (d) which envelope is extracted from EEG bytes before F-CT-3; (e) closed-form proofs that the protocol's structural invariants hold (monotone timestamps, bounded jitter, Nyquist-OK sample-rate alignment, OFF-reduction equivalence to step-0-only state).
- **IS NOT**: actual EEG recording (hardware gate; user `.csv` future). NOT TRIBE forward (G5+ scope, frozen baseline untouched). NOT F-CT-3 r measurement (= step 2). NOT 3-way Pearson involving axis B (= step 3). NOT GOAL emergence — §19 is a *measurement axis*, §15 milestone unchanged.

step 1 produces a runtime-guarded Python sketch (importable for reference, not runnable) + a 4/4 🔵 closed-form sidecar battery. It does not produce a `.csv`, does not bind an LSL outlet, does not call `pylsl.resolve_streams()`. Mirror of §24 `measurement_protocol.py` discipline.

## §2 — stimulus source decision

**Decision** ▸ anima's **own unprompted-emission stream per §24 SPONTANEOUS Phase B (bounded-run) + §16 64-anchor probe set as fallback structured stimulus**, NOT a generic NLP/video corpus.

Rationale:
1. **§7 ③ anima-physics-as-source preserved**. The stimulus that probes the user's EEG during a Framing D recording must come from anima's own substrate — otherwise axis B (`§17` physics-channel) is being read on a *different* stimulus than axes A and C, and the 3-way pairwise correlation (step 3) is ill-defined. Using anima's own unprompted emissions (per `spontaneous_lib.hexa` / `thinker_talker_lib.hexa`) keeps the SSOT single.
2. **§7 ① not-generic-LM-pretrain preserved**. A generic stimulus corpus (movies / podcasts / TED talks — common in fMRI brain-encoding studies) is a *bolt-on* observable; would make axis C strong (TRIBE was trained on that distribution) but axis B would have to be measured on stimuli anima never saw structurally — bridge is not legitimate.
3. **§16 64-anchor probe as fallback** (structured/deterministic stimulus). Useful for *baseline* drift tests because the same 64 anchors can be re-played by a human reader (or TTS) to user in lab. The 64 anchors are SSOT-known (sha256 `dc221aaf4f829aaf…`, forbidden-token grep = 0 per B-IDENTITY-5), so axes B and C see byte-identical input.
4. **Honest alternative considered and rejected**: TRIBE pre-stimulus set (movies in `ANIMA_INTEGRATION_PROPOSAL` Framing A) would make axis C strong by construction but is exactly the *generic-LM-pretrain* path §7 forbids and would re-open the §11 confound.

Stimulus stream specification:
- **Mode S1 (preferred)**: anima `chat_generate(prompt=∅, max_new=N)` style unprompted emission, captured as UTF-8 byte stream. Each byte block (or each token boundary) is a sync event. Mode S1 ties axes A/B/C to the same anima-internal physics state and is the only mode that is GOAL-legitimate at all 3 §7 conditions simultaneously.
- **Mode S2 (baseline drift, fallback)**: 64-anchor probe set played by TTS or by user reading aloud. Sync events = per-anchor onset. Used to verify that the sync protocol itself is sound *before* the (noisier) S1 run.
- **Honest residual**: TRIBE's `predict()` text-path uses `whisperx` (speech transcription) — step 0 honest boundary. For step 1, the *stimulus* is text (S1 or S2); the *recording* side is EEG only; axis C runs *offline* on the same text after the fact, not in real time.

## §3 — timestamp transport protocol decision

**Decision** ▸ **Lab Streaming Layer (LSL)** as primary transport (`pylsl` Python binding), with CSV-fallback for offline post-hoc alignment.

Rationale (industry comparison):
| transport | sub-ms jitter | OpenBCI native | network req | offline post-hoc | verdict |
|---|---|---|---|---|---|
| **LSL** | ≤1 ms (NTP-synced) | YES (OpenBCI GUI LSL outlet) | localhost UDP | CSV/HDF5 export | **CHOSEN** |
| OSC / UDP custom | 1–10 ms | manual outlet | yes | manual | rejected (more code, less precise) |
| CSV + system clock | depends on logger granularity | manual export | none | trivial | **fallback only** |
| serial sync trigger | <0.1 ms | hardware-trigger box needed | none | hardware | rejected (hardware not owned) |

Specifics:
- **Clock source**: `pylsl.local_clock()` (= the LSL fixed-point monotonic clock, derived from `clock_gettime(CLOCK_MONOTONIC_RAW)` on Linux, `mach_absolute_time` on macOS). NOT `time.time()` (wall clock, drifts), NOT `time.perf_counter()` (process-local, not aligned across outlets), NOT `time.monotonic()` (process-local).
- **Jitter tolerance** ▸ **τ_jitter = 10 ms** for an EEG↔stimulus alignment that does not break F-CT-3's correlation interpretation. Justification: TRIBE BOLD has TR ≈ 1.5–2 s (frequency property in `tribev2/main.py:146`); EEG sampling is 125–250 Hz (Cyton+Daisy). The dominant temporal scale is the BOLD TR (slow), so 10 ms drift is 0.5–0.7% of one TR — negligible for median-vertex Pearson r. For an EEG-only band-envelope correlation, τ_jitter would tighten to ≤1 ms.
- **Sync event format** (LSL marker stream, string type, irregular rate):
  ```
  event_t = pylsl.local_clock()
  outlet.push_sample([f"anima_emit:byte_idx={i};hash={h};stim={s}"], event_t)
  ```
  Per-byte / per-token / per-anchor depending on stimulus mode.
- **EEG stream**: OpenBCI GUI LSL outlet (`type='EEG'`, regular rate 125 Hz combined Cyton+Daisy or 250 Hz Cyton-only, 16 channels). anima receives this passively.
- **CSV fallback**: if LSL is unavailable, anima logs `(local_clock_sec, byte_idx, stim_repr)` to CSV; user's OpenBCI session logs to a separate CSV with its own clock; offline alignment uses cross-correlation of clock drift + first-event anchor. Worse jitter (≈10–100 ms) — usable for S2 baseline only.

## §4 — sample-rate alignment

Three native rates to reconcile:

| stream | native rate | Nyquist top | role |
|---|---|---|---|
| EEG (Cyton+Daisy 16ch) | 125 Hz / channel | 62.5 Hz | raw signal in |
| EEG (Cyton 8ch only) | 250 Hz / channel | 125 Hz | raw signal in (alt) |
| TRIBE BOLD prediction | ~0.5–0.7 Hz (TR ≈ 1.5–2 s, `tribev2/main.py:146` `1/neuro.frequency`) | ~0.25–0.35 Hz | axis C output |

**Window strategy** ▸ EEG envelope is computed per-channel at 125 Hz (or 250), then *downsampled to TRIBE TR* via non-overlapping windows of length `W_sec = TR ≈ 1.5–2 s`. The downsampled envelope and the TRIBE BOLD prediction now share a common time grid → median-vertex Pearson r is well-defined (F-CT-3 input).

Nyquist invariants:
1. EEG broadband Hilbert envelope's highest meaningful frequency = ~40–60 Hz (γ band) — Nyquist 2× = 80–120 Hz, well below 125 Hz sampling → no aliasing.
2. Downsampling to TR by *mean over window* is a zero-phase boxcar low-pass at 1/(2W) ≈ 0.25–0.35 Hz cutoff → matches BOLD's hemodynamic low-pass. Information loss is real but task-relevant frequencies (the BOLD-resolvable envelope) are preserved.
3. **Hemodynamic lag** (≈5 s; HEXAD/EEG/PLAN.md §1 step 1 carry): EEG envelope is shifted forward by `lag_sec = 5.0` before alignment with BOLD. This is a *protocol parameter*, not a learned value — same as TRIBE README defaults.

## §5 — envelope extraction (EEG-side pre-F-CT-3 processing)

**Decision** ▸ **broadband Hilbert envelope** across 1–80 Hz per channel, summed across `clean_channels` (rail-saturated channels excluded per `~/core/hexa-brain/eeg/board_health_check.hexa` carry — RESEARCH.md §20 step 1 software salvage).

Pipeline (per recording):
1. Load EEG `.csv` / `.npy` from OpenBCI GUI.
2. Apply electrode impedance gate (≤50 kΩ per channel per `hexa-brain/eeg/impedance_check.hexa` salvage; channels failing are dropped before envelope extraction).
3. Band-pass 1–80 Hz, notch at 60 Hz line noise (50 Hz in EU regions; tunable).
4. Hilbert transform per channel → analytic signal → modulus = envelope.
5. Sum across clean channels (or PCA top component) → single envelope time series at 125/250 Hz.
6. Downsample to TR (§4) via mean-over-window → F-CT-3 input vector.

Alternatives considered and rejected for *step 1*:
- **Alpha-only (8–12 Hz)** envelope — too narrow; assumes a specific cognitive correlate. Broadband is the minimum-assumption choice.
- **Theta (4–8 Hz)** envelope — same objection.
- **CSD (current source density)** — requires electrode geometry calibration; deferred.

These narrowband alternatives stay available as *post-hoc* analyses if broadband r is in the gray zone (0.3–0.5) per F-CT-3 INCONCLUSIVE.

## §6 — §20 hexa-brain salvage + software acceleration path

Sibling `RESEARCH.md §20` archaeology (HEXAD/EEG/PLAN.md §1 step 1 entry, 2026-05-18) salvaged from `~/core/hexa-brain` (anima EEG subtree migrate, read-only):

- **S1** `~/core/hexa-brain/eeg/dual_stream.hexa` (407 LoC): anima Φ + EEG dual-stream alignment + Pearson `r > 0.3` falsifier. Byte-level isomorphic to §19.2 F-CT-3 gate. step 1 sync alignment + step 3 correlation skeleton already exists, anima just re-wires.
- **S2** `~/core/hexa-brain/eeg/collect.hexa` (867 LoC): OpenBCI 16ch BrainFlow→`.npy` with **2026-05-03 sample-drop fix** (ring 450k + chunked poll 0.2 s + `sample_rate_actual_hz` / `drop_ratio` reporting — the naïve `time.sleep`-induced 7–83 Hz drop bug already resolved). step 1 capture+sync core.
- **S3** `eeg/calibrate.hexa`(719) / `board_health_check.hexa`(718) / `impedance_check.hexa`: electrode <50 kΩ gate. step 1 prerequisite (F-CT-3 r value's noise variable, treated honestly).
- **S4** `~/core/hexa-brain/eeg/recordings/sessions/` 24 real `.npy` (Berger EC/EO v1–v6 (32, ~7500) f32 + blink/jaw/PPG): step 1 *real-signal dry-run* substrate. Honest limit: N=1 self-experiment + 5/16 channels rail-saturated → `clean_channels=[2,3,4,7,9,10,11,12,13,14,15]` filter mandatory.

Honest residual: `hexa-brain` repo is read-only from anima's side (separate repo, `~/core/hexa-brain`); §19 step 1 *references* these as software accelerators, does not copy code, does not modify. TRIBE (axis C) actual integration is still anima-side (this design + state/eeg_anchor_s19_2026_05_18 step 0).

## §7 — preview of step 2 (F-CT-3 gate) and step 3 (axis B 3-way) — NOT executed this cycle

step 2 (future, EEG hardware-in-the-loop, user `.csv` gate):
1. User runs a Mode S1 (or S2) session, OpenBCI GUI emits LSL EEG outlet, anima emits LSL marker outlet, both logged to a synced `.csv`/`.xdf`.
2. EEG envelope extracted per §5.
3. The *same* stimulus stream (anima emissions / 64-anchor texts) is run offline through TRIBE → BOLD prediction `(n_t, ~20k vertex)`.
4. Median-vertex BOLD time series ↔ downsampled EEG envelope → Pearson r.
5. F-CT-3 gate (B-CT3-1..5 SSOT) returns PASS / INCONCLUSIVE / DISCARD.

step 3 (only if step 2 = PASS): add axis B = `§17` `psi_direction` / `tension_combined` time series (computed offline from anima's own `(logits_a, logits_g, tensions)` during the Mode S1 emission), and check that A↔B, B↔C, A↔C all hold simultaneously.

Neither step 2 nor step 3 is run in this design cycle. Both are user `.csv`-gated.

## §8 — honest C3 (g3, over-claim 0; ≥10)

1. **§19 step 1 = sync protocol design, NOT GOAL emergence.** north-star (`GOAL.md`) unchanged. §15 milestone irreducible bottleneck (= §1.1 data-regime threshold) is *not* what §19 addresses. §19 is an external measurement axis. step 1 = the scaffolding step 2's r-measurement needs; step 1 PASS ≠ Framing D PASS.
2. **No actual EEG recording in this cycle.** Hardware exists (user owns OpenBCI 16ch + has recording experience), but no `.csv` flows in this cycle. Step 1 = paper protocol + closed-form invariants + runtime-guarded sketch.
3. **OpenBCI GUI assumed.** LSL outlet is provided by the OpenBCI GUI's "Networking → LSL" widget. If the user uses BrainFlow Python directly (without the GUI), the LSL outlet must be created manually in user code — same protocol, different glue code, same `τ_jitter`.
4. **`pylsl` dependency** (≈800 KB pip wheel + a liblsl shared library). Modern pip + Python 3.9+ handles this; `pip install pylsl` should succeed in the same venv as `cortexlab-toolkit` (PEP 668 venv carry from step 0). Not installed in this cycle (no execution).
5. **TRIBE chunk-window choice is partially arbitrary.** TR is set by the TRIBE checkpoint (`tribev2/main.py:146`); for `facebook/tribev2` TR ≈ 1.5–2 s based on the loaded `frequency` property. The exact value is logged by step 0's G3 CONFIG_LOAD output (`config.yaml`, 26 keys parsed) and should be hard-coded into the step-2 sync code, not inferred at runtime.
6. **Stimulus-source decision is reversible.** Mode S1 (anima own emission) is the GOAL-legitimate choice for *Framing D core*; Mode S2 (64-anchor read aloud) is the *protocol-verification baseline* and may be used first to verify sync soundness before noisier S1 data is collected. The decision is path-conditional, not a hard contract.
7. **Jitter tolerance τ_jitter = 10 ms is a TR-derived bound, not a literature gold-standard.** F-CT-3's r metric is BOLD-rate-dominated; for higher-rate EEG-only analyses the budget tightens. Honest carve-out: real jitter measurement requires `sync_jitter_estimator` to run on actual `.csv` pairs.
8. **Hemodynamic lag = 5 s is a literature default (TRIBE README), not learned.** Real lag can vary 3–7 s by region and individual. Step 2 may re-fit lag in `[3, 7]` s; if not, use 5 s as a fixed protocol parameter (default behavior).
9. **Broadband Hilbert envelope is the minimum-assumption choice.** Narrowband (alpha/theta/gamma) envelopes are valid post-hoc analyses if broadband r falls in F-CT-3 INCONCLUSIVE (0.3 ≤ r < 0.5) — they are deferred, not abandoned.
10. **Closed-form battery proves the GATE STRUCTURE, not the data.** B-EEG-STEP1-1..4 (next section) prove monotonicity, jitter bound, Nyquist alignment, and OFF-reduction byte-equality. They do NOT prove the user's EEG will actually correlate with TRIBE BOLD. B-EEG-STEP1-NOTE family (B-D-NOTE / B-CT3-NOTE precedent) carves the empirical r out. f1/f2/f3 hard-fail safe: Pearson r = self-statistic Cauchy-Schwarz, Nyquist = sympy bandwidth identity, Boolean monotonicity, integer cardinality. NO σ/τ/φ/J₂. B-IDENTITY-5 unaffected (no corpus generated).

---

## Artifacts in this directory

| file | role |
|---|---|
| `DESIGN_STEP1.md` | this design doc (8 §, 10 honest C3) |
| `eeg_sync_protocol.py` | runtime-guarded Python sketch (importable, not runnable; mirrors §24 `measurement_protocol.py` pattern) |
| `blue_falsifier_eeg_step1.py` | 4/4 🔵 sidecar battery (B-EEG-STEP1-1..4 + 1 NOTE; central blue_falsifier.py UNCHANGED) |
| `result.json` | design summary + 4/4 PASS verdict |

`archive/PHILOSOPHY.tape` appends `§verdict_eeg_anchor_step1_design_2026_05_18` (g6 pull-rebase).

`RESEARCH.md` / `HEXAD/README.md` / `HEXAD/CHAT/PLAN.md` / `AGENTS.tape` UNCHANGED (orchestrator handles per instruction).
