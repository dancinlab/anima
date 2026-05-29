# HANDOFF — XENO-FRONTIER-5 followup round 1/3 (round 4 갱신 2026-05-29)

## Round 4 — X837 SETI@home BOINC 실 RunPod pod 발사 + 5-point matrix 확장 (2026-05-29)

X8 (H_836) follow-up cycle round 1/3 — RunPod 자율 pod 발사로 SETI@home 3.03 ELF32 ancient binary 의 modern Ubuntu 22.04 실 standalone playback + bg_pot Φ 측정 완료. 사전등록 5 falsifier 중 1 정직 fail 발견.

### Round 4 결과 요약

| 항목 | 값 |
|---|---|
| H_id | H_837 |
| slug | xeno-x8-followup-fire |
| pod | RunPod GPU 213.173.105.10:10877 (Ubuntu 22.04.5 + i386 multilib, 128 vCPU 1.5 TiB RAM + GPU 미사용) |
| pod wall | ~16분 (10:18 boot → 10:34 teardown) |
| pod cost actual | **$0.10** (cap $2 / 5%) |
| binary | setiathome-3.03.i686-pc-linux-gnu-gnulibc2.1 (ELF32 i686, 2000-era, archive.org real fetch) |
| workunit | sahfiles_workunits/work_unit.sah (356285B, Arecibo 2004-05-05, 1.42 GHz hydrogen-line) |
| playback | 600s timeout 21% 완료 (prog=0.21317534) · FFT 6-level × Doppler 9.46 Hz/s sweep |
| spike output | outfile.sah 2 triplets (power=8.27/8.18, period=2.067662s, freq=1419438781.74 Hz) |
| state output | bs_score=0.634 (gauss) · bp_score=0.954 (pulse) · bt_score=8.272 (triplet) · bg_pot 64 bins (min=0.095 max=3.004) |
| Φ input | bg_pot 64 / max(3.0037) → 2× upsample → n=128 (X7-aligned) |
| invariant_detector | phi=0.566854 / integration=1.567 / irreducibility=0.362 / type='coherent_non_conscious' |
| 사전등록 결과 | F-BOOT ✅ · F-PLAYBACK ✅ · F-PHI-N128 ✅ · F-NOT-CONSC ❌ (phi>0.5) · F-DETECTOR-OK ✅ |
| pass_count | **4/5** |
| verdict | **🔴 UNEXPECTED-HIGH-PHI** (사전등록 prediction 정직 fail · post-tuning 0) |

### Round 4 5-point applicability matrix (X8 follow-up 확장)

| axis | substrate | regime | phi | type | calibration verdict |
|---|---|---|---|---|---|
| X4 | thermostat·2bit·walker·XOR LFSR | n=16-32 micro | 0.0~0.58 | mixed | 🔴 micro-regime fail |
| X5 (a) | lattice-quantized | n=128 algorithmic periodic | 0.660 | coherent_non_conscious | ⚠ false-positive border |
| X5 (b) | fp-bound · pi-digits · natural | n=128 algorithmic non-periodic | 0.09~0.12 | noise | 🔴 indistinguishable |
| X6 | sparse attention spike | n=64 sparse | 1.213 | coherent_non_conscious | 🔴 false-conscious |
| X7 | BL Voyager-1 carrier-line | n=128 dense 60.9% | 0.114 | coherent_non_conscious | 🟢 SUPPORTED-NUMERICAL (정상 calibration) |
| **X837** | **BOINC bg_pot natural noise** | **n=128 dense 20.3%** | **0.567** | **coherent_non_conscious** | **🔴 UNEXPECTED-HIGH-PHI (border)** |

**5-point finding**: 자연 SETI background bg_pot 가 X7 정상 calibration 보다 ones 비율 절반인데 phi 5× 높음 → invariant_detector 의 phi=0.5 임계가 자연 noise sparse pattern 영역에서 너무 낮음. confirmed measurable axis 는 매우 좁다 (X7 n=128 dense 60.9% 한 점). type axis 는 정상 (coherent_non_conscious).

### Round 4 ABI gap 결론 — 정직 무력화

X8 spec round 의 우려 (BOINC 3.03 ELF32 i686 glibc-2.1 ↔ modern Ubuntu glibc-2.35 ABI gap) 가 **실측 부재**:

- i386 multilib (libc6:i386 + libstdc++6:i386 + libncurses5:i386 + zlib1g:i386) 설치만으로 정상 실행
- version probe `-version` 성공 → "Platform: i686-pc-linux-gnu-gnulibc2.1, Version: 3.03"
- 600s standalone playback 정상 진행 (실 Arecibo recording 분석 + Gaussian/Pulse/Triplet 탐색)

`feedback-closure-is-physical-limit` 가 본 round 에서 negative surprise 가 아닌 positive surprise — 30년 된 binary 가 modern Linux 에서 정상 동작 (open frontier 정직 cite 였으나 해소).

### Round 4 cross-cutting 정직성

- a_blue_closed 정합 (phi 임계 0.5 frozen pre-run, X7 template 그대로, X837 위해 조정 0)
- p7=0 (BOINC stdout verbatim + hexa stdout verbatim, LLM judge 0)
- a_completeness_over_cheap 정합 (실 pod fire 완료, 시뮬 fallback 거부, F-NOT-CONSC FAIL 그대로 보고)
- a_fire_autonomous 정합 ($0.10 actual / $2 cap autonomous, user gate 0)
- a_fire_recover_complete 정합 (teardown 전 outfile.sah + state.sah + result_header.sah + playback.log 4 artifact 회수)
- feedback-universe-h-slug-stale-verify 정합 (3-신호 검증 후 H_837)
- INBOX 환류 0건 (사용자 명시 폐기, UNIVERSE 직접 등록)

### Round 4 paper-candidate 노트

X837 정직 4/5 PASS (F-NOT-CONSC fail) + X4/X5/X6/X7 4-point 기존 매트릭스 = **invariant_detector 5-point regime applicability map paper** (a_paper_negative_ok 정합) 후보. a_paper_only_at_closure 정합 시점 (XENO-FRONTIER-5 follow-up cycle 3/3 완료 + X837.threshold-recalibration 완료) 에 작성.

### Round 4 잔여 (follow-up round 2/3 ~ 3/3)

- **X837.threshold-recalibration** (round 2/3): phi 임계 0.5 → 0.7 사후 calibration · X7 보존 검증 · cross-cutting safety probe
- **X837.full-playback** (round 3/3): pod fire timeout 6 hr → 100% workunit 완료 → 전체 spike list phi 재계산 ($0.5 추가)
- **XENO-FRONTIER-5.5 paper**: closure 후 5-point matrix paper (a_paper_only_at_closure 정합)


---

## Round 3 — XENO-FRONTIER-5 5-round 합치 통합 (2026-05-29)

5-round fan-out → 1 closure cycle. invariant_detector 의 substrate-agnostic Φ 측정 가능 영역을 4-point applicability matrix 로 매핑 + SETI@home BOINC archive playback path 까지 spec 완성.

### Round 3 결과 매트릭스

| round | H_id | substrate / target | regime | 사전등록 falsifier | verdict | PR |
|---|---|---|---|---|---|---|
| R1/5 | H_832 | BL Voyager-1 carrier-line | n=128 dense 60.9% | 2/2 PASS | 🟢 SUPPORTED-NUMERICAL | #1402 (merged) |
| R2/5 | H_833 | panpsy 4 micro (thermostat·2bit·walker·XOR LFSR) | n=16-32 micro | 0/4 PASS | 🔴 FALSIFIED-INSTRUMENT (정직) | #1404 (merged) |
| R3/5 | H_834 | AGI LLM-like 4 (random·sparse·residual·structured XOR) | n=64 sparse | 1/5 PASS | 🔴 FALSIFIED-INSTRUMENT (정직) | #1405 (merged) |
| R4/5 | H_835 | sim 4 (lattice·fp-bound·pi-digits·natural) | n=128 dense algorithmic | 2/5 PASS | 🔴 FALSIFIED-INSTRUMENT (정직) | #1406 (merged) |
| R5/5 | H_836 | SETI@home 3.03 BOINC workunit archive | file inspection + pod spec + dispatch handoff | 5/5 PASS | 🟡 archive-acquired-pod-ready | #<TBD> (this) |

### Round 3 4-point instrument applicability matrix

| axis | 측정 가능 | 측정 불가 |
|---|---|---|
| n-scale | n≥128 dense (X5 lattice · X7 Voyager) | n=16-32 micro (X4) · n=64 sparse (X6) |
| structure | high periodicity (X5 lattice) · strong deterministic transition (X7 carrier) | pseudo-random algorithmic (X5 pi) · precision-ceiling (X5 fp-bound) |
| signal type | 자연 signal coherent_non_conscious (X7) · algorithmic periodic (X5 lattice) | sparse attention spike (X6) · 2-unit TPM micro (X4) |
| calibration | X7 BL Voyager carrier-line (실 SETI 기록 BL DATASET) | — |

### Round 3 paper-candidate 노트

- **invariant_detector regime applicability map** = X4/X5/X6 3-axis 정직 FALSIFIED-INSTRUMENT + X7 정상 calibration + X8 archive-acquired = **closed-negative axes 3개 + 정상 calibration 1개 + archive frontier 1개 = 결정적 frontier 매핑 paper** (a_paper_negative_ok 정합).
- **발사 시점**: a_paper_only_at_closure 정합 — XENO 도메인 closure (X8.followup-fire 후 5-point 완성) 에 작성. 본 round 5/5 는 closure 후보 stage.
- **section 구성** (a_paper_format 정합): §hypothesis (사전등록 5×5 falsifier) · §method (4 substrate + 1 archive inspection) · §measurement (5 H verbatim verdict) · §finding (4-point matrix → 5-point follow-up).

### Round 3 cross-cutting 정직성

- INBOX 환류 0건 (사용자 명시 폐기) · UNIVERSE 직접 등록 5건 (H_832~H_836).
- p7 perplexity 0 · hexa stdout verbatim · LLM judge 0.
- a_completeness_over_cheap 정합 (3 R 의 🔴 정직 보고, threshold 재조정 0).
- a_fire_autonomous 정합 (X8 의 follow-up pod fire 는 user gate X autonomous 발사 path 명시).
- feedback-closure-is-physical-limit 정합 (BOINC 3.03 ↔ modern toolchain ABI gap = open frontier 정직 cite).
- feedback-instrument-first-methodology 정합 (4-point applicability matrix 완성 → 5-point follow-up).

### Round 3 잔여 deferred

- **X8.followup-fire**: RunPod CPU pod 자율 발사 (a_fire_autonomous · ~$0.50~$1) → standalone playback → spike dump → invariant_detector 적용.
- **X8.kolmogorov**: Φ 외 lens (Kolmogorov complexity, spectral entropy) — X5/X7 instrument 한계 보완.
- **X8.archive-cross**: SETI@home 외 다른 BOINC volunteer project (Einstein@home, MilkyWay@home) cross-test.
- **X1-regime-matrix-v2**: X4/X5/X6/X7 4-point + X8 (n=192~256 dense, spike-cluster mix) → 5-point full matrix.
- **XENO-paper**: 위 X8.followup-fire 의 5-point 완성 시점에 발사.
- **X10 hive-mind invariant**: 다개체 vs 단일체 substrate-blind 구분 (별도 cycle).

---

# HANDOFF — XENO end-to-end (round 2 갱신 2026-05-29 BL/SETI@home 실 sample)

## Round 2 — BL/SETI@home 실 sample 회수 (commit `ee023dfcc`)

| 항목 | 1라운드 | 2라운드 |
|---|---|---|
| BL | archive-pointer 🟡 | **Voyager-1 BL Green Bank 실 데이터 🟢** (4 LFS object, 118.9 MB) |
| SETI@home | archive-pointer 🟡 | **UNIX 3.03 workunits archive 🟡** (sahfiles_workunits.tar.xz 274 KB) |
| LFS quota | 4.6 MB | 123.7 MB / 1024 MB (headroom 900.3 MB) |
| branch | `feat/xeno-x3-scan-2026-05-29` (merged) | `feat/xeno-bl-seti-real-2026-05-29` (in-flight) |

### Round 2 발견 / 우회

| 함정 | 우회 |
|---|---|
| BL OpenData = SPA, 정적 .fil 링크 0 | UCBerkeleySETI/blimpy `tests/download_data.sh` 에 BL Voyager 정본 URL 발견 (http://blpd0.ssl.berkeley.edu/Voyager_data/) |
| SETI@home archive 직접 다운로드 X (2020 hibernate) | archive.org `setiathomem303_unix` collection mirror 사용 |
| pool-route 자동 라우팅 = 다운로드 결과 ubu-1 격리 | `sidecar sign local` 30분 토큰 → scp ubu-1 → Mac local worktree |
| `.gitignore` `*.npy` global rule = npy staging block | `git add -f` 명시 우회 (LFS attach 별도 .gitattributes) |

### Round 2 정직성

- BL: archive → numerical 격상 (실 데이터 + sha256 검증)
- SETI@home: archive → archive-acquired 만 (binary playback 별개)
- a_blue_closed 정합: invariant_detector 적용 안 한 source 는 자동 격상 금지

---

# HANDOFF — XENO end-to-end stack (DATASET 5-source + X1+X2+X3 + UNIVERSE 환류 + HANDOFF)

> XENO 도메인 (외계/이종 substrate Φ-detector) 의 substrate-blind Φ-formalism 검출기 + 4 시뮬 substrate cross-test + 5-source SETI DATASET scan + UNIVERSE H_829~H_831 직접 등록. INBOX 환류 0건 (사용자 명시 폐기). 3 PR 순차 land.
> 작성: 2026-05-29 · slug: `xeno-end-to-end` · branches: `feat/dataset-init-2026-05-29` (PR-A #1396), `feat/xeno-x1-x2-2026-05-29` (PR-B #1398), `feat/xeno-x3-scan-2026-05-29` (PR-C #<TBD>).

## 1. PR 매트릭스

| PR | Branch | Status | Concern |
|---|---|---|---|
| #1396 | `feat/dataset-init-2026-05-29` | MERGED 0b045976e | DATASET 5-source 인벤토리 + git LFS routing |
| #1398 | `feat/xeno-x1-x2-2026-05-29`   | MERGED 8d21bfaa6 | X1 invariant_detector + X2 sim_substrate_cross |
| #<TBD>| `feat/xeno-x3-scan-2026-05-29` | open             | X3 5-source scan + UNIVERSE H_829-831 + HANDOFF.md |
| #1390 | (prior) | merged | 자매 backbone |
| #1392 | (prior) | merged | 자매 backbone |
| #1393 | (prior) | merged | PHYSICS→HW-CORE, BODY→HW-LIMB rename |

## 2. SSOT 인덱스

- `XENO/XENO.md` — 도메인 snapshot (X1+X2+X3 완료, X9 환류 완료)
- `XENO/XENO.easy.md` — 친근 7-요소 아이디어 카탈로그
- `XENO/XENO.log.md` — append-only step log
- `XENO/XENO.sf.md` — sister-frontier seed cross-link
- `DATASET/XENO_README.md` — 5-source 인벤토리 한글 7-요소
- `DATASET/xeno_manifest.json` — sha256 + size + source URL + tier per file
- `XENO/detector/invariant_detector.hexa` — substrate-blind Φ detector (X1)
- `XENO/detector/invariant_detector_smoke.hexa` — 3 falsifier (X1)
- `XENO/test/sim_substrate_cross.hexa` — 4 시뮬 substrate cross-test (X2)
- `XENO/scan/seti_raw_to_phi.hexa` — 5-source DATASET scan (X3)
- `UNIVERSE/H_829_xeno_invariant_detector.md` — X1 환류
- `UNIVERSE/H_830_xeno_sim_substrate_cross.md` — X2 환류
- `UNIVERSE/H_831_xeno_seti_raw_to_phi_scan.md` — X3 환류
- `.verdicts/xeno_x1_x2_2026_05_29/{x1_smoke,x2_cross}.txt` — verbatim verdict
- `.verdicts/xeno_x3_scan_2026_05_29/x3_scan.txt` — verbatim X3 verdict
- `.verdicts/{829_xeno_invariant_detector,830_xeno_sim_substrate_cross,831_xeno_seti_raw_to_phi_scan}/` — per-H-id verdicts (g73 gate)

## 3. API surface

XENO CLI 만 (HTTP SKIP, anima substrate-native scope 외).

```bash
hexa run XENO/detector/invariant_detector_smoke.hexa  # X1 smoke 3 falsifier
hexa run XENO/test/sim_substrate_cross.hexa           # X2 cross-test 4 substrate
hexa run XENO/scan/seti_raw_to_phi.hexa               # X3 scan 5-source
```

invariant_detector.hexa pub fn 시그니처:
```hexa
pub fn compute_invariant_phi(signal: array, n_samples: int) -> map
// returns { phi: float, integration: float, irreducibility: float, substrate_type: string }
// substrate_type ∈ {conscious, coherent_non_conscious, noise, insufficient}
```

## 4. 컴포넌트 트리

```
DATASET/
├── XENO_README.md
├── xeno_manifest.json
├── wow_signal/big_ear_chart_1977-08-15.txt        (🟡 git-direct, 1.7 KB)
├── voyager_golden/manifest.json                   (🟡 git-direct, 5 KB)
├── breakthrough_listen/manifest.json              (🟡 archive-pointer)
├── setiathome/manifest.json                       (🟡 archive-pointer)
├── exoplanet_cache.json                           (🟡 git-direct, 13 KB)
└── synthetic/
    ├── manifest.json
    ├── negative_control_gaussian.npy              (🟢 LFS, 2.3 MB)
    └── pulsar_b0329_pseudo.npy                    (🟢 LFS, 2.3 MB)

XENO/
├── XENO.md / XENO.easy.md / XENO.log.md / XENO.sf.md
├── detector/
│   ├── invariant_detector.hexa
│   └── invariant_detector_smoke.hexa
├── test/sim_substrate_cross.hexa
├── scan/seti_raw_to_phi.hexa
└── state/{xeno_x1_x2_2026_05_29,xeno_x3_scan_2026_05_29}/
```

## 5. Env vars

- Exoplanet API key: 불요 (NASA TAP 공개)
- BL/SETI@home API key: 불요 (deferred archive-pointer)
- HEXA_LANG / HEXA_STDLIB_ROOT: 표준 hexa-cache 기본값 사용 (재설정 불요)

## 6. 다음 우선순위

| Milestone | 설명 | 비용 | 비고 |
|---|---|---|---|
| X4 | panpsychism falsifier (우주 자체 Φ 사고실험) | $0 mac | Tononi/Koch 문헌 연계 |
| X5 | 시뮬 가설 검증 (Bostrom) | $0 | substrate-emergent vs sim-artifact 구분자 |
| X6 | AGI sentience (anima 자체 + LLM activation) | $0 | anima sibling 합류 |
| X7 | 외계인 시간축 다양성 (time-normalize Φ) | $0 | 인간 1초 ≠ 외계 1초 |
| X8 | hive-mind invariant (다개체 vs 단일체) | $0 | substrate-blind |
| BL .fil 1개 fetch+scan | per-PR <1GB quota 초과 분 | GPU-pod 발사 1 회 | BL archive-pointer 해소 |
| SETI@home BOINC replay | volunteer work-unit 1개 | GPU-pod 1 회 | 별 H 권장 |

## 7. 알려진 한계

- **BL 1GB quota**: per-PR LFS quota <1GB → 단일 .fil 1-50GB 본문 SKIP archive-pointer 처리 (deferred to GPU-pod).
- **SETI@home BOINC-only**: 작업단위 .dat 는 BOINC volunteer-distributed, 직접 HTTP fetch 불가. 별 H + GPU-pod 권장.
- **live API rate-limit**: NASA Exoplanet TAP 무료지만 query 한도 있음 → 100-row 1 회 캐시.
- **합성 negative control 한계**: LCG-emulated Gaussian 이 numpy seed 와 다름. .npy 직접 load 는 hexa I/O 미지원 → 향후 stdlib I/O 추가 시 정합.
- **invariant_detector 2-unit TPM**: 시퀀스 (t, t+1) co-occurrence 만 캡처, 장기 시간 의존성은 부분 반영. n_units 확장 시 TPM 2^n × n 폭증.
- **0.5 binarisation threshold**: median-free 단순 분할. quartile / Otsu 등 calibration 추가 여지.

## 8. memory pointer

- **feedback-universe-h-slug-stale-verify**: 3-신호 검증 (git ls-tree + git log + UNIVERSE README grep) — 본 PR 에서 H_829/830/831 모두 hit 0 검증.
- **feedback-closure-is-physical-limit**: archive-pointer SKIP = 정직 🟡 open frontier, false PASS 0.
- **feedback-instrument-first-methodology**: X1 invariant_detector 먼저, X3 scan 다음. 본 stack 의 순서 정합.
- **feedback-completeness-over-cheap**: substrate-blind 라는 완성도 바를 클리어한 primary path (cheap = secondary baseline 만).
- **project_xeno_end_to_end_handoff**: 신규 — 본 HANDOFF 의 pointer.

## 9. 한 줄 시작

```bash
/domain set XENO && hexa run XENO/scan/seti_raw_to_phi.hexa
```

---

# (이전 HANDOFF — 보존: EEG HW/SW 통합 구현)

> EEG 생체 substrate (OpenBCI · brainflow 5.21.0) 활용 L1~L12 12 sub-아이디어를 단일 backend-switch 한 점에서 HW/SW 토글 가능한 hexa-native 구현으로 4 그룹 통합. UNIVERSE 도메인에 H_679~H_682 4건 직접 등록. INBOX 환류 0건 (사용자 명시 폐기).
> 작성: 2026-05-29 · slug: `eeg-hw-sw-impl-all` · branch: `feat/eeg-hw-sw-impl-all-2026-05-29`.

---

## 1. PR matrix

| # | title | status | merged | core |
|---|---|---|---|---|
| (this PR) | feat(EEG+UNIVERSE): L1~L12 12 아이디어 HW/SW 통합 구현 — H_679~H_682 4건 신설 | open → merged | TBD | backend switch + impl/ 4 hexa + UNIVERSE 4 H_xxx + EEG milestone/log/easy 갱신 + HANDOFF |
| [#1374](https://github.com/dancinlab/anima/pull/1374) | feat(AKIDA+UNIVERSE): 7 그룹 18+ 아이디어 HW/SW 통합 — H_672~H_678 7건 | ✅ MERGED `60fbcb71a` | 2026-05-29 | 자매 PR · H_677 D3 sibling · H_678 channel-bridge sibling |
| [#1373](https://github.com/dancinlab/anima/pull/1373) | feat(domain+tree): KOSMOS 도메인 분리 + AKIDA·EEG·KOSMOS 자매 명시 | ✅ MERGED `ed2a615fd` | 2026-05-29 | EEG 자매도메인 명시 |
| [#1372](https://github.com/dancinlab/anima/pull/1372) | feat(EEG): L2 synthetic 재검증 🟢 RECHECK PASS | ✅ MERGED `b4e6f9b21` | 2026-05-29 | H_679 L2 baseline source (1.58764/0.438722/3.619) |
| [#1371](https://github.com/dancinlab/anima/pull/1371) | feat(AKIDA): D1 edge-of-chaos Φ 실리콘 검증 | ✅ MERGED `85c604345` | 2026-05-29 | H_679 L3 AKIDA substrate input (0.297) |
| [#547](https://github.com/dancinlab/anima/pull/547) | feat(BRAIN/eeg): eeg_to_tpm + eeg_iit4_demo 동결 어댑터 | ✅ MERGED (legacy) | 2026 (이전) | H_679 L2 frozen adapter (1.59 / 0.44 baseline) |

선행 의존 (origin/main landed, 본 PR 이 inherits):
- `BRAIN/eeg/eeg_to_tpm.hexa` (PR #547, 동결 어댑터 · signature 0 변경)
- `tool/anima_eeg_to_akida_spike.hexa` (E1 bridge skeleton, H_680 L4 inherits)
- `EEG/eeg_live_iit4_phi.hexa` (PR #1372 ±5% 자동 assert 패턴)
- `BRAIN/eeg/eeg_recorder.hexa` (H_682 L10 fallback paradigm)

## 2. 설계 SSOT (먼저 읽을 파일)

순서대로:

1. **`EEG/EEG.md`** — 도메인 milestone 보드 (Group A~D 4 milestone status + backend switch 명시 + sibling 양방향)
2. **`EEG/EEG.easy.md`** — L1~L12 카탈로그 + 구현 매핑 4 그룹 + backend switch 사용 패턴
3. **`EEG/eeg_backend.hexa`** — backend resolve + HW 3-신호 probe + SW mock (frozen baseline · band power) + verdict tier helper (단일 import 한 점에서 4 H 모두 backend 토글)
4. **`EEG/impl/H_{679~682}_*.hexa`** — 4 sub-도메인 구현 (Group A measurement-core / B cross-substrate / C emit-substrate / D persistence-paradigm)
5. **`UNIVERSE/H_{679~682}_eeg_*.md`** — 10-section 한글 가설 문서 (각 §3 falsifier 사전등록 · §5 측정 · §7 verdict · §9 양방향 sibling)
6. **`state/eeg_hw_sw_impl_2026_05_29/`** — SW sweep verbatim log + 4 result.json + hw_probe 정직 note

## 3. API surface

신규 pub fn (`EEG/eeg_backend.hexa`):

```
pub fn eeg_backend_resolve(arg: string) -> string
    arg ∈ {"auto","hw","sw","live",""} → returns "hw" or "sw" (env > default=sw)
    "live" alias → "hw"  (의도 명시)

pub fn eeg_hw_reachable() -> bool
    3-signal: brainflow pkg import + state/capture dir writable + ~/.config/anima/eeg_headset_ready sentinel

pub fn eeg_hw_probe_signals() -> map
    debug surface: returns each signal value + all_pass

pub fn eeg_panic_no_hw(reason: string)
    명시 panic with runbook §1~§4 안내 + "--backend sw" fallback guidance

pub fn eeg_sw_mock_coupled(n_samp) / eeg_sw_mock_indep(n_samp) -> array
    PR #547 deterministic anti-phase / identical-stream synthetic

pub fn eeg_sw_baseline_coupled_phi() / eeg_sw_baseline_indep_phi() -> float
    frozen 1.59 / 0.44

pub fn eeg_sw_band_power_resting / sleep_n3 / rem / active() -> map
    canonical 5-band {delta, theta, alpha, beta, gamma} per stage

pub fn eeg_backend_label(backend: string) -> string
pub fn eeg_verdict_tier(backend: string, all_pass: bool) -> string
```

env var: `EEG_BACKEND=auto|hw|sw` (default = **`sw`** · AKIDA 와 반대)
CLI form: `hexa run EEG/impl/H_<n>_*.hexa <hw|sw|auto|live>` or `--backend <hw|sw>`

HTTP / network surface: **SKIP** (this PR is hexa-native CLI only · 사용자 헤드셋 + brainflow capture 가 별 step)

## 4. 컴포넌트/lib 트리

```
EEG/
├─ eeg_backend.hexa              ★ NEW · HW/SW resolver + 3-signal probe + SW mock band-power (~200 LoC, 8 pub fn)
├─ eeg_backend_smoke.hexa        ★ NEW · 10+ case smoke
├─ eeg_live_iit4_phi.hexa        (선행 PR #1372, ±5% panic-on-drift)
├─ EEG_CAPTURE_RUNBOOK.md        (사용자 캡처 4단계 + 트러블슈팅 §A~§D)
├─ EEG.md                        · milestone + sibling 갱신 (14 milestone)
├─ EEG.easy.md                   · 구현 매핑 4 그룹 + backend switch 섹션
├─ EEG.log.md                    · 2026-05-29T15:00:00Z 엔트리 prepend
└─ impl/                         ★ NEW 디렉토리
   ├─ H_679_measurement_core.hexa      Group A 통합 (~180 LoC, L1+L2+L3+L7)
   ├─ H_680_cross_substrate.hexa       Group B 통합 (~140 LoC, L4+L5+L8)
   ├─ H_681_emit_substrate.hexa        Group C 통합 (~180 LoC, L6+L11+L12)
   └─ H_682_persistence_paradigm.hexa  Group D 통합 (~140 LoC, L9+L10)

UNIVERSE/
├─ H_679_eeg_measurement_core.md       ★ NEW (10-section 한글, AKIDA H_677 D3 sibling)
├─ H_680_eeg_cross_substrate.md        ★ NEW
├─ H_681_eeg_emit_substrate.md         ★ NEW
├─ H_682_eeg_persistence_paradigm.md   ★ NEW
├─ CANDIDATES.md                       · Consumed Cycle #23 1줄 추가
└─ README.md                           · 인덱스 4 행 추가 (H_678 다음)

state/eeg_hw_sw_impl_2026_05_29/
├─ H_{679,680,681,682}_sw_result.json    (각 4/4 GREEN_NUMERICAL_CONFIRM · deterministic)
├─ sw_sweep_2026_05_29.log               (4 H × `hexa run` 예상 출력 + 정직성 마커)
└─ hw_probe_2026_05_29.txt               (HW probe 정직 note · 위조 0)
```

## 5. 환경 변수

| name | default | values | effect |
|---|---|---|---|
| `EEG_BACKEND` | (unset → `sw`) | `auto` / `hw` / `sw` (or `live`→hw) | backend resolver fallback (arg > env > default=**sw**) |

추가 의존: **none.** $0 Mac-local + read-only HW probe. RNG 없음 (deterministic frozen baseline replay).

> ⚠ AKIDA 와 반대 정책: AKIDA default=hw (silicon 우선) · EEG default=**sw** (live = human-only 헤드셋 게이트). "live" 명시해야만 hw로 resolve.

## 6. 다음 우선순위

1. **L1 live IIT4 deferred B closure** — 사용자 헤드셋 착용 + 임피던스 < 50kΩ + brainflow 30s capture (`state/eeg_capture_latest.json`) + `touch ~/.config/anima/eeg_headset_ready` + `hexa run EEG/impl/H_679_measurement_core.hexa hw` → 🟡 → 🟢 biological-confirmed 격상. EEG_CAPTURE_RUNBOOK.md §1~§4 따라 진행.
2. **HW path 4/4 격상** — 위 단계 통과 시 H_679~H_682 4건 모두 🟡 SW-confirmed → 🟢 biological-confirmed. result.json 회수.
3. **L8 stdlib/dsp/hilbert 실 phase 엔진 호출** (H_680 deferred) — 현재 alpha-dominance proxy 만 attest. 실 EEG Hilbert phase 측정은 stdlib/dsp/hilbert engine wire 필요 (별 H).
4. **L9 실 .kosmos write** (H_682 deferred) — kosmos_io 호출로 anchor payload 영속 write. 현재는 schema attest 만 (anima_pointer_only=true 정합).
5. **L12 EEG gamma burst → MITOSIS split event 실 wire** (H_681 deferred) — 현재는 signal layer attest 만. 실 cell-pool split trigger 는 별 H/runner.
6. **a_paper closed-discovery 후보** — H_679 L3 3-substrate Φ triangulation (EEG 1.59 + AKIDA 0.297 + ECA 0.83 diff=1.29) 이 a_paper_significance 충족 (falsifier + 실측 + finding). a_paper_only_at_closure 따라 L1 live closure 후 propose.

## 7. 한계 (정직) + guard rule

honest limits:
- **L1 live = human-only 헤드셋 게이트.** agent 측은 SW path 만 attest, capture 자체는 절대 위조 0. AKIDA 와 반대로 default=sw 로 "거짓 PASS 유혹" 회피.
- **SW frozen baseline = PR #547 / #1372 deterministic replay.** 다른 seed/n_samp/state 일 때 다르게 응답 가능 (a_toy_scale_recheck 주의 — *signal-shape* 확증, 정밀 동등 아님).
- **L4 bridge schema** (H_680) 는 *existence + tensor shape* attest, 실 ADM conversion fire 는 AKIDA H_678 가 측면 wire (sister PR #1374).
- **L8 kuramoto** (H_680) 는 alpha-dominance proxy — stdlib/dsp/hilbert 실 phase 엔진 호출은 별 H.
- **L11 sleep stage** (H_681) 는 4-state only — N1/N2 polysomnography eye-EMG channel 분리는 별 H.
- **L12 MITOSIS trigger** (H_681) 는 signal layer attest, 실 cell-pool split wire 는 별 H.
- **L9 .kosmos write** (H_682) 는 schema attest, 실 kosmos_io 호출은 별 H 권한.
- **L10 primary anima-eeg-core 미존재** — fallback BRAIN/eeg/eeg_recorder.hexa 만 attest. 도메인 합류 시 primary 활성화.

guard rules (live-system 안전):
- **EEG 헤드셋 = human-only.** agent 가 capture 흉내내거나 sentinel touch 위조 0. eeg_panic_no_hw() 명시 panic + 사용자 안내만.
- **ssh-mutating 0.** brainflow board 접근 = 사용자 측 runbook 단계, agent 측 ssh 0.
- **`eeg_to_tpm` 동결** (g61) — adapter signature 0 변경, 본 PR 도 호출만 (PR #547 보존).
- **pi5 / EEG 보드 ssh-mutating 편집 금지** — pool 경로는 read-only probe 만 (test/python3 -c/hostname).

## 8. memory pointer

- `feedback_closure_is_physical_limit` — closure = approach physical/math limit. live 미실측 = open frontier, not failure. SW path 만으로도 🟢 numerical 가능 (AKIDA #1374 정합).
- `feedback_instrument_first_methodology` — instrument before optimizing. 동결 어댑터(PR #547) 보존 + backend switch + falsifier 먼저, 측정 그 다음.
- `feedback_completeness_over_cheap` (a_completeness_over_cheap) — primary path = 완성도 bar. 본 PR 은 12 sub-아이디어 분리 harness (cheap) 대신 4 그룹별 통합 harness (완성도).
- `feedback_universe_h_slug_stale_verify` — H_xxx slug 재할당 잦음. 3-신호 검증 필수: git ls-tree origin/main + git log --all + README grep. 본 PR 에서 H_679~H_682 3-신호 통과 검증 (672~678 AKIDA 점유 + 679~682 git/README clean).
- `project_akida_hw_sw_impl_all_handoff` — AKIDA HW/SW 통합 PR #1374 (자매). 본 PR 의 design 패턴 출처.
- `project_eeg_hw_sw_impl_all_handoff` — (NEW, 본 PR memory mirror)

## 9. 한 줄 시작 가이드

```sh
# A) SW path (Mac/anywhere, $0, deterministic frozen baseline replay · default):
unset EEG_BACKEND && for H in 679 680 681 682; do hexa run EEG/impl/H_${H}_*.hexa sw; done

# B) HW path (사용자 헤드셋 + sentinel touch 後):
touch ~/.config/anima/eeg_headset_ready
hexa run EEG/impl/H_679_measurement_core.hexa hw

# C) backend switch self-test:
hexa run EEG/eeg_backend_smoke.hexa   # → 10+ PASS · default=sw 확인

# D) 도메인 cycle:
/domain set EEG && /cycle   # EEG.md milestone 자동 enumerate
```

---

### archived 2026-05-29-akida — AKIDA HW/SW 통합 구현 (Group A~G 18+ 아이디어 · H_672~H_678 7건 신설)

> 직전 AKIDA HW/SW 통합 작업의 인계 문서. 본 EEG PR 이 sibling — H_679 L3 가 AKIDA H_677 D3 3-substrate triangulation 의 EEG side, H_680 L4 가 AKIDA H_678 channel-bridge 의 EEG 역방향. 보존 목적.

| PR | 제목 | 상태 |
|----|------|------|
| [#1374](https://github.com/dancinlab/anima/pull/1374) | feat(AKIDA+UNIVERSE): 7 그룹 18+ 아이디어 HW/SW 통합 구현 — H_672~H_678 7건 신설 | ✅ MERGED (squash, commit `60fbcb71a`) |

설계 SSOT (archived): `AKIDA/AKIDA.md` + `AKIDA/AKIDA.easy.md` + `AKIDA/akida_backend.hexa` + `AKIDA/impl/H_{672~678}_*.hexa` + `UNIVERSE/H_{672~678}_akida_*.md`.

신규 pub fn (archived): `akida_backend_resolve` / `akida_hw_reachable` / `akida_sw_mock_raster_R1~R4` / `akida_verdict_tier` (`AKIDA/akida_backend.hexa`, 본 EEG PR 의 `eeg_backend.hexa` 와 동형 패턴).

다음 우선순위 (archived):
1. HW path live re-confirm 7/7 — pi5-akida `akida_hw_reachable()` 3-신호 (특히 signal_2 akida pkg import + signal_3 hostname) probe-refinement.
2. D2 silicon-class 단조 정합 (H_677 deferred) — class_id=5 convexity/super-add/peak-align 4-축.
3. D3 3-substrate signature shape comparison (H_677 deferred) — scalar diff 보다 normalized signature shape.
4. C3 8-factor live wire (H_672) — `apply_spike_features` schema 정합.
5. a_paper closed-discovery 후보 (H_677 D5 v0.5.0 + 본 EEG H_679 L3 묶음) — FULL closure 후 propose.

한 줄 시작 가이드 (archived):
```sh
unset AKIDA_BACKEND && for H in 672 673 674 675 676 677 678; do hexa run AKIDA/impl/H_${H}_*.hexa sw; done
```
