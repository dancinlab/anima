#!/usr/bin/env python3
# ============================================================================
# H_9114 — Receiver-PANEL referent-agreement (PREREG.md). Is anima's emit reference
#   PUBLIC/objective (≥2 heterogeneous external minds independently converge on the same
#   referent) or single-oracle-idiosyncratic? Same FROZEN H_9111 emits (14 concepts),
#   anima side FROZEN. Receivers = {claude-fable-5, sonnet, haiku} via sidecar fable
#   (heterogeneous theta, all outside anima closure). STDLIB ONLY -> grep-clean.
#   Tier target = PANEL-CONSENSUS-DIRECTIONAL (lifts single-oracle DIRECTIONAL).
# ============================================================================
import subprocess, sys, json, os, re, statistics, itertools

SLUG   = os.path.dirname(os.path.abspath(__file__))
EMITS  = os.path.join(SLUG, "..", "9111_llm_interlocutor", "emits.tsv")
OUT    = os.path.join(SLUG, "rescore_fixture.jsonl")
RESULT = os.path.join(SLUG, "RESULT.md")
RECEIVERS = ["claude-fable-5", "sonnet", "haiku"]

# --- FROZEN config (PREREG.md) ---
K_FIXED    = 14
TRUNC      = [8, 4]                   # informative 2-point: 8B strong-signal, 4B divergence-onset (H_9113)
SEED       = 9114
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
    picks = {}
    m = re.search(r"\[.*\]", out, re.S)
    if m:
        try:
            for o in json.loads(m.group(0)):
                picks[int(o["id"])] = str(o.get("pick", "")).strip().lower()
        except (ValueError, KeyError, TypeError) as ex:
            sys.stderr.write(f"[parse] JSON malformed ({ex}); line-regex fallback\n")
    if not picks:
        for ln in out.splitlines():
            mm = re.match(r"\s*(\d+)\D+([a-z]+)", ln.strip().lower())
            if mm:
                picks[int(mm.group(1))] = mm.group(2)
    return picks

def ask(model, items):
    lines = ["You are a referential-decoding receiver. Below are numbered TRIALS.",
             "Each trial has a CLUE describing exactly ONE concept from its CANDIDATES",
             "(the concept's own name was removed -- match by MEANING only).",
             "The clue may be very SHORT (a few bytes) -- give your single best guess anyway.",
             'Reply ONLY a JSON array like [{"id":0,"pick":"volcano"}, ...] -- no prose.', ""]
    for it in items:
        lines.append(f'TRIAL {it["id"]}: candidates={it["cands"]}')
        lines.append(f'  clue: "{it["clue"]}"')
    tmp = os.path.join(SLUG, f".prompt_{model}.txt")
    open(tmp, "w").write("\n".join(lines))
    try:
        p = subprocess.run(["sidecar", "fable", "--model", model, "--file", tmp, "--timeout", "150"],
                           capture_output=True, text=True, timeout=210)
    except (subprocess.TimeoutExpired, OSError) as ex:
        sys.stderr.write(f"[oracle {model}] failed: {ex}\n"); return None
    pk = parse_picks(p.stdout)
    return pk if pk else None

def pairwise_agreement(picks_by_recv, n):
    # mean over trials of (fraction of receiver-pairs picking the same concept)
    recvs = [m for m in picks_by_recv if picks_by_recv[m] is not None]
    if len(recvs) < 2:
        return None, recvs
    pairs = list(itertools.combinations(recvs, 2))
    tot = 0.0
    for k in range(n):
        same = sum(1 for a, b in pairs
                   if picks_by_recv[a].get(k, "_a") == picks_by_recv[b].get(k, "_b"))
        tot += same / len(pairs)
    return tot / n, recvs

def run(concepts, emit, mapping, arm, fix):
    n = len(concepts); rows = []
    for t in TRUNC:
        r = rng(SEED + t)
        items, meta = [], []
        for k, tgt in enumerate(concepts):
            clue = clean(emit[mapping[tgt]])[:t]
            items.append({"id": k, "clue": clue, "cands": distractors(tgt, concepts, K_FIXED, r)})
            meta.append((k, tgt))
        picks_by_recv = {m: ask(m, items) for m in RECEIVERS}
        acc = {}
        for m, pk in picks_by_recv.items():
            if pk is None: acc[m] = None; continue
            acc[m] = sum(1 for k, tgt in meta if pk.get(k) == tgt) / n
        # consensus (majority vote) accuracy
        cons_hits = 0
        for k, tgt in meta:
            votes = [pk.get(k) for pk in picks_by_recv.values() if pk is not None]
            if votes:
                win = max(set(votes), key=votes.count)
                cons_hits += int(win == tgt)
        cons = cons_hits / n
        agr, recvs = pairwise_agreement(picks_by_recv, n)
        rows.append({"t": t, "acc": acc, "consensus": cons, "agreement": agr, "responders": recvs})
        for k, tgt in meta:
            fix.write(json.dumps({"arm": arm, "t": t, "tgt": tgt,
                                  "picks": {m: (picks_by_recv[m].get(k) if picks_by_recv[m] else None) for m in RECEIVERS}},
                                 ensure_ascii=False) + "\n")
        accs = " ".join(f"{m.split('-')[0]}={acc[m]:.2f}" if acc[m] is not None else f"{m.split('-')[0]}=SKIP" for m in RECEIVERS)
        print(f"[{arm}] t={t}B: {accs} | consensus={cons:.2f} agreement={('%.2f'%agr) if agr is not None else 'NA'}", flush=True)
    return rows

def main():
    concepts, emit = load(); n = len(concepts)
    fix = open(OUT, "w")
    print(f"=== H_9114 receiver-PANEL ({','.join(RECEIVERS)}) frozen bar: PREREG.md ===", flush=True)
    real = run(concepts, emit, {c: c for c in concepts}, "real", fix)
    shuf = run(concepts, emit, derange(concepts, rng(SEED)), "shuffle", fix)
    fix.close()
    # frozen-bar eval on signal bytes t>=4
    sig_real = [x for x in real if x["t"] >= 4]; sig_shuf = [x for x in shuf if x["t"] >= 4]
    responders = sorted(set().union(*[set(x["responders"]) for x in real])) if real else []
    # (1) >=2 receivers decode real>shuffle at signal bytes
    def recv_beats(m):
        rr = [x["acc"].get(m) for x in sig_real if x["acc"].get(m) is not None]
        ss = [x["acc"].get(m) for x in sig_shuf if x["acc"].get(m) is not None]
        return rr and ss and statistics.mean(rr) > statistics.mean(ss)
    beaters = [m for m in RECEIVERS if recv_beats(m)]
    b1 = len(beaters) >= 2
    # (2) agreement real >= 0.60 and >= shuffle+0.20 at signal bytes
    ar = [x["agreement"] for x in sig_real if x["agreement"] is not None]
    ash = [x["agreement"] for x in sig_shuf if x["agreement"] is not None]
    mean_ar = statistics.mean(ar) if ar else None
    mean_ash = statistics.mean(ash) if ash else None
    b2 = mean_ar is not None and mean_ash is not None and mean_ar >= 0.60 and (mean_ar - mean_ash) >= 0.20
    # (3) consensus >= best single receiver
    cons_sig = statistics.mean(x["consensus"] for x in sig_real)
    best_single = max((statistics.mean([x["acc"][m] for x in sig_real if x["acc"].get(m) is not None])
                       for m in RECEIVERS if any(x["acc"].get(m) is not None for x in sig_real)), default=0)
    b3 = cons_sig >= best_single - 1e-9
    if b1 and b2 and b3:
        verdict = f"🟢 PUBLIC-REFERENCE (tier-lift to PANEL-CONSENSUS) — {len(beaters)} receivers decode>shuffle, agreement={mean_ar:.2f} vs shuffle {mean_ash:.2f}, consensus={cons_sig:.2f}>=best {best_single:.2f}"
    elif len(beaters) <= 1:
        verdict = f"🟠 SINGLE-ORACLE-IDIOSYNCRATIC — only {beaters} decode; reference not cross-mind objective"
    else:
        verdict = f"🟠 PARTIAL — beaters={beaters} b2(agr)={b2} b3(consensus)={b3}; agreement={mean_ar} vs {mean_ash}"
    with open(RESULT, "w") as f:
        f.write("# H_9114 -- Receiver-PANEL referent-agreement -- RESULT\n\n")
        f.write(f"**VERDICT: {verdict}**\n\n")
        f.write(f"- responders: {responders} · receivers-beating-shuffle(t>=4): {beaters}\n")
        f.write(f"- mean inter-receiver agreement (real, t>=4) = {mean_ar} · shuffle = {mean_ash}\n")
        f.write(f"- consensus acc (t>=4) = {cons_sig:.3f} · best single receiver = {best_single:.3f}\n")
        f.write(f"- receivers = {RECEIVERS} (heterogeneous theta, all outside anima closure) · emits FROZEN engine-native (H_9111)\n")
        f.write(f"- tier = PANEL-CONSENSUS-DIRECTIONAL if 🟢 else DIRECTIONAL-on-external-oracle\n\n")
        f.write("## real arm\n")
        for x in real: f.write(f"  t={x['t']}B: acc={ {m:(round(v,3) if v is not None else None) for m,v in x['acc'].items()} } consensus={x['consensus']:.3f} agreement={x['agreement']}\n")
        f.write("## shuffle arm\n")
        for x in shuf: f.write(f"  t={x['t']}B: acc={ {m:(round(v,3) if v is not None else None) for m,v in x['acc'].items()} } consensus={x['consensus']:.3f} agreement={x['agreement']}\n")
    print("\n" + verdict, flush=True)
    print(f"-> {RESULT}", flush=True)

if __name__ == "__main__":
    main()
