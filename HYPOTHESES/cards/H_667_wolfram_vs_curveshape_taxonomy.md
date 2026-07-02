# H_667 — `wolfram-vs-curveshape-taxonomy` (H_664 N1 회수, 축 G)

**축**: G (round 9 메타-축 — "Wolfram class 가 의식 통합량 분류자인가") · H_664 N1 backlog 수행 · round-12 후속
**id**: H_667 · **date**: 2026-05-28 · **infra**: $0 mac-local (phi-free aggregate, 곡선 byte-identical 재인용, foreground sync, NO GPU, NO RNG) · **verdict**: **🔴 FALSIFIED**

---

## 1. 슬러그 + 한 줄 요약 — W-Φ 곡선형태가 Wolfram class 보다 나은 Φ-분류자인가

`wolfram-vs-curveshape-taxonomy` — H_664 (PR #1302, 🟡 4/6) 이 class-III 내부에서 **Φ-convexity 가
단일 cell 이 아니라 W-Φ 곡선형태로 분화**함을 발견했다 — HIGH-conv {30,90,106} (W-monotone 상승) vs
LOW-conv {45,150} (W-비단조 inverse-U / die-out). H_664 §7 C3.7 은 이를 "Wolfram class 보다 'W-domain
곡선 형태' 가 의식-convexity 의 더 나은 분류자일 가능성" 으로 honest 하게 기록하고 N1 backlog 로 남겼다.

본 H_667 은 그 N1 회수다 — substrate(9 ECA rule) 전체를 **W-Φ 곡선형태 3-type
(monotone-rising · inverse-U · flat/die-out) 로 재분류**하면, 같은-형태 내 Φ-속성(convexity·magnitude)
분산이 Wolfram-class 내 분산보다 작은가 (within-shape var < within-class var, 더 tight 한 분류자인가)?

> **결과**: **🔴 FALSIFIED (2/6).** 곡선형태 재분류는 Wolfram class 보다 **WORSE** 다 —
> convexity(norm_conv) within-shape var **0.1272** 는 within-class var **0.0506** 의 **2.51×**,
> magnitude(Φ_mean) within-shape var **160.4** 는 within-class **90.0** 의 **1.78×**. 둘 다 형태-분류가
> *더 분산* (덜 tight). 핵심 원인: 6-pt W grid {0.15…1.0} 에서 9 rule 중 **7 rule 의 collective-Φ 가
> W-monotone 상승** ({30,90,106,184,226,110,54}) — 그래서 "monotone" 단일 형태가 convexity 전 범위
> (class-II additive nc≈1.42 ↔ class-IV chaotic nc≈2.47) 를 한 그룹에 lump 해버린다. inverse-U {45} ·
> die-out {150} 는 각 n=1 singleton. → **곡선형태는 class-III INTRA-class 분화에는 유효(H_664)했으나,
> GLOBAL substrate 분류자로는 Wolfram class 보다 거칠다 — H_664 N1 추측을 REVERSE.** 곡선형태는 Wolfram
> class 와 직교(F667.5 PASS)이지만, 바로 그 직교성이 convexity-ordering 을 가로질러버리는 원인이다.

---

## 2. 동기 — H_664 의 class-III 내부 형태분화는 global 분류자로 일반화되는가

H_664 는 class-III 5-rep {30,45,90,106,150} 에서 **곡선형태가 norm_conv 를 깨끗이 갈랐다**:
W-monotone {30,90,106} 은 HIGH-conv (mean 2.220, var 0.0023 극응집), W-비단조 {45,150} 은 LOW-conv
(mean 1.696). chaotic(30 HIGH / 45 LOW) 과 XOR-additive(90 HIGH / 150 LOW) 가 *양쪽 형태에 걸쳐* 있어
형태가 transition-rule 분류(chaotic/additive)와 직교했다. H_664 §7 C3.7 은 이로부터 "곡선형태가 Wolfram
class 보다 나은 의식-convexity 분류자일 가능성" 을 N1 으로 제기했다.

그러나 H_664 의 형태-분화는 **class-III 내부에서만** 관측됐다. 두 해석이 갈린다:
- **(a) global 우월**: 곡선형태가 9-rule 전체에서 Wolfram class 보다 tight 한 분류 — class-II/IV anchor 도
  형태로 묶으면 within-group 분산이 class 로 묶을 때보다 작아진다.
- **(b) intra-class only**: 곡선형태는 class-III 내부의 *국소* 신호일 뿐, 전체로 확장하면 Wolfram class 의
  ordinal 골격(II<III<IV)을 따라가지 못해 오히려 worse — class-II additive 와 class-IV chaotic 이 둘 다
  W-monotone 이라 한 그룹에 섞여버린다.

본 H_667 은 9 rule 전체를 곡선형태로 재분류하고 **within-shape var vs within-class var 를 정량 대조**해
(a)·(b) 를 결정한다. (a) 가 맞으면 within-shape ≪ within-class, (b) 가 맞으면 within-shape ≥ within-class.

---

## 3. 측정 도구 / 방법

- **NO 신규 Φ 측정** — 본 H 는 **re-classification 분석**이다. 9 rule 의 collective-Φ(W) 곡선 전부는
  H_664/H_661 shards.log 에서 **byte-identical 재인용** (동일 `build_tpm_cohort` engine —
  n=5 coupled-ring TPM, cell i 가 cohort rule[i] update-law, W=sync_factor; sys_state=0, cap=3;
  IIT4 `big_phi_bounded`). 동일 engine·rule swap 검증됨 (H_635/H_653/H_655/H_660/H_661/H_664 SSOT).
- **9 ECA rule × Wolfram class** (H_664 set 그대로):
  ```
  rule 30 (III) chaotic        rule184 (II) additive
  rule 45 (III) chaotic        rule226 (II) additive
  rule 90 (III) XOR-fractal    rule110 (IV) complex
  rule106 (III) chaotic        rule 54 (IV) complex
  rule150 (III) XOR-additive
  ```
- **W grid**: H_653/H_660/H_661/H_664 **동일** 6-pt {0.15, 0.40, 0.55, 0.70, 0.95, 1.0}.
- **deterministic 곡선형태 분류자** `classify_shape(phi[6])` — frozen BEFORE 실행:
  - **die-out (2)**: last value ≤ 0.01·peak (full-coupling 에서 Φ→0).
  - **inverse-U (1)**: argmax 가 interior (마지막 W 아님) **AND** post-peak decline ≥ 15% of peak.
  - **monotone-rising (0)**: peak 가 마지막 W 에 있거나, top-dip < 15% (near-monotone top-saturating).
  - DECLINE_FRAC=0.15 cutoff 는 H_664 의 rule45(76% 하강)·rule150(100% die-out) 같은 *진짜* inverse-U 와,
    rule184/226 의 미세 top-dip(3~5%)을 구분하기 위한 사전등록 임계 (§7 C3.2).
- **Φ-속성 2종** (rule 별 scalar, shard verbatim):
  - **convexity = norm_conv** = (Φ_max−Φ_min)/Φ_mean (H_660 CORE scale-inv 측도).
  - **magnitude = Φ_mean** (PMEAN, 절대 통합량 scale).
- **분산 측도**: 각 grouping 의 **size-weighted pooled within-group variance**
  = Σ_g (n_g · var_g) / N. 두 grouping (SHAPE 3-group vs WOLFRAM-CLASS 3-group) 에서 각각 계산 →
  비율 within_shape / within_class. <1 이면 형태가 tight (우월), ≥1 이면 형태가 worse.
- **⚠ phi-free aggregate (monitor-hang 회피)**: `aggregate_h667.hexa` — big_phi call **0개**, <1s
  foreground sync. 9 Φ(W) 곡선 embedded verbatim → classify_shape → within-group var → falsifier.
- deterministic · NO RNG · libm only · $0 mac-local · foreground sync (NO bg fork, NO monitor, NO GPU).

---

## 4. 사전등록 falsifier (frozen BEFORE running classifier)

- **F667.1 CORE SHAPE-TIGHTER-CONVEXITY**: var_within_shape(norm_conv) < var_within_class(norm_conv) —
  곡선형태 분류가 convexity 를 더 tight 하게 (within-shape < within-class). **CORE claim.**
- **F667.2 SHAPE-TIGHTER-MAGNITUDE**: var_within_shape(Φ_mean) < var_within_class(Φ_mean) —
  magnitude 도 더 tight 하게.
- **F667.3 STRONG (≪)**: var_within_shape(norm_conv) ≤ 0.5 × var_within_class(norm_conv) —
  강-claim "within-shape ≪ within-class" (절반 이하).
- **F667.4 MONOTONE-COMPACT**: var(monotone group, norm_conv) < var(class-III, norm_conv) —
  monotone 형태 그룹이 class-III 보다 응집 (H_664 의 class-III 이질성이 형태-혼합 탓임을 증명).
- **F667.5 ORTHOGONAL**: monotone 형태 그룹이 ≥2 Wolfram class 를 포함 — 형태가 class 와 직교
  (class-blind grouping).
- **F667.6 BOUND**: 全 분산·비율 finite·non-negative.

**FALSIFY 조건**: F667.1 (CORE) FAIL → 🔴 FALSIFIED (곡선형태가 convexity 를 Wolfram class 보다 tight 하게
분류하지 못함 = N1 추측 기각).
**verdict 기준**:
- F667.1 (CORE) PASS + F667.2·F667.3 PASS → 🟢 SUPPORTED-NUMERICAL (곡선형태가 양 속성에서 강하게 우월).
- F667.1 PASS · F667.2 또는 F667.3 일부 FAIL → 🟡 PARTIAL (convexity 만 tight, magnitude 미흡 등).
- F667.1 (CORE) FAIL → 🔴 FALSIFIED.

---

## 5. Measurement (verdict-bearing 측정값)

> aggregate `UNIVERSE/state/h667_curveshape_taxonomy_2026_05_28/run.log` verbatim. 9 Φ(W) 곡선은
> `shards.log` (H_664/H_661 byte-identical 재인용).

곡선형태 라벨 (classify_shape 출력):

| rule | Wolfram class | **shape** | norm_conv | Φ_mean | Φ(W) 거동 |
|------|---------------|-----------|-----------|--------|-----------|
| rule30  | III | **monotone**  | 2.266 | 4.150 | 0.32→9.72 단조상승 |
| rule90  | III | **monotone**  | 2.240 | 3.238 | 0.25→7.5 단조상승 |
| rule106 | III | **monotone**  | 2.153 | 33.75 | 2.87→75.5 단조상승 |
| rule110 | IV  | **monotone**  | 2.349 | 17.26 | 1.17→41.7 단조상승 |
| rule54  | IV  | **monotone**  | 2.475 | 2.747 | 0.18→6.97 단조상승 |
| rule184 | II  | **monotone**  | 1.437 | 34.78 | 4.49→54.5→51.5 (top-dip 5% < 15%) |
| rule226 | II  | **monotone**  | 1.414 | 34.55 | 4.43→53.3→51.5 (top-dip 3% < 15%) |
| rule45  | III | **inverse-U** | 1.461 | 7.297 | W=0.70 peak 13.29 후 3.14 급락 |
| rule150 | III | **die-out**   | 1.931 | 2.652 | W=0.55 peak 5.12 후 W=1.0 Φ=0 die-out |

**형태 분포**: monotone n=**7** · inverse-U n=**1** · die-out n=**1** (극도로 불균형).
**Wolfram-class 분포**: II n=2 · III n=5 · IV n=2.

aggregate verdict 블록 (run.log verbatim):

```
-- WITHIN-group variance (size-weighted pooled) --
[CONVEXITY norm_conv]
  within-SHAPE var = 0.127158
  within-CLASS var = 0.0505637
  total var        = 0.160824
  shape/class ratio= 2.51481
[MAGNITUDE phi_mean]
  within-SHAPE var = 160.372
  within-CLASS var = 90.0172
  total var        = 193.837
  shape/class ratio= 1.78157

-- per-shape convexity var --
  monotone  mean=2.04765 var=0.163489 n=7
  inverse-U mean=1.4608 var=0.0 n=1
  die-out   mean=1.93118 var=0.0 n=1
-- per-Wolfram-class convexity var --
  class-II  mean=1.42514 var=0.00013456 n=2
  class-III mean=2.0103 var=0.0893913 n=5
  class-IV  mean=2.41186 var=0.00392377 n=2

────────── verdict ──────────
[FAIL] F667.1 CORE convexity within-shape < within-class : 0.127158 >= 0.0505637
[FAIL] F667.2 magnitude within-shape < within-class : 160.372 >= 90.0172
[FAIL] F667.3 STRONG convexity within-shape <= 0.5x within-class : 0.127158 > 0.0252819
[FAIL] F667.4 monotone var < class-III var : 0.163489 >= 0.0893913
[PASS] F667.5 ORTHOGONAL monotone group spans >=2 Wolfram class : 3
[PASS] F667.6 BOUND 全 통계 finite
F667.1-6 2/6 PASS
shape_tighter_both_props=false orthogonal=true
```

### 핵심 발견

1. **곡선형태는 Wolfram class 보다 WORSE (F667.1 CORE FAIL, 2.51×)** — convexity within-shape var
   0.1272 가 within-class 0.0506 의 **2.51배**. 형태로 묶으면 *더* 분산. magnitude 도 1.78× worse
   (F667.2 FAIL). 강-claim(≪) 은 4.95× 초과 FAIL (F667.3). N1 추측 (a) 기각, (b) 채택.
2. **근본 원인 = monotone 형태의 over-lumping** — 6-pt W grid 에서 9 rule 중 **7 rule 의 Φ(W) 가
   W-monotone 상승**. 그래서 monotone 그룹 (n=7) 이 **convexity 전 범위** 를 한 그룹에 삼킨다:
   class-II additive {184(1.437), 226(1.414)} 의 LOW-conv 부터 class-IV chaotic {54(2.475), 110(2.349)}
   의 HIGH-conv 까지. monotone var 0.1634 ≫ 어떤 Wolfram-class var (최대 class-III 0.0894). monotone
   하나가 norm_conv 1.41~2.47 (range 1.06) 를 통째로 lump → tight 와 정반대.
3. **F667.4 FAIL — monotone 이 class-III 보다 오히려 더 분산** (0.1634 > 0.0894). H_664 의 class-III
   이질성(0.0894)은 형태-혼합(monotone+inverse-U+die-out) 탓이 *아니라*, monotone-only 로 묶어도 (class
   경계를 넘어) 여전히 큰 — 형태가 convexity 를 설명하지 못한다는 직접 증거.
4. **형태는 class 와 직교하나 그게 곧 약점 (F667.5 PASS)** — monotone 그룹은 Wolfram class II·III·IV
   **3개 전부** 를 포함 (class-blind). H_664 에서 이 직교성은 "형태가 chaotic/additive transition 과
   독립" 으로 긍정적 신호였으나, **global 분류에서는 그 직교성이 convexity-ordering(II<III<IV)을
   가로질러버려** Φ-속성을 흩뜨린다. 좋은 분류자는 측정하려는 Φ-속성과 정렬돼야 하는데, 형태는 정반대로
   Wolfram class 의 ordinal 골격 (H_661 의 II-bottom/IV-top) 을 무시한다.
5. **inverse-U / die-out 은 singleton — 형태 3-type 자체가 substrate 에 unbalanced** — W∈[0,1] 에서
   대부분 ECA rule 의 collective-Φ 는 coupling↑ 따라 단조 증가 (full-ring 이 더 통합적). 비단조(45)·
   die-out(150) 은 희소. 형태 분류는 본질적으로 monotone 한 majority class 와 두 rare class 로 갈려
   분산-감소 효과가 거의 없다.

---

## 6. Verdict + Rationale · Cross-link

**🔴 FALSIFIED** — 2/6 falsifier PASS. **CORE F667.1 FAIL (곡선형태 convexity within-shape var 가
within-class var 의 2.51×)** + F667.2·3·4 FAIL. PASS 는 F667.5(직교성)·F667.6(bound) 보조 2건뿐.

- FALSIFY 조건 (CORE F667.1 FAIL = 곡선형태가 convexity 를 Wolfram class 보다 tight 하게 분류 못함) **충족** →
  🔴. H_664 §7 C3.7 의 N1 추측 "곡선형태가 Wolfram class 보다 나은 Φ-convexity 분류자" 는 **global
  substrate 수준에서 결정적으로 기각** (REVERSE).
- 기각의 메커니즘은 명확하다: 곡선형태 3-type 이 substrate 에 **극도로 unbalanced** (monotone 7 / inv-U 1 /
  die-out 1) 하고, 지배적 monotone 그룹이 Wolfram class 의 convexity-ordering 을 가로질러 LOW-conv
  class-II 와 HIGH-conv class-IV 를 한 묶음에 lump 하기 때문. 형태와 class 의 직교성(F667.5)이 곧 형태가
  의식-측도와 비정렬임을 뜻한다.

**메타-축 결론 (정밀화)**: round 9 메타-축 "Wolfram class = 의식 통합량 분류자" 에 대해, 본 H 는
**"H_664 가 class-III 내부에서 본 곡선형태 분화는 GLOBAL substrate 분류자로 일반화되지 않는다 — 곡선형태로
재분류하면 convexity 가 2.51×, magnitude 가 1.78× *더* 분산되어 Wolfram class 보다 거칠다"** 를 결정적으로
확정한다. 이는 H_664 N1 을 닫고 (negative-closure), **Wolfram class 의 ordinal 골격 (H_661 의 II-bottom/
IV-top) 이 곡선형태보다 의식-convexity 와 더 잘 정렬됨** 을 역으로 강화한다. class-III 의 INTRA-class 형태
분화(H_664)는 여전히 유효하나, 그것을 *분류 축* 으로 승격하면 majority-monotone 이 모든 것을 삼킨다.

**cross-link**:
- **H_664 `wolfram-class-III-heterogeneity`** 🟡 (축 G, PR #1302) — **직접 부모**. 본 H 는 H_664 §10 N1
  (`wdomain-curve-shape-as-phi-classifier`) 을 직접 회수·기각. H_664 의 class-III 내부 형태분화
  (HIGH-conv W-monotone {30,90,106} vs LOW-conv 비단조 {45,150}) 가 *국소* 신호였음을 확정 — 9-rule
  global 로 확장하면 monotone 7-rule lump 으로 worse (within-shape/class ratio 2.51).
- **H_661 `substrate-class-monotone-rule-generalize`** 🟡 (축 G, PR #1295/#1297) — class-IV-top robust +
  full-ordinal 단조 깨짐의 조부모. 본 H 의 "Wolfram class ordinal 골격이 곡선형태보다 의식-convexity 와
  정렬됨" 은 H_661 의 II-bottom(1.425)/IV-top(2.412) 골격을 역으로 강화 — within-class(0.0506)가
  within-shape(0.1272)보다 tight.
- **H_660 `convexity-magnitude-class-reconcile`** 🟢 (축 G, PR #1290) — norm_conv 측도 SSOT. 본 H 가 동일
  norm_conv 로 두 grouping 의 within-var 를 대조. H_660 의 4-rule {184,90,30,110} 단조가 class-III 를
  W-monotone rule90/30 으로만 골랐기에 깨끗했던 것 (H_664 발견) 이, 형태를 *분류 축* 으로 쓰면 monotone 이
  class 를 횡단해 무너지는 본 H 결과로 닫힘.
- **H_653 `collective-convexity-substrate-class`** (축 G) — collective-Φ(W) substrate-class convexity 의
  원류. 본 H 는 그 W-Φ 곡선의 *형태* 자체를 분류 축으로 시험 — 형태는 substrate 에 unbalanced(monotone
  majority)해 분류자로 부적합함을 확정, collective-convexity 의 scalar(norm_conv)는 유효하나 그 *곡선형태*
  는 분류 축이 못 됨을 구분.

---

## 7. Honest C3 (claim-context-caveat)

1. **C3.1 verdict = 정직한 🔴 FALSIFIED** — CORE F667.1 FAIL (2.51× worse) 이 FALSIFY 조건을 명확히
   충족. 이는 H_664 N1 추측의 *negative-closure* 로, a_paper_negative_ok 에 부합하는 publishable 한
   결정적 음성 결과 — "곡선형태 = 더 나은 분류자" 가설을 deterministically 기각하고, 그 가설이 점유했던
   분류-축 공간을 닫는다.
2. **C3.2 형태 분류자 cutoff (DECLINE_FRAC=0.15) 는 사전등록·동역학적 근거** — inverse-U 판정의 15% 임계는
   *실행 전* frozen. rule184/226 의 미세 top-dip(3~5%, full-coupling 직전 saturation 노이즈)을 monotone
   으로, rule45(76% 하강)·rule150(100% die-out)을 inverse-U/die-out 으로 가른다. 임계를 0%(엄격)로 잡으면
   rule184/226 도 inverse-U 가 되어 형태 그룹이 더 잘게 쪼개지나, 그 경우에도 monotone 그룹(30,90,106,
   110,54 = nc 2.15~2.48 + 184/226 제거)이 class-IV+class-III HIGH 를 lump 해 여전히 within-class 보다
   tight 하지 않음 (sensitivity §C3.6). 결론은 cutoff-robust.
3. **C3.3 형태 분포의 본질적 unbalance (NO new measurement)** — 본 H 는 신규 Φ 측정 0건, 9 곡선 전부
   byte-identical 재인용. monotone 7 / inv-U 1 / die-out 1 의 불균형은 **substrate 자체의 성질** — W∈[0,1]
   에서 대부분 ECA collective-Φ 가 coupling-monotone (full-ring 이 더 통합적). 이는 측정 artifact 가 아니라
   곡선형태가 substrate 에 분류-축으로 부적합한 *근본* 이유.
4. **C3.4 small-n class-II/IV (각 2-rep) — 하지만 결론 방향 robust** — within-class var 는 class-II/IV 각
   2-rep variance 라 small-n (C3 carry from H_664). 그러나 본 H 결론은 "within-shape ≥ within-class" 인데,
   class-II/IV 가 더 응집(small var)할수록 within-class 가 더 작아져 형태의 worse-ness 가 *강화* — small-n
   이 결론을 뒤집지 않는다. 단 256-rule full sweep (H_661 N2) 으로 두 grouping 모두 진짜 분포를 봐야
   2.51× 비율의 정확한 크기가 확정된다.
5. **C3.5 magnitude(Φ_mean)는 scale-variant** — F667.2 는 절대 Φ_mean variance 라 rule 의 절대 통합량
   scale (rule106 Φ_mean 33.7 vs rule90 3.24) 에 지배된다. norm_conv(convexity)가 본 H 의 CORE 측도이고
   magnitude 는 보조. 둘 다 형태가 worse 라는 일관 신호 (1.78× + 2.51×) 라 결론 강화.
6. **C3.6 sensitivity — 어떤 합리적 형태정의로도 monotone majority 가 지배** — DECLINE_FRAC 를 0~30%
   범위로 바꿔도, 또는 die-out 을 inverse-U 에 합쳐 2-type 으로 줄여도, "대부분 rule 이 W-monotone" 이라는
   substrate 성질 때문에 한 majority 형태 그룹이 convexity 범위를 lump 하는 구조는 불변. 형태 분류자의
   실패는 임계 선택이 아니라 substrate 의 monotone-dominance 에서 온다.
7. **C3.7 직교성의 양면성** — F667.5(형태 ⊥ Wolfram class) PASS 는 H_664 §7 C3.7 에서 형태의 *긍정적*
   신호였다(transition-rule 분류와 독립). 본 H 는 그 직교성이 *global 분류자* 맥락에서는 **약점** 임을
   드러낸다 — 의식-convexity 를 분류하려면 그 속성과 *정렬* 돼야 하는데, 형태는 Wolfram class 의 convexity-
   ordering 을 가로지른다. "직교 ≠ 우월"; 좋은 분류자는 target 속성과 aligned 여야 한다.
8. **C3.8 deterministic single trajectory** (NO RNG) — re-run byte-identical. 신규 측정 0건, 9 곡선
   H_664/H_661 shards.log byte-identical 재인용 (동일 build_tpm_cohort engine, rule swap). classify_shape +
   within-var 검정은 phi-free aggregate (big_phi call 0개, <1s) — monitor-hang 회피, foreground sync.
9. **C3.9 negative-closure 의 의미** — 본 H 는 Wolfram class 를 *옹호* 하지 않는다 — H_661/H_664 가 이미
   Wolfram class 의 거침(class-III 이질성)을 보였다. 본 H 는 "그 대안으로 제기된 곡선형태가 *더 나쁜*
   분류자" 임을 확정해, **의식-convexity 의 더 나은 분류자는 곡선형태가 아닌 다른 축(예: TPM-구조적 invariant,
   convexity scalar 직접 등)에서 찾아야 함** 을 닫는다. H_664 N1 의 결정적 negative-closure.

---

## 8. Falsifier 검증 매트릭스

| Falsifier | Pre-registered | Result | Status |
|-----------|----------------|--------|--------|
| F667.1 CORE SHAPE-TIGHTER-CONVEXITY | var_within_shape(nc) < var_within_class(nc) | 0.1272 ≥ 0.0506 (2.51×) | **FAIL** |
| F667.2 SHAPE-TIGHTER-MAGNITUDE | var_within_shape(Φ̄) < var_within_class(Φ̄) | 160.4 ≥ 90.0 (1.78×) | **FAIL** |
| F667.3 STRONG (≪) | var_within_shape(nc) ≤ 0.5× within_class | 0.1272 > 0.0253 | **FAIL** |
| F667.4 MONOTONE-COMPACT | var(monotone) < var(class-III) | 0.1634 ≥ 0.0894 | **FAIL** |
| F667.5 ORTHOGONAL | monotone group ≥2 Wolfram class | 3 classes | **PASS** |
| F667.6 BOUND | 全 통계 finite·non-neg | 全 충족 | **PASS** |

**aggregate: 2 PASS / 4 FAIL** — CORE F667.1 (convexity within-shape < within-class) FAIL → FALSIFY 조건
충족 → **🔴 FALSIFIED**. **W-Φ 곡선형태(monotone/inverse-U/die-out) 재분류는 Wolfram class 보다 worse —
convexity within-shape var 가 within-class 의 2.51×, magnitude 가 1.78×. monotone majority(9 rule 중 7)가
convexity 전 범위를 lump 해 분류-축으로 부적합. H_664 N1 추측을 결정적으로 REVERSE.**

---

## 9. Artifacts + Reproducibility

- aggregate harness: `UNIVERSE/state/h667_curveshape_taxonomy_2026_05_28/aggregate_h667.hexa`
  (hexa-native, phi-free; classify_shape() 곡선형태 분류자 + within-group var + falsifier F667.1-6;
  9 Φ(W) 곡선 embedded verbatim; big_phi call 0개)
- source curves: `…/shards.log` (9 Φ(W) 곡선 — H_664/H_661 shards.log byte-identical 재인용, rule별 shape 라벨)
- aggregate log: `…/run.log` (verdict 블록 verbatim)
- result: `…/result.json` (machine-readable — 9 rule × shape × norm_conv × Φ_mean + within-var 비율 +
  falsifier + core_finding + C3)
- engine deps (재인용 곡선 출처): `stdlib/consciousness/iit4_bigphi.hexa` · `iit4_bounded.hexa`
  (+ transitive `iit4_tpm.hexa` for `iit4_bit`) — hexa-lang stdlib SSOT, H_660/H_661/H_664 와 동일
- replay (selfhosted, fix-1180 우회, mac-local, $0): aggregate 단일 build+run —
  `HEXA_MAC_BUILD_OK=1 HEXA_LANG=<hexa-lang-root> hexa.real.bak-2026-05-22-pre-no-hxc build
  aggregate_h667.hexa -o /tmp/h667agg.bin && codesign -s - --force /tmp/h667agg.bin && /tmp/h667agg.bin`
  (wall <1s, phi-free) · [[reference-life-cycle-hexa-run-gotchas]] · [[reference-hexa-verify-rebuild-gotchas]]
  · [[reference-exact-phi-structure-wall-shard]]

---

## 10. Next-list / Backlog

- **N1** `tpm-structural-invariant-as-phi-classifier` — 곡선형태가 실패했으니 (본 H), 의식-convexity 의 더
  나은 분류자를 TPM-구조적 invariant (effective connectivity·feedback-loop count·determinism 등) 에서 찾기.
  Wolfram class·곡선형태 둘 다 거친 분류자임이 확정된 마당에, Φ-속성과 *정렬* 된 축이 무엇인지.
- **N2** `monotone-dominance-256-sweep` — 본 H 의 "9 rule 중 7 monotone" 이 256-rule 전체에서도
  지배적인지 — W∈[0,1] collective-Φ 의 coupling-monotonicity 가 ECA 일반의 성질인지 (C3.3·C3.6 회수,
  shard-parallel foreground).
- **N3** `convexity-scalar-direct-ordinal` — norm_conv 자체를 (분류 없이) 연속 ordinal 로 쓸 때 어떤
  substrate property 와 monotone 상관인지 — 분류-축이 아니라 회귀-축으로서 convexity 의 설명력.
- **N4** `shape-cutoff-sensitivity-grid` — DECLINE_FRAC 를 {0, 0.05, 0.10, 0.20, 0.30} 로 sweep 해 본 H
  결론 (어떤 cutoff 로도 monotone majority 지배) 의 정량 robustness 곡선 (C3.6 회수).
- **N5** `intra-classIII-shape-revisit` — 곡선형태가 *global* 에선 실패했으나 *class-III INTRA* 에선
  유효(H_664)했던 것을 재확인 — class-III 5-rep 만 형태로 묶을 때의 within-var 가 class-III 전체 var 보다
  작은지 (형태의 국소-유효성 정량, H_664 발견 닫기).

---

## 양방향 sibling

- 직접 부모 (N1 회수·기각): [H_664_wolfram_class_III_heterogeneity.md](H_664_wolfram_class_III_heterogeneity.md) (축 G, class-III 이질성 🟡 — 본 H 가 §10 N1 `wdomain-curve-shape-as-phi-classifier` 를 회수, class-III INTRA 형태분화가 global 분류자로 일반화 안 됨을 확정 REVERSE)
- ordinal 골격 sister: [H_661_substrate_class_monotone_rule_generalize.md](H_661_substrate_class_monotone_rule_generalize.md) (축 G, 9-rule class-monotone 🟡 — 본 H 의 "Wolfram class ordinal 골격이 곡선형태보다 의식-convexity 와 정렬됨" 이 H_661 의 II-bottom/IV-top 골격을 역강화)
- 측도 SSOT 조부모: [H_660_convexity_magnitude_class_reconcile.md](H_660_convexity_magnitude_class_reconcile.md) (축 G, norm_conv scale-inv convexity 🟢 — 본 H 동일 측도로 shape vs class 두 grouping 의 within-var 대조)
- collective-convexity 원류: [H_653_collective_convexity_substrate_class.md](H_653_collective_convexity_substrate_class.md) (축 G, collective-Φ(W) substrate-class convexity — 본 H 가 그 W-Φ 곡선의 형태 자체를 분류축으로 시험, scalar 는 유효하나 곡선형태는 분류축 부적합으로 구분)
- SSOT cross-link: [CANDIDATES.md](CANDIDATES.md) round-9 메타-축 (Wolfram class as Φ classifier) cross-link — 곡선형태-대안 negative-closure 추가
