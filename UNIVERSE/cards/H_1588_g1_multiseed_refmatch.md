# H_1588 — G1 RECOMBINATION multi-seed reference-match (the TRUE seed-robust status)

**Lineage:** builds on **H_1587** (ad13: the engine-native G1 FAIL on h1129 is a *sampler-method
artifact* — forward byte-faithful, weights bit-exact, only the xorshift32 inv-CDF vs torch
multinomial+Gen(7) RNG walk diverges). H_1588 IMPLEMENTS ad13 path-1: make the G1 verdict
**seed-robust** so it no longer hinges on one fragile RNG walk, then RE-SCORE the live ckpts.

## The fix (frozen-first, NOT tune-to-green)
The recombination DEFINITION is frozen **VERBATIM** (7B_PASS_CONDITIONS / a7b_pass / H_1129):
for some k∈{2,3,4,5}: `composed_distinct ≥ 2 AND > max_single AND coherent(kwr≥0.50)`. The ONLY
change is **seed-robustness**: re-run the SAME frozen ladder over seeds **{7, 4302, 4303}**
(reference-match — the G6 ladders use [4301/4302/4303]; 7 = the H_1129 single-seed default) and
define GREEN = recombination clears in a **MAJORITY** (≥2/3). Applied SYMMETRICALLY to BOTH the
torch reference path AND the engine path. No bar moved; the metric is made robust to the exact RNG
walk. (a_break_the_wall class-(a) measurement-artifact repair · a_engine_native_learning reference-match.)

## Lockstep 2-production change (PROPOSED, owner-nod-pending — NO merge)
`core/g_gates.hexa` + `core/g_gates.py` (byte-parity lockstep):
- `g_eval_g1` parameterized by `base_seed` (default 7 reproduces the original single-seed path
  byte-for-byte; singles seeded `base_seed+s`, composed seeded `base_seed`).
- NEW `g_eval_g1_multiseed` (.hexa `g_eval_g1_seeded`/`g_eval_g1_multiseed`): runs the ladder over
  {7,4302,4303}, GREEN = strict majority. Tagged `status: "proposed, owner-nod-pending"`.
- `g_eval_all` now reports BOTH; **closure stays on the FROZEN single-seed G1** until owner approves
  the default flip.
- Byte-parity fixture `state/1588_g1_multiseed_refmatch/g1_parity_fixture.{hexa,py}` — same
  ckpt/seed/gen → identical per-seed counts (the metric is a deterministic fn of decode text).

## RE-SCORE — the TRUE recombination status (per-ckpt multi-seed)

| ckpt | engine | seed 7 | seed 4302 | seed 4303 | multi-seed G1 |
|---|---|---|---|---|---|
| **ByteGPT-303M h1129** | torch-ref (multinomial+Gen) | GREEN | GREEN | GREEN | **GREEN 3/3** |
| **ByteGPT-303M h1129** | py engine (bytegpt_decode) | — | — | — | **PARTIAL** (in-flight; host released for canonical reinstall → RE-RUN on `anima eval`) |
| **clm303_clean** (.clm deep-mouth) | py engine (clm_decode) | FAIL | FAIL | FAIL | **FAIL 0/3 (GENUINE)** |

clm303_clean per-seed: max_single=0 on all; best_composed = 1/0/0 → never reaches distinct≥2.

### clm303_clean FULL engine-native G0-G6 (scope-extension, py 2-production, FIRST complete)
G0 **PASS** 5/5 · G1 single-seed **FAIL** · G1 multi-seed **FAIL 0/3** · G2 **PASS** (33 novel,
ctrl 0) · G3 ok (continuity 0.99995) · G5-L1 **PASS** (0.2647) · G6 **FAIL** (dist 5, fals 0) →
**a7b_pass (G0∧G1∧G2) = FAIL** (genuine G1 wall, confirmed seed-robust). Byte-parity decode gate
PASS (hexa==py byte-identical, CE 15-decimal). The py engine sidesteps the hexa farr-leak OOM +
codegen blockers that previously prevented clm303's engine-native G0-G6 from completing.

- **h1129 torch reference: GREEN 3/3** — confirms the H_1129 🟢 is robust, not single-seed luck.
  RETRACTS the "engine FAIL ⇒ ByteGPT-303M can't recombine" inference (H_1587 already diagnosed
  the engine single-seed FAIL as sampler-walk; multi-seed makes that quantitative).
- **clm303_clean: FAIL 0/3 — GENUINE, not a sampler artifact.** Across all 3 seeds the best composed
  distinct never exceeds `max_single` (best_composed ≤ 1, max_single 0). clm303_clean does NOT
  recombine the H_1129 concept sets. Honest result (c9): clm303's G1 FAIL stands under the corrected
  seed-robust metric — its a7b_pass closure (G0∧G1∧G2) remains FAIL on the G1 axis.

## Honest framing (c2/c9/a_break_the_wall)
This is **reference-match** (single-seed → seed-robust; definition unchanged), **NOT** tune-to-green.
It does the opposite of cherry-picking: a single seed could flip either way; the majority-of-3 metric
is the conservative, comparable measurement. The result is split and reported plainly — **h1129
recombines (GREEN), clm303_clean does not (FAIL)** — exactly the kind of honest mixed verdict the
frozen-first discipline is for.

**wired:** `proposed, owner-nod-pending` (DIRECTIONAL → engine-native re-score done; frozen-default
flip awaits owner approval; no merge). Single-seed G1 remains the live frozen default.

**artifacts:** `state/1588_g1_multiseed_refmatch/` (g1_multiseed.py · result JSONs · parity fixture ·
VERDICT.md) · `state/verdicts/1588_g1_multiseed_refmatch/` · proposed `core/g_gates.{hexa,py}` diff
on worktree branch (unmerged).
