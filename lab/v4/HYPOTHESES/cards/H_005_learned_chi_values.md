---
id: H_005
ssot: ARCHITECTURE.json → next-gate.mech1.g3-research-gate (this card is the pre-register SEED for G3-a)
slug: learned-chi-values
title: a LEARNED concord χ̂ = g(φᵢ,φⱼ) on the FIXED proxy-parser support reproduces the hand-computed field's causal power on held-out honorific binding — i.e. the FIELD VALUES (signs), not just the format, can be trained; one variable = χ policy (hand χ vs learned χ̂), support held fixed
domain: verification-design (causal drill · learned-values stage G3-a · pre-register SEED)
status: inconclusive-consolidate-at-g2
exploration_method: research-gate delegated to Fable 5 (DESIGN_g3_research_gate_fable5.md, literature-verified) — G3-a is the run-first, cheapest-decisive half of the learned-duel extension after H_004 🟢 SUPPORTED
verification_method: deterministic forced-choice d_acc (free-slot {0,1,2,4}) on the H_004 f2″/f1′/drill panels; a learned χ̂ module trained jointly on the drill, with a same-g wrong-support placebo (C-χ̂plc) + the H_004 controls carried verbatim
pre_register_frozen: true
frozen_at: 2026-07-17 (G3-0d PASS probe φ→hon=1.0 · re-smoke GREEN chi_grad+phi_frozen · d=64 MPS full-check GREEN incl F4/F5 · collector wiring-verified · honest-limit(a) SCOPE recorded)
deterministic: false
llm: none in the eval path (design only; χ̂ is trained, scoring is deterministic forced-choice)
---

# H_005 — G3-a: can a LEARNED χ̂ reproduce the hand-computed concord field's causal power?

> **SSOT**: design tree `ARCHITECTURE.json → ng.mech1.g3-research-gate`. Absorbed from Fable's G-3
> research-gate (`state/h004_.../DESIGN_g3_research_gate_fable5.md`). **FROZEN 2026-07-17** — G3-0d PASS
> (probe φ→hon=1.0, SCOPED) + re-smoke GREEN + d=64 MPS full-check + collector wiring-verified all cleared.
> H_004 (G-2, the FIELD FORMAT claim) stays SEALED 🟢; H_005 extends its scope FORMAT→VALUES (drill-register).

## Why this hypothesis (the caveat H_004's own verdict names)

H_004 SUPPORTED certifies the parse-tension FIELD FORMAT (edge-aligned support × concord values) as the
causal carrier of held-out honorific binding — but the concord χ (which sign each contested cell carries)
was **hand-computed** (`gc.concord_field`: χ[i][j] = +1 if hon[i]==hon[j] else −1). G3-a asks the next
falsifiable question with the SUPPORT held fixed (the proxy L→R/R→L disagreement `gc.t_struct`, unchanged):
**can a trained χ̂ = g(φᵢ,φⱼ) learn those signs from node honorific features and reproduce the field's
causal power?** This is the field's VALUES half; the harder SUPPORT half (trained parser opposition) is
H_006/G3-b, gated behind this.

## The one-variable lever — χ policy (hand χ vs learned χ̂), support FIXED

- **A-hand** — the H_004 A-duel field verbatim: T = t_struct(support) ⊙ χ_hand(hon). The anchor (E≈0.95 free-slot).
- **A-χ̂** — SAME support t_struct, but VALUES from a trained module: T̂ = t_struct(support) ⊙ χ̂, where
  χ̂[i][j] = tanh((Uφᵢ)·(Vφⱼ)/√r + b) is a BILINEAR g (U,V ∈ R^{4×d}, ~2–4k params), and **φᵢ = per-node
  mean-pooled state of the FROZEN post-CPT trunk** over node i's SURFACE bytes (answer-blind, struct-free —
  the same top-layer interface G3-b's shared readout will read). g trains jointly on the drill (χ̂ is IN the
  resolver's forward graph); φ is frozen (no grad). One variable vs A-hand: the concord is learned from what
  the model REPRESENTS instead of hand-set; support/panel/model/steps/seed byte-identical. **Why φ=trunk not
  raw hon** (Fable fidelity review g3a_review): g(raw hon) cannot fail — learning the equality of the two
  scalars χ_hand compares is trivial, so A-χ̂≡A-hand and F1a/K2/K3 become unreachable; it would certify the
  MLP, not the mechanism (the exact `dont`). Reading trunk φ makes "is concord recoverable from the model's
  representation" the real, falsifiable content, and keeps G3-a a genuine kill-gate for G3-b (which reads
  learned tower states).
- **C-χ̂plc** (primary control) — the SAME trained g, but on per-item-PERMUTED support (right learned values,
  wrong cells). Isolates alignment-not-capacity. (The VALUES-matter control is **F5 carried** — the
  strip-resolution substitution on A-χ̂ must collapse d_acc, as H_004 measured 1.0→0.5.)
- **C-scaf** (T̂≡0) · **C-perm** (permuted-gold harness) — carried verbatim from H_004.

## Falsifiers + admissibility (arithmetic, before any training)

- **F1a (primary)**: Δ = d_acc(A-χ̂, f2″) − d_acc(C-χ̂plc, f2″). SUPPORTED iff Δ ≥ 0.15 both seeds;
  DEAD iff Δ < 0.05 both. Admissibility: E-anchor A-χ̂≈0.95 (matches A-hand ceiling) vs C-χ̂plc≈0.63
  (H_004's measured C-plc, same spectrum-preserved-but-misaligned floor) ⇒ headroom 0.32 = 2× the bar ✓.
- **F1a′ (non-inferiority)**: d_acc(A-χ̂) ≥ d_acc(A-hand) − 0.05 both seeds — the learned values must not
  be materially worse than the hand ones (else G3-a reports the measured COST of removing the hand, K3).
- **F2 liveness** f1′(A-χ̂) ≥ 0.85 both · **precond** drill d_acc(A-χ̂) ≥ 0.95 both · **F3 not-free**
  f2″(C-scaf) < 0.60 · **harness** f2″(C-perm) ∈ [0.45,0.55] · **F4 eff-rank** A-χ̂ offtop ≥ 0.20 ·
  **F5 union** A-χ̂ union ΔCE ≥ 0.01 OR Δd_acc ≥ 0.05 — carried from H_004 (all on free-slot d_acc {0,1,2,4}).
  (No standalone F6: in G3-a the **C-χ̂plc arm IS the placebo** — same learned χ̂, spectrum-matched but
  edge-misaligned support — so F1a already tests A-χ̂ against a matched-magnitude placebo; the H_004 F6
  vs C-plc does not apply and is deliberately dropped, not omitted.)

## $0 gate before training (G3-0d) — must pass before freeze

Logistic probe: is the honorific bit recoverable (≥0.90, held-out split) from the FROZEN d=384 CPT trunk's
per-node φ? If the trunk does not represent the concord, χ̂ = g(φ) has nothing to read and G3-a is UNBUILT
(the gate doing its job, not a setback). No H_004 checkpoint needed — G3-a's OWN CPT stage is the same
recipe; run one CPT per seed and probe (tens of minutes, $0 cash). `train_g3a.py --g3-0d`.

**RESULT (2026-07-17): probe φ→hon held-out acc = 1.0 (n=1200) ≥ 0.90 → PASS, χ̂ can read concord ⇒ build.**
But acc=1.0 TRIGGERS honest-limit (a) below at the ceiling: the templatic drill register lets the trunk
encode the hon bit near-verbatim, so g(φ) is ~one linear unmix from g(raw hon). G3-a stays admissible and F5
still guards vacuity, but the eventual F1a-green claim is SCOPED to "concord recoverable from trunk
representations on the drill register" — a modest, honestly-bounded result, NOT a strong natural-text claim.

## Honest-limit (Fable fidelity review) — when G3-a is STILL a scaffolding-certifier

Even rewired, name it on the frozen record: (a) if G3-0d probes ≈1.0 because the templatic drill register
preserves byte identity nearly verbatim in top-layer states, then g(φ) is one linear unmix from g(raw hon)
and a green F1a certifies "concord is recoverable from trunk representations **on the drill register**,
nothing about learned SUPPORT" — scope it, and RECORD the probe's actual number; (b) if F5 on A-χ̂ fails to
collapse d_acc, the signs were epiphenomenal on this rig and the "values" framing is vacuous regardless of F1a.

## Honest kill criteria (Fable K2/K3 — G-2 is a defensible resting place)

- **K2**: F1a fails (Δ < 0.05 both seeds) ⇒ learned values work equally on WRONG support ⇒ it is capacity,
  not binding ⇒ STOP and consolidate at H_004's FORMAT claim; do NOT proceed to G3-b (strictly harder).
- **K3**: F1a′ fails (A-χ̂ < A-hand − 0.15, precond met) ⇒ trained values cannot reproduce hand concord at
  this scale ⇒ same stop; report the gap as the measured cost of removing the hand.

## Cross-Links

- H_004 (SEALED 🟢) — the FORMAT claim this extends. `ARCHITECTURE.json → ng.mech1.g2-precond-failed`.
- H_006 / G3-b (trained parser opposition = SUPPORT half) — gated behind G3-a green + $0 gates G3-0a/b/c.
- Design: `state/h004_parser_duel_tension_rank_drill_2026-07-16/DESIGN_g3_research_gate_fable5.md`.

## Verdict — 🟡 INCONCLUSIVE → CONSOLIDATE AT G-2 (2026-07-17)

collect_verdict_g3a.py (free-slot, d=384 ×2seed ×5arm) → **WIRING FAILURE (precond)**: A-χ̂ fit its own
drill UNSTABLY (s0=1.0, s1=0.832 < 0.95). Measurement path CLEAN (chi_grad+phi_frozen assert both seeds;
A-hand on the same rig fit 1.0/1.0) — so this is a **training-stability limit of the tiny learned bilinear g**,
not a tool bug, and per `infra-wall-noneval` a precond-failed run is not graded a clean verdict.

But the substantive signal is unambiguous and does NOT need the unstable seed:
- **F1a passes** (Δ = A-χ̂ − C-χ̂plc = 0.298 / 0.191, both ≥ 0.15) — the learned values DO require correct
  edge alignment (not capacity). F4 (0.35/0.50 ≥0.20) + F5 (dCE 14/68, d_dacc 0.32/0.21) also fire clean.
- **F1a′ FAILS on BOTH seeds — including the fit seed s0** (margin −0.176 / −0.290): A-χ̂ f2″ 0.82/0.71 ≪
  A-hand 1.0. This is Fable's **K3**: the learned χ̂ cannot reproduce the hand concord's power at this scale;
  the FORMAT can be hand-specified but the VALUES are only ~partially recoverable from a frozen-trunk φ that
  encodes hon near-verbatim (honest-limit (a), G3-0d probe = 1.0).

**Decision (K3 STOP + honest-limit): CONSOLIDATE AT G-2.** H_004's FIELD-FORMAT claim (🟢 SUPPORTED) stands
as the campaign's proven, defensible result. G3-a does NOT extend it: the learned-values stage is inconclusive
(precond-unstable) and, where admissible, materially below the hand concord (K3). No re-run — a fit s1 would
still land at PARTIAL-K3, not SUPPORTED, since even the fit s0 fails F1a′. The measured cost of removing the
hand: ~0.18–0.29 d_acc. G3-b (trained SUPPORT = H_006) remains the only untried lever, but it is strictly
harder and inherits this scale's optimization fragility — do not open it without a fresh research/feasibility
gate. Artifacts: g3a_result_full.json · verdict_g3a.json.

## G3-b feasibility RE-GATE (2026-07-17) — H_006 NOT OPENED, mech-1 sealed at G-2

`state/h004_.../REGATE_g3b_feasibility_fable5.md` ($0, closed-form on this card's own numbers): G3-a
upper-bounds G3-b's value channel (the concord sign must still be computed by the shared readout f from
the same trunk-state interface under the same drill-CE objective; the s0 drill-1.0/f2″-0.824 gap is an
IDENTIFICATION failure, not capacity, so a bigger f worsens it), and support recall only multiplies down:
E[A-tduel] ≈ 0.53 + 0.24·r ⇒ F1b non-inferiority has NEGATIVE headroom at any r, and the Δ form needs
r ≥ 1.25 for the 2×-bar headroom this card was frozen under (bare bar r ≥ 0.65 vs literature 0.46–0.50
directed at ≥8M params). No $0 run can greenlight (G3-0b is kill-only; G3-0a needs the absent external
parser). **mech-1 SEALS at G-2**: FIELD-FORMAT 🟢 + K3's measured 0.18–0.29 cost-of-removing-the-hand;
trained SUPPORT = substrate wall, UNREACHED (not falsified). Reopen: ≥8M/jamo substrate passing an
F1a′-analog first · non-templatic register (probe < 1.0) · or external parser as a new campaign premise.
