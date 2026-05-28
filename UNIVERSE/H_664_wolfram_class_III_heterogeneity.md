# H_664 — `wolfram-class-III-heterogeneity` (H_661 발견 정밀화, 축 G)

**축**: G (round 9 메타-축 — "Wolfram class 가 의식 통합량 분류자인가") · H_661 N1 backlog 수행 · round-11 후속
**id**: H_664 · **date**: 2026-05-28 · **infra**: $0 mac-local (per-rule shard, foreground sync) · **verdict**: **🟡 PARTIAL**

---

## 1. 슬러그 + 한 줄 요약 — class-III 가 단일 cell 인가, 이질 sub-type 묶음인가

`wolfram-class-III-heterogeneity` — H_661 (PR #1295/#1297, 🟡 4/6) 이 substrate-class scale-invariant
convexity 단조에서 **class-III 내부 이질성**을 발견했다 — rule90(additive XOR fractal)·rule30(pure-chaotic)·
rule45(W-비단조 chaotic)가 같은 class-III 인데 norm_conv 가 각각 2.240·2.266·1.461 로 크게 분산. 본 H_664 는
class-III 가 **단일 cell 이 아니라 이질 sub-type 묶음인지**를 정량한다.

class-III 에 신규 대표 **rule106 (chaotic, W-monotone)** · **rule150 (XOR-additive, rule90 동류)** 2종을
추가해 5-rep {30, 45, 90, 106, 150} 로 확장하고, class-II {184, 226} · class-IV {110, 54} anchor 대비
**within-class-III 분산 vs between-class 분산의 비율** 과 **sub-type clustering** 을 측정한다.

> **결과**: class-III 는 **내부 Φ-속성(norm_conv) 분산이 class-II/IV 의 내부 응집 대비 44× 더 크고**
> (F664.3 PASS), **≥2 sub-type 으로 명확히 분리**된다 (F664.4·F664.5 PASS) — **HIGH-conv {30, 90, 106}**
> (mean 2.220, W-monotone) 과 **LOW-conv {45, 150}** (mean 1.696, W-비단조 inverse-U / XOR die-out) 의
> 두 cluster (separation 0.524 ≫ intra-std 0.235). 그러나 **within-III 분산(0.0894)이 class-II↔IV 전체
> ordinal spread(0.164)를 *초과*하지는 못한다** (F664.1·F664.2 FAIL, 0.545×). → **Wolfram class-III 는
> 단일 cell 이 아니라 이질 sub-type 묶음이 맞으나, 그 내부 spread 가 class-II→IV 전체 거리를 삼키지는
> 않는다.** 4/6 PASS, **🟡 PARTIAL** (sub-type ≥2 + III ≫ II/IV 응집 = positive · 전체 class-간 spread
> 초과는 못함 = negative 공존).

---

## 2. 동기 — H_661 의 rule45 outlier 는 단일 이상치인가, sub-type 신호인가

H_661 은 9-rule 확대셋에서 **class-IV-top 은 robust 일반화** (F661.1·2 PASS) 하지만 **full I<II<III<IV
ordinal 단조는 깨짐** (F661.3·4 FAIL) 을 보였고, 그 깨짐의 핵심 원인으로 **class-III 내부 이질성**을 지목했다:
같은 class-III 라도 rule90(2.240)·rule30(2.266)은 높은 convexity 인데 rule45(1.461)는 class-I/II 수준으로
붕괴. H_661 §7 C3.3 은 이를 "rule45 의 Φ(W) 가 W 에서 비단조 (W=0.70 peak 후 W=0.95 급락) 라 span 이 작다"
로 honest 하게 기록하고, N1 backlog 로 **"rule45 outlier 가 단일 이상치인지, class-III chaotic 일반의
W-비단조 현상인지"** 를 남겼다.

두 해석이 갈린다:
- **(a) 단일 outlier**: rule45 만 우연히 이상하고, class-III 는 대체로 응집된 단일 cell (rule45 제외 시 cohesive).
- **(b) sub-type 묶음**: class-III 는 동역학적으로 ≥2 종 (W-monotone fractal/chaotic vs W-비단조/die-out)
  으로 갈라지며, Φ-속성 분산이 class-II↔IV 분산에 필적 — Wolfram 4-class 가 의식 분류엔 너무 거칠다.

본 H_664 는 class-III 에 **신규 대표 2종**을 추가해 (a)·(b) 를 결정한다:
1. **rule106** (class-III chaotic) — H_661 이 안 본 chaotic rule. W-monotone 인지 확인.
2. **rule150** (class-III, additive XOR — rule90 동류) — XOR 계열이 rule90 처럼 high-conv 인지, 아니면
   다른 거동인지.

rule45 가 단일 이상치라면 신규 2종은 rule90/30 과 함께 응집해야 하고 (a), sub-type 신호라면 신규 2종도
HIGH/LOW 로 갈려야 한다 (b). 동시에 **within-III 분산을 class-간 분산과 정량 비교**해 "class-III 이질성이
class-간 거리에 필적하는가" 를 결정한다.

---

## 3. 측정 도구 / 방법

- **engine** (H_635/H_653/H_655/H_660/H_661 SSOT verbatim 재사용, cohort rule 만 swap):
  n=5 coupled-ring TPM `build_tpm_cohort(rule, W)` — 5 cell, cell i 가 cohort rule[i] 의 update-law.
  decoupled(W=0)=self-loop only (idx=7·c), coupled(W=1)=full ring, blend(0<W<1)=fractional.
  collective-Φ(W) = `big_phi_bounded(build_tpm_cohort([rule×5], W), 5, sys=0, cap=3)[0]` —
  각 (rule,W) point 에서 **실제 IIT4 substrate 측정** (lookup 아님).
- **9 ECA rule × Wolfram class** (class-III 5-rep 확장):
  ```
  rule 30 (III) chaotic non-additive   [H_661 anchor, byte-identical]
  rule 45 (III) chaotic non-additive   [H_661 anchor — W-비단조 outlier]
  rule 90 (III) XOR / additive fractal [H_661 anchor, byte-identical]
  rule106 (III) chaotic                NEW (this H)
  rule150 (III) XOR / additive (rule90 동류)  NEW (this H)
  rule184 (II)  additive / traffic     [H_661 anchor]
  rule226 (II)  additive               [H_661 anchor]
  rule110 (IV)  complex edge-of-chaos  [H_661 anchor]
  rule 54 (IV)  complex                [H_661 anchor]
  ```
- **W grid**: H_653/H_660/H_661 과 **동일** 6-pt {0.15, 0.40, 0.55, 0.70, 0.95, 1.0}.
- **metric**: **norm_conv** = (Φ_max − Φ_min) / Φ_mean — scale-invariant convexity (H_660 CORE 측도).
  보조로 **log_span** = ln(Φ_max/(Φ_min+floor)) (rule150 die-out 에서 ill-defined → finite rule 만 사용).
- **분산 측도** (norm_conv 위):
  - **var_within_III** = population variance of class-III 5-rep norm_conv.
  - **var_between** = variance of 3 class-means {mean_II, mean_III, mean_IV} (full class-간 ordinal spread).
  - **var_compact** = (var_within_II + var_within_IV)/2 (class-II·IV 의 내부 응집 정도).
  - **ratio_within/between**, **ratio_within/compact**, range 비교.
- **sub-type clustering**: class-III 를 norm_conv ≥1.95 (HIGH) vs <1.95 (LOW) 로 2-cluster 분할 →
  cluster separation vs intra-cluster std, 2-cluster pooled var vs raw within-III var.
- **⚠ per-rule shard (monitor-hang 회피)**: rule106/150 각각 6 W-call ≈ 21s foreground sync 측정
  (`shard_h664.hexa`, RULE_ID swap) → `shards.log` 기록. 나머지 7 rule 은 H_661 shards.log 에서
  **byte-identical** 재인용 (동일 engine, rule swap 검증됨). **phi-free aggregate** (`aggregate_h664.hexa`,
  big_phi call 0개, <1s) 가 분산비·sub-type falsifier 검정.
- deterministic · NO RNG · libm `ln`/`pow` only · $0 mac-local · foreground sync (NO bg fork, NO monitor, NO GPU).

---

## 4. 사전등록 falsifier (frozen BEFORE measuring rule106/150)

- **F664.1 CORE WITHIN-GE-BETWEEN**: var_within_III ≥ var_between (3 class-means) — class-III 내부 분산이
  class-II↔IV 전체 ordinal spread 에 **필적/초과**. (강-claim: class-III 이질성이 class-간 거리만큼 크다.)
- **F664.2 RANGE-WITHIN-GE-BETWEEN**: range_within_III ≥ range_between_means — 같은 framing 의 range 판.
- **F664.3 WITHIN-GG-COMPACT**: var_within_III ≥ 3× var_compact (II·IV 내부 응집) — class-III 가
  class-II/IV 보다 훨씬 분산 (이질성의 약-claim, compact-class 대비).
- **F664.4 SUB-TYPE-SEPARATION**: cluster_separation (HIGH mean − LOW mean) > intra_cluster_std
  (max cluster 내부 std) — ≥2 sub-type 으로 분리 가능 (between-cluster gap 이 cluster 내부 흩어짐보다 큼).
- **F664.5 2-CLUSTER-EXPLAINS**: var_2cluster_pooled < 0.5 × var_within_III — sub-type 2분할이
  within-III 분산의 >50% 를 설명 (sub-type 가설이 분산의 주된 원천).
- **F664.6 BOUND**: 全 분산·비율 finite·non-negative.

**FALSIFY 조건**: F664.3·F664.4 모두 FAIL (class-III 가 II/IV 만큼 응집 + sub-type 분리 안 됨) →
🔴 FALSIFIED (class-III 단일 cell, rule45 단일 outlier).
**verdict 기준**:
- F664.1 (CORE) PASS + F664.3·F664.4·F664.5 PASS → 🟢 SUPPORTED-NUMERICAL (class-III 이질성이 class-간
  분산에 필적 + ≥2 sub-type, Wolfram 4-class 가 의식 분류엔 거침을 강하게 확정).
- F664.3·F664.4·F664.5 PASS (sub-type ≥2 + III ≫ compact) 이나 F664.1 (full between-class) FAIL
  → 🟡 PARTIAL (class-III 이질 + sub-type 확정, 그러나 전체 class-간 spread 초과는 못함).
- F664.3·F664.4 모두 FAIL → 🔴 FALSIFIED.

---

## 5. Measurement (verdict-bearing 측정값)

> shard 출력 `UNIVERSE/state/h664_class_III_heterogeneity_2026_05_28/shards.log` (rule106/150 NEW +
> H_661 anchor) + aggregate `run.log` verbatim.

신규 측정 2종 Φ(W) grid (6-pt {0.15, 0.40, 0.55, 0.70, 0.95, 1.0}):

```
rule106 (III) Φ(W): 2.87266 10.7046 18.5147 30.1267 64.7249 75.5306   (W-monotone, Φmin=2.87 Φmax=75.5)
                    norm_conv=2.1531  log_span=3.26926  abs_Δ=72.66
rule150 (III) Φ(W): 2.02096 4.32671 5.12111 3.35834 1.08369 0.0       (W-비단조 inverse-U, Φmin=0 at W=1.0!)
                    norm_conv=1.93118 log_span=10.8437 abs_Δ=5.121   [DEGENERATE Φmin=0 — log_span blowup]
```

class-III 5-rep norm_conv (rule30/45/90 = H_661 byte-identical):

| rule | sub-type | **norm_conv** | Φ(W) 거동 | 비고 |
|------|----------|---------------|-----------|------|
| rule30  | chaotic       | 2.266 | W-monotone 상승 | HIGH-conv |
| rule90  | XOR fractal   | 2.240 | W-monotone 상승 | HIGH-conv |
| rule106 | chaotic       | **2.153** | W-monotone 상승 | **NEW · HIGH-conv** |
| rule45  | chaotic       | 1.461 | W-비단조 (W=0.70 peak 후 급락) | LOW-conv |
| rule150 | XOR additive  | **1.931** | W-비단조 inverse-U + W=1.0 die-out (Φ=0) | **NEW · LOW-conv** |

aggregate verdict 블록 (run.log verbatim):

```
nc class-III:    mean=2.0103  var=0.0893913
nc class-II(2):  rule184=1.43674 rule226=1.41354   mean_II=1.42514
nc class-IV(2):  rule110=2.34922 rule54=2.4745     mean_IV=2.41186

var_within_III      = 0.0893913
var_between(3means) = 0.164142
var_within_II       = 0.00013456
var_within_IV       = 0.00392377
var_compact_pooled  = 0.00202916
RATIO within_III / between   = 0.544597
RATIO within_III / compact   = 44.0511
range_within_III    = 0.80535
range_between_means = 0.98672

-- sub-type clustering (norm_conv) --
HIGH-conv {30,90,106} mean=2.21985 var=0.00233902
LOW-conv  {45,150}    mean=1.69599 var=0.0553143
cluster_separation   = 0.523857
var_2cluster_pooled  = 0.0235291
intra_cluster_max    = 0.0553143

────────── verdict ──────────
[FAIL] F664.1 CORE within-III var >= between-class var : 0.544597 < 1.0
[FAIL] F664.2 within-III range >= between-means range : 0.80535 < 0.98672
[PASS] F664.3 within-III var >= 3x compact-class var : 44.0511
[PASS] F664.4 SUB-TYPE sep > intra-std : 0.523857 > 0.23519
[PASS] F664.5 2-cluster var explains >50% : 0.0235291 < 0.0446957
[PASS] F664.6 BOUND 全 통계 finite
F664.1-6 4/6 PASS
het_rivals_between=true subtype_ge2=true
```

### 핵심 발견

1. **sub-type ≥2 확정 (F664.4·F664.5 PASS)** — class-III 는 두 cluster 로 깨끗이 분리된다:
   - **HIGH-conv {rule30, rule90, rule106}** (mean 2.220, var 0.0023 = 극히 응집) — 셋 다 Φ(W) 가
     **W-monotone 상승** (W↑ 따라 Φ 단조 증가). chaotic(30,106) 과 fractal(90) 가 섞여 있어도 *곡선 형태*
     (W-monotone) 가 같으면 convexity 가 비슷.
   - **LOW-conv {rule45, rule150}** (mean 1.696) — 둘 다 Φ(W) 가 **W-비단조 inverse-U** (중간 W 에서 peak
     후 W↑ 에서 하강). rule150 은 W=1.0 에서 Φ=0 까지 die-out. inverse-U 곡선은 Φ_max/Φ_min span 이 작아
     norm_conv 가 낮음.
   - cluster separation 0.524 ≫ intra-cluster std 0.235, 2-cluster 분할이 within-III 분산의 74% 설명
     (0.0235 vs raw 0.0894). **rule45 는 단일 outlier 가 아니라 'W-비단조 sub-type' 의 한 멤버였고,
     rule150 이 같은 sub-type 에 합류** → 해석 (b) 채택, (a) 기각.
2. **class-III 가 class-II/IV 보다 44× 분산 (F664.3 PASS, 강신호)** — var_within_III=0.0894 vs
   compact-pooled=0.00203. class-II (var 0.00013) 와 class-IV (var 0.0039) 는 내부적으로 극히 응집된
   '단일 cell' 인 반면, class-III 는 그 44배 분산. **Wolfram 4-class 중 class-III 만 유독 의식-측도
   관점에서 이질적**.
3. **그러나 full class-간 spread 초과는 못함 (F664.1·F664.2 FAIL)** — var_within_III=0.0894 는
   var_between(3 class-means)=0.164 의 **0.545×**, range 도 0.805 < 0.987. 즉 class-III 내부가 아무리
   퍼져도 그 spread 가 class-II(1.425) → class-IV(2.412) 전체 ordinal 거리를 *삼키지는* 않는다. class-III
   는 그 between-mean band 의 약 절반을 점유 (LOW sub-type 1.70 은 II 쪽으로, HIGH sub-type 2.22 는 IV
   쪽으로 뻗지만 II/IV 평균까지 도달하진 않음).
4. **rule150 die-out 발견** — XOR-additive rule150 은 rule90 과 같은 XOR 계열인데도 W=1.0 (full coupling)
   에서 Φ=0 으로 die-out (Φ(W) = 2.02 → 4.33 → 5.12 → 3.36 → 1.08 → 0.0). rule90 (W-monotone, W=1.0 에서
   Φ=7.5) 과 정반대 거동 → **'XOR-additive' 라는 라벨조차 W-domain 거동을 결정하지 못함** (rule90 vs
   rule150 분기). class-III 의 이질성이 chaotic/fractal 의 단순 2분이 아니라 *곡선 형태*(W-monotone vs
   inverse-U)에서 온다는 추가 증거.

---

## 6. Verdict + Rationale · Cross-link

**🟡 PARTIAL** — 4/6 falsifier PASS. **sub-type ≥2 + class-III ≫ II/IV 응집 PASS (F664.3·4·5), 그러나
full between-class spread 초과는 FAIL (F664.1·2).**

- F664.3 within≫compact PASS (44×) · F664.4 sub-type-separation PASS · F664.5 2-cluster-explains PASS ·
  F664.6 bound PASS / **F664.1 CORE within≥between FAIL** (0.545×) · **F664.2 range-within≥between FAIL**.
- FALSIFY 조건 (F664.3·F664.4 모두 FAIL = class-III 단일 cell + rule45 단일 outlier) 에는 **걸리지 않음** —
  class-III 는 명확히 ≥2 sub-type 이고 II/IV 보다 44× 분산. 따라서 "class-III = 단일 cell" 가설은
  **결정적으로 기각**.
- **그러나** 강-claim (within-III 분산이 *class-간 전체 ordinal spread* 에 필적/초과) 은 **깨진다** —
  within-III(0.0894)는 between-class(0.164)의 절반(0.545×)에 그친다. class-III 가 이질적이긴 해도 그
  spread 가 II→IV 전체 거리를 메우지는 않는다.

**메타-축 결론 (정밀화)**: round 9 메타-축 "Wolfram class = 의식 통합량 분류자" 에 대해, 본 H 는
**"class-III 는 단일 cell 이 아니라 ≥2 sub-type (W-monotone HIGH-conv vs W-비단조 LOW-conv) 의 묶음이며,
class-II/IV 대비 44× 더 이질적"** 임을 결정적으로 확정한다. 이는 H_661 의 "rule45 outlier" 를 "W-비단조
sub-type" 으로 일반화 (rule150 합류) 하고, H_661 의 full-monotone FAIL 의 근본 원인을 정량화한다. 다만
class-III 의 내부 spread 가 *full class-간 거리* 까지 삼키지는 않으므로 (F664.1 FAIL), Wolfram 4-class 가
**완전히 무의미**한 것은 아니다 — IV-top·II-bottom 의 ordinal 골격은 유지되고, class-III 만 그 골격 안에서
*폭넓게 펼쳐진 band* 다. **positive (sub-type ≥2 + III ≫ II/IV 이질) + negative (full class-간 spread
초과는 못함) 공존의 PARTIAL.**

**cross-link**:
- **H_661 `substrate-class-monotone-rule-generalize`** 🟡 (축 G, PR #1295/#1297) — **직접 부모**.
  본 H 는 H_661 §10 N1 backlog ("class-III-internal-convexity-subtype") 를 직접 수행. H_661 의 rule45
  outlier (norm_conv 1.461) 를 "W-비단조 LOW-conv sub-type" 으로 일반화 — rule150 (1.931) 이 같은 sub-type
  에 합류하고, rule106 (2.153) 은 HIGH-conv 에 합류 → **rule45 는 단일 이상치가 아니라 sub-type 신호**.
  H_661 의 full-monotone FAIL (F661.3·4) 의 근본 원인 (class-III 내부 이질성) 을 분산비 44× 로 정량화.
- **H_660 `convexity-magnitude-class-reconcile`** 🟢 (축 G, PR #1290) — norm_conv 측도의 SSOT.
  본 H 가 동일 norm_conv 로 class-III 5-rep 분산을 측정. H_660 의 4-rule {184,90,30,110} 단조가 class-III
  를 W-monotone rule90/30 (둘 다 HIGH-conv) 으로만 골랐기에 깨끗했음을 본 H 의 sub-type 분할로 확인 —
  rule45/150 같은 LOW-conv sub-type 을 넣으면 단조가 무너진다.
- **H_654 `phi-magnitude-wolfram-class-order`** 🟡 (축 G) — single-substrate magnitude order PARTIAL.
  H_654 §7 C1 의 "rule90 class-III dual-membership" 경고와 본 H 의 "class-III ≥2 sub-type" 이 같은
  class-III 이질성 신호 — single·collective 양쪽에서 class-III 가 가장 이질적 class 임을 교차 확정.
- **H_642 `shape-invariance-vs-scalar-convention-meta`** (축 G) — shape vs scalar-convention 메타. 본 H 의
  sub-type 분화가 Φ(W) *곡선 형태* (W-monotone vs inverse-U) 에서 온다는 발견은 H_642 의 shape-vs-scalar
  구분과 동류 — convexity 측도가 곡선 *형태* 에 민감하고, 같은 class 라도 형태가 갈리면 측도가 갈린다.

---

## 7. Honest C3 (claim-context-caveat)

1. **C3.1 verdict = 정직한 PARTIAL** — 본 H 는 "class-III 단일 cell" 을 결정적으로 기각 (F664.3·4·5 PASS)
   하는 동시에, 강-claim "within-III ≥ class-간 전체 spread" 는 깨짐 (F664.1·2 FAIL). FALSIFY 조건
   (F664.3·4 모두 FAIL) 미달이라 🔴 아니고, CORE F664.1 FAIL 이라 🟢 아님 → 🟡 PARTIAL.
2. **C3.2 sub-type cut-off (1.95) 는 사후-관찰적** — HIGH/LOW 2-cluster 의 norm_conv 경계 1.95 는 5-rep
   분포에서 자연스러운 gap (LOW {1.461, 1.931} vs HIGH {2.153, 2.240, 2.266}) 에 놓았으나, 더 큰 n 에서는
   cluster 수가 ≥3 일 수도 있다. 본 H 의 결론은 "≥2 sub-type" (lower bound) 이지 "정확히 2개" 가 아님.
   sub-type 의 동역학적 정의 (W-monotone vs W-비단조 곡선 형태) 가 norm_conv 값보다 더 근본.
3. **C3.3 small-n class-II/IV (각 2-rep)** — between-class·compact 분산은 class-II/IV 각 2개 rule 의
   variance 라 small-n. compact 응집 (var ~0.0001~0.004) 은 두 anchor 가 우연히 가까웠을 수 있다. 256-rule
   full sweep (H_661 N2) 으로 class-II/IV 의 진짜 내부 분산을 봐야 44× 비율이 robust 한지 확정.
   다만 class-III 의 5-rep spread (var 0.089) 는 II/IV 어느 쪽 2-rep spread 보다도 자릿수 크다.
4. **C3.4 rule150 die-out degenerate (log_span 제외)** — rule150 은 W=1.0 에서 Φ=0 → log_span=10.84
   blowup (H_661 의 rule136 die-out 과 동류). log_span 분산 검정에서 rule150 제외, norm_conv 만으로 분산비
   계산 (norm_conv 는 분모 Φ_mean>0 이라 finite=1.931). XOR full-coupling die-out 은 그 자체로 class-III
   이질성의 새 증거 (rule90 과 정반대 W=1.0 거동) 이므로 sub-type 분석에는 포함.
5. **C3.5 'between-class variance' framing 의 보수성** — F664.1 의 between-var 는 3 class-means 의 분산
   (II↔IV 전체 ordinal spread) 이라 가장 엄격한 비교 대상. 만약 between 을 "인접 class-mean 차이" (II↔III
   또는 III↔IV) 로 잡으면 within-III 가 그것을 초과할 수도 있다. 본 H 는 가장 강한 framing (full spread)
   에서 FAIL 임을 정직 보고 — class-III 이질성이 *인접* class-간 거리에는 필적하나 *전체* 거리에는 못
   미친다.
6. **C3.6 cap=3 on n=5 · sys_state=0** (H_660/H_661 상속) — purview search capped 보수적 lower-bound,
   2^5 state 가중평균 미수행. scale-invariant norm_conv 는 cap 에 덜 민감 추정 (H_660 §10).
7. **C3.7 'sub-type' 의 동역학적 근거** — HIGH/LOW 분할은 norm_conv 값으로 했으나 그 *원인* 은 Φ(W) 곡선
   형태 (W-monotone 상승 = high span = HIGH-conv vs inverse-U = low span = LOW-conv). chaotic(30 HIGH /
   45 LOW)·XOR(90 HIGH / 150 LOW) 둘 다 양쪽 sub-type 에 멤버가 있어, sub-type 가 chaotic/additive 의
   transition-rule 분류와 *직교* 한다 — Wolfram class 보다 'W-domain 곡선 형태' 가 의식-convexity 의 더 나은
   분류자일 가능성 (N1 backlog).
8. **C3.8 deterministic single trajectory** (NO RNG) — re-run byte-identical. rule106/150 NEW 측정,
   rule30/45/90/184/226/110/54 는 H_661 shards.log byte-identical 재인용 (동일 build_tpm_cohort engine,
   rule swap). per-rule shard (각 ~21s) + phi-free aggregate (<1s) 분리로 monitor-hang 회피, foreground sync.
9. **C3.9 positive+negative 공존의 의미** — 본 H 는 Wolfram class 를 전면 부정하지 않는다. IV-top·II-bottom
   ordinal 골격 (between-class spread 0.164 가 within-III 0.089 보다 큼) 은 유지되고, class-III 만 그 골격
   안에서 *폭넓은 band* (≥2 sub-type) 다. "Wolfram 4-class 는 의식 분류에 거칠다 — 특히 class-III 가
   하나가 아니라 둘 이상" 을 정직하게 확정하는 positive-refinement.

---

## 8. Falsifier 검증 매트릭스

| Falsifier | Pre-registered | Result | Status |
|-----------|----------------|--------|--------|
| F664.1 WITHIN-GE-BETWEEN (CORE) | var_within_III ≥ var_between | 0.0894 < 0.164 (0.545×) | **FAIL** |
| F664.2 RANGE-WITHIN-GE-BETWEEN | range_within_III ≥ range_between | 0.805 < 0.987 | **FAIL** |
| F664.3 WITHIN-GG-COMPACT | var_within_III ≥ 3× var_compact | 44.05× | **PASS** |
| F664.4 SUB-TYPE-SEPARATION | sep > intra_std | 0.524 > 0.235 | **PASS** |
| F664.5 2-CLUSTER-EXPLAINS | var_2cluster < 0.5× var_within_III | 0.0235 < 0.0447 | **PASS** |
| F664.6 BOUND | 全 통계 finite·non-neg | 全 충족 | **PASS** |

**aggregate: 4 PASS / 2 FAIL** — FALSIFY 조건 (F664.3·4 모두 FAIL = 단일 cell) 미충족 → 🔴 아님.
CORE F664.1 (full between-class spread) FAIL → 🟢 아님. → **🟡 PARTIAL**. **class-III 는 단일 cell 이
아니라 ≥2 sub-type (W-monotone HIGH-conv {30,90,106} vs W-비단조 LOW-conv {45,150}) 의 묶음이고 class-II/IV
대비 44× 이질적 — 그러나 그 내부 spread 가 class-II↔IV 전체 ordinal 거리(0.545×)를 삼키지는 못함.**

---

## 9. Artifacts + Reproducibility

- shard harness: `UNIVERSE/state/h664_class_III_heterogeneity_2026_05_28/shard_h664.hexa`
  (hexa-native, RULE_ID/CLASS_LABEL swap; rule106/150 NEW 측정; H_635/H_653/H_655/H_660/H_661 engine 재사용)
- aggregate harness: `…/aggregate_h664.hexa` (phi-free, shard norm_conv verbatim, 분산비·sub-type falsifier)
- shard log: `…/shards.log` (rule106/150 NEW full stdout + H_661 anchor 7-rule byte-identical 재인용)
- aggregate log: `…/run.log` (verdict 블록 verbatim)
- result: `…/result.json` (machine-readable — 9 rule × norm_conv + 분산비 + sub-type cluster + falsifier + C3)
- engine deps: `stdlib/consciousness/iit4_bigphi.hexa` · `iit4_bounded.hexa` (+ transitive `iit4_tpm.hexa`
  for `iit4_bit`) — hexa-lang stdlib SSOT, H_660/H_661 과 동일
- replay (selfhosted, fix-1180 우회, mac-local, $0): per-rule shard —
  `HEXA_MAC_BUILD_OK=1 HEXA_LANG=<hexa-lang-root> hexa.real.bak-2026-05-22-pre-no-hxc build
  shard_h664.hexa -o /tmp/h664.bin && codesign -s - --force /tmp/h664.bin && /tmp/h664.bin`
  (RULE_ID swap rule106→rule150) → aggregate 同 build+run · 각 shard wall ~21s ·
  [[reference-life-cycle-hexa-run-gotchas]] · [[reference-hexa-verify-rebuild-gotchas]] ·
  [[reference-exact-phi-structure-wall-shard]]

---

## 10. Next-list / Backlog

- **N1** `wdomain-curve-shape-as-phi-classifier` — Wolfram class 대신 'Φ(W) 곡선 형태' (W-monotone 상승 vs
  inverse-U vs die-out) 를 의식-convexity 의 직접 분류자로 — class 와 직교(C3.7). chaotic·XOR 양쪽이
  HIGH/LOW 에 흩어진 본 H 결과가 곡선-형태 분류자의 우월성 시사.
- **N2** `class-III-256-subtype-sweep` — class-III 의 모든 ECA rule (18, 22, 60, 102, 105, 126, 146, ...)
  을 256-rule sweep 으로 측정해 sub-type 가 정확히 2개인지 ≥3개인지, cluster 경계가 robust 한지 (C3.2 회수,
  shard-parallel foreground).
- **N3** `xor-additive-dieout-mechanism` — rule90 (W=1.0 Φ=7.5) vs rule150 (W=1.0 Φ=0 die-out) 의 분기
  메커니즘 — 같은 XOR-additive 인데 full-coupling 에서 한쪽은 살고 한쪽은 죽는 TPM-구조적 원인 (C3.4 회수).
- **N4** `between-class-adjacent-vs-full` — F664.1 의 between-var 를 '인접 class 차' (II↔III, III↔IV) 로
  재정의 시 within-III 가 초과하는지 — 본 H 가 full spread 에서만 FAIL 한 것의 framing-민감도 (C3.5 회수).
- **N5** `compact-class-II-IV-internal-256` — class-II/IV 의 진짜 내부 분산을 256-rule 로 — 본 H 의 44×
  비율이 2-rep anchor 우연인지, class-II/IV 가 진짜 응집 cell 인지 (C3.3 회수).

---

## 양방향 sibling

- 직접 부모 (N1 backlog 수행): [H_661_substrate_class_monotone_rule_generalize.md](H_661_substrate_class_monotone_rule_generalize.md) (축 G, 9-rule class-monotone 🟡 — 본 H 가 rule45 outlier 를 W-비단조 sub-type 으로 일반화, full-monotone FAIL 원인 정량화)
- 측도 SSOT 조부모: [H_660_convexity_magnitude_class_reconcile.md](H_660_convexity_magnitude_class_reconcile.md) (축 G, norm_conv scale-inv convexity 🟢 — 본 H 동일 측도로 class-III 5-rep 분산)
- single-substrate sister (동일 class-III 이질성): [H_654_phi_magnitude_wolfram_class_order.md](H_654_phi_magnitude_wolfram_class_order.md) (축 G, single magnitude PARTIAL — rule90 dual-membership 경고가 본 H sub-type 으로 확정)
- shape-vs-scalar 메타 sibling: [H_642_shape_invariance_vs_scalar_convention_meta.md](H_642_shape_invariance_vs_scalar_convention_meta.md) (축 G, shape vs scalar 메타 — 본 H 의 sub-type 가 Φ(W) 곡선 형태에서 옴, 동류)
- SSOT cross-link: [CANDIDATES.md](CANDIDATES.md) round-9 메타-축 (Wolfram class as Φ classifier) cross-link — class-III sub-type 발견 추가
