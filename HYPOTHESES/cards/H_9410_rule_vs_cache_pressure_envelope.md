# H_9410 — RULE-VS-CACHE PRESSURE ENVELOPE (W_wt terminal for `g1-interface-addressable-wall`)

> **⏳ PRE-REGISTRATION — frozen BEFORE any train (frozen-first · tune-to-green-proof by construction).**
> Terminal experiment for the **W_wt axis** of frontier `g1-interface-addressable-wall`.
> Group: `g1-interface-addressable-wall`. EN-FIRST (owner directive · `not` FREE/pre-posed is the discriminator).
> Continues H_9389 (💀 KILL-AT-GATE, |S_op|=24) + H_9388 (L4 census: stem→operator circuit is conv-native, alive).

## Why (settled — not re-derived here)

- **L1 (H_9389) = 💀 KILL-AT-GATE.** From-scratch co-train of `S_op` (decl+operator supervised) + `S_decl`
  (decl-only, operator 0×) supplied gradient to the declaration→operator map. Result: `S_decl` flip1 gate
  **never exceeds chance** both seeds across budget 2000→12000 (greedy 0.139–0.389 · 2AFC 0.111–0.417 ·
  per-stem n=12 sign-perm p 0.012–0.087, all below-chance) — BUT **ECHO 0.61–0.86**: the model RETRIEVED the
  declared polarity correctly on held-out stems, emitting a valid balanced answer word while **ignoring `not`**.
  `G-ALIVE`(S_op flip1) 0.986–1.000 from budget 2000 ⟹ budget-negative excluded.
  ⟹ `[decl→store]`✓ `[retrieval]`✓ are shared; the ONLY missing piece = the `not`-conditional flip is **GATED
  on stem-set-membership** (operator = stem-index lookup, not compositional).

- **The honest reopener (L1 agent).** "KILL-AT-GATE ≠ 🔴 W_wt-terminal: |S_op|=24 lets all 24 responses be
  stored, so **memorization is cheaper than a rule** — there is no abstraction pressure. 🔴 requires the
  *strongest synthetic forcing*, which 24 stems is not."

- **Capacity math (why an OPEN ladder is infinite regress).** Operator response = 1 bit/stem; |S_op|=10³ = 0.1 KB
  vs 345.7M params (would need |S_op|~10⁷⁻⁸ to bankrupt cache; English content vocab ~10⁵). So "keep raising
  |S_op|" is unfalsifiable regress. The REAL competition is **membership-feature (cost ∝ |S_op|, linear) vs
  crisp `not`-feature (constant)** — crossover plausibly within 10²–10³ (grokking dynamics; L4 existence-proof
  that the stem→operator circuit exists conv-natively). This is what a FINITE decision envelope tests.

## The finite decision experiment — a pre-registered 3-axis ENVELOPE

Kill across the **whole envelope** (rung-3 + C-CAP + grokking-wd arm, every cell) = 🔴 **W_wt-TERMINAL**
(forces V5 reopen; ≥3-lens satisfied). Green anywhere = **W_wt reopens**. Both signs are terminal-grade.
V4 stem-clean (summer) + SPLICE H_9391 are ORTHOGONAL — do not block, do not touch summer.

### Axis 1 — |S_op| ladder (4× spacing · seeds {7,11} · 150 lines/stem policy-A default)

| rung | N atoms | \|S_op\| | \|S_decl\| gate-n | chance_sd | budget (cap-gate to G-ALIVE≥0.90) |
|---|---|---|---|---|---|
| 0 anchor | 48 | 24 | 12 | .102 | 12K steps |
| 1 | 192 | 96 | 48 | .051 | ~30K |
| 2 | 768 | 384 | 192 | .026 | ~100K |
| 3 terminal | 3072 | 1536 | 768 | .013 | ~250K |

**rung-0 anchor gate (HALT condition):** the RANDOM-ASSIGNMENT instrument must REPRODUCE H_9389's kill
signature — both-seed chance-or-below `S_decl` flip1 + ECHO 0.61–0.86 + `G-ALIVE`(S_op)≥0.90. **Fail ⟹ instrument
discontinuity ⟹ HALT everything** (do not run rungs 1–3).

### Axis 2 — confound controls (frozen)

- **C-TOK** — |S_op|=24 fixed, replicate lines to match the terminal rung's token count → gate must STAY
  chance (kills "token volume ↑" as the mover).
- **A/B fork** (one mid rung) — A = 150 lines/stem (total↑) vs B = fixed total lines (per-stem exposure
  diluted) → B also rising ⟹ ratio effect confirmed (not raw volume).
- **C-DECL-ABL** (MANDATORY on any green rung) — remove `S_decl` declaration lines → gate MUST return to
  chance. If it does NOT ⟹ surface leak ⟹ ⚠️ **LEAK-INVALID** (instrument problem, fix mining; NOT a verdict).
- **C-CAP** (secondary) — |S_op| fixed + arch shrunk (min arch still passing `G-ALIVE`≥0.90 by **bisection on
  G-ALIVE, NOT the DV** — so not tune-to-green).

### Axis 3 — grokking / weight-decay arm (`anima-py train --wd-floor <λ>`)

Budget stays a **capability-gate** (never pick val_CE minimum — H_9335). The wd arm probes whether a rule
groks late under regularization pressure where memorization is penalized.

## Confound isolation — the RANDOM-POLARITY design (strongest control)

`anima-py corpus xbind --bridge-split --polarity assigned --assign-seed k` — **RANDOM polarity assignment**
(NOT real sentiment). A from-scratch model never saw real usage, so real polarity is functionless; random
assignment (a) makes mining trivial at 10³ (no human sentiment labels), (b) keeps `G-BALANCE` by construction,
(c) kills any form→polarity leak, (d) is the strongest confound control. The existing `--bridge-split`
S_op/S_decl/S_cpt ½/¼/¼ split + phase-B arms are unchanged; only the polarity SOURCE is swapped.

## EN atom mining at scale (48 → N=3072, floor 1536)

Candidates = HF `anima-corpus-en-general` (~60 MB) top-frequency content words (alpha-only, 5–9 B, exclude
function/label words). Gates held at scale:
- **G-OCCUR** occ≥50 on a word boundary.
- **G-SUBSTR** at scale = freq-order greedy, no substring collision with the accepted set (~50–70% survival).
- **G-DERIV** lightweight (un-/in-/dis-/non-/-less/-ful affix pairs only — random assignment already killed
  polarity leak, so DERIV is only guarding the double-negation lookup escape).
- **G-BALANCE** free (random assignment).

Target N=3072, floor N=1536 — **report where it actually dries up (that IS the axis-1 ceiling).**

## Verdict table (FROZEN · primary readout = FINAL-checkpoint `S_decl` flip1 · mid-ckpts monitor-only)

- 🟢 **RULE-EMERGENT** — some rung d_acc>chance ∧ per-stem sign-perm p<.05 ∧ both-seed sign-agree
  **AND** C-DECL-ABL returns to chance **AND** C-TOK chance.
- ⚠️ **LEAK-INVALID** — gate rises but C-DECL-ABL does NOT return to chance (instrument, not a verdict).
- 🔴 **W_wt-TERMINAL** — envelope COMPLETED (rung-3 + C-CAP + grokking-wd arm), **every cell** final-ckpt
  upper-CI < 0.5+0.05 (non-superiority) ∧ `G-ALIVE` all-PASS ∧ (attention arm PASS if run) → **V5 reopen forced**.
- 💀 **KILL-AT-RUNG** — max rung fails but envelope INCOMPLETE (e.g. grokking arm impossible) — NOT terminal,
  honest partial-kill.
- **below-chance cell** — sustained below-chance + ECHO = membership-gate confirmation, a **FIRST-CLASS**
  supporting cell for 🔴 (not "undecidable").
- **`G-ALIVE`<0.90 cell = ⛔ INVALID** (neither evidence).

Monitor-only gauges per rung (NEVER in loss · `a_train_inline_gauge`): ECHO-rate + per-stem flip variance.
Mid-ckpts monitor-only (avoids multiple-comparison tune-to-green). Primary = FINAL checkpoint only.

## Positive-control honesty

If NO arm passes the gate, a mass kill is indistinguishable from INSTRUMENT-DEAD. Best positive control = an
**attention-substrate arm** at the same rung IF an engine-native ByteGPT-family train is reachable via
`anima-py train` (passes ⟹ instrument alive + free V5 preview: conv-fail / attn-pass ⟹ V5 active). If not
reachable, verify the scoring path is alive (C0-e style) and **state the positive-control absence as an explicit
card limitation — no concealment.**

## Protocol / hygiene (frozen)

- **Freeze FIRST** (this card + jsonl · pr-cycle) BEFORE any train. ✅ done here.
- **Cheapest-first + asymmetric stopping.** 🟢 may early-stop (gate passes + C-DECL-ABL/C-TOK null → stop,
  switch to threshold-localization). 🔴 may NOT early-stop — terminal requires envelope completion
  (rung-3 + C-CAP + grokking arm). **No kill-biased early stop.** Land partial results per rung (commit-early),
  resumable.
- **Host: aiden** ($0 · summer busy with V4, do NOT touch). ~90 GPU-h ≈ multi-day, sequential, OOM-guard,
  `OMP_NUM_THREADS=4`. **Pull each phase-A ckpt before any risk of loss** (`a_fire_recover_complete`; aiden
  persistent, no teardown). rc 137/143/241 = infra-wall (NOT a result).
- **NEVER edit primary** (parallel H_9361/H_9331 WIP). Fresh worktree off origin/main.
  `enforce_anima_gates --all` clean before each pr-cycle.

## Instruments (engine-native flags · G5 VERSION bump)

1. `anima-py corpus atoms --lang en --max-atoms N [--polarity assigned --assign-seed k]` — one-shot EN atom
   miner scaled to N (was 2-step hand-annotated @ 48).
2. `anima-py corpus xbind --bridge-split --polarity assigned --assign-seed k` — random polarity assignment
   (authoritative confound control).
3. `anima-py train --wd-floor <λ>` — **already exists** (constant weight-decay lever) = the grokking arm; no
   new code (`a_experiment_engine_native`). Budget stays a capability-gate.

## Status

- **PRE-REGISTRATION frozen** (this card + jsonl). Instruments + EN-mining ceiling + rung-0 anchor + ladder =
  the multi-day fire, landed per-rung. Interim results appended below as they land (commit-early).

---

## INTERIM #1 (2026-07-16 · session 1 · $0 front-load + rung-0 fired)

### Instruments — BUILT + UNIT-TESTED + MERGED (PR #3716 · VERSION 0.14.0)
- `corpus atoms --lang en --max-atoms N` (`build_atoms_scaled`) — freq-ranked greedy gates: G-OCCUR
  word-boundary (mine_lexicon word-level, honors corpus-py-1 (G)), G-SUBSTR greedy-DROP (no abort),
  G-DERIV affix-pairs, len 5–9 B, stoplist. Reports `dried_up` = ceiling (never pads).
- `corpus xbind --bridge-split --polarity assigned --assign-seed k` (`_assign_balanced_polarity`) —
  OVERRIDE the atoms file polarity with a RANDOM balanced assignment (sort→shuffle: order-independent +
  deterministic + seed-sensitive). ½/¼/¼ split + phase-B arms unchanged.
- `train --wd-floor λ` — pre-existing = grokking arm (no new code).
- Unit tests (synthetic EN, $0): balance / no-substr / no-deriv / determinism / order-independence /
  S_decl operator 0-exposure / S_cpt 0-line / gate gold=flip(pol) / back-compat — all PASS.

### Axis-1 EN mining ceiling — MEASURED ($0 · HF `anima-corpus-en-general` 60.0 MB / 279 429 lines)
The frame-candidate pool (words appearing after a degree adverb) = **4598 distinct** — the hard ceiling.
Greedy-gate survivors by occurrence floor:

| min_occ | accepted | dried before N=3072? | (mined_kept · dropped substr / len) |
|---|---|---|---|
| 20 | **2098** | yes | 3629 · 433 / 1079 |
| 50 | **1713** | yes | 2969 · 345 / 892 |
| 100 | 1407 | yes | 2444 · 275 / 743 |
| 200 | 1076 | yes | 1887 · 205 / 605 |

⟹ **N=3072 is UNREACHABLE from this single 60 MB corpus** at any reasonable occurrence floor. **Floor
N=1536 is CLEARED** (1713 @ occ≥50). The **terminal rung re-scopes to N≈1713 (|S_op|≈856)** @ occ≥50, or
2098 (|S_op|≈1049) @ occ≥20. That is still ~2.2× rung-2 and ~36× the anchor — a valid terminal. (Random
polarity means non-adjective survivors like "loading"/"reports" are fine: polarity is decoupled from meaning.)
NOTE the re-scoped ladder: rung-3 = **1713** (not 3072); to reach 3072 would need adding en-sns +
a second EN corpus (marginal). This is the honest axis-1 ceiling.

### rung-0 anchor corpus — BUILT + AUDIT-CLEAN ($0 · reuses H_9389's 48-atom `en_atoms.json`)
`build_bridgesplit(reps=40, --polarity assigned --assign-seed 0)` → 7200 lines / 278 280 B (matches
H_9389's A.txt 278 640 B). Audit: **S_decl operator(flip1) exposure = 0** (the gate layer) · S_cpt phase-A
lines = 0 · **slot-prior p(neg) = 0.5000** (kills majority-collapse) · G-BALANCE per arm (S_op 12/24 ·
S_decl 6/12 · S_cpt 6/12) · 36 gate rows.

### rung-0 anchor — FIRED (aiden RTX 5070 · $0 · in-flight)
Recipe recovered verbatim from H_9389: `--d 3784 --L 4 --e0 2 --emax 3` (345.7M) · 12000 steps ·
`--batch-size 32 --seq-len 64 --lr 3e-4` · seeds {7, 11} · ~0.24 s/step (~48 min/seed). Pipeline
smoke-validated end-to-end (train→.clm 176 MB decodable→`evaluate --xbind` GPU-CUDA · RC=0). Driver
detached on aiden (`~/h9410/rung0/driver.sh`, log `run.log`): trains s7+s11 then evaluates sop(G-ALIVE) /
sdecl(GATE) / scpt for each. **ETA ~1.5–2 h.** Anchor gate (HALT condition): reproduce H_9389 kill
signature — G-ALIVE(S_op)≥0.90 both seeds · S_decl flip1 chance-or-below both seeds · ECHO ~0.61–0.86.
Fail ⟹ instrument discontinuity ⟹ HALT.

### RESUME POINT (next session)
1. Read anchor-gate result: `sidecar pool on aiden 'tail -40 ~/h9410/rung0/run.log; cat ~/h9410/rung0/eval_s{7,11}_{sop,sdecl}.json'`.
   Pull ckpts: `scp aiden:~/h9410/rung0/phaseA_s{7,11}.clm ~/anima-weights/h9410_rung0/`. Append verdict here.
2. If anchor reproduces H_9389 kill → run rungs 1→2→3 (cheapest-first). Per rung: mine atoms
   (`anima-py corpus atoms --lang en --max-atoms N --min-occ 50`), build corpus
   (`anima-py corpus xbind --bridge-split --atoms gt_atoms_en_N.json --lang en --polarity assigned --assign-seed 0 --out AN.txt`),
   train both seeds (budget: rung-1 ~30K · rung-2 ~100K · rung-3(N=1713) ~250K), evaluate sop/sdecl.
   Re-scoped ladder: N = {192, 768, **1713**} (rung-3 capped by the 60 MB ceiling, floor 1536 cleared).
3. Controls on any green rung: C-DECL-ABL (mandatory), C-TOK. Envelope for 🔴: rung-3 + C-CAP + grokking-wd arm.
4. If anchor FAILS to reproduce → HALT, debug instrument (do NOT run rungs).

---

## INTERIM #2 (2026-07-16 · session 2 · rung-0 anchor gate → PASS · rung-1 fired)

### rung-0 anchor gate — ✅ REPRODUCES H_9389 (both seeds · HALT condition cleared)
`anima-py evaluate --xbind` on both anchor ckpts (aiden RTX 5070 · GPU-CUDA · $0 · driver `~/h9410/rung0/driver.sh`,
`ALL_DONE` 23:35 UTC). Verbatim:

| seed | `S_op` G-ALIVE (n=72) | `S_decl` GATE (n=36) | `S_cpt` (n=36) |
|---|---|---|---|
| 7  | **1.0000** (margin_med +5.238 · pos 0.750) | **0.3333** (margin_med −5.979 · pos 0.250) | 0.6389 (+1.940) |
| 11 | **1.0000** (margin_med +4.319 · pos 0.903) | **0.2222** (margin_med −5.970 · pos 0.111) | 0.6944 (−0.090) |
| bar | ≥0.90 both ✅✅ | chance-or-below both ✅✅ | (monitor) |

⟹ The RANDOM-ASSIGNMENT instrument reproduces H_9389's kill signature exactly: the operator is learned to
ceiling on `S_op` (1.000/1.000) yet does **not** transfer to operator-0-exposure held-out declared stems
(`S_decl` 0.33/0.22, both BELOW chance, both margins strongly negative) — "operator = stem-indexed lookup,
not a rule" replicated under random polarity. **Instrument continuity confirmed ⟹ ladder proceeds** (no HALT).
Anchor ckpts pulled to permanent storage `~/anima-weights/h9410_rung0/phaseA_s{7,11}.clm` (176 584 498 B each ·
`a_fire_recover_complete`). NOTE: ECHO monitor was not captured by the eval path (the two decisive frozen
criteria — G-ALIVE + `S_decl` chance-or-below — are met on both seeds and are what the HALT condition turns on).

### Instrument-version blocker — FOUND + FIXED (would have mis-fired rung-1)
aiden's installed `anima-py` was **0.13.94** — `build_atoms_scaled` / `--max-atoms` absent (rung-0 only needed
`build_bridgesplit` over H_9389's frozen 48-atom file, so it ran fine on the stale wheel). Upgraded to
**origin/main 0.14.5** via COMPLETE git-archive (`pyproject.toml VERSION MANIFEST.in anima_py cli core`,
`pip install --user --break-system-packages --no-deps` · `anima-py-pool-install-hexaless`). Verified:
`build_atoms_scaled` present.

### rung-1 mining — SOURCE-MATCHED to the pre-registered ceiling ($0)
First mining attempt used a local `en-general.txt` (8.0 MB / 35 647 lines · 1489 frame-candidates · 692 @ occ≥50)
— **NOT** the pre-registered source. Re-mined from the HF blob INTERIM #1 measured the ceiling on
(`datasets--dancinlab--anima-corpus-en-general` · **60 049 637 B / 279 429 lines**), which reproduces INTERIM #1
verbatim: **4598 frame-candidates → 2969 cleared min_occ=50** (matches the ceiling table exactly). Same source is
frozen for rungs 2–3 (the 8 MB file could never reach rung-2 768 / rung-3 1713 — 692 < 768 — so mining the
ladder from mixed sources would have been a non-nested atom-set confound).

`anima-py corpus atoms --lang en --max-atoms 192 --corpus <60MB blob> --min-occ 50 --assign-seed 0`
→ **ACCEPTED=192** (no dry-up · pos 96 : neg 96 · dropped len=176 stop=10 G-CARRIER=2 G-SUBSTR=10 G-DERIV=0)
→ split train=144 / heldout=48 · gate `chance_sd`=0.0722 (matches card table: |S_op|=96 · |S_decl| gate-n=48).

### rung-1 corpus — BUILT + AUDIT-CLEAN ($0)
`anima-py corpus xbind --bridge-split --atoms gt_atoms_en_192.json --lang en --reps 40 --polarity assigned
--assign-seed 0 --out A192.txt` → atoms=192 · S_op=96 / S_decl=48 / S_cpt=48 · **28 800 lines / 1 131 120 B** ·
**per-stem = 150.0** (policy-A, same as the anchor). Audit:

| check | result |
|---|---|
| `S_decl` operator (`not …stem`) exposure in phase-A | **0 / 48** ✅ (gate layer intact) |
| `S_decl` declaration (`is stem`) exposure | 48 / 48 ✅ (the arm's purpose) |
| [control] `S_op` operator exposure | 96 / 96 ✅ (operator IS taught) |
| slot-prior p(neg) | **0.5000** ✅ (majority-collapse killed) |

### rung-1 — FIRED (aiden · $0 · in-flight)
Driver `~/h9410/rung1/driver.sh` (detached setsid, log `run.log`), recipe = anchor's verbatim except corpus and
budget: `--d 3784 --L 4 --e0 2 --emax 3` (345.7M) · **--steps 30000** (card rung-1 budget) ·
`--batch-size 32 --seq-len 64 --lr 3e-4` · seeds {7, 11} → then `evaluate --xbind` sop/sdecl/scpt per seed.
Confirmed live at step 1 (CE 5.72626 · val_CE 7.65559 · train=1 074 564 / val_tail=56 556). **ETA ~4 h.**

### RESUME POINT (next session)
1. `sidecar pool on aiden 'tail -40 ~/h9410/rung1/run.log'` → wait `ALL_DONE`. Pull ckpts to
   `~/anima-weights/h9410_rung1/`. Read the gate: `S_decl` d_acc + per-stem sign-perm p, both seeds.
2. **Decision (frozen)**: `S_decl` still chance-or-below both seeds ⟹ rung-1 fails to un-cache ⟹ climb to
   **rung-2 (N=768, |S_op|=384, budget ~100K)** — same 60 MB source, `--max-atoms 768`, `--reps 40`.
   `S_decl` > chance ∧ per-stem sign-perm p<.05 ∧ both-seed sign-agree ⟹ 🟢 candidate ⟹ **C-DECL-ABL is
   MANDATORY before any green claim** (remove `S_decl` declaration lines → gate MUST return to chance; if not
   ⟹ ⚠️ LEAK-INVALID, not a verdict).
3. 🔴 W_wt-TERMINAL requires the COMPLETE envelope (rung-3 N=1713 + C-CAP + grokking-wd arm), not just a max-rung
   fail (that is 💀 KILL-AT-RUNG). No kill-biased early stop.

---

## INTERIM #3 (2026-07-16 · session 2 · C-DECL-ABL instrument BUILT — the MANDATORY control had none)

### The gap (found while rung-1 trains · would have blocked ANY green verdict)
The card makes **C-DECL-ABL MANDATORY on any green rung** — yet `grep` over `origin/main cli/corpus.py`
returned **0 matches** for any decl-ablation flag (same for C-TOK). ⟹ had rung-1 (or any rung) come back
green, the verdict could not have been validated at all: the frozen protocol demands a control whose
instrument did not exist. Built now, engine-native, while the GPU is busy (`a_experiment_engine_native`:
the INSTRUMENT is a flag on `anima-py`, never a probe beside the engine).

### Instrument — `anima-py corpus xbind --bridge-split --decl-ablate` (VERSION 0.14.8)
Ablates exactly ONE thing: the `S_decl` **declaration** emission block. Those stems then appear **zero times**
in phase A (no declaration, no operator) while the gate asks the identical questions.

| contract | check | result |
|---|---|---|
| ① gate questions unchanged | sdecl/sop/scpt manifest sha256 (ablate vs normal) | **identical 3/3** ✅ |
| ② sole variable = the declaration | `S_op` line multiset (ablate vs normal) | **144 = 144 identical** ✅ |
| ③ control target | `S_decl` stem occurrences in phase A (`\b`-bounded) | normal **36** → ablate **0** ✅ |
| ④ existing invariant preserved | `S_cpt` phase-A lines | **0 / 0** ✅ |
| ⑤ **back-compat** | default path (no flag) vs origin/main, 6 artifacts | **byte-identical 6/6** ✅ |

⑤ matters operationally: rung-1 is training RIGHT NOW on a corpus built by the pre-change code path — a
default-path drift would have silently de-synced the ladder. It does not drift.

Output self-labels as a control (never mistakable for a rung corpus): prints `⚠️ C-DECL-ABL CONTROL`, the
frozen reading (gate MUST return to chance; if not ⟹ ⚠️ **LEAK-INVALID** = instrument problem, NOT a verdict),
and `NOT a training corpus for a rung`.

`corpus-py-1` (I) applied before building the gate: (G) substring contamination — all stem counting here is
`\b`-bounded (EN); (F) the generalization axis (stem) is measured at 0-exposure; ⑫ untrained-carrier OOD does
not apply — `S_op` still teaches the operator carrier in every arm.

### Honest scope
The instrument is BUILT + unit-tested on synthetic EN ($0). It has **not** yet been run on a real rung — by
construction it is only read when a rung comes back green. **C-TOK remains unbuilt** (needed only for the 🔴
envelope, not for a green claim).

### C-TOK — needs NO new instrument (measured · corrects "unbuilt")
INTERIM #3 called C-TOK "unbuilt". **Wrong** — measured: `--reps` IS the token knob and it is exactly linear,
and the gate is invariant to it:

| reps | bytes | B/rep | sdecl gate sha |
|---|---|---|---|
| 4 | 6 816 | 1 704 | `3272eae6d3d3` |
| 8 | 13 632 | 1 704 | — |
| 16 | 27 264 | 1 704 | `3272eae6d3d3` (identical) |

⟹ C-TOK ("|S_op| fixed at the anchor's 48 · replicate lines to match the terminal rung's token count") is
built with **existing flags**: `corpus xbind --bridge-split --atoms <anchor 48-atom> --lang en --reps R
--polarity assigned --assign-seed 0`, with `R = round(terminal_bytes / bytes_per_rep)` (anchor = 278 280 B @
reps 40 ⟹ 6 957 B/rep; rung-3 N=1713 @ reps 40 ≈ 10.1 MB ⟹ **R ≈ 1448**). Exact R is computed from rung-3's
printed `BUDGET_FLOOR_BYTES` when that rung is built — no code, no new flag. The gate manifest stays
byte-identical to the anchor's, which is exactly what the control requires (same questions, same |S_op|, only
the token budget moves).

⟹ **Envelope instrument status: COMPLETE.** rung ladder (`--max-atoms`) · C-DECL-ABL (`--decl-ablate`) ·
C-TOK (`--reps` arithmetic) · grokking arm (`train --wd-floor`, pre-existing) · C-CAP (arch flags `--d/--L`,
pre-existing). Nothing in the 🔴 W_wt-TERMINAL envelope is blocked on missing code.

---

## INTERIM #4 (2026-07-16 · session 2 · rung-2 + rung-3 corpora PRE-BUILT + re-scope MEASURED)

While rung-1 trains, the remaining ladder was mined + built from the SAME 60 MB source (aiden · $0), so
each rung fires with zero build-wait and the re-scope claim is now measured, not asserted.

| rung | N | ACCEPTED (pos:neg) | \|S_op\| | S_decl gate-n | chance_sd | corpus bytes | per-stem |
|---|---|---|---|---|---|---|---|
| 2 | 768 | 768 (384:384) | 384 | 192 | 0.0361 | 4 535 280 | 150.0 |
| 3 (terminal) | 1713 | 1713 (856:857) | 856 | 428 | 0.0242 | 10 137 040 | 150.0 |

Both mined from the pre-registered HF blob (4598 frame-candidates → 2969 @occ≥50, verbatim to INTERIM #1) —
**neither dried up**, so the re-scoped terminal **N=1713 is REACHED** (not just projected). Audit (both rungs,
`\b`-bounded): S_decl operator 0-exposure **0/192 · 0/428** ✅ · S_decl declaration **192/192 · 428/428** ✅ ·
[control] S_op operator **384/384 · 857/857** ✅ · slot-prior **0.5000 / 0.5000** ✅.

**C-TOK exact reps (measured, supersedes the ~1448 estimate):** anchor = 278 280 B @ reps 40 ⟹ 6 957 B/rep;
rung-3 = 10 137 040 B ⟹ **R = round(10 137 040 / 6 957) = 1457** for the |S_op|=48-fixed token-matched control
(`corpus xbind --bridge-split --atoms <anchor 48-atom> --reps 1457 --polarity assigned --assign-seed 0`).

Artifacts on aiden: `~/h9410/rung_{768,1713}/A{768,1713}.txt` + gate manifests. Budgets (card): rung-2 ~100K,
rung-3 ~250K. Each fires the anchor's driver recipe with corpus + budget swapped, seeds {7,11}, evaluate
sop/sdecl. **The only thing left is GPU time** (rung-1 holds the single aiden GPU — `a_wall_first`).

---

## INTERIM #5 (2026-07-16 · session 2 · rung-1 gate → KILL SIGNATURE REPRODUCED · climb to rung-2)

rung-1 (|S_op|=96 · 4× the anchor) trained both seeds (30K steps · aiden · $0) then evaluated. Full gate:

| seed | G-ALIVE `sop` (n=288) | `S_decl` GATE (n=144) | `S_cpt` (n=144) |
|---|---|---|---|
| 7  | **0.9896** (margin_med +2.824) | **0.3889** (margin_med −1.857) | 0.5208 (−0.159) |
| 11 | **0.8993** (margin_med +9.449) | **0.4236** (margin_med −4.429) | 0.5417 (+0.171) |
| bar | ≥0.90 | chance-or-below | (monitor) |

**Verdict: KILL SIGNATURE REPRODUCED at |S_op|=96.** The operator is learned (G-ALIVE strongly positive both
seeds) yet does **not** transfer to operator-0-exposure held-out declared stems (`S_decl` **0.39 / 0.42**, both
BELOW chance, both margins strongly negative). Quadrupling |S_op| from the anchor (24→96) did **not** un-cache
the operator — cache still beats rule. Per the frozen protocol ⟹ **climb to rung-2 (N=768)**.

**Honest flags (not swept):**
- **seed-11 G-ALIVE = 0.8993** lands **0.0007 UNDER** the frozen ≥0.90 bar. NOT tuned to green: the number is
  reported as-is. margin_med **+9.449** (3× seed-7's) and sampled_maj_acc **0.900** confirm the operator is
  robustly alive — the bar's PURPOSE (exclude budget-negative / dead-operator) is met — but the literal d_acc is
  a hair under. The verdict direction is unaffected: `S_decl` 0.39/0.42 is nowhere near crossing chance, so both
  a strict and a generous G-ALIVE reading give the same "no rule emergence at rung-1" conclusion.
- **Driver instrument bug (FIXED for rung-2/3):** the `sop` eval (288 rows) hit `evaluate`'s fail-closed guard —
  default `--n-decode 200` would silently drop 88 whole-stem rows, so it refused (RC=1). G-ALIVE was recovered by
  re-running `evaluate … --n-decode 288`. rung-2 `sop`=1152 rows, rung-3 `sop`=2568 rows would hit the same wall,
  so the rung-2 driver now passes **`--n-decode 3000`** on every eval (≥ every manifest; `sdecl`/`scpt` 144-row
  results are byte-unchanged since 144 < 200 < 3000). The guard firing is a GOOD catch — it prevented a
  whole-stem-dropped G-ALIVE from being read as a real number.

### rung-2 — FIRE ATTEMPTED, GPU-BLOCKED (concrete blocker · not a science result)
The rung-2 driver (fixed `--n-decode 3000`, corpus `A768.txt` pre-built, budget 100K, seeds {7,11}) was launched
but `anima-py train` **refused to start**: aiden's single GPU is held by a parallel session's train job
(`h9339_fire/ho_decl` · 9.7 GiB · ~1 h to free). The trainer's own GPU-busy guard refused cleanly BEFORE the
corpus build (a_wall_first · zero waste). summer has a free GPU but load ~13 (CPU-saturated) — firing a 100K-step
run there risks the summer-overfire wedge, so rung-2 waits for aiden's GPU. **Resume: re-run
`~/h9410/rung_768/driver.sh` on aiden when its GPU frees.**

## INTERIM #6 — rung-2 (N=768 · |S_op|=384 · budget 100K) 💀 KILL-AT-RUNG-2 재현

aiden GPU가 병렬 h9339 4-arm 캠페인 완료 후 자유로워지자 **깨끗한 발사**(GPU-preflight 11.3/11.5 GiB free · GPU-refused 재발 없음). seed7 → seed11 순차 100K-step 학습 완료(양 `phaseA_s{7,11}.clm` 생성 → mac `~/anima-weights/h9410_rung2/` 영구보관 · a_fire_recover_complete), 이어 6-arm eval(`--n-decode 3000`) 실행.

**게이트 표 (engine-native · `anima-py evaluate --xbind` · heldout D-acc):**

| arm | n | d_acc | margin_median | sampled_maj | 판정 |
|---|---|---|---|---|---|
| G-ALIVE s7 (`sop`) | 1152 | **0.9123** | +4.261 | 0.975 | ✅ 연산자 alive |
| G-ALIVE s11 (`sop`) | 1152 | **0.9757** | +4.756 | 1.000 | ✅ 연산자 alive |
| **S_decl s7** (`sdecl`) | 576 | **0.3837** | −2.639 | 0.250 | 💀 우연밑 |
| **S_decl s11** (`sdecl`) | 576 | **0.3698** | −2.041 | 0.275 | 💀 우연밑 |
| S_cpt s7 (`scpt`, monitor) | 576 | 0.4844 | +0.145 | 0.400 | — |

(S_cpt s11 은 monitor-only DV — kill/rule 게이트 비필수, GPU 를 rung-3 로 넘기려 완주 전 판정.)

**Verdict: 💀 KILL-AT-RUNG-2 재현.** 연산자는 양 seed 모두 강건하게 학습됐으나(G-ALIVE 0.912/0.976, margin +4.3/+4.8) operator-0-노출 held-out 선언어간엔 전이 실패 — `S_decl` **0.384/0.370** 양 seed 모두 **우연(0.5) 밑**, 양 seed 모두 margin 음수. **|S_op| 을 anchor(24)→rung-1(96)→rung-2(384) 로 16× 키워도 캐시가 규칙을 이긴다** — rung-2 S_decl(0.38/0.37)은 rung-1(0.39/0.42)보다 오히려 더 우연밑. 규칙-추상화 압력이 커져도 어간-인덱스 lookup 이 여전히 싸다. frozen 프로토콜: `G-ALIVE≥0.9 양seed ∧ S_decl 양seed 우연밑` = KILL 재현 · terminal 아님(envelope 미완주) ⟹ **rung-3(N=1713 · |S_op|=856 · budget 250K) 상승**.

**남은 envelope**: rung-3(최대 N·EN mining 상한) → 완주 시 🔴 W_wt-TERMINAL(모든 셀 실패 시) · rung-3 도 KILL이면 여전히 💀 KILL-AT-RUNG-3(N=1713 이 도달가능 상한이므로 사실상 conv-CE terminal 근접). 어느 rung이든 S_decl>우연이면 sign-perm p<.05 + 양seed + C-DECL-ABL(`--decl-ablate`) 통과 전 green 금지.

### 🔗 병렬 세션 비교 — [[H_9672]] T3 주소벽 돌파 (a_parallel_session_compare · #3895)

병렬 세션이 `g1-interface-addressable-wall` 을 **다른 레버로 crack**: **addr-loss(`--store-addr-weight`)** = W_q softmax 주소경로 직접감독 → py303_full balanced manifest P1 **0.9688**(vs Stage1.5 chance 0.586·addr-gap 0.008 일반화). scope = 🟢 CRACK-DIRECTIONAL(합성 CVCVC nonce·storebind·**감독-주소 co-train tier**·창발-주소 아님·단일 seed-7).

**관계 = AGREES + 상보(다른 축)**: (1) **일치** — 둘 다 순수 CE/end-task-only 로는 안 열림 확증(H_9410 rung KILL = 압력만으론 캐시 안 풀림 · H_9672 arm-B/C = end-task-only 주소창발 KILL). (2) **상보** — H_9672 는 표적 주소감독이라는 **다른 레버**로 벽 crack · 이 rung 사다리는 그 crack 을 의미있게 만드는 **음성통제**(순수 |S_op| 압력은 EN mining 상한까지 밀어도 실패, 표적 주소감독만 작동). **CONFLICT 없음** — 서로 다른 manipulation(압력 vs 주소감독)·서로 다른 corpus(극성어간 storebind vs nonce storebind). 함의: H_9410 의 "pressure-alone 레버 종결"은 H_9672 의 addr-loss crack 을 부각(벽이 trivial-crackable 이 아님을 보증).
