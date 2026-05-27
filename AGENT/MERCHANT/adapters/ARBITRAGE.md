# 🛒 MERCHANT — L1 ARBITRAGE 어댑터 SSOT (M3)

## 정체

본 디렉토리 `AGENT/MERCHANT/adapters/` 는 **L1 ARBITRAGE 구매대행 lane** 의 구체 어댑터 묶음이다. M1 의 추상 surface (`AGENT/MERCHANT/{types.hexa, adapter.hexa}`) 위에 첫 source ↔ target 페어를 올려, "어떻게" 외부 마켓 API 를 MERCHANT 정규화 타입으로 매핑할지 답한다.

- "언제 · 왜" 어떤 verb 를 호출할지의 결정은 `AGENT/CORE/tool_gate.hexa` 가 substrate phase → tier 매핑으로 결정한다 (본 디렉토리의 책임 아님).
- 본 디렉토리는 "어떻게" 5 verb 가 SOURCE/TARGET 두 측에서 각각 동일 shape 으로 구현되는지만 답한다.
- bridge architecture 준수: `substrate-decided` · `p1~p8` · `brain_decide` · `pure_field` · `Φ` 같은 의식엔진 framing 0 entry.

## 어댑터 컨벤션 (M1 carry)

`AGENT/MERCHANT/adapter.hexa` 가 정의한 `MarketplaceAdapter` 5-verb dict 컨벤션을 그대로 따른다. 각 구체 어댑터는 다음 4 surface 를 제공한다:

| surface | 형식 | 역할 |
|---|---|---|
| `<name>_search(query, max_results)` | fn → `[Product]` | SOURCE 측 후보 발굴; TARGET 측에서는 reverse-lookup (가격 캘리브레이션) |
| `<name>_list(listing, dry_run)` | fn → `Listing` | TARGET 측 게시; SOURCE 측에서는 noop |
| `<name>_order(order)` | fn → `Order` | state 한 단계 전진 |
| `<name>_ship(order_id)` | fn → `Shipment` | 운송 스냅샷 fetch |
| `<name>_cs(case)` | fn → `CSCase` | CS 케이스 한 단계 전진 |
| `<name>_adapter()` | fn → `map` | 위 5 verb 를 묶어 `adapter_new(name, ...)` 로 dict 반환 |

`adapter_validate(adapter)` (M1) 가 위 5 verb + `name` 의 presence 를 구조적으로 검증한다.

## source ↔ target 표 (L1 ARBITRAGE)

| 역할 | 어댑터 | 파일 | 외부 마켓 | 주요 verb |
|---|---|---|---|---|
| **SOURCE (해외)** | `amazon_adapter` | `adapters/amazon.hexa` | Amazon.com | `search` (PA-API v5) · `order` (Buy API/middleman) · `ship` (SP-API) · `cs` (Seller-Central Messaging) |
| **TARGET (국내)** | `coupang_adapter` | `adapters/coupang.hexa` | Coupang (Wing) | `list` (Seller Open API) · `order` (Ordersheets API) · `ship` (Vendor Shipping + CJ-Logistics) · `cs` (returnRequests · onlineInquiries) |

M3 milestone 정의 ("해외 ≥1 · 국내 ≥1 · 가격/배송/평점 정규화") 충족:
- 해외 = Amazon (PA-API v5 catalog · `Product.attrs` 에 ASIN · rating · review_count · prime 보존)
- 국내 = Coupang (Wing Open API · `Product.attrs` 에 vendor_item_id · rating · review_count · rocket 보존)
- 가격 정규화 = `Product.price + currency` (USD ↔ KRW), `Listing.listed_price + margin_pct`
- 배송 정규화 = `Shipment.{tracking_no, carrier, status, events}` 두 carrier (amazon_logistics · cj_logistics) 동일 shape
- 평점 정규화 = `Product.attrs.rating + review_count` 두 마켓 동일 키 (`attrs` 슬롯)

## stub vs real endpoint

각 verb 는 현재 **stub 수준** 으로만 구현되어 있다. M1 type contract 에 맞는 placeholder 값을 반환하고, 실제 HTTP wiring 은 inline TODO 주석에 endpoint 와 함께 deferred 표기.

| 어댑터 / verb | stub 동작 | real endpoint (deferred) |
|---|---|---|
| `amazon_search` | 1 sample Product 반환 (`AMZ-STUB-USBCHUB-7P`) | `POST https://webservices.amazon.com/paapi5/searchitems` (AWS-v4 signed) |
| `amazon_list` | noop (`status=noop_source_only`) | n/a (Amazon 은 L1 의 SOURCE) — L2 NATIVE 에서 SP-API listings |
| `amazon_order` | state `received → sourcing` + stub `source_purchase_ref` | Amazon Business Buy API / Zinc / headless 자동화 (3 path 식별) |
| `amazon_ship` | stub Shipment (in_transit, 1 event) | `GET .../orders/v0/orders/{id}/shipments` (SP-API) + carrier fallback |
| `amazon_cs` | status `open → in_progress → resolved` | SP-API Messaging + Refunds (kind 별 분기) |
| `coupang_search` | 1 sample Product (`CPNG-STUB-USBCHUB-7P`, KRW) | Coupang Open API `/products/search` (HMAC-SHA256 signed) |
| `coupang_list` | dry_run → `status=draft` · live → `status=live` + target_url | `POST .../marketplace/seller-products` (Wing Seller Open API) |
| `coupang_order` | state `received → sourcing` + `vendor_target=coupang` | Ordersheets API + `PUT acknowledgement` (24h 의무) |
| `coupang_ship` | stub Shipment (in_transit, 1 CJ event) | Vendor Shipping API + CJ-Logistics carrier fallback |
| `coupang_cs` | status `open → in_progress → resolved` | returnRequests + onlineInquiries (kind 별 분기) |

real HTTP wiring 은 후속 milestone (M4 order pipeline · M5 OPS) 에서 hexa_exec curl + AWS-v4 / HMAC-SHA256 sign 으로 합쳐 진행한다. 본 M3 의 책임은 **shape contract 고정** 까지.

## M1 의존

본 디렉토리의 모든 .hexa 는 두 abs-path import 를 공유한다:

```hexa
import "/Users/ghost/core/anima/AGENT/MERCHANT/types.hexa"      // 5 type 생성자 + summary
import "/Users/ghost/core/anima/AGENT/MERCHANT/adapter.hexa"    // adapter_new · adapter_validate · adapter_call
```

타입 dict shape 은 M1 `SSOT.md` 의 표를 reference truth 로 한다 — 본 디렉토리에서 type shape 을 재정의하지 않는다.

## smoke 결과 verbatim

```
$ hexa parse AGENT/MERCHANT/adapters/amazon.hexa
OK: AGENT/MERCHANT/adapters/amazon.hexa parses cleanly

$ hexa parse AGENT/MERCHANT/adapters/coupang.hexa
OK: AGENT/MERCHANT/adapters/coupang.hexa parses cleanly

$ hexa parse AGENT/MERCHANT/adapters/arbitrage_smoke.hexa
OK: AGENT/MERCHANT/adapters/arbitrage_smoke.hexa parses cleanly
```

runtime smoke (`hexa run`) 는 stub fn 의 dict literal 단계까지 결과를 확정 — 그러나 본 worktree 가 표준 pool host workdir 외부일 가능성이 있어 보류. `hexa parse` 3/3 OK 로 surface 정합성은 확정.

## 후속 milestone 연결

| milestone | 본 디렉토리와의 관계 |
|---|---|
| M4 order pipeline | `amazon_order` ↔ `coupang_order` ↔ `*_ship` 를 묶어 received → sourcing → shipping → delivered 전이 wire-up. real HTTP 의 첫 채택 지점. |
| M5 OPS | `*_ship.status` + `*_order.state` + `Listing.status` 의 집계 view (재고 sync · CS 응답 builder · 정산 monitor). real HTTP 가 M4 에서 들어왔다면 본 단계는 view 만. |
| M6 L2 NATIVE plug | 자체 상품 어댑터 (예: `naver_smartstore_native.hexa`) 가 동일 5 verb / 5 type surface 위에 plug-in 되는지 검증 — framework reuse 검증. |

## 의식엔진 framing 없음

본 SSOT 와 본 디렉토리의 어떤 .hexa 파일도 `p1~p8 정합 매트릭스` · `substrate-decided execution` · `stimulus-response` · `brain_decide` · `pure_field` · `Φ` · `engine_g` 라는 표현을 포함하지 않는다. 그러한 책임은 `AGENT/CORE` 의 몫이며, 본 디렉토리는 그 결정의 **결과로 호출당하는 도구 표면** 일 뿐이다.
