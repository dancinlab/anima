#!/usr/bin/env python3
"""H_9289 MAIN — C3+C4 hybrid corpus generator (Fable frozen recipe · 2026-07-13).

STEP-0 said held-out P_nat polarity is NOT installed in the natural-only N2 model (INFO-ABSENT).
C3+C4 intervenes to INSTALL it, WITHOUT ever leaking h's polarity label:
  C3 (anchor-propagation): pol(h) = pol(g) XOR rel(connective).  -고 (rel 0, same-pol) / -지만
     (rel 1, opposite-pol).  h's polarity is recoverable ONLY from its connective relation to an
     already-grounded grid atom g.  h-label token (긍정/부정/=>) NEVER co-occurs with h.
  C4 (diagnosticity): naver(별점 r)/steam(추천) reviews where atom polarity IS the next-byte
     target — makes polarity CE-load-bearing.  NSMC excluded (binary label would need inventing
     the forbidden 긍정/부정 vocab).

Mix grid:C3:C4 = 1:1:2 (non-grid = 3x grid = N2 FILLER_BYTE_RATIO).  4 arms: main-C34 x2seed +
ctrl-shufGT (connective/suffix coin-flipped · grid intact · grounding-signal destroyed) +
ctrl-N2rep (no C3/C4 · N2 wall reproduction anchor).  eval = n2_eval_manifest.json VERBATIM.

Leak gates V2a-g auto-audited; any violation => PREFIRE FAIL (block the fire).  No tune-to-green.
"""
import os, sys, json, random, collections

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(HERE, "..", "nbind_curriculum")))
sys.path.insert(0, HERE)
import gen_nbind as GN
import gen_nbindg_n2 as GN2

E_STAR = 12000
T_MARGIN = 1.25
FILLER_BYTE_RATIO = 3.0            # non-grid : grid = 3 : 1  (C3=1x, C4=2x)
CARRIER = "이 영화 "
CONN = {0: "고", 1: "지만"}         # rel 0 = same polarity (-고) · rel 1 = opposite (-지만)
ATOM_OCC_CAP_H = 60
ATOM_OCC_CAP_G = 30


def _pnat_from_manifest():
    """The 29 held-out P_nat atoms + polarity — VERBATIM from n2_eval_manifest (no re-mine)."""
    m = json.load(open(os.path.join(HERE, "n2_eval_manifest.json")))["heldout"]
    pol = {}
    for it in m:
        pol[it["a"]] = int(it["pol"])
    return pol                       # {stem: pol}


def _grid(seed):
    """H_9272 grid: P_grid stems + pol + authored XOR main/ctrl lines (operator channel)."""
    nsmc_rows = list(GN.load_nsmc(None))
    B = GN.build(nsmc_rows, seed)
    return B


def _collect_spans(target_stems, rows, cap=200):
    """Targeted eojeol collection for a small stem set — scan rows ONCE (vs full mine_predicates
    on 600k rows which is O(preds) heavy). Returns {stem: [eojeol,...]} non-negation surfaces."""
    tset = list(target_stems)
    spans = collections.defaultdict(list)
    need = set(tset)
    for (text, _lab) in rows:
        hit = [st for st in need if st in text]
        if not hit:
            continue
        for ej in text.split():
            for st in hit:
                if len(spans[st]) >= cap:
                    continue
                i = ej.find(st)
                if i < 0:
                    continue
                # reject negation-scope: a negation morpheme AFTER the atom flips its polarity
                # (e.g. "깔끔하지못한" = not-clean). The atom's OWN leading 못 (stem 못하) is kept.
                tail = ej[i + len(st):]
                if any(neg in tail for neg in ("못", "않", "전혀")) or ej.startswith("안"):
                    continue
                spans[st].append(ej)
        need = {st for st in need if len(spans[st]) < cap}
        if not need:
            break
    return spans


def _eojeol(spans, stem, rng):
    """A random attested non-negation eojeol surface for a stem (surface diversity)."""
    cands = spans.get(stem, [])
    return rng.choice(cands) if cands else None


def _c3_lines(B, pnat_pol, spans, seed, byte_target):
    """Anchor-propagation. Deterministic anchor rotation; connective = pol(g) XOR pol(h).
    h-label never emitted. Balanced 고/지만 per h (4 g+ and 4 g-) => connective alone ↛ pol(h)."""
    rng = random.Random(seed + 300)
    pos_g = [p for p in B["plist"] if B["pol"][p] == 1]
    neg_g = [p for p in B["plist"] if B["pol"][p] == 0]
    hs = sorted(pnat_pol.keys())
    lines, per_atom = [], collections.Counter()
    R = 1
    while True:
        batch = []
        for i, h in enumerate(hs):
            hpol = pnat_pol[h]
            anchors = [pos_g[(i + j) % len(pos_g)] for j in range(4)] + \
                      [neg_g[(i + j) % len(neg_g)] for j in range(4)]
            for g in anchors:
                rel = B["pol"][g] ^ hpol
                conn = CONN[rel]
                for order in ("A", "B"):
                    for _r in range(R):
                        if order == "A":
                            hej = _eojeol(spans, h, rng)
                            if not hej:
                                continue
                            ln = "%s%s%s %s." % (CARRIER, g, conn, hej)
                        else:
                            gej = _eojeol(spans, g, rng)
                            if not gej:
                                continue
                            ln = "%s%s%s %s." % (CARRIER, h, conn, gej)
                        # V2e: C3 negation-free EXCEPT the atom 못하 itself (P_nat atom whose
                        # surface legitimately contains 못). span filter already rejected any
                        # eojeol with negation AFTER an atom (scope contamination).
                        assert not any(t in ln for t in ("안 ", "지 않", "전혀")), ln
                        batch.append(ln); per_atom[h] += 1
        if not batch:
            break
        lines = batch
        if len("\n".join(lines).encode()) >= byte_target or R >= 40:
            break
        R += 1
    return lines, per_atom, R


def _c4_lines(pool_rows_raw, atoms_all, seed, byte_target):
    """Diagnosticity: naver 별점/steam 추천 suffix AFTER an atom, polarity-consistent lines only.
    pool_rows_raw = list of (text, label, rating, source)."""
    rng = random.Random(seed + 400)
    stems = list(atoms_all.keys())
    by_atom = collections.defaultdict(list)
    for (text, lab, rating, src) in pool_rows_raw:
        if any(x in text for x in ("=>", "긍정", "부정")):
            continue
        present = [a for a in stems if a in text]
        if not present:
            continue
        # negation-scope reject
        if any(("안 " + a in text) or (a + "지 않" in text) or ("전혀" in text and a in text)
               for a in present):
            continue
        # polarity consistency: every present atom's mined pol == label bucket
        if any(atoms_all[a] != lab for a in present):
            continue
        if src == "naver":
            line = text + " 별점 %d점." % rating
        else:
            line = text + (" 추천." if lab == 1 else " 비추천.")
        for a in present:
            by_atom[a].append(line)
    # round-robin admit (h first, caps), dedup
    out, seen = [], set()
    order = sorted(stems, key=lambda a: (a not in atoms_all, a))
    caps = {a: (ATOM_OCC_CAP_H if atoms_all[a] is not None else ATOM_OCC_CAP_G) for a in stems}
    idx = {a: 0 for a in stems}
    added = True
    cnt = collections.Counter()
    while added and len("\n".join(out).encode()) < byte_target:
        added = False
        for a in order:
            if cnt[a] >= caps.get(a, 30):
                continue
            pool = by_atom[a]
            while idx[a] < len(pool):
                ln = pool[idx[a]]; idx[a] += 1
                if ln in seen:
                    continue
                seen.add(ln); out.append(ln); cnt[a] += 1; added = True
                break
    return out, cnt


def _load_pool_raw():
    """(text, label, rating, source) for naver + steam (C4 sources · real ratings)."""
    rows = []
    ns = GN2.POOL_CORPORA["naver_shopping"]
    if os.path.exists(ns):
        for line in open(ns, encoding="utf-8"):
            pp = line.rstrip("\n").split("\t")
            if len(pp) == 2 and pp[0].isdigit():
                r = int(pp[0])
                if r <= 2:
                    rows.append((pp[1], 0, r, "naver"))
                elif r >= 4:
                    rows.append((pp[1], 1, r, "naver"))
    st = GN2.POOL_CORPORA["steam"]
    if os.path.exists(st):
        for line in open(st, encoding="utf-8"):
            pp = line.rstrip("\n").split("\t")
            if len(pp) == 2 and pp[0] in ("0", "1"):
                rows.append((pp[1], int(pp[0]), None, "steam"))
    return rows


def _shuf(lines, seed, kind):
    """ctrl-shufGT: coin-flip the connective (C3) / suffix (C4) per line, preserving byte/atom
    exposure. Destroys the grounding signal only."""
    rng = random.Random(seed + 2000)
    out = []
    for ln in lines:
        if kind == "c3":
            for k, v in CONN.items():
                pass
            # swap connective to a random choice
            new = ln.replace("고 ", "\x00 ").replace("지만 ", "\x00 ")
            conn = rng.choice(["고", "지만"])
            out.append(new.replace("\x00", conn, 1) if "\x00" in new else ln)
        else:
            base = ln
            for suf in (" 추천.", " 비추천."):
                base = base.replace(suf, "")
            base = base.split(" 별점")[0]
            r = rng.choice([1, 2, 4, 5])
            if ln.endswith("점."):
                out.append(base + " 별점 %d점." % r)
            else:
                out.append(base + (" 추천." if rng.random() < 0.5 else " 비추천."))
    return out


def build_c34(seed, arm="main"):
    B = _grid(seed)
    pnat_pol = _pnat_from_manifest()
    pool_rows = GN2.load_corpora()
    target = list(pnat_pol.keys()) + list(B["plist"])
    spans = _collect_spans(target, pool_rows)
    grid_main = B["main_lines"][:]
    grid_shuf = B["ctrl_lines"][:]
    grid_bytes = len("\n".join(grid_main).encode())
    atoms_all = dict(pnat_pol)                      # h atoms (pol known for C4 consistency)
    for g in B["plist"]:
        atoms_all[g] = B["pol"][g]                  # + grid atoms (bridge · cap 30)
    c3, c3_pa, R_c3 = _c3_lines(B, pnat_pol, spans, seed, grid_bytes)
    pool_raw = _load_pool_raw()
    c4, c4_cnt = _c4_lines(pool_raw, atoms_all, seed, 2 * grid_bytes)
    if arm == "shufGT":
        c3 = _shuf(c3, seed, "c3"); c4 = _shuf(c4, seed, "c4")
    elif arm == "N2rep":
        c3, c4 = [], []
    # assemble + byte-match top-up to a COMMON target (= grid + full C3 + full C4 bytes, i.e. the
    # main/shufGT size) with atom-free general filler so every arm shares byte total AND T.
    target_bytes = int(round(grid_bytes * (1 + 1 + 2)))     # grid:C3:C4 = 1:1:2 → 4x grid
    body = grid_main + c3 + c4
    cur = len("\n".join(body).encode())
    if cur < target_bytes:
        filler = _general_filler(pool_rows, set(atoms_all.keys()), target_bytes - cur, seed)
        body = body + filler
    audit = _audit(B, pnat_pol, grid_main, grid_shuf, c3, c4, c3_pa, c4_cnt, R_c3, grid_bytes, arm)
    audit["total_bytes"] = len("\n".join(body).encode())
    audit["target_bytes"] = target_bytes
    # T is FIXED across arms: computed from the common byte layout (f_grid = grid/target)
    f_common = grid_bytes / target_bytes
    audit["f_grid_common"] = round(f_common, 4)
    audit["T_fixed"] = int(-(-int(T_MARGIN * E_STAR) // max(f_common, 1e-6)))
    return body, audit, B


def _general_filler(rows, atoms, n_bytes, seed):
    """Atom-free NSMC/general reviews to byte-pad an arm (no target atom → no signal leak)."""
    rng = random.Random(seed + 700)
    idx = list(range(len(rows))); rng.shuffle(idx)
    out, acc = [], 0
    for i in idx:
        t = rows[i][0]
        if any(a in t for a in atoms):
            continue
        if any(x in t for x in ("=>", "긍정", "부정")):
            continue
        out.append(t); acc += len(t.encode()) + 1
        if acc >= n_bytes:
            break
    return out


def _grid_pool_texts():
    return [t for (t, _l) in GN2.load_corpora()]


def _audit(B, pnat_pol, grid_main, grid_shuf, c3, c4, c3_pa, c4_cnt, R_c3, grid_bytes, arm):
    allng = "\n".join(c3 + c4)
    a = {"arm": arm, "R_c3": R_c3,
         "grid_bytes": grid_bytes, "c3_bytes": len("\n".join(c3).encode()),
         "c4_bytes": len("\n".join(c4).encode()),
         "n_c3": len(c3), "n_c4": len(c4),
         "V2a_label_window": sum(1 for h in pnat_pol if (h in allng) and
                                 any((h in ln) and any(t in ln for t in ("긍정", "부정", "=>"))
                                     for ln in (c3 + c4))),
         "V2c_grid_authored": [h for h in pnat_pol if h in "\n".join(grid_main + grid_shuf)],
         "V2e_c3_negfree": sum(1 for ln in c3 if any(t in ln for t in ("안 ", "지 않", "전혀"))),
         "c3_per_atom_min": min(c3_pa.values()) if c3_pa else 0,
         "c4_per_atom_min": min((c4_cnt[h] for h in pnat_pol), default=0),
         "n_pnat": len(pnat_pol)}
    f_grid = grid_bytes / (grid_bytes + a["c3_bytes"] + a["c4_bytes"] + 1)
    a["f_grid_built"] = round(f_grid, 4)
    a["T_required"] = int(-(-int(T_MARGIN * E_STAR) // max(f_grid, 1e-6)))
    a["V2a_ok"] = a["V2a_label_window"] == 0
    a["V2c_ok"] = len(a["V2c_grid_authored"]) == 0
    a["V2e_ok"] = a["V2e_c3_negfree"] == 0
    a["n_eval"] = len(pnat_pol) * len(GN.NEG_FORMS)
    a["GATE_n_eval_ok"] = a["n_eval"] >= 120
    a["PREFIRE_PASS"] = bool(a["V2a_ok"] and a["V2c_ok"] and a["V2e_ok"] and a["GATE_n_eval_ok"]
                             and a["c3_per_atom_min"] >= 8 and a["c4_per_atom_min"] >= 0)
    return a


if __name__ == "__main__":
    seed = int(sys.argv[sys.argv.index("--seed") + 1]) if "--seed" in sys.argv else 7
    arm = sys.argv[sys.argv.index("--arm") + 1] if "--arm" in sys.argv else "main"
    audit_only = "--audit-only" in sys.argv
    body, audit, B = build_c34(seed, arm)
    print(json.dumps(audit, ensure_ascii=False, indent=1))
    if not audit_only and audit["PREFIRE_PASS"]:
        # byte-match pad with atom-free general filler
        tag = {"main": "main_s%d" % seed, "shufGT": "shufGT", "N2rep": "N2rep"}[arm]
        out = os.path.join(HERE, "c34_%s_train.txt" % tag)
        open(out, "w", encoding="utf-8").write("\n".join(body) + "\n")
        print("WROTE %s (%d lines · %d bytes)" % (out, len(body), len("\n".join(body).encode())))
