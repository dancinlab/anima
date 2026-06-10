#!/usr/bin/env python3
"""chat_eval_only_7b.py — re-run the p7 eval (with the fixed turn-stopping) against an
already-saved ByteGPT ckpt, plus the anti-Goodhart BEFORE control on the wiki backbone.
No training. Reuses the evaluator from chat_finetune_7b_eval.py (single SSOT)."""
import argparse, json
from pathlib import Path
import torch

from chat_finetune_7b_eval import (ByteGPT, load_corpus, p7_eval, build_corpus_wordset)


def load_model(path, device):
    ck = torch.load(path, map_location="cpu", weights_only=False)
    cfg = ck["config"]
    m = ByteGPT(cfg["vocab"], cfg["d"], cfg["n_layer"], cfg["n_head"], cfg["block"], grad_ckpt=False).bfloat16()
    m.load_state_dict(ck["model"], strict=False)
    return m.to(device), cfg


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--backbone", required=True)
    ap.add_argument("--finetuned", required=True)
    ap.add_argument("--corpus", required=True)
    ap.add_argument("--out-dir", default="out")
    args = ap.parse_args()
    device = "cuda" if torch.cuda.is_available() else "cpu"
    out = Path(args.out_dir); out.mkdir(parents=True, exist_ok=True)

    wordset = build_corpus_wordset(args.corpus)
    print(f"[wordset] {len(wordset)} corpus assistant-side words", flush=True)

    bb, cfg = load_model(args.backbone, device)
    bs = cfg["block"]
    print("\n=== p7 BEFORE (backbone — anti-Goodhart control; MUST FAIL) ===", flush=True)
    before = p7_eval(bb, device, bs, "backbone_before_finetune", wordset)
    print(before["transcript"], flush=True)
    print(f"[before] verdict={before['verdict']} n_pass={before['n_pass']}/5", flush=True)
    del bb
    torch.cuda.empty_cache()

    ft, _ = load_model(args.finetuned, device)
    print("\n=== p7 AFTER (finetuned 7B — should PASS) ===", flush=True)
    after = p7_eval(ft, device, bs, "finetuned_7b", wordset)
    print(after["transcript"], flush=True)
    print(f"[after] verdict={after['verdict']} n_pass={after['n_pass']}/5", flush=True)

    summary = {
        "rung": "rung-7B (7.25B byte ByteGPT chat-finetune) — eval re-run (fixed turn-stopping)",
        "lane": "Lane-G/torch-cuda REFERENCE (a_lane_akida_gpu_split — NOT AKIDA)",
        "base_model": "dancinlab/clm-v1-ref-pytorch-cuda-7b",
        "corpus": "dancinlab/anima-chat-corpus-mix-70wiki-30dialogue",
        "before_backbone": {"verdict": before["verdict"], "n_pass": before["n_pass"]},
        "after_finetune": {"verdict": after["verdict"], "n_pass": after["n_pass"]},
        "anti_goodhart_ok": (after["verdict"] == "PASS" and before["verdict"] == "FAIL"),
        "chat_pass": (after["verdict"] == "PASS" and before["verdict"] == "FAIL"),
    }
    (out / "p7_before.json").write_text(json.dumps(before, ensure_ascii=False, indent=2))
    (out / "p7_after.json").write_text(json.dumps(after, ensure_ascii=False, indent=2))
    (out / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2))
    print("\n=== SUMMARY ===", flush=True)
    print(json.dumps(summary, ensure_ascii=False, indent=2), flush=True)


if __name__ == "__main__":
    main()
