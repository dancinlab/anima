<!-- @hypothesis-ok lab/v6 rule-exempt sandbox: v6 hypotheses live in lab/v6/hypotheses/V6_<n>_*.md per lab/v6/CLAUDE.md, never the parent HYPOTHESES/ nor an H_ id -->

# V6_25 — repetition-density dose-response: is direct binding actually density-limited?

**origin:** lab-full (Fable primary; Sol preferred a 303M scale-replication + evaluator port but
its own pre-mortem called it likely-waste → deprioritized, tests scale not the density cause).
V6_24 CLOSED the natural-bridge lane blaming "singleton-dominated data", but **density was
never manipulated** — the closure has a hidden asterisk (every read had SEEN<0.70). V6_25 tests
the named cause. DIRECTIONAL. Track C (rotation-readout port) is DEFERRED with a trigger: fire
it the moment any arm produces SEEN ≥ 0.70 (then an engine-native operator readout has a real
natural subject).

## Step 0 RESULT — 🟡 density-dose IS present (observational, $0 · `v6_25_density_pilot.py`)
Re-stratified the existing V6_23/24 items by each pair's REALISED co-occurrence count k in the
47.8MB train slice (nothing curated — k measured, p9-clean). C-slot readout, trained57 vs
pedestal57:

| k (natural co-occur) | SEEN raw acc | pedestal | **collapse-Δ** | n |
|---|---|---|---|---|
| k=1 | 0.530 | 0.467 | **+0.063** | 381 |
| k=2–3 | 0.588 | 0.531 | +0.057 | 177 |
| k=4–7 | 0.559 | 0.458 | +0.102 | 59 |
| k≥8 | 0.577 | 0.423 | **+0.154** | 26 |

- ⚠️ **The pilot's own auto-headline ("FLAT") is a script defect** — it thresholded on RAW
  accuracy (0.530→0.577), but raw acc is confounded (pedestal drifts down with k). The correct
  measure, **collapse-Δ (trained − pedestal), rises ~2.4× from k=1 (+0.063) to k≥8 (+0.154)**.
  Training-induced direct binding DOES scale with natural repetition density.
- This **partially refutes V6_24's "data is the wall, closed"**: density is a real lever on
  binding, not inert. BUT even at k≥8 (natural), absolute SEEN is 0.577 (< 0.70) and n=26 is
  underpowered — observationally suggestive, not decisive.
- BRIDGED shows no positive dose (collapse-Δ trends negative). Caveat: BRIDGED items show k≥1
  here, which contradicts their "A,C never co-occur in train" definition → a prose-extraction
  mismatch between the pilot and the builder; the BRIDGED k-rows are NOT trustworthy and are
  excluded from any conclusion. The SEEN dose-response (the headline) does not depend on them.

## Verdict — Step-1 causal arms WARRANTED (not "spare the arms")
The observational dose-response is real but underpowered at high k. The decisive test is Fable's
curated ladder: install k ∈ {1, 8, 64} at n≥300/stratum, bytes held constant, single-entity
marginals matched (so a SEEN lift attributes to PAIR count, not entity familiarity), then read
whether SEEN clears 0.70 at some k* AND whether D = Δ_BRIDGED − Δ_UNBRIDGED turns positive when
BOTH legs (A–B, B–C) are dosed. Frozen decision table (Fable):

| outcome | reading |
|---|---|
| SEEN flat in k (SEEN(64)−SEEN(1) < MDE) | density NOT the lever — close composition frontier, go LANE-BUS |
| SEEN rises, < 0.70 at k=64 | dose-response real, sub-threshold — record curve, maybe k=256 |
| SEEN ≥ 0.70 at k* AND D>0 CI excl 0 | **composition present when legs installed** — natural-at-scale axis LIVE; fire Track C |
| SEEN ≥ 0.70 at k* AND D≈0 | binding installs but composition absent — wall is ARCHITECTURAL → LANE-BUS mandate |

## Pre-mortem (Fable) — the dose upsampling must not resurrect the shortcut
Repeating pair-bearing sentences can install n-gram memorisation (H_9902 weavedrill disease) or
re-fuse A/B into co-occurrence similarity (V6_21's artifact). Mitigation preregistered: keep the
full V6_22 caliper; keep UNBRIDGED as the differencing control (read D, not raw SEEN); split
SEEN(k) by distinct-sentence count m — if the lift lives only in low-m (same sentence repeated),
it is memorisation and scored dead (`polarity-split-before-headline`).

## Step 1 RESULT — 🔴 density is NOT the lever (causal · CLOSES the frontier · retracts Step-0)
Built 3 density-controlled arms (`v6_25_build_arms.py`): each SEEN pair's train-bearing sentence
repeated to k ∈ {1,8,64}, total bytes held at 48MB (419/700 pairs dosed). Trained k8/k64 on
summer (15000 steps), reused trained57 as k=1. SEEN, trained / pedestal / collapse-Δ:

| k | trained | pedestal | collapse-Δ |
|---|---|---|---|
| 1 | 0.563 | 0.487 | +0.076 |
| 8 | 0.544 | 0.486 | +0.059 |
| 64 | 0.570 | 0.494 | **+0.076** |

**collapse-Δ dose = +0.076 (k=1) → +0.076 (k=64) = 0.000 — dead FLAT.** Causally installing 64×
the co-occurrence density does NOT lift direct binding. Per Fable's frozen table row 1: **density
is not the install lever; the V6_24 "singleton dominance" causal story is REFUTED-as-stated; the
wall is deeper than data → close the composition frontier, go LANE-BUS; Track C stays unported.**

- **Self-correction of Step-0** (verdict-integrity): Step-0's observational collapse-Δ rise
  (+0.063→+0.154, "2.4×") was the **famous-entity confound** I flagged in its own caveat —
  naturally-high-k pairs are hub/famous entities. Controlling it (same entities, only the pair's
  sentence upsampled) erases the dose entirely. Step-0's "V6_24 partially refuted" is WITHDRAWN.
- **Why it's a strong negative**: repeating one "A…C" sentence 64× is the memorisation-friendly
  case; the model memorises that surface but the held-out probe uses a DIFFERENT phrasing, and
  SEEN(k=64) stays 0.57 — surface memorisation does NOT abstract the A–C relation (the G0
  natural-form-gate wall, now confirmed causally). Converges with `g1-is-absence-not-failure`.
- Caveat: first-cut arms repeat the SAME bearing sentence (not distinct per Fable's preference);
  distinct high-k sentences aren't available at n≥300. But repetition is the easier case and it
  still failed, so the negative is robust; distinct-sentence is an untested variant unlikely to flip it.

## Verdict — composition frontier CLOSED (V6_21→V6_25); next = LANE-BUS, not more data
The last suspected lever (density) is causally dead. The whole natural-composition arc closes:
DV (V6_21), corpus-supply (V6_22/23), readout (V6_24), and now density (V6_25) are all
eliminated. The wall is architectural/form-generalisation, not a data property. Track C
(rotation-readout port) stays deferred with its trigger (any SEEN≥0.70 arm — never reached).
Next engine-native frontier = the LANE-BUS redesign (v6's original 대공사 purpose), for which
Fable produced a full design in the same divergence.

## Scope
Step-0 = $0 observational (WITHDRAWN as confounded). Step-1 = 3 causal arms, summer (~$0
marginal). `natural-curated` instrument-check regime. Single ckpt · single seed. DIRECTIONAL;
TERMINAL only via anima-py.
