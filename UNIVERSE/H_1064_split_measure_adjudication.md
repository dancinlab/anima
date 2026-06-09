# H_1064 — split-measure-adjudication (practical capstone of the Φ measure-dependence arc)

Status: PRE-REGISTERED (generation-only; not yet measured)
Lane: zero-cost CPU toy. Engines: stdlib faithful_phi + iit4_bigphi (a_phi_iit4_tool, NO proxy).

## Hypothesis
The whole Φ measure-dependence arc established that on PLANNING policies the faithful φ_EI scalar
and big-Φ DISAGREE in sign (faithful↑ / big-Φ↓) — robustly (H_1037 n=6, H_1038 real-CLM), causally
redundancy-driven (H_1039), and bounded to planning (H_1062/H_1063). The arc leaves ONE unanswered
PRACTICAL question: **when the two measures SPLIT, WHICH ONE should a consciousness-ruler trust?**
I.e. on the split policies, does faithful φ_EI or big-Φ better track an INDEPENDENT, NON-CIRCULAR
behavioral/causal consciousness-proxy?

## Pre-registered INDEPENDENT consciousness-proxy (FROZEN before scoring)
PRIMARY proxy = **causal self-prediction (CSP)** — a BEHAVIORAL readout of how strongly the macro
binary state CAUSALLY constrains its OWN next macro state, in IIT's cause-effect SPIRIT but rendered
as a plain held-out prediction accuracy number, NOT a Φ computation.

Operationalization (on the SAME median-binarized macro bits the H_1039 path produces, n=4 units):
- Form one-step transition pairs (s_t -> s_{t+1}) over the rollout (s = the n-bit macro state vector).
- Fit a leave-one-out / held-out per-bit predictor of each next-bit from the current full macro state
  (closed-form ridge on the {0,1} bits, evaluated held-out), and score
  CSP = mean over bits of (held-out balanced-accuracy − chance) clipped at 0 — i.e. how much the
  current macro state DETERMINES its own next state ABOVE the per-bit base-rate chance.
- This is do→see causal constraint of the state on its own future, scored behaviorally.

ROBUSTNESS proxy = **intervention-robustness (IR)** — stability of the macro next-state map under a
controlled single-bit perturbation: flip one current bit, re-predict the next state with the same
fitted map, average the |Δ predicted-next-state| over bits/steps; IR = 1 − normalized perturbation
sensitivity (a stable, integrated macro-dynamics resists single-bit perturbation washing out its
future). Reported alongside CSP; the PRIMARY frozen falsifier is on CSP.

### Non-circularity justification (FROZEN)
- CSP/IR are NOT faithful φ_EI: faithful φ_EI is the MIP-minimized effective-information INTEGRAL over
  a TPM with a partition search. CSP has NO partition, NO minimization-over-cuts — it is a held-out
  next-state regression accuracy. IR has no TPM/partition either.
- CSP/IR are NOT big-Φ: big-Φ is the irreducibility of the whole over its MINIMUM partition. The proxy
  NEVER partitions the system; it never computes irreducibility.
- CSP/IR are NOT perplexity (p7): perplexity is a token-vocabulary likelihood/loss treated as truth.
  CSP is a macro-state→macro-state determinism accuracy on the substrate's OWN dynamics (no token
  vocabulary, no loss-as-verdict). p7 honored — the proxy is a coherence/causal readout, scored by code.
- The proxy reads the SAME bits both Φ-measures read, but transforms them by a DIFFERENT operation
  (held-out predictive accuracy of the next state) than EITHER Φ-measure — so it is an external
  adjudicator, not a relabelled copy of one of them.

## Design (non-circular adjudication)
On the planning policies where the split occurs (REUSE the H_1039 substrate: planning_trajectories +
top-variance median-binarization, h1004/h1012 UNMODIFIED), treat each of the 30 SEEDS' planning
trajectory as one split-policy instance. Per instance compute, on the SAME bits:
- faithful φ_EI (stdlib mirror exact n=4),
- big-Φ (stdlib mirror exact n=4),
- the independent proxy CSP (and IR).
Then rank-correlate (Spearman) EACH Φ-measure against the proxy ACROSS the 30 split-policy instances:
Spearman(faithful, CSP) vs Spearman(big-Φ, CSP). Per-seed sign-stability via leave-one-out jackknife
of the Spearman sign + lead across the 30 seeds.

## Pre-registered FALSIFIER (FROZEN thresholds; TEXT tokens only — set BEFORE any Φ-vs-proxy view)
- Δρ_bar = 0.30 (FROZEN). SIGN_STABILITY_BAR = 0.80 (≥80% of leave-one-out jackknife folds keep the
  WINNING measure's Spearman sign AND its lead).
- H1 PASS = ONE-MEASURE-TRACKS-PROXY: |Spearman(faithful,CSP) − Spearman(big-Φ,CSP)| ≥ Δρ_bar AND the
  winning measure's sign is stable across ≥80% of leave-one-out folds → the ruler should use THAT
  measure when they split. Report which measure wins.
- FAIL (a) NEITHER-SEPARATES = |Δρ| < Δρ_bar → the split is UNDECIDABLE at toy scale; the ruler must
  REPORT BOTH (strengthens the measure-dependence paper's "name the measure" prescription). Publishable
  closed-negative (a_paper_negative_ok).
- FAIL (b) PROXY-RELATIVE = the two proxies (CSP vs IR) disagree on which Φ-measure wins → adjudication
  is proxy-relative; report both proxies' rankings. Publishable (a_paper_negative_ok).
- NO goalpost move. Δρ_bar + SIGN_STABILITY_BAR + the proxy definition are frozen in THIS file before
  the harness computes any Φ-vs-proxy correlation.

## Reproduce-gate (BEFORE scoring)
- RE-PROVE python mirror ≡ stdlib EXACT 6dp at n=4 AND n=5 (h1012.prove_mirrors_at_n); BITS/log2
  MI = H(A)+H(B)−H(A,B) (H_1043 nats-bug lesson).
- Confirm reproduce-H_1039: planning-vs-greedy CONTROL split contrast ≈ faithful +2.33 / big −4.01
  (SPLIT present on control) BEFORE the per-instance adjudication is scored.

## Honest scope (a_scale_honest_scope, a_toy_scale_recheck)
Toy n=4 EXACT (n=5 mirror-proven), 30 seeds, SERIAL CPU $0, NO GPU/pod. CSP is the PRIMARY proxy, IR
the robustness proxy; other behavioral proxies (held-out behavioral-class recoverability) are
follow-ups. Production scale UNVERIFIED. g5 CODE-measured (no LLM self-judge, p7).

## Verdict
(pending — TEXT-only until .verdicts/1064_split_measure_adjudication/H_1064.txt lands)
