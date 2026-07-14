# H_9354 — SPLICE (V4): 연산자의 어간 판독은 **런타임 활성**인가, **가중치-수준**인가

- **group**: g1-interface-addressable-wall
- **date**: 2026-07-15
- **status**: ⏳ PRE-REGISTERED (수치 보기 전 동결)
- **instrument**: `anima-py evaluate <ckpt> --splice <spec.json> --out <f.json>` (engine-native · `cli/evaluate.py::splice_run`)
- **spec (동결)**: `state/verdicts/H_9354_splice/splice_spec.json`
- **ckpt**: `~/anima-weights/c34/natem_c34_main_s7.clm` · `natem_c34_main_s11.clm` (base 20-SEEN · 2 seed)

## 질문

H_9327 이 남긴 벽: 연산자는 SEEN 어간에서 **살아있고**(flip1 0.98~1.00), CPT 로 쓴 사실은 **가중치에 있는데**(WRITE 0.98),
held-out 어간에선 연산자가 **우연**(0.46~0.56)이고 LIE 통제는 심은 사실이 **조회조차 안 된다**고 말했다(편향-무관 +0.073).
Fable 의 최소모형 = **two-lane**(선언 저장소 ⊥ 연산자 저장소, 다리 없음).

읽기전용 프로브로는 답할 수 없는 단 하나: **연산자의 어간 판독은 그 자리의 활성(runtime activation)의 함수인가?**

## 개입 (SPLICE)

held-out 어간 X 의 연산자 프롬프트(`이 영화 X지 않다 => `)를 돌리되, **X 의 바이트 스팬 잔차를 SEEN 어간 Y 의 것으로 이식**한다.
Y 는 **같은 담체 · 같은 어간 바이트길이** ⇒ 프롬프트 길이 동일 ⇒ 우측정렬 창에서 **스팬 오프셋이 동일**(위치 교란 0, 보정 불필요).
길이 불일치 = **skip, 절대 패딩 금지**(패딩된 donor 는 통제군이 아니라 다른 자리다).

- 답이 Y 를 따르면(부정 담체이므로 **pos donor → 부정**) ⟹ 연산자 lane 은 **그 자리의 런타임 내용을 소비**한다
  ⟹ held-out 실패 = **내용 사실**(held-out 어간 잔차에 극성 성분이 없다 · AUDIT-A 와 정합) ⟹ 활성 주입 = wire-to-prod 후보
- 답이 Y 를 무시하면(**단 SEEN→SEEN 양성통제는 성립**) ⟹ lane 판독은 **가중치-수준(라우팅/채널 정체성)** ⟹ 이식으로는 못 읽음

## DV (동결)

`dep = P(ans=긍정 | donor pol=1) − P(ans=긍정 | donor pol=0)`, **recipient 마다 paired**, 극성당 k=3 donor 평균.
전역 답 편향은 차분에서 **구조적으로 소거**(H_9327 의 LIE 검사를 인과형으로).
소비되면: `dep(flip0) → +1`(평이 담체가 donor 를 되뇜) · `dep(flip1) → −1`(연산자가 donor 를 **부정**). **부호가 주장**이다.

## 팔 (통제 ≥3 · 전부 수치 전 동결)

| 팔 | 구성 | 역할 |
|---|---|---|
| **PC** | SEEN recipient ← SEEN donor | **양성통제 = kill 게이트**(자기이식). 연산자가 다루는 게 확실한 두 어간 사이 swap 이 답을 못 움직이면 **계기가 죽은 것** — held-out 수치 판독 금지 |
| **CORE** | held-out recipient ← SEEN donor | **DV** |
| **NEU** | held-out ← 길이정합 **중립** donor (AUDIT-A 동결 중립 인벤토리 · 시드 pseudo-label) | \|dep\| ≈ 0 이어야. 아니면 "아무 패치나 답을 움직인다" |
| **SHAM** | held-out ← **자기 값** | 편집 기계 자체는 **불활성**이어야(change-rate ≈ 0) |
| **DEG** | (진단 · bar 아님) 이식된 답 vs **donor 자기 프롬프트**의 답 일치율 | 얕은 depth 에선 스팬 이식이 "그냥 donor 프롬프트 돌리기"에 **근접**(두 프롬프트는 어간에서만 다르다) ⇒ 그 동어반복 지분을 **수치로 깎아** 보고한다 |

## 층 격자 (사전등록 · 사후 최적층 선택 금지)

`depth 0..L × span-rung(끝 1B → 끝 3B → 어간 전체)` 전수 스캔, **PC 팔(SEEN 데이터)만으로** 선택 = 교정이지 tune-to-green 아님.
`l_shallow` = 고정 순서상 첫 통과 셀 · `l_deep` = 마지막 통과 셀. **전 팔을 두 셀 모두에서** 돌리고 **둘 다 보고**.
**판정은 `l_deep`에서 읽는다** — 거기가 recipient 자신의 정체성이 패치된 스팬 **밖에 아직 살아있는** 자리다.

## 동결 결정트리 (bar 는 움직이지 않는다)

```
V0  SEEN base 정확도(flip0·flip1) ≥ 0.75            아니면 INVALID-READOUT
V1  PC dep(flip1) ≤ −0.60 인 격자 셀 존재            아니면 INVALID-LOCALIZATION (계기 사실 · 벽 아님)
    ∧ SHAM change-rate ≤ 0.05
V2  |NEU dep| ≤ 0.15                                아니면 INVALID-INSTRUMENT
--- V0 ∧ V1 ∧ V2 일 때만 ---
DV  CORE dep(flip1) ≤ −0.60 ∧ 순열 p < .01     ⟹ MEDIATED    (런타임 활성 판독)
    |dep| + 1.96·se ≤ 0.20 (TOST)              ⟹ WEIGHT-LEVEL (이식이 lane 에 닿지 못함)
    그 외                                       ⟹ UNDERPOWERED (bar 불변 · n 을 올려라)
```

**kill**: 자기이식(PC) 양성통제 실패 = **계기 무효**(층/폭 재설계 1회, 그 후 INVALID — **벽 아님**).
**cement**: 2 seed(s7·s11)가 **부호 일치**해야 tier 확정.

## 계기 무결성

- **device 각인 필수** — hidden 은 GPU/CPU 가 byte-identical 아니다(2.5e-14 · cuBLAS dgemm). 출력에 device 각인 · 장치 넘어 비교 금지.
- **담체는 `cli/corpus.py` 의 `GROUND_FORMS_FLIP0/FLIP1` 을 import** — 손으로 재유도 금지(모델이 본 적 없는 문자열을 먹이면 연산자가 *우리 탓으로* 죽어 보인다).
- **스팬은 점수 창에서 계산한다**: 채점 forward 는 `seed + cont` 위에서 돈다 ⇒ 오프셋 = `T − len(seed) − len(cont)`.
  `len(cont)` 를 빼먹으면 패치가 어간이 아니라 **6B 오른쪽(= `지 않` 부정 접미사)** 에 떨어진다. (미실행 `--bind-locus` 에 이 결함이 있었고 여기서 같이 고쳤다.)

## 무엇을 지지하게 되나

- **MEDIATED** ⟹ two-lane 의 "다리 부재"는 **주소 문제가 아니라 내용 문제** — 연산자 lane 은 그 자리를 읽는데 held-out 어간이 거기 극성을 안 싣는다.
- **WEIGHT-LEVEL** ⟹ two-lane 강화 — lane 의 판독은 활성이 아니라 **가중치/라우팅**에 있고, 활성 주입은 wire-to-prod 경로가 **아니다**.
