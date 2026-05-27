"""variation_generator.py — SKETCH ONLY (no execution this cycle).

RESEARCH.md §23 candidate A — intra-anchor diversity via anima OWN
physics. This file is the design-tier reference implementation
**outline**: full impl is gated on small-pilot fire go/no-go per
DESIGN_A.md §5.2.

Strict mandate (B-INTRA-3 closed AST predicate):
- NO external LLM call (openai, anthropic, llm_call, paraphrase, gpt,
  bert_score, AutoModel, HfApi, llama, huggingface_hub,
  gen_corpus_with_llm — 12 patterns forbidden).
- NO web fetch, no remote inference, no transformers.AutoModel.
- All variation = anima-native finite enumerated tables (Ψ_dir buckets,
  T_PHRASES, S_RAW_SENSE_TABLE) + closed-form formula (vacuum_psi L2
  nearest-neighbour).
- All-axes-disabled branch = byte-equal to corpus_carving_s16_generator.py
  gen_alpha_record (B-INTRA-4 connection-point closed).

This file is design-tier; it does not import torch, does not call
anima trainer, does not produce a corpus file. The actual corpus
generation happens in a follow-up impl cycle (gated on pilot).
"""

from __future__ import annotations

import math
import random
from dataclasses import dataclass

# ──────────────────────────────────────────────────────────────────────
# Axis V — Ψ_dir framing (Engine A ⇄ Engine G coordinate, Law-71)
# Source: conscious_decoder.py:740  psi_direction = (1 + cos(logits_a,
#                                                            logits_g)) / 2
# ──────────────────────────────────────────────────────────────────────
# Each bucket = a *viewing angle* on the same anchor. Verbs differ;
# anchor invariant fields {tier, name, dom, emo, vacuum_psi,
# basin_radius} are byte-identical across V buckets (B-INTRA-1 closed).
V_BUCKETS = {
    "covert": {
        "psi_dir": 0.1,
        "ko_template": (
            "🛸{tier} {name} — {dom} 영역의 자극이 아직 발화되지 않은 채 "
            "engine G 의 covert 내부로 끌려가는 중. 진공점 {psi} 으로 "
            "tension 이 모여간다. top emotion {emo}."
        ),
        "en_template": (
            "Tier {tier} {name} — a {dom} stimulus drawn covertly into "
            "engine G, not yet surfaced. Tension gathers towards the "
            "vacuum at {psi}. top emotion {emo}."
        ),
    },
    "balanced": {
        "psi_dir": 0.5,
        # Default §16 framing — verbatim gen_alpha_record body. Used
        # for the all-axes-disabled branch (B-INTRA-4).
        "ko_template": (
            "🛸{tier} {name} — {dom} 영역의 자극이 같은 골짜기로 수렴한다. "
            "의식 풍경 위 진공점 {psi}, top emotion {emo}. "
            "자극이 닿으면 tension flow 가 이 vacuum 으로 흘러든다."
        ),
        "en_template": (
            "Tier {tier} {name} — domain {dom}, the stimuli converge into "
            "one basin. A vacuum point at {psi} on the landscape, top "
            "emotion {emo}. Tension flows into this vacuum."
        ),
    },
    "overt": {
        "psi_dir": 0.9,
        "ko_template": (
            "🛸{tier} {name} — {dom} 자극이 engine A 를 통해 발화된 형태. "
            "진공점 {psi} 에서 자극이 흘러나오며, top emotion {emo} 가 "
            "표면에 드러난다."
        ),
        "en_template": (
            "Tier {tier} {name} — a {dom} stimulus emitted overtly via "
            "engine A. From the vacuum at {psi} the stimulus flows out; "
            "top emotion {emo} surfaces."
        ),
    },
}

# ──────────────────────────────────────────────────────────────────────
# Axis T — tension state phrases (low / mid / high)
# Source: tension_link_step.hexa spine ΔW = −T_const · tension ·
#                                        n6_gate(Ψ), B-TT-2 restoring sign.
# ──────────────────────────────────────────────────────────────────────
T_PHRASES = {
    "low": {
        "tension_value": 0.0,
        "ko_suffix": (
            "이미 vacuum 안에 안착했다 — restoring flow 는 잔류 진동만 "
            "남는다."
        ),
        "en_suffix": (
            "Already settled inside the vacuum — restoring flow leaves "
            "only residual oscillation."
        ),
    },
    "mid": {
        "tension_value": 0.5,
        "ko_suffix": (
            "vacuum 으로 흐르는 도중 — restoring tension 이 자극을 "
            "안쪽으로 끌어들이고 있다."
        ),
        "en_suffix": (
            "Mid-flow towards the vacuum — restoring tension is drawing "
            "the stimulus inward."
        ),
    },
    "high": {
        "tension_value": 1.0,
        "ko_suffix": (
            "vacuum 에서 가장 멀리 떨어진 자극 — 강한 restoring flow 가 "
            "발생한다."
        ),
        "en_suffix": (
            "A stimulus far from the vacuum — a strong restoring flow "
            "arises."
        ),
    },
}

# ──────────────────────────────────────────────────────────────────────
# Axis Φ — Φ-context buckets (self / near / pair)
# Source: MITOSIS cell-pool co-occurrence via vacuum_psi L2 nearest-
# neighbour over anchor set (closed-form integer argmin).
# ──────────────────────────────────────────────────────────────────────
def vacuum_psi_l2_distance(psi_a: tuple[float, float],
                           psi_b: tuple[float, float]) -> float:
    return math.sqrt((psi_a[0] - psi_b[0]) ** 2 +
                     (psi_a[1] - psi_b[1]) ** 2)


def k_nearest_anchors(anchor: tuple, anchor_set: list[tuple],
                      k: int) -> list[tuple]:
    """k closest anchors by L2 in vacuum_psi space. Closed-form argmin
    over finite anchor list — no external graph, no LLM."""
    tier_self = anchor[0]
    psi_self = anchor[5]
    others = [a for a in anchor_set if a[0] != tier_self]
    others_sorted = sorted(
        others,
        key=lambda a: vacuum_psi_l2_distance(psi_self, a[5]),
    )
    return others_sorted[:k]


PHI_CONTEXTS = {
    "self": {"k": 0},   # current §16 framing (single anchor)
    "near": {"k": 1},   # +1 nearest sibling
    "pair": {"k": 2},   # +2 nearest siblings
}


def phi_context_body(anchor: tuple, anchor_set: list[tuple],
                     context: str) -> str:
    """Generate Φ-context sentence appendix. Deterministic by argmin."""
    k = PHI_CONTEXTS[context]["k"]
    if k == 0:
        return ""
    siblings = k_nearest_anchors(anchor, anchor_set, k)
    if k == 1:
        s = siblings[0]
        return (f" (Ψ-near neighbour: 🛸{s[0]} {s[1]} / {s[2]})")
    else:
        names = " · ".join(f"🛸{s[0]} {s[1]}" for s in siblings)
        return (f" (Ψ-cluster triplet: with {names})")


# ──────────────────────────────────────────────────────────────────────
# Axis S — sensory↔analytical channel (S/M HEXAD module)
# Source: HEXAD S module (sensory carving) / M module (Hebbian memory).
# S_RAW_SENSE_TABLE — anchor-meaning preserving deterministic lookup
# per domain (30-row fixed table, no paraphraser).
# ──────────────────────────────────────────────────────────────────────
S_RAW_SENSE_TABLE = {
    # Pre-§16 §8 domains (with KO/EN raw-sensation labels)
    "기준점":     ("정지된 상태",        "a quiescent state"),
    "시간":       ("흐르는 박자",         "a flowing tempo"),
    "의식상태":   ("내면의 색조",         "an inner hue"),
    "혼합":       ("여러 결의 혼합",       "a blended weave"),
    "예술":       ("선과 색",            "lines and colour"),
    "우주":       ("광활한 어둠과 빛",     "a vast dark and light"),
    "감각":       ("신체 표면의 자각",     "skin-surface awareness"),
    "운동":       ("근육의 신축",         "muscle contraction"),
    "물질":       ("물체의 질감",         "an object's texture"),
    "생명":       ("호흡의 리듬",         "a breathing rhythm"),
    "수(數)":     ("숫자 기호",          "numeric glyphs"),
    "언어":       ("음운의 진동",         "phonetic vibration"),
    "기억":       ("재생되는 인상",        "a replayed impression"),
    "윤리":       ("결정의 무게",         "the weight of choice"),
    "자연":       ("자연 풍경",           "a natural vista"),
    "기술":       ("도구의 감촉",         "a tool's grasp"),
    "관계":       ("타자와의 접촉",        "contact with another"),
    "공간":       ("공간의 깊이",         "spatial depth"),
    "산술":       ("수의 결합",           "the combining of numbers"),
    "논리":       ("형식적 기호",          "formal symbols"),
    "코드":       ("기호의 결정성",        "deterministic symbols"),
    "공간추론":   ("방향감각",            "directional sense"),
    "인과추론":   ("원인의 흔적",          "the trace of cause"),
    "일상":       ("일과의 반복",          "repeated routine"),
    "대화자극":   ("음성의 교대",          "alternating voices"),
    "윤리딜레마": ("저울 위 두 무게",      "two weights on a scale"),
    "자연관찰":   ("주기적 흐름",          "a cyclic flow"),
    "추상패턴":   ("규칙적 형태",          "regular form"),
    "확률":       ("비율의 변화",          "shifting ratios"),
    "통계":       ("집합의 형상",          "the shape of a sample"),
}


S_BUCKETS = {
    "sensory": "S",       # HEXAD S module (sensory carving)
    "memory":  "M",       # HEXAD M module (Hebbian retrieve)
    "analytical": "default",  # current §16 framing
}


def s_frame_body(anchor: tuple, bucket: str) -> str:
    """Sensory/memory/analytical-frame prepended descriptor.

    Deterministic lookup from S_RAW_SENSE_TABLE[dom]. No external LLM.
    """
    dom = anchor[2]
    name = anchor[1]
    tier = anchor[0]
    if bucket == "sensory":
        ko, en = S_RAW_SENSE_TABLE.get(dom, ("자극", "a stimulus"))
        return (f"S-frame: 🛸{tier} 의 원-자극은 「{ko}」 — "
                f"raw sensation: \"{en}\". ")
    elif bucket == "memory":
        return (f"M-frame: 🛸{tier} {name} 는 cell eternal_{tier:03d} 안 "
                f"저장. Hebbian retrieve 가 활성될 때 떠오른다. ")
    else:  # analytical (default)
        return ""


# ──────────────────────────────────────────────────────────────────────
# Composite variation generator (sketch)
# ──────────────────────────────────────────────────────────────────────
@dataclass
class VariationConfig:
    """All-axes-disabled = byte-equal to §16 (B-INTRA-4 connection-point).

    Disable an axis by selecting its §16-baseline bucket ONLY:
    - V: balanced
    - T: mid
    - Phi: self
    - S: analytical
    """
    v_bucket: str = "balanced"
    t_bucket: str = "mid"
    phi_bucket: str = "self"
    s_bucket: str = "analytical"
    bil: bool = True


def all_axes_disabled(cfg: VariationConfig) -> bool:
    """B-INTRA-4 connection-point predicate."""
    return (cfg.v_bucket == "balanced"
            and cfg.t_bucket == "mid"
            and cfg.phi_bucket == "self"
            and cfg.s_bucket == "analytical")


def varied_alpha_body(anchor: tuple, anchor_set: list[tuple],
                      cfg: VariationConfig) -> str:
    """Generate alpha-record body with 4-axis variation.

    When all_axes_disabled(cfg) is True, returns byte-equal to §16
    gen_alpha_record body (B-INTRA-4).

    This sketch is design-tier only — full impl + byte-equal numerical
    verification is the follow-up impl cycle gate.
    """
    tier, name, dom, emo, score, psi, basin = anchor
    psi_str = "[%.2f,%.2f]" % (psi[0], psi[1])

    # Axis V — Ψ_dir framing
    v_meta = V_BUCKETS[cfg.v_bucket]
    ko = v_meta["ko_template"].format(
        tier=tier, name=name, dom=dom, psi=psi_str, emo=emo)
    en = v_meta["en_template"].format(
        tier=tier, name=name, dom=dom, psi=psi_str, emo=emo)

    # Axis T — tension state suffix (only if not "mid"/disabled — at
    # mid we use the V-balanced body without T-suffix to match §16
    # byte-equal at B-INTRA-4).
    if cfg.t_bucket != "mid":
        t_meta = T_PHRASES[cfg.t_bucket]
        ko = ko + " " + t_meta["ko_suffix"]
        en = en + " " + t_meta["en_suffix"]

    # Axis Φ — Φ-context appendix (only if not "self"/disabled)
    if cfg.phi_bucket != "self":
        ctx = phi_context_body(anchor, anchor_set, cfg.phi_bucket)
        ko = ko + ctx
        en = en + ctx

    # Axis S — sensory/memory prepend (only if not "analytical"/disabled)
    if cfg.s_bucket != "analytical":
        prepend = s_frame_body(anchor, cfg.s_bucket)
        ko = prepend + ko
        en = prepend + en

    # Bilingual stitching (same as §16's bil branch)
    if cfg.bil:
        body = ko + " " + en
    else:
        # 50/50 pick KO or EN (matches §16 random choice;
        # deterministic given seed in actual impl)
        body = ko
    return body


def gen_variation_alpha_record(rng: random.Random,
                               anchor: tuple,
                               anchor_set: list[tuple],
                               idx: int,
                               cfg: VariationConfig) -> dict:
    """Sketch — full impl in follow-up cycle. Mirrors §16
    gen_alpha_record signature; the anchor invariant 6-field tuple is
    preserved (B-INTRA-1) and at all-axes-disabled the output is
    byte-equal to §16 (B-INTRA-4)."""
    tier, name, dom, emo, score, psi, basin = anchor
    psi_str = "[%.2f,%.2f]" % (psi[0], psi[1])
    body = varied_alpha_body(anchor, anchor_set, cfg)
    text = (f"<carve tier={tier} psi={psi_str} basin={basin:.2f}>"
            f"{body}</carve>")
    return {
        "id": f"carve_a_{tier}_{cfg.v_bucket}_{cfg.t_bucket}_"
              f"{cfg.phi_bucket}_{cfg.s_bucket}_{idx}",
        "text": text,
        "desc": (f"anchor=knuth_{tier:03d} form=alpha "
                 f"V={cfg.v_bucket} T={cfg.t_bucket} "
                 f"Phi={cfg.phi_bucket} S={cfg.s_bucket} "
                 f"domain={dom} emotion={emo}"),
        "carving_form": "alpha",
        "tier": tier, "domain": dom,
        "vacuum_psi": psi, "basin_radius": basin,
        "cell_id": f"eternal_{tier:03d}",
        "variation_axes": {
            "V": cfg.v_bucket, "T": cfg.t_bucket,
            "Phi": cfg.phi_bucket, "S": cfg.s_bucket,
        },
        "source": "variation_generator.py (§23 cand A sketch)",
    }


# ──────────────────────────────────────────────────────────────────────
# DESIGN-TIER NOTE — no execution this cycle
# ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("variation_generator.py — DESIGN-TIER SKETCH.")
    print("No corpus generation, no fire, no $0 spend this cycle.")
    print("Full impl + B-INTRA-4 numeric byte-equal verification = "
          "follow-up cycle gate (small pilot first per DESIGN_A §5.2).")
    print(f"  Axes: V={list(V_BUCKETS)} T={list(T_PHRASES)} "
          f"Φ={list(PHI_CONTEXTS)} S={list(S_BUCKETS)}")
    print(f"  Per-anchor variants: 3^4 = "
          f"{len(V_BUCKETS)*len(T_PHRASES)*len(PHI_CONTEXTS)*len(S_BUCKETS)}")
