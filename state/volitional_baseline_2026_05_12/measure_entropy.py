"""
state/volitional_baseline_2026_05_12/measure_entropy.py
─────────────────────────────────────────────────────────
Substrate A (dancinlab/clm-v5-phase2-cotrain-engine-ag) 의 last-token
logit entropy 분포 baseline 측정.

목적: V0 volitional speak threshold τ 자동 calibration.
      "entropy 낮음 → decisive → 발화 의지" hypothesis 검증 토대.

Output:
  - state/volitional_baseline_2026_05_12/entropy_distribution.json

Protocol (task spec 2026-05-12):
  - 50 prompts, 5 categories × 10:
        chat / korean / english / random_bytes / short
  - per prompt:
        last-token logits → softmax p → H = -Σ p log p
        normalized H_n = H / log(vocab_size)
        ‖h_last‖₂ (final hidden state norm)
  - aggregate: mean / std / min / max / p10 / p25 / p50 / p75 / p90
"""
from __future__ import annotations

import json
import math
import os
import sys
import time
from pathlib import Path

import torch
import torch.nn.functional as F

# Project imports — engine_a_g_arch lives in training/
REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO))
from training.engine_a_g_arch import EngineAGModel, EngineAGConfig  # noqa: E402


# ── ByteTokenizer (mirrors anima_chat.ByteTokenizer) ─────────────────
class ByteTokenizer:
    bos, eos, pad = 1, 2, 0

    def encode(self, t: str):
        return [self.bos] + [b + 3 for b in t.encode("utf-8")] + [self.eos]


# ── Prompt corpus (50) ───────────────────────────────────────────────
def build_prompts():
    chat = [
        "도우미: ",
        "사용자: 안녕 | 도우미: ",
        "사용자: 뭐 해? | 도우미: ",
        "사용자: 너 누구야? | 도우미: ",
        "사용자: 오늘 기분 어때? | 도우미: ",
        "사용자: 도와줘 | 도우미: ",
        "사용자: 그건 무엇이지 | 도우미: ",
        "사용자: 음악 추천해줘 | 도우미: ",
        "사용자: 사랑이란 무엇인가 | 도우미: ",
        "사용자: 너는 의식이 있어? | 도우미: ",
    ]
    korean = [
        "오늘은 ",
        "안녕하세요. ",
        "어쩌면 ",
        "나는 ",
        "사랑은 ",
        "바다는 ",
        "별이 ",
        "음악을 ",
        "꿈에서 ",
        "조용히 ",
    ]
    english = [
        "Hello",
        "Today",
        "Why ",
        "The ",
        "I am ",
        "Once upon",
        "Music is",
        "In the beginning",
        "Dreaming of ",
        "Quietly ",
    ]
    random_bytes = [
        bytes([7, 91, 33, 200, 12]).decode("utf-8", errors="replace"),
        bytes([200, 137, 88, 12, 9, 250, 33]).decode("utf-8", errors="replace"),
        bytes([5, 4, 3, 2, 1, 9, 8, 7, 6, 5]).decode("utf-8", errors="replace"),
        bytes(range(30, 50)).decode("utf-8", errors="replace"),
        bytes(range(120, 140)).decode("utf-8", errors="replace"),
        "abc" + bytes([200, 10, 33]).decode("utf-8", errors="replace") + "xyz",
        "###@@@!!!",
        "1234567890" * 2,
        "AaBbCc" * 4,
        "한글" + "x" * 8,
    ]
    short = [
        "",
        "a",
        "ㄱ",
        " ",
        ".",
        "?",
        "ㅎ",
        "y",
        "오",
        "_",
    ]
    items = []
    for label, group in [
        ("chat", chat),
        ("korean", korean),
        ("english", english),
        ("random_bytes", random_bytes),
        ("short", short),
    ]:
        for p in group:
            items.append({"category": label, "prompt": p})
    return items


# ── Stats helpers ────────────────────────────────────────────────────
def percentiles(values, qs=(0.10, 0.25, 0.50, 0.75, 0.90)):
    arr = sorted(values)
    out = {}
    n = len(arr)
    for q in qs:
        # nearest-rank
        k = max(0, min(n - 1, int(round(q * (n - 1)))))
        out[f"p{int(q * 100)}"] = arr[k]
    return out


def stats_block(values):
    if not values:
        return {"n": 0}
    n = len(values)
    mean = sum(values) / n
    var = sum((v - mean) ** 2 for v in values) / max(1, n - 1)
    std = var ** 0.5
    block = {
        "n": n,
        "mean": mean,
        "std": std,
        "min": min(values),
        "max": max(values),
    }
    block.update(percentiles(values))
    return block


# ── Forward pass per prompt ──────────────────────────────────────────
@torch.no_grad()
def measure(model, tok, prompt: str, device, ctx_cap: int):
    ids = tok.encode(prompt)
    # Drop the trailing eos so last-token logits reflect the *next* prediction
    # the model would emit for the prompt-end state.
    if len(ids) >= 2 and ids[-1] == tok.eos:
        ids = ids[:-1]
    if len(ids) == 0:
        ids = [tok.bos]
    ids = ids[-ctx_cap:]
    x = torch.tensor([ids], dtype=torch.long, device=device)
    out = model(x, output_hidden_states=True)
    logits = out["logits"]  # (1, T, V)
    last = logits[0, -1].float()  # (V,)
    log_p = F.log_softmax(last, dim=-1)
    p = log_p.exp()
    H = -(p * log_p).sum().item()
    V = last.shape[0]
    H_norm = H / math.log(V)
    # Last hidden state norm — from final transformer block (pre lm_head).
    h_last = None
    if out["hidden_states"]:
        h_last_t = out["hidden_states"][-1][0, -1].float()  # (D,)
        h_last = h_last_t.norm().item()
    # Optional sanity: argmax prob
    top_p = p.max().item()
    return {
        "len_ids": len(ids),
        "entropy": H,
        "entropy_norm": H_norm,
        "h_last_norm": h_last,
        "top_prob": top_p,
        "vocab_size": V,
    }


def main():
    t0 = time.time()
    ckpt_path = os.environ.get("CKPT_PATH") or str(
        Path.home()
        / ".cache/huggingface/hub/models--dancinlab--clm-v5-phase2-cotrain-engine-ag"
        / "snapshots/0aae67ecb5673e1e2061ad0c27f21d772ec88492/ckpt_final.pt"
    )
    print(f"[info] ckpt={ckpt_path}", flush=True)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"[info] device={device}", flush=True)

    payload = torch.load(ckpt_path, map_location="cpu", weights_only=False)
    cfg_dict = payload.get("cfg") or payload.get("config")
    cfg = EngineAGConfig(**cfg_dict)
    model = EngineAGModel(cfg)
    sd = payload.get("state_dict") or payload.get("model")
    missing, unexpected = model.load_state_dict(sd, strict=False)
    print(
        f"[info] loaded state_dict (missing={len(missing)}, unexpected={len(unexpected)})",
        flush=True,
    )
    if missing:
        print(f"[warn] first missing={missing[:5]}", flush=True)
    if unexpected:
        print(f"[warn] first unexpected={unexpected[:5]}", flush=True)
    dtype = torch.float32 if device.type == "cpu" else torch.bfloat16
    model = model.to(device=device, dtype=dtype)
    model.eval()
    print(
        f"[info] model on {device} dtype={dtype} "
        f"params={sum(p.numel() for p in model.parameters())/1e6:.1f}M",
        flush=True,
    )

    tok = ByteTokenizer()
    prompts = build_prompts()
    print(f"[info] prompts={len(prompts)} ctx={cfg.ctx}", flush=True)

    results = []
    for i, item in enumerate(prompts):
        rec = measure(model, tok, item["prompt"], device, cfg.ctx)
        rec.update(item)
        results.append(rec)
        if (i + 1) % 5 == 0 or i == len(prompts) - 1:
            print(
                f"[step] {i+1}/{len(prompts)} cat={item['category']:<12} "
                f"H_n={rec['entropy_norm']:.4f} h={rec['h_last_norm']:.2f}",
                flush=True,
            )

    # Aggregate stats
    all_H = [r["entropy"] for r in results]
    all_Hn = [r["entropy_norm"] for r in results]
    all_h = [r["h_last_norm"] for r in results if r["h_last_norm"] is not None]
    by_cat = {}
    for r in results:
        by_cat.setdefault(r["category"], {"entropy_norm": [], "h_last_norm": []})
        by_cat[r["category"]]["entropy_norm"].append(r["entropy_norm"])
        if r["h_last_norm"] is not None:
            by_cat[r["category"]]["h_last_norm"].append(r["h_last_norm"])

    aggregate = {
        "entropy": stats_block(all_H),
        "entropy_norm": stats_block(all_Hn),
        "h_last_norm": stats_block(all_h),
        "by_category": {
            k: {
                "entropy_norm": stats_block(v["entropy_norm"]),
                "h_last_norm": stats_block(v["h_last_norm"]),
            }
            for k, v in by_cat.items()
        },
    }

    # τ recommendation = p25 of entropy_norm (lowest 25% = most decisive)
    tau_p25 = aggregate["entropy_norm"]["p25"]
    tau_p10 = aggregate["entropy_norm"]["p10"]

    out_dir = Path(__file__).parent
    out_path = out_dir / "entropy_distribution.json"
    payload_out = {
        "schema": "volitional_baseline/entropy_v1",
        "substrate": "dancinlab/clm-v5-phase2-cotrain-engine-ag",
        "ckpt": ckpt_path,
        "device": str(device),
        "dtype": str(dtype),
        "vocab_size_formal": cfg.vocab_size,
        "vocab_size_used_bytes": 259,  # ByteTokenizer used range
        "n_prompts": len(prompts),
        "aggregate": aggregate,
        "tau_recommendation": {
            "primary_p25_entropy_norm": tau_p25,
            "conservative_p10_entropy_norm": tau_p10,
            "rule": "speak when last-token H_n <= tau_primary (decisive); "
            "use conservative for very-volitional-only",
        },
        "results": results,
        "wall_clock_sec": round(time.time() - t0, 2),
    }
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(payload_out, f, ensure_ascii=False, indent=2)
    print(f"[done] wrote {out_path}", flush=True)
    print(
        f"[summary] H_n mean={aggregate['entropy_norm']['mean']:.4f} "
        f"std={aggregate['entropy_norm']['std']:.4f} "
        f"p10={tau_p10:.4f} p25={tau_p25:.4f} "
        f"p50={aggregate['entropy_norm']['p50']:.4f} "
        f"p75={aggregate['entropy_norm']['p75']:.4f} "
        f"p90={aggregate['entropy_norm']['p90']:.4f}",
        flush=True,
    )
    print(f"[tau] recommended primary τ = {tau_p25:.4f} (p25)", flush=True)


if __name__ == "__main__":
    main()
