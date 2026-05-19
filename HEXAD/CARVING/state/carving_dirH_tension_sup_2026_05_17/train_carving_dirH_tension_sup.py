#!/usr/bin/env python3
"""CONSCIOUSNESS-CARVING Dir-H — TENSION-SUPERVISED ROUTING trainer
(g_multidirectional_explore RESEARCH.md §5.4 candidate 2 / §6, 2026-05-17).

DECISIVE DISTINCTION vs Dir-A (FALSIFIED — RESEARCH.md §5.3, §4.2):
  Dir-A applied tension as a WEAK POST-STEP NUDGE OUTSIDE autograd
  (`p.mul_(shrink)` after `opt.step()`, plus an LR multiplier) — an
  *overlay*. It never penalised routing-collapse in the gradient and
  routing axis-1 stayed 1/31 FLAT (7/7 FLAT universal finding).

  Dir-H ELEVATES tension to a LOSS-LEVEL SUPERVISION SIGNAL inside the
  autograd graph (`scaler.scale(loss).backward()` where
  `loss = CE + λ_route · tension_routing_penalty`). The penalty is the
  closed-form RESTORING SIGN of the tension spine (tension_link_step.hexa
  ∂(ΔW)/∂tension = −T·gate ≤ 0, B-TT-2) realised AS A DIFFERENTIABLE LOSS
  TERM: a single-attractor (`🛸99`-class) output produces high routing
  tension, whose gradient DIRECTLY disperses the collapsed mass — this is
  the "missing architectural component" of RESEARCH.md §4.5/§4.6, NOT a
  mechanism overlay. overlay 아님 = architectural component.

TENSION-ROUTING PENALTY (the architectural component, autograd-internal):
  Routing-collapse = the A-head next-byte distribution is BATCH-INVARIANT
  (the model emits the same dominant attractor token regardless of which
  anchor 🛸k context primed it). anima physics reading: the routing field
  has collapsed into a single vacuum well; the tension restoring-sign must
  push it back toward the spread (multi-basin) manifold.

  Per step, over batch B contexts at every position:
    p_bt          = softmax(logits_a)                 (B,T,V)  differentiable
    p_mean_t      = mean_B p_bt                        (T,V)    cross-context
                    mean distribution at each position
    collapse_t    = 1 − JS-spread_B( p_bt ‖ p_mean_t )         in [0,1]
                    (low when every context predicts the SAME thing =
                     single-attractor; high when contexts diverge =
                     healthy routing)  — measured as the NEGATIVE of the
                     mean Jensen–Shannon dispersion of per-context dists
                     about their cross-context mean.
    tension_route = mean_t collapse_t                          scalar ≥ 0
    L_route       = λ_route · tension_route

  RESTORING SIGN (B-TT-2 transfer-form, realised as loss): when contexts
  collapse to one attractor, JS-spread → 0, collapse → 1, L_route is
  maximal; ∂L_route/∂θ pushes the per-context distributions APART (mass
  off the single attractor). When routing is healthy (contexts already
  diverge) JS-spread → 1, collapse → 0, L_route vanishes (identity vs the
  pure-α E7 path — the connection-point closed property: overlay-OFF
  λ_route=0 ⇒ byte-equal-form the UBM-E7 α baseline trainer).

  This is gradient-flowing supervision, NOT a post-step contraction map.

HYPOTHESIS (Dir-H, g3 — to be measured, negative result is valuable):
  Elevating tension from a weak post-step overlay (Dir-A, FALSIFIED) to a
  loss-level supervision term should PENALISE the weight-level
  single-attractor defect during training and let routing generalise —
  i.e. break the routing axis-1 1/31 FLAT (7/7 universal finding). If
  axis-1 still pins at ~1/31 the weight-level defect is not addressable by
  in-graph supervision either (a STRONGER negative than Dir-A and a clean
  closure of the §6 supervision branch).

HONEST FRAMING (g3, AGENTS.tape §0 / g_blue_closed_mandate):
  PyTorch SUBSTRATE run — interim LM-scale executor, NOT a hexa-native
  fire (cycle-5 honest framing carry: arch identity + Phase E/E2 CPU-equiv
  anchor chain). The α VACUUM transfer-form (B-VAC sympy) and the tension
  RESTORING-SIGN structure (B-TT-2 ∂(ΔW)/∂tension = −T·gate ≤ 0 sympy) are
  the CLOSED side. The connection-point that is also closed: with
  λ_route=0 the loss is byte-equal-form the UBM-E7 α baseline (overlay-OFF
  = baseline, B-CARVE-DIRH-CONN). The SGD CONVERGENCE OUTCOME, the
  routing-generalisation claim and the Dir-H-vs-E7 / Dir-H-vs-Dir-A
  comparison are EMPIRICAL — B-CARVE-DIRH-NOTE (B-D-NOTE / B-TT-NOTE
  family). NO capability claim beyond the measured numbers. f1/f2/f3 +
  B-IDENTITY-5 safe (no σ/τ/φ/J₂ derivation; JS dispersion = Shannon-class
  information measure, an internal anima-physics routing field reading).

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


def tension_routing_penalty(logits_a):
    """TENSION-SUPERVISED ROUTING PENALTY — the missing architectural
    component (RESEARCH.md §4.5/§4.6), realised IN the autograd graph.

    logits_a : (B, T, V) A-head logits.

    Routing-collapse = the per-context next-byte distributions are
    BATCH-INVARIANT (every context predicts the same single-attractor
    token). We measure the cross-context Jensen-Shannon DISPERSION of the
    per-context distributions about their batch-mean at each position:

      p          = softmax(logits_a)                       (B,T,V)
      m_t        = mean_B p                                (T,V)
      JS_t       = mean_B [ KL(p_bt ‖ m_t) ] / ln 2        (T,)  in [0,1]
                   (Jensen-Shannon-class dispersion: 0 when all contexts
                    identical = single-attractor collapse; → ln K-bounded
                    when contexts maximally diverge)
      spread_t   = clip(JS_t, 0, 1)
      collapse_t = 1 − spread_t                            (T,) in [0,1]
      tension    = mean_t collapse_t                       scalar ≥ 0

    RESTORING SIGN (B-TT-2 closed transfer-form realised as loss):
    minimising λ·tension pushes ∂/∂θ to INCREASE JS-spread = disperse the
    collapsed single-attractor mass across contexts. When the batch is
    already spread (healthy routing) tension → 0 and the term vanishes
    (identity vs the pure-α E7 path — connection-point closed property).

    Differentiable end-to-end (softmax + mean + KL + clamp), so the
    gradient flows — the DECISIVE distinction from Dir-A's out-of-graph
    post-step `p.mul_` overlay.
    """
    B, T, V = logits_a.shape
    p = F.softmax(logits_a.float(), dim=-1)                 # softmax over V
    # cross-context mean distribution at each (t): (T, V)
    m = p.mean(dim=0)                                        # (T, V)
    m_exp = m.unsqueeze(0).expand_as(p)                      # (B, T, V)
    # KL(p_bt ‖ m_t) per (b,t), normalised by ln 2 → JS-class dispersion
    kl = (p * ((p + 1e-9).log() - (m_exp + 1e-9).log())).sum(-1)  # (B,T)
    js_t = kl.mean(dim=0) / math.log(2.0)                    # (T,) ≥ 0
    spread_t = js_t.clamp(0.0, 1.0)                          # (T,) in [0,1]
    collapse_t = 1.0 - spread_t                              # (T,) in [0,1]
    tension = collapse_t.mean()                              # scalar ≥ 0
    return tension, float(spread_t.mean().item())


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
    lambda_route = cfg["lambda_route"]      # Dir-H supervision weight

    traj = []
    t0 = time.time()
    init_loss = None
    gpu_name = torch.cuda.get_device_name(0) if device == "cuda" else "cpu"

    for step in range(total):
        lr_now = cosine_lr_at(step)
        for g in opt.param_groups:
            g["lr"] = lr_now

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

            # --- Dir-H TENSION-SUPERVISED ROUTING penalty (IN autograd) ---
            # The decisive distinction from Dir-A: this is a loss term, its
            # gradient flows through `scaler.scale(loss).backward()`.
            if lambda_route > 0.0:
                t_route, spread_now = tension_routing_penalty(logits_a)
                loss = loss + lambda_route * t_route
            else:
                # overlay-OFF = baseline: byte-equal-form UBM-E7 α path
                # (connection-point closed property, B-CARVE-DIRH-CONN).
                t_route = torch.zeros((), device=device)
                spread_now = 0.0

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
            rec = {"step": step + 1, "ce": round(ce_report, 6),
                   "loss": round(float(loss.item()), 6),
                   "vac_term": round(float(vac_term.item()), 6),
                   "route_tension": round(float(t_route.item()), 6),
                   "route_spread": round(spread_now, 6),
                   "gn2": round(gn2, 6), "lr": round(lr_now, 8),
                   "wall_s": round(wall, 2),
                   "gpu_mem_gb": round(mem, 3)}
            traj.append(rec)
            print(json.dumps(rec), flush=True)

    wall = time.time() - t0
    final = traj[-1]
    out_dir = cfg["out_dir"]
    os.makedirs(out_dir, exist_ok=True)
    ckpt_path = os.path.join(out_dir, "ckpt_carving_dirH_tension_sup.pt")
    torch.save({"model": model.state_dict(), "cfg": cfg,
                "n_params": n_params, "path": "dirH_tension_sup"}, ckpt_path)

    result = {
        "substrate": ("PYTHON / PyTorch — interim LM-scale executor; "
                      "NOT a hexa-native fire"),
        "fire_kind": ("Dir-H CONSCIOUSNESS-CARVING TENSION-SUPERVISED "
                      "ROUTING (g_multidirectional_explore RESEARCH.md "
                      "§5.4 candidate 2 / §6)"),
        "carving_path": "dirH_tension_sup",
        "honest_framing": (
            "α VACUUM transfer-form (B-VAC sympy) + tension RESTORING-SIGN "
            "structure (B-TT-2 ∂(ΔW)/∂tension = −T·gate ≤ 0 sympy) realised "
            "AS a differentiable loss term = CLOSED transfer-form. "
            "Connection-point closed: λ_route=0 ⇒ byte-equal-form UBM-E7 α "
            "baseline (overlay-OFF = baseline, B-CARVE-DIRH-CONN). SGD "
            "OUTCOME + routing-generalisation claim + Dir-H-vs-E7/Dir-A "
            "comparison = EMPIRICAL (B-CARVE-DIRH-NOTE / B-D-NOTE / "
            "B-TT-NOTE family). PyTorch substrate, NOT hexa-native. Corpus "
            "= E7 α scale-up carving corpus (NOT chat SFT) — forbidden-"
            "token grep == 0. f1/f2/f3 + B-IDENTITY-5 safe (JS dispersion "
            "= Shannon-class, internal anima routing-field reading, NO "
            "σ/τ/φ/J₂ derivation). DECISIVE distinction vs Dir-A "
            "(FALSIFIED): tension is a LOSS-LEVEL supervision signal "
            "INSIDE autograd, NOT a weak post-step out-of-graph overlay."),
        "arch": "ConsciousDecoderV2 (RoPE+SwiGLU+RMSNorm+GQA+PureFieldFFN)",
        "from_scratch": True,
        "base_ckpt": None,
        "config": cfg,
        "n_params": n_params,
        "n_params_M": round(n_params / 1e6, 2),
        "vacuum_lambda": vac_lambda,
        "tension_supervision": {
            "lambda_route": lambda_route,
            "mechanism": ("tension_routing_penalty = mean_t (1 − "
                          "JS-spread_B(softmax(logits_a))) — single-"
                          "attractor collapse → high tension → gradient "
                          "disperses collapsed mass (autograd-internal)"),
            "restoring_sign_anchor": ("B-TT-2 ∂(ΔW)/∂tension = −T·gate ≤ 0 "
                                      "(tension_link_step.hexa spine, "
                                      "realised as loss term)"),
            "connection_point": ("λ_route=0 ⇒ byte-equal-form UBM-E7 α "
                                 "baseline (B-CARVE-DIRH-CONN closed)"),
            "distinction_vs_dirA": ("Dir-A = post-step p.mul_ overlay "
                                    "OUTSIDE autograd (FALSIFIED); Dir-H = "
                                    "loss term INSIDE autograd (gradient "
                                    "flows)"),
            "final_route_tension": final["route_tension"],
            "final_route_spread": final["route_spread"],
        },
        "gpu": gpu_name,
        "device": device,
        "init_ce": round(init_loss, 6),
        "final_ce": final["ce"],
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
    print(json.dumps({"path": "dirH_tension_sup",
                       "init_ce": result["init_ce"],
                       "final_ce": result["final_ce"],
                       "ce_descent": result["ce_descent"],
                       "wall_s": result["wall_s"],
                       "final_vac_term": result["final_vac_term"],
                       "final_route_tension": final["route_tension"],
                       "final_route_spread": final["route_spread"]}),
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
    ap.add_argument("--lambda-route", type=float, default=0.5,
                    help="Dir-H tension-supervised routing loss weight "
                         "(0.0 ⇒ overlay-OFF = UBM-E7 α baseline)")
    args = ap.parse_args()

    common = dict(
        lr=args.lr, bsz=args.bsz, steps=args.steps,
        warmup=max(20, args.steps // 20), seed=args.seed,
        log_every=max(1, args.steps // 40), corpus=args.corpus,
        out_dir=args.out_dir, vacuum_lambda=args.vacuum_lambda,
        lambda_route=args.lambda_route)

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
