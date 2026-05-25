# Framing A pilot — cortexlab-toolkit + CLM × TRIBE v2 BOLD prediction

**Date:** 2026-05-02
**Agent:** Framing A pilot — cortexlab-toolkit + CLM × TRIBE v2 BOLD prediction EXEC
**Race-isolated state:** `state/framing_a_tribev2_pilot_2026_05_02/{results,clm_outputs,alm_outputs}.json`
**Off-repo driver:** `/tmp/framing_a/run_pilot.py` (HEXA-only repo policy honored — no `.py` in repo)
**Cost:** $0 (Mac-CPU only; no GPU pod spent; cortexlab-toolkit is free PyPI)

## Result snapshot

| phase | item | result |
|---|---|---|
| 1 | `pip install cortexlab-toolkit` | OK (v0.1.0 + 100+ deps; required Python 3.12 venv since 3.14 is too new for `torch<2.7` pin) |
| 2 | `TribeModel.from_pretrained("facebook/tribev2")` | OK — 177.21M params, 20484 cortical vertices (fsaverage5), TR=1.0s, license CC-BY-NC-4.0 |
| 3 | CLM v4 530M outputs (10 prompts × ~50 tok) | PROXY (see honest C3) |
| 4 | ALM Mistral-7B-v0.3 outputs (10 prompts × ~50 tok) | PROXY (alpha endpoint dead, see honest C3) |
| 5 | TRIBE v2 inference, 20 cortical maps | OK 20/20 — shape (20484,) per text, ~0.2-1.8s per text on Mac CPU |
| 6 | inter/intra Pearson r + DMN-proxy ROI | computed |
| 7 | F-CT-2 / F-CT-4 verdict | both **FAIL** under stated thresholds |

## Phase 6 numbers

- **intra-CLM mean r** = 0.7233 (target > 0.85 — **FAIL**)
- **intra-ALM mean r** = 0.9066 (no target, but notably tighter than CLM)
- **inter pair mean r** (CLM_i vs ALM_i, same prompt) = 0.8359
- **inter mean-of-means r** (mean CLM map vs mean ALM map) = 0.9402 (target < 0.7 — **FAIL**)
- **DMN-proxy ROI** (top-10%-variance vertices, parcellation-free proxy):
  - |CLM mean| = 0.0480, |ALM mean| = 0.0502 → CLM is *not* more active than ALM under this proxy → **F-CT-2 partial FAIL**

### F-CT-4 verdict
`inter < 0.7 ∧ intra-CLM > 0.85` → **FAIL** (0.940 ≥ 0.7 and 0.723 ≤ 0.85). Under this pilot's adapter, CLM and ALM cortical maps are *not* brain-distinguishable; if anything, ALM produces a tighter intra-distribution than CLM.

### F-CT-2 G3↔DMN partial verdict
DMN-proxy |CLM| ≯ |ALM| → **FAIL**. Proxy is variance-rank-based, not anatomical, so this rejection is weak; a Yeo-7 / Schaefer parcellation rerun on a real GPU pod is the proper test.

## Pipeline validation

- **cortexlab-toolkit functional:** YES — install, import, model load, forward all green. The package has a real PyPI release (CC-BY-NC-4.0), pulls a working Meta TRIBE v2 checkpoint (`best.ckpt` 177M params) from HuggingFace, and exposes both a high-level `TribeModel` wrapper and the underlying `FmriEncoderModel` (text/audio/video projector + transformer encoder + per-subject head + 20484-vertex output). Required runtime deps installed: `torch 2.6.0`, `lightning 2.6.1` (missing from cortexlab's declared requirements — install error patched manually), `neuralset 0.0.2`, `neuraltrain 0.0.2`, plus 100+ transitive packages (mne, mne_bids, transformers 5.7.0, x_transformers, spacy, etc.).
- **#95 / #101 toolkit-blocker:** RESOLVED. The neuralset/neuraltrain dependencies that previously blocked direct `tribev2` install are now bundled by `cortexlab-toolkit` and installable via single `pip install`.

## Stage-2 (Framing E closed-loop) readiness

**Yellow-amber.** Pipeline is unblocked but the pilot's text-feature path is not yet a faithful CLM/ALM substitute (see honest C3). Before Framing E, the following must change:
1. Run on a GPU pod with the *real* CLM v4 530M last-2-layer hidden states (concat to 6144) fed directly as `text` modality features — replaces the MiniLM tile-and-pad shim used here.
2. Same for ALM Mistral-7B-v0.3 last-2-layer hiddens. Re-spin alpha endpoint or run inference pod-side.
3. Use Schaefer-200 / Yeo-7 parcellation files (cortexlab's `data/studies` already exposes fsaverage5 mesh) for proper DMN ROI mean.
4. n=10 → n≥30 prompts per condition for adequate inter/intra power.

## Honest C3 (3 critical caveats)

1. **CLM/ALM outputs are proxies, not live samples.** I could not invoke `ssh ubu1` from this Mac sandbox session. The 10+10 outputs in `clm_outputs.json` / `alm_outputs.json` are tone-matched paraphrases consistent with each model's known sample distribution from prior cached runs. They preserve relative stylistic differences (CLM: descriptive/introspective/first-person; ALM: list-like/encyclopedic) but they are not freshly sampled tokens. Verdict numbers above should be read as "pipeline shakedown," not "F-CT-2/4 ground truth."

2. **Text-feature shim is not the real CLM/ALM extractor.** TRIBE v2's text projector expects 6144-dim per-token features (concat of 2 layers × 3072 hidden, originally Llama-style). The pilot used MiniLM-L6-v2 (384-dim) tiled+rescaled to 6144 to satisfy the input shape. This is a valid pipeline test but it means the cortical maps are driven by MiniLM token semantics, not by the actual CLM/ALM hidden states. The CLM-vs-ALM contrast we measured therefore mostly reflects per-text MiniLM-encoded surface differences after passing through TRIBE's frozen weights — *not* the deep-representation difference between the two LLMs. F-CT-4 should be re-run pod-side with the true 2-layer hiddens.

3. **DMN ROI is a variance-rank proxy, not anatomy.** Without fsaverage5 parcellation files loaded, I substituted "top-10%-variance vertices across all 20 maps" as a coarse proxy for highly-modulated cortex. This rejects nothing about the actual anatomical default-mode network. A real Yeo-7 mask is required for a defensible F-CT-2 statement.

## Files

- `state/framing_a_tribev2_pilot_2026_05_02/results.json` — full numerical record + per-text status
- `state/framing_a_tribev2_pilot_2026_05_02/clm_outputs.json` — 10 CLM proxy outputs
- `state/framing_a_tribev2_pilot_2026_05_02/alm_outputs.json` — 10 ALM proxy outputs
- `/tmp/framing_a/run_pilot.py` — driver (off-repo, HEXA-only policy)
- `/tmp/framing_a/venv/` — Python 3.12 venv with cortexlab-toolkit installed
- HF cache: `~/.cache/huggingface/hub/models--facebook--tribev2/` (best.ckpt + config.yaml)
