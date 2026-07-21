# H_9826 — 학습 구현과 추론 구현이 **여전히 같은가**? (주석 동기화를 실행 검사로)

**status:** 🔧 INSTRUMENT LANDED (계기 착륙 · 실측 PASS) · 2-production 무결성 가드
**source:** `lab/v2/gradcheck.py` `--selftest` 규율 (v2 카드 = source, 수치 이식 없음)
**wired:** yes — `anima-py evaluate --store-parity-selftest [--parity-tol 2e-5]`

## Question

store lane 은 **두 번** 쓰여 있다 — `CLMSModule.forward`(torch, 학습)와 `store_apply`(numpy, 추론).
둘을 맞춰 온 것은 **주석 한 줄**뿐이었다(`core/clms.py`: "Op order MIRRORS core/clms.store_apply 6–14").
조용한 연산순서 발산은 판정을 **양방향으로** 움직이는데 이를 잡는 실행 검사가 0이었다
(origin/main 재검증: `parity` 언급 9건 전부 주석, `def`/`assert` parity 0).

## Intervention

무작위 `CLMSModule` 1개 → `clms_weights_from_torch` 로 numpy 변환 → **같은 입력**으로 두 경로를
돌려 `max|Δ|` 비교. 이어서 텐서를 하나씩 **자기 스케일로 재표집**(두 구현이 그 텐서에서 어긋난
현실적 형태)하고 그 발산이 전부 잡히는지 확인 — 가드는 실패할 수 있음이 보여진 뒤에만 믿는다.

## 🔑 작동점 — 왜 `q_scale` 이 있는가 (가정 아니라 실측)

첫 실행이 **`W_q` 손상을 놓쳤다**(Δ 1.3e-05 < tol). 원인은 버그가 아니라 작동점: 무작위 초기화에서
주소 softmax 가 거의 균등(a_max 0.1281 vs 균등 0.1250)이라 `v = a·V_slots` 가 주소 변화에 거의
반응하지 않는다 ⟹ 그 지점에서 `W_q` 불일치는 **원리적으로 안 보인다**. 영향력은 질의 스케일과
단조 증가하고 **정합성은 모든 지점에서 정확**했다:

| q_scale | a_max | parity | W_q 손상 Δ |
|---|---|---|---|
| 1 | 0.1281 | 1.39e-17 | 1.283e-05 ❌ 미검출 |
| 4 | 0.1376 | 0.00e+00 | 5.147e-05 |
| 8 | 0.1512 | 6.94e-18 | 1.032e-04 |
| 16 | 0.1808 | 1.39e-17 | 2.066e-04 |

⟹ 잘 스케일된 지점에 놓고, **주소 영향력을 전제조건으로 assert** 한다(a_max > 1.10×균등).
평평한 지점에서 손상 팔을 읽는 것이 가드를 가짜로 만든다. `q_scale=8` 채택.

## Result — 실측

```
tolerance = 2.0e-05  (torch fp64 vs numpy fp64) · q_scale = 8.0
  parity (uncorrupted)   max|delta| = 6.939e-18   PASS
  address influence      a_max = 0.1512 (uniform 0.1250)   PASS
  drift W_q   1.032e-04 CAUGHT   drift W_g   2.118e-01 CAUGHT
  drift val   1.898e-03 CAUGHT   drift W_h   1.683e-01 CAUGHT
  drift b_h   5.009e-02 CAUGHT   drift W_out 1.433e-01 CAUGHT
  drift lam   1.152e-01 CAUGHT
SELFTEST PASS ✓
```

- **numpy 거울은 torch 트레이너와 실제로 일치한다**(6.9e-18) — 주석이 지금까지는 맞았다. 이제 그것이
  검사로 강제된다.
- 7/7 텐서 발산이 잡힌다 ⟹ 이 가드는 실패할 수 있다.
- torch 없는 numpy-only 설치: **SKIPPED · rc=3**, 절대 PASS 아님(안 돌린 가드가 성공을 출력하는 것이
  이 계기가 막으려는 실패 양식이다).

## 부수 관측 — arm64 허위 FPE 재확인

`h @ W_g` 등에서 numpy 가 divide-by-zero/overflow RuntimeWarning 을 뱉지만 **모든 값이 유한**하다
(이 repo 기존 기록과 일치). 오진 방지로 경고 대신 **유한성**을 assert 한다.

## Falsify

- parity Δ 가 tol 을 넘으면 → 두 구현이 실제로 갈렸다. 어느 쪽이 맞는지는 이 계기가 답하지 않는다.
- 어떤 텐서가 MISSED 면 → 그 텐서에 대해 가드가 눈이 멀었다. 작동점부터 의심하라(위 표).
- a_max 전제조건이 깨지면 → 손상 팔 전체가 **판독 불가**, PASS 로 읽지 말 것.

## 정직 고지

- 이것은 **무결성 가드**이지 능력·의식 판정이 아니다. 어떤 bar 도 움직이지 않는다.
- 무작위 모듈 1개·1 작동점의 검사다. 학습된 ckpt 전 구간 동치의 증명이 아니다.
- lane_type 2 경로만 덮는다 — lane_type 3/4/5(RV-3·CLMS-FAN·fresh-query)는 **미커버**.
