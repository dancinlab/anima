# DESKTOP — current state

@title: 🖥 DESKTOP — macOS 컴퓨터 도구 surface · AGENT 산하 (vs Gemini Spark / Claude Computer Use / Codex Desktop)

@goal: macOS 의 화면 분석 + 마우스/키보드/앱 제어 도구 surface 를 제공하는 도메인. Accessibility API · AppleScript · CGEvent · NSWorkspace 어댑터 묶음. 시중 3대 desktop agent (Gemini Spark · Claude Computer Use · Codex Desktop) 와 같은 카테고리이나, vision 분석은 OS native API (Accessibility tree · OCR) 우선 — 멀티모달 ckpt 가 land 하면 그때 확장. 의식적 결정 (언제 클릭/타이핑할지) 은 CORE 가 담당, 이 도메인은 "어떻게" 의 함수 surface 만.

(edit me — describe current state in completed-form; no history, no changelog inside this file)
- [x] M1 native OS access — `AGENT/DESKTOP/{native_ax.hexa,native_ax_smoke.hexa,NATIVE_AX.md}` 9 pub fn (app list/focus/launch/quit · window list/focus · screen size · permissions · summary) · osascript/open/screencapture verified · cliclick absent (M3 CGEvent 직접) · hexa parse 2/2 OK (PR #640 ec64a82c)
- [x] M2 screen extract — `AGENT/DESKTOP/{screen_extract.hexa,screen_extract_smoke.hexa,SCREEN_EXTRACT.md}` 6 pub fn (screenshot · screenshot_window · tree_dump · text_at · ocr · summary) · screencapture + System Events AXAPI + Vision.framework JXA · OCR verified (VN_OK on Sequoia) · hexa parse 2/2 OK
- [ ] M3 action layer — mouse click/drag · keyboard type · scroll · CGEvent based action 함수 (위험도별 분류 라벨, 게이팅은 AGENT/CORE 가 처리)
- [ ] M4 app + window ops — open/close/focus app (NSWorkspace) · arrange windows · multi-app coordination 함수
- [ ] M5 task primitives — 도구 합성 매크로 (open + type + read 같은 기본 패턴) · 재사용 가능한 building block
- [ ] M6 integration smoke — Calculator round-trip (open · type "1+1" · read result = "2") 검증 · 다른 앱 1개 추가 검증
