# H_9808 — PRE-REGISTRATION GATES: four $0 referees that REFUSE a doomed spend before it happens

> **tier**: 🔵 INSTRUMENT LANDED · TOY e2e PASS · **NOT a verdict** (no 303M fire, not even DIRECTIONAL)
> **id**: H_9808 · **date**: 2026-07-20 · **cost**: $0 (closed-form, stdlib-only, no forward pass)
> **surfaces**: this card + ONE line in `HYPOTHESES/HYPOTHESES.jsonl`. Nothing else.

## What this is

Four **admissibility referees** absorbed from the `lab/v4` and `lab/v5` campaigns into production
`anima-py`. Each one is a gate that **would have refused a spend that actually happened**, and none
of them existed here: `trained-control-ceiling` had **0 hits** in `HYPOTHESES.jsonl` and **0 hits**
in `ARCHITECTURE.json` before this card.

They decide **admissibility, never a verdict**. A gate PASS is not a result, is not DIRECTIONAL, and
does not predict that the run it admits will be green. It says only: *the number this run produces
will be capable of carrying a bit.*

## Why an admissibility gate is not optional (the measured bill)

| gate | the spend it would have refused | the number that made it inadmissible |
|---|---|---|
| trained-control-ceiling | `lab/v4` **H_007**, ~7h GPU × 5 arms × 2 seeds | C-scaf **0.8073**, C-dup **1.0000** at d=384 vs an F1 bar of 0.15 ⇒ headroom 0 ⇒ Δ≈0 FORCED under both "mechanism alive" and "mechanism dead" |
| falsifier-headroom | `lab/v4` **H_001**, mech-3's clause (2) | ablation target already scored **0.9083–0.9167**; max attainable Δ = **0.0917 < 0.10 bar** ⇒ DEAD returned unconditionally, before the experiment existed |
| free-slot-score | `lab/v4` **H_004**'s codebook | K=6 codebook was **GF(2) rank-4** ⇒ teacher-forcing completed 2 parity slots ⇒ field-blind ceiling **0.667** reaching held-out, inflating EVERY arm equally |
| register-leak-probe | `lab/v4` **H_005**'s K3 | the G3-0d probe read **φ→hon = 1.0 held-out** ⇒ K3 falsified only the LEAKY VARIANT of its question (`lab/v5` H5_001) |

H_007's is the sharpest, because its anchor was not merely wrong but **inherited**: E[C-dup]=0.62 came
from another experiment's band (truth 1.00), and its own d=64 smoke **INVERTED** at d=384
(+0.073 → −0.010). That is why gate 1 refuses an inherited anchor as a first-class refusal, with no
override flag.

## Instrument (engine-native — flags on the installed CLI, never a script beside the engine)

`core/pregates.py` — CORE-owned SSOT, pure stdlib, deterministic by construction.

```
anima-py train  --trained-control-ceiling <bar> --control-anchor <a.json> --pregate-panel <id>
                                                       # ABORT BEFORE SPEND (runs at t=0)
anima-py evaluate --falsifier-headroom   <spec.json>   [--pregate-out f]
anima-py evaluate --free-slot-score      <codebook.json> [--pregate-bar b]
anima-py evaluate --register-leak-probe  <items.json>  [--leak-bar b] [--leak-eps e] [--leak-nmax n]
anima-py evaluate --pregate-selftest                   # all four, PASS and REFUSE inputs
```

Exit-code contract: **0 = PASS · 3 = REFUSE (abort before spend) · 2 = malformed spec**. A malformed
spec is never silently a PASS.

Gate 1 runs **before the DDP re-exec, before any CUDA allocation, before one corpus byte is read** —
H_007 discovered its inadmissibility *after* the spend, from the collected verdict. It is
**DEFAULT-OFF** (bar 0.0), and the toy e2e measures that the golden path is byte-identical.

## The concrete input that makes each gate ABORT (a gate that can only pass is theatre)

1. **trained-control-ceiling** — control **> 1 − 2×bar** (SATURATED · H_007's 0.8073 vs cap 0.70) ·
   control **< chance + margin** (DEAD-CONTROL · H_008 G-1.5a's 0.5104) · anchor scale ≠ this run's
   (SCALE-MISMATCH · the d=64 smoke) · anchor panel ≠ this run's · `measured != true` · no anchor at
   all · target scale left at the recipe default (the gate refuses to *guess* the scale it certifies).
2. **falsifier-headroom** — max Δ = ceiling − control **< bar** (VACUOUS) or **< 2×bar**
   (NO-HEADROOM) · **no negative control comes back reachable** (AUDIT-VOID — H_001's own F-001-4:
   an audit that condemns every comparison is condemning arithmetic, not detecting vacuity).
   Omitting the negative-control section is an ERROR, not a pass.
3. **free-slot-score** — any slot field-blind determinable, by prefix-determinism **or** GF(2)
   dependence · length-parity violation · a supplied **inherited** free-slot set that disagrees with
   the recomputed one · a bar that does not clear the recomputed ceiling with 2× headroom.
4. **register-leak-probe** — held-out probe accuracy **> surface-blind chance + eps**. Chance is
   re-derived as the held-out majority-class rate, not assumed 0.5
   (`chance-level-must-be-derived-per-metric`).

## Definitions worth pinning

- **field-blind ceiling** = mean over slots of `1.0 if determined else 1/|choices|`. On a K=6 binary
  codebook of GF(2) rank 4 this is `(2×1 + 4×0.5)/6 = 0.6667` — **H_004's measured 0.667 falls out
  of the definition**, which is why this is the definition used, not a fitted constant.
- **the leak probe is an EXACT COUNT, not a trained classifier.** For every byte n-gram (n ≤ nmax)
  in the fit split, the two-cell decision stump is fit by counting and scored on held-out. A trained
  probe would certify the probe; an exact count certifies the SURFACE.

## Toy e2e (run ONCE before landing · `instrument-never-run-hides-multiple-bugs`)

Every gate demonstrated **both PASSING and REFUSING**, through the installed `anima-py`, plus the
default-off parity control. Two real bugs were caught by the self-test **before the gate was ever
used**, both in gate 4:

1. the n-gram rule predicted the GLOBAL majority off-cell and skipped any gram whose in-cell
   majority equalled it — which **silently skipped the leaking gram whenever the leak was carried by
   the majority class**. The gate would have passed a leaking register. Fixed to a proper two-cell stump.
2. the "deleaked" fixture was itself leaky (`alpha 0..7` with target = `i%2` — the DIGIT carried the
   target). The **fixture was wrong, not the gate**; the gate had correctly refused it.

```
$ anima-py evaluate --pregate-selftest
  PASS g1 pass: control 0.62 under bar 0.15
  PASS g1 REFUSE: H_007 C-scaf 0.8073 saturates cap 0.70
  PASS g1 REFUSE: H_008 C-dup 0.5104 is a dead control
  PASS g1 REFUSE: d=64 smoke anchor for a d=384 run
  PASS g1 REFUSE: anchor from another panel
  PASS g1 REFUSE: measured != true
  PASS g2 REFUSE: H_001 mech-3 clause (2) is vacuous
  PASS g2 arithmetic: max Δ over M_s4302 = 0.0917
  PASS g2 negative control 0.6167 IS reachable (F-001-4)
  PASS g2 pass: bar 0.10 vs control 0.6167
  PASS g3 REFUSE: rank-4 K=6 codebook
  PASS g3 gf2_rank == 4
  PASS g3 field-blind ceiling == 0.667 (H_004's number falls out)
  PASS g3 pass: full-rank codebook, ceiling == chance == 0.5
  PASS g3 REFUSE: inherited free-slot set that disagrees
  PASS g4 REFUSE: surface carries the answer token
  PASS g4 pass: deleaked register sits at chance
SELFTEST pregates: OK                                                    exit=0
```

**GATE 1 — REFUSE on H_007's real d=384 numbers** (`anima-py train … --control-anchor …`):

```
  bar b        = 0.1500   ⇒ control must sit in (0.5500, 0.7000]
  this run     = {"L": 4, "arch": "clm", "batch_size": 8, "d": 384, "seq_len": 0, "steps": 4000}
  anchor arm   = C-scaf   src: lab/v4 H_007 g2_full.out — the REAL measured C-scaf/C-dup at d=384
    seed s0     control=0.8073  cap=0.7000  floor=0.5500  headroom=0.1927 (need 0.3000)
    seed s1     control=0.9531  cap=0.7000  floor=0.5500  headroom=0.0469 (need 0.3000)
  ⛔ GATE REFUSE — ABORT BEFORE SPEND. Reasons:
    · SATURATED: seed s0 control=0.8073 > cap 0.7000 (= 1.0000 − 2.0000×bar 0.1500) — the band above
      the control is narrower than the bar; Δ≈0 is FORCED whether the mechanism works or not (H_007)
    · SATURATED: seed s1 control=0.9531 > cap 0.7000 …
VERDICT: REFUSE
  NOT STARTING THIS RUN.                                                 exit=3
```

Other gate-1 refusals, each exit=3: `SCALE-MISMATCH: anchor d=64 vs this run d=384` (the smoke) ·
`DEAD-CONTROL: seed s0 control=0.5104 < floor 0.5500` (H_008) · no `--control-anchor` ·
`--d, --L, --steps left at the recipe default`.

**GATE 1 — PASS proceeds to real training** (toy d=64 L=2 steps=2, admissible anchor 0.62/0.66):

```
    seed s0     control=0.6200  cap=0.7000  floor=0.5500  headroom=0.3800 (need 0.3000)
  🟢 GATE PASS — admissible on this axis. …
  step     1  CE=5.68697  E=3  val_CE=5.52464
  step     2  CE=5.61500  E=3  val_CE=5.36846
  .clm WRITTEN 117502 bytes · clm_decodable=True                         exit=0
```

**DEFAULT-OFF PARITY** — the same toy run with the gate flags absent:
`sha256 9b86baef…c771854` in BOTH arms ⇒ **BYTE-IDENTICAL (1.000000)**.

**GATE 2 — REFUSE on H_001's verbatim record** / PASS on its own negative control:

```
  M_s4302  score=0.9083  max attainable Δ = 1.0000 − 0.9083 = 0.0917   reachable=False
  M_s7     score=0.9167  max attainable Δ = 1.0000 − 0.9167 = 0.0833   reachable=False
  NEGATIVE CONTROLS (H_001 F-001-4 — at least one MUST be reachable):
  C1_s4302 score=0.6167  max attainable Δ = 0.3833                      reachable=True
  ⛔ VACUOUS: … strictly BELOW the pre-registered bar 0.1000 …           exit=3
  (same gate, controls = C1_s4302 only)  🟢 GATE PASS                    exit=0
```

**GATE 3 — REFUSE on a K=6 GF(2) rank-4 codebook** / PASS on a full-rank one:

```
  codewords=16 slots=6 binary=True GF(2) rank=4
  prefix-determined slots: ['p0', 'p1']   GF(2)-dependent slots: ['p0', 'p1']
  FREE slots (recomputed, never inherited): [0, 1, 2, 3]
  FIELD-BLIND ceiling = 0.6667   (derived chance = 0.5000)
  ⛔ REDUNDANT-CODEBOOK … (H_004: ceiling 0.667 reached held-out)        exit=3
  (full-rank K=4)  FIELD-BLIND ceiling = 0.5000 = chance  🟢 GATE PASS   exit=0
```

**GATE 4 — REFUSE on a leaky register (the H_005 signature) / PASS on a deleaked one:**

```
  held-out probe accuracy  = 1.0000   ⚠ CERTAIN LEAK
  surface-blind chance     = 0.5000   (held-out majority-class rate, derived per metric)
  ⛔ REGISTER-LEAKS … no 'learned' claim on this panel is about learning  exit=3
  (deleaked)  held-out probe accuracy = 0.5000 = chance  🟢 GATE PASS     exit=0
```

Malformed spec ⇒ `exit=2` (never silently a PASS).

## Honest limits

1. **This card lands an INSTRUMENT, not a finding.** Nothing here is a verdict about anima's
   substrate, and no gate output may be cemented as one. The gates are referees; they produce
   admissibility booleans, not measurements of the engine.
2. **The gates are only as good as the numbers fed to them.** Gate 1 reads a control anchor from a
   JSON file — it verifies the anchor's *provenance fields* (measured/panel/scale/seeds/source), and
   it CANNOT verify that the person who wrote the file actually ran that control. It closes the
   inherited-anchor hole, not the fabricated-anchor hole.
3. **The scale comparison is exact-match on the keys the anchor declares.** An anchor that declares
   only `{d}` is certified only on `d`; the gate reports what it checked and never claims more. An
   anchor declaring a key this run does not expose is refused as SCALE-UNVERIFIABLE rather than
   waved through.
4. **The leak probe is bounded at n ≤ nmax byte n-grams.** Longer-range and cross-sentence leaks are
   unaudited **by construction** — carried verbatim from `lab/v5` H5_001's own honest limit 3. A PASS
   means "no short-n-gram leak was found", never "the register is clean".
5. **The field-blind ceiling formula reproduces H_004's 0.667, but H_004's codebook was not re-read.**
   The 0.667 is cited from the `lab/v4` campaign record; the agreement is a consistency check on the
   definition, not an independent re-derivation of that panel.
6. **Toy scale only.** The e2e ran at d=64 L=2 steps=2 on CPU. Gate 1's *arithmetic* is
   scale-invariant (it reads numbers), but its integration with a 303M pool run is UNMEASURED
   (`a_toy_scale_recheck`).

## Cross-Links

- Sources (read-only): `lab/v4/HYPOTHESES/cards/H_007…` · `H_001…` · `H_008…` ·
  `lab/v4/state/campaign_result_2026-07-17/CAMPAIGN_RESULT.md` §3 ·
  `lab/v5/HYPOTHESES/cards/H5_001…` · `lab/v5/CLAUDE.md` (its five standing gates G1–G5).
- Memory rows this hardens: `power-before-negative-verdict` · `negative-claims-need-tost-not-ns` ·
  `control-must-match-mediating-covariate` · `chance-level-must-be-derived-per-metric` ·
  `burned-gate-no-refreeze-sequential-gating` · `check-ledger-before-lever-fire`.
- Governance: `a_experiment_engine_native` (a manipulation is a flag on `anima-py`) ·
  `a_break_the_wall` (no tune-to-green) · `a_cli_single_entry`.

## Verdict

**No verdict — this card lands an instrument.** The only measured facts are: the four gates run,
each REFUSES on the concrete input it was built to refuse (with the real `lab/v4`/`lab/v5` numbers)
and PASSES on an admissible one, exit codes honor the 0/2/3 contract, the trainer aborts at t=0
before any allocation, and the default-off path is byte-identical (sha256 match). Whether these
gates change any future verdict is unmeasured and is not claimed.
