#!/usr/bin/env python3
"""Run the preregistered full-CE to aligned turn-SFT curriculum."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import math
import os
from pathlib import Path
import subprocess
import sys


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
ALIGNED_SCRIPT = ROOT / "state/anima_303m_r4_aligned_100_2026_08_13/run_aligned_100.py"
SPEC = importlib.util.spec_from_file_location("r4_aligned_100", ALIGNED_SCRIPT)
aligned = importlib.util.module_from_spec(SPEC)
if SPEC.loader is None:
    raise RuntimeError("aligned 100-document harness loader is missing")
SPEC.loader.exec_module(aligned)
four = aligned.four
parent = aligned.parent
diagnostics = aligned.diagnostics


def sha256(path: str | Path) -> str:
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def run_train(command: list[str], log_path: Path) -> dict:
    completed = subprocess.run(
        command, cwd=ROOT, env={**os.environ, "OMP_NUM_THREADS": "2", "MKL_NUM_THREADS": "2"},
        text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=False)
    log_path.write_text(completed.stdout, encoding="utf-8")
    if completed.returncode != 0:
        raise RuntimeError(f"training failed with {completed.returncode}\n{completed.stdout[-6000:]}")
    return json.loads(log_path.with_suffix(".summary.json").read_text(encoding="utf-8"))


def fixed_byte_ce(checkpoint: Path, raw: bytes, device: str) -> dict:
    model = diagnostics._load_engine_torch(checkpoint, device)
    documents = [raw[offset:offset + model.block].decode("utf-8", "surrogateescape")
                 for offset in range(0, len(raw) - model.block + 1, model.block)]
    return diagnostics._validation_full_ce(model, documents, device)


def train_command(output: Path, train: Path, validation: Path, *, steps: int,
                  device: str, init: Path | None = None, dialogue: bool = False) -> list[str]:
    command = [
        sys.executable, str(ROOT / "cli/train.py"), "--arch", "bytegpt", "--d", "128",
        "--L", "4", "--seq-len", "512", "--steps", str(steps), "--batch-size", "8",
        "--device", device, "--seed", "7", "--corpus", str(train),
        "--validation-corpus", str(validation), "--cell-label", "dialogue" if dialogue else "broad",
        "--require-cells", "1", "--sample", "proportional", "--lr", "0.001",
        "--adam-beta2", "0.95", "--weight-decay", "0.1", "--lr-schedule", "cosine",
        "--warmup-steps", "50", "--lr-decay-steps", str(steps), "--min-lr-ratio", "0.1",
        "--val-every", "100", "--val-batches", "4", "--log-every", "100",
        "--out", str(output.with_suffix(".bin")), "--ckpt-out", str(output.with_suffix(".pt")),
        "--gauges-out", str(output.with_suffix(".summary.json")), "--skip-inline-rho",
        "--deterministic",
    ]
    if init is not None:
        command.extend(["--init", str(init)])
    if dialogue:
        command.extend([
            "--chat-framed-sampling", "--chat-frame-alignment", "document",
            "--answer-ce-marker", four.generator.CHAT_ASSISTANT_PREFIX,
            "--answer-ce-weight", "1.0", "--answer-ce-all-spans",
            "--answer-ce-mode", "turn-only",
        ])
    return command


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--broad-source", required=True)
    parser.add_argument("--dialogue-data", required=True)
    parser.add_argument("--work", required=True)
    parser.add_argument("--result", required=True)
    parser.add_argument("--protocol", default=str(HERE / "protocol.json"))
    parser.add_argument("--device", choices=["cpu"], default="cpu")
    args = parser.parse_args()
    protocol_path = Path(args.protocol).resolve()
    protocol = json.loads(protocol_path.read_text(encoding="utf-8"))
    parent_result = (protocol_path.parent / protocol["parent_result"]).resolve()
    if sha256(parent_result) != protocol["parent_result_sha256"]:
        raise RuntimeError("parent result SHA differs from preregistration")

    broad_spec = protocol["broad_data"]
    broad_source = Path(args.broad_source)
    if broad_source.stat().st_size != broad_spec["file_bytes"] or sha256(broad_source) != broad_spec["file_sha256"]:
        raise RuntimeError("broad source identity differs from preregistration")
    broad_raw = broad_source.read_bytes()
    train_start, train_end = broad_spec["train_range"]
    val_start, val_end = broad_spec["validation_range"]
    broad_train = broad_raw[train_start:train_end]
    broad_validation = broad_raw[val_start:val_end]
    if sha256_bytes(broad_train) != broad_spec["train_sha256"] or sha256_bytes(broad_validation) != broad_spec["validation_sha256"]:
        raise RuntimeError("broad derived view differs from preregistration")

    dialogue_spec = protocol["dialogue_data"]
    dialogue_dir = Path(args.dialogue_data)
    train_source = dialogue_dir / dialogue_spec["train_file"]
    validation_source = dialogue_dir / dialogue_spec["validation_file"]
    if sha256(train_source) != dialogue_spec["train_file_sha256"] or sha256(validation_source) != dialogue_spec["validation_file_sha256"]:
        raise RuntimeError("dialogue source identity differs from preregistration")
    panel_path = (protocol_path.parent / dialogue_spec["panel"]).resolve()
    if sha256(panel_path) != dialogue_spec["panel_sha256"]:
        raise RuntimeError("panel identity differs from preregistration")
    source_documents = parent._documents(train_source)
    selected = []
    for document in source_documents:
        exchange = parent._final_exchange(document)
        if exchange is not None and len(exchange[1].encode("utf-8", "surrogateescape")) <= four.generator.CHAT_MAX_NEW_BYTES:
            selected.append(document)
            if len(selected) == 100:
                break
    validation_documents = parent._documents(validation_source)[:32]
    train_bytes = parent._view_bytes(selected)
    validation_bytes = parent._view_bytes(validation_documents)
    if parent._sha256_bytes(train_bytes) != dialogue_spec["hundred_document_view_sha256"] or parent._sha256_bytes(validation_bytes) != dialogue_spec["heldout_32_view_sha256"]:
        raise RuntimeError("dialogue derived view differs from preregistration")

    work = Path(args.work)
    work.mkdir(parents=True, exist_ok=True)
    broad_train_path = work / "broad.train.bin"
    broad_validation_path = work / "broad.validation.bin"
    dialogue_train_path = work / "hundred.train.txt"
    dialogue_validation_path = work / "heldout32.validation.txt"
    broad_train_path.write_bytes(broad_train)
    broad_validation_path.write_bytes(broad_validation)
    dialogue_train_path.write_bytes(train_bytes)
    dialogue_validation_path.write_bytes(validation_bytes)

    language = work / "language_phase"
    language_summary = run_train(
        train_command(language, broad_train_path, broad_validation_path, steps=2000, device=args.device),
        language.with_suffix(".log"))
    language_fixed_validation = fixed_byte_ce(language.with_suffix(".bin"), broad_validation, args.device)

    turn = work / "turn_phase"
    turn_summary = run_train(
        train_command(turn, dialogue_train_path, dialogue_validation_path, steps=1875,
                      device=args.device, init=language.with_suffix(".bin"), dialogue=True),
        turn.with_suffix(".log"))
    post_turn_broad_validation = fixed_byte_ce(turn.with_suffix(".bin"), broad_validation, args.device)
    panel = json.loads(panel_path.read_text(encoding="utf-8"))
    exchanges = [parent._final_exchange(document) for document in selected[:8]]
    if any(exchange is None for exchange in exchanges):
        raise RuntimeError("registered training probe is incomplete")
    training_probe = four._score_arm(turn.with_suffix(".bin"), exchanges, panel["bars"], args.device)
    turn_model = diagnostics._load_engine_torch(turn.with_suffix(".bin"), args.device)
    validation_exchanges = [diagnostics.v1._exchange(document) for document in validation_documents]
    validation_rows = [diagnostics._teacher_trace_seed(turn_model, seed, target, args.device)
                       for seed, target in validation_exchanges]
    dialogue_validation = {"full": diagnostics._validation_full_ce(turn_model, validation_documents, args.device),
                           "assistant_turn": diagnostics._aggregate_trace(validation_rows)}
    conversation_path = work / "conversation_result.json"
    completed = subprocess.run(
        [sys.executable, str(ROOT / "cli/evaluate.py"), str(turn.with_suffix(".bin")),
         "--conversation-panel", str(panel_path), "--conversation-panel-sha256",
         dialogue_spec["panel_sha256"], "--out", str(conversation_path)],
        cwd=ROOT, env={**os.environ, "OMP_NUM_THREADS": "2", "MKL_NUM_THREADS": "2"},
        text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=False)
    (work / "conversation.log").write_text(completed.stdout, encoding="utf-8")
    if not conversation_path.is_file():
        raise RuntimeError("conversation evaluator did not produce its registered result")
    conversation = json.loads(conversation_path.read_text(encoding="utf-8"))

    counts = training_probe["counts"]
    language_gate = language_fixed_validation["ce"] < math.log(256.0)
    turn_gate = (training_probe["teacher"]["top1_accuracy"] >= 0.80 and counts["exact"] == 8
                 and counts["target_recovered"] == 8 and counts["structural"] == 8
                 and training_probe["prompt_causality"]["counts"]["ce_controlled"] >= 6)
    automatic = bool(language_gate and turn_gate and conversation.get("pass"))
    if not language_gate:
        verdict = protocol["decision"]["language_failure"]
    elif not turn_gate:
        verdict = protocol["decision"]["turn_failure"]
    elif not conversation.get("pass"):
        verdict = protocol["decision"]["conversation_failure"]
    else:
        verdict = protocol["decision"]["automatic_pass"]
    result = {
        "schema": "anima-303m-r4-full-ce-curriculum-result/v1",
        "protocol_sha256": sha256(protocol_path), "parent_result_sha256": sha256(parent_result),
        "device": args.device, "language_engine_sha256": sha256(language.with_suffix(".bin")),
        "turn_engine_sha256": sha256(turn.with_suffix(".bin")),
        "language_summary": language_summary, "language_fixed_validation": language_fixed_validation,
        "language_gate": language_gate, "turn_summary": turn_summary,
        "post_turn_broad_validation": post_turn_broad_validation,
        "training_probe": training_probe, "turn_gate": turn_gate,
        "dialogue_validation": dialogue_validation, "conversation_evaluator_exit": completed.returncode,
        "conversation": conversation, "gate": automatic, "verdict": verdict,
        "next_allowed_step": "No 303M, IIT-mouth, participant, or production action without automatic and manual conversation passes."
    }
    Path(args.result).write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
