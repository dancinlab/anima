# shim v5 Phase 1 — landed handoff (2026-05-05)

**Status**: LANDED (Mac-side $0, ~25 min wall, no commit, no HF push).
**BG lane**: BG-SHIM-V5-PHASE1-IMPL.
**Spec anchor**: `docs/clm_v4_hf_format_shim_v5_spec_2026_05_05.md`.
**Companion (this doc)**: `docs/clm_v4_hf_format_shim_v5_phase1_landed_2026_05_05.ai.md`.
**Verdict**: `state/clm_v4_hf_format_shim_v5_phase1_2026_05_05/verdict.json`.

---

## §1 What landed

- `tool/transient_py/clm_v4_hf_format_shim_v5.py` — sibling file to LOCKED shim v4. 1631 lines (v4 is 1485). Diff vs v4: header banner + `SHIM_VERSION = "v5"` + `CLM_V5_CROSS_ATTN_O_PROJ_STD = 0.02` + new `_patch_conscious_decoder_copy` patch P3 + post-construction in-memory re-init in `_build_decoder_module`. raw#15 additive — shim v4 byte-identical (md5 `5c07f214f9a551c9a086dbfc4dfc866a` pre = post).
- `tool/transient_py/clm_v4_hf_format_shim_v5_selftest.py` — F-SHIM-V5-1 dry-run finite forward selftest. Mac CPU fp32, ~22 sec wall. Tests case A (consciousness_states=None bypass) + case B (canonical_zero [1, 8, 192] zeros fixture). Verifies 16/16 ConsciousCrossAttention modules re-initialised at std≈0.02 (band [0.0199815, 0.0200380], mean 0.0200021).
- `state/clm_v4_hf_format_shim_v5_phase1_2026_05_05/verdict.json` — structured Phase 1 verdict (PASS/FAIL fields, diff record, honest C3, Phase 2 GO recommendation).

## §2 F-SHIM-V5-1 verdict — PASS

| Case | consciousness_states | Finite | Shape | logits std | Verdict |
|---|---|---|---|---|---|
| A bypass | None | true | [1, 64, 64000] | 0.5554 | PASS |
| B canonical_zero | [1, 8, 192] zeros | true | [1, 64, 64000] | 0.5542 | PASS |

V5-1 spec statement: `model.forward()` returns finite logits on canonical_zero fixture for B=1, T=64. Threshold: `torch.isfinite(logits).all() AND shape [B, T, vocab=64000]`. Both cases PASS. Selftest wall=21.53 sec, total Phase 1 wall ~25 min including authoring + verdict + handoff.

Auxiliary observation: case A vs case B logits std differ by ~0.2% (0.5554 vs 0.5542). Expected — `cross_attn(Q, zeros, zeros) ~= 0` regardless of `o_proj` scale, so canonical_zero residual is near-zero. The std=0.02 effect only manifests when the fixture is non-zero (real `train_avg` fixture L2=2.2022). Phase 2 V5-3 sanity bound `|lift_pp| < 5pp` on canonical_zero is consistent with this prediction.

## §3 Diff vs shim v4

Single architectural change anchored to F-SHIM-V4-4 verdict §recommendations.shim_v5_design_hint:

```python
# shim v4 (LOCKED, conscious_decoder.py:420)
nn.init.normal_(self.o_proj.weight, std=0.001)

# shim v5 (Phase 1, OUTPUT-DIR copy via patch P3)
nn.init.normal_(self.o_proj.weight, std=0.02)  # 10x larger
```

Applied via two mirrored sites in shim v5:

1. **OUTPUT-DIR copy patch P3** (`_patch_conscious_decoder_copy`) — rewrites the line in the copy of `conscious_decoder.py` that lands inside the HF custom-code package. This is what HF `trust_remote_code=True` consumes. Wired from `_copy_legacy_sources` after the existing P1 + P2 patches on `decoder_v3.py`.
2. **In-memory re-init** in `_build_decoder_module` — for paths that construct the decoder without loading `best.pt` (Mac dry-run, F-SHIM-V5-1 selftest, fresh-init harness). Selector: modules with `.o_proj` AND `.k_proj` where `k_proj.in_features == 192` (consciousness_dim). Disambiguates from `CausalSelfAttention.o_proj`. Touched 16/16 expected modules.

Q decisions honoured per spec §7:
- Q1 std=0.02 (default).
- Q2 q/k/v re-init = NO (only o_proj — preserves residual *direction*, only changes *scale*).
- Q3 separate file (raw#15 additive).
- Q4 H100 ACK — DEFERRED (not in Phase 1 scope).
- Q5 PEFT compat — SCOPE-OUT (Risk C).

## §4 Falsifier suite F-SHIM-V5-1..5 progress

| Falsifier | Phase | Cost | Status |
|---|---|---|---|
| V5-1 dry-run finite forward | 1 (Mac) | $0 | **PASS (this BG)** |
| V5-2 v3 byte-equivalent regression `max_abs_diff <= 1e-5` | 2 (ubu1) | $0 | OPEN — Phase 2 |
| V5-3 canonical_zero finite forward + sanity bound `|lift_pp| < 5pp` | 2 (ubu1) | $0 | OPEN — Phase 2 |
| V5-4 real-fixture lift_pp >= +5pp on hellaswag-200 (decisive gate) | 3 (H100) | $1-3 | OPEN — needs Q4 ACK |
| V5-5 phi_star no_flip vs shim v4 base (in-pipeline 35.81) | 4 (Mac/ubu1 fp32) | $0 | OPEN — Phase 4 |

Threshold lock: per raw#71 falsifier pre-register, all V5-1..5 thresholds are LOCKED at spec land time. V5-1 PASS here uses the spec threshold verbatim (no relaxation).

## §5 Phase 2 GO recommendation

**GO**. Rationale:
- shim v5 substrate authored (.py + selftest), syntax-clean, F-SHIM-V5-1 PASS.
- shim v4 byte-identical preserved (md5 unchanged) — raw#15 additive verified.
- Phase 2 is $0 (ubu1 venv_orchestrator GPU time, no H100 spend) — no Q4 ACK needed.
- Phase 2 scope: V5-2 + V5-3. V5-2 is the Risk B gate (bypass guard leak detection). V5-3 is the canonical_zero sanity bound.

Phase 2 launch artifacts ready for ubu1 BG:
- shim v5 source (Mac authored, ubu1 reads via shared anima git tree).
- ubu1 venv: `/home/aiden/venv_orchestrator/bin/python` (RTX 5070 sm_120 needs torch 2.11.0+cu128 per memory).
- F-SHIM-V4-4 retry-2 hf CLI auth pre-flight pattern carryable.

## §6 Honest C3 (≥5)

- **C1** — F-SHIM-V5-1 PASS validates wiring + std=0.02 init landed in 16/16 ConsciousCrossAttention modules, but does NOT validate F-SHIM-V5-4 (real-fixture lift). std=0.02 calibration is a 10× heuristic anchored to verdict §recommendations.shim_v5_design_hint; actual hellaswag-200 lift unknown until Phase 3 H100 exec.
- **C2** — case B (canonical_zero) logits are near-identical to case A (bypass) — ~0.2% std delta. Expected because `cross_attn(Q, zeros, zeros) ~= 0` regardless of `o_proj` scale. The std=0.02 effect only manifests for non-zero fixtures (real train_avg L2=2.2022). Phase 2 V5-3 `|lift_pp| < 5pp` sanity bound is consistent with this expectation.
- **C3** — fresh-init model (no best.pt loaded) was used because Mac does not have best.pt locally. V5-1 spec statement does not require checkpoint-loaded weights — only finite forward on the architecture. Trained `o_proj` weights (when best.pt is loaded on ubu1/H100) would OVERWRITE this init UNLESS `cross_attn.o_proj` was never trained — which is exactly F-SHIM-V4-4 verdict's rationale (cross-attn bypassed during v3 training, so o_proj weights in best.pt sit at init scale). Phase 2 V5-2 byte-equivalent regression validates this empirically.
- **C4** — Risk B (V5-2 byte-equivalent regression) NOT yet validated. Bypass guard SHOULD make `consciousness_states=None` forward identical to shim v4 byte-for-byte, but PEFT introspection or hidden-state geometry side-effects could leak the bypass invariant. Phase 2 must validate `max_abs_diff <= 1e-5` before any Phase 3 H100 spend.
- **C5** — case A logits stats (mean=-0.0011, std=0.5554, range [-3.06, +2.81]) on a fresh-init random-token forward are within expected magnitude band for a 350M decoder — no NaN/Inf, no degenerate collapse. Sanity confidence, NOT a learned-weight signal.
- **C6** — patch P3 site detection uses exact-string match with 8-space indent. Upstream refactors will raise RuntimeError at convert time (fail-loud, not silent miss). Idempotent path handles re-runs.
- **C7** — selftest re-runs are idempotent (`torch.manual_seed(20260505)`) and do NOT modify HF cache or upstream sources. Shim v4 MD5 verified byte-identical pre/post selftest run.

## §7 Conformance checklist

- [x] raw#9 — shim v5 .py lives in `tool/transient_py/` (OPT-OUT path per .own 4)
- [x] raw#10 — ≥5 honest C3 (7 in verdict + 7 here)
- [x] raw#15 — additive only; shim v4 LOCKED + byte-identical, shim v5 sibling
- [x] raw#71 — F-SHIM-V5-1 threshold carried verbatim from spec (no relaxation)
- [x] No git commit (per BG spec CRITICAL)
- [x] No HF push (Phase 1 Mac-only)
- [x] No shim v4 mutation (md5 unchanged `5c07f214f9a551c9a086dbfc4dfc866a`)
- [x] `.own N` taxonomy preserved (.own 4 transient_py namespace)

## §8 Artifacts referenced

- `tool/transient_py/clm_v4_hf_format_shim_v5.py` — shim v5 source (1631 lines)
- `tool/transient_py/clm_v4_hf_format_shim_v5_selftest.py` — F-SHIM-V5-1 selftest (~22 sec wall)
- `tool/transient_py/clm_v4_hf_format_shim.py` — shim v4 LOCKED (md5 verified unchanged)
- `state/clm_v4_hf_format_shim_v5_phase1_2026_05_05/verdict.json` — Phase 1 verdict
- `state/clm_v4_hf_format_shim_v5_phase1_2026_05_05/selftest_output.json` — raw selftest stdout (49 lines)
- `state/clm_v4_hf_format_shim_v5_phase1_2026_05_05/selftest_stderr.log` — selftest stderr (empty)
- `docs/clm_v4_hf_format_shim_v5_spec_2026_05_05.md` — landed spec
- `docs/clm_v4_hf_format_shim_v5_spec_landed_2026_05_05.ai.md` — landed spec handoff
- `state/clm_v4_f_shim_v4_4_harvest_2026_05_05/verdict.json` — F-SHIM-V4-4 verdict (shim v5 design rationale anchor)
- `ready/models/conscious_decoder.py:420` — upstream `nn.init.normal_(self.o_proj.weight, std=0.001)` (LOCKED, NOT modified)

---

**END OF HANDOFF** — Phase 2 (ubu1 V5-2 + V5-3) may proceed.
