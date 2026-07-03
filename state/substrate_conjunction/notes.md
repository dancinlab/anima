# substrate_conjunction — gap #1 conjunction readout + gap #3 A⇄G conflict monitor (engine-native)

> Slug produced 2026-07-03. **op skeleton + engine-native fixtures.** Frozen/HYPOTHESES/cards/commit/PR/
> CHANGELOG/ARCHITECTURE **untouched** (op NOT yet lifted into core — that is the rung-3/4 follow-on).
> hexa v0.574.1 on mini (cheap CPU fixtures, no decode/GPU). Source-of-truth read = `core/engine_cli.hexa`.

---

## (a) conjunction readout op — DESIGN

**Gap (reference-match, `core/engine_cli.hexa` §ADAPTATION):** MITOSIS recall is **winner-take-all** —
`_vnearest_idx` (:528) returns a single argmax cell. That answers *"which ONE regime is this?"* (OR/argmax).
It **cannot** answer *"are TWO learned regimes present at once?"* (AND-over-regimes / conjunction). No op
reads conjunction — the missing capability. This is binding-**as-detection** (sensory fusion, e.g. "SNS ∧
Korean" co-present), **not** G1 generation → it sits OUTSIDE the DPI recombination wall (same class as
`self_drift_exp` H_9038, which opened a non-recombination capability and went GREEN-WIRED).

**Mechanism — fuzzy-AND = min-activation = the SECOND-nearest distance.** The engine's own scan already
surfaces `[d1,d2]` (nearest + second-nearest L2, `vadapt_field_two_recon_err` :~660, pub). WTA reads only
`d1`. Conjunction keys on **`d2`** — the FARTHER = WEAKER of the two co-active regimes. Gating on `d2` =
min-over-the-two-activations = Zadeh fuzzy-AND: a conjunction fires only when *even the weaker* regime is
still within `thr`. **Zero new geometry** — pure read over the engine's existing top-2 affinity.

Ops (skeleton `conjunction_readout.hexa`, ready to lift into core §ADAPTATION):
- `vadapt_field_conjunction(af,x,thr) -> float` — binary: 1.0 iff `n_cells>=2 && d2<thr`, else 0.0.
- `vadapt_field_conjunction_score(af,x,thr) -> float` — graded fuzzy-AND membership `clip01(1 - d2/thr)`.
- `_conj_wta_collapse(af,x,thr)` — ABLATION twin that reads `d1` (=WTA); discrimination vanishes (INERT).

**The load-bearing distinction:** two inputs can share the SAME nearest cell (identical `d1`, so argmax/WTA
sees them as identical) yet differ in `d2` — one is single-regime, one is a conjunction. Only the `d2` read
separates them. That is exactly what the fixture proves.

## (b) A⇄G conflict monitor op + fixture — ⚠️ ALREADY EXISTS + engine-native re-verify

**Reference-match finding:** the `ag_conflict` monitor the substrate-gaps analysis proposed
(`|a_drive - g_drive|`) **already exists in the live engine as `conflict_scalar`** (`engine_cli.hexa`:8450),
and is strictly better than `|a-b|`:
- both-strong-**opposite-sign** gate: `0` unless signs oppose, else `clip01(|a|·|b|)`. A single-engine state
  (one drive ≈0) → 0 (no competition); `|a-b|` would spuriously fire there.
- ships with its own parent-control `conflict_net_tension = |a+g|` (the Ψ/emit-drive analog) — reads the SAME
  value for high-conflict `(+x,−x)` and low-drive `(+e,−e)`; `conflict_scalar` separates them (the exact
  dissociation the analysis wanted a "shuffle control" to provide — built in).
- downstream `conflict_recruited_depth` (conflict → deeper A⇄G deliberation budget).

**Provenance:** its monitor leg is already engine-native GREEN (**H_9094**, 4/4: conflict-matched budget
PRESERVES Ψ=½, treatment 0.125 < shuffle 0.25 < ablation 0.375) AND wired per-tick into the real loop
(**H_9095** rung-3, `cli/anima.hexa` L1937–1961). So gap #3's monitor leg is **already at rung-3** — not
OPEN. `ag_conflict_monitor.hexa` documents the mapping + gives the analysis's `self_drift`-pattern NAME as a
thin pass-through alias to the single existing op (no fork — `a_core_engine_map`).

**Independent engine-native re-verify — `ag_conflict_fixture.hexa` = 8 pass / 0 fail:**
```
c_hi=0.81  c_agree=0.0  c_single=0.0  c_lo=0.0025   (conflict rises only for opposite+strong)
net_hi=0.0 net_lo=0.0                                (net-tension BLIND: hi==lo)
depth_hi=9 depth_lo=4 depth_abl=4                    (recruits deeper; ablation conflict=0 → base, INERT)
```
Monitor(4/4) + dissociation(2/2, conflict separates what net-tension merges) + downstream/ablation(2/2).

**Conjunction fixture — `conjunction_fixture.hexa` = 8 pass / 0 fail** (LIVE VAdaptField, 2nd cell grown by
the real p8 mitosis tick `vadapt_field_step`→`engine_mitosis_tick`, reads `vadapt_field_two_recon_err`):
```
d_mid=[0.707, 0.707]   d_single=[0.707, 1.871]      ← SAME d1 (WTA sees identical), DIFFERENT d2
wta_mid=0.214 == wta_single=0.214                    ← ABLATION (read d1): INERT, no discrimination
full_mid=0.214  >  full_single=0.0                   ← FULL op (read d2): SEPARATES conjunction
```
mid=conjunction→1, single→0, far→0, single-cell field→0. The `d1`-collapse ablation is INERT; the `d2` read
is where the whole capability lives.

## (c) disjoint check (a_substrate_disjoint) — both ops PASS by construction

| op | reads | writes | Ψ (pure_field Φ/phase/Ψ) | emit-drive lane 0/4 (ci_emit_drive) | §ImmuneMemory recall_thr |
|----|-------|--------|:---:|:---:|:---:|
| `vadapt_field_conjunction[_score]` | VAdaptField protos only (top-2 accessor) | nothing (pure read → float) | untouched | untouched | untouched |
| `conflict_scalar` (gap #3, existing) | a_drive,g_drive scalars | nothing (pure read → float) | untouched | READ emit_drive only¹ | untouched |

¹ Per H_9095: conflict_scalar's ONLY downstream effect is recruiting **deliberation depth** (the
tension_resolve maxdepth axis), never overwriting the emit gate — H_1561 (savant invading the shared
emit-lane → Ψ collapse) is thereby avoided. Conjunction is a fresh read-only readout lane over MITOSIS
protos, disjoint from emit-drive and recall_thr → capability ∧ Ψ=½ ∧ G5 non-fab can co-exist. **Placement-
first satisfied for both.**

## (d) output paths

- `state/substrate_conjunction/conjunction_readout.hexa` — gap#1 op skeleton (2 ops + ablation twin; self-test).
- `state/substrate_conjunction/conjunction_fixture.hexa` — gap#1 engine-native falsifier (**8/8**, live mitosis).
- `state/substrate_conjunction/ag_conflict_monitor.hexa` — gap#3 provenance + named alias to live conflict_scalar.
- `state/substrate_conjunction/ag_conflict_fixture.hexa` — gap#3 engine-native monitor re-verify (**8/8**).
- `state/substrate_conjunction/notes.md` — this file.

**Untouched:** HYPOTHESES.jsonl · UNIVERSE cards · commit · PR · CHANGELOG · ARCHITECTURE.json · frozen verdicts · core/*.hexa.

## HONEST SCOPE (c9 / a_engine_native_learning)

- **gap #1 conjunction — MONITOR/DETECTION leg is engine-native GREEN candidate** (8/8, ablation INERT,
  Ψ-disjoint, runs on the LIVE VAdaptField). It is a **read-only detector**, NOT a generation/recombination
  op — deliberately, to stay outside the DPI wall. It does NOT claim to open G1. **Not yet WIRED**: op lives
  in `state/` only; rung-3 (lift `vadapt_field_conjunction[_score]` into `core/engine_cli.hexa` §ADAPTATION
  using `_vtwo_nearest_dist` directly — zero geometry change) + rung-4 (ARCHITECTURE.json lockstep) are the
  follow-on. `wired: DIRECTIONAL-mirror → engine-native (this fixture) → WIRED-live (TODO)`.
- **gap #3 conflict — monitor leg is ALREADY engine-native GREEN + WIRED** (H_9094/H_9095). This slug only
  re-verifies it independently and names the alias; nothing new to wire.
- **CAPABILITY leg (both gaps) = DIRECTIONAL, NOT claimed.** "conjunction detection improves some downstream
  outcome" and "conflict-driven exploration > fixed exploration" are outcome claims measured **nowhere here**.
  Per H_1836/1837 (temporal/decode-procedure readout axes floored — "just resample" collapses to DPI floor),
  any capability wiring must be **conflict-CONDITIONAL / conjunction-CONDITIONAL pre-registered**, never an
  unconditional resample. This slug closes only the **monitor/detector** legs.
- The tier here is fixture-verified (8/8 each, engine-native, deterministic). NO card/jsonl/CHANGELOG stamp
  was made (per task constraint) — promotion to a HYPOTHESES verdict is a separate registered step.
