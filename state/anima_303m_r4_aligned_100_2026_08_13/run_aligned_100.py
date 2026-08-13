#!/usr/bin/env python3
"""Run the preregistered aligned 100-document and conversation gate."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
FOUR_SCRIPT = ROOT / "state/anima_303m_r4_four_doc_2026_08_13/run_experiment.py"
SPEC = importlib.util.spec_from_file_location("r4_four_document", FOUR_SCRIPT)
four = importlib.util.module_from_spec(SPEC)
if SPEC.loader is None:
    raise RuntimeError("four-document harness loader is missing")
SPEC.loader.exec_module(four)
parent = four.parent
diagnostics = four.diagnostics


def _sha256(path: str | Path) -> str:
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", required=True)
    parser.add_argument("--work", required=True)
    parser.add_argument("--result", required=True)
    parser.add_argument("--protocol", default=str(HERE / "protocol.json"))
    parser.add_argument("--device", choices=["cpu"], default="cpu")
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

    documents = parent._documents(train_source)
    validation = parent._documents(validation_source)[:32]
    selected = []
    for document in documents:
        exchange = parent._final_exchange(document)
        if (exchange is not None
                and len(exchange[1].encode("utf-8", "surrogateescape"))
                <= four.generator.CHAT_MAX_NEW_BYTES):
            selected.append(document)
            if len(selected) == 100:
                break
    if len(selected) != 100:
        raise RuntimeError("source cannot provide 100 registered runtime-compatible documents")
    train_bytes = parent._view_bytes(selected)
    validation_bytes = parent._view_bytes(validation)
    if parent._sha256_bytes(train_bytes) != fixed_data["hundred_document_view_sha256"]:
        raise RuntimeError("100-document view differs from preregistration")
    if parent._sha256_bytes(validation_bytes) != fixed_data["heldout_32_view_sha256"]:
        raise RuntimeError("heldout view differs from preregistration")
    exchanges = [parent._final_exchange(document) for document in selected[:8]]
    if any(exchange is None for exchange in exchanges):
        raise RuntimeError("registered probe is not eight complete exchanges")

    work = Path(args.work)
    work.mkdir(parents=True, exist_ok=True)
    train_path = work / "hundred.train.txt"
    validation_path = work / "heldout32.validation.txt"
    train_path.write_bytes(train_bytes)
    validation_path.write_bytes(validation_bytes)
    fixed = protocol["fixed_recipe"]
    arm = {"d": fixed["d"], "layers": fixed["layers"], "steps": fixed["steps"],
           "checkpoint_every": 0}
    summary = four._train_arm(
        {"fixed_recipe": fixed}, "A100_document_alignment", arm,
        train_path, validation_path, work, args.device)
    checkpoint = work / "a100_document_alignment.bin"
    panel = json.loads(panel_path.read_text(encoding="utf-8"))
    typed_exchanges = [exchange for exchange in exchanges if exchange is not None]
    training_probe = four._score_arm(checkpoint, typed_exchanges, panel["bars"], args.device)

    model = diagnostics._load_engine_torch(checkpoint, args.device)
    validation_exchanges = [diagnostics.v1._exchange(document) for document in validation]
    validation_rows = [diagnostics._teacher_trace_seed(model, seed, target, args.device)
                       for seed, target in validation_exchanges]
    fixed_validation = {
        "full": diagnostics._validation_full_ce(model, validation, args.device),
        "assistant_turn": diagnostics._aggregate_trace(validation_rows),
    }

    conversation_path = work / "conversation_result.json"
    completed = subprocess.run(
        [sys.executable, str(ROOT / "cli/evaluate.py"), str(checkpoint),
         "--conversation-panel", str(panel_path),
         "--conversation-panel-sha256", fixed_data["panel_sha256"],
         "--out", str(conversation_path)], cwd=ROOT,
        env={**os.environ, "OMP_NUM_THREADS": "2", "MKL_NUM_THREADS": "2"},
        text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=False)
    (work / "conversation.log").write_text(completed.stdout, encoding="utf-8")
    if not conversation_path.is_file():
        raise RuntimeError("conversation evaluator did not produce its registered result")
    conversation = json.loads(conversation_path.read_text(encoding="utf-8"))
    counts = training_probe["counts"]
    training_gate = (
        training_probe["teacher"]["top1_accuracy"] >= 0.80
        and counts["exact"] == 8 and counts["target_recovered"] == 8
        and counts["structural"] == 8
        and training_probe["prompt_causality"]["counts"]["ce_controlled"] >= 6)
    automatic = bool(training_gate and conversation.get("pass"))
    result = {
        "schema": "anima-303m-r4-aligned-100-result/v1",
        "protocol_sha256": _sha256(protocol_path),
        "parent_result_sha256": _sha256(parent_result),
        "device": args.device,
        "engine_sha256": _sha256(checkpoint),
        "summary": summary,
        "training_probe": training_probe,
        "training_gate": training_gate,
        "fixed_validation": fixed_validation,
        "conversation_evaluator_exit": completed.returncode,
        "conversation": conversation,
        "gate": automatic,
        "verdict": ("AUTOMATIC-PASS-MANUAL-REVIEW-REQUIRED" if automatic
                    else "FAIL-ALIGNED-100-MEANINGFUL-CONVERSATION"),
        "next_allowed_step": (
            "Do not run 303M or couple IIT unless the fixed automatic and later manual gates pass."),
    }
    Path(args.result).write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
