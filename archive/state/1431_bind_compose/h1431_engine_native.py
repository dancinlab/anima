#!/usr/bin/env python3
"""h1431_engine_native.py — ENGINE-NATIVE re-measure of H_1431 (a_engine_native_learning).

Swaps ONLY the mouth: torch gauge_lib._decode -> the byte-faithful hexa engine
bytegpt_decode_topk_sampled (via state/1431_bind_compose/engine_decode_cli.hexa). ALL scoring
(frozen H_1305 _is_falsifiable, COMPARATOR/MEASURABLE extraction, _weld, the 5 bars, the
cross-pair shuffle control) is IMPORTED VERBATIM from the original torch probe
h1431_bind_compose.py — NOT redefined. The engine uses its OWN xorshift32 seeded top-k
sampler (torch.multinomial is not hexa-reproducible), so this is a genuine INDEPENDENT
engine measurement on the faithful forward, not a byte-replica of the torch samples.

SCOPE (env): H1431_NSUBJ (default 2), H1431_NSEED (default 1), H1431_MAXNEW (default 110),
H1431_BIN (serialized weights). The 102s/forward dispatch-runtime wall makes the full FREEZE
(5 subj x 3 seed x 110) ~90h; scope down for a feasible engine-native pilot and report it
honestly as a pilot (NOT the frozen 5-bar) unless run at full scope.
"""
import os, sys, json, subprocess, importlib.util

HERE = os.path.dirname(os.path.abspath(__file__))
ANIMA = os.path.dirname(os.path.dirname(HERE))
BIN = os.environ.get("H1431_BIN", "/tmp/parity-verify/chat_full.bin")
HEXA = os.path.expanduser("~/.hx/bin/hexa")
CLI = os.path.join(HERE, "engine_decode_cli.hexa")
NSUBJ = int(os.environ.get("H1431_NSUBJ", "2"))
NSEED = int(os.environ.get("H1431_NSEED", "1"))
MAXNEW = int(os.environ.get("H1431_MAXNEW", "110"))
TOP_K, TEMP = 40, 0.7

# import the original probe VERBATIM (reuse its scoring; do NOT redefine)
def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    return mod
P = _load("h1431", os.path.join(HERE, "h1431_bind_compose.py"))

SUBJECTS = P.SUBJECTS[:NSUBJ]
SEEDS = P.SEEDS[:NSEED]

def engine_decode(seed_text, seed_rng):
    """Engine-native replacement for gauge_lib._decode — shells the hexa CLI."""
    cmd = [HEXA, "run", CLI, BIN, str(MAXNEW), str(TOP_K), str(int(TEMP*1000)), str(seed_rng), seed_text]
    env = dict(os.environ); env["HEXA_MEM_UNLIMITED"] = "1"
    out = subprocess.run(cmd, capture_output=True, text=True, env=env, timeout=36000).stdout
    for line in out.splitlines():
        if line.startswith("ENGINE_DECODE "):
            return line[len("ENGINE_DECODE "):].strip()
    return ""

def decode_fragments_engine(seed_rng):
    rel, meas = [], []
    for subj in SUBJECTS:
        rel.append(engine_decode(P._relation_seed(subj), seed_rng))
        meas.append(engine_decode(P._measure_seed(subj), seed_rng))
    return rel, meas

def main():
    # monkeypatch the probe's SUBJECTS to the scoped slice so its scorers use the slice
    P.SUBJECTS = SUBJECTS
    print(f"[engine-native H_1431] BIN={BIN} NSUBJ={NSUBJ} NSEED={NSEED} MAXNEW={MAXNEW}", flush=True)
    rows = []
    for s_i, seed_rng in enumerate(SEEDS):
        rel, meas = decode_fragments_engine(seed_rng)
        for i, subj in enumerate(SUBJECTS):
            print(f"  [seed {seed_rng}] {subj}: REL={rel[i]!r}  MEAS={meas[i]!r}", flush=True)
        compose = P.score_from_fragments(rel, meas, shuffle=False)
        shuffle = P.score_from_fragments(rel, meas, shuffle=True, rng_seed=seed_rng)
        ablate  = P.score_ablate_from_fragments(rel)
        rows.append({"seed": seed_rng,
                     "compose": {"fals": compose["fals"], "dist": compose["dist"]},
                     "shuffle": {"fals": shuffle["fals"], "dist": shuffle["dist"]},
                     "ablate":  {"fals": ablate["fals"],  "dist": ablate["dist"]},
                     "claims": compose["claims"]})
        print(f"  [seed {seed_rng}] COMPOSE fals={compose['fals']} dist={compose['dist']} | "
              f"SHUFFLE fals={shuffle['fals']} dist={shuffle['dist']} | "
              f"ABLATE fals={ablate['fals']} dist={ablate['dist']}", flush=True)
        for c in compose["claims"]:
            print(f"      claim: {c!r}", flush=True)
    n = len(rows)
    mean = lambda arm,k: sum(r[arm][k] for r in rows)/n
    print("\n==== ENGINE-NATIVE H_1431 (scoped pilot) ====", flush=True)
    print(f"  COMPOSE   FALS={mean('compose','fals'):.4f}  DIST={mean('compose','dist'):.4f}", flush=True)
    print(f"  SHUFFLE   FALS={mean('shuffle','fals'):.4f}  DIST={mean('shuffle','dist'):.4f}", flush=True)
    print(f"  ABLATE    FALS={mean('ablate','fals'):.4f}  DIST={mean('ablate','dist'):.4f}", flush=True)
    print(f"  (scope NSUBJ={NSUBJ} NSEED={NSEED} MAXNEW={MAXNEW}; full FREEZE = 5/3/110)", flush=True)
    json.dump({"scope":{"nsubj":NSUBJ,"nseed":NSEED,"maxnew":MAXNEW},"rows":rows},
              open(os.path.join(HERE, "engine_native_result.json"), "w"), indent=2)
    print("ENGINE_NATIVE_DONE", flush=True)

if __name__ == "__main__":
    main()
