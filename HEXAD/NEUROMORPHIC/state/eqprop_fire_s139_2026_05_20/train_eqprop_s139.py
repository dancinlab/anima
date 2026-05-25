#!/usr/bin/env python3
"""§139 EQPROP-C2 — Equilibrium-Propagation-flavored 2-phase local update on
ConsciousDecoderV2.

WHY: §96-Q2 hypothesis ("`§11-B is GPU tautology`") needs *multiple* algorithm
data points. §125 NONCE-FF (Hinton goodness-contrast) LANDED S11B_LIKE_DEGEN.
§126 PCN-C4 (top-down prediction error) — in-flight. §139 adds a third
distinct non-CE non-backprop algorithm: Equilibrium Propagation
(Scellier-Bengio 2017).

REFERENCES:
  - Scellier & Bengio (2017) "Equilibrium Propagation: Bridging the Gap
    Between Energy-Based Models and Backpropagation" — canonical recurrent
    energy-based formulation with TWO PHASES (free + nudge).
  - Laborieux & Zenke (2022) "Holomorphic Equilibrium Propagation" /
    "Lifted EqProp" — extension to feedforward networks.

DESIGN CHOICE — EqProp-FLAVORED 2-PHASE LOCAL UPDATE:
Canonical EqProp needs a recurrent network reaching fixed-point — does
NOT directly fit feedforward transformer. We use the Laborieux-style
"lifted" idea applied minimally: two FORWARD passes with different output
boundary conditions, weight update from the activation DIFFERENCE.

PHASE-1 (free): standard forward through all blocks, no target signal at output
PHASE-2 (nudge): same forward but with output logits nudged by β·one_hot(target)
                 BEFORE the final softmax (= a small "pull" toward the right
                 answer at the output layer; the nudge then propagates BACK
                 through the layers as the difference of activations)

WEIGHT UPDATE (LOCAL, per block, no global backward):
    ΔW_i ∝ (act2_i.detach() - act1_i.detach()) · prev_act_i.detach()
the i-th block's params updated from the activation-difference between the
two phases. NO call to .backward() on any aggregate loss; the update is
computed as a tensor-product on .detach()'d activations and applied via
optimizer.step() on a synthetic local loss `((act2 - act1).detach() ·
block_output_with_grad).sum()` which acts as the canonical EqProp gradient.

KEY INVARIANTS:
  - B-S139-1 NO-CE: F.cross_entropy / nll_loss never called.
  - B-S139-2 NO-GLOBAL-BACKWARD: each block_i's .backward() is on its
    own LOCAL synthetic loss tensor; activations are .detach()'d
    between blocks AND between phases.
  - B-S139-3 TWO-PHASE-STRUCTURAL: pass-1 (free) + pass-2 (nudged) are
    structurally distinct in source.
  - B-S139-4 PER-BLOCK OPTIMIZERS: one AdamW per block + head.
  - B-S139-5 FROM-SCRATCH: g_clm_from_scratch.

HONEST CARVE-OUT (B-S139-NOTE):
This is "EqProp-flavored 2-phase local" — NOT canonical recurrent EqProp.
The canonical algorithm requires fixed-point recurrent inference which
doesn't fit feedforward transformer; the "lifted" feedforward variant we
use is structurally distinct from FF/PCN (its update uses ACTIVATION
DIFFERENCE between two output-conditioning regimes) but is a simplified
form. Verdict applies to this specific algorithm point.

GPU DISPATCH CONDITIONAL on §126 PCN verdict — if §126 lands SUPP, §139
priority HIGH (algorithmic decomposition matters); if §126 lands DEG, §139
priority MEDIUM (third confirming data point) — fire still informative
either way.
"""
import os, sys, json, math, random, argparse, time
import torch
import torch.nn as nn
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


class EqPropSampler:
    """(context, target) sampler. Like §126 PCN: positive only, no negatives."""
    def __init__(self, corpus_bytes, block_size, seed=1337):
        self.corpus = corpus_bytes
        self.T = block_size
        self.rng = random.Random(seed)

    def sample_batch(self, bsz, device):
        N = len(self.corpus)
        starts = [self.rng.randint(0, N - self.T - 2) for _ in range(bsz)]
        ctx = torch.tensor(
            [list(self.corpus[s : s + self.T]) for s in starts],
            dtype=torch.long, device=device,
        )
        tgt = torch.tensor(
            [list(self.corpus[s + 1 : s + self.T + 1]) for s in starts],
            dtype=torch.long, device=device,
        )
        return ctx, tgt


def run(cfg):
    torch.manual_seed(cfg["seed"])
    torch.cuda.manual_seed_all(cfg["seed"])
    random.seed(cfg["seed"])

    device = ("cuda" if torch.cuda.is_available() and not cfg.get("cpu_only")
              else "cpu")
    print(f"[§139-EqProp] device={device} d_model={cfg['d_model']} "
          f"n_layer={cfg['n_layer']} steps={cfg['steps']}", flush=True)

    model = ConsciousDecoderV2(
        vocab_size=256, d_model=cfg["d_model"], n_head=cfg["n_head"],
        n_layer=cfg["n_layer"], block_size=cfg["block_size"],
        n_kv_head=cfg["n_kv_head"], consciousness_dim=128, dropout=0.1,
    ).to(device)
    model.train()

    # per-block optimizers
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

    corpus_bytes = load_corpus_bytes(cfg["corpus"])
    print(f"[§139-EqProp] corpus bytes: {len(corpus_bytes):,}", flush=True)
    sampler = EqPropSampler(corpus_bytes, cfg["block_size"], seed=cfg["seed"])

    beta = cfg["beta"]  # nudge strength
    t0 = time.time()
    log = []
    steps = cfg["steps"]
    log_every = cfg["log_every"]

    for step in range(steps):
        ctx, tgt = sampler.sample_batch(cfg["bsz"], device)

        # ── PHASE-1 (free): standard forward, no target signal ──
        with torch.no_grad():
            x = model.drop(model.tok_emb(ctx))
            acts_free = [x.clone()]
            for block in model.blocks:
                xb, _t, _kv, _aux = block(
                    x, consciousness_signal=None, consciousness_states=None,
                    use_cache=False, past_kv=None, position_offset=0,
                )
                acts_free.append(xb.clone())
                x = xb
            free_top = acts_free[-1]
            free_top_n = model.ln_f(free_top)
            free_logits = model.head_a(free_top_n)

        # ── PHASE-2 (nudge): forward with output-end target nudge ──
        # We propagate the nudge BACK through the network by re-running the
        # forward in REVERSE conceptually — but since blocks are non-invertible,
        # we use the Laborieux-style "compute the same forward but with the
        # input at the top end mildly perturbed by β·gradient-of-target-MSE".
        # Practical Laborieux approximation: re-do forward, at each block
        # add β · (one_hot(target) lifted-back) — implemented as adding β·grad of
        # the output MSE w.r.t. each block's output, computed STRICTLY locally.
        with torch.no_grad():
            tgt_oh = F.one_hot(tgt, num_classes=256).float()
            # Nudge target on the output: difference between free softmax and one-hot.
            # We propagate this AS A SCALED ADDITION to each layer's residual stream
            # (Laborieux feedforward simplification).
            free_probs = F.softmax(free_logits, dim=-1)
            output_err = (tgt_oh - free_probs)  # (B, T, V)
            # Lift to residual space via head_a's transpose
            head_w = model.head_a.weight if hasattr(model.head_a, "weight") else None
            if head_w is not None:
                lift = output_err @ head_w     # (B, T, d_model)
            else:
                lift = torch.zeros_like(free_top)
            # Phase-2 activations: free + β·lift, propagated through blocks
            x = model.drop(model.tok_emb(ctx)) + beta * lift / (1.0 + cfg["n_layer"])
            acts_nudge = [x.clone()]
            for i, block in enumerate(model.blocks):
                xb, _t, _kv, _aux = block(
                    x, consciousness_signal=None, consciousness_states=None,
                    use_cache=False, past_kv=None, position_offset=0,
                )
                # add a fraction of the lift at each layer (lifted-eqprop)
                xb = xb + beta * lift * ((i + 1) / cfg["n_layer"])
                acts_nudge.append(xb.clone())
                x = xb

        # ── LOCAL WEIGHT UPDATE (no global backward) ──
        # For each block i, the EqProp local update rule is:
        #   ΔW_i ∝ -(act_nudge[i+1] - act_free[i+1]) / β  (Scellier-Bengio thm.1)
        # We implement this by computing a synthetic local loss
        # `L_i = ((act_nudge[i+1] - act_free[i+1]).detach() * block_out).mean()`
        # whose gradient w.r.t. block_i's params equals the EqProp rule.
        layer_losses = []
        for i, block in enumerate(model.blocks):
            x_in = acts_free[i].detach().requires_grad_(False)
            # the GROUND TRUTH activation-difference (Scellier-Bengio scaled by 1/β)
            diff = (acts_nudge[i + 1] - acts_free[i + 1]).detach() / max(beta, 1e-6)
            # forward block_i with grad enabled
            x_pred, _t, _kv, _aux = block(
                x_in, consciousness_signal=None, consciousness_states=None,
                use_cache=False, past_kv=None, position_offset=0,
            )
            # synthetic local loss whose grad ≡ EqProp local rule
            L_i = -(diff * x_pred).mean()      # negative sign per Scellier thm.1
            block_opts[i].zero_grad(set_to_none=True)
            L_i.backward()
            torch.nn.utils.clip_grad_norm_(
                [p for p in block_opts[i].param_groups[0]["params"]
                 if p.grad is not None], max_norm=1.0,
            )
            block_opts[i].step()
            layer_losses.append(float(L_i.detach()))

        # ── HEAD update (NON-CE MSE on free output vs one-hot target) ──
        z = acts_free[-1].detach().requires_grad_(False)
        z_n = model.ln_f(z)
        logits_a = model.head_a(z_n)
        probs_a = F.softmax(logits_a, dim=-1)
        L_head = F.mse_loss(probs_a, F.one_hot(tgt, num_classes=256).float())
        head_opt.zero_grad(set_to_none=True)
        L_head.backward()
        torch.nn.utils.clip_grad_norm_(
            [p for p in head_opt.param_groups[0]["params"]
             if p.grad is not None], max_norm=1.0,
        )
        head_opt.step()

        if step == 0 or (step + 1) % log_every == 0 or step == steps - 1:
            mean_L = sum(layer_losses) / max(1, len(layer_losses))
            elapsed = time.time() - t0
            entry = dict(
                step=step + 1, mean_layer_eqprop_loss=mean_L,
                first_layer_loss=layer_losses[0],
                last_layer_loss=layer_losses[-1],
                L_head_mse=float(L_head.detach()),
                elapsed_s=elapsed,
            )
            log.append(entry)
            print(f"[§139-EqProp] step={step+1:6d}  L̄_block={mean_L:+.6f}  "
                  f"L_head={entry['L_head_mse']:.6f}  "
                  f"t={elapsed:.1f}s", flush=True)

    out_dir = cfg["out_dir"]
    os.makedirs(out_dir, exist_ok=True)
    ckpt_path = os.path.join(out_dir, "ckpt_eqprop_s139.pt")
    torch.save({
        "model": model.state_dict(), "cfg": cfg, "log": log,
    }, ckpt_path)

    result = dict(
        battery="§139 EQPROP-C2 (lifted 2-phase local) training",
        cfg=cfg, device=device,
        n_params=sum(p.numel() for p in model.parameters()),
        train_wall_s=time.time() - t0,
        init_log=log[0] if log else None,
        final_log=log[-1] if log else None,
        n_block_optimizers=len(block_opts),
        head_optimizer=True,
        algorithm="EqProp-lifted-2-phase (Scellier-Bengio 2017 + Laborieux-Zenke 2022)",
        beta_nudge=beta,
        non_ce_supervision="MSE on softmax(logits_a) vs one-hot(target)",
    )
    with open(os.path.join(out_dir, "result.json"), "w") as f:
        json.dump(result, f, indent=2, default=str)
    print(f"[§139-EqProp] DONE wall={result['train_wall_s']:.1f}s "
          f"ckpt={ckpt_path}", flush=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", default="main", choices=["main", "sanity"])
    ap.add_argument("--corpus", required=True)
    ap.add_argument("--out-dir", required=True)
    ap.add_argument("--steps", type=int, default=3000)
    ap.add_argument("--lr", type=float, default=3e-4)
    ap.add_argument("--bsz", type=int, default=32)
    ap.add_argument("--seed", type=int, default=1337)
    ap.add_argument("--beta", type=float, default=0.1,
                    help="EqProp nudge strength (Scellier-Bengio β)")
    ap.add_argument("--d-model", type=int, default=768)
    ap.add_argument("--n-layer", type=int, default=12)
    ap.add_argument("--n-head", type=int, default=12)
    ap.add_argument("--n-kv-head", type=int, default=4)
    ap.add_argument("--cpu-only", action="store_true")
    args = ap.parse_args()
    if args.mode == "main":
        cfg = dict(d_model=args.d_model, n_head=args.n_head,
                   n_kv_head=args.n_kv_head, n_layer=args.n_layer,
                   block_size=128, lr=args.lr, bsz=args.bsz,
                   steps=args.steps, seed=args.seed, beta=args.beta,
                   log_every=max(1, args.steps // 40),
                   corpus=args.corpus, out_dir=args.out_dir,
                   cpu_only=args.cpu_only)
    else:
        cfg = dict(d_model=32, n_head=4, n_kv_head=2, n_layer=3,
                   block_size=64, lr=1e-3, bsz=8, steps=args.steps,
                   seed=args.seed, beta=args.beta,
                   log_every=max(1, args.steps // 10),
                   corpus=args.corpus, out_dir=args.out_dir, cpu_only=True)
    run(cfg)


if __name__ == "__main__":
    main()
