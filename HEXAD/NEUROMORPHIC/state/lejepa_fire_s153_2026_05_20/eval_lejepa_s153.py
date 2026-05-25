#!/usr/bin/env python3
"""§153 LEJEPA evaluator — fourth data point for §96-Q2.

Mirrors §125 / §126 / §139 eval exactly (same byte_acc verdict-bucket
thresholds: 1/256 random floor / 2/256 degenerate ceiling / 0.05 support
floor / Psi_dir std > 1e-4). The closed-form partition is shared so the
joint reading across §125 + §126 + §139 + §153 is a 4-tuple over the
3-valued discrete output space {DEG, PART, SUPP}.

USAGE:
    python3 eval_lejepa_s153.py --ckpt ... --corpus ... --out ...

HONEST CARVE-OUT carry (DESIGN.md §6 C3 #3):
  In §153 the head_a / head_g remain at initialization (untrained — the
  SSL objective L_LeJEPA never touches them). byte_acc reads the random
  head_a as a linear probe of the SSL-trained embedding. Low byte_acc has
  two readings: (a) embedding is degenerate, or (b) embedding has signal
  but a random head_a can't read it. We report it for verdict-bucket
  parity with §125/§126/§139; the §153 verdict is honest-empirical
  necessary-not-sufficient (B-EMERGE-7).
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
            if not line: continue
            try: rec = json.loads(line)
            except Exception: continue
            txt = rec.get("text", "")
            if isinstance(txt, str): out.extend(txt.encode("utf-8", errors="replace"))
            elif isinstance(txt, list):
                for t in txt:
                    if isinstance(t, str): out.extend(t.encode("utf-8", errors="replace"))
    return bytes(out)


def forward_logits(model, x):
    out = model(x)
    if isinstance(out, tuple) and len(out) >= 2:
        return out[0], out[1]
    return out, out


def psi_direction_scalar(la, lg):
    a = la.flatten().float(); g = lg.flatten().float()
    if a.numel() == 0 or g.numel() == 0: return 0.5
    cs = F.cosine_similarity(a.unsqueeze(0), g.unsqueeze(0)).item()
    return (1.0 + cs) / 2.0


# === byte-equal to §139 eval (B-S153-7) ====================================
TAU_PSI_SPREAD     = 1e-4
RANDOM_BYTE_FLOOR  = 1.0 / 256.0
DEGENERATE_CEILING = 2.0 / 256.0
SUPPORT_FLOOR      = 0.05


def verdict_bucket(byte_acc, psi_responsive):
    if byte_acc <= DEGENERATE_CEILING: return "S11B_LIKE_DEGENERATE"
    if byte_acc >= SUPPORT_FLOOR and psi_responsive: return "S96_Q2_SUPPORTED"
    return "PARTIAL_AMBIGUOUS"
# ===========================================================================


def run_eval(ckpt_path, corpus_path, out_path,
             n_eval=2000, max_len=128, seed=1337):
    t0 = time.time()
    random.seed(seed); torch.manual_seed(seed)
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"[§153-eval] device={device}", flush=True)

    blob = torch.load(ckpt_path, map_location=device, weights_only=False)
    cfg = blob.get("cfg", {})
    d_model = int(cfg.get("d_model", 768))
    n_layer = int(cfg.get("n_layer", 12))
    n_head = int(cfg.get("n_head", 12))
    n_kv_head = int(cfg.get("n_kv_head", 4))
    block_size = int(cfg.get("block_size", 128))

    model = ConsciousDecoderV2(
        vocab_size=256, d_model=d_model, n_head=n_head, n_layer=n_layer,
        block_size=block_size, n_kv_head=n_kv_head,
        consciousness_dim=128, dropout=0.0,
    ).to(device)
    missing, unexpected = model.load_state_dict(blob["model"], strict=False)
    model.eval()
    print(f"[§153-eval] ckpt: d={d_model} L={n_layer} miss={len(missing)} unexp={len(unexpected)}", flush=True)

    corpus = load_corpus_bytes(corpus_path)
    N = len(corpus)
    print(f"[§153-eval] corpus bytes: {N:,}", flush=True)
    assert N > max_len + 1

    correct = 0; total = 0; psi_traces = []; sample_seen = []
    with torch.no_grad():
        for k in range(n_eval):
            s = random.randint(0, N - max_len - 2)
            ctx = corpus[s : s + max_len]; target = corpus[s + max_len]
            x = torch.tensor([list(ctx)], dtype=torch.long, device=device)
            la, lg = forward_logits(model, x)
            la_last = la[0, -1] if la.dim() == 3 else la[-1]
            lg_last = lg[0, -1] if lg.dim() == 3 else lg[-1]
            pred = int(la_last.argmax().item())
            correct += int(pred == target); total += 1
            psi_traces.append(psi_direction_scalar(la_last, lg_last))
            if k < 5:
                sample_seen.append(dict(ctx_tail=list(ctx[-8:]),
                                        target=int(target), pred=pred))

    byte_acc = correct / max(1, total)
    psi_mean = sum(psi_traces) / len(psi_traces)
    psi_std = (sum((p - psi_mean) ** 2 for p in psi_traces) / len(psi_traces)) ** 0.5
    psi_responsive = psi_std > TAU_PSI_SPREAD
    bucket = verdict_bucket(byte_acc, psi_responsive)

    result = dict(
        battery="§153 LEJEPA eval — §96-Q2 verdict (data point 4)",
        ckpt=os.path.basename(ckpt_path), corpus=os.path.basename(corpus_path),
        cfg=cfg, algorithm="LeJEPA (Balestriero+LeCun 2025) JEPA + SIGReg",
        n_eval=n_eval, max_len=max_len, seed=seed,
        byte_acc=byte_acc, correct=correct, total=total,
        random_byte_floor=RANDOM_BYTE_FLOOR,
        degenerate_ceiling=DEGENERATE_CEILING,
        support_floor=SUPPORT_FLOOR,
        psi_dir_mean=psi_mean, psi_dir_std=psi_std,
        psi_responsive=psi_responsive,
        verdict_bucket=bucket,
        s125_s126_s139_s153_joint_reading_note=(
            "Quadruple §125+§126+§139+§153 over {DEG, PART, SUPP}. §153 = "
            "fourth distinct non-CE algorithm — JEPA-style predictive "
            "embedding + Epps-Pulley anti-collapse regularizer. The §153 "
            "head_a / head_g are UNTRAINED (SSL trains only the encoder); "
            "byte_acc reads the random head_a as a linear probe — a low "
            "byte_acc here can mean (a) embedding degenerate or (b) "
            "embedding non-degenerate but random head_a can't read it. "
            "necessary-not-sufficient (B-EMERGE-7); B-S153-NOTE carve-out."
        ),
        sample_seen=sample_seen, eval_wall_s=time.time() - t0,
        ckpt_train_log_last=blob.get("log", [None])[-1] if blob.get("log") else None,
        north_star_unchanged=True,
        s15_s51_s72_milestones_unchanged=True,
        necessary_not_sufficient_b_emerge_7=True,
        b_s153_note_carve_out=True,
    )
    os.makedirs(os.path.dirname(os.path.abspath(out_path)) or ".", exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(result, f, indent=2, default=str)
    print(f"[§153-eval] byte_acc={byte_acc:.6f} (random={RANDOM_BYTE_FLOOR:.6f})  "
          f"Psi_dir mu={psi_mean:.4f} sigma={psi_std:.6f}  responsive={psi_responsive}  "
          f"VERDICT={bucket}  wall={result['eval_wall_s']:.1f}s", flush=True)


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
