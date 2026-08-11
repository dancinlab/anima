#!/usr/bin/env python3
"""Build the preregistered R0 conversation corpus from pinned HF revisions.

The builder is intentionally state-directory scoped: protocol.json is the SSOT,
while all model training consumes only the immutable HF revision it publishes.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import sqlite3
import unicodedata


HERE = Path(__file__).resolve().parent


def normalized_document(text: str) -> str:
    return re.sub(r"\s+", " ", unicodedata.normalize("NFC", str(text))).strip()


def document_hash(text: str) -> str:
    return hashlib.sha256(normalized_document(text).encode("utf-8")).hexdigest()


def file_sha256(path: str | Path) -> str:
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


class DocumentRegistry:
    """Disk-backed exact dedup with held-out validation winning ownership."""

    def __init__(self, path: str | Path):
        self.db = sqlite3.connect(path)
        self.db.execute("PRAGMA journal_mode=WAL")
        self.db.execute(
            "CREATE TABLE docs (hash TEXT PRIMARY KEY, label TEXT NOT NULL, "
            "split TEXT NOT NULL, text TEXT NOT NULL)")
        self.seen = 0
        self.empty = 0

    def add(self, label: str, split: str, text: str) -> None:
        if split not in {"train", "validation"}:
            raise ValueError(f"invalid split: {split}")
        value = normalized_document(text)
        if not value:
            self.empty += 1
            return
        self.seen += 1
        digest = document_hash(value)
        self.db.execute(
            "INSERT INTO docs(hash,label,split,text) VALUES(?,?,?,?) "
            "ON CONFLICT(hash) DO UPDATE SET label=excluded.label, "
            "split=excluded.split, text=excluded.text "
            "WHERE excluded.split='validation' AND docs.split='train'",
            (digest, label, split, value),
        )

    def commit(self) -> None:
        self.db.commit()

    def write_cells(self, output: str | Path, labels: list[str]) -> dict:
        output = Path(output)
        output.mkdir(parents=True, exist_ok=True)
        report = {}
        for label in labels:
            report[label] = {}
            for split in ("train", "validation"):
                path = output / f"{label}.{split}.txt"
                count = 0
                with open(path, "wb") as handle:
                    rows = self.db.execute(
                        "SELECT text FROM docs WHERE label=? AND split=? ORDER BY hash",
                        (label, split),
                    )
                    for (text,) in rows:
                        handle.write(text.encode("utf-8") + b"\n\n")
                        count += 1
                report[label][split] = {
                    "documents": count,
                    "bytes": path.stat().st_size,
                    "sha256": file_sha256(path),
                    "file": path.name,
                }
        return report

    def overlap(self) -> int:
        # A hash has one owner by schema; retain an explicit audited value in the manifest.
        return int(self.db.execute(
            "SELECT COUNT(*) FROM (SELECT hash FROM docs GROUP BY hash "
            "HAVING COUNT(DISTINCT split)>1)").fetchone()[0])

    def contamination(self, prompts: list[str]) -> list[dict]:
        found = []
        needles = [(document_hash(p), normalized_document(p)) for p in prompts]
        for digest, label, split, text in self.db.execute(
                "SELECT hash,label,split,text FROM docs"):
            for prompt_hash, prompt in needles:
                if digest == prompt_hash or prompt in text:
                    found.append({"document_sha256": digest, "prompt_sha256": prompt_hash,
                                  "label": label, "split": split})
        return found

    def remove_contamination(self, prompts: list[str]) -> list[dict]:
        found = self.contamination(prompts)
        hashes = sorted({row["document_sha256"] for row in found})
        self.db.executemany("DELETE FROM docs WHERE hash=?", ((digest,) for digest in hashes))
        self.db.commit()
        return found

    @staticmethod
    def _simhash64(text: str) -> int:
        value = normalized_document(text)
        grams = [value[i:i + 5] for i in range(max(1, len(value) - 4))][:256]
        scores = [0] * 64
        for gram in grams:
            bits = int.from_bytes(hashlib.blake2b(gram.encode("utf-8"), digest_size=8).digest(),
                                  "big")
            for bit in range(64):
                scores[bit] += 1 if bits & (1 << bit) else -1
        return sum((1 << bit) for bit, score in enumerate(scores) if score >= 0)

    def near_duplicate_audit(self, limit: int = 100_000, max_distance: int = 3) -> dict:
        buckets: dict[tuple[int, int], list[tuple[str, int]]] = {}
        near_pairs = 0
        candidate_pairs = 0
        examples = []
        sample_size = 0
        rows = self.db.execute(
            "SELECT hash,label,split,text FROM docs ORDER BY hash LIMIT ?", (limit,))
        for digest, label, split, text in rows:
            sample_size += 1
            fingerprint = self._simhash64(text)
            candidates: dict[str, int] = {}
            for band in range(4):
                key = (band, (fingerprint >> (band * 16)) & 0xFFFF)
                for other_digest, other_fingerprint in buckets.get(key, []):
                    candidates[other_digest] = other_fingerprint
            for other_digest, other_fingerprint in candidates.items():
                candidate_pairs += 1
                distance = (fingerprint ^ other_fingerprint).bit_count()
                if distance <= max_distance:
                    near_pairs += 1
                    if len(examples) < 20:
                        examples.append({"a_sha256": other_digest, "b_sha256": digest,
                                         "hamming_distance": distance,
                                         "b_label": label, "b_split": split})
            for band in range(4):
                key = (band, (fingerprint >> (band * 16)) & 0xFFFF)
                buckets.setdefault(key, []).append((digest, fingerprint))
        return {
            "policy": "report_only",
            "sample_size": sample_size,
            "sample_order": "lexicographically_smallest_sha256",
            "fingerprint": "simhash64_first_256_unicode_char_5grams",
            "candidate_index": "four_16bit_bands",
            "near_hamming_distance_max": max_distance,
            "candidate_pairs": candidate_pairs,
            "near_pairs": near_pairs,
            "examples": examples,
        }

    def close(self) -> None:
        self.db.close()


def _quality(row: dict) -> float:
    labels = row.get("labels") or {}
    names = labels.get("name") or []
    values = labels.get("value") or []
    try:
        return float(values[names.index("quality")])
    except (ValueError, IndexError, TypeError):
        return -1.0


def oasst_best_documents(rows: list[dict]) -> list[str]:
    eligible = {
        row["message_id"]: row for row in rows
        if row.get("lang") == "en"
        and row.get("review_result") is True
        and not row.get("deleted")
        and not row.get("synthetic")
        and row.get("role") in {"prompter", "assistant"}
        and normalized_document(row.get("text") or "")
    }
    children: dict[str, list[dict]] = {}
    roots = []
    for row in eligible.values():
        parent = row.get("parent_id")
        if parent is None:
            roots.append(row)
        elif parent in eligible:
            children.setdefault(parent, []).append(row)

    documents = []
    for root in sorted(roots, key=lambda row: row["message_id"]):
        path = [root]
        cursor = root
        while True:
            choices = [row for row in children.get(cursor["message_id"], [])
                       if row["role"] != cursor["role"]]
            if not choices:
                break
            cursor = min(
                choices,
                key=lambda row: (
                    row.get("rank") if row.get("rank") is not None else 2**31,
                    -_quality(row),
                    row["message_id"],
                ),
            )
            path.append(cursor)
        if len(path) >= 2 and path[0]["role"] == "prompter" and path[-1]["role"] == "assistant":
            turns = []
            for row in path:
                role = "user" if row["role"] == "prompter" else "assistant"
                turns.append(f"{role}: {normalized_document(row['text'])}")
            documents.append("\n".join(turns))
    return documents


def klue_documents(rows: list[dict]) -> list[str]:
    documents = []
    for row in rows:
        answers = (row.get("answers") or {}).get("text") or []
        if row.get("is_impossible") or not answers:
            continue
        question = normalized_document(row.get("question") or "")
        answer = normalized_document(answers[0])
        if question and answer:
            documents.append(f"user: {question}\nassistant: {answer}")
    return documents


def _source(protocol: dict, label: str) -> dict:
    return next(source for source in protocol["source_data"] if source["label"] == label)


def _download(source: dict, filename: str, token: str | None) -> str:
    from huggingface_hub import hf_hub_download
    return hf_hub_download(repo_id=source["repo"], revision=source["revision"],
                           filename=filename, repo_type="dataset", token=token)


def build(protocol_path: str | Path, panel_path: str | Path, output: str | Path,
          token: str | None) -> dict:
    import pyarrow.parquet as pq

    protocol = json.loads(Path(protocol_path).read_text(encoding="utf-8"))
    panel = json.loads(Path(panel_path).read_text(encoding="utf-8"))
    output = Path(output)
    output.mkdir(parents=True, exist_ok=True)
    db_path = output / ".documents.sqlite3"
    if db_path.exists():
        db_path.unlink()
    registry = DocumentRegistry(db_path)
    source_files = []
    try:
        for label in ("en_general", "ko_general"):
            source = _source(protocol, label)
            path = _download(source, source["file"], token)
            source_files.append({"label": label, "file": source["file"],
                                 "sha256": file_sha256(path)})
            with open(path, "r", encoding="utf-8", errors="strict") as handle:
                for line in handle:
                    text = normalized_document(line)
                    if text:
                        split = ("validation" if int(document_hash(text), 16) % 20 == 0
                                 else "train")
                        registry.add(label, split, text)
            registry.commit()

        source = _source(protocol, "en_dialogue")
        for filename, split in zip(source["files"], ("train", "validation")):
            path = _download(source, filename, token)
            source_files.append({"label": "en_dialogue", "file": filename,
                                 "sha256": file_sha256(path)})
            for text in oasst_best_documents(pq.read_table(path).to_pylist()):
                registry.add("en_dialogue", split, text)
            registry.commit()

        source = _source(protocol, "ko_dialogue")
        for filename, split in zip(source["files"], ("train", "validation")):
            path = _download(source, filename, token)
            source_files.append({"label": "ko_dialogue", "file": filename,
                                 "sha256": file_sha256(path)})
            for text in klue_documents(pq.read_table(path).to_pylist()):
                registry.add("ko_dialogue", split, text)
            registry.commit()

        prompts = []
        for item in panel["items"]:
            prompts.extend(turn["user"] for turn in item["turns"])
        removed_contamination = registry.remove_contamination(prompts)
        contamination = registry.contamination(prompts)
        near_duplicates = registry.near_duplicate_audit()
        cells = registry.write_cells(
            output, ["en_general", "ko_general", "en_dialogue", "ko_dialogue"])
        manifest = {
            "schema": "anima-303m-r0-conversation-data/v1",
            "protocol_sha256": file_sha256(protocol_path),
            "panel_sha256": file_sha256(panel_path),
            "dedup": {
                "candidates_seen": registry.seen,
                "empty_dropped": registry.empty,
                "validation_wins_duplicate_ownership": True,
                "cross_train_validation_hash_overlap": registry.overlap(),
            },
            "panel_decontamination": {
                "policy": "remove_before_training",
                "removed_documents": len({row["document_sha256"]
                                           for row in removed_contamination}),
                "removed_matches": removed_contamination,
                "remaining_matches": contamination,
            },
            "near_duplicate_audit": near_duplicates,
            "source_files": source_files,
            "cells": cells,
        }
        if manifest["dedup"]["cross_train_validation_hash_overlap"] != 0:
            raise RuntimeError("cross train/validation hash overlap is nonzero")
        if contamination:
            raise RuntimeError(f"registered conversation panel contamination: {contamination}")
        (output / "manifest.json").write_text(
            json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        (output / "LICENSES.md").write_text(
            "# Source licenses\n\n"
            "- OpenAssistant/oasst1: Apache-2.0.\n"
            "- klue/klue MRC: CC-BY-SA-4.0.\n"
            "- dancinlab general cells: provenance retained from their pinned private revisions.\n",
            encoding="utf-8",
        )
        return manifest
    finally:
        registry.close()
        if db_path.exists():
            db_path.unlink()


def upload(output: str | Path, repo_id: str, token: str) -> str:
    from huggingface_hub import HfApi

    api = HfApi(token=token)
    api.create_repo(repo_id=repo_id, repo_type="dataset", private=True, exist_ok=True)
    commit = api.upload_folder(repo_id=repo_id, repo_type="dataset", folder_path=str(output),
                               commit_message="Publish preregistered R0 conversation dataset")
    info = api.dataset_info(repo_id=repo_id, revision=commit.oid)
    if not info.private:
        raise RuntimeError("refusing public dataset result")
    return commit.oid


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--protocol", default=str(HERE / "protocol.json"))
    parser.add_argument("--panel", default=str(HERE / "conversation_panel.json"))
    parser.add_argument("--output", required=True)
    parser.add_argument("--upload", action="store_true")
    args = parser.parse_args()
    token = os.environ.get("HF_TOKEN")
    manifest = build(args.protocol, args.panel, args.output, token)
    print(json.dumps({"cells": manifest["cells"], "dedup": manifest["dedup"]}, indent=2))
    if args.upload:
        if not token:
            raise SystemExit("HF_TOKEN is required for upload")
        protocol = json.loads(Path(args.protocol).read_text(encoding="utf-8"))
        revision = upload(args.output, protocol["data_rules"]["output_repository"], token)
        print(json.dumps({"uploaded_revision": revision}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
