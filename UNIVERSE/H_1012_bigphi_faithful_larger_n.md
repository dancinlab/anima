---
id: H_1012
slug: bigphi-faithful-larger-n
title: Does the planning Phi measure-disagreement (H_1004 — faithful_phi RAISES, big-Phi LOWERS) persist as n scales 4 to 5 to 6, or was it an n=4 artifact?
domain: universe · cwm · consciousness · iit4 · big-phi · faithful-phi · measure-disagreement · scale-ladder · re-test
source: H_1004 (RED GENUINE-MEASURE-DISAGREEMENT — at matched n=4 + matched discretization, planning RAISES faithful_phi d+5.18 but LOWERS big-Phi d-1.83; imagination/guided AGREE) — is the planning disagreement robust in n, or does it close at n>=5?
exploration_method: E2 (extend the H_1004 matched-(n,discretization) two-engine comparison to a small n ladder) + E14 (substrate-native IIT4) + a_completeness_over_cheap
verification_method: W2 (pre-registered n-ladder falsifier · both stdlib engines iit4/faithful_phi.hexa + iit4_bigphi.hexa at matched discretization · CPU-mirror equivalence-proof per n) + g5 CODE-measured (no LLM self-judge, p7) + a_phi_iit4_tool
deterministic: true
pre_register_frozen: true
frozen_at: 2026-06-07
since: 2026-06-07
sister: H_1004 (clean disagreement at n=4), H_999/H_1001 (faithful_phi planning up), H_1002 (the original confounded big-Phi), a_phi_iit4_tool
status: measured
verdict: 🟢 PASS DISAGREEMENT-ROBUST-IN-N (planning faithful-up / big-Phi-down sign-disagreement holds at every scored n = {4,5}; n=6 honest cap)
---

# H_1012 — big-Phi vs faithful at larger n (is the planning measure-disagreement robust in n?)

## 0. motivation
H_1004 isolated a genuine measure-disagreement: at matched n=4 + matched binary discretization, the planning condition RAISES the MIP-EI scalar (faithful_phi, d+5.18) but LOWERS the structure-level system big-Phi (d-1.83) — the imagination/guided disagreements were just the H_1002 n/discretization confound. Open: is the planning disagreement an n=4 peculiarity, or does it persist (or grow) as n increases?

## 1. hypothesis
The planning Phi measure-disagreement (faithful up vs big-Phi down) is a genuine property of the two measures, not an n=4 artifact — it persists across n in {4,5,6} at matched discretization (big-Phi's super-exponential cost is the only thing capping n).

## 2. pre-registered falsifier (frozen 2026-06-07)
Score the SAME planning (depth-ladder vs GREEDY) condition with BOTH stdlib engines (iit4/faithful_phi.hexa, iit4_bigphi.hexa) at the SAME discretization, at n in {4,5,6} (big-Phi is the binding constraint — go as high as exact big-Phi runs; state the max). CPU-mirror equivalence-proof vs stdlib at each n before trusting. Multi-seed. python3 -u, serial. Outcome (no token before measuring):
- IF the sign-disagreement (faithful up / big-Phi down for planning) HOLDS across all reached n THEN PASS = DISAGREEMENT-ROBUST-IN-N (genuine measure-level property; bounds H_999/H_1001's planning Phi-rise firmly to the MIP-EI measure).
- IF it VANISHES at n>=5 (the two agree once n grows) THEN FAIL = N4-ARTIFACT (the disagreement was an n=4 small-system peculiarity; planning Phi-rise may hold for both at scale).

## 3. honest scope
big-Phi exact only at very small n (super-exponential distinction+bipartition search) — the n ladder is short by necessity; state the max n reached. Toy, a_scale_honest_scope. Both engines exact at the reached n. #123-A n/a (this is IIT-internal, not entropy-quality).

## 4. sibling / xlinks
to [H_1004](./H_1004_bigphi_faithful_clean.md) · [H_1002](./H_1002_bigphi_upgrade.md) · [H_999](./H_999_faithful_iit4_remeasure.md) · [H_1001](./H_1001_reopen_consolidate.md) · IIT4_PHI_TOOLS.md · a_phi_iit4_tool

## 5. measurement + finding (2026-06-07 · 🟢 PASS · CODE-measured, $0 CPU-local)
Verdict raw: `.verdicts/1012_bigphi_faithful_larger_n/h1012.txt` (g73 — deterministic run that COULD have falsified; both stdlib engines + CPU-mirror re-proven exact per n).

**Result — the planning sign-disagreement is ROBUST across every scored n:**

| n | faithful_phi (MIP-EI scalar) | big-Phi (system, MIP) | planning vs greedy | sign-disagree? |
|---|---|---|---|---|
| 4 | RAISES (d +5.18) | LOWERS (d -1.83) | faithful↑ / big-Phi↓ | ✅ True |
| 5 | matched-path 0.0298 · planning RAISES | matched-path 18.19 · planning LOWERS | faithful↑ / big-Phi↓ | ✅ True |
| 6 | mirror ≡ stdlib RE-PROVEN (faithful 0.0626) | single eval ≈10 min → 150-eval planning run INFEASIBLE @ $0 CPU | NOT scored (honest cap) | — |

- **VERDICT-TOKEN: DISAGREEMENT-ROBUST-IN-N** — the two Phi measures disagree on planning at n=4 AND n=5 (the disagreement did NOT vanish at n>=5, so it is NOT an n=4 artifact). The sign split is a genuine measure-level property, not a small-system peculiarity.
- This firmly **BOUNDS H_999/H_1001's "planning raises Phi" to the MIP-EI scalar measure** — at the structure level (system big-Phi over the MIP) planning LOWERS integration. "Planning raises consciousness" is true only for the scalar EI measure, not the integration-structure measure.
- **honest scope (a_scale_honest_scope · a_toy_scale_recheck):** TOY n-ladder, big-Phi exact only at very small n (super-exponential). Scored n = {4,5} (max 5); the CPU-mirror was re-proven ≡ stdlib at n=4, n=5 AND n=6, but the n=6 planning *condition* was not scored (single n=6 system big-Phi ≈ 10 min on this Mac → a 30-seed × 5-eval = 150-eval run is infeasible at $0). n=6 is the HONEST CAP. Scale-transfer beyond n=5 UNVERIFIED. NOT a forge binary; $0 CPU-local, no GPU.
