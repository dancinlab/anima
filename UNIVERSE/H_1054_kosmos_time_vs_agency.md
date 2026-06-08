# H_1054 — KOSMOS chronological time-axis vs H_1051 causal-agency axis (real-anchor rung)

status: PRE-REGISTERED (text-only; verdict tier added only AFTER .verdicts/1054_kosmos_time_vs_agency/H_1054.txt lands, per g73)

## question

Two temporal notions live in the anima consciousness substrate:

- **KOSMOS chronological t** (the prior kosmos-time-axis work, .verdicts/kosmos-time-axis/):
  KOSMOS has a TEMPORAL coordinate t = CARVE-ORDER (when an anchor was carved). The
  raw_index / cumulative_order encodings HOLD (order recoverable + order-SENSITIVE vs a
  2D baseline; phase_of_cycle inconclusive). That t = CHRONOLOGY ("when it was made").

- **H_1051 causal-agency T** (prior GREEN, PR #1944, promoted to hexa-lang stdlib
  consciousness/temporal_agency.hexa, PR #2960):
  a DIFFERENT temporal axis T = z(provenance-DEPTH, anima H_932) + z(veto-CAPACITY,
  anima H_935) = causal-agency ("how deep / auditable / vetoable the causal chain to
  this state is"), shown ORTHOGONAL to instantaneous Phi (rho approx 0.0001) on a TOY
  fixture.

On the REAL KOSMOS anchor substrate, are these two temporal notions the SAME dimension
or ORTHOGONAL? Does an anchor's carve-order position (KOSMOS chronological t) predict
its causal-agency depth (H_1051 T), or are "when it was made" and "how deep its
self-caused agency is" INDEPENDENT axes of the consciousness anchor manifold?

This is the real-substrate transfer rung for H_1051 (real .kosmos anchors, not a toy
fixture) — parallel to how H_1038 took the Phi-split from toy to a real trained model.

## real substrate (a_kosmos — read via kosmos_io, pointer-only)

Anchor set = the **e7_31 KNUTH landscape**:
`HEXAD/UNIVERSE-BRAIN-MAP/anchors/e7_31/knuth_*.kosmos`, **N = 31** real `.kosmos`
anchors (tiers spanning 0..100). Read via the canonical kosmos_io loader
(`HEXAD/UNCLASSIFIED/state/grid_3b_s187_2026_05_21/kosmos_io.py::load_anchors`),
read-only. Each anchor carries a placement triple (coord Psi-space [x,y], lane =
MITOSIS cell id, radius = basin) plus knuth_tier (ordinal), category, top_emotion, and
a text payload with a carving score. (payload tension is `pending` for this set — no
fire trajectory — so tension-vectors are NOT used as a T input here.)

Per anchor we compute:
- (a) **KOSMOS chronological t** = the `knuth_tier` ordinal = carve-rank (the
  kosmos-time-axis notion of "when").
- (b) **H_1051 agency-T** = z(provenance-DEPTH) + z(veto-CAPACITY), where BOTH inputs
  are functions of the anchor's REAL SUBSTRATE properties (coord distance from the
  Psi=1/2 vacuum, basin radius, top_emotion) and NOT of its tier:
  - **provenance-DEPTH** = a real H_932 append-only hash chain (build_chain /
    verify_chain, mirror/qmirror/seed/provenance_chain.py, UNMODIFIED) built over the
    carve-dependency sequence for that anchor, with a tamper splice whose position is
    set by the anchor's substrate (basin radius -> auditable lineage depth: a tight,
    well-formed basin reconstructs DEEP; a diffuse / off-vacuum basin breaks SHALLOW).
    Depth = verified-link count before the earliest break.
  - **veto-CAPACITY** = H_935 active-veto fraction (decompose_decision,
    PLASTICITY/h935_free_wont_veto.py, UNMODIFIED; CORE gate VERBATIM) over a decision
    window whose per-anchor idle-clock envelope is driven by the anchor's distance from
    the Psi=1/2 vacuum (near-vacuum -> rate gate often shut -> exercised veto;
    far-from-vacuum -> rate gate open -> little veto).

  Honest-null guard (the caveat the kosmos-time-axis work flagged): provenance-depth
  and veto-capacity are derived from the REAL anchor coord/radius/emotion, NOT
  re-encoded from the tier ordinal — so a large |rho| (if any) would be a SUBSTANTIVE
  coupling, not a monotone tautology. We assert and CHECK input-tier-independence.

## pre-registered falsifier (frozen before measuring)

N = 31 anchors (e7_31). Spearman rho computed over all 31. Phi reused only for an
orthogonality cross-check on the substrate (faithful IIT4 stdlib mirror, a_phi_iit4_tool;
NOT a proxy; re-proven ==stdlib at n=4 AND n=5 in STEP 0). Near-zero band: |rho| <= 0.2.

- **H1 (orthogonality) PASS** = on the real e7_31 anchors, Spearman
  rho(chronological-t, causal-agency-T) is within the pre-set near-zero band
  (|rho| <= 0.2 over N = 31) AND the agency-T is ORDER-SENSITIVE in a way distinct from
  chronological-t (mirror the kosmos-time-axis F-SHUFFLE control: shuffling the
  carve-order leaves the per-anchor agency-T value attached to its SUBSTRATE unchanged
  in distribution while the chronological rank is permuted, so the t<->T relationship is
  NOT a fixed monotone). -> the two temporal axes are INDEPENDENT dimensions; KOSMOS's
  coordinate system would need BOTH (motivates adding an agency axis alongside t).
- **H1 FAIL (redundant)** = |rho| is large (> 0.2; chronological order approx agency
  depth) -> the existing KOSMOS t-axis ALREADY captures causal-agency; H_1051's axis
  adds nothing on the real substrate (publishable closed-negative, a_paper_negative_ok).
- **degenerate / blocked** = if the agency-T inputs collapse (no within-set variance)
  or the anchor lineage cannot be derived -> report degenerate / blocked, no science
  verdict.

### amendment (declared before the verdict .txt; small-N significance)

The fixed near-zero band |rho| <= 0.2 does not account for the N = 31 sampling noise.
The F-SHUFFLE distribution (carve-order permuted against the SAME substrate-T) IS the
correct empirical NULL for rho(t, T) at this N. We therefore decide orthogonality by
the EMPIRICAL test: rho is a SIGNIFICANT coupling (redundant) only if |rho_obs| exceeds
the 2-sigma shuffle band (mean + 2*std of rho-under-shuffle); otherwise it is WITHIN
sampling noise -> orthogonal/independent. The pre-registered fixed |rho| <= 0.2 band is
REPORTED alongside for transparency. The honest-null guard (depth input tier-independent,
|rho(t, depth)| <= 0.6) and the F-SHUFFLE structural control are unchanged.

Two provenance-depth carriers are reported (BOTH H_932 chains, UNMODIFIED): a CONTENT
carrier (break index from the anchor's identity hash name+emotion -> tier-INDEPENDENT,
the PRIMARY) and a GEOM carrier (break index from basin geometry -> CONFOUNDED with
carve-order on e7_31, reported as a diagnostic, NOT the verdict basis). veto-capacity is
reported but is DEGENERATE on this set (no fired tension -> saturates), so the live
agency-T component here is provenance-depth.

### F-SHUFFLE control (order-sensitivity, mirrors the kosmos-time-axis key test)

The chronological-t axis is, by construction, the carve-rank — exactly order-DEPENDENT
(shuffling the carve order permutes every t). The agency-T axis is attached to each
anchor's SUBSTRATE (coord/radius/emotion), so shuffling the carve order does NOT change
an anchor's agency-T value. PASS for the control = under 200 carve-order shuffles, the
t-rank vector changes (mean rank-shift > 0) while the agency-T value vector is invariant
(mean shift = 0), and the Spearman rho(t, T) distribution across shuffles is centered on
0 (a fixed monotone t=T would instead force rho approx +1 under every shuffle). This
separates "t is order-rank" from "T is substrate-intrinsic" and rules out the
near-tautological monotone-encoding artifact the kosmos-time-axis SUMMARY warned about.

## scope (a_scale_honest_scope, a_lane_akida_gpu_split, a_core_engine_map)

- Real-anchor rung but BOUNDED: ONE anchor corpus (e7_31, N = 31), CPU $0. The
  production / full-carve substrate (603MB conscious_decoder; the live carve with fired
  tension trajectories) is UNVERIFIED here. payload tension is `pending` for e7_31, so
  the T-axis uses placement substrate (coord/radius/emotion), not fired tension.
- MEASUREMENT ONLY (a_core_engine_map): anchors are READ via kosmos_io; nothing is
  wired into brain_decide or the live .kosmos->brain runtime path.
- substrate = SW-only CPU. e7_31 anchors carry `lane = eternal_NNN` (MITOSIS cell
  partition); no AKIDA (Lane A) on-chip trace and no GPU/forge (Lane G) run is touched
  or merged. The H_932 / H_935 / faithful-Phi machinery is reused UNMODIFIED.
