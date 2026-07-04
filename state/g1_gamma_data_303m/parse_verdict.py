#!/usr/bin/env python3
"""Parse the 6 (2-arm x 3-seed) engine-native eval txts + base into the H_9127 verdict."""
import re, sys, glob, os

def parse(path):
    if not os.path.exists(path):
        return None
    t = open(path, errors="replace").read()
    g0 = re.search(r"G0 COHERENCE\s+(\S+)\s+kwr>=0\.50 on (\d+)/5", t)
    g1 = re.search(r"G1 RECOMBINATION\s+(\S+)\s+best_distinct=(\d+)\s+>\s+max_single=(\d+)", t)
    if not g1:
        return {"file": path, "parse": "FAIL", "tail": t[-400:]}
    return {"file": path,
            "g0_pass": g0.group(1) if g0 else "?",
            "g0_coherent": int(g0.group(2)) if g0 else -1,
            "g1_pass": g1.group(1),
            "best_distinct": int(g1.group(2)),
            "max_single": int(g1.group(3))}

def main(wd):
    print("=== H_9127 gamma-DATA-channel — engine-native G1 verdict ===\n")
    base = parse(os.path.join(wd, "base_eval.txt"))
    print("BASE h1129:", base, "\n")
    res = {"gamma": {}, "add": {}}
    for seed in (7, 4302, 4303):
        for arm in ("gamma", "add"):
            r = parse(os.path.join(wd, f"{arm}_s{seed}_eval.txt"))
            res[arm][seed] = r
            print(f"{arm}_s{seed}:", r)
    print()
    # frozen bar: GAMMA best_distinct>=2 AND >max_single AND >ADD AND G0>=4 coherent
    votes = []
    for seed in (7, 4302, 4303):
        g = res["gamma"].get(seed); a = res["add"].get(seed)
        if not g or not a or "best_distinct" not in g or "best_distinct" not in a:
            votes.append(("seed%d" % seed, "MISSING")); continue
        gb, gm, gc = g["best_distinct"], g["max_single"], g.get("g0_coherent", -1)
        ab = a["best_distinct"]
        green = (gb >= 2) and (gb > gm) and (gb > ab) and (gc >= 4)
        votes.append((f"seed{seed}", f"GAMMA bd={gb} ms={gm} g0={gc}/5 | ADD bd={ab} -> "
                                     f"{'GREEN' if green else 'no-lift'}", green))
    print("PER-SEED:")
    for v in votes:
        print("  ", v)
    greens = sum(1 for v in votes if len(v) == 3 and v[2])
    print(f"\nGREEN seeds: {greens}/3  -> majority {'YES (VERDICT 🟢)' if greens>=2 else 'NO'}")

if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else ".")
