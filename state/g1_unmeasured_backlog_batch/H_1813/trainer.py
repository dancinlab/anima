#!/usr/bin/env python3
"""H_1813 TPR-EXPERT-WEIGHT 303M — NON-NEGOTIABLE recomb-objective baked.

POSITION HYPOTHESIS: binding belongs in expert WEIGHT space (not readout).
We already floored MULTIPLICATIVE BINDING at the READOUT position (EXP-3).
This package probes a DIFFERENT structural position: the internal weight of
each ConvMoE expert reparameterized via TLoRA (TensorPoly, 2405.16671).

KEY LESSON BAKED (non-negotiable per session spec):
  TPR-weight ALONE will floor like every op-alone (toy Task B proof).
  Therefore L_recomb is REQUIRED on BOTH arms — ctrl and tlora — so that the
  only variable between arms is TPR factorization in the expert weight.

ARMS (single variable: expert weight structure):
  ctrl  : production CLMConvMoE expert weight + recomb-objective
  tlora : TLoRA expert weight (rank R, base on) + recomb-objective

RECOMB-OBJECTIVE (L_recomb, per spec):
  Two-concept composite CE — for each batch pair (i, j=derangement(i)):
    composite_x[i] = cat(x[i, :T//2], x[j, T//2:])
    composite_y[i] = cat(y[i, :T//2], y[j, T//2:])
  L_recomb = CE(model(composite_x, composite_y))  [forces generalization to
  novel compositions; positive=genuine composite; negatives=all other pairings].
  total = next_byte_CE + aux_moe + lambda_recomb * L_recomb

FIXED SPEC (≥4000 steps, G0 PASS required, held-out 4/4 DESCENT gate,
seeds {7,4302,4303}, ctrl vs tlora matched trunk-init+seed+data).
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

from model import CLMConfig, CLMConvMoE   # train/clm/model/model.py
import clm_serialize_v2 as S             # serialize_v3
import verify_clm_v2 as VC               # clm_decodable / descent
import train as T                        # cli/train.py (recipe levers)

# ── frozen hyperparams (pre-registered, tune-to-green 금지) ──────────────────
TLORA_RANK   = 8            # CP decomposition rank for TLoRA expert weight
TLORA_BASE   = True         # keep small dense base alongside low-rank TP
RECOMB_LAMBDA = 0.10        # λ_recomb default (L_recomb weight)

LN2 = math.log(2.0)


# ════════════════════════════════════════════════════════════════════════════
#  N1 — TLoRA / TensorPoly expert weight (same impl as 1631_tpr_expert_weight)
#  W[o,i,k] = base[o,i,k] + sum_r  A[r,o] * B[r,i] * Kf[r,k]
#  Materialized to dense at serialize → engine-native by-construction.
# ════════════════════════════════════════════════════════════════════════════
class TLoRAConvExpert(nn.Module):
    def __init__(self, cfg: CLMConfig, rank: int, base: bool):
        super().__init__()
        d, K = cfg.d_model, cfg.expert_kernel_size
        self.d, self.K, self.R = d, K, rank
        self.dilation = 1
        self.pad = (K - 1) * self.dilation
        self.A  = nn.Parameter(torch.empty(rank, d))
        self.B  = nn.Parameter(torch.empty(rank, d))
        self.Kf = nn.Parameter(torch.empty(rank, K))
        nn.init.normal_(self.A,  std=d ** -0.5)
        nn.init.normal_(self.B,  std=d ** -0.5)
        nn.init.normal_(self.Kf, std=K ** -0.5)
        if base:
            self.base = nn.Parameter(torch.zeros(d, d, K))
            nn.init.normal_(self.base, std=(d * K) ** -0.5 * 0.1)
        else:
            self.register_parameter("base", None)
        self.bias = nn.Parameter(torch.zeros(d))
        self.act  = nn.GELU()

    def materialized_weight(self) -> torch.Tensor:
        W = torch.einsum("ro,ri,rk->oik", self.A, self.B, self.Kf)
        if self.base is not None:
            W = W + self.base
        return W

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        W  = self.materialized_weight()
        xp = F.pad(x, (self.pad, 0))
        y  = F.conv1d(xp, W, self.bias, dilation=self.dilation)
        return self.act(y)


def install_tlora_experts(model: CLMConvMoE, rank: int, base: bool):
    cfg = model.cfg
    new = nn.ModuleList(TLoRAConvExpert(cfg, rank, base)
                        for _ in range(len(model.moe.experts)))
    model.moe.experts = new
    return new


def tlora_aware_split(mito, parent: int, opt) -> int:
    if mito.e_active >= mito.emax:
        return mito.e_active
    with torch.no_grad():
        child = mito.e_active
        moe   = mito.model.moe
        pe = moe.experts[parent]; ce = moe.experts[child]
        touched = []
        for name in ("A", "B", "Kf", "base", "bias"):
            pp = getattr(pe, name, None); cp = getattr(ce, name, None)
            if pp is None or cp is None: continue
            flat = pp.detach().clone().reshape(-1)
            eps  = torch.full_like(flat, 1e-4); eps[1::2] = -1e-4
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
                if "exp_avg"    in st: st["exp_avg"].zero_()
                if "exp_avg_sq" in st: st["exp_avg_sq"].zero_()
        mito.active_mask[child] = 1.0
        mito.e_active = child + 1
        return mito.e_active


def materialize_experts_into_state(model: CLMConvMoE):
    """Dense state_dict for serialize_v3 — TLoRA experts materialized to standard keys."""
    sd  = {k: v.detach().cpu() for k, v in model.state_dict().items()}
    out = {k: v for k, v in sd.items() if not k.startswith("moe.experts.")}
    for j, e in enumerate(model.moe.experts):
        if isinstance(e, TLoRAConvExpert):
            out[f"moe.experts.{j}.conv.conv.weight"] = e.materialized_weight().detach().cpu()
            out[f"moe.experts.{j}.conv.conv.bias"]   = e.bias.detach().cpu()
        else:
            for k, v in sd.items():
                if k.startswith(f"moe.experts.{j}."):
                    out[k] = v
    return out


# ════════════════════════════════════════════════════════════════════════════
#  L_RECOMB — two-concept composite CE (NON-NEGOTIABLE per session spec)
#
#  For each sample i in batch B, pair with j = (i + B//2) % B (derangement).
#  Composite sequence: first half from sample i, second half from sample j.
#  L_recomb = CE(model(composite_x), composite_y).
#
#  Forces the model to generalize to novel cross-concept compositions that
#  neither "leg" alone predicts. The TLoRA expert weight's structured inductive
#  bias (low-rank tensor product = compositional prior) should help here where
#  a plain dense expert cannot.
# ════════════════════════════════════════════════════════════════════════════
def recomb_loss(model: CLMConvMoE, x: torch.Tensor, y: torch.Tensor,
                lambda_r: float) -> tuple[torch.Tensor, dict]:
    B, T = x.shape
    half  = T // 2
    shift = max(1, B // 2)
    j     = (torch.arange(B, device=x.device) + shift) % B
    cx    = torch.cat([x[:, :half],  x[j, half:]], dim=1)
    cy    = torch.cat([y[:, :half],  y[j, half:]], dim=1)
    out   = model(cx, cy)
    rl    = out["ce_loss"]
    return lambda_r * rl, {"recomb_ce": round(float(rl.detach()), 5)}


# ════════════════════════════════════════════════════════════════════════════
#  N3 DBES — expert-specialization diagnostic (measure-only, no grad)
# ════════════════════════════════════════════════════════════════════════════
@torch.no_grad()
def dbes_specialization(model: CLMConvMoE, x: torch.Tensor) -> dict:
    b  = model
    h  = b.embed(x).transpose(1, 2)
    h  = b.embed_conv(h)
    for layer in b.trunk:
        h = layer(h)
    outs = [e(h) for e in b.moe.experts]
    n_e  = len(outs)
    flat = [o.reshape(-1) for o in outs]
    div, npair = 0.0, 0
    for i in range(n_e):
        for j in range(i + 1, n_e):
            cos  = F.cosine_similarity(flat[i], flat[j], dim=0).item()
            div += (1.0 - cos); npair += 1
    expert_div = (div / npair) if npair else 0.0
    logits = b.moe.router(h)
    probs  = F.softmax(logits, dim=1)
    ent    = -(probs * torch.log(probs + 1e-9)).sum(dim=1).mean().item()
    usage  = probs.mean(dim=(0, 2))
    u      = torch.sort(usage).values
    nn_    = u.numel()
    idx    = torch.arange(1, nn_ + 1, dtype=u.dtype, device=u.device)
    gini   = (2.0 * (idx * u).sum() / (nn_ * u.sum() + 1e-9) - (nn_ + 1) / nn_).item()
    return {"expert_div": round(expert_div, 5), "router_entropy": round(ent, 5),
            "usage_gini": round(gini, 5),
            "usage": [round(float(z), 5) for z in usage.tolist()], "n_experts": n_e}


# ════════════════════════════════════════════════════════════════════════════
ARMS = {
    "ctrl":  False,  # standard expert weight + recomb-objective
    "tlora": True,   # TLoRA expert weight + recomb-objective
}


def main():
    ap = ap = argparse.ArgumentParser()
    ap.add_argument("--arm", required=True, choices=list(ARMS))
    ap.add_argument("--tlora-rank", type=int, default=TLORA_RANK)
    ap.add_argument("--tlora-no-base", action="store_true")
    ap.add_argument("--recomb-lambda", type=float, default=RECOMB_LAMBDA,
                    help="L_recomb weight (non-negotiable; must be >0 for both arms)")
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
    ap.add_argument("--bf16", action="store_true")
    ap.add_argument("--sample", choices=["roundrobin", "proportional"], default="proportional")
    ap.add_argument("--val-frac", type=float, default=0.05)
    ap.add_argument("--val-every", type=int, default=200)
    ap.add_argument("--val-batches", type=int, default=4)
    ap.add_argument("--log-every", type=int, default=100)
    ap.add_argument("--dbes-every", type=int, default=500)
    ap.add_argument("--out", default="")
    ap.add_argument("--ckpt-out", default="")
    ap.add_argument("--gauges-out", default="")
    a = ap.parse_args()

    tlora_on = ARMS[a.arm]
    if a.recomb_lambda <= 0.0:
        print("WARNING: --recomb-lambda=0 disables L_recomb — NOT RECOMMENDED per spec.", flush=True)
    savant_on  = not a.no_savant
    mitosis_on = not a.no_mitosis
    if a.canon:
        d       = a.d or 3784;  L      = a.L or 4
        seq_len = a.seq_len or 1024; steps = a.steps or 4000   # ≥4000 per spec
    else:
        d       = a.d or 64;   L      = a.L or 2
        seq_len = a.seq_len or 128; steps = a.steps or 60
    e0, emax = a.e0, a.emax
    V, K     = 256, 3
    device   = "cuda" if torch.cuda.is_available() else "cpu"

    print(f"=== H_1813 TPR-EXPERT-WEIGHT arm={a.arm} seed={a.seed} recomb_λ={a.recomb_lambda} ===",
          flush=True)
    print(f"  levers: tlora={tlora_on}(rank={a.tlora_rank},base={not a.tlora_no_base})",
          flush=True)
    print(f"  device={device} d={d} L={L} E0={e0} Emax={emax} seq_len={seq_len} "
          f"steps={steps} bs={a.batch_size}", flush=True)
    if device == "cuda":
        cap = torch.cuda.get_device_capability()
        print(f"  cuda: {torch.cuda.get_device_name(0)} cap={cap[0]}.{cap[1]} "
              f"torch={torch.__version__}", flush=True)

    torch.manual_seed(a.seed)
    cfg   = CLMConfig(n_experts=emax, n_trunk_layers=L, d_model=d, kernel_size=K,
                      variant="AB", dilation_base=2, max_dilation=512)
    model = CLMConvMoE(cfg).to(device)
    if tlora_on:
        install_tlora_experts(model, a.tlora_rank, base=not a.tlora_no_base)
        model.to(device)
    n_params = sum(p.numel() for p in model.parameters())
    print(f"  params: {n_params} ({n_params / 1e6:.3f}M)", flush=True)

    mito = T.MitosisMoE(model, e0, emax)
    T.install_router_mask(model, mito)
    opt  = torch.optim.AdamW(model.parameters(), lr=a.lr,
                             betas=(0.9, 0.999), eps=1e-8, weight_decay=0.0)
    gen  = torch.Generator().manual_seed(42)
    val_gen = torch.Generator().manual_seed(1234)

    latch      = {"on": False, "at": 0}
    i0         = T.GZ_UPPER
    i_floor    = T.GZ_LOWER - 0.05
    split_step = max(1, steps // 2)

    # corpus cells
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
    _samp_w     = torch.tensor([float(c.train_end) for c in _samp_cells]) \
        if _samp_cells else torch.tensor([1.0])

    def get_batch(step):
        if cells:
            xs, ys = [], []
            for b in range(a.batch_size):
                if _samp_cells:
                    ci   = int(torch.multinomial(_samp_w, 1, generator=gen).item())
                    cell = _samp_cells[ci]
                else:
                    cell = cells[(step - 1 + b) % len(cells)]
                w = cell.window(seq_len, gen)
                if w is None:
                    base = torch.arange(seq_len)
                    w    = (base % V, (base + 1) % V)
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

    # ── train loop ────────────────────────────────────────────────────────────
    model.train()
    t0 = time.time(); loss0 = lossF = None; last_aux = {}; dbes_log = []
    for step in range(1, steps + 1):
        if savant_on:
            inh = T.savant_inhibition(step, steps, i0, i_floor, latch)
            wd  = T.inhibition_to_wd(inh); dp = T.inhibition_to_dropout(inh)
        else:
            wd, dp = 0.0, 0.0
        for grp in opt.param_groups:
            grp["weight_decay"] = wd
        for m in model.modules():
            if isinstance(m, nn.Dropout): m.p = dp
        if mitosis_on and step == split_step and mito.e_active < emax:
            prev  = mito.e_active
            new_e = (tlora_aware_split(mito, 0, opt) if tlora_on else mito.split(0, opt))
            print(f"  step {step} (MITOSIS SPLIT) E {prev}->{new_e}", flush=True)
        x, y = get_batch(step)
        opt.zero_grad(set_to_none=True)
        if a.bf16 and device == "cuda":
            with torch.autocast("cuda", dtype=torch.bfloat16):
                out            = model(x, y)
                loss           = out["ce_loss"] + out["aux_loss"]
                rl, raux       = recomb_loss(model, x, y, a.recomb_lambda)
                loss           = loss + rl
        else:
            out              = model(x, y)
            loss             = out["ce_loss"] + out["aux_loss"]
            rl, raux         = recomb_loss(model, x, y, a.recomb_lambda)
            loss             = loss + rl
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        opt.step()
        ce       = float(out["ce_loss"].detach())
        last_aux = raux
        if loss0 is None: loss0 = ce
        lossF    = ce
        if a.dbes_every and (step % a.dbes_every == 0 or step == steps):
            db         = dbes_specialization(model, x); db["step"] = step
            dbes_log.append(db)
        if step == 1 or step % a.log_every == 0 or step == steps:
            do_val = a.val_every > 0 and (step == 1 or step % a.val_every == 0
                                          or step == steps)
            vtxt   = ""
            if do_val:
                per  = val_per_cell()
                vc   = (sum(per.values()) / len(per)) if per else float("nan")
                vtxt = f"  val_CE={vc:.5f}"
            print(f"  step {step:5d}  CE={ce:.5f}  E={mito.e_active}  "
                  f"wd={wd:.4f} dp={dp:.4f}  recomb_ce={raux.get('recomb_ce', '?')}{vtxt}",
                  flush=True)
    wall = time.time() - t0

    # ── held-out DESCENT gate (math.log mirror — dt_ln bug workaround) ──────
    uniform = math.log(V)
    per     = val_per_cell()
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

    # ── N3 DBES final ─────────────────────────────────────────────────────────
    dbes_final = None
    try:
        xb, _  = get_batch(steps + 1)
        dbes_final = dbes_specialization(model, xb)
        print(f"  [N3 DBES] {json.dumps(dbes_final, ensure_ascii=False)}", flush=True)
    except Exception as e:
        print(f"  DBES error: {e}", flush=True)

    # ── torch ckpt persist (a_fire_recover_complete) ─────────────────────────
    if a.ckpt_out:
        torch.save({k: v.detach().cpu() for k, v in model.state_dict().items()}, a.ckpt_out)
        print(f"  torch ckpt -> {a.ckpt_out} ({os.path.getsize(a.ckpt_out)} bytes)", flush=True)

    summary = {
        "hyp": "H_1813", "arm": a.arm, "seed": a.seed,
        "levers": {"tlora": tlora_on, "tlora_rank": a.tlora_rank,
                   "tlora_base": not a.tlora_no_base, "recomb_lambda": a.recomb_lambda},
        "n_params": n_params, "loss0": round(loss0, 5), "lossF": round(lossF, 5),
        "wall_s": round(wall, 1), "uniform_ce": round(uniform, 5),
        "final_val_ce_pooled": (round(final_val, 5) if final_val is not None else None),
        "registers_descent": f"{n_desc}/{len(per)}", "heldout_descent": descent,
        "last_aux": last_aux, "dbes_final": dbes_final, "dbes_log": dbes_log,
        "tier": "engine-native-eligible (.clm materialized experts); torch-probe DIRECTIONAL"
    }
    if a.gauges_out:
        with open(a.gauges_out, "w") as f:
            json.dump(summary, f, ensure_ascii=False, indent=2)
        print(f"  summary -> {a.gauges_out}", flush=True)

    # ── serialize .clm (TLoRA materialized to dense, engine-native) ──────────
    if a.out:
        e_ser = mito.e_active
        mat   = materialize_experts_into_state(model)
        sd_a  = {}
        for k, v in mat.items():
            if k in ("moe.router.weight", "moe.router.bias"):
                sd_a[k] = v[:e_ser].contiguous()
            elif k.startswith("moe.experts."):
                if int(k.split(".")[2]) < e_ser:
                    sd_a[k] = v
            else:
                sd_a[k] = v
        S.serialize_v3(sd_a, n_trunk_layers=L, n_experts=e_ser, out_path=a.out)
        print(f"  .clm -> {a.out} ({os.path.getsize(a.out)} bytes)", flush=True)
        rb = open(a.out, "rb").read()
        print(f"  clm_decodable={VC.clm_decodable(rb)}", flush=True)


if __name__ == "__main__":
    main()
