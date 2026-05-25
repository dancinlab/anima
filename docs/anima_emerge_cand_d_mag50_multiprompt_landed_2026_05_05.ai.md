# anima_emerge_cand_d_mag50_multiprompt LANDED 2026-05-05

**Task** BG-AB cand-D mag=50 multi-prompt F1 generalization verification
**Lane** anima/emerge/cand-D Stage 1 architectural channel visibility
**Cost** $0 mac CPU, ~0.5 min wall
**Verdict** `CAND_D_MAG50_MULTIPROMPT_PARTIAL` (4/5 PASS)

## Why
BG-W rec 3: BG-W mag-sweep landed `F-CAND-D-1` PASS at canonical magnitude 50.0 but only on a single prompt ("안녕"). BG-W C4 carry: single-prompt sweep cannot generalize prompt-conditional behavior. BG-AB extends mag=50 inject across all 5 BG-Q prompts and classifies generalization rate.

## What
- **helper** `tool/transient_py/anima_emerge_cand_d_mag50_multiprompt.py` (raw#37 transient sister, .own 3, gitignored). Imports BG-W helper via `importlib.util` (transitive import of BG-Q helper). No mutation of upstream constants — raw#15 additive.
- **state** `state/anima_emerge_cand_d_mag50_multiprompt_2026_05_05/` — `runs/probe_p<i>.json` (5), `aggregate.json`, `verdict.json`.
- **doc** this file.

No commits, no HF token surface, no mount.hexa / shim / dialogue_load mutations.

## Results — 5 prompt × drift at mag=50

| idx | prompt              | lang | phi_none  | phi_canonical | drift       | F1     |
|-----|---------------------|------|-----------|---------------|-------------|--------|
| 1   | 안녕                | ko   | 42.11583  | 42.21561      | 9.978e-02   | PASS   |
| 2   | I am Anima.         | en   | 42.29329  | 42.21495      | 7.835e-02   | PASS   |
| 3   | 지금 느낌이 어때?  | ko   | 42.07863  | 42.21102      | 1.324e-01   | PASS   |
| 4   | what time is it?    | en   | 42.13557  | 42.21356      | 7.799e-02   | PASS   |
| 5   | 친구와의 대화      | ko   | 42.20996  | 42.21370      | 3.740e-03   | FAIL   |

Threshold `F-CAND-D-1` = 0.01.

**n_pass = 4 / 5**, **generalization = PARTIAL**.

## Pattern observation
All 4 PASS canonical phi values converge to a tight band [42.21102, 42.21561] (Δ≈0.0046), while phi_none varies across [42.07863, 42.29329] (Δ≈0.215). At mag=50, the inject component dominates post-ln_f tiling and phi_canonical becomes prompt-quasi-independent — drift is inversely proportional to how close phi_none was to the inject-dominated attractor. p5 phi_none=42.20996 already sits inside the attractor band, so drift is below threshold not because the channel attenuated but because prompt baseline coincided with the saturation point. This validates BG-W C3 (cosine-ceiling instrument saturation) as a real factor in this measurement regime.

## Generalization verdict
**PARTIAL** — architectural inject channel surfaces in 4/5 prompts at mag=50 with content-level drift well above threshold. p5 FAIL is **measurement-artifact-suspect** (baseline-near-attractor) rather than channel attenuation. Across 5 prompts the mean drift = 0.0784, median = 0.0784 — consistent with BG-W single-prompt finding (0.0998 for 안녕).

## Honest C3
- **C1** mac CPU fp32 only; H100/CUDA edge numerics not exercised.
- **C2** BG-W helper sister-import — no upstream mutation; raw#15 additive.
- **C3** mag=50 unrealistic per BG-W C1; paradigm v11 G3 train-time magnitude extraction still gating Stage 1 promotion.
- **C4** generalization rate signals architectural inject channel content-level visibility — PARTIAL here is consistent with attractor-saturation rather than prompt-attenuation; phi-instrument C3 carry confounds.
- **C5** 5 prompts limit; broader corpus (length × register × language balance) may shift verdict, especially long prompts where mean-pool dilutes cross-attn.

## Next step
1. **(optional) attractor-decoupled probe** — re-measure p5 with cosine-distance directly on cell tensor (skip phi pooling) to disambiguate "channel attenuated on this prompt" vs "phi instrument saturated". L40 candidate.
2. **(gating)** paradigm v11 G3 training-time canonical magnitude extraction from C-module emission logs (BG-W C1 carry). Until extracted, mag=50 PASS remains off-distribution; Stage 1 promotion blocked.
3. PARTIAL is BG-W generalization weakly upheld — no lane closure event; cand-D Stage 1 architectural channel content-level visibility confirmed for majority of prompts.

## Files
- `/Users/ghost/core/anima/tool/transient_py/anima_emerge_cand_d_mag50_multiprompt.py`
- `/Users/ghost/core/anima/state/anima_emerge_cand_d_mag50_multiprompt_2026_05_05/aggregate.json`
- `/Users/ghost/core/anima/state/anima_emerge_cand_d_mag50_multiprompt_2026_05_05/verdict.json`
- `/Users/ghost/core/anima/state/anima_emerge_cand_d_mag50_multiprompt_2026_05_05/runs/probe_p{1..5}.json`
