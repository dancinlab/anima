#!/usr/bin/env python3
# ════════════════════════════════════════════════════════════════════════════
#  cli/train.py — anima REFERENCE + BRIDGE trainer (torch Lane-P).
#
#  ┌── ROLE (a_clm_gen_pipeline) ─────────────────────────────────────────────┐
#  │ This is the REFERENCE + BRIDGE trainer, NOT the production trainer.        │
#  │                                                                           │
#  │   Production trainer = cli/train.hexa (hexa-native flame/forge,            │
#  │   a_train_flame_forge: .hexa on stdlib/flame own-GEMM, NO .py trainer).    │
#  │                                                                           │
#  │ cli/train.hexa is single-thread native-CPU-scalar-bound (#2598/#2600 :     │
#  │ util peak ~65% / sustained <30%) so an actual 303M GPU train on it idles   │
#  │ the GPU. This torch Lane-P path is GPU-BOUND (cuda GEMM-saturating), so it │
#  │ can train the real clm303 (L4·d3784·E2->Emax4) efficiently TODAY — the     │
#  │ explicitly-sanctioned REFERENCE + BRIDGE path (a_clm_gen_pipeline:         │
#  │ "Lane-P torch = REFERENCE + bridge, forge is the PUBLIC production trainer")│
#  │                                                                           │
#  │ It trains a CLMConvMoE GPU-bound, then SERIALIZES the weights to a         │
#  │ .clm v0.3 file (CLM\x01 magic + CLMX trailer) that CORE core/clm_decode    │
#  │ .hexa loads back byte-exact for the engine-native G6 verdict.              │
#  │                                                                           │
#  │   ENGINE-NATIVE GATE (a_engine_native_learning, HARD-GATE):                │
#  │     torch-side CE / metrics here  = DIRECTIONAL only (NOT terminal).       │
#  │     TERMINAL verdict              = CORE re-measure of the serialized .clm │
#  │                                     on core/clm_decode.hexa frozen G6 bars │
#  │                                     (H_1129/1139 recombination, H_1140     │
#  │                                     novelty). The trained ckpt MUST be     │
#  │                                     pulled before teardown (a_fire_recover │
#  │                                     _complete) so engine-check is possible.│
#  └───────────────────────────────────────────────────────────────────────────┘
#
#  RECIPE PARITY with cli/train.hexa (reflected verbatim):
#    * MODE_CANON shape — clm303: L4 · d3784 · E2->Emax4 (true 303M), byte V=256,
#      K=3, dilation = min(2^l, 512) (model.py CausalDilatedConv1d).
#    * SAVANT (a_savant_train, H_1560/1562/1563) — golden-zone inhibition with a
#      CUSP latch + asymmetric hysteresis. GZ_LOWER = 1/2 - ln(4/3) ~ 0.2123179.
#      Inhibition (weight-decay / dropout / router-temperature) anneals from a
#      high I0 toward a floor BELOW GZ_LOWER (H_1559: learning-inhibition sweet-
#      spot may sit under the Phi golden zone) so the real sweet-spot is reached.
#      When I first ENTERS [GZ_LOWER, GZ_UPPER] the savant mode latches ON (cusp
#      hard-step) and STAYS on (hysteresis, never re-raised).
#    * MITOSIS (a_mitosis_train, H_1288) — cell division E->E+1 mid-training: a
#      parent expert's conv is copied (+tiny perturbation) into a fresh slot and
#      the router bias splits by -ln2 on both children (near-continuous gate-mass
#      conservation). Experts are allocated at Emax so the split writes in place.
#    * 4-cell register corpus (a_chat_registers) — {ko·en}x{normal·SNS} byte
#      stream, round-robin, mmap streaming (no whole-file slurp). HF dataset
#      names and/or local byte files via --corpus.
#    * AdamW + next-byte CE (grad-exact).
#
#  .clm SERIALIZE — reuses the GROUND-TRUTH bridge serializer
#  train/clm/model/clm_serialize_v2.py::serialize_v3 (the SAME byte layout the
#  golden reference reexport_d768_v2_fast.clm uses), so the output is byte-exact
#  to what core/clm_decode.hexa parses. verify_clm_v2.clm_decodable / parse_clm
#  self-check the written file.
#
#  USAGE:
#    python cli/train.py --out ckpt.clm --corpus <p1> [<p2> ...] \
#        [--canon | --d D --L L] [--steps N] [--no-savant] [--no-mitosis]
#  GPU (cuda) by default; CPU fallback for the $0 smoke.
# ════════════════════════════════════════════════════════════════════════════
from __future__ import annotations

import argparse
import math
import os
import sys
import time

import torch
import torch.nn as nn
import torch.nn.functional as F

# ── locate the CLM model + the ground-truth .clm serializer/verifier ─────────
_HERE = os.path.dirname(os.path.abspath(__file__))
_REPO = os.path.dirname(_HERE)
_MODEL = os.path.join(_REPO, "train", "clm", "model")
if _MODEL not in sys.path:
    sys.path.insert(0, _MODEL)

# (imports resolve via the sys.path insert above to the ground-truth CLM model
#  + .clm serializer/verifier under train/clm/model/.)
from model import CLMConfig, CLMConvMoE, MoEStats   # train/clm/model/model.py
import clm_serialize_v2 as S                         # serialize_v3 = bridge SSOT
import verify_clm_v2 as VC                           # clm_decodable / parse_clm


# ════════════════════════════════════════════════════════════════════════════
#  golden-zone constants (SAVANT/savant_lib.hexa H_347/348, verbatim — same as
#  cli/train.hexa gz_lower()/gz_upper()).
# ════════════════════════════════════════════════════════════════════════════
GZ_LOWER = 0.21231792755821914   # 1/2 - ln(4/3)  (sa_gz_lower)
GZ_UPPER = 0.5                    # sa_gz_upper
LN2 = 0.6931471805599453


def savant_inhibition(step: int, n_steps: int, i0: float, i_floor: float,
                      latch: dict) -> float:
    """Golden-zone cusp-anneal inhibition for THIS step (a_savant_train).

    Linear anneal I0 -> I_floor over training. When I first crosses INTO the
    golden zone [GZ_LOWER, GZ_UPPER] on the way down, latch['on'] hard-steps to
    True (cusp, H_1562) and STAYS True for the rest of training (asymmetric
    hysteresis, H_1563) even as the anneal drives I below GZ_LOWER (H_1559: the
    sweep below the floor is intentional so the learning sweet-spot is reached).
    Mirrors cli/train.hexa::savant_inhibition in arithmetic.
    """
    denom = (n_steps - 1) if n_steps > 1 else 1
    frac = (step - 1) / denom
    inh = i0 + (i_floor - i0) * frac
    if not latch["on"]:
        if GZ_LOWER <= inh <= GZ_UPPER:
            latch["on"] = True
            if latch["at"] == 0:
                latch["at"] = step
    return inh


def inhibition_to_wd(inh: float) -> float:
    """Map inhibition I -> AdamW weight decay (I in [0,0.5] -> wd in [0,0.05]).
    Deterministic (p7). Same linear lever as cli/train.hexa::inhibition_to_wd."""
    return inh * 0.1


def inhibition_to_dropout(inh: float) -> float:
    """Inhibition also realized as dropout p (clamped to a sane [0, 0.5]). The
    dropout/weight-decay/temperature variants share the single scalar lever."""
    return max(0.0, min(0.5, inh))


# ════════════════════════════════════════════════════════════════════════════
#  MITOSIS split E -> E+1 (a_mitosis_train) — continuity-preserving cell division
#  on the live torch MoEConvLayer. Port of cli/train.hexa::train_mitosis_split /
#  clm_mitosis.hexa::mitosis_split semantics:
#    * child expert conv = copy(parent) + tiny alternating +/-1e-4 perturbation
#    * router weight row for child = copy(parent row)
#    * router bias: both parent and child get (parent_bias - ln2) so the two
#      children jointly reproduce the parent's gate mass (near-continuous split)
#    * the optimizer's Adam moments for the touched params are reset to 0.
#  Experts are pre-allocated at Emax (inactive experts masked out of the router
#  until they are "born"), so a split just UNMASKS + seeds the next slot.
# ════════════════════════════════════════════════════════════════════════════
class MitosisMoE:
    """Tracks the ACTIVE expert count E while experts/router are physically
    allocated at Emax. Inactive experts are masked out of the router softmax
    (logit += -1e9) so they are inert until born."""

    def __init__(self, model: CLMConvMoE, e0: int, emax: int):
        self.model = model
        self.e_active = e0
        self.emax = emax
        dev = next(model.parameters()).device
        self.active_mask = torch.zeros(emax, device=dev)
        self.active_mask[:e0] = 1.0

    def neg_inf_bias(self) -> torch.Tensor:
        # additive router-logit bias: 0 for active slots, -1e9 for dormant.
        return (self.active_mask - 1.0) * 1e9

    @torch.no_grad()
    def split(self, parent: int, opt: torch.optim.Optimizer) -> int:
        """Divide `parent` into a fresh child slot (= current e_active index).
        Returns the new active count, or the unchanged count if at Emax."""
        if self.e_active >= self.emax:
            return self.e_active
        child = self.e_active
        moe = self.model.moe
        pe = moe.experts[parent].conv.conv     # parent expert Conv1d
        ce = moe.experts[child].conv.conv      # child  expert Conv1d
        # copy weights + tiny alternating perturbation (parity w/ hexa eps loop)
        pw = pe.weight.detach().clone()
        flat = pw.reshape(-1)
        eps = torch.full_like(flat, 1e-4)
        eps[1::2] = -1e-4
        ce.weight.copy_((flat + eps).reshape(pw.shape))
        if pe.bias is not None and ce.bias is not None:
            ce.bias.copy_(pe.bias)
        # router: child row = parent row; bias splits by -ln2 on BOTH children
        rw = moe.router.weight             # (Emax, d, 1)
        rb = moe.router.bias               # (Emax,)
        rw[child].copy_(rw[parent])
        pb = rb[parent].item()
        rb[parent] = pb - LN2
        rb[child] = pb - LN2
        # reset Adam moments for the touched params (m,v -> 0).
        for p in (pe.weight, ce.weight, pe.bias, ce.bias, rw, rb):
            if p is None:
                continue
            st = opt.state.get(p, None)
            if st:
                if "exp_avg" in st:
                    st["exp_avg"].zero_()
                if "exp_avg_sq" in st:
                    st["exp_avg_sq"].zero_()
        self.active_mask[child] = 1.0
        self.e_active = child + 1
        return self.e_active


# ════════════════════════════════════════════════════════════════════════════
#  Router masking — patch MoEConvLayer.forward so dormant experts are inert.
#  We add the dormant-slot -inf bias to the router logits before softmax so an
#  allocated-at-Emax model behaves EXACTLY like an E-active model until a mitosis
#  split unmasks the next slot. Pure additive logit mask; trunk/embed/readout are
#  untouched, so the serialized .clm round-trips the grown E.
# ════════════════════════════════════════════════════════════════════════════
def install_router_mask(model: CLMConvMoE, mito: MitosisMoE):
    moe = model.moe
    orig_router = moe.router

    def masked_forward(x):
        B, C, T = x.shape
        n_e = moe.rc.n_experts
        logits = orig_router(x) + mito.neg_inf_bias().view(1, n_e, 1)
        probs = F.softmax(logits, dim=1)
        ent_tok = -(probs * torch.log(probs + 1e-9)).sum(dim=1)
        entropy = ent_tok.mean()
        ex_out = torch.stack([e(x) for e in moe.experts], dim=1)
        if moe.rc.hard_top_k:
            k = min(moe.rc.top_k, int(mito.e_active))
            topv, topi = probs.topk(k, dim=1)
            gate = topv / (topv.sum(dim=1, keepdim=True) + 1e-9)
            mask = torch.zeros_like(probs).scatter_(1, topi, gate)
        else:
            mask = probs
        y = (mask.unsqueeze(2) * ex_out).sum(dim=1)
        usage = probs.mean(dim=(0, 2))
        aux = x.new_zeros(())
        if moe.rc.load_balance_coef > 0.0:
            top1 = probs.argmax(dim=1)
            f_i = F.one_hot(top1, n_e).to(probs.dtype).mean(dim=(0, 1))
            lb = n_e * (f_i * usage).sum()
            aux = aux + moe.rc.load_balance_coef * lb
        if moe.rc.entropy_coef > 0.0:
            aux = aux - moe.rc.entropy_coef * entropy
        return y, MoEStats(usage=usage, aux_loss=aux, entropy=entropy)

    moe.forward = masked_forward


# ════════════════════════════════════════════════════════════════════════════
#  4-cell register corpus (a_chat_registers) — {ko·en}x{normal·SNS}. Each
#  --corpus entry is a LOCAL byte file OR an HF dataset path (resolved to a local
#  cached byte stream). Windows are sampled round-robin across the cells so every
#  step sees the register mix. Files are mmap'd so a multi-GB cell is never
#  slurped whole into RAM.
# ════════════════════════════════════════════════════════════════════════════
class ByteCell:
    """One register cell — a memory-mapped byte file sampled by random windows.

    The TAIL `val_frac` of the file is reserved as a held-out validation region
    DISJOINT from the train region (overfit detector, a_savant_train held-out
    monitor). Train windows are sampled only from [0, train_end); val windows
    only from [train_end, size). A window can NEVER straddle the boundary
    (start ranges are clamped to keep start+seq_len+1 within the region), so the
    val region's bytes are never seen by a training gradient step."""

    def __init__(self, path: str, val_frac: float = 0.0):
        import mmap
        self.path = path
        self.size = os.path.getsize(path)
        self._f = open(path, "rb")
        if self.size > 0:
            self._mm = mmap.mmap(self._f.fileno(), 0, access=mmap.ACCESS_READ)
        else:
            self._mm = b""
        # boundary: bytes [0, train_end) = train, [train_end, size) = held-out val.
        vf = max(0.0, min(0.5, val_frac))
        self.train_end = int(self.size * (1.0 - vf)) if self.size > 0 else 0

    def _window_in(self, lo: int, hi_excl: int, seq_len: int,
                   gen: torch.Generator):
        """Sample one (x,y) window whose [start, start+seq_len+1) lies entirely
        inside the byte range [lo, hi_excl). Returns None if the range is too
        small for even one window."""
        if hi_excl - lo < seq_len + 2:
            return None
        hi = hi_excl - seq_len - 1            # last valid start (exclusive upper bound)
        start = int(torch.randint(lo, hi, (1,), generator=gen).item())
        chunk = self._mm[start:start + seq_len + 1]
        buf = torch.frombuffer(bytearray(chunk), dtype=torch.uint8).long()
        return buf[:seq_len], buf[1:seq_len + 1]

    def window(self, seq_len: int, gen: torch.Generator):
        """A TRAIN window — sampled only from [0, train_end) (never the val tail)."""
        return self._window_in(0, self.train_end, seq_len, gen)

    def val_window(self, seq_len: int, gen: torch.Generator):
        """A held-out VAL window — sampled only from [train_end, size)."""
        return self._window_in(self.train_end, self.size, seq_len, gen)


def resolve_corpus_path(spec: str) -> str:
    """Resolve a --corpus entry to a local byte-file path.

    * existing local path -> use directly.
    * else treat as an HF dataset id (a_chat_registers names like
      'anima-corpus-5lang-unified-v2', 'anima-corpus-ko-fineweb2-broad',
      'anima-persona-sns-corpus') and stream it to a local cached byte file
      under $ANIMA_CORPUS_CACHE (default ./.corpus_cache) via `datasets`; the
      text column is concatenated UTF-8 -> raw bytes (V=256).
    """
    if os.path.exists(spec):
        return spec
    cache_root = os.environ.get("ANIMA_CORPUS_CACHE",
                                os.path.join(os.getcwd(), ".corpus_cache"))
    os.makedirs(cache_root, exist_ok=True)
    local = os.path.join(cache_root, spec.replace("/", "__") + ".bytes")
    if os.path.exists(local) and os.path.getsize(local) > 0:
        return local
    try:
        from datasets import load_dataset
    except Exception as e:
        raise FileNotFoundError(
            f"--corpus '{spec}' is not a local file and `datasets` is not "
            f"installed to fetch it as an HF dataset ({e}). Provide a local "
            f"byte file, or `pip install datasets`."
        )
    # An HF id never looks like a bare local filename (no slash AND ends in a
    # file extension that doesn't exist locally) — a plain missing path is almost
    # always a staging mistake, so make the HF intent explicit in the log.
    repo = spec if "/" in spec else f"dancinlab/{spec}"
    print(f"  resolve: '{spec}' is not a local path -> streaming HF dataset {repo}")
    ds = load_dataset(repo, split="train", streaming=True)
    maxrows = int(os.environ.get("ANIMA_CORPUS_MAXROWS", "0") or 0)
    text_col = None
    with open(local, "wb") as out:
        for i, row in enumerate(ds):
            if text_col is None:
                for c in ("text", "content", "body", "caption"):
                    if c in row:
                        text_col = c
                        break
                if text_col is None:
                    text_col = next(iter(row))
            out.write(str(row[text_col]).encode("utf-8", "replace"))
            out.write(b"\n")
            if maxrows > 0 and i + 1 >= maxrows:
                break
    return local


# ════════════════════════════════════════════════════════════════════════════
def main():
    ap = argparse.ArgumentParser(
        description="anima torch Lane-P REFERENCE+BRIDGE trainer "
                    "(NOT production; production = cli/train.hexa)")
    ap.add_argument("--out", required=True, help="serialized .clm v0.3 output path")
    ap.add_argument("--corpus", nargs="*", default=[],
                    help="4-cell register byte files OR HF dataset ids "
                         "(round-robin {ko·en}x{normal·SNS}); empty -> synthetic smoke")
    ap.add_argument("--cell-label", nargs="*", default=[],
                    help="optional register label per --corpus entry, same order "
                         "(e.g. ko-normal en-normal ko-sns en-sns) — used in the "
                         "per-cell balance/val report so the 4 registers are named")
    ap.add_argument("--require-cells", type=int, default=0,
                    help="abort unless EXACTLY this many usable corpus cells load "
                         "(e.g. 4 for the full {ko·en}x{normal·SNS} register). "
                         "Catches the silent register-incompleteness that caused "
                         "the ko-SNS-only overfit. 0 = off.")
    ap.add_argument("--canon", action="store_true",
                    help="clm303 canonical shape (L4·d3784·E2->Emax4, 303M)")
    ap.add_argument("--d", type=int, default=0, help="model width (override mode default)")
    ap.add_argument("--L", type=int, default=0, help="trunk depth (override mode default)")
    ap.add_argument("--steps", type=int, default=0, help="training steps (override mode default)")
    ap.add_argument("--seq-len", type=int, default=0, help="window length (override mode default)")
    ap.add_argument("--batch-size", type=int, default=8)
    ap.add_argument("--lr", type=float, default=3e-4)
    ap.add_argument("--no-savant", action="store_true", help="disable golden-zone inhibition lever")
    ap.add_argument("--no-mitosis", action="store_true", help="disable cell-division split lever")
    ap.add_argument("--e0", type=int, default=2, help="initial active experts")
    ap.add_argument("--emax", type=int, default=4, help="max experts (mitosis grows toward this)")
    ap.add_argument("--bf16", action="store_true", help="bf16 autocast (cuda)")
    ap.add_argument("--ckpt-out", default=None, help="optional torch state_dict path")
    ap.add_argument("--log-every", type=int, default=10)
    # ── anti-overfit regularization (explicit 1st-class knobs) ───────────────
    ap.add_argument("--dropout", type=float, default=-1.0,
                    help="FIXED trunk dropout p; overrides the savant-derived "
                         "dropout when >=0 (default -1 = let savant drive it)")
    ap.add_argument("--weight-decay", type=float, default=-1.0,
                    help="FIXED AdamW weight-decay; overrides the savant-derived "
                         "wd when >=0 (default -1 = let savant drive it)")
    # ── held-out validation monitor (overfit detector) ───────────────────────
    ap.add_argument("--val-frac", type=float, default=0.0,
                    help="fraction of EACH corpus cell's TAIL held out for "
                         "validation, disjoint from train (e.g. 0.02); 0 = off")
    ap.add_argument("--val-every", type=int, default=0,
                    help="log held-out val-CE every N steps (0 = off). Requires "
                         "--val-frac>0; val-CE is the generalization gate, NOT "
                         "train-CE (a_savant_train held-out monitor).")
    ap.add_argument("--val-batches", type=int, default=4,
                    help="number of val batches averaged per val-CE measurement")
    # ── fail-loud corpus guard (anti-starvation, a_no_llm_frame_trap) ────────
    ap.add_argument("--min-corpus-bytes", type=int, default=0,
                    help="abort if the TOTAL effective train corpus is below this "
                         "many bytes (catches the silent single-cell/missing-file "
                         "starvation that caused the 120x-repetition overfit). "
                         "0 = warn only.")
    a = ap.parse_args()

    savant_on = not a.no_savant
    mitosis_on = not a.no_mitosis

    # ── shape: canon (clm303) vs smoke defaults, with per-flag overrides ──────
    if a.canon:
        d = a.d or 3784
        L = a.L or 4
        seq_len = a.seq_len or 1024
        steps = a.steps or 2000
    else:
        d = a.d or 8
        L = a.L or 1
        seq_len = a.seq_len or (64 if a.corpus else 4)
        steps = a.steps or 40
    e0, emax = a.e0, a.emax
    V, K = 256, 3

    device = "cuda" if torch.cuda.is_available() else "cpu"
    print("=== anima cli/train.py — torch Lane-P REFERENCE+BRIDGE trainer ===")
    print("  ROLE: bridge (NOT production; production = cli/train.hexa)")
    print(f"  mode: {'CANON clm303' if a.canon else 'SMOKE'}  device={device}")
    print(f"  config: d={d} L={L} E0={e0} Emax={emax} V={V} K={K} "
          f"seq_len={seq_len} steps={steps} bs={a.batch_size}")
    print(f"  savant={savant_on} mitosis={mitosis_on}")
    if device == "cuda":
        cap = torch.cuda.get_device_capability()
        print(f"  cuda: {torch.cuda.get_device_name(0)} cap={cap[0]}.{cap[1]} torch={torch.__version__}")

    # ── model — allocate experts at Emax so mitosis grows in place ───────────
    cfg = CLMConfig(n_experts=emax, n_trunk_layers=L, d_model=d,
                    kernel_size=K, variant="AB", dilation_base=2, max_dilation=512)
    model = CLMConvMoE(cfg).to(device)
    n_params = model.num_params()
    print(f"  params: {n_params} ({n_params/1e6:.3f}M)")

    mito = MitosisMoE(model, e0, emax)
    install_router_mask(model, mito)

    opt = torch.optim.AdamW(model.parameters(), lr=a.lr, betas=(0.9, 0.999),
                            eps=1e-8, weight_decay=0.0)
    gen = torch.Generator().manual_seed(42)

    # ── savant schedule state ────────────────────────────────────────────────
    latch = {"on": False, "at": 0}
    i0 = GZ_UPPER                      # start HIGH (max inhibition)
    i_floor = GZ_LOWER - 0.05          # anneal BELOW GZ_LOWER (H_1559)
    split_step = max(1, steps // 2)    # one division at the midpoint (E0 -> E0+1)

    # ── corpus cells (4-register) or synthetic smoke batch ───────────────────
    cells = []
    labels = []
    for ci, spec in enumerate(a.corpus):
        p = resolve_corpus_path(spec)
        cells.append(ByteCell(p, val_frac=a.val_frac))
        labels.append(a.cell_label[ci] if ci < len(a.cell_label) else f"cell{ci}")
        c = cells[-1]
        print(f"  corpus cell[{ci}] {labels[ci]:<12s} {p}  size={c.size} bytes  "
              f"(train={c.train_end} val_tail={c.size - c.train_end})")
    if not cells:
        print("  corpus: NONE -> synthetic byte batch ($0 wiring smoke)")

    # ── fail-loud corpus guard + PER-CELL balance/repetition table ────────────
    # The previous overfit was driven by ONLY cell[0] (4MB ko-SNS) actually
    # loading while the manifest claimed a 4-register {ko·en}x{normal·SNS} set —
    # so ~500M tokens were drawn from 4MB (~120x repetition = memorization). The
    # per-cell table surfaces BOTH starvation (missing cell) AND imbalance (one
    # tiny register repeated far more than the others = per-register overfit).
    if cells:
        usable = [c for c in cells if c.train_end >= seq_len + 2]
        total_train_bytes = sum(c.train_end for c in usable)
        tokens_to_see = steps * a.batch_size * seq_len
        rep = (tokens_to_see / total_train_bytes) if total_train_bytes else float("inf")
        # round-robin gives each cell an EQUAL step-share, so each cell sees
        # ~tokens_to_see/len(cells) tokens — per-cell repetition = that / its bytes.
        n = len(cells)
        per_cell_tokens = tokens_to_see / n if n else 0
        print(f"  ── 4-cell register balance table "
              f"(tokens_to_see={tokens_to_see}, equal step-share /{n}) ──")
        print(f"     {'register':<12s} {'train_bytes':>12s} {'tokens/cell':>12s} "
              f"{'rep_ratio':>10s}")
        worst_rep = 0.0
        for c, lab in zip(cells, labels):
            cell_rep = (per_cell_tokens / c.train_end) if c.train_end else float("inf")
            worst_rep = max(worst_rep, cell_rep if c.train_end else 0.0)
            flag = "  <-- MEMORIZATION RISK" if cell_rep > 5.0 else ""
            print(f"     {lab:<12s} {c.train_end:>12d} {per_cell_tokens:>12.0f} "
                  f"{cell_rep:>9.2f}x{flag}")
        print(f"  corpus guard: cells={n} usable={len(usable)}  "
              f"total_train_bytes={total_train_bytes}  "
              f"repetition_ratio(pooled)={rep:.2f}x  worst_per_cell={worst_rep:.2f}x")
        if len(usable) < len(cells):
            dead = [c.path for c in cells if c.train_end < seq_len + 2]
            print(f"  corpus guard: WARNING {len(cells)-len(usable)} cell(s) too "
                  f"small to yield a train window (seq_len={seq_len}): {dead}")
        if worst_rep > 5.0:
            print(f"  corpus guard: WARNING worst per-cell repetition {worst_rep:.1f}x "
                  f">5x — that register will be MEMORIZED. Enlarge the small "
                  f"register(s) or reduce steps (balance = even per-cell exposure).")
        # register-completeness gate (the 4-cell requirement)
        if a.require_cells > 0 and len(usable) != a.require_cells:
            print(f"FAIL — require_cells={a.require_cells} but {len(usable)} usable "
                  f"cell(s) loaded. The 4-register {{ko·en}}x{{normal·SNS}} set is "
                  f"INCOMPLETE — refusing to train (this is the register-"
                  f"incompleteness that caused the ko-SNS-only overfit). Check "
                  f"every --corpus path staged (esp. HF-only ko_fineweb2_broad).")
            sys.exit(3)
        if a.min_corpus_bytes > 0 and total_train_bytes < a.min_corpus_bytes:
            print(f"FAIL — total effective train corpus {total_train_bytes} bytes "
                  f"< --min-corpus-bytes {a.min_corpus_bytes}. Refusing to train "
                  f"(this is the silent starvation that caused the overfit). "
                  f"Check that every --corpus path actually staged.")
            sys.exit(2)

    def get_batch(step: int):
        if cells:
            xs, ys = [], []
            for b in range(a.batch_size):
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

    val_gen = torch.Generator().manual_seed(1234)   # disjoint RNG from train

    @torch.no_grad()
    def _cell_val_ce(c: ByteCell) -> float | None:
        """Mean next-byte CE over held-out VAL windows of a SINGLE cell."""
        if c.size - c.train_end < seq_len + 2:
            return None
        was_training = model.training
        model.eval()
        tot, nb = 0.0, 0
        for vb in range(a.val_batches):
            xs, ys = [], []
            for _ in range(a.batch_size):
                w = c.val_window(seq_len, val_gen)
                if w is None:
                    continue
                xs.append(w[0]); ys.append(w[1])
            if not xs:
                continue
            vx = torch.stack(xs).to(device); vy = torch.stack(ys).to(device)
            if a.bf16 and device == "cuda":
                with torch.autocast("cuda", dtype=torch.bfloat16):
                    vo = model(vx, vy)
            else:
                vo = model(vx, vy)
            tot += float(vo["ce_loss"].detach()); nb += 1
        if was_training:
            model.train()
        return (tot / nb) if nb else None

    def eval_val_per_cell() -> dict:
        """Per-register held-out val-CE: {label: CE}. Lets us see WHICH register
        generalizes vs overfits (the 4-cell separate-monitor requirement)."""
        out = {}
        for c, lab in zip(cells, labels):
            v = _cell_val_ce(c)
            if v is not None:
                out[lab] = v
        return out

    def eval_val_ce() -> float | None:
        """Pooled mean held-out val-CE across all registers (= the single
        generalization number for the loop log). Mean over per-cell CEs so each
        register is weighted equally (matches the balanced step-share)."""
        per = eval_val_per_cell()
        return (sum(per.values()) / len(per)) if per else None

    # ── train loop ───────────────────────────────────────────────────────────
    model.train()
    t0 = time.time()
    loss0 = lossF = None
    ce_before_split = ce_after_split = None
    for step in range(1, steps + 1):
        if savant_on:
            inh = savant_inhibition(step, steps, i0, i_floor, latch)
            wd = inhibition_to_wd(inh)
            dp = inhibition_to_dropout(inh)
        else:
            wd, dp = 0.0, 0.0
        # explicit overrides take precedence over the savant-derived values
        # (anti-overfit knobs decoupled from the savant inhibition schedule).
        if a.weight_decay >= 0.0:
            wd = a.weight_decay
        if a.dropout >= 0.0:
            dp = a.dropout
        for grp in opt.param_groups:
            grp["weight_decay"] = wd
        for m in model.modules():
            if isinstance(m, nn.Dropout):
                m.p = dp

        if mitosis_on and step == split_step and mito.e_active < emax:
            prev = mito.e_active
            new_e = mito.split(0, opt)
            print(f"  step {step} (MITOSIS SPLIT) E {prev}->{new_e}")

        x, y = get_batch(step)
        opt.zero_grad(set_to_none=True)
        if a.bf16 and device == "cuda":
            with torch.autocast("cuda", dtype=torch.bfloat16):
                out = model(x, y)
                loss = out["loss"]
            loss.backward()
        else:
            out = model(x, y)
            loss = out["loss"]
            loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        opt.step()

        ce = float(out["ce_loss"].detach())
        if loss0 is None:
            loss0 = ce
        lossF = ce
        if step == split_step - 1:
            ce_before_split = ce
        if step == split_step + 1:
            ce_after_split = ce
        do_val = (a.val_every > 0 and (step == 1 or step % a.val_every == 0
                                       or step == steps))
        val_ce = eval_val_ce() if do_val else None
        if step == 1 or step % a.log_every == 0 or step == steps or do_val:
            vtxt = ""
            if val_ce is not None:
                gap = val_ce - ce
                vtxt = f"  val_CE={val_ce:.5f}  gap={gap:+.5f}"
            print(f"  step {step:5d}  CE={ce:.5f}  E={mito.e_active}  "
                  f"wd={wd:.4f}  dp={dp:.4f}{vtxt}")
    wall = time.time() - t0

    # ── final held-out val-CE PER REGISTER (the generalization verdict) ───────
    if a.val_frac > 0.0:
        per = eval_val_per_cell()
        uniform = math.log(V)
        if per:
            print(f"  ── FINAL held-out val-CE per register "
                  f"(uniform_ref={uniform:.4f}; DESCENT iff < uniform) ──")
            for lab, v in per.items():
                verdict = "DESCENT" if v < uniform else "NO-DESCENT(memorized/garbage)"
                print(f"     {lab:<12s} val_CE={v:.5f}  {verdict}")
            final_val = sum(per.values()) / len(per)
            n_desc = sum(1 for v in per.values() if v < uniform)
            print(f"  FINAL val_CE(pooled)={final_val:.5f}  (train_CE={lossF:.5f}  "
                  f"gap={final_val - lossF:+.5f})  registers_DESCENT={n_desc}/{len(per)}")
            if n_desc < len(per):
                print(f"  WARNING {len(per)-n_desc}/{len(per)} register(s) NOT "
                      f"generalizing (val_CE >= uniform {uniform:.4f}).")

    print(f"  loss0={loss0:.5f}  lossF={lossF:.5f}  wall={wall:.1f}s")
    print(f"  savant latched_at={latch['at']}  mitosis E0={e0}->E={mito.e_active}")
    if ce_before_split is not None and ce_after_split is not None:
        print(f"  mitosis CE across split: {ce_before_split:.5f} -> {ce_after_split:.5f}")

    # ── serialize -> .clm v0.3 (ground-truth bridge) + verify ────────────────
    sd = {k: v.detach().cpu() for k, v in model.state_dict().items()}
    if a.ckpt_out:
        torch.save(sd, a.ckpt_out)
        print(f"  torch ckpt -> {a.ckpt_out} ({os.path.getsize(a.ckpt_out)} bytes)")

    # serialize the ACTIVE (born) expert count. The model is allocated at Emax,
    # so the router weight/bias have Emax rows and there are Emax expert modules;
    # we SLICE the router (cout Emax -> e_ser) and drop dormant expert keys so the
    # engine recovers E == active from the router-block cout. serialize_v3 reads
    # only e0..e{E-1} experts; the sliced router makes block[nblk-2].cout == e_ser.
    e_ser = mito.e_active
    sd_active = {}
    for k, v in sd.items():
        if k == "moe.router.weight":
            sd_active[k] = v[:e_ser].contiguous()      # (Emax,d,1) -> (e_ser,d,1)
        elif k == "moe.router.bias":
            sd_active[k] = v[:e_ser].contiguous()      # (Emax,) -> (e_ser,)
        elif k.startswith("moe.experts."):
            eidx = int(k.split(".")[2])
            if eidx < e_ser:
                sd_active[k] = v                        # keep active experts only
        else:
            sd_active[k] = v
    print(f"  serializing .clm v0.3 (L={L} E={e_ser} d={d} V={V} K={K}) -> {a.out}")
    S.serialize_v3(sd_active, n_trunk_layers=L, n_experts=e_ser, out_path=a.out)
    nbytes = os.path.getsize(a.out)
    print(f"  ckpt WRITTEN {nbytes} bytes -> {a.out}")

    # ── self-check: CORE-loadable (mirror of core/clm_decode.hexa) ───────────
    rb = open(a.out, "rb").read()
    decodable = VC.clm_decodable(rb)
    pc = VC.parse_clm(rb)
    # ground-truth layout (core/clm_decode.hexa::clm_load + clm_serialize_v2
    #   _general_ext_order): blocks = ecW + tcW*L + eW*E + rW + roW (nblk=L+E+3);
    #   ext = embed,ecB, tcB*L, eB*E, rB,roB, tgG*L, tgB*L, noG,noB (n_ext=3L+E+6).
    exp_nblk = L + e_ser + 3
    exp_n_ext = 3 * L + e_ser + 6
    ok_nblk = (pc["nblk"] == exp_nblk)
    ok_next = (pc["n_ext"] == exp_n_ext)
    rec_E = pc["blocks"][-2]["cout"] if pc["blocks"] else None
    rec_V = pc["blocks"][-1]["cout"] if pc["blocks"] else None
    rec_d = pc["blocks"][0]["cout"] if pc["blocks"] else None
    rec_K = (pc["blocks"][0]["rest"] // rec_d) if rec_d else None
    rec_L = (pc["nblk"] - rec_E - 3) if (pc["nblk"] and rec_E is not None) else None
    print("")
    print("=== CORE-loadable self-check (mirror of core/clm_decode.hexa) ===")
    print(f"  clm_decodable      = {decodable}")
    print(f"  nblk               = {pc['nblk']}  (expect {exp_nblk})  -> {'OK' if ok_nblk else 'MISMATCH'}")
    print(f"  n_ext              = {pc['n_ext']}  (expect {exp_n_ext})  -> {'OK' if ok_next else 'MISMATCH'}")
    print(f"  CLMX trailer found = {pc['clmx_found']}")
    print(f"  exact_eof          = {pc['exact_eof']}")
    print(f"  recovered clm_config: d={rec_d} K={rec_K} V={rec_V} E={rec_E} L={rec_L}")
    ok_cfg = (rec_d == d and rec_V == V and rec_E == e_ser and rec_L == L and rec_K == K)
    all_ok = (decodable and ok_nblk and ok_next and pc["clmx_found"]
              and pc["exact_eof"] and ok_cfg)
    print("")
    if all_ok:
        print(f"PASS — .clm v0.3 is CORE-loadable; clm_config recovers d/L/E/V/K exactly "
              f"(d={d} L={L} E={e_ser} V={V} K={K}). Engine-native G6 verdict = CORE "
              f"re-measure (a_engine_native_learning: torch CE above is DIRECTIONAL only).")
        sys.exit(0)
    print("FAIL — serialized .clm is NOT CORE-loadable / config mismatch (see above)")
    sys.exit(1)


if __name__ == "__main__":
    main()
