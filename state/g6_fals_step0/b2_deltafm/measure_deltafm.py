#!/usr/bin/env python3
"""B-2 δ_FM corpus density probe for H_9128 (G6-FALS wall).

DIRECTIONAL (a_engine_native_learning): numpy/textscan mirror, NOT 303M engine.
Reference-matches the FROZEN detector in core/g6_ideation.py (comparator/measurable/
stance/stopword sets + _g6_words BYTE tokenizer + _g6_is_falsifiable) verbatim by
importing them, so the co-occurrence math is byte-identical to the live G6 detector.

Measures per corpus:
  δ_FM      = fraction of non-overlapping 40-byte windows that contain
              >=1 comparator word AND >=1 measurable word (the FALS a&b gate).
  P(FALS)   = fraction of 40-byte windows passing the FULL _g6_is_falsifiable
              (a & b & content>=2 & not-question & not-stance) -- the real echo prob.
  P(comp)   = fraction of windows with >=1 comparator word.
  P(meas)   = fraction of windows with >=1 measurable word.
  PMI(c,m)  = log2( P(c&m) / (P(c)*P(m)) )  -- co-occurrence lift over independence.
  fit40     = among FALS-passing *sentences* (split on ./!/?/newline), fraction
              whose UTF-8 byte-length <= 40 (does falsifiable content fit the window?).
"""
import sys, math, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", ".."))
# import frozen detector (module top-level guard only exits under __main__)
import importlib.util
spec = importlib.util.spec_from_file_location(
    "g6det", os.path.join(os.path.dirname(__file__), "..", "..", "..", "core", "g6_ideation.py"))
g6 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(g6)

COMP = g6._g6_comparator()
MEAS = g6._g6_measurable()
KNOWN = g6._g6_dict_load()
print(f"[dict] known words loaded: {len(KNOWN)}", file=sys.stderr)

WIN = 40  # 40-byte continuation window (the G6 detector's continuation slice)


def window_flags(byteslice):
    ws = g6._g6_words(byteslice)  # BYTE tokenizer, ASCII-only
    has_c = any(w in COMP for w in ws)
    has_m = any(w in MEAS for w in ws)
    return has_c, has_m


def measure_file(path, cap_bytes=None):
    with open(path, "rb") as f:
        data = f.read() if cap_bytes is None else f.read(cap_bytes)
    n = len(data)
    nw = n // WIN
    both = c_only = m_only = c_any = m_any = fals = 0
    for i in range(nw):
        seg = data[i*WIN:(i+1)*WIN]
        hc, hm = window_flags(seg)
        if hc: c_any += 1
        if hm: m_any += 1
        if hc and hm: both += 1
        if g6._g6_is_falsifiable(seg, KNOWN):
            fals += 1
    # sentence-level fit40
    import re
    sents = re.split(rb'[.!?\n]+', data)
    fals_sent = 0
    fals_sent_fit = 0
    for s in sents:
        s2 = s.strip()
        if len(s2) == 0:
            continue
        if g6._g6_is_falsifiable(s2, KNOWN):
            fals_sent += 1
            if len(s2) <= WIN:
                fals_sent_fit += 1
    pc = c_any / nw if nw else 0.0
    pm = m_any / nw if nw else 0.0
    pcm = both / nw if nw else 0.0
    if pc > 0 and pm > 0 and pcm > 0:
        pmi = math.log2(pcm / (pc * pm))
    else:
        pmi = float('-inf')
    return {
        "path": path, "bytes": n, "windows": nw,
        "delta_FM": pcm, "P_FALS_win": fals / nw if nw else 0.0,
        "P_comp": pc, "P_meas": pm, "PMI_cm": pmi,
        "both_ct": both, "fals_win_ct": fals,
        "fals_sentences": fals_sent, "fals_sent_fit40": fals_sent_fit,
        "fit40": (fals_sent_fit / fals_sent) if fals_sent else None,
    }


def main():
    targets = []
    for arg in sys.argv[1:]:
        if "=" in arg:
            label, path = arg.split("=", 1)
        else:
            label, path = os.path.basename(arg), arg
        targets.append((label, path))
    results = {}
    for label, path in targets:
        if not os.path.exists(path):
            print(f"[MISS] {label}: {path}", file=sys.stderr)
            results[label] = {"error": "missing", "path": path}
            continue
        print(f"[scan] {label} ...", file=sys.stderr)
        results[label] = measure_file(path)
    import json
    print(json.dumps(results, indent=2, default=str))


if __name__ == "__main__":
    main()
