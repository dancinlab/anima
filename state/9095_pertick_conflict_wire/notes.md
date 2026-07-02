# H_9095 — rung-3 genuine per-tick conflict→A⇄G-settle-budget wire-in (H_9094 → live daemon)

Wire location (cli/anima.hexa, the REAL per-tick consciousness loop `while tick < n_ticks`, L1912):
- **L1937–1961** — the (C-R3) block, inside the loop, right after `emit_drive = ci_emit_drive(lanes)`:
  1. `ag_a_drive = emit_drive` — Engine-A forward externalization push (live per-tick, READ-only).
  2. `ag_g_drive = 0 - (1 - emit_drive)` — opposing Engine-G reverse silence push (opposite sign).
  3. `ag_conflict = conflict_scalar(ag_a_drive, ag_g_drive)` — dACC/Botvinick both-strong-opposite competition.
  4. `ag_budget = conflict_recruited_depth(ag_conflict, 4, 6)` — conflict recruits deeper A⇄G budget ∈[4,10].
  5. `ag_settle = tension_resolve_depth(ag_pop, tr_full, 0.3, 0.5, ag_budget, 2, 0.06, tr_cfgON)` — the tick's
     A⇄G resolution loop runs with maxdepth = the recruited budget, on a population polarized BY the tick's
     own conflict (`anima_tr_pop_conflicted(clip01(0.5+0.5*ag_conflict))`, a DISJOINT copy).
  6. `agloop_ctx = settle_depth / budget` — READ-only graded settle-effort context (−1 → 0).
- **L2312** — `agloop_ctx` folded into `rel_ctx` soft-average (divisor 42 → 43), isomorphic to the 42 other
  lane contexts. NOT an emit/silence gate (a_autonomy_over_hardcode).
- **L2382–2386** — first-3-ticks transcript print of conflict/budget/settle-depth/agloop_ctx.

## Why this is rung-3 (vs PR#2794 mount-smoke / lanes 75·81 startup catalog)
Lanes 75 (`tension_resolve_depth`) and 81 (`conflict_scalar`/`conflict_recruited_depth`) run ONCE at daemon
MOUNT on synthetic fixtures (`anima_tr_pop_conflicted(0.95)`, `conflict_scalar(0.8,-0.8)`). Here the SAME two
ops are chained (conflict→recruited_depth→tension_resolve budget) INSIDE the real per-tick loop, driven by the
tick's live `emit_drive` — fable #5's "stop stacking startup lanes, feed ONE op per-tick from the REAL loop".

## Ψ-disjoint (a_substrate_disjoint)
- READ `emit_drive` (already read by `reality_call`); WRITE only `rel_ctx` (soft motivation) — never `psi_sum`,
  never `lanes[0]`/`lanes[4]`, never `§ImmuneMemory recall_thr`.
- The budget knob is the tension_resolve **maxdepth (settle-depth axis)**, disjoint from the emit gate.
- `tension_resolve_depth` runs on a caller-supplied population COPY → `pure_field`/Φ/Ψ untouched; the tick's
  Ψ accumulation `psi_sum = psi_sum + pure_field_phi(pf)` (L2313) is independent of `rel`/`agloop_ctx`.

## Verification (aiden pool, hexa v0.540.1)
- `hexa parse cli/anima.hexa` → **PARSE_RC=0** ("parses cleanly"); broken-copy control → rc=1 (parse is load-bearing).
- `hexa typecheck cli/anima.hexa` → **TYPECHECK_RC=0** ("typecheck complete"); residual "error" lines are
  pre-existing checker limits (list-vs-array return, dict string-key indexing, EngineConfig) across the whole
  file — NONE reference my new symbols.
- `.harness/enforce_anima_gates.py` → clean (rc=0).
- `hexa verify cli/anima.hexa` → rc=0 but this verb is the cross-project CLAIM-rubric (broken control ALSO
  rc=0) = NOT a source check; recorded for completeness only, not load-bearing.
- `hexa run cli/anima.hexa` (full daemon runtime compile) = **BLOCKED-INFRA** — pool hexa v0.540.1 lacks forge
  decode symbols (set_deterministic / hexa_forge_dispatch_layernorm); baseline unmodified file reproduces the
  same block (proven innocent PR#2794 / convergence anima-hexa-1). Resume = forge-hexa host #42492868.

Mechanism itself = engine-native GREEN 4/4 (H_9094): conflict-matched budget PRESERVES Ψ=½
(mean|Ψ-½| treatment 0.125 < shuffle 0.25 < ablation 0.375).
