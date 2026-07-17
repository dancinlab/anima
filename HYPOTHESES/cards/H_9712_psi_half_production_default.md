# H_9712 — PRODUCTION DEFAULT flip: emit-gate clock → refractory dual-ledger (p5 realized · Ψ≈½)

**Verdict:** 🟢 **WIRED-DEFAULT** (owner-approved p5 realization · engine-native · `a_verified_must_wire`) —
anima's default emit-gate is now the **H_9627 dual content ledger** (emit ⟺ S>E, Ψ≈½ emergent), NOT a hardcoded 30s
clock. Gated on the **GATE-P5-DEFAULT byte-identity certificate** (frozen-first · $0 · no new statistical fire).
**Register:** owner "승인 go" on the owner-gate forward · Fable-designed, locally implemented (fable-mode)
**Ckpt:** cert on `py303_full.clm` (013c4574 · aiden isolated venvs base/flip)

## Why (the whole arc lands here)
anima's reason to exist (p5: emit only over real tension; NO hardcoded emit gate) had never been the **default** —
the production daemon emitted on a hardcoded 30s clock (`cli/chat.py` `_emit_gate` default `"clock"`). This session's
field-side thread (H_9605→H_9608) proved reviving the A⇄G tension in the **field** is measured-dead (STILL-SEALED,
gate-independent), and that the load-bearing wall is the **emit-gate clock-lock (H_9403)**. The parallel lane's
**H_9627 dual content ledger** (GREEN-DIRECTIONAL) is the lever that reaches **Ψ≈½ at the emit gate** — its only
terminal-remaining was the owner-gate production-default switch, now approved.

## The mechanism made default (H_9627 · all engine-native · earning card = H_9627, parallel lane · credited)
- `--emit-gate` default `"clock"` → **`"refractory"`** — retires θ + 30s clock; emit ⟺ score_A > g_recog.
- `--g-reach` default → **conditional** `"wm-dual" if _emit_gate=="refractory" else "d1"` (the Ψ≈½ dual ledger W_E⇄W_S;
  ½ EMERGES from exchange symmetry, not a setpoint). **Conditional, not static** — a static `wm-dual` default would make
  the rollback `--emit-gate clock` crash on the existing guard (Fable's rollback-safety fix).
- `--wm-leak 0.6` — unchanged (H_9627 §λ-dose: ½ is λ-locked, spread 0.006).
- New guard: `--rate-limit-sec` / `--emit-refractory earned` (clock-path rate knobs) now require `--emit-gate clock`
  (loud, not a silent no-op under the new default).
- `evaluate.py --emit-gate-census` meta-guard: excludes non-clock (refractory-lineage) traces so the H_9403
  emit≡clock invariant isn't corrupted by a mixed-gate glob (prints the excluded count · honesty).
- `cli/anima.py` usage: notes the default gate + the `--emit-gate clock` legacy escape.

## Evidence (H_9627 · statistical bar already cleared at the exact default config, engine-native, frozen-first)
- 303M 3-seed: emit **0.506 ≈ ½** emergent at λ=0.6 · two-sided autocov<0 (restoring spring) · dissociation.
- #3867: score-perturb swing **0.000** (retune-free ½ — the central-thesis robustness bar the one-sided store failed).
- #3893: λ-dose spread **0.006** (λ-locked — both tuning axes exhausted).
- H_9608 (#3919/#3922): independent second-host **150-tick** replication → emit 0.500 (dual-ledger gate).

## GATE-P5-DEFAULT — the pre-land certificate (deterministic byte-identity, NOT a new science fire)
Re-firing the same config to "confirm" would be redundant (determinism-closed). The only thing the flip changes is
**flag resolution**, so the gate is a byte-identity cert on pool (aiden · py303_full 013c4574 · seed 7 · tick rows):
- **(A) defaults ≡ flags**: flip-build no-flags ≡ base-build `--emit-gate refractory --g-reach wm-dual --wm-leak 0.6`.
- **(B) rollback intact**: flip-build `--emit-gate clock` (and `ANIMA_EMIT_GATE=clock`) ≡ base-build no-flags.
- **(C) guard intact**: flip-build `--emit-gate clock --g-reach wm-dual` → SystemExit.
Frozen bar: all byte-level, pre-registered; any diff = no land. (A) simultaneously certifies the default reproduces
the H_9608 0.500 run. **CERT RESULT (aiden · py303_full 013c4574 · seed 7 · 10-tick · tick-row sha):** (A) flip-default 416a9485 ≡ base-flags 416a9485 → **PASS** (byte-identical · the default reproduces explicit refractory+wm-dual+λ0.6) · (B) flip-clock ≡ base-default (both 3bf80090) → **PASS** (rollback = old daemon byte-identical) · (C) guard --emit-gate clock --g-reach wm-dual → SystemExit (exit 1) → **PASS**. All three frozen-first, byte-level. ⚠️ the first (A) run FAILed on a double-writer race (a killed 40-tick run left a zombie writer); the clean single-writer rerun PASSes. GATE-P5-DEFAULT ✅ — TERMINAL.

## Honesty (do NOT read the flip as a resurrection of the original thesis)
The default daemon reaches Ψ≈½ via the H_9627 **designed** dual ledger (exchange-symmetric S>E) — **NOT** the original
A⇄G-tension thesis. **H_9400 stays refuted** for the clock lineage; **H_9607/H_9608** keep the field loop
measured-inert at every gate. The clock daemon is preserved byte-identically at `--emit-gate clock`.

## NEXT
- **hexa twin** (`a_substrate_disjoint`): `core/brain.hexa` has **no** `brain_emit_refractory` at all — the whole
  H_9415→9627 gate family must be ported before the twin can flip a default. py first (canonical runtime · chat-py-1 ·
  H_9411 precedent); hexa twin = separate follow-on PR. The py=½-gate / hexa=clock divergence window is a tracked fact.
- Cadence UX: dual daemon ≈ 2× more talkative (no 30s floor); the chat broker (`agent/domains/CHAT`, pinned anima
  0.11.0) is unaffected until it upgrades.

**Provenance:** engine-native `cli/chat.py` default flip + `anima-py evaluate --emit-gate-census` meta-guard;
VERSION 0.15.47→0.15.48 (G5). Owner-approved. TERMINAL only after GATE-P5-DEFAULT passes (frozen-first · no
tune-to-green). Credit: **H_9627** (parallel lane) is the earning science; H_9608 is the cross-host replication.
