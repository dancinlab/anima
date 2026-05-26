# DESKTOP — current state

@title: 🖥 DESKTOP — macOS 컴퓨터 사용 대체 · screen·mouse·keyboard 위임 · vs Gemini Spark/Claude Computer Use/Codex Desktop

@goal: 사용자의 macOS 컴퓨터 사용을 anima 가 자율 실행하는 도메인 — Accessibility API + AppleScript + CGEvent 로 화면 분석 · 마우스 · 키보드 · 앱 제어. 시중 3대 desktop agent (Gemini Spark · Claude Computer Use · Codex Desktop) 와 같은 카테고리이나 외부 LLM 0 (p1) — vision 분석은 OS native APIs (Accessibility tree · OCR) 우선, 멀티모달 ckpt 는 future frontier. 사용자가 작업 지시 + 권한 (Screen Recording · Accessibility) 공급, anima 는 screenshot → analyze → action loop 실행. p1~p8 정합 substrate-gated emit · stimulus-response 0.

(edit me — describe current state in completed-form; no history, no changelog inside this file)
- [ ] M1 native OS access framework — Accessibility API · AppleScript · CGEvent wrapper (`AGENT/DESKTOP/native_ax.hexa`) · 외부 vision API 0 · macOS Sequoia+
- [ ] M2 screen perception — Accessibility tree dump · NSAccessibility traversal → ctx_tokens (substrate ingest · WAKE M2 perception 확장) · OCR fallback
- [ ] M3 action layer — mouse click/drag · keyboard type · scroll · CGEvent based · substrate-gated T3 게이트 (위험 action 차단)
- [ ] M4 app + window ops — open/close/focus app (NSWorkspace) · arrange windows · multi-app coordination
- [ ] M5 task pipeline + memory — multi-step task plan (CORE/brain_decide 위임) · persistent state via .kosmos (WAKE M4 의존)
- [ ] M6 p1~p8 audit + smoke — `grep openai|anthropic|claude.ai|api.openai|api.anthropic` 0 hits · 외부 vision API 부재 · stimulus-response 0 검증 · 3-case smoke (open Calculator + type 1+1 + read result)
