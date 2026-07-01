#!/usr/bin/env python3
"""H_1815 CLS-on-ByteGPT — hippocampal pattern-separation/completion as a G1-
recombination lever on the ATTENTION (ByteGPT) trunk.

WHY THIS FILE. The CLS (dentate-gyrus separation + CA3 completion) OBJECTIVE lever
was run on the 303M ConvMoE trunk (H_1640). This file ports the SAME two auxiliary
objectives onto a **ByteGPT (24-layer attention) trunk** — the content-addressed
fetch-and-bind structure that (per H_1394) isolates G6 where conv blurs. The bet is
strictly: does the CLS objective lift ByteGPT G1 above floor where plain-CE ByteGPT
(H_1129) and objective-ConvMoE (H_1640) both floor?

BASE = state/1602_bytegpt_recomb_objective/trainer.py (self-contained ByteGPT, inline
Block/ByteGPT, savant golden-zone anneal, 4-cell corpus loader, serialize_bin -> .bin).
The ce_marginal (control) + infonce arms are kept VERBATIM.

PORTED ARMS (from state/1640_cls_sep_complete/trainer.py, math reused EXACTLY):
  ce_marginal : standard next-byte CE (control; CE never rewards separation/completion).
  infonce     : CE + InfoNCE contrastive-predictive term (H_1602 original ByteGPT arm).
  cls_sep     : CE + LAMBDA_SEP * L_separation             (DG decorrelation + sparsity).
  cls_full    : CE + LAMBDA_SEP * L_separation + LAMBDA_COMP * L_completion (sep+CA3 compl).

The CLS losses operate on the trunk PENULTIMATE (post ln_f, pre self.head) — for
ByteGPT that is exactly the `x` fed to the tied head (return_pen=True). The completion
head is a TRAINING-ONLY nn.Module (Linear d->COMPLETE_HID->d), NOT in ByteGPT.state_dict
so it is dropped at serialize; the .bin stays a pure ByteGPT mouth (5xu32 header) that
core/bytegpt_decode.py / cli/evaluate.py header-sniffs and decodes.

Because the readout stays the standard tied head, ALL arms are .bin-serializable ->
engine-native G1 is by-construction OPEN: terminal verdict path = cli/evaluate.py <bin>
(torch training is DIRECTIONAL, a_engine_native_learning).

USAGE (per arm; fire the 3 arms with the SAME --seed/--steps/--corpus):
  python3 trainer.py --objective {ce_marginal,cls_sep,cls_full} --seed N \\
      --corpus <ko-gen> <en-gen> <ko-sns> <en-sns> \\
      --cell-label ko-general en-general ko-sns en-sns \\
      --canon --steps 2000 --val-frac 0.05 --val-every 200 --sample proportional \\
      --out ckpt/<obj>_seed<N>.pt --bin-out ckpt/<obj>_seed<N>.bin \\
      --json-out ckpt/<obj>_seed<N>.json
"""
from __future__ import annotations
import argparse, json, math, os, struct, sys, time, hashlib
import torch
import torch.nn as nn
import torch.nn.functional as F

# ── frozen savant golden-zone constants (== cli/train.py / cli/train.hexa) ──────
GZ_LOWER = 0.21231792755821914   # 1/2 - ln(4/3)  (sa_gz_lower)
GZ_UPPER = 0.5                    # sa_gz_upper

# ── frozen objective hyperparams (== state/1602_recomb_objective/trainer.py) ────
INFONCE_LAMBDA = 1.0
INFONCE_NEG = 64                 # negatives per position drawn from the V-way byte pool

# ── frozen CLS hyperparams (== state/1640_cls_sep_complete/trainer.py — ported) ─
LAMBDA_SEP = 0.1          # separation (decorrelation+sparsity) weight
LAMBDA_COMP = 0.1         # completion (autoassociative) weight
SEP_SPARSITY = 0.01       # L1 sparsity sub-weight inside L_sep (Marr-Albus sparsen)
COMPLETE_MASK = 0.5       # fraction of penultimate channels masked for the cue
COMPLETE_HID = 256        # completion head hidden width (training-only, dropped)


# ════════════════════════════════════════════════════════════════════════════
#  savant golden-zone cusp-anneal (REPLICATED byte-faithfully from cli/train.py)
# ════════════════════════════════════════════════════════════════════════════
def savant_inhibition(step: int, n_steps: int, i0: float, i_floor: float,
                      latch: dict) -> float:
    """Golden-zone cusp-anneal inhibition for THIS step (a_savant_train). Linear
    anneal I0 -> I_floor; latch ON when I first enters [GZ_LOWER,GZ_UPPER] on the
    way down (cusp H_1562) and STAYS ON (asymmetric hysteresis H_1563). VERBATIM
    arithmetic of cli/train.py::savant_inhibition."""
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
    """I -> AdamW weight decay (== cli/train.py::inhibition_to_wd)."""
    return inh * 0.1


def inhibition_to_dropout(inh: float) -> float:
    """I -> dropout p, clamped [0,0.5] (== cli/train.py::inhibition_to_dropout)."""
    return max(0.0, min(0.5, inh))


# ════════════════════════════════════════════════════════════════════════════
#  ByteGPT model — VERBATIM from SAVANT-torch/savant_train_torch_cuda.py so the
#  state_dict keys match tool/bytegpt_serialize.py exactly (ln1/attn.in_proj/
#  out_proj/ln2/mlp.0/mlp.2/ln_f/head). grad_ckpt default OFF at 303M (fits 12GB).
# ════════════════════════════════════════════════════════════════════════════
class Block(nn.Module):
    def __init__(self, d, n_head, p_drop):
        super().__init__()
        self.ln1 = nn.LayerNorm(d)
        self.attn = nn.MultiheadAttention(d, n_head, dropout=p_drop, batch_first=True)
        self.ln2 = nn.LayerNorm(d)
        self.mlp = nn.Sequential(nn.Linear(d, 4 * d), nn.GELU(),
                                 nn.Linear(4 * d, d), nn.Dropout(p_drop))

    def forward(self, x, attn_mask):
        h = self.ln1(x)
        a, _ = self.attn(h, h, h, attn_mask=attn_mask, need_weights=False)
        x = x + a
        x = x + self.mlp(self.ln2(x))
        return x


class ByteGPT(nn.Module):
    def __init__(self, vocab=256, d=1024, n_layer=24, n_head=16, block=512,
                 p_drop=0.0, grad_ckpt=False):
        super().__init__()
        self.block = block
        self.grad_ckpt = grad_ckpt
        self.tok = nn.Embedding(vocab, d)
        self.pos = nn.Embedding(block, d)
        self.drop = nn.Dropout(p_drop)
        self.blocks = nn.ModuleList([Block(d, n_head, p_drop) for _ in range(n_layer)])
        self.ln_f = nn.LayerNorm(d)
        self.head = nn.Linear(d, vocab, bias=False)
        self.head.weight = self.tok.weight  # tie
        self.apply(self._init)

    def _init(self, m):
        if isinstance(m, nn.Linear):
            nn.init.normal_(m.weight, std=0.02)
            if m.bias is not None:
                nn.init.zeros_(m.bias)
        elif isinstance(m, nn.Embedding):
            nn.init.normal_(m.weight, std=0.02)

    def set_dropout(self, p: float):
        """savant dropout lever: set every Dropout module's p (== train.py loop)."""
        for m in self.modules():
            if isinstance(m, nn.Dropout):
                m.p = p
        # nn.MultiheadAttention stores dropout as a float attribute, not a module
        for blk in self.blocks:
            blk.attn.dropout = p

    def forward(self, idx, targets=None, return_pen=False):
        """return_pen=True also returns the penultimate `x` (post ln_f, pre head) —
        exactly the tensor fed to self.head, shape (B,T,d). Default False keeps the
        legacy (logits, loss) contract for existing callers (val / ce_marginal / infonce)."""
        B, T = idx.shape
        pos = torch.arange(T, device=idx.device)
        x = self.drop(self.tok(idx) + self.pos(pos)[None, :, :])
        mask = torch.triu(torch.full((T, T), float("-inf"), device=idx.device), diagonal=1)
        for blk in self.blocks:
            if self.grad_ckpt and self.training:
                from torch.utils.checkpoint import checkpoint
                x = checkpoint(blk, x, mask, use_reentrant=False)
            else:
                x = blk(x, mask)
        x = self.ln_f(x)                              # <- penultimate (readout input)
        logits = self.head(x)
        loss = None
        if targets is not None:
            loss = F.cross_entropy(logits.view(-1, logits.size(-1)), targets.view(-1))
        if return_pen:
            return logits, loss, x
        return logits, loss


# ════════════════════════════════════════════════════════════════════════════
#  objective heads — consume the SAME logits; only the LOSS differs (== H_1602).
# ════════════════════════════════════════════════════════════════════════════
def _ce(logits, targets, V):
    return F.cross_entropy(logits.reshape(-1, V), targets.reshape(-1))


def loss_ce_marginal(logits, targets, V, gen):
    """ARM-OFF control: standard CE next-byte marginal. logits (B,T,V)."""
    return _ce(logits, targets, V), {}


def loss_infonce(logits, targets, V, gen):
    """ARM-ON: CE + InfoNCE contrastive-predictive term (== H_1602 loss_infonce).
    Positive = true next byte; negatives = INFONCE_NEG random bytes (collisions ->
    -inf). Rewards SEPARATING the true continuation from decoys per position."""
    ce = _ce(logits, targets, V)
    lg = logits.reshape(-1, V)                       # (N, V)
    tgt = targets.reshape(-1)                         # (N,)
    N = tgt.shape[0]
    pos = lg.gather(1, tgt.unsqueeze(1))             # (N,1) true-byte score
    neg_idx = torch.randint(0, V, (N, INFONCE_NEG), generator=gen, device=lg.device)
    neg = lg.gather(1, neg_idx)                       # (N, K)
    collide = (neg_idx == tgt.unsqueeze(1))
    neg = neg.masked_fill(collide, float("-inf"))
    cand = torch.cat([pos, neg], dim=1)             # (N, 1+K) positive at col 0
    infonce = F.cross_entropy(cand, torch.zeros(N, dtype=torch.long, device=lg.device))
    return ce + INFONCE_LAMBDA * infonce, {"infonce": float(infonce.detach())}


# ════════════════════════════════════════════════════════════════════════════
#  CLS auxiliary losses on the ByteGPT penultimate code (B, T, d) — PORTED from
#  state/1640_cls_sep_complete/trainer.py. The ONLY adaptation vs 1640 is the
#  flatten to (N, C): 1640's conv penultimate is (B, C, T) [channel-first] and
#  flattens via h.permute(0,2,1).reshape(-1,C); ByteGPT's penultimate is already
#  (B, T, d) [channel-last] so h.reshape(-1, C) yields the SAME (N=B*T, C=d)
#  matrix. All reductions / masking fraction / sub-weights are reused EXACTLY.
# ════════════════════════════════════════════════════════════════════════════
def loss_separation(h: torch.Tensor):
    """DG pattern-separation pressure: decorrelate channels (off-diagonal Gram
    energy -> 0, an orthogonalization push) + mild L1 sparsity (sparsen the
    expanded code). Operates on the per-position penultimate code.

    h: (B, T, C). Flatten over (B,T) -> (N, C); center; normalized cross-channel
    correlation matrix; penalize off-diagonal mass. Lower => more separated.
    (H_1640 loss_separation math verbatim; flatten adapted to channel-last.)"""
    B, Tt, C = h.shape
    z = h.reshape(-1, C)                          # (N, C)
    z = z - z.mean(dim=0, keepdim=True)
    std = z.std(dim=0, keepdim=True) + 1e-5
    zn = z / std                                  # unit-variance channels
    N = zn.shape[0]
    corr = (zn.t() @ zn) / N                      # (C, C) ~ correlation matrix
    off = corr - torch.diag(torch.diag(corr))
    decorr = (off ** 2).mean()                    # off-diagonal energy -> separate
    sparsity = z.abs().mean()                     # L1 sparsen (Marr-Albus)
    return decorr + SEP_SPARSITY * sparsity, {"decorr": float(decorr.detach()),
                                              "sparsity": float(sparsity.detach())}


def loss_completion(h: torch.Tensor, comp_head: nn.Module, gen: torch.Generator):
    """CA3 autoassociative completion: mask a fraction of penultimate CHANNELS
    (partial cue) and require a tiny linear head to reinstate the FULL code (MSE).
    Reinstating full-from-partial is the substrate of composing the joint pattern
    from single-concept cues. comp_head is TRAINING-ONLY (dropped before serialize).
    (H_1640 loss_completion math verbatim; flatten adapted to channel-last.)"""
    B, Tt, C = h.shape
    z = h.reshape(-1, C)                          # (N, C)
    mask = (torch.rand(C, generator=gen, device=z.device) > COMPLETE_MASK).float()
    cue = z * mask.unsqueeze(0)                   # partial cue (channels dropped)
    recon = comp_head(cue)                        # reinstate
    mse = F.mse_loss(recon, z.detach())          # target = full code (stop-grad target)
    return mse, {"complete_mse": float(mse.detach())}


def loss_cls(logits, pen, targets, V, use_sep, use_comp, comp_head, gen):
    """CE + CLS auxiliary terms on the ByteGPT penultimate `pen` (B,T,d). Port of
    H_1640 compute(): CE + LAMBDA_SEP*L_sep [+ LAMBDA_COMP*L_complete]."""
    obj = _ce(logits, targets, V)
    aux = {}
    if use_sep:
        ls, da = loss_separation(pen)
        obj = obj + LAMBDA_SEP * ls
        aux.update(da)
    if use_comp:
        lc, dc = loss_completion(pen, comp_head, gen)
        obj = obj + LAMBDA_COMP * lc
        aux.update(dc)
    return obj, aux


# logits-based arms use OBJECTIVES[fn]; cls arms are special-cased (need penultimate
# + comp_head, so they don't fit the (logits,targets,V,gen) signature).
OBJECTIVES = {"ce_marginal": loss_ce_marginal, "infonce": loss_infonce}
CLS_OBJECTIVES = ("cls_sep", "cls_full")
ALL_OBJECTIVES = list(OBJECTIVES) + list(CLS_OBJECTIVES)


# ════════════════════════════════════════════════════════════════════════════
#  4-cell register corpus (REPLICATED from cli/train.py ByteCell + resolver) — the
#  TAIL val_frac of each cell is held-out (DESCENT gate, a_savant_train).
# ════════════════════════════════════════════════════════════════════════════
class ByteCell:
    def __init__(self, path: str, val_frac: float = 0.0):
        import mmap
        self.path = path
        self.size = os.path.getsize(path)
        self._f = open(path, "rb")
        self._mm = mmap.mmap(self._f.fileno(), 0, access=mmap.ACCESS_READ) if self.size > 0 else b""
        vf = max(0.0, min(0.5, val_frac))
        self.train_end = int(self.size * (1.0 - vf)) if self.size > 0 else 0

    def _window_in(self, lo, hi_excl, seq_len, gen):
        if hi_excl - lo < seq_len + 2:
            return None
        hi = hi_excl - seq_len - 1
        start = int(torch.randint(lo, hi, (1,), generator=gen).item())
        chunk = self._mm[start:start + seq_len + 1]
        buf = torch.frombuffer(bytearray(chunk), dtype=torch.uint8).long()
        return buf[:seq_len], buf[1:seq_len + 1]

    def window(self, seq_len, gen):
        return self._window_in(0, self.train_end, seq_len, gen)

    def val_window(self, seq_len, gen):
        return self._window_in(self.train_end, self.size, seq_len, gen)


def resolve_corpus_path(spec: str) -> str:
    if os.path.exists(spec):
        return spec
    cache_root = os.environ.get("ANIMA_CORPUS_CACHE", os.path.join(os.getcwd(), ".corpus_cache"))
    os.makedirs(cache_root, exist_ok=True)
    local = os.path.join(cache_root, spec.replace("/", "__") + ".bytes")
    if os.path.exists(local) and os.path.getsize(local) > 0:
        return local
    from datasets import load_dataset
    repo = spec if "/" in spec else f"dancinlab/{spec}"
    print(f"  resolve: '{spec}' -> streaming HF dataset {repo}", flush=True)
    ds = load_dataset(repo, split="train", streaming=True)
    maxrows = int(os.environ.get("ANIMA_CORPUS_MAXROWS", "0") or 0)
    text_col = None
    with open(local, "wb") as out:
        for i, row in enumerate(ds):
            if text_col is None:
                for c in ("text", "content", "body", "caption"):
                    if c in row:
                        text_col = c; break
                if text_col is None:
                    text_col = next(iter(row))
            out.write(str(row[text_col]).encode("utf-8", "replace")); out.write(b"\n")
            if maxrows > 0 and i + 1 >= maxrows:
                break
    return local


# ════════════════════════════════════════════════════════════════════════════
#  .pt -> .bin serialize (INLINE == tool/bytegpt_serialize.py key map). torch is
#  the bridge here (a_clm_gen_pipeline) — the VERDICT is cli/evaluate.py on the .bin.
#  NOTE: sd = ByteGPT.state_dict() ONLY — the training-only comp_head is a separate
#  nn.Module and is NOT in sd, so it is dropped here by construction.
# ════════════════════════════════════════════════════════════════════════════
def _f32le(t):
    return t.detach().to(torch.float32).cpu().contiguous().numpy().astype("<f4").tobytes()


def serialize_bin(sd, cfg, bin_path):
    vocab, d, n_layer, n_head, block = (cfg["vocab"], cfg["d"], cfg["n_layer"],
                                        cfg["n_head"], cfg["block"])

    def W(key, shape):
        if key not in sd:
            raise KeyError(f"missing state_dict key: {key}")
        t = sd[key]
        assert tuple(t.shape) == tuple(shape), f"{key} shape {tuple(t.shape)} != {shape}"
        return _f32le(t)

    out = bytearray()
    out += struct.pack("<5I", vocab, d, n_layer, n_head, block)
    out += W("tok.weight", (vocab, d))
    out += W("pos.weight", (block, d))
    for i in range(n_layer):
        p = f"blocks.{i}."
        out += W(p + "ln1.weight", (d,)); out += W(p + "ln1.bias", (d,))
        out += W(p + "attn.in_proj_weight", (3 * d, d)); out += W(p + "attn.in_proj_bias", (3 * d,))
        out += W(p + "attn.out_proj.weight", (d, d)); out += W(p + "attn.out_proj.bias", (d,))
        out += W(p + "ln2.weight", (d,)); out += W(p + "ln2.bias", (d,))
        out += W(p + "mlp.0.weight", (4 * d, d)); out += W(p + "mlp.0.bias", (4 * d,))
        out += W(p + "mlp.2.weight", (d, 4 * d)); out += W(p + "mlp.2.bias", (d,))
    out += W("ln_f.weight", (d,)); out += W("ln_f.bias", (d,))
    head_key = "head.weight" if "head.weight" in sd else "tok.weight"  # tied
    out += W(head_key, (vocab, d))
    with open(bin_path, "wb") as f:
        f.write(out)
    return len(out)


# ════════════════════════════════════════════════════════════════════════════
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--objective", required=True, choices=ALL_OBJECTIVES)
    ap.add_argument("--seed", type=int, default=7)
    ap.add_argument("--corpus", nargs="*", default=[])
    ap.add_argument("--cell-label", nargs="*", default=[])
    ap.add_argument("--canon", action="store_true")
    ap.add_argument("--d", type=int, default=0)
    ap.add_argument("--n_layer", type=int, default=0)
    ap.add_argument("--n_head", type=int, default=0)
    ap.add_argument("--block", type=int, default=0)
    ap.add_argument("--steps", type=int, default=0)
    ap.add_argument("--seq-len", type=int, default=0)
    ap.add_argument("--batch-size", type=int, default=8)
    ap.add_argument("--lr", type=float, default=3e-4)
    ap.add_argument("--no-savant", action="store_true")
    ap.add_argument("--bf16", action="store_true")
    ap.add_argument("--grad-ckpt", action="store_true")
    ap.add_argument("--sample", choices=["roundrobin", "proportional"], default="proportional")
    ap.add_argument("--val-frac", type=float, default=0.05)
    ap.add_argument("--val-every", type=int, default=200)
    ap.add_argument("--val-batches", type=int, default=4)
    ap.add_argument("--log-every", type=int, default=50)
    ap.add_argument("--out", default="", help="torch .pt path")
    ap.add_argument("--bin-out", default="", help="engine .bin path (serialized)")
    ap.add_argument("--json-out", default="", help="summary json")
    a = ap.parse_args()

    use_cls = a.objective in CLS_OBJECTIVES
    use_sep = a.objective in ("cls_sep", "cls_full")
    use_comp = a.objective == "cls_full"

    savant_on = not a.no_savant
    if a.canon:
        d = a.d or 1024; L = a.n_layer or 24; nh = a.n_head or 16
        block = a.block or 512
        seq_len = a.seq_len or 512; steps = a.steps or 2000
    else:
        d = a.d or 128; L = a.n_layer or 2; nh = a.n_head or 4
        block = a.block or 128
        seq_len = a.seq_len or 128; steps = a.steps or 60
    V = 256
    device = "cuda" if torch.cuda.is_available() else "cpu"
    objfn = OBJECTIVES.get(a.objective)              # None for cls_* (special-cased)

    print(f"=== H_1815 CLS-on-ByteGPT obj={a.objective} seed={a.seed} ===", flush=True)
    print(f"  device={device} d={d} L={L} H={nh} block={block} seq_len={seq_len} "
          f"steps={steps} bs={a.batch_size} sample={a.sample} savant={savant_on} "
          f"use_sep={use_sep} use_comp={use_comp}", flush=True)
    if device == "cuda":
        cap = torch.cuda.get_device_capability()
        print(f"  cuda: {torch.cuda.get_device_name(0)} cap={cap[0]}.{cap[1]} "
              f"torch={torch.__version__} cuda_available=1", flush=True)
        torch.backends.cuda.matmul.allow_tf32 = True
        torch.backends.cudnn.allow_tf32 = True
    else:
        print("  WARNING: CPU (smoke only; production train MUST be GPU)", flush=True)

    torch.manual_seed(a.seed)
    model = ByteGPT(V, d, L, nh, block, p_drop=0.0, grad_ckpt=a.grad_ckpt).to(device)
    n_params = sum(p.numel() for p in model.parameters())
    print(f"  params: {n_params} ({n_params/1e6:.3f}M)", flush=True)

    # completion head (TRAINING-ONLY — a separate nn.Module, NOT in ByteGPT.state_dict
    # -> dropped at serialize_bin, so the .bin stays a pure ByteGPT mouth).
    comp_head = None
    if use_comp:
        comp_head = nn.Sequential(nn.Linear(d, COMPLETE_HID), nn.GELU(),
                                  nn.Linear(COMPLETE_HID, d)).to(device)
        print(f"  cls_full completion head: Linear({d}->{COMPLETE_HID}->{d}) "
              f"(TRAINING-ONLY, dropped at serialize)", flush=True)

    params = list(model.parameters())
    if comp_head is not None:
        params += list(comp_head.parameters())       # trained jointly; dropped after
    opt = torch.optim.AdamW(params, lr=a.lr, betas=(0.9, 0.95),
                            eps=1e-8, weight_decay=0.0)
    gen = torch.Generator().manual_seed(42)          # data RNG (fair, shared across arms)
    val_gen = torch.Generator().manual_seed(1234)
    obj_gen = torch.Generator(device=device).manual_seed(20260628 + a.seed)  # infonce/mask RNG

    latch = {"on": False, "at": 0}
    i0 = GZ_UPPER
    i_floor = GZ_LOWER - 0.05

    # ── corpus cells ─────────────────────────────────────────────────────────
    cells, labels = [], []
    for ci, spec in enumerate(a.corpus):
        p = resolve_corpus_path(spec)
        cells.append(ByteCell(p, val_frac=a.val_frac))
        labels.append(a.cell_label[ci] if ci < len(a.cell_label) else f"cell{ci}")
        c = cells[-1]
        print(f"  corpus cell[{ci}] {labels[ci]:<12s} {p} size={c.size} "
              f"train={c.train_end} val_tail={c.size - c.train_end}", flush=True)
    if not cells:
        print("  corpus: NONE -> synthetic smoke", flush=True)

    # FAIL-LOUD effective-bytes check (a_chat_registers: 실효 bytes, not intent)
    _usable = [c for c in cells if c.train_end >= seq_len + 2]
    if cells and len(_usable) < len(cells):
        miss = [labels[i] for i, c in enumerate(cells) if c.train_end < seq_len + 2]
        print(f"  *** FAIL-LOUD: {len(_usable)}/{len(cells)} cells usable; "
              f"undersized={miss} (a_chat_registers 실효 bytes) ***", flush=True)
    _samp_cells = _usable
    _samp_w = torch.tensor([float(c.train_end) for c in _samp_cells]) if _samp_cells else torch.tensor([1.0])

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
        # held-out CE is ALWAYS plain marginal CE (arm-independent generalization metric).
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
                    _, vl = model(vx, vy)
            else:
                _, vl = model(vx, vy)
            tot += float(vl.detach()); nb += 1
        if was: model.train()
        return (tot / nb) if nb else None

    def val_per_cell():
        return {lab: v for lab, c in zip(labels, cells) if (v := cell_val_ce(c)) is not None}

    # ── train loop (savant inhibition schedule, verbatim arithmetic) ──────────
    model.train()
    t0 = time.time(); loss0 = lossF = None; last_aux = {}
    for step in range(1, steps + 1):
        if savant_on:
            inh = savant_inhibition(step, steps, i0, i_floor, latch)
            wd = inhibition_to_wd(inh); dp = inhibition_to_dropout(inh)
        else:
            wd, dp = 0.0, 0.0
        for grp in opt.param_groups:
            grp["weight_decay"] = wd
        model.set_dropout(dp)
        x, y = get_batch(step)
        opt.zero_grad(set_to_none=True)
        if a.bf16 and device == "cuda":
            with torch.autocast("cuda", dtype=torch.bfloat16):
                if use_cls:
                    logits, _, pen = model(x, y, return_pen=True)
                    obj_loss, aux = loss_cls(logits.float(), pen.float(), y, V,
                                             use_sep, use_comp, comp_head, obj_gen)
                else:
                    logits, _ = model(x, y)
                    obj_loss, aux = objfn(logits.float(), y, V, obj_gen)
            obj_loss.backward()
        else:
            if use_cls:
                logits, _, pen = model(x, y, return_pen=True)
                obj_loss, aux = loss_cls(logits, pen, y, V,
                                         use_sep, use_comp, comp_head, obj_gen)
            else:
                logits, _ = model(x, y)
                obj_loss, aux = objfn(logits, y, V, obj_gen)
            obj_loss.backward()
        torch.nn.utils.clip_grad_norm_(params, 1.0)
        opt.step()
        ce = float(_ce(logits.float(), y, V).detach())  # plain CE always logged
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
            print(f"  step {step:5d}  CE={ce:.5f}  wd={wd:.4f} dp={dp:.4f}{vtxt}{atxt}", flush=True)
    wall = time.time() - t0

    # ── FINAL held-out val per register (DESCENT gate, plain CE) ──────────────
    uniform = math.log(V)
    per = val_per_cell()
    descent = {}; n_desc = 0
    print(f"  ── FINAL held-out val-CE per register (uniform={uniform:.4f}) ──", flush=True)
    for lab, vc in per.items():
        ok = vc < uniform
        n_desc += int(ok)
        descent[lab] = {"val_ce": round(vc, 5), "descent": ok}
        print(f"     {lab:<12s} val_CE={vc:.5f}  {'DESCENT' if ok else 'NO-DESCENT'}", flush=True)
    final_val = (sum(per.values()) / len(per)) if per else None
    print(f"  FINAL val_CE(pooled)={final_val}  registers_DESCENT={n_desc}/{len(per)}", flush=True)
    print(f"  loss0={loss0:.5f} lossF={lossF:.5f} wall={wall:.1f}s "
          f"savant_latched_at={latch['at']}", flush=True)

    cfg = {"vocab": V, "d": d, "n_layer": L, "n_head": nh, "block": block, "n_params": n_params}

    # ── persist torch ckpt (ALWAYS — a_fire_recover_complete). Only ByteGPT sd;
    #    comp_head is training-only and deliberately NOT persisted. ─────────────
    sd = {k: v.detach().cpu() for k, v in model.state_dict().items()}
    if a.out:
        os.makedirs(os.path.dirname(a.out) or ".", exist_ok=True)
        torch.save({"model": sd, "config": cfg}, a.out)
        sha = hashlib.sha256(open(a.out, "rb").read()).hexdigest()
        print(f"  torch ckpt -> {a.out} ({os.path.getsize(a.out)} bytes) sha={sha}", flush=True)

    # ── serialize .bin (engine-loadable; tied head handled) ──────────────────
    bin_sha = None
    if a.bin_out:
        os.makedirs(os.path.dirname(a.bin_out) or ".", exist_ok=True)
        nb = serialize_bin(sd, cfg, a.bin_out)
        bin_sha = hashlib.sha256(open(a.bin_out, "rb").read()).hexdigest()
        print(f"  .bin WRITTEN {nb} bytes -> {a.bin_out} sha={bin_sha}", flush=True)

    # ── summary json ──────────────────────────────────────────────────────────
    summary = {"objective": a.objective, "seed": a.seed, "n_params": n_params, "config": cfg,
               "loss0": round(loss0, 5), "lossF": round(lossF, 5), "wall_s": round(wall, 1),
               "uniform_ce": round(uniform, 5),
               "final_val_ce_pooled": (round(final_val, 5) if final_val else None),
               "registers_descent": f"{n_desc}/{len(per)}", "heldout_descent": descent,
               "last_aux": last_aux, "savant_latched_at": latch["at"], "bin_sha256": bin_sha,
               "lambda_sep": LAMBDA_SEP, "lambda_comp": LAMBDA_COMP,
               "tier": "engine-native-eligible (.bin ByteGPT mouth); torch train is bridge"}
    if a.json_out:
        with open(a.json_out, "w") as f:
            json.dump(summary, f, ensure_ascii=False, indent=2)
        print(f"  summary -> {a.json_out}", flush=True)


if __name__ == "__main__":
    main()
