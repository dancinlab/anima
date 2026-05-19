"""Sampling-based generation test for cells64/cells128 — does the chat-cap survive
when we sample (top-k=40, temp=0.8) instead of argmax?

BG-R2 finding: top-1 = 0x20 (space) for ALL 5 prompts via argmax.
This script tests if the model still has multi-modal output distribution
that produces meaningful Korean/English under sampling.

raw#10 honest: this is generation smoke only, not full chat eval.
"""
import sys
import math
import json
import time
from pathlib import Path

import torch
import torch.nn as nn
import torch.nn.functional as F

# import reconstructed arch from sibling file
sys.path.insert(0, "/Users/ghost/core/anima/state/anima_clm_v2_mitosis_cells_recovery_2026_05_09")
from forward_smoke import ConsciousLMReconstructed, text_to_byte_ids  # noqa: E402

THIS_DIR = Path("/Users/ghost/core/anima/state/anima_clm_v2_mitosis_cells_recovery_2026_05_09")


def sample_next_byte(logits, top_k: int = 40, temperature: float = 0.8) -> int:
    """Top-k temperature sampling for next byte."""
    logits = logits / max(temperature, 1e-6)
    if top_k > 0:
        top_vals, top_idx = torch.topk(logits, k=min(top_k, logits.size(-1)))
        probs = F.softmax(top_vals, dim=-1)
        choice = torch.multinomial(probs, num_samples=1)
        return int(top_idx[choice].item())
    probs = F.softmax(logits, dim=-1)
    choice = torch.multinomial(probs, num_samples=1)
    return int(choice.item())


def generate(model, prompt_ids: torch.Tensor, max_new: int = 50,
             top_k: int = 40, temperature: float = 0.8,
             use_head: str = "a") -> tuple[bytes, list[float]]:
    """Generate max_new bytes auto-regressively. Returns (bytes, per-token tension trace)."""
    cur = prompt_ids.clone()
    out_bytes = []
    tensions_trace = []
    block_size = model.block_size
    for _ in range(max_new):
        # truncate to block_size
        if cur.shape[1] > block_size:
            cur = cur[:, -block_size:]
        with torch.no_grad():
            la, lg, tensions = model(cur)
        # Use specified head (a or g, or combined)
        if use_head == "a":
            logits = la[0, -1]
        elif use_head == "g":
            logits = lg[0, -1]
        else:  # combined: la - lg
            logits = la[0, -1] - lg[0, -1]
        # Track tension
        per_layer = sum(t.mean().item() for t in tensions) / len(tensions)
        tensions_trace.append(per_layer)
        next_id = sample_next_byte(logits, top_k=top_k, temperature=temperature)
        out_bytes.append(next_id)
        cur = torch.cat([cur, torch.tensor([[next_id]], dtype=torch.long)], dim=1)
    return bytes(out_bytes), tensions_trace


def run_test(pt_path: str, label: str):
    print(f"=== sampling generation test: {label} ===")
    ckpt = torch.load(pt_path, map_location="cpu", weights_only=False)
    sd = ckpt.get("model_state", ckpt)
    config = ckpt.get("config", {})
    d_model = config.get("dim", 384)
    n_layer = config.get("layers", 6)
    n_head = config.get("heads", 6 if "cells64" in label else 4)
    block_size = config.get("block_size", 256)

    model = ConsciousLMReconstructed(
        vocab_size=256, d_model=d_model, n_head=n_head, n_layer=n_layer, block_size=block_size, dropout=0.0
    )
    model.eval()
    miss, unexp = model.load_state_dict(sd, strict=False)
    print(f"  load: missing={len(miss)} unexpected={len(unexp)}")
    print(f"  config: d={d_model} L={n_layer} h={n_head} block={block_size} step={ckpt.get('step')}")

    prompts = [
        "안녕하세요",
        "의식이란",
        "사용자: 안녕하세요\n도우미:",
        "사용자: 의식이란 무엇인가요?\n도우미:",
        "Hi there!",
        "Consciousness is",
        "User: Hello\nAssistant:",
        "The meaning of life is",
    ]

    results = []
    settings = [
        {"top_k": 40, "temperature": 0.8, "use_head": "a"},
        {"top_k": 40, "temperature": 0.8, "use_head": "g"},
        {"top_k": 40, "temperature": 0.8, "use_head": "combined"},
        {"top_k": 1, "temperature": 1.0, "use_head": "a"},  # argmax baseline
    ]

    for setting in settings:
        for p in prompts:
            try:
                ids = text_to_byte_ids(p, max_len=block_size)
                t0 = time.time()
                gen_bytes, tens_trace = generate(
                    model, ids, max_new=60,
                    top_k=setting["top_k"],
                    temperature=setting["temperature"],
                    use_head=setting["use_head"],
                )
                dt = time.time() - t0
                # decode
                try:
                    gen_text = gen_bytes.decode("utf-8", errors="replace")
                except Exception:
                    gen_text = repr(gen_bytes)
                # printable ratio
                printable = sum(1 for b in gen_bytes if 32 <= b < 127 or b > 127) / max(len(gen_bytes), 1)
                # mean tension
                mean_tension = sum(tens_trace) / max(len(tens_trace), 1)
                results.append({
                    "setting": setting,
                    "prompt": p,
                    "gen_bytes_len": len(gen_bytes),
                    "gen_text": gen_text,
                    "printable_ratio": round(printable, 3),
                    "mean_tension": round(mean_tension, 4),
                    "wall_s": round(dt, 2),
                })
                print(f"  [{setting['use_head']:<8s} k={setting['top_k']:<2d} t={setting['temperature']:.1f}] {p!r}")
                print(f"      → {gen_text!r}  printable={printable:.2f} tens={mean_tension:.3f}")
            except Exception as e:
                results.append({"setting": setting, "prompt": p, "error": f"{type(e).__name__}: {e}"})
                print(f"  ERROR: {e}")

    # Heuristic verdict
    def is_hangul_byte(b: int) -> bool:
        return b >= 0xE0  # rough — Hangul UTF-8 starts with 3-byte sequences 0xEA-0xED first byte

    has_korean_output = False
    has_meaningful = False
    for r in results:
        if "gen_text" not in r:
            continue
        gt = r["gen_text"]
        # check for Korean characters (Hangul Syllables U+AC00-U+D7A3)
        for ch in gt:
            if 0xAC00 <= ord(ch) <= 0xD7A3:
                has_korean_output = True
                break
        # check for ASCII letters (English)
        ascii_letters = sum(1 for ch in gt if ch.isalpha() and ord(ch) < 128)
        if ascii_letters >= 5:
            has_meaningful = True

    if has_korean_output and has_meaningful:
        verdict = "PARTIAL_PASS_chat_cap_signal"
    elif has_meaningful:
        verdict = "PARTIAL_PASS_english_only"
    elif has_korean_output:
        verdict = "PARTIAL_PASS_korean_only"
    else:
        verdict = "FAIL_degenerate_output"

    return {
        "label": label,
        "verdict": verdict,
        "has_korean_output": has_korean_output,
        "has_meaningful_english": has_meaningful,
        "n_results": len(results),
        "results": results,
    }


def main():
    out = {}
    for label, fname in [("cells64", "cells64_final.pt"), ("cells128", "cells128_step_35000.pt")]:
        path = str(THIS_DIR / fname)
        out[label] = run_test(path, label)
        print()
    out["overall_verdict"] = (
        "PASS_chat_cap_recovered" if all(
            r["verdict"].startswith("PARTIAL_PASS") and r["has_meaningful_english"]
            for r in out.values() if isinstance(r, dict)
        ) else "FAIL_or_partial"
    )
    out_path = THIS_DIR / "sampling_gen_test_result.json"
    with out_path.open("w") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)
    print(f"\nresult: {out_path}")
    print(f"overall_verdict: {out['overall_verdict']}")


if __name__ == "__main__":
    main()
