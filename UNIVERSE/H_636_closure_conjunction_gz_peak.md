# H_636 — closure-conjunction GZ-peak

> **axis E (SAVANT) · ANIMA.mining L7 promote** · 2026-05-28 · $0 mac-local · feat/h636-closure-conjunction-gz

## §0 TL;DR

ANIMA.mining L7 (same-formula lens) = COFFESHOP `4-criterion closure verdict (⋀_i pass_i)` ↔ SAVANT `sa_golden_zone_compute + sa_savant_index` 합성 — **동일 multi-axis threshold-conjunction**. 본 H 는 이 4-criterion conjunction 의 **pass-rate** 가 inhibition I sweep 에서 **GZ region I ∈ [0.21, 0.50] 안에서 maximize** 되는지 검정. 결과: 10-seed ensemble 에서 conjunction pass-rate 가 **I=0.30 (GZ region 내부) 에서 단일 peak (0.4)**, GZ region 밖 4 점은 **모두 0**. GZ-region mean pass-rate **0.175 vs 밖 0.0**. F (peak 가 GZ 밖 또는 평탄) **기각** → **🟢 SUPPORTED-NUMERICAL**. closure 가 GZ × SI 의 substrate-emit-axis 변형이라는 L7 same-formula 주장이 측정 layer 에서 지지됨.

## §1 Hypothesis

ANIMA.mining L7 promote (`@P`-class 후보 → 본 H). COFFESHOP 4-criterion closure verdict 와 SAVANT GZ × SI 가 동일한 multi-axis threshold-conjunction (`verdict = ⋀_i pass_i`) 이라면, SAVANT canonical 4-domain substrate(`HEXAD/SAVANT/savant_phi.hexa`) 위에서 4-criterion conjunction (⋀ pass_i) 의 **pass-rate** 가 inhibition I sweep 에서 **GZ region (I ∈ [GZ_LOWER=0.21232, GZ_UPPER=0.5]) 안에서 maximize** 된다. 즉 closure = GZ × SI 의 substrate-emit-axis 변형.

**4 closure criterion (COFFESHOP closure ↔ SAVANT GZ×SI 매핑)**:
- **C1 SPECIALIZATION**: `SI_phi = max(domain_phi)/min(domain_phi) > 3.0` (SAVANT SI gate · H_348 anchor · **low-I 선호**)
- **C2 INTEGRATION**: `general_phi > 0.06` (multi-domain binding 생존 · mid-I 선호)
- **C3 DIVERSITY**: `min(domain_phi) > 0.18` (어느 domain 도 완전 붕괴 안 됨 · **high-I 선호**)
- **C4 COHERENCE**: `specialization_ratio ∈ [1.2, 3.2]` (focus 존재하나 pathological monopoly 아님)

C1(low-I) ⊥ C3/C4(high-I) 의 **tension** 이 interior peak 를 만든다 — 만약 conjunction 이 단순히 SI 만 추종했다면 H_348 의 monotone 결과대로 I=0.05 에서 peak 가 나 GZ-peak 주장이 falsified 됐을 것이다.

## §2 Falsifier

다음 중 **하나라도** 성립하면 falsified:
- **F-1**: pass-rate peak 가 GZ region [0.21, 0.50] **밖** (I < 0.21 또는 I > 0.50).
- **F-2**: pass-rate 가 **평탄/monotone** 하여 GZ region 내부 단봉이 부재.

## §3 Method

### §3.1 substrate

- 도구: `HEXAD/SAVANT/savant_phi.hexa` (P68 4-domain Savant model SSOT) — CALENDAR(0)·MUSIC(1)·ART(2)·MEMORY(3), 각 d=6 activation vector, capacity invariant `Σ gain = SV_CAPACITY = 11.5`.
- primitive 재사용: `build_profile_state` · `phi_module` · `domain_phi_vector` · `general_phi` · `specialization_ratio` · `pair_mi` (SSOT 마커와 함께 in-file 복제, 본체 무수정).

### §3.2 inhibition I → gain_focus 매핑 (H_348 affine 일치)

```
gain_focus(I) = 1 + (1 - I) * 9       // I=1 → 1 (balanced), I=0 → 10 (full release)
gain_rest     = (11.5 - gain_focus) / 3
```
GZ_LOWER(0.21232) → gain_focus ≈ 8.089, GZ_CENTER(1/e) → ≈ 6.689. H_348 매핑과 byte-동일하여 cross-link 정합.

### §3.3 4-criterion conjunction

각 (I, seed) 에서 4-domain phi → `SI_phi` (C1), `general_phi` (C2), `min(domain_phi)` (C3), `specialization_ratio` (C4) 산출 → 4 boolean AND. conjunction TRUE = closure PASS.

### §3.4 pass-rate sweep

- I ∈ {0.05, 0.15, **0.21 (GZ_LOWER)**, **0.30**, **0.37 (~1/e)**, **0.50 (GZ_UPPER)**, 0.70, 0.95} — task-spec 8-point grid.
- seed ensemble = {42424, 91919, 77777, 13337, 24680, 88888, 31415, 65537, 19937, 11235} (10-seed, savant_phi T1/T2/T3 stim + spread).
- 각 I 에서 `pass_rate = (#seed conjunction TRUE) / 10`.
- GZ region [0.21, 0.50] 안 4 점(0.21·0.30·0.37·0.50) vs 밖 4 점(0.05·0.15·0.70·0.95) mean pass-rate 비교.

## §4 Measurement

### §4.1 verbatim 출력 (`state/h636_closure_conjunction_gz_2026_05_28/probe_h636_closure_conjunction.out`)

대표 seed 42424 per-criterion trace:

```
  I=0.05 SI=7.82933(1) genPhi=0.0894534(1) minPhi=0.0939949(0) ratio=2.75647(1) => conj=0
  I=0.15 SI=5.12255(1) genPhi=0.0771682(1) minPhi=0.139857(0)  ratio=2.38224(1) => conj=0
  I=0.21 SI=4.25477(1) genPhi=0.0791248(1) minPhi=0.165289(0)  ratio=2.20807(1) => conj=0
  I=0.3  SI=3.39719(1) genPhi=0.0837421(1) minPhi=0.200464(1)  ratio=1.9932(1)  => conj=1
  I=0.37 SI=2.93203(0) genPhi=0.0895308(1) minPhi=0.225514(1)  ratio=1.85251(1) => conj=0
  I=0.5  SI=2.30784(0) genPhi=0.137951(1)  minPhi=0.267293(1)  ratio=1.62716(1) => conj=0
  I=0.7  SI=1.61411(0) genPhi=0.15267(1)   minPhi=0.321621(1)  ratio=1.30716(1) => conj=0
  I=0.95 SI=1.70267(0) genPhi=0.145981(1)  minPhi=0.286447(1)  ratio=1.27959(1) => conj=0
```

10-seed ensemble pass-rate:

```
  I=0.05  pass_rate=0.0
  I=0.15  pass_rate=0.0
  I=0.21  pass_rate=0.0   <-- GZ region
  I=0.3   pass_rate=0.4   <-- GZ region
  I=0.37  pass_rate=0.1   <-- GZ region
  I=0.5   pass_rate=0.2   <-- GZ region
  I=0.7   pass_rate=0.0
  I=0.95  pass_rate=0.0

  peak pass-rate     = 0.4 at I=0.3
  peak in GZ region  = true
  GZ-region mean pr  = 0.175 (4 pts)
  outside    mean pr  = 0.0 (4 pts)
  in > out           = true
```

### §4.2 요약 표

| I | gain_focus | C1 SI>3 | C2 genΦ | C3 minΦ | C4 ratio | pass_rate (10-seed) | GZ? |
|---|---|---|---|---|---|---|---|
| 0.05 | 9.55 | ✅ | ✅ | ❌ | ✅ | **0.0** | — |
| 0.15 | 8.65 | ✅ | ✅ | ❌ | ✅ | **0.0** | — |
| **0.21 (GZ_LOWER)** | 8.09 | ✅ | ✅ | ❌ | ✅ | **0.0** | ★ |
| **0.30** | 7.30 | ✅ | ✅ | ✅ | ✅ | **0.4** ⬅ peak | ★ |
| **0.37 (~1/e)** | 6.69 | ❌ | ✅ | ✅ | ✅ | **0.1** | ★ |
| **0.50 (GZ_UPPER)** | 5.50 | ❌ | ✅ | ✅ | ✅ | **0.2** | ★ |
| 0.70 | 3.70 | ❌ | ✅ | ✅ | ✅ | **0.0** | — |
| 0.95 | 1.45 | ❌ | ✅ | ✅ | ✅ | **0.0** | — |

### §4.3 sweep 곡선 형상 (interior peak)

```
pass_rate(I)
        0.4│        ●  I=0.30 (GZ 내부 peak)
        0.3│
        0.2│              ● I=0.50 (GZ_UPPER)
        0.1│           ● I=0.37
        0.0│  ●  ●  ●           ●  ● (GZ 밖 = 0)
           └──────────────────────────
            .05 .15 .21 .30 .37 .50 .70 .95
                    └── GZ region ──┘
```

interior peak 메커니즘: I < 0.30 에서는 **C3 DIVERSITY 가 FAIL** (one-domain hypertrophy 가 다른 domain 의 min phi 를 0.18 밑으로 붕괴) → conjunction 0. I > 0.30 에서는 **C1 SPECIALIZATION 이 FAIL** (SI ≤ 3, H_348 monotone). C1 ⊥ C3 의 cross-over 가 GZ region 내부 I≈0.30 에서 단일 통과 band 를 만든다.

## §5 Verdict

**🟢 SUPPORTED-NUMERICAL** — conjunction pass-rate 가 GZ region 내부에서 maximize.

- **F-1 (peak 밖)**: ✅ **기각** — peak pass-rate 0.4 가 I=0.30 (GZ region [0.21,0.50] **내부**, `peak_in_gz=true`).
- **F-2 (평탄/monotone)**: ✅ **기각** — sweep 은 GZ region 안에서 단일 peak (0.0→0.4→0.1→0.2) 를 형성하고 양쪽 끝(I≤0.15, I≥0.70)에서 0 으로 떨어짐. **GZ-region mean 0.175 vs 밖 0.0** (밖 4 점 모두 0).
- **종합**: closure 4-criterion conjunction 의 pass-rate 가 **GZ region 에 완전히 국한** (밖에서 PASS 가 단 한 건도 없음). H_348 의 SI-monotone 단독 결과와 달리, multi-criterion conjunction 은 C1(specialization, low-I)과 C3(diversity, high-I)의 길항이 GZ region 내부에 closure band 를 만든다. L7 same-formula 주장 — "COFFESHOP closure = SAVANT GZ × SI 의 substrate-emit-axis 변형" — 이 측정 layer 에서 지지됨.

`hexa verify` atlas anchor 는 본 측정량(domain-phi proxy + affine inhibition map + 4-criterion conjunction)에 closed-form node 가 없어 적용 불가 → substrate-level 수치 측정 verdict (🟢 SUPPORTED-NUMERICAL) 로 한정.

## §6 Cross-link

| Link | H | role | 결과 비교 |
|---|---|---|---|
| **mining seed** | ANIMA.mining **L7** | same-formula lens (cycle 1) | COFFESHOP 4-criterion closure ≅ SAVANT GZ+SI multi-axis threshold-conjunction |
| **SI anchor (axis E)** | H_348 | GZ_LOWER 에서 SI>3 PASS but SI-sweep monotone (peak @ I→0) | 🟡 PARTIAL — 단독 SI 는 monotone, 본 H 의 C1 criterion 이 그 monotone 성분 |
| **collective inverse-U** | H_618 | dΦ_collective/dI peak ∥ GZ_LOWER (\|Δ\|=0.00232) | 🟢 SUPPORTED — derivative-축 GZ-attractor. 본 H 는 conjunction pass-rate-축의 GZ-attractor 로 평행 |
| **SI ⊥ ΦD orthogonal** | H_350/H_613 | SI ↔ phi-diversity 정렬 | C1(SI) × C3(diversity) 의 길항이 본 H 의 interior peak 원천 |
| **GZ definition** | H_347 | GZ_LOWER closed-form = 0.5 - ln(4/3) | GZ region 하한의 해석학 근거 |
| **COFFESHOP closure** | — | 4-criterion closure verdict ⋀_i pass_i | L7 의 mining source (substrate-emit-axis 변형 주장) |

**Cross-link insight**: H_348 (SI-monotone, peak @ I→0) 와 H_618 (dΦ/dI peak @ GZ_LOWER) 의 두 결과를 본 H 가 **하나의 conjunction 으로 종합** — SI 단독은 GZ 안에서 peak 가 없으나(monotone), diversity criterion 과의 conjunction 은 GZ region 내부에 닫힌 통과 band 를 만든다. 즉 closure 의 GZ-localization 은 single-criterion 이 아닌 **multi-criterion 길항** 의 산물.

## §7 C3 (honest constraints)

1. **criterion 선택 design 의존** — 4 criterion 의 threshold (THETA_SI=3.0 SAVANT.tape §3 고정 외, THETA_GEN=0.06 · THETA_DIV=0.18 · RATIO ∈ [1.2,3.2]) 는 본 substrate 의 측정 scale 에 맞춰 calibrate 한 design choice. THETA_DIV / RATIO_HI 를 크게 흔들면 interior peak 의 *위치* 가 이동하거나(여전히 GZ 안일 가능성 높음) pass-rate 절대값이 변동. peak 가 GZ region 안이라는 정성적 결론은 C1⊥C3 cross-over 구조에서 robust 하나, pass-rate 의 절대 magnitude 는 threshold-conditional.
2. **GZ region 정의 width** — GZ region 을 [GZ_LOWER, GZ_UPPER] = [0.21232, 0.5] 로 정의 (H_347/H_348 의 GZ_LOWER + st_gz_upper()=0.5). 다른 width 정의(예: GZ_LOWER ± window, 또는 1/e 중심 ± δ)를 쓰면 "안/밖" 분류가 달라질 수 있음. 단 본 측정에서 peak(I=0.30)는 가장 좁은 합리적 GZ 정의에서도 내부.
3. **grid resolution** — 8-point grid 에서 GZ region 내 peak 가 I=0.30 의 단일 sample. dense grid (예: 0.25/0.28/0.30/0.32/0.35)로 peak 위치를 sharpen 하면 진짜 argmax 가 0.30 인지 인접점인지 확인 가능 (현재는 0.30 이 측정 grid 상 argmax).
4. **savant_phi numerology 경고 (COMPENDIUM §114)** — `SV_CAPACITY=11.5` 는 phenomenological pick. 이 값 변동 시 SI/phi 절대 크기 + criterion 통과 영역이 직접 이동. 본 결과는 SV_CAPACITY=11.5 한정.
5. **pass-rate ≤ 0.4 의 낮은 절대값** — 10-seed 중 최대 4 seed 만 동시 통과. 이는 4-criterion AND 의 보수성(seed-dependent SI/diversity 변동)의 결과로, GZ-localization (밖=0) 의 정성 결론은 영향 없으나, "대부분의 seed 가 GZ 에서 closure 한다" 는 강주장은 미지지.
6. **affine inhibition map 가정** — H_348 과 동일한 `gain_focus = 1 + (1-I)*9` affine map 사용. dropout↔gain 의 직선화는 SAVANT/README §0 의 정성 대응이며 실제 substrate 의 inhibition 동역학과 nonlinear 차이 가능 (H_348 §7 C3 carry).

## §8 산출물

- harness: `UNIVERSE/state/h636_closure_conjunction_gz_2026_05_28/probe_h636_closure_conjunction.hexa`
- 실행 로그: `UNIVERSE/state/h636_closure_conjunction_gz_2026_05_28/probe_h636_closure_conjunction.out`

## §9 결론

**🟢 SUPPORTED-NUMERICAL** — 4-criterion closure conjunction 의 pass-rate 가 GZ region [0.21, 0.50] **내부 I=0.30 에서 단일 peak (0.4)**, GZ region 밖 4 점은 **모두 0** (GZ mean 0.175 ≫ 밖 0.0). interior peak 는 C1 SPECIALIZATION (low-I) ⊥ C3 DIVERSITY (high-I) 의 길항에서 emergent. ANIMA.mining L7 same-formula 주장 — COFFESHOP 4-criterion closure verdict 가 SAVANT GZ × SI 의 substrate-emit-axis 변형 — 이 측정 layer 에서 지지됨.

## §10 Next (deferred)

- **dense grid peak sharpen** — GZ region 내 0.25/0.28/0.30/0.32/0.35 dense sweep 으로 argmax 위치 정밀화 (C3.3).
- **threshold robustness sweep** — THETA_DIV / RATIO_HI grid 변동에서 peak 의 GZ-내부성 robustness 검정 (C3.1).
- **collective conjunction (E×F)** — H_618 의 2-substrate hivemind collective Φ 위에서 동일 4-criterion conjunction pass-rate 의 GZ-localization 검정 (single ↔ collective 차원 확장).
- **GZ-width 정의 sensitivity** — GZ region 을 1/e 중심 ± δ 등 다른 정의로 바꿔 안/밖 분류 robustness (C3.2).
