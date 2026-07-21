#!/usr/bin/env python3
"""H_003 span-policy encoder — position-keyed one-variable lever, verified $0.

The experiment rests on ONE claim: A-atom and A-shat produce byte streams that are
IDENTICAL everywhere EXCEPT inside matched negator spans (A-atom emits the negator's
atomic token; A-shat suppresses merges there → base-jamo singletons). If that fails,
the arms differ in more than one variable and the contrast is confounded (adm.3).

An earlier shatter-by-TOKEN-ID version was BROKEN and is preserved in git history
(commit 00ca7b2) + span_policy_verify_v1_BROKEN.out: the negator's atomic token is a
frequency jamo n-gram, not a morpheme (token 438 fires inside 아닐까, 안=286 inside
안녕/안전, 못=381 inside 연못), so shattering by id degraded non-negation words. This
version keys the shatter on SYNTACTIC NEGATION POSITION:

  - BOUND 않 (jamo C:ㅇ V:ㅏ J:ㄶ) — negation-exclusive (아니하 contraction), always.
  - BOUND 지+못하 / 지+아니 — 못하/아니 preceded by 지 (long-form bound frame).
  - FREE standalone — an eojeol that IS exactly 안 or 못 (pre-verb adverb negator).

Everything outside a matched position is byte-identical between arms. The verifier
proves it: lines with no syntactic negation, and the confounders the old policy
broke (안녕/연못/아닐까), must now encode identically.

It consumes v1's jamo-BPE codec (morph2b), owning only the H_003 span policy here.

Run:  python3 state/h003_atomicity_fixed_codec_drill_2026-07-16/span_policy_encode.py
"""

from __future__ import annotations

import importlib.util
import json
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_V1 = "/Users/mini/dancinlab/anima/state/nbind_curriculum/morph2b.py"
_NSMC = os.path.expanduser("~/g1_natem/nsmc_ratings_train.txt")

# jamo signatures as v1's to_jamo emits them (C:/V:/J: markers)
JAMO = {
    "안": ["C:ㅇ", "V:ㅏ", "J:ㄴ"],
    "않": ["C:ㅇ", "V:ㅏ", "J:ㄶ"],   # negation-exclusive
    "못": ["C:ㅁ", "V:ㅗ", "J:ㅅ"],
    "지": ["C:ㅈ", "V:ㅣ"],
    "못하": ["C:ㅁ", "V:ㅗ", "J:ㅅ", "C:ㅎ", "V:ㅏ"],
    "아니": ["C:ㅇ", "V:ㅏ", "C:ㄴ", "V:ㅣ"],
}


def load_codec():
    sys.argv = ["morph2b.py", "--corpus", "/dev/null"]
    spec = importlib.util.spec_from_file_location("morph2b", _V1)
    m = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(m)
    except SystemExit:
        pass
    return m


def _match_at(syms, i, sig):
    return syms[i:i + len(sig)] == sig


def negation_spans(eojeols):
    """Per eojeol index, the (start, end) jamo ranges that are a negator in a
    SYNTACTIC negation position. `eojeols` = the non-space eojeols' jamo-symbol
    lists."""
    spans = {}
    for ei, syms in enumerate(eojeols):
        found = []
        n = len(syms)
        i = 0
        while i < n:  # BOUND 않 — always negation
            if _match_at(syms, i, JAMO["않"]):
                found.append((i, i + 3))
                i += 3
                continue
            i += 1
        i = 0
        while i < n:  # BOUND 지+못하 / 지+아니 within one eojeol
            if _match_at(syms, i, JAMO["지"]) and _match_at(syms, i + 2, JAMO["못하"]):
                found.append((i + 2, i + 2 + len(JAMO["못하"])))
                i += 2 + len(JAMO["못하"])
                continue
            if _match_at(syms, i, JAMO["지"]) and _match_at(syms, i + 2, JAMO["아니"]):
                found.append((i + 2, i + 2 + len(JAMO["아니"])))
                i += 2 + len(JAMO["아니"])
                continue
            i += 1
        if syms == JAMO["안"] or syms == JAMO["못"]:  # FREE standalone pre-verb adverb
            found = [(0, len(syms))]
        if found:
            spans[ei] = sorted(set(found))
    return spans


def placebo_spans(eojeols, morpheme_jamo):
    """Per eojeol index, the jamo range(s) of a PLACEBO morpheme (a frequency-matched
    NON-negator, e.g. 진짜) wherever it appears. The C-plc arm (F6) shatters this the
    same way A-shat shatters negation — if shattering ANY frequent morpheme degrades
    the model as much as shattering the negator, the F1 pass is a generic-disruption
    artifact, not atomicity. Matches the morpheme's atomic jamo run inside each eojeol."""
    spans = {}
    for ei, syms in enumerate(eojeols):
        found = []
        i = 0
        n = len(syms)
        L = len(morpheme_jamo)
        while i <= n - L:
            if syms[i:i + L] == morpheme_jamo:
                found.append((i, i + L))
                i += L
                continue
            i += 1
        if found:
            spans[ei] = sorted(set(found))
    return spans


def encode(m, line, merge_rank, tok2id, shatter: bool, placebo_jamo=None):
    """2-byte token stream. shatter=True suppresses merges inside matched spans;
    everything else merges normally (byte-identical to A-atom). Default spans are
    the syntactic NEGATION spans (A-shat); pass placebo_jamo to shatter a
    non-negator morpheme instead (C-plc)."""
    pieces = list(m.eojeol_split(line))
    eojeols = [syms for syms, sp in pieces if not sp]
    if not shatter:
        spans = {}
    elif placebo_jamo is not None:
        spans = placebo_spans(eojeols, placebo_jamo)
    else:
        spans = negation_spans(eojeols)
    out = bytearray()
    ei = 0
    for syms, sp in pieces:
        if sp:
            toks = [" "]
        else:
            toks = (_encode_with_shatter(m, syms, spans[ei], merge_rank)
                    if ei in spans else m.apply_merges(syms, merge_rank))
            ei += 1
        for t in toks:
            i = tok2id.get(t)
            if i is None:
                for bb in t.replace("\x00", "").encode("utf-8", "replace"):
                    out += bytes((0, bb))
            else:
                out += bytes((i >> 8, i & 0xFF))
    return bytes(out)


def _encode_with_shatter(m, syms, ranges, merge_rank):
    """Merge OUTSIDE the negation ranges, emit base-jamo singletons INSIDE them."""
    out = []
    pos = 0
    for (a, b) in ranges:
        if a > pos:
            out.extend(m.apply_merges(syms[pos:a], merge_rank))
        out.extend(syms[a:b])  # singleton jamo — passed through as OOV
        pos = b
    if pos < len(syms):
        out.extend(m.apply_merges(syms[pos:], merge_rank))
    return out


def main() -> int:
    m = load_codec()
    lines = [l.split("\t")[1] for l in open(_NSMC, encoding="utf-8").read().splitlines()[1:20001]
             if len(l.split("\t")) > 2]
    merges = m.train_bpe(lines[:20000], 2048)
    merge_rank, tok2id, vocab = m.build_vocab(lines, merges)

    print("=" * 74)
    print("H_003 span-policy — position-keyed one-variable verification ($0)")
    print("=" * 74)
    print(f"vocab={len(vocab)}")
    print()

    n_ident = n_diff = 0
    for line in lines[:5000]:
        a = encode(m, line, merge_rank, tok2id, shatter=False)
        s = encode(m, line, merge_rank, tok2id, shatter=True)
        if a == s:
            n_ident += 1
        else:
            n_diff += 1

    # The confounders the old token-id policy broke: NON-negation words carrying a
    # negator SYLLABLE (안녕/안전/편안/불안/연못). 아니-family is EXCLUDED — 아니라/아닐까
    # are 아니다 conjugations = real negation, correctly shattered. A confounder line
    # must contain a non-negation syllable AND no negation morpheme at all (그 어떤
    # 않/아니/standalone 안·못/지-못하 도 없어야 순수 대조).
    import re as _re
    # Safe non-negation syllables to seed the confounder set. 연못 is dropped: it
    # carries 못, and the maximally-conservative filter below excludes any line with
    # 못/않/아니/standalone 안 to guarantee ZERO negation (past filters kept letting
    # conjugated negation through — 치않, 아니라, 지못한 — so this excludes the
    # morpheme entirely rather than trying to match every conjugation).
    nonneg = ["안녕", "안전", "편안", "불안", "미안", "안심", "안내", "안경", "안개"]

    def _has_any_negator(t):
        return bool("않" in t or "아니" in t or "못" in t
                    or _re.search(r"(^|\s)안\s", t))

    conf_lines = [l for l in lines[:20000]
                  if any(c in l for c in nonneg) and not _has_any_negator(l)][:300]
    conf_identical = 0
    conf_broken = []
    for l in conf_lines:
        a = encode(m, l, merge_rank, tok2id, shatter=False)
        s = encode(m, l, merge_rank, tok2id, shatter=True)
        if a == s:
            conf_identical += 1
        elif len(conf_broken) < 5:
            conf_broken.append(l)  # full line — truncating hid negation past char 40

    print(f"all lines: identical={n_ident}  differ(=shattered a negation span)={n_diff}")
    print(f"pure non-negation confounder lines (안녕/안전/편안/…, no 못/않/아니/안, n={len(conf_lines)}): "
          f"identical={conf_identical}  still-differ={len(conf_lines) - conf_identical}")
    if conf_broken:
        print(f"  STILL BROKEN on: {conf_broken}")
    print()
    ok = (conf_identical == len(conf_lines)) and n_diff > 0
    print("VERDICT:", "one-variable RESTORED — only syntactic negation spans differ"
          if ok else "STILL CONFOUNDED — some non-negation words differ")

    out = {"vocab": len(vocab), "all_identical": n_ident, "all_differ": n_diff,
           "confounder_lines": len(conf_lines), "confounder_identical": conf_identical,
           "confounder_still_differ": len(conf_lines) - conf_identical,
           "one_variable_holds": ok, "still_broken_examples": conf_broken}
    with open(os.path.join(_HERE, "span_policy_verify.json"), "w") as fh:
        json.dump(out, fh, indent=2, ensure_ascii=False)
    print("wrote span_policy_verify.json")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
