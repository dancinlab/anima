#!/usr/bin/env python3
# ============================================================================
# H_9113 — Referential-efficacy THRESHOLD resolution (sub-8-byte sweep, PREREG.md).
#   H_9112 landed 🟢 but real stayed near-ceiling (0.982) -> psychometric threshold
#   UNRESOLVED. Here K is fixed at 14 (hardest) and the clue is truncated SUB-8-byte
#   {8,6,4,3,2,1} until real referential decode breaks -> resolves the coupling-strength
#   SCALAR b50 (clue-bytes at 50% decode). Same FROZEN H_9111 emits (14 concepts), anima
#   side FROZEN, external oracle receiver (claude-fable-5, theta outside anima closure).
#   STDLIB ONLY (subprocess/json/re) -> grep-clean. Tier = DIRECTIONAL-on-external-oracle.
# ============================================================================
import subprocess, sys, json, os, re, statistics

SLUG   = os.path.dirname(os.path.abspath(__file__))
EMITS  = os.path.join(SLUG, "..", "9111_llm_interlocutor", "emits.tsv")
OUT    = os.path.join(SLUG, "rescore_fixture.jsonl")
RESULT = os.path.join(SLUG, "RESULT.md")
MODEL  = "claude-fable-5"

# --- FROZEN config (PREREG.md) ---
K_FIXED    = 14                       # hardest distractor set (all concepts)
TRUNC      = [8, 6, 4, 3, 2, 1]       # sub-8-byte sweep (the new regime H_9112 didn't reach)
SEED       = 9113
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
             "The clue may be very SHORT (a few bytes) -- give your single best guess anyway.",
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
    for t in TRUNC:
        r = rng(SEED + t)
        items, meta = [], []
        for k, tgt in enumerate(concepts):
            src = mapping[tgt]
            clue = clean(emit[src])[:t]
            cands = distractors(tgt, concepts, K_FIXED, r)
            items.append({"id": k, "clue": clue, "cands": cands}); meta.append((k, tgt))
        picks = ask_fable_batch(items); hits = 0
        for k, tgt in meta:
            pk = picks.get(k, ""); hit = int(pk == tgt); hits += hit
            fix.write(json.dumps({"arm": arm, "t": t, "tgt": tgt, "pick": pk, "hit": hit},
                                 ensure_ascii=False) + "\n")
        acc = hits / len(concepts); rows.append({"t": t, "acc": acc})
        print(f"[{arm}] K=14 t={t}B: acc={acc:.3f} (chance={1.0/K_FIXED:.3f})", flush=True)
    return rows

def b50(rows):
    # clue-byte length at which real acc crosses 0.5 (linear interp between adjacent
    # sweep points, largest-t first). None if never below 0.5 within the sweep.
    s = sorted(rows, key=lambda x: -x["t"])   # descending byte length (easy -> hard)
    for i in range(len(s) - 1):
        a, b = s[i], s[i + 1]
        if a["acc"] >= 0.5 > b["acc"]:
            # interp between t=a.t (acc>=.5) and t=b.t (acc<.5)
            frac = (a["acc"] - 0.5) / (a["acc"] - b["acc"]) if a["acc"] != b["acc"] else 0.0
            return a["t"] + frac * (b["t"] - a["t"])
    if s[-1]["acc"] >= 0.5:
        return None   # never dropped below 0.5 even at t=1 -> UNRESOLVED-STILL (extreme lower bound)
    return float(s[0]["t"])  # already below 0.5 at the easiest point (shouldn't happen post-H_9112)

def main():
    concepts, emit = load(); r0 = rng(SEED)
    real_map = {c: c for c in concepts}; shuf_map = derange(concepts, r0)
    fix = open(OUT, "w")
    print("=== H_9113 THRESHOLD resolution (sub-8-byte, frozen bar: PREREG.md) ===", flush=True)
    real = run_arm(concepts, emit, real_map, "real", fix)
    shuf = run_arm(concepts, emit, shuf_map, "shuffle", fix)
    fix.close()
    b = b50(real)
    real_gt_shuf = all(rr["acc"] > sh["acc"] for rr, sh in zip(real, shuf))
    if b is None:
        verdict = "🔴/lower-bound UNRESOLVED-STILL — real never < 0.5 even at t=1 byte (reference so strong 1 byte suffices; b50 < 1)"
    elif real_gt_shuf:
        strength = "very strong" if b <= 6 else "strong"
        verdict = f"🟢 THRESHOLD-RESOLVED — b50_real={b:.2f} bytes ({strength} reference) · real>shuffle at every t"
    else:
        verdict = f"🟠 PARTIAL — b50_real={b:.2f} bytes but real≈shuffle at some t (coupling floor under extreme truncation)"
    mean_real = statistics.mean(x["acc"] for x in real); mean_shuf = statistics.mean(x["acc"] for x in shuf)
    with open(RESULT, "w") as f:
        f.write("# H_9113 -- Referential-efficacy THRESHOLD resolution -- RESULT\n\n")
        f.write(f"**VERDICT: {verdict}**\n\n")
        f.write(f"- coupling-strength scalar b50_real = {('<1' if b is None else round(b,2))} bytes-of-clue at 50% decode (K=14, near-synonym distractors)\n")
        f.write(f"- real>shuffle at EVERY t: {real_gt_shuf} · mean_acc_real={mean_real:.3f} · mean_acc_shuffle={mean_shuf:.3f}\n")
        f.write(f"- oracle={MODEL} (theta outside anima closure) - emits FROZEN engine-native (H_9111) - tier=DIRECTIONAL-on-external-oracle\n\n")
        f.write("## real arm (acc vs clue bytes, K=14)\n")
        for x in real: f.write(f"  t={x['t']}B: acc={x['acc']:.3f}\n")
        f.write("## shuffle arm\n")
        for x in shuf: f.write(f"  t={x['t']}B: acc={x['acc']:.3f}\n")
        f.write(f"\nchance (K=14) = {1.0/K_FIXED:.3f}. H_9112 established acc=0.857 at t=8B (this sweep starts there and pushes down).\n")
    print("\n" + verdict, flush=True)
    print(f"-> {RESULT}", flush=True)

if __name__ == "__main__":
    main()
