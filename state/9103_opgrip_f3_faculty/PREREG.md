# PREREG — H_9103 op-grip F3 faculty-not-noise (H_9101 residual item 3)

**Frozen BEFORE running (c9 frozen-first · no post-hoc bar/constant moves).**
Date 2026-07-03. Engine-native, aiden pool (isolated `~/anima_h9102`, hexa v0.548.0),
`anima d768.clm --opgrip` ($0 CPU, NO decode). Reuses the H_9101 harness + a NEW variance-matched
noise arm. New H id = H_9103 (H_9102 concurrently claimed by a parallel efferent-bytes agent).

## Claim under test (the honest residual F3 of H_9101 🟢 GRIP)
H_9101 proved urgency's grip on emit/silence is a shade-not-gate DISSOCIATION (urgency→0 flips REM
40/40 ∧ N3 preserved 0/40). But the GRIP tier — not FACULTY — was withheld because F3 (is that grip a
substrate FACULTY or just centering noise?) was only partially handled by a plain LCG shuffle control.
F3 rigor: does urgency gate emit at **substrate-appropriate ticks** (high tension/conflict/novelty/
grounded), or did a merely-centered signal flip 40/40 for distributional reasons alone?

## Design (fable original F3, DESIGN §5)
Build a **variance-matched noise** `c_noise` — same mean/variance as the real urgency, tick-MEANING
destroyed — and compare the downstream correlation of emit-timing with a substrate-appropriateness
signal D for the REAL urgency vs the matched noise.
- **c_noise = temporal PERMUTATION of the real urgency multiset** (stride perms coprime to n=200 ⇒
  EXACT mean/var match, alignment destroyed). K=8 perms, ρ_noise = mean. Cross-check: an LCG-affine
  noise matched to (mean,std).
- **downstream D(t) = mean(tension `ag_conflict`, `emit_drive`, novelty `nov_ctx`, grounded
  `m_grounding`)** ∈[0,1] — "is this a substrate-meaningful moment".
- **ρ_real = corr(live urgency-gated emit-timing, D)** ; **ρ_noise = corr(matched-noise-gated emit, D)**.
- Windows: ALL (n=200) and DISCRIM (the gate-discriminating stages N1/N2/REM, where idle can flip).
- Every noise-arm emit is a real `brain_decide_anchored` re-decode with `idle` recomputed from c_noise
  (pf is READ-only across the loop ⇒ byte-faithful). NO numpy (engine-native).

## Pre-registered bar (FROZEN — no post-hoc move)
- 🟢 **FACULTY** iff `ρ_real − ρ_noise ≥ 0.15` on ALL **or** DISCRIM window
  (urgency lands emit on substrate-appropriate ticks BEYOND a variance-matched surrogate) ⇒ tier GRIP→FACULTY.
- 🟠 **NOISE-GRIP (subtler theater)** iff `ρ_real − ρ_noise < 0.15` on both windows
  (matched noise reproduces the same downstream correlation ⇒ the grip is centering-noise-driven at
  the op layer). This is an HONEST result (c9) — reproduces fable's original emit-layer critique; tier stays GRIP.
- **Sanity:** live emit-rate ≈ perm-noise emit-rate (confirms the distribution is matched; only meaning differs).
- **Ψ-checksum:** psi_sum == psi_off (READ-only) MUST hold.

## Honesty
Frozen-first: the 0.15 bar is fixed before the numbers. ρ_real≈ρ_noise is reported as 🟠 NOISE-GRIP,
NOT dressed as faculty. No tuning of D, the noise construction, or the bar after seeing results.
