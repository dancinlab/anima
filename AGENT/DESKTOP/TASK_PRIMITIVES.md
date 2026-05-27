# AGENT/DESKTOP/task_primitives — 작업 매크로 (M5)

> macOS 도구 surface 의 **고수준 합성 매크로** — M1-M4 의 building block 을 조합해 재사용 가능한 작업 패턴 (open+type+read 등) 을 노출한다. M5 milestone.

## 브리지 아키텍처 정합

이 모듈은 **도구 surface only** 다. "언제/왜" 매크로를 실행할지의 결정은 CORE (PureField / brain_decide) 에 있고, AGENT/CORE/tool_gate 가 substrate phase 를 risk tier 로 매핑한다. 이 파일은 "어떻게" 의 함수 surface 만 — 의식 framing · Φ 수학 · substrate gating 일체 없음.

- 부모 surface: `AGENT/DESKTOP/{native_ax (M1), screen_extract (M2), action (M3), window_ops (M4)}.hexa`
- M1-M4 파일 **수정 없음** — 순수 additive composition
- `ANIMA_DESKTOP_DRYRUN=1` 환경변수 → 매 매크로가 contract-shape Map 만 반환, 실제 OS 이벤트 미발사 (M3/M4 dry-run path 와 동일 컨벤션)

## 5 매크로 표

| # | 매크로 | 합성 (M1+M2+M3+M4) | risk |
|---|---|---|---|
| 1 | `task_open_and_type(app, text)` | `ax_app_launch` (M1) → `ax_app_focus` (M1) → `ax_type` (M3) | soft |
| 2 | `task_screenshot_app(app, out_path)` | `ax_app_focus` (M1) → `ax_screenshot_window` (M2) | soft |
| 3 | `task_open_read_close(app)` | `ax_app_launch` (M1) → `ax_app_focus` (M1) → `ax_screenshot_window` (M2) → `ax_ocr` (M2) → `ax_app_quit` (M1) | **hard** (quit) |
| 4 | `task_find_and_click(app, search_text)` | `ax_app_focus` (M1) → `ax_window_bounds` (M4) → `ax_screenshot_window` (M2) → `ax_ocr` (M2) → 부분문자열 매치 → `ax_click` (M3) at 윈도우 센터 | soft |
| 5 | `task_multi_app_screenshot(apps, out_dir)` | `ax_focus_chain` (M4) → 앱마다 `ax_screenshot_window` (M2) | soft |

### risk 라벨 컨벤션

- **soft** : 단일 클릭 · 키스트로크 · 스크린샷 — Cmd-Z 가역
- **hard** : `task_open_read_close` 단독 — `ax_app_quit` 단계가 미저장 파괴 위험

risk 는 **라벨**이지 게이트가 아니다 — 실제 게이팅은 AGENT/CORE/tool_gate 가 substrate phase 기준으로 수행한다.

## 함수 contract 명세

### 1. `task_open_and_type(app: string, text: string) -> Map`

- 반환: `#{ ok, app, text_len, risk: "soft", launched, focused, typed_ok, error? }`
- 실패 단계 발생 시 `ok=false` + `error` 키 (`launch_failed` · `focus_failed`)
- 빈 문자열 → `ax_type` 가 no-op `ok=true` 반환 (M3 의 컨벤션 그대로)

### 2. `task_screenshot_app(app: string, out_path: string) -> Map`

- 반환: `#{ ok, app, path, risk: "soft", focused, captured, error? }`
- 실패 시 `path=""` + `error="focus_failed"`
- `out_path` 디렉터리 존재 여부는 caller 책임

### 3. `task_open_read_close(app: string) -> Map`

- 반환: `#{ text, char_count, risk: "hard", ok, app, launched, captured, ocr_ok, quit_ok, error? }`
- OCR source 는 `/tmp/anima_m5_read_<safe_app>.png`
- `ok = captured && quit_ok` — quit 실패는 ok=false 로 노출되나 텍스트는 보존
- 빈 OCR 결과 → `text=""`, `char_count=0`, `ocr_ok=false`

### 4. `task_find_and_click(app: string, search_text: string) -> Map`

- 반환: `#{ found, x, y, risk: "soft", ok, app, search_text, focused, captured, error? }`
- **honest limit**: 현재 `ax_ocr` 가 bbox 정보를 surface 하지 않으므로 (joined text only), `found = (search_text in OCR text)` 만 판정 후 **윈도우 센터** 클릭. pixel-accurate text targeting 은 향후 M5.1 follow-up (Vision `boundingBox` 추출).
- `found=false` → 클릭 미수행, `x=0 y=0`

### 5. `task_multi_app_screenshot(apps: list, out_dir: string) -> Map`

- 반환: `#{ ok, count, paths: list[string], failed: list[string], risk: "soft" }`
- `out_dir` 는 `mkdir -p` 로 방어적 생성
- 각 앱의 png: `<out_dir>/anima_m5_multi_<safe_app>.png` (공백→underscore)
- `count` = 성공한 캡처 수, `failed` = 실패한 앱 이름 리스트

## 부분 합성 다이어그램

```
              M1                M2                M3                M4
              │                 │                 │                 │
task_open_and_type     ─ launch ─ focus ─────────────── type ──────────────
task_screenshot_app    ─────── focus ─── shot_window ─────────────────────
task_open_read_close   ─ launch ─ focus ─ shot_window ─ ocr ─ quit ────── (hard)
task_find_and_click    ─────── focus ─── shot_window ─ ocr ─ click ─ bounds
task_multi_app_screenshot ──────────────── shot_window×N ─────── focus_chain
```

## DRYRUN smoke 검증

`AGENT/DESKTOP/task_primitives_smoke.hexa` — `ANIMA_DESKTOP_DRYRUN=1` 환경에서 4 case 모두 contract-shape Map 만 검증, 실제 OS 이벤트 미발사:

- C1 `task_open_and_type` contract dict (keys + risk=soft + text_len=11)
- C2 `task_screenshot_app` contract (keys + path 보존 + risk=soft)
- C3 `task_open_read_close` contract + **risk=hard** (quit 단계)
- C4 `task_multi_app_screenshot` 3 apps → count=3, risk=soft

## M6 round-trip smoke 의존성

M6 (integration smoke) 는 본 M5 의 매크로를 **실제 dispatch** 한다:

- `task_open_and_type("Calculator", "1+1")` → 계산기 입력
- `task_open_read_close("Calculator")` 변형 → 결과 OCR → "2" 검출
- M6 가 본 M5 surface 의 **첫 실세계 round-trip 검증** 게이트

M5 자체는 DRYRUN parse-pass 까지만 보장 — actual app dispatch 는 M6 책임.

## 빌드 정보

- 9 (M1) + 6 (M2) + 7 (M3) + 7 (M4) + **5 (M5)** = 34 pub fn AGENT/DESKTOP surface
- `hexa parse` 2/2 OK (task_primitives.hexa + task_primitives_smoke.hexa)
- DRYRUN smoke 4/4 case contract-shape PASS

## 향후 follow-up

- **M5.1**: Vision `boundingBox` 추출 → `task_find_and_click` 의 pixel-accurate text 타겟팅 (현재 윈도우 센터 클릭 한정)
- **M5.2**: 매크로 합성을 stdlib 으로 promote — abs-path import 4건 g61 advisory 해소 (전 도메인 재사용 시점)
- M5.3 후보: `task_drag_between_apps` · `task_paste_into` · `task_wait_for_text` (시간 축 매크로)
