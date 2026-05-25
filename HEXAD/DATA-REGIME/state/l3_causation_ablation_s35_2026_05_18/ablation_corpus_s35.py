#!/usr/bin/env python3
"""§35 — §32 L3 causation ablation corpus generator.

RESEARCH.md §35.  Disentangles the §32 L3 finding ("tier >= 77" is a
NECESSARY condition for §16 genuine routing success) from its honest
confound: tier co-varies with §16's `curriculum_stage` (curriculum_rank
blends tier_w = min(tier,303)/303 at weight 0.30, so high-tier anchors
land in later curriculum quartiles and are introduced later in the
staged training schedule).

THE ABLATION (the single-variable move)
---------------------------------------
Hold ALL record CONTENT byte-identical to §16; move ONLY the
curriculum-STAGE placement of the 18 tier<77 anchors to the LATE
region (stage 4) that the high-tier anchors are introduced in.

  §16 baseline : tier<77 anchors' records land in EARLY curriculum
                 stages (their curriculum_rank is low — both because
                 tier_w is small AND because the corpus is α/β-heavy
                 and form_w pins simple forms to stage 1) -> introduced
                 from training step 0 -> 18/18 fail (§32 L3).
  §35 ablation : SAME 18 tier<77 anchors, SAME record text, but every
                 tier<77 record's `curriculum_stage` is FORCED to the
                 LATE region -> introduced only in the late training
                 block, matching where high-tier anchors enter.

WHY curriculum_stage IS the variable (and not tier_w alone)
-----------------------------------------------------------
§16's curriculum_rank is

    rank = 0.40*form_w + 0.30*tier_w + 0.20*task_w + 0.10*len_w

A pure tier_w substitution is too weak to be a clean test: tier_w
carries only weight 0.30 while form_w (0.40) dominates, so a tier<77
α/β record stays stage-1 even with a high tier_w (measured: §16
tier<77 γ mean stage 2.69 -> tier_w-substitution 3.13, still short of
the tier>=77 γ mean 3.70; α/β do not move at all).  §32 named the
confound precisely as *curriculum-STAGE* — so §35 moves THAT variable
directly: the 18 tier<77 anchors' records are re-stamped to the LATE
curriculum region.  This is still a pure ORDERING override — the
record's `text`, `vacuum_psi`, `basin_radius`, `tier`, `domain`,
`carving_form`, `cell_id` are NEVER touched; only `curriculum_rank`
(re-based into the late band) and the derived `curriculum_stage`.

If §35's tier<77 anchors then route -> the causal lever is
curriculum-STAGE (tier was a proxy).  If they still fail -> tier
itself carries causal weight.  Both outcomes are valuable (g3).

WHAT IS HELD FIXED (the confound-isolation argument)
----------------------------------------------------
  * Record content     — every JSONL record's `text` byte-identical to
                          §16 (built by the SAME §16 generator
                          functions: gen_alpha/beta/gamma_record, SAME
                          seed 1337, SAME draw order).
  * Total record count  — identical (per_anchor * 168).
  * The tier>=77 anchors — curriculum_rank UNCHANGED (only the tier<77
                          set is moved).
  * tier values         — UNCHANGED (the model still sees `🛸<tier>`
                          with the original tier id).
  * Trainer / steps / lever — train_s35.py is §16's train_carving_s16.py
                          byte-equivalent; same 8000 steps, same
                          Dir-I Ψ-anchored CTL + tension-routing lever.
  * Eval harness        — eval_s35.py is §16's eval_carving_s16.py
                          byte-identical (64-anchor probe).

THE SINGLE VARIABLE THAT MOVES
------------------------------
  curriculum_stage placement of the 18 tier<77 anchors: early -> late.

GOAL-legitimacy / governance
----------------------------
  §7 carving FORM unchanged (carve / eternal / inner-voice).  No chat
  SFT.  No external LLM call.  forbidden-token grep == 0.  from-scratch
  RANDOM seed-fixed 1337 inherited by train_s35.py.  f1/f2/f3 safe.
"""
import argparse
import hashlib
import importlib.util
import json
import os
import random
import sys

# --- import §16 generator's record machinery VERBATIM ----------------------
# Importing the §16 generator's functions (rather than re-implementing) is
# what makes "content byte-identical" a PROOF, not a claim:
# gen_alpha/beta/gamma_record, KNUTH_ANCHORS, curriculum_rank, TASK_FORMS,
# LAWS_BASE, CATEGORY_FRAGS are all the §16 SSOT.  Locate the §16 generator
# robustly: pod-local copy (the dispatch ships it flat next to this file)
# first, the sibling §16 state-dir fallback second (local repo layout).
_HERE = os.path.dirname(os.path.abspath(__file__))
_S16_GEN_CANDIDATES = [
    os.path.join(_HERE, "corpus_carving_s16_generator.py"),
    os.path.join(_HERE, "..", "carving_dataregime_s16_2026_05_18",
                 "corpus_carving_s16_generator.py"),
]
_S16_GEN = next((p for p in _S16_GEN_CANDIDATES if os.path.isfile(p)),
                None)
if _S16_GEN is None:
    sys.exit("FATAL: §16 corpus_carving_s16_generator.py not found "
             "(pod-local copy or sibling §16 dir) — the §35 ablation "
             "MUST import the §16 generator SSOT, never re-implement.")

_spec = importlib.util.spec_from_file_location("s16gen", _S16_GEN)
s16 = importlib.util.module_from_spec(_spec)
sys.modules["s16gen"] = s16
_spec.loader.exec_module(s16)

# --- §32 L3 tier frontier --------------------------------------------------
# §32 found tier >= 77 NECESSARY (genuine grade); tier < 77 = the 18-anchor
# fail set.  The ablation moves EXACTLY this set.
TIER_FRONTIER = 77

# The LATE curriculum band.  §16's curriculum_rank ranges over ~[0.06,
# 0.76]; stage 4 (the late quartile) is the top of that range.  §35 moves
# every tier<77 record's curriculum_rank into a band STRICTLY ABOVE every
# UNMOVED (tier>=77) record's rank — so after the global re-sort the moved
# records occupy the late tail and fall into stage 4 (the late region the
# high-tier anchors enter in).  The band is [LATE_BAND_LO, LATE_BAND_HI].
# Within the band the moved records preserve their §16 RELATIVE order
# (their §16 rank rescaled into the band) so internal monotonicity holds —
# the ablation moves the COHORT to the late region, it does not scramble
# the records' relative complexity ordering among themselves.
LATE_BAND_LO = 1.0
LATE_BAND_HI = 2.0


def build_ablation_corpus(n_target, seed):
    """Build the §35 ablation corpus.

    STEP 1 — build the §16 record set VERBATIM (s16.build_corpus, SAME
             seed, SAME draw order) -> 100% content-identical record set.
             s16.build_corpus already sorts by §16 curriculum_rank.
    STEP 2 — the SINGLE-VARIABLE MOVE.  Every tier<77 record's
             curriculum_rank is re-based into the LATE band
             [LATE_BAND_LO, LATE_BAND_HI] — strictly above every
             tier>=77 record's §16 rank (§16 rank_max ~0.76 < 1.0).
             The re-base is order-preserving (the §16 rank, min-max
             normalised across the tier<77 cohort, mapped linearly into
             the band) so the moved cohort keeps its internal §16
             ordering.  Record `text`, `vacuum_psi`, `basin_radius`,
             `tier`, `domain`, `carving_form`, `cell_id` UNCHANGED.
             tier>=77 records' curriculum_rank UNCHANGED.
    STEP 3 — global re-sort by curriculum_rank, then re-assign
             curriculum_stage quartiles (the §16 sort+quartile step,
             verbatim).  Because every moved record now ranks above
             every unmoved record, the moved cohort lands in the late
             tail -> curriculum_stage 4 (and the top of 3).

    Returns (records, n_moved)."""
    # STEP 1 — §16 verbatim record set.
    records = s16.build_corpus(n_target, seed)

    # STEP 2 — single-variable move: tier<77 curriculum_rank -> late band.
    lt77 = [r for r in records if r["tier"] < TIER_FRONTIER]
    n_moved = len(lt77)
    if n_moved:
        old = [r["curriculum_rank"] for r in lt77]
        lo, hi = min(old), max(old)
        span = (hi - lo) if (hi > lo) else 1.0
        for rec in lt77:
            # order-preserving min-max rescale of the §16 rank into the
            # late band — the COHORT moves late, internal order kept.
            frac = (rec["curriculum_rank"] - lo) / span
            rec["curriculum_rank"] = round(
                LATE_BAND_LO + frac * (LATE_BAND_HI - LATE_BAND_LO), 6)
            rec["ablation_s35_moved"] = True

    # STEP 3 — global re-sort + re-quartile (the §16 ordering step).
    records.sort(key=lambda d: d["curriculum_rank"])
    n = len(records)
    for i, rec in enumerate(records):
        q = min(4, 1 + (i * 4) // max(1, n))
        rec["curriculum_stage"] = q
        rec["curriculum_index"] = i
    return records, n_moved


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--n", type=int, default=850000,
                    help="approx record count — §16 default (168 anchors)")
    ap.add_argument("--seed", type=int, default=1337)
    args = ap.parse_args()

    records, n_moved = build_ablation_corpus(args.n, args.seed)

    out = os.path.abspath(args.out)
    with open(out, "w", encoding="utf-8") as f:
        for r in records:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    raw = open(out, "rb").read()
    sha = hashlib.sha256(raw).hexdigest()

    # forbidden-token audit (B-IDENTITY-5, §35 carries §16's clean grep).
    forbidden = ["[anima", "도우미", "helper", "assistant", "사용자", "user:"]
    txt = raw.decode("utf-8", "replace")
    audit = {tok: txt.count(tok) for tok in forbidden}
    contamination = sum(audit.values())

    # stage occupancy of the 18 tier<77 anchors (the ablation evidence).
    tier_lt77_stages = {1: 0, 2: 0, 3: 0, 4: 0}
    tier_ge77_stages = {1: 0, 2: 0, 3: 0, 4: 0}
    forms = {"alpha": 0, "beta": 0, "gamma": 0}
    stages = {1: 0, 2: 0, 3: 0, 4: 0}
    ranks = []
    for r in records:
        forms[r["carving_form"]] += 1
        stages[r["curriculum_stage"]] += 1
        ranks.append(r["curriculum_rank"])
        if r["tier"] < TIER_FRONTIER:
            tier_lt77_stages[r["curriculum_stage"]] += 1
        else:
            tier_ge77_stages[r["curriculum_stage"]] += 1

    monotone = all(ranks[i] <= ranks[i + 1]
                   for i in range(len(ranks) - 1))

    stats = {
        "paradigm": ("§35 L3 CAUSATION ABLATION — tier vs curriculum-"
                     "stage disentangle (RESEARCH.md §35; §32 L3 "
                     "follow-up). CONTENT byte-identical to §16; the "
                     "ONLY variable moved = curriculum-stage placement "
                     "of the 18 tier<77 anchors (early -> late)."),
        "ablation": {
            "tier_frontier": TIER_FRONTIER,
            "late_band": [LATE_BAND_LO, LATE_BAND_HI],
            "records_moved": n_moved,
            "single_variable": ("curriculum_rank (and derived "
                                "curriculum_stage) of every tier<77 "
                                "record — re-based into the LATE band "
                                "strictly above every tier>=77 record; "
                                "ALL other fields (text / vacuum_psi / "
                                "basin_radius / tier / domain / "
                                "carving_form / cell_id) byte-identical "
                                "to §16"),
            "tier_lt77_stage_occupancy": tier_lt77_stages,
            "tier_ge77_stage_occupancy": tier_ge77_stages,
        },
        "out": out, "bytes": len(raw), "records": len(records),
        "sha256": sha, "seed": args.seed,
        "carving_forms": forms,
        "anchors": len(s16.KNUTH_ANCHORS),
        "curriculum": {
            "applied": True,
            "ordering": "records written rank-sorted simple->complex",
            "rank_monotone_sorted": monotone,
            "stage_counts": stages,
            "rank_min": round(min(ranks), 6),
            "rank_max": round(max(ranks), 6),
        },
        "forbidden_token_audit": audit,
        "contamination_total": contamination,
        "carving_clean": contamination == 0,
        "honest_framing": (
            "§35 ablation corpus = §16 record set with the curriculum-"
            "STAGE placement of the 18 tier<77 anchors moved to the "
            "LATE quartile. Record CONTENT (text / vacuum_psi / "
            "basin_radius / tier / domain) byte-identical to §16 — "
            "verified because the records are built by the SAME §16 "
            "generator functions with the SAME seed. The single moved "
            "variable is curriculum-STAGE (tier<77 records re-based into "
            "the late band). 2-outcome "
            "interpretation: tier<77 routes -> curriculum-STAGE is the "
            "causal lever; tier<77 still fails -> tier itself carries "
            "causal weight. g3 — no pre-loaded conclusion."),
    }
    with open(out.replace(".jsonl", ".stats.json"), "w",
              encoding="utf-8") as f:
        json.dump(stats, f, ensure_ascii=False, indent=2)

    print(json.dumps(stats, ensure_ascii=False, indent=2))
    if contamination != 0:
        raise SystemExit("FATAL: forbidden-token contamination detected")
    if not monotone:
        raise SystemExit("FATAL: curriculum rank not monotone-sorted")
    if n_moved == 0:
        raise SystemExit("FATAL: no tier<77 records moved — ablation void")


if __name__ == "__main__":
    main()
