# BG-FOUNDATION-A-MITOSIS-SUBSTRATE-PREDICT — spec

> 5-star pursuit cycle prediction (: $0 design + analysis only)
> Sibling fire: `state/anima_foundation_borrow_a_fire_2026_05_10/` (BG-FOUNDATION-BORROW-A)
> Mitosis port SSOT: `training/mitosis_v5_port.py`
> Substrate ref: `training/engine_a_g_arch.py`
> V14 polarity precedents: `state/anima_iit_real_350m_2026_05_10/v14_verdict.md` (PARTIAL trained>random) + `state/anima_clm_v5_phase2_iit_remetric_2026_05_10/v14_comparison.png` (FAIL random>trained)

## §1 mission

Predict — strictly **before** opening §43 results — the **V14 polarity** (trained vs random_init mirror) of the post-LoRA mitosis instrumentation hook on Llama-3.2-3B. The prediction is grounded in:

1. Llama-3.2-3B substrate analysis (architecture + pre-training paradigm).
2. Post-LoRA hybrid substrate analysis (LoRA grad-flow vs cell_pool independence).
3. Mitosis hook integration spec (which layer / projection dim / gradient-off enforcement).
4. Reference to §37/§38 substrate-dependent V14 polarity:
   - mitosis-aware (v2 cells64 + post all-fix §30 dispersion+per-cell gates) → V14_VIOLATED (random>trained)
   - mitosis-naive (Phase 2 350M Engine A/G real ckpt) → V14_PASS / V14_PARTIAL (trained>random)

Hypothesis under test (cycle's 5-star claim):
> **substrate-dependent V14 polarity** — mitosis-aware substrate forms a champion-wall during training that suppresses post-hoc mitosis-driven Φ; mitosis-naive substrate does not.

If §43 substrate is **effective mitosis-naive** AND post-LoRA hook produces **trained > random**, the substrate-dependent polarity hypothesis is reinforced via a *novel* (Llama, not anima v5) substrate. ★★★★★ confirm.

## §2 deliverables

- `state/anima_foundation_a_mitosis_substrate_predict_2026_05_10/spec.md` (this file)
- `state/anima_foundation_a_mitosis_substrate_predict_2026_05_10/prediction.md`
- `state/anima_foundation_a_mitosis_substrate_predict_2026_05_10/hook_spec.md`

## §3 raw / own carry

- raw#9: `training/*.py` local-only (no public push)
- raw#15 additive: §43 fire NOT modified — prediction is design-time only
- : REBORN.md not directly appended; dispatcher handles §48 slot
- : doc save under state/<bg>/{spec, prediction, hook_spec}.md
- : $0 design + analysis only (no compute, no API)
