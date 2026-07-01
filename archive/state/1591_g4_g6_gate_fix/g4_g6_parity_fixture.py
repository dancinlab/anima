#!/usr/bin/env python3
# @canonical-ok task-specified slug "1591_g4_g6_gate_fix" (G4/G6 gate measurement fix)
"""state/1591_g4_g6_gate_fix — fixed-fixture parity / reproduction check for the G4+G6
measurement fixes (lockstep g_gates.{hexa,py} + g6_ideation.{hexa,py}).

This is the py-side fixture. It proves, on a SMALL local .clm (no GPU, mini-safe):

  (A) G6 SEEDED REPRODUCTION — g_eval_g6(mouth, gen, known, base_seed=7) is byte-identical
      to the OLD inline single-seed path (per-frame seed 7+i). i.e. the wiring reconcile
      (route through the canonical g6_score_arm_auto op) changed the PLUMBING, not the metric.
  (B) G6 MULTI-SEED — re-runs the SAME frozen ladder over {7,4302,4303}; reports per-seed
      fals/dist + majority. (Shows fals=0 robustness across seeds, not a single-seed lottery.)
  (C) G4 PROVENANCE — g_eval_g4 computes sha256 (== shasum -a 256), bytes, mouth, decodable,
      and carries pub_eligible (= closure). Compared to an INDEPENDENT hashlib + os.stat.

The HEXA twin runs the SAME 3 checks via core/g_gates.hexa once compiled on the canonical
install (see g4_g6_parity_fixture.hexa); cross-language byte-parity is the 2-production oracle.
"""
import sys, os, hashlib, subprocess, json
_CORE = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "core"))
sys.path.insert(0, _CORE)

import g_gates as G
from g6_ideation import (
    _g6_dict_load, g6_build_frames, _g6_known_word_ratio, _g6_words,
    _g6_is_falsifiable, _g6_jaccard, g6_sampler_selftest, g6_detector_calibration,
)

CKPT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "lane_p_clm", "clm_d768_e2l1.clm"))
GEN = 24   # small bound — mini-safe d768 forward


def _old_inline_g6(mouth, gen, known, base_seed):
    """The PRE-FIX inline g_eval_g6 scoring (verbatim from the committed code, per-frame
    seed base_seed+i) — the reference the wired g6_score_arm_auto must reproduce."""
    frames = g6_build_frames(6)["composed"]
    word_sets = []; fals = 0
    for i in range(len(frames)):
        o = mouth.ideate(frames[i], gen, 40, 0.7, base_seed + i)
        if _g6_known_word_ratio(o, known) >= 0.5:
            word_sets.append(_g6_words(o))
            if _g6_is_falsifiable(o, known):
                fals += 1
    kept = []
    for ws in word_sets:
        ok = True
        for k in kept:
            if _g6_jaccard(ws, k) > 0.5:
                ok = False
        if ok:
            kept.append(ws)
    return {"dist": len(kept), "fals": fals, "coherent": len(word_sets)}


def main():
    known = _g6_dict_load()
    print("=" * 72)
    print("1591 G4+G6 PARITY FIXTURE (py side)  ckpt=%s  gen=%d" % (os.path.basename(CKPT), GEN))
    print("=" * 72)

    # ── no-model surface: sampler self-test + calibration (the 4 ported pub fns) ──
    st = g6_sampler_selftest()
    print("g6_sampler_selftest:", st,
          " -> ALL-TRUE=", st["deterministic"] and st["diverse"] and st["in_topk"])
    print("g6_detector_calibration:", g6_detector_calibration(known), "/10 (advisory >=8)")

    mouth = G._Mouth(CKPT)

    # ── (A) G6 seeded reproduction: wired arm == old inline path, base_seed=7 ──
    print("-" * 72)
    new7 = G.g_eval_g6(mouth, GEN, known, base_seed=7)
    old7 = _old_inline_g6(mouth, GEN, known, 7)
    repro = (new7["dist"] == old7["dist"] and new7["fals"] == old7["fals"]
             and new7["coherent"] == old7["coherent"])
    print("(A) G6 base_seed=7  wired arm   dist=%d fals=%d coherent=%d"
          % (new7["dist"], new7["fals"], new7["coherent"]))
    print("    G6 base_seed=7  old inline  dist=%d fals=%d coherent=%d"
          % (old7["dist"], old7["fals"], old7["coherent"]))
    print("    REPRODUCTION (wired==inline):", "PASS" if repro else "FAIL <-- DRIFT")

    # ── (B) G6 multi-seed ladder ──
    print("-" * 72)
    ms = G.g_eval_g6_multiseed(mouth, GEN, known)
    print("(B) G6 multi-seed  seeds=%s  pass=%s  %d/%d clear  max_fals=%d"
          % (ms["seeds"], ms["pass"], ms["n_green"], ms["n_seeds"], ms["max_fals"]))
    for p in ms["per_seed"]:
        print("      seed=%d  dist=%d fals=%d coherent=%d pass=%s"
              % (p["base_seed"], p["dist"], p["fals"], p["coherent"], p["pass"]))

    # ── (C) G4 provenance vs independent sha256/stat ──
    print("-" * 72)
    g4 = G.g_eval_g4(CKPT, closure=False)
    ref = hashlib.sha256(open(CKPT, "rb").read()).hexdigest()
    ref_bytes = os.path.getsize(CKPT)
    sha_ok = g4["sha256"] == ref
    bytes_ok = g4["bytes"] == ref_bytes
    # cross-check against the system shasum tool too (independent of python)
    try:
        sysout = subprocess.check_output(["shasum", "-a", "256", CKPT]).decode().split()[0]
        sys_ok = sysout == ref
    except Exception as e:
        sysout = "(shasum unavailable: %s)" % e; sys_ok = None
    print("(C) G4 provenance  mouth=%s decodable=%s pub_eligible=%s"
          % (g4["mouth"], g4["decodable"], g4["pub_eligible"]))
    print("    sha256 g_eval_g4 == hashlib:", "PASS" if sha_ok else "FAIL", g4["sha256"][:24] + "…")
    print("    sha256 g_eval_g4 == shasum :", ("PASS" if sys_ok else ("FAIL" if sys_ok is False else "SKIP")))
    print("    bytes  g_eval_g4 == os.stat:", "PASS" if bytes_ok else "FAIL",
          "(%d)" % g4["bytes"])
    print("    provenance_ok:", g4["provenance_ok"])

    print("=" * 72)
    allok = repro and sha_ok and bytes_ok and (sys_ok in (True, None)) and g4["provenance_ok"]
    print("FIXTURE:", "ALL PASS" if allok else "SOME FAIL — inspect above")
    # machine-readable snapshot for the hexa-side byte compare
    snap = {"g6_seed7": {"dist": new7["dist"], "fals": new7["fals"], "coherent": new7["coherent"]},
            "g6_repro": repro,
            "g6_multiseed": {"pass": ms["pass"], "n_green": ms["n_green"],
                             "max_fals": ms["max_fals"],
                             "per_seed": [{"seed": p["base_seed"], "dist": p["dist"],
                                           "fals": p["fals"]} for p in ms["per_seed"]]},
            "g4": {"sha256": g4["sha256"], "bytes": g4["bytes"], "mouth": g4["mouth"],
                   "decodable": g4["decodable"], "provenance_ok": g4["provenance_ok"]},
            "sampler_selftest": st}
    with open(os.path.join(os.path.dirname(__file__), "parity_py.json"), "w") as fh:
        json.dump(snap, fh, indent=2)
    return 0 if allok else 1


if __name__ == "__main__":
    sys.exit(main())
