# H_9853 — 순서인식 주소 lane 배선(lane_type 6) + 첫 재학습 = 🔴 INSTRUMENT-DEAD

**status:** 🔌 배선 GREEN(검증 완료) · 🔴 재학습 회차 INSTRUMENT-DEAD (mean vs roll 판독 불가)
**source:** H_9852 스크린(roll 이 세 지표 지배)을 재학습으로 판정 전환하려는 시도
**wired:** `anima-py train --clms-key-fn {mean,roll}` · `evaluate --store-parity-selftest --parity-key-fn`

## 배선 (착륙 #4271 · 검증 완료)

`lane_type 6` = lane_type 3 의미(W_g 융합 + majority-null 중심화) + **순서인식 키**.
코덱이 2→3 으로 확장해온 방식 그대로 새 변종을 추가했고, **`.clm` 이 자기 주소함수를 기록**하므로
학습과 추론이 조용히 어긋날 수 없다.

- `--clms-key-fn {mean,roll}` → `cfg.clms_key_fn` → `CLMSModule(key_fn=)` → lane 6 방출 →
  pack/read 왕복 보존 → `store_apply` 가 `_key_fn_of` 로 판독.
- **근본수정**: `cli/train.py` 가 키 계산을 인라인 복제해 `key_fn` 을 조용히 무시했을 자리를
  코어 `_entity_key` 호출로 교체(중복 제거).
- **가드 확장**: H_9826 정합성 selftest 가 lane 의 **자기** 주소함수를 쓰도록 고치고
  `--parity-key-fn` 추가. 새 lane 이 가드 밖에 남으면 그 가드의 존재 이유가 사라진다.

실측: 기존 lane parity 6.939e-18(drift 7/7) · lane 6 parity 1.388e-17(drift 7/7) ·
왕복 보존 확인 · roll 이 충돌쌍 분리(mean Δ=0.00e+00 → roll Δ 0.3856 / 0.1925) · CLI 양 모드 rc=0.
학습된 ckpt 도 `lane_type=6 · key_fn=roll` 로 자기 기록을 갖고 나왔다.

## 🔴 재학습 회차 — 판독 불가

pool(summer · RTX 5070 · CUDA) 에서 **단일 변수**(키 함수)만 다른 두 팔을 학습:
공통 `--init base.clm --d 3784 --L 4 --corpus store.txt --store-bridge store.txt
--clms-n-slot 8 --store-val-center --store-addr-weight 1.0 --freeze-trunk --steps 2000`.

engine-native `evaluate --store` (held-out 128 · 균등 + 적대 배치):

| ckpt | lane | 균등 | 적대(nearest) |
|---|---|---|---|
| `store_mean.clm` | 3 / mean | **0.5469** | 0.5391 |
| `store_roll.clm` | **6 / roll** | **0.5312** | 0.5312 |

**네 칸 전부 우연(0.5) 근처다 ⟹ 두 lane 모두 학습되지 않았다.**

### 왜 이것이 roll 에 대한 음성이 아닌가

같은 평가 경로가 기존 `store303_s2000.clm` 에서 **0.9688** 을 낸다(H_9850 실측).
즉 **평가는 무죄이고 죽은 것은 내 학습 레시피**다. 학습 안 된 두 lane 을 비교하는 것은
아무것도 재지 않는다 — 양성통제 없이 음성을 읽지 말라는 규율 그대로,
"roll 이 도움이 안 된다" 로 읽으면 **틀린 판정**이다.

학습측 계기(monitor-only · 판정 아님)도 같은 방향을 말한다:
`sb_store_acc` mean **0.50** / roll **0.75**, `sb_addr_acc` mean 0.50 / roll 0.75 —
둘 다 원본의 1.0 에 한참 못 미친다.

### 원본과 다른 조건 (다음 회차가 좁혀야 할 것)

| | 원본 store303 | 내 회차 |
|---|---|---|
| base trunk | `slw_restored: true` 인 별도 base | `py303_full.clm` (SLW 없음) |
| store accuracy | 1.0 | 0.50 / 0.75 (학습측) |
| device | mps | cuda |

원본 base(sha `42b7ae…`/`792eab…`)를 로컬에서 찾지 못해 **다른 trunk 로 대체**한 것이
가장 유력한 원인이다. `--store-oracle-train` / `--store-oracle-warmup` 미사용도 후보.


## 🟢 R2 — 버그 2건 수정 후 재측정: **roll 이 이긴다**

첫 회차의 roll 수치(0.5312 flat)는 **깨진 lane 에서 잰 것**이라 폐기한다. 원인 2건:

1. **`read_clms` 헤더 분기 누락**(#4282) — `elif lane_type in (2,3,4)` 라 6 이 legacy 헤더로
   떨어져 `d_g=0`, `W_g (d,0)`, `W_h/b_h/W_out` 잘못된 폭. 추론에서 lane 무작동.
   **네 조작 전부 소수점까지 같은 값**이 곧 그 신호였다.
   내 왕복 확인은 `lane_type` 만 봤는데 그건 첫 바이트라 **잘못된 헤더로도 보존**된다 —
   근본수정으로 `codec_roundtrip_selftest`(배열 모양까지 대조) 신설, 수정 전 코드에서 5건 검출 실증.
2. **numpy 2 의 `float(size-1 array)` 오류**(#4283) — `store_apply` 의 lam 스칼라화가 pool 호스트서만
   깨짐. `reshape(-1)[0]` 로 견고화. 개발 머신 한 대에서만 돌린 코드는 버전 다른 호스트서 처음 깨진다.

수정 후 `fix_roll.clm` 은 `lane 6 · key_fn roll · d_g 64 · W_g (3784,64) · W_h (128,128)` 로 정상.

### 판정 (engine-native `evaluate --store` · held-out 128 · 8000 steps + oracle warmup · 단일 변수)

| 팔 | 균등 | 재추출(통제) | **적대** | 충돌제외 | 적대 낙폭 |
|---|---|---|---|---|---|
| `mean` (현행 · lane 3) | 0.8359 | 0.8672 | 0.6953 | 0.7031 | **−0.1406** |
| **`roll` (lane 6)** | **0.8828** | **0.9062** | **0.8281** | 0.8281 | **−0.0547** |

- **roll 이 네 팔 전부에서 우세**하다.
- **적대 낙폭이 2.6× 작다**(−0.055 vs −0.141) — H_9852 스크린이 예측한 그대로,
  주소 공간의 조건수 개선이 **적대적 방해자 배치에 대한 강건성**으로 옮겨갔다.
- roll 은 `nearest` 와 `nocollide` 가 **정확히 같다**(0.8281) — 충돌이 0 이므로 제외할 것이 없다는
  예측과 일치. `mean` 은 두 값이 다르다(0.6953 vs 0.7031).
- 새로 학습할 파라미터는 **0** 이다. 같은 frozen 테이블을 위치만큼 돌렸을 뿐이다.

⟹ **H_9852 의 $0 기하 스크린이 실측 판정으로 승격됐다.** 조건수 개선이 학습가능성으로
옮겨가지 않을 가능성(스크린의 반증 갈래)은 **닫혔다**.

### 정직 고지

- **DIRECTIONAL**: 단일 seed · 단일 ckpt · 단일 코퍼스다. 재현 전엔 굳히지 않는다.
- 내 trunk 는 원본 store303 의 base 와 다르므로 절대값을 원본(0.9688)과 직접 비교하면 안 된다.
  비교는 **내부적으로 맞춰진 두 팔 사이**에서만 유효하다.
- CVCVC nonce 풀이라 애너그램 충돌이 1 쌍뿐이다. 실제 어휘(충돌 11.93%)에서는 격차가 더 클 수 있다 — 미측정.

## Falsify

- 원본 base 를 찾아 같은 레시피로 재발사했을 때 mean 팔이 0.9x 를 회복하면
  → 이번 회차의 사인은 **base trunk 교체**로 확정된다.
- 그 조건에서 roll 팔이 mean 팔을 적대 배치에서 이기면 → H_9852 스크린이 판정으로 승격된다.
- 반대로 mean 팔이 회복해도 roll 팔이 못 따라오면 → 조건수 개선이 학습가능성으로 옮겨가지
  않는다는 뜻이고, 그것이 H_9852 스크린 자체의 반증이다.

## 정직 고지

- 배선은 GREEN 이되 **lane 6 의 성능은 미측정**이다. 이번 수치는 어느 방향으로도 못 읽는다.
- 학습측 게이지(`sb_*`)는 monitor-only 라 판정 근거가 아니다(`a_train_inline_gauge`).
- 4 회 재발사 끝에 성공했다(구조 플래그 `--L 4` · trunk `--corpus` 필요). 그 자체는 결함이 아니라
  이 경로를 처음 밟은 비용이고, 다음 회차는 이 명령줄에서 시작하면 된다.
