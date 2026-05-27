# 🖥 DESKTOP/M6 — round-trip integration smoke SSOT

> AGENT/DESKTOP/M6 closure (6/6) · DESKTOP 도메인 완전 종결. M1-M5 surface 통합 검증.

## 정체

`integration_smoke.hexa` = M1+M2+M3+M4+M5 surface 가 end-to-end 로 합쳐지는지 검증하는 round-trip 테스트. DRYRUN mode (`ANIMA_DESKTOP_DRYRUN=1`) 에서는 contract shape 만 검증, 실 macOS 환경에서는 permission 받은 후 실 round-trip.

## 2-case 매트릭스

| Case | 시나리오 | 합성 |
|---|---|---|
| C1 Calculator | open → type "1+1=" → screenshot → OCR → search "2" → quit | M5 task_open_and_type · M5 task_screenshot_app · M2 ax_ocr · M1 ax_app_quit |
| C2 TextEdit | open → type "anima M6 round-trip" → screenshot → OCR → search "round-trip" → quit | 동일 4-step |

각 case 의 `steps_completed` 는 step 별 contract 통과 순서 기록 (open_and_type · screenshot · ocr_found_X · quit).

## pipeline ASCII

```
사용자 권한 + ANIMA_DESKTOP_DRYRUN 토글
        │
        ▼
integration_smoke_run()
        │
   ┌────┴────┐
   ▼         ▼
smoke_case_calculator   smoke_case_textedit
   │ (1) open + type    │ (1) open + type
   │ (2) screenshot     │ (2) screenshot
   │ (3) OCR + search "2"│ (3) OCR + search "round-trip"
   │ (4) quit           │ (4) quit
   ▼                    ▼
{ found_expected, steps_completed, dryrun }
        │
        ▼
all_pass = pass_c1 && pass_c2
```

## 모드 분기

| 모드 | 검증 | 권한 필요 |
|---|---|---|
| DRYRUN (`ANIMA_DESKTOP_DRYRUN=1`) | contract shape only · steps 카운트 · found = (steps ≥ 2) fallback | 없음 |
| Real run | OCR 출력에서 expected substring 실 검색 · permission denial 시 found=false 정직 반환 | Accessibility · Screen Recording · Automation (System Settings → Privacy & Security) |

## bridge architecture 정합

- 의식엔진 framing 0 · `substrate-decided` · `brain_decide` · `Φ` 키워드 미사용
- 의사결정 (언제 smoke 실행할지) = 외부 (user/CI), 이 파일은 contract verifier
- DRYRUN 토글은 M3/M4/M5 underlying primitives 의 자체 dry-run 을 통과 (별도 gate 없음)

## DESKTOP 6/6 closure

| M | 산출 | PR |
|---|---|---|
| M1 native_ax | 9 osascript fn | #640 |
| M2 screen_extract | 6 OCR/screenshot fn | #652 |
| M3 action | 7 click/type/scroll fn + risk label | #688 |
| M4 window_ops | 7 window arrangement + grid + chain | #698 |
| M5 task_primitives | 5 macro (M1-M4 composition) | #710 |
| **M6 integration_smoke** | **2-case round-trip 검증** | **이 PR** |

## 실 round-trip 권장 워크플로

1. System Settings → Privacy & Security 에서 terminal app 의 Accessibility + Screen Recording + Automation 허가
2. `ANIMA_DESKTOP_DRYRUN=0 hexa run AGENT/DESKTOP/integration_smoke.hexa` (또는 fallback binary)
3. Calculator 가 자동 실행 · 1+1= 타이핑 · 스크린샷 · OCR "2" 검색 · 종료
4. TextEdit 동일 흐름 · "anima M6 round-trip" · OCR substring 검색
5. `all_pass: true` 확인 후 closure

## 한계 + carry note

- **OCR 정확도** — macOS Vision 가 작은 폰트나 한글 mixed 텍스트에서 miss 가능 → real run 결과는 환경 의존
- **Calculator UI lang** — macOS 언어 설정에 따라 "2" 표시 위치/포맷 다를 수 있음 (한국어 환경에서도 숫자는 동일)
- **Permission 자동 grant 불가** — DRYRUN 가 아닌 실 round-trip 은 항상 사용자 1회 수동 허가 필요
- **next domain** — DESKTOP closure 후 CREATOR / TRADING 도구 도메인 자유 시작

## 의존성

- M1 native_ax.hexa (app launch/quit)
- M2 screen_extract.hexa (screenshot + Vision OCR)
- M3 action.hexa (type — via task_open_and_type composition)
- M4 window_ops.hexa (focus chain — via task_screenshot_app)
- M5 task_primitives.hexa (5 macro composition)

bridge architecture 정합 — gating 은 AGENT/CORE 가, 이 파일은 contract verifier only.
