#!/usr/bin/env python3
"""Push updated MODEL_CARD.md (with V5.8 capability eval) to HF
dancinlab/hexad — main + cycle 2 revision branch.

Per AGENTS.tape g_hf_naming d=2026-05-17, the canonical model README is the
MODEL_CARD.md content (English, honest framing).
"""
import sys
from pathlib import Path
from huggingface_hub import HfApi, upload_file

REPO_ID = "dancinlab/hexad"
REVISION = "v1-py-hexad-d768x12L-cycle2-2026-05-17"
CARD_PATH = Path("/Users/ghost/core/anima/state/hexad_py_d768x12L_fire_2026_05_17/MODEL_CARD.md")

api = HfApi()
me = api.whoami()["name"]
print(f"whoami: {me}")
assert CARD_PATH.exists(), CARD_PATH
print(f"MODEL_CARD.md: {CARD_PATH.stat().st_size:,} bytes")

for ref in ["main", REVISION]:
    print(f"[upload] README.md -> {REPO_ID}@{ref}")
    res = upload_file(
        path_or_fileobj=str(CARD_PATH),
        path_in_repo="README.md",
        repo_id=REPO_ID,
        repo_type="model",
        revision=ref,
        commit_message=f"V5.8 × 4-mode capability eval (cycle 2, 2026-05-17) — model card update",
    )
    print(f"  -> {res}")

print("done.")
