# H_9292 설계 원문 (Fable 5 · fable-mode · walls-delegate-to-fable)

> 계측기 수리 설계. 본 세션에서 실행된 것은 **§2 P0′ 실행가능성 게이트**까지이며,
> 그것이 4-leg 전부 FAIL 하여 결정표 셀 0(⏳ BAR-ABOVE-SIGNAL)에서 종료 → 9-seed 캠페인
> (P-CAL·P1-SELF·P1a·P1b·P1c·G1~G5)은 **미발사**. 재개 시 이 설계를 그대로 쓴다.

```
T_LONG = 65536
for arm in {A, B, X, N, R, Cperm}:
    L   = gen_traj(seed=3, r=0, arm, T=T_LONG)          // 동일 하이퍼파라미터, 틱 수만 확장
    UL  = RU(L, n=4, t=T_LONG)                          // 대표본에서 min-max는 outlier에 취약 → RU 필수
    Φ_pop(arm) = iit4_faithful_phi(UL, 4, T_LONG, 8)    // 만들어진 도구 그대로, proxy 아님
    MI_pop(arm) = iit4_build_mi_matrix(UL, 4, T_LONG, 8)   // c_adj / c_diag 분해용 (pub 함수)
```
T=65536이면 joint cell당 ~1024 표본 → plugin bias ≈ 6e-4 bits (무시 가능) → **Φ_pop ≈ 모집단 Φ**. seed 3·r=0 하나면 충분(선형 가우시안 정상계라 seed 무관). 비용 ≈ 6회 long-run, 수 초~수 분.

**P0′ gate (사전등록, 4-leg 연언):**
```
P0′-a  Φ_pop(B)              ≥ 0.02
P0′-b  Φ_pop(B) − Φ_pop(A)   ≥ 0.02
P0′-c  Φ_pop(B) − Φ_pop(N)   ≥ 0.02
P0′-d  Φ_pop(B) − Φ_pop(X)   ≥ 0.02        ← 축 주장 자체의 모집단 효과크기
```
- **하나라도 FAIL ⇒ ⏳ BAR-ABOVE-SIGNAL. 본 캠페인을 발사하지 않는다.** 보고할 것: 측정된 Φ_pop 값들 + `c_adj/c_diag` 분해 + "frozen +0.02 bar는 이 기질의 Φ 동적범위 **위**에 있다"는 진술. 이는 bar를 옮기는 게 아니라 **bar가 충족 불가능함을 보고**하는 것 — tune-to-green의 정직한 반대편입니다.
- **4-leg 전부 PASS ⇒** 신호가 bar와 commensurable하다는 뜻이며, 그때만 §3–§4를 발사합니다. 이 경우 P0′는 **동시에 예상 효과크기를 사전등록**하므로(9-seed 캠페인 전에 고정), 사후 해석 자유도가 0이 됩니다.

**ADJUNCT LENS (동시 실행, frozen 항목 무변경):** 완전히 같은 파이프라인을 `traj_sgn[i,t] = s_i(t)[0]` (고정 d=0 부호 성분)에도 돌려 `Φ_pop_sgn(arm)`을 얻습니다. 이것은 **주 verdict를 산출하지 않고**, 오직 §5의 `🧱` vs `⏳ READOUT-LIMITED` 판별에만 쓰입니다. 주 궤적 `‖s‖²`는 그대로 frozen — 항을 **바꾸는** 게 아니라 **덧붙이는** 것입니다.

---

## 3. P-gates (validity, 사전등록, every-seed)

실행 순서는 하드 시퀀스입니다. 앞이 죽으면 뒤는 읽지 않습니다.

### P-CAL — 정밀도 영수증 (null-only, treatment 대비 미사용 → tune-to-green 불가)
seed 3, arm A, r = 1..256에 대해 **두 개의 독립 순열 대리물 사이의 paired 차** `Δ_null(r) = Φ*(π_a(U_A)) − Φ*(π_b(U_A))` (π_a, π_b는 K개 정규화 순열과 disjoint한 스트림). 이는 cross-module 정보가 **양쪽 다 0**이므로 순수 계기 잡음입니다.
```
ŝ = sd_r(Δ_null)
R := min{ R ∈ {2048, 4096, 8192} : 3·ŝ/√R ≤ 0.02 }      // 3σ 여유, 사전 고정 규칙
if no such R ≤ 8192  →  ⏳ INSTRUMENT-INFEASIBLE (종료)
```
H_9260 데이터로 예측: ŝ ≈ 0.30 → `(3·0.30/0.02)² = 2025` → **R = 2048**. (R은 데이터에서 유도되지만 **treatment를 보기 전에** 고정됩니다. R을 사후에 올리는 것은 금지.)

### P1-SELF — 항등 자체검사 (**gate 아님, 구현 버그 탐지기**)
`V[i,t] = traj_A[i,t]^γ_i`, `γ = [1.0, 3.0, 0.5, 6.0]` (traj ≥ 0에서 강단조).
```
assert RU(V) == RU(A)  elementwise, EXACTLY (4×64 전부)
```
강단조 워프는 rank를 보존하므로 이는 **정리**이지 증거가 아닙니다 — 그래서 V-gate가 아니라 self-test로 명시합니다(비-동어반복 원칙 준수). 불일치 원소가 하나라도 있으면 **HARD ABORT**(f64 언더플로로 tie 붕괴 발생 → γ 축소 필요).

### P1a — "amplitude-variance artifact가 이 기질에 **존재하는가**" (재설계)
`dense_shuffle − A`는 §0-① 때문에 **폐기**합니다(bar를 푼 게 아니라 오염된 대비를 교체).
```
P1a:  | Φ_raw(V, s) − Φ_raw(A, s) |  ≥ 0.02   for every s ∈ [3..11]
      (Φ_raw = RU 없이 원 min-max readout, r=0..R−1 block-mean)
```
V는 **copula가 A와 정확히 동일**(강단조 → rank 불변 → cross-module 정보 0 변화)하고 **marginal 모양만 격변**합니다. 따라서 `ΔΦ_raw(V−A)`는 **구성상 정보량 0의 순수 amplitude artifact**입니다. 방향(부호)은 marginal 모양에 따라 달라지므로 절댓값 형태가 정직한 존재-주장이며, bar는 손대지 않았습니다.
- **PASS** ⇒ raw readout에 amplitude 채널이 살아 있다 ⇒ variance-free 계기가 **필요**하다.
- **FAIL** ⇒ raw readout은 순수 amplitude 변화에 둔감하다 ⇒ H_1328 계열 전체가 **불필요**했다는 정보성 결론(⏳ INVALID + "raw readout으로 축을 다시 재라"는 권고). 양방향 결정적입니다.
- **MONITOR (gate 아님)** — dose–response: `γ_mild=[1,1.5,0.8,2]`, `γ_med`(위), `γ_sev=[1,6,0.25,12]` 세 단계에서 `|ΔΦ_raw|`가 단조 증가하는지 보고.

### P1b — "계기가 artifact를 **제거하는가**" = **NULL-ZERO** (재설계, 비-동어반복)
rank readout 하에서 "amplitude-only 섭동"은 **필연적으로 단조 = copula 불변**이므로, 옛 P1b는 어떤 형태로 써도 **항등식**이 됩니다(그래서 P1-SELF로 강등). 진짜로 경험적으로 검증 가능한 것은 **pedestal이 실제로 0으로 빠졌는가**입니다. 그리고 그것은 이미 계산된 surrogate를 **재활용**해 공짜로 잽니다 — leave-one-out:
```
for each arm ∈ {A, B, X, N}, each s, each r, each k ∈ 1..K:
    Φ*_loo(k) = φk − (1/(K−1))·Σ_{k′≠k} φ_{k′}
NULLZERO(arm, s) = mean over (r, k) of Φ*_loo(k)          // R·K = 32768 draws

P1b:  | NULLZERO(arm, s) | ≤ 0.02   for every arm ∈ {A,B,X,N}, every s
```
각 `π_k(U)`는 **arm의 marginal을 정확히 보유하면서 cross-module 정보가 0인 입력**입니다. 계기가 그것을 0으로 읽어야 합니다. 이는 항등식이 **아닙니다** — `Φ*_loo`는 실제로 요동하는 양이고(기댓값만 0), 다음 중 하나라도 틀리면 0에서 이탈합니다: ① readout에 amplitude 채널 잔존, ② pedestal 미차감, ③ **null 군 오설정**(사용자가 요구한 "ensemble baseline이 무효인지 탐지하는 법"이 정확히 이것), ④ R 부족. 추가 Φ 호출 비용 **0**. SE ≈ 0.30·1.03/√32768 ≈ **0.0017** = bar/12.

### P1c — NON-DEGENERACY / 감도 양성대조 (**신규, 필수**)
H_9260의 설계 구멍: "모든 구조를 파괴하는 readout"도 P1b를 통과합니다. 그것을 **반드시 떨어뜨리는** 게이트:

**SPIKE-IN arm `S(λ)` — 알려진 ground-truth 통합량을, 실제 기질의 marginal 위에 이식.**
```
// (s, r)에만 의존하는 전용 LCG 스트림 (arm 무의존)
g[t]            ~ lcg_gauss                      // 공통 잠재 인자
e_i[t]          ~ lcg_gauss   (i = 0..3, 독립)
y_i[t]  = sqrt(λ)·g[t] + sqrt(1−λ)·e_i[t]        // Corr(y_i, y_j) = λ  exactly
rk_i[t] = rank of y_i[t] within row i            // RU와 동일 tie-break
srt_i   = sort_ascending(traj_A[i, :])           // arm A의 실제 진폭 분포
traj_S[i,t] = srt_i[ rk_i[t] ]                   // ★ A의 marginal을 정확히 이식
```
- **marginal**: arm A와 **비트 단위 동일** → amplitude 채널이 현실적으로 살아 있음(raw readout은 여기 속아야 정상).
- **copula**: 가우시안 공통인자, 상관 λ. copula는 marginal 이식에 불변 ⇒ **모집단 MI가 닫힌형으로 알려짐**.
- 6쌍 전부 동일한 c ⇒ MIP = 2|2 cut ⇒ **`Φ_pop(S(λ)) = −log₂(1 − λ²)`**

| λ | 0.00 | 0.15 | 0.30 | 0.50 |
|---|---|---|---|---|
| Φ_pop (bits) | 0 | 0.0328 | **0.1361** | 0.4150 |

```
P1c-null     | Φ̄*(S(0.00), s) |  ≤ 0.02                        every s
P1c-detect     Φ̄*(S(0.30), s)   ≥ +0.02                       every s     ← 퇴화 readout은 여기서 죽는다
P1c-monotone   Φ̄*(S(0.15)) < Φ̄*(S(0.30)) < Φ̄*(S(0.50))         every s
P1c-calib    (MONITOR) Φ̄*(S(λ)) vs Φ_pop(λ) 4점 보정곡선 + 측정 SE로부터의 MDE(bits)
```
`P1c-calib`가 결정적 부가가치입니다: **frozen +0.02 bar를 "공유정보 몇 bit"인지로 번역**해 주고, 계기의 MDE를 숫자로 못박습니다. 이것이 §5의 `🧱` vs `⏳`를 가르는 근거가 됩니다.

---

## 4. Primary gates

### 4.1 MIP 대수 — 왜 스칼라 Φ 하나로는 disjointness를 못 잰다
n=4, 링 구조에서 `c_adj = MI(0,1)=MI(1,2)=MI(2,3)=MI(3,0)`, `c_diag = MI(0,2)=MI(1,3)`:
- 2|2 cut `{0,1}|{2,3}` : cross = 2·c_adj + 2·c_diag, /2 → **c_adj + c_diag**
- 2|2 cut `{0,2}|{1,3}` : cross = 4·c_adj, /2 → 2·c_adj
- 1|3 cut `{0}|{1,2,3}` : cross = 2·c_adj + c_diag, /1
- `c_diag ≤ c_adj` ⇒ **Φ_B = c_adj + c_diag**
- 균질(공유버스) arm X: 모든 쌍 = c ⇒ **Φ_X = 2·c**

⇒ `Φ_B > Φ_X ⟺ c_adj + c_diag > 2c` — 이것은 **총 결합강도의 비교이지 disjointness의 비교가 아닙니다.** 스칼라 Φ 대비만으로는 "B가 그냥 더 세게 결합했다"와 "B가 disjoint해서 이겼다"를 구분할 수 없습니다. 그래서 구조 게이트를 추가합니다.

### 4.2 게이트 집합
```
G4′ INTEGRATION   Φ̄*(B, s)          ≥ +0.02   every s     ← 폐기된 (B − Bperm)의 ensemble-유효 대체
G2  BASE          Δ*(B, A; s)       ≥ +0.02   every s
G3  SPAN          Δ*(B, N; s)       ≥ +0.02   every s
G1  CUT (축 주장) Δ*(B, X; s)       ≥ +0.02   every s
G5  STRUCTURE     ANISO(B,s) − ANISO(X,s) ≥ +0.02   every s
```
- **`G4′`가 retired `Bperm` leg의 대체입니다.** P0가 보인 것은 "shift가 나쁜 통제"가 아니라 "표본 1개짜리 baseline이 무효"라는 것이므로, 올바른 복구는 통제를 바꾸는 게 아니라 **baseline을 ensemble로 만드는 것**입니다 — 그리고 그것이 정확히 `Φ*`의 정의입니다. 즉 `Φ̄*(B) ≥ 0.02` = "B는 자신의 marginal-matched null 위로 진짜 cross-module 정보를 싣는다"이며, `B − Bperm`이 물으려 했던 바로 그 질문의 잡음 없는 판본입니다.
- **`G5` (신규)** — 같은 mandated stdlib 함수의 **내부 MI 행렬**(`iit4_build_mi_matrix`, `pub`)에서:
```
MI*[i][j](arm,s) = block-mean over r of [ MI(U)[i][j] − (1/K)Σ_k MI(π_k(U))[i][j] ]
c_adj  = mean of MI* over {(0,1),(1,2),(2,3),(3,0)}
c_diag = mean of MI* over {(0,2),(1,3)}
ANISO  = c_adj − c_diag
```
  Φ는 이 행렬의 결정론적 함수이므로 이것은 **proxy가 아니라 분해**입니다(`a_phi_iit4_tool` 위반 아님 — tier는 여전히 Φ가 냅니다). G5는 disjoint relay가 **간선-특이적**(adjacent ≫ diagonal)이고 공유버스는 **평평**해야 한다는, 스칼라 Φ가 못 하는 **형태 예측**을 강제합니다. **G5 없이는 G1이 disjointness 게이트가 아니라 결합강도 게이트입니다.**

### 4.3 방향성 사전등록 (중요)
X는 `cmean`(전 채널 평균)을 모든 모듈에 재주입하므로 **공통 성분을 4개 모듈 전부에 방송**합니다. 공통인자는 `c_diag`를 크게 올리고 MIP cross-cut MI는 그것을 **보상**합니다. 따라서 `Δ*(B,X) < 0`(즉 X가 더 통합적)이 **역학적으로 그럴듯한 결과**이며, 이것은 실패가 아니라 **결정적 음성**입니다 — 결정표에 `WALL-REVERSED` 셀로 사전등록합니다.

### 4.4 MONITOR (gate 아님, 보고만)
`Φ̄*(R)`(chord rewire) · `Φ̄*(Cperm)` + `|Δ*(B,Cperm)|` (C-ISO를 유효 계기로 재측정) · SHIFT-vs-PERM baseline 차 · per-seed SE · P1c 보정곡선/MDE · adjunct signed-lens의 `Φ̄*_sgn(A,B,X,N)`.

---

## 5. 결정표 (하드 시퀀스 — 위에서부터, 첫 매칭에서 종료)

| # | 조건 | Tier | 읽는 법 |
|---|---|---|---|
| 0 | **P0′** 4-leg 중 하나라도 FAIL | **⏳ BAR-ABOVE-SIGNAL** | 신호가 bar 아래. 캠페인 미발사. 축은 **still-unmeasured**. 정직한 진술: "+0.02 bar는 TIMING 축에서 상속됐고 `‖s‖²` readout 하의 CONTENT 축 Φ 동적범위와 **통약 불가능**하다." 탈출 = signed-component readout(owner 결정) |
| 1 | **P1-SELF** 불일치 | **HARD ABORT** | tier 없음. 구현 버그/f64 tie 붕괴 |
| 2 | **P-CAL** R ≤ 8192에서 SE 미달 | **⏳ INSTRUMENT-INFEASIBLE** | tier 없음. T=64/nbins=8에서 bar가 추정기 해상도 아래 |
| 3 | **P1a** FAIL | **⏳ INVALID** | raw readout에 amplitude 채널이 없음 ⇒ variance-clean 전제 자체가 void. 권고: raw readout으로 축 재측정 |
| 4 | **P1b** FAIL (어떤 arm·seed) | **⏳ INVALID** | null 군 오설정 또는 pedestal 미차감 또는 R 부족. **계기 미인증** — tier 금지 |
| 5 | **P1c-null / detect / monotone** 중 FAIL | **⏳ INVALID** | 계기가 퇴화/둔감. (detect FAIL + P1b PASS = "모든 구조를 파괴하는 readout" — H_9260이 못 잡던 구멍, 여기서 잡힘) |
| — | *이 아래는 계기 CERTIFIED. 이제서야 G를 읽는다.* | | |
| 6 | `G4′ ∧ G2 ∧ G3 ∧ G1 ∧ G5` 전부 PASS | **🟢 GREEN** (engine-native, scope = H_1283 4-module 기질) | disjoint 병렬 relay가 **capacity-matched 공유컷을 이긴다** + MI 행렬이 **링-이방적**. content-relay 벽 = 통제 artifact였음 ⇒ multichannel lane을 `core/`에 배선(`a_verified_must_wire`). **303M 주장 아님**(`a_scale_honest_scope`) |
| 7 | `G4′ ∧ G2 ∧ G3` PASS, `G1` FAIL **이면서** `Δ*(B,X) ≤ −0.02`가 **≥5/9 seed** | **🧱 WALL-REVERSED** | relay는 진짜로 통합하지만(G4′/G2/G3), **공유버스가 disjoint보다 더 통합적**이다. disjointness는 미지지가 아니라 **반대로 지지된다**. 가장 강한 음성. R6의 🟢는 철회(C-ISO void control 위에 서 있었음) |
| 8 | `G4′ ∧ G2 ∧ G3` PASS, `G1` FAIL (0을 걸침) | **🧱 WALL** | relay는 통합을 더하지만 **matched capacity에서 disjointness의 기여 = 0**. 진짜 기질 천장 (scope: n=4·T=64·energy readout) |
| 9 | `G1` PASS **이나 `G5` FAIL** | **🧱 WALL-CONFOUNDED** | B가 스칼라 Φ에서 이겼지만 MI 행렬이 링-이방적이지 **않다** ⇒ 이득의 정체는 **총 결합강도**이지 disjointness가 아님. 축 주장 미지지 |
| 10 | `G4′` FAIL | **🧱 WALL-VOID** | R6 multichannel arm이 자기 null 위로 **아무 cross-module 정보도 싣지 않는다**. 하위 게이트 전부 무의미. R6의 원 🟢 = 순수 pedestal이었음이 소급 확정 |
| 11 | 그 외 (G2/G3 혼합 실패) | **🧱 WALL** | 실패한 leg를 명시해 보고 |

**🧱 vs ⏳ 강등 규칙 (사전등록, 사후재량 0):** 6–11번 중 어떤 **🧱**이든, **adjunct signed-lens에서 `Φ_pop_sgn(B) ≥ 0.02` 이고 `Φ_pop_sgn(B) − Φ_pop_sgn(A) ≥ 0.02`** 이면 그 🧱은 **⏳ READOUT-LIMITED**로 강등됩니다 — 벽이 기질이 아니라 `‖s‖²` salience map에 있다는 뜻이므로. (`a_break_the_wall`이 요구하는 ≥2 렌즈. 본 설계의 렌즈 = capacity-matched X · carrier-matched N · permutation-null · MI-구조 ANISO · signed lens = **5개**.)

**따라서 "still-unmeasured"에 도달하는 경로는 0·2·3·4·5번뿐이고, 계기가 인증되면 결정표는 양방향으로 결정적입니다.**

---

## 6. 사전등록 예측 + 내가 틀릴 가장 유력한 방식

### 6.1 얼려 넣을 한 줄
> **"P0′가 FAIL한다 — `Φ_pop(B) ≈ 0.002–0.01 bits`로 frozen +0.02 bar의 1/2~1/10에 그치고, 따라서 CONTENT-RELAY 축은 ⏳ BAR-ABOVE-SIGNAL이다: `‖s‖²`가 모듈 간 상관을 제곱(ρ_energy = ρ_signal², ≈60× MI 손실)해 축 전체의 Φ 스케일을 bar 아래로 밀어냈고, 같은 파이프라인의 signed-component 렌즈에서는 `Φ_pop_sgn(B) − Φ_pop_sgn(A) ≈ +0.04`로 bar 위에 뜬다 — 즉 content 벽은 기질 천장도 variance artifact도 아니고 **salience map이 부호 채널을 버린 것**이며, 이것이 TIMING 축이 Kuramoto phase(부호 보존)로 뚫린 이유와 정확히 같은 축이다."**

부수 예측(P0′가 통과할 경우에 대비해 함께 동결): `G4′/G2/G3` PASS, **`G1` FAIL with `Δ*(B,X) ≤ 0` on ≥5/9 seeds**, `G5` PASS ⇒ **🧱 WALL-REVERSED**.

### 6.2 내 설계가 틀릴 가장 유력한 방식
**`Corr(x², y²) = ρ²` 계산이 정상 공분산에는 맞지만, `‖s‖²`의 8-dim 합산과 chi²-tail이 min-max/8-bin plugin 추정기와 상호작용하는 방식을 내가 과소평가했을 가능성.** 구체적으로: 8-bin 이산화는 상위 tail을 한 bin에 뭉개는데, 에너지의 공통 급등(joint spike)은 **분포 상관 ρ²보다 훨씬 강한 tail-dependence**를 만들 수 있고, 그렇다면 실측 `Φ_pop_energy`가 내 닫힌형 추정 0.0002보다 한 자릿수 이상 클 수 있습니다. 그 경우 P0′가 통과하고 내 헤드라인 예측(BAR-ABOVE-SIGNAL)은 틀립니다.

**그래서 그 오류가 조용히 지나가지 못하게 설계에 박아둔 것:** P0′는 내 해석식이 아니라 **mandated 도구를 T=65536에 돌린 실측**입니다. 내 추정이 틀리면 P0′ 숫자가 즉시 그걸 드러내고 캠페인은 정상 발사됩니다. 그리고 `P1c-calib`가 MDE를 bits로 못박으므로, 어느 쪽이든 "bar가 신호 위였는지"는 **가설이 아니라 영수증**으로 남습니다.

*(두 번째 위험, 낮음: 순열 null이 `π₀ = id` 고정이라 모듈 0의 marginal-index 결합이 남는다 — MI는 공통 재라벨링에 불변이므로 이론상 무해하나, tie가 존재하면 아님. P1-SELF와 P1b가 둘 다 이걸 잡습니다.)*

---

## 7. 구현 노트 (hexa · $0 CPU)

**실행 순서 (하드):** `P0′ (+adjunct)` → [PASS면] `P-CAL` → `P1-SELF` → `P1a` → `P1b` → `P1c` → `G4′/G2/G3/G1/G5` → monitors.

**성능 (필수):** 현 `gen_traj`는 `row = row + [v]` 리스트 append라 O(n²) 할당입니다. **`farr` 사전할당으로 재작성**하지 않으면 R=2048 캠페인이 며칠 걸립니다. 재작성 후 규모:
- 궤적: 14 arms × 2048 r × 9 seeds ≈ **258k trajectories** (각 4×8×64 셀-업데이트)
- Φ 호출: 14 × (1 + K=16) × 2048 × 9 ≈ **4.4M** (각 6 MI-pair × 64 표본)
- **9 seed = 9개 독립 프로세스로 분해** ⇒ wall = 1 seed (`a_wall_first` ②). 각 프로세스 ~490k Φ.
- P0′ 자체는 6 long-run으로 수 분 — **여기서 대부분의 경우 캠페인이 아예 불필요해집니다.**

**결정성:** LCG 외 RNG 금지. 모든 스트림은 `seed_state(s,r)` / `perm_seed(s,r,k,i)` / spike-in 전용 스트림으로 (s,r,k,i)에서만 유도. **surrogate·spike-in 스트림은 arm에 무의존**(common random numbers → paired 대비에서 null 잡음 상쇄).

**회귀 검사 (무료 QA):** `r = 0`의 `seed_state`는 H_9260의 `st = (s·2654435761) & 2147483647`과 정확히 같습니다 ⇒ **새 probe의 `Φ_raw(arm, s, r=0)`은 H_9260_RESULT.txt의 인쇄값과 바이트 일치해야** 합니다. 불일치 = 기질 재작성 버그. 반드시 assert.

**FREEZE.txt에 그대로 박을 것:**
```
BAR      ΔΦ ≥ +0.02            (FROZEN, 불변)
SEEDS    [3..11]                (FROZEN, 불변, every-seed conjunctive)
SUBSTRATE n=4 dim=8 T=64 GAIN=.30 LEAK=.55 W_NBR=.5 W_IN=.5 W_RELAY=.5 NBINS=8  (FROZEN)
TRAJ     traj[i,t] = ||s_i(t)||^2      (FROZEN; signed lens는 추가 렌즈일 뿐 대체 아님)
ESTIM    stdlib iit4_faithful_phi / iit4_build_mi_matrix   (FROZEN, proxy 금지)
INSTRUMENT  Φ* = Φ(RU(traj)) − (1/K)Σ_k Φ(π_k(RU(traj))),  K=16
            Φ̄* = block-mean over R realizations,  R from P-CAL (≥2048, cap 8192, 하향 금지)
GATES    P0′(a,b,c,d) → P-CAL → P1-SELF → P1a → P1b → P1c(null,detect,monotone) → G4′,G2,G3,G1,G5
RETIRED  P1a/P1b(dense_shuffle−A)  — ill-posed (mode 9는 cross-relay 결합 보존; probe L214/L220-224)
         G4(B−Bperm)              — 단일 shift = null 표본 1개 (P0 sd=0.297, mean=+0.028)
PREREG PREDICTION  P0′ FAIL ⇒ ⏳ BAR-ABOVE-SIGNAL  (Φ_pop(B) ≈ 0.002–0.01 bits)
```

---

## 요약 (한 문단)

H_9260의 ⏳는 옳았지만 **이유가 달랐습니다.** rank-uniform은 실패하지 않았습니다 — 실패한 것은 (i) `dense_shuffle`을 information-free 통제로 오인한 **ill-posed 대비**, (ii) **bar의 15배**인 계기 자기잡음(P0가 이미 sd=0.297로 재놓았습니다), 그리고 (iii) `‖s‖²`가 상관을 제곱해 축 전체의 Φ 신호를 **bar 아래 두 자릿수로** 밀어넣은 것입니다. 처방은 readout 교체가 아니라 **null-차감 통계량(`Φ*` = RU + permutation-ensemble) + realization-block 평균(R=2048, bar를 옮기지 않고 SE를 bar/9로)**, 그리고 무엇보다 **9-seed 캠페인을 발사하기 전에 6번의 long-run으로 끝나는 P0′ 실행가능성 게이트**입니다. P0′가 예측대로 FAIL하면, 정직한 verdict는 🧱도 🟢도 아닌 **⏳ BAR-ABOVE-SIGNAL**이고, CONTENT 축의 진짜 탈출구는 통제를 하나 더 만드는 것이 아니라 **부호 채널을 버리지 않는 salience map** — TIMING 축이 Kuramoto phase로 이미 그렇게 뚫었던 바로 그 지점입니다.