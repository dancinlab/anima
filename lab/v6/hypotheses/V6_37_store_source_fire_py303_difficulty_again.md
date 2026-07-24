<!-- @hypothesis-ok lab/v6 rule-exempt sandbox: v6 hypotheses live in lab/v6/hypotheses/V6_<n>_*.md per lab/v6/CLAUDE.md, never the parent HYPOTHESES/ nor an H_ id -->

# V6_37 — STORE-SOURCE fire on the REAL 303M: DIFFICULTY-AGAIN (authorship label is difficulty-confounded at source)

**origin:** the STORE-SOURCE pipeline (V6_36: lane_type 9 codec + eval/train/build surfaces, all
landed + $0-verified) fired on the real 303M `py303_full.clm` on the summer pool host (RTX 5070,
`[GPU-FIRED] CUDA cupy 14.1.1`). This is the decisive P0 build gate — the $0 pre-registered ABORT
that decides whether a store-routed agency faculty is even testable on the real model. DIRECTIONAL.

## RESULT — 🔴 DIFFICULTY-AGAIN (pre-registered ABORT fired on the real 303M)
`anima-py evaluate py303_full.clm --store-source-build --corpus en_general.txt --build-prompts 800`:
- 318 cue-paired words · 636 episodes (318 SELF / 318 OTHER)
- **difficulty TOST: self_nll = 1.148 vs other_nll = 1.703 · diff = −0.555 → NOT balanced → ABORT**

The SELF spans (py303's OWN temperature-sampled continuations) are far more predictable TO py303
(NLL 1.148) than the natural continuations (1.703) — a 0.555-nat gap, **5× the 0.109 gap trained57
showed** (V6_35). The stronger the model, the more trivially self-predictable its own output, so the
authorship label SELF-vs-OTHER collapses into a difficulty signal AT THE SOURCE. The builder's
pre-registered TOST gate (`abs(diff)+2se < 0.15`) fires ABORT: routing this label through the store
would route DIFFICULTY, not agency (p7-aligned), so no train/eval spend is warranted.

## Reading — the store channel does NOT rescue agency on the real model
This completes the redesign arc's mechanism on the real 303M: **agency has no difficulty-orthogonal
label to route through ANY channel.** V6_33/34 showed the MOUTH channel is difficulty-complete; V6_37
shows that even for the NON-mouth content-addressed store channel, the authorship label it would carry
is itself a difficulty shadow on the strong model (self-generated text is trivially self-predictable).
Converges hard with frontier R9 (agency UNIDENT): agency reads as absent because there is no
difficulty-orthogonal agency signal to instrument — on the real model the very label is p7.

## The match-first follow-up — RUN, and it CLOSES the edge (measured, not argued)
The first build aborted on the RAW paired-episode TOST, leaving one honest open edge: does a
difficulty-MATCHED subset still carry authorship (V6_35 found matched-ΔAUC +0.161 on trained57)?
`--store-source-build` was extended with **match-first that PRESERVES cue-pairing** — a paired word is
usable only if its SELF and OTHER spans are per-word difficulty-balanced (|nll_s − nll_o| <= 0.15),
the only construction satisfying BOTH the address-leak kill (same word both sides) and the
difficulty-confound kill — and re-fired on py303 (summer GPU, 400 prompts, seed 7):

| | measured |
|---|---|
| paired words | 142 (284 episodes, 142 self / 142 other) |
| **balanced-pair words (|nll_s−nll_o| ≤ 0.15)** | **10 / 142 = 7%** — too few for even ONE 8-slot ring set (needs 4·n_slot = 32) |
| raw TOST | self_nll 1.147 vs other_nll 1.750, diff −0.603 (replicates the 800-prompt −0.555) |

⟹ **STRUCTURAL DIFFICULTY-AGAIN, measured.** On a strong generator the two constraints are mutually
incompatible: cue-pairing forces an easy-SELF span to be paired with a hard-OTHER span for the SAME
word (self-generated text is uniformly more self-predictable), so difficulty-matching can only keep
the thin 7% overlap band — not enough to build a manifest. The edge flagged in the first pass is
therefore CLOSED by measurement, not by the structural argument alone.

## Scope + infra
Real 303M `py303_full.clm` (summer RTX 5070, ~93 min GPU build, sequential SELF sampling), engine-native
`anima-py evaluate --store-source-build` (V6_36 surfaces landed #4492/4494/4495/4496). Log recovered to
`~/.fire-recover/v6_36_store_source/py303_build_s7.log` (a_fire_recover_complete; ABORT → no ckpts to
pull). The full STORE-SOURCE production pipeline works end-to-end; the $0 build gate did exactly its job
— it aborted the pool spend BEFORE train/eval on a difficulty-confounded label. Honest terminal for the
mouth-vs-store redesign: on the real model, agency's label is p7 at source; the store lane carries real
content-addressed VALUE (H_9775) but the authorship VALUE it would carry is not difficulty-orthogonal.
Even a match-first PASS would be "store-routed source memory", not agency (causal-credit test pends).
