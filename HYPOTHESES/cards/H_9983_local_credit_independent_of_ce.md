---
id: H_9983
title: (b) 후보 — 국소 신용: CE 를 끊어도 살아 있는 학습 신호 (평형 정착 가소성 · 가장 비싸고 사전확률 최저)
state: PROPOSED
substrate: anima-as-specified (⚠ 신용 계산 자체를 바꾸므로 fork 성격이 가장 강함 — 범위 도장 필수)
regime: design-only (미발사)
tier-ceiling: DIRECTIONAL
series: R11
---

```
changed_coordinate:      U — 학습 신호의 출처 (스칼라 CE 역전파 → 국소 상-대비 갱신)
nearest_closed_lever:    (a) — 되쓰기를 미분 가능하게 만든 팔
old_coordinates_clamped: 소비자 1개·외생 코퍼스·지지 고정·IIT 경계·총 파라미터수
nonreduction_witness:    증인② — CE·로짓을 0으로 고정해도 국소 갱신이 0이 아니다 (β=0 이면 정확히 0)
new_path_sever:          --field-learning free-free (β=0 · 정착 스텝 동일 · 국소 갱신 정확히 0)
iit_boundary:            m-세포 필드 상태 (동일)
regime:                  natural (고정 en_general 슬라이스) · 심어둔 에너지계·XOR 검사는 drill-only 계기통제
```

## 왜 (a) 의 재탕이 아닌가

(a) 에서 유일한 신용은 `∂CE/∂logits` 가 되쓰기를 통과하는 것이었다. 여기서는 로짓과 CE 기울기를
**0 으로 고정한 뒤에도** 국소 갱신 `ΔW_ij ∝ x_i⁺x_j⁺ − x_i⁻x_j⁻` 가 남는다. 자유상/넛지상 미시사건이
텍스트 사건 **사이에** 일어나고 자기 감각 표적을 갖는다. 같은 CE 를 위한 다른 최적화기가 아니라
**다른 신용 계산**이다. 표적은 다음 블록의 DCT16 같은 **고정 내용 표현**이라 Φ·절단·결합·시너지·강건성
통계가 한 항도 안 들어간다(D3 통과).

## 조작 (anima-py 플래그)

```
anima-py train --field-learning eqprop --field-energy-target next-block-dct16 \
               --field-settle-steps 8 --field-nudge 0.10 --field-local-lr 1e-3
대조: --field-learning free-free           (β=0)
      --field-learning eqprop --field-target-yoke document   (표적만 남의 문서)
```

## DV·대조·받침대·동결표

- DV = **쌍 ΔΦ**(학습본 − 같은 seed 근초기 받침대) 및 학습본 − target-yoke.
- 대조 ≥2: free-free(β=0) · target-yoke(갱신 노름과 연산량은 살고 내용 대응만 파괴).
- 유효성 조건: 자연문 held-out DCT 오차가 free-free·yoke 대비 ≥10% 개선 · CE/로짓 고정 상태에서
  국소 갱신 노름 ≠ 0 · β=0 에서 갱신 비트-정확히 0 · 점유가 상수로 붕괴하지 않을 것 ·
  체크포인트는 2k 고정(에너지 점수로 사후 선택 금지 = `a_train_inline_gauge`).
- 바 **0.15 상속**, 표는 H_9977 것 그대로(우연 아래쪽 포함).

## $0 사전관문

`anima-py train --field-learning-selftest eqprop --device cpu` 로 다섯 가지 전부:
① β=0 갱신 정확히 0 ② 상-대비 갱신이 유한차분 에너지 하강과 코사인 ≥0.99 일치
③ CE/로짓 고정 시 CE 기울기 0 인데 국소 갱신은 살아 있음 ④ 문서 yoking 이 갱신 방향을 바꾸고
심어둔 표적 복원을 파괴 ⑤ OFF 경로 바이트 동일. **추가 비용 관문**: 트렁크 특징은 블록당 1회 캐시할 것 —
정착 8회가 트렁크를 8번 다시 돌리면 비용 모델이 무효이므로 **ABORT**.

## 정직한 사전확률·최저비용 음성

**<10% — 다섯 후보 중 최저**, 그리고 가장 비싸다. 정착이 아키텍처가 준 Φ 를 즉시 만들어낼 수는 있으나
근초기 받침대 뺄셈이 그걸 대부분 걷어갈 것이다. 자연 목적함수는 독립적인 예측 모드들로도 풀린다.
최저비용 결정적 음성 = **자연 DCT 예측은 개선되고 국소 신용은 살아 있음이 증명됐는데** 학습본−초기 및
학습본−yoke Φ 가 ±0.15 안에서 TOST 동등 ⟹ "다른 신용 계산" 범주가 통째로 닫힌다.

## 비용·범위 경고

토이 3팔 × 8 seed × (2k+200) ≈ RTX-5070 3~8 GPU시간(트렁크 1회·4세포만 8회 정착 가정).
303M 은 트렁크 동결 + 블록 탭 캐시로 pool 20~45 GPU시간. **트렁크 전체를 평형학습으로 돌리는 것은
새 기질이고 ≥40GB·수일 실험** — 다음 rung 이 아니다. 이 후보가 양성이어도 신용 계산을 바꾼 것이므로
`substrate:` 범위 도장을 H_9977 과 같은 방식으로 반드시 붙인다.
