---
license: cc-by-sa-4.0
tags: [anima, clm, akida, qat, int4, measurement-rung, negative-result]
---

# anima-clm-mid — CLM production measurement-rung (mid d512/L8/E8) AKIDA-envelope QAT

First **measurement-rung** quality proof for the anima CLM production roadmap
(CLM/P4_PRODUCTION_ROADMAP.md @L5/@L7). PRIVATE: measurement artifacts only
(loss/step-rate JSON + log + verdict), NOT a deploy ckpt.

- **rung**: mid (d_model=512 · n_trunk_layers=8 · n_experts=8) · 13,653,768 params
- **envelope**: weights int4-sym[-7,+7] per-channel STE · acts act_bits=4 · grads STE
- **fire**: runpod NVIDIA A40 · torch 2.1.0+cu118 · 3-arm (A/B/AB) × seed 42 × 2000 step
- **result**: CE 5.5444 (random ln256) → ~2.22 nats · step-rate ~25/s · no divergence

## Files
- `clm_mid_A_s42.json` · `clm_mid_B_s42.json` · `clm_mid_AB_s42.json` — raw per-arm result
- `clm_fire.log` — fire log
- `F-CLM-PROD-RUNG.txt` — verdict (verbatim)

## Honest scope (a_scale_honest_scope)
Measurement track ⊥ deploy chip-fit track. Toy two-lane corpus → no
production-quality / routing-diversity claim. Inference stays AKIDA-int4-only
(byte-identical chip transplant). External LLM 0 · foundation-borrow 0 (pure scratch).
