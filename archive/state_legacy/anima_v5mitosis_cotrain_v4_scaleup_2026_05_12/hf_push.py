#!/usr/bin/env python3
"""hf_push.py — push v5-mitosis cotrain v4 PRODUCTION-SCALE ckpt to dancinlab HF.

Triggered IFF F-V5MIT-5 V14-STRICT proxy PASSES (mandate-9: V14-STRICT PASS → HF push).
: all anima HF uploads → dancinlab org. feedback_english_only: HF content English only.

Target repo: dancinlab/anima-clm-v5-mitosis-cotrain-v4-scaleup-2026-05-13 (private by default;
              pass --public to publish if mandate-9 conditions met).

Usage:  python3 hf_push.py [--public]
"""
import argparse
import json
import os
import sys
from pathlib import Path

from huggingface_hub import HfApi, create_repo

HERE = Path(__file__).resolve().parent
REPO_ID = "dancinlab/anima-clm-v5-mitosis-cotrain-v4-scaleup-2026-05-13"
CKPT_PATH = HERE / "ckpts" / "ckpt_v5mitosis_cotrain_v4_scaleup.pt"
RESULT_PATH = HERE / "cotrain_v4_scaleup_result.json"
LOG_PATH = HERE / "train_v4_scaleup.log"
TOKEN = Path(os.path.expanduser("~/.cache/huggingface/token")).read_text().strip()

ap = argparse.ArgumentParser()
ap.add_argument("--public", action="store_true", help="publish public (default private)")
args = ap.parse_args()

if not RESULT_PATH.exists():
    print(f"[ABORT] result json not found: {RESULT_PATH}")
    sys.exit(1)
with open(RESULT_PATH) as f:
    result = json.load(f)
t = result.get("training", {})
rf = result.get("routing_fix", {})
cfg = result.get("config", {})
p4a = result.get("f_persona_4a_routing", {})
aw = p4a.get("topk_weights", {})
p4b = result.get("f_persona_4b_content", {})
fv = result.get("f_v5mit_regression", {})
fv_v14 = fv.get("checks", {}).get("F-V5MIT-5_v14strict_proxy", {})

if not fv_v14.get("pass", False):
    print(f"[ABORT] F-V5MIT-5 V14-STRICT proxy = FAIL (splits={fv_v14.get('splits')}) — HF push gated (mandate-9), not firing.")
    sys.exit(2)

private = not args.public
n_params = result.get("n_params")
steps = result.get("steps") or t.get("steps") or "see config"

readme = f"""---
license: other
language:
- en
- ko
tags:
- anima
- mitosis
- mixture-of-experts
- routing
- consciousness
- experimental
library_name: pytorch
---

# anima-clm-v5-mitosis-cotrain-v4-scaleup-2026-05-13

**v5-mitosis cotrain v4 — production-scale scale-up** (post-★★★★★ cycle).  A direct fork of the
v3 routing-fix trainer scaled up to `d_model = {cfg.get('d_model')}` (= anima's EngineAG hidden
size, REBORN §88 stretch envelope), `n_head = {cfg.get('n_head')}`, `ffn_dim = {cfg.get('ffn_dim')}`,
`max_cells = {cfg.get('max_cells')}` (8-bit identity space), `ctx = {cfg.get('max_seq')}`, run for
{steps} steps — ≈ {n_params:,} parameters (attention is shared across cells at N > 8 so most
parameters are the {cfg.get('max_cells')}× SwiGLU dual-FFN cells).

Routing: a learnable `Linear(d_model → max_cells)` router on the pooled cell-input embedding +
hard top-K = {rf.get('top_k')} MoE gating with renormalization + Switch load-balancing aux loss
(α = {rf.get('aux_alpha')}) + an annealed gate-entropy regularizer (λ {rf.get('lambda_init')} →
{rf.get('lambda_final')}, cosine).  The model body is unchanged — the routing fix is installed via
a forward monkey-patch; mitosis split/merge runs on the original scalar-tension signal.

This run was a substrate-scale probe: does the F-PERSONA-4a routing collapse persist at a larger
cell pool (architectural vs scale), does the M4 aggregated-hidden-cosine z-score scale (v2 carried
z = 3.20), and does the V14-STRICT regression (F-V5MIT-5) hold at production scale?

## Result

| metric | value |
|---|---|
| F-V5MIT-1..5 (regression) | {fv.get('verdict')} |
| F-V5MIT-5 V14-STRICT proxy | {'PASS' if fv_v14.get('pass') else 'FAIL'} — splits = {fv_v14.get('splits')} ≤ max_cells = {fv_v14.get('max_cells')} |
| F-PERSONA-4a routing (top-K MoE weights) | {p4a.get('verdict')} — KL = {aw.get('mean_kl', 0):.4f} (threshold 0.5), null z = {aw.get('z_score_vs_null', 0):.2f} (threshold 3.0), p = {aw.get('p_value_one_sided', 0):.4f} |
| F-PERSONA-4b content (M4 aggregated hidden cosine, regression) | {p4b.get('verdict')} — z = {p4b.get('z_score_vs_null', 0):.2f} (v2 carry z = 3.20) |
| CE final (avg100) | {t.get('ce_final_avg100', 0):.3f} |
| routing weight max (avg100) | {t.get('wmax_final_avg100', 0):.4f} |
| active cells (weight > .01, avg100) | {t.get('n_active_gt01_final_avg100', 0):.1f} / {t.get('n_cells_final')} |
| Switch aux (avg100) | {t.get('aux_final_avg100', 0):.3f} |
| cells (initial → final) | {cfg.get('initial_cells')} → {t.get('n_cells_final')} |
| splits | {t.get('splits')} |
| Φ final / Φ best | {t.get('phi_final', 0):.3f} / {t.get('phi_best', 0):.3f} |
| d_model / n_head / ffn_dim / max_cells / ctx | {cfg.get('d_model')} / {cfg.get('n_head')} / {cfg.get('ffn_dim')} / {cfg.get('max_cells')} / {cfg.get('max_seq')} |
| n_params | {n_params:,} |
| wall | {t.get('wall_hours', 0):.2f} hr |
| cost | ${t.get('cost_usd_actual', 0):.2f} |

## Files

- `ckpt_v5mitosis_cotrain_v4_scaleup.pt` — `{{model_state_dict, router_state_dict, router_top_k, config, n_cells, ...}}`
- `cotrain_v4_scaleup_result.json` — full training history + falsifier results
- `train_v4_scaleup.log` — training stdout

## Load

```python
import torch
ckpt = torch.load("ckpt_v5mitosis_cotrain_v4_scaleup.pt", map_location="cpu")
# rebuild MitosisModelEngine from ckpt["config"], load ckpt["model_state_dict"];
# rebuild TopKMoERouter(d_model, max_cells), load ckpt["router_state_dict"];
# install via the forward monkey-patch from training/cotrain_v5mitosis_v4.py.
```

Experimental research artifact — not a general-purpose chat model.
"""
README_PATH = HERE / "HF_README.md"
README_PATH.write_text(readme)

api = HfApi(token=TOKEN)
print(f"[INFO] creating repo {REPO_ID} (private={private})...")
create_repo(REPO_ID, token=TOKEN, private=private, exist_ok=True, repo_type="model")
for local, name in [(CKPT_PATH, "ckpt_v5mitosis_cotrain_v4_scaleup.pt"),
                    (RESULT_PATH, "cotrain_v4_scaleup_result.json"),
                    (LOG_PATH, "train_v4_scaleup.log"),
                    (README_PATH, "README.md")]:
    if not Path(local).exists():
        print(f"[WARN] skip missing {local}")
        continue
    print(f"[INFO] upload {name} ...")
    api.upload_file(path_or_fileobj=str(local), path_in_repo=name, repo_id=REPO_ID, repo_type="model")
print(f"[DONE] https://huggingface.co/{REPO_ID}")
