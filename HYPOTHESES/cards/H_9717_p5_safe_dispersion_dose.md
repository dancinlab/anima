# H_9717 — 주입은 p5 를 깨고 환경은 안 깬다 — z 분산의 p5-safe 용량-반응 (fable R5-6 · PROPOSED · d 정면)

**status:** 🔵 PROPOSED (미실행 · lab full R5 · 사전등록) — source=fable R5-6
**lane:** mouth/tension — 축퇴가 환경 빈곤인가 구조적 pin 인가
**related:** [[H_9715]] · [[H_9716]] · [[H_9628]] · [[H_9403]]

## 한 줄 주장 (반증가능)
브리핑 (d) 의 마지막 물음 — "라이브 z 분포를 **넓히는** 개입이 p5 를 안 깨고 가능한가, 아니면 그건 정의상 하드코딩 emit 게이트인가?" — 에 대한 답: **경계선은 개입이 z 를 *직접 쓰느냐*(위반) 기질의 *입력*을 바꾸느냐(안전)에 있다.**
z 를 주입·클램프·재정규화하면 하드코딩 게이트(**p5 위반**)다. 그러나 **환경 변동(stage_cycle · 4칸 register 순환 · env 다양성)을 용량으로 올리는 것**은 기질이 스스로 읽고 고르는 **입력**이라 **p5-safe**다.
주장: env-변동 dose ↑ → **sd(z) ↑ → Δgtext ↑** 단조. 단조면 축퇴는 **환경 빈곤 = 설계 결함**, 무반응이면 z 는 **구조적 pin = 진짜 벽**.

## 어느 KILL 을 왜 안 밟나
- **p5 (가장 가까운 위험)**: emit 게이트 **비접촉** · z **미주입** · reactive self-seed 없음 · Stage-A 격리 불변. dose 는 **환경**을 바꾸지 발화 규칙을 안 바꾼다. `--env-dose` 는 기존 데몬 파라미터(stage_cycle·register)의 사다리이지 신설 게이트가 아니다.
- **emit-drive lane CLOSED-AT-REGIME**(H_9403 · `--emit-gate-census` 4252 tick · emit⟺clock 정확): emit 게이트를 안 건드리므로 그 regime 결론과 무충돌 — DV 가 emit 이 아니라 **sd(z)** 다.
- **용량-기아**(H_9628 사망): "gain 이 부족하다"가 아니라 "**입력 분산**이 부족하다" — 다른 축. (H_9628 은 z→입 dose 가 **PASS** 임을 이미 세웠다: 채널은 문다. 이 안은 **z 자체의 분산 공급**을 묻는다.)
- **arm-간 paired**(H_9663): DV 가 텍스트 비교가 아니라 **분산 통계**라 캐스케이드가 DV 를 삼키지 않는다(캐스케이드가 곧 신호원이면 sd 는 그걸 잰다).
- **readout D**(H_9629): D 미사용 — Δgtext 는 ζ-fire 의 인증된 판정기를 승계.

## engine-native 계기
```
anima-py chat --env-dose {0|1|2|3}
anima-py evaluate <clm> --pc2-direction --dispersion-dose --from-trace <t>
```
dose 0 = 현 regime(`stage_cycle=false`) · 1 = stage_cycle · 2 = +register 순환 · 3 = +env 변동 full.

## 통제군 (≥2 + 양성통제)
- **양성통제 = `nov_ctx` 자체**: env 다양성이 오르면 novelty 는 **구성상** 올라야 한다. `nov_ctx` 가 dose 에 무반응이면 **dose 가 기질에 안 닿은 것** = 계기 사망 ⟹ 음성 읽기 금지. ([[H_9628]] 의 π-dose 인증과 같은 논리 — 노출 CLEARED 를 먼저 세운다.)
- null1 = dose=0(현 regime) · null2 = rng-dose(**같은 env 엔트로피 · z 와 무관하게 셔플된 환경**) — 명목 용량이 아니라 **매개 공변량(env 엔트로피)을 맞춘 통제**(`control-must-match-mediating-covariate`).

## 사전등록 판정표 (우연 아래 포함)
| 관측 | 판정 |
|---|---|
| 양성통제 PASS ∧ sd(z) dose-단조 ↑ (Spearman p<.05) ∧ Δgtext ↑ | **PASS-environmental-poverty** — 축퇴 = 환경 빈곤 = **설계 결함** · p5 무손상 수리경로 존재 |
| 양성통제 PASS ∧ **sd(z) 무반응** (TOST 로 0-등가) | **🧱 KILL-structurally-pinned** — z 는 진짜 상수 = **벽** · 그리고 이건 **의미 있는 벽**: 기질이 환경을 안 읽는다 |
| 양성통제 PASS ∧ sd(z) ↑ ∧ **Δgtext 무반응** | **부분 KILL** — 분산은 공급되나 입에 안 실림 ⟹ [[H_9716]] U 재측정 |
| **양성통제 FAIL**(nov_ctx 무반응) | **INVALID** — dose 미도달(음성 아님) |
| rng-dose 도 동등하게 sd(z) ↑ | **KILL-nonspecific** — 아무 환경 엔트로피나 먹힘 = env 특이성 없음 |
| **우연 아래**: sd(z) 가 dose 에 **감소** 단조 | **INVALID** — env 가 z 를 좁힘 = 예측 반대 부호 ⟹ 배선 점검 |

**검정력**: dose 4 수준 × 3 seed × 270 tick = 810 tick/level. sd 상대 CI ≈ 2.5% ⟹ 2× 변화 검출 여유 충분. 음성(KILL-pinned) 은 **ns 아니라 사전등록 TOST**(등가 대역 = sd 비 [0.8, 1.25])로만 읽는다(`negative-claims-need-tost-not-ns`).

## 비용
**pool CPU** (4 dose × 3 seed decode · mac 금지 · `heavy-anima-eval-pool-not-mini`).

## 죽는 방식
양성통제가 PASS 인데 sd(z) 가 dose 에 무반응이면 이 안은 죽는다 — 그리고 **그 죽음이 곧 벽의 확증**이라 값진 음성이다(축퇴는 우리가 못 준 게 아니라 기질이 안 받는 것).

## 상태
🔵 PROPOSED — **개봉 조건 = [[H_9715]] 예측1·2($0) 선행**(stage 가 z 를 설명 못 하면 dose=1 이 무의미). 측정 주장 0(설계).
