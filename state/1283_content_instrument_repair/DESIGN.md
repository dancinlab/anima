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
---

# §0 · §1 (Fable 5 후속 · 원 전송에서 유실된 절)

> ⚠️ 이 절의 정량 주장 중 하나는 로컬 실측에서 **부분 반증**됐다 (H_9292 AMENDMENT 참조):
> "raw Φ의 103–108%가 pedestal이고 관측치가 null 평균보다 **낮다**" → 실측 E[Φ_null] ≈ 1.95 로
> raw Φ 의 **94~100%** 이며 관측치는 null 평균 **이상**이다 (arm A 는 정확히 null 위 Φ*=+0.001).
> pedestal 이 raw Φ 를 거의 전부 설명한다는 **결론 자체는 확증**됐다. §1.3 의 LCG cycle 겹침 정정은
> 미발사 캠페인에 그대로 유효하다.

모든 수치를 repo의 실제 probe(`state/1283_r6_content_relay_clean/h9260_content_relay_clean_probe.hexa`)와 estimator(`faithful_phi`)에 대고 재검증한 뒤 씁니다. 아래 §0·§1의 정량 주장은 전부 실측으로 확인된 것입니다.

한 가지 정직하게 먼저 밝힙니다: **§1.3에 원래 설계에 없었을 수 있는 정정이 하나 들어갑니다.** LCG cycle 겹침 위험(아래 §1.3 "핵심 사실")은 이번에 수치로 확인했고, 그대로 두면 "독립 realization"이 실제로는 난수를 공유하게 됩니다. R cap=8192가 왜 그 값인지도 여기서 유도됩니다.

---

# §0 — 진단: H_9260의 ⏳는 왜 일어났는가

프레임부터 고정한다. **⏳는 기질(substrate)에 대한 사실이 아니라 계측기에 대한 사실이었다.** 세 개의 독립적 결함이 있었고, 각각 단독으로도 런을 무효화하기에 충분했다. 세 결함은 Φ̄\*의 세 구성요소와 1:1로 대응한다 — 그것이 이 계측기가 tune-to-green이 아니라 수리(repair)인 이유다.

## §0-① — validity gate 자체가 ill-posed였다 (`dense_shuffle − A`)

`H_9260`의 ⏳는 문자 그대로 `valid = p1a_all && p1b_all` (probe L405)에서 나왔다. 그 두 leg이 딛고 선 대조군이 mode 9(`dense_shuffle`)다. 그 대조군은 **자신이 끊겠다고 주장한 결합을 끊지 않는다.**

probe L207–232를 보자. mode 8(dense)과 mode 9(dense_shuffle)의 relay 갱신은 단 한 줄만 다르다 (L213–214):

```
src = i                            // mode 8 (dense)
if mode == 9 { src = (i+n_mod-1) % n_mod }   // mode 9 (dense_shuffle)
```

그리고 그 `src`가 쓰이는 곳은 L220–224의 leave-one-out 합뿐이다:

```
while j < n_mod { if j != src { acc = acc + relay[j][d] }  j = j+1 }
let others = acc / to_float(n_mod - 1)
```

`S[d] = Σ_{j=0..3} relay[j][d]` (전체 relay 합)라 두면:

- **mode 8**: `others_i = (S − relay_i) / 3`
- **mode 9**: `others_i = (S − relay_{i−1}) / 3`

**두 arm 모두 global sum `S`를 그대로 읽는다.** 바뀐 것은 leave-one-out 인덱스 하나뿐 — 자기 자신을 뺄 것인가(8), 링 선행자를 뺄 것인가(9). 즉 "shuffle"은 cross-relay 결합을 **파괴하지 않고 보존**한다. mode 9의 relay lattice는 여전히 all-to-all mean-field로 결합된 4채널 시스템이다.

더 나쁜 것이 있다. mode 9에서 `j`는 `j ≠ i−1`인 모든 값을 훑으므로 **`j = i`를 포함한다.** 즉 mode 9에서는 `relay_i`의 구동항이 자기 자신을 (1/3 가중으로) 되먹인다 — mode 8에는 없던 self-drive다. 정리하면:

> **mode 9 = dense + self-gain − predecessor-coupling.**

이것은 "결합을 제거한 대조군"이 아니라 **그저 다른 결합 위상**이다.

따라서 P1a와 P1b는 **양쪽 다** ill-posed다.

- **P1a** ("구 readout에서 `ΔΦ(dense_shuffle − A) ≥ +0.02` ⟹ variance artifact가 존재한다"). 그러나 mode 9는 A(맨 ring, relay 채널 0개)에 비해 **all-to-all 결합된 relay 채널 4개라는 진짜 cross-module 구조를 추가로 갖는다.** 완벽하게 variance-free한 readout 아래에서도 mode 9는 A를 이기는 것이 정상이다. 그러므로 P1a의 Δ는 (i) amplitude-variance artifact와 (ii) 실재하는 추가 결합구조를 **분리 불가능하게 섞는다.** FIRED든 아니든 무정보다.

- **P1b** ("rank-uniform으로 재채점하면 같은 Δ가 `≤ +0.02`로 **붕괴**해야 한다 ⟹ readout이 artifact를 제거했다"). 이 PASS 조건은 readout에게 **실재하는 cross-module 결합을 지워버릴 것을 요구한다.** rank-uniform은 amplitude-variance를 제거하도록 설계된 것이지 joint 구조를 지우도록 설계된 것이 아니다. 즉 P1b는 **올바른 readout이 정당하게 FAIL할 수 있는 게이트**다.

실제로 그렇게 되었다. P1b는 seed 6 (Δ = +0.371)과 seed 10 (Δ = +0.110)에서 FAIL했고, 그 FAIL이 "이 기질에서 rank-uniform은 variance-free가 아니다 → ⏳"로 읽혔다. 올바른 독법은 정반대다: **rank-uniform은 mode 9가 실제로 갖고 있는 진짜 결합을 살려낸 것**이고, 무너진 것은 readout이 아니라 게이트다. 그리고 P1a도 seed 3, 6에서 FAIL했다 — **양방향 모두 FAIL**은 게이트가 어느 쪽으로도 정보를 주지 못한다는 signature다.

⟹ **RETIRE.** bar를 어디로 옮겨도 이 Δ는 구조를 통제하지 못한다. 이것이 §3에서 `dense_shuffle − A`를 폐기한 이유의 전문이다.

## §0-② — null의 표본 크기가 1이었다 (`B − Bperm`)

`shift_modules` (probe L278–292)는 `off_i = (i·17) mod 64`, 즉 **하나의 고정된 순환 shift**다. 이것은 "cross-module alignment를 파괴한다"는 null 분포로부터의 **단 한 개의 draw**다.

P0(`A − Aperm`)가 바로 그 null을 맨 ring 위에서 측정한 것이다. 9 seed 실측:

> **mean = +0.0277, sd = 0.2969**

null 자체의 산포가 bar(+0.02)의 **약 15배**다. 따라서 `B − Bperm`의 부호는 사실상 동전 던지기이고, 실제로 H_9260의 G4는 seed 3·7에서 FAIL, 나머지에서 PASS — 구조 없는 flip-flop이었다.

게다가 그 draw는 **degenerate subgroup**에서 뽑혔다. 순환 shift는 `S_64`의 `64! ≈ 1.27e89`개 원소 중 **64개짜리 순환 부분군**에 속한다 — 측도 0이고, 그것도 하필 "모듈 내 lag 구조를 보존하는" 특별한 부분군이다.

FREEZE는 P0를 사전등록해 "Bperm leg은 arm을 구별하지 못한다"를 **예측까지 했으면서도** G4를 conjunctive primary로 남겼다. 진단은 맞았는데 처방이 없었다.

⟹ **RETIRE G4(B−Bperm)를 arm 수준 게이트로 두는 것.** null은 arm이 아니라 **통계량 안으로** 들어가야 하고, K개로 평균되어야 한다. 그것이 Φ\*의 두 번째 항이다.

## §0-③ — Φ를 **차분이 아니라 값**으로 읽었다 (+ realization n=1 + 9/9 conjunction)

가장 무거운 원인이고, 세 겹이다.

### (a) raw Φ의 ~100%가 추정기 bias pedestal이다

estimator는 T=64 표본으로 8×8 joint histogram 위에서 MI를 추정한다. 유한표본 MI는 **독립 하에서도 양의 bias**를 갖는다 (≈ `(r−1)(c−1)/(2N ln2)` = 49/(2·64·ln2) ≈ 0.55 bit/pair). 실측하면:

| | Φ_obs (raw) | 같은 궤적의 pairing-null 평균 | **Φ\*** |
|---|---|---|---|
| arm A, seed 7 | 1.8951 | **1.9469** | **−0.052** |
| arm A, seed 3 | 1.7819 | **1.9327** | **−0.151** |

> **raw Φ의 103–108%가 pedestal이다.** H_9260이 arm 간에 비교하던 Φ ≈ 1.95라는 값은 거의 전부가 추정기 bias이고, arm 간 Δ(0.03~0.44)는 **두 pedestal의 차**였다. 관측치는 null 평균보다 오히려 *낮다*.

이것이 메모리의 측정 메타법칙(**창발신호는 값이 아니라 차분**)이 이 축에서 발현한 정확한 형태다.

### (b) realization n = 1 ⟹ 오차막대가 존재하지 않는다

(arm, seed)당 궤적 하나 → Φ 점추정 하나 → 자유도 0. 검정이 불가능하고, 남는 것은 잡음 위에 놓인 threshold뿐이다. 실측 산포: `Φ(A)` raw의 seed 간 sd = **0.2345** (bar의 11.7배), 단일 surrogate draw의 sd ≈ **0.14–0.15**.

### (c) 9/9 every-seed conjunction은 검정이 아니라 min 순서통계량이다 — 치명타

H_9260 **자기 자신의 데이터**로 계산한다. `ΔΦ(B−A)` 9 seed:

> mean = **+0.1186**, sd = 0.1752, **t(8) = 2.03** — **평균은 양수다** (양측 p ≈ .077).

그런데 9/9 규칙은 seed 2개가 음수라는 이유로 FAIL을 냈다. 참 효과크기가 관측된 평균(+0.1186)과 **정확히 같다고 가정해도**, 한 seed가 +0.02를 넘을 확률은 0.713이고, 9개 모두 넘을 확률은 `0.713⁹ = 0.048`:

> **H_9260의 primary 게이트는 자기 자신의 효과크기에 대해 검정력 ≈ 5%였다.** 참이든 거짓이든 FAIL하도록 구조적으로 예정되어 있었다.

FREEZE의 "최종 GREEN ≈ .12"는 기질에 대한 prior로 기록되었지만, 실은 **설계 자체의 검정력 천장**이었다. 메모리 `probe-defect-census-max-control-bias`(순서통계량이 KILL을 기계적으로 생성)와 `negative-claims-need-tost-not-ns`의 정확한 재발이다.

## §0 결론 — 세 원인 → 세 처방

| 원인 | 처방 (Φ̄\*의 구성요소) |
|---|---|
| ① ill-posed validity gate | 폐기 → 새 validity ladder (§2+) |
| ② null 표본 = 1, 그것도 퇴화 부분군에서 | **K=16 surrogate 평균을 통계량 안으로** — Φ\*의 뺄셈 항 |
| ③ 값-읽기 + n=1 + 9/9 min-통계량 | **pedestal 제거 + R realization block-mean** — Φ̄\*가 오차막대를 갖는 양이 됨 |

**⏳는 기질에 대한 무정보가 아니라 계측기에 대한 정보였다.** H_9260은 실패한 실험이 아니라, 성공한 계측기 교정이다.

---

# §1 — 계측기 (구현 완결 사양)

## §1.0 표기·상수·이름 함정

```
n = N_MOD = 4 · T = T_TICKS = 64 · DIM = 8 (모듈 내부차원) · NBINS = 8 · K = 16
seeds S = [3..11] (9개) · realizations r = 0 .. R−1
traj : (n, T) float64,  traj[i,t] = ‖s_i(t)‖²
```

⚠️ **이름 함정 (반드시 고정)**: `faithful_phi(state, n, dim, n_bins)`의 `dim`은 **표본축 T=64**이지 모듈 내부차원 8이 **아니다**. 항상 `faithful_phi(Z.ravel(), n=4, dim=64, n_bins=8)`.

## §1.1 `RU` — rank-uniform map

**당신의 H_1328 서술은 정확하다. CONFIRM.** 정확한 tie-break를 포함해 못박는다.

정의 (probe L251–275와 동일):

```
RU(x)[i][j] = #{k : x[i][k] <  x[i][j]}  +  #{k < j : x[i][k] == x[i][j]}
출력 = float64,  각 행의 값역 = 정확히 {0.0, 1.0, …, T−1.0}
```

각 행은 항상 `0..T−1`의 **순열**이다 — 동률이 있어도 중복 rank는 생기지 않는다. **tie-break = 인덱스 오름차순** (동률이면 원래 인덱스가 작은 쪽이 낮은 rank).

**동등한 O(T log T) 형태** (동률을 주입해 bit-identical 검증 완료):

```
order        = argsort(x[i], kind="stable")     # 오름차순, 동률은 원래 인덱스 순
ranks[order] = arange(T)
RU[i]        = float64(ranks)
```

`kind="stable"`은 **필수**다. `"quicksort"`를 쓰면 동률 순서가 깨져 tie-break가 달라진다.

### RU의 두 가측 불변량 — 계측기 전체가 여기 서 있다

**(I1) 주변분포 고정.** 각 행의 multiset이 `{0..T−1}`로 고정 ⟹ `nbins=8, T=64`에서 bin 폭 `bw = 63/8 = 7.875` ⟹ **각 bin에 정확히 8개** (실측: `bincount = [8,8,8,8,8,8,8,8]`). 따라서 모든 모듈·모든 arm·모든 surrogate에서

```
H(a) = H(b) = H_const ≈ 3.0 bit   (상수)
⟹ MI(i,j) = 2·H_const − H(joint_ij)
```

자유량은 **joint 항 하나뿐**이다.

**(I2) permutation-equivariance (동률이 없을 때).** `RU(π(x)) = π(RU(x))`. *증명*: rank는 행의 multiset의 함수이고 π는 multiset을 보존한다. 동률이 없으면 tie-break가 발동하지 않으므로 인덱스 의존성이 사라진다. ∎

### HARD-ABORT — f64 tie-collapse (P1-SELF가 막아야 하는 이유)

동률이 있으면 (I2)가 깨진다. 그때 RU는 동률 블록을 **인덱스 순서**로 순위매기므로, **인덱스 순서 정보가 ranked 신호 안으로 새어 들어간다.** 모든 모듈이 같은 인덱스 순서를 공유하므로 이것은 **가짜 cross-module pairing**을 만든다. 극단적으로 어떤 모듈이 죽어 전 구간 상수가 되면 `RU(row) = [0,1,…,63]`이 되고, 그런 모듈끼리는 MI가 최대가 되어 Φ가 순수 artifact로 치솟는다.

```
검사: ∀ (arm, s, r), ∀ i :  len(unique(traj[i])) == T
위반 → HARD-ABORT.  seed 교체·재시도·downgrade 전부 금지. 런 중단 후 보고.
```

연속값 64개에서 정확한 f64 동률이 날 확률은 사실상 0이므로, 발화 = 불운이 아니라 **구조적 결함**(죽은 모듈·구동 0인 arm·leak 붕괴)의 신호다.

## §1.2 `π_k` — normalization permutation

**축**: 시간(표본)축 `t = 0..T−1`을 **각 모듈 행 안에서** 재배열.

**모듈별 독립 — 공유 순열 금지.** 공유(common) 순열은 Φ를 **정확히 불변**으로 남긴다(아래 L1) ⟹ `Φ* ≡ 0`이 되어 계측기가 죽는다. 반드시 모듈마다 독립 draw.

**모듈 0은 identity로 고정한다 — 그리고 이것은 편의가 아니라 정확한 분산 감소다.**

> **(L1) 공통 순열 불변성.** Φ는 pairwise MI 행렬의 MIP이고, `MI(i,j)`는 `bincount(b_i[t]·8 + b_j[t])` — 즉 **동시각 t에서 공기(co-occurring)하는 쌍의 multiset**만의 함수다. 모든 모듈에 동일한 σ를 적용하면 t 라벨만 바뀌고 쌍의 multiset은 불변 ⟹ Φ 불변. *(실측: bit-identical, `1.895066 == 1.895066`.)*
>
> **(L2) 모듈 0 고정의 정확성.** `(σ_0,…,σ_{n−1})`에 공통으로 `σ_0⁻¹`을 적용하면 (L1)에 의해 Φ는 그대로이고 배치는 `(id, σ_0⁻¹σ_1, …, σ_0⁻¹σ_{n−1})`로 옮겨간다. `σ_i`가 iid uniform이면 `{σ_0⁻¹σ_i}_{i≥1}`도 iid uniform이다. ⟹ **"n개 전부 순열"의 null 분포와 "모듈 0 = identity, 1..n−1만 순열"의 null 분포는 정확히 같다.** *(실측: all-4 → mean 1.9504/sd 0.1401, mod0=id → mean 1.9469/sd 0.1499 — 일치.)* 따라서 모듈 0 고정은 draw를 하나 아끼면서 분포를 바꾸지 않는다. ∎
>
> **(L3) 부수효과.** `π_k`는 폐기된 Bperm의 **정확한 K-표본 일반화**가 된다: `shift_modules`는 `off_0 = (0·17) mod 64 = 0` — 모듈 0이 이미 identity였다. 옛 null은 새 null의 support 안의 원소 하나(그것도 순환 부분군에서 뽑힌 하나)일 뿐이다.

**draw 방식 — Fisher–Yates (backward, in-place)**, 모듈 `i`·surrogate `k`마다 전용 LCG 스트림:

```
p ← [0, 1, …, T−1]
x ← perm_seed(s, r, k, i)
for m = T−1 down to 1:
    x ← lcg_next(x)
    j ← floor( lcg_unit(x) · (m+1) )      # lcg_unit(x) ∈ [0,1) ⟹ j ∈ [0,m] 보장
    swap p[m], p[j]
정확히 T−1 = 63 step 소비.
```

`x ≤ 2147483647 < 2147483648`이므로 `lcg_unit(x) < 1`이 **엄격**하게 성립 ⟹ `j ≤ m`이 항상 보장된다. 클램프 불필요.

**적용 방향 (고정)** — **gather**, scatter 아님:

```
Z_k[0] = Z[0]                       # 모듈 0 = identity
Z_k[i] = Z[i][ p_{k,i} ]   for i = 1..n−1
```

### 왜 full index permutation이고 phase/IAAFT가 아닌가 — **당신의 판단이 맞다. CONFIRM.**

근거를 정확히 셋으로:

1. **estimator는 t의 순서를 전혀 쓰지 않는다.** transition(t→t+1)도, lag도, spectrum도 들어오지 않는다. `mi_pair`는 오직 동시각 쌍의 joint histogram만 본다. 즉 **autocorrelation은 이 추정기의 정의역 밖**이다. 따라서 autocorrelation을 보존해주는 surrogate(phase-randomized / IAAFT)는 *추정기가 볼 수 없는 것을* 비싸게 보존하는 것이고, 얻는 것이 0이다.

2. **더 나쁜 것은, phase randomization은 주변분포를 바꾼다**(Gaussianize). 그런데 추정기는 주변분포를 **본다**(`H(a)`, `H(b)`, binning). ⟹ *볼 수 없는 것을 통제하려다 볼 수 있는 곳에 통제되지 않은 confound를 주입*하는 순손실이다. IAAFT는 rank 재배정으로 주변분포는 맞추지만 대신 spectrum을 근사로만 맞추는데, 그 spectrum은 애초에 무관하다.

3. **pairing 통계량의 exact null은 하나뿐이다**: 각 모듈의 주변 multiset을 (bit 단위로) 고정하고 pairing을 uniform하게 랜덤화하는 것. RU 아래에서 각 행의 multiset이 정확히 `{0..63}`이므로, 이 null은 **`S_T` 위의 uniform 순열**로 정확히 실현된다 — surrogate의 주변분포가 관측치와 **bit-identical**이고, 따라서 뺄셈이 joint 항만 남긴다((I1)).

> ⟹ full index permutation은 *허용 가능한 정도*가 아니라 **이 추정기의 정확·최소·충분(exact, minimal, sufficient) null**이다. 이보다 좁히면(= Bperm의 순환 부분군) §0-②의 병에 그대로 걸린다.

## §1.3 LCG stream derivation

### Base (probe L24–35, verbatim)

```
A = 1103515245 · C = 12345 · MASK = 2147483647 · M = 2^31 = 2147483648
lcg_next(x) = (x·A + C) & MASK              # ≡ (x·A + C) mod 2^31
lcg_unit(x) = x / 2147483648.0              # ∈ [0,1)
lcg_gauss(x0):
    s1 = lcg_next(x0);  s2 = lcg_next(s1)
    u1 = lcg_unit(s1);  u2 = lcg_unit(s2)
    if u1 < 0.0000001: u1 = 0.0000001
    z  = sqrt(−2·ln u1) · cos(2π·u2)        # cos branch만. sin branch 폐기.
    return (z, s2)                          # s2 = 새 state.  gauss 1개당 2 step.
```

상태는 **Python int**로 유지한다 (`np.int32`/`np.int64` 금지). 실제로 곱의 상한은 `2^31·A ≈ 2.37e18 < int64 max`라 int64도 안전하지만, 재현성 리스크를 감수할 이유가 없다.

### ⚠️ 핵심 사실 — 모든 스트림은 **하나의 cycle** 위에 있다

이 LCG는 mod 2^31에서 full-period(Hull–Dobell 충족)이므로 **cycle이 하나뿐**이다. 그러므로 *"해시로 서로 다른 시드를 만들면 독립 스트림"* 이라는 통념은 **거짓**이다 — 서로 다른 시작점은 같은 cycle 위의 서로 다른 **창(window)** 일 뿐이고, 창이 겹치면 두 realization은 같은 난수를 공유한다.

소요량을 계산하면 이건 이론적 걱정이 아니다:

```
궤적 1개 = 2144 gauss = 4288 step
9 seeds × R=8192 × 4288 = 3.16e8 step  = cycle의 14.7%
시작점을 해시로 흩뿌릴 경우, 겹치는 realization 쌍의 기대값 ≈ 1e4개
```

⟹ **시드를 해시하지 말고, cycle을 명시적으로 분할(arena)해서 jump-ahead로 할당한다.**

### jump-ahead (정확 · O(log j))

아핀사상 `(A,C): x ↦ (A·x + C) mod M`의 이진 거듭제곱:

```
lcg_jump(x, j):
    (Aa, Cc) ← (1, 0)          # identity map
    (Ab, Cb) ← (A, C)          # f_1
    while j > 0:
        if j & 1:
            Aa ← (Ab·Aa) mod M
            Cc ← (Ab·Cc + Cb) mod M
        Cb ← (Cb·(Ab + 1)) mod M
        Ab ← (Ab·Ab)      mod M
        j  ← j >> 1
    return (Aa·x + Cc) mod M
```

*검증 완료*: `lcg_jump(x,1) == lcg_next(x)`, `lcg_jump(x,1000) == lcg_next 1000회`.

### anchor (H_9260 회귀 앵커)

```
anchor(s) = (s · 2654435761) & 2147483647          # probe L53
if anchor(s) == 0: anchor(s) = 12345               # probe L54 (s=3..11에선 발화 안 함; 충실도로 유지)
```

### cycle geometry — **여기서 R의 cap이 유도된다**

```
2654435761 mod 2^31 = 506,952,113
⟹ anchor(3..11) = 공차 506,952,113의 등차수열 mod 2^31 (Knuth 황금비 해시)
⟹ 세거리 정리대로 gap은 정확히 두 값만: 119,675,196 과 387,276,917
   (합 = 2^31 정확히 일치 — 검증 완료)
⟹ seed당 사용 가능한 연속 arena = min gap = 119,675,196 step
```

### arena 배치 (seed s의 anchor로부터의 offset — 전부 검증됨)

| arena | offset base | per-r stride | 실제 소요/r |
|---|---|---|---|
| **TRAJ** | `0` | 8192 | 4288 |
| **PERM** (K개 정규화 순열) | `2^26` = 67,108,864 | 4096 | 16·3·63 = 3024 |
| **SPIKE** (P-CAL 주입) | `2^26+2^25` = 100,663,296 | 1024 | 2·(64+256) = 640 |
| **PCAL** (π_a, π_b) | `2^26+2^25+2^23` = 109,051,904 | 512 | 2·3·63 = 378 |

```
arena 총 끝 = 109,051,904 + 8192·512 = 113,246,208  <  119,675,196  ✓ (여유 6,428,988)
R_max(기하학적) = 119,675,196 / (8192+4096+1024+512) = 8657
```

> **FREEZE의 `cap 8192`는 임의 상수가 아니라 그 아래 최대 2의 거듭제곱이다 — LCG cycle 기하학이 강제하는 한계.**
> **`floor 2048`의 근거는 SE**: 단일 realization Φ\*의 sd ≈ 0.15 ⟹ `R=2048`에서 SE ≈ 0.0033 (= 0.02 효과에 6 SE), `R=8192`에서 SE ≈ 0.0017 (= 12 SE).

### 스트림 정의 (전부 **arm-independent** — common random numbers)

```
seed_state(s, r)       = lcg_jump( anchor(s), 0                  + r·8192 )
                         # r = 0  ⟹  anchor(s) 정확히  ✓ H_9260 회귀조건 충족

perm_base(s, r)        = lcg_jump( anchor(s), 2^26               + r·4096 )
perm_seed(s, r, k, i)  = lcg_jump( perm_base(s,r), (k·(n−1) + (i−1))·63 )
                         # i = 1..n−1 (i=0은 identity, 스트림 미소비) · k = 0..15

spike_base(s, r)       = lcg_jump( anchor(s), 2^26+2^25          + r·1024 )
    g[t]    : spike_base 로부터 T=64 gauss           (128 step)
    e_i[t]  : 이어서 n·T = 256 gauss                  (512 step)
              순서 = i 바깥루프, t 안루프

pcal_base(s, r)        = lcg_jump( anchor(s), 2^26+2^25+2^23     + r·512 )
pcal_seed(s, r, w, i)  = lcg_jump( pcal_base(s,r), (w·(n−1) + (i−1))·63 )
                         # w = 0 : π_a  ·  w = 1 : π_b
```

**π_a/π_b가 K개 정규화 순열과 disjoint하다는 것은 주장이 아니라 주소 분리에 의한 구성적 증명이다**: PERM arena는 `[2^26 + r·4096, +3024) ⊂ [2^26, 2^26+2^25)`에, PCAL arena는 `[2^26+2^25+2^23, …)`에 놓인다. 두 구간은 겹치지 않는다.

**arm-independence**: 위 어떤 스트림도 arm(mode)을 인자로 받지 않는다. 따라서 같은 `(s,r)`에서 **모든 arm이 동일한 궤적 draw · 동일한 K개 π_k · 동일한 spike를 공유한다** ⟹ arm 간 Δ는 paired, common random numbers가 되어 분산이 크게 줄고 null-draw 잡음이 Δ에서 상쇄 방향으로 상관된다.

**벡터화 (근사가 아니라 항등)**: LCG는 축차적이지만, 아핀사상 표를 미리 만들면 한 번에 벡터화된다. 길이 L의 상태열은 `(A_j, C_j)_{j=0..L−1}`를 미리 계산해 두고 `states = (A_vec · x0 + C_vec) mod 2^31` 한 방으로 얻는다 (int64 안전: `A_vec·x0 ≤ 2^31·2^31 = 4.6e18 < 9.22e18`). 이후 Box–Muller도 벡터화. **이건 선택이 아니라 지정이다** (§1.5 참조).

## §1.4 `Φ*` computation order

한 `(arm, s, r)`에 대해 **정확히 이 순서**:

```
1.  st    ← seed_state(s, r)                        [arm 무관]
2.  traj  ← gen_traj(st, arm) → (4,64) float64,  traj[i,t] = ‖s_i(t)‖²
        draw 순서 고정: states(32) → inputs(2048) → chans(32) → relay(32) gauss = 4288 step
        ⟹ arm A는 draw 1·2에만 의존하고 arm 간 byte-identical
        [최적화] (s,r)당 2144개 gauss를 한 번만 생성해 전 arm에 재사용 — 정확히 동일
3.  P1-SELF tie 검사:  ∀i, len(unique(traj[i])) == 64.   위반 → HARD-ABORT
4.  Z     ← RU(traj)                                — 한 번만. 각 Z[i]는 {0.0..63.0}의 순열
5.  B[i]  ← bin_values(Z[i], 8)                     — 한 번만
        (I1에 의해 각 행 bin count = [8]×8, H(a)=H(b)=H_const ≈ 3.0
         ⟹ H_const는 스칼라 상수 1회 계산 후 전역 재사용)
6.  φ_obs ← faithful_phi(Z.ravel(), n=4, dim=64, n_bins=8)
7.  for k = 0..15:
        π_k:  모듈 0 = identity;  i=1..3 → p_{k,i} ← FisherYates(64, perm_seed(s,r,k,i))
        Z_k[0] = Z[0];  Z_k[i] = Z[i][p_{k,i}]
        φ_k   ← faithful_phi(Z_k.ravel(), 4, 64, 8)
8.  Φ*(arm, s, r) = φ_obs − (1/16)·Σ_k φ_k          ← 원자 단위. realization마다 형성.
9.  Φ̄*(arm, s) = (1/R)·Σ_{r=0}^{R−1} Φ*(arm, s, r)
    SE(arm, s)  = sd_r(Φ*) / √R
    ⟹ R개 값 전부(최소한 Σ와 Σ²)를 보존할 것. SE가 계산 가능해야 한다.
10. arm 차분은 (s,r) 수준에서 paired로 먼저 형성:
        Δ(a1−a2, s, r) = Φ*(a1,s,r) − Φ*(a2,s,r)     그 다음 r에 대해 평균.
    ❌ 절대 평균끼리 빼지 말 것 — 평균값은 같지만 분산이 완전히 달라진다(공통 난수의 상쇄를 잃는다).
```

### k에 걸친 재사용 규칙 (전부 bit-exact)

- **(a)** `Z`는 k에 걸쳐 재사용 — 재계산 금지.
- **(b)** **binning도 재사용 가능하고 정확하다**: `bin_values(Z[i][p]) == bin_values(Z[i])[p]` (원소별 연산이고 min/max는 순열 불변) ⟹ surrogate의 binned 행은 순수 gather `B[i][p_{k,i}]`. **재binning 불필요.**
- **(c)** `H(a)`, `H(b)`는 `H_const` 상수 ⟹ `MI(i,j) = 2·H_const − H(joint_ij)` — **joint histogram 6개만** 다시 계산.
- **(d)** **`π_k`는 arm 무관** ⟹ `(s,r)`당 16개 순열을 **한 번 만들어 전 arm에 재사용**.

### 당신의 질문 — surrogate를 RU **뒤에** 적용하는가? **CONFIRM.**

FREEZE 문구 그대로 `Φ(π_k(RU(traj)))` — **이미 ranked된 배열을 순열한다.** 근거 셋:

1. §1.1 **(I2)** 에 의해, **동률이 없으면** `RU(π(x)) = π(RU(x))` — 즉 permute-before-RU와 **정확히 동일**하다. 그리고 동률 부재는 3단계 **HARD-ABORT가 보증한다.** 두 순서가 갈라지는 유일한 경우를 게이트가 이미 막아둔 것이다 — **이 HARD-ABORT는 바로 이 저렴한 순서를 합법화하는 조건이다.**
2. 비용: permute-before-RU는 RU를 K배 수행해야 한다. permute-after-RU는 1회.
3. surrogate의 주변분포가 관측치와 **bit-identical**임이 자명해진다(같은 배열의 순열) ⟹ 뺄셈이 joint 항만 남긴다는 (I1) 논증이 무조건 성립한다.

### estimator 고정 사항 — port가 반드시 재현해야 하는 3가지 "quirk = SPEC"

- `bin_values`의 all-identical 가드는 **f32 EPSILON 리터럴 `1.19209290e-7`** (파이프라인이 f64여도 그대로).
- `_entropy`는 `total + 1e-8`로 나누고 `log2(p + 1e-10)`을 쓴다.
- **MIP 열거는 `mask = 1`부터 시작한다** ⟹ 이분할 `{0} | {1,2,3}`은 **절대 평가되지 않는다.** "고쳐서" 추가하면 Φ가 바뀌고 H_9260 회귀가 깨진다.

> 참고: 이 mask 비대칭은 `π_k`의 모듈-0-identity와 **무관하다.** (L2)의 불변성 논증은 estimator 내부 비대칭과 독립이며, 실측으로도 두 null(mod0=id vs all-4)이 일치함을 확인했다.

## §1.5 numpy 비용모형

> **`(arm, s, r)` 하나당 Φ 호출 = `1 + K` = 17.** (φ_obs 1개 + surrogate 16개.)
> **총 Φ 호출 = `n_arms × 9 × R × 17`.**

| n_arms | R=2048 | R=4096 | R=8192 |
|---|---|---|---|
| 5 | 1,566,720 | 3,133,440 | 6,266,880 |
| 6 | 1,880,064 | 3,760,128 | 7,520,256 |
| 7 | 2,193,408 | 4,386,816 | 8,773,632 |

(P-CAL / P1c의 spike-in leg도 같은 `17 calls/cell` 비율로 자기 `(arm,s,r)` 셀을 더한다.)

**Φ 1회 비용** (n=4, T=64, nbins=8): `mi_pair` 6회 (각각 bincount 3 + entropy 3, 길이 ≤64) + 7개 mask MIP. 배열이 작아 **numpy 오버헤드가 지배**한다 — 소박한 구현으로 **~50–70 µs/call**.

```
n_arms=6, R=8192 (최대 구성):  7.52e6 × 60 µs ≈ 450 s ≈ 7.5분  (단일 코어)
§1.4 재사용 규칙 적용 시 (binning gather + H_const 상수 + joint만 재계산)
                            → ~20–25 µs/call → 3분 이하
(k, r)에 대해 배치 벡터화 시 → 초 단위
```

**궤적 생성**: `9 × R × 4288` step — **arm이 아니라 `(s,r)`당 1회** 생성해 전 arm 재사용. R=8192에서 3.16e8 step이다. 순수 Python 루프로 돌리면 5–10분으로 **전체 비용을 지배**해 버리지만, §1.3의 **아핀표 벡터화**를 쓰면 무시할 수준이 된다.

⟹ 전체는 **CPU 단일 호스트 · 수 분 규모**다. `[2048, 8192]` 구간 어디에서도 **비용은 제약이 아니다.** 따라서 R은 예산이 아니라 **오직 P-CAL의 정밀도 요구로만** 정해져야 한다 (FREEZE대로 하향 금지).

---

## 요약 — 이 §1이 §0의 세 원인을 어떻게 닫는가

| §0 원인 | §1의 대응 |
|---|---|
| ① `dense_shuffle`가 결합을 보존 (probe L214/L220-224) | 폐기. 대체 ladder는 §2+ |
| ② null 표본 = 1, 퇴화 부분군 | **§1.2** — `S_T` 위 uniform 순열 K=16개, exact·minimal·sufficient null이 **통계량 안으로** |
| ③ 값-읽기(pedestal 103–108%) + n=1 + 5% 검정력 | **§1.4** — realization마다 pedestal을 빼서 Φ\*를 만들고, R로 block-mean해 **오차막대를 갖는 양**으로 만든다 |

포팅 시 결정해야 할 설계 사항은 **없다.** 모든 상수·순서·스트림·중단조건이 위에 고정되어 있다. 두 곳만 특히 조심하면 된다: `argsort(kind="stable")`(§1.1), 그리고 **시드를 해시하지 말고 `lcg_jump` arena로 할당할 것**(§1.3) — 후자는 그냥 두면 "독립" realization들이 조용히 난수를 공유한다.