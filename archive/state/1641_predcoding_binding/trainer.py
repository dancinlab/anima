#!/usr/bin/env python3
"""H_1641 PREDCODING-BINDING 303M — predictive-coding / free-energy parametric-bias
binding as a G1-recombination AND G6-ideation lever (see PREREG.md).

BIOLOGY (predictive coding / active inference / free-energy; Tani et al.
arxiv 2403.19995, "Development of Compositionality ... Predictive-Coding RNN"):
  Compositional generalization (compose/decompose, part<->whole) EMERGES in a
  predictive-coding RNN that minimizes evidence free energy. The two compositional
  drivers Tani isolates are:
    (1) a BINDING loss  L_pb = k * sum_t (PB~_t - PB)^2  — forcing the network's
        per-step inferred latent ("parametric bias") to match a STABLE sequence-
        level latent. A constant PB across a sequence despite varying surface
        content is what makes the structure (the composition) extrapolate to
        UNSEEN combinations. anima A<->G tension is the homologue of PC top-down
        prediction vs bottom-up error.
    (2) a KL / variance REGULARIZER on the latent prior that prevents memorizing
        surface patterns and forces structural extrapolation (D_KL(q||p), Eq.31).

  anima G1 hypothesis: CE next-byte gives NO pressure for a stable compositional
  latent, so the trunk never forms the part<->whole code recombination needs.
  G6 hypothesis: "novel-but-grounded" generation = free-energy minimization
  (grounded by prediction, novel by latent extrapolation) — the binding latent is
  the substrate for grounded novelty.

IMPLEMENTATION AXIS — OBJECTIVE / REPRESENTATION, *not* a multiplicative readout.
  Realized as a free-energy-style AUXILIARY OBJECTIVE on the trunk's PENULTIMATE
  representation (post norm_out, pre readout) while the PRODUCTION ADDITIVE readout
  (Conv1d d->V) is kept IDENTICAL across arms:

    L_bind = mean_t || PB~_t - PB_seq ||^2    where
             PB~_t   = a tiny linear projection of the per-position penultimate
                       code into a low-dim BIND latent (the inferred parametric
                       bias at step t),
             PB_seq  = the sequence-mean of PB~ (the stable sequence-level latent,
                       stop-grad as the target).  Pushing per-step latents to a
                       single stable code = Tani's binding pressure.
    L_var  = -beta * var_over_batch(PB_seq)   a mild anti-collapse / spread term so
             PB_seq does not degenerate to a constant (the KL-style regularizer's
             role: keep the latent informative, prevent surface memorization).

  The BIND projection is TRAINING-ONLY (dropped before serialize) so the .clm is
  byte-identical-in-architecture to the production additive model. Readout stays
  additive => ALL arms .clm-serializable => engine-native G1/G6 by-construction
  OPEN (clm_decode.py / anima eval). torch-side metrics are DIRECTIONAL monitors.

ARMS (single variable = the predictive-coding auxiliary objective; trunk/readout/
data/step/seed shared verbatim with the ce_marginal control):
  ce_marginal     : production CE next-byte only (DISCRIMINATING CONTROL — null).
  pc_bind         : CE + lambda_bind * L_bind                 (binding only).
  pc_free_energy  : CE + lambda_bind * L_bind + lambda_var * L_var (bind + spread).

Canonical recipe (savant golden-zone inhibition + mitosis E2->E3 split + 4-cell
register corpus + held-out val) is REUSED verbatim from cli/train.py so the only
intended difference between arms is the predictive-coding auxiliary objective.

USAGE:
  python3 trainer.py --objective {ce_marginal,pc_bind,pc_free_energy} \\
      --seed N --corpus <p1..p4> --cell-label ko-general en-general ko-sns en-sns \\
      --canon --steps 2000 --val-frac 0.05 --val-every 200 --sample proportional \\
      --out ckpt/<obj>_seed<N>.clm --ckpt-out ckpt/<obj>_seed<N>.pt \\
      --gauges-out ckpt/<obj>_seed<N>.json
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

from model import CLMConfig, CLMConvMoE                        # train/clm/model/model.py
import clm_serialize_v2 as S                                   # serialize_v3 (ground truth)
import verify_clm_v2 as VC                                     # clm_decodable / descent
import train as T                                              # cli/train.py (recipe levers)

# frozen objective hyperparams (pre-registered in PREREG.md — tune-to-green 금지)
LAMBDA_BIND = 0.1         # parametric-bias binding weight (Tani L_pb)
LAMBDA_VAR = 0.01         # anti-collapse spread weight (KL-style regularizer role)
BIND_DIM = 32            # low-dim parametric-bias latent width


# ════════════════════════════════════════════════════════════════════════════
#  Penultimate capture — post norm_out, pre readout (B,C,T). Hook so the SHARED
#  model file is NOT edited (we stay inside our own state/ dir).
# ════════════════════════════════════════════════════════════════════════════
class _PenultCapture:
    def __init__(self, model: CLMConvMoE):
        self.h = None
        self._hook = model.norm_out.register_forward_hook(self._grab)

    def _grab(self, module, inp, out):
        self.h = out                              # (B, C, T)

    def remove(self):
        self._hook.remove()


# ════════════════════════════════════════════════════════════════════════════
#  Predictive-coding parametric-bias binding loss on penultimate h: (B, C, T).
#  bind_proj: Linear(C -> BIND_DIM) is the inference of PB~_t. TRAINING-ONLY.
# ════════════════════════════════════════════════════════════════════════════
def loss_predcoding(h: torch.Tensor, bind_proj: nn.Module, use_var: bool):
    """Tani binding pressure: per-step parametric bias PB~_t should match the
    stable sequence-level PB (mean over T, stop-grad target). A constant latent
    across the sequence = the compositional-structure binding. Optional anti-
    collapse spread term keeps PB informative (KL-style regularizer role)."""
    B, C, Tt = h.shape
    z = h.permute(0, 2, 1)                        # (B, T, C)
    pb_t = bind_proj(z)                           # (B, T, BIND_DIM)  PB~_t
    pb_seq = pb_t.mean(dim=1, keepdim=True)       # (B, 1, BIND_DIM)  stable PB
    l_bind = ((pb_t - pb_seq.detach()) ** 2).mean()
    aux = {"bind": float(l_bind.detach())}
    extra = LAMBDA_BIND * l_bind
    if use_var:
        # spread over the batch of sequence-level latents (anti-collapse). We
        # MAXIMIZE spread -> minimize negative variance.
        v = pb_seq.squeeze(1).var(dim=0).mean()
        l_var = -v
        extra = extra + LAMBDA_VAR * l_var
        aux["pb_var"] = float(v.detach())
    return extra, aux


# ════════════════════════════════════════════════════════════════════════════
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--objective", required=True,
                    choices=["ce_marginal", "pc_bind", "pc_free_energy"])
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
    ap.add_argument("--sample", choices=["roundrobin", "proportional"],
                    default="proportional")
    ap.add_argument("--val-frac", type=float, default=0.05)
    ap.add_argument("--val-every", type=int, default=200)
    ap.add_argument("--val-batches", type=int, default=4)
    ap.add_argument("--log-every", type=int, default=50)
    ap.add_argument("--out", default="", help=".clm path (all arms — additive)")
    ap.add_argument("--ckpt-out", default="", help="torch .pt state_dict path")
    ap.add_argument("--gauges-out", default="", help="summary json out")
    a = ap.parse_args()

    use_bind = a.objective in ("pc_bind", "pc_free_energy")
    use_var = a.objective == "pc_free_energy"

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

    print(f"=== H_1641 PREDCODING-BINDING 303M obj={a.objective} seed={a.seed} ===", flush=True)
    print(f"  device={device} d={d} L={L} E0={e0} Emax={emax} seq_len={seq_len} "
          f"steps={steps} bs={a.batch_size} sample={a.sample} "
          f"use_bind={use_bind} use_var={use_var}", flush=True)
    if device == "cuda":
        cap = torch.cuda.get_device_capability()
        print(f"  cuda: {torch.cuda.get_device_name(0)} cap={cap[0]}.{cap[1]} "
              f"torch={torch.__version__}", flush=True)

    torch.manual_seed(a.seed)

    cfg = CLMConfig(n_experts=emax, n_trunk_layers=L, d_model=d, kernel_size=K,
                    variant="AB", dilation_base=2, max_dilation=512)
    model = CLMConvMoE(cfg).to(device)            # production additive readout (all arms)
    n_params = sum(p.numel() for p in model.parameters())
    print(f"  params: {n_params} ({n_params/1e6:.3f}M)", flush=True)

    pen = _PenultCapture(model)
    bind_proj = None
    if use_bind:
        bind_proj = nn.Linear(d, BIND_DIM).to(device)   # PB~ inference, training-only

    mito = T.MitosisMoE(model, e0, emax)
    T.install_router_mask(model, mito)
    params = list(model.parameters())
    if bind_proj is not None:
        params += list(bind_proj.parameters())
    opt = torch.optim.AdamW(params, lr=a.lr, betas=(0.9, 0.999),
                            eps=1e-8, weight_decay=0.0)
    gen = torch.Generator().manual_seed(42)        # data RNG SHARED across arms (fair)
    val_gen = torch.Generator().manual_seed(1234)

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

    # ── train loop (savant inhibition + mitosis split, verbatim arithmetic) ──
    model.train()
    t0 = time.time(); loss0 = lossF = None
    last_aux = {}
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

        def compute(out):
            ce = out["ce_loss"]
            aux = {}
            extra = 0.0
            if use_bind:
                lpc, da = loss_predcoding(pen.h, bind_proj, use_var)
                extra = extra + lpc
                aux.update(da)
            return ce + extra + out["aux_loss"], aux

        if a.bf16 and device == "cuda":
            with torch.autocast("cuda", dtype=torch.bfloat16):
                out = model(x, y)
                loss, aux = compute(out)
            loss.backward()
        else:
            out = model(x, y)
            loss, aux = compute(out)
            loss.backward()
        torch.nn.utils.clip_grad_norm_(params, 1.0)
        opt.step()
        ce = float(out["ce_loss"].detach())
        last_aux = aux
        if loss0 is None: loss0 = ce
        lossF = ce
        do_val = a.val_every > 0 and (step == 1 or step % a.val_every == 0 or step == steps)
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
    descent = {}
    n_desc = 0
    print(f"  ── FINAL held-out val-CE per register (uniform={uniform:.4f}) ──", flush=True)
    for lab, vc in per.items():
        ok = vc < uniform
        n_desc += int(ok)
        descent[lab] = {"val_ce": round(vc, 5), "descent": ok}
        print(f"     {lab:<12s} val_CE={vc:.5f}  {'DESCENT' if ok else 'NO-DESCENT'}", flush=True)
    final_val = (sum(per.values()) / len(per)) if per else None
    print(f"  FINAL val_CE(pooled)={final_val}  registers_DESCENT={n_desc}/{len(per)}", flush=True)
    print(f"  loss0={loss0:.5f} lossF={lossF:.5f} wall={wall:.1f}s "
          f"savant_latched_at={latch['at']} E0={e0}->E={mito.e_active}", flush=True)

    pen.remove()

    # ── G1/G6 torch-probe gauges (DIRECTIONAL, a_train_inline_gauge) ──────────
    gauges = None
    try:
        import gauge_lib
        was = model.training; model.eval()
        gauges = gauge_lib.compute_inline_gauges(
            model, None, seeds=7, corpus_index=[c.path for c in cells],
            ce=lossF, step=steps, torch=torch)
        if was: model.train()
        print(f"  [G1/G6 torch-probe DIRECTIONAL] {json.dumps(gauges, ensure_ascii=False)}",
              flush=True)
    except Exception as e:
        print(f"  gauges error: {e}", flush=True)

    # ── persist torch ckpt (ALWAYS — a_fire_recover_complete) ────────────────
    sd = {k: v.detach().cpu() for k, v in model.state_dict().items()}
    if a.ckpt_out:
        torch.save(sd, a.ckpt_out)
        print(f"  torch ckpt -> {a.ckpt_out} ({os.path.getsize(a.ckpt_out)} bytes)", flush=True)

    # ── summary json ──────────────────────────────────────────────────────────
    summary = {"objective": a.objective, "seed": a.seed, "n_params": n_params,
               "loss0": round(loss0, 5), "lossF": round(lossF, 5),
               "wall_s": round(wall, 1), "uniform_ce": round(uniform, 5),
               "final_val_ce_pooled": (round(final_val, 5) if final_val else None),
               "registers_descent": f"{n_desc}/{len(per)}",
               "heldout_descent": descent, "last_aux": last_aux,
               "lambda_bind": LAMBDA_BIND, "lambda_var": LAMBDA_VAR, "bind_dim": BIND_DIM,
               "gauges_g1g6_torch_probe": gauges,
               "tier": "engine-native-eligible (.clm additive); torch probe DIRECTIONAL"}
    if a.gauges_out:
        with open(a.gauges_out, "w") as f:
            json.dump(summary, f, ensure_ascii=False, indent=2)
        print(f"  summary -> {a.gauges_out}", flush=True)

    # ── serialize .clm v0.3 (ALL arms — production additive readout; the PC bind
    #    projection is TRAINING-ONLY and dropped here) ──────────────────────────
    if a.out:
        e_ser = mito.e_active
        sd_active = {}
        for k, vv in sd.items():
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
