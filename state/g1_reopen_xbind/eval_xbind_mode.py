#!/usr/bin/env python3
"""eval_xbind_mode.py — fold-in `--xbind` mode for the canonical py evaluator
(place xbind_run() beside interaction_lift_run(); add the dispatch stanza
`if "--xbind" in argv: return xbind_run(argv)` in main(), mirroring the
--interaction-lift precedent). Engine-native numpy core/decode.py only
(a_eval_py_canonical -> TERMINAL-eligible). Design SSOT: DESIGN_PREREG.md.

Usage (after fold-in):
  anima-py evaluate <ckpt.clm> --xbind xbind_eval_manifest.json \
      --out xbind_eval_<arm>_<seed>.json [--arm main|ctrl] [--gen 16] [--win 64] \
      [--n-decode 200] [--n-sampled 40]

Scores (ALL raw outputs dumped — full-capture, never tail-truncate a control):
  PRIMARY   D-acc  : greedy (top_k=1) decode, first emitted word == gold branch word
                     ("fuse"/"part"), per split {heldout, seen}. Deterministic,
                     sampler-artifact-free.
  CONSTRUCT C-rate : gold-fuse held-out items only — order-covariant portmanteau
                     "<ab>." appears in the greedy output (novel byte string for
                     held-out pairs by construction = the constructive tier).
  MARGIN            : teacher-forced NLL(counterfactual) - NLL(gold) over the full
                     continuation via _fwd_logits (win=64 forward; decode-window-free
                     secondary, robust to sampling).
  SAMPLED (2nd)     : canonical top_k=40 temp=0.7, rng {7,4302,4303} majority D-hit
                     on the first --n-sampled items (seed-robustness check).

Arm semantics: --arm ctrl scores the shuffle-control model. Its SEEN gold =
gold_word_ctrl (its own memorized coin); its HELDOUT gold = the rule gold (no rule
in its corpus -> expected ~=0.5 = the instrument-leak floor V-B).
"""
import json
import math


def _first_word(text):
    t = text.strip()
    return t.split()[0].strip(",.;:") if t.split() else ""


def _cont_nll(np, clm, W, seed, cont, T):
    """Sum NLL of `cont` bytes given `seed` (right-aligned window T forward)."""
    text = seed + cont
    tok = clm._seed_to_tok(text, T)
    logits = clm._fwd_logits(W, tok, T)
    k = len(cont.encode())
    lo = max(0, T - 1 - k)
    s = 0.0
    for i in range(lo, T - 1):
        row = logits[i]
        m = float(np.max(row))
        lse = m + math.log(float(np.sum(np.exp(row - m))) + 1e-30)
        s += lse - float(row[int(tok[i + 1])])
    return s


def xbind_run(argv):
    import numpy as np
    ckpt = argv[0]
    spec_path = evaluate_strval(argv[1:], "--xbind", "")
    out_path = evaluate_strval(argv[1:], "--out", "xbind_eval.json")
    arm = evaluate_strval(argv[1:], "--arm", "main")
    spec = json.load(open(spec_path))
    gen = evaluate_intval(argv[1:], "--gen", int(spec.get("gen", 16)))
    T = evaluate_intval(argv[1:], "--win", int(spec.get("win", 64)))
    n_dec = evaluate_intval(argv[1:], "--n-decode", 200)
    n_smp = evaluate_intval(argv[1:], "--n-sampled", 40)

    print("=== anima evaluate --xbind — held-out XBIND recombination (G1 reopen lane a) ===")
    print("ckpt: " + ckpt + "  arm=" + arm + "  gen=%d win=%d" % (gen, T))
    W = clm.clm_load_weights(ckpt)
    if not W.get("ok"):
        print("ERROR: ckpt not decodable (clm): " + ckpt)
        return 1

    res = {"ckpt": ckpt, "arm": arm, "gen": gen, "win": T, "splits": {}}
    for split in ("heldout", "seen"):
        items = spec[split][:n_dec]
        rows = []
        d_hits = c_hits = c_n = 0
        margins = []
        for ix, it in enumerate(items):
            gold_w = it["gold_word"]
            if arm == "ctrl" and split == "seen":
                gold_w = it["gold_word_ctrl"]
            o = clm.clm_decode_topk_sampled_W(W, it["seed"], gen, 1, 0.7, 7)["text"]
            fw = _first_word(o)
            d_hit = int(fw == gold_w)
            d_hits += d_hit
            c_hit = None
            if it.get("construct") and arm == "main":
                c_hit = int(it["construct"] in o)
                c_hits += c_hit
                c_n += 1
            mg = (_cont_nll(np, clm, W, it["seed"], it["counterfactual"], T)
                  - _cont_nll(np, clm, W, it["seed"], it["gold"], T))
            margins.append(mg)
            smp = None
            if ix < n_smp:
                votes = 0
                for r in (7, 4302, 4303):
                    os_ = clm.clm_decode_topk_sampled_W(W, it["seed"], gen, 40, 0.7, r)["text"]
                    votes += int(_first_word(os_) == gold_w)
                smp = int(votes >= 2)
            rows.append({"a": it["a"], "b": it["b"], "gold_word": gold_w,
                         "first_word": fw, "d_hit": d_hit, "c_hit": c_hit,
                         "margin": mg, "sampled_maj": smp, "raw": o})
            if (ix + 1) % 25 == 0:
                print("  [xbind %s #%d/%d] d_acc=%.3f" %
                      (split, ix + 1, len(items), d_hits / (ix + 1)), flush=True)
        margins.sort()
        med = margins[len(margins) // 2] if margins else 0.0
        smp_rows = [r["sampled_maj"] for r in rows if r["sampled_maj"] is not None]
        summ = {"n": len(items), "d_acc": d_hits / max(1, len(items)),
                "c_rate": (c_hits / c_n) if c_n else None, "c_n": c_n,
                "margin_median": med,
                "margin_frac_pos": sum(1 for m in margins if m > 0) / max(1, len(margins)),
                "sampled_maj_acc": (sum(smp_rows) / len(smp_rows)) if smp_rows else None}
        res["splits"][split] = {"summary": summ, "rows": rows}
        # verdict numerics INLINE (convergence evaluate-py-1: never tail-truncatable)
        print("  xbind %s  arm=%s  D-acc=%.4f  C-rate=%s  margin_med=%.3f  "
              "margin_pos=%.3f  sampled=%s  n=%d" %
              (split, arm, summ["d_acc"], str(summ["c_rate"]), med,
               summ["margin_frac_pos"], str(summ["sampled_maj_acc"]), summ["n"]),
              flush=True)
    json.dump(res, open(out_path, "w"), ensure_ascii=False)
    print(json.dumps({"out": out_path,
                      "heldout_d_acc": res["splits"]["heldout"]["summary"]["d_acc"],
                      "seen_d_acc": res["splits"]["seen"]["summary"]["d_acc"]}))
    return 0
