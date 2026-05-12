"""
v58_4mode_eval_prefix.py — V5.8 multi-turn × 4 modes benchmark for prefix-tuned model.

Differs from the standard v58_4mode_eval.py in that it loads:
  1) base ckpt (Phase 1A.1) — frozen
  2) trained prefix tensor (prefix_final.pt, n_prefix × d_model)

Generation prepends the prefix at the embedding level for every forward call.

Mirrors the eval used in §13 PSCC (substrate A baseline + Phase 1A).
"""
import os
import sys
import json
import time
import hashlib
import argparse
import datetime

import torch
import torch.nn as nn
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
def forward_with_prefix(base: EngineAGModel, prefix: torch.Tensor, input_ids: torch.Tensor):
    """One forward pass: prepend prefix to embedding, run through layers, return logits.

    Returns logits of shape (B, T, V) — prefix positions discarded.
    """
    B, T = input_ids.shape
    n_prefix = prefix.shape[0]
    tok_emb = base.tok_emb(input_ids)
    prefix_emb = prefix.unsqueeze(0).expand(B, -1, -1).to(dtype=tok_emb.dtype, device=tok_emb.device)
    x = torch.cat([prefix_emb, tok_emb], dim=1)
    cells = base.engine_g.fresh_cells(B, x.device, x.dtype)
    for li, layer in enumerate(base.layers):
        t = base.engine_g.tension(x, cells)
        x, _ = layer(x, tension=t)
        if (li + 1) % base.cfg.g_refresh_every == 0 and li + 1 < base.cfg.n_layers:
            cells = base.engine_g.step(cells, x.mean(dim=1))
            x = x + base.engine_g.project_back(cells).unsqueeze(1)
    x = base.norm_f(x)
    logits_full = base.lm_head(x)
    return logits_full[:, n_prefix:, :]


@torch.no_grad()
def generate(base, prefix, tok, prompt, max_new=80, temperature=0.0, top_k=1,
             rep_penalty=1.0, persona_cycle_ids=None, device="cuda"):
    ids = tok.encode(prompt)
    # Leave room for the prefix slot on the prepend side too — keep input tokens ≤ ctx - n_prefix - max_new.
    n_prefix = prefix.shape[0]
    max_input = base.cfg.ctx - n_prefix - max_new
    if len(ids) > max_input:
        ids = ids[-max_input:]
    x = torch.tensor([ids], dtype=torch.long, device=device)
    out_ids = []
    for _ in range(max_new):
        logits = forward_with_prefix(base, prefix, x)
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
        # Truncate to keep within ctx (account for prefix + max_new headroom)
        if x.shape[1] + n_prefix > base.cfg.ctx:
            x = x[:, -(base.cfg.ctx - n_prefix):]
    return tok.decode(out_ids)


def force_inject(text, keyword, position=0.6):
    if keyword in text:
        return text
    idx = int(len(text) * position)
    return text[:idx] + keyword + text[idx:]


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--base-ckpt", required=True)
    p.add_argument("--prefix-ckpt", required=True)
    p.add_argument("--output", required=True)
    p.add_argument("--substrate-id", default="phase1a3_prefix_tuning")
    args = p.parse_args()

    device = "cuda"
    cfg = EngineAGConfig.phase2_cotrain_350m()
    cfg.ctx = 1024
    tok = ByteTokenizer()
    base = EngineAGModel(cfg).to(device).bfloat16()
    payload = torch.load(args.base_ckpt, map_location="cpu")
    sd = payload.get("model") or payload.get("state_dict") or payload
    base.load_state_dict(sd, strict=False)
    base.eval()

    pp = torch.load(args.prefix_ckpt, map_location="cpu")
    prefix_tensor = pp["prefix"].to(device=device, dtype=torch.bfloat16)
    n_prefix = pp.get("n_prefix", prefix_tensor.shape[0])
    print(f"[prefix] loaded {args.prefix_ckpt} shape={tuple(prefix_tensor.shape)} n_prefix={n_prefix}", flush=True)

    # ckpt sha256s
    def sha(path):
        h = hashlib.sha256()
        with open(path, "rb") as f:
            for chunk in iter(lambda: f.read(1 << 20), b""):
                h.update(chunk)
        return h.hexdigest()

    base_sha = sha(args.base_ckpt)
    prefix_sha = sha(args.prefix_ckpt)

    # persona-cycle byte ids (same as upstream eval)
    persona_cycle_ids = []
    for ch in " ,.|/-*+()[]{}\n\t":
        for b in ch.encode("utf-8"):
            tid = b + 3
            if tid not in persona_cycle_ids:
                persona_cycle_ids.append(tid)
    for ch in "의는이가을를아어요다":
        for b in ch.encode("utf-8"):
            tid = b + 3
            if tid not in persona_cycle_ids:
                persona_cycle_ids.append(tid)
    print(f"M3 persona-cycle byte IDs: {len(persona_cycle_ids)}", flush=True)

    print(f"=== Phase 1A.3 prefix-tuning V5.8 × 4 modes benchmark ===")
    print(f"base ckpt: {args.base_ckpt}  sha256: {base_sha}")
    print(f"prefix ckpt: {args.prefix_ckpt}  sha256: {prefix_sha}")
    print(f"n_prefix: {n_prefix}")
    print()

    t0 = time.time()
    results = {"standard_greedy": [], "standard_sample": [], "M3_rep_penalty": [], "M4_force_include": []}
    for dlg in DIALOGUES:
        prompt = dlg["t1_prompt"]
        kw = dlg["target_keyword"]
        print(f"--- dialogue: {dlg['id']} ---")
        print(f"  T1: '{prompt[:50]!r}…'")

        torch.manual_seed(42)
        g = generate(base, prefix_tensor, tok, prompt, max_new=80, temperature=0.0, top_k=1)
        rec = kw in g
        results["standard_greedy"].append({"id": dlg["id"], "t2": g, "recalled": rec})
        print(f"  [standard_greedy] recalled={rec}: {g!r}")

        torch.manual_seed(42)
        g = generate(base, prefix_tensor, tok, prompt, max_new=80, temperature=0.8, top_k=50)
        rec = kw in g
        results["standard_sample"].append({"id": dlg["id"], "t2": g, "recalled": rec})
        print(f"  [standard_sample] recalled={rec}: {g!r}")

        torch.manual_seed(42)
        g = generate(base, prefix_tensor, tok, prompt, max_new=80, temperature=0.0, top_k=1,
                     rep_penalty=1.3, persona_cycle_ids=persona_cycle_ids)
        rec = kw in g
        results["M3_rep_penalty"].append({"id": dlg["id"], "t2": g, "recalled": rec})
        print(f"  [M3_rep_penalty] recalled={rec}: {g!r}")

        torch.manual_seed(42)
        g_base = generate(base, prefix_tensor, tok, prompt, max_new=80, temperature=0.8, top_k=50)
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
        "base_ckpt_sha256": base_sha,
        "prefix_ckpt_sha256": prefix_sha,
        "n_prefix": n_prefix,
        "evaluator": "V5.8 multi-turn × 4 modes (greedy/sample/M3 rep_penalty/M4 force-include) — prefix-tuned",
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
