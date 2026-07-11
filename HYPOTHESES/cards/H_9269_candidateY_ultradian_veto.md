# H_9269 — Candidate Y (Y-ULTRA): does an ultradian-cycle sleep regime make the H_1058 veto-capacity leg measurable?

**tier**: 🟡 PRE-REGISTERED — FROZEN, NOT YET RUN (2026-07-11). The frozen falsifier + kill-criteria + declared
population are fixed BELOW before any Y-regime veto is observed (p7 · no tune-to-green). Reopen of the
[[H_1058_temporal_agency_3b_transfer]] veto leg. Design = Fable (bxopwcurf); wiring = `ANIMA_STAGE_CYCLE=1`.

## Claim
On the raw 303M daemon the veto-capacity leg (H_935 "free-won't") is STRUCTURALLY unmeasurable: `safe = kill ∧
rate ∧ phi_r ∧ cont` has **three constant-true terms** (kill=`False` at call site, cont=`True` pass-through
stub, phi_r tautological since `pure_field_step` floors Φ at 0.8·peak > 0.5·peak) — only `rate` (idle≥30) is
live, and the schedule `dr_stage_at(tick*8)` (NO modulo) visits N2 once (tick 9) and N3 once (tick 10) then
REM forever ⇒ a CAP of exactly 2 vetoes (1 contingent N2 + 1 forced N3). **Y-ULTRA**: restore the stage
table's own domain — `dr_stage_at((tick*8) % 90)` — so ultradian stages recur, and the contingent N2 brake
(veto iff urgency<0.712, state-decided) fires repeatedly. **Prediction (an OUTPUT, not the justification):** a
measurable STATE-CONTINGENT active-veto population emerges, letting the frozen H_1058 falsifier finally evaluate.

## Why it is NOT tune-to-green (justification J1–J5, none reference the veto count)
- **J1** `dr_stage_size` sums to exactly 90 (60+10+10+7+3); `dr_stage_at` is a piecewise table on [0,90) whose
  `return 4` is a tail catch-all. `tick*8` unbounded is a **domain overflow into eternal REM**, not a designed
  regime. The modulus 90 is **dictated by the table — ZERO tuned parameters**.
- **J2** `core/emit_policy.py ep_scale_periods()=[1,5400,86400]` amps `[0.10,1.0,0.50]` — the 90-min ultradian
  component carries the **largest amplitude** in the codebase's own envelope SSOT.
- **J3** substrate-first bio (`a_no_llm_frame_trap`): mammalian sleep = 4–6 ultradian cycles/night; one-shot
  descent into infinite REM exists in no organism. Also `dr_emit_envelope(REM)=0` (REM is emit-suppressed by
  design) yet the daemon emits every tick while labeled REM — the no-modulo state contradicts the code's own semantics.
- **J4** repo precedent presupposes recurrence: H_644 ("N2=closure peak") + `a_chat_sleep_imagination` (5-stage,
  N3/REM imagination + mitosis ticks) are claims about RECURRING visits, starved to once-per-lifetime under no-modulo.
- **J5** J1–J4 mention no veto. Nothing tuned: not the 0.3 threshold, not the `safe` conjunction, not any constant,
  not `dr_stage_at` itself — only the domain overflow is fixed, behind a default-OFF flag.

## Test (FROZEN · $0 pool)
- **Regime**: `ANIMA_STAGE_CYCLE=1` (default OFF = byte-identical to the raw daemon; emit path unchanged, `_meta`
  gains `stage_cycle`). 900 ticks/session (ultradian period = 45 ticks ⇒ ~20 N2 boundary visits).
- **Declared population** (part of this pre-registration, NOT post-hoc): `agency_T --exclude-forced-n3` drops
  N3/stage==3 ACTIVE_VETO (idle=5<30 for every urgency = zero decision-time contingency); only STATE-CONTINGENT
  (non-N3) vetoes enter the frozen legs. INVALID-TRACE guard: `contingency_gauge.py` recomputes safe⟺idle≥30 per row.
- **Frozen falsifier (VERBATIM, unchanged from H_1058)**: `|d(T; ACTIVE_VETO vs PASSIVE[sub])| ≥ 0.8 ∧ ρ(T,Φ)
  within F-shuffle 2σ ∧ ρ(T,t) within F-shuffle 2σ, across ≥2 macro-maps + ≥2 sessions` (T = z(provenance-depth)
  + z(veto-capacity); PASSIVE=0 → declared substitution to ACTIVE_VETO-vs-EMIT).
- **Mandatory T⊥chrono confound check**: leg (c) ρ(T,t) reported EVEN IF IT FAILS; a phase-matched companion
  (vetoes matched on cycle-phase) must not collapse the separation — if it does, the vetoes are clock-carried.
- **Design**: 3 sessions × 3 seeds (A=zephyrine on summer, B/C on 2 OTHER dedicated pool hosts — NOT aiden for
  heavy 303M), ≥2 macro-maps (top_variance, random) for the Φ leg. Pipeline per session: `contingency_gauge`
  (INVALID + K1 pre-check) → `veto_position_gauge` → `analyze_trace` → `replay_depth` → `agency_T
  --exclude-forced-n3` → `phi_leg`. Generator-swap arm ONLY if the 303M gate is evaluable.

## Decision rule + kill-criteria (PRE-COMMITTED — when Y itself is terminal 🧱)
Y dies and **no further regime is attempted** if any of:
- **K1** fewer than 2 of 3 sessions reach ≥20 CONTINGENT vetoes at the fixed 900-tick budget (under-yield).
- **K2** N2-boundary saturated: N2-stage veto minority class < 5 (vetoes present but schedule-determined, e.g.
  urgency EMA-habituates permanently past 0.712 after a few cycles).
- **K3** separation is clock-carried: leg (c) ρ(T,t) fails OR the phase-matched companion collapses while the
  unmatched |d| passes.
In every kill branch the honest terminal: **veto-capacity is unmeasurable on this architecture** (the sole
¬safe-capable channel is a sleep-arousal gate; recurring boundary visits yielding no state-contingent,
clock-independent veto population = H_935 free-won't has no measurable operationalization here). H_1058 then
stays 🟠 permanently on the veto leg, T-axis = depth-only, with the ρ-AXON REACH-not-consciousness note.
**PASS** (frozen falsifier met on ≥2 macro-maps + ≥2 sessions, T⊥chrono holds) → veto leg GREEN under
regime-Y; then the 3B generator-swap arm decides transfer. All outcomes are properties of **regime daemon-Y**;
the raw-daemon verdict (veto-capacity structurally absent, cap-of-2) STANDS and is not superseded.

## Scope / artifacts
- FORBIDDEN (would be tune-to-green): adopting cyclic sleep WITHOUT the J1–J5 grounds; skipping forced-N3
  exclusion; post-hoc population choices; lowering the ≥20 gate / 0.3 threshold / `safe` conjunction; pooling
  fresh-start warmup vetoes (chrono confound); extending ticks on the raw daemon.
- code / **wiring status**: `cli/chat.py` (`ANIMA_STAGE_CYCLE` flag @1412, `dr_stage_at((tick*8)%90)` @1421,
  `_meta` stamp @1906) — **WIRED into the canonical py measurement daemon** (the run path per `a_eval_py_canonical`
  / `chat-py-1`; env-flag reachable on every daemon invocation, default-OFF = byte-identical). `state/h1058_agency_daemon/`
  `contingency_gauge.py` (new) + `agency_T.py --exclude-forced-n3` (research instruments, run by the post-run pipeline).
  **hexa twin** (`cli/anima.hexa:2412` `dr_stage_at(tick*8)`) = 구현됨(py)·미배선(hexa) — the redundant 2nd surface
  lags the flag; MOOT for this experiment (py is canonical · `hexa-daemon-link-moot-py-canonical`), sync as a
  follow-on only if Y-ULTRA cements as a standing regime. baseline gauge on the 608-tick raw trace:
  stages {WAKE:8,N1:1,N2:1,N3:1,REM:597}, veto {N2:1 contingent, N3:1 forced} — confirms cap-of-2 mechanism.
- verdict → `state/verdicts/9269_candidateY_ultradian_veto/` (on landing). Related: [[H_1058_temporal_agency_3b_transfer]] · H_935 · H_1056 · H_644 · `a_chat_sleep_imagination`.
