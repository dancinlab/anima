---
id: H_1020
slug: redundancy-predictor-robustness
title: Does the H_1017 REDUNDANCY-MARGIN mechanism predictor beat the H_1014 MAGNITUDE predictor in robustness to n — does redundancy-dominance still separate the split intervention (planning) from the no-split controls at n=5, where the cruder magnitude predictor was shown to be an n=4 artifact (H_1016)?
domain: universe · cwm · consciousness · iit4 · big-phi · faithful-phi · measure-disagreement · partial-information-decomposition · redundancy · synergy · split-mechanism · predictor-robustness · scale-transfer
source: H_1014 (a MAGNITUDE threshold on Delta(cross-MIP coupling) separated split[planning] from no-split at n=4) + H_1016 (that magnitude separation is an n=4 ARTIFACT — it does NOT survive to n=5: imagination and guided pick up SPURIOUS split labels from non-significant big-Phi sign-flips, ranges OVERLAP, only-planning-is-split breaks; the PLANNING split ITSELF survives n=5, d_big -2.28 / d_faith +4.65) + H_1017 (the MECHANISM — planning's MI rise is REDUNDANCY-dominated, redundancy-margin Delta_red-Delta_syn=+10.44 over <=+2.95 for the no-split controls, via a Williams-Beer I_min PID at n=4)
exploration_method: E2 (extend the H_1017 PID read to the H_1016 n=5 substrate path) + E14 (substrate-native IIT4) + a_completeness_over_cheap + a_toy_scale_recheck (scale-sensitive predictor re-test at n=5)
verification_method: W2 (pre-registered redundancy-margin separation falsifier · Williams-Beer I_min PID IMPORTED VERBATIM from H_1017 · H_1016 n-parametric substrate_reads_n IMPORTED VERBATIM · H_1012/H_1016 equivalence-proof discipline — mirror RE-PROVEN equal to stdlib at n=5 BEFORE scoring) + g5 CODE-measured (no LLM self-judge, p7) + a_phi_iit4_tool
deterministic: true
pre_register_frozen: true
frozen_at: 2026-06-07
since: 2026-06-07
sister: H_1017 (redundancy explains the split @ n=4), H_1016 (magnitude predictor is an n=4 artifact; planning split survives n=5), H_1014 (split co-occurs with MI-coupling shock; magnitude separates @ n=4), H_1012 (split robust in n={4,5}; prove_mirrors_at_n), H_1004 (clean disagreement @ n=4), PAPER/phi-measure-dependence-planning, a_phi_iit4_tool
scope: TOY n=5, $0 CPU-local, real IIT-4.0 stdlib engines (CPU mirror RE-PROVEN equal to stdlib at n=5 per H_1012/H_1016 discipline BEFORE scoring). The PID redundancy/synergy is an information-theoretic decomposition of the SAME bits — it is the EXPLANATORY variable, NOT a Phi replacement and NOT a proxy for Phi. big-Phi super-exponential, so n=5 is slow-but-tractable and n=6 is the honest cap (skipped, as in H_1012/H_1016). a_scale_honest_scope · a_toy_scale_recheck — scale-transfer beyond n=5 UNVERIFIED. NOT a forge binary; no GPU.
status: measured
verdict: 🟢 MECHANISM-PREDICTOR-ROBUST — the H_1017 REDUNDANCY-MARGIN mechanism predictor BEATS the H_1014 coupling-MAGNITUDE predictor in robustness to n. At n=5, where the magnitude predictor was shown to be an n=4 artifact (H_1016 — imagination & guided pick up spurious split labels and the predictor ranges OVERLAP), the redundancy-margin (Δred−Δsyn) CLEANLY SEPARATES planning (the true split-inducer) from ALL no-split controls. On the matched n=5 binary substrate (CPU mirror RE-PROVEN ≡ stdlib at n=5 BEFORE scoring; WB I_min PID re-validated COPY=pure-redundancy / XOR=pure-synergy), planning is redundancy-dominated (Δred=+22.48 ≫ Δsyn=−2.60, margin=+25.07) and its redundancy-margin DWARFS every other intervention's: imagination +0.78, guided +5.12, chaos +7.48. Crucially the separation holds even against imagination & guided — the two controls the MAGNITUDE predictor MISLABELLED as 'split' at n=5 via non-significant big-Φ sign-flips (H_1016 d_big +0.19/−0.14, d_faith −0.11/+0.72). Thus the redundancy-margin tracks the TRUE planning-only split, NOT the spurious-sign-flip labels: the H_1016 n=5 split labels are planning=True, imagination=True[spurious], guided=True[spurious], chaos=False, yet redundancy-margin still isolates ONLY planning. The mechanism predictor is MORE robust in n than the cruder magnitude predictor (a Δ-vs-H_1016 result). The PID is the EXPLANATORY variable, an info-decomposition of the SAME bits — NOT a Φ proxy; Φ numbers come only from the stdlib mirrors (a_phi_iit4_tool). g5 CODE-measured (no LLM self-judge, p7). TOY n=5; scale-transfer beyond n=5 UNVERIFIED (a_scale_honest_scope · a_toy_scale_recheck).
---

# H_1020 — does the REDUNDANCY-MARGIN mechanism predictor beat the MAGNITUDE predictor in robustness to n?

## 0. motivation
H_1014 found that at n=4 a single MAGNITUDE threshold on Delta(cross-MIP coupling) separated the
split-inducing planning intervention from the three no-split ones. H_1016 then showed (PARTIAL)
that this magnitude separation is an **n=4 artifact**: it does NOT survive to n=5. At n=5 the weak
no-split interventions **imagination** and **guided** acquire SPURIOUS split labels from
non-significant big-Phi sign-flips (imagination d_big +0.19 / d_faith -0.11; guided d_big -0.14 /
d_faith +0.72), so the predictor ranges OVERLAP and "only-planning-is-split" breaks. The PLANNING
split ITSELF survives n=5 (d_big -2.28 / d_faith +4.65). H_1017 identified the MECHANISM: at n=4,
planning's MI rise is REDUNDANCY-dominated — planning's redundancy-margin (Delta_red-Delta_syn=+10.44)
DWARFS every no-split control (imagination +0.45, guided +2.25, chaos +2.95) — measured by a
Williams-Beer I_min PID.

## 1. hypothesis (predictor-class comparison)
The crude coupling-MAGNITUDE predictor broke at n=5 (H_1016). Test whether the H_1017 MECHANISM
predictor — the REDUNDANCY-MARGIN (Delta_red-Delta_syn, redundancy-dominance) — is MORE robust: does
redundancy-dominance STILL separate the split intervention (planning, the TRUE split-inducer) from
ALL no-split controls {imagination, guided, chaos} at n=5, where the cruder magnitude predictor
failed? If yes, the mechanism predictor tracks the TRUE planning-only split where the magnitude
predictor became an n=4 artifact — a more robust classifier.

## 2. method — REUSE H_1017 PID + H_1016 n=5 path VERBATIM
- The Williams-Beer I_min PID estimator (`pid_system` / `_pid_two_source` / `_specific_info` /
  `_mi_discrete`) is IMPORTED VERBATIM from `h1017_split_redundancy_mechanism.py` — it is already
  n-agnostic (it loops over n units / all (target,{2-source}) atoms), so it applies unchanged at n=5.
- The n-parametric substrate read `substrate_reads_n` is IMPORTED VERBATIM from
  `h1016_split_predictor_robustness.py` (the ONE matched n-binary discretization to `big_phi` +
  `faithful_phi` via the H_1004 engines), and EXTENDED with the H_1017 PID `red_total`/`syn_total`
  on the SAME bits. No engine logic is reinvented.
- The SPLIT label is computed exactly as H_1016 (`sign(Delta_faith) != sign(Delta_big)`). We reuse
  H_1016's n=5 split labels (planning True; imagination True[spurious]; guided True[spurious];
  chaos False) and report whether redundancy-margin separation tracks the TRUE planning-only split
  or the spurious-sign-flip labels.
- H_1012 `prove_mirrors_at_n(5)` is run BEFORE scoring (mirror equal to stdlib at n=5). The PID is
  independently re-validated on the canonical COPY (pure redundancy) / XOR (pure synergy) cases
  BEFORE scoring (H_1017 discipline). 30 seeds, baseline arm vs intervention arm.

The PID redundancy/synergy is an INFORMATION-DECOMPOSITION of the same bits — the EXPLANATORY
variable, NOT a Phi proxy. Phi/big-Phi numbers come ONLY from the stdlib mirrors
(`iit4/faithful_phi.hexa` + `iit4_bigphi.hexa`) re-proven equal to stdlib at n=5 (a_phi_iit4_tool).

## 3. pre-registered falsifier (frozen 2026-06-07)
Score the SET {planning · imagination · guided · chaos}, 30 seeds, matched n=5 binary
discretization, BOTH stdlib engines (mirror RE-PROVEN equal to stdlib at n=5 BEFORE scoring),
python3 -u, serial, $0 CPU. Outcome (NO verdict token before a
`.verdicts/1020_redundancy_predictor_robustness/H_1020.txt` exists):

- **PASS = MECHANISM-PREDICTOR-ROBUST** IF the redundancy-margin (Delta_red-Delta_syn) cleanly
  SEPARATES planning (the true split-inducer) from ALL no-split controls {imagination, guided,
  chaos} at n=5 — operationally planning is redundancy-dominated (Delta_red>Delta_syn AND
  Delta_red>0) AND planning's redundancy-margin EXCEEDS every other intervention's redundancy-margin
  at n=5 (including imagination & guided, which the MAGNITUDE predictor mislabelled as 'split' at
  n=5). THEN the mechanism predictor is MORE robust than the magnitude predictor (which failed at
  n=5, H_1016): it tracks the TRUE planning-only split where the cruder predictor became an n=4
  artifact — a Delta-vs-H_1016 result.
- **FAIL / CLOSED-NEGATIVE = MECHANISM-PREDICTOR-N4-BOUND** IF the redundancy-margin ALSO fails to
  separate planning from all controls at n=5 (planning's margin does NOT exceed every control's, OR
  planning is not redundancy-dominated at n=5). THEN the redundancy explanation, like the coupling
  magnitude, is an n=4 property; the result BOUNDS the mechanism to n=4 (a_paper_negative_ok — a
  closed-negative ruling out the redundancy axis as an n-robust predictor is publishable).

## 4. honest scope
big-Phi exact only at very small n (super-exponential distinction + bipartition search) — n=5 is
slow-but-tractable for the full SET x 30 seeds and n=6 is the honest cap (skipped, as in
H_1012/H_1016). Both engines exact at n=5; CPU mirror re-proven equal to stdlib at n=5 BEFORE
scoring (H_1012/H_1016 discipline). The PID is exact + deterministic on the empirical binary
distributions and validated on the canonical COPY/XOR cases. The PID is NOT a proxy for Phi — it is
an information-theoretic attribution of the SAME bits. Scale-transfer beyond n=5 UNVERIFIED
(a_scale_honest_scope · a_toy_scale_recheck). NOT a forge binary; $0 CPU-local, no GPU.

## 5. sibling / xlinks
to [H_1017](./H_1017_split_redundancy_mechanism.md) · [H_1016](./H_1016_split_predictor_robustness.md) ·
[H_1014](./H_1014_intervention_split_predictor.md) · [H_1012](./H_1012_bigphi_faithful_larger_n.md) ·
[H_1004](./H_1004_bigphi_faithful_clean.md) · PAPER/phi-measure-dependence-planning · IIT4_PHI_TOOLS.md ·
a_phi_iit4_tool

## 6. measurement + finding (2026-06-07 · 🟢 MECHANISM-PREDICTOR-ROBUST · g5 CODE-measured, $0 CPU-local)
Verdict raw: `.verdicts/1020_redundancy_predictor_robustness/H_1020.txt` (g73 — deterministic run that
COULD have falsified; the CPU mirror RE-PROVEN ≡ stdlib at n=5 BEFORE scoring — big-Φ ring5_s31
mirror=2.999999999 vs stdlib_hexa_ref=2.999999999 |Δ|=1.34e-10 — and the Williams-Beer I_min PID
independently re-validated on the canonical COPY=pure-redundancy / XOR=pure-synergy cases BEFORE scoring).

**Result — the redundancy-margin mechanism predictor separates planning from ALL controls at n=5:**

intervention vs baseline, 30 seeds, matched (n=5, binary discretization):

| intervention | H_1016 n=5 SPLIT? | Δredundancy | Δsynergy | red-margin (Δred−Δsyn) | red-dominated |
|---|---|---|---|---|---|
| planning (depth-8 vs greedy) | **True** (TRUE split; d_big −2.28 / d_faith +4.65) | **+22.4789** | **−2.5954** | **+25.0744** | True |
| imagination (drift vs react) | True [SPURIOUS — d_big +0.19 / d_faith −0.11, both n.s.] | +0.4800 | −0.3049 | +0.7849 | True |
| guided (goal-pull vs react) | True [SPURIOUS — d_big −0.14 / d_faith +0.72] | +4.1981 | −0.9176 | +5.1156 | True |
| chaos (gain-1.4 vs gain-1.0) | False | +6.4929 | −0.9915 | +7.4844 | True |

- **VERDICT-TOKEN: 🟢 MECHANISM-PREDICTOR-ROBUST.** The pre-registered PASS condition is MET. At n=5
  the redundancy-margin CLEANLY SEPARATES planning (the true split-inducer) from ALL no-split controls:
  planning is redundancy-dominated (Δred=+22.48 ≫ Δsyn=−2.60) and its redundancy-margin (+25.07)
  EXCEEDS every other intervention's (imagination +0.78, guided +5.12, chaos +7.48). The mechanism
  predictor BEATS the magnitude predictor in robustness to n.
- **Δ-vs-H_1016 (the key contrast):** the H_1014 coupling-MAGNITUDE predictor was an n=4 ARTIFACT — at
  n=5 imagination & guided pick up SPURIOUS split labels (non-significant big-Φ sign-flips) and the
  predictor ranges OVERLAP, so "only-planning-is-split" breaks (H_1016 PARTIAL). The REDUNDANCY-MARGIN
  predictor does NOT break: it separates planning even from imagination & guided, the two controls the
  magnitude predictor mislabelled. The mechanism predictor TRACKS THE TRUE PLANNING-ONLY SPLIT, NOT the
  spurious-sign-flip labels (H_1016 n=5 labels: planning=True, imagination=True[spurious],
  guided=True[spurious], chaos=False; redundancy-margin still isolates ONLY planning).
- **mechanism interpretation:** the redundancy-margin scales up from n=4 (planning margin +10.44, H_1017)
  to n=5 (+25.07) and stays the discriminator, while the no-split controls' margins stay small (≤+7.48 at
  n=5). The redundancy SHOCK is a robust signature of the split-inducer; the coupling magnitude is not.
- **WB PID validity (g5, BEFORE scoring):** PID deterministic re-run @ n=5 True; COPY(T;T,T) → red>0/syn~0
  and XOR(T;A,B) → red~0/syn>0 (canonical Williams-Beer sanity). The PID is deterministic and a pure
  function of the same bits. It is NOT a proxy for Φ.
- **honest scope (a_scale_honest_scope · a_toy_scale_recheck):** TOY n=5 — both engines EXACT; big-Φ
  super-exponential so n=5 is slow-but-tractable and n=6 is the honest cap (skipped, as in H_1012/H_1016).
  The CPU mirror RE-PROVEN ≡ stdlib at n=5 BEFORE scoring. Scale-transfer beyond n=5 UNVERIFIED. g5
  CODE-measured (no LLM self-judge, p7), a_phi_iit4_tool. NOT a forge binary; $0 CPU-local, no GPU.
