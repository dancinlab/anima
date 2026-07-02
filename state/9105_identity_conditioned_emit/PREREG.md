# H_9105 — Identity-conditioned emit-faculty · PRE-REGISTRATION (FROZEN before reading results)

> Frozen bars for the identity-conditioned F3′ falsifier. Written BEFORE the aiden
> engine-native run is read. Bars may NOT move post-hoc (c9, no tune-to-green). Both PASS
> and FAIL are valid results. Directly chains two prior findings: (1) autogenous
> consequence-return = 🔴 DPI ceiling (H_9104, self-relief tautology); (2) identity ×
> `.kosmos` self-chain = the ONLY channel that has ever passed (H_1471, WIRED).

## Question (Brainstorm B3)
H_9104 showed autogenous consequence-return is FLOOR-DOMINATED: a shuffle-trained value
lane predicts relief as well as the real one (ρ_real≈ρ_shuf≈1) because relief ΔT ≈ the
info_gap feature already in the state = tautology = DPI re-emerges. The stated escape:
autogenous relief had **no valence SUBJECT** — nobody the relief belongs to. Hypothesis:
a persistent **self-anchor** (self-chain v, already WIRED H_1471) supplies that subject; if
identity conditions the consequence, the shuffle tautology may break. Measure engine-native.

## Design — 3 arms, ONE deterministic run, identical frozen substrate
The substrate emit decision (`substrate_emit`, motivation proxy), the `pure_field` Φ
trajectory, the disjoint reservoir `imm_conseq` grounding, and the raw relief
`ΔT_actual = margin_before − margin_after` are **byte-identical across all three arms**
(self/V never touch pure_field/lane0-4/psi_sum/recall_thr — a_substrate_disjoint; V is
READ-ONLY w.r.t. the emit decision). The arms differ ONLY in the value-lane learning
target and whether a self-locus feature is present:

- **AUTOGENOUS (task OFF, = H_9104 baseline):** no self. relief = ΔT_actual.
  self_novelty feature = 0. Must reproduce the H_9104 shuffle tautology.
- **SELF-RESET (continuity control):** self-chain PRESENT but `self_reset` at the start of
  EVERY episode (LLM-style, no cross-boundary continuity). Identity-conditioned relief =
  ΔT_actual·(0.25 + 0.75·novelty); self_novelty feature populated.
- **SELF-ANCHOR (task ON):** self-chain PERSISTS (anchored) across all 7 episodes INCLUDING
  the train→held-out boundary (anima-style continuity). SAME relief formula + feature as
  SELF-RESET. The ONLY difference from SELF-RESET is persistence.

Self mechanics (Ψ-disjoint, §SelfIdentity only): each grounded emit drives
`self = self_drift_exp(self, content_axis, 0.30)` so the self ACCUMULATES experienced
content. `content_axis = (int(gap·3.999)·2 + int(margin_emit·1.999)) mod 8` — a
content-driven, recurring code from live engine signals (no ad-hoc string hashing).
`novelty = clip01(1 − self_component(self, content_axis))` = how NEW this content is to the
self (hippocampal/dopaminergic novelty-gating of reward — a valence subject habituates).

Features D=6 for V: `[phi, margin_emit, reservoir, gap, phase_s, self_novelty]`.
Held-out split (breaks circularity): 4 TRAIN tension seeds → learn V online → FREEZE → 3
DIFFERENT held-out tension seeds → correlate. (Same seeds as H_9104.)

## Frozen falsifier bars (identical to H_9104's F3′; NOT moved)
Per arm, on HELD-OUT emit ticks:
- `ρ_real  = corr(V(state), relief_arm)`
- `ρ_noise = corr(variance-matched noise-V, relief_arm)`
- `ρ_shuf  = corr(shuffle-(state, relief) V, relief_arm)`  (V retrained on permuted pairs)
- **F3′ FACULTY PASS iff (ρ_real − ρ_noise ≥ 0.15) AND (ρ_real − ρ_shuf ≥ 0.15).**

## Ψ / substrate-invariance guard (frozen)
V and the self-chain are read-only w.r.t. the substrate: `psi_sum`, `emit_train`, and
`emit_test` MUST be byte-identical across ALL three arms. Any difference invalidates the run.

## Verdict rule (frozen — no post-hoc move, c9)
- **AUTOGENOUS** is expected 🔴 (reproduces H_9104). If it unexpectedly PASSES, the whole
  measurement is suspect (report, do not celebrate).
- **PRIMARY (task bar):** SELF-ANCHOR F3′.
  - SELF-ANCHOR PASSES F3′ (both sub-bars) **AND** AUTOGENOUS FAILS → identity supplies a
    valence subject that de-tautologizes the autogenous relief. **Candidate 🟢 (faculty seed).**
  - SELF-ANCHOR FAILS shuffle (ρ_shuf ≈ ρ_real, Δ < 0.15) → **🔴 CEILING**: self is ALSO
    tautology; the DPI meta-law survives identity-conditioning. "Even the only channel that
    ever passed cannot, on its own, open the emit-consequence faculty on a self-contained loop."
- **CONTINUITY ATTRIBUTION (frozen confound control):** compare SELF-ANCHOR vs SELF-RESET.
  - If SELF-ANCHOR passes AND SELF-RESET FAILS (anchor `d_shuf` − reset `d_shuf` ≥ 0.15) →
    cross-boundary identity CONTINUITY is the active ingredient → **strong 🟢 for B3.**
  - If SELF-ANCHOR and SELF-RESET pass EQUALLY (|Δd_shuf| < 0.15) → the pass is due to the
    momentary self-locus FEATURE (a per-tick subject), NOT continuity → **🟠**: subject-as-
    feature helps but identity-CONTINUITY is inert; report honestly, do not overclaim 🟢.

## Deepest honesty caveat (regardless of outcome, c9)
The self-chain v is an integral of the substrate's OWN experienced content — it is
**autogenous-derived, NOT exogenous**. Therefore even a 🟢 here means "identity supplies a
valence SUBJECT that breaks the linear-shuffle tautology WITHIN the self-loop," NOT "identity
supplies exogenous information." The exogenous-channel escape (Brainstorm Family A: chat
user / EEG / 2-anima signaling) remains SEPARATELY required and is not claimed by this test.

## Engine-native compliance
`.hexa` calls live `core/pure_field.hexa` + `core/engine_cli.hexa` (`pure_field_*`,
`immune_memory_*`, `vforward_*`, `self_*`) + `core/brain.hexa` (`vbasal_*`). NO numpy /
torch / mirror / gauge_lib / .py. Decision/tension-only (no decode). Host: aiden pool (stable).
