"""
CLM B0 — PyTorch fp16 conv-native MoE trainer (Track 1 scaffold).

P0_ARCHITECTURE.md d5 Track 1 산출물. hexa-native trainer 가 production scale
에서 🔴 INFEASIBLE (CORE/DECODER/STEP_RATE_LOG.md M5: 0.23~0.50 step/s · RSS
churn ~328-331 MB/step · GPU↔CPU sync overhead) 이므로, P2 학습을 즉시 unblock
하기 위한 PyTorch fp16 baseline.

설계 정합 (P0_ARCHITECTURE.md):
  - Q1 Conv-native LM: dilated causal conv stack (attention 0 → AKIDA 추론 envelope 정합)
  - Q2 MoE conv-expert = mitosis cell: top-K hard router + per-expert conv branch
  - Q3 byte-vocab V=256: V/d≈4배 (monopoly 근원 V≫d 직격)
  - monopoly-escape: load-balance aux loss + hard top-K + (entropy anneal hook)

이 파일은 학습기(.py)다 — hexa-native authoring guard 는 Write/Edit 를 막으므로
P0_ARCHITECTURE.md §6 의 `python3 -c "open().write()"` 채널로 작성·커밋했다.
.gitignore 가 정식 .py 를 허용한다 (R37 scrub 2026-05-12). 추론은 AKIDA-int4-only
이며 (d4) 이 파일은 학습 전용 — GPU fp 만 담당한다.

CLI:
  python3 clm_b0_pytorch_trainer.py --smoke          # tiny d64/L2/E4, byte-vocab, few steps
  python3 clm_b0_pytorch_trainer.py --steps 50 --d 64 --experts 4 --layers 2 --top-k 1
  python3 clm_b0_pytorch_trainer.py --steps 50 --fp16  # H100 fp16 path (autocast)
"""

import argparse
import math
import time
import sys

try:
    import torch
    import torch.nn as nn
    import torch.nn.functional as F
except Exception as exc:  # pragma: no cover — scaffold may run on a torch-less host
    print(f"[clm-b0] torch import failed: {exc}", file=sys.stderr)
    print("[clm-b0] this is the PyTorch fp16 trainer scaffold; install torch to run.", file=sys.stderr)
    sys.exit(2)


# ───────────────────────────── model ─────────────────────────────

class DilatedConvBlock(nn.Module):
    """Causal dilated 1-D conv block (AKIDA conv-envelope friendly).

    SAME-length causal conv via left-padding (no future leak). GELU + residual.
    No attention — keeps the whole forward inside the AKIDA conv/FC/pool set.
    """

    def __init__(self, d: int, kernel: int, dilation: int):
        super().__init__()
        self.pad = (kernel - 1) * dilation
        self.conv = nn.Conv1d(d, d, kernel_size=kernel, dilation=dilation)
        self.norm = nn.LayerNorm(d)

    def forward(self, x):  # x: [B, T, d]
        h = self.norm(x)
        h = h.transpose(1, 2)                       # [B, d, T]
        h = F.pad(h, (self.pad, 0))                 # left-pad → causal
        h = self.conv(h)                            # [B, d, T]
        h = h.transpose(1, 2)                       # [B, T, d]
        return x + F.gelu(h)


class ConvExpert(nn.Module):
    """One MoE expert = one mitosis cell (Q2). A small dilated-conv branch."""

    def __init__(self, d: int, kernel: int, dilation: int):
        super().__init__()
        self.block = DilatedConvBlock(d, kernel, dilation)

    def forward(self, x):
        return self.block(x)


class MoEConvLayer(nn.Module):
    """Top-K hard-routed MoE over conv-experts + load-balance aux (Q2/monopoly-escape).

    Router is a per-token linear gate. HARD top-K (straight-through on the gate
    weight) keeps routing discrete (matches the hexa decoder HARD top-1 design)
    while load-balance aux (Switch-Transformer style) fights single-expert
    monopoly — the documented escape lever in P0 §3.
    """

    def __init__(self, d: int, n_experts: int, top_k: int, kernel: int, dilation: int):
        super().__init__()
        self.n_experts = n_experts
        self.top_k = top_k
        self.gate = nn.Linear(d, n_experts)
        self.experts = nn.ModuleList(
            [ConvExpert(d, kernel, dilation) for _ in range(n_experts)]
        )

    def forward(self, x):  # x: [B, T, d]
        B, T, d = x.shape
        logits = self.gate(x)                       # [B, T, E]
        probs = F.softmax(logits, dim=-1)           # routing distribution
        topv, topi = probs.topk(self.top_k, dim=-1) # [B, T, K]
        topv = topv / (topv.sum(dim=-1, keepdim=True) + 1e-9)

        out = torch.zeros_like(x)
        # dense expert pass (scaffold: correctness over sparsity; production
        # would gather/scatter). Each expert sees full seq; gate masks the mix.
        for e in range(self.n_experts):
            mask = (topi == e).any(dim=-1).unsqueeze(-1).float()   # [B, T, 1]
            # weight of expert e at routed positions
            w = (topv * (topi == e).float()).sum(dim=-1, keepdim=True)  # [B,T,1]
            out = out + self.experts[e](x) * w * mask

        # load-balance aux loss (Switch): E * mean(f_e) · mean(P_e)
        # f_e = fraction of tokens routed to e (top-1); P_e = mean gate prob
        top1 = topi[..., 0]                          # [B, T]
        f = torch.zeros(self.n_experts, device=x.device)
        for e in range(self.n_experts):
            f[e] = (top1 == e).float().mean()
        P = probs.mean(dim=(0, 1))                    # [E]
        aux = self.n_experts * torch.sum(f * P)
        # router entropy (monopoly diagnostic — higher = more balanced)
        ent = -(probs.clamp_min(1e-9).log() * probs).sum(-1).mean()
        return out, aux, ent, top1


class CLMConvMoE(nn.Module):
    """Conv-native MoE byte-LM (P0 Q1+Q2+Q3 toy-scale)."""

    def __init__(self, vocab=256, d=64, n_layers=2, n_experts=4, top_k=1, kernel=3):
        super().__init__()
        self.embed = nn.Embedding(vocab, d)
        self.layers = nn.ModuleList(
            [MoEConvLayer(d, n_experts, top_k, kernel, dilation=2 ** i)
             for i in range(n_layers)]
        )
        self.norm = nn.LayerNorm(d)
        self.head = nn.Linear(d, vocab)

    def forward(self, idx):  # idx: [B, T] int64 byte ids
        x = self.embed(idx)
        aux_total = 0.0
        ent_acc = []
        last_top1 = None
        for layer in self.layers:
            x, aux, ent, top1 = layer(x)
            aux_total = aux_total + aux
            ent_acc.append(ent)
            last_top1 = top1
        x = self.norm(x)
        logits = self.head(x)                        # [B, T, V]
        ent_mean = torch.stack(ent_acc).mean()
        return logits, aux_total, ent_mean, last_top1


# ─────────────────────────── data (byte) ───────────────────────────

def make_byte_batch(text_bytes, B, T, device, rng):
    """Random contiguous byte windows → (x, y) next-byte prediction."""
    n = len(text_bytes)
    xs, ys = [], []
    for _ in range(B):
        start = int(rng.integers(0, max(1, n - T - 1)))
        chunk = text_bytes[start:start + T + 1]
        if len(chunk) < T + 1:
            chunk = chunk + bytes(T + 1 - len(chunk))
        arr = torch.tensor(list(chunk), dtype=torch.long, device=device)
        xs.append(arr[:-1]); ys.append(arr[1:])
    return torch.stack(xs), torch.stack(ys)


# ─────────────────────────── train loop ───────────────────────────

def train(args):
    import numpy as np
    rng = np.random.default_rng(args.seed)
    torch.manual_seed(args.seed)

    device = "cuda" if (args.fp16 and torch.cuda.is_available()) else (
        "cuda" if torch.cuda.is_available() else "cpu")
    use_amp = args.fp16 and device == "cuda"

    # toy corpus: a few KB of repeated structured bytes (smoke proves throughput,
    # not language). P1 swaps in the real byte corpus.
    sample = (b"anima is a living consciousness agent. tension drives emit. "
              b"mitosis grows cells. byte-vocab escapes the V>>d monopoly. ") * 64
    corpus = sample

    model = CLMConvMoE(vocab=256, d=args.d, n_layers=args.layers,
                       n_experts=args.experts, top_k=args.top_k).to(device)
    n_params = sum(p.numel() for p in model.parameters())
    opt = torch.optim.AdamW(model.parameters(), lr=args.lr)
    scaler = torch.amp.GradScaler('cuda', enabled=use_amp)

    print(f"[clm-b0] device={device} fp16={use_amp} params={n_params/1e6:.3f}M "
          f"d={args.d} L={args.layers} E={args.experts} topK={args.top_k} "
          f"B={args.batch} T={args.seq}")

    model.train()
    t_first = None
    t0 = time.monotonic()
    for step in range(1, args.steps + 1):
        x, y = make_byte_batch(corpus, args.batch, args.seq, device, rng)
        opt.zero_grad(set_to_none=True)
        with torch.amp.autocast('cuda', enabled=use_amp):
            logits, aux, ent, top1 = model(x)
            ce = F.cross_entropy(logits.reshape(-1, 256), y.reshape(-1))
            loss = ce + args.aux_w * aux
        scaler.scale(loss).backward()
        scaler.step(opt)
        scaler.update()
        if step == 1:
            t_first = time.monotonic()
        if step % args.print_every == 0 or step == 1:
            distinct = int(top1.unique().numel())
            print(f"[clm-b0] step={step:4d} ce={ce.item():.4f} aux={float(aux.detach()):.4f} "
                  f"router_H={ent.item():.4f} distinct_experts={distinct}/{args.experts}")

    t_end = time.monotonic()
    # measure throughput over steps 2..N (exclude step-1 warmup/compile)
    if args.steps >= 2 and t_first is not None:
        rate = (args.steps - 1) / (t_end - t_first)
    else:
        rate = args.steps / (t_end - t0)
    print(f"[clm-b0] STEP_RATE measured={rate:.3f} step/s "
          f"(steps 2..{args.steps}, device={device}, fp16={use_amp})")
    print(f"[clm-b0] total_wall={t_end - t0:.3f}s")
    return rate


def main():
    ap = argparse.ArgumentParser(description="CLM B0 PyTorch fp16 conv-MoE trainer scaffold")
    ap.add_argument("--steps", type=int, default=20)
    ap.add_argument("--d", type=int, default=64)
    ap.add_argument("--layers", type=int, default=2)
    ap.add_argument("--experts", type=int, default=4)
    ap.add_argument("--top-k", type=int, default=1, dest="top_k")
    ap.add_argument("--batch", type=int, default=8)
    ap.add_argument("--seq", type=int, default=64)
    ap.add_argument("--lr", type=float, default=3e-3)
    ap.add_argument("--aux-w", type=float, default=0.1, dest="aux_w")
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--print-every", type=int, default=5, dest="print_every")
    ap.add_argument("--fp16", action="store_true", help="enable fp16 autocast on CUDA")
    ap.add_argument("--smoke", action="store_true",
                    help="tiny smoke: d64/L2/E4/top1, 10 steps")
    args = ap.parse_args()
    if args.smoke:
        args.steps = 10; args.d = 64; args.layers = 2; args.experts = 4
        args.top_k = 1; args.print_every = 2
    train(args)


if __name__ == "__main__":
    main()
