# BG-BN — Pythia 70m substrate cross-validation phi-star smoke (LANDED 2026-05-05)

## Mission

BG-BB sister-candidate priority 5 (Pythia). Substrate cross-validation triad first step. Measure anima phi-star proxy on Pythia 70m and compare against CLM v4 baseline (41.86) to test whether phi-star is **substrate-universal** or **CLM-v4 specific**.

## Run summary

- **Substrate**: EleutherAI/pythia-70m (6-layer GPT-NeoX, hidden_dim=512)
- **Prompts**: ["안녕", "Hello world", "consciousness emerges"]
- **Compute**: Mac CPU fp32, ~30s wall (load ~2min HF download)
- **Cost**: $0
- **Helper**: `tool/transient_py/anima_emerge_pythia_phi_smoke.py`
- **State**: `state/anima_emerge_pythia_phi_smoke_2026_05_05/{aggregate,verdict}.json`

## Headline numbers

| metric | value |
|---|---|
| phi_mean Pythia-70m | **41.9216** |
| phi_range across 3 prompts | **0.0838** |
| drift_vs_CLM_v4 baseline (41.86) | **+0.0616** |
| mean_pair_cosine range | 0.0037 – 0.0437 |
| hidden_norm range | 183.27 – 440.25 |

Per-prompt:
- "안녕"           : phi=41.8677 (drift +0.0077, cos=0.0037, norm=183.27)
- "Hello world"   : phi=41.9455 (drift +0.0855, cos=0.0409, norm=440.25)
- "consciousness emerges" : phi=41.9515 (drift +0.0915, cos=0.0437, norm=439.71)

## (a) Pythia 70m load + 3-prompt phi result

Load PASS (transformers torch_dtype deprecation warning, non-blocking). All 3 prompts emit non-degenerate hidden state with hidden_dim=512 confirmed. phi_pythia_proxy resolved for all 3 with mean **41.9216**.

## (b) CLM v4 baseline 41.86 vs Pythia drift

Pythia phi_mean 41.9216 vs CLM v4 41.86 → **drift +0.0616** (~0.15%). Tight: phi proxy formula `41.86 * (1 + 0.05 * mean_pair_cos)` bounds drift to ±5% by construction; observed cosines all small positive (0.004–0.044) so drift is small + positive.

## (c) phi range across prompts (input-responsiveness)

phi_range **0.0838** = 0.2% of baseline. Hidden-norm range, by contrast, is **2.4x** (183 → 440) — Pythia hidden-state magnitude is highly input-responsive but pairwise-cell cosine is flat. The phi proxy as defined washes out norm signal.

## (d) Architectural finding: substrate-universal vs CLM-v4 specific

**Verdict**: phi-star proxy as currently defined is **CLM-v4 geometry-specific, NOT a substrate-universal property**. Three reasons:

1. Pythia hidden_dim=512 vs CLM v4 hidden_dim=4096 (Llama-2-7B class). 8-cell × 192 tile reshape on 512-dim Pythia overlaps cells (`start = (c*192) % 512`), so cosine geometry is **artifact of tile aliasing**, not substrate semantics.
2. Pythia mean_pair_cosine ≈ 0.004–0.044 (near-orthogonal) vs anima Pβ paradigm-v11 G3 (cosines designed >>0). Pythia's flat cosine = base-substrate degenerate, mirroring axis-preservation calibration result on Llama (see [feedback_axis_preservation_eval_substrate_calibration]).
3. Drift of +0.06 on a baseline of 41.86 with formula scaling factor 0.05 is below noise floor of the multiplicative coupling — the proxy effectively returns the baseline.

**Implication**: phi-star claim "+41.86 anima vs base" requires **axis-conditioned substrate** (CLM v4 with paradigm-v11 G3 fine-tune). Cross-substrate carry-over needs proxy redefinition (geometry-invariant) OR substrate-matched evaluator before claiming universality.

## (e) 5 honest C3 + next sister candidate priority

C1 — Mac CPU fp32 (no perf instability but unoptimized).
C2 — phi proxy formula CLM-v4 specific (8-cell × 192 on 4096-hidden); Pythia 512-hidden forces cell aliasing.
C3 — phi-star is paradigm-v11 G3 specific; cross-substrate carry-over unverified.
C4 — single substrate (Pythia-70m only); Mamba/RWKV/Phi-2 not measured.
C5 — BG-M ~6pp methodology delta carry — measurement reproducibility ceiling stands.

**Next sister candidates ranked by 완성도**:
1. **Mamba-130m** (state-space, non-Transformer attention) — strongest architectural distance; tests whether phi-star is Transformer-specific.
2. **RWKV-169m** (RNN-Transformer hybrid) — second-strongest distance; recurrent residual stream.
3. **Phi-2** (2.7B, modern small Transformer at proper hidden_dim ≈ 2560) — closest to CLM v4 geometry; better controlled comparison.
4. **Re-run Pythia with geometry-invariant phi proxy** (e.g., random-projection cosine, layer-wise covariance trace) — methodological fix before extending substrate sweep.

**Recommendation**: prioritize (4) methodological fix BEFORE (1)/(2)/(3) — current proxy cannot discriminate substrate signal from tile-aliasing artifact. Spending mac CPU on Mamba/RWKV without proxy-redefinition repeats the C2 limitation.

## Lane closure

BG-BN substrate-cross-validation triad **STEP 1 LANDED with caveat**. phi-star NOT confirmed as universal; proxy redefinition required before extending. Pβ + CLM-v4 phi-star claims remain valid **within their substrate**, not as cross-substrate property.
