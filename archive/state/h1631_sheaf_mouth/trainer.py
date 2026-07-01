#!/usr/bin/env python3
"""H_1631 — Sheaf-gluing binding mouth (local sections -> global consistency), 303M.

PREREG card: UNIVERSE/cards/H_1631_sheaf_section_glue_bind.md

Mechanism (per card):
  Treat the cell/feature sequence as a graph with a cover: positions/roles = nodes,
  role-edges = overlaps. Each node carries a local stalk vector; each edge carries a
  learned low-rank RESTRICTION map R_{i->e}. The bind (one pass, K Jacobi steps) drives
  node features whose restrictions AGREE on shared edges, i.e. minimizes
  Sum_edges || R_{i->e} x_i - R_{j->e} x_j ||^2 (sheaf-Laplacian consistency). The
  consistent global section IS the bound composite; the residual disagreement
  (coboundary norm) is an explicit MONITOR-ONLY 'failed-to-bind' signal (NOT added to loss).

  Implemented with N role-nodes, a fixed ring/complete edge set, per-edge low-rank
  restriction maps, K Jacobi iterations toward the sheaf-Laplacian fixed point. The
  glued node features are concatenated and a head predicts the next byte -> aux CE.

SERIALIZATION (.clm-safe, same pattern as H_1640/1641):
  The sheaf layer + its byte head are TRAINING-ONLY (auxiliary loss L_bind shaping the
  shared trunk). The PRODUCTION additive readout Conv1d(d->V) is RETAINED for byte
  generation and serializes -> .clm engine-native loadable. The sheaf binder is DROPPED
  before serialize.

ARMS (frozen, PREREG · card ablation):
  arm    : full sheaf (learned low-rank restriction maps R, K Jacobi consistency iters).
  ident  : ABLATION  R = identity -> sheaf collapses to plain graph-Laplacian smoothing
           (= vanilla message passing) -> recombination should drop to baseline (INERT).
  k1     : ABLATION  K=1 Jacobi step (no settling toward global consistency).
All arms share IDENTICAL trunk init seed / data / steps / production readout.

USAGE:
  python3 trainer.py --arm {arm,ident,k1} --seed N --corpus <4 paths> \\
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

# frozen hyperparams (pre-registered — tune-to-green forbidden)
BIND_LAMBDA = 1.0          # weight of the binding aux-loss
N_NODES = 4                # role-nodes in the cover (card: 4-node role graph)
STALK_DIM = 32             # local stalk vector width per node
RESTRICT_RANK = 16         # low-rank restriction map dim on edges
JACOBI_K = 3               # Jacobi consistency iterations (card: 1-2, use 3 full)
JACOBI_ETA = 0.5           # Jacobi step size


class SheafBinder(nn.Module):
    """Sheaf-gluing binding aux head (TRAINING-ONLY).

    N node stalks projected from the trunk feature; a fixed complete edge set with
    learned low-rank restriction maps R_e (per edge, per endpoint). K Jacobi steps drive
    each node toward agreement of restrictions on shared edges (sheaf-Laplacian descent).
    The glued nodes -> head -> next-byte aux CE. ident ablation forces R=I (plain
    Laplacian); k1 ablation uses a single Jacobi step (no global settling).
    """
    def __init__(self, d, V, n=N_NODES, sdim=STALK_DIM, rank=RESTRICT_RANK,
                 k=JACOBI_K, mode="arm"):
        super().__init__()
        self.n, self.sdim, self.rank, self.mode = n, sdim, rank, mode
        self.k = 1 if mode == "k1" else k
        self.identity_restrict = (mode == "ident")
        # project trunk feature -> n node stalks
        self.node_proj = nn.Conv1d(d, n * sdim, 1)
        # edge list (complete undirected graph over n nodes)
        edges = [(i, j) for i in range(n) for j in range(i + 1, n)]
        self.edges = edges
        # per-edge per-endpoint low-rank restriction maps  R: sdim -> rank
        # stored as (n_edges, 2, rank, sdim)
        ne = len(edges)
        self.R = nn.Parameter(torch.randn(ne, 2, rank, sdim) * (1.0 / math.sqrt(sdim)))
        self.head = nn.Conv1d(n * sdim, V, 1)

    def _restrict(self, e_idx, endpoint, x):
        # x: (B,sdim,T) ; map -> (B,rank,T)
        if self.identity_restrict:
            # plain Laplacian: identity restriction (pad/truncate sdim->rank)
            if self.rank <= self.sdim:
                return x[:, :self.rank, :]
            return F.pad(x, (0, 0, 0, self.rank - self.sdim))
        Rm = self.R[e_idx, endpoint]                  # (rank,sdim)
        return torch.einsum("rs,bst->brt", Rm, x)

    def forward(self, x, targets, V):
        B, _, Tt = x.shape
        nodes = self.node_proj(x).view(B, self.n, self.sdim, Tt)    # (B,n,sdim,T)
        for _ in range(self.k):
            upd = torch.zeros_like(nodes)
            for ei, (i, j) in enumerate(self.edges):
                ri = self._restrict(ei, 0, nodes[:, i])             # (B,rank,T)
                rj = self._restrict(ei, 1, nodes[:, j])             # (B,rank,T)
                disagree = ri - rj                                  # coboundary on edge
                # push i down-gradient, j up-gradient (back through restriction^T)
                if self.identity_restrict:
                    gi = F.pad(disagree, (0, 0, 0, self.sdim - self.rank)) \
                        if self.sdim > self.rank else disagree[:, :self.sdim, :]
                    gj = gi
                else:
                    gi = torch.einsum("rs,brt->bst", self.R[ei, 0], disagree)
                    gj = torch.einsum("rs,brt->bst", self.R[ei, 1], disagree)
                upd[:, i] = upd[:, i] - JACOBI_ETA * gi
                upd[:, j] = upd[:, j] + JACOBI_ETA * gj
            nodes = nodes + upd
        glued = nodes.reshape(B, self.n * self.sdim, Tt)
        logits = self.head(glued)
        ce = F.cross_entropy(logits.transpose(1, 2).reshape(-1, V), targets.reshape(-1))
        return ce


class BindCLM(nn.Module):
    """CLMConvMoE (PRODUCTION additive readout retained) + sheaf binding aux."""
    def __init__(self, cfg, arm):
        super().__init__()
        self.base = CLMConvMoE(cfg)
        self.cfg = cfg
        self.binder = SheafBinder(cfg.d_model, cfg.vocab_size, mode=arm)

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
        x = b.norm_out(x)
        return x, stats

    def forward(self, tokens, targets=None):
        x, stats = self._trunk_feat(tokens)
        logits = self.base.readout(x)                # PRODUCTION additive readout
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


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--arm", required=True, choices=["arm", "ident", "k1"])
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

    print(f"=== H_1631 SHEAF-GLUE-BIND 303M arm={a.arm} seed={a.seed} ===", flush=True)
    print(f"  device={device} d={d} L={L} E0={e0} Emax={emax} seq_len={seq_len} "
          f"steps={steps} bs={a.batch_size} sample={a.sample} "
          f"bind_lambda={BIND_LAMBDA} nodes={N_NODES} stalk={STALK_DIM} "
          f"rank={RESTRICT_RANK} jacobi_K={JACOBI_K}", flush=True)
    if device == "cuda":
        cap = torch.cuda.get_device_capability()
        print(f"  cuda: {torch.cuda.get_device_name(0)} cap={cap[0]}.{cap[1]} "
              f"torch={torch.__version__}", flush=True)

    torch.manual_seed(a.seed)
    cfg = CLMConfig(n_experts=emax, n_trunk_layers=L, d_model=d, kernel_size=K,
                    variant="AB", dilation_base=2, max_dilation=512)
    model = BindCLM(cfg, a.arm).to(device)
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

    if a.out:
        e_ser = mito.e_active
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
