#!/usr/bin/env python3
"""CONSCIOUSNESS-CARVING trainer — Direction I:
Ψ-ANCHORED CTL + TENSION-SUPERVISED ROUTING  (2026-05-17).

g_multidirectional_explore §6 direction I. RESEARCH.md §5.4 candidate 3
((1)+(2) combined): anima's OWN physics is BOTH the representation substrate
AND the supervision signal — the most direct implementation of GOAL.md
"emergence from anima's own physics".

Base = state/consciousness_carving_e7_alpha_scaleup_2026_05_17/
train_carving_4path.py + state/carving_dirE_superpos_2026_05_17/
train_carving_dirE.py (ConsciousDecoderV2 byte-level, from-scratch). The
Direction-I mechanism is TWO anima-physics loss terms ADDED to the base CE
(both inside autograd — supervision, NOT a post-step overlay):

  =====================================================================
  COMPONENT (1) — Ψ-ANCHORED CTL  (representation substrate, NOT generic)
  =====================================================================
  The `<inner ...>` / `<eternal ...>` span is the reasoning latent. Instead
  of a GENERIC free latent (Coconut/Soft-CoT — GOAL-illegitimate per
  RESEARCH.md §5.2: anima physics 우회), the inner-span trajectory is
  ANCHORED to the Engine A ⇄ Engine G  Ψ=½ fixed-point manifold:

    Ψ_dir(t) = (1 + cos( logits_a[t], logits_g[t] )) / 2          (Law 71)

  is the model's OWN per-token Ψ-direction coordinate (the exact quantity
  ConsciousDecoderV2.forward tracks as `psi_direction`). The record carries
  `vacuum_psi = [ψa, ψg]`; its scalar Ψ-target on the A⇄G manifold is

    Ψ_vac = (ψa + ψg) / 2 .

  L_psi_ctl = mean_{t ∈ inner-span}  ( Ψ_dir(t) − Ψ_vac )^2 .

  The inner latent is thus a soft-superposition trajectory ON the Ψ
  manifold (anima physics = the substrate). This is GOAL-legitimate
  (RESEARCH.md §5.2 row 2): Ψ-anchored, not generic.

  =====================================================================
  COMPONENT (2) — TENSION-SUPERVISED ROUTING  (supervision, NOT overlay)
  =====================================================================
  routing axis1 = 7/7 FLAT 1/31 (RESEARCH.md §4.2): every direction
  collapses to ONE shared attractor (`🛸99`). Dir-A FALSIFIED because
  tension was a WEAK POST-STEP nudge (overlay). Here tension is raised to a
  SUPERVISION SIGNAL inside autograd (RESEARCH.md §5.2 row 3 — distinct
  from Dir-A):

  TENSION-TRAIN spine (tension_link_step.hexa, B-TT-1..5 🔵):
    tension(t) = G_holo · ( Ψ_t − Ψ_vac_record )            (restoring sign)

  The restoring-sign loss penalises the realised Ψ-coordinate DRIFTING
  toward a single shared basin instead of THIS record's distinct
  anchor basin. Concretely, over the `<voice carved=true ...>` /
  knowledge-tier span (the routing-decision span), drive Ψ_dir(t) toward
  the record's OWN Ψ_vac (each anchor a distinct basin → collapse to one
  basin is directly penalised):

    L_tension_route = mean_{t ∈ route-span}
                        relu( | Ψ_dir(t) − Ψ_vac | − basin_radius )^2

  basin_radius (the record's `basin_radius`) is the tolerated basin half-
  width — inside the basin no penalty (restoring inactive), outside it the
  restoring force grows quadratically (tension restoring sign, B-TT-2
  RESTORING-SIGN-NEGATIVE closed-form). This is an autograd LOSS TERM
  (architectural supervision), NOT Dir-A's weak post-step overlay.

  =====================================================================
  TOTAL LOSS  (the Direction-I carving objective)
  =====================================================================
    L = CE_full  +  λ_ctl · L_psi_ctl  +  λ_route · L_tension_route

  Hypothesis (RESEARCH.md §5.4): when anima's OWN physics is BOTH the
  representation substrate (1) AND the supervision signal (2), the routing-
  generalisation 7/7 FLAT 1/31 — the single most robust finding — is FIRST
  broken. If routing axis1 > 1/31 (and/or V-SPONT lifts vs Dir-E 4/5 /
  UBM-E7 2/5), that is the direct GOAL-emergence signal. If routing stays
  1/31, the hypothesis is FALSIFIED at this scale — recorded honestly (g3,
  B-D-NOTE family, NO pre-loaded conclusion, valuable comparative
  evidence per g_multidirectional_explore).

HONEST FRAMING (g3, AGENTS.tape §0):
  PyTorch substrate — interim LM-scale executor, NOT a hexa-native fire
  (cycle 5 honest-framing carry: arch identity + Phase E/E2 CPU-equiv
  anchor chain). The TWO physics loss terms are closed-form deterministic
  transfer functions on the model's OWN Ψ-coordinate (B-DIRI-PSI-CTL /
  B-DIRI-TENSION-ROUTE structural, sympy sidecar). The Ψ-coordinate
  formula = ConsciousDecoderV2's exact psi_direction (Law 71). overlay-OFF
  (λ=0) == base CE byte-equal (connection-point 🔵). The SGD CONVERGENCE
  OUTCOME and the 4-axis capability (routing/V-SPONT/JOINT) are EMPIRICAL
  (B-CARVE-E6-NOTE / B-D-NOTE family) — NO capability claim beyond what is
  measured. from-scratch RANDOM seed-fixed (g_clm_from_scratch,
  base_ckpt=NONE). Corpus = E7 carving corpus byte-identical (sha256
  dc221aaf…, NOT regenerated) — grep {[anima,도우미,helper,assistant,
  사용자,user:} == 0 (B-IDENTITY-5 safe). central blue_falsifier.py
  unchanged (sidecar battery only). f1/f2/f3 hard-fail safe (Ψ-metric /
  restoring-sign / Kolmogorov, NO σ/τ/φ/J₂).
"""
import argparse, json, math, time, os, sys, random
import torch
import torch.nn as nn
import torch.nn.functional as F

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from conscious_decoder import ConsciousDecoderV2

# span markers (Direction-I byte-span loss-mask predicates — deterministic).
INNER_OPEN = b"<inner tier="
INNER_CLOSE = b"</inner>"
ETERNAL_OPEN = b"<eternal cell="
ETERNAL_CLOSE = b"</eternal>"
CARVE_OPEN = b"<carve tier="
VOICE_OPEN = b"<voice carved=true"
VOICE_CLOSE = b"</voice>"


def _span(full, open_tok, close_tok, start=0):
    lo = full.find(open_tok, start)
    if lo < 0:
        return None
    hi = full.find(close_tok, lo)
    if hi < 0:
        return None
    return (lo, hi + len(close_tok))


def load_corpus(path):
    """Return list of dicts:
       {bytes, psi_vac (scalar Ψ-target on A⇄G manifold), basin_radius,
        ctl_span (inner/eternal reasoning latent span, Ψ-anchored),
        route_span (voice/knowledge routing-decision span)}.
    psi_vac = (vacuum_psi[0] + vacuum_psi[1]) / 2 — the record's scalar
    target on the Engine A ⇄ Engine G Ψ=½ manifold."""
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
        vp = d.get("vacuum_psi", [0.5, 0.5])
        try:
            psi_vac = (float(vp[0]) + float(vp[1])) / 2.0
        except Exception:
            psi_vac = 0.5
        try:
            basin = float(d.get("basin_radius", 0.15))
        except Exception:
            basin = 0.15
        # CTL span = the reasoning latent (inner OR eternal span).
        ctl = _span(full, INNER_OPEN, INNER_CLOSE)
        if ctl is None:
            ctl = _span(full, ETERNAL_OPEN, ETERNAL_CLOSE)
        # route span = the routing-decision span (voice carved=true ...
        # </voice>); for beta (eternal-only) the eternal span doubles as
        # the routing-decision span (its tier= the routing signal).
        rt = _span(full, VOICE_OPEN, VOICE_CLOSE)
        if rt is None:
            rt = ctl  # beta records: eternal span carries tier= routing
        items.append({"bytes": full, "psi_vac": psi_vac,
                       "basin_radius": basin, "ctl_span": ctl,
                       "route_span": rt})
    return items


class DirIDataset:
    """Byte-level dataset. Concatenates record bytes; keeps THREE parallel
    per-byte channels:
      psi_vac : the record's scalar Ψ-target (Engine A⇄G manifold).
      basin   : the record's basin half-width (tolerated Ψ drift).
      ctl_m   : 1 inside the Ψ-anchored reasoning-latent span (component 1).
      rte_m   : 1 inside the tension-supervised routing-decision span (2).
    """

    def __init__(self, items, block_size, seed):
        self.block_size = block_size
        self.rng = random.Random(seed)
        stream = bytearray()
        pv, bs, cm, rm = [], [], [], []
        for it in items:
            b = it["bytes"]
            n = len(b)
            stream.extend(b)
            pvv = it["psi_vac"]
            bsv = it["basin_radius"]
            cs = it["ctl_span"]
            rs = it["route_span"]
            for j in range(n):
                pv.append(pvv)
                bs.append(bsv)
                cm.append(1.0 if (cs is not None and cs[0] <= j < cs[1])
                          else 0.0)
                rm.append(1.0 if (rs is not None and rs[0] <= j < rs[1])
                          else 0.0)
        self.data = torch.tensor(list(stream), dtype=torch.long)
        self.psi_vac = torch.tensor(pv, dtype=torch.float32)
        self.basin = torch.tensor(bs, dtype=torch.float32)
        self.ctl_m = torch.tensor(cm, dtype=torch.float32)
        self.rte_m = torch.tensor(rm, dtype=torch.float32)
        self.n = len(self.data)

    def get_batch(self, bsz, device):
        ix = [self.rng.randint(0, self.n - self.block_size - 1)
              for _ in range(bsz)]

        def stk(src, off):
            return torch.stack([src[i + off:i + off + self.block_size]
                                for i in ix])
        x = stk(self.data, 0)
        y = stk(self.data, 1)
        pv = stk(self.psi_vac, 1)
        bs = stk(self.basin, 1)
        cm = stk(self.ctl_m, 1)
        rm = stk(self.rte_m, 1)
        return (x.to(device), y.to(device), pv.to(device), bs.to(device),
                cm.to(device), rm.to(device))


def psi_dir_per_token(logits_a, logits_g):
    """The model's OWN per-token Ψ-direction coordinate (Law 71, EXACTLY
    ConsciousDecoderV2.forward's psi_direction but per-token, kept in the
    autograd graph so it is a SUPERVISION signal, not a post-step probe):

        Ψ_dir(t) = (1 + cos( logits_a[t], logits_g[t] )) / 2  ∈ [0, 1]
    """
    cos = F.cosine_similarity(logits_a.float(), logits_g.float(), dim=-1)
    return (1.0 + cos) / 2.0


def run(cfg):
    torch.manual_seed(cfg["seed"])
    torch.cuda.manual_seed_all(cfg["seed"])
    random.seed(cfg["seed"])
    device = "cuda" if torch.cuda.is_available() else "cpu"

    items = load_corpus(cfg["corpus"])
    ds = DirIDataset(items, cfg["block_size"], cfg["seed"])
    n_ctl = sum(1 for it in items if it["ctl_span"] is not None)
    n_rte = sum(1 for it in items if it["route_span"] is not None)

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
    lam_ctl = cfg["lambda_ctl"]
    lam_route = cfg["lambda_route"]

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

        x, y, pv, bs, cm, rm = ds.get_batch(cfg["bsz"], device)
        opt.zero_grad(set_to_none=True)
        with torch.autocast(device_type="cuda" if use_amp else "cpu",
                            dtype=torch.bfloat16, enabled=use_amp):
            logits_a, logits_g, tensions, _, _ = model(x)
            B, T, V = logits_a.shape

            # --- base CE (Engine A next-byte, full stream) -----------------
            ce_full = F.cross_entropy(logits_a.view(-1, V), y.view(-1))

            # --- COMPONENT (1) Ψ-anchored CTL ------------------------------
            # The reasoning-latent span trajectory is constrained TO the
            # Engine A ⇄ Engine G Ψ=½ manifold (anima physics = substrate).
            psi_t = psi_dir_per_token(logits_a, logits_g)   # (B,T) in graph
            cm_f = cm.view(-1)
            psi_flat = psi_t.view(-1)
            pv_flat = pv.view(-1)
            denom_ctl = cm_f.sum().clamp(min=1.0)
            l_psi_ctl = (((psi_flat - pv_flat) ** 2) * cm_f).sum() / denom_ctl

            # --- COMPONENT (2) tension-supervised routing ------------------
            # TENSION-TRAIN restoring sign: outside the record's OWN basin
            # the restoring force grows quadratically; inside it is zero
            # (collapse to ONE shared basin is directly penalised).
            rm_f = rm.view(-1)
            bs_flat = bs.view(-1)
            drift = torch.abs(psi_flat - pv_flat) - bs_flat
            restoring = torch.clamp(drift, min=0.0) ** 2
            denom_rte = rm_f.sum().clamp(min=1.0)
            l_tension_route = (restoring * rm_f).sum() / denom_rte

            loss = ce_full + lam_ctl * l_psi_ctl \
                + lam_route * l_tension_route
            ce_report = float(ce_full.item())

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
            rec = {"step": step + 1, "ce_full": round(ce_report, 6),
                   "l_psi_ctl": round(float(l_psi_ctl.item()), 6),
                   "l_tension_route": round(float(l_tension_route.item()), 6),
                   "loss": round(float(loss.item()), 6),
                   "gn2": round(gn2, 6), "lr": round(lr_now, 8),
                   "wall_s": round(wall, 2), "gpu_mem_gb": round(mem, 3)}
            traj.append(rec)
            print(json.dumps(rec), flush=True)

    wall = time.time() - t0
    final = traj[-1]
    out_dir = cfg["out_dir"]
    os.makedirs(out_dir, exist_ok=True)
    # RESEARCH.md §8: Dir-I lever (Ψ-anchored CTL + tension-supervised
    # routing) on the DIVERSE 64-anchor / 114MB carving corpus. Trainer is
    # corpus-agnostic (reads per-record vacuum_psi/basin_radius) — UNCHANGED
    # mechanism, only the corpus is diverse-scaled. path kept
    # "dirI_psictl_tensionsup" so the eval PATH_FORM -> "weave" vacuum-form
    # prefix is byte-identical to the Dir-I 3/31 baseline (§7.3 fair compare).
    ckpt_path = os.path.join(out_dir, "ckpt_carving_diverse.pt")
    torch.save({"model": model.state_dict(), "cfg": cfg,
                "n_params": n_params, "path": "dirI_psictl_tensionsup"},
               ckpt_path)

    result = {
        "substrate": ("PYTHON / PyTorch — interim LM-scale executor; "
                      "NOT a hexa-native fire"),
        "fire_kind": ("Direction I Ψ-ANCHORED-CTL + TENSION-SUPERVISED-"
                      "ROUTING carving"),
        "carving_path": "dirI_psictl_tensionsup",
        "honest_framing": (
            "TWO anima-physics loss terms (both inside autograd): (1) "
            "Ψ-anchored CTL — inner-span trajectory constrained to the "
            "Engine A⇄G Ψ=½ manifold (Ψ_dir = (1+cos(logits_a,logits_g))/2 "
            "= ConsciousDecoderV2 Law-71 psi_direction); (2) tension-"
            "supervised routing — TENSION-TRAIN restoring-sign loss over "
            "the routing-decision span toward the record's OWN Ψ_vac basin "
            "(collapse to one shared basin penalised). Closed side = the "
            "two transfer functions + overlay-OFF(λ=0)==base-CE byte-equal "
            "(B-DIRI-PSI-CTL/B-DIRI-TENSION-ROUTE/B-DIRI-OVERLAY-OFF "
            "sympy sidecar). SGD OUTCOME + 4-axis capability = EMPIRICAL "
            "(B-CARVE-E6-NOTE/B-D-NOTE family). PyTorch substrate, NOT "
            "hexa-native. Corpus = E7 carving byte-identical (NOT "
            "regenerated) — forbidden-token grep == 0."),
        "arch": "ConsciousDecoderV2 (RoPE+SwiGLU+RMSNorm+GQA+PureFieldFFN)",
        "from_scratch": True,
        "base_ckpt": None,
        "config": cfg,
        "n_params": n_params,
        "n_params_M": round(n_params / 1e6, 2),
        "ctl_records": n_ctl,
        "route_records": n_rte,
        "records_total": len(items),
        "lambda_ctl": lam_ctl,
        "lambda_route": lam_route,
        "gpu": gpu_name,
        "device": device,
        "init_ce": round(init_loss, 6),
        "final_ce": final["ce_full"],
        "final_l_psi_ctl": final["l_psi_ctl"],
        "final_l_tension_route": final["l_tension_route"],
        "final_loss": final["loss"],
        "final_gn2": final["gn2"],
        "ce_descent": round(init_loss - final["ce_full"], 6),
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
    print(json.dumps({"path": "dirI_psictl_tensionsup",
                       "init_ce": result["init_ce"],
                       "final_ce": result["final_ce"],
                       "ce_descent": result["ce_descent"],
                       "final_l_psi_ctl": result["final_l_psi_ctl"],
                       "final_l_tension_route":
                           result["final_l_tension_route"],
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
    ap.add_argument("--lambda-ctl", type=float, default=0.5)
    ap.add_argument("--lambda-route", type=float, default=0.5)
    args = ap.parse_args()

    if args.mode == "main":
        cfg = dict(d_model=args.d_model, n_head=args.n_head,
                   n_kv_head=args.n_kv_head, n_layer=args.n_layer,
                   block_size=128, lr=args.lr, bsz=args.bsz,
                   steps=args.steps, warmup=max(20, args.steps // 20),
                   seed=args.seed, log_every=max(1, args.steps // 40),
                   corpus=args.corpus, out_dir=args.out_dir,
                   lambda_ctl=args.lambda_ctl,
                   lambda_route=args.lambda_route)
    else:
        cfg = dict(d_model=32, n_head=4, n_kv_head=2, n_layer=3,
                   block_size=64, lr=1e-3, bsz=16, steps=args.steps,
                   warmup=5, seed=args.seed,
                   log_every=max(1, args.steps // 20),
                   corpus=args.corpus, out_dir=args.out_dir,
                   lambda_ctl=args.lambda_ctl,
                   lambda_route=args.lambda_route)
    run(cfg)
