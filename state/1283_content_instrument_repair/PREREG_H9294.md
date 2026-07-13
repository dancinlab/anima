# H_9294 — 사전등록 (FROZEN 2026-07-14 · 데이터를 열기 前 커밋)

H_9293 이 남긴 **단 하나의 잔여**를 닫는다.

H_9293 판정(⏳ STRENGTH-CONFOUND)의 근본 원인은 통제군 X 에 있었다: X 는 **용량**(총 채널차원
4×8, W_RELAY)은 B 와 맞췄지만, 그 결과로 나온 **결합강도**는 맞추지 못했다 —
`S_tot(B) = 0.0685` vs `S_tot(X) = 0.0585`. 그래서 "B 가 X 를 이긴다" 는 사실이 disjointness 때문인지
그냥 B 가 더 세게 결합해서인지 갈리지 않았다.

**본 H 의 유일한 물음:** 결합강도를 **맞추고 나서도** B 가 X 를 이기는가?
(= disjointness 의 **잔차**가 존재하는가)

---

## §1 계측기 (H_9293 에서 그대로 · 무이동)

```
Φ* = Φ(RU(traj)) − E[Φ(RU(π_k(traj)))]   K=32 · Philox surrogate · signed lens · T=65536
estimator = stdlib iit4_faithful_phi (실제 정의 = RAW cross-cut 의 argmin ⇒ Φ=3c · H_9293 §0)
seeds = [4..11] (n=8, paired) — seed 3 은 계속 exploratory 격리
substrate/hypers = H_9260 이래 무이동
V-게이트 = V-PED · V-SPIKE · V-ZERO · V-SEED (H_9293 과 동일 · 하나라도 FAIL → INVALID)
```

## §2 강도 정합 — 두 경로를 **모두** 사전등록 (한 경로가 실패해도 다른 하나가 답한다)

### 경로 1 — X′ : W_RELAY 를 올려 X 의 S_tot 를 B 에 맞춘다

X 의 **유일한** 자유 파라미터 `W_RELAY` 를 격자 탐색해 `S_tot(X′) ≈ S_tot(B)` 가 되는 값
`w*` 를 찾는다 (격자 = W_RELAY ∈ {0.50, 0.55, …, 1.00}, 목적 = |S_tot(X′) − S_tot(B)| 최소,
seeds[4..11] 평균 기준 · **arm 간 Φ 를 보지 않고 S_tot 만으로 결정**).

> 이 튜닝은 **통제군을 강하게** 만든다 = B 에게 **불리한** 방향이다. 통제군을 유리하게 조정하는
> tune-to-green 과 정반대이며, 그래서 허용된다. (반대로 B 를 건드리는 것은 금지.)

**정합 게이트 (측정 前 동결):** `|S_tot(X′) − S_tot(B)| / S_tot(B) < 0.05` (5% 이내).
불충족 → ⏳ MATCH-FAIL, 경로 1 의 tier 미보고.

```
d′_s = Φ*(B; s) − Φ*(X′; s)      s ∈ [4..11] · paired · 90% CI
```

### 경로 2 — ANCOVA : 강도를 공변량으로 회귀하고 잔차를 본다 (튜닝 0)

전 arm(A·B·X·N·R·Cperm) × seeds[4..11] = 48 점에서
```
Φ*  ~  β0 + β1 · S_tot        (pooled OLS · arm 라벨 미사용)
resid(arm, s) = Φ* − 예측값
G-RESID = paired mean[ resid(B;s) − resid(X;s) ]  · 90% CI
```
강도가 우위를 **전부** 설명하면 두 arm 의 잔차는 같아야 한다(G-RESID CI 가 0 을 포함).

## §3 결정표 (양방향 결정적 · 위에서부터 첫 매칭)

| 경로 1 (d′ = B − X′) | 경로 2 (G-RESID) | Verdict |
|---|---|---|
| CI_low > P̄ | CI_low > 0 | **🟢-DIR (toy)** — 강도를 맞춰도 B 가 이긴다 ⇒ **disjointness 잔차 실재** · R6 의 핵심이 부분 회생 |
| CI_low > P̄ | 0 을 포함/음 | **⏳ SPLIT** — 두 경로 불일치 ⇒ 강도 정합 방식에 의존. 양쪽 보고, tier 미확정 |
| CI 가 P̄ 를 걸침 / CI_high < P̄ | 0 을 포함 | **🧱 STRENGTH-ONLY (종결)** — 강도를 맞추면 B 의 우위가 사라진다 ⇒ **B 의 이점은 전적으로 총 결합강도** · disjointness 의 기여 = 0 · content-relay 축의 disjointness 레버 **CLOSED** |
| CI_high < P̄ | CI_high < 0 | **🧱 STRENGTH-ONLY, 강함** — 강도 정합 후 X′ 가 오히려 B 를 **이긴다**(공유버스가 더 통합적) |
| 그 외 | — | **⏳ power-limited** — MDE 보고 · 벽 선언 금지 |

## §4 사전등록 예측 (데이터 미개봉)

> **🧱 STRENGTH-ONLY.** H_9293 에서 G5-SHAPE 가 **역방향으로 결정적**이었다(B 의 adjacency share 가
> X 보다 **낮다**, −0.0080). 즉 B 의 채널은 간선-특이 정보를 더하는 게 아니라 **대각 정보**를 더한다.
> 강도를 맞추면 남을 것이 없다고 예측한다. `d′` 의 90% CI 가 P̄ 를 걸치거나 아래로 떨어지고,
> G-RESID 는 0 을 포함할 것이다.

**틀릴 최빈 경로:** W_RELAY 만으로 S_tot 를 올리면 X′ 의 **형태**(s_adj)도 함께 변해, 강도는 맞췄지만
"같은 형태의 더 센 X" 가 아니라 "다른 arm" 이 되어버릴 수 있다 — 그래서 경로 2(ANCOVA, 튜닝 0)를
**동시에** 사전등록했고, 두 경로가 갈리면 정직하게 ⏳ SPLIT 을 보고한다.

**모니터(게이트 아님):** X′ 의 s_adj · A 를 뺀 4-arm 회귀 민감도 · w* 값.
