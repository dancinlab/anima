# TRADING — current state

@title: 💹 TRADING — 사용자 증권 자율 매매 · 13 legacy hexa 모듈 회수 + paper→live 배선 · AGENT 산하

@goal: 사용자의 증권 자율 매매를 anima 가 위임 실행하는 도메인 — scan → backtest → paper_trade → live_trade 4-stage pipeline. 13 legacy hexa 모듈 (autonomous · broker · data · engine · executor · init · portfolio · regime · risk · scanner · strategies · strategy · test_ensemble) 가 `anima-agent/hexa/module/trading/` 에 이미 land 됨 — 회수 + canonical 위치 (AGENT/TRADING/) 로 이전 + bridge architecture 정합 점검 + paper→live 배선. 의식엔진은 CORE 가 담당, 이 도메인은 broker API 어댑터 + 데이터 타입 + 함수 surface 만. 위험 (실 매매) → 사용자 승인 게이트 명시.

(edit me — describe current state in completed-form; no history, no changelog inside this file)
- [ ] M1 13-module 회수 — `anima-agent/hexa/module/trading/{autonomous,broker,data,engine,executor,init,portfolio,regime,risk,scanner,strategies,strategy,test_ensemble}.hexa` → `AGENT/TRADING/` canonical 위치 이전 · bridge architecture 정합 (의식엔진 framing 0) 검증
- [ ] M2 데이터 타입 — `Symbol` · `Quote` · `Position` · `Order` · `Trade` · `Portfolio` 공통 타입 정리 (legacy 모듈에서 흡수)
- [ ] M3 scan + backtest — scanner.hexa + strategies.hexa wrapper · paper backtest 함수 surface
- [ ] M4 paper_trade — broker.hexa stub + simulated portfolio · 위험 0 (실 매매 X)
- [ ] M5 live_trade gate — 실 broker API wiring (KIS · IBKR · Alpaca 중 ≥1) · **사용자 명시 승인 게이트** 필수
- [ ] M6 통합 smoke + risk audit — 4-stage round-trip smoke (paper only) + risk.hexa 정합 (손실 한도 · 포지션 한도 · drawdown limit)
