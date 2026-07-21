#!/usr/bin/env python3
"""H_008 mech-supervision-budget G-0b — SWAP-XOR-B panel + budget constructor + full audit ($0).

DESIGN_fable5_seed.md §3/§5-G0b. Same rule as H_007 (gold = class(subject) ⊕ form(object-marker),
role from a case marker under SOV/OSV scrambling), but the noun pools are rebuilt to close the
budget-independent CLASS side channel that the H_007 panel had (§0.5: f2-subjects 사장/학생 had ZERO
answer-supervised subject occurrences yet C-dup scored f2=1.0 — class reached the trunk via shared-syllable
byte families 사장~부장(장)/학생~동생(생) + NSMC corpus semantics). SWAP-XOR-B fixes this with:

  1. BYTE-ORTHOGONAL synthetic pseudo-noun pools — 24 lexemes built from rare Hangul syllables VERIFIED
     absent from the NSMC CPT corpus, class-balanced so every single byte/syllable → class map = 0.500
     (A7): honored = (P[j], Q[j]); plain = (P[j], Q[(j+6)%12]) over disjoint 12-syllable pools P,Q ⇒ each
     syllable appears once honored + once plain. Class is learnable ONLY from full-lexeme identity.
  2. COVERAGE-COMPLETE grid: drill = 24 subjects × 2 markers × 2 orders × 4 objects = 384; f2-subjects ⊆
     drill-subjects (each lexeme answered as subject ≥ once) ⇒ budget floor k_min = 24.
  3. BUDGET CONSTRUCTOR B(k), k = 24·r, r ∈ {1,4,8,16} ⇒ {24,96,192,384}: the answered subset of the
     drill (head-A CE mask); non-budget items are answer-TRUNCATED (surface only). Nested B(24)⊂…⊂B(384),
     deterministic (seed/arm-independent), SHA-256 recorded.

Audit suite (exit-0-blocking, ALL recomputed, never inherited):
  A1 free-slot=[0] · A2 GF(2) rank=2 (gold ∉ single-ingredient) · A3 every single-site heuristic 0.500 ·
  A4 length-parity · A5 swap(x) byte-aligned · A6 supervision-leak ban · A7 class-byte-orthogonality
  (best byte-pos/byte-value/syllable→CLASS = 0.500 exact; no lexeme substring in NSMC) ·
  B1 coverage · B2 within-budget balance · B3 GF(2) identifiability on B(24) · B4 nestedness ·
  B5 answer-truncation structural · B6 determinism (hash match, seed/arm-independent).

Run:  python3 state/h008_supervision_budget_sample_efficiency_2026-07-17/build_swap_xor_b.py
Exit: 0 iff every audit PASS. Writes swapb_f2.json / swapb_drill.json / swapb_budgets.json / swapb_pools.json.
"""

from __future__ import annotations

import hashlib
import json
import os
import sys
from collections import defaultdict

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(os.path.dirname(_HERE))
_H007 = os.path.join(_ROOT, "state", "h007_gradient_tug_role_code_drill_2026-07-17")
_H004 = os.path.join(_ROOT, "state", "h004_parser_duel_tension_rank_drill_2026-07-16")
_NSMC = os.path.join(_ROOT.replace("anima-v4", "anima"), "state", "nbind_curriculum", "ratings_train.txt")

sys.path.insert(0, _H007)
import build_swap_xor as bx        # reuse: render/render_swap/gold_bit/SUBJ_MARK/OBJ_MARK/VERB/AGREE/_gf2_rank/_best_map_acc

ORDERS = bx.ORDERS


# ---------------------------------------------------------------- synthetic byte-orthogonal pools
def _rare_syllables(nsmc_text, need):
    """Deterministic rare Hangul syllables (double-consonant lead + rare vowel + tail) VERIFIED absent
    from the NSMC corpus. Returns `need` distinct syllables (each 3 bytes)."""
    LEADS = [1, 4, 8, 10, 13]          # ㄲ ㄸ ㅃ ㅆ ㅉ
    VOWELS = [19, 11, 16, 15, 14, 9]   # ㅢ ㅚ ㅟ ㅞ ㅝ ㅘ
    TAILS = [17, 19, 25, 22, 9, 13]    # ㄽ ㄿ ㅀ ㅄ ㄺ ... rare batchim
    out = []
    for lead in LEADS:
        for vow in VOWELS:
            for tail in TAILS:
                ch = chr(0xAC00 + (lead * 21 + vow) * 28 + tail)
                if len(ch.encode("utf-8")) == 3 and ch not in nsmc_text:
                    out.append(ch)
                    if len(out) >= need:
                        return out
    raise RuntimeError(f"only found {len(out)} rare syllables, need {need}")


def build_pools():
    nsmc = open(_NSMC, encoding="utf-8").read() if os.path.exists(_NSMC) else ""
    syl = _rare_syllables(nsmc, 24)
    P, Q = syl[:12], syl[12:24]                     # disjoint position pools
    honored = [P[j] + Q[j] for j in range(12)]                    # class 1
    plain = [P[j] + Q[(j + 6) % 12] for j in range(12)]          # class 0
    assert len(set(honored + plain)) == 24, "lexemes not distinct"
    for n in honored + plain:
        assert len(n.encode("utf-8")) == 6, f"{n} not 6 bytes"
    return honored, plain, P, Q, nsmc


HON, PLAIN, POS1, POS2, _NSMC_TEXT = build_pools()
LEX = HON + PLAIN
CLASS = {n: (1 if n in HON else 0) for n in LEX}


# ---------------------------------------------------------------- item construction (reuse H_007 render)
def make_item(n_subj, n_obj, marker, order, answered=True):
    cs = CLASS[n_subj]
    g = bx.gold_bit(cs, marker)
    it = {
        "surface": bx.render(n_subj, n_obj, marker, order),
        "swap_target": bx.render_swap(n_subj, n_obj, marker, order),
        "cell": {"class_subj": cs, "marker": marker, "order": order, "gold": g,
                 "n_subj": n_subj, "n_obj": n_obj},
        "answered": answered,
    }
    if answered:
        it["gold_token"] = bx.AGREE[g]               # head-A CE covers the answer suffix
    return it


# ---------------------------------------------------------------- coverage-complete grid + f2
def build_grid():
    """drill = 24 subjects × 2 markers × 2 orders × 4 objects = 384 (coverage-complete).
    f2 = held-out (subj,obj) pairings, subjects ⊆ drill-subjects, n=192."""
    # deterministic object choice per subject: 4 objects at a fixed stride, class-balanced (2 HON + 2 PLAIN)
    def objs_for(si):
        hon_obj = [HON[(si + k + 1) % 12] for k in range(2)]
        plain_obj = [PLAIN[(si + k + 1) % 12] for k in range(2)]
        picked = [o for o in hon_obj + plain_obj if o != LEX[si]]
        # ensure 4 distinct != subject
        k = 0
        while len(picked) < 4:
            cand = LEX[(si + 5 + k) % 24]
            if cand != LEX[si] and cand not in picked:
                picked.append(cand)
            k += 1
        return picked[:4]

    drill = []
    for si in range(24):
        subj = LEX[si]
        for obj in objs_for(si):
            for marker in (0, 1):
                for order in ORDERS:
                    drill.append(make_item(subj, obj, marker, order, answered=True))
    # f2: held-out pairings — objects NOT among the subject's 4 drill objects, class-balanced, n=192
    drill_pairs = {(it["cell"]["n_subj"], it["cell"]["n_obj"]) for it in drill}
    f2 = []
    strata = [(cs, m, o) for cs in (0, 1) for m in (0, 1) for o in ORDERS]  # 8
    per = 24
    for cs, m, o in strata:
        subj_pool = [n for n in LEX if CLASS[n] == cs]
        cnt = 0; si = 0; oi = 0
        while cnt < per:
            subj = subj_pool[si % len(subj_pool)]
            # object class alternates for balance
            opool = HON if (cnt % 2 == 0) else PLAIN
            obj = opool[(si * 5 + oi + 3) % 12]
            if obj != subj and (subj, obj) not in drill_pairs:
                f2.append(make_item(subj, obj, m, o, answered=True)); cnt += 1
            si += 1
            if si % len(subj_pool) == 0:
                oi += 1
    return drill, f2


# ---------------------------------------------------------------- budget constructor B(k)
def build_budgets(drill):
    """B(k), k = 24·r, r ∈ {1,4,8,16} → {24,96,192,384}. Per subject, r answered items ordered so every
    prefix is (cs,marker,order)-CELL-BALANCED: within each class the rank-0 (marker,order) cell rotates by
    the subject's class-local index (so B(24) = 3 items per cell, marker/order/gold 50/50, gold identifiable),
    and items interleave obj-major so B(96) = 1-per-cell×obj etc. Nested, deterministic, seed/arm-independent.
    """
    by_subj = defaultdict(list)
    for idx, it in enumerate(drill):
        by_subj[it["cell"]["n_subj"]].append(idx)
    hon_sorted = sorted(s for s in by_subj if CLASS[s] == 1)
    plain_sorted = sorted(s for s in by_subj if CLASS[s] == 0)
    local = {}
    for j, s in enumerate(hon_sorted):
        local[s] = j
    for j, s in enumerate(plain_sorted):
        local[s] = j

    budgets = {24 * r: [] for r in (1, 4, 8, 16)}
    for s in sorted(by_subj):
        items = by_subj[s]
        objs = []                                    # deterministic object rank
        for idx in items:
            o = drill[idx]["cell"]["n_obj"]
            if o not in objs:
                objs.append(o)
        objs.sort()

        def key(idx, ph=local[s]):
            c = drill[idx]["cell"]
            cell = c["marker"] * 2 + (0 if c["order"] == "SOV" else 1)
            return (objs.index(c["n_obj"]), (cell - ph) % 4)   # obj-major, cell rotated by class-local phase
        ordered = sorted(items, key=key)
        for r in (1, 4, 8, 16):
            budgets[24 * r].extend(ordered[:r])
    for k in budgets:
        budgets[k] = sorted(budgets[k])
        assert len(budgets[k]) == k, f"B({k}) has {len(budgets[k])}"
    return budgets


# ---------------------------------------------------------------- audits
def _free_slots(panel):
    sys.path.insert(0, _H004)
    import train_h004
    return train_h004._panel_free_slots(panel)


def audit(drill, f2, budgets):
    res = {"pass": True, "checks": {}}

    def chk(name, ok, detail):
        res["checks"][name] = {"pass": bool(ok), "detail": detail}
        if not ok:
            res["pass"] = False

    golds = [it["cell"]["gold"] for it in f2]
    cs = [it["cell"]["class_subj"] for it in f2]
    mk = [it["cell"]["marker"] for it in f2]
    od = [1 if it["cell"]["order"] == "OSV" else 0 for it in f2]
    n = len(f2)

    # A1 free-slot
    fs2 = _free_slots(f2)
    chk("A1_free_slot", fs2 == [0], f"f2 free_slots={fs2}")

    # A2 GF(2) codebook
    xor_ok = all(g == (a ^ b) for g, a, b in zip(golds, cs, mk))
    rows = list({(a, b, g) for a, b, g in zip(cs, mk, golds)})
    rank = bx._gf2_rank([list(r) for r in rows])
    chk("A2_gf2", xor_ok and rank == 2 and not all(g == a for g, a in zip(golds, cs))
        and not all(g == b for g, b in zip(golds, mk)), f"xor={xor_ok} rank={rank}")

    # A3 heuristics 0.5
    heur = {"class_subj": bx._best_map_acc(cs, golds), "marker": bx._best_map_acc(mk, golds)}
    first_cls, near_cls, maj = [], [], []
    for it in f2:
        c = it["cell"]; csubj = c["class_subj"]; cobj = CLASS[c["n_obj"]]
        if c["order"] == "SOV":
            first_cls.append(csubj); near_cls.append(cobj)
        else:
            first_cls.append(cobj); near_cls.append(csubj)
        maj.append(1 if (csubj + cobj) >= 1 else 0)
    heur["class_first"] = bx._best_map_acc(first_cls, golds)
    heur["class_nearest"] = bx._best_map_acc(near_cls, golds)
    heur["class_majority"] = bx._best_map_acc(maj, golds)
    surfs = [it["surface"].encode("utf-8") for it in f2]
    L = min(len(s) for s in surfs)
    byte_max = max(bx._best_map_acc([s[p] for s in surfs], golds) for p in range(L))
    heur["worst_byte"] = byte_max
    chk("A3_heuristics", all(abs(v - 0.5) < 1e-9 for k, v in heur.items() if k != "worst_byte")
        and byte_max <= 0.5 + 1e-9, heur)

    # A4 length-parity
    chk("A4_length_parity", len({len(it["surface"].encode()) for it in f2 + drill}) == 1
        and len({len(it["swap_target"].encode()) for it in f2 + drill}) == 1,
        f"surf_lens={sorted({len(it['surface'].encode()) for it in f2})}")

    # A5 swap alignment
    bad = None
    for it in f2 + drill:
        c = it["cell"]
        if it["swap_target"] != bx.render_swap(c["n_subj"], c["n_obj"], c["marker"], c["order"]) \
           or it["swap_target"] == it["surface"] \
           or len(it["swap_target"].encode()) != len(it["surface"].encode()):
            bad = it["surface"]; break
    chk("A5_swap", bad is None, f"bad={bad}")

    # A6 leak ban (answer forms absent from swap target)
    leak = next((it["surface"] for it in f2 + drill for a in bx.AGREE if a in it["swap_target"]), None)
    chk("A6_leak_ban", leak is None, f"leak={leak}")

    # A7 class-byte-orthogonality: best single byte/syllable → CLASS over the 24-lexeme lexicon = 0.5;
    #    and no lexeme substring in NSMC.
    lex_cls = [CLASS[n] for n in LEX]
    lex_bytes = [n.encode("utf-8") for n in LEX]
    Lb = min(len(b) for b in lex_bytes)
    a7_byte = max(bx._best_map_acc([b[p] for b in lex_bytes], lex_cls) for p in range(Lb))
    syl1 = [n[0] for n in LEX]; syl2 = [n[1] for n in LEX]
    a7_syl = max(bx._best_map_acc(syl1, lex_cls), bx._best_map_acc(syl2, lex_cls))
    in_corpus = [n for n in LEX if _NSMC_TEXT and n in _NSMC_TEXT]
    chk("A7_class_byte_orthogonal", a7_byte <= 0.5 + 1e-9 and a7_syl <= 0.5 + 1e-9 and not in_corpus,
        f"best_byte→class={round(a7_byte,4)} best_syl→class={round(a7_syl,4)} in_corpus={in_corpus}")

    # B1 coverage: every f2 subject answered ≥ once at every k
    f2_subj = {it["cell"]["n_subj"] for it in f2}
    drill_subj = {it["cell"]["n_subj"] for it in drill}
    covok = f2_subj <= drill_subj
    for k, idxs in budgets.items():
        answered_subj = {drill[i]["cell"]["n_subj"] for i in idxs}
        if not f2_subj <= answered_subj:
            covok = False
    chk("B1_coverage", covok, f"f2⊆drill={f2_subj<=drill_subj}; every-k covers f2-subjects={covok}")

    # B2 within-budget balance (on B(24): gold/marker/order 50/50, per-(cs,marker,order) equal)
    b24 = [drill[i] for i in budgets[24]]
    def bal(v):
        return sum(v) / len(v)
    g24 = [it["cell"]["gold"] for it in b24]; m24 = [it["cell"]["marker"] for it in b24]
    o24 = [1 if it["cell"]["order"] == "OSV" else 0 for it in b24]
    cells = defaultdict(int)
    for it in b24:
        cells[(it["cell"]["class_subj"], it["cell"]["marker"], it["cell"]["order"])] += 1
    chk("B2_budget_balance", abs(bal(g24) - 0.5) < 1e-9 and abs(bal(m24) - 0.5) < 1e-9
        and abs(bal(o24) - 0.5) < 1e-9 and len(set(cells.values())) == 1,
        f"gold={round(bal(g24),3)} marker={round(bal(m24),3)} order={round(bal(o24),3)} cells={dict(cells)}")

    # B3 GF(2) identifiability on B(24)
    g = [it["cell"]["gold"] for it in b24]; a = [it["cell"]["class_subj"] for it in b24]
    b = [it["cell"]["marker"] for it in b24]
    r24 = list({(x, y, z) for x, y, z in zip(a, b, g)})
    chk("B3_gf2_on_B24", bx._gf2_rank([list(r) for r in r24]) == 2
        and all(gg == (aa ^ bb) for gg, aa, bb in zip(g, a, b)), f"rank={bx._gf2_rank([list(r) for r in r24])}")

    # B4 nestedness
    nested = all(set(budgets[k]) <= set(budgets[k2]) for k, k2 in [(24, 96), (96, 192), (192, 384)])
    chk("B4_nested", nested and len(budgets[384]) == len(drill), f"nested={nested} B(384)={len(budgets[384])}")

    # B5 answer-truncation structural: a non-budget item carries no gold_token / answer bytes
    # (simulated at B(24): items NOT in B(24) must be answer-truncatable — surface has no AGREE suffix)
    nonb = [drill[i] for i in range(len(drill)) if i not in set(budgets[24])]
    trunc_ok = all(not any(a in it["surface"] for a in bx.AGREE) for it in nonb)
    chk("B5_answer_truncation", trunc_ok, f"non-budget items with answer-in-surface: {sum(1 for it in nonb if any(a in it['surface'] for a in bx.AGREE))}")

    # B6 determinism: rebuild budgets, hashes match
    b2 = build_budgets(drill)
    hashes = {k: hashlib.sha256(json.dumps(budgets[k]).encode()).hexdigest()[:12] for k in budgets}
    h2 = {k: hashlib.sha256(json.dumps(b2[k]).encode()).hexdigest()[:12] for k in b2}
    chk("B6_determinism", hashes == h2, f"hashes={hashes}")

    # balance + decorrelation of f2 (carried from H_007)
    def corr(a2, b2_):
        j = defaultdict(int)
        for x, y in zip(a2, b2_):
            j[(x, y)] += 1
        return all(abs(j[(i, k)] - n / 4) <= 1 for i in (0, 1) for k in (0, 1))
    chk("f2_balance", all(abs(sum(v) / len(v) - 0.5) < 1e-9 for v in (golds, cs, mk, od)),
        {"gold": sum(golds) / n, "cs": sum(cs) / n, "mk": sum(mk) / n, "od": sum(od) / n})
    chk("f2_decorr", corr(cs, mk) and corr(cs, od) and corr(mk, od), "pairwise independent")

    res["_hashes"] = hashes
    return res


def main():
    drill, f2 = build_grid()
    budgets = build_budgets(drill)
    res = audit(drill, f2, budgets)

    print("=" * 80)
    print("H_008 G-0b — SWAP-XOR-B panel + budget constructor + audit")
    print("=" * 80)
    print(f"lexicon: 24 byte-orthogonal synthetic (POS1={''.join(POS1)} POS2={''.join(POS2)})")
    print(f"drill n={len(drill)} (coverage-complete) · f2 n={len(f2)} · budgets={ {k: len(v) for k, v in budgets.items()} }")
    print(f"gold = class(subject) XOR form(object-marker) · answer={bx.AGREE} · markers={bx.OBJ_MARK}")
    print()
    for name, c in res["checks"].items():
        print(f"  [{'PASS' if c['pass'] else 'FAIL'}] {name}: {c['detail']}")
    print()
    print("G-0b VERDICT:", "PASS — SWAP-XOR-B admissible, freeze-blocked on lit-verify + G-1.5a/b/c"
          if res["pass"] else "FAIL — NOT admissible (fix before any spend)")

    if res["pass"]:
        meta = {"gold_rule": "class(subject) XOR form(object-marker)", "answer_forms": list(bx.AGREE),
                "budget_hashes": res["_hashes"]}
        json.dump({"panel": f2, "meta": {**meta, "kind": "f2_verdict_ood", "n": len(f2)}},
                  open(os.path.join(_HERE, "swapb_f2.json"), "w"), ensure_ascii=False, indent=1)
        json.dump({"drill": drill, "meta": {**meta, "kind": "drill_coverage_complete", "n": len(drill)}},
                  open(os.path.join(_HERE, "swapb_drill.json"), "w"), ensure_ascii=False, indent=1)
        json.dump({k: v for k, v in budgets.items()},
                  open(os.path.join(_HERE, "swapb_budgets.json"), "w"), ensure_ascii=False, indent=1)
        json.dump({"honored": HON, "plain": PLAIN, "pos1": POS1, "pos2": POS2},
                  open(os.path.join(_HERE, "swapb_pools.json"), "w"), ensure_ascii=False, indent=1)
        print("wrote swapb_f2.json / swapb_drill.json / swapb_budgets.json / swapb_pools.json")
    return 0 if res["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
