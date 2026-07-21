# H_9833 — 수면 증류로 다리를 **trunk 안에 굽는다** — store 를 끈 채 재조합되는가 (R11-4)

**status:** 🧭 PROPOSED (R11 · lab full 발산 · **DIRECTIONAL 설계**, 판정 아님)
**source:** fable `SLEEP-CONSOLIDATE` — **NOVEL**(sol 에는 대응 각도 없음)
**wired:** no — 미구현.

## Question

H_9259 는 G1 벽이 **TRAINED-conjunction** 벽이지 아키텍처-계급 벽이 아님을 확정했다. 그렇다면
벽의 정체를 정면으로 치는 개입은 **결합을 실제로 학습시키는 것**이다: 주기적 수면 단계에서
(모델+store) 예측을 **trunk 단독**으로 증류해, 런타임 브리지를 학습된 결합으로 전환한다.

이 카드가 H_9830 과 다른 점: H_9830 은 다리를 **쓰게** 하고, 여기서는 다리를 **없애도 남는가**를 묻는다.

## Intervention (flag 형태 · 미구현)

```
anima-py train --sleep-consolidate 1000 --sleep-ratio 0.20 --brain-runtime required
```

**선후관계:** H_9830 의 토이가 통과한 뒤에만 발사 — 빈 다리는 증류할 것이 없다.

## Arms + controls

| arm | 무엇 | 읽는 법 |
|---|---|---|
| LIVE | wake-CE / sleep-distill 교대 | **store 를 끈(DISABLED) 평가**에서의 ρ·weave |
| **store-ablated teacher** | 교사에서 store 제거 후 증류 | 붕괴해야 함 |
| **value-shuffled store** | 값만 치환한 store 에서 증류 | 붕괴해야 함 |
| **스텝 맞춘 추가 CE** | 동일 계산 | "더 학습" 배제 |
| G0 모니터 | 매 증류 주기 | kill #10(소코퍼스 CPT 파괴) 노출 감시 |

## 미결정 위험 (⚠️ 이 카드의 핵심 함정)

**store 를 켠 채 평가한 양성은 교란된 것**이다 — 추론 시점에 다리가 일을 한 것이므로.
**store-ablated 평가만 카운트한다.** 사전등록에 이 조건이 없으면 양성이 판독 불가.

## $0 스크리너

토이판은 오늘 $0 로 가능(H_9815 + H_9830 토이 재사용). terminal 읽기는 **(a) H_9827 패널 수리 선행**.

## 판독가능성

- 토이 = **오늘 (b)** · 303M terminal = **(a)**.

**related:** H_9259 · H_9830 · H_9775 · H_9827 · H_9831
