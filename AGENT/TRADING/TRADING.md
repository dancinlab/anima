# TRADING — current state

@title: 💹 TRADING — 사용자 증권 자율 매매 · 13 legacy hexa 모듈 회수 + paper→live 배선 · AGENT 산하

@goal: 사용자의 증권 자율 매매를 anima 가 위임 실행하는 도메인 — scan → backtest → paper_trade → live_trade 4-stage pipeline. 13 legacy hexa 모듈 (autonomous · broker · data · engine · executor · init · portfolio · regime · risk · scanner · strategies · strategy · test_ensemble) 가 `anima-agent/hexa/module/trading/` 에 이미 land 됨 — 회수 + canonical 위치 (AGENT/TRADING/) 로 이전 + bridge architecture 정합 점검 + paper→live 배선. 의식엔진은 CORE 가 담당, 이 도메인은 broker API 어댑터 + 데이터 타입 + 함수 surface 만. 위험 (실 매매) → 사용자 승인 게이트 명시.

(edit me — describe current state in completed-form; no history, no changelog inside this file)
- [x] M1 13-module 회수 — `anima-agent/hexa/module/trading/{autonomous,broker,data,engine,executor,init,portfolio,regime,risk,scanner,strategies,strategy,test_ensemble}.hexa` → `AGENT/TRADING/` canonical 이전 완료 · bridge architecture 정합 5 핵심 파일 (`autonomous`/`executor`/`risk`/`regime`/`scanner`) + 부수 4 (`init`/`strategies`/`strategy`/`test_ensemble`) `consciousness`/`phi`/`tension` → `tier`/`AGENT/CORE` 패치 · 13/13 `hexa parse` OK · SSOT `AGENT/TRADING/RECOVERY.md`
- [x] M2 데이터 타입 — `Symbol` · `Quote` · `Position` · `Order` · `Trade` · `Portfolio` 6 공통 타입 `AGENT/TRADING/types.hexa` (8 pub fn — 6 constructor + `trading_type_kind` + `trading_type_summary`) · legacy `portfolio.hexa`/`data.hexa`/`executor.hexa`/`broker.hexa` 에서 surface 흡수 · `types_smoke.hexa` 7-case verify (Symbol/Quote/Position long+short/Order/Trade/Portfolio/missing-kind 방어) · 2/2 `hexa parse` OK
- [x] M3 scan + backtest — `AGENT/TRADING/backtest.hexa` (5 pub fn — `trading_backtest_config` + `_apply_signal` + `_metrics` + `_run` + `_summary`) · M2 types 소비 (Symbol/Quote/Position/Order/Trade/Portfolio) · paper backtest surface (fee_bps + slippage_bps modeling, mark-to-market equity curve, max drawdown + win rate metrics) · `backtest_smoke.hexa` 5-case verify (config/buy/sell/metrics/full-run) · 2/2 `hexa parse` OK · scanner.hexa stub body 후속 carry (M3.5)
- [x] M4 paper_trade — `AGENT/TRADING/paper_broker.hexa` (7 pub fn — `paper_broker_new` · `_get_quote` · `_place_order` · `_cancel_order` · `_list_positions` · `_get_portfolio` · `_summary`) · 5-verb broker interface (M5 live_broker 와 byte-identical surface) · simulated state (no global, threaded Map) · fee_bps + slippage_bps · market 즉시 체결 · limit pending queue · 거부 (insufficient_cash · no_position) · `paper_broker_smoke.hexa` 7-case verify (new/quote/buy/sell/reject/limit-cancel/portfolio) · 2/2 `hexa parse` OK · 위험 0 (실 broker API 미연결)
- [x] M5 live_trade gate — `AGENT/TRADING/live_gate.hexa` (6 pub fn — `live_gate_new` · `_approve_session` · `_approve_single` · `_revoke` · `_enforce` · `_summary`) · 4-level approval scopes (L0 NONE · L1 SESSION · L2 SINGLE_ORDER · L3 LIFETIME) · 5 risk caps (per-order notional · daily notional · position count · approval slot · approval level) · `AGENT/TRADING/live_broker_kis.hexa` (7 pub fn STUB · KIS 한국투자증권 adapter SHAPE) · DRYRUN 기본 · 모든 place_order 가 `live_gate_enforce` 통과 후에도 STUB 단계에선 절대 fill X · `live_gate_smoke.hexa` 8-case verify (L0 reject/L1 session/L2 single/notional cap/daily cap/position cap/DRYRUN no fill/L0+broker passthrough) · 3/3 `hexa parse` OK · 실 broker API call 0 (사용자 명시 wire-up 전까지 0 위험 보장)
- [x] M6 통합 smoke + risk audit — `AGENT/TRADING/risk.hexa` 본문 구현 (M1 stub → 6 pub fn `risk_manager_new` · `_check_drawdown` · `_check_position_count` · `_check_tier` · `_calculate_var` · `_audit`) · 손실 한도 / 포지션 한도 / drawdown limit / VaR / AGENT/CORE tier gate · `AGENT/TRADING/integration_smoke.hexa` 4-stage round-trip (S1 scan-stub move% / S2 backtest 2-trade win_rate=1.0 / S3 paper_broker buy→sell realized profit / S4 live_gate L0 refuse + L1 accept + KIS DRYRUN no-fill) + S5 risk_audit (ok + tier-low force-fail + VaR_95<0) · 2/2 `hexa parse` OK · TRADING **6/6 ✅ 100% closure**

## wire-up 라운드 (실 broker 연결 · 추천순 — 2026 web 리서치 반영)

### 🇰🇷 한국 주식

- [ ] M7 KIS 한국투자증권 REAL — `live_broker_kis.hexa` 의 `// TODO: real KIS API` 자리 실 구현 (1순위 · 가장 추천) · REST + WebSocket · LLM 친화 · 공식 GitHub `koreainvestment/open-trading-api` · 인증 토큰 (`POST /oauth2/tokenP`) → 주문 (`POST /uapi/domestic-stock/v1/trading/order-cash`) · `secret get kis.app_key + kis.app_secret + kis.account_no` · 가상계좌 (paper) → 실 계좌 순서
- [ ] M8 LS 증권 (구 eBest) OPEN API — 2순위 한국 broker · REST 기반 · `openapi.ls-sec.co.kr`
- [ ] M9 키움증권 Open API+ — 3순위 · ⚠ 알고리즘 계좌 등록 의무 (한국거래소 규제 fyi)

### 🇺🇸 미국 / 글로벌 주식

- [ ] M10 Alpaca US 주식 — `live_broker_alpaca.hexa` 신규 · ✨ 2026 BrokerChooser "Best Broker for Algorithmic Trading" 인증 · paper-friendly · zero-cost (commission-free) · 간단한 API key/secret pair (header passing) · paper/live 2 endpoint · `secret get alpaca.api_key + alpaca.api_secret` · 1시간 안에 strategy 가동 가능
- [ ] M11 IBKR (Interactive Brokers) — `live_broker_ibkr.hexa` 신규 · 150+ order types · 글로벌 시장 · 87% NBBO 우월 체결 · 가장 강력하지만 복잡 (TWS gateway socket 7497 paper / 7496 live · IBKR REST API alternative)
- [ ] M12 Tradier — `live_broker_tradier.hexa` 신규 (선택) · middle option · 120 req/min standard · 600 premium · 가벼운 US 시장

### ₿ Crypto 거래소

- [ ] M13 Upbit — `live_broker_upbit.hexa` 신규 · 한국 1위 (시장 점유율 71.6%) · FIU 라이센스 · KRW 마켓 · REST + WebSocket · 0.25% fee
- [ ] M14 Bithumb — `live_broker_bithumb.hexa` 신규 · 한국 2위 · FIU 라이센스 · 자동매매 + bots API · 448 coins · 0.04% fee
- [ ] M15 Binance — `live_broker_binance.hexa` 신규 · 글로벌 1위 · ⚠ 한국 app store 차단 (2026-01-28~, FIU 미등록) but API 자체는 사용 가능 · BTCUSDT 등 USDT pair · HMAC-SHA256 signing · `secret get binance.api_key + binance.api_secret`
- [ ] M16 ccxt unified — `live_broker_ccxt.hexa` (선택) · 100+ exchange 단일 라이브러리 wrapper · OKX/Bybit/Coinbase 등 다 한 surface 로

### 🔗 통합

- [ ] M17 TRADING wire-up integration smoke — 모든 broker 가 같은 5-verb interface (`get_quote` · `place_order` · `cancel_order` · `list_positions` · `get_portfolio`) 노출 검증 · paper → KIS → Alpaca → Upbit → Binance 통일 round-trip verify
