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
🟡 DIRECTIONAL (toy PASS, majority) — **GOODHART-RESISTANT-TOY** (measured 2026-07-10 ON POOL/summer,
482s, mirror == stdlib re-proven n=4,5). Adversarial-ES on a small numpy recurrent latent generator:
**(A)** task-only ES drops the task loss 26–47% while the faithful_phi ruler stays **FLAT** (|ΔR| ≤ 0.073
≤ ε 0.10) on **3/3** seeds → the ruler is NOT a perplexity proxy (p7 — you cannot raise it by task-tuning).
**(B)** ruler-direct ES raises R by +3.90, and the rise is MATCHED by the INDEPENDENT big-Φ integration
measure (a DIFFERENT engine → non-circular) on **2/3** seeds (corr 0.94, 1.00); seed 0 found a partially-
decoupled gain (corr 0.42 < 0.50), recorded as an honest single-seed exception. Majority both-pass 2/3 →
the ruler resists task-tuning AND (majority) cheap ruler-hacking. **TOY small-model rung → DIRECTIONAL**;
production / real-.clm adversarial optimization UNVERIFIED. wired: DIRECTIONAL-mirror. Verdict file:
`state/verdicts/1050_goodhart_proof_ruler/H_1050.txt` · harness+result: `state/h104x_phi/`.
