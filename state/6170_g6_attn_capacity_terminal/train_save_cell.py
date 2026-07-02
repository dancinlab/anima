#!/usr/bin/env python3
"""train_save_cell.py — H_6165 SINGLE-cell re-run WITH ckpt-save (a_fire_recover_complete).

Reuses the VERBATIM campaign harness in ~/g6_h6165 (g6_common, bindattn_stack, h1435).
Trains ONE cell and SAVES the trained injected stack as a torch .pt in the
{"bind": [block_sd,...], "gate": [float,...], "config": {...}} contract that
core/serialize.py::serialize_bind + `anima serialize-bind` expects — closing the
JSON-only gap of run_factorial.py.

Usage: python3 train_save_cell.py --reg on --nblocks 2 --seed 7 --steps 600 --out <path.pt>
"""
import os, sys, json, time, argparse

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
os.environ.setdefault("G6_PROBES", HERE)
os.environ.setdefault("G6_CKPT", os.path.join(HERE, "h1129c_chat.pt"))

import g6_common as C
import bindattn_stack as BS
import h1435_continued_pretrain as H1435
import run_factorial as RF


def save_injected_stack(m, cfg, out_path, meta):
    import torch
    # m.bind = nn.ModuleList[Block]; m.gates = nn.ParameterList[scalar]
    binds = [blk.state_dict() for blk in m.bind]
    gates = [float(g.detach().cpu().reshape(-1)[0]) for g in m.gates]
    ck = {
        "bind": binds,   # list of Block state_dicts (serialize_bind _normalize_bind_list)
        "gate": gates,   # list of gate floats, index-aligned to bind
        "config": {"vocab": 256, "d": cfg["d"], "n_layer": cfg["n_layer"],
                   "n_head": cfg["n_head"], "block": cfg["block"]},
        "meta": meta,
        "note": "H_6165 injected BindAttn stack; load base .bin then splice via "
                "anima serialize-bind (BGB trailer). gate index-aligned to bind list.",
    }
    torch.save(ck, out_path)
    return binds, gates


def main():
    import torch
    ap = argparse.ArgumentParser()
    ap.add_argument("--device", default="cuda:0")
    ap.add_argument("--reg", required=True, choices=["on", "off"])
    ap.add_argument("--nblocks", type=int, required=True)
    ap.add_argument("--seed", type=int, required=True)
    ap.add_argument("--steps", type=int, default=600)
    ap.add_argument("--lines", type=int, default=4000)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    dev = args.device

    print("[train_save] reg=%s N=%d seed=%d steps=%d dev=%s" %
          (args.reg, args.nblocks, args.seed, args.steps, dev), flush=True)
    base, cfg = C.load_base(C.CKPT_BASE, dev)
    for p in base.parameters():
        p.requires_grad_(False)

    corpus_seed = 6165 if args.reg == "on" else 6166
    corpus = RF.build_corpus(args.reg, args.lines, seed=corpus_seed)
    t0 = time.time()
    m = RF.train_stack(base, cfg, args.nblocks, corpus, args.steps, dev, args.seed,
                       tag="REG-" + args.reg)
    train_min = (time.time() - t0) / 60.0
    print("[train_save] trained in %.1f min" % train_min, flush=True)

    meta = {"H": "H_6165", "cell": "REG-%s N=%d seed=%d" % (args.reg, args.nblocks, args.seed),
            "steps": args.steps, "lines": args.lines, "corpus_seed": corpus_seed,
            "base_sha_note": "h1129c_chat.pt", "train_min": round(train_min, 2)}
    binds, gates = save_injected_stack(m, cfg, args.out, meta)
    print("[train_save] SAVED %s  n_bind=%d gates=%s" %
          (args.out, len(binds), [round(g, 6) for g in gates]), flush=True)
    print("[train_save] block keys=%s" % sorted(binds[0].keys()), flush=True)
    print("[train_save] DONE", flush=True)


if __name__ == "__main__":
    main()
