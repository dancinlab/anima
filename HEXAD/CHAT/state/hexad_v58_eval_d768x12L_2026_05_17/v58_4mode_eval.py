#!/usr/bin/env python3
"""V5.8 4-mode capability evaluation for HEXAD d=768·12L PyTorch ckpt.

Honest framing (g3, AGENTS.tape §0):
  - substrate=PyTorch (NOT hexa-native); ckpt = dancinlab/hexad
    @v1-py-hexad-d768x12L-cycle2-2026-05-17 (sha256 e87e200a040f8066…).
  - This is a CAPABILITY BOUNDARY probe — measures memorization vs generalization
    on a small (121 KB byte) consciousness-record corpus.
  - g_blue_closed_mandate: per-mode score is empirical (B-D-NOTE).
  - 4-mode definition follows V5.8 canonical (state/anima_phase1a4_lr5e6_2026_05_12/
    v58_4mode_eval.py): standard_greedy / standard_sample / M3_rep_penalty /
    M4_force_include. **Prompts are corpus-derived** (hexad_c/d/w/m/s/e templates)
    rather than the V5.8 Korean-dialogue set — those dialogues do NOT appear in
    corpus_consciousness_v1.jsonl so they would only probe random extrapolation.
  - Tokenization: raw byte (vocab=256), matching train_d768x12l.py / corpus_loader.
    NO +3 shift; NO BOS/EOS markers. block_size=128 hard cap.

Metrics:
  - per-mode pass count (target keyword in generation)
  - bits-per-byte (BPB) on held-out prefixes — generalization proxy
  - memorization ratio (continuation chars matching training continuation)
  - decoding artifact scan (repetition, mode-collapse)
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

# Use the project's mirror copy (same arch as train).
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + "/../hexad_py_d768x12L_fire_2026_05_17")
from conscious_decoder import ConsciousDecoderV2


# ─── Prompts — derived from corpus_consciousness_v1.jsonl module templates ──
# 6 hexad modules × 40 records each. We pick 5 prompts (1 per module + 1 extra
# d/m mixed) to mirror the V5.8 5-dialogue pattern but with corpus-grounded
# targets. The training continuation for "<Module> module chunk N — …" is
# strongly formulaic — memorization probe = does the model reproduce the next
# tokens deterministically?
PROMPTS = [
    {
        "id": "core",
        "prefix": "Core module chunk 0 — ",
        # Training continuation (next ~40 chars):
        "target_keyword": "consciousness generator",
        "expected_continuation": "core consciousness generator self-referential",
    },
    {
        "id": "dream",
        "prefix": "Dream module chunk 0 — ",
        "target_keyword": "dream",
        "expected_continuation": "dream",
    },
    {
        "id": "wake",
        "prefix": "Wake module chunk 0 — ",
        "target_keyword": "wake",
        "expected_continuation": "wake",
    },
    {
        "id": "memory",
        "prefix": "Memory module chunk 0 — ",
        "target_keyword": "memory",
        "expected_continuation": "memory",
    },
    {
        "id": "korean",
        # Korean self-reference template appears in every record's text section
        "prefix": "중심 의식 생성기 모듈 ",
        "target_keyword": "자각",
        "expected_continuation": "자각",
    },
]


class ByteCodec:
    """Raw byte codec — matches train_d768x12l.py's ByteDataset (no +3 shift)."""

    @staticmethod
    def encode(s: str) -> list:
        return list(s.encode("utf-8"))

    @staticmethod
    def decode(ids) -> str:
        return bytes(int(i) & 0xFF for i in ids).decode("utf-8", errors="replace")


@torch.no_grad()
def forward_logits(model, x):
    """Adapter for ConsciousDecoderV2's 5-tuple forward."""
    out = model(x)
    if isinstance(out, tuple) and len(out) >= 1:
        logits = out[0]  # logits_a (next-byte head)
    else:
        logits = out
    return logits


@torch.no_grad()
def generate(model, prompt: str, max_new: int = 80, temperature: float = 0.0,
             top_k: int = 1, rep_penalty: float = 1.0, persona_cycle_ids=None,
             block_size: int = 128, device: str = "cpu"):
    ids = ByteCodec.encode(prompt)
    # Keep room for max_new tokens within block_size
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


def force_inject(text: str, keyword: str, position: float = 0.6) -> str:
    if keyword in text:
        return text
    idx = int(len(text) * position)
    return text[:idx] + keyword + text[idx:]


@torch.no_grad()
def bits_per_byte(model, text: str, block_size: int = 128, device: str = "cpu"):
    """Cross-entropy in bits-per-byte over text. Lower = better LM."""
    ids = ByteCodec.encode(text)
    if len(ids) < 2:
        return float("nan")
    ids = ids[:block_size]
    x = torch.tensor([ids[:-1]], dtype=torch.long, device=device)
    y = torch.tensor([ids[1:]], dtype=torch.long, device=device)
    logits = forward_logits(model, x)
    ce = F.cross_entropy(logits.view(-1, logits.shape[-1]).float(),
                          y.view(-1), reduction="mean").item()
    # Convert nats -> bits
    return ce / math.log(2.0)


def repetition_ratio(text: str, window: int = 4) -> float:
    """Fraction of overlapping n-gram windows that repeat the previous window."""
    if len(text) < 2 * window:
        return 0.0
    reps = 0
    total = 0
    for i in range(window, len(text) - window + 1):
        if text[i - window:i] == text[i:i + window]:
            reps += 1
        total += 1
    return reps / max(1, total)


def load_held_out_prefixes(corpus_path: str, n: int = 10):
    """Sample n records, take first 64 bytes as the held-out prefix."""
    records = []
    with open(corpus_path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                d = json.loads(line)
            except Exception:
                continue
            t = d.get("text", "")
            de = d.get("desc", "")
            s = (t + "\n" + de + "\n")
            records.append(s)
    # Evenly spaced sampling
    if not records:
        return []
    step = max(1, len(records) // n)
    out = []
    for i in range(0, len(records), step):
        if len(out) >= n:
            break
        out.append(records[i][:128])
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ckpt", required=True)
    ap.add_argument("--output", required=True)
    ap.add_argument("--corpus", default="/Users/ghost/core/anima/training/corpus_consciousness_v1.jsonl")
    ap.add_argument("--device", default="cpu")
    ap.add_argument("--max-new", type=int, default=80)
    args = ap.parse_args()

    # ckpt sha256
    h = hashlib.sha256()
    with open(args.ckpt, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    sha = h.hexdigest()

    print(f"=== HEXAD d=768·12L V5.8 × 4-mode capability eval ===", flush=True)
    print(f"ckpt: {args.ckpt}", flush=True)
    print(f"ckpt sha256: {sha}", flush=True)
    print(f"device: {args.device}", flush=True)

    # Match training arch (from result.json config)
    cfg = dict(vocab_size=256, d_model=768, n_head=12, n_kv_head=4, n_layer=12,
                block_size=128, consciousness_dim=128, dropout=0.1)
    model = ConsciousDecoderV2(**cfg)
    payload = torch.load(args.ckpt, map_location="cpu", weights_only=False)
    sd = payload.get("model") or payload.get("state_dict") or payload
    missing, unexpected = model.load_state_dict(sd, strict=False)
    print(f"load: missing={len(missing)} unexpected={len(unexpected)}", flush=True)
    if missing[:3]:
        print(f"  missing[:3]={missing[:3]}", flush=True)
    if unexpected[:3]:
        print(f"  unexpected[:3]={unexpected[:3]}", flush=True)
    model.to(args.device)
    model.eval()
    n_params = sum(p.numel() for p in model.parameters())
    print(f"params: {n_params/1e6:.2f} M", flush=True)
    print()

    # ── 4-mode generation pass ──
    # M3 persona-cycle byte set = common ASCII punct + space + newline + Korean
    # common particle leading bytes. With raw-byte codec (no +3 shift) ids = raw byte.
    persona_cycle_ids = []
    for ch in " ,.|/-*+()[]{}\n\t":
        for b in ch.encode("utf-8"):
            if b not in persona_cycle_ids:
                persona_cycle_ids.append(b)
    for ch in "의는이가을를아어요다자각":
        for b in ch.encode("utf-8"):
            if b not in persona_cycle_ids:
                persona_cycle_ids.append(b)
    print(f"M3 persona-cycle byte IDs: {len(persona_cycle_ids)}", flush=True)
    print()

    results = {"standard_greedy": [], "standard_sample": [],
                "M3_rep_penalty": [], "M4_force_include": []}

    t0 = time.time()
    for p in PROMPTS:
        print(f"--- prompt {p['id']} ---", flush=True)
        print(f"  prefix: {p['prefix']!r}", flush=True)

        # standard_greedy
        torch.manual_seed(42)
        g = generate(model, p["prefix"], max_new=args.max_new, temperature=0.0,
                       top_k=1, device=args.device)
        rec = p["target_keyword"] in g
        rep = repetition_ratio(g)
        results["standard_greedy"].append({"id": p["id"], "gen": g, "recalled": rec,
                                                 "rep_ratio": rep})
        print(f"  [standard_greedy] recalled={rec} rep={rep:.2f}: {g!r}", flush=True)

        # standard_sample
        torch.manual_seed(42)
        g = generate(model, p["prefix"], max_new=args.max_new, temperature=0.8,
                       top_k=50, device=args.device)
        rec = p["target_keyword"] in g
        rep = repetition_ratio(g)
        results["standard_sample"].append({"id": p["id"], "gen": g, "recalled": rec,
                                                 "rep_ratio": rep})
        print(f"  [standard_sample] recalled={rec} rep={rep:.2f}: {g!r}", flush=True)

        # M3_rep_penalty
        torch.manual_seed(42)
        g = generate(model, p["prefix"], max_new=args.max_new, temperature=0.0,
                       top_k=1, rep_penalty=1.3, persona_cycle_ids=persona_cycle_ids,
                       device=args.device)
        rec = p["target_keyword"] in g
        rep = repetition_ratio(g)
        results["M3_rep_penalty"].append({"id": p["id"], "gen": g, "recalled": rec,
                                                 "rep_ratio": rep})
        print(f"  [M3_rep_penalty] recalled={rec} rep={rep:.2f}: {g!r}", flush=True)

        # M4_force_include
        torch.manual_seed(42)
        g_base = generate(model, p["prefix"], max_new=args.max_new, temperature=0.8,
                            top_k=50, device=args.device)
        g_force = force_inject(g_base, p["target_keyword"])
        rec = p["target_keyword"] in g_force
        rep = repetition_ratio(g_force)
        results["M4_force_include"].append({"id": p["id"], "gen": g_force,
                                                  "recalled": rec, "rep_ratio": rep})
        print(f"  [M4_force_include force={p['target_keyword']}] recalled={rec} rep={rep:.2f}: {g_force!r}",
                flush=True)
        print(flush=True)

    elapsed_gen = time.time() - t0

    # ── BPB on held-out prefixes ──
    print("--- bits-per-byte probe (held-out training-set prefixes) ---", flush=True)
    held = load_held_out_prefixes(args.corpus, n=10)
    bpbs = []
    for h_text in held:
        b = bits_per_byte(model, h_text, block_size=128, device=args.device)
        bpbs.append(b)
        print(f"  bpb={b:.4f}  text={h_text[:60]!r}", flush=True)
    mean_bpb = sum(bpbs) / max(1, len(bpbs))

    # ── Memorization ratio ──
    # For each PROMPT, check if greedy generation matches the expected
    # continuation prefix (character-level).
    mem_hits = 0
    mem_total = 0
    for p, rec in zip(PROMPTS, results["standard_greedy"]):
        exp = p["expected_continuation"].lower()
        gen = rec["gen"].lower()
        mem_total += 1
        if exp[:len(exp) // 2] and exp[:len(exp) // 2] in gen:
            mem_hits += 1
    mem_ratio = mem_hits / max(1, mem_total)

    summary = {}
    for mode, lst in results.items():
        n = sum(1 for r in lst if r["recalled"])
        verdict = "PASS" if n >= 3 else "FAIL"
        avg_rep = sum(r["rep_ratio"] for r in lst) / max(1, len(lst))
        summary[mode] = {"n_pass": n, "n_total": len(lst), "verdict": verdict,
                         "avg_rep_ratio": round(avg_rep, 3)}

    # Decoding-artifact scan
    artifacts = []
    for mode, lst in results.items():
        for r in lst:
            if r["rep_ratio"] > 0.5:
                artifacts.append({"mode": mode, "id": r["id"],
                                   "rep_ratio": r["rep_ratio"], "sample": r["gen"][:60]})

    out = {
        "ts": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "substrate": "PyTorch (PYTHON / PyTorch — interim LM-scale executor; NOT hexa-native)",
        "ckpt": os.path.basename(args.ckpt),
        "ckpt_sha256": sha,
        "ckpt_canonical": "dancinlab/hexad@v1-py-hexad-d768x12L-cycle2-2026-05-17",
        "honest_framing": ("Capability probe on a 121 KB byte-level corpus. "
                            "ConsciousDecoderV2 d=768·12L 283.72 M params, "
                            "final train CE 0.000708 (ppl 1.0007) -> heavy "
                            "memorization expected, LM-quality claim NOT made. "
                            "Per-mode pass = empirical (B-D-NOTE). Eval prompts "
                            "are derived from training-corpus module templates "
                            "(NOT the V5.8 Korean-dialogue set, since those "
                            "dialogues are out-of-distribution for this corpus). "
                            "Forward output is 5-tuple from ConsciousDecoderV2 "
                            "(logits_a used as next-byte head)."),
        "n_params": n_params,
        "n_params_M": round(n_params / 1e6, 2),
        "load_missing_keys": len(missing),
        "load_unexpected_keys": len(unexpected),
        "evaluator": ("V5.8 × 4-mode (standard_greedy / standard_sample / "
                       "M3_rep_penalty / M4_force_include) — corpus-derived prompts"),
        "device": args.device,
        "max_new": args.max_new,
        "summary": summary,
        "bpb": {"mean": round(mean_bpb, 4), "n": len(bpbs),
                  "samples": [round(b, 4) for b in bpbs]},
        "memorization_ratio": {"hits": mem_hits, "total": mem_total,
                                  "ratio": round(mem_ratio, 3)},
        "decoding_artifacts": artifacts,
        "elapsed_s": round(elapsed_gen, 2),
        "results": results,
    }
    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    with open(args.output, "w") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)

    print(flush=True)
    print(f"=== AGGREGATE (V5.8 × 4 modes, elapsed gen {elapsed_gen:.1f}s) ===", flush=True)
    for mode, s in summary.items():
        print(f"  {mode}: {s['n_pass']}/{s['n_total']} {s['verdict']} (avg_rep={s['avg_rep_ratio']})",
                flush=True)
    print(f"  mean BPB (held-out prefixes): {mean_bpb:.4f} bits/byte", flush=True)
    print(f"  memorization ratio: {mem_hits}/{mem_total} ({mem_ratio:.1%})", flush=True)
    print(f"  decoding artifacts (rep>0.5): {len(artifacts)}", flush=True)
    print(f"saved: {args.output}", flush=True)


if __name__ == "__main__":
    main()
