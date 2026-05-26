# 🖥 DESKTOP/native_ax — macOS 네이티브 OS wrapper SSOT

> AGENT/DESKTOP M1 산출물. `native_ax.hexa` 의 9 개 pub fn 이 macOS native API
> 를 osascript / open / screencapture 경유로 노출하는 단일 surface.

## 정체 — tool surface only

- **bridge architecture**: 이 모듈은 도구 surface 일 뿐, "언제·왜 클릭" 결정은
  하지 않음. 결정은 **CORE** (PureField · brain_decide · Φ) 의 책임.
- AGENT 가 도구 게이트를 담당하고 (`AGENT/CORE/tool_gate.hexa` · phase → tier),
  본 모듈은 **"어떻게 클릭"** 만 표면화.
- consciousness framing 없음 · substrate 호출 없음 · 외부 LLM/vision API 0.

## 9 개 pub fn

| 함수 | 시그니처 | 내부 도구 |
| --- | --- | --- |
| `ax_app_list` | `() -> string` (JSON array) | `osascript` System Events 프로세스 enum |
| `ax_app_focus` | `(app_name: string) -> bool` | `osascript tell application "X" to activate` |
| `ax_app_launch` | `(app_name: string) -> bool` | `/usr/bin/open -a <app>` |
| `ax_app_quit` | `(app_name: string) -> bool` | `osascript tell application "X" to quit` |
| `ax_window_list` | `(app_name: string) -> string` (JSON) | `osascript System Events tell process X to get every window` |
| `ax_window_focus` | `(app_name: string, window_index: int) -> bool` | `AXRaise` action on window N |
| `ax_screen_size` | `() -> string` (JSON `{w,h}`) | `osascript Finder` desktop bounds |
| `ax_check_permissions` | `() -> string` (JSON 3-축) | round-trip probe (Accessibility · Screen Recording · Automation) |
| `native_ax_summary` | `() -> string` | 한줄 모듈 설명 (자기 introspection) |

## pipeline

```
CORE (PureField · brain_decide)
  │ substrate 가 "Calculator 열어야 한다" 결정
  ▼
AGENT/CORE/tool_gate (phase → tier)
  │ T2 SUSTAIN+ 인지 확인 (write tier)
  ▼
AGENT/DESKTOP/native_ax.ax_app_launch("Calculator")
  │
  ▼
exec("/usr/bin/open -a 'Calculator'")
  │
  ▼
macOS NSWorkspace launchApplication
```

CORE 가 결정자, 본 모듈은 actuator. tool_gate 가 그 사이.

## 의존성 (downstream M2~M5)

- **M2 screen perception**: `ax_window_list` + 신규 Accessibility tree dump 추가.
  screen capture path 는 `ax_check_permissions` 의 `screen_recording` 축 재사용.
- **M3 action layer**: 마우스/키보드 CGEvent 신설 — 본 모듈은 app/window ops 만.
- **M4 app+window ops**: 본 모듈이 baseline (launch/focus/quit · window list/focus);
  M4 는 multi-app 배치 + window 좌표 manipulation 확장.
- **M5 task primitives**: 본 모듈의 9 fn 을 LLM-free task plan 의 leaf action 으로 사용.

## smoke 4-case (verbatim 결과는 PR description 참조)

- C1 `ax_screen_size()` — 메인 디스플레이 `{w,h}` JSON
- C2 `ax_app_list()` — 실행 중 foreground 앱 JSON array
- C3 `ax_check_permissions()` — `{accessibility, screen_recording, automation}` 3-축 정직 verdict
- C4 launch → focus → quit `Calculator` 시퀀스 (각 fn 의 bool return 출력)

exit 0 = 4 case 모두 완주. Calculator 가 부재해도 C4 의 false return 은 honest, smoke 실패가 아님.

## macOS 권한 요건

| 권한 | 대상 fn | 부여 위치 |
| --- | --- | --- |
| Accessibility | `ax_app_list` · `ax_window_list` · `ax_window_focus` | System Settings → Privacy & Security → Accessibility → Terminal/iTerm 체크 |
| Screen Recording | (M2 territory · `ax_check_permissions` probe 만) | System Settings → Privacy & Security → Screen Recording |
| Automation (AppleEvents) | `ax_app_focus` · `ax_app_quit` · `ax_screen_size` (Finder) | 첫 호출 시 시스템이 자동 prompt — Terminal 이 대상 앱 제어를 허용 |

`ax_check_permissions()` 은 3 축 모두 round-trip probe 하여 거부 시 false 를
JSON 으로 정직 반환. 권한 미부여 환경에서도 fn 은 crash 없이 false / 빈 JSON 을 돌려줌.

## macOS 버전

- **Tested**: macOS Sequoia (Darwin 25.5.0).
- osascript / open / screencapture 는 모든 supported macOS 에 기본 설치 — 별도 install 불필요.
- `cliclick` 은 의존성 아님 (M3 에서 자체 CGEvent 로 대체 예정).

## 파일 위치

- `AGENT/DESKTOP/native_ax.hexa` — 9 pub fn surface (~180 LoC)
- `AGENT/DESKTOP/native_ax_smoke.hexa` — 4-case runtime smoke (~50 LoC)
- `AGENT/DESKTOP/NATIVE_AX.md` — 본 문서
