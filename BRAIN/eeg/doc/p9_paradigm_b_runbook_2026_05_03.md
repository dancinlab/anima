# P9 Paradigm B — Runbook (ZuCo ETL + φ-proxy pilot scaffolding)

> **ts**: 2026-05-03
> **scope**: operational runbook for Phase 3+ entry of Paradigm B (EEG-derived φ-proxy as direct CLM training target). Companion to spec doc.
> **predecessor**: `docs/p9_paradigm_b_eeg_phi_proxy_2026_05_03.md` (spec, 9 sections, 10-caveat C3)
> **status**: SCAFFOLDING_LANDED · DOWNLOAD_DEFERRED · PILOT_GATED_ON_P0_SFT

---

## §0 Executive

This runbook covers the **operational tasks** for Paradigm B Phase 3 entry, with download script + sample subject + ETL spec verified against actual ZuCo 1.0 data structure. Full corpus download is **deferred** until prerequisite P1 (P0 SFT live complete) and P5 (Paradigm A γ gradient verified) per spec §6.2.

**Verified facts (2026-05-03 OSF API crawl + 1-subject sample download)**:

| Property | Value | Source |
|---|---|---|
| ZuCo 1.0 OSF node | `q3zws` | https://osf.io/q3zws/ |
| ZuCo 2.0 OSF node | `2urht` | https://osf.io/2urht/ |
| ZuCo 1.0 subjects (alphabetical) | ZAB, ZDM, ZDN, ZGW, ZJM, ZJN, ZJS, ZKB, ZKH, ZKW, ZMG, ZPH | `task1-SR/Preprocessed/` enumeration |
| ZuCo 1.0 tasks | task1-SR (Sentiment Reading), task2-NR (Normal Reading), task3-TSR (Task-Specific Reading) | OSF root |
| ZuCo 2.0 tasks | task1-NR, task2-TSR (no SR; TSR distinct from 1.0 — paraphrase task) | OSF root |
| EEG sample rate | **500 Hz** (verified `EEG.srate` field) | sample probe |
| EEG channels post-preproc | **105** (was 128 raw; 23 channels rejected via Hollenstein's pipeline `automagic` ICA + bad-channel removal) | sample probe |
| Continuous EEG length / sentence-block | ~244 sec (1 task block, e.g. SR1) → 122,182 samples × 105 ch float32 ≈ 48 MB | sample probe `gip_ZAB_SR1_EEG.mat` |
| Per-subject Preprocessed size (1 task) | ~416 MB (18 .mat files) | direct measurement |
| Full Preprocessed (12 subj × 3 tasks ZuCo 1.0) | ~15 GB (extrapolated) | linear extrapolation |
| Full Preprocessed (18 subj × 2 tasks ZuCo 2.0) | ~22 GB | linear extrapolation |
| **Preprocessed-only corpus total** | **~37 GB** | both versions |
| Full corpus (Preproc + Raw + Matlab) | ~50-70 GB | spec §2.1 estimate confirmed |

---

## §1 Artifacts landed this cycle

| Path | Purpose | Size |
|---|---|---|
| `ubu1:/tmp/zuco_download.sh` | resumable parallel OSF crawler + downloader (Preproc/Raw/Matlab tier flags, subject filter, dry-run) | 201 lines bash |
| `ubu1:/tmp/zuco_sample/ZAB_task1_SR_preprocessed/` | full ZAB subject task1-SR Preprocessed tier (18 .mat files, 415.6 MB) | 416 MB |
| `docs/p9_paradigm_b_eeg_phi_proxy_2026_05_03.md` | spec (predecessor, this cycle's prior commit) | — |
| `docs/p9_paradigm_b_runbook_2026_05_03.md` | this doc | — |


**No commits this cycle** — per task instruction; sample data lives only in `ubu1:/tmp/`.

---

## §2 Sample-subject structural verification

### §2.1 File-type taxonomy in `ZAB_task1_SR_preprocessed/`

```
gip_ZAB_SRx_EEG.mat   (8 files: SR1-3, SR5, SNR6-8)  ~50-55 MB each   = continuous EEG, sentence-trial concatenated
oip_ZAB_SR4_EEG.mat   (1 file)                       ~55 MB           = "outlier-included preprocessing" variant for SR4 (per Hollenstein README)
ZAB_SRx_corrected_ET.mat (8 files: SR1-8)            ~0.8-0.9 MB each = eye-tracking with sentence/word-level fixation events, manually corrected
wordbounds_SNRx_ZAB.mat  (2 files: SNR1, SNR2)       ~20-35 KB        = pixel bounding boxes per word per sentence (for fixation-to-word mapping)
```

Naming convention (Hollenstein 2018 README):
- `SR` = Sentiment Reading (task1, ~400 sentences)
- `SNR` = Sentiment Normal-Reading (task1 control)
- `gip` = "good ICA preprocessing" (canonical pipeline output)
- `oip` = "outlier-included preprocessing" (less-strict alternative for low-yield blocks)

### §2.2 EEG `.mat` (v7.3 = HDF5) inner structure

```
gip_ZAB_SR1_EEG.mat  (HDF5 root)
├── EEG/                                  # EEGLAB struct (matlab struct → HDF5 group)
│   ├── data       : (122182, 105) float32   # samples × channels (≈ 244s @ 500Hz, 105 channels)
│   ├── srate      : (1,1) float64 = 500     # sampling rate Hz
│   ├── nbchan     : (1,1) float64 = 105     # channel count
│   ├── pnts       : (1,1) float64 = 122182  # total samples
│   ├── trials     : (1,1) float64 = 1       # continuous (not epoched here)
│   ├── xmin/xmax  : (1,1) = 0 / 244.362     # seconds
│   ├── chanlocs   : group with 'labels','X','Y','Z','theta','radius',...  (per-channel HDF5 references)
│   ├── event      : group with 'type','latency','duration','urevent',...   (event triggers — fixation onsets etc)
│   ├── epoch      : group (per-epoch metadata if epoched; here trials=1 so likely empty)
│   ├── icachansind, icaweights, icasphere, icaact     : ICA decomposition (post-rejection)
│   └── (other EEGLAB fields: filename, filepath, history, ...)
├── #refs#                                 # HDF5 cross-references (EEGLAB cell-array storage)
├── auto_badchans   : (10,1) — automatic bad-channel indices flagged
├── ica_rejected    : (14,1) — rejected ICA components
├── man_badchans    : (10,1) — manually-marked bad channels
├── automagic/      : version + parameters of Hollenstein's `automagic` toolbox
├── params/         : channel_rejection_params, eeg_system, filter_params, ica_params, interpolation_params, pca_params
└── tobe_interpolated, is_interpolated, rate
```

### §2.3 ET `.mat` (v7.3 = HDF5) inner structure (`ZAB_SR1_corrected_ET.mat`)

EEGLAB `EEG.event` struct serialized — per-fixation events with these fields (Hollenstein 2018 ZuCo readme):
- `type` : event class label string (`'L_fixation'`, `'L_saccade'`, `'L_blink'`, `'sentence_start'`, ...)
- `latency` : sample index (re EEG, 500Hz) of event onset
- `duration` : duration in samples
- `sentence` : sentence ID (1..400 for ZuCo 1.0 SR)
- `word` : word index within sentence (1..N_words)
- `pix_x`, `pix_y` : fixation pixel coordinates (matched against wordbounds for word disambiguation)

### §2.4 wordbounds `.mat` (v5 — scipy-readable)

Cell array `(1, 250)` of float arrays `(N_words_in_sentence, 4)` = `[x1, y1, x2, y2]` pixel bounding boxes per word per sentence. Used for **fixation → word index** mapping (cross-reference with `pix_x/pix_y` in ET file).

---

## §3 ETL pipeline spec (target: `ubu1:/data/zuco_etl/` after full download)

### §3.1 Stage E1 — Per-sentence epoch extraction

**Input**: `gip_<SUBJ>_<TASK_BLOCK>_EEG.mat` + `<SUBJ>_<TASK_BLOCK>_corrected_ET.mat`

**Logic**:
1. Load EEG.data (T×C) and EEG.srate via `h5py.File`.
2. Load ET events via same; filter `type == 'sentence_start' / 'sentence_end'`.
3. For each sentence interval `[t_start, t_end]` in samples, slice `data[t_start:t_end, :]`.
4. Bandpass 0.1-100Hz (already done in `gip_*` per Hollenstein), notch 50Hz (Swiss line freq).
5. Re-reference to average (already done in pipeline; verify via `EEG.ref` field).

**Output (per sentence)**: dict
```
{
  "subject": "ZAB", "task": "task1-SR", "block": "SR1", "sentence_id": 7,
  "text": "<sentence string from task_materials/>",
  "n_samples": 4521, "n_channels": 105, "srate": 500,
  "data": np.float32 array (4521, 105),
  "channel_labels": [...],
  "fixations": [
    {"word_idx": 0, "word": "The", "t_onset_sample": 12, "duration_samples": 95, "pix_x": 92.0, "pix_y": 86.0},
    {"word_idx": 1, "word": "Apple",  ...},
    ...
  ]
}
```

### §3.2 Stage E2 — Word-fixation alignment

For each sentence dict, for each `fixation`:
- Compute window `EEG[t_onset_sample - w_pre : t_onset_sample + w_post]` where (per spec §3.2 strategy 1) `w_pre = 100` samples (200ms / 2), `w_post = 100`. = 200ms window.
- For strategy 3 (N400-locked): `w_pre = -50` (i.e. `t + 100ms`), `w_post = 250` (i.e. `t + 500ms`). = 400ms window.

**Output**: per-fixation EEG window `(N_samples_window, 105)`.

### §3.3 Stage E3 — φ-proxy computation per window (recommended: §1.3 sample-partition φ)

Recommended primary method (§5 below): **sample-partition φ on EEG channels** (direct port of `tool/anima_phi_v3_canonical.hexa`).

```python
def phi_v3_eeg(window: np.ndarray, K: int = 8, hid_frac: float = 0.5, seed: int = 0) -> float:
    """
    window: (N_samples, C_channels) float32
    Returns scalar Φ★ = MIN_k [ log|Cov(X)| - (log|Cov(X[S1_k])| + log|Cov(X[S2_k])|) ]
    """
    N, C = window.shape
    # Top-variance channel projection (mirror anima_phi_v3 HID = max(2, N//2))
    HID = max(2, C // 2)
    top_idx = np.argsort(window.var(axis=0))[-HID:]
    X = window[:, top_idx]                                   # (N, HID)
    log_det_full = np.linalg.slogdet(np.cov(X, rowvar=False))[1]
    rng = np.random.default_rng(seed)
    phis = []
    for k in range(K):
        perm = rng.permutation(N)
        s1, s2 = perm[:N//2], perm[N//2:]
        d1 = np.linalg.slogdet(np.cov(X[s1], rowvar=False))[1]
        d2 = np.linalg.slogdet(np.cov(X[s2], rowvar=False))[1]
        phis.append(log_det_full - (d1 + d2))
    return float(min(phis))
```

**Output**: scalar `phi_eeg` per fixation (or per sentence, aggregating).

Auxiliary monitor: gamma-band coherence (§1.1) — fast scalar, sanity-check signal.

### §3.4 Stage E4 — JSONL per-token training pairs (CLM-side ingest format)

**Output schema** (one line per CLM token, mirrors current `state/p9_p0_sft_data_50k_2026_05_03/sft_data.jsonl` format extended):

```jsonl
{"subject":"ZAB","sentence_id":7,"word_idx":3,"text":"Apple","prefix_text":"The Apple","phi_eeg":0.0421,"phi_eeg_gamma_coh":0.117,"window_ms":[t-100, t+100]}
```

Then in SFT loader, the `phi_eeg` becomes the supervision target for `π_φ(h_t)` per spec §3.4.

### §3.5 Stage E5 — Manifest + train/val/holdout split

Mirror P0 SFT manifest pattern:
- `state/p9_paradigm_b_corpus_<DATE>/manifest_v1.jsonl` (per-subject availability, fixation count, mean phi_eeg, sigma phi_eeg)
- subject-level holdout split: 8 train, 2 val, 2 test ZuCo 1.0 (random by RNG seed=20260503); 12 train, 3 val, 3 test ZuCo 2.0
- **No subject crosses splits** (avoids subject-level leakage given §7 caveat 6 inter-subject variance).

---

## §4 ETL wall-time estimate (refined post-investigation)

Original spec §6.2 P3 estimate: **2-4 days**. Refined breakdown after sample-subject probe:

| Subtask | Original estimate | Refined | Notes |
|---|---|---|---|
| OSF API crawl + URL list | 0.5 day | **0.5 hour** | API responsive; script written + tested this cycle |
| Preprocessed download (37 GB, parallel=4) | 1 day | **3-6 hours** wall, OSF rate-limited ~5 MB/s/conn | network-bound; can start unattended |
| `gip_*_EEG.mat` parsing (HDF5 → npy per sentence) | 0.5 day | **6-12 hours** for ~12k sentences (12 subj × ~1000 sent) × 100ms/sentence | h5py overhead; can parallelize with `joblib` (4-8 workers) |
| ET event extraction + word-fixation alignment | 1 day | **4-8 hours** for ~30k fixations | pure CPU, vectorizable |
| φ-proxy compute per fixation (~30k windows × 20ms each) | 0.5 day | **10-20 minutes** with K=8, HID=52 | trivial — SVDs are fast on 200-sample windows |
| JSONL emission + manifest + split | 0.5 day | **1-2 hours** | I/O-bound |
| Sanity QA (channel-rejection rate, fixation count distribution, phi_eeg histogram, NaN/Inf check) | 0.5 day | **2-4 hours** | first-time discovery work |
| **Total** | **2-4 days** | **~1.5-2.5 days wall** with parallelism | requires ~4 cores + 100 GB SSD |

**Refined estimate: 1.5-2.5 days** (down from 2-4) — primarily because download is faster than expected (OSF server gave us ~415 MB in <2 minutes for ZAB sample → extrapolate to ~3 hours full Preprocessed at parallelism=4) and φ-proxy compute is negligible vs spec assumption.

If we include `--raw` tier (+20 GB BDF/SET files for re-preprocessing experiments), add ~6 hours download + 1 day for own preprocessing pipeline (MNE ICA + interpolation), bringing total to ~3 days.

---

## §5 φ-proxy method recommendation (spec §1.3 vs §1.1 vs §1.5)

### §5.1 Recommendation: **§1.3 sample-partition φ on EEG channels** (TOP-1)

### §5.2 Rationale

1. **Same-formula cross-substrate claim** (spec §5.1 load-bearing point) — `Φ★_CLM(h)` and `Φ★_EEG(brain)` use **identical formula** on different substrates. This is the primary scientific value of Paradigm B over Paradigm A. Choosing §1.1 (gamma coherence) or §1.5 (PLV) reduces the claim from "same-formula-different-substrate" to "analogous-measure-different-substrate" — significantly weaker.

2. **Compute cost is non-blocking** — spec §1.3 estimate: HIGH (~20ms per window). Refined empirical estimate (200-sample window × 52 HID × 8 partitions): **~5-10ms per window** on modern CPU with numpy SVD. For ~30k fixations → ~5 minutes total. Fully tractable.

3. **Differentiability not required on EEG side** — φ-proxy is a precomputed *target* (spec §4.3), not a gradient path. The non-smoothness of `MIN_k` and `slogdet` doesn't matter — we just need a stable scalar per window.

4. **Sample-size adequacy for Cov estimation**:
   - 200ms window @ 500Hz = 100 samples per window
   - HID = 52 (half of 105 channels)
   - Cov(52×52) on 100 samples → **slightly under-determined for full-rank Cov** (need ≥52 samples; have 100; condition number will be moderate)
   - Mitigation: shrinkage covariance (Ledoit-Wolf, `sklearn.covariance.LedoitWolf`) or expand window to 300-400ms (150-200 samples) if log|Cov| diverges
   - Validation: pilot run 100 fixations, plot histogram of `log_det_full` — if any negative-infinity (singular Cov), enable shrinkage

5. **Auxiliary monitor: §1.1 gamma coherence** as secondary signal
   - 5-10ms per window, scalar output
   - Gives an interpretable "synchrony" proxy alongside the φ scalar
   - Use for QA (correlation `phi_eeg vs gamma_coh` should be positive; if negative, diagnostic of artifact-domination)
   - Do not use for loss — only logging

6. **NOT recommended: §1.2 k-NN MI** — too expensive for per-fixation pipeline (50-200ms × 30k fixations = 25-100 minutes); offers no advantage over §1.3 for cross-substrate framing.

7. **NOT recommended (yet): §1.4 microstate dynamics** — adds complexity (k-means fit per subject, transition matrix entropy) without clear φ-family payoff. Defer to future cycle.


Per spec §5.3: PASS if `|Φ★_CLM(P) − Φ★_EEG(P)| / Φ★_EEG ≤ 0.30` on ≥80% of held-out ZuCo prompts P. This requires §1.3 method on EEG — methods §1.1/§1.5 have no comparable scale and would require a learned alignment (additional confound, weaker falsifier).

---

## §6 Phase 3 entry prerequisites (spec §6.2 — operational checklist)

Six prereqs from spec §6.2, with this cycle's status:

| # | Prereq | Status (2026-05-03) | Evidence |
|---|---|---|---|
| **P1** | P9 SFT P0 LIVE complete (Paradigm A baseline) | **IN PROGRESS** — warmup live landed 2026-05-03 (`state/markers/p9_p0_warmup_live_landed.marker`); full 50k SFT pending | `state/p9_p0_warmup_live_2026_05_03/trajectory.json`, `docs/p9_p0_warmup_live_landed_2026_05_03.ai.md` |
| **P2** | Φ★ baseline reproduced post-SFT (≥ floor 5.0) | **PENDING P1** | will produce `state/.../phi_v3_canonical_post_sft.json` |
| **P3** | ZuCo 1.0+2.0 downloaded + MNE-preprocessed | **SCAFFOLDED** — script written + tested + 1 sample subject (415 MB) verified; full download deferred (37 GB, awaiting P1+P5) | `ubu1:/tmp/zuco_download.sh`, `ubu1:/tmp/zuco_sample/ZAB_task1_SR_preprocessed/` |
| **P5** | Paradigm A delivers measurable BOLD-MSE convergence | **PENDING P1** — γ-term gradient flow audit deferred to post-P0-50k | `state/p9_sft_pareto_results_*/` (not yet created) |
| **P6** | Pilot alignment study (100 ZuCo sentences × Mistral forward → corr Φ★_CLM, Φ★_EEG) | **PENDING P1+P3+P4** | will land at `state/p9_paradigm_b_pilot_<DATE>/correlation.json` |

**Decision gate** (per spec §6.3 decision tree): proceed to Phase 3 (Paradigm B addition or replacement) only **after** P1 + P5 complete, then re-evaluate based on Paradigm A γ-gradient quality.

---

## §7 Operational notes for next-cycle executor

1. **Run script with dry-run first**: `ssh ubu1 '/tmp/zuco_download.sh --dry-run'` — verifies OSF reachability, prints manifest with file sizes, no bytes transferred. Sanity check disk (`/data` partition needs ≥40GB for Preproc-only, ≥80GB for `--all`).
2. **Default destination `/data/zuco/`**: override via `ZUCO_DEST=/path` env var or `--dest` flag. ubu1 currently has 635 GB free on `/`.
3. **Resume support**: script uses `curl -C -` for partial-file resume + size-check skip on existing complete files. Safe to re-run.
4. **Parallelism**: `ZUCO_PARALLEL=4` default (xargs -P). OSF connection limit ~6-8 per IP; do not exceed 6.
5. **Subject subset for fast iteration**: `--subjects ZAB,ZDM,ZGW` — useful for pilot before committing to full 30-subject corpus.
6. **License compliance**: ZuCo CC-BY 4.0 requires attribution in any derived dataset/publication. Cite `Hollenstein et al. 2018, Sci Data 5:180291` (ZuCo 1.0) and `Hollenstein et al. 2020, arXiv:1912.00903` (ZuCo 2.0).

---

## §8 raw compliance summary

- **POLICY R4**: Paradigm B remains Phase 3 entry — current Phase 2 baseline (`state/p9_sft_spec_2026_05_02/loss_design.json` 4-loss family) unchanged.

---

**status**: P9_PARADIGM_B_RUNBOOK_2026_05_03_LANDED
**verdict_key**: SCAFFOLDING_LANDED · DOWNLOAD_DEFERRED · PHI_METHOD_RECOMMENDED_§1.3 · ETL_WALL_REFINED_1.5_TO_2.5_DAYS · PREREQ_CHECKLIST_LANDED
