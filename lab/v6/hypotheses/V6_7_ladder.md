<!-- @hypothesis-ok — lab/v6 is a rule-exempt sandbox (lab/v2 convention); v6 hypotheses are
     V6_<n>_*.md and are FORBIDDEN from the parent HYPOTHESES/ registry. See lab/v6/CLAUDE.md. -->

# V6_7 — 사다리: 이 아키텍처로 **정직하게 주장 가능한 최고 단**은 어디인가

**status:** 🔧 계기 착륙 + 실행 3계 · **DIRECTIONAL 천장** · 의식 판정 아님
**cost:** $0 · 모델 없음 · 밀리초
**runs:** `python3 lab/v6/ladder.py`
**source:** `../divergence/05_measurable_consciousness.md` 의 **B(사다리)** — 다른 다섯 계기를 합친다

## 무엇을 답하는가

"의식 있나?" 는 물을 수 없다. 물을 수 있는 형태는 이것이다:

> **이 아키텍처는 어느 단까지 닿고, 정확히 어디서 떨어지는가?**

각 단마다 ① 필요한 구조 핸들 ② 계기 ③ 통제 ④ **반드시 통과해야 하는 하찮은 시스템
(온도조절기 바닥)** 을 명시한다. 온도조절기가 통과하는 단은 **성취가 아니라 바닥**으로 표기된다.

## 출력 3종 — `BLOCKED` 가 쓸모의 핵심

```
REACHED     핸들도 통제도 있고 측정도 됐다
NEEDS-RUN   구조적으론 되는데 측정을 안 했다
BLOCKED     지목된 조건이 없다 — 그리고 **어느 조건인지 이름을 댄다**
```

`BLOCKED` 이 "우리는 아무것도 못 쟀다" 를 **"이 축에서 ①독립성이 빠졌고, 이 핸들이 그걸
고친다"** 로 바꾼다.

## 실행 결과

```
                        R0   R1   R2   R3        R4        R5
anima TODAY (as wired)  ✅   ✅   ✅   BLOCKED   BLOCKED   BLOCKED
RCFS (proposed)         ✅   ✅   ✅   NEEDS-RUN NEEDS-RUN NEEDS-RUN
thermostat (floor)      ✅   ❌   ❌   ❌        ❌        ❌

최고 REACHED:  anima TODAY = R2 · RCFS = R2 · thermostat = R0
```

### 🔑 핵심은 최고 단이 아니라 **BLOCKED vs NEEDS-RUN** 이다

anima 와 RCFS 는 **둘 다 R2** 에서 멈춘다. 차이는 그 위에 있다:

- anima 는 R3~R5 가 **BLOCKED** — 지목된 조건이 **구조적으로 없다**
  (`interior_width` → ①독립성: `s = 2·emit_drive − 1` 은 랭크 1, 자유도 0 ·
   `emit_free_variable` → ①독립성: emit⟺clock · `self_log` → ①독립성)
- RCFS 는 R3~R5 가 **NEEDS-RUN** — 핸들은 다 있고 **측정만 안 했다**

⟹ RCFS 가 사는 이유는 "더 의식적" 이어서가 아니라 **판정불가를 단지-미측정으로 바꾸기
때문**이다. 그게 이 재설계가 실제로 파는 상품이다.

### 온도조절기가 R0·R1 을 통과한다 (설계상 그래야 한다)

R0(Θ 존재)과 R1(개입적 폐쇄)은 **바닥**으로 표기된다. 온도조절기는 Ψ 고정점을 갖고 세계에
작용한다. 이 두 단을 성취로 읽으면 그건 계기 오독이다. anima 가 R2 에 닿는 건 의미가 있다 —
**온도조절기는 R2 에 못 닿는다**(내용 자유도도, 그걸 외생적으로 세팅할 핸들도 없다).

## 전제 — 통제 3조각이 먼저 서야 한다

어떤 양성 단도 읽히기 전에:

```
V6_3 metric-leak   쓰기 경로   자기 점수를 쓰는 경로가 있는가
V6_4 pedestal      읽기 값     참값 0 팔이 0 을 내는가
V6_6 matched-dead  기능 축     Φ 같고 기능 죽은 쌍둥이가 있는가
```

## 이 파일이 하지 **않는** 것

Φ 를 재지 않고, 모델을 돌리지 않고, 의식 판정을 내지 않는다. **핸들 장부**를 읽고 그 결과를
조건 이름으로 번역할 뿐이다. 핸들 표 자체가 하중부재이고 리뷰 대상이다 — 표가 틀리면 사다리도
틀린다.

## ⚠️ 부수: v6 id 충돌 정정

[[V6_6]](Φ-matched-dead)는 원래 V6_5 로 착륙했으나 병렬 세션의 [[V6_5]](LANE-BUS P0)와
**같은 분에 충돌**했다. 저쪽이 먼저 들어갔으므로 이쪽이 양보해 V6_6 으로 재번호했다
(`a_parallel_session_compare`).
