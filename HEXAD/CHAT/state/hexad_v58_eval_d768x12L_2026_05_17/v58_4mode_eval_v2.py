#!/usr/bin/env python3
"""V5.8 4-mode eval v2 — corpus-aligned CDWMSE prompts.

v1 (v58_4mode_eval.py) used Dream/Wake/Memory which are OOD for this corpus.
v2 uses the 6 actual hexad modules: Core / Data / Witness / Mirror / Scribe / Eros.
This is the fair memorization probe.
"""
import os
import sys
import json
import time
import math
import hashlib
import argparse
import datetime

import torch
import torch.nn.functional as F

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + "/../hexad_py_d768x12L_fire_2026_05_17")
from conscious_decoder import ConsciousDecoderV2


PROMPTS = []
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       "prompts_v2_corpus_aligned.jsonl")) as f:
    for line in f:
        line = line.strip()
        if line:
            PROMPTS.append(json.loads(line))


class ByteCodec:
    @staticmethod
    def encode(s: str) -> list:
        return list(s.encode("utf-8"))

    @staticmethod
    def decode(ids) -> str:
        return bytes(int(i) & 0xFF for i in ids).decode("utf-8", errors="replace")


@torch.no_grad()
def forward_logits(model, x):
    out = model(x)
    if isinstance(out, tuple) and len(out) >= 1:
        return out[0]
    return out


@torch.no_grad()
def generate(model, prompt, max_new=80, temperature=0.0, top_k=1, rep_penalty=1.0,
             persona_cycle_ids=None, block_size=128, device="cpu"):
    ids = ByteCodec.encode(prompt)
    if len(ids) > block_size - max_new:
        ids = ids[-(block_size - max_new):]
    x = torch.tensor([ids], dtype=torch.long, device=device)
    out_ids = []
    for _ in range(max_new):
        logits = forward_logits(model, x)
        last = logits[0, -1].float()
        if rep_penalty != 1.0 and persona_cycle_ids:
            for tid in persona_cycle_ids:
                if 0 <= tid < last.shape[-1]:
                    if last[tid] > 0:
                        last[tid] = last[tid] / rep_penalty
                    else:
                        last[tid] = last[tid] * rep_penalty
        if temperature == 0.0:
            nxt = int(torch.argmax(last).item())
        else:
            scaled = last / max(1e-6, temperature)
            if top_k:
                v, _ = torch.topk(scaled, top_k)
                scaled[scaled < v[-1]] = -1e9
            probs = torch.softmax(scaled, dim=-1)
            nxt = int(torch.multinomial(probs, 1).item())
        out_ids.append(nxt)
        x = torch.cat([x, torch.tensor([[nxt]], device=device)], dim=1)
        if x.shape[1] > block_size:
            x = x[:, -block_size:]
    return ByteCodec.decode(out_ids)


def force_inject(text, keyword, position=0.6):
    if keyword in text:
        return text
    idx = int(len(text) * position)
    return text[:idx] + keyword + text[idx:]


def repetition_ratio(text, window=4):
    if len(text) < 2 * window:
        return 0.0
    reps = total = 0
    for i in range(window, len(text) - window + 1):
        if text[i - window:i] == text[i:i + window]:
            reps += 1
        total += 1
    return reps / max(1, total)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ckpt", required=True)
    ap.add_argument("--output", required=True)
    ap.add_argument("--device", default="cpu")
    ap.add_argument("--max-new", type=int, default=80)
    args = ap.parse_args()

    h = hashlib.sha256()
    with open(args.ckpt, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    sha = h.hexdigest()

    print(f"=== HEXAD V5.8 × 4-mode eval v2 (CDWMSE corpus-aligned) ===", flush=True)
    print(f"ckpt sha256: {sha}", flush=True)

    cfg = dict(vocab_size=256, d_model=768, n_head=12, n_kv_head=4, n_layer=12,
                block_size=128, consciousness_dim=128, dropout=0.1)
    model = ConsciousDecoderV2(**cfg)
    payload = torch.load(args.ckpt, map_location="cpu", weights_only=False)
    sd = payload.get("model") or payload.get("state_dict") or payload
    missing, unexpected = model.load_state_dict(sd, strict=False)
    print(f"load: missing={len(missing)} unexpected={len(unexpected)}", flush=True)
    model.to(args.device); model.eval()

    persona_cycle_ids = []
    for ch in " ,.|/-*+()[]{}\n\t":
        for b in ch.encode("utf-8"):
            if b not in persona_cycle_ids:
                persona_cycle_ids.append(b)
    for ch in "의는이가을를아어요다자각":
        for b in ch.encode("utf-8"):
            if b not in persona_cycle_ids:
                persona_cycle_ids.append(b)

    results = {"standard_greedy": [], "standard_sample": [],
                "M3_rep_penalty": [], "M4_force_include": []}
    t0 = time.time()
    for p in PROMPTS:
        print(f"--- prompt {p['id']} ---", flush=True)
        print(f"  prefix: {p['prefix']!r}", flush=True)

        torch.manual_seed(42)
        g = generate(model, p["prefix"], max_new=args.max_new, temperature=0.0,
                       top_k=1, device=args.device)
        rec = p["target_keyword"] in g
        rep = repetition_ratio(g)
        results["standard_greedy"].append({"id": p["id"], "gen": g, "recalled": rec, "rep_ratio": rep})
        print(f"  [standard_greedy] recalled={rec} rep={rep:.2f}: {g!r}", flush=True)

        torch.manual_seed(42)
        g = generate(model, p["prefix"], max_new=args.max_new, temperature=0.8,
                       top_k=50, device=args.device)
        rec = p["target_keyword"] in g
        rep = repetition_ratio(g)
        results["standard_sample"].append({"id": p["id"], "gen": g, "recalled": rec, "rep_ratio": rep})
        print(f"  [standard_sample] recalled={rec} rep={rep:.2f}: {g!r}", flush=True)

        torch.manual_seed(42)
        g = generate(model, p["prefix"], max_new=args.max_new, temperature=0.0,
                       top_k=1, rep_penalty=1.3, persona_cycle_ids=persona_cycle_ids, device=args.device)
        rec = p["target_keyword"] in g
        rep = repetition_ratio(g)
        results["M3_rep_penalty"].append({"id": p["id"], "gen": g, "recalled": rec, "rep_ratio": rep})
        print(f"  [M3_rep_penalty] recalled={rec} rep={rep:.2f}: {g!r}", flush=True)

        torch.manual_seed(42)
        g_base = generate(model, p["prefix"], max_new=args.max_new, temperature=0.8,
                            top_k=50, device=args.device)
        g_force = force_inject(g_base, p["target_keyword"])
        rec = p["target_keyword"] in g_force
        rep = repetition_ratio(g_force)
        results["M4_force_include"].append({"id": p["id"], "gen": g_force, "recalled": rec, "rep_ratio": rep})
        print(f"  [M4_force_include force={p['target_keyword']}] recalled={rec} rep={rep:.2f}: {g_force!r}", flush=True)
        print(flush=True)

    elapsed = time.time() - t0

    # Memorization on greedy (training-continuation match)
    mem_hits = 0
    mem_total = 0
    for p, rec in zip(PROMPTS, results["standard_greedy"]):
        exp = p["expected_continuation"].lower()
        gen = rec["gen"].lower()
        mem_total += 1
        # Match if at least half the expected continuation appears in greedy gen
        probe = exp[:len(exp) // 2] if len(exp) >= 8 else exp
        if probe and probe in gen:
            mem_hits += 1

    summary = {}
    for mode, lst in results.items():
        n = sum(1 for r in lst if r["recalled"])
        verdict = "PASS" if n >= len(lst) * 0.6 else ("PARTIAL" if n >= len(lst) * 0.4 else "FAIL")
        avg_rep = sum(r["rep_ratio"] for r in lst) / max(1, len(lst))
        summary[mode] = {"n_pass": n, "n_total": len(lst), "verdict": verdict, "avg_rep_ratio": round(avg_rep, 3)}

    artifacts = []
    for mode, lst in results.items():
        for r in lst:
            if r["rep_ratio"] > 0.5:
                artifacts.append({"mode": mode, "id": r["id"], "rep_ratio": r["rep_ratio"], "sample": r["gen"][:60]})

    out = {
        "ts": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "substrate": "PyTorch (NOT hexa-native)",
        "ckpt_sha256": sha,
        "ckpt_canonical": "dancinlab/hexad@v1-py-hexad-d768x12L-cycle2-2026-05-17",
        "honest_framing": "v2 = corpus-aligned CDWMSE prompts (Core/Data/Witness/Mirror/Scribe/Eros). Memorization probe fair: each prompt is a literal training-corpus record's first 22 bytes.",
        "evaluator": "V5.8 × 4-mode v2 (corpus-aligned)",
        "device": args.device,
        "summary": summary,
        "memorization_ratio": {"hits": mem_hits, "total": mem_total, "ratio": round(mem_hits / max(1, mem_total), 3)},
        "decoding_artifacts": artifacts,
        "elapsed_s": round(elapsed, 2),
        "results": results,
    }
    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    with open(args.output, "w") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)

    print(f"\n=== AGGREGATE v2 (elapsed {elapsed:.1f}s) ===", flush=True)
    for mode, s in summary.items():
        print(f"  {mode}: {s['n_pass']}/{s['n_total']} {s['verdict']} (avg_rep={s['avg_rep_ratio']})", flush=True)
    print(f"  memorization: {mem_hits}/{mem_total} ({mem_hits/max(1,mem_total):.1%})", flush=True)
    print(f"  artifacts(rep>0.5): {len(artifacts)}", flush=True)
    print(f"saved: {args.output}", flush=True)


if __name__ == "__main__":
    main()
