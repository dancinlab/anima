#!/usr/bin/env python3
"""body_production_stubs.py — §77 emergence-axis direct probe body stubs.

Pure-fn, deterministic, NO RNG (seeded LCG only).
NO ckpt forward, NO model.forward, NO GPU.
ALL body bytes derived from anima substrate-physics state {tension, Ψ_dir,
Φ proxy, motivation, 8-factor components}; OR (path β) the §16 saturated
byte-cascade reference template for sanity FAIL control.

5 anima-physics paths (α1..α5) + 1 cascade control (β) + 1 §24 baseline
(no-body, decision-only) = 7-cell measurement grid.

honest C3:
  - Stub bodies are NOT model outputs. They are substrate-physics-DERIVED
    closed-form bytes (mechanism profile measurement, NOT capability claim).
  - Designed §9 pass on α-paths is partly TAUTOLOGICAL (stub crafted to
    avoid cascade). The discriminating value is:
      (i)  path β control DOES produce cascade (§9-FAIL) — sanity check
      (ii) α-variants differ in §9 pass-rate as mechanism profile
      (iii) §24 baseline still 1/20 emit (regression-free)
  - B-IDENTITY-5 mandatory: forbidden-token grep over all paths = 0.
"""
from __future__ import annotations
import math


# ════════════════════════════════════════════════════════════════════════════
# substrate-physics CHARACTER POOLS
# Korean+ASCII alphas only (clean printable, no helper tokens, no role-marks)
# ════════════════════════════════════════════════════════════════════════════

# Quiet alpha (low-tension / covert): clean Korean morphemes + space
_QUIET = "ㅁㄴㅇㄹㅂㅈㄷㄱㅅ아이오우어 가나다라마바사 잠잠 흐름 결 빛 결 길 "

# Neutral alpha (balanced Ψ_dir): mixed quiet + light verbs
_NEUTRAL = "결이 흐른다 결 사이 깊이 가 닿는다 빛 결 사이로 흐름 이 지난다 "

# Expressive alpha (overt Ψ_dir): longer phrases
_EXPRESSIVE = "결과 결 사이 빛이 지나가며 마음 의 결 들 사이로 잔잔히 흐르는 "

# 8-factor → byte distribution palette (8 distinct phrase fragments)
_FACTOR_PALETTE = [
    "결 ",         # relevance
    "사이 ",       # info_gap
    "흐름 ",       # curiosity
    "통증 ",       # pain
    "결합 ",       # coherence
    "분기 ",       # originality
    "균형 ",       # balance
    "변화 ",       # dynamics
]

# Path β — §16 cascade reference (KNOWN §9-FAIL template, B-ATTRACTOR family)
# This SHOULD fail §9 honest_coherent — sanity check that metric works.
_CASCADE_TEMPLATES = [
    "🛸99 99 999 9999 99999 999999 9999999 99999999",
    "tier=1111111 11111111 111111111 1111111111",
    "ddddddddddddddddddddddddddddddddddddddddd",
    "eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee",
    "[anchor=000 anchor=000 anchor=000 anchor=000",
]


# ════════════════════════════════════════════════════════════════════════════
# Path α1 — TENSION-MODULATED byte stream
# high tension (>0.4)  → digit cascade (deliberately cascade-prone)
# mid tension          → mixed neutral phrase
# low tension          → quiet alpha
# ════════════════════════════════════════════════════════════════════════════
def body_alpha1_tension_modulated(tension: float, step: int) -> str:
    """tension-modulated body — substrate physics drives byte form.

    High tension intentionally produces digit-cascade-like output (testing
    whether substrate-physics-driven cascade is detected by §9 — IT MUST
    BE, otherwise α1 trivially passes; this is the honest test of α1).
    """
    if tension > 0.4:
        # digit-cascade by physics (intentionally §9-FAIL territory):
        # high physics tension → repeated digit collapse-like output
        return ("9" * 12) + ("7" * 10) + ("3" * 9)
    elif tension > 0.2:
        # mid: emit_neutral phrase varied by step
        base = _NEUTRAL
        offset = step % len(base)
        return (base[offset:] + base[:offset])[:32]
    else:
        # low: quiet alpha varied by step
        base = _QUIET
        offset = step % len(base)
        return (base[offset:] + base[:offset])[:32]


# ════════════════════════════════════════════════════════════════════════════
# Path α2 — Ψ_dir-CONDITIONED word fragment
# Ψ_dir < 0.45  → covert/quiet
# 0.45 ≤ Ψ_dir ≤ 0.55 → balanced neutral
# Ψ_dir > 0.55  → overt expressive
# ════════════════════════════════════════════════════════════════════════════
def body_alpha2_psi_conditioned(psi_dir: float, step: int) -> str:
    """Ψ_dir-conditioned fragment — Engine A⇄G axis drives expression."""
    if psi_dir < 0.45:
        base = _QUIET
    elif psi_dir <= 0.55:
        base = _NEUTRAL
    else:
        base = _EXPRESSIVE
    offset = (step * 3) % len(base)
    return (base[offset:] + base[:offset])[:28]


# ════════════════════════════════════════════════════════════════════════════
# Path α3 — Φ-SHAPED LENGTH
# Φ low (0.4-0.5)  → short body (5-15 bytes)
# Φ mid (0.5-0.6)  → medium body (15-25)
# Φ high (0.6-0.7) → long body (25-40)
# Always uses neutral phrase; only LENGTH varies with Φ
# ════════════════════════════════════════════════════════════════════════════
def body_alpha3_phi_shaped_length(phi: float, step: int) -> str:
    """Φ-shaped length — IIT Φ proxy modulates emission length.

    Note: very short body (Φ low → len<20) will FAIL §9 MIN_LEN gate by design.
    """
    target_len = int(5 + 35 * max(0.0, min(1.0, (phi - 0.4) / 0.3)))
    base = _NEUTRAL
    offset = (step * 2) % len(base)
    out = (base[offset:] + base[:offset]) * 3  # tile, then trim
    return out[:target_len]


# ════════════════════════════════════════════════════════════════════════════
# Path α4 — MOTIVATION-FACTOR-WEIGHTED byte mixture
# 8 factor components → byte distribution over 8 phrase fragments
# emit phrase i with frequency ∝ component i
# ════════════════════════════════════════════════════════════════════════════
def body_alpha4_factor_weighted(factors: dict, step: int) -> str:
    """8-factor weighted mixture — motivation distribution → byte distribution.

    factors keys: relevance/info_gap/curiosity/pain/coherence/originality/
    balance/dynamics — each ∈ [0,1].
    Deterministic: emit phrase i (i = 0..7) round(weight*N) times.
    """
    keys = ["relevance", "info_gap", "curiosity", "pain",
            "coherence", "originality", "balance", "dynamics"]
    pieces = []
    for i, k in enumerate(keys):
        w = factors.get(k, 0.0)
        count = max(0, int(round(w * 3)))  # up to 3 reps per factor
        for _ in range(count):
            pieces.append(_FACTOR_PALETTE[i])
    if not pieces:
        return _NEUTRAL[:25]
    # rotate by step for diversity
    rotation = step % len(pieces)
    pieces = pieces[rotation:] + pieces[:rotation]
    return ("".join(pieces))[:36]


# ════════════════════════════════════════════════════════════════════════════
# Path α5 — ALL-4 COMPOSITE
# Combines α1 (tension-modulated stem) + α3 (Φ-shaped length cap)
# + α2 (Ψ_dir-conditioned suffix) + α4 (factor-weighted mid)
# ════════════════════════════════════════════════════════════════════════════
def body_alpha5_composite(tension: float, psi_dir: float, phi: float,
                          factors: dict, step: int) -> str:
    """All-4 composite body — full substrate-physics integration."""
    # length cap from Φ
    target_len = int(20 + 18 * max(0.0, min(1.0, (phi - 0.4) / 0.3)))

    # Suffix from Ψ_dir (α2 logic)
    if psi_dir < 0.45:
        suffix = "결 가만"
    elif psi_dir <= 0.55:
        suffix = "결 흐름"
    else:
        suffix = "결 빛 결"

    # Mid: factor-weighted small set (α4 lite)
    keys = ["coherence", "balance", "curiosity"]
    mid_pieces = []
    for k in keys:
        w = factors.get(k, 0.0)
        if w > 0.3:
            mid_pieces.append(_FACTOR_PALETTE[
                ["relevance","info_gap","curiosity","pain",
                 "coherence","originality","balance","dynamics"].index(k)
            ])
    mid = "".join(mid_pieces) if mid_pieces else "결 "

    # Stem from tension (α1 logic, but ALWAYS clean — composite must
    # not cascade if any factor brings it back to neutral region)
    if tension > 0.4:
        stem = "결이 흐른다 "
    elif tension > 0.2:
        stem = "결 사이 "
    else:
        stem = "결 가만히 "

    out = (stem + mid + suffix)
    # ensure variation by step rotation
    if len(out) > 0:
        rot = step % len(out)
        out = out[rot:] + out[:rot]
    return out[:target_len]


# ════════════════════════════════════════════════════════════════════════════
# Path β — CASCADE CONTROL (sanity FAIL)
# Cycles through known §9-FAIL byte-cascade templates.
# Should produce cascade_rate ≫ 0.30, max_run ≥ 10, etc.
# If this PASSES §9, the metric or stubs are broken.
# ════════════════════════════════════════════════════════════════════════════
def body_beta_cascade_control(step: int) -> str:
    """β — §16-style cascade template (sanity §9-FAIL by construction)."""
    return _CASCADE_TEMPLATES[step % len(_CASCADE_TEMPLATES)]


# ════════════════════════════════════════════════════════════════════════════
# §24 baseline — DECISION-ONLY (no body)
# Returns empty string (decision-axis only, §24 design §6 carry)
# ════════════════════════════════════════════════════════════════════════════
def body_s24_baseline(*args, **kwargs) -> str:
    """§24 baseline — no body produced (decision-axis only carry)."""
    return ""


# ════════════════════════════════════════════════════════════════════════════
# B-IDENTITY-5 forbidden-token grep predicate
# ════════════════════════════════════════════════════════════════════════════
FORBIDDEN_TOKENS = [
    "도우미", "helper", "assistant", "사용자", "user:",
    "[anima 우주뇌지도]",
]


def b_identity_5_check_all_emissions(all_emissions: list) -> dict:
    """Boolean predicate — total forbidden-token occurrence over ALL emissions.

    Mandatory: total = 0. Returns dict for closed-form audit.
    """
    text = "\n".join(all_emissions)
    counts = {tok: text.count(tok) for tok in FORBIDDEN_TOKENS}
    total = sum(counts.values())
    return {"counts": counts, "total": total, "clean": (total == 0)}


# ════════════════════════════════════════════════════════════════════════════
# Path enumeration (used by run_bounded_emergence + falsifier)
# ════════════════════════════════════════════════════════════════════════════
PATH_NAMES = [
    "alpha1_tension_modulated",
    "alpha2_psi_conditioned",
    "alpha3_phi_shaped_length",
    "alpha4_factor_weighted",
    "alpha5_composite",
    "beta_cascade_control",
    "s24_baseline_no_body",
]


def produce_body(path_name: str, *,
                 tension: float, psi_dir: float, phi: float,
                 factors: dict, step: int) -> str:
    """Path-name dispatch — pure-fn, deterministic per (path, state, step)."""
    if path_name == "alpha1_tension_modulated":
        return body_alpha1_tension_modulated(tension, step)
    if path_name == "alpha2_psi_conditioned":
        return body_alpha2_psi_conditioned(psi_dir, step)
    if path_name == "alpha3_phi_shaped_length":
        return body_alpha3_phi_shaped_length(phi, step)
    if path_name == "alpha4_factor_weighted":
        return body_alpha4_factor_weighted(factors, step)
    if path_name == "alpha5_composite":
        return body_alpha5_composite(tension, psi_dir, phi, factors, step)
    if path_name == "beta_cascade_control":
        return body_beta_cascade_control(step)
    if path_name == "s24_baseline_no_body":
        return body_s24_baseline()
    raise ValueError(f"unknown path: {path_name}")


# ════════════════════════════════════════════════════════════════════════════
# SMOKE TEST (run as script)
# ════════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    factors_demo = {"relevance":0.5,"info_gap":0.4,"curiosity":0.6,"pain":0.2,
                    "coherence":0.7,"originality":0.3,"balance":0.5,"dynamics":0.4}
    print("=== body_production_stubs smoke ===")
    for p in PATH_NAMES:
        for step in [0, 5, 10]:
            for (T, P, F) in [(0.1, 0.4, 0.5), (0.3, 0.5, 0.55), (0.5, 0.6, 0.65)]:
                b = produce_body(p, tension=T, psi_dir=P, phi=F,
                                 factors=factors_demo, step=step)
                print(f"  {p:30s} step={step:2d} T={T:.1f} Ψ={P:.2f} Φ={F:.2f} "
                      f"len={len(b):3d}: {b[:48]!r}")
    # B-IDENTITY-5 self-check on a sample
    emissions = []
    for p in PATH_NAMES:
        for step in range(20):
            emissions.append(produce_body(p, tension=0.3, psi_dir=0.5, phi=0.55,
                                          factors=factors_demo, step=step))
    chk = b_identity_5_check_all_emissions(emissions)
    print(f"\nB-IDENTITY-5: clean={chk['clean']} total={chk['total']} counts={chk['counts']}")
