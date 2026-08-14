#!/usr/bin/env python3
"""Build deterministic R3.7 English event data outside the Git worktree."""

import argparse
import hashlib
import json
import os
from pathlib import Path
import sys


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / "core"))

import iit_daemon as ID


DATASET_SCHEMA = "anima-iit-daemon-r37-sequence-dataset/1"
LICENSE = "CC0-1.0"


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":")).encode("utf-8")


def digest_bytes(value):
    return hashlib.sha256(value).hexdigest()


def digest_file(path):
    sha = hashlib.sha256()
    with open(path, "rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            sha.update(block)
    return sha.hexdigest()


def read_json(path):
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def row(text, labels):
    return ID._semantic_bridge_example({"text": text, "labels": labels})


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--out-dir", required=True)
    args = parser.parse_args(argv)
    output = Path(args.out_dir).resolve()
    output.mkdir(parents=True, exist_ok=False)

    r36_dir = ROOT / "state" / "iit_daemon_r36_semantic_bridge_2026_08_15"
    r35_dir = ROOT / "state" / "iit_daemon_r35_workspace_2026_08_14"
    exhaustion_dir = ROOT / "state" / "iit_daemon_r36_encoder_exhaustion_2026_08_15"
    contrastive_dir = ROOT / "state" / "iit_daemon_r36_contrastive_support_2026_08_15"
    r36_panel_path = r36_dir / "panel.json"
    r35_panel_path = r35_dir / "panel.json"
    exhaustion_protocol_path = exhaustion_dir / "protocol.json"
    contrastive_protocol_path = contrastive_dir / "protocol.json"
    sequence_panel_path = HERE / "sequence_panel.json"

    r36_panel = read_json(r36_panel_path)
    r35_panel = read_json(r35_panel_path)
    fixture = ID.semantic_bridge_micro_fixture(r36_panel, r35_panel)
    stress = [row(item["text"], item["labels"])
              for item in read_json(exhaustion_protocol_path)["stress"]]
    confirmation = [row(item["text"], item["labels"])
                    for item in read_json(contrastive_protocol_path)["confirmation"]]
    sequence_rows = [row(item["text"], item["labels"])
                     for item in read_json(sequence_panel_path)["rows"]]
    forbidden = {item["text"] for item in fixture["frozen"] + stress +
                 confirmation + sequence_rows}

    addresses = fixture["addresses"]
    original_entities = fixture["entities"]
    original_values = fixture["values"]
    entities = original_entities + ["garen", "hali", "iona", "jora"]
    values = original_values + ["linen", "quartz", "silver"]
    relation_surfaces = {
        "carries": ["carries", "is carrying", "holds", "bears", "transports"],
        "guards": ["guards", "is guarding", "protects", "defends", "watches over"],
        "observes": ["observes", "is observing", "watches", "sees", "monitors"],
    }
    heldout = set()
    for trial in r35_panel["trials"]:
        records = ID.validate_content_records(trial["records"], addresses)
        selected = records[trial["active_address"]]
        counterfactual = dict(selected, value=trial["counterfactual_value"])
        irrelevant = ID.validate_content_records(
            {trial["irrelevant_address"]: trial["irrelevant_record"]})[
                trial["irrelevant_address"]]
        for record in list(records.values()) + [counterfactual, irrelevant]:
            heldout.add(tuple(record[field] for field in ID.CONTENT_RECORD_FIELDS))

    memory_templates = [
        "Store under {address}: {entity} {surface} {value}.",
        "Place this fact in {address}: {entity} {surface} {value}.",
        "Archive for {address} the statement {entity} {surface} {value}.",
        "Keep at {address} the record that {entity} {surface} {value}.",
        "Preserve this observation under {address}: {entity} {surface} {value}.",
        "Commit to {address} the entry {entity} {surface} {value}.",
    ]
    query_templates = [
        "Fetch the saved fact from {address}.",
        "Tell me what is stored under {address}.",
        "Show the current record for {address}.",
        "Report what {address} contains.",
        "Recover the saved entry from {address}.",
        "Bring back the fact at {address}.",
        "Access {address} and return the record.",
        "Give me the observation kept in {address}.",
        "What content is assigned to {address}?",
        "Which entry belongs to {address}?",
        "Read and report {address}.",
        "Please fetch {address} now.",
    ]
    negative_query_templates = [
        "Do not fetch the saved fact from {address}.",
        "Never tell me what is stored under {address}.",
        "Leave {address} untouched; do not report it.",
        "Only mention the word {address}, without reading memory.",
        "The phrase fetch {address} is quoted, not requested.",
        "Nothing in {address} should be returned or changed.",
    ]
    negative_memory_templates = [
        "Do not store under {address}: {entity} {surface} {value}.",
        "Never archive for {address} the statement {entity} {surface} {value}.",
        "Leave {address} untouched although {entity} {surface} {value} is mentioned.",
    ]
    reversed_templates = [
        "{value} {surface} {entity} beside {address}, but no memory action occurs.",
        "At {address}, the words {value} {surface} {entity} are only discussed.",
    ]

    examples = list(fixture["training"])
    for address in addresses:
        for entity in entities:
            for relation in sorted(relation_surfaces):
                for value in values:
                    key = (entity, relation, value)
                    if entity in original_entities and value in original_values and key in heldout:
                        continue
                    surface_options = relation_surfaces[relation]
                    selector = sum(map(ord, address + entity + relation + value))
                    for index, template in enumerate(memory_templates):
                        surface = surface_options[(selector + index) % len(surface_options)]
                        examples.append(row(template.format(
                            address=address, entity=entity, surface=surface, value=value),
                            {"kind": "memory", "address": address, "entity": entity,
                             "relation": relation, "value": value}))
                    surface = surface_options[selector % len(surface_options)]
                    for template in negative_memory_templates:
                        examples.append(row(template.format(
                            address=address, entity=entity, surface=surface, value=value),
                            {"kind": "other"}))
                    for template in reversed_templates:
                        examples.append(row(template.format(
                            address=address, entity=entity, surface=surface, value=value),
                            {"kind": "other"}))
        for template in query_templates:
            examples.append(row(template.format(address=address),
                                {"kind": "query", "address": address}))
        for template in negative_query_templates:
            examples.append(row(template.format(address=address), {"kind": "other"}))

    neutral = [
        "Continue the session without changing memory.",
        "The word archive describes a building, not a command.",
        "A report may discuss alpha without fetching it.",
        "An observer watches quietly while no record is stored.",
        "Only ordinary conversation occurs here.",
        "Never is a word in this sentence and nothing more.",
        "The current facts should remain untouched.",
        "Thank you for waiting.",
    ]
    examples.extend(row(text, {"kind": "other"}) for text in neutral)

    unique = {}
    for example in examples:
        text = example["text"]
        if text in forbidden:
            raise ValueError("evaluation text leaked into source data: " + text)
        prior = unique.get(text)
        if prior is not None and prior != example:
            raise ValueError("one text has conflicting labels: " + text)
        unique[text] = example
    examples = [unique[text] for text in sorted(unique)]

    train = []
    validation = []
    for example in examples:
        bucket = int(hashlib.sha256(example["text"].encode("utf-8")).hexdigest()[:8], 16) % 10
        (validation if bucket == 0 else train).append(example)
    if not train or not validation or {item["text"] for item in train} & \
            {item["text"] for item in validation}:
        raise ValueError("invalid deterministic split")

    for name, rows in (("train", train), ("validation", validation)):
        path = output / (name + ".jsonl")
        with open(path, "wb") as handle:
            for example in rows:
                handle.write(canonical(example) + b"\n")

    train_records = {
        tuple(item["labels"].get(field) for field in ID.CONTENT_RECORD_FIELDS)
        for item in train if item["labels"]["kind"] == "memory"
    }
    if heldout & train_records:
        raise ValueError("R3.5 held-out complete record leaked into train")
    frozen_atoms = {
        "entity": set(original_entities), "relation": set(relation_surfaces),
        "value": set(original_values), "address": set(addresses),
    }
    for field, expected in frozen_atoms.items():
        actual = {item["labels"][field] for item in train if field in item["labels"]}
        if not expected <= actual:
            raise ValueError("frozen atom support is incomplete: " + field)

    manifest = {
        "schema": DATASET_SCHEMA,
        "license": LICENSE,
        "language": "en",
        "provenance": "repository-authored deterministic bounded English event grammar",
        "generator": "state/iit_daemon_r37_sequence_bridge_2026_08_15/build_dataset.py",
        "inputs": {
            "r36_panel_sha256": digest_file(r36_panel_path),
            "r35_panel_sha256": digest_file(r35_panel_path),
            "r36_exhaustion_protocol_sha256": digest_file(exhaustion_protocol_path),
            "r36_contrastive_protocol_sha256": digest_file(contrastive_protocol_path),
            "sequence_panel_sha256": digest_file(sequence_panel_path),
        },
        "counts": {"train": len(train), "validation": len(validation),
                   "forbidden_evaluation": len(forbidden),
                   "heldout_complete_records": len(heldout)},
        "files": {},
        "checks": {
            "train_validation_disjoint": True,
            "evaluation_text_disjoint": True,
            "heldout_complete_records_excluded": True,
            "frozen_atoms_supported": True,
        },
    }
    for filename in ("train.jsonl", "validation.jsonl"):
        path = output / filename
        manifest["files"][filename] = {"bytes": path.stat().st_size,
                                       "sha256": digest_file(path)}
    manifest["dataset_sha256"] = digest_bytes(canonical({
        "train": train, "validation": validation,
    }))
    with open(output / "manifest.json", "wb") as handle:
        handle.write(json.dumps(manifest, ensure_ascii=False, sort_keys=True,
                                indent=2).encode("utf-8") + b"\n")
    with open(output / "README.md", "w", encoding="utf-8") as handle:
        handle.write("---\nlicense: cc0-1.0\nlanguage: [en]\ntags: "
                     "[anima, iit, semantic-bridge, sequence, microexperiment]\n---\n\n"
                     "# anima IIT daemon R3.7 sequence-semantic data\n\n"
                     "Deterministic bounded English microdata generated by the pinned anima "
                     "R3.7 builder. It is not an open-domain conversation corpus. See "
                     "`manifest.json` for provenance, exclusions, counts and SHA-256 custody.\n")
    print(json.dumps(manifest, ensure_ascii=False, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
