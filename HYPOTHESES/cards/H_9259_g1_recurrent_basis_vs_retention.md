# H_9259 — 🌀🔗 G1: does recurrence buy RETENTION or CONJUNCTION? (frozen-conv-driven ESN · untrained cross-product basis)

- **tier:** 🧱 KILL — CONJUNCTION-MUST-BE-BAKED (measured 2026-07-10 · DIRECTIONAL · numpy mirror · frozen bar unmoved)
- **wired:** none. $0 CPU numpy mirror ⇒ ceiling = DIRECTIONAL (`a_engine_native_learning`). Nothing on AKIDA (`a_lane_akida_gpu_split`).
- **source:** **H_9258** (`neuromorphic_recurrence_recomb`, registered this session, UNMEASURED) — this H is its **corrected successor**: it removes two confounds that make H_9258's step-1 proxy pre-determined, and re-aims the lever at the mechanism the session's own data leaves open.
- **lens:** reservoir computing / liquid-state machine (Jaeger, Maass) — fading-memory Volterra kernel as an **UNTRAINED** cross-product basis
- **artifacts:** `state/g1_temporal_binding_reservoir/`
- **xref:** **H_1638** (ESN transient-kernel mouth — 🔵 PRE-REGISTERED, cheap_test **NEVER FIRED**; this H is its anima-faithful rung) · H_1000/H_1003/H_1005/H_1008 (recurrent-WM toy ladder, already measured) · H_9206 (ATD crux — CE collapses bilinear→additive) · H_848 (AKD1000 op envelope = feedforward) · H_1603 (G1≡G6 binding deficit) · H_1840 (γ trained-constructive-bind, STEP-0 killed)
- **key:** `recurrent_basis_vs_retention`

## 0. Why H_9258's design cannot answer its own question

H_9258 proposes: toy task with **`GAP >= RF`**, train a **GRU** vs a matched **feedforward conv**, CRACK if the recurrent arm's swap-margin > 0 while the conv's ≈ 0.

Three defects, each fatal on its own:

1. **The comparison is rigged.** `GAP >= RF` means the conv's emit position has **zero mutual information** with D. The conv failing is a *theorem*, not a measurement. A recurrent arm beating it is the textbook result that motivated LSTMs.
2. **It moves two levers at once.** The GRU is **trained**; anima's trunk is **frozen**. A GRU win is attributable to *training the recurrence*, not to recurrence-as-architecture. The controlled variable is not isolated.
3. **It targets a bottleneck the session already ruled out.** H_9258's mechanism story is "hold D active across the gap." But the session measured a mean-pool linear probe recovering **D at 0.95 / R at 0.97** from the frozen conv hiddens. **D is retained.** Retention is not the wall.

Additionally, H_9258's step-1 result is **largely pre-determined by the existing ledger**: H_1000 already ran a width-matched numpy GRU vs a stateless baseline on exactly this shape and found **T1 "carry a stored symbol across a delay" = d 38.7, acc 1.000** (recurrence wins retention, decisively) while **T2 XOR-conjunction sat at chance** under direct training and cracked only under a curriculum (H_1003). Firing H_9258 as written would re-discover H_1000's T1.

## 1. The reframe

G1 decomposes into two claims. Only one is open.

| claim | status |
|---|---|
| **RETENTION** — D survives the gap and is present at readout | ✅ already true (0.95 pool probe; H_1000 T1 d=38.7). **NOT the bottleneck.** |
| **CONJUNCTION** — a bounded linear readout computes the non-additive D×R interaction | ❓ **open.** Every falsified lane (parametric-value 🧱, pointer-cache 🧱, xattn 🟡, xattn+InfoNCE 🟡) is a **routing/selection** operator. **None manufactured a multiplicative cross-product basis.** |

So recurrence is interesting **only if it supplies the cross-product basis** — not because it "holds D active." That distinction is the entire hypothesis, and the ρ=0 ablation below makes it directly falsifiable.

Convergence: `substrate-framebreak-g1-combination-operator` (the wall is a COMBINATION OPERATOR) · `gamma-divergence-instrument-arc` (additive floor = main-effect logit; the true product-code is **XOR**) · H_9206 (CE collapses a bilinear target back to additive).

## 2. Hypothesis (one falsifiable claim)

A **FIXED, UNTRAINED** recurrent reservoir driven by **frozen conv-trunk hiddens**, read by a **linear** head, solves distal recombination on **held-out (D,R) combinations** — because nonlinear temporal feedback manufactures the D⊗R Volterra cross-product basis for free — whereas the **same linear head** on the **same** frozen conv hiddens (emit-position *or* mean-pool) cannot, **at any retention level**.

⊥ **Null:** the reservoir also floors. Then the combination operator cannot be obtained **unbaked**; it must be **trained into the trunk** (γ, H_1840) — and recurrence, spiking, and neuromorphic substrates are all irrelevant to G1.

## 3. Task — a G1 analog with a PROVABLE additive floor

`[D] [filler × L=24] [R] → emit`, D,R ∈ {0..7}, **target = D XOR R** (3 bits). T = 26. Conv **RF = 31 ≥ T** (deliberately *de-rigged*, contra H_9258).

1. **XOR is provably unreachable by additive main effects.** With scores `s_v(d,r) = a_v(d) + b_v(r)` and V=2: `argmax_v = d⊕r` forces `α(d)+β(r) > 0 ⟺ d≠r`, giving `α0+β0 < 0`, `α1+β1 < 0`, `α0+β1 > 0`, `α1+β0 > 0`. The two pair-sums are the same quantity with opposite signs. Contradiction. **The additive floor is a theorem here**, not an empirical bar ⇒ additive-floor-immune by construction, like the session's swap-margin.
2. **Held-out combos are compositionally determined.** XOR is bit-decomposable: a model holding the pairwise products `{d_i·r_i}` generalizes to unseen cells; a lookup/memorizer does not. Train on 48/64 cells, test on the **16 unseen** cells.

Because RF ≥ T, the emit position **can** formally see D. Any conv failure is genuine attenuation/routing — **not** an information-theoretic rigging.

## 4. Arms — the trunk is the ONLY moved variable

Every arm feeds the **same** trained ridge readout over target bits (the "bounded linear readout" constraint). Shared frozen random embedding. **Nothing recurrent is ever trained.**

- **A1 `conv-emit`** — frozen random dilated causal conv (dil 1,2,4,8, tanh), hidden at emit. *(anima's emit point)*
- **A2 `conv-pool`** — same trunk, mean-pool. *(anima's 0.95 probe)*
- **A3 `esn-rho`** — frozen leaky ESN (M=300, α=0.9), state at emit, ρ ∈ {0.0, 0.3, 0.6, 0.9, 1.1}. *(H_1638's never-fired cheap_test)*
- **A4 `conv→esn`** — frozen conv hiddens **drive** the frozen ESN. *(the only arm wireable onto the frozen 303M — H_1638's gpu_recipe shape; a read-side DISJOINT lane per `a_substrate_disjoint`)*

**The load-bearing ablation.** At ρ=0 with leak α=0.9 the state is `h_t = 0.1·h_{t−1} + 0.9·tanh(x_t W_in)` — a decaying sum of **per-timestep** terms: **memory WITHOUT cross-products**. So `ρ=0` vs `ρ=0.9` isolates *products* from *retention*. This single comparison is what the H turns on, and it is the comparison H_9258 cannot make.

**Oracle calibrators** (bound what "solvable" means; no learning claim):
- `oracle-additive` = `[onehot(D); onehot(R)]` → must sit at chance (empirical check of the §3 theorem).
- `oracle-lookup` = `onehot(D) ⊗ onehot(R)` → fits train, must fail held-out (memorization detector).
- `oracle-bitprod` = `[D_bits, R_bits, D_bits·R_bits]` → must solve **and** generalize (the cross-product basis exists and suffices).

**Controls:** D-probe / R-probe per arm (retention measured *orthogonally* to binding) · label-shuffle (margin must collapse) · ridge λ chosen on a TRAIN-only inner split, never on test cells · fixed seeds.

## 5. Metrics

- **held-out 8-way accuracy** on the 16 unseen cells (chance 0.125) and per-bit (chance 0.5).
- **swap-margin** (the session's bar): `P(t(d,r) | d) − mean_{d'≠d} P(t(d,r) | d')`, fillers and R fixed, D counterfactually swapped. Additive readouts give ≈ 0 by the §3 theorem.
- **retention** = D-probe accuracy, reported separately from binding.

## 6. FROZEN outcome rules (fixed 2026-07-10 BEFORE measurement · no post-hoc movement · p7 / `a_break_the_wall`)

- 🟢 **CRACK — BASIS-NOT-RETENTION.** `esn-rho>=0.6` and/or `conv→esn` reach held-out 8-way ≫ 0.125 with swap-margin > 0, **while** ρ=0 collapses to chance **and** `conv-emit`/`conv-pool` sit at chance **despite** conv-pool's high D-probe. ⇒ The G1 wall is a **missing cross-product basis**, obtainable **UNTRAINED**. The 4 falsified read-side lanes lacked a multiplicative basis, not routing. Next rung = H_1638's gpu_recipe on the frozen 303M (engine-native). *This* — not "temporal binding" — is what a neuromorphic substrate would have to supply.
- 🧱 **KILL — CONJUNCTION-MUST-BE-BAKED.** Every reservoir arm floors on held-out **while** `oracle-bitprod` solves it. ⇒ Retention is free, products are not; an **unbaked** basis cannot be linearly decoded. The combination operator must be **trained into the trunk** (γ / H_1840). The frozen-readout terminal **hardens**, and recurrent + spiking + neuromorphic lanes are **ruled out for G1** — H_9258 answered in the negative, Akida confirmed a distraction.
- 🟡 **DIRECTIONAL** if ρ>0 lifts above ρ=0 but stays far below `oracle-bitprod` — a real but insufficient basis. Report the ρ-curve verbatim; no promotion.
- ⛔ **INVALID** if `oracle-additive` beats chance (task not additive-immune) or `oracle-bitprod` fails (task unlearnable) — re-design before ruling on any arm.

## 7. Akida scope (why the chip is NOT in this H)

`a_lane_akida_gpu_split` — this is Lane G/CPU. The chip is excluded on **ledger evidence**, not preference:

- **H_848** (silicon-verified): the AKD1000 byte-identical op envelope is `conv / FC / sepconv / maxpool / int4-quantizer` — **entirely feedforward**; even softmax / top-K argmax falls *outside* it. A "spiking net" on AKD1000 is a quantized feedforward CNN with spike encoding ⇒ **the same RF-decay class as the 303M conv trunk**. It cannot supply the variable under test.
- **H_910**: the recurrent LIF-ring result is a **SIM mirror**; live silicon was explicitly deferred (measure ⊥ deploy).
- **H_866**: on-chip edge-learn in a live dialogue loop = LOOP PASS / **GAIN FAIL 5/5**.

Any cross-gap recurrence on Pi5+AKD1000 must run as a **host-side CPU loop** re-injecting state per timestep — the reservoir is numpy on the Pi5 and the chip is a frozen feedforward feature extractor contributing **nothing** to the scientific question. Firing the chip for G1 is a **category error**; this $0 CPU probe strictly dominates it. Akida re-enters only *after* a 🟢 CRACK, and then as a **Lane-A body/energy embodiment** claim, never as a "does the wall exist" claim.

## 8. Honest scope (c9 · `a_toy_scale_recheck` · `a_scale_honest_scope`)

TOY: single gap L=24, K=M=8, one conv trunk, one reservoir width, numpy. **A crack here is DIRECTIONAL, never GREEN** — a numpy mirror cannot cement a tier (`a_engine_native_learning`); cementing requires an engine-native 303M re-measure via H_1638's gpu_recipe. The frozen bar above must not move after measurement (p7 · no tune-to-green). A KILL is a real result (`a_paper_negative_ok`) and is the **more useful** outcome: it retires an entire substrate class for $0. Not a forge binary. $0 CPU-local.

## 9. Related

[[substrate-framebreak-g1-combination-operator]] · [[gamma-divergence-instrument-arc]] · [[gamma-trunk-bake-step0-killed-not-unmeasured]] (γ trunk-bake is STEP-0 killed ⇒ an **untrained** basis is the one route to a combination operator that does **not** re-open a tune-to-green fire) · [[check-ledger-before-lever-fire]] · [[g1-topdown-routing-forkA]] (sibling read-side lane; this H is the *basis-expansion* class, fork-A the *pooling/routing* class)


## MEASUREMENT (2026-07-10 · $0 CPU numpy · seed 20260710 · frozen bar §6 unmoved)

Raw: `state/g1_temporal_binding_reservoir/verdicts/{h9259_run1,h9259_run2}.txt` · verdict: `.../VERDICT.md`.

Validity ⛔ gates PASS: oracle-additive held8=0.000 / bitacc 0.292 (additive floor real) · oracle-bitprod held8=1.000 (task learnable+generalizes) · oracle-lookup held8=0.125 (memorizer can't generalize).

| arm | held8 (chance .125) | Dprobe | swapM |
|---|---|---|---|
| conv-emit | 0.099 | 0.019 | +0.002 |
| conv-pool | 0.009 | 0.517 | −0.002 |
| esn-rho 0/.6/.9/1.1 | .015/.057/.062/.041 | 0.000 | ≈0 |
| conv→esn 0/.9 | .106/.051 | .015/.168 | — |
| **v2 retention-fixed** esn-pool/cat, esnfeat, convpool+esn | 0.001–0.015 | **1.000** | — |

**🧱 KILL — CONJUNCTION-MUST-BE-BAKED.** All reservoir arms floor on held-out while oracle-bitprod=1.000; the floor PERSISTS with retention forced to Dprobe=1.000 (v2), landing bit-acc at the additive floor (~0.29 = oracle-additive). ρ=0→0.9 gives no lift. An **untrained** Volterra basis + bounded linear readout cannot expose the D×R product; the combination operator must be **TRAINED into the trunk** (γ, H_1840). Falsifies H_1638's core bet. Converges with H_1000 (direct-trained GRU fails XOR) + H_1003 (curriculum-TRAINED GRU cracks it). Frozen-readout G1 terminal HARDENS; recurrent/spiking/**1st-gen AKD1000 (feedforward, H_848) ruled out as untrained G1 levers = distraction**. Akida re-enters only post-🟢 as a Lane-A body/energy claim (there was none).