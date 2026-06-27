#!/usr/bin/env python3
"""H_1602 RECOMB-OBJECTIVE 303M — objective-as-G1-lever (see PREREG.md).

Trains THREE arms of the production 303M CLMConvMoE that share an IDENTICAL trunk
AND IDENTICAL production additive readout (Conv1d d->V), differing ONLY in the
TRAINING OBJECTIVE:

  ce_marginal            : standard CE next-byte marginal likelihood (baseline /
                           discriminating control — CE does not reward conjunction,
                           the gauge null).
  infonce                : CE + lambda * InfoNCE/contrastive-predictive term
                           (positive=true byte, negatives sampled from corpus).
  contrastive_equilibrium: CE + lambda * margin(E_pos - E_neg) equilibrium-prop
                           style (positive phase = true seq, negative phase =
                           model-sampled seq; push energies apart).

Because ALL arms keep the production additive readout, ALL arms are .clm-
serializable -> engine-native G1 is by-construction OPEN (unlike exp3 bind which
was BLOCKED). torch-side metrics here are DIRECTIONAL monitors; the .clm export
+ engine-native G1 (anima eval / clm_decode.py) is the terminal path.

Canonical recipe (savant golden-zone inhibition + mitosis E2->E3 split + 4-cell
register corpus + held-out val) is REUSED verbatim from cli/train.py so the only
intended difference between arms is the objective.

USAGE:
  python3 trainer.py --objective {ce_marginal,infonce,contrastive_equilibrium} \\
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
INFONCE_LAMBDA = 1.0
EQ_LAMBDA = 1.0
EQ_MARGIN = 0.5
INFONCE_NEG = 64          # negatives per position drawn from the in-batch byte pool


# ════════════════════════════════════════════════════════════════════════════
#  Objective heads — all consume the SAME production logits (B,V,T); no trunk or
#  readout difference. Only the LOSS computed from (logits, targets) differs.
# ════════════════════════════════════════════════════════════════════════════
def _ce(logits, targets, V):
    return F.cross_entropy(logits.transpose(1, 2).reshape(-1, V),
                           targets.reshape(-1))


def loss_ce_marginal(logits, targets, V, gen):
    """Standard CE next-byte. Baseline / discriminating control."""
    return _ce(logits, targets, V), {}


def loss_infonce(logits, targets, V, gen):
    """CE + InfoNCE contrastive-predictive term.

    For each position the model's logit vector is the score over the V-way byte
    vocabulary. InfoNCE contrasts the score of the TRUE next byte (positive)
    against a sampled set of negatives drawn from the actual byte pool. This is
    the V-class softmax restricted to {positive} U {negatives} — it rewards the
    representation for SEPARATING the true continuation from plausible decoys,
    a predictive-coding pressure CE-marginal does not impose per-position."""
    ce = _ce(logits, targets, V)
    B, _V, Tt = logits.shape
    lg = logits.transpose(1, 2).reshape(-1, V)      # (N, V)
    tgt = targets.reshape(-1)                        # (N,)
    N = tgt.shape[0]
    pos = lg.gather(1, tgt.unsqueeze(1))             # (N,1) true-byte score
    # negatives: random bytes (uniform over V), masked off if they collide w/ pos
    neg_idx = torch.randint(0, V, (N, INFONCE_NEG), generator=gen,
                            device=lg.device)        # (N, K)
    neg = lg.gather(1, neg_idx)                      # (N, K) negative scores
    collide = (neg_idx == tgt.unsqueeze(1))
    neg = neg.masked_fill(collide, float("-inf"))
    cand = torch.cat([pos, neg], dim=1)             # (N, 1+K) positive at col 0
    infonce = F.cross_entropy(cand, torch.zeros(N, dtype=torch.long,
                                                device=lg.device))
    return ce + INFONCE_LAMBDA * infonce, {"infonce": float(infonce.detach())}


def loss_contrastive_equilibrium(logits, targets, V, gen):
    """CE + margin(E_pos - E_neg) equilibrium-prop style.

    E_pos = mean per-token NLL of the TRUE sequence under the model (positive
    phase energy). E_neg = mean per-token NLL the model assigns to a NEGATIVE
    sequence sampled from its OWN predictive distribution (negative phase, a
    model-imagined continuation). The objective pushes the model to assign LOWER
    energy to the true sequence than to its own sample by at least EQ_MARGIN —
    a contrastive-divergence pressure that (unlike marginal CE) explicitly
    separates real conjunctions from self-generated ones."""
    ce = _ce(logits, targets, V)
    B, _V, Tt = logits.shape
    lg = logits.transpose(1, 2).reshape(-1, V)      # (N, V)
    tgt = targets.reshape(-1)
    logp = F.log_softmax(lg, dim=1)                 # (N, V)
    e_pos = -logp.gather(1, tgt.unsqueeze(1)).mean()        # positive-phase energy
    with torch.no_grad():
        probs = logp.exp()
        samp = torch.multinomial(probs, 1, generator=gen).squeeze(1)   # (N,)
    e_neg = -logp.gather(1, samp.unsqueeze(1)).mean()       # negative-phase energy
    # margin loss: want e_pos + margin <= e_neg  ->  relu(e_pos - e_neg + margin)
    eq = F.relu(e_pos - e_neg + EQ_MARGIN)
    return ce + EQ_LAMBDA * eq, {"e_pos": float(e_pos.detach()),
                                 "e_neg": float(e_neg.detach()),
                                 "eq": float(eq.detach())}


OBJECTIVES = {
    "ce_marginal": loss_ce_marginal,
    "infonce": loss_infonce,
    "contrastive_equilibrium": loss_contrastive_equilibrium,
}


# ════════════════════════════════════════════════════════════════════════════
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--objective", required=True, choices=list(OBJECTIVES))
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

    print(f"=== H_1602 RECOMB-OBJECTIVE 303M obj={a.objective} seed={a.seed} ===", flush=True)
    print(f"  device={device} d={d} L={L} E0={e0} Emax={emax} seq_len={seq_len} "
          f"steps={steps} bs={a.batch_size} sample={a.sample}", flush=True)
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

    mito = T.MitosisMoE(model, e0, emax)
    T.install_router_mask(model, mito)
    opt = torch.optim.AdamW(model.parameters(), lr=a.lr, betas=(0.9, 0.999),
                            eps=1e-8, weight_decay=0.0)
    gen = torch.Generator().manual_seed(42)        # data RNG SHARED across arms (fair)
    val_gen = torch.Generator().manual_seed(1234)
    # objective RNG (negatives / neg-phase sampling) — device-resident, seeded fair
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

    @torch.no_grad()
    def cell_val_ce(c):
        # held-out CE is ALWAYS plain marginal CE (fair, arm-independent — the
        # objective changes TRAIN pressure, not the generalization metric).
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
        if a.bf16 and device == "cuda":
            with torch.autocast("cuda", dtype=torch.bfloat16):
                out = model(x, y)
                obj_loss, aux = objfn(out["logits"].float(), y, V, obj_gen)
                loss = obj_loss + out["aux_loss"]
            loss.backward()
        else:
            out = model(x, y)
            obj_loss, aux = objfn(out["logits"], y, V, obj_gen)
            loss = obj_loss + out["aux_loss"]
            loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        opt.step()
        ce = float(out["ce_loss"].detach())        # plain CE always logged (comparable)
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
               "gauges_g1g6_torch_probe": gauges,
               "tier": "engine-native-eligible (.clm additive); torch probe DIRECTIONAL"}
    if a.gauges_out:
        with open(a.gauges_out, "w") as f:
            json.dump(summary, f, ensure_ascii=False, indent=2)
        print(f"  summary -> {a.gauges_out}", flush=True)

    # ── serialize .clm v0.3 (ALL arms — production additive readout) ──────────
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
