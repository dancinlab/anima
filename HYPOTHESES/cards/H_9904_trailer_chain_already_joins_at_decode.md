# H_9904 — decode-time join 은 포맷이 막은 게 아니다: 레인 트레일러 체인이 이미 7칸 있고 그중 하나는 in-vivo 증명됐다

**tier:** 🔧 코드-확증 스코핑 정정 (측정 0 · 새 코드 0줄) · **DIRECTIONAL** · NOT a verdict
**group:** R13-instrument-audit
**date:** 2026-07-22
**source:** [[H_9903]](#4380) 의 "decode-time joining is impossible by construction" 을 코드에서 재확인하다 반례 발견
**wired:** n/a (기존 배선을 가리키는 카드 · 새 계기 없음)
**verdict:** 원 판정의 **범위**를 좁힌다 — 결론(그 lane 은 mouth 에 못 닿는다)은 유지, **원인 귀속**은 정정

## 무엇을 정정하나

[[H_9903]] 은 [[H_9901]] 의 ρ·weave 0.000 이 배선 문제임을 옳게 짚고, 해법으로 지목한
decode-time join(레인 로짓을 디코드 중 mouth 로짓에 더하기)이 **포맷 계약상 불가능**이라 결론지었다:

> "a head that is not in the file cannot be read by evaluate's mouth. Decode-time joining is
> impossible by construction, not by effort." ⟹ .clm v3 에 보조-헤드 슬롯 신설 + core 디코더 +
> 2-production 바이트패리티 = **별도 캠페인**.

**앞 문장은 맞고 뒤 문장은 과도하다.** 코드 확인(추정 아님):

### 사실 1 — .clm 은 이미 **레인 트레일러 체인**을 갖고 있다 (7칸)

`core/serialize.py:72` — 체인 순서가 주석으로 못박혀 있다:

```
CLMB → SLW → CLML → CLMS → MBND → IFAN → TFLD
```

"보조 헤드 슬롯 신설(format version change)" 은 신설이 아니라 **여덟 번째 선례**다.
레인을 트레일러로 착륙시키는 것은 이 저장소가 **일곱 번 반복한 확립된 패턴**이다.

### 사실 2 — 디코더가 그 슬롯을 읽고 eval 에 적용한다

`core/decode.py:336~350` 이 `_CLMS_STORE` / `_CLMS_QUERY` 등 프로세스-전역 주입점을 갖고
`store_apply` 를 부른다. 트레일러가 있어도 store 미주입이면 **passthrough(바이트 동일 · C0-f 봉인)**.

### 사실 3 — 그리고 그 융합이 정확히 "레인 로짓을 mouth 로짓에 더하기" 다

`core/clms.py:117~183, 314` (H_9695/H_9696):

```
query="every-token"  → 모든 행에서 발화 (자유 생성엔 리터럴 트리그램이 없으므로)
fuse="gated-add"     → out[t] = logits[t] + λ·s     ← 트렁크 보존 + 레인은 섭동
                        (모든 행 overwrite 는 트렁크를 지우므로 add 로 설계됨)
```

**모든 위치**에서 트렁크 로짓에 더한다 = [[H_9903]] 이 "불가능" 이라 한 그 연산.
그리고 이 경로는 [[H_9775]] 에서 **in-vivo 로 증명**됐다(2/2 seed · value-permute 0.4446 붕괴).

## 정확한 스코핑 (이게 이 카드의 본체)

```
❌ 틀린 귀속:  .clm 포맷이 decode-time join 을 막는다
✅ 맞는 귀속:  H_9900 의 comp-lane 헤드가 model.state_dict 밖(objective 모듈)에 살아서
               serialize_v3 가 안 쓴다 — 그 헤드를 **어디에 두었는가**의 문제이지
               포맷의 능력 문제가 아니다
```

⟹ 필요한 것은 "포맷 버전 변경 별도 캠페인" 이 아니라, **레인을 트레일러 체인에 얹는
기존 패턴을 따르는 것**이다(선례 7개 · [[H_9775]] 가 그 경로로 mouth 도달을 이미 증명).

## ⚠️ 정직한 잔여 제약 — 이 카드가 해결하지 **않는** 것

- [[H_9899]] 가 확정한 **1바이트 제약은 학습 셀(StoreBindCell `gold[:1]`)의 성질**이지
  트레일러/디코드 경로의 성질이 아니다. `every-token` 은 모든 위치에 쓰므로 다중바이트
  스팬을 덮을 수 **있으나**, 그 값이 store 행 읽기(내용주소)에서 나온다는 점은 그대로다.
- 따라서 **조성 헤드의 파라미터가 CLMS 트레일러 파라미터 집합
  `{key_emb, W_q, val, W_h, b_h, W_out, λ}` 모양에 들어가는가**는 실제 설계 물음이며
  이 카드가 답하지 않는다. 안 들어가면 여덟 번째 트레일러(고유 magic)를 새로 정의하면 되고,
  그것도 **선례 7개가 있는 확립된 작업**이지 포맷 재설계가 아니다.
- 2-production 바이트패리티 요구는 유효하다(hexa/py 양쪽). 그건 트레일러 신설이든
  재사용이든 동일하게 걸린다.

## 왜 지금 이게 중요한가

캠페인 현황([[H_9903]] 자신의 정리)에서 막힌 칸이 정확히 이 칸이다:

```
조성 faculty      실재      (H_9883 · 2 seed · 통제 0 · 암기 0/76)
밀도 축           닫힘      (H_9889 · H_9898 · 등노출 포함 6점)
분리, 학습측      됨        (H_9900 · 요건 3/3)
분리, 읽기측      ❌ 막힘   ← 이 카드가 여기를 다시 연다
```

"별도 캠페인" 으로 미루면 이 계보가 멈춘다. 선례를 따르면 멈추지 않는다.

## 반증

`core/serialize.py` 의 체인 주석과 `core/decode.py` 의 CLMS 주입점, `core/clms.py` 의
`fuse="gated-add"` 경로 중 **하나라도 실제로는 죽어 있거나 eval 에서 안 불린다면** 이 카드는
틀린다. 확인 방법 = `anima-py evaluate <H_9775-ckpt> --store m.json --store-query every-token
--store-fuse gated-add` 가 base 와 다른 출력을 내는가($0 · 기존 ckpt · 새 학습 없음).

---

## 🔬 반증 시험 실행 결과 (2026-07-22 · 토이 · $0) — 카드 주장 부분 확증 + **내 시험은 무효**

카드에 적어둔 반증법을 직접 돌렸다. 결과를 보기 **전에** 판독 기준을 고정했다:
*두 팔이 다른 값 ⟹ 카드 유지 · 같은 값 ⟹ 카드 반증.*

`anima-py evaluate ~/anima-weights/store_struct_toy/toy.clm --store …held.json` (128 items):

| 팔 | overall | is/good | is/bad | not/good | not/bad |
|---|---|---|---|---|---|
| A `qpos·overwrite`(기본) | **126/128 = 0.9844** | 1.0000 | 0.9630 | 0.9737 | 1.0000 |
| B `every-token·gated-add` | **126/128 = 0.9844** | 1.0000 | 0.9630 | 0.9737 | 1.0000 |

소수점까지 동일 — 첫 반응은 "경로 사망"(`flat-across-manipulations-means-the-lane-is-dead`)이었다.
**그 판독은 틀렸다.** 코드를 열어보니 계기가 조작 지점을 안 본다:

```python
clm.set_clms_store(..., query=store_query, fuse=store_fuse)   # 플래그는 실제로 전달됨
logits = clm._fwd_logits(W, tok, T)
qp = _clms.find_qpos(tok)
if not qp: return None
row = logits[qp[-1]]        # ← qpos 행 하나만 채점
```

`every-token` 의 존재 이유는 **마커 없는 자유 생성에서 발화**하는 것인데(H_9695: "free ideation
carries no marker"), 이 매니페스트는 전 항목이 `=> ` 마커를 갖고 채점기는 qpos 행만 읽는다.
⟹ **조작이 만드는 차이가 DV 밖에 있다.** 게다가 qpos 행에서 `overwrite`(λ·s)와
`gated-add`(logits+λ·s)는 g/b 2지선다 argmax 를 같은 쪽으로 몰기 쉬워(레인이 0.9844 로 강하게
학습됨) 이 거친 readout 은 두 모드를 원리적으로 구분하지 못한다.

⟹ **이 시험은 반증이 아니라 INVALID** 다. 계기가 조작을 볼 수 있음을 먼저 증명하지 않고 null 을
읽었다 — `positive-control-before-reading-a-negative` 위반을 내가 저질렀다. 판정 철회.

### ✅ 다만 ARM A 가 카드의 핵심 주장을 **실증**한다

`toy.clm` 은 `CLMX` + **`CLMS` 트레일러를 실제로 담고 있고**(바이트 확인 · 406,763 B),
디코더가 그것을 읽어 답위치 로짓을 바꿔 **0.9844** 를 만든다. 즉:

> "a head that is not in the file cannot be read by evaluate's mouth" ([[H_9903]]) 의 전제에
> 대해 — **파일 안에 있고 mouth 가 읽는 헤드가 실재한다**는 살아있는 반례가 여기 있다.

포맷이 decode-time join 을 막지 않는다는 이 카드의 결론은 **유지**된다. 막힌 것은
[[H_9900]] 의 헤드가 `model.state_dict` 밖에 살아 `serialize_v3` 가 안 쓴 것뿐이다.

### 교체된 반증법 (다음 사람이 쓸 것)

`every-token` 을 판독하려면 **마커 없는** 창과 **qpos 아닌 행**을 보는 DV 가 필요하다:
- 매니페스트에서 `=> ` 를 제거한 자유-생성 창(마커 부재 ⟹ `qpos` 팔은 `find_qpos` 가 비어
  `None` 반환 = 무응답, `every-token` 팔만 발화) — 이 대조가 진짜 판별식이다.
- 또는 전 행 로짓의 L1 차이 `‖logits_B − logits_A‖₁` 를 직접 보고. 0 이면 경로 사망,
  >0 이면 살아있음. qpos-2지선다 argmax 로는 영원히 못 가른다.

⚠️ 이 절은 **계기 판정**이지 기질 판정이 아니다. cement 는 engine-native `anima-py` 로만.
