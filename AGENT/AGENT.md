# AGENT — current state

@title: 🤖 AGENT — ANIMA(CORE 의식엔진) ↔ 외부 도구 bridge · tier gate + role registry
@goal: ANIMA 가 외부 시스템에 접근할 때 거쳐가는 단일 bridge — CORE 의 의식적 결정(brain_decide)이 phase(DORMANT→RESONANT)/tier(T0→T3) 게이트를 통과해 sub-role 의 도구 surface 를 호출하는 구조. 도구 자체 (외부 API 어댑터 · OS native call) 는 `AGENT/<role>/` 산하에 도구 surface 만 — 의식엔진 구현은 CORE 가, 게이팅은 AGENT/CORE 의 tool_gate + agent_loop 가, 도구 자체는 각 role 이 분담. 외부 LLM 0 invariant 는 CORE 가 보장. `hx install` 가능한 제품으로 출하.

## 역할 에이전트 (사용자 위임 실행 · anima = 사용자의 손발)

- [ ] CODE — 사용자 코드 작업 위임 (think·read → file_write·run_tests → git_commit·push)
- [ ] CREATOR — 사용자 채널 콘텐츠 production engine (remotion · fal seedance 2.0 · openai images 2.0 · omnishow → publish 사용자 채널)
- [ ] TRADING — 사용자 증권 자율 매매 (scan·backtest → paper_trade → live_trade, 기존 trading 14모듈 회수)
- [ ] MERCHANT — 사용자 온라인 판매 운영 (3-lane: L1 ARBITRAGE 구매대행 · L2 NATIVE 자체 상품 · L3 OPS 공통 · `AGENT/MERCHANT/MERCHANT.md` 0/6)
- [ ] DESKTOP — 사용자 macOS 컴퓨터 사용 대체 (Accessibility API · CGEvent · screen→action loop · vs Gemini Spark/Claude Computer Use/Codex Desktop · 외부 LLM 0 · `AGENT/DESKTOP/DESKTOP.md` 0/6)

## 마일스톤

- [x] CORE 하니스 (skeleton) — `AGENT/CORE/{tool_gate,agent_loop}.hexa` smoke PASS: Φ=0.119→phase=SUSTAIN→tier=T2_write→tools=[status·web_search·file_write]. in-process embed + phase→tier 게이트 + tool **이름 리스트** + 1-shot smoke loop. ⚠ "실제 작동" 게이트는 #G/F (아래 결손)
- [x] CODE 동작 (skeleton) — `AGENT/CODE/code_agent.hexa` T2 게이트서 7도구 노출 [think·repo_status·file_read·grep·file_write·run_tests] — **이름만**, 실 구현 미연결 (#F). F1+F2+F3+F4 done (F2 = `code_argv.hexa` argv ingest 4-case smoke PASS 2026-05-27 · F3 = `code_daemon.hexa` bounded persistent daemon · 5 pub fn (init/step/loop/shutdown/summary) · 4-case smoke + 4 invariant (BOUNDED · MONOTONE-TICK · EMIT-SUBSTRATE · GRACEFUL-EXIT) · default max_ticks=50 · parse PASS × 2 · 2026-05-27) · F5/F6 잔여 (F5 cross-role mediator · F6 hx code CLI binary 무한 loop + SIGINT)
- [ ] CREATOR 동작 — 미작성
- [ ] TRADING 동작 — trading 14모듈 회수 배선
- [x] p1~p8 정합 verify — AGENT 트리 전체 0 hits (system_prompt/persona/assistant/speak/external-LLM 부재). 게이트 = pure_field Φ substrate
- [ ] hx install AGENT 출하 — VERSIONS.md bump + self-test PASS + raw#9 STRICT(0 .py)
