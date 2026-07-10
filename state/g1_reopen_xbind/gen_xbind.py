#!/usr/bin/env python3
"""gen_xbind.py — XBIND corpus generator (G1 reopen lane a, owner rent=spend go 2026-07-10).

DESIGN-STAGE deterministic reference implementation, structured to fold into the
canonical corpus single entry (`anima corpus xbind|xbind-shuffle`, cli/corpus.py) at
landing time (a_cli_single_entry). Pure procedural string generation, torch-free,
zero external-LLM text (p1-p8).

TASK CLASS (XBIND): each concept c carries a hidden polarity bit pol(c), observable
ONLY through pair outcomes. A pair line's continuation branch is xor(pol(a),pol(b)):
    xor=0 : "<a> <b>: fuse, <ab>."      (portmanteau = order-covariant construct)
    xor=1 : "<a> <b>: part, <a> <b>."
Held-out pairs (20% of C(N,2), NEITHER order ever in corpus) are predictable ONLY by
(i) inferring pol per concept from its training pairings and (ii) applying the xor
rule — NOT by memorized collocation (pair unseen) and NOT by main effects (per-concept
relation marginals are ~exactly 0.5 by construction; audited).

Control arm (xbind-shuffle): content-matched same stream/permutation, but the branch
is an independent per-unordered-pair coin (memorizable, ruleless) — the collocation
regime distilled. Its held-out D-acc floor ≈ 0.5 bounds instrument leak.

Pre-fire $0 validity gates computed here (all must pass BEFORE GPU spend):
  V-C main-effect ceiling  : additive score (b_a+b_b)/2 held-out acc <= 0.55
  V-D pol⊥surface          : averaged-perceptron char-feature probe acc <= 0.60
  V-E marginal balance     : max_c |P(part|c)-0.5| <= 0.10
  V-F no-leak              : no held-out pair prefix (either order) in corpus
  V-G window physics       : eval seed 25B (>=24, no pad), both names inside the
                             last-24-byte decode window (H_6189 T=24 compliance)

Usage:
  python3 gen_xbind.py --out-dir . [--n 400] [--heldout-frac 0.2] [--reps 2]
                       [--singles-per 100] [--seed 7] [--smoke]
"""
import json
import random
import sys

CONS = "bdfghjklmnprstvwz"          # 17 consonants
VOWS = "aeiou"                       # 5 vowels
BANNED = {"now"}                     # CVC collisions with template words
SING = ["{a} waits here.", "{a} stands still.", "{a} rests now."]
N_EVAL_PER_SPLIT = 200


def make_names(rng, n):
    pool = [c1 + v + c2 for c1 in CONS for v in VOWS for c2 in CONS
            if c1 + v + c2 not in BANNED]
    rng.shuffle(pool)
    if n + 1 > len(pool):
        raise SystemExit("name pool exhausted")
    return pool[:n + 1]              # [0]=filler, rest=pair-eligible


def pair_line(a, b, x):
    if x == 0:
        return a + " " + b + ": fuse, " + a + b + "."
    return a + " " + b + ": part, " + a + " " + b + "."


def build(seed, n_concepts, heldout_frac, reps, singles_per):
    rng = random.Random(seed)
    names = make_names(rng, n_concepts)
    filler, concepts = names[0], names[1:]

    porder = concepts[:]
    rng.shuffle(porder)
    pol = {c: (0 if i < len(porder) // 2 else 1) for i, c in enumerate(porder)}

    pairs = [(concepts[i], concepts[j])
             for i in range(len(concepts)) for j in range(i + 1, len(concepts))]
    rng.shuffle(pairs)
    n_held = int(len(pairs) * heldout_frac)
    heldout, train = pairs[:n_held], pairs[n_held:]

    def xor(a, b):
        return pol[a] ^ pol[b]

    # control-arm branch: independent per-unordered-pair coin (consistent across
    # orders/reps = memorizable but ruleless)
    crng = random.Random(seed + 1000)
    ctrl_x = {}
    for (a, b) in train:
        ctrl_x[(a, b)] = 1 if crng.random() < 0.5 else 0

    # content-matched twin streams: one instance list, one shared permutation
    inst = []                                     # (kind, a, b)
    for _ in range(reps):
        for (a, b) in train:
            inst.append(("p", a, b))
            inst.append(("p", b, a))
    for c in [filler] + concepts:
        for k in range(singles_per):
            inst.append(("s", c, k))
    rng.shuffle(inst)

    main_lines, ctrl_lines = [], []
    for kind, a, b in inst:
        if kind == "p":
            key = (a, b) if (a, b) in ctrl_x else (b, a)
            main_lines.append(pair_line(a, b, xor(a, b)))
            ctrl_lines.append(pair_line(a, b, ctrl_x[key]))
        else:
            s = SING[b % 3].format(a=a)
            main_lines.append(s)
            ctrl_lines.append(s)

    return {"filler": filler, "concepts": concepts, "pol": pol,
            "pairs_heldout": heldout, "pairs_train": train, "ctrl_x": ctrl_x,
            "xor": xor, "main_lines": main_lines, "ctrl_lines": ctrl_lines}


def eval_manifest(B, er_seed=97):
    er = random.Random(er_seed)
    xor = B["xor"]

    def items(pairs, split):
        out = []
        for (a, b) in er.sample(pairs, min(N_EVAL_PER_SPLIT, len(pairs))):
            if er.random() < 0.5:
                a, b = b, a
            x = xor(a, b)
            seed_s = B["filler"] + " waits here. " + a + " " + b + ": "
            gold = ("fuse, " + a + b + ".") if x == 0 else ("part, " + a + " " + b + ".")
            cf = ("part, " + a + " " + b + ".") if x == 0 else ("fuse, " + a + b + ".")
            it = {"a": a, "b": b, "xor": x, "seed": seed_s,
                  "gold": gold, "counterfactual": cf,
                  "gold_word": "fuse" if x == 0 else "part",
                  "construct": (a + b + ".") if x == 0 else None}
            if split == "seen":
                key = (a, b) if (a, b) in B["ctrl_x"] else (b, a)
                it["gold_word_ctrl"] = "fuse" if B["ctrl_x"][key] == 0 else "part"
            out.append(it)
        return out

    return {"format": "xbind-eval-v1",
            "note": "engine-native scoring via anima-py evaluate --xbind (fold-in "
                    "eval_xbind_mode.py). PRIMARY=greedy top_k=1 first-word D-acc; "
                    "SECONDARY=teacher-forced gold-vs-counterfactual NLL margin + "
                    "sampled canonical top_k=40 temp=0.7.",
            "gen": 16, "win": 64,
            "heldout": items(B["pairs_heldout"], "heldout"),
            "seen": items(B["pairs_train"], "seen")}


# ── pre-fire $0 validity gates ────────────────────────────────────────────
def audit(B, manifest):
    xor = B["xor"]
    A = {}

    # V-E marginal balance + V-C main-effect ceiling
    cnt = {c: [0, 0] for c in B["concepts"]}       # [n, n_part]
    for (a, b) in B["pairs_train"]:
        x = xor(a, b)
        for c in (a, b):
            cnt[c][0] += 1
            cnt[c][1] += x
    bc = {c: (v[1] / v[0] if v[0] else 0.5) for c, v in cnt.items()}
    skews = [abs(v - 0.5) for v in bc.values()]
    A["V_E_max_marginal_skew"] = max(skews)
    A["V_E_pass"] = A["V_E_max_marginal_skew"] <= 0.10

    hits = 0
    for (a, b) in B["pairs_heldout"]:
        pred = 1 if (bc[a] + bc[b]) / 2.0 > 0.5 else 0
        hits += int(pred == xor(a, b))
    A["V_C_main_effect_heldout_acc"] = hits / len(B["pairs_heldout"])
    A["V_C_pass"] = A["V_C_main_effect_heldout_acc"] <= 0.55
    A["global_majority"] = max(
        sum(xor(a, b) for a, b in B["pairs_heldout"]) / len(B["pairs_heldout"]),
        1 - sum(xor(a, b) for a, b in B["pairs_heldout"]) / len(B["pairs_heldout"]))

    # V-D pol ⊥ surface (averaged perceptron, char features, 80/20 concept split)
    sr = random.Random(13)
    cs = B["concepts"][:]
    sr.shuffle(cs)
    n_tr = int(len(cs) * 0.8)
    tr, te = cs[:n_tr], cs[n_tr:]

    def feats(c):
        return [("p0", c[0]), ("p1", c[1]), ("p2", c[2]), ("b01", c[:2]), ("b12", c[1:])]

    w, wa = {}, {}
    for ep in range(100):
        sr.shuffle(tr)
        for c in tr:
            s = sum(w.get(f, 0.0) for f in feats(c))
            y = 1 if B["pol"][c] == 1 else -1
            if y * s <= 0:
                for f in feats(c):
                    w[f] = w.get(f, 0.0) + y
        for f, v in w.items():
            wa[f] = wa.get(f, 0.0) + v
    hits = sum(int((1 if sum(wa.get(f, 0.0) for f in feats(c)) > 0 else 0) == B["pol"][c])
               for c in te)
    A["V_D_surface_pol_probe_acc"] = hits / len(te)
    A["V_D_pass"] = A["V_D_surface_pol_probe_acc"] <= 0.60

    # V-F no-leak: no held-out pair prefix (either order) anywhere in either arm
    forbidden = set()
    for (a, b) in B["pairs_heldout"]:
        forbidden.add(a + " " + b + ":")
        forbidden.add(b + " " + a + ":")
    leak = 0
    for ln in B["main_lines"] + B["ctrl_lines"]:
        if ln[:8] in forbidden:                    # prefix "aaa bbb:" is 8 bytes
            leak += 1
    A["V_F_leak_lines"] = leak
    A["V_F_pass"] = leak == 0

    # V-G window physics (H_6189: decode T=24 right-aligned)
    ok = True
    for it in manifest["heldout"][:20] + manifest["seen"][:20]:
        s = it["seed"]
        win = s[-24:]
        ok = ok and len(s) == 25 and (it["a"] in win) and (it["b"] in win)
    A["V_G_pass"] = ok
    A["line_len_fuse"] = len(pair_line("bek", "lus", 0))
    A["line_len_part"] = len(pair_line("bek", "lus", 1))

    A["ALL_PASS"] = all(A[k] for k in ("V_C_pass", "V_D_pass", "V_E_pass",
                                       "V_F_pass", "V_G_pass"))
    return A


def main():
    args = sys.argv[1:]

    def val(flag, default, cast):
        return cast(args[args.index(flag) + 1]) if flag in args else default

    out_dir = val("--out-dir", ".", str)
    n = val("--n", 400, int)
    hf = val("--heldout-frac", 0.2, float)
    reps = val("--reps", 2, int)
    sp = val("--singles-per", 100, int)
    seed = val("--seed", 7, int)
    if "--smoke" in args:
        n, reps, sp = 40, 1, 10

    B = build(seed, n, hf, reps, sp)
    M = eval_manifest(B)
    A = audit(B, M)

    main_txt = "\n".join(B["main_lines"]) + "\n"
    ctrl_txt = "\n".join(B["ctrl_lines"]) + "\n"
    with open(out_dir + "/xbind_train.txt", "w") as f:
        f.write(main_txt)
    with open(out_dir + "/xbind_shuffle_train.txt", "w") as f:
        f.write(ctrl_txt)
    with open(out_dir + "/xbind_eval_manifest.json", "w") as f:
        json.dump(M, f, ensure_ascii=False, indent=1)
    meta = {"seed": seed, "n_concepts": n, "filler": B["filler"],
            "n_pairs_total": len(B["pairs_train"]) + len(B["pairs_heldout"]),
            "n_pairs_train": len(B["pairs_train"]),
            "n_pairs_heldout": len(B["pairs_heldout"]),
            "heldout_frac": hf, "reps": reps, "singles_per": sp,
            "bytes_main": len(main_txt.encode()),
            "bytes_ctrl": len(ctrl_txt.encode()),
            "audit": A}
    with open(out_dir + "/AUDIT.json", "w") as f:
        json.dump(meta, f, indent=1)
    with open(out_dir + "/EXAMPLES.txt", "w") as f:
        f.write("\n".join(B["main_lines"][:10]) + "\n")
    print(json.dumps(meta, indent=1))
    if not A["ALL_PASS"]:
        print("PRE-FIRE VALIDITY GATE FAILED — DO NOT SPEND GPU", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
