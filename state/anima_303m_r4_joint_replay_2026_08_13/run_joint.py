#!/usr/bin/env python3
"""Run native two-cell joint broad replay and dialogue supervision."""

from __future__ import annotations

import argparse
import importlib.util
import json
import math
import os
from pathlib import Path
import subprocess
import sys


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
LOW_SCRIPT = ROOT / "state/anima_303m_r4_low_lr_sft_2026_08_13/run_low_lr.py"
SPEC = importlib.util.spec_from_file_location("r4_low_lr", LOW_SCRIPT)
low = importlib.util.module_from_spec(SPEC)
if SPEC.loader is None:
    raise RuntimeError("low-LR harness loader is missing")
SPEC.loader.exec_module(low)
curriculum, four, parent, diagnostics = low.curriculum, low.four, low.parent, low.diagnostics


def joint_command(output: Path, broad_train: Path, broad_validation: Path,
                  dialogue_train: Path, dialogue_validation: Path,
                  language_checkpoint: Path, device: str) -> list[str]:
    return [
        sys.executable, str(ROOT / "cli/train.py"), "--arch", "bytegpt", "--d", "128",
        "--L", "4", "--seq-len", "512", "--steps", "3750", "--batch-size", "8",
        "--device", device, "--seed", "7", "--corpus", str(broad_train), str(dialogue_train),
        "--validation-corpus", str(broad_validation), str(dialogue_validation),
        "--cell-label", "broad", "dialogue", "--require-cells", "2",
        "--sample", "roundrobin", "--chat-framed-sampling", "--chat-frame-alignment", "document",
        "--answer-ce-marker", four.generator.CHAT_ASSISTANT_PREFIX,
        "--answer-ce-weight", "1.0", "--answer-ce-all-spans", "--answer-ce-mode", "additive",
        "--lr", "0.001", "--adam-beta2", "0.95", "--weight-decay", "0.1",
        "--lr-schedule", "cosine", "--warmup-steps", "50", "--lr-decay-steps", "3750",
        "--min-lr-ratio", "0.1", "--val-every", "100", "--val-batches", "4",
        "--log-every", "100", "--init", str(language_checkpoint),
        "--out", str(output.with_suffix(".bin")), "--ckpt-out", str(output.with_suffix(".pt")),
        "--gauges-out", str(output.with_suffix(".summary.json")), "--skip-inline-rho",
        "--deterministic",
    ]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--language-checkpoint", required=True)
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
    source_protocol_path = (protocol_path.parent / protocol["source_protocol"]).resolve()
    if curriculum.sha256(parent_result) != protocol["parent_result_sha256"] or curriculum.sha256(source_protocol_path) != protocol["source_protocol_sha256"]:
        raise RuntimeError("registered parent identity differs")
    source = json.loads(source_protocol_path.read_text(encoding="utf-8"))
    language_checkpoint = Path(args.language_checkpoint)
    if curriculum.sha256(language_checkpoint) != protocol["language_checkpoint_sha256"]:
        raise RuntimeError("language checkpoint differs from preregistration")

    broad_spec = source["broad_data"]
    broad_source = Path(args.broad_source)
    if curriculum.sha256(broad_source) != broad_spec["file_sha256"]:
        raise RuntimeError("broad source identity differs")
    raw = broad_source.read_bytes()
    ts, te = broad_spec["train_range"]
    vs, ve = broad_spec["validation_range"]
    broad_train_bytes, broad_validation_bytes = raw[ts:te], raw[vs:ve]
    if curriculum.sha256_bytes(broad_train_bytes) != broad_spec["train_sha256"] or curriculum.sha256_bytes(broad_validation_bytes) != broad_spec["validation_sha256"]:
        raise RuntimeError("broad view differs")

    dialogue_spec = source["dialogue_data"]
    dialogue_dir = Path(args.dialogue_data)
    train_source = dialogue_dir / dialogue_spec["train_file"]
    validation_source = dialogue_dir / dialogue_spec["validation_file"]
    if curriculum.sha256(train_source) != dialogue_spec["train_file_sha256"] or curriculum.sha256(validation_source) != dialogue_spec["validation_file_sha256"]:
        raise RuntimeError("dialogue source identity differs")
    selected = []
    for document in parent._documents(train_source):
        exchange = parent._final_exchange(document)
        if exchange is not None and len(exchange[1].encode("utf-8", "surrogateescape")) <= four.generator.CHAT_MAX_NEW_BYTES:
            selected.append(document)
            if len(selected) == 100:
                break
    validation_documents = parent._documents(validation_source)[:32]
    dialogue_train_bytes = parent._view_bytes(selected)
    dialogue_validation_bytes = parent._view_bytes(validation_documents)
    if parent._sha256_bytes(dialogue_train_bytes) != dialogue_spec["hundred_document_view_sha256"] or parent._sha256_bytes(dialogue_validation_bytes) != dialogue_spec["heldout_32_view_sha256"]:
        raise RuntimeError("dialogue view differs")
    panel_path = (source_protocol_path.parent / dialogue_spec["panel"]).resolve()
    if curriculum.sha256(panel_path) != dialogue_spec["panel_sha256"]:
        raise RuntimeError("panel identity differs")

    work = Path(args.work); work.mkdir(parents=True, exist_ok=True)
    paths = {"bt": work / "broad.train.bin", "bv": work / "broad.validation.bin",
             "dt": work / "hundred.train.txt", "dv": work / "heldout32.validation.txt"}
    paths["bt"].write_bytes(broad_train_bytes); paths["bv"].write_bytes(broad_validation_bytes)
    paths["dt"].write_bytes(dialogue_train_bytes); paths["dv"].write_bytes(dialogue_validation_bytes)
    output = work / "joint_replay"
    summary = curriculum.run_train(
        joint_command(output, paths["bt"], paths["bv"], paths["dt"], paths["dv"],
                      language_checkpoint, args.device), output.with_suffix(".log"))
    checkpoint = output.with_suffix(".bin")
    broad_score = curriculum.fixed_byte_ce(checkpoint, broad_validation_bytes, args.device)
    panel = json.loads(panel_path.read_text(encoding="utf-8"))
    exchanges = [parent._final_exchange(document) for document in selected[:8]]
    training_probe = four._score_arm(checkpoint, exchanges, panel["bars"], args.device)
    model = diagnostics._load_engine_torch(checkpoint, args.device)
    validation_exchanges = [diagnostics.v1._exchange(document) for document in validation_documents]
    validation_rows = [diagnostics._teacher_trace_seed(model, seed, target, args.device)
                       for seed, target in validation_exchanges]
    dialogue_score = {"full": diagnostics._validation_full_ce(model, validation_documents, args.device),
                      "assistant_turn": diagnostics._aggregate_trace(validation_rows)}
    conversation_path = work / "conversation_result.json"
    completed = subprocess.run(
        [sys.executable, str(ROOT / "cli/evaluate.py"), str(checkpoint), "--conversation-panel",
         str(panel_path), "--conversation-panel-sha256", dialogue_spec["panel_sha256"],
         "--out", str(conversation_path)], cwd=ROOT,
        env={**os.environ, "OMP_NUM_THREADS": "2", "MKL_NUM_THREADS": "2"},
        text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=False)
    (work / "conversation.log").write_text(completed.stdout, encoding="utf-8")
    if not conversation_path.is_file():
        raise RuntimeError("conversation evaluator produced no result")
    conversation = json.loads(conversation_path.read_text(encoding="utf-8"))
    counts = training_probe["counts"]
    retention_gate = broad_score["ce"] < math.log(256.0)
    turn_gate = (training_probe["teacher"]["top1_accuracy"] >= 0.80 and counts["exact"] == 8
                 and counts["target_recovered"] == 8 and counts["structural"] == 8
                 and training_probe["prompt_causality"]["counts"]["ce_controlled"] >= 6)
    automatic = bool(retention_gate and turn_gate and conversation.get("pass"))
    decision = protocol["decision"]
    verdict = (decision["retention_failure"] if not retention_gate else
               decision["turn_failure"] if not turn_gate else
               decision["conversation_failure"] if not conversation.get("pass") else
               decision["automatic_pass"])
    result = {"schema": "anima-303m-r4-joint-replay-result/v1",
              "protocol_sha256": curriculum.sha256(protocol_path),
              "parent_result_sha256": curriculum.sha256(parent_result),
              "language_checkpoint_sha256": curriculum.sha256(language_checkpoint),
              "engine_sha256": curriculum.sha256(checkpoint), "device": args.device,
              "summary": summary, "broad_validation": broad_score,
              "retention_gate": retention_gate, "training_probe": training_probe,
              "turn_gate": turn_gate, "dialogue_validation": dialogue_score,
              "conversation_evaluator_exit": completed.returncode, "conversation": conversation,
              "gate": automatic, "verdict": verdict,
              "next_allowed_step": "No 303M, IIT-mouth, participant, or production action without automatic and manual conversation passes."}
    Path(args.result).write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
