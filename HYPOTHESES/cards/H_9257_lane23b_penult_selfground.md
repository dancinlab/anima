# H_9257 — lane-23b penult self-grounding (self-continuity: synthetic → substrate-grounded)

**Slug**: `lane23b_penult_selfground` · **Tier**: 🔧 WIRED (4-site landed · toy DIRECTIONAL · 303M control-battery PENDING pool) · **Registered**: 2026-07-10 · **Wired**: 2026-07-10

> **wired:** engine-native (hexa `cli/anima.hexa` + 2-production py twin `cli/chat.py`, both live) — ARCHITECTURE §decode + §SelfIdentity lockstep landed same PR. **303M control-battery = PENDING pool** (REAL-SEPARATES / BEATS-SYNTHETIC / ORDER-LOCK not yet run — toy .clm only cements DIRECTIONAL).

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

## Wire status (2026-07-10 · toy DIRECTIONAL)
4 sites landed on `feat/lane23b-build`:
1. `core/decode.hexa` — `clm_penult_pooled_W(W, seed)` split out; entry = load→_W→free (**ZERO math
   change**, pure refactor). `penult_fold8(pooled)` FROZEN reducer added. + py twin `core/decode.py`
   `clm_penult_pooled_W` (= `clm_forward_hidden` + mean-pool) + `penult_fold8`.
2. `core/generator.hexa` — `gen_penult_pooled_W(W, seed)` read-only wrapper (+ py twin
   `core/generator.py`). Single L3 entry, emits no bytes.
3. `cli/anima.hexa` — lane-23b: boot restore-else-`self_new` + heard-context (session_seed) drift ·
   own-emit drift at C9 REMEMBER · session-end `.kosmos` self-anchor persist (dedicated dir, never
   `kdir`). `self_ctx` (:~2585) BYTE-UNTOUCHED.
4. `cli/chat.py` — full 2-production twin of all three (same fold8, same anchor format).

**Verification (this PR):**
- **self⊥mouth (go/no-go safety gate) — PASS.** 12-tick toy chat, lane-on (`cli/chat.py`) vs
  origin/main lane-off, same tape: emit-stream stdout **byte-identical** ∧ `kdir` emit-anchors
  **byte-identical** (once `emitted_at` wall-clock — kosmos_io's own parity-masked field — is masked).
  Only new output = the `LANE-23b self-g` lines + the separate self-anchor. Emit never diverges.
- **.kosmos self-anchor round-trip — PASS.** Persisted at session end to `~/.anima_kosmos_self/
  self_live.kosmos`; `_selfg_restore` reads it back at boot (`SELFG8:` payload → `self_from_vec`).
- **2-production parity — PASS (summer pool, hexa v0.609).** `state/9257_lane23b/parity.py`
  (+`parity_hexa.hexa`): hexa `gen_penult_pooled_W` vs py `clm_penult_pooled_W`, exact `float_to_bits`
  dump → **pooled max|Δ| = 1.665e-16 ≤ 2e-16** ∧ **fold8 axis-seq identical** (6/6 seeds). (mini hexa
  `runtime.a` lacks `forge_dispatch_attn_core/rmsnorm` symbols — infra fault, so the hexa side runs on
  pool, not mini.)
- **byte-exact no-regression — PASS (summer pool).** `state/9257_lane23b/nogr_probe.hexa` dumps the
  `clm_penult_pooled` ENTRY bits: origin/main vs the `_W`-split tree = **byte-identical** (all seeds).
  Cross-check: the entry's bits == `clm_penult_pooled_W`'s bits (via `gen_penult_pooled_W`) for shared
  seeds → the split is a pure refactor, ZERO math change.
- toy `.clm` = **DIRECTIONAL**; **303M control-battery (REAL-SEPARATES · BEATS-SYNTHETIC headline ·
  ORDER-LOCK · IDENTITY · MOUTH guard) = PENDING POOL** (`anima-py` + hexa live run, summer/aiden) —
  the terminal verdict re-measures on real 303M, not this toy build. No tune-to-green: fold8 buckets
  + falsifier FROZEN.

## Links
H_1471 (self-identity · 🟢 · R2b open) · H_9099 (clm_penult_pooled DIRECTIONAL-GREEN 4/5) · H_9038
(self_drift_exp) · H_9209/9225/9226 (self⊥mouth THEATER — self cannot shade emit, must persist not gate) ·
whole-repo unwired census (2026-07-10: self-continuity currently SYNTHETIC not substrate-grounded) · a_kosmos.
