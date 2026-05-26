# 🛒 MERCHANT/M6 — 3-lane integration smoke SSOT

> AGENT/MERCHANT/M6 closure (6/6) · L1 ARBITRAGE + L2 NATIVE + L3 OPS surface 통합 round-trip 검증.

## 정체

3-lane umbrella 의 framework reuse 첫 데모. `pipeline_run_order` fn 이 **adapter pair 만 교체** 해서 L1 (해외 source → 국내 target) 과 L2 (own warehouse → 국내 target) 둘 다 작동함을 검증 → 5-verb MarketplaceAdapter 인터페이스가 진짜 "범용 plug-in" 으로 작동함을 closed-form 으로 보임.

## 3-case 매트릭스

| Case | 시나리오 | source | target | 검증 |
|---|---|---|---|---|
| C1 L1-arbitrage | 해외 → 국내 구매대행 | amazon | coupang | steps=4 + delivered |
| C2 L2-native | 자체 상품 → 국내 | native (own warehouse) | coupang | steps=4 + delivered |
| C3 L3-ops | OPS surface | — (target=coupang) | — | cs_response 정확 + settlement keys |

## framework reuse 핵심

```
pipeline_run_order(src_adapter, tgt_adapter, order_id)
                    ▲             ▲
                    │             │
  ┌─────────────────┴─┐    ┌─────┴─────────┐
  │ C1: amazon_adapter│    │ coupang_adapter│
  │ C2: native_adapter│    │ coupang_adapter│
  └───────────────────┘    └────────────────┘

  → SAME pipeline fn · DIFFERENT adapter pair · ZERO modification
```

native_adapter() 가 amazon_adapter() 와 byte-identical surface (5 verb: search/list/order/ship/cs) 를 갖춤 → adapter_call dispatch 가 그대로 작동.

## L2 NATIVE 정체 (신규)

`native.hexa` 5 verb stub:
- **search**: own warehouse SKU 검색 (`NATIVE-SKU-0001` ID convention)
- **list**: own brand → target marketplace 등록
- **order**: own warehouse picked (state=sourcing · source_ref=NATIVE-PO-STUB-*)
- **ship**: own_logistics carrier · tracking_no=NATIVE-TRK-STUB-*
- **cs**: direct support (status=in_progress)

→ 실 wholesale/manufacturing API 는 추후 wiring (`hexa cloud` integration 잔여).

## pipeline ASCII

```
3-case 통합 smoke
        │
   ┌────┴─────────────────────────────┐
   ▼            ▼                     ▼
C1 arbitrage   C2 native         C3 ops
 amazon→coupang  native→coupang   ops fn × 2
 (4-step chain)  (4-step chain)   cs + settlement
   │            │                     │
   ▼            ▼                     ▼
delivered     delivered           cs match + keys ok
   │            │                     │
   └────────────┴─────────────────────┘
                │
                ▼
           all_pass
```

## bridge architecture 정합

- 의식엔진 framing 0 · `substrate-decided` / `brain_decide` / `Φ` 키워드 미사용
- LLM 호출 0 (CS response = pure template substitution)
- 실 HTTP 0 (모든 adapter stub return — M3 inline TODO 가 production wiring 자리)
- M1-M5 file modification 0 (additive only)

## MERCHANT 6/6 closure

| M | 산출 | PR |
|---|---|---|
| M1 types + adapter framework | 5 type + adapter convention | #639 |
| M3 L1 ARBITRAGE adapter | amazon + coupang stub | #653 |
| M4 order_pipeline | 6 fn + state transition | #700 |
| M5 OPS | 5 fn + cs template + settlement | #712 |
| **M6 L2 NATIVE + 3-lane smoke** | **native.hexa + integration_smoke** | **이 PR** |

(M2 `adapter framework` 는 M1 PR 에 effectively 흡수, line 9 미플립이지만 framework 자체는 land 됨 — honest carry.)

## 잔여 carry

- **real HTTP wiring** — 각 adapter 의 inline TODO 가 production 진입 자리 (Amazon PA-API · Coupang Wing · NATIVE own DB)
- **M2 line collapse** — MERCHANT.md line 9 (M2 adapter 프레임워크) 는 M1 #639 의 `adapter.hexa` 가 실제 surface 라 redundant — 차후 cleanup PR 에서 통합 가능
- **L3 settlement adapter verb** — 현재 coupang_adapter 에 `settlement` verb 미존재, ops_settlement_monitor 가 zero-shape fallback 반환 (honest)

## 의존성

- M1 types.hexa (5 type)
- M1 adapter.hexa (5 verb convention)
- M3 amazon.hexa + coupang.hexa (L1 adapter)
- M4 order_pipeline.hexa (6 pipeline fn)
- M5 ops.hexa (5 OPS fn)
- M6 native.hexa (신규 · L2 lane)

bridge architecture 정합 — gating 은 AGENT/CORE 가, 이 파일은 framework reuse contract verifier only.
