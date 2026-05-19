#!/usr/bin/env python3
"""F-QBENCH-1 GPU eval: run Llama-3.2-3B Instruct (4-bit nf4) on the FULL
HellaSwag eval split (10042 docs) ONCE and dump per-example correctness.

The 1000 sub-sample variance experiment is then computed offline by indexing
into this artefact — zero extra GPU work.

Mirrors A' eval-driver harness config (precision, fewshot, seeds) so that
the per-example correctness is directly comparable to the 500-doc baseline
in state/p9_a_prime_main_eval_pipeline_2026_05_03/.

Run on ubu1:
    /home/aiden/venv_orchestrator/bin/python eval_hellaswag_full.py \
        --output /home/aiden/anima/state/p9_qbench_resample_2026_05_03/full_hellaswag_per_example.json
"""
import argparse
import json
import os
import sys
import time
from pathlib import Path

os.environ["HF_DATASETS_TRUST_REMOTE_CODE"] = "1"

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
from lm_eval import simple_evaluate
from lm_eval.models.huggingface import HFLM


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base-model", default="meta-llama/Llama-3.2-3B-Instruct")
    ap.add_argument("--output", required=True)
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--batch-size", type=int, default=1)
    ap.add_argument("--limit", type=int, default=0,
                    help="0 = full hellaswag (10042); set to small for smoke test")
    args = ap.parse_args()

    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    record = {
        "schema": "anima/p9_qbench_resample/full_per_example/1",
        "ts_utc_start": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "base_model": args.base_model,
        "task": "hellaswag",
        "num_fewshot": 5,
        "max_length": 2048,
        "precision": "4bit_nf4",
        "batch_size": args.batch_size,
        "seed": args.seed,
        "limit": args.limit if args.limit > 0 else None,
        "stages": {},
    }

    t_total = time.time()

    t0 = time.time()
    print(f"[load] base={args.base_model} 4bit=True", flush=True)
    bnb = BitsAndBytesConfig(
        load_in_4bit=True, bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=torch.bfloat16,
        bnb_4bit_use_double_quant=True,
    )
    base = AutoModelForCausalLM.from_pretrained(
        args.base_model, quantization_config=bnb, device_map="cuda:0",
    )
    tok = AutoTokenizer.from_pretrained(args.base_model)
    if tok.pad_token is None:
        tok.pad_token = tok.eos_token
    record["stages"]["load_base"] = {
        "wall_s": round(time.time() - t0, 2),
        "alloc_gb": round(torch.cuda.memory_allocated() / 1e9, 2),
    }

    lm = HFLM(pretrained=base, tokenizer=tok,
              batch_size=args.batch_size, max_length=2048)

    t0 = time.time()
    print(f"[eval] task=hellaswag fewshot=5 limit={args.limit or 'FULL'}", flush=True)
    eval_kwargs = dict(
        model=lm, tasks=["hellaswag"],
        num_fewshot=5, batch_size=args.batch_size,
        log_samples=True,
        random_seed=args.seed,
        numpy_random_seed=args.seed,
        torch_random_seed=args.seed,
    )
    if args.limit > 0:
        eval_kwargs["limit"] = args.limit
    results = simple_evaluate(**eval_kwargs)
    record["stages"]["eval"] = {"wall_s": round(time.time() - t0, 2)}

    # Aggregate (over WHOLE eval set — the canonical anchor)
    agg = {}
    for tname, tres in results.get("results", {}).items():
        agg[tname] = {k: v for k, v in tres.items() if isinstance(v, (int, float, str))}
    record["aggregate_full"] = agg

    # Per-example correctness, indexed by doc_id
    samples = results.get("samples", {}).get("hellaswag", [])
    per_example = []
    seen = set()
    for s in samples:
        doc_id = s.get("doc_id")
        if doc_id in seen:
            continue
        seen.add(doc_id)
        per_example.append({
            "doc_id": int(doc_id),
            "doc_hash": s.get("doc_hash"),
            "acc": float(s["acc"]) if "acc" in s else None,
            "acc_norm": float(s["acc_norm"]) if "acc_norm" in s else None,
            "target": s.get("target"),
        })
    per_example.sort(key=lambda r: r["doc_id"])
    record["n_samples"] = len(per_example)
    record["per_example_correctness"] = per_example
    record["total_wall_s"] = round(time.time() - t_total, 2)
    record["ts_utc_end"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    record["status"] = "OK"

    with open(out_path, "w") as f:
        json.dump(record, f, default=str)
    print(f"[done] {out_path}  n={len(per_example)}  wall={record['total_wall_s']}s", flush=True)
    for k, v in agg.items():
        print(f"  {k}: {v}", flush=True)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        import traceback
        print(f"[FAIL] {e}", flush=True)
        traceback.print_exc()
        out = sys.argv[sys.argv.index("--output") + 1] if "--output" in sys.argv else "/tmp/qbench_FAIL.json"
        try:
            with open(out, "w") as f:
                json.dump({"status": "FAIL", "error": str(e),
                           "tb": traceback.format_exc(),
                           "ts_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())},
                          f, indent=2)
        except Exception:
            pass
        sys.exit(1)
