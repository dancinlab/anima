#!/usr/bin/env python3
"""5-seed engine-native G1 mouth-generation score for the A11 TPR .clm.

Torch-free (imports cli/evaluate.py, which imports core/decode.py — both numpy).
Replicates the FROZEN g_eval_g1 bar per seed with a decorrelating seed offset,
plus a SCRAMBLE control (char-shuffled composed seed must NOT reach coverage):
  HIT(seed) iff best_distinct>=2 AND best_distinct>max_single AND coherent AND scramble<=1.
Verdict: >=4/5 HIT -> PREDICTIVE-ESCAPED (H_9120 flip) ; <4/5 -> FALSIFIED-CEILING.
"""
import sys, os, json, random
_REPO = sys.argv[2]
sys.path.insert(0, os.path.join(_REPO, "core"))
sys.path.insert(0, os.path.join(_REPO, "cli"))
import evaluate as EV

clm = sys.argv[1]
json_out = sys.argv[3] if len(sys.argv) > 3 else None
GEN = 40
mouth = EV._Mouth(clm)
known = EV._g6_dict_load()
cz = EV._g6_concepts()
n = len(cz)
print(f"=== A11 TPR .clm 5-seed G1 (engine-native --py numpy) | concepts={n} gen={GEN} ===", flush=True)


def one_seed(base):
    g_single = GEN if 0 < GEN < 80 else 80
    g_comp = GEN if 0 < GEN < 120 else 120
    max_single = 0
    for s in range(n):
        o = mouth.ideate(cz[s] + ". ", g_single, 40, 0.7, base + s)
        max_single = max(max_single, EV._g_coverage(o))
    best_distinct = 0; best_coherent = False; best_seed_str = ""
    for k in range(2, n + 1):
        seed = ". ".join(cz[:k]) + ". "
        o = mouth.ideate(seed, g_comp, 40, 0.7, base)
        cov = EV._g_coverage(o)
        coh = EV._g6_known_word_ratio(o, known) >= 0.5
        if cov > best_distinct:
            best_distinct, best_coherent, best_seed_str = cov, coh, seed
    # SCRAMBLE control: char-shuffle the best composed seed
    rnd = random.Random(base + 7919)
    chars = list(best_seed_str); rnd.shuffle(chars)
    o_scr = mouth.ideate("".join(chars), g_comp, 40, 0.7, base + 313)
    scr = EV._g_coverage(o_scr)
    hit = (best_distinct >= 2 and best_distinct > max_single and best_coherent and scr <= 1)
    return dict(base=base, max_single=max_single, best_distinct=best_distinct,
                coherent=best_coherent, scramble=scr, hit=hit)


rows = []
for i in range(5):
    r = one_seed(7 + 1000 * i)
    rows.append(r)
    print(f"  seed#{i} base={r['base']}: best_distinct={r['best_distinct']} "
          f"max_single={r['max_single']} coherent={r['coherent']} scramble={r['scramble']} "
          f"-> {'HIT' if r['hit'] else 'floor'}", flush=True)

hits = sum(r["hit"] for r in rows)
verdict = "PREDICTIVE-ESCAPED" if hits >= 4 else "FALSIFIED-CEILING"
flip = hits >= 4
print(f"\n=== G1 5-seed: HIT {hits}/5 -> {verdict} (H_9120 terminal_flip={flip}) ===", flush=True)
out = dict(clm=clm, gen=GEN, concepts=n, hits=hits, rows=rows, verdict=verdict,
           terminal_flip=flip, bar="best_distinct>=2 AND >max_single AND coherent AND scramble<=1")
print("JSON " + json.dumps({k: out[k] for k in ("hits", "verdict", "terminal_flip")}))
if json_out:
    json.dump(out, open(json_out, "w"), indent=2)
