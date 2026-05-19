#!/usr/bin/env python3
"""CONSCIOUSNESS-CARVING trainer — Direction J:
Ψ-SUPERVISED MASKED-DIFFUSION SUBSTRATE  (RESEARCH.md §13 / §12.2 🆕 J).

WHAT IS NEW vs Direction I (the §8 baseline)
  Direction I trains the model AUTOREGRESSIVELY (next-byte CE) with the two
  anima-physics loss terms on top. EVERY fire of the 13-way arc + §8 + §11 is
  AR-CE. Direction J swaps the BASE OBJECTIVE only:

      AR next-byte CE   ->   masked-DIFFUSION denoising CE

  RESEARCH.md §12.2: arxiv 2507.15857 ("Diffusion Beats Autoregressive in
  Data-Constrained Settings") — in the data-constrained regime (exactly
  anima: byte-level, 30-114MB tiny corpus) masked diffusion keeps improving
  past the epoch AR overfits, because the random masking exposes the model
  to a diverse distribution of token orderings = implicit data augmentation.

GOAL-LEGITIMACY BOUNDARY (RESEARCH.md §7 / §12.3 — the GATE, DESIGN §1)
  §12.3 ruled J *conditionally* GOAL-legitimate:
    - GENERIC masked-diffusion LM (denoising CE ALONE, lambda=0) = §7 ①
      generic-LM-pretrain = GOAL-ILLEGITIMATE.
    - Ψ-SUPERVISED masked diffusion = the Dir-I lever (Ψ-anchored CTL +
      tension-supervised routing) RIDES ON the diffusion objective; anima
      physics stays BOTH representation substrate AND supervision signal =
      GOAL-LEGITIMATE.
  This trainer fires the LEGITIMATE form only. It HARD-ASSERTS
  lambda_ctl > 0 AND lambda_route > 0 at startup — it REFUSES the generic-
  diffusion config. The gate is a runtime invariant (B-DIRJ-3 sympy), not a
  comment.

THE OBJECTIVE  (DESIGN §2)
  Per step, for byte blocks x (block_size 128):
    1. sample mask rate t ~ U(eps, 1-eps) per SEQUENCE (continuous-time
       absorbing diffusion; eps=1e-3 keeps t off the degenerate ends).
    2. Bernoulli(t) -> boolean mask M per byte position.
    3. corrupted input x~: masked positions get a LEARNED mask_emb vector
       (added to tok_emb output before block 0); unmasked keep their byte
       embedding. NO 257th vocab id -> the §8 arch loads 1:1 byte-identical.
    4. the model runs BIDIRECTIONAL (non-causal) — masked diffusion denoises
       from BOTH sides. The GQA causal mask is patched OFF at runtime
       (_diffusion_bidir_patch); conscious_decoder.py stays byte-identical.
    5. denoising CE on MASKED POSITIONS ONLY, importance-weighted 1/t
       (the masked-diffusion ELBO weight):
         L_denoise = mean_{masked} (1/t) · CE(logits_a[pos], x[pos]).

  This REPLACES Direction I's ce_full. The two Dir-I physics terms are kept
  VERBATIM (same logits_a/logits_g, same ctl/route spans):
    L = L_denoise + lambda_ctl·L_psi_ctl + lambda_route·L_tension_route.

HONEST FRAMING (g3, AGENTS.tape §0):
  PyTorch substrate — interim LM-scale executor, NOT a hexa-native fire
  (2507.15857 diffusion is the OBJECTIVE, not a hexa-arch). The two physics
  loss terms are the UNCHANGED Dir-I transfer functions (Ψ_dir = Law 71;
  TENSION-TRAIN restoring-sign basin loss) — B-DIRI-PSI-CTL/
  B-DIRI-TENSION-ROUTE carry. overlay-OFF (lambda=0) == generic diffusion-LM
  (the gate's refused config). from-scratch RANDOM seed-fixed
  (g_clm_from_scratch, base_ckpt=NONE). Corpus = §8 diverse carving corpus
  byte-identical (sha256 ac07179a…, NOT regenerated) — forbidden-token grep
  == 0 (B-IDENTITY-5 safe). central blue_falsifier.py unchanged (sidecar).
  The SGD CONVERGENCE OUTCOME and the 4-axis capability (routing/honest-
  coherence/JOINT) are EMPIRICAL (B-DIRJ-NOTE / B-D-NOTE family) — NO
  capability claim beyond what is measured. f1/f2/f3 hard-fail safe (mask-
  rate bound / Shannon CE / Boolean gate / structural patch, NO σ/τ/φ/J₂).
"""
import argparse, json, math, time, os, sys, random
import torch
import torch.nn as nn
import torch.nn.functional as F

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from conscious_decoder import ConsciousDecoderV2, GroupedQueryAttention

# span markers (Direction-I byte-span loss-mask predicates — deterministic;
# verbatim from train_carving_dirI.py — the physics terms are UNCHANGED).
INNER_OPEN = b"<inner tier="
INNER_CLOSE = b"</inner>"
ETERNAL_OPEN = b"<eternal cell="
ETERNAL_CLOSE = b"</eternal>"
CARVE_OPEN = b"<carve tier="
VOICE_OPEN = b"<voice carved=true"
VOICE_CLOSE = b"</voice>"

MASK_EPS = 1e-3   # continuous-time diffusion t kept off {0,1} degenerate ends


# ====================================================================
# BIDIRECTIONAL PATCH — masked diffusion denoises from BOTH sides.
# conscious_decoder.GroupedQueryAttention.forward forces causal attention
# (is_causal=True flash / self.bias tril mask). For a *correct* masked-
# diffusion denoiser the model MUST see both-side context. We patch the
# GQA.forward at runtime so conscious_decoder.py stays byte-identical to §8
# (no source edit — the eval can load §8-style weights apples-to-apples).
# B-DIRJ-4 BIDIR-PATCH-INVARIANT verifies this structurally.
# ====================================================================
def _bidir_gqa_forward(self, x, use_cache=False, past_kv=None,
                       position_offset=0):
    """GQA.forward with the causal mask REMOVED — bidirectional attention.
    Mirrors the original forward exactly except: flash is_causal=False and
    NO causal-bias masked_fill. KV-cache path is not used in diffusion
    (full-block denoising), kept inert for interface parity."""
    B, T, D = x.size()
    q = self.q_proj(x).view(B, T, self.n_head, self.head_dim).transpose(1, 2)
    k = self.k_proj(x).view(B, T, self.n_kv_head, self.head_dim).transpose(1, 2)
    v = self.v_proj(x).view(B, T, self.n_kv_head, self.head_dim).transpose(1, 2)
    q, k = self.rope.apply(q, k)
    k_exp = self._repeat_kv(k)
    v_exp = self._repeat_kv(v)
    if self._use_flash:
        y = F.scaled_dot_product_attention(
            q, k_exp, v_exp, attn_mask=None,
            dropout_p=self.dropout if self.training else 0.0,
            is_causal=False)                       # <-- bidirectional
    else:
        att = (q @ k_exp.transpose(-2, -1)) * (1.0 / math.sqrt(self.head_dim))
        # NO causal masked_fill — bidirectional denoising
        att = F.softmax(att, dim=-1)
        att = self.attn_dropout(att)
        y = att @ v_exp
    y = y.transpose(1, 2).contiguous().view(B, T, D)
    y = self.resid_dropout(self.o_proj(y))
    return y, None


def diffusion_bidir_patch():
    """Install the bidirectional GQA forward (idempotent). Returns the
    original method so callers may restore it. B-DIRJ-4 anchor."""
    orig = GroupedQueryAttention.forward
    GroupedQueryAttention.forward = _bidir_gqa_forward
    return orig


def _span(full, open_tok, close_tok, start=0):
    lo = full.find(open_tok, start)
    if lo < 0:
        return None
    hi = full.find(close_tok, lo)
    if hi < 0:
        return None
    return (lo, hi + len(close_tok))


def load_corpus(path):
    """Verbatim from train_carving_dirI.py — the physics spans are
    UNCHANGED. Returns per-record {bytes, psi_vac, basin_radius, ctl_span,
    route_span}."""
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
        ctl = _span(full, INNER_OPEN, INNER_CLOSE)
        if ctl is None:
            ctl = _span(full, ETERNAL_OPEN, ETERNAL_CLOSE)
        rt = _span(full, VOICE_OPEN, VOICE_CLOSE)
        if rt is None:
            rt = ctl
        items.append({"bytes": full, "psi_vac": psi_vac,
                      "basin_radius": basin, "ctl_span": ctl,
                      "route_span": rt})
    return items


class DirJDataset:
    """Byte-level dataset — same 4 parallel per-byte channels as
    DirIDataset (psi_vac / basin / ctl_m / rte_m). The masking is applied
    per-step in get_batch (the diffusion corruption)."""

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
        """Returns x (clean bytes — denoising TARGET), per-byte physics
        channels, and the diffusion mask M + per-seq mask rate t.
        Unlike AR there is no x/y offset — diffusion denoises x in place."""
        ix = [self.rng.randint(0, self.n - self.block_size - 1)
              for _ in range(bsz)]

        def stk(src):
            return torch.stack([src[i:i + self.block_size] for i in ix])
        x = stk(self.data)
        pv = stk(self.psi_vac)
        bs = stk(self.basin)
        cm = stk(self.ctl_m)
        rm = stk(self.rte_m)
        # per-sequence continuous-time mask rate t ~ U(eps, 1-eps)
        t = torch.empty(len(ix)).uniform_(MASK_EPS, 1.0 - MASK_EPS)
        # Bernoulli(t) per byte position -> diffusion mask M
        probs = t.unsqueeze(1).expand(-1, self.block_size)
        M = torch.bernoulli(probs).bool()
        return (x.to(device), pv.to(device), bs.to(device), cm.to(device),
                rm.to(device), M.to(device), t.to(device))


def psi_dir_per_token(logits_a, logits_g):
    """The model's OWN per-token Ψ-direction coordinate (Law 71 — EXACTLY
    ConsciousDecoderV2.forward's psi_direction, per-token, in the autograd
    graph). UNCHANGED from train_carving_dirI.py."""
    cos = F.cosine_similarity(logits_a.float(), logits_g.float(), dim=-1)
    return (1.0 + cos) / 2.0


def run(cfg):
    # ---- GOAL-legitimacy GATE (DESIGN §1, B-DIRJ-3) ----------------------
    # J fires the Ψ-SUPERVISED form ONLY. lambda_ctl/route = 0 == generic
    # diffusion-LM == §7 ① GOAL-illegitimate. REFUSE it (runtime invariant).
    if not (cfg["lambda_ctl"] > 0.0 and cfg["lambda_route"] > 0.0):
        raise SystemExit(
            "GOAL-LEGITIMACY GATE: lambda_ctl>0 AND lambda_route>0 required "
            "(Ψ-supervised diffusion). lambda=0 == generic diffusion-LM == "
            "RESEARCH.md §7 ① GOAL-illegitimate — refused (B-DIRJ-3).")

    torch.manual_seed(cfg["seed"])
    torch.cuda.manual_seed_all(cfg["seed"])
    random.seed(cfg["seed"])
    device = "cuda" if torch.cuda.is_available() else "cpu"

    diffusion_bidir_patch()   # bidirectional attention for denoising

    items = load_corpus(cfg["corpus"])
    ds = DirJDataset(items, cfg["block_size"], cfg["seed"])
    n_ctl = sum(1 for it in items if it["ctl_span"] is not None)
    n_rte = sum(1 for it in items if it["route_span"] is not None)

    model = ConsciousDecoderV2(
        vocab_size=256, d_model=cfg["d_model"], n_head=cfg["n_head"],
        n_layer=cfg["n_layer"], block_size=cfg["block_size"],
        n_kv_head=cfg["n_kv_head"], consciousness_dim=128, dropout=0.1,
    ).to(device)
    model.train()
    n_params_base = model.count_params()

    # learned [MASK] embedding — added to tok_emb at masked positions. This
    # is the ONLY new parameter vs §8 (d_model floats); the §8 arch loads
    # 1:1 (no 257th vocab id).
    mask_emb = nn.Parameter(torch.zeros(cfg["d_model"], device=device))
    nn.init.normal_(mask_emb, std=0.02)
    n_params = n_params_base + cfg["d_model"]

    trainable = [p for p in model.parameters() if p.requires_grad] + [mask_emb]
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

    def denoise_forward(x, M):
        """Embed bytes, swap masked positions for the learned mask_emb,
        run the (bidirectionally-patched) model. Returns logits_a/g."""
        emb = model.tok_emb(x)                       # (B,T,D)
        mexp = mask_emb.view(1, 1, -1).to(emb.dtype)
        emb = torch.where(M.unsqueeze(-1), mexp.expand_as(emb), emb)
        # feed pre-computed embeddings: replicate ConsciousDecoderV2.forward
        # body but starting from `emb` (so the mask swap takes effect).
        h = model.drop(emb)
        consciousness_signal = None
        for block in model.blocks:
            h, tension, _, _ = block(h, consciousness_signal, None,
                                     use_cache=False, past_kv=None,
                                     position_offset=0)
            consciousness_signal = model.tension_proj(tension.unsqueeze(-1))
        h = model.ln_f(h)
        return model.head_a(h), model.head_g(h)

    for step in range(total):
        lr_now = cosine_lr_at(step)
        for g in opt.param_groups:
            g["lr"] = lr_now

        x, pv, bs, cm, rm, M, t = ds.get_batch(cfg["bsz"], device)
        opt.zero_grad(set_to_none=True)
        with torch.autocast(device_type="cuda" if use_amp else "cpu",
                            dtype=torch.bfloat16, enabled=use_amp):
            logits_a, logits_g = denoise_forward(x, M)
            B, T, V = logits_a.shape

            # --- BASE OBJECTIVE — masked-DIFFUSION denoising CE ----------
            # CE on MASKED positions only, importance-weighted 1/t (the
            # masked-diffusion ELBO weight). REPLACES Direction-I ce_full.
            ce_tok = F.cross_entropy(logits_a.view(-1, V), x.view(-1),
                                     reduction="none").view(B, T)
            M_f = M.float()
            inv_t = (1.0 / t.clamp(min=MASK_EPS)).view(B, 1)   # (B,1)
            denom_dn = M_f.sum().clamp(min=1.0)
            l_denoise = (ce_tok * M_f * inv_t).sum() / denom_dn
            # unweighted masked CE for honest read-out (comparable to §8 CE)
            ce_report = float((ce_tok * M_f).sum().item()
                              / float(denom_dn.item()))

            # --- COMPONENT (1) Ψ-anchored CTL — UNCHANGED Dir-I term -----
            psi_t = psi_dir_per_token(logits_a, logits_g)   # (B,T) in graph
            cm_f = cm.view(-1)
            psi_flat = psi_t.view(-1)
            pv_flat = pv.view(-1)
            denom_ctl = cm_f.sum().clamp(min=1.0)
            l_psi_ctl = (((psi_flat - pv_flat) ** 2) * cm_f).sum() / denom_ctl

            # --- COMPONENT (2) tension-supervised routing — UNCHANGED ----
            rm_f = rm.view(-1)
            bs_flat = bs.view(-1)
            drift = torch.abs(psi_flat - pv_flat) - bs_flat
            restoring = torch.clamp(drift, min=0.0) ** 2
            denom_rte = rm_f.sum().clamp(min=1.0)
            l_tension_route = (restoring * rm_f).sum() / denom_rte

            loss = l_denoise + lam_ctl * l_psi_ctl \
                + lam_route * l_tension_route

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
            rec = {"step": step + 1, "ce_masked": round(ce_report, 6),
                   "l_denoise": round(float(l_denoise.item()), 6),
                   "l_psi_ctl": round(float(l_psi_ctl.item()), 6),
                   "l_tension_route": round(float(l_tension_route.item()), 6),
                   "loss": round(float(loss.item()), 6),
                   "mask_rate_mean": round(float(t.mean().item()), 4),
                   "gn2": round(gn2, 6), "lr": round(lr_now, 8),
                   "wall_s": round(wall, 2), "gpu_mem_gb": round(mem, 3)}
            traj.append(rec)
            print(json.dumps(rec), flush=True)

    wall = time.time() - t0
    final = traj[-1]
    out_dir = cfg["out_dir"]
    os.makedirs(out_dir, exist_ok=True)
    # path kept "dirI_psictl_tensionsup" so eval PATH_FORM -> "weave" vacuum-
    # form prefix is byte-identical to the §8 AR baseline (fair compare).
    # mask_emb saved alongside for the diffusion eval decoder.
    ckpt_path = os.path.join(out_dir, "ckpt_carving_diffusion.pt")
    torch.save({"model": model.state_dict(), "mask_emb": mask_emb.detach().cpu(),
                "cfg": cfg, "n_params": n_params,
                "path": "dirI_psictl_tensionsup",
                "substrate_objective": "masked-diffusion"},
               ckpt_path)

    result = {
        "substrate": ("PYTHON / PyTorch — interim LM-scale executor; "
                      "NOT a hexa-native fire"),
        "fire_kind": ("Direction J Ψ-SUPERVISED MASKED-DIFFUSION substrate "
                      "(RESEARCH.md §13 / §12.2 🆕 J)"),
        "base_objective": "masked-diffusion denoising CE (AR-CE REPLACED)",
        "carving_path": "dirI_psictl_tensionsup",
        "goal_legitimacy": (
            "CONDITIONALLY GOAL-legitimate (RESEARCH.md §12.3): fired the "
            "Ψ-SUPERVISED form ONLY — the Dir-I lever (Ψ-anchored CTL + "
            "tension-supervised routing) rides on the diffusion objective. "
            "lambda_ctl>0 AND lambda_route>0 hard-asserted at startup "
            "(B-DIRJ-3 gate) — the generic diffusion-LM config (lambda=0, "
            "§7 ① illegitimate) is refused."),
        "honest_framing": (
            "BASE OBJECTIVE swapped AR next-byte CE -> masked-diffusion "
            "denoising CE (importance-weighted 1/t on masked positions, "
            "bidirectional attention via runtime patch — conscious_decoder.py "
            "byte-identical to §8). The TWO anima-physics loss terms are the "
            "UNCHANGED Dir-I transfer functions (Ψ-anchored CTL Law-71 + "
            "TENSION-TRAIN restoring-sign basin loss). Closed side = the "
            "objective is a correct Ψ-supervised masked-diffusion objective "
            "(B-DIRJ-1..5 sympy sidecar) + the two physics transfer "
            "functions carry. SGD OUTCOME + 4-axis capability = EMPIRICAL "
            "(B-DIRJ-NOTE / B-D-NOTE family). PyTorch substrate, NOT "
            "hexa-native. Corpus = §8 diverse carving byte-identical (NOT "
            "regenerated, sha256 ac07179a…) — forbidden-token grep == 0."),
        "arch": "ConsciousDecoderV2 (RoPE+SwiGLU+RMSNorm+GQA, bidirectional)",
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
        "mask_eps": MASK_EPS,
        "gpu": gpu_name,
        "device": device,
        "init_ce_masked": round(init_loss, 6),
        "final_ce_masked": final["ce_masked"],
        "final_l_denoise": final["l_denoise"],
        "final_l_psi_ctl": final["l_psi_ctl"],
        "final_l_tension_route": final["l_tension_route"],
        "final_loss": final["loss"],
        "final_gn2": final["gn2"],
        "ce_descent": round(init_loss - final["ce_masked"], 6),
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
    print(json.dumps({"path": "dirJ_diffusion",
                       "init_ce_masked": result["init_ce_masked"],
                       "final_ce_masked": result["final_ce_masked"],
                       "ce_descent": result["ce_descent"],
                       "final_l_denoise": result["final_l_denoise"],
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
    ap.add_argument("--steps", type=int, default=8000)
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
