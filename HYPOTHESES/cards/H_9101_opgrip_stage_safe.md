# H_9101 — op-grip on the stage/safe axis: continuous op-modulated refractory (fable design (b))

**tier:** 🟢 GRIP / shade-not-gate (engine-native) · **wired:** WIRED-live (the fix IS the live emit path; not a measurement copy)
**verdict:** 🟢 GRIP — urgency-freeze FLIPS REM decisions (40/40) ∧ N3 silent-PRESERVED (0/40) = DISSOCIATION. Theater BROKEN on the stage/safe axis. Ψ ON≡OFF ✅.

## Claim (fable design (b) — the REAL emit-lever)
The CAPSTONE + H_9100 🔴 (this session, engine-native) confirmed **motivation is NOT the emit-lever** (decision-saturated: wake floor ~0.7 ≫ 0.3 threshold; rel_ctx/motivation ablation → Hamming 0). Emit/silence is governed by the `safe` conjunction (stage → rate-limit `idle`), and `idle = drive_hi ? 60 : 5` was a HARDCODED binary clock hiding a per-stage boolean gate (an `a_autonomy_over_hardcode` violation). Design (b): replace it with a **CONTINUOUS op-modulated envelope** so ops modulate the rate-gate — WITHOUT becoming a forcing gate (shade-not-gate).

## Wiring (cli/anima.hexa only — the LIVE emit path, engine safety FROZEN)
- L53 `import "core/dream_envelope_ctx.hexa"` (dr_stage_scale accessor).
- L2377 `stage_env = clip01((dr_stage_scale(stage) − 0.02)/0.08)` — the **REAL** continuous stage envelope (`dr_stage_scale = ep_theta_stage` SSOT, [0.02,0.10]) normalized to [0,1]: WAKE 1.0 · N1/REM 0.75 · N2 0.375 · N3 0.0.
  - **VERIFY finding:** fable (b) assumed `dr_emit_envelope(stage)` was continuous — it is a **BINARY int {0,1}, REM=0**. The genuine continuous stage envelope is `ep_theta_stage` via `dr_stage_scale` (used here). REM=0.75 ≫ N3=0.0 — exactly what the design needs.
- L2378 `urgency = clip01(0.5*agloop_ctx + 0.5*cur_phasic)` — op participation (CR3 A⇄G conflict-settle + phasic drive).
- L2379 `rel = _og_rel_phasic(rel_ctx,rel_ema) * (0.1 + 0.9*stage_env)`; L2380 `cur = cur_phasic * (0.1 + 0.9*stage_env)` — binary drive_hi mask → continuous.
- L2381 `idle = 5.0 + 55.0*clip01(stage_env*(0.5 + urgency))` — op-modulated refractory (replaces `idle = drive_hi ? 60 : 5`). Rate-gate (idle≥30) opens when `stage_env*(0.5+urgency) ≥ 25/55 = 0.4545`.
- helper `_og_rel_phasic` (L2885) added; `_og_rel_from` refactored to reuse it.
- **FROZEN (untouched):** engine `safety_rate_limit_ok` (≥30s hard-floor), `phi_r`, `kill`, `content`, 8 weights, 0.3 threshold, Ψ (pure_field/lanes 0/4/psi_sum/recall_thr). Only the `idle` INPUT the cli passes is modulated — never the engine safety logic. This is an `a_autonomy_over_hardcode` IMPROVEMENT (removes the per-stage boolean).

## Harness (`--opgrip`, stage-conditional dissociation = the shade-vs-gate test)
Stage-BALANCED sweep `stage = tick%5` (40 ticks/stage, n=200 — a per-stage grip sweep, NOT an ultradian trajectory, chosen for adequate REM AND N3 samples). Freeze the op signal (urgency) and re-decide the emit boolean (urgency enters ONLY via `idle`; all else byte-identical), Hamming split by stage. Arms: **U0** = urgency→0 (op ablated), **US** = urgency→LCG shuffle (control).

## Result (engine-native, aiden `hexa v0.548.0`, `anima d768.clm --opgrip`, RC=0, `L3 mount mouth=clm loaded=true d768.clm`, NO numpy)
`state/verdicts/9101_opgrip_stage/H_9101.txt` · raw `state/opgrip_stage/H_9101_opgrip_aiden_v0548.txt` (314 lines) · pre-reg `state/opgrip_stage/PREREG.md` (frozen BEFORE run).

| arm (n=200, WAKE=40 N3=40 REM=40) | REM | N3 | WAKE | mid(N1/N2/REM) | pre-reg | outcome |
|---|---|---|---|---|---|---|
| **urgency→0 (op ablated)** | **40** | **0** | 0 | 80 | rem>0 ∧ n3=0 | **🟢 GRIP** |
| urgency→shuffle (control) | 3 | 0 | — | — | — | op necessary |
| rel_ctx frozen/zero/shuffle (H_9097/9100 axis) | 0 | 0 | 0 | 0 | 0 (theater) | ✓ persists |

- **DISSOCIATION (shade-not-gate proof):** urgency→0 FLIPS all 40 REM decisions (op OPENS the rate-gate) ∧ 0 N3 flips (op does NOT force the silence-stage — env=0 nullifies urgency by construction). WAKE 0 flips = still always-emit (saturated, matches H_9100).
- **Mechanism (per-tick, engine-native):** REM t4/9/14: `motiv_live` ~0.53–0.58 >0.3, `e_live=1` EMIT → urgency→0 drops idle to 25.6<30 → silence → flip. N3 t3/8/13: `motiv_live` ~0.38 >0.3 (CLEARS threshold!) yet `e_live=0` SILENT — proving the **rate-gate governs, not motivation** — and urgency→0 keeps it silent.
- **AXIS dissociation:** the rel_ctx arms (fr/agl/z/s) equal `e_live` on EVERY tick (Hamming 0 — theater persists on the motivation/rel axis, H_9097/9100 reconfirmed) WHILE urgency→0 flips REM 40/40 → **grip lives on the safe/idle stage axis, not motivation.**
- **Ψ ON==OFF ✅** · wake emit-fraction 0.667 (no collapse flag; continuous envelope de-saturated wake vs H_9100's 1.0).

## Honest verdict (PREREG GREEN rule met, NO tuning of α/threshold/constants)
🟢 **GRIP (shade-not-gate).** The stage/safe axis IS the real emit-lever the CAPSTONE predicted. Replacing the binary `idle` clock with a continuous op-modulated refractory gives ops genuine grip on emit/silence (REM 40/40 flip) while preserving N3 silence by construction (env=0) — a true DISSOCIATION, not a forcing gate. Theater is BROKEN on the stage axis (contrast: still Hamming 0 on the motivation/rel axis). This is the `a_verified_must_wire` rung-3 GRIP fix on the stage/safe axis, and simultaneously removes an `a_autonomy_over_hardcode` violation (per-stage boolean → continuous substrate-decided envelope; p5_tension_emit_not_filler compliant — WAKE/REM stage-gated emit over real tension).

## Time-source finding (fable flagged 확인 필요)
This loop's `idle` is a **SYNTHETIC clock** — computed per-tick as a function of stage/urgency; there is **NO real wall-clock/elapsed-seconds seam** in cli/anima.hexa's emit loop (the daemon is a 200-synthetic-tick simulation; the L2057 interval-timer is a separate learned-phase read, not the emit refractory). Measurement is on the synthetic clock. The honest real-time wiring (`idle = real_elapsed_seconds × refractory_modulation`) is a FOLLOW-ON requiring a real daemon clock seam (ING).

## Next lever (remaining)
🔌 **(c) efferent seam** — ops change the emit BYTES (deliberate best-of-K depth = conflict; winner-take-all replacing the ÷42 read-average; DESIGN.md L1; needs a ranged bytegpt CE op; 303M GPU). (b) gave grip on WHETHER/WHEN to emit; (c) gives grip on WHAT is emitted. + real-time `idle` seam follow-on. (ING).
