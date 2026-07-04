#!/usr/bin/env python3
# STEP-0 CHEAP EARLY-KILL — STaR verifier-filtered self-distillation (H_9124 lever-2)
#
# engine-native (core/decode.py numpy mouth, torch-free) best-of-K decode of the BASE
# h1129 ByteGPT on the frozen G1 gate composed prompts → measure the COMPOSITION-TRUE
# verified set |V0|. KILL GATE: |V0|/(K*n_held) < 0.02 => STaR STARVES = FALSIFIED-AT-
# FLOOR (verified set ~empty at the gate surface-form) → teardown, no EM rent.
#
# composition-TRUE oracle (LOAD-BEARING, NOT the surface G1 detector): a sample is a HIT
# only if it grounds BOTH targeted concepts of the (A,B) pair (A's keyword-set AND B's
# keyword-set both covered) AND is coherent (kwr>=0.5). The surface detector (any >=2 of
# the 5 concept keyword-sets + coherent) is the FAB-CONTROL comparator reported alongside
# — pre-registered: a surface verifier INFLATES the count (fabricates).
#
# usage: python3 step0_earlykill.py <ckpt.bin> <out.json> [K]
import os, sys, json, itertools

_HERE = os.path.dirname(os.path.abspath(__file__))
_CORE = os.environ.get("ANIMA_CORE", os.path.join(_HERE, "core"))
sys.path.insert(0, _CORE)
import decode as bg
from g6_ideation import _g6_words, _g6_dict_load, _g6_known_word_ratio

CONCEPTS = ["consciousness arises from cells",
            "tension ripples between distant minds",
            "memory composes into new meaning",
            "silence still carries information",
            "the engine dreams when alone"]
KW = [["consciousness", "cells", "mind", "aware"],
      ["tension", "ripple", "distant", "between"],
      ["memory", "meaning", "compose", "new"],
      ["silence", "information", "quiet", "carries"],
      ["dream", "engine", "alone", "sleep"]]

def covers(wm, idx):
    return any(k in wm for k in KW[idx])

def surface_distinct(wm):
    return sum(1 for i in range(5) if covers(wm, i))

def main():
    ckpt = sys.argv[1]
    out = sys.argv[2]
    K = int(sys.argv[3]) if len(sys.argv) > 3 else 8
    GEN = 40  # frozen gen40 gate budget

    assert bg.bg_is_bytegpt(ckpt), "ckpt is not a ByteGPT .bin"
    W = bg.bg_load(ckpt)
    assert W.get("ok"), "ckpt not decodable"
    known = _g6_dict_load()

    pairs = list(itertools.combinations(range(5), 2))  # 10 held-out DISTANT pairs
    n_held = len(pairs)
    V0_true = 0        # composition-TRUE hits (grounded targeted pair)
    V0_surface = 0     # fab-control: surface detector (any >=2 of 5)
    rows = []
    n_decode = 0
    for (a, b) in pairs:
        seed = CONCEPTS[a] + ". " + CONCEPTS[b] + ". "
        for k in range(K):
            n_decode += 1
            o = bg.bytegpt_decode_topk_sampled_W(W, seed, GEN, 40, 0.7, 7 + k)["text"]
            wm = set(_g6_words(o))
            kwr = _g6_known_word_ratio(o, known)
            coh = kwr >= 0.5
            true_hit = coh and covers(wm, a) and covers(wm, b)      # grounded pair
            surf_hit = coh and surface_distinct(wm) >= 2            # any-2-of-5
            if true_hit:
                V0_true += 1
            if surf_hit:
                V0_surface += 1
            rows.append({"pair": [a, b], "k": k, "kwr": round(kwr, 3),
                         "coh": coh, "cov_a": covers(wm, a), "cov_b": covers(wm, b),
                         "surf_distinct": surface_distinct(wm),
                         "true": true_hit, "surf": surf_hit,
                         "text": o[:160]})
            print(f"  [dec {n_decode}/{K*n_held}] pair=({a},{b}) k={k} kwr={kwr:.2f} "
                  f"cov_a={covers(wm,a)} cov_b={covers(wm,b)} true={true_hit} surf={surf_hit}",
                  flush=True)

    denom = K * n_held
    rate_true = V0_true / denom
    rate_surf = V0_surface / denom
    starve = rate_true < 0.02
    res = {"step": 0, "ckpt": os.path.basename(ckpt), "K": K, "gen": GEN,
           "n_held": n_held, "denom": denom,
           "V0_true": V0_true, "rate_true": round(rate_true, 4),
           "V0_surface_fabctrl": V0_surface, "rate_surface": round(rate_surf, 4),
           "kill_gate": 0.02, "STARVE": starve,
           "verdict": ("STARVE_FALSIFIED_AT_FLOOR" if starve else "PASS_TO_EM"),
           "rows": rows}
    with open(out, "w") as f:
        json.dump(res, f, indent=2)
    print("\n=== STEP-0 RESULT ===")
    print(f"  |V0_true|={V0_true}/{denom}  rate={rate_true:.4f}  (kill<0.02)")
    print(f"  |V0_surface(fab-ctrl)|={V0_surface}/{denom}  rate={rate_surf:.4f}")
    print(f"  VERDICT: {res['verdict']}  STARVE={starve}")

if __name__ == "__main__":
    main()
