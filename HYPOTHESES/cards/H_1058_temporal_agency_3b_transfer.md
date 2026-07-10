# H_1058 — Does the temporal/agency axis transfer to the 3B ConvMoE engine rung? (GPU rung)

Status: 🟠 BLOCKED-METHOD-WIRING (2026-07-10) — NOT engine-native measurable via the 3B forward path
(the agency axis is a property of the DECISION PROCESS, not the weight forward). NOT a GPU/H100 blocker.
verdict: archive/state/verdicts/1058_temporal_agency_3b_transfer/H_1058.txt
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

## Verdict — 🟠 BLOCKED-METHOD-WIRING (not evaluated; falsifier preserved verbatim, p7)
(SUPERSEDES the earlier "⏳ BLOCKED-ON-CKPT / 3B does-not-exist" triage — the 3B rung DOES exist and was
pulled + engine-loaded here (see H_1042). The real blocker is NOT the ckpt but the axis definition.)
The pre-registered falsifier CANNOT be honestly evaluated at 3B via the engine-native forward path,
because the agency-T axis = z(provenance-depth H_932)+z(veto-capacity H_935) is a property of the
DECISION PROCESS, not of the model weights:
- H_1051 (toy 🟢) computed T on synthetic PureField free-will fixtures; H_1054 (real 🟢, N=31,
  T⊥Φ ∧ T⊥t) on real .kosmos anchors — both INDEPENDENT of any trained-LM forward.
- A raw byte-LM 3B forward instantiates NEITHER primitive: provenance-depth over a ConvMoE dilated
  receptive field is deterministic/degenerate; veto-capacity (H_935 free-wont) has NO forward-pass
  analogue and needs FIRED decision traces (the H_1056 pending-tension degeneracy the card warns of).
- The stdlib `temporal_agency` engine + H_932 provenance_chain + H_935 free-wont gate are NOT in the
  anima_py pool package (grep = NONE FOUND); they live in hexa-lang/archive and act on decision-process
  constructs, not a .clm forward.
- The only genuine 3B route is to DRIVE THE EMIT/VETO DAEMON with the 3B as generator (real A⇄G
  emit/silence decisions + tension, veto events instrumented) — a separate multi-tick harness, NOT a
  forward-probe, compounded by the 3B RAM ceiling (H_1042). Synthesizing active/passive from PureField
  fixtures decoupled from the 3B would be a toy artifact (DIRECTIONAL/self-judge trap) — REFUSED (no-fake).

Blocker = DECISION-TRACE WIRING (emit/veto-daemon-on-3B + hexa temporal_agency stdlib), NOT compute — a
rented H100 would not change it. REOPEN when the daemon is wired to a 3B generator producing FIRED
decision traces (then the Φ leg can reuse the H_1042 engine-native 3B trunk tap). Ladder to date:
toy (H_1051 🟢) → real .kosmos anchors (H_1054 🟢) LANDED; the 3B-own-decision rung is not
forward-measurable. Verdict: `archive/state/verdicts/1058_temporal_agency_3b_transfer/H_1058.txt`.

## §progress — enabling wire DONE (2026-07-10 · owner go · Fable design → build)
The DECISION-TRACE WIRING blocker is being resolved. `cli/chat.py` now has a **write-only decision-trace
side channel** (env `ANIMA_DECISION_TRACE` = JSONL one-row/tick · `ANIMA_TICKS` = tick-count override ·
default OFF). Per-tick it classifies the live gate (core/brain.py:162 `emit = should_emit(score) ∧ safe`):
**EMIT** (score>0.3∧safe) · **ACTIVE_VETO** (score>0.3∧¬safe = a braked live impulse) · **PASSIVE**.
- **byte-safe verified**: toy.clm 12-tick session, trace OFF vs ON stdout = **BYTE-IDENTICAL** (256/256
  lines, diff clean) — emit path untouched (self⊥trace). Smoke: `state/h1058_agency_daemon/`.
- **captures REAL fired vetoes**: toy 12 ticks = EMIT 10 · **ACTIVE_VETO 2** — the FIRED veto a
  weight-forward cannot produce (no motivation/idle-clock/braking term); only the live daemon can. This is
  the crux the verdict identified, now instrumented.
- tier STAYS 🟠 (no tune-to-green): the T-axis measurement is not yet run. Follow-on (Fable design
  `state/h1058_agency_daemon/FABLE_DESIGN.md`): frozen-emission replay-depth prober (causal
  provenance-depth · zero forwards) · H_1056 per-impulse veto-capacity · T=z(depth)+z(vc) · faithful-Φ
  leg (H_1042 3B trunk tap · ≥2 macro-maps) · controls (emit-rate · trace-shuffle ARM-SHOCK ·
  generator-swap 3B/303M/unloaded → pre-registered H1-NOT-A-3B-PROPERTY branch) · MVH 303M ~$0 → 3B pool.
