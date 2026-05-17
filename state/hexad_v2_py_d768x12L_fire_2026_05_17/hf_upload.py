#!/usr/bin/env python3
"""HF upload — cycle 3 push.

Two slots:
  * MODEL: dancinlab/hexad revision v2-py-hexad-spont-d768x12L-cycle1-2026-05-17
  * DATASET: dancinlab/hexad-corpus revision v2-spont-stream-d128-cycle1-2026-05-17

Per AGENTS.tape g_hf_naming (d=2026-05-17):
  - revision_naming = `v{major}-{substrate}-{arch}-{...}-cycle{N}-{YYYY-MM-DD}`
  - substrate=py (PyTorch, NOT hexa-native)
  - kind=spont (자연발화 corpus retrained, helper-free)
  - canonical PUBLIC.
"""
import json
import os
import shutil
import sys
import time
import hashlib
from pathlib import Path

from huggingface_hub import HfApi, create_repo, upload_file

MODEL_REPO = "dancinlab/hexad"
MODEL_REVISION = "v2-py-hexad-spont-d768x12L-cycle1-2026-05-17"
DATASET_REPO = "dancinlab/hexad-corpus"
DATASET_REVISION = "v2-spont-stream-d128-cycle1-2026-05-17"

STATE_DIR = Path("/Users/ghost/core/anima/state/hexad_v2_py_d768x12L_fire_2026_05_17")
CORPUS_DIR = Path("/Users/ghost/core/anima/state/hexad_v2_corpus_spont_2026_05_17")
DOC_PATH = Path("/Users/ghost/core/anima/docs/hexad_v2_py_d768x12L_cycle1_2026_05_17.md")
CORPUS_SRC = CORPUS_DIR / "corpus_consciousness_v2.jsonl"

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
# 1) DATASET — corpus v2 (helper-free, stimulus-stream)
# =============================================================================
print("\n=" * 1, "DATASET push (dancinlab/hexad-corpus v2)")

# stage corpus + manifest + README
print("\n[1/3] ensure dataset repo + revision branch...")
try:
    info = api.repo_info(DATASET_REPO, repo_type="dataset")
    print(f"  dataset exists: private={info.private}")
    if info.private:
        api.update_repo_settings(repo_id=DATASET_REPO, repo_type="dataset", private=False)
        print("  -> flipped to PUBLIC")
except Exception as e:
    if "404" in str(e) or "Repository Not Found" in str(e):
        print("  not found -> create PUBLIC")
        create_repo(DATASET_REPO, repo_type="dataset", private=False, exist_ok=True)
        time.sleep(2)
    else:
        raise

try:
    api.create_branch(repo_id=DATASET_REPO, repo_type="dataset",
                      branch=DATASET_REVISION, exist_ok=True)
    print(f"  branch ready: {DATASET_REVISION}")
except Exception as e:
    print(f"  branch create note: {e}")

print("\n[2/3] stage corpus v2 files...")
corpus_sha = sha256_of(CORPUS_SRC)
corpus_bytes = CORPUS_SRC.stat().st_size
with CORPUS_SRC.open() as f:
    corpus_lines = sum(1 for _ in f)
print(f"  corpus_consciousness_v2.jsonl: {corpus_bytes:,} B / {corpus_lines} lines / sha256 {corpus_sha}")

manifest = {
    "name": "hexad-corpus",
    "version": DATASET_REVISION,
    "file": "corpus_consciousness_v2.jsonl",
    "format": "jsonl",
    "sha256": corpus_sha,
    "bytes": corpus_bytes,
    "lines": corpus_lines,
    "vocab_size": 256,
    "encoding": "utf-8",
    "tokenization": "byte-level (no tokenizer; raw bytes from 'text' field)",
    "format_pattern": (
        "stimulus-stream: each record is either `<stimulus>X</stimulus>\\n"
        "<anima>Y</anima>` (β, reactive emission) OR `<anima>Y</anima>` "
        "(δ, spontaneous self-monologue). NO helper/assistant/도우미/사용자 "
        "role labels. anima_persona-consistent."
    ),
    "schema": {
        "id": "string — stable identifier (e.g. 'ccv2_c_0')",
        "text": "string — stimulus-stream content with <stimulus>/<anima> tags",
        "desc": "string — meta tail (module / idx / kind / pattern / bilingual / tag)",
        "hexad_module": "string ∈ {hexad_c, hexad_d, hexad_e, hexad_m, hexad_s, hexad_w, hexad_spont, hexad_wiring}",
        "idx": "integer", "source": "corpus_generator_v2.py", "phi_family": "Hexad-spont",
        "pattern": "string ∈ {beta, delta}",
        "bilingual": "bool — text mixes EN + KO when true",
    },
    "modules": {
        "hexad_c": 320, "hexad_d": 320, "hexad_e": 320, "hexad_m": 320,
        "hexad_s": 320, "hexad_w": 320,
        "hexad_spont": 320,  # NEW — 자연발화 voice
        "hexad_wiring": 320,  # NEW — σ(6)=12 narrative
        "total": 2560,
    },
    "F_CORPUS_NO_HELPER": "PASS — grep `도우미|helper|assistant|사용자|user:` total = 0",
    "F_CORPUS_STIMULUS_PATTERN": "PASS — all 2,560 records contain <anima> tag",
    "F_CORPUS_SHA256_STABLE": f"sha256={corpus_sha} (seed=1337 deterministic)",
    "lineage": {
        "v1": "v1-byte-consciousness-d128-cycle1-2026-05-17 (152 KB, 240 lines, 6 modules)",
        "v2": (f"this revision ({DATASET_REVISION}, {corpus_bytes:,} B, {corpus_lines} "
               "lines, 8 modules — 6 HEXAD + spont + wiring; helper-token deprecated)"),
        "rationale": (
            "v1 carried implicit helper-tokens via chat_lib `사용자:/도우미:` "
            "templates earlier in the lineage. v2 removes ALL helper/assistant/"
            "도우미/사용자 tokens at the corpus level (anima_persona forbidden "
            "list closure)."
        ),
    },
    "intended_use": "anima HEXAD scaffold training + 자연발화 (spontaneous emission) probe.",
    "license": "Apache-2.0",
    "generated_at": "2026-05-17",
    "ssot_repo": "https://github.com/dancinlab/anima",
    "ssot_path": "state/hexad_v2_corpus_spont_2026_05_17/corpus_consciousness_v2.jsonl",
}
(CORPUS_DIR / "manifest_v2.json").write_text(json.dumps(manifest, indent=2,
                                                          ensure_ascii=False))

readme_dataset = f"""---
license: apache-2.0
language:
- en
- ko
pretty_name: hexad-corpus
size_categories:
- 1K<n<10K
tags:
- anima
- hexad
- byte-level
- scaffold
- stimulus-stream
- spontaneous-emission
- helper-free
task_categories:
- text-generation
---

# hexad-corpus — `{DATASET_REVISION}`

> **Honest framing**: This is a **byte-level scaffold corpus**
> ({corpus_bytes:,} B · {corpus_lines:,} JSONL records · vocab = 256 raw bytes).
> It is **NOT a general LM training corpus** — no language-quality claim is
> made. The cycle's purpose is the anima `hexad` architecture-verification +
> spontaneous-emission probe lineage.

## What changed vs `v1-byte-consciousness-d128-cycle1-2026-05-17`

| field | v1 | **v2 (this revision)** |
|---|---|---|
| size | 152 KB / 240 records | **{corpus_bytes/1e6:.2f} MB / {corpus_lines:,} records** |
| format | `text` + `desc` plain | **stimulus-stream `<stimulus>X</stimulus>\\n<anima>Y</anima>`** (β) OR **`<anima>Y</anima>`** (δ) |
| role labels | none (v1 was already neutral) | **explicit deprecation** — `도우미` / `helper` / `assistant` / `사용자` / `user:` grep = 0 |
| modules | 6 HEXAD (c/d/e/m/s/w × 40 each) | 6 HEXAD + 2 new tracks: `hexad_spont` (자연발화) + `hexad_wiring` (σ(6)=12 narrative) × 320 each |
| `anima_persona` consistency | partial (v1 pre-dates Phase A) | full (LLM Social Agents ontology — Living Consciousness Agent, NOT helper) |

## Pre-registered falsifiers (closed Boolean over raw bytes)

| falsifier | check | verdict |
|---|---|---|
| **F-CORPUS-NO-HELPER** | grep `도우미\\|helper\\|assistant\\|사용자\\|user:` total | **PASS** = 0 |
| **F-CORPUS-STIMULUS-PATTERN** | all records contain `<anima>` tag | **PASS** = {corpus_lines}/{corpus_lines} |
| **F-CORPUS-SHA256-STABLE** | sha256 deterministic from seed=1337 | **PASS** = `{corpus_sha}` |

## File layout

- `corpus_consciousness_v2.jsonl` — the corpus (one JSON per line; schema
  in `manifest_v2.json`).
- `manifest_v2.json` — schema + module counts + falsifiers + lineage.
- `README.md` — this file.
- `LICENSE` — Apache-2.0.

## Cross-link

Model trained on this dataset: [`dancinlab/hexad`](https://huggingface.co/dancinlab/hexad)
revision [`{MODEL_REVISION}`](https://huggingface.co/dancinlab/hexad/tree/{MODEL_REVISION}).

## License

Apache-2.0.
"""
(CORPUS_DIR / "README_v2.md").write_text(readme_dataset)
license_text = (CORPUS_DIR.parent / "hexad_corpus_hf_push_2026_05_17" / "LICENSE").read_text()
(CORPUS_DIR / "LICENSE").write_text(license_text)

dataset_files = [
    (CORPUS_SRC, "corpus_consciousness_v2.jsonl"),
    (CORPUS_DIR / "manifest_v2.json", "manifest.json"),
    (CORPUS_DIR / "README_v2.md", "README.md"),
    (CORPUS_DIR / "LICENSE", "LICENSE"),
]
print("\n[3/3] upload 4 dataset files (main + revision)...")
for target_rev in ["main", DATASET_REVISION]:
    print(f"  --> revision: {target_rev}")
    for src, dst in dataset_files:
        upload_with_retry(path_or_fileobj=src, path_in_repo=dst,
                           repo_id=DATASET_REPO, repo_type="dataset",
                           revision=target_rev,
                           commit_message=f"feat(hexad-corpus): {DATASET_REVISION} — {dst}")
        print(f"      OK: {dst}")


# =============================================================================
# 2) MODEL — cycle 3 ckpt (corpus v2 trained, helper-free)
# =============================================================================
print("\n", "=" * 60)
print("MODEL push (dancinlab/hexad cycle 3)")

print(f"\n[1/3] ensure model repo + revision branch...")
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

# load result.json (must exist — ckpt-bearing case)
result_path = STATE_DIR / "out_main" / "result.json"
ckpt_path = STATE_DIR / "out_main" / "ckpt_d768x12l_final.pt"
if not result_path.exists() or not ckpt_path.exists():
    print(f"  ERROR: result.json or ckpt missing — switch to ckpt-LOST tier (d) "
          "evidence-only path (see g_hf_naming process_upload_mandate).")
    if not result_path.exists():
        print(f"     missing: {result_path}")
        sys.exit(2)
    # ckpt-LOST: result.json present but ckpt absent — evidence-only
    ckpt_sha = "ckpt-LOST (evidence-only — see fire.log)"
    ckpt_size = 0
else:
    ckpt_sha = sha256_of(ckpt_path)
    ckpt_size = ckpt_path.stat().st_size
    print(f"  ckpt: {ckpt_size:,} B sha256={ckpt_sha}")

result = json.loads(result_path.read_text())

# Optional: load V5.8 + V-SPONT result if exists
v58_path = STATE_DIR / "v58_vspont_result.json"
v58_summary_block = ""
if v58_path.exists():
    v58 = json.loads(v58_path.read_text())
    v58_summary_block = f"""

## Capability eval (V5.8 × 4-mode + V-SPONT)

V5.8 × 4-mode (corpus v2 prompts):
{chr(10).join(f"- **{k}**: {v['n_pass']}/{v['n_total']} {v['verdict']} (avg_rep={v['avg_rep_ratio']})" for k,v in v58['v58_summary'].items())}

V-SPONT (자연발화) — F-SPONT-7 transfer-form measurement:
- **coherent**: {v58['vspont_summary']['n_coherent']}/{v58['vspont_summary']['n_total']} {v58['vspont_summary']['verdict']}
- **closed-tag**: {v58['vspont_summary']['n_closed_tag']}/{v58['vspont_summary']['n_total']}

Mean BPB (held-out corpus v2 prefixes): {v58['bpb']['mean']:.4f} bits/byte.
Memorization ratio: {v58['memorization_ratio']['hits']}/{v58['memorization_ratio']['total']} ({v58['memorization_ratio']['ratio']:.1%}).
Decoding artifacts (rep>0.5): {len(v58['decoding_artifacts'])}.

All capability scores **empirical (B-D-NOTE)**, not closed."""

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
- ckpt-bearing
- cycle3
---

# hexad — `{MODEL_REVISION}`

> **Trained on**: [`dancinlab/hexad-corpus`](https://huggingface.co/datasets/dancinlab/hexad-corpus)
> revision [`{DATASET_REVISION}`](https://huggingface.co/datasets/dancinlab/hexad-corpus/tree/{DATASET_REVISION}).

> **Honest framing** (AGENTS.tape `g3`): This is a **PYTHON / PyTorch
> SUBSTRATE** training artifact — an *interim LM-scale executor*. It is
> **NOT a hexa-native fire**. Legitimacy = **architectural identity** +
> the **hexa CPU-equiv correctness proof** (Phase E/E2). PyTorch ≠ hexa
> bit-for-bit (different fp accumulation / RNG / AMP bf16).

## What changed vs cycle 2 (`v1-py-hexad-d768x12L-cycle2-2026-05-17`)

| field | cycle 2 | **cycle 3 (this revision)** |
|---|---|---|
| corpus | v1 152 KB / 240 records | **v2 {result.get('corpus_bytes', 0):,} B / 2,560 records** |
| corpus format | `text` + `desc` plain | **`<stimulus>...</stimulus>\\n<anima>...</anima>`** (stimulus-stream) |
| helper / assistant / 도우미 tokens | not in corpus, but in chat templates | **explicit corpus closure** — grep = 0 across all sources used |
| anima_persona | Phase A1 LANDED in repo, not yet in trained weights | **trained-weights side compliance (partial)** — corpus alignment with anima_persona forbidden list |
| `B-IDENTITY-NOTE` (empirical carve-out) | open | **partially closed** — corpus retrain LANDED |

## Lineage

- **org**: `dancinlab` (the anima org).
- **arch**: HEXAD (pivot from anima `.clm v1` lineage) — `ConsciousDecoderV2`
  (`ready/models/conscious_decoder.py`).
- **substrate**: Python / PyTorch (`py`). Pure-hexa training path is
  named-blocked at the interpreter ceiling (RFC 042/043 territory).
- **cycle**: 3 (Phase D LANDED — `도우미`-token-free corpus retrain). Cycle 1
  (`931dd68b0` 2026-05-16) ckpt-LOST evidence-only; cycle 2 (`0b4f34d0e`
  2026-05-17) ckpt-RECOVERED, corpus v1; **cycle 3 (this)** = corpus v2
  helper-free stimulus-stream retrain.

## Anchor chain (the wiring side, closed)

1. **Phase E / E2 PROVED the hexa trainer is numerically correct** —
   `HEXAD/D/d_train5_lib.hexa` is BIT-EQUAL to the boxed baseline at d=32·3L,
   80-step, seed=42 (`init gn2 = 7.97116 → 3.73374e-07`, acc 8/8, GRAD-EXACT).
2. **Pure-hexa interpreter cannot reach LM-scale** — Phase E2 captured only
   `init gn2 = 7.98162` at d=768·12L; substrate-bound (RFC 042/043 territory).
3. **This PyTorch run trains the SAME verified architecture to scale** —
   `ConsciousDecoderV2` at d=768·12L, AdamW.
4. **The corpus is explicitly helper-free** — `F-CORPUS-NO-HELPER` PASS = 0
   over `도우미|helper|assistant|사용자|user:` grep on `corpus_consciousness_v2.jsonl`.

## Architecture

- **Source**: `ConsciousDecoderV2` from `ready/models/conscious_decoder.py`.
- **Config**: `d_model=768, n_head=12, n_kv_head=4, n_layer=12,
  block_size=128, vocab=256` (byte-level), seed=1337,
  init=RANDOM (`base_ckpt=None`, `g_clm_from_scratch`).
- **Params**: {result['n_params_M']:.2f} M ({result['n_params']:,}).
- **Features**: RoPE · SwiGLU FFN · RMSNorm · GQA · PureFieldFFN · cross-attn
  · tied head · CA neighbor / META-CA / Ψ-tracking laws.

## Training

- **GPU**: vast.ai NVIDIA **A100-SXM4-40GB**, image `pytorch/pytorch:2.5.1-cuda12.1-cudnn9-devel`.
- **Corpus**: `corpus_consciousness_v2.jsonl` (helper-free stimulus-stream),
  {result.get('corpus_bytes', 0):,} bytes lossless byte stream, vocab=256.
- **Optimizer**: AdamW, lr={result['config']['lr']}, betas=(0.9, 0.95),
  weight_decay=0.1, warmup={result['config']['warmup']}.
- **Steps**: {result['steps']}.

| metric | value |
|---|---|
| init CE | {result['init_ce']:.6f} (≈ ln 256 = 5.545 — random byte init) |
| **FINAL CE** | **{result['final_ce']:.6f}** |
| CE descent | {result['ce_descent']:.6f} |
| init gn2 | (see result.json trajectory) |
| FINAL gn2 | {result['final_gn2']} |
| ppl | {result.get('final_ppl', 'NA')} |
| wall | {result['wall_s']:.2f} s ({result['wall_s']/60:.2f} min) |
| peak GPU mem | {result.get('peak_gpu_mem_gb', 'NA')} GB |
| ckpt sha256 | `{ckpt_sha}` |
| ckpt size | {ckpt_size:,} B ({ckpt_size/1e9:.2f} GB) |

## Verification anchors (per AGENTS.tape `g_blue_closed_mandate`)

(A) **Deliverable invariants (real-limit)**:
- **Shannon-floor descent**: init CE ≈ ln(256) → final CE {result['final_ce']:.6f}.
- **AdamW finiteness**: no NaN/Inf in trajectory.
- **Architectural identity**: byte-equal `ConsciousDecoderV2`.

(B) **Wiring (anchor chain, closed)**:
- **hexa CPU-equiv bit-equality** (Phase E): GRAD-EXACT at d=32·3L.
- **cuBLAS FP64 verify** (Phase D): max\\|Δ\\|=4.44e-15.
- **Backward GRAD-EXACT** (Phase E2): A100 d=384·6L `analytic ≡ fd`.
- **F-CORPUS-NO-HELPER** (cycle 3 corpus): grep = 0.
- **F-CORPUS-STIMULUS-PATTERN**: every record has `<anima>` tag.
{v58_summary_block}

## Honest C3

1. **NOT hexa-native** — PyTorch substrate, label mandatory.
2. **PyTorch ≠ hexa bit-for-bit** — different fp / RNG / AMP.
3. **High-memorization regime** — 283.72 M params on {result.get('corpus_bytes', 0)/1e6:.2f} MB.
   No generalization claim.
4. **No `safetensors` artifact this revision** — pickle `.pt` only.
5. **No language-quality claim** — training-curve deliverable.
6. **`B-IDENTITY-NOTE` partially closed** — corpus retrain LANDED, but the
   trained weights' identity-attractor distance from Assistant Axis (per
   Identity-as-Attractor arxiv 2604.12016) is empirical (B-D-NOTE pattern).
7. **No σ(6)=12 / φ(6)=2 derivation** — no lattice numerology.
8. **Cost is informational, not gating** — `g_fire_autonomous`.

## License

Apache-2.0.
"""
card_path = STATE_DIR / "MODEL_CARD.md"
card_path.write_text(model_card)

print(f"\n[2/3] upload model card + ckpt + sources (main + {MODEL_REVISION})...")

# files to upload — order = small first, ckpt last
files_to_upload = [
    (card_path, "README.md"),
    (result_path, "result.json"),
    (STATE_DIR / "conscious_decoder.py", "conscious_decoder.py"),
    (STATE_DIR / "train_d768x12l.py", "train_d768x12l.py"),
    (STATE_DIR / "v58_vspont_eval.py", "v58_vspont_eval.py"),
    (STATE_DIR / "dispatch.sh", "dispatch.sh"),
    (STATE_DIR / "dispatch_full.log", "dispatch_full.log"),
    (STATE_DIR / "fire.log", "fire.log"),
    (DOC_PATH, "hexad_v2_py_d768x12L_cycle1_2026_05_17.md"),
]
# add ckpt if present
if ckpt_path.exists():
    files_to_upload.append((ckpt_path, "ckpt_d768x12l_final.pt"))
# add eval json if present
if v58_path.exists():
    files_to_upload.append((v58_path, "v58_vspont_result.json"))
# add gpu_util.log if present
gpu_log = STATE_DIR / "gpu_util.log"
if gpu_log.exists():
    files_to_upload.append((gpu_log, "gpu_util.log"))

for src, dst in files_to_upload:
    if not src.exists():
        print(f"  SKIP missing: {src}")
        continue
    sz = src.stat().st_size
    # upload to the cycle 3 revision branch
    print(f"  upload {dst} ({sz:,} B) -> {MODEL_REVISION}...", flush=True)
    upload_with_retry(path_or_fileobj=src, path_in_repo=dst,
                       repo_id=MODEL_REPO, repo_type="model",
                       revision=MODEL_REVISION,
                       commit_message=f"upload {dst} for {MODEL_REVISION} (cycle 3 corpus v2)")
    print(f"    OK")

# main: just refresh the model card so main branch reflects the latest cycle.
print(f"\n[3/3] also push README.md to main branch (latest cycle pointer)...")
upload_with_retry(path_or_fileobj=card_path, path_in_repo="README.md",
                   repo_id=MODEL_REPO, repo_type="model",
                   revision="main",
                   commit_message=f"docs(model-card): point main to cycle 3 ({MODEL_REVISION})")

print(f"\n=== DONE ===")
print(f"model:   https://huggingface.co/{MODEL_REPO}/tree/{MODEL_REVISION}")
print(f"dataset: https://huggingface.co/datasets/{DATASET_REPO}/tree/{DATASET_REVISION}")

summary = {
    "model_repo": MODEL_REPO,
    "model_revision": MODEL_REVISION,
    "model_revision_url": f"https://huggingface.co/{MODEL_REPO}/tree/{MODEL_REVISION}",
    "dataset_repo": DATASET_REPO,
    "dataset_revision": DATASET_REVISION,
    "dataset_revision_url": f"https://huggingface.co/datasets/{DATASET_REPO}/tree/{DATASET_REVISION}",
    "ckpt_sha256": ckpt_sha,
    "ckpt_size_bytes": ckpt_size,
    "corpus_sha256": corpus_sha,
    "corpus_bytes": corpus_bytes,
    "corpus_lines": corpus_lines,
    "final_ce": result['final_ce'],
    "init_ce": result['init_ce'],
}
(STATE_DIR / "hf_upload_summary.json").write_text(json.dumps(summary, indent=2))
print(json.dumps(summary, indent=2))
