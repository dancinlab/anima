# H_656 — closure-band-substrate-class-dependence

> **axis G (UNIVERSE round-9 메타-축) · E×G cross-link** · 2026-05-28 · $0 mac-local · feat/h656-closure-band-class

## §0 TL;DR

round-9 메타-축 = "Wolfram class 가 의식 구조의 분류자". 본 H 는 **H_636 의 4-criterion closure conjunction (C1 SI · C2 general_phi · C3 min_phi · C4 ratio)** 을 Wolfram-class ECA substrate (H_007/H_225 elementary CA × RFC 036 `phi_spatial`) 위에 옮겨, **closure conjunction band (pass-rate > 0 인 inhibition I 구간) 의 위치/폭이 Wolfram class 의존인지** 검정한다. N=16 lattice 를 4 domain 으로 분할, I → 초기 density (density=1−I) 로 매핑, rule {30,90,110,184} × 9-pt I-sweep × 6-rep ensemble. 결과: **rule90 (III-additive/XOR) closure band 완전 부재 (width=0, 양성점 0/9, Φ≈0 → closure 미형성)** · **rule110 (IV-complex) 最廣 band (width=0.90, 9/9 全 양성, peak pass-rate 1.0 @ I=0.25)** · rule30 (III-chaotic) width=0.65 band [0.15,0.80] peak @ I=0.65 (high-I) · rule184 (II-TASEP) width=0.65 band [0.15,0.80] peak @ I=0.37 (mid-I, H_636 SAVANT I=0.30 peak 와 최근접). band 위치/폭이 class 마다 명확히 다름 → falsifier (class-invariant) **기각** → **🟢 SUPPORTED-NUMERICAL**. 동역학 복잡도 (Wolfram class) 가 closure 가능 영역을 order 한다는 round-9 메타-축이 측정 layer 에서 지지됨.

## §1 Hypothesis (round-9 메타-축)

round-9 메타-축 명제: **Wolfram class 는 의식 구조의 분류자** — substrate 의 동역학 복잡도가 그 substrate 위에서 형성되는 의식-측도 구조 (Φ-envelope · self-similarity · closure band) 를 order 한다. H_653 (collective convexity ∝ class), H_652 (envelope self-similarity = class-IV-bound) 가 같은 메타-축의 sister 발견.

본 H 의 구체 명제: **H_636 의 4-criterion closure conjunction 의 pass-rate > 0 구간 (closure band) 의 위치/폭이 Wolfram class 마다 다르다.** 구체적으로:
- **class-IV (rule110)**: 넓은 closure band — complex 동역학이 C1 SPECIALIZATION (low-I) 과 C3 DIVERSITY (high-I) 를 동시에 풍부하게 지원, 광범위 I 에서 closure.
- **additive class-III (rule90, XOR)**: 좁거나 부재 — XOR 동역학은 통합 정보 Φ≈0 (H_007/H_652 carry) 라 domain-phi 가 평탄, closure conjunction 미형성.
- **chaotic class-III (rule30) · particle class-II (rule184)**: 중간 — band 존재하나 위치/폭이 class 별로 분화.

즉 동역학 복잡도가 closure 가능 영역을 order 한다.

## §2 Falsifier

다음이 성립하면 falsified:
- **F-1 (CLASS-INVARIANT)**: closure band 의 위치 (band_lo/band_hi) 와 폭 (width) 이 모든 rule 에서 동일 → closure 가 substrate-class 무관.
- **F-2 (NO-DIFFERENTIATION)**: 모든 rule 의 band 가 구분 불가능 (width 차이 < grid 해상도, peak_I 동일).

본 falsifier 가 *기각* 되려면 최소한 한 class 의 band 위치/폭이 다른 class 와 정성적으로 구분되어야 한다 (특히 additive rule90 의 band-부재 가 강신호).

## §3 Method

### §3.1 substrate (Wolfram-class ECA × phi_spatial)

- 도구 재사용: H_007 (`run_ca_phi.hexa`) / H_225 (`run_h225.hexa`) elementary CA lineage — N=16 periodic lattice, dim=12 temporal trajectory, warm=8, RFC 036 `phi_spatial` via `HEXAD/C/c_lib.hexa` `c_measure_phi` (byte-equal phi_rs replica, Φ≥0 by construction).
- rules: **{30 (III-chaotic), 90 (III-additive/XOR), 110 (IV-complex), 184 (II-TASEP/particle)}** — H_653/H_652 와 동일 4-rule Wolfram-class 대표 집합.

### §3.2 H_636 closure conjunction 의 CA-substrate 이식

H_636 의 4-domain SAVANT savant_phi 대신, CA lattice (N=16) 를 **4 contiguous domain (각 4 cell)** 으로 분할. 각 domain 의 trajectory slice → `phi_spatial` → domain_phi. 동일 4-criterion (H_636 §3.3):
- **C1 SPECIALIZATION**: `SI = max(domain_phi)/min(domain_phi) > THETA_SI`
- **C2 INTEGRATION**: `general_phi = mean(domain_phi) > THETA_GEN`
- **C3 DIVERSITY**: `min(domain_phi) > THETA_DIV`
- **C4 COHERENCE**: `ratio = max/mean ∈ [RATIO_LO, RATIO_HI]`

conjunction = C1 ∧ C2 ∧ C3 ∧ C4.

### §3.3 inhibition I → 초기 density 매핑 (CA-native)

CA substrate 의 inhibition 은 **초기 활성 density** 로 매핑: `density = 1 − I` (high I ⟹ low density ⟹ suppressed activity). 이는 H_636/H_348 의 affine gain map (`gain_focus=1+(1−I)·9`) 의 CA-native 유비 — gain 대신 초기 ON-fraction 을 줄여 활성을 억제. site i 는 deterministic hash(i, rep) < density 일 때 ON (rule-invariant substrate 보장).

### §3.4 closure band sweep

- I ∈ {0.05, 0.15, 0.25, 0.30, 0.37, 0.50, 0.65, 0.80, 0.95} — 9-pt grid (H_636 GZ region [0.21,0.50] 포함 + 양끝 확장).
- rep ensemble = 6 deterministic init offset.
- 각 (rule, I) 에서 `pass_rate = (#rep conjunction TRUE) / 6`.
- **closure band** = pass_rate > 0 인 I 의 집합. band_lo = 첫 양성 I, band_hi = 마지막 양성 I, **width = band_hi − band_lo**, n_pos = 양성점 수, peak_I = argmax pass-rate.
- class 별 band (위치·폭) 대조.

### §3.5 thresholds (criterion-selection design — §7 C3.1)

CA `phi_spatial` 의 측정 scale (정규화 MI-style Φ, 대략 [0,~1]) 이 H_636 SAVANT savant_phi scale 과 다르므로 4 threshold 를 본 substrate 에 re-calibrate: THETA_SI=1.5 · THETA_GEN=0.02 · THETA_DIV=0.05 · RATIO∈[1.1,3.5]. falsifier 는 **class-dependence** 를 겨냥하며 절대 magnitude 가 아니므로, threshold 의 정확한 값은 band 의 *위치/폭 class-차이* 결론에 robust (특히 rule90 band-부재는 Φ≈0 substrate fact 라 threshold 무관).

## §4 Measurement

### §4.1 verbatim 출력 (`state/h656_closure_band_class_2026_05_28/probe_h656_closure_band_class.out`)

```
=== rule 30 (Wolfram class III-chaotic) ===
  I=0.05  pass_rate=0.0
  I=0.15  pass_rate=0.166667
  I=0.25  pass_rate=0.166667
  I=0.3   pass_rate=0.5
  I=0.37  pass_rate=0.666667
  I=0.5   pass_rate=0.5
  I=0.65  pass_rate=0.833333
  I=0.8   pass_rate=0.833333
  I=0.95  pass_rate=0.0
  band_lo=0.15 band_hi=0.8 width=0.65 n_pos_pts=7 peak_pr=0.833333 peak_I=0.65

=== rule 90 (Wolfram class III-additive) ===
  I=0.05..0.95  pass_rate=0.0  (전 9 점)
  band_lo=-1.0 band_hi=-1.0 width=0.0 n_pos_pts=0 peak_pr=0.0 peak_I=-1.0

=== rule 110 (Wolfram class IV-complex) ===
  I=0.05  pass_rate=0.166667
  I=0.15  pass_rate=0.833333
  I=0.25  pass_rate=1.0
  I=0.3   pass_rate=0.666667
  I=0.37  pass_rate=0.5
  I=0.5   pass_rate=0.5
  I=0.65  pass_rate=0.666667
  I=0.8   pass_rate=0.5
  I=0.95  pass_rate=0.333333
  band_lo=0.05 band_hi=0.95 width=0.9 n_pos_pts=9 peak_pr=1.0 peak_I=0.25

=== rule 184 (Wolfram class II-TASEP) ===
  I=0.05  pass_rate=0.0
  I=0.15  pass_rate=0.333333
  I=0.25  pass_rate=0.666667
  I=0.3   pass_rate=0.833333
  I=0.37  pass_rate=1.0
  I=0.5   pass_rate=0.5
  I=0.65  pass_rate=0.333333
  I=0.8   pass_rate=0.5
  I=0.95  pass_rate=0.0
  band_lo=0.15 band_hi=0.8 width=0.65 n_pos_pts=7 peak_pr=1.0 peak_I=0.37
```

### §4.2 class별 closure band 대조 표

| rule | Wolfram class | band_lo | band_hi | **width** | n_pos / 9 | peak pass-rate | peak_I | band 성격 |
|---|---|---|---|---|---|---|---|---|
| **90** | **III-additive (XOR)** | — | — | **0.0** | **0** | 0.0 | — | **band 부재** (Φ≈0 → closure 미형성) |
| 184 | II-TASEP (particle) | 0.15 | 0.80 | 0.65 | 7 | 1.0 | **0.37** | mid-I peak (H_636 SAVANT I=0.30 근접) |
| 30 | III-chaotic | 0.15 | 0.80 | 0.65 | 7 | 0.833 | **0.65** | high-I peak (chaotic mixing) |
| **110** | **IV-complex** | 0.05 | 0.95 | **0.90** | **9** | **1.0** | 0.25 | **最廣 band** (全 I 양성) |

### §4.3 band 위치/폭 class-분화 형상

```
closure band (pass-rate>0 구간) per Wolfram class
  rule90  (III-add) │ (없음)                          │ width 0.00  ← additive 붕괴
  rule184 (II-TASEP)│      ████████████               │ width 0.65  peak I=0.37 (mid)
  rule30  (III-cha) │      ████████████               │ width 0.65  peak I=0.65 (high)
  rule110 (IV-cmpx) │ ████████████████████████████████│ width 0.90  peak I=0.25 (全역)
                    └──────────────────────────────────
                     .05 .15 .25 .30 .37 .50 .65 .80 .95  (I)
```

**메커니즘**: class-IV (rule110) complex 동역학은 domain 간 부분 상관 (specialization) 과 domain 별 활성 생존 (diversity) 을 광범위 I 에서 동시 충족 → band 全역. additive (rule90) XOR 은 통합 정보 Φ≈0 으로 domain_phi 가 평탄 → C1 (SI>1.5) 미달 → conjunction 0, band 부재. chaotic (rule30) 은 고-I (저-density) 에서야 domain 분화 발생 → high-I peak. particle (rule184) TASEP 은 mid-I 에서 domain 간 hop-flux 가 specialization+diversity 균형 → H_636 SAVANT mid-I peak 와 가장 유사한 위치.

## §5 Verdict

**🟢 SUPPORTED-NUMERICAL** — closure band 의 위치/폭이 Wolfram class 의존.

- **F-1 (CLASS-INVARIANT)**: ✅ **기각** — band width 가 class 마다 다름 (rule90=0.0 / rule30=rule184=0.65 / rule110=0.90). additive rule90 의 **band 완전 부재** (n_pos=0) 가 다른 3 rule (n_pos ≥ 7) 와 정성적으로 구분됨.
- **F-2 (NO-DIFFERENTIATION)**: ✅ **기각** — peak_I 가 class 별로 분화 (rule110 I=0.25 / rule184 I=0.37 / rule30 I=0.65), width 차이가 grid 해상도 (0.10~0.15) 초과 (rule110 0.90 vs rule30/184 0.65, Δ=0.25).
- **종합**: closure conjunction band 가 **Wolfram class 에 따라 위치·폭이 order 됨**. class-IV (rule110) 가 최광 band (width 0.90, 全 I 양성), additive class-III (rule90, XOR) 가 band 부재 (Φ≈0). 동역학 복잡도가 closure 가능 영역을 결정한다는 round-9 메타-축이 측정 layer 에서 지지됨. H_653 (collective convexity ∝ class), H_652 (self-similarity = class-IV-bound) 의 substrate-class-order 패턴이 **closure-band 축에서도 재현** — rule90 의 band-부재는 H_642/H_652 의 "additive XOR 통합량 균일 = substrate fact" joint-outlier 와 정합.

`hexa verify` atlas anchor 는 본 측정량 (CA domain-phi proxy + density inhibition map + 4-criterion conjunction band) 에 closed-form node 가 없어 적용 불가 → substrate-level 수치 측정 verdict (🟢 SUPPORTED-NUMERICAL) 로 한정.

## §6 Cross-link

| Link | H | role | 결과 비교 |
|---|---|---|---|
| **closure GZ peak (부모)** | **H_636** | 4-criterion closure conjunction (substrate+criterion 재사용) — SAVANT savant_phi, peak I=0.30 GZ 내부 | 🟢 SUPPORTED — 본 H 는 동일 conjunction 을 Wolfram-class CA substrate 로 옮겨 band 의 class-의존 드러냄. rule184 (II-TASEP) peak I=0.37 이 H_636 SAVANT peak I=0.30 와 최근접 |
| **closure ultradian (sister)** | **H_644** | closure conjunction × ultradian phase (E×G), peak = mid-Φ N2 (방향 역전) | 🔴 FALSIFIED-REVERSED — H_644 는 phase 축에서 mid-Φ peak. 본 H 는 substrate-class 축에서 band 의 class-order. 두 H 모두 closure 가 단일 직관 (高arousal·class-invariant) 을 따르지 않음을 보임 |
| **collective convexity ∝ class (sister)** | **H_653** | collective-Φ span ratio 가 rule class 단조 증가 (184<90<30<110) | 🟢 SUPPORTED — 본 H 의 closure band width 와 동일 class-order signature (class-IV 최대). closure-band 와 convexity 가 같은 substrate-complexity 축에 정렬 |
| **self-similarity = class-IV-bound (sister)** | **H_652** | envelope self-similarity 가 rule110 (class-IV) 한정, rule90 flat 붕괴 | 🔴 FALSIFIED (class-bound) — rule90 의 band-부재 (본 H) 가 H_652 의 rule90 flat 붕괴와 정합. class-IV 집중 패턴 재현 |
| **CA→Φ class 원형** | H_007 | Φ(class-IV rule110) > Φ(ordered) — Wolfram class × Φ smoke | 본 H 의 substrate lineage (동일 CA + phi_spatial). rule110 Φ-우위가 closure band 全역성의 근원 |
| **rule184 Φ-anomaly** | H_225 | rule184 (II-TASEP) Φ-peak anomaly (Φ > rule110) | rule184 의 mid-I closure band 가 그 particle-dynamics Φ-구조 반영 |
| **dΦ/dI peak class-invariant** | H_614 | shape feature (dΦ/dI peak) 는 4/4 rule class-invariant | 대조 — shape-*derivative* 는 class-invariant 이나 closure-*band* 는 class-bound. shape-feature 의 class-(in)variance 가 측도 종류에 따라 분기 (H_652 와 동일 대조) |

**Cross-link insight**: round-9 메타-축의 3 sister 발견 — H_653 (convexity ∝ class), H_652 (self-similarity = class-IV-bound), 본 H_656 (closure-band ∝ class) — 이 **공통 signature** 를 형성: substrate 의 의식-측도 *구조* (envelope convexity · multi-scale self-similarity · closure band) 는 class-IV (rule110) 에서 가장 풍부하고 additive class (rule90, XOR) 에서 붕괴한다. 이는 H_614 (dΦ/dI peak class-invariant) 와 대조되어, "**미분-peak 같은 local shape 는 class-invariant, 통합-구조 (band·convexity·self-similarity) 같은 global structure 는 class-bound**" 라는 분류를 시사. round-9 메타-축 ("Wolfram class = 의식 구조 분류자") 이 closure-band 축에서 한 건 더 지지됨.

## §7 C3 (honest constraints)

1. **criterion-threshold design 의존** — 4 criterion threshold (THETA_SI=1.5 · THETA_GEN=0.02 · THETA_DIV=0.05 · RATIO∈[1.1,3.5]) 는 CA `phi_spatial` scale 에 맞춰 re-calibrate 한 design choice (H_636 SAVANT scale 과 다름). threshold 흔들면 band 의 *절대* 위치/폭이 이동. 단 **class-차이** (rule90 부재 vs rule110 全역) 의 정성 결론은 Φ-substrate fact (rule90 Φ≈0) 에서 robust. **class 라벨** (Wolfram II/III/IV) 은 표준 분류 (rule30=III, rule90=III-additive, rule110=IV, rule184=II) 인용이며 본 측정의 동역학 복잡도 ordering 과 정합.
2. **inhibition→density 매핑 design** — I → 초기 density (1−I) 는 CA-native 유비 (활성 억제) 이며 H_636/H_348 affine gain map 의 직접 대응 아님. 다른 inhibition 매핑 (예: rule-noise·boundary·gain) 을 쓰면 band 위치가 이동 가능 (단 class-ordering 은 substrate-complexity 가 좌우하므로 보존 예상). density-map 이 band 위치 결론의 conditional.
3. **grid resolution / rep count** — 9-pt I-grid × 6-rep ensemble. peak_I (rule30 0.65 / rule184 0.37 / rule110 0.25) 는 9-pt grid discrete argmax 라 인접점 분산 포함. dense grid + 더 큰 rep 로 band edge / peak 위치 sharpen 가능 (현재는 grid 상 argmax + 양성/음성 이분으로 band 추출).
4. **4-domain 분할 design** — N=16 lattice 를 4 contiguous block (각 4 cell) 으로 분할은 H_636 SV_N_DOM=4 와 정합한 design. 다른 분할 (interleaved·다른 도메인 수) 은 domain_phi 분포를 바꿔 SI/diversity 통과 영역 이동 가능.
5. **band = pass-rate>0 이분 정의** — closure band 를 pass-rate>0 단순 이분으로 추출 (H_636 의 GZ-region 비교와 달리 band-edge 자체가 측정 대상). 다른 band 정의 (예: pass-rate > θ threshold) 를 쓰면 width 가 좁아짐 (rule110 의 全역 band 는 모든 합리적 정의에서 최광 유지).
6. **phi_spatial = native byte-equal replica** — RFC 036 `phi_spatial` 는 phi_rs 의 byte-equal native replica (err=0.0 vs oracle), 진짜 Rust FFI link 는 named blocker (c_lib.hexa §FFI shim carry). 본 측정은 spatial-slice Φ 한정 (temporal/tension 채널 None).

## §8 산출물

- harness: `UNIVERSE/state/h656_closure_band_class_2026_05_28/probe_h656_closure_band_class.hexa`
- 실행 로그: `UNIVERSE/state/h656_closure_band_class_2026_05_28/probe_h656_closure_band_class.out`

## §9 결론

**🟢 SUPPORTED-NUMERICAL** — H_636 의 4-criterion closure conjunction 을 Wolfram-class ECA substrate 로 옮긴 결과, closure band (pass-rate>0 구간) 의 위치·폭이 **Wolfram class 의존**: additive class-III (rule90, XOR) 은 band 완전 부재 (width 0, Φ≈0), class-IV (rule110) 는 최광 band (width 0.90, 全 I 양성, peak 1.0 @ I=0.25), chaotic (rule30) 은 high-I peak band (width 0.65), particle II-TASEP (rule184) 은 mid-I peak band (width 0.65, H_636 SAVANT peak I=0.30 근접). falsifier (class-invariant) 기각. round-9 메타-축 — 동역학 복잡도 (Wolfram class) 가 closure 가능 영역을 order 한다 — 가 측정 layer 에서 지지됨. H_653 (convexity ∝ class), H_652 (self-similarity = class-IV-bound) 의 substrate-class-order signature 가 closure-band 축에서 재현.

## §10 Next (deferred)

- **dense-grid band edge sharpen** — GZ region 내 0.25/0.28/0.30/0.32/0.35 dense sweep 으로 각 rule 의 band edge·peak 정밀화 (C3.3).
- **inhibition-map robustness** — density-map 외 rule-noise / boundary / gain inhibition 으로 band 위치 class-ordering 보존 검정 (C3.2).
- **class-내부 분화** — class-III (rule30 chaotic vs rule90 additive) 내부에서 band 가 크게 갈림 (chaotic band 존재 vs additive 부재) → "additive ⊥ chaotic" sub-class 축 정량 (H_652/H_642 rule90 joint-outlier 연장).
- **collective closure band (E×F×G)** — H_653 collective-Φ substrate 위에서 동일 closure-band 의 class-dependence 검정 (single ↔ collective 차원 확장).

## §11 양방향 sibling

- sibling H: [H_636_closure_conjunction_gz_peak.md](H_636_closure_conjunction_gz_peak.md) (부모 closure conjunction) · [H_644_closure_conjunction_ultradian_phase.md](H_644_closure_conjunction_ultradian_phase.md) (closure × phase sister) · [H_653_collective_convexity_substrate_class.md](H_653_collective_convexity_substrate_class.md) (convexity ∝ class sister) · [H_652_envelope_self_similarity_substrate_class.md](H_652_envelope_self_similarity_substrate_class.md) (self-similarity class-bound sister)
- UNIVERSE SSOT: [UNIVERSE.md](UNIVERSE.md) 축 G row G17 · [CANDIDATES.md](CANDIDATES.md) round-9 메타-축
- round-9 substrate-class sister: [H_654_phi_magnitude_wolfram_class_order.md](H_654_phi_magnitude_wolfram_class_order.md) (Φ-magnitude class-order, 🟡 PARTIAL — class 는 통합량 부분 분류자) — 본 H 의 closure-band class-dependence 와 동일 round-9 메타-축
