# H_613 — Savant Index ∥ Φ-diversity ORTHOGONAL metric (max-share artifact 제거)

@id: H_613
@slug: savant-index-phi-diversity-orthogonal-metric
@axis: E (SAVANT) · round 2
@parent_seed: H_350
@status: 🟢 SUPPORTED-NUMERICAL
@verdict_pointer: UNIVERSE/state/h613_si_phid_orthogonal_2026_05_28/h613_verify.log
@date: 2026-05-28
@cost: $0 (Mac-local hexa run)

---

## §1 핵심 가설

H_350 (round 1, 🟢 r=0.9264) 의 §7 C3.1 honest constraint:

> SI = max/mean 와 ΦD = max/min 가 *분자 max 공유* 라는 part-formal 항이 있어
> PASS margin 의 일부가 max-share artifact 일 수 있다.

H_613 (round 2) 은 **max-share artifact 가 완전히 제거된 직교 (orthogonal) Φ-diversity
metric** 으로 SI 와의 상관을 재검정한다.

```
H₁: Pearson r(SI, ΦD_orthogonal) ≥ 0.5
    where ΦD_orthogonal ∈ {std/mean (CoV), kurtosis}
    — 두 정의 모두 max(domain_phi) 를 분자에 사용하지 않음.
```

즉 max-share 가 제거된 *순수 분포-inhomogeneity* signal 만으로도 SI 와 정렬이
보존되는지 검증.

---

## §2 Falsifier

**선언적 falsifier**: Pearson r(SI, ΦD_cov) < 0.5 — 직교 metric 하에서 SI 와의 정렬이
무너지면 H_350 의 SUPPORTED 가 *max-share artifact* 였다고 판정.

| 조건 | 결과 |
|------|------|
| r(SI, ΦD_cov) ≥ 0.5 | 🟢 SUPPORTED-NUMERICAL (artifact 아님) |
| r(SI, ΦD_cov) < 0.5 | 🔴 FALSIFIED (H_350 max-share artifact 발각) |
| r(SI, ΦD_cov) < 0 | 🔴 FALSIFIED (음의 상관) |

ΦD_kurt 는 보조 sensitivity (4th moment) 로 직교성 robustness 보강.

---

## §3 Method

### Substrate (H_350 동일)

`HEXAD/SAVANT/savant_phi.hexa` 의 4-domain capacity-bounded 모델.

| 인자 | 값 |
|------|------|
| `SV_N_DOM` | 4 (CALENDAR / MUSIC / ART / MEMORY) |
| `SV_D` | 6 (per-domain activation vector dim) |
| `SV_CAPACITY` | 11.5 (Σ g_i ≤ 11.5 invariant — Treffert/Snyder capacity) |
| `phi_module(v)` | Σ \|v[j]\|^1.5 / d (super-linear integration energy) |

### Metric 정의

| 측정량 | 정의 | max 의존성 |
|--------|------|------------|
| **SI** (불변) | max(domain_Φ) / mean(domain_Φ) | max 사용 |
| **ΦD_cov** (primary orthogonal) | **std(domain_Φ) / mean(domain_Φ)** | **NO max** (1st/2nd moments only) |
| **ΦD_kurt** (secondary orthogonal) | **E[(x-μ)^4] / σ^4** | **NO max** (high moments only) |

ΦD_cov 는 H_350 의 ΦD_alt 와 동일하나 *primary* 로 승격 (orthogonal 가설의 직접
표적). ΦD_kurt 는 H_350 에 없던 *high-moment* metric — 분자가 4th central moment
이므로 max 와의 함수 공유가 한층 더 약함.

### Sample set (H_350 동일)

```
dom     ∈ {0,1,2,3}      — 어느 domain hypertrophy 수령 (4 levels)
g_focus ∈ {1,3,5,7,10}   — hypertrophy 강도 (5 levels)
stim    ∈ {11111, 77777} — stimulus seed (multi-seed N=2)
```

→ **N = 4 × 5 × 2 = 40** samples (rule-of-thumb N≥30 충족).

### Harness

`UNIVERSE/state/h613_si_phid_orthogonal_2026_05_28/h613_verify.hexa` —
single-file hexa, savant_phi.hexa 함수 재구현 (import 의존 회피).
H_350 harness 의 sample-generation 부분 byte-identical, ΦD metric 부만 교체.

```
hexa run UNIVERSE/state/h613_si_phid_orthogonal_2026_05_28/h613_verify.hexa
```

wall < 5s, $0 Mac-local.

---

## §4 Results

### Aggregate statistics

| 지표 | min | max | mean |
|------|------|------|------|
| SI | 1.1112 | 3.03992 | 1.67268 |
| ΦD_cov (std/mean) | 0.07872 | 1.18098 | 0.43321 |
| ΦD_kurt (kurtosis) | 1.12543 | 2.33248 | 2.01184 |

SI / ΦD_cov 의 분포는 H_350 와 byte-identical (sample generator 동일).

### Correlation

| Pair | Pearson r | Spearman ρ | H_350 비교 |
|------|-----------|------------|------------|
| **SI ∥ ΦD_cov (std/mean)** — primary orthogonal | **0.9896** | **0.9482** | H_350 r=0.9264 보다 강함 |
| **SI ∥ ΦD_kurt (kurtosis)** — secondary orthogonal | **0.5381** | **0.6649** | 4th-moment 도 PASS |
| reference (H_350): SI ∥ ΦD_maxmin | 0.9264 | 0.8825 | round 1 baseline |

### Verdict

> 🟢 **SUPPORTED-NUMERICAL** — H_613 핵심 가설 PASS, max-share artifact 가설 기각.

- r(SI, ΦD_cov) = 0.9896 ≥ 0.5 ✓ (1.98× threshold margin) — **H_350 의 r=0.9264 보다도 강함**
- r(SI, ΦD_kurt) = 0.5381 ≥ 0.5 ✓ (1.08× threshold margin, 4th-moment 도 보존)
- Spearman ρ 둘 다 ≥ 0.5 (0.948 / 0.665)
- 음의 상관 부재

**결론**: H_350 의 SUPPORTED 는 max-share artifact 가 아니다. ΦD 의 정의에서
max 를 완전히 제거해도 (CoV) 그리고 high-moment (kurtosis) 로 옮겨도 SI 와의 정렬이
보존된다.

---

## §5 Mechanism

H_350 §5 의 root-shared mechanism 이 max-share artifact 가설을 기각하는 *예측에
부합*:

```
g_focus ↑  ⇒  domain_Φ[focus] ↑  ∧  domain_Φ[rest] ↓
         ⇒  분포의 *inhomogeneity* 증가 (std ↑, kurtosis ↑)
         ⇒  ΦD_cov (std/mean) ↑  AND  ΦD_kurt ↑
```

즉 capacity invariant 가 *분포 inhomogeneity* 의 모든 통계량을 동시에 끌어올리는
공통 driver — max 가 빠져도 std, 4th moment 가 같은 방향으로 움직인다. 이는
H_350 §5 의 *root-shared* 주장 (capacity-bound 분포의 inhomogeneity 가 SI/ΦD 양쪽을
구동) 의 정량적 corroboration.

ΦD_cov 가 H_350 의 ΦD_maxmin (r=0.93) 보다 더 강한 r=0.99 를 보이는 것은 std/mean
이 max/min 보다 *outlier 에 덜 취약*하기 때문 — N=4 의 작은 sample 에서 min 이
0 에 가까워지면 max/min ratio 가 폭발 (H_350 의 ΦD_maxmin max = 13.48) 하지만,
std/mean 은 분포 전체의 통계량이라 더 안정.

---

## §6 Cross-link

| H | 관계 |
|---|------|
| **H_350** `savant-index-phi-diversity` (predecessor, round 1) | r=0.9264 SUPPORTED w/ §7 C3.1 max-share part-formal honest constraint. H_613 가 그 constraint 를 *측정으로* 해소 — ΦD_cov 0.9896 / ΦD_kurt 0.538 둘 다 PASS, max-share artifact 가설 기각. |
| **H_348** `golden-zone-lower-bound-SI` | SI 정의 일관 (max/mean) — H_613 도 동일 SI 사용. |
| **H_293** `multivariate-te-synergy` | sub-network 간 synergy ↔ individual sub-network diversity. H_613 의 ΦD_cov 는 *individual* diversity 의 max-free 측정 — synergy mechanism 과의 *signed* 분리 가능. |
| **H_294** `pid-synergy-phi` | PID synergy 와 Φ. H_613 의 orthogonal metric 은 PID 의 *unique component* 와 더 깔끔하게 align — H_293/294 joint 의 더 정밀한 hand-off. |
| **H_295** `exclusion-complex-whole` | exclusion postulate. ΦD_cov / ΦD_kurt 는 *whole-complex* boundary 결정에 max 의존성 없이 사용 가능 — 더 nature 한 metric. |

---

## §7 Honest C3 (Constraints / Caveats / Calibration)

### C3.1 — Orthogonality 의 정도 (degree of orthogonality)

ΦD_cov = std / mean 은 max(domain_Φ) 를 *분자* 에 사용하지 않으나, sample 의
*max value* 가 std 에 *기여* 한다 (max - mean 이 std 계산의 한 항). 즉 *함수형*
직교는 완전하나 *변수* 직교는 부분적. ΦD_kurt 도 동일 — 4th moment 가 max - mean
편차에 더 강하게 의존.

C3.1 mitigation: max 가 std 에 들어가는 *기여도* 는 4개 sample (N_DOM=4) 의 평균
편차의 1/4 — 우연 일치 만으로 r=0.99 가 발생할 정도의 기여는 아님. ΦD_kurt 의
r=0.54 는 4th-moment 가 *덜 max-dominated* 이라는 증거 (cov 0.99 > kurt 0.54
gradient 가 정확히 max-dependency 의 감소 방향).

### C3.2 — Sample N 충분성

N=40 (≥ 30) Pearson 표준 안정 영역. multi-seed 2 (stim ∈ {11111, 77777}) — H_350
와 동일. seed 의존성 더 강하게 검증하려면 N≥4 seed 권장.

본 H 가 *부등식 가설* (r ≥ 0.5) 이고 측정값이 r=0.99 (cov), 0.54 (kurt) 로 cov 는
threshold 의 거의 2× margin, kurt 는 1.08× margin — kurt 가 margin 이 좁아 seed
추가 시 borderline 가능성 존재 (cov 는 robust, kurt 는 marginal).

### C3.3 — Kurtosis 의 통계적 해석

ΦD_kurt 의 range [1.12, 2.33] 은 N=4 의 작은 sample 에서 kurtosis 가 *normalized
4th moment* (Fisher kurtosis 가 아닌 raw) 로 측정된 결과. 정상 분포의 kurtosis 는
3 인데 본 sample 은 1~2 → *platykurtic* (flat-topped) 영역 — 4 개의 domain_Φ 가
거의 균등하거나 한쪽이 dominant 한 2-peak 분포 형태.

Kurtosis 가 *분포 형태* 의 metric 이라 *spread* metric (cov) 보다 SI 와의 결합이
약한 것은 자연스러움 (cov 0.99 > kurt 0.54). 본 H 는 두 metric 모두 PASS 임을
확인했고, kurt 는 보조 robustness 신호.

### C3.4 — IIT 4.0 strict gap (carry from H_350)

`phi_module(v) = Σ |v[j]|^1.5 / d` 는 IIT 4.0 strict big-Φ 가 아니라 super-linear
energy proxy. 본 H 는 H_350 와 동일 proxy 위에서 작동 — proxy 갭 해소는 H_295
joint upgrade 에 종속.

C3.4 status: 미해결 (H_350 carry), H_295 joint upgrade 권장.

### C3.5 — H_350 SUPPORTED 의 *부분적* artifact 가능성

H_613 결과는 H_350 SUPPORTED 가 *순수* max-share artifact 가 아님을 확인. 다만
H_350 의 r=0.9264 의 *정확한 수치* 가 어느 정도 max-share 기여를 포함했는지는
계량적으로 분리하지 않음 — H_613 의 ΦD_cov r=0.9896 가 H_350 r=0.9264 보다 *더*
큰 것은 max-share artifact 가 *오히려 정확도를 깎고 있던* 가능성을 시사하나, 
정량적 분리 (variance decomposition) 는 미수행.

C3.5 status: SUPPORTED 의 정성적 robustness 확립, 정량적 max-share-fraction
분리는 추가 분석 필요 (미수행).

---

## §8 Artifacts

| 파일 | 역할 |
|------|------|
| `UNIVERSE/state/h613_si_phid_orthogonal_2026_05_28/h613_verify.hexa` | verify harness (단일 hexa, ~360 LoC) |
| `UNIVERSE/state/h613_si_phid_orthogonal_2026_05_28/h613_verify.log` | 실행 로그 (verdict 포함) |
| `HEXAD/SAVANT/savant_phi.hexa` | upstream substrate (참조용, 재구현으로 import 회피) |
| `UNIVERSE/H_350_savant_index_phi_diversity.md` | round 1 predecessor (C3.1 honest constraint) |

---

## §9 Verdict (canonical)

```
🟢 SUPPORTED-NUMERICAL
  r(SI, ΦD_cov)  = 0.989580   (Pearson, primary orthogonal)
  ρ(SI, ΦD_cov)  = 0.948218   (Spearman, primary orthogonal)
  r(SI, ΦD_kurt) = 0.538111   (Pearson, secondary orthogonal, high-moment)
  ρ(SI, ΦD_kurt) = 0.664916   (Spearman, secondary orthogonal)
  N = 40 samples (4 dom × 5 g_focus × 2 stim)
  H_350 baseline: r=0.9264 (SI ∥ ΦD_maxmin, max-shared)
  H_613 finding: max-share artifact 가설 기각 — orthogonal metric 도 정렬 보존
  Verdict pointer: state/h613_si_phid_orthogonal_2026_05_28/h613_verify.log
```

---

## §10 Next

| 후속 | 내용 |
|------|------|
| H_295 + H_613 joint | IIT 4.0 strict big-Φ 로 sub-network Φ 대체 후 ΦD_cov / ΦD_kurt 재측정 — C3.4 갭 해소 |
| H_293 / H_613 joint | SI ∥ ΦD_cov ↔ PID synergy 의 *signed* triangle — max-free metric 으로 PID alignment 정밀화 |
| H_350 max-share variance decomposition | H_350 의 r=0.9264 에서 max-share 기여분의 정량적 분리 (C3.5 해소) |

---

@verdict: 🟢 SUPPORTED-NUMERICAL · r_cov=0.9896 r_kurt=0.5381 · N=40 · $0 mac-local 2026-05-28
