#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""derivtrace multi-pair robustness — close the H_9124 open caveat with the CANONICAL corpus tool ($0 toy).

#3043: F2 corpus = `anima corpus derivtrace` (cli/corpus.py 'G1 data-format lever'), NOT a hand-gen.
H_9124: derivation-trace = first engine-native G1 lift (DERIV PASS bd=2>ms=1 vs FLAT FAIL) on held-out
{c0,c1} — but 🔴 NOT-ROBUST (multi-pair 재현실패 · single-pair bd=2 artifact · robustness follow-on open).
That verdict came from expensive 303M warm-FT centered on ONE held-out pair. This closes the multi-pair
robustness caveat cheaply: import cli/corpus.py's CANONICAL build() (no reinvention, a_cli_single_entry),
generate derivtrace + flat (content-matched control, same seed) for EACH of several held-out pairs, train
a toy byte-LM on each arm, and score held-out composition = distinct concept-families bound in the emitted
OUT (a best_distinct analog: 2 families = composed; 1 = echo). Robust iff DERIV > FLAT consistently.

  score: greedy-decode OUT for the held-out pair prompt; count distinct held-out families whose keywords
         appear in the emitted OUT. distinct=2 => composed both concepts; =1 => echo/single.
  robust-PASS : DERIV distinct >= 2 AND > FLAT distinct on >= majority of held-out pairs (consistent lift).
  NOT-ROBUST  : DERIV lift over FLAT not consistent across pairs (confirms H_9124 🔴).
toy=DIRECTIONAL (a_toy_scale_recheck); 303M anima evaluate --py = TERMINAL. summer torch.
"""
import os, sys, json, argparse
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(REPO, "cli"))
import corpus as C          # CANONICAL anima corpus generator (cli/corpus.py) — no reinvention
import atd_crux as A        # reuse the toy byte-LM trainer

def score_holdout(greedy, S, KW, held, block=64):
    """distinct concept-families whose keywords appear in the emitted OUT for the held-out pair."""
    i, j = held
    prompt = f"{S[i]}. {S[j]}. "
    gen = greedy(prompt, n=80)                         # emit the OUT (+ maybe deriv for derivtrace)
    low = gen.lower()
    fam_i = sum(1 for w in KW[i] if w.lower() in low)
    fam_j = sum(1 for w in KW[j] if w.lower() in low)
    distinct = int(fam_i > 0) + int(fam_j > 0)
    return dict(distinct=distinct, fam_i_hits=fam_i, fam_j_hits=fam_j, emitted=gen[:120])

def run_pair(held, seed, comp_per_pair=200, single_per_concept=200):
    S, KW = C.DEFAULT_SEEDS, C.DEFAULT_KW
    out = {}
    for fmt in ("derivtrace", "flat"):
        text, train_pairs = C.build(fmt, S, KW, held, comp_per_pair, single_per_concept, seed)
        lh, gr = A.train_bytelm(text, seed, steps=8000)      # canonical corpus -> toy byte-LM
        sc = score_holdout(gr, S, KW, held)
        out[fmt] = dict(bytes=len(text.encode()), n_train_pairs=len(train_pairs), **sc)
    out["held"] = list(held); out["seed"] = seed
    out["deriv_beats_flat"] = bool(out["derivtrace"]["distinct"] >= 2 and
                                   out["derivtrace"]["distinct"] > out["flat"]["distinct"])
    return out

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pairs", default="0,1;2,3;1,4;0,3;2,4")   # multi held-out pairs (robustness)
    ap.add_argument("--seed", default="7"); ap.add_argument("--out", default="DERIVTRACE_ROBUST_RESULT.json")
    a = ap.parse_args()
    pairs = [tuple(int(x) for x in p.split(",")) for p in a.pairs.split(";")]
    seed = int(a.seed)
    cells = []
    for held in pairs:
        c = run_pair(held, seed); cells.append(c)
        print(f"  held={held}: DERIV distinct={c['derivtrace']['distinct']}(i{c['derivtrace']['fam_i_hits']}/j{c['derivtrace']['fam_j_hits']}) "
              f"FLAT distinct={c['flat']['distinct']}(i{c['flat']['fam_i_hits']}/j{c['flat']['fam_j_hits']}) "
              f"deriv>flat={c['deriv_beats_flat']}", flush=True)
    n = len(cells); n_deriv_pass = sum(c["deriv_beats_flat"] for c in cells)
    n_deriv_2 = sum(c["derivtrace"]["distinct"] >= 2 for c in cells)
    n_flat_2 = sum(c["flat"]["distinct"] >= 2 for c in cells)
    if n_deriv_pass >= (n + 1) // 2 and n_deriv_2 > n_flat_2:
        verdict = "DERIV-ROBUST-consistent-lift-over-flat"
    elif n_deriv_2 == 0:
        verdict = "DERIV-FLOOR-no-composition (converges with ATD CLEAN-KILL)"
    else:
        verdict = "NOT-ROBUST-confirms-H9124 (inconsistent deriv lift across pairs)"
    out = dict(probe="derivtrace multi-pair robustness (canonical cli/corpus.py, toy byte-LM)",
               n_pairs=n, n_deriv_beats_flat=n_deriv_pass, n_deriv_distinct2=n_deriv_2,
               n_flat_distinct2=n_flat_2, verdict=verdict, cells=cells)
    json.dump(out, open(os.path.join(HERE, a.out), "w"), ensure_ascii=False, indent=1)
    print(f"\nVERDICT: {verdict}  (deriv>flat {n_deriv_pass}/{n} · deriv-distinct2 {n_deriv_2}/{n} · flat-distinct2 {n_flat_2}/{n})")

if __name__ == "__main__":
    main()
