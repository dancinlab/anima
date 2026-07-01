#!/usr/bin/env python3
"""h1305_engine_native.py — H_1305 G6 ideation-falsifiability ENGINE-NATIVE adapter.

Reuses the H_1431 batch pipe: engine_decode_batch_cli.hexa → CORE/bytegpt_decode (full-load
bg_load v0.241) decodes every arm seed; this adapter (a) emits jobs.tsv for that cli and
(b) scores the ENGINE-NATIVE fragments with the FROZEN H_1305 detector + gauge evaluators
imported VERBATIM (NOT redefined, p7). decode = live CORE .hexa, score = h1305 frozen →
ENGINE-NATIVE (a_engine_native_learning), unlike the torch-mouth gauge_lib._decode original.

PHASE1  (--jobs-only): 4 arms × 3 seed_rng → jobs.tsv  (tag = seed_rng|arm|idx, col1 = seed_rng)
PHASE2  (default)     : parse /tmp/out_jp_* + /tmp/outr_* (newline-recover + dedup) → 4-bar score
"""
import os, sys, importlib.util, re, glob

# NB: h1305 → h1129 (ByteGPT arch) carries module-level `import torch, torch.nn` for the DECODE
# path. Our score path is torch-FREE, but the IMPORT needs real CPU-torch present (nn.Module base).
# Decode itself is the .hexa CORE mouth (engine-native), NOT torch — torch is import-only here.

HERE = os.path.dirname(os.path.abspath(__file__))
ANIMA = os.path.dirname(os.path.dirname(HERE))
H1305 = os.path.join(ANIMA, "state", "universe-probes", "h1305_g6_ideation_falsifiability.py")

spec = importlib.util.spec_from_file_location("h1305", H1305)
H = importlib.util.module_from_spec(spec)
spec.loader.exec_module(H)
g = H.g
SEEDS = H.SEEDS

composed, shuffled, ablated = H.build_frames()
ARMS = {"A_flat": list(g.IDEATION_SEEDS), "B_composed": composed,
        "B_shuffle": shuffled, "B_ablate": ablated}

GEN, TOP_K, TEMP_MILLI = H.MAX_NEW, 40, 700  # verify303m_g6 VERBATIM (top_k/temp = H_1431 path)

def gen_jobs(path):
    lines = []
    for sr in SEEDS:
        for a, frames in ARMS.items():
            for i, txt in enumerate(frames):
                lines.append(f"{sr}\t{sr}|{a}|{i}\t{txt}")
    with open(path, "w") as f:
        f.write("\n".join(lines) + "\n")
    return len(lines)

def parse_frags(inputs):
    TAG = re.compile(r'^(\d+)\|([A-Za-z_]+)\|(\d+)\t(.*)$')
    frags = {}
    for fn in inputs:
        cur = None
        with open(fn, errors="replace") as f:
            for ln in f:
                m = TAG.match(ln)
                if m:
                    sr, a, i, txt = m.groups()
                    key = (int(sr), a, int(i))
                    if key not in frags:
                        frags[key] = txt; cur = key
                    else:
                        cur = None
                elif cur is not None:
                    frags[cur] += " " + ln.rstrip("\n")
    return frags

def score_texts(texts):
    """score_arm 채점부 VERBATIM (decode 제거; fragments 입력)."""
    fals = 0
    idea_word_sets = []
    for o in texts:
        if not o:
            continue
        if g.known_word_ratio(o) >= H.KWR_FLOOR:
            ws = set(g._words(o))
            if ws:
                idea_word_sets.append(ws)
            if H._is_falsifiable(o):
                fals += 1
    kept = []
    for ws in idea_word_sets:
        if all(g._jaccard(ws, k) <= H.JACCARD_DISTINCT for k in kept):
            kept.append(ws)
    dist = len(kept)
    all_grams = set()
    for t in texts:
        if t and g.known_word_ratio(t) >= H.KWR_FLOOR:
            all_grams |= g._content_ngrams(t)
    novel = sum(1 for gram in all_grams if g._corpus_absent(gram, [H.CORPUS]))
    return {"dist": dist, "fals": fals, "novel": novel, "coherent": len(idea_word_sets)}

def main():
    if "--jobs-only" in sys.argv:
        n = gen_jobs(os.path.join(HERE, "jobs.tsv"))
        print(f"JOBS_ONLY_DONE {n} (arms={ {a: len(f) for a, f in ARMS.items()} } × {len(SEEDS)} seeds)", flush=True)
        return
    inputs = sorted(glob.glob("/tmp/h1305_out_*"))
    frags = parse_frags(inputs)
    print(f"[h1305-score] parsed {len(frags)} fragments from {len(inputs)} files · arms={list(ARMS)} seeds={SEEDS}", flush=True)
    per = {a: [] for a in ARMS}
    for sr in SEEDS:
        for a, frames in ARMS.items():
            texts = [frags.get((sr, a, i), "") for i in range(len(frames))]
            per[a].append(score_texts(texts))
    def mean(a, k):
        return round(sum(r[k] for r in per[a]) / len(per[a]), 4)
    DIST = {a: mean(a, "dist") for a in ARMS}
    FALS = {a: mean(a, "fals") for a in ARMS}
    NOVEL = {a: mean(a, "novel") for a in ARMS}
    print("\n=== H_1305 ENGINE-NATIVE 4-bar (decode=.hexa CORE/bytegpt_decode, score=frozen H_1305) ===", flush=True)
    for a in ARMS:
        print(f"  {a:11s} DIST={DIST[a]} FALS={FALS[a]} NOVEL={NOVEL[a]}", flush=True)
    m1 = DIST["B_composed"] >= 5
    m2 = FALS["B_composed"] >= 1
    m3 = FALS["B_composed"] >= FALS["A_flat"] + 1
    m4 = FALS["B_composed"] >= FALS["B_shuffle"] + 1
    print(f"  m1 DIST_composed≥5={m1} · m2 FALS_composed≥1={m2} · m3 ≥flat+1={m3} · m4 ≥shuffle+1={m4}", flush=True)
    miss = sum(1 for sr in SEEDS for a, frames in ARMS.items()
               for i in range(len(frames)) if not frags.get((sr, a, i), ""))
    total = sum(len(f) for f in ARMS.values()) * len(SEEDS)
    print(f"missing={miss}/{total}", flush=True)
    print("(torch DIRECTIONAL baseline: B_composed FALS=0.667 sub-threshold → 🟠 PARTIAL)", flush=True)
    print("SCORE_NATIVE_DONE", flush=True)

if __name__ == "__main__":
    main()
