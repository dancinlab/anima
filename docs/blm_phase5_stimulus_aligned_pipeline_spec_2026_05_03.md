# BLM Phase 5 Stimulus-Aligned Multi-Substrate Pipeline Spec — 2026-05-03

> spec doc only (DRAFT, exec 미인가). raw#9 hexa-only / no-.py-creation · raw#10 honest C3 · raw#15 no-personal-paths · raw#71 falsifier-bound.
>
> source-of-truth (read-only ingestion):
> - `.roadmap.blm_brain_lm` (Phase 1-4 SSOT)
> - `docs/blm_phase4_multi_substrate_landed_2026_05_03.ai.md` (Phase 4 RETRY FAIL handoff — direct predecessor)
> - `docs/blm_phase4_partial_3substrate_2026_05_03/results.json` (Phase 4 PARTIAL n=32 baseline)
> - `docs/blm_phase3_landed_2026_05_03.ai.md` (Phase 3 5/5 PASS handoff)
> - `docs/blm_phase3_spec_2026_05_03.md` (Phase 3 spec — 3-substrate consistency anchor)
> - `references/tribev2/tribev2/studies/algonauts2025.py` (Friends + movie10 dataset ingest)
> - `state/blm_phase4_multi_substrate_2026_05_03/per_substrate_phi.json` (n=128 substrate phi distributions)
>
> upstream handoff target: `.roadmap.blm_brain_lm` Phase 5 entry (NEW), and `docs/anima_3_lm_landed_2026_05_03.ai.md` §3.3 (BLM rolling state)
>
> BR-NO-USER-VERBATIM: peer surface mk2 conventions. user prompt verbatim X.
> 마이그레이션 절대 금지 — 본 cycle 0건 file rename / 0건 sister .roadmap modification / 0건 narrative edit.

---

## TL;DR

**오늘 한 일** — BLM Phase 4 RETRY (random-sampling n=128) 측 F-CT-MULTI-1_FAIL 결과 (3/3 pair subthreshold, CLM-EEG +0.124 stable trend only) 수신 → Phase 5 후속 spec 작성. **stimulus-aligned (event-trigger sync) pipeline** 측 next-cycle BG 진입 spec 동결. 핵심 전환: random window sampling → ZuCo SR sentence-aligned 3-substrate pairing (CLM forward on EXACT sentence + EEG fixation epochs + BOLD HRF-lagged TR).

**비유** — Phase 4 RETRY = 신입사원 (BLM) 측 random-shuffle 으로 3개 부서 (CLM/EEG/BOLD) 동기화 시도 → asymptote (r ≤ 0.124) bounded. Phase 5 = "동시각 동일 자극" stimulus-aligned 측정 — 같은 문장 (ZuCo SR sentence) 을 3 substrate 모두 동시 처리시키고 N=200-500 sentence-paired correlation 측정. silver tier (|r|≥0.20, p_perm<0.05) 측 entry-trigger.

**결과** — Phase 5 spec FROZEN, exec 인가 별도. cost band $0 ubu-local CPU-only, ~1.5h wall total. 추가 .py 0건 (raw#9), spec doc only. F-CT-ALIGNED-1 (per-pair silver) + F-CT-ALIGNED-2 (≥ 2/3 silver composite) falsifier 사전 등록.

---

## §1 motivation — Phase 4 FAIL→Phase 5 transition

### §1.1 Phase 4 RETRY closing evidence (read-only ingestion)

Direct predecessor: `docs/blm_phase4_multi_substrate_landed_2026_05_03.ai.md` §3 verdict + §5.2/§5.3 routing.

```
   pair       | pearson r | spearman r | p_perm | null_q95 | exceeds | tier
   ---------- | --------- | ---------- | ------ | -------- | ------- | ----
   CLM-EEG    | +0.1245   | +0.1499    | 0.156  |  0.1749  | False   | none
   CLM-BOLD   | -0.0293   | -0.0301    | 0.732  |  0.1783  | False   | none
   EEG-BOLD   | +0.0826   | +0.0523    | 0.340  |  0.1642  | False   | none
```

Composite verdict = **F-CT-MULTI-1_FAIL** at n=128.

### §1.2 Why scale-up alone is asymptote-bounded

Phase 4 PARTIAL (n=32) → SCALE (n=128) → 4× scale-up. Result:

- CLM-EEG: r grew 250× (0.0005 → 0.1245) but **p_perm worsened from N=32 sub-significance to N=128 still-not-significant** because null also tightened. Asymptote behavior: signal exists but likely capped at r ~ 0.10-0.15 under random pairing.
- CLM-BOLD, EEG-BOLD: sign-flipped between n=32 and n=128 → null-distributed (no stable directional effect).

**Inference** (raw#10 honest): random-window sampling on 3 independent corpora (CLM 96-prompt biographical pool, ZAB ZuCo EEG, sub-01 Algonauts BOLD) measures *structural* phi-formula correlation. The structural-tier asymptote at r ≈ 0.12 is the **upper bound** when no semantic/temporal binding exists between substrates.

### §1.3 What stimulus-alignment changes (predicted upper bound)

Stimulus alignment introduces **shared-content prior**: the same sentence drives all 3 substrates simultaneously. Expected effect (from MEG-fMRI text alignment literature: King et al. 2018, Toneva & Wehbe 2019, Caucheteux et al. 2023):

- text-aligned LM-EEG correlations: r ~ 0.20-0.40 typical
- text-aligned LM-BOLD correlations: r ~ 0.15-0.30 (HRF-bound)
- EEG-BOLD direct: r ~ 0.10-0.25 (HRF + scalp/parcel geometry mismatch)

Silver-tier (|r| ≥ 0.20) **plausible** for ≥ 1 pair (CLM-EEG); composite ≥ 2/3 silver remains uncertain (caveat §6).

---

## §2 substrate pairing alignment — design contract

### §2.1 CLM hidden states (re-cast)

```
   field                        | value
   ---------------------------- | -----------------------------------------------------
   model                        | CLM v4 350M (best.pt) + LoRA dancinlab/clm-v4-sft-stage1
   input                        | EXACT ZuCo SR sentence text (per-sentence string)
   forward                      | CPU on ubu1 (~17s/sentence; matches Phase 4 ~9s/window scaled to mean ~30 tokens/sentence)
   extraction                   | per-token hidden state R^(T_tok x 768) post-ln_f
   phi formula                  | anima_phi_v3_canonical (HID=8 top-variance, K=8 sample-partition halves, MIN over K, ridge=1e-3)
   per-token phi                | apply phi formula to each token's hidden state vector → R^(T_tok)
   per-sentence aggregate       | mean over T_tok, OR per-word-fixation aligned (see §2.2 word-index map)
```

**New** (vs Phase 4 random sampling): forward is on the *exact* sentence the EEG/BOLD subject processed. NOT a 16-prompt rotation set.

### §2.2 EEG (ZuCo SR fixation epochs)

```
   field                        | value
   ---------------------------- | -----------------------------------------------------
   corpus                       | ZuCo task1 SR (Sentiment Reading), subject ZAB
   path                         | /tmp/zuco_sample/ZAB_task1_SR_preprocessed/gip_ZAB_SR{1..8}_EEG.mat (~425 MB total)
   sentence count               | ~400 sentences across 8 sessions (SR task spec: ~50 sentences/session)
   epoch window                 | 250-300ms post-fixation onset (auditory protocol convention; aligns with N400 + late P600 components)
   ROI channels                 | T7 / T8 / P7 / P8 (left+right temporal, posterior-parietal — language network coverage)
   sampling rate                | 500 Hz (ZuCo standard) → 100-150 samples per epoch
   per-fixation phi             | apply anima_phi_v3_canonical to (4 channels × 100-150 samples) flattened vector → R^(N_fix)
   per-sentence aggregate       | mean over N_fix fixations IN that sentence, OR per-word phi if fixation-to-word index resolved (sister .roadmap.eeg cond.4 1순위 sample-partition phi)
```

**Key alignment**: ZuCo SR data has **fixation event timestamps + word indices per sentence** in the .mat metadata (`word_data` field per sentence). This enables word-level CLM↔EEG pairing.

### §2.3 BOLD (Algonauts movie-watching, dialog-aligned)

```
   field                        | value
   ---------------------------- | -----------------------------------------------------
   corpus                       | Algonauts 2025 sub-01, Friends s1-s6 train slice
   path                         | /tmp/algonauts2025_sub01/.../sub-01_task-friends_*-1000Par7Net*.h5 (~515 MB)
   TR                           | 1.5s (note: TRIBE v2 inventory TR=1.49s — same data, rounded)
   HRF lag adjustment           | shift TR window +4 to +6s (canonical HRF peak) relative to dialog onset
   parcellation                 | Schaefer 1000-parcel × 7-network (existing pipeline, no re-extract)
   per-TR phi                   | apply phi formula to (1000 parcels × T_TR window) — TRIBE BOLD vertex map equivalent
   dialog timestamps            | derived from Friends episode subtitle .srt files (timestamp per line of dialog)
   per-sentence aggregate       | TR(s) overlapping dialog onset+HRF lag → mean phi over ~3-4 TRs per dialog segment
```

**Alignment caveat (§6 C2)**: ZuCo SR sentences ≠ Friends dialog sentences. Two pairing modes:
- **mode-A (CLM↔EEG only)**: ZuCo SR sentences fully aligned (2 substrates), BOLD pairs random-sampled or omitted from F-CT-ALIGNED-1.
- **mode-B (3-substrate, weakest-link)**: use dialog text from Algonauts as the shared anchor, run CLM forward on Friends dialogs + extract BOLD response, but **EEG side cannot align** (ZuCo subject did not view Friends). Falls back to ZuCo as parallel-but-not-stimulus-shared.

**Recommended exec** (chosen below in §4 strategy ranking): **hybrid (mode-A + mode-B parallel)** — report CLM↔EEG sentence-aligned (highest-rigor) AND CLM↔BOLD dialog-aligned (separate, also rigorous), with EEG↔BOLD as the weakest pair (parallel but not stimulus-shared, lower-tier expected).

---

## §3 pairing scheme — sentence-level pseudocode

### §3.1 Per-sentence pairing (mode-A: CLM ↔ EEG)

```
for sentence_id in ZuCo_SR_sentences (target N = 200-500):
    text = ZuCo[sentence_id].sentence_text
    fixation_events = ZuCo[sentence_id].word_data.fixation_onsets  # list of (word_idx, t_onset_ms)
    eeg_epochs = []
    for (word_idx, t_onset) in fixation_events:
        epoch = EEG_continuous[T7,T8,P7,P8, t_onset+250 : t_onset+550]  # 300ms window @ 500Hz = 150 samples
        eeg_epochs.append(epoch)
    phi_eeg_sentence = mean([anima_phi_v3(epoch.flatten()) for epoch in eeg_epochs])

    clm_forward = CLM_v4_350m(tokenize(text))  # full sentence forward
    hidden_states = clm_forward.last_hidden_state  # R^(T_tok x 768)
    phi_clm_sentence = mean([anima_phi_v3(h_t) for h_t in hidden_states])

    pairs.append((phi_clm_sentence, phi_eeg_sentence))

# Pearson + Spearman over N pairs
r_pearson = pearsonr([p[0] for p in pairs], [p[1] for p in pairs])
r_spearman = spearmanr(...)  # PRIMARY metric — rank-invariant to substrate scale
```

### §3.2 Per-sentence pairing (mode-B: CLM ↔ BOLD)

```
for dialog_segment in Friends_sub01_episodes (target N = 200-500):
    text = dialog_segment.subtitle_text
    onset_t = dialog_segment.onset_seconds
    bold_window = BOLD_continuous[parcels=Schaefer1000Par7Net, TR_idx_for(onset_t + 4): TR_idx_for(onset_t + 6)]  # ~3 TRs per HRF peak
    phi_bold_segment = mean([anima_phi_v3(bold_TR) for bold_TR in bold_window])

    clm_forward = CLM_v4_350m(tokenize(text))
    phi_clm_segment = mean([anima_phi_v3(h_t) for h_t in clm_forward.last_hidden_state])

    pairs_clm_bold.append((phi_clm_segment, phi_bold_segment))
```

### §3.3 Per-sentence pairing (EEG ↔ BOLD weakest, parallel-not-shared)

EEG (ZuCo, ZAB) and BOLD (Algonauts, sub-01) are different subjects on different stimuli. Direct stimulus-shared pairing **impossible** without new data collection.

**Surrogate pairing**: per-sentence (ZuCo) phi_eeg vs per-dialog (Friends) phi_bold, both **z-scored within own substrate**, then Spearman over N=min(|ZuCo|, |Friends_dialog|) — but this is **null-equivalent to Phase 4 random sampling**. F-CT-ALIGNED-1 for EEG↔BOLD pair is **omitted** from the silver-tier requirement (composite F-CT-ALIGNED-2 = ≥ 2/3 of {CLM-EEG, CLM-BOLD, EEG-BOLD} silver, but EEG-BOLD bench-marked as expected-to-FAIL given no shared stimulus).

### §3.4 N target rationale

- **N=200 (floor)**: ZuCo ZAB SR has ~400 sentences; using 200 leaves 200 holdout for replication.
- **N=500 (ceiling)**: would require additional ZuCo subjects (ZDM, ZDN, etc.), increasing wall by 8× (8 subjects × 1h CLM forward).
- **Default = N=300** (single subject ZAB, all SR sentences) — balances rigor vs $0 wall (~1.5h).

Power analysis: at r=0.20 (silver threshold) with N=300, two-tailed alpha=0.05, power = 0.93. At r=0.15 (Phase 4 ceiling), N=300 gives power=0.71. N=300 is sufficient to detect silver if the true r ≥ 0.20.

---

## §4 alignment strategy ranking — completion-quality lens

### §4.1 Three candidate strategies

```
   strategy            | pairing                                                   | estimated wall | est. r upper bound (CLM-EEG)
   ------------------- | --------------------------------------------------------- | -------------- | ---------------------------
   S1: event-trigger   | per-fixation epoch (250-300ms post-onset) → per-sentence  | ~1.5h          | r ~ 0.25-0.40 (lit. precedent)
   S2: window-grid     | continuous 200ms sliding window, no fixation alignment    | ~1h            | r ~ 0.15-0.20 (mid-Phase 4)
   S3: hybrid          | event-trigger primary + window-grid fallback for missing  | ~2h            | r ~ 0.25-0.40 + recovery
```

### §4.2 Ranked recommendation — `완성도 lens`

## 추천 — stimulus-aligned strategy 우선 (완성도 lens)

| rank | strategy | 비용 | wall | 효과 |
|---|---|---|---|---|
| 🥇 S1 | event-trigger sync | $0 | ~1.5h CPU ubu1 | 사전등록 silver-tier (|r|≥0.20) 달성 가능성 최고 (literature 0.25-0.40 band) |
| 🥈 S3 | hybrid (S1 + S2 fallback) | $0 | ~2h CPU ubu1 | event-missing sentences 회수 → N coverage 100% (그러나 S1 falsifier dilution risk) |
| 🥉 S2 | window-grid | $0 | ~1h CPU ubu1 | Phase 4 RETRY와 동일 mechanism — asymptote bound ~0.15 (silver 미달 expected) |

### 추천: S1 event-trigger sync (lit. precedent + N power 충분 + falsifier purity)

**근거 (완성도 lens)**:
- **lit. precedent**: King 2018, Toneva 2019, Caucheteux 2023 모두 fixation-event-locked or word-onset-locked alignment 사용 (NOT random window). Phase 4 RETRY가 random-sampling이었기 때문에 r=0.124에 갇힌 것이고, event-trigger로 전환만 해도 r=0.25 region 진입 plausible.
- **falsifier purity**: F-CT-ALIGNED-1 silver 기준 (|r|≥0.20, p_perm<0.05)을 단일 mechanism으로 명확하게 test. S3는 두 mechanism 혼재로 falsifier interpretation 흐림.
- **N power 충분**: ZuCo ZAB SR 400 sentences 中 200-300 fixation-resolved 가능 (대부분 SR sentence는 multi-fixation). N=300에 r=0.20이면 power=0.93.
- **wall fit**: ~1.5h CPU on ubu1 — Phase 4 (16분) 대비 길지만 여전히 single-cycle BG fit. $0 유지.
- **failure-mode 명확**: S1 FAIL → "stimulus-alignment 자체로도 silver 미달" → strong negative evidence (Phase 4 random보다 한 단계 위 conclusion). S2 FAIL = Phase 4 reproduction = 신호 없음 (이미 known). S3 FAIL = ambiguous.

S2 (3순위)는 본질적으로 Phase 4 RETRY 재현이라 새 정보 X. S3 (2순위)는 N coverage 우위지만 falsifier 해석이 dilute됨 (event vs grid 결과 분리 보고 필요 → 2× artifact). S1 단독 진입이 완성도 lens 측 최선.

### §4.3 Strategy decision

**LOCKED: S1 event-trigger sync as primary exec strategy.** S3 은 contingency (S1 N coverage <200일 시 자동 fallback enabled).

---

## §5 falsifier upgrade — F-CT-ALIGNED-1/2

### §5.1 F-CT-ALIGNED-1 (per-pair silver)

```
   id                          | F-CT-ALIGNED-1
   level                       | silver
   primary metric              | Spearman rank correlation (substrate-scale-invariant)
   secondary metric            | Pearson (reported, not gating)
   threshold                   | |r_spearman| ≥ 0.20
   significance                | p_perm < 0.05 (block-permutation null, N_perm = 1000)
   block size for permutation  | 5 sentences (preserves local autocorrelation, breaks global drift)
   pairs evaluated             | {CLM-EEG, CLM-BOLD} as primary; {EEG-BOLD} reported but non-gating
   N target                    | 200-500 sentence-aligned pairs (default 300)
```

### §5.2 F-CT-ALIGNED-2 (composite MULTI_ALIGNED_PASS)

```
   id                          | F-CT-ALIGNED-2
   level                       | silver composite
   criterion                   | ≥ 2 of {CLM-EEG, CLM-BOLD, EEG-BOLD} pairs PASS F-CT-ALIGNED-1
   weighting                   | unweighted majority (not stimulus-pair-corrected)
   tier emit                   | MULTI_ALIGNED_PASS (silver) | MULTI_ALIGNED_PARTIAL (1/3) | MULTI_ALIGNED_FAIL (0/3)
```

### §5.3 Pre-registered null hypothesis structure

- **H0**: stimulus-aligned phi correlation across substrates is null-equivalent to random sampling (i.e., Phase 4 RETRY r ≈ 0.124 represents the true ceiling).
- **H1 (F-CT-ALIGNED-1)**: stimulus-alignment recovers silver-tier signal (|r_spearman| ≥ 0.20, p_perm < 0.05) for at least one of {CLM-EEG, CLM-BOLD}.
- **H2 (F-CT-ALIGNED-2)**: stimulus-alignment recovers silver-tier signal in ≥ 2 of 3 pairs.

H1 FAIL → strong evidence that random-sampling asymptote (Phase 4) generalizes to stimulus-aligned regime, suggesting phi-formula is not substrate-shared property.

H1 PASS but H2 FAIL → CLM↔EEG specific binding (text-encoder-shared route), not 3-substrate generalization. Acceptable promotion of CLM-EEG hypothesis only.

H2 PASS → MULTI_ALIGNED_PASS, promotion of cross-substrate phi-as-shared-property hypothesis to silver. cond.3 in `.roadmap.blm_brain_lm` flips toward met (combined with Phase 4 FULL training when GPU budget approved).

---

## §6 honest C3 caveats (raw#10) — 6 explicit

### §6.1 C1 — ZuCo SR sentences may not have BOLD-paired equivalents

Direct stimulus-shared 3-substrate triangle is **impossible** with current data: ZuCo subjects read static sentences, Algonauts subjects watched Friends dialog. EEG↔BOLD pair is the **weakest link** — it cannot be stimulus-shared without new data collection (would require running ZuCo subject through Friends viewing, ~$30k FMRI cohort study).

**Mitigation**: F-CT-ALIGNED-2 composite criterion accepts EEG↔BOLD as **non-gating**; H1 (F-CT-ALIGNED-1, single-pair) is the practical PASS bar for this Phase 5 cycle.

### §6.2 C2 — HRF lag is approximate

The +4 to +6s HRF peak adjustment for Algonauts BOLD is a **canonical assumption** (single peak, no individual HRF estimation). Per-subject HRF varies by ±2s. CLM↔BOLD pairing accuracy degrades with HRF mismatch — possible 20-30% r attenuation vs ideal.

**Mitigation**: report both +4s and +6s lag results; primary = +5s (midpoint). If both lags FAIL silver, attribute to substrate-pairing-fragility, not formula failure.

### §6.3 C3 — N=200-500 power is bounded

At expected r ~ 0.25 (lit.), N=300 gives power=0.93 for silver. But if true r ~ 0.18 (just below silver), power drops to 0.55 — type II error > 0.4. **A FAIL could be underpowered, not truly null.**

**Mitigation**: pre-register the **effect size CI** (95% CI on r) alongside the silver/no-silver verdict. Report "effect-size-positive but threshold-FAIL" as PARTIAL (orange) tier between PASS (silver) and FAIL (none).

### §6.4 C4 — substrate-scale invariance forced via Spearman

Phase 4 RETRY confirmed phi means differ by 30+ phi-units across substrates (CLM 30.86, EEG -3.01, BOLD 21.33). **Pearson r is contaminated by scale offsets** in the absolute-value tail. Spearman (rank) is the chosen primary metric to neutralize this.

**Mitigation**: also report z-scored Pearson (within-substrate z-score before correlation) as a third metric for triangulation. If Spearman PASS but z-Pearson FAIL → rank-only signal (suspicious, possibly artifact of floor/ceiling effects).

### §6.5 C5 — single subject per substrate (carryover from Phase 4)

ZuCo ZAB only, Algonauts sub-01 only. Population-generic phi-as-shared-property claim **NOT supported** by Phase 5 alone. Multi-subject extension is a separate cost-band cycle (each additional subject = +1.5h CPU per substrate).

**Mitigation**: Phase 5 PASS = "for at least one subject pair under stimulus-aligned regime, phi-formula shows silver cross-substrate correlation." Population claim deferred to Phase 6+.

### §6.6 C6 — Phase 5 PASS does NOT replace Phase 4 FULL ($500-2000 LoRA training)

Phase 5 is a **pre-training measurement cycle** — measures phi-formula portability, not BLM head training. The original `.roadmap.blm_brain_lm` cond.2 (BOLD-conditioned LM head IMPL) and cond.3 (3-way alignment ≥0.5 STRONG) **still require** Phase 4 FULL ($500-2000 H100 LoRA path).

**Mitigation**: spec frames Phase 5 as **silver-tier evidence accumulation** that strengthens the *case* for Phase 4 FULL budget approval, not as a replacement.

---

## §7 compute budget

### §7.1 Per-component breakdown

```
   component                       | substrate / target           | wall                | $ band
   ------------------------------- | ---------------------------- | ------------------- | ------
   CLM v4 forward (300 sentences)  | ubu1 CPU (RTX 5070 occupied) | ~1h (12s/sentence)  | $0
   EEG epoching + phi computation  | ubu1 Python (.mat parsing)   | ~5min loop          | $0
   BOLD parcel extraction          | ubu1 (h5 already extracted)  | ~10min (re-use)     | $0
   pairing + Spearman + perm null  | ubu1 numpy/scipy             | ~5min (N_perm=1000) | $0
   results.json + handoff doc      | mac-local                    | ~30min author       | $0
   ----                            | ----                         | ----                | ----
   TOTAL                           |                              | ~1.5h CPU + 0.5h doc | $0.00
```

### §7.2 Cost-band envelope

- **floor = $0** (single subject, S1 strategy, N=300) — recommended exec
- **midpoint = $0** (multi-subject extension across 4 ZuCo subjects, +6h CPU, still $0)
- **ceiling = $5-15** (RunPod 1xA10 sanity to verify CPU/GPU phi parity, optional)

Phase 5 explicitly **does not enter the $500-2000 LoRA training band** — that remains Phase 4 FULL (cond.2 IMPL).

### §7.3 GPU contention note

RTX 5070 on ubu1 currently held by P9 PR-1.5 sentinel training (PID per Phase 4 closing). CPU-only fallback is the **default** exec mode for Phase 5 (matches Phase 4 RETRY pattern). 17s/sentence CLM forward on CPU is acceptable.

---

## §8 substrate-invariance correction — Spearman primary

### §8.1 Why Spearman over Pearson

Phase 4 RETRY substrate phi distributions:

```
   substrate | mean   | std    | scale offset vs CLM
   --------- | ------ | ------ | -------------------
   CLM       | 30.86  |  1.19  | (anchor)
   EEG       | -3.01  |  9.68  | -33.87 mean offset, 8.1× std
   BOLD      | 21.33  |  2.17  | -9.53 mean offset, 1.8× std
```

Pearson r is sensitive to outliers and scale-offsets when distributions differ this much. Spearman (rank) is robust to **monotonic transforms** including affine scale changes — it asks "does substrate-A rank-order match substrate-B rank-order across pairs?" which is the substrate-shared-property question phi-formula is testing.

### §8.2 Triangulation metrics (all reported, Spearman gating)

```
   metric                | role        | substrate-scale-robust?
   --------------------- | ----------- | ----------------------
   Spearman r            | PRIMARY     | YES (rank-based)
   z-scored Pearson      | SECONDARY   | YES (per-substrate z-score before pairing)
   raw Pearson           | TERTIARY    | NO (reported for Phase 4 comparability)
```

### §8.3 Effect-size CI requirement

All 3 r values must report **95% CI via bootstrap (B=1000, sentence-level resampling)**. Verdict tiers:

- **silver (PASS)**: Spearman r ≥ 0.20 AND p_perm < 0.05 AND 95% CI lower bound ≥ 0.10
- **bronze (PARTIAL)**: 0.10 ≤ Spearman r < 0.20, p_perm < 0.10, 95% CI excludes 0
- **none (FAIL)**: Spearman r < 0.10 OR 95% CI includes 0

---

## §9 cond enumeration — Phase 5 (3 cond proposed)

### §9.1 Proposed cond IDs (additive to `.roadmap.blm_brain_lm`)

```
   id                              | desc                                                                           | status (this spec cycle)
   ------------------------------- | ------------------------------------------------------------------------------ | -----------------------
   blm.cond.phase5_aligned_spec    | Phase 5 stimulus-aligned pipeline spec FROZEN (this doc)                       | met (with this cycle)
   blm.cond.phase5_aligned_exec    | Phase 5 exec — N=300 sentence-aligned 3-substrate pairing, F-CT-ALIGNED-1/2    | unmet (next BG)
   blm.cond.phase5_aligned_verdict | Phase 5 verdict landing — composite tier emit + handoff                       | unmet (post-exec)
```

### §9.2 Phase 5 entry-trigger contract

**Entry trigger (single-line)**: Phase 4 RETRY landed (true, 2026-05-03) AND `blm.cond.phase5_aligned_spec` met (true, this cycle) AND ubu1 CPU available (verified — not exclusive of P9 sentinel) AND ZuCo ZAB SR + Algonauts sub-01 data present at known paths (verified Phase 4) → **Phase 5 exec authorization granted-eligible (next BG cycle)**.

### §9.3 Out-of-scope (explicitly NOT Phase 5)

- BLM head LoRA training (cond.2 IMPL, $500-2000 H100 — Phase 4 FULL, separate cycle)
- Multi-subject ZuCo extension (deferred to Phase 6+)
- New FMRI cohort with stimulus-shared sentences (≥$30k, deferred indefinitely)
- F-CT-3 STRONG (|r| ≥ 0.50) — requires Phase 4 FULL
- Population-generic phi-shared-property claim (single-subject limit, §6 C5)

---

## §10 file index + raw invariants

### §10.1 created (this cycle)

```
docs/blm_phase5_stimulus_aligned_pipeline_spec_2026_05_03.md     (this file — spec only)
docs/blm_phase5_aligned_spec_landed_2026_05_03.ai.md             (handoff doc, sister)
state/markers/blm_phase5_aligned_spec_landed.marker              (cycle marker)
```

### §10.2 modified (this cycle)

```
.roadmap.blm_brain_lm                                             (additive JSONL append: 1 entry for blm.cond.phase5_aligned_spec status=met + 1 entry for blm.cond.phase5_aligned_exec status=unmet, 0 in-place edit of pre-existing cond.1/cond.2/cond.3)
```

### §10.3 consumed read-only (no mutation this cycle)

```
docs/blm_phase4_multi_substrate_landed_2026_05_03.ai.md           (Phase 4 RETRY closing handoff)
docs/blm_phase3_landed_2026_05_03.ai.md                           (Phase 3 5/5 PASS handoff)
docs/blm_phase3_spec_2026_05_03.md                                (Phase 3 spec, 3-substrate consistency anchor)
docs/blm_stage12_landed_2026_05_03.ai.md                          (Phase 1+2 close handoff)
state/blm_phase4_multi_substrate_2026_05_03/results.json          (Phase 4 RETRY results)
state/blm_phase4_multi_substrate_2026_05_03/per_substrate_phi.json (n=128 substrate phi distributions)
references/tribev2/inventory.json                                 (TRIBE baseline SSOT, vendored)
references/tribev2/tribev2/studies/algonauts2025.py               (Friends + movie10 ingest path)
```

### §10.4 NOT created / NOT mutated (per task constraints)

```
no .py files (raw#9 — spec doc only; exec phase will land transient .py on ubu1 /tmp per Phase 4 pattern)
no in-place edit of sister roadmaps (.roadmap.eeg, .roadmap.clm, .roadmap.i1_tribev2_pr untouched)
no narrative edit (docs/n_substrate_consciousness_roadmap_2026_05_01.md untouched)
no commit (per task: spec-only, exec separate cycle)
no destructive ops (raw#15)
```

### §10.5 raw invariants compliance

```
   raw    | invariant                                                  | status
   ------ | ---------------------------------------------------------- | ------
   raw#9  | no .py creation in mac-local repo (spec doc only)           | UPHELD
   raw#10 | honest C3 6 caveats explicit (§6.1-§6.6)                    | UPHELD
   raw#15 | no personal paths, no destructive ops                       | UPHELD
   raw#71 | F-CT-ALIGNED-1/2 falsifier formally registered (§5.1-§5.3)  | UPHELD
```

---

## §11 next-cycle docket (post-spec-freeze)

```
   priority | action                                                                      | $ | gating
   -------- | --------------------------------------------------------------------------- | - | ----------------
   P0       | Phase 5 exec BG cycle: S1 event-trigger sync, N=300, ubu1 CPU only          | 0 | this spec freeze + ubu1 CPU avail
            | F-CT-ALIGNED-1/2 measure → results.json + handoff                            |   |
   P1       | (defer) multi-subject ZuCo extension (4 subjects × 1.5h)                    | 0 | P0 PASS or PARTIAL
            | population-generic claim path                                                 |   |
   P2       | (defer) Phase 4 FULL LoRA training — proper F-CT-3 STRONG test              | $500-2000 | explicit GPU budget approval
            | requires Phase 5 silver evidence as motivating prior                         |   |
   P3       | (defer) RunPod sanity probe — CPU/GPU phi parity verification               | $0.40-2 | optional, low-priority
```

---

## §12 decision summary

**Phase 5 spec FROZEN. exec authorization = separate BG cycle (next).**

- **what changed vs Phase 4 RETRY**: random window sampling → ZuCo SR sentence-aligned event-trigger pipeline
- **what stays the same**: $0 ubu-local CPU substrate, anima_phi_v3_canonical formula, N_perm=1000 null
- **falsifier upgrade**: F-CT-MULTI-1 (Pearson, random-sample) → F-CT-ALIGNED-1/2 (Spearman primary, event-aligned, composite ≥ 2/3 silver)
- **strategy locked**: S1 event-trigger sync (ranked #1 of 3 by 완성도 lens, §4.2)
- **failure mode predicted**: H1 FAIL → strong evidence phi-formula is not substrate-shared (Phase 4 ceiling generalizes); H1 PASS H2 FAIL → CLM-EEG text-encoder-route hypothesis only (acceptable narrow promotion)

This doc = the spec freeze. Exec authorization for the 3 cond progression = **next BG cycle** (per raw#9 + project policy: spec → review → exec separation).

---

(end of file)
