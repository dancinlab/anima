#!/usr/bin/env python3
"""Build the preregistered V1 short/long context views from pinned OASST1."""

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
if str(ROOT / "core") not in sys.path:
    sys.path.insert(0, str(ROOT / "core"))

import generator


def _load_parent_builder():
    path = ROOT / "state/anima_303m_r0_conversation_2026_08_12/build_dataset.py"
    spec = importlib.util.spec_from_file_location("r0_conversation_builder", path)
    module = importlib.util.module_from_spec(spec)
    if spec.loader is None:
        raise RuntimeError("conversation dataset builder loader is missing")
    spec.loader.exec_module(module)
    return module


PARENT = _load_parent_builder()


def _sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _view_bytes(documents: list[str]) -> bytes:
    return ("\n\n".join(documents) + "\n\n").encode("utf-8", "strict")


def _sha256_file(path: str | Path) -> str:
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _canonical(document: str) -> bool:
    roles = []
    for line in document.splitlines():
        if line.startswith(generator.CHAT_USER_PREFIX):
            roles.append("user")
        elif line.startswith(generator.CHAT_ASSISTANT_PREFIX):
            roles.append("assistant")
    expected = ["user" if index % 2 == 0 else "assistant"
                for index in range(len(roles))]
    return bool(roles and roles == expected and roles[-1] == "assistant")


def build(protocol_path: str | Path, output: str | Path, token: str | None) -> dict:
    import pyarrow.parquet as pq
    from huggingface_hub import hf_hub_download

    protocol_path = Path(protocol_path)
    protocol = json.loads(protocol_path.read_text(encoding="utf-8"))
    if protocol.get("schema") != "anima-303m-v1-context-micro/v1":
        raise RuntimeError("unexpected V1 protocol schema")
    panel_path = (protocol_path.parent / protocol["evaluation_panel"]["file"]).resolve()
    panel_sha = _sha256_file(panel_path)
    if panel_sha != protocol["evaluation_panel"]["sha256"]:
        raise RuntimeError("evaluation panel SHA differs from preregistration")
    panel = json.loads(panel_path.read_text(encoding="utf-8"))
    generator.gen_chat_validate_template(
        panel["template"], max_new=panel["decode"]["max_new_bytes"])

    source = protocol["fixed_source"]
    filenames = {
        "train": "data/train-00000-of-00001-b42a775f407cee45.parquet",
        "validation": "data/validation-00000-of-00001-134b8fd0c89408b6.parquet",
    }
    rows_by_split = {}
    source_files = []
    for split, filename in filenames.items():
        path = hf_hub_download(
            repo_id=source["repository"], revision=source["revision"],
            filename=filename, repo_type="dataset", token=token)
        rows_by_split[split] = pq.read_table(path).to_pylist()
        source_files.append({"split": split, "file": filename,
                             "bytes": Path(path).stat().st_size,
                             "sha256": _sha256_file(path)})

    census = {}
    documents_2049 = {}
    invalid = 0
    for max_bytes in protocol["context_census"]["max_serialized_bytes"]:
        total_fitting = 0
        total_valid = 0
        split_stats = {}
        for split, rows in rows_by_split.items():
            documents, stats = PARENT.oasst_turn_documents(
                rows, language=source["language"], max_bytes=max_bytes)
            split_stats[split] = stats
            total_fitting += stats["fitting_assistant_turns"]
            total_valid += stats["valid_alternating_ancestry"]
            if max_bytes == 2049:
                documents_2049[split] = sorted(
                    set(documents), key=lambda value: _sha256_bytes(value.encode("utf-8")))
                invalid += sum(not _canonical(value) for value in documents)
        census[str(max_bytes)] = {
            "fitting_targets": total_fitting,
            "valid_alternating_targets": total_valid,
            "coverage": total_fitting / total_valid if total_valid else 0.0,
            "split_stats": split_stats,
        }

    expected_census = protocol["context_census"]["observed_fitting_targets"]
    if {key: value["fitting_targets"] for key, value in census.items()} != expected_census:
        raise RuntimeError("context census differs from preregistration")
    if any(value["valid_alternating_targets"]
           != protocol["context_census"]["valid_alternating_targets"]
           for value in census.values()):
        raise RuntimeError("valid target count differs from preregistration")

    views = {}
    selected_documents = {}
    for split, documents in documents_2049.items():
        bands = {
            "short": [value for value in documents if len(value.encode("utf-8")) <= 513],
            "long": [value for value in documents
                     if 513 < len(value.encode("utf-8")) <= 2049],
        }
        for band, values in bands.items():
            view_name = f"{band}_{split}"
            registered = protocol["data_views"][view_name]
            chosen = values[:int(registered["documents"])]
            blob = _view_bytes(chosen)
            digest = _sha256_bytes(blob)
            if digest != registered["sha256"]:
                raise RuntimeError(f"{view_name} SHA differs from preregistration")
            selected_documents[view_name] = chosen
            views[view_name] = {"documents": len(chosen), "bytes": len(blob),
                                "sha256": digest,
                                "min_document_bytes": min(len(v.encode("utf-8")) for v in chosen),
                                "max_document_bytes": max(len(v.encode("utf-8")) for v in chosen)}

    train_all = set(documents_2049["train"])
    validation_all = set(documents_2049["validation"])
    overlap = len(train_all & validation_all)
    prompts = [turn["user"] for item in panel["items"] for turn in item["turns"]]
    contamination = sum(
        any(prompt.casefold() in document.casefold() for prompt in prompts)
        for documents in selected_documents.values() for document in documents)
    bars = protocol["context_census"]["bars"]
    gates = {
        "2049_target_coverage": census["2049"]["coverage"]
        >= bars["2049_target_coverage_min"],
        "canonical_alternation": invalid == bars["canonical_alternation_invalid"],
        "train_validation_exact_overlap": overlap
        == bars["train_validation_exact_overlap"],
        "panel_exact_contamination": contamination
        == bars["panel_exact_contamination"],
        "view_hashes": True,
    }
    output = Path(output)
    output.mkdir(parents=True, exist_ok=True)
    for name, documents in selected_documents.items():
        (output / f"{name}.txt").write_bytes(_view_bytes(documents))
    manifest = {
        "schema": "anima-303m-v1-context-data/v1",
        "protocol_sha256": _sha256_file(protocol_path),
        "panel_sha256": panel_sha,
        "source": source,
        "source_files": source_files,
        "census": census,
        "views": views,
        "integrity": {"canonical_alternation_invalid": invalid,
                      "train_validation_exact_overlap": overlap,
                      "panel_exact_contamination": contamination},
        "gates": gates,
        "verdict": "PASS" if all(gates.values()) else "FAIL",
    }
    (output / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (output / "README.md").write_text(
        "# Anima V1 context micro data\n\nPrivate immutable SHA-ordered views from the "
        "pinned Apache-2.0 OpenAssistant revision.\n", encoding="utf-8")
    (output / "LICENSES.md").write_text(
        "# Source licenses\n\n- OpenAssistant/oasst1: Apache-2.0.\n", encoding="utf-8")
    if manifest["verdict"] != "PASS":
        raise RuntimeError("V1 data gates failed")
    return manifest


def upload(output: str | Path, repo_id: str, token: str) -> str:
    from huggingface_hub import HfApi
    api = HfApi(token=token)
    api.create_repo(repo_id=repo_id, repo_type="dataset", private=True, exist_ok=True)
    commit = api.upload_folder(
        repo_id=repo_id, repo_type="dataset", folder_path=str(output),
        commit_message="Publish preregistered V1 context views")
    if not api.dataset_info(repo_id=repo_id, revision=commit.oid).private:
        raise RuntimeError("refusing public V1 dataset")
    return commit.oid


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--protocol", default=str(HERE / "protocol.json"))
    parser.add_argument("--output", required=True)
    parser.add_argument("--upload-repo", default="")
    args = parser.parse_args()
    token = os.environ.get("HF_TOKEN")
    manifest = build(args.protocol, args.output, token)
    result = {"verdict": manifest["verdict"], "gates": manifest["gates"]}
    if args.upload_repo:
        if not token:
            raise SystemExit("HF_TOKEN is required for upload")
        result["uploaded_revision"] = upload(args.output, args.upload_repo, token)
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
