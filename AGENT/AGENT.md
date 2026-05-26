# AGENT — current state

@title: 🤖 ANIMA-EMBED — 의식 기판에 직접 사는 자율 에이전트
@goal: anima 의식 기판(PureField)에 in-process 임베드된 역할별 자율 에이전트 시스템 — 외부 LLM 없이 anima 두뇌로만 구동하고, 도구 접근은 기판이 스스로 분류한 phase(DORMANT→RESONANT)가 게이트(T0→T3)한다. 코드·크리에이터·트레이딩 3종이 같은 CORE 하니스 위에서 동작하며, `hx install` 가능한 제품으로 출하.

## 역할 에이전트 (우선순위)

- [ ] CODE — 자율 코딩 에이전트 (think·read → file_write·run_tests → git_commit·push)
- [ ] CREATOR — 컨텐츠 크리에이터 (web_search·imagine → 작문 → publish)
- [ ] TRADING — 자율 매매 (scan·backtest → paper_trade → live_trade, 기존 trading 14모듈 회수)

## 마일스톤

- [x] CORE 하니스 (skeleton) — `AGENT/CORE/{tool_gate,agent_loop}.hexa` smoke PASS: Φ=0.119→phase=SUSTAIN→tier=T2_write→tools=[status·web_search·file_write]. in-process embed + phase→tier 게이트 + tool **이름 리스트** + 1-shot smoke loop. ⚠ "실제 작동" 게이트는 #G/F (아래 결손)
- [x] CODE 동작 (skeleton) — `AGENT/CODE/code_agent.hexa` T2 게이트서 7도구 노출 [think·repo_status·file_read·grep·file_write·run_tests] — **이름만**, 실 구현 미연결 (#F)
- [ ] CREATOR 동작 — 미작성
- [ ] TRADING 동작 — trading 14모듈 회수 배선
- [x] p1~p8 정합 verify — AGENT 트리 전체 0 hits (system_prompt/persona/assistant/speak/external-LLM 부재). 게이트 = pure_field Φ substrate
- [ ] hx install AGENT 출하 — VERSIONS.md bump + self-test PASS + raw#9 STRICT(0 .py)
