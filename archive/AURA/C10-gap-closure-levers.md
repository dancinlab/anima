# AURA C10–C13 — /gap full top-3 closure + 🧲 RTSC 돌파 (비침습 천장 재측정)

> `/gap full` 40-렌즈 감사가 C5–C9 toy의 3 핵심 gap을 짚음 — ① strawman lead-field ② oracle-prior 순환 ③ 미탐색 모달(OPM-MEG)·미실행 디코더(ML). 셋을 실제 측정으로 닫고(C10–C12), 사용자 follow-up "RTSC로도 돌파"를 C13으로 측정. honest: 🟡 toy(2D 8×8 sheet · synthetic · ridge/weighted/learned · 8-seed). verdict `.verdicts/c10-gap-closure/run.txt`.

## C10 — strawman lead-field 검증 (gap #1) 🟡

C5의 가우시안-blur lead-field가 결론을 정의상 보장하나? **3 커널(가우시안/지수/멱법칙) × seed 0–7**로 재측정:

| 커널 | EEG M64 | EEG M256 | tFUS M64 | 전극 sat(256−64) | sharp−blur |
|---|---|---|---|---|---|
| gauss | 0.332±.10 | 0.400±.11 | 0.809±.07 | +0.068 (포화) | **+0.476** |
| exp | 0.626±.09 | 0.832±.05 | 0.817±.07 | **+0.206** (미포화) | +0.191 |
| power | 0.485±.07 | 0.651±.04 | 0.814±.07 | **+0.166** (미포화) | +0.329 |

- ✅ **"sharp 모달 이김" 생존** (sharp−blur +0.19~+0.48, 전 커널) → C6 tFUS-명제는 lead-field 모양에 robust.
- ❌ **"전극 포화"는 가우시안 전용 인공물** — 현실적 지수/멱법칙 커널선 M64→256이 +0.17~+0.21(미포화). **C5의 전극-포화 주장 부분 반증**(PARTIAL-FALSIFY): 두피 blur가 가우시안이 아니면 전극 증설이 여전히 도움.

## C11 — oracle→현실 prior (gap #2, 순환 검증) 🟡

C7 oracle-prior(0.798)는 소스위치를 알려주고 찾는지 본 것 = 순환. **품질 열화 + 위양성 오염** prior로 재측정:

| prior | R² |
|---|---|
| blind ridge (C5) | 0.332 |
| degraded p=0.3 +4위양성 | 0.356±.24 |
| degraded p=0.6 +2위양성 | 0.523±.22 |
| oracle p=1.0 (C7) | 0.883±.09 |

→ **헤드라인 "prior로 80% 복원"은 오라클 가정에 전적 의존.** 현실 prior(불완전+오염)는 **0.36~0.52(±0.22 불안정)** — blind에서 +0.02~+0.19뿐. C7의 0.798은 거의 순환(소스 support 누설). **bayesian-순환 gap 닫음 — 정직 현실수치 = 0.36~0.52.**

## C12 — OPM-MEG 모달 + ML 디코더 (gap #3, landscape+axis) 🟡

```
C12a 융합 lever (32ch each)         C12b 디코더 (M64)
EEG-only        0.285               analytic-ridge  0.287
+fNIRS(같은blur) 0.301 (+0.016 중복) learned-Wiener  0.239
+OPM-MEG(다른물리)0.457 (+0.172 ✅)  learned-MLP     0.120
+tFUS(음향)      0.602 (+0.317 ✅)
```

- ✅ **OPM-MEG = 진짜 lever**(+0.172) — fNIRS(+0.016 중복)와 달리 자기장은 다른 물리/배치 → 비중복. 異種모달 명제가 tFUS 넘어 일반화.
- ❌ **ML/딥 디코더 = dead-end**(원래 5법): 학습 Wiener(0.239)·MLP(0.120) 둘 다 analytic ridge(0.287)에 미달. 선형 forward선 analytic inverse가 이미 최적 — 학습 디코더는 과적합/열위. **정직 negative**(a_paper_negative_ok).

## C13 — 🧲 RTSC 상온 SQUID-MEG = 최강 비침습 lever (사용자 follow-up "RTSC로도 돌파")

```
🧲 RTSC-MEG — "상온 자기 안경"
- 하는 일: 상온초전도로 cryo 없이 두피에 자기센서를 빽빽이 깔아 뇌 자기장을 고해상 읽기
- 비유: 추운 날에만 쓰던 적외선 카메라(SQUID, 액체헬륨)를 상온에서 쓰게 돼 화소를 100배 늘린 것
```

| 모달 스택 | R² |
|---|---|
| EEG-only (64ch s1.6 20dB) | 0.331±.14 |
| EEG+OPM-MEG (32ch s1.1) [C12a] | 0.483±.10 |
| **EEG+RTSC-SQUID (256ch s0.9 35dB)** | **0.854±.04** |
| RTSC-SQUID 단독 | 0.869±.04 |
| **EEG+RTSC+tFUS (풀스택)** | **0.903±.03** |

```
복원율 R²  (← 침습 ECoG ~1.0)
0.90┤                  ███ EEG+RTSC+tFUS (침습급 근접)
0.85┤              ███     EEG+RTSC-MEG
0.48┤          ███         EEG+OPM-MEG
0.33┤ ███                  EEG-only
    └─EEG─OPM─RTSC─stack─▶
```

**RTSC 지렛대 분해 — 어느 RTSC 특성이 본질?**

| RTSC 추가 특성 | R² (EEG+MEG 0.483 기준) |
|---|---|
| + 밀도 256ch | **0.649** (+0.166) ⭐ |
| + 근접도 s0.9 | 0.559 (+0.076) |
| + 저잡음 35dB | 0.500 (+0.017) |

→ 🎯 **RTSC의 돌파 본질 = 채널 밀도.** 상온초전도가 cryo(액체헬륨 dewar) 비용·부피 장벽을 없애 **자기센서를 고밀도로** 깔 수 있게 함. 현재 SQUID-MEG가 ~300ch에 멈춘 건 물리가 아니라 cryo 비용 — RTSC가 그 벽을 제거. 저잡음(+0.017)은 미미, 밀도가 지렛대.

## 지렛대 MAP v2 (C6–C13 종합)

| 지렛대 | 효과 | 종류 | 상태 |
|---|---|---|---|
| 🧲 RTSC 상온 SQUID-MEG | EEG+RTSC 0.85 / 풀스택 0.90 | 하드웨어(자기·고밀도) | ✅ 최강 |
| tFUS 음향 | +0.317 | 하드웨어(음향 우회) | ✅ |
| OPM-MEG | +0.172 | 하드웨어(자기) | ✅ |
| prior-injection | +0.02~0.19 현실 (0.55 oracle) | 算法 | ✅ 약(현실) |
| fNIRS | +0.016 | 같은-blur 중복 | ❌ |
| ML/딥 디코더 | −0.05~−0.15 | 학습 | ❌ dead-end |
| temporal-smooth (C9) | ~0 | 후처리 | ❌ |
| 전극수 (C5) | 커널의존 (가우시안 포화·지수 미포화) | 밀도 | ⚠ 조건부 |

→ **"비침습으로 침습급"의 정답 = 異種 물리 모달의 고밀도화.** 자기(RTSC-MEG)·음향(tFUS)이 두개골 전기-LPF를 물리적으로 우회하고, RTSC가 자기센서를 침습급(0.90) 도달하게 함. 算법(prior)은 보조, ML/시간/전극은 헛다리.

## honest + 다음 frontier
- 🟡 toy(2D-sheet·synthetic·8-seed): 절대%는 toy-specific. **정성 robust**: 異種물리 모달=지렛대, 같은-blur=중복, RTSC=밀도-lever.
- ⚠ RTSC-MEG는 **상온초전도 실재 가정** — 2026 현재 검증된 상온상압 초전도체 없음(LK-99 등 미확증). "있다면" 비침습 자기-MEG 밀도 혁명이 가능하다는 conditional 측정. 실 SQUID-MEG는 cryo로 이미 작동(고가·~300ch).
- C10이 C5 전극-포화를 부분반증 — 실 두피 blur 커널 모양(가우시안 vs 지수)이 전극 증설 가치를 좌우 → real head-model(MNE/OpenMEEG)이 결정적(C-lane external #1).
- 잔여 external: real head-model 다중커널 fwd · 실 OPM-MEG 데이터 · 상온초전도 실증 시 RTSC-MEG 재평가.

## 양방향 sibling
- [C5](C5-source-recon-ceiling.md)(전극-포화 부분반증됨) · [C6](C6-multimodal-breakthrough.md)(異種모달) · [C7](C7-prior-stack-levers.md)(oracle 현실화됨) · RTSC 도메인(상온초전도 — 형제 repo el-ph 잡)
