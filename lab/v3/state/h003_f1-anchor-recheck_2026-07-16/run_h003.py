"""H_003 — f1-anchor-recheck. Run of the 9 pre-registered falsifiers.

Verdict = rig LICENSED (H_004 pilot may fire) or REFUSED. Deterministic, stdlib
only, $0. Card frozen 2026-07-16 (genspec_sha256 in the frontmatter).

Run: python3 state/h003_f1-anchor-recheck_2026-07-16/run_h003.py
"""

from __future__ import annotations

import json
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.abspath(os.path.join(_HERE, "..", ".."))
sys.path.insert(0, os.path.join(_ROOT, "tool"))
sys.path.insert(0, os.path.join(_ROOT, "src", "generator"))

from anima_v3 import Falsifier, binom_two_sided_p, chance_band, evaluate, two_proportion_n

import spec as S
import stream as ST
import codec as C
import audit as A
from lang import render, parse, to_jamo, from_jamo

# --- frozen inputs (must match the card frontmatter) --------------------------
GENSPEC_SHA = "fbcf0c8ad444d0f3c2fa5ad018d12ce8f33ad6bcf8e0f78eb26be5495527ce2b"
K = 512
BPE_SAMPLE_LINES = 20000
DRIFT_FLOOR = 0.05
N_REQUIRED_WORST = 1178
ANCHOR = {"n": 120, "M": 109, "C1": 74, "C3": 110, "cement_M": 110, "cement_C1": 69}
P0 = 0.50
CONF = 0.99


def main() -> int:
    m = {}
    print("=" * 78)
    print("H_003 — f1-anchor-recheck · verdict = rig LICENSED or REFUSED")
    print("=" * 78)

    spec = S.build_spec()
    got_hash = S.spec_hash(spec)
    m["genspec_sha256"] = got_hash
    m["genspec_matches_card"] = (got_hash == GENSPEC_SHA)
    print(f"\ngenspec_sha256 = {got_hash}")
    print(f"  matches frozen card: {m['genspec_matches_card']}")

    # === Anchor bounds (B-1..B-4) ==========================================
    print("\n[Anchor] exact 99% chance band, n=120, p0=0.50")
    n = ANCHOR["n"]
    lo, hi = chance_band(n, P0, CONF)
    k_lo, k_hi = round(lo * n), round(hi * n)
    m["band_counts"] = [k_lo, k_hi]
    print(f"  band = [{k_lo}/{n}, {k_hi}/{n}] = [{lo:.4f}, {hi:.4f}]")

    m["B1_M_above"] = ANCHOR["M"] >= 75
    m["B2_C3_live"] = ANCHOR["C3"] >= 108
    m["B3_C1_no_leak"] = ANCHOR["C1"] <= 74
    m["B4_cement_agrees"] = (ANCHOR["cement_M"] >= 75 and ANCHOR["cement_C1"] <= 74)
    for name, k, rule in (("B-1 M treatment", ANCHOR["M"], ">=75 outside band"),
                          ("B-2 C3 liveness", ANCHOR["C3"], ">=108"),
                          ("B-3 C1 leak", ANCHOR["C1"], "<=74 inside band"),
                          ("B-4 cement M", ANCHOR["cement_M"], ">=75"),
                          ("B-4 cement C1", ANCHOR["cement_C1"], "<=74")):
        p = binom_two_sided_p(k, n, P0)
        print(f"  {name:18s} = {k}/{n}  ({rule})  two-sided p={p:.3e}")

    # === Generator: fit the two codecs =====================================
    print(f"\n[Generator] fitting BPE-jamo codecs (K={K}, {BPE_SAMPLE_LINES} lines/phase)")
    s1 = ST.stream_sample(spec, 1, BPE_SAMPLE_LINES)
    s2 = ST.stream_sample(spec, 2, BPE_SAMPLE_LINES)
    codec_p1 = C.fit_bpe_jamo(s1, K)
    codec_p2 = C.fit_bpe_jamo(s2, K)
    print(f"  codec_p1 merges={len(codec_p1)}  codec_p2 merges={len(codec_p2)}")

    # N-1 drift existence
    probes = ST.probes(spec)
    rate = C.boundary_shift_rate(codec_p1, codec_p2, probes)
    m["boundary_shift_rate"] = rate
    m["drift_floor"] = DRIFT_FLOOR
    print(f"\n[N-1] boundary-shift rate = {rate:.4f}  (floor {DRIFT_FLOOR})")

    # N-2 contrast existence — audit novel allomorphs IN CONTEXT
    novel = spec["novel_neg_forms"]
    heldout = spec["heldout_stems"]
    fic = []
    for i, af in enumerate(novel):
        stem = heldout[i % len(heldout)]
        ctx = to_jamo(render(stem, [af]))
        fic.append((to_jamo(af), ctx))
    aud_frozen = C.atomicity_audit(codec_p1, fic)
    aud_refit = C.atomicity_audit(codec_p2, fic)
    m["deficit_frozen"] = aud_frozen["deficit"]
    m["deficit_refit"] = aud_refit["deficit"]
    m["frozen_single_token"] = aud_frozen["single_token"]
    m["refit_single_token"] = aud_refit["single_token"]
    print(f"[N-2] frozen codec: {aud_frozen['single_token']}/{aud_frozen['n']} single-token "
          f"-> deficit={aud_frozen['deficit']:.3f} (want 1.0)")
    print(f"      refit  codec: {aud_refit['single_token']}/{aud_refit['n']} single-token "
          f"-> deficit={aud_refit['deficit']:.3f} (want 0.0)")

    # N-3 emittability (after leak filtering, below)
    items = ST.eval_items(spec)
    m["eval_candidate_pairs"] = len(items)

    # N-4 zero leak — scan both phase streams for eval-string substrings.
    # Cap the scan at a bounded prefix of each phase for tractability at $0;
    # a leak that only appears deep in the stream is still a leak, so record
    # the scanned byte count honestly.
    scan_lines = 200000
    # Scan the NEG eval forms only: `pos` forms are held-out stem + PLAIN affix,
    # which the stream emits legitimately (the stems are in-distribution — that is
    # the design, not a leak). Only the novel (stem x NEG) composition must be absent.
    forms = sorted({it["neg"] for it in items})
    def _bounded(phase):
        rng_iter = ST.stream(spec, phase)
        for i, ch in enumerate(rng_iter):
            if i >= scan_lines:
                break
            yield ch
    leak1 = A.leak_scan(_bounded(1), spec, forms)
    leak2 = A.leak_scan(_bounded(2), spec, forms)
    cooc = A.heldout_neg_cooccurrence(spec, _bounded(1))
    total_leak = leak1["total"] + leak2["total"]
    m["leak_hits"] = total_leak
    m["heldout_neg_cooccurrence"] = cooc
    m["leak_scan_lines_per_phase"] = scan_lines
    n_clean = len(items) if total_leak == 0 else len(items) - total_leak
    m["n_clean_items"] = n_clean
    m["n_required_worst"] = N_REQUIRED_WORST
    print(f"[N-3] clean held-out items = {n_clean} (need >= {N_REQUIRED_WORST})")
    print(f"[N-4] leak hits = {total_leak}  ·  heldout-NEG co-occurrence = {cooc}  "
          f"(scanned {scan_lines} lines/phase)")

    # N-5 determinism + round-trip
    hash2 = S.spec_hash(S.build_spec())
    codec_p1b = C.fit_bpe_jamo(ST.stream_sample(spec, 1, BPE_SAMPLE_LINES), K)
    merges_match = codec_p1.merges == codec_p1b.merges
    rt_ok = True
    for st in spec["stems"][:50]:
        for af in ST.neg_forms if False else [spec["affixes_p1"][0]["form"]]:
            surf = render(st, [af])
            p = parse(surf, spec["stems"], [a["form"] for a in spec["affixes_p1"]])
            if p[0] != st or from_jamo(to_jamo(surf)) != surf:
                rt_ok = False
    m["spec_hash_stable"] = (hash2 == got_hash)
    m["bpe_deterministic"] = merges_match
    m["roundtrip_ok"] = rt_ok
    print(f"[N-5] spec_hash stable={m['spec_hash_stable']}  bpe_deterministic={merges_match}  "
          f"roundtrip={rt_ok}")

    # === ledger ============================================================
    falsifiers = [
        Falsifier("B-1 treatment above floor", lambda x: not x["B1_M_above"], "M inside chance band"),
        Falsifier("B-2 liveness", lambda x: not x["B2_C3_live"], "C3 could not detect handed flip"),
        Falsifier("B-3 leak test", lambda x: not x["B3_C1_no_leak"], "control above chance = leak"),
        Falsifier("B-4 replication", lambda x: not x["B4_cement_agrees"], "replicate disagrees"),
        Falsifier("N-1 drift existence", lambda x: x["boundary_shift_rate"] < x["drift_floor"],
                  "stream cannot move the codec"),
        Falsifier("N-2 contrast existence",
                  lambda x: x["deficit_frozen"] < 1.0 or x["deficit_refit"] > 0.0,
                  "no atomicity contrast to measure"),
        Falsifier("N-3 emittability", lambda x: x["n_clean_items"] < x["n_required_worst"],
                  "underpowered by construction"),
        Falsifier("N-4 zero leak", lambda x: x["leak_hits"] > 0 or x["heldout_neg_cooccurrence"] > 0,
                  "eval measures memory not recombination"),
        Falsifier("N-5 determinism+roundtrip",
                  lambda x: not (x["spec_hash_stable"] and x["bpe_deterministic"] and x["roundtrip_ok"]),
                  "rig not reproducible"),
        Falsifier("genspec matches card", lambda x: not x["genspec_matches_card"],
                  "spec drifted from the frozen hash"),
    ]
    ledger = evaluate(m, falsifiers)
    m["rig"] = "LICENSED" if ledger["all_pass"] else "REFUSED"

    print("\n" + "=" * 78)
    print("FALSIFIER LEDGER")
    print("=" * 78)
    for r in ledger["falsifiers"]:
        print(f"  {r['status']:4s}  {r['name']}")
    print(f"\n  {ledger['n_pass']}/{ledger['n_total']} PASS")
    print(f"\n  VERDICT: rig = {m['rig']}")

    out = os.path.join(_HERE, "result.json")
    with open(out, "w") as f:
        json.dump({"metrics": m, "falsifiers": ledger["falsifiers"],
                   "n_pass": ledger["n_pass"], "n_total": ledger["n_total"],
                   "rig": m["rig"]}, f, ensure_ascii=False, indent=1)
        f.write("\n")
    print(f"\n  artifacts: {os.path.relpath(out, _ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
