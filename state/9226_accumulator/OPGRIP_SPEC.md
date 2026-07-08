# H_9226 — accumulator-to-threshold BUFFER op-grip spec (Family B · DDM evidence-integration)

> **Provenance:** Fable wrote this spec in design-only (read-only) mode; it did NOT persist to
> disk on `origin/main`. This file was reconstructed verbatim from the authoritative design
> summary and committed as the preserve-state SSOT for the H_9226 op-grip harness.
> **Status:** 🛠️ IMPLEMENTED (`cli/anima.hexa`, extends the H_9225 D1/D2/D3 block · 3-site) ·
> engine-native summer $0 op-grip **PENDING** (do NOT fire on summer while its 303M job runs).

## 0. Premise (why Family B is DISTINCT, not A-redundant)

Family A (H_9225 tonic→phasic transducer) measured 🔴 THEATER (#3181): converting self+tension
to a phasic Δ left emit unchanged — the currency-mismatch spine is FALSIFIED. Family B is the
surviving DISTINCT mechanism: **NOT a currency conversion** — a leaky **ACCUMULATOR** that
integrates a weak-but-persistent self/tension bias over ticks to a decision-boundary crossing
(drift-diffusion / DDM). Its distinguishing evidence is a **LATENCY signature** (the effect
appears only after N≈8 consistent ticks, not at signal onset) + **collapse under tick-ORDER
shuffle**. A and B are told apart by their latency fingerprint (A = transition-concentrated at
onset; B = N-tick latent then a gate-crossing).

## 1. Arithmetic (per lane · SELF x=`self_ctx_live` ⊥ TEN x=`ag_conflict`)

```
acc = 0.90*acc + (x − x_base)                 # leaky integrator, λ = 0.90
acc → 0   on the arm's OWN emit                # HARD reset — DDM discharge-at-decision
x_base = median of x over calibration ticks 10–49
b_med  = median |x − x_base| over ticks 10–49
G      = min( 0.175*(1−λ)/b_med , 32.0 )       # = min(0.0175/b_med, 32.0)
shade(acc) = clip01( 0.5 + G*acc )
idle_accSlf = 5 + 55*clip01( stage_env * (0.5 + urgency + 1.0*(shade(acc_slf)−0.5)) )   # W_SELF = 1.0
idle_accTen = 5 + 55*clip01( stage_env * (0.5 + urgency + 1.0*(shade(acc_ten)−0.5)) )   # W_TEN  = 1.0
```

Own-lane idle is **DISJOINT** from urgency AND from the H_9225 phasic lanes (`a_substrate_disjoint`).
`|shade| ≤ 0.5` by clip. A SUSTAINED median bias charges to exactly the H_9101 coupling-invariant
swing **0.175** (steady state acc* = b_med/(1−λ), so G·acc* = 0.175).

## 2. Charge math (why N=8 is non-arbitrary)

Charge after `r` consecutive consistent ticks = `1 − 0.9^r`:
- r=3 → 27% charge (swing ≤ 0.047, **sub-gate**)
- r=8 → 57% charge (≈ 0.10, **gate-visible**)

An integrator **cannot flip early** and **should flip late**. This is the latency signature.

## 3. Guards (frozen · never cement THEATER)

- **CAP-SAT** (carried from H_9225): `g==32 ∧ 32*b_med < 0.0875` → UNDER-COUPLED → INSTRUMENT-FAIL.
- **STIM-ABSENT** (NEW · B-specific): `swing_max < 0.0875` (acc trajectory never held a bias long
  enough to half-charge) → INSTRUMENT-FAIL, **never THEATER**.
- **AXIS-DEGENERATE**: `b_med < 0.002` → `g = −1.0` → INSTRUMENT-FAIL ($0 no-decode expected; fix
  = `--opgrip-live`).

## 4. Three arms

- **LIVE** — accumulator active (`idle_accSlf`/`idle_accTen`).
- **FROZEN** — shade pinned 0.5 ⇒ `idle_frzB` byte-identical to prod `e_live`. Invariant
  `og_h_frzB == 0` — else HARNESS-BUG, run VOID.
- **POSITIVE CONTROL** — reuse the existing dense ARM-SHOCK `og_h_shock_mid` (POS-PASS ≥ 2).

SELF ⊥ TEN scored separately → independent verdicts.

## 5. Latency signature (B's evidence)

Per-tick **sign-run length** of the bias `(x − x_base)` with a `0.5*b_med` deadband (below the
deadband the sign is neutral and resets the run). Buckets on mid-scored ticks by current run
length: **EARLY (run 1–3)** / **GAP (4–7, unscored)** / **LATE (≥8)**.

```
BAR:  ΔEff_late ≥ 3*ΔEff_early  ∧  ΔEff_early ≤ 0.05  ∧  n_late ≥ 10
```

A `ΔEff ≥ 0.10` that FAILS this shape = **DIRECTIONAL** (instantaneous-reader phenotype,
A-redundant), NOT COMPETENT.

## 6. Theater-killer (order-shuffle re-integration)

Same stride-perm `j = (t*7+13) % N` reusing H_9225's recorded raw-input arrays
(`og_f3_xself` / `og_f3_xten`), but **re-INTEGRATED post-loop** with the calibrated gain +
per-tick re-decode (reset-on-own-emit dynamics faithful). A scrambled input order destroys the
persistent-bias structure the integrator needs. Margin bar **M = 0.08** (`ΔEff_live − ΔEff_inperm`).

## 7. Verdict ladder (frozen · printed BEFORE verdicts · p7 no tune-to-green)

1. **HARNESS-BUG** — `og_h_frzB > 0` → VOID.
2. **INSTRUMENT-FAIL** — POS-FAIL ∨ AXIS-DEGENERATE ∨ CAP-SAT ∨ STIM-ABSENT.
3. **FORCING-GATE** — `N3 > 0` ∨ `Ψ_ON < Ψ_OFF` ∨ `Ψ_ON − Ψ_OFF > 0.05` → REVERT.
4. **🟢 COMPETENT** — `ΔEff ≥ 0.10 ∧ shuffle-margin ≥ 0.08 ∧ latency-shape ∧ POS-PASS ∧ N3=0 ∧ Ψ-guard`.
5. **🔴 THEATER** — `ΔEff < 0.02 ∧ POS-PASS ∧ ¬degenerate ∧ ¬capsat ∧ swing_max ≥ 0.0875`.
6. **🟠 DIRECTIONAL** — else (incl. `ΔEff ≥ 0.10` that FAILS latency shape).

### INTERPRETATION (only if BOTH lanes THEATER)

B-THEATER after A-THEATER = **convergent seam-law**: shape-conversion (A) AND
evidence-integration (B) both inert at the idle seam under a passing dense POS-CONTROL ⇒ the emit
gate is causally sealed to everything but urgency; read-side recoding closed, remaining escalation
= **write-side (train-time coupling)**.

## 8. Implementation (3 edit sites in `cli/anima.hexa`, extend the H_9225 block)

- **Site A — carriers** (after the H_9225 Site-A carrier block): `acc_slf/acc_ten`, `xB_cal_*`,
  `xB_base_*`, `bB_med_*`, `gB_*`, `capsatB_*`, latency run state (`runlenB_*`/`runsgnB_*`),
  `swingB_max_*`, ΔEff/guard counters (`og_h_slfB_mid/n3/wake`, `og_h_tenB_*`), `og_h_frzB`,
  Ψ numerators, latency buckets (`earlyB_*`/`lateB_*`).
- **Site B — in-loop arms** (after the H_9225 in-loop arms, inside `if og_measure`): calibrate at
  tick 50, integrate post-calibration, latency sign-run, decode LIVE/FROZEN, score mid, guards,
  HARD reset on own emit.
- **Site C — post-loop verdict** (after the H_9225 verdict block, before `return`): ARM-INPERM
  order-shuffle re-integration, latency ΔEff, Ψ-guard, frozen bars, per-lane verdict, interpretation.
  Reuses `midf` / `pos_pass` / `live_anchors` / `n9` from the H_9209/H_9225 blocks (no re-decl).

Production `idle`/`e_live` **BYTE-UNTOUCHED** — measurement arms only; the additive-only diff
(0 deletions) + runtime `og_h_frzB == 0` are the proof. `a_substrate_disjoint` / p5 / p7.
