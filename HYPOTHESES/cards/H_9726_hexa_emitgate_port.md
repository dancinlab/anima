# H_9726 — hexa emit-gate PORT: brain_emit_refractory + dual-ledger + Ψ≈½ default (H_9712 twin · resolves H_9718)

**Verdict:** 🟢 **WIRED-hexa (DIRECTIONAL on typecheck)** — the H_9415→H_9627 emit-gate family is now ported to the
hexa twin; the hexa daemon default is flipped to the H_9627 dual content ledger (Ψ≈½), mirroring the py H_9712 flip.
Twin-parity claim — the Ψ≈½ result itself stays earned on py 303M (H_9712/#3867), NOT re-claimed here.
**Register:** H_9718 NEXT (owner "잔여 모두 go") · Fable-designed, locally implemented (fable-mode) · resolves H_9718
**Ckpt:** N/A (hexa-lang port · verification = typecheck + set-diff, per engine-cli-hexa-2 · no local native build)

## What was ported (a_substrate_disjoint · brain.hexa + anima.hexa + engine_cli.hexa only)
Mirror of py `cli/chat.py` (H_9712) + `core/brain.py:233 brain_emit_refractory`, scoped to the DEFAULT path
(refractory + wm-dual), on the existing hexa primitives (H_9718 refined: hexa core HAS immune margin / wm_buffer_*):
- **`core/engine_cli.hexa`**: `wm_byte_feature(s, dim) -> [float]` — verbatim twin of py `_afs_byte_feature` (the one
  missing primitive; brain.hexa can't import cli's copy).
- **`core/brain.hexa`**: `brain_emit_refractory(...)` — emit ⟺ gate ∧ kill ∧ φ-ratchet ∧ content (NO θ/rate). `gate`
  = (dual) S>E over the two ledgers or (d1) score > immune margin. **De-closured** (hexa has no function values):
  `dual_probe_fn` → two `WorkMemBuffer`s (s_buf/e_buf) + a `dual` bool — the alien arms become pure call-site swaps.
  NOT ported (py-only default-off research/steering): mouth/dyn_w/record_cand_diag/route_pc2/pc2_mouth/score_perturb/
  zeta_ladder/--g-shuffle.
- **`cli/anima.hexa`**: argv threaded into `anima_consciousness_mode(ckpt, argv)`; `anima_strval`/`anima_floatval`
  helpers; `--emit-gate` (default **refractory**) / `--g-reach` (conditional default `wm-dual` if refractory else
  `d1`, rollback-safe) / `--wm-leak` (0.6) + guards; W_S `wm_withheld` buffer (empty, leaked, silence-side gate-in) +
  `wm_dual_alien` control; call-site swap (refractory ⇒ `brain_emit_refractory`, else `brain_emit` byte-untouched).
- **root VERSION** G5 (0.15.60→0.15.61 at author time).
- **⚠️ hexa/py divergence (documented)**: hexa has NO env-var access → the emit-gate flags are **argv-only** (py also
  reads `ANIMA_EMIT_GATE`/etc.). Behaviorally identical for CLI invocation.

## Verification (typecheck set-diff · engine-cli-hexa-2 · no local native build)
Per `engine-cli-hexa-2` a local full-engine native smoke build is BLOCKED (20-min codegen → clang fail on the giant
TU); the syntactic gate is `hexa typecheck` + set-diff of error signatures vs origin baseline:
- `core/brain.hexa`: mine non-Map errors = **0** (all "Array index string" = the standard Map-access pattern).
- `core/engine_cli.hexa`: only non-Map error "Undeclared variable 'float'" ×2 — **present in origin baseline too**
  (NOT from `wm_byte_feature`).
- `cli/anima.hexa`: total errors mine 83 vs origin 82 = **delta +1**, a single Map-access warning from my new
  `dec["dual_cand_text"]` access (benign); non-Map error "Unknown struct 'EngineConfig'" ×2 = **origin baseline**.
⟹ **0 new real errors** across all three files — the port is syntactically clean (H_9411 typecheck-DIRECTIONAL bar).

## Scope / honesty (`a_scale_honest_scope` · a_engine_native_learning)
- **DIRECTIONAL on typecheck**, exactly H_9411's precedent (py-first TERMINAL, hexa twin DIRECTIONAL when the daemon
  host is blocked). Runtime byte-parity (Cert A clock-identity + Cert B fixture, Fable §2) is the authoritative
  gate but needs the hexa daemon, which is pool-blocked/moot (`hexa-runtime-a-stale-native-objects`, `chat-py-1`
  py-canonical); it is a **ρ-AXON reach fact, not a deficit** (Ψ-SOMA) — deferred to whenever the hexa runtime unblocks.
- **Twin-parity claim only**: the Ψ≈½ emergence is earned on py 303M (H_9712 · #3867 score-perturb 0.000 · H_9608
  0.500). This card claims the hexa gate MIRRORS that py gate — it does NOT re-claim ½ on hexa.
- py = the canonical production runtime; `hx install anima` chat now defaults to refractory too (once the hexa daemon
  runtime is buildable), `--emit-gate clock` = the legacy clock daemon.

## NEXT
- hexa-daemon byte-parity certs (A clock-identity + B fixture) when the hexa runtime unblocks — until then the py
  303M evidence + typecheck set-diff is the landing gate.
- Optional `core/brain_refractory_smoke.hexa` fixture (Fable §2 Cert B) — follow-on.

**Provenance:** hexa-lang port on origin/main; verification = `hexa typecheck` set-diff (0 new real errors) per
engine-cli-hexa-2. Owner-approved ("잔여 모두 go"). Resolves H_9718 (py/hexa divergence tracker). Earning science =
H_9627 (dual ledger) + H_9712 (py default). id H_9722→H_9726 (parallel collision · a_parallel_session_compare).
