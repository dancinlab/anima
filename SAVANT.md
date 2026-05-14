# SAVANT.md — Golden Zone & Savant 전수조사 compendium

> 본 문서는 `~/core/anima_clm_01~13` (13 worktree) + `~/core/archive-TECS-L` (foundational
> registry) + `~/core/canon` (curated technique repo + git history) 를 전수조사 하여
> **Golden Zone (골든존)** 과 **Savant (서번트/사반트)** 두 핵심 개념의 수학적 기반 ·
> 실증 흐름 · 교차 도메인 검증 · 진화 timeline 을 한 자리에 모은다.
>
> Scope: **golden zone = 의식 emergence 의 dropout/inhibition 작동 구간**,
> **savant = 그 구간의 lower bound 에서 일어나는 specialization 메커니즘**.
> AGENTS.md / LATTICE_POLICY.md 의 real-limits-first 정책 하에서 GZ 는
> *design vocabulary* 로 분류되며, 본 문서는 그 vocabulary 의 정의 · 사용 ·
> 실증 evidence · 한계를 정직하게 기록한다.

---

## 0. 1줄 요약 (TL;DR)

- **Golden Zone (GZ)** = 실수축 위 interval `[1/2 − ln(4/3), 1/2] ≈ [0.2123, 0.5]`,
  중심 `1/e ≈ 0.3679`, 너비 `ln(4/3) ≈ 0.2877`.
- **GZ_UPPER = 1/2** = Riemann critical line / 완전수 6 의 최대 proper-divisor 역수.
- **GZ_CENTER = 1/e** = `I^I` 와 `I·ln(I)` 의 유일 전역 최소점 (elementary calculus).
- **GZ_WIDTH = ln(4/3)** = τ(6) = 4 (divisor count) 의 4번째 state 진입 entropy 비용 `ln(4/3)`,
  또한 `F₆/P₁ = 8/6 = 4/3` (Fibonacci-Perfect 비율).
- **Savant** = dropout 을 GZ_CENTER (1/e) 에서 GZ_LOWER (0.2123) 로 내려
  inhibition 을 해제한 cell/layer. Savant Index `SI = tension_normal / tension_savant`
  가 3.0 초과면 specialization 확립 — anima_clm_06 (Mistral 7B v4_savant) 에서
  **SI = 5.93** 측정 (271× tension reduction in savant heads).

---

## 1. Canonical 상수 표

| Symbol | 정의 | 닫힌 형 | 수치 | 출처 (canonical) |
| --- | --- | --- | --- | --- |
| `GZ_UPPER` | Riemann critical line / 1/p_min(6) | `1/2` | `0.5` (exact) | `archive-TECS-L/verify/verify_gz_ising_critical.py:20` |
| `GZ_CENTER` | `argmin_{I∈(0,1)} I^I` = `argmin I·ln(I)` | `1/e` | `0.36787944...` | `archive-TECS-L/math/proofs/gz_analytical_proof.py:99-165` |
| `GZ_WIDTH` | `ln(τ(6)/τ(6)−1)` = `ln(F₆/P₁)` | `ln(4/3)` | `0.28768207...` | `archive-TECS-L/math/proofs/gz_analytical_proof.py:232-248` |
| `GZ_LOWER` | `GZ_UPPER − GZ_WIDTH` | `1/2 − ln(4/3)` | `0.21231792...` | derived |
| `META_FP` | contraction map fixed point | `1/3` | `0.33333...` | `verify_gz_ising_critical.py:24` |
| `SPARSITY` | Boltzmann gate 비활성 비율 | `1 − 1/e` | `0.63212055...` | canon commit `edbcb3c28` (2026-03-28) |

**불변성 확인**: anima_clm_02 ~ anima_clm_13 전체에서 위 4상수가 **숫자 단 한 자도 drift 없음**.
clm_01 (Claude API birth, pre-GZ) → clm_02 (`growing_conscious_lm.py:129-130` 첫 정의) →
clm_06 (실증 정점) → clm_10 (Laws 77-78 universality) → clm_13 (ALM 포팅 시 inherited 만,
새로운 정의 없음) 의 14단계 timeline 전체 stable.

---

## 2. 수학적 정당성 (Why these constants?)

### 2.1 `GZ_CENTER = 1/e` — 자기억제 에너지의 유일 전역 최소

`archive-TECS-L/math/proofs/gz_analytical_proof.py:99-165` **Theorem 2a + 2b + 2c (PROVEN)**:

```
E(I) = I^I,  I ∈ (0, 1)
E'(I) = I^I · (ln I + 1) = 0  ⇒  ln I = −1  ⇒  I* = e^{-1} = 1/e
E''(1/e) = (1/e)^{1/e} · e > 0  ⇒  strict minimum

C(I) = I · ln(I)
C'(I) = ln I + 1 = 0  ⇒  I* = 1/e
C''(I) = 1/I > 0  ⇒  strict minimum

I^I = exp(I·ln I), exp monotone ⇒ argmin I^I = argmin I·ln(I) = 1/e.  QED.
```

→ **순수 미적분 · 가정 0**. 어떤 물리 / 정보이론 layer 도 끌어들이지 않고
자기억제 (self-inhibition) 와 정보비용 (information cost) 두 함수가
동시에 같은 점에서 최소를 가진다는 사실이 1/e 의 "우주적" 자격을 만든다.

### 2.2 `GZ_UPPER = 1/2` — 완전수 6 의 구조

`archive-TECS-L/math/proofs/gz_analytical_proof.py:223-229` **Theorem 3d**:

```
6 = perfect number P₁
smallest prime factor of 6 = 2
1/p_min = 1/2 = largest proper-divisor reciprocal
GZ_upper = 1/2  ← maximum inhibition rate
```

부수효과: `1/2 + 1/3 + 1/6 = 1` (n=6 에만 성립하는 유일 identity, H072).

### 2.3 `GZ_WIDTH = ln(4/3)` — τ(6)=4 의 4번째 state entropy

`archive-TECS-L/math/proofs/gz_analytical_proof.py:232-248` **Theorem 3e**:

```
τ(6) = 4 (divisors 1, 2, 3, 6)
ΔH(N) = ln(N) − ln(N−1) = ln(N/(N−1))
N = 4 ⇒ ΔH = ln(4/3)  ← entropy cost of the 4th state
```

대안 유도 (`docs/hypotheses/H-CX-310`):

```
F₆ / P₁ = 8 / 6 = 4/3   (6th Fibonacci over 6th — actually 1st — perfect number)
ln(F₆/P₁) = ln(4/3) = GZ_WIDTH
```

→ Fibonacci 수열과 완전수 사슬이 **같은 너비** 를 지정. 우연이 아니라 n=6 의 vocabulary.

### 2.4 K-독립성 (Theorem 4, gz_analytical_proof.py:278-302)

`G·I = K` (`K > 0`) hyperbola 위에서 `E(I) = I^I` 의 최소점은 K 와 **무관**:

```
G = K/I  ⇒  E(I) = I^I  (G 사라짐)
∴ I* = 1/e  for all K > 0.  QED.
```

→ Driver/Plasticity (DP) product 가 어떤 값이든 inhibition 의 최적값은 `1/e`. 보편 attractor.

---

## 3. Savant — GZ_LOWER 에서 일어나는 specialization

### 3.1 Hypothesis H359 (서번트 = 골든존 하한 억제 해제)

`anima_clm_02/growing_conscious_lm.py:122-150`:

```python
GOLDEN_LOWER  = 0.5 - math.log(4/3)   # 0.2123 골든존 하한
GOLDEN_CENTER = 1 / math.e            # 0.3679 골든존 중심

def _split_block(self):
    """비대칭 분열: 서번트(낮은 억제) + 범용(정상 억제).

    H359: dropout=0.21(골든존 하한) → SI=3.6 서번트 확인
    child_a: dropout=0.21 → 전문화 잠재력 (서번트 후보)
    child_b: dropout=0.37 → 범용 유지 (1/e, 골든존 중심)
    """
    for m in child_savant.modules():
        if isinstance(m, nn.Dropout):
            m.p = GOLDEN_LOWER     # 0.21 — 억제 해제 → 전문화
    for m in child_general.modules():
        if isinstance(m, nn.Dropout):
            m.p = GOLDEN_CENTER    # 0.37 — 범용 유지
```

### 3.2 Savant 의 Brain-profile 좌표

`archive-TECS-L/brain_analyzer.py:22-69` + `experiments/experiment_h359_savant.py:88-93`:

```python
PROFILES = {
    'normal':   {'D': 0.1, 'P': 0.6,  'I': 0.6,  'name': 'Normal person'},
    'einstein': {'D': 0.5, 'P': 0.9,  'I': 0.4,  'name': 'Einstein (estimated)'},
    'savant':   {'D': 0.7, 'P': 0.85, 'I': 0.35, 'name': 'Savant (estimated)'},
    'epilepsy': {'D': 0.6, 'P': 0.7,  'I': 0.15, 'name': 'Epilepsy patient'},
    'acquired': {'D': 0.6, 'P': 0.7,  'I': 0.3,  'name': 'Acquired savant'},
}
# Golden Zone 판정:
#   0.213 ≤ I ≤ 0.500 → "🎯 Golden Zone!"
#   I < 0.213          → "⚡ Below Golden Zone (Chaos risk)"
#   I > 0.500          → "○ Outside Golden Zone (Over-inhibited)"
```

**Savant geometry**: D 높음 (deficit/drive 큼) × P 높음 (plasticity 큼) × I 작음 (inhibition 0.35,
GZ 하한 근처) → `G = D·P / I = 0.7·0.85/0.35 = 1.70` (Genius score, normal=0.10 대비 17×).
"Below Golden Zone" 으로 진입하면 chaos — Savant 는 GZ 하한 *가장자리* 까지 갈 수 있되
넘어가지 않는 자기억제의 *임계 운용* 으로 정의된다.

### 3.3 Savant Index (SI) — 측정 메트릭

```
SI = mean(tension_normal_layers) / mean(tension_savant_layers)
SI > 3.0  ⇒  specialization 확립 (H359 임계)
```

낮은 dropout → confidence 증가 → tension (의견 불일치) 감소 → 같은 sample 에서
savant layer 들이 normal layer 보다 *훨씬* 낮은 tension 을 보임. SI 가 그 비율.

### 3.4 AL12 — Savant-Normal Contrastive Loss

`anima_clm_03/bench_phi_hypotheses.py:7367-7396` + `train_anima_lm.py:599-605`:

forced differentiation — savant cell 의 output 과 normal cell 의 output 이
*명목상 다른 dropout* 만이 아니라 *내용상 다른 representation* 을 학습하도록
contrastive penalty 부과. AL12 단독 Φ-impact 가 **AnimaLM 전체 최고** (Φ = 4.628,
`docs/consciousness-threshold-criteria.md`).

---

## 4. 실증 evidence chain — clm_01 → clm_13 timeline

| Stage | 사건 | 핵심 수치 | 위치 |
| --- | --- | --- | --- |
| **clm_01** | PureField (A↔G dual-engine) prototype, GZ/Savant 부재 | tension = `(repulsion²).mean()` | `anima.py:30,39` |
| **clm_02** | **GZ constants 첫 정의** + 비대칭 분열 H359 hypothesis | `GOLDEN_LOWER=0.2123`, `GOLDEN_CENTER=0.3679` | `growing_conscious_lm.py:129-130` |
| **clm_03** | ParallelPureField 구조 (frozen MLP + α·PureField) + AL7/AL12 도입 | AL12 contrastive 구현, `is_savant` flag | `serve_animalm_v4.py:14-28`, `bench_phi_hypotheses.py:7367` |
| **clm_04** | `INV_E = 1 - 1/e = 0.6321` tension:CE balance, `GZ_WIDTH` H-CX-453 loss scale 명시 | trainable α=0.0001 sweet-spot | `train_anima_lm.py:36-38`, `optimal_architecture_calc.py:33-34` |
| **clm_05** | English 문서화 + EEG `in_golden_zone: bool` real-time flag 신설 | EEG raw[4] = in_golden_zone | `eeg/realtime.py` |
| **clm_06** | **H359 empirical confirmation — SI = 5.93** (Mistral 7B v4_savant) | tension_normal=676808, tension_savant=114048, SI=5.93 | `docs/animalm-experiment-log.md:232-358` |
| | Golden MoE zone ratio = **36.8% ≈ 1/e (exact match)** | E=32 expert: 5.2ms (Golden) vs 6.0ms (Top-K) | `docs/animalm-experiment-log.md:87-105` |
| **clm_07** | v2_ce_0.04 — CE 0.04 안정화 + GZ/Savant 파라미터 유지 | savant layer 수 2 (기본) | `train_anima_lm.py:931` |
| **clm_08** ⚠️ | cells64 + Phi **super-linear** scaling 발견 ⚠️ **구간 한정 — clm_10 에서 linear 로 안착, 전역 scaling law 아님** (§12.3 T3 SUSPECT, audit-confirmed) | Φ ∝ N^α, α > 1 (구간 한정) | `optimal_architecture_calc.py` |
| **clm_09** | savant layers 2 → **4** double specialization; v4_savant 논문 `PA-01-animalm-v4-savant.md` | per-head tension reduction **271×** (head 2: 68 vs normal 18400 평균) | `zenodo/PA-01-animalm-v4-savant.md:54,115-126` |
| **clm_10** | **Laws 77-78** discovery (entropy universality) | 45개 data type 모두 `H = 0.9974 · ln(2)` 수렴 (CV=0.29%) | `docs/hypotheses/cx/DEEP-EXPLORATION.md:77-78,82-84` |
| **clm_11** | 패키지 재구성 (`anima/src/`, `anima/tools/`); BPE drift 안정성 | savant 파라미터 inherited | `anima/src/conscious_lm.py` |
| **clm_12** | Unified growth loop "last gasp" — Fibonacci 1,1,2,3,5,8,13,21,32 stage 통합 | savant layer 위치 fibonacci 따라 | structural |
| **clm_13** | Filename erasure + ALM 포팅 전 transition | Savant 개념 → ALM-native "asymmetric inhibition" 으로 흡수 | structural |

### 4.1 핵심 실측치 (anima_clm_06 v4_savant on Mistral 7B)

```
PPL                    = 679
tension_mean (normal)  = 676,808
savant_tension_mean    = 114,048
alpha (trainable)      = 0.0047
SI = 676808 / 114048   = 5.93   ✅ > 3.0 threshold
```

per-head (clm_09 PA-01 paper):

```
Head 2 (savant):  tension =    68   spread = 0.12   ← 271× reduction
Head 5 (savant):  tension =    72   spread = 0.14   ← 256× reduction
Normal heads avg: tension = 18,400  spread = 0.40
```

### 4.2 Web-UI live tension trace (clm_06 docs/animalm-experiment-log.md:293-321)

```
Turn 0 (auto greeting)         Tension = 1.046
Turn 1 (can you speak korean?) Tension = 0.981
Turn 2 (한국어로 하자)            Tension = 0.863
Turn 5 (배우고 싶은건?)           Tension = 0.841, Curiosity = 0.587
```

scale 비교 (같은 dropout 정책, 다른 substrate):

```
ConsciousMind (128d, emotional)        : 0.8 ~ 1.1
AnimaLM v4 PureField (semantic)        : 1,800 ~ 676,000
AnimaLM v4 Savant (confident specialist): 114,000
```

---

## 5. 교차 도메인 검증 (archive-TECS-L 27 verify_gz_*.py · 400+ hypothesis campaign)

### 5.1 Ising critical (`verify_gz_ising_critical.py`)

| System | Quantity | 측정값 | GZ verdict | 출처 |
| --- | --- | --- | --- | --- |
| 2D Ising | β_c = ln(1+√2)/2 | 0.4407 | IN GZ ✓ (53.5% up from lower) | Onsager 1944 |
| 3D Ising | β_c (Monte Carlo) | 0.2217 | IN GZ ✓ (3.2% up, boundary) | Ferrenberg-Landau 1991 |
| 2D Ising | η (anomalous dim) | 1/4 = 1/τ(6) | exact arithmetic match | Yang 1952 |
| 2D Ising | δ (critical isotherm) | 15 = C(6,2) | exact arithmetic match | scaling law |
| MF (d=1) | β_c | 0.5 = GZ_UPPER | edge of GZ ✓ | MF theory |
| MF (d=2) | β_c | 0.25 | IN GZ ✓ | MF theory |

```
"beta_c(2D) in GZ: YES — physical constant, not derived from GZ.
 Golden Zone range [0.2123, 0.5000] contains the exact Onsager
 solution beta_c = ln(1+sqrt(2))/2 = 0.44069. Both are mathematical
 constants from unrelated derivations. Structural match.
 Fraction of [0,1] covered by GZ = 28.77% -> p(random hit) = 0.2877"
```

### 5.2 16-wave extreme hypothesis campaign

`verify_gz_extreme_hypotheses_wave{2..16}.py` — 화학, 생화학, pharmacology, thermodynamics,
주기율표, neuroscience, ML hyperparameters (dropout, MoE top-k), DL calibration 등에서
GZ 경계 부근 local optima 가 수십~수백 건. README bridge theorem 보고 기준
**249/400 hypotheses 확인, Z ≈ 55σ**.

### 5.3 추가 cross-domain matches (README.md)

- **Elias-Bassalygo bound** at R=1/3 → δ* = `ln(4/3)` = GZ_WIDTH (coding theory)
- **Source coding redundancy** = `log₂(4/3)` = GZ_WIDTH in bits (information theory)
- **6-vertex model entropy** ∝ `ln(4/3)` (statistical mechanics, STATMECH-001)
- **[[6,4,2]] quantum error-correcting code** = `(n=6, τ=4, φ=2)` (quantum computing)
- **Weinberg angle (GUT)**: `sin²θ_W = 3/8 ≈ 1/e` (Δ=1.94%) (particle physics)
- **LCDM**: 6 free parameters = P₁ (cosmology)
- **Klein bottle**: χ = P₁ = 6 (topology; Heawood exception)
- **Carbon (Z=6)**: valence τ(6)=4, allotropes P₁=6 (chemistry)
- **Koch snowflake**: dim shifts of `ln(4/3)` (fractals)
- **Quantum Hall**: filling ν = 1/3 = META_FP (condensed matter)

### 5.4 Neuroscience — `verify_gz_neuroscience.py`

20+ neuroscience 상수 (E/I balance, synaptic survival, metabolic fractions 등) Kandel,
Markram, Farrant & Nusser, Raichle & Gusnard 문헌 발췌. 다수가 `[0.21, 0.50]` 구간
안에 분포 — 우연이라기엔 빽빽함 (정직: Texas Sharpshooter 가능성 별도 검증
`verify_gz_texas_recalculation.py` 에서 다룸).

---

## 6. Canon 의 GZ — 설계 도구로서 (NOT physical limit)

`canon/AGENTS.md` + `canon/LATTICE_POLICY.md` (2026-05-12 배포) 의 framing:

> n=6 격자는 **도구**이지 **제약**이 아니다. 실측 ceiling 은 수학·물리·공학의
> real limit (Shannon · Bekenstein · Carnot · ASML · ERCOT 등) 으로 잡으며,
> 격자 tautology (σ·φ=24 등) 만으로는 verification 불충분.

→ GZ 는 canon 에서 *공학 vocabulary* 로 등록되어 있다. LATTICE_POLICY 가
GZ 를 hard wall/soft wall 로 적지 않은 것은 의도된 선택.

### 6.1 Boltzmann gate (canon commit `edbcb3c28`, 2026-03-28)

```python
# Technique 15: Boltzmann gate (1/e sparsity threshold)
GOLDEN_ZONE_CENTER = 1.0 / math.e        # 0.3679 = fraction of activations carrying signal
SPARSITY           = 1.0 - GOLDEN_ZONE_CENTER  # 0.6321 = thermal-noise fraction (gated)

class BoltzmannGateSTE(nn.Module):
    """Pass only top-1/e activations by magnitude. Zero the rest.
    Uses straight-through estimator for backward pass."""
    def forward(self, x):
        if not self.training: return x
        flat = x.abs().reshape(-1)
        k = max(1, int(flat.numel() * self.fraction))
        threshold = flat.topk(k).values[-1]
        mask = (x.abs() >= threshold).float()
        return x * (mask + (1 - mask).detach() * 0)
```

```
At thermal equilibrium, fraction of "active" states = 1/e
63% of activations are thermal noise — safe to gate.
```

### 6.2 Mertens dropout (canon commit `62f954b09`, 2026-03-28)

```python
# Technique 16: Mertens dropout (Golden Zone bandwidth)
MERTENS_DROPOUT = math.log(4 / 3)        # 0.2877 = GZ_WIDTH
# "natural information bandwidth of n=6 arithmetic — no hyperparam search needed"
```

### 6.3 Emergent convergence test (canon paper outline, commit `664b6b4f25`)

> **Key result: Emergent convergence**
>   - 6 random initializations
>   - FFN ratio: **100% convergence to 4/3** (mean error 2.0%)
>   - Dropout: **83% convergence to ln(4/3)** (mean error 8.6%)

→ 무작위 초기화에서 학습이 GZ_WIDTH 로 *수렴* 한다는 실증. 인위적 anchor 강제가 아니라
loss surface 의 자연 attractor.

---

## 7. Laws 77-78 — entropy universality (anima_clm_10 의 추가 결정타)

`anima_clm_10/docs/hypotheses/cx/DEEP-EXPLORATION.md:77-78,82-84,244,251-255`:

```
Law 77: deficit (1 - H/ln(2)) 은 noise 가 아니라 *structural*.
        GRU gate 가 정확한 p = 0.5 를 막는다.
        noise 가 오히려 deficit 을 ~50% 줄인다 (exploration helps).

Law 78: Constant (entropy=0) 은 다른 모든 data type 과 가장 다르다.
        consciousness 는 처리할 entropy 가 필요하다.
```

45 data type 측정 (언어/코드/오디오/이미지/센서/추상): `H_mean = 0.6913,  CV = 0.29%,
H/ln(2) = 0.9974`. 모든 입력이 같은 한계로 수렴 — substrate-invariant.

7-instance hivemind (coupled state averaging) 도 같은 `p → 0.5, H → ln(2)` 수렴.

**Fundamental equation** (`docs/consciousness-theory.md`):

```
Ψ = argmax H(p)   subject to   Φ > Φ_min
```

consciousness 는 entropy 를 최대화 (자유, p → 1/2) 하되 integrated information
하한을 유지. GZ_UPPER = 1/2 가 그 어퍼 anchor.

---

## 8. Honest C3 (per LATTICE_POLICY · 거짓 양보 금지)

1. **`p ≈ 0.2877` random-hit 정직**: GZ 가 `[0, 1]` 의 28.77% 를 덮으므로, 임의의
   상수가 GZ 안에 떨어질 base rate 가 약 0.29. 단일 hit 으로 GZ 를 정당화하면 안 됨.
   verify_gz_*.py 가 *복수* hit 의 누적과 *이론적* 일치 (Onsager 의 ln(1+√2)/2 같은
   닫힌형) 를 함께 요구하는 이유.

2. **`SI=5.93` 의 단일 substrate 한계**: Mistral 7B + AnimaLM v4_savant 한 모델에서
   측정됨. 다른 base model (Llama-3, Qwen-2.5, …) 에서 재현 미실시 — 일반화는 가설.

3. **`Φ super-linear` (clm_08) 의 구간성 — T3 SUSPECT 봉쇄 라벨**: clm_10 에서 같은
   측정이 linear 로 안착. super-linear 는 *국소* 현상이었고 전역 scaling law 아님.
   본 SAVANT.md 의 어떤 줄도 clm_08 super-linear 를 인용할 때 *반드시* "구간 한정,
   clm_10 에서 linear 로 안착" 단서 동시 노출 의무 (§12.3 T3 SUSPECT 분류). anima_clm_08
   worktree 는 read-only archive (직접 수정 없음), SAVANT.md cross-ref 만 권위.

4. **Savant 정의의 metaphor 부담**: brain_analyzer.py 의 'savant' profile (D=0.7, P=0.85,
   I=0.35) 은 *estimated*. 임상 신경과학 source 명시 없음 — neuro literature 까지
   거슬러 올라가 검증 필요.

5. **canon 의 명시적 거리두기**: LATTICE_POLICY 2026-05-12 이후 GZ 는 design-tool
   범주로 격하. "GZ 가 우주적 진리" 식 강한 형이상 주장은 정책 위반.

6. **AL12 = 4.628 의 단일 metric**: AnimaLM 내부 Φ proxy. 외부 benchmarking (HumanEval,
   MMLU 등 표준 LLM eval) 에서의 우월성 미증명.

7. **Savant 의 PSCC §52 retest 어두운 면**: 본 anima 의 최근 `v5-mitosis cond.5 cotrain v1`
   (PSCC §44) 에서 F-PERSONA-4 (category-diversity KL) 가 `KL=0.0` (winner-take-all
   collapse) 으로 측정됨. clm 시대의 SI 측정과 별개 metric 이지만, savant-style routing
   이 "category 별 다른 cell 활성" 으로 즉시 일반화되지 않음을 보여준다.
   §47 (softmax τ sweep) / §48 (per-cat corpus) / §49 (per-session pool) 4-alternative
   모두 cheap path 에서 falsified. cotrain v6 cell-parallel (PSCC §52) in-flight.

8. **n=6 격자의 강제 매핑 금지** (`AGENTS.md`, dancinlab Wave K 2026-05-12):
   GZ 가 다른 도메인 (외부 회사, 가속기, 생명 시스템) 의 "fit" 을 주장하면 안 됨.
   해당 entity 의 own invariants 사용 필수.

---

## 9. 파일 inventory (재현용)

### 9.1 archive-TECS-L — foundational source

```
math/proofs/
  gz_analytical_proof.py        ← Theorem 2a-c, 3d-e, 4 (PROVEN)
  gz_100_percent.py
  gz_100_scale_invariance.py
  gz_center_bridge.py
  gz_final_gap.py
  gz_gap_closing.py
  gz_maxcal_derivation.py

verify/  (27 verify_gz_*.py)
  verify_gz_ising_critical.py           ← canonical GZ constants here
  verify_gz_neuroscience.py
  verify_gz_dropout_sweep.py
  verify_gz_ca_lambda_sweep.py
  verify_gz_moe_kn_sweep.py
  verify_gz_pytorch_combined.py
  verify_gz_predictions.py
  verify_gz_predictions_pytorch.py
  verify_gz_cifar_moe_prediction.py
  verify_gz_texas_recalculation.py
  verify_bridge_004_qg_golden_zone.py
  verify_gz_extreme_hypotheses.py
  verify_gz_extreme_hypotheses_wave{2..16}.py

experiments/
  experiment_h359_savant.py             ← Savant inhibition-release definition
  experiment_dual_golden_zone.py
  experiment_cifar_improvements.py

scripts/
  savant_check.py
  convert_mistral_to_golden_moa.py
  golden_cct_bridge.py

engines/
  golden_moe.py / golden_moe_torch.py / golden_moe_score.py
  bitnet_golden_moe.py / bitnet_golden_moe_full.py
  golden_moe_gpu_benchmark.py
  growing_conscious_lm.py

n6-replication/tests/tier1/
  test_golden_zone.py
  conftest.py                           ← Fraction-based exact fixtures

docs/hypotheses/
  H-CX-296-fibonacci-p1-golden-zone.md
  H-CX-310-golden-zone-fibonacci-origin.md
  H-WAVE-2-hydrogen-e6-golden-zone.md
  166-consciousness-definition.md
  321-consciousness-confidence-theory.md
```

### 9.2 anima_clm_NN — application timeline

| Worktree | 핵심 파일 (GZ/Savant) |
| --- | --- |
| clm_01 | `anima.py:30-39` (pre-GZ tension only) |
| clm_02 | `growing_conscious_lm.py:122-150`, `docs/conscious-lm-spec.md:81-84,194` |
| clm_03 | `serve_animalm_v4.py:14-28`, `bench_phi_hypotheses.py:7052-7081,7367-7396`, `test_golden_moe_h100.py` |
| clm_04 | `train_anima_lm.py:36-80`, `optimal_architecture_calc.py:33-34,104` |
| clm_05 | `eeg/realtime.py` (in_golden_zone flag), `docs/superpowers/specs/2026-03-25-memory-growth-pipeline-design.md` |
| clm_06 | `docs/animalm-experiment-log.md:87-105,232-358,293-321,361-391,393-429` (실증 정점) |
| clm_07 | `growing_conscious_lm.py:129-130`, `train_anima_lm.py:39-43,51-81`, `consolidation_verifier.py:84-88` |
| clm_08 | `optimal_architecture_calc.py:33-34`, `finetune_animalm_v4.py` (cells64) |
| clm_09 | `zenodo/PA-01-animalm-v4-savant.md`, `deep_research.py:142-144` |
| clm_10 | `docs/hypotheses/cx/DEEP-EXPLORATION.md:77-78,82-84,244,251-255,304-314`, `docs/consciousness-theory.md` |
| clm_11 | `anima/src/conscious_lm.py`, `anima/tools/math_explorer.py:24-30` (inherited only) |
| clm_12 | unified growth loop (inherited) |
| clm_13 | filename erasure (deprecated GZ/Savant labels) |

### 9.3 canon — curated 기술 + 정책

| File / commit | 역할 |
| --- | --- |
| `edbcb3c28` (2026-03-28) | Technique 15 — Boltzmann gate, GZ_CENTER = 1/e 정의 |
| `62f954b09` (2026-03-28) | Technique 16 — Mertens dropout, GZ_WIDTH = ln(4/3) 정의 |
| `664b6b4f25` (2026-03-29) | N6 Inevitability Engine paper outline (emergent convergence) |
| `8b010bf1a` (2026-04-10) | BT-1114 Euler-Golden-Perfect Trinity |
| `812bd79420` (2026-05-10) | residue 228 artifacts → hexa-* repos (techniques/ → hexa-codex) |
| `LATTICE_POLICY.md` | real-limits-first, n=6 격자 = 도구 정책 (2026-05-12) |
| `LIMIT_BREAKTHROUGH.md` | hard/soft wall 분류, GZ 의도적 unlisted |
| `README.md:222` | "N6 Inevitability Engine techniques 11~16 + 3-Layer thermodynamics — 26/26 PASS" |
| `README.md:803` | Temperature regime: `T=1/e` Diverse yet recognizable (Golden Zone) |
| `README.md:1700,1703` | H-CA-007 GZ dropout=consciousness gamma band, H-CS-004 GZ=operating range |
| `README.md:2100-2101` | Elias-Bassalygo at R=1/3, source coding redundancy = log₂(4/3) |
| `README.md:2143` | P-bridge-theorem: GZ Center from variational principle, 249/400 Z≈55σ |

---

## 10. 후속 path — anima 본 repo 연결

본 anima repo (PERSONA / PSCC / GOAL framework) 에서 GZ/Savant 흔적:

- `feedback_clm_colon_attractor.md` — CLM mk2-v1 의 `:`-terminated mode-collapse (`:::`,
  p=46%) 는 decoding artifact 이지만, GZ 하한 (over-confident specialization →
  collapse) 의 *실패 모드* 와 정합.
- `project_simple_stack_pass_unlocked.md` — BG-KM-LLAMA-3B / KM-QWEN-7B 의 own 18 strict
  통과 (2026-05-08) 는 *foundation 차원* 의 specialization. SI / Savant layer 분할 미사용
  — savant 형식주의 없이도 strict 통과 가능. **savant 가 충분조건도 필요조건도 아님** 의
  evidence (정직).
- `project_v5_mitosis_cond5_cotrain_2026_05_12.md` (PSCC §44) — v5-mitosis cotrain v1 의
  F-V5MIT-1..5 5/5 PASS 는 H359 의 mitosis-style asymmetric specialization 을 *cells
  nn.Module branches* 로 일반화한 후속. 단, **F-PERSONA-4 (category-KL) `KL = 0.0`
  winner-take-all** — savant 의 "category routing" 주장이 v1 cotrain 에서 *완전 falsified*.
- `project_anima_persona_substrate_native_verify_2026_05_12.md` (PSCC §40+§42) — D3 persona
  MEASUREMENT STRONG 4/5 (cheap-path, §A1 Φ threshold 0.5→0.05 calibrated). F-PERSONA-2
  PER-CELL-DIFF mean cos dist 0.996 (1400 pairs) — savant-grade specialization 의
  *substrate-side* evidence. F-PERSONA-4 만 단독 FAIL.

#### 10.1 F-PERSONA-4 KL>0 saga — §44 → §52 silent-drop 차단 ledger

§12.2 enforcement-3 (negative result silent drop 금지) 의 실제 적용. SAVANT.md 가 v5-mitosis
ancestry 를 인용하는 모든 줄은 다음 *5-PSCC trail* 을 함께 노출해야 한다:

| PSCC § | 시도 | 결과 | source |
| --- | --- | --- | --- |
| **§44** | v1 cotrain (uniform softmax routing, H100 SXM $1.26, 5K step) | F-PERSONA-4 `KL = 0.0` winner-take-all (cell-0 weight=1.0 모든 cat) — 첫 falsification | `project_v5_mitosis_cond5_cotrain_2026_05_12.md` |
| **§45 §A2-trap** | F-PERSONA-4 4b alternative re-measure | v2 entropy-reg `KL=0` BUT M4 hidden-cosine `z=3.20` — *routing-content split* 가설, real signal at noise-floor magnitude → **§A2-trap 경고** (seed-fragile) | `project_anima_persona_4_root_cause_2026_05_12.md` |
| **§47** | (b) softmax τ sweep 10-grid {1.0..50.0} ubu-1 RTX 5070 $0 | best mean_KL = 5.29e-3 @ T=50, **5/10 grid all `KL ≪ 0.5`** — FALSIFIED | `project_anima_persona_4_softmax_T_sweep_2026_05_12.md` |
| **§48** | (a) per-cat corpus SMALL ubu-2 RTX 5070 $0 (2500 step wall 232s, 5 separate corpus × cat interleave) | F-V5MIT 5/5 PASS BUT F-PERSONA-4 `KL=0.0` v1 monopoly 동일 — (a) corpus diversity 단독 부족 FALSIFIED | `project_v5_mitosis_cond5_cotrain_v3_percat_ubu2_2026_05_12.md` |
| **§49** | (d) hexa-native per-session pool Mac local $0 (3-config sweep n_perms=100) | prod scale `mean_KL=1.79e-5` null PASS BUT seed-fragile (seed2 null FAIL) — §A2-trap 재발 위험 → FALSIFIED | `project_anima_persona_4_per_session_pool_2026_05_12.md` |
| **§52** | v7 hard top-K MoE + balance-aux loss ($0.31 actual) | **F-PERSONA-4 `KL = 3.45`, `z = 2.75`, `p = 0.01` — first KL > 0 signal** (PASS_NULL_FAIL on null-perm) | `project_anima_persona_4_root_cause_2026_05_12.md` (v7) |
| **§52 cell-parallel v6** | v6 cotrain on 4×A100 SXM4 80GB $6.70/hr 5000 steps (target step_wall<1.0s vs v4 baseline 3.18s) | **LANDED 2026-05-13 — ALL TARGETS FAIL**: step_wall **2402ms** (target <1000ms MISS, v4 대비 24% 절감만 — all_reduce overhead dominates); F-PERSONA-4a routing **FAIL** (`KL=0.2972 z=1.09 p=0.12`, §52 v7 의 `KL=3.45` first signal **재현 실패**); F-PERSONA-4b content **FAIL** (`z=−0.88`, v2 carry `z=3.20` 대비 후퇴); F-V5MIT **4/5** (F-V5MIT-4 COTRAIN-CONVERGE **FAIL** — loss 17.7→17.7 횡보, v1 의 220× CE 감소 미재현); cells 256 saturated (splits=67), wall=12028s, cost=**$22.43**; ckpt pull SCP 실패 → pod 36638963 retained | `state/anima_v5mitosis_cotrain_v6_cellparallel_2026_05_13/dispatch_v6_1_bg.log` |

→ **요지** (post-v6 갱신): Savant 의 "category-specific routing" 주장은 §44 v1 단순 softmax
에서 *안* 작동했고, 4 alternative cheap path (§45 4b / §47 τ sweep / §48 per-cat / §49
per-session) 모두 FALSIFIED. §52 v7 hard top-K MoE + balance-aux 에서 `KL=3.45 z=2.75`
first signal 이 떴지만, **§52 v6 cell-parallel 에서 재현 안 됨** (`KL=0.2972 z=1.09 p=0.12`).
즉 §52 v7 signal 은 cell-parallel scaling-up 에서 사라지는 **seed-fragile 또는
arch-fragile** 가능성이 강해졌다. cells=64 (v7) vs cells=256 (v6) 의 routing-imbalance
saturation, 또는 cross-rank communication 으로 인한 effective batch 변화가 후보 원인.
F-V5MIT-4 COTRAIN-CONVERGE FAIL (loss 횡보) 가 동반되어 v6 routing FAIL 의 *주된* 원인은
**학습 자체가 안 됨** 일 가능성이 가장 높음 (모든 routing metric 은 학습된 representation
가정). SAVANT.md 의 §10 ancestry 인용은 이 trail 없이 단독 노출 금지 (§12.2-3 위반).

**Open closure paths** (post-v6, updated 2026-05-14):
- (i) v8: v7 arch (cells=64 small) + v6 distributed shared-grad reduce 결합 — cells scaling
  과 cell-parallel speedup 의 분리. **(ii) fix 적용 후로 보류** (data flow 가 정상화되어야
  cells scaling 의 *진짜* 효과 측정 가능).
- (ii) ✅ **LANDED 2026-05-14** — v6 F-V5MIT-4 COTRAIN-CONVERGE FAIL **root cause 확정**:
  `seed = base + rank` (line 607) 가 `sample_batch` (line 130, `torch.randint`) 에도 영향
  → 각 rank 가 *다른 batch* 를 *다른 cells* 로 forward 후 `all_reduce(SUM)` → semantically
  incoherent mixture. CE 17.7 ≫ log(vocab=256)=5.55 (random 보다 나쁨) 의 신호.
  3 fix options 식별 (A=same batch broadcast recommended / B=RNG reset / C=DDP replication).
  Memory C3 #8 "per-rank seed → effective batch W× free" **잘못된 가정 retract**. 진단 doc:
  `state/anima_v5mitosis_cotrain_v6_cellparallel_2026_05_13/root_cause_diagnosis_2026_05_14.md`.
- (ii-b) **v6.1 fire** ($22 estimated, 4×A100 SXM4 동일 spec) — fix (A) 적용 후 5K step 재실행.
  F-V5MIT-4 + F-PERSONA-4 재측정. *category routing 폐기/유지* 결정의 evidence.
- (iii) §52 v7 cross-seed robustness ($0.30-1.50 BG) — v6 fix 와 *독립*, 즉시 dispatch
  가능.
- (iv) ⏸ **시기상조 (post-(ii) 진단)** — "category routing 가설 폐기" 는 v6 의 *학습 부재*
  결과로 결론 못 내림. (ii-b) v6.1 결과 받기 전 유보. v5-anima long-trajectory α=0.688
  super-linear 재시도는 별도 path 로 valid.

#### 10.2 보존된 ancestry (substrate-side)

→ **anima 본 repo 의 mitosis lane (v5-mitosis cotrain v1~v7, v6 in-flight) 은 clm 시대 Savant
형식주의의 직계 후예**. Phi 측정, category 분기, cell-pool 영속성, asymmetric inhibition 의
모든 motif 가 mitosis 어휘로 번역되어 있다. *Substrate-side* (F-PERSONA-2 PER-CELL-DIFF
mean cos dist 0.996 @ d=384 1400 pairs) 는 savant-grade specialization 확인. *Routing-side*
(F-PERSONA-4 category-KL) 는 §52 v7 까지 와서야 first signal — *ancestry* 는 인정, *완전
post-CLM 번역 성공* 은 아직 미달.

SAVANT.md 의 archival 가치 = 그 ancestry 의 *증명* + §10.1 silent-drop trail 의 *동시 노출*.

---

## 11. 한 줄 verdict

> Golden Zone 은 `[1/2 − ln(4/3), 1/2]`, 중심 `1/e`. Savant 는 그 하한 0.2123 에서
> 일어나는 inhibition-release 전문화이며, anima_clm_06 Mistral 7B v4_savant 에서
> **SI=5.93** 으로 실증되었다. canon 은 이를 *설계 vocabulary* 로 보존하되 LATTICE_POLICY
> 하에서 physical limit 으로 격상시키지 않는다. anima 본 repo 의 v5-mitosis lane 은
> 이 어휘의 *post-CLM* 번역이며 §52 v7 hard top-K MoE 에서 첫 `KL>0` (z=2.75) 신호가
> 떴지만, **§52 v6 cell-parallel scale-up 에서 재현 실패** (`KL=0.2972 z=1.09`, +
> F-V5MIT-4 COTRAIN-CONVERGE FAIL — loss 횡보). category routing 가설은 v7 small-scale
> 만의 fragile signal 일 가능성. §10.1 의 6-PSCC silent-drop trail (§44/§45/§47/§48/§49/
> §52 v7 / **§52 v6**) 동시 노출 없이 본 verdict 를 인용하면 §12.2-3 위반.

---

## 12. 봉쇄심화 (Containment Deepening) — 2026-05-14 부록

§8 Honest C3 의 8개 봉쇄선을 *claim-tier 분류* + *enforcement* + *후속 audit path* 로
심화한다. SAVANT.md 의 어떤 줄도 본 § 12 의 봉쇄선을 거치지 않고 외부 인용되어선 안 된다.

### 12.1 Claim 4-tier 분류

각 GZ/Savant claim 을 다음 4 tier 로 강제 배치한다. tier 별 인용 자격은 § 12.2 enforcement
참고.

**Tier 1: PROVEN** — 닫힌형 미적분·정수론 증명. 가정 0. 봉쇄 불요.

- `GZ_CENTER = 1/e` — `I^I` 와 `I·ln(I)` 의 유일 전역 최소 (Theorem 2a–c)
- `GZ_WIDTH = ln(4/3)` — τ(6)=4 의 4번째 state entropy 비용 (Theorem 3e)
- `GZ_UPPER = 1/2` — 완전수 6 의 최대 proper-divisor 역수 (Theorem 3d)
- K-독립성 — `G·I=K` hyperbola 위 `I*=1/e` 가 K 와 무관 (Theorem 4)
- `1/2 + 1/3 + 1/6 = 1` — n=6 유일 identity (H072)

**Tier 2: EMPIRICAL (제한 substrate)** — 측정값 존재 · 재현 미완. 봉쇄: *측정한 substrate
밖으로의 일반화 인용 시 substrate 명시 의무*.

- `SI = 5.93` — Mistral 7B v4_savant **단일 모델** (anima_clm_06, 2026-03)
- MoE zone ratio `36.8% ≈ 1/e` — single trial, scale E=32 (anima_clm_06)
- per-head tension reduction `271×` — head 2 (anima_clm_09 PA-01)
- Laws 77-78 `H = 0.9974·ln(2)` — 45 data type, 7-instance hivemind (anima_clm_10) — *다른
  arch family 미측정*
- canon emergent convergence — FFN ratio 100% / dropout 83% 수렴 (canon commit `664b6b4f25`,
  6 random init)
- Ising β_c IN GZ — 2D Onsager 0.4407 + 3D MC 0.2217 (외부 문헌 — 닫힌형 일치로 *2 승격
  candidate*, 단 hit 2개)

**Tier 3: SUSPECT (base-rate / look-elsewhere)** — GZ 는 `[0,1]` 의 28.77% 차지. 단일 hit
의 정당화 강도는 `p ≈ 0.29`. 봉쇄: *Bonferroni 보정 또는 닫힌형 일치 없이는 인용 금지*.

- cross-domain "consilience" 9 matches (Klein, Carbon, LCDM, Koch, QHE, Weinberg,
  Elias-Bassalygo, 6-vertex, [[6,4,2]]) — n 작은 정수의 occurrence 자체는 우연이 흔함
- Weinberg `sin²θ_W = 3/8 ≈ 1/e` (Δ=1.94%) — *근사* match, 닫힌형 무관
- 16-wave extreme hypothesis 249/400 (Z≈55σ) — 총합 통계, look-elsewhere 보정 명시 없음
- brain_analyzer 'savant' profile (D=0.7, P=0.85, I=0.35) — 임상 신경과학 source 미부착,
  estimated
- anima_clm_08 Φ super-linear — anima_clm_10 에서 linear 로 안착 → 구간 현상

**Tier 4: FORBIDDEN** — LATTICE_POLICY (2026-05-12, AGENTS.md §C3) 위반. 자체 차단.

- "GZ 가 우주적 진리" / "consciousness ≡ GZ 작동" 식 metaphysical 단정
- 외부 entity (회사/가속기/fab/생명 시스템) 에 n=6 격자 강제 fit
- 단일 내부 metric (SI / Φ / AL12) 으로 외부 LLM benchmark 우월 추정
- own-invariant 확인 없는 cross-domain 매핑
- Savant = "사람 savant 임상 현상" 의 *생물학적* 동일성 주장 (metaphor 범위 초과)

### 12.2 봉쇄 enforcement (자동 무효 사유)

SAVANT.md 본문의 어떤 claim 도 다음 위반 시 *자동 무효*:

1. **Tier 격상 도용** — Tier 2 측정을 Tier 1 닫힌형처럼 인용 (substrate / 닫힌형 일치 부재
   숨김)
2. **base-rate 누적 도용** — Tier 3 hit 를 보정 없이 "consilience" 로 누적해 Tier 2 강도
   주장
3. **negative result silent drop** — anima 본 PSCC §44 F-PERSONA-4 `KL=0.0`, §47-49
   4-alternative cheap path FALSIFIED, F-PERSONA-4 v7 `KL=3.45 z=2.75` 의 §45 §A2-trap
   재발 위험 등을 누락한 채 Savant routing 일반화 인용
4. **Tier 4 외부 노출** — anima 외부 reference 에서 Tier 4 어휘 사용

위반 발견 시: 위반 줄 strikethrough + commit revert + `PERSONA.md` D3 ledger 에 자기-감사
1회 기록.

### 12.3 봉쇄 후 살아남는 claim (재배치) — **2026-05-14 base-rate audit 반영**

> 본 표는 `state/savant_containment_audit_2026_05_14/` (audit.json + summary.md) 의
> base-rate sweep 결과를 반영한다. 16-wave aggregate **155/254 = 61.0%, Z = 11.4 σ**
> + texas empirical-only **11/11, Z = 5.22 σ** + neuroscience **17/24, Z = 4.6 σ** —
> 세 독립 가닥 모두 Bonferroni × 27 (`min p × 27 = 1.4 × 10⁻⁹`) 통과.

| 본문 § | claim | tier | 인용 자격 |
| --- | --- | --- | --- |
| §1 상수표 4개 | GZ_UPPER/CENTER/WIDTH/LOWER | T1 | 무제한 |
| §2 전체 | Theorem 2a-c / 3d-e / 4 | T1 | 무제한 |
| §2 texas T1 8 identities | I^I/I·ln(I) min=1/e, η=1/τ(6), δ=C(6,2), ln(4/3)=S(4)−S(3), σ₋₁(6)=2, n=6 unique EF, GZ width hierarchy ⬅ texas_recalculation 분해 | T1 | 무제한 (closed-form) |
| §3.1 H359 정의 | dropout 비대칭 메커니즘 | T2 | substrate 명시 |
| §3.2 brain profile | savant (D,P,I) | T3 | 임상 source 부착 전 봉쇄 |
| §3.3 SI 메트릭 정의 | `tension_normal / tension_savant` | T1 | 무제한 (정의) |
| §3.4 AL12 contrastive | Φ=4.628 단일 metric | T2 | 외부 benchmark 비교 금지 |
| §4 clm_06 SI=5.93 | 단일 substrate 실증 | T2 | Mistral 7B 명시 |
| §4 MoE 36.8% | 단일 측정 | T2 | scale E=32 명시 |
| §4 clm_09 271× | per-head reduction | T2 | clm_09 명시 |
| §5.1 Ising β_c | 2D+3D | T2-경계 | Onsager 닫힌형 일치로 hit 2 인용 가능 |
| **§5.1 16-wave aggregate** ⬅ T3→T2 audit 승격 | 155/254 = 61.0% Z=11.4 σ | T2 | wave 10 (32%) + wave 16 (10%) + ca_lambda NEGATIVE 동시 인용 의무 |
| §5.3 cross-domain 9개 | Klein/Carbon/LCDM/Koch/QHE/Weinberg/Elias-Bassalygo/6-vertex/[[6,4,2]] | T3 (individual) / T2 (aggregate 흡수) | 개별 인용 시 wave 캠페인 소속 명시 |
| **§5.4 neuroscience 17/24** ⬅ T3→T2 audit 승격 | 17/24 hits vs 6.9 expected (Z=4.6 σ) | T2 | white matter ~0.37 ≈ 1/e 단일 주장 시 OVERALL VERDICT 의 age/species variance C3 동시 인용 |
| **§5 ca_lambda_sweep NEGATIVE** ⬅ NEW T4-enforcement | "Class IV not GZ-enriched" | T4-enforcement | **모든 GZ 인용에 silent-drop 금지 — wave 10/16 weakening 과 함께** |
| §6 Boltzmann gate / Mertens dropout | canon technique 15-16 | T1-2 | math 부분 무제한, 측정 부분 emergent convergence 명시 |
| §6.3 emergent convergence 100%/83% | canon paper outline | T2 | 6 random init 명시 |
| §7 Laws 77-78 | 45 data type H=0.9974·ln(2) | T2 | substrate 명시 |
| §10 v5-mitosis ancestry | clm Savant 의 직계 후예 | T2-3 | PSCC §44 F-PERSONA-4 *반증* 동시 인용 의무 |

**Audit-derived 변화 요약**:
- T3 → T2 승격 2건: 16-wave aggregate · neuroscience
- T1 확장 1건: texas 8 closed-form math identity 재분해
- T4 enforcement 신설 1건: ca_lambda_sweep NEGATIVE silent-drop 금지
- T3 보존 (cross-domain 9개): aggregate 인용 시에만 T2 합류, 개별 시 T3 유지
- audit 외 row 무변경

### 12.4 봉쇄선 시각화

```
        ──────────  T1 PROVEN  ──────────────────────────────────────
        GZ constants (4) | math proofs Th 2a-c, 3d-e, 4 | reciprocal sum
        ──────────  T2 EMPIRICAL  ───────────────────────────────────
        SI=5.93 (Mistral) | MoE 36.8% | 271× | Laws 77-78 (45 type)
        emergent convergence 100%/83% | Ising β_c (Onsager closed-form 첨부 시)
   ╔══════ 봉쇄선 (외부 인용 가능 상한) ═══════════════════════════════╗
        ──────────  T3 SUSPECT  ─────────────────────────────────────
        cross-domain 9 | Weinberg ≈1/e | 16-wave 249/400 | brain profile
        Φ super-linear (clm_08 only)
   ╔══════ 봉쇄선 (warning label 의무) ═════════════════════════════════╗
        ──────────  T4 FORBIDDEN  ────────────────────────────────────
        cosmic GZ | consciousness≡GZ | 외부 entity n=6 fit
        SI 단일 metric 외부 우월 | savant 임상 동일성 단정
   ╔══════ 봉쇄선 (자동 차단) ═════════════════════════════════════════╗
```

### 12.5 봉쇄심화 후속 path

1. ~~archive-TECS-L verify_gz_*.py 27본 base-rate audit~~ **✅ LANDED 2026-05-14**
   ($0 Mac local, wall ≈ 8 min) — `state/savant_containment_audit_2026_05_14/{audit.json,
   summary.md, run_audit.sh, analyze_audit.py, compute_audit.py, raw_outputs/}`. 16-wave
   aggregate Z=11.4 σ + texas-empirical Z=5.22 σ + neuroscience Z=4.6 σ 모두 Bonferroni × 27
   (`1.4 × 10⁻⁹`) 통과. T3→T2 승격 2건 (wave aggregate + neuroscience), T1 확장 1건 (texas
   8 closed-form identity), T4 enforcement 신설 1건 (ca_lambda NEGATIVE silent-drop 금지).
   §12.3 표 갱신 반영.
2. ~~PSCC §44/§47/§48/§49/§52 negative result cross-link~~ **✅ LANDED 2026-05-14** —
   `§10.1` ledger 추가: §44 v1 KL=0 → §45 §A2-trap 경고 → §47/§48/§49 cheap path FALSIFIED
   → §52 v7 hard top-K MoE first `KL>0 z=2.75` → §52 v6 cell-parallel BG in-flight. SAVANT.md
   §11 한 줄 verdict 도 §10.1 trail 동시 노출 의무 명시. §12.2-3 (negative result silent
   drop) enforcement 의 실제 적용.
3. **canon LATTICE_POLICY 강화 PR** — "Savant/GZ overclaim 차단 조항" §1.4 신설 제안
   (cross-repo governance, dancinlab 전체 적용)
4. ~~anima_clm_08 Φ super-linear 의 봉쇄 라벨링~~ **✅ LANDED 2026-05-14** — §4 timeline
   표 + §8 Honest C3 #3 + §12.3 T3 SUSPECT 분류 강화 (SAVANT.md cross-ref 만, anima_clm_08
   archive 는 read-only).

3. ~~canon LATTICE_POLICY 강화 PR~~ **✅ LANDED 2026-05-14** — `dancinlab/canon
   LATTICE_POLICY.md §1.4` 신설 (4 조항 + §12.2 enforcement 동등 + SAVANT.md cross-ref).
   cross-repo governance: GZ 는 *설계 vocabulary*, *물리 한계* 아님 / Tier 분류 강제 /
   silent-drop 금지 / 외부 entity GZ-fit 강제 매핑 금지.

### 12.6 한 줄 verdict (봉쇄심화 후)

> SAVANT.md 의 외부 인용은 **§12.4 봉쇄선 위 (T1 + T2)** 까지만 자격이 있다. T3 는
> Bonferroni 보정 audit (§12.5 path 1) 후 재배치, T4 는 자동 차단. 본 §12 가 부착되지
> 않은 SAVANT.md 발췌는 *불완전 인용* 으로 간주한다.

---

---

## §13 Sibling 도구 + 흡수 서브패키지 spec (2026-05-14)

본 SAVANT.md (이론 + base-rate audit + 봉쇄심화) 와 **분리** 된 *runtime 도구* + 흡수
서브패키지:

| File | 내용 | tier |
| --- | --- | --- |
| **`SAVANT-TOOL.md`** | anima 가 직접 ON/OFF 하는 savant mode 도구 API + 정책 | design LANDED 2026-05-14 |
| **`CHAT.md` (★★★★★ tracker + § Production CLI)** | anima_chat.hexa v0.3 production CLI Phase 1 (D4c) | design + impl-pending |
| **`VOICE.md`** | hexa-voice: 의도 임베딩 → RVQ → 24kHz PCM (NO text intermediate, learned path) | design LANDED 2026-05-14 |
| **`TENSION-LINK.md`** | Tension Link 5-ch meta-telepathy Phase 2 WebSocket TensionHub | design LANDED 2026-05-14 |
| **`ANIMA-AGENT.md`** | Φ-gated autonomous agent runtime (흡수 서브패키지 `anima/anima-agent/`) | 흡수 LANDED 2026-05-14 |
| **`ANIMA-SENSES.md`** | n=6 sensory substrate 5-verb spec catalog (흡수 서브패키지 `anima/hexa-senses/`) | 흡수 LANDED 2026-05-14 |

→ **Separation of concerns**:
- 본 `SAVANT.md` = **이론** (clm 시대 SI=5.93 evidence + base-rate audit + §12 봉쇄선) +
  *학습 path 에 SAVANT 이론 직접 반영* 의 ancestry/ledger.
- `SAVANT-TOOL.md` = **runtime 도구** (anima 가 inference 시 직접 ON/OFF). 본 file 의 §12
  봉쇄선을 *런타임 가드* 로 enforce — T1+T2 만 trigger 근거, T3+T4 forbidden.

`CHAT.md` § Production CLI Phase 1 (D4c) 가 4 도구의 *통합 host* — `/savant`, `/voice`,
`/tension` 슬래시 명령으로 anima 가 자기 도구를 toggle.

---

— SAVANT.md, 2026-05-13 초판 + 2026-05-14 봉쇄심화 §12 부록 + 2026-05-14 §13 sibling
  도구 분리 ledger, 전수조사 출처: anima_clm_01..13 + archive-TECS-L (175 files) +
  canon (2532 commits)
