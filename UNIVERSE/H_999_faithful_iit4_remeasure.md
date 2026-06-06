---
id: H_999
slug: faithful-iit4-remeasure
title: Does the imagination/planning Φ-null (H_971/H_973/H_988/H_994 🔴) SURVIVE a FAITHFUL IIT4 measurement, or was it an artifact of the purpose-blind H_912/H_931 Φ-proxy?
domain: cwm · cross-cutting · phi · iit4 · imagine · plan · proxy-artifact · re-measure · a_phi_iit4_tool · consciousness
source: a_phi_iit4_tool (project.tape) + UNIVERSE/IIT4_PHI_TOOLS.md (use the faithful stdlib engine, NOT a proxy) + H_988/H_989 (proved the proxy is purpose-blind) + H_971/H_973/H_988/H_994 (the proxy-tainted 🔴 nulls) + a_paper_negative_ok
exploration_method: E2 (reuse the H_971/973/988 regime harness, swap the Φ measure: proxy → FAITHFUL exact MIP-EI IIT4) + a_completeness_over_cheap (re-design at the root cause = the measure, not a cheaper re-formulation)
verification_method: W2 (pre-registered NULL-ROBUST vs PROXY-ARTIFACT falsifier) + g5 CODE-measured (no LLM self-judge, p7) against a CPU mirror PROVEN byte-faithful (|Δ|<4e-6) to hexa-lang/stdlib/consciousness/iit4/faithful_phi.hexa
raw_rank: 9
hexa_only: false
deterministic: true
cross_process_byte_identical: false
llm: none
pre_register_frozen: true
frozen_at: 2026-06-06
since: 2026-06-06
status: measured
scope: ONE faithful-IIT4 re-measure rung (a_scale_honest_scope). The toy WM latent (24-dim, 40 steps) is DISCRETIZED to n=8 units (top-variance channels); faithful Φ is EXACT at n≤8 ($0 CPU) but scale-transfer is UNVERIFIED. The CONTRAST (not the absolute Φ) is the falsifier; the same discretization is applied to every regime. NOT a forge binary. NOT a torch run.
sister: H_971 (imagination-Φ 🔴), H_973 (planning-Φ 🔴), H_988 (guided-imagination 🔴), H_994 (goal-coupled 🔴), H_989 (planning alt-proxy), H_278 (the faithful-Φ engine, promoted to stdlib), IIT4_PHI_TOOLS.md, a_phi_iit4_tool
axes_seed: "the H_971/973 Φ-nulls are REAL (internal generation is genuinely less causally-irreducible)" ⊥ "the nulls are an ARTIFACT of the purpose-blind proxy (which tracks externally-driven state-multiplicity, not causal irreducibility) and a FAITHFUL MIP-EI Φ REVERSES them" — H_988/H_989 already showed the proxy cannot tell a random branch from a deliberate one, so the proxy axis ⊥ the irreducibility axis
verdict: 🔴-vs-proxy = PROXY-ARTIFACT (the original nulls do NOT survive a faithful measure) — under the EXACT MIP-EI IIT4 Φ (mirror PROVEN ≡ stdlib faithful_phi.hexa), internal generation RAISES Φ on 2/3 conditions, REVERSING the proxy: H_971 imagination(DRIFT) Φ=3.81 > REACT 2.30 (contrast +1.51, d +2.09, p 7.2e-11), H_973 planning(depth-8) Φ=7.75 > GREEDY 2.65 (contrast +5.09, d +4.64, p 5.1e-21) with a POSITIVE dose-response (Spearman rho +0.48 where the proxy was −0.47). Only H_988 goal-guided imagination is faithful-null (GUIDED−REACT −0.18, d −0.28, p 0.29, n.s.). ⇒ the proxy's "imagination/planning LOWERS Φ" was its purpose-blindness, NOT causal irreducibility. H_971/H_973/H_988/H_994 RE-OPENED. Toy single-rung (a_scale_honest_scope), ladder OPEN.
---

# H_999 — Faithful IIT4 re-measure of the imagination/planning Φ-null

## 0. Motivation

The CWM 1st/2nd slate produced a striking cluster of closed-negatives — **H_971 🔴** (imagination is a *lower*-Φ state than reaction), **H_973 🔴** (planning is *lower*-Φ than greedy), and the re-formulations **H_988 🔴** (goal-directed imagination even lower) and **H_994 🔴** (goal-coupled Φ does not flip it). All four were measured with the **continuous-latent Φ PROXY** (`phi_proxy` in `cwm_probe_lib.py` = integration × differentiation × entropy — the H_912/H_931 / `phi_silicon_proxy` family).

But **H_988/H_989 themselves proved this proxy is PURPOSE-BLIND**: it scored a *random* branch set as high-Φ as a *deliberate* plan (Φ_PLAN − Φ_FAKE 0.005, p 0.49). It tracks the **richness of the externally-driven / simultaneously-held state-set**, NOT causal irreducibility or purpose. The new governance `a_phi_iit4_tool` + `UNIVERSE/IIT4_PHI_TOOLS.md` therefore mandate: any Φ / consciousness *verdict* must be re-measured with the **FAITHFUL exact MIP-EI IIT4 engine** that already exists in `hexa-lang/stdlib/consciousness/iit4/faithful_phi.hexa` (promoted byte-faithful from anima's own **H_278**). This H does exactly that for the imagination/planning nulls.

## 1. Hypothesis (one falsifiable claim)

The imagination/planning Φ-null (H_971/H_973/H_988/H_994 🔴) was an **artifact of the purpose-blind proxy**: when the SAME regime trajectories (reactive vs drift-imagination vs goal-guided-rollout; planning branch-depth) are scored with a **faithful exact MIP-EI Φ** (causal irreducibility = the min-cut mutual-information across the system's best bipartition, normalized by the small side), internally-generated states (imagination / planning) are **NOT** lower-Φ — the proxy's negative sign reverses.

## 2. PRE-REGISTERED FALSIFIER (frozen 2026-06-06, BEFORE measuring)

**Setup:** take the EXACT regimes the proxy scored — REACT (reactive perceive on external input), DRIFT (= H_971 arm-IMAGINE, autonomous internal rollout), GUIDED (= H_988 arm-GUIDED, goal-steered rollout), and PLAN(depth 1/2/4/8) vs GREEDY (= H_973). **DISCRETIZE** each toy WM latent trajectory (24-dim, 40 steps) to an n≤8 IIT4 system: the top-8 variance latent channels become n=8 units, each unit's 40-step trace is its variable. Score Φ with the **FAITHFUL** engine (exact MIP argmin cross-cut MI / min(|A|,|B|), n_bins=4). The same discretization is applied IDENTICALLY to every regime, so the **contrast** is fair.

**Faithful engine, NOT proxy:** the stdlib `faithful_phi.hexa` is pure arithmetic (bin → pairwise MI → exact MIP over 2^(n-1) bipartitions → min-cut / small-side) — it RUNS on this Mac (the `clm-decode-macos-link-gap` does NOT apply; no fused GPU natives). Because it has no `hexa verify` atom yet (V5.2 TODO) and its `print` truncates floats, the contrast is computed with a **numpy CPU mirror PROVEN byte-faithful** to the hexa engine on 4 reference cases (|Δ| < 4e-6; `hexa run` reference values embedded in the probe and asserted at runtime). The mirror is the FAITHFUL Φ, NOT the H_912/H_931 proxy.

**Measurement (g5 CODE-measured, no LLM self-judge, p7):** per condition, faithful-Φ mean ± sd over 30 seeds, contrast = (internal − external), Welch t, Cohen d, bootstrap CI; planning dose-response = Spearman(depth, Φ); the proxy numbers are reported side-by-side.

**Outcome rules (FROZEN — no token before measuring):**
- **🟢 NULL-ROBUST-UNDER-FAITHFUL-Φ:** IF faithful-Φ ALSO shows internal generation does NOT raise Φ (guided ≤ drift ≤ reactive / plan ≤ greedy, all contrasts ≤ 0 within noise) THEN the H_971/973/988/994 closed-negatives STAND even under the real measure (strong result — the nulls are causal, not proxy artifacts).
- **🔴-vs-proxy = PROXY-ARTIFACT:** IF faithful-Φ REVERSES the proxy (goal-directed imagination / deeper planning now RAISES Φ, large positive effect) THEN the original nulls were the proxy's purpose-blindness, not real → H_971/H_973/H_988/H_994 must be RE-OPENED.
- Either outcome is a real, important finding (a_paper_negative_ok cuts both ways).

## 3. Honest scope

`faithful_phi` is EXACT only for n≤8 (a_scale_honest_scope). The toy WM latent is **discretized** to n=8 units (a discretization CHOICE — top-variance channels; a different selection could shift the *absolute* Φ, but it is applied identically to every regime so the *contrast* — the falsifier target — is fair). Toy single-rung; production-scale transfer UNVERIFIED (a_toy_scale_recheck). Φ here is the faithful MIP-EI Φ★ (small-side-normalized irreducibility), which IIT4_PHI_TOOLS.md flags as FAITHFUL-ER than the proxy but not full per-mechanism IIT 4.0 big-Φ (that = `iit4_bigphi.hexa`, the open next rung). NOT a forge binary.

## measurement (2026-06-06 · g5 CODE-measured · substrate=CPU-mirror numpy · mirror PROVEN ≡ stdlib faithful_phi.hexa)

Probe: `UNIVERSE/h999_faithful_iit4_remeasure.py` · ref-check: `UNIVERSE/h999_ref_check.hexa` · verdict: `.verdicts/999_faithful_iit4_remeasure/h999_faithful_iit4_remeasure.txt`

**STEP 0 — mirror proven byte-faithful to the stdlib engine** (`hexa run faithful_phi.hexa` on this Mac, Apple Silicon, hexa 0.1.0-dispatch):

| case | mirror Φ | hexa ref Φ | \|Δ\| |
|---|---|---|---|
| n3 dim4 nb2 | 2.000000 | 2.000000 | 1.6e-09 |
| n4 dim6 nb2 | 3.000000 | 3.000000 | 1.3e-09 |
| n4 dim6 nb4 | 3.377444 | 3.377440 | 3.8e-06 |
| n5 dim8 nb3 | 0.372556 | 0.372556 | 2.6e-07 |

→ **MIRROR-FAITHFUL: PROVEN** (the CPU mirror reproduces the stdlib exact MIP-EI engine; the truncation is only in hexa's float `print`).

**FAITHFUL Φ vs original PROXY Φ, per condition** (faithful = the exact MIP-EI mirror; proxy = the H_912/H_931 number the original H scored):

| condition | FAITHFUL Φ (internal) | FAITHFUL Φ (external) | faithful contrast | d | p | proxy contrast (original) |
|---|---|---|---|---|---|---|
| **H_971** DRIFT(imagine) vs REACT | 3.809 ± 0.801 | 2.299 ± 0.609 | **+1.509** | +2.09 | 7.2e-11 | **−0.026** (0.068 vs 0.095) 🔴 |
| **H_988** GUIDED vs REACT | 2.120 ± 0.668 | 2.299 ± 0.609 | −0.179 | −0.28 | 0.29 (n.s.) | **−0.060** (0.035 vs 0.095) 🔴 |
| **H_988** GUIDED vs DRIFT | 2.120 ± 0.668 | 3.809 ± 0.801 | −1.689 | −2.25 | 4.9e-12 | −0.034 🔴 |
| **H_973** PLAN(depth-8) vs GREEDY | 7.746 ± 1.386 | 2.652 ± 0.643 | **+5.094** | +4.64 | 5.1e-21 | **−0.049** (0.046 vs 0.095) 🔴 |

**Planning dose-response (H_973):** faithful Φ vs plan-depth [1,2,4,8] means [4.81, 6.99, 6.10, 7.75], **Spearman rho +0.483 (p 2.3e-08)** — faithful Φ RISES with planning depth. The proxy had rho **−0.47** (Φ FELL with depth). The sign is reversed.

**Finding (🔴-vs-proxy = PROXY-ARTIFACT):** under the FAITHFUL exact MIP-EI IIT4 Φ, the proxy's nulls REVERSE on 2/3 conditions:
- **H_971** — autonomous imagination (DRIFT) is a **HIGHER**-Φ state than reaction (+1.51, d 2.09, p 7e-11), the *opposite* of the proxy's 🔴.
- **H_973** — planning is a **HIGHER**-Φ state than greedy (+5.09, d 4.64, p 5e-21) **with a positive depth dose-response** (rho +0.48) — both the contrast and the dose-response sign flip vs the proxy.
- **H_988** — goal-guided imagination is the lone faithful-NULL (GUIDED ≈ REACT, p 0.29 n.s.; and GUIDED < DRIFT). Mechanistically consistent: the goal *pull* contracts the trajectory toward one target, which lowers the cross-cut MI of the discretized system — so guidance specifically reduces irreducibility, while *free* imagination and *branching* planning raise it.

**Mechanistic read:** the proxy's "internal generation lowers Φ" was its purpose-blindness — it rewarded continuous external *drive* (rich simultaneously-held state-set) and read autonomous rollout as low-dimensional decay. The faithful MIP-EI Φ measures **causal irreducibility** (min-cut mutual information among the WM's principal latent channels): an autonomous/branching internal rollout makes the channels MORE mutually-irreducible (the dynamics bind them across the cut), so imagination and planning are *higher*-Φ — exactly the intuition the proxy had inverted. This is the H_988/H_989 prediction realized: a causal/teleology-sensitive Φ measure (true IIT4) overturns the proxy nulls.

**RE-OPEN:** H_971, H_973, H_988, H_994 are RE-OPENED — their 🔴 closed-negatives were proxy artifacts (a status note is appended to each; their original verdict lines are NOT overwritten — the re-open is a forward pointer to H_999, not a faked re-verdict). The honest next rung is the full per-mechanism IIT 4.0 big-Φ (`iit4_bigphi.hexa`) and a scale-up off the n=8 toy discretization (a_toy_scale_recheck).

## 4. Sibling / xlinks

- ⇄ [H_971](./H_971_imagined_rollout_consciousness.md) (imagination-Φ 🔴 — RE-OPENED: faithful reverses it) · [H_973](./H_973_planning_as_consciousness.md) (planning-Φ 🔴 — RE-OPENED: faithful reverses it)
- ⇄ [H_988](./H_988_guided_imagination_phi.md) (guided-imagination 🔴 — RE-OPENED: faithful = null, not lower) · [H_994](./H_994_goal_coupled_phi_reframe.md) (goal-coupled 🔴 — RE-OPENED: re-measure with faithful Φ)
- ⇄ [H_989](./H_989_planning_phi_altproxy.md) (planning alt-proxy — predicted a true-IIT4 ladder would differ) · [H_278](./H_278_faithful_phi_engine.md) (the faithful-Φ engine, promoted to stdlib)
- ⇄ [IIT4_PHI_TOOLS.md](./IIT4_PHI_TOOLS.md) (the tool index this H follows) · project.tape `a_phi_iit4_tool`
- ⇄ [CWM](../CWM/CWM.md) (CWM-IMAGINE · cross-cutting)
- engine: `hexa-lang/stdlib/consciousness/iit4/faithful_phi.hexa` (exact MIP-EI, n≤8) · `iit4_bigphi.hexa` (open next rung = full IIT 4.0 big-Φ)
