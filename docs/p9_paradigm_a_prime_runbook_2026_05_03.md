# P9 Paradigm A' — Runbook (Algonauts 2025 sub-01 γ-only mini-run)

**Date:** 2026-05-03
**Status:** Pre-flight DONE on ubu1 (data downloaded, scaffold validated). NO training executed.
**Spec:** `docs/p9_paradigm_a_prime_measured_bold_2026_05_03.md`
**Scaffold:** `/tmp/p9_paradigm_a_prime_mini.py` (ubu1, raw#9-allowed scratch path)
**Dataset:** `/tmp/algonauts2025_sub01/algonauts_2025.competitors/` (ubu1)

---

## 0. Pre-flight summary (DONE 2026-05-03)

| Item | Status | Evidence |
|------|--------|----------|
| ubu1 reachable | OK | ssh aiden@ubu1 |
| git-annex installed | OK | `git-annex version 10.20240129` (apt) |
| datalad installed | OK | `datalad 1.4.1` (`pip --user --break-system-packages`) |
| Algonauts repo cloned | OK | `datalad clone https://github.com/courtois-neuromod/algonauts_2025.competitors.git` |
| sub-01 BOLD fetched | OK | `datalad get fmri/sub-01/func/` |
| Friends s01+s02 transcripts fetched | OK | `datalad get stimuli/transcripts/friends/{s1,s2}/` (98 .tsv) |
| BOLD shape verified | OK | (T_TR, 1000) float32, z-scored already, 292 keys |
| Transcript schema verified | OK | cols: text_per_tr, words_per_tr, onsets_per_tr, durations_per_tr |
| Mini-run scaffold dry-run | OK | 94 train + 2 holdout chunks, 118 484 tokens, 44 911 TR-steps |

**Actual disk used:** 585 MB in `.git/annex/objects/` (sub-01 only; well under 5 GB budget).
**Total clone footprint:** ~632 MB including git overhead.

---

## 1. Reproducing the pre-flight

```bash
# On ubu1 as user `aiden`:

# 1.1 Install datalad + h5py if missing
pip3 install --user --break-system-packages datalad h5py numpy pandas
sudo apt install -y git-annex                 # requires sudo on ubu1 (already done)
export PATH=$HOME/.local/bin:$PATH

# 1.2 git config (one-time)
git config --global user.name  "aiden"
git config --global user.email "aiden@local"

# 1.3 Clone metadata only
mkdir -p /tmp/algonauts2025_sub01 && cd /tmp/algonauts2025_sub01
datalad clone https://github.com/courtois-neuromod/algonauts_2025.competitors.git

# 1.4 Fetch sub-01 BOLD + Friends s01-s02 transcripts ONLY
cd algonauts_2025.competitors
datalad get fmri/sub-01/func/                                       # ~600 MB
datalad get stimuli/transcripts/friends/s1/ stimuli/transcripts/friends/s2/

# 1.5 Validate scaffold
python3 /tmp/p9_paradigm_a_prime_mini.py --dry-run
```

**Fallback (no DataLad):** raw HTTP via the GitHub-LFS-equivalent
`conp-ria-storage-http` sibling — `datalad siblings` lists the URL pattern
`https://conp.ca/.../<MD5E-hash>`. Each file's MD5E hash is the symlink target
under `.git/annex/objects/`. Easy to wget directly if datalad becomes unavailable.

---

## 2. Dataset inventory (post-download)

### 2.1 BOLD (Schaefer-1000 parcellation, MNI152NLin2009cAsym)

| File | Size | Keys | Shape |
|------|------|------|-------|
| `fmri/sub-01/func/sub-01_task-friends_..._desc-s123456_bold.h5` | 515 MB | 292 chunks (s01–s06) | (T_TR ≈ 482, 1000) per key |
| `fmri/sub-01/func/sub-01_task-movie10_..._bold.h5` | 92 MB | (movie10 chunks) | (T_TR, 1000) |

Key naming: `ses-NNN_task-sXXeYY[abcd]` (Friends) — TR-major, parcel-minor.
Values: float32, z-scored per run per parcel (range ≈ ±3.9 in spot check).

### 2.2 Transcripts (TR-aligned, word-level)

| Path | Files | Schema |
|------|-------|--------|
| `stimuli/transcripts/friends/s1/friends_s01eXX[ab].tsv` | 48 | tab-sep, 4 cols |
| `stimuli/transcripts/friends/s2/friends_s02eXX[ab].tsv` | 48 | tab-sep, 4 cols |

Columns (one row per TR):
- `text_per_tr`: concatenated text in TR
- `words_per_tr`: stringified python list of words (parse with `ast.literal_eval`)
- `onsets_per_tr`: list of float seconds (chunk-relative)
- `durations_per_tr`: list of float seconds

Empty TRs have `[]` (silence).

Sample non-empty row: `{'words_per_tr': '["There\'s"]', 'onsets_per_tr': '[18.97]', 'durations_per_tr': '[0.176]'}`.

---

## 3. Mini-run scaffold (`/tmp/p9_paradigm_a_prime_mini.py`)

### 3.1 What's wired

- `iter_friends_chunks()` — per-chunk `(BOLD, words, onsets, durations)` iterator.
- `canonical_hrf_kernel()` — SPM double-gamma at 2 Hz, 32 taps, peak at +5 s.
- `assign_token_to_tr()` — `floor(onset / 1.49)` per spec §2.3 step 2.
- `tr_bin_hidden_states()` — mean over tokens within each TR (spec §2.3 step 4).
- `convolve_decimate()` — HRF conv at internal 2 Hz, decimate by factor 3 → 1/TR Hz.
- `gamma_mse_loss()` — z-scored MSE (spec §2.1).
- `f4_pearson_per_vertex()` — per-parcel Pearson r vs. measured BOLD.
- `f4_verdict()` — tiered verdict against thresholds bronze 0.10 / silver 0.20 / gold 0.30 / aspirational 0.50.
- `build_run_plan()` — manifest builder (called by `--dry-run`).

### 3.2 What's intentionally NOT wired

- **No model loading.** Llama-3.2-3B + LoRA + projector P_S are deferred to Phase-2 entry sign-off. Scaffold raises `SystemExit(0)` with explicit message if invoked without `--dry-run`.
- **No training loop.** AdamW, scheduler, gradient checkpointing — none. Add when Phase-2 gate opens.
- **No tensor backend.** Numpy only; promote to torch+autograd before training.

### 3.3 F4 tiered thresholds (sanity confirmed against spec §4.3)

| Tier | F4_lang threshold | Source |
|------|-------------------|--------|
| bronze | 0.10 | above-chance brain alignment |
| silver | 0.20 | weak text-only encoding-model parity (early Huth-lab) |
| gold | 0.30 | contemporary encoding-model parity (Lebel 2023, TRIBE v2) |
| aspirational | 0.50 | exceeds published SoTA — spec flags as unrealistic for mini-run |

Gate to Phase 2 full per spec §6.1 step 2: F4-bronze (`F4_lang ≥ 0.10`) within 5 K steps.

---

## 4. Cost re-estimate (post-download, anchored on actual data sizes)

Pre-flight numbers vs. spec §3.1 estimates:

| Metric | Spec estimate | Actual (sub-01 s01-s02) |
|--------|---------------|--------------------------|
| Train chunks | ~100 | 94 |
| Token count | ~200 K | 118 484 |
| TR-steps | ~20 K | 44 911 |
| Disk footprint | ~5 GB | **0.585 GB** |

Tokens came in ~40 % lower than spec; TR-steps ~2× higher. Net compute load is comparable.

**Updated 1×H100 spot estimate** (Llama-3.2-3B + LoRA-r16 + P_S rank 256 + 32-tap HRF conv1d):

| Tier | Steps | Wall (compute) | Wall (e2e w/ I/O + eval) | Cost @ 2.20 USD/h |
|------|-------|----------------|--------------------------|-------------------|
| Low  | 5 000 | 33 min @ 2.5 step/s | 2.0–2.5 h | **5–6 USD** |
| Mid  | 7 500 | 50 min | 2.5–3.5 h | 6–8 USD |
| High | 10 000 | 67 min | 3.5–4.5 h | 8–10 USD |

Spec band of 5–18 USD remains valid; **revised midpoint ≈ 6–10 USD** given lower token count cuts I/O cost.

Storage on RunPod node: 1 GB persistent volume sufficient; ephemeral 5 GB scratch ample.

---

## 5. F4 holdout chunks (locked)

- `s02e24a` and `s02e24b` excluded from `iter_friends_chunks` train iteration.
- Eval cadence: every 500 steps.
- Statistical sanity: phase-randomization null per spec §4.4 (compute on first eval pass; cache null distribution).

---

## 6. Phase-2 entry gating (no execution until)

Per spec §6.1 step 2:

1. Pre-flight (THIS DOC) — DONE.
2. Wire LoRA + P_S — DEFERRED.
3. γ-only training run — GATED.
4. Gate decision: `F4_lang ≥ 0.10` within 5 K steps → proceed to extended γ-only on Lebel 2023 supplement.

Decision authority: Anima research lead. No execution without explicit prompt.

---

## 7. Honest C3 (3 mandatory caveats from spec §7, restated for runbook)

1. **License heterogeneity.** cNeuroMod-derived BOLD + transcripts are CC-BY 4.0; underlying Friends video is Warner Bros. copyright. We never redistribute video. Transcripts are short quotations consumed only as training input — a model release derived from this run still requires legal sign-off before publication. (Spec §7 caveat 4.)

2. **Hemodynamic temporal smearing.** TR=1.49 s + canonical HRF (peak +5 s, undershoot +15 s) imposes a hard ceiling on the temporal resolution Paradigm A' can ever match. Sub-second integration / ignition signatures (50–300 ms) are invisible to BOLD. F4 success means we match the slow envelope only — not "brain integration" in the IIT/GWT sense. (Spec §7 caveat 1, §5.)

3. **Vertex/parcel resolution mismatch.** `loss_design.json` references fsaverage5 (10 242 v/hemi). Algonauts 2025 ships at Schaefer-1000 parcels — coarser, ~163× fewer "vertices." Our γ-target dimensionality is 1 000, not 20 484. Cross-dataset comparisons against Lebel 2023 (full fsaverage 163 842 / hemi → must downsample to fsaverage5) require a separate `mri_surf2surf` step. P_S architecture must therefore be parameterized by output dim, not hard-wired. (Spec §1 vertex clarification, §4.1 cross-dataset holdout.)

---

## 8. Pointers / next steps

- Author state config: `state/p9_paradigm_a_prime_data_v0/manifest.json` (one entry per chunk: chunk_id, n_tokens, n_tr, holdout flag).
- Wire torch model in `mini_run` Phase-2 entry PR (deferred).
- Confirm P_S projector spec implementation supports configurable output dim (1 000 ↔ 20 484).
- Optional: fetch `stimuli/transcripts/movie10/` and `fmri/sub-01/func/sub-01_task-movie10_*` to add ~6 h additional training data (~92 MB extra disk).

---

*End of runbook. Pre-flight DONE; training EXECUTION DEFERRED to Phase-2 sign-off.*
