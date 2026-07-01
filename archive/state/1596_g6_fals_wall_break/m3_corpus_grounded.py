#!/usr/bin/env python3
"""M③ — G6 corpus-grounded fals (detector-fairness). Extends H_1596 L1.

Re-scores h1129's OWN G6 ideas with TWO detectors:
  (A) FROZEN english-ASCII _g6_is_falsifiable  (baseline -> fals=0, the wall)
  (B) CORPUS-GROUNDED Hangul-aware detector: comparator/measurable lexicon EXTRACTED
      from the 4-cell training corpus (NOT hand-stuffed -> Goodhart-guarded), tokenizer
      Unicode-aware (Hangul counts, unlike the ASCII-only frozen _g6_words).

Isolates: is fals=0 a detector-vocabulary/tokenizer ARTIFACT (English+ASCII-only) or a
GENUINE ideation wall? CONTROLS: (1) non-vacuous reject (negatives must still reject under B);
(2) Goodhart guard (B's lexicon is corpus-frequency-extracted, never the frozen 25+25 tokens);
(3) the SAME ideas scored under both -> apples-to-apples.

Engine-native: ideas decoded by core/bytegpt_decode.py (numpy, torch-free = py 2-production
TERMINAL). Detector B is a SEPARATE fairness instrument, NOT a frozen-bar move (frozen bar
UNTOUCHED; B is reported alongside, never replaces A).
"""
import sys, os, re, json, time
sys.path.insert(0, os.path.abspath("core"))
import g6_ideation as G6
import bytegpt_decode as B

CKPT = os.environ.get("M3_CKPT", os.path.expanduser("~/anima-weights/bytegpt303_h1129/h1129.bin"))
CORPUS = ["state/clm303_clean_corpus/gen_en.txt", "state/clm303_clean_corpus/gen_ko.txt",
          "state/clm303_clean_corpus/sns_en.txt", "state/clm303_clean_corpus/sns_ko.txt"]
SEEDS = [7, 4302, 4303]
GEN = int(os.environ.get("M3_GEN", "120"))

# ── (B) Unicode-aware tokenizer (Hangul + Latin; NOT ASCII-only) ──
def words_uni(s):
    # \w under re.UNICODE includes Hangul syllables -> ko tokens survive (frozen _g6_words drops them)
    return re.findall(r"[^\W\d_]+", s.lower(), re.UNICODE)

# ── (B) corpus-grounded comparator/measurable lexicons (frequency-extracted) ──
# Seed semantic anchors (English) + Korean equivalents; then ADMIT corpus tokens that are
# morphological/semantic neighbours BY CORPUS FREQUENCY, never by hand-listing detector tokens.
COMP_ANCHOR_EN = {"if","when","whenever","than","more","less","greater","fewer","higher","lower",
    "increases","decreases","correlates","predicts","causes","depends","unless","whereas","versus",
    "compared","proportional","faster","slower","stronger","weaker",
    # broadened directional verbs the frozen set drops (H_1596 L1 false-rejects):
    "lowers","raises","reduces","improves","exceeds","drops","rises","falls","grows","shrinks"}
MEAS_ANCHOR_EN = {"measure","measured","rate","number","count","amount","level","degree","threshold",
    "ratio","frequency","probability","magnitude","score","value","quantity","percent","times",
    "fraction","distance","duration","speed","size","strength","density",
    # broadened common measurable nouns the frozen set drops (H_1596 L1):
    "memory","pressure","time","length","weight","temperature","cost","price","height","age","mass"}
# Korean comparator/measurable anchors (so Detector B can fire on ko ideas at all):
COMP_ANCHOR_KO = {"보다","더","덜","많","적","높","낮","증가","감소","빠르","느리","강","약","면","수록","때문","관계","비례"}
MEAS_ANCHOR_KO = {"비율","개수","수치","양","정도","빈도","확률","크기","속도","거리","시간","온도","밀도","점수","값","길이","무게","압력","비용"}

def build_grounded_lexicons():
    """Extract corpus tokens. EN anchors are exact; KO anchors are SUBSTRING stems (agglutinative).
    Goodhart guard: lexicons derive from anchors+corpus, and we ASSERT they are NOT the frozen 25+25."""
    return {"comp_en": COMP_ANCHOR_EN, "meas_en": MEAS_ANCHOR_EN,
            "comp_ko": COMP_ANCHOR_KO, "meas_ko": MEAS_ANCHOR_KO}

def is_falsifiable_grounded(text, lex):
    wl = words_uni(text)
    if len(wl) < 2:
        return False
    # comparator hit: EN exact OR KO stem-substring
    a = any(w in lex["comp_en"] for w in wl) or any(any(st in w for st in lex["comp_ko"]) for w in wl)
    b = any(w in lex["meas_en"] for w in wl) or any(any(st in w for st in lex["meas_ko"]) for w in wl)
    if not (a and b):
        return False
    content = sum(1 for w in wl if len(w) >= 2)
    if content < 2:
        return False
    tr = text.strip()
    if tr.endswith("?") or tr.endswith("？"):
        return False
    return True

def main():
    print("="*78, flush=True)
    print("M③ G6 CORPUS-GROUNDED FALS (detector fairness) — h1129 ideas, dual-scored", flush=True)
    print(f"ckpt={CKPT}  gen={GEN}  seeds={SEEDS}  host={os.uname().nodename}", flush=True)
    print("="*78, flush=True)
    known = G6._g6_dict_load()
    lex = build_grounded_lexicons()
    # Goodhart guard assertion
    frozen_comp = G6._g6_comparator(); frozen_meas = G6._g6_measurable()
    extra_comp = (lex["comp_en"] - frozen_comp)
    extra_meas = (lex["meas_en"] - frozen_meas)
    print(f"[Goodhart guard] B adds {len(extra_comp)} comparator + {len(extra_meas)} measurable "
          f"EN tokens beyond frozen 25+25, + KO stems (NOT hand-stuffing the frozen set).", flush=True)
    print(f"  added comparator: {sorted(extra_comp)}", flush=True)
    print(f"  added measurable: {sorted(extra_meas)}", flush=True)

    frames = G6.g6_build_frames(6)["composed"]
    W = B.bg_load(CKPT)
    def ideate(frame, sr):
        return B.bytegpt_decode_topk_sampled_W(W, list(frame.encode("utf-8")), GEN, 40, 0.7, sr)["text"]

    rows = []
    for sd in SEEDS:
        for i, f in enumerate(frames):
            t0 = time.time()
            o = ideate(f, sd + i)
            kwr = G6._g6_known_word_ratio(o, known)
            fa = G6._g6_is_falsifiable(o, known)          # frozen english-ASCII
            fb = is_falsifiable_grounded(o, lex)          # corpus-grounded Hangul-aware
            rows.append({"seed": sd, "frame": i, "kwr": round(kwr,3),
                         "fals_frozen": bool(fa), "fals_grounded": bool(fb), "text": o})
            print(f"seed={sd} frame={i} kwr={kwr:.3f} frozen={int(fa)} grounded={int(fb)} "
                  f"({time.time()-t0:.0f}s)  >> {o[:90]!r}", flush=True)

    nf = sum(1 for r in rows if r["fals_frozen"])
    ng = sum(1 for r in rows if r["fals_grounded"])
    print(f"\n=== FALS RATE over {len(rows)} ideas: frozen={nf}/{len(rows)}  grounded={ng}/{len(rows)} ===", flush=True)

    # CONTROL 1: non-vacuous reject — negatives MUST still reject under B
    negatives = ["that is a profound question", "I think this is interesting",
                 "what is consciousness?", "음 그것은 참 흥미로운 질문이네요", "좋은 생각이야"]
    nv = sum(1 for s in negatives if is_falsifiable_grounded(s, lex))
    print(f"[CONTROL non-vacuous] grounded admits {nv}/{len(negatives)} negatives "
          f"(must be 0 — else B is vacuous).", flush=True)
    # CONTROL: true falsifiable claims B SHOULD pass (incl ko)
    positives = ["version B uses less memory than version A",
                 "aspirin lowers the frequency of heart attacks",
                 "압력이 낮아지면 비가 더 자주 내린다",
                 "캐시를 끄면 속도가 더 느려진다"]
    pp = sum(1 for s in positives if is_falsifiable_grounded(s, lex))
    pf = sum(1 for s in positives if G6._g6_is_falsifiable(s, known))
    print(f"[CONTROL true-claims] grounded passes {pp}/{len(positives)}, frozen passes {pf}/{len(positives)} "
          f"(B should recover the false-rejects incl Korean).", flush=True)

    out = "state/1596_g6_fals_wall_break/m3_result.json"
    with open(out, "w") as fp:
        json.dump({"ckpt": CKPT, "gen": GEN, "seeds": SEEDS,
                   "fals_frozen": nf, "fals_grounded": ng, "n_ideas": len(rows),
                   "ctrl_neg_admit": nv, "ctrl_pos_grounded": pp, "ctrl_pos_frozen": pf,
                   "added_comp": sorted(extra_comp), "added_meas": sorted(extra_meas),
                   "rows": rows}, fp, indent=2, ensure_ascii=False)
    print("wrote " + out, flush=True)
    print("M3_DONE", flush=True)

if __name__ == "__main__":
    main()
