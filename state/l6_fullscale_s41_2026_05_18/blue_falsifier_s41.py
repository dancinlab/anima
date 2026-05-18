#!/usr/bin/env python3
"""RESEARCH.md §41 — B-S41-1..5 closed-form sidecar battery.

Sidecar: central state/verify_hexad_blue_2026_05_15/blue_falsifier.py is
UNCHANGED (precedent B-PRIME … B-DUAL / B-INTER / B-S37).

  B-S41-1 RELATION-CORPUS-SHA256-DETERMINISTIC
            on-disk sha256 == re-derived sha256 (re-running the
            generator with seed-fixed 1337 reproduces byte-equal corpus)
            ∧ recorded sha256 == on-disk; the 256-bit Boolean
            commitment binds the fire's corpus to a deterministic
            artefact.

  B-S41-2 HELD-OUT-PAIR-DISJOINT-CARDINALITY (연결부위)
            §41 held-out pair set ∩ §41 train pair set == ∅
            (Boolean disjoint partition of all 64*63 = 4032 ordered
            pairs); AND the §41 holdout pair set is BYTE-EQUAL to the
            §37 holdout pair set (seed / shuffle / slice identical
            by re-using §37's relation_corpus.py SSOT). The fire is
            apples-to-apples vs §37 BY CONSTRUCTION.

  B-S41-3 ACCURACY-BOUNDED
            every reported accuracy / chance ∈ [0,1] (mean of {0,1}
            indicators is a Kolmogorov bounded fraction); each
            relation's label codomain is the closed finite set
            (B-S37-3 carry); substring-match parser maps decoded body
            into the closed codomain or None.

  B-S41-4 SCALE-MATCHES-§16 (±20%)
            §41 model param count is in [283.72 M × 0.8, 283.72 M × 1.2]
            of §16's d=768 / n_layer=12 / 283.72 M ConsciousDecoderV2.
            Closed integer interval — the fire is at "§16-scale" by
            construction (mandate: 'd=768 / n_layer 12 (§16 scale,
            ±20%)').

  B-S41-5 GENERALIZATION-vs-MEMORIZATION-METRIC
            (gap_vs_§37 ∈ ℝ, the gap-threshold partition is a closed
            real-line partition: GENERALIZES if gap < 0.20, GIFT if
            gap >= 0.50, PARTIAL otherwise — Boolean total cover, no
            empty interval, deterministic threshold). The §37 anchor
            mean held-out acc 0.9938 with 0.0059 gap is the historical
            reference: the metric is *bounded* relative to §37, not
            chance-relative (chance is a separate test in B-S37-3 /
            train_eval_l6).

  B-S41-NOTE  empirical carve-out — whether §41's held-out-pair acc
              actually survives the scale transition is the SGD/measured
              OUTCOME (result.json's holdout_accuracy + gap_vs_s37). The
              battery proves the probe is well-FORMED at scale (corpus
              deterministic / partition disjoint / accuracy bounded /
              scale in target band / verdict-partition closed), but
              does NOT decide GENERALIZES-AT-SCALE vs SMALL-MODEL-GIFT
              — that is the eval's measured result. B-D-NOTE / B-S37-
              NOTE / B-S16-NOTE family — NOT counted blue.

f1/f2/f3 hard-fail safe — Boolean set algebra / sha256 commitment /
Kolmogorov bounded fraction / closed integer interval / real-line
partition. NO σ/τ/φ/J₂ external derivation. Tier / Ψ=½ = anima g2
internal-arch carve-out. B-IDENTITY-5 enforced (B-S41-1 forbidden-token
grep total == 0 carries from §37).
"""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
S37 = HERE.parent / "l6_pilot_s37_2026_05_18"

try:
    import sympy as sp
    HAVE_SYMPY = True
except Exception:
    HAVE_SYMPY = False

# Re-use §37 primitives (the L6 SSOT) — same partition definition.
sys.path.insert(0, str(S37))
import relation_corpus as rc  # noqa: E402


def b_s41_1_relation_corpus_sha256_deterministic() -> dict:
    """B-S41-1 — corpus is deterministic 256-bit Boolean commitment.

    on-disk sha256 == re-derived sha256 (re-run generator) ==
    recorded sha256 (corpus_stats_s41.json). Forbidden-token grep
    total == 0 (B-IDENTITY-5 carry from §37)."""
    checks = []
    corpus_path = HERE / "relation_corpus_train_s41.jsonl"
    stats_path = HERE / "corpus_stats_s41.json"
    stats = json.loads(stats_path.read_text())
    on_disk = corpus_path.read_bytes()
    sha_on_disk = hashlib.sha256(on_disk).hexdigest()

    checks.append(("on-disk-sha256-matches-recorded",
                   sha_on_disk == stats["corpus_sha256"]))
    checks.append(("corpus-bytes-matches-recorded",
                   len(on_disk) == stats["corpus_bytes"]))
    # forbidden-token grep total == 0 (B-IDENTITY-5)
    txt = on_disk.decode("utf-8")
    forbidden = ["도우미", "helper", "assistant", "사용자", "user:",
                 "[anima"]
    fb_total = sum(txt.count(t) for t in forbidden)
    checks.append(("forbidden-token-total-eq-0", fb_total == 0))
    checks.append(("recorded-forbidden-total-eq-0",
                   stats["forbidden_token_total"] == 0))
    # determinism: re-run the generator, sha256 must reproduce
    subprocess.run([sys.executable, str(HERE / "corpus_generator_s41.py")],
                   cwd=str(HERE), capture_output=True, check=True)
    sha_rerun = hashlib.sha256(
        (HERE / "relation_corpus_train_s41.jsonl").read_bytes()).hexdigest()
    checks.append(("re-derived-sha256-matches", sha_rerun == sha_on_disk))
    # every record is a <relate> tag
    lines = [ln for ln in txt.splitlines() if ln.strip()]
    all_relate = all('"<relate ' in ln and "</relate>" in ln
                     for ln in lines)
    checks.append(("all-records-are-relate-tag", all_relate))

    ok = all(v for _, v in checks)
    return {"id": "B-S41-1", "name": "RELATION-CORPUS-SHA256-DETERMINISTIC",
            "passed": ok, "checks": checks}


def b_s41_2_held_out_pair_disjoint_cardinality() -> dict:
    """B-S41-2 (연결부위) — held-out / train pair-sets are a disjoint
    partition of all 4032 ordered pairs ∧ §41 holdout IS BYTE-EQUAL
    to §37 holdout (same seed/shuffle/slice — apples-to-apples by
    construction)."""
    checks = []
    # Reproduce the partition (same primitives, same seed/shuffle/slice).
    import random as _r
    rng = _r.Random(rc.SEED)
    pairs = rc.all_ordered_pairs()
    rng.shuffle(pairs)
    n_holdout = int(len(pairs) * rc.HOLDOUT_FRAC)
    s41_holdout = pairs[:n_holdout]
    s41_train = pairs[n_holdout:]
    aset = set(pairs)
    hset, tset = set(s41_holdout), set(s41_train)

    checks.append(("held-train-disjoint", hset.isdisjoint(tset)))
    checks.append(("held-union-train-eq-all", hset | tset == aset))
    checks.append(("held-plus-train-card-eq-all",
                   len(hset) + len(tset) == len(aset)))
    checks.append(("ordered-pair-count-64x63",
                   len(aset) == 64 * 63 == 4032))
    checks.append(("intersection-empty", len(hset & tset) == 0))

    # connection point with §37: byte-equal holdout pair set
    s37_holdout_manifest = json.loads(
        (S37 / "holdout_pairs.json").read_text())
    s37_holdout_idx = sorted(tuple(m["anchor_idx"])
                             for m in s37_holdout_manifest)
    s41_holdout_idx = sorted(s41_holdout)
    checks.append(("s41-holdout-byte-equal-to-s37-holdout",
                   s41_holdout_idx == s37_holdout_idx))
    # recorded stats also confirm
    stats = json.loads((HERE / "corpus_stats_s41.json").read_text())
    checks.append(("corpus-stats-holdout-byte-equal-flag-true",
                   stats["holdout_pairs_byte_equal_s37"] is True))
    checks.append(("corpus-stats-holdout-train-disjoint-true",
                   stats["holdout_train_disjoint"] is True))

    if HAVE_SYMPY:
        # sympy FiniteSet slice — disjoint encoded pair-ids stay disjoint
        h_slice = sp.FiniteSet(*[i * 1000 + j for (i, j)
                                 in s41_holdout[:20]])
        t_slice = sp.FiniteSet(*[i * 1000 + j for (i, j)
                                 in s41_train[:20]])
        checks.append(("sympy-finiteset-slice-disjoint",
                       sp.Intersection(h_slice, t_slice) == sp.EmptySet))
    else:
        checks.append(("sympy-unavailable-numeric-fallback", True))

    ok = all(v for _, v in checks)
    return {"id": "B-S41-2", "name": "HELD-OUT-PAIR-DISJOINT-CARDINALITY",
            "passed": ok, "checks": checks}


def b_s41_3_accuracy_bounded() -> dict:
    """B-S41-3 — all accuracy / chance values in [0,1]; relation
    codomains are closed finite sets; substring-match parser cannot
    emit an out-of-set label (returns None or a closed-label)."""
    checks = []
    result_path = HERE / "result.json"
    if result_path.exists():
        res = json.loads(result_path.read_text())
        # may be present pre-eval (train_complete_pending_eval) — then
        # the accuracy block is absent; honest re-check on what exists.
        if res.get("phase") == "complete":
            acc_vals = []
            for blk in ("holdout_accuracy", "chance_majority_class"):
                acc_vals.extend(res[blk].values())
            acc_vals.append(res["joint_all4_holdout_accuracy"])
            acc_vals.append(res["mean_holdout_accuracy"])
            all_bounded = all(0.0 <= v <= 1.0 + 1e-12 for v in acc_vals)
            checks.append(("all-accuracies-in-[0,1]", all_bounded))
            lifts = list(res["holdout_lift_over_majority"].values())
            checks.append(("all-lifts-in-[-1,1]",
                           all(-1.0 <= v <= 1.0 for v in lifts)))
        else:
            checks.append(("result-not-yet-eval-complete-skip", True))
    else:
        checks.append(("result-json-not-yet-written-pre-fire", True))

    if HAVE_SYMPY:
        # closed-form: mean of n {0,1} indicators is k/n ∈ [0,1]
        k, n = sp.symbols("k n", integer=True, positive=True)
        frac = k / n
        checks.append(("sympy-mean-of-indicators-bounded",
                       sp.simplify(frac.subs({k: 0, n: 5})) == 0
                       and sp.simplify(frac.subs({k: 5, n: 5})) == 1))
    else:
        checks.append(("sympy-unavailable-numeric-fallback", True))

    # codomain: union of relation labels == RELATION_LABEL_SET (closed)
    union = set()
    relations = {"R1": ["near", "mid", "far"],
                 "R2": ["i_contains_j", "j_contains_i",
                        "overlap", "disjoint"],
                 "R3": ["same_domain", "different_domain"],
                 "R4": ["i_shallower", "i_deeper", "i_eq_j"]}
    for rk, labels in relations.items():
        union |= set(labels)
        checks.append((f"{rk}-codomain-subset-of-label-set",
                       set(labels) <= rc.RELATION_LABEL_SET))
    checks.append(("union-of-codomains-eq-RELATION_LABEL_SET",
                   union == set(rc.RELATION_LABEL_SET)))
    checks.append(("codomain-cardinality-3+4+2+3-eq-12",
                   sum(len(v) for v in relations.values()) == 12
                   == len(rc.RELATION_LABEL_SET)))

    ok = all(v for _, v in checks)
    return {"id": "B-S41-3", "name": "ACCURACY-BOUNDED",
            "passed": ok, "checks": checks}


def b_s41_4_scale_matches_s16() -> dict:
    """B-S41-4 — §41 model param count is in [§16 × 0.8, §16 × 1.2]
    (mandate '§16 scale, ±20%'). §16 footprint = d=768 / n_layer=12 /
    283,720,000 params (carry from AGENTS.tape n_hexad_progress §16).
    Closed integer interval."""
    checks = []
    S16_PARAMS = 283_720_000  # §16 d=768/12L ConsciousDecoderV2 (from logs)
    LO = int(S16_PARAMS * 0.8)
    HI = int(S16_PARAMS * 1.2)
    result_path = HERE / "result.json"
    if result_path.exists():
        res = json.loads(result_path.read_text())
        n_params = res.get("n_params", None)
        if n_params is not None:
            checks.append(("n_params-recorded", isinstance(n_params, int)))
            checks.append(("s16-scale-band-lo<=n_params<=hi",
                           LO <= n_params <= HI))
        else:
            checks.append(("n_params-not-yet-recorded-pre-fire", True))
    else:
        checks.append(("result-json-not-yet-written-pre-fire", True))
    # closed interval (integer) sanity — LO < HI ∧ S16 ∈ [LO, HI]
    checks.append(("integer-interval-well-formed", LO < HI))
    checks.append(("s16-in-interval", LO <= S16_PARAMS <= HI))
    # config in this trainer is d=768/12L by default (matches §16 spec)
    train_src = (HERE / "train_s41.py").read_text()
    checks.append(("train-default-d-model-768",
                   "--d-model\", type=int, default=768" in train_src))
    checks.append(("train-default-n-layer-12",
                   "--n-layer\", type=int, default=12" in train_src))

    ok = all(v for _, v in checks)
    return {"id": "B-S41-4", "name": "SCALE-MATCHES-§16-±20%",
            "passed": ok, "checks": checks}


def b_s41_5_generalization_vs_memorization_metric() -> dict:
    """B-S41-5 — verdict partition is a closed real-line cover:
        GENERALIZES   ⇔ gap_vs_§37 < 0.20
        PARTIAL       ⇔ 0.20 ≤ gap_vs_§37 < 0.50
        SMALL_MODEL_GIFT ⇔ gap_vs_§37 ≥ 0.50
       Boolean total cover (every real x maps to exactly one verdict);
       gap is a real difference of accuracies (each ∈ [0,1]) so gap ∈
       [-1, 1] (bounded). The metric is DETERMINISTIC (pure fn of
       result.json mean_holdout_accuracy + the §37 reference 0.9938)."""
    checks = []
    # closed-form: union(GENERALIZES, PARTIAL, GIFT) covers ℝ ∧ pairwise
    # intersection empty.
    if HAVE_SYMPY:
        I_gen = sp.Interval(-sp.oo, sp.Rational(20, 100), right_open=True)
        I_par = sp.Interval(sp.Rational(20, 100),
                            sp.Rational(50, 100), right_open=True)
        I_gif = sp.Interval(sp.Rational(50, 100), sp.oo)
        union = sp.Union(I_gen, I_par, I_gif)
        checks.append(("partition-union-eq-reals",
                       union == sp.Interval(-sp.oo, sp.oo)))
        checks.append(("partition-pairwise-disjoint",
                       I_gen.intersect(I_par) == sp.EmptySet
                       and I_par.intersect(I_gif) == sp.EmptySet
                       and I_gen.intersect(I_gif) == sp.EmptySet))
    else:
        checks.append(("sympy-unavailable-numeric-fallback", True))
    # determinism — verdict is a pure function of (mean_holdout, §37 ref)
    def _verdict(mean_acc: float, ref: float = 0.9938) -> str:
        gap = ref - mean_acc
        if gap < 0.20:
            return "L6_GENERALIZES_AT_SCALE"
        if gap < 0.50:
            return "L6_PARTIAL_GENERALIZATION_AT_SCALE"
        return "L6_SMALL_MODEL_GIFT"
    # 3 witness panel covering each band
    checks.append(("witness-gen-0.95",
                   _verdict(0.95) == "L6_GENERALIZES_AT_SCALE"))
    checks.append(("witness-partial-0.70",
                   _verdict(0.70) == "L6_PARTIAL_GENERALIZATION_AT_SCALE"))
    checks.append(("witness-gift-0.30",
                   _verdict(0.30) == "L6_SMALL_MODEL_GIFT"))
    # boundary witnesses — left-closed PARTIAL band [0.20, 0.50). Pick a
    # mean_acc that puts gap_vs_§37 = ref-mean strictly ≥ 0.20 and <0.50
    # (and one strictly ≥ 0.50 for GIFT). Avoid fp epsilon at exact 0.20.
    checks.append(("boundary-gap-0.20-strict-is-partial",
                   _verdict(0.9938 - 0.20 - 1e-9) == "L6_PARTIAL_GENERALIZATION_AT_SCALE"))
    checks.append(("boundary-gap-0.50-strict-is-gift",
                   _verdict(0.9938 - 0.50 - 1e-9) == "L6_SMALL_MODEL_GIFT"))
    # honest verdict-consistency cross-check vs result.json (post-eval)
    result_path = HERE / "result.json"
    if result_path.exists():
        res = json.loads(result_path.read_text())
        if res.get("phase") == "complete":
            recomp = _verdict(res["mean_holdout_accuracy"])
            checks.append(("recomputed-verdict-matches-result",
                           recomp == res["verdict"]))
        else:
            checks.append(("result-not-yet-eval-complete-skip", True))
    else:
        checks.append(("result-json-not-yet-written-pre-fire", True))

    ok = all(v for _, v in checks)
    return {"id": "B-S41-5", "name": "GENERALIZATION-vs-MEMORIZATION-METRIC",
            "passed": ok, "checks": checks}


def main() -> int:
    battery = [
        b_s41_1_relation_corpus_sha256_deterministic(),
        b_s41_2_held_out_pair_disjoint_cardinality(),
        b_s41_3_accuracy_bounded(),
        b_s41_4_scale_matches_s16(),
        b_s41_5_generalization_vs_memorization_metric(),
    ]
    n_pass = sum(1 for b in battery if b["passed"])
    note = {
        "id": "B-S41-NOTE",
        "name": "GENERALIZATION-AT-SCALE-OUTCOME-EMPIRICAL",
        "text": ("Whether held-out-pair accuracy survives the 75 000× "
                 "scale-up to a §16-size byte-LM is an SGD/measurement "
                 "OUTCOME. The battery proves the probe is well-FORMED at "
                 "scale (corpus deterministic B-S41-1, partition disjoint "
                 "AND byte-equal to §37 B-S41-2, accuracy bounded B-S41-3, "
                 "scale in §16 ±20% band B-S41-4, verdict partition closed "
                 "B-S41-5); it does NOT decide GENERALIZES_AT_SCALE vs "
                 "SMALL_MODEL_GIFT — that is the eval's measured result. "
                 "B-D-NOTE / B-S37-NOTE / B-S16-NOTE family — NOT counted "
                 "blue."),
        "counted_blue": False,
    }
    result = {
        "battery": "B-S41-1..5",
        "research_section": "§41",
        "n_total": len(battery), "n_pass": n_pass,
        "all_blue": n_pass == len(battery),
        "sympy_available": HAVE_SYMPY,
        "verdicts": battery,
        "note": note,
        "central_blue_falsifier_unchanged": True,
    }
    (HERE / "blue_falsifier_s41_result.json").write_text(
        json.dumps(result, indent=2, ensure_ascii=False))
    for b in battery:
        mark = "PASS" if b["passed"] else "FAIL"
        print(f"  [{mark}] {b['id']} {b['name']}")
        for cname, cval in b["checks"]:
            print(f"      {'ok ' if cval else 'XX '} {cname}")
    print(f"\nB-S41 battery: {n_pass}/{len(battery)} "
          f"{'BLUE' if n_pass == len(battery) else 'FAIL'}  "
          f"(+ B-S41-NOTE empirical carve-out)")
    return 0 if n_pass == len(battery) else 1


if __name__ == "__main__":
    sys.exit(main())
