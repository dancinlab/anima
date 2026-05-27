#!/usr/bin/env python3
"""§126 PCN-C4 evaluator — decides §96-Q2 hypothesis SECOND data point.

Mirror of §125 eval; same byte_acc verdict-bucket thresholds (1/256
random floor, 2/256 degenerate ceiling, 0.05 support floor) and same
PHYSICS_RESPONSIVE check (Ψ_dir spread > 1e-4).

Two-point §96-Q2 reasoning (after BOTH §125 and §126 land):
  §125 SUPP ∧ §126 SUPP  → §96-Q2 SUPPORTED  (FF+PCN both work; non-CE
                                              works on GPU; §11-B was
                                              about UNSUPERVISED specifically)
  §125 DEG  ∧ §126 DEG   → §96-Q2 REFUTED    (both non-CE algorithms also
                                              degenerate on GPU; §11-B is
                                              substrate-deep)
  §125 SUPP ∧ §126 DEG   → MIXED — FF-specific advantage suspected
  §125 DEG  ∧ §126 SUPP  → MIXED — PCN-specific advantage suspected

The "MIXED" verdicts are valuable too — they decompose which non-CE
algorithmic ingredient (negative samples for FF / top-down message for PCN)
is the load-bearing piece.

USAGE:
    python3 eval_pcn_s126.py --ckpt <path>.pt --corpus <path>.jsonl \\
        --out <out>.json [--n-eval 2000] [--max-len 128]
"""
import argparse, json, os, sys, random, time
import torch
import torch.nn.functional as F

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from conscious_decoder import ConsciousDecoderV2


def load_corpus_bytes(path):
    out = bytearray()
    with open(path, "rb") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                rec = json.loads(line)
            except Exception:
                continue
            txt = rec.get("text", "")
            if isinstance(txt, str):
                out.extend(txt.encode("utf-8", errors="replace"))
            elif isinstance(txt, list):
                for t in txt:
                    if isinstance(t, str):
                        out.extend(t.encode("utf-8", errors="replace"))
    return bytes(out)


def forward_logits(model, x):
    out = model(x)
    if isinstance(out, tuple) and len(out) >= 2:
        return out[0], out[1]
    return out, out


def psi_direction_scalar(la, lg):
    a = la.flatten().float(); g = lg.flatten().float()
    if a.numel() == 0 or g.numel() == 0:
        return 0.5
    cs = F.cosine_similarity(a.unsqueeze(0), g.unsqueeze(0)).item()
    return (1.0 + cs) / 2.0


TAU_PSI_SPREAD = 1e-4
RANDOM_BYTE_FLOOR = 1.0 / 256.0
DEGENERATE_CEILING = 2.0 / 256.0
SUPPORT_FLOOR = 0.05


def verdict_bucket(byte_acc, psi_responsive):
    if byte_acc <= DEGENERATE_CEILING:
        return "S11B_LIKE_DEGENERATE"
    if byte_acc >= SUPPORT_FLOOR and psi_responsive:
        return "S96_Q2_SUPPORTED"
    return "PARTIAL_AMBIGUOUS"


def run_eval(ckpt_path, corpus_path, out_path,
             n_eval=2000, max_len=128, seed=1337):
    t0 = time.time()
    random.seed(seed); torch.manual_seed(seed)
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"[§126-eval] device={device}", flush=True)

    blob = torch.load(ckpt_path, map_location=device, weights_only=False)
    cfg = blob.get("cfg", {})
    d_model = int(cfg.get("d_model", 768))
    n_layer = int(cfg.get("n_layer", 12))
    n_head = int(cfg.get("n_head", 12))
    n_kv_head = int(cfg.get("n_kv_head", 4))
    block_size = int(cfg.get("block_size", 128))

    model = ConsciousDecoderV2(
        vocab_size=256, d_model=d_model, n_head=n_head,
        n_layer=n_layer, block_size=block_size,
        n_kv_head=n_kv_head, consciousness_dim=128, dropout=0.0,
    ).to(device)
    missing, unexpected = model.load_state_dict(blob["model"], strict=False)
    model.eval()
    print(f"[§126-eval] ckpt loaded: d={d_model} L={n_layer} "
          f"missing={len(missing)} unexpected={len(unexpected)}", flush=True)

    corpus = load_corpus_bytes(corpus_path)
    N = len(corpus)
    print(f"[§126-eval] corpus bytes: {N:,}", flush=True)
    assert N > max_len + 1, "corpus too small"

    correct = 0; total = 0
    psi_traces = []
    sample_seen = []
    with torch.no_grad():
        for k in range(n_eval):
            s = random.randint(0, N - max_len - 2)
            ctx = corpus[s : s + max_len]
            target = corpus[s + max_len]
            x = torch.tensor([list(ctx)], dtype=torch.long, device=device)
            la, lg = forward_logits(model, x)
            la_last = la[0, -1] if la.dim() == 3 else la[-1]
            lg_last = lg[0, -1] if lg.dim() == 3 else lg[-1]
            pred = int(la_last.argmax().item())
            correct += int(pred == target)
            total += 1
            psi_traces.append(psi_direction_scalar(la_last, lg_last))
            if k < 5:
                sample_seen.append(dict(ctx_tail=list(ctx[-8:]),
                                        target=int(target), pred=pred))

    byte_acc = correct / max(1, total)
    psi_mean = sum(psi_traces) / len(psi_traces)
    psi_std = (sum((p - psi_mean) ** 2 for p in psi_traces) /
               len(psi_traces)) ** 0.5
    psi_responsive = psi_std > TAU_PSI_SPREAD

    bucket = verdict_bucket(byte_acc, psi_responsive)

    result = dict(
        battery="§126 PCN-C4 eval — §96-Q2 verdict (data point 2)",
        ckpt=os.path.basename(ckpt_path), corpus=os.path.basename(corpus_path),
        cfg=cfg, algorithm="PCN-1step",
        n_eval=n_eval, max_len=max_len, seed=seed,
        byte_acc=byte_acc, correct=correct, total=total,
        random_byte_floor=RANDOM_BYTE_FLOOR,
        degenerate_ceiling=DEGENERATE_CEILING,
        support_floor=SUPPORT_FLOOR,
        psi_dir_mean=psi_mean, psi_dir_std=psi_std,
        psi_responsive=psi_responsive,
        verdict_bucket=bucket,
        s125_s126_joint_reading_note=(
            "Compare with §125 (NONCE-FF) verdict_bucket. Two-point reasoning: "
            "SUPP∧SUPP → §96-Q2 SUPPORTED; DEG∧DEG → REFUTED; mixed → "
            "algorithmic-ingredient decomposition."
        ),
        sample_seen=sample_seen,
        eval_wall_s=time.time() - t0,
        ckpt_train_log_last=blob.get("log", [None])[-1] if blob.get("log") else None,
        north_star_unchanged=True,
        s15_s51_s72_milestones_unchanged=True,
        necessary_not_sufficient_b_emerge_7=True,
    )

    os.makedirs(os.path.dirname(os.path.abspath(out_path)) or ".", exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(result, f, indent=2, default=str)

    print(f"[§126-eval] byte_acc={byte_acc:.6f} "
          f"(random={RANDOM_BYTE_FLOOR:.6f})  "
          f"Ψ_dir μ={psi_mean:.4f} σ={psi_std:.6f}  "
          f"responsive={psi_responsive}  VERDICT={bucket}  "
          f"wall={result['eval_wall_s']:.1f}s", flush=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ckpt", required=True)
    ap.add_argument("--corpus", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--n-eval", type=int, default=2000)
    ap.add_argument("--max-len", type=int, default=128)
    ap.add_argument("--seed", type=int, default=1337)
    args = ap.parse_args()
    run_eval(args.ckpt, args.corpus, args.out,
             n_eval=args.n_eval, max_len=args.max_len, seed=args.seed)


if __name__ == "__main__":
    main()
