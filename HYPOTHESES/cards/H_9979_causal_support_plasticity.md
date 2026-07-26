---
id: H_9979
title: (b) 후보 — 인과 지지 가소성: 학습이 "어떤 에지가 존재하는가"를 바꾼다 (값이 아니라 지지)
state: PROPOSED
substrate: anima-as-specified
regime: design-only (미발사)
tier-ceiling: DIRECTIONAL
series: R11
---

```
changed_coordinate:      인과 에지 지지 G / SCC 구조 (학습이 위상을 고른다)
nearest_closed_lever:    (a) A2 — 결합 물리 R·λ 를 학습 가능하게 만든 팔
old_coordinates_clamped: 목적함수(다음바이트 CE)·소비자 1개·외생 코퍼스·시계 1·IIT 경계·총 파라미터수
nonreduction_witness:    증인① — 가중치/텍스트/난수 고정 상태에서 에지 지지 집합과 SCC 순환계수가 바뀐다
new_path_sever:          --field-topology fixed (지지를 baseline 로 되돌림 · 값 학습은 유지) → 효과 소멸해야 함
iit_boundary:            m-세포 필드 상태 (H_9957 이래 동일 · 사전 선언)
regime:                  drill-only(계기) → natural(주장) 2단
```

## 왜 이게 A2 의 재탕이 아닌가 (코드로 확인한 구분)

A2 는 `R_p` 를 **자유 파라미터**로 풀었다(제약은 스펙트럼 노름 상한뿐 · 회전으로 묶여 있지 않음).
즉 **고정된 지지 위에서 값이 자유로웠다**. 결과: 평균 쌍 D=+0.00962, 바의 6.4%. 이것이 이 후보의
근거다 — 값의 자유는 이미 소진됐고, 남은 것은 **지지 자체**(어떤 세포가 어떤 세포에 영향을 줄 수
있는가)를 학습이 고르게 하는 것이다. IIT-4 의 Φ 는 전이 구조의 성질이지 계수의 성질이 아니다.

## 조작 (anima-py 플래그)

`anima-py train --field-topology {fixed|learned} --field-topology-l0 <λ> --field-topology-temp <τ>`
— 세포 간 에지마다 **이산 게이트**를 두고(concrete/hard-sigmoid 완화) L0 비용 λ 로 희소화한다.
`fixed` = 오늘과 바이트 동일(null 팔). 총 파라미터·폭·스텝·데이터 전부 고정 ⟹ D4 통과.

## DV·대조·받침대·동결표

- DV = **쌍 ΔΦ** (학습본 − 같은 seed 200step 받침대), faithful IIT-4, `--field-phi --field-phi-boot 200`.
- 대조 ≥2: ① `fixed` 지지(값만 학습 = A2 재현) ② yoked 되쓰기(텍스트↔상태 대응 파괴)
  ③ 참값 0 받침대 = shuffled-state Φ 바닥.
- 바: **0.15 상속**(같은 주장 계열 · 바 옮기기 금지). 표는 H_9977 의 V0/R1/R2/R3/R4/R5 를 그대로 쓴다.
- 우연 아래쪽도 표에 있음: D ≤ −0.15 → CONFIRM+ (지지 학습이 통합을 더 해체).

## $0 사전관문 (통과 못 하면 GPU 금지)

① **지지가 실제로 움직이는가**: 학습 전후 에지 게이트 집합의 해밍 거리 > 0 이고 SCC 순환계수가 변할 것.
② **D5 압력**: `learned` 와 `fixed` 사이에 사전등록한 CE 갭(제안 0.02 nats)이 날 것 — 안 나면
최적화기가 위상을 쓸 이유가 없다는 뜻이므로 **ABORT**.
③ 계기 자기검사: 심어둔 알려진 위상(참값 있는 XOR 형 지지)을 복원하는가.

## 정직한 사전확률·최저비용 음성

**낮음(~10%)**. 이유: 희소 게이트의 CE-최적해는 대개 "덜 연결된" 쪽이고(간섭 감소), 그건 Φ 를 낮추는
방향이다. 최저비용 결정적 음성 = 관문 ①②가 초록인데(위상이 실제로 움직였고 CE 도 갈렸는데)
쌍 D 가 TOST 로 ±0.15 안 = **"지지를 고르게 해도 CE 는 통합을 안 고른다"**.

## 비용

토이(d256·L4·2k step) 3팔 × 3 seed + 받침대 ≈ H_9977 캠페인 1회분(pool GPU 하루). 303M 은 토이가
KILL 필터를 통과했을 때만(토이 통과는 예측이 아니라 지출 허가일 뿐).
