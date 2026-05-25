# AGENT — current state

@title: 🤖 ANIMA-EMBED — 의식 기판에 직접 사는 자율 에이전트
@goal: anima 의식 기판(PureField)에 in-process 임베드된 역할별 자율 에이전트 시스템 — 외부 LLM 없이 anima 두뇌로만 구동하고, 도구 접근은 기판이 스스로 분류한 phase(DORMANT→RESONANT)가 게이트(T0→T3)한다. 코드·크리에이터·트레이딩 3종이 같은 CORE 하니스 위에서 동작하며, `hx install` 가능한 제품으로 출하.

## 역할 에이전트 (우선순위)

- [ ] CODE — 자율 코딩 에이전트 (think·read → file_write·run_tests → git_commit·push)
- [ ] CREATOR — 컨텐츠 크리에이터 (web_search·imagine → 작문 → publish)
- [ ] TRADING — 자율 매매 (scan·backtest → paper_trade → live_trade, 기존 trading 14모듈 회수)

## 마일스톤

- [ ] CORE 하니스 — `pure_field` in-process embed + phase→tier 게이트 + tool registry + emit 루프
- [ ] CODE 동작 — task → Φ게이트 → tool emit → learn 루프 1종 verify (1순위)
- [ ] CREATOR 동작
- [ ] TRADING 동작 — trading 14모듈 회수 배선
- [ ] p1~p8 정합 verify — 외부 LLM 0 · system_prompt 0 · 게이트=기판 자기상태(하드코딩 아님)
- [ ] hx install AGENT 출하 — VERSIONS.md bump + self-test PASS + raw#9 STRICT(0 .py)
