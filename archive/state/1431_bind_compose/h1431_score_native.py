#!/usr/bin/env python3
"""h1431_score_native.py — PHASE 2 (ENGINE-NATIVE scoring).

Scores the ENGINE-NATIVE fragments (batch_out.tsv, decoded by CORE/bytegpt_decode.hexa
via engine_decode_batch_cli.hexa — NOT a torch mouth) with the FROZEN H_1305 detector,
reusing h1431_bind_compose.score_from_fragments / score_ablate_from_fragments VERBATIM
(p7: detector imported, NOT redefined). The torch import inside h1431_bind_compose is for
the decode path only (decode_fragments) which we DO NOT call — we feed our .hexa fragments.

This makes the COMPOSE/SHUFFLE/ABLATE 5-bar ENGINE-NATIVE (a_engine_native_learning):
decode = live .hexa CORE, score = frozen detector. Contrast: the prior torch run decoded
WITH gauge_lib._decode (torch mouth) → DIRECTIONAL only.
"""
import os, sys, importlib.util, re, glob

HERE = os.path.dirname(os.path.abspath(__file__))
# engine-native shard outputs: launch2 (out_jp_00..09, 30 jobs) + relaunch (outr_*, 2 missing).
# A decode fragment can span MULTIPLE lines (the byte-LM emits raw newlines); a continuation
# line (no tag prefix) is welded back onto its fragment. Duplicate tags keep the FIRST.
INPUTS = sorted(glob.glob("/tmp/out_jp_0[0-9]")) + sorted(glob.glob("/tmp/outr_*"))
TAG_RE = re.compile(r'^(\d+)\|([a-z]+)\|(rel|meas)\t(.*)$')

spec = importlib.util.spec_from_file_location("h1431", os.path.join(HERE, "h1431_bind_compose.py"))
H = importlib.util.module_from_spec(spec)
spec.loader.exec_module(H)

frags = {}
for fn in INPUTS:
    cur = None
    with open(fn, errors="replace") as f:
        for ln in f:
            m = TAG_RE.match(ln)
            if m:
                seed, subj, kind, txt = m.groups()
                key = (int(seed), subj, kind)
                if key not in frags:
                    frags[key] = txt
                    cur = key
                else:
                    cur = None  # duplicate tag → skip (keep first); its continuations too
            elif cur is not None:
                frags[cur] += " " + ln.rstrip("\n")

print(f"[score-native] parsed {len(frags)} fragments from {len(INPUTS)} shard files", flush=True)
print(f"[score-native] SEEDS={H.SEEDS} SUBJECTS={H.SUBJECTS}", flush=True)

arms = {"COMPOSE": [], "SHUFFLE_BIND": [], "ABLATE": []}
missing = 0
for seed in H.SEEDS:
    rel = []
    meas = []
    for s in H.SUBJECTS:
        r = frags.get((seed, s, "rel"), "")
        m = frags.get((seed, s, "meas"), "")
        if not r or not m:
            missing += 1
        rel.append(r)
        meas.append(m)
    rc = H.score_from_fragments(rel, meas, shuffle=False)
    rs = H.score_from_fragments(rel, meas, shuffle=True, rng_seed=seed)
    ra = H.score_ablate_from_fragments(rel)
    arms["COMPOSE"].append(rc)
    arms["SHUFFLE_BIND"].append(rs)
    arms["ABLATE"].append(ra)
    print(f"  seed {seed}: COMPOSE fals={rc['fals']}/{H.N_IDEAS} dist={rc['dist']} coh={rc['coherent']} "
          f"| SHUF fals={rs['fals']} | ABL fals={ra['fals']}", flush=True)

def mean(a, k):
    return round(sum(r[k] for r in arms[a]) / len(arms[a]), 4)

print("\n=== H_1431 5-BAR ENGINE-NATIVE (decode=.hexa CORE/bytegpt_decode, score=frozen H_1305) ===", flush=True)
print(f"COMPOSE  fals={mean('COMPOSE','fals')}  dist={mean('COMPOSE','dist')}  coh={mean('COMPOSE','coherent')}", flush=True)
print(f"SHUFFLE  fals={mean('SHUFFLE_BIND','fals')}", flush=True)
print(f"ABLATE   fals={mean('ABLATE','fals')}", flush=True)
print(f"missing_fragments={missing}", flush=True)
print("\n(torch DIRECTIONAL baseline was COMPOSE=0.3333 SHUF=0 ABL=0 → 🧱 BIND-CAPACITY-BOUND)", flush=True)
print("SCORE_NATIVE_DONE", flush=True)
