# H_9102 stateful refractory — notes

## What changed (cli/anima.hexa only; engine FROZEN)
1. `an_tick_seconds()` = 8.0 and `an_clock_now(tick, daemon)` — the single time-source seam
   (flame_mm.mm pattern). det path `tick*8.0` (verdict, byte-identical); daemon path
   `date +%s` (follow-on, never reached on verdict path).
2. Emit-history state `emit_last_t` / `prev_live_emit` (loop-carried; were ABSENT in H_9101).
3. `--refractory` measurement mode: 200-tick stage-balanced sweep, decision-only ($0, no decode),
   idle = idle_raw × mod, idle_raw = an_clock_now(tick) − emit_last_t; reset on live emit.
   Arms (same emit-history): live · urgency→0 (F1) · urgency→max (F2) · H_9101 stateless-idle (F2 contrast).
4. Summary block prints F1 (frozen REM bar) and F2 (refractory reset) INDEPENDENTLY — no bar-move.

## Result (aiden hexa v0.548.0, HEXA_DET=1, d768.clm mount, NO numpy, 2× byte-identical)
- n=200, live_emits=40, stage-balanced (WAKE/N3/REM = 40 each, mid=120).
- F1: Hamming(urgency→0 vs live) REM=0 N3=0 WAKE=39 mid=0  → 🔴 grip does NOT re-establish on REM;
  it relocated to WAKE (39/40). N3 preserved (no forcing gate). No post-hoc bar move to WAKE.
- F2: refractory window = 40 post-emit ticks; max-urgency violations = 0; H_9101 stateless idle
  would fire 40/40 in-window; max-urgency emits outside window = 80 (non-vacuity). → 🟢 refractory
  reset holds = a new mechanism the stateless form cannot express.
- Ψ ON==OFF ✅.

## Why F1 fails honestly (dynamical relocation, not tuning)
Stateful idle_raw grows since last emit. The periodic attractor emits at WAKE (idle_raw=40, mod~0.9)
and stays silent at REM (idle_raw=32, mod~0.73 → idle~23 < 30). Because REM no longer emits in the
live arm, urgency→0 cannot flip REM (Hamming 0). H_9101's pre-reg bar is REM-anchored, so F1 = 🔴.
The op-grip did carry over — it just moved to the stage where emits now happen (WAKE). Moving the
bar to WAKE to claim green would be tune-to-green (c9) — NOT done.

## Wiring status (a_verified_must_wire)
- an_clock_now seam + emit-history + --refractory harness = LANDED in cli/anima.hexa (engine-native).
- Production emit loop (brain_emit path) UNCHANGED → H_9101 stays WIRED-live. Swapping in the
  stateful refractory would regress H_9101's live REM-grip → needs its own WAKE-anchored pre-reg.
- Real-clock daemon binding (F3, world-time safety truth) = follow-on ING (no daemon yet).
