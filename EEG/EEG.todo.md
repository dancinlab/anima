# 🧠 EEG — 사용자가 해야 할 일 (TODO)

> **이 문서 = 사람만 할 수 있는 단계 모음.** 에이전트는 SW 구현·검증·UNIVERSE 등록 다 끝냈고, **딱 한 가지** 남았습니다:
> 사용자가 EEG 헤드셋 착용하고 4번 명령 실행 → IIT4 deferred B 완전 닫힘.
>
> 정식 진행 표 → [EEG.md](./EEG.md) · 친근 카탈로그 → [EEG.easy.md](./EEG.easy.md) · 캡처 절차 상세 → [EEG_CAPTURE_RUNBOOK.md](./EEG_CAPTURE_RUNBOOK.md)

---

## 한눈에 — 지금 상태

```
🧠 EEG — "음식점 셋업 끝, 손님(사용자) 한 분만 오시면 됨"

- SW 검증     ✅ 4/4 🟢 (PR #1375 머지됨)
- HW 검증     ☐ 사용자 헤드셋 착용 + 30초 캡처 필요
- 보상       → IIT4 deferred B 최종 closure + 3-substrate Φ 삼각측정 완결
```

```
       에이전트 끝난 일                사용자 1회 단계               결과
  ┌────────────────────────┐    ┌────────────────────────┐    ┌────────────────┐
  │ 4 H_xxx 구현 ✅          │    │ 헤드셋 착용             │    │ 🟡 → 🟢 격상     │
  │ SW path 4/4 PASS ✅      │ →  │ 30초 capture           │ →  │ IIT4 B CLOSED  │
  │ UNIVERSE H_679~682 ✅    │    │ hexa run × 4           │    │ 3-substrate 완성│
  │ HANDOFF.md ✅            │    │ (총 ~10분)              │    │                │
  └────────────────────────┘    └────────────────────────┘    └────────────────┘
```

---

## 준비물 (1회)

| 필요한 것 | 메모 |
|---|---|
| EEG 헤드셋 | OpenBCI · Muse · Ganglion 등 brainflow 5.21.0 지원 보드 (`.venv-eeg` 설치 완료) |
| 보드 ID | brainflow 보드 번호 (예: OpenBCI Cyton = 0, Muse 2 = 22 등) — 보드 매뉴얼 참조 |
| 임피던스 < 50kΩ | 젤/식염수로 전극 접촉 좋게 (보드별 LED·앱 확인) |
| 조용한 환경 30초 | 눈감고 rest state 캡처 권장 |

---

## 단계 (4-step · ~10분)

### ① sentinel 파일 만들기 (사용자 sign-off 토큰)

```bash
mkdir -p ~/.config/anima
touch ~/.config/anima/eeg_headset_ready
```

> 이 파일이 있어야 `eeg_hw_reachable()`가 true 반환. **헤드셋 실제 착용 + 캡처 완료 후에만** 만드세요 (거짓 PASS 방지 게이트).

---

### ② 헤드셋 착용 + brainflow 30초 캡처

상세 절차 → [EEG_CAPTURE_RUNBOOK.md](./EEG_CAPTURE_RUNBOOK.md) §1~§4.

요약:
- 헤드셋 착용 → 임피던스 체크 (< 50kΩ)
- 30초 resting baseline 캡처 (눈감고 안정 상태)
- 결과 `.npy` (또는 `.csv`) 저장 → 경로 기억

옵션 A — brainflow 직접:
```bash
# (보드 id · 경로는 본인 보드에 맞게)
python -c "
import brainflow, numpy as np, time
from brainflow.board_shim import BoardShim, BrainFlowInputParams
params = BrainFlowInputParams()
b = BoardShim(0, params)  # 보드 id 교체
b.prepare_session(); b.start_stream(); time.sleep(30); b.stop_stream()
data = b.get_board_data(); b.release_session()
np.save('/tmp/eeg_capture.npy', data)
print('saved /tmp/eeg_capture.npy', data.shape)
"
```

옵션 B — anima-eeg-core paradigm (별도 dir):
```bash
hexa run ~/core/anima-eeg-core/tool/modules/_paradigms/resting_baseline.hexa --live
```

---

### ③ HW path 실행 — 4 H_xxx 순차

```bash
cd ~/core/anima

# (필요 시) sidecar local-sign 토큰 30분 발행
! sidecar sign local

# 4 H_xxx HW path 실행
hexa run EEG/impl/H_679_measurement_core.hexa hw
hexa run EEG/impl/H_680_cross_substrate.hexa hw
hexa run EEG/impl/H_681_emit_substrate.hexa hw
hexa run EEG/impl/H_682_persistence_paradigm.hexa hw
```

각 명령 stdout 의 verdict 줄(`🟢 GREEN_*` 또는 `🔴 FAIL_*`)을 그대로 보고해 주세요.

---

### ④ 보고 — 한 줄이면 됨

다음 정보만 알려주시면 됩니다:
- ✅ HW 4/4 통과 / ⚠ 일부 실패 (몇 번)
- 캡처 파일 경로 (예: `/tmp/eeg_capture.npy`)
- 임피던스 대략 값 (옵션)

이후 에이전트가:
- 🟡 → 🟢 biological-confirmed 격상 PR 1개
- `IIT4.md` deferred B `🟠 hw-ready → 🟢 LIVE-MEASURED` flip
- 3-substrate Φ 삼각측정 (EEG 생체 + AKIDA 실리콘 + ECA 시뮬) 완결 entry
- UNIVERSE/H_679~682 §6 결과 갱신

까지 자동 정리합니다.

---

## ❓ 자주 나오는 막힘

| 증상 | 원인 | 대응 |
|---|---|---|
| `EEG HW 미도달: sentinel missing` | ①번 파일 없음 | `touch ~/.config/anima/eeg_headset_ready` |
| `EEG HW 미도달: brainflow board NOT_FOUND` | 보드 미인식 | USB/블루투스 연결 · 보드 id 확인 (board 매뉴얼) |
| `EEG HW 미도달: capture file missing` | ②번 캡처 안 됨 | brainflow 명령 재실행 · 경로 확인 |
| 임피던스 > 50kΩ 알람 | 전극 접촉 불량 | 젤·식염수 추가 · 압력 살짝 ↑ · 머리카락 정리 |
| `hexa run` SIGKILL (Mac) | ASP/AMFI 정책 | `! sidecar sign local` 토큰 + 30분 안에 실행 |

---

## 정합

- **이 문서 = human-only TODO**, 에이전트 자동화 불가능한 단계만 모음
- HW path 실행 결과 = 사용자 단계 1회 → 자동 환류 (UNIVERSE + IIT4 + ANIMA 트리)
- 거짓 PASS 보고 회피: sentinel 파일 + brainflow board ping + capture file 3-신호 모두 필요
- 정합 = `feedback-closure-is-physical-limit` (헤드셋 미착용 = open frontier, not failure)

## 양방향 sibling
- ⇄ [EEG.md](./EEG.md): 정식 milestone 표
- ⇄ [EEG.easy.md](./EEG.easy.md): L1~L12 친근 카탈로그
- ⇄ [EEG_CAPTURE_RUNBOOK.md](./EEG_CAPTURE_RUNBOOK.md): 헤드셋 4단계 상세 절차
- ⇄ [../HANDOFF.md](../HANDOFF.md): 다음 세션 AI 인계 9-section
- ⇄ [../HEXAD/IIT4/IIT4.md](../HEXAD/IIT4/IIT4.md): deferred B closure 트리거
- ⇄ [../UNIVERSE/H_679_eeg_measurement_core.md](../UNIVERSE/H_679_eeg_measurement_core.md) 등: HW 결과 갱신 대상 (H_679~682)
