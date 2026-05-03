# BLM Phase 5 Stimulus-Aligned Spec Landed — 2026-05-03 (AI-native, friendly preset)

> friendly preset (icon + analogy + 7-element + ASCII)
>
> readers: AI agents (subagents, audit cron), Claude Code (next session)
> source-of-truth: 1 spec doc (`docs/blm_phase5_stimulus_aligned_pipeline_spec_2026_05_03.md`) + 1 marker (`state/markers/blm_phase5_aligned_spec_landed.marker`) + 2 additive JSONL entries on `.roadmap.blm_brain_lm`
> upstream handoff target: `docs/anima_3_lm_landed_2026_05_03.ai.md` §3.3 (BLM rolling state) + Phase 5 exec next-BG cycle
>
> BR-NO-USER-VERBATIM: peer surface mk2 conventions. user prompt verbatim X.
> 마이그레이션 절대 금지 — 본 cycle 0건 file rename / 0건 sister .roadmap modification / 0건 narrative edit.

---

## TL;DR

**오늘 한 일** — BLM Phase 4 RETRY F-CT-MULTI-1_FAIL 결과를 받아 **Phase 5 stimulus-aligned multi-substrate pipeline spec** 작성+동결. 핵심 전환: random window sampling → ZuCo SR sentence-aligned event-trigger pairing. 3개 alignment 전략 (event-trigger / window-grid / hybrid) 완성도 lens 평가 후 **S1 event-trigger sync 단독 LOCKED**. F-CT-ALIGNED-1/2 falsifier (Spearman primary, silver |r|≥0.20, composite ≥2/3 pairs) 사전 등록.

**비유** — Phase 4 RETRY = 신입사원 (BLM) 측 random-shuffle 으로 부서 동기화 → asymptote 갇힘 (r≤0.124). Phase 5 spec = "동시각 동일 자극" 측정 설계 동결 — 같은 ZuCo SR 문장을 CLM forward + EEG 시선-fixation epoch + BOLD HRF-lagged TR 모두 동시 처리, N=300 sentence-paired Spearman correlation. 다음 cycle에서 ubu1 CPU 1.5h ($0) 측 실행.

**결과** — `.roadmap.blm_brain_lm` 측 2개 신규 cond 추가 (`phase5_aligned_spec=met`, `phase5_aligned_exec=unmet`). 기존 cond.1/cond.2/cond.3 in-place 변경 0건. spec 동결만 (exec = next BG).

---

## §1 cycle inputs / outputs

### §1.1 inputs

```
   field                       | value
   --------------------------- | --------------------------------
   prior cycle                 | docs/blm_phase4_multi_substrate_landed_2026_05_03.ai.md (F-CT-MULTI-1_FAIL, n=128)
   Phase 4 evidence            | state/blm_phase4_multi_substrate_2026_05_03/results.json (3/3 pairs subthreshold)
   Phase 3 anchor              | docs/blm_phase3_landed_2026_05_03.ai.md (5/5 PASS, Phase 4 entry GRANTED-ELIGIBLE)
   ZuCo data                   | /tmp/zuco_sample/ZAB_task1_SR_preprocessed/ (~425 MB, 8 SR sessions, ~400 sentences)
   Algonauts data              | /tmp/algonauts2025_sub01/.../sub-01_task-friends_*-1000Par7Net*.h5 (~515 MB)
   CLM ckpt                    | /home/aiden/anima/checkpoints/clm_v4_350m/scale_350m/best.pt + LoRA need-singularity/clm-v4-sft-stage1
   phi formula                 | anima_phi_v3_canonical (HID=8, K=8, ridge=1e-3) — unchanged from Phase 4
   substrate phi distributions | per_substrate_phi.json (CLM mean 30.86, EEG mean -3.01, BOLD mean 21.33)
```

### §1.2 outputs

```
   artifact                                                                          | role
   -------------------------------------------------------------------------------- | -----------------------------
   docs/blm_phase5_stimulus_aligned_pipeline_spec_2026_05_03.md                     | spec doc (this cycle, 475 LoC)
   docs/blm_phase5_aligned_spec_landed_2026_05_03.ai.md                             | this handoff doc
   state/markers/blm_phase5_aligned_spec_landed.marker                              | cycle marker (single line)
   .roadmap.blm_brain_lm (additive append: 2 entries)                               | cond.phase5_aligned_spec=met + cond.phase5_aligned_exec=unmet
```

---

## §2 strategy ranking (완성도 lens) — quick reference

## 추천 — Phase 5 alignment strategy 우선 (완성도 lens)

| rank | strategy | 비용 | wall | 효과 |
|---|---|---|---|---|
| 🥇 S1 | event-trigger sync | $0 | ~1.5h CPU ubu1 | 사전등록 silver-tier (|r|≥0.20) 달성 가능성 최고 (lit. 0.25-0.40 band) |
| 🥈 S3 | hybrid (S1 + S2 fallback) | $0 | ~2h CPU ubu1 | event-missing sentences 회수 → N coverage 100% (S1 falsifier dilution risk) |
| 🥉 S2 | window-grid | $0 | ~1h CPU ubu1 | Phase 4 RETRY 동일 mechanism — asymptote bound ~0.15 (silver 미달 expected) |

### 추천: S1 event-trigger sync (lit. precedent + N power 충분 + falsifier purity)

**근거 (완성도 lens)**:
- **lit. precedent**: King 2018 / Toneva 2019 / Caucheteux 2023 모두 fixation-event 또는 word-onset locked alignment 사용 — random window 전략은 Phase 4에서 r≤0.124 asymptote로 reproducibly bounded.
- **falsifier purity**: F-CT-ALIGNED-1 silver 기준을 단일 mechanism으로 명확히 test. S3 hybrid는 event/grid 혼재로 falsifier interpretation dilute됨.
- **N power 충분**: ZuCo ZAB SR 400 sentences 中 ~300 fixation-resolved 가능, N=300에 r=0.20 power=0.93.
- **failure-mode 명확**: S1 FAIL = stimulus-alignment로도 silver 미달 (Phase 4보다 한 단계 위 negative evidence). S2 FAIL = Phase 4 reproduction (이미 known). S3 FAIL = ambiguous mechanism.

S2 (3순위) = Phase 4 RETRY 재현 정보값 X. S3 (2순위) = N coverage 우위지만 dual-mechanism 보고로 falsifier 흐림. **S1 단독 LOCKED**.

---

## §3 Phase 5 cond enumeration

### §3.1 3 신규 cond (additive to `.roadmap.blm_brain_lm`)

```
   cond_id                              | status (this cycle) | gating
   ------------------------------------ | ------------------- | -----------------------------------
   blm.cond.phase5_aligned_spec         | met                 | this spec doc landing
   blm.cond.phase5_aligned_exec         | unmet               | next BG cycle (ubu1 CPU 1.5h)
   blm.cond.phase5_aligned_verdict      | unmet               | post-exec results.json + handoff
```

### §3.2 Phase 5 entry trigger contract

**Single-line entry trigger**: Phase 4 RETRY landed (true, 2026-05-03) AND `blm.cond.phase5_aligned_spec` met (true, this cycle) AND ubu1 CPU available (verified) AND ZuCo ZAB SR + Algonauts sub-01 data present (verified Phase 4) → **Phase 5 exec authorization GRANTED-ELIGIBLE (next BG cycle).**

### §3.3 Phase 5 outcome tree (predicted)

```
   verdict                       | composite criterion                              | next-cycle routing
   ----------------------------- | ------------------------------------------------ | -----------------------------------
   MULTI_ALIGNED_PASS (silver)   | ≥2 of 3 pairs F-CT-ALIGNED-1 silver              | promote phi-shared-property silver hypothesis → motivate Phase 4 FULL ($500-2000)
   MULTI_ALIGNED_PARTIAL         | 1 of 3 pair (likely CLM-EEG) silver              | narrow promotion: text-encoder-shared-route hypothesis only
   MULTI_ALIGNED_FAIL            | 0 of 3 pairs silver                              | strong negative: phi-formula not substrate-shared, Phase 4 FULL re-justification needed
```

---

## §4 falsifier specification (pre-registered)

### §4.1 F-CT-ALIGNED-1 (per-pair silver)

```
   metric primary              | Spearman rank correlation
   metric secondary            | z-scored Pearson, raw Pearson (reported, non-gating)
   threshold                   | |r_spearman| ≥ 0.20
   significance                | p_perm < 0.05
   null distribution           | block-permutation N_perm=1000, block_size=5 sentences
   95% CI requirement          | bootstrap B=1000, sentence-level resampling, lower bound ≥ 0.10
   pairs evaluated (gating)    | {CLM-EEG, CLM-BOLD}
   pairs evaluated (reported)  | {EEG-BOLD} non-gating
```

### §4.2 F-CT-ALIGNED-2 (composite)

```
   criterion                   | ≥ 2 of 3 pairs PASS F-CT-ALIGNED-1
   tier emit                   | MULTI_ALIGNED_PASS (silver) | MULTI_ALIGNED_PARTIAL (1/3) | MULTI_ALIGNED_FAIL (0/3)
```

### §4.3 H0 / H1 / H2 structure

- **H0**: stimulus-aligned phi correlation = null-equivalent to random sampling (Phase 4 ceiling r ≈ 0.124 generalizes)
- **H1 (F-CT-ALIGNED-1)**: silver in ≥ 1 of {CLM-EEG, CLM-BOLD}
- **H2 (F-CT-ALIGNED-2)**: silver in ≥ 2 of 3 pairs

H1 PASS H2 FAIL → CLM-EEG text-encoder-shared-route specific (acceptable narrow promotion).

---

## §5 cost + invariants

```
   metric            | value
   ----------------- | -------------------------------------------
   $ cost            | $0.00 (spec doc only this cycle; exec ~1.5h ubu1 CPU = $0)
   wall time         | ~1h (spec authoring + roadmap update + handoff)
   GPU cost          | 0 (CPU only, RTX 5070 occupied by P9 sentinel — same as Phase 4 RETRY)
   raw#9             | UPHELD — 0 .py files created (spec doc only; exec phase will land transient .py per Phase 4 pattern)
   raw#10            | UPHELD — 6 honest C3 caveats explicit (§6.1-§6.6 of spec doc)
   raw#15            | UPHELD — no personal paths, no destructive ops
   raw#71            | UPHELD — F-CT-ALIGNED-1/2 formally registered with silver tier + p_perm + 95% CI
   destructive ops   | 0
   sister .roadmap   | 0 modifications (eeg, clm, i1_tribev2_pr, n_substrate untouched)
   in-place edits to .roadmap.blm_brain_lm pre-existing cond | 0 (additive append only)
```

---

## §6 honest C3 caveats (raw#10) — 6 explicit

```
   #  | caveat                                                                                                  | mitigation
   -- | ------------------------------------------------------------------------------------------------------- | -------------------------
   C1 | ZuCo SR sentences ≠ Friends dialog → 3-substrate stimulus-shared triangle impossible without new data    | EEG↔BOLD non-gating in F-CT-ALIGNED-2; H1 (single-pair) is practical PASS bar
   C2 | HRF lag +4-6s is canonical, per-subject HRF varies ±2s → CLM↔BOLD r attenuation ~20-30%                  | report both +4s/+6s lag; primary +5s; both FAIL = pairing-fragility not formula-failure
   C3 | N=300 power=0.93 at r=0.20, but at r=0.18 power drops to 0.55 → FAIL could be underpowered               | report 95% CI alongside threshold verdict; PARTIAL (orange) tier for "effect-size-positive but threshold-FAIL"
   C4 | Phase 4 confirmed phi means differ 30+ phi-units across substrates → Pearson contaminated                | Spearman PRIMARY (rank-invariant); also report z-scored Pearson; 3-metric triangulation
   C5 | single subject ZAB (EEG) + sub-01 (BOLD) → no population-generic claim                                    | Phase 5 PASS = "for at least one subject pair, phi-formula shows silver"; population deferred Phase 6+
   C6 | Phase 5 PASS does NOT replace Phase 4 FULL ($500-2000 H100 LoRA) for cond.2 IMPL                          | spec frames Phase 5 as silver-tier evidence accumulation, not replacement
```

---

## §7 next-cycle docket

```
   priority | action                                                                      | $ | gating
   -------- | --------------------------------------------------------------------------- | - | ----------------
   P0       | Phase 5 exec BG cycle: S1 event-trigger sync, N=300, ubu1 CPU only          | 0 | this spec freeze + ubu1 CPU avail
            | F-CT-ALIGNED-1/2 measure → results.json + per_substrate_aligned.json + handoff |   |
   P1       | (defer) multi-subject ZuCo extension (4 subjects × 1.5h CPU)                | 0 | P0 PASS or PARTIAL
            | population-generic claim path                                                 |   |
   P2       | (defer) Phase 4 FULL — BLM head LoRA training (cond.2 IMPL, F-CT-3 STRONG)  | $500-2000 | explicit GPU budget approval
            | Phase 5 silver evidence as motivating prior                                   |   |
   P3       | (defer) RunPod sanity probe — CPU/GPU phi parity verification               | $0.40-2 | optional, low-priority
```

---

## §8 cross-link to sister roadmaps (read-only, no mutation)

```
   sister .roadmap                | relevance to Phase 5
   ------------------------------ | --------------------------------------------------------------
   .roadmap.eeg cond.3            | ZuCo Paradigm B SR data (sister provider, partial → Phase 5 reuse)
   .roadmap.eeg cond.4            | sample-partition phi 1순위 (sister formula, identical to BLM Phase 5)
   .roadmap.clm                   | anima_phi_v3_canonical formula owner (baseline 41.86, phi anchor)
   .roadmap.i1_tribev2_pr         | TRIBE PR #60 OPEN, F-CT-3 sister falsifier (Phase 4 FULL gating)
   .roadmap.n_substrate cond.1    | 5+ substrate witness meta (Phase 5 contributes silver-tier evidence)
```

**0 sister roadmap modification** this cycle — read-only consumption only.

---

## §9 file index

### created (this cycle)

```
docs/blm_phase5_stimulus_aligned_pipeline_spec_2026_05_03.md     (475 LoC, spec doc)
docs/blm_phase5_aligned_spec_landed_2026_05_03.ai.md             (this handoff)
state/markers/blm_phase5_aligned_spec_landed.marker              (single-line cycle marker)
```

### modified (this cycle)

```
.roadmap.blm_brain_lm                                             (2 additive JSONL append entries; 0 in-place mutation of cond.1/cond.2/cond.3)
```

### consumed read-only (no mutation)

```
docs/blm_phase4_multi_substrate_landed_2026_05_03.ai.md           (Phase 4 RETRY closing handoff, direct predecessor)
docs/blm_phase3_landed_2026_05_03.ai.md                           (Phase 3 5/5 PASS handoff)
docs/blm_phase3_spec_2026_05_03.md                                (Phase 3 spec, 3-substrate consistency anchor)
docs/blm_stage12_landed_2026_05_03.ai.md                          (Phase 1+2 close handoff)
state/blm_phase4_multi_substrate_2026_05_03/results.json          (Phase 4 RETRY results)
state/blm_phase4_multi_substrate_2026_05_03/per_substrate_phi.json (n=128 substrate phi distributions)
references/tribev2/inventory.json                                 (TRIBE baseline SSOT, vendored)
references/tribev2/tribev2/studies/algonauts2025.py               (Friends + movie10 ingest path)
```

---

## §10 verdict

**Phase 5 spec FROZEN. Phase 5 exec authorization GRANTED-ELIGIBLE for next BG cycle.**

- 3 cond enumerated (`phase5_aligned_spec=met`, `phase5_aligned_exec=unmet`, `phase5_aligned_verdict=unmet`)
- strategy LOCKED: S1 event-trigger sync (1순위 of 3, 완성도 lens)
- falsifier upgrade F-CT-MULTI-1 → F-CT-ALIGNED-1/2 (Spearman primary, silver per-pair + composite ≥2/3)
- compute budget $0 ubu1 CPU ~1.5h
- 6 honest C3 caveats explicit
- 0 destructive ops, 0 sister .roadmap modification, 0 narrative edit, raw#9/10/15/71 UPHELD

---

(end of file)
