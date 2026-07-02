#!/usr/bin/env python3
"""run_factorial.py - H_6165 CAP x REG factorial G6 IDEATION* FALS fire (DIRECTIONAL screen).

Isolates the H_1449 confound (lift = attention CAPACITY vs corpus-REGISTER exposure) by
crossing two factors on the FROZEN h1305 detector + g6_common 5-bar battery (VERBATIM reuse):

  FACTOR CAP  = n_blocks of injected gated BindAttn stack (1 / 2 / 4), base 303M FROZEN.
  FACTOR REG  = training corpus register:
      REG-on  = h1435 co-emission corpus (every line binds a comparator AND a measurable).
      REG-off = split-leg corpus: SAME subjects/vocab/volume, but each line carries a
                comparator XOR a measurable, NEVER both -> removes ONLY the co-emission
                STRUCTURE (the register), holding token exposure ~constant.

Per cell: freeze_base train (only the injected stack), then FROZEN 5-bar (B1..B5) +
c4 ABLATE (all gates->0 identity; lift must regress to base else INERT=register-not-capacity)
+ conditional SHUF-CORP sibling (byte-shuffled corpus; lift there = artifact).

torch-side = DIRECTIONAL (a_engine_native_learning). Terminal engine-native read =
`anima evaluate --py <base .bin>` (base G6 floor anchor); a GREEN cell needs a wire-in
follow-on (BindAttn-stack not directly engine-mountable) => stays DIRECTIONAL until wired.

NO tune-to-green (c9/p7): detector + bars FROZEN in g6_common before any weight touched.
"""
import os, sys, json, time, random, argparse

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
PROBES = os.environ.get("G6_PROBES", HERE)
sys.path.insert(0, PROBES)

import g6_common as C
import bindattn_stack as BS
import h1435_continued_pretrain as H1435

TRAIN_SUBJECTS = H1435.TRAIN_SUBJECTS
COMPS = H1435.COMPS
MEAS = H1435.MEAS

COMP_ONLY = [
    "if {s} grows, then {s2} {c} before.",
    "{s} {c} more than {s2} under load.",
    "when {s} {c}, {s2} responds each day.",
    "{s} {c} again after {s2} moved.",
    "the way {s} {c} kept {s2} steady.",
]
MEAS_ONLY = [
    "the {m} of {s} stayed fixed all day.",
    "{s} recorded a steady {m} once again.",
    "we logged the {m} for {s} again.",
    "the {m} near {s} held overnight.",
    "a plain {m} of {s} was noted.",
]


def gen_corpus_reg_on(n_lines, seed):
    return H1435.gen_corpus(n_lines, seed=seed)


def gen_corpus_reg_off(n_lines, seed):
    # token-exposure matched to REG-on: n_lines comparator-only + n_lines measurable-only
    # (REG-on has n_lines lines each carrying BOTH marks; REG-off carries the SAME per-mark
    # token count, only the WITHIN-LINE co-occurrence is removed).
    rng = random.Random(seed)
    lines = []
    for _ in range(n_lines):
        tc = rng.choice(COMP_ONLY)
        lines.append(tc.format(s=rng.choice(TRAIN_SUBJECTS),
                               s2=rng.choice(TRAIN_SUBJECTS), c=rng.choice(COMPS)))
        tm = rng.choice(MEAS_ONLY)
        lines.append(tm.format(s=rng.choice(TRAIN_SUBJECTS), m=rng.choice(MEAS)))
    rng.shuffle(lines)
    return "\n".join(lines) + "\n"


def build_corpus(reg, n_lines, seed):
    return gen_corpus_reg_on(n_lines, seed) if reg == "on" else gen_corpus_reg_off(n_lines, seed)


def train_stack(base, cfg, N, corpus, steps, device, seed, lr=3e-5, bs=16, tag=""):
    import torch
    torch.manual_seed(seed)
    m = BS.build_stack_model(base, cfg["n_head"], N, ablate_off=False).to(device)
    BS.freeze_base(m)
    params = [p for p in m.parameters() if p.requires_grad]
    n_train = sum(p.numel() for p in params)
    opt = torch.optim.AdamW(params, lr=lr, betas=(0.9, 0.95), weight_decay=0.1)
    gen = H1435.make_batches(corpus, cfg["block"], bs, device)
    m.train()
    t0 = time.time()
    for st in range(steps):
        x, y = next(gen)
        _, loss = m(x, y)
        opt.zero_grad(set_to_none=True)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(params, 1.0)
        opt.step()
        if st % 100 == 0 or st == steps - 1:
            print("      [%s N=%d step %4d] ce=%.4f train_params=%.1fM %.1fmin" %
                  (tag, N, st, loss.item(), n_train/1e6, (time.time()-t0)/60), flush=True)
    return m


def run_cell(base, cfg, base_eval, N, reg, seed, steps, n_lines, device, out_dir, do_shuf):
    import torch
    tag = "REG-" + reg
    corpus = build_corpus(reg, n_lines, seed=6165 if reg == "on" else 6166)
    m = train_stack(base, cfg, N, corpus, steps, device, seed, tag=tag)

    m.ablate_off = False
    trained_eval = C.evaluate(m, cfg, "trained_N%d_%s_s%d" % (N, reg, seed), list(C.g.IDEATION_SEEDS))
    m.ablate_off = True
    ablate_eval = C.evaluate(m, cfg, "ablate_N%d_%s_s%d" % (N, reg, seed), list(C.g.IDEATION_SEEDS))
    m.ablate_off = False
    del m
    torch.cuda.empty_cache()

    shuf_eval = None
    if do_shuf and trained_eval["FALS_in"] >= 1:
        shuf_corpus = H1435.shuffle_bytes(corpus, seed=seed)
        ms = train_stack(base, cfg, N, shuf_corpus, steps, device, seed, tag=tag + "-SHUF")
        ms.ablate_off = False
        shuf_eval = C.evaluate(ms, cfg, "shufcorp_N%d_%s_s%d" % (N, reg, seed), list(C.g.IDEATION_SEEDS))
        del ms
        torch.cuda.empty_cache()

    name = "CELL N=%d REG-%s seed=%d" % (N, reg, seed)
    bars = C.print_bars(name, base_eval, trained_eval, shuf_eval, ablate_eval)

    rec = {"cell": {"N": N, "reg": reg, "seed": seed, "steps": steps, "n_lines": n_lines},
           "base": base_eval, "trained": trained_eval,
           "ablate": ablate_eval, "shuf_corp": shuf_eval, "bars": bars}
    op = os.path.join(out_dir, "cell_N%d_REG%s_s%d.json" % (N, reg, seed))
    json.dump(rec, open(op, "w"), ensure_ascii=False, indent=2)
    print("[cell done] %s  green=%s" % (op, bars["green"]), flush=True)
    return rec


def main():
    import torch
    ap = argparse.ArgumentParser()
    ap.add_argument("--device", default="cuda:0")
    ap.add_argument("--reg", required=True, choices=["on", "off"])
    ap.add_argument("--nblocks", default="1,2,4")
    ap.add_argument("--seeds", default="7,4302,4303")
    ap.add_argument("--steps", type=int, default=600)
    ap.add_argument("--lines", type=int, default=4000)
    ap.add_argument("--no-shuf", action="store_true")
    ap.add_argument("--out", default=os.path.join(HERE, "results"))
    args = ap.parse_args()
    os.makedirs(args.out, exist_ok=True)
    dev = args.device
    Ns = [int(x) for x in args.nblocks.split(",")]
    seeds = [int(x) for x in args.seeds.split(",")]

    print("[factorial] device=%s reg=%s N=%s seeds=%s steps=%d" %
          (dev, args.reg, Ns, seeds, args.steps), flush=True)
    base, cfg = C.load_base(C.CKPT_BASE, dev)
    for p in base.parameters():
        p.requires_grad_(False)
    base_eval = C.evaluate(base, cfg, "base", list(C.g.IDEATION_SEEDS))
    print("[factorial] BASE FALS_in=%s DIST_in=%s FALS_shuf=%s FALS_ho=%s" %
          (base_eval["FALS_in"], base_eval["DIST_in"], base_eval["FALS_shuf"],
           base_eval["FALS_ho"]), flush=True)
    json.dump(base_eval, open(os.path.join(args.out, "base_eval_%s.json" % args.reg), "w"),
              ensure_ascii=False, indent=2)

    all_recs = []
    for N in Ns:
        for seed in seeds:
            try:
                rec = run_cell(base, cfg, base_eval, N, args.reg, seed, args.steps,
                               args.lines, dev, args.out, do_shuf=not args.no_shuf)
                all_recs.append(rec)
            except Exception as e:
                import traceback
                print("[cell ERROR] N=%d reg=%s seed=%d: %s" % (N, args.reg, seed, e), flush=True)
                traceback.print_exc()
    json.dump(all_recs, open(os.path.join(args.out, "all_cells_REG%s.json" % args.reg), "w"),
              ensure_ascii=False, indent=2)
    print("[factorial done] reg=%s cells=%d" % (args.reg, len(all_recs)), flush=True)


if __name__ == "__main__":
    main()
