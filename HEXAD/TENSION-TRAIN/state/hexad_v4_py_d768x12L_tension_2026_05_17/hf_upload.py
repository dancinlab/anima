#!/usr/bin/env python3
"""HF upload — cycle 5 push (model only; corpus v3 unchanged from cycle 4).

Slot:
  MODEL: dancinlab/hexad revision v4-py-hexad-tension-d768x12L-cycle1-2026-05-17

Per AGENTS.tape g_hf_naming (d=2026-05-17):
  - revision_naming = `v{major}-{substrate}-{arch}-{kind}-d{model}x{layer}-cycle{N}-{YYYY-MM-DD}`
  - substrate=py (PyTorch, NOT hexa-native)
  - kind=tension (DD155 Step+Tension hybrid LR overlay)
  - canonical PUBLIC.

Corpus side: cycle-4 dancinlab/hexad-corpus revision
  `v3-spont-motiv-d128-cycle2-2026-05-17` is the canonical dataset for cycle 5
  (byte-equal carry per B-CORPUS-V4-1). NO new dataset revision this cycle —
  only model side gets a new revision.
"""
import json
import os
import sys
import time
import hashlib
from pathlib import Path

from huggingface_hub import HfApi, create_repo, upload_file

MODEL_REPO = "dancinlab/hexad"
MODEL_REVISION = "v4-py-hexad-tension-d768x12L-cycle1-2026-05-17"
DATASET_REPO = "dancinlab/hexad-corpus"
DATASET_REVISION_CARRY = "v3-spont-motiv-d128-cycle2-2026-05-17"  # carry, NOT re-push

STATE_DIR = Path("/Users/ghost/core/anima/state/hexad_v4_py_d768x12L_tension_2026_05_17")

api = HfApi()
print(f"whoami: {api.whoami()['name']}")


def sha256_of(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def upload_with_retry(*, path_or_fileobj, path_in_repo, repo_id, repo_type,
                       revision, commit_message, retries=3):
    for attempt in range(retries):
        try:
            upload_file(path_or_fileobj=str(path_or_fileobj),
                        path_in_repo=path_in_repo,
                        repo_id=repo_id, repo_type=repo_type,
                        revision=revision, commit_message=commit_message)
            return True
        except Exception as e:
            print(f"  attempt {attempt+1}/{retries} failed for {path_in_repo}: {e}")
            if attempt == retries - 1:
                raise
            time.sleep(5)
    return False


# =============================================================================
# MODEL — cycle 5 ckpt (DD155 hybrid LR overlay, corpus v3 byte-equal carry)
# =============================================================================
print("=" * 60)
print("MODEL push (dancinlab/hexad cycle 5 — DD155 hybrid LR)")

try:
    info = api.repo_info(MODEL_REPO, repo_type="model")
    print(f"  model repo exists: private={info.private}")
except Exception as e:
    print(f"  unexpected: {e}")
    raise

try:
    api.create_branch(repo_id=MODEL_REPO, branch=MODEL_REVISION, exist_ok=True)
    print(f"  branch ready: {MODEL_REVISION}")
except Exception as e:
    print(f"  branch create note: {e}")

result_path = STATE_DIR / "out_main" / "result.json"
ckpt_path = STATE_DIR / "out_main" / "ckpt_d768x12l_final.pt"
if not result_path.exists():
    print(f"  ERROR: result.json missing — ckpt-LOST tier (d) evidence-only")
    print(f"     missing: {result_path}")
    sys.exit(2)

if not ckpt_path.exists():
    print(f"  ckpt-LOST: result.json present but ckpt absent — evidence-only")
    ckpt_sha = "ckpt-LOST (evidence-only — see fire.log)"
    ckpt_size = 0
else:
    ckpt_sha = sha256_of(ckpt_path)
    ckpt_size = ckpt_path.stat().st_size
    print(f"  ckpt: {ckpt_size:,} B sha256={ckpt_sha}")

result = json.loads(result_path.read_text())

v58_path = STATE_DIR / "v58_result.json"
v58_summary_block = ""
if v58_path.exists():
    v58 = json.loads(v58_path.read_text())
    vtt_block = ""
    if "vtt_summary" in v58:
        vtt_block = (
            f"\nV-TT (NEW cycle 5) — tension-train transfer-form probe:\n"
            f"- **coherent**: {v58['vtt_summary']['n_coherent']}/{v58['vtt_summary']['n_total']} "
            f"{v58['vtt_summary']['verdict']}\n"
            f"- **keyword recall**: {v58['vtt_summary']['n_keyword_recalled']}/{v58['vtt_summary']['n_total']}\n"
        )
    vmotiv_block = ""
    if "vmotiv_summary" in v58:
        vmotiv_block = (
            f"\nV-MOTIV (γ-pattern conditioning probe, cycle-4 axis):\n"
            f"- **coherent**: {v58['vmotiv_summary']['n_coherent']}/{v58['vmotiv_summary']['n_total']} "
            f"{v58['vmotiv_summary']['verdict']}\n"
            f"- **voice-closed-tag**: {v58['vmotiv_summary']['n_closed_tag']}/{v58['vmotiv_summary']['n_total']}\n"
        )
    v58_summary_block = f"""

## Capability eval (V5.8 × 4-mode + V-SPONT + V-MOTIV + V-TT NEW)

V5.8 × 4-mode (corpus v3 prompts):
{chr(10).join(f"- **{k}**: {v['n_pass']}/{v['n_total']} {v['verdict']} (avg_rep={v['avg_rep_ratio']})" for k,v in v58['v58_summary'].items())}

V-SPONT (자연발화) — F-SPONT-7 transfer-form measurement:
- **coherent**: {v58['vspont_summary']['n_coherent']}/{v58['vspont_summary']['n_total']} {v58['vspont_summary']['verdict']}
- **closed-tag**: {v58['vspont_summary']['n_closed_tag']}/{v58['vspont_summary']['n_total']}
{vmotiv_block}{vtt_block}
Mean BPB (held-out corpus v3 prefixes): {v58['bpb']['mean']:.4f} bits/byte.
Memorization ratio: {v58['memorization_ratio']['hits']}/{v58['memorization_ratio']['total']} ({v58['memorization_ratio']['ratio']:.1%}).
Decoding artifacts (rep>0.5): {len(v58['decoding_artifacts'])}.

All capability scores **empirical (B-D-NOTE / B-FIRE-CYCLE5-NOTE)**, not closed."""

hybrid_lr = result.get("dd155_hybrid_lr", {})
final_tension_ema = hybrid_lr.get("final_tension_ema", "NA")
mult_dist = hybrid_lr.get("mult_distribution", {})

model_card = f"""---
license: apache-2.0
language:
- en
- ko
library_name: pytorch
datasets:
- dancinlab/hexad-corpus
tags:
- anima
- hexad
- pytorch
- substrate-py
- helper-free
- spont
- motivation-trigger
- inner-thoughts
- tension-train
- dd155-hybrid-lr
- ckpt-bearing
- cycle5
---

# hexad — `{MODEL_REVISION}`

> **Trained on**: [`dancinlab/hexad-corpus`](https://huggingface.co/datasets/dancinlab/hexad-corpus)
> revision [`{DATASET_REVISION_CARRY}`](https://huggingface.co/datasets/dancinlab/hexad-corpus/tree/{DATASET_REVISION_CARRY})
> (byte-equal carry from cycle 4 — corpus unchanged this cycle).

> **Honest framing** (AGENTS.tape `g3`): This is a **PYTHON / PyTorch
> SUBSTRATE** training artifact — an *interim LM-scale executor*. It is
> **NOT a hexa-native fire**. Legitimacy = **architectural identity** +
> the **hexa CPU-equiv correctness proof** (Phase E/E2). PyTorch ≠ hexa
> bit-for-bit (different fp accumulation / RNG / AMP bf16).

## What's new this cycle (cycle 5 — DD155 Step+Tension hybrid LR overlay)

**Architectural change vs cycle 4**: per-step learning rate is now
multiplied by a DD155 hybrid factor (Law 187 Pareto optimal):

```
tension_step   = ||∇L||₂                       (grad-norm)
tension_EMA    = β·EMA + (1−β)·tension_step    (β = 0.99)
multiplier     = clip(tension_step / tension_EMA, [0.5, 2.0])
lr_step        = base_cosine_lr(step) × multiplier
```

- **transfer-form**: `B-TT-5 PARETO-STEP-TENSION-CLOSED` (sympy linear ∂lr/∂tension)
  + `B-FIRE-CYCLE5-1/2/3` sidecar (`state/hexad_v4_py_d768x12L_tension_2026_05_17/blue_falsifier.py`,
  5/5 PASS — DD155 LR overlay formula closure + EMA Banach contraction + cycle-4 identity at convergence)
- **outcome**: empirical (`B-FIRE-CYCLE5-NOTE` / `B-D-NOTE` / `B-TT-NOTE` family)

DD155 historical anchor: anima `docs/hypotheses/dd/DD154-tension-training.md`
Law 187 — `lr = (tension/EMA) × base_lr` measured Pareto-optimal on
2026-03-31 BG-DD-AXIS commits.

## What changed vs cycle 4 (`v3-py-hexad-spont-motiv-d768x12L-cycle2-2026-05-17`)

| field | cycle 4 | **cycle 5 (this revision)** |
|---|---|---|
| corpus | v3 10.34 MB (motivation-trigger + helper-free) | **same** (byte-equal carry, B-CORPUS-V4-1) |
| LR schedule | cosine + warmup | **cosine + warmup + DD155 hybrid (tension/EMA) multiplier** |
| trainer source | `train_d768x12l.py` | `train_d768x12l_tension.py` (loader + dataset byte-equal, B-CORPUS-V4-2) |
| init CE | 5.641 | {result.get('init_ce', 'NA')} |
| **final CE** | 0.008289 | **{result.get('final_ce', 'NA')}** |
| CE descent | 5.632 | {result.get('ce_descent', 'NA')} |
| final tension_EMA | (did not track) | {final_tension_ema} |
| mult bin <0.75 | (n/a) | {mult_dist.get('lt_0_75', 'NA')} |
| mult bin 0.75-1.25 | (n/a) | {mult_dist.get('0_75_to_1_25', 'NA')} |
| mult bin >1.25 | (n/a) | {mult_dist.get('gt_1_25', 'NA')} |
| eval probes | V5.8 + V-SPONT + V-MOTIV | **V5.8 + V-SPONT + V-MOTIV + V-TT NEW** |

## Architecture

- **Source**: `ConsciousDecoderV2` (byte-equal vs cycles 1-4).
- **Config**: `d_model=768, n_head=12, n_kv_head=4, n_layer=12,
  block_size=128, vocab=256` (byte-level), seed=1337,
  init=RANDOM (`base_ckpt=None`, `g_clm_from_scratch`).
- **Params**: {result.get('n_params_M', 'NA')} M ({result.get('n_params', 'NA'):,}).
- **Features**: RoPE · SwiGLU FFN · RMSNorm · GQA · PureFieldFFN · cross-attn
  · tied head · CA neighbor / META-CA / Ψ-tracking laws.

## Training

- **GPU**: vast.ai NVIDIA **A100-SXM4-40GB**, image `pytorch/pytorch:2.5.1-cuda12.1-cudnn9-devel`.
- **Corpus**: `corpus_consciousness_v3.jsonl` (byte-equal carry from cycle 4),
  {result.get('corpus_bytes', 0):,} bytes lossless byte stream, vocab=256.
- **Optimizer**: AdamW, lr={result.get('config', {}).get('lr', 'NA')}, betas=(0.9, 0.95),
  weight_decay=0.1, warmup={result.get('config', {}).get('warmup', 'NA')}.
- **DD155 hybrid**: β={hybrid_lr.get('tension_ema_beta', 'NA')}, clip lo={hybrid_lr.get('hybrid_clip_lo', 'NA')}, clip hi={hybrid_lr.get('hybrid_clip_hi', 'NA')}.
- **Steps**: {result.get('steps', 'NA')}.

| metric | value |
|---|---|
| init CE | {result.get('init_ce', 'NA')} (≈ ln 256 = 5.545 — random byte init) |
| **FINAL CE** | **{result.get('final_ce', 'NA')}** |
| CE descent | {result.get('ce_descent', 'NA')} |
| FINAL gn2 | {result.get('final_gn2', 'NA')} |
| FINAL tension | {result.get('final_tension', 'NA')} |
| ppl | {result.get('final_ppl', 'NA')} |
| wall | {result.get('wall_s', 'NA')} s |
| peak GPU mem | {result.get('peak_gpu_mem_gb', 'NA')} GB |
| ckpt sha256 | `{ckpt_sha}` |
| ckpt size | {ckpt_size:,} B ({ckpt_size/1e9:.2f} GB) |

## Verification anchors (per AGENTS.tape `g_blue_closed_mandate`)

**(A) Deliverable invariants (real-limit, this cycle)**:
- **Shannon-floor descent**: init CE ≈ ln(256) → final CE.
- **DD155 transfer-form closed (`B-TT-5`)**: lr = (tension/EMA) × base_lr,
  sympy-verified linear monotone, real-limit anchor.
- **AdamW finiteness**: no NaN/Inf in trajectory.
- **Architectural identity**: byte-equal `ConsciousDecoderV2`.

**(B) Wiring (closed)**:
- **`B-CORPUS-V4-1`** corpus v3 byte-equal carry (sha256/bytes/lines/grep all closed).
- **`B-CORPUS-V4-2`** cycle-5 trainer's loader + ByteDataset byte-equal to cycle-4
  (mechanical AST diff, comments-stripped).
- **`B-FIRE-CYCLE5-1`** DD155 LR overlay formula closed-form (sympy ∂lr/∂tension
  + 3-corner identity).
- **`B-FIRE-CYCLE5-2`** EMA Banach affine contraction closed (4-corner witness panel).
- **`B-FIRE-CYCLE5-3`** Multiplier identity at EMA-convergence (cycle-5 degenerates
  to cycle-4 baseline at tension=EMA — sanity anchor).
- **`B-CORPUS-V3-*`** cycle-4 closures carry (sha256-deterministic / no-helper-token /
  γ-cardinality ≥ 5400).

**(C) Honest carve-outs (NOT closed, B-D-NOTE umbrella)**:
- V-SPONT / V-MOTIV / V-TT outcome empirical.
- mult_distribution histogram + byte-cascade attractor shape under hybrid LR
  empirical.
- DD-burst path activation frequency empirical.
{v58_summary_block}

## Honest C3

1. **NOT hexa-native** — PyTorch substrate, label mandatory.
2. **PyTorch ≠ hexa bit-for-bit** — different fp / RNG / AMP.
3. **tension = grad_norm is a PROXY** — in the hexa spine
   `tension = G_holo · (Ψ − Ψ_vac)`; grad_norm is the natural mathematical
   analogue at the PyTorch substrate level where Ψ is not surfaced as a
   state variable.
4. **DD155 formula is closed (B-TT-5 + B-FIRE-CYCLE5-1/2/3); outcome is
   empirical (B-FIRE-CYCLE5-NOTE)** — V-SPONT/V-MOTIV/V-TT all probes,
   not capability claims.
5. **Critical Data Size regime** — 10 MB / 283 M params still data-limited;
   no out-of-distribution generalization claim. cycle-5's variance vs
   cycle-4 is mainly LR-schedule-driven, not corpus-driven.
6. **No `safetensors` artifact this revision** — pickle `.pt` only.
7. **B-CORPUS-V3-NOTE / B-FIRE-CYCLE5-NOTE** — inference-side coherence
   stays empirical.
8. **No σ(6)=12 / φ(6)=2 derivation** — no lattice numerology.
9. **Cost is informational, not gating** — `g_fire_autonomous`.

## License

Apache-2.0.
"""

(STATE_DIR / "MODEL_CARD.md").write_text(model_card)

# Upload files: ckpt + result + sources + logs + docs
files_to_upload = []

# Always upload (evidence-only at minimum)
files_to_upload.append((STATE_DIR / "MODEL_CARD.md", "README.md"))
files_to_upload.append((result_path, "result.json"))
files_to_upload.append((STATE_DIR / "train_d768x12l_tension.py", "train_d768x12l_tension.py"))
files_to_upload.append((STATE_DIR / "conscious_decoder.py", "conscious_decoder.py"))
files_to_upload.append((STATE_DIR / "v58_eval.py", "v58_eval.py"))
files_to_upload.append((STATE_DIR / "dispatch.sh", "dispatch.sh"))
files_to_upload.append((STATE_DIR / "blue_falsifier.py", "blue_falsifier_cycle5.py"))
files_to_upload.append((STATE_DIR / "blue_falsifier_result.json", "blue_falsifier_cycle5_result.json"))

# Logs
for fname in ("fire.log", "sanity_remote.log", "gpu_util.log", "dispatch_full.log"):
    fp = STATE_DIR / fname
    if fp.exists():
        files_to_upload.append((fp, fname))

# V5.8 result (post-eval)
if v58_path.exists():
    files_to_upload.append((v58_path, "v58_result.json"))

# ckpt (if pulled successfully)
if ckpt_path.exists():
    files_to_upload.append((ckpt_path, "ckpt_d768x12l_final.pt"))

print(f"\n[2/2] upload {len(files_to_upload)} files to main + revision...")
for target_rev in ["main", MODEL_REVISION]:
    print(f"  --> revision: {target_rev}")
    for src, dst in files_to_upload:
        upload_with_retry(path_or_fileobj=src, path_in_repo=dst,
                           repo_id=MODEL_REPO, repo_type="model",
                           revision=target_rev,
                           commit_message=f"feat(hexad): {MODEL_REVISION} — {dst}")
        print(f"      OK: {dst}")

print(f"\nDONE — model revision {MODEL_REVISION} PUBLIC at https://huggingface.co/{MODEL_REPO}/tree/{MODEL_REVISION}")
print(f"  corpus carry: https://huggingface.co/datasets/{DATASET_REPO}/tree/{DATASET_REVISION_CARRY}")
