#!/usr/bin/env python3
"""H_1818 — co-trained LIVE-RETAINED bind op: does Hadamard binding lift G1/G6
when the operator is (a) retained in the .clm at serialize AND (b) co-trained
end-to-end with trunk+readout (NOT dropped like EXP-3 / NOT frozen like mouthbind)?

TWO ARMS (both engine-native-eligible via clm_decode.py CLMB extension):
  bind : CLMConvMoE trunk + Hadamard bind readout  u=Wa(x), v=Wb(x), g=u*v, logit=Wo(g)
          serialized via serialize_v3_bind (CLMB section — bind op LIVE at decode)
  ctrl : Standard CLMConvMoE (additive Conv1d d->V readout)
          serialized via serialize_v3 (no CLMB — same as EXP-3 ctrl)

DESIGN (engine-transform-to-fit, a_engine_native_learning):
  · clm_decode.py is EXTENDED to parse CLMB + execute bind in _fwd_logits.
  · For bind: roW holds Wo(V,k), CLMB holds Wa(k,d)/WaB(k)/Wb(k,d)/WbB(k).
  · g_gates.py uses clm_decode.py → bind op LIVE during G0-G6 eval.
  · k=512 (matches EXP-3 bind head width for fair comparison).

DIFFERENCE FROM EXP-3 (state/binding_arch_census/exp3_303m/):
  EXP-3 "NOT .clm-serializable" → bind readout DROPPED before serialize →
  g_gates decoded WITHOUT bind → DIRECTIONAL-floor verdict.
  H_1818: bind op RETAINED in .clm + clm_decode executes it → FIRST engine-native
  test of the co-trained live bind hypothesis.

FROZEN BAR (pre-registered, NO tune-to-green, p7):
  G1: composed_distinct>=2 AND >max_single AND coherent, >=2/3 seeds {7,4302,4303}.
  G6: dist>=5 AND fals>=1.
  LIFT: bind-ON strictly > ctrl on G1 best_distinct / G6 fals, same seeds.
  held-out: 4/4 register DESCENT (else overfit → invalid verdict).

USAGE:
  python3 trainer.py --arm {bind,ctrl} --seed N --corpus <4 paths> \\
      --cell-label ko-general en-general ko-sns en-sns --canon --steps 2000 \\
      --val-frac 0.05 --val-every 200 --sample proportional --bf16 \\
      --out ckpt/<arm>_seed<N>.clm --ckpt-out ckpt/<arm>_seed<N>.pt \\
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

# ── bind head bottleneck width (matches EXP-3 default for fair comparison) ──
BIND_K = 512


# ════════════════════════════════════════════════════════════════════════════
# BindCLM — CLMConvMoE trunk + co-trained Hadamard bind readout
# SERIALIZES via serialize_v3_bind (CLMB retained, bind op LIVE at decode).
# ════════════════════════════════════════════════════════════════════════════
class BindCLM(nn.Module):
    """CLMConvMoE trunk with Hadamard bind readout co-trained end-to-end.

    The standard base.readout (Conv1d d->V) is REPLACED by:
        Wa: Conv1d(d, k, 1) — projection A
        Wb: Conv1d(d, k, 1) — projection B
        Wo: Conv1d(k, V, 1) — output projection
        g  = Wa(x) * Wb(x) — element-wise Hadamard product
        logits = Wo(g)

    Serialization (serialize_v3_bind):
        Wo  → roW slot (cout=V, rest=k) in main CLM body
        WoB → roB ext
        Wa/WaB, Wb/WbB → CLMB section (appended after CLMX)
    At decode, clm_decode.py parses CLMB and executes the bind op in
    _fwd_logits, making the bind op LIVE (not dropped, not frozen-only).
    """

    def __init__(self, cfg: CLMConfig, k: int = BIND_K):
        super().__init__()
        d, V = cfg.d_model, cfg.vocab_size
        self.base = CLMConvMoE(cfg)
        self.base.readout = nn.Identity()          # replaced by bind readout
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
        x = b.embed(tokens).transpose(1, 2)        # (B, d, T)
        x = b.embed_conv(x)
        for layer in b.trunk:
            x = layer(x)
        x, stats = b.moe(x)
        x = b.norm_out(x)                          # (B, d, T)
        return x, stats

    def forward(self, tokens, targets=None):
        x, stats = self._trunk_out(tokens)         # (B, d, T)
        u = self.Wa(x)                             # (B, k, T)
        v = self.Wb(x)                             # (B, k, T)
        g = u * v                                  # Hadamard (B, k, T)
        logits = self.Wo(g)                        # (B, V, T)

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


def _serialize_bind(model: BindCLM, mito, L: int, out_path: str):
    """Serialize BindCLM via serialize_v3_bind: trunk + CLMB bind weights retained."""
    e_ser = mito.e_active
    sd = {k: v.detach().cpu() for k, v in model.state_dict().items()}

    # Build a dict that serialize_v3_bind understands.
    # Trunk keys (under 'base.') map to standard CLMConvMoE keys.
    # Wa/Wb/Wo are at top-level in BindCLM state_dict.
    norm = {}
    for k, v in sd.items():
        # Strip 'base.' prefix so trunk keys match CLMConvMoE standard layout.
        nk = k[5:] if k.startswith("base.") else k
        norm[nk] = v

    # Prune experts to the active count (mitosis).
    pruned = {}
    for k, v in norm.items():
        if k in ("moe.router.weight", "moe.router.bias"):
            pruned[k] = v[:e_ser].contiguous()
        elif k.startswith("moe.experts."):
            if int(k.split(".")[2]) < e_ser:
                pruned[k] = v
        else:
            pruned[k] = v

    # serialize_v3_bind routes Wo -> readout.{weight,bias} (roW/roB in body)
    # and Wa/WaB/Wb/WbB -> CLMB section. readout_type=1 = Hadamard.
    S.serialize_v3_bind(pruned, n_trunk_layers=L, n_experts=e_ser,
                        readout_type=S.RO_BIND_HADAMARD, out_path=out_path)


def _serialize_ctrl(model: CLMConvMoE, mito, L: int, out_path: str):
    """Serialize standard CLMConvMoE via serialize_v3 (no CLMB)."""
    e_ser = mito.e_active
    sd = {k: v.detach().cpu() for k, v in model.state_dict().items()}
    pruned = {}
    for k, v in sd.items():
        if k in ("moe.router.weight", "moe.router.bias"):
            pruned[k] = v[:e_ser].contiguous()
        elif k.startswith("moe.experts."):
            if int(k.split(".")[2]) < e_ser:
                pruned[k] = v
        else:
            pruned[k] = v
    S.serialize_v3(pruned, n_trunk_layers=L, n_experts=e_ser, out_path=out_path)


# ════════════════════════════════════════════════════════════════════════════
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--arm", required=True, choices=["bind", "ctrl"])
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
    ap.add_argument("--k", type=int, default=BIND_K, help="bind head bottleneck width")
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
    ap.add_argument("--out", default="", help=".clm output path")
    ap.add_argument("--ckpt-out", default="", help="torch .pt path (a_fire_recover_complete)")
    ap.add_argument("--gauges-out", default="", help="summary json path")
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
    k = a.k
    V, K = 256, 3
    device = "cuda" if torch.cuda.is_available() else "cpu"

    print(f"=== H_1818 CO-TRAINED-LIVE-BIND arm={a.arm} seed={a.seed} ===", flush=True)
    print(f"  device={device} d={d} L={L} E0={e0} Emax={emax} k={k} seq_len={seq_len} "
          f"steps={steps} bs={a.batch_size} sample={a.sample}", flush=True)
    if device == "cuda":
        cap = torch.cuda.get_device_capability()
        print(f"  cuda: {torch.cuda.get_device_name(0)} cap={cap[0]}.{cap[1]} "
              f"torch={torch.__version__}", flush=True)

    torch.manual_seed(a.seed)
    cfg = CLMConfig(n_experts=emax, n_trunk_layers=L, d_model=d, kernel_size=K,
                    variant="AB", dilation_base=2, max_dilation=512)

    if a.arm == "bind":
        model = BindCLM(cfg, k=k).to(device)
        core = model.base
    else:
        model = CLMConvMoE(cfg).to(device)
        core = model

    n_params = model.num_params() if hasattr(model, "num_params") else \
               sum(p.numel() for p in model.parameters())
    print(f"  params: {n_params:,} ({n_params / 1e6:.3f}M)", flush=True)

    mito = T.MitosisMoE(core, e0, emax)
    T.install_router_mask(core, mito)
    opt = torch.optim.AdamW(model.parameters(), lr=a.lr, betas=(0.9, 0.999),
                            eps=1e-8, weight_decay=0.0)
    gen = torch.Generator().manual_seed(42)      # data RNG shared across arms
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

    # ── FINAL held-out val per register (H_1579 DESCENT gate) ────────────────
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

    # ── persist torch ckpt (ALWAYS — a_fire_recover_complete) ────────────────
    sd_full = {k: v.detach().cpu() for k, v in model.state_dict().items()}
    if a.ckpt_out:
        torch.save(sd_full, a.ckpt_out)
        print(f"  torch ckpt -> {a.ckpt_out} ({os.path.getsize(a.ckpt_out)} bytes)", flush=True)

    summary = {"arm": a.arm, "seed": a.seed, "n_params": n_params, "k": k,
               "loss0": round(loss0, 5), "lossF": round(lossF, 5),
               "wall_s": round(wall, 1), "uniform_ce": round(uniform, 5),
               "final_val_ce_pooled": (round(final_val, 5) if final_val else None),
               "registers_descent": f"{n_desc}/{len(per)}",
               "heldout_descent": descent,
               "tier": ("engine-native-eligible (CLMB retained, bind LIVE at decode)"
                        if a.arm == "bind" else
                        "engine-native-eligible (standard additive readout)")}
    if a.gauges_out:
        with open(a.gauges_out, "w") as f:
            json.dump(summary, f, ensure_ascii=False, indent=2)
        print(f"  summary -> {a.gauges_out}", flush=True)

    # ── serialize .clm + DESCENT gate (a_clm_gen_pipeline) ──────────────────
    if a.out:
        if a.arm == "bind":
            _serialize_bind(model, mito, L, a.out)
            print(f"  .clm (CLMB bind) WRITTEN {os.path.getsize(a.out)} bytes -> {a.out}",
                  flush=True)
        else:
            _serialize_ctrl(model, mito, L, a.out)
            print(f"  .clm (additive) WRITTEN {os.path.getsize(a.out)} bytes -> {a.out}",
                  flush=True)
        rb = open(a.out, "rb").read()
        decodable = VC.clm_decodable(rb)
        print(f"  clm_decodable={decodable}", flush=True)
        # Descent gate: held-out CE via math.log mirror (not engine CE — dt_ln bug)
        if n_desc > 0 and cells:
            try:
                heldout_path = cells[0].path   # ko-general held-out
                r = VC.descent(a.out, heldout_path)
                print(f"  verify_descent={r}", flush=True)
            except Exception as e:
                print(f"  verify_descent error: {e}", flush=True)


if __name__ == "__main__":
    main()
