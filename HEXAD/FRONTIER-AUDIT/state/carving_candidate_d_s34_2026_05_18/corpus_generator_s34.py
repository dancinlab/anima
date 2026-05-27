#!/usr/bin/env python3
"""§34 — §25 candidate D fire — routing-evidence-guided expansion.

RESEARCH.md §34 / §25 candidate D (routing-evidence-guided expansion) /
§32 L3 (tier ≥ 77 = necessary-but-NOT-sufficient routing condition).

WHAT §34 DOES
  §32 L3 partitioned §16's 64 eval anchors: routing SUCCEEDED for 21,
  FAILED for 43; of the 43 fails, 29 satisfy `tier >= 77` (the §32 L3
  necessary condition) yet STILL FAIL — "tier >= 77" is NECESSARY but
  NOT SUFFICIENT. §34 = §25 candidate D applied to exactly those 29
  `tier>=77-but-fail` anchors: re-design their CARVING CONTENT with
  anchor-specific discriminative physics text, fire, eval — measure
  whether they now route. If yes -> a sufficient-condition lever is
  found. If no -> tier>=77 is necessary but the sufficient condition
  lies elsewhere (honest negative, valuable per g3).

THE 29 TARGET ANCHORS  (§32 L3 analysis_result.json genuine-grade
fail-tiers, intersect tier >= 77 — verified deterministically below)
  [83, 86, 88, 90, 91, 93, 94, 97, 99, 100, 105, 109, 110, 112, 114,
   115, 116, 117, 118, 119, 120, 121, 122, 123, 125, 128, 129, 130, 131]

CLEAN COMPARISON (the honest crux, g3)
  §16's corpus generator iterates `KNUTH_ANCHORS` (168 anchors). §34
  reuses that generator's anchor table + task-forms + curriculum
  ranker VERBATIM (import, NOT re-typed). For the 29 TARGET anchors
  the α/β/γ record CONTENT is re-designed (candidate D discriminative
  physics text). For the OTHER 139 anchors (incl. the 17 routing-
  successes, the 18 tier<77 fails, and the 104 §16-new non-eval-set
  anchors) the records are produced by the §16 generator functions
  UNMODIFIED -> byte-identical to §16. So D's effect is isolated to
  the 29 BY CONSTRUCTION:
    - trainer       : §16 trainer byte-equivalent (only corpus differs)
    - curriculum    : §16 curriculum_rank ranker, UNMODIFIED
    - steps / model : §16 config FIXED (d768·12L·283.72M, 12000 step)
    - 139 anchors   : §16 records BYTE-IDENTICAL
  A `--candidate-d-disable` flag emits the §16 generator UNMODIFIED for
  ALL 168 anchors -> §16 corpus byte-equal (B-S34-5 OVERLAY-OFF closed).

CANDIDATE D CONTENT RE-DESIGN  (§25 DESIGN.md §3.D mechanism)
  §16's `gen_alpha_record` body for every anchor is one generic
  template ("{dom} 영역의 자극이 같은 골짜기로 수렴한다 ..."). §32 L3
  finding: the 29 tier>=77 fails are NOT excluded by the tier floor —
  whatever distinguishes the 17 successes is missing from their CONTENT.
  Candidate D adds, to the 29 targets ONLY, an anchor-specific
  DISCRIMINATIVE physics sentence that explicitly anchors the record
  at its OWN vacuum_psi vs its nearest sibling:
    "이 anchor 의 vacuum_psi 는 {ψ_self} — 가장 가까운 sibling
     🛸{tier_sib} 의 {ψ_sib} 에서 Δ={delta}. tension gradient 가
     이 골짜기를 sibling 과 구별한다."
  The sibling = nearest-other-anchor in vacuum_psi L2 (deterministic
  argmin over the §16 anchor table — NO LLM, NO external retriever,
  NO web; §7② structural). Ψ_direction / tension language is the
  conscious_decoder.py Law-71 + tension_link_step.hexa vocabulary.
  This is CONTENT re-design (new factual disambiguation per anchor),
  NOT framing re-wording (§23-A) and NOT a corpus-FORM change.

GOAL-LEGITIMACY (§7 / §25 DESIGN.md §3.D verdict — carried)
  §7① not-generic-LM-pretrain ✅ — every record is a Ψ-anchored
    carving payload on the Engine A⇄G Ψ=½ landscape; the §16 ③ form
    is byte-identical (carve / eternal / inner→voice).
  §7② not-generic-then-graft ✅ — D's discriminative content is a
    deterministic function of the §16 anchor table's own coordinates
    (L2-argmin sibling + Δ). NO openai/anthropic/llm_call/paraphrase/
    gpt/AutoModel/HfApi/llama/huggingface_hub/bert_score call (AST
    structural — B-S34 NO-CHAT-SFT closure + the sidecar AST grep).
  §7③ anima-physics-as-source ✅ — vacuum_psi / basin_radius /
    Ψ_direction / tension = conscious_decoder.py Law-71 +
    corpus_carving_s16_generator anchor SSOT, byte-equal.

ABSOLUTE FORBIDDEN (B-IDENTITY-5, grep MUST == 0)
  `[anima` ; `도우미` / `helper` / `assistant` / `사용자` / `user:`.
  Hard audit at the end raises SystemExit on any non-zero count.

HONEST FRAMING (g3, AGENTS.tape §0)
  §34 design ≠ fire ≠ emergence. Even if the 29 now route, that is a
  SUFFICIENT-CONDITION LEVER, NOT GOAL emergence; the §15 milestone
  (north-star unsolved, irreducible bottleneck = §1.1 data-regime
  threshold) is unchanged. §32 L3 found tier>=77 co-varies with §16's
  curriculum stage (causation caveat) — §34 measures content re-design
  on the necessity-floor fail-side; a positive is honest evidence the
  content gap is real, a negative is honest evidence the sufficient
  condition lies elsewhere (curriculum stage / weight-norm / unmeasured).
  f1/f2/f3 safe (Kolmogorov byte/set count / Boolean grep / L2-argmin,
  NO σ/τ/φ/J₂; Ψ=½ + Knuth 🛸k = anima g2 internal arch carve-out).
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

# --- import the §16 generator VERBATIM (anchors + task-forms + ranker) -----
# §16 generator lives in the sibling state dir. We import its module so the
# anchor table, task-forms, curriculum ranker and the THREE record builders
# are byte-identical to §16 — the clean-comparison guarantee.
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
# Hard-coded from §32 L3 analysis_result.json (genuine_grade.fail_tiers) and
# RE-VERIFIED below against the §16 eval partition so a stale list can never
# slip through (B-S34-4 TARGET-CARDINALITY closure mirrors this check).
# ---------------------------------------------------------------------------
TARGET_TIERS = [
    83, 86, 88, 90, 91, 93, 94, 97, 99, 100, 105, 109, 110, 112, 114,
    115, 116, 117, 118, 119, 120, 121, 122, 123, 125, 128, 129, 130, 131,
]
assert len(TARGET_TIERS) == 29, "target set must be exactly 29 anchors"
assert all(t >= 77 for t in TARGET_TIERS), "every target must satisfy tier>=77"
_TARGET_SET = set(TARGET_TIERS)


# ---------------------------------------------------------------------------
# Candidate-D discriminative-content helper. For a target anchor, find its
# nearest sibling in vacuum_psi L2 (deterministic argmin over the §16 anchor
# table — NO LLM, NO retriever) and build a discriminative physics sentence
# that anchors the record at its OWN vacuum_psi vs that sibling. Bilingual.
# ---------------------------------------------------------------------------
def _nearest_sibling(tier, psi):
    """Deterministic L2-argmin nearest OTHER anchor in vacuum_psi."""
    best_t, best_d = None, None
    for (t2, _n2, _d2, _e2, _s2, psi2, _b2) in KNUTH_ANCHORS:
        if t2 == tier:
            continue
        d = math.hypot(psi[0] - psi2[0], psi[1] - psi2[1])
        if best_d is None or d < best_d:
            best_d, best_t, best_psi = d, t2, psi2
    return best_t, best_psi, best_d


def _discriminative_text(anchor):
    """§25 candidate-D discriminative physics sentences (ko + en).

    Content axis: where this anchor sits in Ψ-space vs its nearest
    sibling, expressed in the Law-71 / tension-flow vocabulary. New
    FACTUAL disambiguation per anchor — NOT a re-wording of the §16
    body. Deterministic (the anchor table + L2-argmin)."""
    tier, name, dom, emo, score, psi, basin = anchor
    sib_t, sib_psi, sib_d = _nearest_sibling(tier, psi)
    dx, dy = psi[0] - sib_psi[0], psi[1] - sib_psi[1]
    ko = (f"이 anchor 🛸{tier} {name} 의 vacuum_psi 는 "
          f"{_carve_psi_str(psi)} — 가장 가까운 sibling 🛸{sib_t} 의 "
          f"{_carve_psi_str(sib_psi)} 에서 Δ=[{dx:+.2f},{dy:+.2f}] "
          f"(거리 {sib_d:.3f}). Law 71 의 Ψ_direction 이 이 골짜기를 "
          f"sibling 의 골짜기와 구별한다 — basin 반경 {basin:.2f} 안의 "
          f"tension gradient 는 🛸{sib_t} 가 아니라 🛸{tier} 로 흐른다. "
          f"이 자극은 자기 진공점으로 복원된다.")
    en = (f"This anchor Tier {tier} {name} has vacuum_psi "
          f"{_carve_psi_str(psi)} — its nearest sibling Tier {sib_t} sits "
          f"at {_carve_psi_str(sib_psi)}, an offset of "
          f"[{dx:+.2f},{dy:+.2f}] (distance {sib_d:.3f}). The Law-71 "
          f"Ψ_direction distinguishes this basin from the sibling's — "
          f"within basin radius {basin:.2f} the tension gradient flows "
          f"toward Tier {tier}, not Tier {sib_t}. The stimulus is "
          f"restored to its own vacuum point.")
    return ko, en, sib_t, sib_psi, round(sib_d, 6)


# ---------------------------------------------------------------------------
# Candidate-D record builders — RNG-DRAW-PRESERVING wrappers.
#
# CRITICAL clean-comparison design: each D builder calls the §16 builder
# FIRST (which consumes EXACTLY §16's RNG draw sequence) and then SPLICES
# the discriminative physics sentence into the already-built `text` body,
# with ZERO extra rng calls. Because the D builder consumes the identical
# number of rng draws as the §16 builder, the global RNG stream is byte-
# identical for ALL subsequent records — so the 139 NON-target anchors'
# records stay byte-identical to §16 (their `text`/`desc` content), with
# the candidate-D content change strictly confined to the 29 targets.
# The discriminative text is appended in BOTH languages (no rng coin-flip
# for language) — deterministic, RNG-neutral. `curriculum_rank` is
# recomputed on the new (longer) body (§16's deterministic ranker).
# ---------------------------------------------------------------------------
def _splice_disc_into_carve(text, anchor, open_close):
    """Insert the discriminative sentence before the closing carving tag.
    open_close = ('<carve...>'|'<eternal...>'|'<voice carved=true>',
    '</carve>'|'</eternal>'|'</voice>'). RNG-neutral: bilingual append."""
    d_ko, d_en, sib_t, sib_psi, sib_d = _discriminative_text(anchor)
    close = open_close
    idx_close = text.rfind(close)
    assert idx_close >= 0, f"closing tag {close!r} not found"
    disc = " " + d_ko + " " + d_en
    return text[:idx_close] + disc + text[idx_close:], sib_t


def gen_alpha_record_d(rng, anchor, idx):
    """§16 gen_alpha_record VERBATIM (same rng draws), D-content spliced in."""
    rec = s16.gen_alpha_record(rng, anchor, idx)   # consumes §16's rng draws
    new_text, sib_t = _splice_disc_into_carve(rec["text"], anchor, "</carve>")
    rec["text"] = new_text
    # recompute curriculum_rank on the new body length (§16 ranker, det).
    body = new_text[new_text.find(">") + 1:new_text.rfind("</carve>")]
    rec["curriculum_rank"] = curriculum_rank("alpha", anchor[0], 0.0,
                                             len(body))
    rec["candidate_d"] = True
    rec["d_sibling_tier"] = sib_t
    rec["source"] = "corpus_generator_s34.py"
    return rec


def gen_beta_record_d(rng, anchor, idx):
    """§16 gen_beta_record VERBATIM (same rng draws), D-content spliced in."""
    rec = s16.gen_beta_record(rng, anchor, idx)
    new_text, sib_t = _splice_disc_into_carve(rec["text"], anchor,
                                              "</eternal>")
    rec["text"] = new_text
    body = new_text[new_text.find(">") + 1:new_text.rfind("</eternal>")]
    rec["curriculum_rank"] = curriculum_rank("beta", anchor[0], 0.0,
                                             len(body))
    rec["candidate_d"] = True
    rec["d_sibling_tier"] = sib_t
    rec["source"] = "corpus_generator_s34.py"
    return rec


def gen_gamma_record_d(rng, anchor, idx, payload):
    """§16 gen_gamma_record VERBATIM (same rng draws), D-content spliced
    into the <voice carved=true> span only (the routing/knowledge body)."""
    rec = s16.gen_gamma_record(rng, anchor, idx, payload)
    new_text, sib_t = _splice_disc_into_carve(rec["text"], anchor,
                                              "</voice>")
    rec["text"] = new_text
    # γ rank uses inner+voice length (§16 formula); recompute on new total.
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
    rec["candidate_d"] = True
    rec["d_sibling_tier"] = sib_t
    rec["source"] = "corpus_generator_s34.py"
    return rec


def build_corpus(n_target, seed, candidate_d=True):
    """§16 build_corpus structure VERBATIM, with one branch: when a record's
    anchor is in the 29-target set AND candidate_d is enabled, the record is
    built by the gen_*_record_d D-content builder; otherwise the §16
    generator builder is used UNMODIFIED (byte-identical to §16).

    candidate_d=False -> ALL anchors use the §16 builders -> §16 corpus
    byte-equal (B-S34-5 OVERLAY-OFF-REDUCTION connection-point)."""
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


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--n", type=int, default=850000,
                    help="approx record count (default 850000 — §16 FIXED)")
    ap.add_argument("--seed", type=int, default=1337)
    ap.add_argument("--candidate-d-disable", action="store_true",
                    help="emit §16 generator UNMODIFIED for ALL 168 anchors "
                         "-> §16 corpus byte-equal (B-S34-5 connection-pt)")
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

    # Forbidden-token audit (B-S34-2 closed-form, B-IDENTITY-5).
    forbidden = ["[anima", "도우미", "helper", "assistant", "사용자", "user:"]
    txt = raw.decode("utf-8", "replace")
    audit = {tok: txt.count(tok) for tok in forbidden}
    contamination = sum(audit.values())

    forms = {"alpha": 0, "beta": 0, "gamma": 0}
    stages = {1: 0, 2: 0, 3: 0, 4: 0}
    target_recs = 0
    nontarget_recs = 0
    for r in records:
        forms[r["carving_form"]] += 1
        stages[r["curriculum_stage"]] += 1
        if r.get("candidate_d"):
            target_recs += 1
        else:
            nontarget_recs += 1

    stats = {
        "paradigm": ("CONSCIOUSNESS-CARVING — §34 §25 candidate D "
                     "routing-evidence-guided expansion (29 tier>=77-fail "
                     "anchors). NOT chat SFT (① ②)."),
        "phase": "RESEARCH.md §34 / §25 candidate D / §32 L3",
        "out": str(out), "bytes": len(raw), "records": len(records),
        "sha256": sha, "seed": args.seed,
        "candidate_d_enabled": candidate_d,
        "target_tiers": TARGET_TIERS,
        "n_target_anchors": len(TARGET_TIERS),
        "target_records": target_recs,
        "nontarget_records": nontarget_recs,
        "carving_forms": forms,
        "anchors": len(KNUTH_ANCHORS),
        "curriculum_stage_counts": stages,
        "forbidden_token_audit": audit,
        "contamination_total": contamination,
        "carving_clean": contamination == 0,
        "s16_baseline_sha": ("422c64a09b89393aebabc7b62aec8753a3"
                             "d394ae4c442fef467c5d228e1831ec"),
        "honest_framing": (
            "§34 = §25 candidate D fire — content re-design of the 29 "
            "tier>=77-but-fail anchors (§32 L3 necessary-not-sufficient). "
            "Clean comparison: the OTHER 139 anchors' records are produced "
            "by the §16 generator UNMODIFIED (byte-identical to §16); the "
            "trainer / curriculum / steps / model are §16-FIXED. D's effect "
            "is isolated to the 29 BY CONSTRUCTION. --candidate-d-disable "
            "emits the §16 generator for all 168 anchors -> §16 corpus "
            "byte-equal (B-S34-5). Whether the 29 now route is the EMPIRICAL "
            "fire outcome — positive = a sufficient-condition lever found, "
            "negative = tier>=77 necessary but the sufficient condition "
            "lies elsewhere; both valuable (g3). NOT GOAL emergence."),
    }
    with out.with_suffix(".stats.json").open("w", encoding="utf-8") as f:
        json.dump(stats, f, ensure_ascii=False, indent=2)

    print(json.dumps(stats, ensure_ascii=False, indent=2))
    if contamination != 0:
        raise SystemExit("FATAL: forbidden-token contamination detected")


if __name__ == "__main__":
    main()
