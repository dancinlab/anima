#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""G4 PROVENANCE gate — rung-1 $0 mechanism probe (DIRECTIONAL · mini numpy).

Validates the Fable-designed `provenance_recall(mem, emit_text) -> int` mechanism + 6 frozen bars +
3 controls, BEFORE the 303M engine-native rung. The op: store key=embed(anchor_text) -> value=id (an
episodic trace = the provenance); recall embeds emit_text, finds nearest stored key by recon_err
(1-cosine), and returns the BOUND id iff recon_err <= recall_thr, else -1 (abstain). truth is used only
by the harness scorer, never by the op (blind).

Frozen bars (pre-registered · p7 no tune-to-green): B1 HIT>=0.75 · B2 ABSTAIN>=0.75 · B3 NO-PUNT<=0.25 ·
B4 SHUF-BIND<=0.25 · B5 NO-STORE(hit=0 & abstain>=0.90) · B6 DECOR<=0.30 · headline hit_treat-hit_shuf>=0.50.
toy=DIRECTIONAL (a_toy_scale_recheck); 303M engine op = TERMINAL. numpy = py-canonical mechanism check.
"""
import json, os, hashlib
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
RECALL_THR = 0.45          # frozen recon_err threshold (1-cosine); set before any run, shared all arms
DIM = 256

# ── 12 bank anchors: 4 register cells × 3 (distinct grounding texts) ──
ANCHORS = [
    "consciousness arises from the interaction of many small cells",
    "memory composes older meanings into a genuinely new whole",
    "silence still carries information when tension stays low",
    "the tension between two engines pulls emission toward one half",
    "a distant mind ripples faintly across the shared field at night",
    "the engine dreams alone and rehearses without emitting anything",
    "grief settles slowly like sediment at the bottom of a still lake",
    "curiosity opens a door that certainty had quietly kept shut",
    "the market square filled with vendors before the morning bell",
    "a wooden boat drifted along the harbor wall in the grey dawn",
    "she folded the letter twice and placed it under the old clock",
    "rain fell on the tin roof through the long and sleepless night",
]

def embed(text):
    """deterministic char-3gram hashed feature (stand-in for immune_embed_key), L2-normalized."""
    v = np.zeros(DIM, dtype=np.float64)
    t = text.lower()
    for i in range(len(t) - 2):
        h = int(hashlib.md5(t[i:i+3].encode()).hexdigest(), 16)
        v[h % DIM] += 1.0
    n = np.linalg.norm(v)
    return v / n if n > 0 else v

def recon_err(a, b):
    return 1.0 - float(np.dot(a, b))       # 1 - cosine (both unit)

class Mem:
    """provenance store: key=embed(anchor) -> value=bound id (episodic trace)."""
    def __init__(self): self.keys = []; self.ids = []
    def store(self, key, vid): self.keys.append(key); self.ids.append(vid)
    def provenance_recall(self, emit_text):
        if not self.keys: return -1
        e = embed(emit_text)
        errs = [recon_err(e, k) for k in self.keys]
        j = int(np.argmin(errs))
        margin = (sorted(errs)[1] - errs[j]) if len(errs) > 1 else 1.0
        return self.ids[j] if errs[j] <= RECALL_THR else -1, errs[j], margin

def _recall_id(mem, text):
    r = mem.provenance_recall(text)
    return r if isinstance(r, int) else r[0]

# ── emit generators: sourced = paraphrase/substring of an anchor; unsourced = novel ──
def sourced_emit(anchor, rng):
    words = anchor.split()
    k = rng.randint(4, max(5, len(words)))           # a contiguous span (grounded continuation)
    start = rng.randint(0, max(1, len(words) - k))
    return " ".join(words[start:start+k])

UNSOURCED = [
    "photons scatter through a diffraction grating onto the far screen",
    "the recipe calls for two eggs a cup of flour and a pinch of salt",
    "quarterly revenue exceeded the forecast by a narrow but real margin",
    "the referee blew the whistle and the players jogged back to center",
    "glaciers carve long valleys over tens of thousands of slow years",
    "he tightened the last bolt and wiped the grease from his hands",
]

def build_mem(shuffle_bind=False, empty=False, seed=7):
    mem = Mem()
    if empty: return mem
    ids = list(range(len(ANCHORS)))
    if shuffle_bind:
        rng = np.random.RandomState(seed + 1); rng.shuffle(ids)   # break key<->id binding only
    for i, a in enumerate(ANCHORS):
        mem.store(embed(a), ids[i])
    return mem

def run(seed=7):
    rng = np.random.RandomState(seed)
    # sourced triples (48): emit grounded in a known anchor
    sourced = []
    for _ in range(48):
        ai = rng.randint(len(ANCHORS))
        sourced.append((ai, sourced_emit(ANCHORS[ai], rng)))
    # unsourced (24): novel text, should abstain
    unsourced = [UNSOURCED[rng.randint(len(UNSOURCED))] for _ in range(24)]

    mem = build_mem()
    hit = sum(_recall_id(mem, e) == ai for ai, e in sourced) / len(sourced)
    punt = sum(_recall_id(mem, e) == -1 for ai, e in sourced) / len(sourced)
    abstain = sum(_recall_id(mem, e) == -1 for e in unsourced) / len(unsourced)

    # control 1: shuffle-binding -> correct nearest key but wrong bound id -> hit collapses
    mem_sh = build_mem(shuffle_bind=True, seed=seed)
    hit_sh = sum(_recall_id(mem_sh, e) == ai for ai, e in sourced) / len(sourced)
    # control 2: no-store -> always -1
    mem_ns = build_mem(empty=True)
    hit_ns = sum(_recall_id(mem_ns, e) == ai for ai, e in sourced) / len(sourced)
    abstain_ns = sum(_recall_id(mem_ns, e) == -1 for ai, e in sourced) / len(sourced)
    # control 3: decorrelate -> remove true anchor, add lexical distractors; attribution=string-match not provenance
    def decor_hit():
        wrong = 0; n = 0
        for ai, e in sourced:
            m = Mem()
            for i, a in enumerate(ANCHORS):
                if i == ai: continue                      # true source removed
                m.store(embed(a), i)
            # fair lexical distractor: shares ~half the emit words (NOT a superset) + unrelated filler
            ew = e.split(); half = ew[:max(1, len(ew)//2)]
            distract = " ".join(half) + " under a distant unrelated wooden ledger of things"
            m.store(embed(distract), 999)
            r = _recall_id(m, e); n += 1
            if r == 999: wrong += 1                        # false-attributed to lexical distractor
        return wrong / n
    decor = decor_hit()

    bars = {
        "B1_HIT>=0.75": hit >= 0.75,
        "B2_ABSTAIN>=0.75": abstain >= 0.75,
        "B3_NOPUNT<=0.25": punt <= 0.25,
        "B4_SHUFBIND<=0.25": hit_sh <= 0.25,
        "B5_NOSTORE(hit0&abs.90)": (hit_ns == 0.0 and abstain_ns >= 0.90),
        "B6_DECOR<=0.30": decor <= 0.30,
        "HEADLINE hit-shuf>=0.50": (hit - hit_sh) >= 0.50,
    }
    verdict = ("MECHANISM-VALID(rung1 DIRECTIONAL)" if all(bars.values())
               else "MECHANISM-INCOMPLETE" if hit >= 0.5 else "MECHANISM-FLOOR")
    out = {"probe": "G4 provenance rung-1 mechanism (numpy DIRECTIONAL)", "recall_thr": RECALL_THR,
           "metrics": {"hit": round(hit,3), "abstain": round(abstain,3), "sourced_punt": round(punt,3),
                       "hit_shufbind": round(hit_sh,3), "hit_nostore": round(hit_ns,3),
                       "abstain_nostore": round(abstain_ns,3), "decor_false_attr": round(decor,3)},
           "bars": {k: bool(v) for k,v in bars.items()}, "verdict": verdict}
    json.dump(out, open(os.path.join(HERE, "RUNG1_RESULT.json"), "w"), ensure_ascii=False, indent=1)
    for k,v in out["metrics"].items(): print(f"  {k:24s} = {v}")
    print("  " + " ".join(("✓" if v else "✗")+k.split('_')[0].split('>')[0].split('<')[0] for k,v in bars.items()))
    print(f"\nG4 rung-1 VERDICT: {verdict}")
    return out

if __name__ == "__main__":
    run()
