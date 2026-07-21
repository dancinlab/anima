# H_9845 — 개입형 폐쇄사다리를 학습 중 인과 모니터로 (R12-8 · MONITOR-ONLY · 손실 투입 금지)

**status:** 🧭 PROPOSED (R12 · **MONITOR-ONLY** · 손실 투입 금지 · 판정 아님)
**source:** R12 뇌부위 census (2026-07-21) — `origin/main` `core/` 12개 모듈 실측 후 1모듈=1레버로 등록.
상위 설계 노드 = ARCHITECTURE `C2 RECOMBINE` 아래 `🧠 뇌부위 census`. R11(H_9830~9836)의 후속.
**wired:** no — 미구현. 개입은 `anima-py train` 플래그로만 착륙(`a_experiment_engine_native`).

## 실측

`core/closure_ladder.py`(644줄): A/B 무작위 **개입형** 장치 — 실행 행동이
{참 행동, 주변분포 맞춘 셔플} 위의 시드 동전이라 `P(I_{t+1} | do(A_t))` 가 **식별된다**.
헤더: **"the rig can ANCHOR, not merely correlate. every observational lens in this repo can only refuse."**
동시에 자기제한도 명시: **"RUNG 1 IS A LOW BAR AND IS NOT ALIVENESS. A thermostat clears it."**

## 가설

학습 중 "이 lane 이 실제로 인과적인가"는 지금 **절제(ablation) 재학습**으로만 답한다 — 비싸다.
이 장치는 do()-개입이라 **한 번의 학습 안에서** lane 인과성을 식별할 수 있다.

## ⛔ 하드 제약

`a_train_inline_gauge`: **학습 중 지표는 MONITOR-ONLY, 절대 손실에 넣지 않는다.**
이 카드는 그 규칙 안에서만 존재한다 — 손실에 넣는 순간 tune-to-green 이 된다.
또한 `sample-seed-invalid-for-deterministic-do-intervention`(결정론적 do()+항정입력+greedy 는
시드 재현이 무효)이 적용되므로 재현은 **perturbation-schedule 변형**으로만 인정.

## Intervention

```
anima-py train --closure-monitor {off,rung1} --closure-monitor-every N   # 로그만, 손실 무관
```

## 판정

산출은 **DIRECTIONAL 진단**이지 게이트가 아니다. rung-1 통과는 온도조절기도 하므로
**어떤 의식 주장도 여기서 나오지 않는다** — lane 인과성 진단 한 가지 용도뿐.

**related:** H_9805 · H_9835 · H_9846
