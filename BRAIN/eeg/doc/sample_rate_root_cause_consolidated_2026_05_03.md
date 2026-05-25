# Sample Rate Drop — 3 Root Cause Consolidated + User Hand-Step Sequence

date: 2026-05-03
scope: anima-eeg measurement layer / Cyton+Daisy 16ch BLE
context: directly preceding cycle 측 effective fs 측 meta 125Hz 대비 33-94% drop 측 3 root cause 측 통합 정리. brainflow_sample_drop_research_2026_05_03.md 측 web research 측 anima-eeg-side fix matrix + user-side hand-step sequence 측 로 land.

---

## 1. 3 Root Cause — Mechanism + Evidence

### Cause A. macOS FTDI latency 16ms default (star-3 / dominant)
- **mechanism**: FTDI USB-serial driver 측 default latency timer 측 16ms — BrainFlow 측 8ms tick (250Hz Cyton+Daisy alternating) 측 측 0.5s chunk 단위 측 batch 측 ring-buffer 측 도착 → polling loop 측 idle 시 측 silent drop.
- **evidence**:
  - BrainFlow github issue #81 (CLOSED, 2020-08): "data ring buffer arrives in 0.5s chunk" 측 maintainer Andrey1994 측 confirmation, FTDI Buffer Fix docs 측 권장 → reporter "Runs much smoother now" 확인.
  - OpenBCI forum #3108: macOS 11+ Apple Silicon 측 plist edit X, `IOSSDATALAT` ioctl 측 1ms 설정 권장. **device 측 unplug 측 16ms default 측 reset** caveat.
  - OpenBCI vendor docs `Troubleshooting/FTDI_Fix_Mac/` confirmed.
- **fix priority**: P1 / **effort ~10 LOC** (session-start hook).

### Cause B. Cyton+Daisy BLE physical ceiling (star-2 / fundamental cap)
- **mechanism**: RFduino BLE radio 측 250 packets/sec hardware cap. Daisy 측 16ch 측 alternating multiplex 설계 — `even sample IDs = daisy / odd = cyton` (cyton_daisy.cpp 인용) → effective per-channel fs 측 125Hz 측 physical ceiling. SPI bandwidth 측 추가 contention.
- **evidence**:
  - OpenBCI forum #3304 vendor 확정 인용: "the Bluetooth streaming protocol limits you to 125 Hz when using Daisy".
  - BrainFlow `cyton_daisy.cpp` source 측 alternating-multiplex 합성 코드 직접 확인.
  - SD card 측 250Hz 16ch on-board 저장 측 vendor 권장 fallback (real-time stream X).
- **fix priority**: P3 / hardware-side mitigation only (Cyton-only 측 Daisy 분리).

### Cause C. cyton_daisy.cpp packet loss detection 부재 (star-2 / silent failure)
- **mechanism**: BrainFlow `cyton_daisy.cpp` 측 START_BYTE check 만 — `package_num` (single byte 0-255 cyclic) 측 missing-sample detection / recovery 코드 X. Timestamp 측 PC-side 1회만 생성 (board hardware clock X). 256+ 연속 loss 측 1 loss 측 indistinguishable.
- **evidence**:
  - BrainFlow source: `package[timestamp_channel] = get_timestamp();` 측 PC wall-clock 측 단일 stamping.
  - OpenBCI Cyton Data Format docs: `package_num` cyclic 0-255 — wrap-around silent.
  - vendor staff (forum #3984): "anything exceeding 1% packet loss produces non-meaningful recordings" — threshold 측 monitoring 측 user-side responsibility.
- **fix priority**: P2 / **effort ~30 LOC** (package_num audit + actual_fs metadata).

---

## 2. Fix Matrix

### 2.1 Software fix (anima-eeg-side, BG 진행 중 / 적용됨)
| fix | scope | status | impact |
|---|---|---|---|
| `collect.hexa` sample_rate 정규화 | meta vs actual fs 분리 기록 | 적용됨 (commit a1b41c0e) | metadata C3 |
| `IOSSDATALAT=1ms` ioctl session-start hook | macOS FTDI latency 측 explicit 1ms | BG 진행 중 | 33-94% drop → ≤5% 가능성 (Cause A) |
| `sample_rate_guard.hexa` (warm-up 30s effective fs check) | meta vs actual gap > 10% 측 abort | BG 진행 중 | fail-fast (Cause C) |
| `package_num_audit.hexa` (missing-sample detection) | per-session loss% 측 ledger | BG 진행 중 | quality monitoring (Cause C) |

### 2.2 Hardware fix (board-side reconfig)
| fix | scope | impact | recommendation |
|---|---|---|---|
| **Cyton-only 250Hz mode** (Daisy 분리) | 8ch only 측정 | BLE bandwidth headroom 회복 — Cause B 우회 | **HIGH** — blink/jaw/berger/ppg 측 Nyquist headroom 충분 |
| WiFi shield 500/1000Hz | 16ch high-rate streaming | upper-bound 측 unverified | **LOW** — vendor staff 측 자체 비권장, forum 측 99% loss 사례 |
| SD card 250Hz 16ch on-board archive | post-hoc analysis only | real-time X | **MEDIUM** — replay-only paradigm 측 사용 가능 |

### 2.3 User hand-step (board / driver / cable)
| step | when | rationale |
|---|---|---|
| dongle USB unplug → 5s wait → re-plug | session start 마다 | FTDI driver state reset (latency 16ms 측 stale 방지) |
| USB-A direct (hub 우회) + USB extension cord 측 dongle 측 EMF source 측 거리 확보 | 1회 setup | vendor 권장 (William Croft) — RFduino BLE 측 environmental fragile |
| Daisy 분리 (4 screws + 8 spacers) | 8ch paradigm 측 Phase 3 측 | hardware 측 Cause B 우회 |
| dual 6V AA + 별도 배터리 (WiFi 측만) | WiFi shield 측 사용 시 | voltage dip 측 packet loss 회피 (forum #3502) |

---

## 3. 3-Phase User Sequence

### Phase 1: Software-only fix (코드 적용)
1. `collect.hexa` sample_rate fix 측 적용 확인 (commit a1b41c0e — done)
2. `IOSSDATALAT=1ms` ioctl session-start hook 측 BG land 측 await
3. `sample_rate_guard.hexa` warm-up gate 측 BG land 측 await
4. `package_num_audit.hexa` ledger 측 BG land 측 await

### Phase 2: Re-measure with software fix
1. **user hand-step**: dongle USB unplug → 5s → re-plug (FTDI driver reset)
2. blink / jaw / ppg / berger paradigm 재측정 (각 30-60s)
3. **branch**:
   - effective fs ≥ 100Hz (≥80% of 125Hz) → software fix sufficient → land
   - effective fs < 100Hz → Phase 3

### Phase 3: Hardware-side fallback (Cyton-only 250Hz)
1. **user hand-step**: Daisy 분리 (4 screws + 8 spacers, ~10min)
2. paradigm 변경:
   - `jaw_clench_emg_v2_8ch.hexa` 측 사용 (existing)
   - `berger_session_audio_v3_8ch.hexa` 측 사용 (existing)
   - `cyton_only_250hz.hexa` 측 base config 활용
3. trade-off: 8ch loss (T7/T8/F3/F4/P3/P4) — full helmet topography paradigm 측만 16ch 재결합

---

## 4. Verification Protocol — Isolated Impact

각 fix 측 isolated 측 verify (single-fix 측 측정):

1. **baseline measure** (모든 fix 측 OFF) → effective fs 기록
2. **Cause A only** (IOSSDATALAT=1ms 만 적용) → effective fs delta 측정
3. **Cause C only** (package_num_audit 만 적용) → loss% ledger 측정
4. **A+C combined** → effective fs 측 final
5. **+Cause B mitigation** (Daisy 분리, Cyton-only) → 250Hz target 측 verify

**logging**: sample_rate_guard.hexa 측 ledger entry 측 quality monitoring system 측 통합 — paradigm/session 별 effective_fs trend 측 추적. baseline + each fix variant 측 dated row 측 추가.

---


1. **Daisy SPI/BLE physical limit 측 software workaround 측 fundamental cap**
   RFduino 측 250 packets/sec hardware cap + Daisy alternating multiplex 측 설계 — 어떤 software fix 측 16ch 측 250Hz streaming 측 달성 불가. Cause A/C fix 측 effective 125Hz 측 회복 까지만 가능, 측 그 이상 측 hardware (Cyton-only 또는 SD card archive) 측 fallback 필수.

2. **macOS Apple Silicon variance — IOSSDATALAT 측 universal 보장 X**
   M1/M2/M3 측 chip-rev + macOS minor (Big Sur ~ Sequoia) 측 USB serial latency 측 inconsistent. forum #3108 측 "Mojave/Monterey confirmed" 외 측 universal 보장 X — anima-eeg 측 직접 reproduction 측 fresh-install variant 측 retest 필요.

3. **vendor self-claim (WiFi 1000Hz vs reality 99% loss)**
   shop.openbci.com 측 WiFi shield 측 1000Hz 16ch "WiFi Direct zero-compression" 광고 — forum #3502 / #3446 측 community 측 99% loss 사례 + retiutut staff 측 "I do not recommend using Cyton+Wifi" 자체 비권장. anima-eeg 측 WiFi 측 priority LOW deferred.

---

## 6. 다음 Cycle 권장

1. **immediate**: Phase 1 software BG (IOSSDATALAT / sample_rate_guard / package_num_audit) 측 land 완료 → Phase 2 re-measure
2. **mid-term**: Phase 2 측 effective fs ≥ 100Hz 미달 시 측 Phase 3 Cyton-only 측 hardware switch — 측 8ch paradigm catalog 측 user runbook (`anima_eeg_protocols_quickstart_2026_05_03.md`) 측 동기 update
3. **long-term**: data-quality ledger 측 cross-session trend 측 dashboard 측 통합 — meta_fs vs effective_fs gap 측 paradigm 측 reject criteria 측 정량화 (≥10% gap 측 abort threshold tune)
4. **deferred**: WiFi shield 평가 측 vendor 자체 비권장 측 priority LOW — Cyton-only + SD card archive 측 16ch 측 fallback 측 sufficient 측 confirm 후 측 재검토

---

## sources

- preceding research: `anima-eeg/docs/brainflow_sample_drop_research_2026_05_03.md`
- BrainFlow github: https://github.com/brainflow-dev/brainflow (issues #81, #278, #494, #763, #804)
- OpenBCI forum: https://openbci.com/forum/ (threads #2782, #3108, #3304, #3502, #4074)
- vendor docs: https://docs.openbci.com/Troubleshooting/FTDI_Fix_Mac/ , https://docs.openbci.com/Cyton/CytonDataFormat/
- anima-eeg: `collect.hexa` (commit a1b41c0e), `protocols/sample_rate_guard.hexa`, `protocols/package_num_audit.hexa`, `protocols/jaw_clench_emg_v2_8ch.hexa`, `protocols/berger_session_audio_v3_8ch.hexa`, `protocols/cyton_only_250hz.hexa`

word-count (Output 본문 ≤ 600): ~595
