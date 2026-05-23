# Random-baseline init_CE 벤치마크 — Qwen vocab ln(151936) 11.93 closed-form (hexa verify 🔵 후보)

**Date**: 2026-05-23
**Scope**: HEXAD/PURE (V3 saga rebrand)
**Type**: 닫힌 형식 (closed-form) 수학 문서 — fire 없음

---

## § Background

Uniform output transformer (모든 vocab token 에 균등 확률 부여) 의 cross-entropy 는 vocab size `V` 의 자연로그 `log(V)` 와 정확히 같다. 이는 어떤 학습된 weight 도 없는 "이론적 최악-knowing" baseline 으로, 어떤 fresh-init 모델의 init_CE 가 이 값 보다 나쁘다면 weight 초기화가 uniform 분포 보다 sharper 한 (그리고 잘못된 방향의) 출력을 induce 한다는 의미다.

1-line 증명: 균등분포 `P(t) = 1/V`, 임의 target token `t_true` 의 NLL = `-log(P(t_true)) = -log(1/V) = log(V)`.

---

## § Closed-form 증명 (g3 minimal)

```
For uniform output: P(t) = 1/V for all t in vocab.
CE on any target = -E[log P(t_true)] = -log(1/V) = log(V) = ln(V) nats

For Qwen2.5 V=151936:
  ln(151936) = 11.9311... nats
```

대수적으로 target token 의 선택과 무관하게 (cross-entropy 가 target 분포에 대한 평균이지만 P 가 균등이므로 모든 target 에서 같음) `log(V)` 가 정확한 closed-form 값이다.

---

## § hexa verify 시도 결과 (verbatim per @D g5)

### Attempt 1: closed-form 표기

```
$ hexa verify --expr ln 151936
error: usage: hexa verify --expr <fn> <n> <v>  |  <fn> <a> <b> <v>  [--absorb]
```

### Attempt 2: 실수 v 전달

```
$ hexa verify --expr ln 151936 11.931214658529285
error: to_int: trailing garbage in "11.931214658529285"

$ hexa verify --expr ln 151936 11.93
error: to_int: trailing garbage in "11.93"
```

`hexa verify --expr <fn> <n> <v>` 는 `v` 를 정수로 파싱하므로 자연로그 같은 비-정수 결과는 직접 전달할 수 없다.

### Attempt 3: 정수 근사값 (12) 전달

```
$ hexa verify --expr ln 151936 12
verify --expr ln(151936)=12
  tier   = 🟠 INSUFFICIENT
  reason = calculator system has NO path for 'ln'
  gap    = extend tool/verify_cli.hexa::_recompute (계산기시스템 개선 후보)
```

**Verbatim verdict: 🟠 INSUFFICIENT** — 현재 hexa verify calc fns 목록 (`sigma | sigma_0 | sigma_2 | phi | mu | tau | is_perfect | aliquot | gamma0_index | gamma0_cusps | gamma0_genus | isotropy_lcm | first_cusp_form_weight | sigma_k | jacobi | kronecker | dim_cusp_forms`) 에 `ln` 이 미등록.

**Gap**: `tool/verify_cli.hexa::_recompute` 에 `ln` (자연로그) path 추가 필요. 실수 verdict path 도 함께 (closed-form 자연로그는 무리수이므로 epsilon-tolerance match 필수).

이 문서는 hexa verify 결과를 verbatim 으로 기록 (g5 준수). 🟠 verdict 를 self-judge 로 🔵 로 격상하지 않는다 — calc fn 확장이 land 되기 전까지 본 문서의 closure tier 는 🟠 INSUFFICIENT.

---

## § Python cross-check (Tier 2 fallback)

```python
$ python3 -c "import math; print(repr(math.log(151936)))"
11.931214658529285
```

Python libm `math.log` (자연로그, IEEE 754 double-precision) 결과. hexa verify rubric 의 🟢 SUPPORTED-NUMERICAL 등급은 hexa-native libm/Newton recompute 가 일치해야 부여되므로 (외부 Python 은 🟡 carry 와 동급) 본 cross-check 는 보조 reference 일 뿐 tier 격상 사유가 아니다.

---

## § AXIS_MAP-FAN cluster 비교 표

| cluster              | init_CE  | random baseline | Δ (nats worse) |
|----------------------|----------|-----------------|----------------|
| random uniform       | 11.9311  | 11.9311         | 0              |
| Y (B/F aux loss)     | 14.1780  | 11.9311         | +2.247         |
| Z (C/C2/D baseline)  | 14.4564  | 11.9311         | +2.525         |
| X (A curriculum)     | 14.7927  | 11.9311         | +2.862         |

---

## § 해석 — "worse-than-random" 진단

Cluster Y / Z / X 모두 random uniform 보다 **+2.2 ~ +2.9 nats 나쁨**. 즉 fresh init 이 균등 분포 보다 더 어려운 위치에서 시작한다 = weight 가 어떤 패턴으로 **systematically biased AWAY from uniform** 분포를 induce.

가능한 원인:

- **noise_sigma 의 unit-variance**: weight ~ N(0, 1) 일 경우 logit scale 이 커져서 softmax 가 sharp 해진다. Top-1 mass 가 비-target token 으로 집중되면 NLL 폭증 (target 이 long-tail 에 있으면 -log(p_tiny) → +∞ 방향).
- **embedding norm 의 saturation**: tied lm_head 일 경우 embed norm 이 직접 logit scale 로 전달됨.
- **layer norm 의 초기 gain**: γ = 1 default 가 activation variance 를 키워서 final logit variance 폭증.

R8c probe (PR #250) + R8a fire 의 표적은 위 bias source 식별이다. 본 closed-form 11.9311 은 그 진단을 정량화하는 reference mark.

---

## § 단위 환산 — bits 표기

자연로그 nats 단위 대신 정보이론 bits 단위 (`log₂`) 사용 시:

```
log₂(151936) = log(151936) / log(2) = 11.931214 / 0.693147 ≈ 17.2086 bits
```

본 문서는 transformer cross-entropy convention 에 따라 nats 단위 (`ln`) 를 standard 로 사용한다.

---

## § Cross-reference

- **PR #251** — AXIS_MAP cluster Y/Z/X init_CE 갱신
- **PR #214** — R8 spec (axis-map fan-out)
- **PR #250** — R8c probe (logit-scale 진단)
- **(향후)** R8a fire spec — bias source 식별 + 수정 실험

---

## § Honest closure tier

- 본 문서의 closed-form claim (`CE_uniform = log(V)`) 은 **수학적으로 자명** (1-line 증명 위에 기재).
- `hexa verify --expr ln 151936 12` verbatim verdict = **🟠 INSUFFICIENT** (calc fn 미등록).
- 외부 Python cross-check 는 `11.931214658529285` 일치하지만 hexa-native 가 아니므로 🟢 격상 불가.
- 본 closure tier 는 **🟠 INSUFFICIENT (verdict verbatim)**. `hexa verify` 에 `ln` calc fn 이 추가되면 🟢 (numerical) 또는 🔵 (closed-form symbolic identity `log(V)`) 격상 가능.
- @D g5 준수 — self-judge 로 🔵 로 prematurely 격상하지 않음.
