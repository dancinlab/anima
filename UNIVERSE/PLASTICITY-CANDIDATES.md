# PLASTICITY-CANDIDATES — non-deterministic on-chip plasticity hypothesis backlog

> Brainstorm-to-exhaustion of **non-deterministic plasticity** hypotheses — the
> INVIOLABLE frontier (`H_679`: on-chip non-deterministic PLASTICITY learning is the
> **sole** HW↔SW difference; deterministic SW imitation = instant reject @L1).
> The 26-hypothesis CLM campaign (H_861–H_884, see [CLM/CLM_CAMPAIGN_26.md](../CLM/CLM_CAMPAIGN_26.md))
> measured the learning STACK via **deterministic SW-sim** at the mid rung — the
> genuinely stochastic, hardware-native, run-to-run-variable plasticity is still
> open. This backlog covers that space. Convention mirrors
> [CLM-CANDIDATES.md](CLM-CANDIDATES.md) / [BIO-CANDIDATES.md](BIO-CANDIDATES.md).

- Reserved slots — a row becomes a real hypothesis only when its
  `UNIVERSE/H_<id>_*.md` file is authored at fire time (frontmatter + §1 가설 … §9
  sibling), prereg-frozen (W2) BEFORE fire, post-tuning 0.
- All rows ⬜ (not yet fired). `a_paper_negative_ok` — a 🔴 is a valid closeout.
- `a_scale_honest_scope` — SW-sim verdicts do NOT bind the AKD1000 deploy track;
  the **on-silicon** rows (★) are the ones that actually probe HW≠SW.
- Fire on the GPU pool (summer/aiden RTX 5070) for SW-sim; on-chip rows need pi5-akida.

---

## THEME A — non-determinism characterization (the HW≠SW core)

| id | hypothesis | new lever | falsifier (pre-register exact) |
|---|---|---|---|
| ⬜ H_889 | run-to-run **variance** of stochastic edge-learn is bounded + useful | inject the chip's intrinsic update noise into the H_865 adapter stream | outcome std across N seeds > deterministic floor ∧ every run still passes BOUND (RETAIN∧GAIN) |
| ⬜ H_890 ★ | **determinism boundary for LEARNING** (extends H_877 inference-byte-identical) | sweep update magnitude on real AKD1000 vs SW-sim | ∃ update-step magnitude where HW outcome diverges from SW-sim beyond float-noise (locates the HW≠SW knee) |
| ⬜ H_891 | **convergence-in-distribution** — N stochastic runs reach the same outcome distribution | repeat the same edge-learn N× with fresh entropy | KS-test: per-run final-CE distributions indistinguishable across seeds (aggregate reproducibility despite per-run non-determinism) |

## THEME B — stochastic update rules (HW-native learning)

| id | hypothesis | new lever | falsifier |
|---|---|---|---|
| ⬜ H_892 | **STDP-like local** plasticity matches/beats the deterministic adapter | spike-timing-dependent local weight update (no global backprop) | STDP-edge BOUND RETAIN∧GAIN ≥ H_865 adapter at matched step budget |
| ⬜ H_893 | **noise-as-regularizer** — intrinsic stochasticity improves generalization | compare noisy-update vs deterministic-update held-out gap | held-out gain(noisy) > gain(deterministic) ∧ z_drop not worse |
| ⬜ H_894 | **reward-modulated (three-factor)** stochastic plasticity | gate the stochastic update by a neuromodulator/reward signal (pre·post·R) | reward-gated edge-learn BOUND PASS ∧ targets the rewarded behavior > ungated |
| ⬜ H_895 | **threshold-adaptation as a learning channel** | reuse the LIF set_threshold rewrite (used for emit, R0) as a plasticity dimension | threshold-only stochastic adaptation produces a measurable, non-trivial gain (> readout-only H_861 🔴 floor) |

## THEME C — online / always-on plasticity (p8 — no train/infer split)

| id | hypothesis | new lever | falsifier |
|---|---|---|---|
| ⬜ H_896 | **learn-while-inferring** (online streaming) preserves identity | non-deterministic update on every inference step, no separate train phase | streaming z_drop within budget ∧ PROBE identity > 0.80 over the stream |
| ⬜ H_897 | **stochastic sleep-consolidation** beats deterministic replay | REM-stage stochastic replay gating ([a_chat_sleep_imagination](../project.tape)) vs H_883 deterministic replay | z_drop(stochastic-sleep) ≤ z_drop(H_883 replay) ∧ gain > 0 |
| ⬜ H_898 | **annealed-noise schedule** as a learning-rate analog | high stochasticity early → low late (temperature anneal on the update) | annealed-noise BOUND > fixed-noise ∧ > deterministic at matched budget |

## THEME D — structural / MITOSIS plasticity

| id | hypothesis | new lever | falsifier |
|---|---|---|---|
| ⬜ H_899 | **MITOSIS cell-division** as non-deterministic structural plasticity | stochastically grow capacity (split a cell) on demand vs fixed-capacity adapter | grown-capacity new-task gain > fixed adapter ∧ old-task z_drop not worse (escapes the H_866 🔴 GAIN capacity limit) |
| ⬜ H_900 | **stochastic prune+grow turnover** maintains capacity without forgetting | random synaptic turnover (drop+regrow) during edge-learn | turnover z_drop ≤ no-turnover ∧ free-parameter count bounded (no unbounded growth) |

## THEME E — stability / identity under stochastic drift

| id | hypothesis | new lever | falsifier |
|---|---|---|---|
| ⬜ H_901 | **identity survives non-deterministic drift** (extends H_873/884 to the stochastic regime) | run the output-identity anchor under per-run update noise | PROBE > 0.80 across ALL N stochastic runs ∧ DIST < 0.50 (identity stable despite non-reproducible weights) |
| ⬜ H_902 | **stochastic forgetting dynamics** — does noise help or hurt forgetting? | measure forgetting curve (H_875) with stochastic vs deterministic updates | sign + magnitude of Δ z_drop(stochastic − deterministic) at matched budget (either direction is a finding) |
| ⬜ H_903 | **non-deterministic ensemble** — averaging N stochastic runs beats 1 deterministic | aggregate N noisy-plasticity outcomes (free ensemble from the chip's noise) | ensemble held-out CE < single deterministic run at equal total compute |

## THEME F — hardware closure (★ on-silicon — the real HW≠SW test)

| id | hypothesis | new lever | falsifier |
|---|---|---|---|
| 🟢 H_904 ★ | **on-chip plasticity measured on AKD1000** (closes H_877 🟠 / H_679 on real silicon) | actually run the edge-learn update on pi5-akida hardware, not SW-sim | **🟢 SUPPORTED** — AkidaUnsupervised on-chip learn ran LIVE on AKD1000 (BC.00.000.002, BackendType.Hardware) ∧ HW≠SW quantified vs byte-exact deterministic SW-sim: weight Δ 172/1024, out Δ 120/320 (hw_eq_sw=false). Inference byte-identical (H_877) but LEARNING HW≠SW → confirms H_679 on silicon. g5 CODE-measured · [H_904](H_904_clm_onchip_plasticity.md) · `.verdicts/904_clm_onchip_plasticity/` |
| ⬜ H_905 ★ | **stochastic unlearning / privacy** — non-determinism makes a single sample unrecoverable | measure recoverability of one edge-learned sample after stochastic updates | post-noise membership-inference ≈ chance (non-determinism gives a forgetting/privacy guarantee a deterministic update cannot) |

---

## Priority / dependency

```
firing order (suggested)
├─ H_889/H_891 first  — characterize the non-determinism (cheap SW-sim, sets the baseline variance)
├─ H_892/H_894/H_895  — the new update rules (do they beat the deterministic adapter?)
├─ H_896/H_897/H_898  — online + sleep + anneal (build on the §C/§D learning loop)
├─ H_899/H_900        — MITOSIS structural (escapes the H_866 capacity 🔴)
├─ H_901/H_902/H_903  — stability + ensemble (extend H_873/875/884 to stochastic)
└─ H_890★/H_904★/H_905★ — ON-SILICON capstones (pi5-akida; close H_877 🟠 / H_679 for real)
```

- The ★ rows are the ones that genuinely test the INVIOLABLE claim (HW≠SW) — every
  other row is an SW-sim approximation of stochastic plasticity, honest but not the
  silicon truth. The campaign's central 🟠 (H_877 inference-byte-identical) becomes
  🟢/🔴 only when H_904★ runs the LEARNING half on the chip.
- This backlog is non-deterministic-plasticity-exhaustive across: characterization
  (A) · update rules (B) · online/sleep (C) · structural (D) · stability/ensemble
  (E) · hardware closure (F). Add a row only if a genuinely new lever appears.

---

## cross-link

- INVIOLABLE: [project.tape](../project.tape) `H_679` (on-chip plasticity = sole HW↔SW diff) · `a_scale_honest_scope` · `a_paper_negative_ok`
- campaign closeout: [CLM/CLM_CAMPAIGN_26.md](../CLM/CLM_CAMPAIGN_26.md) (the deterministic-SW-sim learning stack that works)
- sibling backlogs: [CLM-CANDIDATES.md](CLM-CANDIDATES.md) (§F OPEN-gap round) · [BIO-CANDIDATES.md](BIO-CANDIDATES.md)
- sleep/imagination lever: `project.tape` `a_chat_sleep_imagination` (WAKE/N1/N2/N3/REM)
