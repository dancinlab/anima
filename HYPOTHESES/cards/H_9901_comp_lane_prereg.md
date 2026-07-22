# H_9901 — 조성 lane 발사 (사전등록 · 양성통제 **동시** 발사)

**status:** 🔒 PRE-REGISTERED — 선결·판정표·통제 전부 **발사 전** 동결
**wired:** `train --comp-lane` ([[H_9900]]) → `evaluate --rho-axon --grow-window --weave-panel`
**source:** [[H_9898]] replay 가 원인 · [[H_9900]] lane 구현 · [[H_9869]] 양성통제 교훈

## 이 발사가 검정하는 것

[[H_9898]]: 조성과 언어가 **같은 트렁크 CE 를 공유하면** 조성이 안 들어간다(등노출 대조).
[[H_9900]]: lane 의 CE 는 **트렁크에 gradient 를 주지 않는다**(`pen.grad is None` 검증).

⟹ **예측**: replay 를 25% 로 유지해 언어를 지키면서(=선결 통과 지점),
조성을 lane 으로 넣으면 **둘 다 성립**한다. 밀도 축에서 불가능했던 조합이다.

## 🔒 팔 (발사 전 확정)

| 팔 | 코퍼스 | lane |
|---|---|---|
| **LANE** | `mix_25.txt` (드릴 25% + replay) | `--comp-lane` **ON** |
| **CTRL** | `mix_25.txt` (동일) | OFF ← [[H_9889]] 에서 이미 측정: `weave 0.000` |

CTRL 은 재실행하지 않는다 — 동일 코퍼스·동일 스텝의 값이 이미 있고,
**재측정하면 그것이 곧 두 번 뽑기**다.

## 🔒 선결 무효조건 (BLOCKING)

1. `HILLOCK` = LIVE
2. **`ρ·form` 축 == PASS** (val 아니라 축)
3. `self-shuffle ≤ 0.05`
4. **양성통제**: SEEN 슬라이스에서 `ρ·weave` reach **≥ 0.30** ← [[H_9869]] 가 6팔을 태운 항목

⚠️ **④ 를 이번엔 held-out 과 동시에 발사한다.** 앞선 캠페인은 held-out 만 재고
양성통제를 나중에 걸어 전부 VOID 가 됐다. 같은 실수를 반복하지 않는다.

## 🔒 판정표 (동결 · BASE = [[H_9861]] 0/212, 95% 상한 0.0142)

| 조건 (선결 4/4 전제) | 판정 |
|---|---|
| `ρ·weave` **PASS** (reach≥0.30 ∧ 통제 3종≤0.15 ∧ reach≥3×worst) | 🔑 **G1 BREAK** — 2 seed 필수 |
| reach > 0.0142 ∧ FAIL ∧ 통제 3종 ≤0.15 | 🟡 PARTIAL |
| reach 상승했으나 어느 통제든 > 0.15 | 🔴 ECHO-KILL |
| reach ≤ 0.0142 | 🔴 **NEGATIVE — lane 분리도 실패** |
| 선결 1~4 중 하나라도 실패 | ⛔ INVALID |

**2 seed 요건**: [[H_9859]]·[[H_9883]] 이 정확히 이 시험에서 무너졌다. seed 7·11 양쪽 성립시만 캠페인 주장.

## ⚠️ 발사 전에 적어두는 예상 실패 모드

[[H_9900]] 이 이미 지적했다: **`ρ·weave` 는 트렁크 mouth 로 디코드한다.**
lane 이 조성을 완벽히 배워도 그것이 mouth 로 나오지 않으면 `reach` 는 **0 에 머문다.**
⟹ 그 경우 판정은 🔴 NEGATIVE 가 아니라 **배선 문제**이고, 그것을 구별하려면
lane head 자체의 held-out 정확도를 따로 봐야 한다 —
**이 카드는 그 구별을 사후에 만들지 않기 위해 지금 적어둔다**(`a_verified_must_wire`).

## Cross-links

[[H_9900]] lane · [[H_9898]] 원인 · [[H_9869]] 양성통제 · [[H_9889]] CTRL 값 · [[H_9861]] BASE
