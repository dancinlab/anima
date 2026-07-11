#!/usr/bin/env python3
"""gen_xfan.py — XFAN corpus generator (G6 / ρ·fan reopen lane, owner rent=spend go 2026-07-11).

DESIGN-STAGE deterministic reference impl (frozen spec = state/g6_reopen_xfan/DESIGN_PREREG.md),
structured to fold into the canonical corpus single entry (`anima corpus xfan|xfan-shuffle`,
cli/corpus.py) at landing (a_cli_single_entry). Pure procedural, torch-free, 0 external-LLM (p1-p8).

TASK CLASS (XFAN — G6 one-to-many fan, the G6 homolog of XBIND's 1-bit discrimination):
each concept c carries a hidden class pair (a,b), a in A(4), b in B(4) = 16 cells, observable
ONLY through: (i) a `decl` line "<c> is <aw> <bw>." installing the latent (present for ALL 400
concepts incl. held-out; at eval it sits OUTSIDE the T=24 window = in the weights), and (ii) for
TRAIN concepts, K=5 `fan` lines "<c>? <s_k>, <g_k(a,b)>." — the SAME prompt "<c>? " with 5
distinct slot-continuations CO-PRESENT = one-to-many placed physically in the CE target.
Per-slot rule table g_k maps cell->member (seeded random, generally NON-additive; audited). 2 slots
are UNARY (g depends on a only / b only), 3 are JOINT (g depends on the (a,b) joint) — the built-in
discriminator (held-out failure decomposes into fan-intrinsic vs joint-binding[G1-class] per slot).

Held-out concepts (80, 5/cell balanced) have NO fan line for ANY slot (fully corpus-absent); their
gold K-set is predictable ONLY by inferring (a,b) from decl + applying each slot table learned from
TRAIN concepts' fan lines. NOT memorizable (fan absent), NOT main-effect (random joint table, V-C
audited), NOT surface (random concept->cell, V-D audited). MDL: 5x16 tables + 400 decls << memorizing
400 held-out fan lines.

Control arm (xfan-shuffle): content-matched same stream/permutation, but each concept's per-slot
member is an INDEPENDENT per-(concept,slot) random draw from that slot's vocab (consistent per
concept = seen-memorizable, but rule-free = no held-out generalization). decl kept. = collocation
regime distilled; its held-out C floor bounds instrument leak.

Pre-fire $0 validity gates (all must pass BEFORE GPU spend):
  V-C main-effect ceiling : additive (a-marginal + b-marginal) held-out member-acc <= chance band
  V-D latent ⊥ surface    : char-feature perceptron cell(16-way) probe acc <= 0.20 (chance 1/16≈0.06)
  V-E balance             : cell / marginal-class skew <= 0.10
  V-H slot marginal bal    : per-slot corpus line-frequency skew <= 0.10 (sampler-bias≠mode-pref)
  V-F no-leak             : no held-out "<c>? " fan prefix (any slot) anywhere in corpus
  V-G window physics       : eval seed >= 24B, concept name inside last-24-byte decode window

Usage:
  python3 gen_xfan.py --out-dir . [--n 400] [--heldout-per-cell 5] [--reps 3]
                      [--singles-per 60] [--seed 7] [--smoke]
"""
import json
import random
import sys

CONS = "bdfghjklmnprstvwz"          # 17 consonants
VOWS = "aeiou"                       # 5 vowels
SLOTS = ["fo", "mi", "ra", "ku", "ze"]   # 5 fixed slot markers (NOT from the concept pool)
SLOT_KIND = ["a", "b", "j", "j", "j"]    # 2 unary (a-only, b-only) + 3 joint
SING = ["{c} waits here.", "{c} stands still.", "{c} rests now."]
NA = 4
NB = 4
NCELL = NA * NB
N_EVAL_PER_SPLIT = 80


def make_pool(rng, need):
    pool = [c1 + v + c2 for c1 in CONS for v in VOWS for c2 in CONS]
    rng.shuffle(pool)
    if need > len(pool):
        raise SystemExit("CVC pool exhausted")
    return pool


def build(seed, n_concepts, heldout_per_cell, reps, singles_per):
    rng = random.Random(seed)
    # pool carve: filler + concepts + class-a words(4) + class-b words(4) + 5*16 member words
    n_members = len(SLOTS) * NCELL
    pool = make_pool(rng, 1 + n_concepts + NA + NB + n_members)
    idx = 0
    filler = pool[idx]; idx += 1
    concepts = pool[idx:idx + n_concepts]; idx += n_concepts
    aw = pool[idx:idx + NA]; idx += NA          # surface words for class-a (decl)
    bw = pool[idx:idx + NB]; idx += NB          # surface words for class-b (decl)
    member = {}                                  # (slot_k, cell) -> member word
    for k in range(len(SLOTS)):
        vocab = pool[idx:idx + NCELL]; idx += NCELL
        for cell in range(NCELL):
            member[(k, cell)] = vocab[cell]

    # per-slot rule table g_k(a,b) -> member.  unary slots collapse to a-only / b-only.
    trng = random.Random(seed + 7)
    table = {}                                   # (k, a, b) -> member word
    for k, kind in enumerate(SLOT_KIND):
        # a random permutation of the slot's 16-vocab over the 16 cells makes JOINT tables
        # non-additive; unary tables reuse a single member per a (or per b).
        perm = list(range(NCELL)); trng.shuffle(perm)
        for a in range(NA):
            for b in range(NB):
                if kind == "a":
                    cellkey = a                      # depends on a only -> 4 distinct members
                elif kind == "b":
                    cellkey = NA + b                 # depends on b only (offset region)
                else:
                    cellkey = a * NB + b             # joint -> all 16 distinct
                table[(k, a, b)] = member[(k, perm[cellkey])]

    # balanced cell assignment: 25/cell for 400, held-out 5/cell
    cells = []
    per = n_concepts // NCELL
    for cell in range(NCELL):
        cells += [cell] * per
    cells += [rng.randrange(NCELL) for _ in range(n_concepts - len(cells))]
    rng.shuffle(cells)
    cls = {}                                      # concept -> (a, b)
    for c, cell in zip(concepts, cells):
        cls[c] = (cell // NB, cell % NB)

    # held-out: heldout_per_cell per cell (fan fully absent), rest train
    bycell = {}
    for c in concepts:
        a, b = cls[c]
        bycell.setdefault(a * NB + b, []).append(c)
    heldout, train = [], []
    for cell, cs in bycell.items():
        rng.shuffle(cs)
        heldout += cs[:heldout_per_cell]
        train += cs[heldout_per_cell:]

    def gold_set(c):
        a, b = cls[c]
        return [(SLOTS[k], table[(k, a, b)]) for k in range(len(SLOTS))]

    # control arm: per-(concept,slot) independent member (rule-free, seen-consistent)
    crng = random.Random(seed + 1000)
    ctrl_member = {}
    for c in concepts:
        for k in range(len(SLOTS)):
            ctrl_member[(c, k)] = member[(k, crng.randrange(NCELL))]

    def decl_line(c):
        a, b = cls[c]
        return c + " is " + aw[a] + " " + bw[b] + "."

    def fan_line(c, k, arm):
        m = table[(k, cls[c][0], cls[c][1])] if arm == "main" else ctrl_member[(c, k)]
        return c + "? " + SLOTS[k] + ", " + m + "."

    # content-matched twin streams (one instance list, one shared permutation)
    inst = []                                     # (kind, concept, k|rep)
    for _ in range(reps):
        for c in train:
            for k in range(len(SLOTS)):
                inst.append(("f", c, k))
    for c in concepts:                            # decl for ALL concepts (incl held-out)
        for _ in range(max(1, reps)):
            inst.append(("d", c, 0))
    for c in [filler] + concepts:
        for j in range(singles_per):
            inst.append(("s", c, j))
    rng.shuffle(inst)

    main_lines, ctrl_lines = [], []
    for kind, c, k in inst:
        if kind == "f":
            main_lines.append(fan_line(c, k, "main"))
            ctrl_lines.append(fan_line(c, k, "ctrl"))
        elif kind == "d":
            ln = decl_line(c)                      # decl identical both arms (latent kept)
            main_lines.append(ln); ctrl_lines.append(ln)
        else:
            ln = SING[k % 3].format(c=c)
            main_lines.append(ln); ctrl_lines.append(ln)

    return {"filler": filler, "concepts": concepts, "cls": cls, "aw": aw, "bw": bw,
            "table": table, "member": member, "ctrl_member": ctrl_member,
            "heldout": heldout, "train": train, "gold_set": gold_set,
            "main_lines": main_lines, "ctrl_lines": ctrl_lines}


def eval_manifest(B, er_seed=97):
    er = random.Random(er_seed)

    def items(cs, split):
        out = []
        for c in er.sample(cs, min(N_EVAL_PER_SPLIT, len(cs))):
            seed_s = B["filler"] + " waits here. " + c + "? "
            gold = [{"slot": s, "member": m} for (s, m) in B["gold_set"](c)]
            # per-slot foil (same-slot different-cell member) for the teacher-forced margin
            foils = {}
            for k, (s, m) in enumerate(B["gold_set"](c)):
                alt = [B["member"][(k, cc)] for cc in range(NCELL) if B["member"][(k, cc)] != m]
                foils[s] = alt[(er.randrange(len(alt)))] if alt else m
            it = {"concept": c, "seed": seed_s, "gold": gold, "foils": foils,
                  "slot_kind": {SLOTS[k]: SLOT_KIND[k] for k in range(len(SLOTS))}}
            if split == "seen":
                it["gold_ctrl"] = [{"slot": SLOTS[k],
                                    "member": B["ctrl_member"][(c, k)]} for k in range(len(SLOTS))]
            out.append(it)
        return out

    return {"format": "xfan-eval-v1",
            "note": "engine-native scoring via anima-py evaluate --xfan (fold-in eval_xfan_mode.py). "
                    "PRIMARY=coverage C=|correct unique (slot,member)|/5 over 16 sampled decodes "
                    "(top_k=40 temp=0.7); per-slot-kind (unary vs joint) breakout; valid/spurious "
                    "split; SECONDARY=teacher-forced NLL margin foil-vs-gold (mode-collapse "
                    "discriminator); greedy-collapse (top_k=1) control.",
            "gen": 16, "win": 64, "n_slots": len(SLOTS),
            "heldout": items(B["heldout"], "heldout"),
            "seen": items(B["train"], "seen")}


# ── pre-fire $0 validity gates ────────────────────────────────────────────
def audit(B, manifest):
    A = {}
    concepts, cls, table = B["concepts"], B["cls"], B["table"]
    heldout, train = B["heldout"], B["train"]

    # V-E cell balance + marginal class balance
    cellcnt = [0] * NCELL
    for c in concepts:
        a, b = cls[c]; cellcnt[a * NB + b] += 1
    exp = len(concepts) / NCELL
    A["V_E_max_cell_skew"] = max(abs(x - exp) / exp for x in cellcnt)
    A["V_E_pass"] = A["V_E_max_cell_skew"] <= 0.10

    # V-C main-effect ceiling on JOINT slots: additive predictor = most-common member for the
    # held-out concept's a (over train, this slot) OR its b — take best; must trail gold.
    jslots = [k for k in range(len(SLOTS)) if SLOT_KIND[k] == "j"]
    def marg_pred_acc(byfeat):
        # byfeat: 'a' or 'b' — predict the plurality member among train concepts sharing that feat
        hit = 0; tot = 0
        for k in jslots:
            tally = {}
            for c in train:
                a, b = cls[c]; key = a if byfeat == "a" else b
                m = table[(k, a, b)]
                tally.setdefault((k, key), {}).setdefault(m, 0)
                tally[(k, key)][m] += 1
            for c in heldout:
                a, b = cls[c]; key = a if byfeat == "a" else b
                d = tally.get((k, key), {})
                pred = max(d, key=d.get) if d else None
                hit += int(pred == table[(k, a, b)]); tot += 1
        return hit / tot if tot else 0.0
    acc_a = marg_pred_acc("a"); acc_b = marg_pred_acc("b")
    A["V_C_main_effect_heldout_acc"] = round(max(acc_a, acc_b), 4)
    A["V_C_chance_band"] = round(1.0 / NB + 0.10, 4)   # a fixes 4 members over b → ~1/4 best-case
    A["V_C_pass"] = A["V_C_main_effect_heldout_acc"] <= A["V_C_chance_band"]

    # V-D latent ⊥ surface: averaged-perceptron char-feature 16-way cell probe (one-vs-rest)
    sr = random.Random(13)
    cs = concepts[:]; sr.shuffle(cs)
    ntr = int(len(cs) * 0.8); tr, te = cs[:ntr], cs[ntr:]
    def feats(c):
        return [("p0", c[0]), ("p1", c[1]), ("p2", c[2]), ("b01", c[:2]), ("b12", c[1:])]
    W = {cell: {} for cell in range(NCELL)}
    for ep in range(30):
        sr.shuffle(tr)
        for c in tr:
            a, b = cls[c]; y = a * NB + b
            scores = {cell: sum(W[cell].get(f, 0.0) for f in feats(c)) for cell in range(NCELL)}
            pred = max(scores, key=scores.get)
            if pred != y:
                for f in feats(c):
                    W[y][f] = W[y].get(f, 0.0) + 1
                    W[pred][f] = W[pred].get(f, 0.0) - 1
    hit = 0
    for c in te:
        a, b = cls[c]; y = a * NB + b
        scores = {cell: sum(W[cell].get(f, 0.0) for f in feats(c)) for cell in range(NCELL)}
        hit += int(max(scores, key=scores.get) == y)
    A["V_D_surface_cell_probe_acc"] = round(hit / len(te), 4)
    A["V_D_pass"] = A["V_D_surface_cell_probe_acc"] <= 0.20

    # V-H slot marginal balance: per-slot fan-line frequency in the corpus
    scnt = {s: 0 for s in SLOTS}
    for ln in B["main_lines"]:
        if "? " in ln:
            mk = ln.split("? ", 1)[1][:2]
            if mk in scnt:
                scnt[mk] += 1
    tot = sum(scnt.values()) or 1
    A["V_H_max_slot_skew"] = round(max(abs(v / tot - 1.0 / len(SLOTS)) for v in scnt.values()), 4)
    A["V_H_pass"] = A["V_H_max_slot_skew"] <= 0.10

    # V-F no-leak: no held-out "<c>? " fan prefix anywhere in either arm
    forbidden = set(c + "? " for c in heldout)
    leak = sum(1 for ln in B["main_lines"] + B["ctrl_lines"] if ln[:5] in forbidden)
    A["V_F_leak_lines"] = leak
    A["V_F_pass"] = leak == 0

    # V-G window physics (H_6189 T=24): the concept name must sit inside the last-24-byte decode
    # window AND the decl latent ("<c> is …") must NOT be in the seed (it lives in the weights).
    ok = True
    for it in manifest["heldout"][:20] + manifest["seen"][:20]:
        s = it["seed"]
        ok = ok and (it["concept"] in s[-24:]) and ((it["concept"] + " is ") not in s)
    A["V_G_pass"] = ok

    A["ALL_PASS"] = all(A[k] for k in ("V_C_pass", "V_D_pass", "V_E_pass",
                                       "V_H_pass", "V_F_pass", "V_G_pass"))
    return A


def main():
    args = sys.argv[1:]

    def val(flag, default, cast):
        return cast(args[args.index(flag) + 1]) if flag in args else default

    out_dir = val("--out-dir", ".", str)
    n = val("--n", 400, int)
    hpc = val("--heldout-per-cell", 5, int)
    reps = val("--reps", 3, int)
    sp = val("--singles-per", 60, int)
    seed = val("--seed", 7, int)
    if "--smoke" in args:
        n, hpc, reps, sp = 160, 2, 2, 8

    B = build(seed, n, hpc, reps, sp)
    M = eval_manifest(B)
    A = audit(B, M)

    main_txt = "\n".join(B["main_lines"]) + "\n"
    ctrl_txt = "\n".join(B["ctrl_lines"]) + "\n"
    with open(out_dir + "/xfan_train.txt", "w") as f:
        f.write(main_txt)
    with open(out_dir + "/xfan_shuffle_train.txt", "w") as f:
        f.write(ctrl_txt)
    with open(out_dir + "/xfan_eval_manifest.json", "w") as f:
        json.dump(M, f, ensure_ascii=False, indent=1)
    meta = {"seed": seed, "n_concepts": n, "filler": B["filler"], "n_slots": len(SLOTS),
            "slot_kind": SLOT_KIND, "n_heldout": len(B["heldout"]), "n_train": len(B["train"]),
            "heldout_per_cell": hpc, "reps": reps, "singles_per": sp,
            "bytes_main": len(main_txt.encode()), "bytes_ctrl": len(ctrl_txt.encode()),
            "audit": A}
    with open(out_dir + "/AUDIT.json", "w") as f:
        json.dump(meta, f, indent=1)
    with open(out_dir + "/EXAMPLES.txt", "w") as f:
        f.write("\n".join(B["main_lines"][:12]) + "\n")
    print(json.dumps(meta, indent=1))
    if not A["ALL_PASS"]:
        print("PRE-FIRE VALIDITY GATE FAILED — DO NOT SPEND GPU", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
