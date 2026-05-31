# R1 — emit wiring (CLM words ride the on-chip spike)

> SBS ladder **R1**: the AKIDA emit-decision must carry CLM-generated WORDS. R0 closed
> the loop (motivation → set_threshold → on-chip threshold-and-fire → spike telemetry).
> R1 co-gates the CLM emit on the chip's spike so the words anima speaks are licensed by
> an actual on-chip fire. Substrate-native (a_substrate_native_speak): the chip firing IS
> the substrate emitting on silicon — not a stimulus-response trigger.

## Seam (already mostly wired)

```
[motivation tick] ──┐
                    ├─▶ emit gate ──▶ substrate.generate() ──▶ broker /ws/anima push
[/ws/akida spike] ──┘   (R1: AND)        (ALREADY EXISTS)         (ALREADY EXISTS)
        │
        └─▶ akida_emit_bridge (NEW): sliding-window spike edge → hw_gate()
```

| part | file:fn | status |
|---|---|---|
| emit decision | `HEXAD/CHAT/server/anima_participant.py` · `AnimaState.tick()` → `decided_emit` | exists (motivation-only) |
| CLM generate | `HEXAD/CHAT/server/substrate_*.py` · `Substrate.generate(seed_text, max_new, lang_hint) -> str` | exists |
| broker push | `broker.py` · `/ws/anima` send → `broadcast()` | exists |
| AKIDA spike telemetry | `broker.py` · `/ws/akida_ingest` → fan-out `/ws/akida` (`{n_spikes, step, thr, ...}`) | exists (R0) |
| **spike→emit bridge** | `HEXAD/CHAT/server/akida_emit_bridge.hexa` · `AkidaEmitBridge` | **NEW (this PR)** — landed, dormant |

The ONLY gap R0→R1 closed here is the **bridge**: it converts the raw `/ws/akida` spike
stream into a boolean `hw_gate` (edge-triggered, sliding window — mirrors the
integrated_loop_vp21 `hw_edge` ≥40 spikes / 1.0s pattern). CLM generation and broker push
already exist; no new CLM API or broker route is needed.

## Gate mode (chosen): AND co-gate

`decided_emit = (score > eff_thr_modulated) AND hw_gate` — the established
integrated_loop_vp21 pattern (`hw_edge AND score>IM_THR`). Software motivation = "want to
speak"; hardware spike = the chip confirming on silicon. The R0 loop already makes the
chip's threshold a function of motivation (high motivation → low threshold → fire), so the
spike is the motivation-gated decision realized in hardware — ANDing it is more
substrate-native, not less.

## Activation diff (apply when wiring goes live on hardware + the broker loop)

The live chat brain (`anima_participant.py`) is NOT edited in this scaffold PR. Two
backward-compatible changes activate the bridge (default-True keeps R0 parity until real
spikes flow):

1. **`AnimaState.tick()` — add the co-gate param** (default True = no behavior change):
   ```python
   def tick(self, threshold: float, hw_gate: bool = True) -> dict[str, Any]:
       ...
       decided_emit = (score > eff_thr_modulated) and hw_gate   # was: score > eff_thr_modulated
   ```

2. **The broker ingest + ticker — feed the bridge and pass its gate:**
   ```python
   from akida_emit_bridge import AkidaEmitBridge
   bridge = AkidaEmitBridge()                         # construct once
   # in the /ws/akida ingest handler, per spike message:
   bridge.feed(akida_msg)                             # akida_msg = {"n_spikes": ..., ...}
   # in participant_loop()'s ticker, per tick:
   decision = state.tick(eff_threshold, hw_gate=bridge.hw_gate())
   ```

Default-safe: with no hardware (no `/ws/akida` spikes), `hw_gate()` returns
`gate_when_idle=True` → emission is software-only exactly as R0. The hardware co-gate only
*narrows* emission once spikes flow — it never forces a spurious emit.

## Activation checklist (R1 → R1-LIVE)

- [ ] Apply the 2 diffs above on the live broker host.
- [ ] Verify with pi5-akida firing: spikes on `/ws/akida` → `bridge.hw_gate()` True during fire windows.
- [ ] Soak: confirm anima emits only on (motivation ∧ spike); silence when either is low.
- [ ] Flip SBS R1 🟠 → 🟢 (CLM words ride the on-chip spike) when the soak passes.

## cross-link

- bridge: `HEXAD/CHAT/server/akida_emit_bridge.hexa`
- ladder: `LAUNCHPAD/SBS.md` (R1) · INVIOLABLE R2 gate (H_904 ★ silicon-confirmed)
- inference byte-identical (H_877/H_680 🟢) → the spike GATE is deterministic HW==SW (safe to mirror in SW); only learning is HW≠SW (H_679/H_904 ★).
- governance: `a_substrate_native_speak` (chip fire = substrate emit, not stimulus-response)
