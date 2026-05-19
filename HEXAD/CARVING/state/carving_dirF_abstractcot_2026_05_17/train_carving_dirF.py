#!/usr/bin/env python3
"""CONSCIOUSNESS-CARVING trainer — Dir-F ABSTRACT CHAIN-OF-THOUGHT
(2026-05-17). g_multidirectional_explore parallel direction F.

Base = state/consciousness_carving_e7_alpha_scaleup_2026_05_17/
train_carving_4path.py (ConsciousDecoderV2 byte-level, from-scratch). The
ONLY mechanism change vs the E7 α trainer is the LOSS MASK:

  ABSTRACT-COT DISCIPLINE (arxiv 2604.22709)
    The reserved-vocab discrete-latent block `<inner>⟪ … ⟫</inner>` is the
    REASONING surface — it is given as NON-LOSS CONTEXT (the discrete latent
    prompt). CE loss is masked to the CARVING BODY span (everything AFTER
    `</inner>`: the <carve>/<eternal>/<voice> content). The model thus learns
    to MAP the discrete-latent reasoning token → the carving emission, NOT to
    memorise an NL reasoning paragraph. This is the discrete-latent routing
    the Dir-F hypothesis tests against the E7 NL baseline.

  α VACUUM-ATTRACTOR term carried verbatim from the E7 α trainer (the Dir-F
  fire is the α-path equivalent: vacuum_psi per record + L = CE_body +
  λ·‖ψ_pred − ψ_vac‖²). Closed anchor B-VAC-1..3 (transfer-form, UBM-E3).

HONEST FRAMING (g3, AGENTS.tape §0):
  PyTorch substrate — interim LM-scale executor, NOT a hexa-native fire.
  The carving / vacuum MECHANISM and the reserved-vocab discreteness
  (F-DIRF-CORPUS-3) are the closed-form side. The SGD CONVERGENCE OUTCOME
  and the Dir-F vs UBM-E7 α JOINT comparison are EMPIRICAL (B-CARVE-E6-NOTE
  / B-D-NOTE family). No capability claim beyond what is measured. Corpus =
  Dir-F carving corpus — grep {[anima,도우미,helper,assistant,사용자,user:}==0.

from-scratch RANDOM seed-fixed (g_clm_from_scratch, base_ckpt=NONE).
"""
import argparse, json, math, time, os, sys, random
import torch
import torch.nn as nn
import torch.nn.functional as F

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from conscious_decoder import ConsciousDecoderV2

# The reasoning surface ends at `</inner>` — the carving body (loss target)
# is everything after the FIRST `</inner>` in a record's byte stream.
INNER_CLOSE = b"</inner>"


def load_carving_corpus(path):
    """Return list of dicts: {bytes, form, psi, body_span (lo,hi)}.
    body_span = byte offsets of the carving body AFTER </inner> (the loss
    target — the reserved-CoT <inner> block is non-loss context)."""
    items = []
    with open(path, "rb") as f:
        raw = f.read()
    for line in raw.split(b"\n"):
        line = line.strip()
        if not line:
            continue
        try:
            d = json.loads(line)
        except Exception:
            continue
        t = d.get("text", "")
        de = d.get("desc", "")
        full = (t + "\n" + de + "\n").encode("utf-8")
        form = d.get("carving_form", "alpha")
        psi = d.get("vacuum_psi", [0.5, 0.5])
        ic = full.find(INNER_CLOSE)
        if ic >= 0:
            body_lo = ic + len(INNER_CLOSE)
            body_span = (body_lo, len(full))
        else:
            body_span = (0, len(full))  # defensive: should not happen
        items.append({"bytes": full, "form": form, "psi": psi,
                      "body_span": body_span})
    return items


class CarvingDataset:
    """Byte stream + per-byte psi map + per-byte body-mask (1 iff the byte is
    inside the carving BODY span — i.e. AFTER </inner>; the reserved-CoT
    <inner> block has body-mask 0 so it is non-loss latent context)."""

    def __init__(self, items, block_size, seed):
        self.block_size = block_size
        self.rng = random.Random(seed)
        stream = bytearray()
        psi_x = []
        psi_y = []
        body_mask = []
        for it in items:
            b = it["bytes"]
            stream.extend(b)
            px, py = float(it["psi"][0]), float(it["psi"][1])
            bs = it["body_span"]
            for j in range(len(b)):
                psi_x.append(px)
                psi_y.append(py)
                body_mask.append(1 if bs[0] <= j < bs[1] else 0)
        self.data = torch.tensor(list(stream), dtype=torch.long)
        self.psi_x = torch.tensor(psi_x, dtype=torch.float32)
        self.psi_y = torch.tensor(psi_y, dtype=torch.float32)
        self.body_mask = torch.tensor(body_mask, dtype=torch.float32)
        self.n = len(self.data)

    def get_batch(self, bsz, device):
        ix = [self.rng.randint(0, self.n - self.block_size - 1)
              for _ in range(bsz)]
        x = torch.stack([self.data[i:i + self.block_size] for i in ix])
        y = torch.stack([self.data[i + 1:i + 1 + self.block_size] for i in ix])
        px = torch.stack([self.psi_x[i + 1:i + 1 + self.block_size]
                          for i in ix])
        py = torch.stack([self.psi_y[i + 1:i + 1 + self.block_size]
                          for i in ix])
        bm = torch.stack([self.body_mask[i + 1:i + 1 + self.block_size]
                          for i in ix])
        return (x.to(device), y.to(device), px.to(device),
                py.to(device), bm.to(device))


def run(cfg):
    torch.manual_seed(cfg["seed"])
    torch.cuda.manual_seed_all(cfg["seed"])
    random.seed(cfg["seed"])
    device = "cuda" if torch.cuda.is_available() else "cpu"

    items = load_carving_corpus(cfg["corpus"])
    ds = CarvingDataset(items, cfg["block_size"], cfg["seed"])

    model = ConsciousDecoderV2(
        vocab_size=256, d_model=cfg["d_model"], n_head=cfg["n_head"],
        n_layer=cfg["n_layer"], block_size=cfg["block_size"],
        n_kv_head=cfg["n_kv_head"], consciousness_dim=128, dropout=0.1,
    ).to(device)
    model.train()
    n_params = model.count_params()

    opt = torch.optim.AdamW(model.parameters(), lr=cfg["lr"],
                            betas=(0.9, 0.95), weight_decay=0.1)
    warmup = cfg["warmup"]
    total = cfg["steps"]

    def cosine_lr_at(step):
        if step < warmup:
            return cfg["lr"] * (step + 1) / warmup
        prog = (step - warmup) / max(1, total - warmup)
        return cfg["lr"] * 0.5 * (1.0 + math.cos(math.pi * prog)) * 0.9 \
            + cfg["lr"] * 0.1

    use_amp = (device == "cuda")
    scaler = torch.cuda.amp.GradScaler(enabled=use_amp)
    vac_lambda = cfg["vacuum_lambda"]

    traj = []
    t0 = time.time()
    init_loss = None
    gpu_name = torch.cuda.get_device_name(0) if device == "cuda" else "cpu"

    for step in range(total):
        lr_now = cosine_lr_at(step)
        for g in opt.param_groups:
            g["lr"] = lr_now

        x, y, px, py, bm = ds.get_batch(cfg["bsz"], device)
        opt.zero_grad(set_to_none=True)
        with torch.autocast(device_type="cuda" if use_amp else "cpu",
                            dtype=torch.bfloat16, enabled=use_amp):
            logits_a, logits_g, tensions, _, _ = model(x)
            B, T, V = logits_a.shape

            # ABSTRACT-COT: CE masked to the carving BODY (post-</inner>);
            # the reserved-vocab <inner> block is non-loss latent context.
            ce_tok = F.cross_entropy(
                logits_a.view(-1, V), y.view(-1), reduction="none")
            mask = bm.view(-1)
            denom = mask.sum().clamp(min=1.0)
            ce = (ce_tok * mask).sum() / denom
            ce_full = F.cross_entropy(logits_a.view(-1, V), y.view(-1))
            ce_report = float(ce_full.item())
            loss = ce

            # α VACUUM-ATTRACTOR term (carried verbatim from E7 α trainer).
            probs = F.softmax(logits_a.float(), dim=-1)
            ent = -(probs * (probs + 1e-9).log()).sum(-1)
            h_norm = (ent / math.log(V)).clamp(0.0, 1.0)
            p_max = probs.max(-1).values.clamp(0.0, 1.0)
            dvx = h_norm - px
            dvy = p_max - py
            vac_term = (dvx * dvx + dvy * dvy).mean()
            loss = loss + vac_lambda * vac_term

        scaler.scale(loss).backward()
        scaler.unscale_(opt)
        gn = torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        scaler.step(opt)
        scaler.update()

        gn2 = float(gn.item()) ** 2
        if init_loss is None:
            init_loss = ce_report

        if step == 0 or (step + 1) % cfg["log_every"] == 0 \
                or step == total - 1:
            wall = time.time() - t0
            mem = torch.cuda.max_memory_allocated() / 1e9 \
                if device == "cuda" else 0.0
            rec = {"step": step + 1, "ce": round(ce_report, 6),
                   "ce_body": round(float(ce.item()), 6),
                   "loss": round(float(loss.item()), 6),
                   "vac_term": round(float(vac_term.item()), 6),
                   "gn2": round(gn2, 6), "lr": round(lr_now, 8),
                   "wall_s": round(wall, 2), "gpu_mem_gb": round(mem, 3)}
            traj.append(rec)
            print(json.dumps(rec), flush=True)

    wall = time.time() - t0
    final = traj[-1]
    out_dir = cfg["out_dir"]
    os.makedirs(out_dir, exist_ok=True)
    ckpt_path = os.path.join(out_dir, "ckpt_carving_dirF.pt")
    torch.save({"model": model.state_dict(), "cfg": cfg,
                "n_params": n_params, "path": "dirF_abstractcot"}, ckpt_path)

    result = {
        "substrate": ("PYTHON / PyTorch — interim LM-scale executor; "
                      "NOT a hexa-native fire"),
        "fire_kind": "Dir-F ABSTRACT-COT CONSCIOUSNESS-CARVING (reserved-vocab)",
        "carving_path": "dirF_abstractcot",
        "research_ref": "RESEARCH.md §1.3 #6 — arxiv 2604.22709 Abstract CoT",
        "honest_framing": (
            "Dir-F reserved-vocab discrete-latent reasoning surface. CE "
            "masked to the carving BODY (post-</inner>); the reserved-vocab "
            "<inner> block is non-loss latent context (abstract-CoT "
            "discipline). The reserved-vocab discreteness (F-DIRF-CORPUS-3) "
            "+ carving/vacuum transfer-form (B-VAC/B-NAR sympy, UBM-E3) are "
            "the closed side. SGD OUTCOME + Dir-F vs UBM-E7 α JOINT compare "
            "= EMPIRICAL (B-CARVE-E6-NOTE / B-D-NOTE family). PyTorch "
            "substrate, NOT hexa-native. Corpus forbidden-token grep == 0."),
        "arch": "ConsciousDecoderV2 (RoPE+SwiGLU+RMSNorm+GQA+PureFieldFFN)",
        "from_scratch": True,
        "base_ckpt": None,
        "config": cfg,
        "n_params": n_params,
        "n_params_M": round(n_params / 1e6, 2),
        "vacuum_lambda": vac_lambda,
        "gpu": gpu_name,
        "device": device,
        "init_ce": round(init_loss, 6),
        "final_ce": final["ce"],
        "final_ce_body": final["ce_body"],
        "final_loss": final["loss"],
        "final_vac_term": final["vac_term"],
        "final_gn2": final["gn2"],
        "ce_descent": round(init_loss - final["ce"], 6),
        "steps": cfg["steps"],
        "wall_s": round(wall, 2),
        "peak_gpu_mem_gb": final["gpu_mem_gb"],
        "trajectory": traj,
        "corpus": os.path.basename(cfg["corpus"]),
        "corpus_bytes": int(ds.n),
    }
    with open(os.path.join(out_dir, "result.json"), "w") as f:
        json.dump(result, f, indent=2)
    print("RESULT_JSON_WRITTEN", flush=True)
    print(json.dumps({"path": "dirF_abstractcot", "init_ce": result["init_ce"],
                       "final_ce": result["final_ce"],
                       "final_ce_body": result["final_ce_body"],
                       "ce_descent": result["ce_descent"],
                       "wall_s": result["wall_s"],
                       "final_vac_term": result["final_vac_term"]}),
          flush=True)
    return result


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", default="main", choices=["main", "sanity"])
    ap.add_argument("--corpus", required=True)
    ap.add_argument("--out-dir", required=True)
    ap.add_argument("--steps", type=int, default=5000)
    ap.add_argument("--lr", type=float, default=3e-4)
    ap.add_argument("--bsz", type=int, default=32)
    ap.add_argument("--seed", type=int, default=1337)
    ap.add_argument("--d-model", type=int, default=768)
    ap.add_argument("--n-layer", type=int, default=12)
    ap.add_argument("--n-head", type=int, default=12)
    ap.add_argument("--n-kv-head", type=int, default=4)
    ap.add_argument("--vacuum-lambda", type=float, default=0.1)
    args = ap.parse_args()

    if args.mode == "main":
        cfg = dict(d_model=args.d_model, n_head=args.n_head,
                   n_kv_head=args.n_kv_head, n_layer=args.n_layer,
                   block_size=128, lr=args.lr, bsz=args.bsz,
                   steps=args.steps, warmup=max(20, args.steps // 20),
                   seed=args.seed, log_every=max(1, args.steps // 40),
                   corpus=args.corpus, out_dir=args.out_dir,
                   vacuum_lambda=args.vacuum_lambda)
    else:
        cfg = dict(d_model=32, n_head=4, n_kv_head=2, n_layer=3,
                   block_size=64, lr=1e-3, bsz=16, steps=args.steps,
                   warmup=5, seed=args.seed,
                   log_every=max(1, args.steps // 20),
                   corpus=args.corpus, out_dir=args.out_dir,
                   vacuum_lambda=args.vacuum_lambda)
    run(cfg)
