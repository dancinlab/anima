# H_9698 — R6 mouth-내 저랭크 bilinear cross-position binder (store 없이 추상화)

**status:** 🧱 MBND-BIND-ABSENT — **범위 축소 · TERMINAL 강등 (2026-07-21 실제입력 재판독)**. 원 판정
(bilinear bind-Δ 0.0139/0.0243 ≪ 0.20 both seeds = kill#7 붕괴)은 **무회귀 완전재현**(OLD 2셀이 원본 pod
로그와 12개 통계 전부 일치 · 3 device path)이나, 개념판을 **실제 학습코퍼스 문장**으로 바꾸면 composed·
shuffled·참값0 받침대·cA-echo 가 **전부 정확히 0.0000**(emit_rate 0 < emit_floor 0.005 · m=0) = 계기가
실제 입력에서 **판별력 0**. 원 bind-Δ 는 co-train 에 **심어둔 어휘의 회상 채널** 위에서 잰 값이었다 ⟹
🧱 은 **합성 g6bind 판 한정**이고 "mouth-내 bilinear binder 가 G6 composition 을 안 심는다"는 **일반
TERMINAL 이 아니다**. 미실행 게이트셀 "held-out 자연 concept pair"는 미결→**이 계기로 물을 수 없음**
확정. 선행 [[H_9693]] · 재심 [[H_9746]]/[[H_9694]]/[[H_9745]] (같은 심어둔 판 위)
**wired:** engine-native (`anima-py train --mouth-binder` + `evaluate --fan-bind --mouth-binder`, v0.18.0 · pod 8m9ojdtk5zfk3p A100 SECURE) · 심화 = `evaluate --fan-bind --fan-concepts-real <corpus>` (v0.20.125)
**lane:** G6/ρ·fan · mouth-내 nonlinear 연산 **related:** [[H_9696]] (store 판) · [[H_1603]]

## 물음 (Sol)

외부 store 없이, 프레임의 두 원거리 개념 표현을 별도 bank 에 유지하고 생성 hidden 과 **multiplicative 결합**: `g_t=(U h_t)⊙ Σ_i a_ti(V m_i)`, `ℓ_t=W[g_t;h_t]`. 단순 깊이증가가 아니라 **"두 원거리 내용이 같은 logit 결정에 곱셈 상호작용으로 들어오는가"**를 직접 겨냥 — CLMS 성공을 **store faculty 가 아닌 동적 비선형 binding 연산으로 추상화**한 각도.

## 조작
`anima-py train --mouth-binder bilinear --mouth-memory causal-bank --bind-rank 64 --bind-objective counterfactual` → `anima-py evaluate <clm> --g6 --g6-bind-delta --mouth-binder on --gen 40`. 통제: `--mouth-binder off | --mouth-memory-order-scramble | --mouth-memory-role-scramble | --mouth-binder-linear`.

## 게이트
- nonlinear intact bind-Δ **≥0.20** · role/order scramble 후 **≤0.05** · **linear arm ≤0.05 또는 nonlinear 대비 ≥0.15 낮음**(= kill#7 DOA 를 내부 음성대조로 재현) · held-out 자연 concept pair 동일 bar · 이후 canonical FALS ≥1 ≥2/3 seed ∧ `fals_bound` 동반상승.

## kill-list 회피
#7 = Hadamard interaction + 내용의존 attention → 고정선형 붕괴 안 함. #4 = arch 계급교체 아니라 mouth 직전 구체연산. #6 = intervention sensitivity 가 주판정. #1 = 스캐폴드 없음.

## 최대위험
**memory bank 에 무엇을 남길지 다시 주소/write 문제로 귀착** = store 없앴을 뿐 **H_9672 이전 주소벽을 다른 이름으로 재생성**. `--mouth-binder-linear` 가 반드시 kill#7 DOA 재현해야 계기 유효.

## falsify
🟢 nonlinear bind-Δ≥0.20 ∧ linear DOA 재현 ∧ scramble 붕괴. | 🧱 nonlinear==linear = kill#7 로 붕괴(선형동치). | ⚠️ write 문제 재귀 = H_9696 과 동일벽.

## verdict (2026-07-18 · engine-native 2-seed · 🧱 MBND-BIND-ABSENT)

6-arm 303M warm-FT(base py303_full · g6bind targeted/shuf `--n-blocks 4000 --seed 7` frame_sha 98c48115 = R2 frozen 일치 · `--steps 6000 --lr 1e-4 --bind-rank 64`) → `evaluate --fan-bind --mouth-binder --fan-smp 48`(H_9745 paired McNemar+TOST · powered N=288). pod 8m9ojdtk5zfk3p(runpod A100 80GB SECURE · reclaim-fixed).

| arm | binder/corpus | composed J | shuffled J | **bind_delta** | McNemar p | paired |
|---|---|---|---|---|---|---|
| **BT_s7** | bilinear/targeted | 0.0451 | 0.0208 | **+0.0243** | 0.072 | ⛔ UNDECIDABLE |
| **BT_s4302** | bilinear/targeted | 0.0347 | 0.0208 | **+0.0139** | 0.172 | 🧱 BIND-ABSENT (TOST⊂±0.05=0등가) |
| **LT_s7** | linear/targeted (DOA) | 0.0312 | 0.0312 | 0.0000 | 0.605 | 🧱 (kill#7 DOA 재현 = 계기유효) |
| **BS_s7** | bilinear/shuf (control) | 0.0347 | 0.0312 | +0.0035 | 0.500 | 🧱 (코퍼스 통제 clean) |

**판정 = 🧱 MBND-BIND-ABSENT.** falsify 표 매핑: (1) 🟢 nonlinear bind-Δ≥0.20 → **양 seed 0.0139/0.0243 ≪ 0.20 = 2-seed 배제**. (2) 🧱 nonlinear==linear kill#7 → bilinear(0.014~0.024) ≈ linear DOA(0.000)·shuf(0.0035), 전부 mismatched-null 바닥, s4302 는 TOST 로 0 등가 = 곱셈 binder 가 고정선형 수준으로 붕괴. **계기 유효**: LT_s7 linear DOA 가 0.0000 재현(카드 "계기 유효" 조건) + [[H_9746]] bindpos 양성통제가 fan-bind 서 bind_delta 0.20(McNemar p<0.0001) = dynamic-range 실증. ⟹ 아키텍처 mouth-내 bilinear binding 연산자도 [[H_9694]]/[[H_9745]] 의 data-format 레버처럼 G6 composition 을 **안 심는다**(operator 축 = data 축과 동일 결론).

**scope/정직**: 결정 셀은 lever 2-seed(BT) + seed7 controls(LT DOA · BS shuf) + [[H_9746]] 양성통제. confirmatory 2-seed 통제 replicate(LT_s4302·BS_s4302)·order-scramble·암기 census 는 🧱(lever 1차 bar 2-seed 실패)엔 moot — CRACK 을 form-artifact 와 가르는 셀이라 lever 가 crack 을 안 냈으면 판정 불변. ckpt 6개 로컬 영구보존(`~/.fire-recover/h9698_r6/` 각 184MB · a_fire_recover_complete). 합성 g6bind 상한 = DIRECTIONAL scope(자연 concept pair 로의 전이는 별개).

## 🔎 심화 — 실제 입력 스왑 (H_9854 원장 감사 · 2026-07-21)

H_9854 감사가 이 카드를 "토이/심어둔 입력 위에 굳은 양성 85건"에 하중 4로 올렸다. 이 카드는
**양성이 아니라 landed NEGATIVE(TERMINAL)** 이므로 질문이 더 날카롭다 — 토이 입력에서 잰 부재는
**거짓 음성**일 수 있다(계기가 그냥 눈이 멀었을 수 있다). 그래서 물음은 하나다:
**부재가 실제 입력에서도 재현되는가, 아니면 토이 기하가 실재하는 bind 를 가리고 있었나.**

### 무엇을 바꿨나 (입력 출처 하나만)

`--fan-bind` 가 재는 모든 것은 `core/rho_fan.py::_rho_fan_concepts()` — **손으로 쓴 5개 문자열**에
얹혀 있다(프레임 빌더·페어 빌더·사전 로드가 전부 이걸 읽는다). 새 플래그
`anima-py evaluate <clm> --fan-bind --fan-concepts-real <corpus.txt>` 는 그 판을 **303M 이 실제로
학습한 EN 자연어 코퍼스**(`anima-corpus-en-general`)에서 뽑은 판으로 교체한다. 선택규칙은 **동결**
(순위·탐색·쌍별 필터 없음): *파일 순서상 앞에서부터, 자격을 갖춘 첫 5문장*. 자격 = ① 바이트길이
∈[28,37] = **동결 판의 실현 범위 그대로**(길이는 매개 공변량이다 — CLM mouth 가 seed 를 T=24 창에
우측정렬하므로 개념 길이가 프레임 중 모델이 실제로 보는 양을 정한다 ·
`control-must-match-mediating-covariate`) ② 인쇄가능 ASCII·숫자 없음 ③ **계기 자신의**
`rho_fan_frame_guard` 통과 ④ 채점가능 content word ≥1. **일부러 걸지 않은 필터: 쌍별 content-word
서로소** — 강제하면 손으로 만든 기하를 이름만 바꿔 재건하는 것이다.

**팔·통제·바·문턱·seed 정책·`--fan-smp 48`·`--gen 40` 전부 불변.** 스코어러 인증(`fan_bind_calibration`)은
스왑 **전에 동결 판으로** 그대로 돌린다 — 그것은 DV 술어의 인증이지 판의 인증이 아니고, 새 판에
재정박하면 입력이 아니라 바를 옮기는 것이다(`burned-gate-reanchor-is-tune-to-green`).

### 재현

```
# OLD (카드 원본 경로 · verbatim)
anima-py evaluate BT_s7.clm --fan-bind --mouth-binder --fan-smp 48 --gen 40
anima-py evaluate LT_s7.clm --fan-bind --mouth-binder --fan-smp 48 --gen 40
# REAL (입력만 스왑)
anima-py evaluate BT_s7.clm --fan-bind --mouth-binder --fan-smp 48 --gen 40 \
    --fan-concepts-real <anima-corpus-en-general.txt 앞 4MiB>
anima-py evaluate LT_s7.clm --fan-bind --mouth-binder --fan-smp 48 --gen 40 \
    --fan-concepts-real <anima-corpus-en-general.txt 앞 4MiB>
```
ckpt = `~/.fire-recover/h9698_r6/{BT,LT}_s7.clm` (원본 pod ckpt 로컬 영구보존분).
실제 판 (`panel_sha=c3ee806b88dd`, 코퍼스 앞 4MiB · sha256 `199e2ff58902bc5e…`):
`He never got on board a plane` / `- Your body gets ready to boot it` / `Frankly, winter is miserable` /
`Boston constantly surprises me` / `They make Boston feel like home`.

### ① 통제 먼저 — 감사가 지목한 기전이 이 카드에는 **적용되지 않는다** ($0 · 실측)

H_9854 캠페인의 반복 기전은 "심어둔 코드는 사실상 직교, 실제 표현은 근사공선(cosine ~0.92)".
두 축 모두에서 실측했고, 둘 다 그 기전을 **부정**한다:

| 축 | 동결(손으로 만든) 판 | 실제 코퍼스 판 |
|---|---|---|
| 실제 303M penult pooled-rep 쌍별 코사인 (`clm_penult_pooled_W` · **BT_s7** · n=10쌍) | mean **0.4732** [0.4294..0.5510] | mean **0.4885** [0.4105..0.6114] |
| 〃 (**LT_s7**) | mean **0.3530** [0.2673..0.4499] | mean **0.4119** [0.2818..0.5878] |
| DV 자신의 축 = 쌍별 content-word Jaccard (n=10쌍) | mean **0.0000** · max 0.0000 · 겹치는 쌍 **0/10** | mean **0.0143** · max 0.1429 · 겹치는 쌍 **1/10** |
| 계기가 실제로 만드는 프레임 중 퇴화(J=None) | composed 0/6 · shuffled 0/6 | composed 0/6 · shuffled 0/6 (N=288 유지) |

즉 ⓐ 표현공간에서 동결 판은 애초에 직교가 아니었고(0.47), 실제 판이 더 공선이지도 않다(0.49) ·
ⓑ DV 가 실제로 쓰는 어휘 축에서는 동결 판이 **구성상 완전 서로소(Jaccard 0/10쌍)** 인 게 맞지만
실제 판도 거의 서로소(1/10쌍)라 채점 영역이 그대로 살아 있다 · ⓒ 퇴화 프레임 0/6 로 표본이 줄지도
않는다. **⟹ H_9838/H_9839 를 죽인 "직교→공선" 기전은 H_9698 에 존재하지 않는다.** 감사 대기열의
하중 4 항목 중 이 셀은 그 기전으로는 무너지지 않는다 — 대기열은 반박이 아니라 대기열이었다는
H_9854 자신의 유보를 이 카드가 실측으로 확인한다.

### ② 계기 범위 — 새로 기록해 두는 정직 (판정 불변)

동결 프레임의 **T=24 디코드 창 실측**(`rho_fan_build_frames` + `core/decode.py::_seed_to_tok` 계약에서
바이트 산술로 유도 · 모델 무관): composed/shuffled 프레임은 71–82B 인데 CLM mouth 는 마지막 24B 만
본다 ⟹ **cA 는 12/12 프레임 전부에서 창 밖**이고, 18개 프레임(6×3팔)이 **구별되는 입력 5개**로
붕괴한다(예: composed i=1 · shuffled i=0 · composed i=5 가 모두 `'poses into new meaning: '`).
실제 판도 길이가 맞춰져 있어 같은 절단을 받는다. 이것은 이 심화가 새로 만든 결함이 아니라
[[H_9746]] 이 STEP-0 census 로 이미 다툰 교란이며(A-only 28%<50% ⟹ truncation 비지배 판단), 같은
프레임에서 bindpos 양성통제가 bind_delta 0.20 을 냈으므로 **계기 사망 주장은 성립하지 않는다**.
다만 "두 원거리 내용이 같은 logit 결정에 곱셈으로 들어오는가" 라는 이 카드의 물음에 대해서는,
읽히는 창 안에 cA 가 없다는 사실이 **부재 판정의 범위를 좁힌다**: 측정된 것은 *창 안 cross-position
binding* 이지 *프레임 전체에 걸친 composition* 이 아니다. 사전등록 후속(실행 안 함 · 여기서 돌리면
tune-to-green): `--grow-window`(H_9804 Fix-W)를 `fan_bind_run` 에 배선해 cA 를 창 안에 넣고 동일 바로
재측정 — 별도 H 로 사전등록해야 한다.

### ③ 결정 셀 — bind-Δ 재판독 (4셀 · 각 N=288 · `--fan-smp 48 --gen 40`)

팔당 OLD/REAL 을 **같은 호스트·같은 device path** 에서 돌렸다(스왑이 유일한 차이가 되도록):
LT 쌍 = mini CPU-numpy · BT 쌍 = summer RTX 5070 cupy 13.6.0(`[GPU-FIRED]`). 원본은 A100 cupy.

| 셀 | composed J | shuffled J | ablated(받침대) | **bind_Δ** | b/c/m | McNemar p | emit_rate | cA-echo comp/shuf | PAIRED |
|---|---|---|---|---|---|---|---|---|---|
| **LT_s7 OLD** (통제·DOA) | 0.0312 | 0.0312 | 0.0486 | **0.0000** | 7/7/14 | 0.6047 | 0.0312 | 93/64 | 🧱 BIND-ABSENT |
| **LT_s7 REAL** | **0.0000** | **0.0000** | **0.0000** | **0.0000** | 0/0/0 | 1.0000 | **0.0000** | **0/0** | ⛔ UNDECIDABLE |
| **BT_s7 OLD** (레버) | 0.0451 | 0.0208 | 0.0382 | **+0.0243** | 12/5/17 | 0.0717 | 0.0330 | 106/82 | ⛔ UNDECIDABLE |
| **BT_s7 REAL** | **0.0000** | **0.0000** | **0.0000** | **0.0000** | 0/0/0 | 1.0000 | **0.0000** | **0/0** | ⛔ UNDECIDABLE |

**무회귀(zero regression) 증명 — 완전 일치.** OLD 두 셀은 원본 pod 로그(`~/.fire-recover/h9698_r6/eval_{LT,BT}_s7.log`)와
**출력된 12개 통계 전부** 가 자리수까지 동일하다: LT_s7 composed/shuffled/ablated 0.0312/0.0312/0.0486 ·
null mean 0.0278 p95 0.0451 · b=7 c=7 m=14 · p=0.6047 · Tango90 [−0.0231,+0.0231] · TOST=True ·
cA-echo 93/64 · emit 0.0312 // BT_s7 0.0451/0.0208/0.0382 · null 0.0326/0.0521 · b=12 c=5 m=17 ·
p=0.0717 · CI [+0.0008,+0.0505] · TOST=False · cA-echo 106/82 · emit 0.0330. **A100-cupy → mac
CPU-numpy / RTX5070-cupy 3개 device path 에서 동일** = 계기·ckpt·바 무결. (원본 로그엔 DUAL-GATE
블록이 없다 — 그건 H_9698 후속으로 나중에 착륙한 **출력 전용** 합산 게이트라 수치를 안 건드린다.)

**실제 입력 결과 — DV 가 통째로 죽는다.** 실제 판에서는 composed·shuffled·**참값0 ablated 받침대까지**
전부 정확히 0.0000 이고, 판별셀 m=0, **emit_rate=0.0000 < 계기 자신의 사전등록 emit_floor 0.005**,
그리고 결정적으로 **cA-echo = 0/288 · 0/288** — 864 회 방출 중 실제 개념의 content word 가 **단 한 번도**
나오지 않았다. 퇴화 프레임 때문이 아니다(N=288 유지 · 위 통제표 ⓒ). 즉 실제 입력에서 이 계기는
음성을 내는 게 아니라 **아무 신호도 실어나를 수 없다** = 판별력 0.

**왜 죽는가 — 기전은 기하가 아니라 어휘였다.** ① 에서 봤듯 판의 기하(표현 코사인·어휘 서로소도)는
동결↔실제가 사실상 같다. 다르게 만든 유일한 것은 **동결 판의 다섯 문장이 g6bind co-train 코퍼스에
4,000블록 심어져 있다**는 사실이다. 그래서 OLD 에서 모델은 cA 를 32~37%(93·106/288) 되뇌었고 —
창 안에 cA 가 없는데도(② 참조) — 그 되뇌임이 bind_Δ 가 0 이 아닐 수 있는 **유일한 통로**였다.
학습에 안 심긴 실제 문장으로 바꾸자 그 통로가 0 으로 닫힌다. **⟹ OLD 의 bind_Δ 는 composition 채널이
아니라 심어둔 어휘의 회상 채널 위에서 측정된 값이다.**

### 판정 — landed TERMINAL 은 **그대로 살아남지 않는다** (범위 축소)

**bind 가 나타나서 뒤집힌 게 아니다** — 실제 입력에서도 bind_Δ 는 0 이고 어떤 CRACK 도 없다.
뒤집히는 것은 **TERMINAL 자격**이다:

- 🧱 **MBND-BIND-ABSENT 자체는 유지**되나 범위가 **합성 g6bind 판(심어둔 어휘) 한정**으로 줄어든다.
  "mouth-내 bilinear binding 연산자가 G6 composition 을 안 심는다"는 **일반 주장으로는 TERMINAL 이
  아니다** — 그 주장을 시험할 통로가 심어둔 어휘 밖에서는 존재하지 않기 때문이다.
- 카드가 게이트에 적어놓고 **한 번도 안 돌린 셀** "held-out **자연** concept pair 동일 bar" 는 이제
  미결이 아니라 **이 계기로는 물을 수 없음**으로 실측 확정됐다(⛔ INSTRUMENT-DEAD-ON-REAL-INPUT).
  카드의 원 scope 유보("자연 concept pair 로의 전이는 별개")는 **옳았고, 이제 추정이 아니라 측정이다.**
- 함께 재심 대상: [[H_9746]] 양성통제(bind_delta 0.20)도 `--arm bindpos` 가 cA+cB 를 co-train 에
  **심어서** 만든 판이다. 따라서 그 "dynamic range 실증"이 입증한 것은 **심어둔 어휘 위에서의**
  dynamic range다. 심기지 않은 판에서도 살아남는지는 **여기서 재지 않았다**(재려면 별도 H).
  같은 이유로 [[H_9694]]/[[H_9745]] R2 의 BIND-ABSENT 도 동일 판 위에 있다.

**차단되는 하류 지출**: ① `--fan-bind` 로 **자연 개념쌍** 을 읽으려는 모든 후속 레버(측정 자체가 0) ·
② R6 를 "operator 축 = data 축" 일반 결론으로 인용해 mouth-내 binding 계열을 접는 판단 ·
③ bindpos 양성통제 하나만 믿고 이 표면 위에서 새 레버를 태우는 GPU 지출.

**사전등록 후속(여기서 실행 안 함 — 돌리면 tune-to-green)**: (R-a) `--grow-window` 를 `fan_bind_run`
에 배선해 cA 를 T=24 창 안에 넣고 동일 바 재측정 · (R-b) `corpus g6bind --arm bindpos` 를 **실제 판**
으로 만들어 양성통제가 심기지 않은 어휘에서도 0.20 을 내는지 · (R-c) DV 를 어휘 집합 일치가 아닌
표현공간 술어로 바꾸는 계기 교체. 셋 다 **바를 옮기는** 변경이므로 각각 별도 사전등록 H 로만.

## 계기 인증 (2026-07-17 · 학습 전 · DIRECTIONAL)

## 계기 인증 (2026-07-17 · 학습 전 · DIRECTIONAL)

`core/mbnd.py`(MBND trailer) + `core/decode.py` 배선 착륙(read 순서: CLMF → CLML → CLMS → **MBND**).
셀프테스트가 **통제 결함 2건**을 잡아 수리했고, 둘 다 고치기 전이었다면 R6 는 해석불가로 발사됐을 것:

- **linear arm 이 선형이 아니었다** — softmax 주소가 데이터 의존이라 ⊙→+ 만 바꾼 arm 의 선형편차가 59.9.
  이 arm 은 아무것도 통제하지 못했다. uniform attention(주소 고정)으로 교체 → 편차 **0.0000** =
  kill#7 고정역할 선형붕괴를 BY CONSTRUCTION 재현 ⟹ 이 카드의 "계기 유효" 조건 충족.
- **order-scramble 통제가 무효였다** — content attention 은 bank 에 순열-등변이라 Δ=0.000. 통제가
  살아남은 게 아니라 통제가 lane 을 **건드릴 수 없었다**(`corpus-py-1` 위조게이트 계급). 더 나쁘게,
  순서 없는 lane 은 "A causes B"와 "B causes A"를 구별 못 해 **binder 자격 자체가 없다**.
  상대거리 bias `b_pos` 추가 → Δ=**325.6**.

**선례 정렬 — [[H_1640]] 은 R6 를 죽이지 않는다**: Hamiltonian symplectic binding mouth 가 G6 fals=0 을
받았으나 그 binder 는 **직렬화 전 DROP**(trunk-shaping scope) = binding op 이 decode 경로에 도달한 적이 없다.
MBND 는 정반대로 trailer 를 타고 추론에서 실행되며, parity 작업이 정확히 그걸 인증한다.

2-production mirror: torch `MouthBinder` ⇄ numpy `mbnd_apply` parity **3.55e-15**(summer · f4 격자 스냅 후).
numpy≥2 의 shape-(1,) lam 스칼라 캐스팅 거부(이식성 버그)도 pool 실행이 적발 — mac numpy 는 허용해 로컬에선 안 보였다.

미완: train 플래그(`--mouth-binder`/`--mouth-memory`/`--bind-rank`) + `--g6-bind-delta` 판정면.
bind-Δ 숫자는 학습된 ckpt 로만 — 현재는 **계기지 verdict 아님**.

## 학습·판정 배선 (2026-07-17 · DIRECTIONAL)

계기(core/mbnd.py)에 이어 **co-train + 판정 경로** 착륙:
- `core/model.py`: config(mbnd/mbnd_rank/mbnd_linear/mbnd_lam0) + `MouthBinder` 할당 + forward 적용.
  bank tap = **PRE-slot penultimate**(mb_tap) = `core/decode.py` 가 mbnd_apply 에 먹이는 `yn_trunk`
  와 동일. post-SLW `x` 를 쓰면 train/decode parity 가 조용히 깨져 verdict 자체가 읽을 수 없게 된다.
- `cli/train.py`: `--mouth-binder {bilinear,linear}` · `--mouth-memory causal-bank` · `--bind-rank` ·
  `--bind-lam0`. **linear = kill#7 DOA 내부 음성대조**(uniform address + additive). trailer 는 CLMS 뒤.
- `cli/evaluate.py`: `fan_bind_run` 에 `--mouth-binder` / `--mouth-binder-order-scramble` lane 스위치
  + `_KNOWN_FLAGS` 등록(H_9672 `--store-addr-audit` 이 이 등록 누락으로 pool 서 죽은 전례 회피).

pool 스모크: `train`/`evaluate --help` 에 플래그 확인 · `--fan-bind` scorer 인증 통과 · default OFF ⇒
trailer 실은 ckpt 도 byte-identical. **bind-Δ 는 학습된 303M ckpt 로만** — 현재 R2 pod(5090) 진행중.

## source
lab full Sol 3위(NOVEL) · store→연산 추상화.
