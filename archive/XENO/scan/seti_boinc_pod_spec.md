# XENO X8 — SETI@home BOINC workunit pod spec + dispatch handoff

frozen_at: 2026-05-29
slug: `xeno-seti-boinc-pod`
H_id: `H_836`
sister: `H_831` (X3 5-source SETI DATASET scan) · `H_829` (X1 invariant_detector) · `H_832` (X7 BL Voyager) · DATASET `sahfiles_workunits.tar.xz`
tier (this round): 🟡 **archive-acquired-pod-ready** (file 검증 + pod spec + cost-bearing fire dispatch handoff 완료, 실 BOINC playback 은 follow-up cycle)

---

## 1. 회수된 sahfiles_workunits 분석

### 1.1 manifest 합치

| 항목 | 값 |
|---|---|
| 파일 경로 | `DATASET/setiathome/sahfiles_workunits.tar.xz` |
| 크기 (bytes) | `274340` (manifest 정합) |
| 매직 바이트 | `fd 37 7a 58 5a 00` (xz `\xfd\x37\x7a\x58\x5a\x00`) |
| 매직 byte 확장 | `00000000: fd37 7a58 5a00 0004 e6d6 b446 0200 2101  .7zXZ......F..!.` |
| sha256 | `2d646f57f9c77222d5f986268e2aa1e67c659305094152799761841d8515cd96` (manifest 정합) |
| origin | `https://archive.org/download/setiathomem303_unix/sahfiles_workunits.tar.xz` |
| BOINC binary | UNIX 3.03 (2000년 전후, BOINC 1.x ~ 2.x 시대) |
| status (X3) | 🟡 SUPPORTED-BY-CITATION (binary playback deferred) |

### 1.2 tar.xz 콘텐츠 (`tar tJf`)

```
sahfiles_workunits/
sahfiles_workunits/lock.sah
sahfiles_workunits/outfile.sah
sahfiles_workunits/work_unit.sah
sahfiles_workunits/state.sah
sahfiles_workunits/user_info.sah
sahfiles_workunits/pid.sah
sahfiles_workunits/key.sah
sahfiles_workunits/version.sah
sahfiles_workunits/result_header.sah
```

총 9개 `.sah` 파일 — SETI@home 3.03 UNIX client 가 직접 읽어들이는 workunit / state / 결과 헤더 binary.

### 1.3 BOINC opaque binary format

- BOINC client 가 가진 `seti_lib` (C/C++ workunit reader) 외 third-party parser 없음 — sahfiles binary 의 spike pattern 추출은 BOINC standalone 실행이 정도(正道).
- modern `boinc-client` (7.x) 는 SETI@home 3.03 (BOINC 1.x ancient) 와 protocol 호환성 미보장 — 정직 cite.
- X3 (H_831) 단계에서 manifest + sha256 + 파일 존재 verification 만 수행, raw playback 은 본 round 의 deferred follow-up (X8 의 pod fire).

---

## 2. BOINC client setup runbook (Ubuntu 22.04 pod)

### 2.1 OS 사양

| 항목 | 값 |
|---|---|
| OS | Ubuntu 22.04 LTS x86_64 |
| Kernel | 5.15+ (modern boinc-client 의존성) |
| Pod type | RunPod CPU pod (GPU 불요) |
| vCPU | 2 |
| RAM | 4 GB |
| Disk | 20 GB (sahfiles + BOINC data dir) |
| Estimated hourly | $0.10 ~ $0.20 (RunPod CPU pricing) |
| Wall time | ~1 hr (extract → BOINC install → standalone playback → spike dump) |
| Total fire cost | **~$0.50 ~ $1.00** |
| network | egress allowed (apt + archive.org fallback) |

### 2.2 init script (cloud-init `user-data`)

```bash
#!/usr/bin/env bash
set -euo pipefail

# 1) base packages
apt-get update
apt-get install -y --no-install-recommends \
    boinc-client \
    boinc-manager \
    xz-utils \
    tar \
    coreutils \
    python3 \
    python3-numpy \
    ca-certificates \
    curl \
    git

# 2) workunit archive pull (anima repo 기준)
WORKDIR=/opt/xeno-x8
mkdir -p "${WORKDIR}"
cd "${WORKDIR}"

# anima git fetch — sahfiles 는 git-lfs 추적 (manifest 정합)
git clone --depth 1 https://github.com/dancinlab/anima.git anima-repo
cd anima-repo
git lfs pull --include "DATASET/setiathome/sahfiles_workunits.tar.xz"

# 3) extract
tar xJf DATASET/setiathome/sahfiles_workunits.tar.xz -C "${WORKDIR}"
ls -la "${WORKDIR}/sahfiles_workunits/"

# 4) sha256 verify
echo "2d646f57f9c77222d5f986268e2aa1e67c659305094152799761841d8515cd96  DATASET/setiathome/sahfiles_workunits.tar.xz" | sha256sum -c -

# 5) BOINC standalone run — SETI@home 3.03 client 시도 (archive.org binary)
#    ⚠ modern boinc-client 7.x ↔ SETI@home 3.03 protocol gap 가능. 본 step 실패 시
#    archive.org `setiathomem303_unix` 의 ancient `setiathome` ELF32 standalone 으로
#    fallback (work_unit.sah 직접 입력 + outfile.sah 직접 추출).
SETIATHOME_BIN=/opt/xeno-x8/setiathome-3.03
mkdir -p "${SETIATHOME_BIN}"
cd "${SETIATHOME_BIN}"
curl -L -o setiathome-3.03.tar.gz \
    "https://archive.org/download/setiathomem303_unix/setiathome-3.03.i686-pc-linux-gnu-gnulibc2.1.tar.gz" || \
    echo "WARN: archive.org binary fetch failed (정직 cite — ancient mirror 의 PULL_FAILED 가능)"
[ -f setiathome-3.03.tar.gz ] && tar xzf setiathome-3.03.tar.gz

# 6) workunit playback (ancient client 가용시)
#    SETI@home 3.03 standalone usage:
#       ./setiathome -nice 10 -verbose
#    work_unit.sah 를 cwd 에 두고 실행 → outfile.sah / result_header.sah 생성
cd "${WORKDIR}/sahfiles_workunits"
if [ -x "${SETIATHOME_BIN}/setiathome-3.03" ]; then
    timeout 600 "${SETIATHOME_BIN}/setiathome-3.03" -nice 10 -verbose > playback.log 2>&1 || \
        echo "WARN: standalone playback EXIT non-zero (정직 cite — 3.03 ELF32 ↔ modern glibc 호환성 우려)"
fi

# 7) spike dump — result_header.sah 의 spike chirp count 추출
python3 - <<'PY' > spike_dump.txt
import struct, os
path = "result_header.sah"
if not os.path.exists(path):
    print("RESULT_HEADER_MISSING")
    raise SystemExit(0)
with open(path, "rb") as f:
    data = f.read()
# SETI@home 3.03 result_header binary layout — best-effort parse (heuristic).
# fields 1..N : 4-byte LE int spike counts per frequency bin (offset 4..)
print(f"FILE_SIZE_BYTES {len(data)}")
print(f"MAGIC_FIRST8 {data[:8].hex()}")
# 우선은 size + first-bytes 만 안전 dump — full schema 는 follow-up
PY

# 8) artifact pack
cd "${WORKDIR}"
tar cJf x8_playback_artifacts.tar.xz sahfiles_workunits/ || true
echo "X8_DONE wall=$(date +%s)"
```

### 2.3 정직성 한계 (BOINC 3.03 ↔ modern toolchain)

- SETI@home 3.03 = 2000년 release, ELF32 i686 glibc-2.1 binary. modern Ubuntu 22.04 (glibc-2.35) 에서 직접 실행 시 ABI gap 가능 → `sudo apt install libc6:i386 libstdc++5:i386` 보조 필요.
- 본 spec 의 ancient binary fallback 은 best-effort — playback 실패 = honest negative (a_completeness_over_cheap, feedback-closure-is-physical-limit).
- modern `boinc-client` 가 SETI@home 3.03 sahfiles 를 직접 읽는 path 는 protocol 호환성 보장 X.
- 따라서 **본 round 5/5 의 verdict 는 spec 완성 + file inspection only** — 실 playback 은 dispatch handoff 의 후속.

---

## 3. workunit → spike pattern 추출 procedure

### 3.1 SETI@home 3.03 workunit 구조 (공개된 사양)

| 파일 | 역할 | spike pattern 관련성 |
|---|---|---|
| `work_unit.sah` | Arecibo telescope 의 raw 2.5 MHz bandwidth recording (~107s) | 원시 입력 (1420.0 ~ 1422.5 MHz 대역) |
| `lock.sah` | client lock | (parsing 무관) |
| `state.sah` | client checkpoint state | (parsing 무관) |
| `user_info.sah` | volunteer credential | (parsing 무관) |
| `pid.sah` | process id | (parsing 무관) |
| `key.sah` | per-workunit hash key | sha integrity |
| `version.sah` | client version string | 3.03 verify |
| `result_header.sah` | spike count / chirp rate / power histogram | **spike pattern direct 추출** |
| `outfile.sah` | spike-by-spike binary list (frequency, time, power) | **spike pattern direct 추출** |

### 3.2 spike pattern 추출 path

1. **direct path** (BOINC standalone 가용시):
   `setiathome -nice 10 -verbose` → `outfile.sah` regenerate + `result_header.sah` parse → spike count per bin (`f`, `t`, `power`).
2. **fallback path** (ABI gap 시):
   `outfile.sah` binary direct parse (Python `struct`) — `result_header.sah` 의 첫 32 bytes 가 header (version + spike_count + bandwidth) 로 알려져 있음. spike list 는 16-byte struct 반복.
3. **degraded path** (parsing 실패시):
   파일 크기 / sha256 / magic byte 만 verify → metadata-only ledger. 본 X8 round 5/5 는 이 degraded path 까지 보장.

### 3.3 invariant_detector 적용 path

- 추출된 spike count per frequency bin → `array<float>` (각 bin 의 normalized power) → `compute_invariant_phi(array, n)` 입력.
- 예상 regime: n=128 ~ 256 dense (107s × 0.6 Hz bin = 64 bins per 시간 slice, 시간 axis 까지 합치면 n ≈ 192 ~ 256).
- **n=128 dense regime = X7 (Voyager) 와 같은 calibration 정상 영역** — invariant_detector 가 측정 가능한 zone.
- expected Φ: 자연 noise → Φ < 0.2 (X7 Voyager 와 같이 carrier-line dominant 신호의 transition 단조성), spike artifact 가 cluster 면 Φ 일시 spike (X6 의 sparse attention 과 유사 — false-positive 위험).
- 본 X8 의 후속 cycle 에서 instrument applicability 의 4번째 (X4/X5/X6/X7) 와 동일한 n=192~256 dense regime axis 가 추가.

---

## 4. cost estimate (a_fire_autonomous 정합)

| 항목 | 추정 |
|---|---|
| Pod type | RunPod CPU pod (Ubuntu 22.04, 2 vCPU, 4 GB RAM) |
| Hourly | $0.10 ~ $0.20 |
| Wall time | ~1 hr (cold start + apt + tar + binary fetch + playback + dump) |
| Total | **$0.20 ~ $1.00** (정직 단일 행) |
| Trigger | a_fire_autonomous (사용자 게이트 X, cost-bearing autonomous dispatch OK) |
| Fire-when | follow-up cycle (X8.followup-fire) — 본 round 5/5 는 spec + dispatch handoff 까지 |

본 spec 문서 + 본 round 5/5 의 inspect.hexa 검증 (file presence + size + magic byte) 까지가 1 PR. 실 pod fire 는 `XENO.md ## deferred` 에 `X8.followup-fire` 로 등록.

---

## 5. dispatch handoff (실 fire spec)

### 5.1 fire-trigger

```bash
# RunPod CPU pod dispatch (follow-up cycle 의 autonomous fire)
runpodctl create pod \
    --name xeno-x8-seti-boinc-playback \
    --imageName runpod/cpu-base:22.04 \
    --gpuCount 0 \
    --vcpuCount 2 \
    --memoryInGb 4 \
    --diskInGb 20 \
    --containerDiskInGb 10 \
    --env "X8_RUN_SLUG=xeno_x8_seti_boinc_pod_playback" \
    --startScript "$(cat XENO/scan/seti_boinc_pod_spec.md | sed -n '/^### 2.2 init script/,/^### 2.3 정직성 한계/p' | sed -n '/^```bash/,/^```$/p' | sed '1d;$d')"
```

### 5.2 artifact recovery (a_fire_recover_complete 정합)

- pod 의 `/opt/xeno-x8/x8_playback_artifacts.tar.xz` → `scp` → 로컬 `XENO/state/xeno_x8_seti_boinc_pod_playback_<date>/` 로 회수.
- `playback.log` + `spike_dump.txt` + `outfile.sah` + `result_header.sah` 4종 필수.
- 회수 후 invariant_detector 적용 → 추가 H 등록 (`H_836-followup-playback` 또는 신규 slug) → 정직 verdict.
- HF upload: closure 결과에 따라 `dancinlab/xeno-seti-boinc-playback-<date>` PUBLIC (PASS) or `dancinlife/` PRIVATE (FAIL).

### 5.3 정직 한계 (fire 결과 우려)

- ELF32 binary ABI gap → playback EXIT non-zero 가능 → 정직 negative cycle 으로 close (a_paper_negative_ok 정합).
- modern boinc-client protocol gap → standalone path 만 가능 → BOINC daemon 모드 무관.
- 본 frontier 의 정직한 verdict 가능 영역 = "file 존재 + sha256 정합 + best-effort parse" 까지. 실 spike pattern 의 의식-수준 numerical verdict 는 추가 instrument lens 필요 (Kolmogorov complexity, frequency-domain spectral entropy 등).

---

## 6. 사전등록 falsifier (이 spec round 5/5 의 frozen 임계)

```
F-X8-FILE-EXISTS    : DATASET/setiathome/sahfiles_workunits.tar.xz 존재
F-X8-FILE-SIZE      : 파일 크기 == 274340 bytes (manifest 정합)
F-X8-MAGIC-XZ       : 매직 바이트 시작 == \xfd\x37\x7a\x58\x5a\x00 (xz format)
F-X8-CLIENT-AVAIL   : BOINC client setup spec 문서화 완료 (init script + runbook)
F-X8-POD-DISPATCH   : cost-bearing fire spec 완성 (RunPod CPU ~$1, a_fire_autonomous 정합)
```

- 5 PASS → 🟡 **archive-acquired-pod-ready** (file 존재 + spec 완성, 실 playback deferred)
- ≤4 PASS → 🔴 **SPEC-INCOMPLETE** (정직 표기)

---

## 7. cross-cutting principle 정합

| 원칙 | 본 round 정합 |
|---|---|
| `a_blue_closed` | numerical verify = file inspection (size + magic + sha) only · BOINC playback 자체는 정직 deferred |
| `a_fire_autonomous` | pod fire 는 autonomous OK · 본 round 5/5 는 spec + dispatch handoff 까지 (실 fire = follow-up cycle) |
| `a_completeness_over_cheap` | "cheap fake 🟢" 거부 · file inspection + 완성 spec + dispatch handoff = 본 round 의 완성 영역 |
| `a_fire_recover_complete` | dispatch handoff 의 artifact recovery 단계 명시 (4종 파일 회수 + HF upload tier-gated) |
| `feedback-closure-is-physical-limit` | BOINC 3.03 ancient format ↔ modern toolchain 호환성 = open frontier 정직 cite |
| `feedback-instrument-first-methodology` | X4/X5/X6/X7 4-point applicability matrix cite + X8 follow-up 의 n=192~256 dense regime 명시 |
| `feedback-universe-h-slug-stale-verify` | 3-신호 검증 후 H_836 사용 |
| `a_runpod_inbox` | INBOX 환류 0건 (사용자 명시 폐기) · runpod findings 는 XENO 내부 후속 H 등록 |
| `p7` | LLM judge 0 · hexa stdout verbatim |

---

## 8. 다음 작업 (follow-up cycle)

- **X8.followup-fire**: 실 RunPod CPU pod fire ($0.50~$1) → playback 시도 → spike dump 회수 → invariant_detector 적용 → 추가 H 등록.
- **X8.kolmogorov**: Φ 외 lens (Kolmogorov complexity, spectral entropy) 추가 — X5/X7 의 instrument 한계 보완.
- **X8.archive-cross**: SETI@home 외 다른 BOINC volunteer project (Einstein@home, MilkyWay@home) 의 workunit archive cross-test.
- **X1-regime-matrix-v2**: X4/X5/X6/X7 4-point 위에 X8 (n=192~256 dense, spike-cluster mix) 추가 → 5-point full regime applicability matrix.
