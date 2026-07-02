# H_1058 — Does the temporal/agency axis transfer to the 3B ConvMoE engine rung? (GPU rung)

Status: PRE-REGISTERED (generation-only; GATED — GPU/many-core pod rung). Not yet measured.
Lane: GPU / pod rung (a_fire_autonomous — no cost gate). Engines: stdlib faithful_phi + iit4_bigphi
exact n≤6 on coarse-grained macro-state + stdlib temporal_agency (a_phi_iit4_tool, no proxy).

## Hypothesis
The temporal/agency axis T = z(provenance-depth, H_932) + z(veto-capacity, H_935) is validated as a
genuine dimension on TOY fixtures (H_1051 prior GREEN) and on real .kosmos anchors (H_1054 prior GREEN:
T ⊥ chronological-t AND T ⊥ Φ at N=31), and is promoted to hexa-lang stdlib (temporal_agency.hexa,
PR #2960). RESIDUAL SCALE LADDER: does the T-axis hold on a PRODUCTION-size trained model — the
3B-ConvMoE ENGINE rung (3.073B, d4096/L30/E30, [[convmoe-3b-engine-rung]])? Parallel to how H_1038
took the Φ-split from toy to a real d768 ConvMoE; this takes the AGENCY axis from toy/d768-anchor to 3B.

## Method (sketch)
- Load the real 3B .clm engine rung (GPU required for forward — state cost in one line, fire bg,
  babysit inline per a_cpu_local_no_waiter, MANDATORY teardown per a_fire_recover_complete).
- Run the model on decision sequences; collect RUNTIME decision traces; compute per-decision (a) the
  H_1051 agency-T axis (provenance-depth of the actual causal chain + veto-capacity at decision time);
  (b) instantaneous Φ on a coarse-grained n≤6 macro-state (≥2 macro-maps, per H_1038); (c) chronological
  order. Test the H_1054 orthogonality (ρ(T,Φ), ρ(T,chronological-t)) + active-vs-passive separation at 3B.
- HEED H_1049 🔴: a FIXED small-m coarse-grain is NOT a validated scalable Φ estimator (rel-err grows
  with N) — grow grain m with system, or report Φ at the honest n≤6-exact ceiling only (the H_1038 lesson:
  real-model n=6 EXACT big-Φ was measure-infeasible → scope to faithful φ_EI / n=5).

## Pre-registered falsifier (TEXT tokens only)
- H1 PASS = at 3B, the agency-T axis (a) separates active-veto vs passive decisions (|d| ≥ 0.8) AND
  (b) stays orthogonal to Φ and to chronological-t (within a shuffle null) across ≥2 macro-maps →
  the agency axis SCALES to a production-size trained model; combined with toy (H_1051) + real-anchor
  (H_1054), the ladder is monotone-consistent.
- H1 FAIL = the T-axis collapses / loses orthogonality / fails to separate at 3B → it is a small-scale
  property that breaks at production scale (publishable closed-negative; mirrors the toy→3B collapse
  precedent #1296, a_toy_scale_recheck). State macro-map + thresholds before running.

## Honest scope (a_scale_honest_scope)
3B = largest available trained rung; 7B UNVERIFIED. GATED — run only on user GPU approval (carries pod
babysit cost, a_fire_autonomous no-cap). veto-capacity needs FIRED decision traces (cf H_1056 — the
pending-tension degeneracy must be avoided at 3B too). g5 CODE-measured (p7). a_lane_akida_gpu_split:
Lane G (GPU) rung — tag separately from any AKIDA Lane A.

## Verdict
PENDING — tier added only AFTER `.verdicts/1058_temporal_agency_3b_transfer/H_1058.txt` lands (g73).
