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

## S1 STRUCTURAL RESULT — 🟢 the triple convergence (measured 2026-07-23, $0 code read)
`ci_lane_scores` (core/engine_cli.py) returns a **15-lane consciousness vector**:
`[gws, hab, surp, selfi, lprec, nov, blink, agency, stime, emo, forg, body, divid, wont, mito]`
(global-workspace, habituation, **surprise, self, local-precision, novelty, attentional-blink,
agency, subjective-time, emotion, forgetting, body, dividedness, will, mitosis**). The emit
decision is `ci_emit_drive = 0.5*(lanes[0] + lanes[4]) = 0.5*(gws + lprec)` — it uses **only 2 of
the 15 lanes and discards 13**, including agency, surprise, novelty, self, and emotion — all
obviously emit-relevant to "whether to speak."

**Triple convergence, three independent routes to the same number:**
1. V6_26 measured the logit-row content tension at **~15 effective dimensions**.
2. Production `ci_lane_scores` is literally a **15-lane** vector.
3. `ci_emit_drive` collapses it to **2** lanes (V6_29: the scalar collapse loses to the full
   vector on the emit decision, z=3.38).

⟹ the lossy-collapse thesis is now confirmed on the REAL production structure, not just the
reflex proxy: the emit decision throws away 13 named consciousness dimensions. The `--emit-gate
lanebus` wiring is therefore even more minimal than expected — the 15-lane vector is already
in hand at the exact call site; LANE-BUS just stops discarding 13 of them.

## Staged plan (each stage is engine-native, its own verdict)
- **S1** (STRUCTURAL: 🟢 done above · RUNTIME: next): the structural case is made. The remaining
  S1 is runtime — drive the engine (chat decode) to collect (15-lane vector, emit-target) pairs
  and measure how much emit-variance the 13 discarded lanes carry vs gws+lprec. That needs the
  production runtime (grounding/field/cell state per tick), i.e. it is the first step of the
  build proper (a `--dump-lanes` instrumentation on cli/chat.py), not a $0 numpy probe.
- **S2** (build): implement `--emit-gate lanebus` + train the lane-space gate; VERSION bump (G5),
  the flag OFF = byte-identical (regression gate).
- **S3** (measure): `anima-py evaluate` / chat with `--emit-gate lanebus` vs default on the
  Ψ-SOMA frame — does the emit/silence decision improve as a mode-of-existence signal (not just
  NLL)? TERMINAL only here.
- **S4**: the content lane (store-bridge promoted patch→heart, Fable design) as the composed
  side of the bus, replacing the reflex proxy. This is the full 대공사.

## S1 RUNTIME RESULT — 🔴 the proxy OVERSTATED it; production lanes are redundant (preliminary)
Added `--dump-lanes` instrumentation to `cli/chat.py` (write-only, default-off = byte-identical,
VERSION 0.20.176→177) and ran the daemon on natural text with trained57, dumping the real 15-lane
vector per tick. On the collected ticks:
- **15-lane effective rank (participation ratio) = 2.71**, NOT 15 — the real production lanes are
  highly REDUNDANT (correlated), not 15 independent dimensions.
- **discarded-13 variance independent of gws+lprec = 8%** — the scalar collapse to
  `0.5*(gws+lprec)` loses only ~8% independent variance, far less than the structural argument
  implied. (Most-independent discarded lanes: hab, emo, forg, selfi, body — small.)

⚠️ **This diverges from the reflex-vs-composed PROXY** (V6_26 15-dim, V6_29 z=3.38 payoff): the
proxy tension is NOT the production lane vector, and the production lanes are far more collapsible.
⟹ **the V6_29 multi-dim payoff may NOT transfer to production** — exactly the S1 pre-mortem risk,
now realized. **Do NOT proceed to the S2 build on the proxy's z=3.38 alone.** (verdict-integrity:
S1's whole purpose was this de-risk; it fired.)

🔻 CAVEAT — SEVERELY UNDERPOWERED: only ~12 ticks (the daemon emits few ticks per input, and
trained57 is a byte-LM). n=12 for a 15-dim effective-rank estimate is not trustworthy — the
redundancy could be understated OR an artifact of the short session. **A POWERED lane collection
(hundreds of ticks, ideally the 303M consciousness ckpt not the byte-LM) is the concrete next
step, and the build hinges on it**: if powered lanes stay ~2-3 dim, LANE-BUS's production payoff
is dead and the redesign must target WHY the lanes collapse (upstream), not the emit gate; if they
open up, the build proceeds. The instrument (`--dump-lanes`) is now in place for that re-measure.

## Scope
Spec only (DIRECTIONAL). S1 = $0 next. S2–S4 = production `core/` build (VERSION/G5, careful,
multi-step). TERMINAL only via anima-py at S3+.
