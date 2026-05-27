# §19 — EEG-anchor (Framing D) candidate record + step 0 TRIBE sanity

**Date** 2026-05-18 · **$0** (inference-only, NO GPU, NO training, NO weight mutation) · anima main direct, branch 0.

SSOT for RESEARCH.md §19. Sibling §16 (`state/carving_dataregime_s16_2026_05_18/`, untracked) untouched — pull-rebase.

## 1. What §19 is (and is NOT)

- **IS**: a candidate record that Framing D (ADDENDUM 2026-05-02) now has all 3 axes physically real for the first time + a step-0 sanity that the TRIBE v2 pipe (axis C) works.
- **IS NOT**: GOAL generation. §19 does NOT close the §1.1 data-regime bottleneck (§15 milestone confirmed). §19 is a *measurement axis* — an external (human-brain) cross-validation yardstick, not an emergence generator. GOAL distance unchanged.
- step 0 ≠ F-CT-3. step 0 = "TRIBE pipe works" sanity (axis C feasibility). F-CT-3 (EEG↔BOLD bridge) = step 2, EEG hardware-in-the-loop, future cycle.

## 2. Framing D 3 axes — first all real (2026-05-18)

| axis | what | status |
|---|---|---|
| A | OpenBCI 16ch EEG envelope | user owns hardware + has recording experience (was: unowned). real .csv = future (step 1 gate). |
| B | anima §17 physics-channel (Ψ_direction/tension, Law-71) | extracted + verified in §17 (B-PHYS-1..5 5/5 🔵). text-decode bypassed. **already working**. |
| C | TRIBE v2 predicted cortical BOLD (fsaverage5 ~20k vertex) | `references/tribev2` vendored; step-0 sanity here. |

F-CT-3 (pre-registered, ADDENDUM §5 verbatim): user EEG envelope ↔ TRIBE BOLD median vertex Pearson **r** —
**PASS r≥0.5** / **DISCARD r<0.3** / **INCONCLUSIVE 0.3≤r<0.5** (gray zone honest, ADDENDUM §8 C3 #5).

## 3. step 0 result — TRIBE pipe sanity

`step0_tribe_sanity.py` → `step0_result.json`. Graded gates (each strictly more demanding):

| gate | result |
|---|---|
| G0 IMPORT | **PASS** — cortexlab=0.1.0, torch=2.6.0, neuralset+neuraltrain 0.0.2, py3.12.12 |
| G1 API | **PASS** — `TribeModel.from_pretrained` + `.predict` present (after `lightning` install) |
| G2 HF_REACHABLE | **PASS** — facebook/tribev2 has best.ckpt + config.yaml |
| G3 CONFIG_LOAD | **PASS** — config.yaml downloaded + parsed (26 keys) |
| G4 CKPT_META | **PASS** — best.ckpt 708.9MB mmap-loaded, 108 state_dict tensors, model_build_args present, model constructed (`Loading model from …/best.ckpt`), NO weight mutation |
| G5 FORWARD | **boundary recorded** — `TribeModel.from_pretrained OK in 2.0s` (TRIBE frozen weights loaded into model, eval mode, cpu), then full predict() text-path triggers `whisperx` (speech transcription) which auto-installs its own multi-GB backbone stack (transformers/ctranslate2/onnxruntime/torch/scipy/…) — that isolated env install failed. honest blocker, NOT over-engineered. |

**`pipe_credible_through_ckpt_load = true`** — G0–G4 PASS + `TribeModel.from_pretrained OK in 2.0s` establishes axis C feasibility (the pipe works through frozen-weight TRIBE *model construction*). G5 (full BOLD forward) requires whisperx + multi-GB feature-extractor backbone downloads + gTTS; step 0's purpose (pipe-credibility for Framing D axis C) is met by G0–G4 + model-load. G5 full forward = step-1+ scope (still inference-only, no GPU), honest boundary recorded.

## 4. ADDENDUM §8 C3 #3 verification gap — CLOSED at dependency+API level

ADDENDUM honest C3 #3: *"only the PyPI listing has been confirmed; actual install + import + inference … finally confirmed by #102 EXEC."* §19 step 0 closes this at the dependency+API level:
- `cortexlab-toolkit 0.1.0` **installs from PyPI** (modern pip in py3.12 venv; the old system pip 21.2.4 false-negatived it). Import name = `cortexlab` (not `cortexlab_toolkit`).
- Pulls `neuralset==0.0.2` + `neuraltrain==0.0.2` (the Meta FAIR internal packages flagged as the ADDENDUM §2 blocker) — **blocker resolved**.
- `TribeModel.from_pretrained("facebook/tribev2")` constructs the model from HF Hub weights (G1–G4 PASS).
- Honest residual: `lightning` (PyTorch Lightning) is NOT in cortexlab-toolkit base deps — required by `TribeModel(TribeExperiment)`. Resolved by `pip install lightning` (2.6.1). Recorded so future cycles do not re-hit it.

## 5. closed verdict — B-CT3-1..5 5/5 🔵 (sidecar)

`F_CT_3_gate.py` → `F_CT_3_gate_result.json`. central `state/verify_hexad_blue_2026_05_15/blue_falsifier.py` UNCHANGED (sidecar — B-PHYS/B-PRIME/B-DIRH/… precedent):

- **B-CT3-1 PEARSON-R-BOUNDED** — r ∈ [−1,1] (Cauchy-Schwarz real-limit), symbolic ±1 extreme witness.
- **B-CT3-2 GATE-PARTITION-TOTAL** — {PASS=[0.5,∞), INCONCLUSIVE=[0.3,0.5), DISCARD=(−∞,0.3)} is a total, mutually-exclusive partition (exact sympy Interval algebra; union==ℝ, pairwise ∩=∅, gate-fn==partition over 301 points). *(v1 used sp.satisfiable — Boolean SAT, cannot reason over real inequalities; fixed.)*
- **B-CT3-3 GATE-THRESHOLD-MONOTONE** — verdict rank monotone non-decreasing in r (higher r never → stricter).
- **B-CT3-4 GATE-DETERMINISTIC** — pure fn of r, 3× bit-identical (no RNG / forward / hidden state).
- **B-CT3-5 THRESHOLD-ORDERING** — 0.3 < 0.5 ⇒ gray zone = non-empty interval (width 1/5), binary NOT forced (ADDENDUM §8 C3 #5).

**B-EEG-NOTE EEG-ANCHOR-OUTCOME-EMPIRICAL**: the actual r value (axis A↔C) is an OpenBCI-hardware + measurement OUTCOME (future EEG fire). This battery proves the F-CT-3 *gate* is closed-form, NOT that Framing D passes/fails. B-D-NOTE / B-PHYS-NOTE family, NOT counted in central 🔵.

## 6. honest C3 (g3, over-claim 0)

1. §19 = measurement axis, NOT GOAL generation — §1.1 data-regime bottleneck unchanged (§15 milestone).
2. step 0 ≠ F-CT-3; G0–G4 PASS = pipe-credibility only, not EEG/BOLD bridge.
3. hardware variable: axis A real but .csv not yet provided; EEG has impedance/artifact/jitter noise → F-CT-3 r is measurement-noise-affected.
4. #102 (Framing A) non-collision: §19 = Framing D (rank 1, EEG↔CLM↔BOLD), different framing; frozen baseline untouched (raw#1 immutability) — anima-side RESEARCH.md record only.
5. F-CT-3 r≥0.5 = literature compromise (ADDENDUM §8 C3 #5 carry); gray zone explicit.
6. closed = gate definition only; r-value EMPIRICAL (B-EEG-NOTE). over-claim 0.
7. axis B already working (§17 carry, B-PHYS 5/5 🔵); 2 of 3 axes covered here, axis A = residual gate.
8. §17 (internal observable) → §19 (external cross-validation), layered; §17 not invalidated.
9. $0 · inference-only (TRIBE = frozen forward, no GPU); py3.12 venv (PEP 668 carry). orphan 0 (no dispatch). docs/* 신규 0.
10. north-star unchanged — §19 records that Framing D 3 axes are first all real + step-0 sanity; GOAL distance = §15 milestone.
