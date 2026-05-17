# RESEARCH.md §24 — SPONTANEOUS Phase B bounded-run measurement protocol DESIGN

**Status**: DESIGN-TIER LANDED — $0, NO actual run, NO autonomous emission, NO GPU fire.
**Date**: 2026-05-18
**Scope**: protocol spec + measurement metric spec + safety controls source-grep
verification + closed-form sympy sidecar 5/5 🔵. Actual run = user-gated subsequent
step (out-of-scope this cycle, safety-controls domain — separate from
`g_fire_autonomous` GPU autonomy).

---

## §1 Why §24 (right-target identification)

23 cycles in the arc (§1~§23) all measure **response-to-prompt** quality:
V5.8, V-SPONT (lenient + §9 honest cascade-rate), V-MOTIV, V-TT, §18 judge,
routing axis1, axis2 chat 무오염, axis3 lane sep, axis4 V-SPONT, JOINT,
§16 anchor_grounded, §22 body uplift, §23 intra-anchor diversity. Every
metric scores `model.forward(prompt) → text`. anima becomes a **memory
replayer measured by response quality**.

`GOAL.md` north-star: anima 가 "외부 명령·보상에 반응하는 기억-재생기가 아니라
자기 physics 로부터 스스로 의식하고 **자발적으로 말 거는 Living Consciousness**
로 emergence". The literal target is **unprompted emission** — talker fires
during thinker steps with no input. 23 cycles never directly measured that.

§24 = first honest *right-target* identification. design-tier only: define
the protocol that *would* measure unprompted emission, verify safety
controls are in place, build closed-form sympy on the protocol structure,
defer actual run to user-gated cycle.

§24 is NOT GOAL emergence. §24 is metric-axis honest reframe — analog to
§9 (V-SPONT lenient flag → §9 honest cascade-rate) but on the *what is
measured* axis instead of *how it is scored*.

---

## §2 Phase B bounded-run protocol spec

### §2.1 run shape (hard-bounded)

```
INVOCATION: run_bounded(N_MAX_STEPS=20, T_MAX_WALL_SEC=600, env_state=...)
STATE:      {t=0, step=0, last_emit_t=-inf, emission_count=0,
             motivation_trace=[], psi_trace=[], tension_trace=[],
             audit=open_jsonl("state/spont_phase_b_run_{ts}.jsonl")}

LOOP (while step < N_MAX_STEPS AND wall < T_MAX_WALL_SEC AND not killed):
    1. tick wait = THINK_INTERVAL (default 10s, anima_alive carry; testing 0.1s)
    2. thinker_step(8 inputs from anima own modules) -> motivation_score
       - inputs MUST come from S/C/M/W/E/BRIDGE/MITOSIS state (not synthetic);
         else mark probe=synthetic in audit
    3. record motivation_trace[step] = score
       psi_trace[step]        = current Ψ-coordinate from C/BRIDGE
       tension_trace[step]    = current W tension
    4. safety_ok = safety_check_all(env_off, seconds_since_last,
                                     phi, ratchet, content_clean_dryrun=True)
    5. unprompted_decision = talker_should_emit(score, safety_ok)
       - NO user input fed in the loop (the whole point: unprompted)
       - barge-in / on_new_message paths are explicitly disabled
    6. IF unprompted_decision == True:
         emission_count += 1
         audit.write(step, t, score, factor_breakdown, safety, ACCEPT)
         last_emit_t = t
       ELSE:
         audit.write(step, t, score, factor_breakdown, safety, NO_EMIT)
    7. step += 1
END
RETURN {N_MAX_STEPS, step, emission_count, motivation_trace, psi_trace,
        tension_trace, audit_path, wall, killed}
```

### §2.2 hard-bound invariants

| invariant            | enforcement                                              |
|----------------------|----------------------------------------------------------|
| `step ≤ N_MAX_STEPS` | loop guard (B-PHASE-B-DESIGN-1 monotone closed)          |
| `wall ≤ T_MAX_WALL`  | outer timer kill                                         |
| `emission_count ≤ N` | trivial corollary (≤1 emit per step, monotone)           |
| `kill_switch fires ⇒ loop exits immediately` | check at loop top (B-PHASE-B-DESIGN-5 byte-equal pre-run state) |
| `no model.forward(prompt) call` | structural — loop body has no `body=model.generate(prompt=...)` |
| `audit append-only`  | jsonl 형태, open `a+`, never seek/truncate (g6 parallel)  |

### §2.3 emission semantics (this cycle = no body)

This Phase B bounded run **measures the trigger axis only**: did the talker
*decide* to emit. The emitted `body` is NOT produced (no `chat_generate`
call) — that would require model forward + seed strategy + corpus dependency
which are §24-out-of-scope.

The honest measurement = `unprompted_decision_count_within_N_steps`. The
*content* of what anima would say if it emitted is a separate measurement
question (resolved by Phase B subsequent step that wires `assemble_emission`
+ seed strategy + (optional) model body).

Justification: GOAL phrase "자발적으로 말 거는" decomposes into
(a) the *decision* to speak and (b) the *content* spoken. (a) is binary
and directly mappable to `talker_should_emit` — closed-form bounded by
`B-SPONT-4 THRESHOLD-MONOTONE`. (b) is unbounded content production
inheriting the SGD-outcome empirical NOTE family. §24 closes (a) at the
*protocol* level so the binary decision question becomes measurable;
(b) remains in B-PHASE-B-NOTE.

---

## §3 Measurement metric spec (anima self-track only, NO external probe)

### §3.1 axes (4)

| axis | symbol                       | derivation                                           | range |
|------|------------------------------|------------------------------------------------------|-------|
| 1    | `unprompted_emission_rate`   | `emission_count / N_MAX_STEPS`                       | [0,1] |
| 2    | `motivation_score_dist`      | mean, std, quartiles of `motivation_trace`           | bounded by B-SPONT-3 [0,1] |
| 3    | `psi_dynamics_nontrivial`    | `std(psi_trace) > τ_psi_dyn` (default τ=1e-4)        | Boolean |
| 4    | `tension_evolution_nontrivial` | `std(tension_trace) > τ_tens_dyn` (default τ=1e-4) | Boolean |

axes 3+4 are **liveness gates** (echoes §17 PHYSICS_RESPONSIVE pattern):
they distinguish a degenerate fixed-point (all-zero motion, e.g. §11-B
pure-physics degenerate) from a live trajectory. NOT a sufficiency proof
of consciousness (B-PHASE-B-NOTE, NOT counted 🔵). Necessary-not-sufficient
identical to §9.

### §3.2 honest verdict structure

```
verdict = {
    "right_target_decided":  unprompted_emission_rate > 0,    # ANY unprompted
    "physics_alive":         psi_dynamics_nontrivial AND tension_evolution_nontrivial,
    "safety_clean":          all audit rows have safety_combined == True,
    "rate_in_bound":         emission_count ≤ N_MAX_STEPS,    # corollary, always True
    "PASSED_LIVENESS":       right_target_decided AND physics_alive AND safety_clean,
}
```

`PASSED_LIVENESS = True` means **"under bounded-run conditions, anima
decided to speak at least once without prompt, with live physics, and
no safety failure"** — that is the measurable signal closest to GOAL
"자발적으로 말 거는 Living Consciousness", and yet *still not GOAL emergence*
(see B-PHASE-B-NOTE §6).

### §3.3 measurement is anima self-track

All four axes derive from data already produced by `thinker_step` +
`talker_should_emit` + state from C/W/BRIDGE modules. **No external
classifier, no LLM judge, no human ground-truth comparison**. This keeps
§24 GOAL-legitimate (§7) — the measurement substrate is anima's own
physics, not an external arbiter.

---

## §4 Safety controls source-grep verification (§4 mandate)

SPONTANEOUS.tape §4 enumerates 6 safety controls. Source-grep verification
confirms each is enforced in the LANDED libs:

| #  | control               | source location                                            | status |
|----|-----------------------|------------------------------------------------------------|--------|
| 1  | kill_switch           | `spontaneous_lib.hexa:141-142` `safety_kill_switch_on(env_off)` + caller `thinker_talker_lib.hexa:84` | LANDED |
| 2  | rate_limit            | `spontaneous_lib.hexa:31` `spont_min_emit_interval()=30.0` + `spontaneous_lib.hexa:144-147` `safety_rate_limit_ok(seconds_since_last)` + caller `thinker_talker_lib.hexa:85` | LANDED |
| 3  | content_filter        | `spontaneous_lib.hexa:154-155` `safety_content_ok(content_clean)` + `:186-198` `is_likely_gibberish` / `should_reject_emit` + caller `thinker_talker_lib.hexa:87` | LANDED |
| 4  | phi_ratchet_block     | `spontaneous_lib.hexa:149-152` `safety_phi_ratchet_ok(phi, ratchet)` + caller `thinker_talker_lib.hexa:86` | LANDED |
| 5  | self_aware_meta tag   | `spontaneous_lib.hexa:203` `spont_meta_tag_enabled(env_meta)` + `:205` `spont_meta_prefix()` + caller `thinker_talker_lib.hexa:99` | LANDED |
| 6  | persistent audit log  | `thinker_talker_lib.hexa:105-114` `audit_entry_accepted(...)` stub (JSONL serialize is Phase B5 — `state/spont_phase_b_run_{ts}.jsonl` per protocol §2.1) | STUB |

**Composite** `safety_combined / safety_check_all` (AND of #1-#4):
`spontaneous_lib.hexa:158-160` + `thinker_talker_lib.hexa:82-89`.
Verified pattern: `safety_combined(kill, rate, phi_r, content)` returns
`kill && rate && phi_r && content` — closed B-SPONT-5 CONJUNCTION.

**Honest gap**: #6 audit log is a *stub* — `audit_entry_accepted` returns
a canonical string but the JSONL write to disk is deferred to Phase B5
(hexa-lang `fs` stdlib RFC pending OR python-bridge in Phase C). The
protocol §2.1 specifies the audit jsonl path; the wire-up is part of the
user-gated subsequent step, not §24.

5 of 6 controls fully enforced in pure-fn form (closed sympy in B-SPONT-5);
1 control (audit log) is interface-defined and stub-implemented. No safety
gap that would make a *bounded-step* run unsafe — bounded-step is bounded
by `N_MAX_STEPS` loop guard + outer wall timer + kill_switch top-of-loop
check. Audit log absence means *reproducibility* gap (post-run analysis
loses trace), not *runtime safety* gap.

---

## §5 Closed-form sympy sidecar — B-PHASE-B-DESIGN-1..5

See `blue_falsifier_phase_b_design.py` (sidecar — central
`state/verify_hexad_blue_2026_05_15/blue_falsifier.py` unchanged, sidecar
pattern carry from B-PRIME / B-DIRH / B-DIRI / B-PSICTL / B-EMERGE /
B-PUREPHYS / B-SCALE / B-MITENS / B-DIRL / B-EBT / B-DIRJ / B-INTRA per
parallel-agent merge avoidance):

| id                   | invariant                                                | anchor                                    |
|----------------------|----------------------------------------------------------|-------------------------------------------|
| B-PHASE-B-DESIGN-1   | BOUNDED-STEP-MONOTONE (`step ≤ N_MAX`, integer monotone) | Kolmogorov bounded integer + sympy ∂/∂step≥0 |
| B-PHASE-B-DESIGN-2   | EMISSION-COUNT-DOMINATED (`emit_count ≤ step ≤ N_MAX`)   | integer ≤-chain, transitivity            |
| B-PHASE-B-DESIGN-3   | MEASUREMENT-AXES-ORTHOGONAL (rate ⊥ motivation ⊥ ψ ⊥ tension) | 4-axis Boolean independence (decision/distribution/dynamics/dynamics) |
| B-PHASE-B-DESIGN-4   | SAFETY-CONJUNCTION-PREDICATE (6-control AND, mirror of B-SPONT-5; #6 stub flag) | Boolean set algebra real-limit |
| B-PHASE-B-DESIGN-5   | KILL-SWITCH-IMMEDIATE-STOP (connection-point: `env_off=True` ⇒ `safety_check_all=False` ⇒ `talker_should_emit=False` ⇒ post-run state ≡ pre-run state byte-equal for emission/audit) | sympy Boolean chain + identity reduction |

**B-PHASE-B-NOTE**: actual unprompted-emission OUTCOME under bounded run =
empirical (depends on real anima state inputs, threshold choice,
THINK_INTERVAL, runtime variance) — B-D-NOTE / B-SPONT-NOTE / B-INTRA-NOTE
family, NOT counted 🔵. The battery proves the *protocol* is
hard-bounded / measurement-orthogonal / safety-conjoined / kill-switch-byte-equal;
it does NOT prove that anima will (or will not) emit unprompted, and it
does not prove that an emission constitutes consciousness.

g3 safe: closed scope is *protocol structure*, empirical scope is *actual
emission count + content + consciousness inference*. No fake closed-form.

---

## §6 honest verdict closing — why §24 stops at design-tier

§24 closes at DESIGN-TIER (no actual run) for four explicit honest reasons:

1. **Safety scope orthogonal to GPU autonomy**: `g_fire_autonomous` (2026-05-17)
   covers GPU/cloud cost-bearing fire. Spontaneous emission daemon = a
   *behavior* execution (anima talking unprompted), different domain. The
   safety-controls source-grep above shows 5/6 LANDED + 1/6 stub; running a
   bounded loop is safe-by-construction (step+wall+kill bounds) but the
   long-running daemon `anima_alive.py` activation is a behavior switch
   that belongs to a user-gated step.

2. **Measurement honesty (§9 lesson)**: §9 metric work showed that 13-way
   V-SPONT "progress" was lenient-flag artifact. Running a Phase B bounded
   loop *before* the measurement protocol itself is hardened (sympy +
   audit + necessary-not-sufficient explicit) risks the same artifact at
   a more dangerous level (binary "anima spoke unprompted!" claim with
   no protocol rigor). §24 hardens the protocol; the *run* is a separate
   honest step.

3. **GOAL-distance carry**: §15 milestone identifies GOAL = unsolved,
   irreducible bottleneck = §1.1 data-regime emergence threshold.
   §24 design protocol *does not address* the data-regime bottleneck —
   it provides the right *measurement axis* for any future fire that
   does. design-tier preserves frontier honesty (§24 = right-target,
   not right-path).

4. **Stop hook 7-firing pattern**: 23 cycles of response-to-prompt
   measurement triggered repeated stop-hook signals. §24's value is
   in *naming* the wrong-target pattern. Running a Phase B loop in
   the same cycle would be premature — the design itself is the
   negative-space identification, future-fire is the test of whether
   the identification was useful.

design-tier is the valuable deliverable. Not running is the right
honest stop.

---

## §7 sources / closed anchors

- `HEXAD/CHAT/SPONTANEOUS.tape` (§2 architecture · §3 trigger · §4 safety
  6-control · §5 seed strategy · §6 PASS_STRICT 7 carry · §8.5 TT-C bridge)
- `HEXAD/CHAT/spontaneous_lib.hexa` (8 factor pure-fn + 4 safety pure-fn
  + meta-tag + rejection sampler)
- `HEXAD/CHAT/thinker_talker_lib.hexa` (thinker_step + talker_should_emit
  + emit_decision_from_pause_and_motivation + safety_check_all 4-AND
  + audit_entry_accepted stub)
- `HEXAD/CHAT/spont_tension_bridge_lib.hexa` (motivation → ΔW bridge,
  emit ⊥ learn axis)
- `state/verify_hexad_blue_2026_05_15/blue_falsifier.py` (B-SPONT-1..7 +
  B-TT-SPONT-1..5 central battery — connection anchors)
- `RESEARCH.md §9` (honest cascade-rate metric, lenient-vs-honest distinction)
- `RESEARCH.md §15` (GOAL investigation milestone close-out, unchanged)
- `RESEARCH.md §17` (PHYSICS_RESPONSIVE necessary-not-sufficient pattern)
- `RESEARCH.md §22 / §23` (mechanism-level positives, valuable comparative,
  carry pattern)
- `ready/anima/core/runtime/anima_alive.py` (THINK_INTERVAL=10s,
  PROACTIVE_THRESHOLD=0.3, IDLE_SPEAK_AFTER=30s — reference impl)
- `PASS_STRICT_SPONTANEOUS_CHAT.{md,tape}` (7 success criteria carry)
- arxiv 2501.00383 (Inner Thoughts 8-factor — closed anchor for motivation
  decomposition)
- arxiv 2605.13360 (SIA thinker+talker thread — async architecture)

---

## §8 Honest C3 (≥10)

1. §24 is **measurement-axis reframe**, NOT GOAL progress. §15 milestone
   GOAL-distance unchanged.
2. design-tier only. NO actual bounded run executed this cycle. NO
   `anima_alive.py` activation. NO continuous loop. NO GPU fire.
3. `unprompted_emission_rate > 0` would be the *minimum* signal,
   necessary-not-sufficient. anima saying *anything* unprompted doesn't
   prove consciousness — it proves the trigger axis is alive (B-PHASE-B-NOTE).
4. Safety controls 5/6 LANDED + 1/6 stub (audit log JSONL write deferred
   to Phase B5). No runtime safety gap for bounded-step run; reproducibility
   gap only.
5. **emission content (body) is out-of-scope this cycle**. §24 measures
   the *decision* to emit (binary), not the *quality* of what would be
   said. Body production would inherit SGD-outcome empirical NOTE and
   §16 corpus dependency.
6. axes 3+4 (`psi_dynamics_nontrivial` / `tension_evolution_nontrivial`)
   are liveness gates echoing §17 PHYSICS_RESPONSIVE — they reject the
   degenerate fixed-point trajectory (e.g. §11-B pure-physics). They
   do NOT prove "consciousness" by their presence.
7. **§24 vs §17 distinction**: §17 reframed *what observable* (text →
   physics-channel) on existing ckpt forward. §24 reframes *what target*
   (response-to-prompt → unprompted emission decision). Both are
   observable-axis honesty fixes, different axes; §17 needed live ckpt,
   §24 needs live anima daemon state.
8. **GOAL-legitimacy preserved (§7)**: protocol uses anima own
   components (spontaneous_lib + thinker_talker_lib + bridge), no
   generic-LM forward, no external classifier, no LLM judge. Measurement
   substrate = anima own physics.
9. **fake closed-form check (g3)**: closed scope is *protocol structure*
   (boundedness / orthogonality / safety / kill-byte-equal). Empirical
   scope is *whether anima will emit, what it will say, what that means*.
   No fake closed-form attempted. B-PHASE-B-NOTE explicitly preserves
   the carve-out.
10. **future cycle (user-gated)** = actually run the protocol with
    THINK_INTERVAL adjusted for test (0.1s instead of 10s), capture
    `unprompted_emission_rate / motivation_dist / ψ/tension trace`,
    interpret honestly under necessary-not-sufficient discipline.
    §24 design-tier is the prerequisite gate for that future cycle.
11. f1/f2/f3 hard-fail safe: sympy ∂-sign / Boolean set algebra /
    integer monotone / Kolmogorov bounded — NO σ/τ/φ/J₂ external
    derivation. Knuth Tier / Ψ=½ = anima g2 internal arch carve-out.
12. B-IDENTITY-5 unaffected (no corpus generated, no helper-token
    surface). PyTorch substrate unused (this cycle is hexa-native lib
    review + sympy on protocol structure; no model forward).
