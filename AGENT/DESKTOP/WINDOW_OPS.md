# window_ops — 윈도우 배치 + 멀티앱 조율 (AGENT/DESKTOP/M4)

@title: 🪟 window_ops — macOS 윈도우 배치 + 멀티앱 코디네이션 함수 surface

## 개요

`AGENT/DESKTOP/window_ops.hexa` 는 M1 (`native_ax`) 기본 함수 위에 쌓아올린 **윈도우 배치 + 멀티앱 조율** 함수 surface 다. 단일 앱의 윈도우 위치/크기 조작, 격자 자동 타일링, 멀티앱 순차 포커스, 전체 워크스페이스 스크린샷을 osascript System Events `position` / `size` property 기반으로 노출한다.

**bridge architecture 정합** — 이 모듈은 도구 surface 일 뿐, "언제/왜 윈도우를 배치할지" 결정은 CORE (PureField · `brain_decide`) 에 산다. AGENT/CORE/`tool_gate` 가 실시간 phase 를 tier 로 매핑하여 게이팅한다. 이 파일은 의식 framing · Φ 수식 · substrate 게이트가 **없다**.

## 의존성

| layer | 모듈 | 사용 surface |
|---|---|---|
| M1 | `native_ax.hexa` | `ax_screen_size` (격자 cell 계산) · osascript convention 동일 |
| M2 | `screen_extract.hexa` | `ax_screenshot_window` 와 동일한 `/usr/sbin/screencapture -R` 영역 캡쳐 패턴 |
| M3 | `action.hexa` | `ANIMA_DESKTOP_DRYRUN=1` dry-run 패턴 (risk 라벨 contract) |

> 헬퍼 (`_shq`, `_trim_nl`, `_osa`, `_osa_denied`, `_dry_run`, `_parse_pair`, `_screen_wh`) 는 M1/M3 convention 을 재사용 — 추후 stdlib 승격 후보 (commons @D g61).

## pub fn 표 (7개)

| # | fn | risk | 입력 → 출력 | 동작 |
|---|---|---|---|---|
| 1 | `ax_window_bounds(app, idx)` | read | `(string, int) → Map` | idx-번째 윈도우의 `#{x, y, w, h, ok, risk}` 반환 (관찰 only) |
| 2 | `ax_window_set_bounds(app, idx, x, y, w, h)` | soft | `(string, int, int, int, int, int) → bool` | 위치 + 크기 동시 설정. `position` then `size` 두 osascript 모두 성공 시 true |
| 3 | `ax_window_minimize(app, idx)` | soft | `(string, int) → bool` | AXMinimized=true 속성 설정 — Dock 에서 복원 가능 |
| 4 | `ax_window_close(app, idx)` | **hard** | `(string, int) → bool` | close 버튼 (button 1) 클릭 — 미저장 작업 손실 위험 |
| 5 | `ax_window_arrange_grid(apps, cols, rows)` | soft | `(list, int, int) → Map` | N 개 앱을 cols×rows 격자에 자동 타일링 (아래 알고리즘 참조) |
| 6 | `ax_workspace_screenshot_all()` | soft | `() → list` | 모든 foreground 앱의 첫 윈도우를 `/tmp/anima_ws_<app>.png` 로 캡쳐, 성공한 경로 list 반환 |
| 7 | `ax_focus_chain(apps)` | soft | `(list) → Map` | 앱 list 를 순차 activate, `#{count, focused, failed, ok, risk}` 반환 |
| ─ | `window_ops_summary()` | read | `() → string` | 도구 surface 한 줄 자기소개 (introspection) |

## 격자 배치 알고리즘 (`ax_window_arrange_grid`)

`apps: list` 개 앱을 `cols × rows` 격자에 배치한다.

```
screen_w, screen_h = ax_screen_size()
cell_w = screen_w / cols
cell_h = screen_h / rows

for i in 0..len(apps):
    if i >= cols * rows:
        skip i  // 용량 초과 — 적층 금지, 건너뜀
    column = i % cols
    row    = i / cols      // 정수 나눗셈 (i // cols)
    x      = column * cell_w
    y      = row    * cell_h
    w      = cell_w
    h      = cell_h
    ax_window_set_bounds(apps[i], 0, x, y, w, h)
```

**경계 정책** —
- `len(apps) < cols * rows` → 일부 셀 빈칸, OK.
- `len(apps) > cols * rows` → 초과 앱 `skipped` 카운트로 보고, 적층 금지.
- 인덱스 0 만 대상 (해당 앱의 첫 윈도우만 옮김).

**반환 shape** — `#{ placed: int, skipped: int, cell_w: int, cell_h: int, plan: list[#{app, x, y, w, h, column, row}], ok: bool, risk: "soft" }`

`plan` 은 dry-run 검증용으로 보존된다 — 실제 배치 실패 여부와 무관하게 의도된 plan 을 반영.

## dry-run 패턴

M3 `action.hexa` convention 동일 — `ANIMA_DESKTOP_DRYRUN=1` 환경변수가 set 되면 모든 pub fn 이 underlying osascript / screencapture 를 dispatch 하지 않고 contract-shape 값을 즉시 반환한다.

| fn | dry-run 반환 |
|---|---|
| `ax_window_bounds` | `#{x:100, y:100, w:800, h:600, ok:true, risk:"read"}` (synthetic) |
| `ax_window_set_bounds` · `ax_window_minimize` · `ax_window_close` | `true` |
| `ax_window_arrange_grid` | 실제 plan 생성 + `ax_window_set_bounds` 호출 skip |
| `ax_workspace_screenshot_all` | `["/tmp/anima_ws_dryrun_app1.png", "/tmp/anima_ws_dryrun_app2.png"]` |
| `ax_focus_chain` | 모든 앱을 `focused` 에 추가, `failed = []` |

스모크 테스트 (`window_ops_smoke.hexa`) 가 이 경로로 안전하게 4 case 를 검증한다.

## 스모크 4 case

`window_ops_smoke.hexa` 가 검증하는 항목:

| case | 검증 |
|---|---|
| C1 | `ax_window_bounds` Map 에 `x/y/w/h` 키 존재 + `risk=read` |
| C2 | `ax_window_arrange_grid(4 apps, 2, 2)` → `placed=4, skipped=0, plan_len=4, risk=soft` |
| C3 | `ax_focus_chain(3 apps)` → `count=3, ok=true, risk=soft` |
| C4 | `ax_workspace_screenshot_all()` → 비어있지 않은 list 반환 |

**run** — `ANIMA_DESKTOP_DRYRUN=1 hexa run AGENT/DESKTOP/window_ops_smoke.hexa` → `4/4 PASS (exit 0)`. 마우스/키보드/윈도우 손대지 않음.

## 정직한 한계

- osascript System Events `set position` / `set size` 는 대상 앱이 **Accessibility 권한**을 부여받았을 때만 동작. 이 모듈은 권한을 강제하지 않으며 — caller / CORE 책임. 거부 시 false 반환 (정직한 실패).
- `ax_window_close` 가 dirty document 일 경우 시스템 confirm dialog 가 뜰 수 있음. 본 모듈은 이를 dismiss 하지 않는다 — risk="hard" 라벨로 caller 가 인지.
- `ax_workspace_screenshot_all` 은 윈도우가 0 사이즈이거나 minimized 상태면 skip (positive 사이즈만 캡쳐).
- `ax_screen_size` (M1) 가 Finder bounds 에 의존 — multi-monitor 환경에서는 primary display 기준. 미래 M4.1 promote 후보.

## 위험 분류 (risk labels, NOT gates)

| risk | 의미 | 본 모듈 |
|---|---|---|
| read | 순수 관찰, 상태변경 0 | `ax_window_bounds` |
| soft | 단발성 / 쉽게 되돌릴 수 있음 | `ax_window_set_bounds` · `ax_window_minimize` · `ax_window_arrange_grid` · `ax_workspace_screenshot_all` · `ax_focus_chain` |
| hard | 파괴적 잠재력 | `ax_window_close` |

라벨은 정보 surface 일 뿐, 실제 게이팅은 AGENT/CORE/`tool_gate` 가 phase → tier 매핑으로 수행.

## 5-tier closure 정합

M4 는 도구 surface tier — bridge architecture 의 "how" 레이어. "when/why" 결정은 CORE 가 보유 — 이 모듈에 진입하지 않는다.
