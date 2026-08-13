#!/usr/bin/env python3
"""Run the preregistered low-LR turn-SFT arm from the fixed language engine."""

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
CURRICULUM_SCRIPT = ROOT / "state/anima_303m_r4_full_ce_curriculum_2026_08_13/run_curriculum.py"
SPEC = importlib.util.spec_from_file_location("r4_curriculum", CURRICULUM_SCRIPT)
curriculum = importlib.util.module_from_spec(SPEC)
if SPEC.loader is None:
    raise RuntimeError("curriculum harness loader is missing")
SPEC.loader.exec_module(curriculum)
four = curriculum.four
parent = curriculum.parent
diagnostics = curriculum.diagnostics


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
    if curriculum.sha256(parent_result) != protocol["parent_result_sha256"]:
        raise RuntimeError("parent result SHA differs from preregistration")
    source_protocol_path = (protocol_path.parent / protocol["source_protocol"]).resolve()
    if curriculum.sha256(source_protocol_path) != protocol["source_protocol_sha256"]:
        raise RuntimeError("source protocol SHA differs from preregistration")
    source_protocol = json.loads(source_protocol_path.read_text(encoding="utf-8"))

    language_checkpoint = Path(args.language_checkpoint)
    if curriculum.sha256(language_checkpoint) != protocol["language_checkpoint_sha256"]:
        raise RuntimeError("language checkpoint differs from preregistration")
    broad_spec = source_protocol["broad_data"]
    broad_source = Path(args.broad_source)
    if broad_source.stat().st_size != broad_spec["file_bytes"] or curriculum.sha256(broad_source) != broad_spec["file_sha256"]:
        raise RuntimeError("broad source identity differs from preregistration")
    broad_raw = broad_source.read_bytes()
    val_start, val_end = broad_spec["validation_range"]
    broad_validation = broad_raw[val_start:val_end]
    if curriculum.sha256_bytes(broad_validation) != broad_spec["validation_sha256"]:
        raise RuntimeError("broad validation view differs from preregistration")

    dialogue_spec = source_protocol["dialogue_data"]
    dialogue_dir = Path(args.dialogue_data)
    train_source = dialogue_dir / dialogue_spec["train_file"]
    validation_source = dialogue_dir / dialogue_spec["validation_file"]
    if curriculum.sha256(train_source) != dialogue_spec["train_file_sha256"] or curriculum.sha256(validation_source) != dialogue_spec["validation_file_sha256"]:
        raise RuntimeError("dialogue source identity differs from preregistration")
    panel_path = (source_protocol_path.parent / dialogue_spec["panel"]).resolve()
    if curriculum.sha256(panel_path) != dialogue_spec["panel_sha256"]:
        raise RuntimeError("panel identity differs from preregistration")
    selected = []
    for document in parent._documents(train_source):
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
    train_path = work / "hundred.train.txt"
    validation_path = work / "heldout32.validation.txt"
    train_path.write_bytes(train_bytes)
    validation_path.write_bytes(validation_bytes)
    output = work / "low_lr_turn"
    summary = curriculum.run_train(
        curriculum.train_command(output, train_path, validation_path, steps=1875,
                                 device=args.device, init=language_checkpoint,
                                 dialogue=True, peak_lr=0.0001),
        output.with_suffix(".log"))
    checkpoint = output.with_suffix(".bin")
    broad_validation_score = curriculum.fixed_byte_ce(checkpoint, broad_validation, args.device)
    panel = json.loads(panel_path.read_text(encoding="utf-8"))
    exchanges = [parent._final_exchange(document) for document in selected[:8]]
    if any(exchange is None for exchange in exchanges):
        raise RuntimeError("registered training probe is incomplete")
    training_probe = four._score_arm(checkpoint, exchanges, panel["bars"], args.device)
    model = diagnostics._load_engine_torch(checkpoint, args.device)
    validation_exchanges = [diagnostics.v1._exchange(document) for document in validation_documents]
    validation_rows = [diagnostics._teacher_trace_seed(model, seed, target, args.device)
                       for seed, target in validation_exchanges]
    dialogue_validation = {"full": diagnostics._validation_full_ce(model, validation_documents, args.device),
                           "assistant_turn": diagnostics._aggregate_trace(validation_rows)}
    conversation_path = work / "conversation_result.json"
    completed = subprocess.run(
        [sys.executable, str(ROOT / "cli/evaluate.py"), str(checkpoint),
         "--conversation-panel", str(panel_path), "--conversation-panel-sha256",
         dialogue_spec["panel_sha256"], "--out", str(conversation_path)],
        cwd=ROOT, env={**os.environ, "OMP_NUM_THREADS": "2", "MKL_NUM_THREADS": "2"},
        text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=False)
    (work / "conversation.log").write_text(completed.stdout, encoding="utf-8")
    if not conversation_path.is_file():
        raise RuntimeError("conversation evaluator did not produce its registered result")
    conversation = json.loads(conversation_path.read_text(encoding="utf-8"))

    counts = training_probe["counts"]
    retention_gate = broad_validation_score["ce"] < math.log(256.0)
    turn_gate = (training_probe["teacher"]["top1_accuracy"] >= 0.80 and counts["exact"] == 8
                 and counts["target_recovered"] == 8 and counts["structural"] == 8
                 and training_probe["prompt_causality"]["counts"]["ce_controlled"] >= 6)
    automatic = bool(retention_gate and turn_gate and conversation.get("pass"))
    if not retention_gate:
        verdict = protocol["decision"]["retention_failure"]
    elif not turn_gate:
        verdict = protocol["decision"]["turn_failure"]
    elif not conversation.get("pass"):
        verdict = protocol["decision"]["conversation_failure"]
    else:
        verdict = protocol["decision"]["automatic_pass"]
    result = {
        "schema": "anima-303m-r4-low-lr-sft-result/v1",
        "protocol_sha256": curriculum.sha256(protocol_path),
        "parent_result_sha256": curriculum.sha256(parent_result),
        "language_checkpoint_sha256": curriculum.sha256(language_checkpoint),
        "engine_sha256": curriculum.sha256(checkpoint), "device": args.device,
        "summary": summary, "broad_validation": broad_validation_score,
        "retention_gate": retention_gate, "training_probe": training_probe,
        "turn_gate": turn_gate, "dialogue_validation": dialogue_validation,
        "conversation_evaluator_exit": completed.returncode, "conversation": conversation,
        "gate": automatic, "verdict": verdict,
        "next_allowed_step": "No 303M, IIT-mouth, participant, or production action without automatic and manual conversation passes."
    }
    Path(args.result).write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
