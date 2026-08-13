#!/usr/bin/env python3
"""Run the preregistered four-document ByteGPT optimization/capacity arms."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys

import torch


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
for path in (ROOT / "core", ROOT / "cli"):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

import generator
from core import serialize as serializer

DIAGNOSTIC_SCRIPT = (
    ROOT / "state/anima_303m_r4_mouth_diagnostics_2026_08_13/run_diagnostics.py")
SPEC = importlib.util.spec_from_file_location("r4_mouth_diagnostics", DIAGNOSTIC_SCRIPT)
diagnostics = importlib.util.module_from_spec(SPEC)
if SPEC.loader is None:
    raise RuntimeError("R4 diagnostic harness loader is missing")
SPEC.loader.exec_module(diagnostics)
parent = diagnostics.parent


def _sha256(path: str | Path) -> str:
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _checkpoint_path(base: Path, final_step: int, step: int) -> Path:
    if step == final_step:
        return base.with_suffix(".bin")
    return Path(str(base.with_suffix(".bin")) + f".step{step}.bin")


def _parameter_count(checkpoint: Path) -> int:
    state, _ = serializer.deserialize_bytegpt(str(checkpoint))
    return sum(int(value.numel()) for value in state.values())


def _train_arm(protocol: dict, arm_name: str, arm: dict, train_path: Path,
               validation_path: Path, work: Path, device: str) -> dict:
    fixed = protocol["fixed_recipe"]
    output = work / arm_name.lower()
    expected = [output.with_suffix(ext) for ext in (".bin", ".pt", ".summary.json", ".log")]
    if all(path.is_file() for path in expected):
        payload = torch.load(output.with_suffix(".pt"), map_location="cpu", weights_only=False)
        recipe = payload.get("recipe", {})
        answer = recipe.get("answer_ce") or {}
        valid = (
            payload.get("completed_step") == arm["steps"]
            and payload.get("endpoint_steps") == arm["steps"]
            and recipe.get("arch") == "bytegpt"
            and recipe.get("d") == arm["d"]
            and recipe.get("L") == arm["layers"]
            and recipe.get("seed") == fixed["seed"]
            and recipe.get("seq_len") == fixed["block"]
            and recipe.get("batch_size") == fixed["batch"]
            and recipe.get("corpus") == [str(train_path)]
            and recipe.get("validation_corpus") == [str(validation_path)]
            and answer.get("mode") == "turn-only"
            and recipe.get("chat_frame_alignment", "stream")
                == fixed.get("chat_frame_alignment", "stream"))
        if not valid:
            raise RuntimeError(f"completed {arm_name} artifacts differ from protocol")
        summary = json.loads(output.with_suffix(".summary.json").read_text(encoding="utf-8"))
        summary["reused_completed"] = True
        return summary

    command = [
        sys.executable, str(ROOT / "cli/train.py"),
        "--arch", "bytegpt", "--d", str(arm["d"]), "--L", str(arm["layers"]),
        "--seq-len", str(fixed["block"]), "--steps", str(arm["steps"]),
        "--batch-size", str(fixed["batch"]), "--device", device,
        "--seed", str(fixed["seed"]), "--corpus", str(train_path),
        "--validation-corpus", str(validation_path),
        "--cell-label", "dialogue", "--require-cells", "1", "--sample", "proportional",
        "--chat-framed-sampling", "--answer-ce-marker", generator.CHAT_ASSISTANT_PREFIX,
        "--answer-ce-weight", "1.0", "--answer-ce-all-spans",
        "--answer-ce-mode", "turn-only",
        "--lr", str(fixed["peak_lr"]), "--adam-beta2", "0.95", "--weight-decay", "0.1",
        "--lr-schedule", "cosine", "--warmup-steps", "50",
        "--lr-decay-steps", str(arm["steps"]), "--min-lr-ratio", "0.1",
        "--val-every", "100", "--val-batches", "4", "--log-every", "100",
        "--out", str(output.with_suffix(".bin")),
        "--ckpt-out", str(output.with_suffix(".pt")),
        "--gauges-out", str(output.with_suffix(".summary.json")),
        "--skip-inline-rho",
    ]
    if fixed.get("deterministic", False):
        command.append("--deterministic")
    if fixed.get("chat_frame_alignment", "stream") != "stream":
        command.extend(["--chat-frame-alignment", fixed["chat_frame_alignment"]])
    if arm["checkpoint_every"]:
        command.extend(["--ckpt-every", str(arm["checkpoint_every"])])
    completed = subprocess.run(
        command, cwd=ROOT,
        env={**os.environ, "OMP_NUM_THREADS": "2", "MKL_NUM_THREADS": "2"},
        text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=False)
    output.with_suffix(".log").write_text(completed.stdout, encoding="utf-8")
    if completed.returncode != 0:
        raise RuntimeError(
            f"{arm_name} training failed with {completed.returncode}\n{completed.stdout[-6000:]}")
    return json.loads(output.with_suffix(".summary.json").read_text(encoding="utf-8"))


def _score_arm(checkpoint: Path, exchanges: list[tuple[str, str]], bars: dict,
               device: str) -> dict:
    score = diagnostics._score_checkpoint(checkpoint, exchanges, bars, device)
    score["counts"]["exact"] = sum(
        row["free"]["decoded"].get("text", "").strip() == row["free"]["target"].strip()
        for row in score["rows"])
    # The shared D4 helper was frozen for eight probes and advances with modulo 8.
    # Repeat shorter registered cycles only enough to satisfy that contract.
    expected = min(8, len(exchanges))
    repeats = (8 + len(exchanges) - 1) // len(exchanges)
    prompt = diagnostics._prompt_intervention(
        checkpoint, (exchanges * repeats)[:8], bars, device)
    prompt["rows"] = prompt["rows"][:expected]
    prompt["counts"] = {
        "ce_controlled": sum(row["ce_controlled"] for row in prompt["rows"]),
        "output_controlled": sum(row["output_controlled"] for row in prompt["rows"]),
    }
    prompt["gate_all"] = (
        prompt["counts"]["ce_controlled"] == expected
        and prompt["counts"]["output_controlled"] == expected)
    prompt["gate_four"] = prompt["gate_all"] if expected == 4 else None
    score["prompt_causality"] = prompt
    counts = score["counts"]
    score["gate_reachability"] = _exact_gate_reachability(exchanges)
    score["memorization_gate"] = (
        score["gate_reachability"]["exact_completion_reachable"]
        and
        score["teacher"]["top1_accuracy"] >= 0.95
        and counts["exact"] == expected
        and counts["target_recovered"] == expected
        and counts["structural"] == expected)
    score["gate"] = score["memorization_gate"] and prompt["gate_all"]
    return score


def _classify(baseline_ok: bool, passes: dict[str, bool]) -> str:
    if not baseline_ok:
        return "INVALID-BASELINE-MISMATCH"
    optimization = passes.get("O1_horizon", False)
    capacity = passes.get("C1_width", False) or passes.get("C2_depth", False)
    if optimization and capacity:
        return "SUPPORTED-BOTH-HORIZON-AND-CAPACITY"
    if optimization:
        return "SUPPORTED-INSUFFICIENT-OPTIMIZATION-HORIZON"
    if capacity:
        return "SUPPORTED-TINY-CAPACITY-OR-GEOMETRY"
    if passes.get("B0_baseline", False):
        return "BASELINE-PASS-NO-TREATMENT-NEEDED"
    return "FALSIFIED-BOUNDED-HORIZON-AND-CAPACITY-TREATMENTS"


def _exact_gate_reachability(exchanges: list[tuple[str, str]]) -> dict:
    target_bytes = [len(target.encode("utf-8", "surrogateescape"))
                    for _, target in exchanges]
    return {
        "canonical_max_new_bytes": generator.CHAT_MAX_NEW_BYTES,
        "target_bytes": target_bytes,
        "exact_completion_reachable": all(
            size <= generator.CHAT_MAX_NEW_BYTES for size in target_bytes),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", required=True)
    parser.add_argument("--work", required=True)
    parser.add_argument("--result", required=True)
    parser.add_argument("--protocol", default=str(HERE / "protocol.json"))
    parser.add_argument("--device", choices=["mps", "cpu"], default="mps")
    args = parser.parse_args()

    protocol_path = Path(args.protocol).resolve()
    protocol_dir = protocol_path.parent
    protocol = json.loads(protocol_path.read_text(encoding="utf-8"))
    parent_result = (protocol_dir / protocol["parent_result"]).resolve()
    fixed_data = protocol["fixed_data"]
    panel_path = (protocol_dir / fixed_data["panel"]).resolve()
    if _sha256(parent_result) != protocol["parent_result_sha256"]:
        raise RuntimeError("parent result SHA differs from preregistration")
    if _sha256(panel_path) != fixed_data["panel_sha256"]:
        raise RuntimeError("conversation panel SHA differs from preregistration")

    data = Path(args.data)
    train_source = data / fixed_data["train_file"]
    validation_source = data / fixed_data["validation_file"]
    if _sha256(train_source) != fixed_data["train_file_sha256"]:
        raise RuntimeError("training source SHA differs from preregistration")
    if _sha256(validation_source) != fixed_data["validation_file_sha256"]:
        raise RuntimeError("validation source SHA differs from preregistration")
    train_documents = parent._documents(train_source)
    validation_documents = parent._documents(validation_source)
    four = train_documents[:4]
    val32 = validation_documents[:32]
    if parent._sha256_bytes(parent._view_bytes(four)) != fixed_data["four_document_view_sha256"]:
        raise RuntimeError("four-document view differs from preregistration")
    if parent._sha256_bytes(parent._view_bytes(val32)) != fixed_data["heldout_32_view_sha256"]:
        raise RuntimeError("heldout view differs from preregistration")
    exchanges = [parent._final_exchange(document) for document in four]
    if any(exchange is None for exchange in exchanges):
        raise RuntimeError("registered four-document view is not four complete exchanges")
    typed_exchanges = [exchange for exchange in exchanges if exchange is not None]

    work = Path(args.work)
    work.mkdir(parents=True, exist_ok=True)
    train_path = work / "four.train.txt"
    validation_path = work / "heldout32.validation.txt"
    train_path.write_bytes(parent._view_bytes(four))
    validation_path.write_bytes(parent._view_bytes(val32))
    panel = json.loads(panel_path.read_text(encoding="utf-8"))
    result = {
        "schema": "anima-303m-r4-four-document-result/v1",
        "protocol_sha256": _sha256(protocol_path),
        "parent_result_sha256": _sha256(parent_result),
        "data_sha256": {
            "train_source": _sha256(train_source),
            "validation_source": _sha256(validation_source),
            "four_document_view": _sha256(train_path),
            "heldout_32_view": _sha256(validation_path),
        },
        "device": args.device,
        "arms": {},
    }
    for name, arm in protocol["arms"].items():
        summary = _train_arm(protocol, name, arm, train_path, validation_path, work, args.device)
        checkpoint = work / f"{name.lower()}.bin"
        score = _score_arm(checkpoint, typed_exchanges, panel["bars"], args.device)
        chronology = {}
        if arm["checkpoint_every"]:
            for step in range(arm["checkpoint_every"], arm["steps"] + 1,
                              arm["checkpoint_every"]):
                chronology[str(step)] = _score_arm(
                    _checkpoint_path(work / name.lower(), arm["steps"], step),
                    typed_exchanges, panel["bars"], args.device)
        result["arms"][name] = {
            "registered": arm,
            "parameters": _parameter_count(checkpoint),
            "summary": summary,
            "score": score,
            "chronology": chronology,
        }

    baseline = result["arms"]["B0_baseline"]["score"]
    expected = protocol["gates"].get("baseline_expected", {
        "teacher_top1": 0.6977964323, "tolerance": 0.002,
        "target_prefix": 2, "structural": 1})
    baseline_ok = (
        abs(baseline["teacher"]["top1_accuracy"] - expected["teacher_top1"])
        <= expected["tolerance"]
        and baseline["counts"]["target_recovered"] == expected["target_prefix"]
        and baseline["counts"]["structural"] == expected["structural"])
    passes = {name: value["score"]["gate"] for name, value in result["arms"].items()}
    result["baseline_reproduction_gate"] = baseline_ok
    result["arm_gates"] = passes
    result["verdict"] = _classify(baseline_ok, passes)
    result["next_allowed_step"] = (
        "Interpret only the preregistered decision table. This diagnostic does not authorize "
        "303M training, IIT coupling, participant mounting or production.")
    Path(args.result).write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return 0 if baseline_ok else 4


if __name__ == "__main__":
    raise SystemExit(main())
