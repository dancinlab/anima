#!/usr/bin/env python3
"""HF upload — dancinlab/hexad-corpus revision v1-byte-consciousness-d128-cycle1-2026-05-17.

Per AGENTS.tape g_hf_naming (d=2026-05-17):
- canonical dataset slot: dancinlab/hexad-corpus (PUBLIC).
- revision tag: v1-byte-consciousness-d128-cycle1-2026-05-17
  (substrate-independent corpus -> kind = byte-consciousness).
- 4 file payload: corpus_consciousness_v1.jsonl + manifest.json + README.md + LICENSE.
- model card cross-link: add trained_on dataset reference on dancinlab/hexad.
"""
import json
import os
import shutil
import sys
import time
from pathlib import Path

from huggingface_hub import HfApi, create_repo, upload_file

DATASET_REPO = "dancinlab/hexad-corpus"
MODEL_REPO = "dancinlab/hexad"
REVISION = "v1-byte-consciousness-d128-cycle1-2026-05-17"
MODEL_REVISION = "v1-py-hexad-d768x12L-cycle2-2026-05-17"

STATE_DIR = Path("/Users/ghost/core/anima/state/hexad_corpus_hf_push_2026_05_17")
CORPUS_SRC = Path("/Users/ghost/core/anima/training/corpus_consciousness_v1.jsonl")
MODEL_CARD_SRC = Path(
    "/Users/ghost/core/anima/state/hexad_py_d768x12L_fire_2026_05_17/MODEL_CARD.md"
)

api = HfApi()
who = api.whoami()["name"]
print(f"whoami: {who}")

# ----------------------------------------------------------------------
# Step 1: ensure DATASET repo exists + is PUBLIC
# ----------------------------------------------------------------------
print(f"\n[1/6] ensure dataset repo {DATASET_REPO} (PUBLIC)...")
try:
    info = api.repo_info(DATASET_REPO, repo_type="dataset")
    print(f"  exists: private={info.private}, id={info.id}")
    if info.private:
        api.update_repo_settings(
            repo_id=DATASET_REPO, repo_type="dataset", private=False
        )
        print("  -> flipped to PUBLIC")
except Exception as e:
    msg = str(e)
    if "404" in msg or "Repository Not Found" in msg:
        print("  not found -> create_repo PUBLIC ...")
        create_repo(
            DATASET_REPO,
            repo_type="dataset",
            private=False,
            exist_ok=True,
        )
        time.sleep(2)
        info = api.repo_info(DATASET_REPO, repo_type="dataset")
        print(f"  created: private={info.private}, id={info.id}")
    else:
        raise

# ----------------------------------------------------------------------
# Step 2: create the tagged revision branch
# ----------------------------------------------------------------------
print(f"\n[2/6] create branch {REVISION} on dataset repo...")
try:
    api.create_branch(
        repo_id=DATASET_REPO,
        repo_type="dataset",
        branch=REVISION,
        exist_ok=True,
    )
    print("  branch ready")
except Exception as e:
    print(f"  branch create note: {e}")

# ----------------------------------------------------------------------
# Step 3: stage 4 files in a deterministic dir
# ----------------------------------------------------------------------
print("\n[3/6] stage 4 files...")
# copy the corpus into the state dir so the upload is byte-equal to repo SSOT
staged_corpus = STATE_DIR / "corpus_consciousness_v1.jsonl"
shutil.copyfile(CORPUS_SRC, staged_corpus)

import hashlib

h = hashlib.sha256()
with staged_corpus.open("rb") as f:
    for chunk in iter(lambda: f.read(1 << 20), b""):
        h.update(chunk)
corpus_sha = h.hexdigest()
corpus_bytes = staged_corpus.stat().st_size
with staged_corpus.open() as f:
    corpus_lines = sum(1 for _ in f)

print(f"  corpus: {corpus_bytes:,} B  lines={corpus_lines}  sha256={corpus_sha}")
assert (
    corpus_sha
    == "804664361e639be7ecceae6ff3c470961e015090c264da9eac1df8716144681f"
), "corpus sha drift!"
assert corpus_bytes == 151943, "corpus bytes drift!"
assert corpus_lines == 240, "corpus lines drift!"

files = [
    (staged_corpus, "corpus_consciousness_v1.jsonl"),
    (STATE_DIR / "manifest.json", "manifest.json"),
    (STATE_DIR / "README.md", "README.md"),
    (STATE_DIR / "LICENSE", "LICENSE"),
]
for src, dst in files:
    assert src.exists(), f"staged file missing: {src}"
    print(f"  staged: {src.name} ({src.stat().st_size:,} B) -> {dst}")

# ----------------------------------------------------------------------
# Step 4: upload to dataset repo  -- on main AND on tagged revision
# ----------------------------------------------------------------------
print("\n[4/6] upload 4 files to dataset repo (main + tagged revision)...")
for target_rev in ["main", REVISION]:
    print(f"  --> revision: {target_rev}")
    for src, dst in files:
        for attempt in range(3):
            try:
                upload_file(
                    path_or_fileobj=str(src),
                    path_in_repo=dst,
                    repo_id=DATASET_REPO,
                    repo_type="dataset",
                    revision=target_rev,
                    commit_message=(
                        f"feat(hexad-corpus): {REVISION} — {dst} (PUBLIC dataset push)"
                    ),
                )
                print(f"      OK: {dst}")
                break
            except Exception as e:
                print(f"      attempt {attempt+1} failed for {dst}: {e}")
                if attempt == 2:
                    raise
                time.sleep(5)

# ----------------------------------------------------------------------
# Step 5: model card cross-link (dancinlab/hexad README -> dataset)
# ----------------------------------------------------------------------
print(f"\n[5/6] update model card on {MODEL_REPO} (add dataset cross-link)...")
mc = MODEL_CARD_SRC.read_text()

# add `datasets:` line to YAML front matter if missing
if "datasets:" not in mc.split("---", 2)[1]:
    front, body = mc.split("---", 2)[1], mc.split("---", 2)[2]
    # insert datasets line after `library_name:` row
    new_front_lines = []
    inserted = False
    for line in front.splitlines():
        new_front_lines.append(line)
        if line.startswith("library_name:") and not inserted:
            new_front_lines.append("datasets:")
            new_front_lines.append("- dancinlab/hexad-corpus")
            inserted = True
    if not inserted:
        # fallback: append at end of front matter
        new_front_lines.append("datasets:")
        new_front_lines.append("- dancinlab/hexad-corpus")
    new_front = "\n".join(new_front_lines)
    mc = "---" + new_front + "---" + body
    print("  -> added 'datasets: [dancinlab/hexad-corpus]' to front matter")

# add a dataset cross-link section near top of body (if missing)
cross_link_line = (
    "> **Trained on**: [`dancinlab/hexad-corpus`](https://huggingface.co/datasets/dancinlab/hexad-corpus) "
    f"revision [`{REVISION}`](https://huggingface.co/datasets/dancinlab/hexad-corpus/tree/{REVISION})."
)
if "dancinlab/hexad-corpus" not in mc.split("---", 2)[2]:
    body_marker = "## Lineage"
    if body_marker in mc:
        mc = mc.replace(
            body_marker,
            cross_link_line + "\n\n" + body_marker,
            1,
        )
        print("  -> inserted 'Trained on' cross-link before ## Lineage")
    else:
        mc = mc + "\n\n" + cross_link_line + "\n"
        print("  -> appended 'Trained on' cross-link at EOF")
else:
    print("  -> dataset cross-link already present, skip")

# persist updated model card locally for the commit
updated_mc_path = STATE_DIR / "MODEL_CARD_with_dataset_xlink.md"
updated_mc_path.write_text(mc)

# upload to MODEL repo: main + the cycle 2 revision
print("  uploading model card README.md (cross-link) to dancinlab/hexad ...")
for target_rev in ["main", MODEL_REVISION]:
    for attempt in range(3):
        try:
            upload_file(
                path_or_fileobj=str(updated_mc_path),
                path_in_repo="README.md",
                repo_id=MODEL_REPO,
                repo_type="model",
                revision=target_rev,
                commit_message=(
                    f"feat(model-card): cross-link dataset dancinlab/hexad-corpus {REVISION}"
                ),
            )
            print(f"      OK: README.md on revision {target_rev}")
            break
        except Exception as e:
            print(f"      attempt {attempt+1} failed: {e}")
            if attempt == 2:
                raise
            time.sleep(5)

# ----------------------------------------------------------------------
# Step 6: verify revision
# ----------------------------------------------------------------------
print("\n[6/6] verify dataset revision...")
refs = api.list_repo_refs(DATASET_REPO, repo_type="dataset")
print("  branches:", [b.name for b in refs.branches])
print("  tags:", [t.name for t in refs.tags])
info = api.repo_info(DATASET_REPO, repo_type="dataset", revision=REVISION)
print(f"  revision sha @ {REVISION}: {info.sha}")
print(f"  private: {info.private}")
print(f"  siblings: {[s.rfilename for s in info.siblings]}")

# Final summary JSON
summary = {
    "dataset_repo": DATASET_REPO,
    "dataset_url": f"https://huggingface.co/datasets/{DATASET_REPO}",
    "revision": REVISION,
    "revision_url": f"https://huggingface.co/datasets/{DATASET_REPO}/tree/{REVISION}",
    "revision_sha": info.sha,
    "visibility": "private" if info.private else "PUBLIC",
    "corpus_sha256": corpus_sha,
    "corpus_bytes": corpus_bytes,
    "corpus_lines": corpus_lines,
    "files_uploaded": [dst for _, dst in files],
    "model_repo_xlink": MODEL_REPO,
    "model_revision_xlink": MODEL_REVISION,
    "whoami": who,
}
(STATE_DIR / "upload_summary.json").write_text(json.dumps(summary, indent=2))
print("\n=== SUMMARY ===")
print(json.dumps(summary, indent=2))
print("DONE.")
