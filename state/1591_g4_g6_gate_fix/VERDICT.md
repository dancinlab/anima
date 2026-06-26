# H_1591 — G4 + G6 gate MEASUREMENT/wiring integrity fix
<!-- @canonical-ok task-specified slug "1591_g4_g6_gate_fix" -->

**Class:** same as the G1 multi-seed fix (H_1588) — fix HOW G4/G6 are measured/wired so their
verdicts are trustworthy; gate DEFINITIONS unchanged (frozen-first, NOT tune-to-green).
**Base:** cherry-picked the G1 multi-seed reference-match (cd33878bf) so G1+G4+G6 land coherently.
**Status:** measurement made TRUSTWORTHY — the terminal G4/G6 NUMBERS come from the canonical
re-score (below), NOT declared here. Lockstep `.hexa`+`.py`, both parse clean; py fixture ALL-PASS.

---

## G6 — ideation gate (multi-seed + wiring reconcile)

### (1) Multi-seed robustness
- `g_eval_g6` parameterized by `base_seed` (`g_eval_g6_seeded`); `base_seed=7` reproduces the old
  per-frame `7+i` path frame-for-frame (fixture (A): wired arm == old inline, dist=4 fals=0 coherent=4).
- NEW `g_eval_g6_multiseed` re-runs the SAME frozen ladder over `{7,4302,4303}`, GREEN = majority
  ≥2/3 (reference-match: G6 best-of-K ladders use 4301/4302/4303). `status="proposed, owner-nod-pending"`.
- So a `fals=0` FAIL is now read as a REAL G6 wall ONLY when it holds across seeds, not a single-seed
  sampler-walk artifact. **Fixture observation (toy d768, NOT the verdict ckpt):** fals=0 on all 3
  seeds (`max_fals=0`) — i.e. on this tiny ckpt fals=0 is seed-robust. The h1129/clm303 TERMINAL
  number must come from the canonical re-score below.

### (2) Wiring drift reconcile (audit a89a F3)
- **CLAUDE.md claimed** G6 scoring = the wired op `g6_score_arm`, but `g_eval_g6` REIMPLEMENTED the
  scoring INLINE (mouth-agnostic via `gen_auto_ideate`) because `g6_score_arm` hard-codes the CLM-only
  `gen_clm_ideate`. The true canonical path IS the mouth-agnostic one (G6 must run on ByteGPT too).
- **Fix:** added `core/g6_ideation.hexa::g6_score_arm_auto` — the mouth-agnostic twin of
  `g6_score_arm` (SAME DIST/FALS/jaccard logic, decode via `gen_auto_ideate`). `g_eval_g6` now calls
  THAT op (no dead inline duplicate → the "G6 scoring = wired engine op" claim is TRUE).
  - file:line — `core/g_gates.hexa` `g_eval_g6` → `g_eval_g6_seeded` → `g6_score_arm_auto`;
    `core/g6_ideation.hexa` `g6_score_arm_auto`.
- **CLAUDE.md reconciled** (a_engine_native_learning, the G6-채점 line): now cites
  `g6_score_arm_auto` (mouth=`gen_auto_ideate`) as canonical; `g6_score_arm`/`g6_decode_best_of_k`
  flagged H_1381 best-of-K research (CLM-only).
- **2-production drift:** the 4 `g6_ideation` pub fns absent from `core/g6_ideation.py`
  (`g6_decode_best_of_k`, `g6_decode_best_of_k_W`, `g6_sampler_selftest`, `g6_score_arm`) are now
  ported byte-for-byte + the new `g6_score_arm_auto`. `g6_sampler_selftest` verified ALL-TRUE
  (deterministic ∧ diverse ∧ in_topk) on mini, matching the hexa contract.

## G4 — provenance gate (was UNMEASURED — absent from `g_eval_all`)

- **Diagnosis:** G4 was genuinely ABSENT from `g_eval_all` (not implemented-but-unwired). CLAUDE.md
  a7b_pass = `G0∧G1∧G2∧G3∧G4`, so G4 missing ⇒ the closure tally was UNDER-measured.
- **G4 is a STRUCTURAL/process gate** (7B_PASS §G4: ckpt sha256 recorded · HF upload + model card +
  manifest · PUBLIC iff G0∧G1∧G2), NOT a generation score — said so explicitly and wired the part the
  decode-eval CAN witness: `g_eval_g4` computes **ckpt sha256** (the §G4 fact named FIRST, FIPS 180-4
  `sha256_file` / hashlib), bytes, mouth-decodability, and carries `pub_eligible = closure` (the §G4
  PUBLIC rule the uploader reads). HF-upload/card/manifest are flagged `process_external` (off-engine,
  a_hf_*), NOT silently passed. No softer bar invented.
- Wired into `g_eval_all` (both `.hexa` + `.py`) so G4 is now COMPUTED + REPORTED in the per-gate tally.
- **Fixture (C):** `g_eval_g4` sha256 == python hashlib == system `shasum -a 256`; bytes == os.stat;
  `provenance_ok=True`, `mouth=clm`. Provenance is now witnessable.

## Constraints honored
- **Lockstep + byte-parity:** every `.hexa` change mirrored in `.py`; fixed-fixture parity check
  (`g4_g6_parity_fixture.{py,hexa}`, same ckpt/seed/gen) — py side ALL-PASS; hexa twin parses clean
  (full decode parity runs on the canonical install).
- **Frozen-first, NOT tune-to-green:** G4/G6 DEFINITIONS verbatim from 7B_PASS_CONDITIONS.md. The
  multi-seed variants + the closure-flip are `proposed, owner-nod-pending`; the frozen single-seed
  G1/G6 + the G0∧G1∧G2 closure are UNCHANGED.
- **No merge** — committed to the worktree branch only. Smoke = `hexa parse` clean on all 3 files.

## CANONICAL RE-SCORE (the terminal G4/G6 numbers — run post-install)
On a canonical `hx install`'d host (summer/aiden, once a2601 reinstall finishes), engine-native:

    hexa run cli/anima.hexa -- eval <ckpt.clm|.bin> [--corpus <path>...] [--gen N]

(single entry → generator L3 `gen_auto_ideate` → g_eval_all → now reports G0-G6 INCLUDING G4 + the
G1/G6 multi-seed variants). The 2-production py twin:

    python3 core/g_gates.py <ckpt> [corpus ...] [--gen N]

The G6 `fals` TERMINAL verdict (h1129 ByteGPT-303M, clm303_clean) = the **multi-seed** `n_green`/3 +
`max_fals` from that run (NOT the toy-ckpt fixture numbers above). G4 `provenance_ok` + the recorded
sha256 come from the same run.
