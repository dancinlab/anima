---
id: H_9792
title: STORE-VALUE SEED-STABILIZATION — value-echo warmup to make H_9720 CRACK oracle-valid on ≥3 seeds
tier: PROPOSED (lab-full EA divergence · Fable ∥ Sol 수렴 · DESIGN-ONLY · pool cost-gated · NOT a verdict)
frontier: g1-interface-addressable-wall
lane: g1-emergent-address (value-plumbing seed-stability · NOT the address query)
created: 2026-07-18
series: EA-3
related: "[[H_9720]] · [[H_9672]] · [[H_9719]] · [[H_9423]] · cotrained-store-bridge"
source: sidecar lab full (fable claude-fable-5 ∥ sol gpt-5.6-sol · 2026-07-18)
---

# H_9792 (EA-3) — the emergent ADDRESS is fine; the VALUE plumbing is seed-fragile. Stabilize ONLY the value payload path, then re-measure H_9720's unchanged detached L3 readout.

## Why (premise · from H_9720 #4113)
H_9720 CRACK (detached L3-tap readout-route restores held-out lookup) is oracle-VALID and robust on
2 seeds (s7 0.922 · s11 0.836). The 3rd-seed firm-up (s4302) came back near-tie (fresh 0.664 vs
legacy 0.648) **because store-oracle 0.82 < C0-e validity gate 0.90** — the VALUE/store lane was
under-trained on that seed, so the read is INVALID, not a clean negative. Root cause = store-lane
value-read is **seed-fragile** (prior: cotrained-store-bridge s7 ORACLE 0.99 vs s11 0.50). The
address mechanism is not the blocker; the value plumbing is. Promoting H_9720 toward TERMINAL
requires making store-oracle ≥ 0.90 reproducibly across ≥3 seeds WITHOUT any address supervision.

## Claim (one line · falsifiable)
A value-only stabilization warmup (self-supervised value round-trip, no `target_slot` anywhere)
raises store-oracle ≥ 0.90 on ≥3/5 seeds {7,11,4302,4303,9423} (incl s4302) while leaving the
detached L3 address readout byte-untouched at the terminal training regime ⟹ H_9720's fresh−legacy
lookup gap re-appears on the newly-valid seeds. `a_substrate_disjoint`: value ⊥ address.

## Mechanism (engine-native · primary = Fable, fallback = Sol)
**PRIMARY — `anima-py train --store-echo-weight <w> [--store-echo-anneal <n:m>]`** (Fable):
at each store WRITE, immediately read back at the model's OWN write address `a_w` under stop-grad
(`sg(a_w)`), decode, and add `w · CE(decode(read(sg(a_w),S)), v_target)` to the loss. Gradient
reaches ONLY {value encoder, write projection, store cells, value decoder}. `w=0` (default) builds
no term, no RNG, no graph change = byte-identical. Schedule = warmup-anneal (NOT freeze/thaw):
`w=1.0` for steps 0→0.4T, linear `w→0` over 0.4T→0.6T, then `w=0` for the release window (≥40% of
T) so the **terminal regime is bit-for-bit the H_9720 objective** (fresh:64@3, stop-grad into trunk,
store-CE only, no addr-loss). Boundaries = fixed pre-registered step counts (NOT gated on an in-train
echo metric — `a_train_inline_gauge`; echo accuracy logged monitor-only). Admissibility is
**structurally trivial**: `target_slot` is used NOWHERE at train time, so `∂L_echo/∂θ_query ≡ 0`
identically and no oracle statistic exists in any lane.

**FALLBACK / Sol dissent — `--store-value-stabilize oracle-mux:2000,lock:1000`** (Sol · NOVEL):
2-phase freeze/thaw. Phase-A (0–2000): freeze trunk + L3 tap + query/router + keys + slot-embeds +
address logits; `target_slot` drives a NON-differentiable store-side mux; train only value
enc/write/read/decoder (value params slot-shared, no slot-indexed weights). Phase-B1 (2000–3000):
destroy mux, freeze warmed value params, enable H_9720 query, new query-lane optimizer state.
Phase-B2 (3000→T): continue H_9720, value frozen. Admissibility via HARD graph+param firewall +
C-F taint audit (below). Escalate to this ONLY if PRIMARY passes toy byte-parity but fails to lift
pool oracle (⟹ fragility is slot-ASSIGNMENT, not value-FIDELITY — which the self-supervised echo
cannot fix). Sol threshold stricter (all-5 ≥0.90, 4/5 ≥0.95); Fable's fidelity-lever is the safer
first attempt because it can never be accused of address supervision.

Cheap simplicity fallback (toy-only): `--store-value-lr-mult` — if a plain value-lane LR bump
matches echo on toy oracle, it wins on Occam and replaces the flag (same experiment/controls).

## Controls (≥3) + $0 pre-screen
- **C-A / C-V0** — matched original H_9720, same seeds/steps, NO stabilization: confirms untreated
  s4302 oracle-failure reproduces (else "fragility" was a one-off, whole premise dead).
- **C-B / C-V1** — **load-bearing confound**: SAME warmup on the **legacy-penult** query (Fable) OR
  compute/param-matched non-oracle predicted-routing warmup (Sol). If stabilization lifts *legacy*
  lookup too, the gain was value plumbing not the L3 tap ⟹ H_9720 depth claim confounded, re-scope.
  Lever must BEAT this control by pre-set margin (Sol: min-seed oracle > C-V1 by ≥0.05).
- **C-shuffle (address mediation)** — H_9720's C3 eval on every valid ARM model: store-oracle stays
  within 0.02 of unshuffled but emergent-query lookup collapses to ≤0.55 ⟹ still address-mediated.
- **C-F (info-flow taint audit · $0)** — trace: zero `target_slot` taint and zero grad/update in any
  query/address param; no slot-indexed value state. Any violation KILLS as supervised contamination.
- **$0 pre-screen (mandatory · never-run-instrument lesson)**: toy end-to-end 2-seed CPU — (i)
  flag-absent byte-parity by ckpt hash, (ii) echo/warmup loss actually moves toy oracle, (iii)
  `target_slot`-change moves only mux indices not query tensors, (iv) exit=0 + artifacts + controls.

## Pre-registered PASS / KILL (frozen before fire · no tune-to-green)
- **Validity gate (read FIRST)**: ARM store-oracle ≥ 0.90 on ≥3/5 seeds **incl s4302**; else the
  stabilization lever FAILS and NO lookup number is read.
- **PASS (promotes H_9720 toward TERMINAL)**: on ≥3 valid-oracle seeds, fresh−legacy(C-B-paired)
  ≥ +0.10 (Fable) / ≥ +0.05 with positive 5-seed paired mean and no seed < −0.02 (Sol), AND
  C-shuffle collapse ≥ 0.15 each.
- **KILL branches** (table covers below-chance · prereg discipline): (a) validity gate missed →
  value-lever dead; (b) valid seeds but Δ(fresh−legacy) < 0.05 majority incl any legacy>fresh
  reversal → H_9720 CRACK was seed-lucky → DOWNGRADE H_9720; (c) C-B legacy rises within 0.05 of
  fresh → depth claim confounded → re-scope; (d) shuffle fails to collapse → not address-mediated →
  INVALID for promotion.

## Cost
$0 pre-screen (byte-parity + toy oracle move + firewall audit) → pool-GPU: gate on first
{11,4302,7}+C-V0 (continue only if all ≥0.90 incl s11,s4302 AND taint audit clean) → full 5-seed
+ C-B on {11,4302,9423} + C-shuffle/C-F on every valid seed. ~10 runs, one dedicated host per
track (wall = max(track)), ckpt → `~/anima-weights/` BEFORE any teardown. ~$25–40.

## Verdict-integrity self-check
(1) Certifying the instrument (store-oracle ≥0.90 validity precondition) is NOT tune-to-green on the
DV — oracle is C0-e, the lookup gap is the claim; they are separate. (2) A PASS reads "H_9720 CRACK
re-validates once value plumbing is seed-stable", NOT "the value warmup created the address" — the
address readout is byte-untouched at terminal regime and C-B/C-shuffle guard the attribution.
(3) A KILL of the value-lever does NOT kill H_9720's 2-seed CRACK (s7·s11 remain oracle-valid); it
only means the 3rd+ seeds stay uninterpretable and H_9720 holds at DIRECTIONAL-STRONG. (4) Any
number here is DIRECTIONAL until produced by `anima-py evaluate` on the 303M py channel
(`a_engine_native_learning`).
