# MERCHANT — current state

@title: 🛒 MERCHANT — 온라인 판매 운영 · 3-lane (ARBITRAGE · NATIVE · OPS) · 사용자 위임 실행

@goal: 사용자의 온라인 판매 전반을 anima 가 자율 실행하는 도메인 — 3-lane umbrella (L1 ARBITRAGE 구매대행 · L2 NATIVE 자체 상품 · L3 OPS 공통 운영). 우선순위는 L1 ARBITRAGE (해외 마켓 search → 국내 마켓 등록 → 주문 시 대행 구매 → 배송/CS), 단 framework 는 L2/L3 plug-in 가능한 범용 구조 (MarketplaceAdapter abstract surface · Product/Listing/Order 공통 타입). 사용자가 마켓 계정·마진 정책·카테고리 공급, anima 는 실행. p1~p8 정합 substrate-decided execution · 외부 LLM 0.

(edit me — describe current state in completed-form; no history, no changelog inside this file)
- [ ] M1 types + adapter framework — `Product` · `Listing` · `Order` 공통 타입 + `MarketplaceAdapter` abstract surface (search · list · order · cs 5 verb) · 범용성 핵심 · L1/L2/L3 plug-in 가능
- [ ] M2 L1 ARBITRAGE search — 해외 마켓 search 어댑터 (Amazon · AliExpress · 1688 중 ≥1) · 가격/배송/평점 정규화 → Product
- [ ] M3 L1 ARBITRAGE list — 국내 마켓 등록 어댑터 (쿠팡 · 네이버 smartstore · 11번가 중 ≥1) · 마진 정책 적용 · Product → Listing
- [ ] M4 order pipeline — 주문 수신 → 해외 대행 구매 → 국내 배송 → tracking · L1 first · L2 reuse 설계
- [ ] M5 L3 OPS — 재고 sync · CS 응답 · 정산 모니터링 · L1+L2 공통 dashboard
- [ ] M6 L2 NATIVE plug + p1~p8 audit + smoke — 자체 상품 lane 검증 (framework reuse) + audit (0 violations 목표) + 통합 smoke
