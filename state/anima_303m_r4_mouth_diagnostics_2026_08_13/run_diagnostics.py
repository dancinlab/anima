#!/usr/bin/env python3
"""Run the preregistered R4 D0-D6 diagnostics through the shared Python engine."""

from __future__ import annotations

import argparse
import hashlib
import importlib
import importlib.util
import json
import math
import os
from pathlib import Path
import re
import subprocess
import sys
from typing import Iterable

import numpy as np
import torch


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
for path in (ROOT / "core", ROOT / "cli"):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

import decode
import generator
from model import ByteGPT, ByteGPTConfig
from core import serialize as serializer

evaluate = importlib.import_module("evaluate")
PARENT_SCRIPT = ROOT / "state/anima_303m_r4_objective_micro_2026_08_13/run_micro.py"
PARENT_SPEC = importlib.util.spec_from_file_location("r4_objective_micro", PARENT_SCRIPT)
parent = importlib.util.module_from_spec(PARENT_SPEC)
if PARENT_SPEC.loader is None:
    raise RuntimeError("R4 objective harness loader is missing")
PARENT_SPEC.loader.exec_module(parent)
V1_SCRIPT = ROOT / "state/anima_303m_v1_context_micro_2026_08_12/run_micro.py"
V1_SPEC = importlib.util.spec_from_file_location("r4_v1_context_micro", V1_SCRIPT)
v1 = importlib.util.module_from_spec(V1_SPEC)
if V1_SPEC.loader is None:
    raise RuntimeError("V1 context harness loader is missing")
V1_SPEC.loader.exec_module(v1)


def _sha256(path: str | Path) -> str:
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _softmax_stats(logits: torch.Tensor, gold: int) -> tuple[int, float, float, float]:
    values = logits.float()
    probs = torch.softmax(values, dim=0)
    gold_prob = float(probs[gold])
    gold_rank = 1 + int(torch.count_nonzero(values > values[gold]))
    top = torch.topk(values, 2).values
    return int(torch.argmax(values)), gold_prob, gold_rank, float(top[0] - top[1])


def _load_engine_torch(checkpoint: str | Path, device: str) -> ByteGPT:
    state, cfg = serializer.deserialize_bytegpt(str(checkpoint))
    model = ByteGPT(ByteGPTConfig(**cfg)).to(device)
    model.load_state_dict(state, strict=True)
    model.eval()
    return model


def _load_resume_torch(checkpoint: str | Path, device: str) -> ByteGPT:
    payload = torch.load(checkpoint, map_location="cpu", weights_only=False)
    recipe = payload["recipe"]
    cfg = ByteGPTConfig(
        vocab=256, d=int(recipe["d"]), n_layer=int(recipe["L"]),
        n_head=max(1, int(recipe["d"]) // 64), block=int(recipe["seq_len"]))
    model = ByteGPT(cfg).to(device)
    model.load_state_dict(payload["model"], strict=True)
    model.eval()
    return model


def _next_logits(model: ByteGPT, prefix: bytes, device: str) -> torch.Tensor:
    if not prefix:
        raise ValueError("next-byte prefix must not be empty")
    ids = list(prefix[-model.block:])
    tensor = torch.tensor(ids, dtype=torch.long, device=device)[None, :]
    with torch.no_grad():
        return model(tensor)["logits"][0, :, -1].detach().cpu()


def _teacher_trace_seed(model: ByteGPT, seed_text: str, target: str, device: str) -> dict:
    seed = seed_text.encode("utf-8", "surrogateescape")
    target_bytes = target.encode("utf-8", "surrogateescape")
    rows = []
    prefix = bytearray(seed)
    for index, gold in enumerate(target_bytes):
        logits = _next_logits(model, bytes(prefix), device)
        top1, probability, rank, margin = _softmax_stats(logits, gold)
        rows.append({
            "index": index,
            "gold": gold,
            "top1": top1,
            "correct": top1 == gold,
            "gold_probability": probability,
            "gold_rank": rank,
            "top1_top2_margin": margin,
        })
        prefix.append(gold)
    first_error = next((row for row in rows if not row["correct"]), None)
    return {
        "bytes": len(rows),
        "ce": (-sum(math.log(max(row["gold_probability"], 1e-45)) for row in rows)
               / max(1, len(rows))),
        "top1_accuracy": sum(row["correct"] for row in rows) / max(1, len(rows)),
        "mean_gold_probability": (sum(row["gold_probability"] for row in rows)
                                  / max(1, len(rows))),
        "mean_gold_rank": sum(row["gold_rank"] for row in rows) / max(1, len(rows)),
        "first_error_position": None if first_error is None else first_error["index"],
        "first_error_margin": None if first_error is None else first_error["top1_top2_margin"],
    }


def _teacher_trace(model: ByteGPT, prompt: str, target: str, device: str) -> dict:
    return _teacher_trace_seed(
        model, generator.gen_chat_seed("", prompt), target, device)


def _first_divergence(actual: bytes, expected: bytes) -> int | None:
    for index, (left, right) in enumerate(zip(actual, expected)):
        if left != right:
            return index
    return None if len(actual) == len(expected) else min(len(actual), len(expected))


def _longest_byte_run(value: bytes) -> int:
    best = current = 0
    previous = None
    for byte in value:
        current = current + 1 if byte == previous else 1
        previous = byte
        best = max(best, current)
    return best


def _longest_word_run(text: str) -> int:
    words = re.findall(r"[A-Za-z]+", text.lower())
    best = current = 0
    previous = None
    for word in words:
        current = current + 1 if word == previous else 1
        previous = word
        best = max(best, current)
    return best


def _free_row(checkpoint: Path, prompt: str, target: str, bars: dict,
              weights: dict | None = None) -> dict:
    seed = generator.gen_chat_seed("", prompt)
    if weights is None:
        decoded = generator.gen_auto_chat(
            str(checkpoint), seed, generator.CHAT_MAX_NEW_BYTES)
    else:
        decoded = generator.gen_loaded_chat(
            "bytegpt", weights, seed, generator.CHAT_MAX_NEW_BYTES)
    actual = decoded.get("text", "").encode("utf-8", "surrogateescape")
    expected = target.encode("utf-8", "surrogateescape")
    prefix = expected[:16]
    structural = evaluate.score_conversation_response(
        prompt, decoded.get("text", ""),
        {"required_groups": [], "forbidden_terms": []}, "en", bars,
        stopped=bool(decoded.get("stopped")),
        raw_text=decoded.get("raw_text", decoded.get("text", "")))
    return {
        "prompt": prompt,
        "target": target,
        "decoded": decoded,
        "target_prefix_recovered": actual.startswith(prefix),
        "first_divergence_position": _first_divergence(actual, expected),
        "structural": bool(structural["structural_pass"]),
        "longest_byte_run": _longest_byte_run(actual),
        "longest_word_run": _longest_word_run(decoded.get("text", "")),
    }


def _aggregate_trace(rows: Iterable[dict]) -> dict:
    values = list(rows)
    total_bytes = sum(row["bytes"] for row in values)
    return {
        "documents": len(values),
        "bytes": total_bytes,
        "ce": (sum(row["ce"] * row["bytes"] for row in values) / max(1, total_bytes)),
        "top1_accuracy": (sum(row["top1_accuracy"] * row["bytes"] for row in values)
                          / max(1, total_bytes)),
        "mean_gold_probability": (
            sum(row["mean_gold_probability"] * row["bytes"] for row in values)
            / max(1, total_bytes)),
        "mean_gold_rank": (sum(row["mean_gold_rank"] * row["bytes"] for row in values)
                           / max(1, total_bytes)),
    }


def _score_checkpoint(checkpoint: Path, exchanges: list[tuple[str, str]], bars: dict,
                      device: str) -> dict:
    model = _load_engine_torch(checkpoint, device)
    weights = decode.bg_load(str(checkpoint))
    rows = []
    for prompt, target in exchanges[:8]:
        trace = _teacher_trace(model, prompt, target, device)
        free = _free_row(checkpoint, prompt, target, bars, weights=weights)
        rows.append({"teacher": trace, "free": free})
    normalized = {
        " ".join(row["free"]["decoded"].get("text", "").lower().split())
        for row in rows if row["free"]["decoded"].get("text", "").strip()
    }
    return {
        "teacher": _aggregate_trace(row["teacher"] for row in rows),
        "counts": {
            "nonempty": sum(bool(row["free"]["decoded"].get("text", "").strip())
                            for row in rows),
            "distinct": len(normalized),
            "target_recovered": sum(row["free"]["target_prefix_recovered"] for row in rows),
            "structural": sum(row["free"]["structural"] for row in rows),
        },
        "rows": rows,
    }


def _validation_full_ce(model: ByteGPT, documents: list[str], device: str) -> dict:
    losses = []
    correct = total = 0
    for document in documents:
        raw = document.encode("utf-8", "surrogateescape")
        if len(raw) < 2 or len(raw) - 1 > model.block:
            raise RuntimeError("fixed validation document exceeds the registered block")
        x = torch.tensor(list(raw[:-1]), dtype=torch.long, device=device)[None, :]
        y = torch.tensor(list(raw[1:]), dtype=torch.long, device=device)
        with torch.no_grad():
            logits = model(x)["logits"][0].transpose(0, 1).float()
            losses.append(float(torch.nn.functional.cross_entropy(logits, y, reduction="sum")))
            correct += int(torch.count_nonzero(torch.argmax(logits, dim=1) == y))
            total += int(y.numel())
    return {"bytes": total, "ce": sum(losses) / max(1, total),
            "top1_accuracy": correct / max(1, total)}


def _train(protocol: dict, work: Path, name: str, train_path: Path,
           validation_path: Path, mode: str, device: str, checkpoints: bool) -> dict:
    cfg = protocol["model"]
    output = work / name
    completed_paths = [output.with_suffix(suffix) for suffix in
                       (".bin", ".pt", ".summary.json", ".log")]
    if all(path.is_file() for path in completed_paths):
        payload = torch.load(output.with_suffix(".pt"), map_location="cpu", weights_only=False)
        recipe = payload.get("recipe", {})
        answer = recipe.get("answer_ce")
        expected_answer_mode = None if mode == "full" else mode
        observed_answer_mode = None if answer is None else answer.get("mode")
        valid = (
            payload.get("completed_step") == cfg["steps"]
            and payload.get("endpoint_steps") == cfg["steps"]
            and recipe.get("arch") == "bytegpt"
            and recipe.get("d") == cfg["d"]
            and recipe.get("L") == cfg["layers"]
            and recipe.get("seed") == cfg["seed"]
            and recipe.get("seq_len") == cfg["block"]
            and recipe.get("batch_size") == cfg["batch"]
            and recipe.get("corpus") == [str(train_path)]
            and recipe.get("validation_corpus") == [str(validation_path)]
            and observed_answer_mode == expected_answer_mode)
        if not valid:
            raise RuntimeError(f"completed {name} artifacts do not match the frozen recipe")
        summary = json.loads(output.with_suffix(".summary.json").read_text(encoding="utf-8"))
        summary["diagnostic_reused_completed"] = True
        return summary
    command = [
        sys.executable, str(ROOT / "cli/train.py"),
        "--arch", "bytegpt", "--d", str(cfg["d"]), "--L", str(cfg["layers"]),
        "--seq-len", str(cfg["block"]), "--steps", str(cfg["steps"]),
        "--batch-size", str(cfg["batch"]), "--device", device,
        "--seed", str(cfg["seed"]), "--corpus", str(train_path),
        "--validation-corpus", str(validation_path),
        "--cell-label", "dialogue", "--require-cells", "1", "--sample", "proportional",
        "--chat-framed-sampling", "--answer-ce-marker", generator.CHAT_ASSISTANT_PREFIX,
        "--lr", str(cfg["peak_lr"]), "--adam-beta2", "0.95", "--weight-decay", "0.1",
        "--lr-schedule", "cosine", "--warmup-steps", "50",
        "--lr-decay-steps", str(cfg["steps"]), "--min-lr-ratio", "0.1",
        "--val-every", "100", "--val-batches", "4", "--log-every", "100",
        "--out", str(output.with_suffix(".bin")),
        "--ckpt-out", str(output.with_suffix(".pt")),
        "--gauges-out", str(output.with_suffix(".summary.json")),
        "--skip-inline-rho",
    ]
    if mode != "full":
        command.extend(["--answer-ce-weight", "1.0", "--answer-ce-all-spans"])
    if mode in ("only", "turn-only"):
        command.extend(["--answer-ce-mode", mode])
    if checkpoints:
        command.extend(["--ckpt-every", str(cfg["checkpoint_every"])])
    completed = subprocess.run(
        command, cwd=ROOT,
        env={**os.environ, "OMP_NUM_THREADS": "2", "MKL_NUM_THREADS": "2"},
        text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=False)
    output.with_suffix(".log").write_text(completed.stdout, encoding="utf-8")
    if completed.returncode != 0:
        raise RuntimeError(f"{name} training failed with {completed.returncode}\n"
                           + completed.stdout[-6000:])
    return json.loads(output.with_suffix(".summary.json").read_text(encoding="utf-8"))


def _d0(actual_bin: Path, actual_pt: Path,
        exchanges: list[tuple[str, str]]) -> dict:
    torch_model = _load_resume_torch(actual_pt, "cpu")
    engine_model = _load_engine_torch(actual_bin, "cpu")
    weights = decode.bg_load(str(actual_bin))
    pt_state = torch_model.state_dict()
    bin_state = engine_model.state_dict()
    state_error = max(float((pt_state[name] - bin_state[name]).abs().max())
                      for name in pt_state)
    logit_error = 0.0
    argmax_equal = True
    probes = []
    for prompt, target in exchanges[:8]:
        seed = generator.gen_chat_seed("", prompt).encode("utf-8", "surrogateescape")
        target_bytes = target.encode("utf-8", "surrogateescape")
        prefix_rows = []
        for extent in (0, 1, 4, 16):
            prefix = seed + target_bytes[:extent]
            torch_logits = _next_logits(torch_model, prefix, "cpu").numpy()
            engine_logits = np.asarray(decode.bg_forward_last_W(
                weights, list(prefix[-weights["block"]:]),
                min(len(prefix), weights["block"])))
            error = float(np.max(np.abs(torch_logits - engine_logits)))
            logit_error = max(logit_error, error)
            same = int(np.argmax(torch_logits)) == int(np.argmax(engine_logits))
            argmax_equal = argmax_equal and same
            prefix_rows.append({"target_prefix_bytes": extent, "max_abs_error": error,
                                "argmax_equal": same})
        fast = decode._decode_argmax_W(weights, seed, 32)
        full = decode._decode_argmax_W_full(weights, seed, 32)
        canonical = generator.gen_auto_chat(str(actual_bin), seed.decode(
            "utf-8", "surrogateescape"), 32)
        canonical_raw = canonical.get("raw_text", "").encode("utf-8", "surrogateescape")
        probes.append({
            "prompt": prompt,
            "prefix_logits": prefix_rows,
            "kv_full_equal": fast["ids"] == full["ids"],
            "canonical_resident_equal": canonical_raw == bytes(fast["ids"]),
        })
    gate = (state_error == 0.0 and logit_error <= 0.0001 and argmax_equal
            and all(row["kv_full_equal"] and row["canonical_resident_equal"]
                    for row in probes))
    return {"state_max_abs_error": state_error, "logit_max_abs_error": logit_error,
            "argmax_equal": argmax_equal, "probes": probes, "gate": gate}


def _prompt_intervention(checkpoint: Path, exchanges: list[tuple[str, str]],
                         bars: dict, device: str) -> dict:
    model = _load_engine_torch(checkpoint, device)
    weights = decode.bg_load(str(checkpoint))
    rows = []
    for index, (prompt, target) in enumerate(exchanges[:8]):
        shuffled = exchanges[(index + 1) % 8][0]
        conditions = {}
        for name, conditioned_prompt in (
                ("normal", prompt), ("blank", ""), ("shuffled", shuffled)):
            trace = _teacher_trace(model, conditioned_prompt, target, device)
            free = _free_row(checkpoint, conditioned_prompt, target, bars, weights=weights)
            conditions[name] = {"ce": trace["ce"], "top1_accuracy": trace["top1_accuracy"],
                                "text": free["decoded"].get("text", "")}
        normal_text = conditions["normal"]["text"]
        ce_controlled = (conditions["normal"]["ce"] < conditions["blank"]["ce"]
                         and conditions["normal"]["ce"] < conditions["shuffled"]["ce"])
        output_controlled = not (
            normal_text == conditions["blank"]["text"]
            and normal_text == conditions["shuffled"]["text"])
        rows.append({"prompt": prompt, "shuffled_prompt": shuffled,
                     "conditions": conditions, "ce_controlled": ce_controlled,
                     "output_controlled": output_controlled})
    gate = (sum(row["ce_controlled"] for row in rows) >= 6
            and all(row["output_controlled"] for row in rows))
    return {"rows": rows,
            "counts": {"ce_controlled": sum(row["ce_controlled"] for row in rows),
                       "output_controlled": sum(row["output_controlled"] for row in rows)},
            "gate": gate}


def _checkpoint_path(base: Path, step: int) -> Path:
    if step == 600:
        return base.with_suffix(".bin")
    return Path(str(base.with_suffix(".bin")) + f".step{step}.bin")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", required=True)
    parser.add_argument("--artifacts", required=True)
    parser.add_argument("--work", required=True)
    parser.add_argument("--result", required=True)
    parser.add_argument("--device", choices=["mps", "cpu"], default="mps")
    args = parser.parse_args()

    protocol_path = HERE / "protocol.json"
    protocol = json.loads(protocol_path.read_text(encoding="utf-8"))
    fixed = protocol["fixed_artifacts"]
    if _sha256((HERE / fixed["panel"]).resolve()) != fixed["panel_sha256"]:
        raise RuntimeError("conversation panel SHA differs from preregistration")
    parent_result = (HERE / protocol["parent_result"]).resolve()
    if _sha256(parent_result) != protocol["parent_result_sha256"]:
        raise RuntimeError("parent result SHA differs from preregistration")

    data = Path(args.data)
    artifacts = Path(args.artifacts)
    train_source = data / fixed["train_file"]
    validation_source = data / fixed["validation_file"]
    if _sha256(train_source) != fixed["train_file_sha256"]:
        raise RuntimeError("training source SHA differs from preregistration")
    if _sha256(validation_source) != fixed["validation_file_sha256"]:
        raise RuntimeError("validation source SHA differs from preregistration")
    actual_bin = artifacts / fixed["actual_failed_engine_checkpoint"]
    actual_pt = artifacts / fixed["actual_failed_torch_checkpoint"]
    manifest = json.loads((artifacts / "artifact_manifest.json").read_text(encoding="utf-8"))
    for relative, path in ((fixed["actual_failed_engine_checkpoint"], actual_bin),
                           (fixed["actual_failed_torch_checkpoint"], actual_pt)):
        if _sha256(path) != manifest["files"][relative]["sha256"]:
            raise RuntimeError(f"artifact SHA differs from HF manifest: {relative}")

    train_documents = parent._documents(train_source)
    validation_documents = parent._documents(validation_source)
    train100 = train_documents[:100]
    val32 = validation_documents[:32]
    observed_views = {
        "single_document_sha256": parent._sha256_bytes(parent._view_bytes(train_documents[:1])),
        "hundred_document_sha256": parent._sha256_bytes(parent._view_bytes(train100)),
        "heldout_32_sha256": parent._sha256_bytes(parent._view_bytes(val32)),
    }
    for name, digest in observed_views.items():
        if digest != fixed["views"][name]:
            raise RuntimeError(f"{name} differs from preregistration")
    exchanges = [exchange for document in train100
                 if (exchange := parent._final_exchange(document)) is not None][:8]
    if len(exchanges) != 8:
        raise RuntimeError("frozen probe does not contain eight single exchanges")
    panel = json.loads((HERE / fixed["panel"]).resolve().read_text(encoding="utf-8"))
    bars = panel["bars"]

    work = Path(args.work)
    work.mkdir(parents=True, exist_ok=True)
    validation_path = work / "heldout32.validation.txt"
    validation_path.write_bytes(parent._view_bytes(val32))
    result = {
        "schema": "anima-303m-r4-mouth-diagnostics-result/v1",
        "protocol_sha256": _sha256(protocol_path),
        "parent_result_sha256": _sha256(parent_result),
        "artifact_sha256": {
            "engine": _sha256(actual_bin), "torch": _sha256(actual_pt),
            "manifest": _sha256(artifacts / "artifact_manifest.json")},
        "data_sha256": {"train": _sha256(train_source),
                        "validation": _sha256(validation_source), **observed_views},
        "device": args.device,
    }

    result["D0"] = _d0(actual_bin, actual_pt, exchanges)
    if not result["D0"]["gate"]:
        result["verdict"] = "INVALID-D0-DECODER-BISIMULATION"
        result["next_allowed_step"] = "Repair the shared serializer/decode path; do not interpret D1-D6."
        Path(args.result).write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n",
                                     encoding="utf-8")
        return 4

    actual_model = _load_resume_torch(actual_pt, args.device)
    actual_traces = [_teacher_trace(actual_model, prompt, target, args.device)
                     for prompt, target in exchanges]
    actual_free = _score_checkpoint(actual_bin, exchanges, bars, args.device)
    result["D1"] = {"teacher": _aggregate_trace(actual_traces),
                    "free": actual_free["counts"], "rows": actual_free["rows"]}

    ladder = {}
    ladder_paths = {}
    for count in protocol["diagnostics"]["D2"]["document_counts"]:
        documents = train_documents[:count]
        repetitions = 4 if count == 1 else 1
        train_path = work / f"ladder_{count}.train.txt"
        train_path.write_bytes(parent._view_bytes(documents * repetitions))
        name = f"ladder_{count}_turn"
        summary = _train(protocol, work, name, train_path, validation_path,
                         "turn-only", args.device, checkpoints=(count == 100))
        checkpoint = work / f"{name}.bin"
        probes = [exchange for document in documents
                  if (exchange := parent._final_exchange(document)) is not None][:8]
        scored = _score_checkpoint(checkpoint, probes, bars, args.device)
        ladder[str(count)] = {
            "unique_documents": count,
            "materialized_repetitions": repetitions,
            "train_view_sha256": _sha256(train_path),
            "summary": summary,
            "score": scored,
        }
        ladder_paths[count] = checkpoint
    result["D2"] = ladder

    train100_path = work / "ladder_100.train.txt"
    objective = {"turn-only": ladder["100"]}
    objective_paths = {"turn-only": ladder_paths[100]}
    for mode in ("full", "additive"):
        name = f"objective_100_{mode}"
        summary = _train(protocol, work, name, train100_path, validation_path,
                         mode, args.device, checkpoints=False)
        checkpoint = work / f"{name}.bin"
        objective[mode] = {"summary": summary,
                           "score": _score_checkpoint(checkpoint, exchanges, bars, args.device)}
        objective_paths[mode] = checkpoint
    result["D3"] = objective

    result["D4"] = {mode: _prompt_intervention(path, exchanges, bars, args.device)
                    for mode, path in objective_paths.items()}
    d5 = {}
    validation_exchanges = [v1._exchange(document) for document in val32]
    for mode, checkpoint in objective_paths.items():
        model = _load_engine_torch(checkpoint, args.device)
        turn_rows = [_teacher_trace_seed(model, seed, target, args.device)
                     for seed, target in validation_exchanges]
        d5[mode] = {"full": _validation_full_ce(model, val32, args.device),
                    "assistant_turn": _aggregate_trace(turn_rows)}
    result["D5"] = d5

    chronology = {}
    base = work / "ladder_100_turn"
    for step in protocol["diagnostics"]["D6"]["steps"]:
        checkpoint = _checkpoint_path(base, step)
        chronology[str(step)] = _score_checkpoint(checkpoint, exchanges, bars, args.device)
    result["D6"] = chronology

    d1_low = result["D1"]["teacher"]["top1_accuracy"] < 0.80
    full_support = any(
        objective[mode]["score"]["teacher"]["top1_accuracy"] >= 0.80
        and objective[mode]["score"]["counts"]["target_recovered"] >= 6
        and objective[mode]["score"]["counts"]["structural"] == 8
        for mode in ("full", "additive"))
    turn_support = (
        objective["turn-only"]["score"]["teacher"]["top1_accuracy"] >= 0.80
        and objective["turn-only"]["score"]["counts"]["target_recovered"] >= 6)
    result["classification"] = {
        "actual_checkpoint_underlearned": d1_low,
        "full_ce_curriculum_supported": full_support and not turn_support,
        "prompt_conditioning_by_arm": {mode: value["gate"]
                                       for mode, value in result["D4"].items()},
        "posthoc_checkpoint_promotion_forbidden": True,
    }
    if d1_low:
        verdict = "DIAGNOSED-TEACHER-FORCED-UNDERLEARNING"
    elif result["D1"]["free"]["target_recovered"] < 6:
        verdict = "DIAGNOSED-AUTOREGRESSIVE-ROLLOUT-FAILURE"
    else:
        verdict = "DIAGNOSTICS-PASS-MOUTH-CAUSE-NOT-REPRODUCED"
    result["verdict"] = verdict
    result["next_allowed_step"] = (
        "Use the frozen D2-D6 evidence to preregister one root-cause treatment; "
        "303M, IIT coupling and production remain blocked.")
    Path(args.result).write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n",
                                 encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
