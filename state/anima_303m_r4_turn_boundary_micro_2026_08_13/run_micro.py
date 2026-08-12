#!/usr/bin/env python3
"""Run the preregistered assistant-turn-boundary treatment through shared paths."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import sys


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PARENT_DIR = ROOT / "state" / "anima_303m_r4_objective_micro_2026_08_13"
spec = importlib.util.spec_from_file_location("r4_objective_micro", PARENT_DIR / "run_micro.py")
parent = importlib.util.module_from_spec(spec)
if spec.loader is None:
    raise RuntimeError("objective micro harness loader is missing")
spec.loader.exec_module(parent)

for path in (ROOT / "core", ROOT / "cli"):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

import generator


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", required=True)
    parser.add_argument("--work", required=True)
    parser.add_argument("--result", required=True)
    parser.add_argument("--device", choices=["mps", "cuda", "cpu"], default="mps")
    args = parser.parse_args()

    protocol_path = HERE / "protocol.json"
    protocol = json.loads(protocol_path.read_text(encoding="utf-8"))
    parent_result = (HERE / protocol["parent_result"]).resolve()
    if parent._sha256(parent_result) != protocol["parent_result_sha256"]:
        raise RuntimeError("parent failure result SHA differs from preregistration")
    panel_path = (HERE / protocol["evaluation_panel"]["file"]).resolve()
    if parent._sha256(panel_path) != protocol["evaluation_panel"]["sha256"]:
        raise RuntimeError("evaluation panel SHA differs from preregistration")
    panel = json.loads(panel_path.read_text(encoding="utf-8"))
    generator.gen_chat_validate_template(
        panel["template"], max_new=panel["decode"]["max_new_bytes"])

    data = Path(args.data)
    if parent._sha256(data / "en_dialogue.train.txt") != protocol["fixed_data"]["train_file_sha256"]:
        raise RuntimeError("training file SHA differs from preregistration")
    if parent._sha256(data / "en_dialogue.validation.txt") != protocol["fixed_data"]["validation_file_sha256"]:
        raise RuntimeError("validation file SHA differs from preregistration")
    train_documents = parent._documents(data / "en_dialogue.train.txt")
    validation_documents = parent._documents(data / "en_dialogue.validation.txt")
    single = train_documents[:1]
    train100 = train_documents[:100]
    val32 = validation_documents[:32]
    views = protocol["fixed_data"]["views"]
    observed = {
        "single_document": parent._sha256_bytes(parent._view_bytes(single)),
        "hundred_document_train": parent._sha256_bytes(parent._view_bytes(train100)),
        "heldout_validation": parent._sha256_bytes(parent._view_bytes(val32)),
    }
    for name, digest in observed.items():
        if digest != views[name]["sha256"]:
            raise RuntimeError(f"{name} SHA differs from preregistration")

    exchanges = [exchange for document in train100
                 if (exchange := parent._final_exchange(document)) is not None][:8]
    if len(exchanges) != 8:
        raise RuntimeError("registered probe does not contain eight single exchanges")
    single_exchange = parent._final_exchange(single[0])
    if single_exchange is None:
        raise RuntimeError("registered single document is not one complete exchange")

    work = Path(args.work)
    work.mkdir(parents=True, exist_ok=True)
    single_path = work / "single.train.txt"
    train_path = work / "hundred.train.txt"
    validation_path = work / "heldout.validation.txt"
    single_path.write_bytes(parent._view_bytes(
        single * views["single_document"]["repetitions_for_full_window"]))
    train_path.write_bytes(parent._view_bytes(train100))
    validation_path.write_bytes(parent._view_bytes(val32))

    result = {
        "schema": "anima-303m-r4-turn-boundary-micro-result/v1",
        "protocol_sha256": parent._sha256(protocol_path),
        "parent_result_sha256": parent._sha256(parent_result),
        "panel_sha256": parent._sha256(panel_path),
        "dataset": {
            "repository": protocol["fixed_data"]["repository"],
            "revision": protocol["fixed_data"]["revision"],
            "view_sha256": observed,
        },
        "device": args.device,
        "mask_control": {
            "assistant_payload": True,
            "internal_newline": True,
            "next_user_role_delimiter": True,
            "following_user_content": False,
        },
        "single": {},
        "hundred": None,
    }
    summary = parent._train(
        protocol, work, "single_turn_only", single_path, None,
        protocol["model"]["single_document_steps"], "turn-only", args.device)
    decoded = parent._decode(work / "single_turn_only.bin", single_exchange[0])
    single_exact = decoded.get("text", "").strip() == single_exchange[1].strip()
    result["single"] = {
        "mode": "turn-only", "summary": summary,
        "prompt": single_exchange[0], "target": single_exchange[1],
        "decoded": decoded, "exact": single_exact,
    }

    if single_exact:
        summary = parent._train(
            protocol, work, "hundred_turn_only", train_path, validation_path,
            protocol["model"]["hundred_document_steps"], "turn-only", args.device)
        probe = parent._score(
            work / "hundred_turn_only.bin", exchanges, panel["bars"])
        result["hundred"] = {"mode": "turn-only", "summary": summary, "probe": probe}

    hundred = result["hundred"]
    counts = hundred["probe"]["counts"] if hundred else {}
    series = hundred["summary"].get("validation_series", []) if hundred else []
    final_val = (hundred["summary"]["heldout_descent"]["dialogue"]["val_ce"]
                 if hundred else None)
    gates = {
        "protocol_parent_data_panel_sha": True,
        "mask_positive_control": True,
        "single_document_positive_control": single_exact,
        "heldout_full_ce_descent": bool(
            len(series) >= 2 and final_val is not None
            and final_val < series[0]["full_ce"] and final_val < 5.545177444479562),
        "prompt_conditioning": bool(
            counts.get("nonempty", 0) >= 6 and counts.get("distinct", 0) >= 6),
        "target_recovery": counts.get("target_recovered", 0) >= 6,
        "structural": counts.get("structural", 0) == 8,
    }
    result["gates"] = gates
    result["verdict"] = ("PASS-R4-TURN-BOUNDARY-MICRO" if all(gates.values())
                         else "FAIL-R4-TURN-BOUNDARY-MICRO")
    result["next_allowed_step"] = (
        "Preregister one 303M single-seed assistant-turn-only R4 mouth screen."
        if result["verdict"].startswith("PASS") else
        "Do not run 303M or couple IIT state; preserve failed turn-boundary evidence.")
    Path(args.result).write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return 0 if result["verdict"].startswith("PASS") else 3


if __name__ == "__main__":
    raise SystemExit(main())
