#!/usr/bin/env python3
"""H_9128 TERMINAL — canonical gen=40 x multiseed G1 gate + form-priming probe.

Reference-matched to cli/evaluate.py eval_rho_weave (the FROZEN G1 gate) — same
_g_coverage, same kwr>=0.5 coherence, same 'best_distinct>=2 AND >max_single AND
coherent' clause. The ONLY parametrization is the RNG base_seed (canonical uses 7;
we sweep {7,107,207} for seed-robustness) and gen is pinned to canonical 40. No bar
moved (c9/p7): this is the pre-registered terminal (canonical+shuffle-bind+multiseed).

Applied to 3 arms (HI / LO / SHUF) it yields the bind-destruction margin:
  bd(HI) - bd(SHUF) <= 0  OR  form-priming self-pair ties  ->  coverage = form-artifact.
  bd(HI) > bd(SHUF), seed-robust                            ->  the one surviving crack.

usage: terminal_eval.py <ckpt> --label HI --gen 40 --seeds 7,107,207 --json out.json
"""
import os, sys, json

_HERE = os.path.dirname(os.path.abspath(__file__))
# resolve the bundle cli/ + core/ (pod layout: <root>/cli, <root>/core)
for cand in (os.path.join(_HERE, "cli"), os.path.join(_HERE, "core"),
             os.path.join(_HERE, "..", "..", "cli"), os.path.join(_HERE, "..", "..", "core")):
    if os.path.isdir(cand):
        sys.path.insert(0, os.path.abspath(cand))
# allow ANIMA_SRC override (pod bundle root)
_src = os.environ.get("ANIMA_SRC")
if _src:
    sys.path.insert(0, os.path.join(_src, "cli"))
    sys.path.insert(0, os.path.join(_src, "core"))

import evaluate as EV

TOP_K = 40
TEMP = 0.7


def g1_at_seed(mouth, cz, known, gen, base_seed):
    """eval_rho_weave VERBATIM logic, base_seed-parametrized, gen-pinned."""
    n = len(cz)
    g_single = gen if (0 < gen < 80) else 80
    g_comp = gen if (0 < gen < 120) else 120
    max_single = 0
    single_cov = []
    for s in range(n):
        o = mouth.ideate(cz[s] + ". ", g_single, TOP_K, TEMP, base_seed + 1 + s)
        cov = EV._g_coverage(o)
        single_cov.append(cov)
        if cov > max_single:
            max_single = cov
    ks = []
    passed = False
    best_distinct = 0
    best_k = 0
    for k in range(2, n + 1):
        seed = ". ".join(cz[c] for c in range(k)) + ". "
        o = mouth.ideate(seed, g_comp, TOP_K, TEMP, base_seed)
        cov = EV._g_coverage(o)
        kwr = EV._rho_fan_known_word_ratio(o, known)
        coherent = kwr >= 0.5
        clears = cov >= 2 and cov > max_single and coherent
        ks.append({"k": k, "distinct": cov, "kwr": round(kwr, 4),
                   "coherent": coherent, "clears": clears})
        if clears:
            passed = True
        if cov > best_distinct:
            best_distinct = cov
            best_k = k
    return {"base_seed": base_seed, "max_single": max_single, "single_cov": single_cov,
            "best_distinct": best_distinct, "best_k": best_k, "pass": bool(passed), "ks": ks}


def form_priming(mouth, cz, known, gen, base_seed):
    """Self-pair probe: seed the SAME concept twice. A genuine composer covers 1 family
    (bd=1); a template/seed-copy form-primer may hallucinate a 2nd family slot (bd>=2).
    If self-pair bd ~ real-pair bd, the bd signal is FORM, not binding."""
    g_comp = gen if (0 < gen < 120) else 120
    out = []
    for i in range(len(cz)):
        seed = cz[i] + ". " + cz[i] + ". "
        o = mouth.ideate(seed, g_comp, TOP_K, TEMP, base_seed)
        cov = EV._g_coverage(o)
        kwr = EV._rho_fan_known_word_ratio(o, known)
        out.append({"i": i, "self_bd": cov, "kwr": round(kwr, 4), "coherent": kwr >= 0.5})
    return {"base_seed": base_seed, "self_pair_bd_max": max(r["self_bd"] for r in out),
            "rows": out}


def main():
    ckpt = sys.argv[1]
    label = "?"
    gen = 40
    seeds = [7, 107, 207]
    jout = None
    i = 2
    while i < len(sys.argv):
        a = sys.argv[i]
        if a == "--label": label = sys.argv[i + 1]; i += 2
        elif a == "--gen": gen = int(sys.argv[i + 1]); i += 2
        elif a == "--seeds": seeds = [int(x) for x in sys.argv[i + 1].split(",")]; i += 2
        elif a == "--json": jout = sys.argv[i + 1]; i += 2
        else: i += 1

    known = EV._rho_fan_dict_load()
    cz = EV._rho_fan_concepts()
    mouth = EV._Mouth(ckpt)

    per_seed = [g1_at_seed(mouth, cz, known, gen, s) for s in seeds]
    fp = [form_priming(mouth, cz, known, gen, s) for s in seeds]

    bds = sorted(r["best_distinct"] for r in per_seed)
    med = bds[len(bds) // 2]
    n_pass = sum(1 for r in per_seed if r["pass"])
    out = {
        "ckpt": ckpt, "label": label, "gen": gen, "seeds": seeds,
        "per_seed_g1": per_seed,
        "form_priming": fp,
        "summary": {
            "best_distinct_by_seed": [r["best_distinct"] for r in per_seed],
            "max_single_by_seed": [r["max_single"] for r in per_seed],
            "median_best_distinct": med,
            "n_pass": n_pass, "n_seeds": len(seeds),
            "self_pair_bd_max_by_seed": [r["self_pair_bd_max"] for r in fp],
        },
    }
    js = json.dumps(out, indent=1)
    print(js)
    if jout:
        with open(jout, "w") as f:
            f.write(js)
    sm = out["summary"]
    print(f"\n[{label}] gen={gen} bd_by_seed={sm['best_distinct_by_seed']} "
          f"ms_by_seed={sm['max_single_by_seed']} median_bd={sm['median_best_distinct']} "
          f"n_pass={sm['n_pass']}/{sm['n_seeds']} self_pair_bd={sm['self_pair_bd_max_by_seed']}")


if __name__ == "__main__":
    main()
