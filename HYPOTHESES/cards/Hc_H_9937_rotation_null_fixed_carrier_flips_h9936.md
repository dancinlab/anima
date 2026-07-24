# H_9937 · 고정 carrier + 회전 null: 학습본이 압도한다 — H_9936 의 "null 밑"은 self-sampling artifact였다

**한 줄:** self-sampling 없는 **고정 held-out carrier** 로 MI 를 재고, Sol 이 지목한 **회전 null**
(학습 오프셋을 강체 회전 → 노름·Gram·평균·실현변위 D 모두 보존, 방향만 파괴)로 통제하면, 판정점
gs=0.1 의 학습본 3 seed 가 회전 null 을 **z=+28~+38 로 압도(PASS>q99)**. H_9936 의 "판정점서 무작위
null 밑, FAIL" 은 **self-loop carrier(각 게이트가 자기 분포로 샘플·채점하는 대각 artifact)** 위에서
잰 것이었다 — H_9933 이 swap 을 비판별로 만든 바로 그 병이 등방 null 의 MI 를 부풀렸다.

- 신설 계기: `core/clmg.py::random_orthogonal`/`rotate_offsets` + `cli/graft.py graft check --rotation-null N`.
  단위검증 6/6: R 직교성 2.4e-07 · 노름 4.8e-07 · Gram 1.5e-05 · 평균 1.7e-07 · **RMS(=변위) 0.0e+00** ·
  방향이동 4.32(항등 아님). 회전은 D-EXACT 통제 — 등방 null(D 만 근사)보다 강하다.
- 설치본 = 로컬 파일 동일 확인. regime `no-corpus` · scope TOY(`trained57`) · `a_toy_scale_recheck`.

## 결과 — 두 측정이 정반대, 고정 carrier 가 옳다

**① 회전 null (고정 carrier · n=64 · 판정점 gs=0.1)**
| seed | 학습본 MI | 회전 null mean / q99 | z | 판정 |
|---|---|---|---|---|
| 1 | 0.2150 | 0.0218 / 0.0392 | +27.8 | PASS(>q99) |
| 2 | 0.3186 | 0.0349 / 0.0524 | +32.2 | PASS(>q99) |
| 3 | 0.2735 | 0.0280 / 0.0461 | +37.6 | PASS(>q99) |

**② 같은 고정 carrier 로 등방 null(step0, 학습0회) 재측정** — 학습본이 10~12배 압도
| seed | 학습본 MI | 등방 null MI | 비율 |
|---|---|---|---|
| 1 | 0.2150 | 0.0175 | 12.3× |
| 2 | 0.3186 | 0.0337 |  9.5× |
| 3 | 0.2735 | 0.0273 | 10.0× |

## 왜 갈렸나 — 측정 방식이 진범
- **self-loop carrier(H_9936·fit)**: 각 상태가 자기 게이트로 continuation 을 샘플 → 그 상태의 분포에서
  뽑은 텍스트라 그 상태가 잘 예측(대각 우도 이점). 무작위 게이트도 자기 텍스트는 잘 예측하고, **진폭이
  클수록** 그 이점이 커진다(H_9935). H_9936 은 등방 null 을 gs=0.4 로 올려 D 를 맞췄으므로 그 큰-진폭
  무작위 게이트가 대각 이점을 크게 받아 학습본을 "이겼다".
- **고정 carrier(이번·Sol 요구)**: 모든 상태를 같은 외부 held-out 텍스트로 채점 → 자기 텍스트 이점 소멸
  → 순수하게 "codes 가 그 텍스트에서 상태를 구분하는가". 여기서 학습본의 정렬이 드러나고 두 null 모두
  10배+ 압도.

## 판정 — 🟢 GRAFT 는 실재 상태구분을 학습한다 (toy · 고정 carrier · 회전+등방 null 압도)
- 학습이 codes 를 언어기관의 민감한 방향에 정렬시켰음이 **displacement-exact 회전 null** 로 확인된다
  (같은 D·같은 Gram, 방향만 다르면 MI 1/10). 이는 "우위=변위 매개"(H_9936)를 반증한다.
- ⚠️ **verdict-integrity 정정**: H_9936 의 결론 한 줄("GRAFT 우위=변위 매개, 판정점서 null 밑, 상태구분
  아님")은 self-loop carrier 측정 artifact 였다. H_9936 의 유효한 부분은 남는다 — gs-매칭 lift 가 진폭
  교란이라는 것, D=MI+L_common 프레임, η. 뒤집히는 것은 등방-null 비교의 판정 방향뿐이며, 그 원인은
  null 종류가 아니라 **MI 를 self-sampling 으로 쟀다는 것**이다.
- ⚠️ 정직 경계: 이것도 여전히 `MI`(고정 carrier)라는 계기 위 판정이지 자연 코퍼스 faculty 아님(p9).
  fit 목적함수는 아직 self-loop MI 를 최대화하므로, **fit 자체를 고정-carrier MI 로 바꾸면** 결과가
  어떻게 달라지는지 미측정.

## 다음
① fit 의 목적함수 MI 를 고정 held-out carrier 로 바꿔 재학습(현재 self-loop) — 학습신호 자체의 오염 제거.
② py303(TERMINAL 은 거기서만). ③ 회전 null 을 `graft check` 기본 패널로 승격(self-loop swap 은 이미 폐기).
산출물 `~/.fire-recover/graft_toy_3seed/{rotation_null,fixed_carrier_isotropic}.log`.
