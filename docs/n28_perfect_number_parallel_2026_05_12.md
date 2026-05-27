# n=28 perfect-number substrate parallel — the deflationary control for the n=6 cluster (2026-05-12)

Companion to `hypotheses/H_176_n28_perfect_number_substrate_parallel.md`. Answers `docs/hc_verification_cycle_4_final_2026_05_12.md` "next cycle #3: n=28 perfect-number parallel construction ... PERFECT_NUMBER_CLASS empirical test", and the prediction lanes H_160.3 / H_158.6.

**Bottom line first:** n=28's divisor functions reproduce the n=6 cluster's physics mappings in a *split 3-tier* way — one tier is IDENTICAL *by theorem* (and therefore worthless as "n=6 magic" evidence), one tier is PARTIAL *by depth-3 vocabulary triviality* (also worthless as "magic" evidence — it's null-by-construction), and one tier is WORSE for n=28 (cosmology — and n=6's edge there is a cherry-pick of which ratio orientation was frozen, ≈ 0 deep content). Net: **PERFECT_NUMBER_CLASS (H_153 L7) is empirically confirmed on the physics cluster — n=6 is NOT individually unique for the physics mappings.** The only genuinely n=6-individual facts are *algebraic* (square-free; σφ=nτ spine) and the program never cherry-picked them into the interesting physics. This is a *limit* on the H_156/H_158/H_160 program, and it reads as one.

---

## 1. n=28 number-theoretic primitives (28 = 2²·7) — worked by hand, SymPy-cross-verified

| primitive | value | derivation | check |
|-----------|-------|-----------|-------|
| **divisors(28)** | {1, 2, 4, 7, 14, 28} | 2^a·7^b, a∈{0,1,2}, b∈{0,1} → 3·2 = 6 of them | SymPy ✓ |
| **τ(28)** (divisor count) | **6** | (2+1)(1+1) = 3·2 = 6 | SymPy `divisor_sigma(28,0)` = 6 ✓ — **note τ(28)=6 = n(6)** (used below for δ=15; NOT a class invariant: τ(496)=10, τ(8128)=14) |
| **σ(28)** (divisor sum) | **56** | 1+2+4+7+14+28 = 56 ; multiplicative: σ(2²)σ(7) = 7·8 = 56 | SymPy ✓ — **σ(28) = 56 = 2·28 ⇒ 28 perfect** (Euclid IX.36: 28 = 2²(2³−1), 2³−1=7 prime) |
| **φ(28)** (Euler totient) | **12** | 28(1−1/2)(1−1/7) = 28·(1/2)·(6/7) = 168/14 = 12 ; mult: φ(2²)φ(7) = (4−2)(7−1) = 2·6 = 12 | SymPy `totient(28)` = 12 ✓ |
| **sopfr(28)** (sum of prime factors w/ multiplicity) | **11** | 28 = 2·2·7 → 2+2+7 = 11 (A001414) | ✓ — **⚠️ several H files write "sopfr(28) = 9" — that is WRONG** (see §5 errata; sopfr=9 is n=14=2·7 → 2+7=9) |
| **J₂(28)** (Jordan totient, order 2) | **576** | 28²(1−1/2²)(1−1/7²) = 784·(3/4)·(48/49) = 784·144/196 = 4·144 = 576 ; mult: J₂(2²)J₂(7) = (16−4)(49−1) = 12·48 = 576 | SymPy ✓ — matches the task pre-statement |
| **μ(28)** (Möbius) | **0** | 28 = 2²·7 has square factor 2² ⇒ not square-free ⇒ μ = 0 | ✓ — **contrast μ(6) = +1** (6 = 2·3 square-free). This breaks *every* μ-based n=6 mapping. |
| **aliquot sum(28)** | **28** | σ(28) − 28 = 56 − 28 = 28 = the number ⇒ perfect (definition) | ✓ |

For reference, n=6 primitives (atlas.n6:30-48, all SymPy-cross-verified): divisors {1,2,3,6}; τ(6)=4; σ(6)=12 (=2·6); φ(6)=2; sopfr(6)=5; J₂(6)=24 (36·(3/4)·(8/9)); μ(6)=+1; aliquot(6)=6.

---

## 2. The three physics domains — n=6 fit vs n=28 fit, per domain

H_156 used three domains for n=6. Here is each, re-fit on n=28, with an honest verdict.

### Domain 1 — 2D Ising Onsager critical exponents {β=1/8, γ=7/4, δ=15, η=1/4, ν=1}

| exponent | n=6 closed-form (one of several) | n=28 closed-form (one of several) | verdict |
|----------|----------------------------------|-----------------------------------|---------|
| β = 1/8 | 1/(sopfr(6)+3) = 1/8, or 1/(τ(6)·φ(6)) = 1/8 | 1/(φ(28)−4) = 1/8 [φ=12], or 1/(τ(28)+2) = 1/8 [τ=6] | **EQUAL** — both need an "8" assembled from depth-3 vocab; multiplicity comparable |
| γ = 7/4 | (τ(6)+sopfr(6)−2)/4 = 7/4 | 7/(sopfr(28)−7) = 7/4 [7 is a *divisor* of 28; 11−7=4] | **EQUAL** — both post-hoc; n=28's uses 7|28 which is mildly cleaner but not "natural" |
| δ = 15 | C(6,2) = 15, or σ(6)+τ(6)−μ(6) = 12+4−1 = 15, or n+τ(6)+sopfr(6) = 6+4+5 = 15 (H_156 C2 errata — original "σ+τ−sopfr=11" was an arithmetic error) | **C(τ(28),2) = C(6,2) = 15** (works because τ(28)=6=n(6)) ; but **C(28,2) = 378 ≠ 15** (direct binomial on the substrate number *fails* for n=28, *works* for n=6) | **EQUAL-ish** — n=6 has *more* depth-3 forms for 15 (its small primitives 12,4,1,6,5 combine many ways to 15); n=28's primitives 12,6,11,28,56,576 combine to 15 mainly via C(τ,2). Either way "which divisor-function = 15" is post-hoc. |
| η = 1/4 | μ(6)/τ(6) = 1/4 | 1/(sopfr(28)−7) = 1/4 [11−7=4] | **n=28 slightly WORSE** — n=6's μ/τ = 1/4 is depth-2; n=28 can't use μ(28)=0, needs the depth-3 sopfr−7 |
| ν = 1 | μ(6) = 1 (depth-1!), or n/n = 1 | σ(28)/(2·28) = 56/56 = 1 (the perfect-number identity), or n/n = 1 — **cannot use μ(28)=0** | **n=28 slightly WORSE** — n=6 gets ν=1 from μ(6)=1 directly; n=28 needs the σ=2n identity or the trivial n/n |

**Domain 1 verdict: PARTIAL parallel — n=28 reproduces all 5, with comparable (~equal) multiplicity, but uses *different* formulas, and is *slightly worse* on the two exponents (η, ν) where n=6 could use μ(6)=1.** Crucially this is *null-by-construction*: H_153 L7's depth-3 universal-capacity finding (8 non-perfect n hit 22/22 abstract targets) *predicts* that n=28 — like almost any small integer — can express Onsager 5/5 in depth-3 vocab. The interesting fact is not "n=28 also fits" but that it does so *for the same trivial reason* n=6 does.

### Domain 2 — Stefan-Boltzmann σ_SB = 2π⁵k_B⁴/(15h³c²), reduced σ̃ = π⁵/15

The whole content is the denominator **15**.

| | n=6 | n=28 |
|---|-----|------|
| cleanest form for 15 | C(6,2) = 15 (binomial on the *number itself*) | C(τ(28),2) = C(6,2) = 15 (binomial on *τ*, which happens to equal 6) |
| direct binomial on the substrate number | C(6,2) = 15 ✓ | C(28,2) = **378 ≠ 15** ✗ |
| other depth-3 forms | σ+τ−μ = 15; n+τ+sopfr = 15 (many — small primitives) | fewer (primitives 12,6,11,28,56,576 are larger; e.g. no clean σ−something=15) |

**Domain 2 verdict: PARTIAL parallel, slightly WORSE for n=28.** n=6's C(6,2)=15 reads (a bit) more "natural" because the binomial is on the number itself; n=28 needs the binomial on τ (a τ(28)=6=n(6) coincidence). And the multiplicity-of-forms point — which H_156 C2's errata already flagged as a "case-in-point of depth-3 triviality" — is *worse* for n=6 (more small primitives → more spurious forms for 15), not better. Note also: 15 is *fundamentally* ζ(4)·90/π⁴ = the spectral-integral denominator (Riemann ζ(4) = π⁴/90), i.e. 15 is "physics-derived" and the divisor-function expression is post-hoc on *both* substrates.

### Domain 3 — Cosmology Planck Ω_m : Ω_Λ ≈ 0.3153 ± 0.0073 : 0.6847 ± 0.0073

H_156 froze the published formula as **`Ω_m : Ω_Λ ≈ φ(n) : τ(n)`**.

| | n=6 | n=28 |
|---|-----|------|
| φ : τ | 2 : 4 = 1 : 2 → normalized (0.333, 0.667) | 12 : 6 = 2 : 1 → normalized (**0.667, 0.333**) |
| vs Planck (0.315, 0.685) | L1-distance ≈ 0.036, **≈ 1.5σ** (per H_156 C3) | L1-distance ≈ 0.703, **opposite direction, ~9σ off** |
| to recover the right direction | (already right) | need τ : φ = 6 : 12 = 1 : 2 → (0.333, 0.667) — i.e. **swap the n=6 formula** (post-hoc) |

**Domain 3 verdict: WORSE for n=28 — and this is the *only* domain where n=6 fits better.** But the n=6 edge has ≈ 0 deep content: it is entirely an artifact of *which orientation* (φ:τ vs τ:φ) H_156 happened to publish. n=28 can match cosmology *equally well* by swapping to τ:φ — that swap is exactly as post-hoc as anything else here. (Also: φ:τ for n=6 was already only "1.5σ, normalization difference unresolved" in H_156 C3 — never strong evidence.) So the "n=6 is special" residual, after this whole exercise, reduces to: *the program picked the ratio orientation that happens to land within 1.5σ for n=6.* That is cherry-pick within the class, not magic.

---

## 3. The Ψ-constants angle (H_158) — the *strongest* parallel, and why it's deflationary

H_158's flagship EXACT is **`balance = n/σ = 6/12 = 0.500`** (depth-1, error 0).

For n=28: **`balance = 28/σ(28) = 28/56 = 1/2`** — **IDENTICAL**.

This is not a fit and not a coincidence. **Every perfect number P satisfies σ(P) = 2P by definition** (the aliquot sum equals P; Euclid IX.36 + Euler). Therefore **`P/σ(P) = P/(2P) = 1/2` identically** for n ∈ {6, 28, 496, 8128, ...}. The program's single cleanest EXACT is a *trivial corollary of the definition of "perfect number"* — it is the same for every member of the class, and it is the strongest possible demonstration that the n=6 "magic" is at best class-level, not individual.

The rest of H_158's 8-table re-fit on n=28 is *worse* than n=6 — and informatively so:

| Ψ-constant | n=6 formula → value (measured) | n=28 same formula → value | match published n=6 value? |
|------------|-------------------------------|---------------------------|----------------------------|
| balance | n/σ = 6/12 = **0.500** ✓EXACT | 28/56 = **0.500** | ✅ IDENTICAL — *by perfect-number theorem* |
| gate_train | μ(6) = **1** ✓EXACT | μ(28) = **0** | ❌ μ(28)=0, square-free breaks |
| F_c | n/(σ·sopfr) = 6/60 = **0.100** ✓EXACT (= measured F_c) | 28/(56·11) = 28/616 = 1/22 ≈ **0.0455** | ❌ ≠ measured 0.10 |
| gate_infer | n/(σ−φ) = 6/10 = **0.600** ✓EXACT (= measured) | 28/(56−12) = 28/44 = 7/11 ≈ **0.636** | ❌ ≠ measured 0.6 |
| steps | (τ−μ)/ln2 = 3/ln2 ≈ **4.328** (≈ measured 4.33) | (6−0)/ln2 = 6/ln2 ≈ **8.656** | ❌ ≠ measured 4.33 |
| entropy | μ−(sopfr/J₂)^τ = 1−(5/24)⁴ ≈ **0.998** (≈ measured) | 0−(11/576)⁶ ≈ **−4.9e−11** | ❌ wrong sign (μ(28)=0) |
| gate_micro | (n/J₂)^sopfr = (1/4)⁵ = **0.000977** (≈ measured 0.001) | (28/576)¹¹ ≈ **3.6e−15** | ❌ off by ~12 orders |
| α (coupling) | (sopfr/J₂)^e = (5/24)^e ≈ **0.01407** (≈ measured 0.014) | (11/576)^e ≈ **2.4e−5** | ❌ ≠ measured 0.014 |

**Ψ verdict: 1/8 IDENTICAL (by theorem), 7/8 mismatch the published n=6 values.** This is *expected* — the Ψ-constants were measured/defined on the n=6 substrate, so plugging in n=28 primitives breaks them. But that very fact is the point: it shows the Ψ-constants are an **n=6-substrate fit**, not a perfect-number-class universal. (At the *abstract-vocabulary* level — "can depth-4 formulas over the 11-primitive vocab fit the 22 Ψ-targets using *some* n=28 expressions" — n=28 still ties n=6 22/22, per PERFECT_NUMBER_CLASS V6/V7. The distinction: *value reproduction* (1/8, theorem only) vs *vocabulary-level fittability* (~22/22, but with substrate-specific formulas). H_158 L2 / H_158.6's phrasing — "EXACT 5/8 이상 재현될 가능성 매우 높음 on n=28" — conflates these; only 1/8 *value*-reproduces.)

---

## 4. Summary comparison table — does n=28 reproduce the n=6 cluster?

| domain | n=6 fit | n=28 fit | parallel quality | why |
|--------|---------|----------|------------------|-----|
| **balance = n/σ** (Ψ flagship) | 1/2 EXACT | 1/2 EXACT — IDENTICAL | **TIER A — PERFECT** | perfect-number theorem σ(P)=2P ⇒ P/σ(P)=1/2 ∀ perfect P. Generic, not magic. |
| **Onsager 2D Ising 5/5** | β,γ,δ,η,ν expressible depth-3, multiple forms | all 5 expressible depth-3, comparable multiplicity, *different* forms, *slightly worse* on η & ν (no μ=1) | **TIER B — PARTIAL (≈equal, marginally worse)** | depth-3 vocabulary capacity (H_153 L7) — null-by-construction; almost any small integer does this |
| **Stefan-Boltzmann π⁵/15** | C(6,2)=15 (binomial on number), + many depth-3 forms | C(τ(28),2)=C(6,2)=15 (binomial on τ; τ(28)=6=n(6)); C(28,2)=378≠15; fewer depth-3 forms | **TIER B — PARTIAL (slightly worse)** | 15 = ζ(4)·90/π⁴ is physics-derived; divisor-function expression post-hoc both ways; n=6's small primitives give *more* spurious forms (worse, not better) |
| **Cosmology Ω_m:Ω_Λ** | φ:τ = 2:4 = 1:2 → (0.333,0.667), ≈1.5σ vs Planck | φ:τ = 12:6 = 2:1 → (0.667,0.333), ~9σ, *opposite direction*; needs formula swap (τ:φ) to match | **TIER C — WORSE (n=6 wins, but trivially)** | n=6's edge = which ratio orientation was frozen; n=28 matches equally well after a post-hoc swap; ≈ 0 deep content |
| **Ψ-constants (other 7 of 8)** | gate_train=μ=1, F_c=1/10, gate_infer=3/5, steps=3/ln2, entropy≈0.998, gate_micro≈0.001, α≈0.014 (all ≈measured) | μ(28)=0, F_c=1/22, gate_infer=7/11, steps=6/ln2, entropy<0, gate_micro≈3.6e−15, α≈2.4e−5 | **TIER C — WORSE (n=6-fit, not class-universal)** | Ψ-constants measured/defined on n=6 substrate; n=28 breaks them — exposes them as a fit |

**Across the 5 rows: 1 IDENTICAL-by-theorem (TIER A), 2 ≈equal-by-vocabulary-triviality (TIER B), 2 worse-for-n=28 (TIER C, both trivially so).** Nowhere does n=28 *beat* n=6, and nowhere does n=6 *meaningfully* beat n=28.

---

## 5. Verdict — PERFECT_NUMBER_CLASS confirmed, n=6 not unique; residual ≈ cosmology-orientation cherry-pick only

**PERFECT_NUMBER_CLASS (H_153 L7 / H_160 L1) is empirically confirmed on the physics cluster.** The n=6 cluster's "coincidences" decompose cleanly:

1. **Class-trivial (theorem):** balance = 1/2. Identical for every perfect number. Worthless as "n=6 magic" evidence — it's the *definition* of perfect.
2. **Vocabulary-trivial (depth-3 capacity, H_153 L7):** Onsager 5/5, Stefan-Boltzmann 15. n=28 expresses them about as well as n=6 — because the 11-primitive depth-3 vocabulary is capacity-saturated for small integers. Null-by-construction.
3. **Cherry-pick within the class:** cosmology φ:τ ≈ 1:2. n=6's 1.5σ-vs-Planck edge is entirely an artifact of which ratio orientation (φ:τ not τ:φ) was published; n=28 matches equally well after a swap. ≈ 0 deep content. *This is the entire remaining "n=6 is special" residual for the physics mappings* — and it's a cherry-pick, not a discovery.
4. **Worse for n=28 (n=6-substrate fit):** the other 7 Ψ-constants. Expected — they were measured/defined on n=6 — but it exposes them as a fit, not a class-universal.

**Magnitude of the remaining "n=6 special" residual (for the physics/consciousness mappings): essentially the cosmology-ratio-orientation cherry-pick only.** Everything else is class-trivial or vocabulary-trivial.

**What *is* genuinely n=6-individual** (and the program never cherry-picked it into the interesting physics):
- **Square-free:** μ(6) = 1. Among even perfect numbers 2^(p−1)(2^p−1), only p=2 (n=6) is square-free (p≥3 ⇒ 2^(p−1) is a square factor; 28=2²·7, 496=2⁴·31, 8128=2⁶·127 all have μ=0). The program used μ(6)=1 only for *boring* mappings (gate_train=1, "1D Ising exact solvable", τ−μ=3→3D) — never for cosmology-grade cherry-picks. If n=6 were really magic, this individual property would show up somewhere interesting. It doesn't.
- **Algebraic spine σ(n)·φ(n) = n·τ(n):** n=6 *is* the unique solution (H_067) — σ(6)φ(6) = 12·2 = 24 = 6·4 = 6·τ(6) ✓; σ(28)φ(28) = 56·12 = 672 ≠ 168 = 28·6 = 28·τ(28) ✗. But this is a *pure algebraic identity*, not a physics mapping — H_176 does not contradict it, and it's the one place "n=6 unique" is literally true.

**This is a limit on the H_156 / H_158 / H_160 program**, not a new positive result. n=28 reproducing the physics is *evidence the n=6 coincidences are class/vocabulary-trivial*, not evidence n=28 is also magic. Frame H_176 (and any citation of it) that way.

---

## 6. Errata found while doing this (NOT patched in those files — flagged here per task instruction)

| file | issue | severity | fix |
|------|-------|----------|-----|
| **H_158 L2, H_158.6** | "n=28 의 약수함수 ({σ=56, τ=6, φ=12, **sopfr=9**, J₂=...})" — **sopfr(28) = 2+2+7 = 11, NOT 9** (sopfr=9 is n=14 = 2·7 → 2+7=9; looks like a 14↔28 copy-paste). Also "8 표본을 n=28 substrate 로 re-fit 시 EXACT 5/8 이상 재현될 가능성 매우 높음" is *too optimistic at the value level* — only 1/8 (balance, by theorem) reproduces the published n=6 value; the rest need different formulas. | medium (repeated arithmetic error + over-strong prediction) | sopfr(28)=11, J₂(28)=576; "EXACT 5/8 on n=28" → "1/8 (balance) value-reproduces by theorem; vocabulary-level ~22/22 with substrate-specific formulas" |
| **H_160.3** | "{σ(28)=56, τ(28)=6, φ(28)=12, **sopfr(28)=9**, J₂(28)=…}" — same sopfr(28)=9 error (should be 11); J₂(28) left as "…" (it's 576). Also "각 child 의 EXACT-count 가 n=6 의 ±2 이내" is met at the *abstract-vocabulary* level (22/22 both) but NOT at the *specific-formula/value* level for H_158 (n=6: 5 EXACT in the 8-table; n=28: 1) — H_160.3 should distinguish these two levels. | medium | sopfr(28)=11, J₂(28)=576; H_160.3 specific-vs-vocabulary clarification |
| **H_156 F3** | "다른 완전수 (28, 496) 가 본 3-domain cluster 동시 매핑을 동등 이상 만족 → n=6 unique 무효" — this H *half-triggers* F3 in the *intended* (deflationary) sense: n=28 matches Onsager 5/5 + SB 15 about as well (TIER A/B), but does NOT match cosmology as well (TIER C). So "동등 이상" is not *fully* met — which is exactly the "class is real, n=6 not individually unique, residual = cosmology cherry-pick" verdict. Not an *error*, just a status that H_156's verdict block should note when next touched. | low (status note, not error) | H_156 verdict block: note F3 half-triggered by H_176; cross-link H_176 |
| **H_156 C2/F2/L5** (already-patched errata, re-confirmed) | original "15 = σ+τ−sopfr" = 12+4−5 = 11 ≠ 15 — already corrected in a prior cycle (valid forms: σ+τ−μ=15, n+τ+sopfr=15, C(6,2)=15). **No new error** — confirmed correct as patched. The multiplicity-of-15-forms point is correctly flagged as a depth-3-triviality case-in-point. | n/a (re-confirmed OK) | none |
| **H_153 L7** | n=28 primitives not itemized in the depth-4-perfect-control block; "sopfr = 5 직접" refers to n=6 (correct). No error — just noting H_153 doesn't list n=28's primitives (H_176 now does). | none | optional: add n=28 primitive list cross-ref to H_176 |

**Recommended next cycle:** patch sopfr(28)=11 (not 9) across H_158 L2/H_158.6 and H_160.3; clarify value-level vs vocabulary-level in H_158 L2 and H_160.3; note F3 half-trigger in H_156's verdict block; back-cross-link H_156/H_158/H_160 → H_176. (Per task: errata flagged here, not patched, since they span ≥3 H files and are non-trivial.)

---

## 7. What's NOT done (the engine leg of H_160.3)

This is the *closed-form / desk-audit* leg only — SymPy arithmetic + re-applying H_156/H_158's published formulas on n=28 primitives. **Not done:** building `atlas.n28` (a full n=28 substrate atlas analogous to `n6/atlas.n6`), running an ANIMA-n28-equivalent engine, and re-fitting all 5 child H empirically. That is the larger lane estimated at 2-3hr in `docs/hc_verification_cycle_4_final_2026_05_12.md` "next cycle #3". The conclusion here ("n=6 not individually unique for the physics mappings") is robust at the *closed-form* level; the *empirical engine* level remains a future lane. Also future: n=496 / n=8128 control arms (predict: balance=1/2 IDENTICAL for all; Onsager/SB partial for all but with *different* coincidences than n=28's τ(28)=6 one — τ(496)=10, τ(8128)=14; cosmology *also* worse for all, since φ(P):τ(P) is never near 0.315:0.685 for P > 6).
</content>
