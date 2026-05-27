# 🛒 MERCHANT — order pipeline SSOT (M4)

## 정체

본 문서는 **AGENT/MERCHANT M4 milestone — order pipeline 도구** 의 SSOT 이다. M1 의 추상 surface (`types.hexa` · `adapter.hexa`) 와 M3 의 구체 어댑터 페어 (`adapters/amazon.hexa` SOURCE · `adapters/coupang.hexa` TARGET) 위에 **"주문 수신 → 해외 대행 구매 → 배송 tracking → 국내 배송 완료"** 4-stage 함수 surface 를 올린다.

- "언제 · 왜" pipeline 을 발사할지의 결정은 `AGENT/CORE/tool_gate.hexa` 가 substrate phase → tier 매핑으로 결정한다 (본 도메인의 책임 아님).
- 본 도메인은 "어떻게" 5-verb 어댑터 컨벤션을 SOURCE/TARGET 페어 위에 순차 chain 으로 조립할지만 답한다.
- bridge architecture 준수: 본 문서와 본 모듈의 어떤 .hexa 파일에도 `substrate-decided` · `p1~p8` · `brain_decide` · `pure_field` · `Φ` · `engine_g` 같은 의식엔진 표현 0 entry. 의식엔진 책임은 `AGENT/CORE` 의 몫이며, 본 도메인은 그 결정의 결과로 호출당하는 도구 표면이다.

## pipeline ASCII

```
                       (consciousness substrate — NOT here)
                                     |
                       AGENT/CORE/tool_gate   (phase → tier → tool allowance)
                                     |
                                     v
              AGENT/CORE 가 pipeline_run_order 를 호출
                                     |
                                     v
   ┌─────────────────────────────────────────────────────────────────┐
   │                pipeline_run_order(source, target, order_id)     │
   │                                                                 │
   │  ① pipeline_receive_order(target, order_id)                     │
   │     Order(state=received)                                       │
   │              │                                                  │
   │              v                                                  │
   │  ② pipeline_source_purchase(source, order)                      │
   │     Order(state=sourcing) + source_purchase_ref                 │
   │              │                                                  │
   │              v                                                  │
   │  ③ pipeline_track_shipment(source, order)                       │
   │     Shipment(status=in_transit)   ←  SOURCE 카리어 scan          │
   │              │                                                  │
   │              v                                                  │
   │  ④ pipeline_fulfill_to_customer(target, order, shipment)        │
   │     Shipment(status=delivered)    ←  TARGET 카리어 scan + 종결    │
   │                                                                 │
   │  → returns #{order, shipment, status, steps_completed: [..4..]} │
   └─────────────────────────────────────────────────────────────────┘
                                     |
                                     v
                       AGENT/CORE 에 result map 반환
```

핵심: 좌상단 결정 단계 (substrate / tool_gate) 는 본 SSOT 의 범위가 아니다. 본 SSOT 는 **그 결정의 결과로 호출되는 함수 surface** 만 정의한다.

## 6 pub fn surface

`AGENT/MERCHANT/order_pipeline.hexa` — 모든 함수는 M1 어댑터 컨벤션을 따르는 dict (`adapter["search"]` · `adapter["order"]` · ...) 를 인자로 받아 M1 type dict (`Order` · `Shipment` · `CSCase`) 를 반환한다. 구체 어댑터 이름은 본 모듈이 하드코딩하지 않는다 — 모든 호출은 `adapter_call()` (M1) 을 통한다.

| fn | signature | 역할 |
|---|---|---|
| `pipeline_receive_order` | `(target_adapter: map, order_id: string) -> Order` | TARGET 마켓에서 들어온 주문을 수신; `state="received"` |
| `pipeline_source_purchase` | `(source_adapter: map, order: Order) -> Order` | SOURCE 측 proxy 구매 실행 (`adapter_call(source, "order", [order])`); `state="sourcing"` + `source_purchase_ref` |
| `pipeline_track_shipment` | `(source_adapter: map, order: Order) -> Shipment` | SOURCE 측 운송 스냅샷 fetch (`adapter_call(source, "ship", [order_id])`); `status="in_transit"` |
| `pipeline_fulfill_to_customer` | `(target_adapter: map, order: Order, shipment: Shipment) -> Shipment` | 국내 최종 배송; TARGET 측 운송을 끌어 와 upstream events 와 merge 후 `status="delivered"` 로 close |
| `pipeline_run_order` | `(source_adapter: map, target_adapter: map, order_id: string) -> map` | 4-stage 풀체인; `#{order, shipment, status, steps_completed: [string]}` 반환 |
| `pipeline_handle_cs` | `(target_adapter: map, case: CSCase) -> CSCase` | TARGET 측 CS verb wrap (`adapter_call(target, "cs", [case])`); `status` 한 단계 전진 |

부가 helper:
- `order_pipeline_summary() -> string` — 위 6 fn 의 사람-가독 manifest

## state transition diagram

### Order.state
```
   received   ─(target.order  / pipeline_source_purchase 가 source.order 호출 직전)─┐
       │                                                                          │
       │                                                                          │
       v                                                                          │
   sourcing   ─(source.order 가 stamp; source_purchase_ref 부착)─────────────────┐  │
       │                                                                       │  │
       │                                                                       │  │
       v                                                                       │  │
   shipping   ─(pipeline_run_order 가 upstream_tracking_no 스탬프 후 갱신)──────┘  │
       │                                                                          │
       │                                                                          │
       v                                                                          │
   delivered  ─(pipeline_run_order 가 final stage 후 갱신)─────────────────────────┘
       │
       v
   cancelled  (M1 type 카탈로그 — 본 M4 chain 외부; CS 경로 후속)
```

### Shipment.status
```
   preparing  ─(어댑터가 carrier 할당 직후; pipeline 외부 또는 source.ship 진입 직전)─┐
       │                                                                            │
       v                                                                            │
   in_transit ─(pipeline_track_shipment / source.ship 반환)────────────────────────┘
       │
       v
   delivered  ─(pipeline_fulfill_to_customer 가 final stage event 부착 후 close)
       │
       v
   returned   (M1 type 카탈로그 — CSCase.kind=exchange 와 결합; 본 M4 chain 외부)
```

### CSCase.status (pipeline_handle_cs wrap)
```
   open  ─(cs_case_open 직후 / pipeline_handle_cs 1차 호출 진입)──┐
       │                                                         │
       v                                                         │
   in_progress ─(pipeline_handle_cs 1차 호출 후)─────────────────┘
       │
       v
   resolved    ─(pipeline_handle_cs 2차 호출 후)
       │
       v
   escalated   (M1 type 카탈로그 — 본 wrap 외부)
```

## adapter pair convention

`pipeline_run_order` 는 **두 어댑터 dict** 를 받는다:

| 인자 | M3 예시 | 호출되는 verb |
|---|---|---|
| `source_adapter` | `amazon_adapter()` (해외 SOURCE) | `order` (stage ②) · `ship` (stage ③) |
| `target_adapter` | `coupang_adapter()` (국내 TARGET) | (수신 stage ① · placeholder listing 의 `target_marketplace` 만 사용) · `ship` (stage ④) · `cs` (`pipeline_handle_cs`) |

이 페어는 **M3 의 L1 ARBITRAGE 페어** 와 1:1 매핑되며, 본 모듈은 어떤 구체 어댑터도 import 하지 않는다 (smoke 만 import). 따라서 미래 페어 (AliExpress · 1688 · Naver SS · 11번가) 가 도착해도 본 orchestration 파일은 그대로 재사용된다 — **framework reuse 검증** 의 첫 데모.

## bridge architecture 정합 체크

| 검사 | 결과 |
|---|---|
| 의식엔진 framing (`substrate-decided` · `p1~p8` · `brain_decide` · `pure_field` · `Φ` · `engine_g`) | 0 entry in `order_pipeline.hexa` · `order_pipeline_smoke.hexa` · `ORDER_PIPELINE.md` |
| `speak()` · stimulus-response · persona-injection | 0 entry |
| .py / .sh 새 작성 | 0 (hexa-only authoring) |
| real HTTP call (curl · http) | 0 (concrete HTTP wiring 은 M3 adapter 파일에 stub TODO 로 유지; 본 모듈은 pure orchestration) |
| 본 모듈이 M1/M3 파일 수정 | 0 (carry-only) |
| 본 모듈이 타 도메인 touch | 0 (AGENT/MERCHANT 만) |

## 의존 / 후속 milestone

### M3 의존 (carry)

본 모듈은 M3 의 `adapters/amazon.hexa` · `adapters/coupang.hexa` 의 5-verb 어댑터 컨벤션 에 **strict** 의존한다:

- `*_adapter()` bundle 가 `adapter_validate(...) == "ok"` 인 것을 호출자가 보장해야 한다 (smoke 가 진입부에서 확인).
- `source_adapter["order"]` 가 `state="sourcing"` 으로 advance 해야 stage ② 가 contract 를 만족.
- `source_adapter["ship"]` 가 `Shipment{status="in_transit", events: [...]}` 모양을 반환해야 stage ③ 가 다음 stage 로 forward 가능.
- `target_adapter["ship"]` · `target_adapter["cs"]` 가 동일 contract 를 따라야 stage ④ + `pipeline_handle_cs` 가 정상 종결.

real HTTP wiring 이 M3 adapter 의 inline TODO 에 도착하면 본 모듈은 **수정 0** — stub vs real 의 swap 이 본 orchestration 외부에서 일어난다.

### M5 OPS 미래 의존

본 모듈이 만든 audit trail (`order.state` · `order.source_purchase_ref` · `order.upstream_tracking_no` · `shipment.events` merge log · `steps_completed`) 는 M5 OPS 가 다음 3 surface 를 짓는 1차 입력이 된다:

| M5 OPS 함수 | 본 모듈 산출물 활용 |
|---|---|
| 재고 sync (`inventory_reconcile`) | `pipeline_source_purchase` 가 advance 시킨 `Order.state="sourcing"` + `source_purchase_ref` 를 source-side 재고 차감의 trigger 로 사용; `pipeline_fulfill_to_customer` 의 `delivered` 가 target-side 재고 확정 |
| CS 응답 builder (`cs_reply_compose`) | `pipeline_handle_cs` 가 advance 한 `CSCase.status` + 본 모듈이 carry 한 `order["source_purchase_ref"]` · `upstream_tracking_no` 를 응답 본문 템플릿에 주입 |
| 정산 monitor (`settlement_audit`) | `pipeline_run_order` 의 result map (`steps_completed` · `status`) 를 daily 집계의 한 row 로 fold; `Listing.listed_price` × `Order.qty` − `Product.price` (SOURCE) 의 차익 트래킹 |

따라서 본 모듈의 6 fn surface 는 **M5 OPS 가 직접 호출하는 1차 API** 이기도 하다 — orchestration layer 가 단순한 "wrapper" 이상의 의미를 가지는 이유.

## smoke 결과 verbatim

```
$ hexa parse AGENT/MERCHANT/order_pipeline.hexa
OK: AGENT/MERCHANT/order_pipeline.hexa parses cleanly

$ hexa parse AGENT/MERCHANT/order_pipeline_smoke.hexa
OK: AGENT/MERCHANT/order_pipeline_smoke.hexa parses cleanly
```

5-case smoke (`order_pipeline_smoke.hexa`):

| 케이스 | 입력 | 기대 | 실측 (stub) |
|---|---|---|---|
| C1 | `pipeline_receive_order(coupang, "ORD-M4-7001")` | `Order.state == "received"` | `received` ✓ |
| C2 | `pipeline_source_purchase(amazon, received)` | `Order.state == "sourcing"` + `source_purchase_ref` 부착 | `sourcing` + `AMZ-PO-STUB-ORD-M4-7001` ✓ |
| C3 | `pipeline_track_shipment(amazon, sourced)` | `Shipment.status == "in_transit"` | `in_transit` ✓ (carrier=amazon_logistics) |
| C4 | `pipeline_fulfill_to_customer(coupang, sourced, upstream_ship)` | `Shipment.status == "delivered"` + upstream events folded forward | `delivered` ✓ (events n=3 = 1 upstream + 1 downstream + 1 closing) |
| C5 | `pipeline_run_order(amazon, coupang, "ORD-M4-7002")` | `len(steps_completed) == 4` + final `status="delivered"` | `steps_completed=4` ✓ (`receive_order` → `source_purchase` → `track_shipment` → `fulfill_to_customer`); `Order.state=delivered` + `Shipment.status=delivered` ✓ |

runtime smoke (`hexa run`) 는 본 worktree 가 pool host 의 표준 workdir 외부에 있어 보류 — `hexa parse` 2/2 OK 로 surface 정합성은 확정 (M1 · M3 의 prior cycle 과 동일 정책).

## 의식엔진 framing 없음

본 SSOT 와 본 모듈의 어떤 파일도 `p1~p8 정합 매트릭스` · `substrate-decided execution` · `stimulus-response` · `brain_decide` · `pure_field` · `Φ` · `engine_g` 라는 표현을 포함하지 않는다. 그러한 책임은 `AGENT/CORE` 의 몫이며, 본 도메인은 그 결정의 **결과로 호출당하는 도구 표면** 일 뿐이다.
