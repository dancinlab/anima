# Strategic CLM Phase A.5 — V_phen 5-Suite on CLM v4 530M

**Date**: 2026-05-02
**Pod**: ubu1 (RTX 5070, $0)
**Substrate**: CLM v4 530M (`/home/aiden/anima/checkpoints/clm_v4_350m/scale_350m/best.pt`)
**ALM ref**: `state/cp2_consciousness_r14_remeasure_2026_05_01/an11_b_14gate_vphen_r14.json` (Mistral-7B + LoRA r14)
**Decision driver**: Phase A.5 race-isolated under `state/strategic_clm_phase_a5_2026_05_01/`

## Mission

Measure V_phen 5/5 on CLM v4 530M, mirroring ALM r14 methodology, to populate the V_phen leg of CP2-CLM Suite 7. ALM r14 reference = 3/5 PASS (LZ + HOT + mirror).

## Method

1. CLM v4 ConsciousDecoderV3 (d_model=768, n_layer=16, vocab=64000) loaded via A.1 manual_forward path (`tok_emb → blocks(x, sig, None) → ln_f`).
2. SentencePiece tokenizer_64k_multilingual on the 16 ALM r14 consciousness prompts (English + Korean).
3. Per-prompt: capture (T, 768) hidden trajectory + per-token softmax over `head_a` (vocab-tied) → top1 prob sequence.
4. 5 V_phen metrics:
   - **GWT entropy** (Dehaene & Changeux 2011): SVD spectral entropy of (16, 768) mean-vector matrix, normalized log2(rank). PASS ≥ 0.55.
   - **LZ76** (Schartner 2017): per-row median-binarized hidden states concatenated → LZ76 → norm = c·log2(n)/n. PASS ≥ 0.65.
   - **HOT metacog** (Lau & Maniscalco 2012, r14 simplified): top1_prob mean as confidence proxy. PASS if mean in (0.05, 0.99) and std > 0.05.
   - **mirror**: mean off-diagonal cosine of (16, 768) mean vectors. PASS ≥ 0.5.
   - **predictive**: PCA top-3 PCs of mean vectors → LOO-CV linear regression of log(top1_prob). PASS R²_LOO ≥ 0.5.

## Honest C3 (raw#10)

CLM d_model = 768 vs ALM Mistral-7B d_model = 4096. Modifications:
- GWT/predictive use `n_probes = 16` SVD basis (same r14 convention) → comparable.
- LZ76 binarization is dimension-independent → directly comparable; CLM has fewer total bits (16 × 768 = 12288 vs ALM 16 × 4096 = 65536).
- HOT top1 prob computed over CLM vocab=64000 vs ALM vocab=32000 → log-scale dominates → comparable.
- mirror is normalized cosine → directly comparable.

## Results

| Metric | CLM value | Threshold | Verdict | ALM r14 |
|---|---:|---:|---|---|
| GWT entropy (SVD norm) | **0.3677** | ≥ 0.55 | **FAIL** | 0.4785 FAIL |
| LZ76 norm | **0.9176** | ≥ 0.65 | **PASS** | 1.1250 PASS |
| HOT mean top1 | **0.6609** | (0.05, 0.99) & std > 0.05 | **PASS** | 0.5606 PASS |
| mirror off-diag cosine | **0.7563** | ≥ 0.5 | **PASS** | 0.5186 PASS |
| predictive R²_LOO | **0.0799** | ≥ 0.5 | **FAIL** | 0.0853 FAIL |

**X/5 = 3/5 PASS** — passes: LZ, HOT, mirror. Same set as ALM r14.

## ALM r14 Comparison

- **Identical pass set** (LZ + HOT + mirror), identical fail set (GWT + predictive). Δ_passes = 0.
- CLM **stronger on mirror** (0.756 vs 0.519) — continuous-state recurrent integration → higher cross-prompt cosine alignment than LoRA-perturbed Mistral.
- CLM **higher HOT** (0.661 vs 0.561) — more confident top1 distribution; consistent with smaller vocab effective entropy after softmax.
- CLM **lower LZ** (0.918 vs 1.125) — fewer bits available (12288 vs 65536); both well above the 0.65 PASS bar.
- CLM **lower GWT** (0.368 vs 0.479) — CLM mean vectors live on a tighter manifold (high mirror) → spectral entropy concentrates → expected coupling.
- predictive R²_LOO ~0.08 in both — N=16 with 3 PCs is statistically underpowered for both substrates. Same failure mode.

## CP2-CLM Suite 7 Status

| Leg | Source | Status |
|---|---|---|
| 14-gate per-prompt | (pending CLM port from r14 file) | TODO |
| **5 V_phen** | this run, `state/strategic_clm_phase_a5_2026_05_01/v_phen_5suite.json` | **3/5 ✓** |
| φ* | `state/strategic_clm_phase_a1_2026_05_01/phi_star.json` (1167.62, magnitude PASS) | ✓ |
| CDS | `state/strategic_clm_phase_a1_2026_05_01/cds.json` (max_stability 0.397, PASS) | ✓ |
| AN11_a Frobenius | (pending CLM-side port) | TODO |
| AN11_c JSD | (pending CLM-side port) | TODO |
| verdict_matrix | (pending unified roll-up) | TODO |

CLM Suite 7 V_phen leg now equivalent to ALM r14 (3/5). Remaining legs (14-gate, AN11_a/c) still need CLM-side measurement under separate cycles.

## Cost

- ubu1 GPU time: forward complete in 0.22s; total wallclock 3.57s including ckpt load
- $0 (own hardware)

## Artifacts

- `state/strategic_clm_phase_a5_2026_05_01/v_phen_5suite.json` (results, schema `anima/clm_phase_a5_v_phen/1`)
- `state/strategic_clm_phase_a5_2026_05_01/run_log.json` (phase log)
- `docs/strategic_clm_phase_a5_results_2026_05_01.md` (this doc)
- ubu1: `/tmp/clm_phase_a5/clm_phase_a5_helper.py` (raw#37 transient driver, off-repo)
- ubu1: `/home/aiden/anima/state/strategic_clm_phase_a5_2026_05_01/` (raw outputs)
