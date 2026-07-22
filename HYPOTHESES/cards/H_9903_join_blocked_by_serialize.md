# H_9903 — 합류 경로는 **직렬화 계약이 막는다** (aux head 는 serialize 에서 버려진다)

**status:** 🔴 **BLOCKED-BY-CONTRACT** — [[H_9901]] 이 지명한 다음 축의 실행 가능성을 코드에서 확정
**wired:** 판독 대상 = `cli/train.py` serialize 계약 · `cli/evaluate.py::_Mouth.ideate`
**source:** [[H_9901]] *"다음 설계는 읽기 시점에 합류하는 경로여야 한다"*

## 확인한 것

[[H_9901]] 은 ①CE 트렁크 무접촉과 ④lane→mouth 도달이 **서로 배타적**임을 측정하고,
해법으로 **디코드 시점 합류**(lane logits 를 mouth logits 에 더하기)를 지명했다.
그 실행 가능성을 [[H_9899]] 와 같은 방식으로 **발사 전에** 코드에서 확인했다.

### 🔴 계약이 명시적으로 막는다

`cli/train.py` 의 직렬화 계약이 세 번 반복해 적고 있다:

> *"Heads **DROPPED at serialize**"* (×2)
> *"aux heads/projections live **OUTSIDE `model.state_dict`** (in the objective module),
> so `serialize_v3` writes **only the standard additive-readout CLMConvMoE**"*

⟹ [[H_9900]] 의 lane head 는 **`.clm` 에 실리지 않는다.** 실리지 않으면
`evaluate` 의 mouth 는 그 가중치를 **볼 수 없고**, 디코드 시점 합류는 **원리적으로 불가능**하다.

## 이것이 뜻하는 것

합류 경로는 *구현 노력* 문제가 아니라 **포맷 계약 문제**다. 필요한 것은:
1. `.clm` v3 포맷에 **보조 head 슬롯 신설**(포맷 버전 변경)
2. `core/` 디코더가 그 슬롯을 읽어 logits 에 합류
3. 두 프로덕션 트윈(py·hexa)의 **byte-parity 유지**

⟹ 이건 `cli/` 실험 하나가 아니라 **`core/` 포맷 변경**이며,
`a_cli_single_entry`·2-production parity 규율상 **별도 캠페인**이다.

## 🔑 그래서 이 캠페인의 정확한 종착점

| 층위 | 상태 |
|---|---|
| 조성 능력 | ✅ **실재**([[H_9883]] · 2 seed · 통제 3종 0 · 암기교란 0/76) |
| 밀도 축 | 🧱 **닫힘**([[H_9889]]·[[H_9898]] — 6 지점 전수 · 등노출 포함) |
| 분리 축(학습측) | ✅ **구현·검증**([[H_9900]] 요건 3/3) |
| 분리 축(읽기측) | 🔴 **포맷 계약이 막음** ← 이 카드 |

⟹ G1 은 **기질의 벽도, 데이터의 벽도 아니고, 지금은 `.clm` 포맷의 벽**이다.
이 문장은 이 캠페인이 **측정으로 도달한 가장 깊은 층**이며, 세션 시작의
*'조성 부재'* 와는 다른 종류의 진술이다.

## ⚠️ 이 카드가 하지 않는 것

포맷을 바꾸지 **않는다**. 2-production parity 를 건드리는 변경을 세션 말미에
검증 없이 밀어넣는 것이야말로 이 캠페인이 6팔을 태우고 배운 것의 정반대다.
필요 작업 3개를 명시해 다음 캠페인에 넘긴다.

## Cross-links

[[H_9901]] 이 지명한 축 · [[H_9900]] 학습측 lane · [[H_9899]] 같은 방식의 사전 스코핑 · [[H_9883]] 조성 실재
