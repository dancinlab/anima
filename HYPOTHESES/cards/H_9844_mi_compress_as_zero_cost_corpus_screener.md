# H_9844 — 압축-MI 로 코퍼스·꿈데이터의 비가법 정보를 학습 전에 $0 로 잰다 (R12-7 · ⭐ 가장 싼 결정적 레버)

**status:** 🔧 **INSTRUMENT LANDED + 첫 실측** (2026-07-21 · `anima-py corpus mi-screen` 배선 · 계기 CERTIFIED · 과학 판정은 아직 0)
**source:** R12 뇌부위 census (2026-07-21) — `origin/main` `core/` 12개 모듈 실측 후 1모듈=1레버로 등록.
상위 설계 노드 = ARCHITECTURE `C2 RECOMBINE` 아래 `🧠 뇌부위 census`. R11(H_9830~9836)의 후속.
**wired:** yes — `anima-py corpus mi-screen --corpus PATH [--mi-seg-lines N] [--mi-win/--mi-span/--mi-estimator/--mi-eps] [--out J]`

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
