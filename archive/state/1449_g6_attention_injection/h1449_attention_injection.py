#!/usr/bin/env python3
"""H_1449 — ATTENTION-injection ROOT-FIX for the G6 IDEATION FALS-depth wall.

ANGLE (root-cause, H_1431 diagnostic): the 303M mouth per draw emits comparator 20%
· measurable 27% · BOTH 0% (within-draw mutually exclusive) = an ATTENTION/binding
deficit at the emission head. H_1435/1436/1437 all hit WALL=CAPACITY: form is learned
but cross-shuffle never collapses (comparator-leg and measurable-leg stay interchangeable
shells). H_1362 crossed the bar with an L24 attention stack.

This variant INJECTS a dedicated cross-binding self-attention block ("BindAttn") AFTER
the L24 trunk (before ln_f), freshly initialized, whose explicit job is to let the
comparator-bearing positions and the measurable-bearing positions attend to each other
within ONE forward pass so the mouth can co-emit a BOUND claim. We then re-measure the
FROZEN 5-bar (g6_common, h1305 detector VERBATIM). DECISIVE = B3 cross-shuffle COLLAPSE.

ISOLATION (c4 ABLATE): the SAME trained ckpt is re-evaluated with the BindAttn block
forced to an IDENTITY passthrough (its attention output zeroed -> pure residual). If the
FALS lift survives that, the lift came from the extra full-weight training, NOT from the
injected attention binding => not a real root-fix. If FALS COLLAPSES under ablation, the
lift IS the injected attention.

anti-tune-to-green (inherited from g6_common): corpus subjects DISJOINT from gauge CONCEPT
keywords / eval seeds / held-out seeds; shuffle-corpus control trains on byte-shuffled
corpus; detector + 5 bars FROZEN before any weight touched (c9, p7).
"""
import os, sys, json, random, time, argparse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import g6_common as C
import torch
import torch.nn as nn

OUT = os.environ.get("G6_OUT", "/workspace/g6/out")

# reuse H_1435 falsifiable-claim corpus generator (same distribution, eval-disjoint)
import h1435_continued_pretrain as base1435
gen_corpus = base1435.gen_corpus
shuffle_bytes = base1435.shuffle_bytes
make_batches = base1435.make_batches


# ── injected cross-binding attention block ──────────────────────────────────
class BindAttn(nn.Module):
    """A single self-attention + MLP block (same shape as a ByteGPT trunk Block)
    inserted AFTER the L24 trunk. Initialized FRESH. `ablate=True` forces the block
    to an identity passthrough (attention + mlp contributions zeroed) so c4 can test
    whether the lift is the injected attention binding or just extra training."""
    def __init__(s, d, h, p=0.0):
        super().__init__()
        s.ln1 = nn.LayerNorm(d)
        s.attn = nn.MultiheadAttention(d, h, dropout=p, batch_first=True)
        s.ln2 = nn.LayerNorm(d)
        s.mlp = nn.Sequential(nn.Linear(d, 4 * d), nn.GELU(), nn.Linear(4 * d, d), nn.Dropout(p))
        s.ablate = False

    def forward(s, x, mask):
        if s.ablate:
            return x  # identity passthrough — attention binding OFF
        hh = s.ln1(x)
        a, _ = s.attn(hh, hh, hh, attn_mask=mask, need_weights=False)
        x = x + a
        return x + s.mlp(s.ln2(x))


class BindByteGPT(nn.Module):
    """Wraps the base ByteGPT trunk and appends ONE BindAttn block before ln_f."""
    def __init__(s, base, d, n_head, block):
        super().__init__()
        s.base = base                       # the loaded L24 ByteGPT
        s.bind = BindAttn(d, n_head)
        s.block = block

    def forward(s, idx, targets=None):
        b = s.base
        B, T = idx.shape
        pos = torch.arange(T, device=idx.device)
        x = b.drop(b.tok(idx) + b.pos(pos)[None, :, :])
        mask = torch.triu(torch.full((T, T), float("-inf"), device=idx.device), diagonal=1)
        for blk in b.blocks:
            x = blk(x, mask)
        x = s.bind(x, mask)                 # <-- injected cross-binding attention
        logits = b.head(b.ln_f(x))
        loss = None
        if targets is not None:
            loss = torch.nn.functional.cross_entropy(
                logits.view(-1, 256), targets.view(-1))
        return logits, loss


def build_bind_model(device):
    """Load base L24 ByteGPT, wrap with the injected BindAttn block."""
    base, cfg = C.load_model(C.CKPT_BASE, device)
    m = BindByteGPT(base, cfg["d"], cfg["n_head"], cfg["block"]).to(device)
    return m, cfg


def train(m, cfg, corpus_text, steps, device, lr=3e-5, bs=16):
    m.train()
    opt = torch.optim.AdamW(m.parameters(), lr=lr, betas=(0.9, 0.95), weight_decay=0.1)
    gen = make_batches(corpus_text, cfg["block"], bs, device)
    t0 = time.time()
    for st in range(steps):
        x, y = next(gen)
        _, loss = m(x, y)
        opt.zero_grad(set_to_none=True)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(m.parameters(), 1.0)
        opt.step()
        if st % 50 == 0 or st == steps - 1:
            print(f"    [H1449 step {st:4d}] ce={loss.item():.4f} {(time.time()-t0)/60:.1f}min",
                  flush=True)
    return m


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--device", default="cuda:0")
    ap.add_argument("--steps", type=int, default=400)
    ap.add_argument("--lines", type=int, default=4000)
    ap.add_argument("--seed", type=int, default=7)
    args = ap.parse_args()
    dev = args.device
    torch.manual_seed(args.seed)

    print(f"[H_1449] device={dev} steps={args.steps} seed={args.seed}", flush=True)

    # BASE eval = the un-injected L24 ByteGPT (the H_1410 deep-conv-equivalent baseline)
    base_m, cfg = C.load_model(C.CKPT_BASE, dev)
    base_eval = C.evaluate(base_m, cfg, "base", list(C.g.IDEATION_SEEDS))
    print(f"[H_1449] base FALS_in={base_eval['FALS_in']} DIST_in={base_eval['DIST_in']} "
          f"FALS_ho={base_eval['FALS_ho']}", flush=True)
    del base_m
    torch.cuda.empty_cache()

    corpus = gen_corpus(args.lines, seed=1449)

    # ── REAL attention-injection train ──
    m, _ = build_bind_model(dev)
    m = train(m, cfg, corpus, args.steps, dev)
    out_pt = os.path.join(OUT, f"h1449_attention_injection_seed{args.seed}.pt")
    os.makedirs(OUT, exist_ok=True)
    torch.save({"base_state": m.base.state_dict(),
                "bind_state": m.bind.state_dict(),
                "config": {"vocab": 256, "d": cfg["d"], "n_layer": cfg["n_layer"],
                           "n_head": cfg["n_head"], "block": cfg["block"]},
                "meta": {"variant": "H_1449", "steps": args.steps, "seed": args.seed,
                         "injected": "BindAttn-1block"}}, out_pt)

    # trained eval (BindAttn ON)
    m.bind.ablate = False
    trained_eval = C.evaluate(m, cfg, "trained", list(C.g.IDEATION_SEEDS))

    # ── c4 ABLATE: SAME ckpt, BindAttn forced to identity passthrough ──
    m.bind.ablate = True
    ablate_eval = C.evaluate(m, cfg, "ablate_bindattn", list(C.g.IDEATION_SEEDS))
    m.bind.ablate = False
    del m
    torch.cuda.empty_cache()

    # ── SHUFFLE-CORPUS control (same bytes, structure destroyed) ──
    shuf_corpus = shuffle_bytes(corpus, seed=1449)
    ms, _ = build_bind_model(dev)
    ms = train(ms, cfg, shuf_corpus, args.steps, dev)
    shuf_eval = C.evaluate(ms, cfg, "shuffle_corpus", list(C.g.IDEATION_SEEDS))
    del ms
    torch.cuda.empty_cache()

    bars = C.print_bars("H_1449 attention-injection", base_eval, trained_eval, shuf_eval)

    # c4 ABLATE bar (BindAttn-specific isolation, printed separately, FROZEN)
    b_ablate_collapse = ablate_eval["FALS_in"] < trained_eval["FALS_in"]
    print("\n  ---- c4 ABLATE BAR (attention isolation) ----", flush=True)
    print(f"  ABLATE   FALS_in={ablate_eval['FALS_in']} FALS_shuf={ablate_eval['FALS_shuf']} "
          f"FALS_ho={ablate_eval['FALS_ho']}", flush=True)
    print(f"  c4 ABLATE COLLAPSE  ablate.FALS_in<trained.FALS_in : "
          f"{ablate_eval['FALS_in']}<{trained_eval['FALS_in']} -> {b_ablate_collapse}", flush=True)

    bars["c4_ablate_collapse"] = bool(b_ablate_collapse)
    # GREEN requires the g6_common 5-bar GREEN AND the c4 ablate collapse
    bars["green_h1449"] = bool(bars["green"] and b_ablate_collapse)
    if bars["green_h1449"]:
        bars["tier_h1449"] = ("🟢 ROOT-FIX — injected attention crosses G6 FALS binding; "
                              "cross-shuffle COLLAPSES, held-out holds, control inert, "
                              "AND ablating the BindAttn block collapses the lift => "
                              "attention was the missing primitive")
    else:
        bars["tier_h1449"] = ("🧱 WALL — attention-injection did NOT root-fix the G6 FALS "
                              "binding (see failing bars / c4)")
    print(f"\n  H_1449 VERDICT: {bars['tier_h1449']}", flush=True)

    out = {"variant": "H_1449", "ckpt_base": C.CKPT_BASE, "ckpt_out": out_pt,
           "seed": args.seed,
           "base": base_eval, "trained": trained_eval,
           "ablate_bindattn": ablate_eval, "shuffle_corpus": shuf_eval, "bars": bars}
    json.dump(out, open(os.path.join(OUT, f"h1449_result_seed{args.seed}.json"), "w"),
              ensure_ascii=False, indent=2)
    print(f"[H_1449 done] {OUT}/h1449_result_seed{args.seed}.json", flush=True)


if __name__ == "__main__":
    main()
