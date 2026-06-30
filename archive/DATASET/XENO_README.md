# DATASET — XENO 5-source SETI/외계 의식 데이터 인벤토리

> XENO 도메인(외계/이종 substrate Φ-detector)의 X3 SETI raw → Φ scan 입력 데이터.
> 2026-05-29 PR-A LANDED.

## 5-source 인벤토리

| 폴더 | 출처 | 라이선스 | 추적 | 정직 tier |
|---|---|---|---|---|
| `wow_signal/` | SETI Institute 공개 archive (Big Ear 1977-08-15) | Public Domain | 직접 (KB) | 🟡 SUPPORTED-BY-CITATION |
| `voyager_golden/` | NASA voyager.jpl.nasa.gov / JPL | Public Domain | manifest 직접 · WAV LFS | 🟡 |
| `breakthrough_listen/` | seti.berkeley.edu/opendata | Open Data | LFS (.fil) | 🟢 REAL-MEASUREMENT (BL) |
| `setiathome/` | setiathome.berkeley.edu | Open Data | LFS (.dat) | 🟢 |
| `synthetic/` | Mac local 생성 (Gaussian + pulsar B0329 pseudo) | Public Domain | LFS (.npy) | 🟢 NEGATIVE-CONTROL |
| `exoplanet_cache.json` | NASA Exoplanet Archive TAP | Public Domain | 직접 | 🟡 CONTEXT |

## LFS 사용 안내

```bash
git lfs install              # 초기화
git lfs pull                 # 큰 파일 받기
git lfs ls-files --size-only # 사용량
```

## 다운로드 실패 정직 처리

각 파일의 sha256 + size + source_url + 다운로드 상태는 `manifest.json`에 기록.
- `status: "ok"` — 정상 다운로드 완료
- `status: "failed"` — 다운로드 실패, `reason` verbatim 기록 (open frontier 🟡, false PASS 0)

## 보관 규약 (DATASET/README.md 와 동일)

1. manifest.json — sha256 + size + source URL + tier per file
2. 대용량 raw 는 git LFS, 메타데이터는 직접 추적
3. 라이선스 명시 — 재배포 제한이면 URL pointer만
4. 측정 산출물(Φ)은 `state/xeno_x3_scan_*/result.json` 에 기록
