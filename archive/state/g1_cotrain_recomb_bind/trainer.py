#!/usr/bin/env python3
"""
PREREG: co-trained LIVE bind op × recombination objective — 3-arm decisive experiment.

3 ARMS (matched trunk-init seed/data/steps — causal isolation):
  op_plaince : BindCLM + plain CE only  (= H_1818 bind arm; audio-neg control)
  obj_only   : CLMConvMoE (additive) + L_recomb aux only  (objective-only control)
  op_obj     : BindCLM + L_recomb  (★ decisive ★ — structure + objective)

DECISION TEST (PREREG FROZEN):
  (c) op_obj > (a) op_plaince AND (c) op_obj > (b) obj_only on G1 best_distinct,
  same 3 seeds {7, 4302, 4303} → "structure + objective together lift G1".

FROZEN BAR (tune-to-green forbidden, p7):
  G1: composed_distinct>=2 AND >max_single AND coherent, >=2/3 seeds.
  G6: dist>=5 AND fals>=1.
  LIFT: (c) strictly > (a) AND (c) strictly > (b) on G1 best_distinct / G6 fals.
  held-out: 4/4 register DESCENT (math.log mirror) — overfit => verdict invalid.
  G0: >=4/5 (>=4000 steps required, else INCONCLUSIVE-at-floor).

L_recomb (InfoNCE — PREREG §recomb-objective-정의):
  trunk penultimate x (B, d, T):
    z_a = x[:, :, T//3 - 1]  (concept A = context at 1/3 of sequence)
    z_b = x[:, :, 2*T//3 - 1] (concept B = context at 2/3 of sequence)
    z_c = x[:, :, T - 1]      (composite target = end-of-sequence)
  Pa, Pb, Pc: Conv1d(d, k, 1) projections
    g = Pa(z_a) * Pb(z_c) — Hadamard composite  (element-wise product)
  InfoNCE: F.cross_entropy(normalize(g) @ normalize(Pc(z_c)).T / tau, arange(B))
  For op_obj: Pa = Wa, Pb = Wb (shared bind readout projections); Pc is new.
  For obj_only: Pa, Pb, Pc are separate aux projections (discarded at serialize).
  Lambda_recomb = 0.1  (PREREG mid-range; single value to avoid sweep cost)
  Temperature tau = 0.1

total loss = CE_byte + aux_moe + lambda_bind * bind_ce + lambda_recomb * L_recomb
  op_plaince: lambda_bind=1, lambda_recomb=0
  obj_only:   lambda_bind=0, lambda_recomb=0.1
  op_obj:     lambda_bind=1, lambda_recomb=0.1

SERIALIZATION:
  op_plaince: serialize_v3_bind (CLMB retained, bind op LIVE at decode)
  obj_only:   serialize_v3 (additive, Pa/Pb/Pc aux discarded)
  op_obj:     serialize_v3_bind (CLMB retained; Pa=Wa/Pb=Wb are bind projections)

USAGE:
  python3 trainer.py --arm {op_plaince,obj_only,op_obj} --seed N \\
      --corpus <4 paths> --cell-label ko-general en-general ko-sns en-sns \\
      --canon --steps 4000 --val-frac 0.05 --val-every 200 --sample proportional \\
      --bf16 --out ckpt/<arm>_seed<N>.clm --ckpt-out ckpt/<arm>_seed<N>.pt \\
      --gauges-out ckpt/<arm>_seed<N>.json
"""
from __future__ import annotations
import argparse, json, math, os, sys, time
import torch
import torch.nn as nn
import torch.nn.functional as F

_HERE = os.path.dirname(os.path.abspath(__file__))
_REPO = _HERE
while _REPO != "/" and not os.path.exists(os.path.join(_REPO, "cli", "train.py")):
    _REPO = os.path.dirname(_REPO)
for p in (os.path.join(_REPO, "cli"), os.path.join(_REPO, "train", "clm", "model"),
          os.path.join(_REPO, "tool")):
    if p not in sys.path:
        sys.path.insert(0, p)

from model import CLMConfig, CLMConvMoE
import clm_serialize_v2 as S
import verify_clm_v2 as VC
import train as T

# ── hyperparameters ───────────────────────────────────────────────────────────
BIND_K = 512           # bind head bottleneck (matches EXP-3/H_1818 for fair comparison)
LAMBDA_RECOMB = 0.1    # PREREG fixed value (mid-range of 0.05–0.3 sweep)
TAU = 0.1              # InfoNCE temperature


# ════════════════════════════════════════════════════════════════════════════
# InfoNCE helper (PREREG §recomb-objective-정의)
# ════════════════════════════════════════════════════════════════════════════
def _infonce_recomb(x: torch.Tensor, Pa: nn.Conv1d, Pb: nn.Conv1d,
                    Pc: nn.Conv1d, tau: float = TAU) -> torch.Tensor:
    """Compute recombination InfoNCE loss from trunk output x (B, d, T).

    Concept A embedding: z_a = x[:, :, T//3 - 1]   (1/3 position)
    Concept B embedding: z_b = x[:, :, 2*T//3 - 1] (2/3 position)
    Composite target:    z_c = x[:, :, T - 1]       (end)

    Composite: g[b] = Pa(z_a[b]) * Pb(z_b[b])  (Hadamard product in k-space)
    Target:    c[b] = Pc(z_c[b])

    InfoNCE: g[b] should be closest to c[b] (positive) vs c[b'] where b' ≠ b (negatives).
    This forces the bind projections to learn factored representations where the
    PRODUCT of two context summaries predicts the future better than any cross-pair.

    The additive path cannot satisfy this if the joint information content of A×B is
    not expressible as A+B (the essence of why p7/composition matters here).
    """
    T_ = x.shape[2]
    B = x.shape[0]
    t1 = max(1, T_ // 3)
    t2 = max(t1 + 1, 2 * T_ // 3)

    # Extract context summaries at three positions
    z_a = x[:, :, t1 - 1]    # (B, d)
    z_b = x[:, :, t2 - 1]    # (B, d)
    z_c = x[:, :, T_ - 1]    # (B, d)

    # Project through Conv1d (kernel=1) — match BindCLM's projection style
    def _conv_proj(conv: nn.Conv1d, z: torch.Tensor) -> torch.Tensor:
        return conv(z.unsqueeze(-1)).squeeze(-1)  # (B, k)

    g = _conv_proj(Pa, z_a) * _conv_proj(Pb, z_b)   # (B, k) Hadamard composite
    c = _conv_proj(Pc, z_c)                           # (B, k) target

    # L2-normalize for numerically stable InfoNCE (avoids scale collapse)
    g = F.normalize(g, dim=1)
    c = F.normalize(c, dim=1)

    # scores[b, b'] = g[b] · c[b'] / tau
    scores = g @ c.T / tau    # (B, B)

    # InfoNCE: diagonal = positive pairs; off-diagonal = negatives
    # Use CrossEntropy with identity labels (row b → column b)
    labels = torch.arange(B, device=x.device)
    return F.cross_entropy(scores, labels)


# ════════════════════════════════════════════════════════════════════════════
# BindCLM — arm `op_plaince` (IDENTICAL to H_1818; plain CE only)
# ════════════════════════════════════════════════════════════════════════════
class BindCLM(nn.Module):
    """CLMConvMoE trunk + Hadamard bind readout (no recomb objective).

    This is IDENTICAL to H_1818's BindCLM — plain CE only.
    Serves as arm (a) op_plaince: the co-trained bind op without the
    recombination objective (audio-neg control for the decisive test).

    Serializes via serialize_v3_bind → CLMB section retained in .clm.
    clm_decode.py parses CLMB and executes bind op LIVE at decode.
    """

    def __init__(self, cfg: CLMConfig, k: int = BIND_K):
        super().__init__()
        d, V = cfg.d_model, cfg.vocab_size
        self.base = CLMConvMoE(cfg)
        self.base.readout = nn.Identity()
        self.cfg = cfg
        self.k = k
        self.Wa = nn.Conv1d(d, k, 1, bias=True)
        self.Wb = nn.Conv1d(d, k, 1, bias=True)
        self.Wo = nn.Conv1d(k, V, 1, bias=True)

    @property
    def moe(self):
        return self.base.moe

    def _trunk_out(self, tokens):
        b = self.base
        x = b.embed(tokens).transpose(1, 2)    # (B, d, T)
        x = b.embed_conv(x)
        for layer in b.trunk:
            x = layer(x)
        x, stats = b.moe(x)
        x = b.norm_out(x)                       # (B, d, T)
        return x, stats

    def forward(self, tokens, targets=None):
        x, stats = self._trunk_out(tokens)      # (B, d, T)
        u = self.Wa(x)                          # (B, k, T)
        v = self.Wb(x)                          # (B, k, T)
        g = u * v                               # Hadamard (B, k, T)
        logits = self.Wo(g)                     # (B, V, T)

        out = {"logits": logits, "usage": stats.usage,
               "aux_loss": stats.aux_loss, "routing_entropy": stats.entropy,
               "x": x}
        if targets is not None:
            ce = F.cross_entropy(
                logits.transpose(1, 2).reshape(-1, self.cfg.vocab_size),
                targets.reshape(-1))
            out["ce_loss"] = ce
            out["loss"] = ce + stats.aux_loss
        return out

    @torch.no_grad()
    def num_params(self) -> int:
        return sum(p.numel() for p in self.parameters())


# ════════════════════════════════════════════════════════════════════════════
# BindRecombCLM — arm `op_obj` (★ DECISIVE: bind op + L_recomb)
# ════════════════════════════════════════════════════════════════════════════
class BindRecombCLM(nn.Module):
    """BindCLM + InfoNCE recombination objective (arm op_obj — the decisive arm).

    Pa = Wa (shared with bind readout projection A)
    Pb = Wb (shared with bind readout projection B)
    Pc = separate Conv1d(d, k, 1) for target projection

    PREREG rationale: the bind op forces composition at inference time (Hadamard product);
    the recomb objective forces composition DURING TRAINING (InfoNCE on segment pairs).
    Together they should make it IMPOSSIBLE for the trunk to memorize without using
    the bilinear path, unlike plain CE which lets the trunk bypass the bind op (Task B).

    Serialization: serialize_v3_bind (CLMB retained; Wa=Pa/Wb=Pb are the bind weights).
    Pc is auxiliary (training only; not serialized).
    """

    def __init__(self, cfg: CLMConfig, k: int = BIND_K, lambda_recomb: float = LAMBDA_RECOMB):
        super().__init__()
        d, V = cfg.d_model, cfg.vocab_size
        self.base = CLMConvMoE(cfg)
        self.base.readout = nn.Identity()
        self.cfg = cfg
        self.k = k
        self.lambda_recomb = lambda_recomb
        self.Wa = nn.Conv1d(d, k, 1, bias=True)   # Pa = Wa (shared)
        self.Wb = nn.Conv1d(d, k, 1, bias=True)   # Pb = Wb (shared)
        self.Wo = nn.Conv1d(k, V, 1, bias=True)
        self.Pc = nn.Conv1d(d, k, 1, bias=True)   # target projection (aux, training only)

    @property
    def moe(self):
        return self.base.moe

    def _trunk_out(self, tokens):
        b = self.base
        x = b.embed(tokens).transpose(1, 2)
        x = b.embed_conv(x)
        for layer in b.trunk:
            x = layer(x)
        x, stats = b.moe(x)
        x = b.norm_out(x)
        return x, stats

    def forward(self, tokens, targets=None):
        x, stats = self._trunk_out(tokens)      # (B, d, T)
        u = self.Wa(x)                          # (B, k, T)
        v = self.Wb(x)                          # (B, k, T)
        g = u * v                               # Hadamard (B, k, T)
        logits = self.Wo(g)                     # (B, V, T)

        out = {"logits": logits, "usage": stats.usage,
               "aux_loss": stats.aux_loss, "routing_entropy": stats.entropy,
               "x": x}
        if targets is not None:
            ce = F.cross_entropy(
                logits.transpose(1, 2).reshape(-1, self.cfg.vocab_size),
                targets.reshape(-1))
            # L_recomb: InfoNCE on (z_a, z_b, z_c) segment triples
            l_recomb = _infonce_recomb(x, self.Wa, self.Wb, self.Pc)
            out["ce_loss"] = ce
            out["l_recomb"] = float(l_recomb.detach())
            out["loss"] = ce + stats.aux_loss + self.lambda_recomb * l_recomb
        return out

    @torch.no_grad()
    def num_params(self) -> int:
        return sum(p.numel() for p in self.parameters())


# ════════════════════════════════════════════════════════════════════════════
# ObjOnlyCLM — arm `obj_only` (recomb objective only, additive readout)
# ════════════════════════════════════════════════════════════════════════════
class ObjOnlyCLM(nn.Module):
    """Standard CLMConvMoE (additive readout) + L_recomb aux loss only (arm obj_only).

    Pa, Pb, Pc are separate aux Conv1d projections used ONLY during training for L_recomb.
    At serialize: standard serialize_v3 (additive .clm, Pa/Pb/Pc discarded — NOT in .clm).
    At decode: standard additive readout (same as ctrl arm).

    PREREG rationale: tests whether the recomb objective ALONE (without bind op at
    inference time) can lift G1. Expected to floor (per toy Task B: trunk will still
    memorize additively). Required arm for causal isolation of the decisive (c) vs (a),(b).
    """

    def __init__(self, cfg: CLMConfig, k: int = BIND_K, lambda_recomb: float = LAMBDA_RECOMB):
        super().__init__()
        d, V = cfg.d_model, cfg.vocab_size
        self.base = CLMConvMoE(cfg)
        self.cfg = cfg
        self.k = k
        self.lambda_recomb = lambda_recomb
        # Aux projections for L_recomb (training only, not serialized)
        self.Pa = nn.Conv1d(d, k, 1, bias=True)
        self.Pb = nn.Conv1d(d, k, 1, bias=True)
        self.Pc = nn.Conv1d(d, k, 1, bias=True)

    @property
    def moe(self):
        return self.base.moe

    def _trunk_out(self, tokens):
        b = self.base
        x = b.embed(tokens).transpose(1, 2)
        x = b.embed_conv(x)
        for layer in b.trunk:
            x = layer(x)
        x, stats = b.moe(x)
        x = b.norm_out(x)
        return x, stats

    def forward(self, tokens, targets=None):
        x, stats = self._trunk_out(tokens)      # (B, d, T)
        logits = self.base.readout(x)           # Conv1d(d, V, 1) additive readout

        out = {"logits": logits, "usage": stats.usage,
               "aux_loss": stats.aux_loss, "routing_entropy": stats.entropy,
               "x": x}
        if targets is not None:
            ce = F.cross_entropy(
                logits.transpose(1, 2).reshape(-1, self.cfg.vocab_size),
                targets.reshape(-1))
            # L_recomb: InfoNCE on (z_a, z_b, z_c) using aux projections
            l_recomb = _infonce_recomb(x, self.Pa, self.Pb, self.Pc)
            out["ce_loss"] = ce
            out["l_recomb"] = float(l_recomb.detach())
            out["loss"] = ce + stats.aux_loss + self.lambda_recomb * l_recomb
        return out

    @torch.no_grad()
    def num_params(self) -> int:
        return sum(p.numel() for p in self.parameters())


# ════════════════════════════════════════════════════════════════════════════
# Serialization helpers
# ════════════════════════════════════════════════════════════════════════════
def _prune_experts(sd, e_active):
    """Prune expert weights to the active count (post-mitosis)."""
    out = {}
    for k, v in sd.items():
        if k in ("moe.router.weight", "moe.router.bias"):
            out[k] = v[:e_active].contiguous()
        elif k.startswith("moe.experts."):
            if int(k.split(".")[2]) < e_active:
                out[k] = v
        else:
            out[k] = v
    return out


def _serialize_bind_arm(model, mito, L: int, out_path: str):
    """Serialize op_plaince or op_obj arm (both use serialize_v3_bind + CLMB)."""
    e_ser = mito.e_active
    sd = {k: v.detach().cpu() for k, v in model.state_dict().items()}
    # Normalize: strip 'base.' prefix so keys match CLMConvMoE layout
    norm = {}
    for k, v in sd.items():
        nk = k[5:] if k.startswith("base.") else k
        norm[nk] = v
    # Prune and exclude training-only Pc (only in BindRecombCLM)
    pruned = _prune_experts({k: v for k, v in norm.items() if not k.startswith("Pc")},
                            e_ser)
    S.serialize_v3_bind(pruned, n_trunk_layers=L, n_experts=e_ser,
                        readout_type=S.RO_BIND_HADAMARD, out_path=out_path)


def _serialize_ctrl_arm(model, mito, L: int, out_path: str):
    """Serialize obj_only arm (additive readout, Pa/Pb/Pc aux discarded)."""
    e_ser = mito.e_active
    sd = {k: v.detach().cpu() for k, v in model.state_dict().items()}
    # Only serialize the CLMConvMoE (base) weights; discard Pa/Pb/Pc aux
    norm = {}
    for k, v in sd.items():
        if k.startswith("Pa.") or k.startswith("Pb.") or k.startswith("Pc."):
            continue  # aux projections — discard
        nk = k[5:] if k.startswith("base.") else k
        norm[nk] = v
    pruned = _prune_experts(norm, e_ser)
    S.serialize_v3(pruned, n_trunk_layers=L, n_experts=e_ser, out_path=out_path)


# ════════════════════════════════════════════════════════════════════════════
# Training loop
# ════════════════════════════════════════════════════════════════════════════
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--arm", required=True, choices=["op_plaince", "obj_only", "op_obj"])
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
    ap.add_argument("--k", type=int, default=BIND_K)
    ap.add_argument("--lambda-recomb", type=float, default=LAMBDA_RECOMB)
    ap.add_argument("--e0", type=int, default=2)
    ap.add_argument("--emax", type=int, default=3)
    ap.add_argument("--no-savant", action="store_true")
    ap.add_argument("--no-mitosis", action="store_true")
    ap.add_argument("--bf16", action="store_true")
    ap.add_argument("--sample", choices=["roundrobin", "proportional"],
                    default="proportional")
    ap.add_argument("--val-frac", type=float, default=0.05)
    ap.add_argument("--val-every", type=int, default=200)
    ap.add_argument("--val-batches", type=int, default=4)
    ap.add_argument("--log-every", type=int, default=100)
    ap.add_argument("--out", default="", help=".clm output path")
    ap.add_argument("--ckpt-out", default="", help="torch .pt path (a_fire_recover_complete)")
    ap.add_argument("--gauges-out", default="", help="summary json path")
    a = ap.parse_args()

    savant_on = not a.no_savant
    mitosis_on = not a.no_mitosis
    if a.canon:
        d = a.d or 3784; L = a.L or 4
        seq_len = a.seq_len or 1024; steps = a.steps or 4000  # >=4000 per PREREG
    else:
        d = a.d or 64; L = a.L or 2
        seq_len = a.seq_len or 128; steps = a.steps or 60
    e0, emax = a.e0, a.emax
    k = a.k
    lambda_recomb = a.lambda_recomb
    V, K = 256, 3
    device = "cuda" if torch.cuda.is_available() else "cpu"

    print(f"=== RECOMB-BIND arm={a.arm} seed={a.seed} "
          f"lambda_recomb={lambda_recomb} ===", flush=True)
    print(f"  device={device} d={d} L={L} E0={e0} Emax={emax} k={k} "
          f"seq_len={seq_len} steps={steps} bs={a.batch_size} sample={a.sample}",
          flush=True)
    if device == "cuda":
        cap = torch.cuda.get_device_capability()
        print(f"  cuda: {torch.cuda.get_device_name(0)} cap={cap[0]}.{cap[1]} "
              f"torch={torch.__version__}", flush=True)

    torch.manual_seed(a.seed)
    cfg = CLMConfig(n_experts=emax, n_trunk_layers=L, d_model=d, kernel_size=K,
                    variant="AB", dilation_base=2, max_dilation=512)

    # Build model per arm
    if a.arm == "op_plaince":
        model = BindCLM(cfg, k=k).to(device)
        core = model.base
    elif a.arm == "obj_only":
        model = ObjOnlyCLM(cfg, k=k, lambda_recomb=lambda_recomb).to(device)
        core = model.base
    else:  # op_obj
        model = BindRecombCLM(cfg, k=k, lambda_recomb=lambda_recomb).to(device)
        core = model.base

    n_params = sum(p.numel() for p in model.parameters())
    print(f"  params: {n_params:,} ({n_params / 1e6:.3f}M)  arm={a.arm}", flush=True)

    mito = T.MitosisMoE(core, e0, emax)
    T.install_router_mask(core, mito)
    opt = torch.optim.AdamW(model.parameters(), lr=a.lr, betas=(0.9, 0.999),
                            eps=1e-8, weight_decay=0.0)
    gen = torch.Generator().manual_seed(42)      # DATA RNG: shared across arms (matched)
    val_gen = torch.Generator().manual_seed(1234)

    latch = {"on": False, "at": 0}
    i0 = T.GZ_UPPER
    i_floor = T.GZ_LOWER - 0.05
    split_step = max(1, steps // 2)

    cells, labels = [], []
    for ci, spec in enumerate(a.corpus):
        p = T.resolve_corpus_path(spec)
        cells.append(T.ByteCell(p, val_frac=a.val_frac))
        labels.append(a.cell_label[ci] if ci < len(a.cell_label) else f"cell{ci}")
        c = cells[-1]
        print(f"  corpus cell[{ci}] {labels[ci]:<12s} {p} "
              f"size={c.size} train={c.train_end} val={c.size - c.train_end}", flush=True)
    if not cells:
        print("  corpus: NONE -> synthetic smoke", flush=True)

    _samp_cells = [c for c in cells if c.train_end >= seq_len + 2]
    _samp_w = (torch.tensor([float(c.train_end) for c in _samp_cells])
               if _samp_cells else torch.tensor([1.0]))

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

    # ── training loop ──────────────────────────────────────────────────────
    model.train()
    t0 = time.time(); loss0 = lossF = None; recomb_sum = 0.0; recomb_n = 0
    for step in range(1, steps + 1):
        if savant_on:
            inh = T.savant_inhibition(step, steps, i0, i_floor, latch)
            wd = T.inhibition_to_wd(inh); dp = T.inhibition_to_dropout(inh)
        else:
            wd, dp = 0.0, 0.0
        for grp in opt.param_groups:
            grp["weight_decay"] = wd
        for m in model.modules():
            if isinstance(m, nn.Dropout):
                m.p = dp
        if mitosis_on and step == split_step and mito.e_active < emax:
            prev = mito.e_active; new_e = mito.split(0, opt)
            print(f"  step {step} (MITOSIS SPLIT) E {prev}->{new_e}", flush=True)
        x, y = get_batch(step)
        opt.zero_grad(set_to_none=True)
        if a.bf16 and device == "cuda":
            with torch.autocast("cuda", dtype=torch.bfloat16):
                out = model(x, y); loss = out["loss"]
            loss.backward()
        else:
            out = model(x, y); loss = out["loss"]; loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        opt.step()
        ce = float(out["ce_loss"].detach())
        if "l_recomb" in out:
            recomb_sum += out["l_recomb"]; recomb_n += 1
        if loss0 is None: loss0 = ce
        lossF = ce

        do_val = a.val_every > 0 and (step == 1 or step % a.val_every == 0
                                       or step == steps)
        if step == 1 or step % a.log_every == 0 or step == steps:
            vtxt = ""
            if do_val:
                per = val_per_cell()
                vc = (sum(per.values()) / len(per)) if per else float("nan")
                vtxt = f"  val_CE={vc:.5f}"
            recomb_txt = (f"  l_recomb={recomb_sum/recomb_n:.5f}" if recomb_n else "")
            print(f"  step {step:5d}  CE={ce:.5f}  E={mito.e_active}  "
                  f"wd={wd:.4f} dp={dp:.4f}{vtxt}{recomb_txt}", flush=True)
    wall = time.time() - t0

    # ── FINAL held-out val per register (H_1579 DESCENT gate, math.log mirror) ──
    uniform = math.log(V)
    per = val_per_cell()
    descent = {}; n_desc = 0
    print(f"  ── FINAL held-out val-CE (uniform={uniform:.4f}) ──", flush=True)
    for lab, vc in per.items():
        ok = vc < uniform; n_desc += int(ok)
        descent[lab] = {"val_ce": round(vc, 5), "descent": ok}
        print(f"     {lab:<12s} val_CE={vc:.5f}  {'DESCENT' if ok else 'NO-DESCENT'}",
              flush=True)
    final_val = (sum(per.values()) / len(per)) if per else None
    print(f"  FINAL val_CE(pooled)={final_val}  registers_DESCENT={n_desc}/{len(per)}",
          flush=True)
    print(f"  loss0={loss0:.5f} lossF={lossF:.5f} wall={wall:.1f}s "
          f"savant_latched_at={latch['at']} E0={e0}->E={mito.e_active}", flush=True)
    if recomb_n:
        print(f"  mean_l_recomb={recomb_sum/recomb_n:.5f} "
              f"lambda_recomb={lambda_recomb}", flush=True)

    # ── persist torch ckpt (ALWAYS — a_fire_recover_complete) ────────────────
    sd_full = {k: v.detach().cpu() for k, v in model.state_dict().items()}
    if a.ckpt_out:
        torch.save(sd_full, a.ckpt_out)
        print(f"  torch ckpt -> {a.ckpt_out} ({os.path.getsize(a.ckpt_out)} bytes)",
              flush=True)

    summary = {
        "arm": a.arm, "seed": a.seed, "n_params": n_params, "k": k,
        "lambda_recomb": lambda_recomb, "tau": TAU,
        "loss0": round(loss0, 5), "lossF": round(lossF, 5),
        "wall_s": round(wall, 1), "uniform_ce": round(uniform, 5),
        "final_val_ce_pooled": (round(final_val, 5) if final_val else None),
        "registers_descent": f"{n_desc}/{len(per)}",
        "heldout_descent": descent,
        "mean_l_recomb": round(recomb_sum / recomb_n, 5) if recomb_n else None,
        "tier": (
            "op_plaince: bind LIVE at decode (CLMB), no recomb objective" if a.arm == "op_plaince"
            else "obj_only: additive decode, recomb objective during training only" if a.arm == "obj_only"
            else "op_obj: bind LIVE at decode (CLMB) + recomb objective (DECISIVE ARM)"
        )
    }
    if a.gauges_out:
        with open(a.gauges_out, "w") as f:
            json.dump(summary, f, ensure_ascii=False, indent=2)
        print(f"  summary -> {a.gauges_out}", flush=True)

    # ── serialize .clm + DESCENT gate (a_clm_gen_pipeline) ──────────────────
    if a.out:
        if a.arm == "op_plaince" or a.arm == "op_obj":
            _serialize_bind_arm(model, mito, L, a.out)
            print(f"  .clm (CLMB bind) WRITTEN {os.path.getsize(a.out)} bytes -> {a.out}",
                  flush=True)
        else:
            _serialize_ctrl_arm(model, mito, L, a.out)
            print(f"  .clm (additive) WRITTEN {os.path.getsize(a.out)} bytes -> {a.out}",
                  flush=True)
        rb = open(a.out, "rb").read()
        decodable = VC.clm_decodable(rb)
        print(f"  clm_decodable={decodable}", flush=True)
        # Descent gate: math.log mirror (NOT engine CE — dt_ln bug, H_1579)
        if n_desc > 0 and cells:
            try:
                heldout_path = cells[0].path   # ko-general held-out
                r = VC.descent_gate(a.out, heldout_path)
                print(f"  verify_descent_gate={r}", flush=True)
            except Exception as e:
                print(f"  verify_descent_gate error: {e}", flush=True)


if __name__ == "__main__":
    main()
