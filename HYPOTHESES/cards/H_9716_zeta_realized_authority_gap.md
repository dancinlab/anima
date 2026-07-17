# H_9716 — 능력 있음·미사용 을 숫자로 — ζ 실현권한 간극 (fable R5-5 · PROPOSED · d 정면)

**status:** 🔵 PROPOSED (미실행 · lab full R5 · 사전등록 · **ζ-fire 편승 · 추가 decode 0**) — source=fable R5-5
**lane:** mouth/tension — 동작점(operating point) vs 능력(capability) 의 분리
**related:** [[H_9664]] · [[H_9576]] · [[H_9715]] · [[H_9717]]

## 한 줄 주장 (반증가능)
[[H_9664]] ζ-fire 가 채널 GREEN 을 줘도 그것은 **"능력"이지 "사용"이 아니다.** 두 수를 곱해 분리하면 간극 자체가 사전등록 판정 가능한 양이 된다:
**A_realized = slope_ζ × sd(z)_live** vs **A_potential = slope_ζ × range(ζ 사다리)**, 이용률 **U = sd(z)_live / range_ζ**.
주장: **U < 0.05** — 라이브 데몬은 자기 채널의 **5% 미만**만 쓴다.
⟹ 브리핑 (d) 의 "간극 자체를 측정 대상으로" 에 대한 직답: **간극 = 기울기 × 분산의 비**.

## 왜 이 분해가 필요한가
ζ-fire 는 **ζ 를 우리가 정한다** — 사다리 범위는 설계값이다. 라이브는 **z 를 기질이 정한다** — sd(z)≈0.038~0.100. 채널 GREEN 은 `slope ≠ 0` 만 말하지 **라이브가 그 slope 위 어디에 서 있는지** 말하지 않는다. 두 실험이 각각 반쪽만 답한 채 끝나는 것을 막는다.

## 어느 KILL 을 왜 안 밟나
- **arm-간 paired**(H_9663): ζ-fire 의 **within-tick** 설계를 그대로 승계(null95 반폭 0.12 → 0.016) — arm-간 대조 신설 0.
- **readout D**(H_9629): D 미사용 — DV = ζ 사다리 slope(ζ-fire 의 인증된 판정기 `--zeta-slope`) × 라이브 sd(z).
- **용량-기아**(H_9628 사망): gain 을 **올리자는 게 아니라** 라이브 gain 이 이미 어디 있는지 **재는** 것.
- **p5**: 관측 전용 · z 미주입 · 게이트 비접촉.

## engine-native 계기
```
anima-py evaluate <clm> --zeta-slope --authority-gap --from-trace <live_trace.jsonl>
```
ζ 사다리 slope 와 라이브 sd(z) 를 **한 계기서** 산출·곱함(두 숫자를 다른 H 에서 빌려오지 않는 것이 [[H_9713]] 가 지적한 결함의 재발 방지).

## 통제군 (≥2 + 양성통제)
- **양성통제 = ζ 사다리 극단(±max) 의 Δgtext > bar** — 채널이 실제로 문다는 증거. (ζ-fire 의 🔐 격리 인증 23/23 승계.)
- null1 = ζ=0 arm(격리 인증상 **slope 0 · byte-identical** 이어야) · null2 = rng-ζ arm(같은 편집크기·무방향).

## 사전등록 판정표 (우연 아래 포함)
| 관측 | 판정 |
|---|---|
| slope 유의 ∧ **U < 0.05** | **PASS-capability-unused** — 벽 = **동작점** · 후속 = [[H_9717]] dispersion dose |
| slope 유의 ∧ **U > 0.5** | **KILL-already-used** — 라이브가 이미 채널을 씀 ⟹ **z 축퇴 서사 자체 폐기** |
| slope 유의 ∧ 0.05 ≤ U ≤ 0.5 | **회색 — 사전등록 미결** ⟹ 판정 보류(밴드를 사후 이동 금지 = tune-to-green) |
| **slope ≈ 0** (ζ-fire KILL) | **VOID** — 능력이 없으면 권한 간극은 정의 불가(0×0) · **음성 아님** |
| ζ=0 arm 의 slope ≠ 0 | **INVALID** — 격리 파손(23/23 인증과 모순) |
| **우연 아래**: slope 부호가 ζ 방향과 **반대** | **INVALID** — 사다리 배선 뒤집힘 |

**검정력**: ζ-fire within-tick n≈300 ⟹ null95 반폭 0.016 ⟹ slope se 작음. U 는 비율 ⟹ delta-method CI. **U 의 CI 가 0.05 와 0.5 를 동시에 덮으면 VOID** (회색 칸의 검정력 방어).

## 비용
**$0** — ζ-fire 편승(추가 decode 0). ζ-fire 판정 착륙이 **개봉 조건**.

## 죽는 방식
U > 0.5 면 죽는다 — 라이브는 채널을 이미 쓰고 있고 "능력 있음·미사용" 프레임이 틀린 것이다.

## 상태
🔵 PROPOSED — **개봉 조건 = [[H_9664]] ζ-fire 판정 착륙.** ζ-fire KILL 이면 이 안은 VOID(음성 아님). 측정 주장 0(설계).
