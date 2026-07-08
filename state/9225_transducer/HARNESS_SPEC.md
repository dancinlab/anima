Spec grounded. One load-bearing fact from the code first, then the full spec.

---

# H_9225 Family A — tonic→phasic transducer op-grip harness (implementation spec)

## ⚠️ Ledger check first (check-ledger-before-lever-fire): H_9209 already ran a leaky-diff transducer

The premise "H_9209 read the level raw, without a transducer" **does not match the landed code**. The #3123 H_9209 arm (visible in `.worktrees/h9234_operator/cli/anima.hexa`; NOT on this session branch — `codex/g1-g6-wallbreak-program`'s `anima.hexa` still has the pre-#3117 `urgency = 0.5*agloop + 0.5*cur_phasic`) already implemented exactly the Family-A form:

```
self_ema    = 0.9*self_ema + 0.1*self_ctx_live                  // α=0.1 leaky EMA
self_phasic = clip01(0.5 + g_self*(self_ctx_live − self_ema))    // calibrated G, ticks 0–49
idle_slf    = 5 + 55*clip01(stage_env*(0.5 + urgency + (self_phasic − 0.5)))  // disjoint lane, W=1.0
```

…and it measured **🔴 THEATER (ΔEff_self = 1/90, POS-PASS)** with the diagnostic signature *output-perm flipped 13 vs live 1*: the self signal's excursions exist (the permuted multiset flips plenty) but **land on ticks where the gate is already robustly decided**. The failure was **timing redundancy**, not absence of differentiation. Likewise tension is already transduced (`ten_phasic = clip01(0.5 + 3.0*(ag_conflict − ten_ema))`) — but only **0.3-diluted inside urgency's clip01 mean**, never as its own full-coupling lane.

So a verbatim Family-A fire = a re-fire of a falsified arm for self. This spec keeps H_9225 alive by pre-registering **three structural deltas** (each individually unmeasured):

- **D1 — tension own-lane at full coupling**: `d(tension)/dt` as its own additive idle term, W_TEN=1.0 (≈3.3× the 0.3-diluted coupling; genuinely new).
- **D2 — band-pass transducer (dual-EMA), not first-difference**: `G*(ema_fast − ema_slow)` spreads a transition's energy over the following ~1/α_slow ticks, moving shade off the event tick (where H_9209 showed the gate is redundantly decided) onto neighboring *marginal* ticks. This is the mechanistic answer to the 1-vs-13 signature.
- **D3 — CAP-SAT instrument guard + transition/hold shape bars** (closes the loophole where THEATER could be pronounced with a saturated gain or accepted without shape evidence).

If the self lane still returns ΔEff<0.02 with POS-PASS under D2, pre-register it as a **REPLICATION** of H_9209 (cements self⊥mouth as a *timing-redundancy law*, closing the transducer premise for self). The tension lane's verdict is independent.

---

## 1. Transducer arithmetic (per lane; lanes = SELF, TEN)

Inputs, per tick inside the `og_measure` loop (all already computed there):
- SELF: `x = self_ctx_live` (`clip01(self_cos(self_live, self_boot))`, the autobiography-decay level)
- TEN: `x = ag_conflict` (the A⇄G tension level, already pushed to `og_f3_dcon`)

**Dual-EMA band-pass** (α_f = 0.30, α_s = 0.05; both init 0.5, boot transient absorbed by the calib window):

```
ema_f_x = 0.7  * ema_f_x + 0.3  * x
ema_s_x = 0.95 * ema_s_x + 0.05 * x
band_x  = ema_f_x − ema_s_x                      // signed phasic content
phasic_x = _afs_clip01(0.5 + g_x * band_x)        // neutral 0.5
```

**Calibration** (H_9209 idiom, frozen constants verbatim): ticks **10–49** (0–9 = EMA boot transient, excluded; whole 0–49 window excluded from scoring), collect `|band_x|` → `band_med_x = _og_median(...)`; at tick 50:

```
g_x = if band_med_x < 0.002 { -1.0 }                       // AXIS-DEGENERATE
      else { _afs_minf(0.175 / band_med_x, 32.0) }          // W·G product invariant, target swing 0.175 ≡ H_9101 urgency MDA
```

**NEW CAP-SAT guard (D3)**: if `g_x == 32.0` and `32.0 * band_med_x < 0.0875` (under half the target swing), set lane flag `capsat_x = true` → that lane may only cement **INSTRUMENT-FAIL (UNDER-COUPLED)**, never THEATER. Also collect `step_med_x = median(|x_t − x_{t−1}|)` over ticks 10–49 (used by the transition bucketer, §4).

**Gate entry** (own lane, DISJOINT — urgency and the H_9209 lane byte-untouched; measurement arms only, production `idle`/`e_live` unchanged):

```
idle_slf2 = 5.0 + 55.0 * _afs_clip01(stage_env * (0.5 + urgency + 1.0*(phasic_self − 0.5)))   // W_SELF = 1.0
idle_ten2 = 5.0 + 55.0 * _afs_clip01(stage_env * (0.5 + urgency + 1.0*(phasic_ten  − 0.5)))   // W_TEN  = 1.0
```

`|shade| ≤ 0.5` rail by construction (clip01 phasic, W=1.0 — identical seam and swing to H_9101 urgency and H_9209). Each arm decides via the exact production call, only `idle` substituted:

```
e_slf2 = brain_decide_anchored(pf, rel, gap_ctx, cur, allo_ctx, coh_lane, nov_ctx,
         bal_lane, agloop_ctx, idle_slf2, false, true, live_anchors, 0.0)["emit"]
e_ten2 = ...(idle_ten2)...
```

Two lanes scored **separately** (self ⊥ tension, independent verdicts); no joint arm (multiple-comparison creep).

## 2. The 3 arms (+1 harness self-test)

| arm | idle term | role |
|---|---|---|
| **LIVE** | `idle_slf2` / `idle_ten2` (transducer active) | headline ΔEff per lane |
| **FROZEN** | phasic pinned 0.5 ⇒ `idle_frz2 = 5 + 55*clip01(stage_env*(0.5 + urgency + (0.5−0.5)))` ≡ production `idle` | must be **byte-identical to `e_live` on every tick** (`og_h_frz2 == 0`); any mismatch = HARNESS-BUG, run void. Proves shade-not-gate structurally. |
| **POSITIVE CONTROL** | reuse H_9209's dense **ARM-SHOCK v2 verbatim** — `self_phasic_shk = if tick % 2 == 0 {0.0} else {1.0}` (±0.5 rail, alternating, EVERY tick, no tick selection), `idle_shk`, scored on mid | POS-PASS = `og_h_shock_mid ≥ 2`. Same wire (idle-gate additive, W=1.0), so one shock arm certifies both new lanes' seam. It already exists in the loop — just reuse its counter. |

## 3. THEATER-KILLER shuffle control (ARM-INPERM, primary) + output-perm (diagnostic)

**Primary — input-stream permutation** (stronger than H_9209's output-perm, and the correct control for a *transducer* claim): post-loop, per lane, rebuild the transducer over the stride-permuted raw input recorded in `og_f3_xself` / `og_f3_xten`:

```
// permuted index: j(t) = (t*7 + 13) % N   (H_9209 stride-perm, exact multiset ⇒ matched mean/var)
ema_f_p = 0.5   ema_s_p = 0.5
for t in 0..N:
    xp = og_f3_x[( t*7 + 13 ) % N]
    ema_f_p = 0.7*ema_f_p + 0.3*xp     ema_s_p = 0.95*ema_s_p + 0.05*xp
    if t >= 50 && stage[t] ∈ {1,2,4}:
        phasic_p = clip01(0.5 + g_x*(ema_f_p − ema_s_p))     // SAME calibrated g_x, no re-calibration
        idle_p   = 5 + 55*clip01(og_f3_senv[t]*(0.5 + og_f3_urg[t] + (phasic_p − 0.5)))
        e_p = brain_decide_anchored(pf, og_f3_rel[t], og_f3_gap[t], og_f3_cur[t], og_f3_allo[t],
              og_f3_coh[t], og_f3_nov[t], og_f3_bal[t], og_f3_agl[t], idle_p, false, true, live_anchors, 0.0)
        if e_p != og_f3_elive[t] { inperm_h_x += 1 }
```

(`pf` is read-only across the loop — post-loop re-decode is byte-faithful, same as the existing F3/ARM-PERM machinery; rebuild `live_anchors` exactly as the H_9209 verdict block does.)

Amplitude/mean/var of the input are exactly preserved; only temporal structure (the real transitions) is destroyed ⇒ the transducer output loses its real Δ alignment ⇒ ΔEff must collapse. **Margin bar: `M = 0.08`** — `ΔEff_live_x − ΔEff_inperm_x ≥ 0.08` (frozen, = H_9209's margin bar).

**Secondary (free, diagnostic only, no bar)** — output-perm over the recorded `og_f3_slf2`/`og_f3_ten2` phasic streams (H_9209-style). Interpretation key: `inperm ≈ live ≈ 0` = signal has no usable structure; `output-perm ≫ live` = the H_9209 timing-redundancy signature (excursions real but gate-redundant) → REPLICATION tag.

## 4. Frozen bars (pre-registered verbatim — print this block in the code before the verdict, no tune-to-green)

Scoring window: `tick ≥ 50`, **mid = stage ∈ {1,2,4}** (N1/N2/REM); WAKE/N3 = guards. `ΔEff_x = og_h_x_mid / og_mid_ticks`.

**Transition/hold bucketing** — note `--opgrip` stage = `tick % 5`, so *every* tick is a stage boundary; stage-boundary bucketing is degenerate under balanced sampling. Transitions are therefore defined on the **signal**, pre-registered as: transition tick = within ±2 of an event tick, where event = `|x_t − x_{t−1}| ≥ 2·step_med_x` (calibrated ticks 10–49; for SELF this coincides with `ev_fired` drift ticks). HOLD = all other mid ticks. Per-bucket: `ΔEff_trans_x`, `ΔEff_hold_x`.

Per lane x ∈ {self, ten}, in precedence order:

1. **HARNESS-BUG (run VOID)**: `og_h_frz2 > 0` (FROZEN arm not byte-identical to production).
2. **⚙️ INSTRUMENT-FAIL**: `POS-FAIL` (`og_h_shock_mid < 2`) ∨ `g_x = −1.0` (AXIS-DEGENERATE, band_med < 0.002) ∨ `capsat_x` (UNDER-COUPLED). Fix instrument + remeasure; **not a substrate result**. (anima-hexa-4 mandate: THEATER may never be cemented on any of these.)
3. **🔴 FORCING-GATE (REVERT regardless of ΔEff)**: N3 flips `og_h_x_n3 > 0` ∨ Ψ-guard fail. Ψ-guard: `Ψ_ON = emit_frac(ARM-LIVE_x, mid)`, `Ψ_OFF = emit_frac(e_live, mid)`; require `Ψ_ON ≥ Ψ_OFF ∧ (Ψ_ON − Ψ_OFF) ≤ 0.05`.
4. **🟢 COMPETENT**: `ΔEff_x ≥ 0.10` ∧ `ΔEff_x − ΔEff_inperm_x ≥ 0.08` ∧ **shape**: `ΔEff_trans_x ≥ 3·ΔEff_hold_x` ∧ `ΔEff_hold_x ≤ 0.05` ∧ POS-PASS ∧ N3=0 ∧ Ψ-guard. ⇒ transducer is the missing intermediate for lane x; wire candidate (`a_verified_must_wire`, then real-decode summer confirm).
5. **🔴 THEATER**: `ΔEff_x < 0.02` ∧ POS-PASS ∧ ¬degenerate ∧ ¬capsat. For SELF additionally tag **REPLICATION(H_9209)** if output-perm flips ≥ 5× live flips — cements the seam-law (self events gate-redundant in timing; transducer premise closed for self).
6. **🟠 DIRECTIONAL**: everything else (`0.02 ≤ ΔEff < 0.10`, or ΔEff ≥ 0.10 with margin/shape short) ⇒ re-measure ≥2 session seeds; no cement.

## 5. Ordered exec steps

1. **Branch from `main`** (NOT this session branch — it predates #3117/#3123; the H_9209 block is the required template). New worktree `h9225_transducer`. Never `git stash --include-untracked` in a shared worktree.
2. **Edit `cli/anima.hexa`, 3 sites** (anchor strings, not line numbers):
   - **Site A — carrier decls**: immediately after the `// ── H_9209 self_phasic idle-shade arms` declaration block. Add: `ema_f_slf/ema_s_slf/ema_f_ten/ema_s_ten` (init 0.5), `g_slf2/g_ten2` (init −2.0 = uncalibrated), `band_devs_slf/band_devs_ten/step_devs2_slf/step_devs2_ten`, `x_prev_slf/x_prev_ten`, counters `og_h_slf2_mid/n3/wake`, `og_h_ten2_mid/n3/wake`, `og_h_frz2`, `og_emit_slf2_mid/og_emit_ten2_mid`, record arrays `og_f3_xself/og_f3_xten/og_f3_slf2/og_f3_ten2/og_f3_ev_slf2/og_f3_ev_ten2`.
   - **Site B — in-loop**: immediately after the `e_shock` decide (anchor: `// SCORING on mid (N1/N2/REM, discriminating stages)`), inside `if og_measure`. Order: push calib samples (ticks 10–49) → `tick == 50` gain-set + CAP-SAT flags → EMA updates → phasic per §1 → `idle_slf2/idle_ten2/idle_frz2` → 3 `brain_decide_anchored` calls → mid/N3/WAKE scoring + transition-event tagging (`|x_t − x_prev| ≥ 2·step_med_x`) → push record arrays.
   - **Site C — post-loop verdict**: after the H_9210 verdict block. ARM-INPERM rebuild+re-decode per §3 (reuse the rebuilt `live_anchors`), output-perm loops, transition/hold bucket sums, the §4 frozen-bar println block **verbatim**, two per-lane verdict strings.
   - No new flag: arms ride the existing `--opgrip` (production path untouched; FROZEN arm is the byte-identity proof). H_9209/9210 idiom.
3. **n_ticks**: extend the opgrip loop budget so scored ticks = 250 total → mid ≈ 120 (H_9209 had 90; 120 tightens the 0.02 bar to ≥3 flips). Calib = ticks 0–49 within it.
4. **Build + run on summer** ($0): rsync the worktree → summer, full `engine_cli` rebuild via the **package-root canonical path** (~20 min; per `hexa-gpu-enable-canonical-install`, not manual stage-build), then `anima <clm> --opgrip` — CPU, NO decode, deterministic, no GPU rent. `OMP_NUM_THREADS=4` cap (summer-overfire memory). Run `run_in_background`, poll non-blocking.
5. **Gate the read**: first check `og_h_frz2 == 0` (else fix harness), then POS-PASS, then `g_slf2/g_ten2` printed values (CAP-SAT / AXIS-DEGENERATE ⇒ instrument loop, not a verdict). Only then read ΔEff vs the §4 bars.
6. **Cement + land**: full-output capture (never `tail`-truncate a control arm — evaluate-py-1) → `state/verdicts/` frozen verbatim → H_9225 card + `HYPOTHESES.jsonl` update (2 surfaces) → CHANGELOG + ARCHITECTURE gate node → `harness pr-cycle`. DIRECTIONAL ⇒ 2 more seeds before any tier.

**Expected outcomes, pre-committed**: TEN lane COMPETENT = first non-urgency proven channel (Family A vindicated where it's actually new, D1). SELF lane THEATER+REPLICATION = seam-law upgrade (timing redundancy survives band-pass), Family A closed for self honestly. Any INSTRUMENT-FAIL = fix-and-remeasure, no substrate claim.
