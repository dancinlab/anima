"""Deterministic, source-derived workspace curriculum with a sealed held-out split."""

from __future__ import annotations

import hashlib
import json
import os
import re


def _norm(text):
    return re.sub(r"\s+", " ", text.strip())


def _hash(text):
    return hashlib.sha256(text.encode("utf-8", "surrogatepass")).hexdigest()


def _records(line):
    words = line.split()
    cut = max(2, min(len(words) - 2, len(words) // 2))
    left, right = " ".join(words[:cut]), " ".join(words[cut:])
    key = _hash(line)[:12]
    return [
        (f"FACT {key} relation contains VALUE {left}\n"
         f"QUERY {key} relation => {left}"),
        (f"FACT {key} relation contains VALUE {left}\n"
         f"QUERY {key} shuffled_relation => UNGROUNDED"),
        (f"PREMISE A {left} ; PREMISE B {right}\n"
         f"PAIR A->B ; ORDER A,B\nCONCLUSION {line}"),
        (f"OBSERVATION {line}\nHYPOTHESIS {key} MEASURE occurrence CONTROL shuffled "
         "COMPARATOR increase FALSIFIER no-change EVIDENCE required STATUS grounded"),
    ]


def build_workspace_curriculum(paths, out_path, heldout_frac=0.2, seed=7):
    if not 0.0 < heldout_frac < 1.0:
        raise ValueError("heldout_frac must be between 0 and 1")
    unique = {}
    for path in paths:
        with open(path, "r", encoding="utf-8", errors="surrogateescape") as src:
            for raw in src:
                line = _norm(raw)
                if len(line.split()) >= 6:
                    unique.setdefault(_hash(line), line)
    if len(unique) < 2:
        raise ValueError("workspace curriculum needs at least two distinct six-word source lines")

    split = {"train": [], "heldout": []}
    source_hashes = {"train": [], "heldout": []}
    for digest, line in sorted(unique.items()):
        bucket = int(_hash(f"{seed}:{digest}")[:16], 16) / float(16 ** 16)
        name = "heldout" if bucket < heldout_frac else "train"
        source_hashes[name].append(digest)
        split[name].extend(_records(line))
    if not split["train"] or not split["heldout"]:
        raise ValueError("deterministic split produced an empty arm; add source lines or change seed")

    heldout_path = out_path + ".heldout.txt"
    manifest_path = out_path + ".workspace.json"
    for name, path in (("train", out_path), ("heldout", heldout_path)):
        with open(path, "w", encoding="utf-8") as dst:
            dst.write("\n\n".join(split[name]) + "\n")
    record_hashes = {k: sorted(_hash(_norm(v)) for v in vals) for k, vals in split.items()}
    overlap = set(record_hashes["train"]) & set(record_hashes["heldout"])
    source_overlap = set(source_hashes["train"]) & set(source_hashes["heldout"])
    manifest = {
        "schema": "anima.workspace-curriculum.v1",
        "seed": seed,
        "heldout_frac": heldout_frac,
        "sources": [os.path.abspath(p) for p in paths],
        "source_lines": {k: len(v) for k, v in source_hashes.items()},
        "records": {k: len(v) for k, v in record_hashes.items()},
        "source_sha256": source_hashes,
        "record_sha256": record_hashes,
        "source_overlap": len(source_overlap),
        "record_overlap": len(overlap),
        "leakage_free": not source_overlap and not overlap,
        "heldout_path": os.path.abspath(heldout_path),
    }
    with open(manifest_path, "w", encoding="utf-8") as dst:
        json.dump(manifest, dst, ensure_ascii=False, indent=2, sort_keys=True)
        dst.write("\n")
    return manifest, manifest_path
