# H_9938 · fit 목적함수를 self-loop→고정 carrier 로 바꿔도 학습 결과는 동등 — 오염은 측정만, 학습은 견고

**한 줄:** fit 의 MI 목적함수를 self-loop carrier(자기샘플)에서 **고정 held-out carrier**(자연 텍스트,
self-sampling 없음)로 교체해 재학습하니, rotation-null z 가 old-fit 과 **동등**(OLD +27.8/+29.9/+35.1 vs
NEW +20.4/+30.9/+32.3 · Δz 평균 약간 음수). ⟹ self-loop 의 대각 artifact 는 **목적함수 값은 부풀렸지만
gradient 는 유용한 방향(언어기관 정렬)으로도 흘러 학습된 것 자체는 오염되지 않았다.** H_9937 이 old-fit 도
고정 carrier 로 재면 압도함을 보였고, 이번엔 학습까지 고정 carrier 로 해도 동등함을 확인.

- 신설 계기: `cli/graft.py graft fit --carrier-corpus <자연텍스트> [--carrier-k K]` — self-loop 전부 제거
  (`_sample_carrier`/`buf`/carrier-health guard 미사용), MI·L_common 을 매 스텝 K=4 고정 held-out
  windows 평균으로, 모든 N state 가 같은 windows 에서 채점. train80/val20 + `ctx+T` gap 분리, 매 스텝
  seeded-shuffle w/o replacement resample. `.graft.json` 에 corpus SHA·split offsets 기록. 설계 = lab full
  (Fable+Sol) 조율 — carrier 로더 단위검증 5/5(SHA·gap≥win·window 길이·reshuffle).
- ⚠️ **(d) 조율 결정**: Fable 은 τ hinge, Sol 은 L_tail CVaR 을 목적함수에 추가 권고했으나 **둘 다 repo 가
  명시 금지한 컨트롤러 계열**(`core/clmg.py:40`·`cli/graft.py:32`: `beta·relu(L_KL−target)` FORBIDDEN,
  v2b MI 0.118→0 붕괴). 저렴한 확인(repo 규칙)이 결정 — 목적함수 `L=(logN−MI)+λ·L_common` 불변,
  collapse 는 (b)의 val 일반화 통제로 탐지. Sol dissent 1줄: L_tail 미채택.
- regime `no-corpus`(carrier 는 채점용 held-out 이지 학습 코퍼스 아님) · scope TOY · `a_toy_scale_recheck`.

## 결과 — old-fit vs new-fit (동일 init·seed·schedule · 3 seed · 400 step · 고정 carrier check)
| seed | OLD lift(self-loop carrier) | NEW val lift(disjoint) | rot-null z OLD | rot-null z NEW | Δz |
|---|---|---|---|---|---|
| 1 | +0.2194 | +0.2199 | +27.8 | +20.4 | −7.4 |
| 2 | +0.2488 | +0.2122 | +29.9 | +30.9 | +1.0 |
| 3 | +0.2713 | +0.2147 | +35.1 | +32.3 | −2.8 |

new-fit 의 val lift 는 **학습에 안 쓴 disjoint 검증 bank(64 windows)** 에서 +0.21~+0.22 → carrier 메모리
아니라 일반화(Sol 의 (b) 통제 통과). old·new 둘 다 고정 carrier check 에서 rotation-null 을 z≥20 압도.

## 판정
🟡 **스위치는 학습 결과를 유의미하게 개선하지 않음 — self-loop 학습은 대각 오염에 견고했다** · DIRECTIONAL(toy)
- 정직 경계(no tune-to-green): NEW rotation-null z 가 OLD 보다 높지 않으므로(Δz 평균 음수) "고정 carrier
  학습이 능력을 개선했다"는 **주장 불가**. 결론은 개선이 아니라 **동등**이다.
- 스위치의 가치는 능력이 아니라 **정직성**: fit 의 목적함수가 이제 측정(고정 carrier check)과 같은 표면을
  써서 self-loop 인플레이션 없이 disjoint val 에서 정직하게 읽힌다. 계기 정렬이지 faculty 진전 아님.
- 확정: GRAFT 의 학습 신호는 self-loop 오염에 견고 — 오염은 H_9933/9935/9936 처럼 **측정**을 무너뜨렸으나
  gradient 는 유용한 방향으로도 흘렀다. 측정은 고정 carrier(H_9937)로 이미 해결됐고, 학습은 애초에 괜찮았다.

## 다음
① py303(TERMINAL 은 거기서만) — 고정 carrier fit + rotation-null check 로. ② rotation-null 을 `graft check`
기본 패널로 승격, self-loop swap 은 완전 폐기. ③ 진폭 조작(gs ×0.5/×2)에 rotation-null z 안정성 확인
(Fable 의 (e) 잔여 — 진짜 방향코딩이면 z 가 진폭에 안 흔들려야).
산출물 `~/.fire-recover/graft_toy_3seed/{carrier_switch_ab,lab_fitcarrier_fable_sol}.*`.
