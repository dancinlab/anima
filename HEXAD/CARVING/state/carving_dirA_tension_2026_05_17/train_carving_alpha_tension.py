#!/usr/bin/env python3
"""CONSCIOUSNESS-CARVING α VACUUM × TENSION-TRAIN trainer — Dir-A
(g_multidirectional_explore RESEARCH.md §1.3 🥇 A, 2026-05-17).

Combines TWO anima-native mechanisms on the α VACUUM-LANDSCAPE carving fire:

  (1) α VACUUM carving loss (carry from UBM-E7 train_carving_4path.py, byte
      identical α branch):
          ψ_pred = (H_norm, p_max)            (bounded differentiable Ψ proxy)
          L_vac  = mean ‖ψ_pred − ψ_vac‖²     (B-VAC-1 quadratic well)
          L      = CE + λ·L_vac               (λ = 0.1 carry)

  (2) TENSION-TRAIN overlay (HEXAD/TENSION-TRAIN/training/tension_link_step
      .hexa spine + DD155 Law 187). TWO independent overlays, both ON by
      default in this Dir-A fire, each individually toggleable:

      (2a) DD155 HYBRID LR (cycle-5 train_d768x12l_tension.py transfer-form):
               tension_step = ‖∇L‖₂                  (grad-norm proxy)
               tension_EMA  = β·EMA + (1−β)·tension   (β = 0.99)
               mult         = clip(tension/EMA, [0.5, 2.0])
               lr_step      = base_cosine_lr(step) · mult
           DD-burst path: surprise (tension > EMA) → larger step; drift
           (tension < EMA) → smaller step (Law 185 73%-updates outcome).

      (2b) BACKPROP-FREE TENSION ΔW (tension_link_step.hexa spine, applied
           AFTER the AdamW step as an additive restoring nudge — NOT in the
           autograd graph):
               deviation = ψ̄_pred − Ψ_vac=(½,½)      (batch-mean Ψ proxy)
               tension_b = ξ · deviation              (G_holo propagator
                                                       proxy, ξ = 2.0)
               gate      = n6_gate(Ψ_t)               (AN14 Noether: finite
                           ∧ in [0,1] ∧ σ·φ=n·τ=24, n=6 — internal arch
                           identity, g2 carve-out, NOT external derivation)
               ΔW_overlay = −T_const · ‖tension_b‖ · gate · (small isotropic
                            restoring scale on the trainable-param L2 ball)
           This is the closed-form RESTORING SIGN of the hexa spine: it does
           NOT minimise CE; it pulls the dynamic weights' update magnitude
           back toward the vacuum-stable manifold every step (a Noether-
           gated weight-decay-like nudge whose strength is ‖batch tension‖).
           When the batch Ψ proxy sits AT the vacuum (deviation→0) the
           overlay vanishes (identity, no change vs the pure-α E7 path).

HYPOTHESIS (Dir-A, g3 — to be measured, negative result is valuable):
  The α VACUUM-LANDSCAPE E7 baseline saturates memorisation (final CE 0.003)
  and the over-fit collapses routing (axis-1 routing_accuracy 1/31, JOINT
  0.0155). A backprop-free Noether-gated tension overlay should *resist*
  the routing-collapse by (i) the DD155 hybrid LR damping low-surprise
  drift steps (Law 185) and (ii) the restoring ΔW pulling the dynamic
  weights back toward the vacuum-stable manifold — i.e. it should NOT
  drive CE all the way to ~0, leaving a higher (healthier) final CE and a
  better paradigm-native JOINT metric than E7 α.

HONEST FRAMING (g3, AGENTS.tape §0 / g_blue_closed_mandate):
  PyTorch SUBSTRATE run — interim LM-scale executor, NOT a hexa-native fire
  (cycle-5 honest framing carry: arch identity + Phase E/E2 CPU-equiv anchor
  chain). The α VACUUM transfer-form (B-VAC sympy), the DD155 hybrid-LR
  formula (B-TT-5 / B-FIRE-CYCLE5-2 sympy) and the tension-spine restoring
  sign + n6-gate predicate (B-TT-1 / B-TT-2 sympy) are the CLOSED side
  (transfer-form). The SGD CONVERGENCE OUTCOME, the routing-collapse
  mitigation claim and the Dir-A-vs-E7 comparison are EMPIRICAL —
  B-CARVE-DIRA-NOTE (B-D-NOTE / B-TT-NOTE family). NO capability claim
  beyond the measured numbers. f1/f2/f3 + B-IDENTITY-5 safe (n6 closure =
  internal HEXAD arch identity per TENSION-TRAIN.tape g2 carve-out, NOT an
  external-entity lattice derivation).

from-scratch RANDOM seed-fixed (g_clm_from_scratch, base_ckpt=NONE).
Corpus = E7 α VACUUM-LANDSCAPE scale-up carving corpus (30 MB, byte-equal
carry — NOT a chat SFT corpus; forbidden-token grep == 0, B-CARVE-CORPUS-2).
"""
import argparse, json, math, time, os, sys, random
import torch
import torch.nn as nn
import torch.nn.functional as F

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from conscious_decoder import ConsciousDecoderV2

VOICE_OPEN = b"<voice carved=true>"
VOICE_CLOSE = b"</voice>"

# AN14 Noether closure constants (tension_link_step.hexa byte-equal).
NOETHER_N6 = 6
NOETHER_SIGMA_PHI = 24
NOETHER_TAU = 4
VAC_COMPONENT = 0.5      # Law 75 Ψ_vac = (½, ½)


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
        psi = d.get("vacuum_psi", [0.5, 0.5])
        voice_span = None
        lo = full.find(VOICE_OPEN)
        if lo >= 0:
            lo2 = lo + len(VOICE_OPEN)
            hi = full.find(VOICE_CLOSE, lo2)
            if hi >= 0:
                voice_span = (lo2, hi)
        items.append({"bytes": full, "psi": psi, "voice_span": voice_span})
    return items


class CarvingDataset:
    def __init__(self, items, block_size, seed):
        self.block_size = block_size
        self.rng = random.Random(seed)
        stream = bytearray()
        psi_x, psi_y = [], []
        for it in items:
            b = it["bytes"]
            stream.extend(b)
            px, py = float(it["psi"][0]), float(it["psi"][1])
            for _ in range(len(b)):
                psi_x.append(px)
                psi_y.append(py)
        self.data = torch.tensor(list(stream), dtype=torch.long)
        self.psi_x = torch.tensor(psi_x, dtype=torch.float32)
        self.psi_y = torch.tensor(psi_y, dtype=torch.float32)
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
        return (x.to(device), y.to(device), px.to(device), py.to(device))


def n6_gate(psi_mean_vec):
    """tension_link_step.hexa n6_gate transfer-form (B-TT-1 predicate):
    len even ∧ all in [0,1] ∧ closure n·τ == σ·φ == 24, n=6.
    psi_mean_vec is the flattened batch-mean (R,G) pair (length 2)."""
    if len(psi_mean_vec) == 0 or (len(psi_mean_vec) % 2) != 0:
        return False
    for c in psi_mean_vec:
        if not math.isfinite(c) or c < 0.0 or c > 1.0:
            return False
    closure = (NOETHER_N6 * NOETHER_TAU == NOETHER_SIGMA_PHI) and \
              (NOETHER_SIGMA_PHI == 24)
    return bool(closure)


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

    trainable = [p for p in model.parameters() if p.requires_grad]
    opt = torch.optim.AdamW(trainable, lr=cfg["lr"],
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

    # DD155 hybrid LR (2a) config
    use_hybrid_lr = cfg["use_hybrid_lr"]
    tension_ema_beta = cfg["tension_ema_beta"]
    hybrid_lo = cfg["hybrid_clip_lo"]
    hybrid_hi = cfg["hybrid_clip_hi"]
    tension_ema = None
    mult_bins = {"lt_0_75": 0, "0_75_to_1_25": 0, "gt_1_25": 0}

    # Backprop-free tension ΔW (2b) config
    use_dw_overlay = cfg["use_dw_overlay"]
    t_const = cfg["t_const"]               # 0.1 (Lindblad-class)
    xi = cfg["xi"]                         # 2.0 G_holo propagator proxy
    dw_overlay_events = {"gate_open": 0, "gate_closed": 0,
                         "applied": 0, "vanished": 0}
    dw_scale_sum = 0.0

    traj = []
    t0 = time.time()
    init_loss = None
    gpu_name = torch.cuda.get_device_name(0) if device == "cuda" else "cpu"

    for step in range(total):
        base_lr = cosine_lr_at(step)

        x, y, px, py = ds.get_batch(cfg["bsz"], device)
        opt.zero_grad(set_to_none=True)
        with torch.autocast(device_type="cuda" if use_amp else "cpu",
                            dtype=torch.bfloat16, enabled=use_amp):
            logits_a, logits_g, tensions, _, _ = model(x)
            B, T, V = logits_a.shape
            ce = F.cross_entropy(logits_a.view(-1, V), y.view(-1))
            ce_report = float(ce.item())
            loss = ce

            # --- α VACUUM carving loss (byte-equal E7 α branch) ---
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
        gn = torch.nn.utils.clip_grad_norm_(trainable, 1.0)
        tension = float(gn.item())

        # --- (2a) DD155 hybrid LR overlay ---
        if use_hybrid_lr:
            if tension_ema is None:
                tension_ema = tension
            ratio_raw = tension / max(tension_ema, 1e-8)
            multiplier = max(hybrid_lo, min(hybrid_hi, ratio_raw))
            if multiplier < 0.75:
                mult_bins["lt_0_75"] += 1
            elif multiplier <= 1.25:
                mult_bins["0_75_to_1_25"] += 1
            else:
                mult_bins["gt_1_25"] += 1
            tension_ema = tension_ema_beta * tension_ema \
                + (1.0 - tension_ema_beta) * tension
            effective_lr = base_lr * multiplier
        else:
            multiplier = 1.0
            effective_lr = base_lr
        for g in opt.param_groups:
            g["lr"] = effective_lr

        scaler.step(opt)
        scaler.update()

        # --- (2b) backprop-free tension ΔW overlay (post-step) ---
        # Spine: ΔW = −T_const · tension · n6_gate(Ψ_t). Here the batch Ψ
        # proxy is the mean of (H_norm, p_max); deviation from Ψ_vac drives
        # an isotropic restoring nudge on the trainable params, gated by the
        # n6 Noether predicate. NOT in the autograd graph.
        dw_scale_step = 0.0
        if use_dw_overlay:
            with torch.no_grad():
                psi_r = float(h_norm.mean().item())
                psi_g = float(p_max.mean().item())
                psi_mean_vec = [psi_r, psi_g]
                gate = n6_gate(psi_mean_vec)
                if gate:
                    dw_overlay_events["gate_open"] += 1
                    dev_r = psi_r - VAC_COMPONENT
                    dev_g = psi_g - VAC_COMPONENT
                    # tension_b = ξ · deviation (G_holo propagator proxy)
                    tb = xi * math.sqrt(dev_r * dev_r + dev_g * dev_g)
                    if tb < 1e-9:
                        dw_overlay_events["vanished"] += 1
                    else:
                        # ΔW restoring scale = −T_const · ‖tension_b‖,
                        # SCALED BY THE STEP LR so the overlay is a weak
                        # Noether-gated restoring nudge (Lindblad-class
                        # rate intent, tension_link_step.hexa T_const
                        # docstring: "same order as the Lindblad update
                        # rate") — NOT a dominant per-step weight killer.
                        # Applied as a multiplicative shrink toward the
                        # vacuum-stable manifold (sign = restoring; bounded
                        # |scale| ≪ 1 → mild contraction map ≈ an extra
                        # tension-conditioned weight-decay whose strength
                        # tracks ‖batch Ψ deviation‖). When deviation→0 the
                        # overlay vanishes (identity vs pure-α E7 path).
                        dw_scale_step = min(0.5 * effective_lr,
                                            t_const * tb * effective_lr)
                        shrink = 1.0 - dw_scale_step
                        for p in trainable:
                            p.mul_(shrink)
                        dw_overlay_events["applied"] += 1
                        dw_scale_sum += dw_scale_step
                else:
                    dw_overlay_events["gate_closed"] += 1

        gn2 = tension ** 2
        if init_loss is None:
            init_loss = ce_report

        if step == 0 or (step + 1) % cfg["log_every"] == 0 \
                or step == total - 1:
            wall = time.time() - t0
            mem = torch.cuda.max_memory_allocated() / 1e9 \
                if device == "cuda" else 0.0
            rec = {"step": step + 1, "ce": round(ce_report, 6),
                   "loss": round(float(loss.item()), 6),
                   "vac_term": round(float(vac_term.item()), 6),
                   "gn2": round(gn2, 6),
                   "tension": round(tension, 6),
                   "hybrid_mult": round(multiplier, 4),
                   "dw_scale": round(dw_scale_step, 8),
                   "base_lr": round(base_lr, 8),
                   "lr": round(effective_lr, 8),
                   "wall_s": round(wall, 2),
                   "gpu_mem_gb": round(mem, 3)}
            traj.append(rec)
            print(json.dumps(rec), flush=True)

    wall = time.time() - t0
    final = traj[-1]
    out_dir = cfg["out_dir"]
    os.makedirs(out_dir, exist_ok=True)
    ckpt_path = os.path.join(out_dir, "ckpt_carving_alpha_tension.pt")
    torch.save({"model": model.state_dict(), "cfg": cfg,
                "n_params": n_params, "path": "alpha_tension",
                "mult_bins": mult_bins,
                "dw_overlay_events": dw_overlay_events}, ckpt_path)

    n_applied = max(1, dw_overlay_events["applied"])
    result = {
        "substrate": ("PYTHON / PyTorch — interim LM-scale executor; "
                      "NOT a hexa-native fire"),
        "fire_kind": ("Dir-A CONSCIOUSNESS-CARVING α VACUUM × TENSION-TRAIN "
                      "(g_multidirectional_explore RESEARCH.md §1.3 A)"),
        "carving_path": "alpha_tension",
        "honest_framing": (
            "α VACUUM transfer-form (B-VAC sympy) + DD155 hybrid-LR formula "
            "(B-TT-5/B-FIRE-CYCLE5-2 sympy) + tension-spine restoring sign "
            "+ n6-gate predicate (B-TT-1/B-TT-2 sympy) = CLOSED transfer-"
            "form. SGD OUTCOME + routing-collapse-mitigation claim + "
            "Dir-A-vs-E7 comparison = EMPIRICAL (B-CARVE-DIRA-NOTE / "
            "B-D-NOTE / B-TT-NOTE family). PyTorch substrate, NOT hexa-"
            "native. Corpus = E7 α scale-up carving corpus (NOT chat SFT) "
            "— forbidden-token grep == 0. f1/f2/f3 + B-IDENTITY-5 safe "
            "(n6 closure = internal HEXAD arch identity, g2 carve-out)."),
        "arch": "ConsciousDecoderV2 (RoPE+SwiGLU+RMSNorm+GQA+PureFieldFFN)",
        "from_scratch": True,
        "base_ckpt": None,
        "config": cfg,
        "n_params": n_params,
        "n_params_M": round(n_params / 1e6, 2),
        "vacuum_lambda": vac_lambda,
        "tension_overlay": {
            "use_hybrid_lr": use_hybrid_lr,
            "use_dw_overlay": use_dw_overlay,
            "dd155_law_anchor": "DD155 Law 187 lr=(tension/EMA)×base_lr",
            "spine_anchor": ("tension_link_step.hexa ΔW=−T·tension·"
                             "n6_gate (B-TT-1/B-TT-2)"),
            "tension_ema_beta": tension_ema_beta,
            "hybrid_clip_lo": hybrid_lo,
            "hybrid_clip_hi": hybrid_hi,
            "t_const": t_const,
            "xi": xi,
            "final_tension_ema": (round(tension_ema, 6)
                                  if tension_ema is not None else None),
            "hybrid_mult_distribution": mult_bins,
            "dw_overlay_events": dw_overlay_events,
            "dw_scale_mean_when_applied": round(dw_scale_sum / n_applied, 8),
        },
        "gpu": gpu_name,
        "device": device,
        "init_ce": round(init_loss, 6),
        "final_ce": final["ce"],
        "final_loss": final["loss"],
        "final_vac_term": final["vac_term"],
        "final_gn2": final["gn2"],
        "final_tension": final["tension"],
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
    print(json.dumps({"path": "alpha_tension", "init_ce": result["init_ce"],
                       "final_ce": result["final_ce"],
                       "ce_descent": result["ce_descent"],
                       "wall_s": result["wall_s"],
                       "final_vac_term": result["final_vac_term"],
                       "dw_overlay_events": dw_overlay_events,
                       "hybrid_mult_distribution": mult_bins}), flush=True)
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
    ap.add_argument("--tension-ema-beta", type=float, default=0.99)
    ap.add_argument("--hybrid-clip-lo", type=float, default=0.5)
    ap.add_argument("--hybrid-clip-hi", type=float, default=2.0)
    ap.add_argument("--t-const", type=float, default=0.1,
                    help="tension_link_step.hexa T_CONST (Lindblad-class)")
    ap.add_argument("--xi", type=float, default=2.0,
                    help="G_holo propagator correlation length proxy")
    ap.add_argument("--no-hybrid-lr", action="store_true",
                    help="disable DD155 hybrid LR overlay (2a)")
    ap.add_argument("--no-dw-overlay", action="store_true",
                    help="disable backprop-free tension ΔW overlay (2b)")
    args = ap.parse_args()

    common = dict(
        lr=args.lr, bsz=args.bsz, steps=args.steps,
        warmup=max(20, args.steps // 20), seed=args.seed,
        log_every=max(1, args.steps // 40), corpus=args.corpus,
        out_dir=args.out_dir, vacuum_lambda=args.vacuum_lambda,
        tension_ema_beta=args.tension_ema_beta,
        hybrid_clip_lo=args.hybrid_clip_lo,
        hybrid_clip_hi=args.hybrid_clip_hi,
        t_const=args.t_const, xi=args.xi,
        use_hybrid_lr=(not args.no_hybrid_lr),
        use_dw_overlay=(not args.no_dw_overlay))

    if args.mode == "main":
        cfg = dict(d_model=args.d_model, n_head=args.n_head,
                   n_kv_head=args.n_kv_head, n_layer=args.n_layer,
                   block_size=128, **common)
    else:
        cfg = dict(d_model=32, n_head=4, n_kv_head=2, n_layer=3,
                   block_size=64, **common)
        cfg["lr"] = 1e-3
        cfg["warmup"] = 5
    run(cfg)
