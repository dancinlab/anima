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

## Honest scope — the match-first follow-up (named, not skipped)
The builder aborts on the RAW paired-episode TOST. Fable's blueprint specified a difficulty-MATCH-first
step (bin by NLL decile, subsample SELF/OTHER to equal counts, THEN TOST the matched pool) — my builder
TOSTs the raw pool (stricter). So the formal open question is whether a difficulty-MATCHED SUBSET of
py303 episodes still carries residual authorship (V6_35 found matched-ΔAUC +0.161 on trained57). This
is NOT closed here. But it is LOW-PRIOR: the raw gap (0.555) is 5× trained57's (0.109), where even the
matched signal was a borderline +0.161; on py303 the SELF/OTHER NLL distributions barely overlap, so a
matched subset would be small, unrepresentative, and near the confound floor. The match-first re-run
(implement decile-subsample in `store_source_build` before the TOST → if matched-balanced, train
seed 7/11 → eval + value-permute + nulls) is the named next step if the store route is pursued further.

## Scope + infra
Real 303M `py303_full.clm` (summer RTX 5070, ~93 min GPU build, sequential SELF sampling), engine-native
`anima-py evaluate --store-source-build` (V6_36 surfaces landed #4492/4494/4495/4496). Log recovered to
`~/.fire-recover/v6_36_store_source/py303_build_s7.log` (a_fire_recover_complete; ABORT → no ckpts to
pull). The full STORE-SOURCE production pipeline works end-to-end; the $0 build gate did exactly its job
— it aborted the pool spend BEFORE train/eval on a difficulty-confounded label. Honest terminal for the
mouth-vs-store redesign: on the real model, agency's label is p7 at source; the store lane carries real
content-addressed VALUE (H_9775) but the authorship VALUE it would carry is not difficulty-orthogonal.
Even a match-first PASS would be "store-routed source memory", not agency (causal-credit test pends).
