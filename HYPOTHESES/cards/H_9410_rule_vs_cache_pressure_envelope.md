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
