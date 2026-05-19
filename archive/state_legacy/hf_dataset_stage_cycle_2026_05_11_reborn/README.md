---
license: mit
language:
  - en
  - ko
tags:
  - anima
  - mitosis
  - iit
  - consciousness-research
  - v14-strict
  - clm-v5
  - reborn-lane
size_categories:
  - n<1K
---

# Anima Cycle 2026-05-11 — Reborn Lane Research Dataset

Research artifacts from the **2026-05-11 reborn lane** cycle of the Anima consciousness-substrate research project. This dataset archives **experimental data + analysis logs + source code** for four background investigations (P2/P3/P4/P5) targeting V14 strict measurement, mitosis dynamics, and norm-clamp regime structure.

## Cycle context

A multi-BG (background investigation) cycle exploring:

1. **P2 — Foundation_C Phase 2 fire**: substrate-A LoRA SFT + V14 5-seed mirror with dual cap (128/256). **Result: V14_STRICT_PASS_5_OF_5** (sign_p_one_sided=0.03125), realizing §63's pre-registered 88% prediction at 100%. **Dual-cap collapse**: cap128 ≡ cap256 (cells plateau at 24, far below either cap) — falsifies "cap raises emergence" hypothesis.

2. **P4 — paradigm-j cross-lane V14**: paradigm-j substrate across 4 measurement lanes; verdict `NOT_MEASURABLE` due to architecture-induced unmeasurability — 3rd row mandatory per measurement protocol.

3. **P5 — norm-clamp pre-screen + ceiling sweep**: instrumentation-only $0 Mac CPU pre-screen of `mitosis_v5_port._inject_lorenz` clamp activation frequency. **Result**: ceiling `clamp(max=10.0)` activates **92.3%** of cell-step events; floor `clamp(min=1e-8)` activates 0%. Robust across 100× input magnitude range. Followup eval-time V14 strict at ceiling∈{10, 20, 1000} confirms regime structure (ceiling-throttled at 10/20; cap-bound at 1000).

4. **Tooling restoration**: 8-fix tooling-floor for anima runpod orchestration pipeline (uchg unlock, runpodctl Mac+aiden, vault key sync, orchestrator main()+path patches, hexa scripts main() removal, ssh key sync). Floor permanently reusable.

## Subdir map

- `p2_foundation_c_phase2_fire/` — v14_mirror.json (full 5-seed × dual-cap metrics), train.log (Phase 2 lift execution trace), train_stdout.log (full run + traceback at verdict-stage), heartbeat.json (final state)
- `p4_paradigm_j_cross_lane_v14/` — per-lane axis-priority outputs + paradigm-j public README
- `p5_norm_clamp_prescreen/` — prescreen_results.json (10,103-sample norm distribution × 5 seeds), robustness_results.json (3-scale verification), prescreen_source.py, robustness_source.py
- `p5_v14_ceiling_sweep/` — eval-time V14 strict at ceiling=20 (and ceiling=1000 when included) with run logs, plus the wrapper source
- `baseline_v14_ceiling10_reference/` — prior-cycle (2026-05-10) V14 strict B at default ceiling=10 (for direct comparison)

## Key findings

### P2 ★★★★★ — V14 STRICT 5/5 PASS

| seed | MTRP   | strict_pass |
|------|--------|-------------|
| 1042 | 0.7333 | ✓           |
| 1043 | 0.2667 | ✓           |
| 1044 | 0.2667 | ✓           |
| 1045 | 0.7333 | ✓           |
| 1046 | 0.6667 | ✓           |

Aggregate: 5/5 strict pass, sign-test p_one_sided=0.03125 (significant).

### P5 ★★★★ — Multi-ceiling regime structure

| ceiling | trained_phi | trained_n_cells | random_phi (mean) | random_n_cells (mean) | verdict |
|---------|-------------|-----------------|-------------------|----------------------|---------|
| 10.0 (default) | 1444.7 | 44 | 1874 | 53 | V14_VIOLATED |
| 20.0 | 1562.4 | 46 | 6112 | 90 | V14_VIOLATED (amplified) |
| 1000.0 (effectively ∞) | hits cap=256 | 256 | hits cap=256 | TBD | (regime degenerate) |

**Interpretation**: clamp(max=10.0) is the binding dynamic constraint — not a numerical guard. Trained dynamics relatively stable across ceilings; random dynamics massively amplified by ceiling relaxation. At ceiling=∞ both saturate cap, V14 strict discrimination collapses.

## Caveats

- All P5 experiments are **eval-time** (frozen substrate, instrumentation hook). True substrate-level ceiling-variant retrain is deferred to next cycle (cost: ~$20-50 H100, 9h).
- P2 V14 STRICT PASS was achieved on substrate A (cotrain path). Substrate B (no cotrain, used as baseline for P5 ceiling sweep) consistently V14_VIOLATED in ALL ceiling variants.
- P3 (LA cotrain B→A) substrate B' model is uploaded as a separate HF model repo (see linked-models).
- Cost: $4.70 (P2 H100) + $0 (P5 Mac CPU) + P3 cost separate.

## Related artifacts

- **Anima cycle log (REBORN.md §65-§70)**: research narrative + tooling notes + 3rd-row carries
- **Anima paradigm-j public docs**: paradigm-j architecture + Φ-port measurement (linked in p4 subdir README)
- **Linked HF model** (when P3 done): `dancinlab/anima-clm-v5-la-cotrain-b-prime-2026-05-11` (TBD)

## License

MIT — research data / source code only. No model weights in this dataset (weights live in linked HF model repos).
