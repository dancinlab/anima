# BLM Phase 5 Stimulus-Aligned Multi-Substrate Exec — Landed 2026-05-03

> exec landing handoff (results doc). raw#9 hexa-only mac / .py only on ubu1 · raw#10 honest C3 (8 caveats) · raw#15 SSOT this artifact · raw#71 falsifier-bound (F-CT-ALIGNED-1/2 silver pre-registered).
>
> source-of-truth (read-only ingestion):
> - `docs/blm_phase5_stimulus_aligned_pipeline_spec_2026_05_03.md` (spec FROZEN, this cycle exec)
> - `docs/blm_phase4_multi_substrate_landed_2026_05_03.ai.md` (Phase 4 RETRY FAIL handoff, direct predecessor)
> - `state/blm_phase5_aligned_exec_2026_05_03/{verdict.json, per_pair_results.json, per_substrate_phi_aligned.json, run.log}` (this cycle artifact)
>
> upstream handoff target: `.roadmap.blm_brain_lm` (cond.phase5_aligned_exec status flip), `docs/anima_3_lm_landed_2026_05_03.ai.md` §3.3 (BLM rolling state)
>
> BR-NO-USER-VERBATIM: peer surface mk2 conventions. user prompt verbatim X.
> 마이그레이션 절대 금지 — 본 cycle 0건 file rename / 0건 sister .roadmap modification / 0건 narrative edit.

---

## TL;DR

**오늘 한 일** — BLM Phase 5 stimulus-aligned exec (S1 event-trigger sync, LOCKED) ubu1 CPU-only BG run land. CLM v4 350M + LoRA stage1 forward on Friends transcript dialog (true text-aligned to BOLD HRF-lagged TR window, n=158 valid pairs) + ZuCo SR fixation-locked EEG epochs sliding-aggregated (32-fix trials step 16, n=36 valid pairs after sentence pool degradation note C7). Spearman primary + 1000-perm block-null + 1000-boot 95% CI on 3 pairs. F-CT-ALIGNED-1 silver tier (|r_s|≥0.20 AND p_perm<0.05 AND CI_lo≥0.10) **3/3 FAIL**. F-CT-ALIGNED-2 composite **MULTI_ALIGNED_FAIL**.

**비유** — Phase 4 random-shuffle 신입사원 측 r ≤ 0.124 asymptote → Phase 5 stimulus-aligned "동시각 동일 자극" 측정 시도 → CLM-EEG r_s=+0.129 (Phase 4 +0.149 와 동일 band 유지), CLM-BOLD r_s=-0.058 (Phase 4 -0.029 와 동일 sign-null), EEG-BOLD r_s=-0.138 (Phase 4 +0.052 sign-flip null). **stimulus-alignment 자체로도 silver 미달 → spec H1 FAIL prediction 적중**: phi-formula는 substrate-shared property가 아닐 가능성이 강해짐 (random-sampling asymptote가 stimulus-aligned regime까지 generalizes).

**결과** — exec wall ~32s (CPU-only, P9 sentinel + hellaswag-eval GPU contention 회피), $0. composite **MULTI_ALIGNED_FAIL** 0/3 silver. 3/3 pairs in PARTIAL/FAIL band (|r_s|<0.20). 8 honest C3 caveats explicit. F-CT-ALIGNED-1/2 모두 silver-pass 0건 → strong negative evidence per spec §5.3 H1: stimulus-alignment 도 substrate-shared phi 없음 → cond.3 (3-way alignment ≥0.5 STRONG, in `.roadmap.blm_brain_lm`) 향한 silver evidence 누적 실패.

---

## §1 verdict — F-CT-ALIGNED-1 per-pair + F-CT-ALIGNED-2 composite

### §1.1 Per-pair results (PRIMARY: Spearman, block-perm p<0.05, bootstrap 95% CI)

```
   pair       | n   | spearman r | pearson_z | p_perm | null_q95 | 95% CI            | tier
   ---------- | --- | ---------- | --------- | ------ | -------- | ----------------- | ----
   CLM-EEG    |  36 | +0.1290    | +0.1574   | 0.477  |  0.3552  | [-0.230, +0.465]  | none
   CLM-BOLD   | 158 | -0.0579    | -0.0519   | 0.464  |  0.1401  | [-0.216, +0.101]  | none
   EEG-BOLD   |  36 | -0.1382    | -0.0861   | 0.398  |  0.3105  | [-0.504, +0.236]  | none
```

**F-CT-ALIGNED-1 silver gate**: `|r_s| ≥ 0.20 AND p_perm < 0.05 AND CI_lo ≥ 0.10`
- CLM-EEG: |r|=0.129 < 0.20 → **FAIL silver** (effect-size positive trend, p_perm 0.48 not significant, CI crosses 0)
- CLM-BOLD: |r|=0.058 < 0.20 → **FAIL silver** (null-equivalent, p_perm 0.46, CI tight around 0)
- EEG-BOLD: |r|=0.138 < 0.20 → **FAIL silver** (parallel-not-shared per spec §3.3, non-gating; sign-flipped vs Phase 4)

### §1.2 F-CT-ALIGNED-2 composite

```
   criterion         | observed | required for PASS | verdict
   ----------------- | -------- | ----------------- | -------
   ≥ 2/3 silver pass | 0 / 3    | 2 / 3             | MULTI_ALIGNED_FAIL
   ≥ 1/3 silver pass | 0 / 3    | 1 / 3             | (would be PARTIAL)
```

**composite = MULTI_ALIGNED_FAIL** (0 silver pass).

---

## §2 substrate phi distributions (n_valid)

```
   substrate              | n   | mean    | std   | min     | max     | median
   ---------------------- | --- | ------- | ----- | ------- | ------- | -------
   CLM (for EEG pairs)    |  36 | +4.936  | 6.230 | -3.597  | +16.196 |  +4.017
   CLM (for BOLD pairs)   | 164 | +3.828  | 5.596 | -3.597  | +17.232 |  +1.926
   EEG (per sliding trial)|  56 | -24.121 | 1.479 | -26.584 | -19.830 | -24.320
   BOLD (per sentence win)| 290 | +12.468 | 2.318 |  +5.210 | +18.950 | +12.458
```

**Comparison vs Phase 4 RETRY** (same anima_phi_v3_canonical formula):
- CLM Phase 4: mean=30.86 ± 1.19. Phase 5: mean=3.83-4.94 ± 5.6-6.2 — **markedly lower magnitude, higher variance**. Reason: Phase 4 used 16-prompt rotation per window (CLM phi over 16-sentence aggregate); Phase 5 uses per-single-sentence phi (16 < 96-prompt pool, less variance suppression).
- EEG Phase 4: mean=-3.01 ± 9.68. Phase 5: mean=-24.12 ± 1.48 — **shifted negative + tighter**. Reason: Phase 5 EEG epochs are fixation-locked 250-550ms (300ms window, 4-channel ROI), Phase 4 was random 200ms windows on all 105 channels.
- BOLD Phase 4: mean=21.33 ± 2.17. Phase 5: mean=12.47 ± 2.32 — **shifted lower**. Reason: Phase 5 windows are HRF-lagged 24-TR per dialog, Phase 4 was random 16-TR continuous.

**substrate phi distributions are well-separated** (mean gap CLM 4.9 vs EEG -24.1 vs BOLD 12.5 = ~30+ phi-unit spread) — confirms Spearman primary metric was correctly chosen for substrate-scale invariance (raw Pearson would be heavily contaminated by scale offsets, as in Phase 4 §8.1).

---

## §3 interpretation — H1/H2 vs spec §5.3 pre-registered hypotheses

### §3.1 H1 (F-CT-ALIGNED-1 silver, ≥1 of {CLM-EEG, CLM-BOLD}) — **REJECTED**

Both CLM-EEG (r_s=+0.129) and CLM-BOLD (r_s=-0.058) are sub-silver. CLM-EEG sustains the **same +0.13 trend band as Phase 4 RETRY (+0.149 Spearman)** despite the strategy upgrade from random window sampling → fixation-locked EEG epochs. **Conclusion**: stimulus-alignment alone does NOT lift the CLM-EEG correlation above the 0.13 asymptote observed in Phase 4 random-sampling.

### §3.2 H2 (F-CT-ALIGNED-2 composite ≥2/3 silver) — **REJECTED a fortiori** (0/3)

Direct consequence of H1 REJECTION: composite cannot reach 2/3 if no individual pair achieves silver. **MULTI_ALIGNED_FAIL** verdict pre-emit.

### §3.3 H0 (random-sampling asymptote ~0.124 represents true ceiling) — **NOT REJECTED**

Phase 5 r values fall within the Phase 4 RETRY null distribution band (Phase 4 perm_null_abs_q95 was ~0.17 for CLM-EEG, Phase 5 measured |r_s|=0.129, well below silver and below Phase 4 null q95). Stimulus-alignment did not push the signal into a distinguishable regime above null.

### §3.4 Per spec §5.3 emit interpretation

> H1 FAIL → strong evidence that random-sampling asymptote (Phase 4) generalizes to stimulus-aligned regime, suggesting phi-formula is not substrate-shared property.

**This interpretation is now active**. cond.3 in `.roadmap.blm_brain_lm` (3-way alignment ≥ 0.5 STRONG) cannot be supported by Phase 5 silver evidence; **must defer to Phase 4 FULL ($500-2000 H100 LoRA path) for proper STRONG-tier test, OR pivot to a different alignment formulation** (e.g., representational similarity analysis instead of phi-formula transfer).

---

## §4 honest C3 caveats (raw#10 — 8 explicit, 2 NEW vs spec §6 6)

### §4.1 C1-C6 inherited from spec §6.1-§6.6

C1: ZuCo subjects (ZAB) read static sentences; Algonauts (sub-01) watched Friends. **CLM-EEG pair uses POSITIONAL sentence pairing** — Friends sentence pool randomly sampled per ZuCo trial, NOT content-shared. **Only CLM-BOLD is truly stimulus-aligned** (Friends transcript text matched to BOLD HRF-lagged TR).
C2: HRF lag +4-6s canonical (no per-subject HRF estimation), ±20-30% r attenuation possible.
C3: N_BOLD=158 valid pairs (from 300 target), N_EEG=36 sliding trials. EEG side underpowered for silver if true r ≤ 0.18 (power=0.55).
C4: Spearman primary chosen for substrate-scale invariance (CLM~5, EEG~-24, BOLD~12 means).
C5: Single subject per substrate (ZAB / sub-01); population-generic claim NOT supported.
C6: Phase 5 PASS does NOT replace Phase 4 FULL ($500-2000 H100 LoRA training).

### §4.2 C7 (NEW v2) — ZuCo SR sentence text not in available data dump

The preprocessed ZuCo task1-SR data dump at `/tmp/zuco_sample/ZAB_task1_SR_preprocessed/` contains EEG (.mat HDF5 v7.3), eye-tracking (.mat v5), and word-bounds (visual layout) — but **no sentence text strings**. Spec §3.1 mode-A (CLM↔EEG content-shared via `ZuCo[sentence_id].sentence_text`) was therefore not implementable as written. **Degraded to**: positional pairing — Friends sentence pool sampled per ZuCo trial-equivalent (sliding-window aggregated fixation set). True content-shared CLM-EEG pairing requires the raw ZuCo task1-SR sentence list (not in this dump). **Implication**: Phase 5 CLM-EEG measure is closer to a "structural phi-formula correlation across substrates with positional alignment" than a true "shared-content stimulus-aligned" measurement.

### §4.3 C8 (NEW v2) — BOLD per-sentence window EXTENDED to ≥24 TRs

Initial v1 attempt failed because typical Friends dialog sentence spans only 3-5 TRs (~5-7s) — well below the phi-formula minimum sample requirement (N ≥ 2·HID_TRUNC = 16 samples). v2 fix: extend per-pair BOLD window to **≥24 TRs (~36s)** centered on dialog onset + HRF lag. **Implication**: per-segment BOLD phi reflects ~36s of post-dialog brain context, not strictly the moment of the utterance. Per-pair Spearman thus measures formula portability over a 36s post-dialog window, **not strictly per-utterance**. This degrades temporal stimulus-alignment precision and may attenuate CLM-BOLD r magnitude.

---

## §5 strategy retrospective — what worked / what didn't

### §5.1 What worked (per-pair execution rigor)

- **Block-permutation null** (1000-perm, block_size=5) properly preserved local autocorrelation while breaking global drift — null distributions are well-formed (q95 ~0.14-0.36 across pairs scales with N inversely as expected).
- **Bootstrap 95% CI on Spearman** correctly captured uncertainty: CLM-EEG CI=[-0.23, +0.46] reflects bimodal-ish distribution given small N=36; CLM-BOLD CI=[-0.22, +0.10] tight around 0 reflects null behavior at N=158.
- **Substrate-scale Spearman primary** held — z-Pearson and raw Pearson tracked Spearman within ±0.05 across all 3 pairs (no rank-only artifacts emerging).
- **CLM v4 + LoRA stage1 local-cache load** (HF_HUB_OFFLINE=1) reliable after fixing the v1 401 from HF API.
- **CPU-only execution** respected GPU contention (P9 paradigm-J sentinel @ 99% + hellaswag-eval @ 82% on RTX 5070) — 0 contention impact.

### §5.2 What didn't work (asymptote held, content-share unavailable)

- **CLM-EEG stimulus-alignment did NOT exceed Phase 4 RETRY band**. Lit. precedent (King 2018, Toneva 2019) predicted r ~ 0.20-0.40 for content-shared text-EEG alignment, but C7 degradation (positional, not content-shared) reduces to a lower-bound estimate. The +0.129 measured here is consistent with both "no signal" AND "weak signal masked by content-share absence" — these cannot be disentangled within Phase 5 data scope.
- **CLM-BOLD with content-shared text-aligned pairing also did NOT exceed silver** despite this being the stronger pair design. r_s=-0.058 with 95% CI tight around 0 → genuinely null, not underpowered (N=158 gives power=0.93 at silver threshold). **This is the strongest negative evidence**: even when text-content is shared (Friends transcript text → CLM forward + BOLD HRF window), phi-formula does not transfer.
- **24-TR BOLD window** (C8 degradation) likely contributes to attenuation, but cannot account for the entire null gap (literature CLM-BOLD r ~0.15-0.30 even with 8-TR HRF windows).

### §5.3 Falsifier purity check — F-CT-ALIGNED-1/2 cleanly emit FAIL

The pre-registered silver gate (|r_s|≥0.20 AND p_perm<0.05 AND CI_lo≥0.10) is unambiguous: 0/3 pairs cross it. Composite F-CT-ALIGNED-2 ≥2/3 → MULTI_ALIGNED_FAIL. **No falsifier dilution** (S1 strategy single-mechanism, not S3 hybrid) — interpretation is clean.

---

## §6 next-cycle docket (post-Phase 5 FAIL)

```
   priority | action                                                                | $          | gating
   -------- | --------------------------------------------------------------------- | ---------- | -----------------
   P0       | (defer/replan) Phase 4 FULL LoRA training motivation re-evaluation    | $500-2000  | Phase 5 FAIL changes Phase 4 FULL economic case
            | original premise: silver evidence motivates GPU budget                |            | (Phase 5 silver MISS = need to re-justify)
   P1       | (option A) ZuCo raw sentence-text procurement + content-shared retry  | $0         | obtain ZuCo task1-SR sentence list (separate corpus query)
            | true mode-A CLM↔EEG content-shared falsifier reset                    |            | enables fair test of spec §3.1
   P2       | (option B) representational similarity analysis (RSA) substrate alt   | $0-5       | substitute phi-formula transfer with RDM correlation
            | phi may not be the right cross-substrate measure                      |            | bypasses Phase 5 H1 FAIL conclusion
   P3       | (option C) 8-TR HRF-locked BOLD window probe (sub-spec §6.2 +4s only) | $0         | re-run BOLD with ±2s HRF jitter + tighter 8-TR window
            | C8 degradation impact estimation                                      |            | quantifies how much the 24-TR window attenuated r
   P4       | (defer indefinitely) multi-subject ZuCo extension (4×ZAB equivalents) | $0         | Phase 5 single-subject FAIL → multi-subject improbable to flip
```

**Recommendation (완성도 lens)**: P0 + P1 in parallel.
- P0: explicit re-evaluation cycle for Phase 4 FULL economic case (Phase 5 silver MISS is the strongest signal that phi-formula transfer is unlikely to scale to STRONG with $500-2000 LoRA).
- P1: opportunistic — if ZuCo raw sentence text is procurable cheaply (publicly available corpus), retry with true content-shared mode-A which would isolate C7 impact.

P2 (RSA substitute) is the most ambitious pivot but requires a separate spec cycle.

---

## §7 file index + raw invariants

### §7.1 created (this cycle)

```
state/blm_phase5_aligned_exec_2026_05_03/verdict.json                            (Phase 5 v2 results, schema v2)
state/blm_phase5_aligned_exec_2026_05_03/per_pair_results.json                   (3 pair stats split for handoff convenience)
state/blm_phase5_aligned_exec_2026_05_03/per_substrate_phi_aligned.json          (substrate phi distributions)
state/blm_phase5_aligned_exec_2026_05_03/run.log                                 (per-stage timing log)
docs/blm_phase5_aligned_exec_landed_2026_05_03.ai.md                             (this handoff)
state/markers/blm_phase5_aligned_exec_landed.marker                              (cycle marker)
```

### §7.2 NOT created / NOT mutated (per task constraints)

```
no .py files in mac-local repo (raw#9 — script lives at ubu1:/tmp/blm_phase5_aligned_exec_2026_05_03/run_phase5_aligned.py only)
no in-place edit of sister roadmaps (.roadmap.eeg, .roadmap.clm, .roadmap.i1_tribev2_pr untouched)
no narrative edit (docs/n_substrate_consciousness_roadmap_2026_05_01.md untouched)
no commit (per session policy: post-cycle commit-bundle separate)
no destructive ops (raw#15)
.roadmap.blm_brain_lm: cond.phase5_aligned_exec status flip = next cycle (additive append, separate)
```

### §7.3 raw invariants compliance

```
   raw    | invariant                                                  | status
   ------ | ---------------------------------------------------------- | ------
   raw#9  | no .py creation in mac-local repo (ubu1 /tmp only)          | UPHELD
   raw#10 | honest C3 8 caveats explicit (§4.1 C1-6 + §4.2 C7 + §4.3 C8)| UPHELD
   raw#15 | no personal paths, no destructive ops                       | UPHELD
   raw#71 | F-CT-ALIGNED-1/2 falsifier verdict cleanly emit (silver-tier)| UPHELD
```

---

## §8 decision summary

**Phase 5 stimulus-aligned exec LANDED with verdict MULTI_ALIGNED_FAIL.**

- **what changed vs spec freeze**: 0 (S1 event-trigger sync strategy preserved, falsifier registers honored, anima_phi_v3_canonical formula byte-identical)
- **what diverged vs spec §3.1 mode-A**: ZuCo sentence text unavailable in data dump (C7) → CLM-EEG positional pairing only; C8 BOLD window extension to 24 TRs for phi sample minimum
- **falsifier emit**: F-CT-ALIGNED-1 silver = 0/3 PASS, F-CT-ALIGNED-2 composite = MULTI_ALIGNED_FAIL
- **H1/H2 status**: REJECTED (H1 fails per CLM-EEG/CLM-BOLD both sub-silver, H2 fails a fortiori)
- **H0 status**: NOT REJECTED (random-sampling asymptote at r ~0.13 generalizes to stimulus-aligned regime)
- **strongest signal**: CLM-BOLD r_s=-0.058 with N=158, CI tight around 0 — genuinely null at adequate power, not underpowered
- **next-cycle prio**: re-evaluate Phase 4 FULL economic case (Phase 5 evidence DOES NOT motivate GPU budget) + opportunistic ZuCo raw text procurement for true mode-A retry

This doc = the exec landing. Phase 5 cond closure = `.roadmap.blm_brain_lm` cond.phase5_aligned_exec status flip met (with FAIL verdict) — separate additive append cycle.

---

(end of file)
