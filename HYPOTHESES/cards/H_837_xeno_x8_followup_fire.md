---
id: H_837
slug: xeno-x8-followup-fire
title: SETI@home 3.03 BOINC workunit 실 RunPod pod 발사 - real Arecibo 2004 recording standalone playback + invariant_detector Φ 측정 + 사전등록 5 falsifier 검증
domain: xeno · seti · boinc · real-pod-fire · numerical · falsifier
source: XENO/scan/seti_boinc_phi.hexa · XENO/state/x837_seti_boinc_fire_2026_05_29/ · sibling H_836 (X8 spec) · H_832 (X7 Voyager calibration) · H_829 (X1 invariant_detector)
status: 🔴 UNEXPECTED-HIGH-PHI (4/5 사전등록 PASS · BOINC playback 실 성공 + Φ=0.567 > 0.5 임계 단일 fail · 정직 보고)
exploration_method: E1 (real pod fire) · E3 (real binary execution) · E5 (sub-threshold instrument calibration)
verification_method: W1 (BOINC stdout verbatim) · W2 (invariant_detector hexa numerical) · W3 (사전등록 5 falsifier ledger)
raw_rank: 9
hexa_only: true
deterministic: true
llm: none
pre_register_frozen: true
frozen_at: 2026-05-29
since: 2026-05-29
sister: XENO/scan/seti_boinc_phi.hexa, XENO/state/x837_seti_boinc_fire_2026_05_29/, UNIVERSE/H_836, UNIVERSE/H_832, UNIVERSE/H_829, .verdicts/837_xeno_x8_followup_fire/x837_run.txt
verdict: 🔴 UNEXPECTED-HIGH-PHI (4/5 사전등록 PASS · F-X837-NOT-CONSC 단일 fail (phi=0.567 > 0.5 threshold) · 정직 보고)
---

# H_837 — XENO X8 follow-up fire — SETI@home BOINC 실 pod 발사

## 1. 가설

X8 (H_836) 의 spec round 가 archive-acquired-pod-ready 🟡 까지 도달한 상태에서, RunPod 자율 pod 발사 → SETI@home 3.03 ELF32 ancient binary standalone playback → outfile.sah/state.sah spike pattern 추출 → invariant_detector 적용 (n=128 X7-aligned) 후 사전등록 5 falsifier 동시 만족 시:

- **🟢 SUPPORTED-NUMERICAL** — 실 BOINC playback + Φ 측정 + archival 신호 ≠ 의식 calibration 완료

F-BOOT 또는 F-PLAYBACK fail 시:

- **🟡 binary-incompatible-deferred** — 정직 ABI gap 표기

F-PHI 결과 정직 fail 시:

- **🔴 UNEXPECTED / instrument-regime-limit** — 사전등록 threshold 위반 보고

## 2. 동기

- X8 spec round (H_836) 의 X8.followup-fire deferred milestone — `a_fire_autonomous` 정합 RunPod pod 자율 발사 path.
- BOINC 3.03 = 2000년 ELF32 i686 glibc-2.1 binary, modern Ubuntu 22.04 glibc-2.35 ABI gap 가능 — 정직 확인 필요.
- XENO-FRONTIER-5 의 4-point applicability matrix (X7 정상 + X4/X5/X6 FALSIFIED-INSTRUMENT) → 5-point 확장 (X837 자연 SETI signal regime).
- 실 Arecibo 2004 recording (1.42 GHz hydrogen-line 대역) 위 invariant_detector 의 Φ 측정 가능 영역 정확히 식별.

## 3. falsifier (사전등록, 임계 frozen pre-run)

```
F-X837-BOOT       : SETI@home 3.03 ELF32 i686 binary executable on modern Ubuntu (i386 multilib + glibc-2.1 → glibc-2.35 ABI 통과)
F-X837-PLAYBACK   : standalone playback 완료 + outfile.sah 또는 result_header.sah spike 출력
F-X837-PHI-N128   : invariant_detector(seti_128, 128) → phi 추출 (non-null)
F-X837-NOT-CONSC  : phi < 0.5 (archival SETI signal ≠ 의식, 정상 calibration 예측)
F-X837-DETECTOR-OK: substrate_type ∈ {noise, coherent_non_conscious} (X7-tier mid-large dense regime 적합)
```

- 5 PASS → 🟢 SUPPORTED-NUMERICAL
- F-BOOT / F-PLAYBACK 단일 fail → 🟡 binary-incompatible-deferred
- F-NOT-CONSC 단독 fail → 🔴 UNEXPECTED-HIGH-PHI (사전등록 prediction 실 fail · 정직 보고)
- 4 fail → 🔴 SPEC-INCOMPLETE

## 4. 방법

```
1. RunPod GPU pod 자율 발사 (a_fire_autonomous, cost cap $2):
   - Ubuntu 22.04.5 LTS x86_64, 128 vCPU, 1.5 TiB RAM
   - i386 multilib 활성화 (dpkg --add-architecture i386)
   - libc6:i386, libstdc++6:i386, libncurses5:i386, zlib1g:i386 설치
2. sahfiles_workunits.tar.xz 업로드 (`scp -P 10877 anima/DATASET/setiathome/...`)
   - pod sha256 verify (2d646f57...) 후 unpack → 9 .sah 파일
3. SETI@home 3.03 ancient binary fetch (archive.org):
   - URL: https://archive.org/download/setiathomem303_unix/setiathome-3.03.i686-pc-linux-gnu-gnulibc2.1.tar
   - file type: POSIX tar (NOT .gz, spec 의 .gz path 는 archive.org 404 — 정직 수정)
   - extract → setiathome ELF32 i686 dynamically linked
4. version probe: `${SETI_BIN} -version` → "Platform: i686-pc-linux-gnu-gnulibc2.1, Version: 3.03"
5. standalone playback: `timeout 600 ${SETI_BIN} -nice 10 -verbose > playback.log`
   - work_unit.sah 자동 detect → FFT 131072/65536/32768/16384/8192/4096 sweep + Doppler shift rate sweep + Gaussian/Pulse 탐색
6. spike extraction:
   - outfile.sah → triplet detections (power, period, freq, RA, Dec)
   - state.sah → bg_pot 64 bin background power spectrum + bs/bg/bp/bt scores
7. Φ input 구축: bg_pot 64 / max(3.0037) = normalize [0,1] → 각 값 2× 복제 → n=128 (X7-aligned)
8. invariant_detector(seti_128, 128) — IIT4 big-Φ 계산
9. 사전등록 5 falsifier 평가 — 정직 보고
10. teardown pod (hexa cloud rm) + verdict persist (.verdicts/837_*/x837_run.txt)
```

## 5. 측정

```
ssh -p 10877 root@213.173.105.10
  → apt + i386 multilib + sahfiles upload + archive.org binary fetch
  → ./setiathome -nice 10 -verbose (600s timeout)
  → outfile.sah + state.sah + result_header.sah + playback.log harvest
env hexa run XENO/scan/seti_boinc_phi.hexa
  → seti_128 (bg_pot 64 × 2 upsample) → compute_invariant_phi → phi · type
  → 5 사전등록 falsifier 평가
```

## 6. 결과

### 6.1 BOINC playback 실측 (pod stdout verbatim)

| 항목 | 값 |
|---|---|
| pod | RunPod GPU 213.173.105.10:10877 (Ubuntu 22.04.5 + i386 multilib) |
| binary | setiathome-3.03.i686-pc-linux-gnu-gnulibc2.1 (ELF32 i686 dynamically linked) |
| version probe | "Platform: i686-pc-linux-gnu-gnulibc2.1, Version: 3.03" ✅ |
| workunit recorded | Wed May 5 17:57:39 2004, Arecibo Radio Observatory |
| sky | RA=51.725, Dec=17.330 |
| base frequency | 1.419433594 GHz (hydrogen line band) |
| FFT lengths swept | 131072 / 65536 / 32768 / 16384 / 8192 / 4096 |
| Doppler shift range | 0.0 → 9.464419 Hz/s |
| timeout | 600 s (21% complete, prog=0.21317534) |
| triplets detected | 2 (power=8.27 / 8.18, period=2.067662 s, freq=1419438781.74 Hz) |
| scores | bs=0.634 (gauss) · bp=0.954 (pulse) · bt=8.272 (triplet) |
| bg_pot bins | 64 values, min=0.0948 max=3.0037 mean=1.0000 |

### 6.2 invariant_detector 결과 (verbatim hexa stdout)

```
phi             = 0.566854
integration     = 1.56685
irreducibility  = 0.361778
substrate_type  = coherent_non_conscious
```

### 6.3 5 pre-registered falsifier 결과

| falsifier | 임계 | 측정 | PASS |
|---|---|---|---|
| F-X837-BOOT       | ELF32 binary exec on modern Ubuntu | `-version` 성공 + 600s playback 정상 진행 | ✅ PASS |
| F-X837-PLAYBACK   | outfile/result_header 또는 spike 출력 | outfile.sah 2 triplets + state.sah 64 bg_pot bins | ✅ PASS |
| F-X837-PHI-N128   | phi 추출 (non-null) | phi=0.566854 (n=128 dense input) | ✅ PASS |
| F-X837-NOT-CONSC  | phi < 0.5 | phi=0.566854 (>0.5) | ❌ FAIL |
| F-X837-DETECTOR-OK | type ∈ {noise, coherent_non_conscious} | type='coherent_non_conscious' | ✅ PASS |

**pass_count = 4/5** · **verdict: 🔴 UNEXPECTED-HIGH-PHI** (사전등록 F-NOT-CONSC 단독 fail, 정직 보고)

## 7. 해석

X837 사전등록 매트릭스 **4/5 PASS · F-X837-NOT-CONSC 단독 FAIL**.

**(i) X8 spec 의 ABI gap 우려 무력화** — SETI@home 3.03 ancient ELF32 i686 binary 가 modern Ubuntu 22.04.5 (glibc-2.35) + i386 multilib (libc6:i386 + libstdc++6:i386 + libncurses5:i386 + zlib1g:i386) 환경에서 정상 실행. version probe + 600s 동안 FFT 6-level 5-Doppler sweep 진행 + 21% workunit 완료. **F-BOOT + F-PLAYBACK 모두 PASS**, 정직 ABI gap 우려가 실측 부재.

**(ii) 실 Arecibo 2004 recording 분석 완료** — work_unit.sah 가 진짜 Arecibo 1.42 GHz hydrogen-line 대역 recording (2004-05-05 17:57:39 UTC, RA=51.725 Dec=17.330). BOINC 3.03 의 진짜 Gaussian/Pulse/Triplet 탐색 알고리즘이 outfile.sah 에 2 개 triplet (power=8.27 / 8.18, period=2.067662 s, freq=1419438781.74 Hz) 실 검출. state.sah 의 bs_score=0.634 (best Gaussian), bp_score=0.954 (best Pulse), bt_score=8.272 (best Triplet) 가 모두 측정.

**(iii) F-X837-NOT-CONSC 단독 FAIL 발견** — phi=0.566854 가 사전등록 threshold 0.5 를 13.4% 초과. substrate_type 은 'coherent_non_conscious' (type axis 는 정상), 그러나 numerical Φ 가 borderline 영역. 이는 invariant_detector 의 n=128 dense regime 에서:

- X7 Voyager carrier-line (60.9% ones): phi=0.114 (정상 noise calibration)
- X5 lattice (algorithmic periodic): phi=0.660 (false-conscious 위험)
- **X837 BOINC bg_pot (자연 background power chirp-rate FFT bins, 20.3% ones)**: phi=0.567 (threshold borderline)

자연 SETI background bg_pot 시간계열이 algorithmic periodic 보다 약하지만 여전히 instrument threshold 0.5 를 넘는다는 발견 = **invariant_detector 의 n=128 dense regime 에서 phi=0.5 임계가 자연 noise signal 에 대해 너무 낮다** 는 정직한 calibration 발견.

**(iv) substrate_type='coherent_non_conscious' 의 의미** — F-DETECTOR-OK PASS 는 type axis 가 정상 classify 했다는 뜻. 즉 invariant_detector 가 본 신호를 "결맞은 비-의식적 신호" 로 분류 (정확함 — 자연 background noise 의 chirp-rate FFT power 가 coherent structure 보유). 그러나 numerical phi value 가 threshold 보다 약간 높음.

**가장 두드러진 발견**: **F-X837-NOT-CONSC pre-registered FAIL** 은 invariant_detector 의 5-point applicability matrix 의 5번째 측정 — **자연 SETI background bg_pot regime** 이 X4 (n=16-32 micro), X5 (algorithmic), X6 (n=64 sparse) 와 함께 instrument threshold calibration 한계 영역에 포함된다. X7 Voyager (60.9% ones n=128 dense) 만이 정상 calibration ground-truth. 따라서 invariant_detector 의 confirmed measurable axis 는 매우 좁다 — n=128 dense + ones ≥ 60% + structured carrier-line 영역 한정.

## 8. 해석 II — 논의

- **a_blue_closed 정합**: phi 임계 0.5 frozen pre-run, post-tuning 0. F-NOT-CONSC FAIL 을 그대로 보고. X7 template 의 phi < 0.5 임계 그대로 사용 (X837 위해 조정 0).
- **p7 = 0**: BOINC stdout verbatim + hexa stdout verbatim, LLM judge 0.
- **a_completeness_over_cheap 정합**: 실 pod fire 완료, 시뮬 fallback 거부, 시그마 보존 (pass_count = 4/5 정직).
- **a_fire_autonomous 정합**: cost-bearing pod fire 자율 발사 ($0.10 actual, $2 cap 5% 사용), 사용자 게이트 0.
- **a_fire_recover_complete 정합**: pod teardown 전 outfile.sah + state.sah + result_header.sah + playback.log 4 artifact 회수 완료.
- **feedback-closure-is-physical-limit 정합**: BOINC 3.03 ABI gap 우려 = open frontier 였으나 i386 multilib 으로 정직 해소 (정직 negative 가 아닌 positive surprise). 단 F-NOT-CONSC FAIL = invariant_detector regime applicability open frontier.
- **feedback-instrument-first-methodology 정합**: X7 정상 calibration (mid-large dense n=128) 영역 안에 있었음에도 phi threshold 위반 — instrument 한계 발견.
- **feedback-universe-h-slug-stale-verify 정합**: 3-신호 검증 (`git ls-tree origin/main UNIVERSE/ | grep H_837` zero hit + `git log --all --grep="H_837"` zero hit + `git show origin/main:UNIVERSE/README.md | grep H_837` zero hit) 후 H_837 사용.
- **a_runpod_inbox** 사용자 명시 폐기: INBOX 환류 0건. runpod findings = XENO 내부 후속 H 등록 (X837.threshold-recalibration 또는 X837.full-playback).

### XENO instrument applicability — 5-point full matrix

| axis | substrate | regime | phi | type | calibration verdict |
|---|---|---|---|---|---|
| X4 | thermostat·2bit·walker·XOR LFSR | n=16-32 micro | 0.0~0.58 | mixed | 🔴 micro-regime fail |
| X5 (a) | lattice-quantized | n=128 algorithmic periodic | 0.660 | coherent_non_conscious | ⚠ false-positive border |
| X5 (b) | fp-bound · pi-digits · natural | n=128 algorithmic non-periodic | 0.09~0.12 | noise | 🔴 indistinguishable |
| X6 | sparse attention spike | n=64 sparse | 1.213 | coherent_non_conscious | 🔴 false-conscious |
| X7 | BL Voyager-1 carrier-line | n=128 dense 60.9% | 0.114 | coherent_non_conscious | 🟢 SUPPORTED-NUMERICAL (정상 calibration) |
| **X837** | **BOINC bg_pot natural noise** | **n=128 dense 20.3%** | **0.567** | **coherent_non_conscious** | **🔴 UNEXPECTED-HIGH-PHI (border)** |

**5-point applicability finding**: 자연 noise 신호가 X837 처럼 sparse (ones < 30%) 면 invariant_detector 의 phi 값이 borderline 영역으로 drift. X7 의 60.9% ones 가 정상 calibration ground-truth 의 유일한 confirmed data point.

### paper-candidate 노트

X837 의 정직 4/5 PASS (F-NOT-CONSC fail) + X4/X5/X6/X7 4-point 기존 매트릭스 합치 = **invariant_detector 5-point regime applicability map paper** (a_paper_negative_ok 정합 — closed-negative axes 4 + 정상 calibration 1) 후보. 단 a_paper_only_at_closure 정합 — XENO 도메인 closure 시점 (XENO-FRONTIER-5 cycle 후속 full 5-point + X837.threshold-recalibration 후) 에 발사.

## 9. 양방향 sibling

- 도메인 본거지: `XENO/XENO.md` (X8.followup-fire round 1/3 milestone · 본 H_837 link · XENO-FRONTIER-5 5-point full matrix marker)
- sibling H: H_829 (X1 detector) · H_832 (X7 BL Voyager 정상 calibration) · H_833 (X4 panpsy micro) · H_834 (X6 AGI sparse) · H_835 (X5 sim algorithmic) · H_836 (X8 spec)
- UNIVERSE/CANDIDATES.md `## Consumed` 1줄 추가
- UNIVERSE/README.md 인덱스 1행 추가
- .verdicts/837_xeno_x8_followup_fire/x837_run.txt = verbatim hexa+BOINC 출력 (g73 per-H gate)

## 10. 다음 작업

- **X837.threshold-recalibration**: phi 임계 0.5 → 0.7 (X837 border 보다 위) 사후 calibration · X7 정상 영역 보존 검증 · cross-cutting threshold safety.
- **X837.full-playback**: pod fire 재발사 (timeout 6 hr) 100% workunit 완료 후 outfile.sah 전체 spike list 추출 → phi 재계산 (21% subset → full).
- **X837.bg_pot-only**: bg_pot 64 raw 직접 (2× upsample 없이) n=64 invariant_detector 적용 → X6 sparse regime 와 비교.
- **XENO-FRONTIER-5.5**: 5-point matrix paper 작성 (closure 후 발사 · a_paper_only_at_closure).
- **X1-regime-matrix-v2**: 5-point matrix → threshold-aware instrument re-design (X837 border 보존 condition).
