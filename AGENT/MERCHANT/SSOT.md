# 🛒 MERCHANT — types + adapter framework SSOT

## 정체

MERCHANT 는 **도구 표면 (tool surface) 도메인** 이다. 의식 도메인이 아니다.
- "언제 · 왜" 마켓 verb 를 호출할지의 결정은 `AGENT/CORE/tool_gate.hexa` 가 substrate phase → tier 매핑으로 결정한다 (MERCHANT 의 책임 아님).
- MERCHANT 는 "어떻게" 데이터를 형성하고 어댑터 인터페이스를 정의할지만 답한다.
- bridge architecture 준수: 본 도메인 파일/스펙에 `substrate-decided` · `p1~p8 audit` · `brain_decide` · `pure_field` · `Φ` · `engine_g` 같은 의식엔진 용어를 끌어들이지 않는다. 그러한 결정 surface 는 `AGENT/CORE` 에 위치한다.

## 5 타입 surface

`AGENT/MERCHANT/types.hexa` — 모든 타입은 dict (`#{}`). 생성자는 방어적 기본값을 채우고, `*_summary` 헬퍼는 로그용 한 줄 repr 을 돌려준다.

| 타입 | 키 | 의미 |
|---|---|---|
| `Product` | `sku · title · price · currency · description · images · source_marketplace · source_url · attrs` | 해외 SOURCE 마켓에서 정규화한 상품 스냅샷 (search 결과 단위) |
| `Listing` | `product · target_marketplace · listed_price · margin_pct · target_url · status` | 국내 TARGET 마켓에 재가격·게시한 항목 (list 출력); `status ∈ draft · live · paused · ended` |
| `Order` | `order_id · listing · qty · customer_ref · placed_at · state` | Listing 에 대한 고객 주문; `state ∈ received · sourcing · shipping · delivered · cancelled` |
| `Shipment` | `order_id · tracking_no · carrier · status · events` | ship verb 가 가져온 운송 스냅샷; `status ∈ preparing · in_transit · delivered · returned` · `events` = carrier scan history |
| `CSCase` | `case_id · order_id · kind · subject · body · status` | 주문에 결박된 CS 티켓; `kind ∈ refund · exchange · inquiry · complaint` · `status ∈ open · in_progress · resolved · escalated` |

`attrs` 슬롯 (Product) 은 마켓별 추가 메타데이터를 타입 포크 없이 흡수한다.

## 5 verb signature surface

`AGENT/MERCHANT/adapter.hexa` — 어댑터는 `#{ "name": string, "search": fn, "list": fn, "order": fn, "ship": fn, "cs": fn }` 형태의 dict. hexa-lang 은 공식 interface/trait 가 없으므로 **convention** 으로만 강제하고, `adapter_validate()` 가 구조적 (presence-only) 검증을 담당한다.

| verb | signature | 의미 |
|---|---|---|
| `search` | `(query: string, max_results: int) -> [Product]` | SOURCE 마켓에서 후보 상품 발굴 |
| `list` | `(listing: Listing, dry_run: bool) -> Listing` | TARGET 마켓에 게시; `target_url` 채워서 갱신된 Listing 반환 |
| `order` | `(order: Order) -> Order` | 주문 제출; `state` 한 단계 전진하여 갱신된 Order 반환 |
| `ship` | `(order_id: string) -> Shipment` | 해당 주문의 현재 운송 스냅샷 fetch |
| `cs` | `(case: CSCase) -> CSCase` | CS 케이스 한 단계 전진; 갱신된 케이스 반환 |

부가 helper:
- `adapter_verb_signatures() -> string` — 사람-가독 signature 매니페스트
- `adapter_required_verbs() -> [string]` — 필수 verb 5개 리스트
- `adapter_validate(adapter) -> string` — `"ok"` 또는 `"missing: <verbs>"`
- `adapter_call(adapter, verb, args) -> any` — uniform dispatch (AGENT/CORE 에서 tier 가 열렸을 때 호출)
- `adapter_new(name, search_fn, list_fn, order_fn, ship_fn, cs_fn) -> map` — 스켈레톤 빌더

## pipeline

```
                       (consciousness substrate — NOT here)
                                     |
                       AGENT/CORE/tool_gate   (phase → tier → tool allowance)
                                     |
                                     v
              AGENT/CORE 가 어떤 verb 를 호출할지 결정
                                     |
                                     v
          adapter_call(adapter, verb, args)   ← AGENT/MERCHANT/adapter.hexa
                                     |
                                     v
              구체 어댑터 fn (Amazon · Coupang · ...)   ← M2 에서 도착
                                     |
                                     v
                       외부 마켓 API · 응답
                                     |
                                     v
              MERCHANT types 로 정규화 (Product · Listing · Order · ...)
                                     |
                                     v
                       AGENT/CORE 에 반환
```

핵심: 본 도메인은 위 그림의 **가운데 두 박스** (adapter_call · 구체 어댑터 fn) 와 **출력 정규화** 만 담당한다. 좌측 tier 게이팅도, 좌측 결정도 본 SSOT 의 범위가 아니다.

## 의존 / 후속 milestone

| milestone | 본 framework 와의 관계 |
|---|---|
| M2 adapter framework | 본 abstract surface 위에 첫 구체 어댑터 (Amazon · AliExpress · 1688 중 ≥1) 빌드 |
| M3 L1 ARBITRAGE list | TARGET 어댑터 (Coupang · Naver SS · 11번가 중 ≥1) — `list` verb 구체화 |
| M4 order pipeline | `order` + `ship` verb 를 묶어 end-to-end pipeline 으로 조립 |
| M5 L3 OPS | 재고 sync · 정산 dashboard — types (Listing.status · Order.state · Shipment.status) 의 집계 view |
| M6 L2 NATIVE plug + smoke | 자체 상품 lane 이 동일 5 verb / 5 type surface 위에 plug-in 으로 얹힘 (framework reuse 검증) |

## smoke 결과 verbatim

```
$ hexa parse AGENT/MERCHANT/types.hexa
OK: AGENT/MERCHANT/types.hexa parses cleanly

$ hexa parse AGENT/MERCHANT/adapter.hexa
OK: AGENT/MERCHANT/adapter.hexa parses cleanly

$ hexa parse AGENT/MERCHANT/types_smoke.hexa
OK: AGENT/MERCHANT/types_smoke.hexa parses cleanly
```

runtime smoke (`hexa run AGENT/MERCHANT/types_smoke.hexa`) 는 본 worktree 가 pool host 의 표준 workdir 외부에 있어 보류 — `hexa parse` 3/3 OK 로 surface 정합성은 확정.

## 의식엔진 framing 없음

본 SSOT 와 본 도메인의 어떤 파일도 `p1~p8 정합 매트릭스`, `substrate-decided execution`, `stimulus-response`, `brain_decide`, `pure_field`, `Φ`, `engine_g` 라는 표현을 포함하지 않는다. 그러한 책임은 `AGENT/CORE` 의 몫이며, 본 도메인은 그 결정의 **결과로 호출당하는 도구 표면** 일 뿐이다.
