#!/usr/bin/env python3
"""Download only the preregistered native-303M assets from pinned HF revisions."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

from huggingface_hub import snapshot_download

from run_recovery import load_protocol


def declared_data_patterns(data_root: Path) -> list[str]:
    root = json.loads((data_root / "manifest.json").read_text(encoding="utf-8"))
    target_root = data_root / "data-conversation-target"
    target = json.loads((target_root / "manifest.json").read_text(encoding="utf-8"))
    patterns = ["manifest.json", "data-conversation-target/manifest.json"]
    patterns.extend(root["splits"]["train_general"])
    patterns.extend(root["splits"]["validation_general"])
    for split in ("train_dialogue", "validation_dialogue"):
        patterns.extend(f"data-conversation-target/{name}" for name in target["splits"][split])
    if len(patterns) != len(set(patterns)):
        raise ValueError("pinned data manifests contain duplicate paths")
    return patterns


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model-root", type=Path, required=True)
    parser.add_argument("--data-root", type=Path, required=True)
    args = parser.parse_args()
    token = os.environ.get("HF_TOKEN")
    if not token:
        parser.error("HF_TOKEN is required")
    protocol = load_protocol()
    parent = protocol["parent"]
    model_patterns = [
        relative for relative in protocol["source_hashes"]
        if relative not in {"manifest.json", "data-conversation-target/manifest.json"}
    ]
    model_patterns.extend((
        parent["base_checkpoint"],
        "checkpoints/step-035000/tokenizer.json",
        "checkpoints/step-035000/train_summary.json",
    ))
    snapshot_download(
        repo_id=parent["model_repository"], revision=parent["model_revision"],
        token=token, local_dir=args.model_root, allow_patterns=model_patterns,
    )
    snapshot_download(
        repo_id=parent["data_repository"], repo_type="dataset",
        revision=parent["data_revision"], token=token, local_dir=args.data_root,
        allow_patterns=["manifest.json", "data-conversation-target/manifest.json"],
    )
    patterns = declared_data_patterns(args.data_root)
    snapshot_download(
        repo_id=parent["data_repository"], repo_type="dataset",
        revision=parent["data_revision"], token=token, local_dir=args.data_root,
        allow_patterns=patterns,
    )
    missing = [str(path) for path in (
        *(args.model_root / item for item in model_patterns),
        *(args.data_root / item for item in patterns),
    ) if not path.is_file()]
    if missing:
        raise FileNotFoundError(f"pinned HF download is incomplete: {missing}")
    files = [path for root in (args.model_root, args.data_root) for path in root.rglob("*")
             if path.is_file() and ".cache" not in path.parts]
    print(json.dumps({
        "model_revision": parent["model_revision"],
        "data_revision": parent["data_revision"],
        "declared_data_files": len(patterns),
        "local_files": len(files),
        "local_bytes": sum(path.stat().st_size for path in files),
    }, sort_keys=True), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
