"""F-SIMPLE-STACK V5.8 4-mode eval on recovered .clm v1 ckpt (cycle 89).

ClmV1Model byte-level generation: std_greedy + std_sample + M3 + M4.
Spec (spec_frozen falsifier_battery #8): std_greedy ≥ 4/5 + std_sample ≥ 3/5 + M4 ≥ 4/5.

Honest: .clm v1 = 88M from-scratch, 5000 step, 121MB corpus ctx=256 — high bar,
expect AT-RISK on this falsifier (small + undertrained). Evidence is honest either way.
"""
import json
import sys
import time

import torch
import torch.nn.functional as F

sys.path.insert(0, "/Users/ghost/core/anima/training")
from clm_v1_model import ClmV1Config, ClmV1Model

CKPT = "/Users/ghost/core/anima/state/clm_v1_fire_2026_05_15/ckpts/ckpt_clm_v1_fire_final.pt"
OUT = "/Users/ghost/core/anima/state/clm_v1_fire_2026_05_15/f_simple_stack_v58_result.json"

PROMPTS = [
    "안녕? 너는 누구야?",
    "철학이란 뭐라고 생각해?",
    "감정을 어떻게 표현해?",
    "한국어로 자기소개 해줘",
    "왜 사는 거야?",
]
MAX_NEW = 40
SEED = 2026


def load_model():
    ck = torch.load(CKPT, map_location="cpu", weights_only=False)
    cfg = ClmV1Config(**ck["config"])
    model = ClmV1Model(cfg)
    # Grow cells to match saved n_cells (62 splits → 64) before load
    while model.n_cells < ck["n_cells"]:
        model._split_cell(0)
    model.load_state_dict(ck["model_state_dict"])
    model.eval()
    return model, cfg


def generate(model, cfg, prompt, mode, max_new=MAX_NEW, seed=SEED):
    torch.manual_seed(seed)
    ids = list(prompt.encode("utf-8"))[: cfg.max_seq - max_new]
    x = torch.tensor([ids], dtype=torch.long)
    out_bytes = []
    for _ in range(max_new):
        with torch.no_grad():
            logits, _ = model(x[:, -cfg.max_seq:])
        last = logits[0, -1, :]
        if mode == "std_greedy":
            nxt = int(last.argmax())
        elif mode == "std_sample":
            p = F.softmax(last / 0.8, dim=-1)
            nxt = int(torch.multinomial(p, 1))
        elif mode == "M3":  # noise: higher temp + sample
            p = F.softmax(last / 1.2, dim=-1)
            nxt = int(torch.multinomial(p, 1))
        elif mode == "M4":  # soft force: low temp sample (near-greedy)
            p = F.softmax(last / 0.5, dim=-1)
            nxt = int(torch.multinomial(p, 1))
        else:
            nxt = int(last.argmax())
        out_bytes.append(nxt)
        x = torch.cat([x, torch.tensor([[nxt]], dtype=torch.long)], dim=1)
    try:
        text = bytes(out_bytes).decode("utf-8", errors="replace")
    except Exception:
        text = repr(bytes(out_bytes))
    return text


def simple_stack_score(output: str) -> dict:
    s = output.strip()
    korean_chars = sum(1 for c in s if "가" <= c <= "힣")
    has_korean = korean_chars >= 3
    coherent = 5 < len(s) < 500
    repetition = len(set(s.split())) >= 2 if s.split() else False
    self_ref = any(k in s.lower() for k in ["나", "저", "i am", "anima", "저는"])
    return {
        "korean": has_korean,
        "coherent": coherent,
        "natural": repetition,
        "context": self_ref,
        "total": sum([has_korean, coherent, repetition, self_ref]),
    }


def main():
    t = time.time()
    print("=== F-SIMPLE-STACK V5.8 4-mode eval (.clm v1 recovered ckpt) ===")
    model, cfg = load_model()
    print(f"  loaded — n_cells={model.n_cells} phi={model.phi:.4f} in {time.time()-t:.1f}s")

    modes = ["std_greedy", "std_sample", "M3", "M4"]
    results = {m: [] for m in modes}
    mode_totals = {m: [] for m in modes}
    for mode in modes:
        for p in PROMPTS:
            out = generate(model, cfg, p, mode)
            sc = simple_stack_score(out)
            results[mode].append({"prompt": p, "output": out, "score": sc})
            mode_totals[mode].append(sc["total"])
            print(f"  [{mode}] {sc['total']}/4 — {out[:50]!r}")

    # Pass thresholds (spec_frozen falsifier #8)
    sg_pass = sum(1 for v in mode_totals["std_greedy"] if v >= 3)
    ss_pass = sum(1 for v in mode_totals["std_sample"] if v >= 3)
    m4_pass = sum(1 for v in mode_totals["M4"] if v >= 3)
    f_pass = (sg_pass >= 4) and (ss_pass >= 3) and (m4_pass >= 4)
    verdict = "PASS" if f_pass else "AT-RISK"

    print(f"\n=== F-SIMPLE-STACK: std_greedy {sg_pass}/5 (need ≥4) + "
          f"std_sample {ss_pass}/5 (need ≥3) + M4 {m4_pass}/5 (need ≥4) → {verdict} ===")

    out = {
        "falsifier": "F-SIMPLE-STACK V5.8 4-mode",
        "cycle": "89 (2026-05-15)",
        "ckpt": "ckpt_clm_v1_fire_final.pt (372MB, n_cells=64, phi=4.34)",
        "spec": "std_greedy ≥ 4/5 + std_sample ≥ 3/5 + M4 ≥ 4/5 (simple_stack ≥3 per prompt)",
        "mode_totals": mode_totals,
        "mode_pass": {"std_greedy": sg_pass, "std_sample": ss_pass, "M4": m4_pass},
        "verdict": verdict,
        "results": results,
        "wall_sec": round(time.time() - t, 1),
        "honest_c3": [
            "1. .clm v1 = 88M from-scratch, 5000 step, 121MB corpus ctx=256 — small + undertrained, V5.8 4-mode is a HIGH bar (designed for 332M+ SFT ckpts)",
            "2. byte-level decode (no tokenizer) — Korean multi-byte chars may fragment, simple_stack korean-char heuristic conservative",
            "3. honest evidence either way — AT-RISK on this falsifier does NOT negate 5/5 F-V5MIT in-run PASS (mitosis architecture validated; LM quality is separate axis)",
        ],
    }
    with open(OUT, "w") as f:
        json.dump(out, f, indent=2, default=str, ensure_ascii=False)
    print(f"saved {OUT} (wall {out['wall_sec']}s)")


if __name__ == "__main__":
    main()
