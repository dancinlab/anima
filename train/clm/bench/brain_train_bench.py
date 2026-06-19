"""brain_train_bench.py — 4-arm TOY benchmark: do brain-derived auxiliary
TRAINING signals help a small byte-CLM lower held-out CE?

EVERYTHING IS TOY (CPU, $0, fast — a_toy_scale_recheck):
  - toy byte-CLM (<1M params, reuses CLM/model CLMConvMoE *shape*: dilated
    causal conv trunk + MoE conv layer, no attention).
  - NO real TRIBE forward, NO real/live EEG, NO GPU, NO human gate.
  - Every "brain signal" is a SYNTHETIC, seeded, frozen surrogate generated
    from the byte text itself. It is NOT facebook/tribev2, NOT real EEG.

Arms (each = CE + lambda * aux_loss, SAME corpus/seed/steps/arch as baseline):
  baseline   : CE only (lambda = 0).
  Arm 1 TRIBE        : aux = MSE(proj(hidden), pseudo_BOLD(text))
                       pseudo_BOLD = frozen smooth (neighbor-correlated)
                       text-embed -> N-vertex cortical-shaped map.
  Arm 2 EEG          : aux = MSE(proj(hidden), eeg5(text))
                       eeg5 = frozen synthetic 5-channel tension target
                       [alpha, theta, gamma, 1-delta, beta] per window.
  Arm 3 TRIBE+KOSMOS : Arm-1 pseudo_BOLD vertices REORGANIZED onto the
                       KOSMOS Psi-coordinate layout (coord/lane/radius/tier),
                       then aligned. Comparator = PLAIN Arm-1.
  Arm 4 EEG+KOSMOS   : Arm-2 5ch tension stored AT KOSMOS anchor placements
                       (tension 5ch + coord + tier), then aligned.
                       Comparator = PLAIN Arm-2.

Primary metric = held-out val CE (val_ce_contig + val_ce_rand), gen2 style.
Delta = baseline_val_ce - arm_val_ce  (positive => aux helped).
HOLDS / REFUTED / INCONCLUSIVE decided vs a measured noise band (seed spread).

p7/g5: report the ACTUAL numbers. Closed-negative is a valid result
(a_paper_negative_ok). Do NOT round a REFUTE into a HOLD.
"""
from __future__ import annotations

import argparse
import json
import math
import sys
from dataclasses import dataclass

import torch
import torch.nn as nn
import torch.nn.functional as F


# --------------------------------------------------------------------------- #
# Repro
# --------------------------------------------------------------------------- #
def set_seed(seed: int) -> None:
    torch.manual_seed(seed)
    import random
    random.seed(seed)


# --------------------------------------------------------------------------- #
# Data: byte LM over a fixed small clean corpus
# --------------------------------------------------------------------------- #
@dataclass
class Data:
    train: torch.Tensor   # (Ntr,) long bytes
    val: torch.Tensor     # (Nva,) long bytes


def load_corpus(path: str, max_bytes: int, val_frac: float) -> Data:
    with open(path, "rb") as f:
        raw = f.read()
    if len(raw) > max_bytes:
        raw = raw[:max_bytes]
    arr = torch.tensor(list(raw), dtype=torch.long)
    n_val = int(len(arr) * val_frac)
    # contiguous tail held out (no leakage into train)
    return Data(train=arr[:-n_val], val=arr[-n_val:])


def make_batches(seq: torch.Tensor, block: int, bs: int, n_batches: int,
                 g: torch.Generator) -> list[tuple[torch.Tensor, torch.Tensor]]:
    """Random (x, y=next-byte) blocks."""
    out = []
    hi = len(seq) - block - 1
    for _ in range(n_batches):
        ix = torch.randint(0, hi, (bs,), generator=g)
        x = torch.stack([seq[i:i + block] for i in ix])
        y = torch.stack([seq[i + 1:i + 1 + block] for i in ix])
        out.append((x, y))
    return out


# --------------------------------------------------------------------------- #
# Toy CLM: dilated causal conv trunk + MoE conv layer (CLMConvMoE shape)
# --------------------------------------------------------------------------- #
class CausalDilatedConv1d(nn.Module):
    def __init__(self, ch: int, k: int, dilation: int):
        super().__init__()
        self.pad = (k - 1) * dilation
        self.conv = nn.Conv1d(ch, ch, k, dilation=dilation)

    def forward(self, x):
        return self.conv(F.pad(x, (self.pad, 0)))


class TrunkLayer(nn.Module):
    def __init__(self, d: int, k: int, dilation: int):
        super().__init__()
        self.conv = CausalDilatedConv1d(d, k, dilation)
        self.norm = nn.GroupNorm(1, d)
        self.act = nn.GELU()

    def forward(self, x):
        return x + self.act(self.norm(self.conv(x)))


class ConvExpert(nn.Module):
    def __init__(self, d: int, k: int):
        super().__init__()
        self.conv = CausalDilatedConv1d(d, k, 1)
        self.act = nn.GELU()

    def forward(self, x):
        return self.act(self.conv(x))


class MoEConvLayer(nn.Module):
    def __init__(self, d: int, n_e: int, k: int):
        super().__init__()
        self.experts = nn.ModuleList(ConvExpert(d, k) for _ in range(n_e))
        self.router = nn.Conv1d(d, n_e, 1)

    def forward(self, x):
        probs = F.softmax(self.router(x), dim=1)            # (B, n_e, T)
        ex = torch.stack([e(x) for e in self.experts], 1)   # (B, n_e, C, T)
        return (probs.unsqueeze(2) * ex).sum(1)             # (B, C, T)


class ToyCLM(nn.Module):
    """Small byte LM. Exposes `hidden` (pre-readout) so an aux head can
    align it to a brain-shaped target."""

    def __init__(self, vocab=256, d=64, n_trunk=2, n_e=4, k=3,
                 bold_n=256, eeg_n=5):
        super().__init__()
        self.embed = nn.Embedding(vocab, d)
        self.embed_conv = CausalDilatedConv1d(d, k, 1)
        dils = [2 ** i for i in range(n_trunk)]
        self.trunk = nn.ModuleList(TrunkLayer(d, k, dl) for dl in dils)
        self.moe = MoEConvLayer(d, n_e, k)
        self.norm_out = nn.GroupNorm(1, d)
        self.readout = nn.Conv1d(d, vocab, 1)
        # aux projection heads (only used by aux arms; cheap, shared shape)
        self.bold_head = nn.Linear(d, bold_n)
        self.eeg_head = nn.Linear(d, eeg_n)

    def forward(self, tokens):
        x = self.embed(tokens).transpose(1, 2)   # (B, C, T)
        x = self.embed_conv(x)
        for layer in self.trunk:
            x = layer(x)
        x = self.moe(x)
        h = self.norm_out(x)                       # (B, C, T) hidden
        logits = self.readout(h)                   # (B, V, T)
        return logits, h


# --------------------------------------------------------------------------- #
# Frozen "text-embedding" used to synthesize ALL brain targets.
# A fixed (seeded) random byte-embedding -> a per-position feature vector.
# This is deterministic given the bytes, and is NOT the model's own embedding
# (so the aux target is a genuine external regression target, not trivially
#  reconstructable from the model's first layer).
# --------------------------------------------------------------------------- #
class FrozenTextEmbed:
    def __init__(self, d_feat: int, seed: int):
        g = torch.Generator().manual_seed(seed)
        self.W = torch.randn(256, d_feat, generator=g)  # byte -> feature
        self.d = d_feat

    def feat(self, tokens: torch.Tensor) -> torch.Tensor:
        # tokens (B, T) -> (B, T, d_feat), smoothed over a small causal window
        f = self.W[tokens]                              # (B, T, d)
        # depthwise causal smoothing (mimic temporal context binding)
        f = f.transpose(1, 2)                           # (B, d, T)
        f = F.avg_pool1d(F.pad(f, (2, 0)), kernel_size=3, stride=1)
        return f.transpose(1, 2)                        # (B, T, d)


# --------------------------------------------------------------------------- #
# Brain-target generators (all FROZEN, seeded, synthetic).
# --------------------------------------------------------------------------- #
class PseudoBOLD:
    """Arm 1: text-feature -> N-vertex cortical-shaped BOLD map with SPATIAL
    smoothness (neighbor-correlated vertices), mimicking an Hc-style map shape.
    Frozen linear map + a fixed neighbor-averaging (smoothness) operator."""

    def __init__(self, d_feat: int, n_vert: int, seed: int, kosmos_perm=None):
        g = torch.Generator().manual_seed(seed)
        self.M = torch.randn(d_feat, n_vert, generator=g) / math.sqrt(d_feat)
        self.n = n_vert
        # spatial smoothness: averaging over a ring of neighbors on a 1-D
        # cortical-strip layout (vertices ordered by position).
        self.smooth_k = 5
        self.perm = kosmos_perm  # if set, reorder vertices by KOSMOS layout

    def target(self, feat: torch.Tensor) -> torch.Tensor:
        # feat (B, T, d) -> (B, T, n_vert), then smooth ACROSS VERTICES
        b = feat @ self.M                                # (B, T, n)
        bt = b.reshape(-1, 1, self.n)                    # (BT, 1, n)
        pad = self.smooth_k // 2
        bt = F.avg_pool1d(F.pad(bt, (pad, pad), mode="replicate"),
                          kernel_size=self.smooth_k, stride=1)
        b = bt.reshape(b.shape)
        if self.perm is not None:
            b = b[..., self.perm]
        return b


class EEG5:
    """Arm 2: synthetic 5-channel tension target [alpha, theta, gamma, 1-delta,
    beta] per position. Frozen band-projection of the text feature, squashed
    into a bounded tension range. Echoes BRAIN/eeg coupled-vs-indep big-Phi
    idea: channels are correlated (a shared coupling factor), NOT independent."""

    def __init__(self, d_feat: int, seed: int, kosmos_anchor=None):
        g = torch.Generator().manual_seed(seed)
        self.B = torch.randn(d_feat, 5, generator=g) / math.sqrt(d_feat)
        # shared coupling vector -> introduces cross-channel correlation
        self.couple = torch.randn(d_feat, 1, generator=g) / math.sqrt(d_feat)
        self.anchor = kosmos_anchor  # (5,) additive KOSMOS-tier offset, or None

    def target(self, feat: torch.Tensor) -> torch.Tensor:
        bands = feat @ self.B                            # (B, T, 5)
        shared = feat @ self.couple                      # (B, T, 1)
        t = torch.tanh(bands + 0.5 * shared)             # bounded tension
        if self.anchor is not None:
            t = t + self.anchor                          # KOSMOS-anchored shift
        return t


# --------------------------------------------------------------------------- #
# KOSMOS Psi-coordinate layout (toy, from HEXAD/KOSMOS.md anchor shape).
# coord=[x,y] in Psi-space, lane (partition), radius (scope), tier (ordinal).
# We build a deterministic 2-D Psi placement of the BOLD vertices and a
# tier-based offset for the EEG channels.
# --------------------------------------------------------------------------- #
def kosmos_vertex_permutation(n_vert: int, seed: int) -> torch.Tensor:
    """Place n_vert vertices on a 2-D Psi grid, then order them by a
    space-filling traversal (Hilbert-ish: sort by lane then radius then
    angle). The PERMUTATION reorganizes the plain (positional) vertex order
    into the KOSMOS cosmic-map order, so spatial smoothness now follows the
    Psi-layout instead of raw index order."""
    g = torch.Generator().manual_seed(seed)
    # 2-D Psi coords in [0,1]^2
    coord = torch.rand(n_vert, 2, generator=g)
    # lane = quadrant partition (MITOSIS cell id), radius = dist from centre
    lane = (coord[:, 0] > 0.5).long() * 2 + (coord[:, 1] > 0.5).long()
    centre = torch.tensor([0.5, 0.5])
    radius = (coord - centre).norm(dim=1)
    angle = torch.atan2(coord[:, 1] - 0.5, coord[:, 0] - 0.5)
    # KOSMOS order: lane, then radius shell, then angle (constellation walk)
    key = lane.float() * 10.0 + radius * 3.0 + (angle + math.pi) / (2 * math.pi)
    return torch.argsort(key)


def kosmos_eeg_anchor(seed: int, tier: int = 77) -> torch.Tensor:
    """A KOSMOS anchor placement -> a tier-scaled 5-channel tension offset.
    tier (Knuth ordinal) scales the anchored shift; coord/lane select which
    channels the anchor emphasizes (the a_kosmos tension 5-ch payload shape)."""
    g = torch.Generator().manual_seed(seed)
    base = torch.randn(5, generator=g)
    return (tier / 100.0) * torch.tanh(base) * 0.3       # bounded anchored shift


# --------------------------------------------------------------------------- #
# Train + eval
# --------------------------------------------------------------------------- #
@dataclass
class ArmCfg:
    name: str
    lam: float
    aux: str            # "none" | "bold" | "eeg"
    kosmos: bool


def eval_val(model: ToyCLM, data: Data, block: int, seed: int):
    """val_ce_contig (sliding windows over the held-out tail) + val_ce_rand
    (random windows). gen2 style."""
    model.eval()
    with torch.no_grad():
        # contiguous: tile the val tail into non-overlapping blocks
        v = data.val
        n = (len(v) - 1) // block
        xs = torch.stack([v[i * block:(i + 1) * block] for i in range(n)])
        ys = torch.stack([v[i * block + 1:(i + 1) * block + 1] for i in range(n)])
        logits, _ = model(xs)
        ce_contig = F.cross_entropy(
            logits.transpose(1, 2).reshape(-1, 256), ys.reshape(-1)).item()
        # random windows
        g = torch.Generator().manual_seed(seed + 999)
        batches = make_batches(v, block, bs=16, n_batches=8, g=g)
        tot, cnt = 0.0, 0
        for x, y in batches:
            lg, _ = model(x)
            tot += F.cross_entropy(
                lg.transpose(1, 2).reshape(-1, 256), y.reshape(-1)).item()
            cnt += 1
        ce_rand = tot / cnt
    return ce_contig, ce_rand


def run_arm(cfg: ArmCfg, data: Data, *, seed: int, steps: int, block: int,
            bs: int, d: int, bold_n: int, frozen: FrozenTextEmbed,
            bold_plain: PseudoBOLD, bold_kosmos: PseudoBOLD,
            eeg_plain: EEG5, eeg_kosmos: EEG5):
    set_seed(seed)
    model = ToyCLM(d=d, bold_n=bold_n)
    opt = torch.optim.AdamW(model.parameters(), lr=3e-3)
    g = torch.Generator().manual_seed(seed + 1)
    batches = make_batches(data.train, block, bs, steps, g)

    model.train()
    for x, y in batches:
        logits, h = model(x)                              # h: (B, C, T)
        ce = F.cross_entropy(
            logits.transpose(1, 2).reshape(-1, 256), y.reshape(-1))
        loss = ce
        if cfg.aux != "none" and cfg.lam > 0:
            feat = frozen.feat(x)                          # (B, T, d_feat)
            ht = h.transpose(1, 2)                         # (B, T, C)
            if cfg.aux == "bold":
                gen = bold_kosmos if cfg.kosmos else bold_plain
                tgt = gen.target(feat)                     # (B, T, n_vert)
                pred = model.bold_head(ht)
            else:  # eeg
                gen = eeg_kosmos if cfg.kosmos else eeg_plain
                tgt = gen.target(feat)                     # (B, T, 5)
                pred = model.eeg_head(ht)
            aux = F.mse_loss(pred, tgt)
            loss = ce + cfg.lam * aux
        opt.zero_grad()
        loss.backward()
        opt.step()

    ce_contig, ce_rand = eval_val(model, data, block, seed)
    return {"val_ce_contig": ce_contig, "val_ce_rand": ce_rand,
            "val_ce": 0.5 * (ce_contig + ce_rand)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--corpus", default="CORE/testdata/clm_mid_5lang_c4.txt")
    ap.add_argument("--max-bytes", type=int, default=120_000)
    ap.add_argument("--val-frac", type=float, default=0.15)
    ap.add_argument("--steps", type=int, default=400)
    ap.add_argument("--block", type=int, default=64)
    ap.add_argument("--bs", type=int, default=16)
    ap.add_argument("--d", type=int, default=64)
    ap.add_argument("--bold-n", type=int, default=256)
    ap.add_argument("--seeds", type=int, nargs="+", default=[0, 1, 2])
    ap.add_argument("--out", default=None, help="JSON results path")
    args = ap.parse_args()

    data = load_corpus(args.corpus, args.max_bytes, args.val_frac)
    n_params = sum(p.numel() for p in ToyCLM(d=args.d, bold_n=args.bold_n).parameters())
    print(f"# corpus={args.corpus} train={len(data.train)}B val={len(data.val)}B "
          f"params={n_params} (<1M: {n_params < 1_000_000})")
    print(f"# steps={args.steps} block={args.block} bs={args.bs} d={args.d} "
          f"bold_n={args.bold_n} seeds={args.seeds}")

    # Frozen surrogate generators (seed-fixed, shared across all arms/seeds)
    FROZEN_SEED = 12345
    frozen = FrozenTextEmbed(d_feat=32, seed=FROZEN_SEED)
    perm = kosmos_vertex_permutation(args.bold_n, seed=FROZEN_SEED + 7)
    bold_plain = PseudoBOLD(32, args.bold_n, seed=FROZEN_SEED + 1, kosmos_perm=None)
    bold_kosmos = PseudoBOLD(32, args.bold_n, seed=FROZEN_SEED + 1, kosmos_perm=perm)
    anchor = kosmos_eeg_anchor(seed=FROZEN_SEED + 2, tier=77)
    eeg_plain = EEG5(32, seed=FROZEN_SEED + 3, kosmos_anchor=None)
    eeg_kosmos = EEG5(32, seed=FROZEN_SEED + 3, kosmos_anchor=anchor)

    # Arm matrix: baseline (lam=0) + 4 arms x lam{0.1,1.0}
    arms = [ArmCfg("baseline", 0.0, "none", False)]
    for lam in (0.1, 1.0):
        arms.append(ArmCfg("TRIBE", lam, "bold", False))
        arms.append(ArmCfg("EEG", lam, "eeg", False))
        arms.append(ArmCfg("TRIBE-KOSMOS", lam, "bold", True))
        arms.append(ArmCfg("EEG-KOSMOS", lam, "eeg", True))

    results = {}
    for arm in arms:
        key = f"{arm.name}@lam{arm.lam}"
        per_seed = []
        for s in args.seeds:
            r = run_arm(arm, data, seed=s, steps=args.steps, block=args.block,
                        bs=args.bs, d=args.d, bold_n=args.bold_n, frozen=frozen,
                        bold_plain=bold_plain, bold_kosmos=bold_kosmos,
                        eeg_plain=eeg_plain, eeg_kosmos=eeg_kosmos)
            per_seed.append(r)
            print(f"  {key:24s} seed={s} "
                  f"contig={r['val_ce_contig']:.5f} rand={r['val_ce_rand']:.5f} "
                  f"val_ce={r['val_ce']:.5f}")
        vals = [r["val_ce"] for r in per_seed]
        mean = sum(vals) / len(vals)
        std = (sum((v - mean) ** 2 for v in vals) / max(1, len(vals) - 1)) ** 0.5
        results[key] = {"arm": arm.name, "lam": arm.lam, "aux": arm.aux,
                        "kosmos": arm.kosmos, "per_seed": per_seed,
                        "val_ce_mean": mean, "val_ce_std": std}
        print(f"  {key:24s} MEAN val_ce={mean:.5f} +/- {std:.5f}")

    out = {"meta": {"corpus": args.corpus, "max_bytes": args.max_bytes,
                    "steps": args.steps, "block": args.block, "bs": args.bs,
                    "d": args.d, "bold_n": args.bold_n, "seeds": args.seeds,
                    "n_params": n_params}, "results": results}
    if args.out:
        with open(args.out, "w") as f:
            json.dump(out, f, indent=2)
        print(f"# wrote {args.out}")
    return out


if __name__ == "__main__":
    main()
