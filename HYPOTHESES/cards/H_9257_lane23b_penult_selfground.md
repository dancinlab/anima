# H_9257 — lane-23b penult self-grounding (self-continuity: synthetic → substrate-grounded)

**Slug**: `lane23b_penult_selfground` · **Tier**: 🌱 PRE-REGISTERED (frozen before run · H_9099 rung-3) · **Registered**: 2026-07-10

## Claim (pre-registration · frozen)
Feeding the runtime lane-23b `self_drift_exp` with **fold8 of the mounted 303M's real pooled
penultimate representation** (`clm_penult_pooled` over each lived experience event: heard user
message + own emit), plus **`.kosmos` self-anchor persistence**, yields a self-continuity trace
that:
- **(i) BEATS-SYNTHETIC** — separates different lived sessions MORE than the current synthetic-axis
  control (session-seed byte-feature / internal-lane argmax int-drift) on the SAME tapes;
- **(ii) preserves H_1471** — anchor-restore recognition > 0.99 + impostor reject unchanged;
- **(iii) self⊥mouth** — the emit stream is BYTE-IDENTICAL with the lane on (Ψ emit-gap ≤ 0.05).

This closes **H_1471 R2b** (real cross-session `.kosmos` persistence — currently the anchor is an
in-memory struct save/restore simulation), and grounds H_9038's content source in the real rep.

## Falsifier (frozen · no tune-to-green)
- grounded divergence ≤ synthetic divergence → 🧱 grounding adds nothing → DO NOT land, keep synthetic.
- ORDER-LOCK fail (same bytes, shuffled event order → trajectory NOT differing) → scope-limited
  partial verdict, verbatim (NOT a re-tune).
- any emit-stream byte diff → wiring defect → reject the run.

## Build spec (4 sites · Fable design 2026-07-10 · ~100 LOC · $0 · +1 trunk forward/event)
1. `core/decode.hexa` — split `clm_penult_pooled_W(W, seed) -> [float]` (loaded-W core; entry =
   load→call→free). Zero math change; re-run committed H_9099 harness as byte-exact no-regression.
2. `core/generator.hexa` — `gen_penult_pooled_W(W, seed)` thin wrapper (read-only, "not a 2nd path").
3. `cli/anima.hexa` — at experience events (heard msg + own emit, co-located w/ C9 REMEMBER):
   `axis = fold8(gen_penult_pooled_W(W, tail_ctx)); self_live_g = self_drift_exp(self_live_g, axis, 0.15)`.
   **fold8 (FROZEN):** sum |pooled[c]| over 8 contiguous d/8=96-wide buckets → argmax → axis∈[0,8).
   Session end → persist `self_live_g` as `.kosmos` self-anchor (kosmos_io single entry); boot →
   restore-if-present else `self_new`. The per-tick `self_ctx` read (:2550 boot constant) stays
   BYTE-UNTOUCHED (self⊥mouth invariant).
4. `cli/chat.py` — 2-production lockstep: same via `clm_forward_hidden(W, _seed_to_tok(ctx,24), 24)`
   + mean-pool T + same fold8 + same anchor format. Parity bar = pooled max|Δ| + identical axis seq.

## Control battery (frozen bars · engine-native on POOL · mini forbidden for 303M)
REAL-SEPARATES (2 sessions diff tapes → cos < 0.99) · **BEATS-SYNTHETIC (headline)** · ORDER-LOCK
(BAR4 retry) · IDENTITY guard (H_1471 non-regression) · MOUTH guard (emit byte-identical · Ψ-gap ≤ 0.05).

## Scope / tier
T=24 window = "lived context" is the last 24 bytes/event (= H_9099 scope; full-context CLML pool = v2).
toy-.clm = DIRECTIONAL; cement on real 303M via py canonical (`anima-py`) + hexa live run on pool;
GREEN-WIRED only with ARCHITECTURE §decode/§SelfIdentity lockstep in the same PR (a_verified_must_wire).

## Links
H_1471 (self-identity · 🟢 · R2b open) · H_9099 (clm_penult_pooled DIRECTIONAL-GREEN 4/5) · H_9038
(self_drift_exp) · H_9209/9225/9226 (self⊥mouth THEATER — self cannot shade emit, must persist not gate) ·
whole-repo unwired census (2026-07-10: self-continuity currently SYNTHETIC not substrate-grounded) · a_kosmos.
