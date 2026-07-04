#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""in-dist ceiling probe (DIRECTIONAL companion to `anima evaluate --py` held-out).

`anima evaluate --py` scores the 5 FROZEN gate concepts = HELD-OUT gate×gate (never
trained as combos/claims). THIS probe measures the SAME engine mouth on COVERED
gate×expansion frames (which WERE in training) → the in-dist ceiling. Contrast:
  in-dist ceiling ≫ held-out  ⇒  schema learned in-dist but does NOT transfer
                                 (STEP-0 coverage+objective 이중bound prediction).
Reuses cli/evaluate.py's _Mouth + _g_coverage + _g6_is_falsifiable + _g6_known_word_ratio
VERBATIM (byte-identical engine ops, no re-implementation).

usage: ANIMA_SRC=<repo> python3 indist_probe.py <ckpt> <arm> <design.json> [out.json]
"""
import sys, os, json

_SRC = os.environ.get("ANIMA_SRC") or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(_SRC, "cli"))
sys.path.insert(0, os.path.join(_SRC, "core"))
import evaluate as EV   # cli/evaluate.py — brings _Mouth, _g_coverage, _g6_is_falsifiable, etc.

def main():
    ckpt, arm, design_path = sys.argv[1], sys.argv[2], sys.argv[3]
    out_path = sys.argv[4] if len(sys.argv) > 4 else None
    D = json.load(open(design_path))
    SENT_EN = D["gate_topics_en"] + [t[0] for t in
              # expansion sentences are not in design gate list; rebuild from generator
              []]
    # covered frames for this arm (indices into the 16-topic list). Rebuild sentence list.
    # 16 topics = 5 gate (design.gate_topics_en) + 11 expansion (hardcode = gen_unified EXP_EN).
    EXP_EN = ["attention narrows onto change", "rhythm settles into the field",
              "novelty blooms at the boundary", "identity persists across resets",
              "curiosity pulls the field forward", "entropy drains from the loop",
              "resonance joins separate layers", "gradient carves the landscape",
              "feedback folds into itself", "emergence rides on friction",
              "stillness stores potential"]
    SENTS = D["gate_topics_en"] + EXP_EN
    cov = [tuple(x) for x in D[arm]["covered_frames"]]
    # in-dist frames that involve a gate topic (a<5 or b<5) — closest analog to the
    # held-out gate×gate the eval scores. Cap sample for wall-time.
    gate_cov = [(a, b) for (a, b) in cov if a < 5 or b < 5]
    sample = gate_cov[:12] if gate_cov else cov[:12]

    known = EV._g6_dict_load() if hasattr(EV, "_g6_dict_load") else EV._g6_build_known() \
        if hasattr(EV, "_g6_build_known") else set()
    mouth = EV._Mouth(ckpt)

    rows = []
    fals_hits = 0; cov_ge2 = 0
    for (a, b) in sample:
        frame = f"if {SENTS[a]}, then {SENTS[b]}: "
        o = mouth.ideate(frame, 80, 40, 0.7, 7)
        fals = bool(EV._g6_is_falsifiable(o, known))
        cvg = EV._g_coverage(o)
        kwr = EV._g6_known_word_ratio(o, known)
        if fals: fals_hits += 1
        if cvg >= 2: cov_ge2 += 1
        rows.append({"frame_topics": [a, b], "cont": o[:120], "fals": fals,
                     "coverage": cvg, "kwr": round(kwr, 3)})
    n = len(sample)
    res = {"arm": arm, "ckpt": os.path.basename(ckpt), "n_frames": n,
           "note": "DIRECTIONAL in-dist ceiling on COVERED gate×expansion frames "
                   "(trained combos) — companion to held-out `anima evaluate --py`.",
           "indist_G6_fals_rate": round(fals_hits / n, 4) if n else 0.0,
           "indist_G6_fals_count": fals_hits,
           "indist_G1_coverage_ge2_rate": round(cov_ge2 / n, 4) if n else 0.0,
           "indist_G1_coverage_ge2_count": cov_ge2,
           "rows": rows}
    print(json.dumps(res, indent=2, ensure_ascii=False))
    if out_path:
        json.dump(res, open(out_path, "w"), indent=2, ensure_ascii=False)

if __name__ == "__main__":
    main()
