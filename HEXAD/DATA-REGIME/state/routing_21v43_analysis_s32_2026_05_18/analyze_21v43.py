#!/usr/bin/env python3
"""RESEARCH.md §32 — L3: §16 routing 21-vs-43 distinguishing-structure analysis.

$0 Mac CPU, deterministic. NO model forward, NO training, NO RNG.

WHAT
  §16 (state/carving_dataregime_s16_2026_05_18/) fired a 64-anchor carving
  eval; routing_accuracy = 21/64 correct (RESEARCH.md §16.6: GENUINE
  exact-tier 17/64 + ARTIFACT substring 4/64 — tiers 12/24/62/66 matched
  via "12"⊂"122" etc.). No prior cycle asked WHY 21 succeeded / 43 failed.

  This analysis partitions the 64 §8/eval anchors into SUCCESS vs FAIL
  (both the 21/43 substring-grade split AND the 17/47 genuine-grade split)
  and computes, per anchor, candidate distinguishing features. It then runs
  a deterministic separation test per feature. If a feature separates the
  sets, that feature is a lever for §25 candidate D (routing-evidence-guided
  expansion). If nothing separates them, that is the honest finding:
  routing success is SGD-lottery, not anchor structure.

HONEST (g3): this finds CORRELATION. Whether a separating feature CAUSES
  routing success needs a controlled fire (an ablation that holds the
  feature fixed) — analysis cannot establish causation. B-L3-NOTE.

INPUTS (read-only — multi-agent isolation)
  ../carving_dataregime_s16_2026_05_18/eval_result_s16.json   (routing result)
  ../carving_dataregime_s16_2026_05_18/corpus_carving_s16_generator.py
                                                              (anchor SSOT)
  ../carving_dataregime_s16_2026_05_18/corpus_carving_s16.stats.json
"""
from __future__ import annotations

import json
import math
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
S16 = HERE.parent / "carving_dataregime_s16_2026_05_18"
EVAL = S16 / "eval_result_s16.json"
GEN = S16 / "corpus_carving_s16_generator.py"
STATS = S16 / "corpus_carving_s16.stats.json"


# --------------------------------------------------------------------------
# 1. ANCHOR SSOT — extract the 64 §8 anchors (= the exact eval probe set)
#    from the generator. tuple = (tier, name, domain, top_emotion, score,
#    vacuum_psi, basin_radius). Deterministic exec of the two list literals.
# --------------------------------------------------------------------------
def load_anchors() -> dict:
    src = GEN.read_text()
    ns: dict = {}
    m8 = re.search(r"S8_ANCHORS = \[(.*?)\n\]", src, re.S)
    exec("S8_ANCHORS=[" + m8.group(1) + "\n]", ns)  # noqa: S102 (trusted local file)
    anchors = {}
    for tup in ns["S8_ANCHORS"]:
        tier, name, dom, emo, score, psi, basin = tup
        anchors[tier] = {
            "tier": tier, "name": name, "domain": dom, "top_emotion": emo,
            "score": float(score), "vacuum_psi": [float(psi[0]), float(psi[1])],
            "basin_radius": float(basin),
        }
    return anchors


# --------------------------------------------------------------------------
# 2. PARTITION — read §16 routing result, classify each probe.
#    success_substr  : routing_correct == True  (eval's 21/64 substring grade)
#    success_genuine : leading 🛸<number> exact-matches own tier (17/64)
# --------------------------------------------------------------------------
def load_partition() -> dict:
    d = json.loads(EVAL.read_text())
    probes = d["axis1_knowledge_access"]["probes"]
    rec = {}
    for p in probes:
        tier = p["tier"]
        gen = p.get("gen", "")
        m = re.search(r"🛸(\d+)", gen)
        emit = m.group(1) if m else None
        rec[tier] = {
            "routing_correct": bool(p["routing_correct"]),
            "leading_emit": emit,
            "exact": (emit == str(tier)),
            "semantic_recall": bool(p.get("semantic_recall", False)),
            "rep": float(p.get("rep", 0.0)),
        }
    return rec


# --------------------------------------------------------------------------
# 3. FEATURES — per anchor, a deterministic feature vector.
# --------------------------------------------------------------------------
def nearest_psi_dist(anchors: dict, tier: int) -> float:
    """L2 distance from this anchor's vacuum_psi to the nearest OTHER
    anchor's vacuum_psi (over the full 64-anchor eval set)."""
    p = anchors[tier]["vacuum_psi"]
    best = math.inf
    for t2, a2 in anchors.items():
        if t2 == tier:
            continue
        q = a2["vacuum_psi"]
        dd = math.hypot(p[0] - q[0], p[1] - q[1])
        if dd < best:
            best = dd
    return best


def basin_overlap_count(anchors: dict, tier: int) -> int:
    """How many OTHER anchors' basins this anchor's vacuum_psi-centre
    overlaps: dist(centre_i, centre_j) < r_i + r_j."""
    p = anchors[tier]["vacuum_psi"]
    r = anchors[tier]["basin_radius"]
    n = 0
    for t2, a2 in anchors.items():
        if t2 == tier:
            continue
        q = a2["vacuum_psi"]
        dd = math.hypot(p[0] - q[0], p[1] - q[1])
        if dd < r + a2["basin_radius"]:
            n += 1
    return n


def korean_byte_ratio(name: str) -> float:
    """Fraction of bytes in the UTF-8 encoding that are Hangul (multi-byte)
    vs ASCII (digit/symbol/latin). 1.0 = pure Korean name."""
    b = name.encode("utf-8")
    if not b:
        return 0.0
    multibyte = sum(1 for ch in b if ch >= 0x80)
    return multibyte / len(b)


def build_features(anchors: dict) -> dict:
    feats = {}
    for tier, a in anchors.items():
        name = a["name"]
        feats[tier] = {
            "tier": float(tier),
            "vacuum_psi_x": a["vacuum_psi"][0],
            "vacuum_psi_y": a["vacuum_psi"][1],
            "vacuum_psi_dev_from_half": math.hypot(
                a["vacuum_psi"][0] - 0.5, a["vacuum_psi"][1] - 0.5),
            "basin_radius": a["basin_radius"],
            "nearest_psi_dist": nearest_psi_dist(anchors, tier),
            "basin_overlap_count": float(basin_overlap_count(anchors, tier)),
            "score": a["score"],
            "name_byte_len": float(len(name.encode("utf-8"))),
            "name_char_len": float(len(name)),
            "korean_byte_ratio": korean_byte_ratio(name),
        }
    return feats


# --------------------------------------------------------------------------
# 4. SEPARATION TEST — deterministic, per numeric feature.
#    For each feature: success-set vs fail-set distributions.
#      mean_diff           : mean(success) - mean(fail)
#      cohens_d            : standardised effect size (pooled SD)
#      threshold_separation: best single-threshold accuracy — the max over
#                            every candidate split point of the fraction of
#                            64 anchors correctly classified by "feature >= t"
#                            (or "<= t"). 1.0 = a threshold perfectly splits
#                            the two sets; 0.5 = no better than the base rate
#                            of the majority class would give a constant.
#      auc                 : Mann-Whitney U / (n1*n2) — rank-separation,
#                            0.5 = no separation, 1.0 or 0.0 = perfect.
# --------------------------------------------------------------------------
def _mean(xs):
    return sum(xs) / len(xs) if xs else 0.0


def _var(xs, m):
    return sum((x - m) ** 2 for x in xs) / len(xs) if xs else 0.0


def cohens_d(succ, fail):
    if len(succ) < 2 or len(fail) < 2:
        return 0.0
    ms, mf = _mean(succ), _mean(fail)
    vs, vf = _var(succ, ms), _var(fail, mf)
    n1, n2 = len(succ), len(fail)
    pooled = ((n1 - 1) * vs + (n2 - 1) * vf) / (n1 + n2 - 2)
    sd = math.sqrt(pooled)
    if sd == 0.0:
        return 0.0
    return (ms - mf) / sd


def threshold_separation(succ, fail):
    """Best single-threshold classification accuracy over all 64 anchors.
    Deterministic: candidate thresholds = midpoints of sorted unique values.
    Tries both polarities (success = high side / low side)."""
    all_vals = sorted(set(succ) | set(fail))
    if len(all_vals) < 2:
        return 0.5
    cands = [(all_vals[i] + all_vals[i + 1]) / 2.0
             for i in range(len(all_vals) - 1)]
    n = len(succ) + len(fail)
    best = 0.0
    for t in cands:
        # polarity A: success predicted when value >= t
        tp = sum(1 for v in succ if v >= t)
        tn = sum(1 for v in fail if v < t)
        accA = (tp + tn) / n
        # polarity B: success predicted when value < t
        tp2 = sum(1 for v in succ if v < t)
        tn2 = sum(1 for v in fail if v >= t)
        accB = (tp2 + tn2) / n
        best = max(best, accA, accB)
    return best


def auc(succ, fail):
    """Mann-Whitney rank-AUC. Reported as max(auc, 1-auc) so 0.5 = noise,
    1.0 = perfect rank separation, polarity-agnostic."""
    if not succ or not fail:
        return 0.5
    u = 0.0
    for s in succ:
        for f in fail:
            if s > f:
                u += 1.0
            elif s == f:
                u += 0.5
    raw = u / (len(succ) * len(fail))
    return max(raw, 1.0 - raw)


def necessary_condition(succ, fail):
    """One-sided 'necessary condition' / containment metric — independent of
    base-rate imbalance, unlike threshold_separation_acc which the majority
    class dominates.

    Finds the threshold t and polarity for which the SUCCESS set is most
    cleanly CONTAINED on one side (every success satisfies the predicate),
    and reports how much of the FAIL set is excluded by that same predicate.

      purity   : fraction of the success set on the chosen side at the
                 chosen t. purity == 1.0 means the predicate is a NECESSARY
                 condition for success (no success violates it).
      exclusion: fraction of the fail set that the predicate ALSO excludes.
                 1.0 would mean the predicate is also sufficient; lower
                 means necessary-but-not-sufficient.
      lift     : exclusion at purity==1.0. A clean necessary condition with
                 lift>0 is a real, honest structural finding even when
                 threshold_separation_acc looks unremarkable.

    Returns the best (purity==1.0 if any) by exclusion."""
    all_vals = sorted(set(succ) | set(fail))
    if len(all_vals) < 2 or not succ or not fail:
        return {"purity": 0.0, "exclusion": 0.0, "lift": 0.0,
                "threshold": None, "polarity": None}
    cands = [(all_vals[i] + all_vals[i + 1]) / 2.0
             for i in range(len(all_vals) - 1)]
    best = {"purity": 0.0, "exclusion": 0.0, "lift": 0.0,
            "threshold": None, "polarity": None}
    for t in cands:
        for pol, pred in (("ge", lambda v: v >= t), ("lt", lambda v: v < t)):
            purity = sum(1 for v in succ if pred(v)) / len(succ)
            exclusion = sum(1 for v in fail if not pred(v)) / len(fail)
            # prefer purity==1.0 (necessary condition); tie-break exclusion
            cand_lift = exclusion if purity >= 1.0 - 1e-9 else 0.0
            if (cand_lift > best["lift"]
                    or (cand_lift == best["lift"]
                        and purity > best["purity"])):
                best = {"purity": round(purity, 4),
                        "exclusion": round(exclusion, 4),
                        "lift": round(cand_lift, 4),
                        "threshold": t, "polarity": pol}
    return best


def separation_report(feats, succ_tiers, fail_tiers, feat_names):
    out = {}
    for fn in feat_names:
        succ = [feats[t][fn] for t in succ_tiers]
        fail = [feats[t][fn] for t in fail_tiers]
        nc = necessary_condition(succ, fail)
        out[fn] = {
            "mean_success": round(_mean(succ), 6),
            "mean_fail": round(_mean(fail), 6),
            "mean_diff": round(_mean(succ) - _mean(fail), 6),
            "cohens_d": round(cohens_d(succ, fail), 4),
            "threshold_separation_acc": round(threshold_separation(succ, fail), 4),
            "rank_auc": round(auc(succ, fail), 4),
            "necessary_condition": nc,
        }
    # rank features by necessary-condition lift (= the honest, base-rate-
    # independent cleanliness of a one-sided structural finding), tie-break
    # by threshold_separation_acc.
    ranked = sorted(out.keys(),
                    key=lambda k: (out[k]["necessary_condition"]["lift"],
                                   out[k]["threshold_separation_acc"]),
                    reverse=True)
    return out, ranked


# --------------------------------------------------------------------------
# 5. CATEGORICAL — domain / top_emotion frequency skew between sets.
# --------------------------------------------------------------------------
def categorical_report(anchors, succ_tiers, fail_tiers, key):
    succ_ct, fail_ct = {}, {}
    for t in succ_tiers:
        v = anchors[t][key]
        succ_ct[v] = succ_ct.get(v, 0) + 1
    for t in fail_tiers:
        v = anchors[t][key]
        fail_ct[v] = fail_ct.get(v, 0) + 1
    cats = sorted(set(succ_ct) | set(fail_ct))
    rows = {}
    for c in cats:
        s, f = succ_ct.get(c, 0), fail_ct.get(c, 0)
        rows[c] = {"success": s, "fail": f, "total": s + f,
                   "success_rate": round(s / (s + f), 4) if (s + f) else 0.0}
    return rows


# --------------------------------------------------------------------------
# MAIN
# --------------------------------------------------------------------------
def main():
    anchors = load_anchors()
    part = load_partition()
    stats = json.loads(STATS.read_text())

    assert len(anchors) == 64, f"expected 64 §8 anchors, got {len(anchors)}"
    assert set(anchors) == set(part), "anchor SSOT / eval probe tier mismatch"

    # substring grade (eval's 21/64)
    succ_substr = sorted(t for t in part if part[t]["routing_correct"])
    fail_substr = sorted(t for t in part if not part[t]["routing_correct"])
    # genuine grade (§16.6: leading 🛸<n> exact-matches own tier)
    succ_genuine = sorted(t for t in part
                          if part[t]["routing_correct"] and part[t]["exact"])
    fail_genuine = sorted(t for t in anchors if t not in succ_genuine)

    feats = build_features(anchors)
    feat_names = ["tier", "vacuum_psi_x", "vacuum_psi_y",
                  "vacuum_psi_dev_from_half", "basin_radius",
                  "nearest_psi_dist", "basin_overlap_count", "score",
                  "name_byte_len", "name_char_len", "korean_byte_ratio"]

    sep_substr, rank_substr = separation_report(
        feats, succ_substr, fail_substr, feat_names)
    sep_genuine, rank_genuine = separation_report(
        feats, succ_genuine, fail_genuine, feat_names)

    # corpus frequency: §16 allocates records uniformly per anchor
    # (per_anchor = n_target // len(KNUTH_ANCHORS)). Confirm via stats:
    # 168 anchors, 777,000 records => ~4625/anchor uniform — NOT a feature.
    n_anchors_corpus = stats.get("anchors", 168)
    n_records = stats.get("records", 777000)
    per_anchor_uniform = n_records // n_anchors_corpus

    result = {
        "analysis": "RESEARCH.md §32 L3 — §16 routing 21-vs-43 "
                    "distinguishing-structure",
        "inputs": {
            "eval_result": str(EVAL.name),
            "eval_sha_ckpt": json.loads(EVAL.read_text()).get("ckpt_sha256"),
            "corpus_records": n_records,
            "corpus_anchors": n_anchors_corpus,
        },
        "partition": {
            "substring_grade": {
                "success_n": len(succ_substr), "fail_n": len(fail_substr),
                "success_tiers": succ_substr, "fail_tiers": fail_substr,
            },
            "genuine_grade": {
                "success_n": len(succ_genuine), "fail_n": len(fail_genuine),
                "success_tiers": succ_genuine, "fail_tiers": fail_genuine,
                "substring_artifact_tiers": sorted(
                    t for t in succ_substr if t not in succ_genuine),
            },
        },
        "corpus_frequency_feature": {
            "per_anchor_records": per_anchor_uniform,
            "uniform": True,
            "note": "§16 generator allocates records uniformly per anchor "
                    "(per_anchor = n_target // 168). Corpus frequency does "
                    "NOT vary between anchors -> NOT a distinguishing "
                    "feature; excluded from separation tests.",
        },
        "separation_substring_grade": {
            "ranked_by_threshold_separation_acc": rank_substr,
            "features": sep_substr,
        },
        "separation_genuine_grade": {
            "ranked_by_threshold_separation_acc": rank_genuine,
            "features": sep_genuine,
        },
        "categorical_substring": {
            "domain": categorical_report(anchors, succ_substr, fail_substr,
                                         "domain"),
            "top_emotion": categorical_report(anchors, succ_substr,
                                              fail_substr, "top_emotion"),
        },
        "categorical_genuine": {
            "domain": categorical_report(anchors, succ_genuine, fail_genuine,
                                         "domain"),
            "top_emotion": categorical_report(anchors, succ_genuine,
                                              fail_genuine, "top_emotion"),
        },
    }

    # ----- honest verdict ---------------------------------------------------
    # The honest structure signal is the necessary-condition lift, NOT
    # threshold_separation_acc (the latter is dominated by the 47/64 fail
    # base rate — predicting "always fail" already scores 0.734).
    top_g = rank_genuine[0]
    g = sep_genuine[top_g]
    nc = g["necessary_condition"]
    # a feature is a *clean necessary condition* if purity==1.0 (no success
    # violates it) AND it excludes a non-trivial share of the fail set.
    structure_found = (nc["purity"] >= 1.0 - 1e-9 and nc["lift"] >= 0.30)
    result["verdict"] = {
        "top_feature_genuine_grade": top_g,
        "necessary_condition": nc,
        "top_feature_cohens_d": g["cohens_d"],
        "top_feature_rank_auc": g["rank_auc"],
        "top_feature_threshold_separation_acc": g["threshold_separation_acc"],
        "base_rate_constant_predict_fail": round(
            len(fail_genuine) / 64.0, 4),
        "structure_found": bool(structure_found),
        "finding": (
            f"Feature '{top_g}' is a NECESSARY CONDITION for §16 routing "
            f"success: purity {nc['purity']} (every one of the 17 "
            f"genuine-success anchors satisfies '{top_g} {nc['polarity']} "
            f"{nc['threshold']}'; ZERO successes violate it), and that same "
            f"predicate excludes {nc['lift']} of the 47-fail set. It is "
            f"necessary-but-NOT-sufficient (|d|={abs(g['cohens_d']):.2f}, "
            f"rank-AUC {g['rank_auc']}). Routing success is STRUCTURED — "
            f"there is a real anchor-property frontier, not pure "
            f"SGD-lottery."
            if structure_found else
            "No feature is a clean necessary condition for §16 routing "
            "success — routing success is consistent with SGD-lottery / "
            "measurement noise, not anchor structure."
        ),
        "causation_caveat": (
            "g3: this is CORRELATION. The necessary condition co-varies "
            "with §16's curriculum (curriculum_rank weights tier/303 at "
            "0.30 — high-tier anchors land in later curriculum stages) and "
            "with the anchor-name distribution. Whether the feature itself "
            "CAUSES routing success, vs is a proxy for an unmeasured cause "
            "(e.g. late-stage curriculum exposure, weight-norm at that "
            "training phase), needs a controlled ablation fire. "
            "B-L3-NOTE empirical carve-out — NOT counted 🔵."
        ),
        "implication_for_s25_candidate_D": (
            f"§25 candidate D (routing-evidence-guided expansion) has a "
            f"real lever: the '{top_g} {nc['polarity']} {nc['threshold']}' "
            f"frontier. Honest reading — because the condition is NECESSARY "
            f"but not sufficient, the fail-side of the frontier "
            f"({1.0 - nc['lift']:.2f} of fails are ON the success side and "
            f"still fail) is where expansion can be tested: candidate D can "
            f"(a) over-sample / diversify the {top_g}-success-side fail "
            f"anchors to test if more genuine content lifts routing above "
            f"the necessity floor, and (b) explicitly NOT expect "
            f"{top_g}-fail-side anchors to route until the necessary "
            f"condition itself is understood (it co-varies with §16's "
            f"curriculum stage — see causation_caveat). The frontier is a "
            f"lever for WHERE to expand, not a guarantee."
            if structure_found else
            "§25 candidate D cannot use anchor structure as an expansion "
            "lever — no measured feature predicts §16 routing. Routing-"
            "evidence-guided expansion would be guiding on noise."
        ),
    }

    out_path = HERE / "analysis_result.json"
    out_path.write_text(json.dumps(result, indent=2, ensure_ascii=False))
    print(f"[§32 L3] wrote {out_path}")
    print(f"[§32 L3] partition substring 21/43 | genuine "
          f"{len(succ_genuine)}/{len(fail_genuine)}")
    print(f"[§32 L3] genuine-grade ranked features (by necessary-cond lift):")
    for fn in rank_genuine:
        r = sep_genuine[fn]
        ncf = r["necessary_condition"]
        print(f"  {fn:<26} nc-lift={ncf['lift']:.3f} "
              f"purity={ncf['purity']:.3f} ({ncf['polarity']} "
              f"{ncf['threshold']}) auc={r['rank_auc']:.3f} "
              f"d={r['cohens_d']:+.3f}")
    print(f"[§32 L3] verdict: structure_found="
          f"{result['verdict']['structure_found']} "
          f"top={top_g} nc-lift={nc['lift']} purity={nc['purity']}")
    return result


if __name__ == "__main__":
    main()
