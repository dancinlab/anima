# H_1591 — G4 + G6 gate MEASUREMENT/wiring integrity (lockstep `.hexa`+`.py`)
<!-- @canonical-ok task-specified slug "1591_g4_g6_gate_fix" -->

**Lineage:** same CLASS as **H_1588** (G1 multi-seed reference-match) — fix HOW G4/G6 are
measured/wired so their verdicts are trustworthy; gate DEFINITIONS frozen VERBATIM
(7B_PASS_CONDITIONS.md), NOT tune-to-green (a_break_the_wall). Built ON the G1 fix (cherry-picked
cd33878bf as base) so G1+G4+G6 land coherently. This fix makes G4/G6 MEASURABLE — the terminal
NUMBERS come from the canonical re-score, not declared here (verdict-integrity).

## G6 — ideation gate
**(1) Multi-seed.** `g_eval_g6` parameterized by `base_seed` (`g_eval_g6_seeded`); `base_seed=7`
reproduces the old per-frame `7+i` path frame-for-frame (fixture: wired==inline, dist4 fals0 coher4).
NEW `g_eval_g6_multiseed` re-runs the SAME frozen ladder over `{7,4302,4303}`, GREEN=majority ≥2/3
(reference-match — G6 best-of-K ladders use 4301/4302/4303). So a `fals=0` FAIL is read as a REAL G6
wall ONLY if it survives across seeds, not a single-seed sampler-walk artifact. `proposed, owner-nod-pending`.

**(2) Wiring drift reconcile (audit a89a F3).** CLAUDE.md claimed G6 scoring = wired op
`g6_score_arm`, but `g_eval_g6` reimplemented scoring INLINE (mouth-agnostic via `gen_auto_ideate`)
because `g6_score_arm` hard-codes the CLM-only `gen_clm_ideate`. The true canonical path IS
mouth-agnostic (G6 must score the ByteGPT mouth too). **Fix:** added
`core/g6_ideation.hexa::g6_score_arm_auto` (mouth-agnostic twin of `g6_score_arm`, SAME
DIST/FALS/jaccard logic via `gen_auto_ideate`); `g_eval_g6` now calls THAT op (no dead inline
duplicate → claim TRUE). CLAUDE.md `a_engine_native_learning` G6-채점 line reconciled to cite
`g6_score_arm_auto` as canonical (`g6_score_arm` = H_1381 CLM-only best-of-K research).
- file:line — `core/g_gates.hexa` `g_eval_g6`→`g_eval_g6_seeded`→`g6_score_arm_auto`;
  `core/g6_ideation.hexa` `g6_score_arm_auto`.

**(3) 2-production parity.** The 4 `g6_ideation` pub fns ABSENT from `core/g6_ideation.py`
(`g6_decode_best_of_k`, `g6_decode_best_of_k_W`, `g6_sampler_selftest`, `g6_score_arm`) ported
byte-for-byte + the new `g6_score_arm_auto`. `g6_sampler_selftest` verified ALL-TRUE
(deterministic∧diverse∧in_topk) on mini = the hexa contract.

## G4 — provenance gate (was UNMEASURED — absent from `g_eval_all`)
Diagnosis: G4 genuinely ABSENT from `g_eval_all` (not implemented-but-unwired). a7b_pass per
CLAUDE.md = `G0∧G1∧G2∧G3∧G4`, so G4 missing ⇒ closure UNDER-measured. G4 is a STRUCTURAL/process
gate (7B_PASS §G4: ckpt sha256 recorded · HF upload + card + manifest · PUBLIC iff G0∧G1∧G2) — said
so explicitly and wired what the decode-eval CAN witness: `g_eval_g4` = ckpt **sha256** (the §G4 fact
named first; FIPS 180-4 `sha256_file` / py hashlib), bytes, mouth-decodability, `pub_eligible=closure`
(the §G4 PUBLIC rule the uploader reads). HF-upload/card/manifest flagged `process_external`
(off-engine a_hf_*), NOT silently passed. No softer bar. Wired into `g_eval_all` (.hexa + .py) ⇒ now
COMPUTED + REPORTED in the per-gate tally. Fixture: `g_eval_g4` sha256 == hashlib == `shasum -a 256`,
bytes == os.stat, `provenance_ok=True`.

## Constraints
- **Lockstep byte-parity** — every `.hexa` change mirrored in `.py`; fixed-fixture parity
  (`g4_g6_parity_fixture.{py,hexa}`, same ckpt/seed/gen): py side **ALL-PASS**, hexa twin parses clean
  (full decode parity = canonical install). All 3 hexa files `hexa parse` OK.
- **Frozen-first, NOT tune-to-green** — G4/G6 definitions verbatim; multi-seed variants + closure-flip
  are `proposed, owner-nod-pending`; the frozen single-seed G1/G6 + the G0∧G1∧G2 closure UNCHANGED.
- **No merge** — worktree branch only.

## Terminal numbers — CANONICAL RE-SCORE (post-install, summer/aiden after a2601)
`hexa run cli/anima.hexa -- eval <ckpt> [--corpus …] [--gen N]` (single entry → `gen_auto_ideate` →
`g_eval_all`, now reports G0-G6 INCLUDING G4 + G1/G6 multi-seed). py twin
`python3 core/g_gates.py <ckpt> [corpus …] [--gen N]`. The G6 `fals` TERMINAL (h1129/clm303) =
multi-seed `n_green`/3 + `max_fals` from that run (NOT the toy-d768 fixture). G4 `provenance_ok` +
sha256 from the same run.

**wired:** `proposed, owner-nod-pending` (engine-native re-score pending canonical install; frozen
defaults UNCHANGED; no merge). ARCHITECTURE.json core/ note lockstep updated for the new G4/G6 ops.

**artifacts:** `state/1591_g4_g6_gate_fix/` (VERDICT.md · g4_g6_parity_fixture.{py,hexa} · parity_py.json
· parity_py.out) · `core/g_gates.{hexa,py}` + `core/g6_ideation.{hexa,py}` (worktree, unmerged).
