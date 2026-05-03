# Cyton firmware 'v' soft-reset escalation — hardware-touching modules (2026-05-03)

raw#9 hexa-only · raw#10 honest C3 · raw#11 snake_case · raw#15 no-personal-paths · raw#37 transient-helper · raw#65 idempotent · raw#80 sentinel

## 0. Purpose

OpenBCI Cyton firmware `'v'` 명령은 board-side **soft reset** (ADS1299 + LIS3DH + daisy 재초기화 + EOT `$$$`). 사용자 토글 (Cyton 전원 OFF→PC) 없이 board 측 fresh state 복귀 가능. 본 spec 은 모든 hardware-touching `anima-eeg/*.hexa` 모듈의 transient helper python 안에 **inline-embed** 형태로 `cyton_soft_reset(port)` + `prepare_session_with_recovery()` wrapper 를 정의한다.

목적: `_is_leak()` 검출 시 자동 `'v'` 송신 → `$$$` poll → BrainFlow re-prepare. 사용자 손 토글 영구 제거 (RFduino dongle 살아있을 때).

## 1. 직전 BG audit 결과 (cyton firmware audit)

- Cyton firmware `'v'` = soft reset (ADS1299 + LIS3DH + daisy 재초기화 + EOT `$$$`)
- timing: `'s'` (stop) 100ms → `'v'` (firmware 측 500ms 내부 reset) → `$$$` poll ≤1.5s → 200ms 안정화 → BrainFlow `prepare_session()`
- 'V' (대문자) = firmware version probe → `'v3.x.x$$$'` (dongle alive health check)
- 'C' = channel count query → `'8$$$'` (cyton-only) or `'16$$$'` (daisy attached)

**제한 (raw#10 honest C3 #1)**: RFduino dongle 살아있어야 'v' 도달. dongle ↔ Cyton pair 자체 stuck 시 사용자 토글 필요 (escalation step 3).

## 2. Helper inline-embed 패턴 — **결정: inline-embed**

raw#37 transient helper 측 inline-embed 채택 (공통 helper module 신설 X). 근거:
1. 모든 hardware-touching 모듈이 이미 `_write_helper()` 안 raw#37 transient python 을 emit. 추가 import-import 사슬 X.
2. 공통 helper 신설 시 module 간 import dependency + raw#9 hexa-only 침범 위험 (python helper 가 다른 python helper 를 import 하는 anti-pattern).
3. 6 module × 30 lines ≈ 180 line 중복; trade-off 측 maintenance overhead < dependency complexity.

## 3. inline-embed 표준 코드 (raw#9-호환 transient python)

helper python 안 BrainFlow import 직후 + `params` setup 직전 위치에 다음 함수 block 을 push:

```python
# ---- Cyton firmware 'v' soft-reset escalation (raw#10 honest C3) ----
import serial, time as _time

def cyton_soft_reset(port: str, baud: int = 115200, timeout_s: float = 1.5) -> bool:
    """Send 's' (stop) + 'v' (soft reset) to Cyton firmware via dongle.
    Returns True if '$$$' EOT seen within timeout_s, False otherwise.
    Requires RFduino dongle alive — if dongle/Cyton pair stuck, user power toggle needed.
    """
    try:
        with serial.Serial(port, baud, timeout=0.5) as ser:
            ser.write(b's'); _time.sleep(0.1); ser.reset_input_buffer()
            ser.write(b'v')
            deadline = _time.time() + timeout_s
            buf = b''
            while _time.time() < deadline:
                chunk = ser.read(64)
                if chunk:
                    buf += chunk
                    if b'$$$' in buf:
                        _time.sleep(0.2)  # post-reset stabilization
                        return True
            return False
    except Exception:
        return False

def cyton_dongle_alive(port: str, baud: int = 115200, timeout_s: float = 1.0) -> bool:
    """Send 'V' (firmware version probe). Returns True if 'v...$$$' received.
    If False, dongle is dead — soft-reset will not work, user must power-cycle."""
    try:
        with serial.Serial(port, baud, timeout=0.5) as ser:
            ser.reset_input_buffer()
            ser.write(b'V')
            deadline = _time.time() + timeout_s
            buf = b''
            while _time.time() < deadline:
                chunk = ser.read(64)
                if chunk:
                    buf += chunk
                    if b'$$$' in buf:
                        return True
            return False
    except Exception:
        return False

def cyton_daisy_attached(port: str, baud: int = 115200, timeout_s: float = 1.0) -> bool:
    """Send 'C' (channel count). Returns True if '16$$$' (daisy seated).
    False if '8$$$' (cyton-only) or no response."""
    try:
        with serial.Serial(port, baud, timeout=0.5) as ser:
            ser.reset_input_buffer()
            ser.write(b'C')
            deadline = _time.time() + timeout_s
            buf = b''
            while _time.time() < deadline:
                chunk = ser.read(64)
                if chunk:
                    buf += chunk
                    if b'16$$$' in buf:
                        return True
                    if b'8$$$' in buf:
                        return False
            return False
    except Exception:
        return False
# ---- end Cyton firmware soft-reset block ----
```

## 4. 기존 leak-retry escalation 통합

기존 모든 module 측 `_is_leak()` 검출 후 BrainFlow `release_all_sessions()` + `time.sleep(2)` 만 수행. 본 spec 측 추가 escalation:

```python
# Existing: Retry-once on leaked-session error during prepare_session
try:
    board.prepare_session()
except Exception as _e1:
    if _is_leak(_e1):
        try: BoardShim.release_all_sessions()
        except Exception: pass
        time.sleep(0.5)
        # NEW: Cyton firmware 'v' soft-reset escalation (no user toggle needed)
        try:
            if cyton_soft_reset(PORT):
                sys.stderr.write('cyton_soft_reset=ok\n')
            else:
                sys.stderr.write('cyton_soft_reset=fail (dongle dead?)\n')
        except Exception:
            pass
        time.sleep(0.5)
        board = BoardShim(BOARD_ID, params)
        board.prepare_session()
    else:
        raise
```

start_stream 측 동일 pattern (release_session → release_all_sessions → cyton_soft_reset → fresh prepare → start_stream).

## 5. prepare_session_with_recovery() wrapper (max_retry=3)

raw#9 hexa-only constraint 측 별도 wrapper 함수 X — 기존 try/except retry-once pattern 을 retry-twice (max 3 attempts) 로 확장:

```python
def prepare_with_recovery(board_factory, port, max_retry=3):
    for attempt in range(max_retry):
        try:
            b = board_factory()
            b.prepare_session()
            return b
        except Exception as _e:
            if attempt + 1 >= max_retry: raise
            if not _is_leak(_e): raise
            try: BoardShim.release_all_sessions()
            except Exception: pass
            time.sleep(0.5)
            try: cyton_soft_reset(port)
            except Exception: pass
            time.sleep(0.5 + attempt * 0.5)  # backoff
    raise RuntimeError('prepare_with_recovery exhausted')
```

## 6. 사용자 토글 escalation tier (raw#10 honest C3)

soft-reset attempts exhausted 시 Korean stderr message:

```
reason: cyton-soft-reset-exhausted: 'v' 명령 3회 재시도 실패 — RFduino dongle 또는 Cyton firmware stuck
fix: 1) Cyton 전원 OFF→PC 토글  2) dongle GPIO 6 위치 확인  3) USB 재삽입  4) 재시도
```

## 7. 'V' 시작 시 health probe (best-effort)

helper main entry 측 capture/collect 시작 직전 1회:

```python
if not cyton_dongle_alive(port):
    emit_trailer('cyton-dongle-dead',
                 "'V' firmware probe 응답 없음 — dongle 또는 board 측 stuck",
                 '1) Cyton 전원 OFF→PC  2) dongle USB 재삽입  3) 재시도')
    sys.exit(2)
```

## 8. Daisy 16ch 검증 (cyton_daisy board 한정)

```python
if BOARD_ID == 2:  # CYTON_DAISY_BOARD
    if not cyton_daisy_attached(port):
        sys.stderr.write('warn: daisy not detected ("C" returned 8$$$ or no response)\n')
        # do not exit — let BrainFlow shape mismatch surface explicit error
```

## 9. 적용 대상 + write race avoidance

| 모듈 | 파일 경로 | 본 cycle 적용 | 근거 |
|------|-----------|---------------|------|
| collect | `anima-eeg/collect.hexa` | **SKIP** | NameError BG (agentId 별) 측 동시 write 진행중 (mtime 14:55:19, others 14:45-14:46) |
| eeg_brainflow_sanity | `anima-eeg/eeg_brainflow_sanity.hexa` | **APPLY (priority)** | race-free, user 손 첫 실측 (cyton_first_real_session_2026_05_03.md §2 step 3) |
| calibrate | `anima-eeg/calibrate.hexa` | **APPLY** | race-free, mtime 14:45:50 |
| realtime | `anima-eeg/realtime.hexa` | **APPLY** | race-free, mtime 14:46:20 |
| eeg_recorder | `anima-eeg/eeg_recorder.hexa` | **APPLY** | race-free, mtime 14:46:45 |

**collect.hexa**: NameError BG fix land 후 다음 cycle 통합 BG 측 동일 pattern 적용 권장.

## 10. selftest 회귀 verify

각 모듈 측 `--selftest` synthetic path 측 hardware touch X → cyton_soft_reset 호출 X → 회귀 위험 0.

회귀 verify command (race-free 4 modules):

```
hexa run anima-eeg/eeg_brainflow_sanity.hexa --selftest
hexa run anima-eeg/calibrate.hexa --selftest
hexa run anima-eeg/realtime.hexa --selftest
hexa run anima-eeg/eeg_recorder.hexa --selftest
```

각 expected: `selftest=ok` + `verdict=PASS`.

## 11. 사용자 즉시 재시도 시나리오

soft-reset land 후 사용자 측 다음 sequence 가능:

```
hexa run anima-eeg/eeg_brainflow_sanity.hexa --port /dev/cu.usbserial-DP04WGIQ --board cyton_daisy --seconds 5
```

leak error 발생 시 자동으로:
1. `release_all_sessions()` 호출
2. `cyton_soft_reset()` → `'s'` + `'v'` + `$$$` poll
3. fresh `prepare_session()` + `start_stream()` 재시도
4. 통과 시 `__EEG_SANITY_RESULT__ PASS shape=32x625 port=...` 사용자 토글 불필요

PASS 시 `recordings/sessions/first_real_2026_05_03.{npy,json}` 생성 가능 (`cyton_first_real_session_2026_05_03.md` §3 falsifier triad audit 가능).

## 12. 3 honest C3 caveats (raw#10)

1. **Dongle dead 시 soft-reset 무익** — RFduino dongle 자체 stuck (ENXIO 또는 데이터 송수신 불가) 시 `'v'` 명령 도달 X. cyton_dongle_alive() 'V' probe 측 해당 case 검출 → 사용자 토글 안내 (한국어 stderr).

2. **Serial port lock contention** — BrainFlow 측 prepare_session 이 port 점유한 상태에서 `cyton_soft_reset(port)` 호출 시 OS-level port-busy. 따라서 본 spec 측 `BoardShim.release_all_sessions()` **선행**, 그 다음 cyton_soft_reset 호출 sequence 강제.

3. **'C' daisy probe 측 board mode 가정** — Cyton firmware 측 `'C'` 명령 응답 spec 은 firmware version 별 차이 가능 (legacy `8` vs `16` plain text vs `'$$$'` 포함 여부). 본 spec 은 OpenBCI v3.1.2 firmware 기준 (`16$$$` / `8$$$`). 다른 firmware version 측 응답 mismatch 시 daisy probe 가 false-negative 가능 → BrainFlow shape mismatch 단계에서 explicit error surface 됨 (silent fail X, raw#12 준수).

## 13. 다음 cycle 권장

1. NameError BG land 후 collect.hexa 측 동일 inline-embed 적용 (별도 BG, race-free).
2. board_health_check.hexa 측 `--check` path 에 'V' health probe + 'C' daisy probe 통합 (separate BG, B1 gate 강화).
3. 사용자 손 first-real session 재시도 → cyton_first_real_session_2026_05_03.md §2 step 3 PASS 검증 (사용자 토글 0회 목표).
4. F_CTON_REAL_01/02/03 falsifier triad audit BG land (read-only verification, write-conflict X).

## 14. 산출물

- 본 spec doc: `anima-eeg/docs/cyton_soft_reset_v_command_spec_2026_05_03.md`
- 적용 대상 (race-free 4 module): eeg_brainflow_sanity.hexa, calibrate.hexa, realtime.hexa, eeg_recorder.hexa
- 적용 보류 (race avoid): collect.hexa (NameError BG ownership)
