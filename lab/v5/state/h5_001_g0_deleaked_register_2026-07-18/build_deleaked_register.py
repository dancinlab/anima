#!/usr/bin/env python3
"""H5_001 G-0 — constructed DELEAKED register: grammar + generator + panel + closed-form audits ($0).

SPEC: state/h5_001_g0_design_2026-07-18/SPEC_deleaked_register_g0_fable5.md (Fable design gate, 2026-07-18).
SSOT: anima-v5 ARCHITECTURE.json → defect-encoding · lever.g0-construction · next-gate.ladder.

The register lever, mechanically: v4's H_005 measured its learned-values K3 (A-χ̂ 0.82/0.71 vs hand 1.0)
under a TEMPLATIC register whose surface gave the concord bit away — the G3-0d probe read φ→hon = 1.0
held-out. The deleaked register must make the surface STOP predicting gold_k / hp_k / pos_k on all byte
n-grams n≤4 (A1 census ≤ 0.5+ε) WHILE the trunk can still learn the rule (A2, measured at G-0k).

The ONE surviving construction (SPEC §2, three parity traps rejected by count BEFORE any code):
  constant-시-count marking over site-isomorphic verb sites + implicit-subject adverbial clauses
  (±시 free by a pre-registered axiom extension, NEVER entering gold) + decoy 님-contexts
  ([님의]/[님도] balancers) for the pos_k channel — the templatic register leaked pos_k at n=4 via
  [님+의] vs [님+도] (verified present in v4's f2″ panel, 180/192 items each).

Reused verbatim from anima-v4 build_honbind_multi.py (the codebook is orthogonal to surface — changing it
would be a second lever): the [6,3] GF(4)-MDS strength-2 orthogonal array `_codeword`, the cell→(hp,pos)
map, and `_gold_flip`. The gold rule cell→bit is UNCHANGED; only the surface realization deleaks.

Stdlib only, deterministic, NO `random` (H_008's first SWAP-XOR-B build failed A3 at worst-byte 0.677 from
random sampling — the priced lesson; the census bar ε = 1/(2·m_min) = 0.021 only holds under exact balance).

Run:  python3 state/h5_001_g0_deleaked_register_2026-07-18/build_deleaked_register.py
Exit: 0 iff every δ≥1 passes A1/A3/A4 + codebook + free-slot + disjointness + anti-parity, AND the census
      unit-test fails a planted 0.75 count-leak fixture (collector-frozen discipline).
"""

from __future__ import annotations

import itertools
import json
import os
from collections import defaultdict

_HERE = os.path.dirname(os.path.abspath(__file__))
_ANS = ("앞", "뒤")                              # answer tokens (앞/뒤), 3 bytes each, differ at byte 0
EPS_PANEL = 1 / (2 * 24)                          # 0.0208 — m_min=24 (smallest crossing cell, n=192)
EPS_DRILL = 1 / (2 * 64)                          # 0.0078 — drill min cell >= 64


# ============================================================ codebook (REUSED from v4, verbatim)
_GF_MUL = [[0, 0, 0, 0], [0, 1, 2, 3], [0, 2, 3, 1], [0, 3, 1, 2]]
def _gadd(a, b): return a ^ b
def _gmul(a, b): return _GF_MUL[a][b]
_A_COLS = [(1, 1, 1), (1, 2, 3), (1, 3, 2)]
def _codeword(m):
    parity = []
    for col in _A_COLS:
        acc = 0
        for mk, ak in zip(m, col):
            acc = _gadd(acc, _gmul(mk, ak))
        parity.append(acc)
    return list(m) + parity
# GF(4) elem -> (cell_name, hp, honored_position). hp = honorific present; pos = which arg noun is honored.
_CELL_BY_GF = {
    0: ("SI_N1", 1, 1), 1: ("SI_N2", 1, 2), 2: ("PL_N1", 0, 1), 3: ("PL_N2", 0, 2),
}
def _gold_flip(hp, honored_position):
    return 1 ^ hp ^ (honored_position - 1)        # 0 = 앞/N1, 1 = 뒤/N2


# ============================================================ deleaked pools (SPEC §3 · A3: A7′ carried)
# Argument noun pools carried structurally from v4 SPEC §1 (6+6 held-out, substring-disjoint). The
# recombination axis stays "argument noun lexemes only" — everything else (adverbial verbs, frame words,
# decoy nouns) is DRILLED register machinery.
HON6 = ["어머님", "회장님", "스승님", "박사님", "원장님", "총장님"]        # drilled honorific args
PLAIN6 = ["조카", "후배", "제자", "비서", "조수", "신입"]                  # drilled plain args
HON_HELD = ["사장님", "교수님", "부장님", "국장님", "실장님", "차장님"]    # held-out honorific (f2d)
PLAIN_HELD = ["동생", "이웃", "손자", "친구", "동료", "청년"]              # held-out plain (f2d)

# Verb stem pool — SHARED between contested RC sites and adverbial sites (F-3 full site isomorphism):
# identical stems ⇒ identical allomorphy (으시/시), so the same 시-bearing bytes occur at BOTH site types.
# No pool-disjoint adverbial verbs (that would CREATE a stem→site lookup shortcut = H_005's shape, F-3).
# F-6a: all stems VOWEL-ending so the honorific is a uniform +3B (시) — replaces 웃 (consonant stem,
# 으시 = +6B) with 만나 (시 = +3B), matching 오/떠나. Uniform 시-width shrinks every sensitive span and
# simplifies the F-6b padding arithmetic (ADJUDICATION3 §3.2). Surface-only; gold is cell-derived.
VERBS = [("만나", "만나는", "만나시는"), ("오", "오는", "오시는"), ("떠나", "떠나는", "떠나시는")]
ADV_VERBS = VERBS                                                    # F-3: same stem pool, no disjoint set
FRAME_WORDS = ["마당", "동네", "거리", "골목", "시장", "광장", "학교", "공원"]   # adverbial FRAMEWORDs (drilled)
MATRIX_FRAMES = ["기다렸다", "기다렸어요", "기다렸음", "기다렸네"]         # matrix paraphrase frames (drilled)


# (the per-conjunct surface is built inline in emit's _emit_one — F-2 needs a flippable hp there;
#  the former _adv_clause/_adv_pool path was superseded by the inline F-5 mirror and is deleted.)

# F-6b filler — licensed 1-syllable manner adverbs (3 bytes each), used ONLY to pad a region/prefix/tail
# to its exact quantized width W. Grammatical as a matrix/adjunct adverb, never touches the contested core.
FILL = ["늘", "잘", "곧", "또", "막", "꼭", "참", "좀"]
PREFIX_SCENE = ["오늘", "어제", "아침에", "저녁에", "여기서", "거기서", "그날", "그때"]  # matrix scene-setters


def _fill(need, key):
    """A string of EXACTLY `need` bytes of licensed filler (3B adverbs + space separators; residual < 4B
    padded with spaces). `key` (an int derived from (k, rot) — NEVER a label/flip/slot/mi) only varies WHICH
    adverbs, never the length ⇒ the padding is byte-identical across the orbit ⇒ label-inert (no count key
    can read it). need is label-independent by construction (region width = f(k,rot), measured constant)."""
    if need <= 0:
        return ""
    out, used, i = [], 0, 0
    while need - used >= 4:                    # room for a 3B adverb + a 1B space
        out.append(FILL[(key + i) % len(FILL)]); out.append(" "); used += 4; i += 1
    out.append(" " * (need - used))            # residual 0..3 bytes as spaces
    return "".join(out)


def _pad_to(s, W, key):
    """Pad string `s` to EXACTLY W bytes: s + one space + filler. Asserts s fits (< W)."""
    nat = len(s.encode())
    assert nat < W, f"segment {nat}B >= W={W} (raise W)"
    return s + " " + _fill(W - nat - 1, key)


# ============================================================ δ dial (SPEC §4)
# W = quantized segment width (F-6b): every item is L = 8W bytes — prefix(W) · region 0..5 (W each) ·
# tail(W) — so every census bin boundary (mW, L−mW) coincides with a segment edge and each (g,bin) key
# degenerates to per-region presence (ADJUDICATION3). W ≥ max natural region width + headroom, per δ.
# W (filler fraction) is the ONE F-1-safe hardness axis (G-0k SPEC finding A): the former order/jitter
# keys were declared but NEVER read by build_delta — order is subsumed by the F-5 slot orbit and jitter
# breaks the F-1 anti-parity audit (variable mirror count ⇒ non-constant si_total), so δ3=δ4=δ5 were
# byte-identical (a fake knee). Spacing W gives ≥5 genuinely distinct settings; δ≤3 surfaces are
# unchanged so the existing G-0 PASS stays pinned.
DELTA = {
    0: dict(F=1, D=0, W=96),    # templatic anchor (report-only, census FAILS by design)
    1: dict(F=2, D=2, W=96),    # minimal census-clean (quantized layout)
    2: dict(F=4, D=2, W=96),    # + paraphrase (frame variety)
    3: dict(F=4, D=2, W=120),   # + wider quantum
    4: dict(F=4, D=2, W=144),   # + wider still (more label-inert filler fraction)
    5: dict(F=8, D=2, W=168),   # max filler fraction + frame variety
}




def build_delta(delta):
    """Emit drill grid + f2d + f1d panels for one δ. Returns dict of item lists."""
    conf = DELTA[delta]
    out = {"drill": [], "f2d": [], "f1d": []}
    messages = list(itertools.product(range(4), repeat=3))          # 64 codewords
    assert len(messages) == 64

    # A4 gold balance for the SIZED panels (f2d n=192, f1d n=64): the orbit needs COMPLETE 8-member sets
    # per message (else hp/pos aren't balanced per k), so a panel of n items covers exactly n/8 messages.
    # A naive prefix slice (out[:192]) took the first 24 messages in itertools order — a gold-IMBALANCED
    # subset (measured f2d mean 0.4722, f1d 0.4167). Instead pick a subset via complement-pairing: every
    # codeword m has a partner p with gold_pattern(p) = ¬gold_pattern(m) (verified: all 64 paired), so any
    # set of complement-pairs is gold-balanced 50/50 at EVERY conjunct k (measured per-k 0.5 for n=24/64).
    def _gold_pat(m):
        return tuple(_gold_flip(*_CELL_BY_GF[s][1:]) for s in _codeword(m))
    _by_pat = {}
    for m in messages:
        _by_pat.setdefault(_gold_pat(m), []).append(m)
    def _balanced_msgs(n):
        used, chosen = set(), []
        for m in messages:
            if m in used:
                continue
            comp = tuple(1 - x for x in _gold_pat(m))
            parts = [p for p in _by_pat.get(comp, []) if p not in used and p != m]
            if not parts:
                continue
            chosen += [m, parts[0]]
            used.add(m); used.add(parts[0])
            if len(chosen) >= n:
                break
        return chosen[:n]

    SI_BUDGET = 2          # per-conjunct constant 시-count over {contested}∪{ADV} (F-1); ≥1 so hp=0 conjuncts
                           # still carry 시 at an ADV site (that is what makes the 시-gram support balanced)

    def _emit_one(panel, hon_pool, plain_pool, decoy_pool, frame_id, rot, mi, m, flip, slot):
        """Emit one sentence. flip (F-2 involution): a per-conjunct bool list — where True, BOTH the contested
        verb's ±시 (hp) AND the honored position (pos = 의/도 noun order) are flipped from their cell values,
        with gold recomputed. The 4-item orbit {no-flip, hp+pos-flip, ...} balances every 시-gram AND every
        noun⊗particle/position gram across hp=0/1 AND pos=1/2 at the SAME site/bin by symmetry (SPEC §5).
        Flipping both is necessary: flipping hp alone left pos cell-determined ⇒ a posbin key localized pos
        to the last conjunct (measured: 님의/님도 → pos_5 at bin s7/e0, support 96)."""
        code = _codeword(m)
        W = conf["W"]                                    # F-6b quantized segment width (bytes)
        conjs = []
        for k in range(6):
            cell, hp0, pos0 = _CELL_BY_GF[code[k]]
            hp = (1 - hp0) if flip[k] else hp0               # F-2: flip hp on the contested verb
            pos = (3 - pos0) if flip[k] else pos0            # F-2: flip pos (1↔2) = swap 의/도 noun order
            hon = hon_pool[(k + rot) % len(hon_pool)]        # F-3-adjacent: rotate hon (kill k-determinism)
            plain = plain_pool[(k + 2 * rot) % len(plain_pool)]
            verb = VERBS[k % len(VERBS)]
            stem, pf, hf = verb
            vf = hf if hp == 1 else pf
            n1, n2 = (hon, plain) if pos == 1 else (plain, hon)
            core = f"{vf} {n1}의 {n2}도"
            # F-5 region-mirror decoy (ADJUDICATION2 §2): the adjunct is this region's core with the noun
            # ROLES EXCHANGED (pos-complement) AND the honorific COMPLEMENTED (hp-complement), + a frame
            # licensor. Then per region the chunk multiset = {[V-adn(±시) H의 P도], [V′-adn(∓시) P의 H도]}:
            #   • pos-complement ⇒ all four bridges {H의,H도,P의,P도} occur once per region in EVERY item
            #     (kills presence/count/junction pos-keys — Fable's measured leak family);
            #   • hp-complement ⇒ the mirror bears 시 IFF the core does not, so regional 시-count = 1 always
            #     (F-1 constant, independent of hp; my prior [1,2] bug was an un-complemented si-budget);
            #   • the F-2 orbit flip already exchanges which string is "core" ⇒ support closes under ι.
            # F-3: the mirror uses the SAME verb stem as the core, so 시-form bytes are byte-identical at
            # both sites — no gram can tell "which verb bears 시" (= hp). A distinct mirror stem would let a
            # stem gram identify the site and re-leak hp (measured: hp_k back to 1.0 when stems differed).
            mirror_hp = 1 - hp                                    # hp-complement ⇒ constant regional 시-count
            av_vf = hf if mirror_hp == 1 else pf                 # SAME verb (stem, pf, hf) as the core
            mn1, mn2 = (n2, n1)                                   # role-exchange: swap the two core nouns
            # frame index must be gold-INDEPENDENT: gold_k = f(message m, k), so any mi-dependence makes the
            # frame word's byte-count predict gold_k (measured: 마(마당) count 2↔1 = gold_2 0↔1, score 1.0).
            # Keying on (k, rot) only — never mi — makes every frame value see all messages ⇒ gold-balanced.
            frame = FRAME_WORDS[(k + rot) % len(FRAME_WORDS)]
            mirror = f"{av_vf} {mn1}의 {mn2}도 {frame}에서"
            # F-5 slot-order — INDEPENDENT of the pos/hp flip (a separate binary `slot[k]`), so which of
            # {core, mirror} sits last (nearest the region's high position bin) is UNCORRELATED with pos.
            # The slot-orbit takes slot[k] both values equally at every k ⇒ the gold-bearing core lands in
            # each slot equally often at EVERY conjunct's bin (an earlier flip-tied version left slot⊥pos
            # coupled, leaving pos_4 at bin s6 = 1.0; measured fix: 님의@s7 96/0 → 48/48).
            core_last = (slot[k] == 1)
            chunks = ([mirror, core] if core_last else [core, mirror]) if conf["D"] else [core]
            region_nat = " ".join(chunks)
            # F-6b: pad this region to EXACTLY W bytes so it occupies one census bin. Filler is (k,rot)-keyed
            # (label-independent — region width = f(k,rot), measured orbit-constant), so the pad is byte-
            # identical across the orbit and no (g,bin) key can read a label off it.
            region = _pad_to(region_nat, W, key=k * 3 + rot)
            advs = [mirror] if conf["D"] else []
            gf = _gold_flip(hp, pos)
            si_total = (1 if hp == 1 else 0) + ((1 if mirror_hp == 1 else 0) if conf["D"] else 0)  # F-1 const
            conjs.append({"cell": cell, "hp": hp, "honored_position": pos, "surface": region_nat,
                          "region": region, "advs": advs, "hon_lexeme": hon, "plain_lexeme": plain,
                          "n1_lexeme": n1, "n2_lexeme": n2, "gold_flip": gf, "gold_token": _ANS[gf],
                          "si_total": si_total,
                          # G-0k node-span sources (exact byte offsets derived below): cv/n1of/n2do are
                          # the core eojeols, mirror the whole ADV clause, core_last the slot order.
                          "_cv": vf, "_n1of": f"{n1}의", "_n2do": f"{n2}도",
                          "_mirror": mirror, "_core_last": core_last})
        mtail = MATRIX_FRAMES[frame_id % min(conf["F"], len(MATRIX_FRAMES))]
        # F-6b bin-quantized layout: L = 8W = prefix(W) · region 0..5 (W each) · tail(W). Segments are each
        # EXACTLY W bytes and concatenated with NO extra separator, so every bin boundary (mW) lands on a
        # segment edge. prefix/tail are (rot)-keyed, label-inert. tail ends with the " => " answer marker.
        prefix = _pad_to(PREFIX_SCENE[rot % len(PREFIX_SCENE)], W, key=rot)
        tail = _pad_to(mtail, W - 4, key=rot + 1) + " => "
        surface = prefix + "".join(c["region"] for c in conjs) + tail
        assert len(surface.encode()) == 8 * W, (len(surface.encode()), 8 * W, panel, delta)
        # G-0k node_spans + support_edges (SPEC §2.2/§4). Node ids: conjunct k → ADV=4k, CONTESTED_V=4k+1,
        # N1=4k+2, N2=4k+3; TAIL=24, ANS=25. Offsets are EXACT by construction: region k = [W(k+1),W(k+2)),
        # chunk order = slot, each eojeol owns its trailing space (v4 convention). Filler/prefix/tail-pad =
        # UNMAPPED (NULL). Re-derived + asserted by A_map/A_sup in audit_delta before exit.
        blen = lambda s: len(s.encode())
        d_on = bool(conf["D"])
        node_spans = []
        for k, c in enumerate(conjs):
            off = W * (k + 1)
            order = (["mirror", "core"] if c["_core_last"] else ["core", "mirror"]) if d_on else ["core"]
            for kind in order:
                if kind == "mirror":
                    end = off + blen(c["_mirror"]) + 1          # whole ADV clause + trailing space
                    node_spans.append([off, end, 4 * k]); off = end
                else:
                    for nid, piece in ((4 * k + 1, c["_cv"]), (4 * k + 2, c["_n1of"]), (4 * k + 3, c["_n2do"])):
                        end = off + blen(piece) + 1             # eojeol + trailing space
                        node_spans.append([off, end, nid]); off = end
        node_spans.append([7 * W, 7 * W + blen(mtail) + 1, 24])   # TAIL = mtail + trailing space
        node_spans.append([8 * W - 3, 8 * W, 25])                 # ANS = final "=> " (3 bytes)
        node_spans.sort()
        head_a, head_g = {}, {}
        for k in range(6):
            head_a[4 * k + 1] = 4 * k + 2; head_g[4 * k + 1] = 4 * k + 3   # THE contested RC edge (N1 vs N2)
            head_a[4 * k + 2] = 4 * k + 3; head_g[4 * k + 2] = 4 * k + 3   # N1 → N2 (agreed)
            head_a[4 * k + 3] = 24;        head_g[4 * k + 3] = 24          # N2 → TAIL (agreed)
            if d_on:
                head_a[4 * k] = 24;        head_g[4 * k] = 24              # ADV → TAIL (agreed, inert)
        head_a[25] = 24; head_g[25] = 24                                    # ANS → TAIL (agreed)
        for c in conjs:                                                     # drop span-source scratch fields
            for kk in ("_cv", "_n1of", "_n2do", "_mirror", "_core_last"):
                c.pop(kk, None)
        return {"panel": panel, "delta": delta, "rot": rot, "msg": list(m), "frame_id": frame_id,
                "conjuncts": conjs, "surface": surface, "W": W,
                "node_spans": node_spans, "support_edges": {"head_a": head_a, "head_g": head_g},
                "gold_flips": [c["gold_flip"] for c in conjs],
                "gold_pattern": "".join(c["gold_token"] for c in conjs),
                "cells": [c["cell"] for c in conjs], "node_roles": _node_roles(conjs),
                "char_len": len(surface), "si_totals": [c["si_total"] for c in conjs]}

    def emit(panel, hon_pool, plain_pool, decoy_pool, frame_id, rot, msgs=None):
        for mi, m in enumerate(messages if msgs is None else msgs):
            # F-2 involution orbit — 4 flip patterns. ι flips hp AND pos together, so per (msg,k) the orbit
            # realizes only the DIAGONAL of (hp,pos) — 2 of 4 combos (measured {2:144}), e.g. {(1,1),(0,2)}.
            # This is BY DESIGN: ι preserves gold = 1^hp^(pos-1), so the orbit holds the label fixed while
            # balancing hp AND pos each MARGINALLY across k (both take 0/1 equally over the 4 patterns). It
            # canNOT balance gold (that needs pair-closed supports + F-6 bin-inert geometry, ADJUDICATION3).
            flips = [
                [False] * 6,
                [True] * 6,
                [(k % 2 == 0) for k in range(6)],
                [(k % 2 == 1) for k in range(6)],
            ]
            # F-5 slot orbit — INDEPENDENT of flip: the two parity patterns are each balanced per-k
            # ([k even]→T at even k, [k odd]→T at odd k ⇒ at any fixed k the pair = {one T, one F}).
            # Crossed with the 4 flips, (flip[k], slot[k]) hits all 4 combos equally at every k ⇒ which
            # sub-slot (core vs mirror) sits nearest region k's position bin is UNCORRELATED with pos_k,
            # killing the bin-localized 님의/님도 → pos leak (measured pos_4@s6 = 1.0 under the old
            # flip-tied slot). 4×2 = 8 orbit members per message, exact balance (no random sampling).
            slots = [
                [(k % 2 == 0) for k in range(6)],
                [(k % 2 == 1) for k in range(6)],
            ]
            for fl in flips:
                for sl in slots:
                    out[panel].append(
                        _emit_one(panel, hon_pool, plain_pool, decoy_pool, frame_id, rot, mi, m, fl, sl))

    F = conf["F"]
    # F-4 decoy_pool: the SAME argument lexeme set as the core — drilled nouns on drill surfaces, held-out
    # nouns on the panel surfaces (§6 disjointness bans held-out from DRILL surfaces only; a held-out noun
    # in a decoy slot on an f2d surface adds no drill exposure).
    for frame_id in range(min(F, len(MATRIX_FRAMES) - 1)):
        for rot in range(3):
            emit("drill", HON6, PLAIN6, HON6 + PLAIN6, frame_id, rot)
    # f2d n=192 = 24 gold-balanced messages × 8-orbit, split into 3 rot-groups of 8 (each group = 4
    # complement-pairs ⇒ itself balanced) so held-out-noun assignment still varies across the panel.
    bal24 = _balanced_msgs(24)
    for r in range(3):
        emit("f2d", HON_HELD, PLAIN_HELD, HON_HELD + PLAIN_HELD, 0, r, msgs=bal24[r * 8:(r + 1) * 8])
    # f1d n=64 = 8 gold-balanced messages × 8-orbit, single rot.
    emit("f1d", HON6, PLAIN6, HON6 + PLAIN6, len(MATRIX_FRAMES) - 1, 0, msgs=_balanced_msgs(8))
    assert len(out["f2d"]) == 192 and len(out["f1d"]) == 64, (len(out["f2d"]), len(out["f1d"]))
    return out


def _node_roles(conjs):
    roles = []
    for c in conjs:
        for a in c["advs"]:
            roles.append("ADV")
        roles.append("CONTESTED_V"); roles.append("N1"); roles.append("N2")
    roles.append("TAIL"); roles.append("ANS")
    return roles


# ============================================================ A1 census (SPEC §5)
def _targets(item):
    """18 bits per sentence: gold_k, hp_k, pos_k for k=0..5."""
    t = {}
    for k, c in enumerate(item["conjuncts"]):
        t[f"gold_{k}"] = c["gold_flip"]
        t[f"hp_{k}"] = c["hp"]
        t[f"pos_{k}"] = c["honored_position"] - 1
    return t


def _ngrams(surf_bytes, n):
    return [bytes(surf_bytes[i:i + n]) for i in range(len(surf_bytes) - n + 1)]


def census(items, eps):
    """max over all byte n-grams (n∈1..4) × {presence, count, (g,posbin)} of majority-by-key predictiveness
    of any target, over grams with support ≥ m_min. posbin keys are BOTH-ENDS + "=>"-relative (§5 bug fix),
    votes are PER-SENTENCE not per-occurrence (§5 bug fix). Returns (worst, detail, per_target_max, top24)."""
    M_MIN = 24
    tkeys = [f"{p}_{k}" for p in ("gold", "hp", "pos") for k in range(6)]
    pres = defaultdict(lambda: defaultdict(list))
    cnt = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))   # gram->target->count->[vals]
    posb = defaultdict(lambda: defaultdict(list))                       # (gram,binkey)->target->[vals]
    for it in items:
        sb = it["surface"].encode("utf-8")
        tg = _targets(it)
        L = len(sb)
        arrow = sb.rfind(b" => ")                                       # "=>"-relative anchor (§5)
        seen_grams = defaultdict(int)
        seen_binkeys = set()                                            # per-SENTENCE dedup for posbin (§5)
        for n in (1, 2, 3, 4):
            for i in range(L - n + 1):
                g = bytes(sb[i:i + n])
                seen_grams[g] += 1
                bs = min(7, (i * 8) // max(L, 1))                       # bin from START
                be = min(7, ((L - i) * 8) // max(L, 1))                 # bin from END (both-ends, §5)
                ba = "n" if arrow < 0 else ("A" if i >= arrow else "B")  # after/before the "=>" anchor
                for binkey in ((g, "s", bs), (g, "e", be), (g, "a", ba)):
                    seen_binkeys.add(binkey)
        for g, c in seen_grams.items():
            for t in tkeys:
                pres[g][t].append(tg[t])                               # one vote per sentence (dedup'd)
                cnt[g][t][min(c, 4)].append(tg[t])
        for binkey in seen_binkeys:                                    # one vote per sentence per binkey
            for t in tkeys:
                posb[binkey][t].append(tg[t])

    def majority(vals):
        if not vals:
            return 0.0
        s = sum(vals) / len(vals)
        return max(s, 1 - s)

    worst, detail = 0.0, None
    per_target = defaultdict(float)
    top = []                                  # (score, target, keydesc, gram_decoded, support) — leak hunt
    def consider(vals, keytype, g, t, extra=""):
        nonlocal worst, detail
        if len(vals) < M_MIN:
            return
        sc = majority(vals)
        per_target[t] = max(per_target[t], sc)
        if sc > 0.55:
            try:
                gd = g.decode("utf-8")
            except UnicodeDecodeError:
                gd = repr(g)
            top.append((round(sc, 4), t, f"{keytype} n={len(g)}{extra}", gd, len(vals)))
        if sc > worst:
            worst, detail = sc, f"{keytype} n={len(g)}{extra} gram={g!r}→{t}"

    for g, tt in pres.items():
        for t, vals in tt.items():
            consider(vals, "presence", g, t)
    for g, tt in cnt.items():
        for t, cc in tt.items():
            for c, vals in cc.items():
                consider(vals, "count", g, t, f"={c}")
    for (g, ax, b), tt in posb.items():
        for t, vals in tt.items():
            consider(vals, "posbin", g, t, f"={ax}{b}")
    top.sort(reverse=True)
    return round(worst, 4), detail, {t: round(v, 4) for t, v in per_target.items()}, top[:24]


# ============================================================ codebook + free-slot audits (v4, recomputed)
def _panel_free_slots(items):
    pats = sorted({it["gold_pattern"] for it in items})
    M = [[0 if ch == "앞" else 1 for ch in p] for p in pats]
    K = len(M[0])
    def col_xor(cols):
        x = [0] * len(M)
        for j in cols:
            x = [a ^ M[i][j] for i, a in enumerate(x)]
        return x
    free = []
    for k in range(K):
        det = any(col_xor(list(sub)) == [row[k] for row in M]
                  for r in range(1, k + 1) for sub in itertools.combinations(range(k), r))
        if not det:
            free.append(k)
    return free


def _gf2_rank(rows):
    mat = [r[:] for r in rows]; rank = 0
    ncol = len(mat[0]) if mat else 0
    for col in range(ncol):
        piv = next((r for r in range(rank, len(mat)) if mat[r][col]), None)
        if piv is None:
            continue
        mat[rank], mat[piv] = mat[piv], mat[rank]
        for r in range(len(mat)):
            if r != rank and mat[r][col]:
                mat[r] = [a ^ b for a, b in zip(mat[r], mat[rank])]
        rank += 1
    return rank


# ============================================================ audits assembly
def audit_delta(delta, panels):
    res = {"delta": delta, "checks": {}, "pass": True}
    def chk(name, ok, detail):
        res["checks"][name] = {"pass": bool(ok), "detail": detail}
        if not ok and delta >= 1:
            res["pass"] = False

    for pname, items in panels.items():
        eps = EPS_DRILL if pname == "drill" else EPS_PANEL
        worst, det, per_t, top = census(items, eps)
        leakers = "; ".join(f"{sc}:{t}:{gd!r}({m})" for sc, t, kt, gd, m in top[:5])
        chk(f"A1_census_{pname}", worst <= 0.5 + eps + 1e-9,
            f"worst={worst} (bar {round(0.5+eps,4)}) at [{det}] · "
            f"per-target {dict(sorted(per_t.items(), key=lambda x: -x[1])[:4])} · top: {leakers}")

    # A4_geom (F-6b, exit-blocking): every item is EXACTLY 8W bytes and region k occupies exactly the byte
    # interval [W(k+1), W(k+2)) — so every census bin boundary (mW) coincides with a segment edge and no
    # (g,bin) key can straddle a region into the label (ADJUDICATION3). This is what licenses the census
    # PIN at every δ; if any realization breaks the invariant the audit says so before anything trains.
    W = DELTA[delta]["W"]
    geom_bad = []
    for pname, items in panels.items():
        for it in items:
            sb = it["surface"].encode()
            if len(sb) != 8 * W:
                geom_bad.append(f"{pname} len={len(sb)}≠{8*W}"); break
            if any(sb[W * (k + 1):W * (k + 2)] != c["region"].encode()
                   for k, c in enumerate(it["conjuncts"])):
                geom_bad.append(f"{pname} region interval mismatch"); break
    chk("A4_geom_bin_quantized", not geom_bad, f"L==8W({8*W}) & region k==[W(k+1),W(k+2)): "
        f"{'all items OK' if not geom_bad else geom_bad[:3]}")

    # A_map (G-0k, exit-blocking): re-derive every node span INDEPENDENTLY from conjunct fields by a
    # region-bounded substring search and assert == emitted node_spans. A wrong byte→node map silently
    # corrupts the φ→hon probe = the whole G-0k verdict, so this makes it a loud $0 failure (SPEC §2.3).
    map_bad = []
    for pname, items in panels.items():
        for it in items:
            sb = it["surface"].encode(); Wv = it["W"]; spans = it["node_spans"]
            exp = {}                                          # node_id -> expected content string (no space)
            for k, c in enumerate(it["conjuncts"]):
                # reconstruct from stored fields: cv = verb form by hp; n1of/n2do by pos order
                stem, pf, hf = VERBS[k % len(VERBS)]
                cv = hf if c["hp"] == 1 else pf
                exp[4 * k + 1] = cv
                exp[4 * k + 2] = f"{c['n1_lexeme']}의"
                exp[4 * k + 3] = f"{c['n2_lexeme']}도"
                if c["advs"]:
                    exp[4 * k] = c["advs"][0]
            emap = {nid: (s, e) for s, e, nid in spans}
            for nid, content in exp.items():
                k = nid // 4
                lo, hi = Wv * (k + 1), Wv * (k + 2)
                cb = (content + " ").encode()
                # region-bounded search: content must occur exactly once inside region k, at the emitted span
                hit = sb[lo:hi].find(content.encode())
                if hit < 0 or nid not in emap or sb[emap[nid][0]:emap[nid][1]] != cb:
                    map_bad.append(f"{pname} node {nid}: {content!r} vs {sb[emap.get(nid,(0,0))[0]:emap.get(nid,(0,0))[1]]!r}")
                    break
            else:
                # coverage/disjoint + TAIL/ANS + arity
                if not all(spans[i][1] <= spans[i + 1][0] for i in range(len(spans) - 1)):
                    map_bad.append(f"{pname} spans not disjoint/sorted")
                elif sb[spans[-1][0]:spans[-1][1]] != b"=> " or spans[-1][2] != 25:
                    map_bad.append(f"{pname} ANS span wrong")
                elif len(spans) != (26 if it["delta"] >= 1 else 20):
                    map_bad.append(f"{pname} δ{it['delta']} n_spans={len(spans)}")
            if map_bad:
                break
        if map_bad:
            break
    chk("A_map_node_spans", not map_bad, f"spans re-derived == emitted, region-bounded, disjoint: "
        f"{'all items OK' if not map_bad else map_bad[:3]}")

    # A_sup (G-0k): support_edges = exactly one CONTESTED edge per conjunct (head_a≠head_g at 4k+1 only),
    # everything else AGREED ⇒ 6 contested rows, offtop = 5/6 (SPEC §4; a contested ADV edge would be a
    # second lever). Asserted on f2d (structural, identical across items).
    se = panels["f2d"][0]["support_edges"]
    ha, hg = se["head_a"], se["head_g"]
    contested = [nid for nid in ha if ha[nid] != hg.get(nid)]
    sup_ok = (sorted(contested) == [4 * k + 1 for k in range(6)]
              and all(ha[4 * k + 1] == 4 * k + 2 and hg[4 * k + 1] == 4 * k + 3 for k in range(6)))
    chk("A_sup_contested_edges", sup_ok, f"contested rows={sorted(contested)} (expect [1,5,9,13,17,21], "
        f"6 = offtop 5/6)")

    # codebook + free-slot on f2d (recomputed OUTPUTS, expected {0,1,2,4} / rank / ceiling)
    f2d = panels["f2d"]
    free = _panel_free_slots(f2d)
    pats = sorted({it["gold_pattern"] for it in f2d})
    Mrows = [[0 if ch == "앞" else 1 for ch in p] for p in pats]
    rank = _gf2_rank(Mrows)
    ceiling = (len(free) * 0.5 + (6 - len(free)) * 1.0) / 6
    chk("codebook_free_slots", free == [0, 1, 2, 4], f"free={free} (expect [0,1,2,4])")
    chk("codebook_gf2_rank", rank == 4, f"GF(2) rank={rank} (expect 4)")
    chk("field_blind_ceiling", abs(ceiling - 0.667) < 0.01, f"ceiling={round(ceiling,4)} (expect 0.667)")

    # A3: pool disjointness (held-out args absent from drill surfaces) + non-corpus-family construction
    drill_surf = " ".join(it["surface"] for it in panels["drill"])
    held = HON_HELD + PLAIN_HELD
    leak = [h for h in held if h in drill_surf]
    chk("A3_heldout_disjoint", not leak, f"held-out args in drill: {leak}")

    # A4: exact balance — gold 50/50 per slot, hp/pos balanced
    for pname in ("f2d", "f1d"):
        items = panels[pname]
        golds = [c["gold_flip"] for it in items for c in it["conjuncts"]]
        bal = sum(golds) / len(golds)
        chk(f"A4_gold_balance_{pname}", abs(bal - 0.5) < 0.02, f"gold mean={round(bal,4)}")

    # anti-parity (F-1): the per-conjunct 시-count over {contested}∪{ADV} must be CONSTANT (= SI_BUDGET),
    # so no count key over 시-bytes can read hp_k. This audits the RIGHT invariant (the as-built adv-only
    # version passed at 0.0625 auditing the wrong one — the whole reason δ leaked hp at 1.0).
    if delta >= 1:
        all_totals = {t for it in panels["f2d"] for t in it["si_totals"]}
        chk("anti_parity_si_constant", len(all_totals) == 1,
            f"per-conjunct si_total values = {sorted(all_totals)} (must be a single constant)")

    return res


def census_unit_test():
    """The census code MUST FAIL a planted 0.75 count-leak fixture before it can certify anything
    (collector-frozen discipline; H_008 pattern). Build a corpus where a gram's count perfectly tails hp."""
    planted = []
    for hp in (0, 1):
        for _ in range(48):
            # surface where the byte '시' appears (hp+1)*2 times → count certifies hp (a real leak)
            marker = "시" * ((hp + 1) * 2)
            planted.append({"surface": f"{marker} 밥 => ",
                            "conjuncts": [{"gold_flip": hp, "hp": hp, "honored_position": 1}] * 6})
    worst, det, _, _ = census(planted, EPS_PANEL)
    return worst > 0.7, worst, det          # census MUST catch it (worst high)


def main():
    print("=" * 80)
    print("H5_001 G-0 — constructed DELEAKED register: build + closed-form audit")
    print("=" * 80)

    # 0) census self-test FIRST (frozen-collector discipline)
    caught, cw, cd = census_unit_test()
    print(f"\n[census unit-test] planted 0.75 count-leak → census worst={cw} ({cd}) · CAUGHT={caught}")
    if not caught:
        print("FAIL — census does not detect a planted leak; unsafe to certify. Exit 1.")
        return 1

    all_pass = True
    verdict = {}
    for delta in range(6):
        panels = build_delta(delta)
        res = audit_delta(delta, panels)
        verdict[f"d{delta}"] = res
        report = ("REPORT-ONLY (templatic anchor)" if delta == 0
                  else ("PASS" if res["pass"] else "FAIL"))
        print(f"\n--- δ{delta}  [{report}]  drill={len(panels['drill'])} f2d={len(panels['f2d'])} f1d={len(panels['f1d'])}")
        for name, c in res["checks"].items():
            flag = "PASS" if c["pass"] else ("rpt" if delta == 0 else "FAIL")
            print(f"    [{flag}] {name}: {c['detail']}")
        if delta >= 1 and not res["pass"]:
            all_pass = False
        # write artifacts
        for pname, items in panels.items():
            json.dump({"panel": pname, "delta": delta, "items": items},
                      open(os.path.join(_HERE, f"{pname}_d{delta}.json"), "w"), ensure_ascii=False)
    json.dump(verdict, open(os.path.join(_HERE, "g0_verdict.json"), "w"), ensure_ascii=False, indent=1)

    print("\n" + "=" * 80)
    print("G-0 VERDICT:", "PASS — deleaked register admissible for δ≥1; G-0k window pre-check next"
          if all_pass else "FAIL — a δ≥1 audit failed (fix before G-0k)")
    print("wrote {drill,f2d,f1d}_d{0..5}.json + g0_verdict.json")
    return 0 if (all_pass and caught) else 1


if __name__ == "__main__":
    raise SystemExit(main())
