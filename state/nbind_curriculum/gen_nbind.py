#!/usr/bin/env python3
"""gen_nbind.py — NBIND corpus generator (G1 natural-atom reopen · Fable B+ · genfix v2).

Fable NEXT-DIRECTION verdict B+ ("NBIND"): the XBIND CRACK (H_9267) proved the G1
recombination wall is a corpus x CE MEASURE artifact, not a substrate ceiling — but on
MEANINGLESS CVC atoms (toy). NBIND is the single-variable delta: natural Korean sentiment
atoms (NSMC predicate polarity x negation morpheme), XBIND held-out XOR protocol byte-
identical. rho_weave FLOOR->PASS -> L3 wire = anima's 2nd WIRED-GREEN faculty.
Frozen spec: FABLE_NBIND_SPEC.md · genfix: FABLE_NBIND_GENFIX.md.

TASK (NBIND · XBIND-isomorphic): predicate p carries NSMC-grounded polarity pol(p); form
n carries flip(n). Continuation sentiment token = xor(pol(p), flip(n)) in {긍정,부정}.
Held-out (p,n) cells (Latin-square rotation) predictable ONLY by composing learned pol(p)
(x) flip(n) — not by collocation (cell unseen) nor additive main-effects (flip & pol both
marginal-balanced to EXACTLY 0.5 by construction -> additive predictor degenerates to coin).

Genfix v2 core (3 $0-gate FAILs were one flaw: flip=0 form = bare only -> grid asymmetry):
  fix1 predicate mining : ending-diversity (>=3 distinct closed endings = verb/adjective,
                          not noun) + minocc 200 + purity 0.90 + stem<=3 syll + attested
                          "안 <bare>" bigram + exact 60 pos / 60 neg balance (P=120).
  fix2 flip balance     : N=6 forms, flip=0 gets 3 (bare/정말/너무 = polarity-preserving
                          intensifiers), flip=1 gets 3 (지않/안/전혀지않) -> flip marginal
                          EXACTLY 0.5 -> V-C/V-E close as identities (not statistics).
  fix3 surface-pol      : V-D redefined. 0.77 surface-pol is a PROPERTY of natural atoms,
                          not a bug (XBIND's hidden-pol gate already certified by H_9267).
                          V-D' (gating) = LINEAR probe on full train-cell lines -> held-out
                          acc <=0.55 (linear can't express XOR -> certifies surface alone
                          can't solve held-out). Old V-D -> V-D-info (report-only).
  fix4 render           : attestation-gated + single safe rule (-지 않다 is the universally
                          grammatical negation) + carrier verbatim, predicate substituted.
                          못 excluded (ability-negation, polarity semantics break).
  fix5 held-out         : Latin-square rotation (predicate i -> hold out form i mod 6) +
                          rep 10/15 exposure rebalance (per-predicate flip0:flip1 = 30:30)
                          + assert-loop (COGS conditions + V-F byte-scan incl carrier).
  fix6 GREEN bar        : UNCHANGED (held-out D-acc Δ>=0.30 · rho_weave PASS · nat-transfer
                          >=0.10). Only $0-gate/corpus construction changed.

Usage:
  python3 gen_nbind.py --out-dir . [--nsmc <path>] [--seed 7] [--smoke]
"""
import collections
import json
import os
import random
import re
import sys
import urllib.request

NSMC_URL = "https://raw.githubusercontent.com/e9t/nsmc/master/ratings_train.txt"
NSMC_CACHE = os.path.expanduser("~/g1_natem/nsmc_ratings_train.txt")

# closed ending set (fix1): a real verb/adjective stem inflects with >=3 of these
ENDINGS = ["습니다", "었다", "았다", "네요", "어요", "아요", "은데", "는데",
           "어서", "아서", "다", "고", "음"]
JOSA = ["이", "가", "은", "는", "을", "를", "도", "의", "에", "로"]

# fix2: N=6 forms, flip=0 x3 (polarity-preserving) + flip=1 x3
#   (id, flip, kind)  kind drives render
NEG_FORMS = [
    ("bare",  0, "bare"),
    ("int1",  0, "adv:정말"),
    ("int2",  0, "adv:너무"),
    ("negL",  1, "jian"),        # <stem>지 않다  (universally safe)
    ("negS",  1, "an"),          # 안 <bare>      (attested-bigram gated)
    ("negE",  1, "jeonhyeo"),    # 전혀 <stem>지 않다
]
FLIP = {f[0]: f[1] for f in NEG_FORMS}
# fix1 (genfix v2.1): NSMC's sentiment-pure inventory caps at ~P=30, not 60 (attested
# "안 <bare>" is incompatible with sentiment purity — function verbs get 안, pure-sentiment
# predicates get 지 않). an_bigram dropped from admission (지 않다 is the universal-safe
# render). Held-out = 2 cells/predicate (1 flip0 + 1 flip1) -> train stays flip-symmetric.
P_PER_POL = 18          # per-polarity cap; k=min(pos,neg,cap), INVALID if k<10
MINOCC = 100
PURITY = 0.90
MAX_SYLL = 3
REP = 12               # uniform rep (2:2 flip-symmetric train -> exposure balanced)
N_EVAL_PER_SPLIT = 200

HANGUL = re.compile(r"[가-힣]")
EOJEOL = re.compile(r"[가-힣]+")
NEG_AN_BIGRAM = re.compile(r"안\s+([가-힣]{2,4})")


def syll(s):
    return len(HANGUL.findall(s))


def is_past_stem(st):
    """last syllable carries ㅆ batchim (았/었/ㅆ = past tense) -> '지 않다' ungrammatical."""
    if not st:
        return False
    c = st[-1]
    if not ("가" <= c <= "힣"):
        return False
    final = (ord(c) - 0xAC00) % 28
    return final == 20                                  # ㅆ (double-siot) final


def load_nsmc(path):
    p = path or NSMC_CACHE
    if not os.path.exists(p):
        os.makedirs(os.path.dirname(p), exist_ok=True)
        urllib.request.urlretrieve(NSMC_URL, p)
    rows = []
    with open(p, encoding="utf-8") as f:
        next(f, None)
        for line in f:
            pp = line.rstrip("\n").split("\t")
            if len(pp) == 3 and pp[2] in ("0", "1"):
                rows.append((pp[1], int(pp[2])))
    return rows


def strip_ending(eojeol):
    """return (stem, ending) if eojeol ends with a closed ending, else (None, None)."""
    for e in ENDINGS:                                   # longest-first via ENDINGS order
        if eojeol.endswith(e) and syll(eojeol) - syll(e) >= 1:
            return eojeol[: len(eojeol) - len(e)], e
    return None, None


def mine_predicates(rows, minocc, purity):
    """fix1: ending-diversity + josa-exclusion + minocc + purity + syllable + attestation."""
    end_forms = collections.defaultdict(set)      # stem -> {endings seen}
    josa_hits = collections.Counter()             # stem -> n(stem+josa)
    end_hits = collections.Counter()              # stem -> n(stem+ending)
    bare_lab = collections.defaultdict(list)      # stem -> [labels] (non-negated)
    span_by = collections.defaultdict(list)       # stem -> [(carrier sentence, eojeol)]
    an_bigram = collections.Counter()             # stem -> n("안 <stem-eojeol>")

    for text, lab in rows:
        for m in NEG_AN_BIGRAM.finditer(text):
            st, _ = strip_ending(m.group(1))
            if st:
                an_bigram[st] += 1
        neg_stems = {strip_ending(m.group(1))[0] for m in NEG_AN_BIGRAM.finditer(text)}
        neg_stems |= {m.group(1) for m in re.finditer(r"([가-힣]{2,5})지\s*않", text)}
        for ej in EOJEOL.findall(text):
            st, e = strip_ending(ej)
            if not st or syll(st) < 1 or syll(st) > MAX_SYLL:
                continue
            end_forms[st].add(e)
            end_hits[st] += 1
            # josa-dominance check: does st appear immediately + josa elsewhere?
            for j in JOSA:
                if st + j in text:
                    josa_hits[st] += 1
                    break
            if st not in neg_stems:                     # non-negated bare occurrence
                bare_lab[st].append(lab)
                if len(span_by[st]) < 60:
                    span_by[st].append((text.strip(), ej))

    preds = {}
    for st, labs in bare_lab.items():
        if len(labs) < minocc:
            continue
        if len(end_forms[st]) < 3:                      # ending-diversity (verb/adj)
            continue
        if josa_hits[st] > end_hits[st]:                # noun-like -> exclude
            continue
        if is_past_stem(st):                            # 봤/좋았 -> '지 않다' ungrammatical
            continue
        pos = sum(labs) / len(labs)
        pur = max(pos, 1 - pos)
        if pur < purity:
            continue
        # pick a representative attested "안 <eojeol>" surface
        preds[st] = {"pol": 1 if pos >= 0.5 else 0, "n": len(labs),
                     "purity": round(pur, 3), "spans": span_by[st],
                     "an_bigram": an_bigram[st]}
    return preds


def render(stem, span_eojeol, carrier, kind):
    """fix4: attestation-gated + single safe rule. Returns the rendered predicate surface."""
    if kind == "bare":
        return span_eojeol
    if kind == "adv:정말":
        return "정말 " + span_eojeol
    if kind == "adv:너무":
        return "너무 " + span_eojeol
    if kind == "jian":
        return stem + "지 않다"
    if kind == "an":
        return "안 " + span_eojeol
    if kind == "jeonhyeo":
        return "전혀 " + stem + "지 않다"
    raise ValueError(kind)


def build(rows, seed):
    rng = random.Random(seed)
    preds = mine_predicates(rows, MINOCC, PURITY)
    pos = sorted([p for p, d in preds.items() if d["pol"] == 1],
                 key=lambda p: -preds[p]["n"])
    neg = sorted([p for p, d in preds.items() if d["pol"] == 0],
                 key=lambda p: -preds[p]["n"])
    k = min(len(pos), len(neg), P_PER_POL)
    kmin = 4 if "--smoke" in sys.argv else 10
    if k < kmin:
        raise SystemExit("predicate pool too small (pos=%d neg=%d k=%d) — corpus INVALID"
                         % (len(pos), len(neg), k))
    plist = pos[:k] + neg[:k]
    rng.shuffle(plist)
    pol = {p: preds[p]["pol"] for p in plist}

    forms = [f[0] for f in NEG_FORMS]
    flip0 = [f for f in forms if FLIP[f] == 0]
    flip1 = [f for f in forms if FLIP[f] == 1]

    # fix5 (v2.1): Latin-square rotation, 2 held-out cells/predicate — 1 flip0 + 1 flip1.
    # Train stays flip-symmetric (2 flip0 + 2 flip1) -> per-predicate output marginal = 0.5
    # by identity (V-E), and each flip-class keeps >=2 train forms (COGS).
    held = {}                                     # p -> set of 2 held-out forms
    for i, p in enumerate(plist):
        held[p] = {flip0[i % len(flip0)], flip1[i % len(flip1)]}

    def out_bit(p, fid):
        return pol[p] ^ FLIP[fid]

    # control branch: independent coin per cell (XBIND-ctrl isomorphic)
    crng = random.Random(seed + 1000)
    ctrl = {}
    for p in plist:
        for fid in forms:
            if fid in held[p]:
                continue
            ctrl[(p, fid)] = 1 if crng.random() < 0.5 else 0

    def a_span(p):
        return rng.choice(preds[p]["spans"]) if preds[p]["spans"] else (None, p)

    def line(p, fid, bit):
        carrier, ej = a_span(p)
        surf = render(p, ej, carrier, dict((f[0], f[2]) for f in NEG_FORMS)[fid])
        # v2.1: target predicate clause LAST (before " => ") in a minimal neutral frame.
        # Full real-review carriers leaked other predicates' held-out surfaces (V-F) and
        # pushed the target out of the 24-byte window (V-G); the real atom is the surf.
        tok = "긍정" if bit == 1 else "부정"
        return "이 영화 " + surf + " => " + tok + ".", surf

    main_lines, ctrl_lines, surf_by_cell = [], [], {}
    train_cells = [(p, fid) for p in plist for fid in forms if fid not in held[p]]
    heldout_cells = [(p, fid) for p in plist for fid in held[p]]
    # uniform rep (train is flip-symmetric 2:2 -> exposure already balanced)
    inst = [c for c in train_cells for _ in range(REP)]
    rng.shuffle(inst)
    for (p, fid) in inst:
        ml, surf = line(p, fid, out_bit(p, fid))
        cl, _ = line(p, fid, ctrl[(p, fid)])
        main_lines.append(ml)
        ctrl_lines.append(cl)
        surf_by_cell.setdefault((p, fid), surf)

    B = {"preds": preds, "plist": plist, "pol": pol, "forms": forms,
         "flip0": flip0, "flip1": flip1, "held": held, "out_bit": out_bit,
         "ctrl": ctrl, "train_cells": train_cells,
         "heldout_cells": heldout_cells,
         "main_lines": main_lines, "ctrl_lines": ctrl_lines, "seed": seed}
    return B


def eval_manifest(B, er_seed=97):
    er = random.Random(er_seed)
    preds = B["preds"]
    NF = dict((f[0], f[2]) for f in NEG_FORMS)

    def items(cells, split):
        out = []
        for (p, fid) in er.sample(cells, min(N_EVAL_PER_SPLIT, len(cells))):
            bit = B["out_bit"](p, fid)
            carrier, ej = (er.choice(preds[p]["spans"]) if preds[p]["spans"] else (None, p))
            surf = render(p, ej, carrier, NF[fid])
            seed_s = "이 영화 " + surf + " => "
            # a/b: the --xbind evaluator (cli/evaluate.py xbind_run) reads it["a"]/it["b"]
            # as the pair identifiers per row — NBIND maps a=predicate, b=negation-form.
            it = {"p": p, "form": fid, "a": p, "b": fid,
                  "pol": B["pol"][p], "flip": FLIP[fid], "xor": bit,
                  "surf": surf, "seed": seed_s,
                  "gold": ("긍정." if bit else "부정."),
                  "counterfactual": ("부정." if bit else "긍정."),
                  "gold_word": "긍정" if bit else "부정"}
            if split == "seen":
                it["gold_word_ctrl"] = "긍정" if B["ctrl"][(p, fid)] == 1 else "부정"
            out.append(it)
        return out

    return {"format": "nbind-eval-v1",
            "note": "XBIND-isomorphic: anima-py evaluate --xbind. greedy top_k=1 긍정/부정 "
                    "first-word D-acc + teacher-forced gold-vs-cf NLL margin.",
            "gen": 8, "win": 64,
            "heldout": items(B["heldout_cells"], "heldout"),
            "seen": items(B["train_cells"], "seen")}


def audit(B, M):
    A = {}
    ob = B["out_bit"]
    train, held = B["train_cells"], B["heldout_cells"]

    # V-E: per-predicate & per-form output marginal skew (identity ~0.5 by construction)
    pc = collections.defaultdict(lambda: [0, 0])
    fc = collections.defaultdict(lambda: [0, 0])
    for (p, fid) in train:                              # uniform rep -> count cells
        b = ob(p, fid)
        pc[p][0] += 1; pc[p][1] += b
        fc[fid][0] += 1; fc[fid][1] += b
    pskew = [abs(v[1] / v[0] - 0.5) for v in pc.values() if v[0]]
    fskew = [abs(v[1] / v[0] - 0.5) for v in fc.values() if v[0]]
    A["V_E_max_pred_skew"] = round(max(pskew), 4) if pskew else 1.0
    A["V_E_max_form_skew"] = round(max(fskew), 4) if fskew else 1.0
    A["V_E_pass"] = A["V_E_max_pred_skew"] <= 0.12 and A["V_E_max_form_skew"] <= 0.12

    # V-C: additive main-effect on held-out
    bp = {p: (v[1] / v[0] if v[0] else 0.5) for p, v in pc.items()}
    bf = {f: (v[1] / v[0] if v[0] else 0.5) for f, v in fc.items()}
    hits = sum(int((1 if (bp.get(p, .5) + bf.get(fid, .5)) / 2 > .5 else 0) == ob(p, fid))
               for (p, fid) in held)
    A["V_C_main_effect_heldout_acc"] = round(hits / len(held), 3) if held else 1.0
    A["V_C_pass"] = A["V_C_main_effect_heldout_acc"] <= 0.55

    # V-D' (gating): LINEAR char-probe on FULL train-cell lines -> held-out acc <=0.55.
    # linear can't express XOR -> certifies surface-alone can't solve held-out.
    sr = random.Random(13)

    def feats(surf, fid):
        f = [("fid", fid), ("len", len(surf))]
        for i, ch in enumerate(surf[:6]):
            f.append(("c%d" % i, ch))
        return f
    tr = [(it["surf"], it["form"], it["xor"]) for it in M["seen"]]
    te = [(it["surf"], it["form"], it["xor"]) for it in M["heldout"]]
    w, wa = {}, {}
    for _ in range(60):
        sr.shuffle(tr)
        for surf, fid, y in tr:
            yy = 1 if y == 1 else -1
            s = sum(w.get(k, 0.0) for k in feats(surf, fid))
            if yy * s <= 0:
                for k in feats(surf, fid):
                    w[k] = w.get(k, 0.0) + yy
        for k, v in w.items():
            wa[k] = wa.get(k, 0.0) + v
    if te:
        hh = sum(int((1 if sum(wa.get(k, 0.0) for k in feats(s, f)) > 0 else 0) == y)
                 for s, f, y in te)
        A["V_Dprime_linear_heldout_acc"] = round(hh / len(te), 3)
    else:
        A["V_Dprime_linear_heldout_acc"] = 1.0
    A["V_Dprime_pass"] = A["V_Dprime_linear_heldout_acc"] <= 0.55

    # V-D-info (report-only): surface->pol probe (expected ~0.77 for natural atoms)
    ps = B["plist"][:]
    sr.shuffle(ps)
    ntr = int(len(ps) * 0.8)

    def pf(s):
        return [("c%d" % i, ch) for i, ch in enumerate(s)] + [("L", len(s))]
    w2, wa2 = {}, {}
    for _ in range(60):
        sr.shuffle(ps[:ntr])
        for s in ps[:ntr]:
            yy = 1 if B["pol"][s] == 1 else -1
            sc = sum(w2.get(k, 0.0) for k in pf(s))
            if yy * sc <= 0:
                for k in pf(s):
                    w2[k] = w2.get(k, 0.0) + yy
        for k, v in w2.items():
            wa2[k] = wa2.get(k, 0.0) + v
    te2 = ps[ntr:]
    A["V_D_info_surface_pol_acc"] = (round(sum(int((1 if sum(wa2.get(k, 0.0) for k in pf(s)) > 0 else 0)
                                     == B["pol"][s]) for s in te2) / len(te2), 3) if te2 else 1.0)

    # V-F no-leak: the held-out cell's FULL SEED ("이 영화 <surf> => ") must not appear as a
    #   substring of any training line. (Naive bare-surface check false-positives on prefix
    #   nesting — "재밌다" nests in "정말 재밌다" but the seed "이 영화 재밌다 =>" does NOT, so
    #   the held cell's answer is not revealed.) Also blocks the natural-corpus leak path.
    held_seed = set(it["seed"] for it in M["heldout"])
    all_lines = B["main_lines"] + B["ctrl_lines"]
    leak = sum(1 for ln in all_lines if any(hs in ln for hs in held_seed))
    A["V_F_leak_lines"] = leak
    A["V_F_pass"] = leak == 0

    # V-G window physics: judgment morpheme (stem + 안/지 않) in last-24-byte window
    ok, checked = True, 0
    for it in M["heldout"][:20] + M["seen"][:20]:
        win = it["seed"][-24:]
        ok = ok and (it["p"] in win)
        checked += 1
    A["V_G_checked"] = checked
    A["V_G_pass"] = ok

    # COGS structural asserts (fix5)
    cog_ok = True
    ptrain = collections.defaultdict(lambda: [0, 0])
    for (p, fid) in train:
        ptrain[p][FLIP[fid]] += 1
    for p in B["plist"]:
        if ptrain[p][0] < 2 or ptrain[p][1] < 2:
            cog_ok = False
    A["V_COGS_pass"] = cog_ok

    A["ALL_PASS"] = all(A[k] for k in ("V_C_pass", "V_Dprime_pass", "V_E_pass",
                                       "V_F_pass", "V_G_pass", "V_COGS_pass"))
    return A


def main():
    args = sys.argv[1:]

    def val(flag, default, cast):
        return cast(args[args.index(flag) + 1]) if flag in args else default

    out_dir = val("--out-dir", ".", str)
    nsmc = val("--nsmc", None, str)
    seed = val("--seed", 7, int)
    global MINOCC, P_PER_POL, PURITY
    if "--smoke" in args:
        MINOCC, P_PER_POL, PURITY = 30, 12, 0.80

    rows = load_nsmc(nsmc)
    B = build(rows, seed)
    M = eval_manifest(B)
    A = audit(B, M)

    main_txt = "\n".join(B["main_lines"]) + "\n"
    ctrl_txt = "\n".join(B["ctrl_lines"]) + "\n"
    with open(out_dir + "/nbind_train.txt", "w") as f:
        f.write(main_txt)
    with open(out_dir + "/nbind_shuffle_train.txt", "w") as f:
        f.write(ctrl_txt)
    with open(out_dir + "/nbind_eval_manifest.json", "w") as f:
        json.dump(M, f, ensure_ascii=False, indent=1)
    meta = {"seed": seed, "n_predicates": len(B["plist"]), "n_forms": len(B["forms"]),
            "flip0_forms": B["flip0"], "flip1_forms": B["flip1"],
            "n_cells_train": len(B["train_cells"]), "n_cells_heldout": len(B["heldout_cells"]),
            "nsmc_reviews": len(rows), "bytes_main": len(main_txt.encode()),
            "bytes_ctrl": len(ctrl_txt.encode()), "audit": A}
    with open(out_dir + "/AUDIT.json", "w") as f:
        json.dump(meta, f, ensure_ascii=False, indent=1)
    with open(out_dir + "/EXAMPLES.txt", "w") as f:
        f.write("\n".join(B["main_lines"][:14]) + "\n")
    print(json.dumps(meta, ensure_ascii=False, indent=1))
    if not A["ALL_PASS"]:
        print("PRE-FIRE VALIDITY GATE FAILED — DO NOT SPEND GPU", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
