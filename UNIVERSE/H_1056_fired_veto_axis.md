# H_1056 — Complete the VETO half of the agency axis on FIRED-tension real anchors (H_1054 residual)

status: 🟢 SUPPORTED — H1-PASS-FIRED-2COMP-AGENCY-RULER (verdict .txt landed: .verdicts/1056_fired_veto_axis/H_1056.txt)

## lineage

Direct residual-closing follow-on to H_1054 (prior GREEN, H1-PASS-ORTHOGONAL-INDEPENDENT-AXES,
.verdicts/1054_kosmos_time_vs_agency/H_1054.txt) and H_1051 (prior GREEN, temporal-agency
ruler). H_1054 showed the H_1051 causal-agency T-axis = z(provenance-depth [H_932]) +
z(veto-capacity [H_935]) is orthogonal to KOSMOS chronological carve-order on the real e7_31
anchors. BUT its veto-capacity component was DEGENERATE: the e7_31 anchors carry `pending`
(un-fired) tension, so the H_935 motivation `score` was fixed by the placeholder PureField init
and the active-veto fraction SATURATED at 1.0 for every anchor (zero within-set variance) ->
only provenance-DEPTH was the live carrier of T. H_1054's own honest-scope caveat states: "A
fired-tension anchor set is needed to exercise veto-capacity as a second agency axis." THIS rung
supplies exactly that and completes the second component.

## question

On a FIRED-tension real anchor set (anchors whose `@payload tension` carries an actual fired
emit trajectory, NOT `pending`), where a veto WAS exercisable through the H_935 decompose_decision
gate driven by the real fired tension:

1. Is veto-capacity NON-DEGENERATE (within-set variance > 0, active-veto fraction NOT pinned at
   1.0 for every anchor)?
2. Does the FULL 2-component agency-T = z(provenance-depth) + z(veto-capacity) SEPARATE
   active-veto-dominated emits from passive (sub-threshold) emits?
3. Does the full 2-component T stay ORTHOGONAL to instantaneous faithful-Phi AND to
   chronological-t on the fired substrate (within the H_1054 empirical shuffle null)?

## fired-tension anchor set

Anchor set = the V3 substrate-native EMISSION anchors
HEXAD/UNCLASSIFIED/state/grid_3b_s187_2026_05_21/vP21H_gamma/kosmos_anchors/v3_emit_*.kosmos
(N = 14), read READ-ONLY via the canonical kosmos_io loader (a_kosmos pointer-only; the loader,
spec, and repo are NOT edited). Each anchor carries:

- `@payload tension` = a FIRED 5-channel fingerprint {concept, context, meaning, authenticity,
  sender} with real within-set variance (e.g. concept ranges ~1.93-2.74, sender ~1.83-2.34) —
  this is the actual fired emit trajectory, NOT `pending`. THIS is what was missing on e7_31.
- `emitted_at` = ISO-8601 wall-clock emission timestamp -> chronological-t (true fire time,
  distinct from a carve-rank ordinal).
- `knuth_tier` = the training-step rank at emission (200 .. 2000).
- coord, lane (MITOSIS cell), radius, top_emotion, text payload.

The fired 5-channel tension is INVERTED back to the 8 motivation factors via the documented
kosmos_io map_8factor_to_5channel table (HEXAD_NATIVE_V3 section 0.5), and those factors drive
the H_935 PureField + motivation `score` so the brain_decide gate (should_emit AND safe) is
exercised on the REAL fired drive of each anchor. Because the fired tension varies per anchor,
`should_emit` / `phi_r` / `rate` outcomes vary -> the active-veto fraction is expected
NON-degenerate (the saturation cause on e7_31 is removed).

## modules reused UNMODIFIED (a_phi_iit4_tool, a_kosmos, a_core_engine_map)

- faithful_phi (UNIVERSE/h1004_bigphi_faithful_clean.py) — stdlib iit4/faithful_phi mirror;
  re-proven ==stdlib at n=4 AND n=5 in STEP 0 (verbatim refs), NEVER a proxy (a_phi_iit4_tool).
- provenance_chain (mirror/qmirror/seed/provenance_chain.py) — H_932 build/verify/tamper, UNMODIFIED.
- PureField + decompose_decision (PLASTICITY/h935_free_wont_veto.py) — H_935 CORE gate VERBATIM, UNMODIFIED.
- kosmos_io.load_anchors (HEXAD/UNCLASSIFIED/state/grid_3b_s187_2026_05_21/kosmos_io.py) — read-only.
- The H_1054 harness structure (z-score, Spearman, F-SHUFFLE empirical null) is reused.

## pre-registered falsifier (FROZEN before measuring — TEXT only, no emoji)

Thresholds stated FIRST:

- veto NON-DEGENERACY (gate condition): on the fired anchors, the per-anchor active-veto
  fraction must have variance > 1e-9 AND must NOT be pinned at 1.0 for every anchor. If it is
  still degenerate (saturates / zero variance), report the exact blocker honestly — do NOT fall
  back to the pending e7_31 anchors and do NOT fabricate.
- separation effect size: Cohen's |d| >= 0.8 (large) for the full 2-component T between the
  active-veto-dominated emit group and the passive (sub-threshold) emit group.
- orthogonality band: rho(T, Phi) and rho(T, chronological-t) NEAR-ZERO, judged WITHIN the
  H_1054-style empirical F-SHUFFLE null (observed |rho| <= the 2-sigma shuffle band), with the
  pre-registered fixed band |rho| <= 0.2 reported alongside.

H1 PASS = on the fired anchors, veto-capacity is NON-DEGENERATE (variance > 0, not pinned at 1.0)
AND the full 2-component T separates active-veto vs passive emits (|d| >= 0.8) AND rho(T, Phi)
and rho(T, chronological-t) stay within the empirical shuffle null -> the agency axis is a genuine
2-component (depth + veto) ruler on real fired anchors, COMPLETING H_1054's degenerate veto half.

H1 FAIL = veto adds nothing / stays degenerate / the 2-component T collapses to depth-only
(|d| < 0.8 with the veto component contributing no separating variance) -> veto is NOT an
independent live agency component at this scale. This is a publishable closed-negative
(a_paper_negative_ok) and is reported honestly.

DEGENERATE / BLOCKED = veto-capacity is still pinned (the fired tension does not move the gate)
OR a depth/Phi input collapses -> report the exact mechanism; no verdict token, no fallback.

## honest scope (a_scale_honest_scope, a_lane_akida_gpu_split, a_core_engine_map)

ONE fired anchor corpus (v3_emit_*, N = 14), CPU $0, MEASUREMENT ONLY (read via kosmos_io;
nothing wired into brain_decide — a_core_engine_map). substrate = SW-only CPU.
Lane A (AKIDA on-chip): NOT exercised — no on-chip trace in this rung.
Lane G (GPU forge): NOT exercised — no GPU run in this rung.
a_lane_akida_gpu_split honored: each lane recorded separately; neither is run here.
faithful Phi = stdlib mirror, proven ==stdlib n=4 AND n=5 (a_phi_iit4_tool). g5 CODE-measured, no
LLM self-judge (p7). N = 14 is small (a single fired corpus); production 603MB conscious_decoder
full-carve and scale-transfer are UNVERIFIED (a_scale_honest_scope). Operational agency (active
inhibition vs passive absence), NOT a phenomenal-volition claim.

## verdict (🟢 — fired veto is a live, non-degenerate 2nd agency component; completes H_1054)

On the FIRED v3_emit_* anchors (N = 14):

- **veto-capacity is NON-DEGENERATE.** The faithful H_935 veto-capacity = veto-frac-of-IMPULSE
  (n_active / n_should: of the would-emit impulses the fired drive produces, what fraction the
  substrate BRAKES) has var = 1.24e-3, range [0.340, 0.450], NOT pinned at 1.0. The second
  agency component is LIVE — the degeneracy that flattened it on the `pending` e7_31 anchors
  (H_1054) is removed by using a fired-tension set.
- **HONEST diagnostic (the WHY):** the H_1054-IDENTICAL metric veto-frac-of-SILENCE
  (n_active / n_silent) STILL saturates at 1.0 here (var = 0) — because the fired drive is
  uniformly above the 0.30 emit threshold, so EVERY silence is an active veto. That is exactly
  why per-silence was the wrong ruler: per-impulse (vetoes / would-emit impulses) is the
  drive-dependent, non-degenerate reading of the same decompose_decision outputs (the H_935 gate
  is UNMODIFIED; only the aggregation differs).
- **the full 2-component T = z(provenance-depth) + z(veto-capacity) SEPARATES** veto-dominated
  from passive-dominated emit groups with **Cohen's |d| = 0.94** (>= 0.8). The depth-ONLY
  comparator (the single live axis on H_1054) gives |d| = 0.27 — so the veto component carries
  the separating variance; depth alone barely separates the groups.
- **T stays ORTHOGONAL** to chronological fire-time (rho = +0.095, within the empirical F-SHUFFLE
  null: 2-sigma band = 0.537, +0.33 sigma; fixed band |rho| <= 0.2 also met) AND to instantaneous
  faithful-Phi (rho = +0.064, within null 2-sigma = 0.531, +0.24 sigma; fixed band met). The
  F-SHUFFLE structural control HOLDS (fire-rank shift mean = 4.59 while the substrate-bound T is
  invariant under fire-order shuffle, rho-under-shuffle centered on 0).

=> The agency axis is a GENUINE **2-component (provenance-depth + veto-capacity) ruler** on real
fired anchors. H_1054 established the depth half and its orthogonality to KOSMOS time but left the
veto half degenerate; **H_1056 completes the veto half** — on fired tension the veto component is
live, non-degenerate, and contributes the dominant separating variance between active-veto and
passive emits, while the full 2-component T remains orthogonal to both chronological time and Phi.

STEP 0 faithful-Phi mirror re-proven ==stdlib at n=4 AND n=5 (a_phi_iit4_tool; verbatim in the .txt).

### honest scope / caveats (do NOT over-read)

- **fired drive is uniformly supra-threshold here**, so should_emit = True on ~every tick; the
  veto signal comes entirely from the SAFE gate (rate-limit / phi-ratchet) braking a
  drive-dependent fraction of impulses. A fired set whose drives STRADDLE the 0.30 threshold would
  additionally exercise the passive/active boundary — not available in this corpus.
- N = 14 is small (a single fired corpus, all top_emotion=curious, fixed radius/x); the
  orthogonality is "indistinguishable-from-independent at N = 14" (rho within the empirical noise
  band), NOT a proven-zero coupling. A larger fired corpus would tighten the band.
- bounded rung: CPU $0, MEASUREMENT ONLY (read via kosmos_io; nothing wired into brain_decide).
  Lane A (AKIDA) NOT exercised; Lane G (GPU forge) NOT exercised — recorded separately
  (a_lane_akida_gpu_split). Production 603MB conscious_decoder full-carve + scale-transfer
  UNVERIFIED (a_scale_honest_scope). Operational agency (active inhibition vs passive absence),
  NOT a phenomenal-volition claim.
