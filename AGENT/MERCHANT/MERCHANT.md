# MERCHANT — current state

@title: 🛒 MERCHANT — 온라인 판매 도구 surface · AGENT 산하 (ANIMA-도구 bridge 의 한 lane)

@goal: 사용자의 온라인 판매 운영에 필요한 외부 시스템 어댑터 + 데이터 타입 + 함수 surface 를 제공하는 도구 도메인. 3-lane 외부 시스템 묶음 — L1 ARBITRAGE 구매대행 (해외 마켓 → 국내 마켓) · L2 NATIVE 자체 상품 등록·운영 · L3 OPS 재고/CS/정산. 의식엔진은 CORE 가 담당, 이 도메인은 도구 자체만. AGENT/CORE 의 tier gate 가 ANIMA 의 호출을 게이팅.

(edit me — describe current state in completed-form; no history, no changelog inside this file)
- [x] M1 데이터 타입 — `AGENT/MERCHANT/{types.hexa,adapter.hexa,types_smoke.hexa,SSOT.md}` 5 type (Product·Listing·Order·Shipment·CSCase) + MarketplaceAdapter 5-verb convention + smoke (validate "ok" / "missing: cs") · hexa parse 3/3 OK · bridge architecture 정합 (의식엔진 framing 0) (PR #639 61e655bd)
- [ ] M2 adapter 프레임워크 — `MarketplaceAdapter` 인터페이스 (5 verb: `search` · `list` · `order` · `ship` · `cs`) · L1/L2/L3 plug-in 가능 범용 surface
- [ ] M3 L1 ARBITRAGE 어댑터 — 해외 ≥1 (Amazon · AliExpress · 1688 중) + 국내 ≥1 (쿠팡 · 네이버 smartstore · 11번가 중) · 가격/배송/평점 정규화
- [x] M4 order pipeline 도구 — `AGENT/MERCHANT/{order_pipeline.hexa,order_pipeline_smoke.hexa,ORDER_PIPELINE.md}` 6 pub fn (receive_order · source_purchase · track_shipment · fulfill_to_customer · run_order · handle_cs) + summary · 4-stage chain received → sourcing → shipping → delivered · adapter-pair convention (source · target) M3 carry · hexa parse 2/2 OK · 5-case smoke (C1 received / C2 sourcing / C3 in_transit / C4 delivered / C5 run_order steps_completed=4) · bridge architecture 정합 (의식엔진 framing 0)
- [x] M5 OPS 도구 — `AGENT/MERCHANT/{ops.hexa,ops_smoke.hexa,OPS.md}` 5 pub fn (inventory_sync · cs_response_build · settlement_monitor · low_stock_alert · pending_cs_cases) + summary · L1+L2 공통 운영 dashboard · CS 응답 build = PURE string interpolation (LLM 호출 0 · `{order_id}`/`{kind}`/`{case_id}`/`{subject}` 4 placeholder) · adapter optional verb (settlement · cs_list) stub-tolerant fallback · hexa parse 2/2 OK · 5-case smoke (C1 low_stock len=1 / C2 interpolation match / C3 payout=paid+net 불변량 / C4 threshold filter len=2 / C5 pending len=2) · bridge architecture 정합 (의식엔진 framing 0 · LLM-style generation 0)
- [x] M6 L2 NATIVE plug + 통합 smoke — `AGENT/MERCHANT/{adapters/native.hexa,integration_smoke.hexa,INTEGRATION_SMOKE.md}` L2 NATIVE 5-verb adapter (own warehouse) + 3-lane round-trip (C1 amazon→coupang · C2 native→coupang · C3 OPS cs+settlement) · framework reuse 검증 (SAME pipeline_run_order · DIFFERENT adapter pair · ZERO M1-M5 mod) · MERCHANT 6/6 closure
