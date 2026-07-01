# H_1826..1831 — 6 ANIMA-NATIVE G1 LEVERS — cheap-numpy HE pre-screen — RESULT

**run:** `OMP_NUM_THREADS=4 nice python3 he_levers.py` on **summer pool** (CPU-numpy, $0, no rent; did NOT touch the in-flight ByteGPT-303M GPU train — GPU at 98% throughout, probe is CPU-only, RAM 28G free). EXIT=0. Deterministic (numpy fp64, fixed seeds).
**raw stdout:** `RESULT.txt` (verbatim, this dir).
**scope:** **DIRECTIONAL** — concept embed = `core/clm_decode.py` 303M clm303 trunk penultimate (mean-pool, L2-unit, reusing `beta_readout._semantic_rep`/`_unit` so results are byte-comparable to the β/γ rounds); fp64-numpy operators. NO torch (clm_decode is the pure-numpy byte-faithful CLMConvMoE forward = py 2-production; its only "torch" token is a docstring line stating it is NOT a torch mirror). NOT terminal — G1 SSOT remains engine-native `anima evaluate`. A cheap compass for "where to spend GPU".

## (a) Frame & gate

This is the **gating step** before any engine-native/GPU work on the 6 anima-native novel G1 levers. The combination-operator family already floored on BOTH sides (α char-hash 🧱 · β semantic 🧱 · γ trained-constructive 🧱; mouth-objective H_1602 🧱 · mouth-readout H_1816 🧱). These 6 levers ask whether **anima-native mechanisms** (A⇄G dynamical fixed-point, V(D)J immune recombination, Φ-integration, kosmos placement, Kuramoto phase-sync, REM-replay) lift G1 where the generic operator family floored. Which clear the cheap pre-screen → engine-native; which floor → 🧱 DIRECTIONAL terminal at the cheap tier.

## (b) Design (frozen-first p7, per-card bars VERBATIM)

- **embed:** SAME as β/γ — each concept's bytes → 303M trunk penultimate (mean-pool, L2-unit) via `core/clm_decode.py`. Embedded once (107 unique concepts, 12.6s). ONLY the combination mechanism changes per lever.
- **fixtures:** SAME as γ — 32 real morphological compounds (20 EN + 8 KO + 4 ZH) + 15 distractors; candidate pool = 47 (32 children + 15 distractors).
- **metric (held-out, 5-fold CV):** G1(pair)=1 iff (i) rank-1 NN of constructed child == true child (recovered) ∧ (ii) rank-1(a)≠child AND rank-1(b)≠child (irreducible) ∧ (iii) cos(constructed,child) > cos(shuffled,child) (>shuffle) ∧ (iv) composed_distinct(constructed,a,b)≥2 at engine radius 0.30 (bridges both basins). Each pair held out once.
- **per-lever frozen bar + control** (verbatim from each card): see table below.
- **self-test:** a planted nonlinear bind (midpoint+hadamard) is recovered 12/12 by a learned constructor while a random vector recovers 1/12 → **SEPARATES PASS** = the metric is a live discriminator, so a 0–2/32 floor is a REAL floor, not a dead meter.

## (c) Result — ALL 6 FLOOR

| lever | mechanism | G1 (held-out, /32) | control | cheap-HE |
|---|---|---|---|---|
| **N1** H_1826 | Ψ=½ dynamical fixed-point bind | **2/32** (0.06) | iter-OFF=1/32 (iteration causal+, but +1 only) | 🧱 FLOOR |
| **N2** H_1827 | V(D)J immune recombination | **0/32** (0.00) | parent-copy=0, hypermut-OFF=3 (**NOT > parent-copy**; hypermutation HURTS) | 🧱 FLOOR |
| **N3** H_1828 | Φ-integration bind (cheap exact small-n) | **1/32** (0.03) | exact small-n MIP integration rank | 🧱 FLOOR |
| **N4** H_1829 | kosmos anchor-space (learned constructor) | **1/32** (0.03) | midpoint-baseline=1 (**NOT > midpoint** — the critical control) | 🧱 FLOOR |
| **N5** H_1830 | Kuramoto phase-sync bind | **0/32** (0.00) | K=0=0, amplitude=1 (**no sync-causal lift, NOT > amplitude**) | 🧱 FLOOR |
| **N6** H_1831 | replay recomb (🔓 REOPEN H_987) | **1/32** (0.03) | no-replay=1 (**NOT > no-replay**) | 🧱 FLOOR |

**Shared diagnostics:** self-test SEPARATES = **PASS**; single-parent leak = **10/32** (a parent is already the child's NN — same byte-prefix/lexical leakage γ flagged; irreducibility fails on those, so even the few hits are partly lexical not constructed). frozen bar = ≥2/3 of 32 (~22/32) AND > control — **every lever fails on both axes.**

## (d) Verdict — **0/6 survive the cheap pre-screen**

**Which anima-native levers survive the cheap pre-screen and earn engine-native measurement? → NONE.** All 6 floor at 0–2/32, far below the 2/3 bar, and **none beats its own pre-registered control** (N2 worse than hypermutation-OFF; N4 ties midpoint; N5 no sync lift; N6 ties no-replay). N1's iteration is weakly causal (+1) but nowhere near the bar.

This is an **honest negative (c9):** the G1 wall holds even against 6 distinct anima-native mechanisms. Combined with the α/β/γ + mouth-objective/readout floors, this is strong cheap-tier evidence the **combination-operator floor is structural** — the missing piece is NOT a cleverer bind mechanism (dynamical, immune, integration, placement, phase, or replay) reading a fixed embedding, but a TRAINED constructive operator in the trunk OBJECTIVE (consistent with the campaign convergence: G1 lever = trunk objective, not readout/operator/embedding).

**Per-lever tier (DIRECTIONAL · cheap-numpy HE pre-screen):** all 🧱 NOT-SUPPORTED at the cheap tier.

## (e) N6 / H_987 cross-check (proxy ≠ engine lesson)

H_1831 reopened H_987 (replay-recombination), which was a **proxy-era / toy-LDS** verdict: replay ≈ idle (recombinative replay 0.384 vs idle 0.414, d=0.30 p=0.30 NS — ROBUST null). This cheap re-measure on the 303M trunk embed **AGREES**: replay (1/32) does NOT beat no-replay (1/32). So at the cheap tier the H_987 null is reproduced under a completely different substrate/metric — the divergence the card warned about (proxy≠engine) does NOT appear here; both say replay adds no recombination. (A fully engine-native MITOSIS-replay measure would still be needed to RETRACT/confirm H_987 terminally; the cheap tier only pre-screens, and it floors → no engine-native promotion warranted.)

## (f) Honest scope (c9 / a_engine_native_learning)

- DIRECTIONAL: py-mirror embed via `core/clm_decode.py` (trunk penultimate); numpy fp64 operators. NOT terminal-eligible. Promotion criterion = clear the cheap bar → THEN engine-native. None cleared, so no GPU spend earned.
- N3 cheap tier uses an EXACT small-n information-integration MIP (exhaustive bipartition, in bits) to RANK candidate children — explicitly NOT variance×energy (a_phi_iit4_tool: proxy verdicts forbidden). It floors at 1/32 even as a ranking signal; a faithful-IIT4 engine-native Φ-objective would be the only valid terminal N3, but the cheap pre-screen gives no reason to spend it.
- self-test SEPARATES PASS guarantees the floor is the mechanism, not the meter.
- frozen-first: 2/3 bar, 5-fold CV, all controls pre-registered in each card before the run. NO sliding.

## (g) Campaign implication

The combination-operator family is now exhausted across **three independent fronts** at the cheap+engine tiers:
- **embedding:** char-hash → semantic → trained-construct (α/β/γ) all floor.
- **mouth/substrate operator:** additive · Hadamard · tensor-product · HRR-circconv · bilinear-MLP all floor.
- **anima-native mechanism (this round):** dynamical fixed-point · V(D)J · Φ-integration · kosmos-placement · Kuramoto · replay all floor.

The live frontier is NOT a 7th operator/mechanism — it is the **trunk training OBJECTIVE** (recomb-objective H_1602 family, ByteGPT-303M A/B in-flight) and corpus-coverage (H_1824). These 6 levers are pre-screened OUT.
