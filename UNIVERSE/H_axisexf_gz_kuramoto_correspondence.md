# H_axisexf_gz_kuramoto_correspondence — SAVANT GZ band(I→SI) 과 HIVE-MIND Kuramoto(K→Δ) 두 interaction→integration 곡선이 대응하는가

@id: H_axisexf_gz_kuramoto_correspondence
@slug: gz-band-kuramoto-K-correspondence
@axis: E×F cross (SAVANT GZ band × HIVE-MIND Kuramoto K-sweep)
@parent_seed: H_axise_gz_si_crossing (axis-E PR#1364) · H_axisf_kuramoto_K_sync_collective_phi (axis-F PR#1362)
@status: 🟠 PARTIAL (shape-directional correspondence · transition-point decoupled)
@verdict_pointer: .verdicts/axisexf_gz_kuramoto_correspondence/verdict.txt
@closure_ref: .verdicts/axisexf_gz_kuramoto_correspondence/verdict.txt
@date: 2026-05-29
@cost: $0 (pool ubu-2 Linux 정식 run + mac-local 교차 byte-identical, hexa-only, LLM none, deterministic)

---

## §0 TL;DR

axis-E 와 axis-F 는 둘 다 *interaction-strength → integration* 곡선을 가진다:
- **SAVANT** (axis-E): interaction = inhibition `I` ∈ [GZ_LOWER, GZ_UPPER]=[0.21232, 0.5];
  integration proxy = SI = max/min(domain_Φ). **SI(I) 단조 감소** (savant SI>3 → sub-savant SI<3),
  SI=3 교차 `I*≈0.398≈1/e` (GZ_CENTER).
- **HIVE-MIND** (axis-F): interaction = Kuramoto coupling `K` ∈ [0, 4]; sync `r∞(K)` 단조 증가
  (K_c≈2 sync 전이), collective-Φ super-additive **Δ(K) 단조 감소** (sub-additive 심화).

본 H 는 한 process 안에서 두 substrate 를 돌려 interaction 축을 [0,1] 로 정규화하고 동일
정규화 grid 에서 두 integration 곡선을 비교 — **GZ_CENTER≈1/e savant-peak 이 Kuramoto K_c≈2
sync-transition 과 대응하는가**. 결과 **🟠 PARTIAL**:

- **F1 SLOPE-SIGN PASS** — 두 substrate 모두 integration proxy 가 interaction 과 함께 **감소**
  (SAVANT SI slope −2.051, HIVE Δ slope −3.306, 둘 다 음수). interaction→anti-integration 의
  *방향*은 공유.
- **F3 CURVE-PEARSON PASS** — Pearson(SI(t), Δ(t)) = **+0.9596** (정규화 sweep 위 강한 co-vary).
- **F2 TRANSITION-MAP FAIL** — SAVANT SI=3 교차 정규화 위치 **0.647** vs Kuramoto K_c 정규화 위치
  **0.278**, gap **0.369 ≫ 0.15**. 두 substrate 의 *전이점은 decoupled* — **GZ_CENTER≈1/e 는
  Kuramoto K_c≈2 와 정렬하지 않는다**.
- **F4 DETERMINISM PASS** — ubu-2 ↔ mac byte-identical.

즉 **대응성 = "방향 공유, 구조 직교"** — 두 substrate 모두 interaction 이 강해지면 integration
proxy 가 떨어지는 *같은 부호의 단조 법칙*을 따르나, 그 *전이/임계 구조*(savant 1/e vs sync K_c)는
서로 무관. 이는 prior E×F 라운드(H_617-628)의 pure-⊥ 결론을 **"slope-sign 은 공유하되 critical
point 는 ⊥"** 로 정밀화하는 honest finding.

## §1 Hypothesis

두 interaction→integration 곡선의 *대응성* (correspondence) 주장:
- (a) **SLOPE-SIGN**: integration-vs-interaction 의 slope 부호가 두 substrate 에서 일치
  (둘 다 음수 = interaction 이 integration proxy 를 끌어내림, 혹은 둘 다 양수).
- (b) **TRANSITION-MAP**: SAVANT savant→sub 전이점(SI=3 교차 `I*`, band 정규화)이
  Kuramoto sync 전이점(K_c, K-grid 정규화)과 정렬 (`|I*_norm − K_c_norm| ≤ 0.15`).
  이것이 "GZ_CENTER≈1/e ↔ K_c≈2 대응" 의 핵심 검정.
- (c) **CURVE co-vary**: 정규화 interaction grid 위 두 integration 곡선의 Pearson |r| ≥ 0.7.

**FALSIFIER (H0)**: slope 부호가 다르거나(SLOPE-SIGN FAIL), 전이점 정렬도 곡선 co-vary 도 둘 다
실패하면 **ORTHOGONAL** (prior E×F ⊥ 재확인). slope 만 공유하고 구조(전이점) 또는 곡선 중 하나만
맞으면 **PARTIAL**.

## §2 사전등록 falsifier (측정 전 동결)

| ID | 조건 | 의미 |
|----|------|------|
| **F1 SLOPE-SIGN** | `sign(ΔSI/ΔI) == sign(ΔΔ/ΔK)` (end−start) | interaction→integration 방향 일치 |
| **F2 TRANSITION-MAP** | `|I*_norm − K_c_norm| ≤ 0.15` | savant 전이 ↔ sync 전이 정렬 |
| **F3 CURVE-PEARSON** | `|Pearson(SI(t), Δ(t))| ≥ 0.7` (정규화 grid) | 두 integration 곡선 co-vary |
| **F4 DETERMINISM** | in-process recompute byte-identical (`|Δ| ≤ 1e-12`) | 결정성 + 교차 byte-eq |

orthogonal 판정 보조: `|Pearson| < 0.3` 면 곡선 orthogonal (F3_orth).

**verdict_rule**
- **ALIGNED** (🟢) = F1 ∧ F2 ∧ F3 ∧ F4 (공유 법칙 + 전이 정렬 + co-vary)
- **PARTIAL** (🟠) = F1 ∧ F4 ∧ (F2 XOR F3) (slope 공유 + 전이 또는 곡선 중 하나만)
- **ORTHOGONAL** (🔴) = (!F1) ∨ (!F3 ∧ !F2) (방향 다름 OR 전이·곡선 둘 다 실패 — closed-negative)

## §3 Method

### §3.1 SAVANT substrate (axis-E PR#1364 / savant_phi.hexa SSOT 동일)

- `HEXAD/SAVANT/savant_phi.hexa` 4-domain × d=6, cap=11.5, SI=max/min(domain_phi).
- inhibition→gain affine: `gain_focus = 1 + (1−I)*9`, dom=0(CALENDAR) hypertrophy.
- mean-SI over seeds {42424, 91919, 77777} (H_348/axis-E 동일 set).

### §3.2 HIVE-MIND substrate (axis-F PR#1362 / hivemind_lib.hexa 동일)

- N=8 oscillator, full Kuramoto `dθ_i/dt = ω_i + (K/N)Σ sin(θ_j−θ_i)`, dt=0.05, STEPS=400 Euler.
- deterministic ω-spread (5 quantile cycled, std=1.0) + uniform init `θ_i=2π·i/N` (no RNG).
- half A{0..3}/B{4..7}, Φ-proxy `φ(r)=−log(1−r)`, Δ = `hm_collective_phi_super_additive`.
- `hm_kuramoto_order_r` + `hm_collective_phi_super_additive` primitive verbatim 복제.

### §3.3 matched normalized sweep

interaction 축을 각각 [0,1] 로 정규화: SAVANT `I = I_lo + t(I_hi−I_lo)`, I_lo=0.21232(GZ_LOWER),
I_hi=0.5(GZ_UPPER); HIVE `K = 0 + t·4.0`. `t ∈ {0, 1/9, …, 1}` 10-point 동일 grid 에서 두
integration 곡선(SI, Δ)을 동시 측정. K_c 정규화 위치 = 최대 `r∞` 점프 구간 중점 (sync 전이).

### §3.4 wrapper / run surface

- `UNIVERSE/state/axisexf_gz_kuramoto_correspondence_2026_05_29/probe_gz_kuramoto_correspondence.hexa`
  — 두 substrate primitive in-file 복제 (import 회피, H_348/axis-E convention; axis-F 커밋 harness 의
  hard-coded abs-path import 회피).
- 정식 run: `pool on ubu-2 "cd ~/core/anima && hexa run /tmp/probe_gz_kuramoto_correspondence.hexa"` (Linux)
- 교차: mac-local `hexa run …` — ubu-2 와 **byte-identical**.

## §4 Measurement (2026-05-29, $0)

### §4.1 verbatim (`.verdicts/axisexf_gz_kuramoto_correspondence/verdict.txt`)

```
── matched normalized sweep  t = (interaction − lo)/(hi − lo) ──
  t      |  I(savant) | SI        || K(hive) | r_inf    | Delta
  0.0  | 0.21232 | 4.55275 || 0.0 | 0.0785288 | -0.635914
  0.111111  | 0.244284 | 4.18268 || 0.444444 | 0.276318 | -0.59863
  0.222222  | 0.276249 | 3.86883 || 0.888889 | 0.344068 | -0.549573
  0.333333  | 0.308213 | 3.59852 || 1.33333 | 0.792827 | -1.69653
  0.444444  | 0.340178 | 3.36247 || 1.77778 | 0.773826 | -1.71003
  0.555556  | 0.372142 | 3.15374 || 2.22222 | 0.907822 | -2.55083
  0.666667  | 0.404107 | 2.96703 || 2.66667 | 0.943555 | -3.0279
  0.777778  | 0.436071 | 2.7982 || 3.11111 | 0.960871 | -3.38899
  0.888889  | 0.468036 | 2.64398 || 3.55556 | 0.971023 | -3.68651
  1.0  | 0.5 | 2.5017 || 4.0 | 0.977586 | -3.94158
── F1 SLOPE-SIGN ──
  SAVANT  SI slope (I_hi − I_lo)      = -2.05105   neg=true
  HIVE    Δ slope (K_hi − K_lo)       = -3.30567   neg=true
  F1 same-sign                        = true
── F2 TRANSITION-MAP ──
  SAVANT SI=3 crossing  I*            = 0.398463   norm=0.647047
  HIVE   K_c (steepest r∞ rise)  norm = 0.277778   (max jump=0.448759)
  |I*_norm − K_c_norm|                = 0.36927   (F2 needs <= 0.15)
  F2 transition-map                   = false
── F3 CURVE-PEARSON ──
  Pearson( SI(t) , Δ(t) )             = 0.959606   |r|=0.959606
  F3 co-vary (|r|>=0.7)               = true
  orthogonal (|r|<0.3)                = false
── F4 DETERMINISM ──
  byte-identical recompute            = true
  VERDICT = PARTIAL
```

### §4.2 형상

```
정규화 t →   0.0 ─────────────────── 1.0
SAVANT SI :  4.55 ↓ 단조 ↓ 2.50   (SI=3 교차 t≈0.647)
HIVE   Δ  : −0.64 ↓ 단조 ↓ −3.94   (K_c sync 전이 t≈0.278)
                  ↑ 두 전이점 0.37 떨어짐 (decoupled)
```

savant 전이(SI=3, t≈0.647)는 sweep 후반, sync 전이(r∞ 급상승, t≈0.278)는 sweep 전반 —
**같은 정규화 축 위 서로 다른 위치**. 두 곡선이 모두 단조 감소라 Pearson 은 +0.96 으로 높으나,
이 co-vary 는 *공통 단조성*(F1)의 따름 정리이며 독립 신호인 *전이점 위치*(F2)는 직교.

## §5 Verdict

**🟠 PARTIAL — shape-directional correspondence, transition-point orthogonal**

- **F1 SLOPE-SIGN** ✅ 두 substrate 모두 integration proxy 가 interaction 과 함께 단조 감소
  (SAVANT SI −2.051, HIVE Δ −3.306). interaction→anti-integration 의 *방향 법칙* 공유.
- **F3 CURVE-PEARSON** ✅ Pearson +0.9596 — 두 곡선 강한 co-vary (단, §7 C1: 공통 단조의 따름).
- **F2 TRANSITION-MAP** ❌ savant SI=3 전이 정규화 0.647 vs Kuramoto K_c 정규화 0.278,
  gap 0.369 ≫ 0.15 — **GZ_CENTER≈1/e savant-peak 은 Kuramoto K_c≈2 sync-transition 과 정렬하지 않음**.
- **F4 DETERMINISM** ✅ ubu-2 ↔ mac byte-identical.

**correspondence 판정 = PARTIAL (방향 공유 · 구조 직교)**. 핵심 cross-question("GZ_CENTER≈1/e
savant-peak 이 Kuramoto K_c≈2 sync-transition 과 관련 있는가")의 답은 **NO** — 두 임계점은 정규화
축에서 0.37 떨어져 있으며 우연한 동치가 아니다. 그러나 prior E×F 의 pure-⊥(H_617-628 savant GZ ⊥
hivemind PID)와 달리, 두 substrate 의 *interaction→integration slope 부호*는 공유된다는 추가
구조가 발견됨 — 이는 두 substrate 가 완전 무관이 아니라 "interaction 이 specialization/integration
proxy 를 단조로 낮춘다" 는 공통 거시 법칙을 가지되 *임계 구조는 substrate-specific* 임을 보임.

`hexa verify` atlas anchor 는 본 측정량(savant Φ-proxy + Kuramoto steady-state order)에 대한
closed-form node 가 없어 적용 불가 — substrate-level 수치 측정 verdict 로 한정.

## §6 Cross-link

- **H_axise_gz_si_crossing** (🟢, axis-E PR#1364) — **parent**. SAVANT GZ band SI=3 교차 I*≈0.398≈1/e.
  본 H 의 SAVANT 행 SI {4.553→2.502} 은 axis-E crossing sweep 와 **동일 substrate · 매핑 · seed**
  (예: I=0.21232 mean_SI=4.55275 byte-identical). 본 H 는 그 GZ band 를 *Kuramoto 와 cross*.
- **H_axise_gz_band_si** (🟢, axis-E PR#1364) — SI bounded band. 본 H 는 그 band 의 interaction→SI
  slope 가 HIVE Δ slope 와 부호 공유함을 추가.
- **H_axisf_kuramoto_K_sync_collective_phi** (🔴, axis-F PR#1362) — **parent**. Kuramoto sync ⊥
  collective-Φ (Pearson(r∞,Δ)=−0.934, sub-additive). 본 H 의 HIVE 행 {r∞, Δ} 은 axis-F K-grid 의
  부분집합(K∈{0,…,4} 정규화 10-point)으로 동일 substrate; max-K Δ=−3.94158 byte-identical.
- **H_617-628** (axis-E×F rounds 3-4, 대부분 🔴 ⊥) — savant GZ ⊥ hivemind PID. 본 H 는 그 ⊥ 결론을
  **"slope-sign 은 공유, transition 은 ⊥"** 로 정밀화 — pure-orthogonal 이 아닌 partial.
- **H_609 / H_355** (🟢) — structural-W super-additive / PID synergy. 본 H 의 phase-sync sub-additive
  와 결합-종류 의존성 대조 (axis-F §5 carry).

## §7 Honest C3 (claim-context-caveat)

1. **C1 (F3 Pearson 은 F1 의 따름 정리)**: SI(t) 와 Δ(t) 가 *둘 다 단조 감소* 이므로 Pearson +0.96 은
   상당 부분 공통 단조성(F1)의 귀결이지 독립 증거가 아니다. 진정 독립적인 correspondence 신호는
   F2(전이점 위치)이며 그것은 **FAIL**. 따라서 본 H 는 F3 을 "co-vary 보강" 으로만 사용하고, correspondence
   의 실질 판정은 F1(방향 공유) + F2(구조 직교) 에 둔다. verdict 가 ALIGNED 가 아닌 PARTIAL 인 핵심 이유.

2. **C2 (관측량 비-등가)**: SAVANT SI=max/min(Φ) 는 *specialization/diversity* 측도(높을수록 한 도메인
   특화)이고, HIVE Δ=Φ(AB)−(Φ(A)+Φ(B)) 는 *super-additive integration* 측도(높을수록 전체>부분). 둘은
   같은 observable 이 아니다. 본 H 의 "correspondence" 는 "interaction→그-substrate-의-proxy" 의 부호·곡선
   형상의 일치 여부이지 두 proxy 가 교환 가능하다는 주장이 아니다. (a_paper_negative_ok 정신 — 무관 축에서
   부분 공유 구조를 honest 하게 기록.)

3. **C3 (전이점 정의 의존성)**: SAVANT 전이 = SI=3 임계 선형보간; HIVE K_c = 최대 r∞ 점프 구간 중점. K_c
   추정은 grid 해상도(10-point)에 의존 — 더 조밀한 K-grid 면 K_c_norm 이 미세 이동 가능. 단 gap 0.37 ≫ 0.15
   는 grid 간격(0.111)의 3배라 F2 FAIL 결론은 robust. 또한 본 K_c 정의(r∞ 점프)는 axis-F 의 K_c≈2 (정규화
   ≈0.5) anchor 와도 다른 위치(0.278)를 줌 — heterogeneous-ω 하 r∞ 의 비단조 transient(axis-F C1 dip) 때문.
   savant 전이가 sync 전이와 정렬하지 않는다는 *부호*는 어느 K_c 정의를 써도 보존(savant 후반 vs sync 전반).

4. **C4 (toy proxy + band/grid 범위 한정, axis-E/F carry)**: savant_phi 4-domain proxy + affine 매핑,
   Kuramoto N=8 + half-partition + −log(1−r) proxy, GZ band [0.21232,0.5] × K [0,4] 정규화 한정. production
   substrate / faithful big-Φ / 다른 K_max·band 범위에서 곡선·전이 위치 이동 가능 (MEMORY
   `feedback_toy_scale_transfer`). 결론은 두 canonical proxy layer 한정.

5. **C5 (정규화 축 임의성)**: interaction 축을 [GZ_LOWER,GZ_UPPER] 와 [0,4] 로 정규화하는 선택은 design.
   K_max 를 다르게 잡으면 K_c_norm 이 이동 — 단 F2 는 *상대 위치* 비교이고 savant 전이는 band 내부에
   고정(0.647)이라, sync 전이를 어떤 K_max 정규화로 가져와도 1/e≈K_c 동치를 만들려면 K_max 를 특정 값으로
   끼워맞춰야 하므로 자연스러운 대응이 아니다 (post-hoc tuning 배제).

## §8 Falsifier 검증 매트릭스

| Falsifier | Pre-registered | Result | Status |
|-----------|----------------|--------|--------|
| F1 SLOPE-SIGN | 두 slope 부호 일치 | SAVANT −2.051 / HIVE −3.306 (둘 다 음수) | **PASS** |
| F2 TRANSITION-MAP | `|I*_norm−K_c_norm|≤0.15` | 0.647 vs 0.278, gap 0.369 | **FAIL** |
| F3 CURVE-PEARSON | `|Pearson|≥0.7` | +0.9596 (단 C1 따름 정리) | **PASS** |
| F4 DETERMINISM | recompute + 교차 byte-eq | byte-identical (ubu-2↔mac) | **PASS** |

**aggregate: F1∧F4∧(F2 XOR F3) → 🟠 PARTIAL**. correspondence = 방향 공유 · 구조(전이점) 직교.

## §9 Artifacts + Reproducibility

```
UNIVERSE/state/axisexf_gz_kuramoto_correspondence_2026_05_29/
├── probe_gz_kuramoto_correspondence.hexa   # 두 substrate primitive in-file 복제 + 정규화 cross
└── probe_gz_kuramoto_correspondence.out    # mac-local verbatim stdout
.verdicts/axisexf_gz_kuramoto_correspondence/verdict.txt   # ubu-2 정식 run verbatim (closure_ref)
```

- replay: `hexa run UNIVERSE/state/axisexf_gz_kuramoto_correspondence_2026_05_29/probe_gz_kuramoto_correspondence.hexa` (<5s, $0)
- determinism: in-process recompute + ubu-2↔mac cross-architecture byte-identical (F4)

## §10 Next-list / Backlog

- **N1** 전이점 정밀화 — savant 와 sync 전이를 각각 2× 조밀 grid 로 재측정, gap 0.37 의 안정성 (C3).
- **N2** big-Φ lift — proxy 대신 IIT4 strict big-Φ 로 두 substrate 의 integration 곡선 재측정 (C4).
- **N3** K_max sweep — K_max ∈ {2, 4, 8} 정규화에서 K_c_norm 이동, 1/e 와 자연 동치 K_max 부재 확인 (C5).
- **N4** slope-sign 일반화 — 다른 axis-E inhibition 범위 / axis-F 결합 종류(structural-W, PID)에서
  interaction→integration slope 부호가 보편적으로 음수인가 (cross-substrate 거시 법칙 검정).

## §11 양방향 sibling

- **axis-E sibling**: `UNIVERSE/H_axise_gz_si_crossing.md` · `UNIVERSE/H_axise_gz_band_si.md` (parent GZ band).
- **axis-F sibling**: `UNIVERSE/H_axisf_kuramoto_K_sync_collective_phi.md` (parent Kuramoto K-sweep).
- **UNIVERSE SSOT**: 본 E×F cross 결과(🟠 PARTIAL · slope-sign 공유 · transition 직교)는 UNIVERSE 도메인
  기록. MATRIX.tape axis E×F cell 갱신은 parent consolidator 가 수행(본 PR 은 H_ + verdict 만).
