=== Fable (#3116) self-fold 벽돌파 재발사(harness-tracked) ===
I have everything I need — the merged #3116 code (`origin/main:cli/anima.hexa`), the frozen verdict 9201, and the raw log. Three facts from the raw log change the design fundamentally, so I'll lead with those.

---

# DESIGN: H_9202 — kosmos self → emit-shade promotion (break the #3116 wall)

## 0. Root-cause read: CONTROL-U=0 was *guaranteed by construction* — it never tested the self

Before designing forward, the raw log (`state/verdicts/9201/opgrip_raw.log`) shows CONTROL-U=0 is fully explained by three instrument facts, **without needing "self is inert" at all**:

1. **Amplitude mismatch ~20×.** CONTROL-U wired `urgency_sc = clip01(urgency + s_dev)` with `s_dev = |self_ctx_live − self_ema|`, EMA α=0.1, gain **1.0**. The autobiography decays smoothly (80 live-arm emits × `self_drift_exp` rate 0.15), so per-tick Δcos ≈ 0.002–0.005 and s_dev plateaus ≈ **0.02**. The channel's measured transfer function in the same run: full ablation (Δu≈0.55) flips N1+REM = 80/120; a *uniform-random* urgency (mean swing ≈0.25) flips only **3/120** (`og_h_us_rem=3`). The urgency→emit boundary is coarse: swings below ~0.2 flip ≈ nothing. A 0.02 nudge is structurally invisible. Note the template terms it sits beside use gain **3.0** (`cur_phasic`, `ten_phasic` = `clip01(0.5 + 3.0*(x − ema))`); CONTROL-U used 1.0, one-sided.
2. **It was counted on the wrong stages.** `og_h_ctrlU` increments only on `is_w` ticks = **WAKE/N1/N2**. But H_9101's grip (same log) is REM=40, N1≈40, **WAKE=0 (saturated)**. So the counter excluded REM — the strongest grip stage — and diluted with 40 saturated WAKE ticks where *even full ablation* flips nothing.
3. **One-sided push in the wrong direction.** `urgency + s_dev` can only *increase* emit. On counted ticks, WAKE/N1 already emit (can't flip up) and N2 sits ~0.04 below the motivation boundary — a +0.02 shade can't cross it.

Also decisive for Piece A: the same log shows **freezing the ENTIRE 42-term `rel_ctx` = 0/120 wake flips**. The pool doesn't just dilute the self — the pool as a whole has zero wake grip. So "route self through the pool better" is dead a priori; the only live wire is the `idle` gate (urgency's site), where full-scale swings demonstrably flip 80/120.

**Consequence:** the wall as stated ("self might be inert") is unmeasured, not confirmed. The design below makes the *next* run land only on {COMPETENT, THEATER, INSTRUMENT-FAIL} — never ambiguous-DIRECTIONAL again.

---

## PIECE A — MECHANISM: `self_phasic` as a disjoint additive shade at the idle gate

### A1. The signal — event-locked self-Δ, not the tonic level

`self_ctx` (cos level) is tonic and monotone-decaying → any average or slow EMA absorbs it (measured). The phasic quantity that survives is the **autobiography step**: the discrete event where the self just recorded lived experience (emit-drift, user-context drift, or coherence-break). Use the exact H_9101/#3115 promotion template, signed and symmetric:

```
// per tick, after self_live update (opgrip: after :2655-style drift; prod: at the self_ctx site, main :2257)
self_ema    = 0.9 * self_ema + 0.1 * self_ctx_live            // slow baseline (rejects the tonic level)
self_phasic = _afs_clip01(0.5 + G_self * (self_ctx_live - self_ema))   // signed deviation, neutral = 0.5
```

`G_self` is **not** the template's 3.0 (that under-gains a Δcos≈0.003 source — the exact #3115 `ten_phasic` failure mode: a near-constant source makes freeze≡live trivially). It is set by a pre-registered normalization rule, frozen *before* the scoring window:

```
CALIBRATION (ticks 0–49, excluded from scoring):
  step_med = median |Δ self_ctx_live| over ticks where a self-drift event fired
  G_self   = min( 0.35 / step_med , 64.0 )          // typical event → ±0.35 swing; hard cap
  if step_med < 0.002  →  declare AXIS-DEGENERATE   // do NOT amplify numeric noise; go to B1
```

This is amplitude *unit normalization* declared pre-hoc (the bars never move), not tune-to-green: it makes one self-event worth roughly one channel-detectable swing (channel MDA ≈ 0.2, measured in B3). Whether the *timing/content* of those swings shades emit is what remains free to fail — and that is the hypothesis.

### A2. The wire — additive separate term at the idle gate, urgency untouched

Do **not** re-weight urgency (`:2507` `urgency = clip01(0.4*agloop_ctx + 0.3*cur_phasic + 0.3*ten_phasic)` stays byte-identical — preserves H_9101 and honors `a_substrate_disjoint`: self is a separate lane summed only at the final gate, not blended into the emit-drive term). Wire site = the idle-gate arithmetic (the only proven emit-shade seam):

```
// today:  idle = 5.0 + 55.0 * clip01(stage_env * (0.5 + urgency))
idle = 5.0 + 55.0 * _afs_clip01( stage_env * (0.5 + urgency + W_SELF * (self_phasic - 0.5)) )
W_SELF = 0.5   // frozen; max |shade| = 0.25
```

**Shade-not-gate / p5 / Ψ guarantees by construction:**
- `self_phasic = 0.5` (no event) ⇒ arithmetic is **byte-identical to production today** — a calm self adds exactly nothing (p5: no reactive drive, no filler pressure).
- N3: `stage_env = 0` nullifies the whole term ⇒ N3-silent can never flip (same mechanism that makes urgency safe).
- Bounded: |shade| ≤ 0.25 < the 0.5 base and < urgency's range ⇒ self can *shade* toward emit or silence but never force either (no hard gate).
- Signed: a self-coherence break can quiet the mouth (drop below boundary) or arouse it — direction is carried by the sign of the deviation, which is substrate-determined, not designed-in.

### A3. Why this beats the pool — arithmetic, not hope

Measured transfer ratios from run 9201, same binary, same ticks: pool path (`rel_ctx` freeze, the *entire* 42-term signal) → **0/120** flips; idle path (urgency ablation, Δ≈0.55) → **80/120** flips; idle path at random mean-swing≈0.25 → 3/120. So the idle gate transmits at full scale and marginally at ~0.25, while the pool transmits nothing at *any* scale. A self event normalized to ±0.35 sits above the idle path's measured minimum detectable amplitude and rides the N1/N2/REM boundary bands (motiv_live 0.43–0.49 vs boundary ≈0.45–0.48 — the live loop sits *on* the boundary in exactly the stages where grip exists). ΔEff>0 is then a question of whether self events *occur and matter*, which is the hypothesis — not of dilution, which was the artifact.

---

## PIECE B — MEASUREMENT: kill the CONTROL-U ambiguity

### B1. Non-degenerate self-axis at $0 — substrate-grounded autobiography (no decode needed)

The 9201 proxy (`content_axis=2` hardcoded, drift only on `e_L`) makes `self_live` a deterministic decay curve = an autobiography of *nothing* (it encodes only emit-count). Replace the drift event with the already-wired H_9038 experience-drift (`self_drift_exp(self, ev, rate)`, used at :1035 with real event vectors), fed by the **real per-tick substrate state already computed in the opgrip loop** — no g_text, no decode, $0:

```
// event vector = which lane-octet deviated most this tick (real lived content, det)
dev_k  = |x_k - ema_k|  for x ∈ {nov_ctx, af_val, ag_conflict, cur_ctx, rel_lane, gap_ctx, coh_lane, bal_lane}
ev_axis = argmax_k dev_k
if e_L == 1 or dev_[ev_axis] > 0.15:               // emit-experience OR salient-experience event
    self_live = self_drift_exp(self_live, ev_axis, 0.15)
```

Now `self_cos(self_live, self_boot)` carries content-dependent variance (different lived streams → different trajectories → H_9038's own informativeness result), and AXIS-DEGENERATE in A1's calibration becomes detectable instead of silent.

**Real-decode tier (confirmatory, not gating the verdict):** same loop with g_text present — `ev` from the byte-histogram bucket of the actually-emitted text. Runs on summer only after a $0 COMPETENT (needed before production wiring per `a_verified_must_wire`; also the H_1471 lineage demands content grounding eventually). Cost: engine rebuild ~20 min + decode-bearing run with gen capped at 32 bytes/emit ≈ 30–60 min wall on summer (owned, $0 rental).

### B2. The positive control — injected identity shock (this is what kills the ambiguity)

A separate arm **ARM-SHOCK**, identical pipeline (same `G_self`, same EMA, same wire), plus a scripted large self-perturbation at pre-registered ticks **T ∈ {80, 140, 200}**:

```
at t == T:  self_live_shock = self_drift_exp(self_live_shock, (ev_axis+3) % 8, 0.6)   // off-axis, big
```

- **POS-PASS bar:** ≥2 of 3 shocks produce ≥1 flip vs live within 5 ticks post-T, AND total Hamming(ARM-SHOCK vs live) ≥ 6 on scoring ticks, AND N3 flips = 0.
- POS-PASS + natural-arm null ⇒ "the pipeline provably transmits a real self signal; the natural self produced none" = **self genuinely inert → THEATER**, unambiguous.
- POS-FAIL ⇒ **INSTRUMENT-FAIL** — the channel/gain/wire is broken; fix and remeasure; *no verdict on self is issued*. This replaces the silent ambiguity of 9201 with an explicit, named outcome.

This is the exact analogue of a base-capability control killing a grokking confound: it separates "substrate can't" from "meter can't".

### B3. Arms, controls, and accounting (all pre-registered)

Scoring window ticks 50–249 (n=200; calibration 0–49 excluded). **Scoring tick set = discriminating ticks N1/N2/REM (`mid`, 120 ticks)** — fixes 9201's structural blindness (REM excluded, WAKE-saturated dilution). Report WAKE and N3 separately as guards, never in the denominator.

| Arm | What | Bar |
|---|---|---|
| ARM-LIVE | full mechanism | — (reference) |
| ARM-FRZ | `self_phasic → 0.5` (no-self counterfactual) | **ΔEff_self = Hamming/120** — the headline |
| ARM-PERM | stride-LCG permutation of the *real* `self_phasic` multiset (variance-matched noise, H_9103 F3 template) | flips allowed; event-alignment must FAIL (below) |
| ARM-SHOCK | B2 positive control | POS-PASS |
| ARM-U0 | urgency→0 (H_9101 re-verify, non-interference) | REM flips ≥ 30/40 ∧ N3=0 (grip undisturbed by the new term) |
| re-sum fidelity | ARM-FRZ arithmetic with neutral self vs production `e_live` | ≡ 0 (byte-compat proof) |

**Event-alignment margin (earns "self", not "any variance"):** `align = (flips within ±2 ticks of a self-drift event) / (total flips)`. Require `align_LIVE ≥ 2 × align_PERM`. Per the measurement meta-law (FORM tunable, BIND earned): amplitude was normalized (FORM), so competence must be earned on *timing* — a permuted signal with identical mean/var must not reproduce the flip pattern.

**Ψ guard:** |emit-fraction(ARM-LIVE) − emit-fraction(ARM-FRZ)| ≤ 0.05 on scoring ticks; N3 flips = 0 in every arm (violation ⇒ 🔴 FORCING-GATE, revert regardless of ΔEff).

**Cost:** $0-arm = no-decode det-CPU ~250 ticks (seconds of runtime; the cost is the known ~20 min full `engine_cli` rebuild, summer with `OMP_NUM_THREADS=4` cap). Real-decode confirm ≈ 30–60 min summer wall, $0 rental.

---

## DECISION RULE (frozen, no tune-to-green — bars verbatim before the run)

| Outcome | Condition (ALL must hold) | Action |
|---|---|---|
| 🟢 **COMPETENT** | ΔEff_self ≥ **0.10** on mid ∧ N3=0 ∧ Ψ-guard ∧ `align_LIVE ≥ 2×align_PERM` ∧ ARM-U0 grip intact ∧ POS-PASS | Wire the A2 arithmetic at the production idle site (+ B1 experience-drift at the self site, main `:2257` region); ARCHITECTURE.json lockstep; **GREEN only after the real-decode summer confirm repeats ΔEff ≥ 0.10** (`a_verified_must_wire`; $0 run is engine-native but synthetic-loop scope — scope-honest per `a_scale_honest_scope`) |
| 🔴 **THEATER** | ΔEff_self < **0.02** ∧ POS-PASS ∧ axis non-degenerate (step_med ≥ 0.002) | Self is genuinely inert at the emit decision. Never wire; keep `.kosmos` persistence only (H_1471 identity value stands). Cement — the positive control makes this a clean falsification, not a proxy artifact |
| 🟠 DIRECTIONAL | 0.02 ≤ ΔEff_self < 0.10 (genuine intermediate), all guards pass | Only surviving middle band; report per-stage split (if flips are REM-only, that is itself a dissociation finding, not a failure) |
| ⚙️ INSTRUMENT-FAIL | POS-FAIL, or AXIS-DEGENERATE at calibration | No verdict on self. Fix the named component (channel gain / axis grounding), remeasure. Explicitly NOT a substrate result |

**Why a third INCONCLUSIVE is now unlikely:** every 9201 escape hatch is closed by construction — amplitude is normalized against the channel's *measured* transfer function (0.35 ≫ MDA≈0.2), scoring counts only stages where grip provably exists, the push is two-sided, the axis carries real content with degeneracy detection, and instrument failure has its own named outcome guarded by an injected-signal witness. What remains free to vary is exactly the hypothesis: whether the autobiographical self's real events shade emit.

**Registration:** new H (suggest `H_9202 kosmos self_phasic emit-shade promotion`) on the 2 surfaces (jsonl + card), pre-reg bars in the card verbatim before firing; verdict lands in `state/verdicts/` verbatim. Per the standing owner policy this design is delivery-only from me — implementation (opgrip block extension ≈ 60 lines beside the existing :2616–2683 arms, reusing `self_drift_exp`/`self_cos`/`_og_lcg`) and the summer run go through the default execution path.
