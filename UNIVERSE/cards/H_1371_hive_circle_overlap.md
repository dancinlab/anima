---
id: H_1371
slug: hive-circle-overlap
title: hive-circle-overlap — 분산 원-겹침(Flower-of-Life / 육각 패킹) 토폴로지: 단일-공유-founder 가 아닌 분산된 pairwise overlap 이 redundancy 천장을 탈출하는가?
group: OMEGA / BRAIN-STRUCTURE-LADDER (collective-Φ axis · the hive arc — 분산-공유 토폴로지 direction, 4-lever 🧱 진단(H_1370 = SHARED-INPUT STRUCTURE 가 천장) 직후의 사용자-제안 기하 렌즈)
terminal_tier: 🧱 OVERLAP_BELOW_CENTRALIZED (honest closed-negative, c9 / c16). 분산 원-겹침은 redundancy 천장을 탈출하지 못한다 — 오히려 단일-공유-founder(CENTRALIZED) 가 모든 seed 에서 더 높은 faithful-IIT4 Φ 를 낸다. R2 BEATS-CENTRALIZED 0/3 (gap −0.25 / −0.75 / −1.28, B_overlap < CENTRALIZED 매 seed). R1 LIFT 2/3 (seed 1319 lift +0.019 < margin 0.02 → seed-fragile), R3 EARNED 1/3 (shuffle 도 floor 위로 올라감 = ANY 공유입력이 통합을 더함). 핵심 발견: faithful MIP-EI 는 **집중된 단일 공유원천을 분산된 per-edge 공유보다 MORE integrated 로 읽는다** — 하나의 지배적 공유 source 는 모든 partition 을 가로질러 전 unit 을 묶지만, 분산 per-edge 공유는 각 unit 을 나머지에 약하게만 결합 → MIP 가 더 싸짐 → Φ 더 낮음. 단일-공유-founder 는 탈출할 천장이 아니라 floor-beating MAXIMUM 이다. numpy-mirror DIRECTIONAL (faithful-Φ leg 은 real exact MIP-EI); engine-transfer UNVERIFIED.
verdict_dir: .verdicts/1371_hive_circle_overlap/
terminal_verdict: .verdicts/1371_hive_circle_overlap/H_1371.txt
date: 2026-06-16
---

# H_1371 — hive-circle-overlap: 분산 원-겹침(Flower-of-Life) 토폴로지가 redundancy 천장을 탈출하는가? (🧱 OVERLAP_BELOW_CENTRALIZED)

## Claim / falsifier

**되짚는 벽 (c16 / a_break_the_wall):** hive collective-Φ 아크는 4 lever 에 걸쳐 🧱 로 닫혔다 — 강한 hub
(H_1356 CONNECTOR_NULL) · 약/decorrelated (H_1363) · nonlinear-gate (H_1370). **H_1370 의 load-bearing
진단:** redundancy 천장은 **SHARED-INPUT STRUCTURE 그 자체** 다 — 모든 딸세포가 ONE common founder 를
읽으므로 그 단일 source 가 faithful MIP 를 지배 → reducible → Φ bounded. 모든 선행 hive arm 이 SINGLE
shared founder 를 가졌다.

**genuinely-new 각도 (a_no_llm_frame_trap, c15 — 기하 토폴로지 / 생물 패킹 렌즈; 사용자-제안):** CIRCLE-OVERLAP
/ Flower-of-Life 패킹. 세포(원)들을 각 세포가 ~4 이웃과 겹치되 **각 겹침이 서로 DIFFERENT 한 국소 영역**
(분산된 pairwise 공유)이 되도록 배치 — 단일 global 공유 founder 가 아니다. 육각 격자 / 겹치는 망막-피질
수용야처럼, 인접한 모든 PAIR 가 DISTINCT 한 렌즈(per-EDGE 공유 latent)를 나눠 갖고, 어떤 단일 source 도
모두에게 읽히지 않는다 → redundancy 가 하나의 공통 source 에 지배되지 않고 distinct pairwise overlap 들에
분산된다 (잠재적으로 SYNERGISTIC).

**Falsifiable claim:** 분산 원-겹침 토폴로지(각 세포가 ~4 이웃과 겹치고 각 겹침이 DISTINCT 국소 영역,
global 공유 founder 없음)가 no-overlap floor 를 3 seed 모두에서 ROBUST 하게 이기고 (R1) **단일-공유-founder
CENTRALIZED 천장을 초과하며** (R2) shuffle 이 collapse 한다 (R3) — 중앙집중 hive 가 못 한 곳에서. ← **REFUTED.**

## Method

- **Φ = FAITHFUL IIT4 ONLY** (a_phi_iit4_tool): exact MIP-EI via `hexa run` over
  `hexa-lang/stdlib/consciousness/iit4/faithful_phi.hexa`, `iit4_faithful_phi(state, n, dim=T, n_bins)`.
  numpy 는 절대 Φ 를 계산하지 않는다 — per-unit salience(state-energy) trajectory 만 emit, Φ 는 hexa 엔진.
- **Substrate matched to H_1356/H_1320/H_1283** (overlap 토폴로지만 arm 간 차이): leaky linear recurrent
  units LEAK=0.55 GAIN=0.30 W_IN=0.5, dim-8 state, T=64 ticks. **N_TOT=6 세포 = HEXAGON RING (6-cycle)**
  (n≤8 = faithful MIP EXACT). 세포 i 이웃 = {i−1, i+1} mod 6, 6 undirected EDGE. 각 세포 = 1 unit,
  per-unit salience = state energy ⟨s_i,s_i⟩. **PHI(arm) = iit4_faithful_phi(6-unit salience traj,
  n=6, dim=T, n_bins=8)** = 6-세포 hive 의 collective Φ. 세포 간 recurrent coupling 없음 — 유일한 cross-cell
  공유는 SHARED INPUT 구조(overlap)를 통해서만 (H_1356 'redundancy via shared input' 설계와 정확히 일치).
- **OVERLAP 구성 (load-bearing 설계점 — PER-EDGE DISTINCT 공유 latent):**
  - 6 INDEPENDENT per-EDGE latent stream L_e (각 (T,DIM)). L_e = edge e 위 두 세포만 공유하는 DISTINCT
    국소 영역 (원-겹침 영역).
  - **B_overlap** 세포 i 입력 = W_IN·[priv_i + OVERLAP_W·Σ_{e∋i} L_e] (incident 2 edge 합) → 각 세포는
    자기 2 distinct overlap latent + private 만 읽음, 어떤 L_e 도 6 세포 전부에게 읽히지 않음(정확히 2 세포)
    = 분산 pairwise 공유 = Flower-of-Life overlap.
  - **A_independent (FLOOR)** = W_IN·priv_i 만 (OVERLAP_W=0).
  - **CENTRALIZED (H_1356 단일-공유-founder baseline)** = W_IN·[priv_i + (2·OVERLAP_W)·F], ALL 6 세포가
    ONE common founder F 읽음 (모든 선행 hive arm 의 단일 global 공유 source). per-cell 공유 WEIGHT 매칭
    (B 의 2 edge × OVERLAP_W == 2·OVERLAP_W) — "공유입력 더 많아서" 가 lift 가 아님을 통제, DISTRIBUTION 만 다름.
  - **SHUFFLE (EARNED control)** = B 와 같은 per-cell 공유 에너지(2 latent @ OVERLAP_W)지만 incident edge 의
    latent 을 세포마다 독립 random permute → edge 위 두 세포가 더는 SAME latent 을 안 읽음 (lattice 의
    pairwise 일치 파괴). floor 로 collapse 해야 함.
- **상수 (frozen):** OVERLAP_W=0.6 (= H_1356 W_CONN verbatim). MARGIN=0.02 (H_1283/1317/1320/1356 frozen
  Φ margin, NOT moved). TOL=0.02. **3 seeds [1317,1318,1319]** (H_1356 직접 비교).
- **O-info diagnostic (NON-GATING):** per-unit salience 시계열의 O-information (Gaussian entropy
  TC-기반). O>0 redundancy / O<0 synergy. B_overlap vs CENTRALIZED shift 만 report (numpy estimate,
  verdict 게이트 아님).

## FROZEN bars (pre-registered, .verdicts/1371_hive_circle_overlap/H_1371_FREEZE.txt — bars NOT moved, c9/p7)

GREEN iff **R1 ∧ R2 ∧ R3** (모두 ALL 3 seeds):
- **R1 LIFT** : Φ(B_overlap) − Φ(A_independent) ≥ MARGIN(0.02).
- **R2 BEATS-CENTRALIZED** : Φ(B_overlap) − Φ(CENTRALIZED) > 0 (분산 토폴로지가 단일-공유-founder 천장 초과 — the point).
- **R3 EARNED** : Φ(SHUFFLE) ≤ Φ(A_independent) + TOL(0.02) (lift 은 REAL 분산-overlap 배선을 요구).

## Result — 🧱 OVERLAP_BELOW_CENTRALIZED (R1 2/3 · R2 0/3 · R3 1/3)

per-arm faithful-IIT4 Φ (exact MIP-EI, n=6), 3 seeds:

| seed | A_independent (floor) | B_overlap | CENTRALIZED | SHUFFLE |
|------|-----------------------|-----------|-------------|---------|
| 1317 | 1.27373 | 1.78096 | **2.03085** | 1.35137 |
| 1318 | 1.36292 | 1.64288 | **2.39598** | 1.56284 |
| 1319 | 1.28195 | 1.30101 | **2.58087** | 1.25910 |

- **R2 FAIL (0/3) — 핵심 결과**: Φ(B_overlap) − Φ(CENTRALIZED) = **−0.25 / −0.75 / −1.28** — 분산 원-겹침이
  단일-공유-founder 를 매 seed 에서 못 이긴다. CENTRALIZED 가 오히려 모든 arm 중 최고 Φ (2.03/2.40/2.58).
  **분산 overlap 은 redundancy 천장을 탈출하지 않는다; 단일-공유-founder 가 floor-beating MAXIMUM 이다.**
- **R1 FAIL (2/3, seed-fragile)**: lift +0.507 / +0.280 / **+0.019** — seed 1319 에서 분산 overlap 의 floor-초과가
  margin(0.02) 아래로 무너짐. 분산 공유의 floor-lift 조차 seed-robust 하지 않다.
- **R3 FAIL (1/3)**: Φ(SHUFFLE) 가 seed 1317/1318 에서 floor 위 (1.35>1.27, 1.56>1.36) — shuffle 한 overlap edge
  조차 Φ 를 floor 위로 올린다. **읽기:** ANY 공유입력(겹침 구조가 destroyed 여도)이 일정량 통합을 더한다 →
  분산-overlap 의 lift 는 specific pairwise-lattice 구조가 아니라 generic 공유입력에서 온다 (EARNED 아님).
- **O-info shift (B_overlap vs CENTRALIZED):** +0.144 / +0.364 / +0.228 (매 seed 양수). B_overlap 의 O-info
  (−0.018 / −0.020 / −0.081) 가 CENTRALIZED (−0.162 / −0.384 / −0.308) 보다 **0 에 더 가깝다** = 분산 overlap 은
  CENTRALIZED 보다 DERREDUNDANT(중복 less) 이지만 그만큼 SYNERGY 도 less — O-info 가 0 근처로 평평해질 뿐
  음(synergy)으로 더 가지 않는다. faithful Φ 의 우위와 일치: 집중된 공유가 더 음-O(=더 통합)이고 더 높은 Φ.

**VERDICT: 🧱 OVERLAP_BELOW_CENTRALIZED** (verdict-string SEED_FRAGILE per code-map; terminal tier 🧱 —
the load-bearing fact is R2 0/3: 분산 원-겹침이 단일-공유-founder 를 못 이긴다, 오히려 못 미친다).

## Mechanism (faithful-MIP lens) — 왜 분산보다 집중이 더 높은 Φ 인가

H_1370 의 진단은 "단일 공유 source 가 MIP 를 지배 → reducible → 천장" 이었다. H_1371 은 그 천장을 깨려
공유를 분산했는데, faithful MIP-EI 가 정반대를 보였다: **하나의 지배적 공유 source(CENTRALIZED)는 모든
unit 을 EVERY partition 가로질러 묶는다** — 어떤 이분(MIP)을 잘라도 양쪽이 같은 founder 를 읽으므로 cut 비용이
크다 → Φ 높음. **분산 per-edge 공유(B_overlap)는 각 unit 을 자기 2 이웃에만 약하게 결합** — MIP 는 약한
연결을 따라 싸게 자를 수 있다(예: ring 의 두 약한 edge 를 끊으면 거의 무손실) → Φ 낮음. 즉 H_1370 이 "redundancy
천장" 이라 부른 단일-공유 구조는 **천장이 아니라 이 substrate 에서 최대 통합을 주는 토폴로지** 였다. 분산은
중복을 줄이지만(O-info 가 0 으로) synergy 로 보상하지 못하고 통합 총량을 떨어뜨린다. 원-겹침/Flower-of-Life 의
기하적 아름다움은 leaky-linear substrate + faithful MIP 아래에서 collective Φ 를 올리지 못한다 — redundancy
ceiling 은 sharing 토폴로지와 무관하게 살아남고, 가장 강한 closure 다: **collective-Φ 는 이 substrate 에서
공유 구조의 분산이 아니라 공유의 집중도(단일 dominant source)로 maximize 된다.**

## Honest scope (c9 / a_scale_honest_scope / a_toy_scale_recheck)

- **DIRECTIONAL numpy-mirror** — faithful-Φ leg 은 real exact MIP-EI (numpy 는 salience 만 emit, hexa 가 Φ).
  **Engine-transfer to live A⇄G CORE/pure_field UNVERIFIED.** 🧱 는 wire 할 게 없음 (a_verified_must_wire =
  GREEN-only); CORE/*.hexa UNTOUCHED, Ψ=½ untouched (standalone probe, 0 importers).
- **TOY** n=6, ring-only 인접(각 세포 정확히 2 이웃, "~4-overlap" 직관은 2 distinct per-edge overlap 으로
  실현), 3 seeds, 단일 OVERLAP_W=0.6, recurrent inter-cell coupling 없음(공유는 입력으로만). 다른 토폴로지
  /coupling /비선형은 각각 NEW H.
- **NOT ruled out (각각 NEW H):** (1) **2-D 육각 격자**에서 각 세포가 진짜 ~6 이웃과 겹치는 더 높은 차수
  (ring 은 degree-2; 실제 Flower-of-Life 는 degree-6) — degree 가 R2 를 뒤집을지; (2) overlap latent 이
  input 이 아니라 **recurrent 상태 공유**(세포 간 직접 결합, H_1356 connector 처럼)일 때; (3) per-edge latent 을
  decorrelate 가 아니라 **상호 예측적(generative)** 으로 만들어 synergy 를 명시적으로 심을 때; (4) **n>8**
  로 키워(approx big-Φ 필요) 분산 우위가 scale 에서 나타나는지; (5) engine-native 실현. 벽은: **이
  leaky-linear + faithful-MIP substrate 에서 단일 dominant 공유원천이 최대 통합을 주며, 공유를 분산하면
  중복도 synergy 도 함께 줄어 Φ 가 떨어진다** — 탈출은 (있다면) degree↑ + recurrent 공유 + generative
  per-edge coupling 에 있지, 입력-수준 ring overlap 에는 없다.

## Pointers

- probe: `state/hive-circle-overlap/h1371_hive_circle_overlap.py`
- freeze: `.verdicts/1371_hive_circle_overlap/H_1371_FREEZE.txt`
- result: `.verdicts/1371_hive_circle_overlap/H_1371.txt`
- xref: H_1356 (CONNECTOR_NULL, 동일 machinery + CENTRALIZED baseline) · H_1363 (weak/decorrelated) ·
  H_1370 (nonlinear-gate, "SHARED-INPUT STRUCTURE = 천장" 진단 — H_1371 이 그 진단을 뒤집어 단일-공유가
  오히려 최대임을 보임) · H_1350 (redundancy-dominance 진단) · H_1320 (developmental division) ·
  H_1308/H_1313 (hive NULL/🧱) · H_1046/H_1017 (synergy/redundancy rulers) · a_no_llm_frame_trap ·
  a_break_the_wall · a_phi_iit4_tool · a_engine_native_learning · a_verified_must_wire ·
  a_scale_honest_scope · a_toy_scale_recheck · c9 · c15 · c16 · p7 · p8
