#!/usr/bin/env python3
# ============================================================================
# H_9117 — §2 Stage-0: validate the in-engine forward-model proxy d̂ BEFORE any .hexa/GPU.
#   (fable §2 impl DESIGN_fable_s2impl.md.) The engine's mouth-backend can SCORE (run backwards)
#   = an in-engine surrogate listener, no external oracle. fable's d̂ = frozen-listener contrastive
#   PREFIX decodability: s_k = logP(r*|e_{:k}) − logsumexp_r P(r|e_{:k}); d̂ = Σ_k w_k·s_k (front-decay).
#   Here we compute a $0 LOWER-BOUND surrogate of that listener: a lexical IDF-contrastive prefix
#   scorer (concept profiles = content-words of each full emit; the mouth-backend would see richer
#   discriminability, so this is a floor). GATE: corr(d̂, oracle-decodability) must (a) be meaningful
#   and (b) BEAT the filler_prefix degenerate baseline (Screen-A's surface proxy). If a crude lexical
#   listener already correlates, the real CLM-listener certainly does → Stage-1 .hexa justified.
#   STDLIB ONLY, no oracle calls (reuse H_9115 fixture for labels). Tier=DIRECTIONAL.
# ============================================================================
import json, os, re, math, statistics

SLUG   = os.path.dirname(os.path.abspath(__file__))
EMITS  = os.path.join(SLUG, "..", "9111_llm_interlocutor", "emits.tsv")
FIX    = os.path.join(SLUG, "..", "9115_forward_model_screen", "screenb_fixture.jsonl")
RESULT = os.path.join(SLUG, "RESULT.md")
DEGEN_TAIL = "the state and the concern for the state"
STOP = {"a","an","the","that","with","of","and","to","in","its","it","you","your","on","above",
        "under","from","for","or","as","by","is","are","used","up","down","very","into","out",
        "other","where","they","their","head","stay","open","full","small","long","tall","big","huge"}
DECAY = 0.75   # front-byte geometric weight (fable ep_fm_prefix_decay analog)

def clean(c):
    i = c.find(DEGEN_TAIL[:18]); return (c[:i] if i >= 0 else c).strip()

def load_emits():
    e = {}
    for ln in open(os.path.normpath(EMITS)):
        if ln.startswith("EMIT\t"):
            _, i, c, ok, txt = ln.rstrip("\n").split("\t", 4); e[c] = clean(txt)
    return e

def content_words(txt):
    return [w for w in re.findall(r"[a-z]+", txt.lower()) if w not in STOP]

def d_hat(target, emits, idf):
    # contrastive prefix decodability surrogate: walk the target emit's content words in order;
    # after each word accumulate per-concept lexical score, take target-vs-best-distractor margin,
    # front-weight by geometric decay. Higher = target wins EARLY (front-loaded decodable).
    words = content_words(emits[target])
    score = {c: 0.0 for c in emits}
    dh = 0.0
    for i, w in enumerate(words):
        for c in emits:
            if w in profile[c]:
                score[c] += idf.get(w, 0.0)
        tgt = score[target]
        best_other = max(v for c, v in score.items() if c != target)
        margin = tgt - best_other
        dh += (DECAY ** i) * margin
    return dh

def pearson(xs, ys):
    n = len(xs)
    if n < 3: return None
    mx, my = statistics.mean(xs), statistics.mean(ys)
    num = sum((x-mx)*(y-my) for x, y in zip(xs, ys))
    dx = sum((x-mx)**2 for x in xs) ** 0.5; dy = sum((y-my)**2 for y in ys) ** 0.5
    return num/(dx*dy) if dx > 0 and dy > 0 else None

emits = load_emits()
profile = {c: set(content_words(emits[c])) for c in emits}
# IDF: rare content-word across concept profiles = discriminative
docfreq = {}
for c in emits:
    for w in profile[c]:
        docfreq[w] = docfreq.get(w, 0) + 1
N = len(emits)
idf = {w: math.log(N / df) for w, df in docfreq.items()}

def filler_prefix(txt):
    for w in re.finditer(r"[a-z]+", txt.lower()):
        if w.group(0) not in STOP: return w.start()
    return len(txt)

def main():
    # oracle-decodability label per emit = # short-prefix hits (raw mode) across truncations
    hits = {}
    for ln in open(FIX):
        r = json.loads(ln)
        if r["mode"] == "raw" and r["t"] != "full":
            hits.setdefault(r["tgt"], 0); hits[r["tgt"]] += r["hit"]
    concepts = sorted(emits)
    dh   = [d_hat(c, emits, idf) for c in concepts]
    fp   = [-filler_prefix(emits[c]) for c in concepts]   # neg: less filler = more decodable
    orc  = [hits.get(c, 0) for c in concepts]
    corr_dhat = pearson(dh, orc)
    corr_fill = pearson(fp, orc)
    beats = corr_dhat is not None and corr_fill is not None and corr_dhat > corr_fill
    strong = corr_dhat is not None and corr_dhat >= 0.5
    if strong and beats:
        verdict = f"🟢 PROXY-VALIDATED — in-engine listener surrogate d̂ predicts oracle-decodability (r={corr_dhat:.3f}) AND beats the filler_prefix degenerate baseline (r={corr_fill:.3f}) → Stage-1 .hexa (frozen-listener rerank) JUSTIFIED"
    elif strong:
        verdict = f"🟡 PROXY-CORRELATES-NOT-BETTER — d̂ r={corr_dhat:.3f} correlates but does NOT beat filler_prefix (r={corr_fill:.3f}); the lexical surrogate adds little over surface length — the real CLM-listener may still, but this $0 floor is inconclusive on the RICHER proxy's advantage"
    else:
        verdict = f"🔴 PROXY-WEAK — d̂ r={corr_dhat} below 0.5 → lexical listener surrogate does not predict decodability; needs the true CLM-listener (heavier) to decide, or the proxy hypothesis is weak"
    with open(RESULT, "w") as f:
        f.write("# H_9117 — §2 Stage-0 in-engine proxy validation ($0) — RESULT\n\n")
        f.write(f"**VERDICT: {verdict}**\n\n")
        f.write(f"- corr(d̂ lexical-contrastive-prefix, oracle-decodability) = {corr_dhat}\n")
        f.write(f"- corr(filler_prefix degenerate baseline, oracle-decodability) = {corr_fill}\n")
        f.write(f"- d̂ beats degenerate baseline: {beats} · gate corr≥0.5: {strong}\n")
        f.write(f"- oracle-decodability label = # raw short-prefix hits (t∈8,6,4,3,2) per emit, from H_9115 fixture\n")
        f.write(f"- tier=DIRECTIONAL: lexical listener is a $0 LOWER-BOUND surrogate of the CLM mouth-backend; real in-engine listener sees richer discriminability\n\n")
        f.write("## per-emit (concept · d̂ · filler_prefix · oracle-decodability)\n")
        for c in sorted(concepts, key=lambda c: -d_hat(c, emits, idf)):
            f.write(f"  {c:<12} d̂={d_hat(c,emits,idf):+7.3f}  fp={filler_prefix(emits[c]):>2}  orc_hits={hits.get(c,0)}\n")
        f.write("\nGate (fable §2 stage-0): 🟢 → Stage-1 minimal .hexa (rz_forward_model resolver + mouth-gate K-rerank). 🔴/🟡 → CLM-listener before .hexa.\n")
    print(verdict, flush=True)
    print(f"corr d̂={corr_dhat} · filler baseline={corr_fill} -> {RESULT}", flush=True)

if __name__ == "__main__":
    main()
