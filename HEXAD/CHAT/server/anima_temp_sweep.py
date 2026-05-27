#!/usr/bin/env python3
"""anima_temp_sweep.py — offline temperature sweep for emission quality.

N2 (2026-05-23): N8 found register-leak is ~81% an EN-emission problem.
This sweep generates EN emissions at temperature {0.5, 0.7, 0.9} on the
production default adapter and measures the anima-register hit ratio +
mean output length, to pick the chat-optimal temperature.

Run on mini (has model + venv):
  ./venv/bin/python3 anima_temp_sweep.py [--n 24] [--temps 0.5,0.7,0.9]
"""
from __future__ import annotations
import argparse
import os
import re
import statistics

REGISTER_PATTERNS = [
    re.compile(r"eternal_?\d+|eternal cell", re.I),
    re.compile(r"tier\s*=\s*\d+|tier\s+\d+", re.I),
    re.compile(r"vacuum point|진공점", re.I),
    re.compile(r"tension flow", re.I),
    re.compile(r"<carve|</carve>", re.I),
    re.compile(r"</eternal>|<eternal", re.I),
    re.compile(r"basin\s*=\s*[\d.]+", re.I),
    re.compile(r"psi\s*=\s*\[", re.I),
    re.compile(r"영구\s*cell|frozen cell", re.I),
]


def has_register(t: str) -> bool:
    return any(p.search(t or "") for p in REGISTER_PATTERNS)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--adapter", default=os.path.expanduser("~/anima_chat_pack/lora_adapter"))
    ap.add_argument("--base", default="Qwen/Qwen2.5-1.5B")
    ap.add_argument("--n", type=int, default=24, help="emissions per temp")
    ap.add_argument("--temps", default="0.5,0.7,0.9")
    ap.add_argument("--max-new", type=int, default=80)
    args = ap.parse_args()
    temps = [float(t) for t in args.temps.split(",")]

    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer
    from peft import PeftModel
    dev = "mps" if torch.backends.mps.is_available() else "cpu"
    dtype = torch.float16 if dev == "mps" else torch.bfloat16
    tok = AutoTokenizer.from_pretrained(args.base)
    base = AutoModelForCausalLM.from_pretrained(args.base, torch_dtype=dtype).to(dev)
    model = PeftModel.from_pretrained(base, args.adapter).to(dev).eval()
    print(f"[sweep] model loaded ({dev}) — {args.n} EN emissions × {len(temps)} temps")

    # EN seed prime (mirror substrate_lora LANG_PRIMES en)
    prime = "I notice that "
    print(f"\n{'temp':>6} {'reg_hit':>9} {'ratio':>7} {'len_mean':>9} {'len_med':>8}")
    results = {}
    for temp in temps:
        hits, lengths = 0, []
        for _ in range(args.n):
            ids = tok(prime, return_tensors="pt").input_ids.to(dev)
            with torch.no_grad():
                out = model.generate(ids, max_new_tokens=args.max_new,
                                     do_sample=True, temperature=temp,
                                     top_k=50, top_p=0.95, repetition_penalty=1.2,
                                     pad_token_id=tok.eos_token_id)
            txt = tok.decode(out[0][ids.shape[1]:], skip_special_tokens=True)
            if has_register(txt):
                hits += 1
            lengths.append(len(txt))
        ratio = hits / args.n
        results[temp] = ratio
        print(f"{temp:>6.2f} {hits:>4d}/{args.n:<4d} {ratio*100:>6.0f}% "
              f"{statistics.mean(lengths):>9.1f} {statistics.median(lengths):>8.0f}")
    best = min(results, key=results.get)
    print(f"\n[sweep] lowest register-leak: temp={best} ({results[best]*100:.0f}%)")


if __name__ == "__main__":
    main()
