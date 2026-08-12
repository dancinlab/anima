#!/usr/bin/env python3
"""Build the preregistered turn-complete OASST1 treatment dataset."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import sys


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
CORE = ROOT / "core"
if str(CORE) not in sys.path:
    sys.path.insert(0, str(CORE))

import generator as chat_runtime


def _load_shared_builder():
    path = (ROOT / "state" / "anima_303m_r0_conversation_2026_08_12" /
            "build_dataset.py")
    spec = importlib.util.spec_from_file_location("r0_conversation_builder", path)
    module = importlib.util.module_from_spec(spec)
    if spec.loader is None:
        raise RuntimeError("conversation dataset builder loader is missing")
    spec.loader.exec_module(module)
    return module


builder = _load_shared_builder()


def _sha256(path: str | Path) -> str:
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _audit_serialized_documents(documents: list[str], max_bytes: int) -> dict:
    invalid = 0
    partial = 0
    largest = 0
    assistant_turns = 0
    for document in documents:
        encoded = document.encode("utf-8", "strict")
        largest = max(largest, len(encoded))
        role_lines = []
        for line in document.splitlines():
            if line.startswith(chat_runtime.CHAT_USER_PREFIX):
                role_lines.append("user")
                if not line[len(chat_runtime.CHAT_USER_PREFIX):].strip():
                    partial += 1
            elif line.startswith(chat_runtime.CHAT_ASSISTANT_PREFIX):
                role_lines.append("assistant")
                assistant_turns += 1
                if not line[len(chat_runtime.CHAT_ASSISTANT_PREFIX):].strip():
                    partial += 1
        expected = ["user" if index % 2 == 0 else "assistant"
                    for index in range(len(role_lines))]
        if (not role_lines or role_lines != expected
                or role_lines[-1] != "assistant" or len(encoded) > max_bytes):
            invalid += 1
    return {
        "documents": len(documents),
        "assistant_turns_in_documents": assistant_turns,
        "canonical_alternation_invalid": invalid,
        "partial_role_or_response": partial,
        "largest_serialized_document_bytes": largest,
    }


def build(protocol_path: str | Path, output: str | Path, token: str | None) -> dict:
    import pyarrow.parquet as pq
    from huggingface_hub import hf_hub_download

    protocol_path = Path(protocol_path)
    protocol = json.loads(protocol_path.read_text(encoding="utf-8"))
    panel_path = (protocol_path.parent / protocol["evaluation_panel"]["file"]).resolve()
    panel_sha = _sha256(panel_path)
    if panel_sha != protocol["evaluation_panel"]["sha256"]:
        raise RuntimeError("evaluation panel SHA differs from preregistration")
    panel = json.loads(panel_path.read_text(encoding="utf-8"))
    chat_runtime.gen_chat_validate_template(
        panel["template"], max_new=panel["decode"]["max_new_bytes"])

    output = Path(output)
    output.mkdir(parents=True, exist_ok=True)
    db_path = output / ".documents.sqlite3"
    if db_path.exists():
        db_path.unlink()
    registry = builder.DocumentRegistry(db_path, preserve_role_lines=True)
    source = protocol["fixed_source"]
    filenames = [
        "data/train-00000-of-00001-b42a775f407cee45.parquet",
        "data/validation-00000-of-00001-134b8fd0c89408b6.parquet",
    ]
    max_bytes = int(protocol["single_variable_data_test"]["gates"]
                    ["all_serialized_documents_fit_bytes_max"])
    split_stats = {}
    source_files = []
    serialized_documents = []
    try:
        for filename, split in zip(filenames, ("train", "validation")):
            path = hf_hub_download(repo_id=source["repository"],
                                   revision=source["revision"], filename=filename,
                                   repo_type="dataset", token=token)
            rows = pq.read_table(path).to_pylist()
            documents, stats = builder.oasst_turn_documents(
                rows, language=source["language"], max_bytes=max_bytes)
            split_stats[split] = stats
            source_files.append({"file": filename, "bytes": Path(path).stat().st_size,
                                 "sha256": _sha256(path)})
            for document in documents:
                registry.add("en_dialogue", split, document)
            serialized_documents.extend(documents)
            registry.commit()

        prompts = [turn["user"] for item in panel["items"] for turn in item["turns"]]
        removed = registry.remove_contamination(prompts)
        remaining = registry.contamination(prompts)
        cells = registry.write_cells(output, ["en_dialogue"])
        audit = _audit_serialized_documents(serialized_documents, max_bytes)
        fitting = sum(value["fitting_assistant_turns"] for value in split_stats.values())
        serialized = sum(value["serialized_assistant_turns"] for value in split_stats.values())
        coverage = serialized / fitting if fitting else 0.0
        overlap = registry.overlap()
        gates = protocol["single_variable_data_test"]["gates"]
        gate_results = {
            "canonical_alternation": audit["canonical_alternation_invalid"]
            == gates["canonical_alternation_invalid"],
            "partial_role_or_response": audit["partial_role_or_response"]
            == gates["partial_role_or_response"],
            "train_validation_exact_overlap": overlap
            == gates["train_validation_exact_overlap"],
            "panel_exact_contamination": len(remaining)
            == gates["panel_exact_contamination"],
            "eligible_assistant_turn_coverage": coverage
            >= gates["eligible_assistant_turn_coverage_min"],
            "serialized_document_bytes": audit["largest_serialized_document_bytes"]
            <= max_bytes,
        }
        manifest = {
            "schema": "anima-303m-v0-v2-turn-dataset/v1",
            "protocol_sha256": _sha256(protocol_path),
            "panel_sha256": panel_sha,
            "source": source,
            "source_files": source_files,
            "construction": {
                "algorithm": "every eligible assistant target with longest complete ancestry suffix",
                "max_bytes": max_bytes,
                "byte_or_turn_truncation": False,
                "split_stats": split_stats,
                "coverage": coverage,
            },
            "audit": audit,
            "dedup": {
                "candidates_seen": registry.seen,
                "cross_train_validation_hash_overlap": overlap,
                "validation_wins_duplicate_ownership": True,
            },
            "panel_decontamination": {
                "removed_documents": len({row["document_sha256"] for row in removed}),
                "remaining_matches": remaining,
            },
            "cells": cells,
            "gates": gate_results,
            "verdict": "PASS" if all(gate_results.values()) else "FAIL",
        }
        (output / "manifest.json").write_text(
            json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        (output / "README.md").write_text(
            "# Anima 303M V0/V2 turn-complete dialogue data\n\n"
            "Private immutable training data derived from the pinned Apache-2.0 "
            "OpenAssistant/oasst1 revision. Every record is a complete canonical "
            "user/assistant trajectory fitting 513 bytes; no response is truncated.\n",
            encoding="utf-8")
        (output / "LICENSES.md").write_text(
            "# Source licenses\n\n- OpenAssistant/oasst1: Apache-2.0.\n",
            encoding="utf-8")
        if manifest["verdict"] != "PASS":
            raise RuntimeError("turn dataset failed preregistered gates: "
                               + json.dumps(gate_results, sort_keys=True))
        return manifest
    finally:
        registry.close()
        if db_path.exists():
            db_path.unlink()


def upload(output: str | Path, repo_id: str, token: str) -> str:
    from huggingface_hub import HfApi
    api = HfApi(token=token)
    api.create_repo(repo_id=repo_id, repo_type="dataset", private=True, exist_ok=True)
    commit = api.upload_folder(repo_id=repo_id, repo_type="dataset",
                               folder_path=str(output),
                               commit_message="Publish preregistered V0/V2 turn-complete data")
    info = api.dataset_info(repo_id=repo_id, revision=commit.oid)
    if not info.private:
        raise RuntimeError("refusing public dataset result")
    return commit.oid


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--protocol", default=str(HERE / "protocol.json"))
    parser.add_argument("--output", required=True)
    parser.add_argument("--upload", action="store_true")
    args = parser.parse_args()
    token = os.environ.get("HF_TOKEN")
    manifest = build(args.protocol, args.output, token)
    result = {"verdict": manifest["verdict"], "coverage": manifest["construction"]["coverage"],
              "cells": manifest["cells"], "gates": manifest["gates"]}
    if args.upload:
        if not token:
            raise SystemExit("HF_TOKEN is required for upload")
        protocol = json.loads(Path(args.protocol).read_text(encoding="utf-8"))
        result["uploaded_revision"] = upload(
            args.output, protocol["dataset_repository"], token)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
