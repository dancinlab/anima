# H_1065 — csp-cheap-scalable-ruler-validation

**Status:** PRE-REGISTERED (frozen before scoring)
**Date:** 2026-06-09
**Lineage:** forward of H_1064 (CSP defined + rank-tracked φ on planning split); re-opens the
H_1049 scalable-estimator question (IB-coarse-grain 🔴 was NOT a scalable Φ estimator) with a
NEW candidate (CSP), under the H_988/989 proxy-blindness wall.
**Scope:** TOY n≤4 EXACT (n=5 mirror-proven), 30 seeds, SERIAL CPU $0, 0 GPU/pod.

## §hypothesis (falsifier)

H_1064 found a SURPRISE: on **planning split** policies the independent causal proxy **CSP**
(causal self-prediction — held-out LOO ridge balanced-accuracy of macro-state→next-macro-state;
NO partition, NO MIP, O(n) not O(2^n)) rank-tracked BOTH faithful φ_EI AND big-Φ. That raises
the high-value question H_1049 left open: **can the cheap behavioral CSP serve as a VALIDATED
cheap scalable ruler that rank-matches the EXACT faithful φ_EI ground-truth ACROSS MULTIPLE
substrates — or does it hit the H_988/989 proxy-blindness wall (a purpose-blind proxy scores
structured == random)?**

### FROZEN falsifier (locked BEFORE any CSP-vs-φ correlation is viewed; NO goalpost move)

- `SPEARMAN_BAR = 0.7` — pooled rank-match bar.
- `WITHIN_FRAC = 3/4` — must rank-match within ≥3 of 4 substrates (per-substrate Spearman ≥ 0.7).
- `D_BAR = 0.8` — proxy-blindness wall discrimination effect-size bar (Cohen's d).
- `SIGN_EPS = 1e-3`.

**H1-VALIDATED-CHEAP-RULER (PASS):** CSP rank-matches exact faithful φ_EI
(pooled Spearman ≥ `SPEARMAN_BAR` **AND** holds within ≥ `WITHIN_FRAC` substrates) **AND** passes
the proxy-blindness wall on **ALL** substrates (CSP[structured] > CSP[random] with d ≥ `D_BAR`)
→ CSP is a validated cheap scalable ruler.

**FAIL modes (BOTH publishable, a_paper_negative_ok):**
- **(a) PROXY-BLIND-WALL-HIT:** CSP fails the H_988/989 wall on ≥1 substrate (structured ≈ random,
  d < `D_BAR`) → CSP is a purpose-blind proxy, NOT a ruler — confirms the a_phi_iit4_tool / H_988
  prohibition is fundamental; H_1064's rank-agreement was planning-substrate-local.
- **(b) SUBSTRATE-RELATIVE-ONLY:** CSP rank-matches within-substrate but pooled Spearman < bar
  OR within < 3/4 (no global ordinal scale) → cheap ruler is substrate-relative only.

## §method

**Ground truth (a_phi_iit4_tool, NEVER a proxy-as-Φ-verdict):** exact faithful φ_EI via the
stdlib IIT-4.0 mirror (h1004 `faithful_phi`), RE-PROVEN ≡ stdlib EXACT 6dp at n=4 AND n=5
(h1012 `prove_mirrors_at_n`) BEFORE scoring. MI in **BITS/log2** (MI=H(A)+H(B)−H(A,B); H_1043
nats-bug lesson). CSP is the CANDIDATE tested AGAINST φ_EI, never used AS the Φ verdict.

**CSP candidate (REUSED UNMODIFIED from H_1064):** `causal_self_prediction(bits)` — per-target-bit
leave-one-out held-out closed-form ridge predicts next-bit from the current full macro state;
CSP = mean_j max(0, balanced_acc_j − 0.5). O(n)/MIP-free.

**≥4 DISTINCT toy substrates** spanning the campaign's range, each producing a STRUCTURED and a
RANDOM variant of the same macro bits (n=4) per seed (30 seeds):
1. **planning-split** — `planning_trajectories(seed,8)` plan rollout (H_1039/H_1064 path).
2. **integrated/low-rank** — H_1062 `_iv_lowrank` on the GREEDY channels (shared rank-1 mixing).
3. **temporal-recurrence** — H_1062 `_iv_ema` on the GREEDY channels (temporal redundancy).
4. **modular/gain** — H_1062 `_iv_gain` on the GREEDY channels (per-channel sharpening, low cross-coupling).

For each substrate the STRUCTURED variant is the intervention output (median-binarized); the
RANDOM variant is a per-column time-shuffle control on the SAME structured bits (destroys the
temporal cause-effect structure CSP and φ_EI both read, while preserving each bit's marginal
on-fraction exactly). The shuffle is the H_988/989-style purpose-blindness stressor: a proxy
blind to causal structure scores the shuffle == the structured original.

**TEST per substrate (over 30 seeds):**
- (a) GENERALITY: Spearman(CSP, faithful φ_EI) within-substrate (structured arm); pooled Spearman
  over all 4×30 structured instances.
- (b) PROXY-BLINDNESS WALL (MANDATORY, the H_988/989 guard): Cohen's d of CSP[structured] vs
  CSP[random]; the SAME wall reported for faithful φ_EI as a sanity baseline (φ_EI MUST pass it).
- (c) COST: confirm CSP is O(n)/MIP-free vs faithful's exact-EI cost (structural asymptotic claim).

## §measurement

Real run: `python3 UNIVERSE/h1065_csp_cheap_scalable_ruler.py` → raw stdout +
`h1065_csp_cheap_scalable_ruler_result.json`. Reproduce-H_1064 check (CSP ρ_faithful ≈ +0.815 on
planning split) confirmed BEFORE scoring. Verdict persisted verbatim at
`.verdicts/1065_csp_cheap_scalable_ruler/H_1065.txt`.

## §finding

Per-substrate {faithful φ_EI mean · CSP mean · CSP↔φ_EI rank-match Spearman · structured-vs-random
d} table + pooled Spearman vs FROZEN 0.7 + proxy-blindness wall result per substrate vs FROZEN
d 0.8 → terminal verdict (validated cheap ruler / proxy-blind-wall-hit closed-neg /
substrate-relative-only). a_scale_honest_scope: the O(n) cost claim is STRUCTURAL (asymptotic),
but the rank-MATCH is validated only at n≤4 (n=5 mirror-proven) — scale-transfer UNVERIFIED.

## xref
- [[h1064-split-measure-adjudication]] — CSP defined; rank-tracked φ on planning split.
- [[scalable-phi-estimator-ib-closed-neg]] — H_1049 IB-coarse-grain 🔴 (the open question).
- [[iit4-real-engine-in-stdlib-not-proxy]] — faithful φ_EI = ground truth, NEVER proxy-as-verdict.
