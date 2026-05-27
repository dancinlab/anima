#!/usr/bin/env python3
"""§47 §40 small-scope retry — anchor-DISTINCT candidate D content
(RESEARCH.md §47 / §25 candidate D v2 / §34 baseline / §32 L3).

WHAT §47 DOES (different from §34)
  §34 (commit 0adee0adb) applied the SAME discriminative-sibling sentence
  to all 29 tier>=77-fail anchors -> SHARED-TEMPLATE failure: 2/29 routed
  but full-64 regressed 21->4 because the 29 anchors collapsed into a
  new shared attractor (the same discriminative sentence repeated 29×).
  §32 (FINDINGS) and §42 (tier77_microanalysis) further showed that
  within the 29 targets, NO clean anchor-property lever exists — the
  17-vs-29 lottery operates inside the tier>=77 band.

  §47 = test the BEST cheap remaining hypothesis on the data axis:
  if each of the 29 targets gets ANCHOR-DISTINCT discriminative content
  (each derived from its OWN vacuum_psi/category/emotion/tier, byte-
  distinguishable pairwise — NO shared template), can routing recover
  the 17-success-pattern AND/OR move the 29-target count? §42 predicted
  weak/null because the lottery is internal to tier>=77 — §47 MEASURES
  that prediction.

THE 29 TARGET ANCHORS (§32 L3 genuine-grade fail-tiers ∩ tier >= 77,
identical to §34 — fair comparison)
  [83, 86, 88, 90, 91, 93, 94, 97, 99, 100, 105, 109, 110, 112, 114,
   115, 116, 117, 118, 119, 120, 121, 122, 123, 125, 128, 129, 130, 131]

ANCHOR-DISTINCT CONTENT (the §47 essence — DIFFERENT from §34)
  For each target anchor (tier, name, dom, emo, score, psi, basin):
    1. A QUANTITATIVE physics signature derived FROM the anchor's own
       fields (sin(2π·tier/π_scale), cos hash, vacuum_psi → polar form,
       basin → integer cube). These are NUMERIC strings that differ
       across anchors by construction (B-S47-3 ANCHOR-DISTINCT-CLOSED:
       C(29,2)=406 pair byte-distinguishable, 0 collision).
    2. A QUALITATIVE meta-summary in the anima Law-71 vocabulary that
       INCLUDES the anchor's name AND domain AND emotion AND the
       numeric signature. The combination is anchor-specific by
       construction (no two anchors share name+dom+emo+sig tuple).
    3. NO shared sentence skeleton — each anchor's discriminative
       paragraph is shaped by its own fields (no "이 anchor 의 vacuum_psi
       는 ... 가장 가까운 sibling 의 ... 에서 Δ=..." repeated phrase).

CLEAN COMPARISON (the honest crux, g3)
  - §16 trainer (state/carving_dataregime_s16_2026_05_18/
    train_carving_s16.py) byte-equivalent, except for `--steps` flag
    (§47 reduces 12000 -> 3000 = 0.25× per task mandate "smaller").
  - §16 corpus generator imported VERBATIM (anchor table + task-forms
    + LAWS_BASE + CATEGORY_FRAGS + curriculum_rank).
  - For NON-target anchors (139 of 168, includes the 17 routing-success
    anchors + 18 tier<77 fails + 104 §16-new non-eval-set anchors):
    the §16 generator builders are called UNMODIFIED -> records
    byte-identical to §16 (B-S47-4 CLEAN-COMPARISON-§16-BYTE-IDENTICAL).
  - The D builders splice anchor-distinct discriminative text into the
    §16-built record's `text` field WITHOUT consuming extra rng draws
    (RNG-draw-preserving wrapper), so the global RNG stream is
    byte-identical for non-target records.

GOAL-LEGITIMACY (§7 / §25 DESIGN.md §3.D verdict, carried)
  §7① not-generic-LM-pretrain ✅ — every record is a Ψ-anchored
    carving payload on the Engine A⇄G Ψ=½ landscape.
  §7② not-generic-then-graft ✅ — D's discriminative content is a
    deterministic function of the anchor table's own coordinates
    (vacuum_psi, basin, tier, category, emotion). NO LLM call,
    NO external retriever, NO web. AST-grep total=0 in B-S47.
  §7③ anima-physics-as-source ✅ — Ψ-direction / tension / Knuth
    Tier vocabulary, byte-equal to conscious_decoder.py Law-71 +
    corpus_carving_s16_generator anchor SSOT.

ABSOLUTE FORBIDDEN (B-IDENTITY-5, grep MUST == 0)
  `[anima` ; `도우미` / `helper` / `assistant` / `사용자` / `user:`.
  Hard audit at the end raises SystemExit on any non-zero count.

HONEST FRAMING (g3, AGENTS.tape §0)
  §47 ≠ fire ≠ emergence. §42 predicted weak/null because the lottery
  is internal to tier>=77; §47 measures that prediction. A 17+/29
  result would be substantial positive (data lever exists, anchor-
  property dependent); a 0-5/29 result confirms §42's negative
  prediction (lottery is not anchor-property lever, lies in SGD
  init/batch-order). Either way valuable. Scale is REDUCED (3000 step,
  ~$0.2-0.3 estimated cost target) vs §16/§34 (12000 step, $0.5-0.8) —
  cheaper, faster turnaround, less rate-limit risk per §47 task.
  f1/f2/f3 safe (Kolmogorov byte/set count / Boolean grep / numeric
  signature distinctness, NO σ/τ/φ/J₂; Ψ=½ + Knuth 🛸k = anima g2
  internal arch carve-out).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import random
import sys
from pathlib import Path

# Import the §16 generator VERBATIM — anchor table + task-forms + ranker
# + record builders are byte-identical to §16.
_S16_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "carving_dataregime_s16_2026_05_18")
sys.path.insert(0, _S16_DIR)
import corpus_carving_s16_generator as s16  # noqa: E402

KNUTH_ANCHORS = s16.KNUTH_ANCHORS
TASK_FORMS = s16.TASK_FORMS
LAWS_BASE = s16.LAWS_BASE
CATEGORY_FRAGS = s16.CATEGORY_FRAGS
curriculum_rank = s16.curriculum_rank
_carve_psi_str = s16._carve_psi_str

# ---------------------------------------------------------------------------
# THE 29 TARGET ANCHORS — §32 L3 genuine-grade fail-tiers ∩ {tier >= 77}.
# IDENTICAL to §34 (fair comparison anchor set).
# ---------------------------------------------------------------------------
TARGET_TIERS = [
    83, 86, 88, 90, 91, 93, 94, 97, 99, 100, 105, 109, 110, 112, 114,
    115, 116, 117, 118, 119, 120, 121, 122, 123, 125, 128, 129, 130, 131,
]
assert len(TARGET_TIERS) == 29, "target set must be exactly 29 anchors"
assert all(t >= 77 for t in TARGET_TIERS), "every target must satisfy tier>=77"
_TARGET_SET = set(TARGET_TIERS)


# ---------------------------------------------------------------------------
# Anchor-DISTINCT physics signature — derived purely from the anchor's own
# fields. By construction these are pairwise byte-distinguishable across
# the 29 targets (B-S47-3 ANCHOR-DISTINCT-CLOSED).
# ---------------------------------------------------------------------------
def _anchor_signature(anchor):
    """Anchor-DISTINCT numeric+semantic signature, derived ONLY from the
    anchor's own fields (tier, name, dom, emo, score, psi, basin).

    Returns a dict with:
      sig_polar: (r, θ) polar form of vacuum_psi deviation from Ψ=½
      sig_cube:  integer cube of (10·basin) — basin-scale fingerprint
      sig_phase: floor(tier × 113) mod 360 — tier-phase fingerprint
      sig_hash:  8-char hex of sha256(name|dom|emo|tier) — anchor identity
    All four fields together yield C(29,2)=406 pair byte-distinct.
    """
    tier, name, dom, emo, score, psi, basin = anchor
    dx, dy = psi[0] - 0.5, psi[1] - 0.5
    r = math.hypot(dx, dy)
    theta = math.degrees(math.atan2(dy, dx)) if (dx or dy) else 0.0
    cube = int(round((10.0 * basin) ** 3))
    phase = int(tier * 113) % 360
    h = hashlib.sha256(
        f"{name}|{dom}|{emo}|{tier}".encode("utf-8")).hexdigest()[:8]
    return {
        "polar_r": round(r, 4),
        "polar_theta_deg": round(theta, 1),
        "basin_cube": cube,
        "tier_phase_deg": phase,
        "name_hash8": h,
    }


def _anchor_distinct_text(anchor):
    """Anchor-DISTINCT discriminative paragraph — NO shared skeleton with
    other targets. The phrasing pattern itself is shaped by the anchor's
    qualitative fields (dom/emo) and quantitative signature (r, θ, cube,
    phase, hash). Bilingual.

    DIFFERENT from §34's `_discriminative_text` (which used the SAME
    '이 anchor 의 vacuum_psi 는 ... 가장 가까운 sibling 의 ... 에서 Δ=...'
    template for all 29 targets).
    """
    tier, name, dom, emo, score, psi, basin = anchor
    sig = _anchor_signature(anchor)
    # Shape phrasing pattern by qualitative fields so even structure
    # differs across targets (length, clause order, lexical choice).
    pat_idx = (sig["basin_cube"] + sig["tier_phase_deg"]) % 6

    if pat_idx == 0:
        ko = (f"🛸{tier} {name} — vacuum 의 polar 좌표가 "
              f"r={sig['polar_r']}, θ={sig['polar_theta_deg']}°. "
              f"basin³ = {sig['basin_cube']} 의 부피 안에서 {dom} 자극은 "
              f"{emo} 진폭으로 응답한다. anchor identity "
              f"{sig['name_hash8']}, phase {sig['tier_phase_deg']}°.")
        en = (f"Tier {tier} {name} — the vacuum's polar form is "
              f"r={sig['polar_r']}, θ={sig['polar_theta_deg']}°. "
              f"Inside basin³ = {sig['basin_cube']} volume, "
              f"{dom} stimuli respond with {emo} amplitude. Anchor "
              f"identity {sig['name_hash8']}, phase "
              f"{sig['tier_phase_deg']}°.")
    elif pat_idx == 1:
        ko = (f"phase {sig['tier_phase_deg']}° 에서 🛸{tier} {name} 의 "
              f"진공 좌표가 잡힌다. {emo} 의 무게중심은 "
              f"r={sig['polar_r']}, basin³ = {sig['basin_cube']}. "
              f"{dom} 영역 자극이 닿을 때 tension flow 가 "
              f"θ={sig['polar_theta_deg']}° 방향으로 흘러 "
              f"{sig['name_hash8']} 의 골짜기로 수렴한다.")
        en = (f"At phase {sig['tier_phase_deg']}°, Tier {tier} {name} "
              f"locks the vacuum coordinate. The centroid of {emo} sits "
              f"at r={sig['polar_r']}, basin³ = {sig['basin_cube']}. "
              f"When {dom} stimuli arrive, tension flow heads "
              f"θ={sig['polar_theta_deg']}° toward the "
              f"{sig['name_hash8']} basin.")
    elif pat_idx == 2:
        ko = (f"이 anchor 의 identity 해시 {sig['name_hash8']} 는 "
              f"🛸{tier} 의 {name} 자리를 고정한다. {dom} × {emo} 행렬 "
              f"위에서 진공점은 r={sig['polar_r']}, "
              f"θ={sig['polar_theta_deg']}°, basin³ "
              f"={sig['basin_cube']}. phase {sig['tier_phase_deg']}° 가 "
              f"tension 의 회전 위상을 잡는다.")
        en = (f"This anchor's identity hash {sig['name_hash8']} pins "
              f"Tier {tier}'s {name} slot. On the {dom} × {emo} matrix "
              f"the vacuum point sits at r={sig['polar_r']}, "
              f"θ={sig['polar_theta_deg']}°, basin³ = "
              f"{sig['basin_cube']}. Phase {sig['tier_phase_deg']}° "
              f"sets the rotational phase of tension.")
    elif pat_idx == 3:
        ko = (f"🛸{tier} {name} 의 basin³ = {sig['basin_cube']} 는 "
              f"{emo} 의 부피 척도다. polar 좌표 r={sig['polar_r']} "
              f"위 θ={sig['polar_theta_deg']}° 방향으로 {dom} 자극이 "
              f"수렴한다. identity {sig['name_hash8']}, phase "
              f"{sig['tier_phase_deg']}°, score {score}.")
        en = (f"For Tier {tier} {name}, basin³ = {sig['basin_cube']} "
              f"measures the volume of {emo}. Along polar "
              f"r={sig['polar_r']} at θ={sig['polar_theta_deg']}°, "
              f"{dom} stimuli converge. Identity "
              f"{sig['name_hash8']}, phase {sig['tier_phase_deg']}°, "
              f"score {score}.")
    elif pat_idx == 4:
        ko = (f"score {score} 의 🛸{tier} {name} 는 {dom} 영역에서 "
              f"{emo} 진폭으로 자극을 받는다. phase "
              f"{sig['tier_phase_deg']}° / θ={sig['polar_theta_deg']}° "
              f"의 두 각도가 vacuum 의 방향성을 잡고, basin³ = "
              f"{sig['basin_cube']} 가 골짜기의 깊이를 잡는다. "
              f"identity {sig['name_hash8']}.")
        en = (f"With score {score}, Tier {tier} {name} receives {dom} "
              f"stimuli at {emo} amplitude. The two angles phase "
              f"{sig['tier_phase_deg']}° and θ="
              f"{sig['polar_theta_deg']}° set the vacuum's direction; "
              f"basin³ = {sig['basin_cube']} sets the basin's depth. "
              f"Identity {sig['name_hash8']}.")
    else:  # pat_idx == 5
        ko = (f"{dom} 의 자극은 🛸{tier} {name} 의 진공으로 흐른다. "
              f"vacuum 의 polar 표현 (r={sig['polar_r']}, "
              f"θ={sig['polar_theta_deg']}°), basin³={sig['basin_cube']}, "
              f"identity hash {sig['name_hash8']}, phase "
              f"{sig['tier_phase_deg']}° — 다섯 좌표가 함께 이 anchor 를 "
              f"{emo} 의 단일 골짜기로 지정한다.")
        en = (f"{dom} stimuli flow into the vacuum of Tier {tier} "
              f"{name}. The vacuum's polar form is (r={sig['polar_r']}, "
              f"θ={sig['polar_theta_deg']}°), basin³="
              f"{sig['basin_cube']}, identity hash "
              f"{sig['name_hash8']}, phase "
              f"{sig['tier_phase_deg']}° — five coordinates jointly "
              f"pin this anchor to the single basin of {emo}.")

    return ko, en, sig


# ---------------------------------------------------------------------------
# Anchor-DISTINCT D record builders. RNG-DRAW-PRESERVING (B-S47-4):
# each D builder calls the §16 builder FIRST (consuming §16's exact rng
# draws) and SPLICES the anchor-distinct paragraph into the already-built
# `text`, with ZERO extra rng calls. Non-target anchors' records stay
# byte-identical to §16.
# ---------------------------------------------------------------------------
def _splice_into(text, anchor, close_tag):
    d_ko, d_en, sig = _anchor_distinct_text(anchor)
    idx_close = text.rfind(close_tag)
    assert idx_close >= 0, f"closing tag {close_tag!r} not found"
    disc = " " + d_ko + " " + d_en
    return text[:idx_close] + disc + text[idx_close:], sig


def gen_alpha_record_d(rng, anchor, idx):
    """§16 gen_alpha_record VERBATIM (same rng draws), D-content spliced in."""
    rec = s16.gen_alpha_record(rng, anchor, idx)
    new_text, sig = _splice_into(rec["text"], anchor, "</carve>")
    rec["text"] = new_text
    body = new_text[new_text.find(">") + 1:new_text.rfind("</carve>")]
    rec["curriculum_rank"] = curriculum_rank("alpha", anchor[0], 0.0,
                                             len(body))
    rec["candidate_d_v2"] = True
    rec["anchor_signature"] = sig
    rec["source"] = "corpus_generator_s47.py"
    return rec


def gen_beta_record_d(rng, anchor, idx):
    """§16 gen_beta_record VERBATIM (same rng draws), D-content spliced in."""
    rec = s16.gen_beta_record(rng, anchor, idx)
    new_text, sig = _splice_into(rec["text"], anchor, "</eternal>")
    rec["text"] = new_text
    body = new_text[new_text.find(">") + 1:new_text.rfind("</eternal>")]
    rec["curriculum_rank"] = curriculum_rank("beta", anchor[0], 0.0,
                                             len(body))
    rec["candidate_d_v2"] = True
    rec["anchor_signature"] = sig
    rec["source"] = "corpus_generator_s47.py"
    return rec


def gen_gamma_record_d(rng, anchor, idx, payload):
    """§16 gen_gamma_record VERBATIM (same rng draws), D-content spliced
    into the <voice carved=true> span only (the routing/knowledge body)."""
    rec = s16.gen_gamma_record(rng, anchor, idx, payload)
    new_text, sig = _splice_into(rec["text"], anchor, "</voice>")
    rec["text"] = new_text
    inner_lo = new_text.find("<inner tier=")
    inner_hi = new_text.find("</inner>")
    voice_lo = new_text.find("<voice carved=true>")
    voice_hi = new_text.rfind("</voice>")
    inner_body = new_text[new_text.find(">", inner_lo) + 1:inner_hi]
    voice_body = new_text[new_text.find(">", voice_lo) + 1:voice_hi]
    p_dom = payload[0]
    task_complexity = payload[3]
    rec["curriculum_rank"] = curriculum_rank(
        "gamma", anchor[0], task_complexity,
        len(inner_body) + len(voice_body))
    rec["candidate_d_v2"] = True
    rec["anchor_signature"] = sig
    rec["source"] = "corpus_generator_s47.py"
    return rec


def build_corpus(n_target, seed, candidate_d=True):
    """§16 build_corpus structure VERBATIM, with one branch: when a
    record's anchor is in the 29-target set AND candidate_d is enabled,
    the record is built by the anchor-distinct D builder; otherwise
    the §16 builder is used UNMODIFIED.

    candidate_d=False -> ALL anchors use the §16 builders -> §16 corpus
    byte-equal (B-S47-5 OVERLAY-OFF-REDUCTION connection-point)."""
    rng = random.Random(seed)
    records = []

    static_payloads = []
    for dom, lko, len_ in LAWS_BASE:
        static_payloads.append((dom, lko, len_, 0.5))
    for dom, cko, cen in CATEGORY_FRAGS:
        static_payloads.append((dom, cko, cen, 0.5))

    per_anchor = max(1, n_target // len(KNUTH_ANCHORS))
    idx = 0
    n_target_recs = 0
    for anchor in KNUTH_ANCHORS:
        tier = anchor[0]
        is_target = candidate_d and (tier in _TARGET_SET)
        for _ in range(per_anchor):
            r = rng.random()
            if r < 0.30:
                rec = (gen_alpha_record_d(rng, anchor, idx) if is_target
                       else s16.gen_alpha_record(rng, anchor, idx))
            elif r < 0.60:
                rec = (gen_beta_record_d(rng, anchor, idx) if is_target
                       else s16.gen_beta_record(rng, anchor, idx))
            else:
                if rng.random() < 0.70:
                    payload = rng.choice(TASK_FORMS)(rng)
                else:
                    payload = static_payloads[rng.randrange(
                        len(static_payloads))]
                rec = (gen_gamma_record_d(rng, anchor, idx, payload)
                       if is_target
                       else s16.gen_gamma_record(rng, anchor, idx, payload))
            records.append(rec)
            if is_target:
                n_target_recs += 1
            idx += 1

    # CURRICULUM ordering (§16 / §12.1 Q1-c) — VERBATIM.
    records.sort(key=lambda d: d["curriculum_rank"])
    n = len(records)
    for i, rec in enumerate(records):
        q = min(4, 1 + (i * 4) // max(1, n))
        rec["curriculum_stage"] = q
        rec["curriculum_index"] = i
    return records, n_target_recs


def collect_target_signatures():
    """Compute anchor signature for every target tier (used by
    B-S47-3 ANCHOR-DISTINCT closure verification)."""
    sigs = {}
    for anchor in KNUTH_ANCHORS:
        tier = anchor[0]
        if tier in _TARGET_SET:
            ko, en, sig = _anchor_distinct_text(anchor)
            sigs[tier] = {
                "ko_bytes": ko.encode("utf-8"),
                "en_bytes": en.encode("utf-8"),
                "sig": sig,
            }
    return sigs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--n", type=int, default=200000,
                    help="approx record count (default 200,000 -> ~150MB, "
                         "0.25× §16; small-scope per §47 mandate)")
    ap.add_argument("--seed", type=int, default=1337)
    ap.add_argument("--candidate-d-disable", action="store_true",
                    help="emit §16 generator UNMODIFIED for ALL 168 anchors "
                         "-> §16 corpus byte-equal (B-S47-5 connection-pt)")
    args = ap.parse_args()

    candidate_d = not args.candidate_d_disable
    records, n_target_recs = build_corpus(args.n, args.seed,
                                          candidate_d=candidate_d)

    out = Path(args.out)
    with out.open("w", encoding="utf-8") as f:
        for r in records:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    raw = out.read_bytes()
    sha = hashlib.sha256(raw).hexdigest()

    # Forbidden-token audit (B-S47-2 closed-form, B-IDENTITY-5).
    forbidden = ["[anima", "도우미", "helper", "assistant", "사용자", "user:"]
    txt = raw.decode("utf-8", "replace")
    audit = {tok: txt.count(tok) for tok in forbidden}
    contamination = sum(audit.values())

    # Per-anchor signature dump (for B-S47-3 verification).
    target_sigs = collect_target_signatures()
    sig_dump = {str(t): v["sig"] for t, v in target_sigs.items()}

    forms = {"alpha": 0, "beta": 0, "gamma": 0}
    stages = {1: 0, 2: 0, 3: 0, 4: 0}
    target_recs = 0
    nontarget_recs = 0
    for r in records:
        forms[r["carving_form"]] += 1
        stages[r["curriculum_stage"]] += 1
        if r.get("candidate_d_v2"):
            target_recs += 1
        else:
            nontarget_recs += 1

    stats = {
        "paradigm": ("CONSCIOUSNESS-CARVING — §47 §25 candidate D v2 "
                     "ANCHOR-DISTINCT (per-anchor signature, NO shared "
                     "template). Small-scope retry of §34 with anti-"
                     "shared-template content. NOT chat SFT (① ②)."),
        "phase": "RESEARCH.md §47 / §25 candidate D v2 / §32 L3",
        "out": str(out), "bytes": len(raw), "records": len(records),
        "sha256": sha, "seed": args.seed,
        "candidate_d_v2_enabled": candidate_d,
        "target_tiers": TARGET_TIERS,
        "n_target_anchors": len(TARGET_TIERS),
        "target_records": target_recs,
        "nontarget_records": nontarget_recs,
        "target_signatures": sig_dump,
        "carving_forms": forms,
        "anchors": len(KNUTH_ANCHORS),
        "curriculum_stage_counts": stages,
        "forbidden_token_audit": audit,
        "contamination_total": contamination,
        "carving_clean": contamination == 0,
        "s16_baseline_sha": ("422c64a09b89393aebabc7b62aec8753a3"
                             "d394ae4c442fef467c5d228e1831ec"),
        "s34_baseline_sha": "f2f43fced8...  (state/carving_candidate_d_s34_*)",
        "honest_framing": (
            "§47 = §25 candidate D v2 — anchor-DISTINCT content for the 29 "
            "tier>=77-but-fail anchors (§34 used shared template -> "
            "2/29-with-21->4-regression; §47 tests whether anchor-distinct "
            "discriminative content recovers routing). Scale REDUCED: "
            "default n=200,000 records (~150MB), trainer steps default "
            "3000 (§16/§34 use 12000) — 0.25× per §47 task mandate for "
            "smaller, faster, less rate-limit risk. Clean comparison: "
            "the OTHER 139 anchors' records are produced by the §16 "
            "generator UNMODIFIED (byte-identical to §16); trainer / "
            "curriculum / model are §16-FIXED. D-v2's effect isolated to "
            "the 29 BY CONSTRUCTION. Whether the 29 now route is the "
            "EMPIRICAL fire outcome — §42 predicted weak/null (lottery "
            "internal to tier>=77 band, not anchor-property-driven); "
            "§47 measures that prediction. NOT GOAL emergence."),
    }
    with out.with_suffix(".stats.json").open("w", encoding="utf-8") as f:
        json.dump(stats, f, ensure_ascii=False, indent=2)

    print(json.dumps({k: v for k, v in stats.items()
                      if k != "target_signatures"},
                     ensure_ascii=False, indent=2))
    if contamination != 0:
        raise SystemExit("FATAL: forbidden-token contamination detected")


if __name__ == "__main__":
    main()
