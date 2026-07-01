#!/usr/bin/env python3
"""H_1630 REG-DICTAUX 303M — objective-side G1/G6 levers (see PREREG.md).

Trains arms of the production 303M CLMConvMoE that share an IDENTICAL trunk AND
the IDENTICAL production additive readout (Conv1d d->V). Every lever here acts on
the TRAINING SIGNAL / REGULARIZATION / DIAGNOSTIC side, NOT on the readout. That
is deliberate: this session's engine-native A/B closed the multiplicative binding
READOUT as NOT-SUPPORTED (floor), and the external literature (RESEARCH.md §6,
Furrer 2020 / Barin Pacela 2026 / Doshi-Gromov 2023) converges on the real G1
lever being the trunk OBJECTIVE + REGULARIZATION, not an architecture operator.

Because ALL arms keep the production additive readout, ALL arms are .clm-
serializable -> engine-native G1/G6 is by-construction OPEN. torch-side training
metrics are DIRECTIONAL monitors only; the .clm export + engine-native G0-G6
(core/g_gates.py <- core/clm_decode.py, torch-free numpy decode = TERMINAL) is
the verdict path (a_engine_native_learning). This trainer file itself stays
torch-only-for-TRAINING; NO scoring is done here (grep self-check: this file
imports torch for the train loop, but emits no G1/G6 verdict — measurement is the
official engine CLI).

LEVERS (each = one --arm value; baseline = ce_marginal control):
  ce_marginal   : standard CE next-byte (BASELINE / discriminating control).
  n6_grok       : N6 grokking — wider weight-decay/dropout band x longer-step
                  schedule around savant golden-zone GZ_LOWER~0.212. Pure
                  regularization+step lever (no extra loss term). Excludes the
                  "undertrain floor" confound (Doshi/Gromov 2023, 2310.13061 /
                  Verma 2026, 2605.20441).
  n7_dictaux    : N7 Stop-Probing — trunk-penultimate (norm_out features) sparse-
                  coding / dictionary-learning AUX LOSS at small lambda. Encodes
                  "binding = a learned representation (dictionary direction)" as
                  an objective term (Barin Pacela 2026, 2603.28744).
  n6n7          : N6 + N7 combined (regularization band + dict-aux), the primary
                  proposed cheap lever in RESEARCH.md §92 제언1.
  n1_tlora      : N1 TensorPoly/TLoRA — reparameterize each MoE expert's conv
                  weight as a tensor-product (low-rank outer product) factor and
                  route over it. Puts the TPR at the expert WEIGHT (not the dead
                  readout). (2405.16671). Optional, off the cheap path.
  n8_jamo       : N8 SCRIPT — Korean Jamo subcharacter compositional TEACH SIGNAL
                  as an aux loss: predict the leading-Jamo class of the next byte
                  from trunk features (cheap aux head, dropped at serialize).
                  (2604.12377; ko-jamo-mitosis H_1316/1321 lineage). Optional.

DIAGNOSTIC (orthogonal, --dbes flag, any arm):
  N3 DBES expert-specialization metric — logged at end (does the ConvMoE actually
  differentiate experts?). Measurement-only; isolates "recomb fails because
  experts never specialized." (2605.18523). No effect on training.

SEARCH (orthogonal, --n4-set-search K, eval side only — recorded in summary):
  N4 diverse-set-search hint — record top-K diverse continuations from the final
  model (Si 2024 diversity bottleneck). Heavy generation belongs to the GPU eval
  on 303M; here we only emit the toggle into the summary for the launch spec.

USAGE (303M canonical):
  python3 trainer.py --arm n6n7 --seed 4307 --canon \\
      --corpus <ko-gen> <en-gen> <ko-sns> <en-sns> \\
      --cell-label ko-general en-general ko-sns en-sns \\
      --sample proportional --steps 4000 --val-frac 0.05 --val-every 200 \\
      --dbes --out ckpt/n6n7_seed4307.clm --ckpt-out ckpt/n6n7_seed4307.pt \\
      --gauges-out ckpt/n6n7_seed4307.json

USAGE (CPU smoke):
  python3 trainer.py --arm n6n7 --seed 1 --steps 4 --d 16 --L 2 --seq-len 32 \\
      --batch-size 2 --no-mitosis --out ckpt/smoke.clm
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

from model import CLMConfig, CLMConvMoE                         # train/clm/model/model.py
import clm_serialize_v2 as S                                    # serialize_v3 (ground truth)
import verify_clm_v2 as VC                                      # clm_decodable / descent
import train as T                                               # cli/train.py (recipe levers)

# ════════════════════════════════════════════════════════════════════════════
#  FROZEN hyperparameters (pre-registered in PREREG.md — tune-to-green 금지).
# ════════════════════════════════════════════════════════════════════════════
# N7 dictionary-learning aux: small lambda; over-complete factor; L1 sparsity on
# the codes; reconstruct norm_out features from a learned dictionary D.
DICT_LAMBDA = 0.05          # weight of the dict-aux loss added to CE
DICT_FACTOR = 4             # dictionary atoms = DICT_FACTOR * d_model (over-complete)
DICT_L1 = 0.001            # L1 sparsity coefficient on the codes
# N6 grokking band: weight-decay/dropout pushed a notch ABOVE the default savant
# map so regularization clears the memorization floor (Doshi/Gromov 2023). The
# default lever is inhibition_to_wd(inh)=inh*0.1; N6 widens the cap.
N6_WD_GAIN = 2.0           # multiply the savant-derived weight-decay by this
N6_DROP_CAP = 0.30         # dropout cap during the N6 band (vs default <=0.5)
# N8 Jamo teach-signal: Korean leading-consonant (초성) class as a cheap aux head.
JAMO_LAMBDA = 0.05
JAMO_N_CLASSES = 20        # 19 leading consonants (초성) + 1 "not-a-Jamo-lead" bucket


# ════════════════════════════════════════════════════════════════════════════
#  N7 — dictionary-learning aux head over trunk-penultimate (norm_out) features.
#  A learned over-complete dictionary D (d x M); codes c = relu(D^T h); recon
#  h_hat = D c. Loss = ||h - h_hat||^2 + L1 * ||c||_1. Encodes "binding lives in
#  a learned sparse dictionary direction" as a trunk objective (Barin Pacela 26).
#  The head is NOT serialized into the .clm (the .clm only stores the production
#  additive readout); it only shapes the trunk during training.
# ════════════════════════════════════════════════════════════════════════════
class DictAuxHead(nn.Module):
    def __init__(self, d: int, factor: int = DICT_FACTOR):
        super().__init__()
        m = factor * d
        self.enc = nn.Linear(d, m, bias=False)      # code inference (probe)
        self.dec = nn.Linear(m, d, bias=False)      # dictionary D (atoms = cols)

    def forward(self, h):                            # h: (B, d, T)
        x = h.transpose(1, 2)                        # (B, T, d)
        c = F.relu(self.enc(x))                      # sparse codes (B, T, M)
        recon = self.dec(c)                          # (B, T, d)
        recon_err = F.mse_loss(recon, x)
        sparsity = c.abs().mean()
        return recon_err + DICT_L1 * sparsity, {
            "dict_recon": float(recon_err.detach()),
            "dict_sparsity": float(sparsity.detach())}


# ════════════════════════════════════════════════════════════════════════════
#  N8 — Korean Jamo (초성 leading-consonant) teach-signal aux head.
#  Maps each TARGET byte to a leading-consonant class via the precomputed table,
#  then a tiny linear head predicts that class from trunk features. Teaches the
#  trunk the subcharacter compositional structure (SCRIPT 2026) cheaply. Dropped
#  at serialize. Bytes that are not the lead byte of a Hangul syllable map to the
#  "other" bucket (class 0) so the head is harmless on en/sns registers.
# ════════════════════════════════════════════════════════════════════════════
def _build_jamo_lut() -> torch.Tensor:
    """Per-byte -> 초성 class in [0, JAMO_N_CLASSES). Hangul syllables U+AC00..
    U+D7A3 are UTF-8 3-byte sequences EC..ED ..; the LEAD byte of a syllable
    block (0xEA..0xED) is mapped by its high range to a coarse 초성 bucket. This
    is an intentionally cheap byte-level proxy (V=256, no real codepoint decode)
    — exact 초성 needs 3-byte assembly; here the lead byte's value bucket is a
    sufficient *teach signal* (a_no_llm_frame_trap: cheap structural injection)."""
    lut = torch.zeros(256, dtype=torch.long)
    # Hangul-syllable UTF-8 lead bytes are 0xEA..0xED. Bucket them across classes
    # 1..19 by (byte - 0xEA)*K + spread so the head has a non-trivial target on
    # Korean text but is class-0 (other) elsewhere.
    for b in range(0xEA, 0xEE):
        lut[b] = 1 + ((b - 0xEA) % (JAMO_N_CLASSES - 1))
    # continuation bytes 0x80..0xBF carry the finer 초성/중성 distinction; spread
    # them over the remaining classes so the aux target varies within a syllable.
    for b in range(0x80, 0xC0):
        lut[b] = 1 + (b % (JAMO_N_CLASSES - 1))
    return lut


class JamoAuxHead(nn.Module):
    def __init__(self, d: int):
        super().__init__()
        self.head = nn.Conv1d(d, JAMO_N_CLASSES, 1)
        self.register_buffer("lut", _build_jamo_lut(), persistent=False)

    def forward(self, h, targets):                   # h:(B,d,T) targets:(B,T)
        logits = self.head(h)                        # (B, C, T)
        cls = self.lut.to(targets.device)[targets]   # (B, T)
        loss = F.cross_entropy(logits.reshape(-1, JAMO_N_CLASSES).contiguous()
                               if False else
                               logits.transpose(1, 2).reshape(-1, JAMO_N_CLASSES),
                               cls.reshape(-1))
        return loss, {"jamo_ce": float(loss.detach())}


# ════════════════════════════════════════════════════════════════════════════
#  N3 — DBES-style expert-specialization diagnostic. For a held batch, measure
#  per-expert routing usage entropy and pairwise expert-output divergence. High
#  divergence + balanced usage => experts specialized; near-zero => collapse
#  ("recomb fails because experts never differentiated"). Measurement-only.
# ════════════════════════════════════════════════════════════════════════════
@torch.no_grad()
def dbes_diagnostic(model, x):
    model.eval()
    out = model(x)
    usage = out["usage"].detach().float()            # (E,) routing mass per expert
    usage = usage / (usage.sum() + 1e-9)
    ent = float(-(usage * (usage + 1e-9).log()).sum())
    e_active = int((usage > 1e-4).sum())
    norm_ent = ent / math.log(max(2, e_active)) if e_active > 1 else 0.0
    return {"expert_usage": [round(float(u), 4) for u in usage.tolist()],
            "usage_entropy": round(ent, 4),
            "usage_entropy_norm": round(norm_ent, 4),
            "n_active_experts": e_active,
            "note": "DBES proxy: norm usage-entropy ~1 => balanced/specialized; "
                    "~0 => collapse onto one expert (recomb material absent)."}


# ════════════════════════════════════════════════════════════════════════════
#  N1 — TLoRA tensor-product expert factor. OFF the cheap path; documented +
#  wired as an OPTIONAL low-rank outer-product perturbation added to each MoE
#  expert conv weight. We do NOT replace the production expert (that would break
#  .clm serialization); instead we ADD a rank-r tensor-product term during
#  training so its effect folds into the production weight at serialize time
#  (the .clm sees only the summed production conv weight => still additive,
#  still engine-loadable). This realizes "TPR at the expert WEIGHT, not the
#  readout" (2405.16671) while preserving the engine-native verdict path.
# ════════════════════════════════════════════════════════════════════════════
class TLoRAExpertFactors(nn.Module):
    def __init__(self, model, rank: int = 8):
        super().__init__()
        self.factors = nn.ParameterList()
        self.targets = []
        for name, mod in model.named_modules():
            # MoE expert conv weights live under moe.experts.*; attach a low-rank
            # outer-product (a (out,r) x (r, in*k) tensor product) to each.
            if name.startswith("moe.experts.") and isinstance(mod, nn.Conv1d):
                w = mod.weight                       # (out, in, k)
                o, i, k = w.shape
                a = nn.Parameter(torch.zeros(o, rank))
                b = nn.Parameter(torch.randn(rank, i * k) * 0.01)
                self.factors.append(a); self.factors.append(b)
                self.targets.append((mod, a, b, (o, i, k)))

    def apply_into_weights(self):
        """Fold the tensor-product factor into each expert conv weight in-place
        (so a subsequent serialize sees the production additive weight)."""
        with torch.no_grad():
            for mod, a, b, (o, i, k) in self.targets:
                delta = (a @ b).reshape(o, i, k)
                mod.weight.add_(delta)

    def delta_norm(self):
        with torch.no_grad():
            return float(sum((a @ b).norm() for _m, a, b, _s in self.targets))


# ════════════════════════════════════════════════════════════════════════════
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--arm", required=True,
                    choices=["ce_marginal", "n6_grok", "n7_dictaux", "n6n7",
                             "n1_tlora", "n8_jamo"])
    ap.add_argument("--seed", type=int, default=4307)
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
    ap.add_argument("--tlora-rank", type=int, default=8)
    ap.add_argument("--no-savant", action="store_true")
    ap.add_argument("--no-mitosis", action="store_true")
    ap.add_argument("--bf16", action="store_true")
    ap.add_argument("--dbes", action="store_true", help="N3 expert-specialization diagnostic")
    ap.add_argument("--n4-set-search", type=int, default=0,
                    help="N4 diverse-set-search K hint (recorded in summary; gen on GPU eval)")
    ap.add_argument("--sample", choices=["roundrobin", "proportional"],
                    default="proportional")
    ap.add_argument("--val-frac", type=float, default=0.05)
    ap.add_argument("--val-every", type=int, default=200)
    ap.add_argument("--val-batches", type=int, default=4)
    ap.add_argument("--log-every", type=int, default=50)
    ap.add_argument("--out", default="", help=".clm path (all arms — additive readout)")
    ap.add_argument("--ckpt-out", default="", help="torch .pt state_dict path")
    ap.add_argument("--gauges-out", default="", help="summary json out")
    a = ap.parse_args()

    savant_on = not a.no_savant
    mitosis_on = not a.no_mitosis
    if a.canon:
        d = a.d or 3784; L = a.L or 4
        seq_len = a.seq_len or 1024; steps = a.steps or 4000
    else:
        d = a.d or 64; L = a.L or 2
        seq_len = a.seq_len or 128; steps = a.steps or 60
    e0, emax = a.e0, a.emax
    V, K = 256, 3
    device = "cuda" if torch.cuda.is_available() else "cpu"

    arm = a.arm
    want_n6 = arm in ("n6_grok", "n6n7")
    want_n7 = arm in ("n7_dictaux", "n6n7")
    want_n8 = arm == "n8_jamo"
    want_n1 = arm == "n1_tlora"

    print(f"=== H_1630 REG-DICTAUX 303M arm={arm} seed={a.seed} ===", flush=True)
    print(f"  device={device} d={d} L={L} E0={e0} Emax={emax} seq_len={seq_len} "
          f"steps={steps} bs={a.batch_size} sample={a.sample}", flush=True)
    print(f"  levers: N6_grok={want_n6} N7_dictaux={want_n7} N8_jamo={want_n8} "
          f"N1_tlora={want_n1} N3_dbes={a.dbes} N4_setsearch={a.n4_set_search}", flush=True)
    if device == "cuda":
        cap = torch.cuda.get_device_capability()
        print(f"  cuda: {torch.cuda.get_device_name(0)} cap={cap[0]}.{cap[1]} "
              f"torch={torch.__version__}", flush=True)

    torch.manual_seed(a.seed)

    cfg = CLMConfig(n_experts=emax, n_trunk_layers=L, d_model=d, kernel_size=K,
                    variant="AB", dilation_base=2, max_dilation=512)
    model = CLMConvMoE(cfg).to(device)             # production additive readout (all arms)

    # ── optional aux heads / factors (NOT serialized into .clm) ──────────────
    dict_head = DictAuxHead(d).to(device) if want_n7 else None
    jamo_head = JamoAuxHead(d).to(device) if want_n8 else None
    tlora = TLoRAExpertFactors(model, rank=a.tlora_rank).to(device) if want_n1 else None

    params = list(model.parameters())
    if dict_head is not None: params += list(dict_head.parameters())
    if jamo_head is not None: params += list(jamo_head.parameters())
    if tlora is not None: params += list(tlora.parameters())
    n_params = sum(p.numel() for p in model.parameters())
    print(f"  params(model)={n_params} ({n_params/1e6:.3f}M)  "
          f"aux_params={sum(p.numel() for p in params) - n_params}", flush=True)

    mito = T.MitosisMoE(model, e0, emax)
    T.install_router_mask(model, mito)
    opt = torch.optim.AdamW(params, lr=a.lr, betas=(0.9, 0.999),
                            eps=1e-8, weight_decay=0.0)
    gen = torch.Generator().manual_seed(42)        # data RNG SHARED across arms (fair)
    val_gen = torch.Generator().manual_seed(1234)

    latch = {"on": False, "at": 0}
    i0 = T.GZ_UPPER
    i_floor = T.GZ_LOWER - 0.05
    split_step = max(1, steps // 2)

    # ── intercept trunk-penultimate (norm_out) features for the aux heads ─────
    # We capture the norm_out output via a forward hook so we don't fork model.py.
    feat_box = {}
    if dict_head is not None or jamo_head is not None:
        def _hook(_m, _i, out):
            feat_box["h"] = out                     # (B, d, T) post GroupNorm
        model.norm_out.register_forward_hook(_hook)

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
        # lever changes TRAIN pressure, not the generalization metric).
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

    # ── N6 regularization band: widen savant-derived wd/dropout to clear floor ─
    def reg_for_step(step):
        if not savant_on:
            return 0.0, 0.0
        inh = T.savant_inhibition(step, steps, i0, i_floor, latch)
        wd = T.inhibition_to_wd(inh)
        dp = T.inhibition_to_dropout(inh)
        if want_n6:
            wd = wd * N6_WD_GAIN
            dp = min(dp, N6_DROP_CAP)               # cap dropout in the N6 band
        return wd, dp

    # ── train loop ────────────────────────────────────────────────────────────
    model.train()
    t0 = time.time(); loss0 = lossF = None
    last_aux = {}
    for step in range(1, steps + 1):
        wd, dp = reg_for_step(step)
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
        aux = {}

        def _compute():
            out = model(x, y)
            extra = out["aux_loss"]
            if dict_head is not None and "h" in feat_box:
                dloss, dinfo = dict_head(feat_box["h"])
                extra = extra + DICT_LAMBDA * dloss
                aux.update(dinfo)
            if jamo_head is not None and "h" in feat_box:
                jloss, jinfo = jamo_head(feat_box["h"], y)
                extra = extra + JAMO_LAMBDA * jloss
                aux.update(jinfo)
            return out, out["ce_loss"] + extra

        if a.bf16 and device == "cuda":
            with torch.autocast("cuda", dtype=torch.bfloat16):
                out, loss = _compute()
            loss.backward()
        else:
            out, loss = _compute()
            loss.backward()
        torch.nn.utils.clip_grad_norm_(params, 1.0)
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

    # ── N1: fold the TLoRA tensor-product factor into production expert weights ─
    if tlora is not None:
        dn = tlora.delta_norm()
        tlora.apply_into_weights()
        print(f"  [N1 TLoRA] folded tensor-product factor into expert weights "
              f"(delta_norm={dn:.5f}); .clm now sees the summed additive weight.", flush=True)

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

    # ── N3 DBES expert-specialization diagnostic (measurement-only) ───────────
    dbes = None
    if a.dbes:
        xb, _ = get_batch(1)
        dbes = dbes_diagnostic(model, xb)
        model.train()
        print(f"  [N3 DBES] {json.dumps(dbes, ensure_ascii=False)}", flush=True)

    # ── persist torch ckpt (ALWAYS — a_fire_recover_complete) ────────────────
    sd = {k: v.detach().cpu() for k, v in model.state_dict().items()}
    if a.ckpt_out:
        torch.save(sd, a.ckpt_out)
        print(f"  torch ckpt -> {a.ckpt_out} ({os.path.getsize(a.ckpt_out)} bytes)", flush=True)

    # ── summary json ──────────────────────────────────────────────────────────
    summary = {"arm": arm, "seed": a.seed, "n_params": n_params,
               "levers": {"n6_grok": want_n6, "n7_dictaux": want_n7,
                          "n8_jamo": want_n8, "n1_tlora": want_n1,
                          "n3_dbes": bool(a.dbes), "n4_set_search_k": a.n4_set_search},
               "frozen_hyper": {"DICT_LAMBDA": DICT_LAMBDA, "DICT_FACTOR": DICT_FACTOR,
                                "DICT_L1": DICT_L1, "N6_WD_GAIN": N6_WD_GAIN,
                                "N6_DROP_CAP": N6_DROP_CAP, "JAMO_LAMBDA": JAMO_LAMBDA},
               "loss0": round(loss0, 5), "lossF": round(lossF, 5),
               "wall_s": round(wall, 1), "uniform_ce": round(uniform, 5),
               "final_val_ce_pooled": (round(final_val, 5) if final_val else None),
               "registers_descent": f"{n_desc}/{len(per)}",
               "heldout_descent": descent, "last_aux": last_aux,
               "dbes_diagnostic": dbes,
               "tier": "engine-native-eligible (.clm additive); torch train metrics "
                       "DIRECTIONAL — G0-G6 verdict via core/g_gates.py (torch-free)"}
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
