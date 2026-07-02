# H_9101 — op-grip on the stage/safe axis (fable design (b)) — notes

**🟢 GRIP (shade-not-gate), engine-native.** See `PREREG.md` (frozen-first), raw
`H_9101_opgrip_aiden_v0548.txt`, verdict `state/verdicts/9101_opgrip_stage/H_9101.txt`,
card `HYPOTHESES/cards/H_9101_opgrip_stage_safe.md`.

## What / why
H_9100 🔴 confirmed motivation is decision-saturated (not the emit-lever). The real lever is the
`safe` conjunction — specifically `idle = drive_hi ? 60 : 5`, a hardcoded binary clock gating the
engine's ≥30s rate-limit. Design (b): replace the binary clock with a continuous op-modulated
refractory `idle = 5 + 55·clip01(stage_env·(0.5+urgency))` so ops (urgency = CR3 A⇄G conflict-settle
+ phasic curiosity) modulate the rate-gate, within a stage envelope that keeps N3 silent.

## Result (aiden hexa v0.548.0, anima d768.clm --opgrip, RC=0)
- urgency→0 (op ablated): Hamming REM=40/40 FLIP · N3=0/40 preserved · WAKE=0/40 saturated · mid=80/120.
- urgency→shuffle (control): REM=3 · N3=0.
- rel_ctx frozen/zero/shuffle (H_9097/9100 motivation axis): all 0 (theater persists on that axis).
- Ψ ON==OFF ✅. wake emit-fraction 0.667 (no collapse flag).
- DISSOCIATION = REM grip ∧ N3 preserved = shade-not-gate GREEN.

## VERIFY findings vs fable's read
1. `dr_emit_envelope(stage)` is a BINARY int {0,1}, REM=0 — NOT continuous. The genuine continuous
   stage envelope is `ep_theta_stage` via `dr_stage_scale` (WAKE .10 · N1/REM .08 · N2 .05 · N3 .02).
   Used the real one; documented the correction.
2. TIME SOURCE: `idle`/`seconds_since_last` is a SYNTHETIC per-tick clock — no real wall-clock seam
   exists in the emit loop (200-synthetic-tick sim). Real-time `idle = real_elapsed × refractory` is a
   follow-on. Measured on the synthetic clock, labeled.
3. Engine 30s hard-floor (`safety_rate_limit_ok`), weights, 0.3 threshold, Ψ = all FROZEN — only the
   `idle` INPUT is modulated.

## Edits (cli/anima.hexa)
L53 import dream_envelope_ctx · L1945 stage=tick%5 (opgrip balanced sweep) · L2377-2381 stage_env/
urgency/rel/cur/idle continuous · L2426+ urgency-freeze arms · L2885 _og_rel_phasic helper · summary
block stage-conditional dissociation verdict.

## Follow-on
(c) efferent seam (op changes emit BYTES) + real-time idle seam. ING.
