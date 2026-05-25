#!/usr/bin/env python3
"""Upload vP21M LoRA adapter to dancinlab/anima-vp21m (private).

Per @D a_hf_complete: weights + config + tokenizer + model card all required.
"""
import os
import sys
import json
import subprocess
from pathlib import Path

ADAPTER_DIR = Path("/Users/ghost/core/anima/HEXAD/UNCLASSIFIED/state/grid_3b_s187_2026_05_21/vP21M/lora_adapter")
REPO_ID = "dancinlab/anima-vp21m"
PRIVATE = True

# token from secret
tok = subprocess.run(["secret", "get", "hf.token"],
                     capture_output=True, text=True, check=True).stdout.strip()
if not tok:
    print("FATAL: no hf.token secret"); sys.exit(1)

os.environ["HF_TOKEN"] = tok

from huggingface_hub import HfApi, create_repo, upload_folder

api = HfApi(token=tok)

# 1. ensure repo exists
try:
    repo_url = create_repo(repo_id=REPO_ID, repo_type="model",
                            private=PRIVATE, exist_ok=True, token=tok)
    print(f"[ok] repo ready: {repo_url}")
except Exception as e:
    print(f"FATAL create_repo: {e}"); sys.exit(1)

# 2. file manifest verify (a_hf_complete)
REQUIRED = ["adapter_model.safetensors", "adapter_config.json",
            "tokenizer.json", "tokenizer_config.json",
            "special_tokens_map.json", "added_tokens.json",
            "vocab.json", "merges.txt", "README.md"]
present = sorted(p.name for p in ADAPTER_DIR.iterdir() if p.is_file())
missing = [r for r in REQUIRED if r not in present]
if missing:
    print(f"FATAL missing artifacts: {missing}"); sys.exit(1)
print(f"[ok] manifest verified: {len(present)} files present")
for p in ADAPTER_DIR.iterdir():
    if p.is_file():
        print(f"     {p.name} ({p.stat().st_size:,} bytes)")

# 3. upload
print(f"[upload] folder {ADAPTER_DIR} → {REPO_ID} (private={PRIVATE})")
url = upload_folder(folder_path=str(ADAPTER_DIR), repo_id=REPO_ID,
                    repo_type="model", token=tok,
                    commit_message="anima-vp21m LoRA r32 multilingual (en/ko/zh/ru/ja) — VP21M_WORKS")
print(f"[ok] upload complete: {url}")

# 4. verify upload manifest
remote = sorted(f.rfilename for f in api.list_repo_files(REPO_ID, token=tok)
                if not f.startswith(".") if hasattr(f, "rfilename"))
if not remote:
    remote = sorted(api.list_repo_files(REPO_ID, token=tok))
print(f"[verify] remote files ({len(remote)}):")
for f in remote:
    print(f"     {f}")
remote_missing = [r for r in REQUIRED if r not in remote]
if remote_missing:
    print(f"WARN: remote missing {remote_missing}")
    sys.exit(2)
print(f"[done] dancinlab/anima-vp21m PRIVATE — complete per a_hf_complete")
