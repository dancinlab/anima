#!/usr/bin/env python3
"""EXP-3 303M ARM-BIND (H_1603/H_1617 scale-up) — DIRECTIONAL (torch, see PREREG.md).

Trains THREE arms of the production 303M CLMConvMoE that share an IDENTICAL trunk
(embed/conv-trunk/MoE/norm_out), differing ONLY in the byte readout:

  ctrl        : production additive readout  Conv1d(d->V)
  bind        : Hadamard coincidence readout u=Wa(x), v=Wb(x), g=u*v, logit=Wo(g)
  bind_linear : SAME params (Wa,Wb,Wo) but g=u+v  (multiply->add ablation)

Canonical recipe (savant golden-zone inhibition + mitosis E2->E3 split + 4-cell
register corpus + held-out val) is REUSED verbatim from cli/train.py so the only
intended difference between arms is the readout. This is the REFERENCE+BRIDGE
torch path (a_clm_gen_pipeline); torch-side metrics here are DIRECTIONAL only
(a_engine_native_learning). ARM-BIND is NOT .clm-serializable (the .clm format
only knows an additive readout), so engine-native is by-construction BLOCKED for
bind/bind_linear — ARM-CTRL serializes to .clm for an optional engine-native anchor.

USAGE:
  python3 trainer.py --arm {ctrl,bind,bind_linear} --seed N --corpus <p1..p4> \\
      --cell-label ko-general en-general ko-sns en-sns --canon --steps 2000 \\
      --val-frac 0.05 --val-every 200 --sample proportional \\
      --out ckpt/<arm>_seed<N>.clm --ckpt-out ckpt/<arm>_seed<N>.pt \\
      --gauges-out ckpt/<arm>_seed<N>.gauges.json
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

from model import CLMConfig, CLMConvMoE, MoEStats            # train/clm/model/model.py
import clm_serialize_v2 as S                                 # serialize_v3 (ground truth)
import verify_clm_v2 as VC                                   # clm_decodable / descent
# canonical recipe levers (savant/mitosis/corpus/val) — imported verbatim:
import train as T                                            # cli/train.py


# ════════════════════════════════════════════════════════════════════════════
#  BIND readout wrapper — shares the CLMConvMoE trunk, replaces the readout only.
# ════════════════════════════════════════════════════════════════════════════
class BindCLM(nn.Module):
    """CLMConvMoE trunk + a multiplicative (or param-matched additive) readout.

    Trunk path (embed -> embed_conv -> trunk -> moe -> norm_out) is the EXACT
    production path; only the final byte projection differs. base.readout is
    dropped (Identity) so it neither runs nor inflates the param count."""

    def __init__(self, cfg: CLMConfig, mode: str, k: int = 512):
        super().__init__()
        assert mode in ("bind", "bind_linear")
        self.base = CLMConvMoE(cfg)
        self.base.readout = nn.Identity()          # unused for bind arms
        self.mode = mode
        self.cfg = cfg
        d, V = cfg.d_model, cfg.vocab_size
        self.Wa = nn.Conv1d(d, k, 1)
        self.Wb = nn.Conv1d(d, k, 1)
        self.Wo = nn.Conv1d(k, V, 1)

    @property
    def moe(self):
        return self.base.moe

    def _features(self, tokens):
        b = self.base
        x = b.embed(tokens).transpose(1, 2)        # (B, C, T)
        x = b.embed_conv(x)
        for layer in b.trunk:
            x = layer(x)
        x, stats = b.moe(x)
        x = b.norm_out(x)
        return x, stats

    def forward(self, tokens, targets=None):
        x, stats = self._features(tokens)
        u, v = self.Wa(x), self.Wb(x)
        g = (u * v) if self.mode == "bind" else (u + v)
        logits = self.Wo(g)                         # (B, V, T)
        out = {"logits": logits, "usage": stats.usage,
               "aux_loss": stats.aux_loss, "routing_entropy": stats.entropy}
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
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--arm", required=True, choices=["ctrl", "bind", "bind_linear"])
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
    ap.add_argument("--k", type=int, default=512, help="bind head bottleneck width")
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
    ap.add_argument("--out", default="", help=".clm path (ctrl only; bind skips)")
    ap.add_argument("--ckpt-out", default="", help="torch .pt state_dict path")
    ap.add_argument("--gauges-out", default="", help="G1/G6 torch-probe json out")
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

    print(f"=== EXP-3 303M ARM-{a.arm.upper()} seed={a.seed} ===", flush=True)
    print(f"  device={device} d={d} L={L} E0={e0} Emax={emax} seq_len={seq_len} "
          f"steps={steps} bs={a.batch_size} sample={a.sample}", flush=True)
    if device == "cuda":
        cap = torch.cuda.get_device_capability()
        print(f"  cuda: {torch.cuda.get_device_name(0)} cap={cap[0]}.{cap[1]} "
              f"torch={torch.__version__}", flush=True)

    torch.manual_seed(a.seed)

    cfg = CLMConfig(n_experts=emax, n_trunk_layers=L, d_model=d, kernel_size=K,
                    variant="AB", dilation_base=2, max_dilation=512)
    if a.arm == "ctrl":
        model = CLMConvMoE(cfg).to(device)
        core = model
    else:
        model = BindCLM(cfg, a.arm, k=a.k).to(device)
        core = model.base
    n_params = model.num_params()
    print(f"  params: {n_params} ({n_params/1e6:.3f}M)", flush=True)

    mito = T.MitosisMoE(core, e0, emax)
    T.install_router_mask(core, mito)
    opt = torch.optim.AdamW(model.parameters(), lr=a.lr, betas=(0.9, 0.999),
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
        if loss0 is None: loss0 = ce
        lossF = ce
        do_val = a.val_every > 0 and (step == 1 or step % a.val_every == 0 or step == steps)
        if step == 1 or step % a.log_every == 0 or step == steps:
            vtxt = ""
            if do_val:
                per = val_per_cell()
                vc = (sum(per.values()) / len(per)) if per else float("nan")
                vtxt = f"  val_CE={vc:.5f}"
            print(f"  step {step:5d}  CE={ce:.5f}  E={mito.e_active}  "
                  f"wd={wd:.4f} dp={dp:.4f}{vtxt}", flush=True)
    wall = time.time() - t0

    # ── FINAL held-out val per register (DESCENT gate, torch correct CE) ──────
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

    # ── gauges/descent summary json ──────────────────────────────────────────
    summary = {"arm": a.arm, "seed": a.seed, "n_params": n_params,
               "loss0": round(loss0, 5), "lossF": round(lossF, 5),
               "wall_s": round(wall, 1), "uniform_ce": round(uniform, 5),
               "final_val_ce_pooled": (round(final_val, 5) if final_val else None),
               "registers_descent": f"{n_desc}/{len(per)}",
               "heldout_descent": descent, "gauges_g1g6_torch_probe": gauges,
               "tier": "DIRECTIONAL (torch probe; engine-native bind=BLOCKED-by-construction)"}
    if a.gauges_out:
        with open(a.gauges_out, "w") as f:
            json.dump(summary, f, ensure_ascii=False, indent=2)
        print(f"  summary -> {a.gauges_out}", flush=True)

    # ── ctrl: serialize .clm v0.3 + descent gate (engine-native anchor) ──────
    if a.arm == "ctrl" and a.out:
        e_ser = mito.e_active
        sd_active = {}
        for k, vv in sd.items():
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
        print(f"  .clm WRITTEN {os.path.getsize(a.out)} bytes -> {a.out}", flush=True)
        rb = open(a.out, "rb").read()
        print(f"  clm_decodable={VC.clm_decodable(rb)}", flush=True)
    elif a.arm != "ctrl":
        print(f"  ARM-{a.arm.upper()}: NOT .clm-serializable (Hadamard readout); "
              f"engine-native BLOCKED-by-construction -> torch .pt only (DIRECTIONAL).",
              flush=True)


if __name__ == "__main__":
    main()
