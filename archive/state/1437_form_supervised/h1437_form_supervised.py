#!/usr/bin/env python3
"""H_1437 — H_1314 negatable-form scaffold supervised training, then FREE generation.

ANGLE: H_1314 supplied a negatable-form SCAFFOLD ("if A, then B: <claim>") externally.
H_1437 internalizes it: SUPERVISE the model on the negatable-form FORMAT (scaffold ->
completed falsifiable claim) so the FORM becomes native, then evaluate FREE generation
(no scaffold at eval). If form-supervision transfers to free generation, the model
emits negatable claims unprompted; the cross-shuffle control then tests whether the bind
is EARNED (idea-specific) or a generic learned template that always satisfies the detector
(the H_1413/H_1434 form-lift trap).

The supervision targets are TEMPLATED claims over training-only subjects (eval-disjoint).
Eval is FREE: gauge_lib IDEATION_SEEDS (in-domain) + HELD-OUT seeds. shuffle-corpus control
trains on byte-shuffled targets => if lift persists it is an artifact => INVALID.
"""
import os, sys, json, random, time, argparse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import g6_common as C
import torch

OUT = os.environ.get("G6_OUT", "/workspace/g6/out")

import h1435_continued_pretrain as base1435
TRAIN_SUBJECTS = base1435.TRAIN_SUBJECTS
COMPS = base1435.COMPS
MEAS = base1435.MEAS
shuffle_bytes = base1435.shuffle_bytes
make_batches = base1435.make_batches


def gen_scaffold_corpus(n_lines, seed=0):
    """Negatable-form scaffold -> completed falsifiable claim (H_1314 form), so the
    model learns to COMPLETE a scaffold into a negatable claim. The scaffold prefix
    is the H_1314 shape; the completion binds a comparator + a measurable."""
    rng = random.Random(seed)
    lines = []
    for _ in range(n_lines):
        s = rng.choice(TRAIN_SUBJECTS)
        s2 = rng.choice(TRAIN_SUBJECTS)
        c = rng.choice(COMPS)
        m = rng.choice(MEAS)
        # scaffold then completion on the SAME line (form-supervised)
        line = f"a testable claim: if {s} changes, then the {m} of {s2} is {c} measured."
        lines.append(line)
    return "\n".join(lines) + "\n"


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
            print(f"    [H1437 step {st:4d}] ce={loss.item():.4f} {(time.time()-t0)/60:.1f}min",
                  flush=True)
    return m


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--device", default="cuda:0")
    ap.add_argument("--steps", type=int, default=400)
    ap.add_argument("--lines", type=int, default=4000)
    args = ap.parse_args()
    dev = args.device

    print(f"[H_1437] device={dev} steps={args.steps}", flush=True)
    base_m, cfg = C.load_model(C.CKPT_BASE, dev)
    base_eval = C.evaluate(base_m, cfg, "base", list(C.g.IDEATION_SEEDS))
    print(f"[H_1437] base FALS_in={base_eval['FALS_in']} FALS_ho={base_eval['FALS_ho']}", flush=True)
    del base_m; torch.cuda.empty_cache()

    corpus = gen_scaffold_corpus(args.lines, seed=1437)

    m, _ = C.load_model(C.CKPT_BASE, dev)
    m = train(m, cfg, corpus, args.steps, dev)
    out_pt = os.path.join(OUT, "h1437_form_supervised.pt")
    C.save_model(m, cfg, out_pt, {"variant": "H_1437", "steps": args.steps})
    # FREE generation eval (no scaffold given at eval)
    trained_eval = C.evaluate(m, cfg, "trained", list(C.g.IDEATION_SEEDS))
    del m; torch.cuda.empty_cache()

    shuf_corpus = shuffle_bytes(corpus, seed=1437)
    ms, _ = C.load_model(C.CKPT_BASE, dev)
    ms = train(ms, cfg, shuf_corpus, args.steps, dev)
    shuf_eval = C.evaluate(ms, cfg, "shuffle_corpus", list(C.g.IDEATION_SEEDS))
    del ms; torch.cuda.empty_cache()

    bars = C.print_bars("H_1437 form-supervised", base_eval, trained_eval, shuf_eval)
    out = {"variant": "H_1437", "ckpt_base": C.CKPT_BASE, "ckpt_out": out_pt,
           "base": base_eval, "trained": trained_eval, "shuffle_corpus": shuf_eval, "bars": bars}
    os.makedirs(OUT, exist_ok=True)
    json.dump(out, open(os.path.join(OUT, "h1437_result.json"), "w"), ensure_ascii=False, indent=2)
    print(f"[H_1437 done] {OUT}/h1437_result.json", flush=True)


if __name__ == "__main__":
    main()
