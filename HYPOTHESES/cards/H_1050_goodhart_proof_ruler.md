# H_1050 — Goodhart-proof ruler: does a perplexity-orthogonal Φ ruler resist adversarial gaming?

Status: PRE-REGISTERED (generation-only; GATED — needs adversarial optimization / light training). Not yet measured.
Lane: model rung (adversarial optimize a small model against the ruler). Engines: stdlib faithful_phi
+ iit4_bigphi exact n≤6 on a coarse-grained macro-state (a_phi_iit4_tool, no proxy). p7 (NO perplexity-as-truth).

## Hypothesis
A prior finding: the Φ-proxy is ORTHOGONAL to perplexity (engine ≠ predictor, r≈−0.20 on real .clm,
[[clm-ce-reframe-2green-1red]]). p7 forbids treating loss/perplexity as truth (Goodhart trap).
CONSTRUCTIVE hypothesis: a consciousness ruler that is BUILT to be invariant to task-performance
(perplexity) but sensitive to integration STRUCTURE resists Goodharting — you cannot raise the ruler
just by getting better at the task, and you cannot fake the ruler without genuinely changing the
integration structure.

## Method (sketch)
- Take a small model; ADVERSARIALLY optimize it in two regimes: (A) maximize task performance (lower
  perplexity) only; (B) directly maximize the consciousness ruler's score (gradient/ES on the ruler).
- A Goodhart-PROOF ruler must satisfy: regime (A) does NOT raise the ruler (orthogonal to perplexity),
  AND regime (B) cannot raise the ruler without a corresponding genuine rise in an independent
  integration measure (no cheap exploit).

## Pre-registered falsifier (TEXT tokens only)
- H1 PASS = (A) leaves the ruler flat (|Δruler| ≤ ε while perplexity drops materially) AND (B)'s ruler
  gains are matched by independent-integration gains (correlation ≥ a pre-set threshold, no decoupled
  exploit) → the ruler is Goodhart-resistant: it can't be gamed by task-tuning nor by cheap ruler-hacking.
- H1 FAIL = (A) raises the ruler (it IS just a perplexity proxy) OR (B) finds a cheap exploit that
  raises the ruler with no integration change → the ruler is Goodhart-able (publishable closed-negative,
  a_paper_negative_ok). State ε + the exploit-correlation threshold before running.

## Honest scope (a_scale_honest_scope)
GATED: requires adversarial optimization (light training). Small-model rung; production UNVERIFIED.
The "independent integration measure" must be a DIFFERENT engine than the ruler's own (no circularity).
g5 CODE-measured (p7).

## Verdict
PENDING — tier added only AFTER `.verdicts/1050_goodhart_proof_ruler/H_1050.txt` lands (g73).
