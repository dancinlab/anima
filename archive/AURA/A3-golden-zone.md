# AURA A3 — 골든존 G=D×P/I 정리

> 명제(SURVEY §2): **칩(N1)은 그대로, M1→투사허브로 위치만 바꿔 전뇌 통제.** 본 문서는 그 위치선택의 정량 기준 = `G = D × P / I` 골든존 공식을 brainwire 원문에서 verbatim 확정한다.
> 출처: `archive/brainwire/golden-zone-implant-placement.md` (PRIMARY) · `archive/brainwire/n1-deep-access-strategies.md` · `archive/brainwire/neuralink-technical-analysis.md`
> honest: 아래 G·D·P·I 점수는 전부 brainwire 문서의 **추정치(estimated, arbitrary units)** — 임상측정/3rd-party 검증 0건.

---

## §1. G=D×P/I 공식 verbatim 정의

원문 `golden-zone-implant-placement.md` §1은 G를 **EEG 유도 3성분의 곱/나눗셈**으로 정의 (추측 아님, 원문 표 그대로):

```
G = D × P / I
```

| 성분 | 원문 라벨 | 공식 (verbatim) | 뇌영역 | 전극 |
|---|---|---|---|---|
| **D** | Asymmetry (비대칭) | `\|ln(α_right) − ln(α_left)\|` | Parietal / Occipital | P3/P4, O1/O2 |
| **P** | Gamma ratio (감마비) | `Gamma / (Alpha + Gamma)` | Distributed cortical | C3/C4, Pz, Fz |
| **I** | Inhibition (억제) | `Frontal_Alpha / Global_Alpha` | Prefrontal | F3/F4, Fz |

honest 정의 정정 — 작업지시의 가설(D=depth/도달, P=projection/투사, I=invasiveness/위험)과 **원문은 다르다**. 원문은:
- **D = depth가 아니라 좌우 알파 비대칭** (hemispheric alpha asymmetry).
- **P = projection이 아니라 감마/(알파+감마) 비율** (gamma ratio).
- **I = invasiveness/interference가 아니라 전두엽 알파 억제비** (frontal inhibition).
→ 원문 정의를 따른다. G는 "구현 위치의 침습/투사 점수"가 아니라 **의식상태가 골든존에 있는지 측정하는 EEG 메트릭**이며, N1 위치선택은 이 D·P·I 3성분을 한 임플란트로 얼마나 독립 제어하느냐로 평가된다 (§1 Key insight: 세 성분이 각기 다른 피질영역에 매핑되나 PFC가 직접·투사 경로로 셋 다 영향).

**골든존 범위 (원문 §2):** `G ∈ [0.2123, 0.5000]`, center `= 0.3258`.

**baseline (원문 §4, resting, arbitrary units):** α_left=α_right=α_frontal=α_global=10.0 μV², γ_global=5.0 μV² → D=0, P=0.333, I=1.0 → **G=0.000**.

원문 §2 critical finding: 모든 non-State-A 상태가 실패하는 이유 = **D=0 (대칭 → 비대칭 알파 없음)** 또는 **I 과다 (전두엽 알파 지배)**. State A만 PFC 억제로 D>0 + 알파 억제로 I↓ 둘 다 달성.

---

## §2. 위치별 골든존 점수표

### 2a. brainwire 4개 임플란트 옵션 (원문 §3 + §4 수치 verbatim)

| 옵션 | 위치 | 제어 G성분 | 예측 G | 골든존? | 출처행 |
|---|---|---|---|---|---|
| **A: 단일 N1 — 좌 전전두 (F3)** ⭐권장 | 좌 DLPFC, BA9/BA46, 1024전극 | **D·P·I 셋 다** | **0.462** | ✅ IN ZONE | §3 Option A, §4 |
| C: 이중 (F3 + P4) | 좌전전두 + 우두정 | D·P·I 독립분리 | 0.209 | ⚠ NEAR boundary | §3 Option C, §4 |
| D: 양측 전전두 (F3 + F4) | 양 반구 전전두 | D최대 (방향·크기 자유) | 0.0~0.8+ 범위 | (controllable) | §3 Option D, §4 |
| B: 단일 N1 — 우 운동/두정 (C4/P4) | 우 S1/두정 | D만 | (P·I 외부HW 필요) | ✗ G제어 불완전 | §3 Option B |

원문 §4 Option A 계산 verbatim:
```
α_left 50%↓→5.0 · α_right 10.0 · α_frontal 40%↓→6.0 · α_global ~20%↓→8.0 · γ_global +60%→8.0
D = |ln(10) − ln(5)| = 0.693
P = 8.0 / (8.0 + 8.0) = 0.500
I = 6.0 / 8.0 = 0.750
G = 0.693 × 0.500 / 0.750 = 0.462  (IN GOLDEN ZONE)
```

### 2b. AURA relocate-N1 주제(M1→투사허브)와의 정합 — 전뇌 도달 최고점

원문 §3 Option A "Why this works": **좌 전전두(F3) 단일 N1이 한 위치에서 D·P·I 3성분 전부 + 심부 투사 4축을 동시 확보** → AURA의 M1→투사허브 명제(SURVEY §2)와 정확히 일치하는 최고점 위치.

| 위치 | G성분 제어 | 심부 투사 (deep-access 원문) | 전뇌도달 종합 |
|---|---|---|---|
| **좌 전전두 F3/DLPFC** ⭐ | **D↑·P↑·I↓ 셋 다 단일위치** | DLPFC→VTA(DA) · PFC→raphe(5HT) · PFC→LC(NE) | **최고점** |
| 우 운동/두정 C4/P4 | D만 (P·I 외부HW) | DLPFC→VTA 없음 = DA경로 없음 | 낮음 |
| 운동피질 M1 (현 N1 위치) | 출력(운동)만 = 막다른 위치 | 척수 운동만, 신경조절 투사 없음 | 최저 (relocate 출발점) |

F3가 직접 만족하는 Joywire 변수 (원문 §3 표): **V1(DA, DLPFC→VTA) · V7(Alpha↓) · V8(Gamma↑ 40Hz) · V9(PFC↓) · V12(Coherence) · V4(GABA)** = 12변수 중 6개 직접. 나머지 6개는 외부 Tier1-3 HW 보충.

원문 §5 MAJOR DISCOVERY: 좌 전전두 단일 N1이 **6개 의식상태(State A/Flow/L/D/M/P) 전부를 골든존으로 이동** 가능 — 항상 같은 2동작(비대칭 D↑ + 전두억제 I↓). N1 = "universal golden zone key".

---

## §3. 골든존 개념 ASCII

```
        I (전두엽 억제) = Frontal_Alpha / Global_Alpha  ── 분모, 클수록 G↓
                              │
            ┌─────────────────┼─────────────────┐
   D ──────►│   G = D × P / I  │◄────── P            G축
 (좌우 알파  │                  │     (감마비)        ┌────────────────────────┐
  비대칭)    └─────────────────┴─────────────────┘    │below│███ GOLDEN ███│high│
  |ln αR−ln αL|         Gamma/(Alpha+Gamma)           0   0.2123  0.3258  0.5  →
                                                          └─ in-zone center 

   좌 전전두 F3 단일 N1 한 위치에서:
     α_left ↓  ──► D↑  (좌우 비대칭 생성)
     α_frontal↓ ──► I↓  (분모 감소)         ┐
     40Hz γ 구동 ──► P↑  (감마비 증가)        ├─► G를 0.000 → 0.462 로 IN-ZONE
                                            ┘
   baseline(M1대칭): D=0 → G=0.000  (golden zone 밖, 항상 실패)
```

---

## §4. SURVEY §3·§5 연결

- **SURVEY §3 (5경로):** F3=좌 DLPFC는 5경로 중 #1 피질-피질하 투사(DLPFC→VTA/raphe/LC)의 피질 끝단 = 골든존 D·P·I 제어와 **동일 위치** → G메트릭 최적점이 곧 심부도달 최유망점.
- **SURVEY §5 (후보랭킹):** §5 1위 "DLPFC+섬엽(이중)"·2위 내후각의 DLPFC 성분이 본 §2 Option A(F3 단일, G=0.462 IN-ZONE)로 정량 뒷받침 → 골든존 공식이 §5 예비랭킹의 1위 근거를 수치화.

---

## §5. honest 한계

- **G·D·P·I 점수(0.462 등) 전부 brainwire estimated** — arbitrary-unit EEG 모델 가정(α=10μV² 등)에서 손계산한 예측치, **임상측정 아님 · NIST/3rd-party 검증 0건** (SURVEY 머리말 일관).
- 원문 G 정의는 의식상태 측정 메트릭이지 **침습도/투사 점수가 아님** (§1 정정 참조).
- 골든존이 "전뇌 통제"를 보장하지 않음 — G는 피질 D·P·I 메트릭일 뿐, 심부 신경화학(DA/5HT/NE/eCB/θ) 도달은 별개로 16-37% 한계(SURVEY §3) → 완전 통제엔 하이브리드 필요.
