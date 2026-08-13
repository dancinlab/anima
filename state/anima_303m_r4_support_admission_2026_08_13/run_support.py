#!/usr/bin/env python3
"""Run the preregistered complete-trajectory admission ladder."""

from __future__ import annotations

import argparse
import importlib.util
import json
import math
from pathlib import Path
import sys


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
for module_path in (ROOT / "core", ROOT / "cli"):
    if str(module_path) not in sys.path:
        sys.path.insert(0, str(module_path))

import generator

CAPACITY_SCRIPT = ROOT / "state/anima_303m_r4_capacity_ladder_2026_08_13/run_capacity.py"
SPEC = importlib.util.spec_from_file_location("r4_capacity_ladder", CAPACITY_SCRIPT)
capacity = importlib.util.module_from_spec(SPEC)
if SPEC.loader is None:
    raise RuntimeError("capacity-ladder harness loader is missing")
SPEC.loader.exec_module(capacity)
exposure, scale, curriculum, parent = (
    capacity.exposure, capacity.scale, capacity.curriculum, capacity.parent)


def _metrics(documents: list[str]) -> dict:
    parsed = [generator.gen_chat_parse_turns(document) for document in documents]
    return {
        "documents": len(documents),
        "single_turn": sum(len(turns) == 2 for turns in parsed),
        "multiturn": sum(len(turns) > 2 for turns in parsed),
        "assistant_turns": sum(
            sum(role == "assistant" for role, _ in turns) for turns in parsed),
    }


def _admit(documents: list[str], arm: dict) -> list[str]:
    admitted = []
    for document in documents:
        turns = generator.gen_chat_parse_turns(document)
        final_bytes = len(turns[-1][1].encode("utf-8", "strict"))
        policy = arm["policy"]
        if policy == "single_turn_final_response_le_192":
            accept = len(turns) == 2 and final_bytes <= generator.CHAT_MAX_NEW_BYTES
        elif policy == "complete_final_response_le_192":
            accept = final_bytes <= generator.CHAT_MAX_NEW_BYTES
        elif policy == "all_complete":
            accept = True
        else:
            raise RuntimeError("unregistered admission policy: " + str(policy))
        if accept:
            admitted.append(document)
    limit = arm.get("limit")
    return admitted if limit is None else admitted[:int(limit)]


def _view(documents: list[str]) -> bytes:
    return parent._view_bytes(documents)


def _final_exchange(document: str) -> tuple[str, str]:
    turns = generator.gen_chat_parse_turns(document)
    history = turns[:-2]
    transcript = (generator.gen_chat_render_turns(history)
                  + generator.CHAT_TURN_SEPARATOR) if history else ""
    seed = generator.gen_chat_seed(transcript, turns[-2][1])
    return seed, turns[-1][1]


def _control_reproduced(point: dict, expected: dict) -> bool:
    tolerance = float(expected["absolute_ce_tolerance"])
    return bool(
        abs(point["broad_validation"]["ce"] - expected["prior_broad_ce"]) <= tolerance
        and abs(point["dialogue_validation"]["assistant_turn"]["ce"]
                - expected["prior_heldout_assistant_ce"]) <= tolerance
        and point["semantic"] == expected["prior_semantic"]
        and point["structural"] == expected["prior_structural"])


def _run_arm(*, arm: dict, protocol: dict, language_checkpoint: Path,
             broad_train: Path, broad_validation: Path, dialogue_validation: Path,
             validation_documents: list[str], training_exchanges: list[tuple[str, str]],
             panel_path: Path, work: Path, device: str, documents: list[str]) -> dict:
    arm_work = work / arm["label"].lower().replace("-", "_")
    arm_work.mkdir(parents=True, exist_ok=True)
    dialogue_train = arm_work / "dialogue.train.txt"
    dialogue_train.write_bytes(_view(documents))
    mouth = arm_work / "joint"
    shape = {
        "label": arm["label"], "d": protocol["fixed_model"]["d"],
        "layers": protocol["fixed_model"]["layers"],
        "heads": protocol["fixed_model"]["heads"],
        "parameters": protocol["fixed_model"]["parameters"],
    }
    recipe = {
        "joint_phase": {
            "steps": protocol["fixed_recipe"]["steps"],
            "dialogue_rows": protocol["fixed_recipe"]["dialogue_rows"],
        }
    }
    summary = curriculum.run_train(
        capacity.joint_command(
            mouth, broad_train, broad_validation, dialogue_train,
            dialogue_validation, language_checkpoint, shape, recipe, device),
        mouth.with_suffix(".log"))
    capacity._validate_summary_shape(summary, shape)
    point = exposure.evaluate_point(
        checkpoint=mouth.with_suffix(".bin"), step=protocol["fixed_recipe"]["steps"],
        dialogue_rows=protocol["fixed_recipe"]["dialogue_rows"],
        broad_validation=broad_validation, validation_documents=validation_documents,
        training_exchanges=training_exchanges, panel_path=panel_path,
        panel_sha256=protocol["evaluation"]["panel_sha256"], work=arm_work,
        device=device)
    return {
        "label": arm["label"],
        "primary": bool(arm.get("primary", False)),
        "admission": _metrics(documents),
        "dialogue_view_bytes": dialogue_train.stat().st_size,
        "dialogue_view_sha256": scale.sha256(dialogue_train),
        "training_summary": summary,
        "point": point,
        "arm_gate": bool(point["broad_retention"] and point["conversation_pass"]),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--language-checkpoint", required=True)
    parser.add_argument("--broad-source", required=True)
    parser.add_argument("--dialogue-data", required=True)
    parser.add_argument("--work", required=True)
    parser.add_argument("--result", required=True)
    parser.add_argument("--protocol", default=str(HERE / "protocol.json"))
    parser.add_argument("--device", choices=["cpu", "cuda"], default="cpu")
    args = parser.parse_args()

    protocol_path = Path(args.protocol).resolve()
    protocol = json.loads(protocol_path.read_text(encoding="utf-8"))
    parent_result = (protocol_path.parent / protocol["parent_result"]).resolve()
    if scale.sha256(parent_result) != protocol["parent_result_sha256"]:
        raise RuntimeError("parent result identity differs from preregistration")

    model = protocol["fixed_model"]
    language_checkpoint = Path(args.language_checkpoint)
    if scale.sha256(language_checkpoint) != model["language_sha256"]:
        raise RuntimeError("language checkpoint identity differs from preregistration")

    broad = protocol["fixed_broad_data"]
    broad_source = Path(args.broad_source)
    if (broad_source.stat().st_size != broad["file_bytes"]
            or scale.sha256(broad_source) != broad["file_sha256"]):
        raise RuntimeError("broad source identity differs from preregistration")
    raw = broad_source.read_bytes()
    train_start, train_end = broad["train_range"]
    val_start, val_end = broad["validation_range"]
    broad_train_bytes = raw[train_start:train_end]
    broad_validation_bytes = raw[val_start:val_end]
    if (curriculum.sha256_bytes(broad_train_bytes) != broad["train_sha256"]
            or curriculum.sha256_bytes(broad_validation_bytes) != broad["validation_sha256"]):
        raise RuntimeError("broad view identity differs from preregistration")

    dialogue = protocol["fixed_dialogue_source"]
    dialogue_dir = Path(args.dialogue_data)
    train_source = dialogue_dir / dialogue["train_file"]
    validation_source = dialogue_dir / dialogue["validation_file"]
    for path, size_key, sha_key in (
            (train_source, "train_file_bytes", "train_file_sha256"),
            (validation_source, "validation_file_bytes", "validation_file_sha256")):
        if path.stat().st_size != dialogue[size_key] or scale.sha256(path) != dialogue[sha_key]:
            raise RuntimeError("dialogue source identity differs from preregistration")
    source_documents = parent._documents(train_source)
    if _metrics(source_documents) != {
            "documents": dialogue["source_documents"],
            "single_turn": dialogue["source_single_turn"],
            "multiturn": dialogue["source_multiturn"],
            "assistant_turns": dialogue["source_assistant_turns"]}:
        raise RuntimeError("dialogue support census differs from preregistration")
    validation_documents = parent._documents(validation_source)[:dialogue["heldout_documents"]]
    heldout_bytes = _view(validation_documents)
    if (len(heldout_bytes) != dialogue["heldout_view_bytes"]
            or curriculum.sha256_bytes(heldout_bytes) != dialogue["heldout_view_sha256"]):
        raise RuntimeError("heldout dialogue view differs from preregistration")

    admitted = []
    for arm in protocol["admission_arms"]:
        documents = _admit(source_documents, arm)
        view = _view(documents)
        metrics = _metrics(documents)
        expected = {key: arm[key] for key in
                    ("documents", "single_turn", "multiturn", "assistant_turns")}
        if metrics != expected or len(view) != arm["bytes"] or curriculum.sha256_bytes(view) != arm["sha256"]:
            raise RuntimeError("admitted dialogue view differs for " + arm["label"])
        admitted.append((arm, documents))

    panel_path = (protocol_path.parent / protocol["evaluation"]["panel"]).resolve()
    if scale.sha256(panel_path) != protocol["evaluation"]["panel_sha256"]:
        raise RuntimeError("conversation panel identity differs from preregistration")

    work = Path(args.work)
    work.mkdir(parents=True, exist_ok=True)
    broad_train = work / "broad.train.bin"
    broad_validation = work / "broad.validation.bin"
    dialogue_validation = work / "dialogue.validation.txt"
    broad_train.write_bytes(broad_train_bytes)
    broad_validation.write_bytes(broad_validation_bytes)
    dialogue_validation.write_bytes(heldout_bytes)
    control_documents = admitted[0][1]
    training_exchanges = [_final_exchange(document) for document in control_documents[:8]]

    arms = [_run_arm(
        arm=arm, protocol=protocol, language_checkpoint=language_checkpoint,
        broad_train=broad_train, broad_validation=broad_validation,
        dialogue_validation=dialogue_validation,
        validation_documents=validation_documents, training_exchanges=training_exchanges,
        panel_path=panel_path, work=work, device=args.device, documents=documents)
        for arm, documents in admitted]
    control_ok = _control_reproduced(arms[0]["point"], protocol["control_reproduction"])
    primary = next(arm for arm in arms if arm["primary"])
    gate = bool(control_ok and primary["arm_gate"])
    verdict = (
        protocol["decision"]["control_mismatch"] if not control_ok else
        protocol["decision"]["primary_automatic_pass"] if gate else
        protocol["decision"]["primary_failure"])
    result = {
        "schema": "anima-303m-r4-complete-support-admission-result/v1",
        "protocol_sha256": scale.sha256(protocol_path),
        "parent_result_sha256": scale.sha256(parent_result),
        "research_reference": protocol["research_reference"],
        "device": args.device,
        "control_reproduced": control_ok,
        "arms": arms,
        "primary_endpoint": protocol["evaluation"]["primary_endpoint"],
        "gate": gate,
        "verdict": verdict,
        "consciousness_claim": False,
        "next_allowed_step": (
            "Manual review and separately preregistered replication only."
            if gate else
            "Preregister broad-language data/compute scaling; 303M, IIT-mouth, participant and production remain blocked."),
    }
    Path(args.result).write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
