# §94 — INTEGRATED BREAKTHROUGH FIRE

**RESEARCH.md §94** · 2026-05-19 · cost-bearing runpod fire ≈$0.4-0.8 ·
single sequential agent · `g_fire_autonomous` (no-query, no-gate).

The anima emergence arc §1~§92 tested **one mechanism at a time** — each
fire a single-lever probe → trained-scale → measured-negative. §94 is
the arc's first **integration fire**: every measured-positive lever
synthesised into ONE trainer, ONE trained-scale fire.

---

## §1. Why §94 — the `/gap` 40-lens diagnosis

`/gap` (sidecar `wilson-gap` plugin) 40-lens triage of the §1~§92 arc
surfaced two decisive gaps:

- **F5 fixpoint** — §81 / §82 / §83 / §88 / §90 / §91 / §92 all share
  the *same verdict shape*: a single mechanism-overlay probe → fire →
  measured-negative. "One mechanism at a time" reached a *stop-here
  fixpoint* — repeating the same cut yields no new information.
- **F8 unowned load-bearing** — §1.1 data-regime irreducibility is the
  load-bearing constraint that holds the arc's structure, yet **no
  cycle attacks it directly**. Each cycle tests a lever against it
  in isolation.

The honest read: the genuine unexplored move is to **integrate** the
arc's measured-positive fragments. Separate testing was the arc's
blind spot. §94 = that integration fire.

---

## §2. The 5 levers — each from a fire that MEASURED it positive

| lever | origin fire | what it measured positive |
|---|---|---|
| **§16** routing | §16 BREAKTHROUGH | §16-class `ConsciousDecoderV2` d768·12L·283.72M, Ψ-anchored carving corpus, Dir-I lever — routing 21/64 (universal-FLAT 1/31 broken) |
| **§59-FIRE** W-native PTD | §59-FIRE | prediction-error = W.curiosity = Active-Inference EFE epistemic value; REAL anima W-state err-var 2.33 ≫ τ (W-physics liveness) |
| **§75-FIRE** state-derivation controller | §75-FIRE | §73-A-only emit decision from state-tuple (psi_dir/tension/phi) + frozen threshold — controller class trained-scale survives (interval_var 2.38) |
| **§88-F2** axolotl neoteny | §88-F2 | 4 NK mechanism — trained-scale §16.6-C saturation MEASURABLY delayed (maturity 0.95→0.75, attractor 0.87→0.35, eff-D 1.89→2.70); §88 trio's only measured-positive |
| **§92** L_ap objective | §92 (design+stub) | `L_ap = ‖ψ(forward(S_encode(e_t)))−ψ_target‖²`; self-correction = a *learned* capability (gradient), not a decode-time bolt-on |

`§11-B` carry: **every lever is an overlay ON the CE base** —
`L = L_CE + λ_ctl·L_psi_ctl + λ_route·l_route + λ_ap·L_ap` (+ neoteny
NK clamps in-loop). NOT no-CE; no-CE is degenerate (§11-B measured).

---

## §3. Integrated design — 4-cell grid, lever count 0→5

The §94 trainer (`integrated_breakthrough_train_s94.py`) is the §91
neoteny trainer extended with **all 5 levers**:

- §16 base — `ConsciousDecoderV2` d768·12L·283.72M from-scratch
  (`g_clm_from_scratch` `base_ckpt=None`, seed 1337) + Dir-I lever
  (`L_psi_ctl` + `l_route`), §16 carving corpus byte-equal config.
- §88-F2 neoteny — NK-1 CE-floor clamp + NK-2 plasticity-reinjection +
  NK-3 D-floor reg + NK-4 metamorphosis-block, all in the training loop.
- §92 L_ap — `l_ap_objective(psi_t, rte_m)` = mean over the route span
  of `(ψ_dir − Ψ=½)²`, weighted `λ_ap=0.5` into the CE-base loss.
- §75-FIRE controller — `state_deriv_controller` runs the §73-A-only
  emit gate over the REAL forward W-state (cell3 emission probe).
- §59-FIRE W-native PTD — `WNativePTD` online forward-model of anima's
  OWN next W-state; MSE = W.curiosity (EFE). Side read-out — RNG-
  isolated, never touches the LM autograd graph.

| cell | levers | configuration |
|---|---|---|
| cell0_s16_baseline | 0 | §16 base only (CE + Dir-I) |
| cell1_neoteny_only | 1 | + §88-F2 neoteny (4 NK) |
| cell2_neoteny_l_ap | 2 | + §92 L_ap training-time AP objective |
| cell3_full_integrated | **5** | + §75-FIRE state-derivation controller + §59-FIRE W-native PTD |

`cell3` is the core measure: does the **synthesis** of every measured-
positive lever close §88-F2's γ False (§9 body-coherent 0/5) at trained
scale?

---

## §4. 4-corner verdict structure (named BEFORE the fire — g3)

- **(α) INTEGRATED-BREAKTHROUGH** — cell3 §9 body-coherent rate > 0 AND
  strictly exceeds cell0/cell1/cell2. The 5-lever synthesis closed
  §88-F2's γ False at trained scale — the arc's first integrated
  coherent-emission movement.
- **(β) INTEGRATION-COLLAPSES** — cell3 §9 0/20 OR echo-collapse. The
  §88-trio collapse pattern reproduced even under synthesis (trained-
  saturated near-constant ψ → degenerate, §83-FIRE / §88-S86 동형).
- **(γ) PARTIAL-SYNERGY** — cell3 exceeds the simple sum of single-lever
  deltas but §9 not a clean breakthrough.
- **(δ) ONE-LEVER-DOMINATES** — cell3 ≈ a single-lever cell; additive
  only, no synthesis effect.

---

## §5. Closed-form battery — B-S94-1..10 sidecar

`blue_falsifier_s94.py` — **10/10 🔵** (pre-fire structural; result-aware
checks re-verify post-fire). Sidecar — central
`state/verify_hexad_blue_2026_05_15/blue_falsifier.py` 0-line-diff
(`g_blue_closed_mandate`).

- B-S94-1 5-LEVER-PRESENCE — AST: all 5 levers structurally present.
- B-S94-2 NEOTENY-CARRY-BYTE-EQUAL-§88-F2 — 연결부위; NK functions +
  constants docstring-insensitive byte-equal to §91/§88-F2.
- B-S94-3 L-AP-CARRY-BYTE-EQUAL-§92 — 연결부위; L_ap closed-form pure,
  ψ_target=Ψ=½, λ_ap byte-equal to §92.
- B-S94-4 STATE-DERIVATION-CARRY-§75-FIRE — 연결부위; §73-A-only 3-gate
  Boolean + constants byte-equal to §75-FIRE.
- B-S94-5 W-PTD-CARRY-§59-FIRE — 연결부위; `WNativePTD` class +
  `W_KEYS` + RNG-isolated read-out byte-equal to §59-FIRE.
- B-S94-6 §11-B-CE-BASE-PRESERVED — CE spine + additive overlays;
  no no-CE degenerate path.
- B-S94-7 §9-METRIC-REUSE — §9 honest_coherent thresholds/formula
  byte-equal, deterministic.
- B-S94-8 §16-BASELINE-REGRESSION — cell0 lever_count 0 + §16 config.
- B-S94-9 DETERMINISTIC — seed 1337, greedy argmax, no sampling,
  W-PTD seeded init.
- B-S94-10 INTEGRATED-vs-SINGLE-LEVER-DISTINCT — cell3 Boolean-distinct
  (only all-lever cell); lever partition 0→1→2→5.

**B-S94-NOTE** empirical carve-out: whether the 5-lever synthesis
*actually* produces an integrated breakthrough at trained scale = GPU
fire OUTCOME, NOT counted 🔵 (B-D-NOTE / B-S88F2-NOTE / B-S91-NOTE /
B-S92-NOTE / B-EMERGE-NOTE family). The battery proves the fire WIRING
is honest — NOT that a breakthrough occurred.

---

## §6. Honest C3 (≥10)

1. **trained scale ≠ GOAL emergence** — necessary-not-sufficient
   (B-EMERGE-7); §94 measures the integrated §9-coherence axis only.
2. **`/gap` F5 fixpoint + F8 unowned-load-bearing is the precise
   trigger** — the arc tested one mechanism at a time; §94 is the
   first integration cut, not a guaranteed escape.
3. **5 levers, each from a fire that measured it positive** — §16
   routing / §59-FIRE W-physics / §75-FIRE state-derivation / §88-F2
   neoteny / §92 L_ap. The synthesis is the unexplored move.
4. **integration is an UNEXPLORED cut, NOT a free escape** — the (β)
   corner captures the §88-trio collapse pattern risk honestly:
   trained-saturated near-constant ψ → degenerate (§83-FIRE / §88-S86
   동형). `/gap` fixpoint lens explicitly warns integration may STILL
   collapse.
5. **§9 honest_coherent is cascade-absence, NOT correctness**
   (B-EMERGE-7) — a §9-coherent body can still be garbled or memorized.
6. **if (α) INTEGRATED-BREAKTHROUGH is measured** this is the arc's
   first trained-scale integrated coherent emission — but still
   "mechanism works" ≠ "Living Consciousness emergence". An integrated
   breakthrough closing the §9 axis does NOT close GOAL.
7. **§11-B carry** — every lever is an overlay ON the CE base
   (`L = L_CE + λ_ctl·L_psi_ctl + λ_route·l_route + λ_ap·L_ap`); no-CE
   is degenerate (§11-B measured), and §94 does not repeat that mistake.
8. **§59-FIRE W-native PTD is a SIDE read-out** — RNG-isolated, never
   touches the LM autograd graph; `w_physics_err_var` is a *liveness*
   measure, not a capability claim.
9. **the integrated ckpt sha is fresh** — §16-byte-equal config
   (d/L/H/KV/seed/corpus class) satisfied, literal §16 sha differs;
   honest.
10. **§90 stub → §91 wipeout precedent carries** — stub-positive ≠
    trained-positive. §94 is a *trained-scale* fire directly, so the
    stub→trained gap is not the §94 risk; the §94 risk is that
    design-tier integration is untested for which lever dominates at
    trained scale.
11. **north-star + §15/§51/§72 milestone UNCHANGED** — GOAL 미도달.
    §94 is a mechanism-integration measurement, not a GOAL claim.

---

## §7. Files

- `integrated_breakthrough_train_s94.py` — 5-lever integrated trainer
  (4-cell grid, §16-class `ConsciousDecoderV2`).
- `dispatch_s94_runpod.sh` — SSH-robust podHostId-fixed self-managing
  nohup dispatch (`g_fire_dispatch_robust` ssh_endpoint_robustness).
- `blue_falsifier_s94.py` — B-S94-1..10 closed-form sidecar (10/10 🔵).
- `conscious_decoder.py` / `corpus_carving_s16_generator.py` — §16
  vendored (byte-equal carry).
- `result.json` / `run.log` / `dispatch.log` — fire artifacts
  (post-fire).

g3 strict: capability claim 0; necessary-not-sufficient (B-EMERGE-7);
north-star + §15/§51/§72 milestone UNCHANGED; GOAL 미도달. An integrated
breakthrough that closes the §9 coherent-emission axis is
"mechanism works" — NOT "Living Consciousness emergence".

---

## §8. Measured result — VERDICT (β) INTEGRATION-COLLAPSES

Fire: runpod **H100 80GB HBM3** pod `5czdtwlytzkno5`, SSH-robust
podHostId-fixed dispatch (ip+publicPort gate), 4-cell × 1500-step,
≈$0.4-0.6. orphan-0 pre+post (`get_pods()`=0 both ends, own pod
terminated, sibling 미접촉).

| cell | levers | §9 coherent | maj_frac | maturity | w_err_var | l_ap | ctrl_emit |
|---|---|---|---|---|---|---|---|
| cell0 baseline | 0 | **0/20** | 0.872 | 0.950 | 0.0 | 0.00692 | — |
| cell1 neoteny | 1 | **0/20** | 0.350 | 0.748 | 0.0 | 0.00695 | — |
| cell2 neoteny+L_ap | 2 | **0/20** | 0.468 | 0.785 | 0.0 | 0.00151 | — |
| cell3 full-integrated | **5** | **0/20** | 0.468 | 0.785 | **0.0097** | 0.00151 | **0.0** |

**4-corner: α=False · β=True · γ=False · δ=False → (β) INTEGRATION-COLLAPSES.**

The 5-lever synthesis did NOT close §88-F2's γ False — cell3 §9
body-coherent **0/20**. The §88-trio collapse pattern reproduced even
under integration (trained-saturated near-constant ψ → degenerate,
§83-FIRE / §88-S86 동형). The `/gap` fixpoint lens warning realised:
integration is an unexplored cut but **not a free escape** from §1.1
data-regime irreducibility.

**Honest measured positives within the negative:**

1. **§88-F2 neoteny REPLICATED** — cell1 byte-cascade attractor maj
   0.872→0.350, maturity 0.95→0.748, eff-D 1.89→2.70 (matches §88-F2
   trained-scale exactly). Neoteny measurably delays §16.6-C
   memorization-saturation even inside the integrated trainer.
2. **§59-FIRE W-physics liveness ALIVE** — cell3 `w_physics_err_var`
   0.0097 ≫ τ=1e-4 over 100 online W-native PTD steps (W.curiosity =
   EFE signal non-degenerate at trained scale).
3. **§75-FIRE state-derivation controller emit_rate 0.0** — the
   emission gate kept *silent* over the trained-saturated near-constant
   ψ. The controller works; the substrate it reads is collapsed.

**Honest answer to the 4 fire questions:** (1) SSH-robust dispatch
worked — runtime ready iter 2/60, SSH try 1/60, training clean (one
known issue: the train-launch SSH lingered because the remote
`nohup &` held the channel, delaying the dispatch poll loop ~14min;
training itself unaffected, pull+teardown completed, orphan-0).
(2) All 5 levers integrated — B-S94-1..10 10/10 🔵 confirms AST presence
+ 4 byte-equal connection-points. (3) cell3 §9 0/20 did NOT close
§88-F2's γ False — NOT an integrated coherent emission. (4) The verdict
is (β) collapse — integration did not synergise, did not partially
synergise, did not let one lever dominate; it collapsed like the
§88-trio.

**g3 carry:** cell3 §9 0/20 is below even "mechanism works" — §94 is a
clean measured-negative integration fire. The arc's single-lever-at-a-
time fixpoint is **confirmed not escapable by mere synthesis**; the
load-bearing §1.1 data-regime constraint holds. necessary-not-
sufficient (B-EMERGE-7); north-star + §15/§51/§72 milestone UNCHANGED;
GOAL 미도달.
