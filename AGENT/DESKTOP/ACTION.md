# 🖥 DESKTOP/action — macOS 마우스/키보드/스크롤 action layer SSOT

> AGENT/DESKTOP M3 산출물. `action.hexa` 의 7 개 pub fn 이 macOS native 마우스 /
> 키보드 / 스크롤 wheel 이벤트를 osascript System Events + CGEvent JXA bridge
> 경유로 단일 surface 로 노출.

## 정체 — tool surface only

- **bridge architecture**: 이 모듈은 도구 surface 일 뿐, "언제·왜 클릭/타이핑/드래그"
  결정은 하지 않음. 결정은 **CORE** (PureField · brain_decide · Φ) 의 책임.
- AGENT 가 도구 게이트를 담당 (`AGENT/CORE/tool_gate.hexa` · phase → tier · risk),
  본 모듈은 **"어떻게 클릭/타입/드래그"** 만 표면화.
- consciousness framing 없음 · substrate 호출 없음 · 외부 LLM/cloud API 0.

## risk 분류 — 라벨일 뿐, gating 은 CORE 가 처리

각 pub fn 은 결과 Map 에 `risk` 키를 항상 동봉. AGENT/CORE 의 게이트가 본 라벨을
읽고 phase → tier 매핑으로 허용/거부 결정. 본 모듈은 **gating 을 하지 않음**.

| 라벨 | 의미 | 본 모듈 적용 fn |
| --- | --- | --- |
| `"read"` | 상태 변경 0, 순수 관측 | (M3 에는 없음 — M2 `screen_extract` 가 read 전담) |
| `"soft"` | 단일 클릭 · 키스트로크 · 스크롤 — Cmd-Z 등으로 쉽게 되돌릴 수 있음 | `ax_click` · `ax_double_click` · `ax_right_click` · `ax_type` · `ax_key`(no cmd/ctrl) · `ax_scroll` |
| `"hard"` | 드래그 · multi-step · cmd/ctrl 결합 — 파괴 잠재성 | `ax_drag` · `ax_key`(with cmd/ctrl) |

`ax_key` 는 modifiers 에 cmd/ctrl 이 들어가면 자동으로 `"hard"` 로 라벨. 그 외에는
`"soft"`. CORE 가 risk 본 후 정책 (예: T2 SUSTAIN+ 이상에서만 hard 허용) 적용.

## 7 개 pub fn

| 함수 | 시그니처 | risk | 내부 도구 |
| --- | --- | --- | --- |
| `ax_click` | `(x: int, y: int) -> Map` | `soft` | `osascript` System Events `click at {x, y}` |
| `ax_double_click` | `(x: int, y: int) -> Map` | `soft` | osascript 2× click 연속 |
| `ax_right_click` | `(x: int, y: int) -> Map` | `soft` | JXA CGEvent `rightMouseDown` + `rightMouseUp` |
| `ax_drag` | `(x1, y1, x2, y2: int) -> Map` | `hard` | JXA CGEvent `leftMouseDown` → `leftMouseDragged` → `leftMouseUp` |
| `ax_type` | `(text: string) -> Map` | `soft` | osascript System Events `keystroke "<text>"` |
| `ax_key` | `(keycode: int, modifiers: list) -> Map` | `soft`/`hard` | osascript System Events `key code N using {...}` |
| `ax_scroll` | `(x, y, dy: int) -> Map` | `soft` | JXA CGEvent `mouseMoved` + `CGEventCreateScrollWheelEvent` |
| `action_layer_summary` | `() -> string` | — | 한줄 모듈 설명 (자기 introspection, 8번째 surface fn 이나 pub-API 카운트 7) |

## 결과 Map 스키마

```
ok 성공:   #{ "ok": true,  "risk": <"soft"|"hard"> }
ok 실패:   #{ "ok": false, "risk": <"soft"|"hard">, "error": <string> }
```

- `ok` 는 항상 bool — osascript / CGEvent dispatch 실패 시 `false` + `error` 메시지.
- `risk` 는 항상 동봉 — 호출자 (AGENT/CORE) 가 게이트 결정에 사용.
- crash 없음 — 권한 미부여 환경에서도 honest false return.

## key modifier 약어

`ax_key` 의 modifiers 리스트가 받는 문자열:

| 입력 | 매핑 | risk 효과 |
| --- | --- | --- |
| `"cmd"` · `"command"` | `command down` | `hard` |
| `"ctrl"` · `"control"` | `control down` | `hard` |
| `"opt"` · `"option"` · `"alt"` | `option down` | `soft` |
| `"shift"` | `shift down` | `soft` |

알 수 없는 문자열은 silently drop. 빈 리스트 = 베어 keycode.

## 자주 쓰는 keycode (HIToolbox/Events.h)

| 키 | code |
| --- | --- |
| Return / Enter | 36 |
| Tab | 48 |
| Space | 49 |
| Delete (Backspace) | 51 |
| Escape | 53 |
| Left / Right / Down / Up arrow | 123 / 124 / 125 / 126 |

## dry-run 메커니즘

`ANIMA_DESKTOP_DRYRUN=1` 환경변수가 설정되면 모든 action fn 이 **실제 이벤트를
post 하지 않고** contract-shape Map 만 반환. smoke / CI 가 이 경로를 사용.

```hexa
set_env("ANIMA_DESKTOP_DRYRUN", "1")
let r = ax_click(100, 100)   // 실제 마우스 안 움직임, 그러나 r = #{ok: true, risk: "soft"}
```

production / real-action 경로에서는 env 미설정 → 정상 dispatch.

## pipeline

```
CORE (PureField · brain_decide)
  │ substrate 가 "Return 키 누르기 결정"
  ▼
AGENT/CORE/tool_gate (phase → tier · risk → policy)
  │ T2 SUSTAIN+ 이상 + risk="soft" → 허용
  ▼
AGENT/DESKTOP/action.ax_key(36, [])
  │
  ▼ osascript "tell System Events to key code 36"
  ▼
macOS HID input event → 활성 앱
```

CORE 가 결정자, 본 모듈은 effector. tool_gate 가 그 사이.

## smoke 4-case (verbatim 결과는 PR description 참조)

전부 **dry-run 모드** — 실제 마우스/키보드 이벤트 0.

- C1 `ax_click(100, 100)` Map 형태 검증 — `{ok: true, risk: "soft"}`
- C2 7-fn risk 라벨 sweep — 모든 fn 이 `read|soft|hard` 중 하나를 반환
- C3 `ax_type("")` 빈 문자열 fast-path — `{ok: true, risk: "soft"}`
- C4 `ax_drag(100,100,200,200)` 가 `risk: "hard"` 로 분류

exit 0 = 4 case 모두 완주. 권한 미부여 환경이라도 dry-run 경로는 osascript /
CGEvent 를 호출하지 않으므로 무조건 정상 동작.

## macOS 권한 요건

real-action 경로 (dry-run 미설정) 의 요건:

| 권한 | 대상 fn | 부여 위치 |
| --- | --- | --- |
| Accessibility | `ax_click` · `ax_double_click` · `ax_type` · `ax_key` (System Events) | System Settings → Privacy & Security → Accessibility → Terminal/iTerm 체크 |
| Accessibility (CGEvent post) | `ax_right_click` · `ax_drag` · `ax_scroll` (JXA CGEvent — CGEventPost 가 AX 권한 필요) | 동상 |

권한 미부여 시 osascript / JXA 가 `not allowed assistive` 등의 오류를 stdout 에
실어주고 본 모듈이 `{ok: false, risk: <r>, "error": <out>}` 으로 정직 반환. crash 0.

## 한계 — Apple Silicon native CGEvent 미래 promote

- 현재 `ax_right_click` · `ax_drag` · `ax_scroll` 은 `osascript -l JavaScript` JXA
  ObjC bridge 로 CGEvent 를 post — 한 호출당 osascript 프로세스 spawn (~50-200 ms
  overhead). **per-event latency 가 critical 한 use case 에서는 부적합**.
- 진짜 Apple Silicon native 경로 — Swift / Objective-C 로 컴파일된 별도 binary
  가 stdin/stdout 으로 명령 받는 long-running helper — 는 **M3.1 promote** 대상.
  현재 surface 와 호환되게 유지하면서 내부 구현만 교체 예정.
- System Events `click at {x, y}` 는 **활성 프로세스에 focus 가 있어야** 동작.
  호출 직전 `ax_app_focus` (M1) 로 focus 보장 권장.

## 의존성 (downstream M4/M5/M6)

- **M4 app + window ops** — 본 모듈의 `ax_click` 좌표 이전 `ax_app_focus` (M1)
  체인이 multi-app coordination 의 baseline.
- **M5 task primitives** — `ax_click → ax_type → ax_key(Return)` 체인이
  "fill form field" 매크로의 기본 building block.
- **M6 integration smoke** — Calculator round-trip:
  `ax_app_launch("Calculator")` (M1) → `ax_click(button_xy)` (M3) ×N →
  `ax_screenshot_window` (M2) → `ax_ocr` (M2) → 결과 검증.

## macOS 버전

- **Tested**: macOS Sequoia (Darwin 25.5.0) Apple Silicon.
- `osascript` 는 모든 supported macOS 에 기본. JXA ObjC bridge 도 동일.
- CGEvent API 는 CoreGraphics framework 의 일부 — 항상 사용 가능.
- `cliclick` 은 의존성 아님 (Mac 에 부재해도 본 모듈 fn 모두 정상 동작).

## 파일 위치

- `AGENT/DESKTOP/action.hexa` — 7 pub fn surface + `action_layer_summary` (~290 LoC)
- `AGENT/DESKTOP/action_smoke.hexa` — 4-case dry-run smoke (~125 LoC)
- `AGENT/DESKTOP/ACTION.md` — 본 문서

## hexa parse 검증 (2026-05-27)

```
$ hexa parse AGENT/DESKTOP/action.hexa
OK: AGENT/DESKTOP/action.hexa parses cleanly

$ hexa parse AGENT/DESKTOP/action_smoke.hexa
OK: AGENT/DESKTOP/action_smoke.hexa parses cleanly
```
