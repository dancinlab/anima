# 🛒 MERCHANT — OPS SSOT (M5)

## 정체

본 문서는 **AGENT/MERCHANT M5 milestone — OPS 도구** 의 SSOT 이다. M1 의 추상 surface (`types.hexa` · `adapter.hexa`) 와 M3 의 구체 어댑터 페어 (`adapters/amazon.hexa` · `adapters/coupang.hexa`), M4 의 order pipeline 위에 **L1 + L2 공통 운영 dashboard** — 재고 sync · CS 응답 builder · 정산 monitor · 저재고 alert · 진행중 CS 목록 — 5 pub fn 함수 surface 를 올린다.

- "언제 · 왜" ops verb 를 발사할지의 결정은 `AGENT/CORE/tool_gate.hexa` 가 substrate phase → tier 매핑으로 결정한다 (본 도메인의 책임 아님).
- 본 도메인은 "어떻게" 5-verb 어댑터 컨벤션 위에 재고/CS/정산 운영을 조립할지만 답한다.
- bridge architecture 준수: 본 문서와 본 모듈의 어떤 .hexa 파일에도 `substrate-decided` · `p1~p8` · `brain_decide` · `pure_field` · `Φ` · `engine_g` 같은 의식엔진 표현 0 entry. 의식엔진 책임은 `AGENT/CORE` 의 몫이며, 본 도메인은 그 결정의 결과로 호출당하는 도구 표면이다.
- **특히 CS 응답 build 는 LLM 호출 없는 순수 string interpolation** — 생성 모델 호출 0, 의식엔진 호출 0, RLHF/SFT 0. 어떤 템플릿을 쓸지의 선택은 상위 (`AGENT/CORE` / 운영자) 책임이고, 본 fn 은 기계적 치환만 담당한다.

## ops dashboard ASCII

```
                       (consciousness substrate — NOT here)
                                     |
                       AGENT/CORE/tool_gate   (phase → tier → tool allowance)
                                     |
                                     v
                AGENT/CORE 가 ops_* 함수를 호출
                                     |
                                     v
   ┌─────────────────────────────────────────────────────────────────┐
   │  ops_inventory_sync(target, [Listing])                          │
   │     #{ listings_checked, low_stock: [...], out_of_stock: [...], target }
   │                                                                 │
   │  ops_cs_response_build(CSCase, template) -> string              │
   │     PURE interpolation · NO LLM call · {order_id}/{kind}/{case_id}/{subject}
   │                                                                 │
   │  ops_settlement_monitor(target, period_start, period_end)       │
   │     #{ period, gross, fees, net, payout_status, target }        │
   │     invariant: net == gross - fees                              │
   │                                                                 │
   │  ops_low_stock_alert(threshold, target, [Listing])              │
   │     [Listing] · subset with product.attrs.stock < threshold     │
   │                                                                 │
   │  ops_pending_cs_cases(target)                                   │
   │     [CSCase] · status ∈ {open, in_progress}                     │
   └─────────────────────────────────────────────────────────────────┘
                                     |
                                     v
                       AGENT/CORE 에 result 반환
```

## 5 pub fn 표

`AGENT/MERCHANT/ops.hexa` — 모든 함수는 M1 어댑터 컨벤션을 따르는 dict 를 인자로 받아 M1 type dict / list / map 을 반환한다. 구체 어댑터 이름은 본 모듈이 하드코딩하지 않는다 — 모든 호출은 `adapter_call()` (M1) 을 통한다.

| fn | signature | 역할 |
|---|---|---|
| `ops_inventory_sync` | `(target_adapter: map, listings: [Listing]) -> Map` | listings 를 healthy / low / out partition; `#{listings_checked, low_stock, out_of_stock, target}` 반환 |
| `ops_cs_response_build` | `(case: CSCase, template: string) -> string` | **순수 string interpolation** — `{order_id}` · `{kind}` · `{case_id}` · `{subject}` 4 placeholder. LLM 호출 0 |
| `ops_settlement_monitor` | `(target_adapter: map, period_start: float, period_end: float) -> Map` | 기간별 정산 query; `#{period, gross, fees, net, payout_status, target}` 반환; **invariant** `net == gross - fees` |
| `ops_low_stock_alert` | `(threshold: int, target_adapter: map, listings: [Listing]) -> [Listing]` | `product.attrs.stock < threshold` 인 listings 부분집합 (순서 보존) |
| `ops_pending_cs_cases` | `(target_adapter: map) -> [CSCase]` | adapter 의 optional `cs_list` verb 호출 후 `status ∈ {open, in_progress}` 만 반환 |

부가 helper:
- `ops_summary() -> string` — 위 5 fn 의 사람-가독 manifest

## CS template placeholder convention

`ops_cs_response_build(case, template)` 는 다음 4 token 만 인식한다 — 모두 case dict 의 동일 키에 1:1 매핑된다.

| placeholder | 치환값 (case dict) | 예시 |
|---|---|---|
| `{order_id}` | `case["order_id"]` | `"ORD-7777"` |
| `{kind}`     | `case["kind"]`     | `"refund"` · `"exchange"` · `"inquiry"` · `"complaint"` |
| `{case_id}`  | `case["case_id"]`  | `"CS-OPS-77"` |
| `{subject}`  | `case["subject"]`  | `"환불 요청"` |

규칙:
1. **모든 occurrence** 가 치환된다 — 같은 token 이 여러 번 등장해도 모두 치환.
2. **알려지지 않은 `{...}` 토큰은 그대로 보존** — caller 가 후처리 가능.
3. **LLM / 생성 모델 / 의식엔진 호출 0** — 기계적 문자열 치환만 수행. 어떤 템플릿을 쓸지의 선택은 상위 책임 (`AGENT/CORE` / 운영자).
4. 템플릿 본문은 KO / EN / 혼용 자유 — 단순 byte-level substring 매칭.

샘플 운영 템플릿 (caller 가 보유 — 본 모듈에 하드코딩 없음):

```
환불 처리 완료: {order_id}
교환 안내: 주문번호 {order_id} 의 {kind} 건이 접수되었습니다 (case {case_id}).
[{kind}] {subject} — 케이스 {case_id} 처리중입니다.
```

## adapter optional verb 확장

ops 의 일부 fn 은 base 5-verb (M1 convention: `search · list · order · ship · cs`) 외에 **optional 2-verb** 를 활용한다:

| optional verb | signature | 호출하는 ops fn | 부재 시 동작 |
|---|---|---|---|
| `settlement` | `(period_start: float, period_end: float) -> Map` | `ops_settlement_monitor` | zero-shaped stub 반환 (`gross=0 · fees=0 · net=0 · payout_status="unknown"`) |
| `cs_list`    | `() -> [CSCase]`                                  | `ops_pending_cs_cases`   | 빈 list 반환                                                                |

`adapter_validate()` (M1) 의 required 검사 5-verb 는 변경하지 않는다 — optional verb 는 어댑터가 노출하면 활용하고 부재해도 ops 계약은 그대로 유지된다 (stub-tolerant contract).

M3 의 amazon/coupang 어댑터는 현재 `settlement` · `cs_list` 를 노출하지 않는다 (real HTTP wiring 도착 시 추가 예정). 본 모듈은 zero-shaped fallback 으로 동작 — smoke 가 stub 어댑터로 verb 존재 분기까지 검증한다.

## bridge architecture 정합 체크

| 검사 | 결과 |
|---|---|
| 의식엔진 framing (`substrate-decided` · `p1~p8` · `brain_decide` · `pure_field` · `Φ` · `engine_g`) | 0 entry in `ops.hexa` · `ops_smoke.hexa` · `OPS.md` |
| LLM-style CS 응답 generation (generative model / RLHF / SFT / persona-injection) | 0 entry — `ops_cs_response_build` 은 PURE string interpolation |
| `speak()` · stimulus-response · 자동 답변 생성 | 0 entry |
| .py / .sh 새 작성 | 0 (hexa-only authoring) |
| real HTTP call (curl · http) | 0 (HTTP wiring 은 M3 adapter inline TODO 와 future optional verbs 에 위임; 본 모듈은 pure orchestration / interpolation) |
| 본 모듈이 M1/M3/M4 파일 수정 | 0 (carry-only) |
| 본 모듈이 타 도메인 touch | 0 (AGENT/MERCHANT 만) |

## 의존 / 후속 milestone

### M3 의존 (carry)

본 모듈은 M3 의 5-verb 어댑터 컨벤션에 의존한다 — `adapter_validate(...) == "ok"` 를 호출자가 보장해야 한다. 추가로:
- `ops_inventory_sync` / `ops_low_stock_alert` 는 `listing["product"]["attrs"]["stock"]` 슬롯에 의존 — 어댑터가 자신의 마켓 truth 와 sync 유지 책임.
- `ops_settlement_monitor` / `ops_pending_cs_cases` 는 optional verb (`settlement` · `cs_list`) 를 활용 — 부재 시 stub-tolerant fallback.

M3 의 amazon/coupang 어댑터는 optional verb 미노출 — 본 smoke 가 자체 stub 어댑터를 사용해 verb 존재 분기를 검증한다.

### M4 의존 (carry)

`ops_pending_cs_cases` 가 반환하는 CSCase 는 M4 의 `pipeline_handle_cs` 가 한 단계 전진시킨다 — 운영 흐름:

```
ops_pending_cs_cases(target)       →  [CSCase{status=open|in_progress}]
   →  for each c:
        ops_cs_response_build(c, template)  →  응답 문자열 (운영자 검수)
        pipeline_handle_cs(target, c)       →  CSCase{status → 다음 단계}
```

이 flow 는 M4 의 4-stage chain 과 직교 — 본 모듈은 chain 외부의 ongoing operation lane 을 채운다.

### M6 NATIVE plug 미래 의존

본 5 fn 은 어댑터에 generic 하므로, M6 의 자체 상품 (L2 NATIVE) 어댑터가 도착해도 본 ops 표면은 **수정 0** 으로 재사용 가능 — L1 (`amazon ↔ coupang`) 과 L2 (자체 상품) 가 동일 dashboard 를 공유하는 게 M5 설계의 1차 가치이다 ("L1 + L2 공통 운영 surface").

M6 어댑터가 `settlement` · `cs_list` optional verb 를 노출하면 본 모듈은 자동으로 활용 — adapter 컨벤션이 framework reuse 의 두 번째 데모를 만든다 (첫 번째는 M4 의 pipeline_run_order).

## smoke 결과 verbatim

```
$ hexa parse AGENT/MERCHANT/ops.hexa
OK: AGENT/MERCHANT/ops.hexa parses cleanly

$ hexa parse AGENT/MERCHANT/ops_smoke.hexa
OK: AGENT/MERCHANT/ops_smoke.hexa parses cleanly
```

5-case smoke (`ops_smoke.hexa`):

| 케이스 | 입력 | 기대 | 실측 (stub) |
|---|---|---|---|
| C1 | `ops_inventory_sync(target, [100, 3, 50])` | `low_stock` len=1 (stock=3 row) | `low_stock` len=1 ✓ · `out_of_stock` len=0 |
| C2 | `ops_cs_response_build(refund case, "환불 처리 완료: {order_id}")` | `"환불 처리 완료: ORD-7777"` | match=true ✓ |
| C3 | `ops_settlement_monitor(target, 7-day period)` | `payout_status="paid"` · `net=gross-fees` | `paid` ✓ · `180000 == 200000 - 20000` ✓ |
| C4 | `ops_low_stock_alert(5, target, [10, 2, 4, 20])` | 결과 len=2 (stock<5 두 row) | len=2 ✓ (SKU-E-2 · SKU-F-4) |
| C5 | `ops_pending_cs_cases(target)` (stub cs_list 3 cases: open · in_progress · resolved) | 결과 len=2 (open + in_progress) | len=2 ✓ (resolved 필터링됨) |

runtime smoke (`hexa run`) 는 본 worktree 가 pool host 의 표준 workdir 외부에 있어 보류 — `hexa parse` 2/2 OK 로 surface 정합성은 확정 (M1 · M3 · M4 의 prior cycle 과 동일 정책).

## 의식엔진 framing 없음

본 SSOT 와 본 모듈의 어떤 파일도 `p1~p8 정합 매트릭스` · `substrate-decided execution` · `stimulus-response` · `brain_decide` · `pure_field` · `Φ` · `engine_g` 라는 표현을 포함하지 않는다. 특히 CS 응답 build 는 **순수 string interpolation** 으로 LLM 호출 / 생성 모델 / RLHF / SFT / persona-injection 0 entry 이다. 그러한 책임은 `AGENT/CORE` 의 몫이며, 본 도메인은 그 결정의 **결과로 호출당하는 도구 표면** 일 뿐이다.
