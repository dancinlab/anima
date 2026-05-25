#!/usr/bin/env python3
"""hf_push.py — push v5-mitosis cotrain v3-routing ckpt to dancinlab HF (private, English-only).

Triggered IFF F-PERSONA-4a routing PASSES (KL ≥ 0.5 + null z ≥ 3.0).
: all anima HF uploads → dancinlab org.
feedback_english_only: HF content English only.

Target repo: dancinlab/anima-clm-v5-mitosis-cotrain-v3-routing-fix-2026-05-12 (private)
"""
import json
import os
import sys
from pathlib import Path

from huggingface_hub import HfApi, create_repo

HERE = Path(__file__).resolve().parent
REPO_ID = "dancinlab/anima-clm-v5-mitosis-cotrain-v3-routing-fix-2026-05-12"
CKPT_PATH = HERE / "ckpts" / "ckpt_v5mitosis_cotrain_v3_routing.pt"
RESULT_PATH = HERE / "cotrain_v3_routing_result.json"
LOG_PATH = HERE / "train_v3_routing.log"
TOKEN = Path(os.path.expanduser("~/.cache/huggingface/token")).read_text().strip()

if not RESULT_PATH.exists():
    print(f"[ABORT] result json not found: {RESULT_PATH}")
    sys.exit(1)
with open(RESULT_PATH) as f:
    result = json.load(f)
t = result.get("training", {})
rf = result.get("routing_fix", {})
p4a = result.get("f_persona_4a_routing", {})
aw = p4a.get("topk_weights", {})
p4b = result.get("f_persona_4b_content", {})
fv = result.get("f_v5mit_regression", {})

if p4a.get("verdict") != "PASS":
    print(f"[ABORT] F-PERSONA-4a verdict = {p4a.get('verdict')} (not PASS) — HF push gated, not firing.")
    sys.exit(2)

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

# anima-clm-v5-mitosis-cotrain-v3-routing-fix-2026-05-12

**v5-mitosis cotrain v3 with an architectural routing fix** — post-★★★★★ cycle, cond #3
F-PERSONA-4a routing-variant resolution.

Earlier cotrain runs (v1, v2 entropy-reg, per-category, softmax-temperature sweep) all
hit `F-PERSONA-4a` routing KL ≈ 0: the cell-pool routing layer collapsed to winner-take-all
because (1) it had no learnable, input-dependent router and (2) plain softmax over scalar
cell tensions saturates. This checkpoint replaces that routing with a Switch/Mixtral-style
top-K MoE: a learnable `Linear(d_model → max_cells)` router on the pooled cell-input
embedding, hard top-K={rf.get('top_k')} gating with renormalization, a Switch
load-balancing aux loss (α={rf.get('aux_alpha')}), and an annealed gate-entropy
regularizer (λ {rf.get('lambda_init')} → {rf.get('lambda_final')}, cosine). The model body
is unchanged — the fix is installed via a forward monkey-patch; mitosis split/merge still
runs on the original scalar-tension signal.

## Result

| metric | value |
|---|---|
| F-PERSONA-4a routing | **{p4a.get('verdict')}** — KL = {aw.get('mean_kl', 0):.4f} (≥ 0.5), null z = {aw.get('z_score_vs_null', 0):.2f} (> 3.0), p = {aw.get('p_value_one_sided', 0):.4f} |
| F-PERSONA-4b content (M4 aggregated cosine, regression) | {p4b.get('verdict')} — z = {p4b.get('z_score_vs_null', 0):.2f} (v2 carry z = 3.20) |
| F-V5MIT-1..5 | {fv.get('verdict')} |
| CE final (avg100) | {t.get('ce_final_avg100', 0):.3f} |
| routing weight max (avg100) | {t.get('wmax_final_avg100', 0):.4f} |
| active cells (weight > .01, avg100) | {t.get('n_active_gt01_final_avg100', 0):.1f} / {t.get('n_cells_final')} |
| Switch aux (avg100) | {t.get('aux_final_avg100', 0):.3f} |
| cells (initial → final) | 2 → {t.get('n_cells_final')} |
| splits | {t.get('splits')} |
| d_model / n_head / ffn | {result.get('config', {}).get('d_model')} / {result.get('config', {}).get('n_head')} / {result.get('config', {}).get('ffn_dim')} |
| steps | {len(result.get('history_sample', {}).get('loss', [])) and 'see config'} |
| wall | {t.get('wall_hours', 0):.2f} hr |
| cost | ${t.get('cost_usd_actual', 0):.2f} |

## Files

- `ckpt_v5mitosis_cotrain_v3_routing.pt` — `{{model_state_dict, router_state_dict, router_top_k, config, n_cells, ...}}`
- `cotrain_v3_routing_result.json` — full training history + falsifier results
- `train_v3_routing.log` — training stdout

## Load

```python
import torch
ckpt = torch.load("ckpt_v5mitosis_cotrain_v3_routing.pt", map_location="cpu")
# rebuild MitosisModelEngine from ckpt["config"], load ckpt["model_state_dict"];
# rebuild TopKMoERouter(d_model, max_cells), load ckpt["router_state_dict"];
# install via the forward monkey-patch from train_v5mitosis_cotrain_v3_routing.py.
```

Experimental research artifact — not a general-purpose chat model.
"""
README_PATH = HERE / "HF_README.md"
README_PATH.write_text(readme)

api = HfApi(token=TOKEN)
print(f"[INFO] creating repo {REPO_ID} (private)...")
create_repo(REPO_ID, token=TOKEN, private=True, exist_ok=True, repo_type="model")
for local, name in [(CKPT_PATH, "ckpt_v5mitosis_cotrain_v3_routing.pt"),
                    (RESULT_PATH, "cotrain_v3_routing_result.json"),
                    (LOG_PATH, "train_v3_routing.log"),
                    (README_PATH, "README.md")]:
    if not Path(local).exists():
        print(f"[WARN] skip missing {local}")
        continue
    print(f"[INFO] upload {name} ...")
    api.upload_file(path_or_fileobj=str(local), path_in_repo=name, repo_id=REPO_ID, repo_type="model")
print(f"[DONE] https://huggingface.co/{REPO_ID}")
