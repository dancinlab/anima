#!/usr/bin/env python3
"""Run the preregistered fixed-capacity dialogue-support scale ladder."""

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
JOINT_SCRIPT = ROOT / "state/anima_303m_r4_joint_replay_2026_08_13/run_joint.py"
SPEC = importlib.util.spec_from_file_location("r4_joint_replay", JOINT_SCRIPT)
joint = importlib.util.module_from_spec(SPEC)
if SPEC.loader is None:
    raise RuntimeError("joint-replay harness loader is missing")
SPEC.loader.exec_module(joint)
curriculum, four, parent, diagnostics = (
    joint.curriculum, joint.four, joint.parent, joint.diagnostics)


def sha256(path: str | Path) -> str:
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def runtime_compatible_documents(path: str | Path) -> list[str]:
    selected = []
    for document in parent._documents(Path(path)):
        exchange = parent._final_exchange(document)
        if (exchange is not None
                and len(exchange[1].encode("utf-8", "surrogateescape"))
                <= four.generator.CHAT_MAX_NEW_BYTES):
            selected.append(document)
    return selected


def evaluate_arm(*, limit: int, selected: list[str], validation_documents: list[str],
                 panel_path: Path, panel_sha256: str, broad_train: Path,
                 broad_validation: Path, language_checkpoint: Path, work: Path,
                 device: str) -> dict:
    arm_work = work / f"n{limit}"
    arm_work.mkdir(parents=True, exist_ok=True)
    dialogue_train = arm_work / "dialogue.train.txt"
    dialogue_validation = arm_work / "dialogue.validation.txt"
    dialogue_train.write_bytes(parent._view_bytes(selected[:limit]))
    dialogue_validation.write_bytes(parent._view_bytes(validation_documents))
    output = arm_work / "joint_replay"
    summary = curriculum.run_train(
        joint.joint_command(
            output, broad_train, broad_validation, dialogue_train,
            dialogue_validation, language_checkpoint, device),
        output.with_suffix(".log"))
    checkpoint = output.with_suffix(".bin")
    broad_score = curriculum.fixed_byte_ce(
        checkpoint, broad_validation.read_bytes(), device)
    panel = json.loads(panel_path.read_text(encoding="utf-8"))
    exchanges = [parent._final_exchange(document) for document in selected[:8]]
    if any(exchange is None for exchange in exchanges):
        raise RuntimeError("registered training probe contains an incomplete exchange")
    training_probe = four._score_arm(
        checkpoint, [item for item in exchanges if item is not None], panel["bars"], device)
    model = diagnostics._load_engine_torch(checkpoint, device)
    validation_exchanges = [
        diagnostics.v1._exchange(document) for document in validation_documents]
    validation_rows = [
        diagnostics._teacher_trace_seed(model, seed, target, device)
        for seed, target in validation_exchanges]
    dialogue_score = {
        "full": diagnostics._validation_full_ce(model, validation_documents, device),
        "assistant_turn": diagnostics._aggregate_trace(validation_rows),
    }
    conversation_path = arm_work / "conversation_result.json"
    completed = subprocess.run(
        [sys.executable, str(ROOT / "cli/evaluate.py"), str(checkpoint),
         "--conversation-panel", str(panel_path),
         "--conversation-panel-sha256", panel_sha256,
         "--out", str(conversation_path)], cwd=ROOT,
        env={**os.environ, "OMP_NUM_THREADS": "2", "MKL_NUM_THREADS": "2"},
        text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=False)
    (arm_work / "conversation.log").write_text(completed.stdout, encoding="utf-8")
    if not conversation_path.is_file():
        raise RuntimeError(f"conversation evaluator produced no result for N={limit}")
    conversation = json.loads(conversation_path.read_text(encoding="utf-8"))
    return {
        "documents": limit,
        "dialogue_train_bytes": dialogue_train.stat().st_size,
        "dialogue_train_sha256": sha256(dialogue_train),
        "engine_sha256": sha256(checkpoint),
        "summary": summary,
        "broad_validation": broad_score,
        "broad_retention": broad_score["ce"] < math.log(256.0),
        "training_probe": training_probe,
        "dialogue_validation": dialogue_score,
        "heldout_improvement": dialogue_score["assistant_turn"]["ce"] < 5.00458,
        "conversation_evaluator_exit": completed.returncode,
        "conversation": conversation,
    }


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
    source_protocol = (protocol_path.parent / protocol["source_protocol"]).resolve()
    if sha256(parent_result) != protocol["parent_result_sha256"]:
        raise RuntimeError("parent result identity differs from preregistration")
    if sha256(source_protocol) != protocol["source_protocol_sha256"]:
        raise RuntimeError("source protocol identity differs from preregistration")

    fixed = protocol["fixed_recipe"]
    language_checkpoint = Path(args.language_checkpoint)
    if sha256(language_checkpoint) != fixed["language_checkpoint_sha256"]:
        raise RuntimeError("language checkpoint identity differs from preregistration")
    source = json.loads(source_protocol.read_text(encoding="utf-8"))
    broad_source = Path(args.broad_source)
    if sha256(broad_source) != source["broad_data"]["file_sha256"]:
        raise RuntimeError("broad source identity differs from preregistration")
    raw = broad_source.read_bytes()
    ts, te = source["broad_data"]["train_range"]
    vs, ve = source["broad_data"]["validation_range"]
    broad_train_bytes, broad_validation_bytes = raw[ts:te], raw[vs:ve]
    if curriculum.sha256_bytes(broad_train_bytes) != fixed["broad_train_sha256"]:
        raise RuntimeError("broad training view differs from preregistration")
    if curriculum.sha256_bytes(broad_validation_bytes) != fixed["broad_validation_sha256"]:
        raise RuntimeError("broad validation view differs from preregistration")

    data_spec = protocol["data"]
    dialogue_dir = Path(args.dialogue_data)
    train_source = dialogue_dir / data_spec["train_file"]
    validation_source = dialogue_dir / data_spec["validation_file"]
    if sha256(train_source) != data_spec["train_file_sha256"]:
        raise RuntimeError("dialogue training source differs from preregistration")
    if sha256(validation_source) != data_spec["validation_file_sha256"]:
        raise RuntimeError("dialogue validation source differs from preregistration")
    selected = runtime_compatible_documents(train_source)
    if len(selected) != data_spec["eligible_documents"]:
        raise RuntimeError("eligible dialogue support differs from preregistration")
    validation_documents = parent._documents(validation_source)[:32]
    if curriculum.sha256_bytes(parent._view_bytes(validation_documents)) != data_spec["heldout_32_sha256"]:
        raise RuntimeError("heldout dialogue view differs from preregistration")
    for limit in protocol["arms"]:
        view = parent._view_bytes(selected[:limit])
        expected = data_spec["views"][str(limit)]
        if len(view) != expected["bytes"] or curriculum.sha256_bytes(view) != expected["sha256"]:
            raise RuntimeError(f"dialogue N={limit} view differs from preregistration")
    panel_path = (protocol_path.parent / data_spec["panel"]).resolve()
    if sha256(panel_path) != data_spec["panel_sha256"]:
        raise RuntimeError("conversation panel identity differs from preregistration")

    work = Path(args.work)
    work.mkdir(parents=True, exist_ok=True)
    broad_train = work / "broad.train.bin"
    broad_validation = work / "broad.validation.bin"
    broad_train.write_bytes(broad_train_bytes)
    broad_validation.write_bytes(broad_validation_bytes)
    arms = [
        evaluate_arm(
            limit=int(limit), selected=selected,
            validation_documents=validation_documents, panel_path=panel_path,
            panel_sha256=data_spec["panel_sha256"], broad_train=broad_train,
            broad_validation=broad_validation,
            language_checkpoint=language_checkpoint, work=work, device=args.device)
        for limit in protocol["arms"]
    ]
    endpoint = next(
        arm for arm in arms if arm["documents"] == protocol["primary_endpoint"])
    gate = bool(
        endpoint["broad_retention"] and endpoint["heldout_improvement"]
        and endpoint["conversation"].get("pass"))
    result = {
        "schema": "anima-303m-r4-dialogue-support-scale-result/v1",
        "protocol_sha256": sha256(protocol_path),
        "parent_result_sha256": sha256(parent_result),
        "research_reference": protocol["research_reference"],
        "device": args.device,
        "control_100": {
            "source": str(parent_result.relative_to(ROOT)),
            "assistant_turn_ce": 5.00458,
            "conversation_semantic": "0/7",
            "conversation_pass": False
        },
        "arms": arms,
        "primary_endpoint": protocol["primary_endpoint"],
        "gate": gate,
        "verdict": (
            protocol["decision"]["automatic_pass"] if gate
            else protocol["decision"]["endpoint_failure"]),
        "consciousness_claim": False,
        "next_allowed_step": (
            "Manual review is required before any larger mouth experiment."
            if gate else
            "Do not run 303M, IIT-mouth coupling, participant mounting, or production."
        ),
    }
    Path(args.result).write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
