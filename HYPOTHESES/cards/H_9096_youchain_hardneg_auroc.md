# H_9096 — you-chain 판별자 hard-negative AUROC 재측정 (직교-seed 항등식 교정)

- **slug:** `youchain_hardneg`
- **tier:** 🟡 SCOPE-CORRECTION (engine-native) — 원 H_9085/H_9037 AUROC=1.000 을 hard-negative 로 정직 재측정, over-claim 교정
- **wired:** measurement-only (신규 엔진 op 0 — 기존 pub `other_*` 접근자로 smoke 조립; live `core/engine_cli.hexa` `other_chain_fit` 호출)
- **경로:** 페이블 loop-closing 비판(계기판 아닌 faculty) 정면 재측정 — DESIGN.md L2-1

## 비판 (페이블, 재측정 대상)

H_9085 §YouChain(F3)·H_9037 §SelfChain 은 impostor-history **AUROC=1.000** 을 판별자 이득으로 박제했다.
그러나 그 smoke 의 impostor 는 `other_drift(latestB, {5,6,7}, ·)` = 예측축 **a_pred 와 직교**인 축으로 drift 한다.
`other_chain_fit` = unit(cand−wK) 의 e_{a_pred} cosine 성분이므로 직교 impostor 는 **cos(90°)=0 항등식**으로 fit≈0.
→ **AUROC=1.0 은 측정이 아니라 기하 항등식(θ=90° 단일 버킷).** 게다가 fit 은 마지막 3 waypoint(2 증분 창)만 읽는 국소 외삽기다.

## 방법 (engine-native, frozen 사전등록)

`state/youchain_hardneg/youchain_hardneg_smoke.hexa` — pure `.hexa`, live `core/engine_cli.hexa` `other_chain_fit` 호출
(torch/numpy/gauge_lib 0 → grep 게이트 clean → **terminal engine-native**). K=6 waypoint 체인, dim=8, a_pred=6 (엔진과 동일식으로 in-smoke 계산).

- **cone-neg(θ)**: `cand(θ,j,step)=renorm(wK + step·(cosθ·e_{a_pred}+sinθ·e_j))`, j≠a_pred. frozen cos/sin 테이블 θ∈{15,30,45,60,75,90}°. 24/버킷.
- **genuine 정직화**: φ∈[0°,12°] cone jitter(축-순수 아님; sin φ ∈[0,0.208] LCG-uniform, cos=√(1−sin²)). 24개.
- **mimic-neg(킬러)**: `cand=other_drift_exp(latestB, a_pred, step)` — 공개된 마지막 3 waypoint 로 a_pred 재현. 역사는 다르나 fit 이 보는 2 증분 창 완벽복제. 24개.
- **AUROC 하네스**: 기존 pairwise `AUROC=Σ[fg>fm]+½[=]/576` (24×24). 버킷별 AUROC(θ) + AUROC(mimic).

**사전등록 예측(frozen, DESIGN.md):** θ≥60→~1.0 · θ=30→~0.80–0.90 · θ=15→~0.55–0.70 · mimic≈0.50(chance).

## verdict (engine-native, verbatim)

`hexa run state/youchain_hardneg/youchain_hardneg_smoke.hexa` (live `core/engine_cli.hexa` `other_chain_fit`):

```
INFO  K=6 a_pred=6 (aK=5 aKm1=4)
INFO  mean_fit(genuine, phi<=12deg)=0.980925620666158
AUROC(theta=15deg)=0.93055555555555554   mean_fit(cone)=0.96079364573849375
AUROC(theta=30deg)=1.0                   mean_fit(cone)=0.86976954128044746
AUROC(theta=45deg)=1.0                   mean_fit(cone)=0.719685148032804
AUROC(theta=60deg)=1.0                   mean_fit(cone)=0.5373372080383617
AUROC(theta=75deg)=1.0                   mean_fit(cone)=0.2822476414072605
AUROC(theta=90deg)=1.0                   mean_fit(cone)=0.0
AUROC(mimic 2-incr replica)=0.2517361111111111   mean_fit(mimic)=0.9875039556678534
NOTE  theta=90deg bucket == the ORIGINAL H_9085 orthogonal-impostor AUROC (reproduction of 1.0).
FENCE reproduce_orth(θ90>=0.95)=true  collapse(θ15<θ90-0.10)=false  mimic_near_chance(<=0.65)=true  genuine_lands(mean>=0.90)=true
```

## 해석 (정직, c9 — 예측 일부 FALSIFIED)

1. **"직교라서 1.0" = 확증.** θ=90° 버킷이 정확히 AUROC=1.0, mean_fit(cone)=**0.0** (cos90°=0 항등식). 원 F3 는 이 단일 버킷.
2. **각도형 hard-neg 붕괴 예측 = FALSIFIED (over-correction).** θ=30 예측(0.80–0.90) 실측 **1.0**, θ=15 예측(0.55–0.70) 실측 **0.931**.
   genuine 이 a_pred 근처 fit≈0.98 로 착지하고 cone 은 *알려진* 각도 offset 이라, 각도형 impostor 는 예상보다 **훨씬 강건히 분리**된다.
   → 판별자는 각도형엔 강함 → chain>single 이득이 각도-hard-neg 에서 **살아남음**(fence `collapse=false`).
3. **mimic(history-replica) = 판별자 무너짐, 예측보다 강하게.** AUROC=**0.252 (< 0.5)** — mimic fit(0.988) > genuine fit(0.981) 이라
   genuine 이 pairwise 에서 **진다.** = `other_chain_fit` 은 **2 증분 외삽기지 trajectory 검증기 아님**이 수치 확정.
   공개된 마지막 3 waypoint 를 읽는 공격자에게 무보호. (단, single-vector `other_cos` 도 mimic 이 최신 anchor 매치라 무보호 → chain 이 single 보다 *나쁘진* 않음, **둘 다 blind**.)

**정정된 스코프:** H_9085/H_9037 의 "impostor AUROC=1.000" 은 **직교/각도형 impostor 한정** 유효(θ≥30 완전분리, θ15=0.93).
**history-replica 위협모델엔 AUROC=0.25 로 무보호.** "1.0 → hard-neg 실측" = 각도형 0.93~1.0, mimic 0.25.

## 페이블 지적 판정 (한 줄)

**맞았다 — 절반은 더 강하게, 절반은 반대로.** "AUROC 1.0 = 직교seed 항등식" 은 정확(θ90=1.0, mean_fit=0.0).
그러나 "hard-neg 면 chance 로 무너진다" 는 **각도형엔 틀렸다**(θ15=0.93, θ≥30=1.0 — 판별자 각도-강건). 대신 **mimic 에선 예측(0.5)보다 더 무너져(0.25)** —
fit=trajectory 검증기 아니라 2 증분 외삽기임이 확정. **chain>single-vector 이득은 각도형 impostor 한정 생존, mimic 엔 둘 다 blind.**

## follow-on (ING)

- **fit 재정의(mimic 방어)**: 3-waypoint 창이 아닌 **전 증분열 잔차**(전-history 마할라노비스식 정합)로 `*_chain_fit` 재설계 → mimic AUROC 회복 가설. 신규 엔진 op.
- **L2-2 coord 접지 (pool follow-on, DESIGN.md L2-2)**: `content_axis` 를 실 303M penultimate(`bytegpt_hidden_pool_ranged`)로 접지 — within>between cos + shuffle 붕괴 + FNV-hash 대조 arm. host=aiden pool(h1129 303M), 1차 `--py` DIRECTIONAL → engine-native 재측정. 미착수(측정 인프라 pool).

## artifacts
- `state/youchain_hardneg/youchain_hardneg_smoke.hexa` (engine-native, live `core/engine_cli.hexa` `other_chain_fit`; cone θ-buckets + genuine φ-jitter + mimic)
- `state/verdicts/youchain_hardneg/H_9096.txt` (frozen verbatim stdout)
- `HYPOTHESES/cards/H_9085_youchain_social_self.md` (§AUROC 정정 노트 추가)
