#!/usr/bin/env python3
"""Run the preregistered V1 context arms through the canonical trainer/mouth."""

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


def _sha256(path: str | Path) -> str:
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _exchange(document: str) -> tuple[str, str]:
    markers = list(re.finditer(r"(?m)^(user|assistant): ", document))
    roles = [match.group(1) for match in markers]
    if not roles or roles[0] != "user" or roles[-1] != "assistant":
        raise RuntimeError("probe document has invalid roles")
    expected = ["user" if index % 2 == 0 else "assistant"
                for index in range(len(roles))]
    if roles != expected:
        raise RuntimeError("probe document does not alternate roles")
    final = markers[-1]
    return document[:final.end()], document[final.end():].strip()


def _train(protocol: dict, work: Path, name: str, train_path: Path,
           validation_path: Path, block: int, batch: int, device: str) -> dict:
    cfg = protocol["tiny_model_test"]
    output = work / name
    command = [
        sys.executable, str(ROOT / "cli/train.py"), "--arch", "bytegpt", "--canon",
        "--d", str(cfg["d"]), "--L", str(cfg["layers"]),
        "--seq-len", str(block), "--steps", str(cfg["steps"]),
        "--batch-size", str(batch), "--device", device, "--seed", str(cfg["seed"]),
        "--corpus", str(train_path), "--validation-corpus", str(validation_path),
        "--cell-label", "dialogue", "--require-cells", "1", "--sample", "proportional",
        "--chat-framed-sampling", "--answer-ce-marker", generator.CHAT_ASSISTANT_PREFIX,
        "--lr", str(cfg["peak_lr"]), "--adam-beta2", "0.95", "--weight-decay", "0.1",
        "--lr-schedule", "cosine", "--warmup-steps", "100",
        "--lr-decay-steps", str(cfg["steps"]), "--min-lr-ratio", "0.1",
        "--val-every", str(cfg["validation_every"]),
        "--val-batches", str(cfg["validation_batches"]),
        "--out", str(output.with_suffix(".bin")),
        "--ckpt-out", str(output.with_suffix(".pt")),
        "--gauges-out", str(output.with_suffix(".summary.json")),
        "--skip-inline-rho", "--log-every", "100",
    ]
    completed = subprocess.run(
        command, cwd=ROOT, env={**os.environ, "OMP_NUM_THREADS": "2", "MKL_NUM_THREADS": "2"},
        text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=False)
    output.with_suffix(".log").write_text(completed.stdout, encoding="utf-8")
    if completed.returncode != 0:
        raise RuntimeError(f"{name} training failed with {completed.returncode}")
    return json.loads(output.with_suffix(".summary.json").read_text(encoding="utf-8"))


def _score(checkpoint: Path, documents: list[str], bars: dict) -> dict:
    weights = None
    kind = generator.gen_mouth_kind(str(checkpoint))
    if kind != "bytegpt":
        raise RuntimeError("V1 checkpoint is not ByteGPT")
    import decode
    weights = decode.bg_load(str(checkpoint))
    rows = []
    for document in documents[:8]:
        seed, target = _exchange(document)
        decoded = generator.gen_loaded_chat(
            kind, weights, seed, generator.CHAT_MAX_NEW_BYTES)
        prefix = target.encode("utf-8")[:16].decode("utf-8", "ignore")
        score = evaluate.score_conversation_response(
            seed, decoded.get("text", ""),
            {"required_groups": [], "forbidden_terms": []}, "en", bars,
            stopped=bool(decoded.get("stopped")),
            raw_text=decoded.get("raw_text", decoded.get("text", "")))
        rows.append({"seed": seed, "target": target, "target_prefix": prefix,
                     "decoded": decoded,
                     "target_prefix_recovered": decoded.get("text", "").startswith(prefix),
                     "structural": bool(score["structural_pass"])})
    normalized = {" ".join(row["decoded"].get("text", "").lower().split())
                  for row in rows if row["decoded"].get("text", "").strip()}
    counts = {"nonempty": sum(bool(row["decoded"].get("text", "").strip()) for row in rows),
              "distinct": len(normalized),
              "structural": sum(row["structural"] for row in rows),
              "target_recovered": sum(row["target_prefix_recovered"] for row in rows)}
    return {"rows": rows, "counts": counts}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--device", choices=["cuda", "mps", "cpu"], default="cuda")
    args = parser.parse_args()
    protocol_path = HERE / "protocol.json"
    protocol = json.loads(protocol_path.read_text(encoding="utf-8"))
    data = Path(args.data)
    manifest = json.loads((data / "manifest.json").read_text(encoding="utf-8"))
    if manifest.get("verdict") != "PASS":
        raise RuntimeError("V1 data manifest did not pass")
    if manifest.get("protocol_sha256") != _sha256(protocol_path):
        raise RuntimeError("V1 data manifest protocol SHA mismatch")
    work = Path(args.output)
    work.mkdir(parents=True, exist_ok=True)
    arms = {
        "V0_short_512": ("short_train.txt", "short_validation.txt", 512, 8, "short_train"),
        "V1_short_2048": ("short_train.txt", "short_validation.txt", 2048, 2, "short_train"),
        "V1_long_2048": ("long_train.txt", "long_validation.txt", 2048, 2, "long_train"),
    }
    panel = json.loads((HERE / protocol["evaluation_panel"]["file"])
                       .resolve().read_text(encoding="utf-8"))
    result = {"schema": "anima-303m-v1-context-result/v1",
              "protocol_sha256": _sha256(protocol_path),
              "data_manifest_sha256": _sha256(data / "manifest.json"),
              "data": manifest, "arms": {}}
    for name, (train_name, validation_name, block, batch, probe_name) in arms.items():
        summary = _train(protocol, work, name.lower(), data / train_name,
                         data / validation_name, block, batch, args.device)
        probe = _score(work / f"{name.lower()}.bin",
                       _documents(data / f"{probe_name}.txt"), panel["bars"])
        heldout = summary["heldout_descent"]["dialogue"]
        result["arms"][name] = {"block": block, "batch": batch,
                                 "target_bytes_per_step": block * batch,
                                 "summary": summary, "probe": probe,
                                 "heldout_descent": bool(heldout["descent"])}
    v0 = result["arms"]["V0_short_512"]["probe"]["counts"]
    short = result["arms"]["V1_short_2048"]["probe"]["counts"]
    long = result["arms"]["V1_long_2048"]["probe"]["counts"]
    gates = {
        "data": manifest["verdict"] == "PASS",
        "heldout_descent": all(arm["heldout_descent"] for arm in result["arms"].values()),
        "short_prompt_conditioning": (short["nonempty"] >= 6 and short["distinct"] >= 6
                                      and short["structural"] >= 6),
        "short_target_recovery": (short["target_recovered"] >= 6
                                  and short["target_recovered"] > v0["target_recovered"]),
        "long_prompt_conditioning": (long["nonempty"] >= 6 and long["distinct"] >= 6
                                     and long["structural"] >= 6),
        "long_target_recovery": long["target_recovered"] >= 6,
    }
    result["gates"] = gates
    result["verdict"] = "PASS-V1-CONTEXT-MICRO" if all(gates.values()) else "FAIL-V1-CONTEXT-MICRO"
    result["next_allowed_step"] = (
        "Preregister one 303M single-seed R4 mouth screen."
        if result["verdict"] == "PASS-V1-CONTEXT-MICRO" else
        "Do not run 303M or couple IIT state; isolate the remaining mouth/data objective cause.")
    (work / "result.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return 0 if result["verdict"] == "PASS-V1-CONTEXT-MICRO" else 3


if __name__ == "__main__":
    raise SystemExit(main())
