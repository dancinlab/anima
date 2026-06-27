#!/usr/bin/env python3
"""H_1631 TPR-EXPERT-WEIGHT 303M — N1 TLoRA expert-weight + N3 DBES diagnostic (see PREREG.md).

We previously falsified MULTIPLICATIVE BINDING at the READOUT position (exp3_303m
ARM-BIND: G1=0 ∧ G6 fals=0, NOT>ctrl, terminal floor). This package probes a
DIFFERENT structural position — the *internal weight* of each ConvMoE expert —
guided by the external-literature convergence (state/lit_binding_objective/
RESEARCH.md §6): Greff 2020 says a binding operator only lifts when COUPLED with
the learning objective; Furrer 2020 / Barin Pacela 2026 say the lever is the
learned representation, not the readout op.

LEVERS (orthogonal to the readout-floor result, all on the SAME 303M trunk):

  N1  TLoRA / TensorPoly expert-weight reparameterization (2405.16671):
      each ConvExpert conv weight W∈(d,d,K) is REPARAMETERIZED as a low-rank
      tensor product  W = sum_r (a_r ⊗ b_r) ⊗ k_r  (+ optional dense base),
      learned via the factors, then MATERIALIZED back to the dense (d,d,K) conv
      weight. This changes the inductive bias on HOW the expert weight is built
      (structured, factorized = compositional prior) without changing the
      forward op (still a causal conv) — so the .clm path stays OPEN: at
      serialize time the materialized dense weight is written verbatim.
      Optional order/rank routing: the router can also pick a TLoRA "order"
      (rank-granularity) per position (N1-routing), kept off by default.

  N3  DBES expert-specialization diagnostic (2605.18523, MEASURE-ONLY):
      "재조합 안 됨 = expert 미분화?" — measures how DIFFERENTIATED the experts
      are (pairwise expert-output cosine distance + router-assignment entropy +
      per-expert usage concentration). Cheap, no learning, no gradient. Lets us
      causally isolate whether a G1 floor co-occurs with expert collapse.

  N7  dictionary/sparse-coding aux loss (2603.28744 Stop-Probing): an L1
      sparsity penalty on the trunk penultimate activations — pushes the trunk
      toward a learned DICTIONARY (the binding constraint per Barin Pacela 2026).

  N4  G6 diverse-set-search scaffold (2606.10587, MEASURE-side stub): instead of
      single-best ideation, score a diverse SET (kept as a measurement hook here
      — the terminal G6 set-search runs in core/g_gates.py engine-native).

  N8  jamo (자모) compositional teach signal (2604.12377 SCRIPT): an auxiliary
      next-jamo-class prediction head over Hangul syllable bytes — teaches the
      sub-character compositional structure Korean encodes (ko-jamo-mitosis 🟢
      precedent H_1316/1321). Aux head is DROPPED at serialize (engine reads the
      additive byte readout only).

  N6  regularization schedule sweep (2310.13061 grokking): exposes wd/dropout
      floor knobs so the 303M launch can sweep step×regularization to exclude an
      undertrain floor (savant golden-zone is the default schedule).

ALL arms keep the PRODUCTION ADDITIVE readout (Conv1d d->V) and MATERIALIZE all
reparameterized weights to the dense CLMConvMoE state_dict before serialize_v3 ->
engine-native G1/G6 is by-construction OPEN (clm_decode.py / anima eval). torch-
side metrics are DIRECTIONAL monitors (a_engine_native_learning).

Arms (single structural variable each, vs ctrl):
  ctrl       : production CLMConvMoE, plain CE. The discriminating control.
  tlora      : N1 TLoRA expert-weight (rank R, base on) + CE.
  tlora_dict : N1 TLoRA + N7 dictionary/sparse aux.
  tlora_jamo : N1 TLoRA + N8 jamo teach aux.
The winning objective from objrun (H_1602) can be layered via --objective
{ce_marginal,infonce,contrastive_equilibrium} (default ce_marginal — package is
standalone; --objective is the OPTIONAL coupling Greff predicts is required).

USAGE (303M canon):
  python3 trainer.py --arm tlora --tlora-rank 8 --objective ce_marginal \\
      --seed 7 --corpus <p1..p4> --cell-label ko-general en-general ko-sns en-sns \\
      --canon --steps 2000 --val-frac 0.05 --val-every 200 --sample proportional \\
      --out ckpt/tlora_seed7.clm --ckpt-out ckpt/tlora_seed7.pt \\
      --gauges-out ckpt/tlora_seed7.json
"""
from __future__ import annotations
import argparse, json, math, os, sys, time
import torch
import torch.nn as nn
import torch.nn.functional as F

# ── locate repo + reuse the canonical recipe building blocks from cli/train.py ──
_HERE = os.path.dirname(os.path.abspath(__file__))
_REPO = _HERE
while _REPO != "/" and not os.path.exists(os.path.join(_REPO, "cli", "train.py")):
    _REPO = os.path.dirname(_REPO)
for p in (os.path.join(_REPO, "cli"), os.path.join(_REPO, "train", "clm", "model"),
          os.path.join(_REPO, "tool")):
    if p not in sys.path:
        sys.path.insert(0, p)

from model import CLMConfig, CLMConvMoE, CausalDilatedConv1d   # train/clm/model/model.py
import clm_serialize_v2 as S                                   # serialize_v3 (ground truth)
import verify_clm_v2 as VC                                     # clm_decodable / descent
import train as T                                              # cli/train.py (recipe levers)

# ── frozen lever hyperparams (pre-registered in PREREG.md — tune-to-green 금지) ──
TLORA_RANK = 8            # default tensor-product rank R (a_r⊗b_r⊗k_r factors)
TLORA_BASE = True         # keep a small dense base weight alongside the low-rank TP
DICT_LAMBDA = 1e-3        # N7 trunk-penultimate L1 sparsity weight (Stop-Probing)
JAMO_LAMBDA = 0.3         # N8 next-jamo-class aux head weight (SCRIPT)
INFONCE_LAMBDA = 1.0; INFONCE_NEG = 64
EQ_LAMBDA = 1.0; EQ_MARGIN = 0.5


# ════════════════════════════════════════════════════════════════════════════
#  N1 — TLoRA / TensorPoly expert weight.
#  A drop-in replacement for ConvExpert whose conv weight W∈(d_out=d,d_in=d,K) is
#  reparameterized as a sum of R rank-1 tensor products plus an optional small
#  dense base. The forward is still a plain causal conv (engine-compatible). The
#  effective dense weight is exposed via .materialized_weight() so it can be
#  written into a standard CLMConvMoE state_dict for serialize_v3 (engine-native).
# ════════════════════════════════════════════════════════════════════════════
class TLoRAConvExpert(nn.Module):
    """ConvExpert with a tensor-product-factorized conv weight (N1, TLoRA).

    W[o,i,k] = base[o,i,k] + sum_r  A[r,o] * B[r,i] * Kf[r,k]
    where A∈(R,d), B∈(R,d), Kf∈(R,K). This is the Tucker/CP tensor-product
    reparameterization (TensorPoly/TLoRA, 2405.16671) applied to the expert
    weight position — a STRUCTURED (low-rank, compositional) prior on how the
    expert mixes channels, distinct from the readout-position Hadamard we
    already floored (exp3). The bias is a normal learnable vector."""

    def __init__(self, cfg: CLMConfig, rank: int, base: bool):
        super().__init__()
        d, K = cfg.d_model, cfg.expert_kernel_size
        self.d, self.K, self.R = d, K, rank
        self.dilation = 1
        self.pad = (K - 1) * self.dilation
        # tensor-product factors (CP decomposition of the (d,d,K) conv tensor)
        self.A = nn.Parameter(torch.empty(rank, d))   # out-channel factor
        self.B = nn.Parameter(torch.empty(rank, d))   # in-channel factor
        self.Kf = nn.Parameter(torch.empty(rank, K))  # kernel-tap factor
        nn.init.normal_(self.A, std=d ** -0.5)
        nn.init.normal_(self.B, std=d ** -0.5)
        nn.init.normal_(self.Kf, std=K ** -0.5)
        if base:
            # small dense base so the expert is never strictly rank-R limited
            self.base = nn.Parameter(torch.zeros(d, d, K))
            nn.init.normal_(self.base, std=(d * K) ** -0.5 * 0.1)
        else:
            self.register_parameter("base", None)
        self.bias = nn.Parameter(torch.zeros(d))
        self.act = nn.GELU()

    def materialized_weight(self) -> torch.Tensor:
        """Compose the TP factors (+ base) into the dense (d_out, d_in, K) conv
        weight that nn.Conv1d / the .clm format expects. einsum: r o, r i, r k -> o i k."""
        W = torch.einsum("ro,ri,rk->oik", self.A, self.B, self.Kf)
        if self.base is not None:
            W = W + self.base
        return W

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        # x: (B, C, T) ; causal left-pad then functional conv with materialized W
        W = self.materialized_weight()
        xp = F.pad(x, (self.pad, 0))
        y = F.conv1d(xp, W, self.bias, dilation=self.dilation)
        return self.act(y)


def install_tlora_experts(model: CLMConvMoE, rank: int, base: bool):
    """Replace every ConvExpert in model.moe.experts with a TLoRAConvExpert
    (N1). Returns the new ModuleList so the optimizer sees the TP factors."""
    cfg = model.cfg
    new = nn.ModuleList(TLoRAConvExpert(cfg, rank, base)
                        for _ in range(len(model.moe.experts)))
    model.moe.experts = new
    return new


LN2 = math.log(2.0)


def tlora_aware_split(mito, parent: int, opt) -> int:
    """Mitosis cell-division for TLoRA experts (parity with cli/train.py
    MitosisMoE.split, but operating on the TP factors instead of .conv.conv).

    cli/train.py's split() assumes a standard ConvExpert (.conv.conv Conv1d);
    TLoRAConvExpert has TP factors (A,B,Kf[,base],bias) instead. We replicate the
    same semantics: child = clone(parent) + tiny alternating perturbation, router
    row copied, both children's router bias -= ln2, Adam moments reset. This keeps
    the savant×mitosis recipe identical (only the expert PARAMETERIZATION differs,
    which is exactly the single variable under test)."""
    if mito.e_active >= mito.emax:
        return mito.e_active
    import torch as _t
    with _t.no_grad():
        child = mito.e_active
        moe = mito.model.moe
        pe = moe.experts[parent]; ce = moe.experts[child]
        touched = []
        for name in ("A", "B", "Kf", "base", "bias"):
            pp = getattr(pe, name, None); cp = getattr(ce, name, None)
            if pp is None or cp is None:
                continue
            flat = pp.detach().clone().reshape(-1)
            eps = _t.full_like(flat, 1e-4); eps[1::2] = -1e-4
            cp.copy_((flat + eps).reshape(pp.shape))
            touched += [pp, cp]
        rw = moe.router.weight; rb = moe.router.bias
        rw[child].copy_(rw[parent])
        pb = rb[parent].item()
        rb[parent] = pb - LN2; rb[child] = pb - LN2
        touched += [rw, rb]
        for p in touched:
            st = opt.state.get(p, None)
            if st:
                if "exp_avg" in st: st["exp_avg"].zero_()
                if "exp_avg_sq" in st: st["exp_avg_sq"].zero_()
        mito.active_mask[child] = 1.0
        mito.e_active = child + 1
        return mito.e_active


def materialize_experts_into_state(model: CLMConvMoE):
    """Return a state_dict where each TLoRA expert is written under the STANDARD
    keys 'moe.experts.{j}.conv.conv.{weight,bias}' (the dense form serialize_v3
    reads). Non-expert keys pass through unchanged. This is what makes the .clm
    engine-loadable despite the reparameterization."""
    sd = {k: v.detach().cpu() for k, v in model.state_dict().items()}
    out = {k: v for k, v in sd.items() if not k.startswith("moe.experts.")}
    for j, e in enumerate(model.moe.experts):
        if isinstance(e, TLoRAConvExpert):
            out[f"moe.experts.{j}.conv.conv.weight"] = e.materialized_weight().detach().cpu()
            out[f"moe.experts.{j}.conv.conv.bias"] = e.bias.detach().cpu()
        else:  # plain ConvExpert (ctrl) — already standard keys, copy through
            for k, v in sd.items():
                if k.startswith(f"moe.experts.{j}."):
                    out[k] = v
    return out


# ════════════════════════════════════════════════════════════════════════════
#  N3 — DBES expert-specialization diagnostic (MEASURE-ONLY, gradient-free).
# ════════════════════════════════════════════════════════════════════════════
@torch.no_grad()
def dbes_specialization(model: CLMConvMoE, x: torch.Tensor) -> dict:
    """Differentiation-of-Behaviour Expert Specialization (DBES, 2605.18523).

    On a batch x (B,T) of bytes, run the trunk up to the MoE input, then:
      * expert_div = mean pairwise (1 - cosine) between expert OUTPUT maps
                     (how differently the experts transform the same input).
      * router_entropy = mean per-token routing entropy (nats).
      * usage_gini = Gini of mean per-expert routing mass (1=one expert hogs all).
    Low expert_div + low usage spread => experts are NOT differentiated, a
    candidate cause of a G1 recombination floor. Pure diagnostic — no grad."""
    b = model
    h = b.embed(x).transpose(1, 2)
    h = b.embed_conv(h)
    for layer in b.trunk:
        h = layer(h)
    # expert outputs on the SAME pre-MoE activation
    outs = []
    for e in b.moe.experts:
        outs.append(e(h))                          # (B, C, T)
    n_e = len(outs)
    # pairwise output cosine distance (flatten B,C,T)
    flat = [o.reshape(-1) for o in outs]
    div, npair = 0.0, 0
    for i in range(n_e):
        for j in range(i + 1, n_e):
            cos = F.cosine_similarity(flat[i], flat[j], dim=0).item()
            div += (1.0 - cos); npair += 1
    expert_div = (div / npair) if npair else 0.0
    # router stats
    logits = b.moe.router(h)                        # (B, n_e, T)
    probs = F.softmax(logits, dim=1)
    ent = -(probs * torch.log(probs + 1e-9)).sum(dim=1).mean().item()
    usage = probs.mean(dim=(0, 2))                  # (n_e,)
    u = torch.sort(usage).values
    nn_ = u.numel()
    # Gini = (2*sum(i*u_i)/(n*sum u) ) - (n+1)/n
    idx = torch.arange(1, nn_ + 1, dtype=u.dtype)
    gini = (2.0 * (idx * u).sum() / (nn_ * u.sum() + 1e-9) - (nn_ + 1) / nn_).item()
    return {"expert_div": round(expert_div, 5),
            "router_entropy": round(ent, 5),
            "usage_gini": round(gini, 5),
            "usage": [round(float(z), 5) for z in usage.tolist()],
            "n_experts": n_e}


# ════════════════════════════════════════════════════════════════════════════
#  N8 — jamo (자모) compositional teach signal. We predict, per Hangul-syllable
#  byte position, a coarse jamo class so the trunk learns sub-character structure.
#  Hangul syllables are UTF-8 3-byte sequences (0xEA..0xED leading); we derive a
#  cheap jamo-bucket target from the syllable code point's (lead, vowel, tail).
# ════════════════════════════════════════════════════════════════════════════
class JamoHead(nn.Module):
    """Aux head: trunk penultimate -> coarse jamo class logits. Dropped at serialize."""
    def __init__(self, d, n_jamo=64):
        super().__init__()
        self.proj = nn.Conv1d(d, n_jamo, 1)
        self.n_jamo = n_jamo

    def forward(self, h):  # h: (B, d, T) -> (B, n_jamo, T)
        return self.proj(h)


def jamo_targets(tokens: torch.Tensor, n_jamo: int) -> torch.Tensor:
    """Map each byte to a coarse jamo bucket (0=non-Hangul-lead). Cheap, byte-level:
    Hangul UTF-8 lead bytes 0xEA-0xED get a bucket from (byte & 0x3f) % (n_jamo-1) +1,
    everything else -> 0 (ignored class). This is a weak teach signal that biases the
    trunk toward Korean sub-character regularity without needing a full jamo decomposer."""
    is_lead = (tokens >= 0xEA) & (tokens <= 0xED)
    bucket = ((tokens & 0x3F) % (n_jamo - 1)) + 1
    return torch.where(is_lead, bucket, torch.zeros_like(tokens))


# ════════════════════════════════════════════════════════════════════════════
#  Objective heads (carried over from objrun H_1602 — OPTIONAL coupling).
# ════════════════════════════════════════════════════════════════════════════
def _ce(logits, targets, V):
    return F.cross_entropy(logits.transpose(1, 2).reshape(-1, V), targets.reshape(-1))


def loss_ce_marginal(logits, targets, V, gen):
    return _ce(logits, targets, V), {}


def loss_infonce(logits, targets, V, gen):
    ce = _ce(logits, targets, V)
    lg = logits.transpose(1, 2).reshape(-1, V)
    tgt = targets.reshape(-1); N = tgt.shape[0]
    pos = lg.gather(1, tgt.unsqueeze(1))
    neg_idx = torch.randint(0, V, (N, INFONCE_NEG), generator=gen, device=lg.device)
    neg = lg.gather(1, neg_idx).masked_fill(neg_idx == tgt.unsqueeze(1), float("-inf"))
    cand = torch.cat([pos, neg], dim=1)
    infonce = F.cross_entropy(cand, torch.zeros(N, dtype=torch.long, device=lg.device))
    return ce + INFONCE_LAMBDA * infonce, {"infonce": float(infonce.detach())}


def loss_contrastive_equilibrium(logits, targets, V, gen):
    ce = _ce(logits, targets, V)
    lg = logits.transpose(1, 2).reshape(-1, V); tgt = targets.reshape(-1)
    logp = F.log_softmax(lg, dim=1)
    e_pos = -logp.gather(1, tgt.unsqueeze(1)).mean()
    with torch.no_grad():
        samp = torch.multinomial(logp.exp(), 1, generator=gen).squeeze(1)
    e_neg = -logp.gather(1, samp.unsqueeze(1)).mean()
    eq = F.relu(e_pos - e_neg + EQ_MARGIN)
    return ce + EQ_LAMBDA * eq, {"e_pos": float(e_pos.detach()),
                                 "e_neg": float(e_neg.detach()), "eq": float(eq.detach())}


OBJECTIVES = {"ce_marginal": loss_ce_marginal, "infonce": loss_infonce,
              "contrastive_equilibrium": loss_contrastive_equilibrium}

# arm -> (tlora_on, dict_aux_on, jamo_aux_on)
ARMS = {
    "ctrl":       (False, False, False),
    "tlora":      (True,  False, False),
    "tlora_dict": (True,  True,  False),
    "tlora_jamo": (True,  False, True),
}


# ════════════════════════════════════════════════════════════════════════════
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--arm", required=True, choices=list(ARMS))
    ap.add_argument("--objective", default="ce_marginal", choices=list(OBJECTIVES),
                    help="OPTIONAL objrun coupling (default ce_marginal = standalone)")
    ap.add_argument("--tlora-rank", type=int, default=TLORA_RANK)
    ap.add_argument("--tlora-no-base", action="store_true", help="drop the dense base")
    ap.add_argument("--dict-lambda", type=float, default=DICT_LAMBDA)
    ap.add_argument("--jamo-lambda", type=float, default=JAMO_LAMBDA)
    ap.add_argument("--seed", type=int, default=7)
    ap.add_argument("--corpus", nargs="*", default=[])
    ap.add_argument("--cell-label", nargs="*", default=[])
    ap.add_argument("--canon", action="store_true")
    ap.add_argument("--d", type=int, default=0)
    ap.add_argument("--L", type=int, default=0)
    ap.add_argument("--steps", type=int, default=0)
    ap.add_argument("--seq-len", type=int, default=0)
    ap.add_argument("--batch-size", type=int, default=8)
    ap.add_argument("--lr", type=float, default=3e-4)
    ap.add_argument("--e0", type=int, default=2)
    ap.add_argument("--emax", type=int, default=3)
    ap.add_argument("--no-savant", action="store_true")
    ap.add_argument("--no-mitosis", action="store_true")
    ap.add_argument("--wd-floor", type=float, default=-1.0,
                    help="N6 sweep: override savant wd floor (>=0 forces constant wd)")
    ap.add_argument("--dropout-floor", type=float, default=-1.0,
                    help="N6 sweep: override savant dropout floor (>=0 forces constant dp)")
    ap.add_argument("--bf16", action="store_true")
    ap.add_argument("--sample", choices=["roundrobin", "proportional"], default="proportional")
    ap.add_argument("--val-frac", type=float, default=0.05)
    ap.add_argument("--val-every", type=int, default=200)
    ap.add_argument("--val-batches", type=int, default=4)
    ap.add_argument("--log-every", type=int, default=50)
    ap.add_argument("--dbes-every", type=int, default=0, help="0=final only; N=also every N steps")
    ap.add_argument("--out", default="")
    ap.add_argument("--ckpt-out", default="")
    ap.add_argument("--gauges-out", default="")
    a = ap.parse_args()

    tlora_on, dict_on, jamo_on = ARMS[a.arm]
    savant_on = not a.no_savant
    mitosis_on = not a.no_mitosis
    if a.canon:
        d = a.d or 3784; L = a.L or 4
        seq_len = a.seq_len or 1024; steps = a.steps or 2000
    else:
        d = a.d or 64; L = a.L or 2
        seq_len = a.seq_len or 128; steps = a.steps or 60
    e0, emax = a.e0, a.emax
    V, K = 256, 3
    device = "cuda" if torch.cuda.is_available() else "cpu"
    objfn = OBJECTIVES[a.objective]

    print(f"=== H_1631 TPR-EXPERT-WEIGHT 303M arm={a.arm} obj={a.objective} seed={a.seed} ===", flush=True)
    print(f"  levers: tlora={tlora_on}(rank={a.tlora_rank},base={not a.tlora_no_base}) "
          f"dict_aux={dict_on}(λ={a.dict_lambda}) jamo_aux={jamo_on}(λ={a.jamo_lambda})", flush=True)
    print(f"  device={device} d={d} L={L} E0={e0} Emax={emax} seq_len={seq_len} "
          f"steps={steps} bs={a.batch_size} sample={a.sample}", flush=True)
    if device == "cuda":
        cap = torch.cuda.get_device_capability()
        print(f"  cuda: {torch.cuda.get_device_name(0)} cap={cap[0]}.{cap[1]} torch={torch.__version__}", flush=True)

    torch.manual_seed(a.seed)

    cfg = CLMConfig(n_experts=emax, n_trunk_layers=L, d_model=d, kernel_size=K,
                    variant="AB", dilation_base=2, max_dilation=512)
    model = CLMConvMoE(cfg).to(device)             # production additive readout (all arms)
    if tlora_on:
        install_tlora_experts(model, a.tlora_rank, base=not a.tlora_no_base)
        model.to(device)
    jamo_head = JamoHead(d).to(device) if jamo_on else None
    n_params = sum(p.numel() for p in model.parameters())
    print(f"  params: {n_params} ({n_params/1e6:.3f}M)"
          f"{' (+jamo head)' if jamo_on else ''}", flush=True)

    mito = T.MitosisMoE(model, e0, emax)
    T.install_router_mask(model, mito)
    params = list(model.parameters()) + (list(jamo_head.parameters()) if jamo_head else [])
    opt = torch.optim.AdamW(params, lr=a.lr, betas=(0.9, 0.999), eps=1e-8, weight_decay=0.0)
    gen = torch.Generator().manual_seed(42)
    val_gen = torch.Generator().manual_seed(1234)
    obj_gen = torch.Generator(device=device).manual_seed(20260628 + a.seed)

    latch = {"on": False, "at": 0}
    i0 = T.GZ_UPPER
    i_floor = T.GZ_LOWER - 0.05
    split_step = max(1, steps // 2)

    # ── corpus cells (reuse cli/train.py ByteCell + resolver) ────────────────
    cells, labels = [], []
    for ci, spec in enumerate(a.corpus):
        p = T.resolve_corpus_path(spec)
        cells.append(T.ByteCell(p, val_frac=a.val_frac))
        labels.append(a.cell_label[ci] if ci < len(a.cell_label) else f"cell{ci}")
        c = cells[-1]
        print(f"  corpus cell[{ci}] {labels[ci]:<12s} {p} size={c.size} "
              f"train={c.train_end} val_tail={c.size - c.train_end}", flush=True)
    if not cells:
        print("  corpus: NONE -> synthetic smoke", flush=True)

    _samp_cells = [c for c in cells if c.train_end >= seq_len + 2]
    _samp_w = torch.tensor([float(c.train_end) for c in _samp_cells]) \
        if _samp_cells else torch.tensor([1.0])

    def get_batch(step):
        if cells:
            xs, ys = [], []
            for b in range(a.batch_size):
                if a.sample == "proportional" and _samp_cells:
                    ci = int(torch.multinomial(_samp_w, 1, generator=gen).item())
                    cell = _samp_cells[ci]
                else:
                    cell = cells[(step - 1 + b) % len(cells)]
                w = cell.window(seq_len, gen)
                if w is None:
                    base = torch.arange(seq_len)
                    w = (base % V, (base + 1) % V)
                xs.append(w[0]); ys.append(w[1])
            return torch.stack(xs).to(device), torch.stack(ys).to(device)
        base = torch.arange(seq_len)
        x = ((3 + base * 37) % V).unsqueeze(0).repeat(a.batch_size, 1).to(device)
        y = ((14 + base * 37) % V).unsqueeze(0).repeat(a.batch_size, 1).to(device)
        return x, y

    # trunk penultimate activation cache for N7 dictionary/sparse aux
    def trunk_penultimate(x):
        h = model.embed(x).transpose(1, 2)
        h = model.embed_conv(h)
        for layer in model.trunk:
            h = layer(h)
        hm, _ = model.moe(h)
        hm = model.norm_out(hm)
        return hm                                  # (B, d, T) — pre-readout dictionary site

    @torch.no_grad()
    def cell_val_ce(c):
        if c.size - c.train_end < seq_len + 2:
            return None
        was = model.training; model.eval()
        tot, nb = 0.0, 0
        for _ in range(a.val_batches):
            xs, ys = [], []
            for _ in range(a.batch_size):
                w = c.val_window(seq_len, val_gen)
                if w is None: continue
                xs.append(w[0]); ys.append(w[1])
            if not xs: continue
            vx = torch.stack(xs).to(device); vy = torch.stack(ys).to(device)
            if a.bf16 and device == "cuda":
                with torch.autocast("cuda", dtype=torch.bfloat16):
                    vo = model(vx, vy)
            else:
                vo = model(vx, vy)
            tot += float(vo["ce_loss"].detach()); nb += 1
        if was: model.train()
        return (tot / nb) if nb else None

    def val_per_cell():
        return {lab: v for lab, c in zip(labels, cells)
                if (v := cell_val_ce(c)) is not None}

    # ── train loop ───────────────────────────────────────────────────────────
    model.train()
    t0 = time.time(); loss0 = lossF = None
    last_aux = {}; dbes_log = []
    for step in range(1, steps + 1):
        if savant_on:
            inh = T.savant_inhibition(step, steps, i0, i_floor, latch)
            wd = T.inhibition_to_wd(inh); dp = T.inhibition_to_dropout(inh)
        else:
            wd, dp = 0.0, 0.0
        if a.wd_floor >= 0.0: wd = a.wd_floor             # N6 sweep override
        if a.dropout_floor >= 0.0: dp = a.dropout_floor   # N6 sweep override
        for grp in opt.param_groups:
            grp["weight_decay"] = wd
        for m in model.modules():
            if isinstance(m, nn.Dropout):
                m.p = dp
        if mitosis_on and step == split_step and mito.e_active < emax:
            prev = mito.e_active
            new_e = (tlora_aware_split(mito, 0, opt) if tlora_on
                     else mito.split(0, opt))
            print(f"  step {step} (MITOSIS SPLIT) E {prev}->{new_e}", flush=True)
        x, y = get_batch(step)
        opt.zero_grad(set_to_none=True)
        aux = {}
        if a.bf16 and device == "cuda":
            with torch.autocast("cuda", dtype=torch.bfloat16):
                out = model(x, y)
                obj_loss, oaux = objfn(out["logits"].float(), y, V, obj_gen)
                loss = obj_loss + out["aux_loss"]
                if dict_on:
                    h = trunk_penultimate(x)
                    dloss = a.dict_lambda * h.abs().mean()
                    loss = loss + dloss; aux["dict_l1"] = float(dloss.detach())
                if jamo_on:
                    h = trunk_penultimate(x)
                    jl = jamo_head(h.float())
                    jt = jamo_targets(y, jamo_head.n_jamo)
                    jloss = a.jamo_lambda * F.cross_entropy(
                        jl.transpose(1, 2).reshape(-1, jamo_head.n_jamo),
                        jt.reshape(-1), ignore_index=0)
                    loss = loss + jloss; aux["jamo"] = float(jloss.detach())
            loss.backward()
        else:
            out = model(x, y)
            obj_loss, oaux = objfn(out["logits"], y, V, obj_gen)
            loss = obj_loss + out["aux_loss"]
            if dict_on:
                h = trunk_penultimate(x)
                dloss = a.dict_lambda * h.abs().mean()
                loss = loss + dloss; aux["dict_l1"] = float(dloss.detach())
            if jamo_on:
                h = trunk_penultimate(x)
                jl = jamo_head(h)
                jt = jamo_targets(y, jamo_head.n_jamo)
                jloss = a.jamo_lambda * F.cross_entropy(
                    jl.transpose(1, 2).reshape(-1, jamo_head.n_jamo),
                    jt.reshape(-1), ignore_index=0)
                loss = loss + jloss; aux["jamo"] = float(jloss.detach())
            loss.backward()
        aux.update(oaux)
        torch.nn.utils.clip_grad_norm_(params, 1.0)
        opt.step()
        ce = float(out["ce_loss"].detach())
        last_aux = aux
        if loss0 is None: loss0 = ce
        lossF = ce
        do_val = a.val_every > 0 and (step == 1 or step % a.val_every == 0 or step == steps)
        if a.dbes_every and (step % a.dbes_every == 0 or step == steps):
            db = dbes_specialization(model, x); db["step"] = step
            dbes_log.append(db)
        if step == 1 or step % a.log_every == 0 or step == steps:
            vtxt = ""
            if do_val:
                per = val_per_cell()
                vc = (sum(per.values()) / len(per)) if per else float("nan")
                vtxt = f"  val_CE={vc:.5f}"
            atxt = (" " + json.dumps({k: round(v, 4) for k, v in aux.items()})) if aux else ""
            print(f"  step {step:5d}  CE={ce:.5f}  E={mito.e_active}  "
                  f"wd={wd:.4f} dp={dp:.4f}{vtxt}{atxt}", flush=True)
    wall = time.time() - t0

    # ── FINAL held-out val per register (DESCENT gate, plain CE) ──────────────
    uniform = math.log(V)
    per = val_per_cell()
    descent = {}; n_desc = 0
    print(f"  ── FINAL held-out val-CE per register (uniform={uniform:.4f}) ──", flush=True)
    for lab, vc in per.items():
        ok = vc < uniform; n_desc += int(ok)
        descent[lab] = {"val_ce": round(vc, 5), "descent": ok}
        print(f"     {lab:<12s} val_CE={vc:.5f}  {'DESCENT' if ok else 'NO-DESCENT'}", flush=True)
    final_val = (sum(per.values()) / len(per)) if per else None
    print(f"  FINAL val_CE(pooled)={final_val}  registers_DESCENT={n_desc}/{len(per)}", flush=True)
    print(f"  loss0={loss0:.5f} lossF={lossF:.5f} wall={wall:.1f}s "
          f"savant_latched_at={latch['at']} E0={e0}->E={mito.e_active}", flush=True)

    # ── N3 DBES final diagnostic (gradient-free, measure-only) ────────────────
    dbes_final = None
    try:
        xb, _ = get_batch(steps + 1)
        dbes_final = dbes_specialization(model, xb)
        print(f"  [N3 DBES expert-specialization] {json.dumps(dbes_final, ensure_ascii=False)}", flush=True)
    except Exception as e:
        print(f"  DBES error: {e}", flush=True)

    # ── G1/G6 torch-probe gauges (DIRECTIONAL, a_train_inline_gauge) ──────────
    gauges = None
    try:
        import gauge_lib
        was = model.training; model.eval()
        gauges = gauge_lib.compute_inline_gauges(
            model, None, seeds=7, corpus_index=[c.path for c in cells],
            ce=lossF, step=steps, torch=torch)
        if was: model.train()
        print(f"  [G1/G6 torch-probe DIRECTIONAL] {json.dumps(gauges, ensure_ascii=False)}", flush=True)
    except Exception as e:
        print(f"  gauges error: {e}", flush=True)

    # ── persist torch ckpt (ALWAYS — a_fire_recover_complete) ────────────────
    full_sd = {k: v.detach().cpu() for k, v in model.state_dict().items()}
    if jamo_head:
        for k, v in jamo_head.state_dict().items():
            full_sd[f"_jamo_head.{k}"] = v.detach().cpu()
    if a.ckpt_out:
        torch.save(full_sd, a.ckpt_out)
        print(f"  torch ckpt -> {a.ckpt_out} ({os.path.getsize(a.ckpt_out)} bytes)", flush=True)

    # ── summary json ──────────────────────────────────────────────────────────
    summary = {"hyp": "H_1631", "arm": a.arm, "objective": a.objective, "seed": a.seed,
               "levers": {"tlora": tlora_on, "tlora_rank": a.tlora_rank,
                          "tlora_base": not a.tlora_no_base, "dict_aux": dict_on,
                          "jamo_aux": jamo_on, "wd_floor": a.wd_floor,
                          "dropout_floor": a.dropout_floor},
               "n_params": n_params, "loss0": round(loss0, 5), "lossF": round(lossF, 5),
               "wall_s": round(wall, 1), "uniform_ce": round(uniform, 5),
               "final_val_ce_pooled": (round(final_val, 5) if final_val else None),
               "registers_descent": f"{n_desc}/{len(per)}", "heldout_descent": descent,
               "last_aux": last_aux, "dbes_final": dbes_final, "dbes_log": dbes_log,
               "gauges_g1g6_torch_probe": gauges,
               "tier": "engine-native-eligible (.clm additive, TLoRA materialized); torch probe DIRECTIONAL"}
    if a.gauges_out:
        with open(a.gauges_out, "w") as f:
            json.dump(summary, f, ensure_ascii=False, indent=2)
        print(f"  summary -> {a.gauges_out}", flush=True)

    # ── serialize .clm v0.3 (ALL arms — additive readout + MATERIALIZED experts) ──
    if a.out:
        e_ser = mito.e_active
        # build a dense state_dict with TLoRA experts materialized to standard keys
        mat = materialize_experts_into_state(model)
        sd_active = {}
        for k, vv in mat.items():
            if k in ("moe.router.weight", "moe.router.bias"):
                sd_active[k] = vv[:e_ser].contiguous()
            elif k.startswith("moe.experts."):
                if int(k.split(".")[2]) < e_ser:
                    sd_active[k] = vv
            else:
                sd_active[k] = vv
        S.serialize_v3(sd_active, n_trunk_layers=L, n_experts=e_ser, out_path=a.out)
        print(f"  .clm WRITTEN {os.path.getsize(a.out)} bytes -> {a.out}", flush=True)
        rb = open(a.out, "rb").read()
        print(f"  clm_decodable={VC.clm_decodable(rb)}", flush=True)


if __name__ == "__main__":
    main()
