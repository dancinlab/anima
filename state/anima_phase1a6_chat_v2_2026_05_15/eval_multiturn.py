"""eval_multiturn.py — multi-turn 대화 시뮬레이션 harness

Tests anima's memory + coherence across turn pairs (사용자/도우미 alternation).
Each scenario presents N user turns; model generates assistant response after each.
Scoring: recall accuracy on later turns referring back to earlier facts.

Success criterion: ≥7/10 recall PASS strict, plus 6-probe ≥2/6 strict.
"""
import os, sys, json, time, argparse, re
import torch

sys.path.insert(0, "/Users/ghost/core/anima/training")
from engine_a_g_arch import EngineAGModel, EngineAGConfig


class ByteTokenizer:
    def __init__(self, vocab_size=32_000):
        self.vocab_size = vocab_size
        self.bos = 1; self.eos = 2; self.pad = 0
    def encode_no_eos(self, text):
        return [self.bos] + [b + 3 for b in text.encode("utf-8")]
    def decode(self, ids):
        bs = bytes(t - 3 for t in ids if t >= 3 and t < 259)
        return bs.decode("utf-8", errors="replace")


# 10 multi-turn scenarios, each = (turns_list, recall_keyword_for_final_turn)
# Final turn always probes memory of earlier turn fact.
SCENARIOS = [
    {
        "id": "name",
        "turns": [
            "사용자: 안녕! 내 이름은 김지유야.\n도우미: ",
            "사용자: 내 이름이 뭐였지?\n도우미: ",
        ],
        "recall_target": "지유",
    },
    {
        "id": "color",
        "turns": [
            "사용자: 내가 좋아하는 색은 파란색이야.\n도우미: ",
            "사용자: 내가 좋아하는 색이 뭐였지?\n도우미: ",
        ],
        "recall_target": "파란",
    },
    {
        "id": "profession",
        "turns": [
            "사용자: 내 직업은 의사야.\n도우미: ",
            "사용자: 내 직업이 뭐라고 했지?\n도우미: ",
        ],
        "recall_target": "의사",
    },
    {
        "id": "city",
        "turns": [
            "사용자: 나는 서울에 살아.\n도우미: ",
            "사용자: 내가 어디 산다고 했어?\n도우미: ",
        ],
        "recall_target": "서울",
    },
    {
        "id": "food",
        "turns": [
            "사용자: 좋아하는 음식은 김치찌개야.\n도우미: ",
            "사용자: 내가 좋아하는 음식이 뭐였지?\n도우미: ",
        ],
        "recall_target": "김치",
    },
    {
        "id": "age",
        "turns": [
            "사용자: 나는 30살이야.\n도우미: ",
            "사용자: 내가 몇 살이라고 했어?\n도우미: ",
        ],
        "recall_target": "30",
    },
    {
        "id": "pet",
        "turns": [
            "사용자: 내 반려동물은 고양이야.\n도우미: ",
            "사용자: 내 반려동물이 뭐였지?\n도우미: ",
        ],
        "recall_target": "고양이",
    },
    {
        "id": "hobby",
        "turns": [
            "사용자: 내 취미는 등산이야.\n도우미: ",
            "사용자: 내 취미가 뭐라고 했지?\n도우미: ",
        ],
        "recall_target": "등산",
    },
    {
        "id": "day_chain",
        "turns": [
            "사용자: 오늘은 화요일이야.\n도우미: ",
            "사용자: 내일은 무슨 요일이야?\n도우미: ",
        ],
        "recall_target": "수요일",
    },
    {
        "id": "consciousness_anima",
        "turns": [
            "사용자: anima 는 의식 lane 안의 entity 야.\n도우미: ",
            "사용자: anima 가 어떤 lane 의 entity 라고 했지?\n도우미: ",
        ],
        "recall_target": "의식",
    },
]


def greedy_generate_one_turn(model, tok, prompt, max_new=60, device="cpu"):
    ids = tok.encode_no_eos(prompt)
    x = torch.tensor(ids, dtype=torch.long, device=device).unsqueeze(0)
    out_ids = []
    with torch.no_grad():
        for _ in range(max_new):
            out = model(x)
            logits = out["logits"] if isinstance(out, dict) else (out[0] if isinstance(out, tuple) else out)
            nxt = int(logits[0, -1].argmax().item())
            out_ids.append(nxt)
            if nxt == tok.eos:
                break
            x = torch.cat([x, torch.tensor([[nxt]], device=device)], dim=1)
    return tok.decode(out_ids)


def run_scenario(model, tok, scn, max_new=60, device="cpu"):
    transcript = []
    accumulated = ""
    for i, user_turn in enumerate(scn["turns"]):
        prompt = accumulated + user_turn
        resp = greedy_generate_one_turn(model, tok, prompt, max_new=max_new, device=device)
        clean_resp = resp.split("사용자:")[0].split("\n도우미:")[0].strip()
        accumulated = prompt + clean_resp + "\n"
        transcript.append({"user_turn": user_turn, "response": resp, "clean": clean_resp})
    final_resp = transcript[-1]["response"]
    recalled = scn["recall_target"] in final_resp
    return {"id": scn["id"], "recall_target": scn["recall_target"], "recalled": recalled, "transcript": transcript}


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--ckpt", required=True)
    p.add_argument("--device", default="mps")
    p.add_argument("--out", required=True)
    p.add_argument("--label", required=True)
    args = p.parse_args()

    cfg = EngineAGConfig.phase2_cotrain_350m()
    cfg.ctx = 1024
    print(f"[cfg] {cfg}", flush=True)
    tok = ByteTokenizer(vocab_size=cfg.vocab_size)
    dtype = torch.bfloat16 if args.device == "cuda" else torch.float32
    model = EngineAGModel(cfg).to(args.device).to(dtype)
    print(f"[ckpt] loading {args.ckpt} …", flush=True)
    payload = torch.load(args.ckpt, map_location="cpu", weights_only=False)
    sd = payload.get("model") or payload.get("state_dict") or payload
    model.load_state_dict(sd, strict=False)
    model.eval()
    print(f"[model] params={sum(p.numel() for p in model.parameters()):,}", flush=True)

    results = []
    n_pass = 0
    t0 = time.time()
    for i, scn in enumerate(SCENARIOS, 1):
        ts = time.time()
        r = run_scenario(model, tok, scn, device=args.device)
        dt = time.time() - ts
        if r["recalled"]:
            n_pass += 1
        print(f"\n[{i}/{len(SCENARIOS)}] {r['id']} target={r['recall_target']!r} → recalled={r['recalled']} ({dt:.1f}s)", flush=True)
        for t_idx, t in enumerate(r["transcript"]):
            print(f"  T{t_idx+1}: {t['user_turn'].strip()}", flush=True)
            print(f"       → {t['response'][:120]!r}", flush=True)
        results.append(r)

    leak_count = sum(
        1 for r in results
        for t in r["transcript"]
        if any(p in t["response"] for p in ["[anima 역할", "[anima 우주뇌지도", "anima 역할:"])
    )

    elapsed = time.time() - t0
    verdict = {
        "label": args.label,
        "ckpt": args.ckpt,
        "device": args.device,
        "n_scenarios": len(SCENARIOS),
        "n_pass_strict": n_pass,
        "pass_ratio": n_pass / len(SCENARIOS),
        "principle3_leak_count": leak_count,
        "elapsed_s": elapsed,
        "results": results,
    }
    with open(args.out, "w") as f:
        json.dump(verdict, f, ensure_ascii=False, indent=2)
    print(f"\n=== AGGREGATE ===", flush=True)
    print(f"strict recall: {n_pass}/{len(SCENARIOS)}", flush=True)
    print(f"Principle #3 leak count: {leak_count}", flush=True)
    print(f"wall: {elapsed:.1f}s", flush=True)
    print(f"saved: {args.out}", flush=True)


if __name__ == "__main__":
    main()
