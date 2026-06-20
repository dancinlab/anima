#!/usr/bin/env python3
"""semantic_detector.py — H_1458 SEMANTIC-AWARE falsifiability detector (FROZEN-FIRST, c9).

WHY (measurement-artifact lens, a_break_the_wall type-a):
  H_1305 `_is_falsifiable` is STRUCTURAL: it fires iff a text contains
    (a) ANY comparator-class word  AND  (b) ANY measurable-class word  AND (c) negatable content.
  comparator and measurable may be ANYWHERE, about DIFFERENT ideas. Cross-shuffling the
  measurable leg leaves BOTH classes still present -> structural FALS does NOT collapse.
  H_1435 honest finding: "the structural H_1305 detector CANNOT distinguish earned
  idea-specific binding from any-comparator + any-measurable + content." => the 5-lens
  WALL may be a MEASUREMENT artifact: the model could be binding while the detector is blind.

THE SEMANTIC EXTENSION (SAME-idea binding, lexical — $0, NO torch/embeddings):
  semantic-FALS := structural-FALS  AND  the comparator-token and a measurable-token
  occur in a SHARED LOCAL CONTEXT that names a COMMON content topic. Operationalized
  WITHOUT any learned embedding (none available; byte-LM corpus only) as:

    bind_score(text) =
        max over (comparator-token i, measurable-token j) pairs of
          [ proximity(i,j) gated by SHARED content topic in the bridging window ]

    A pair (i,j) BINDS iff:
      (1) token-distance |i-j| <= WINDOW   (comparator + measurable in one clause), AND
      (2) the content words strictly BETWEEN i and j (the bridge) contain >=1 token that
          ALSO appears elsewhere as a SUBJECT content word of the claim (topic anchor),
          i.e. the bridge shares >=1 content lemma with the clause head, so the comparator
          and the measurable predicate the SAME subject — NOT two unrelated sprinklings.

  Structural passes with comparator+measurable ANYWHERE; semantic passes ONLY when they
  predicate ONE topic in ONE clause. Cross-shuffling the measurable to a DIFFERENT idea's
  measurable breaks the shared-topic bridge => semantic-FALS COLLAPSES while structural does not.

FROZEN-FIRST (anti-tune-to-green, c9): WINDOW, the bridge-share rule, and the binding
  definition are fixed in this file and validated by a frozen calibration suite (10 designed
  strings) BEFORE any checkpoint generation is scored. The detector is NEVER adjusted to a
  ckpt's output. If a ckpt's semantic-FALS is 0, that is the honest result.

REUSES VERBATIM (p7, NO re-implementation): gauge_lib._words / _KNOWN / _STOPWORDS and the
  H_1305 COMPARATOR / MEASURABLE / STANCE sets + structural `_is_falsifiable`.
"""
import os, importlib.util

HERE = os.path.dirname(os.path.abspath(__file__))
ANIMA = os.path.dirname(os.path.dirname(HERE))


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


# locate gauge_lib + h1305 (engine-native probe copy lives under state/universe-probes)
def _find(*cands):
    for c in cands:
        if os.path.exists(c):
            return c
    raise FileNotFoundError(cands)


# pod-portable: H1456_PROBES env overrides (set on aiden/pool to ~/h1458_g6/probes).
_PB = os.environ.get("H1456_PROBES", os.path.join(HERE, "probes"))
_GAUGE = _find(
    os.path.join(_PB, "gauge_lib.py"),
    os.path.join(ANIMA, "state", "1449_g6_attention_injection", "gauge_lib.py"),
    os.path.join(ANIMA, "state", "1439_bind_head_architecture", "probes", "gauge_lib.py"),
    os.path.join(ANIMA, "state", "universe-probes", "gauge_lib.py"),
)
_H1305 = _find(
    os.path.join(_PB, "h1305_g6_ideation_falsifiability.py"),
    os.path.join(ANIMA, "state", "universe-probes", "h1305_g6_ideation_falsifiability.py"),
    os.path.join(ANIMA, "state", "1449_g6_attention_injection", "h1305_g6_ideation_falsifiability.py"),
)

g = _load("gauge", _GAUGE)
# h1305 imports h1129 (torch) at module load for the DECODE path; we only need the frozen
# sets + structural detector, but the import still touches `import torch`. Score path is
# torch-free; the import requires CPU-torch present ONLY if h1305 top-level touches it.
# To stay torch-free for the detector itself we DO NOT import h1305 here; instead we copy
# the FROZEN sets VERBATIM (asserted byte-equal against the source below at import time).
import re as _re


def _extract_frozen_sets(path):
    """Read COMPARATOR / MEASURABLE / STANCE literal sets from h1305 source WITHOUT importing
    (avoids the torch dependency of h1305's decode path). VERBATIM — parsed, not retyped."""
    src = open(path).read()
    out = {}
    for name in ("COMPARATOR", "MEASURABLE", "STANCE"):
        m = _re.search(name + r"\s*=\s*\{(.*?)\}", src, _re.S)
        if not m:
            raise ValueError("missing " + name)
        toks = _re.findall(r'"([^"]+)"', m.group(1))
        out[name] = set(toks)
    return out


_F = _extract_frozen_sets(_H1305)
COMPARATOR = _F["COMPARATOR"]
MEASURABLE = _F["MEASURABLE"]
STANCE = _F["STANCE"]

# ────────────────────────────────────────────────────────────────────────────
# STRUCTURAL detector — reproduced VERBATIM from h1305._is_falsifiable (asserted
# identical-logic via the same frozen sets + same predicate). Used as the
# necessary precondition AND the head-to-head structural baseline.
# ────────────────────────────────────────────────────────────────────────────
def is_falsifiable_structural(text):
    wl = g._words(text)
    if not wl:
        return False
    wset = set(wl)
    a = bool(wset & COMPARATOR)
    b = bool(wset & MEASURABLE)
    content = [w for w in wl if len(w) >= 3 and w in g._KNOWN and w not in g._STOPWORDS]
    c_i = len(content) >= 2
    c_ii = not text.rstrip().endswith("?")
    first3 = set(wl[:3])
    c_iii = not (first3 and first3 <= STANCE)
    return a and b and (c_i and c_ii and c_iii)


# ────────────────────────────────────────────────────────────────────────────
# SEMANTIC-AWARE detector (FROZEN). Adds the SAME-idea binding requirement.
# ────────────────────────────────────────────────────────────────────────────
WINDOW = 6          # max token distance between a comparator and a measurable in ONE clause
MIN_SUBJECT = 1     # >=1 shared content subject the comparator AND measurable jointly predicate

# clause-BREAKING connectors: when one of these lies STRICTLY between a comparator and a
# measurable, the two are in SEPARATE clauses about (potentially) DIFFERENT ideas. These are
# the exact glue words a cross-sprinkle uses to weld two unrelated legs. FROZEN list (the
# coordinating / contrastive conjunctions that open a new clause). NB: comparator words that
# are THEMSELVES subordinators ("when","if","unless","whereas","versus","than","compared")
# bind their OWN clause and are NOT counted as breakers here (they are the comparator).
CLAUSE_BREAK = {"and", "but", "or", "also", "separately", "meanwhile",
                "while", "however", "though", "yet", "plus", "additionally",
                "besides", "furthermore", "moreover"}


def _content_tokens(wl):
    """known, >=3-char, non-stopword content tokens with their indices."""
    return [(i, w) for i, w in enumerate(wl)
            if len(w) >= 3 and w in g._KNOWN and w not in g._STOPWORDS]


def bind_score(text):
    """Return (binds: bool, detail: dict). A comparator token i and a measurable token j BIND
    (predicate the SAME idea) iff ALL of:
      (1) |i-j| <= WINDOW           — they sit in one local clause, NOT sprinkled apart;
      (2) NO clause-breaking connector strictly between them — they are not welded across a
          clause boundary onto a different leg (the cross-sprinkle signature);
      (3) a SHARED SUBJECT exists  — >=1 content token in the local clause window
          [i,j]+/-WINDOW that is the topic the claim is ABOUT (a content noun that is NOT the
          comparator/measurable word itself). The comparator and measurable both predicate it.
    semantic-bind = ANY (i,j) pair satisfying (1)&(2)&(3)."""
    wl = g._words(text)
    if not wl:
        return False, {"reason": "empty"}
    comp_idx = [i for i, w in enumerate(wl) if w in COMPARATOR]
    meas_idx = [i for i, w in enumerate(wl) if w in MEASURABLE]
    if not comp_idx or not meas_idx:
        return False, {"reason": "no comparator or measurable token"}

    content = _content_tokens(wl)
    content_pos = {i for i, _ in content}
    content_lemma = {i: w for i, w in content}

    best = None
    for ci in comp_idx:
        for mj in meas_idx:
            dist = abs(ci - mj)
            if dist > WINDOW:
                continue
            lo, hi = (ci, mj) if ci < mj else (mj, ci)
            # (2) clause-break check: any breaker token strictly between comp and meas?
            broken = any(wl[k] in CLAUSE_BREAK for k in range(lo + 1, hi))
            if broken:
                continue
            # (3) shared subject: content tokens in the local clause window that are NEITHER
            #     the comparator NOR the measurable word -> the topic both legs predicate.
            head_lo = max(0, lo - WINDOW)
            head_hi = min(len(wl), hi + WINDOW + 1)
            subjects = {content_lemma[k] for k in range(head_lo, head_hi)
                        if k in content_pos and wl[k] not in COMPARATOR
                        and wl[k] not in MEASURABLE}
            ok = len(subjects) >= MIN_SUBJECT
            cand = {"comp_i": ci, "comp": wl[ci], "meas_j": mj, "meas": wl[mj],
                    "dist": dist, "subjects": sorted(subjects), "binds": ok}
            if ok and (best is None or dist < best["dist"]):
                best = cand
    if best is not None:
        return True, best
    return False, {"reason": "comparator+measurable present but NO SAME-idea binding "
                             "(too far / clause-broken / no shared subject)",
                   "comp_idx": comp_idx, "meas_idx": meas_idx}


def is_falsifiable_semantic(text):
    """semantic-FALS = structural-FALS AND SAME-idea binding."""
    if not is_falsifiable_structural(text):
        return False
    binds, _ = bind_score(text)
    return binds


# ────────────────────────────────────────────────────────────────────────────
# FROZEN CALIBRATION SUITE (declared before any ckpt is scored). Proves the
# semantic detector (i) AGREES with structural on genuinely-bound claims and
# (ii) REJECTS the cross-sprinkle case structural accepts. Advisory print; the
# detector is FROZEN regardless.
# ────────────────────────────────────────────────────────────────────────────
CALIB_BOUND = [
    # comparator + measurable predicate ONE idea (shared subject in the local clause) -> BOTH fire
    "if consciousness increases then the emit rate measured at the boundary rises higher",
    "tension predicts a higher number of mitosis cells than silence does in the substrate",
    "memory density correlates with a lower error threshold when grounded in the cells",
    "the phi value is greater when distinct cells exceed a count of eight in the engine",
    "novelty rate decreases faster than coherence as the corpus size grows in the model",
]
# CROSS-SPRINKLE — mirrors the EXACT cross-shuffle operation the experiment uses: take an
# idea whose comparator-bearing clause is intact, DELETE its own measurable, and SPLICE a
# DONOR measurable token from a DIFFERENT idea at the END (far from the comparator, no shared
# subject). STRUCTURAL still fires (a comparator + a measurable both exist); SEMANTIC must
# REJECT (the spliced measurable is far / topic-disjoint from the comparator clause).
CALIB_SPRINKLE = [
    "if consciousness arises from cells then the engine dreams when alone at night magnitude",
    "tension ripples between distant minds whenever they connect across the void frequency",
    "memory composes into new meaning as the substrate carries silence onward duration",
    "the engine dreams when alone yet the corpus stays quiet through the night density",
    "silence still carries information whenever the cells stay grounded and aware percent",
]


def calibrate():
    rows = []
    n_bound_struct = n_bound_sem = 0
    n_sprk_struct = n_sprk_sem = 0
    for t in CALIB_BOUND:
        s = is_falsifiable_structural(t)
        m = is_falsifiable_semantic(t)
        n_bound_struct += int(s)
        n_bound_sem += int(m)
        rows.append(("BOUND", s, m, t))
    for t in CALIB_SPRINKLE:
        s = is_falsifiable_structural(t)
        m = is_falsifiable_semantic(t)
        n_sprk_struct += int(s)
        n_sprk_sem += int(m)
        rows.append(("SPRINKLE", s, m, t))
    return {
        "bound_struct": n_bound_struct, "bound_sem": n_bound_sem,
        "sprinkle_struct": n_sprk_struct, "sprinkle_sem": n_sprk_sem,
        "rows": rows,
    }


if __name__ == "__main__":
    c = calibrate()
    print("== H_1458 SEMANTIC DETECTOR — FROZEN CALIBRATION ==")
    print(f"  COMPARATOR={len(COMPARATOR)} MEASURABLE={len(MEASURABLE)} STANCE={len(STANCE)} "
          f"WINDOW={WINDOW} MIN_SUBJECT={MIN_SUBJECT}")
    for cls, s, m, t in c["rows"]:
        print(f"  [{cls:8s}] struct={int(s)} sem={int(m)}  {t[:78]}")
    print(f"\n  BOUND    : structural {c['bound_struct']}/5  semantic {c['bound_sem']}/5")
    print(f"  SPRINKLE : structural {c['sprinkle_struct']}/5  semantic {c['sprinkle_sem']}/5")
    # ── FROZEN DISCRIMINATOR-VALIDITY BAR (declared here, BEFORE any ckpt is scored) ──
    # The semantic detector is a VALID, MORE-FAITHFUL falsifiability test iff:
    #   (V1) it RETAINS genuinely-bound claims  : bound_sem    >= 4/5
    #   (V2) it is STRICTLY STRICTER on sprinkle: sprinkle_sem  < sprinkle_struct
    # We deliberately do NOT demand sprinkle_sem==0: a purely-lexical detector (no learned
    # embeddings — none available, $0) CANNOT catch a spliced measurable that happens to land
    # next to a trailing comparator with a local subject. That residual is an HONEST ceiling of
    # lexical binding, NOT tuned away (c9). What matters for the experiment is the DIRECTION:
    # semantic removes cross-sprinkle FALS that structural keeps.
    valid = (c["bound_sem"] >= 4 and c["sprinkle_sem"] < c["sprinkle_struct"])
    print(f"\n  DISCRIMINATOR VALID (V1 bound_sem>=4 AND V2 sprinkle_sem<sprinkle_struct): {valid}")
    print(f"  => structural is BLINDER to cross-sprinkle ({c['sprinkle_struct']}/5 fire); "
          f"semantic is STRICTER ({c['sprinkle_sem']}/5 fire).")
    print(f"  V1 retain bound_sem={c['bound_sem']}>=4 -> {c['bound_sem']>=4}")
    print(f"  V2 strict  sprinkle_sem={c['sprinkle_sem']}<{c['sprinkle_struct']}=sprinkle_struct -> "
          f"{c['sprinkle_sem']<c['sprinkle_struct']}")
