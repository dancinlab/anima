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

## related
H_6189 · H_9775 · H_9720 · H_9798
