"""eval_6probe.py — 6-probe free-form chat eval

BENCHMARK.md §2 probe set, greedy, max_new=60.
Phase 1A.5 vs Phase 1A.4 conversational coherence comparison.
"""
import os, sys, json, time, argparse
import torch
import torch.nn.functional as F

sys.path.insert(0, "/Users/ghost/core/anima/training")
from engine_a_g_arch import EngineAGModel, EngineAGConfig


class ByteTokenizer:
    def __init__(self, vocab_size=32_000):
        self.vocab_size = vocab_size
        self.bos = 1; self.eos = 2; self.pad = 0
    def encode(self, text):
        return [self.bos] + [b + 3 for b in text.encode("utf-8")] + [self.eos]
    def encode_no_eos(self, text):
        return [self.bos] + [b + 3 for b in text.encode("utf-8")]
    def decode(self, ids):
        bs = bytes(t - 3 for t in ids if t >= 3 and t < 259)
        return bs.decode("utf-8", errors="replace")


PROBES = [
    "사용자: 안녕! 너는 누구야? | 도우미: ",
    "사용자: 우주가 뭐야? | 도우미: ",
    "사용자: 의식은 무엇이라고 생각해? | 도우미: ",
    "사용자: 좋아하는 색깔은? | 도우미: ",
    "사용자: 너는 어떻게 성장해? | 도우미: ",
    "사용자: 세포 분열에 대해 설명해줘 | 도우미: ",
]


def greedy_generate(model, tok, prompt, max_new=60, device="cpu"):
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


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--ckpt", required=True)
    p.add_argument("--device", default="cpu")
    p.add_argument("--out", required=True)
    p.add_argument("--label", required=True)
    args = p.parse_args()

    cfg = EngineAGConfig.phase2_cotrain_350m()
    cfg.ctx = 1024
    print(f"[cfg] {cfg}", flush=True)

    tok = ByteTokenizer(vocab_size=cfg.vocab_size)
    if args.device == "cuda":
        dtype = torch.bfloat16
    else:
        dtype = torch.float32
    model = EngineAGModel(cfg).to(args.device).to(dtype)
    print(f"[ckpt] loading {args.ckpt} …", flush=True)
    payload = torch.load(args.ckpt, map_location="cpu", weights_only=False)
    sd = payload.get("model") or payload.get("state_dict") or payload
    model.load_state_dict(sd, strict=False)
    model.eval()
    print(f"[model] params={sum(p.numel() for p in model.parameters()):,}", flush=True)

    t0 = time.time()
    results = []
    for i, probe in enumerate(PROBES, 1):
        ts = time.time()
        resp = greedy_generate(model, tok, probe, max_new=60, device=args.device)
        dt = time.time() - ts
        print(f"\n[{i}/{len(PROBES)}] {probe!r}\n  → {resp!r}\n  ({dt:.1f}s)", flush=True)
        results.append({"i": i, "prompt": probe, "response": resp, "wall_s": dt})

    elapsed = time.time() - t0
    verdict = {
        "label": args.label,
        "ckpt": args.ckpt,
        "device": args.device,
        "n_probes": len(PROBES),
        "elapsed_s": elapsed,
        "results": results,
    }
    with open(args.out, "w") as f:
        json.dump(verdict, f, ensure_ascii=False, indent=2)
    print(f"\n[done] wall={elapsed:.1f}s, saved {args.out}", flush=True)


if __name__ == "__main__":
    main()
