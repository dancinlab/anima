#!/usr/bin/env python3
"""Run the preregistered matched R4 objective arms through the shared Python engine."""

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


def _sha256(path: str | Path) -> str:
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _documents(path: str | Path) -> list[str]:
    return [value for value in Path(path).read_text(encoding="utf-8").split("\n\n")
            if value]


def _view_bytes(documents: list[str]) -> bytes:
    return ("\n\n".join(documents) + "\n\n").encode("utf-8")


def _final_exchange(document: str) -> tuple[str, str] | None:
    markers = list(re.finditer(r"(?m)^(user|assistant): ", document))
    if [match.group(1) for match in markers] != ["user", "assistant"]:
        return None
    prompt = document[markers[0].end():markers[1].start()].strip()
    response = document[markers[1].end():].strip()
    return (prompt, response) if prompt and response else None


def _validation_series(log: str) -> list[dict]:
    values = []
    pattern = re.compile(r"step\s+(\d+).*?val_CE=([0-9.]+)")
    for match in pattern.finditer(log):
        values.append({"step": int(match.group(1)), "full_ce": float(match.group(2))})
    return values


def _train(protocol: dict, work: Path, name: str, train_path: Path,
           validation_path: Path | None, steps: int, mode: str, device: str) -> dict:
    cfg = protocol["model"]
    output = work / name
    command = [
        sys.executable, str(ROOT / "cli/train.py"),
        "--arch", "bytegpt", "--d", str(cfg["d"]), "--L", str(cfg["layers"]),
        "--seq-len", str(cfg["block"]), "--steps", str(steps),
        "--batch-size", str(cfg["batch"]), "--device", device,
        "--seed", str(cfg["seed"]), "--corpus", str(train_path),
        "--cell-label", "dialogue", "--require-cells", "1", "--sample", "proportional",
        "--chat-framed-sampling", "--answer-ce-marker", generator.CHAT_ASSISTANT_PREFIX,
        "--lr", str(cfg["peak_lr"]), "--adam-beta2", "0.95", "--weight-decay", "0.1",
        "--lr-schedule", "cosine", "--warmup-steps", "50",
        "--lr-decay-steps", str(steps), "--min-lr-ratio", "0.1",
        "--val-every", str(cfg["validation_every"]),
        "--val-batches", str(cfg["validation_batches"]),
        "--out", str(output.with_suffix(".bin")),
        "--ckpt-out", str(output.with_suffix(".pt")),
        "--gauges-out", str(output.with_suffix(".summary.json")),
        "--skip-inline-rho", "--log-every", "100",
    ]
    if validation_path is not None:
        command.extend(["--validation-corpus", str(validation_path)])
    if mode != "full":
        command.extend(["--answer-ce-weight", "1.0", "--answer-ce-all-spans"])
    if mode in ("only", "turn-only"):
        command.extend(["--answer-ce-mode", mode])
    completed = subprocess.run(
        command, cwd=ROOT,
        env={**os.environ, "OMP_NUM_THREADS": "2", "MKL_NUM_THREADS": "2"},
        text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=False)
    output.with_suffix(".log").write_text(completed.stdout, encoding="utf-8")
    if completed.returncode != 0:
        raise RuntimeError(f"{name} training failed with {completed.returncode}\n"
                           + completed.stdout[-4000:])
    summary = json.loads(output.with_suffix(".summary.json").read_text(encoding="utf-8"))
    summary["validation_series"] = _validation_series(completed.stdout)
    return summary


def _decode(checkpoint: Path, prompt: str) -> dict:
    seed = generator.gen_chat_seed("", prompt)
    return generator.gen_auto_chat(str(checkpoint), seed, generator.CHAT_MAX_NEW_BYTES)


def _score(checkpoint: Path, exchanges: list[tuple[str, str]], bars: dict) -> dict:
    rows = []
    for prompt, target in exchanges[:8]:
        decoded = _decode(checkpoint, prompt)
        prefix = target.encode("utf-8")[:16].decode("utf-8", "ignore")
        score = evaluate.score_conversation_response(
            prompt, decoded.get("text", ""),
            {"required_groups": [], "forbidden_terms": []}, "en", bars,
            stopped=bool(decoded.get("stopped")),
            raw_text=decoded.get("raw_text", decoded.get("text", "")))
        rows.append({
            "prompt": prompt,
            "target": target,
            "target_prefix": prefix,
            "decoded": decoded,
            "target_prefix_recovered": decoded.get("text", "").startswith(prefix),
            "structural": bool(score["structural_pass"]),
        })
    normalized = {" ".join(row["decoded"].get("text", "").lower().split())
                  for row in rows if row["decoded"].get("text", "").strip()}
    return {
        "rows": rows,
        "counts": {
            "nonempty": sum(bool(row["decoded"].get("text", "").strip()) for row in rows),
            "distinct": len(normalized),
            "structural": sum(row["structural"] for row in rows),
            "target_recovered": sum(row["target_prefix_recovered"] for row in rows),
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", required=True)
    parser.add_argument("--work", required=True)
    parser.add_argument("--result", required=True)
    parser.add_argument("--device", choices=["mps", "cuda", "cpu"], default="mps")
    args = parser.parse_args()

    protocol_path = HERE / "protocol.json"
    protocol = json.loads(protocol_path.read_text(encoding="utf-8"))
    panel_path = (HERE / protocol["evaluation_panel"]["file"]).resolve()
    if _sha256(panel_path) != protocol["evaluation_panel"]["sha256"]:
        raise RuntimeError("evaluation panel SHA differs from preregistration")
    panel = json.loads(panel_path.read_text(encoding="utf-8"))
    generator.gen_chat_validate_template(
        panel["template"], max_new=panel["decode"]["max_new_bytes"])

    data = Path(args.data)
    manifest = json.loads((data / "manifest.json").read_text(encoding="utf-8"))
    revision = protocol["fixed_data"]["revision"]
    if manifest.get("uploaded_revision") not in (None, revision):
        raise RuntimeError("dataset manifest revision differs from preregistration")
    train_documents = _documents(data / "en_dialogue.train.txt")
    validation_documents = _documents(data / "en_dialogue.validation.txt")
    single = train_documents[:1]
    train100 = train_documents[:100]
    val32 = validation_documents[:32]
    expected_hashes = protocol["fixed_data"]["views"]
    observed_hashes = {
        "single_document": _sha256_bytes(_view_bytes(single)),
        "hundred_document_train": _sha256_bytes(_view_bytes(train100)),
        "heldout_validation": _sha256_bytes(_view_bytes(val32)),
    }
    for name, digest in observed_hashes.items():
        if digest != expected_hashes[name]["sha256"]:
            raise RuntimeError(f"{name} SHA differs from preregistration")

    exchanges = [exchange for document in train100
                 if (exchange := _final_exchange(document)) is not None][:8]
    if len(exchanges) != 8:
        raise RuntimeError("registered probe does not contain eight single exchanges")
    work = Path(args.work)
    work.mkdir(parents=True, exist_ok=True)
    single_path = work / "single.train.txt"
    train_path = work / "hundred.train.txt"
    validation_path = work / "heldout.validation.txt"
    single_path.write_bytes(_view_bytes(single * expected_hashes["single_document"]
                                        ["repetitions_for_full_window"]))
    train_path.write_bytes(_view_bytes(train100))
    validation_path.write_bytes(_view_bytes(val32))

    result = {
        "schema": "anima-303m-r4-objective-micro-result/v1",
        "protocol_sha256": _sha256(protocol_path),
        "panel_sha256": _sha256(panel_path),
        "dataset": {
            "repository": protocol["fixed_data"]["repository"],
            "revision": revision,
            "source_file_sha256": {
                "train": _sha256(data / "en_dialogue.train.txt"),
                "validation": _sha256(data / "en_dialogue.validation.txt"),
                "manifest": _sha256(data / "manifest.json"),
            },
            "view_sha256": observed_hashes,
        },
        "device": args.device,
        "single": {},
        "hundred": {},
    }
    arms = (("O0_full", "full"), ("O1_additive", "additive"),
            ("O2_response_only", "only"))
    single_exchange = _final_exchange(single[0])
    if single_exchange is None:
        raise RuntimeError("registered single document is not one complete exchange")
    for name, mode in arms:
        summary = _train(protocol, work, "single_" + name.lower(), single_path, None,
                         protocol["model"]["single_document_steps"], mode, args.device)
        decoded = _decode(work / ("single_" + name.lower() + ".bin"), single_exchange[0])
        result["single"][name] = {
            "mode": mode, "summary": summary,
            "prompt": single_exchange[0], "target": single_exchange[1],
            "decoded": decoded,
            "exact": decoded.get("text", "").strip() == single_exchange[1].strip(),
        }
    single_pass = all(arm["exact"] for arm in result["single"].values())
    result["single_positive_control"] = single_pass
    if single_pass:
        for name, mode in arms:
            summary = _train(protocol, work, "hundred_" + name.lower(), train_path,
                             validation_path, protocol["model"]["hundred_document_steps"],
                             mode, args.device)
            probe = _score(work / ("hundred_" + name.lower() + ".bin"), exchanges,
                           panel["bars"])
            result["hundred"][name] = {"mode": mode, "summary": summary, "probe": probe}

    o2 = result["hundred"].get("O2_response_only")
    counts = o2["probe"]["counts"] if o2 else {}
    series = o2["summary"].get("validation_series", []) if o2 else []
    final_val = (o2["summary"]["heldout_descent"]["dialogue"]["val_ce"]
                 if o2 else None)
    gates = {
        "protocol_and_data_sha": True,
        "single_document_positive_control": single_pass,
        "heldout_full_ce_descent": bool(
            len(series) >= 2 and final_val is not None
            and final_val < series[0]["full_ce"] and final_val < 5.545177444479562),
        "prompt_conditioning": bool(
            counts.get("nonempty", 0) >= 6 and counts.get("distinct", 0) >= 6),
        "target_recovery": counts.get("target_recovered", 0) >= 6,
        "structural": counts.get("structural", 0) == 8,
        "control_honesty": all(name in result["hundred"] for name, _ in arms)
                           if single_pass else False,
    }
    result["gates"] = gates
    result["verdict"] = ("PASS-R4-RESPONSE-ONLY-MICRO" if all(gates.values())
                         else "FAIL-R4-OBJECTIVE-MICRO")
    result["next_allowed_step"] = (
        "Preregister one 303M single-seed response-only R4 mouth screen."
        if result["verdict"].startswith("PASS") else
        "Do not run 303M or couple IIT state; preserve the failed objective evidence.")
    Path(args.result).write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return 0 if result["verdict"].startswith("PASS") else 3


if __name__ == "__main__":
    raise SystemExit(main())
