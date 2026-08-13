#!/usr/bin/env python3
"""Run the preregistered fixed-data ByteGPT capacity ladder."""

from __future__ import annotations

import argparse
import importlib.util
import json
import math
from pathlib import Path
import sys


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
EXPOSURE_SCRIPT = ROOT / "state/anima_303m_r4_exposure_ladder_2026_08_13/run_exposure.py"
SPEC = importlib.util.spec_from_file_location("r4_exposure_ladder", EXPOSURE_SCRIPT)
exposure = importlib.util.module_from_spec(SPEC)
if SPEC.loader is None:
    raise RuntimeError("exposure-ladder harness loader is missing")
SPEC.loader.exec_module(exposure)
scale, joint, curriculum, four, parent, diagnostics = (
    exposure.scale, exposure.joint, exposure.curriculum,
    exposure.four, exposure.parent, exposure.diagnostics)


def _set_option(command: list[str], name: str, value: str) -> None:
    command[command.index(name) + 1] = value


def _shape_command(command: list[str], arm: dict) -> list[str]:
    command = list(command)
    _set_option(command, "--d", str(arm["d"]))
    _set_option(command, "--L", str(arm["layers"]))
    if "--canon" not in command:
        command.append("--canon")
    return command


def language_command(output: Path, broad_train: Path, broad_validation: Path,
                     arm: dict, recipe: dict, device: str) -> list[str]:
    command = curriculum.train_command(
        output, broad_train, broad_validation,
        steps=int(recipe["language_phase"]["steps"]), device=device)
    return _shape_command(command, arm)


def joint_command(output: Path, broad_train: Path, broad_validation: Path,
                  dialogue_train: Path, dialogue_validation: Path,
                  language_checkpoint: Path, arm: dict, recipe: dict,
                  device: str) -> list[str]:
    command = joint.joint_command(
        output, broad_train, broad_validation, dialogue_train,
        dialogue_validation, language_checkpoint, device)
    _set_option(command, "--steps", str(recipe["joint_phase"]["steps"]))
    _set_option(command, "--lr-decay-steps", "3750")
    return _shape_command(command, arm)


def _conversation_counts(conversation: dict) -> tuple[int, int]:
    english = conversation.get("summary", {}).get("by_language", {}).get("en", {})
    return int(english.get("semantic_passes", -1)), int(english.get("structural_passes", -1))


def _validate_summary_shape(summary: dict, arm: dict) -> None:
    if int(summary.get("n_params", -1)) != int(arm["parameters"]):
        raise RuntimeError(f"trainer parameter count differs for {arm['label']}")


def _run_arm(*, arm: dict, recipe: dict, broad_train: Path, broad_validation: Path,
             dialogue_train: Path, dialogue_validation: Path,
             validation_documents: list[str], training_exchanges: list[tuple[str, str]],
             panel_path: Path, panel_sha256: str, work: Path, device: str) -> dict:
    arm_work = work / arm["label"].lower()
    arm_work.mkdir(parents=True, exist_ok=True)
    language = arm_work / "language"
    language_summary = curriculum.run_train(
        language_command(language, broad_train, broad_validation, arm, recipe, device),
        language.with_suffix(".log"))
    _validate_summary_shape(language_summary, arm)
    language_checkpoint = language.with_suffix(".bin")
    language_validation = curriculum.fixed_byte_ce(
        language_checkpoint, broad_validation.read_bytes(), device)

    mouth = arm_work / "joint"
    joint_summary = curriculum.run_train(
        joint_command(mouth, broad_train, broad_validation, dialogue_train,
                      dialogue_validation, language_checkpoint, arm, recipe, device),
        mouth.with_suffix(".log"))
    _validate_summary_shape(joint_summary, arm)
    point = exposure.evaluate_point(
        checkpoint=mouth.with_suffix(".bin"), step=int(recipe["joint_phase"]["steps"]),
        dialogue_rows=int(recipe["joint_phase"]["dialogue_rows"]),
        broad_validation=broad_validation, validation_documents=validation_documents,
        training_exchanges=training_exchanges, panel_path=panel_path,
        panel_sha256=panel_sha256, work=arm_work, device=device)
    semantic, structural = _conversation_counts(point["conversation"])
    language_gate = language_validation["ce"] < math.log(256.0)
    return {
        "label": arm["label"],
        "shape": {key: arm[key] for key in ("d", "layers", "heads", "parameters")},
        "primary": bool(arm.get("primary", False)),
        "language_summary": language_summary,
        "language_engine_sha256": scale.sha256(language_checkpoint),
        "language_validation": language_validation,
        "language_gate": language_gate,
        "joint_summary": joint_summary,
        "point": point,
        "semantic": f"{semantic}/7",
        "structural": f"{structural}/7",
        "arm_gate": bool(language_gate and point["broad_retention"] and point["conversation_pass"]),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--broad-source", required=True)
    parser.add_argument("--dialogue-data", required=True)
    parser.add_argument("--work", required=True)
    parser.add_argument("--result", required=True)
    parser.add_argument("--protocol", default=str(HERE / "protocol.json"))
    parser.add_argument("--device", choices=["cpu", "cuda"], default="cpu")
    args = parser.parse_args()

    protocol_path = Path(args.protocol).resolve()
    protocol = json.loads(protocol_path.read_text(encoding="utf-8"))
    for path_key, sha_key in (("parent_result", "parent_result_sha256"),
                              ("exposure_protocol", "exposure_protocol_sha256"),
                              ("language_protocol", "language_protocol_sha256")):
        source = (protocol_path.parent / protocol[path_key]).resolve()
        if scale.sha256(source) != protocol[sha_key]:
            raise RuntimeError(f"{path_key} identity differs from preregistration")

    data = protocol["fixed_data"]
    broad_source = Path(args.broad_source)
    if (broad_source.stat().st_size != data["broad_file_bytes"]
            or scale.sha256(broad_source) != data["broad_file_sha256"]):
        raise RuntimeError("broad source identity differs from preregistration")
    raw = broad_source.read_bytes()
    ts, te = data["broad_train_range"]
    vs, ve = data["broad_validation_range"]
    broad_train_bytes, broad_validation_bytes = raw[ts:te], raw[vs:ve]
    if (curriculum.sha256_bytes(broad_train_bytes) != data["broad_train_sha256"]
            or curriculum.sha256_bytes(broad_validation_bytes) != data["broad_validation_sha256"]):
        raise RuntimeError("broad views differ from preregistration")

    dialogue_dir = Path(args.dialogue_data)
    train_source = dialogue_dir / data["dialogue_train_file"]
    validation_source = dialogue_dir / data["dialogue_validation_file"]
    if (scale.sha256(train_source) != data["dialogue_train_file_sha256"]
            or scale.sha256(validation_source) != data["dialogue_validation_file_sha256"]):
        raise RuntimeError("dialogue source identity differs from preregistration")
    selected = scale.runtime_compatible_documents(train_source)
    if len(selected) != data["eligible_documents"]:
        raise RuntimeError("eligible dialogue support differs from preregistration")
    dialogue_train_bytes = parent._view_bytes(selected[:data["documents"]])
    if (len(dialogue_train_bytes) != data["dialogue_view_bytes"]
            or curriculum.sha256_bytes(dialogue_train_bytes) != data["dialogue_view_sha256"]):
        raise RuntimeError("dialogue view differs from preregistration")
    validation_documents = parent._documents(validation_source)[:data["heldout_documents"]]
    dialogue_validation_bytes = parent._view_bytes(validation_documents)
    if curriculum.sha256_bytes(dialogue_validation_bytes) != data["heldout_view_sha256"]:
        raise RuntimeError("heldout dialogue view differs from preregistration")
    panel_path = (protocol_path.parent / data["panel"]).resolve()
    if scale.sha256(panel_path) != data["panel_sha256"]:
        raise RuntimeError("conversation panel identity differs from preregistration")

    work = Path(args.work)
    work.mkdir(parents=True, exist_ok=True)
    paths = {"bt": work / "broad.train.bin", "bv": work / "broad.validation.bin",
             "dt": work / "dialogue.train.txt", "dv": work / "dialogue.validation.txt"}
    paths["bt"].write_bytes(broad_train_bytes)
    paths["bv"].write_bytes(broad_validation_bytes)
    paths["dt"].write_bytes(dialogue_train_bytes)
    paths["dv"].write_bytes(dialogue_validation_bytes)
    training_exchanges = [parent._final_exchange(document) for document in selected[:8]]
    if any(item is None for item in training_exchanges):
        raise RuntimeError("registered training probe contains an incomplete exchange")

    arms = [_run_arm(
        arm=arm, recipe=protocol["fixed_recipe"], broad_train=paths["bt"],
        broad_validation=paths["bv"], dialogue_train=paths["dt"],
        dialogue_validation=paths["dv"], validation_documents=validation_documents,
        training_exchanges=[item for item in training_exchanges if item is not None],
        panel_path=panel_path, panel_sha256=data["panel_sha256"], work=work,
        device=args.device) for arm in protocol["capacity_arms"]]

    primary = next(arm for arm in arms if arm["primary"])
    gate = bool(primary["arm_gate"])
    decision = protocol["decision"]
    verdict = (decision["language_failure"] if not primary["language_gate"] else
               decision["primary_automatic_pass"] if gate else decision["primary_failure"])
    result = {
        "schema": "anima-303m-r4-fixed-data-capacity-ladder-result/v1",
        "protocol_sha256": scale.sha256(protocol_path), "device": args.device,
        "frozen_control": protocol["frozen_control"], "arms": arms,
        "primary": primary["label"], "gate": gate, "verdict": verdict,
        "research_reference": protocol["research_reference"], "consciousness_claim": False,
        "next_allowed_step": (
            "Manual blind review is required before any IIT-mouth or larger-model action."
            if gate else
            "Interpret the fixed-exposure capacity trajectory before preregistering one next axis; 303M, IIT-mouth, participant and production remain blocked."),
    }
    Path(args.result).write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n",
                                encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
