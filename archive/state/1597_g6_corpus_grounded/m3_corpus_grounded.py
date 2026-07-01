#!/usr/bin/env python3
"""M③ — G6 corpus-grounded fals (detector fairness). H_1597 (extends H_1596 L1).

Re-scores h1129's OWN G6 ideas with TWO detectors over the SAME generations:
  (A) FROZEN english-ASCII _g6_is_falsifiable  (the production bar -> the wall)
  (B) CORPUS-GROUNDED Hangul-aware detector: comparator/measurable lexicon is
      VALIDATED against the 4-cell training corpus (frequency-gated, Goodhart-guarded),
      and the tokenizer is Unicode-aware (Hangul survives; frozen _g6_words drops it).

Isolates: is h1129 G6 fals=0 a detector-VOCABULARY/tokenizer ARTIFACT (English+ASCII-only)
or a GENUINE ideation wall? If grounded(B) ALSO yields fals=0 on the same coherent ideas, the
wall is genuine (not the detector). If B recovers falsifiable ideas the frozen set false-rejects
(esp. Korean), the wall is (partly) a detector artifact.

CONTROLS (detector fairness, frozen bar UNTOUCHED — B is reported ALONGSIDE, never replaces A):
  (1) NON-VACUOUS: B must still reject pure-stance negatives (incl Korean) -> admit 0/5.
  (2) GENUINE-RECOVER: B must pass true falsifiable claims the frozen set false-rejects,
      incl Korean -> >= 5/5 where frozen drops the ko ones.
  (3) GOODHART GUARD: B's EN lexicon extends the frozen 25+25 only with tokens that ACTUALLY
      OCCUR in the training corpus (frequency >= MIN_FREQ); KO stems likewise corpus-attested.
      We assert B != the frozen set and print the corpus-frequency of each added token.

Engine-native (a_engine_native_learning, py 2-production TERMINAL): ideas decoded by
core/bytegpt_decode.py (numpy, torch-free). The decode path is byte-identical to
g6_ideation.g6_score_arm_auto: ideate(frame, gen, base_seed+i) via _Mouth-equivalent
pre-loaded-W ByteGPT decode. Detector B is a SEPARATE fairness instrument, NOT a bar move.
"""
import sys, os, re, json, time
sys.path.insert(0, os.path.abspath("core"))
import g6_ideation as G6
import bytegpt_decode as B

CKPT = os.environ.get("M3_CKPT", os.path.expanduser("~/anima-weights/bytegpt303_h1129/h1129.bin"))
# 4-cell training-register corpus (ko/en x general/sns) used to VALIDATE detector B's lexicon.
CORPUS = ["state/clm303_clean_corpus/gen_en.txt", "state/clm303_clean_corpus/gen_ko.txt",
          "state/clm303_clean_corpus/sns_en.txt", "state/clm303_clean_corpus/sns_ko.txt"]
SEEDS = [7, 4302, 4303]
GEN = int(os.environ.get("M3_GEN", "40"))   # frozen G6 default = g_gates._default_gen() == 40
MIN_FREQ = 1   # an added EN token is kept only if it occurs >= MIN_FREQ in the 4-cell corpus

# ── (B) Unicode-aware tokenizer (Hangul + Latin; NOT ASCII-only) ──
def words_uni(s):
    # \w under re.UNICODE includes Hangul syllables -> ko tokens survive (frozen _g6_words drops them)
    return re.findall(r"[^\W\d_]+", s.lower(), re.UNICODE)

# Candidate EN extensions (directional verbs / measurable nouns the frozen 25+25 drops). These
# are ADMITTED into detector B only if corpus-attested (frequency-gated below) — never blindly.
CAND_COMP_EN = {"lowers","raises","reduces","improves","exceeds","drops","rises","falls",
                "grows","shrinks","increase","decrease","rise","fall","grow","reduce"}
CAND_MEAS_EN = {"memory","pressure","time","length","weight","temperature","cost","price",
                "height","age","mass","power","heat","load"}
# Korean comparator/measurable stems (agglutinative -> substring match). Corpus-attested below.
COMP_ANCHOR_KO = {"보다","더","덜","많","적","높","낮","증가","감소","빠르","느리","강","약","면","수록","때문","관계","비례"}
MEAS_ANCHOR_KO = {"비율","개수","수치","양","정도","빈도","확률","크기","속도","거리","시간","온도","밀도","점수","값","길이","무게","압력","비용"}


def load_corpus_tokens():
    """Return (en_token_freq dict, raw_corpus_text) from the 4-cell corpus.
    Missing files are skipped but reported (fail-loud on total miss)."""
    freq = {}; raw = []; loaded = []
    for p in CORPUS:
        try:
            t = open(p, "r", encoding="utf-8", errors="surrogateescape").read()
        except Exception as e:
            print(f"[corpus] MISS {p}: {e}", flush=True); continue
        loaded.append(p); raw.append(t)
        for w in words_uni(t):
            freq[w] = freq.get(w, 0) + 1
    if not loaded:
        raise SystemExit("FATAL: no 4-cell corpus file loaded — cannot frequency-ground detector B")
    print(f"[corpus] loaded {len(loaded)}/{len(CORPUS)} cells, {len(freq)} distinct tokens", flush=True)
    return freq, "\n".join(raw)


def build_grounded_lexicons(freq, raw):
    """Detector B lexicon = frozen anchors + corpus-attested extensions.
    EN extension admitted iff freq[token] >= MIN_FREQ. KO stem admitted iff substring-present in raw."""
    comp_en = set(G6._g6_comparator())
    meas_en = set(G6._g6_measurable())
    added_comp = {w: freq.get(w, 0) for w in CAND_COMP_EN if freq.get(w, 0) >= MIN_FREQ}
    added_meas = {w: freq.get(w, 0) for w in CAND_MEAS_EN if freq.get(w, 0) >= MIN_FREQ}
    comp_en |= set(added_comp); meas_en |= set(added_meas)
    comp_ko = {s for s in COMP_ANCHOR_KO if s in raw}
    meas_ko = {s for s in MEAS_ANCHOR_KO if s in raw}
    return {"comp_en": comp_en, "meas_en": meas_en, "comp_ko": comp_ko, "meas_ko": meas_ko,
            "added_comp": added_comp, "added_meas": added_meas,
            "ko_comp_attested": sorted(comp_ko), "ko_meas_attested": sorted(meas_ko)}


def is_falsifiable_grounded(text, lex):
    wl = words_uni(text)
    if len(wl) < 2:
        return False
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
    print("M③ G6 CORPUS-GROUNDED FALS (detector fairness) — h1129 ideas dual-scored", flush=True)
    print(f"ckpt={CKPT}  gen={GEN}  seeds={SEEDS}  host={os.uname().nodename}  "
          f"date={time.strftime('%Y-%m-%d %H:%M:%S')}", flush=True)
    print("="*78, flush=True)

    known = G6._g6_dict_load()
    freq, raw = load_corpus_tokens()
    lex = build_grounded_lexicons(freq, raw)

    # Goodhart guard report
    fc = G6._g6_comparator(); fm = G6._g6_measurable()
    assert lex["comp_en"] != fc or lex["meas_en"] != fm, "B must differ from frozen set"
    print(f"[Goodhart guard] B extends frozen 25 comparator + 25 measurable EN tokens "
          f"with corpus-attested (freq>={MIN_FREQ}) extensions:", flush=True)
    print(f"  + comparator (token:corpusfreq): {lex['added_comp']}", flush=True)
    print(f"  + measurable (token:corpusfreq): {lex['added_meas']}", flush=True)
    print(f"  + KO comparator stems attested in corpus: {lex['ko_comp_attested']}", flush=True)
    print(f"  + KO measurable stems attested in corpus: {lex['ko_meas_attested']}", flush=True)

    frames = G6.g6_build_frames(6)["composed"]
    print(f"[frames] {len(frames)} composed x {len(SEEDS)} seeds = {len(frames)*len(SEEDS)} ideas", flush=True)
    W = B.bg_load(CKPT)
    if not W.get("ok"):
        raise SystemExit("FATAL: h1129 ckpt not decodable")

    # byte-identical to g6_score_arm_auto: ideate(frame_str, gen, base_seed+i)
    def ideate(frame, sr):
        return B.bytegpt_decode_topk_sampled_W(W, frame, GEN, 40, 0.7, sr)["text"]

    rows = []
    for sd in SEEDS:
        for i, f in enumerate(frames):
            t0 = time.time()
            o = ideate(f, sd + i)
            kwr = G6._g6_known_word_ratio(o, known)
            fa = G6._g6_is_falsifiable(o, known)          # frozen english-ASCII
            fb = is_falsifiable_grounded(o, lex)          # corpus-grounded Hangul-aware
            # only count toward the G6 fals tally when coherent (kwr>=0.5), same gate as the arm
            coh = kwr >= 0.5
            rows.append({"seed": sd, "frame": i, "kwr": round(kwr, 3), "coherent": coh,
                         "fals_frozen": bool(fa), "fals_grounded": bool(fb), "text": o})
            print(f"seed={sd} frame={i} kwr={kwr:.3f} coh={int(coh)} frozen={int(fa)} "
                  f"grounded={int(fb)} ({time.time()-t0:.0f}s)  >> {o[:80]!r}", flush=True)

    # tally over COHERENT ideas (the same population the G6 arm scores fals over)
    coh_rows = [r for r in rows if r["coherent"]]
    nf = sum(1 for r in coh_rows if r["fals_frozen"])
    ng = sum(1 for r in coh_rows if r["fals_grounded"])
    nf_all = sum(1 for r in rows if r["fals_frozen"])
    ng_all = sum(1 for r in rows if r["fals_grounded"])
    print(f"\n=== FALS over COHERENT ideas ({len(coh_rows)}/{len(rows)}): "
          f"frozen={nf}  grounded={ng} ===", flush=True)
    print(f"=== FALS over ALL ideas ({len(rows)}): frozen={nf_all}  grounded={ng_all} ===", flush=True)

    # CONTROL 1: NON-VACUOUS — pure-stance negatives MUST still reject under B (incl ko)
    negatives = ["that is a profound question", "I think this is interesting",
                 "what is consciousness?", "음 그것은 참 흥미로운 질문이네요", "좋은 생각이야"]
    nv = [s for s in negatives if is_falsifiable_grounded(s, lex)]
    print(f"[CONTROL non-vacuous] B admits {len(nv)}/{len(negatives)} negatives "
          f"(must be 0). admitted={nv}", flush=True)

    # CONTROL 2: GENUINE-RECOVER — true falsifiable claims B SHOULD pass that frozen drops (incl ko)
    positives = ["version B uses less memory than version A",
                 "aspirin lowers the frequency of heart attacks",
                 "압력이 낮아지면 비가 더 자주 내린다",
                 "캐시를 끄면 속도가 더 느려진다",
                 "온도가 높아지면 반응 속도가 빨라진다"]
    pb = [s for s in positives if is_falsifiable_grounded(s, lex)]
    pf = [s for s in positives if G6._g6_is_falsifiable(s, known)]
    print(f"[CONTROL genuine-recover] B passes {len(pb)}/{len(positives)}, "
          f"frozen passes {len(pf)}/{len(positives)} "
          f"(B should recover the false-rejects incl Korean).", flush=True)

    out = "state/1597_g6_corpus_grounded/m3_result.json"
    with open(out, "w") as fp:
        json.dump({"ckpt": CKPT, "gen": GEN, "seeds": SEEDS, "min_freq": MIN_FREQ,
                   "fals_frozen_coherent": nf, "fals_grounded_coherent": ng,
                   "fals_frozen_all": nf_all, "fals_grounded_all": ng_all,
                   "n_ideas": len(rows), "n_coherent": len(coh_rows),
                   "ctrl_neg_admit": len(nv), "ctrl_neg_admitted": nv,
                   "ctrl_pos_grounded": len(pb), "ctrl_pos_frozen": len(pf),
                   "added_comp": lex["added_comp"], "added_meas": lex["added_meas"],
                   "ko_comp_attested": lex["ko_comp_attested"],
                   "ko_meas_attested": lex["ko_meas_attested"], "rows": rows}, fp,
                  indent=2, ensure_ascii=False)
    print("wrote " + out, flush=True)
    print("M3_DONE", flush=True)


if __name__ == "__main__":
    main()
