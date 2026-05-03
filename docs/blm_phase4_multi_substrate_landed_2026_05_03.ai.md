# BLM Phase 4 RETRY — Multi-Substrate Consistency Landed — 2026-05-03 (AI-native, friendly preset)

> friendly preset (icon + analogy + 7-element + ASCII)
>
> readers: AI agents (subagents, audit cron), Claude Code (next session)
> source-of-truth: 1 results.json (`state/blm_phase4_multi_substrate_2026_05_03/results.json`) + per-substrate phi (`per_substrate_phi.json`) + transient run script (`run_phase4_scale.py`) + run log (`run.log`)
> prior cycle: `state/blm_phase4_partial_3substrate_2026_05_03/results.json` (n=32 FAIL, r=0.0005)
> upstream handoff target: `.roadmap.blm_brain_lm` Phase 4 entry-trigger contract (cond.2 unmet status preserved)
>
> BR-NO-USER-VERBATIM: peer surface mk2 conventions. user prompt verbatim X.
> 마이그레이션 절대 금지 — 본 cycle 0건 file rename / 0건 sister .roadmap modification / 0건 narrative edit.

---

## TL;DR

**오늘 한 일** — BLM Phase 4 RETRY scale-up (n=32 → n=128 paired windows) executed on ubu1 local CPU ($0). 3-substrate (CLM hidden state ↔ ZuCo EEG ↔ Algonauts BOLD) cross-consistency 측정. F-CT-MULTI-1 silver falsifier 적용 (|r|>0.20 silver, |r|>0.50 strong). 결과 = **F-CT-MULTI-1_FAIL** (tier=none, 0 silver, 0 bronze pairs).

**비유** — Phase 4 PARTIAL = 신입사원 (BLM) 측 32명 셈플로 "다른 부서 (CLM, EEG, BOLD)와 같은 metric 쓰면 비슷한 패턴 나오나" 1차 측정 → r≈0 으로 NO. Phase 4 RETRY = 같은 측정 128명으로 4× 확대 → null 좁아져서 r 작아도 통계적으로 검출 가능해졌지만, **실제 r 자체가 silver 문턱 (|r|>0.20) 미만**. CLM-EEG 만 r=+0.124 (가장 큰 신호, 그러나 perm_null_q95=0.175 미만, p_perm=0.156).

**결과** — 3-substrate cross-consistency = **structural FAIL** at n=128. 같은 phi 공식을 독립 데이터에 적용했을 때 covariation 신호 없음. 이는 의미적 alignment 부재 때문 (random window sampling) 인지, 진짜 phi-as-shared-property 부재 때문인지 구분되지 않음. cond.2 (Phase 3 deferred) 여전히 unmet.

---

## §1 cycle inputs / outputs

### §1.1 inputs

```
   field                       | value
   --------------------------- | --------------------------------
   prior cycle                 | state/blm_phase4_partial_3substrate_2026_05_03/results.json (n=32, FAIL, r=0.0005)
   ZuCo data                   | /tmp/zuco_sample/ZAB_task1_SR_preprocessed/ (~425 MB, 8 SR sessions, gip_ZAB_SR{1..8}_EEG.mat)
   Algonauts data              | /tmp/algonauts2025_sub01/.../sub-01_task-friends_*-1000Par7Net*.h5 (~515 MB symlinked git annex)
   CLM ckpt                    | /home/aiden/anima/checkpoints/clm_v4_350m/scale_350m/best.pt + LoRA need-singularity/clm-v4-sft-stage1
   tokenizer                   | /tmp/tokenizer_64k_multilingual.model (vocab=64000)
   phi formula                 | anima_phi_v3_canonical (HID=8 top-variance, K=8 sample-partition halves, MIN over K, ridge=1e-3)
   N target                    | 128 paired windows (4× scale-up vs PARTIAL n=32)
   permutation null            | N=1000 per pair
   device                      | CPU (RTX 5070 occupied by P9 PR-1.5 sentinel training PID 1726340)
```

### §1.2 outputs

```
   artifact                                                                        | sha-equivalent (size + key fields)
   ------------------------------------------------------------------------------- | ---------------------------------------
   state/blm_phase4_multi_substrate_2026_05_03/results.json                        | 4674 bytes, schema anima/blm_phase4/multi_substrate_scale/1
   state/blm_phase4_multi_substrate_2026_05_03/per_substrate_phi.json              | 120827 bytes, 128 records × 3 substrates + valid_mask
   state/blm_phase4_multi_substrate_2026_05_03/run.log                             | 2831 bytes (transient mirror of ubu1 /tmp run log)
   state/blm_phase4_multi_substrate_2026_05_03/run_phase4_scale.py                 | 25865 bytes (raw#9 transient .py — landed for replay only)
   state/markers/blm_phase4_multi_substrate_landed.marker                          | <new this cycle>
   docs/blm_phase4_multi_substrate_landed_2026_05_03.ai.md                         | <this file>
```

---

## §2 pairwise correlation matrix (3×3 Pearson, n=128)

```
              CLM         EEG         BOLD
   CLM    +1.0000     +0.1245     -0.0293
   EEG    +0.1245     +1.0000     +0.0826
   BOLD   -0.0293     +0.0826     +1.0000
```

Spearman (rank) matrix:

```
              CLM         EEG         BOLD
   CLM    +1.0000     +0.1499     -0.0301
   EEG    +0.1499     +1.0000     +0.0523
   BOLD   -0.0301     +0.0523     +1.0000
```

### §2.1 per-pair permutation tests (N=1000)

```
   pair        | pearson_r | spearman_r | p_perm | null_|r|_q95 | exceeds_q95
   ----------- | --------- | ---------- | ------ | ------------ | -----------
   CLM-EEG     | +0.1245   | +0.1499    | 0.156  |  0.1749      | False
   CLM-BOLD    | -0.0293   | -0.0301    | 0.732  |  0.1783      | False
   EEG-BOLD    | +0.0826   | +0.0523    | 0.340  |  0.1642      | False
```

### §2.2 substrate phi distributions

```
   substrate | n   | mean   | std    | min    | max    | median
   --------- | --- | ------ | ------ | ------ | ------ | ------
   CLM       | 128 | 30.86  |  1.19  | 28.30  | 33.59  | 30.74
   EEG       | 128 | -3.01  |  9.68  |-17.11  | 14.51  | -4.62
   BOLD      | 128 | 21.33  |  2.17  | 16.10  | 28.99  | 21.36
```

(scale anchor compare: CLM HID=8 anchor 41.86 from anima_phi_v3_canonical baseline → CLM-substrate offset −11pt, EEG −44pt, BOLD −20pt — confirms each substrate has its own scale; phi formula is NOT substrate-invariant in absolute value, as predicted by raw#10 caveat 3.)

---

## §3 verdict

**F-CT-MULTI-1_FAIL** (tier = none)

```
   threshold  | criterion                              | n_pairs_passing
   ---------- | -------------------------------------- | ---------------
   strong     | |r| > 0.50 AND p_perm < 0.01           | 0
   silver     | |r| > 0.20 AND p_perm < 0.05           | 0
   bronze     | |r| > perm_null_abs_q95                | 0
```

### §3.1 closest-to-pass pair

CLM-EEG: r=+0.1245, q95=0.1749. Gap to bronze tier: 0.0504. Gap to silver: 0.0755 in r magnitude. p_perm=0.156 (not significant).

### §3.2 vs Phase 4 PARTIAL (n=32) baseline

```
   pair       | partial r (n=32) | scale r (n=128)  | sign change?
   ---------- | ---------------- | ---------------- | -------------
   CLM-EEG    | +0.0005          | +0.1245          | no — increased 250×
   CLM-BOLD   | +0.0357          | -0.0293          | YES (sign flip)
   EEG-BOLD   | -0.0001          | +0.0826          | YES (sign flip)
```

CLM-EEG signal grew with N (consistent with weak true effect emerging from noise), but still subthreshold. CLM-BOLD and EEG-BOLD sign-flipped between PARTIAL and SCALE — consistent with both being null-distributed (no stable directional effect).

---

## §4 honest C3 caveats (raw#10)

1. **Single subject per substrate** — ZuCo ZAB only, Algonauts sub-01 only. Population-generic claim NOT supported.
2. **No semantic alignment** — EEG windows are 200ms slices randomly sampled from ZAB's continuous EEG; BOLD windows are 16-TR (~24s) slices randomly sampled from sub-01 Friends viewing; CLM windows are 16-prompt rotation sets from a 96-prompt biographical pool. **The three substrates are NOT measuring the same content/state at any given window index.** This experiment tests "is the phi formula structurally correlated across independent data" — NOT "does phi at substrate A predict phi at substrate B for the same conscious moment." A FAIL here is uninformative re: phenomenal-tier alignment; only the structural-tier null is rejected (or in this case, not rejected).
3. **phi formula = functional/access tier across all three** — BOLD is hemodynamic (~6s lag, parcel-mean over 1000 Schaefer regions); EEG is scalp electrical (105 channels, 200ms × 500Hz = 100 samples); CLM is post-ln_f mean-pooled hidden state (768-d, top-8 variance dims). Same formula, three different geometries. raw#10 caveat: this is a structural-property cross-check, NOT a phenomenal-phi triangulation.
4. **F-CT-MULTI-1 is silver-tier** — strong biological claim requires F-CT-3 (|r| ≥ 0.50, p < 0.01) which would in turn require BLM Phase 4 FULL (head training on Algonauts BOLD with semantic-aligned text-vertex pairs, $500-2000 GPU budget).

---

## §5 interpretation + next-step routing

### §5.1 what this CONFIRMS

- **structural cross-substrate phi consistency = NOT detectable at n=128 with random sampling** (3/3 pairs FAIL all tiers).
- the 4× scale-up did NOT recover signal — the PARTIAL n=32 result (r=0.0005) was not just an underpowered nullcase; even the largest pair (CLM-EEG +0.124) at n=128 with 1000-perm null does not clear bronze.
- phi formula scale-anchor IS substrate-specific (raw#10 caveat 3 empirically confirmed: CLM mean 30.9, EEG mean −3.0, BOLD mean 21.3 — offsets of 30+ phi-units between substrates).

### §5.2 what this does NOT rule out

- a semantically-aligned 3-substrate experiment (CLM forward on ZuCo SR sentence text + EEG window AROUND that sentence reading + BOLD response to ZuCo sentence stimuli, if such triple-aligned stimulus existed) could still produce r > 0.20. The current experiment intentionally uses random sampling for $0 baseline.
- BLM Phase 4 FULL (train BLM head to predict BOLD vertices from Llama-3.2-3B text encoder activations on Algonauts text-aligned stimuli) is the proper test of `cond.2` and remains unscheduled.

### §5.3 routing

- `.roadmap.blm_brain_lm` Phase 3 cond.2 status: **unmet** (pre-existing) — preserved unchanged. This cycle does not flip cond.2; PARTIAL+SCALE both FAIL is consistent with cond.2 needing the FULL Phase 4 training.
- Phase 4 entry-trigger contract: `GRANTED-ELIGIBLE` status from blm_phase3_landed unchanged. GPU budget $500-2000 for Phase 4 FULL still requires explicit user authorization.
- routing recommendation (완성도 lens):
   1. **bag-of-substrates baseline declared FAIL** (this cycle) → record + move on. Do NOT spend further $0 cycles on random-sampling scale-ups; the asymptote is clear.
   2. **defer Phase 4 FULL until $500-2000 GPU budget approved** OR until ZuCo-Algonauts-CLM aligned stimulus pipeline designed (which would itself be a separate $0 design cycle).
   3. **promote CLM-EEG +0.124 trend signal as a HYPOTHESIS** for the future aligned pipeline (CLM ↔ EEG is the most promising pair, BOLD shows no consistent signal under random sampling).

---

## §6 cost + invariants

```
   metric            | value
   ----------------- | -------------------------------------------
   $ cost            | $0.00 (ubu1 local CPU only, no API/GPU cloud)
   wall time         | 966.6 s (~16 min) — 128 windows CPU CLM forward dominates (~9 s/window)
   GPU cost          | 0 (CUDA OOM at startup due to P9 PR-1.5 sentinel training; fell back to CPU automatically)
   raw#9             | UPHELD — only .py emitted (run_phase4_scale.py, transient on ubu1 /tmp)
   raw#10            | UPHELD — phi-as-functional-tier explicitly stated in 4 caveats
   raw#15            | UPHELD — results.json is single SSOT artifact
   raw#71            | UPHELD — F-CT-MULTI-1 falsifier formally registered with strong/silver/bronze tiers
   destructive ops   | 0
   sister .roadmap   | 0 modifications
```

---

## §7 next-cycle docket (recommendation)

```
   priority | action                                                             | $ | gating
   -------- | ------------------------------------------------------------------ | - | -----------------
   P0       | mark cond.2 PARTIAL+SCALE FAIL evidence in .roadmap.blm_brain_lm   | 0 | additive append only
            | as JSONL phase4_landed entry (no in-place edit of cond.2 status)   |   |
   P1       | (defer) design CLM-EEG aligned pipeline using ZuCo SR sentence-    | 0 | pending user "yes go"
            | level text → CLM forward + co-registered EEG window — silver-tier  |   | (still random pool BOLD)
            | candidate at n≈500 sentences                                       |   |
   P2       | (defer) Phase 4 FULL — BLM head training on Algonauts text-vertex  | $500-2000 | explicit GPU budget approval
            | pairs (proper F-CT-3 test)                                         |   |
```

---

(end of file)
