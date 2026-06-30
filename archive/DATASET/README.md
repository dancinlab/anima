# DATASET — 의식·Φ 검증용 외부 데이터 보관소

> S1–S40 의식 가설 검증 캠페인(2026-05-29)의 실측 데이터 single home.
> 각 클러스터별 하위 폴더에 공개 데이터셋(EEG·fMRI·TMS-EEG 등)을 보관한다.

## 폴더 구조

| 폴더 | 클러스터 | 담당 에이전트 | 주요 데이터 |
|---|---|---|---|
| `eeg_consciousness_level/` | 의식수준 (약물·마취·임종) | E1 | psychedelic/anesthesia/dying-brain EEG (LZ복잡도) |
| `eeg_clinical_doc/` | 임상 DoC·발달 | E2 | 식물인간/locked-in/영아 EEG (PCI) |
| `nonhuman/` | 비인간 substrate | E3 | 문어/식물/organoid 신경기록 |
| `meditation_decoding/` | 명상·신경디코딩 | E4 | 명상 EEG · fMRI brain-decoding |
| `tms_tes/` | TMS-EEG · TES 자극 | T1 | PCI용 TMS-evoked EEG · tDCS/tACS |

## 보관 규약

1. 각 폴더에 `manifest.json` — 데이터셋별 `{name, source_url, accession, sha256, size, format, license, downloaded_at}`.
2. 원본 raw 데이터(대용량 EDF/BIDS/SET)는 git 추적 제외(`.gitignore`), manifest + 소형 derived 산출물만 commit.
3. 라이선스 명시 — 재배포 제한 데이터셋은 URL pointer만 보관(다운로드 금지).
4. 측정 산출물(LZ76·PCI Φ-proxy)은 해당 H_xxx `state/` 또는 `derived/`에 기록.
