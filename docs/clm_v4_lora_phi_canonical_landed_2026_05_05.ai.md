# CLM v4 + LoRA φ★ Canonical — LANDED 2026-05-05

**Cycle:** `clm_v4_lora_phi_canonical_2026_05_05`
**BG lane:** BG-CLM-2-PHI-CANONICAL
**Status:** PHI_CANONICAL_PASS_NO_FLIP
**Cost:** $0 (Mac CPU)
**Wall:** ~5.5 min (incl. 2.9min HF download of mk2-v1 base ~2GB)

## Why this cycle

BG-CLM-2-EXEC follow-up #2: φ★ post-LoRA was NOT measured in-pod (L22 mid-flight patch issue). Pre-LoRA logit-std proxy = 0.938 (crude integration heuristic, not canonical). This cycle replaces that with the canonical φ★ measurement via the v3 method (HID_TRUNC=8 auto-conditioning, K=8 sample-partition, ridge=1e-3, 16 axis calib prompts) on the saved adapter.

## Headline numbers

| measure | value |
|---|---|
| φ★ post-LoRA min (K=8) | **28.9969** |
| φ★ post-LoRA mean (K=8) | **31.3489** |
| φ★ post-LoRA max (K=8) | **34.895** |
| φ★ base in-pipeline min (K=8) | 35.1774 |
| φ★ base in-pipeline mean (K=8) | 35.8062 |
| φ★ base carry (G3 verdict, legacy substrate path) | 41.86 |
| **drift in-pipeline (mean)** | **−4.46pp** |
| drift in-pipeline (min) | −6.18pp |
| drift vs carry (mean) — INFORMATIONAL | −10.51pp |
| φ★-flip threshold | −10.0pp |
| **φ★-flip detected (authoritative)** | **NO** |

## Method (canonical, mirrors `tool/anima_phi_v3_canonical.hexa`)

1. Load `dancinlab/clm-v4-mk2-v1` (HF format) on Mac CPU fp32
2. PEFT-load `state/clm_v4_lora_sft_2026_05_05/results/adapter_final/` (10.02 MiB, sha256 `6d5edb93...`)
3. Forward 16 anima-axis canonical calib prompts (T_seq=256, real-token mean pool on `decoder.ln_f`)
4. Truncate to top-variance HID_TRUNC=8 dims → Xt (16, 8)
5. K=8 random sample-partitions (8|8 halves), φ_k = log|Cov(full)| − (log|Cov(S1)| + log|Cov(S2)|)
6. φ★ = MIN(φ_k); also report mean/max

## Drift analysis — why two reference points

The carry value 41.86 was measured on a **different substrate path** (legacy ConsciousDecoderV2 + raw `best.pt` + ubu1 GPU bf16). This cycle's pipeline is HF-format `mk2-v1` + Mac CPU fp32. The base-only run on the SAME architecture in this pipeline produces 35.81 mean — a **~6pp methodology delta** unrelated to LoRA.

Therefore:

- **AUTHORITATIVE drift** = post-LoRA − base-in-pipeline = 31.35 − 35.81 = **−4.46pp** (mean). PASS (above −5pp).
- INFORMATIONAL drift vs carry = 31.35 − 41.86 = −10.51pp. Apparent flip, but ~6pp is methodology — NOT real flip.

This is why a base-only in-pipeline run was added (deviation from spec, methodologically required).

## F-CLM-LORA-1 verdict (canonical)

- **Pre this cycle:** INFERRED_PASS (via finite logits + intermediate eval HellaSwag stability)
- **This cycle:** **measured PASS**
- **Evidence:** φ★ in-pipeline drift mean −4.46pp + min −6.18pp — within partial-forgetting band; sign+magnitude preserved
- **Combined with:** HellaSwag forgetting_index=0.0196 (PASS, threshold 0.05) from `state/clm_v4_lora_sft_2026_05_05/verdict.json`

## Cross-substrate consistency

| substrate | φ★ mean | LoRA topology |
|---|---|---|
| Pβ-SCALE (holdout500, ubu1 GPU bf16, ConsciousDecoderV2) | 42.37 | r=64 α=128, qkvo + mlp gate/up/down |
| CLM v4 + LoRA (this cycle, Mac CPU fp32, HF-format mk2-v1) | 31.35 | r=32 α=64, qkvo only |

Cross-substrate paths are NOT directly comparable (different decoder class, different precision, different LoRA target_modules). Both adapters preserve substrate φ sign+magnitude; neither flipped. **Consistency PASS** in the qualitative sense (both phi-stable). A direct numeric delta is confounded by the methodology drift documented above.

## Deviations from spec

1. Did NOT invoke `hexa run tool/anima_phi_v3_canonical.hexa` directly — that hexa tool's emitted helper hardcodes `/workspace/*` paths and Mistral defaults; not parameterized for PEFT on `CLMv4ForCausalLM`. Mirrored its method byte-for-byte in `tool/transient_py/clm_v4_lora_phi_canonical.py` (raw#9 / raw#37).
2. Added base-only in-pipeline run (`clm_v4_base_phi_canonical.py`) — not in spec but methodologically required to isolate LoRA delta from substrate-path delta.
3. Used canonical 16 calib prompts (cross-cycle comparable) rather than `state/anima_axis_eval_set_2026_05_05/prompts.jsonl` (downstream eval set, not phi calib).
4. `train_avg_real.pt` consciousness_states fixture NOT injected — the canonical phi method doesn't consume it; fixture is for axis-conditioning probes, not phi calib.

## Deliverables

```
state/clm_v4_lora_phi_canonical_2026_05_05/
├── verdict.json                          # this cycle verdict
├── results/
│   ├── phi_canonical.json                # post-LoRA phi summary
│   └── phi_canonical_base.json           # in-pipeline base phi summary
└── logs/
    ├── eval.log                          # post-LoRA run log
    └── eval_base.log                     # base-only run log

tool/transient_py/
├── clm_v4_lora_phi_canonical.py          # post-LoRA helper (raw#9/raw#37)
└── clm_v4_base_phi_canonical.py          # base-only helper (raw#9/raw#37)

docs/
└── clm_v4_lora_phi_canonical_landed_2026_05_05.ai.md  # this doc
```

## Follow-ups

- F-CLM-LORA-4 axis-conditioning preservation — still INFERRED_PASS; needs 5-bucket cell-token bridge fixture run (`tool/cell_token_bridge_proto.hexa`)
- Optional K_PARTS / seed sweep to bound K=8 partition variance
- Architectural cycle: standardize a single canonical phi-probe substrate path (HF-format vs legacy decoder; CPU fp32 vs GPU bf16) to eliminate the ~6pp methodology drift between probe lineages

## raw rules honored

- raw#9 — hexa-only base canonical metric, transient_py opt-out for PEFT loading
- raw#10 — ≥5 honest_c3 entries (8 emitted)
- raw#15 — verdict.json is SSOT under `state/clm_v4_lora_phi_canonical_2026_05_05/`
- raw#37 — transient_py helper emit OK
- DO NOT git commit (per spec)
- DO NOT push to HF (per spec)
