# H_9100 — op-grip: promote 4 filler constants to live op reads + tonic-phasic (fable design (a))

**tier:** 🔴 RED / AT-FLOOR (engine-native) · **wired:** WIRED-live (inputs), decision-INERT
**verdict:** 🔴 AT-FLOOR — grip NOT achieved; theater NOT broken for op (a).

## Claim (fable design (a) — the CAPSTONE grip=0 fix)
The CAPSTONE (this session, engine-native) confirmed the daemon emit/silence decision has **grip=0** from op context: `rel_ctx` ÷43 dilution + a motivation FLOOR ≥ the 0.3 threshold ⇒ Hamming 0/200 under `rel_ctx` ablation (THEATER). fable design (a): give ops real grip by promoting the 4 constant `brain_emit` args (`gap=0.6, pain=0.0, orig=0.5, dyn=1.0`) to **live op reads** + **tonic-phasic normalization** on `rel`/`cur`. Engine (`core/engine_g.hexa`/`core/brain.hexa`), weights, and the 0.3 threshold FROZEN — only `cli/anima.hexa` call-site inputs change.

## Wiring (cli/anima.hexa only — 156 ins / 8 del)
- `gap` ← `clip01(1−rel_lane)` (L1922 recall) · `pain` ← `allo_ctx` (L2254) · `orig` ← `nov_ctx` (L2122) · `dyn` ← `agloop_ctx` (L1961 CR3 A⇄G settle).
- Promoted ops de-pooled: `rel_ctx` ÷43→÷42 (−`agloop_ctx`), `cur_ctx` ÷19→÷18 (−`nov_ctx`).
- Tonic-phasic (PREREG-frozen α=0.1, gain=3.0): `rel/cur = clip01(0.5 + 3·(x − ema))`, drive_hi sleep-mask preserved.
- Always-on emit-rate collapse FLAG (detector, not a target) + `--opgrip` 5-arm measurement mode.

## Result (engine-native, aiden `hexa v0.548.0`, RC=0, `mouth=clm loaded=true` d768.clm, NO numpy)
`state/verdicts/9100_opgrip_motivation/H_9100_engine_native.txt` (verbatim) · raw `state/opgrip_motivation/H_9100_opgrip_aiden_v0548.txt` · pre-reg `state/opgrip_motivation/PREREG.md`.

| arm (post-fix, 200 ticks, wake=10) | Hamming vs live | pre-reg | outcome |
|---|---|---|---|
| full-rel_ctx frozen | 0 (wake 0/10) | ~75% | MISS |
| single-op agloop frozen | 0 (wake 0/10) | ~55% | MISS |
| rel_ctx→0 / shuffle | 0 / 0 | — | MISS |
| baseline pre-fix (rel-frozen) | 0 | 0 (theater) | ✓ reproduced |
| sleep ticks (190) | 0 | 0 (rate-blocked) | ✓ |

- **No regression**: `e_base == e_live` on ALL 200 ticks (wiring changes motivation VALUES, not the emit DECISION).
- **Ψ ON==OFF invariant ✅** · **collapse FLAG fired** (wake emit-fraction = 1.0).

## Honest verdict (PREREG RED rule — VALID terminal, NO tuning of α/gain/threshold)
🔴 **AT-FLOOR: "phasic normalization still doesn't reach the threshold band = threshold-statistics mismatch is the real wall."** Promoting the constants to live ops + 3× phasic pull-down moved wake motivation ~0.735(base)→~0.62–0.73(live) — still **0.32–0.44 ABOVE** the 0.3 threshold. Wake band (~0.62–0.74) and sleep band (~0.35) both sit on ONE side of 0.3; the emit boolean is determined ENTIRELY by the `safe` conjunction (stage→idle→`safety_rate_limit_ok`). Empirically confirms CAPSTONE layers 2+3: the 8-factor motivation is a saturated dashboard; the decision is a stage-driven rate gate. Op dilution was NOT the sole wall — even undiluted live ops with 3× phasic don't straddle.

## Value landed + next lever
LANDS (RED lands, a_break_the_wall): (1) removes hardcoded filler constants → the 8 factors are now genuinely context-driven (a_autonomy_over_hardcode / a_substrate_native_speak literal), decision-neutral & Ψ-safe; (2) definitively localizes the wall to threshold-statistics / `safe`-seam; (3) permanent collapse detector + `--opgrip` diagnostic. **Next lever = NOT input-side**: fable #2/#3 **efferent seam** (deliberate best-of-K emit-byte change · winner-take-all replacing the ÷42 average) where an op moves the OUTPUT, not a boolean already saturated above threshold. ING efferent (c).
