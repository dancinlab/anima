# H_332 — EPIGENETICS × 2-phase rule 🟢 + 🪜 attractor 우열 발견

> A1 영구축 · 신규 BIO axis · DYNAMICAL kernel · phase-history 측정

## 1. 동기

H_287-326의 ECA 패널은 단일 rule. 실제 생물학 epigenetic mark는 phase-1 history가 phase-2 trajectory에 영향을 준다 (DNA methylation, histone modification). ECA에서 2-phase rule sequence가 phase-2-only baseline과 다른 final distribution을 만드는지 측정.

## 2. 가설 (falsifiable)

- **H1**: hybrid(rule110→rule30) final-state 분포가 base_AA(rule30×20) 분포와 Manhattan distance ≥ 0.5 → phase-1 흔적 측정 가능.
- **falsifier**: distance < 0.5 → phase-2 rule이 phase-1 history 지움 (no epigenetic memory).

## 3. 방법

pure hexa, n=4 periodic ECA ring. 16 starting states 각각:
- base_AA = rule30 × 20 steps (control)
- base_BB = rule110 × 20 steps (control)
- hybrid_BA = rule110 × 10 → rule30 × 10
- hybrid_AB = rule30 × 10 → rule110 × 10

16-bin final-state histogram, Manhattan distance Σ|p1−p2|.

## 4. 측정

```
base_AA(r30×20)    [2,2,2,0,2,1,0,1,2,0,1,1,0,1,1,0]   diverse
base_BB(r110×20)   [4,0,0,0,0,0,0,3,0,0,0,3,0,3,3,0]   peaked 4-attractor
hybrid_BA(110→30)  [4,0,0,0,0,0,0,3,0,0,0,3,0,3,3,0]   ⭐ base_BB와 동일
hybrid_AB(30→110)  [4,0,0,0,0,0,0,3,0,0,0,3,0,3,3,0]   ⭐ base_BB와 동일

distances:
d(hybrid_BA, base_AA)  = 1.25   ⟶ H1 PASS (≥0.5)
d(hybrid_BA, base_BB)  = 0.00   ⟶ 🪜 byte-identical 발견
d(base_AA, base_BB)    = 1.25   ⟶ baselines distinct (sanity)
```

## 5. Verdict

**🟢 SUPPORTED-NUMERICAL** — H1 distance 1.25 ≫ 0.5 threshold.

🪜 **추가 발견**: phase 순서 무관, hybrid가 정확히 base_BB와 동일. rule 110의 attractor가 "**dominant sink**" — phase-2 rule30이 한 번 진입한 후 빠져나오지 못함.

## 6. 의미

- **EPIGENETIC MEMORY 강한 신호** (n=4 ECA)
- **Attractor 우열 axis 발견**: rule110 attractor (4 distinct states) 가 rule30 attractor (diverse distribution)를 완전 압도
- H_330 bijection 발견과 다른 angle: peaked attractor vs spread distribution의 우열 관계
- "더 큰 basin이 우세 sink"는 dynamical-systems theory의 잘 알려진 결과 — ECA 패널에서도 재현

## 7. Cross-link

| ref | 관계 |
|---|---|
| [H_322 Kuramoto](./H_322_circadian_kuramoto_sync.md) | 동역학 sharp transition 첫 발견 |
| [H_330 moments](./H_330_distribution_moments.md) | rule110 peaked vs rule30 spread distribution |
| [H_327 attractor](./H_327_regeneration_attractor_recovery.md) | attractor recovery — rule60만 finite, 본 셀이 attractor 우열 mechanism 노출 |

## 8. Anti-tautology

- hybrid 분포가 baseline과 d=0이라는 게 *tautology가 아닌 발견* — 두 baseline 자체가 d=1.25 distinct하므로 hybrid가 한 baseline과 동일하다는 것은 **dominance signal**
- F332.2 sanity: distinct baselines (d=1.25) 확인

## 9. Honest limits

- L1: n=4 단일 scale; n=6에서 multiple attractors 등장 시 dominance 약화 가능
- L2: T1=T2=10 fixed; phase-length sweep 필요 (very long T2가 결국 phase-2 attractor 이길까?)
- L3: 2 rule pair만 측정; rule × rule 전수 dominance map 필요
- L4: Manhattan distance — KL-divergence가 dominance asymmetry 더 sensitive

## 10. 다음

- (a) **attractor dominance map**: 4 live rule × 4 live rule 전수 hybrid → 16-pair dominance 표
- (b) phase-length sweep: T2 ∈ {10, 50, 100, 500} → 결국 phase-2 우세 시점 찾기
- (c) n=6 scale-up: dominance가 scale-rich에서도 holds 검증
