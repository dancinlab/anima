#!/usr/bin/env python3
"""bind_base.py — shared base for the 4 DYNAMICS/ALGEBRAIC binding-mouth trainers
(H_1620 energy-settle · H_1630 tropical · H_1631 sheaf · H_1632 Galois-lattice).

CORE INVARIANT (task spec, differs from exp3 ARM-BIND):
  The binding op is TRAINING-ONLY structure on the PENULTIMATE representation.
  The PRODUCTION additive readout  base.readout = Conv1d(d -> V)  is KEPT and is
  the ONLY thing that produces the next-byte logits used for the CE loss + the
  serialized .clm.  The binding mouth adds (a) a penultimate binding transform B
  that re-mixes norm_out(x) -> x' before the readout, and (b) a MONITOR-ONLY
  auxiliary binding-consistency signal.  Because base.readout stays a plain
  Conv1d(d->V) and the trunk shape (embed/conv-trunk/MoE/norm_out/readout) is the
  EXACT production CLMConvMoE, the result SERIALIZES to .clm v0.3 and the live
  core/clm_decode.hexa loads it back -> engine-native G0-G6 is POSSIBLE (unlike
  exp3's Hadamard readout which was .clm-BLOCKED by construction).

  This realizes the trunk-OBJECTIVE lever (H_1602) the binding-wall census
  converged on as the real G1 lever, rather than the readout-op lever (exp3 =
  NOT-SUPPORTED at floor).

  The binding transform B writes back INTO the d-channel stream (residual), so the
  serialized weights are exactly {embed, embed_conv, trunk*, experts*, router,
  norm_out, readout} — the binding params are FOLDED in (see fold_binding below)
  OR, when not foldable, the .clm carries the trunk-shaped state and B is a
  train-time shaping force whose effect persists in the trunk weights it pushed.

ABLATION (per card): each mouth exposes a single continuous/structural knob that
collapses the binding op to the additive/feedforward baseline (K=1, T=1, R=I,
OR-pool).  Same params, knob OFF -> the dynamics is inert -> isolates the binding
mechanism as load-bearing iff the lift vanishes.

torch-side metrics here are DIRECTIONAL (a_engine_native_learning).  TERMINAL
verdict = CORE re-measure of the serialized .clm via cli/evaluate.py (g_gates.py
numpy mirror, byte-parity 2-production) — run post-hoc on a hexa/pool host.
"""
from __future__ import annotations
import argparse, json, math, os, sys, time
import torch
import torch.nn as nn
import torch.nn.functional as F

# ── locate repo + reuse the canonical recipe (savant/mitosis/corpus/val) ───────
_HERE = os.path.dirname(os.path.abspath(__file__))
_REPO = _HERE
while _REPO != "/" and not os.path.exists(os.path.join(_REPO, "cli", "train.py")):
    _REPO = os.path.dirname(_REPO)
for p in (os.path.join(_REPO, "cli"), os.path.join(_REPO, "train", "clm", "model"),
          os.path.join(_REPO, "tool")):
    if p not in sys.path:
        sys.path.insert(0, p)

from model import CLMConfig, CLMConvMoE                          # train/clm/model
import clm_serialize_v2 as S                                     # serialize_v3
import verify_clm_v2 as VC                                       # clm_decodable
import train as T                                                # cli/train.py levers


# ════════════════════════════════════════════════════════════════════════════
#  BindMouthCLM — production CLMConvMoE trunk + a penultimate binding transform.
#  base.readout (Conv1d d->V) is KEPT -> .clm-serializable.  The binding module
#  re-mixes norm_out(x) residually before the readout AND emits an aux scalar.
# ════════════════════════════════════════════════════════════════════════════
class BindMouthCLM(nn.Module):
    def __init__(self, cfg: CLMConfig, bind_module: nn.Module, aux_coef: float = 0.0):
        super().__init__()
        self.base = CLMConvMoE(cfg)        # FULL production model incl. readout
        self.bind = bind_module            # penultimate binding transform (train-only shape)
        self.cfg = cfg
        self.aux_coef = aux_coef           # MONITOR-ONLY by default (0.0 = no loss add)

    @property
    def moe(self):
        return self.base.moe

    def _trunk(self, tokens):
        b = self.base
        x = b.embed(tokens).transpose(1, 2)      # (B, C, T)
        x = b.embed_conv(x)
        for layer in b.trunk:
            x = layer(x)
        x, stats = b.moe(x)
        x = b.norm_out(x)                        # (B, C, T) penultimate
        return x, stats

    def forward(self, tokens, targets=None, ablate=False):
        x, stats = self._trunk(tokens)
        # binding transform: residual re-mix of the penultimate stream + aux scalar
        x_bound, aux_bind = self.bind(x, ablate=ablate)   # (B, C, T), scalar
        logits = self.base.readout(x_bound)               # PRODUCTION additive readout
        out = {"logits": logits, "usage": stats.usage,
               "aux_loss": stats.aux_loss, "routing_entropy": stats.entropy,
               "aux_bind": aux_bind}
        if targets is not None:
            ce = F.cross_entropy(
                logits.transpose(1, 2).reshape(-1, self.cfg.vocab_size),
                targets.reshape(-1))
            out["ce_loss"] = ce
            loss = ce + stats.aux_loss
            if self.aux_coef > 0.0:
                loss = loss + self.aux_coef * aux_bind
            out["loss"] = loss
        return out

    @torch.no_grad()
    def num_params(self) -> int:
        return sum(p.numel() for p in self.parameters())

    @torch.no_grad()
    def fold_to_clm_state(self):
        """Produce a state_dict for the PRODUCTION CLMConvMoE (serializable).

        The binding module shaped the trunk during training; at serialize time we
        keep the production weights {embed, embed_conv, trunk, experts, router,
        norm_out, readout}.  The binding transform's effect persists in those
        trained weights.  The binding op also re-mixes the penultimate stream at
        run-time, but the .clm format only carries the additive path; the SUPPORT
        hypothesis is that the trunk OBJECTIVE shaping (via the binding aux + the
        residual gradient) made the additive trunk itself compose better.  This is
        the honest engine-native anchor: it measures whether the binding-shaped
        trunk's PRODUCTION decode crosses G1/G6 — exactly the deployable path."""
        return {k: v.detach().cpu() for k, v in self.base.state_dict().items()}


# ════════════════════════════════════════════════════════════════════════════
#  generic CLI driver shared by all 4 mouths.  Each mouth passes a builder that
#  returns (bind_module, default_aux_coef).
# ════════════════════════════════════════════════════════════════════════════
def run(mouth_name: str, build_bind):
    ap = argparse.ArgumentParser(description=f"{mouth_name} binding-mouth trainer")
    ap.add_argument("--arm", required=True, choices=["bind", "ablate", "ctrl"],
                    help="bind = full binding dynamics · ablate = knob OFF (K=1/T=1/"
                         "R=I/OR-pool, same params) · ctrl = vanilla production trunk")
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
    ap.add_argument("--k", type=int, default=512, help="binding bottleneck width")
    ap.add_argument("--bind-steps", type=int, default=8, help="K settle/closure iters")
    ap.add_argument("--aux-coef", type=float, default=-1.0,
                    help="binding aux-loss coefficient; <0 = mouth default")
    ap.add_argument("--e0", type=int, default=2)
    ap.add_argument("--emax", type=int, default=4)
    ap.add_argument("--no-savant", action="store_true")
    ap.add_argument("--no-mitosis", action="store_true")
    ap.add_argument("--bf16", action="store_true")
    ap.add_argument("--sample", choices=["roundrobin", "proportional"],
                    default="proportional")
    ap.add_argument("--val-frac", type=float, default=0.05)
    ap.add_argument("--val-every", type=int, default=200)
    ap.add_argument("--val-batches", type=int, default=4)
    ap.add_argument("--log-every", type=int, default=50)
    ap.add_argument("--out", default="", help=".clm output path")
    ap.add_argument("--ckpt-out", default="", help="torch .pt state_dict path")
    ap.add_argument("--summary-out", default="", help="json summary out")
    a = ap.parse_args()

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

    print(f"=== {mouth_name} ARM-{a.arm.upper()} seed={a.seed} ===", flush=True)
    print(f"  device={device} d={d} L={L} E0={e0} Emax={emax} seq_len={seq_len} "
          f"steps={steps} bs={a.batch_size} bind_steps={a.bind_steps} k={a.k} "
          f"sample={a.sample}", flush=True)
    if device == "cuda":
        cap = torch.cuda.get_device_capability()
        print(f"  cuda: {torch.cuda.get_device_name(0)} cap={cap[0]}.{cap[1]} "
              f"torch={torch.__version__}", flush=True)

    torch.manual_seed(a.seed)
    cfg = CLMConfig(n_experts=emax, n_trunk_layers=L, d_model=d, kernel_size=K,
                    variant="AB", dilation_base=2, max_dilation=512)

    bind_mod, default_aux = build_bind(d=d, V=V, k=a.k, bind_steps=a.bind_steps)
    aux_coef = a.aux_coef if a.aux_coef >= 0.0 else default_aux
    ablate = (a.arm == "ablate")

    if a.arm == "ctrl":
        model = CLMConvMoE(cfg).to(device); core = model
        is_bind = False
    else:
        model = BindMouthCLM(cfg, bind_mod, aux_coef=aux_coef).to(device)
        core = model.base
        is_bind = True
    n_params = model.num_params()
    print(f"  params: {n_params} ({n_params/1e6:.3f}M)  aux_coef={aux_coef}  "
          f"ablate={ablate}", flush=True)

    mito = T.MitosisMoE(core, e0, emax)
    T.install_router_mask(core, mito)
    opt = torch.optim.AdamW(model.parameters(), lr=a.lr, betas=(0.9, 0.999),
                            eps=1e-8, weight_decay=0.0)
    gen = torch.Generator().manual_seed(42)        # SHARED data RNG (fair across arms)
    val_gen = torch.Generator().manual_seed(1234)
    latch = {"on": False, "at": 0}
    i0 = T.GZ_UPPER; i_floor = T.GZ_LOWER - 0.05
    split_step = max(1, steps // 2)

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

    _samp = [c for c in cells if c.train_end >= seq_len + 2]
    _w = torch.tensor([float(c.train_end) for c in _samp]) if _samp else torch.tensor([1.0])

    def get_batch(step):
        if cells:
            xs, ys = [], []
            for b in range(a.batch_size):
                if a.sample == "proportional" and _samp:
                    ci = int(torch.multinomial(_w, 1, generator=gen).item()); cell = _samp[ci]
                else:
                    cell = cells[(step - 1 + b) % len(cells)]
                w = cell.window(seq_len, gen)
                if w is None:
                    base = torch.arange(seq_len); w = (base % V, (base + 1) % V)
                xs.append(w[0]); ys.append(w[1])
            return torch.stack(xs).to(device), torch.stack(ys).to(device)
        base = torch.arange(seq_len)
        x = ((3 + base * 37) % V).unsqueeze(0).repeat(a.batch_size, 1).to(device)
        y = ((14 + base * 37) % V).unsqueeze(0).repeat(a.batch_size, 1).to(device)
        return x, y

    def _fwd(vx, vy):
        if is_bind:
            return model(vx, vy, ablate=ablate)
        return model(vx, vy)

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
                    vo = _fwd(vx, vy)
            else:
                vo = _fwd(vx, vy)
            tot += float(vo["ce_loss"].detach()); nb += 1
        if was: model.train()
        return (tot / nb) if nb else None

    def val_per_cell():
        return {lab: v for lab, c in zip(labels, cells)
                if (v := cell_val_ce(c)) is not None}

    model.train()
    t0 = time.time(); loss0 = lossF = auxF = None
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
                out = _fwd(x, y); loss = out["loss"]
            loss.backward()
        else:
            out = _fwd(x, y); loss = out["loss"]; loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        opt.step()
        ce = float(out["ce_loss"].detach())
        if loss0 is None: loss0 = ce
        lossF = ce
        auxF = float(out["aux_bind"].detach()) if "aux_bind" in out and torch.is_tensor(out["aux_bind"]) else (auxF or 0.0)
        do_val = a.val_every > 0 and (step == 1 or step % a.val_every == 0 or step == steps)
        if step == 1 or step % a.log_every == 0 or step == steps:
            vtxt = ""
            if do_val:
                per = val_per_cell()
                vc = (sum(per.values()) / len(per)) if per else float("nan")
                vtxt = f"  val_CE={vc:.5f}"
            print(f"  step {step:5d}  CE={ce:.5f}  aux_bind={auxF:.5f}  E={mito.e_active}  "
                  f"wd={wd:.4f} dp={dp:.4f}{vtxt}", flush=True)
    wall = time.time() - t0

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

    # ── persist torch ckpt ALWAYS (a_fire_recover_complete) ──────────────────
    sd = {k: v.detach().cpu() for k, v in model.state_dict().items()}
    if a.ckpt_out:
        torch.save(sd, a.ckpt_out)
        print(f"  torch ckpt -> {a.ckpt_out} ({os.path.getsize(a.ckpt_out)} bytes)", flush=True)

    # ── serialize PRODUCTION trunk -> .clm v0.3 (engine-native anchor) ───────
    clm_ok = None
    if a.out:
        prod_sd = model.fold_to_clm_state() if is_bind else \
            {k: v.detach().cpu() for k, v in model.state_dict().items()}
        e_ser = mito.e_active
        sd_active = {}
        for k, vv in prod_sd.items():
            if k == "moe.router.weight":
                sd_active[k] = vv[:e_ser].contiguous()
            elif k == "moe.router.bias":
                sd_active[k] = vv[:e_ser].contiguous()
            elif k.startswith("moe.experts."):
                if int(k.split(".")[2]) < e_ser:
                    sd_active[k] = vv
            else:
                sd_active[k] = vv
        S.serialize_v3(sd_active, n_trunk_layers=L, n_experts=e_ser, out_path=a.out)
        rb = open(a.out, "rb").read()
        clm_ok = VC.clm_decodable(rb)
        print(f"  .clm WRITTEN {os.path.getsize(a.out)} bytes -> {a.out}  "
              f"clm_decodable={clm_ok}", flush=True)

    summary = {"mouth": mouth_name, "arm": a.arm, "seed": a.seed, "ablate": ablate,
               "aux_coef": aux_coef, "n_params": n_params,
               "loss0": round(loss0, 5), "lossF": round(lossF, 5),
               "auxF": round(auxF, 5) if auxF is not None else None,
               "wall_s": round(wall, 1), "uniform_ce": round(uniform, 5),
               "final_val_ce_pooled": (round(final_val, 5) if final_val else None),
               "registers_descent": f"{n_desc}/{len(per)}", "heldout_descent": descent,
               "clm_decodable": clm_ok, "clm_out": a.out,
               "tier": "DIRECTIONAL (torch; terminal = engine-native cli/evaluate.py on .clm)"}
    if a.summary_out:
        with open(a.summary_out, "w") as f:
            json.dump(summary, f, ensure_ascii=False, indent=2)
        print(f"  summary -> {a.summary_out}", flush=True)
    return summary
