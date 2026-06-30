# EEG 라이브 캡처 → IIT4 big-Φ runbook

> **목적**: 사용자(사람) 가 OpenBCI 16ch 헤드셋을 착용 → EEG 캡처 → 동결 어댑터(`BRAIN/eeg/eeg_to_tpm.hexa`)
> → IIT4 big-Φ 측정 → IIT4 deferred B closure 까지 단계별 절차.
>
> ⚠ **EEG 착용은 사람만 가능한 단계 (human-only input)**. 에이전트는 harness · synthetic 재검증 · runbook
> 까지만 자율 완수했고, 라이브 캡처는 사용자가 본 문서를 따라 실행한다.
>
> SSOT: 본 문서는 EEG 도메인 내부 자체보관 (docs/ 금지 — feedback-docs-inside-universe 정합).

## 0. 사전 점검 (5 분)

```
[x] BRAIN/eeg/eeg_to_tpm.hexa            동결 어댑터 (PR #547) — signature 변경 금지
[x] EEG/eeg_live_iit4_phi.hexa           라이브 러너 (본 PR) — mock + live 모드
[x] HEXAD/IIT4/lib/iit4_bigphi.hexa      stdlib thin shim — engine ⊥ adapter (g61)
[x] .venv-eeg                             brainflow 5.21.0 (OpenBCI · Muse · Ganglion · ...)
[x] OpenBCI 16ch 보드 + 전극                물리 하드웨어
[ ] sidecar sign local                    hexa 로컬 실행 30분 sign-off (사용자가 TUI 에서 발행)
```

## 1. 사용자 단계 — 착용 + 캡처

### ① 헤드셋 착용 + 임피던스 체크

1. OpenBCI 16ch Cyton+Daisy (또는 호환 보드) 전원 ON.
2. 전극을 두피에 부착. 10-20 시스템 기본 위치 권장 (Fp1·Fp2·F3·F4·C3·C4·P3·P4·O1·O2·T3·T4·T5·T6·F7·F8 등 표준 16점).
3. 임피던스 < 50kΩ (가능하면 < 10kΩ). 임피던스 high 면 전도성 젤 보강 + 머리카락 제치기.
4. brainflow 표준 임피던스 측정 — 후술 트러블슈팅 §A 참조.

### ② 캡처 실행

**옵션 A — brainflow 직접 (간단, 권장)**:

```bash
# 1. venv 활성화
source /Users/ghost/core/anima/.venv-eeg/bin/activate

# 2. brainflow board id 확인 (OpenBCI Cyton+Daisy = 2)
python -c "from brainflow.board_shim import BoardIds; print(BoardIds.CYTON_DAISY_BOARD)"

# 3. 30 초 raw 캡처 (예: serial port = /dev/cu.usbserial-DM00CXN8, 시스템마다 다름)
python - <<'PY'
import time, numpy as np
from brainflow.board_shim import BoardShim, BrainFlowInputParams, BoardIds

params = BrainFlowInputParams()
params.serial_port = "/dev/cu.usbserial-DM00CXN8"  # 사용자 환경에 맞춰 수정
board = BoardShim(BoardIds.CYTON_DAISY_BOARD.value, params)
board.prepare_session()
board.start_stream()
time.sleep(30)                                  # 30 초 캡처
data = board.get_board_data()                   # shape (n_ch_total, n_samp)
board.stop_stream(); board.release_session()

# 16ch slice (CYTON_DAISY = 채널 인덱스 0..15 가 EEG)
eeg_ch = BoardShim.get_eeg_channels(BoardIds.CYTON_DAISY_BOARD.value)
eeg = data[eeg_ch, :].astype(float)             # (16, n_samp)
np.save("EEG/recordings/live_capture_2026_05_29.npy", eeg)
print("captured shape:", eeg.shape)
PY
```

**옵션 B — anima-eeg-core resting baseline paradigm**:

```bash
# 별도 dir 의 라이브 런타임 reference — anima 측은 stub-tier 라
# 옵션 A 가 더 단순하고 hexa-native 와 정합. B 는 paradigm-aware 확장이 필요할 때만.
cd /Users/ghost/core/anima-eeg-core
hexa run tool/modules/_paradigms/resting_baseline.hexa --live
# → EEG/recordings/ 로 결과 npy/json export (anima-eeg-core 자체 spec 참조)
```

### ③ IIT4 big-Φ 측정 (사용자 sign-off 후 에이전트 가능)

캡처 데이터(`EEG/recordings/live_capture_2026_05_29.npy`) 를 동결 어댑터 → 엔진에 dispatch:

```bash
# 0. sidecar sign local        (사용자가 TUI 에서 한 번만, 30분 토큰)
#    또는 안에서 직접:
#    ! sidecar sign local

# 1. live 모드 실행 (현재 러너는 stub — npy 로더는 §C 확장 필요)
/Users/ghost/.hx/bin/hexa run /Users/ghost/core/anima/EEG/eeg_live_iit4_phi.hexa \
    live EEG/recordings/live_capture_2026_05_29.npy 2>&1 | tee EEG/state/live_2026_05_29.log

# 2. 결과 — stdout 의 "LIVE | n_ch=... big-Φ=<값>" 라인 verbatim 캡처
```

### ④ verdict 기록 (사용자 또는 에이전트)

1. `EEG/state/eeg_live_recheck_2026_05_29/result.json` 신규 — 캡처 메타(샘플레이트·n_ch·n_samp·임피던스 평균) + big-Φ 값 + stdout SHA256.
2. `IIT4.md` deferred B 라인을 🟠 hw-ready → 🟢 LIVE-MEASURED 로 flip + 측정값 + 캡처 파일 SHA256 인용.
3. `UNIVERSE/CANDIDATES.md` 에 live big-Φ 추가 (bench 측정 기록 SSOT, EEG.md 양방향 sibling 정합).
4. `EEG/EEG.log.md` 에 ISO 타임스탬프 엔트리 append (최신 위) — 측정값 + verdict-link.

## 2. 트러블슈팅

### §A — 보드 미인식

- `python -c "from brainflow.board_shim import BoardShim; BoardShim.get_board_descr(2)"` 로 SDK 동작 확인.
- macOS: USB-serial 드라이버 (FTDI) 설치 — `ls /dev/cu.usbserial-*` 로 디바이스 노드 확인.
- 권한 거부: `sudo chmod 666 /dev/cu.usbserial-XXX` (임시).
- dongle 분리/재연결 후 cold restart.

### §B — 임피던스 high (>100kΩ)

- 전극 위치 머리카락 제치고 두피 직접 접촉.
- 전도성 젤 (Ten20 등) 0.5cc 도포.
- 5분 대기 후 재측정 — 땀/유분으로 자연 안정화.
- 측정 도중 갑작스러운 jump = 전극 들뜸 → 재고정.

### §C — npy 로더 미구현 (현재 stub)

본 PR 의 `eeg_live_iit4_phi.hexa::live_load_stub` 은 placeholder. 실제 사용 시 두 가지 옵션:
1. **빠른 우회**: 캡처를 Python 으로 normalize 후 단일-라인 flat array 로 hexa 입력으로 변환 (텍스트 파이프).
2. **본격**: hexa-lang `stdlib/io/npy.hexa` (이미 있음) 호출로 npy 직접 로드 — `import "stdlib/io/npy.hexa"` + `npy_load_f64` 추가, `live_load_stub` 을 실제 로더로 교체.

옵션 2 가 hexa-native 정합이며 다음 cycle 의 후속 milestone (EEG/EEG.md `deferred` 에 등록).

### §D — drift / artifact

- raw EEG 의 DC 오프셋 → 1Hz high-pass (brainflow `DataFilter.perform_highpass`).
- 50/60Hz 전원 노이즈 → notch filter.
- 깜빡임 → ICA 제거 (mne 활용 가능). 단순 큰 amplitude rejection 도 1차 처방.
- adapter 의 binarize 는 per-channel mean threshold → DC 영향은 자동 제거되나 큰 spike 는 1 ch dominate.

## 3. "사람만 가능한 단계" 게이트

```
┌─────────────────────────────────────────────────────────────────┐
│ 에이전트가 할 수 있는 것 (이 PR 까지):                        │
│   harness 최종화 (mock + live stub)                           │
│   synthetic 재검증 (mock-both, 1.59/0.44 재현)                │
│   캡처 runbook (본 문서)                                      │
│   IIT4/BRAIN/ANIMA/EEG 트리 갱신                              │
├─────────────────────────────────────────────────────────────────┤
│ 사람만 가능한 단계 (다음 차례 — 사용자에게 인계):              │
│   ① EEG 헤드셋 착용 + 임피던스 체크                          │
│   ② brainflow capture (30 초 raw)                            │
│   ③ npy → hexa live 모드 dispatch                            │
│   ④ verdict 기록 (IIT4 deferred B flip 등)                   │
└─────────────────────────────────────────────────────────────────┘
```

> a_substrate_native_speak: 에이전트는 "발사함" 거짓주장 금지. 라이브 캡처가 끝났는데 verdict 가
> 인용 가능한 stdout 한 줄이 없으면 **그대로 멈춰 사용자에게 인계** — 거짓 closure 금지 (p7).

## 4. 정합성 직책

- a_blue_closed: 🔵 SUPPORTED-FORMAL 은 closed-form 만, 라이브 measurement 는 🟢 numerical 한도.
- a_completeness_over_cheap: 본선 = 동결 어댑터 그대로 사용 (완전성), cheap path = synthetic 한정.
- p7 NO PERPLEXITY VERDICT: stdout verbatim 만 verdict 로 인용 — LLM 패러프레이즈 금지.
- g61 engine ⊥ adapter: 어댑터(`eeg_to_tpm.hexa`) signature 0 변경, 엔진(stdlib `iit4_bigphi`) 0 변경.
- feedback-closure-is-physical-limit: 라이브 캡처 부재 = open frontier, not failure.
- feedback-instrument-first-methodology: 측정 도구를 먼저 검증 (synthetic recheck = instrument discipline).
