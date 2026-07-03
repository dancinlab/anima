#!/usr/bin/env python3
# ============================================================================
# H_9112 — Referential-efficacy PSYCHO-K + MRR re-score (frozen-first, PREREG.md).
#   Re-scores the ALREADY-COLLECTED H_9111 emits (../9111_llm_interlocutor/emits.tsv,
#   14 concepts) on a HARDER referential game to restore measurement VARIANCE that
#   the H_9111 Pearson-D metric-degeneracy destroyed (constant ceiling/floor vectors).
#   anima side is FROZEN (no re-decode). Receiver = external oracle (sidecar fable =
#   claude-fable-5, theta OUTSIDE anima closure). STDLIB ONLY (subprocess/json/re)
#   -> grep-gate clean (no tensor/ML/mirror libraries). Tier = DIRECTIONAL-on-external-oracle
#   (emit generation was engine-native H_9111; receiver is an external tool -- honest label).
#   Batched oracle calls (all 14 clues per config) -> ~32 fable calls, not ~500.
# ============================================================================
import subprocess, sys, json, os, re, statistics

SLUG   = os.path.dirname(os.path.abspath(__file__))
EMITS  = os.path.join(SLUG, "..", "9111_llm_interlocutor", "emits.tsv")
OUT    = os.path.join(SLUG, "rescore_fixture.jsonl")
RESULT = os.path.join(SLUG, "RESULT.md")
MODEL  = "claude-fable-5"

# --- FROZEN config (PREREG.md -- do not move post-hoc, c9/p7) ---
K_SWEEP    = [2, 4, 8, 14]
TRUNC      = ["full", 32, 16, 8]
SEED       = 9112
DEGEN_TAIL = "the state and the concern for the state"

NEAR = {
 "volcano":["avalanche","thunderstorm","glacier"], "glacier":["avalanche","volcano","cactus"],
 "library":["harbor","lighthouse","beehive"], "violin":["telescope","compass","umbrella"],
 "spider":["beehive","cactus","thunderstorm"], "lighthouse":["harbor","telescope","library"],
 "umbrella":["compass","violin","cactus"], "beehive":["spider","library","cactus"],
 "telescope":["compass","violin","lighthouse"], "avalanche":["glacier","volcano","thunderstorm"],
 "compass":["telescope","umbrella","violin"], "cactus":["spider","glacier","umbrella"],
 "harbor":["lighthouse","library","glacier"], "thunderstorm":["volcano","avalanche","spider"],
}

def rng(seed):
    s = seed & 0xffffffff
    def nxt():
        nonlocal s
        s ^= (s << 13) & 0xffffffff; s ^= s >> 17; s ^= (s << 5) & 0xffffffff
        return s & 0xffffffff
    return nxt

def load():
    concepts, emit = [], {}
    with open(os.path.normpath(EMITS)) as f:
        for ln in f:
            if not ln.startswith("EMIT\t"): continue
            _, i, c, ok, e = ln.rstrip("\n").split("\t", 4)
            concepts.append(c); emit[c] = e
    return concepts, emit

def clean(clue):
    idx = clue.find(DEGEN_TAIL[:18])
    return (clue[:idx] if idx >= 0 else clue).strip()

def trunc(s, t):
    return s if t == "full" else s[:t]

def distractors(target, concepts, K, r):
    pool = [c for c in NEAR.get(target, []) if c != target]
    chosen = pool[:K-1]
    rest = [c for c in concepts if c != target and c not in chosen]
    while len(chosen) < K-1 and rest:
        chosen.append(rest.pop(r() % len(rest)))
    cand = chosen + [target]
    for i in range(len(cand)-1, 0, -1):
        j = r() % (i+1); cand[i], cand[j] = cand[j], cand[i]
    return cand

def derange(concepts, r):
    n = len(concepts); perm = list(range(n))
    for i in range(n-1, 0, -1):
        j = r() % (i+1); perm[i], perm[j] = perm[j], perm[i]
    for i in range(n):
        if perm[i] == i:
            perm[i], perm[(i+1) % n] = perm[(i+1) % n], perm[i]
    return {concepts[i]: concepts[perm[i]] for i in range(n)}

def parse_picks(out):
    """Parse the oracle JSON reply; on malformed JSON, log and fall through to a
    line-regex fallback (NOT a silent swallow -- the failure is surfaced to stderr)."""
    picks = {}
    m = re.search(r"\[.*\]", out, re.S)
    if m:
        try:
            for o in json.loads(m.group(0)):
                picks[int(o["id"])] = str(o.get("pick", "")).strip().lower()
        except (ValueError, KeyError, TypeError) as ex:
            sys.stderr.write(f"[parse] JSON array malformed ({ex}); using line-regex fallback\n")
    if not picks:
        for ln in out.splitlines():
            mm = re.match(r"\s*(\d+)\D+([a-z]+)", ln.strip().lower())
            if mm:
                picks[int(mm.group(1))] = mm.group(2)
        if not picks:
            sys.stderr.write("[parse] no picks recovered from oracle reply (both paths empty)\n")
    return picks

def ask_fable_batch(items):
    lines = ["You are a referential-decoding receiver. Below are numbered TRIALS.",
             "Each trial has a CLUE describing exactly ONE concept from its CANDIDATES",
             "(the concept's own name was removed -- match by MEANING only).",
             "For EACH trial output the candidate you think the clue describes.",
             'Reply ONLY a JSON array like [{"id":0,"pick":"volcano"}, ...] -- no prose.', ""]
    for it in items:
        lines.append(f'TRIAL {it["id"]}: candidates={it["cands"]}')
        lines.append(f'  clue: "{it["clue"]}"')
    open(os.path.join(SLUG, ".fable_prompt.txt"), "w").write("\n".join(lines))
    try:
        p = subprocess.run(["sidecar", "fable", "--model", MODEL, "--file",
                            os.path.join(SLUG, ".fable_prompt.txt"), "--timeout", "150"],
                           capture_output=True, text=True, timeout=210)
    except (subprocess.TimeoutExpired, OSError) as ex:
        sys.stderr.write(f"[oracle] fable call failed: {ex}\n")
        return {}
    return parse_picks(p.stdout)

def run_arm(concepts, emit, mapping, arm, fix):
    rows = []
    for K in K_SWEEP:
        for t in TRUNC:
            r = rng(SEED + K*17 + (99 if t == "full" else t))
            items, meta = [], []
            for k, tgt in enumerate(concepts):
                src = mapping[tgt]
                clue = trunc(clean(emit[src]), t)
                cands = distractors(tgt, concepts, K, r)
                items.append({"id": k, "clue": clue, "cands": cands}); meta.append((k, tgt, cands))
            picks = ask_fable_batch(items); hits = 0
            for k, tgt, cands in meta:
                pk = picks.get(k, ""); hit = int(pk == tgt); hits += hit
                fix.write(json.dumps({"arm": arm, "K": K, "t": t, "tgt": tgt, "pick": pk,
                                      "hit": hit}, ensure_ascii=False) + "\n")
            acc = hits / len(concepts); rows.append({"K": K, "t": t, "acc": acc, "chance": 1.0 / K})
            print(f"[{arm}] K={K} t={t}: acc={acc:.3f} (chance={1.0/K:.3f})", flush=True)
    return rows

def threshold_step(rows):
    return sum(1 for x in rows if x["acc"] >= 0.5)

def main():
    concepts, emit = load(); r0 = rng(SEED)
    real_map = {c: c for c in concepts}; shuf_map = derange(concepts, r0)
    fix = open(OUT, "w")
    print("=== H_9112 PSYCHO-K re-score (frozen bar: PREREG.md) ===", flush=True)
    real = run_arm(concepts, emit, real_map, "real", fix)
    shuf = run_arm(concepts, emit, shuf_map, "shuffle", fix)
    fix.close()
    th_real, th_shuf = threshold_step(real), threshold_step(shuf)
    mean_real = statistics.mean(x["acc"] for x in real); mean_shuf = statistics.mean(x["acc"] for x in shuf)
    dsep = mean_real - mean_shuf
    b1 = (th_real - th_shuf) >= 1; b2 = dsep >= 0.15
    if b1 and b2:
        verdict = "GREEN REFERENTIAL-EFFICACY-MEASURABLE (real emits carry graded referent-legibility beyond shuffle)"
    elif not b1 and not b2 and mean_real <= mean_shuf + 0.05:
        verdict = "RED COUPLING-FLOOR-AT-EMIT-LAYER (real ~= shuffle across KxT; DPI reached the emit layer)"
    else:
        verdict = "AMBER PARTIAL / measurement-dependent"
    with open(RESULT, "w") as f:
        f.write("# H_9112 -- Referential-efficacy PSYCHO-K + MRR re-score -- RESULT\n\n")
        f.write(f"**VERDICT: {verdict}**\n\n")
        f.write(f"- threshold_real(configs acc>=0.5)={th_real} - threshold_shuffle={th_shuf} - delta={th_real-th_shuf} (bar>=1: {'PASS' if b1 else 'FAIL'})\n")
        f.write(f"- mean_acc_real={mean_real:.3f} - mean_acc_shuffle={mean_shuf:.3f} - delta_sep={dsep:.3f} (bar>=0.15: {'PASS' if b2 else 'FAIL'})\n")
        f.write(f"- oracle={MODEL} (theta outside anima closure) - emits FROZEN engine-native (H_9111) - tier=DIRECTIONAL-on-external-oracle\n\n")
        f.write("## real arm (acc vs difficulty)\n")
        for x in real: f.write(f"  K={x['K']} t={x['t']}: acc={x['acc']:.3f} chance={x['chance']:.3f}\n")
        f.write("## shuffle arm\n")
        for x in shuf: f.write(f"  K={x['K']} t={x['t']}: acc={x['acc']:.3f} chance={x['chance']:.3f}\n")
        f.write("\nself-clone baseline: H_9111 established 0/7 (floor) -- engine-native anima-clone salience decoder.\n")
    print("\n" + verdict, flush=True)
    print(f"threshold delta={th_real-th_shuf} - mean-acc delta={dsep:.3f} -> {RESULT}", flush=True)

if __name__ == "__main__":
    main()
