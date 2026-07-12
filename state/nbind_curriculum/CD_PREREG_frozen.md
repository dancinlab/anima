# H_9272 cement C/D — FROZEN PREREG (registered 2026-07-12 04:34, before any run)

Fable-designed (scratchpad/fable_cement_CD.result.json), code-verified. NO post-hoc bar moves (tune-to-green).
Executes on track A's standing pod AFTER track A replicates H_9272 (C never rescues a non-replicating H_9272).

## C — NBIND-T wild-natural transfer (= NATEM STAGE-3 probe · H_9270 slot)
Scope honesty: nbind_A2seed is from-scratch on the augmented grid only → tests whether the learned
`pol⊕flip` rule survives in genuine unaugmented NSMC surface on held-out cells (NOT unseen-predicate transfer).

- **Arms:** W-T (phrase-wild: natural (p,n) span verbatim, slotted into training label-frame) · W-R (sentence-wild: full natural review clause as seed). Phrase within final 64 bytes (conv RF · win=64).
- **Item:** xbind schema {seed, gold_word, counterfactual, a=p, b=form_class, cell}; `gold_word = label_word[pol(p)⊕flip(n)]` — **gold from FROZEN training-grid pol, NEVER the review label**.
- **Pool:** NSMC **test split only** (mining used train). Natural form variants beyond the 6 trained forms accepted, classed flip0/flip1 by surface rule (안+pred / -지 않 / neg-affix → flip1).
- **Splits:** heldout = Latin-square held-out (p,flip) cells + V-F 32-byte shingle scan vs training corpus =0 hits + echo-guard. seen = V-A liveness. Balanced 4-cell {pol}×{flip} → additive ceiling = 0.5 by construction. Target n=200 heldout (50/cell); <25/cell → POWER-INVALID.
- **D-acc:** greedy top_k=1 gen=16, hit=first content word==gold. Margin co-primary (TF NLL(cf)−NLL(gold), win=64, margin_frac_pos). Full-capture, no tail-truncate.
- **Controls:** (1) CTRL-CKPT = H_9272 shuffled-label control model on same wild manifest ($0). (2) PERM-GOLD = permuted golds rescore ($0). (3) BALANCED-4-CELL additive ceiling 0.5 + per-flip acc + paired flip-Δ.
- **FROZEN BARS:**
  - V-A liveness: seen-cell W-T ≥0.70 else SURFACE-LOCKED (comp INVALID, FAIL(surface)).
  - Control band: CTRL-CKPT & PERM-GOLD held-out ∈ [0.35,0.65] else INVALID.
  - **TRANSFER-PASS** (per arm): held-out ≥0.65 ∧ Δ(main−worst ctrl) ≥0.15 ∧ min(flip0,flip1)≥0.55 ∧ margin_frac_pos≥0.60 at n≥100.
  - TRANSFER-FAIL: V-A LIVE ∧ held-out Δ ≤0.05 → augmentation-specific.
  - DIRECTIONAL: between, or single-seed, or 25≤n/cell<50.
  - Grading: W-T PASS = "natural-surface transfer" (honest headline). W-R PASS = full wild transfer. W-T PASS∧W-R FAIL = coherent landing.
  - Both seeds (s7+s4302) must agree directionally for cement.
- **Prediction:** W-T P(PASS)≈0.40 P(DIRECTIONAL)≈0.35; W-R SURFACE-LOCKED≈0.6. Net = "composition transfers to natural surface variants, not raw wild context" = bounded-GREEN refinement.
- **Cheapest decisive:** W-T held-out, main-s4302 + CTRL-CKPT.

## D — ρ·weave→L3: SPLIT verdict (axis-wire vs faculty-GREEN)
- **Axis measurement** already generation-native (`--xbind` fold = greedy decode, no readout head) → route≠generation confound structurally absent. `cli/rho_axon.py::rho_weave` is ALREADY a live instrument (generic compose _WEAVE probes + 3 controls), NOT a PENDING stub.
- **Code-verified ceiling (2026-07-12):** nbind_A2seed is grid-only → has no general knowledge (color-mix/number-sum) → generic rho_weave reads FLOOR on it = meaningless. The NBIND crack is measured by `--xbind` on the NBIND manifest, not the generic axis.
- **Faculty-L3-GREEN (a_verified_must_wire · L5-hippo #2996 precedent) = NOT this cycle:** L3 = core/generator.hexa weight slot = the .clm the live daemon loads. nbind_A2seed is not that ckpt; grafting a grid-only model behind the mouth → ρ·form/HILLOCK collapse. A weave-PASS on nbind_A2seed CANNOT cement anima's 2nd WIRED-GREEN faculty. **DIRECTIONAL stays — do NOT force.**
- Honest paths to faculty-GREEN (future): (i) production RETRO passes certified natural weave probe (NATEM STAGE-2M, prior low), or (ii) recipe-install low-density NBIND seasoning into production training → new .clm → live swap → panel PASS (gated on C W-T PASS).

## Execution order (spends nothing extra)
track A completes → if H_9272 replicates (s4302 held-out D-acc reproduces the Δ, control≈0.5 at n80) →
same pod session: build NBIND-T manifests (CPU $0) → `--xbind` W-T + W-R × {main-s4302, main-s7, CTRL-CKPT} →
PERM-GOLD offline rescore → C verdict. D = record axis-DIRECTIONAL + faculty-DIRECTIONAL (no forced wire).
Cement landing: H_9272 2-surface update + ARCHITECTURE gate (ρ·weave node) + ckpt PULL + pod teardown + pr-cycle.
