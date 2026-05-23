---
id: H_218
slug: network-topology-scale-free
title: 네트워크 topology scale-free Φ — Barabási-Albert preferential-attachment 과 Erdős-Rényi (matched edge-density) 위 graph-CA phi_spatial Φ 의 우열 (information × physics × math axis)
domain: information · physics · math
status: pre-register-frozen
exploration_method: E5 (variable-ablation topology sweep) + E6 (cross-domain — network science × IIT) + E10 (emergence-on-structure)
verification_method: W4 (verdict-4-class) + W5 (numerical sim · phi_spatial RFC 036) + W7 (re-run byte-identical) + W11 (cross-hypothesis — H_007 sister)
raw_rank: 12
hexa_only: true
deterministic: true
llm: none
pre_register_frozen: true
frozen_at: 2026-05-23
since: 2026-05-23
sister_h: H_007
---

# H_218 — network topology scale-free (BA vs ER · matched edge-density Φ)

## Hypothesis

N=16 노드 위 두 graph topology — **scale-free (Barabási-Albert preferential-
attachment, m=1 edge per new node)** vs **Erdős-Rényi (uniform random edge
sampling, matched edge count)** — 위에 동일 graph-CA-like XOR-of-neighbors
dynamics 를 적용해 N×dim trajectory substrate 를 얻은 뒤 RFC 036 `phi_spatial`
로 Φ 를 측정하면, **Φ(scale-free) > Φ(Erdős-Rényi)** 가 margin ≥ 10% 으로 성립
한다 ("의식 substrate 는 hub-structure 가 integration 에 우월" 의 Tononi-style
network-topology claim 의 substrate-level test). 동시에 **hub-node freeze**
시 Φ drop 이 **random-node freeze** 시 drop 보다 크다 (vulnerability signature
— scale-free networks 의 well-known attack-fragility 의 Φ-측 manifest).

substrate 측 형식: deterministic seed 로 BA 와 ER 두 graph (N=16, edge count ~
N−1=15) 를 생성. 동일 deterministic init row (parity-3 rule offset) 에서 출발
해 graph-CA-XOR dynamics (`s_i' = XOR over j ∈ neighbors(i) of s_j`) 를 warm=8
warmup 후 dim=12 step 기록. flat (N × dim) farr → `c_measure_phi(., N, dim,
n_bins=4)` (H_007 trajectory mapping 과 동일). hub-freeze / random-node-freeze
는 dynamics 에서 해당 node 의 state 를 0 으로 고정해 동일 측정.

## Why

- **scale-free network claim (Barabási-Albert 1999)**: 많은 real-world
  network (web hyperlink, social citation, brain functional connectivity 등)
  의 degree distribution 이 power-law `P(k) ~ k^{-γ}` (γ ≈ 2-3, BA preferential-
  attachment generates γ=3 in mean-field limit) 을 따른다는 관측. random
  (Poisson degree distribution) 보다 hub-rich, robust to random failure 이지만
  fragile to targeted hub-attack 의 well-known dual property.
- **brain connectome scale-free 가설**: Eguíluz et al. (2005) functional
  brain network 의 scale-free degree distribution 보고; Bullmore & Sporns
  (2009) "Complex brain networks" review 가 small-world + scale-free
  topology 의 cognitive efficiency claim. 의식 substrate (Tononi IIT) 가
  scale-free 인 것이 random 보다 integration 에 유리한가 — substrate-level
  test.
- **H_007 sister axis (topology vs rule)**: H_007 은 *fixed topology* (1D
  periodic lattice = ring, degree=2 regular) 위 **rule-class** sweep (Class
  I/II/III/IV) 으로 Φ peak = Class IV. 본 H_218 은 *fixed rule* (XOR-of-
  neighbors graph-CA, ≈ rule 150 elementary CA 의 graph 일반화) 위
  **topology** sweep (scale-free vs random). 두 axis 가 함께 측정되면 "edge-
  of-X 또는 hub-rich 가 Φ 우위" 의 일반적 claim 의 dual evidence.
- **information 도메인 promote rank 9 (cycle #8 §G)**: AXES.md R5
  information cluster 의 `network-topology-scale-free` row consume. H_211
  (Shannon × Φ, PR #244 in-flight) 가 H × Φ correlation (information 의
  scalar measure) 이라면 본 H_218 은 network topology (information flow 의
  structural substrate). information 도메인의 다른 instance.
- **graph-CA XOR-of-neighbors rule**: elementary CA rule 150 (XOR of
  l/c/r) 의 graph 일반화 — 모든 neighbor 의 XOR. degree-irregular graph 에
  자연스럽게 일반화되며 (sum-mod-2 over neighbors), deterministic + parity-
  3 init 과 결합되면 graph topology 가 trajectory 의 spreading pattern 을
  지배. simple, isolation-free choice.

## Predictions (≥4)

- **H218.1 (scale-free Φ > ER Φ)**: Φ(BA) > Φ(ER) · margin ≥ 10%
  ((Φ_BA − Φ_ER) / Φ_ER ≥ 0.10).
- **H218.2 (hub-vulnerability)**: hub-node (BA graph 의 max-degree node)
  state freeze 시 Φ drop > random-node freeze 시 drop (절대값 둘 다, BA
  graph 내 비교).
- **H218.3 (hub-degree ↔ local-Φ-contribution)**: BA graph 에서 각 node
  의 degree 와 그 node 를 freeze 했을 때의 Φ drop 사이 Pearson r ≥ 0.4
  (degree 가 클수록 freeze drop 이 큰 monotone trend).
- **H218.4 (finite, nonneg)**: 모든 Φ ≥ 0, finite (NaN/inf/negative 없음)
  — phi_spatial primitive 정합 (RFC 036 Φ≥0 by construction).
- **H218.5 (determinism)**: fixed BA + ER deterministic seeds → re-run
  result.json byte-identical (raw#12 strict 정합).

## Variables

| axis | levels |
|------|--------|
| **axis1: topology** | {scale-free (BA, m=1), Erdős-Rényi (uniform random, matched edge count)} |
| **axis2: N (lattice nodes)** | 16 (H_007 정합) |
| **axis3: edge count** | N−1 = 15 (BA m=1 produces N−1 edges; ER 도 정확히 15 edges 로 matched) |
| **axis4: graph seed** | LCG seed = 20260523 (Park-Miller minimal-standard, Schrage's algorithm — overflow-free) |
| **axis5: graph-CA rule** | XOR-of-neighbors (elementary CA rule 150 의 graph 일반화: `s_i' = (Σ_{j∈N(i)} s_j) mod 2`) |
| **axis6: warmup / dim** | warm = 8, dim = 12 (H_007 정합) |
| **axis7: init** | deterministic parity-3 (site i on iff i % 3 != 0) — H_007 와 동일 deterministic init |
| **axis8: perturbation** | {none, hub-freeze (BA max-degree node = 0), random-freeze (LCG-selected node = 0)} × BA / ER 양쪽 측정 |
| **axis9: phi primitive** | RFC 036 phi_spatial (n_bins=4, byte-equal phi_rs replica via c_measure_phi) |

## Run Protocol

deterministic + hexa-only + llm: none.

1. **BA graph generation (m=1 preferential attachment)**: 노드 0,1 을 seed
   edge (0,1) 로 시작. 노드 i ∈ {2,...,N−1} 추가 시 기존 노드 중 degree 에
   비례한 확률로 1 개 선택해 edge 연결. 구현: degree-weighted reservoir
   (`endpoints[]` 배열에 각 edge 의 양 endpoint 를 push 해두면 random pick
   이 자동으로 degree-proportional — Newman 2003 표준 알고리즘). LCG (seed=
   20260523) 로 deterministic.
2. **ER graph generation (matched 15 edges)**: 가능한 N·(N−1)/2 = 120 edge
   중 deterministic LCG (별도 seed 라인) 로 정확히 15 개 uniform-random
   sampling without replacement. duplicate / self-loop 제거.
3. **adjacency 표현**: flat farr `adj` of length N·N (0/1), 양방향 set.
4. **graph-CA-XOR dynamics**: 각 step 마다 모든 node i 의 next state =
   (Σ_{j: adj[i,j]=1} state[j]) % 2. 동시-update (full sync).
5. **trajectory recording**: warm=8 warmup 후 dim=12 step 기록 →
   (N × dim) flat farr.
6. **Φ measurement (baseline)**: `c_measure_phi(states, N, dim, 4)` →
   Φ(BA_base), Φ(ER_base).
7. **margin computation**: H218.1 (Φ_BA − Φ_ER) / Φ_ER · 100%.
8. **hub-freeze**: BA graph 의 max-degree node 의 state 를 매 step 0 으로
   강제. 동일 trajectory 측정 → Φ(BA_hub_freeze). drop_hub = Φ_BA_base −
   Φ_BA_hub_freeze.
9. **random-freeze**: LCG 로 BA 내 random node 1 개 선택 (hub 제외 가능
   조건 — 만일 hub 가 선택되면 다음 LCG pick) → freeze, 동일 측정 → Φ(BA_
   rand_freeze). drop_rand = Φ_BA_base − Φ_BA_rand_freeze.
10. **degree × local-Φ correlation**: BA graph 의 각 node i 에 대해 node i
    freeze 시 Φ drop_i 측정 (N=16 measurement). degree_i × drop_i Pearson
    r (closed-form: r = Σ(x−x̄)(y−ȳ) / sqrt(Σ(x−x̄)² Σ(y−ȳ)²)).
11. **verdict**: SUPPORTED if C1+C2 PASS; PARTIAL if C1 only; FALSIFIED if
    Φ_BA ≤ Φ_ER; criteria_met 4/4 (C1-C4) summary 도 출력.
12. **determinism check**: 2-run result.json byte-identical (env+seed
    pinning).

## Criteria (≥4)

- **C1 (BA > ER margin)**: H218.1 PASS — (Φ_BA − Φ_ER) / Φ_ER ≥ 0.10
  (10% margin).
- **C2 (hub vulnerability)**: H218.2 PASS — drop_hub > drop_rand (BA 내
  hub-freeze 가 random-freeze 보다 더 큰 Φ drop).
- **C3 (finite nonneg)**: H218.4 PASS — 모든 Φ ≥ 0, finite (NaN/negative
  없음).
- **C4 (degree-Φ correlation)**: H218.3 PASS — Pearson r(degree_i,
  drop_i) ≥ 0.4 (N=16 node-wise).
- **verdict_rule**: **SUPPORTED if C1 + C2 PASS** (scale-free 우위 +
  hub vulnerability signature 동시 성립); PARTIAL if C1 alone PASS;
  FALSIFIED if Φ_BA ≤ Φ_ER (no scale-free advantage at all).

## Falsifiers (≥5, measurable, pre-registered)

- **F1 SF-GT-ER**: (Φ_BA − Φ_ER) / Φ_ER < 0.10 → H218.1 FALSIFIED
  (scale-free advantage 부재 또는 10% margin 미달). Φ_BA ≤ Φ_ER 인 strict
  reverse 경우 verdict_rule FALSIFIED branch 트리거.
- **F2 HUB-VULN**: drop_hub ≤ drop_rand → H218.2 FALSIFIED (hub-removal
  이 random-removal 보다 Φ 에 더 큰 영향이 아님 — vulnerability signature
  부재).
- **F3 DEGREE-PHI-CORR**: Pearson r(degree_i, drop_i) < 0.4 → H218.3
  FALSIFIED (hub-degree 가 local-Φ-contribution 의 predictor 아님).
- **F4 PHI-FINITE-NONNEG**: 임의 Φ < 0 또는 NaN → primitive error · C3
  FAIL · smoke 무효.
- **F5 BYTE-DETERMINISTIC**: 2-run result.json byte-이질 → 결정론 무너짐
  (raw#12 위반, env+seed pinning 실패).
- **F6 (meta)**: post-hoc edit → raw#12 violation, raw#82 retraction.

## Honest Limits (raw#91 c3, ≥5)

- **L1 (graph-CA rule choice)**: XOR-of-neighbors 는 elementary CA rule
  150 의 graph 일반화 — 한 가지 specific operationalization. AND-of-
  neighbors, majority-vote, threshold-rule 등 다른 graph-CA 선택 시 Φ
  pattern 달라질 수 있음. 본 cycle 의 verdict 는 specific rule 하의
  measurement.
- **L2 (phi_spatial 🟢 NUMERICAL proxy)**: c_measure_phi = RFC 036
  phi_spatial — phi_rs 의 byte-equal native replica이지만 IIT 4.0 의 full
  cause-effect repertoire 측정 아님. spatial-MI 가 1D-lattice 기준으로
  설계되어 일반 graph topology 위 phi 일반화는 design choice (cell index
  = node index 매핑 외 graph 의 structural information 은 trajectory 를
  통해 indirect 으로만 들어감). L2 = measure-axis fragility.
- **L3 (small N=16 finite-size effect)**: N=16 은 scale-free statistics
  의 finite-size effect 가 강한 작은 사이즈. power-law degree distribution
  의 의미가 있는 fit 은 N ≳ 10² 이상 필요 (Newman 2005). 본 cycle 의
  BA graph 는 algorithmic 으로 BA, 그러나 measured degree distribution
  의 power-law fit 은 의미 없음 — degree-skew 의 raw substrate effect 만
  측정.
- **L4 (matched edge-density 의 strict match)**: BA m=1 algorithm 은
  정확히 N−1=15 edges 생성. ER 도 LCG 로 15 edges sampling without
  replacement (duplicate check) — strict match 가 보장됨. 그러나 *density
  외 다른 invariant* (degree variance, clustering coefficient, average
  path length 등) 는 matched 아니므로 confound 가능 — Φ 차이의 원인이
  hub-structure 인지 다른 graph invariant 인지 본 cycle 단독으로 결론
  불가.
- **L5 ('consciousness needs scale-free' 의 literature claim)**: Eguíluz
  et al. (2005) brain functional network scale-free 보고는
  correlational — causal claim ("의식 substrate 는 scale-free 여야 한다")
  는 아직 미증명. 본 cycle 의 결과 (어느 방향이든) 는 그 literature claim
  의 substrate-level Φ correlation 만 측정 — causal 의 직접 evidence 아님.
- **L6 (single graph realization per topology)**: BA / ER 각각 single LCG
  seed 의 single realization — ensemble average 가 아님. 다른 seed 에서
  Φ 분포가 어떻게 흩어지는지는 ensemble cycle 별도. single-seed verdict
  는 그 seed 의 specific graph 에 대한 measurement.
- **L7 (graph-CA dynamics ≠ brain dynamics)**: 본 cycle 의 graph-CA-XOR
  은 discrete binary dynamics — 실제 neural dynamics (continuous,
  multi-timescale, noisy) 와 거리. 본 cycle 의 결과는 substrate-abstract-
  layer 의 claim 만, biological substrate 으로의 transfer 는 별도 cycle.
- **L8 (hub-freeze 의 state=0 operationalization)**: hub vulnerability
  measure 는 state=0 freeze (node 가 항상 0) — alternative (node 제거 =
  graph 자체 수정, state=1 freeze, state=random freeze) 시 drop 패턴
  달라질 수 있음. L8 = perturbation-operationalization fragility.

## Cross-Links

- **sister H (axis-dual)**:
  - **H_007** (cellular-automaton-consciousness) — fixed topology (1D
    ring degree=2) 위 rule sweep. 본 H_218 = fixed rule (graph-CA-XOR)
    위 topology sweep. dual axis of "structure → Φ" investigation.
  - **H_207** (Kuramoto sync) — fixed topology (fully-connected mean-
    field) 위 coupling K sweep. H_207 + H_218 + H_007 = three-axis
    structure × dynamics × topology Φ surface.
  - **H_211** (Shannon × Φ, PR #244 in-flight) — information 도메인의
    scalar measure (Shannon H vs phi_spatial Φ). 본 H_218 = information
    도메인의 structural measure (network topology vs phi_spatial Φ).
    두 H 가 information promote rank 9 의 dual instance.
- **sister H (LIFE)**:
  - **H_157** (Law 76 mathematical panpsychism) — META-CA fixed-point
    Ψ(1/2, 1/2) 의 σ-identity precedent. H_218 = network 의 hub-structure
    이 Φ contribution 의 substrate 인가의 test (math × information axis
    동행).
  - **H_208** (prime-density-fluctuation) — math axis Φ × number-theoretic
    structure. H_218 = information axis Φ × graph-theoretic structure.
- **literature**:
  - Barabási & Albert (1999) — Emergence of scaling in random networks
    (preferential attachment, BA model)
  - Erdős & Rényi (1959/1960) — On random graphs
  - Newman (2003) — The structure and function of complex networks
  - Eguíluz et al. (2005) — Scale-free brain functional networks
  - Bullmore & Sporns (2009) — Complex brain networks: graph theoretical
    analysis of structural and functional systems
  - Cohen et al. (2000) — Resilience of the Internet to random breakdowns
    (scale-free attack-vs-failure asymmetry)
  - Tononi (2004 / 2014) — IIT 3.0 / 4.0 Φ
  - phi_rs (anima archive) — `phi_spatial` deterministic algorithm SSOT
- **raw refs**: raw#12 (deterministic), raw#9/10 (honest operational
  measurement), raw#15 (no-hardcode — sieve / LCG / encoding deterministic
  algorithm), raw#11 (snake_case).
- **substrate**:
  - `HEXAD/C/c_lib.hexa::c_measure_phi` (RFC 036 phi_spatial primitive)
  - Park-Miller LCG (minimal-standard, Schrage's algorithm, seed=20260523)
  - BA preferential-attachment (Newman 2003 degree-weighted reservoir)
  - ER uniform random edge sampling without replacement (matched edge
    count)
  - graph-CA-XOR (rule 150 graph generalization)

## Verdict (pre-register-frozen + cycle #1 measurement)

```
verdict_class  : pre-register-frozen → FALSIFIED (per pre-registered
                 verdict_rule, 2026-05-23 cycle #1 measurement: Φ_BA <
                 Φ_ER → strict-reverse branch triggered)
evidence_summary: 16-node BA (m=1) vs ER (matched 15 edges) graph-CA-XOR
                 substrate × RFC 036 phi_spatial via c_measure_phi.
                 BA Φ=0.897 < ER Φ=1.000 (margin -10.3%, F1 FAIL).
                 F2 HUB-VULN PASS (drop_hub=0.830 > drop_rand=0.439),
                 F3 DEGREE-CORR FAIL (r=0.170 < 0.4 floor),
                 F4 PHI-FINITE PASS, F5 BYTE-DETERMINISTIC PASS
                 (2-run diff = empty). criteria_met=2/4.
honest_tier    : 🟢 SUPPORTED-NUMERICAL — RFC 036 phi_spatial native
                 replica; single-realization single-seed N=16 finite
                 substrate (L3/L6 carve-out); verdict 은 BA preferential-
                 attachment 의 hub-structure 가 본 specific graph-CA-XOR
                 + phi_spatial measure 하에서는 ER 보다 Φ-우위가 아님 의
                 직접 측정. 'consciousness substrate must be scale-free'
                 의 substrate-level claim 은 본 cycle 의 measurement
                 configuration 하에서 SUPPORTED 되지 않음.
cost           : $0 mac local · LCG seed=20260523 · 2-run byte-identical.
```

**State output**: `HEXAD/LIFE/state/h218_network_topology_2026_05_23/{run_h218.hexa, result.json}`

### Cycle #1 Verification (2026-05-23) — BA vs ER × Φ + hub-freeze vulnerability

`HEXAD/LIFE/state/h218_network_topology_2026_05_23/run_h218.hexa`
($0 mac local, deterministic LCG seed=20260523, hexa-only, c_lib.hexa import,
no LLM, no GPU).

**Run verbatim output**:

```
H_218 — network topology scale-free Φ (BA vs ER, matched edge-density, graph-CA-XOR) — raw#12
  N=16 edges=15 warm=8 dim=12  (deterministic, $0 mac local)
  Φ primitive: RFC 036 phi_spatial via HEXAD/C/c_lib.hexa (Φ>=0 by constr.)
  LCG seed=20260523  graph-CA rule: XOR-of-neighbors (rule 150 graph generalization)

  BA edge count : 15 (expected 15)
  ER edge count : 15 (expected 15)
  BA hub node   : 0 (degree=6)
  BA degrees    : [6,1,4,1,1,1,3,1,2,3,2,1,1,1,1,1]
  ER degrees    : [1,3,1,3,1,1,1,1,2,0,1,2,4,4,3,2]

  Φ(BA  baseline) = 0.896792
  Φ(ER  baseline) = 1.00001
  margin (Φ_BA - Φ_ER) / Φ_ER = -0.103218  (floor 0.1)

  Φ(BA hub-freeze [node 0])    = 0.0666781  drop_hub = 0.830114
  Φ(BA rand-freeze [node 9])  = 0.458193  drop_rand = 0.438599

  per-node drops (BA): [0.830114,0.184443,0.823799,0.0296581,0.266848,0.184443,-1.18816,0.366648,-0.0221795,0.438599,-1.10322,0.142383,0.0920292,0.896781,0.266848,-0.115332]
  Pearson r(degree, drop)  = 0.17005  (floor 0.4)

  F1 SF-GT-ER     (margin >= 10%)        : false  (margin=-0.103218)
  F2 HUB-VULN     (drop_hub > drop_rand) : true  (drop_hub=0.830114 drop_rand=0.438599)
  F3 DEGREE-CORR  (r >= 0.4)             : false  (r=0.17005)
  F4 PHI-FINITE   (all Φ >= 0)           : true
  F5 DETERMINISTIC (2-run byte-identical, verified externally) : true

  VERDICT_RULE: SUPPORTED iff C1+C2 PASS; PARTIAL iff C1 alone; FALSIFIED iff Φ_BA <= Φ_ER
  VERDICT     : FALSIFIED  (criteria_met=2/4)

  result.json written → HEXAD/LIFE/state/h218_network_topology_2026_05_23/result.json
=== H_218 network topology scale-free Φ smoke complete: FALSIFIED ===
```

re-run byte-identical (F5 determinism confirmed via `diff` of two result.json runs).

**Honest evidence summary**:
- (i) **BA Φ < ER Φ at this specific (graph, rule, init, seed) config** — Φ(BA)=0.897 < Φ(ER)=1.000, margin = −10.3%. 'scale-free substrate 는 random substrate 보다 Φ-우위' 가설의 strict-reverse 가 측정됨 → verdict_rule FALSIFIED branch.
- (ii) **hub-vulnerability signature 는 PASS** (F2) — BA graph hub node 0 (degree=6) freeze 시 drop_hub=0.830 ≫ random-node freeze drop_rand=0.439, 약 1.9× 큰 drop. scale-free 의 attack-fragility 의 Φ-측 manifest 는 본 substrate 에서도 관측.
- (iii) **degree-Φ-drop 의 monotone correlation 은 weak** (F3 FAIL) — Pearson r=0.170 < 0.4 floor. degree 가 큰 node 가 freeze 시 더 큰 drop 을 일으킨다는 단순 monotone 관계는 measured 되지 않음. per-node drops 에 음수 값 (node 6: -1.188, node 10: -1.103, node 15: -0.115) 이 있어 freeze 가 Φ 를 *증가* 시킨 sub-cluster 가 존재 — graph-CA-XOR 의 nonlinear interaction 의 결과.
- (iv) **F4 PHI-FINITE PASS** — 모든 baseline Φ ≥ 0 (RFC 036 정합). per-node freeze 의 Φ 도 음수 없음 (drop 의 음수 부호는 baseline − freeze 가 음수일 뿐 freeze 자체 Φ 는 양수).
- (v) **F5 DETERMINISTIC PASS** — 2회 run `diff` empty (byte-identical), LCG seed=20260523, raw#12 정합.
- (vi) **measure-axis fragility (L2 carry)**: phi_spatial 은 1D-lattice 기준 spatial-MI design — graph topology 위 일반화에서 graph 의 structural information 이 trajectory 를 통해 indirect 으로만 들어감. true IIT 4.0 graph-aware Φ 측정 시 결과 달라질 가능성 (named blocker).

**State output**: `HEXAD/LIFE/state/h218_network_topology_2026_05_23/result.json`
**Smoke**: `HEXAD/LIFE/state/h218_network_topology_2026_05_23/run_h218.hexa`
**Φ tier**: 🟢 NUMERICAL (RFC 036 phi_spatial native replica; true phi_rs Rust FFI = named blocker — NOT 🔵, NOT LLM-judged, NOT PyPhi/sympy-primary).

<!-- end of cycle #1 verification block -->

**Follow-up cycles (raw#15 additive, not retraction)**:
- ensemble cycle (L6 closure) — 여러 LCG seeds 의 BA / ER 분포 측정으로
  single-seed artefact 분리.
- alternative graph-CA rule sweep (L1 closure) — AND-of-neighbors /
  majority-vote / threshold-rule 등.
- N sweep (L3 closure) — N ∈ {16, 32, 64, 128} 로 finite-size scaling 측정,
  power-law degree distribution 의 의미 있는 fit 확보.
- alternative perturbation operationalization (L8 closure) — node-removal
  graph 수정, state=1 freeze, state=random freeze 등.
- alternative density sweep (H218.4 보조 prediction — edge-density 증가
  시 두 topology Φ 격차 좁아짐) — edge count ∈ {15, 30, 60, 120} 로 saturation
  곡선 측정.
- IIT 4.0 oracle compare (L2 closure) — phi_rs Rust FFI link landed 시
  graph topology Φ 측정의 measure-axis sensitivity test.
