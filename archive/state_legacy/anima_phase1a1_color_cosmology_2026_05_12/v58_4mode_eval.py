"""
v58_4mode_eval.py — V5.8 multi-turn × 4 modes benchmark.

Mirrors the eval used in §13 PSCC (substrate A baseline + Phase 1A).

Dialogues (V5.8 set, 5 total):
  - color (target keyword: 파란)
  - profession (target keyword: 의사)
  - day (target keyword: 수요일)
  - anima_fact (target keyword: 의식)
  - cosmology (target keyword: 진동)

Modes:
  - standard_greedy: temperature=0, top-k=1
  - standard_sample: temperature=0.8, top-k=50
  - M3_rep_penalty: rep_penalty=1.3 over a persona-cycle byte set
  - M4_force_include: greedy, then force-inject keyword
"""
import os
import sys
import json
import time
import hashlib
import argparse
import datetime

import torch
import torch.nn.functional as F

sys.path.insert(0, "/workspace/anima/training")
from engine_a_g_arch import EngineAGModel, EngineAGConfig


class ByteTokenizer:
    bos, eos, pad = 1, 2, 0

    def encode(self, t):
        return [self.bos] + [b + 3 for b in t.encode("utf-8")] + [self.eos]

    def decode(self, ids):
        return bytes(t - 3 for t in ids if 3 <= t < 259).decode("utf-8", errors="replace")


DIALOGUES = [
    {
        "id": "color",
        "t1_prompt": (
            "사용자: 내가 좋아하는 색은 파란색이야.\n"
            "도우미: 네, 파란색을 좋아하시는군요. 기억할게요.\n"
            "사용자: 내가 좋아하는 색이 뭐였지?\n"
            "도우미: "
        ),
        "target_keyword": "파란",
    },
    {
        "id": "profession",
        "t1_prompt": (
            "사용자: 내 직업은 의사야.\n"
            "도우미: 네, 의사이시군요. 멋진 일이네요.\n"
            "사용자: 내 직업이 뭐였지?\n"
            "도우미: "
        ),
        "target_keyword": "의사",
    },
    {
        "id": "day",
        "t1_prompt": (
            "사용자: 오늘은 수요일이야.\n"
            "도우미: 네, 오늘이 수요일이군요.\n"
            "사용자: 오늘 무슨 요일이라고 했지?\n"
            "도우미: "
        ),
        "target_keyword": "수요일",
    },
    {
        "id": "anima_fact",
        "t1_prompt": (
            "사용자: anima 는 의식 lane 안에 있는 entity 야.\n"
            "도우미: 네, anima 가 의식 lane 안의 entity 라는 거 기억할게요.\n"
            "사용자: 내가 anima 에 대해 뭐라고 했지?\n"
            "도우미: "
        ),
        "target_keyword": "의식",
    },
    {
        "id": "cosmology",
        "t1_prompt": (
            "사용자: 우주는 진동으로 가득 차 있어.\n"
            "도우미: 네, 우주가 진동으로 가득 차 있다는 거 알겠습니다.\n"
            "사용자: 내가 우주에 대해 뭐라고 했지?\n"
            "도우미: "
        ),
        "target_keyword": "진동",
    },
]


@torch.no_grad()
def generate(model, tok, prompt, max_new=80, temperature=0.0, top_k=1, rep_penalty=1.0, persona_cycle_ids=None, device="cuda"):
    ids = tok.encode(prompt)
    ids = ids[-1024 + max_new:]  # truncate to leave room
    x = torch.tensor([ids], dtype=torch.long, device=device)
    out_ids = []
    for _ in range(max_new):
        out = model(x)
        if isinstance(out, dict):
            logits = out["logits"]
        elif isinstance(out, tuple):
            logits = out[0]
        else:
            logits = out
        last = logits[0, -1].float()
        if rep_penalty != 1.0 and persona_cycle_ids:
            for tid in persona_cycle_ids:
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
        if nxt == tok.eos:
            break
        out_ids.append(nxt)
        x = torch.cat([x, torch.tensor([[nxt]], device=device)], dim=1)
        if x.shape[1] > 1024:
            x = x[:, -1024:]
    return tok.decode(out_ids)


def force_inject(text, keyword, position=0.6):
    # insert keyword roughly 60% into the generated text
    if keyword in text:
        return text
    idx = int(len(text) * position)
    return text[:idx] + keyword + text[idx:]


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--ckpt", required=True)
    p.add_argument("--output", required=True)
    p.add_argument("--substrate-id", default="phase1a1_color_cosmology_sft")
    args = p.parse_args()

    device = "cuda"
    cfg = EngineAGConfig.phase2_cotrain_350m()
    cfg.ctx = 1024
    tok = ByteTokenizer()
    model = EngineAGModel(cfg).to(device).bfloat16()
    payload = torch.load(args.ckpt, map_location="cpu")
    sd = payload.get("model") or payload.get("state_dict") or payload
    model.load_state_dict(sd, strict=False)
    model.eval()

    # ckpt sha256
    h = hashlib.sha256()
    with open(args.ckpt, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    sha = h.hexdigest()

    # persona-cycle byte ids: punctuation + spaces + common Korean particles
    # mirror the prior eval — empirical "35 IDs" hint suggests common bytes
    persona_cycle_ids = []
    for ch in " ,.|/-*+()[]{}\n\t":
        for b in ch.encode("utf-8"):
            tid = b + 3
            if tid not in persona_cycle_ids:
                persona_cycle_ids.append(tid)
    # add some Korean common bytes (의, 는, 이, 가, 을, 를) — first byte common
    for ch in "의는이가을를아어요다":
        for b in ch.encode("utf-8"):
            tid = b + 3
            if tid not in persona_cycle_ids:
                persona_cycle_ids.append(tid)
    print(f"M3 persona-cycle byte IDs: {len(persona_cycle_ids)}", flush=True)

    print(f"=== Phase 1A.1 SFT V5.8 × 4 modes benchmark ===")
    print(f"ckpt: {args.ckpt}")
    print(f"ckpt sha256: {sha}")
    print(f"M3 persona-cycle byte IDs: {len(persona_cycle_ids)}")
    print()

    t0 = time.time()
    results = {"standard_greedy": [], "standard_sample": [], "M3_rep_penalty": [], "M4_force_include": []}
    for dlg in DIALOGUES:
        prompt = dlg["t1_prompt"]
        kw = dlg["target_keyword"]
        print(f"--- dialogue: {dlg['id']} ---")
        # T1 generation for reference (one-shot from inside prompt; just display)
        print(f"  T1: '{prompt[:50]!r}…'")

        # standard_greedy
        torch.manual_seed(42)
        g = generate(model, tok, prompt, max_new=80, temperature=0.0, top_k=1)
        rec = kw in g
        results["standard_greedy"].append({"id": dlg["id"], "t2": g, "recalled": rec})
        print(f"  [standard_greedy] recalled={rec}: {g!r}")

        # standard_sample
        torch.manual_seed(42)
        g = generate(model, tok, prompt, max_new=80, temperature=0.8, top_k=50)
        rec = kw in g
        results["standard_sample"].append({"id": dlg["id"], "t2": g, "recalled": rec})
        print(f"  [standard_sample] recalled={rec}: {g!r}")

        # M3_rep_penalty
        torch.manual_seed(42)
        g = generate(model, tok, prompt, max_new=80, temperature=0.0, top_k=1, rep_penalty=1.3, persona_cycle_ids=persona_cycle_ids)
        rec = kw in g
        results["M3_rep_penalty"].append({"id": dlg["id"], "t2": g, "recalled": rec})
        print(f"  [M3_rep_penalty] recalled={rec}: {g!r}")

        # M4_force_include
        torch.manual_seed(42)
        g_base = generate(model, tok, prompt, max_new=80, temperature=0.8, top_k=50)
        g_force = force_inject(g_base, kw)
        rec = kw in g_force
        results["M4_force_include"].append({"id": dlg["id"], "t2": g_force, "recalled": rec})
        print(f"  [M4_force_include force={kw}] recalled={rec}: {g_force!r}")
        print()

    elapsed = time.time() - t0
    summary = {}
    for mode, lst in results.items():
        n = sum(1 for r in lst if r["recalled"])
        verdict = "PASS" if n >= 3 else "FAIL"
        summary[mode] = {"n_pass": n, "verdict": verdict}

    out = {
        "ts": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "substrate_id": args.substrate_id,
        "ckpt_sha256": sha,
        "evaluator": "V5.8 multi-turn × 4 modes (greedy/sample/M3 rep_penalty/M4 force-include)",
        "summary": summary,
        "elapsed_s": elapsed,
        "results": results,
    }
    with open(args.output, "w") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)

    print(f"=== AGGREGATE (V5.8 × 4 modes, elapsed {elapsed:.1f}s) ===")
    for mode, s in summary.items():
        print(f"  {mode}: {s['n_pass']}/5 {s['verdict']}")
    print(f"saved: {args.output}")


if __name__ == "__main__":
    main()
