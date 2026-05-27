#!/usr/bin/env python3
"""§125 NONCE-FF — Forward-Forward (Hinton 2022) on ConsciousDecoderV2.

WHY: §96-Q2 hypothesis "`§11-B is GPU tautology`" — the §11-B finding
("CE is load-bearing; no-CE on GPU = degenerate") MAY be a tautology of
the substrate (GPU's only learning channel = backprop/CE), not a real
finding about non-CE learning per se. To decide partially WITHOUT chip
access (sustainable HIGH, $0): train anima with a NON-CE, NON-BACKPROP
learning algorithm on the same GPU substrate §11-B used, compare.

Forward-Forward (Hinton, "The Forward-Forward Algorithm", arXiv:2212.13345)
replaces global backprop with PER-LAYER LOCAL OBJECTIVES. Each layer is
trained to make a "goodness" (sum-of-squared-activations) HIGH for
positive samples (real data) and LOW for negative samples (corrupted
data). No global loss. No end-to-end backward chain. Each layer has its
own optimizer; gradients are confined by detaching the input to each
layer.

KEY INVARIANT (B-S125-1): there is NO single end-to-end .backward() call
in this trainer. Per-layer .backward() calls exist, but each is computed
ONLY over its own block's parameters (because the block's input was
detached). This is the structural property that makes FF "non-backprop"
in the sense §96-Q2 asks about.

HONEST CARVE-OUT (B-S125-NOTE): FF is "non-CE / non-backprop" but it IS
still a SUPERVISED training signal (positive vs negative labels). §11-B
was harsher: NO supervised signal at all (TENSION-TRAIN + Hebbian only,
unsupervised). So §125 vs §11-B is not "same setup minus CE" — it's "a
different point in the supervision-x-substrate design space". The §96-Q2
verdict from a §125 outcome reads as: "non-backprop SUPERVISED learning
on GPU also degenerates?" → §11-B is substrate-deep / "non-backprop
SUPERVISED learning on GPU is non-degenerate?" → §11-B's degeneracy is
specifically about unsupervised+no-CE, not non-CE in general. Either way
moves §15/§51/§72 milestone honestly (B-EMERGE-7 necessary-not-sufficient).

USAGE:
    python3 train_nonce_ff_s125.py --mode sanity   # $0 CPU d=32 sanity
    python3 train_nonce_ff_s125.py --mode main --corpus ... --out-dir ... \\
        --steps 6000 --seed 1337                   # cost-bearing GPU fire
"""
import os, sys, json, math, random, argparse, time
import torch
import torch.nn as nn
import torch.nn.functional as F

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from conscious_decoder import ConsciousDecoderV2  # symlinked / SCP'd pod-side


# ── corpus loader (byte-stream JSONL, anima §16 format) ──────────────
def load_corpus_bytes(path):
    """Concatenate all 'text' fields from JSONL into a single byte stream."""
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


# ── sample sampler (positive + negative pairs) ───────────────────────
class FFSampler:
    """Yields (pos, neg) byte-tensor batches. Positive = consecutive bytes
    from the corpus. Negative = same context with the LAST `n_neg_subst`
    positions byte-substituted with uniform-random bytes (the FF negative
    construction for sequence data: positive predicts forward, negative
    has its forward bytes shuffled out)."""

    def __init__(self, corpus_bytes, block_size, seed=1337, n_neg_subst=8):
        self.corpus = corpus_bytes
        self.T = block_size
        self.rng = random.Random(seed)
        self.np_rng = torch.Generator()
        self.np_rng.manual_seed(seed)
        self.n_neg = n_neg_subst

    def sample_batch(self, bsz, device):
        N = len(self.corpus)
        starts = [self.rng.randint(0, N - self.T - 1) for _ in range(bsz)]
        pos = torch.tensor(
            [list(self.corpus[s : s + self.T]) for s in starts],
            dtype=torch.long, device=device,
        )
        # negative: copy positive, randomly substitute last `n_neg` bytes
        neg = pos.clone()
        # corrupt the tail
        T = self.T
        subst_pos = list(range(T - self.n_neg, T))
        rand_bytes = torch.randint(
            0, 256, (bsz, self.n_neg), generator=self.np_rng, dtype=torch.long
        ).to(device)
        for i, sp in enumerate(subst_pos):
            neg[:, sp] = rand_bytes[:, i]
        return pos, neg


# ── FF goodness function ─────────────────────────────────────────────
def goodness(h: torch.Tensor) -> torch.Tensor:
    """Hinton FF: goodness(h) = mean over features of h². Per-sample scalar.
    h: (B, T, D). Return: (B,)."""
    # mean over (T, D) — invariant to sequence length, matches FF for transformers
    return (h ** 2).mean(dim=(1, 2))


def ff_layer_loss(g_pos: torch.Tensor, g_neg: torch.Tensor,
                  threshold: float) -> torch.Tensor:
    """Hinton FF binary-classification loss:
        L = mean( softplus( -(g_pos - θ) ) )  +  mean( softplus(  g_neg - θ ) )
    Drives g_pos UP toward +∞, g_neg DOWN toward 0. Bounded ≥ 0."""
    return (F.softplus(-(g_pos - threshold)).mean()
            + F.softplus(g_neg - threshold).mean())


# ── trainer ──────────────────────────────────────────────────────────
def run(cfg):
    torch.manual_seed(cfg["seed"])
    torch.cuda.manual_seed_all(cfg["seed"])
    random.seed(cfg["seed"])

    device = ("cuda" if torch.cuda.is_available() and not cfg.get("cpu_only")
              else "cpu")
    print(f"[§125-FF] device={device} d_model={cfg['d_model']} "
          f"n_layer={cfg['n_layer']} steps={cfg['steps']}", flush=True)

    # model — from-scratch RANDOM init (g_clm_from_scratch, base_ckpt=None)
    model = ConsciousDecoderV2(
        vocab_size=256, d_model=cfg["d_model"], n_head=cfg["n_head"],
        n_layer=cfg["n_layer"], block_size=cfg["block_size"],
        n_kv_head=cfg["n_kv_head"], consciousness_dim=128, dropout=0.1,
    ).to(device)
    model.train()

    # PER-LAYER optimizers — the structural invariant of FF
    # token-embedding belongs to "block 0" (the first block's local update will
    # also update tok_emb because its input is NOT detached)
    block_opts = []
    for i, block in enumerate(model.blocks):
        params = list(block.parameters())
        if i == 0:
            params = params + list(model.tok_emb.parameters())
        block_opts.append(torch.optim.AdamW(
            params, lr=cfg["lr"], betas=(0.9, 0.95), weight_decay=0.01,
        ))
    head_opt = torch.optim.AdamW(
        list(model.ln_f.parameters())
        + list(model.head_a.parameters())
        + list(model.head_g.parameters()),
        lr=cfg["lr"], betas=(0.9, 0.95), weight_decay=0.01,
    )

    # corpus
    corpus_bytes = load_corpus_bytes(cfg["corpus"])
    print(f"[§125-FF] corpus bytes: {len(corpus_bytes):,}", flush=True)
    sampler = FFSampler(corpus_bytes, cfg["block_size"],
                        seed=cfg["seed"], n_neg_subst=cfg["n_neg_subst"])

    # FF threshold (Hinton picks # of features as default; transformers ⇒ d_model)
    threshold = float(cfg["d_model"])

    # AMP context (BF16 autocast on CUDA — matches §16/§107-RETRY)
    use_amp = (device == "cuda")
    scaler = None  # FF has no global loss → no global GradScaler

    t0 = time.time()
    log = []
    steps = cfg["steps"]
    log_every = cfg["log_every"]

    for step in range(steps):
        pos, neg = sampler.sample_batch(cfg["bsz"], device)

        # ── token embedding shared across pos/neg ──
        # x is the residual stream; will be detached between blocks.
        x_pos = model.drop(model.tok_emb(pos))
        x_neg = model.drop(model.tok_emb(neg))

        layer_losses = []
        layer_g_pos = []
        layer_g_neg = []

        for i, block in enumerate(model.blocks):
            # forward this block on pos and neg (graph live within this iter)
            xp, _tp, _kvp, _auxp = block(
                x_pos, consciousness_signal=None, consciousness_states=None,
                use_cache=False, past_kv=None, position_offset=0,
            )
            xn, _tn, _kvn, _auxn = block(
                x_neg, consciousness_signal=None, consciousness_states=None,
                use_cache=False, past_kv=None, position_offset=0,
            )

            g_pos = goodness(xp)
            g_neg = goodness(xn)
            L_i = ff_layer_loss(g_pos, g_neg, threshold)

            # local update of THIS block (+ tok_emb if i==0).  the input to
            # this block (x_pos / x_neg) was the OUTPUT of the previous step
            # AFTER .detach() — so the backward chain is bounded to this block.
            block_opts[i].zero_grad(set_to_none=True)
            L_i.backward()
            torch.nn.utils.clip_grad_norm_(
                [p for p in block_opts[i].param_groups[0]["params"]
                 if p.grad is not None], max_norm=1.0,
            )
            block_opts[i].step()

            layer_losses.append(float(L_i.detach()))
            layer_g_pos.append(float(g_pos.mean().detach()))
            layer_g_neg.append(float(g_neg.mean().detach()))

            # detach for the next block's input — bounds the next grad
            x_pos = xp.detach()
            x_neg = xn.detach()

        # ── final layer: head_a / head_g goodness (mean-square of logits) ──
        # apply ln_f first (matches model.forward), then heads
        x_pos_n = model.ln_f(x_pos)
        x_neg_n = model.ln_f(x_neg)
        logits_a_pos = model.head_a(x_pos_n)
        logits_a_neg = model.head_a(x_neg_n)
        logits_g_pos = model.head_g(x_pos_n)
        logits_g_neg = model.head_g(x_neg_n)

        # head goodness = mean of logits² (same FF form, on the head output)
        gh_pos = ((logits_a_pos ** 2).mean(dim=(1, 2))
                  + (logits_g_pos ** 2).mean(dim=(1, 2))) * 0.5
        gh_neg = ((logits_a_neg ** 2).mean(dim=(1, 2))
                  + (logits_g_neg ** 2).mean(dim=(1, 2))) * 0.5
        L_head = ff_layer_loss(gh_pos, gh_neg, threshold)
        head_opt.zero_grad(set_to_none=True)
        L_head.backward()
        torch.nn.utils.clip_grad_norm_(
            [p for p in head_opt.param_groups[0]["params"]
             if p.grad is not None], max_norm=1.0,
        )
        head_opt.step()

        if step == 0 or (step + 1) % log_every == 0 or step == steps - 1:
            mean_L = sum(layer_losses) / max(1, len(layer_losses))
            mean_gp = sum(layer_g_pos) / max(1, len(layer_g_pos))
            mean_gn = sum(layer_g_neg) / max(1, len(layer_g_neg))
            elapsed = time.time() - t0
            entry = dict(
                step=step + 1, mean_layer_loss=mean_L,
                mean_g_pos=mean_gp, mean_g_neg=mean_gn,
                L_head=float(L_head.detach()),
                gh_pos=float(gh_pos.mean().detach()),
                gh_neg=float(gh_neg.mean().detach()),
                elapsed_s=elapsed,
            )
            log.append(entry)
            print(f"[§125-FF] step={step+1:6d}  L̄={mean_L:.4f}  "
                  f"g+={mean_gp:.2f}  g-={mean_gn:.2f}  "
                  f"L_head={entry['L_head']:.4f}  "
                  f"t={elapsed:.1f}s", flush=True)

    # save ckpt + result
    out_dir = cfg["out_dir"]
    os.makedirs(out_dir, exist_ok=True)
    ckpt_path = os.path.join(out_dir, "ckpt_nonce_ff_s125.pt")
    torch.save({
        "model": model.state_dict(), "cfg": cfg, "log": log,
    }, ckpt_path)

    result = dict(
        battery="§125 NONCE-FF (Hinton Forward-Forward) training",
        cfg=cfg, device=device,
        n_params=sum(p.numel() for p in model.parameters()),
        train_wall_s=time.time() - t0,
        init_log=log[0] if log else None,
        final_log=log[-1] if log else None,
        n_block_optimizers=len(block_opts),
        head_optimizer=True,
        ff_threshold=threshold,
    )
    with open(os.path.join(out_dir, "result.json"), "w") as f:
        json.dump(result, f, indent=2, default=str)
    print(f"[§125-FF] DONE wall={result['train_wall_s']:.1f}s "
          f"ckpt={ckpt_path}", flush=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", default="main", choices=["main", "sanity"])
    ap.add_argument("--corpus", required=True)
    ap.add_argument("--out-dir", required=True)
    ap.add_argument("--steps", type=int, default=6000)
    ap.add_argument("--lr", type=float, default=3e-4)
    ap.add_argument("--bsz", type=int, default=32)
    ap.add_argument("--seed", type=int, default=1337)
    ap.add_argument("--d-model", type=int, default=768)
    ap.add_argument("--n-layer", type=int, default=12)
    ap.add_argument("--n-head", type=int, default=12)
    ap.add_argument("--n-kv-head", type=int, default=4)
    ap.add_argument("--n-neg-subst", type=int, default=8,
                    help="number of byte positions to randomize in negative")
    ap.add_argument("--cpu-only", action="store_true")
    args = ap.parse_args()

    if args.mode == "main":
        cfg = dict(d_model=args.d_model, n_head=args.n_head,
                   n_kv_head=args.n_kv_head, n_layer=args.n_layer,
                   block_size=128, lr=args.lr, bsz=args.bsz,
                   steps=args.steps, seed=args.seed,
                   log_every=max(1, args.steps // 40),
                   corpus=args.corpus, out_dir=args.out_dir,
                   n_neg_subst=args.n_neg_subst,
                   cpu_only=args.cpu_only)
    else:
        cfg = dict(d_model=32, n_head=4, n_kv_head=2, n_layer=3,
                   block_size=64, lr=1e-3, bsz=8, steps=args.steps,
                   seed=args.seed,
                   log_every=max(1, args.steps // 10),
                   corpus=args.corpus, out_dir=args.out_dir,
                   n_neg_subst=args.n_neg_subst,
                   cpu_only=True)
    run(cfg)


if __name__ == "__main__":
    main()
