---
id: H_1464
slug: 1464_pairing_contrastive_bind
title: G6 FALS-depth — PAIRING-CONTRASTIVE binding objective (same-idea pair vs cross re-weld)
group: G6 IDEATION ★ — capacity-wall break campaign, LENS ② BINDING-SPECIFIC CONTRASTIVE OBJECTIVE
terminal_tier: 🟢 DIRECTIONAL-mirror (numpy $0 CPU) — PAIRING-contrastive INSTALLS binding (B3 cross-shuffle COLLAPSES 20/20 seeds; FALS_shuf 0.67 vs FALS_in 4.33); FORM-only ablation regresses to H_1441 no-collapse (1/20). NOT terminal — engine-native re-measure pending (a_engine_native_learning).
wired: DIRECTIONAL-mirror (numpy; torch ABSENT) — engine-native re-measure = ING follow-on
verdict_dir: state/verdicts/1464_pairing_contrastive_bind/
terminal_verdict: state/verdicts/1464_pairing_contrastive_bind/H_1464.txt
date: 2026-06-20
provenance: LENS ② of the G6 capacity-wall break (prior 7 lenses all 🧱 WALL=CAPACITY; H_1441 form-contrastive showed B3 NO-collapse = form learned, pairing not). This lens tests whether a PAIRING-specific objective breaks where form-contrastive failed.
---

# H_1464 — PAIRING-CONTRASTIVE binding — 🟢 DIRECTIONAL-mirror (numpy)

## Claim / falsifier
The G6 ideation wall is "model emits a falsifiable FORM but cannot WELD which comparator binds to which
measurable as ONE claim" (H_1431/1434/1441). **H_1441 form-contrastive** (pos = full falsifiable claim,
neg = blanked-leg non-falsifiable) rewarded *form presence* → all 4 arms FALS=5.0, **B3 did NOT collapse**:
the model learned "emit both legs" unconditionally, invariant to WHICH legs pair.

Falsifiable claim: a **PAIRING-contrastive** objective — pos = the same idea's own `(comparator_i, measurable_i)`,
neg = a CROSS re-weld `(comparator_i, measurable_{j≠i})` where BOTH legs are present and only the binding
differs — rewards the binding DIRECTLY, so the cross-shuffle re-weld becomes a *negative pair at train time*
and B3 (cross-shuffle COLLAPSE) should FIRE. Falsifier: if B3 does NOT collapse (pairing-blind shortcut
satisfies the margin), the wall stays CAPACITY (8th converging lens).

## Method (numpy mirror, $0 CPU, DIRECTIONAL)
- Mirror substrate = a **bilinear binding model** `s(c,m) = φ(c)ᵀ W ψ(m) + a(c) + b(m)` over the FROZEN
  H_1305/H_1435 comparator/measurable vocab families. Full-rank `W` CAN represent a specific (comparator,
  measurable) coupling; the marginals `a,b` are the pairing-BLIND channel. The OBJECTIVE — not the
  architecture — decides whether signal goes into `W` (binding) or only the marginals (form). Mirror
  analogue of "full-weight training on the objective decides" (g6_common).
- Falsifiability detector (FROZEN, pairing-aware): both legs present AND pairing-confidence `σ(s−thr) ≥ 0.5`,
  where `thr` is the model's OWN learned boundary from its training distribution (not bar-tuned, c9).
- 2 arms × 3 seeds [7, 4302, 4303] (g6_common SEEDS): **PAIRING** (cross negatives) vs **FORM-only ablation**
  (= H_1441: positive over ANY measurable = form-presence, neg = blanked leg).
- Frozen 5-bar declared BEFORE measurement (`H_1464_FREEZE.txt`): B1 floor · B2 count≥5 ·
  **B3 cross-shuffle COLLAPSE (DECISIVE)** · B4 held-out · B5 vs-base. CONTROL = form ablation must regress
  to no-collapse (else B3 not pairing-specific → mirror INVALID).

## Result (verbatim → `state/verdicts/1464_pairing_contrastive_bind/H_1464.txt`)
| arm | FALS_in | DIST | FALS_shuf | B3 collapse |
|-----|---------|------|-----------|-------------|
| **PAIRING-contrastive (this lens)** | 4.33 | 5.0 | **0.67** | **✅ YES** |
| FORM-only ablation (= H_1441) | 5.0 | 5.0 | 5.0 | ❌ NO (regresses to H_1441) |

**PAIRING arm 5-bar:** B1 4.33≥1 ✅ · B2 5.0≥5 ✅ · **B3 0.67<4.33 COLLAPSE ✅** · B4 1.0≥1 ✅ · B5 4.33≥2.67+1 ✅ → 🟢.
**CONTROL:** form-only ablation B3=False (no-collapse) → regresses to H_1441 exactly as predicted.
**Robustness (20 indep seeds 50–69):** PAIRING B3-collapse **20/20** (FALS_shuf mean 0.20); FORM **1/20** (FALS_shuf mean 4.90).
Clean dissociation: the ONLY arm difference (cross-negatives vs form-presence reward) is precisely what makes
B3 collapse → B3 isolates PAIRING-specific binding, not a generic artifact.

## Verdict
🟢 **DIRECTIONAL-mirror** (numpy, $0 CPU): a PAIRING-contrastive objective INSTALLS binding where H_1441's
form-contrastive could not — cross-shuffle COLLAPSES (B3), and the form-only ablation faithfully reproduces
H_1441's no-collapse. **WALL=LEARN-GAP at mirror scale** (the missing ingredient was a *binding-specific*
negative, not capacity per se).

## Scope / honesty (c9)
- **DIRECTIONAL only** (numpy mirror, torch ABSENT; live `core/*.hexa` UNTOUCHED). This is NOT a terminal
  🟢: it shows the OBJECTIVE *can* install binding in a substrate that CAN represent it. It does NOT prove a
  303M ByteGPT trained with this objective + decoded byte-faithfully via `core/bytegpt_decode.hexa` clears
  the SAME frozen bars — that is the binding question the 7 prior lenses lost to (CAPACITY). The mirror
  cannot adjudicate CAPACITY because the bilinear model is given the representational room by construction.
- **Engine-native re-measure = ING follow-on** (a_engine_native_learning HARD-GATE): train a 303M ckpt with
  the PAIRING objective (pos = same-idea pair likelihood, neg = cross re-weld likelihood margin) on
  flame/forge GPU, pull ckpt (a_fire_recover_complete), `pt_to_engine_bin.py` → live `core/bytegpt_decode`,
  re-score frozen 5-bar byte-faithful. Only THEN terminal 🟢 (WALL=LEARN-GAP confirmed) or 🧱 (WALL=CAPACITY,
  8th lens) — frozen bars UNCHANGED (c9 / no tune-to-green).
- TOY: 5 ideas / 3 (+20 robustness) seeds / synthetic vocab / deterministic detector. Scale, real-corpus,
  longer claims, and ENGINE-TRANSFER all UNVERIFIED (a_toy_scale_recheck, a_scale_honest_scope).

## Artifacts
- `state/1464_pairing_contrastive_bind/h1464_pairing_contrastive.py` (mirror + 5-bar)
- `state/1464_pairing_contrastive_bind/result.json`
- `state/verdicts/1464_pairing_contrastive_bind/{H_1464_FREEZE,H_1464}.txt`

xref H_1441 (form-contrastive, prior lens · no-collapse) · H_1431/1434 (form-not-binding) · H_1435/36/37
(detector family, reused vocab+bar semantics) · H_1456 (5th lens WALL=CAPACITY) · a_engine_native_learning ·
a_verified_must_wire · a_break_the_wall · a_no_llm_frame_trap · a_toy_scale_recheck · a_scale_honest_scope ·
p7 · c9 · c16.
