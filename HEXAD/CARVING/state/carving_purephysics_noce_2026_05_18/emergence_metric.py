#!/usr/bin/env python3
# ──────────────────────────────────────────────────────────────────────
# emergence_metric.py — honest coherent-emergence metric (RESEARCH.md §9)
#
# PURPOSE
#   Replaces the V-SPONT `coherent` flag (lenient: coherence_token presence
#   + low rep) which gave 5/5 to garbled byte-cascade output (RESEARCH.md
#   §8.2). This metric is deterministic, closed-form-checkable, and gates
#   coherence on byte-cascade-rate FIRST (a hard collapse signature).
#
#   It is a $0 re-scorer: it only operates on the `gen` strings already
#   stored in each fire's eval_result*.json. NO GPU, NO model forward.
#
# METRIC — cascade-rate-gated coherence
#   For a generated string g:
#     C_char(g)  = (max consecutive identical-char run length) / len(g)
#     C_digit(g) = (max consecutive digit run length)          / len(g)
#     C_ngram(g) = repetition-rate = 1 - |distinct char 4-grams| / |4-grams|
#     cascade_rate(g)  = max(C_char, C_digit, C_ngram)        in [0, 1]
#     max_run(g)       = max(max-char-run, max-digit-run)     in Z>=0
#     honest_coherent(g) = (cascade_rate(g) < TAU_CASCADE)  AND
#                          (max_run(g)     < MAX_RUN)       AND
#                          (len(g)        >= MIN_LEN)       AND
#                          (printable_ratio(g) >= TAU_PRINT)
#
#   ALL four conditions are deterministic Boolean / arithmetic — a
#   closed-form verdict is provable (see verify_emergence_metric.py).
#
# WHY TWO cascade conditions (rate AND absolute run)
#   V-SPONT `gen` strings are TRUNCATED at ~40-85 bytes. A model that
#   collapses into `tier=1111...` may have the cascade cut mid-run, so the
#   *visible* run is short and the ratio (run/len) can stay under a pure-
#   rate threshold (RESEARCH.md §8.2 Dir-I diverse probe 1: visible run
#   21, rate 0.296 — would slip under a rate-only 0.30 gate). An absolute
#   max-run gate catches the cascade regardless of where truncation cut
#   it: a 10+ identical-char/digit run is itself a hard collapse signature.
#
# THRESHOLDS — honest justification (NOT arbitrary, NOT target-tuned)
#   TAU_CASCADE = 0.30
#     A 4th of the output being one repeated char/digit/4-gram is a
#     collapse signature. 0.30 = smallest round fraction strictly above
#     "1/4 collapse".
#   MAX_RUN = 10
#     The 13-way arc max-run distribution is strictly BIMODAL: semi-prose
#     gens cluster at run <= 4, cascade gens at run >= 11 — the (5..10)
#     band is EMPTY across all 70 probes (survey in this dir's stdout).
#     MAX_RUN = 10 sits in that natural empty gap, so the cut is
#     separating-by-data, not tuned to hit any target score.
#   MIN_LEN = 20
#     V-SPONT max_new ~ 40 bytes. A coherence claim on < 20 bytes is not
#     measurable; below this the cascade-rate denominator is too small.
#   TAU_PRINT = 0.80
#     Korean+ASCII text; >20% replacement chars (U+FFFD) means the byte
#     stream is broken mid-codepoint (encoding-cascade). 0.80 is the
#     loosest bound that still rejects the heavily-garbled gens.
#
# HONESTY (g3) — what this metric does NOT prove
#   The honest gate is NECESSARY, NOT SUFFICIENT for coherent emergence.
#   A low-cascade printable string can still be semantically empty, a
#   memorized training continuation, or locally-garbled (`trructing`,
#   `mattrix`). This metric is a *collapse detector* that removes the
#   garbled-byte-cascade false positives of the lenient flag; it is NOT a
#   capability proof. A genuine GOAL ("자발적 correct emergence") claim
#   still needs held-out generalization evidence (not available at $0).
#
# OPTIONAL byte-level coherence proxy (reported, NOT gating):
#   distinct_byte_ratio = |distinct bytes| / 256  — a memorized cascade
#   has a tiny alphabet; coherent prose spreads over more bytes. Reported
#   alongside but NOT part of the honest_coherent gate (weak proxy; no
#   held-out perplexity at $0).
# ──────────────────────────────────────────────────────────────────────
import json, os

TAU_CASCADE = 0.30
MAX_RUN     = 10
MIN_LEN     = 20
TAU_PRINT   = 0.80


def max_char_run(s):
    if not s:
        return 0
    best = run = 1
    for i in range(1, len(s)):
        run = run + 1 if s[i] == s[i - 1] else 1
        best = max(best, run)
    return best


def max_digit_run(s):
    best = run = 0
    for ch in s:
        run = run + 1 if ch.isdigit() else 0
        best = max(best, run)
    return best


def ngram_rep_rate(s, n=4):
    if len(s) < n + 1:
        return 0.0
    grams = [s[i:i + n] for i in range(len(s) - n + 1)]
    return 1.0 - len(set(grams)) / len(grams)


def printable_ratio(s):
    if not s:
        return 0.0
    bad = sum(1 for ch in s if ch == "�")  # U+FFFD replacement char
    return 1.0 - bad / len(s)


def cascade_rate(s):
    if not s:
        return 1.0
    L = len(s)
    return max(max_char_run(s) / L, max_digit_run(s) / L, ngram_rep_rate(s))


def distinct_byte_ratio(s):
    b = s.encode("utf-8", errors="replace")
    return len(set(b)) / 256.0


def honest_coherent(s):
    cr = cascade_rate(s)
    mr = max(max_char_run(s), max_digit_run(s))
    pr = printable_ratio(s)
    ok = (cr < TAU_CASCADE) and (mr < MAX_RUN) and \
         (len(s) >= MIN_LEN) and (pr >= TAU_PRINT)
    return ok, {
        "cascade_rate": round(cr, 4),
        "max_char_run": max_char_run(s),
        "max_digit_run": max_digit_run(s),
        "max_run": mr,
        "ngram_rep_rate": round(ngram_rep_rate(s), 4),
        "printable_ratio": round(pr, 4),
        "len": len(s),
        "distinct_byte_ratio": round(distinct_byte_ratio(s), 4),
        "honest_coherent": ok,
    }


# ── 13-way fire → eval_result json map ──────────────────────────────
FIRES = {
    "UBM-E6 α (alpha)":  "state/consciousness_carving_e6_fire_2026_05_17/out/alpha/eval_result_v2.json",
    "UBM-E6 β (beta)":   "state/consciousness_carving_e6_fire_2026_05_17/out/beta/eval_result_v2.json",
    "UBM-E6 γ (gamma)":  "state/consciousness_carving_e6_fire_2026_05_17/out/gamma/eval_result_v2.json",
    "UBM-E6 weave":      "state/consciousness_carving_e6_fire_2026_05_17/out/weave/eval_result_v2.json",
    "UBM-E7 α":          "state/consciousness_carving_e7_alpha_scaleup_2026_05_17/eval_result_v2_e7.json",
    "Dir-A tension":     "state/carving_dirA_tension_2026_05_17/eval_result_v2_dirA.json",
    "Dir-B intuitor":    "state/carving_dirB_intuitor_2026_05_17/eval_result_v2_dirB.json",
    "Dir-C prime":       "state/carving_dirC_prime_2026_05_17/prime_result.json",
    "Dir-D cde":         "state/carving_dirD_cde_2026_05_17/eval_result_v2_dirD.json",
    "Dir-E superpos":    "state/carving_dirE_superpos_2026_05_17/eval_result_dirE.json",
    "Dir-F abstractcot": "state/carving_dirF_abstractcot_2026_05_17/eval_result_dirF.json",
    "Dir-G psi_ctl":     "state/carving_dirG_psi_ctl_2026_05_17/eval_result_v2_dirG.json",
    "Dir-H tension_sup": "state/carving_dirH_tension_sup_2026_05_17/eval_result_v2_dirH.json",
    "Dir-I psictl":      "state/carving_dirI_psictl_tensionsup_2026_05_17/eval_result_dirI.json",
    "Dir-I diverse (§8)":"state/carving_dirI_diverse_scaleup_2026_05_18/eval_result_diverse.json",
}


def rescore():
    root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    rows, per_probe = [], {}
    for name, rel in FIRES.items():
        path = os.path.join(root, rel)
        if not os.path.exists(path):
            rows.append({"fire": name, "lenient": "N/A", "honest": "N/A",
                         "note": "result json missing"})
            continue
        d = json.load(open(path))
        v = d.get("axis4_v_spont")
        if not v or "probes" not in v:
            rows.append({"fire": name, "lenient": "N/A", "honest": "N/A",
                         "note": "no axis4_v_spont (V-SPONT probe not run for this fire)"})
            continue
        probes = v["probes"]
        lenient = sum(1 for p in probes if p.get("coherent"))
        honest = 0
        probe_rows = []
        for i, p in enumerate(probes):
            g = p.get("gen", "") or ""
            ok, m = honest_coherent(g)
            honest += int(ok)
            probe_rows.append({"idx": i, "lenient_flag": bool(p.get("coherent")),
                               **m, "gen_excerpt": g[:70]})
        per_probe[name] = probe_rows
        rows.append({"fire": name, "lenient": f"{lenient}/{len(probes)}",
                     "honest": f"{honest}/{len(probes)}",
                     "lenient_n": lenient, "honest_n": honest, "total": len(probes)})
    return rows, per_probe


if __name__ == "__main__":
    rows, per_probe = rescore()
    out = {
        "metric": "cascade-rate-gated coherence (RESEARCH.md §9)",
        "thresholds": {"TAU_CASCADE": TAU_CASCADE, "MAX_RUN": MAX_RUN,
                       "MIN_LEN": MIN_LEN, "TAU_PRINT": TAU_PRINT},
        "honest_note": ("honest gate is NECESSARY not SUFFICIENT for coherent "
                        "emergence — collapse detector, not a capability "
                        "proof (g3)."),
        "rescore_table": rows,
        "per_probe": per_probe,
    }
    here = os.path.dirname(os.path.abspath(__file__))
    json.dump(out, open(os.path.join(here, "rescore_result.json"), "w"),
              ensure_ascii=False, indent=2)

    print("=== 13-way V-SPONT re-score: lenient flag vs honest cascade-gated ===")
    print(f"{'fire':<22}{'lenient':>9}{'honest':>9}")
    print("-" * 40)
    tot_l = tot_h = tot_n = 0
    for r in rows:
        print(f"{r['fire']:<22}{r['lenient']:>9}{r['honest']:>9}"
              + ("   " + r['note'] if r.get('note') else ""))
        if "lenient_n" in r:
            tot_l += r['lenient_n']; tot_h += r['honest_n']; tot_n += r['total']
    print("-" * 40)
    print(f"{'TOTAL (scored)':<22}{str(tot_l)+'/'+str(tot_n):>9}{str(tot_h)+'/'+str(tot_n):>9}")
    print(f"\nwrote rescore_result.json  (lenient {tot_l} -> honest {tot_h})")
