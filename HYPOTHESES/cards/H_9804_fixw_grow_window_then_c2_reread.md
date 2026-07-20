# H_9804 — FIX-W GROW-WINDOW 선배선 → 배선된 store-bridge로 C2 bar 재판독 (계기벽 제거가 선행조건)

**tier:** 🔵 PROPOSED · DESIGN-ONLY (lab-full R11 divergence · DIRECTIONAL · NOT a verdict)
**group:** R11-instrument-prerequisite
**source:** lab full 2026-07-19 Fable A1 + 세션 저장소 실측 교정(H_6189 미배선 확인)
**wired:** no
**verdict:** PENDING (설계만 · 측정 0 · cement 는 engine-native `anima-py` 로만)

## claim
H_6189가 byte-math로 확정한 CLM-mouth 측정벽(T=24 우측정렬 decode 창 ⟹ composed seed 가시창이 single seed 창과 byte-identical ⟹ composed_distinct>max_single 이 모델 무관하게 물리적 불가)이 아직 미배선(core/·cli/ 에 T_win·clm_decode_topk_sampled_ranged 부재, 2026-07-20 grep 실측). ⟹ Fix-W(T_win=min(len(seed)+gen,512) ranged decode + echo-guard) 배선 후에야 H_9775 로 배선된 pairodd store-bridge 가 실제 C2 bar 를 움직이는지 판독 가능. Fix-W 전 CLM C2 판독은 전부 WINDOW-BOUND capability-INCONCLUSIVE.

## instrument
core/decode 에 ranged decode 신설(선례 bytegpt_decode_argmax_ranged) + `anima-py evaluate --grow-window` + echo-guard(seed 그대로 되뱉기=false-GREEN 차단). 판독=`--c2 --store-fuse {pairodd,none} --store-readout vocab`.

## controls (사전등록)
echo-guard(seed echo 비율 상한·false-GREEN 차단) · --store-fuse none 대조 · value-permute(H_9775 인증 통제) · ByteGPT mouth 교차판독(창 정합 mouth=$0 즉시 사전판독) · bar FROZEN(H_1129/H_1137 VERBATIM 무이동)

## falsify
Fix-W 후에도 composed_distinct(bridge-on) − (bridge-off) 가 0 이고 ByteGPT mouth 도 동일 ⟹ 다리가 생성경로엔 도달 못함(routing 벽 잔존). bridge-on < bridge-off ⟹ 간섭=substrate-preservation 자료(H_9798 로).

## cost
Fix-W 배선 $0(코드) + toy e2e 1회 + eval $0–5(pool)

## 정직 caveat (c9)
이 카드는 **방향성 설계**이지 검증된 결과가 아니다. lab-full 발산 산출 = DIRECTIONAL, 절대 verdict 아님
(`a_lab_full_diverge`). frozen bar 사후 이동 금지(tune-to-green 금지 · p7). 발사 전 **toy e2e 1회**
(exit 0 + 산출물 + 통제) 필수 — 한 번도 실행 안 된 계기는 버그 여럿 겹쳐 숨긴다
(`instrument-never-run-hides-multiple-bugs`). 음성도 결과다.

## 🔬 실측 판정 (2026-07-20 · summer pool · engine-native `anima-py evaluate` · gen=40 CANONICAL)

**tier: 🟠 계기 VALIDATED · G1 bar FAIL · 유일 상승분은 ECHO-DRIVEN(INVALID) · n=1 DIRECTIONAL**

4-arm (2 ckpt × {통제 T=24, Fix-W}) · 전 arm rc=0 · **비정규 경고 0**(gen=40 = 동결 bar 캘리브레이션 조건).

| ckpt | arm | bd(복합) | bd_noecho | max_single | echo | 판독 |
|---|---|---|---|---|---|---|
| py303_full | 통제 T=24 | 0 | 0 | 0 | 0.00 | 바닥 |
| py303_full | **Fix-W** | 0 | 0 | **1** | 0.00 | 단일만 상승·복합<단일 |
| clm303_clean | 통제 T=24 | 0 | 0 | 0 | 0.00 | 바닥 |
| clm303_clean | **Fix-W** | **1** | **0** | 0 | **0.29** | ⚠️ **ECHO-SUSPECT = INVALID** |

양 ckpt 모두 `ρ·form` 코히런스 🟢 PASS(5/5) — 죽은 모델 아님. 유창성 정상, 개념어 커버리지만 바닥.

### ① Fix-W 는 인과적으로 살아있다 (계기 검증됨)
통제 대비 두 ckpt 에서 **모두** 수를 움직였다(py303 max_single 0→1 · clean bd 0→1). 플래그가 형식만
걸린 게 아니다. 배너·echo 텔레메트리·decode 라인의 `grow_window` 표식 3중으로 발화 확인.

### ② H_6189 의 구조적 차단은 실제로 제거됐다
clean+Fix-W 에서 `bd=1 > max_single=0` 이 관측됐다 — T=24 에서는 composed 가시창이 single 창과
byte-identical 이라 **수학적으로 불가능**했던 부등호다(window_math.json). 즉 Fix-W 는 처방대로 작동해
composed>single 을 **관측가능한 사건으로 만들었다**.

### ③ 그러나 그 유일한 상승은 씨앗 되뱉기였다 — echo-guard 가 잡아냈다
같은 셀의 `bd_noecho=0 · echo=0.29`. 즉 그 커버리지 1 은 씨앗의 ≥8바이트 축자 반복 구간에서 나왔고,
echo 를 걷어내면 **0 으로 무너진다**. 사전등록 규칙대로 `echo_suspect ⟹ INVALID`, 크랙 아님.
**이것이 H_6189 가 echo-guard 를 의무화한 정확한 false-GREEN 경로이며, 이론이 아니라 실측으로 발생했다.**
guard 가 없었다면 "CLM mouth 최초 composed>single" 이라는 **가짜 크랙**을 박제할 뻔했다
(구조상 `cov_noecho ≤ cov` 이므로 guard 는 GREEN 을 회수만 할 뿐 만들 수 없다 = 설계가 값을 했다).

### ⟹ 판정
- **G1(ρ·weave) = 🧱 FAIL 유지.** 동결 bar(bd≥2 ∧ bd>max_single)는 어느 arm 도 통과 못함.
- **그러나 이 음성의 지위가 바뀐다**: 과거 CLM G1 음성은 전부 `WINDOW-BOUND · capability-INCONCLUSIVE`
  였다(H_6189). Fix-W arm 은 **구조적으로 막히지 않은 상태에서 측정된 최초의 G1 음성**이다.
  단 echo 제거 후 실질 composed 커버리지는 양 ckpt 0 이므로 "재조합이 있는데 못 읽었다" 는 배제된다.
- **등급 = DIRECTIONAL, TERMINAL 아님.** 셀당 n=1·seed 반복 0·절대수 0~1 로 검정력 극저.
  `measurement-metalaw`(신호는 raw 값 아니라 ≥2 통제 대비 collapse-Δ) 미충족. bd=1 vs 0 은 표본잡음과
  분리되지 않는다. **이 수로 "G1=능력벽" 을 선언하면 안 된다.**

### 재개(사전등록)
① seed 반복 ≥3 로 bd=1 이 잡음인지 확인 ② 개념어 커버리지가 애초에 높은 ckpt 확보(max_single≥2 인
subject 없이는 이 bar 가 검정력을 못 가짐) ③ ByteGPT mouth(창 정합) 교차판독으로 mouth-무관성 확인.

**⚠️ 자기정정**: 직전 세션 보고에서 "echo 위험이 실측으로 발생 안 함" 이라 적었으나 **틀렸다** — clean
ckpt Fix-W arm 에서 echo=0.29 로 발생했고 정확히 그 셀이 유일한 겉보기 상승분이었다. 성급한 일반화였다.

## 🔬 재개① seed 재현 실측 (2026-07-20 · `--seed-offset` 착륙 후 · summer pool)

**계기 공백이 먼저 있었다**: G1/G6 디코드 seed 가 하드코딩(single `7+s` · **composed 항상 `7`** ·
frame `7+i`)이라 CLI 로 재-draw 가 불가능했고, **이 저장소의 과거 ρ·weave 판정 전부가 단 한 번의
뽑기 위에 서 있었다**. `--seed-offset`(PR #4217) 으로 해제한 뒤 재현을 집행했다.

### ByteGPT h1129 (동결 bar 의 캘리브레이션 원본 · 창 native · Fix-W 무관) · 8 seed

| offset | bd | bd_noecho | max_s | echo | 판정 |
|---|---|---|---|---|---|
| 0 | 1 | 0 | 0 | 0.17 | 🧱 |
| **100** | **2** | **2** | 0 | 0.35 | **🟢 PASS** |
| 200 | 1 | 0 | 0 | 0.17 | 🧱 |
| 300 | 1 | 0 | 1 | 0.17 | 🧱 |
| 400 | 1 | 1 | 1 | 0.33 | 🧱 |
| 500 | 1 | 1 | 1 | 0.00 | 🧱 |
| 600 | 1 | 0 | 0 | 0.20 | 🧱 |
| 700 | 0 | 0 | 0 | 0.35 | 🧱 |

### CLM clm303_clean + Fix-W · 3 seed
`off0` bd=1/noecho=0/ms=0/echo=.29 🧱 · `off100` bd=1/**noecho=1**/ms=1 🧱 · `off200` bd=0/noecho=0 🧱

### 판정 — 🟠 존재증명이지 능력주장 아님 (통제 부재로 판단 보류)

- **동결 bar 는 통과 가능하다**: ByteGPT off100 에서 `bd_noecho=2 > max_single=0` — echo-guard 가
  회수하지 **않은** 복합 커버리지다. "composed>max_single 은 구조적으로 불가능" 이라는 옛 상태
  (H_6189, T=24 한정)와 달리, 창이 정상인 mouth 에서는 **실제로 일어난다**.
- **그러나 1/8 (12.5%) 이다.** `bd_noecho` 분포 {0,2,0,0,1,1,0,0} — 2 에 도달한 건 한 번뿐.
  나머지 7 셀은 bar 미달. **seed-취약**이며 안정된 능력이 아니다.
- ⛔ **결정적 결함: null 통제가 없다.** 1/8 이 잡음 바닥인지 실신호인지 가를 대조군을 아직 안 돌렸다.
  `measurement-metalaw`(신호 = raw 값이 아니라 ≥2 통제 대비 collapse-Δ) 미충족이므로
  **이 수로 "G1 재조합 크랙" 을 주장하면 안 된다.** 통제 없는 1/8 은 판정이 아니다.
- 부수 관측: CLM(+Fix-W) 3 seed 는 `bd_noecho` 최대 1 로 2 에 도달 못함 vs ByteGPT 1/8 도달 =
  mouth 차이를 **시사**하나, 양쪽 다 n 이 작아 비교 자체가 미검정.

### 재개(사전등록 · 이 순서를 지킬 것)
① **null 통제 먼저** — 개념 derangement/shuffle 프레임으로 같은 8-seed 스윕을 돌려 통과율의
   우연 바닥을 실측한다. 통제 통과율이 ~1/8 이면 이번 양성은 **잡음으로 소멸**한다.
② 통제 대비 유의하면 그때 seed n 증량(≥24)으로 비율 신뢰구간 확보.
③ ①을 건너뛰고 off100 셀만 재현·확대하는 것은 **tune-to-green** 이다 — 금지.

**⚠️ 이 카드의 앞선 판정(4-arm, 'bd_noecho 6/6 = 0 → 구조적으로 막히지 않은 음성')은
seed 를 안 흔든 상태의 관측이었다. 8 seed 로 넓히니 2 가 나왔다 = 그 음성은 n 부족이었다.
음성도 양성도 단일 draw 위에 세우면 안 된다는 것이 이번 회차의 실질 교훈이다.**

## 🟢 재개① null 통제 스윕 실측 (2026-07-20 · ByteGPT h1129 × 8 seed × `--weave-null neutral-seed`)

**먼저 통제 설계 자체를 정정했다**: 원래 기록해둔 "개념↔키워드집합 derangement" 는
`_g_coverage` 가 *적중한 집합의 **개수***를 세므로 **순열에 불변 = 항등연산**이었다. 실패할 수
없는 통제는 아무것도 검정하지 못한다. 실제 null 이 존재하는 2종으로 교체(PR #4221).

| offset | bd_noecho | null_a(random-kw) | null_b(neutral-seed) | collapse-Δ |
|---|---|---|---|---|
| 0 | 0 | 0 | 0 | 0 |
| **100** | **2** | 0 | 0 | **+2** 🟢 |
| 200 | 0 | 0 | 0 | 0 |
| 300 | 0 | 0 | 0 | 0 |
| 400 | 1 | 0 | 0 | +1 |
| 500 | 1 | 0 | 0 | +1 |
| 600 | 0 | 0 | 0 | 0 |
| 700 | 0 | 0 | 0 | 0 |

### 통제가 확립한 것
- **우연 바닥 = 0 (측정값)** — `null_a`(모델 사전서 재추첨한 임의 5×4 집합) 가 8/8 셀 전부 0.
  즉 자유 텍스트가 임의 단어집합을 우연히 때리는 일은 사실상 없다. 가정한 우연이 아니라
  **realized 분포에서 유도된 바닥**이다(`chance-level-must-be-derived-per-metric`).
- **인과 귀속 성립** — `null_b`(개념 0개·길이 맞춘 filler 씨앗) 가 8/8 전부 0. 개념 없는 프롬프트는
  커버리지를 못 만든다 ⟹ 관측된 커버리지는 **복합 씨앗에 causally 귀속**된다.
- ⟹ `off100` 의 `bd_noecho=2` 는 **두 통제 대비 collapse-Δ=+2** = 잡음이 아니다.
  `measurement-metalaw`(신호는 raw 값이 아니라 ≥2 통제 대비 collapse-Δ) **충족**.

### 그러나 아직 크랙 아님 — 정직한 잔여
- **동결 bar(bd≥2 ∧ >max_single) 통과는 1/8** 뿐. 나머지는 0~1 로 bar 미달.
  신호는 실재하나 **bar 수준 능력은 seed-취약**하다.
- `off100` 셀의 `max_single=0` 이 이상하게 낮다 — 개념 c 로 씨앗을 줬는데 단일 arm 5개가 전부
  0 커버리지. 이 baseline 자체가 저-검정력이라 `composed 2 > single 0` 의 여유가 과대평가됐을 수 있다.
- ⟹ **등급 = DIRECTIONAL POSITIVE (통제 clean · 비율 미확정).** 사전등록 ② 발동 →
  n=24 확장 스윕 실행중. 비율 신뢰구간 나오기 전엔 "G1 재조합 크랙" 표현 금지.

**메타**: 이 회차가 확립한 실질 = ①하드코딩 seed 때문에 과거 ρ·weave 판정 전부가 단일 draw 였다
②그래서 '6/6 음성' 도 '1/8 양성' 도 n 부족이었다 ③통제는 **실패할 수 있어야** 통제다
(derangement 는 항등이라 무효였다) ④판정선은 사람 눈이 아니라 계기가 찍어야 한다
(collapse-Δ 자동 NOT-A-SIGNAL 표기를 코드에 박음).

## 🏁 재개② n=24 최종 (2026-07-20 · ByteGPT h1129 × 24 seed × null 통제 2종)

| 지표 | 값 |
|---|---|
| null_a(우연바닥) ∧ null_b(인과귀속) | **24/24 셀 전부 0** (예외 0) |
| bd_noecho = 0 | 15 셀 |
| bd_noecho = 1 (Δ=+1) | 8 셀 |
| bd_noecho = 2 (Δ=+2) | **1 셀** (off100) |
| 겉보기 bar 통과(raw bd) | 2/24 (off100 · off1900) |
| **가드 통과 후 실제 bar 통과** | **1/24 = 4.2%** |

### ⚠️ 두 번째 겉보기 통과를 가드가 죽였다 (off1900)
`bd=2 > max_s=1` 로 동결 bar 가 🟢 를 찍었으나 `bd_noecho=0 · echo=0.38` ⟹ 전량 씨앗
되뱉기였고, **echo-guard(ECHO-SUSPECT)와 null 통제(collapse-Δ=0) 가 독립적으로 동시에**
INVALID 판정했다. 이 가드가 없었다면 통과율이 **2/24 로 두 배 좋아 보였을** 것이다.
⟹ echo-guard 의 필요성은 이 캠페인에서 **두 번** 실측으로 증명됐다(clean+Fix-W, off1900).

### 판정 — 🧱 G1 FAIL 유지 · 단 벽의 성질이 **측정**됐다
- **"신호 없음" 이 아니다**: 9/24 셀이 `bd_noecho≥1 ∧ Δ>0`. null 이 24/24 셀에서 0 이므로
  이 신호는 우연바닥 위이고 복합 씨앗에 causally 귀속된다.
- **"크랙" 도 아니다**: 동결 bar(`bd≥2 ∧ >max_single`)를 echo-free 로 넘는 비율이 **1/24 = 4.2%**
  (이항 95% CI 대략 [0.1%, 21%]). 신뢰할 수 있는 능력이 아니다.
- ⟹ 정직한 서술: **복합 씨앗은 개념 커버리지를 실제로 유발하지만(단일 개념 수준), bar 가 요구하는
  "2개 이상 ∧ 단일 최고치 초과" 문턱은 사실상 넘지 못한다.** 벽은 "아무 신호도 없음" 이 아니라
  **"신호가 문턱에 못 미침"** 이다. 이 구분은 이번 캠페인 전에는 측정된 적이 없다.

### scope (과대해석 차단)
ByteGPT h1129 **1 ckpt** · 24 seed. CLM 계열은 3 seed 뿐(bd_noecho 최대 1). mouth 간·ckpt 간
일반화는 미검정. gen=40 canonical · 전 arm rc=0 · 비정규 경고 0.

## related
H_6189 · H_9775 · H_9720 · H_9798
