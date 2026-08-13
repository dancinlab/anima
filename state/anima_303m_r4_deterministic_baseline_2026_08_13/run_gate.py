#!/usr/bin/env python3
"""Run two exact fresh-process deterministic four-document baselines."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import sys

import torch


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
FOUR_SCRIPT = ROOT / "state/anima_303m_r4_four_doc_2026_08_13/run_experiment.py"
SPEC = importlib.util.spec_from_file_location("r4_four_document", FOUR_SCRIPT)
four = importlib.util.module_from_spec(SPEC)
if SPEC.loader is None:
    raise RuntimeError("four-document harness loader is missing")
SPEC.loader.exec_module(four)
parent = four.parent


def _sha256(path: str | Path) -> str:
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _model_equal(left: Path, right: Path) -> dict:
    a = torch.load(left, map_location="cpu", weights_only=False)
    b = torch.load(right, map_location="cpu", weights_only=False)
    keys_equal = a["model"].keys() == b["model"].keys()
    tensor_equal = keys_equal and all(
        torch.equal(a["model"][name], b["model"][name]) for name in a["model"])
    maximum_error = (max(float((a["model"][name] - b["model"][name]).abs().max())
                         for name in a["model"]) if keys_equal else None)
    return {
        "keys_equal": keys_equal,
        "all_tensors_equal": tensor_equal,
        "maximum_absolute_error": maximum_error,
        "state_digest_a": a.get("state_digest"),
        "state_digest_b": b.get("state_digest"),
        "state_digest_equal": a.get("state_digest") == b.get("state_digest"),
        "deterministic_recipe_a": (a.get("recipe") or {}).get("deterministic"),
        "deterministic_recipe_b": (b.get("recipe") or {}).get("deterministic"),
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
        raise RuntimeError("panel SHA differs from preregistration")
    data = Path(args.data)
    train_source = data / fixed_data["train_file"]
    validation_source = data / fixed_data["validation_file"]
    if _sha256(train_source) != fixed_data["train_file_sha256"]:
        raise RuntimeError("training source SHA differs from preregistration")
    if _sha256(validation_source) != fixed_data["validation_file_sha256"]:
        raise RuntimeError("validation source SHA differs from preregistration")

    train_documents = parent._documents(train_source)
    validation_documents = parent._documents(validation_source)
    train_bytes = parent._view_bytes(train_documents[:4])
    validation_bytes = parent._view_bytes(validation_documents[:32])
    if parent._sha256_bytes(train_bytes) != fixed_data["four_document_view_sha256"]:
        raise RuntimeError("four-document view differs from preregistration")
    if parent._sha256_bytes(validation_bytes) != fixed_data["heldout_32_view_sha256"]:
        raise RuntimeError("heldout view differs from preregistration")
    exchanges = [parent._final_exchange(document) for document in train_documents[:4]]
    if any(exchange is None for exchange in exchanges):
        raise RuntimeError("registered view is not four complete exchanges")
    typed_exchanges = [exchange for exchange in exchanges if exchange is not None]

    work = Path(args.work)
    work.mkdir(parents=True, exist_ok=True)
    train_path = work / "four.train.txt"
    validation_path = work / "heldout32.validation.txt"
    train_path.write_bytes(train_bytes)
    validation_path.write_bytes(validation_bytes)
    fixed = protocol["fixed_recipe"]
    train_protocol = {
        "fixed_recipe": {
            "block": fixed["block"], "seed": fixed["seed"], "batch": fixed["batch"],
            "peak_lr": fixed["peak_lr"], "deterministic": True},
    }
    arm = {"d": fixed["d"], "layers": fixed["layers"], "steps": fixed["steps"],
           "checkpoint_every": 0}
    panel = json.loads(panel_path.read_text(encoding="utf-8"))
    runs = {}
    try:
        for name in protocol["runs"]:
            summary = four._train_arm(
                train_protocol, f"run_{name}", arm, train_path, validation_path,
                work, args.device)
            base = work / f"run_{name.lower()}"
            runs[name] = {
                "engine_sha256": _sha256(base.with_suffix(".bin")),
                "checkpoint_sha256": _sha256(base.with_suffix(".pt")),
                "summary": summary,
                "score": four._score_arm(
                    base.with_suffix(".bin"), typed_exchanges, panel["bars"], args.device),
            }
    except RuntimeError as error:
        result = {
            "schema": "anima-303m-r4-deterministic-baseline-result/v1",
            "protocol_sha256": _sha256(protocol_path),
            "verdict": "FAIL-DETERMINISTIC-UNSUPPORTED",
            "error": str(error),
        }
        Path(args.result).write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
        return 4

    tensors = _model_equal(work / "run_a.pt", work / "run_b.pt")
    score_equal = runs["A"]["score"] == runs["B"]["score"]
    engine_equal = runs["A"]["engine_sha256"] == runs["B"]["engine_sha256"]
    gate = (engine_equal and tensors["state_digest_equal"] and tensors["all_tensors_equal"]
            and tensors["deterministic_recipe_a"] is True
            and tensors["deterministic_recipe_b"] is True and score_equal)
    result = {
        "schema": "anima-303m-r4-deterministic-baseline-result/v1",
        "protocol_sha256": _sha256(protocol_path),
        "parent_result_sha256": _sha256(parent_result),
        "device": args.device,
        "runs": runs,
        "comparison": {
            "engine_sha256_equal": engine_equal,
            "score_equal": score_equal,
            "model": tensors,
        },
        "gate": gate,
        "verdict": ("SUPPORTED-DETERMINISTIC-TRAJECTORY" if gate
                    else "FAIL-DETERMINISTIC-TRAJECTORY-MISMATCH"),
        "next_allowed_step": (
            "A later separately preregistered treatment comparison may use this exact "
            "deterministic execution contract; 303M, IIT coupling and production remain blocked."),
    }
    Path(args.result).write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return 0 if gate else 4


if __name__ == "__main__":
    raise SystemExit(main())
