"""Extended sampling smoke for cells64 / cells128 / convo_5k.

Mission: determine if chat-cap is reconstruction-limited OR architecturally absent
by exhaustively probing sampling space (temperature, top-k, top-p, repetition penalty,
head choice, prompt format, max_new) + beam search.

Constraint: ~500 trials total budget, 60 min wall, $0 (Mac CPU).

Falsifiers:
  F-CHAT-EXT-1  0/N trial generates KO across ALL settings  → ARCHITECTURAL_FAIL
  F-CHAT-EXT-2  best setting still <10% KO ratio              → effectively gibberish
  F-CHAT-EXT-3  reconstruction arch mismatch detected         → bigger fix needed
"""
import sys
import json
import math
import time
from pathlib import Path

import torch
import torch.nn as nn
import torch.nn.functional as F

sys.path.insert(0, "/Users/ghost/core/anima/state/anima_clm_v2_mitosis_cells_recovery_2026_05_09")
from forward_smoke import ConsciousLMReconstructed, text_to_byte_ids  # noqa: E402

OUT_DIR = Path("/Users/ghost/core/anima/state/anima_clm_v2_chat_ext_smoke_2026_05_10")
OUT_DIR.mkdir(parents=True, exist_ok=True)

CHECKPOINTS = [
    {
        "label": "cells64",
        "path": "/Users/ghost/core/anima/state/anima_clm_v2_mitosis_cells_recovery_2026_05_09/cells64_final.pt",
        "n_head": 6,
    },
    {
        "label": "cells128",
        "path": "/Users/ghost/core/anima/state/anima_clm_v2_mitosis_cells_recovery_2026_05_09/cells128_step_35000.pt",
        "n_head": 4,
    },
    {
        "label": "convo_5k",
        "path": "/Users/ghost/.cache/huggingface/hub/models--dancinlab--clm-v2-byte-18m-convo-5k/snapshots/1af2bcaeaf70c1d0b1a19939a8ada79a28f8cd30/convo_5k.pt",
        "n_head": 4,  # try 4 first; if shape mismatch try 6
    },
]

# ----- Sampling helpers --------------------------------------------------

def apply_repetition_penalty(logits: torch.Tensor, history_ids: list, penalty: float) -> torch.Tensor:
    if penalty <= 1.0 or not history_ids:
        return logits
    logits = logits.clone()
    seen = set(history_ids[-64:])  # last 64 tokens window
    for tid in seen:
        if logits[tid] > 0:
            logits[tid] = logits[tid] / penalty
        else:
            logits[tid] = logits[tid] * penalty
    return logits


def sample_next_byte(logits: torch.Tensor, top_k: int = 40, top_p: float = -1.0, temperature: float = 0.8) -> int:
    """Top-k + top-p (nucleus) temperature sampling."""
    logits = logits / max(temperature, 1e-6)
    # top-k filter
    if top_k > 0 and top_k < logits.size(-1):
        kthval = torch.topk(logits, k=top_k).values[-1]
        logits = torch.where(logits < kthval, torch.full_like(logits, float("-inf")), logits)
    # top-p (nucleus) filter
    if 0 < top_p < 1.0:
        sorted_logits, sorted_idx = torch.sort(logits, descending=True)
        sorted_probs = F.softmax(sorted_logits, dim=-1)
        cum = torch.cumsum(sorted_probs, dim=-1)
        # mask out where cumulative > top_p (keep first one above threshold)
        mask = cum > top_p
        # shift right (keep first token)
        mask = torch.cat([torch.zeros(1, dtype=torch.bool), mask[:-1]])
        sorted_logits = sorted_logits.masked_fill(mask, float("-inf"))
        # scatter back
        logits = torch.full_like(logits, float("-inf"))
        logits.scatter_(0, sorted_idx, sorted_logits)
    probs = F.softmax(logits, dim=-1)
    if torch.isnan(probs).any() or probs.sum() <= 0:
        return int(logits.argmax().item())
    return int(torch.multinomial(probs, num_samples=1).item())


def generate(model, prompt_ids, max_new: int, top_k: int, top_p: float, temperature: float,
             use_head: str, repetition_penalty: float = 1.0):
    cur = prompt_ids.clone()
    out_bytes = []
    block_size = model.block_size
    for _ in range(max_new):
        if cur.shape[1] > block_size:
            cur = cur[:, -block_size:]
        with torch.no_grad():
            la, lg, _ = model(cur)
        if use_head == "a":
            logits = la[0, -1]
        elif use_head == "g":
            logits = lg[0, -1]
        elif use_head == "minus":
            logits = la[0, -1] - lg[0, -1]
        elif use_head == "plus":
            logits = la[0, -1] + lg[0, -1]
        else:  # mean
            logits = (la[0, -1] + lg[0, -1]) / 2
        logits = apply_repetition_penalty(logits, out_bytes, repetition_penalty)
        nb = sample_next_byte(logits, top_k=top_k, top_p=top_p, temperature=temperature)
        out_bytes.append(nb)
        cur = torch.cat([cur, torch.tensor([[nb]], dtype=torch.long)], dim=1)
    return bytes(out_bytes)


def beam_generate(model, prompt_ids, max_new: int, beam: int, use_head: str = "a"):
    """Simple beam search w/ argmax over remaining beams. Picks top-beam continuations."""
    block_size = model.block_size
    # Each beam: (ids, logprob, out_list)
    init = (prompt_ids.clone(), 0.0, [])
    beams = [init]
    for _ in range(max_new):
        cands = []
        for ids, lp, out in beams:
            if ids.shape[1] > block_size:
                ids = ids[:, -block_size:]
            with torch.no_grad():
                la, lg, _ = model(ids)
            if use_head == "a":
                logits = la[0, -1]
            elif use_head == "g":
                logits = lg[0, -1]
            elif use_head == "minus":
                logits = la[0, -1] - lg[0, -1]
            else:
                logits = (la[0, -1] + lg[0, -1]) / 2
            log_probs = F.log_softmax(logits, dim=-1)
            top_lp, top_idx = torch.topk(log_probs, k=beam)
            for j in range(beam):
                tid = int(top_idx[j].item())
                tlp = float(top_lp[j].item())
                new_ids = torch.cat([ids, torch.tensor([[tid]], dtype=torch.long)], dim=1)
                cands.append((new_ids, lp + tlp, out + [tid]))
        # keep top-`beam`
        cands.sort(key=lambda x: -x[1])
        beams = cands[:beam]
    # return all beams as bytes
    return [(bytes(o), lp) for (_, lp, o) in beams]


# ----- Scoring -----------------------------------------------------------

def score_text(text: str, gen_bytes: bytes) -> dict:
    """Compute KO/EN/whitespace/uniqueness metrics."""
    n = max(len(text), 1)
    nb = max(len(gen_bytes), 1)
    ko = sum(1 for ch in text if 0xAC00 <= ord(ch) <= 0xD7A3)
    en = sum(1 for ch in text if ch.isalpha() and ord(ch) < 128)
    ws = sum(1 for ch in text if ch.isspace())
    printable = sum(1 for b in gen_bytes if 32 <= b < 127 or b > 127)
    unique = len(set(gen_bytes))
    return {
        "ko_ratio": ko / max(len(text), 1),
        "ko_count": ko,
        "en_ratio": en / max(len(text), 1),
        "en_count": en,
        "ws_ratio": ws / max(len(text), 1),
        "printable_ratio": printable / nb,
        "unique_bytes": unique,
        "unique_ratio": unique / nb,
    }


def gibberish_flag(scores: dict) -> bool:
    """Heuristic: mostly whitespace OR < 3 unique bytes → degenerate."""
    return scores["ws_ratio"] >= 0.85 or scores["unique_bytes"] < 3


def quality_score(scores: dict) -> float:
    """Higher is better. KO weighted strongly; penalty for gibberish."""
    if gibberish_flag(scores):
        return -1.0
    # encourage KO + EN + diverse bytes
    return (
        scores["ko_ratio"] * 5.0
        + scores["en_ratio"] * 1.0
        + scores["unique_ratio"] * 1.0
        - scores["ws_ratio"] * 2.0
    )


# ----- Prompt formats ----------------------------------------------------

PROMPT_FORMATS = [
    ("bare_ko", "안녕하세요"),
    ("bare_ko2", "의식이란 무엇인가요?"),
    ("ko_marker", "사용자: 안녕하세요\n도우미:"),
    ("en_marker", "User: hello\nAssistant:"),
    ("chat_template", "<|user|>안녕하세요<|assistant|>"),
    ("empty_ko", "\n안녕하세요\n"),
    ("bare_en", "Hi there!"),
    ("en_seed", "Consciousness is"),
]


def load_model(ckpt_path: str, n_head_hint: int):
    ckpt = torch.load(ckpt_path, map_location="cpu", weights_only=False)
    sd = ckpt.get("model_state", ckpt)
    config = ckpt.get("config", {}) if isinstance(ckpt, dict) else {}
    d_model = config.get("dim", 384)
    n_layer = config.get("layers", 6)
    n_head = config.get("heads", n_head_hint)
    block_size = config.get("block_size", 256)
    last_err = None
    for nh in [n_head, 4, 6, 8, 3]:
        try:
            m = ConsciousLMReconstructed(
                vocab_size=256, d_model=d_model, n_head=nh, n_layer=n_layer,
                block_size=block_size, dropout=0.0,
            )
            miss, unexp = m.load_state_dict(sd, strict=False)
            if len(miss) == 0 and len(unexp) == 0:
                m.eval()
                return m, {"d_model": d_model, "n_layer": n_layer, "n_head": nh,
                           "block_size": block_size, "step": ckpt.get("step"),
                           "miss": len(miss), "unexp": len(unexp)}
        except Exception as e:
            last_err = e
            continue
    # fallback: best partial
    m = ConsciousLMReconstructed(
        vocab_size=256, d_model=d_model, n_head=n_head, n_layer=n_layer,
        block_size=block_size, dropout=0.0,
    )
    miss, unexp = m.load_state_dict(sd, strict=False)
    m.eval()
    return m, {"d_model": d_model, "n_layer": n_head, "n_head": n_head,
               "block_size": block_size, "step": ckpt.get("step"),
               "miss": len(miss), "unexp": len(unexp), "err": str(last_err)}


# ----- Phase A: focused sampling matrix ----------------------------------

def phase_a_matrix():
    """Reduced but representative grid; ~120 trials per ckpt.

    Settings: 12 sampling configs × ~10 prompts ≈ 120 — but to keep budget,
    we use 8 prompts per config and 12 configs = 96 trials per ckpt, x3 ckpts = 288.
    """
    cfgs = [
        # (label, top_k, top_p, temp, head, rep_pen, max_new)
        ("baseline_a",   40,  -1,   0.8,  "a",     1.0, 60),
        ("low_t_a",      40,  -1,   0.3,  "a",     1.0, 60),
        ("low_t_g",      40,  -1,   0.3,  "g",     1.0, 60),
        ("hi_t_a",       40,  -1,   1.5,  "a",     1.0, 60),
        ("nucleus_a",    -1,   0.9, 0.7,  "a",     1.0, 60),
        ("nucleus_strict_a", -1, 0.95, 1.0, "a",   1.0, 60),
        ("greedy_rep",   1,   -1,   1.0,  "a",     1.5, 120),
        ("repen_a",      40,  -1,   0.8,  "a",     1.5, 60),
        ("repen2_a",     80,   0.99,0.7,  "a",     1.2, 60),
        ("plus_head",    40,  -1,   0.7,  "plus",  1.0, 60),
        ("mean_head",    40,  -1,   0.7,  "mean",  1.0, 60),
        ("minus_head",   40,  -1,   0.7,  "minus", 1.0, 60),
    ]
    return cfgs


def run_phase_a(model, label):
    cfgs = phase_a_matrix()
    results = []
    block_size = model.block_size
    for cfg_label, top_k, top_p, temp, head, rep_pen, max_new in cfgs:
        for fmt_label, prompt in PROMPT_FORMATS:
            try:
                ids = text_to_byte_ids(prompt, max_len=block_size)
                t0 = time.time()
                gb = generate(model, ids, max_new=max_new, top_k=top_k, top_p=top_p,
                              temperature=temp, use_head=head, repetition_penalty=rep_pen)
                dt = time.time() - t0
                txt = gb.decode("utf-8", errors="replace")
                sc = score_text(txt, gb)
                qs = quality_score(sc)
                results.append({
                    "ckpt": label, "phase": "A",
                    "cfg": cfg_label, "fmt": fmt_label,
                    "params": dict(top_k=top_k, top_p=top_p, temperature=temp,
                                   head=head, rep_pen=rep_pen, max_new=max_new),
                    "prompt": prompt,
                    "gen": txt,
                    "scores": sc,
                    "quality": qs,
                    "gibberish": gibberish_flag(sc),
                    "wall_s": round(dt, 2),
                })
            except Exception as e:
                results.append({"ckpt": label, "phase": "A", "cfg": cfg_label,
                                "fmt": fmt_label, "error": f"{type(e).__name__}: {e}"})
    return results


def run_phase_b_beam(model, label):
    """Beam search, head=a, beam=4 and 8, on KO + chat-template prompts."""
    results = []
    block_size = model.block_size
    beam_prompts = [
        ("bare_ko", "안녕하세요"),
        ("ko_marker", "사용자: 안녕하세요\n도우미:"),
        ("en_marker", "User: hello\nAssistant:"),
        ("chat_template", "<|user|>안녕하세요<|assistant|>"),
    ]
    for beam in [4, 8]:
        for head in ["a", "g", "mean"]:
            for fmt_label, prompt in beam_prompts:
                try:
                    ids = text_to_byte_ids(prompt, max_len=block_size)
                    t0 = time.time()
                    cands = beam_generate(model, ids, max_new=40, beam=beam, use_head=head)
                    dt = time.time() - t0
                    # take top-1 + record all
                    best_bytes, best_lp = cands[0]
                    txt = best_bytes.decode("utf-8", errors="replace")
                    sc = score_text(txt, best_bytes)
                    qs = quality_score(sc)
                    results.append({
                        "ckpt": label, "phase": "B-beam",
                        "cfg": f"beam{beam}_{head}",
                        "fmt": fmt_label,
                        "params": dict(beam=beam, head=head, max_new=40),
                        "prompt": prompt,
                        "gen": txt,
                        "scores": sc,
                        "quality": qs,
                        "gibberish": gibberish_flag(sc),
                        "logprob": round(best_lp, 3),
                        "wall_s": round(dt, 2),
                        "n_hyps": len(cands),
                    })
                except Exception as e:
                    results.append({"ckpt": label, "phase": "B-beam",
                                    "cfg": f"beam{beam}_{head}", "fmt": fmt_label,
                                    "error": f"{type(e).__name__}: {e}"})
    return results


def run_for_ckpt(meta):
    label = meta["label"]
    print(f"\n=== {label} ===")
    model, info = load_model(meta["path"], meta["n_head"])
    print(f"  loaded: {info}")
    a = run_phase_a(model, label)
    b = run_phase_b_beam(model, label)
    return {"label": label, "info": info, "results": a + b}


def summarize(all_results):
    """Summary across all ckpts."""
    summary = {}
    by_ckpt = {}
    flat = []
    for ck_block in all_results:
        ck = ck_block["label"]
        rs = [r for r in ck_block["results"] if "scores" in r]
        flat.extend(rs)
        if not rs:
            continue
        rs_sorted = sorted(rs, key=lambda r: -r["quality"])
        ko_max = max(r["scores"]["ko_ratio"] for r in rs)
        gib_count = sum(1 for r in rs if r["gibberish"])
        by_ckpt[ck] = {
            "n_total": len(rs),
            "n_gibberish": gib_count,
            "ko_ratio_max": round(ko_max, 4),
            "ko_count_max": max(r["scores"]["ko_count"] for r in rs),
            "best_quality": round(rs_sorted[0]["quality"], 4),
            "best_cfg": rs_sorted[0]["cfg"],
            "best_fmt": rs_sorted[0]["fmt"],
            "best_gen": rs_sorted[0]["gen"][:120],
        }
    flat_sorted = sorted(flat, key=lambda r: -r["quality"])
    summary["by_ckpt"] = by_ckpt
    summary["overall_top10"] = [
        {"ckpt": r["ckpt"], "cfg": r["cfg"], "fmt": r["fmt"],
         "ko_ratio": round(r["scores"]["ko_ratio"], 4),
         "ko_count": r["scores"]["ko_count"],
         "en_count": r["scores"]["en_count"],
         "quality": round(r["quality"], 4),
         "prompt": r["prompt"], "gen": r["gen"][:200]}
        for r in flat_sorted[:10]
    ]
    # Verdict logic
    any_ko = any(r["scores"]["ko_count"] > 0 for r in flat)
    best_ko_ratio = max((r["scores"]["ko_ratio"] for r in flat), default=0.0)
    if not any_ko:
        verdict = "ARCHITECTURAL_FAIL_no_KO_anywhere"
    elif best_ko_ratio < 0.10:
        verdict = "RECONSTRUCTION_LIMIT_or_SAMPLING_LIMIT_low_KO"
    else:
        verdict = "PARTIAL_PASS_KO_signal"
    summary["best_ko_ratio_global"] = round(best_ko_ratio, 4)
    summary["verdict"] = verdict
    summary["n_total_trials"] = len(flat)
    return summary


def main():
    t_start = time.time()
    all_blocks = []
    for meta in CHECKPOINTS:
        try:
            block = run_for_ckpt(meta)
            all_blocks.append(block)
        except Exception as e:
            print(f"  ERROR for {meta['label']}: {e}")
            all_blocks.append({"label": meta["label"], "error": str(e)})
    summary = summarize(all_blocks)
    out = {
        "summary": summary,
        "ckpts": all_blocks,
        "wall_s_total": round(time.time() - t_start, 1),
    }
    out_path = OUT_DIR / "result.json"
    with out_path.open("w") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)
    # write best_outputs.txt
    txt_path = OUT_DIR / "best_outputs.txt"
    with txt_path.open("w") as f:
        f.write(f"# Best 10 outputs across all ckpts (sorted by quality_score)\n")
        f.write(f"# verdict: {summary['verdict']}\n")
        f.write(f"# best_ko_ratio_global: {summary['best_ko_ratio_global']}\n")
        f.write(f"# n_total_trials: {summary['n_total_trials']}\n\n")
        for i, r in enumerate(summary["overall_top10"], 1):
            f.write(f"--- #{i} ---\n")
            f.write(f"ckpt={r['ckpt']} cfg={r['cfg']} fmt={r['fmt']}\n")
            f.write(f"ko_ratio={r['ko_ratio']} ko_count={r['ko_count']} en_count={r['en_count']} quality={r['quality']}\n")
            f.write(f"prompt: {r['prompt']!r}\n")
            f.write(f"gen:    {r['gen']!r}\n\n")
    print(f"\n=== verdict: {summary['verdict']} ===")
    print(f"best_ko_ratio_global: {summary['best_ko_ratio_global']}")
    print(f"n_total_trials: {summary['n_total_trials']}")
    print(f"wall_s_total: {out['wall_s_total']}")
    print(f"result: {out_path}")
    print(f"best:   {txt_path}")
    for ck, info in summary["by_ckpt"].items():
        print(f"  {ck}: best_q={info['best_quality']} ko_max={info['ko_ratio_max']} cfg={info['best_cfg']} fmt={info['best_fmt']}")


if __name__ == "__main__":
    main()
