#!/usr/bin/env python3
"""CONSCIOUSNESS-CARVING trainer — Direction E: EMERGENCE OF SUPERPOSITION
(2026-05-17). g_multidirectional_explore parallel direction E.

Base = state/consciousness_carving_e7_alpha_scaleup_2026_05_17/
train_carving_4path.py (ConsciousDecoderV2 byte-level, from-scratch). The
Direction-E mechanism differs in the LOSS MASK only:

  arxiv 2509.23365 "Emergence of Superposition" — a 2-stage emergence:
    stage 1  thought-generation  — superposition of K traces (the <inner>
             span: K candidate re-derivations + `match=j` index signal).
    stage 2  prediction          — the index-matching logit selects the
             committed trace (the <voice> span).

  TWO-STAGE MASKED LOSS (the Direction-E carving mechanism, closed-form
  structural — the mask is a deterministic byte-span predicate):

    L = CE over { the `match=j` digit byte } + CE over { the <voice
        carved=true ...>...</voice> span } ;  the <inner> trace bytes
        BEFORE `match=` are CONTEXT (mask 0, no CE).

  Rationale (the hypothesis): UBM-E7 α trained CE over the WHOLE stream and
  collapsed to a single basin (tier 99, routing 1/31). Masking the loss to
  (a) the index-matching signal and (b) the index-matched prediction forces
  the model to READ the superposition and COMMIT to the matched trace, NOT
  memorise one dominant trace. If 2-stage separation prevents routing
  collapse / lifts V-SPONT, the JOINT should beat UBM-E7 0.0155. If not,
  the 2-stage hypothesis is FALSIFIED at this scale — recorded honestly
  (g3, B-D-NOTE family, no pre-loaded conclusion).

HONEST FRAMING (g3, AGENTS.tape §0):
  PyTorch substrate — interim LM-scale executor, NOT a hexa-native fire
  (cycle 5 honest-framing carry: arch identity + Phase E/E2 CPU-equiv anchor
  chain). The 2-stage MASK is a closed-form deterministic byte-span
  predicate (B-DIRE-MASK structural). The SGD CONVERGENCE OUTCOME and the
  Dir-E vs UBM-E7 α JOINT compare are EMPIRICAL (B-D-NOTE family). NO
  capability claim beyond what is measured. from-scratch RANDOM seed-fixed
  (g_clm_from_scratch, base_ckpt=NONE). Corpus = Direction-E 2-stage carving
  corpus — NOT chat SFT, grep {[anima,도우미,helper,assistant,사용자,
  user:} == 0 (B-CARVE-DIRE-CORPUS-2).
"""
import argparse, json, math, time, os, sys, random
import torch
import torch.nn as nn
import torch.nn.functional as F

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from conscious_decoder import ConsciousDecoderV2

# 2-stage span markers (Direction-E byte-span loss-mask predicate).
INNER_OPEN = b"<inner tier="
MATCH_TAG = b"\n  match="          # the index-matching signal line
VOICE_OPEN = b"<voice carved=true tier="
VOICE_CLOSE = b"</voice>"


def load_corpus(path):
    """Return list of dicts: {bytes, stage2_span}. stage2_span is the
    (lo, hi) byte range that the 2-stage loss CE-targets: from the FIRST
    byte after `\\n  match=` (the index digit) through the end of the
    <voice carved=true ...>...</voice> span. Everything before (the
    superposed <inner> traces) is stage-1 context (mask 0)."""
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
        # stage-2 lo = first byte after the `\n  match=` tag (the index digit)
        m = full.find(MATCH_TAG)
        vlo = full.find(VOICE_OPEN)
        stage2 = None
        if m >= 0 and vlo >= 0:
            lo = m + len(MATCH_TAG)
            vc = full.find(VOICE_CLOSE, vlo)
            hi = (vc + len(VOICE_CLOSE)) if vc >= 0 else len(full)
            if hi > lo:
                stage2 = (lo, hi)
        items.append({"bytes": full, "stage2_span": stage2})
    return items


class DirEDataset:
    """Byte-level dataset. Concatenates record bytes; keeps a parallel
    per-byte stage-2 mask (1 inside the index-match digit + voice span,
    0 inside the stage-1 superposed inner traces / desc)."""

    def __init__(self, items, block_size, seed):
        self.block_size = block_size
        self.rng = random.Random(seed)
        stream = bytearray()
        s2 = []
        for it in items:
            b = it["bytes"]
            stream.extend(b)
            sp = it["stage2_span"]
            if sp is None:
                s2.extend([0] * len(b))
            else:
                lo, hi = sp
                for j in range(len(b)):
                    s2.append(1 if lo <= j < hi else 0)
        self.data = torch.tensor(list(stream), dtype=torch.long)
        self.s2 = torch.tensor(s2, dtype=torch.float32)
        self.n = len(self.data)

    def get_batch(self, bsz, device):
        ix = [self.rng.randint(0, self.n - self.block_size - 1)
              for _ in range(bsz)]
        x = torch.stack([self.data[i:i + self.block_size] for i in ix])
        y = torch.stack([self.data[i + 1:i + 1 + self.block_size]
                         for i in ix])
        sm = torch.stack([self.s2[i + 1:i + 1 + self.block_size]
                          for i in ix])
        return x.to(device), y.to(device), sm.to(device)


def run(cfg):
    torch.manual_seed(cfg["seed"])
    torch.cuda.manual_seed_all(cfg["seed"])
    random.seed(cfg["seed"])
    device = "cuda" if torch.cuda.is_available() else "cpu"

    items = load_corpus(cfg["corpus"])
    ds = DirEDataset(items, cfg["block_size"], cfg["seed"])
    n_stage2_records = sum(1 for it in items if it["stage2_span"] is not None)

    model = ConsciousDecoderV2(
        vocab_size=256, d_model=cfg["d_model"], n_head=cfg["n_head"],
        n_layer=cfg["n_layer"], block_size=cfg["block_size"],
        n_kv_head=cfg["n_kv_head"], consciousness_dim=128, dropout=0.1,
    ).to(device)
    model.train()
    n_params = model.count_params()

    trainable = [p for p in model.parameters() if p.requires_grad]
    opt = torch.optim.AdamW(trainable, lr=cfg["lr"],
                            betas=(0.9, 0.95), weight_decay=0.1)
    warmup, total = cfg["warmup"], cfg["steps"]

    def cosine_lr_at(step):
        if step < warmup:
            return cfg["lr"] * (step + 1) / warmup
        prog = (step - warmup) / max(1, total - warmup)
        return cfg["lr"] * 0.5 * (1.0 + math.cos(math.pi * prog)) * 0.9 \
            + cfg["lr"] * 0.1

    use_amp = (device == "cuda")
    scaler = torch.cuda.amp.GradScaler(enabled=use_amp)
    traj, t0, init_loss = [], time.time(), None
    gpu_name = torch.cuda.get_device_name(0) if device == "cuda" else "cpu"

    for step in range(total):
        lr_now = cosine_lr_at(step)
        for g in opt.param_groups:
            g["lr"] = lr_now

        x, y, sm = ds.get_batch(cfg["bsz"], device)
        opt.zero_grad(set_to_none=True)
        with torch.autocast(device_type="cuda" if use_amp else "cpu",
                            dtype=torch.bfloat16, enabled=use_amp):
            logits_a, logits_g, tensions, _, _ = model(x)
            B, T, V = logits_a.shape
            # TWO-STAGE MASKED LOSS — CE only on stage-2 (match index + voice
            # prediction); stage-1 superposed inner traces = context (mask 0).
            ce_tok = F.cross_entropy(
                logits_a.view(-1, V), y.view(-1), reduction="none")
            mask = sm.view(-1)
            denom = mask.sum().clamp(min=1.0)
            ce_stage2 = (ce_tok * mask).sum() / denom
            # report full-corpus CE too for cross-direction comparability
            ce_full = F.cross_entropy(logits_a.view(-1, V), y.view(-1))
            loss = ce_stage2
            ce_report = float(ce_stage2.item())

        scaler.scale(loss).backward()
        scaler.unscale_(opt)
        gn = torch.nn.utils.clip_grad_norm_(trainable, 1.0)
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
            rec = {"step": step + 1, "ce_stage2": round(ce_report, 6),
                   "ce_full": round(float(ce_full.item()), 6),
                   "loss": round(float(loss.item()), 6),
                   "gn2": round(gn2, 6), "lr": round(lr_now, 8),
                   "wall_s": round(wall, 2), "gpu_mem_gb": round(mem, 3)}
            traj.append(rec)
            print(json.dumps(rec), flush=True)

    wall = time.time() - t0
    final = traj[-1]
    out_dir = cfg["out_dir"]
    os.makedirs(out_dir, exist_ok=True)
    ckpt_path = os.path.join(out_dir, "ckpt_carving_dirE.pt")
    torch.save({"model": model.state_dict(), "cfg": cfg,
                "n_params": n_params, "path": "dirE_two_stage"}, ckpt_path)

    result = {
        "substrate": ("PYTHON / PyTorch — interim LM-scale executor; "
                      "NOT a hexa-native fire"),
        "fire_kind": "Direction E EMERGENCE-OF-SUPERPOSITION 2-stage carving",
        "carving_path": "dirE_two_stage",
        "honest_framing": (
            "2-stage MASK is a closed-form deterministic byte-span predicate "
            "(B-DIRE-MASK structural). SGD OUTCOME + Dir-E vs UBM-E7 α JOINT "
            "compare = EMPIRICAL (B-D-NOTE family). PyTorch substrate, NOT "
            "hexa-native. Corpus = 2-stage carving (NOT chat SFT) — "
            "forbidden-token grep == 0."),
        "arch": "ConsciousDecoderV2 (RoPE+SwiGLU+RMSNorm+GQA+PureFieldFFN)",
        "from_scratch": True,
        "base_ckpt": None,
        "config": cfg,
        "n_params": n_params,
        "n_params_M": round(n_params / 1e6, 2),
        "two_stage_records": n_stage2_records,
        "two_stage_records_total": len(items),
        "gpu": gpu_name,
        "device": device,
        "init_ce": round(init_loss, 6),
        "final_ce": final["ce_stage2"],
        "final_ce_full": final["ce_full"],
        "final_loss": final["loss"],
        "final_gn2": final["gn2"],
        "ce_descent": round(init_loss - final["ce_stage2"], 6),
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
    print(json.dumps({"path": "dirE_two_stage", "init_ce": result["init_ce"],
                       "final_ce": result["final_ce"],
                       "ce_descent": result["ce_descent"],
                       "wall_s": result["wall_s"]}), flush=True)
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
    args = ap.parse_args()

    if args.mode == "main":
        cfg = dict(d_model=args.d_model, n_head=args.n_head,
                   n_kv_head=args.n_kv_head, n_layer=args.n_layer,
                   block_size=128, lr=args.lr, bsz=args.bsz,
                   steps=args.steps, warmup=max(20, args.steps // 20),
                   seed=args.seed, log_every=max(1, args.steps // 40),
                   corpus=args.corpus, out_dir=args.out_dir)
    else:
        cfg = dict(d_model=32, n_head=4, n_kv_head=2, n_layer=3,
                   block_size=64, lr=1e-3, bsz=16, steps=args.steps,
                   warmup=5, seed=args.seed,
                   log_every=max(1, args.steps // 20),
                   corpus=args.corpus, out_dir=args.out_dir)
    run(cfg)
