#!/usr/bin/env python3
"""H_1435 — continued-pretrain on a falsifiable-claim natural-language corpus.

ANGLE (capacity vs learn-distribution-gap separation): the base 303M produces
comparative OR measurable shapes but does not BIND them into one negatable claim.
H_1435 asks: is that a CAPACITY ceiling, or just a TRAINING-DISTRIBUTION gap (the
chat corpus rarely contains falsifiable-claim FORM)? Full-weight continued-pretrain
on a corpus DENSE in falsifiable claims; then re-measure the FROZEN 5-bar.

The falsifiable-claim corpus is GENERATED structurally (templated comparator+measurable
claims over neutral subjects DISJOINT from the gauge_lib CONCEPT keywords) — anti-tune-
to-green: the eval seeds + held-out seeds + CONCEPT subjects are NOT the training subjects,
so the model cannot memorize an eval string. The shuffle-corpus control trains on the
SAME bytes token-shuffled (structure destroyed) — lift there = artifact => INVALID.
"""
import os, sys, json, random, time, argparse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import g6_common as C
import torch

OUT = os.environ.get("G6_OUT", "/workspace/g6/out")

# ── falsifiable-claim corpus (training-only subjects, DISJOINT from eval) ──
TRAIN_SUBJECTS = ["the river", "a metal bar", "the crowd", "this alloy", "the signal",
                  "a colony", "the market", "that current", "the sample", "a fold"]
COMPS = sorted(C.COMPARATOR)
MEAS = sorted(C.MEASURABLE)


def gen_corpus(n_lines, seed=0):
    rng = random.Random(seed)
    lines = []
    templates = [
        "if {s} grows, the {m} {c} than before.",
        "{s} {c} a higher {m} when the input rises.",
        "the {m} of {s} is greater whenever {s2} {c}.",
        "{s} shows a lower {m} than {s2} under load.",
        "when {s} {c}, its {m} decreases by a fixed amount.",
    ]
    for _ in range(n_lines):
        t = rng.choice(templates)
        lines.append(t.format(s=rng.choice(TRAIN_SUBJECTS),
                              s2=rng.choice(TRAIN_SUBJECTS),
                              c=rng.choice(COMPS), m=rng.choice(MEAS)))
    return "\n".join(lines) + "\n"


def shuffle_bytes(text, seed=0):
    rng = random.Random(seed)
    b = list(text.encode("utf-8"))
    rng.shuffle(b)
    return bytes(b).decode("utf-8", "ignore")


def make_batches(text, block, bs, device):
    data = torch.tensor(list(text.encode("utf-8")), dtype=torch.long)
    n = (len(data) - 1) // block
    data = data[: n * block + 1]
    while True:
        idxs = torch.randint(0, len(data) - block - 1, (bs,))
        x = torch.stack([data[i:i + block] for i in idxs]).to(device)
        y = torch.stack([data[i + 1:i + 1 + block] for i in idxs]).to(device)
        yield x, y


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
            print(f"    [H1435 step {st:4d}] ce={loss.item():.4f} {(time.time()-t0)/60:.1f}min",
                  flush=True)
    return m


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--device", default="cuda:0")
    ap.add_argument("--steps", type=int, default=400)
    ap.add_argument("--lines", type=int, default=4000)
    args = ap.parse_args()
    dev = args.device

    print(f"[H_1435] device={dev} steps={args.steps}", flush=True)
    base_m, cfg = C.load_model(C.CKPT_BASE, dev)
    base_eval = C.evaluate(base_m, cfg, "base", list(C.g.IDEATION_SEEDS))
    print(f"[H_1435] base FALS_in={base_eval['FALS_in']} DIST_in={base_eval['DIST_in']} "
          f"FALS_ho={base_eval['FALS_ho']}", flush=True)
    del base_m
    torch.cuda.empty_cache()

    corpus = gen_corpus(args.lines, seed=1435)

    # REAL continued-pretrain
    m, _ = C.load_model(C.CKPT_BASE, dev)
    m = train(m, cfg, corpus, args.steps, dev)
    out_pt = os.path.join(OUT, "h1435_continued_pretrain.pt")
    C.save_model(m, cfg, out_pt, {"variant": "H_1435", "steps": args.steps, "lr": 3e-5})
    trained_eval = C.evaluate(m, cfg, "trained", list(C.g.IDEATION_SEEDS))
    del m
    torch.cuda.empty_cache()

    # SHUFFLE-CORPUS control (same bytes, structure destroyed)
    shuf_corpus = shuffle_bytes(corpus, seed=1435)
    ms, _ = C.load_model(C.CKPT_BASE, dev)
    ms = train(ms, cfg, shuf_corpus, args.steps, dev)
    shuf_eval = C.evaluate(ms, cfg, "shuffle_corpus", list(C.g.IDEATION_SEEDS))
    del ms
    torch.cuda.empty_cache()

    bars = C.print_bars("H_1435 continued-pretrain", base_eval, trained_eval, shuf_eval)

    out = {"variant": "H_1435", "ckpt_base": C.CKPT_BASE, "ckpt_out": out_pt,
           "base": base_eval, "trained": trained_eval, "shuffle_corpus": shuf_eval,
           "bars": bars}
    os.makedirs(OUT, exist_ok=True)
    json.dump(out, open(os.path.join(OUT, "h1435_result.json"), "w"), ensure_ascii=False, indent=2)
    print(f"[H_1435 done] {OUT}/h1435_result.json", flush=True)


if __name__ == "__main__":
    main()
