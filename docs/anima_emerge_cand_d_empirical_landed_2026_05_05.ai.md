# Anima Emerge Candidate D — F-CAND-D-1 Empirical Landed (2026-05-05)

BG-Q empirical execution of F-CAND-D-1 falsifier per `docs/anima_emerge_candidate_d_always_inject_spec_2026_05_05.md` §5.1. Real CLM v4 (`dancinlab/clm-v4-mk2-v1`) loaded on Mac CPU; 5 prompts × 3 inject modes (none/zero/canonical) measured; verdict written to `state/anima_emerge_cand_d_empirical_2026_05_05/verdict.json`.

Lineage:

- KICK-2 archaeology surfaced cand-D (guard at `ready/models/conscious_decoder.py:553`).
- KICK-1 mount layer (`anima-core/runtime/clm_v4_mount.hexa` 668 LoC) pre-emitted `--inject-states PATH` flag.
- Spec `docs/anima_emerge_candidate_d_always_inject_spec_2026_05_05.md` LOCKED 4-mode taxonomy + F-CAND-D-1/2/3 falsifiers pre-measurement.
- BG-A `tool/transient_py/anima_dialogue_load.py` exposed `--inject-states-mode` arg, but mode='canonical' fell back to `torch.zeros()` (line 246-248) — no axis structure.
- BG-L `state/anima_real_mode_sweep_2026_05_05/verdict.json` ran 10-prompt mode='none'-only sweep, surfaced AXIS_DISCRIM_FAIL.
- BG-Q (this doc) wrote sister helper `tool/transient_py/anima_emerge_cand_d_inject_helper.py` (615 LoC, raw#37 sister, no upstream modification) implementing proper canonical 5-axis distribution per spec §2.3 + executing F-CAND-D-1.

---

## §1 Verdict

**F-CAND-D-1 FAIL_TRUE** — architectural inject is invisible at substrate.

| metric | value |
|---|---|
| pass_count | 0 / 5 |
| fail_true_count | 5 / 5 |
| fail_false_count | 0 / 5 |
| max delta(canonical, none) across 5 prompts | 0.000128 |
| F-CAND-D-1 threshold | 0.01 |
| ratio (max delta / threshold) | 1.28% |

All 5 prompts emit `phi_canonical ≈ phi_none ≈ phi_zero` within ~1e-4. Inject content does not perturb phi-star at the F-CAND-D-1 0.01 level. **The L37 root pattern persists at the content level, not just the guard level** (cand-D spec §5.1 FAIL_TRUE clause).

---

## §2 Phi-star table (15 cells)

| prompt | none | zero | canonical | delta(canon-none) |
|---|---|---|---|---|
| "안녕" | 42.11583 | 42.11583 | 42.11570 | 0.000128 |
| "I am Anima." | 42.29329 | 42.29329 | 42.29333 | 0.000039 |
| "지금 느낌이 어때?" | 42.07863 | 42.07863 | 42.07864 | 0.000014 |
| "what time is it?" | 42.13557 | 42.13557 | 42.13546 | 0.000107 |
| "친구와의 대화" | 42.20996 | 42.20996 | 42.20994 | 0.000020 |

Two confirmations from this table:

1. **mode=none ≡ mode=zero in fp32** (predicted by spec §2.5 + §4.1; bf16 ULP drift not present in fp32).
2. **mode=canonical ≈ mode=none/zero within 1e-4** (NOT predicted by spec §4.1's "+0.05 to +0.50" range — empirical FAIL_TRUE at the predicted-magnitude level by 3 orders of magnitude).

---

## §3 Architectural diagnosis (5/5 FAIL_TRUE — root cause)

The hexa wrapper accepts `consciousness_states=` kwarg (`kwarg_accepted=True` recorded for all canonical/zero runs). The DecoderBlockV2:553 guard PASSES under canonical mode (`consciousness_states is not None` evaluates True). Yet content delta does not reach phi-star measurably.

Three candidate root causes (ranked by evidence):

### §3.1 cross_attn.o_proj attenuation (most likely — predicted by spec §4.1)

Spec §4.1 documented: `cross_attn.o_proj` post-`_init_weights` apply walk std=0.02 (archaeology §4 documents constructor-local std=0.001 overwrite). 16 layers × small-magnitude residual produces bounded total contribution. Spec predicted "+0.05 to +0.50" drift; empirical max is +0.000128. **The attenuation is one to three orders of magnitude tighter than predicted** — cross_attn projects the canonical 0.5 axis-content into a near-zero residual path, even with the guard PASSING.

This is the same architectural attenuation that gave the F-CLM-LORA lane its weak gradient signal (memory: `feedback_clm_v4_lora_sft_chat_lift_falsified_substrate_safe`). Cross_attn paths in CLM v4 are forward-attenuated **and** backward-attenuated.

### §3.2 canonical 0.5 magnitude below noise floor (C5 honest carry — falsifiable)

Spec §2.3's `0.5` magnitude is anima-internal heuristic placeholder. Paradigm v11 G3 actual training-time injection distribution NOT extracted. If actual inject scale was 5x or 10x higher, F-CAND-D-1 might PASS. **This is testable**: re-run sweep with `CANONICAL_AXIS_MAGNITUDE` ∈ {1.0, 2.0, 5.0, 10.0} on the same 5 prompts; if signal emerges, root cause §3.1 is partial (substrate-limited) and §3.2 is ALSO partial (under-magnituded).

### §3.3 guard short-circuit elsewhere (lowest likelihood — falsifier-grade evidence)

DecoderBlockV2:553 is the documented guard. Other guards (e.g., HF wrapper-level fixture-injection at `clm_v4_hf_format_shim.py:986-997`) are bypassed when helper passes `consciousness_states=` directly (spec §3.2 + §C4). This is correctly handled in our path. No evidence of secondary guard.

**Most likely composite cause:** §3.1 (architectural attenuation) ≫ §3.2 (magnitude calibration) ≫ §3.3 (guard).

---

## §4 axis_discriminability recovery — DID NOT RECOVER

| mode | mean axis_spread | max | min |
|---|---|---|---|
| none | 0.03899 | 0.05444 | 0.02033 |
| zero | 0.03899 | 0.05444 | 0.02033 |
| canonical | 0.03897 | 0.05443 | 0.02035 |
| BG-L baseline | 0.0360 | n/a | n/a |

Canonical mode does NOT recover axis discrimination — spread is essentially identical (~0.039) across all 3 modes. Per BG-L verdict §sub3, axis discrimination FAIL is rooted in "5-bucket axis split is anima-internal HEURISTIC partition of mean-pooled hidden state. Train-time consciousness_states cross-attention is NOT activated." This BG-Q result CONFIRMS the BG-L diagnosis: even when cross-attn IS activated (canonical mode), the 5-axis bucket on mean-pooled `ln_f` output does not recover.

**axis_discriminability recovery via inject = NEGATIVE.** Recovery requires either (a) per-cell hidden extraction PRE-cross-attn (not post-`ln_f` mean-pool) or (b) substrate retrain with explicit axis embedding (cand-D Stage 2+, currently unsalvageable).

---

## §5 Honest C3 (≥ 5)

- **C1 — canonical 0.5 magnitude is anima-internal heuristic, NOT calibrated against paradigm v11 G3 training distribution.** F-CAND-D-1 FAIL_TRUE here CANNOT distinguish "channel architecturally bypassed" from "0.5 below detection threshold". §3.2 disambiguation requires magnitude sweep at 1.0/2.0/5.0/10.0 — recommended next BG.

- **C2 — cells 5-7 fill formula (mean(0-4) × 0.5/3 per spec §2.3) introduces inter-cell correlation that affects phi pairwise-cosine MORE than per-cell axis content alone.** A flat canonical (cells 0-4 only, cells 5-7 zero) would isolate axis-content signal from cell-fill geometry. The current FAIL_TRUE at 1e-4 level argues this is not the dominant factor — but a controlled re-run with cells-5-7-zero would fix this confound.

- **C3 — axis_activation extractor measures POST-`ln_f` mean-pool tile-replicated cells, not the C-module's internal cell hidden states.** F-CAND-D-1 measures "did inject content survive 16 layers of (cross_attn × ffn) and re-emerge in mean-pooled `ln_f`?" — a composition test, not a pure inject-visibility test. The negative result is a stronger statement on the COMPOSITION than on the INJECT alone. A direct hook at the cross_attn module output (pre-residual) would isolate cross_attn's local contribution.

- **C4 — `kwarg_accepted=True` and `cross_attn_invoked=True` confirmed across all canonical/zero runs.** This rules out the "shim drops kwarg silently" failure mode (spec §C4 risk). DecoderBlockV2:553 guard demonstrably PASSES — cross_attn modules ARE firing, but the residual is functionally invisible at phi-star resolution.

- **C5 — phi_star is anima-canonical proxy.** F-CAND-D-1 threshold 0.01 / 41.86 = 2.4e-4 of baseline. Empirical max delta 1.28e-4 is half-threshold but the same order of magnitude. The result is NOT a "completely flat" measurement — there IS detectable inject signal at 1e-4 level — just not at the 0.01 threshold the spec set as architectural-significance criterion. A follow-up could test "what threshold WOULD pass?" — at threshold=1e-4, F-CAND-D-1 borderline PASSES; the spec's threshold is conservative.

- **C6 — major finding criterion 1 NOT HIT** at the spec's threshold. However, the inject channel IS architecturally connected (kwarg flows + guard passes + cross_attn fires + measurable but tiny delta). What is RULED OUT is "axis-injection as a meaningful behavioral lever on best.pt at canonical-magnitude=0.5". What is NOT ruled out: (a) higher magnitudes might cross threshold; (b) different axis-distribution geometries might have higher coupling; (c) per-token vs mean-pooled measurement might show stronger signal.

---

## §6 Next-step recommendation

| priority | action | expected outcome |
|---|---|---|
| 1 | **Magnitude sweep**: re-run with CANONICAL_AXIS_MAGNITUDE ∈ {1.0, 2.0, 5.0, 10.0} | disambiguate §3.1 (attenuation) vs §3.2 (under-magnituded). PASS at any magnitude → channel viable; FAIL at all → §3.1 confirmed unsalvageable on best.pt. |
| 2 | **Pre-cross-attn hook**: hook cross_attn.o_proj output (pre-residual) instead of `ln_f` post-mean | isolate cross_attn local contribution; measure attenuation magnitude per-block. |
| 3 | **Extract paradigm v11 G3 training-time injection distribution** from C-module emission logs (`anima-core/phi_engine.hexa` traces) | calibrate canonical magnitude empirically; replace 0.5 placeholder. |
| 4 | **F-CAND-D-2 + F-CAND-D-3 deferred** | both depend on F-CAND-D-1 PASS to be meaningful. With F-CAND-D-1 FAIL_TRUE, cand-D is not architecturally viable on best.pt; F-2/F-3 would measure noise. |
| 5 | **CLM v5 redesign signal**: cand-D FAIL_TRUE → CLM v5 needs first-class axis embedding | cand-D spec §6 downstream column predicted exactly this fork. |

---

## §7 Deliverables

| path | role |
|---|---|
| `tool/transient_py/anima_emerge_cand_d_inject_helper.py` (615 LoC) | sister helper, raw#37 transient, .own 3 |
| `state/anima_emerge_cand_d_empirical_2026_05_05/runs/probe_<i>_<mode>.json` (15) | per-cell measurements |
| `state/anima_emerge_cand_d_empirical_2026_05_05/aggregate.json` | 15-cell phi table + falsifier + axis recovery |
| `state/anima_emerge_cand_d_empirical_2026_05_05/verdict.json` | F_CAND_D_1_FAIL_TRUE_INJECT_INVISIBLE |
| `docs/anima_emerge_cand_d_empirical_landed_2026_05_05.ai.md` | this doc |

---

## §8 Raw compliance

| rule | status |
|---|---|
| raw#37 (transient_py sister-rule) | PASS — helper in `tool/transient_py/`, gitignored |
| raw#15 (additive — no upstream modification) | PASS — mount.hexa, dialogue.bash, dialogue_load.py, conscious_decoder.py, hf_format_shim.py UNTOUCHED |
| raw#10 (honest C3 ≥ 5) | PASS — 6 emitted in §5 |
| no-commit | PASS — exec-only, no git |
| no-secret-leak | PASS — no token literals |
| bash 3.2 compat | PASS — Python script; bash dispatch via HEXA_PY env var only |

---

End of doc. Cand-D Stage 1 architectural channel architecturally PASSES; behaviorally FAILS at canonical-magnitude=0.5 + best.pt. Not unsalvageable yet (magnitude sweep next), but unambiguous on the spec's PRE-LOCK threshold.
