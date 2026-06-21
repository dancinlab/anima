# H_1549 — SEROTONIN × CLS: NOISE-REJECTION gate (slow-store PRECISION under unconfirmed noise)

**tier:** 🟢 GREEN — DIRECTIONAL (R1 numpy mirror; `wired: DIRECTIONAL-mirror → §Ht5Gate engine R2`)
**verdict source:** `state/verdicts/1549_5ht_noisereject/H_1549_R1.json` (frozen `H_1549_FREEZE.txt`)

## Frame (a_break_the_wall — RIGHT capability / RIGHT measurement, NOT tune-to-green)

A **CAPABILITY RE-CENTER** of 5-HT inside the H_1532 two-store CLS module. **NOT a bar-move
of H_1548.**

H_1548 (5-HT commit-GATE) landed 🟠. Its FROZEN bar was slow-store **CORRECTNESS** under
CONTRADICTION, and that bar was **FALSIFIED honestly**: the contradiction is
**recency-recoverable** (the correction B' is the LAST write), so commit-all already lands the
right value and the gate ties it (gate−all = +0.0000, 0/3). CORRECTNESS was the **wrong target**.

BUT inside H_1548 a **different** capability genuinely PASSED, ablation-decisive: the gate
withholds 100% of never-reconfirmed singleton NOISE from permanent slow commit (no_fab 1.0 vs
control 0.0; SHUFFLE collapse +0.7188). That **NOISE-REJECTION** is a REAL capability the bare
two-store CLS lacks. H_1549 re-centers the **pre-registered** claim onto that genuine capability,
measured frozen-first with its **OWN NEW bars** (`H_1549_FREEZE.txt`, written before the run).
This is a_break_the_wall (right capability / right measurement), **NOT moving H_1548's bars**.

Biological 5-HT (**Dayan-Huys 2009** — serotonin, inhibition & negative valence; **Cools 2008**
— serotonin & behavioral inhibition / aversive prediction) = withholding a commitment **pending
confirmation**. Mapped onto CLS: the consolidation sweep must NOT make a permanent slow
commitment for a binding seen ONCE and never reconfirmed (a transient / noise binding).

## The NEW measurement (distinct from H_1548's correctness axis)

**slow-store PRECISION** = of the bindings the sweep COMMITTED to the permanent slow store, what
fraction are **REAL** (CONFIRMED/CONTRADICTED — has a ground truth) vs **NOISE** (singleton, no
truth). Committing noise PERMANENTLY pollutes the slow store; recall-recovery cannot undo it.

- **DISTINCT vs H_1548 CORRECTNESS:** H_1548 asked *"is the committed VALUE right"* (recency
  fixes it). H_1549 asks *"should this binding be committed AT ALL"* — a singleton noise key
  has **no right value**; the only correct action is **not to commit it**. **Recency CANNOT
  decide this** (a noise key has a `last_val` too); **confirmation-COUNT can**. THAT is the 5-HT
  withholding-pending-confirmation mechanism, and it is exactly what commit-recent lacks.

## Design (frozen-first, c9, NO tune-to-green)

Stream (VERBATIM H_1548 generator, REUSES H_1532 MemStore / key_vec / FNV-1a /
suppress_retrieval encode-mode / LRU byte-exact): CONFIRMED keys (A→V reconfirmed K=2×, REAL,
truth=V) · CONTRADICTED keys (A→B ×2 then A→B' ×2, REAL, truth=B') · NOISE keys (A→X once,
never reconfirmed, **NO truth**). N_CONFIRMED=16 · N_CONTRADICTED=16 · N_NOISE=16 · CONFIRM_K=2 ·
LR*=0.20 · TH*=0.30 · ABSTAIN=0.45 · MARGIN=0.10 · seeds [11,22,33] · $0 CPU · p7.

ARMS: HT5-GATE (commit only reconfirmed count≥K last value → noise WITHHELD) · COMMIT-ALL
(H_1532 default sweep → commits noise too) · COMMIT-RECENT (recency rule, no confirmation →
commits noise too) · ABL (threshold→0 == commit-all) · SHUFFLE (confirmation ledger permuted
across keys).

FROZEN bars — 🟢 iff A∧B∧C∧D∧E:
- **A PRESENCE** — gate_precision − commit_all_precision ≥ +0.10 on ≥2/3 AND mean
- **B DISTINCT** — BOTH commit_all AND commit_recent polluted by noise (each < gate−0.10) →
  gate beats BOTH (recency does **NOT** suffice — the load-bearing honesty check)
- **C ABL** — abl reverts to commit-all (|abl−all|<0.10) AND gate−abl ≥ 0.10
- **D SHUFFLE** — permuted confirmation collapses (gate−shuffle ≥ 0.10)
- **E NO-FAB** — gate abstains on never-reconfirmed noise at recall (gate_no_fab ≥ 0.90)

## Result (3 seeds [11,22,33], mean)

| arm | slow-store precision | no-fab (noise abstain) |
|---|---|---|
| HT5-GATE (commit only reconfirmed) | **1.0000** | **1.0000** |
| COMMIT-ALL (H_1532 default sweep) | 0.6667 | 0.0000 |
| COMMIT-RECENT (recency rule) | 0.6667 | 0.0000 |
| ABL (threshold→0 == commit-all) | 0.6667 | — |
| SHUFFLE (permuted confirmation) | 0.6459 | — |

- **A PRESENCE** ✅ — gate 1.0000 − commit_all 0.6667 = **+0.3333** (all 3/3 seeds, mean). The
  gate commits only the 32 REAL keys (precision 1.0); commit-all commits all 48 keys including
  16 noise → 32/48 = 0.6667.
- **B DISTINCT** ✅ — **BOTH** commit_all (0.6667) AND commit_recent (0.6667) are polluted by
  noise, each < gate−0.10. **Recency does NOT suffice this time** — a noise key has a `last_val`,
  so commit-recent commits it; only confirmation-COUNT withholds it. This is the load-bearing
  contrast vs H_1548 (where recency DID suffice on the correctness axis).
- **C ABL** ✅ — abl 0.6667 == commit_all 0.6667 (gate→0 reverts), gate−abl = **+0.3333**.
- **D SHUFFLE** ✅ — gate 1.0000 − shuffle 0.6459 = **+0.3541** (permuting the confirmation
  ledger scrambles which keys pass count≥K → it commits some noise and drops some real → proves
  the gate reads TRUE per-key confirmation, not a gate-rate side effect).
- **E NO-FAB** ✅ — gate_no_fab **1.0000** ≥0.90 (cross-check: the gate never fabricates a noise
  binding at recall either) vs controls 0.0000.

→ **A ∧ B ∧ C ∧ D ∧ E = 🟢 GREEN.**

## Reading (c9 — honest, NO bar moved, NO tune-to-green)

The RE-CENTERED claim — that the 5-HT noise-rejection gate adds **slow-store PRECISION** (keeps
never-reconfirmed singleton noise OUT of the permanent slow store) over BOTH commit-all and
commit-recent — **PASSES on all 5 frozen bars**. This is the capability that genuinely existed
inside H_1548 (the no-fab/shuffle pair), now measured on its own correct axis with bars frozen
before the run. The honesty pivot is bar **B**: unlike H_1548's correctness axis (where recency
sufficed and the claim was rightly FALSIFIED), on the **commit-AT-ALL / precision** axis recency
**cannot** help — a noise key has a `last_val`, so commit-recent commits it just like commit-all.
Only confirmation-COUNT (the 5-HT signal) withholds it. SHUFFLE (+0.35) confirms the lift reads
true per-key confirmation, not the commit RATE.

**Verdict: 🟢 GREEN (DIRECTIONAL).** 5-HT adds a genuine NOISE-REJECTION capability — withholding
unconfirmed transient bindings from permanent consolidation — that two-store CLS lacks and that
neither a blind sweep nor a recency rule provides. This joins the fusion-law GREEN siblings (ACh
mode-switch H_1541, DA value-rank H_1543, NE state-flush H_1544) as a neurotransmitter that ADDS
a capability, NOT one that merely re-tunes (H_1545 timing 🟠, H_1548 correctness 🟠). **No green
manufactured, no bar moved** — the bars were frozen in `H_1549_FREEZE.txt` before the run; had
commit-recent rejected noise (bar B fail) the verdict would have been honest 🟠.

**wired:** DIRECTIONAL-mirror → §Ht5Gate engine R2 (ING). numpy mirror (host has no torch,
a_engine_native_learning hard-gate-1 → DIRECTIONAL); engine-native R2 re-score on
`core/engine_cli.hexa` §Ht5Gate deferred (shares the §Ht5Gate lane targeted by H_1548 R2).

## Artifacts
- `state/1549_5ht_noisereject/h1549_5ht_noisereject.py` (probe, reuses H_1532/H_1548 harness byte-exact)
- `state/1549_5ht_noisereject/H_1549_FREEZE.txt` (pre-registered falsifier)
- `state/1549_5ht_noisereject/H_1549_R1.json` · `state/verdicts/1549_5ht_noisereject/H_1549_R1.json`
