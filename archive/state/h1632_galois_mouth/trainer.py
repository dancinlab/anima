#!/usr/bin/env python3
"""H_1632 — Galois-closure concept-lattice binding mouth (FCA meet/join), 303M.

PREREG card: HYPOTHESES/cards/H_1632_galois_lattice_meet_bind.md

Mechanism (per card):
  Formal Concept Analysis. One leg projects to an object/extent indicator set, the other
  to an attribute/intent indicator set (sparse sigmoid gates). The bind is the Galois
  closure: intent = attributes shared by ALL gated objects (a soft AND-pool over objects),
  extent = objects having ALL gated attributes (soft AND-pool over attributes); iterate
  the two derivation operators to a fixpoint = a formal concept = a closed (extent,intent)
  pair. Composition = lattice MEET (intersection of intents), associative + idempotent,
  in one pass via 1-2 closure iterations.

  The AND-pool (conjunction) is the load-bearing operator: realized as a soft-min /
  log-product over the gated set (vs the OR/softmax sum of attention). A bound concept
  persists only if ALL its attributes hold -> distinct conjunctions stay distinct through
  depth; idempotence (closure o closure = closure) means no drift. Recombination crosses
  because a novel conjunction is just a new closed set in the same lattice.

SERIALIZATION (.clm-safe, same pattern as H_1640/1641):
  The closure layer + its byte head are TRAINING-ONLY (auxiliary loss L_bind shaping the
  shared trunk). The PRODUCTION additive readout Conv1d(d->V) is RETAINED for byte
  generation and serializes -> .clm engine-native loadable. The closure binder is DROPPED
  before serialize.

ARMS (frozen, PREREG · card ablation):
  arm    : meet-pool   AND-pool = soft-min (log-product of gates) -> conjunction.
  orpool : ABLATION    AND-pool -> OR-pool (sum / softmax, as attention) -> conjunctive
           separation collapses -> recombination to baseline (INERT).
  k1     : ABLATION    1 derivation step (no closure-to-fixpoint).
All arms share IDENTICAL trunk init seed / data / steps / production readout.

USAGE:
  python3 trainer.py --arm {arm,orpool,k1} --seed N --corpus <4 paths> \\
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
N_OBJ = 16                 # objects (extent universe)
N_ATTR = 16                # attributes (intent universe)
CLOSURE_K = 2              # derivation iterations to closure (card: 1-2)
ANDPOOL_BETA = 8.0         # soft-min sharpness (higher = harder AND)


class GaloisBinder(nn.Module):
    """Galois-closure concept-lattice binding aux head (TRAINING-ONLY).

    Two legs project to object-gates g_obj (extent) and attribute-gates g_attr (intent),
    plus a learned formal context I (object x attribute incidence). Galois derivation:
      intent'  = AND-pool over gated objects of I            (attrs shared by ALL objects)
      extent'  = AND-pool over gated attrs of I^T            (objs having ALL attrs)
    iterate K times to a closed (extent,intent). AND-pool = soft-min (log-product); OR-pool
    ablation = mean/softmax (no conjunction). The closed concept -> head -> next-byte aux CE.
    """
    def __init__(self, d, V, n_obj=N_OBJ, n_attr=N_ATTR, k=CLOSURE_K, mode="arm"):
        super().__init__()
        self.n_obj, self.n_attr, self.mode = n_obj, n_attr, mode
        self.k = 1 if mode == "k1" else k
        self.or_pool = (mode == "orpool")
        self.g_obj = nn.Conv1d(d, n_obj, 1)            # extent gates (leg A)
        self.g_attr = nn.Conv1d(d, n_attr, 1)          # intent gates (leg B)
        # learned formal context incidence I (n_obj x n_attr), shared (not per-position)
        self.I = nn.Parameter(torch.randn(n_obj, n_attr) * 0.1)
        self.head = nn.Conv1d(n_obj + n_attr, V, 1)    # closed concept -> byte logits

    def _and_pool(self, gates, incid):
        """gates: (B,n_src,T) sigmoid weights over source set; incid: (n_src,n_tgt).
        Soft AND-pool over the gated source dim -> (B,n_tgt,T): attribute/object is in the
        derived set only if (softly) ALL gated sources have it. Realized via a weighted
        log-product (soft-min). OR-pool ablation = weighted mean (softmax-like sum)."""
        # per (src,tgt) presence prob p in [0,1]
        p = torch.sigmoid(incid)                        # (n_src,n_tgt)
        g = torch.sigmoid(gates)                        # (B,n_src,T)
        if self.or_pool:
            # OR / sum pooling (attention-like): tgt present if ANY gated src has it
            # weighted mean over sources
            num = torch.einsum("bst,sg->bgt", g, p)
            den = g.sum(dim=1, keepdim=True) + 1e-6
            return num / den                            # (B,n_tgt,T)
        # AND pooling: log-product weighted by gate -> tgt present iff ALL gated srcs have it
        # derived[g] = prod_s p[s,g]^{gate[s]} = exp( sum_s gate[s] * log p[s,g] )
        logp = torch.log(p + 1e-6)                      # (n_src,n_tgt)
        acc = torch.einsum("bst,sg->bgt", g, logp)      # (B,n_tgt,T)
        return torch.exp(ANDPOOL_BETA * acc / (g.sum(dim=1, keepdim=True) + 1e-6))

    def forward(self, x, targets, V):
        B, _, Tt = x.shape
        extent = self.g_obj(x)                          # (B,n_obj,T)
        intent = self.g_attr(x)                         # (B,n_attr,T)
        for _ in range(self.k):
            # intent' = attrs shared by ALL gated objects (AND-pool over objects of I)
            new_intent = self._and_pool(extent, self.I)             # (B,n_attr,T)
            # extent' = objs having ALL gated attrs (AND-pool over attrs of I^T)
            new_extent = self._and_pool(intent, self.I.t())         # (B,n_obj,T)
            extent, intent = new_extent, new_intent
        concept = torch.cat([extent, intent], dim=1)    # (B,n_obj+n_attr,T)
        logits = self.head(concept)                     # (B,V,T)
        ce = F.cross_entropy(logits.transpose(1, 2).reshape(-1, V), targets.reshape(-1))
        return ce


class BindCLM(nn.Module):
    """CLMConvMoE (PRODUCTION additive readout retained) + galois binding aux."""
    def __init__(self, cfg, arm):
        super().__init__()
        self.base = CLMConvMoE(cfg)
        self.cfg = cfg
        self.binder = GaloisBinder(cfg.d_model, cfg.vocab_size, mode=arm)

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
    ap.add_argument("--arm", required=True, choices=["arm", "orpool", "k1"])
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

    print(f"=== H_1632 GALOIS-MEET-BIND 303M arm={a.arm} seed={a.seed} ===", flush=True)
    print(f"  device={device} d={d} L={L} E0={e0} Emax={emax} seq_len={seq_len} "
          f"steps={steps} bs={a.batch_size} sample={a.sample} "
          f"bind_lambda={BIND_LAMBDA} n_obj={N_OBJ} n_attr={N_ATTR} "
          f"closure_K={CLOSURE_K} beta={ANDPOOL_BETA}", flush=True)
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
