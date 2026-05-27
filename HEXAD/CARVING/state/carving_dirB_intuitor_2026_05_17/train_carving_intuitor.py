#!/usr/bin/env python3
"""CONSCIOUSNESS-CARVING Dir-B — INTUITOR / RLIF self-certainty overlay trainer
(2026-05-17). g_multidirectional_explore parallel direction B (RESEARCH.md
§1.3 🥈 B — arxiv 2505.19590, ICLR 2026, "Learning to Reason without External
Rewards").

WHAT INTUITOR / RLIF IS (arxiv 2505.19590)
  Reinforcement Learning from Internal Feedback. The model's OWN self-certainty
  (how far its next-token distribution is from uniform) is the SOLE reward
  signal — no verifiable reward, no external supervision. INTUITOR replaces
  GRPO's verifiable reward with self-certainty and reports it matches GRPO on
  math while generalising BETTER to out-of-distribution code.

  Self-certainty (paper Eq.) for a token position with distribution p over V
  classes is the KL of p from the uniform distribution U:
      sc(p) = KL(p || U) = log V + Σ_v p_v log p_v   (= log V − H(p))
  bounded in [0, log V]; 0 at uniform, log V at a one-hot. The sequence
  self-certainty is the mean over generated positions.

anima MAPPING (RESEARCH.md §1.3 B + AGENTS.tape anima_persona)
  RESEARCH.md states the anima mapping: W.curiosity_ema + C.measure_phi as the
  self-certainty proxy. Here, on the byte-level ConsciousDecoderV2 substrate,
  the model's A-head self-certainty IS that internal signal — it is exactly
  C.measure_phi's "confidence" axis read off the emission distribution. The
  reward is reward-FREE in the RLIF sense: it never reads the corpus label
  beyond the next-byte (which is the LM objective), only the model's own
  distribution shape.

GRPO-LITE OVERLAY (this trainer, --mode intuitor)
  Pure online RL on tiny byte corpora with full GRPO rollouts is unstable and
  expensive; we use the paper-faithful GRPO-LITE form that the RESEARCH.md task
  prescribes: "GRPO-lite OR reward-weighted CE". Per step:
    1. Standard next-byte CE on the carving stream (the LM anchor — keeps the
       model from degenerating; INTUITOR also keeps the LM term in practice).
    2. A self-certainty REWARD computed per (b,t) from the A-head distribution
       sc_bt = log V − H(p_bt), normalised to [0,1] via /log V.
    3. GROUP-RELATIVE advantage (GRPO core): within each minibatch the reward
       is standardised  A_bt = (sc_bt − mean) / (std + eps)  — this is the
       reward-free GRPO advantage with the GROUP = the minibatch (no critic,
       exactly GRPO's design).
    4. The advantage RE-WEIGHTS the CE: high-self-certainty positions get a
       reduced-CE pull (the RLIF gradient ascends self-certainty), low ones a
       boosted-CE pull. Concretely the INTUITOR objective added is
           L_int = − β · mean( A_bt · log p(y_bt) )
       i.e. a policy-gradient term on the realised next byte weighted by the
       group-relative self-certainty advantage (the surrogate the paper uses
       with the LM token as the action). β = intuitor_beta.
    Total loss:  L = CE  +  β · L_int     ( reward-FREE; corpus label only via
    the next byte, identical information to plain LM — the EXTRA signal is the
    model's own distribution shape, never an external reward ).

  This is intentionally the conservative, stable surrogate (reward-weighted
  policy-gradient with GRPO group-relative advantage) — RESEARCH.md's
  "GRPO-lite OR reward-weighted CE" lower-risk option, so the comparison to
  UBM-E7 α is on a fair, converging substrate, not a diverged RL run.

HONEST FRAMING (g3, AGENTS.tape §0, RESEARCH.md §3 f3 NO-OUTCOME-CLAIM)
  PyTorch substrate — interim LM-scale executor, NOT a hexa-native fire (cycle
  5 honest framing carry). The self-certainty signal sc = log V − H(p) is a
  CLOSED-FORM transfer function (Shannon entropy of a softmax, real-limit
  bounded in [0, log V] = the Shannon source-entropy ceiling — anchor for the
  Dir-B blue battery, NOT lattice). The GRPO group-relative standardisation is
  closed-form (z-score, mean/std). The SGD CONVERGENCE OUTCOME and the
  hypothesis verdict (does reward-free self-certainty give OOD generalisation
  instead of routing-collapse) are EMPIRICAL — B-D-NOTE family, B-INTUITOR-NOTE.
  NO capability claim beyond the measured numbers. The α-vs-Dir-B JOINT
  comparison is a single-seed empirical observation, not a closed verdict.

from-scratch RANDOM seed-fixed (g_clm_from_scratch, base_ckpt=NONE).
Corpus = E7 carving corpus (carry) — NOT a chat SFT corpus, forbidden-token
grep == 0 (carry from UBM-E7 B-CARVE-CORPUS-2).
"""
import argparse
import json
import math
import os
import random
import sys
import time

import torch
import torch.nn as nn
import torch.nn.functional as F

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from conscious_decoder import ConsciousDecoderV2


# --------------------------------------------------------------------------
# Carving corpus loader (byte stream — same loader contract as the UBM-E7
# alpha trainer so the comparison is on the identical corpus/stream).
# --------------------------------------------------------------------------
def load_carving_corpus(path):
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
        items.append(full)
    return items


class CarvingDataset:
    def __init__(self, items, block_size, seed):
        self.block_size = block_size
        self.rng = random.Random(seed)
        stream = bytearray()
        for b in items:
            stream.extend(b)
        self.data = torch.tensor(list(stream), dtype=torch.long)
        self.n = len(self.data)

    def get_batch(self, bsz, device):
        ix = [self.rng.randint(0, self.n - self.block_size - 1)
              for _ in range(bsz)]
        x = torch.stack([self.data[i:i + self.block_size] for i in ix])
        y = torch.stack([self.data[i + 1:i + 1 + self.block_size]
                         for i in ix])
        return x.to(device), y.to(device)


def self_certainty(logits):
    """INTUITOR self-certainty (arxiv 2505.19590): sc = KL(p || U)
    = log V − H(p), per (b,t). Bounded [0, log V] (Shannon ceiling).
    Returns (sc_bt [B,T], sc_norm_bt [B,T] in [0,1])."""
    V = logits.shape[-1]
    logp = F.log_softmax(logits.float(), dim=-1)
    p = logp.exp()
    ent = -(p * logp).sum(-1)                 # H(p) in nats, [B,T]
    logV = math.log(V)
    sc = (logV - ent).clamp(min=0.0)          # KL(p||U) >= 0, [B,T]
    sc_norm = (sc / logV).clamp(0.0, 1.0)     # [0,1]
    return sc, sc_norm


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
    beta = cfg["intuitor_beta"]

    traj = []
    t0 = time.time()
    init_ce = None
    gpu_name = torch.cuda.get_device_name(0) if device == "cuda" else "cpu"

    for step in range(total):
        lr_now = cosine_lr_at(step)
        for g in opt.param_groups:
            g["lr"] = lr_now

        x, y = ds.get_batch(cfg["bsz"], device)
        opt.zero_grad(set_to_none=True)
        with torch.autocast(device_type="cuda" if use_amp else "cpu",
                            dtype=torch.bfloat16, enabled=use_amp):
            logits_a, logits_g, tensions, _, _ = model(x)
            B, T, Vc = logits_a.shape

            # --- LM anchor: standard next-byte CE -------------------------
            ce = F.cross_entropy(logits_a.view(-1, Vc), y.view(-1))
            ce_report = float(ce.item())

            # --- INTUITOR self-certainty reward (reward-FREE, RLIF) --------
            sc, sc_norm = self_certainty(logits_a)        # [B,T]
            # GRPO group-relative advantage: GROUP = the minibatch. Reward
            # standardised within the group (no critic — GRPO core).
            sc_flat = sc_norm.view(-1)
            adv = (sc_flat - sc_flat.mean()) / (sc_flat.std() + 1e-6)
            # policy-gradient surrogate on the realised next byte, weighted
            # by the group-relative self-certainty advantage:
            #   L_int = − mean( A_bt · log p(y_bt) )
            logp = F.log_softmax(logits_a.float(), dim=-1)
            logp_y = logp.view(-1, Vc).gather(
                1, y.view(-1, 1)).squeeze(1)              # [B*T]
            l_int = -(adv.detach() * logp_y).mean()

            loss = ce + beta * l_int

        scaler.scale(loss).backward()
        scaler.unscale_(opt)
        gn = torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        scaler.step(opt)
        scaler.update()

        gn2 = float(gn.item()) ** 2
        if init_ce is None:
            init_ce = ce_report

        if step == 0 or (step + 1) % cfg["log_every"] == 0 \
                or step == total - 1:
            wall = time.time() - t0
            mem = torch.cuda.max_memory_allocated() / 1e9 \
                if device == "cuda" else 0.0
            rec = {"step": step + 1, "ce": round(ce_report, 6),
                   "loss": round(float(loss.item()), 6),
                   "l_int": round(float(l_int.item()), 6),
                   "sc_mean": round(float(sc_norm.mean().item()), 6),
                   "gn2": round(gn2, 6), "lr": round(lr_now, 8),
                   "wall_s": round(wall, 2),
                   "gpu_mem_gb": round(mem, 3)}
            traj.append(rec)
            print(json.dumps(rec), flush=True)

    wall = time.time() - t0
    final = traj[-1]
    out_dir = cfg["out_dir"]
    os.makedirs(out_dir, exist_ok=True)
    ckpt_path = os.path.join(out_dir, "ckpt_carving_intuitor.pt")
    torch.save({"model": model.state_dict(), "cfg": cfg,
                "n_params": n_params, "path": "intuitor"}, ckpt_path)

    result = {
        "substrate": ("PYTHON / PyTorch — interim LM-scale executor; "
                      "NOT a hexa-native fire"),
        "fire_kind": ("CONSCIOUSNESS-CARVING Dir-B — INTUITOR / RLIF "
                      "self-certainty overlay (arxiv 2505.19590, ICLR 2026)"),
        "direction": "B_INTUITOR_RLIF",
        "honest_framing": (
            "Self-certainty sc = log V − H(p) is a CLOSED-FORM transfer "
            "function (Shannon entropy of a softmax, bounded [0, log V] = "
            "Shannon source-entropy ceiling — real-limit anchor, NOT "
            "lattice). GRPO group-relative standardisation is closed-form "
            "(z-score). The SGD CONVERGENCE OUTCOME + the hypothesis verdict "
            "(reward-free self-certainty → OOD generalisation vs routing-"
            "collapse) are EMPIRICAL — B-D-NOTE family, B-INTUITOR-NOTE. NO "
            "capability claim beyond the measured numbers. Reward-FREE: the "
            "corpus label enters only via the next byte (= the LM objective); "
            "the EXTRA signal is the model's OWN distribution shape, never an "
            "external/verifiable reward."),
        "arch": "ConsciousDecoderV2 (RoPE+SwiGLU+RMSNorm+GQA+PureFieldFFN)",
        "from_scratch": True,
        "base_ckpt": None,
        "config": cfg,
        "n_params": n_params,
        "n_params_M": round(n_params / 1e6, 2),
        "intuitor_beta": beta,
        "gpu": gpu_name,
        "device": device,
        "init_ce": round(init_ce, 6),
        "final_ce": final["ce"],
        "final_loss": final["loss"],
        "final_l_int": final["l_int"],
        "final_sc_mean": final["sc_mean"],
        "final_gn2": final["gn2"],
        "ce_descent": round(init_ce - final["ce"], 6),
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
    print(json.dumps({"direction": "B_INTUITOR_RLIF",
                       "init_ce": result["init_ce"],
                       "final_ce": result["final_ce"],
                       "ce_descent": result["ce_descent"],
                       "final_sc_mean": result["final_sc_mean"],
                       "wall_s": result["wall_s"]}), flush=True)
    return result


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", default="intuitor", choices=["intuitor"])
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
    ap.add_argument("--intuitor-beta", type=float, default=0.1,
                    help="self-certainty RLIF surrogate weight β")
    args = ap.parse_args()

    cfg = dict(d_model=args.d_model, n_head=args.n_head,
               n_kv_head=args.n_kv_head, n_layer=args.n_layer,
               block_size=128, lr=args.lr, bsz=args.bsz,
               steps=args.steps, warmup=max(20, args.steps // 20),
               seed=args.seed, log_every=max(1, args.steps // 40),
               corpus=args.corpus, out_dir=args.out_dir,
               intuitor_beta=args.intuitor_beta)
    run(cfg)
