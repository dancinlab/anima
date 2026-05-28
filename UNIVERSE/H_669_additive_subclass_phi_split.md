# H_669 — `additive-subclass-phi-split` (round-9 메타-축 정밀, 축 G)

**축**: G (round 9 메타-축 — "Wolfram class 가 의식 통합량 분류자인가") · round-12 후속 · H_664 발견(sub-type ⊥ additive/chaotic) 직접 검정
**id**: H_669 · **date**: 2026-05-28 · **infra**: $0 mac-local (per-rule shard + phi-free aggregate, foreground sync) · **verdict**: **🔴 FALSIFIED (CLOSED-NEGATIVE)**

---

## 1. 슬러그 + 한 줄 요약 — round-9 메타-축 정밀: additive 가 별도 Φ-class 인가

`additive-subclass-phi-split` — round 9-12 에서 additive rule (90 XOR · 150 · 60, GF(2) XOR-linear) 이
Φ-속성에서 반복적으로 특이했다 — H_642/H_652 에서 rule90 big-Φ≈0 (XOR linear, Φ-flat), H_664 에서 rule150
W=1.0 die-out (LOW-conv sub-type). additive 가 Wolfram class-III 로 분류되나 Φ-구조상 별도 거동을 보여 왔다.
본 H_669 은 round-9 메타-축의 정밀화로서, **additive substrate (XOR-linear rule90/150/60) 가 chaotic
class-III (30·45·106) 와 구별되는 별도 Φ-class 인가**를 정량한다.

신규 대표 **rule60 (additive XOR, next-state = L⊕C)** 1종을 측정해 additive 3-rep {90, 150, 60} 를 완성하고,
chaotic 3-rep {30, 45, 106} 와 **norm_conv (scale-inv convexity) 분포의 분리도** (분산비 between/within +
cluster separation + 분포 overlap) 를 측정한다.

> **결과**: additive 와 chaotic 의 Φ-속성 분포가 **강하게 겹친다** (분리 불가) — between/within 분산비
> **0.106** (≪ 1.0, 그룹-내 분산이 그룹-간 분산의 9배), group-mean gap **0.177** < max intra-group std
> **0.356** (cluster 분리 안 됨), norm_conv 구간 **overlap_len 0.309** (additive [1.931, 2.240] ∩ chaotic
> [1.461, 2.266], overlap_frac 0.384 = union 의 38%). 더욱이 가설이 예측한 "additive = floor (class-I 유사,
> chaotic 보다 낮음)" 은 **정반대** — mean_ADD **2.137** ≥ mean_CHA **1.960** (additive 가 오히려 약간
> 높음). → **F669.1~5 전부 FAIL, F669.6 BOUND 만 PASS → 1/6, 🔴 FALSIFIED**. **additive 는 별도 Φ-class
> 가 아니다 — class-III 내 variance 일 뿐이며, additive 라벨은 Φ-속성과 직교한다.** 실제 splitter 는
> Φ(W) *곡선 형태* (W-monotone vs W-비단조) 이고, 이는 additive·chaotic 두 그룹을 *모두* 가로지른다.

---

## 2. 동기 — additive 의 반복적 특이성은 별도 class 신호인가, 우연한 분산인가

round 9-12 의 substrate-class × Φ-속성 매트릭스에서 additive rule 은 거듭 특이했다:
- **H_642** (`shape-invariance-vs-scalar-convention-meta`, 🔴): rule90 의 faithful big-Φ ≈ 0.0 — XOR-linear
  factorizable substrate 가 통합량을 거의 만들지 못함 (additive-floor).
- **H_652** (envelope self-similarity-class): rule90 envelope 거동이 chaotic 과 다른 self-similarity.
- **H_664** (`wolfram-class-III-heterogeneity`, 🟡): rule150 (XOR-additive) 이 W=1.0 full-coupling 에서
  Φ=0 die-out — rule90 (W=1.0 Φ=7.5, W-monotone) 과 정반대 거동. class-III 가 HIGH-conv {30,90,106} vs
  LOW-conv {45,150} 2 sub-type 으로 분리되며, **rule150 (additive) 이 rule45 (chaotic) 와 같은 LOW-conv
  sub-type 에 합류**.

이 누적된 특이성에 두 해석이 갈린다:
- **(가설) additive = 별도 sub-class**: additive {90,150,60} 가 한 cluster (floor 근처, class-I 유사) 로
  뭉치고 chaotic {30,45,106} 와 분리. → Wolfram class-III 가 additive ⊎ chaotic 으로 *분할 필요*.
- **(귀무) additive ⊥ Φ-속성**: additive 는 transition-rule 분류일 뿐 Φ-구조 분류가 아니다. additive 내부도
  분산 (rule90 W-monotone vs rule150 die-out, H_664 발견) 하고, additive 와 chaotic 분포가 겹친다. additive
  의 반복적 특이성은 class-III 전체의 큰 분산 (H_664 의 44× within-class-III) 의 일부일 뿐.

H_664 는 이미 강한 *간접* 증거를 남겼다 — §7 C3.7 에서 "sub-type 가 chaotic/additive 의 transition-rule
분류와 *직교*" 라 honest 하게 기록했다 (chaotic 은 30 HIGH / 45 LOW 양쪽, XOR 은 90 HIGH / 150 LOW 양쪽).
본 H_669 은 이 직교성을 **직접·정량 falsifier 로** 검정한다 — additive group {90,150,60} 를 독립 분포로 묶고
chaotic group {30,45,106} 와의 분리도를 사전등록 임계로 판정. neutral rule60 추가가 additive group 의 분포를
완성한다 (rule60 이 floor 면 가설 강화, monotone 이면 귀무 강화).

---

## 3. 측정 도구 / 방법

- **engine** (H_635/H_653/H_655/H_660/H_661/H_664 SSOT verbatim 재사용, cohort rule 만 swap):
  n=5 coupled-ring TPM `build_tpm_cohort(rule, W)` — 5 cell, cell i 가 cohort rule[i] 의 update-law.
  decoupled(W=0)=self-loop only (idx=7·c), coupled(W=1)=full ring, blend(0<W<1)=fractional.
  collective-Φ(W) = `big_phi_bounded(build_tpm_cohort([rule×5], W), 5, sys=0, cap=3)[0]` —
  각 (rule,W) point 에서 **실제 IIT4 substrate 측정** (lookup 아님).
- **6 ECA rule × 2 group**:
  ```
  ── ADDITIVE group (XOR-linear, GF(2)) ──
  rule 60 (additive)  next = L⊕C      [NEW this H — neutral 추가로 additive 분포 완성]
  rule 90 (additive)  next = L⊕R      [H_664 NEW / H_661 anchor, byte-identical]
  rule150 (additive)  next = L⊕C⊕R    [H_664 NEW, byte-identical]
  ── CHAOTIC group (non-additive class-III) ──
  rule 30 (chaotic)   non-additive    [H_661/H_664 anchor, byte-identical]
  rule 45 (chaotic)   non-additive    [H_661/H_664 anchor, byte-identical]
  rule106 (chaotic)   non-additive    [H_664 NEW, byte-identical]
  ```
  (rule60/90/150 가 GF(2) XOR-linear = additive 의 정의 — 이웃의 mod-2 합. rule30/45/106 은 non-linear.)
- **W grid**: H_653/H_660/H_661/H_664 와 **동일** 6-pt {0.15, 0.40, 0.55, 0.70, 0.95, 1.0}.
- **metric**: **norm_conv** = (Φ_max − Φ_min) / Φ_mean — scale-invariant convexity (H_660 CORE 측도).
  보조로 **log_span** = ln(Φ_max/(Φ_min+floor)) (rule150 die-out 에서 ill-defined → finite rule 만).
- **분리 측도** (additive group vs chaotic group, norm_conv 위):
  - **var_between** = variance of 2 group-means {mean_ADD, mean_CHA}.
  - **var_within_pooled** = (var_ADD + var_CHA)/2 (그룹 내부 분산 평균).
  - **ratio_between/within** = F-test 류 분리 비율 (≥1 이면 그룹-간 ≥ 그룹-내 = 분리).
  - **grp_gap** = |mean_ADD − mean_CHA| vs **intra_std** = √(max group var) — cluster 분리 판정.
  - **overlap_len/frac** = 두 그룹 [min,max] norm_conv 구간의 겹치는 길이/비율 (>0 이면 분포 겹침).
  - **additive_is_floor** = (mean_ADD < mean_CHA) — 가설의 "additive = class-I 유사 floor" 직접 검정.
- **⚠ per-rule shard (monitor-hang 회피)**: rule60 단독 6 W-call ≈ 21s foreground sync 측정
  (`shard_h669.hexa`, RULE_ID=60) → `shards.log` 기록. 나머지 5 rule (90/150/30/45/106) 은 H_664/H_661
  shards.log 에서 **byte-identical** 재인용 (동일 engine, rule swap 검증됨). **phi-free aggregate**
  (`aggregate_h669.hexa`, big_phi call 0개, <1s) 가 분리도·falsifier 검정.
- deterministic · NO RNG · libm `ln`/`pow` only · $0 mac-local · foreground sync (NO bg fork, NO monitor, NO GPU).

---

## 4. 사전등록 falsifier (frozen BEFORE measuring rule60)

가설은 "additive 가 chaotic 과 분리된 별도 sub-class (floor 근처)" → 분리 신호 = PASS.

- **F669.1 CORE SEPARATION**: var_between(2 grp-means) ≥ var_within_pooled (ratio ≥ 1.0) — 그룹-간 분산이
  그룹-내 분산에 필적/초과 (additive↔chaotic 분리의 강-claim).
- **F669.2 GAP-EXCEEDS-SPREAD**: grp_gap (|mean_ADD − mean_CHA|) > intra_std (max group √var) — cluster
  중심 거리가 cluster 내부 흩어짐보다 큼 (분리 가능).
- **F669.3 NO-OVERLAP**: overlap_len ≤ 0 — 두 그룹 norm_conv 구간이 겹치지 않음 (분포 완전 분리).
- **F669.4 ADDITIVE-FLOOR**: mean_ADD < mean_CHA — additive 가 chaotic 보다 LOWER (가설의 class-I 유사
  floor 특성 직접 검정).
- **F669.5 DISTINCT-FRAC**: overlap_frac < 0.3 — 겹침이 union 의 30% 미만 (대체로 분리).
- **F669.6 BOUND**: 全 분산·비율 finite·non-negative.

**FALSIFY 조건** (가설 §1 거부): additive 와 chaotic 분포가 **겹침** (F669.3 FAIL = overlap>0) **AND** 분리
임계 미달 (F669.1·F669.2 FAIL) → 🔴 FALSIFIED (additive 별도 class 아님, class-III 내 variance 일 뿐).
**verdict 기준**:
- F669.1 (CORE) PASS + F669.2·F669.3 PASS → 🟢 SUPPORTED-NUMERICAL (additive 별도 sub-class 확정).
- 분리 신호 일부만 (F669.2 PASS · F669.1 FAIL 등) → 🟡 PARTIAL.
- F669.1·F669.2·F669.3 모두 FAIL (분리 임계 전부 미달 + 분포 겹침) → 🔴 FALSIFIED.

---

## 5. Measurement (verdict-bearing 측정값)

> shard 출력 `UNIVERSE/state/h669_additive_subclass_phi_split_2026_05_28/shards.log` (rule60 NEW +
> H_664/H_661 anchor) + aggregate `run.log` verbatim.

신규 측정 rule60 Φ(W) grid (6-pt {0.15, 0.40, 0.55, 0.70, 0.95, 1.0}):

```
rule60 (additive XOR) Φ(W): 0.19718 0.754519 1.32399 2.20647 5.05911 6.0   (W-monotone 상승, Φmin=0.197 Φmax=6.0)
                            norm_conv=2.24029  log_span=3.41489  abs_Δ=5.803
```

→ rule60 (additive) 의 norm_conv = **2.24029 — rule90 (2.24029) 와 완전 동일** (둘 다 2-input XOR
W-monotone). additive rule60 은 floor 가 아니라 **HIGH-conv W-monotone** (가설 예측의 정반대).

6-rule norm_conv (2 group):

| group | rule | next-state | **norm_conv** | Φ(W) 곡선 형태 | 비고 |
|-------|------|-----------|---------------|---------------|------|
| **ADDITIVE** | rule60  | L⊕C   | **2.240** | W-monotone 상승 | **NEW · HIGH-conv** |
| **ADDITIVE** | rule90  | L⊕R   | 2.240 | W-monotone 상승 | H_664/H_661 |
| **ADDITIVE** | rule150 | L⊕C⊕R | 1.931 | W-비단조 die-out (Φ=0 @W=1.0) | H_664 LOW-conv |
| **CHAOTIC**  | rule30  | —     | 2.266 | W-monotone 상승 | H_661/H_664 HIGH |
| **CHAOTIC**  | rule45  | —     | 1.461 | W-비단조 inverse-U | H_661/H_664 LOW |
| **CHAOTIC**  | rule106 | —     | 2.153 | W-monotone 상승 | H_664 HIGH |

aggregate verdict 블록 (run.log verbatim):

```
=== H_669 additive-subclass-phi-split aggregate (phi-free) ===
ADDITIVE(3): rule90=2.24029 rule150=1.93118 rule60=2.24029   mean_ADD=2.13725 var=0.0212331
CHAOTIC (3): rule30=2.26615 rule45=1.4608 rule106=2.1531     mean_CHA=1.96002 var=0.126739

var_within_pooled    = 0.0739859
var_between(2 grp-m) = 0.00785321
RATIO between/within = 0.106145
grp_gap |ADD-CHA|    = 0.177237
intra_std (max grp)  = 0.356004

-- distribution overlap (norm_conv ranges) --
ADD range [1.93118, 2.24029]
CHA range [1.4608, 2.26615]
overlap_len  = 0.30911  (>0 ⇒ 분포 겹침)
overlap_frac = 0.383821
additive_is_floor (mean_ADD < mean_CHA) = false

────────── verdict ──────────
[FAIL] F669.1 CORE between/within var >= 1.0 : 0.106145 < 1.0
[FAIL] F669.2 grp-gap > intra-std : 0.177237 <= 0.356004
[FAIL] F669.3 NO-OVERLAP norm_conv 구간 분리 : overlap_len=0.30911 > 0 (겹침)
[FAIL] F669.4 ADDITIVE-FLOOR mean_ADD < mean_CHA : 2.13725 >= 1.96002
[FAIL] F669.5 DISTINCT overlap_frac < 0.3 : 0.383821
[PASS] F669.6 BOUND 全 통계 finite
F669.1-6 1/6 PASS
additive_separated_class=false additive_floor_subclass=false
```

### 핵심 발견

1. **분포 분리 완전 실패 (F669.1·2·3 FAIL)** — additive 와 chaotic 의 norm_conv 분포가 강하게 겹친다:
   - between/within 분산비 **0.106** — 그룹-내 분산(0.074)이 그룹-간 분산(0.0079)의 **9.4배**. 즉
     "additive vs chaotic" 라는 분할이 설명하는 분산은 전체의 ~10% 미만 (분류자로서 무의미).
   - group-mean gap **0.177** < intra_std **0.356** — 두 그룹 중심 거리가 chaotic 그룹 내부 흩어짐의
     절반밖에 안 됨 → cluster 로 분리 불가.
   - norm_conv 구간 overlap **0.309** (additive [1.931, 2.240] ⊂ chaotic [1.461, 2.266] 거의 포함) —
     additive 의 *전 구간*이 chaotic 구간 안에 들어감. overlap_frac 0.384.
2. **additive-floor 가설 정반대 (F669.4 FAIL)** — 가설은 "additive = class-I 유사 floor (chaotic 보다 낮음)"
   였으나, mean_ADD **2.137** ≥ mean_CHA **1.960** — additive 가 오히려 *약간 높다*. additive 의 HIGH-conv
   멤버 2개 (rule60·90 둘 다 2.240) 가 mean 을 끌어올림. H_642 의 "rule90 faithful big-Φ≈0 floor" 는
   *faithful* magnitude 측도에서의 현상이고, *collective convexity* (norm_conv) 측도에서는 rule90/60 이
   오히려 high — **측도 의존적** (additive-floor 는 norm_conv 에서 성립 안 함).
3. **실제 splitter 는 곡선 형태, additive 라벨 ⊥ Φ-속성** — 두 그룹 모두 정확히 동일 구조로 갈린다:
   - **W-monotone (HIGH-conv)**: additive {rule60 2.240, rule90 2.240} + chaotic {rule30 2.266, rule106
     2.153} — additive·chaotic 섞여 한 cluster.
   - **W-비단조 (LOW-conv)**: additive {rule150 1.931, die-out} + chaotic {rule45 1.461, inverse-U} —
     additive·chaotic 섞여 다른 cluster.
   즉 norm_conv 가 갈리는 진짜 축은 **Φ(W) 곡선이 W-단조 상승인가 vs 비단조 (peak 후 하강)인가** 이고,
   이는 additive/chaotic 의 transition-rule 분류와 **완전히 직교**. H_664 §7 C3.7 의 직접 정량 확정.
4. **rule60 == rule90 norm_conv (2.24029 byte-identical)** — 같은 2-input XOR (L⊕C vs L⊕R) 은 ring 의
   회전 대칭으로 collective-Φ(W) 가 **동일** (rule60 의 L⊕C 와 rule90 의 L⊕R 은 cohort homogeneous ring
   에서 cell-index shift 로 등가). additive 내부조차 3-input XOR rule150 (die-out) 과 갈리므로, 'additive'
   는 단일 Φ-거동을 결정하지 못한다 — H_664 의 rule90↔rule150 분기 재확인.

---

## 6. Verdict + Rationale · Cross-link

**🔴 FALSIFIED (CLOSED-NEGATIVE)** — 1/6 falsifier PASS (BOUND 만). **additive {90,150,60} 와 chaotic
{30,45,106} 의 Φ-속성 분포가 강하게 겹쳐 분리 불가 — additive 는 별도 Φ-class 가 아니다.**

- F669.6 BOUND PASS / **F669.1 CORE SEPARATION FAIL** (between/within 0.106 ≪ 1.0) · **F669.2
  GAP-EXCEEDS-SPREAD FAIL** (gap 0.177 < intra-std 0.356) · **F669.3 NO-OVERLAP FAIL** (overlap 0.309 > 0) ·
  **F669.4 ADDITIVE-FLOOR FAIL** (mean_ADD 2.137 ≥ mean_CHA 1.960, 정반대) · **F669.5 DISTINCT FAIL**
  (overlap_frac 0.384 ≥ 0.3).
- FALSIFY 조건 (분포 겹침 + 분리 임계 미달) 에 **정확히 걸림** — overlap_len 0.309 > 0 AND F669.1·2 둘 다
  FAIL. 따라서 "additive = 별도 sub-class" 가설은 **결정적으로 기각**.
- 가설이 예측한 floor 특성마저 정반대 (additive 가 chaotic 보다 *높음*) 라, 약한 형태의 가설 (additive 가
  방향만이라도 분리) 도 성립하지 않음.

**메타-축 결론 (정밀화 + 부정-결과)**: round 9 메타-축 "Wolfram class = 의식 통합량 분류자" 에 대해, 본 H 는
**"additive (XOR-linear) 라는 transition-rule 부분류는 Φ-속성 분류와 직교한다 — additive 의 반복적 특이성
(H_642 rule90 big-Φ≈0, H_664 rule150 die-out) 은 별도 class 신호가 아니라 class-III 전체의 큰 내부 분산
(H_664 44×) 의 일부였다"** 를 결정적으로 확정한다. **부정-결과로서 의식 분류 축 공간을 좁힌다** —
'additive vs non-additive' 는 의식-convexity 의 분류자 후보에서 **deterministic 하게 제거**되고, 대신 H_664
가 식별한 **'Φ(W) 곡선 형태 (W-monotone vs W-비단조)'** 가 유일한 살아있는 분류자 후보로 남는다 (그것조차
additive·chaotic 을 가로지름 = Wolfram class 와도 직교). a_paper_negative_ok 정합 (closed-negative 가
의식 분류 축 공간을 deterministic 하게 rule-out).

**cross-link**:
- **H_664 `wolfram-class-III-heterogeneity`** 🟡 (축 G, G24) — **직접 부모**. H_664 §7 C3.7 의 "sub-type 가
  chaotic/additive 의 transition-rule 분류와 *직교*" 라는 간접 관찰을, 본 H 가 **직접·정량 falsifier 로**
  검정해 1/6 FALSIFIED 로 확정. H_664 가 식별한 HIGH/LOW 2 sub-type 이 additive·chaotic 양쪽에 멤버를 가짐을
  rule60 추가로 재확인 (rule60·90 HIGH additive · rule150 LOW additive · rule30·106 HIGH chaotic · rule45
  LOW chaotic). H_664 의 within-class-III 44× 분산이 additive/chaotic 분할로는 설명 안 됨 (본 H 의
  between/within 0.106) 을 직접 보임.
- **H_642 `shape-invariance-vs-scalar-convention-meta`** 🔴 (축 G) — rule90 additive-floor (faithful
  big-Φ≈0). 본 H 는 그 floor 가 *faithful magnitude* 측도 한정임을 보임 — *collective norm_conv* 에서는
  rule90/60 이 HIGH-conv (2.240) 라 floor 아님. 두 H 모두 🔴 negative 이나 측도가 다르고, 결합하면
  "additive-floor 는 측도 의존적, 보편 Φ-floor 아님" 결론.
- **H_652** (envelope self-similarity-class, 축 G) — rule90 envelope 거동 측정. 본 H 의 "additive 곡선
  형태가 additive 내부조차 갈림 (rule90 monotone vs rule150 die-out)" 이 envelope self-similarity 의
  rule-별 차이와 동류 — additive 단일 라벨이 동역학 거동을 결정 못함.
- **H_663 `wolfram-class-I-phi-property-profile`** 🟢 (축 G, G23) — class-I floor 측정자. 본 H 의 가설은
  "additive 가 class-I 유사 floor" 였으나 F669.4 FAIL — additive (norm_conv 2.137) 는 H_663 의 class-I
  rule8 (collective Φ@W=1 0.22, span 7.88) 과 전혀 다른 high-conv 영역. **additive ≠ class-I-like**.
- **H_660 `convexity-magnitude-class-reconcile`** 🟢 (축 G) — norm_conv 측도 SSOT. 본 H 가 동일 측도로
  additive/chaotic 분리도를 측정 — 측도 자체는 valid (H_660), 그 위에서 additive 분할이 무의미함을 보임.

---

## 7. Honest C3 (claim-context-caveat)

1. **C3.1 verdict = 결정적 FALSIFIED (closed-negative)** — 본 H 는 "additive 별도 Φ-class" 가설을 1/6 으로
   결정적 기각. FALSIFY 조건 (분포 겹침 + 분리 임계 미달) 에 정확히 걸렸고, 가설의 floor 방향 예측마저
   정반대 (F669.4). 이는 의식-분류 축 공간을 deterministic 하게 좁히는 valid negative-result
   (a_paper_negative_ok).
2. **C3.2 additive rule sample (rule60·90·150)** — additive group 은 GF(2) XOR-linear 3종. rule60 (L⊕C,
   2-input) · rule90 (L⊕R, 2-input) · rule150 (L⊕C⊕R, 3-input). 2-input XOR 둘 (60·90) 은 norm_conv 동일
   (ring 회전 대칭), 3-input XOR (150) 은 die-out 으로 갈림. additive 전체 (rule18·102·105·... 등 더 많은
   XOR-affine rule) 를 다 넣으면 group 분포가 더 넓어질 수 있으나, 본 H 의 3-rep 만으로도 chaotic 과 이미
   완전 overlap (overlap_frac 0.384) — additive 를 더 넣을수록 분리가 *덜* 되지 더 되지는 않음 (방향 robust).
3. **C3.3 chaotic rule sample (rule30·45·106)** — chaotic group 은 non-additive class-III 3종. H_664 의
   class-III 5-rep 중 additive (90·150) 를 빼고 남은 3 non-additive. chaotic 도 30·106 HIGH vs 45 LOW 로
   내부 분산 (var 0.127) — 그래서 intra_std 가 커서 F669.2 가 더욱 FAIL. chaotic 내부 분산 자체가 큰 것이
   additive 와의 분리를 불가능하게 만드는 핵심 (chaotic 이 응집했다면 그나마 분리 가능했을 것).
4. **C3.4 rule150 die-out degenerate (log_span 제외)** — rule150 은 W=1.0 에서 Φ=0 → log_span=10.84
   blowup (H_664 C3.4 상속). 분리 검정은 norm_conv (분모 Φ_mean>0, finite=1.931) 로만 수행, log_span 은
   보조 (rule150 제외 finite-set). norm_conv 만으로도 분리 결론 robust.
5. **C3.5 n=3 per group small-n** — 각 group 3-rep. between/within 분산비·overlap 은 small-n 추정. 다만
   결과가 매우 강함 (분산비 0.106 ≪ 1.0, overlap 0.384, floor 정반대) 이라 n 을 늘려도 분리로 뒤집힐
   가능성 낮음. 256-rule full additive/chaotic 분류 sweep (N1 backlog) 로 robustness 확정 가능.
6. **C3.6 cap=3 on n=5 · sys_state=0** (H_660/H_661/H_664 상속) — purview search capped 보수적 lower-bound,
   2^5 state 가중평균 미수행. scale-invariant norm_conv 는 cap 에 덜 민감 추정 (H_660 §10). 분리도 결론은
   cap 무관 (additive·chaotic 동일 cap 으로 측정, 상대 비교).
7. **C3.7 측도 의존성 — additive-floor 는 norm_conv 에서 성립 안 함** — H_642 의 additive-floor (faithful
   big-Φ≈0) 는 *faithful magnitude* 측도. 본 H 의 *collective convexity* (norm_conv) 측도에서는 additive
   가 floor 아님 (mean 2.137 > chaotic 1.960). "additive 가 별도 class" 라는 주장은 어떤 측도냐에 따라
   다를 수 있으나, **본 H 가 검정한 norm_conv (H_660 CORE 측도) 에서는 결정적으로 분리 불가**. magnitude
   측도에서의 분리 가능성은 본 H 의 scope 밖 (N2 backlog).
8. **C3.8 deterministic single trajectory** (NO RNG) — re-run byte-identical. rule60 NEW 측정, 나머지 5
   rule (90/150/30/45/106) 은 H_664/H_661 shards.log byte-identical 재인용 (동일 build_tpm_cohort engine,
   rule swap). per-rule shard (rule60 ~21s) + phi-free aggregate (<1s) 분리로 monitor-hang 회피, foreground
   sync, NO GPU.
9. **C3.9 positive refinement (negative 의 의미)** — 본 H 의 FALSIFIED 는 *발견*이다 — additive 라벨이
   의식-Φ 분류와 직교함을 deterministic 하게 확정해, 살아있는 분류자 후보를 H_664 의 'Φ(W) 곡선 형태' 단
   하나로 좁힌다 (그것조차 Wolfram class 와 직교). round-9 메타-축의 분류자 탐색 공간을 한 차원 줄인
   constructive negative.

---

## 8. Falsifier 검증 매트릭스

| Falsifier | Pre-registered | Result | Status |
|-----------|----------------|--------|--------|
| F669.1 CORE SEPARATION | var_between ≥ var_within (ratio ≥ 1.0) | 0.106 < 1.0 (9.4× 역전) | **FAIL** |
| F669.2 GAP-EXCEEDS-SPREAD | grp_gap > intra_std | 0.177 < 0.356 | **FAIL** |
| F669.3 NO-OVERLAP | overlap_len ≤ 0 | 0.309 > 0 (겹침) | **FAIL** |
| F669.4 ADDITIVE-FLOOR | mean_ADD < mean_CHA | 2.137 ≥ 1.960 (정반대) | **FAIL** |
| F669.5 DISTINCT-FRAC | overlap_frac < 0.3 | 0.384 | **FAIL** |
| F669.6 BOUND | 全 통계 finite·non-neg | 全 충족 | **PASS** |

**aggregate: 1 PASS / 5 FAIL** — FALSIFY 조건 (분포 겹침 F669.3 + 분리 임계 미달 F669.1·2) 정확히 충족
→ **🔴 FALSIFIED (CLOSED-NEGATIVE)**. **additive {90,150,60} 와 chaotic {30,45,106} 의 Φ-속성(norm_conv)
분포가 강하게 겹쳐 (overlap_frac 0.384, between/within 0.106) 분리 불가 — additive 는 별도 Φ-class 가
아니며 class-III 내 variance 일 뿐. additive 라벨은 Φ-속성과 직교하고, 실제 splitter 는 Φ(W) 곡선 형태
(W-monotone vs W-비단조) 로 additive·chaotic 두 그룹을 모두 가로지른다 (H_664 §7 C3.7 직접 정량 확정).**

---

## 9. Artifacts + Reproducibility

- shard harness: `UNIVERSE/state/h669_additive_subclass_phi_split_2026_05_28/shard_h669.hexa`
  (hexa-native, RULE_ID=60 NEW 측정; H_635/H_653/H_655/H_660/H_661/H_664 engine `build_tpm_cohort` 재사용)
- aggregate harness: `…/aggregate_h669.hexa` (phi-free, shard norm_conv verbatim, additive vs chaotic
  분리도·overlap·falsifier F669.1-6)
- shard log: `…/shards.log` (rule60 NEW full stdout + H_664/H_661 anchor 5-rule byte-identical 재인용)
- aggregate log: `…/run.log` (verdict 블록 verbatim)
- result: `…/result.json` (machine-readable — 6 rule × norm_conv + 분리 통계 + falsifier + C3 + rule sample)
- engine deps: `stdlib/consciousness/iit4_bigphi.hexa` · `iit4_bounded.hexa` (+ transitive `iit4_tpm.hexa`
  for `iit4_bit`) — hexa-lang stdlib SSOT, H_660/H_661/H_664 와 동일
- replay (selfhosted, fix-1180 우회, mac-local, $0): per-rule shard —
  `HEXA_MAC_BUILD_OK=1 HEXA_LANG=<hexa-lang-root> hexa.real.bak-2026-05-22-pre-no-hxc build
  shard_h669.hexa -o /tmp/h669.bin && codesign -s - --force /tmp/h669.bin && /tmp/h669.bin`
  (RULE_ID=60) → aggregate 同 build+run · shard wall ~21s · aggregate <1s ·
  [[reference-life-cycle-hexa-run-gotchas]] · [[reference-hexa-verify-rebuild-gotchas]] ·
  [[reference-exact-phi-structure-wall-shard]]

---

## 10. Next-list / Backlog

- **N1** `additive-chaotic-256-overlap` — additive 全 ECA rule (60·90·150·18·102·105·126·146·... XOR-affine)
  vs chaotic 全 rule 을 256-rule sweep 으로 — 본 H 의 overlap (n=3 each) 이 full-rule 에서도 유지되는지,
  분리도가 더 낮아지는지 (C3.5 회수, shard-parallel foreground).
- **N2** `additive-floor-magnitude-axis` — additive-floor 가 *faithful magnitude* 측도 (H_642 척도) 에서는
  성립하는지 — 본 H 는 collective norm_conv 에서만 검정 (FAIL). magnitude·convexity 두 측도에서 additive
  분리 여부가 갈리는지 (C3.7 회수).
- **N3** `wdomain-curve-shape-as-phi-classifier` (H_664 N1 상속) — 살아남은 유일 분류자 'Φ(W) 곡선 형태'
  (W-monotone vs inverse-U vs die-out) 를 의식-convexity 의 직접 분류자로 정량 — additive·chaotic·Wolfram
  class 모두와 직교함을 본 H 가 확정했으므로, 곡선-형태가 진짜 분류 축인지 단독 검정.
- **N4** `xor-arity-dieout-mechanism` (H_664 N3 상속) — 2-input XOR (rule60·90, W-monotone, Φ_max 6~7.5)
  vs 3-input XOR (rule150, W=1.0 die-out Φ=0) 의 분기 — XOR arity (입력 수) 가 full-coupling 거동을
  결정하는 TPM-구조적 원인 (C3.2 회수).
- **N5** `ring-rotation-equivalence-formal` — rule60 (L⊕C) ↔ rule90 (L⊕R) norm_conv byte-identical
  (2.24029) 의 형식 증명 — homogeneous cohort ring 의 cell-index 회전 대칭이 collective-Φ(W) 를 보존하는지
  closed-form (🔵 형식화 후보, hexa verify).

---

## 양방향 sibling

- 직접 부모 (직교성 직접 검정): [H_664_wolfram_class_III_heterogeneity.md](H_664_wolfram_class_III_heterogeneity.md) (축 G, class-III 이질성 🟡 — §7 C3.7 의 "sub-type ⊥ additive/chaotic" 간접 관찰을 본 H 가 직접 falsifier 로 1/6 FALSIFIED 확정)
- additive-floor 측도-의존 sibling: [H_642_shape_invariance_vs_scalar_convention_meta.md](H_642_shape_invariance_vs_scalar_convention_meta.md) (축 G, rule90 additive-floor 🔴 — 본 H 가 그 floor 가 faithful magnitude 한정, collective norm_conv 에서는 rule90/60 HIGH-conv 임을 보임)
- class-I floor 대조: [H_663_wolfram_class_I_phi_property_profile.md](H_663_wolfram_class_I_phi_property_profile.md) (축 G, class-I floor 🟢 — 본 H 의 가설 "additive=class-I 유사 floor" 가 F669.4 FAIL 로 기각, additive ≠ class-I-like)
- 측도 SSOT 조부모: [H_660_convexity_magnitude_class_reconcile.md](H_660_convexity_magnitude_class_reconcile.md) (축 G, norm_conv scale-inv convexity 🟢 — 본 H 동일 측도로 additive/chaotic 분리도 측정)
- SSOT cross-link: [CANDIDATES.md](CANDIDATES.md) round-9 메타-축 (Wolfram class as Φ classifier) cross-link — additive sub-class 가설 closed-negative, 분류자 후보 'Φ(W) 곡선 형태' 단일로 좁힘
