# TRADING — log

Append-only history sister of `TRADING.md`. Each entry starts with `## <ISO timestamp> — <header>` (newest on top); body = `- [x]` (done) / `- [ ]` (pending) checkbox tasks.

## 2026-05-27T03:15:00Z — M5 live_trade gate closure

- [x] `AGENT/TRADING/live_gate.hexa` 작성 — 6 pub fn (`live_gate_new` · `_approve_session` · `_approve_single` · `_revoke` · `_enforce` · `_summary`)
- [x] 4-level approval scopes — L0 NONE (default refuse all) · L1 SESSION · L2 SINGLE_ORDER · L3 LIFETIME (file-backed, M5+1 carry)
- [x] 5 risk caps in enforce — per-order notional · daily cumulative notional · max position count · approval slot 잔량 · approval level
- [x] `AGENT/TRADING/live_broker_kis.hexa` 작성 — 7 pub fn STUB · KIS 한국투자증권 adapter SHAPE (kis_broker_new/_configure/_get_quote/_place_order/_cancel_order/_list_positions/_summary)
- [x] DRYRUN 기본 · 실제 API call 0 · 모든 place_order 가 `live_gate_enforce` 통과 후에도 stub 단계에선 절대 fill 안 함 (would_send order 반환)
- [x] `live_gate_smoke.hexa` 8-case verify — C1 L0 reject · C2 L1 session · C3 L2 single + exhausted · C4 notional cap · C5 daily cap (8 orders 누적) · C6 position cap (buy refused, sell ok) · C7 DRYRUN no-fill · C8 L0 + broker passthrough
- [x] `hexa parse` 3/3 OK
- [x] TRADING.md M5 line `[ ] → [x]` (4/6 → 5/6)
- [x] 위험 0 보장 — 실 broker API 미연결 (사용자 wire-up 전까지) + DRYRUN env 기본 + STUB 단계 fill 차단
- [ ] M6 통합 smoke + risk audit — 4-stage round-trip smoke (paper only) + risk.hexa 정합 (다음 마일스톤)

## 2026-05-27T02:55:00Z — M4 paper_trade closure

- [x] `AGENT/TRADING/paper_broker.hexa` 작성 — 7 pub fn (`paper_broker_new` · `_get_quote` · `_place_order` · `_cancel_order` · `_list_positions` · `_get_portfolio` · `_summary`)
- [x] 5-verb broker interface — M5 live_broker 와 byte-identical surface (place_order/cancel_order/list_positions/get_quote/get_portfolio)
- [x] simulated state — no global, threaded Map (PaperBrokerState · cash + positions + open_orders + trades + fee_bps + slippage_bps + next_order_id)
- [x] market order 즉시 체결 · limit order pending queue · 거부 시 reason 명시 (insufficient_cash · no_position)
- [x] `paper_broker_smoke.hexa` 7-case verify — C1 new · C2 get_quote (bid/ask spread) · C3 buy market · C4 sell market · C5 reject insufficient_cash · C6 limit queue + cancel · C7 portfolio mark-to-market
- [x] `hexa parse` 2/2 OK
- [x] TRADING.md M4 line `[ ] → [x]` (3/6 → 4/6)
- [x] 위험 0 보장 — 실 broker API 미연결, 모든 체결 simulated
- [ ] M5 live_trade gate — 실 broker (KIS/IBKR/Alpaca) + 사용자 명시 승인 게이트 (다음 마일스톤)

## 2026-05-27T02:40:00Z — M3 scan + backtest closure

- [x] `AGENT/TRADING/backtest.hexa` 작성 — paper backtest wrapper 5 pub fn (`trading_backtest_config` · `_apply_signal` · `_metrics` · `_run` · `_summary`)
- [x] M2 types 소비 — Symbol/Quote/Position/Order/Trade/Portfolio 모두 surface 에 통합
- [x] fee_bps + slippage_bps 모델링 (basis points 단위 · realistic broker cost)
- [x] mark-to-market equity curve + max drawdown + win rate metrics
- [x] `AGENT/TRADING/backtest_smoke.hexa` 5-case verify — C1 config · C2 apply_signal buy · C3 apply_signal sell · C4 metrics on synthetic equity curve · C5 full 5-candle run
- [x] `hexa parse` 2/2 OK
- [x] TRADING.md M3 line `[ ] → [x]` (2/6 → 3/6)
- [ ] scanner.hexa stub body 실제 구현 (carry M3.5 또는 M6 통합 smoke 시점)
- [ ] M4 paper_trade — broker.hexa stub + simulated portfolio (다음 마일스톤)

## 2026-05-27T02:25:00Z — M2 데이터 타입 closure

- [x] `AGENT/TRADING/types.hexa` 작성 — 6 canonical 타입 (Symbol · Quote · Position · Order · Trade · Portfolio) + 2 helper (`trading_type_kind` · `trading_type_summary`) = 8 pub fn
- [x] legacy surface 흡수 — `portfolio.hexa` (Position/Portfolio) · `data.hexa` (MarketData) · `executor.hexa` (Order) · `broker.hexa` (Trade)
- [x] `AGENT/TRADING/types_smoke.hexa` 7-case verify — C1 Symbol · C2 Quote spread · C3 Position long/short PnL · C4 Order status · C5 Trade fees · C6 Portfolio equity · C7 missing-kind 방어
- [x] `hexa parse` 2/2 OK
- [x] TRADING.md M2 line `[ ] → [x]` (1/6 → 2/6)
- [ ] M3 scan + backtest (다음 마일스톤)

## 2026-05-27T02:10:00Z — M1 13-module 회수 closure

- [x] 13 .hexa 모듈 `anima-agent/hexa/module/trading/` → `AGENT/TRADING/` canonical 이전 (cp)
- [x] bridge architecture 정합 — 5 핵심 (autonomous · executor · risk · regime · scanner) + 부수 4 (init · strategies · strategy · test_ensemble) `consciousness`/`phi`/`tension` 식별자·주석 → `tier`/`AGENT/CORE` framing
- [x] `hexa parse` 13/13 OK
- [x] RECOVERY.md SSOT (회수 매트릭스 + 키워드 잔존 grep + parse 검증)
- [x] TRADING.md M1 line `[ ] → [x]`
- [ ] M2 데이터 타입 (다음 마일스톤)

## 2026-05-27T01:55:00Z — domain init

- [x] TRADING.md scaffold (6 milestone · 13 legacy module 회수 roadmap)
- [x] DOMAINS.tape register · ./AGENT/TRADING/TRADING.md
- [x] ANIMA.md + AGENT.md 라인 갱신 (clean slate → 0/6)
- [x] 13 legacy module 위치 cite (anima-agent/hexa/module/trading/) — 회수 작업은 M1
- [ ] M1 13-module 회수 (canonical 위치 이전 + bridge architecture 점검)
