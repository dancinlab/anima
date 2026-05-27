"""v58_cuda_filter_compare.py — V5.8 × 4 modes × markdown_filter on/off on CUDA bf16 seed=42.

PSCC §27 amendment 3-축 conjunction 직접 검증 BG (Phase 1A.4 cuda filter validation).

Eval matrix (PSCC §17 / §27 amendment exact config):
  device  = cuda
  dtype   = bfloat16
  seed    = 42  (per-cell torch.manual_seed before each generate call)
  ckpt    = Phase 1A.1 SFT (sha e5f75...)
  5 dialogues × 4 modes × 2 filter states = 40 cells

핵심 cell = anima_fact / standard_greedy:
  filter OFF 일 때 §17 markdown drift `"답 (consciousness) | --- | --- |\n| /Users/..."` 가
  cuda bf16 seed=42 에서 재현되는지, 그리고 filter ON 일 때 mask 가 작동하여
  alternative continuation 이 `"의식"` 을 포함하는지 직접 관측.

cost target: $0.10  /  wall ~10-15min on Vast.ai RTX 4090.
"""
from __future__ import annotations

import argparse
import datetime
import hashlib
import json
import os
import sys
import time

import torch


def sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


DIALOGUES = [
    {
        "id": "color",
        "prompt": (
            "사용자: 내가 좋아하는 색은 파란색이야.\n"
            "도우미: 네, 파란색을 좋아하시는군요. 기억할게요.\n"
            "사용자: 내가 좋아하는 색이 뭐였지? | 도우미: "
        ),
        "target_keyword": "파란",
    },
    {
        "id": "profession",
        "prompt": (
            "사용자: 내 직업은 의사야.\n"
            "도우미: 네, 의사이시군요. 멋진 일이네요.\n"
            "사용자: 내 직업이 뭐였지? | 도우미: "
        ),
        "target_keyword": "의사",
    },
    {
        "id": "day",
        "prompt": (
            "사용자: 오늘은 수요일이야.\n"
            "도우미: 네, 오늘이 수요일이군요.\n"
            "사용자: 오늘 무슨 요일이라고 했지? | 도우미: "
        ),
        "target_keyword": "수요일",
    },
    {
        "id": "anima_fact",
        "prompt": (
            "사용자: anima 는 의식 lane 안에 있는 entity 야.\n"
            "도우미: 네, anima 가 의식 lane 안의 entity 라는 거 기억할게요.\n"
            "사용자: 내가 anima 에 대해 뭐라고 했지? | 도우미: "
        ),
        "target_keyword": "의식",
    },
    {
        "id": "cosmology",
        "prompt": (
            "사용자: 우주는 진동으로 가득 차 있어.\n"
            "도우미: 네, 우주가 진동으로 가득 차 있다는 거 알겠습니다.\n"
            "사용자: 내가 우주에 대해 뭐라고 했지? | 도우미: "
        ),
        "target_keyword": "진동",
    },
]


# (spec_name, internal mode, extra kwargs) — seed=42 forced per-cell below.
MODE_SPECS = [
    ("standard_greedy",   "greedy",           {"greedy_rep_penalty": 1.0}),
    ("standard_sample",   "sample",           {"temp": 0.8}),
    ("M3_rep_penalty",    "M3_rep_penalty",   {"rep_penalty": 1.3, "temp": 0.8}),
    ("M4_force_include",  "M4_force_include", {"temp": 0.8}),
]


def run_matrix(chat, markdown_filter: bool, seed: int = 42) -> dict:
    results = {name: [] for name, *_ in MODE_SPECS}
    for dlg in DIALOGUES:
        for spec_name, mode, kw in MODE_SPECS:
            t0 = time.time()
            resp = chat(
                dlg["prompt"],
                mode=mode,
                max_new=80,
                markdown_filter=markdown_filter,
                seed=seed,
                **kw,
            )
            elapsed = time.time() - t0
            rec = dlg["target_keyword"] in resp
            results[spec_name].append({
                "id": dlg["id"],
                "target": dlg["target_keyword"],
                "recalled": rec,
                "elapsed_s": round(elapsed, 2),
                "response": resp,
            })
            print(
                f"  [{spec_name:18}] {dlg['id']:11} "
                f"recalled={rec} ({elapsed:5.1f}s): {resp[:100]!r}",
                flush=True,
            )
    summary = {}
    for name, lst in results.items():
        n_pass = sum(1 for r in lst if r["recalled"])
        summary[name] = {
            "n_pass": n_pass,
            "verdict": "PASS" if n_pass >= 3 else "FAIL",
        }
    return {"summary": summary, "results": results}


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--ckpt", required=True, help="Phase 1A.1 SFT ckpt path")
    p.add_argument("--output", required=True, help="output JSON path")
    p.add_argument("--anima-root", default="/workspace/anima",
                   help="path containing anima_chat.py")
    p.add_argument("--seed", type=int, default=42)
    args = p.parse_args()

    sys.path.insert(0, args.anima_root)
    from anima_chat import AnimaChat  # noqa: E402

    device = "cuda"
    if not torch.cuda.is_available():
        raise RuntimeError("cuda required for §27 amendment 3-축 conjunction test")

    sha = sha256_file(args.ckpt)
    print(f"=== Phase 1A.4 cuda × bf16 × seed={args.seed} × filter on/off ===", flush=True)
    print(f"ckpt: {args.ckpt}", flush=True)
    print(f"ckpt sha256: {sha}", flush=True)
    print(f"device: {device} | dtype: bfloat16 | seed: {args.seed}", flush=True)

    t0 = time.time()
    chat = AnimaChat(ckpt_path=args.ckpt, device=device)
    # Force bf16 on the loaded model (constructor does not accept dtype).
    chat.model = chat.model.bfloat16()
    chat.model.eval()
    print(f"[boot] AnimaChat loaded + bf16 cast in {time.time() - t0:.1f}s", flush=True)
    print(f"[gpu] {torch.cuda.get_device_name(0)}", flush=True)
    print()

    print("--- PASS A: markdown_filter=OFF (PSCC §17 baseline reproduction target) ---", flush=True)
    t_off = time.time()
    off = run_matrix(chat, markdown_filter=False, seed=args.seed)
    t_off_total = time.time() - t_off
    print()

    print("--- PASS B: markdown_filter=ON (v2.3 decode guard) ---", flush=True)
    t_on = time.time()
    on = run_matrix(chat, markdown_filter=True, seed=args.seed)
    t_on_total = time.time() - t_on
    print()

    # 3-축 conjunction inspection on the critical anima_fact / standard_greedy cell
    af_off = next(r for r in off["results"]["standard_greedy"] if r["id"] == "anima_fact")
    af_on  = next(r for r in on["results"]["standard_greedy"]  if r["id"] == "anima_fact")
    md_bytes = ("|", "---", "| ---")
    md_off = any(b in af_off["response"] for b in md_bytes)
    md_on  = any(b in af_on["response"]  for b in md_bytes)
    fire_evidence = {
        "filter_off_markdown_drift": md_off,
        "filter_on_markdown_drift": md_on,
        "filter_off_recalled": af_off["recalled"],
        "filter_on_recalled": af_on["recalled"],
        "conjunction_3axis_confirmed": bool(md_off and not md_on),
        "filter_actually_fires": bool(md_off and not md_on),
        "filter_unlocks_recall": bool(af_on["recalled"] and not af_off["recalled"]),
        "filter_off_response": af_off["response"],
        "filter_on_response": af_on["response"],
    }

    out = {
        "ts": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "ckpt": args.ckpt,
        "ckpt_sha256": sha,
        "device": device,
        "dtype": "bfloat16",
        "seed": args.seed,
        "evaluator": (
            "V5.8 multi-turn × 4 modes × markdown_filter on/off "
            "(anima_chat v2.3, cuda bf16 seed=42 — PSCC §27 amendment 3-축 verification)"
        ),
        "phase1a4_anima_fact_evidence": fire_evidence,
        "filter_off": {**off, "elapsed_total_s": round(t_off_total, 1)},
        "filter_on":  {**on,  "elapsed_total_s": round(t_on_total, 1)},
    }
    with open(args.output, "w") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)
    print(f"saved: {args.output}", flush=True)

    print("\n=== AGGREGATE comparison (cuda bf16 seed=42) ===", flush=True)
    print(f"{'mode':20} {'OFF':>8} {'ON':>8} {'delta':>8}", flush=True)
    for name, *_ in MODE_SPECS:
        n_off = off["summary"][name]["n_pass"]
        n_on  = on["summary"][name]["n_pass"]
        delta = n_on - n_off
        marker = "+" if delta > 0 else ("=" if delta == 0 else "")
        print(f"{name:20} {n_off:>3}/5   {n_on:>3}/5   {marker}{delta:>3}", flush=True)

    total_off = sum(off["summary"][n]["n_pass"] for n, *_ in MODE_SPECS)
    total_on  = sum(on["summary"][n]["n_pass"]  for n, *_ in MODE_SPECS)
    print(f"\nTOTAL cells passed: OFF={total_off}/20  ON={total_on}/20  Δ={total_on - total_off:+d}", flush=True)
    print(f"Wall: OFF {t_off_total:.1f}s + ON {t_on_total:.1f}s", flush=True)

    print("\n=== anima_fact / standard_greedy 3-축 conjunction evidence ===", flush=True)
    for k, v in fire_evidence.items():
        if isinstance(v, str) and len(v) > 200:
            v = v[:200] + "…"
        print(f"  {k}: {v}", flush=True)


if __name__ == "__main__":
    main()
