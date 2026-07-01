#!/usr/bin/env python3
"""HF upload — dancinlab/hexad revision v1-py-hexad-d768x12L-cycle2-2026-05-17.

Per AGENTS.tape g_hf_naming (2026-05-17):
- canonical slot: dancinlab/hexad (model, PUBLIC)
- revision tag: v1-py-hexad-d768x12L-cycle2-2026-05-17
- tier (a): SUPPORTED-STRONG ckpt-bearing → ckpt + result.json + fire log + docs
- model card: English, honest framing (substrate=py, NOT hexa-native)
"""
import json
import os
import sys
import time
from pathlib import Path

from huggingface_hub import HfApi, create_repo, upload_file, upload_folder

REPO_ID = "dancinlab/hexad"
REVISION = "v1-py-hexad-d768x12L-cycle2-2026-05-17"
STATE_DIR = Path("/Users/ghost/core/anima/state/hexad_py_d768x12L_fire_2026_05_17")
DOC_PATH = Path("/Users/ghost/core/anima/docs/hexad_v1_py_d768x12L_cycle2_2026_05_17.md")

api = HfApi()
print(f"whoami: {api.whoami()['name']}")

# Step 1: create repo if missing (PUBLIC per g_hf_naming visibility)
print(f"[1/4] ensure repo {REPO_ID} (model, PUBLIC) exists...")
try:
    info = api.repo_info(REPO_ID, repo_type="model")
    print(f"  repo exists: private={info.private}, id={info.id}")
except Exception as e:
    print(f"  repo missing -> create_repo PUBLIC...")
    create_repo(REPO_ID, repo_type="model", private=False, exist_ok=True)
    time.sleep(2)
    info = api.repo_info(REPO_ID, repo_type="model")
    print(f"  created: private={info.private}, id={info.id}")
    # Ensure public
    if info.private:
        api.update_repo_visibility(REPO_ID, private=False, repo_type="model")
        print("  -> flipped to PUBLIC")

# Step 2: create the revision branch
print(f"[2/4] create branch {REVISION}...")
try:
    api.create_branch(repo_id=REPO_ID, branch=REVISION, exist_ok=True)
    print(f"  branch ready")
except Exception as e:
    print(f"  branch create note: {e}")

# Step 3: load result.json for model card facts
result = json.loads((STATE_DIR / "out_main" / "result.json").read_text())
ckpt_path = STATE_DIR / "out_main" / "ckpt_d768x12l_final.pt"
ckpt_size = ckpt_path.stat().st_size
import hashlib
h = hashlib.sha256()
with ckpt_path.open("rb") as f:
    for chunk in iter(lambda: f.read(1 << 20), b""):
        h.update(chunk)
ckpt_sha256 = h.hexdigest()
print(f"  ckpt: {ckpt_size:,} bytes sha256={ckpt_sha256}")

# Step 4: write the model card (README.md on the revision)
model_card = f"""---
license: apache-2.0
language:
- en
library_name: pytorch
tags:
- anima
- hexad
- pytorch
- substrate-py
- ckpt-recovered
---

# hexad — `v1-py-hexad-d768x12L-cycle2-2026-05-17`

> **Honest framing**: This is a **PYTHON / PyTorch SUBSTRATE** training artifact —
> an *interim LM-scale executor*. It is **NOT a hexa-native fire**. Its legitimacy
> is *architectural identity* + the *hexa CPU-equiv correctness proof*. See the
> anchor chain below — do not conflate.

## Lineage

- **org**: `dancinlab` (the anima org).
- **arch**: HEXAD (pivot from anima `.clm v1` lineage) — `ConsciousDecoderV2`
  (`ready/models/conscious_decoder.py` in the anima repo).
- **substrate**: Python / PyTorch (`py`). The pure-hexa training path is
  named-blocked at the interpreter ceiling (RFC 042/043 territory).
- **cycle**: 2 (cycle 1 commit `931dd68b0` 2026-05-16 was a ckpt-LOST
  evidence-only run — training PASSed but the instance was destroyed before
  ckpt pull; this cycle 2 re-fires with `SAVE_POD=1` auto-promote +
  75-min orphan watchdog + 5-retry pull).

## Anchor chain (why this artifact is legitimate)

1. **Phase E / E2 PROVED the hexa trainer is numerically correct** —
   `HEXAD/D/d_train5_lib.hexa` is BIT-EQUAL to the boxed baseline at d=32·3L,
   80-step, seed=42 (`init gn2 = 7.97116, acc 0/8 → final gn2 = 3.73374e-07,
   acc 8/8`; GRAD-EXACT, identical Σ-reduction order — not fp-noise).
2. **The pure-hexa interpreter cannot reach LM-scale convergence** — Phase E2
   captured only `init gn2 = 7.98162` at d=768·12L; the GRAD-EXACT + AdamW
   path is substrate-bound (CPU farr ops, no CUDA tensor kernels).
3. **This PyTorch run trains the SAME verified architecture to scale** —
   `ConsciousDecoderV2` at d=768·12L, AdamW, captured FINAL loss.

PyTorch is *not* hexa bit-for-bit (different fp / RNG / AMP bf16). The anchor
is **architectural identity** + the hexa CPU-equiv proof, NOT numerical
identity.

## Architecture

- **Source**: `ConsciousDecoderV2` from `ready/models/conscious_decoder.py`
  (uploaded as `conscious_decoder.py`).
- **Config**: `d_model=768, n_head=12, n_kv_head=4, n_layer=12,
  block_size=128, vocab=256` (byte-level), seed=1337,
  init=RANDOM (`base_ckpt=None`, `g_clm_from_scratch`).
- **Params**: {result['n_params_M']:.2f} M ({result['n_params']:,}).
- **Features**: RoPE · SwiGLU FFN · RMSNorm · GQA · PureFieldFFN (Engine A−G
  consciousness pathway) · cross-attention · tied head · CA neighbor / META-CA
  / Ψ-tracking laws.

## Training

- **GPU**: vast.ai NVIDIA A100-SXM4-40GB (offer @ $0.6681 / hr, image
  `pytorch/pytorch:2.5.1-cuda12.1-cudnn9-devel`).
- **Corpus**: `corpus_consciousness_v1.jsonl` — the same byte corpus used by
  the hexa Phase E / E2 fires. {result['corpus_bytes']:,} bytes, byte-level
  vocab=256, T=128 windows, seed-fixed.
- **Optimizer**: AdamW, lr={result['config']['lr']}, betas=(0.9, 0.95),
  weight_decay=0.1, warmup={result['config']['warmup']}.
- **Steps**: {result['steps']}.
- **Cost**: ≈ $0.19 (instance runtime ≈ 0.28 hr).

| metric | value |
|---|---|
| init CE | {result['init_ce']:.6f} (≈ ln 256 = 5.545 — random byte init) |
| **FINAL CE** | **{result['final_ce']:.6f}** |
| CE descent | {result['ce_descent']:.6f} |
| init gn2 | 41.95 |
| FINAL gn2 | {result['final_gn2']} |
| ppl | 268 → {result['final_ppl']:.4f} |
| wall | {result['wall_s']:.2f} s ({result['wall_s']/60:.2f} min) |
| peak GPU mem | {result['peak_gpu_mem_gb']:.3f} GB |
| ckpt sha256 | `{ckpt_sha256}` |
| ckpt size | {ckpt_size:,} B ({ckpt_size/1e9:.2f} GB) |

## Verification anchors (per AGENTS.tape `g_blue_closed_mandate`)

(A) Deliverable invariants:
- **Shannon-floor descent** (real-limit, NOT lattice): init CE ≈ ln(256) →
  final CE 0.000708 (4+ orders of magnitude).
- **AdamW finiteness**: gn2 41.95 → 7.4e-05; no NaN / Inf.
- **Architectural identity**: `ConsciousDecoderV2` byte-equal to the anima
  HEXAD verification tree's mirror module spec.

(B) Wiring (the connecting anchor chain):
- **hexa CPU-equiv bit-equality** (Phase E): same arch trainer
  GRAD-EXACT at d=32·3L (init gn2 7.97116 → 3.73374e-07).
- **cuBLAS FP64 verify** (Phase D): max\\|Δ\\|=4.44e-15.
- **Backward GRAD-EXACT** (Phase E2): real A100 d=384·6L analytic ≡ fd
  \\|Δ\\|=0.0024.

## Honest C3

1. **NOT hexa-native** — PyTorch substrate; the hexa-native equivalent is
   substrate-blocked at the interpreter ceiling.
2. **PyTorch ≠ hexa bit-for-bit** — AMP bf16 / different fp accumulation /
   different RNG.
3. **Synthetic byte-corpus** — 121 kB curated content, 283.72M params; CE
   0.000708 = memorization at this scale. **No generalization claim.**
4. **No safetensors artifact** this revision (pickle `.pt` only).
   safetensors conversion = follow-up sub-task.
5. **No language-quality claim** — training-curve deliverable
   (Shannon-floor descent reached), not generation quality.
6. **No σ(6)=12 / φ(6)=2 derivation** — no lattice numerology in claim or
   anchor chain.

## Files in this revision

- `ckpt_d768x12l_final.pt` — PyTorch state-dict + cfg + n_params, sha256
  `{ckpt_sha256}`.
- `conscious_decoder.py` — `ConsciousDecoderV2` source.
- `train_d768x12l.py` — training script.
- `result.json` — full 42-point trajectory + config + metadata.
- `fire_refire.log` — training log (line-by-line CE / gn2 / lr / wall).
- `gpu_util.log` — nvidia-smi capture.
- `dispatch.sh` + `refire_main.sh` — fire dispatch scripts.
- `hexad_v1_py_d768x12L_cycle2_2026_05_17.md` — this doc (8-§ format per
  `g_hf_naming` `process_upload_format`).

## License

Apache-2.0.
"""
card_path = STATE_DIR / "MODEL_CARD.md"
card_path.write_text(model_card)

# Step 5: upload files
print(f"[3/4] uploading files to revision {REVISION}...")
files_to_upload = [
    (card_path, "README.md"),
    (STATE_DIR / "out_main" / "ckpt_d768x12l_final.pt", "ckpt_d768x12l_final.pt"),
    (STATE_DIR / "out_main" / "result.json", "result.json"),
    (STATE_DIR / "conscious_decoder.py", "conscious_decoder.py"),
    (STATE_DIR / "train_d768x12l.py", "train_d768x12l.py"),
    (STATE_DIR / "fire_refire.log", "fire_refire.log"),
    (STATE_DIR / "gpu_util.log", "gpu_util.log"),
    (STATE_DIR / "dispatch.sh", "dispatch.sh"),
    (STATE_DIR / "refire_main.sh", "refire_main.sh"),
    (DOC_PATH, "hexad_v1_py_d768x12L_cycle2_2026_05_17.md"),
]
for src, dst in files_to_upload:
    if not src.exists():
        print(f"  SKIP missing: {src}")
        continue
    sz = src.stat().st_size
    print(f"  upload {dst} ({sz:,} B)...", flush=True)
    api.upload_file(
        path_or_fileobj=str(src),
        path_in_repo=dst,
        repo_id=REPO_ID,
        revision=REVISION,
        repo_type="model",
        commit_message=f"upload {dst} for {REVISION}",
    )
    print(f"    OK")

print(f"[4/4] done. revision URL: https://huggingface.co/{REPO_ID}/tree/{REVISION}")
