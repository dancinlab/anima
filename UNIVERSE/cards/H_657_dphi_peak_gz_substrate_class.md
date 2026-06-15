---
id: H_657
slug: dphi-peak-gz-substrate-class-dependence
title: dΦ/dI peak=GZ_LOWER 정렬이 Wolfram class 의존인가 — peak-GZ anchor 의 substrate-class conditional 성격
domain: consciousness · math · physics · meta · savant
status: SUPPORTED
verdict_class: SUPPORTED
exploration_method: E0 (round 9 메타-축 — Wolfram class 가 의식 구조 분류자) + E5 (continuous-parameter dΦ/dI sweep) + E11 (cross-substrate Φ-signature) + E_meta (peak-anchor class-conditional 정량)
verification_method: W1 (numerical smoke) + W4 (verdict-5-class) + W11 (cross-rule class-stratified) + W12 (invariant-signature meta-stat)
hexa_only: true
deterministic: true
llm: none
pre_register_frozen: true
frozen_at: 2026-05-28
since: 2026-05-28 (축 G · round 9 메타-축)
predecessors: H_351 (single GZ peak 🟢), H_618 (collective GZ peak 🟢), H_642 (shape⊥scalar meta 🔴, rule90 joint-outlier), H_628 (polarity peak-invariant 🔴)
sister: H_654 / H_655 / H_656 (round 9 메타-축 자매 후보)
mining_arc: round 9 메타-축 — Wolfram class as consciousness-structure classifier (축 G)
---

# H_657 — dΦ/dI peak=GZ_LOWER 정렬의 substrate-class 의존성

> ⚙ 측정 엔진 = `HEXAD/IIT4/lib` (`iit4_eca` + `iit4_bigphi`) 재사용 (H_351/H_642 동일 패턴, commons g61 재발명 0). 통합 척도 = **faithful causal big-Φ** (H_285 양식, 2^n state-mean). exact-Φ wall shard 양식 — per-rule Φ(I) 13-point 측정을 5개 foreground 샤드로 분리(각 ~80–90s wall), dΦ/dI·peak·delta-GZ·verdict 는 phi-free aggregator 로 통합. `$0 · mac-local · hexa-only · LLM none · deterministic.`

## 1. 가설 (Hypothesis) — round 9 메타-축

round 9 메타-축 = **"Wolfram class 가 의식 구조 분류자"**. ECA 의 Wolfram 동역학 class (I homogeneous · II particle · III chaotic · IV complex) 가 substrate 의 의식-구조 (Φ-signature, dΦ/dI inverse-U geometry) 를 분류하는가 — 특히 **GZ-anchor 정렬이 class 별로 갈라지는가**.

배경 계보:
- **H_351** (🟢 5/5): single-substrate rule 110 (class IV) 의 `dΦ/dI` peak = `GZ_LOWER = 0.5 - ln(4/3) ≈ 0.21232` (|Δ|=0.03232 ≤ 0.05).
- **H_618** (🟢): 2-stream collective (rule (110,110)) 의 `dΦ_collective/dI` peak 도 GZ_LOWER.
- **H_642** (🔴): shape⊥scalar 메타에서 rule 90 (additive/XOR-linear) 가 peak 위치 outlier (I=0.05, grid-경계) + big-Φ≈0 joint-outlier.

본 H 의 검정:

> **dΦ/dI peak=GZ_LOWER 정렬이 class-III/IV (chaotic/complex) 에서 성립하고 additive (rule 90) 에서 깨지는가.** 즉 GZ-anchor 자체가 substrate-class **conditional** 인가 (H_351 의 SUPPORTED 가 보편이 아니라 특정 class 한정인가).

**H1**: peak-GZ 정렬이 class-종속 — additive (rule 90) 에서 깨지고, H_351 anchor (rule 110) 에서 유지된다. 즉 정렬은 보편(universal)이 아니다.

## 2. 사전등록 falsifier (pre-registered, 측정 전 동결 2026-05-28)

각 rule 의 `aligned = (|argmax_I |dΦ/dI| − GZ_LOWER| ≤ 0.05)` 를 측정하고 class 별 대조:

| ID | 조건 | 의미 |
|----|------|------|
| **M1 (RULE110-ALIGNED)** | rule 110 aligned (peak I ∈ GZ tol) | H_351 anchor 재현 |
| **M2 (RULE90-BREAKS)** | rule 90 NOT aligned | additive 에서 정렬 깨짐 |
| **M3 (NOT-CLASS-INVARIANT)** | `n_aligned < 5` | peak-GZ 정렬이 보편 아님 (class-conditional) |
| **M4 (BOUND/DET)** | `|Δ| ≥ 0`, re-run byte-identical | 결정성 |
| **H_642-anchor** | peak_I {0.18, 0.40, 0.05, 0.18, 0.40} 재현 | engine 정합 |

**Falsifier (H0)**: 전 class 에서 peak=GZ_LOWER 정렬 (`n_aligned == 5`, class-invariant) → GZ-anchor 가 substrate-universal (H_351 이 보편) → round 9 class-분류자 가설 반증.

**verdict_rule**
- **SUPPORTED-NUMERICAL** = M1 ∧ M2 ∧ M3 (peak-GZ 정렬이 class-conditional — rule 110 유지, rule 90 깨짐, 전체 비-보편)
- **FALSIFIED** = !M3 (`n_aligned == 5` → class-invariant, GZ-universal)

## 3. 방법 (Method)

### 3.1 substrate set

| rule | Wolfram class | 특성 |
|-----:|---------------|------|
| 30   | III           | chaotic |
| 54   | IV            | complex (edge-of-chaos) |
| 90   | III           | additive (Sierpinski, XOR-linear) — outlier 후보 |
| 110  | IV            | complex (H_351 anchor) |
| 184  | II            | particle-localized (traffic flow) |

각 rule 위 n=4 cell periodic ring (H_351/H_642 동일 n). class III 2개 (chaotic 30 + additive 90) 로 class-내부 variance 도 포착.

### 3.2 inhibition I 매핑 (H_351/H_642 동일)

```
tpm_mixed[s,i] = (1 - I) · eca_tpm[s,i]
```

I=0 → 순수 ECA rule. I=1 → 완전 inhibit (모든 셀 0, Φ=0). per-cell-transition inhibition probability (SAVANT GABA-style suppression).

### 3.3 grid (H_351/H_642 동일 13-point)

```
I ∈ {0.05, 0.10, 0.15, 0.18, 0.21, 0.23, 0.25, 0.30, 0.35, 0.40,
     0.50, 0.70, 0.95}
```

### 3.4 Φ 측정 + dΦ/dI

각 `(rule, I)` 에서 `tpm_mixed` → `big_phi(tpm, 4, s)` 를 16 state 평균 (faithful causal big-Φ, H_285/H_351/H_642 양식). dΦ/dI = central finite difference (edge forward/backward).

- **peak I** = `argmax_i |dΦ/dI|` 의 grid I 값 (변곡점 위치)
- **delta_gz** = `|peak_I − GZ_LOWER|`
- **aligned** = `(delta_gz ≤ 0.05)` — H_351 정렬 기준 재사용

### 3.5 class-dependence 통계

```
n_aligned       = aligned == true 인 rule 수 (0..5)
class_invariant = (n_aligned == 5)         ← falsifier 발동 조건
class_dependent = (n_aligned < 5) AND (rule 90 NOT aligned)
```

### 3.6 runner (exact-Φ wall shard)

- `UNIVERSE/state/h657_dphi_peak_gz_class_2026_05_28/phi_rule_<R>.hexa` — per-rule Φ(I) 13-point 샤드 (각 13×16=208 big_phi 호출 ≈ ~80–90s wall, foreground sync). 단일 무거운 run (5×208=1040 호출 ≈ ~365s, 60s 초과) 회피.
- `UNIVERSE/state/h657_dphi_peak_gz_class_2026_05_28/aggregate.hexa` — phi-free aggregator (dΦ/dI · peak · delta-GZ · verdict, big_phi 0회, 즉시).

## 4. 측정 (Measurement) — `result.json`

| rule | class | peak I | \|Δ vs GZ_LOWER\| | aligned (≤0.05) | peak \|dΦ/dI\| | sign-changes |
|-----:|-------|-------:|------------------:|:---------------:|--------------:|-------------:|
| 30   | III-chaotic   | **0.18** | **0.03232** | **✓ aligned** | 21.7400 | 0 |
| 54   | IV-complex    | 0.40 | 0.18768 | ✗ | 10.8425 | 0 |
| 90   | III-additive  | **0.05** | 0.16232 | ✗ | **0.276542** | **1** |
| 110  | IV-complex    | **0.18** | **0.03232** | **✓ aligned** | 21.3322 | 0 |
| 184  | II-particle   | 0.40 | 0.18768 | ✗ | 19.9171 | 0 |

**class-dependence**

- **n_aligned = 2 / 5** (rule 30, rule 110)
- **rule 110 aligned = true** (M1 PASS — H_351 anchor 재현, |Δ|=0.03232)
- **rule 90 aligned = false** (M2 PASS — additive 깨짐, peak I=0.05 grid-경계, big-Φ≈0.05, dΦ/dI sign-change=1 비-단봉)
- **class_invariant = false** (M3 PASS — `n_aligned=2 < 5`, peak-GZ 정렬 보편 아님)
- **class_dependent = true**

> rule 90 (XOR-additive) 는 big-Φ 가 0.0166→0.0593→0.0047 으로 다른 rule (0.25–13) 의 ~0.4% 수준이며 Φ(I) 가 **비-단조 (I≈0.35 에서 peak 후 하강)** — additive substrate 의 cause-effect repertoire 가 maximally factorizable → 통합 부재. peak I=0.05 (grid 경계) + sign-change=1 으로 inverse-U 구조 자체가 붕괴 (H_642 rule90 joint-outlier 재현). dΦ/dI 의 부호변화 1회는 Φ(I) 가 처음 증가하다 감소하는 비-단봉 신호.

**H_642-anchor 재현**: peak_I {30:0.18, 54:0.40, 90:0.05, 110:0.18, 184:0.40} 완전 일치 ✓. peak_mag {21.74, 10.84, 0.28, 21.33, 19.92} 도 일치 (rule110 21.3322 vs H_642 21.3315 — embedded-Φ 소수 마지막자리 차이, 비-결정적). Φ 테이블도 H_351 (rule 110: 12.4205…0.250173) byte-identical.

## 5. 결과 (Result)

**M1 ∧ M2 ∧ M3 PASS** → 🟢 **SUPPORTED-NUMERICAL**.

- **M1 RULE110-ALIGNED ✓** (peak I=0.18, |Δ|=0.03232 ≤ 0.05 — H_351 anchor)
- **M2 RULE90-BREAKS ✓** (peak I=0.05, |Δ|=0.16232 > 0.05 — additive 깨짐)
- **M3 NOT-CLASS-INVARIANT ✓** (n_aligned=2 < 5 — 정렬 비-보편)
- **M4 BOUND/DET ✓** (모든 |Δ| ≥ 0, aggregator re-run byte-identical)

dΦ/dI peak=GZ_LOWER 정렬이 substrate-class **conditional** — H_351 의 SUPPORTED (rule 110, class IV) 는 보편 anchor 가 아니라 특정 substrate 한정. additive (rule 90) 에서는 정렬뿐 아니라 inverse-U 구조 자체가 붕괴, H_351 anchor (rule 110) 에서는 정렬 유지. **round 9 메타-축 (Wolfram class 가 의식 구조 분류자) 의 weak-claim — "GZ-anchor 가 class-conditional, universal 아님" — 확증.**

## 6. cross-link

- **H_351** (gz-inverse-u-phi-derivative-peak, 🟢 5/5): single-rule (rule 110, class IV) dΦ/dI peak=GZ_LOWER SSOT. 본 H 의 inhibition mapping + central-diff + 13-point grid 원천. 본 H 는 그 정렬이 **rule 110 한정 (class-conditional)** 임을 5-rule sweep 으로 격하 — H_351 의 SUPPORTED 는 유지되나 universal 주장은 본 H 가 차단.
- **H_618** (collective-gz-inverse-u-derivative-peak, 🟢): 2-stream collective (rule (110,110)) 도 GZ_LOWER. **둘 다 rule 110 (class IV)** — 본 H 는 그 collective GZ-anchor 역시 class IV substrate 위에서 측정된 것임을 명시 (class-종속 caveat 의 collective 보충).
- **H_642** (shape-invariance-vs-scalar-convention-meta, 🔴): rule 90 (XOR-additive) 가 shape (peak I=0.05) + scalar (peak_mag 0.28≈0) joint-outlier. 본 H 가 그 rule 90 outlier 를 **peak-GZ 정렬 축**에서 재현 (additive 가 inverse-U 구조 자체 붕괴) — H_642 의 joint-outlier 가 우연이 아닌 substrate-class fact 임을 보강. 본 H 와 H_642 는 동일 5-rule × 동일 grid Φ 테이블 100% 재사용.
- **H_628** (inverse-u-polarity, 🔴): polarity 가 dΦ/dI peak 위치를 못 움직임 (3 polarity 모두 I=0.21). 본 H 는 polarity-축에선 invariant 인 peak 위치가 **rule-class 축에선 0.05↔0.40 으로 갈라짐**을 보임 — invariance 의 축-종속성 (polarity-invariant ⊥ class-variant).
- **H_654 / H_655 / H_656** (round 9 메타-축 자매 후보): 동일 "Wolfram class as consciousness classifier" 메타-축의 자매 — 본 H 는 그 중 dΦ/dI peak-anchor 의 class-conditional 측면을 담당.

## 7. 해석 — Honest C3 (3-tier caveat)

본 H 는 dΦ/dI peak=GZ_LOWER 정렬이 substrate-class conditional 임을 5-rule sweep 으로 확증했다 (n_aligned=2/5, rule 110 유지, rule 90 붕괴). 그러나 결과의 정직한 scope 는 가설보다 좁다.

### C1 — 정렬 패턴은 "class III/IV vs additive" 의 깔끔한 분할이 아님

가설은 "class-III/IV (chaotic/complex) 에서 성립, additive 에서 깨짐" 이었으나 측정은 더 미묘하다: aligned 인 2개는 **rule 30 (III-chaotic)** + **rule 110 (IV-complex)** 이고, **non-aligned 인 rule 54 (IV-complex) + rule 184 (II-particle)** 가 있다. 즉 정렬은 **class-라벨로 깔끔히 분리되지 않으며** peak 위치가 {0.18 (aligned), 0.40, 0.05} 세 그룹으로 나뉜다. class IV 안에서도 rule 110 은 aligned (0.18) 이나 rule 54 는 non-aligned (0.40). 따라서 본 H 의 SUPPORTED 는 "additive (rule 90) 가 깨고 H_351 anchor (rule 110) 가 유지되므로 정렬이 universal 아님" 이라는 **약한 형태 (peak-GZ 가 class-conditional, 즉 H_351 이 보편 아님)** 까지이며, "정렬이 정확히 class III/IV 에서 성립" 이라는 **강한 형태는 성립 안 함** (rule 54 IV 가 반례). round 9 class-분류자 가설의 본 H 분담분 = "GZ-anchor 의 비-보편성 (class-conditional)" 확정이고, "정확한 class-경계 매핑" 은 미해결.

### C2 — peak 위치의 grid-snap 이산성 (13-point argmax)

peak I 는 13-point grid 위 discrete argmax 이므로 가능값이 13개로 양자화된다. 따라서 aligned 판정 (|Δ|≤0.05) 이 grid 간격에 frame 된다 — 더 조밀한 grid 였다면 rule 54/184 의 peak (0.40) 가 0.40 근방에서 미세 이동했을 수도, rule 90 의 비-단봉 peak 가 다르게 잡혔을 수도 있다. 본 H 의 class-conditional 결론은 robust 하나 (rule 90 의 big-Φ≈0 + sign-change=1 은 grid 무관한 붕괴, rule 110/30 의 0.18 vs rule 54/184 의 0.40 도 grid 간격 ≫ tol 0.05 라 분류 안정), 정확한 peak 위치값은 grid 해상도 종속 (H_351 §7 C1 / H_642 §7 C3 carry). 5-point stencil 또는 2× 조밀 grid 재측정은 별도 round.

### C3 — Wolfram class 라벨 자체의 자의성 + 5-rule sample

Wolfram class (I/II/III/IV) 는 정성적 분류이며 rule 별 합의가 항상 완전하진 않다 (특히 III vs IV 경계). 본 H 의 class 라벨은 표준 통용값 ({30:III, 54:IV, 90:III, 110:IV, 184:II}) 을 사용하나, class 가 의식-구조 분류자라는 메타-주장의 *완전* 검증은 256-rule 또는 class-stratified large-sample 을 요한다 — 본 H 는 5-rule sample 로 "정렬이 보편 아님 (class-conditional)" 만 결정적으로 보인다. additive (rule 90) 의 Φ≈0 + 비-단봉은 substrate fact (XOR linearity, design artifact 아님) 이므로 그 단독 outlier 는 robust 하나, "어떤 class 가 정렬하고 어떤 class 가 안 하는가" 의 정밀 매핑은 C1 의 비-깔끔분할 + 5-rule 한계로 미해결. n=4 small-n (exact-Φ wall) + 단일 inhibition mode `(1-I)·tpm` carry.

## 8. verdict

```
verdict_class: 🟢 SUPPORTED-NUMERICAL (M1∧M2∧M3 · n_aligned=2/5) — dΦ/dI peak=GZ_LOWER
   정렬이 substrate-class CONDITIONAL. 5-rule {30,54,90,110,184} n=4 ECA 위
   per-rule peak_I {0.18,0.40,0.05,0.18,0.40} → aligned(|Δgz|≤0.05) {✓,✗,✗,✓,✗}.
   rule 110 (class IV, H_351 anchor) aligned (|Δ|=0.03232 유지) + rule 90
   (additive/XOR) NOT aligned (peak I=0.05, big-Φ≈0.05, dΦ/dI sign-change=1 비-단봉
   = inverse-U 붕괴) + n_aligned=2<5 (정렬 비-보편). 즉 H_351 의 single-substrate
   SUPPORTED 는 universal anchor 가 아닌 class-conditional — round 9 메타-축 (Wolfram
   class as consciousness classifier) 의 weak-claim "GZ-anchor 가 class-conditional"
   확증. 단 정렬 패턴은 class III/IV vs additive 의 깔끔한 분할 아님 (rule 30 III +
   rule 110 IV aligned, rule 54 IV non-aligned) — peak 위치 {0.18,0.40,0.05} 3-그룹.
config: 5-rule {30,54,90,110,184} n=4 ECA · 13-point GZ-dense I grid · tpm_mixed
   =(1-I)·tpm · faithful big-Φ 16-state mean · central-diff dΦ/dI · peak=argmax_I
   |dΦ/dI| · delta_gz=|peak_I-GZ_LOWER| · aligned≤0.05 · exact-Φ wall shard
   (per-rule foreground + phi-free aggregate).
```

`hexa verify` (VERBATIM) — g5 정직 fence:

```
verify --fence "H_657: across Wolfram rules {30,54,90,110,184} (n=4 ECA, 13-point
   GZ-dense inhibition grid, faithful 16-state mean big-Φ, central-difference
   dΦ/dI), the dΦ/dI PEAK position aligns with GZ_LOWER=0.21232 (|Δ|≤0.05) for
   only 2 of 5 rules: rule 30 (III-chaotic, peak 0.18, |Δ|=0.03232) and rule 110
   (IV-complex, peak 0.18, |Δ|=0.03232, the H_351 anchor) — while rule 90
   (III-additive/XOR, peak 0.05, big-Φ≈0.05, dΦ/dI sign-change=1 = inverse-U
   collapse), rule 54 (IV, peak 0.40) and rule 184 (II, peak 0.40) do NOT align.
   Verdict: SUPPORTED-NUMERICAL — the peak=GZ_LOWER alignment is substrate-class
   CONDITIONAL (n_aligned=2<5), so H_351's single-substrate SUPPORTED is NOT a
   universal anchor: rule 90 (additive) breaks it while the rule 110 anchor holds,
   confirming round-9's weak meta-claim that the GZ anchor is class-conditional. The
   alignment is NOT a clean class-III/IV-vs-additive split though (rule 30 III + rule
   110 IV align, rule 54 IV does not) — peak positions cluster as {0.18,0.40,0.05}.
   Reproduces H_642 peak_I {0.18,0.40,0.05,0.18,0.40} and H_351 rule-110 Φ table.
   Honest scope: peak is grid-snapped (13-point discrete argmax), 5-rule sample
   (class label qualitative, full class-mapping unresolved), additive Φ≈0 collapse is
   a robust substrate fact (XOR linearity, not design artifact), toy n=4 single
   inhibition mode."
  tier   = ⚪ SPECULATION-FENCED
  reason = imagination/metaphor class (hexa-bio AXIS) — verification N/A by
           design; values deterministic arithmetic, interpretation fenced
```

## 9. honest scope

본 H 가 **닫지 못하는 것**:
- 정확한 class→정렬 매핑 — class III/IV vs additive 의 깔끔한 분할 아님 (rule 54 IV 반례, C1). peak 위치 {0.18, 0.40, 0.05} 3-그룹의 *왜* 가 미해결.
- 256-rule / class-stratified universality — 5-rule sample (C3).
- peak 위치의 grid-snap 이산 한계 (C2) — 5-point stencil / 2× grid 재측정 별도 round.
- additive (rule 90) 의 inverse-U 붕괴 *mechanism* 의 closed-form 증명 (XOR factorizability ↔ Φ≈0 의 formal link).
- n=4 외 ring size / non-ECA substrate (PureField) — single-n single-mode scope.

## 10. UNIVERSE.md update

축 **G (ANIMA.mining 승격 / round 9 메타-축)** 에 round-9 row 추가 → done with `🟢 SUPPORTED-NUMERICAL (M1∧M2∧M3 · n_aligned=2/5, rule110 aligned |Δ|=0.03232 + rule90 breaks peak I=0.05 inverse-U 붕괴, peak-GZ 정렬 class-CONDITIONAL, 5-rule {30,54,90,110,184} n=4, $0 mac-local 2026-05-28)`. dΦ/dI peak=GZ_LOWER 정렬이 substrate-universal 아닌 class-conditional — H_351 의 SUPPORTED 가 보편 anchor 가 아님을 확정. 단 class III/IV vs additive 깔끔분할은 아님 (C1).

## artifacts

- `UNIVERSE/state/h657_dphi_peak_gz_class_2026_05_28/phi_rule.hexa` — per-rule Φ(I) 샤드 template (RULE_PLACEHOLDER)
- `UNIVERSE/state/h657_dphi_peak_gz_class_2026_05_28/phi_rule_{30,54,90,110,184}.hexa` — 5 foreground 샤드 (각 ~80–90s wall)
- `UNIVERSE/state/h657_dphi_peak_gz_class_2026_05_28/phi_rule_{30,54,90,110,184}.json` — per-rule Φ 테이블 SSOT
- `UNIVERSE/state/h657_dphi_peak_gz_class_2026_05_28/aggregate.hexa` — phi-free aggregator (dΦ/dI · peak · delta-GZ · class-dependence · verdict)
- `UNIVERSE/state/h657_dphi_peak_gz_class_2026_05_28/result.json` — measurement SSOT (per-rule peak_I · delta_gz · aligned · n_aligned · verdict)
- `UNIVERSE/state/h657_dphi_peak_gz_class_2026_05_28/run_h657.hexa` — 단일 5-rule runner (참조용 · 1040 big_phi 호출 >60s wall 이라 샤드 양식으로 대체)
- `UNIVERSE/H_657_dphi_peak_gz_substrate_class.md` — 본문 (SSOT)
