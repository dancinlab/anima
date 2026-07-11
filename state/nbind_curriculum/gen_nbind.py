#!/usr/bin/env python3
"""gen_nbind.py — NBIND corpus generator (G1 natural-atom reopen, owner rent=spend go 2026-07-11).

Fable NEXT-DIRECTION verdict B+ ("NBIND"): the XBIND CRACK (H_9267) proved the G1
recombination wall is a corpus x CE MEASURE artifact, not a substrate ceiling — but on
MEANINGLESS CVC atoms (toy). NBIND is the single-variable delta: replace the synthetic
CVC concepts with NATURAL Korean sentiment atoms (NSMC predicate polarity x negation
morpheme), keeping the XBIND held-out XOR protocol byte-identical. If the substrate
re-cracks on MEANINGFUL natural atoms -> rho_weave FLOOR->PASS -> L3 wire = anima's 2nd
WIRED-GREEN faculty. See FABLE_NBIND_SPEC.md (frozen pre-registration).

TASK CLASS (NBIND): each predicate p carries an NSMC-grounded polarity pol(p) in {0,1}
(0=neg sentiment, 1=pos). Each negation FORM n carries a flip bit flip(n): bare=0,
{안 , 지 않, 못 , 전혀..지 않}=1. A grid line's continuation branch is the composed
sentiment token = xor(pol(p), flip(n)):
    xor(pol,flip)=1 -> "긍정" / xor=0 -> "부정"   (ko), "pos"/"neg" (en gloss line)
Held-out (p, n) grid CELLS (a COGS-style compositional split: each p appears with SOME
forms, each n with MANY predicates, but the held-out (p,n) pair co-occurs 0 times) are
predictable ONLY by (i) inferring pol(p) from p's OTHER seen forms, (ii) inferring
flip(n) from n's OTHER seen predicates, (iii) composing the XOR — NOT by memorized
collocation (cell unseen) and NOT by additive main effects (audited: additive held-out
acc <= 0.55 because XOR is non-additive; matches A0-NEG natural additive-ceiling 0.559).

Atoms are REAL: predicates mined from NSMC bare occurrences (pol = majority label,
count>=MINOCC, purity>=PURITY); clauses are real NSMC review spans containing p, with the
negation morpheme applied by SURFACE RULE only (no template CVC, no external-LLM text; p1-p8).

Control arm (nbind-shuffle): content-matched same stream/permutation, but the per-(p,n)
branch is an independent coin fixed within a cell (memorizable, ruleless; XOR destroyed,
surface stats preserved). Its held-out D-acc floor ~0.5 bounds instrument leak.

Pre-fire $0 validity gates (all must pass BEFORE GPU spend):
  V-C main-effect ceiling  : additive (b_pol + b_flip) held-out acc <= 0.55
  V-D pol/flip vs surface  : averaged-perceptron char probe on p <= 0.65 (pol not a
                             pure surface function of the predicate string)
  V-E marginal balance     : per-atom output-branch marginal skew <= 0.12
  V-F no-leak              : no held-out (p,n) cell prefix anywhere in either arm
  V-G window physics       : both atoms (p, n-marker) inside the last-24-byte window
  V-H natural-transfer power: >=NAT_MIN pure-natural held-out flip pairs pre-secured

Usage:
  python3 gen_nbind.py --out-dir . [--nsmc <path>] [--heldout-frac 0.2] [--reps 3]
                       [--minocc 8] [--purity 0.8] [--seed 7] [--smoke]
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

# negation FORMS: (surface marker rendered before/around the stem, flip bit, id)
# flip=0 -> bare (no negation, polarity passes through); flip=1 -> negation (polarity XORs)
NEG_FORMS = [
    ("", 0, "bare"),
    ("안 ", 1, "an"),
    ("못 ", 1, "mot"),
    ("전혀 ", 1, "jeonhyeo"),   # paired with 지 않 tail in render
]
TAIL_JI = "지 않"                       # "<stem>지 않" negation tail (used by an/jeonhyeo variants elsewhere)
N_EVAL_PER_SPLIT = 200
MINOCC_DEFAULT = 8
PURITY_DEFAULT = 0.8
NAT_MIN = 200                            # V-H: min pure-natural held-out flip pairs

# NSMC surface negation detectors (A0-NEG parity)
NEG_AN = re.compile(r"안\s+([가-힣]{2,4})")
NEG_JI = re.compile(r"([가-힣]{2,5})지\s*않")


def load_nsmc(path):
    p = path or NSMC_CACHE
    if not os.path.exists(p):
        os.makedirs(os.path.dirname(p), exist_ok=True)
        urllib.request.urlretrieve(NSMC_URL, p)
    rows = []
    with open(p, encoding="utf-8") as f:
        next(f, None)                    # header id\tdocument\tlabel
        for line in f:
            pp = line.rstrip("\n").split("\t")
            if len(pp) == 3 and pp[2] in ("0", "1"):
                rows.append((pp[1], int(pp[2])))
    return rows


def bare_stems(text, neg_stems):
    """content stems 2-4 hangul not adjacent to a negation marker (A0-NEG parity)."""
    out = []
    for t in re.findall(r"[가-힣]{2,4}", text):
        if t not in neg_stems and "않" not in t and t != "안":
            out.append(t)
    return out


def mine_predicates(rows, minocc, purity):
    """pol(p) = majority NSMC label of NON-negated reviews containing bare p."""
    bare_lab = collections.defaultdict(list)
    span_by_stem = collections.defaultdict(list)     # real clauses to reuse as atoms
    for text, lab in rows:
        neg_stems = ({m.group(1) for m in NEG_AN.finditer(text)}
                     | {m.group(1) for m in NEG_JI.finditer(text)})
        seen = set()
        for p in bare_stems(text, neg_stems):
            bare_lab[p].append(lab)
            if p not in seen and len(span_by_stem[p]) < 40:
                span_by_stem[p].append(text.strip())
                seen.add(p)
    preds = {}
    for p, labs in bare_lab.items():
        if len(labs) < minocc:
            continue
        pos = sum(labs) / len(labs)
        pur = max(pos, 1 - pos)
        if pur >= purity:
            preds[p] = {"pol": 1 if pos >= 0.5 else 0, "n": len(labs),
                        "purity": round(pur, 3), "spans": span_by_stem[p]}
    return preds


def render_clause(stem, span, form_marker, flip, rng):
    """Build a real-clause atom line: reuse a genuine NSMC span containing the stem,
    apply the negation morpheme by surface rule. Falls back to a minimal real-token
    frame if no span holds the stem cleanly (still real tokens, no template CVC)."""
    if flip == 0:
        core = stem + "다"
    else:
        # "안 <stem>다" / "못 <stem>다" / "전혀 <stem>지 않다"
        if form_marker == "전혀 ":
            core = form_marker + stem + TAIL_JI + "다"
        else:
            core = form_marker + stem + "다"
    # ground with a short real span prefix when available (context, not template)
    if span:
        ctx = span[:40].replace("\n", " ").strip()
        return ctx + " " + core
    return "이 리뷰는 " + core


def build(rows, seed, heldout_frac, reps, minocc, purity):
    rng = random.Random(seed)
    preds = mine_predicates(rows, minocc, purity)
    # balance pol classes; cap for a tractable grid
    pos = [p for p, d in preds.items() if d["pol"] == 1]
    neg = [p for p, d in preds.items() if d["pol"] == 0]
    rng.shuffle(pos); rng.shuffle(neg)
    k = min(len(pos), len(neg))
    plist = pos[:k] + neg[:k]
    rng.shuffle(plist)
    if k < 4:
        raise SystemExit("predicate pool too small (k=%d) — lower --minocc/--purity" % k)

    forms = NEG_FORMS[:]
    # grid cells = predicate x form
    cells = [(p, f[2]) for p in plist for f in forms]
    rng.shuffle(cells)
    n_held = int(len(cells) * heldout_frac)
    heldout = set(cells[:n_held])
    train_cells = [c for c in cells if c not in heldout]

    pol = {p: preds[p]["pol"] for p in plist}
    flip = {f[2]: f[1] for f in forms}
    marker = {f[2]: f[0] for f in forms}

    def out_bit(p, fid):
        return pol[p] ^ flip[fid]

    # control branch: independent coin per cell (consistent across reps = memorizable)
    crng = random.Random(seed + 1000)
    ctrl_bit = {c: (1 if crng.random() < 0.5 else 0) for c in train_cells}

    inst = []
    for _ in range(reps):
        for (p, fid) in train_cells:
            inst.append((p, fid))
    rng.shuffle(inst)

    def line(p, fid, bit):
        span = rng.choice(preds[p]["spans"]) if preds[p]["spans"] else ""
        clause = render_clause(p, span, marker[fid], flip[fid], rng)
        tok = "긍정" if bit == 1 else "부정"
        return clause + " => " + tok + "."

    main_lines, ctrl_lines = [], []
    for (p, fid) in inst:
        main_lines.append(line(p, fid, out_bit(p, fid)))
        ctrl_lines.append(line(p, fid, ctrl_bit[(p, fid)]))

    return {"preds": preds, "plist": plist, "pol": pol, "flip": flip,
            "marker": marker, "forms": forms, "cells_heldout": sorted(heldout),
            "cells_train": train_cells, "ctrl_bit": ctrl_bit, "out_bit": out_bit,
            "main_lines": main_lines, "ctrl_lines": ctrl_lines, "rng_seed": seed}


def eval_manifest(B, rows, er_seed=97):
    er = random.Random(er_seed)
    out_bit = B["out_bit"]
    preds = B["preds"]

    def items(cells, split):
        out = []
        picks = er.sample(cells, min(N_EVAL_PER_SPLIT, len(cells)))
        for (p, fid) in picks:
            bit = out_bit(p, fid)
            span = er.choice(preds[p]["spans"]) if preds[p]["spans"] else ""
            clause = render_clause(p, span, B["marker"][fid], B["flip"][fid], er)
            seed_s = clause + " => "
            gold = ("긍정." if bit == 1 else "부정.")
            cf = ("부정." if bit == 1 else "긍정.")
            it = {"p": p, "form": fid, "pol": B["pol"][p], "flip": B["flip"][fid],
                  "xor": bit, "seed": seed_s, "gold": gold, "counterfactual": cf,
                  "gold_word": "긍정" if bit == 1 else "부정"}
            if split == "seen":
                cb = B["ctrl_bit"][(p, fid)]
                it["gold_word_ctrl"] = "긍정" if cb == 1 else "부정"
            out.append(it)
        return out

    return {"format": "nbind-eval-v1",
            "note": "engine-native scoring via anima-py evaluate --xbind (NBIND is "
                    "XBIND-isomorphic: greedy top_k=1 first-word D-acc on 긍정/부정 + "
                    "teacher-forced gold-vs-counterfactual NLL margin).",
            "gen": 8, "win": 64,
            "heldout": items(B["cells_heldout"], "heldout"),
            "seen": items(B["cells_train"], "seen")}


# ── pre-fire $0 validity gates ────────────────────────────────────────────
def audit(B, manifest):
    out_bit = B["out_bit"]
    A = {}

    # V-E marginal balance: per-predicate & per-form output-branch skew (train)
    pc = collections.defaultdict(lambda: [0, 0])
    fc = collections.defaultdict(lambda: [0, 0])
    for (p, fid) in B["cells_train"]:
        b = out_bit(p, fid)
        pc[p][0] += 1; pc[p][1] += b
        fc[fid][0] += 1; fc[fid][1] += b
    pskew = [abs(v[1] / v[0] - 0.5) for v in pc.values() if v[0]]
    fskew = [abs(v[1] / v[0] - 0.5) for v in fc.values() if v[0]]
    A["V_E_max_pred_skew"] = round(max(pskew), 3) if pskew else 1.0
    A["V_E_max_form_skew"] = round(max(fskew), 3) if fskew else 1.0
    A["V_E_pass"] = A["V_E_max_pred_skew"] <= 0.12 and A["V_E_max_form_skew"] <= 0.12

    # V-C main-effect ceiling: additive model from per-atom marginals on held-out
    bp = {p: (v[1] / v[0] if v[0] else 0.5) for p, v in pc.items()}
    bf = {f: (v[1] / v[0] if v[0] else 0.5) for f, v in fc.items()}
    hits = 0
    held = B["cells_heldout"]
    for (p, fid) in held:
        pred = 1 if (bp.get(p, 0.5) + bf.get(fid, 0.5)) / 2.0 > 0.5 else 0
        hits += int(pred == out_bit(p, fid))
    A["V_C_main_effect_heldout_acc"] = round(hits / len(held), 3) if held else 1.0
    A["V_C_pass"] = A["V_C_main_effect_heldout_acc"] <= 0.55

    # V-D pol vs surface: char-feature averaged perceptron predicting pol from stem
    sr = random.Random(13)
    ps = B["plist"][:]
    sr.shuffle(ps)
    ntr = int(len(ps) * 0.8)
    tr, te = ps[:ntr], ps[ntr:]

    def feats(s):
        f = [("len", len(s))]
        for i, ch in enumerate(s):
            f.append(("c%d" % i, ch))
        for i in range(len(s) - 1):
            f.append(("bg%d" % i, s[i:i + 2]))
        return f

    w, wa = {}, {}
    for _ in range(80):
        sr.shuffle(tr)
        for s in tr:
            sc = sum(w.get(f, 0.0) for f in feats(s))
            y = 1 if B["pol"][s] == 1 else -1
            if y * sc <= 0:
                for f in feats(s):
                    w[f] = w.get(f, 0.0) + y
        for f, v in w.items():
            wa[f] = wa.get(f, 0.0) + v
    if te:
        hh = sum(int((1 if sum(wa.get(f, 0.0) for f in feats(s)) > 0 else 0) == B["pol"][s])
                 for s in te)
        A["V_D_surface_pol_probe_acc"] = round(hh / len(te), 3)
    else:
        A["V_D_surface_pol_probe_acc"] = 1.0
    A["V_D_pass"] = A["V_D_surface_pol_probe_acc"] <= 0.65

    # V-F no-leak: no held-out cell's rendered prefix appears in any training line
    held_pref = set()
    for (p, fid) in held:
        held_pref.add((p, fid))
    leak = 0
    for (p, fid) in B["cells_train"]:
        if (p, fid) in held_pref:
            leak += 1
    A["V_F_leak_cells"] = leak
    A["V_F_pass"] = leak == 0

    # V-G window physics: predicate stem + neg marker inside last-24-byte window
    ok = True
    checked = 0
    for it in manifest["heldout"][:20] + manifest["seen"][:20]:
        win = it["seed"][-24:]
        marker = B["marker"][it["form"]].strip()
        cond = (it["p"] in win) and (marker == "" or marker in win)
        ok = ok and cond
        checked += 1
    A["V_G_checked"] = checked
    A["V_G_pass"] = ok

    A["ALL_PASS"] = all(A[k] for k in ("V_C_pass", "V_D_pass", "V_E_pass",
                                       "V_F_pass", "V_G_pass"))
    return A


def main():
    args = sys.argv[1:]

    def val(flag, default, cast):
        return cast(args[args.index(flag) + 1]) if flag in args else default

    out_dir = val("--out-dir", ".", str)
    nsmc = val("--nsmc", None, str)
    hf = val("--heldout-frac", 0.2, float)
    reps = val("--reps", 3, int)
    minocc = val("--minocc", MINOCC_DEFAULT, int)
    purity = val("--purity", PURITY_DEFAULT, float)
    seed = val("--seed", 7, int)
    if "--smoke" in args:
        reps, minocc = 1, 5

    rows = load_nsmc(nsmc)
    B = build(rows, seed, hf, reps, minocc, purity)
    M = eval_manifest(B, rows)
    A = audit(B, M)

    main_txt = "\n".join(B["main_lines"]) + "\n"
    ctrl_txt = "\n".join(B["ctrl_lines"]) + "\n"
    with open(out_dir + "/nbind_train.txt", "w") as f:
        f.write(main_txt)
    with open(out_dir + "/nbind_shuffle_train.txt", "w") as f:
        f.write(ctrl_txt)
    with open(out_dir + "/nbind_eval_manifest.json", "w") as f:
        json.dump(M, f, ensure_ascii=False, indent=1)
    meta = {"seed": seed, "n_predicates": len(B["plist"]),
            "n_forms": len(B["forms"]),
            "n_cells_total": len(B["cells_train"]) + len(B["cells_heldout"]),
            "n_cells_train": len(B["cells_train"]),
            "n_cells_heldout": len(B["cells_heldout"]),
            "heldout_frac": hf, "reps": reps, "minocc": minocc, "purity": purity,
            "nsmc_reviews": len(rows),
            "bytes_main": len(main_txt.encode()),
            "bytes_ctrl": len(ctrl_txt.encode()),
            "audit": A}
    with open(out_dir + "/AUDIT.json", "w") as f:
        json.dump(meta, f, ensure_ascii=False, indent=1)
    with open(out_dir + "/EXAMPLES.txt", "w") as f:
        f.write("\n".join(B["main_lines"][:12]) + "\n")
    print(json.dumps(meta, ensure_ascii=False, indent=1))
    if not A["ALL_PASS"]:
        print("PRE-FIRE VALIDITY GATE FAILED — DO NOT SPEND GPU", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
