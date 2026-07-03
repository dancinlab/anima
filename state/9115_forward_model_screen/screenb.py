#!/usr/bin/env python3
# ============================================================================
# H_9115 — Screen-B: forward-model $0 headroom pre-screen (fable §2 DESIGN, DESIGN_fable_s2.md).
#   Does anima's frozen emit have RE-PACKAGING HEADROOM — can the SAME referent MI be
#   decoded from FEWER bytes (lower b50) while ACCURACY HOLDS? If NO transform lowers b50 at
#   held accuracy, the emit is already at the receiver-conditioned coding floor → forward-model
#   INERT → GPU unjustified (DPI wall confirmed). If YES, the §2 lever is physically possible.
#   Info-preserving transform = strip non-discriminative filler (leading article + stopwords),
#   content words kept IN ORDER (no new info). anima emit FROZEN. Single receiver (claude-fable-5,
#   fastest) — $0 DIRECTIONAL screen (headroom existence, not a tier claim). STDLIB ONLY.
# ============================================================================
import subprocess, sys, json, os, re

SLUG   = os.path.dirname(os.path.abspath(__file__))
EMITS  = os.path.join(SLUG, "..", "9111_llm_interlocutor", "emits.tsv")
OUT    = os.path.join(SLUG, "screenb_fixture.jsonl")
RESULT = os.path.join(SLUG, "RESULT.md")
MODEL  = "claude-fable-5"

K_FIXED    = 14
TRUNC      = [8, 6, 4, 3, 2]          # byte sweep to locate b50 per transform
SEED       = 9115
DEGEN_TAIL = "the state and the concern for the state"
# non-discriminative filler removed by the info-preserving 'compressed' transform.
STOP = {"a","an","the","that","with","of","and","to","in","its","it","you","your","on",
        "above","under","from","for","or","as","by","is","are","used","up","down","very",
        "into","out","other","where","they","their","head","stay","open","full","small",
        "long","tall","big","huge"}

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

def compress(text):
    # info-preserving: drop non-discriminative filler words, keep content words IN ORDER.
    words = re.findall(r"[a-z]+", text.lower())
    kept = [w for w in words if w not in STOP]
    return " ".join(kept)

def transform(text, mode):
    c = clean(text)
    return c if mode == "raw" else compress(c)

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

def parse_picks(out):
    picks = {}
    m = re.search(r"\[.*\]", out, re.S)
    if m:
        try:
            for o in json.loads(m.group(0)):
                picks[int(o["id"])] = str(o.get("pick", "")).strip().lower()
        except (ValueError, KeyError, TypeError) as ex:
            sys.stderr.write(f"[parse] malformed ({ex}); regex fallback\n")
    if not picks:
        for ln in out.splitlines():
            mm = re.match(r"\s*(\d+)\D+([a-z]+)", ln.strip().lower())
            if mm: picks[int(mm.group(1))] = mm.group(2)
    return picks

def ask(items):
    lines = ["You are a referential-decoding receiver. Below are numbered TRIALS.",
             "Each trial has a CLUE describing exactly ONE concept from its CANDIDATES",
             "(the concept's own name was removed -- match by MEANING only).",
             "The clue may be very SHORT -- give your single best guess anyway.",
             'Reply ONLY a JSON array like [{"id":0,"pick":"volcano"}, ...] -- no prose.', ""]
    for it in items:
        lines.append(f'TRIAL {it["id"]}: candidates={it["cands"]}')
        lines.append(f'  clue: "{it["clue"]}"')
    tmp = os.path.join(SLUG, ".prompt.txt"); open(tmp, "w").write("\n".join(lines))
    try:
        p = subprocess.run(["sidecar","fable","--model",MODEL,"--file",tmp,"--timeout","150"],
                           capture_output=True, text=True, timeout=210)
    except (subprocess.TimeoutExpired, OSError) as ex:
        sys.stderr.write(f"[oracle] {ex}\n"); return {}
    return parse_picks(p.stdout)

def run_mode(concepts, emit, mode, fix):
    rows = []
    # full-clue accuracy (accuracy-hold check): t = large
    for t in ["full"] + TRUNC:
        r = rng(SEED + (99 if t == "full" else t))
        items, meta = [], []
        for k, tgt in enumerate(concepts):
            txt = transform(emit[tgt], mode)
            clue = txt if t == "full" else txt[:t]
            items.append({"id": k, "clue": clue, "cands": distractors(tgt, concepts, K_FIXED, r)})
            meta.append((k, tgt))
        picks = ask(items); hits = sum(1 for k, tgt in meta if picks.get(k) == tgt)
        acc = hits / len(concepts); rows.append({"t": t, "acc": acc})
        for k, tgt in meta:
            fix.write(json.dumps({"mode": mode, "t": t, "tgt": tgt, "pick": picks.get(k, ""),
                                  "hit": int(picks.get(k) == tgt)}, ensure_ascii=False) + "\n")
        print(f"[{mode}] t={t}: acc={acc:.3f}", flush=True)
    return rows

def b50(rows):
    s = sorted([x for x in rows if x["t"] != "full"], key=lambda x: -x["t"])
    for i in range(len(s) - 1):
        a, b = s[i], s[i + 1]
        if a["acc"] >= 0.5 > b["acc"]:
            frac = (a["acc"] - 0.5) / (a["acc"] - b["acc"]) if a["acc"] != b["acc"] else 0.0
            return a["t"] + frac * (b["t"] - a["t"])
    return None if s[-1]["acc"] >= 0.5 else float(s[0]["t"])

def main():
    concepts, emit = load()
    fix = open(OUT, "w")
    print("=== H_9115 Screen-B: forward-model headroom ($0 DIRECTIONAL) ===", flush=True)
    raw = run_mode(concepts, emit, "raw", fix)
    comp = run_mode(concepts, emit, "compressed", fix)
    fix.close()
    b_raw, b_comp = b50(raw), b50(comp)
    acc_raw_full = next(x["acc"] for x in raw if x["t"] == "full")
    acc_comp_full = next(x["acc"] for x in comp if x["t"] == "full")
    # avg bytes per transform (compression ratio, informational)
    import statistics
    len_raw = statistics.mean(len(transform(emit[c], "raw")) for c in concepts)
    len_comp = statistics.mean(len(transform(emit[c], "compressed")) for c in concepts)
    acc_hold = acc_comp_full >= acc_raw_full - 0.10
    headroom = (b_raw is not None and b_comp is not None and b_comp < b_raw - 0.3 and acc_hold)
    if headroom:
        verdict = f"🟢 HEADROOM-EXISTS — compressed b50={b_comp:.2f} < raw b50={b_raw:.2f} at held accuracy (comp_full={acc_comp_full:.2f} vs raw {acc_raw_full:.2f}) → forward-model lever PHYSICALLY POSSIBLE → engine-native mini justified"
    elif not acc_hold:
        verdict = f"🟠 ACCURACY-DROP — compression hurt accuracy (comp_full={acc_comp_full:.2f} < raw {acc_raw_full:.2f}); transform not info-preserving here, inconclusive on headroom"
    else:
        verdict = f"🔴 NO-HEADROOM (INERT) — compressed b50={b_comp} NOT below raw b50={b_raw} at held accuracy → emit already at receiver-coding floor → forward-model DPI-walled → GPU UNJUSTIFIED"
    with open(RESULT, "w") as f:
        f.write("# H_9115 — Screen-B forward-model headroom ($0) — RESULT\n\n")
        f.write(f"**VERDICT: {verdict}**\n\n")
        f.write(f"- b50_raw={b_raw} · b50_compressed={b_comp} · accuracy-hold(full)={acc_comp_full:.3f} vs {acc_raw_full:.3f} ({'HELD' if acc_hold else 'DROPPED'})\n")
        f.write(f"- mean bytes raw={len_raw:.1f} · compressed={len_comp:.1f} (compression {100*(1-len_comp/len_raw):.0f}%)\n")
        f.write(f"- receiver={MODEL} (single, $0 DIRECTIONAL screen) · emit FROZEN (H_9111) · tier=DIRECTIONAL\n\n")
        f.write("## raw arm (acc vs clue bytes)\n")
        for x in raw: f.write(f"  t={x['t']}: acc={x['acc']:.3f}\n")
        f.write("## compressed arm\n")
        for x in comp: f.write(f"  t={x['t']}: acc={x['acc']:.3f}\n")
        f.write("\nGate: 🟢 HEADROOM → engine-native mini (lane15 side-loop) justified. 🔴 INERT → forward-model DPI-walled, GPU stop.\n")
    print("\n" + verdict, flush=True); print(f"-> {RESULT}", flush=True)

if __name__ == "__main__":
    main()
