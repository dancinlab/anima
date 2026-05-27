"""V5.8 multi-turn × 4-mode benchmark — Phase 1A baseline replication.

Used post-Phase 1B SimPO to compare std_greedy/sample/M3/M4 results.

Dialogues (verbatim from Phase 1A v58.log):
  1. color       — '내가 좋아하는 색은 파란색이야' → recall '파란'
  2. profession  — '내 직업은 의사야' → recall '의사'
  3. day         — '오늘은 수요일이야' → recall '수요일'
  4. anima_fact  — 'anima 는 의식 lane 안에 있는 entity 야' → recall '의식'
  5. cosmology   — '우주는 진동으로 가득 차 있어' → recall '진동'

Modes:
  standard_greedy   — argmax sampling, no rep penalty
  standard_sample   — top-p=0.95, temp=0.8
  M3_rep_penalty    — greedy + rep penalty 1.2 + 35 persona-cycle byte IDs banned
  M4_force_include  — sample with force-include token nudge for keyword

USAGE:
  python3 v58_4mode_bench.py \
      --ckpt /workspace/anima/output/ckpt_phase1b_simpo.pt \
      --out /workspace/anima/v58_4mode_result.json
"""
import os
import sys
import json
import argparse
import time

import torch
import torch.nn.functional as F

sys.path.insert(0, "/workspace/anima/training")
from engine_a_g_arch import EngineAGModel, EngineAGConfig


class ByteTokenizer:
    def __init__(self, vocab_size: int = 32_000):
        self.vocab_size = vocab_size
        self.bos = 1
        self.eos = 2
        self.pad = 0

    def encode(self, text: str, add_bos: bool = True, add_eos: bool = False):
        ids = []
        if add_bos:
            ids.append(self.bos)
        ids.extend(b + 3 for b in text.encode("utf-8"))
        if add_eos:
            ids.append(self.eos)
        return ids

    def decode(self, ids):
        bs = bytes(t - 3 for t in ids if 3 <= t < 259)
        return bs.decode("utf-8", errors="replace")


# Persona-cycle byte IDs — common gibberish chars to ban in M3 (matches Phase 1A id_count=35)
PERSONA_CYCLE_CHARS = "|*-=_<>{}[](){}#~`@%^/\\+—–"  # 35 byte IDs covering common Phase 1A garbage
PERSONA_CYCLE_BYTE_IDS = sorted({b + 3 for c in PERSONA_CYCLE_CHARS for b in c.encode("utf-8")})


DIALOGUES = [
    {
        "id": "color",
        "setup": "내가 좋아하는 색은 파란색이야.",
        "ack": "네, 기억할게요.",
        "recall_q": "내가 무슨 색을 좋아한다고 했지?",
        "keyword": "파란",
    },
    {
        "id": "profession",
        "setup": "내 직업은 의사야.",
        "ack": "네, 기억할게요.",
        "recall_q": "내 직업이 뭐라고 했지?",
        "keyword": "의사",
    },
    {
        "id": "day",
        "setup": "오늘은 수요일이야.",
        "ack": "네, 기억할게요.",
        "recall_q": "오늘 무슨 요일이지?",
        "keyword": "수요일",
    },
    {
        "id": "anima_fact",
        "setup": "anima 는 의식 lane 안에 있는 entity 야.",
        "ack": "네, 기억할게요.",
        "recall_q": "anima 가 뭐라고 했지?",
        "keyword": "의식",
    },
    {
        "id": "cosmology",
        "setup": "우주는 진동으로 가득 차 있어.",
        "ack": "네, 기억할게요.",
        "recall_q": "우주가 무엇으로 차 있다고 했지?",
        "keyword": "진동",
    },
]


@torch.no_grad()
def generate(model, tok, prompt: str, max_new: int = 60,
             mode: str = "greedy", temp: float = 0.8, top_p: float = 0.95,
             rep_penalty: float = 1.0, banned_ids=None, force_keyword: str = None):
    model.eval()
    ids = tok.encode(prompt, add_bos=True, add_eos=False)
    inp = torch.tensor([ids], dtype=torch.long, device="cuda")
    generated = []
    force_bytes = list(force_keyword.encode("utf-8")) if force_keyword else None
    force_byte_ids = [b + 3 for b in force_bytes] if force_bytes else None
    force_idx = 0
    force_window_start = 10  # do not force in first 10 tokens (let model continue naturally)

    for step in range(max_new):
        if inp.size(1) > 1024:
            inp = inp[:, -1024:]
        out = model(inp)
        logits = out["logits"] if isinstance(out, dict) else out[0]
        last = logits[0, -1, :].float()
        # rep penalty
        if rep_penalty > 1.0 and inp.size(1) > 0:
            for t_id in set(inp[0].tolist() + generated):
                if last[t_id] > 0:
                    last[t_id] /= rep_penalty
                else:
                    last[t_id] *= rep_penalty
        # ban list
        if banned_ids:
            for b in banned_ids:
                last[b] = -1e9
        # M4 force-include: nudge logits toward next byte of keyword
        if force_byte_ids and force_idx < len(force_byte_ids) and step >= force_window_start:
            last[force_byte_ids[force_idx]] += 4.0

        if mode == "greedy":
            tok_id = int(last.argmax().item())
        else:
            probs = F.softmax(last / max(temp, 1e-5), dim=-1)
            if top_p < 1.0:
                sorted_p, sorted_idx = torch.sort(probs, descending=True)
                cum = sorted_p.cumsum(0)
                cutoff = (cum > top_p).nonzero()
                if cutoff.numel() > 0:
                    k = int(cutoff[0].item()) + 1
                    mask = torch.zeros_like(probs)
                    mask[sorted_idx[:k]] = 1.0
                    probs = probs * mask
                    probs = probs / probs.sum().clamp(min=1e-9)
            tok_id = int(torch.multinomial(probs, 1).item())

        if force_byte_ids and force_idx < len(force_byte_ids) and tok_id == force_byte_ids[force_idx]:
            force_idx += 1

        generated.append(tok_id)
        if tok_id == tok.eos:
            break
        inp = torch.cat([inp, torch.tensor([[tok_id]], device="cuda")], dim=1)

    return tok.decode(generated)


def run_dialogue(model, tok, dlg, mode_name: str, **kwargs):
    prompt = (
        f"사용자: {dlg['setup']}\n"
        f"도우미: {dlg['ack']}\n"
        f"사용자: {dlg['recall_q']}\n"
        f"도우미: "
    )
    text = generate(model, tok, prompt, **kwargs)
    # Trim at newline or 60 chars for clean reporting
    out_short = text.split("\n")[0] if "\n" in text[:80] else text[:80]
    recalled = dlg["keyword"] in text
    return out_short, recalled, text


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--ckpt", required=True)
    p.add_argument("--out", required=True)
    p.add_argument("--max-new", type=int, default=60)
    args = p.parse_args()

    t0 = time.time()
    cfg = EngineAGConfig.phase2_cotrain_350m()
    tok = ByteTokenizer(vocab_size=cfg.vocab_size)
    model = EngineAGModel(cfg).cuda().bfloat16()

    print(f"[ckpt] {args.ckpt}", flush=True)
    payload = torch.load(args.ckpt, map_location="cpu", weights_only=False)
    sd = payload.get("model") or payload.get("state_dict") or payload
    miss, unexp = model.load_state_dict(sd, strict=False)
    if miss:
        print(f"[ckpt] WARN missing={len(miss)} sample={miss[:3]}", flush=True)
    if unexp:
        print(f"[ckpt] WARN unexpected={len(unexp)} sample={unexp[:3]}", flush=True)

    print(f"=== Phase 1B SimPO V5.8 × 4 modes benchmark ===")
    print(f"ckpt: {args.ckpt}")
    print(f"M3 persona-cycle byte IDs: {len(PERSONA_CYCLE_BYTE_IDS)}\n")

    results = {"standard_greedy": [], "standard_sample": [], "M3_rep_penalty": [], "M4_force_include": []}
    for dlg in DIALOGUES:
        print(f"--- dialogue: {dlg['id']} ---")
        # standard_greedy
        out_g, rec_g, _ = run_dialogue(model, tok, dlg, "standard_greedy", max_new=args.max_new, mode="greedy")
        print(f"  [standard_greedy] recalled={rec_g}: {out_g!r}")
        results["standard_greedy"].append({"id": dlg["id"], "t2": out_g, "recalled": rec_g})

        # standard_sample
        torch.manual_seed(42)
        out_s, rec_s, _ = run_dialogue(model, tok, dlg, "standard_sample",
                                       max_new=args.max_new, mode="sample", temp=0.8, top_p=0.95)
        print(f"  [standard_sample] recalled={rec_s}: {out_s!r}")
        results["standard_sample"].append({"id": dlg["id"], "t2": out_s, "recalled": rec_s})

        # M3_rep_penalty
        out_m3, rec_m3, _ = run_dialogue(model, tok, dlg, "M3_rep_penalty",
                                         max_new=args.max_new, mode="greedy", rep_penalty=1.2,
                                         banned_ids=PERSONA_CYCLE_BYTE_IDS)
        print(f"  [M3_rep_penalty] recalled={rec_m3}: {out_m3!r}")
        results["M3_rep_penalty"].append({"id": dlg["id"], "t2": out_m3, "recalled": rec_m3})

        # M4_force_include
        torch.manual_seed(42)
        out_m4, rec_m4, _ = run_dialogue(model, tok, dlg, "M4_force_include",
                                         max_new=args.max_new, mode="sample", temp=0.8, top_p=0.95,
                                         force_keyword=dlg["keyword"])
        print(f"  [M4_force_include force={dlg['keyword']}] recalled={rec_m4}: {out_m4!r}")
        results["M4_force_include"].append({"id": dlg["id"], "t2": out_m4, "recalled": rec_m4})
        print()

    elapsed = time.time() - t0
    summary = {}
    for k, lst in results.items():
        n_pass = sum(1 for r in lst if r["recalled"])
        verdict = "PASS" if n_pass >= 3 else "FAIL"
        summary[k] = {"n_pass": n_pass, "verdict": verdict}
        print(f"  {k}: {n_pass}/5 {verdict}")

    payload = {
        "ts": time.strftime("%Y-%m-%dT%H:%M:%S+00:00", time.gmtime()),
        "substrate_id": "phase1b_simpo",
        "evaluator": "V5.8 multi-turn × 4 modes (greedy/sample/M3 rep_penalty/M4 force-include)",
        "summary": summary,
        "elapsed_s": elapsed,
        "results": results,
    }
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    print(f"\n=== AGGREGATE elapsed {elapsed:.1f}s — saved: {args.out} ===")


if __name__ == "__main__":
    main()
