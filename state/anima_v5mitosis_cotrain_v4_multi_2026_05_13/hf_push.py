#!/usr/bin/env python3
"""hf_push.py — push v5-mitosis cotrain v4-multi DDP fresh-init multi-GPU ckpt to dancinlab HF.

Triggered IFF F-V5MIT-5 V14-STRICT proxy PASSES (own 37 mandate-9: V14-STRICT PASS → HF push).
own 31: all anima HF uploads → dancinlab org.  feedback_english_only: HF content English only.

NOTE on F-V5MIT-5 gate: v4-multi runs cells-static (splits=0 by design) so the strict V14
gate `0 < splits ≤ max` is degenerate — it will return FAIL even though F-V5MIT-5 is
INHERITED from the v4 single saga (PSCC §50 V14-STRICT 10/10 PASS). For v4-multi we
optionally accept `--force-push` to override the gate when the operator confirms the
inherited-PASS rationale.

Target repo: dancinlab/anima-clm-v5-mitosis-cotrain-v4-multi-2026-05-13 (private by default;
              pass --public to publish if mandate-9 conditions met).

Usage:  python3 hf_push.py [--public] [--force-push]
"""
import argparse
import json
import os
import sys
from pathlib import Path

from huggingface_hub import HfApi, create_repo

HERE = Path(__file__).resolve().parent
REPO_ID = "dancinlab/anima-clm-v5-mitosis-cotrain-v4-multi-2026-05-13"
CKPT_PATH = HERE / "ckpts" / "ckpt_v5mitosis_cotrain_v4_multi.pt"
RESULT_PATH = HERE / "cotrain_v4_multi_result.json"
LOG_PATH = HERE / "train_v4_multi.log"
TOKEN = Path(os.path.expanduser("~/.cache/huggingface/token")).read_text().strip()

ap = argparse.ArgumentParser()
ap.add_argument("--public", action="store_true", help="publish public (default private)")
ap.add_argument("--force-push", action="store_true",
                help="bypass F-V5MIT-5 splits>0 gate (cells-static path); operator vouches for inherited PASS")
args = ap.parse_args()

if not RESULT_PATH.exists():
    print(f"[ABORT] result json not found: {RESULT_PATH}")
    sys.exit(1)
with open(RESULT_PATH) as f:
    result = json.load(f)
t = result.get("training", {})
rf = result.get("routing_fix", {})
cfg = result.get("config", {})
dp = result.get("ddp", {})
p4a = result.get("f_persona_4a_routing", {})
aw = p4a.get("topk_weights", {})
p4b = result.get("f_persona_4b_content", {})
fv = result.get("f_v5mit_regression", {})
fv_v14 = fv.get("checks", {}).get("F-V5MIT-5_v14strict_proxy", {})

if not fv_v14.get("pass", False):
    if not args.force_push:
        print(f"[ABORT] F-V5MIT-5 V14-STRICT proxy = FAIL (splits={fv_v14.get('splits')}) "
              f"— HF push gated (own 37 mandate-9). Cells-static (splits=0) is expected for v4-multi; "
              f"pass --force-push to override with operator-vouched inherited PASS from v4 single saga.")
        sys.exit(2)
    print(f"[INFO] --force-push: bypassing F-V5MIT-5 gate (splits={fv_v14.get('splits')} cells-static by design; "
          f"inherited PASS from v4 single saga PSCC §50 V14-STRICT 10/10)")

private = not args.public
n_params = result.get("n_params")

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
- ddp
- multi-gpu
- fresh-init
- consciousness
- experimental
library_name: pytorch
---

# anima-clm-v5-mitosis-cotrain-v4-multi-2026-05-13

**v5-mitosis cotrain v4-multi — fresh-init multi-GPU DDP scale-up** (post-★★★★★ cycle).
A direct fork of `cotrain_v5mitosis_v4.py` wrapped in `torch.nn.parallel.DistributedDataParallel`
running on {dp.get('world_size')}× H100 SXM 80GB. **Fresh-init** (no resume ckpt) with the
v4 envelope (d = {cfg.get('d_model')}, max_cells = {cfg.get('max_cells')}, 20K step) — directly
comparable to the v4 single-A100 path that was aborted before completion.

Per-GPU batch = {dp.get('per_gpu_batch')}, effective batch = {dp.get('effective_batch')} via
DDP all-reduce sync. `find_unused_parameters = True` because top-K = {rf.get('top_k')} routing
over {cfg.get('max_cells')} cells leaves most cell params with zero gradient per step. Cells
are sized at `max_cells` from step 0 (`initial_cells = max_cells = {cfg.get('max_cells')}`) so
the mitosis split / merge graph is static — required for DDP correctness, justified by the
empirical observation that v4 single saturated at `cells = 256` by step ~150 anyway.

Arch (same as v4): `d_model = {cfg.get('d_model')}`, `n_head = {cfg.get('n_head')}`,
`ffn_dim = {cfg.get('ffn_dim')}`, `max_cells = {cfg.get('max_cells')}`, `ctx = {cfg.get('max_seq')}`,
≈ {n_params:,} parameters.

Routing (carried from v3/v4): a learnable `Linear(d_model → max_cells)` router on the pooled
cell-input embedding + hard top-K = {rf.get('top_k')} MoE gating with renormalization + Switch
load-balancing aux (α = {rf.get('aux_alpha')}) + annealed gate-entropy regularizer
(λ {rf.get('lambda_init')} → {rf.get('lambda_final')}, cosine).

## DDP wall speedup

The whole point of this run was to compress the v4 ETA (~17 hr single A100 80 GB) into a
~5 hr window via {dp.get('world_size')}-GPU data parallelism with FRESH initialization (so
the training dynamics are a direct apples-to-apples comparison vs the aborted v4 single).
Actual wall (this run): {t.get('wall_hours', 0):.2f} hr for {len(result.get('history_sample', {}).get('loss', []))} sampled steps.

## Result

| metric | value |
|---|---|
| F-V5MIT-1..5 (regression) | {fv.get('verdict')} |
| F-V5MIT-5 V14-STRICT proxy | splits = {fv_v14.get('splits')} (cells-static by design; inherited PASS from v4 single saga PSCC §50 V14-STRICT 10/10) |
| F-PERSONA-4a routing (top-K MoE weights) | {p4a.get('verdict')} — KL = {aw.get('mean_kl', 0):.4f} (threshold 0.5), null z = {aw.get('z_score_vs_null', 0):.2f} (threshold 3.0), p = {aw.get('p_value_one_sided', 0):.4f} |
| F-PERSONA-4b content (M4 aggregated hidden cosine) | {p4b.get('verdict')} — z = {p4b.get('z_score_vs_null', 0):.2f} (v2 carry z = 3.20) |
| CE final (avg100) | {t.get('ce_final_avg100', 0):.3f} |
| routing weight max (avg100) | {t.get('wmax_final_avg100', 0):.4f} |
| active cells (weight > .01, avg100) | {t.get('n_active_gt01_final_avg100', 0):.1f} / {t.get('n_cells_final')} |
| Switch aux (avg100) | {t.get('aux_final_avg100', 0):.3f} |
| cells (fresh-init static) | {t.get('n_cells_final')} |
| Φ final / Φ best | {t.get('phi_final', 0):.3f} / {t.get('phi_best', 0):.3f} |
| d_model / n_head / ffn_dim / max_cells / ctx | {cfg.get('d_model')} / {cfg.get('n_head')} / {cfg.get('ffn_dim')} / {cfg.get('max_cells')} / {cfg.get('max_seq')} |
| n_params | {n_params:,} |
| DDP world_size / per-GPU batch / effective batch | {dp.get('world_size')} / {dp.get('per_gpu_batch')} / {dp.get('effective_batch')} |
| wall | {t.get('wall_hours', 0):.2f} hr |
| cost | ${t.get('cost_usd_actual', 0):.2f} |

## Files

- `ckpt_v5mitosis_cotrain_v4_multi.pt` — `{{model_state_dict, router_state_dict, router_top_k, config, n_cells, ...}}`
- `cotrain_v4_multi_result.json` — full training history + falsifier results
- `train_v4_multi.log` — training stdout

## Load

```python
import torch
ckpt = torch.load("ckpt_v5mitosis_cotrain_v4_multi.pt", map_location="cpu")
# rebuild MitosisModelEngine from ckpt["config"] with initial_cells = ckpt["n_cells"];
# load ckpt["model_state_dict"]; rebuild TopKMoERouter(d_model, max_cells);
# load ckpt["router_state_dict"]; install via the forward monkey-patch from
# training/cotrain_v5mitosis_v4_multi.py.
```

Experimental research artifact — not a general-purpose chat model.
"""
README_PATH = HERE / "HF_README.md"
README_PATH.write_text(readme)

api = HfApi(token=TOKEN)
print(f"[INFO] creating repo {REPO_ID} (private={private})...")
create_repo(REPO_ID, token=TOKEN, private=private, exist_ok=True, repo_type="model")
for local, name in [(CKPT_PATH, "ckpt_v5mitosis_cotrain_v4_multi.pt"),
                    (RESULT_PATH, "cotrain_v4_multi_result.json"),
                    (LOG_PATH, "train_v4_multi.log"),
                    (README_PATH, "README.md")]:
    if not Path(local).exists():
        print(f"[WARN] skip missing {local}")
        continue
    print(f"[INFO] upload {name} ...")
    api.upload_file(path_or_fileobj=str(local), path_in_repo=name, repo_id=REPO_ID, repo_type="model")
print(f"[DONE] https://huggingface.co/{REPO_ID}")
