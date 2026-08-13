#!/usr/bin/env python3
"""Run the preregistered fixed-3,500-document optimization-exposure trajectory."""

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
SCALE_SCRIPT = ROOT / "state/anima_303m_r4_dialogue_scale_2026_08_13/run_scale.py"
SPEC = importlib.util.spec_from_file_location("r4_dialogue_scale", SCALE_SCRIPT)
scale = importlib.util.module_from_spec(SPEC)
if SPEC.loader is None:
    raise RuntimeError("dialogue-scale harness loader is missing")
SPEC.loader.exec_module(scale)
joint, curriculum, four, parent, diagnostics = (
    scale.joint, scale.curriculum, scale.four, scale.parent, scale.diagnostics)


def exposure_command(output: Path, broad_train: Path, broad_validation: Path,
                     dialogue_train: Path, dialogue_validation: Path,
                     language_checkpoint: Path, device: str) -> list[str]:
    command = joint.joint_command(
        output, broad_train, broad_validation, dialogue_train,
        dialogue_validation, language_checkpoint, device)
    command[command.index("--steps") + 1] = "30000"
    command[command.index("--lr-decay-steps") + 1] = "3750"
    command.extend(["--ckpt-every", "3750"])
    return command


def conversation_counts(conversation: dict) -> tuple[int, int]:
    english = conversation.get("summary", {}).get("by_language", {}).get("en", {})
    return int(english.get("semantic_passes", -1)), int(english.get("structural_passes", -1))


def control_reproduced(point: dict, control: dict) -> bool:
    semantic, structural = conversation_counts(point["conversation"])
    tolerance = float(control["absolute_ce_tolerance"])
    return bool(
        abs(point["broad_validation"]["ce"] - control["prior_broad_ce"]) <= tolerance
        and abs(point["dialogue_validation"]["assistant_turn"]["ce"]
                - control["prior_heldout_assistant_ce"]) <= tolerance
        and f"{semantic}/7" == control["prior_semantic"]
        and f"{structural}/7" == control["prior_structural"])


def checkpoint_for(output: Path, step: int, final_step: int) -> Path:
    if step == final_step:
        return output.with_suffix(".bin")
    return Path(f"{output.with_suffix('.bin')}.step{step}.bin")


def evaluate_point(*, checkpoint: Path, step: int, dialogue_rows: int,
                   broad_validation: Path, validation_documents: list[str],
                   training_exchanges: list[tuple[str, str]], panel_path: Path,
                   panel_sha256: str, work: Path, device: str) -> dict:
    point_work = work / f"step{step}"
    point_work.mkdir(parents=True, exist_ok=True)
    broad_score = curriculum.fixed_byte_ce(
        checkpoint, broad_validation.read_bytes(), device)
    panel = json.loads(panel_path.read_text(encoding="utf-8"))
    training_probe = four._score_arm(
        checkpoint, training_exchanges, panel["bars"], device)
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
    conversation_path = point_work / "conversation_result.json"
    completed = subprocess.run(
        [sys.executable, str(ROOT / "cli/evaluate.py"), str(checkpoint),
         "--conversation-panel", str(panel_path),
         "--conversation-panel-sha256", panel_sha256,
         "--out", str(conversation_path)], cwd=ROOT,
        env={**os.environ, "OMP_NUM_THREADS": "2", "MKL_NUM_THREADS": "2"},
        text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=False)
    (point_work / "conversation.log").write_text(completed.stdout, encoding="utf-8")
    if not conversation_path.is_file():
        raise RuntimeError(f"conversation evaluator produced no result at step {step}")
    conversation = json.loads(conversation_path.read_text(encoding="utf-8"))
    semantic, structural = conversation_counts(conversation)
    return {
        "step": step,
        "dialogue_row_exposure": dialogue_rows,
        "checkpoint": str(checkpoint.relative_to(work)),
        "engine_sha256": scale.sha256(checkpoint),
        "broad_validation": broad_score,
        "broad_retention": broad_score["ce"] < math.log(256.0),
        "training_probe": training_probe,
        "dialogue_validation": dialogue_score,
        "conversation_evaluator_exit": completed.returncode,
        "conversation": conversation,
        "semantic": f"{semantic}/7",
        "structural": f"{structural}/7",
        "multiturn_final_pass": bool(
            conversation.get("summary", {}).get("multiturn_final_pass")),
        "conversation_pass": bool(conversation.get("pass")),
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
    source_protocol_path = (protocol_path.parent / protocol["source_protocol"]).resolve()
    if scale.sha256(parent_result) != protocol["parent_result_sha256"]:
        raise RuntimeError("parent result identity differs from preregistration")
    if scale.sha256(source_protocol_path) != protocol["source_protocol_sha256"]:
        raise RuntimeError("source protocol identity differs from preregistration")
    source_protocol = json.loads(source_protocol_path.read_text(encoding="utf-8"))

    fixed = protocol["fixed_recipe"]
    language_checkpoint = Path(args.language_checkpoint)
    if scale.sha256(language_checkpoint) != fixed["language_checkpoint_sha256"]:
        raise RuntimeError("language checkpoint identity differs from preregistration")

    broad_source = Path(args.broad_source)
    source_spec_path = (source_protocol_path.parent / source_protocol["source_protocol"]).resolve()
    source_spec = json.loads(source_spec_path.read_text(encoding="utf-8"))
    broad_spec = source_spec["broad_data"]
    if scale.sha256(broad_source) != broad_spec["file_sha256"]:
        raise RuntimeError("broad source identity differs from preregistration")
    raw = broad_source.read_bytes()
    train_start, train_end = broad_spec["train_range"]
    val_start, val_end = broad_spec["validation_range"]
    broad_train_bytes = raw[train_start:train_end]
    broad_validation_bytes = raw[val_start:val_end]
    if curriculum.sha256_bytes(broad_train_bytes) != fixed["broad_train_sha256"]:
        raise RuntimeError("broad training view differs from preregistration")
    if curriculum.sha256_bytes(broad_validation_bytes) != fixed["broad_validation_sha256"]:
        raise RuntimeError("broad validation view differs from preregistration")

    data = protocol["fixed_data"]
    dialogue_dir = Path(args.dialogue_data)
    train_source = dialogue_dir / data["train_file"]
    validation_source = dialogue_dir / data["validation_file"]
    if scale.sha256(train_source) != data["train_file_sha256"]:
        raise RuntimeError("dialogue training source differs from preregistration")
    if scale.sha256(validation_source) != data["validation_file_sha256"]:
        raise RuntimeError("dialogue validation source differs from preregistration")
    selected = scale.runtime_compatible_documents(train_source)
    if len(selected) != data["eligible_documents"]:
        raise RuntimeError("eligible dialogue support differs from preregistration")
    dialogue_train_bytes = parent._view_bytes(selected[:data["documents"]])
    if (len(dialogue_train_bytes) != data["view_bytes"]
            or curriculum.sha256_bytes(dialogue_train_bytes) != data["view_sha256"]):
        raise RuntimeError("fixed 3500-document view differs from preregistration")
    validation_documents = parent._documents(validation_source)[:data["heldout_documents"]]
    dialogue_validation_bytes = parent._view_bytes(validation_documents)
    if curriculum.sha256_bytes(dialogue_validation_bytes) != data["heldout_view_sha256"]:
        raise RuntimeError("heldout dialogue view differs from preregistration")
    panel_path = (protocol_path.parent / data["panel"]).resolve()
    if scale.sha256(panel_path) != data["panel_sha256"]:
        raise RuntimeError("conversation panel identity differs from preregistration")

    work = Path(args.work)
    work.mkdir(parents=True, exist_ok=True)
    broad_train = work / "broad.train.bin"
    broad_validation = work / "broad.validation.bin"
    dialogue_train = work / "dialogue.train.txt"
    dialogue_validation = work / "dialogue.validation.txt"
    broad_train.write_bytes(broad_train_bytes)
    broad_validation.write_bytes(broad_validation_bytes)
    dialogue_train.write_bytes(dialogue_train_bytes)
    dialogue_validation.write_bytes(dialogue_validation_bytes)

    output = work / "exposure"
    command = exposure_command(
        output, broad_train, broad_validation, dialogue_train,
        dialogue_validation, language_checkpoint, args.device)
    summary = curriculum.run_train(command, output.with_suffix(".log"))
    trajectory = protocol["trajectory"]
    points = []
    training_exchanges = [parent._final_exchange(document) for document in selected[:8]]
    if any(exchange is None for exchange in training_exchanges):
        raise RuntimeError("registered training probe contains an incomplete exchange")
    for step, rows in zip(
            trajectory["evaluated_steps"], trajectory["dialogue_row_exposure"], strict=True):
        checkpoint = checkpoint_for(output, step, trajectory["primary_step"])
        if not checkpoint.is_file():
            raise RuntimeError(f"registered checkpoint is missing: {checkpoint}")
        points.append(evaluate_point(
            checkpoint=checkpoint, step=step, dialogue_rows=rows,
            broad_validation=broad_validation,
            validation_documents=validation_documents,
            training_exchanges=[item for item in training_exchanges if item is not None],
            panel_path=panel_path, panel_sha256=data["panel_sha256"],
            work=work, device=args.device))

    control_ok = control_reproduced(points[0], protocol["control_reproduction"])
    endpoint = next(point for point in points if point["step"] == trajectory["primary_step"])
    gate = bool(control_ok and endpoint["broad_retention"] and endpoint["conversation_pass"])
    if not control_ok:
        verdict = protocol["decision"]["control_mismatch"]
    elif gate:
        verdict = protocol["decision"]["automatic_pass"]
    else:
        verdict = protocol["decision"]["endpoint_failure"]
    result = {
        "schema": "anima-303m-r4-fixed-dialogue-exposure-result/v1",
        "protocol_sha256": scale.sha256(protocol_path),
        "parent_result_sha256": scale.sha256(parent_result),
        "research_reference": protocol["research_reference"],
        "device": args.device,
        "training_summary": summary,
        "points": points,
        "control_reproduced": control_ok,
        "primary_step": trajectory["primary_step"],
        "gate": gate,
        "verdict": verdict,
        "consciousness_claim": False,
        "next_allowed_step": (
            "Manual blind review is required before any larger mouth action."
            if gate else
            "If control reproduced and the endpoint still fails, preregister a fixed-data capacity ladder; 303M, IIT-mouth, participant and production remain blocked."
        ),
    }
    Path(args.result).write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
