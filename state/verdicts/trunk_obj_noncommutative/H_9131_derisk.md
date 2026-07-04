# H_9131 ② non-commutative target STEP-0.5 de-risk verdict — 🧱 FALSIFIED-DPI-ceiling — FROZEN 2026-07-05

optimizer-robust closed-form lstsq R²(a5c32ced, $0 mini numpy=DIRECTIONAL·negative 방향). STEP-0의 유일 크랙(REWARDS-RECOMB이 model-based earned서 optimizer-fragile SGD 0↔Adam +0.24) 해소.

## 3-arm held-out R² (frozen bar δ=0.10 · seeds {7,4302,4303} · K=32 · verbatim)
| seed | bind | additive(total-order f(a)−f(b)) | shuffle | sym_ref(z_a+z_b) | gap b−add | gap b−sf |
|---|---|---|---|---|---|---|
| 7    | 0.2726 | 0.4844 | 0.0567 | 0.0677 | −0.2118 | +0.2159 |
| 4302 | 0.3047 | 0.4935 | −0.0599 | 0.0504 | −0.1888 | +0.3646 |
| 4303 | 0.1843 | 0.5178 | −0.0409 | 0.0607 | −0.3334 | +0.2252 |
n_pass(gap_bind−additive≥δ ∧ gap_bind−shuffle≥δ, 2/3) = **0**. gap_bind−additive 3 seed 전부 음수 = bind가 강 total-order baseline 못 이김.

## 크랙 해소
STEP-0 +0.24 = 약한 baseline(sym_ref z_a+z_b 대칭, 0.06) 착시 = bind(0.27)−0.06=+0.21 가짜 PASS. 정직한 total-order additive f(a)−f(b)(0.48) 쓰면 bind −0.24로 짐 = "반대칭 bilinear가 additive subsume" 함정 확인. closed-form lstsq라 optimizer 무관.

## 강건성
용량 스윕: 전 앵커 용량서 bind held-out 우위 max +0.009(≪δ)=FALSIFIED 용량 artifact 아님. train_bind 0.65≫held 0.25=overfit(암기). intransitive cycle_frac 0.092≫total-order-null 0 실재하나 held-out서 암기이지 재조합 아님. leak-check 전수통과(조합-disjoint·feature-disjoint·held R²≠1.0·shuffle 저값).

## 결론
DPI 메타법칙 target 축서도 유지 → census (d) trunk-objective family CLOSED → G1 재조합벽 = readout·lane·decode·objective·target 전수 falsify = 진짜 능력천장 방향(303M byte-LM trunk). STEP-1 GPU 미정당화(신호 소멸, ~1 H100-day 절약). 유일 잔여 저비용 레버=coverage-density(GPU 무관). reopen=새 저비용 target/coverage 축이 additive baseline 통제하 이기면.
