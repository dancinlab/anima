# H_9855 — 경직 담체가 모델을 망가뜨렸다 (falsidrill 담체 3→12)

**status:** 🔧 계기 수리 (과학 판정 0) — [[H_9837]] REAL 팔이 **실측한** 손상의 직접 원인 교정
**wired:** yes — `anima-py corpus falsidrill [--falsi-ablate]` (담체 12 · 기본값)
**source:** [[H_9837]] REAL 팔 — `ρ·form` PASS→FAIL, 통제 `self-shuffle 0.0 → 0.4`

## 무엇이 망가졌나 (추측 아님 · 실측)

[[H_9837]] REAL 팔(2000 step CPT · 15% 드릴 혼합) 판독:

```
CARRY  ρ·form  FAIL  val=1.0 Δ=0.6 · self-shuffle=0.4     (BASE: PASS · Δ=1.0 · shuffle 0.0)
```

**val 은 미동인데 통제가 죽었다.** 바이트를 뒤섞은 자기 출력이 form 게이트를 **40%** 통과한다
(상한 0.05) ⟹ 출력이 **순서가 무의미한 기지단어 자루**가 됐다.

**원인**: 담체 3종을 24,000줄 반복하면 모델은 단어 **정체**만 배우고 **순서**는 배우지 않는다.
그러면 셔플해도 점수가 안 떨어진다 — 정확히 관측된 그대로다.

## 교정

담체 **3 → 12**(양 팔 동일). 조건절 선행/후행 두 어순, 길이 가변, 비교구문 추가 —
**순서를 정보로 유지**하면서 반증가능 구조(비교어 ∧ 측정어)는 불변.

| 팔 | 줄 | 반증가능 | 담체 | held-out 누수 |
|---|---|---|---|---|
| real | 600 | **600 (1.0000)** | 12 | 0 |
| ablation | 600 | **0 (0.0000)** | 12 | 0 |

## 🔑 부수 교정 — 기능어를 held-out 하면 문법만 굶는다

담체가 12로 늘자 감사가 한 프레임의 `when` 을 held-out 위반으로 막았다. 그런데 `when` 은
**개념이 아니라 기능어**다(평가문 `the engine dreams when alone` 유래). held-out 축은 **평가 개념**
이므로 내용어만 강제하고 기능어(`when`·`from`·`into`·`the`·`new`·`between`·`still`)는 분리했다 —
기능어는 replay 코퍼스와 영어 전반에 편재하므로 막는 것이 **무의미하고 불가능**하며, 드릴에서
문법만 굶긴다.

## 이 카드가 판정하지 않는 것

계기 수리다. 이 담체로 다시 학습한 결과는 **아직 없다**. 재발사는 [[H_9837]] 의 FORGET 게이트를
**축 PASS/FAIL + 전 통제값**으로 재설계한 뒤에만 유효하다(convergence
`forget-gate-must-read-the-axis-verdict-not-the-reinforced-value`).

## 재생성 커맨드

```
anima-py corpus falsidrill --out fd_real.txt --n-blocks 600 --seed 7
anima-py corpus falsidrill --out fd_abl.txt  --n-blocks 600 --seed 7 --falsi-ablate
```

## Cross-links

[[H_9837]] 손상을 실측한 팔(동기) · [[H_9828]] 밀도 목표수치의 유래 · [[H_9829]] 연속 rate 판독
