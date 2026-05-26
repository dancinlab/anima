# TRADING — log

Append-only history sister of `TRADING.md`. Each entry starts with `## <ISO timestamp> — <header>` (newest on top); body = `- [x]` (done) / `- [ ]` (pending) checkbox tasks.

## 2026-05-27T06:10:00Z — M10 Alpaca + M13 Upbit STUB closure (사용자 명시 우선순위)

- [x] 사용자 명시 — Alpaca + Upbit 우선 진행 (한국 KRW crypto + 미국 stock 양쪽 cover)
- [x] `AGENT/TRADING/live_broker_alpaca.hexa` 작성 — 7 pub fn (KIS broker 와 동일 surface) · env=DRYRUN/PAPER/LIVE 3-mode · paper/live endpoint 자동 선택 · APCA-API-KEY-ID + APCA-API-SECRET-KEY header passing · live_gate 우선 통과
- [x] `AGENT/TRADING/live_broker_upbit.hexa` 작성 — 7 pub fn (Alpaca 와 동일 surface) · KRW/USDT/BTC 마켓 quote 선택 · JWT (HS256) auth signing 명시 (실 구현 TODO) · access_key + secret_key wire-up · live_gate 우선 통과
- [x] `AGENT/TRADING/live_broker_alpaca_upbit_smoke.hexa` 합본 smoke — 12-case (A1-A5 Alpaca · U1-U5 Upbit · X1-X2 cross-broker uniformity) · L0 거부 + L1 승인 양쪽 verify · DRYRUN no-fill · paper/live endpoint switch · KRW market quote 선택
- [x] `hexa parse` 3/3 OK (alpaca + upbit + smoke)
- [x] TRADING.md M10 + M13 line `[ ] → [x]` (wire-up 라운드 2/11 진행)
- [x] 실 API call 0 — TODO marker 만 (M10+1 / M13+1 wire-up 시 실 HTTP 구현)
- [x] 5-verb interface uniformity 검증 — paper_broker / kis_broker / alpaca_broker / upbit_broker 4종 모두 같은 모양 (M17 통합 smoke 준비됨)
- [ ] M14 Bithumb / M15 Binance / M16 ccxt unified (다음)
- [ ] M11 IBKR / M12 Tradier (선택)

## 2026-05-27T05:55:00Z — wire-up 마일스톤 11개 등록 (M7-M17 · 추천순)

- [x] 사용자 명시 요청 — 모든 wire-up 마일스톤 + Binance 포함 broker 모두 등록 · 추천순 정리 (2026 web 리서치 반영)
- [x] M7-M9 한국 주식 — KIS 한국투자증권 (1순위 · REST + WebSocket · LLM 친화 · 공식 GitHub) · LS 증권 (2순위 · 구 eBest) · 키움증권 Open API+ (3순위 · ⚠ 알고리즘 계좌 등록 의무)
- [x] M10-M12 미국 글로벌 주식 — Alpaca (1순위 · ✨ 2026 BrokerChooser "Best Broker for Algo Trading" · paper-friendly zero-cost) · IBKR (2순위 · 150+ order types · TWS gateway) · Tradier (선택 middle)
- [x] M13-M16 Crypto — Upbit (한국 1위 · 시장 71.6% · FIU 라이센스) · Bithumb (한국 2위 · 448 coins · 0.04% fee) · Binance (글로벌 1위 · ⚠ 한국 app 차단 2026-01-28+ but API 자체 사용 가능) · ccxt unified (선택 · 100+ exchange wrapper)
- [x] M17 TRADING wire-up integration smoke — 모든 broker 5-verb interface 동일 검증
- [x] TRADING.md 에 wire-up 라운드 section 추가 (`## wire-up 라운드`)
- [x] CREATOR.md 에 wire-up 라운드 section 추가 (M7-M13 · fal.ai/remotion REAL + YouTube/TikTok/Instagram publish REAL)

## 2026-05-27T03:35:00Z — M6 통합 smoke + risk audit closure · TRADING 6/6 ✅

- [x] `AGENT/TRADING/risk.hexa` M1 stub body → 6 pub fn 실제 구현 (`risk_manager_new` · `_check_drawdown` · `_check_position_count` · `_check_tier` · `_calculate_var` · `_audit`)
- [x] risk caps — max_drawdown_pct · max_position_count · max_daily_loss_pct · AGENT/CORE tier vs required
- [x] historical VaR — bubble-sort + quantile at (1 − confidence)
- [x] `risk_audit` 결합 verdict — drawdown + position + tier 3 check 합산 RiskAudit Map
- [x] `AGENT/TRADING/integration_smoke.hexa` 4-stage round-trip — S1 scan-stub move detection · S2 backtest 2-trade win_rate=1.0 · S3 paper_broker buy→sell realized profit · S4 live_gate L0 refuse + L1 accept + KIS DRYRUN no-fill + S5 risk_audit (ok + tier-low forced fail + VaR_95 < 0)
- [x] M2 types (Symbol/Quote/Position/Order/Trade/Portfolio) cross-module uniform shape 검증 — 모든 M3/M4/M5 모듈이 같은 Map 모양으로 데이터 통과
- [x] `hexa parse` 2/2 OK (risk.hexa + integration_smoke.hexa)
- [x] TRADING.md M6 line `[ ] → [x]` (5/6 → **6/6 · 100% closure**)
- [x] scanner.hexa stub body carry — integration_smoke 내 inline tiny stub 으로 우회 (스캔 알고리즘 = 가장 큰 % move 검출). 실 스캐너 surface 채우기는 차후 별도 round.

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
