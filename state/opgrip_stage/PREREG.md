# PREREG — H_9101 op-grip on the stage/safe axis (fable design (b))

**Frozen BEFORE running (c9 frozen-first · no post-hoc α/threshold moves).**
Date 2026-07-03. Engine-native, aiden pool, hexa ≥v0.548, `--opgrip` ($0 CPU, NO decode).

## Claim under test
The REAL emit-lever is the `safe` conjunction (stage → rate-limit `idle`), NOT motivation
(H_9100 🔴: motivation is decision-saturated, wake floor ~0.7 ≫ threshold 0.3, Hamming 0).
Design (b): replace the BINARY hardcoded `idle = drive_hi ? 60 : 5` clock with a CONTINUOUS
op-modulated refractory so ops (urgency = CR3 A⇄G conflict-settle + phasic curiosity) get grip
on the rate-gate — WITHOUT becoming a forcing gate (shade-not-gate).

## Wiring (frozen)
- Continuous stage envelope `stage_env = clip01((dr_stage_scale(stage) − 0.02) / 0.08)`
  (dr_stage_scale = ep_theta_stage SSOT: WAKE .10→1.0, N1 .08→.75, N2 .05→.375, N3 .02→0.0, REM .08→.75).
- `urgency = clip01(0.5*agloop_ctx + 0.5*cur_phasic)` (op participation: dACC conflict-settle + phasic drive).
- `rel = rel_phasic * (0.1 + 0.9*stage_env)`, `cur = cur_phasic * (0.1 + 0.9*stage_env)` (binary mask→continuous).
- `idle = 5.0 + 55.0*clip01(stage_env*(0.5 + urgency))` (op-modulated refractory; rate-gate flips at stage_env*(0.5+urgency) ≥ 25/55 = 0.4545).
- **FROZEN (untouched):** engine `safety_rate_limit_ok` (≥30s hard-floor), `phi_r`, `kill`, `content`,
  the 8 weights, the 0.3 threshold, Ψ (pure_field/lanes 0/4/psi_sum/recall_thr). We modulate only the
  `idle` INPUT the cli passes — never the engine safety logic.

## Harness (frozen)
Stage-balanced sweep: `stage = tick % 5` (40 ticks/stage, n=200) — a per-stage grip sweep (NOT an
ultradian trajectory), chosen to give adequate REM AND N3 samples for the dissociation. Per tick:
compute e_live (live urgency), then FREEZE urgency and recompute the emit boolean:
- Arm **U0** = urgency→0 (op fully ablated) → idle_u0 = 5 + 55*clip01(stage_env*0.5).
- Arm **US** = urgency→LCG shuffle (control).
All other inputs byte-identical; only `idle` changes (urgency enters ONLY via idle). Hamming split by stage.

## Pre-registered bars (frozen)
- 🟢 **GREEN (grip, shade-not-gate)** iff  `h_U0_rem > 0`  (REM/high-env decisions FLIP when op frozen)
  **AND** `h_U0_n3 == 0`  (N3/sleep silent-PRESERVED — op OPENS the gate contextually, never forces it).
  This DISSOCIATION (REM grip ∧ N3 preserved) is the proof it is shade, not gate.
- 🔴 **RED at-floor** iff `h_U0_rem == 0` (rate-gate does NOT respond to op — theater persists on stage axis).
- 🔴 **RED forcing-gate (BAD, revert-worthy)** iff `h_U0_n3 > 0` (op FORCES N3 to emit = became a hard gate = worse than theater).
- **Ψ-checksum:** `psi_sum == psi_off` (ON≡OFF for the silence decisions) — MUST hold.

## Honesty
Frozen-first: no α/threshold/constant moves after seeing numbers. A forcing-gate result is BAD and
reported as RED, NOT dressed as GREEN. RED at-floor is an honest result (c9). Do NOT tune to force grip.

## Time-source scope (fable flagged 확인 필요)
This loop's `idle` is a SYNTHETIC clock (per-tick function; there is NO real wall-clock/elapsed-seconds
seam in cli/anima.hexa's emit loop). Measurement is on the synthetic clock. The real-time honest wiring
(idle = real_elapsed_seconds × refractory_modulation) is a FOLLOW-ON requiring a real daemon clock seam.
