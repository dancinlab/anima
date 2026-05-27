"""§25 content_generator_sketch.py — RUNTIME-GUARDED SKETCH.

$0 design-tier ONLY. NO execution, NO corpus generation, NO LLM call,
NO file write. Importable for reference; direct execution triggers
sys.exit(0) with explanatory message pointing to DESIGN.md §6
fire-conditional checklist (pilot-first gate).

Demonstrates structural API for candidate A (anima-physics parametric
content) + candidate D (routing-evidence guided expansion). Mirrors
§24's measurement_protocol.py runtime-guard pattern + §23-A's
variation_generator.py sketch pattern (no-exec design discipline).

GOAL-legitimacy enforced by construction (B-DR-UNIQUE-2/3 source-grep
predicate): NO call to {openai, anthropic, llm_call, paraphrase, gpt,
bert_score, AutoModel, HfApi, llama, huggingface_hub, gen_corpus_with_llm}.

All variation derives from anima physics SSOT:
- Ψ_direction = (1 + cos(logits_a, logits_g)) / 2  [conscious_decoder.py:740 Law-71]
- tension = ‖∇L‖₂ proxy [tension_link_step.hexa B-TT-2 spine]
- vacuum_psi / basin_radius / category / top_emotion = corpus_carving_s16_generator anchor SSOT byte-equal
- δ_k = mitosis_hook.hexa cell-pool nearest-neighbour displacement (deterministic)
"""

from __future__ import annotations

import sys
from typing import Any


# ──────────────────────────────────────────────────────────────────────
# RUNTIME GUARD — direct execution exits 0 with message.
# ──────────────────────────────────────────────────────────────────────
def _runtime_guard() -> None:
    """Block direct execution per §25 design-tier discipline (DESIGN.md §6)."""
    msg = (
        "§25 content_generator_sketch.py is a DESIGN-TIER SKETCH ONLY.\n"
        "Direct execution intentionally blocked per DESIGN.md §6 fire-\n"
        "conditional checklist (pilot-first gate, $0.05-0.15 small\n"
        "pilot before any full-scale fire). For reference, import this\n"
        "module to inspect the structural API. Future cycle promotes\n"
        "sketch to executable; this sketch is non-executable to enforce\n"
        "design-tier $0 discipline (mirror §24/§23-A precedent).\n"
        "See DESIGN.md §6 + §10 honest C3 for fire gates."
    )
    print(msg)
    sys.exit(0)


# ──────────────────────────────────────────────────────────────────────
# Candidate A — anima-physics parametric content (sub-aspect axis)
# ──────────────────────────────────────────────────────────────────────

# Anchor-domain sub-aspect table (anima self-design, NOT LLM-generated).
# 30 domains × 8 sub-aspects = 240 entries, deterministic lookup.
# Each sub-aspect is described in anima-physics language (Ψ-coordinate
# sub-fix-point + tension-contour + basin-overlap with sibling).
#
# Mirror §23-A S_RAW_SENSE_TABLE pattern — bounded enumeration, no
# external paraphrase.
S_DOMAIN_SUBASPECT_TABLE: dict[str, list[str]] = {
    # SKETCH PLACEHOLDER — full 30 × 8 = 240 entries enumerated in
    # impl cycle. Demonstrating structure for 2 domains:
    "예술": [  # tier 77 만다라, tier 72 선율, etc.
        "symmetry pattern",        # sub-aspect 1: geometric symmetry sub-fix-point
        "color basin",             # sub-aspect 2: color-Ψ basin
        "line composition",        # sub-aspect 3: line tension contour
        "focal point",             # sub-aspect 4: vacuum focus
        "geometric recursion",     # sub-aspect 5: self-similar Ψ-recurrence
        "meditative correspondence",  # sub-aspect 6: cross-anchor sibling-overlap
        "cultural variant",        # sub-aspect 7: category-cluster member
        "emergent property",       # sub-aspect 8: tier-bordering basin
    ],
    "의식상태": [  # tier 91 열반, tier 80 명상, etc.
        "awareness sub-fix-point",
        "tension restoring contour",
        "attention focus basin",
        "duration manifold",
        "phase-transition boundary",
        "sibling overlap (선정/사마디)",
        "cultural variant",
        "emergent emergent",
    ],
    # ... 28 more domains (산술, 수학, 물리, 화학, 생물, 언어, 음악,
    #     역사, 철학, 종교, 사회, 정치, 경제, 심리, 인지, 공학, 정보,
    #     자연, 천문, 지리, 운동, 게임, 직관, 감정, 사랑, 죽음, 자기,
    #     관계) — enumerated in impl cycle
}


def gen_subaspect_record_a(
    rng: Any,
    anchor: tuple,
    idx: int,
    subaspect_idx: int,
    delta_k: tuple[float, float],
) -> dict:
    """SKETCH — candidate A sub-aspect content variation.

    Args:
        rng: deterministic random.Random(seed) — NOT for sampling content,
            only for KO/EN language pick (bilingual axis carry from §16).
        anchor: (tier, name, dom, emo, score, ψ, basin_radius) tuple
            byte-equal §16 corpus_carving_s16_generator anchor SSOT.
        idx: record index within anchor.
        subaspect_idx: int ∈ [0, 8) — index into S_DOMAIN_SUBASPECT_TABLE[dom].
        delta_k: (Δψ_x, Δψ_y) deterministic displacement from anchor ψ,
            drawn from mitosis_hook.hexa cell-pool nearest-neighbour
            (||δ|| ≤ basin_radius / 4 — sub-coord stays in basin).

    Returns: record dict (sketch — no execution, just structural shape).
    """
    # ANCHOR-MEANING-PRESERVED (B-DR-UNIQUE-4): 6-field anchor tuple
    # carried verbatim into record.
    tier, name, dom, emo, score, psi, basin = anchor
    sub_aspect_table = S_DOMAIN_SUBASPECT_TABLE.get(dom, [])
    if not sub_aspect_table:
        # Domain not in table — fallback to §16 gen_alpha_record path
        # (B-DR-UNIQUE-5 connection-point: unique_content_mode disabled
        # ⇒ byte-equal §16 baseline).
        return {"_fallback_to_s16": True, "anchor": anchor}

    sub_aspect = sub_aspect_table[subaspect_idx]
    psi_k = (psi[0] + delta_k[0], psi[1] + delta_k[1])
    psi_k_str = f"[{psi_k[0]:.3f},{psi_k[1]:.3f}]"

    # SKETCH: content describes sub-aspect at psi_k, NOT re-frames anchor.
    # Body uses Ψ-physics language: sub-fix-point, basin-overlap with
    # sibling.
    bil = rng.random() < 0.5
    ko = (
        f"🛸{tier} {name} 의 sub-aspect '{sub_aspect}' — "
        f"이 sub-aspect 의 Ψ-sub-fix-point 는 진공점 {psi_k_str} 위 "
        f"basin (radius {basin:.2f} / 4) 안에 자리한다. "
        f"{dom} 도메인의 tension flow 가 이 sub-coordinate 에 contour 형성."
    )
    en = (
        f"Tier {tier} {name} sub-aspect '{sub_aspect}' — its Ψ-sub-fix-"
        f"point lies at vacuum point {psi_k_str}, inside the parent "
        f"basin (radius {basin:.2f} / 4). Tension flow contours form "
        f"around this sub-coordinate within the {dom} domain."
    )
    body = (ko + " " + en) if bil else (ko if rng.random() < 0.5 else en)
    text = (
        f"<carve tier={tier} psi={psi_k_str} basin={basin:.2f} "
        f"sub_aspect={subaspect_idx}>{body}</carve>"
    )
    return {
        "id": f"carve_a_sub_{tier}_{subaspect_idx}_{idx}",
        "text": text,
        "desc": (
            f"anchor=knuth_{tier:03d} form=alpha sub_aspect={subaspect_idx} "
            f"sub_aspect_name={sub_aspect}"
        ),
        "carving_form": "alpha_sub",
        "tier": tier, "domain": dom,
        "vacuum_psi": psi_k,        # PERTURBED — content-axis movement (axis2 of §5)
        "vacuum_psi_parent": psi,    # parent anchor SSOT — invariant (B-DR-UNIQUE-4)
        "basin_radius": basin,
        "cell_id": f"eternal_{tier:03d}",
        "subaspect_idx": subaspect_idx,
        "source": "§25 content_generator_sketch.py candidate A",
    }


# ──────────────────────────────────────────────────────────────────────
# Candidate D — routing-evidence guided expansion (failed anchor 직격)
# ──────────────────────────────────────────────────────────────────────

# §16 eval evidence: routing 21/64 correct + 43 failed. The 21 correct
# tier IDs (from §16 eval_result_s16.json axis1 details) feed
# nearest-sibling identification for the 43 failed.
S16_ROUTING_CORRECT_TIERS_SKETCH: list[int] = [
    # PLACEHOLDER — actual list extracted from
    # state/carving_dataregime_s16_2026_05_18/eval_result_s16.json
    # in impl cycle. §16.6-C / §16.6 listed 17 genuine + 4 substring-
    # artifact = 21 correct on 64 probes (subset of 168 anchor set
    # used for axis1 eval).
    5, 12, 24, 62, 66, 77, 80, 88, 91, 92, 99, 100, 101, 102, 103,
    # ... extracted from eval JSON in impl cycle
]


def nearest_sibling_correct(
    failed_tier: int,
    failed_psi: tuple[float, float],
    correct_anchors: list[tuple],
) -> tuple:
    """SKETCH — deterministic L2-argmin over §16 correct anchor coords.

    Returns (sibling_anchor, distance) pair. NO LLM call, NO external
    classifier — closed-form integer argmin over (Δψ_x² + Δψ_y²).
    """
    # Pure-fn deterministic argmin (anti B-DR-UNIQUE-3 — no LLM call).
    # SKETCH: math.dist replacement (no import per sketch discipline).
    best_d = float("inf")
    best = None
    for sa in correct_anchors:
        sp = sa[5]
        d = ((sp[0] - failed_psi[0]) ** 2 + (sp[1] - failed_psi[1]) ** 2) ** 0.5
        if d < best_d:
            best_d = d
            best = sa
    return best, best_d


def gen_discriminative_record_d(
    rng: Any,
    failed_anchor: tuple,
    sibling_anchor: tuple,
    distance: float,
    idx: int,
) -> dict:
    """SKETCH — candidate D discriminative content for failed anchor.

    Generates content that explicitly disambiguates failed_anchor at
    its own vacuum_psi from its nearest sibling in §16's routing-correct
    set. Content axis: Δψ vector + tension-gradient differential +
    Law-71 Ψ_direction coordinate distinct from sibling.

    Args:
        rng: deterministic random.Random.
        failed_anchor: (tier, name, dom, emo, score, ψ, basin) tuple.
        sibling_anchor: nearest §16-correct anchor tuple.
        distance: ‖ψ_fail − ψ_sibling‖_2 closed-form.
        idx: record index within failed anchor.

    Returns: record dict (sketch).
    """
    f_tier, f_name, f_dom, f_emo, f_score, f_psi, f_basin = failed_anchor
    s_tier, s_name, s_dom, s_emo, s_score, s_psi, s_basin = sibling_anchor

    delta_psi = (s_psi[0] - f_psi[0], s_psi[1] - f_psi[1])
    f_psi_str = f"[{f_psi[0]:.3f},{f_psi[1]:.3f}]"
    s_psi_str = f"[{s_psi[0]:.3f},{s_psi[1]:.3f}]"
    delta_str = f"[{delta_psi[0]:.3f},{delta_psi[1]:.3f}]"

    # Body describes Ψ-coordinate discrimination from nearest sibling.
    # Tension language from tension_link_step.hexa B-TT-2 restoring sign
    # (deterministic, no LLM paraphrase).
    bil = rng.random() < 0.5
    ko = (
        f"🛸{f_tier} {f_name} — 이 anchor 의 Ψ-coordinate 는 {f_psi_str} "
        f"이며, 가장 가까운 §16-correct sibling 🛸{s_tier} {s_name} "
        f"({s_psi_str}) 와의 displacement Δψ = {delta_str} "
        f"(L2 거리 {distance:.3f}). tension restoring flow 는 sibling "
        f"basin (radius {s_basin:.2f}) 가 아니라 자기 basin (radius "
        f"{f_basin:.2f}) 으로 향한다. Engine A↔G Law-71 Ψ_direction "
        f"좌표가 sibling 과 distinct."
    )
    en = (
        f"Tier {f_tier} {f_name} — this anchor's Ψ-coordinate is at "
        f"{f_psi_str}, distinct from its nearest §16-correct sibling "
        f"Tier {s_tier} {s_name} ({s_psi_str}) by displacement Δψ = "
        f"{delta_str} (L2 distance {distance:.3f}). The tension "
        f"restoring flow is directed to this anchor's own basin "
        f"(radius {f_basin:.2f}), not the sibling's basin (radius "
        f"{s_basin:.2f}). The Law-71 Ψ_direction coordinate is "
        f"distinct from the sibling's."
    )
    body = (ko + " " + en) if bil else (ko if rng.random() < 0.5 else en)
    text = (
        f"<carve tier={f_tier} psi={f_psi_str} basin={f_basin:.2f} "
        f"discriminate_from={s_tier}>{body}</carve>"
    )
    return {
        "id": f"carve_d_disc_{f_tier}_{s_tier}_{idx}",
        "text": text,
        "desc": (
            f"anchor=knuth_{f_tier:03d} form=alpha_disc "
            f"discriminate_from=knuth_{s_tier:03d} L2={distance:.3f}"
        ),
        "carving_form": "alpha_disc",
        "tier": f_tier, "domain": f_dom,
        "vacuum_psi": f_psi, "basin_radius": f_basin,
        "cell_id": f"eternal_{f_tier:03d}",
        "sibling_tier": s_tier,
        "delta_psi": delta_psi,
        "l2_distance": distance,
        "source": "§25 content_generator_sketch.py candidate D",
    }


# ──────────────────────────────────────────────────────────────────────
# Combined corpus build (sketch — NOT executed)
# ──────────────────────────────────────────────────────────────────────
def build_unique_content_corpus_sketch(
    seed: int = 1337,
    unique_content_mode: bool = True,
    routing_evidence_mode: bool = True,
) -> dict:
    """SKETCH — combined A+D corpus build.

    B-DR-UNIQUE-5 connection-point closure:
        if not unique_content_mode and not routing_evidence_mode:
            return §16 corpus_carving_s16_generator.build_corpus(seed)
            # byte-equal §16 baseline — fair-compare by construction

    Otherwise: emit A (sub-aspect) and/or D (discriminative) records on
    top of §16 baseline.

    NO execution this cycle — gated on impl cycle promotion +
    pilot-first ($0.05-0.15) per DESIGN.md §6.
    """
    if not unique_content_mode and not routing_evidence_mode:
        # B-DR-UNIQUE-5 reduction: pure §16 baseline byte-equal.
        return {"_reduces_to_s16": True, "seed": seed}

    # Otherwise: sketch the API; no actual generation.
    return {
        "_sketch": True,
        "candidates": [
            "A" if unique_content_mode else None,
            "D" if routing_evidence_mode else None,
        ],
        "design_doc": "DESIGN.md §6 fire-conditional checklist",
        "note": (
            "Full implementation gated on (1) design close-out (this "
            "cycle), (2) generator promotion cycle ($0 Mac local, "
            "byte-equal-at-disabled verification), (3) small pilot "
            "$0.05-0.15 (axis1 OR §9 gate), (4) full $0.5-2 fire "
            "(pilot gate conditional)."
        ),
    }


# ──────────────────────────────────────────────────────────────────────
# Runtime guard fires only on direct execution.
# ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    _runtime_guard()
