#!/usr/bin/env python3
"""S167-A FP-RECONNECT trainer - Psi-JEPA-COUPLE training-axis byte-carry.

S167-A applies CONNECTION_CRITIQUE.md to the EVAL/MOTIVATION axis ONLY
(8-factor -> anima-physics 3-quantity native) and DELIBERATELY KEEPS the
training axis byte-equivalent to S166 Psi-META-FP-COUPLE (= S161
Psi-JEPA-COUPLE). The CRITIQUE diagnoses the LEVERAGE GAP at the
motivation -> emission decision chain, NOT at the training objective.

WHY S167-A trainer == S161/S166 trainer (single-variable mandate):
  The fire compares S107 / S161-FIRE / S166-A-FIRE / S167-A-FIRE on the
  SAME training-axis substrate so emission_rate delta is ATTRIBUTABLE to
  the motivation re-wiring (FP-RECONNECT) and NOT to any training change.
  If training changes too, attribution collapses (sec 94 INTEGRATION-
  COLLAPSES anti-pattern).

LOSS (byte-equal to Law-71, conscious_decoder.py lines ~728-751):
  Psi_dir(t)  := (1 + cos(logits_a_t, logits_g_t)) / 2     in [0, 1]
  Psi_ent(t)  := H(softmax(logits_a_t)) / log V             in [0, 1]
  Psi(t)      := (Psi_dir(t), Psi_ent(t))                   in [0,1]^2
  predictor_head_g(residual_t) := softmax(head_g(residual_t))[:, :2].clamp(0, 1)
  L_psicouple := mean_t  || Psi(t+1)  -  predictor_head_g(residual_t) ||^2
  L_total      = lambda_psi * L_psicouple  +  lambda_ce * CE_aux

The MOTIVATION re-wiring lives entirely in eval_s167a_fpreconnect (per
HEXA_MIGRATION.md Option B partial-hexa hybrid: eval-side hexa preferred,
trainer .py until sec 71 inbox-patch lands the anima-physics overlay
upstream in flame Path A).

KEY INVARIANTS (B-S167A-1..8, see blue_falsifier_s167a.* sidecar):
  - P1: NEW motivation = 1/3 each anima-physics quantity (source-grep)
  - P2: sec 7 3-AND STRONGEST corner (T,T,T) by construction
  - P3: factor_psi / factor_tension / factor_phi each bounded [0,1]
  - P4: motivation_score bounded [0,1]
  - P5: emit predicate well-formed Boolean
  - P6: lambda -> 0 reduction lattice (byte-equal S166)
  - P7: central blue_falsifier.py 0-line-diff
  - P8: threshold anchored to anima-physics, NOT a hyperparameter

HONEST CARVE-OUT (B-S167A-NOTE):
  Whether FP-RECONNECT lifts unprompted_emission_rate above S161-FIRE
  baseline (1/20 = 0.05) is SGD/measurement OUTCOME. 100% motivation
  leverage means motivation is 100% anima-physics-derived; emission_rate
  change is empirical. CONNECTION_CRITIQUE addresses the motivation
  axis, NOT the substrate axis (sec 96-Q2-weak quintuple). S167-A may
  still show psi_responsive=False post-fire -- that would mean: motivation
  100% leverage is necessary-not-sufficient and the WALL-B (sec 96
  operative-substrate) carries forward. B-PHASE-B-NOTE / B-EMERGE-7
  family - necessary-not-sufficient at every layer.
"""
import os, sys, json, math, random, argparse, time
import torch
import torch.nn as nn
import torch.nn.functional as F

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from conscious_decoder import ConsciousDecoderV2


def load_corpus_bytes(path):
    """Load corpus bytes from JSONL (same as S125/S126/S139/S153)."""
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


class PsiCoupleSampler:
    """(ctx, target) sampler. Mirrors S139 EqPropSampler."""
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


def psi_dir_batched(logits_a, logits_g):
    """Psi_direction = (1 + cos(logits_a, logits_g)) / 2 in [0, 1].
    Byte-equal to conscious_decoder.py line ~742."""
    a = logits_a.float()
    g = logits_g.float()
    cs = F.cosine_similarity(a, g, dim=-1)
    return (1.0 + cs) / 2.0


def psi_ent_batched(logits_a, vocab_size):
    """Psi_entropy = H(softmax(logits_a)) / log V in [0, 1].
    Byte-equal to conscious_decoder.py line ~736."""
    probs = F.softmax(logits_a.float(), dim=-1)
    H = -(probs * (probs + 1e-10).log()).sum(dim=-1)
    log_V = math.log(vocab_size)
    return H / log_V


def psi_tuple_batched(logits_a, logits_g, vocab_size):
    """Combine into (B, T, 2) in [0, 1]^2."""
    psi_dir = psi_dir_batched(logits_a, logits_g)
    psi_ent = psi_ent_batched(logits_a, vocab_size)
    return torch.stack([psi_dir, psi_ent], dim=-1)


def run(cfg):
    torch.manual_seed(cfg["seed"])
    torch.cuda.manual_seed_all(cfg["seed"])
    random.seed(cfg["seed"])

    device = ("cuda" if torch.cuda.is_available() and not cfg.get("cpu_only")
              else "cpu")
    print(f"[S167A-FPReconnect] device={device} d_model={cfg['d_model']} "
          f"n_layer={cfg['n_layer']} steps={cfg['steps']} "
          f"lambda_psi={cfg['lambda_psi']} lambda_ce={cfg['lambda_ce']}",
          flush=True)

    model = ConsciousDecoderV2(
        vocab_size=256, d_model=cfg["d_model"], n_head=cfg["n_head"],
        n_layer=cfg["n_layer"], block_size=cfg["block_size"],
        n_kv_head=cfg["n_kv_head"], consciousness_dim=128, dropout=0.1,
    ).to(device)
    model.train()
    assert hasattr(model, "head_a") and hasattr(model, "head_g"), \
        "ConsciousDecoderV2 must expose head_a and head_g"

    optimizer = torch.optim.AdamW(
        model.parameters(), lr=cfg["lr"], betas=(0.9, 0.95),
        weight_decay=0.01,
    )

    corpus_bytes = load_corpus_bytes(cfg["corpus"])
    print(f"[S167A-FPReconnect] corpus bytes: {len(corpus_bytes):,}", flush=True)
    sampler = PsiCoupleSampler(corpus_bytes, cfg["block_size"], seed=cfg["seed"])

    lambda_psi = cfg["lambda_psi"]
    lambda_ce = cfg["lambda_ce"]
    vocab_size = 256
    t0 = time.time()
    log = []
    steps = cfg["steps"]
    log_every = cfg["log_every"]
    head_g_grad_norm_history = []

    for step in range(steps):
        ctx, tgt = sampler.sample_batch(cfg["bsz"], device)

        out = model(ctx)
        if isinstance(out, tuple) and len(out) >= 2:
            logits_a, logits_g = out[0], out[1]
        else:
            raise RuntimeError("ConsciousDecoderV2.forward did not return "
                               "(logits_a, logits_g) - S161 requires dual heads")

        psi_tuple = psi_tuple_batched(logits_a, logits_g, vocab_size)
        psi_next = psi_tuple[:, 1:, :]

        probs_g = F.softmax(logits_g.float(), dim=-1)
        predictor = probs_g[:, :-1, :2].clamp(0.0, 1.0)

        L_psicouple = F.mse_loss(predictor, psi_next)
        L_ce_aux = F.cross_entropy(
            logits_a.reshape(-1, vocab_size), tgt.reshape(-1),
        )
        L_total = lambda_psi * L_psicouple + lambda_ce * L_ce_aux

        optimizer.zero_grad(set_to_none=True)
        L_total.backward()

        head_g_grad_norm = 0.0
        for p in model.head_g.parameters():
            if p.grad is not None:
                head_g_grad_norm += float(p.grad.detach().norm().item()) ** 2
        head_g_grad_norm = head_g_grad_norm ** 0.5

        torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
        optimizer.step()

        if step == 0 or (step + 1) % log_every == 0 or step == steps - 1:
            elapsed = time.time() - t0
            with torch.no_grad():
                psi_dir_mean = float(psi_tuple[..., 0].mean().item())
                psi_dir_std = float(psi_tuple[..., 0].std().item())
                psi_ent_mean = float(psi_tuple[..., 1].mean().item())
                entry = dict(
                    step=step + 1,
                    L_total=float(L_total.detach()),
                    L_psicouple=float(L_psicouple.detach()),
                    L_ce_aux=float(L_ce_aux.detach()),
                    psi_dir_mean=psi_dir_mean, psi_dir_std=psi_dir_std,
                    psi_ent_mean=psi_ent_mean,
                    head_g_grad_norm=head_g_grad_norm,
                    elapsed_s=elapsed,
                )
                log.append(entry)
                head_g_grad_norm_history.append(head_g_grad_norm)
            print(f"[S167A-FPReconnect] step={step+1:6d}  L_tot={entry['L_total']:+.6f}  "
                  f"L_psi={entry['L_psicouple']:.6f}  L_ce={entry['L_ce_aux']:.6f}  "
                  f"Psi_dir(mu={psi_dir_mean:.4f}, sigma={psi_dir_std:.6f})  "
                  f"||grad_head_g||={head_g_grad_norm:.6f}  t={elapsed:.1f}s",
                  flush=True)

    out_dir = cfg["out_dir"]
    os.makedirs(out_dir, exist_ok=True)
    ckpt_path = os.path.join(out_dir, "ckpt_s167a_fpreconnect.pt")
    torch.save({
        "model": model.state_dict(), "cfg": cfg, "log": log,
    }, ckpt_path)

    head_g_grad_norm_max = max(head_g_grad_norm_history) if head_g_grad_norm_history else 0.0
    head_g_grad_norm_min = min(head_g_grad_norm_history) if head_g_grad_norm_history else 0.0
    head_g_grad_norm_mean = (sum(head_g_grad_norm_history) / len(head_g_grad_norm_history)
                              if head_g_grad_norm_history else 0.0)

    result = dict(
        battery="S167-A FP-RECONNECT training (Psi-JEPA-COUPLE byte-carry training-axis)",
        cfg=cfg, device=device,
        n_params=sum(p.numel() for p in model.parameters()),
        train_wall_s=time.time() - t0,
        init_log=log[0] if log else None,
        final_log=log[-1] if log else None,
        n_optimizers=1,
        optimizer_kind="single_global_AdamW",
        algorithm="Psi-JEPA-COUPLE (head_g IS the predictor)",
        lambda_psi=lambda_psi,
        lambda_ce=lambda_ce,
        non_ce_supervision="MSE(predictor_head_g(residual_t), Psi(t+1))",
        ce_aux_kept_load_bearing=False,
        head_g_grad_norm_max=head_g_grad_norm_max,
        head_g_grad_norm_min=head_g_grad_norm_min,
        head_g_grad_norm_mean=head_g_grad_norm_mean,
        head_g_received_gradient=(head_g_grad_norm_min > 0.0),
    )
    with open(os.path.join(out_dir, "result.json"), "w") as f:
        json.dump(result, f, indent=2, default=str)
    print(f"[S167A-FPReconnect] DONE wall={result['train_wall_s']:.1f}s "
          f"ckpt={ckpt_path}  ||grad_head_g||=[{head_g_grad_norm_min:.6f}, "
          f"{head_g_grad_norm_max:.6f}]", flush=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", default="main", choices=["main", "sanity"])
    ap.add_argument("--corpus", required=True)
    ap.add_argument("--out-dir", required=True)
    ap.add_argument("--steps", type=int, default=3000)
    ap.add_argument("--lr", type=float, default=3e-4)
    ap.add_argument("--bsz", type=int, default=32)
    ap.add_argument("--block", type=int, default=128)
    ap.add_argument("--seed", type=int, default=1337)
    ap.add_argument("--lambda-psi", type=float, default=1.0,
                    help="Psi-JEPA-COUPLE objective weight (load-bearing)")
    ap.add_argument("--lambda-ce", type=float, default=0.1,
                    help="CE auxiliary weight (keeps head_a byte-valid)")
    ap.add_argument("--d-model", type=int, default=768)
    ap.add_argument("--n-layer", type=int, default=12)
    ap.add_argument("--n-head", type=int, default=12)
    ap.add_argument("--n-kv-head", type=int, default=4)
    ap.add_argument("--cpu-only", action="store_true")
    args = ap.parse_args()
    if args.mode == "main":
        cfg = dict(d_model=args.d_model, n_head=args.n_head,
                   n_kv_head=args.n_kv_head, n_layer=args.n_layer,
                   block_size=args.block, lr=args.lr, bsz=args.bsz,
                   steps=args.steps, seed=args.seed,
                   lambda_psi=args.lambda_psi, lambda_ce=args.lambda_ce,
                   log_every=max(1, args.steps // 40),
                   corpus=args.corpus, out_dir=args.out_dir,
                   cpu_only=args.cpu_only)
    else:
        cfg = dict(d_model=32, n_head=4, n_kv_head=2, n_layer=3,
                   block_size=64, lr=1e-3, bsz=8, steps=args.steps,
                   seed=args.seed,
                   lambda_psi=args.lambda_psi, lambda_ce=args.lambda_ce,
                   log_every=max(1, args.steps // 10),
                   corpus=args.corpus, out_dir=args.out_dir, cpu_only=True)
    run(cfg)


if __name__ == "__main__":
    main()
