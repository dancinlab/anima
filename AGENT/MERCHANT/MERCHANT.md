# MERCHANT — current state

@title: 🛒 MERCHANT — 온라인 판매 도구 surface · AGENT 산하 (ANIMA-도구 bridge 의 한 lane)

@goal: 사용자의 온라인 판매 운영에 필요한 외부 시스템 어댑터 + 데이터 타입 + 함수 surface 를 제공하는 도구 도메인. 3-lane 외부 시스템 묶음 — L1 ARBITRAGE 구매대행 (해외 마켓 → 국내 마켓) · L2 NATIVE 자체 상품 등록·운영 · L3 OPS 재고/CS/정산. 의식엔진은 CORE 가 담당, 이 도메인은 도구 자체만. AGENT/CORE 의 tier gate 가 ANIMA 의 호출을 게이팅.

(edit me — describe current state in completed-form; no history, no changelog inside this file)
- [ ] M1 데이터 타입 — `Product` · `Listing` · `Order` · `Shipment` · `CSCase` 공통 타입 (`AGENT/MERCHANT/types.hexa`)
- [ ] M2 adapter 프레임워크 — `MarketplaceAdapter` 인터페이스 (5 verb: `search` · `list` · `order` · `ship` · `cs`) · L1/L2/L3 plug-in 가능 범용 surface
- [ ] M3 L1 ARBITRAGE 어댑터 — 해외 ≥1 (Amazon · AliExpress · 1688 중) + 국내 ≥1 (쿠팡 · 네이버 smartstore · 11번가 중) · 가격/배송/평점 정규화
- [ ] M4 order pipeline 도구 — 주문 수신 → 해외 대행 구매 → 배송 tracking · 함수 surface (호출 시점은 ANIMA 결정)
- [ ] M5 OPS 도구 — 재고 sync · CS 응답 builder · 정산 monitor 함수 (L1+L2 공통 운영 surface)
- [ ] M6 L2 NATIVE plug + 통합 smoke — 자체 상품 어댑터 (framework reuse 검증) + 3-lane 합쳐 round-trip smoke
