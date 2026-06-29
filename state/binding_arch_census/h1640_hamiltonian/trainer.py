#!/usr/bin/env python3
"""H_1640 — Conservative coupled-Hamiltonian (symplectic) binding mouth, 303M.

PREREG card: UNIVERSE/cards/H_1640_hamiltonian_symplectic_bind.md

Mechanism (per card):
  H(q,p) = H_A(q_A,p_A) + H_B(q_B,p_B) + lambda * C(q_A,q_B)
  Two legs init (q_A,p_A),(q_B,p_B) from trunk features; a SYMPLECTIC leapfrog
  integrator evolves them K steps (energy-conserving, no settling). The coupling
  C continuously exchanges action between oscillators so A's orbit is modulated
  by B and vice-versa; the bound code = time-pooled action vector (a JOINT
  INVARIANT of both legs) -> feeds an AUXILIARY binding head.

CRITICAL serialization design (differs from exp3 BindCLM which was .clm-BLOCKED):
  The Hamiltonian block + its auxiliary binding head are TRAINING-ONLY. They act
  as an *auxiliary loss* (L_bind) that shapes the SHARED trunk representation; the
  PRODUCTION additive readout Conv1d(d->V) is RETAINED and is what generates bytes
  and what serializes to .clm. So:
    - main next-byte CE goes through the production additive readout (engine-native)
    - L_bind (symplectic invariant must predict the next byte too) is the extra
      gradient pressure that forces the trunk to carry a *bound* (pair-sensitive)
      representation that CE alone never rewards.
  The binding head is DISCARDED before serialize -> the .clm is a plain additive
  CLMConvMoE = engine-native loadable (a_engine_native_learning engine-transform-to-fit).

ARMS (frozen, PREREG):
  arm        : full coupled-Hamiltonian binding aux (lambda>0, symplectic)
  ctrl       : lambda=0 ablation (decoupled oscillators) == card ABLATION-1
  diss       : gradient-descent (dissipative) integrator instead of symplectic
               == card ABLATION-2 (loses the orbit-coupling invariant)
All three share IDENTICAL trunk init seed / data / steps / production readout;
only the binding-aux mechanism differs. ctrl/diss are the inertness controls.

USAGE:
  python3 trainer.py --arm {arm,ctrl,diss} --seed N --corpus <4 paths> \\
      --cell-label ko-general en-general ko-sns en-sns --canon --steps 2000 \\
      --val-frac 0.05 --val-every 200 --sample proportional \\
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

from model import CLMConfig, CLMConvMoE                        # train/clm/model/model.py
import clm_serialize_v2 as S                                   # serialize_v3 (ground truth)
import verify_clm_v2 as VC                                     # clm_decodable / descent
import train as T                                              # cli/train.py (recipe levers)

# frozen hyperparams (pre-registered — tune-to-green forbidden)
BIND_LAMBDA = 1.0          # weight of the binding aux-loss
HAM_K = 10                 # leapfrog steps (card: K~10)
HAM_DIM = 64               # oscillator dim per leg (q,p each HAM_DIM)
HAM_DT = 0.1               # leapfrog step size
HAM_COUPLE = 1.0           # bilinear coupling lambda inside H (0 for ctrl arm)


class HamiltonianBinder(nn.Module):
    """Coupled-Hamiltonian binding aux head (TRAINING-ONLY, discarded pre-serialize).

    Reads the trunk feature x (B,C,T); projects each position into two oscillator
    legs (q_A,p_A) and (q_B,p_B); evolves them K leapfrog steps under
      H = 0.5|p_A|^2 + 0.5 w_A|q_A|^2 + 0.5|p_B|^2 + 0.5 w_B|q_B|^2 + cpl*<q_A, M q_B>
    (separable quadratic self-energy + bilinear coupling C = q_A^T M q_B). The
    coupling makes the leapfrog flow NON-separable -> A's orbit depends on B.
    The time-pooled action vector (mean over leapfrog trajectory of [q_A,p_A,q_B,p_B])
    is a joint invariant -> a small head predicts the next byte from it. That aux
    CE is the binding pressure.
    """
    def __init__(self, d, V, dim=HAM_DIM, k=HAM_K, dt=HAM_DT, couple=HAM_COUPLE,
                 mode="symplectic"):
        super().__init__()
        self.dim, self.k, self.dt, self.couple, self.mode = dim, k, dt, couple, mode
        # leg projections from trunk features
        self.qa = nn.Conv1d(d, dim, 1); self.pa = nn.Conv1d(d, dim, 1)
        self.qb = nn.Conv1d(d, dim, 1); self.pb = nn.Conv1d(d, dim, 1)
        # learned positive frequencies (softplus) for self-energy
        self.log_wa = nn.Parameter(torch.zeros(dim))
        self.log_wb = nn.Parameter(torch.zeros(dim))
        # bilinear coupling matrix M (q_A^T M q_B)
        self.M = nn.Parameter(torch.randn(dim, dim) * (1.0 / math.sqrt(dim)))
        # readout from time-pooled action (4*dim) -> byte logits (aux)
        self.head = nn.Conv1d(4 * dim, V, 1)

    def _force(self, qa, qb, wa, wb):
        # -dH/dq for each leg:  F_qa = -(wa*qa + couple * M qb), F_qb = -(wb*qb + couple * M^T qa)
        # qa: (B,dim,T)
        cpl = self.couple
        Mqb = torch.einsum("ij,bjt->bit", self.M, qb)
        MTqa = torch.einsum("ji,bjt->bit", self.M, qa)
        fa = -(wa.view(1, -1, 1) * qa + cpl * Mqb)
        fb = -(wb.view(1, -1, 1) * qb + cpl * MTqa)
        return fa, fb

    def forward(self, x, targets, V):
        wa = F.softplus(self.log_wa); wb = F.softplus(self.log_wb)
        qa, pa = self.qa(x), self.pa(x)
        qb, pb = self.qb(x), self.pb(x)
        dt = self.dt
        traj = []
        if self.mode == "symplectic":
            # leapfrog (velocity Verlet) — volume-preserving, energy-conserving
            fa, fb = self._force(qa, qb, wa, wb)
            for _ in range(self.k):
                pa = pa + 0.5 * dt * fa
                pb = pb + 0.5 * dt * fb
                qa = qa + dt * pa
                qb = qb + dt * pb
                fa, fb = self._force(qa, qb, wa, wb)
                pa = pa + 0.5 * dt * fa
                pb = pb + 0.5 * dt * fb
                traj.append(torch.cat([qa, pa, qb, pb], dim=1))
        else:
            # dissipative: gradient descent on H (ABLATION-2) — loses orbit invariant
            for _ in range(self.k):
                fa, fb = self._force(qa, qb, wa, wb)
                qa = qa + dt * fa           # descend potential (no momentum half-kicks)
                qb = qb + dt * fb
                pa = pa * 0.9; pb = pb * 0.9  # damp momenta -> settle to a basin
                traj.append(torch.cat([qa, pa, qb, pb], dim=1))
        action = torch.stack(traj, 0).mean(0)        # time-pooled (B,4dim,T) joint invariant
        logits = self.head(action)                   # (B,V,T)
        ce = F.cross_entropy(logits.transpose(1, 2).reshape(-1, V), targets.reshape(-1))
        return ce


class HamCLM(nn.Module):
    """CLMConvMoE (PRODUCTION additive readout retained) + Hamiltonian binding aux."""
    def __init__(self, cfg, arm):
        super().__init__()
        self.base = CLMConvMoE(cfg)              # production trunk + additive readout
        self.cfg = cfg
        couple = 0.0 if arm == "ctrl" else HAM_COUPLE
        mode = "dissipative" if arm == "diss" else "symplectic"
        self.binder = HamiltonianBinder(cfg.d_model, cfg.vocab_size,
                                        couple=couple, mode=mode)

    @property
    def moe(self):
        return self.base.moe

    def _trunk_feat(self, tokens):
        b = self.base
        x = b.embed(tokens).transpose(1, 2)
        x = b.embed_conv(x)
        for layer in b.trunk:
            x = layer(x)
        x, stats = b.moe(x)
        x = b.norm_out(x)                        # (B,C,T) shared bound representation
        return x, stats

    def forward(self, tokens, targets=None):
        x, stats = self._trunk_feat(tokens)
        logits = self.base.readout(x)            # PRODUCTION additive readout (engine-native)
        out = {"logits": logits, "usage": stats.usage,
               "aux_loss": stats.aux_loss, "routing_entropy": stats.entropy}
        if targets is not None:
            ce = F.cross_entropy(logits.transpose(1, 2).reshape(-1, self.cfg.vocab_size),
                                 targets.reshape(-1))
            bind_ce = self.binder(x, targets, self.cfg.vocab_size)
            out["ce_loss"] = ce
            out["bind_ce"] = bind_ce
            out["loss"] = ce + stats.aux_loss + BIND_LAMBDA * bind_ce
        return out

    @torch.no_grad()
    def num_params(self):
        return sum(p.numel() for p in self.parameters())


# ════════════════════════════════════════════════════════════════════════════
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--arm", required=True, choices=["arm", "ctrl", "diss"])
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
    ap.add_argument("--log-every", type=int, default=50)
    ap.add_argument("--out", default="")
    ap.add_argument("--ckpt-out", default="")
    ap.add_argument("--gauges-out", default="")
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

    print(f"=== H_1640 HAMILTONIAN-BIND 303M arm={a.arm} seed={a.seed} ===", flush=True)
    print(f"  device={device} d={d} L={L} E0={e0} Emax={emax} seq_len={seq_len} "
          f"steps={steps} bs={a.batch_size} sample={a.sample} "
          f"bind_lambda={BIND_LAMBDA} ham_K={HAM_K} ham_dim={HAM_DIM}", flush=True)
    if device == "cuda":
        cap = torch.cuda.get_device_capability()
        print(f"  cuda: {torch.cuda.get_device_name(0)} cap={cap[0]}.{cap[1]} "
              f"torch={torch.__version__}", flush=True)

    torch.manual_seed(a.seed)
    cfg = CLMConfig(n_experts=emax, n_trunk_layers=L, d_model=d, kernel_size=K,
                    variant="AB", dilation_base=2, max_dilation=512)
    model = HamCLM(cfg, a.arm).to(device)
    core = model.base
    n_params = model.num_params()
    print(f"  params: {n_params} ({n_params/1e6:.3f}M) (incl. training-only binder)", flush=True)

    mito = T.MitosisMoE(core, e0, emax)
    T.install_router_mask(core, mito)
    opt = torch.optim.AdamW(model.parameters(), lr=a.lr, betas=(0.9, 0.999),
                            eps=1e-8, weight_decay=0.0)
    gen = torch.Generator().manual_seed(42)
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

    model.train()
    t0 = time.time(); loss0 = lossF = None; last_bind = None
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
        last_bind = float(out["bind_ce"].detach()) if "bind_ce" in out else None
        if loss0 is None: loss0 = ce
        lossF = ce
        do_val = a.val_every > 0 and (step == 1 or step % a.val_every == 0 or step == steps)
        if step == 1 or step % a.log_every == 0 or step == steps:
            vtxt = ""
            if do_val:
                per = val_per_cell()
                vc = (sum(per.values()) / len(per)) if per else float("nan")
                vtxt = f"  val_CE={vc:.5f}"
            btxt = f" bind_CE={last_bind:.4f}" if last_bind is not None else ""
            print(f"  step {step:5d}  CE={ce:.5f}{btxt}  E={mito.e_active}  "
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

    sd_full = {k: v.detach().cpu() for k, v in model.state_dict().items()}
    if a.ckpt_out:
        torch.save(sd_full, a.ckpt_out)
        print(f"  torch ckpt -> {a.ckpt_out} ({os.path.getsize(a.ckpt_out)} bytes)", flush=True)

    summary = {"arm": a.arm, "seed": a.seed, "n_params": n_params,
               "loss0": round(loss0, 5), "lossF": round(lossF, 5),
               "bind_ce_final": (round(last_bind, 5) if last_bind is not None else None),
               "wall_s": round(wall, 1), "uniform_ce": round(uniform, 5),
               "final_val_ce_pooled": (round(final_val, 5) if final_val else None),
               "registers_descent": f"{n_desc}/{len(per)}",
               "heldout_descent": descent,
               "tier": "engine-native-eligible (.clm additive readout retained; binder dropped)"}
    if a.gauges_out:
        with open(a.gauges_out, "w") as f:
            json.dump(summary, f, ensure_ascii=False, indent=2)
        print(f"  summary -> {a.gauges_out}", flush=True)

    # ── serialize .clm v0.3 — PRODUCTION additive readout only (binder DROPPED) ──
    if a.out:
        e_ser = mito.e_active
        # strip binder.* and base. prefix -> plain CLMConvMoE state_dict
        base_sd = {}
        for k, vv in sd_full.items():
            if not k.startswith("base."):
                continue                          # drop binder.* (training-only)
            bk = k[len("base."):]
            base_sd[bk] = vv
        sd_active = {}
        for k, vv in base_sd.items():
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
