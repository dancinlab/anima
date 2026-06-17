#!/usr/bin/env python3
"""h1431_decode_only.py — PHASE 1 of the decode⊥score split (Lane C, per team-lead plan).
Decodes ALL H_1431 fragments (303M, ~18GB peak via the ranged CLI, NO torch co-resident),
persists each to fragments.jsonl durably as it goes (commit-early: a mid-run OOM/reboot keeps
the fragments already decoded). Phase 2 (h1431_score_only.py) scores the persisted JSONL with
torch but NO 303M, so the 24GB+2GB co-residence swap never happens.

Seeds/scope are the FROZEN H_1431 values (mirrored here verbatim to avoid importing the
torch-loaded h1431_bind_compose during decode): SUBJECTS, SEEDS, MAX_NEW, TOP_K, TEMP.
"""
import os, sys, json, subprocess

HERE   = os.path.dirname(os.path.abspath(__file__))
BIN    = os.environ["H1431_BIN"]
HEXA   = os.path.expanduser("~/.hx/bin/hexa")
CLI    = os.path.join(HERE, "engine_decode_cli_ranged.hexa")
OUT    = os.path.join(HERE, "fragments.jsonl")

# FROZEN H_1431 (h1431_bind_compose.py verbatim)
SUBJECTS = ["consciousness", "tension", "memory", "silence", "dreaming"]
SEEDS    = [7, 4302, 4303]
MAX_NEW  = int(os.environ.get("H1431_MAXNEW", "110"))
NSUBJ    = int(os.environ.get("H1431_NSUBJ", str(len(SUBJECTS))))
NSEED    = int(os.environ.get("H1431_NSEED", str(len(SEEDS))))
TOP_K, TEMP = 40, 0.7
SUBJECTS = SUBJECTS[:NSUBJ]; SEEDS = SEEDS[:NSEED]

def _relation_seed(s): return f"a relationship about {s}: it tends to be "
def _measure_seed(s):  return f"something we could observe about {s}: the "

def decode(seed_text, seed_rng):
    cmd = [HEXA, "run", CLI, BIN, str(MAX_NEW), str(TOP_K), str(int(TEMP*1000)), str(seed_rng), seed_text]
    env = dict(os.environ); env["HEXA_MEM_UNLIMITED"] = "1"
    out = subprocess.run(cmd, capture_output=True, text=True, env=env, timeout=36000).stdout
    for line in out.splitlines():
        if line.startswith("ENGINE_DECODE "):
            return line[len("ENGINE_DECODE "):].strip()
    return ""

def main():
    # resume: skip fragments already persisted
    done = set()
    if os.path.exists(OUT):
        for ln in open(OUT):
            try: r = json.loads(ln); done.add((r["seed"], r["subj"], r["kind"]))
            except: pass
    print(f"[decode-only] BIN={BIN} NSUBJ={len(SUBJECTS)} NSEED={len(SEEDS)} MAXNEW={MAX_NEW} resume={len(done)}", flush=True)
    f = open(OUT, "a")
    total = len(SEEDS)*len(SUBJECTS)*2; n = 0
    for seed_rng in SEEDS:
        for subj in SUBJECTS:
            for kind, seedfn in (("rel", _relation_seed), ("meas", _measure_seed)):
                n += 1
                if (seed_rng, subj, kind) in done:
                    print(f"  [{n}/{total}] skip {seed_rng}/{subj}/{kind} (already done)", flush=True); continue
                txt = decode(seedfn(subj), seed_rng)
                rec = {"seed": seed_rng, "subj": subj, "kind": kind, "text": txt}
                f.write(json.dumps(rec)+"\n"); f.flush(); os.fsync(f.fileno())
                print(f"  [{n}/{total}] {seed_rng}/{subj}/{kind}: {txt!r}", flush=True)
    f.close()
    print("DECODE_ONLY_DONE", flush=True)

if __name__ == "__main__":
    main()
