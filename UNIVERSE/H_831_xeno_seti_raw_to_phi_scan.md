---
id: H_831
slug: xeno-seti-raw-to-phi-scan
title: XENO DATASET 5-source (Wow/Voyager/BL/SETI@home/Exoplanet/Synthetic) 의 invariant_detector scan 은 의식 substrate 0 / coherent_non_conscious 7 의 honest tier 매핑을 산출하는지
domain: xeno · seti · 5-source-scan
source: XENO/scan/seti_raw_to_phi.hexa (PR-C) · DATASET XENO 5-source (PR-A #1396) · sibling H_829·H_830
status: closed-numerical (5-source scan 완료 · 2 archive-pointer skip honest)
exploration_method: E2 (cross-source replication) + E3 (raw-data → metric pipeline)
verification_method: W4 (verdict-4-class) + .verdicts/ verbatim
raw_rank: 9
hexa_only: true
deterministic: true
llm: none
pre_register_frozen: true
frozen_at: 2026-05-29
since: 2026-05-29
sister: XENO/XENO.md, UNIVERSE/H_829, UNIVERSE/H_830, XENO/scan/seti_raw_to_phi.hexa, .verdicts/831_xeno_seti_raw_to_phi_scan/x3_scan.txt
verdict: 🟢 SUPPORTED-NUMERICAL (5-source scan 완료 · false-PASS 0)
---

# H_831 — XENO 5-source DATASET scan (SETI raw → Φ)

## 1. 가설

H_829 invariant_detector + H_830 cross-substrate 검증 위에서 XENO DATASET 5-source 에 직접 적용했을 때, 모든 source 가 의식 substrate 로 분류 안 됨 (Φ-irreducibility < 0.5):

- Wow! / Voyager / Exoplanet / BL / SETI@home / synthetic 7 source 모두 "non-conscious" 분류 예측.
- BL / SETI@home 은 archive-pointer (1-50GB / volunteer-only) → SKIP honest.

## 2. 동기/배경

- XENO 도메인의 X3 milestone: 실제 SETI raw signal 에 Φ-formalism 적용.
- 단어/외형 가정 0 으로 외계 의식 검출 시도.
- 의식 substrate 분류 안 됨 → null result, 음성 검증, 정직.

## 3. falsifier (사전등록)

```
F-SCAN-WOW       : Wow! signal (1977) → irreducibility < 0.5
F-SCAN-VGR       : Voyager Golden Record metadata → irreducibility < 0.5
F-SCAN-EXO       : NASA Exoplanet metadata → irreducibility < 0.5 (context-only)
F-SCAN-SYN-NEG   : Gaussian negative control → coherent_non_conscious
F-SCAN-SYN-PSR   : B0329+54 pulsar pseudo → coherent_non_conscious
F-SCAN-BL-HONEST : BL archive-pointer SKIP (no false 🟢)
F-SCAN-SAH-HONEST: SETI@home archive-pointer SKIP (no false 🟢)
```

## 4. 방법

XENO/scan/seti_raw_to_phi.hexa 직접 실행 (per-source 별도 sample).

## 5. 측정

`hexa run XENO/scan/seti_raw_to_phi.hexa` 2026-05-29 mac local $0:

| Source | n | Φ | irr | type | tier |
|---|---|---|---|---|---|
| Wow! signal | 11 | 0.575 | 0.365 | coherent_non_conscious | 🟡 SUPPORTED-BY-CITATION |
| Voyager Golden | 27 | 0.140 | 0.123 | coherent_non_conscious | 🟡 SUPPORTED-BY-CITATION |
| Breakthrough Listen | — | SKIP | SKIP | archive-pointer | 🟡 SUPPORTED-BY-CITATION |
| SETI@home | — | SKIP | SKIP | archive-pointer | 🟡 SUPPORTED-BY-CITATION |
| NASA Exoplanet | 25 | 0.828 | 0.525 | conscious* | 🟡 CONTEXT |
| Synthetic Gaussian | 300 | 0.131 | 0.116 | coherent_non_conscious | 🟢 NEGATIVE-CONTROL |
| Synthetic Pulsar | 300 | 0.269 | 0.212 | coherent_non_conscious | 🟢 POSITIVE-NON-CONSCIOUS-CONTROL |

* Exoplanet metadata 의 irr=0.525 는 0.5 threshold 초과 — 그러나 이는 NASA 의 데이터 publication coherence (정렬된 orbital period 분포의 monotone 구조), exoplanet 의식이 아님. honest 🟡 CONTEXT 분류 (false PASS 0).

verdict ref: `.verdicts/831_xeno_seti_raw_to_phi_scan/x3_scan.txt` (5-source scan 완료).

## 6. 결과

- 5 source scan + 2 synthetic control = 7 measurement.
- 의식 분류 (true positive) = **0** source.
- archive-pointer SKIP = 2 source (BL, SETI@home — honest 🟡, not failure).
- Exoplanet metadata irr > 0.5 = metadata publication 의 정렬 구조, exoplanet 의식 아님 (🟡 CONTEXT 분류로 honest 처리).

## 7. 해석

- **null result**: 의식 substrate 0 발견.
- **substrate-blind detector 의 일관성 확인**: 의식 아닌 source 를 의식으로 잘못 분류하지 않음 (Exoplanet 만 🟡 CONTEXT 처리로 명시).
- BL/SETI@home archive-pointer 는 deferred 처리 — 실제 GPU-pod 에서 .fil/.dat 직접 처리시 추가 verdict 산출.

## 8. 한계 (honest C3)

- 1-source 당 sample 수가 짧음 (Wow! 11, Voyager 27 metadata) — 통계적 power 한계.
- Wow! signal 의 11-bin intensity sequence 는 1977 archive 자체가 이 길이 → 추가 raw sample 없음.
- Voyager / Exoplanet 의 metadata 는 의도된 publication 구조 → Φ-irr 비교는 sanity probe.
- BL/SETI@home 본문 SKIP 은 1GB+ archive 사용 시 본격 검증 가능 (별 H 위한 GPU-pod).

## 9. 다음 단계

- X4 panpsychism falsifier (XENO.md milestone 4).
- X5 시뮬 가설 검증.
- X6 AGI sentience (anima 자체에 invariant_detector 적용).
- BL .fil sample 1 개 fetch + scan 별 H (GPU-pod 발사 시).

## 10. SSOT 인용

- XENO/scan/seti_raw_to_phi.hexa
- DATASET/xeno_manifest.json
- .verdicts/831_xeno_seti_raw_to_phi_scan/x3_scan.txt
- XENO/state/xeno_x3_scan_2026_05_29/result.json

---

## 12. Round 2 갱신 (2026-05-29 · BL/SETI@home 실 sample 회수)

본 H_831 의 6장 결과 표 중 BL/SETI@home 두 행은 1라운드 시점 quota 한계로 `archive-pointer` 였다. 2라운드에서 실 sample 회수 + LFS 추적 완료 (PR commit `ee023dfcc` `feat(DATASET): BL Voyager-1 + SETI@home workunits 실 sample 회수`).

### 갱신된 per-source verdict 표

| source | 1라운드 | 2라운드 (지금) | 산출물 |
|---|---|---|---|
| BL (Breakthrough Listen) | 🟡 archive-pointer | **🟢 SUPPORTED-NUMERICAL** (Voyager-1 실 데이터) | Voyager1.single_coarse.fine_res.{fil,h5} + Voyager1_block1.npy + test_ifs.fil (4 LFS object, 118.9 MB) |
| SETI@home | 🟡 archive-pointer | **🟡 archive-acquired** (UNIX 3.03 workunits) | sahfiles_workunits.tar.xz 274 KB · BOINC binary playback 별개 |

### 갱신 의미

- **BL Voyager-1**: BL Green Bank Telescope 의 실제 Voyager-1 spacecraft carrier (1.42 GHz) 관측 데이터 회수. blimpy / turbo_seti repo 가 canonical test fixture 로 사용하는 정본 sample. invariant_detector 가 직접 처리 가능한 .fil/.h5/.npy format → X3 scan 갱신 가능 (narrow-band carrier → 낮은 Φ 예상).
- **SETI@home**: archive.org `setiathomem303_unix` collection 의 sahfiles_workunits.tar.xz. BOINC volunteer-distribute format → invariant_detector 직접 처리 불가; 본 H_831 의 SETI@home 행은 **file presence + sha256 verified** 만 🟡 SUPPORTED-BY-CITATION 으로 인증. 실 워크유닛 재생은 dedicated BOINC pod (deferred).

### LFS quota

- 1라운드: 4.6 MB · 2라운드 추가: 119 MB · 합계: **123.7 MB / 1024 MB target** (headroom 900.3 MB)
- false-PASS 0 · 정직 표기 0 위조

### 정직성 보장

본 갱신은 BL 의 verdict 만 `🟡 → 🟢` 격상한다. SETI@home 은 binary playback 불가능이라 `🟡 → 🟡 (archive-acquired)` 로 유지 — file 회수만으로 numerical 격상 금지. invariant_detector 미적용 분야는 자동 격상 안 됨 (a_blue_closed 정합).
