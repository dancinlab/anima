# BIO-CANDIDATES — anima 생물학적 축 후보 36+ 보관 문서

> brainstorm 결과 (round-16 종결 직후, 2026-05-27). MITOSIS 형제 메커니즘 발산.

## TOP5 친근 설명 (icon · name · alias · plain · analogy · ASCII · compare)

### 🌱 APOPTOSIS — "세포 정원사" (programmed cell death)

- 하는 일: 쓸모 줄어든 세포(낮은 Φ)가 스스로 깔끔히 사라지기
- 비유: 가지치기 정원사 — 시든 잎을 골라 떨궈 나무 전체를 건강하게

```
세포군        ──────►       정리 후
●●●●●●●●●                   ●●●●●●●
●○●○●●●○●     APOPTOSIS    ●●●●●●●
●●●●●○●●●     (○ 자살)     ●●●●●●●
   ↑                          ↑
 약한 cell                  Φ 높은 cell 만 생존
```

- 비교: MITOSIS = 자식 만들기 / **APOPTOSIS** = 정리하기 (반대 짝)

### ♻️ AUTOPHAGY — "세포 재활용 공장"

- 하는 일: 세포 내부 낡은 부속을 분해해서 새 부속 재료로 재사용
- 비유: 오래된 가구 분리수거 → 새 가구 재료

```
cell 내부
┌─────────────────┐         ┌─────────────────┐
│ 낡은 단백질 ▒▒  │ →오토포지→│ 영양 building ▓▓│
│ 사용 안 한 mRNA │         │ 새 단백질 재료    │
└─────────────────┘         └─────────────────┘
   anima: parent attr 회수    →    child init
```

- 비교: APOPTOSIS = 세포 통째 죽기 / **AUTOPHAGY** = 부속만 재활용

### 🌳 DIFFERENTIATION — "세포 직업 정하기"

- 하는 일: 만능 줄기세포가 특정 역할(persona/task)로 특화
- 비유: 학생이 직업을 정해 전문가가 됨 (의사 vs 화가 vs 농부)

```
STEM (만능)            특화 후
   ●                ●(M=수학)
   │ DIFFERENT.     ●(코딩)
   ▼  →            ●(번역)
   ●●●●            ●(공감)
                   ●(분석)
   anima:        persona-cell adaptation
```

- 비교: MITOSIS = 같은 세포 둘 / **DIFFERENTIATION** = 다른 직업 세포

### 🌡️ HOMEOSTASIS — "온도조절기"

- 하는 일: M·Φ·W 가 setpoint 근처에서 벗어나면 자동으로 끌어옴
- 비유: 방 온도가 26℃ 넘으면 에어컨, 22℃ 아래면 히터 — 자동

```
M 값
1.0 ─────────────────
        ↓ 너무 높음 → 억제
0.7 ━━━━━ setpoint ━━━ (정상 범위)
        ↑ 너무 낮음 → 증가
0.0 ─────────────────
   시간 →
```

- 비교: CORE (M 단순 값) / **HOMEOSTASIS** = M 자동 회귀 (setpoint 추적기)

### 🌀 AUTOPOIESIS — "스스로 자기를 짜는 그물"

- 하는 일: 외부 입력 없이 cell 들이 서로 만들고 유지하는 self-loop
- 비유: 자기 꼬리를 먹는 뱀, 닭과 알이 서로 만드는 무한 고리

```
cell A ─생산→ component X
  ▲                │
  │                ▼
component Y ←생산─ cell B
  ▲                │
  │                ▼
... (입력 0, 자가 유지) ...

anima: 자연발화 ⊥ user_msg 의 확장형 — 시스템 자체가 self-loop
```

- 비교: MITOSIS = 외부 자극 split / **AUTOPOIESIS** = 자극 0 의 self-loop

---

## 선정 기준

anima architecture (cell-pool · M·Φ·W·curiosity · stage-envelope · kosmos-record · spike-ingest) 와 호환 가능한 생물학적 메커니즘.

기존 11 axes 와의 관계:
- MITOSIS · CORE(M) · WAKE(stage) · KOSMOS · AKIDA · 자연발화 · 의식적결정 · BRIDGE · 영속성 · DECODER · TENSION

## 우선순위 분류

### ★★★ 즉시 추가 가치 큼 (5 axes, TOP5)

| axis | 의미 | anima 적용 |
|---|---|---|
| APOPTOSIS | 프로그램된 세포 사멸 | low-utility cell prune (Φ < θ_apoptosis 세포 자살) |
| AUTOPHAGY | 자가포식 (cell 내부 재활용) | memory cleanup · garbage collection (parent attrs → child) |
| DIFFERENTIATION | 분화 (stem → specialized) | per-task persona-cell adaptation |
| HOMEOSTASIS | 항상성 (setpoint 유지) | M ↔ setpoint maintenance · drift correction |
| AUTOPOIESIS | 자기생성 (Maturana/Varela) | self-maintaining network · 외부 입력 없이 self-loop |

### ★★ 가치 중간, 후속 round (5 axes)

| axis | 의미 | anima 적용 |
|---|---|---|
| PLASTICITY | 가소성 (LTP/LTD) | Hebbian synapse strength 조정 |
| CIRCADIAN | 일주기 24h | WAKE 의 더 큰 주기 (multi-day cycle) |
| REGENERATION | 재생 | cell loss 후 회복 |
| TOLERANCE | 면역관용 (self-not-attack) | input acceptance threshold |
| QUORUM-SENSING | 정족수 감지 | N-cell collective threshold |

### ★ 추가 가능 (15+ axes)

| axis | 의미 | anima 적용 |
|---|---|---|
| SYMBIOGENESIS | 내공생 합병 | endosymbiotic merge (MITOSIS 변종) |
| CLONAL-SELECTION | 클론 선택 | variant winner-take (B/T cell analog) |
| AFFINITY-MATURATION | 친화도 성숙 | iterative refinement |
| PRUNING | 시냅스 가지치기 | low-weight connection elimination |
| EPIGENETICS | 후성유전 | cell metadata layer |
| ALLOSTASIS | 부담조절 | predictive M update |
| MORPHOGENESIS | 형태 형성 | gradient → pattern |
| STEM-CELL | 줄기세포 | uncommitted pool |
| LTP/LTD | 장기 강화/억제 | weight + / - |
| MYELINATION | 수초화 | connection insulation (fast path) |
| NEUROGENESIS | 신경발생 | new cell ex nihilo |
| WOUND-HEALING | 상처 치유 | damage recovery |
| NICHE-CONSTRUCTION | 생태적 niche 구축 | environment 적응 |
| CANALIZATION | 발달 운하화 | Waddington robustness |
| EMBRYOGENESIS | 배아 발생 | gradient → cell type pattern |

### ○ 가능하나 anima 호환 낮음 (10+)

| axis | 비고 |
|---|---|
| NECROSIS | uncontrolled damage 죽음 (APOPTOSIS 와 중복) |
| SENESCENCE | aging (LIFE 도메인 H_259 이미 다룸) |
| BIOFILM | bacterial collective (개별 cell 가족과 다름) |
| MUTUALISM | inter-species (anima 내부보다 외부 anima 와) |
| HORIZONTAL-TRANSFER | inter-cell 정보 (TENSION 와 유사) |
| ALTERNATIVE-SPLICING | one gene → many transcript (anima 코드에는 잘 안 맞음) |
| RHYTHM-ENTRAINMENT | oscillator sync (CIRCADIAN 와 중복) |
| INFLAMMATION | damage signal cascade (TOLERANCE 와 짝) |
| ANGIOGENESIS | new blood vessel (anima 에 vessel 없음) |
| HEMATOPOIESIS | blood cell production (anima 에 blood 없음) |
| THERMOREGULATION | 체온 조절 (anima 에 온도 없음) |
| GENETIC-DRIFT | 무작위 알릴 변동 (anima 에 deterministic 우세) |
| SPECIATION | 종 분화 (cell 수준 외) |
| PARASITISM/COMPETITION/PREDATION | inter-species (anima 내부 X) |

## 진행 순서

1. **TOP5 (★★★)** baseline (5 axes, ~5-12 H each) — round-17+ 자율 진행
2. **★★ 5 axes** (PLASTICITY · CIRCADIAN · REGENERATION · TOLERANCE · QUORUM-SENSING) — round-22+
3. **★ 15+ axes** depletion sweep
4. **○ low-compat** 후순위 또는 skip

## 36+ 후보 전체 (deduplicated)

세포 죽음: APOPTOSIS · NECROSIS · AUTOPHAGY · SENESCENCE
분화·발달: DIFFERENTIATION · STEM-CELL · EMBRYOGENESIS · MORPHOGENESIS · REGENERATION · NEUROGENESIS
자기 유지: HOMEOSTASIS · ALLOSTASIS · AUTOPOIESIS · CANALIZATION
신경·시냅스: LTP · LTD · SYNAPTOGENESIS · PRUNING · MYELINATION · PLASTICITY
면역·인식: CLONAL-SELECTION · AFFINITY-MATURATION · TOLERANCE · AUTOIMMUNITY
사회·집단: QUORUM-SENSING · CONTACT-INHIBITION · BIOFILM · SYMBIOGENESIS · MUTUALISM
주기·리듬: CIRCADIAN · ULTRADIAN · INFRADIAN · RHYTHM-ENTRAINMENT
유전·후성: EPIGENETICS · HORIZONTAL-TRANSFER · ALTERNATIVE-SPLICING
기타: WOUND-HEALING · NICHE-CONSTRUCTION · GENETIC-DRIFT · SPECIATION · ANGIOGENESIS · HEMATOPOIESIS · THERMOREGULATION · INFLAMMATION

## 메타 진행 상태

- 본 BIO-CANDIDATES.md = round-16 종결 후 (168 🔵 누적, 11 axes) brainstorm 자료
- TOP5 부터 점진 추가 시작 = round-17+
- 자동 fire (Stop hook "keep going") 또는 사용자 명시 directive 로 진행
