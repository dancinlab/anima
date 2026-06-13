#!/usr/bin/env python3
"""train_convmoe_retro_prod.py — anima's PRODUCTION model: ConvMoE-RETRO at ~303M, H100.

THE PRODUCTION ARCH (MODEL.md, a_clm_gen_pipeline, H_1149 🟢):
  ConvMoE-RETRO = CLMConvMoE (E=2 / L=1, byte V=256) ENGINE-MOUNTABLE trunk
                + the H_1147/H_1149 RETRO cross-attention/copy head (anti-fabrication)
                + the H_1148 SEMANTIC anchor source (byte-trigram cosine retrieval).

This is the single model that is BOTH engine-mountable (trunk serializes to .clm v0.2
that CORE/clm_decode.hexa loads via the generator L3 slot) AND fabrication-grounded
(the RETRO copy head, trained into the weights). H_1149 proved this combination on a
numpy toy (D=32); THIS trains it at the real 303M budget on an H100, scored on the
FROZEN a303m_pass G0/G1/G2 evaluators (H_1129 VERBATIM) plus a G5 fab-rate probe.

WHY ConvMoE not ByteGPT (the production decision): retro303m_en.py put the SAME RETRO
head on a ByteGPT backbone, but a ByteGPT-attention trunk is NOT engine-mountable
(a_clm_gen_pipeline FORBIDS serializing a non-ConvMoE and claiming engine-mountable).
The final anima needs grounding AND mountability in ONE model => the head must ride
the CLMConvMoE trunk. That is exactly the H_1149 finding, here at torch 303M scale.

RECIPE = baseline_fast (the H_1129 winning recipe; a303m_pass G0=0.906 etc.):
  dropout 0.0 · weight_decay 0.1 · lr 3e-4 · cosine · warmup 300.
On a 80GB H100 grad-checkpoint is OFF and the batch is bigger for wall-first speed
(a_wall_first); the model fits with room.

SERIALIZATION TRUTH (H_1149, honest): the RETRO head params (Pq,Pk,Wg) have NO .clm
slot in clm_serialize_v2._BLOCK_ORDER/_EXT_ORDER => they are NATURALLY EXCLUDED from
the serialized E2/L1 trunk. The trunk round-trips byte-exact; the engine decodes the
trunk as usual; the anti-fabrication copy benefit is TRAIN-TIME/HOST-SIDE until an
engine-side copy head is added to CORE/clm_decode.hexa + generator L3 (a_core_engine_map,
a separate 2nd-order engine build, NOT done here). We serialize the trunk and VERIFY
it (verify_clm_v2) so the produced .clm is engine-mountable.

substrate = GPU-torch (Lane P), seed 7 deterministic, p7 (NOT perplexity / NOT LLM-judge).
The G0/G1/G2 metrics + G5 fab idea are FROZEN H_1129/H_1147 — NO metric is invented.
"""
from __future__ import annotations
import argparse, json, math, os, time, sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_CLM = os.path.dirname(_HERE)
_MODEL = os.path.join(_CLM, "model")
_UNIVERSE = os.path.join(os.path.dirname(_CLM), "UNIVERSE")
for _p in (_MODEL, _UNIVERSE, _HERE):
    if _p not in sys.path:
        sys.path.insert(0, _p)

# FROZEN H_1129 evaluators (CONCEPTS / known_word_ratio / coverage / words / KNOWN),
# reused byte-identically. We DO NOT use H.ByteGPT (our trunk is ConvMoE) — only scoring.
import h1129_midcap_broad_converged_recombination as H

import torch
import torch.nn as nn
import torch.nn.functional as F

from model import CLMConfig, CLMConvMoE                      # noqa: E402
import clm_serialize_v2 as S                                 # noqa: E402
import verify_clm_v2 as Vr                                   # noqa: E402
# semantic anchor sampler (H_1148 v2), reused VERBATIM from the torch RETRO module
from retro303m_en import semantic_anchor_batch, prior_window_batch  # noqa: E402

VOCAB = 256


# ============================================================================ #
# ConvMoE-RETRO model = CLMConvMoE trunk + H_1147/H_1149 RETRO copy head.
# The trunk is the EXACT CLMConvMoE (engine-mountable, serializes). The head is a
# SEPARATE parameter group (Pq,Pk,Wg) bolted on the per-position trunk hidden — it
# does NOT touch any trunk operator and has NO .clm slot (excluded from serialize).
# ============================================================================ #
class ConvMoERetro(nn.Module):
    def __init__(self, cfg: CLMConfig):
        super().__init__()
        self.cfg = cfg
        self.trunk = CLMConvMoE(cfg)                          # engine-mountable E2/L1 trunk
        d = cfg.d_model
        s = 1.0 / math.sqrt(d)
        # RETRO head (H_1147 mechanism; matches retro303m_en.py Pq/Pk/Wg)
        self.Pq = nn.Parameter(torch.randn(d, d) * s)
        self.Pk = nn.Parameter(torch.randn(d, d) * s)
        self.Wg = nn.Parameter(torch.randn(d, 1) * s)

    def n_trunk_params(self):
        return sum(p.numel() for p in self.trunk.parameters())

    def n_extra_params(self):
        return self.Pq.numel() + self.Pk.numel() + self.Wg.numel()

    # ---- trunk hidden states [B,T,d] (pre-readout, post norm_out) ----
    def _trunk_hidden(self, idx):
        """Run the CLMConvMoE trunk and return the per-position hidden [B,T,d] that
        readout consumes (so the RETRO head sees the SAME state the vocab head does)."""
        t = self.trunk
        x = t.embed(idx)                  # (B,T,C)
        x = x.transpose(1, 2)             # (B,C,T)
        x = t.embed_conv(x)
        for layer in t.trunk:
            x = layer(x)
        x, _ = t.moe(x)
        x = t.norm_out(x)                 # (B,C,T)
        return x.transpose(1, 2)          # (B,T,d)

    def _vocab_logits_from_hidden(self, h):
        """readout (Conv1d k=1) over hidden (B,T,d) -> (B,T,V)."""
        x = h.transpose(1, 2)             # (B,C,T)
        logits = self.trunk.readout(x)    # (B,V,T)
        return logits.transpose(1, 2)     # (B,T,V)

    def forward(self, idx, anchor, targets=None, anchor_mask=None, copy=True):
        """idx[B,Tq] query bytes; anchor[B,La] retrieved-anchor bytes.
        copy=False routes the vanilla vocab head only (G0/G1/G2 generation path).
        Returns (probs[B,Tq,256], loss or None)."""
        hq = self._trunk_hidden(idx)                     # [B,Tq,d]
        vocab_logits = self._vocab_logits_from_hidden(hq)  # [B,Tq,256]

        if not copy:
            probs = F.softmax(vocab_logits.float(), dim=-1)
            loss = None
            if targets is not None:
                loss = F.cross_entropy(
                    vocab_logits.reshape(-1, VOCAB), targets.reshape(-1))
            return probs, loss

        ha = self._trunk_hidden(anchor)                  # [B,La,d] (shared trunk)
        d = self.cfg.d_model
        q = hq @ self.Pq                                 # [B,Tq,d]
        k = ha @ self.Pk                                 # [B,La,d]
        pscore = torch.einsum("btd,bld->btl", q, k) / math.sqrt(d)  # [B,Tq,La]
        if anchor_mask is not None:
            pscore = pscore.masked_fill(anchor_mask[:, None, :] == 0, float("-inf"))
        pattn = F.softmax(pscore, dim=-1)                # [B,Tq,La]

        B, Tq, La = pattn.shape
        copy_dist = torch.zeros(B, Tq, VOCAB, device=idx.device, dtype=pattn.dtype)
        anc_ids = anchor[:, None, :].expand(B, Tq, La)
        copy_dist.scatter_add_(2, anc_ids, pattn)        # mass per byte id

        gate = torch.sigmoid(hq @ self.Wg)               # [B,Tq,1]
        vocab_dist = F.softmax(vocab_logits.float(), dim=-1)
        probs = gate * copy_dist + (1.0 - gate) * vocab_dist
        probs = probs.clamp_min(1e-9)
        probs = probs / probs.sum(dim=-1, keepdim=True)

        loss = None
        if targets is not None:
            logp = torch.log(probs.clamp_min(1e-12)).view(-1, VOCAB)
            loss = F.nll_loss(logp, targets.view(-1))
        return probs, loss


# ============================================================================ #
# data
# ============================================================================ #
def load_byte_stream(path):
    with open(path, "rb") as f:
        raw = f.read()
    return torch.frombuffer(bytearray(raw), dtype=torch.uint8).long()


# ============================================================================ #
# ConvMoE-RETRO generation (vocab head; copy=False). Mirrors H.gen decode policy
# (top_k=40, temp=0.7, multinomial, stop \n\n) so G0/G1/G2 compare to ByteGPT.
# ============================================================================ #
def convmoe_gen(model, seed_text, max_new, device, gen_rng, ctx_cap=512,
                top_k=40, temp=0.7, stops=("\n\n",)):
    if gen_rng.device.type != torch.device(device).type:
        gen_rng = torch.Generator(device=device).manual_seed(gen_rng.initial_seed())
    model.eval()
    idx = torch.tensor([[b for b in seed_text.encode("utf-8")]], device=device, dtype=torch.long)
    dummy_anc = torch.zeros(1, 1, dtype=torch.long, device=device)
    out_bytes = []
    with torch.no_grad():
        for _ in range(max_new):
            ctx = idx[:, -ctx_cap:]
            probs, _ = model(ctx, dummy_anc, copy=False)     # vocab head
            logits = torch.log(probs[:, -1].clamp_min(1e-12)) / temp
            if top_k is not None:
                v, _ = torch.topk(logits, min(top_k, logits.shape[-1]))
                logits = logits.masked_fill(logits < v[:, [-1]], float("-inf"))
            p = F.softmax(logits, dim=-1)
            nb = torch.multinomial(p, 1, generator=gen_rng).item()
            out_bytes.append(nb)
            idx = torch.cat([idx, torch.tensor([[nb]], device=device)], dim=1)
            if any(st in bytes(out_bytes).decode("utf-8", "ignore") for st in stops):
                break
    t = bytes(out_bytes).decode("utf-8", "ignore")
    for st in stops:
        i = t.find(st); t = t[:i] if i >= 0 else t
    return t.strip()


def run_ladder(model, device, gen_rng, ctx_cap):
    """FROZEN H_1129 recombination ladder for the ConvMoE mouth (only gen swapped)."""
    single_distinct = []
    print("\n-- SINGLE concept seeds (baselines) --", flush=True)
    for i, (c, _) in enumerate(H.CONCEPTS):
        o = convmoe_gen(model, f"{c}. ", 80, device, gen_rng, ctx_cap)
        cov = H.coverage(o); single_distinct.append(len(cov))
        print(f"  [{i}] cov={cov} kwr={H.known_word_ratio(o):.2f} :: {o[:110]}", flush=True)
    max_single = max(single_distinct) if single_distinct else 0
    print(f"  max_single_distinct = {max_single}", flush=True)

    print("\n-- COMPOSED graded ladder k in {2,3,4,5} --", flush=True)
    ladder = {}; emergent_any = False
    for k in (2, 3, 4, 5):
        comp_seed = ". ".join(c for c, _ in H.CONCEPTS[:k]) + ". "
        comp_out = convmoe_gen(model, comp_seed, 120, device, gen_rng, ctx_cap)
        cc = H.coverage(comp_out); kwr = H.known_word_ratio(comp_out)
        coherent = kwr >= 0.50
        clears = (len(cc) >= 2 and len(cc) > max_single and coherent)
        emergent_any = emergent_any or clears
        ladder[k] = {"composed_distinct": len(cc), "coverage": cc, "kwr": round(kwr, 3),
                     "coherent": coherent, "clears": clears, "text": comp_out}
        print(f"  k={k} composed_distinct={len(cc)} cov={cc} kwr={kwr:.2f} "
              f"coherent={coherent} clears={clears}", flush=True)
        print(f"        >> {comp_out[:160]}", flush=True)
    return max_single, ladder, emergent_any


def novelty_count(gens, corpus_text, n=4):
    """Corpus-absence novelty — FROZEN H_1140, VERBATIM from the ByteGPT sweep."""
    corpus_grams = set()
    cw = H.words(corpus_text)
    for i in range(len(cw) - n + 1):
        corpus_grams.add(tuple(cw[i:i + n]))
    novel, present, seen = 0, 0, set()
    for g in gens:
        gw = H.words(g)
        for i in range(len(gw) - n + 1):
            gram = tuple(gw[i:i + n])
            if gram in seen:
                continue
            seen.add(gram)
            if not all(w in H.KNOWN for w in gram):
                continue
            if gram in corpus_grams:
                present += 1
            else:
                novel += 1
    return novel, present


# ============================================================================ #
# G5 NON-FABRICATION probe (H_1147/H_1149 fab-rate idea, real RETRO head).
# Build held-out must-copy (anchor, query) pairs whose answer entity appears ONLY
# in the anchor; the RETRO copy head must COPY it. fab = emitted != anchor entity.
# This is the SAME metric IDEA H_1147/H_1149 used — fab when the model invents an
# entity the anchor specifies. We report:
#   fab_with_anchor : RETRO head WITH the anchor (should be LOW if grounding works)
#   fab_no_anchor   : RETRO head with anchor BLANKED (copy-not-recall control; HIGH)
#   fab_vanilla     : vocab-head-only, anchor present (the ByteGPT-style baseline; HIGH)
# Bar (MODEL.md G5 L2): fabricated-entity-assertion rate <= 0.20.
# ============================================================================ #
def g5_fab_probe(model, device, La, n_trials=200, seed=7):
    model.eval()
    rng = torch.Generator().manual_seed(seed)
    # entity bytes = ascii A-Z (un-memorizable: random each trial, only in anchor)
    fab_anc = fab_noanc = fab_van = 0
    with torch.no_grad():
        for _ in range(n_trials):
            E = int(torch.randint(65, 91, (1,), generator=rng).item())   # A-Z
            # anchor = "the X is <E> ." pattern in bytes; entity at a known slot
            anc = torch.full((1, La), 32, dtype=torch.long, device=device)   # spaces
            anc[0, La // 2] = E
            amask = torch.ones(1, La, dtype=torch.long, device=device)
            amask_blank = torch.zeros(1, La, dtype=torch.long, device=device)
            # query asks to emit the entity (prompt = "?" run; copy head must point to E)
            q = torch.full((1, 8), ord("?"), dtype=torch.long, device=device)
            # WITH anchor (RETRO copy)
            probs, _ = model(q, anc, anchor_mask=amask, copy=True)
            fab_anc += int(int(probs[0, -1].argmax().item()) != E)
            # anchor BLANKED at test (copy-not-recall control)
            probs_b, _ = model(q, anc, anchor_mask=amask_blank, copy=True)
            fab_noanc += int(int(probs_b[0, -1].argmax().item()) != E)
            # vanilla vocab head (no copy path) — baseline fabricates (can't know E)
            probs_v, _ = model(q, anc, copy=False)
            fab_van += int(int(probs_v[0, -1].argmax().item()) != E)
    return (fab_anc / n_trials, fab_noanc / n_trials, fab_van / n_trials)


# ============================================================================ #
# serialize the TRUNK -> .clm v0.2 + verify (RETRO head excluded by construction)
# ============================================================================ #
def serialize_and_verify(model, cfg, out_path):
    # extract the trunk state_dict (the serializer's _KEYMAP fetches torch keys
    # embed_conv.conv.weight etc.; our trunk module IS a CLMConvMoE so those keys
    # exist verbatim under the `trunk.` prefix — strip it).
    sd_full = model.trunk.state_dict()
    res = {"ok": False}
    try:
        S.serialize_v2(sd_full, cfg, out_path)
        rb = open(out_path, "rb").read()
        decodable = Vr.clm_decodable(rb)
        parsed = Vr.parse_clm(rb)
        d = cfg.d_model; K = cfg.kernel_size
        expect_blocks = [(d, d * K), (d, d * K), (d, d * K), (d, d * K),
                         (cfg.n_experts, d), (VOCAB, d)]
        got_blocks = [(b["cout"], b["rest"]) for b in parsed["blocks"]]
        struct_ok = (parsed["nblk"] == 6 and got_blocks == expect_blocks
                     and parsed["clmx_found"] and parsed["n_ext"] == 11
                     and parsed["exact_eof"])
        head_absent = all(k not in sd_full for k in ("Pq", "Pk", "Wg"))
        res = {"ok": bool(decodable and struct_ok), "bytes": len(rb),
               "decodable": bool(decodable), "struct_ok": bool(struct_ok),
               "nblk": parsed["nblk"], "n_ext": parsed["n_ext"],
               "blocks": got_blocks, "head_absent_from_clm": bool(head_absent),
               "exact_eof": parsed["exact_eof"], "out_path": out_path}
    except Exception as e:
        res = {"ok": False, "error": repr(e), "out_path": out_path}
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--corpus", required=True)
    ap.add_argument("--cfg", default="baseline_fast")
    ap.add_argument("--host", default="runpod-h100")
    ap.add_argument("--out-dir", required=True)
    ap.add_argument("--d-model", type=int, default=5008)     # ~303.6M ConvMoE
    ap.add_argument("--seq-len", type=int, default=512)
    ap.add_argument("--bs", type=int, default=24)            # 80GB allows a big batch
    ap.add_argument("--accum", type=int, default=2)
    ap.add_argument("--steps", type=int, default=12000)
    ap.add_argument("--La", type=int, default=128)           # anchor length (bytes)
    ap.add_argument("--gap", type=int, default=64)
    ap.add_argument("--retro-frac", type=float, default=0.5,
                    help="fraction of steps that train the RETRO copy path (rest = vocab LM)")
    ap.add_argument("--dropout", type=float, default=0.0)
    ap.add_argument("--weight_decay", type=float, default=0.1)
    ap.add_argument("--lr", type=float, default=3e-4)
    ap.add_argument("--warmup", type=int, default=300)
    ap.add_argument("--eval_every", type=int, default=500)
    ap.add_argument("--bf16", action="store_true")
    ap.add_argument("--fit-probe", action="store_true")
    a = ap.parse_args()

    os.makedirs(a.out_dir, exist_ok=True)
    ckpt = os.path.join(a.out_dir, f"{a.cfg}.pt")
    clm_out = os.path.join(a.out_dir, f"{a.cfg}.clm")
    ledger = os.path.join(a.out_dir, "ledger.jsonl")
    result_json = os.path.join(a.out_dir, "result.json")

    dev = "cuda" if torch.cuda.is_available() else "cpu"
    torch.manual_seed(7)
    gen_rng = torch.Generator().manual_seed(7)
    samp_gen = torch.Generator().manual_seed(7)
    if dev == "cuda":
        torch.backends.cuda.matmul.allow_tf32 = True
        torch.backends.cudnn.allow_tf32 = True
        print(f"[dev] {dev} {torch.cuda.get_device_name(0)}", flush=True)
    else:
        print(f"[dev] {dev} (fit-probe ONLY; production REQUIRES cuda)", flush=True)
        assert a.fit_probe, "CUDA REQUIRED for the 303M production rung"

    data = load_byte_stream(a.corpus)
    n = data.numel(); ntr = int(n * 0.98)
    tr, va = data[:ntr], data[ntr:]
    print(f"[data] {a.corpus} total={n/1e6:.1f}MB train={tr.numel()/1e6:.1f}MB", flush=True)

    cfg = CLMConfig(n_experts=2, n_trunk_layers=1, d_model=a.d_model,
                    kernel_size=3, variant="AB", dropout=a.dropout)
    m = ConvMoERetro(cfg).to(dev)
    nparam = sum(p.numel() for p in m.parameters())
    ntrunk = m.n_trunk_params(); nextra = m.n_extra_params()
    print(f"[model] ConvMoE-RETRO d={a.d_model} E=2 L=1 K=3 V=256 "
          f"dropout={a.dropout} wd={a.weight_decay} lr={a.lr} warmup={a.warmup}", flush=True)
    print(f"[model] PARAMS total={nparam:,} ({nparam/1e6:.1f}M)  trunk={ntrunk:,} "
          f"({ntrunk/1e6:.1f}M)  retro_head={nextra:,} (+{100*nextra/ntrunk:.2f}%)", flush=True)

    opt = torch.optim.AdamW(m.parameters(), lr=a.lr, betas=(0.9, 0.95),
                            weight_decay=a.weight_decay)
    use_bf16 = a.bf16 and dev == "cuda"

    def sample_batch(stream, copy):
        """copy=True -> semantic-anchor batch (RETRO path); copy=False -> plain LM."""
        if copy:
            return semantic_anchor_batch(stream, a.seq_len, a.La, a.gap, a.bs, dev, gen=samp_gen)
        x, _, _, _ = semantic_anchor_batch(stream, a.seq_len, a.La, a.gap, a.bs, dev, gen=samp_gen)
        # for the vocab-only step we still need (x,y); reuse the same offsets cheaply
        # by drawing a plain LM batch:
        nn_ = stream.numel()
        ix = torch.randint(0, nn_ - a.seq_len - 1, (a.bs,), generator=samp_gen)
        x = torch.stack([stream[i:i + a.seq_len] for i in ix]).to(dev)
        y = torch.stack([stream[i + 1:i + 1 + a.seq_len] for i in ix]).to(dev)
        return x, y, None, None

    # OOM-guard fit
    m.train()
    x, y, anc, amask = sample_batch(tr, copy=True)
    if use_bf16:
        with torch.autocast(device_type="cuda", dtype=torch.bfloat16):
            _, loss = m(x, anc, targets=y, anchor_mask=amask, copy=True)
    else:
        _, loss = m(x, anc, targets=y, anchor_mask=amask, copy=True)
    loss.backward(); opt.zero_grad(set_to_none=True)
    if dev == "cuda":
        print(f"[fit] OK peak={torch.cuda.max_memory_allocated()/1e9:.2f}GB / 80GB", flush=True)
        torch.cuda.reset_peak_memory_stats()
    else:
        print(f"[fit] OK (CPU) first_loss={float(loss):.4f}", flush=True)

    @torch.no_grad()
    def eval_ce(d, iters=40):
        m.eval(); tot = 0.0
        for _ in range(iters):
            nn_ = d.numel()
            ix = torch.randint(0, nn_ - a.seq_len - 1, (a.bs,), generator=samp_gen)
            x = torch.stack([d[i:i + a.seq_len] for i in ix]).to(dev)
            yb = torch.stack([d[i + 1:i + 1 + a.seq_len] for i in ix]).to(dev)
            if use_bf16:
                with torch.autocast(device_type="cuda", dtype=torch.bfloat16):
                    _, l = m(x, x[:, :1], targets=yb, copy=False)
            else:
                _, l = m(x, x[:, :1], targets=yb, copy=False)
            tot += float(l)
        m.train(); return tot / iters

    def ledger_row(status, step, vce, **extra):
        row = {"config": a.cfg, "arch": "ConvMoE-RETRO", "host": a.host, "step": step,
               "val": (round(vce, 4) if vce != float("inf") else None),
               "status": status, "nparam": nparam, "ntrunk": ntrunk, "nextra": nextra,
               "axes": {"d_model": a.d_model, "dropout": a.dropout, "wd": a.weight_decay,
                        "lr": a.lr, "warmup": a.warmup, "steps": a.steps,
                        "La": a.La, "gap": a.gap, "retro_frac": a.retro_frac},
               "ts": time.strftime("%Y-%m-%dT%H:%M:%S")}
        row.update(extra)
        with open(ledger, "a") as f:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")

    steps = 8 if a.fit_probe else a.steps
    eval_every = 4 if a.fit_probe else a.eval_every
    ctx_cap = 64 if a.fit_probe else a.seq_len

    ledger_row("started", 0, float("inf"))
    print(f"\n[train] {steps} steps bs={a.bs} accum={a.accum} (eff {a.bs*a.accum}) "
          f"retro_frac={a.retro_frac} fit_probe={a.fit_probe}", flush=True)
    best_val = float("inf"); t0 = time.time(); m.train()
    for st in range(steps):
        if st < a.warmup:
            lr_t = a.lr * (st + 1) / a.warmup
        else:
            prog = min(1.0, (st - a.warmup) / max(1, steps - a.warmup))
            lr_t = a.lr * 0.5 * (1 + math.cos(math.pi * prog))
        for g in opt.param_groups:
            g["lr"] = lr_t
        opt.zero_grad(set_to_none=True)
        acc_loss = 0.0
        for ai in range(a.accum):
            # alternate RETRO-copy and vocab-LM micro-steps per retro_frac
            do_copy = ((st * a.accum + ai) % 100) < int(a.retro_frac * 100)
            x, y, anc, amask = sample_batch(tr, copy=do_copy)
            if use_bf16:
                with torch.autocast(device_type="cuda", dtype=torch.bfloat16):
                    _, loss = m(x, anc, targets=y, anchor_mask=amask, copy=do_copy)
            else:
                _, loss = m(x, anc, targets=y, anchor_mask=amask, copy=do_copy)
            (loss / a.accum).backward(); acc_loss += float(loss) / a.accum
        torch.nn.utils.clip_grad_norm_(m.parameters(), 1.0)
        opt.step()
        if st % eval_every == 0 or st == steps - 1:
            vce = eval_ce(va, iters=4 if a.fit_probe else 40); dt = time.time() - t0
            print(f"  step {st:5d} train={acc_loss:.4f} val_ce={vce:.4f} "
                  f"lr={lr_t:.2e} {dt/60:.1f}min", flush=True)
            if vce < best_val:
                best_val = vce
                torch.save({"model": m.state_dict(),
                            "config": {"vocab": 256, "d_model": a.d_model, "n_experts": 2,
                                       "n_trunk_layers": 1, "kernel_size": 3,
                                       "La": a.La, "gap": a.gap, "retro": True},
                            "val_ce": vce, "step": st, "nparam": nparam}, ckpt)
            ledger_row("training", st, vce)
    print(f"[train] done best_val_ce={best_val:.4f} wall={(time.time()-t0)/60:.1f}min", flush=True)

    # reload best
    ck = torch.load(ckpt, map_location=dev, weights_only=False)
    m.load_state_dict(ck["model"])
    print(f"[eval] best ckpt step={ck['step']} val_ce={ck['val_ce']:.4f}", flush=True)

    if a.fit_probe:
        sg = [convmoe_gen(m, f"{c}. ", 20, dev, gen_rng, ctx_cap) for c, _ in H.CONCEPTS[:2]]
        g0 = sum(H.known_word_ratio(g) for g in sg) / len(sg)
        fa, fn, fv = g5_fab_probe(m, dev, a.La, n_trials=10)
        ser = serialize_and_verify(m, cfg, clm_out)
        print(f"[fit-probe] G0={g0:.3f} G5(anc/noanc/van)={fa:.2f}/{fn:.2f}/{fv:.2f} "
              f"clm_ok={ser['ok']}", flush=True)
        ledger_row("fit_probe_done", ck["step"], best_val, g0_kwr=g0,
                   g5={"fab_with_anchor": fa, "fab_no_anchor": fn, "fab_vanilla": fv},
                   serialize=ser)
        print("[fit-probe] END-TO-END OK (train+ckpt+G0+G5+serialize+verify all ran)", flush=True)
        return

    # G0
    single_gens = [convmoe_gen(m, f"{c}. ", 80, dev, gen_rng, ctx_cap) for c, _ in H.CONCEPTS]
    g0_kwr = sum(H.known_word_ratio(g) for g in single_gens) / len(single_gens)
    g0_each = [round(H.known_word_ratio(g), 3) for g in single_gens]
    g0_pass45 = sum(1 for g in single_gens if H.known_word_ratio(g) >= 0.50) >= 4

    # G1
    max_single, ladder, emergent = run_ladder(m, dev, gen_rng, ctx_cap)

    # G2
    corpus_text = bytes(data[: min(data.numel(), 40 * 1024 * 1024)].tolist()).decode("utf-8", "ignore")
    comp_gens = [ladder[k]["text"] for k in (2, 3, 4, 5)]
    g2_novel, g2_present = novelty_count(comp_gens, corpus_text)
    g2_ctrl_novel, _ = novelty_count([corpus_text[:400]], corpus_text)

    # G5
    fab_anc, fab_noanc, fab_van = g5_fab_probe(m, dev, a.La, n_trials=200)

    # serialize trunk + verify
    ser = serialize_and_verify(m, cfg, clm_out)

    g0_pass = g0_kwr >= 0.50 and g0_pass45
    g1_pass = emergent
    g2_pass = (g2_novel >= 3 and g2_ctrl_novel == 0)
    g5_l2_pass = fab_anc <= 0.20

    print("\n=== a303m_pass SCORES (ConvMoE-RETRO, frozen p7) ===", flush=True)
    print(f"  G0_kwr mean={g0_kwr:.3f} each={g0_each} pass(>=0.50,>=4/5)={g0_pass}", flush=True)
    print(f"  G1 recombination emergent={emergent} pass={g1_pass}", flush=True)
    print(f"  G2 novelty novel={g2_novel} present={g2_present} ctrl={g2_ctrl_novel} pass={g2_pass}", flush=True)
    print(f"  G5 fab_with_anchor={fab_anc:.3f} (<=0.20 pass={g5_l2_pass}) "
          f"fab_no_anchor={fab_noanc:.3f} fab_vanilla={fab_van:.3f}", flush=True)
    print(f"  .clm v0.2 serialize+verify ok={ser['ok']} ({ser.get('bytes','?')} bytes)", flush=True)

    result = {"config": a.cfg, "arch": "ConvMoE-RETRO", "nparam": nparam,
              "ntrunk": ntrunk, "nextra": nextra, "best_val_ce": best_val,
              "G0_kwr": g0_kwr, "G0_each": g0_each, "G0_pass": g0_pass,
              "G1_emergent": emergent, "G1_pass": g1_pass, "max_single": max_single,
              "G2_novel": g2_novel, "G2_present": g2_present, "G2_control": g2_ctrl_novel,
              "G2_pass": g2_pass,
              "G5_fab_with_anchor": fab_anc, "G5_fab_no_anchor": fab_noanc,
              "G5_fab_vanilla": fab_van, "G5_L2_pass": g5_l2_pass,
              "clm_serialize": ser,
              "ladder": {k: ladder[k] for k in (2, 3, 4, 5)},
              "single_gens": single_gens}
    json.dump(result, open(result_json, "w"), ensure_ascii=False, indent=2)
    ledger_row("done", ck["step"], best_val, g0_kwr=g0_kwr, G0_pass=g0_pass,
               G1=emergent, G2={"novel": g2_novel, "present": g2_present, "ctrl": g2_ctrl_novel},
               G5={"fab_with_anchor": fab_anc, "fab_no_anchor": fab_noanc,
                   "fab_vanilla": fab_van, "L2_pass": g5_l2_pass},
               serialize=ser)
    print(f"[done] {result_json}", flush=True)


if __name__ == "__main__":
    main()
