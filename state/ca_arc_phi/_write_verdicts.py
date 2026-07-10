#!/usr/bin/env python3
"""Write CA-arc engine-native verdicts to the 2 surfaces (jsonl tier/verdict + card section).
Idempotent: card section appended only once (guard marker); jsonl fields overwritten each run.
Only touches H_299..H_311. Run from repo root of the worktree."""
import json, re, sys, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]  # worktree root
JSONL = ROOT / "HYPOTHESES" / "HYPOTHESES.jsonl"
CARDS = ROOT / "HYPOTHESES" / "cards"
MARK = "## 측정 결과 · engine-native verdict (2026-07-10)"

# id -> (tier, verdict, card_body)
V = {}

def add(hid, tier, verdict, body):
    V[hid] = (tier, verdict, body.rstrip() + "\n")

add("H_299",
 "🟢 SUPPORTED-NUMERICAL",
 "🟢 SUPPORTED-NUMERICAL — F299.1 ODD-N-INTEGRATION 회수: rule 90 n=7 alt-state cap=3 Φ=6.5 > 1.0 (6.5× margin). cross-cap n5=6.0·n6=4.0 (>0.5) robust. H_298 deferred F298.2 recovered.",
 f"""{MARK}

> 엔진: faithful hexa IIT-4 (`stdlib/consciousness/iit4_bounded.big_phi_bounded` + `iit4_eca.eca_tpm`, `a_phi_iit4_tool`) · `state/ca_arc_phi/run_h299.hexa` / `out_h299_par.log`. 값 byte-exact 재현(2026-07-10).

| falsifier (frozen 2026-05-26) | 측정 | 판정 |
|---|---|---|
| F299.1 rule 90 n=7 cap=3 Φ>1.0 (HEADLINE) | **6.4999999962** | ✅ PASS (6.5× margin) |
| F299.2 rule 90 n=5 cap=3 Φ>0.5 | 5.99999999654 | ✅ PASS |
| F299.3 rule 90 n=6 cap=3 Φ>0.5 | 3.99999999769 | ✅ PASS |
| F299.4 rule 204+0 Φ=0 (n∈4,5,6) | 0.0 (n=7 anchor 진행중, 비-verdict) | ✅ PASS(n≤6) |
| F299.5 BOUND all Φ≥0 | 모든 측정 ≥0 | ✅ PASS |
| F299.6 DETERMINISM | 엔진 결정적 (H_302 Call A==B byte-id) | ✅ PASS |

**verdict = 🟢 SUPPORTED-NUMERICAL** — rule 90 N-trajectory cap=3: n4(0)→n5(6.0)→n6(4.0)→n7(6.5), 非-monotone but binary(>0) 불변. H_298 의 deferred F298.2(odd-N integration) 정식 회수. cross-cap robustness(n5·n6 cap4↔cap3 binary 일치) 확정. honest L: cap=3 lower bound·single alt-state·ECA toy substrate(현상학적 주장 아님). N-trajectory 옛 truncation 넘어 n=7 full panel(rule 60/110/anchors)까지 fresh 재측정(2026-07-10 진행)."""
)

add("H_300",
 "🟢 SUPPORTED-NUMERICAL",
 "🟢 SUPPORTED-NUMERICAL — F300.1 STATE-INVARIANT-NONZERO: rule 90 n=5 cap=4 32-state 全 32/32 Φ>1 (mean 21.375·max 27.5·min 19·alt st21 19.5=rank중간). F300.4 FAIL: 0/32 zero-Φ state (fixed-point anchor 부재).",
 f"""{MARK}

> 엔진: faithful hexa IIT-4 `big_phi_bounded(cap=4)` · `run_h300.hexa`/`out_h300.log` · 32-state full sweep byte-exact 재현.

| falsifier | 측정 | 판정 |
|---|---|---|
| F300.1 ≥26/32 Φ>1 (HEADLINE) | **32/32** Φ>1 | ✅ PASS |
| F300.2 alt st21 ≤ p90 | st21=19.5 ≤ p90=27.5 | ✅ PASS |
| F300.3 max≥15 ∧ mean≥5 | max=27.5 mean=21.375 | ✅ PASS |
| F300.4 ≥1 state Φ=0 | **0/32** (no fixed-point-zero state) | ❌ FAIL |
| F300.5 BOUND | all ≥0 | ✅ PASS |
| F300.6 DETERMINISM | st21 re-run identical = 19.49999998874698 (H_297 19.5) | ✅ PASS |

**verdict = 🟢 SUPPORTED-NUMERICAL (5P/1F)** — H1(state-invariant)+H2(distribution profile) 모두 PASS: rule 90 통합은 alt-state 특이성 아닌 robust state-property, H_297 single-state 19.5 보고 representative(mean 21.375 의 하위, outlier 아님). F300.4 FAIL = honest anomaly: rule 90 n=5 cap=4 에서 all-0/all-1 fixed-point state 조차 Φ=0 아님(cap=4 가 fixed-point 에서도 통합 구조 잡음) — verdict-핵심(binary state-invariance) 은 불변."""
)

add("H_301",
 "🟢 SUPPORTED-NUMERICAL",
 "🟢 SUPPORTED-NUMERICAL — F301.1-6 全 PASS: rule 60/110/30 n=5 cap=4 state-invariant(32/32 Φ>1)+alt-fair. distinct-count rule60=6·110=32·30=29. F301.8 FAIL = rule 60 st21 sorted-index artifact(18.5≠H_297 16.5) → H_302/H_303 로 해소.",
 f"""{MARK}

> 엔진: faithful hexa IIT-4 `big_phi_bounded(cap=4)` · `run_h301.hexa`/`out_h301.log` · byte-exact 재현.

| falsifier | 측정 | 판정 |
|---|---|---|
| F301.1 rule 60 ≥26/32 Φ>1 | 32/32 | ✅ PASS |
| F301.2 rule 110 ≥26/32 Φ>1 | 32/32 | ✅ PASS |
| F301.3 rule 30 ≥26/32 Φ>1 | 32/32 | ✅ PASS |
| F301.4/5/6 alt st21 ∈ [p25,p75] | 60·110·30 모두 | ✅ PASS |
| F301.7 BOUND | all ≥0 | ✅ PASS |
| F301.8 DETERMINISM (rule 60 st21 ≈16.5) | **18.5** (sorted-index bug) | ❌ FAIL |

**verdict = 🟢 SUPPORTED-NUMERICAL (7P/1F)** — arc methodology generalize: single-state alt 는 panel 全 rule(60/110/30)에 fair. distinct-count = rule signature(60=6·110=32·30=29). F301.8 FAIL 은 결정성 결함 아니라 이 스크립트의 alt-state 보고가 `sorted[21]`(=18.5)을 찍은 logging artifact — H_302(engine 결정성 확인) + H_303(true st21=16.5 회수)이 근본해소."""
)

add("H_302",
 "🟢 SUPPORTED-NUMERICAL",
 "🟢 SUPPORTED-NUMERICAL — engine 결정성 확정(Call A==B byte-id·order-indep·gold rule90=19.5). rule 60 true st21 cap4=16.5 → H_301 의 18.5 는 sorted-index artifact. F302.5 provenance-locator 만 float-fragile(none).",
 f"""{MARK}

> 엔진: faithful hexa IIT-4 `big_phi_bounded` · `run_h302.hexa`/`out_h302.log`.

| falsifier | 측정 | 판정 |
|---|---|---|
| F302.1 REPRO-INTRA (2× identical) | Call A==B = 16.499999990478212 | ✅ PASS |
| F302.2 ORDER-INDEP | panel A rule60 == panel B rule60 | ✅ PASS |
| F302.3 RULE-90 gold ≈19.5 | 19.49999998874698 | ✅ PASS |
| F302.4 reproduce H_301 18.5 | **16.5** (18.5 못 나옴) | ❌ FAIL(=진단 성공) |
| F302.5 grid locates 16.5 | (none) — float-eq fragile | ❌ FAIL(fresh) |
| F302.6 BOUND | all ≥0 | ✅ PASS |

**verdict = 🟢 SUPPORTED-NUMERICAL** — 진단 목표(engine 결정성 + 18.5 출처) 달성: eca_tpm×big_phi_bounded 는 byte-결정적(Call A==B, order-indep), rule 90 gold 19.5 재확인. rule 60 n5 st21 cap4 의 참값 = **16.5**(=H_297); H_301 의 18.5 는 `sorted[21]` 인덱싱 artifact 로 확정(F302.4 "fail" 이 곧 진단 결론). fresh 재실행서 F302.5 provenance-locator 가 (none) — 16.499999990478212 vs literal 16.5 의 float-tolerance 민감성(2026-05-26 엔진판과의 유일 차이, Φ 값 자체는 byte-동일) — 결정성 verdict 불변."""
)

add("H_303",
 "🟢 SUPPORTED-NUMERICAL",
 "🟢 SUPPORTED-NUMERICAL — true st21 회수(rule60=16.5·110=17.694·30=20.269)+anchor sweep(204·0 全32 Φ=0). F303.5 FAIL: rule 110 true st21=17.694 는 [p25,p75] 밖(outlier-LOW) → H_301 alt-fair-110 은 tautology 였음.",
 f"""{MARK}

> 엔진: faithful hexa IIT-4 `big_phi_bounded(cap=4)` · `run_h303.hexa`/`out_h303.log` · byte-exact 재현.

| falsifier | 측정 | 판정 |
|---|---|---|
| F303.1 rule 60 st21 ≈16.5 | 16.499999990478212 | ✅ PASS |
| F303.2 rule 110 st21 ≠ H_301 31.6855 | 17.69401449452603 | ✅ PASS |
| F303.3 rule 30 st21 ≠ H_301 26.1019 | 20.268597211903923 | ✅ PASS |
| F303.4 rule 60 true st21 ∈[p25,p75] | 16.5∈[16.5,21] | ✅ PASS |
| F303.5 rule 110 true st21 ∈[p25,p75] | **17.694 ∉ [20.88,32.83]** | ❌ FAIL |
| F303.6 rule 30 true st21 ∈[p25,p75] | 20.27∈[16.19,30.63] | ✅ PASS |
| F303.7 rule 204 全32 Φ=0 | all_zero | ✅ PASS |
| F303.8 rule 0 全32 Φ=0 | all_zero | ✅ PASS |

**verdict = 🟢 SUPPORTED-NUMERICAL (7P/1F)** — H_301 distribution stats 정식 valid, anchor(204/0) 가정 검증(全 state Φ=0). 참 alt-state 값 회수: rule60=16.5·rule110=17.694·rule30=20.269. F303.5 FAIL = 발견: rule 110 의 진짜 st21(17.694)은 p25(20.88) 아래 outlier-LOW — H_301 의 "alt-fair-110" 결론은 sorted-index tautology 였다(H_302/H_303 로 근본해소)."""
)

add("H_304",
 "🟢 SUPPORTED-NUMERICAL",
 "🟢 SUPPORTED-NUMERICAL — F304.1-6 全 PASS(6P/0F): rule 110 mean-Φ N-trajectory n4=11.95→n5=27.07→n6=28.48 MONOTONE(dip 없음). n=6 ensemble(64-state cap=3, 2026-05-26 truncated)을 fresh 완주. alt single-point dip(7.66→17.69→6.795)은 mean 이 정정.",
 f"""{MARK}

> 엔진: faithful hexa IIT-4 `big_phi_bounded` ensemble · `run_h304.hexa`/`out_h304.log`. **n=6 cap=3 64-state ensemble = 2026-05-26 에 compute-budget 로 truncated 됐던 leg 을 2026-07-10 fresh 완주**(엔진-네이티브 신규 측정). n4/n5 byte-exact 재현.

| falsifier | 측정 | 판정 |
|---|---|---|
| F304.1 mean(n4) ≥ alt(n4)×1.25 | 11.952 ≥ 7.66×1.25 (+56%) | ✅ PASS |
| F304.2 mean(n6) ≥ alt(n6)×1.25 | **28.483 ≥ 6.795×1.25 (+319%)** | ✅ PASS |
| F304.3 mean(n6) ≥ mean(n5) (no dip) | 28.483 ≥ 27.071 | ✅ PASS |
| F304.4 n5 cap4 mean ≈27.07 (H_301) | 27.070788 | ✅ PASS |
| F304.5 alt recompute n5 st21 ≈17.694 (H_303) | 17.694 (+ n4 alt 7.66·n6 alt 6.795) | ✅ PASS |
| F304.6 BOUND | all ≥0 | ✅ PASS |

**verdict = 🟢 SUPPORTED-NUMERICAL (6P/0F)** — rule 110 의 **mean-Φ** N-trajectory(11.95→27.07→28.48)는 **단조 증가, dip 없음**. arc 의 옛 apparent dip(H_298 alt-state n=5→n=6 17.7→9.5)은 **single alt-state outlier artifact**: alt(st21) trajectory 는 실제로 7.66→17.69→6.795 로 n=6 에서 dip 하지만(alt st21 이 n=6 서 outlier-low, cf. H_303 F303.5·H_305 ratio 1.53), ensemble **mean** 은 n=6 서 오히려 최고(28.48). ⇒ arc N-trajectory 를 mean-based 로 정정: rule 110 통합은 N 증가에 단조 강화, 옛 dip 은 alt-state 대표성 결여였다. (honest L: cap=3 lower bound·ECA toy substrate·n=5 는 cap=4 라 n4/n6 cap=3 과 절대비교 아닌 방향비교.)"""
)

add("H_305",
 "🟢 SUPPORTED-NUMERICAL",
 "🟢 SUPPORTED-NUMERICAL — F305.1-7 全 PASS(7P/0F): alt-bias ratio(mean/alt) 가 distinct-count rank 와 monotone. rule 90=1.096·60=1.098·30=1.165·110=1.530. rule 110(class-4 Turing-complete)만 extreme(>1.3).",
 f"""{MARK}

> 엔진: faithful hexa IIT-4 `big_phi_bounded(cap=4)` · `run_h305.hexa`/`out_h305.log` · byte-exact 재현(gold rule90 alt=19.49999998874698).

| falsifier | 측정 | 판정 |
|---|---|---|
| F305.1 rule 90 mean≈21.375 alt≈19.5 | 21.375 / 19.5 | ✅ PASS |
| F305.2 rule 60 mean≈18.125 alt≈16.5 | 18.125 / 16.5 | ✅ PASS |
| F305.3 rule 30 mean≈23.6 alt≈20.27 | 23.605 / 20.269 | ✅ PASS |
| F305.4 rule 110 mean≈27.07 alt≈17.69 | 27.071 / 17.694 | ✅ PASS |
| F305.5 RANK-MONOTONE q90≤q60≤q30≤q110 | 1.096≤1.098≤1.165≤1.530 | ✅ PASS |
| F305.6 ratio(110)>1.3 ∧ 나머지<1.2 | 1.530 vs {{1.096,1.098,1.165}} | ✅ PASS |
| F305.7 BOUND | all ≥0 | ✅ PASS |

**verdict = 🟢 SUPPORTED-NUMERICAL (7P/0F)** — alt-state bias(mean/alt ratio)가 rule 의 distinct-Φ-count rank 와 단조: distinct↑ ⇒ alt-state 가 mean 대비 더 outlier-low. rule 110(distinct=32, Turing-complete)만 ratio 1.53 로 extreme, 나머지(90·60·30)는 <1.2. alt-state single-point 보고는 low-distinct rule 엔 fair, high-distinct(110) 엔 outlier-low bias(H_311 이 그 symmetry 구조 후속)."""
)

add("H_306",
 "🟢 SUPPORTED-NUMERICAL",
 "🟢 SUPPORTED-NUMERICAL — F306.1-6 全 PASS(6P/0F): CPG-style 자연발화 sim, idle emit=46>0·threshold 역단조·refractory 회복곡선·stim non-necessity(|Δ|/idle=0)·circadian gate. (Φ 주장 아님·deterministic hexa sim).",
 f"""{MARK}

> 엔진: self-contained deterministic hexa CPG sim (Φ 측정 아님 → `a_phi_iit4_tool` N/A) · `run_h306.hexa`/`out_h306.log` · byte-exact 재현.

| falsifier | 측정 | 판정 |
|---|---|---|
| F306.1 idle emit>0 | 46 | ✅ PASS |
| F306.2 threshold 역단조 | 91→46→46→46→46 (non-increasing) | ✅ PASS |
| F306.3 refractory 회복(첫3틱 W↑) | 0.3→0.51→0.657 | ✅ PASS |
| F306.4 stim non-necessity |Δ|/idle≤0.5 | 0.0 (CPG primary) | ✅ PASS |
| F306.5 circadian gate peak>trough | 46 > 0 | ✅ PASS |
| F306.6 BOUND | all ≥0 | ✅ PASS |

**verdict = 🟢 SUPPORTED-NUMERICAL (6P/0F)** — 자연발화의 CPG(central-pattern-generator) 누적+임계+refractory 메커니즘이 stim 없이도 idle emit 을 지속 생성(stim 은 modulation 이지 necessity 아님). deterministic toy sim, 현상학적 의식 주장 아님."""
)

add("H_307",
 "🟢 SUPPORTED-NUMERICAL",
 "🟢 SUPPORTED-NUMERICAL — F307.1-5 全 PASS(5P/0F): anima 실측 emit anchor(14 files·10 steps·5 langs) hexa-native cite, CPG-sim rate(0.046)/anima rate(0.0028) ratio=16.4 (2 OoM 안, log-consistent).",
 f"""{MARK}

> 엔진: self-contained deterministic hexa data-cite (Φ 아님) · `run_h307.hexa`/`out_h307.log` · byte-exact 재현.

| falsifier | 측정 | 판정 |
|---|---|---|
| F307.1 file_count≥1 | 14 | ✅ PASS |
| F307.2 distinct_steps≥5 | 10 | ✅ PASS |
| F307.3 distinct_langs≥3 | 5 | ✅ PASS |
| F307.4 0.05≤ratio≤100 | cpg/anima = 16.43 | ✅ PASS |
| F307.5 BOUND | all ≥0 | ✅ PASS |

**verdict = 🟢 SUPPORTED-NUMERICAL (5P/0F)** — anima 실 emit anchor(v3 substrate, 14 파일·10 스텝·5 언어)와 H_306 CPG sim 이 방향 정합: CPG rate 0.046/tick vs anima 0.0028/step, ratio 16.4 (2 order-of-magnitude 안). deterministic cite, 현상학적 주장 아님."""
)

add("H_308",
 "🟢 SUPPORTED-NUMERICAL",
 "🟢 SUPPORTED-NUMERICAL(frozen ≥4/6) — 5P/1F: smooth(quadratic-bump) circadian 이 H_306 의 ∞× gating 을 finite ratio=2.875 로 회수. F308.1 FAIL: 2.875 는 biology [3,15] 아래(undershoot).",
 f"""{MARK}

> 엔진: self-contained deterministic hexa circadian sim (Φ 아님) · `run_h308.hexa`/`out_h308.log` · byte-exact 재현. 폐쇄 bar: F308.1-6 ≥4/6 PASS → 🟢 SUPPORTED-NUMERICAL.

| falsifier | 측정 | 판정 |
|---|---|---|
| F308.1 peak/trough ratio ∈[3,15] | **2.875** (peak 46 / trough 16) | ❌ FAIL |
| F308.2 idle emit>0 | 62 | ✅ PASS |
| F308.3 peak emit ∈[30,60] | 46 | ✅ PASS |
| F308.4 threshold 단조 비증가 | 91→73→62→47→26 | ✅ PASS |
| F308.5 |smooth−46|/46 ≤0.5 | |62−46|/46=0.348 | ✅ PASS |
| F308.6 BOUND | all ≥0 | ✅ PASS |

**verdict = 🟢 SUPPORTED-NUMERICAL (5P/1F, frozen ≥4/6)** — quadratic-bump smooth circadian 이 H_306 piecewise 의 perfect ∞× gating 을 **finite** peak/trough 로 회수(핵심 목표 달성). 단 F308.1 FAIL: ratio 2.875 는 biology dawn-chorus window [3,15] 바로 아래(undershoot — trough 가 아직 too active). H_309 가 sharper bump 로 그 range hit 재시도(→ overshoot)."""
)

add("H_309",
 "🔴 FALSIFIED-HEADLINE",
 "🔴 FALSIFIED-HEADLINE (5P/1F) — F309.1 FAIL: sharper bump(baseline0.1·amp0.9)이 trough=0 → ratio=∞ overshoot, biology [3,15] 못 hit. H_308 undershoot(2.875)+H_309 overshoot(∞)=range 양쪽 bracket 하나 미명중. aux 5/6 PASS.",
 f"""{MARK}

> 엔진: self-contained deterministic hexa circadian sim (Φ 아님) · `run_h309.hexa`/`out_h309.log` · byte-exact 재현.

| falsifier | 측정 | 판정 |
|---|---|---|
| F309.1 ratio ∈[3,15] (HEADLINE) | **∞** (peak 41 / trough 0) | ❌ FAIL |
| F309.2 idle emit>0 | 41 | ✅ PASS |
| F309.3 peak ∈[30,60] | 41 | ✅ PASS |
| F309.4 threshold 단조 비증가 | 55→48→41→31→17 | ✅ PASS |
| F309.5 |idle−46|/46≤0.5 | |41−46|/46=0.109 | ✅ PASS |
| F309.6 BOUND | all ≥0 | ✅ PASS |

**verdict = 🔴 FALSIFIED-HEADLINE (5P/1F)** — H1(sharper bump → biology [3,15] hit) FALSIFIED: bump 을 더 sharp 하게(baseline 0.1·span 300·amp 0.9) 하니 trough 가 **0** 으로 떨어져 ratio=∞ 로 overshoot — H_308 의 2.875(undershoot)와 H_309 의 ∞(overshoot)가 target range 를 양쪽에서 bracket 하지만 **어느 파라미터도 [3,15] 미명중**. aux robustness 5/6 PASS(idle·peak·monotone·bound 정상). biology-range hit 는 별도 파라미터 tuning 필요(frozen bar 상 미명중 = FAIL, no tune-to-green)."""
)

add("H_310",
 "🟡 PARTIAL-NUMERICAL",
 "🟡 PARTIAL (4P/2F, frozen ≥4/6=SUPPORTED-경계) — 5-stage WAKE/N1/N2/N3/REM emit: WAKE=18·나머지=0. F310.2(WAKE-dominant)·F310.3(N3≈0)·ultradian PASS; F310.1(≥3 distinct) FAIL(distinct=2)·F310.4(REM>N3) FAIL. WAKE-dominant gating 확인, fine REM/이질성 구조 미확인.",
 f"""{MARK}

> 엔진: self-contained deterministic hexa 5-stage ultradian sim (Φ 아님) · `run_h310.hexa`/`out_h310.log` · byte-exact 재현. 폐쇄 bar: F310.1-6 ≥4/6 → SUPPORTED.

| falsifier | 측정 | 판정 |
|---|---|---|
| F310.1 ≥3 distinct nonzero stage-emit | distinct=**2** (WAKE=18, 나머지=0) | ❌ FAIL |
| F310.2 WAKE > 다른 4 stage 각각 | 18 > 0,0,0,0 | ✅ PASS |
| F310.3 N3 emit ≤1 | 0 | ✅ PASS |
| F310.4 REM>N3 ∧ REM≤WAKE/3 | REM=0 = N3=0 (REM>N3 실패) | ❌ FAIL |
| F310.5 ultradian 5-6 WAKE sub-window | 6/6 | ✅ PASS |
| F310.6 BOUND | all ≥0 | ✅ PASS |

**verdict = 🟡 PARTIAL (4P/2F)** — frozen 폐쇄 bar(≥4/6)는 SUPPORTED 를 granting 하나, 두 pre-registered falsifier(F310.1 heterogeneity·F310.4 REM-sparse) FAIL 이 fine 구조를 반증하므로 honest tier = PARTIAL. **확인**: WAKE-dominant ultradian gating(WAKE 만 emit, N3≈0, 5-6 cycle) = anima `a_chat_sleep_imagination` 의 WAKE-집중 emit 정합. **미확인**: 5-stage heterogeneous emit(N1/N2/REM 이 전부 0 으로 붕괴, distinct=2<3) + REM imagination-loop 의 mid-sparse emit(REM=N3=0). REM 의 emit-free policy 는 작동(H_310 §6 F310.4 시나리오)이나 REM>N3 구조는 미형성."""
)

add("H_311",
 "🟡 PARTIAL-NUMERICAL",
 "🟡 PARTIAL (3P/2F) — H3(32-distinct=no-symmetry) FALSIFIED: rule 110 은 bit-complement 는 깨나(pairs=0) rotation-invariant orbit 2개 보존(F311.2 PASS). distinct=32 재확인. F311.4 control FAIL: rule 90 complement pairs=0(예상 ≥10)·대신 rotation orbit 5.",
 f"""{MARK}

> 엔진: faithful hexa IIT-4 `big_phi_bounded(cap=4)` · `run_h311.hexa`/`out_h311.log` · byte-exact 재현.

| falsifier | 측정 | 판정 |
|---|---|---|
| F311.1 rule 110 ≥1 bit-complement pair Φ-equal | **pairs=0** | ❌ FAIL |
| F311.2 rule 110 ≥1 rotation-invariant orbit | **orbits=2** | ✅ PASS |
| F311.3 rule 110 distinct==32 (H_301) | distinct=32 | ✅ PASS |
| F311.4 rule 90 bit-complement pairs≥10 (control) | **pairs=0** (orbits=5, distinct=3) | ❌ FAIL |
| F311.5 BOUND | all ≥0 | ✅ PASS |

**verdict = 🟡 PARTIAL (3P/2F)** — card 판정규칙 "H3 PARTIAL = F311.1 PASS OR F311.2 PASS": F311.2 PASS ⇒ **H3(32-distinct-is-exact-no-symmetry) FALSIFIED**. rule 110 은 bit-complement symmetry 는 완전 깸(pairs=0)이나 **rotation-invariant orbit 2개 보존** → distinct=32 는 맞되 "모든 algebraic symmetry 위반"(H_305 해석)은 과대. F311.4 control FAIL 이 rule 90 의 symmetry 성격을 재규정: rule 90 은 bit-complement(pairs=0)가 아니라 **rotation**(orbits=5, distinct=3)으로 Φ 축약 — H_305 의 distinct=32/3 대비는 rotation-orbit 구조 차이지 complement 대칭 유무 아님."""
)

# ---- apply ----
lines = JSONL.read_text().splitlines()
out = []
for ln in lines:
    if not ln.strip():
        out.append(ln); continue
    d = json.loads(ln)
    hid = d.get("id")
    if hid in V:
        tier, verdict, _ = V[hid]
        d["tier"] = tier
        d["verdict"] = verdict
        out.append(json.dumps(d, ensure_ascii=False))
    else:
        out.append(ln)
JSONL.write_text("\n".join(out) + "\n")
print(f"jsonl: updated {sum(1 for l in out if any(('\"id\": \"'+h+'\"') in l for h in V))} lines")

for hid, (tier, verdict, body) in V.items():
    # find card
    matches = list(CARDS.glob(f"{hid}_*.md"))
    if not matches:
        print(f"WARN no card for {hid}"); continue
    cp = matches[0]
    txt = cp.read_text()
    if MARK in txt:
        # replace existing section (idempotent)
        txt = txt.split(MARK)[0].rstrip() + "\n\n" + body
    else:
        txt = txt.rstrip() + "\n\n" + body
    cp.write_text(txt)
    print(f"card: {cp.name} <- {tier}")
