#!/usr/bin/env python3
"""Run matched V0/V2 arms through the canonical trainer and mouth dispatcher."""

from __future__ import annotations

import argparse
import hashlib
import importlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
for path in (ROOT / "core", ROOT / "cli"):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

import generator
evaluate = importlib.import_module("evaluate")


def _documents(path: str | Path) -> list[str]:
    return [value for value in Path(path).read_text(encoding="utf-8").split("\n\n")
            if value]


def _view_bytes(documents: list[str]) -> bytes:
    return ("\n\n".join(documents) + "\n\n").encode("utf-8")


def _sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _final_exchange(document: str) -> tuple[str, str] | None:
    markers = list(re.finditer(r"(?m)^(user|assistant): ", document))
    if [match.group(1) for match in markers] != ["user", "assistant"]:
        return None
    prompt = document[markers[0].end():markers[1].start()].strip()
    response = document[markers[1].end():].strip()
    return (prompt, response) if prompt and response else None


def _run_train(data: dict, work: Path, name: str, corpus: Path, validation: Path | None,
               steps: int, answer_ce: bool) -> dict:
    train = data["training"]
    output = work / name
    command = [
        sys.executable, str(ROOT / "cli" / "train.py"),
        "--arch", "bytegpt", "--d", "128", "--L", "4",
        "--seq-len", str(train["sequence_bytes"]), "--steps", str(steps),
        "--batch-size", str(train["batch"]), "--device", "mps",
        "--seed", "7", "--corpus", str(corpus), "--cell-label", "dialogue",
        "--require-cells", "1", "--sample", "proportional",
        "--chat-framed-sampling", "--answer-ce-marker", generator.CHAT_ASSISTANT_PREFIX,
        "--lr", str(train["peak_lr"]), "--adam-beta2", "0.95",
        "--weight-decay", "0.1", "--lr-schedule", "cosine",
        "--warmup-steps", "50", "--lr-decay-steps", str(steps),
        "--min-lr-ratio", "0.1", "--val-every", str(train["validation_every"]),
        "--val-batches", str(train["validation_batches"]),
        "--out", str(output.with_suffix(".bin")),
        "--ckpt-out", str(output.with_suffix(".pt")),
        "--gauges-out", str(output.with_suffix(".summary.json")),
        "--skip-inline-rho", "--log-every", "100",
    ]
    if validation is not None:
        command.extend(["--validation-corpus", str(validation)])
    if answer_ce:
        command.extend(["--answer-ce-weight", "1.0", "--answer-ce-all-spans"])
    completed = subprocess.run(
        command, cwd=ROOT, env={**os.environ, "OMP_NUM_THREADS": "2", "MKL_NUM_THREADS": "2"},
        text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=False)
    output.with_suffix(".log").write_text(completed.stdout, encoding="utf-8")
    if completed.returncode != 0:
        raise RuntimeError(f"{name} training failed with {completed.returncode}")
    return json.loads(output.with_suffix(".summary.json").read_text(encoding="utf-8"))


def _decode(checkpoint: Path, prompt: str) -> dict:
    seed = generator.gen_chat_seed("", prompt)
    return generator.gen_auto_chat(str(checkpoint), seed, generator.CHAT_MAX_NEW_BYTES)


def _structural(prompt: str, result: dict, bars: dict) -> bool:
    score = evaluate.score_conversation_response(
        prompt, result.get("text", ""), {"required_groups": [], "forbidden_terms": []},
        "en", bars, stopped=bool(result.get("stopped")),
        raw_text=result.get("raw_text", result.get("text", "")))
    return bool(score["structural_pass"])


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    protocol = json.loads((HERE / "protocol.json").read_text(encoding="utf-8"))
    data = protocol["tiny_model_test"]
    source = Path(args.data)
    work = Path(args.output)
    work.mkdir(parents=True, exist_ok=True)
    train_documents = _documents(source / "en_dialogue.train.txt")
    validation_documents = _documents(source / "en_dialogue.validation.txt")
    single = train_documents[:1]
    train100 = train_documents[:100]
    val32 = validation_documents[:32]
    views = data["data_views"]
    observed_hashes = {
        "single_document": _sha256_bytes(_view_bytes(single)),
        "hundred_document_train": _sha256_bytes(_view_bytes(train100)),
        "heldout_validation": _sha256_bytes(_view_bytes(val32)),
    }
    for name, digest in observed_hashes.items():
        if digest != views[name]["sha256"]:
            raise RuntimeError(f"{name} SHA differs from preregistration")
    single_path = work / "single.train.txt"
    train_path = work / "hundred.train.txt"
    validation_path = work / "heldout.validation.txt"
    single_path.write_bytes(_view_bytes(single * views["single_document"]
                                        ["repetitions_for_full_window"]))
    train_path.write_bytes(_view_bytes(train100))
    validation_path.write_bytes(_view_bytes(val32))

    parent_panel = json.loads((HERE / protocol["evaluation_panel"]["file"])
                              .resolve().read_text(encoding="utf-8"))
    bars = parent_panel["bars"]
    result = {"schema": "anima-303m-v0-v2-micro-result/v1",
              "protocol_sha256": hashlib.sha256((HERE / "protocol.json").read_bytes()).hexdigest(),
              "data_view_sha256": observed_hashes, "single": {}, "hundred": {}}
    expected_single = _final_exchange(single[0])
    if expected_single is None:
        raise RuntimeError("registered single document is not a single complete exchange")
    for arm, answer_ce in (("V0", False), ("V2", True)):
        summary = _run_train(data, work, f"single_{arm.lower()}", single_path, None,
                             data["training"]["single_document_steps"], answer_ce)
        decoded = _decode(work / f"single_{arm.lower()}.bin", expected_single[0])
        result["single"][arm] = {
            "summary": summary,
            "prompt": expected_single[0], "expected": expected_single[1],
            "decoded": decoded,
            "exact": decoded.get("text", "").strip() == expected_single[1].strip(),
        }
    single_pass = all(value["exact"] for value in result["single"].values())
    result["single_pass"] = single_pass
    if not single_pass:
        result["verdict"] = "FAIL-SINGLE-DOCUMENT-OVERFIT"
        (work / "micro_result.json").write_text(
            json.dumps(result, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")
        return 2

    probes = []
    for document in train100:
        exchange = _final_exchange(document)
        if exchange is not None:
            probes.append(exchange)
        if len(probes) == 8:
            break
    if len(probes) != 8:
        raise RuntimeError("fewer than eight deterministic single-exchange probes")
    for arm, answer_ce in (("V0", False), ("V2", True)):
        summary = _run_train(data, work, f"hundred_{arm.lower()}", train_path,
                             validation_path, data["training"]["hundred_document_steps"],
                             answer_ce)
        rows = []
        for prompt, target in probes:
            decoded = _decode(work / f"hundred_{arm.lower()}.bin", prompt)
            target_prefix = target.encode("utf-8")[:16].decode("utf-8", "ignore")
            rows.append({"prompt": prompt, "target": target, "target_prefix": target_prefix,
                         "decoded": decoded,
                         "target_prefix_recovered": decoded.get("text", "").startswith(target_prefix),
                         "structural": _structural(prompt, decoded, bars)})
        normalized = {" ".join(row["decoded"].get("text", "").lower().split()) for row in rows
                      if row["decoded"].get("text", "").strip()}
        nonempty = sum(bool(row["decoded"].get("text", "").strip()) for row in rows)
        recovered = sum(row["target_prefix_recovered"] for row in rows)
        structural = sum(row["structural"] for row in rows)
        heldout = summary["heldout_descent"]["dialogue"]
        gates = {"heldout_descent": bool(heldout["descent"]),
                 "nonempty_6_of_8": nonempty >= 6,
                 "distinct_6": len(normalized) >= 6,
                 "target_recovery_6_of_8": recovered >= 6,
                 "structural_8_of_8": structural == 8}
        result["hundred"][arm] = {"summary": summary, "probes": rows,
                                   "counts": {"nonempty": nonempty, "distinct": len(normalized),
                                              "target_recovered": recovered,
                                              "structural": structural},
                                   "gates": gates, "pass": all(gates.values())}
    v0 = result["hundred"]["V0"]
    v2 = result["hundred"]["V2"]
    ce_match = (v2["summary"]["final_val_ce_macro_cells"]
                <= v0["summary"]["final_val_ce_macro_cells"] + 0.02)
    result["v2_ce_not_worse"] = ce_match
    result["verdict"] = ("PASS-V2-MICRO" if v2["pass"] and ce_match
                         else "FAIL-V0-V2-MICRO")
    (work / "micro_result.json").write_text(
        json.dumps(result, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")
    return 0 if result["verdict"] == "PASS-V2-MICRO" else 3


if __name__ == "__main__":
    raise SystemExit(main())
