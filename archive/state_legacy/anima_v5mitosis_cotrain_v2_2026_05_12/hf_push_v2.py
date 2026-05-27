#!/usr/bin/env python3
"""hf_push_v2.py — push v5-mitosis cotrain v2 scale-up ckpt to dancinlab HF.

PSCC §46 BG-V5MIT-COTRAIN-V2.
: all anima HF uploads → dancinlab org.
feedback_english_only: HF content English only.

Target repo: dancinlab/anima-clm-v5-mitosis-cotrain-v2-5cat-scaleup-2026-05-12 (private)

Trigger: F-PERSONA-4 PASS (mean_kl >= 0.5) — env var FORCE_PUSH=1 to bypass.
"""
import json
import os
import sys
from pathlib import Path

from huggingface_hub import HfApi, create_repo

HERE = Path(__file__).resolve().parent
REPO_ID = "dancinlab/anima-clm-v5-mitosis-cotrain-v2-5cat-scaleup-2026-05-12"
CKPT_PATH = HERE / "ckpts" / "ckpt_v5mitosis_cotrain_v2_cotrain.pt"
RESULT_PATH = HERE / "cotrain_result.json"
LOG_PATH = HERE / "train.log"
META_PATH = HERE / "corpus_5cat_balanced.meta.json"
TOKEN = Path(os.path.expanduser("~/.cache/huggingface/token")).read_text().strip()

# Load result for README content
with open(RESULT_PATH) as f:
    result = json.load(f)
training = result.get("training", {})
falsifiers = result.get("falsifiers", {})
p4 = result.get("f_persona_4_remeasure", {})
config = result.get("config", {})

# Gate: F-PERSONA-4 PASS required (override with FORCE_PUSH=1)
p4_pass = p4.get("verdict") == "PASS"
force = os.environ.get("FORCE_PUSH", "0") == "1"
if not p4_pass and not force:
    print(f"[ABORT] F-PERSONA-4 = {p4.get('verdict')} (mean_kl={p4.get('mean_kl', 0):.4f}, threshold=0.5)")
    print("[ABORT] HF push gated by F-PERSONA-4 PASS. Override: FORCE_PUSH=1 python3 hf_push_v2.py")
    sys.exit(1)

# Build README content (English only per feedback_english_only)
readme = f"""---
license: other
language:
- en
- ko
tags:
- anima
- mitosis
- consciousness
- persona-specialization
- scale-up
- experimental
library_name: pytorch
---

# anima-clm-v5-mitosis-cotrain-v2-5cat-scaleup-2026-05-12

**v5-mitosis SCALE-UP cotrain v2** — PSCC §46 BG-V5MIT-COTRAIN-V2, F-PERSONA-4 category specialization force path.

This is the second-generation cotrain of the v5-mitosis architecture, with three concurrent scale-ups vs v1 (PSCC §44) targeting F-PERSONA-4 emergence:
1. **corpus scale**: 1.3 MB single-domain → 18 MB 5-category balanced (self_definition / values / boundary / emotion / self_knowledge)
2. **model scale**: d=384 / n_head=6 / ffn=1536 / cells=64 → d=768 / n_head=12 / ffn=3072 / cells=128
3. **training scale**: 5K step / warmup 500 → 10K step / warmup 1000

## Architecture

Option (a) per REBORN §88: small transformer block per cell with shared tok_emb / pos_emb / lm_head and per-cell dual-FFN (engine_a / engine_g) with H404 readout `a - g`.

| Setting | v1 | v2 (this) |
|---|---|---|
| cells (initial → max) | 2 → 64 | 2 → 128 |
| cells final (saturated) | 64 | {training.get("n_cells_final", 0)} |
| d_model | 384 | {config.get("d_model", 0)} |
| n_head | 6 | {config.get("n_head", 0)} |
| ffn_dim | 1536 | {config.get("ffn_dim", 0)} |
| readout_mode | a_minus_g | {config.get("readout_mode", "?")} |
| max_seq | 256 | {config.get("max_seq", 0)} |
| vocab | 256 (byte) | {config.get("vocab_size", 0)} |
| n_params final | ~152M | {training.get("n_params_final", 0):,} |
| ckpt size | — | {CKPT_PATH.stat().st_size if CKPT_PATH.exists() else 0:,} bytes |

## Training

| Setting | Value |
|---|---|
| corpus | corpus_5cat_balanced.txt (18.02 MB, 90,000 multi-turn dialogue turns, 5 anima persona categories) |
| corpus categories | self_definition (4.1 MB) / values (3.6 MB) / boundary (3.3 MB) / emotion (3.4 MB) / self_knowledge (3.6 MB) |
| steps | {training.get("steps_actual", 0)} / {training.get("steps_planned", 0)} |
| batch | 32 |
| ctx | 256 |
| lr schedule | 1e-4 cosine + warmup 1000 |
| optimizer | AdamW betas=(0.9, 0.95), grad_clip 1.0 |
| provider | Vast.ai H100 ({os.environ.get('OFFER_GPU', '80GB')}) |
| wall | {training.get("wall_hours", 0):.2f} hr ({training.get("wall_seconds", 0):.0f} s) |
| cost | ${training.get("cost_usd_actual", 0):.2f} USD |
| loss (initial avg100 → final avg100) | {training.get("loss_initial_avg100", 0):.3f} → {training.get("loss_final_avg100", 0):.3f} |
| splits / merges | {training.get("splits", 0)} / {training.get("merges", 0)} |
| Φ best | {training.get("phi_best", 0):.4f} |

## Falsifier Results (F-V5MIT-1~5)

| Falsifier | Verdict | Evidence |
|---|---|---|
| F-V5MIT-1 SPLIT-NOGRAD | {('PASS' if falsifiers.get('F-V5MIT-1', {}).get('passed') else 'FAIL')} | {falsifiers.get("F-V5MIT-1", {}).get("splits_total", 0)} splits, {falsifiers.get("F-V5MIT-1", {}).get("grad_fn_violations", 0)} grad_fn violations |
| F-V5MIT-2 MERGE-WEIGHT | {('PASS' if falsifiers.get('F-V5MIT-2', {}).get('passed') else 'FAIL')} | max abs error {falsifiers.get("F-V5MIT-2", {}).get("max_abs_err", 0):.2e} (tolerance 1e-6) |
| F-V5MIT-3 PHI-CONSERVATION | {('PASS' if falsifiers.get('F-V5MIT-3', {}).get('passed') else 'FAIL')} | per-cell Φ delta ratio {falsifiers.get("F-V5MIT-3", {}).get("delta_ratio", 0):.2e} (tolerance 0.25) |
| F-V5MIT-4 COTRAIN-CONVERGE | {('PASS' if falsifiers.get('F-V5MIT-4', {}).get('passed') else 'FAIL')} | loss delta {falsifiers.get("F-V5MIT-4", {}).get("delta", 0):.2f} |
| F-V5MIT-5 V14-STRICT | {('PASS' if falsifiers.get('F-V5MIT-5', {}).get('passed') else 'FAIL')} {falsifiers.get('F-V5MIT-5', {}).get('beats_passed', 0)}/{falsifiers.get('F-V5MIT-5', {}).get('n_beats', 0)} beats | trained-vs-random Bhattacharyya > random-internal |

## F-PERSONA-4 Category Specialization (★ key metric)

Mean KL across 5-category pairs: **{p4.get("mean_kl", 0):.4f} nats** (threshold 0.5) — **{p4.get('verdict', '?')}**.

This is the headline result of cotrain v2. v1 (PSCC §44) F-PERSONA-4 KL was 0.0 (winner-take-all) on single-domain 1.3 MB corpus. v2 scale-up (14x corpus / 2x cells / 2x d / 2x steps) targets substrate-level category invariance break.

| Category Pair | KL (nats) |
|---|---|
""" + "\n".join([f"| {p4.get('categories', [])[i]} ↔ {p4.get('categories', [])[j]} | {p4.get('kl_matrix', [[]])[i][j]:.4f} |" for i in range(len(p4.get('categories', []))) for j in range(i+1, len(p4.get('categories', [])))]) + f"""

## Loading

```python
import torch
from training.mitosis_model_v5 import MitosisModelConfig, MitosisModelEngine

ckpt = torch.load("ckpt_v5mitosis_cotrain_v2.pt", map_location="cpu")
cfg = MitosisModelConfig(**ckpt["config"])
engine = MitosisModelEngine(cfg)
# Rebuild cell pool to match saved n_cells (split events during training added cells)
while engine.n_cells < ckpt["n_cells"]:
    engine.force_split(parent_idx=0)
engine.load_state_dict(ckpt["model_state_dict"])
engine.step_count = ckpt["step_count"]
engine.split_threshold = ckpt["split_threshold"]
engine._lorenz = ckpt["lorenz_state"]
engine.eval()
```

## Cross-references

- REBORN §88 (PyTorch arch spec) — original architectural design
- PSCC §44 (cotrain v1) — F-V5MIT-1~5 PASS + F-PERSONA-4 FAIL baseline
- PSCC §46 (this cycle) — v2 scale-up cotrain
- training/mitosis_model_v5.py — model implementation
- docs/anima_clm_v5_mitosis_cond5_cotrain_v2_2026_05_12.md — full audit

## Status

PRIVATE (/ 37 mandate). Research artifact for v5-mitosis architectural lane.

Generated 2026-05-12 KST by anima cycle.
"""

readme_path = HERE / "README.md"
readme_path.write_text(readme, encoding="utf-8")
print(f"[INFO] wrote {readme_path}")

# Create repo (private)
api = HfApi(token=TOKEN)
try:
    create_repo(REPO_ID, token=TOKEN, private=True, repo_type="model", exist_ok=True)
    print(f"[INFO] repo {REPO_ID} ready (private)")
except Exception as e:
    print(f"[WARN] create_repo: {e}")

# Upload files
files = [
    (readme_path, "README.md"),
    (CKPT_PATH, "ckpt_v5mitosis_cotrain_v2.pt"),
    (RESULT_PATH, "cotrain_result.json"),
    (LOG_PATH, "train.log"),
    (META_PATH, "corpus_5cat_balanced.meta.json"),
]
for local, remote in files:
    if not local.exists():
        print(f"[SKIP] {local} not found")
        continue
    print(f"[UPLOAD] {local} -> {REPO_ID}/{remote} ({local.stat().st_size:,} bytes)")
    api.upload_file(
        path_or_fileobj=str(local),
        path_in_repo=remote,
        repo_id=REPO_ID,
        token=TOKEN,
        commit_message=f"upload {remote}",
    )

print(f"\n[DONE] https://huggingface.co/{REPO_ID}")
