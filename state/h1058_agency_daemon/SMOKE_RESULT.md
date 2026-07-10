# H_1058 daemon decision-trace side-channel — byte-safe smoke (2026-07-10)

WIRE: `cli/chat.py` — ANIMA_TICKS (tick-count override) + ANIMA_DECISION_TRACE (write-only
JSONL, one row/tick) side channel. Default OFF. Emit path byte-untouched.

## Byte-identical smoke (toy.clm d32, 12 ticks, same session_seed)
- trace OFF stdout vs trace ON stdout = **BYTE-IDENTICAL** (256 lines each, `diff` clean)
  → self⊥trace: the trace is write-only, emit decision + bytes unchanged (twin of the
  H_9129 hippo-consult write-only discipline).
- trace JSONL valid: 12 rows · **EMIT=10 · ACTIVE_VETO=2** → the daemon fires REAL vetoes
  (score>0.3 ∧ ¬safe = a braked live impulse) every session; now captured instead of thrown
  away. This is the crux the H_1058 verdict identified — a weight-forward CANNOT produce a
  veto (no motivation, no idle clock, no braking term); only the live emit/veto daemon can.
- schema/row: {tick, stage, idle, score, safe, emit, cls, phi, anchor_nudge, gen_emitted,
  gen_backend, gtext_sha, gtext_len}. cls = the gate structure at core/brain.py:162.

## Status
- ✅ enabling wire (FIRED veto trace) — DONE + byte-safe + captures real vetoes.
- follow-on (per FABLE_DESIGN.md): frozen-emission replay-depth prober (causal provenance-depth,
  zero model forwards) · H_1056 per-impulse veto-capacity · T = z(depth)+z(vc) · faithful-Φ leg
  (H_1042 3B trunk tap, ≥2 macro-maps) · controls (emit-rate · trace-shuffle ARM-SHOCK ·
  generator-swap 3B/303M/unloaded → H1-NOT-A-3B-PROPERTY branch) · MVH (303M, 256 ticks, ~$0)
  then 3B on a dedicated pool host. H_1058 pre-registered falsifier FROZEN (p7).
