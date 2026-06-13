#!/usr/bin/env python3
"""sweep_303m_en_train.py — ONE config of the 303M-EN recipe sweep.

Trains the H_1129 303M ByteGPT (d1024/L24/H16/block512, byte vocab256) on a PRE-BUILT
English-dominant corpus (sweep_303m_en_prep_corpus.py output), then scores a303m_pass
G0/G1/G2 with the FROZEN H_1129 evaluators (known_word_ratio + the graded recombination
ladder + corpus-absence novelty) — REUSED VERBATIM by importing the H_1129 module. No new
metric is invented.

Differences from h1129_*.py main(): (1) takes a PRE-BUILT --corpus (English-first, no blend
step); (2) exposes the sweep axes --dropout / --weight_decay / --lr / --warmup; (3) appends
ONE JSONL leaderboard row per run to --ledger (crash-recovery record); (4) RETRO-ready but
does NOT add the RETRO head (MODEL.md: A3 anti-fabrication gated separately on H_1147).

G0 = mean known_word_ratio over the 5 single-concept gens (a303m_pass: kwr>=0.50).
G1 = emergent recombination (some k: composed_distinct>=2 AND >max_single AND coherent).
G2 = corpus-absence novelty count (>=3 coherent corpus-absent n-grams, control=0) — measured
     with the same coverage/known-word machinery; a lightweight in-harness novelty count over
     the composed-ladder gens vs the training corpus (frozen H_1140 idea, kept simple).

Lane-G torch REFERENCE mouth (a_clm_gen_pipeline). seed 7 deterministic, p7 (NOT perplexity).
"""
from __future__ import annotations
import argparse, json, math, os, re as _re, time, sys

# import the H_1129 harness VERBATIM (model + frozen evaluators)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import h1129_midcap_broad_converged_recombination as H

import torch


def novelty_count(gens, corpus_text, n=4):
    """Corpus-absence novelty (frozen H_1140 idea, kept simple): count distinct coherent
    content n-grams in the gens that are ABSENT from the training corpus. control gens
    (verbatim corpus prefix) must score 0. Returns (novel, present)."""
    corpus_grams = set()
    cw = H.words(corpus_text)
    for i in range(len(cw) - n + 1):
        corpus_grams.add(tuple(cw[i:i + n]))
    novel, present = 0, 0
    seen = set()
    for g in gens:
        gw = H.words(g)
        for i in range(len(gw) - n + 1):
            gram = tuple(gw[i:i + n])
            if gram in seen:
                continue
            seen.add(gram)
            # coherent content gram: all tokens known words (no garble)
            if not all(w in H.KNOWN for w in gram):
                continue
            if gram in corpus_grams:
                present += 1
            else:
                novel += 1
    return novel, present


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--corpus", required=True, help="pre-built English-dominant byte corpus")
    ap.add_argument("--cfg", required=True, help="config label for the ledger")
    ap.add_argument("--host", default="aiden")
    ap.add_argument("--ledger", required=True)
    ap.add_argument("--ckpt", required=True)
    # H_1129 base arch (frozen)
    ap.add_argument("--d", type=int, default=1024)
    ap.add_argument("--n_layer", type=int, default=24)
    ap.add_argument("--n_head", type=int, default=16)
    ap.add_argument("--block", type=int, default=512)
    ap.add_argument("--bs", type=int, default=8)
    ap.add_argument("--accum", type=int, default=4)
    ap.add_argument("--steps", type=int, default=12000)
    # sweep axes
    ap.add_argument("--dropout", type=float, default=0.0)
    ap.add_argument("--weight_decay", type=float, default=0.1)
    ap.add_argument("--lr", type=float, default=3e-4)
    ap.add_argument("--warmup", type=int, default=300)
    ap.add_argument("--grad_ckpt", action="store_true")
    ap.add_argument("--eval_every", type=int, default=500)
    a = ap.parse_args()

    dev = "cuda" if torch.cuda.is_available() else "cpu"
    torch.manual_seed(7)
    if dev == "cuda":
        torch.backends.cuda.matmul.allow_tf32 = True
        torch.backends.cudnn.allow_tf32 = True
        print(f"[dev] {dev} {torch.cuda.get_device_name(0)}", flush=True)

    data = H.load_bytes(a.corpus)
    n = data.numel(); ntr = int(n * 0.98)
    tr, va = data[:ntr], data[ntr:]
    print(f"[data] {a.corpus} total={n/1e6:.1f}MB train={tr.numel()/1e6:.1f}MB val={va.numel()/1e6:.2f}MB", flush=True)

    m = H.ByteGPT(d=a.d, n_layer=a.n_layer, n_head=a.n_head, block=a.block,
                  p=a.dropout, grad_ckpt=a.grad_ckpt).to(dev)
    nparam = sum(p.numel() for p in m.parameters())
    print(f"[model] ByteGPT d={a.d} L={a.n_layer} H={a.n_head} block={a.block} "
          f"dropout={a.dropout} wd={a.weight_decay} lr={a.lr} warmup={a.warmup}", flush=True)
    print(f"[model] PARAM COUNT = {nparam:,} ({nparam/1e6:.1f}M)", flush=True)

    opt = torch.optim.AdamW(m.parameters(), lr=a.lr, betas=(0.9, 0.95), weight_decay=a.weight_decay)

    # OOM-guard fit probe
    m.train(); x, y = H.get_batch(tr, a.block, a.bs, dev)
    if dev == "cuda":
        with torch.autocast(device_type="cuda", dtype=torch.bfloat16):
            _, loss = m(x, y)
    else:
        _, loss = m(x, y)
    loss.backward(); opt.zero_grad(set_to_none=True)
    if dev == "cuda":
        print(f"[fit] OK peak={torch.cuda.max_memory_allocated()/1e9:.2f}GB / 12GB", flush=True)
        torch.cuda.reset_peak_memory_stats()

    @torch.no_grad()
    def eval_ce(d, iters=40):
        m.eval(); tot = 0.0
        for _ in range(iters):
            x, y = H.get_batch(d, a.block, a.bs, dev)
            if dev == "cuda":
                with torch.autocast(device_type="cuda", dtype=torch.bfloat16):
                    _, l = m(x, y)
            else:
                _, l = m(x, y)
            tot += l.item()
        m.train(); return tot / iters

    os.makedirs(os.path.dirname(a.ledger), exist_ok=True)

    def ledger_row(status, step, vce, g0=None, g1=None, g2=None):
        val = round(vce, 4) if vce != float("inf") else None  # valid JSONL (no Infinity literal)
        row = {"config": a.cfg, "host": a.host, "step": step, "val": val,
               "G0_kwr": (round(g0, 3) if g0 is not None else None),
               "G1": g1, "G2": g2, "status": status, "ckpt_path": a.ckpt,
               "nparam": nparam,
               "axes": {"dropout": a.dropout, "weight_decay": a.weight_decay,
                        "lr": a.lr, "warmup": a.warmup, "steps": a.steps},
               "ts": time.strftime("%Y-%m-%dT%H:%M:%S")}
        with open(a.ledger, "a") as f:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")

    ledger_row("started", 0, float("inf"))
    print(f"\n[train] {a.steps} steps bs={a.bs} accum={a.accum} (eff {a.bs*a.accum}) cosine warmup={a.warmup}", flush=True)
    best_val = float("inf"); t0 = time.time(); m.train()
    for st in range(a.steps):
        if st < a.warmup:
            lr_t = a.lr * (st + 1) / a.warmup
        else:
            prog = min(1.0, (st - a.warmup) / max(1, a.steps - a.warmup))
            lr_t = a.lr * 0.5 * (1 + math.cos(math.pi * prog))
        for g in opt.param_groups:
            g["lr"] = lr_t
        opt.zero_grad(set_to_none=True)
        acc_loss = 0.0
        for _ in range(a.accum):
            x, y = H.get_batch(tr, a.block, a.bs, dev)
            if dev == "cuda":
                with torch.autocast(device_type="cuda", dtype=torch.bfloat16):
                    _, loss = m(x, y)
            else:
                _, loss = m(x, y)
            (loss / a.accum).backward(); acc_loss += loss.item() / a.accum
        torch.nn.utils.clip_grad_norm_(m.parameters(), 1.0)
        opt.step()
        if st % a.eval_every == 0 or st == a.steps - 1:
            vce = eval_ce(va); dt = time.time() - t0
            print(f"  step {st:5d} train_ce={acc_loss:.4f} val_ce={vce:.4f} lr={lr_t:.2e} {dt/60:.1f}min", flush=True)
            if vce < best_val:
                best_val = vce
                torch.save({"model": m.state_dict(),
                            "config": {"vocab": 256, "d": a.d, "n_layer": a.n_layer,
                                       "n_head": a.n_head, "block": a.block},
                            "val_ce": vce, "step": st, "nparam": nparam}, a.ckpt)
            ledger_row("training", st, vce)
    print(f"[train] done best_val_ce={best_val:.4f} ckpt={a.ckpt} wall={(time.time()-t0)/60:.1f}min", flush=True)

    # ── reload best ckpt, run the FROZEN H_1129 ladder + novelty ──
    ck = torch.load(a.ckpt, map_location=dev, weights_only=False)
    m.load_state_dict(ck["model"]); m.grad_ckpt = False
    print(f"[ladder] best ckpt step={ck['step']} val_ce={ck['val_ce']:.4f}", flush=True)

    # G0: mean kwr over single-concept gens (frozen evaluator)
    single_gens = [H.gen(m, f"{c}. ", 80, dev, a.block) for c, _ in H.CONCEPTS]
    g0_kwr = sum(H.known_word_ratio(g) for g in single_gens) / len(single_gens)

    # G1: frozen recombination ladder
    max_single, ladder, emergent = H.run_ladder(m, dev, a.block)

    # G2: corpus-absence novelty over the composed-ladder gens (control = verbatim prefix -> 0)
    corpus_text = bytes(data[: min(data.numel(), 40 * 1024 * 1024)].tolist()).decode("utf-8", "ignore")
    comp_gens = [ladder[k]["text"] for k in (2, 3, 4, 5)]
    g2_novel, g2_present = novelty_count(comp_gens, corpus_text)
    ctrl_prefix = corpus_text[:400]
    g2_ctrl_novel, _ = novelty_count([ctrl_prefix], corpus_text)

    g0_pass = g0_kwr >= 0.50
    g1_pass = emergent
    g2_pass = (g2_novel >= 3 and g2_ctrl_novel == 0)
    print("\n=== a303m_pass SCORES (frozen p7) ===", flush=True)
    print(f"  G0_kwr (mean single) = {g0_kwr:.3f}  pass={g0_pass}", flush=True)
    print(f"  G1 recombination emergent = {emergent}  pass={g1_pass}", flush=True)
    print(f"  G2 novelty novel={g2_novel} present={g2_present} ctrl={g2_ctrl_novel}  pass={g2_pass}", flush=True)

    ledger_row("done", ck["step"], best_val, g0=g0_kwr,
               g1={"emergent": emergent, "max_single": max_single,
                   "ladder": {k: {"composed_distinct": ladder[k]["composed_distinct"],
                                  "kwr": ladder[k]["kwr"], "clears": ladder[k]["clears"]}
                              for k in (2, 3, 4, 5)}},
               g2={"novel": g2_novel, "present": g2_present, "control": g2_ctrl_novel,
                   "pass": g2_pass})

    json.dump({"config": a.cfg, "nparam": nparam, "best_val_ce": best_val,
               "G0_kwr": g0_kwr, "G0_pass": g0_pass, "G1_emergent": emergent,
               "G2_novel": g2_novel, "G2_present": g2_present, "G2_control": g2_ctrl_novel,
               "G2_pass": g2_pass, "max_single": max_single,
               "ladder": {k: ladder[k] for k in (2, 3, 4, 5)}},
              open(a.ckpt + ".result.json", "w"), ensure_ascii=False, indent=2)
    print(f"[done] {a.ckpt}.result.json", flush=True)


if __name__ == "__main__":
    main()
