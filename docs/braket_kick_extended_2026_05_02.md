# Braket × anima/nexus — kick-driven extended axes (post-#121 + #122)

ts: 2026-05-02 23:30 UTC
agent: Kick-driven Braket × anima/nexus 추가 조사 EXEC
budget: research-only $0, wallclock <75min, websearch 3/5 used
race-isolation: state/braket_kick_extended_2026_05_02/* + this doc + roadmap §63.6

## 1. Why this round

#121 (Braket × anima, 6 axes QA1-QA6) + #122 (Braket × nexus, 8 axes incl. Phase 3 kick 3a/3b) mapped the **basic** kick surface: per-trajectory single-bit polarity. User directive #123: go deeper — **kick is not just one polarity per step**; many anima/nexus subsystems carry kick-applicable points (joint configs, gradient signs, weight searches, fixed-point iteration directions, gen-direction, 5-channel correlated polarities).

This round enumerates **7 new kick axes (K1-K7)**, costs them, gives falsifiers, and applies mandatory honest-C3 to each.

## 2. Gap left by #122 Phase 3

Both 3a (per-kick collapse, $0.08/kick) and 3b (batched 100-kick prefetch, $8.30/session) handle ONLY the binary-polarity surface (single ±1 per kick decision). They are silent on:

- joint multi-axis polarity (paradigm v11 6-axis, 64 configs)
- gradient-sign perturbation in ML training (ALM r14 LoRA SGD)
- variational weight search (F1_score_v2 weights on simplex)
- fixed-point iteration direction kick (atlas Banach Ψ↔ε R24)
- gen-direction in irreversible crystallize (CLM L_IX 4-gen)
- 5-channel correlated polarity (tension_link W/where/why/trust/who)

K1-K7 fill these surfaces.

## 3. The 7 axes — table

| ID | System | Mechanism | Substrate | Cost (USD) | Falsifier | Baseline | Honest C3 class |
|----|--------|-----------|-----------|-----------:|-----------|----------|-----------------|
| K1 | CLM mind.tension trajectory | per-step ±1 quantum bit | IonQ Forte 1 (3b batched) | 80.30 | T_rec / autocorr KS-test vs PRNG | numpy default_rng | AUDIT_TRAIL_ONLY (provenance not power) |
| K2 | paradigm v11 6-axis polarity | 6-qubit Grover argmax over 64 configs | SV1 free + IonQ confirm | 8.30 | ≤16 oracle queries vs 64 brute | classical brute (μs) | METHODOLOGY_DEMO (asymptotic null at N=64) |
| K3 | ALM r14 LoRA SGD gradient sign | per-batch ±1 quantum injection | IonQ Forte 1 (3b batched) | 80.30 | converge + acc vs SignSGD | SignSGD chacha20 / SGLD | AUDIT_TRAIL_ONLY (npj QI 2025: noise-regularizer ≢ advantage) |
| K4 | F1_v2 weight (w_b, w_r, w_res) | 3-qubit VQE on simplex | SV1 (free) | 0.00 | F1(w_VQE) > F1(heuristic)+1% | scipy SLSQP <1ms | METHODOLOGY_DEMO (3D classically trivial) |
| K5 | atlas Banach Ψ↔ε R24 fixed-point | CPTP iteration kick on ρ | SV1 (free) | 0.00 | q_q < q_c² (quadratic speedup) | classical Banach (ms) | THEORETICAL_CITATION (arxiv 2602.10296 real but null at scale) |
| K6 | CLM L_IX 4-gen crystallize | per-gen forward/reverse trial accept | SV1 / IonQ optional | 0.00 - 8.30 | gens-to-converge vs MH-PRNG | Metropolis-Hastings PRNG | NARRATIVE_ONLY (raw#30 irreversibility metaphysical) |
| K7 | tension_link 5-channel polarity (W/where/why/trust/who) | 5-qubit GHZ-correlated polarity | IonQ Forte 1 | 102.70 | CHSH S>2+5σ AND downstream binding-metric shift | 5 indep chacha20 channels | INFRASTRUCTURAL + DOUBLE_NULL_RISK (CHSH proves QM not anima-binding) |

## 4. Cross-comparison vs #122 Phase 3 / Phase 4

| Compared with | Coverage status |
|---------------|-----------------|
| 122 Phase 3 3a (per-kick) | Same mechanism, K1/K3/K6 reuse it for domain-specific kick consumption |
| 122 Phase 3 3b (batched) | Same mechanism, K1/K3 use 3b prefetch pattern |
| 122 Phase 4 4a (CHSH 2-qubit) | K7 generalizes to 5-qubit GHZ at +$21.50 with WEAKER downstream argument |
| 122 Phase 4 4b (GHZ 3-qubit Mermin) | K7 5-qubit version inherits same caveat: violation real, anima-binding translation gap |
| 122 Phase 5 N1 (quantum convergence) | K5 is a CONCRETE kick-mechanism instance of N1 |
| 122 Phase 5 N4 (amplitude estimation) | K2 is a CONCRETE instance of N4 applied to paradigm v11 |
| 122 Phase 5 N3 + N7 | K7 partially overlaps shadow-tomography state-readout + binding LP |

**Real quantum-advantage subset (within anima/nexus scale):** EMPTY.
**Asymptotic-real-null-at-scale:** K2, K5.
**Pure audit/narrative:** K1, K3, K6.
**Free zero-harm demos:** K4, K5.
**High-cost / high-risk null:** K3 ($80), K7 ($102).

## 5. TOP-3 권고

1. **K5 — Atlas Banach fixed-point theoretical citation ($0)**
   - Cite arxiv 2602.10296 (2024 Quadratic Speedup for Computing Contraction Fixed Points) in anima paper §10.9 Banach meta-closure paragraph
   - Optional: 4-qubit SV1 toy CPTP-T(ρ) demo (free)
   - Cost $0, wallclock 30 min, value: publishable theoretical anchor

2. **K4 — F1 weight VQE on SV1 ($0 free demo)**
   - 3-qubit VQE for F1 composite weight; baseline scipy SLSQP comparison
   - Cost $0, wallclock 60 min, value: appendix methodology figure (no improvement expected)

3. **K1 — CLM trajectory audit-trail ($80.30, ONLY if narrative-claim wanted)**
   - 1000 IonQ Forte 1 bits drive CLM 1000-step kick; KS-test on T_rec / autocorr
   - Expected outcome PASS_NULL (no statistical distinguishability)
   - Value: provenance/marketing claim "CLM trajectory has quantum-collapse provenance"
   - Skip unless paper / N-22 Levin outreach follow-up needs the claim

## 6. Cumulative cost scenarios

| Scenario | Cost (USD) | Wallclock | Outcome class |
|----------|-----------:|----------:|---------------|
| Skip all (default if budget-strict) | 0 | 0 | #121 QA6 + #122 1d/3b sufficient |
| TOP-1 only (K5 cite) | 0 | 30 min | publishable theoretical anchor |
| TOP-1 + TOP-2 (K5 + K4) | 0 | 90 min | + appendix figure |
| TOP-1 + TOP-2 + TOP-3 (K5+K4+K1) | 80.30 | 180 min | + provenance claim |
| All 7 axes pilot | 279.90 | ~600 min | comprehensive + multiple null results |

## 7. Honest limits — does kick really need to be quantum?

**Information-theoretic answer: NO at current anima/nexus scale.**

- Single-bit ±1 per kick step. Distinguishability quantum-vs-PRNG bounded at <1 bit per kick. Long-trajectory aggregation amplifies only if Lyapunov λ·T_obs > 1 (chaotic regime). anima/nexus are bounded/contractive (Banach), so amplification is sub-exponential. Practical: KS-test on 1000-step trajectory PASS_NULL likely.
- K2/K5 invoke real quantum theorems (Grover √N, contraction quadratic speedup arxiv 2602.10296) — but constants + small N (≤64 configs, ≤45 lines) nullify wall-clock benefit. Both ASYMPTOTIC.
- K3 quantum-noise-as-regularizer — npj QI May 2025 confirms it works as regularizer but WITHOUT advantage over Gaussian / Bernoulli classical noise at NISQ scale. $80 buys nothing.
- K7 GHZ violation guaranteed on Forte 1 (Aspect 1982 robust) — but translation from "5 measurement bits are non-locally correlated" to "anima 4-axis binding gains nonlocal mediator" is unjustified because the binding mediator is a CLASSICAL LINEAR MIXER (correlation washes out at output unless mixer itself is quantum, which it is not).
- **Truth:** classical PRNG (chacha20 / numpy default_rng) is SUFFICIENT for all 7 kick axes within current anima/nexus measurement frameworks. Quantum kick gives PROVENANCE, not POWER.
- The TRUE high-value Braket axes for anima/nexus remain #121 QA6 (QRNG audit, $0) and #122 1d (hybrid IonQ-seeded HMAC-DRBG, $20.78/session). K1-K7 EXTEND audit-trail coverage but do NOT add new computational/scientific value.

**Anti-hype:** do NOT claim "quantum-kicked anima cognition" from any K1-K7 even if PASS. Only QRNG (QA6), substrate-invariance witness (#121 Plans A/B), and CHSH (#122 4a) are scientifically defensible Braket spending lines for anima/nexus today.

## 8. Decision paths for user

| Path | Cost | Wallclock | Verdict |
|------|-----:|----------:|---------|
| **P_kick_zero_cost (K5+K4)** | $0 | 90 min | **RECOMMENDED if 'do something free with kick'** |
| P_kick_narrative (K5+K4+K1) | $80.30 | 180 min | Optional if quantum-provenance marketing wanted |
| P_kick_paper_grade (K7 GHZ) | $102.70 | 120 min | HIGH RISK; prefer #122 4a CHSH at $81.20 |
| **P_kick_skip (default)** | $0 | 0 | **#122 Phase 3 sufficient; no new science forfeited** |

## 9. Sources

- arxiv 2602.10296 — Quadratic Speedup for Computing Contraction Fixed Points (2024)
- npj Quantum Info May 2025 — Trade-off between gradient measurement efficiency and expressivity in deep quantum NN
- arxiv 2109.03687 — Variational quantum amplitude estimation
- Springer Comm Math Phys 2025 — Exponential Speedups for Quantum Walks in Random Hierarchical Graphs
- arxiv 2410.19921 — Method for noise-induced regularization in quantum NN
- ScienceDirect 2025 — Stochastic quantum NN for neuroinspired intelligence
- prior: state/braket_anima_applications_2026_05_02/applications.json (#121)
- prior: state/braket_nexus_applications_2026_05_02/applications.json (#122)
