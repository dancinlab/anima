#!/usr/bin/env python3
"""H_1441 — CONTRASTIVE falsifiable-vs-nonfalsifiable minimal-pair training.

Targets the H_1435/36/37 공통 실패 ("form installed but cross-shuffle does NOT collapse" =
learned a shuffle-INVARIANT surface form). The contrastive objective forces shuffle-SENSITIVITY:
the model must assign a HIGHER sequence-likelihood to a FULL falsifiable claim (comparator AND
measurable present) than to its MINIMAL PAIR with one leg blanked (→ non-falsifiable).

  loss = CE(falsifiable corpus, H_1435 VERBATIM) + λ · margin(logP(pos) − logP(neg))

NOT detector-supervised (a_train_inline_gauge, p7): the contrastive label is STRUCTURAL
(leg-present vs leg-removed), NOT the h1305 detector score. The detector is eval-ONLY VERBATIM.
torch C.evaluate is SKIPPED here (it would be DIRECTIONAL) — the verdict is measured ENGINE-NATIVE
afterwards: pt_to_engine_bin.py → CORE/bytegpt_decode → frozen 5-bar (a_engine_native_learning).
ckpt MUST be pulled before teardown (a_fire_recover_complete — 1435/36/37 lost theirs).
"""
import os, sys, json, random, time, argparse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import g6_common as C
import torch
import h1435_continued_pretrain as base

gen_corpus = base.gen_corpus
make_batches = base.make_batches
shuffle_bytes = base.shuffle_bytes

OUT = os.environ.get("G6_OUT", "/workspace/g6/out")
COMPS = sorted(C.COMPARATOR)
MEAS = sorted(C.MEASURABLE)
SUBJ = base.TRAIN_SUBJECTS

# FROZEN minimal-pair templates — the SAME 5 as h1435.gen_corpus; neg = one leg blanked.
PAIR_TEMPLATES = [
    "if {s} grows, the {m} {c} than before.",
    "{s} {c} a higher {m} when the input rises.",
    "the {m} of {s} is greater whenever {s2} {c}.",
    "{s} shows a lower {m} than {s2} under load.",
    "when {s} {c}, its {m} decreases by a fixed amount.",
]

def gen_pairs(n, seed):
    rng = random.Random(seed)
    pos, neg = [], []
    for _ in range(n):
        t = rng.choice(PAIR_TEMPLATES)
        s, s2 = rng.choice(SUBJ), rng.choice(SUBJ)
        c, m = rng.choice(COMPS), rng.choice(MEAS)
        pos.append(t.format(s=s, s2=s2, c=c, m=m))
        if rng.random() < 0.5:
            neg.append(t.format(s=s, s2=s2, c="", m=m).replace("  ", " "))   # comparator removed
        else:
            neg.append(t.format(s=s, s2=s2, c=c, m="").replace("  ", " "))   # measurable removed
    return pos, neg

def _seq_loglik(m, text, block, device):
    ids = list(text.encode("utf-8"))[: block + 1]
    if len(ids) < 2:
        return torch.tensor(0.0, device=device)
    x = torch.tensor(ids[:-1], device=device)[None]
    y = torch.tensor(ids[1:], device=device)[None]
    _, ce = m(x, y)
    return -ce   # higher = more likely

def contrastive_loss(m, pos, neg, block, device, margin=0.5):
    terms = [torch.clamp(margin - (_seq_loglik(m, p, block, device) - _seq_loglik(m, n, block, device)), min=0.0)
             for p, n in zip(pos, neg)]
    return torch.stack(terms).mean()

def train(m, cfg, corpus_text, steps, device, lr=3e-5, bs=16, lam=0.5, pairs_per=8):
    m.train()
    opt = torch.optim.AdamW(m.parameters(), lr=lr, betas=(0.9, 0.95), weight_decay=0.1)
    gen = make_batches(corpus_text, cfg["block"], bs, device)
    t0 = time.time()
    for st in range(steps):
        x, y = next(gen)
        _, ce = m(x, y)
        pos, neg = gen_pairs(pairs_per, seed=1441000 + st)
        con = contrastive_loss(m, pos, neg, cfg["block"], device)
        loss = ce + lam * con
        opt.zero_grad(set_to_none=True)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(m.parameters(), 1.0)
        opt.step()
        if st % 50 == 0 or st == steps - 1:
            print(f"    [H1441 step {st:4d}] ce={ce.item():.4f} con={con.item():.4f} "
                  f"{(time.time()-t0)/60:.1f}min", flush=True)
    return m

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--device", default="cuda:0")
    ap.add_argument("--steps", type=int, default=400)
    ap.add_argument("--lines", type=int, default=4000)
    ap.add_argument("--lam", type=float, default=0.5)
    args = ap.parse_args()
    dev = args.device
    os.makedirs(OUT, exist_ok=True)
    print(f"[H_1441] device={dev} steps={args.steps} lam={args.lam}", flush=True)
    corpus = gen_corpus(args.lines, seed=1441)

    # contrastive-trained
    m, cfg = C.load_model(C.CKPT_BASE, dev)
    m = train(m, cfg, corpus, args.steps, dev, lam=args.lam)
    out_pt = os.path.join(OUT, "h1441_contrastive.pt")
    C.save_model(m, cfg, out_pt, {"variant": "H_1441", "steps": args.steps, "lam": args.lam})
    del m; torch.cuda.empty_cache()
    print(f"[H_1441 trained] {out_pt}", flush=True)

    # SHUFFLE-CORPUS control (same bytes, structure destroyed) — same contrastive recipe
    shuf = shuffle_bytes(corpus, seed=1441)
    ms, _ = C.load_model(C.CKPT_BASE, dev)
    ms = train(ms, cfg, shuf, args.steps, dev, lam=args.lam)
    shuf_pt = os.path.join(OUT, "h1441_shuffle.pt")
    C.save_model(ms, cfg, shuf_pt, {"variant": "H_1441_shuffle", "steps": args.steps, "lam": args.lam})
    del ms; torch.cuda.empty_cache()
    print(f"[H_1441 shuffle-control] {shuf_pt}", flush=True)
    print("[H_1441] NEXT: pt_to_engine_bin.py {trained,shuffle}.pt + base h1129c → .bin → "
          "CORE/bytegpt_decode frozen 5-bar (ENGINE-NATIVE). torch eval skipped (DIRECTIONAL).", flush=True)
    print("H1441_TRAIN_DONE", flush=True)

if __name__ == "__main__":
    main()
