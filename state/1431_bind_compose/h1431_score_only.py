#!/usr/bin/env python3
"""h1431_score_only.py — PHASE 2 of the decode⊥score split. Reads the persisted
fragments.jsonl (from h1431_decode_only.py) and runs the FROZEN H_1305 scoring VERBATIM
(P.score_from_fragments + shuffle control + P.score_ablate_from_fragments), per seed,
exactly as the original h1431_engine_native.main(). torch loads here but NO 303M decode
co-resides → ~2GB, no swap. Writes engine_native_result.json + prints the 5-bar summary.
"""
import os, sys, json, importlib.util
HERE = os.path.dirname(os.path.abspath(__file__))
FRAGS = os.path.join(HERE, "fragments.jsonl")

def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
P = _load("h1431", os.path.join(HERE, "h1431_bind_compose.py"))

# read persisted fragments → {seed: {"rel":[...by subj...], "meas":[...]}}
recs = [json.loads(l) for l in open(FRAGS) if l.strip()]
seeds = sorted({r["seed"] for r in recs}, key=lambda s: [7,4302,4303].index(s) if s in [7,4302,4303] else s)
# subject order = frozen SUBJECTS intersected with what's present
SUBJ_ORDER = ["consciousness","tension","memory","silence","dreaming"]
subjs = [s for s in SUBJ_ORDER if any(r["subj"]==s for r in recs)]
P.SUBJECTS = subjs   # scope the scorers to present subjects

def frags_for(seed, kind):
    by = {r["subj"]: r["text"] for r in recs if r["seed"]==seed and r["kind"]==kind}
    return [by[s] for s in subjs]

rows = []
for seed in seeds:
    rel  = frags_for(seed, "rel")
    meas = frags_for(seed, "meas")
    for i, subj in enumerate(subjs):
        print(f"  [seed {seed}] {subj}: REL={rel[i]!r}  MEAS={meas[i]!r}", flush=True)
    compose = P.score_from_fragments(rel, meas, shuffle=False)
    shuffle = P.score_from_fragments(rel, meas, shuffle=True, rng_seed=seed)
    ablate  = P.score_ablate_from_fragments(rel)
    rows.append({"seed": seed,
                 "compose": {"fals": compose["fals"], "dist": compose["dist"]},
                 "shuffle": {"fals": shuffle["fals"], "dist": shuffle["dist"]},
                 "ablate":  {"fals": ablate["fals"],  "dist": ablate["dist"]},
                 "claims": compose["claims"]})
    print(f"  [seed {seed}] COMPOSE fals={compose['fals']} dist={compose['dist']} | "
          f"SHUFFLE fals={shuffle['fals']} dist={shuffle['dist']} | "
          f"ABLATE fals={ablate['fals']} dist={ablate['dist']}", flush=True)
    for c in compose["claims"]:
        print(f"      claim: {c!r}", flush=True)
n = len(rows)
mean = lambda arm,k: sum(r[arm][k] for r in rows)/n if n else 0.0
print("\n==== ENGINE-NATIVE H_1431 (FROZEN 5-bar, decode⊥score) ====", flush=True)
print(f"  COMPOSE   FALS={mean('compose','fals'):.4f}  DIST={mean('compose','dist'):.4f}", flush=True)
print(f"  SHUFFLE   FALS={mean('shuffle','fals'):.4f}  DIST={mean('shuffle','dist'):.4f}", flush=True)
print(f"  ABLATE    FALS={mean('ablate','fals'):.4f}  DIST={mean('ablate','dist'):.4f}", flush=True)
print(f"  (NSUBJ={len(subjs)} NSEED={len(seeds)}; frozen FREEZE = 5/3/110)", flush=True)
json.dump({"scope":{"nsubj":len(subjs),"nseed":len(seeds)},"rows":rows},
          open(os.path.join(HERE, "engine_native_result.json"), "w"), indent=2)
print("SCORE_ONLY_DONE", flush=True)
