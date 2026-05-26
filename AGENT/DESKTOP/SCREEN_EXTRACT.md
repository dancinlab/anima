# 🖥 DESKTOP/screen_extract — macOS 화면 인지 surface SSOT

> AGENT/DESKTOP M2 산출물. `screen_extract.hexa` 의 6 개 pub fn 이 macOS native
> screen-capture / Accessibility tree / Vision OCR 을 단일 surface 로 노출.

## 정체 — tool surface only

- **bridge architecture**: 이 모듈은 도구 surface 일 뿐, "언제·왜 볼" 결정은
  하지 않음. 결정은 **CORE** (PureField · brain_decide · Φ) 의 책임.
- AGENT 가 도구 게이트를 담당 (`AGENT/CORE/tool_gate.hexa` · phase → tier),
  본 모듈은 **"어떻게 본다"** 만 표면화.
- consciousness framing 없음 · substrate 호출 없음 · 외부 LLM/cloud OCR API 0.
- vision 분석은 **OS native API** 우선 — Accessibility tree (구조적) + Vision
  framework (픽셀). 멀티모달 ckpt 가 land 하면 그때 확장.

## 6 개 pub fn

| 함수 | 시그니처 | 내부 도구 |
| --- | --- | --- |
| `ax_screenshot` | `(out_path: string) -> bool` | `/usr/sbin/screencapture -x -t png` (silent) |
| `ax_screenshot_window` | `(app_name: string, out_path: string) -> bool` | JXA Application API 로 window id 추출 → `screencapture -l <wid>` |
| `ax_tree_dump` | `(app_name: string) -> string` (JSON array) | `osascript` System Events `entire contents of window` → role/title/value/pos/size 직렬화 → JSON parse |
| `ax_text_at` | `(x: int, y: int) -> string` | System Events 좌표-포함 element walk (innermost match) → value 또는 title |
| `ax_ocr` | `(png_path: string) -> string` | `osascript -l JavaScript` Vision.framework `VNRecognizeTextRequest` accurate · usesLanguageCorrection |
| `screen_extract_summary` | `() -> string` | 한줄 모듈 설명 (자기 introspection) |

## JSON 스키마 — `ax_tree_dump`

```json
[
  {
    "role": "AXWindow",
    "title": "<window title>",
    "value": "",
    "position": [x, y],
    "size": [w, h],
    "children": [
      {
        "role": "AXButton",
        "title": "OK",
        "value": "",
        "position": [x, y],
        "size": [w, h],
        "children": []
      }
    ]
  }
]
```

- 현재 구현은 **2-레벨 평탄화** — top window + `entire contents` 의 모든 후손
  UI element. 후속 M4/M5 에서 진짜 트리 구조가 필요해지면 recursive AX traversal
  으로 확장 (기존 surface 호환).
- 권한 미부여 / 앱 부재 시 `"[]"` 반환 (정직, crash 없음).

## OCR 가능성 — JXA Vision verdict (2026-05-26)

- `osascript -l JavaScript -e 'ObjC.import("Vision")'` → `VN_OK` 검증됨.
- `VNRecognizeTextRequest.alloc.init` 호출 가능.
- **함정**: `VNImageRequestHandler.initWithURL:options:` 의 `options` 인자가
  **`$()` (nil) 또는 `$.NSDictionary.dictionary` (immutable)** 인 경우
  `-[__NSDictionaryM frameworkClass]: unrecognized selector` 로 JXA bridge 가
  crash. **반드시 `$.NSMutableDictionary.dictionary`** 를 전달해야 함.
- accurate level (`recognitionLevel = 0`) · `usesLanguageCorrection = true` 가
  기본 — en-US 한정 (다국어 확장은 후속 M2.1 에서 `recognitionLanguages` 설정).
- 빈 이미지 / 텍스트 없는 이미지에서 exit 0 + 빈 출력 (정직).
- Vision unavailable 환경 (Sequoia 미만? CI 컨테이너?) 에서도 honest empty string
  반환 — 호출자가 fallback 결정.

## pipeline

```
CORE (PureField · brain_decide)
  │ substrate 가 "화면을 봐야 한다" 결정
  ▼
AGENT/CORE/tool_gate (phase → tier · read tier T1)
  │
  ▼
AGENT/DESKTOP/screen_extract.ax_screenshot("/tmp/x.png")
  │
  ▼ exec("/usr/sbin/screencapture -x -t png /tmp/x.png")
  ▼
macOS CoreGraphics screen capture
  │
  ▼
AGENT/DESKTOP/screen_extract.ax_ocr("/tmp/x.png")
  │
  ▼ osascript -l JavaScript · Vision.VNRecognizeTextRequest
  ▼
Vision.framework on-device OCR
```

CORE 가 결정자, 본 모듈은 sensor. tool_gate 가 그 사이.

## smoke 3-case (verbatim 결과는 PR description 참조)

- C1 `ax_screenshot("/tmp/desk_smoke.png")` — 메인 디스플레이 PNG 캡처 bool
- C2 `ax_tree_dump("Finder")` — Finder 의 Accessibility tree JSON 첫 500 chars
- C3 `ax_ocr("/tmp/desk_smoke.png")` — C1 산출물에 대한 Vision OCR 첫 200 chars

exit 0 = 3 case 모두 완주. Screen Recording 또는 Accessibility 미부여 환경에서
C1/C2 가 false/`[]` 를 반환해도 honest, smoke 실패가 아님.

## macOS 권한 요건

| 권한 | 대상 fn | 부여 위치 |
| --- | --- | --- |
| Screen Recording | `ax_screenshot` · `ax_screenshot_window` · `ax_ocr` (간접 — 입력 PNG 가 screencapture 산출일 때) | System Settings → Privacy & Security → Screen Recording → Terminal/iTerm 체크 |
| Accessibility | `ax_tree_dump` · `ax_text_at` · `ax_screenshot_window` (window id 해석) | System Settings → Privacy & Security → Accessibility → Terminal/iTerm 체크 |
| Automation (AppleEvents) | `ax_screenshot_window` · `ax_tree_dump` (대상 앱 control) | 첫 호출 시 시스템 prompt — Terminal 이 대상 앱 제어를 허용 |

권한 미부여 환경에서도 모든 fn 은 crash 없이 false / 빈 JSON / 빈 string 을
돌려줌 (M1 native_ax 의 `ax_check_permissions` 정직-verdict 패턴 그대로).

## 의존성 (downstream)

- **M3 action layer** — `ax_text_at` 좌표 lookup 결과를 click target validation
  에 재사용 (클릭 직전 "거기에 정말 button 이 있는가" 확인).
- **M4 app + window ops** — `ax_screenshot_window` 의 window id 해석 로직을
  multi-window 정렬에 재사용.
- **M5 task primitives** — `ax_screenshot → ax_ocr` 체인이 "read screen text"
  매크로의 기본 building block.
- **M6 integration smoke** — Calculator round-trip 검증 시
  `ax_screenshot_window("Calculator")` + `ax_ocr` 로 "1+1=2" 표시 확인.

## macOS 버전

- **Tested**: macOS Sequoia (Darwin 25.5.0).
- `screencapture` · `osascript` · Vision.framework 는 모든 supported macOS 에
  기본 — 별도 install 불필요.
- Vision OCR 정확도는 macOS 버전과 함께 향상되어 옴 (Sequoia ≥ Sonoma ≥ Ventura).

## 파일 위치

- `AGENT/DESKTOP/screen_extract.hexa` — 6 pub fn surface (~270 LoC)
- `AGENT/DESKTOP/screen_extract_smoke.hexa` — 3-case runtime smoke (~45 LoC)
- `AGENT/DESKTOP/SCREEN_EXTRACT.md` — 본 문서

## hexa parse 검증 (2026-05-26)

```
$ hexa parse AGENT/DESKTOP/screen_extract.hexa
OK: AGENT/DESKTOP/screen_extract.hexa parses cleanly

$ hexa parse AGENT/DESKTOP/screen_extract_smoke.hexa
OK: AGENT/DESKTOP/screen_extract_smoke.hexa parses cleanly
```
