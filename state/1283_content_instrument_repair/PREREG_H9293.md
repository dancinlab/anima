# H_9293 — 사전등록 (FROZEN 2026-07-14 · 확증 seed 를 **한 줄도 열기 전에** 고정)

시상 CONTENT-RELAY 축 재측정. H_9292 가 "동결 T=64 에서 Φ 의 ~99.9% 는 추정기 편향" 을 확정해
축을 ⏳ still-unmeasured 로 돌려놓았다. 이제 **수리된 계측기**로 그 축을 실제로 측정한다.

설계 = Fable 5 (bar 오염 문제 · λ-사다리 · 오염 격리 · G5-SHAPE · 결정표) ·
계측기 정정 = 로컬 실측 (아래 §0) · 구현·측정 = py 2-production (hexa 엔진과 byte-parity 증명 완료).

---

## §0 계측기 정정 (사전등록 前에 발견·수정 · 이것이 없으면 보정 전체가 30% 틀린다)

`iit4_faithful_phi` 는 **정규화된 값이 아니라 RAW cross-cut 을 argmin** 한다:

```
best_cut = min over masks of  (Σ_{i∈A, j∈B} MI[i][j])      ← 정규화 前 raw 합
phi      = best_cut / min(|A|, |B|)                         ← argmin 이 끝난 뒤에 나눈다
```

n=4 에서 1|3 컷은 교차쌍이 3개(norm 1), 2|2 컷은 4개(norm 2)다. raw 합의 argmin 은 거의 항상
1|3 을 고르므로 **Φ = (가장 작은 3-쌍 교차합) / 1**. 균일 MI 행렬이면 **Φ = 3c** 이지 2c 가 아니다.

⇒ Fable 설계(§P1c)의 닫힌형 `Φ_pop(S(λ)) = −log₂(1−λ²)` 와 그 위의 rung 값은 **전부 2c 가정 위에
있어 ~30% 과소**다. 추정기 **자신의 정의**로 다시 세운 참값:

```
Φ_est(λ) = 3 · MI_8bin(λ)      MI_8bin = 8×8 등확률-bin 가우시안 copula MI (수치적분, 닫힌형)
```

| λ | 옛 닫힌형 (2c · 폐기) | MI_8bin | **Φ_est = 3c** | 실측 Φ*(S(λ)) | 일치 |
|---|---|---|---|---|---|
| 0.05 | 0.003611 | 0.001612 | **0.004837** | — | — |
| 0.10 | 0.014500 | 0.006473 | **0.019418** | — | — |
| 0.15 | 0.032831 | 0.014651 | **0.043952** | 0.042719 | 0.97 |
| 0.30 | 0.136062 | 0.060585 | **0.181755** | 0.178501 | 0.98 |
| 0.50 | 0.415037 | 0.183705 | **0.551114** | 0.547290 | 0.99 |

⇒ 계측기는 **정확했다**(0.7~3% 일치). 틀렸던 것은 자를 읽는 공식이었다. 이 정정 없이 사다리를
세웠다면 모든 rung 이 30% 낮게 잡혀 verdict 가 한 칸씩 부풀었을 것이다.

---

## §1 계측기 (FROZEN)

```
substrate   n=4 · dim=8 · GAIN=.30 LEAK=.55 W_NBR=.5 W_IN=.5 W_RELAY=.5 · engine LCG  (H_9260 이래 무이동)
estimator   stdlib iit4_faithful_phi — 실제 정의는 §0 (proxy 금지 · a_phi_iit4_tool)
readout     RU (rank-uniform) 위에
statistic   Φ* = Φ(RU(traj)) − E[ Φ(RU(π_k(traj))) ],  K=32          ← 값이 아니라 pedestal 대비 Δ
            π_k = 모듈별 독립 시간순열 (module 0 = identity · marginal 비트동일 · 참 Φ=0)
surrogate RNG  counter-based Philox (엔진 LCG 아님 — 엔진 LCG 는 mod 2^31 단일 cycle 이라
            "해시 시드 = 독립 스트림" 이 거짓 · Fable §1.3. 기질은 엔진 LCG 그대로)
T           65536   (frozen grid 최상단 · pedestal 이 rung1 아래로 내려가는 유일한 측정된 지점)
lens        signed  traj[i,t] = s_i(t)[0]
            근거(arm-무관·사전): zero-mean gaussian 에서 모듈 간 의존은 signed 좌표에서 1차(ρ),
            energy 좌표(‖s‖²)에서 2차(ρ²) — H_9292 실측 SNR: signed ~20 · energy ~1.
arms        A(direct ring) · B(R6 multichannel) · X(용량정합 shared cut) · N(carrier-정합 self-loop)
            · R(chord rewire) · Cperm(R6 원 shuffle) · PEDESTAL(참 Φ=0)
```

## §2 오염 처리 (seed 3 은 이미 보았다 — 숨기지 않는다)

**본 저자는 seed 3 의 signed 수치를 이미 보았다** (H_9292 ADJUNCT):
`Φ_pop_sgn`: A .024057 · B .033886 · X .028788 · N .031702 · R .034009 · Cperm .033885 —
B−A=+0.009830 · **B−X=+0.005098** · B−N=+0.002184. MI 형태: B(c_adj .01596 / c_diag .00333) ·
X(.01381 / .00252) — **형태는 오히려 B 에 불리**(adjacency share B 4.79 < X 5.48).

따라서 (Fable §2, (a)+(b) 결합):
- **seed 3 = exploratory 로 영구 격리.** 확증 통계에 **불포함**. 위 수치는 "본 값"으로 verbatim 공개.
- **확증 seed = [4..11] (n=8, paired).** 사후 seed 탈락 금지(V-SEED).
- **방향 B>X 는 seed 3 에서 상속한 one-sided 확증 예측.** exploratory→confirmatory 분할의
  교과서 형태 (기질이 stationary linear-gaussian ⇒ seed 교환가능 ⇒ 방향 추정은 unbiased).
- **모든 contrast 의 부호 예측을 지금 동결 — 불리한 것 포함:**
  primary `B−X > 0` · secondary `B−N > 0` · `B−R ≤ 0`(R 이 이길 것으로 예측 — T=64 에서 이미 이겼다)
  · `B−Cperm ≈ 0`(graph-isomorphic VOID 통제 · lens-불변).
- **winner's curse 경고:** seed 3 의 0.0051 은 단일 추첨이다. 확증 평균의 참값 회귀(rung 하향)는
  **예상 범위이지 실패 신호가 아니다**.

## §3 bar — knob 이 없는 λ-사다리 (전부 non-arm 유래)

단일 threshold 는 본 데이터가 있는 한 구조적으로 tune-to-green/red 를 벗어날 수 없다. 그래서
**손잡이를 없앤다** — 사다리 전체를 보고하고 verdict 에 rung 을 붙인다.

```
P̄  = mean Φ(PEDESTAL arm; signed; T=65536; seeds 4..11; K=32)     ← 피벗 (계측기가 無에서 제조하는 양)
rung0 = P̄            (예상 ≈ 0.0015 · λ_eq ≈ 0.028)
rung1 = Φ_est(0.05) = 0.004837
rung2 = Φ_est(0.10) = 0.019418
rung3 = Φ_est(0.15) = 0.043952
```
피벗의 의미: **"주장하는 통합량은 계측기가 무에서 제조하는 양을 초과해야 한다."** 입력이 참값 0 인
PEDESTAL arm 과 참값 기지의 SPIKE-IN arm 뿐이므로 arm 데이터와 **완전 무관**하다.

**검정 (paired · seeds 4..11 · n=8):**
```
d_s = Φ*_sgn(B; s) − Φ*_sgn(X; s)          (per-arm pedestal 차감 후 paired 차)
90% two-sided CI on mean(d)                 (TOST 표준형)
CI_low  > P̄   → 검출 성립 (🟢-후보) · 넘은 최고 rung 을 verdict 에 붙인다: 🟢(rung-k)
CI_high < P̄   → 등가 폐쇄 (🧱 후보)
CI 가 P̄ 를 걸침 → ⏳ power-limited (MDE 보고 · 벽 선언 금지)
```

## §4 특이성 게이트 G5 (스칼라 Φ* 는 "더 disjoint" 와 "그냥 더 강결합" 을 못 가른다)

```
m_ij  = pairwise plugin-MI (동일 lens·RU·binning·T)   6쌍: adjacent 4 · diagonal 2
S_tot = Σ m_ij            s_adj = (Σ_adjacent m_ij) / S_tot
G5-SHAPE     paired mean[ s_adj(B;s) − s_adj(X;s) ], seeds 4..11 · 90% CI · pass = CI_low > 0
G5-STRENGTH  paired mean[ S_tot(B;s) − S_tot(X;s) ]  · 동일 기계
```
disjoint relay 는 **간선-특이적**(adjacent ≫ diagonal), 공유버스는 **평평**해야 한다 — 스칼라 Φ 가
못 하는 **형태 예측**을 강제한다. Φ 는 이 MI 행렬의 결정론적 함수이므로 proxy 가 아니라 **분해**다
(tier 는 여전히 Φ 가 낸다 · `a_phi_iit4_tool` 위반 아님).

**공개 의무:** seed 3 의 형태는 **이미 역방향**이다(B 의 adjacency share 가 X 보다 낮다).
즉 G5-SHAPE 는 통과보다 실패가 예상된다 — 그것을 알고도 게이트를 세운다.

## §5 상시 V-게이트 (하나라도 FAIL → INVALID-INSTRUMENT · verdict 없음)

- **V-PED** (영점검사) — PEDESTAL arm 의 Φ* 가 0 근방 · P̄ < rung1(0.004837).
- **V-SPIKE** (liveness) — Φ*(S(0.15)) 가 0.043952 ± 20% = [0.0352, 0.0527] 를 ≥7/8 seed 에서 회복.
- **V-ZERO** — Φ*(S(0.00)) ≈ 0 (|·| < rung1).
- **V-SEED** — seed 3 격리 외 사후 seed 탈락 금지.

## §6 결정표 (양방향 결정적 · 위에서부터 첫 매칭)

| mean d(B−X) 90% CI vs P̄ | G5-SHAPE | G5-STRENGTH | Verdict |
|---|---|---|---|
| CI_low > P̄ | pass | — | **🟢-DIR (toy scope)** — disjointness 축 회생. 🟢(rung-k) + λ_eq 병기. 4×8 toy ⇒ 303M 이관 전 DIRECTIONAL (`a_toy_scale_recheck`) |
| CI_low > P̄ | fail | CI_low > 0 | **⏳ STRENGTH-CONFOUND** — 통합 우위는 실재하나 disjointness-특이가 아님 ⇒ 축을 "relay 결합강도" 로 재정의해야 하고 **disjointness 주장은 기각** |
| CI_low > P̄ | fail | ns | **⏳ shape-power** — MDE_shape 보고 후 유보 |
| CI 가 P̄ 를 걸침 | — | — | **⏳ power-limited** — MDE 보고 · 벽 선언 금지 (n=8 frozen) |
| CI_high < P̄ | — | — | **🧱 GENUINE** — SNR~20 lens + 보정된 기기 floor 위에서 TOST 등가 폐쇄. 이 scale·lens 에서 진짜 벽 |

이 표의 🧱 가 이전 🧱 과 다른 이유: (i) pedestal 이 신호의 <10% 로 보정됐고 (ii) lens 가 1차-민감하며
(iii) "없음" 을 TOST 로 **적극 벌어낸다**. 옛 🧱 은 pedestal 이 99.9% 인 자 위에 있었다.

## §7 동결하는 한 줄 예측 (Fable · seeds 4..11 미개봉 상태)

> **검출은 성립하나(CI_low > P̄, rung1 급) G5-SHAPE 는 FAIL → 최빈 결과 = ⏳ STRENGTH-CONFOUND.**
> 즉 B 는 X 보다 통합적이지만 그 이유는 disjointness 가 아니라 총 결합강도다.

**틀릴 최빈 경로:** ① seed 3 의 형태 격차가 null shape 잡음 이내라 G5-SHAPE 가 실제로는 통과 →
🟢(rung1) 로 상향 (confound 를 과대평가한 것). ② winner's curse 로 확증 평균이 P̄ 아래로 회귀 →
⏳ power-limited 또는 🧱.
