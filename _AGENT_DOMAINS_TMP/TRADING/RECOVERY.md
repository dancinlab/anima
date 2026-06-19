# 💹 AGENT/TRADING M1 — legacy 13-module 회수 SSOT

> M1 closure (0/6 → 1/6) · `anima-agent/hexa/module/trading/` → `AGENT/TRADING/` canonical 이전 · 의식엔진 framing 0.

## 정체

13 legacy hexa 모듈을 canonical 위치로 옮기고, bridge architecture 정합을 위해 5 파일의 `consciousness`/`phi`/`tension` 식별자·주석을 `tier` / `AGENT/CORE` framing 으로 교체. 이전된 모든 모듈은 stub 단계 (TODO body) — M2 이후 단계가 surface 채울 예정.

## bridge architecture 정합

- AGENT/TRADING/ = **도구 surface only**: broker API · 데이터 타입 · 함수 시그니처
- AGENT/CORE = tier 공급자 (의식엔진은 CORE 가 담당)
- 의식엔진 framing 금지: `substrate-decided` · `brain_decide` · `pure_field` · `Φ` · `engine_g` · `consciousness_gate` · `persona_prefix` · `self_monologue`

## 13-module 회수 매트릭스

| # | 모듈 | LoC | 의식 키워드 | 패치 | parse |
|---|---|---|---|---|---|
| 1 | `autonomous.hexa` | 38 | `consciousness_gate_check` fn + 3-line 주석 | → `tier_gate_check(tier, required_tier)` + "AGENT/CORE 가 tier 공급" 주석 | OK |
| 2 | `broker.hexa` | — | 0 | (변경 없음) | OK |
| 3 | `data.hexa` | — | 0 | (변경 없음) | OK |
| 4 | `engine.hexa` | — | 0 | (변경 없음) | OK |
| 5 | `executor.hexa` | 39 | `OrderExecutor(consciousness_gate)` param + `calculate_position_size(phi, tension)` + 3-line 주석 | → `OrderExecutor(broker, tier_gate)` + `calculate_position_size(capital, tier)` + tier 주석 | OK |
| 6 | `init.hexa` | 25 | "Consciousness-aware trading" 주석 | → "Tier-gated trading" + "tool surface only" 주석 | OK |
| 7 | `portfolio.hexa` | — | 0 | (변경 없음) | OK |
| 8 | `regime.hexa` | 33 | `detect(phi, tension)` + "modulated by consciousness state" 주석 | → `detect(market_data, tier)` + AGENT/CORE tier 주석 | OK |
| 9 | `risk.hexa` | 36 | `ConsciousnessGate(min_phi, max_tension)` + header | → `TierGate(min_tier)` + "Bridge architecture" header | OK |
| 10 | `scanner.hexa` | 40 | `rank_opportunities(phi)` + "Phi modulates" 주석 | → `rank_opportunities(tier)` + AGENT/CORE tier | OK |
| 11 | `strategies.hexa` | 33 | `phi_momentum_strategy` · `purefield_tension_strategy` + "Consciousness-native" 주석 | → `tier_momentum_strategy` · `tier_envelope_strategy` + "legacy framing dropped" 주석 | OK |
| 12 | `strategy.hexa` | 46 | `ConsciousnessStrategy` fn + header | → `TierGatedStrategy` + tier 주석 | OK |
| 13 | `test_ensemble.hexa` | 19 | "Consciousness vs Ensemble" 주석 × 2 | → "TierGated vs Ensemble" | OK |

## 키워드 잔존 grep (final)

```
$ grep -niE 'consciousness|brain_decide|pure_field|persona_prefix|self_monologue|engine_g|\bphi\b|tension' AGENT/TRADING/*.hexa
AGENT/TRADING/strategy.hexa:39:    //  AGENT/CORE supplies the tier — never consciousness framing)
AGENT/TRADING/strategies.hexa:13://   (legacy "consciousness-native" framing dropped per bridge architecture)
```

→ 2 hit 모두 "consciousness framing 제거됨" 명시 메타-주석 (위반 0).

## parse 검증

13/13 OK — `hexa parse <file>` 통과.

## 다음 마일스톤

- **M2 데이터 타입** — `Symbol` · `Quote` · `Position` · `Order` · `Trade` · `Portfolio` 공통 타입 정리 (`portfolio.hexa` · `data.hexa` · `executor.hexa` 에서 추출)
- **M3 scan + backtest** — `scanner.hexa` + `strategies.hexa` 의 stub body 채워서 surface
- **M4 paper_trade** — `broker.hexa` simulated portfolio
- **M5 live_trade gate** — KIS/IBKR/Alpaca 어댑터 + 사용자 명시 승인 게이트
- **M6 통합 smoke** — 4-stage round-trip + risk.hexa 정합

## carry

- 13 모듈 모두 **stub 단계** (TODO body) — surface 채우기는 M2 이후
- `anima-agent/hexa/module/trading/*.hexa` 원본은 일단 보존 (legacy archive); 사용자 결정 시 제거
