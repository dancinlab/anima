# Cyton 16ch first real session — board_health + brainflow_sanity (2026-05-03)


## 0. Goal

`anima-eeg/` 9-module Phase 4 wrapper 의 첫 실측 evidence 산출.
지금까지 모든 9 module 측 synthetic PASS only (real signal evidence = 0건).
본 cycle 에서 사용자 손으로 step 1-3 실행 → `recordings/sessions/first_real_2026_05_03.{npy,json}` 첫 실측 .npy
산출 + falsifier triad F_CTON_REAL_01/02/03 사후 검증.

Subagent BG 측 hardware 직접 run **불가** (사용자 USB dongle 접근 X).
따라서 본 doc 는 사용자 손 작업 sequence + 사후 audit harness spec only.

## 1. Pre-flight verified state (별도 BG 결과)

- USB dongle: `/dev/cu.usbserial-DP04WGIQ` 인식 OK
- Cyton 부팅 완료 (배터리 6.7V)
- FTDI latency patch: NOT_APPLIED (Apple Silicon DriverKit 경로, hexa 측 detect-only 가능)
- 9-module synthetic PASS verified, real evidence = 0건

## 2. 사용자 손 작업 sequence (copy-paste ready)

### Step 1 — FTDI latency detect-only

```
hexa run anima-eeg/eeg_ftdi_latency_fix.hexa --detect
```

- expected: detect report 출력 (DriverKit vs kext 경로 + 현재 LatencyTimer 값)
- 결정 trigger: 본 cycle 에서는 `--apply` 보류 (sudo 필요, 별도 cycle).
- failure mode (a): hexa fork limit / EAGAIN → 동일 command 즉시 retry
- failure mode (b): "no FTDI device" → dongle USB 재삽입, `ls /dev/cu.usbserial-*` 확인

### Step 2 — board_health_check (B1 gate)

```
hexa run anima-eeg/board_health_check.hexa --check --port /dev/cu.usbserial-DP04WGIQ --board cyton_daisy --seconds 5
```

- expected: dongle ↔ Cyton firmware ping success
- sentinel (success): `__EEG_BOARD_HEALTH__ PASS` (or per `board_health_check.hexa` 측 schema `anima-eeg/board_health/2`)
- failure mode (a): "no response from board" → Cyton 전원 스위치 OFF→ON, dongle GPIO 6 위치 확인 (PC mode)
- failure mode (b): "permission denied /dev/cu.usbserial-*" → `sudo chmod 666 /dev/cu.usbserial-DP04WGIQ` 또는 `dscl . -merge /Groups/_uucp GroupMembership $(whoami)` 후 재로그인
- failure mode (c): "board mode mismatch" → 8ch 만 사용 시 `--board cyton`, daisy module 부착 시 `--board cyton_daisy`
- recovery escalation: 3회 실패 시 step 2 중단 → audit BG 에 fail mode 보고 → 본 cycle 종료, 다음 cycle 재진입

### Step 3 — eeg_brainflow_sanity 5s capture (첫 실측 .npy)

```
hexa run anima-eeg/eeg_brainflow_sanity.hexa --port /dev/cu.usbserial-DP04WGIQ --board cyton_daisy --seconds 5 --tag first_real_2026_05_03
```

- expected:
  - sentinel: `__EEG_SANITY_RESULT__ PASS shape=16x1250 port=/dev/cu.usbserial-DP04WGIQ`
  - 산출물 (1): `anima-eeg/recordings/sessions/first_real_2026_05_03.npy` — 16ch × 1250 samples × float32 = **80128 bytes 정확**
  - 산출물 (2): `anima-eeg/recordings/sessions/first_real_2026_05_03.json` — `brainflow_used: true`, `board: "cyton_daisy"`, `sample_rate: 125.0` (daisy = 125Hz, cyton-only = 250Hz)
- failure mode: brainflow exit-non-zero → step 2 board_health 재실행 후 재시도
- 주의: daisy 부착 시 effective sample_rate = 125 Hz (8ch 250Hz 가 daisy interleave 로 16ch 125Hz 됨). 만약 .json 안 sample_rate=250 + n_samples=1250 이면 daisy 미인식 → `--board cyton` 으로 fallback 후 8ch capture.

### Step 4 — 사용자 손 마무리 trigger

step 3 sentinel PASS 확인 후 사용자가 BG audit harness launch (§4 참조).

## 3. Falsifier triad — F_CTON_REAL_01/02/03

formal spec, 사후 audit harness 측 PASS/FAIL emit.

### F_CTON_REAL_01 — synthetic 아님 증명
- predicate: `recordings/sessions/first_real_2026_05_03.json` 안 `brainflow_used == true` AND `board == "cyton_daisy"` (or `"cyton"` if daisy unavailable)
- FAIL 의미: synthetic Taylor mix fallback 사용됨 → BrainFlow lib 미설치 또는 board detect 실패
- emit: `__F_CTON_REAL_01__ <PASS|FAIL>`

### F_CTON_REAL_02 — byte-exact .npy size
- predicate: `recordings/sessions/first_real_2026_05_03.npy` size == **80128 bytes** (16ch × 1250 samples × 4 bytes float32 + .npy v1.0 header padding 적용 시 정확 80128)
- FAIL 의미: shape 불일치 (e.g. 8ch only, samples < 1250, dtype != float32) → board mode 또는 capture duration 문제
- emit: `__F_CTON_REAL_02__ <PASS|FAIL>`

### F_CTON_REAL_03 — 실 signal evidence (synthetic null 거부)
- predicate: `np.std(signal) > 0.1` AND `np.std(signal) != 1.0` (synthetic Taylor mix 측 std=1.0 정확, 실 signal 측 random std)
- AND per-channel power spectrum 측 60Hz spike 검출 (한국 220V 60Hz 전기 노이즈 — 전극 부착 시 강력 sign)
- FAIL 의미: signal flat (전극 미접촉 floating null) 또는 synthetic Taylor mix
- emit: `__F_CTON_REAL_03__ <PASS|FAIL>`

triad ALL PASS 시 첫 실측 .npy evidence 인정, eeg.cond.1 B2 gate 진입 가능.

## 4. 사후 audit harness — 사용자 launch instruction

step 1-3 완료 후 사용자가 본 cycle 종료 시 BG 1개 launch:

```
prompt: "anima-eeg cyton first real session audit — F_CTON_REAL_01/02/03 triad
verify (recordings/sessions/first_real_2026_05_03.{npy,json}) + per-channel
power spectrum 60Hz spike check + std sanity. spec doc:
anima-eeg/docs/cyton_first_real_session_2026_05_03.md §3.

agentId: <new>, run_in_background: true"
```

audit harness check sequence:
- check 1: file exist (`.npy` + `.json` both present in recordings/sessions/)
- check 2: F_CTON_REAL_01 — `.json brainflow_used == true`
- check 3: F_CTON_REAL_02 — `.npy` size == 80128 bytes
- check 4: F_CTON_REAL_03 — np.std(signal) > 0.1, std != 1.0
- check 5 (sanity): per-channel FFT, 55-65Hz bin power > average noise floor × 3 (60Hz line spike)
- check 6 (sanity): per-channel impedance proxy — DC offset + variance ratio (전극 contact quality, all 16 channels < 50 kΩ proxy)
- output verdict: triad PASS/FAIL + sanity summary, write to `state/eeg_cyton_first_real_audit_2026_05_03.json`


## 5. eeg.cond.1 B1-B4 4관문 매핑

본 cycle 진척:

| gate | desc | 본 cycle |
|------|------|---------|
| B1 | board_health_check exit-0 | step 2 PASS 시 → land |
| B2 | impedance < 50kΩ all 16 ch | step 3 .npy 측 impedance proxy (audit check 6) — 별도 `calibrate.hexa --impedance` cycle 권장 |
| B3 | collect.hexa byte-identical 2x | 본 cycle 측 1회만 capture, 별도 cycle 동일 command 2회 + sha256 hash 비교 |
| B4 | dual_stream pearson_r_phi_alpha null baseline | 본 cycle 측 X, 별도 cycle `dual_stream.hexa --port ... --board cyton_daisy --seconds N --null-baseline` |

다음 cycle (B3+B4 후속):
- cycle T+1: B3 byte-identical 2x — 동일 `--tag` 변경 (`first_real_2026_05_03_run2`) capture 후 sha256 .npy hash diff = 0 검증
- cycle T+2: B4 dual_stream — `dual_stream.hexa --board cyton_daisy --seconds 60 --null-baseline` 실행, pearson_r_phi_alpha 분포 측정 (null baseline 기준선 확보)

## 6. evidence append plan (다음 cycle, write conflict 방지)

본 cycle 측 .roadmap.eeg cond.1 evidence 배열 직접 append **X** (concurrent write 방지 — agentId a7b9e3dd5bb5acad8 와 race 위험).

다음 cycle 측 별도 BG 1개 spawn → audit harness 결과 (check 1-6 PASS 확인) 후 .roadmap.eeg cond.1 evidence 배열에 다음 4건 append:
- `anima-eeg/docs/cyton_first_real_session_2026_05_03.md` (본 doc, spec)
- `anima-eeg/recordings/sessions/first_real_2026_05_03.npy` (첫 실측 evidence, 80128 bytes)
- `anima-eeg/recordings/sessions/first_real_2026_05_03.json` (brainflow_used=true metadata)
- `state/eeg_cyton_first_real_audit_2026_05_03.json` (audit verdict, F_CTON_REAL_01/02/03 PASS log)

블록 시점 — concurrent write 방지를 위해 `state/worktree_merge_plan.json` 측 lock 확인 후 진입.


1. **Hardware run BG 직접 X** — subagent 측 사용자 USB dongle 접근 권한 X, 본 doc 측 사용자 손 작업 sequence + 사후 audit only. step 1-3 측 자동화 X, 사용자 의도적 실행 필요.

2. **60Hz line noise 한국 전기 노이즈 검출** — 한국 220V/60Hz, 미국 110V/60Hz, 유럽 220V/50Hz. 본 audit check 5 측 한국 전제 (60Hz). 만약 50Hz 환경 (e.g. 유럽 출장) 시 audit harness 측 `--line-freq 50` 인자 추가 필요. 측정 location 가정 명시 (한국 default).


## 8. 산출물

- 본 doc: `anima-eeg/docs/cyton_first_real_session_2026_05_03.md`
- 사용자 손 작업: §2 step 1-3 commands (copy-paste ready)
- falsifier triad: §3 F_CTON_REAL_01/02/03 formal spec
- audit harness: §4 instruction (사용자 launch trigger)
- 4관문 mapping: §5 B1-B4 진척 + 다음 cycle plan
- evidence append: §6 concurrent write 방지 plan
- C3 caveats: §7 3 honest disclosures
