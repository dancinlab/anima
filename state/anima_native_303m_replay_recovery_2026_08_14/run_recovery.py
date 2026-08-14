#!/usr/bin/env python3
"""Preflight, invoke and rescore the preregistered native-303M replay arm."""

from __future__ import annotations

import argparse
import copy
import hashlib
import importlib
import json
from pathlib import Path
import subprocess
import sys


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_protocol(path: Path = HERE / "protocol.json") -> dict:
    protocol = json.loads(path.read_text(encoding="utf-8"))
    if protocol.get("schema") != "anima-native-303m-replay-recovery/v1":
        raise ValueError("unsupported replay recovery protocol")
    return protocol


def apply_instrument(protocol: dict) -> dict:
    spec = protocol["conversation_instrument"]
    panel_path = (HERE / spec["base_panel"]).resolve()
    if sha256(panel_path) != spec["base_panel_sha256"]:
        raise ValueError("conversation base panel differs from preregistration")
    panel = json.loads(panel_path.read_text(encoding="utf-8"))
    panel = copy.deepcopy(panel)
    by_id = {item["id"]: item for item in panel["items"]}
    for constraint in spec["turn_constraints"]:
        turn = by_id[constraint["item_id"]]["turns"][int(constraint["turn"])]
        turn["forbidden_terms"] = list(constraint["forbidden_terms"])
    panel["scorer_controls"].extend(copy.deepcopy(spec["additional_controls"]))
    return panel


def rescore_native(native_result: dict, protocol: dict) -> dict:
    from cli.evaluate import (
        _conversation_jaccard,
        conversation_scorer_controls,
        score_conversation_response,
    )

    panel = apply_instrument(protocol)
    controls = conversation_scorer_controls(panel)
    if not controls["pass"]:
        return {"status": "INVALID_SCORER", "pass": False, "scorer_controls": controls}
    panel_items = {item["id"]: item for item in panel["items"]}
    responses = []
    for native_item in native_result.get("rows", []):
        item = panel_items[native_item["id"]]
        if len(native_item.get("turns", [])) != len(item["turns"]):
            raise ValueError("native result turn count differs from the pinned panel")
        for index, native_turn in enumerate(native_item["turns"]):
            turn = item["turns"][index]
            response = str(native_turn.get("response", ""))
            score = score_conversation_response(
                turn["user"], response, turn, item["lang"], panel["bars"],
                stopped=False, raw_text=response,
            )
            responses.append({
                "item_id": item["id"], "turn": index, "lang": item["lang"],
                "prompt": turn["user"], "response": response,
                "multiturn_final": bool(turn.get("multiturn_final")), "score": score,
            })
    duplicate_pairs = []
    for left_index, left in enumerate(responses):
        for right in responses[left_index + 1:]:
            if left["item_id"] == right["item_id"]:
                continue
            value = _conversation_jaccard(left["response"], right["response"])
            if value > float(panel["bars"]["max_cross_response_jaccard"]):
                duplicate_pairs.append({"a": left["item_id"], "b": right["item_id"],
                                        "jaccard": value})
    by_lang = {}
    for lang in sorted({row["lang"] for row in responses}):
        rows = [row for row in responses if row["lang"] == lang]
        by_lang[lang] = {
            "responses": len(rows),
            "structural_passes": sum(row["score"]["structural_pass"] for row in rows),
            "semantic_passes": sum(row["score"]["semantic_pass"] for row in rows),
        }
    bars = panel["bars"]
    automatic = (
        not duplicate_pairs
        and all(row["score"]["structural_pass"] for row in responses)
        and all(not row["multiturn_final"] or row["score"]["pass"] for row in responses)
        and all(row["semantic_passes"] >= int(bars["min_semantic_passes_per_language"])
                for row in by_lang.values())
    )
    return {
        "status": "COMPLETE", "pass": bool(automatic), "scorer_controls": controls,
        "by_language": by_lang, "duplicate_pairs": duplicate_pairs, "responses": responses,
    }


def training_command(protocol: dict, model_root: Path, data_root: Path,
                     output: Path, python: str = sys.executable) -> list[str]:
    recipe = protocol["fixed_recipe"]
    root_manifest = json.loads((data_root / "manifest.json").read_text(encoding="utf-8"))
    target_root = data_root / "data-conversation-target"
    target_manifest = json.loads((target_root / "manifest.json").read_text(encoding="utf-8"))
    command = [
        python, str(model_root / "code/train_native_dialogue_lm.py"),
        "--output-dir", str(output), "--preset", recipe["preset"],
        "--steps", str(recipe["endpoint_step"]),
        "--batch-size", str(recipe["batch_size"]),
        "--grad-accum", str(recipe["gradient_accumulation"]),
        "--lr", str(recipe["learning_rate"]), "--save-every", "1000",
        "--log-every", "50", "--validation-batches", "8", "--device", "cuda",
        "--weights", str(model_root / protocol["parent"]["base_checkpoint"]),
        "--response-only", "--reset-schedule",
    ]
    for name in root_manifest["splits"]["train_general"]:
        command.extend(("--train-general", str(data_root / name)))
    for name in root_manifest["splits"]["validation_general"]:
        command.extend(("--validation-general", str(data_root / name)))
    for name in target_manifest["splits"]["train_dialogue"]:
        command.extend(("--train-dialogue", str(target_root / name)))
    for name in target_manifest["splits"]["validation_dialogue"]:
        command.extend(("--validation-dialogue", str(target_root / name)))
    if "--dialogue-only" in command:
        raise AssertionError("registered recovery must use mixed source mode")
    return command


def resource_safe_training_command(protocol: dict, command: list[str]) -> list[str]:
    """Bound preprocessing parallelism without changing pinned training code."""
    if len(command) < 2:
        raise ValueError("native training command is incomplete")
    workers = int(protocol["fixed_recipe"]["preprocessing_workers"])
    if workers <= 0:
        raise ValueError("preprocessing workers must be positive")
    return [
        command[0], str(HERE / "run_pinned_trainer.py"),
        "--workers", str(workers), "--", *command[1:],
    ]


def manifest_output_checks(manifest_path: Path, data_root: Path,
                           splits: tuple[str, ...], prefix: str = "") -> dict:
    """Verify every consumed generated corpus file against its pinned manifest."""
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    outputs = manifest.get("outputs", {})
    checks = {}
    declared = []
    for split in splits:
        declared.extend(manifest.get("splits", {}).get(split, []))
    if len(declared) != len(set(declared)):
        raise ValueError(f"duplicate corpus path in {manifest_path}")
    for relative in declared:
        expected = outputs.get(relative)
        if not isinstance(expected, dict) or "size" not in expected or "sha256" not in expected:
            raise ValueError(f"missing output custody for {relative} in {manifest_path}")
        path = data_root / relative
        actual_size = path.stat().st_size
        actual_sha = sha256(path)
        checks[f"data/{prefix}{relative}"] = {
            "expected_size": int(expected["size"]),
            "actual_size": actual_size,
            "expected_sha256": str(expected["sha256"]),
            "actual_sha256": actual_sha,
            "pass": actual_size == int(expected["size"]) and actual_sha == str(expected["sha256"]),
        }
    return checks


def preflight(protocol: dict, model_root: Path, data_root: Path) -> dict:
    checks = {}
    for relative, expected in protocol["source_hashes"].items():
        base = data_root if relative in {"manifest.json", "data-conversation-target/manifest.json"} else model_root
        actual = sha256(base / relative)
        checks[relative] = {"expected": expected, "actual": actual, "pass": actual == expected}
    parent = protocol["parent"]
    for label, relative, expected in (
        ("base_checkpoint", parent["base_checkpoint"], parent["base_checkpoint_sha256"]),
        ("tokenizer", "checkpoints/step-035000/tokenizer.json", parent["tokenizer_sha256"]),
    ):
        actual = sha256(model_root / relative)
        checks[label] = {"expected": expected, "actual": actual, "pass": actual == expected}
    checks.update(manifest_output_checks(
        data_root / "manifest.json", data_root,
        ("train_general", "validation_general"),
    ))
    target_root = data_root / "data-conversation-target"
    checks.update(manifest_output_checks(
        target_root / "manifest.json", target_root,
        ("train_dialogue", "validation_dialogue"), "data-conversation-target/",
    ))
    controls = conversation_scorer_controls_result(protocol)
    passed = all(value["pass"] for value in checks.values()) and controls["pass"]
    return {"pass": passed, "checks": checks, "scorer_controls": controls}


def conversation_scorer_controls_result(protocol: dict) -> dict:
    from cli.evaluate import conversation_scorer_controls
    return conversation_scorer_controls(apply_instrument(protocol))


def measure_broad_retention(protocol: dict, model_root: Path, data_root: Path,
                            checkpoint: Path, device: str) -> dict:
    """Replay the preregistered general-validation measurement on one checkpoint."""
    if not (checkpoint / "final.pt").is_file() or not (checkpoint / "tokenizer.json").is_file():
        raise FileNotFoundError(f"native checkpoint is incomplete under {checkpoint}")
    tokenizer_hash = sha256(checkpoint / "tokenizer.json")
    expected_tokenizer_hash = protocol["parent"]["tokenizer_sha256"]
    if tokenizer_hash != expected_tokenizer_hash:
        raise ValueError("retention checkpoint tokenizer differs from preregistration")

    code_root = (model_root / "code").resolve()
    sys.path.insert(0, str(code_root))
    native = importlib.import_module("native_dialogue_lm")
    trainer = importlib.import_module("train_native_dialogue_lm")
    registry = importlib.import_module("measurement.native_dialogue_registry")
    for loaded in (native, trainer, registry):
        loaded_path = Path(loaded.__file__).resolve()
        if not loaded_path.is_relative_to(code_root):
            raise ValueError(f"retention module resolved outside pinned model code: {loaded_path}")
    measurement = protocol["audit"]["broad_measurement"]
    manifest = json.loads((data_root / "manifest.json").read_text(encoding="utf-8"))
    validation_paths = [
        data_root / name for name in manifest["splits"]["validation_general"]
    ]
    if len(validation_paths) != int(measurement["validation_files"]):
        raise ValueError("general validation file count differs from preregistration")
    workers = int(protocol["fixed_recipe"]["preprocessing_workers"])
    validation_general = trainer.load_corpus_files(
        validation_paths, checkpoint / "tokenizer.json", trainer.load_general_tokens, workers
    )
    model, _tokenizer, payload = native.load_native_model(checkpoint, device=device)
    source = trainer.BatchSource(
        validation_general, [], int(payload["config"]["block_size"]),
        int(measurement["seed"]), 0.0,
    )
    value = float(trainer.validation_loss(
        model, source, int(measurement["batches"]), int(measurement["batch_size"]),
        next(model.parameters()).device, source_mode="mixed", response_only=False,
    ))
    threshold = float(protocol["gates"]["broad_retention_ce_max"])
    return {
        "schema": "anima-native-303m-broad-retention/v1",
        "checkpoint": str(checkpoint),
        "checkpoint_sha256": sha256(checkpoint / "final.pt"),
        "tokenizer_sha256": tokenizer_hash,
        "device": str(next(model.parameters()).device),
        "seed": int(measurement["seed"]),
        "batches": int(measurement["batches"]),
        "batch_size": int(measurement["batch_size"]),
        "validation_files": len(validation_paths),
        "ce": value,
        "threshold": threshold,
        "pass": value <= threshold,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model-root", type=Path)
    parser.add_argument("--data-root", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--native-result", type=Path)
    parser.add_argument("--rescore-out", type=Path)
    parser.add_argument("--retention-checkpoint", type=Path)
    parser.add_argument("--retention-out", type=Path)
    parser.add_argument("--device", default="cuda")
    parser.add_argument("--execute", action="store_true")
    args = parser.parse_args()
    protocol = load_protocol()
    if args.retention_checkpoint:
        if not args.model_root or not args.data_root:
            parser.error("model-root and data-root are required for retention measurement")
        source_check = preflight(protocol, args.model_root, args.data_root)
        if not source_check["pass"]:
            print(json.dumps(source_check, ensure_ascii=False, indent=2), flush=True)
            return 3
        result = measure_broad_retention(
            protocol, args.model_root, args.data_root, args.retention_checkpoint, args.device)
        payload = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
        if args.retention_out:
            args.retention_out.write_text(payload, encoding="utf-8")
        else:
            print(payload, end="")
        return 0
    if args.native_result:
        result = rescore_native(
            json.loads(args.native_result.read_text(encoding="utf-8")), protocol)
        payload = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
        if args.rescore_out:
            args.rescore_out.write_text(payload, encoding="utf-8")
        else:
            print(payload, end="")
        return 0 if result["status"] != "INVALID_SCORER" else 3
    if not args.model_root or not args.data_root or not args.output:
        parser.error("model-root, data-root and output are required for preflight/training")
    result = preflight(protocol, args.model_root, args.data_root)
    print(json.dumps(result, ensure_ascii=False, indent=2), flush=True)
    if not result["pass"]:
        return 3
    command = training_command(protocol, args.model_root, args.data_root, args.output)
    launch_command = resource_safe_training_command(protocol, command)
    print(json.dumps({"command": command, "launch_command": launch_command},
                     ensure_ascii=False), flush=True)
    if not args.execute:
        return 0
    completed = subprocess.run(launch_command, cwd=args.model_root / "code", check=False)
    return int(completed.returncode)


if __name__ == "__main__":
    raise SystemExit(main())
