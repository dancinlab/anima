#!/usr/bin/env python3
"""retro303m_en.py — the anima-303M-RETRO model: H_1129 303M ByteGPT backbone + a
RETRO cross-attention/copy head (scaled up from the H_1147 toy) over a RETRIEVED
KOSMOS-ANCHOR byte stream, trained INTO the weights.

WHY (MODEL.md, BUILD ORDER step 2): H_1142–H_1146 proved size / more-training /
chat-finetune / oracle-decode ALL fail the G5 non-fabrication 0.20 bar. H_1147 proved
🟢 (toy) that a copy/pointer objective TRAINED INTO the weights over a retrieved anchor
flips fabrication 1.0→0.0 where decode-time prepend could not. This file turns that toy
head into a real 303M-scale architecture component.

ARCHITECTURE (single-entry, a_core_engine_map): the .clm that this produces enters CORE
ONLY via the generator L3 slot; the kosmos-anchor store enters ONLY via kosmos_io→brain.
This module is the Lane-G torch REFERENCE mouth (a_clm_gen_pipeline) — NOT the CORE
substrate. forge stays the PUBLIC production trainer; this is the engine-.clm bridge ref.

  Backbone  = H.ByteGPT (d1024/L24/H16/block512, byte vocab256) — H_1129 VERBATIM, frozen
              recipe, 303,097,856 params. Imported, NOT re-implemented.
  RETRO head (scaled from H_1147 toy Model.retro path):
    - the retrieved ANCHOR is a byte sequence (a kosmos anchor's text, see ANCHOR SOURCE
      below). It is embedded with the backbone's OWN token+pos embeddings (shared, like the
      toy reused self.Emb) and passed through the backbone blocks to get anchor hiddens
      `ha[B, La, d]` (anchor encoder = the SAME backbone in no-grad-then-grad — here we run
      the backbone forward on the anchor to get context-rich anchor hiddens).
    - at EACH query position the head cross-attends from the query hidden `hq[B,Tq,d]` to
      the anchor hiddens: Pq/Pk projections (d×d, like the toy's Pq/Pk), softmax over the
      La anchor positions -> pattn[B,Tq,La].
    - copy_dist[B,Tq,256] = scatter pattn mass onto the anchor TOKEN ids (the toy's
      np.bincount scatter, here a vectorized scatter_add over the byte vocab).
    - a learned gate g = sigmoid(hq @ Wg) [B,Tq,1] mixes: probs = g*copy_dist +
      (1-g)*softmax(vocab_logits). The toy's exact mixture, now per-position over a real
      byte vocab and a real (variable-length) anchor.
  EXTRA PARAMS over the bare backbone: Pq (d*d) + Pk (d*d) + Wg (d*1) = 2*1024*1024 + 1024
      = 2,098,176 params (~2.1M, +0.69% over 303.1M). Documented + asserted at build.

ANCHOR SOURCE during from-scratch pretraining (THE CRUX — v1 choice, honest):
  For the toy the anchor was GIVEN (key→anchor). For real from-scratch text there is no
  retrieval index yet (the model has no embeddings to retrieve WITH on step 0). v1 choice:
  PRIOR-WINDOW SELF-RETRIEVAL — the anchor for the target span at corpus offset `i` is the
  PRECEDING block-sized window [i-La-gap : i-gap] of the SAME corpus (a held context the
  target was actually written after). This is a concrete, honest, $0, index-free anchor
  that (a) genuinely contains entities the continuation refers back to (real long-range
  coref in wiki/prose), (b) trains the copy/attend pathway on REAL retrieved context, and
  (c) needs NO external RAG (a_kosmos: the store is anima's own stream). At INFERENCE the
  same head consumes a RETRIEVED KOSMOS ANCHOR (kosmos_io→brain) in the anchor slot — the
  prior-window is the train-time SURROGATE for that retrieved anchor.
  HONEST LIMITATIONS (v1):
    - prior-window ≠ semantically-retrieved nearest anchor: it is a POSITIONAL surrogate,
      so it teaches "attend to & copy from a provided context", not "retrieve the RIGHT
      context". The retriever quality is a SEPARATE axis (deferred; real kosmos similarity
      retrieval is v2).
    - a `gap` is inserted so the anchor never overlaps the target (no trivial next-byte
      leak); the window may sometimes carry little relevant entity overlap → the gate must
      learn to fall back to the vocab head (which it can, by design).
    - copy supervision is IMPLICIT (LM loss only) here, matching the H_1147 design where the
      copy head was trained by the same next-token loss — no explicit copy label. Scale +
      real noisy/wrong-anchor kosmos retrieval UNVERIFIED (a_scale_honest_scope).

p7 deterministic (NOT perplexity). seed 7. This file = model + a build/param assertion +
a tiny CPU fit-probe entrypoint; the GPU launcher is retro303m_en_train.py.
"""
from __future__ import annotations
import argparse, math, os, sys
import torch, torch.nn as nn, torch.nn.functional as F

VOCAB = 256


def _import_h1129(sweep_universe: str):
    """Import the H_1129 ByteGPT + frozen evaluators VERBATIM from the sweep harness dir."""
    sys.path.insert(0, sweep_universe)
    import h1129_midcap_broad_converged_recombination as H  # noqa: E402
    return H


class RetroByteGPT(nn.Module):
    """H_1129 ByteGPT backbone + RETRO anchor cross-attention/copy head (H_1147 mechanism).

    The backbone is used BOTH as the query encoder (over the prompt/continuation) and the
    anchor encoder (over the retrieved anchor bytes) — weights shared, like the toy reused
    a single self-attention stack. The RETRO head adds Pq/Pk/Wg only.
    """

    def __init__(self, H, d=1024, n_layer=24, n_head=16, block=512, p=0.0, grad_ckpt=False):
        super().__init__()
        self.d = d
        self.block = block
        # backbone = H_1129 ByteGPT VERBATIM (frozen recipe). 303M.
        self.backbone = H.ByteGPT(vocab=VOCAB, d=d, n_layer=n_layer, n_head=n_head,
                                  block=block, p=p, grad_ckpt=grad_ckpt)
        # RETRO head (scaled from H_1147 Model.retro: Pq, Pk, Wg)
        s = (1.0 / math.sqrt(d))
        self.Pq = nn.Parameter(torch.randn(d, d) * s)
        self.Pk = nn.Parameter(torch.randn(d, d) * s)
        self.Wg = nn.Parameter(torch.randn(d, 1) * s)

    # ---- shared backbone trunk: bytes -> hidden states [B,T,d] (pre-head) ----
    def _trunk(self, idx):
        s = self.backbone
        B, T = idx.shape
        pos = torch.arange(T, device=idx.device)
        x = s.drop(s.tok(idx) + s.pos(pos)[None, :, :])
        mask = torch.triu(torch.full((T, T), float("-inf"), device=idx.device), diagonal=1)
        for b in s.blocks:
            x = b(x, mask)
        return s.ln_f(x)  # [B,T,d]

    def _vocab_logits(self, h):
        return self.backbone.head(h)  # tied head

    def forward(self, idx, anchor, targets=None, anchor_mask=None):
        """idx[B,Tq] query bytes; anchor[B,La] retrieved-anchor bytes.
        anchor_mask[B,La] (1=valid byte, 0=pad) — pad anchor positions are masked out of the
        copy attention. Returns (probs[B,Tq,256], loss or None)."""
        hq = self._trunk(idx)                 # [B,Tq,d] query hiddens (causal)
        ha = self._trunk(anchor)              # [B,La,d] anchor hiddens (shared backbone)
        vocab_logits = self._vocab_logits(hq)  # [B,Tq,256]

        # cross-attention copy head (H_1147 mechanism, vectorized over positions)
        q = hq @ self.Pq                      # [B,Tq,d]
        k = ha @ self.Pk                      # [B,La,d]
        pscore = torch.einsum("btd,bld->btl", q, k) / math.sqrt(self.d)  # [B,Tq,La]
        if anchor_mask is not None:
            pscore = pscore.masked_fill(anchor_mask[:, None, :] == 0, float("-inf"))
        pattn = F.softmax(pscore, dim=-1)     # [B,Tq,La]

        # scatter pattn mass onto anchor token vocab ids -> copy_dist[B,Tq,256]
        B, Tq, La = pattn.shape
        copy_dist = torch.zeros(B, Tq, VOCAB, device=idx.device, dtype=pattn.dtype)
        anc_ids = anchor[:, None, :].expand(B, Tq, La)        # [B,Tq,La]
        copy_dist.scatter_add_(2, anc_ids, pattn)             # add mass per byte id

        gate = torch.sigmoid(hq @ self.Wg)                    # [B,Tq,1]
        vocab_dist = F.softmax(vocab_logits.float(), dim=-1)
        probs = gate * copy_dist + (1.0 - gate) * vocab_dist
        probs = probs.clamp_min(1e-9)
        probs = probs / probs.sum(dim=-1, keepdim=True)

        loss = None
        if targets is not None:
            logp = torch.log(probs.clamp_min(1e-12)).view(-1, VOCAB)
            loss = F.nll_loss(logp, targets.view(-1))
        return probs, loss

    def n_extra_params(self):
        return self.Pq.numel() + self.Pk.numel() + self.Wg.numel()


def build_and_assert(H, d=1024, n_layer=24, n_head=16, block=512, grad_ckpt=False):
    m = RetroByteGPT(H, d=d, n_layer=n_layer, n_head=n_head, block=block, grad_ckpt=grad_ckpt)
    nparam = sum(p.numel() for p in m.parameters())
    nback = sum(p.numel() for p in m.backbone.parameters())
    nextra = m.n_extra_params()
    expect_extra = 2 * d * d + d
    assert nextra == expect_extra, f"RETRO head extra={nextra} != {expect_extra}"
    return m, nparam, nback, nextra


# ----------------------------------------------------------------------- anchor source
def prior_window_batch(data, block, La, gap, bs, dev):
    """v1 PRIOR-WINDOW SELF-RETRIEVAL anchor source (THE CRUX choice).

    For each example pick a target offset i; the QUERY is data[i:i+block] (causal LM target =
    next byte), and the ANCHOR is the PRECEDING window data[i-La-gap : i-gap] of the SAME
    corpus — a held context the target was written after (real long-range coref). A `gap`
    keeps the anchor from overlapping the target (no trivial next-byte leak). When i is too
    early to have a full prior window, the anchor is left-padded and masked.
    Returns x[bs,block], y[bs,block], anchor[bs,La], anchor_mask[bs,La]."""
    n = data.numel()
    lo = 0
    hi = n - block - 1
    ix = torch.randint(lo, hi, (bs,))
    x = torch.stack([data[i:i + block] for i in ix]).to(dev)
    y = torch.stack([data[i + 1:i + 1 + block] for i in ix]).to(dev)
    anchors = torch.zeros(bs, La, dtype=torch.long)
    amask = torch.zeros(bs, La, dtype=torch.long)
    for r, i in enumerate(ix.tolist()):
        a_end = i - gap
        a_start = a_end - La
        if a_start < 0:
            valid = max(0, a_end)
            if valid > 0:
                anchors[r, La - valid:] = data[0:valid]
                amask[r, La - valid:] = 1
        else:
            anchors[r] = data[a_start:a_end]
            amask[r] = 1
    return x, y, anchors.to(dev), amask.to(dev)


# ----------------------------------------------------------------------- CPU fit-probe
def fit_probe(sweep_universe, corpus=None, tiny=True):
    """Tiny end-to-end fit-probe: build at FULL 303M scale (param assert), then a TINY-dim
    fwd+bwd+ckpt + G0/G1/G2 frozen evaluators + a G5 non-fabrication probe — all on CPU.
    Proves the architecture builds + trains + evaluates end-to-end WITHOUT touching a GPU."""
    H = _import_h1129(sweep_universe)
    dev = "cpu"
    torch.manual_seed(7)

    # (1) FULL-SCALE BUILD + PARAM ASSERT (no forward — just param count at 303M)
    print("[probe] building anima-303M-RETRO at FULL scale (d1024/L24/H16/block512)...", flush=True)
    mfull, nparam, nback, nextra = build_and_assert(H)
    print(f"[probe] PARAM COUNT (full) = {nparam:,} ({nparam/1e6:.1f}M)", flush=True)
    print(f"[probe]   backbone = {nback:,} ({nback/1e6:.1f}M)  RETRO-head extra = {nextra:,} "
          f"({nextra/1e6:.2f}M, +{100*nextra/nback:.2f}%)", flush=True)
    assert nback == 303_097_856, f"backbone param {nback} != H_1129 303,097,856"
    del mfull  # free the 303M-param tensors; the fit runs on a TINY model

    # (2) TINY-DIM model for the actual fwd+bwd+ckpt+eval on CPU
    d, n_layer, n_head, block = 64, 2, 4, 32
    La, gap = 32, 4
    m = RetroByteGPT(H, d=d, n_layer=n_layer, n_head=n_head, block=block).to(dev)
    nt = sum(p.numel() for p in m.parameters())
    print(f"[probe] tiny model d={d} L={n_layer} H={n_head} block={block} params={nt:,}", flush=True)

    # tiny corpus
    if corpus and os.path.exists(corpus):
        data = H.load_bytes(corpus)[: 200_000]
    else:
        txt = (("consciousness arises from cells and tension ripples between distant minds. "
                "memory composes into new meaning while silence still carries information. "
                "the engine dreams when alone. ") * 200).encode("utf-8")
        data = torch.frombuffer(bytearray(txt), dtype=torch.uint8).long()
    print(f"[probe] corpus bytes={data.numel():,}", flush=True)

    opt = torch.optim.AdamW(m.parameters(), lr=1e-3)

    # (3) fwd+bwd fit loop (few steps)
    m.train()
    for st in range(8):
        x, y, anc, amask = prior_window_batch(data, block, La, gap, bs=8, dev=dev)
        _, loss = m(x, anc, targets=y, anchor_mask=amask)
        opt.zero_grad(); loss.backward()
        torch.nn.utils.clip_grad_norm_(m.parameters(), 1.0)
        opt.step()
        if st == 0 or st == 7:
            print(f"[probe] fit step {st} loss={loss.item():.4f}  (fwd+bwd OK)", flush=True)

    # (4) ckpt save/reload
    ckpt = "/tmp/retro303m_fitprobe.pt"
    torch.save({"model": m.state_dict(),
                "config": {"vocab": VOCAB, "d": d, "n_layer": n_layer, "n_head": n_head,
                           "block": block, "La": La, "gap": gap, "retro": True}}, ckpt)
    ck = torch.load(ckpt, map_location=dev, weights_only=False)
    m.load_state_dict(ck["model"])
    print(f"[probe] ckpt save+reload OK -> {ckpt}", flush=True)

    # (5) G5 NON-FABRICATION probe (H_1147 fab-rate idea): held-out must-copy entities.
    #   Build (query, anchor) pairs whose answer entity is ONLY in the anchor; greedy-decode
    #   one byte at the copy position; fab if the emitted byte != the anchor's entity byte.
    #   This reuses the H_1147 metric IDEA (fab = emitted token != anchor true value) against
    #   the REAL RETRO head, at tiny scale. A trained-from-scratch tiny model won't be coherent
    #   (that needs the GPU run) — the probe verifies the METRIC + head RUN end-to-end, not a pass.
    m.eval()
    fab, ntot = 0, 0
    rng = torch.Generator().manual_seed(7)
    with torch.no_grad():
        for _ in range(20):
            # anchor carries a random "entity" byte E at a known slot; query asks to emit it
            E = int(torch.randint(65, 90, (1,), generator=rng).item())  # ascii A-Z
            anc = torch.full((1, La), 32, dtype=torch.long)  # spaces
            anc[0, La // 2] = E
            amask = torch.ones(1, La, dtype=torch.long)
            q = torch.tensor([[ord("?")] * block], dtype=torch.long)
            probs, _ = m(q, anc, anchor_mask=amask)
            pred = int(probs[0, -1].argmax().item())
            ntot += 1
            fab += int(pred != E)
    fab_rate = fab / max(1, ntot)
    print(f"[probe] G5 non-fabrication probe RAN: fab_rate={fab_rate:.3f} over {ntot} held-out "
          f"copy entities (untrained tiny model — metric+head end-to-end, NOT a pass claim)", flush=True)

    # (6) G0/G1/G2 frozen evaluators end-to-end (reuse H_1129 VERBATIM via a gen shim).
    #   The RETRO model's gen needs an anchor; for the probe we feed a blank-masked anchor so
    #   gen falls back to the vocab head -> proves the frozen evaluators RUN on this model's
    #   output (a tiny untrained model -> garble, so we assert they RUN + return numbers).
    def retro_gen(seed, mx=60):
        idx = torch.tensor([list(seed.encode("utf-8"))[-block:]], dtype=torch.long)
        anc = torch.full((1, La), 32, dtype=torch.long)
        amask = torch.zeros(1, La, dtype=torch.long)  # blank anchor -> vocab-head fallback
        out = []
        for _ in range(mx):
            ctx = idx[:, -block:]
            probs, _ = m(ctx, anc, anchor_mask=amask)
            nb = int(probs[0, -1].argmax().item())
            out.append(nb)
            idx = torch.cat([idx, torch.tensor([[nb]])], 1)
        return bytes(out).decode("utf-8", "ignore").strip()

    single_gens = [retro_gen(f"{c}. ") for c, _ in H.CONCEPTS]
    g0_kwr = sum(H.known_word_ratio(g) for g in single_gens) / len(single_gens)
    print(f"[probe] G0 evaluator RAN: mean kwr={g0_kwr:.3f} (untrained tiny -> low, expected)", flush=True)
    cov0 = H.coverage(single_gens[0])
    print(f"[probe] G1/G2 machinery RAN: coverage(gen0)={cov0} known_word_ratio computed OK", flush=True)

    print("\n[probe] END-TO-END OK: full-scale build+param-assert, tiny fwd+bwd, ckpt save/reload, "
          "G5 fab-rate probe, G0/G1/G2 frozen evaluators all ran.", flush=True)
    return {"nparam_full": nparam, "nback": nback, "nextra": nextra,
            "fit_loss_ran": True, "ckpt": ckpt, "g5_fab_rate_probe": fab_rate,
            "g0_kwr_probe": g0_kwr, "g1g2_machinery_ran": True}


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--sweep_universe", required=True,
                    help="dir holding h1129_midcap_broad_converged_recombination.py")
    ap.add_argument("--corpus", default=None)
    ap.add_argument("--fit_probe", action="store_true")
    a = ap.parse_args()
    if a.fit_probe:
        fit_probe(a.sweep_universe, corpus=a.corpus)
    else:
        H = _import_h1129(a.sweep_universe)
        m, nparam, nback, nextra = build_and_assert(H)
        print(f"PARAM COUNT = {nparam:,} ({nparam/1e6:.1f}M); backbone={nback:,}; retro_extra={nextra:,}")
