#!/usr/bin/env python3
"""Upload and independently verify this experiment's private HF custody bundle."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import shutil

from huggingface_hub import HfApi, hf_hub_download


REPOSITORY = "dancinlab/anima-native-303m-replay-recovery-2026-08-14"
EXPERIMENT = Path("/workspace/anima/state/anima_native_303m_replay_recovery_2026_08_14")
OUTPUT = Path("/workspace/output")
STAGE = OUTPUT / "hf-stage"
VERIFY = OUTPUT / "hf-verify"
CUSTODY = OUTPUT / "custody.json"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sources() -> dict[str, Path]:
    return {
        "model/final.pt": OUTPUT / "replay/final.pt",
        "model/resume.pt": OUTPUT / "replay/resume.pt",
        "model/tokenizer.json": OUTPUT / "replay/tokenizer.json",
        "model/train_summary.json": OUTPUT / "replay/train_summary.json",
        "evidence/broad_retention.json": OUTPUT / "broad_retention.json",
        "evidence/native_result.json": OUTPUT / "native_result.json",
        "evidence/canonical_result.json": OUTPUT / "canonical_result.json",
        "evidence/source_panel.json": OUTPUT / "source_panel.json",
        "evidence/train.log": OUTPUT / "train.log",
        "evidence/gpu.csv": OUTPUT / "gpu.csv",
        "evidence/model_hashes.txt": OUTPUT / "model_hashes.txt",
        "README.md": EXPERIMENT / "README.md",
        "protocol.json": EXPERIMENT / "protocol.json",
        "result.json": EXPERIMENT / "result.json",
        "manual_review.json": EXPERIMENT / "manual_review.json",
        "code/run_recovery.py": EXPERIMENT / "run_recovery.py",
        "code/run_pinned_trainer.py": EXPERIMENT / "run_pinned_trainer.py",
        "code/download_assets.py": EXPERIMENT / "download_assets.py",
    }


def main() -> int:
    token = os.environ.get("HF_TOKEN")
    if not token:
        raise SystemExit("HF_TOKEN is required")
    files = sources()
    missing = [str(path) for path in files.values() if not path.is_file()]
    if missing:
        raise FileNotFoundError(f"custody source is incomplete: {missing}")
    if STAGE.exists() or VERIFY.exists():
        raise FileExistsError("refusing to reuse custody staging or verification directories")
    for relative, source in files.items():
        target = STAGE / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        os.link(source, target)

    api = HfApi(token=token)
    api.create_repo(REPOSITORY, repo_type="model", private=True, exist_ok=True)
    artifact_commit = api.upload_folder(
        repo_id=REPOSITORY, repo_type="model", folder_path=STAGE,
        commit_message="Preserve failed native 303M replay recovery arm",
    )
    revision = artifact_commit.oid
    expected = {
        relative: {"size": source.stat().st_size, "sha256": sha256(source)}
        for relative, source in files.items()
    }
    verified = {}
    for relative, row in expected.items():
        downloaded = Path(hf_hub_download(
            repo_id=REPOSITORY, repo_type="model", revision=revision,
            filename=relative, local_dir=VERIFY, token=token, force_download=True,
        ))
        actual = {"size": downloaded.stat().st_size, "sha256": sha256(downloaded)}
        actual["pass"] = actual["size"] == row["size"] and actual["sha256"] == row["sha256"]
        verified[relative] = {"expected": row, "downloaded": actual}
    passed = all(row["downloaded"]["pass"] for row in verified.values())
    info = api.repo_info(REPOSITORY, repo_type="model", revision=revision)
    custody = {
        "schema": "anima-native-303m-replay-recovery-custody/v1",
        "repository": REPOSITORY,
        "artifact_revision": revision,
        "private": bool(info.private),
        "files": verified,
        "file_count": len(verified),
        "bytes": sum(row["expected"]["size"] for row in verified.values()),
        "pass": passed and bool(info.private),
    }
    CUSTODY.write_text(json.dumps(custody, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    metadata_commit = api.upload_file(
        repo_id=REPOSITORY, repo_type="model", path_or_fileobj=CUSTODY,
        path_in_repo="custody.json", commit_message="Record independent custody verification",
    )
    custody["metadata_revision"] = metadata_commit.oid
    CUSTODY.write_text(json.dumps(custody, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    shutil.rmtree(VERIFY)
    shutil.rmtree(STAGE)
    print(json.dumps({
        "repository": REPOSITORY, "artifact_revision": revision,
        "metadata_revision": metadata_commit.oid, "files": len(verified),
        "bytes": custody["bytes"], "pass": custody["pass"],
    }, sort_keys=True), flush=True)
    return 0 if custody["pass"] else 3


if __name__ == "__main__":
    raise SystemExit(main())
