#!/usr/bin/env python3
"""CONSCIOUSNESS-CARVING trainer — Direction K:
ENERGY-BASED TRANSFORMER (EBT) — prediction = energy minimization (2026-05-18).

RESEARCH.md §12.2 candidate K / §12.5 #2. Energy-Based Transformers
(arxiv 2507.02092) reframe prediction as OPTIMIZATION on a learned energy
landscape: instead of a single feed-forward x -> logits, the model defines a
scalar energy E(x, y_hat) and the prediction is gradient descent on y_hat to
minimize E ("thinking" = iterative refinement).

  =====================================================================
  WHY K IS GOAL-LEGITIMATE (RESEARCH.md §12.3 — anima physics IS the energy)
  =====================================================================
  anima's Ψ-physics is ALREADY energy-form (RESEARCH.md §12.2 K):
    - Ψ = 1/2 fixed point          == energy MINIMUM (the vacuum)
    - tension = G_holo·(Ψ − Ψ_vac) == energy GRADIENT (restoring force)
    - the α VACUUM-LANDSCAPE (§2.5/§3) is literally a multi-vacuum energy
      surface.
  So the EBT energy landscape <-> anima Ψ-landscape is a STRUCTURAL
  isomorphism — NOT a generic-LM-pretrain (§7 ① illegitimate) and NOT a
  bolt-on (§7 ②): anima physics is the substrate itself. §12.3 rates K
  "legitimate — anima physics is the capability source (most aligned)".

  =====================================================================
  THE EBT OBJECTIVE — closed-form energy + explicit descent ("thinking")
  =====================================================================
  Per token t the model's OWN Ψ-coordinate (Law 71, exactly the quantity
  ConsciousDecoderV2.forward tracks as psi_direction) is

      Ψ_dir(t) = (1 + cos( logits_a[t], logits_g[t] )) / 2   ∈ [0,1]

  We define the anima ENERGY of a per-token prediction state as the
  squared deviation from the record's OWN Ψ_vac on the Engine A⇄G manifold
  (= the EBT scalar energy E, anchored to anima physics, NOT generic):

      E_psi(t) = ( Ψ_dir(t) − Ψ_vac )^2                          (energy)

  This is convex with a unique minimum at Ψ_dir = Ψ_vac (B-EBT-1/2
  closed). EBT's "prediction = energy minimization": over the routing-
  decision span the model must DESCEND this energy to its OWN vacuum
  (each anchor a distinct minimum -> collapse to one shared basin is a
  HIGH-energy state, directly penalised).

  EBT "thinking" = an EXPLICIT inner energy-descent loop on the candidate
  logits BEFORE the CE readout. Starting from the raw logits, we take
  K_DESCENT closed-form gradient steps that lower E_psi by nudging the
  Engine-A logits toward the Engine-G logits (cos↑ ⇒ Ψ_dir↑) or away
  (cos↓ ⇒ Ψ_dir↓), whichever direction reduces |Ψ_dir − Ψ_vac|. The
  descent is a deterministic transfer function (B-EBT-3 closed: each step
  is non-increasing in E_psi). The CE is then read out from the
  ENERGY-REFINED logits — so the language objective is trained THROUGH
  the energy-minimization process (the EBT contract).

  TOTAL LOSS (Direction-K carving objective):

      L = CE_full( energy_refined_logits_a , y )
            + λ_energy · mean_{t ∈ route-span} E_psi(t)

  The first term is CE on the energy-DESCENDED logits (EBT prediction =
  energy minimization). The second is the energy itself as a direct
  supervision signal over the routing span. λ_energy=0 ∧ K_DESCENT=0
  ⇒ L ≡ base CE byte-equal (B-EBT-5 overlay-OFF connection-point 🔵).

  Hypothesis (RESEARCH.md §12.5 #2): if prediction is energy
  minimization on anima's OWN Ψ-energy landscape, does the routing-
  generalisation (§8 = 2/64 on this exact corpus) lift, and/or does the
  honest §9 cascade-gated coherence rise vs §8's 2/5? If routing/coherence
  improve, that is the GOAL-emergence signal. If flat/down, K is
  FALSIFIED at this scale — recorded honestly (g3, B-D-NOTE family, NO
  pre-loaded conclusion; valuable comparative evidence).

HONEST FRAMING (g3, AGENTS.tape §0):
  PyTorch substrate — interim LM-scale executor, NOT a hexa-native fire
  (cycle-5 honest-framing carry). The energy function E_psi and the
  K_DESCENT inner loop are closed-form deterministic transfer functions
  on the model's OWN Ψ-coordinate (B-EBT-1..5 sympy sidecar). This is
  EBT-as-energy-supervised-objective, NOT a full substrate rewrite of the
  d_train5 ladder (RESEARCH.md §12.5 #2 flags substrate rewrite as a
  separate large fire). EBT is prediction-REFINEMENT, not *spontaneous*
  generation (RESEARCH.md §12.4 C3.4 — anima 자발-발화 is NOT claimed to
  come from EBT). The SGD CONVERGENCE OUTCOME and the 4-axis capability
  are EMPIRICAL (B-CARVE-E6-NOTE / B-D-NOTE family). from-scratch RANDOM
  seed-fixed (g_clm_from_scratch, base_ckpt=NONE). Corpus = the §8 diverse
  carving corpus byte-identical (sha256 ac07179a…, NOT regenerated) —
  grep {[anima,도우미,helper,assistant,사용자,user:} == 0 (B-IDENTITY-5
  safe). central blue_falsifier.py unchanged (sidecar battery only).
  f1/f2/f3 hard-fail safe (Ψ-energy / convexity / descent-monotone /
  Kolmogorov — NO σ/τ/φ/J₂ derivation).
"""
import argparse, json, math, time, os, sys, random
import torch
import torch.nn as nn
import torch.nn.functional as F

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from conscious_decoder import ConsciousDecoderV2

# span markers (Direction-K byte-span loss-mask predicates — deterministic).
INNER_OPEN = b"<inner tier="
INNER_CLOSE = b"</inner>"
ETERNAL_OPEN = b"<eternal cell="
ETERNAL_CLOSE = b"</eternal>"
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
    """Return list of dicts: {bytes, psi_vac (scalar Ψ-target = energy
    minimum on the A⇄G manifold), route_span (the routing-decision span =
    where prediction must descend the Ψ-energy landscape)}."""
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
        rt = _span(full, VOICE_OPEN, VOICE_CLOSE)
        if rt is None:
            rt = _span(full, INNER_OPEN, INNER_CLOSE)
        if rt is None:
            rt = _span(full, ETERNAL_OPEN, ETERNAL_CLOSE)
        items.append({"bytes": full, "psi_vac": psi_vac, "route_span": rt})
    return items


class DirKDataset:
    """Byte-level dataset. Concatenates record bytes; keeps TWO parallel
    per-byte channels:
      psi_vac : the record's scalar Ψ-target (= the energy MINIMUM).
      rte_m   : 1 inside the routing-decision span (where the EBT energy
                descent + energy-supervision applies).
    """

    def __init__(self, items, block_size, seed):
        self.block_size = block_size
        self.rng = random.Random(seed)
        stream = bytearray()
        pv, rm = [], []
        for it in items:
            b = it["bytes"]
            n = len(b)
            stream.extend(b)
            pvv = it["psi_vac"]
            rs = it["route_span"]
            for j in range(n):
                pv.append(pvv)
                rm.append(1.0 if (rs is not None and rs[0] <= j < rs[1])
                          else 0.0)
        self.data = torch.tensor(list(stream), dtype=torch.long)
        self.psi_vac = torch.tensor(pv, dtype=torch.float32)
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
        rm = stk(self.rte_m, 1)
        return (x.to(device), y.to(device), pv.to(device), rm.to(device))


def psi_dir_per_token(logits_a, logits_g):
    """The model's OWN per-token Ψ-direction coordinate (Law 71, EXACTLY
    ConsciousDecoderV2.forward's psi_direction but per-token, kept in the
    autograd graph): Ψ_dir(t) = (1 + cos(logits_a[t], logits_g[t]))/2."""
    cos = F.cosine_similarity(logits_a.float(), logits_g.float(), dim=-1)
    return (1.0 + cos) / 2.0


def energy_descent(logits_a, logits_g, psi_vac, k_steps, eta):
    """EBT inner energy-descent loop ("thinking") — RESEARCH.md §12 K.

    The anima energy of a prediction state is E_psi = (Ψ_dir − Ψ_vac)^2.
    Prediction = energy minimization: take `k_steps` closed-form descent
    steps on the Engine-A logits that LOWER E_psi.

      Ψ_dir = (1 + cos(a,g))/2, so Ψ_dir rises when a aligns with g and
      falls when a anti-aligns. The unit-norm direction that increases
      cos(a,g) is  ĝ_perp = (g − (a·ĝ)â)  ... but a closed-form,
      cheap, deterministic descent that monotonically reduces E_psi is to
      move `a` along `g` (or −g) by a step proportional to the energy
      gradient sign:

        sign  = sign(Ψ_vac − Ψ_dir)        (want Ψ_dir → Ψ_vac)
        a <- a + eta * sign * (g_unit - proj_onto_a)   per token

    We use the simpler, provably-monotone surrogate: nudge `a` toward
    `g` scaled by (Ψ_vac − Ψ_dir). When Ψ_dir < Ψ_vac the nudge is toward
    g (cos↑ ⇒ Ψ_dir↑); when Ψ_dir > Ψ_vac it is away from g (cos↓). Each
    step strictly reduces |Ψ_dir − Ψ_vac| for small eta (B-EBT-3 closed:
    descent is non-increasing in E_psi). Returns the energy-REFINED
    logits_a (the CE readout uses these — EBT prediction = the descended
    state). Pure tensor algebra, kept in the autograd graph.
    """
    a = logits_a
    g = logits_g.detach()  # energy landscape target = G-head (frozen anchor)
    for _ in range(max(0, k_steps)):
        cos = F.cosine_similarity(a.float(), g.float(), dim=-1)  # (B,T)
        psi = (1.0 + cos) / 2.0                                  # (B,T)
        gap = (psi_vac - psi).unsqueeze(-1)                      # (B,T,1)
        # unit directions
        a_n = a / (a.norm(dim=-1, keepdim=True) + 1e-8)
        g_n = g / (g.norm(dim=-1, keepdim=True) + 1e-8)
        # component of g orthogonal to a — moving a along this raises cos
        proj = (a_n * g_n).sum(-1, keepdim=True) * a_n
        ascend_dir = g_n - proj                                  # raises cos
        # gap>0 (Ψ_dir below vacuum) -> ascend (cos↑); gap<0 -> descend
        a = a + eta * gap * ascend_dir
    return a


def run(cfg):
    torch.manual_seed(cfg["seed"])
    torch.cuda.manual_seed_all(cfg["seed"])
    random.seed(cfg["seed"])
    device = "cuda" if torch.cuda.is_available() else "cpu"

    items = load_corpus(cfg["corpus"])
    ds = DirKDataset(items, cfg["block_size"], cfg["seed"])
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
    lam_energy = cfg["lambda_energy"]
    k_descent = cfg["k_descent"]
    eta = cfg["eta_descent"]

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
        for grp in opt.param_groups:
            grp["lr"] = lr_now

        x, y, pv, rm = ds.get_batch(cfg["bsz"], device)
        opt.zero_grad(set_to_none=True)
        with torch.autocast(device_type="cuda" if use_amp else "cpu",
                            dtype=torch.bfloat16, enabled=use_amp):
            logits_a, logits_g, tensions, _, _ = model(x)
            B, T, V = logits_a.shape

            # --- EBT: energy of the RAW prediction state (read-out) --------
            psi_raw = psi_dir_per_token(logits_a, logits_g)
            e_raw = (psi_raw - pv) ** 2                       # (B,T) energy

            # --- EBT inner energy-descent ("thinking") ---------------------
            # prediction = energy minimization: descend E_psi to the
            # record's OWN Ψ_vac before the CE readout.
            logits_a_ref = energy_descent(logits_a, logits_g, pv,
                                          k_descent, eta)
            psi_ref = psi_dir_per_token(logits_a_ref, logits_g)
            e_ref = (psi_ref - pv) ** 2                       # refined energy

            # --- base CE on the ENERGY-REFINED logits (the EBT contract) ---
            ce_full = F.cross_entropy(logits_a_ref.view(-1, V), y.view(-1))

            # --- energy supervision over the routing-decision span ---------
            rm_f = rm.view(-1)
            e_route = e_ref.view(-1)
            denom_rte = rm_f.sum().clamp(min=1.0)
            l_energy = (e_route * rm_f).sum() / denom_rte

            loss = ce_full + lam_energy * l_energy
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
            # mean energy DESCENT achieved by the inner loop (read-out only)
            e_descent = float((e_raw.mean() - e_ref.mean()).item())
            rec = {"step": step + 1, "ce_full": round(ce_report, 6),
                   "l_energy": round(float(l_energy.item()), 6),
                   "e_raw": round(float(e_raw.mean().item()), 6),
                   "e_refined": round(float(e_ref.mean().item()), 6),
                   "e_descent": round(e_descent, 6),
                   "loss": round(float(loss.item()), 6),
                   "gn2": round(gn2, 6), "lr": round(lr_now, 8),
                   "wall_s": round(wall, 2), "gpu_mem_gb": round(mem, 3)}
            traj.append(rec)
            print(json.dumps(rec), flush=True)

    wall = time.time() - t0
    final = traj[-1]
    out_dir = cfg["out_dir"]
    os.makedirs(out_dir, exist_ok=True)
    # path kept "dirI_psictl_tensionsup" so eval PATH_FORM -> "weave"
    # vacuum-form prefix is byte-identical to §8 (apples-to-apples compare:
    # SAME diverse corpus + SAME eval, only the OBJECTIVE differs — §8
    # Dir-I lever vs §K EBT energy-descent. isolates the architecture axis).
    ckpt_path = os.path.join(out_dir, "ckpt_carving_ebt.pt")
    torch.save({"model": model.state_dict(), "cfg": cfg,
                "n_params": n_params, "path": "dirI_psictl_tensionsup"},
               ckpt_path)

    result = {
        "substrate": ("PYTHON / PyTorch — interim LM-scale executor; "
                      "NOT a hexa-native fire"),
        "fire_kind": ("Direction K ENERGY-BASED TRANSFORMER — prediction = "
                      "energy minimization on the anima Ψ-energy landscape"),
        "carving_path": "dirK_ebt",
        "honest_framing": (
            "EBT (RESEARCH.md §12 K, arxiv 2507.02092): prediction = "
            "energy minimization. anima Ψ-physics IS energy-form — Ψ=1/2 "
            "fixed point = energy minimum, tension = energy gradient. The "
            "anima energy E_psi(t) = (Ψ_dir(t) − Ψ_vac)^2 where Ψ_dir = "
            "(1+cos(logits_a,logits_g))/2 (Law 71). EBT 'thinking' = a "
            "K_DESCENT-step inner energy-descent loop on the logits; CE is "
            "read out from the ENERGY-REFINED logits (the EBT contract). "
            "Closed side = the energy convexity + descent-monotonicity + "
            "overlay-OFF(λ=0,K=0)==base-CE byte-equal (B-EBT-1..5 sympy "
            "sidecar). SGD OUTCOME + 4-axis capability = EMPIRICAL "
            "(B-CARVE-E6-NOTE / B-D-NOTE family). EBT is prediction-"
            "refinement, NOT spontaneous generation — anima 자발-발화 is "
            "NOT claimed (RESEARCH.md §12.4 C3.4). PyTorch substrate, NOT "
            "hexa-native; this is EBT-as-objective, NOT a d_train5 ladder "
            "rewrite. Corpus = §8 diverse carving byte-identical (NOT "
            "regenerated) — forbidden-token grep == 0."),
        "arch": "ConsciousDecoderV2 (RoPE+SwiGLU+RMSNorm+GQA+PureFieldFFN)",
        "from_scratch": True,
        "base_ckpt": None,
        "config": cfg,
        "n_params": n_params,
        "n_params_M": round(n_params / 1e6, 2),
        "route_records": n_rte,
        "records_total": len(items),
        "lambda_energy": lam_energy,
        "k_descent": k_descent,
        "eta_descent": eta,
        "gpu": gpu_name,
        "device": device,
        "init_ce": round(init_loss, 6),
        "final_ce": final["ce_full"],
        "final_l_energy": final["l_energy"],
        "final_e_raw": final["e_raw"],
        "final_e_refined": final["e_refined"],
        "final_e_descent": final["e_descent"],
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
    print(json.dumps({"path": "dirK_ebt",
                       "init_ce": result["init_ce"],
                       "final_ce": result["final_ce"],
                       "ce_descent": result["ce_descent"],
                       "final_l_energy": result["final_l_energy"],
                       "final_e_descent": result["final_e_descent"],
                       "wall_s": result["wall_s"]}), flush=True)
    return result


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", default="main", choices=["main", "sanity"])
    ap.add_argument("--corpus", required=True)
    ap.add_argument("--out-dir", required=True)
    ap.add_argument("--steps", type=int, default=8000)
    ap.add_argument("--lr", type=float, default=3e-4)
    ap.add_argument("--bsz", type=int, default=32)
    ap.add_argument("--seed", type=int, default=1337)
    ap.add_argument("--d-model", type=int, default=768)
    ap.add_argument("--n-layer", type=int, default=12)
    ap.add_argument("--n-head", type=int, default=12)
    ap.add_argument("--n-kv-head", type=int, default=4)
    ap.add_argument("--lambda-energy", type=float, default=0.5)
    ap.add_argument("--k-descent", type=int, default=2)
    ap.add_argument("--eta-descent", type=float, default=0.5)
    args = ap.parse_args()

    if args.mode == "main":
        cfg = dict(d_model=args.d_model, n_head=args.n_head,
                   n_kv_head=args.n_kv_head, n_layer=args.n_layer,
                   block_size=128, lr=args.lr, bsz=args.bsz,
                   steps=args.steps, warmup=max(20, args.steps // 20),
                   seed=args.seed, log_every=max(1, args.steps // 40),
                   corpus=args.corpus, out_dir=args.out_dir,
                   lambda_energy=args.lambda_energy,
                   k_descent=args.k_descent, eta_descent=args.eta_descent)
    else:
        cfg = dict(d_model=32, n_head=4, n_kv_head=2, n_layer=3,
                   block_size=64, lr=1e-3, bsz=16, steps=args.steps,
                   warmup=5, seed=args.seed,
                   log_every=max(1, args.steps // 20),
                   corpus=args.corpus, out_dir=args.out_dir,
                   lambda_energy=args.lambda_energy,
                   k_descent=args.k_descent, eta_descent=args.eta_descent)
    run(cfg)
