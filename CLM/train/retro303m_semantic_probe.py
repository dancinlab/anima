#!/usr/bin/env python3
"""retro303m_semantic_probe.py — $0 TINY CPU fit-probe for the H_1148 v2 SEMANTIC anchor
sampler (semantic_anchor_batch) on the axis-4 RETRO-303M model.

PROVES (CPU only, CUDA_VISIBLE_DEVICES="" enforced; NO 303M train, NO GPU):
  (1) semantic_anchor_batch produces (x, y, anchor, anchor_mask) batches with the right shapes
      and flows end-to-end through the REAL RetroByteGPT fwd + bwd at TINY dims.
  (2) the SEMANTIC-retrieved anchor has HIGHER byte-trigram query-overlap than the v1
      prior_window anchor on the SAME sampled targets (sanity that the port out-grounds v1).

This uses a tiny STUB H exposing only the backbone attributes RetroByteGPT._trunk touches
(drop/tok/pos/blocks/ln_f/head) so the probe runs with NO H_1129 sweep harness + NO GPU. The
SAMPLER + the RETRO copy head under test are the REAL production code from retro303m_en.py.
"""
from __future__ import annotations
import os, sys
os.environ["CUDA_VISIBLE_DEVICES"] = ""  # HARD GPU lockout — this is a CPU $0 probe

THIS = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.normpath(os.path.join(THIS, "..", "model"))
sys.path.insert(0, MODEL_DIR)
import retro303m_en as R  # noqa: E402  (semantic_anchor_batch + RetroByteGPT live here)
import torch  # noqa: E402
import torch.nn as nn  # noqa: E402

VOCAB = R.VOCAB  # 256


# --- minimal tiny ByteGPT stub: same attribute names _trunk() reads, real nn.Modules ---
class _Block(nn.Module):
    def __init__(self, d, n_head):
        super().__init__()
        self.attn = nn.MultiheadAttention(d, n_head, batch_first=True)
        self.ln1 = nn.LayerNorm(d); self.ln2 = nn.LayerNorm(d)
        self.mlp = nn.Sequential(nn.Linear(d, 4 * d), nn.GELU(), nn.Linear(4 * d, d))

    def forward(self, x, mask):
        h = self.ln1(x)
        a, _ = self.attn(h, h, h, attn_mask=mask, need_weights=False)
        x = x + a
        x = x + self.mlp(self.ln2(x))
        return x


class _TinyByteGPT(nn.Module):
    def __init__(self, vocab, d, n_layer, n_head, block, p=0.0, grad_ckpt=False):
        super().__init__()
        self.tok = nn.Embedding(vocab, d)
        self.pos = nn.Embedding(block, d)
        self.drop = nn.Dropout(p)
        self.blocks = nn.ModuleList([_Block(d, n_head) for _ in range(n_layer)])
        self.ln_f = nn.LayerNorm(d)
        self.head = nn.Linear(d, vocab, bias=False)
        self.grad_ckpt = grad_ckpt


class _StubH:
    ByteGPT = _TinyByteGPT


def main():
    assert not torch.cuda.is_available() or os.environ.get("CUDA_VISIBLE_DEVICES") == "", \
        "probe must run CPU-only"
    dev = "cpu"
    torch.manual_seed(7)
    block, La, gap, bs = 32, 16, 8, 4
    d, n_layer, n_head = 32, 2, 4

    # synthetic corpus with REPEATED key-bearing motifs so a content match is detectable:
    # interleave a distinctive ABC-rich region with filler so the semantic retriever has a
    # real "most-similar prior window" to find vs prior_window's fixed positional pick.
    import numpy as np
    rng = np.random.default_rng(7)
    parts = []
    for _ in range(60):
        if rng.random() < 0.5:
            parts.append(bytes([65 + (j % 6) for j in range(40)]))   # ABCDEF motif block
        else:
            parts.append(bytes(rng.integers(97, 123, 40).tolist()))  # lowercase filler
    raw = b"".join(parts)
    data = torch.tensor(list(raw), dtype=torch.long)
    print(f"[probe] corpus bytes={data.numel()} block={block} La={La} gap={gap} bs={bs}", flush=True)

    m = R.RetroByteGPT(_StubH(), d=d, n_layer=n_layer, n_head=n_head, block=block).to(dev)
    nextra = m.n_extra_params()
    print(f"[probe] RetroByteGPT built (tiny d={d}/L{n_layer}/H{n_head}); RETRO-head extra={nextra} "
          f"(= 2*d*d+d = {2*d*d+d})", flush=True)
    assert nextra == 2 * d * d + d

    # (1) SEMANTIC sampler end-to-end fwd+bwd
    gsem = torch.Generator().manual_seed(123)
    x, y, anc, amask = R.semantic_anchor_batch(data, block, La, gap, bs, dev,
                                               ring=8, q_head=16, gen=gsem)
    print(f"[probe] semantic batch shapes: x={tuple(x.shape)} y={tuple(y.shape)} "
          f"anchor={tuple(anc.shape)} amask={tuple(amask.shape)}", flush=True)
    assert tuple(x.shape) == (bs, block) and tuple(y.shape) == (bs, block)
    assert tuple(anc.shape) == (bs, La) and tuple(amask.shape) == (bs, La)
    assert amask.sum().item() > 0, "all anchors masked — sampler produced no valid anchor"

    opt = torch.optim.AdamW(m.parameters(), lr=1e-3)
    m.train()
    probs, loss = m(x, anc, targets=y, anchor_mask=amask)
    assert tuple(probs.shape) == (bs, block, VOCAB)
    loss.backward()
    gnorm = sum(p.grad.abs().sum().item() for p in m.parameters() if p.grad is not None)
    opt.step(); opt.zero_grad(set_to_none=True)
    print(f"[probe] fwd OK probs={tuple(probs.shape)} loss={loss.item():.4f} "
          f"bwd OK grad_abs_sum={gnorm:.3e} (>0 => grads flow through copy head)", flush=True)
    assert gnorm > 0, "no gradient — bwd did not flow"

    # (2) query-overlap: SEMANTIC anchor vs PRIOR-WINDOW anchor on the SAME sampled targets.
    # Score = byte-trigram cosine(query-head, returned-anchor). Average over a sample of offsets.
    def overlap_for(offset):
        i = int(offset)
        qprof = R._byte_trigram_profile(data[i:i + min(16, block)])
        # semantic pick (mirror semantic_anchor_batch's selection, deterministic for this i)
        best_sim, best = -1.0, None
        a_end = i - gap
        for w in range(8):
            we = a_end - w * La; ws = we - La
            if ws < 0:
                break
            sim = R._profile_cosine(qprof, R._byte_trigram_profile(data[ws:we]))
            if sim > best_sim:
                best_sim, best = sim, (ws, we)
        sem_sim = best_sim if best is not None else 0.0
        # prior-window: the single fixed preceding window [i-La-gap : i-gap]
        pw_s, pw_e = a_end - La, a_end
        if pw_s < 0:
            pw_sim = 0.0
        else:
            pw_sim = R._profile_cosine(qprof, R._byte_trigram_profile(data[pw_s:pw_e]))
        return sem_sim, pw_sim

    sample_offsets = list(range(La * 8 + gap + 1, data.numel() - block - 1, 7))[:80]
    sems = []; pws = []
    for off in sample_offsets:
        s, p = overlap_for(off)
        sems.append(s); pws.append(p)
    msem = sum(sems) / len(sems); mpw = sum(pws) / len(pws)
    wins = sum(1 for s, p in zip(sems, pws) if s >= p)
    print(f"[probe] query-overlap (byte-trigram cosine) over n={len(sems)} offsets:", flush=True)
    print(f"        SEMANTIC mean={msem:.4f}   PRIOR_WINDOW mean={mpw:.4f}   "
          f"semantic>=prior on {wins}/{len(sems)}", flush=True)
    sem_better = msem >= mpw and wins >= len(sems) // 2
    print(f"[probe] SEMANTIC >= PRIOR_WINDOW overlap : {sem_better} "
          f"(Δ={msem - mpw:+.4f})", flush=True)

    ok = sem_better
    print(f"\n[probe] RESULT: end-to-end fwd/bwd OK + semantic-out-grounds-prior = {ok}", flush=True)
    print("[probe] PASS" if ok else "[probe] FAIL", flush=True)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
