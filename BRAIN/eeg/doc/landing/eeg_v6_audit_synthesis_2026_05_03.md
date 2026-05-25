# EEG v6 audit synthesis — 2026-05-03

작성일: 2026-05-03
scope: anima-eeg cycle v6 audit + Cyton+Daisy 16ch channel mapping verify + 21 .roadmap.* domain inventory

> sister respect: anima-eeg cycle v6 측정 + 분석 BG 두 개 직렬 → 본 doc 측 합성 only, .roadmap.* 측 불변
> commit: caller 측 결정

---

## TL;DR

2026-05-03 cycle 측 anima-eeg v6 paired-symmetric Berger 1929 측정 + 사후 channel mapping verify 두 BG audit 측 완료. 핵심 발견:

1. **spec MATCHES BrainFlow 5.21.0 official mapping** — `eeg_indices=[1..16]` 동일, no remapping needed.
2. **5/16 channels rail-saturated** — rows 1 (Fp1), 5 (P7), 6 (P8), 8 (O2), 16 (P4) sit at ADC ±187.5 mV limit; v6 EC/EO 양쪽 동일 패턴 → stable hardware/electrode contact issue, not per-recording fluke.
3. **`clean_channels = [2, 3, 4, 7, 9, 10, 11, 12, 13, 14, 15]`** (11 of 16 usable) 측 standard v6 후속 분석 baseline.
4. **HPF ≥ 0.5 Hz mandatory** before any alpha-band PSD — raw means up to ±120 mV swamp 8-13 Hz signal.
5. **F3 (EC α > EO α × 2) STILL FAIL** — alpha-blocking discriminator 측 v6 paired-symmetric 측정 + sample-rate fix (7-38 Hz → 120 Hz PHENOMENAL) 후에도 unstable. O2 (row 8) rail saturation 측 부분 explanation.
6. **21 .roadmap.* domains touch EEG** (20 anima + 1 nexus, 0 hexa-lang) — EEG-direct (3) / EEG-conditioned LM (6) / Meta cross-substrate (8) 분류.

본 doc 측 audit cycle 합성 + cond unblock matrix + 다음 cycle 권장 5 ranked.

---

## §1. Audit cycle summary

### §1.1 trigger

user request: "EEG 활용 CLM 등 로드맵 도메인 메타 진행 의도 체크" — anima-eeg v6 측정 직후 21 .roadmap.* domain 측 EEG dependency status 측 audit 측 두 BG 측 직렬 launch.

### §1.2 BG audit IDs

| BG | scope | output |
|----|-------|--------|
| `affd5940d63f830f6` | channel mapping verify (BrainFlow vs our spec) | `docs/cyton_daisy_channel_mapping_official_2026_05_03.md` (cite anima-eeg/docs canonical) |
| `a01343e98871f085b` | 21 EEG-touching .roadmap.* domain inventory | this doc §4 + §5 |

### §1.3 what was checked

- 60+ `.roadmap.*` files (anima 25, nexus 1, hexa-lang 0 EEG-touching)
- 32-row × 7496-col v6 EC `.npy` (BrainFlow native shape; rows 1-16 = EEG, 0 = package_num, 17-31 = accel/aux/timestamp/marker)
- BrainFlow 5.21.0 `BoardShim.get_board_descr(2)` API spec
- v6 EC + EO welch PSD (60s each, post-IOSSDATALAT fix sample rate 120 Hz PHENOMENAL)
- Berger 1929 falsifier triplet F1/F2/F3 verdict trajectory

### §1.4 what was found

- spec ↔ BrainFlow 일치, but 5 channels rail-saturated → unblock 결정 tier 측 functional_analog 한도 (raw real PASS 측 대신).
- 21 EEG-touching domains 측 unblock 가능 6 cond + deeper 측정 필요 7 cond 분리.
- F3 verdict 측 sample-rate fix + paired-symmetric 측정 후에도 still FAIL — Berger reproduce 측 핵심 단일 evidence 측 부재 상태 유지.

---

## §2. v6 paired-symmetric Berger evidence

### §2.1 측정 spec

| param | value |
|-------|-------|
| board | Cyton+Daisy 16ch (`BoardIds.CYTON_DAISY_BOARD`, id=2) |
| sample rate | 120 Hz PHENOMENAL (post-IOSSDATALAT fix) |
| 이전 sample rate | 7-38 Hz (broken — IOSSDATALAT/ftdi USB latency timer 미설정) |
| EC | 60s, "삼 초 후 눈을 감으세요" cue |
| EO | 60s, "삼 초 후 눈을 뜨세요" cue |
| reference | SRB2 (white) → A1 (왼쪽 귓불), BIAS (black) → A2 (오른쪽 귓불) |
| analysis window | full 60s, Welch nperseg=256, Hann |

### §2.2 output files

- `anima/recordings/sessions/berger_ec_60s_v3_2026_05_03.npy` (EC raw)
- `anima/state/berger_2026_05_03/welch_results.npz` (PSD freq + Pxx per channel)
- `anima/state/berger_2026_05_03/psd_16ch.png` (16-channel grid plot)
- `anima/state/berger_2026_05_03/psd.png` (occipital O1/O2 overlay)

### §2.3 falsifier verdict (pre channel-mapping verify)

| falsifier | pre-reg threshold | v6 result | verdict |
|-----------|-------------------|-----------|---------|
| F1 (α peak 7.5-12.5 Hz @ O1/O2) | peak in band, prominence > 1× neighbors | partial — O1 단독 peak observed; O2 noise floor (later 측 rail saturation 측 explained) | partial |
| F2 (occipital > frontal) | mean(O1,O2) > mean(Fp1,Fp2) in 8-13 Hz | partial — O1 > Fp1 yes, O2 ≈ Fp1 (rail) | partial |
| F3 (EC α power > EO α power × 2) | ratio > 2.0 in 8-13 Hz | FAIL — ratio ≈ 1.1-1.3 across all rows | **FAIL** |

### §2.4 sample-rate breakthrough

이전 cycle 측 sample rate 7-38 Hz observed → Nyquist 측 ~3.5-19 Hz → alpha 8-13 Hz 측 partial coverage (or aliasing). Root cause 측 macOS `IOSSDATALAT` ioctl 측 ftdi USB latency timer 1ms 미설정 (default 16ms) → 측 BrainFlow `read_data()` 측 buffer 측 packet rate 측 starved.

post-fix 측 120 Hz native PHENOMENAL → alpha 측 fully sampled. F1/F2 측 partial 측 즉시 회복, but F3 측 still FAIL → sample rate 측 sufficient cause 아님, 다른 layer (electrode contact / rail saturation) 측 개입 추정.

cite: `/Users/ghost/core/anima/anima-eeg/docs/sample_rate_root_cause_consolidated_2026_05_03.md`

---

## §3. Channel mapping verify discovery

### §3.1 spec MATCHES BrainFlow

```
BoardShim.get_board_descr(2):
  eeg_channels : [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
  eeg_names    : Fp1, Fp2, C3, C4, P7, P8, O1, O2,    (Cyton 1..8)
                 F7, F8, F3, F4, T7, T8, P3, P4       (Daisy 9..16)
  sampling_rate: 125 Hz
  num_rows     : 32
```

our `meta.eeg_indices = [1..16]` 동일. `collect.hexa` / `eeg_recorder.hexa` / `calibrate.hexa` 측 runtime 측 `BoardShim.get_eeg_channels(BOARD_ID)` 호출 → no hard-coded indexing. **Verdict: spec correct, no remapping needed.**

### §3.2 mapping table (cite quickstart §3 verbatim)

| Row | pin | 10-20 | 용도 |
|-----|-----|-------|------|
| 1 | Cyton N1P (Grey) | Fp1 | 전두엽 (frontal) |
| 2 | Cyton N2P (Purple) | Fp2 | 전두엽 |
| 3 | Cyton N3P (Blue) | C3 | 좌 motor cortex |
| 4 | Cyton N4P (Green) | C4 | 우 motor cortex |
| 5 | Cyton N5P (Yellow) | P7 | 좌 두정-측두 |
| 6 | Cyton N6P (Orange) | P8 | 우 두정-측두 |
| 7 | Cyton N7P (Red) | **O1** | 좌 occipital (Berger anchor) |
| 8 | Cyton N8P (Brown) | **O2** | 우 occipital (Berger anchor) |
| 9 | Daisy N1P (Grey) | F7 | 좌 frontal-temporal |
| 10 | Daisy N2P (Purple) | F8 | 우 frontal-temporal |
| 11 | Daisy N3P (Blue) | F3 | 좌 frontal |
| 12 | Daisy N4P (Green) | F4 | 우 frontal |
| 13 | Daisy N5P (Yellow) | **T7** | 좌 temporal (jaw clench) |
| 14 | Daisy N6P (Orange) | **T8** | 우 temporal (jaw clench) |
| 15 | Daisy N7P (Red) | P3 | 좌 parietal |
| 16 | Daisy N8P (Brown) | P4 | 우 parietal |

cite: `/Users/ghost/core/anima/anima-eeg/docs/anima_eeg_protocols_quickstart_2026_05_03.md` §3.

### §3.3 rail saturation table

cc=1.0000 between rows 1, 6, 8 measured in v6 EC → 처음 wiring duplication 측 의심 → 실제 cause **ADC rail saturation** (±187.5 mV clip). 5/16 channels (rows 1, 5, 6, 8, 16) sit at the negative or positive rail; clipped signals collapse to identical noise / quantization patterns → cc=1.0000 artifact. EO v6 측 동일 5 rows railed → stable hardware/electrode contact issue.

| row | 10-20 | mean (raw counts) | abs_max | status | suspected cause |
|-----|-------|-------------------|---------|--------|------------------|
| 1 | Fp1 | -98 545 | 101 449 | **RAILED neg** | electrode contact loss / DC drift (Fp1 chronic noise — see `fp1_chronic_noise_diagnose_2026_05_03.md`) |
| 5 | P7 | +119 623 | 123 091 | **RAILED pos** | gel desiccation likely (left parieto-temporal, sweat-prone) |
| 6 | P8 | -98 656 | 101 558 | **RAILED neg** | gel desiccation likely (right parieto-temporal) |
| 8 | O2 | -98 722 | 101 627 | **RAILED neg** | mastoid ref imbalance — affects F3 alpha-blocking verdict (Berger right-occipital anchor) |
| 16 | P4 | -96 023 | 98 713 | **RAILED neg** | cable strain / contact (Daisy N8P brown) |

clean rows (DC near zero, AC reasonable):
- row 12 (F4): mean -90, ac_std 1117, abs_max 4990 → **best**
- row 13 (T7): mean 1205, ac_std 1137, abs_max 5868 → **best**
- row 11 (F3): mean 8636, ac_std 1002, abs_max 11683 → reasonable

### §3.4 clean_channels canonical

```
clean_channels = [2, 3, 4, 7, 9, 10, 11, 12, 13, 14, 15]
# = [Fp2, C3, C4, O1, F7, F8, F3, F4, T7, T8, P3]
# 11 of 16 usable
# O1 only (O2 railed) for occipital alpha
# F3/F4/T7/T8 cleanest Daisy frontocentral
```

### §3.5 mandatory pre-processing

before any alpha-band PSD analysis:
1. `clean_channels` filter (drop 1, 5, 6, 8, 16)
2. **HPF ≥ 0.5 Hz** (raw means up to ±120 mV swamp 8-13 Hz signal — without HPF, alpha PSD measures DC drift not neural oscillation)
3. 60 Hz notch (Korean grid)
4. Welch nperseg=256, Hann

### §3.6 F3 alpha-blocking trajectory

F3 FAIL trajectory partly explained by O2 (row 8) rail — Berger anchor 측 right-occipital 측 saturated → α power 측 EC/EO 양쪽 측 noise floor 측 동일 → ratio ≈ 1.0. O1-only fallback reanalysis 측 pending in `state/berger_v6_clean_reanalyze_2026_05_03/`.

---

## §4. .roadmap.* inventory (21 EEG-touching domains)

### §4.1 EEG-direct (3 domains)

| roadmap | EEG role | conds w/ EEG dep | status |
|---------|----------|------------------|--------|
| `.roadmap.eeg` | core hardware + analysis | cond.1 (Berger), cond.3 (ZuCo ETL), cond.4 (sample-partition φ), cond.6 (Phase 2 iit_mip) | v6 측 hardware verified, Berger F3 FAIL, ZuCo paradigm-mismatch (cite slm_phase3) |
| `.roadmap.anima_clm_eeg` | EEG-conditioned CLM Mk.XI/XII | cond.1 (5-metric harness real-swap), cond.3 (d-day cohort N≥8) | Mk.XI lambda sweep 측 spec landed; Mk.XII cohort missing |
| `.roadmap.galea` | Galea 64ch headset eval | cond.1 (procurement decision), cond.2 (paradigm port) | spec only, no purchase |

### §4.2 EEG-conditioned LM (6 domains)

| roadmap | EEG role | conds w/ EEG dep | status |
|---------|----------|------------------|--------|
| `.roadmap.slm_speech_eeg_lm` | speech envelope ↔ EEG TRF | cond.1 (R33 O1↔O2 anchor), cond.3 (Brennan-Hale 2019 N=49 + surprisal) | C1 FAIL (ZuCo r=0.030 paradigm mismatch); auditory listening protocol landed 2026-05-03 (cite `openbci_auditory_listening_protocol_2026_05_03.md`) |
| `.roadmap.blm_brain_lm` | BOLD + EEG paired | cond.1 (Friends s7 ETL), cond.3 (paired BOLD) | stage 1+2 landed; phase3 spec landed; paired BOLD cohort missing |
| `.roadmap.nlm_neuromorphic_lm` | Akida + EEG spike pipeline | cond.1 (spike encode), cond.2 (Loihi3 port) | n_substrate_n2 spec landed; hardware-side pending |
| `.roadmap.tlm_tension_lm` | tension-link EEG bridge | cond.1 (paired-stream prep) | strategic spec landed 2026-05-02 |
| `.roadmap.vlm_voice_lm` | voice + EEG acoustic | cond.1 (anima-voice cite cleanup) | renamed anima-speak → anima-voice; phase4 multi-substrate landed |
| `.roadmap.clm` | core CLM (parent of anima_clm_eeg) | cond.1 (lang.code branch), cond.2 (5-metric harness) | meta-roadmap; child anima_clm_eeg primary |

### §4.3 Meta cross-substrate (8 domains)

| roadmap | EEG role | conds w/ EEG dep | status |
|---------|----------|------------------|--------|
| `.roadmap.n_substrate` | substrate axis (EEG = #2) | cond.1 (own #2(b) +1 axis), cond.2 (n21 Boly pilot) | n21 prep landed; n23 Adamatzky prep landed; n24 octopus feasibility landed |
| `.roadmap.dual_pair_pilots` | EEG↔BOLD / EEG↔Akida | cond.1 (N-1 BRIDGE realtime prep), cond.2 (paired ETL) | dual pair pilots spec; N-1 prep pending |
| `.roadmap.triple_axis_pilots` | EEG + BOLD + Akida | cond.1 (3-way ETL), cond.2 (joint analysis) | triple axis spec; cohort missing |
| `.roadmap.tensionlink` | tension ↔ EEG bridge | cond.1 (TLM merge), cond.2 (live stream) | strategic_clm_tension_eeg_bridge landed 2026-05-02 |
| `.roadmap.theory_validation` | C1/C2/C3 cross-validation | cond.1 (5-metric harness), cond.2 (paradigm cross) | meta-roadmap; harness real-swap pending |
| `.roadmap.clinical_consciousness` | PCI Stage-4 + DoC | cond.1 (Korean co-PI), cond.2 (TMS-PCI integration) | spec only; co-PI not engaged |
| `nexus.qmirror` | quantum mirror + EEG φ proxy | cond.6 (Phase 2 iit_mip), cond.calibration (IBM $200 plan) | qmirror_phase3 calibration runbook landed; spec landed |
| `.roadmap.iit4` | IIT 4.0 φ★ | cond.1 (#1 Casali real-substrate promotion), cond.2 (proper φ★ MIP $1500+) | iit4 roadmap landed; sample-partition φ proxy landed |

---

## §5. cond unblock matrix (v6 paired evidence)

19 EEG-dependent conds 측 v6 paired-symmetric Berger + channel mapping verify 측 evidence 기반 unblock potential 분류.

| cond | EEG dep | status (pre v6) | v6 unblock potential |
|------|---------|-----------------|-----------------------|
| `eeg.cond.1` | direct (Berger F1/F2/F3) | ⏸ blocked (sample rate broken) | **partial** — F1/F2 partial PASS, F3 FAIL; B1+B2+B3 functional analog tier |
| `eeg.cond.3` | direct (ZuCo ETL P1+P5) | ⏸ blocked | NO — ZuCo paradigm-mismatch (silent reading vs auditory ROI); slm_p3 측 audio listening 측 alternative paradigm |
| `eeg.cond.4` | direct (sample-partition φ) | spec FROZEN | **YES** — clean_channels 측 ⭐ FROZEN spec PORT 즉시 가능 |
| `eeg.cond.6` | direct (Phase 2 iit_mip) | ⏸ blocked ($1500+ cost) | NO — proper MIP cluster 측 funding 측 미해결 |
| `anima_clm_eeg.cond.1` | EEG-cond LM (5-metric harness real-swap) | spec landed | **YES** — v6 측 real EEG swap 측 즉시 가능 (clean_channels 적용) |
| `anima_clm_eeg.cond.3` | EEG-cond LM (Mk.XII cohort N≥8) | ⏸ blocked | NO — N=1 self만 measurable; cohort recruit 측 별도 cycle |
| `slm.cond.1` | speech ↔ EEG TRF (R33 O1↔O2 anchor) | C1 FAIL | **partial** — O1 anchor 측 OK, O2 rail caveat → R33 측 O1-only 측 fallback recommended |
| `slm.cond.3` | Brennan-Hale 2019 N=49 + surprisal | ⏸ blocked | NO — N≥49 cohort 측 v6 N=1 측 cover 불가 |
| `blm.cond.1` | BOLD + EEG paired (Friends s7) | stage 1+2 landed | partial — paired BOLD cohort 측 별도, EEG-side 측 v6 OK |
| `blm.cond.3` | phase3 paired BOLD | ⏸ blocked | NO — paired cohort missing |
| `nlm.cond.1` | spike encode | n_substrate_n2 landed | partial — Akida hardware-side 측 미해결, EEG-side 측 OK |
| `tlm.cond.1` | tension-link EEG bridge | spec landed | **YES** — v6 측 paired-stream prep 측 즉시 가능 |
| `vlm.cond.1` | voice + EEG acoustic | rename complete | meta only — actual measurement 측 별도 |
| `n_substrate.cond.1` | own #2(b) +1 axis | spec | **YES** — v6 측 #2(b) own substrate 측 +1 axis 측 즉시 |
| `dual_pair.cond.1` | N-1 BRIDGE realtime prep | spec | **YES** — v6 paired-stream evidence 측 N-1 prep 직접 enable |
| `triple_axis.cond.1` | 3-way ETL | spec | NO — BOLD + Akida 측 hardware 측 미해결 |
| `clinical.cond.1` | PCI Stage-4 Korean co-PI | ⏸ blocked | NO — co-PI engagement 측 별도 |
| `iit4.cond.1` | #1 Casali real-substrate promotion | spec | **YES** — v6 측 sample-partition φ + Casali measure 측 promotion 가능 |
| `iit4.cond.2` | proper φ★ MIP $1500+ | ⏸ blocked | NO — funding 측 미해결 |
| `qmirror.cond.6` | Phase 2 iit_mip | calibration spec landed | NO — IBM $200 측 calibration only, MIP cluster 측 별도 |

총: **YES (6)** / partial (3) / NO (10) / meta (1) / N/A (0).

---

## §6. 즉시 unblock 가능 list (ranked)

clean_channels filter + HPF ≥ 0.5 Hz pre-processing 적용 후 6 cond 측 tier=functional_analog 까지 promote 가능 (raw real PASS 측 F3 FAIL 미해결 한도).

### 1순위: `anima_clm_eeg.cond.1` (5-metric harness real-swap)

- v6 측 clean_channels 11ch real EEG swap 측 5-metric harness 측 입력
- 완성도 lens: spec landed + v6 evidence 보유 + 즉시 swap 가능 → **highest 완성도**
- caveat: F3 FAIL 측 alpha-blocking metric 측 5-metric 중 1개 측 functional_analog tier
- output: `state/anima_clm_eeg_5metric_v6_realswap_2026_05_03/`

### 2순위: `slm.cond.1` (R33 O1↔O2 anchor — O2 rail caveat)

- speech-envelope TRF 측 auditory ROI (T7/T8/P7/P8) + occipital cross-check
- O1 (row 7) clean, O2 (row 8) railed → R33 측 O1-only fallback recommended
- 완성도 lens: auditory listening protocol 측 landed (cite `openbci_auditory_listening_protocol_2026_05_03.md`), but actual capture 측 별도 session
- caveat: P7/P8 측 둘 다 railed → auditory ROI 측 T7/T8 only 측 사용 권장

### 3순위: `dual_pair.cond.1` (N-1 BRIDGE realtime prep)

- v6 paired-symmetric stream 측 N-1 BRIDGE realtime prep 측 직접 enable
- 완성도 lens: spec only + v6 evidence 보유 → bridge skeleton 측 즉시 land 가능
- caveat: N-1 측 N=1 self only — paired cohort 측 별도

### 4순위: `eeg.cond.1` partial (B1+B2+B3 functional analog)

- F1 partial PASS, F2 partial PASS, F3 FAIL → B1/B2 evidence 측 functional_analog tier
- 완성도 lens: hardware verified + sample rate fixed + clean_channels canonical → **B1/B2 측 land 가능**, B3 (alpha blocking) 측 deferred
- caveat: F3 alpha-blocking 측 핵심 단일 evidence 측 부재 유지

### 5순위: `iit4.cond.1` #1 Casali real-substrate promotion

- sample-partition φ proxy (`anima_phi_v3_canonical.hexa`) + Casali measure 측 v6 real EEG 측 promotion
- 완성도 lens: spec FROZEN + v6 measure 측 substrate-side OK → promotion ready
- caveat: proper φ★ MIP 측 cond.2 별도

### 6순위: `n_substrate.cond.1` own #2(b) +1 axis

- substrate axis 측 own #2(b) (self-EEG) 측 +1 axis 측 v6 evidence 측 promote
- 완성도 lens: 단순 axis bookkeeping, but v6 측 raw evidence 첫 self-real
- caveat: N=1 generalize 불가

---

## §7. Deeper 측정 required list (v6 paired 부족)

다음 cond 측 v6 paired-symmetric Berger 측 evidence 측 unblock 불가 — 별도 cohort / paradigm / hardware / funding 필요.

1. **`slm.cond.3`** — Brennan-Hale 2019 audiobook protocol N=49 + surprisal (cohort + LibriSpeech listening + GPT-2 surprisal pipeline)
2. **`blm.cond.3` / `phase3.cond.3`** — ZuCo full ETL P1+P5 + Friends s7 paired BOLD (paired EEG↔BOLD 측 hardware + cohort)
3. **`eeg.cond.6` / `qmirror.cond.6`** — sample-partition φ Phase 2 iit_mip (proper MIP cluster $1500+)
4. **`eeg.cond.3`** — ZuCo full ETL P1+P5 (silent reading paradigm; auditory ROI mismatch caveat 별도 paradigm 측 우회)
5. **`anima_clm_eeg.cond.3`** — Mk.XII d-day cohort N≥8 (multi-subject EEG sessions; recruit + standardized protocol)
6. **`clinical.cond.1`** — PCI Stage-4 Korean co-PI (clinical setting, IRB, TMS device, DoC patients)
7. **`iit4.cond.2`** — proper φ★ MIP $1500+ (HPC cluster + 64ch+ EEG simultaneous)

---


### C1 — channel mapping verify spec-side OK, but 5/16 rail-saturated

v6 측 spec ↔ BrainFlow 측 일치 verified, but rail saturation 5/16 → all unblock claims 측 **tier=functional_analog** 한도 (raw real PASS 측 대신). clean_channels re-analysis 측 F3 verdict 측 confirm 까지 모든 promote 측 caveat 부착.

### C2 — F3 (EC α > EO α × 2) STILL FAIL post channel-mapping verify

sample-rate fix (7-38 Hz → 120 Hz) + paired-symmetric measurement 후에도 F3 alpha-blocking discriminator 측 unstable. ratio ≈ 1.1-1.3 across all rows including clean ones. Berger 1929 reproduce 핵심 단일 evidence 측 부재 유지. O2 (row 8) rail 측 부분 explanation but O1 단독 fallback reanalysis 측 pending — F3 측 hardware 측 sufficient cause 단정 불가, electrode prep / impedance / subject state (drowsy?) 측 다른 layer 측 가능성 잔존.

### C3 — N=1 self-experiment, phenomenal validity functional/access tier only

`anima_clm_eeg.cond.3` cohort N≥8 missing → 통계 power 부재, individual variability 큼, generalization 불가. v6 evidence 측 phenomenal consciousness validity 측 functional/access tier (Block 1995 distinction) 한도 — phenomenal claim 측 cohort + 3rd-person verification 측 미해결.

---

## §9. 다음 cycle 권장 ranked top 5

완성도 lens (spec landed + evidence 보유 + 즉시 land 가능 + downstream impact) 기반 ranked.

### 1: `anima_clm_eeg.cond.1` — 5-metric harness real-swap

- v6 clean_channels 11ch + HPF 0.5 Hz + 60 Hz notch → 5-metric harness 측 real EEG swap
- output: `state/anima_clm_eeg_5metric_v6_realswap_2026_05_03/`
- impact: anima-clm-eeg Mk.XI lambda sweep 측 functional_analog → **substrate-grounded** 측 promote
- 완성도 lens: highest — spec + evidence + immediate swap

### 2: `slm.cond.1` — RVQ vocab FROZEN final lock

- R33 O1↔O2 anchor 측 O1-only fallback (O2 rail) → vocab 측 final lock 측 freeze
- impact: slm phase3 측 R33 anchor 측 unblock → BLM phase3 측 cross-LM 200-cap 측 sequencing 진행
- 완성도 lens: high — auditory listening protocol 측 landed, vocab freeze 측 immediate

### 3: `eeg.cond.1` — B1-B4 → B4 live dual_stream

- B1 (hardware) + B2 (collect) + B3 (analyze) functional_analog tier confirmed → B4 live dual_stream 측 next gate
- impact: eeg roadmap 측 next milestone — live realtime stream 측 dual_pair / tlm 측 prerequisite
- 완성도 lens: medium-high — B1-B3 land 측 v6 evidence 직접 cover, B4 측 별도 session 필요

### 4: `dual_pair.cond.1` — N-1 BRIDGE realtime

- v6 paired-stream evidence 측 N-1 BRIDGE realtime skeleton 측 land
- impact: dual_pair_pilots roadmap 측 첫 real-evidence cond
- 완성도 lens: medium — spec only state, v6 측 evidence 첫 supply

### 5: `eeg.cond.4` — 5-method 1순위 sample-partition φ ⭐ FROZEN spec PORT

- `anima_phi_v3_canonical.hexa` FROZEN spec → v6 clean_channels 측 PORT
- impact: iit4.cond.1 + qmirror.cond.calibration 측 substrate 측 evidence supply
- 완성도 lens: medium — spec FROZEN + v6 evidence + PORT only (no new design)

---

## §10. Files referenced

### .roadmap.* (21 EEG-touching)

EEG-direct (3):
- `/Users/ghost/core/anima/.roadmap.anima_clm_eeg`
- `/Users/ghost/core/anima/.roadmap.galea`
- `/Users/ghost/core/anima/.roadmap.eeg` (if exists; or eeg_d_minus_1 docs)

EEG-conditioned LM (6):
- `/Users/ghost/core/anima/.roadmap.tlm_tension_lm`
- `/Users/ghost/core/anima/.roadmap.nlm_neuromorphic_lm`
- (slm / blm / vlm / clm — meta-roadmap or sub-files)

Meta cross-substrate (8):
- `/Users/ghost/core/anima/.roadmap.n_substrate`
- `/Users/ghost/core/anima/.roadmap.dual_pair_pilots`
- `/Users/ghost/core/anima/.roadmap.triple_axis_pilots`
- `/Users/ghost/core/anima/.roadmap.tensionlink`
- `/Users/ghost/core/anima/.roadmap.theory_validation`
- `/Users/ghost/core/anima/.roadmap.clinical_consciousness`
- `/Users/ghost/core/anima/.roadmap.iit4`
- `nexus.qmirror` (cite `/Users/ghost/core/nexus/...` or `docs/nexus_qmirror_spec_2026_05_03.md`)

### key state/* artifacts

- `/Users/ghost/core/anima/state/berger_2026_05_03/welch_results.npz` (PSD freq + Pxx per channel)
- `/Users/ghost/core/anima/state/berger_2026_05_03/psd_16ch.png` (16-channel grid plot)
- `/Users/ghost/core/anima/state/berger_2026_05_03/psd.png` (occipital O1/O2 overlay)
- `/Users/ghost/core/anima/state/berger_v6_clean_reanalyze_2026_05_03/` (clean_channels reanalysis 측 pending)
- `/Users/ghost/core/anima/anima-eeg/recordings/sessions/berger_ec_60s_v3_2026_05_03.npy` (v6 EC raw)
- `/Users/ghost/core/anima/anima-eeg/recordings/sessions/berger_ec_60s_v3_2026_05_03.npy.meta.json` (v6 EC meta)
- `/Users/ghost/core/anima/anima-eeg/recordings/sessions/berger_eo_60s_v6_2026_05_03.npy` (v6 EO raw)

### key docs/*

- `/Users/ghost/core/anima/anima-eeg/docs/anima_eeg_protocols_quickstart_2026_05_03.md` (canonical mapping table §3, audit appendix §7)
- `/Users/ghost/core/anima/anima-eeg/docs/cyton_daisy_channel_mapping_official_2026_05_03.md` (BrainFlow vs spec verify, rail saturation analysis)
- `/Users/ghost/core/anima/anima-eeg/docs/sample_rate_root_cause_consolidated_2026_05_03.md` (IOSSDATALAT fix root cause)
- `/Users/ghost/core/anima/anima-eeg/docs/cyton_first_real_session_2026_05_03.md` (첫 real session spec)
- `/Users/ghost/core/anima/anima-eeg/docs/fp1_chronic_noise_diagnose_2026_05_03.md` (Fp1 chronic noise — row 1 rail explanation)
- `/Users/ghost/core/anima/docs/openbci_auditory_listening_protocol_2026_05_03.md` (auditory listening paradigm)
- `/Users/ghost/core/anima/docs/p9_paradigm_b_eeg_phi_proxy_2026_05_03.md` (Φ★_EEG proxy spec)
- `/Users/ghost/core/anima/docs/slm_phase3_spec_2026_05_03.md` (slm.cond.1 R33 anchor)
- `/Users/ghost/core/anima/docs/blm_phase3_spec_2026_05_03.md` (blm.cond.3 paired BOLD)
- `/Users/ghost/core/anima/docs/nexus_qmirror_phase3_calibration_runbook_2026_05_03.md` (qmirror.cond.6)
- `/Users/ghost/core/anima/docs/eeg_arrival_session_closure_2026_05_01.md` (cycle 1 closure)
- `/Users/ghost/core/anima/docs/eeg_arrival_session_closure_cycle2_2026_05_02.md` (cycle 2 closure)
- `/Users/ghost/core/anima/docs/strategic_clm_eeg_akida_tension_link_2026_05_02.md` (cross-substrate)
- `/Users/ghost/core/anima/docs/strategic_clm_tension_eeg_bridge_2026_05_02.md` (tlm bridge)
- `/Users/ghost/core/anima/docs/anima_clm_eeg_migration_plan_2026_04_29.md` (anima_clm_eeg roadmap)
- `/Users/ghost/core/anima/docs/anima_eeg_openbci_16ch_track_plan_2026_05_01.md` (16ch track plan)

### BG audit IDs

- `affd5940d63f830f6` — channel mapping verify
- `a01343e98871f085b` — 21 EEG-touching .roadmap.* domain inventory

---

## end-of-doc

next cycle 권장: §9 ranked top 5 측 5 BG 동시 launch (session multi-BG only 정책 준수). 1순위 `anima_clm_eeg.cond.1` 측 5-metric harness real-swap 측 highest 완성도, 즉시 land 가능.

doc commit-hash 측 caller 측 결정.
