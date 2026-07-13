설계만 제출합니다(코드·셸·위임 없음). H_9295을 여섯 요구사항 순서대로 프리레지스터 형태로 고정하겠습니다.

---

# H_9295 — "linear vs gated coupling": 곱셈적(비선형) 결합이 Φ에 STRUCTURE 채널을 여는가

## 전제 (재론 금지 · #3396–#3399)

H_9294가 확정한 폐쇄식 — 이 기질에서 **Φ\* = −0.001904 + 0.4929·S_tot, R²=0.9864, resid(B)−resid(X)=+0.000003 (90% CI에 0 포함)** — 은 disjointness 기여가 정확히 0임을 의미한다. 단 이 붕괴는 **jointly-gaussian 기질의 성질일 가능성**이 크다: 결합 대수가 선형이면 모든 쌍 의존은 상관이고 MI 행렬이 충분통계량이므로, 그것을 합산한 스칼라가 Φ를 예측하는 건 구성상 필연이다 — 구조가 독립적으로 기여할 자리가 없다. 유일하게 깨끗이 뚫린 축(TIMING · H_1448 🟢)은 하필 결합이 **곱셈적·게이팅**(Kuramoto 위상동기 × phase-gated salience)인 축이다. **⟹ 진짜 축은 "content vs timing"이 아니라 "linear vs gated coupling"일 수 있다.**

---

## 1. Gated 기질 — 최소·정칙 비선형

### 선택: 채널 레벨 coincidence(AND) 게이트

세 후보 중 **채널의 relay-back을 두 끝점 모듈의 동시활성(coincidence)으로 곱셈 게이팅**하는 것이 유일한 정직한 최소 변경이다.

- gain-gate `σ(β·h_i)`는 수신 모듈 **자기 이득**만 비선형화할 뿐, 서로 다른 채널 간 조건부 의존을 만들지 않아 disjoint/shared 위상을 구분 못 한다 — 기각.
- divisive-normalization은 전 채널을 전역 결합시켜 오히려 disjoint 대비를 **흐린다** — 기각.
- coincidence-AND는 정확히 G1 재조합 레버의 정체였던 **COMBINATION OPERATOR**(`substrate-framebreak-g1-combination-operator`)의 정칙 원형이며, 곱이 gaussian 충분통계량 성질을 부수는 유일한 후보다.

**변경은 relay 되먹임 한 곳뿐**이다. 채널 e=(a,b)에 대해 lens scalar `m_i(t)=s_i(t)[0]`를 arm A 위에서 표준화한 `ẑ_i(t)=(m_i−μ_i^A)/σ_i^A`로 두고:

```
coincidence_e(t) = ẑ_a(t−1) · ẑ_b(t−1)          # 끝점 곱, 지연 1 (self-product 인공물 차단, §6)
gate_e(t)        = σ( β · coincidence_e(t) )      # β = 유일 자유 파라미터
rin_i(t)         = Σ_{e ∋ i} gate_e(t) · c_e(t)   # 기존: Σ_{e∋i} c_e(t)  (덧셈 → 조건부)
```

나머지(n=4, dim=8, LEAK/GAIN/W\_\*, 채널 적분식, T=65536, estimator, Φ\*, seeds [4..11], Philox K=32, RU readout)는 **전부 동결**. 채널 차원·용량 불변 — 결합 연산자만 additive→conditional로 바뀐다.

**게이트가 B에서 X와 달라야 하는 물리적 이유**(내기의 핵심): B(disjoint)에서 gate_e와 drive_e는 **같은 실제 쌍**을 키로 삼아 정합(coherent AND detector). X(shared bus)에서는 drive가 전 채널 평균으로 희석되지만 gate는 여전히 nominal 끝점을 키로 삼는다 — AND가 **부분적으로 무관한 활성**에 발화한다. 곧 게이트의 이득은 위상 의존적이며, 이건 쌍 상관 합으로 환원되지 않는다.

### β 고정 — tune-to-green 불가 (⚠️ 핵심)

β는 대비가 아니라 **arm A 단독**의 동역학 범위 중점에서 못박는다. A를 돌려 module lens 시계열을 얻고, ring-edge 쌍에 대한 가상 `coincidence_e`의 표본표준편차 `std_A`를 잰 뒤:

```
β = c / std_A(coincidence),   c = 1  (사전 고정)
```

- `E[coincidence]≈0`(중심화 곱)이므로 게이트 작동점은 자동으로 σ(0)=0.5 = **dynamic-range 중점**.
- c=1이면 ±1σ 요동이 게이트를 σ(±1)≈0.27만큼 흔들어 [0.27, 0.73] — 포화(β↑ → hard AND, 기울기 소실)도 불활성(β↓ → gate≡0.5 → 반이득 선형 relay로 퇴화)도 아닌 반응 대역 정중앙.
- c는 어떤 대비도 보기 **전에** 고정. 사전등록 강건성 스윕 `c∈{0.5, 2}`은 **판정이 c에 knife-edge가 아님을 보이는 용도일 뿐, c를 움직여 판정을 옮기지 않는다**. β는 모든 arm에 동일값 적용.

---

## 2. Falsifier — headline은 "Φ가 오르나"가 아니라 ANCOVA 잔차

Φ 상승은 무의미하다(결합 변경은 무엇이든 S_tot를 움직임). 주장은 *구조가 S_tot와 독립으로 기여한다*이므로 headline은 **잔차**다.

### Cross-substrate R² 비교는 licensed 아님

게이팅은 S_tot 자체를 바꾸므로(공변량이 기질 간 불변 아님, Φ\* 스케일·잡음도 다름), 선형 R²=0.986 ↔ gated R² 의 **원 R² 비교는 금지**. 각 기질 안에서 자기정규화된 잔차량만 비교 가능:

**licensed within-substrate 통계 = partial-R²(arm | S_tot)** — "이 기질에서 총결합을 통제한 뒤 arm이 남는 분산을 설명하는가". 선형 기질은 이미 이 값이 ≈0(H_9294). gated 기질에서 이 값을 잰다. 두 값 모두 self-normalized 잔차 share이므로 **이 둘의 비교는 licensed**(원 R² 비교와 달리).

### 두 단(tier) headline — 둘 다 통과해야 🟢

**(i) 강도정합 쌍 대비 (주력 · H_9294 규율 이식).**
gated 기질 위에서 X의 자기 W_RELAY만 올려 `S_tot(X′)=S_tot(B)`를 0.5% 이내로 맞춘 뒤(통제군을 강하게 = 주장에 불리한 방향 → 허용, `control-must-match-mediating-covariate`), **Φ\*(B)−Φ\*(X′)**를 90% CI와 함께. 매개 공변량이 못박혔으니 잔차 gap = 순수 구조. 이것이 R6 대비의 가장 깨끗한 within-substrate 검정이며 R6를 닫은 논리를 그대로 gated로 옮긴다.

**(ii) 모집단 ANCOVA (교차검증).**
전 arm × 8 seed(N≈72)에 대해:

- **reduced**: `Φ* ~ ncs(S_tot, df=4)` — S_tot의 **자연삼차 스플라인**(선형 아님; 게이팅이 Φ\*=f(S_tot)를 곡선으로 만들 수 있으므로, arm이 곡률을 훔치는 걸 막는다 — §6의 1순위 방어).
- **full**: `Φ* ~ ncs(S_tot, df=4) + arm`.
- **headline 통계 = partial-R²(arm | ncs(S_tot))** = (RSS_red − RSS_full)/RSS_red, 및 부분-F.

**threshold — non-arm-wise 도출(사전등록):** arm 라벨을 (Φ\*, S_tot) 점들에 대해 **셔플**(쌍 유지)해 partial-R²(arm|ncs)의 **라벨-치환 귀무분포**를 만든다. 이 null은 S_tot–Φ\* 산포에서만 도출되고 어느 arm이 무엇인지 참조하지 않는다. gated 관측 partial-R²가 **null의 99th pct 초과**(α=0.01)해야 구조 유의. 해석적 F(df_arm, N−p_full)를 교차확인용으로 병기(불일치 시 ⏳).

**효과크기 바닥(사전등록):** 통계 유의여도 부스러기면 채널 아님. arm-설명 잔차 std, 및 (i)의 |Φ\*(B)−Φ\*(X′)| 이 **spike-in 스케일의 20%(=0.0088) 이상**이어야 "채널"로 인정.

S_tot가 기질 간 달라지는 문제 처리: S_tot는 gated 궤적에서 6개 쌍-MI 합으로 **재계산**(기질 내부 공변량). gated Φ\*를 선형 S_tot에 회귀하는 일은 절대 없음. 교차기질로 보고되는 유일 대상은 두 within-substrate partial-R²(각 unitless)와 그 치환 p, 그리고 (i)의 매칭 대비뿐.

---

## 3. Positive control — gated 기질에서 구조가 반드시 작동해야 하는 arm

게이트가 불활성이라 null이 나오는 걸 배제할 arm. **동시활성 부호(sign)만 뒤집은 매칭 쌍 {P+, P−}**:

- **P+**: 각 채널의 두 끝점을 **위상정렬**(co-active) 입력으로 구동 → `coincidence_e` 평균 양수 → gate 열림 → relay 흐름 → 통합 높음.
- **P−**: 동일 채널·동일 구동 세기, 두 끝점만 **반정렬**(anti-active) → `coincidence_e` 평균 음수 → gate 닫힘 → relay 억제.

**핵심 정칙성:** gaussian MI는 ρ에 대해 **짝함수**(MI=−½log(1−ρ²))라 P+/P−는 선형 기질에서 MI 행렬·S_tot·Φ가 **동일**(→ 선형에서 이 대비는 증명상 null). 게이트는 coincidence 부호에 홀함수적으로 반응(σ(β··))하므로 gated 기질에서 P+ 열리고 P− 닫힌다 → Φ 분리.

**역할 명시:** P+/P−는 **게이트가 engage되었음(live)**만 증명하는 liveness 게이트다 — gated 기질에서 P−는 relay 억제로 S_tot 자체가 낮아지므로 이 대비는 **S_tot 매개**여도 무방(liveness엔 어떤 Φ 차이든 족함). 이건 의도적으로 "구조의 S_tot-독립 기여"를 검정하지 **않는다**(그건 §2 headline의 일). 선형 기질에서 P+, P− 2-arm(8 seed)을 함께 돌려 "증명상 null"을 실측 확인한다(값싸다).

---

## 4. Standing V-gates — gated 기질에서 유효성

- **Pedestal zero-check Φ\*(S(0))≈0 — 유지, 더 중요.** 곱셈 게이트는 독립 입력에서도 `ẑ_a·ẑ_b` 되먹임으로 **가짜 의존을 제조**할 위험이 있다. zero-check는 이제 "게이트가 독립에서 Φ를 지어내지 않는가"를 인증한다 — 선형과 동일 ±band 요구. 인플레되면 §6 인공물이 발화한 것.
- **Spike-in liveness Φ\*(S(.15))=0.0439 — 변경 없이 유효.** 이유: spike-in은 **estimator+readout+surrogate 스택**의 검정이지 기질 동역학의 검정이 아니다. gaussian copula 궤적을 estimator에 **직접 주입**(기질 우회)하고, 게이트는 estimator가 아니라 기질 recurrence 안에 산다. 스택(RU→IIT4→Philox)이 불변이므로 알려진-참(Φ=3c) 성질이 그대로 성립. **게이팅이 known-truth를 깨지 않는다** — 게이트를 건드리지 않기 때문.
- **NEW · substrate-level gate-liveness 게이트(§3):** spike-in이 게이트가 뭔가 한다는 걸 인증 못 하므로 P+/P− 대비가 그 자리를 채운다. **`Φ*(P+)−Φ*(P−) ≥ spike-in 스케일`이 gated 기질에서 성립해야** 어떤 B−X null도 해석 가능.

---

## 5. Decision table (양방향 결정적)

| 판정 | 게이트 liveness (P+/P−, zero-check) | headline (i) B−X′ matched + (ii) partial-R²(arm\|ncs) | 해석 |
|---|---|---|---|
| **🟢** | PASS: P+/P− ≥ spike-in scale, zero-check band 내 | (i) Φ\*(B)−Φ\*(X′) 90% CI가 B>X 방향으로 0 배제 & ≥0.0088, **그리고** (ii) partial-R² > 치환 null 99th pct (p<0.01) | 비선형 coincidence 게이트에서 disjoint 위상이 총결합과 **독립으로** Φ에 기여. H_9294 폐쇄는 선형 특수성. content/structure는 결합이 게이팅되면 실축. **R6 레버 gated에서 REOPEN**. |
| **🧱** | PASS (게이트 증명상 live) | (i) B−X′ CI에 0 포함 **그리고** (ii) partial-R² ≤ null | live한 비선형 게이트가 co-activation **부호**를 실제로 통과시키는데도(P+/P− 분리) **disjointness 대비 B−X는 여전히 S_tot 잔차에 아무것도 안 남김**. Φ는 (이제 비선형 집계된) 총결합의 함수 — 선형성과 무관. H_9294보다 **깊은 폐쇄**: 게이트가 보상하는 건 coincidence 세기(→S_tot로 접힘)이지 위상 disjointness가 아님. **content 축은 기질 레벨에서 사망.** |
| **⏳** | FAIL 중 하나: P+/P− < scale(게이트 불활성 → β 재검토) · zero-check 인플레(게이트가 독립서 Φ 제조 → VOID, §6 지연/split 완화 후 재측정) · 치환 null과 해석적 F 불일치 · spline df {3,4,5} 민감도로 판정 뒤집힘 | — | 계측/검정력. β·T·seed 재검토 후 escalate. 벽 선언 아님. |

🧱의 내부 정합성이 이 설계의 힘이다: P+/P−는 Φ를 움직이는데(co-activation은 중요) B/X는 안 움직인다(어느 쌍이 disjoint인지는 무관) → 게이트가 보상하는 것의 정체가 **disjointness가 아니라 결합 세기**임을 한 실험 안에서 이중분리로 증명.

---

## 6. 한 줄 사전등록 예측 + 내 설계가 틀릴 가장 유력한 방식

**Freeze:** *"gated 기질에서 positive control P+/P−는 분리되지만(게이트 live), disjointness 대비의 partial-R²(arm | ncs(S_tot))는 라벨-치환 99th pct를 넘지 못하고 강도정합 Φ\*(B)−Φ\*(X′) CI는 0을 포함한다 — 게이팅은 co-activation 부호를 중요하게 만들지만 disjointness는 여전히 S_tot로 접는다 ⟹ 🧱 deeper closure."*

**가장 유력한 오류 (1순위): S_tot-곡률 누출로 인한 가짜 🟢.** gated 기질에서 Φ\*=f(S_tot)가 곡선이고 arm들이 서로 다른 S_tot 대역을 점유하면, S_tot 통제가 불충분할 때 곡률이 arm으로 새어 partial-R²를 부풀린다(구조가 아니라 곡선의 잔재). 이게 headline을 거짓 양성으로 만드는 가장 subtle하고 개연성 높은 실패다. **완화:** (a) reduced 모델을 선형이 아닌 ncs(S_tot, df=4) 스플라인으로 — arm은 매끄러운 S_tot 함수가 못 잡는 것만 주장 가능; (b) headline 주력을 **강도정합 B−X′**(구성상 S_tot 동일)로 두어 곡률 누출을 원천 차단; (c) df {3,4,5} 민감도가 판정을 뒤집으면 ⏳.

**2순위: 게이트 self-product 되먹임의 의존 제조.** `ẑ_a·ẑ_b`를 다시 a,b로 되먹이면 독립 구동에서도 진짜 a–b 결합을 만들 수 있다(산술의 인공물이지 통합 아님). 이미 지연 1(`t−1`)로 순간 self-product를 끊었고, zero-check가 이 인공물의 파수꾼이다 — Φ\*(S(0)) 인플레 = 인공물 발화 = VUID/⏳. 필요 시 게이트를 split-half copy로 계산해 완전 격리.

---

**비용:** T=65536 × 게이트(스텝당 sigmoid+곱, O(T·n) 무시가능) × arm ≈ 13개(gated: A·B·X·X′·N·R·Cperm·P+·P− + 선형 확인 P+·P− + V-gate S(0)·S(.15)) × 8 seed × K=32 ≈ H_9294의 ~1.8배 → **≈18분, 랩탑 $0 numpy**로 ≲30분 예산 내.

**등록 형태(design only):** HYPOTHESES.jsonl 1행 + `cards/H_9295_gated_vs_linear_coupling.md` 2 surface(`a_hypothesis_register`), verdict는 착지 시 `state/verdicts/` 동결 + ARCHITECTURE `psi-soma`/gate 노드 갱신(`research-verdicts-into-architecture`). 이 카드가 닫는 물음: H_9294 말미의 "구조가 기여하려면 결합이 비선형/게이팅이어야(TIMING만 뚫린 이유와 정합)" — 그 정확한 명제의 결정적 검정.