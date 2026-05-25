# BrainFlow Cyton+Daisy Sample Drop / Packet Loss — Web Deep Research

date: 2026-05-03
scope: anima-eeg measurement layer
context: anima-eeg session 측정 결과 effective fs 가 meta `sample_rate=125Hz` 대비 33-94% drop (blink 60.5Hz / jaw 82.7Hz / berger_ec 38.4Hz / berger_eo **7.4Hz** / ppg 43.3Hz) — Nyquist violation 측 EMG/α band 측정 자체 위협. 본 문서는 community/vendor 측 known-cause + workaround 측 web deep-research 정리.


---

## 1. BrainFlow github issues — top-5

1. **#81 — Data not appearing at sampling rate** (CLOSED, 2020-08)
   - https://github.com/brainflow-dev/brainflow/issues/81
   - cyton+daisy serial 측 ring buffer 측 0.5s chunk 단위 도착
   - maintainer Andrey1994 fix: FTDI Buffer Fix (OS별 docs 안내)
   - reporter 측 "Runs much smoother now" 확인. **단 정확한 8ms tick 보장 X** ("It will not ensure exactly 8ms but data stream will be much smoother").

2. **#278 — Major packet loss when multicasting at high sample rates** (CLOSED, 2021-05)
   - https://github.com/brainflow-dev/brainflow/issues/278
   - Cyton WiFi 1000Hz multicast 측 70-90% loss
   - root cause: multicast streamer `sendto` 측 first-process serial read 측 block → buffer overflow
   - fix: streamer 측 별도 thread + buffering PR merge

3. **#763 — Playback sample rate issue (timestamp drift)** (CLOSED)
   - https://github.com/brainflow-dev/brainflow/issues/763
   - playback timestamp 측 wall-clock 측 drift — 본 anima-eeg 측 timestamp 측 PC-side 생성 (board side X) 측 confirmation.

4. **#804 — CYTON_WIFI_BOARD: `~5` config_board sample-rate change but `get_sampling_rate()` stays 1000** (CLOSED)
   - https://github.com/brainflow-dev/brainflow/issues/804
   - `~` 명령 측 WiFi shield only 측 actual SR 변경 가능하나 BrainFlow API 측 cached SR 측 stale → meta-vs-actual mismatch 위험 (본 anima-eeg 측 case 측 동일 패턴).

5. **#494 — Multiple internal buffers to store and provide data** (CLOSED)
   - https://github.com/brainflow-dev/brainflow/issues/494
   - BrainFlow 측 single ring-buffer architecture — 측정 process 측 GIL 측 idle 측 buffer overflow 측 silent drop 발생.

note: BrainFlow github 측 *"cyton daisy 125Hz drop"* 측 직접 issue X → 측 community 측 측정 자체 측 known-acceptable 처리 (vendor 측 "1% 이하 loss 측 OK" stance).

---

## 2. OpenBCI forum threads — top-5

1. **Packet Loss Analysis: Bug or Real Loss?** — https://openbci.com/forum/index.php?p=/discussion/4074
   - DashBarkHuss 측 5h recording 측 127-packet gap 측 885회 발견 → bimodal distribution 측 "numbering bug" 가능성 제기
   - vendor staff (William Croft): USB extension cord, EMF detector, dongle 측 원거리 배치 권장
   - 권장 원칙: **"aim for only a tiny / small amount of packet loss"** — fundamental 측 packet loss 측 software fix X.

2. **driver "Latency Timer" fix for macOS 11+ & M1 M2** — https://openbci.com/forum/index.php?p=/discussion/3108
   - macOS 11+ Apple Silicon 측 plist edit 측 X → `IOSSDATALAT` ioctl 측 1ms 설정
   - **"latency 측 device 측 unplug 시 default 16ms 측 reset"** caveat (재연결마다 재설정 필요)
   - BrainFlow 측 통합 진행 중 (vendor self-claim).

3. **Are there other ways to remove latency from Cyton in macOS?** — https://openbci.com/forum/index.php?p=/discussion/2782
   - FTDI driver 측 uninstall → board recognition 측 stable but latency 측 persist
   - vendor 권장: BrainFlow 측 buffering 활용 + macOS 측 Mojave/Catalina 이상 권장.

4. **Options for Cyton/Daisy Sampling Rate** — https://openbci.com/forum/index.php?p=/discussion/3304
   - **확정 인용**: "the Bluetooth streaming protocol limits you to 125 Hz when using Daisy"
   - SD card 측 250Hz 16ch 측정 가능 — 측 **on-board 저장 측 vendor 권장 fallback** (실시간 X).

5. **Cyton + Wifi, Packet Loss / Noise Issues** — https://openbci.com/forum/index.php?p=/discussion/3502
   - WiFi shield Daisy 측 99.22% loss 사례 — root cause: 16ch 측 single-board 모드 misconfig + 단일 4V 배터리 측 voltage dip
   - vendor fix: UDPx3 mode + dual 6V AA + 별도 배터리.

vendor stance summary: **"Cyton+Daisy 125Hz BLE 측 hardware fundamental limit, WiFi shield 측 unreliable, SD card 측 most-stable archival"**.

---

## 3. Vendor docs 측 핵심 인용

- BrainFlow `cyton_daisy.cpp` (master, github) — **"even sample IDs are the first sample (daisy) and odd sample IDs are the second sample (cyton)"**: 250Hz 두 board 측 alternating 합성 → 125Hz 1-row. **dropped-packet detection / recovery 코드 X** (단지 START_BYTE check만).
- BrainFlow timestamp logic: `package[timestamp_channel] = get_timestamp();` — combined package 1회만 PC-side 생성. **board hardware clock 측 측정 X**.
- OpenBCI Cyton Data Format 측: package_num 측 single byte (0-255 cyclic) — **256+ 연속 loss 측 1 loss 측 구분 불가**.
- "anything exceeding 1% packet loss produces non-meaningful recordings" — vendor staff 권장 threshold (forum thread #3984).

---

## 4. Community workaround top-5 (ranked by 완성도 / impact)

1. **macOS FTDI latency timer = 1ms** (`IOSSDATALAT` ioctl, M1/M2 측 필수)
   - 측 0.5s chunk 측 → ~125Hz 측 smooth stream 전환 (issue #81 confirmed)
   - cost: 코드 ~5 lines, 측 device 측 unplug 마다 재적용
2. **`start_stream(buffer_size=4500000)` (10x default 450k)**
   - polling 지연 측 buffer overflow 방지 — main thread 측 async loop 측 보호
3. **`get_current_board_data(chunk_size)` 측 chunked retrieve + tight polling loop (≤ 100ms interval)**
   - `get_board_data_count()` 측 sample count 측 monitoring → drop 측 즉시 alarm
4. **USB-A 측 hub 우회 직결 + USB extension cord 측 dongle 측 EMF source 측 거리 확보**
   - vendor 권장 (William Croft) — RFduino BLE 측 environmental fragile
5. **ECG/EMG/EEG 분리 측정 + 측정 paradigm 측 effective-SR 검증 측 metadata 측 actual_fs 기록 (vendor self-claim 측 cross-check)**

---

## 5. macOS-specific 측 fix

- macOS 11+ (Big Sur) ~ 15 (Sequoia): **built-in driver 사용** (third-party FTDI .kext 측 install 금지) — vendor 공식 `docs.openbci.com/Troubleshooting/FTDI_Fix_Mac/` confirmed.
- 기존 FTDIUSBSerialDriver.kext 측 `/Library/Extensions` + `/Library/StagedExtensions/Library/Extensions` 측 제거 후 reboot.
- Apple Silicon (M1/M2/M3): `IOSSDATALAT` ioctl 측 1ms 설정 — `unsigned long microseconds = 1ULL; ioctl(serialfd, IOSSDATALAT, &microseconds);` (값 0 측 "weird behavior" caveat).
- **device unplug 측 latency reset → 16ms default** → anima-eeg 측 session start 측마다 latency 재설정 필요 (코드 측 explicit 측 check).

---

## 6. Cyton-only 250Hz mode 측 활용 plan (Daisy 분리 측정)

Daisy 측 BLE bandwidth 측 fundamental bottleneck → **8ch only 측정 측 250Hz 측 streaming 측 보장**.

- anima-eeg paradigm별 활용:
  - `blink` / `jaw` (EMG, 측 ~30Hz band): 250Hz 측 ample headroom — Cyton-only 측 권장
  - `berger_eo` / `berger_ec` (α 8-13Hz): Nyquist 26Hz 만으로 충분 → 250Hz 측 측 Daisy 측 disconnect 측 권장
  - `ppg` (≤5Hz): 250Hz 측 over-spec, 측 8ch 측 충분
- 16ch 측 필요 paradigm (예: full helmet topography) 측만 Daisy 측 결합 → 측 effective 125Hz 측 acceptance.

**action**: anima-eeg 측 session config 측 `daisy_attached: bool` flag 측 추가, 측정 paradigm 측 channel-count requirement 측 cross-validate.

---

## 7. WiFi shield 측 500/1000Hz 측 비용/시간

- **vendor self-claim** (shop.openbci.com): WiFi shield 측 250/500/1000/2000/4000/8000Hz 가능, 1000Hz 16ch 측 "WiFi Direct mode" 측 zero-compression 가능
- **현실적 평가** (forum + brainflow #278): 1000Hz 측 **70-90% packet loss 사례 다수**, retiutut 측 staff 측 "I do not recommend using Cyton+Wifi" 명시 (forum #3446)
- 가격: vendor shop 측 **공개 가격 미확인** — sales@openbci.com 측 quote 필요 (~$200-400 USD 추정, 본문 검증 X)
- 시간: 주문 + 배송 + driver setup ~ 1-2주
- **권장도: LOW** — vendor staff 측 자체 권장 X, anima-eeg 측 우선순위 최하 deferred.

---


1. **vendor self-claim 측 검증 한계**: WiFi 1000Hz 16ch 측 "zero compression" 측 marketing claim 측, forum #3502 / #3446 측 community 측 99% loss + staff 측 자체 비권장 측 mismatch. anima-eeg 측 직접 검증 측 reproduction 필요.

2. **macOS 측 environment individual variance**: M1/M2/M3 측 각 chip-rev + macOS minor 측 USB serial latency 측 inconsistent — `IOSSDATALAT=1ms` 측 측 issue #3108 측 "Mojave/Monterey confirmed" 외 측 universal 보장 X. Apple Silicon 측 fresh install 측 retest 권장.

3. **Daisy 측 SPI bandwidth 측 fundamental limit**: BLE radio 측 250 packets/sec 측 hardware 측 cap (RFduino spec) — Cyton+Daisy 측 16ch 측 alternating multiplex 측 설계 자체 측 125Hz 측 **physical 측 ceiling**. 어떤 software workaround 측 250Hz 16ch streaming 측 달성 불가능 (SD card 측 archive only).

---

## 9. 다음 cycle 코드 fix priority (ranked)

| rank | fix | impact | effort | 완성도 lens |
|---|---|---|---|---|
| **1** | macOS `IOSSDATALAT=1ms` ioctl 측 session start 마다 explicit 적용 | 33-94% drop → ≤5% drop 가능성 가장 높음 | ~10 LOC | session-start hook 측 추가 |
| **2** | `start_stream(buffer_size=4_500_000)` + polling loop 측 ≤50ms tight | buffer overflow 측 silent drop 방지 | ~5 LOC | config 측 default 측 변경 |
| **3** | `package_num` 측 missing-sample detection + actual_fs metadata 기록 (vendor self-claim 측 vs 측 effective fs cross-check) | 측정 후 alarm + paradigm 측 reject criteria | ~30 LOC | data-quality C3 측 explicit |
| **4** | paradigm별 `daisy_attached` toggle — 8ch 측 충분 측 paradigm 측 Cyton-only 250Hz 측 fallback | berger / blink / jaw / ppg 측 Nyquist headroom 회복 | ~20 LOC + hardware re-wiring | session config 측 schema 변경 |
| **5** | session start 측 30s warm-up 측 effective fs 측정 → meta vs actual gap > 10% 측 abort + user prompt | data 무결성 측 fail-fast | ~15 LOC | quickstart runbook 측 측 step 추가 |
| **6** (deferred) | WiFi shield 측 평가 측 reproduction | upper-bound 검증 | $200-400 + 1-2주 | priority LOW (vendor 자체 비권장) |

priority 1+2 측 측 다음 cycle 측 immediate landing 권장. priority 3 측 측 metadata schema 변경 측 cross-cycle 영향 — 측정 paradigm runbook 측 동기 update 필요.

---

## sources

- BrainFlow github: https://github.com/brainflow-dev/brainflow
  - issue #81, #278, #763, #804, #494 (위 본문)
  - cyton_daisy.cpp: https://github.com/brainflow-dev/brainflow/blob/master/src/board_controller/openbci/cyton_daisy.cpp
- BrainFlow docs: https://brainflow.readthedocs.io/en/stable/UserAPI.html
- OpenBCI forum threads (위 본문 #1-#5)
- OpenBCI docs:
  - https://docs.openbci.com/Troubleshooting/FTDI_Fix_Mac/
  - https://docs.openbci.com/Cyton/CytonDataFormat/
- BCI2000 OpenBCI module: https://www.bci2000.org/mediawiki/index.php/Contributions:OpenBCI_Module

word-count: ~770 (Output 본문)
