#!/usr/bin/env python3
"""Run the preregistered document-aligned four-document treatment."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from pathlib import Path


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
    validation = parent._documents(validation_source)
    selector = fixed_data.get("view_selector", "first_four")
    if selector == "first_four":
        four_docs = documents[:4]
    elif selector == "first_four_runtime_compatible":
        four_docs = []
        for document in documents:
            exchange = parent._final_exchange(document)
            if (exchange is not None
                    and len(exchange[1].encode("utf-8", "surrogateescape"))
                    <= four.generator.CHAT_MAX_NEW_BYTES):
                four_docs.append(document)
                if len(four_docs) == 4:
                    break
    else:
        raise RuntimeError(f"unknown registered view selector: {selector}")
    val32 = validation[:32]
    if parent._sha256_bytes(parent._view_bytes(four_docs)) != fixed_data["four_document_view_sha256"]:
        raise RuntimeError("four-document view differs from preregistration")
    if parent._sha256_bytes(parent._view_bytes(val32)) != fixed_data["heldout_32_view_sha256"]:
        raise RuntimeError("heldout view differs from preregistration")
    exchanges = [parent._final_exchange(document) for document in four_docs]
    if any(exchange is None for exchange in exchanges):
        raise RuntimeError("registered view is not four complete exchanges")
    target_bytes = [len(exchange[1].encode("utf-8", "surrogateescape"))
                    for exchange in exchanges if exchange is not None]
    if any(size > four.generator.CHAT_MAX_NEW_BYTES for size in target_bytes):
        result = {
            "schema": "anima-303m-r4-document-alignment-result/v1",
            "protocol_sha256": _sha256(protocol_path),
            "verdict": "INVALID-GATE-UNREACHABLE",
            "canonical_max_new_bytes": four.generator.CHAT_MAX_NEW_BYTES,
            "target_bytes": target_bytes,
        }
        Path(args.result).write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
        return 4

    work = Path(args.work)
    work.mkdir(parents=True, exist_ok=True)
    train_path = work / "four.train.txt"
    validation_path = work / "heldout32.validation.txt"
    train_path.write_bytes(parent._view_bytes(four_docs))
    validation_path.write_bytes(parent._view_bytes(val32))
    fixed = protocol["fixed_recipe"]
    arm = {"d": fixed["d"], "layers": fixed["layers"], "steps": fixed["steps"],
           "checkpoint_every": 0}
    summary = four._train_arm(
        {"fixed_recipe": fixed}, "A1_document_alignment", arm, train_path,
        validation_path, work, args.device)
    checkpoint = work / "a1_document_alignment.bin"
    panel = json.loads(panel_path.read_text(encoding="utf-8"))
    score = four._score_arm(
        checkpoint, [exchange for exchange in exchanges if exchange is not None],
        panel["bars"], args.device)
    result = {
        "schema": "anima-303m-r4-document-alignment-result/v1",
        "protocol_sha256": _sha256(protocol_path),
        "parent_result_sha256": _sha256(parent_result),
        "device": args.device,
        "control": protocol["control"],
        "treatment": {
            "engine_sha256": _sha256(checkpoint),
            "parameters": four._parameter_count(checkpoint),
            "summary": summary,
            "score": score,
        },
        "gate": score["gate"],
        "verdict": ("SUPPORTED-DOCUMENT-ALIGNED-CONDITIONAL-LEARNING" if score["gate"]
                    else "FALSIFIED-DOCUMENT-ALIGNMENT-TREATMENT"),
        "next_allowed_step": (
            "This local diagnosis does not authorize 303M, IIT coupling, participant mounting "
            "or production; any scale-up requires a separately preregistered heldout test."),
    }
    Path(args.result).write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
