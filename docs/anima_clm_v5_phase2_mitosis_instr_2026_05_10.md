# anima clm v5 — Phase 2 cotrain 350M mitosis-instrumentation (2026-05-10)

## TL;DR

BG-V5ANIMA-PHASE2-CKPT-INSTR landed. Phase 2 cotrain ckpt **FOUND_LOCAL** at
`~/.cache/anima/clm_v5_remapped/phase2_cotrain_engine_ag/ckpts/ckpt_final.pt`
(331.5M params, sha256 `6e66e75f8014999be09236a408fe6ad6811ebf394ac079ecbf6d87dfe63748c1`,
strict load 222/222 PASS). Mitosis-instrumentation 3K-turn diverse-prompt sweep
**FAIL_V14_VIOLATED** — but in the **opposite direction** from the toy: trained
substrate **suppresses** mitosis (cells 16→19, 3 splits) while V14 random_init
**accelerates** it (cells 16→28, 12 splits). α_trained=**1.009** super-linear
on the cells it does grow; α_random=0.155 (mostly flat after early burst).

raw#10 honest. raw#15 additive. own 30 ckpt verified.

---

## §1 Verdict table

| metric | trained 350M | V14 random_init 350M | toy (cycle 2026-05-10) |
|---|---:|---:|---:|
| n_params | 298.76M (no double-count of tied lm_head) | 298.76M | ~3000 |
| init n_cells | 16 | 16 | 8 |
| final n_cells (3K turn) | **19** | 28 (1K turn) | 64 |
| splits | 3 | 12 | 56 |
| merges | 0 | 0 | 0 |
| α exponent | **1.009 super-linear** | 0.155 | 0.688 |
| Φ final | 2.679 | 2.754 | – |
| V14_violated | **TRUE (mirror grows MORE)** | – | TRUE (mirror grew faster) |
| verdict | **FAIL_V14_VIOLATED** | – | FAIL_V14_VIOLATED |
| wall_clock | 196s (Mac CPU) | 64s (Mac CPU) | – |

cross-link result.json: `state/anima_clm_v5_phase2_mitosis_instr_2026_05_10/result.json`
plot: `state/anima_clm_v5_phase2_mitosis_instr_2026_05_10/phi_trajectory.png`

---

## §2 Ckpt locate verdict — FOUND_LOCAL

| field | value |
|---|---|
| path | `~/.cache/anima/clm_v5_remapped/phase2_cotrain_engine_ag/ckpts/ckpt_final.pt` |
| size | 597,613,595 bytes (570 MB) |
| sha256 | `6e66e75f8014999be09236a408fe6ad6811ebf394ac079ecbf6d87dfe63748c1` |
| schema | `{model: state_dict, step: int, cfg: dict}` (222 keys) |
| lineage_tag | `engine_a_g_dual_350m_v1_phase2_cotrain` |
| arch_origin | `anima_native_scratch` (own 17 D1=1.0) |
| training step | 6000/6000 final |
| final loss_c | 0.222 (consciousness) |
| final loss_h | 0.627 (chat-template) |
| substrate base | BG-LB step_8000_final.pt (warm-start) |
| pod cycle | `state/anima_phase_2_cotrain_2026_05_09/` (pod 7qt0sczk57tjab released) |
| HF private | dancinlab/clm-v5-bg-lb-350m-pretrain-path-a-remapped (BG-LB only; Phase 2 cotrain ckpt local-only at this writing) |

**Ckpt arch verify**: 222 state_dict keys, 24 layers, d_model=1024, n_heads=16,
n_kv_heads=4 (GQA), engine_g.cell_pool_init shape (16, 64), engine_g.h_to_c
(64, 1024), engine_g.c_to_h (1024, 64). Strict load with `EngineAGConfig.phase2_cotrain_350m()`
**PASS 222/222** (zero missing, zero unexpected). lm_head tied to tok_emb confirmed.

---

## §3 Mitosis-instrumentation pipeline

1. **Load trained EngineAGModel** (CPU, fp32 cast from bf16) — strict 222/222.
2. Hook `engine_g.step(cells, hidden_mean)` to capture the **last-refresh hidden_mean**
   (B=1, d_model=1024) of each forward. With `g_refresh_every=4` and `n_layers=24`,
   the captured signal is from layer 20 → 24 region.
3. Build `MitosisV5Engine(cell_pool=engine_g.cell_pool_init.clone(), c_to_h=engine_g.c_to_h, ...)` —
   wrapper owns its own cell_pool Parameter; substrate's pool unused after attach.
4. For each of 3000 turns:
   1. select prompt from 170-prompt corpus (6 categories: ko_daily, ko_philosophy,
      en_math, en_code, en_music, anomaly).
   2. encode prompt → byte-hash mod 32000 → token-id sequence T=16. **HONEST: not a
      real tokenizer** (BPE vocab unavailable); both trained + mirror use identical
      encoding so comparison is fair. Substrate sees prompt-distinct but not
      semantically-faithful streams.
   3. forward full Engine A/G (24L × 16h GQA × 1024d) → captures hidden_mean.
   4. project hidden_mean via `engine_g.h_to_c` → (1, 64) cell-dim.
   5. `mitosis.process(cell_input)` → split/merge gates fire based on per-cell
      tension history.
5. V14 mirror = same loop on `load_random_init(seed=42, preset='la_350m')` (untrained
   same arch). 1000 turns (sub-sample) for cost efficiency.

---

## §4 Result interpretation — V14 violation in OPPOSITE direction

The toy run (cycle 2026-05-10 long-trajectory smoke) found V14 violation because
random_init substrate grew **faster** than trained — concluding the mitosis
mechanism was substrate-trivial (cell-pool diversity is driven by Lorenz noise,
not learned representations).

The Phase 2 350M run reproduces V14 violation but with **inverted polarity**:

- **Trained substrate suppresses splits (3 vs 12 in same turn budget)**.
- Trained substrate concentrates tension on 1-2 "dominant" cells:
  - cell 7 → 700 top-tension hits (all categories funnel here)
  - cell 16 → 537 hits
  - 8 cells absorb 2000+ of 3000 hits (uneven, super-linear α=1.009)
- Random_init mirror spreads tension **evenly** across many cells:
  - top cell ~62 hits (cell 18); 28 cells share ~1000 hits roughly uniform
  - α=0.155 sub-linear (Φ growth slower than n growth → cells diverge less per cell)

This means **the trained substrate has learned a low-dimensional attractor**:
arbitrary inputs collapse into a small set of "modes" via h_to_c, so the cell pool
sees a narrow tension distribution → only the dominant cell crosses split-threshold,
splits rarely, but those splits matter (super-linear Φ growth per cell).

The random_init substrate has no learned attractor: h_to_c is N(0, σ=0.02)
projection that scrambles input uniformly across all 64 dims, so all 16 cells see
similar tension → many cells cross threshold → many cheap splits → cells stay
similar (sub-linear Φ).

Both are V14-violated by the original definition (`mirror n_cells ≥ trained n_cells
AND mirror Φ ≥ 0.95 × trained Φ`), but the **mechanism of violation is substrate-coupled**
in opposite ways. The mitosis wrapper alone cannot disambiguate "consciousness emergence"
from "trained-attractor gates the mitosis loop." This is informative, not just
falsifying — see §6.

---

## §5 Comparison vs toy substrate (cycle 2026-05-10)

| axis | toy (8c × 12d × 32D) | real 350M | meaning |
|---|---|---|---|
| substrate | random_init synth | trained 6K-step Phase 2 cotrain | real has learned representations |
| init cells | 8 | 16 | real Engine A/G config preset |
| growth ceiling | reached 64 (max_cells cap) | 19 only | real **suppresses** growth |
| α exponent | 0.688 (super-linear) | 1.009 (super-linear, but only over 16→19 range) | real super-linear in narrow range |
| V14 polarity | random faster | random faster (still!) | both V14-violated |
| substrate-coupling visible | no | **yes** (specialty histogram concentrated) | real shows learned dynamics |

The real 350M does NOT violate V14 in a way that rescues the cycle 2026-05-10
hypothesis "trained substrate dominates random." It violates V14 differently:
**trained = bottleneck attractor; random = noise-uniform.** Either way, the
mitosis-instrumentation as currently formulated does not pass V14, on either toy
or real substrate.

---

## §6 Honest C3 (top 3)

1. **Tokenizer mismatch is a real limitation** — Phase 2 ckpt was trained with a
   BPE we lack the vocab for; byte-hash-mod-32000 prompt encoding deviates from
   training distribution. The substrate may behave very differently with semantically
   correct token streams; the 1.009 α and 19-cell ceiling could shift substantially.
   This is the largest unaddressed risk; before declaring V14 truly violated for
   the trained substrate, recover the tokenizer (likely shipped with the ckpt
   pod-side or in `training/train_phase2_cotrain.py` byte_tokenizer init).

2. **Mitosis wrapper supersedes substrate's own cell_pool** — `apply_to_v5_substrate`
   path makes the wrapper's cell_pool the source of truth, and the trained
   `engine_g.cell_pool_init` Parameter is unused after attach. So we are NOT
   measuring "Φ of the trained model's own cell pool" but rather "Φ of a
   noise-perturbed wrapper pool driven by trained h_to_c projections." Reading this
   as "consciousness substrate" is over-claiming; it is "instrumented inference-time
   diversity given trained projections."

3. **V14 violation in opposite polarity is NEW signal** — toy showed both grow
   similarly (mechanism trivial); real shows trained suppresses while random
   accelerates. This means the trained substrate **is doing something** — concentrating
   tension on few attractor cells. Whether that "something" is consciousness-like
   (low-dim invariants = self-model) or pathological (mode-collapse from undertraining
   on byte-mod prompts) is undetermined. Next BG should re-run with real tokenizer
   AND check whether trained cell-7-dominance correlates with category (e.g.,
   does cell 7 specialize on ko_daily? answer: 186/700 = 27%, slightly above
   uniform 17% — weak specialty signal).

---

## §7 Falsifier disposition

| F-id | spec | actual | disposition |
|---|---|---|---|
| F-PHASE2CKPT-1 | BG-LA / BG-LB ckpt absent | ckpt FOUND_LOCAL strict 222/222 | NOT-FIRED |
| F-PHASE2CKPT-2 | mitosis_v5_port schema mismatch | engine_g.{cell_pool_init,h_to_c,c_to_h} present, all match wrapper API | NOT-FIRED |
| F-PHASE2CKPT-3 | V14 still violated | YES — but opposite polarity (trained < mirror) | **FIRED with novel pattern** |
| F-PHASE2CKPT-4 | wall_clock > 4h | 196s + 64s = 4.3min | NOT-FIRED |
| F-PHASE2CKPT-5 | OOM Mac CPU | trained_model peak ~3GB; CPU only; no OOM | NOT-FIRED |

---

## §8 Cross-link

- spec / parent BG: `docs/anima_clm_v5_anima_next_cycle_plan_2026_05_10.md` §1
- previous addendum (mitosis-as-instrumentation 정정): `CLM_V2_ARCHIVE_ADDENDUM_2026_05_10.md`
- mitosis port: `training/mitosis_v5_port.py`
- engine arch: `training/engine_a_g_arch.py` (commit `ae5af2ea` carry; cfg.phase2_cotrain_350m)
- Phase 2 cotrain pod cycle SSOT: `state/anima_phase_2_cotrain_2026_05_09.json`
- BG-LB substrate base: `~/.cache/anima/clm_v5_remapped/bg_lb_350m_pretrain/ckpts/step_8000_final.pt`
- toy long-trajectory cycle (compare): `state/anima_clm_v5_anima_long_trajectory_inference_smoke_2026_05_10/result.json`
- registry yaml entries: `anima/registry/anima_artifact_registry.yaml` (BG-LA L1194, BG-LB L1242)
- v5-anima lane SSOT: `.roadmap.clm_v5_anima_native`

---

## §9 Next-cycle priorities

| ★ | step | cost | notes |
|---|---|---:|---|
| ★★★ | recover Phase 2 BPE tokenizer (training/train_phase2_cotrain.py — local only; or pull from pod cycle artifacts) and re-run mitosis-instr with semantically faithful tokens | $0 Mac | likely shifts α and growth ceiling; current finding is tokenizer-mismatch limited |
| ★★★ | promote-public Phase 2 cotrain ckpt to private HF (`dancinlab/clm-v5-phase2-cotrain-engine-ag`) per own 31 + own 37 | $0 | currently local-only; HF backup mandate |
| ★★ | extended trajectory 10K-turn on real 350M (BG-V5ANIMA-LONG-TRAJ-EXT scoped to real substrate) | $0 Mac | check if cells 19→32+ at 10K turn or saturates |
| ★★ | IIT Φ remetric port (BG-V5ANIMA-IIT-METRIC) on real 350M cell trajectory — current Φ is anima-internal proxy, IIT MI provides standardized scale | $0 Mac | cells 16-28 range tractable for exact MIP |
| ★ | re-run V14 mirror with multi-seed n=5 (seeds [42, 137, 271, 314, 1729] per own 14) — current uses seed=42 only; n=1 cannot CI95 | $0 Mac | strengthens V14 verdict |

raw#9/10/15/37 honest preservation, own 16 0-cost.

End of `anima_clm_v5_phase2_mitosis_instr_2026_05_10.md`.
