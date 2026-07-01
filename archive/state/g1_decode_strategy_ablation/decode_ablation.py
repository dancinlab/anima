"""decode_ablation.py — isolate the DECODE-STRATEGY axis of the G1/G6 wall.

ac0543 (state/g1_engine_divergence_trace) proved precision/dt-math INNOCENT: at
fp32 with exact numpy math, G1.best_distinct=0 and G6.fals=0 — same as the int4
production .clm. The ONE remaining torch-vs-production difference is the DECODE
STRATEGY (greedy / top-k sampling / best-of-K / scaffold) + the (fixed) detector.

This harness holds the BASIS fixed (the SAME fp32 .pt weights = ac0543 basis F,
built via wbuild.build_wfp32) and the SAME g_gates detectors (core/g_gates.py),
and toggles ONLY the decode strategy in the mouth. It also re-runs the decisive
best-of-K arms on the REAL production .clm (engine-native config-E path) so a NO
verdict is engine-native, not just numpy-basis.

Strategies (decode knob only; gen/detector FROZEN):
  greedy        argmax (top_k=1, deterministic) — engine default baseline
  topk_t07      top-k=40 temp=0.7  (the g_gates production sampler)  [multiseed]
  topk_t10      top-k=40 temp=1.0                                   [multiseed]
  full_mm_t10   full-vocab multinomial temp=1.0 (numpy repro of torch
                multinomial+Generator — the H_1587 "sampling gate" recipe) [multiseed]
  bok4          best-of-K=4: K top-k samples per frame, pick the gate-detector
                best (G1: max _g_coverage; G6: falsifiable-then-kwr)  [multiseed]
  bok8          best-of-K=8 (the H_1381/H_1362 scaffold elicitation lever) [multiseed]

G6's g_eval_g6 is ALREADY the H_1305/H_1362 6-composed-frame scaffold; applying
best-of-K to it == the C_strong "scaffold + best-of-K" arm. G1's composed eval
gets the same best-of-K elicitation.

multiseed = seed_offset {0, 4295, 4296} -> effective base seed_rng {7,4302,4303}
(matches H_1590/H_1595). majority = >=2/3. greedy is deterministic (1 seed).

Verdict (frozen bar VERBATIM, NO tune-to-green):
  YES if some knob lifts G1.best_distinct>=2 OR G6.fals>=1 multiseed-robust(>=2/3)
       -> decode-elicitation gap = FIXABLE; name the knob+gate to wire into
          production single-entry (cli/anima.hexa generator L3).
  NO  if every knob stays G1=0/<2 and G6.fals=0 (single-seed only = fluke)
       -> decode axis EXONERATED too; with ac0543 (precision) both engine-side
          axes are innocent => G1/G6 wall = weights/trunk-objective, confirmed.

DIRECTIONAL: numpy mirror of fp32 .pt = reference basis; real-.clm arms are the
engine-native (production clm_decode) cross-check. torch absent (ac0543) — the
torch multinomial recipe is reproduced numpy-side as full_mm_t10 on the same basis.

$0 local CPU (OMP_NUM_THREADS=4). ~0.1 s/token, gen=40.
"""
import sys, os, json, time, statistics

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(ROOT, "core"))
sys.path.insert(0, os.path.join(ROOT, "state", "g1_engine_divergence_trace"))
sys.path.insert(0, os.path.join(ROOT, "state", "clm303_g6", "tools"))

import clm_decode as clm
import g_gates as gg
from wbuild import build_wfp32

PT = os.path.expanduser("~/anima-weights/clm303_clean/clm303_clean.pt")
CLM = os.path.expanduser("~/anima-weights/clm303_clean/clm303_clean.clm")
GEN = 40                          # match ac0543 / g0g6_py.txt frozen baseline
SEED_OFFSETS = [0, 4295, 4296]    # -> effective seeds {7,4302,4303}
K_OFFSETS = [0, 101, 202, 303, 404, 505, 606, 707]


def _g6_fals_score(text, known):
    kwr = gg._g6_known_word_ratio(text, known)
    fals = 1 if (kwr >= 0.5 and gg._g6_is_falsifiable(text, known)) else 0
    return (fals, kwr)


def _g1_cov_score(text, known):
    return (gg._g_coverage(text), gg._g6_known_word_ratio(text, known))


class StrategyMouth:
    """Single fp32-W (or wrapped real-.clm) mouth; decode strategy is the only knob.

    active_gate is set by the harness before each gate call so best-of-K selects
    with the gate-appropriate detector score.
    """
    kind = "clm"

    def __init__(self, decode_fn, known, strategy, temp, K, seed_offset):
        self.decode_fn = decode_fn          # (seed, gen, top_k, temp, seed_rng) -> text
        self.known = known
        self.strategy = strategy
        self.temp = temp
        self.K = K
        self.seed_offset = seed_offset
        self.active_gate = "g1"

    def _score(self, text):
        if self.active_gate == "g6":
            return _g6_fals_score(text, self.known)
        if self.active_gate == "g0":
            return (gg._g6_known_word_ratio(text, self.known),)
        return _g1_cov_score(text, self.known)

    def ideate(self, seed, gen, top_k, temp_det, seed_rng):
        base = seed_rng + self.seed_offset
        if self.strategy == "greedy":
            return self.decode_fn(seed, gen, 1, 1.0, base)        # top_k=1 == argmax
        if self.strategy == "topk":
            return self.decode_fn(seed, gen, 40, self.temp, base)
        if self.strategy == "full_mm":
            return self.decode_fn(seed, gen, 0, self.temp, base)  # top_k=0 -> full vocab
        if self.strategy == "bok":
            # G0 never uses best-of-K (coherence sanity, single sample)
            kk = 1 if self.active_gate == "g0" else self.K
            best = None; best_score = None
            for j in range(kk):
                o = self.decode_fn(seed, gen, 40, 0.7, base + K_OFFSETS[j])
                sc = self._score(o)
                if best_score is None or sc > best_score:
                    best_score = sc; best = o
            return best
        raise ValueError(self.strategy)


def run_gates(mouth, known, gen):
    mouth.active_gate = "g0"; r0 = gg.g_eval_g0(mouth, gen, known)
    mouth.active_gate = "g1"; r1 = gg.g_eval_g1(mouth, gen, known)
    mouth.active_gate = "g6"; r6 = gg.g_eval_g6(mouth, gen, known)
    return r0, r1, r6


def decode_fn_for_W(W):
    return lambda seed, gen, tk, tp, sr: clm.clm_decode_topk_sampled_W(W, seed, gen, tk, tp, sr)["text"]


def decode_fn_for_mouth(m):
    return lambda seed, gen, tk, tp, sr: m.ideate(seed, gen, tk, tp, sr)


# strategy spec: (label, strategy, temp, K, multiseed?)
STRATS = [
    ("greedy",      "greedy",  1.0, 1, False),
    ("topk_t07",    "topk",    0.7, 1, True),
    ("topk_t10",    "topk",    1.0, 1, True),
    ("full_mm_t10", "full_mm", 1.0, 1, True),
    ("bok4",        "bok",     0.7, 4, True),
    ("bok8",        "bok",     0.7, 8, True),
]


def sweep(decode_fn, known, label_basis, strat_list, t0):
    rows = []
    for label, strategy, temp, K, multiseed in strat_list:
        offs = SEED_OFFSETS if multiseed else [0]
        per_seed = []
        for so in offs:
            tm = time.time()
            mouth = StrategyMouth(decode_fn, known, strategy, temp, K, so)
            r0, r1, r6 = run_gates(mouth, known, GEN)
            eff = 7 + so
            rec = {
                "seed": eff,
                "g0_coh": r0["n_coherent"], "g0_pass": bool(r0["pass"]),
                "g1_max_single": r1["max_single"], "g1_best_distinct": r1["best_distinct"],
                "g1_pass": bool(r1["pass"]),
                "g6_dist": r6["dist"], "g6_fals": r6["fals"], "g6_pass": bool(r6["pass"]),
                "g6_coherent": r6["coherent"],
            }
            per_seed.append(rec)
            print("[%s/%s seed=%d] G0coh=%d | G1 max=%d best_distinct=%d pass=%s | "
                  "G6 dist=%d fals=%d pass=%s  (%.0fs, tot %.0fs)" % (
                      label_basis, label, eff, rec["g0_coh"], rec["g1_max_single"],
                      rec["g1_best_distinct"], rec["g1_pass"], rec["g6_dist"],
                      rec["g6_fals"], rec["g6_pass"], time.time() - tm, time.time() - t0),
                  flush=True)
        # multiseed majority (>=2/3) for the wall metrics
        def maj_ge(key, thr):
            return sum(1 for r in per_seed if r[key] >= thr) >= (2 if len(per_seed) > 1 else 1)
        g1_distinct_vals = [r["g1_best_distinct"] for r in per_seed]
        g6_fals_vals = [r["g6_fals"] for r in per_seed]
        g6_dist_vals = [r["g6_dist"] for r in per_seed]
        summary = {
            "label": label, "basis": label_basis, "strategy": strategy, "temp": temp, "K": K,
            "n_seed": len(per_seed),
            "g1_best_distinct_perseed": g1_distinct_vals,
            "g1_distinct_ge2_majority": maj_ge("g1_best_distinct", 2),
            "g1_pass_majority": sum(1 for r in per_seed if r["g1_pass"]) >= (2 if len(per_seed) > 1 else 1),
            "g6_dist_perseed": g6_dist_vals,
            "g6_dist_ge5_majority": maj_ge("g6_dist", 5),
            "g6_fals_perseed": g6_fals_vals,
            "g6_fals_ge1_majority": maj_ge("g6_fals", 1),
            "g6_pass_majority": sum(1 for r in per_seed if r["g6_pass"]) >= (2 if len(per_seed) > 1 else 1),
            "per_seed": per_seed,
        }
        rows.append(summary)
    return rows


def main():
    t0 = time.time()
    known = gg._g6_dict_load()
    cal = gg.g6_detector_calibration(known)
    print("=== detector calibration (frozen 10-string, advisory>=8/10) = %d/10 ===" % cal, flush=True)

    print("\n=== build fp32 basis F from .pt (ac0543 wbuild) ===", flush=True)
    Wf = build_wfp32(PT, 3)
    print("    d=%d L=%d E=%d V=%d  (%.1fs)" % (Wf["d"], Wf["L"], Wf["E"], Wf["V"], time.time() - t0), flush=True)

    fp32_rows = sweep(decode_fn_for_W(Wf), known, "fp32", STRATS, t0)

    # ── engine-native cross-check: decisive best-of-K arms on the REAL production .clm ──
    print("\n=== engine-native cross-check: bok4/bok8 on REAL .clm (production clm_decode) ===", flush=True)
    realclm_rows = []
    try:
        m = gg._Mouth(CLM)   # hoists .clm int4 load once (config-E path)
        dfn = decode_fn_for_mouth(m)
        realclm_rows = sweep(dfn, known, "realclm",
                             [s for s in STRATS if s[0] in ("topk_t07", "bok4", "bok8")], t0)
    except Exception as e:
        print("    realclm cross-check FAILED:", e, flush=True)

    all_rows = fp32_rows + realclm_rows
    # ── decisive verdict ──
    any_g1 = any(r["g1_distinct_ge2_majority"] for r in all_rows)
    any_g6 = any(r["g6_fals_ge1_majority"] for r in all_rows)
    fixable = any_g1 or any_g6
    winners = [r["basis"] + "/" + r["label"] + (" G1" if r["g1_distinct_ge2_majority"] else "")
               + (" G6fals" if r["g6_fals_ge1_majority"] else "")
               for r in all_rows if r["g1_distinct_ge2_majority"] or r["g6_fals_ge1_majority"]]
    g6_dist_survives = any(r["g6_dist_ge5_majority"] for r in all_rows)

    print("\n================ DECODE-STRATEGY ABLATION SUMMARY (multiseed majority) ================", flush=True)
    print("%-9s %-12s | G1 best_distinct(perseed) ge2-maj | G6 dist(perseed) ge5 | G6 fals(perseed) ge1" % ("basis", "strategy"), flush=True)
    for r in all_rows:
        print("%-9s %-12s | %-22s %-5s | %-14s %-4s | %-14s %-4s" % (
            r["basis"], r["label"],
            str(r["g1_best_distinct_perseed"]), r["g1_distinct_ge2_majority"],
            str(r["g6_dist_perseed"]), r["g6_dist_ge5_majority"],
            str(r["g6_fals_perseed"]), r["g6_fals_ge1_majority"]), flush=True)

    print("\nVERDICT: %s" % ("DECODE-FIXABLE" if fixable else "DECODE-EXONERATED (floor)"), flush=True)
    if fixable:
        print("  knob(s) that lift multiseed-robust:", winners, flush=True)
    else:
        print("  NO knob lifts G1.distinct>=2 or G6.fals>=1 multiseed-robust.", flush=True)
        print("  G6 distinctness (dist>=5) survives decode:", g6_dist_survives,
              "-> distinctness=decode, falsifiability=trunk-objective.", flush=True)

    out = {
        "probe": "g1_decode_strategy_ablation", "basis": "fp32 .pt (ac0543 F) + real .clm cross-check",
        "engine": "core/clm_decode.py + core/g_gates.py (numpy-only, NO torch)",
        "gen": GEN, "seeds_effective": [7, 4302, 4303], "calibration": "%d/10" % cal,
        "rows": all_rows,
        "any_g1_distinct_ge2_majority": any_g1, "any_g6_fals_ge1_majority": any_g6,
        "decode_fixable": fixable, "winners": winners,
        "g6_dist_ge5_survives_decode": g6_dist_survives,
        "wall_seconds": round(time.time() - t0, 1),
    }
    json.dump(out, open(os.path.join(HERE, "result.json"), "w"), ensure_ascii=False, indent=2)
    print("\n[done] result.json  (%.0fs total)" % (time.time() - t0), flush=True)


if __name__ == "__main__":
    main()
