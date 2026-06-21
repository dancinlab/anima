# H_1548 — SEROTONIN × CLS: consolidation COMMIT-GATE (slow-store integrity under contradiction)

**tier:** 🟠 AMBER — DIRECTIONAL (R1 numpy mirror; `wired: DIRECTIONAL-mirror → §Ht5Gate engine R2`)
**verdict source:** `state/verdicts/1548_cls_5ht_gate/H_1548_R1.json` (frozen `H_1548_FREEZE.txt`)

## Frame (a_no_llm_frame_trap — biological structure first)

A **CAPABILITY reframe** of 5-HT inside the H_1532 two-store CLS module — **NOT a bar-move**
of the H_1545 timing framing.

The **fusion law** of this batch (a_break_the_wall): a neurotransmitter that **ADDS a
capability** two-store CLS lacks earns 🟢 (ACh mode-switch H_1541, DA value-rank H_1543,
NE state-flush H_1544); one that only **RE-TUNES an existing op** stays 🟠 (H_1545
5-HT-TIMING: "when to sweep" re-schedules the consolidation period, a fixed period
captured 66.6%). To make 5-HT GREEN we must NOT re-run timing — we must find the
**CAPABILITY** 5-HT adds.

Biological 5-HT (**Cools 2008** — serotonin & behavioral inhibition / aversive prediction;
**Dayan-Huys 2009** — serotonin, inhibition & negative valence) = **withholding an action
pending confirmation** + aversive/error valence. Mapped onto CLS: a **COMMIT-GATE** that
withholds UNCONFIRMED / CONTRADICTED fast-store bindings from permanent commitment to the
slow store, so transient or later-contradicted entries do not permanently corrupt the
consolidated store.

- **DISTINCT vs DA (H_1543):** DA ranks WHICH valid memories replay first (priority ORDER);
  5-HT decides WHETHER to commit AT ALL pending confirmation (error/valence GATE, not rank).
- **DISTINCT vs H_1545 timing 🟠:** H_1545 controls the sweep **PERIOD** (when it fires) —
  every binding present at the boundary is still committed. H_1548 controls the sweep
  **CONTENT** (which bindings the sweep may commit). A fixed period cannot withhold a
  contradicted binding however it is scheduled. (Capability-reframe, NOT a moved bar.)

## Design (frozen-first, c9, NO tune-to-green)

CONTRADICTION stream: CONFIRMED keys (A→V reconfirmed K=2×), CONTRADICTED keys (A→B stale
then A→B' correction, each ×2; truth = the correction B'), NOISE keys (A→X once, never
reconfirmed, no truth). Reuses **H_1532 MemStore / key_vec / FNV-1a / suppress_retrieval
encode-mode / LRU byte-exact**. A confirmation ledger (per-key value counts + last-seen) is
the substrate signal 5-HT reads.

ARMS: HT5-GATE (commit only reconfirmed count≥K AND last-seen) · COMMIT-ALL (H_1532 default,
commit winner/last cell) · COMMIT-RECENT (most-recent value, no confirmation) · ABL
(threshold→0 == commit-all) · SHUFFLE (confirmation ledger permuted across keys).
MARGIN 0.10, seeds [11,22,33], CONFIRM_K 2, $0 CPU, p7.

FROZEN bars — 🟢 iff A∧B∧C∧D∧E:
- **A PRESENCE** — gate_correct − commit_all_correct ≥ +0.10 on ≥2/3 AND mean
- **B DISTINCT** — commit_all corrupted by stale AND commit_recent fooled by recency (gate beats BOTH)
- **C ABL** — abl reverts to commit-all (|abl−all|<0.10) AND gate−abl ≥ 0.10
- **D SHUFFLE** — permuted confirmation collapses (gate−shuffle ≥ 0.10)
- **E NO-FAB** — gate abstains on never-reconfirmed noise (gate_no_fab ≥ 0.90)

## Result (3 seeds [11,22,33], mean)

| arm | slow-store correctness | no-fab (noise abstain) |
|---|---|---|
| HT5-GATE (commit only reconfirmed) | 0.7500 | **1.0000** |
| COMMIT-ALL (H_1532 default sweep) | 0.7500 | 0.0000 |
| COMMIT-RECENT (recency rule) | 0.7500 | 0.0000 |
| ABL (threshold→0 == commit-all) | 0.7500 | — |
| SHUFFLE (permuted confirmation) | 0.0312 | — |

- **A PRESENCE** ❌ — gate − commit_all = **+0.0000** mean (0/3 seeds ≥0.10). The
  contradiction is **recency-recoverable**: the correction B' is the LAST write for the
  key in 11/16 contradicted keys, so commit-all (which commits the last/winning cell)
  already lands the correct binding → the gate adds NO correctness over commit-all.
- **B DISTINCT** ❌ — commit-all is NOT corrupted on the correctness axis (ties gate).
- **C ABL** ❌ — abl == commit-all == gate on correctness (gate−abl = 0.0).
- **D SHUFFLE collapse** ✅ — gate 0.7500 − shuffle 0.0312 = **+0.7188** ≥0.10 (permuting
  the confirmation ledger destroys the commit decision → the gate DOES read the true
  per-key confirmation signal, not noise).
- **E NO-FAB** ✅ — gate_no_fab **1.0000** ≥0.90 vs commit-all/recent **0.0000**: the gate
  withholds EVERY never-reconfirmed noise binding from slow commit; both controls commit
  ALL of them. This IS the biological 5-HT inhibition — but it lives on the NOISE-rejection
  axis, NOT the pre-registered correctness-presence axis.

→ **¬A ∧ D ∧ E = 🟠 AMBER (frozen mapping: not-A → WALL_HOLDS on the correctness claim).**

## Reading (c9 — honest, NO bar moved)

The pre-registered claim — that the 5-HT commit-gate adds **slow-store CORRECTNESS** under
contradiction over commit-all — is **FALSIFIED**: on the frozen stream the contradiction is
**recency-recoverable** (the correction is the last write), so commit-all already lands the
right binding and the gate ties it (gate−all = +0.0000, 0/3). The commit-gate does NOT add
correctness capability where recency suffices. This is the honest type-(d) ceiling on the
correctness axis (NOT a moved bar — the frozen bar stays; we report the tie).

The one capability the gate provably DOES add, that BOTH controls fully lack, is on the
**NO-FAB / noise-rejection** axis: gate withholds 100% of never-reconfirmed singleton noise
from permanent slow commit (no_fab 1.0 vs 0.0), and SHUFFLE proves it reads true per-key
confirmation (collapse +0.7188). This is the genuine 5-HT *withholding-pending-confirmation*
mechanism — but it surfaces as **refusing to fabricate** unconfirmed bindings, not as
repairing contradicted ones, because recency already repairs contradictions in this regime.

**Verdict: 🟠 AMBER.** 5-HT's commit-gate is a REAL, ablation-decisive (SHUFFLE +0.72)
mechanism on the noise-rejection axis, but it does **not** earn 🟢 on the frozen
correctness-presence bar — commit-recent already captures contradiction recovery. Reported
honestly per c9; **no green manufactured, no bar moved.** The commit-gate joins H_1545 as a
5-HT lever that is PRESENT but does not carry the pre-registered majority capability inside
two-store CLS. (Open: a regime where the stale binding is NOT recency-recoverable — e.g.
correction arrives EARLY then noise re-presses the stale cell, or fast-store eviction drops
the correction — would re-separate the correctness axis; that is a NEW frozen stream, a
follow-on, not a post-hoc edit of this bar.)

**wired:** DIRECTIONAL-mirror → §Ht5Gate engine R2 (ING). numpy mirror (host has no torch,
a_engine_native_learning hard-gate-1 → DIRECTIONAL); engine-native R2 re-score on
`core/engine_cli.hexa` §Ht5Gate deferred.

## Artifacts
- `state/1548_cls_5ht_gate/h1548_cls_5ht_gate.py` (probe, reuses H_1532 harness byte-exact)
- `state/1548_cls_5ht_gate/H_1548_FREEZE.txt` (pre-registered falsifier)
- `state/1548_cls_5ht_gate/H_1548_R1.json` · `state/verdicts/1548_cls_5ht_gate/H_1548_R1.json`
