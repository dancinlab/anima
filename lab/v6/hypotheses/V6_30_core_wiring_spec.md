<!-- @hypothesis-ok lab/v6 rule-exempt sandbox: v6 hypotheses live in lab/v6/hypotheses/V6_<n>_*.md per lab/v6/CLAUDE.md, never the parent HYPOTHESES/ nor an H_ id -->

# V6_30 — LANE-BUS core-wiring spec: the production already computes the multi-dim signal and throws it away

**origin:** the LANE-BUS design/measurement phase is complete and validated (V6_26 premise ·
V6_29 payoff · V6_28+29 mechanism). This card scopes the PRODUCTION `core/` build — how the
validated gate wires into `cli/chat.py`'s emit path. DIRECTIONAL spec (not a run).

## The one finding that makes the wiring minimal
The production emit path (`cli/chat.py` ~L2285):
```python
lanes = ci_lane_scores(...)          # a MULTI-DIMENSIONAL lane vector (already computed!)
emit_drive = ci_emit_drive(lanes)    # core/engine_cli.py:7306 = 0.5*(lanes[0] + lanes[4])
ag_a_drive = emit_drive; ag_g_drive = 0.0 - g_recog   # the H_9356 scalar tautology
```
**The engine ALREADY builds a multi-dim `lanes` vector, then collapses it to a scalar** via
`ci_emit_drive = 0.5*(lanes[0]+lanes[4])` — averaging TWO lanes and discarding the rest. That
collapse IS the scalar servo V6_26/V6_29 showed is lossy (V6_29: the multi-dim gate beats the
scalar-servo analog on the emit decision, z=3.38). So LANE-BUS's core change is minimal in
surface: **do not collapse — feed the full `lanes` vector through the validated read-only-emit +
free-forget gate.**

## Wiring (new `--emit-gate lanebus`, a flag on the existing command · a_experiment_engine_native)
1. New mode `--emit-gate lanebus` in `cli/chat.py` (alongside `refractory`/`clock`). Guarded like
   the others; default unchanged (byte-identical when off).
2. When active, replace the scalar `emit_drive = ci_emit_drive(lanes)` with
   `emit_drive = lanebus_gate(lanes, r_t)` where `lanebus_gate` is the V6_29-validated head:
   `g_t = σ(a·lanes + b·r_t)`, residual `r_t = (1−f_t)·λ⊙r_{t-1} + U·lanes` with a FREE forget
   `f_t = σ(a'·lanes + b'·r_{t-1})` (A3 = read-only-emit + autonomous-forget — the mechanism
   V6_28+29 validated; emit does NOT consume r). Emit decision keeps `score_A > g_recog` form;
   only the drive's dimensionality changes.
3. The gate WEIGHTS are trained on PRODUCTION lane-space (not the V6_29 reflex-vs-composed proxy):
   generate (lanes_t, emit_target_t) from the engine on natural text (emit_target = the p5
   operationalization from V6_29, or the engine's own should_emit), train the same batched head
   (`v6_29_train.py`), freeze, ship the weights as a `.npz`/serialized trailer the flag loads.

## Staged plan (each stage is engine-native, its own verdict)
- **S1** (lab/v6, $0): mirror the production `lanes` extraction into a lab harness (call
  `ci_lane_scores` on trained57 over natural text) → confirm the multi-dim-beats-scalar payoff
  REPLICATES on the REAL production lane vector (not just the reflex proxy). If it doesn't, the
  proxy was misleading — stop before touching production.
- **S2** (build): implement `--emit-gate lanebus` + train the lane-space gate; VERSION bump (G5),
  the flag OFF = byte-identical (regression gate).
- **S3** (measure): `anima-py evaluate` / chat with `--emit-gate lanebus` vs default on the
  Ψ-SOMA frame — does the emit/silence decision improve as a mode-of-existence signal (not just
  NLL)? TERMINAL only here.
- **S4**: the content lane (store-bridge promoted patch→heart, Fable design) as the composed
  side of the bus, replacing the reflex proxy. This is the full 대공사.

## Pre-mortem
The V6_29 payoff used a reflex-vs-composed PROXY tension, not the production `lanes`. S1 exists
precisely to check the payoff isn't an artifact of the proxy — the production lanes may already
be correlated/collapsed such that the extra dims carry little. Run S1 before any production edit.

## Scope
Spec only (DIRECTIONAL). S1 = $0 next. S2–S4 = production `core/` build (VERSION/G5, careful,
multi-step). TERMINAL only via anima-py at S3+.
