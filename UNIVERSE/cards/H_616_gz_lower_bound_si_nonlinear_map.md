# H_616 — `gz-lower-bound-SI-nonlinear-map` (H_348 F-2 mapping-artifact recovery test)

> 축 E (SAVANT) round 2 · 2026-05-30 · UNIVERSE H 신설.
> Predecessor: H_348 (`golden-zone-lower-bound-SI`) 🟡 PARTIAL — F-1 (SI>3 @ GZ_LOWER) PASS, F-2 (peak @ GZ_LOWER) FAIL (affine map 하 SI(I) monotone).
> 외부 anchor: `HEXAD/SAVANT/savant_phi.hexa` (4-domain capacity-bounded SSOT) · `UNIVERSE/H_348_golden_zone_lower_bound_SI.md` §7 C3-4 + §9 Next (round-2 lever 명시).

## 0. 1줄 요약 (TL;DR)

H_348 §7 C3-4 가 남긴 escape — "inhibition I → gain affine 매핑은 design choice; 비선형 매핑(1/I, sigmoid)을 채택하면 SI peak 가 GZ_LOWER 로 이동할 가능성 잔존, F-2 falsification 은 affine 한정" — 을 정밀 검정. 동일 endpoint (gf(0)=10, gf(1)=1) 를 공유하나 곡률만 다른 **3 매핑 (AFFINE baseline · RECIPROCAL 1/I front-load · SIGMOID GZ_LOWER 중심 S-curve)** 으로 SI(I) sweep 의 argmax 위치를 재측정. **3/3 seed 에서 세 매핑 모두 argmax(SI) = I→0 boundary (I=0.05), GZ_LOWER window [0.16232, 0.26232] 안 0/3** — peak 위치가 **mapping-independent**. **🔴 FALSIFIED** — H_348 의 F-2 falsification 은 affine artifact 가 아니며, SI(I) 의 I→0 단조 증가는 capacity-bounded savant_phi substrate 의 intrinsic property. GZ_LOWER 는 *SI peak* 가 아니라 *SI>3 threshold boundary* (H_348 F-1) 임이 deterministic 하게 확정.

이로써 SAVANT 축 E 의 round-2 follow-up 5/5 (H_612←H_349 · H_613←H_350 · H_614←H_351 · H_615←H_347 · **H_616←H_348**) 완결, 10-H 측정자 SET 닫힘.

## 1. Hypothesis

**주장 (F-2 recovery)**: H_348 의 affine map `gf = 1 + (1-I)·9` 이 산출한 SI(I) monotone-decrease 는 *매핑 선택의 artifact* 이며, inhibition I → gain_focus 를 **비선형** (front-loaded reciprocal 또는 GZ_LOWER 중심 sigmoid) 으로 바꾸면 SI(I) 의 단봉 peak 가 GZ_LOWER (= 0.21232) ±0.05 window 안으로 이동한다.

- 동기: H_348 §9 Next ("H_351 은 다른 매핑(1/I, sigmoid)에서 GZ_LOWER 가 peak 가 되는지 확인 — PASS 면 H_348 F-2 falsification 이 metric 선택 문제로 재해석 가능") + §7 C3-4 가 직접 지목한 round-2 lever.
- 강한 형태: ≥1 개 비선형 매핑에서 argmax(SI over 9-point I grid) 가 [0.16232, 0.26232] 안, ≥2/3 seed.

## 2. 사전등록 falsifier (pre-registered, 측정 전 동결)

| ID | 조건 | 판정 |
|----|------|------|
| **F-RECOVER** | ≥1 NON-LINEAR 매핑 (RECIPROCAL ∨ SIGMOID) 의 argmax(SI) ∈ GZ_LOWER window, ≥2/3 seed | recovery 성립 (F-2 = mapping artifact) |
| **F-INVARIANT** | 3 매핑 ALL argmax(SI) = I→0 boundary (GZ_LOWER window 밖), 3/3 seed | 🔴 FALSIFIED (peak mapping-independent) |

**verdict_rule**
- recovery = F-RECOVER (≥1 비선형 매핑 ≥2/3 seed window 안) → H_348 F-2 가 affine artifact 였음
- **FALSIFIED** = F-INVARIANT (세 매핑 모두 boundary peak) → F-2 mapping-independent

## 3. Method

### 3.1 substrate + SI metric (H_348 동일)

`HEXAD/SAVANT/savant_phi.hexa` 4-domain capacity-bounded 모델 (CALENDAR/MUSIC/ART/MEMORY, d=6, Σ gain ≤ SV_CAPACITY=11.5). SI = `max(domain_phi) / min(domain_phi)`, `phi_module(v) = Σ|v[j]|^1.5 / d` (Newton-iteration sqrt 8-step). primitive 는 import 회피 위해 in-file 복제 (SSOT 마커).

### 3.2 inhibition I → gain_focus — 3 매핑 (endpoint 공유, 곡률만 상이)

세 매핑 모두 `gf(0)=10` (full release), `gf(1)=1` (balanced) 로 endpoint 고정 — endpoint 차이 confound 제거, 오직 *곡률* 효과만 분리.

| 매핑 | 식 | 곡률 |
|------|------|------|
| **AFFINE** (H_348 baseline) | `gf = 1 + (1-I)·9` | linear |
| **RECIPROCAL** (1/I front-load) | `gf = 1 + 9·(1-I)/(1+8·I)` | small-I 에서 급강하 (front-loaded) |
| **SIGMOID** (GZ_LOWER 중심) | `gf = 1 + 9·norm(L(I))`, `L(I)=1/(1+exp(12·(I-0.21232)))` | GZ_LOWER 중심 S-curve, [l(1),l(0)]→[1,10] renorm |

`gain_rest = (SV_CAPACITY - gf) / 3`.

### 3.3 sweep grid (H_348 동일 9-point)

```
I ∈ {0.05, 0.10, 0.15, 0.21232 (GZ_LOWER ★), 0.25, 0.36788 (GZ_CENTER 1/e), 0.50, 0.75, 0.95}
seed ∈ {42424, 91919, 77777}   (savant_phi T1/T2/T3 stim, H_348 동일)
```

각 (매핑, I, seed) 에서 4-domain phi → SI_phi. 매핑별 argmax(SI over grid) 계산 후 GZ_LOWER window 포함 여부 판정.

### 3.4 runner

`UNIVERSE/state/h616_gz_lower_si_nonlinear_map_2026_05_30/run_h616.hexa` — 단일 hexa, H_348 `probe_h348_gz_si.hexa` 의 substrate 부 byte-identical, 매핑부 3-way 확장. `hexa run`, wall < 2s, $0 mac-local, deterministic.

## 4. Measurement (2026-05-30, mac-local $0)

verbatim → `state/h616_gz_lower_si_nonlinear_map_2026_05_30/result.txt` (= `.verdicts/616_gz_lower_bound_si_nonlinear_map/h616_verify.txt`).

### 4.1 SI(I) argmax per mapping (3/3 seed 동일 패턴)

| 매핑 | seed 42424 | seed 91919 | seed 77777 | argmax I | window? |
|------|-----------:|-----------:|-----------:|---------:|:-------:|
| **AFFINE** | SI@0.05=7.829 (max) | 7.537 (max) | 9.841 (max) | **0.05** | ✗ |
| **RECIPROCAL** | SI@0.05=3.241 (max) | 3.243 (max) | 4.008 (max) | **0.05** | ✗ |
| **SIGMOID** | SI@0.05=7.575 (max) | 7.301 (max) | 9.515 (max) | **0.05** | ✗ |

GZ_LOWER (I=0.21232) 에서의 SI 값: AFFINE 4.23/4.18/5.25 · RECIPROCAL 1.59/1.65/1.99 · SIGMOID 2.47/2.50/3.05 — 어느 매핑도 GZ_LOWER 가 local-max 아님 (모두 I=0.05 가 global max).

### 4.2 곡률 효과 관찰 (mechanism 단서)

- **RECIPROCAL**: gf 가 small-I 에서 급강하 → 전 grid 에서 SI 크게 압축 (max 3.24~4.01), 그러나 argmax 여전히 I=0.05. 추가로 high-I tail (I=0.75/0.95) 에서 SI 재상승 (gf→1, capacity 재분배) → non-monotone 이나 secondary bump 가 GZ_LOWER 아님.
- **SIGMOID**: GZ_LOWER 중심 S-curve 라 GZ_LOWER 부근 gf 가 mid-value (5.85) — 의도적으로 peak 를 GZ_LOWER 로 끌어당기는 설계임에도, SI(I) 는 여전히 I=0.05 에서 global max + high-I tail bump. S-curve 의 중심을 GZ_LOWER 에 놓아도 SI peak 는 이동하지 않음.

### 4.3 Aggregate

```
RECIPROCAL argmax in GZ_LOWER window: 0/3 seeds
SIGMOID    argmax in GZ_LOWER window: 0/3 seeds
```

**F-RECOVER 0/2 매핑. F-INVARIANT 3/3 seed × 3/3 매핑 trigger.**

## 5. Verdict — 🔴 FALSIFIED (SI peak at I→0 boundary mapping-INDEPENDENT)

- **F-RECOVER FAIL**: 두 비선형 매핑 (RECIPROCAL, SIGMOID) 모두 0/3 seed 에서 argmax(SI) 가 GZ_LOWER window 밖. H_348 §7 C3-4 가 남긴 "비선형 매핑이면 peak 가 GZ_LOWER 로 이동" 가설 기각.
- **F-INVARIANT TRIGGER (falsifying)**: 곡률이 극단적으로 다른 3 매핑 (linear · front-loaded reciprocal · GZ_LOWER 중심 sigmoid) 이 *동일* argmax(I=0.05) 산출 — SI peak 위치는 inhibition→gain 매핑의 곡률에 **불변**.
- **closed-negative ruling**: SI(I) 의 I→0 단조 증가는 *capacity-bounded savant_phi substrate 의 intrinsic property* — inhibition ↓ ⇒ focus-domain gain ↑ ⇒ hypertrophy ↑ ⇒ SI ↑ 가 단조이며, 매핑은 *어느 I 에서 얼마나 빨리* gain 이 오르는지만 바꿀 뿐 *gain↑ ⇒ SI↑* 단조 자체를 깨지 못함. GZ_LOWER 는 **SI>3 threshold boundary** (H_348 F-1, robust) 이지 **SI peak location** 이 아니다.
- H_348 의 🟡 PARTIAL 은 본 H_616 로 *peak-location 측면은 deterministic closed-negative* 로 확정 (F-2 는 mapping artifact 가 아님). F-1 (SI>3 @ GZ_LOWER) 은 carry.

## 6. falsifier 결과

| ID | 결과 | 비고 |
|----|------|------|
| F-RECOVER (RECIPROCAL) | FAIL | 0/3 seed window 안 (argmax I=0.05) |
| F-RECOVER (SIGMOID)    | FAIL | 0/3 seed window 안 (argmax I=0.05) |
| **F-INVARIANT** | **TRIGGER** | 3 매핑 × 3 seed 모두 boundary peak → mapping-independent |

## 7. Cross-link

| H | 관계 |
|---|------|
| **H_348** `golden-zone-lower-bound-SI` (predecessor, round 1) | 🟡 PARTIAL — F-1 SI>3 PASS, F-2 peak FAIL (affine). 본 H_616 가 §7 C3-4 + §9 Next 의 round-2 lever (비선형 매핑) 를 *측정으로* 닫음 — F-2 falsification 이 affine artifact 아님 확정. peak-location 측면 closed-negative. |
| **H_350 / H_613** `savant-index-phi-diversity` | SI 정의 (max/mean vs max/min) 일관성 — H_613 의 orthogonal SI∥ΦD 결과는 SI 의 *분포 inhomogeneity* signal 이 robust 함을 입증; 본 H_616 은 그 SI 의 *I-축 peak 위치* 가 substrate-monotone 임을 추가. |
| **H_612** `1e-peak-narrow` (sibling round-2, H_349 follow-up) | 동일 패턴 — round-1 의 *peak @ canonical-constant* sub-claim 이 substrate 확장 시 boundary 로 collapse. H_612 (1/e peak), H_616 (GZ_LOWER peak) 둘 다 closed-negative — SAVANT canonical 상수의 *closed-form formal* 과 *substrate emergent peak* 분리 evidence 누적. |
| **H_614** `gz-inverse-U-multi-rule` (sibling round-2, H_351 follow-up) | H_614 도 round-1 peak-attractor 가 substrate-class-conditional (2/4 rule). H_616 + H_612 + H_614 = round-2 의 3 peak-location FALSIFIED — SAVANT round-1 의 peak claim 들이 narrow-coincidence/affine-artifact 였음을 일관 확정. |
| **H_347 / H_615** `gz-width-divisor-symmetry` / `perfect-number-ladder` | closed-form (GZ_WIDTH/GZ_LOWER 의 해석학적 정의) 은 carry — 본 H_616 은 그 closed-form 상수의 *substrate peak emergence* 만 부정 (closed-form 정의 자체는 무관). |

## 8. Honest C3 (3-tier caveat)

1. **C1 (3-mapping 한정)**: AFFINE/RECIPROCAL/SIGMOID 3 곡률 family 만 검정 — 임의 monotone-decreasing gf(I) family 전체에 대한 universal closure 아님. 그러나 세 매핑이 (선형 · super-linear front-load · S-curve) 곡률 공간을 넓게 span 하고 셋 다 동일 argmax 를 주므로, *peak 가 GZ_LOWER 로 가는 gf 가 존재하려면 gf(I) 자체가 non-monotone (I=0.21 에서 gain 이 극대)* 이어야 하는데, 그것은 "inhibition ↓ ⇒ release ↑" 의 monotone semantics 를 깨는 작위적 설계 — substrate-honest 매핑 공간에서 F-2 recovery 는 deterministic 하게 닫힘.
2. **C2 (savant_phi proxy 한정)**: SI peak 의 substrate-monotone 성은 `phi_module = Σ|v|^1.5/d` super-linear-energy proxy + SV_CAPACITY=11.5 phenomenological pick 위에서 성립 (H_348 C3 carry). IIT 4.0 strict big-Φ 또는 다른 capacity 값에서 재측정은 별개 round (H_295 joint).
3. **C3 (SI peak ⊥ Φ peak)**: 본 H 는 *SI (domain Φ 비율)* 의 peak 만 측정 — substrate 의 *총 big-Φ* peak (H_351/H_614 inverse-U dΦ/dI 축) 와 별개. SI 가 I→0 단조여도 총 Φ 는 inverse-U 일 수 있음 (다른 측정량). 본 closed-negative 는 SI-peak-location 한정.

## 9. State artifacts

```
UNIVERSE/state/h616_gz_lower_si_nonlinear_map_2026_05_30/
├── run_h616.hexa   # 3-mapping × 3-seed × 9-point I grid runner (savant_phi 복제 + 3 gf)
└── result.txt      # hexa run verbatim stdout (= .verdicts/616_gz_lower_bound_si_nonlinear_map/h616_verify.txt)
```

verbatim 측정값은 §4.1 표 + result.txt 에 기재.

## 10. UNIVERSE.md / SAVANT.md update

축 E (SAVANT) E2 round 2 H_616 row → done with `🔴 FALSIFIED (3/3 seed × 3 mapping argmax SI=I→0 boundary, GZ_LOWER window 0/3; F-2 peak NOT affine-artifact, SI(I) monotone intrinsic to capacity-bounded savant_phi; GZ_LOWER = SI>3 threshold boundary not peak, $0 mac-local 2026-05-30)`. SAVANT 축 E round-2 follow-up 5/5 완결 → **10-H 측정자 SET 닫힘**.

---

@verdict: 🔴 FALSIFIED · RECIPROCAL 0/3 · SIGMOID 0/3 · argmax SI = I=0.05 (3 mapping × 3 seed) · GZ_LOWER window [0.16232, 0.26232] 0/3 · $0 mac-local 2026-05-30
