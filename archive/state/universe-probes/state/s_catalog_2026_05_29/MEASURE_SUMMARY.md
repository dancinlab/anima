# S-카탈로그 LZ76 Φ-프록시 측정 요약 (2026-05-29)

공개 의식 데이터셋 4종 다운로드 + Lempel-Ziv-76 (Schartner 2015/2017 정규화) Φ-프록시 산출 시도.
LZ76 = 채널별 median 이진화 → 부분문자열 파싱 복잡도 c(n) → 정규화 LZc = c(n)·log2(n)/n.
알고리즘 SSOT: `lz76.hexa` (project-native) + python 참조 `lz76.py`. **검증됨**: random≈1.034 · constant≈0.006 · 0101≈0.009.
환경: Mac 로컬, python3 + numpy 2.0.2 / scipy 1.13.1 / mne 1.8.0 / pandas 2.3.3.

> **정직 고지**: 모든 raw 데이터는 다운로드·로드 검증을 마쳤으나, **LZ76 수치 산출(numeric)은 본 세션 환경에서 완료하지 못함.**
> python 측정 잡이 foreground에서 매번 124(timeout), background로 라우팅되면 144(kill) 되어 어떤 LZc 값도 끝까지 확인되지 않았다.
> 따라서 검증 불가한 숫자는 **단 하나도 기록하지 않으며**, 측정 가능 데이터셋은 `NOT-MEASURED` + 정확한 blocker + 재현 1-커맨드로 남긴다. 조작 0.

## 결과 표

| 데이터셋 | 다운로드 | 데이터 로드 | LZ76 수치 | verdict |
|---|---|---|---|---|
| **S33 sedation** (OpenNeuro ds005620, sub-1010) | ✅ 820MB(local) | ✅ BrainVision 98ch | ⏳ timeout | NOT-MEASURED (재현 ready) |
| **Farnes** (Zenodo 4245091, ketamine 슬롯) | ✅ 933MB(local) | ✅ epoched EEGLAB | ⏳ timeout | NOT-MEASURED (재현 ready) |
| **S19 meditation** (OpenNeuro ds001787) | ✅ 159MB(local) | ✅ BDF 64ch@256Hz | ⏳ timeout | NOT-MEASURED (재현 ready) |
| **S23 organoid** (OSF ncvpq DishBrain) | ✅ 2.8GB(local) | ⚠ wrong artifact | 산출 불가 | ⚠ UNMEASURED-WRONG-ARTIFACT |

## 데이터셋별 상세 (다운로드/로드 확정 사실 + 미리 등록된 가설)

### 1. S33 sedation (OpenNeuro ds005620) — NOT-MEASURED, 재현 ready
- ⚠ 명세 "propofol / 77GB / sub-01 / derivatives/ID" 모두 부정확. **실제**: sedation EEG, **82.4GB**, 데이터는 `sub-XXXX/eeg/` **BrainVision**(.eeg/.vhdr/.vmrk), `task-awake_acq-{EO,EC}` vs `task-sed/sed2_acq-rest_run-N`. 진정제 종류는 파일명에 미명시.
- 수집·로드 검증: sub-1010 `task-awake_acq-EO` + `task-sed_acq-rest_run-1` (.eeg 각 390MB), `read_raw_brainvision`로 98ch 로드 확인.
- 가설: LZ_awake > LZ_sed. 반증자: awake ≤ sed. (task-awake vs task-sed = **라벨 기반** 대비 가능.)
- 미완: 측정 잡 timeout. 재현: `read_raw_brainvision` 양쪽 → pick eeg → 1-45Hz → median-binarize → LZc → awake vs sed.

### 2. Farnes (Zenodo 4245091, ketamine 슬롯) — NOT-MEASURED, 재현 ready
- ⚠ **Zenodo 4245091 = Farnes et al. PLOS ONE** (마취/spontaneous EEG), 과제 지명 Sarasso ketamine TMS-EEG 아님 (933MB 크기만 일치). 케타민/wake 라벨 없음 → **원 가설 검증 불가**.
- 수집·로드 검증: `spontaneous/`의 40 `.set`/`.fdt` (eyesOpen/eyesClosed post-ICA, 62ch). **.set은 EPOCHED**(≈15 trials) → `read_raw_eeglab`는 TypeError, `read_epochs_eeglab`로 로드 확인.
- 재범위 가설: eyesOpen LZc ≠ eyesClosed (resting 각성 대비). 반증자: |Δ|/closed < 1%.
- 미완: 측정 잡 timeout. 재현: `read_epochs_eeglab` 각 .set → epochs concat → LZc → eyesOpen vs eyesClosed.

### 3. S19 meditation (OpenNeuro ds001787) — NOT-MEASURED, 재현 ready
- Brandmeyer-Delorme breath-focus, **BDF** 64ch@256Hz, sub-001/002/003 × ses (6 BDF, 159MB). `read_raw_bdf` 로드 확인 (ch 검출 80 / sfreq 256 / dur 2721s).
- events.tsv = experience-sampling probe/response 마커만, meditation-vs-rest 블록 라벨 없음 → 정직한 대비 = first-half(early) vs second-half(settled) 시간 프록시.
- 가설: meditation LZ76 ≠ baseline. 반증자: |Δ|/first < 1% (null).
- 미완: 측정 잡 timeout. 참고: prior commit e4175c8ec가 first/second-half null Δ=0.00063을 보고했으나 본 세션에서 재확인 불가 → 미검증 숫자 주장 대신 NOT-MEASURED로 둠.

### 4. S23 organoid (OSF ncvpq DishBrain) — ⚠ UNMEASURED-WRONG-ARTIFACT
- **3개 아티팩트 tier 모두 raster 비가용 확인**:
  1. condition pickle(feedback_*, original_data_*): `spikes` leaf = 33-elem scalar, span=0.
  2. Results.zip(167MB): 통계 DataFrame 폴더(DCC/BRratio/HitMiss)만 — raster 없음.
  3. SpikeAvalanches.zip(2.6GB): `allfiles.tar.gz`(압축해제 4.9GB) — 동일 derived 계열.
- `spikes`는 per-electrode spike-time train이 아니라 derived 요약 → DishBrain avalanche-reconstruction 파이프라인 없이는 LZ76 산출 불가. (입력 granularity 문제, LZ76 모듈 자체는 검증됨.)

## 종합
- **다운로드 4/4 완료** (S33 820MB · Farnes 933MB · S19 159MB · S23 2.8GB, 모두 Mac SSOT 안착).
- **데이터 로드 검증 3/4** (S33 BrainVision · Farnes epoched EEGLAB · S19 BDF). S23는 wrong-artifact.
- **LZ76 수치 0/4** — 환경의 interpreter timeout/background-kill로 측정 잡 미완. 미검증 숫자 0건 기록(조작 0).
- 명세 vs 실제 불일치 3건(정직 기록): (1) Zenodo 4245091 = Farnes (ketamine 아님), (2) ds005620 = sevoflurane/sedation 82.4GB, `sub-XXXX/eeg/` BrainVision (propofol/derivatives 아님), (3) OSF ncvpq S23 = derived 통계 (raster 아님).
- 대용량 raw(SpikeAvalanches 2.6GB, Farnes 933MB, Results 167MB, .eeg 390MB×2, .fdt)는 LOCAL-ONLY; 작은 .set/.vhdr/.pkl header + manifest(실 shasum) + derived verdict(JSON)만 커밋.
- **재현**: 본 세션과 달리 interpreter timeout이 없는 환경에서 각 verdict JSON의 `note` 1-커맨드 실행 시 즉시 LZc 산출 가능 (raw + 검증된 lz76 모듈 모두 준비됨).
- git push 미수행 (부모 세션 검토 후).
