# H_9844 — 압축-MI 로 코퍼스·꿈데이터의 비가법 정보를 학습 전에 $0 로 잰다 (R12-7 · ⭐ 가장 싼 결정적 레버)

**status:** 🔬 **INSTRUMENT LANDED + 실제-입력 교체 완료** (2026-07-21 · `anima-py corpus mi-screen` 배선 ·
계기 CERTIFIED · 절차 코퍼스 3종 + **303M 이 실제 학습한 4칸 chat 코퍼스 4/4 전부 READ=none** · DIRECTIONAL)
**source:** R12 뇌부위 census (2026-07-21) — `origin/main` `core/` 12개 모듈 실측 후 1모듈=1레버로 등록.
상위 설계 노드 = ARCHITECTURE `C2 RECOMBINE` 아래 `🧠 뇌부위 census`. R11(H_9830~9836)의 후속.
**wired:** yes — `anima-py corpus mi-screen [--corpus PATH | --mi-chat-cell CELL] [--mi-seg-lines N] [--mi-robust] [--mi-win/--mi-span/--mi-estimator/--mi-eps] [--out J]`

## 실측 — 이 모듈은 **이미 프로덕션에 있고 아무도 이 용도로 안 쓰고 있다**

`core/mi_compress.py`(810줄 · H_9806): `cond_bpb_gzip` / `cond_bpb_ppm` / `cond_bpb_markov` ·
`stream_mi` · `break_adjacency` · `plant_crossboundary` · `plant_null_stream` · `battery_liveness`.
헤더: **"production anima had ZERO compression-based mutual-information estimators, so every
'does this stream carry information across a boundary' question had to be answered by a forward
pass through a model — which conflates what the STREAM carries with what the MODEL can reach.
This module measures a property of the stream itself, at \$0, stdlib-only, with no GPU and no ckpt."**

## 왜 이게 판을 바꾸는가

G1 의 세 얼굴 중 **데이터면**(H_9304: 비가법 정보 +0.0023 nats ≈ 0)은 지금까지 **모델을 통과시켜서만**
측정됐다. `stream_mi` 는 모델 없이 **스트림 자체**를 잰다 ⟹ "코퍼스에 결합정보가 없다" 와
"모델이 못 읽는다" 를 **처음으로 분리**할 수 있다. 그리고 `plant_crossboundary` / `plant_null_stream`
이 **양성통제와 참값-0 받침대를 이미 내장**하고 있다(`positive-control-before-reading-a-negative` ·
`phi-estimator-needs-zero-truth-pedestal` 둘 다 충족).

## Intervention

```
anima-py corpus mi-screen <corpus.txt> --segments <n> --estimator {gzip,ppm,markov}
```

측정 대상 3종: ① 현행 학습 코퍼스 ② H_9839 가 만든 rule-derived 꿈 데이터 ③ midpoint 꿈 데이터.

## 사전등록 판정표

| 결과 | 읽는 법 |
|---|---|
| plant_crossboundary 가 검출 안 됨 | **INSTRUMENT-DEAD** — 아무것도 읽지 않는다 |
| plant_null 이 0 초과 | **INVALID** — 정보를 제조했다 |
| 코퍼스 MI ≈ null | 데이터면 확정 — 어떤 목적함수도 없는 비트를 못 배운다. **R11/R12 학습레버 전부 재평가** |
| rule-derived > midpoint > null | H_9839 통과 · 꿈이 실제로 결합정보를 제조 |

## 이 카드의 순위 근거

**비용 \$0 · GPU 0 · ckpt 0 · 계기 수리(H_9827/9828) 불요.** 오늘 당장 판독 가능한 유일한 축이며,
음성이 나오면 **위 11장의 학습 레버 전체의 기대값을 한 번에 깎는다**. 정보/비용 최대.

**related:** H_9806 · H_9304 · H_9839 · H_9287 · H_9267


---

## 🔧 착륙 + 첫 실측 (2026-07-21)

### 계기 인증 — 통제 3/3 × 2방향 전부 갈림

동봉 통제를 **먼저** 돌리고, 둘 다 통과하지 못하면 코퍼스 행을 아예 보고하지 않는다(순차 동결 게이트).

| 통제 | gzip | ppm | markov6 | 판정 |
|---|---|---|---|---|
| `plant_crossboundary` (양성) | **+6.664** | **+0.767** | **+5.973** | 전부 발화 ✅ |
| `plant_null_stream` (참값 0 받침대) | **0.000** | +0.002 | +0.004 | 전부 거부 ✅ |

⟹ **CERTIFIED**. 심어둔 신호는 보고, 없는 신호는 만들지 않는다
(`positive-control-before-reading-a-negative` + `phi-estimator-needs-zero-truth-pedestal` 동시 충족).

### 첫 코퍼스 실측 — `corpus flat --lang en --seed 7` (798,570 B · 6,540 줄)

세그먼트 = 60줄 블록 × 109개 (109/109 usable · **underpowered=False**), 기하 = win 4096 / span 2048 / eps 0.02.

```
gzip     ceiling=0.0840  floor=0.0859  over_floor=-0.0020
ppm      ceiling=0.5614  floor=0.5585  over_floor=+0.0029
markov6  ceiling=0.1637  floor=0.1679  over_floor=-0.0043
```

**세 추정기 전부 |over_floor| < 0.005 ≪ eps=0.02, 둘은 음수.** 이 스트림은 경계를 넘는
읽을 수 있는 정보를 **담고 있지 않다** — 모델을 한 번도 통과시키지 않고 얻은 코퍼스 사실이다.
H_9304 가 모델을 통해 잰 +0.0023 nats 와 **크기까지 나란하다**.

### ⚠️ 이 숫자를 과대해석하지 말 것 (정직 범위)

1. **대상이 절차생성 `flat` 코퍼스다.** 줄 단위로 독립 생성된 코퍼스에 60줄 블록 간 구조가 없는 것은
   거의 **동어반복**이다. 이건 벽에 대한 판정이 아니라 **계기가 산다는 증명 + 기준점**이다.
2. 판정이 필요한 진짜 대상은 **303M 이 실제로 학습한 4칸 chat 코퍼스**(ko/en × general/sns)와
   H_9839 가 만들 rule-derived 꿈 데이터다. 그 둘을 재기 전엔 **어떤 데이터면 결론도 없다**.
3. 압축 추정기는 **하한**이다 — null 은 *읽을 수 있음*의 부재를 한정하지 *존재*의 부재를 증명하지 않는다.

### 계기 자체에서 나온 부수 발견

`MI.segments_from_path` 는 빈 줄로 자르는데 **anima 의 절차적 코퍼스에는 빈 줄이 0개**다
(실측: 798,570 B / 6,540 줄 / `b"\n\n"` **0회**). 즉 원본 API 만으로는 이 계기가 **자기 측정 대상을
못 자른다**. `--mi-seg-lines N`(줄-레코드 블록화)을 추가해 교정했고, 짧은 블록은 패딩 없이 **드롭**하고
감소분을 `segmented_as` 에 보고한다(답을 제조하지 않는다).

### 재감사 지문

결과 JSON 에 `reaudit.argv` 전체 · 입력별 `sha256`+바이트수 · 해소된 기하를 박는다
(corpus-py-1 ⑫(J): 재생성 커맨드 없는 verdict 는 아무도 재검증 못 한다). 재현:

```
anima-py corpus flat --out /tmp/mi_en.txt --lang en --seed 7
anima-py corpus mi-screen --corpus /tmp/mi_en.txt --mi-seg-lines 60 --out mi_en.json
```

**NEXT:** 4칸 chat 코퍼스 · H_9839 midpoint vs rule-derived 꿈 데이터 · 그리고 병렬세션의 신규 실측
(G6 = 기질 벽이 아니라 **코퍼스-밀도 벽**)과 같은 축이므로 결과를 맞대볼 것.


---

## ⚠️ 자가적발: 첫 판 계기는 블록 크기로 초록불을 만들 수 있었다 (2026-07-21 · 같은 날)

코퍼스 3종을 스크리닝하다 **기하만 바꿔도 부호가 뒤집히는 것**을 발견했다:

| 코퍼스 | 60줄/4096B 블록 gzip | 8~46줄/512B 블록 gzip |
|---|---|---|
| `flat --lang en` | **−0.0020** | **+0.0312** (eps=0.02 통과) |
| `storebind` | **+0.0195** (최고) | **+0.0000** (소멸) |
| `derivtrace` | −0.0098 | +0.0000 |

두 기하 모두 통제는 정상이었다(plant 발화 · null 거부). 즉 **계기는 살아있는데 판정이 블록 크기의
함수**였다 — 한 기하만 보고하면 블록 크기가 판정을 고르게 되고, 그것이 정확히 `no tune-to-green`
위반이다. 아무도 이 숫자에 cement 하기 전에 잡았다.

### 교정 — `--mi-robust` 강건성 게이트

같은 배터리를 요청 기하 + 그 **1/2 · 1/8** 기하에서 재실행하고 **최솟값**을 헤드라인으로 삼는다.
`read` 는 그 최솟값이 eps 를 넘을 때만 참. `geometry_dependent` 는 "한 블록 크기에선 살고 다른
크기에선 죽는" 추정기를 표시한다(spread > eps 인데 최솟값은 eps 미달) = 분절 인공물.

### 3-기하 census 실측 (통제 3/3 발화 · 3/3 거부 · 전 기하 재인증)

```
코퍼스        robust_over_floor(최솟값)          spread              READ   기하의존
flat(en)      gzip−0.0078 ppm−0.0023 mk−0.0102   .039/.005/.050      none   gzip·markov6
derivtrace    gzip−0.0098 ppm−0.0055 mk−0.0144   .041/.012/.057      none   gzip·markov6
storebind     gzip+0.0000 ppm−0.0022 mk+0.0019   .020/.005/.009      none   없음
```

**판정: READ = none (3/3 코퍼스).** anima 의 절차적 학습 코퍼스 중 **기하-강건한 교차경계 정보를
담은 것은 하나도 없다.** 그리고 앞서 보였던 두 양성(`flat` +0.0312 · `storebind` +0.0195)은
새 게이트가 **분절 인공물로 정확히 분류**했다 — `storebind` 만 기하의존이 아닌데, 그건 그 코퍼스의
설계 구조(store 창 24줄)가 애초에 블록 경계 위에 있지 않기 때문이다.

### 이 결과가 레버들에 주는 함의

DIRECTIONAL 이지만 방향은 분명하다: 데이터면이 비어 있다는 H_9304 의 그림이 **모델 없이도** 재현된다.
⟹ 학습측 레버(R11·R12)들이 기대는 "코퍼스에 결합정보는 있는데 모델이 못 읽는다" 전제는
**적어도 이 세 포맷에서는 지지되지 않는다.** 남은 진짜 대상은 303M 이 실제 학습한 4칸 chat 코퍼스와
H_9839 의 rule-derived 꿈 데이터이며, 그 둘을 재기 전에는 데이터면 결론을 닫지 않는다.

### 재현

```
anima-py corpus flat      --out /tmp/mi_en.txt   --lang en --seed 7
anima-py corpus derivtrace --out /tmp/mi_dt.txt  --lang en --seed 7
anima-py corpus storebind --out /tmp/mi_sb.txt   --lang en --seed 7
anima-py corpus mi-screen --corpus /tmp/mi_en.txt --mi-seg-lines 60  --mi-robust --out en.json
anima-py corpus mi-screen --corpus /tmp/mi_dt.txt --mi-seg-lines 60  --mi-robust --out dt.json
anima-py corpus mi-screen --corpus /tmp/mi_sb.txt --mi-seg-lines 500 --mi-robust --out sb.json
```

---

## 🔬 심화: 입력을 **실제 4칸 chat 코퍼스**로 교체했다 — 착륙한 결론은 살아남았고, 새 위험이 하나 드러났다 (2026-07-21 · 같은 날)

이 카드가 스스로 적어둔 미결 타깃(`NEXT: 4칸 chat 코퍼스`)을 실행했다. **바꾼 것은 입력 하나뿐이다.**
팔 · 동봉 통제(`plant_crossboundary` / `plant_null_stream`) · 바(`eps=0.02`) · `--mi-robust` 3-기하
최솟값 규칙 · 동결 게이트 순서 — 전부 불변.

### 왜 이 교체가 의무였나 (H_9838 선례)

앞선 census 3종(`flat`·`derivtrace`·`storebind`)은 **줄 단위로 절차 생성**된 스트림이라
"블록 경계를 넘는 정보가 없다"는 결론이 **거의 동어반복**이었다 — 이 카드의 정직 범위 ①이 이미
그렇게 적어뒀다. 같은 날 **H_9838** 이 그 위험의 값을 매겼다: 심어둔 정수 fixture 위에서 12× 우연의
헤드라인 양성(양성통제 + 참값-0 받침대 + 3 seed × 3 기하 + 독립 재현)을 착륙시켰는데, **코드 출처만**
프로덕션 trunk 의 실제 penultimate 표현으로 갈아끼우자 참값-0 받침대가 터지고(값-셔플 0.3750 > 바
0.3077) 판정이 **INVALID** 이 됐다. 심어둔 코드는 사실상 직교(within .0469 / across .0117)인데 실제
표현은 2.2배 겹쳤다(.0625 / .0260) — **손으로 만든 유리한 기하가 결과를 제조**하고 있었다.
절차 코퍼스도 정확히 같은 종류의 손으로 만든 세계다.

### 배선 — `--mi-chat-cell` (입력 소스 플래그)

```
anima-py corpus mi-screen --mi-chat-cell {ko-general|en-general|ko-sns|en-sns|all} [반복 가능]
```

PUBLIC HF 데이터셋(`dancinlab/anima-corpus-<cell>`)을 stdlib `urllib` 로 한 번 받아
`$ANIMA_CORPUS_CACHE`(기본 `./.corpus_cache` · `cli/train.py::resolve_corpus_path` 와 같은 캐시 루트)에
저장하고, **평범한 `--corpus` 경로로** 넘긴다. 이 줄 아래로는 계기가 입력 출처를 알지 못한다 — 그게
요점이다. 받지 못한 셀은 **보고만 하고 대체·창작하지 않는다**(`honesty`). VERSION 0.20.111→0.20.112 (G5).

### ① 회귀 0 — 플래그 착륙 **후** 옛 경로가 카드의 숫자를 그대로 낸다

통제(입력과 무관하므로 7회 실행 전부 동일해야 하고, 실제로 전부 동일했다):

| 통제 | gzip | ppm | markov6 | 카드 기재값 |
|---|---|---|---|---|
| `plant_crossboundary` (양성) | **+6.6640625** | **+0.7672949821539197** | **+5.972620150319223** | +6.664 / +0.767 / +5.973 ✅ |
| `plant_null_stream` (참값 0 받침대) | **0.0** | **+0.0018651470619639454** | **+0.0035809337633700977** | 0.000 / +0.002 / +0.004 ✅ |

3-기하 census(`--mi-robust` 최솟값 · eps=0.02):

| 코퍼스 | bytes | robust gzip / ppm / markov6 | spread | READ | 카드 기재값과 대조 |
|---|---|---|---|---|---|
| `flat --lang en` | 798,570 | **−0.0078** / **−0.0023** / **−0.0102** | .0391 / .0052 / .0499 | none | −0.0078/−0.0023/−0.0102 · .039/.005/.050 ✅ |
| `derivtrace` | 1,215,724 | **−0.0098** / **−0.0055** / **−0.0144** | .0410 / .0115 / .0568 | none | −0.0098/−0.0055/−0.0144 · .041/.012/.057 ✅ |
| `storebind` | 544,134 | **+0.0000** / **−0.0022** / **+0.0019** | .0195 / .0049 / .0090 | none | +0.0000/−0.0022/+0.0019 · .020/.005/.009 ✅ |

플래그를 넣기 **전/후** `flat` 실행의 결과 JSON 은 `reaudit.argv`(자기 커맨드를 그대로 기록하는 필드)를
빼면 **완전히 동일**했다 — 회귀 0.

### ② 새 경로 — 실제 4칸 chat 코퍼스 (303M 이 실제로 학습한 데이터)

셀은 **4/4 전부 받았다**(HF PUBLIC · 일반 https · 토큰 불요). 두 general 셀의 sha256 은 HF LFS oid 와
일치한다(`19e6ac9e…` / `66140944…`). 통제는 4/4 실행 전부 CERTIFIED(위 표와 동일 값).

**기하는 셀마다 따로 계산했다** — ko 는 ~3 B/char 라 같은 `--mi-seg-lines` 가 셀마다 전혀 다른 바이트
부하가 된다(`a_korean_byte_budget`). 사전등록 규칙(결과를 보기 **전**에 고정, 4칸에 동일 적용):
`--mi-seg-lines = round(8000 / 셀의 바이트-per-줄)` — 즉 착륙한 절차 census 와 **같은 블록 스케일**
(base 블록 ≈ 8 kB ≈ 1.3 × (win+span)=6144 B)에서 읽는다. 실측 바이트/줄:
ko-general 176.2 → **46** · en-general 214.9 → **38** · ko-sns 128.8 → **62** · en-sns 193.2 → **42**.

| 셀 | bytes | sha256(앞12) | seg-lines | usable 세그먼트 (기하 1/2/3) | underpowered | **robust** gzip / ppm / markov6 | spread | **READ** | 기하의존 |
|---|---|---|---|---|---|---|---|---|---|
| `ko-general` | 60,000,356 | `19e6ac9e34d1` | 46 | 4723 / 8601 / 29132 | False/False/False | **−0.0156** / **−0.0003** / **+0.0010** | .0469/.0184/.0469 | **none** | gzip·markov6 |
| `en-general` | 60,049,637 | `661409443270` | 38 | 5077 / 9473 / 31443 | False/False/False | **−0.0156** / **+0.0010** / **+0.0043** | .0156/.0125/.0185 | **none** | 없음 |
| `ko-sns` | 6,183,822 | `c836e9fc948e` | 62 | 571 / 1114 / 3846 | False/False/False | **+0.0000** / **+0.0006** / **−0.0007** | .0078/.0026/.0085 | **none** | 없음 |
| `en-sns` | 1,326,111 | `49f347c72416` | 42 | 96 / 185 / 668 | False/False/False | **−0.0234** / **+0.0092** / **+0.0106** | .0547/.0145/.0258 | **none** | gzip·markov6 |

### 🔑 새로 드러난 것 — **실제 텍스트에서 단일-기하 신기루가 더 심하다**

기하별 원시 over_floor (위 robust 는 이 셋의 최솟값):

```
셀            기하 4096/2048              기하 2048/1024              기하 512/256
ko-general    gz−0.0156 pp−0.0003 mk+0.0010   gz−0.0078 pp+0.0077 mk+0.0136   gz+0.0312 pp+0.0181 mk+0.0478  ← gz·mk 통과
en-general    gz−0.0156 pp+0.0010 mk+0.0043   gz−0.0078 pp+0.0074 mk+0.0102   gz+0.0000 pp+0.0134 mk+0.0228  ← mk 통과
ko-sns        gz+0.0039 pp+0.0032 mk+0.0078   gz+0.0078 pp+0.0022 mk−0.0007   gz+0.0000 pp+0.0006 mk+0.0009  ← 전부 미달
en-sns        gz−0.0234 pp+0.0154 mk+0.0106   gz+0.0195 pp+0.0236 mk+0.0364   gz+0.0312 pp+0.0092 mk+0.0224  ← 두 기하서 통과
```

**절차 코퍼스에서는 3종 중 2종이 단일-기하 양성을 냈지만, 실제 자연어에서는 4칸 중 3칸이 낸다.**
그리고 방향이 계통적이다 — 블록이 작아질수록 over_floor 가 **모든 셀에서 단조 증가**한다(작은 블록 =
측정 창 두 개가 파일 안에서 물리적으로 더 가까움 = 국소 연속성). 즉 `--mi-robust` 가 없었다면 이번
실측은 "**anima 의 실제 학습 데이터가 교차경계 정보를 담고 있다**"는 헤드라인 양성 3/4 로 착륙했을
것이다. 게이트가 그 4개를 전부 거부했다. 이 게이트는 절차 코퍼스에서 스스로를 잡으려고 만들었는데,
**실제 데이터에서 더 크게 값을 했다**.

### 판정 — **READ = none (4/4 셀). 착륙한 결론은 살아남았고, 범위는 좁아진 게 아니라 넓어졌다.**

H_9838 과 달리 이 계기는 입력 교체에서 **깨지지 않았다**. 이유는 구조적이다: H_9838 의 신호는 **심어둔
코드의 기하**에서 나왔고 실제 표현에는 그 기하가 없었지만, H_9844 의 착륙 결과는 **음성 census**였고
동봉 통제는 입력과 **무관**하다(양성통제·받침대는 자기 스트림을 스스로 만든다) — 그래서 교체가
바꿀 수 있었던 것은 오직 코퍼스 행뿐이었고, 그 행이 절차 코퍼스와 **같은 답**을 냈다.

바뀐 것은 **주장의 세기**다. 착륙 시점의 정직 범위 ①("대상이 절차생성 코퍼스라 결론이 동어반복에
가깝다")이 **해소됐다**: 이제 이 null 은 손으로 만든 스트림이 아니라 **303M 이 실제로 학습한 자연어
67.5 MB** 에서 나온 것이다.

**이것이 R11/R12 학습 레버들에 청구하는 값:**

1. "코퍼스에 결합정보는 있는데 모델이 못 읽는다"는 전제는 **4칸 chat 코퍼스에서 지지되지 않는다**.
   모델을 한 번도 통과시키지 않고 얻은 코퍼스 사실이며, H_9304 가 모델을 통해 잰 +0.0023 nats 와
   **부호도 크기도 나란하다** — 이제 독립적인 두 경로가 같은 곳을 가리킨다.
2. ⟹ **데이터면 레버는 추출형이 아니라 생성형이어야 한다.** 대조군이 이미 이 카드 옆에 있다:
   H_9839 의 rule-derived 꿈 데이터는 같은 계기·같은 게이트에서 robust gzip **+0.1641** / markov6
   **+0.2396** 으로 eps 를 한참 넘겼다(READ 성립). **없는 것을 읽게 만드는 목적함수는 없고,
   만들어 넣은 것은 읽힌다.**
3. ⟹ **차단되는 지출**: "4칸 chat 코퍼스 안의 재조합 결합구조를 목적함수로 표면화한다"를 전제로 한
   303M CPT/co-train 발사는 **발사 전에 $0 로 반증됐다**. 그 전제를 쓰는 레버는 (a) 먼저 읽히는
   코퍼스를 만들거나(H_9839 계열), (b) 자기 전제를 이 스크리너로 통과시킨 뒤에만 GPU 를 쓴다.

### 재현

```
# 옛 경로 (회귀 확인 · 카드의 착륙 숫자와 대조)
anima-py corpus flat       --out /tmp/mi_en.txt --lang en --seed 7
anima-py corpus derivtrace --out /tmp/mi_dt.txt --lang en --seed 7
anima-py corpus storebind  --out /tmp/mi_sb.txt --lang en --seed 7
anima-py corpus mi-screen --corpus /tmp/mi_en.txt --mi-seg-lines 60  --mi-robust --out old_en.json
anima-py corpus mi-screen --corpus /tmp/mi_dt.txt --mi-seg-lines 60  --mi-robust --out old_dt.json
anima-py corpus mi-screen --corpus /tmp/mi_sb.txt --mi-seg-lines 500 --mi-robust --out old_sb.json

# 새 경로 (실제 입력 · 셀마다 seg-lines 다름 · ko 3 B/char)
anima-py corpus mi-screen --mi-chat-cell ko-general --mi-seg-lines 46 --mi-robust --out real_ko_gen.json
anima-py corpus mi-screen --mi-chat-cell en-general --mi-seg-lines 38 --mi-robust --out real_en_gen.json
anima-py corpus mi-screen --mi-chat-cell ko-sns     --mi-seg-lines 62 --mi-robust --out real_ko_sns.json
anima-py corpus mi-screen --mi-chat-cell en-sns     --mi-seg-lines 42 --mi-robust --out real_en_sns.json
```

로컬 CPU · GPU 0 · ckpt 0 · $0. general 셀 1개당 ~55 CPU-min, sns 셀은 1~6분.

### ⚠️ 정직 범위 (이 판정이 **아닌** 것)

1. **압축 추정기는 하한이다.** null 은 *읽을 수 있음*의 부재를 한정하지 *존재*의 부재를 증명하지
   않는다 — 착륙 때와 동일한 제약이고, 입력을 바꿔도 그대로다.
2. **블록 절단은 자연 텍스트의 문서 경계가 아니다.** 4칸 코퍼스도 `b"\n\n"` 이 **0회**다(실측 4/4 셀).
   문단/문서 구분자가 없어 `--mi-seg-lines` 는 줄-레코드를 임의로 자른다. 문서 경계에 정렬된 절단이
   다른 답을 낼 가능성을 **이 실행은 배제하지 못한다** — 이게 남은 가장 큰 구멍이다.
3. **블록 감쇠가 크고 무작위가 아니다.** 자연 텍스트는 줄 길이가 치우쳐 `win+span` 미달 블록이
   드롭된다(en-sns base 96/164 · ko-general base 4723/7403). 짧은 줄이 많은 블록이 계통적으로
   빠진다. 계기는 이 감쇠를 `segmented_as` 에 그대로 보고하고 패딩하지 않는다.
4. **ko 셀은 맥락이지 레버가 아니다** — 연구 코퍼스의 한국어 레인은 🧱 BINDING-dead(H_9327). 다만
   원시 바이트 위의 압축 추정기는 언어 무관이라 값 자체는 그대로 보고한다.
5. **DIRECTIONAL** — 코퍼스 사실이지 학습 판정이 아니다. 그리고 **한 블록 스케일(~8 kB)** 에서의
   판정이다.

### 🚫 여기서 하면 안 되는 것 (사전 차단)

`--mi-seg-lines` / `--mi-win` / `--mi-eps` 를 어떤 조합이 eps 를 넘을 때까지 훑는 것은 **정의상
tune-to-green** 이고, 위 "단일-기하 신기루" 표가 그게 얼마나 쉬운지 보여준다(작은 블록만 고르면
3/4 칸이 양성이다). 살릴 각도가 있다면 **사전등록된 별도 H** 로만 — 이 카드에서는 돌리지 않았다.
후보 2개를 여기 등록만 해둔다:
- **(F1) 문서경계 정렬 절단**: 4칸 코퍼스의 원본 HF 행 경계를 세그먼트로 삼아 재측정. 정직 범위 ②를
  정면으로 겨눈다. 사전등록 필요: 세그먼트 정의 · 기하 스윕 · 동일 eps.
- **(F2) 블록 스케일 사다리**: `--mi-seg-lines` 를 결과와 무관하게 사전 고정한 4개 스케일
  (2 kB·8 kB·32 kB·128 kB)에서 전 4칸을 돌려 over_floor(블록크기) 곡선 자체를 보고. 최솟값 규칙은
  유지하되 신기루의 **함수 형태**를 재는 것이 목적이며, 어느 스케일도 헤드라인이 되지 않는다.
