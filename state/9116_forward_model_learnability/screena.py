#!/usr/bin/env python3
# ============================================================================
# H_9116 — Screen-A: is the forward-model target signal STRUCTURAL (learnable) or emit-noise?
#   ($0, reuse H_9115 fixture, no oracle. fable §2 gate part A.) Screen-B showed compression
#   lowers b50 (headroom real). Screen-A asks: is the GAIN a CONSISTENT structural signal a
#   lane15 forward-model could learn (front-load discriminative content / cut filler-prefix),
#   or a few-emit fluke? Per-emit decompose: does filler-prefix length predict compression gain?
#   If emits with more filler-prefix gain more from front-loading → clean learnable target.
#   STDLIB ONLY (json/re/statistics) → grep-clean. Tier=DIRECTIONAL (feature-proxy on frozen emit;
#   the real forward-model reads the richer A/G trunk, so this is a LOWER BOUND on learnability).
# ============================================================================
import json, os, re, statistics

SLUG   = os.path.dirname(os.path.abspath(__file__))
EMITS  = os.path.join(SLUG, "..", "9111_llm_interlocutor", "emits.tsv")
FIX    = os.path.join(SLUG, "..", "9115_forward_model_screen", "screenb_fixture.jsonl")
RESULT = os.path.join(SLUG, "RESULT.md")
DEGEN_TAIL = "the state and the concern for the state"
STOP = {"a","an","the","that","with","of","and","to","in","its","it","you","your","on",
        "above","under","from","for","or","as","by","is","are","used","up","down","very",
        "into","out","other","where","they","their","head","stay","open","full","small",
        "long","tall","big","huge"}
PROBE_T = 4   # the discriminative truncation (H_9115: raw 0.786 vs compressed 0.857 — variance)

def clean(c):
    i = c.find(DEGEN_TAIL[:18]); return (c[:i] if i >= 0 else c).strip()

def load_emits():
    e = {}
    with open(os.path.normpath(EMITS)) as f:
        for ln in f:
            if ln.startswith("EMIT\t"):
                _, i, c, ok, txt = ln.rstrip("\n").split("\t", 4); e[c] = clean(txt)
    return e

def filler_prefix_bytes(raw):
    # bytes before the first discriminative (non-stop) content word
    m = re.finditer(r"[a-z]+", raw.lower())
    for w in m:
        if w.group(0) not in STOP:
            return w.start()
    return len(raw)

def pearson(xs, ys):
    n = len(xs)
    if n < 3: return None
    mx, my = statistics.mean(xs), statistics.mean(ys)
    num = sum((x-mx)*(y-my) for x, y in zip(xs, ys))
    dx = sum((x-mx)**2 for x in xs) ** 0.5
    dy = sum((y-my)**2 for y in ys) ** 0.5
    return num/(dx*dy) if dx > 0 and dy > 0 else None

def main():
    emits = load_emits()
    # per-emit decode outcome at PROBE_T for raw and compressed
    hit = {"raw": {}, "compressed": {}}
    for ln in open(FIX):
        r = json.loads(ln)
        if r.get("t") == PROBE_T:
            hit[r["mode"]][r["tgt"]] = r["hit"]
    concepts = sorted(emits)
    rows = []
    for c in concepts:
        raw = emits[c]
        fp = filler_prefix_bytes(raw)
        rh = hit["raw"].get(c); ch = hit["compressed"].get(c)
        if rh is None or ch is None: continue
        rows.append({"c": c, "filler_prefix": fp, "raw_hit": rh, "comp_hit": ch, "gain": ch - rh})
    fps   = [r["filler_prefix"] for r in rows]
    gains = [r["gain"] for r in rows]
    n_gain_pos = sum(1 for g in gains if g > 0)
    n_gain_neg = sum(1 for g in gains if g < 0)
    corr = pearson(fps, gains)
    # aggregate at PROBE_T
    raw_acc  = statistics.mean(r["raw_hit"] for r in rows)
    comp_acc = statistics.mean(r["comp_hit"] for r in rows)
    # verdict: structural learnable signal iff compression gain is net-positive & broad,
    # AND filler-prefix positively predicts gain (more filler → more to gain by front-loading).
    broad = n_gain_pos >= 2 * max(1, n_gain_neg) and (comp_acc - raw_acc) >= 0.10
    structured = corr is not None and corr >= 0.3
    if broad and structured:
        verdict = f"🟢 STRUCTURAL-LEARNABLE — compression gain broad ({n_gain_pos}↑/{n_gain_neg}↓, acc {raw_acc:.2f}→{comp_acc:.2f}) AND filler-prefix predicts gain (r={corr:.2f}) → forward-model target is a consistent front-loading signal a lane15 head can learn"
    elif broad:
        verdict = f"🟡 GAIN-BROAD-BUT-UNSTRUCTURED — gain broad ({n_gain_pos}↑/{n_gain_neg}↓) but filler-prefix corr weak (r={corr}) → learnable but the target feature is richer than filler-prefix (needs the A/G trunk, not surface length)"
    else:
        verdict = f"🔴 GAIN-NOT-BROAD — compression gain not consistent ({n_gain_pos}↑/{n_gain_neg}↓) → Screen-B headroom may be few-emit fluke; forward-model target unclear"
    with open(RESULT, "w") as f:
        f.write("# H_9116 — Screen-A forward-model learnability ($0) — RESULT\n\n")
        f.write(f"**VERDICT: {verdict}**\n\n")
        f.write(f"- probe truncation t={PROBE_T}B · raw_acc={raw_acc:.3f} → comp_acc={comp_acc:.3f}\n")
        f.write(f"- compression gain: {n_gain_pos} emits ↑ · {n_gain_neg} ↓ · {len(rows)-n_gain_pos-n_gain_neg} = · corr(filler_prefix, gain) r={corr}\n")
        f.write(f"- tier=DIRECTIONAL (surface-feature proxy on frozen emit; real forward-model reads richer A/G trunk = lower bound on learnability)\n\n")
        f.write("## per-emit (filler-prefix bytes · raw_hit@4B · comp_hit@4B · gain)\n")
        for r in sorted(rows, key=lambda x: -x["filler_prefix"]):
            f.write(f"  {r['c']:<12} fp={r['filler_prefix']:>2}  raw={r['raw_hit']} comp={r['comp_hit']} gain={r['gain']:+d}\n")
        f.write("\nGate (fable §2): Screen-B 🟢(headroom) ∧ Screen-A → engine-native mini (lane15) justified. This is part A.\n")
    print(verdict, flush=True)
    print(f"raw@4B={raw_acc:.3f} comp@4B={comp_acc:.3f} · gain {n_gain_pos}↑/{n_gain_neg}↓ · corr={corr} -> {RESULT}", flush=True)

if __name__ == "__main__":
    main()
