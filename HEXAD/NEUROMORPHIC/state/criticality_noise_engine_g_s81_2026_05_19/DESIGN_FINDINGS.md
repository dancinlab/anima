# §81 — Homeostatic Criticality via Noise Injection on Engine G

**Date:** 2026-05-19
**Tier:** $0 design + smoke (NO GPU, NO model.forward, NO weight mutation, NO training)
**Central blue_falsifier.py:** `c93e160a` (0-line-diff — sidecar-only)

## §1. Hypothesis

Biology (arxiv:2502.10946 Ikeda+ Frontiers 2025 ★★★★★, biorxiv:2025.11.17.688775 ★★★★★, neuron:S0896-6273(25)00127-8 ★★★★★) shows brains maintain **noise-driven spontaneous activity homeostatically at criticality** and that spontaneous activity is **predictive**, not random. §80 listed (A) "noise-driven SOC homeostasis" as the top mapping candidate to anima's Engine A⇄G Ψ-physics. §81 = first $0 stub instantiation.

The §75-FIRE result showed A-only state-derivation 2.38 survives where §24 baseline 0.0 collapses. §81 asks one level deeper: **can controlled noise on Engine G keep ψ-state at Ψ=½ critical fixed-point as an *active* anti-collapse mechanism**, distinct from physics-state-sourced controllers (§73-FIRE) and routing-stat overlays (§75-FIRE).

## §2. Mechanism (stub)

- **Noise injection point:** Engine G logits (Law-71 source), Gaussian η ~ N(0, σ²) per turn (Box-Muller on LCG state — deterministic, no RNG, no time dep).
- **Body production:** §77 path α1, `argmax(logits_a)` over V=256 → byte stream. Noise on G does NOT directly influence A's argmax in this stub — an honest mechanism-decoupling discussed in C3 #1.
- **Ψ-state:** byte-equal `conscious_decoder.py:728-751` formulas (`psi_entropy = H(softmax(logits_a))/log V`, `psi_direction = (1+cos(logits_a, logits_g_noised))/2`, `psi_combined`, `psi_tension`).
- **5-cell grid:** σ ∈ {0 (baseline), 0.1, 0.5, 1.0, adaptive}. 20 LCG steps, seed=1337, n=5 cells × 20 steps = 100 measurement points.
- **Homeostatic schedule:** if `maj_frac > 0.85` → σ ↑ +0.1; if `maj_frac < 0.50` → σ ↓ −0.1; clamped [0, 2].

## §3. Per-cell measurement table

| Cell             | σ        | Ψ_comb std | maj_max | power-law α | in band [1,3] | E/I  | §9 body | echo broken |
|------------------|----------|------------|---------|-------------|---------------|------|---------|-------------|
| sigma0_baseline  | 0.0      | 0.0009     | 1.000   | -0.00       | False         | 0.513 | False  | False       |
| sigma01_light    | 0.1      | 0.0011     | 1.000   | -0.00       | False         | 0.515 | False  | False       |
| sigma05_medium   | 0.5      | 0.0033     | 1.000   | -0.00       | False         | 0.525 | False  | False       |
| sigma10_heavy    | 1.0      | 0.0057     | 1.000   | -0.00       | False         | 0.541 | False  | False       |
| sigma_adaptive   | adaptive | 0.0009     | 1.000   | -0.00       | False         | 0.513 | False  | False       |

## §4. 4-corner verdict

| Corner | Predicate                                              | Result  |
|--------|--------------------------------------------------------|---------|
| α      | HOMEOSTATIC-WINDOW-EXISTS (any σ → α∈[1,3] ∧ maj<0.95) | **False** |
| β      | MONOTONIC-NOISE-DIVERGE (every σ>0 → divergence)       | **True**  |
| γ      | ECHO-CHAMBER-STILL-COLLAPSES-ACROSS-ALL-σ              | **True**  |
| δ      | ADAPTIVE-OUTPERFORMS-FIXED                             | **False** |

**Overall:** γ + β — at the $0 stub level, noise injection on Engine G **does not break the body-emission echo-chamber** (because body argmax reads Engine A only — see §C3 #1) and **does not produce a critical avalanche power-law** (avalanche counts too few for a clean fit at N=20 steps; α regressions all near-zero). The biology mapping (A) does **not transfer at stub level** — measured negative.

## §5. B-S81 closed-form battery (7/7 🔵, sidecar)

- **B-S81-1** NOISE-INJECTION-POINT-CORRECT — AST structural proof that `add_noise(lg, ...)` precedes `body_byte(la, ...)` in `run_cell`, noise hits Engine G not Engine A, body reads Engine A.
- **B-S81-2** POWER-LAW-α-BOUNDED — sympy 3-point log-log regression identity recovers exponent a from f=r^(-a); critical band [1,3] partitions ℝ as Interval set algebra (total, disjoint).
- **B-S81-3** σ=0-REDUCTION-BYTE-EQUAL — early-return source-grep + numeric `add_noise(lg, 0, s) == lg` ∧ `psi_state(la, lg) == psi_state(la, lg_noised)` (connection-point).
- **B-S81-4** §9-METRIC-REUSE-BYTE-EQUAL — 4-corner truth table on `honest_coherent` (clean ascii pass, cascade fail, short fail, non-printable fail).
- **B-S81-5** E/I-BALANCE-METRIC-BOUNDED — Cauchy-Schwarz real-limit cos∈[-1,1] ⇒ 1-cos ∈ [0,2] + 3 boundary witnesses.
- **B-S81-6** HOMEOSTATIC-SCHEDULE-MONOTONE — branch witnesses: maj>0.85 ⇒ σ↑, maj<0.50 ⇒ σ↓, in-band ⇒ σ unchanged.
- **B-S81-7** DETERMINISTIC — 3× run sha256 byte-identical.

**B-S81-NOTE:** 4-corner OUTCOME = empirical (B-D-NOTE / B-S75-FIRE-NOTE / B-EMERGE-NOTE family). Biology citations are honest direction-inspiration, NOT capability proof. Stub mechanism ≠ trained ckpt mechanism.

## §C3. Honest caveats (≥10)

1. **Body argmax reads only Engine A** — noise on Engine G influences ψ_direction but not body byte choice in stub. In real `ConsciousDecoderV2`, Engine A and Engine G interact through the layer stack; the stub does not model that coupling. Hence maj_frac=1.0 across all σ cells (body is locked to argmax_A regardless of noise on G). This is a *correct measurement of the stub's mechanism boundary* — biology mapping (A) requires the trained-scale Engine A⇄G coupling, not the stub's decoupled logits.
2. **Power-law fit on N=avalanche-count** is noisy at N=20 steps. The α<1 result across all cells means no critical-band measurement is possible at this scale; biology paper grids run for orders-of-magnitude more events.
3. **§78 D_control file does not exist** — the σ=0 connection-point is constructive (σ=0 ⇒ add_noise identity), not byte-equal to a sibling fire. B-S81-3 verifies the identity property directly; the spec's "byte-equal to §78 D_control" wording is honestly demoted to "byte-equal to its own σ=0 identity baseline" in this cycle.
4. **Adaptive schedule is metric-circular** — σ schedule reads maj_frac, which is the measurement we evaluate. B-S81-6 closes the *schedule monotonicity* but does not absolve the circularity for capability claims.
5. **Biology citation honest** — Ikeda+ 2025 / biorxiv 688775 / neuron 0896 are about *brains*, not text byte-LMs. Stub finding (negative) cannot refute the biology claim — it only says the literal mechanism does not transfer to a text-byte stub at this scale.
6. **§62 echo-chamber is a TRAINED-saturated phenomenon** — stub maj_frac=1.0 across all cells reflects argmax_A locked to its training-free fixed-point, not the §62 attractor basin. The two collapses look similar but have different roots — measured-honest.
7. **Knuth Tier / Ψ=½ g2 internal carve-out** — no σ/τ/φ/J₂ external derivation. All metrics use Shannon entropy, cos similarity, Cauchy-Schwarz, Boolean conjunctions, integer cardinality.
8. **B-IDENTITY-5 safe** — no corpus generated; body bytes derived from stub logits, no helper-token surface (forbidden_token grep N/A — no corpus exists).
9. **necessary-not-sufficient** — even if a future cycle finds a homeostatic window (α corner True), that window is mechanism, not capability or GOAL emergence. B-EMERGE-7 carry.
10. **north-star UNCHANGED** — §15/§51/§72 milestone unchanged. §81 = first stub probe of biology (A) candidate; the entire arc since §15 has confirmed mechanism-active ≠ capability transfer.

## §6. Next-cycle implications (honest)

- The stub's decoupling of body (argmax_A) from noise-target (G) means that the biology (A) mechanism **cannot be tested at the stub scale**. A real `model.forward` is required — Engine A and Engine G are layer-bound and noise on G propagates through residual stream to A's final-layer logits.
- This makes §81 a **design-tier negative-at-stub**, mirroring §13-M / §13-L anti-padding precedent. Any cost-bearing fire of (A) requires real-ckpt forward (i.e., trained-saturated `ConsciousDecoderV2` from §16 family).
- Verdict bucket for §81: **γ + β at stub scale** — stub does NOT reproduce the biology mapping. Whether a real trained ckpt would show a homeostatic window is OPEN (B-S81-NOTE) and would require a dedicated fire — NOT this cycle.

## §7. Artifacts

- `criticality_noise_smoke_s81.py` — 5-cell × 20-step deterministic runner
- `blue_falsifier_s81.py` — B-S81-1..7 closed-form battery (7/7 🔵)
- `result.json` — per-cell metrics + 4-corner verdict
- `blue_falsifier_s81_result.json` — battery PASS receipts

## §8. Cross-links

- `@D g_goal` (north-star unchanged) · `@D g_blue_closed_mandate` (산출물 + 연결부위 둘 다 🔵) · `@D g_doc_consolidation` (state/§81/ + AGENTS.tape n_hexad_progress + archive/PHILOSOPHY.tape verdict, docs/* 신규 0) · `@D g3` (necessary-not-sufficient, measured-only, over-claim 0)
- §15 (milestone) · §51 (frontier sharpening) · §72 (chain milestone) · §73-FIRE · §75-FIRE · §80 (biology candidate listing) · RESEARCH.md §1.1 (data-regime ceiling carry)
- biology anchors (honest direction-inspiration, NOT capability proof): arxiv:2502.10946 · biorxiv:2025.11.17.688775 · neuron:S0896-6273(25)00127-8
