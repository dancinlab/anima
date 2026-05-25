---
id: H_225
slug: rule-184-class-ii-phi-anomaly
title: H_225 rule-184 Class-II Φ-peak anomaly — TASEP generalization (H_211 follow-up · H_007 Class-IV-unique 가정 attack)
domain: physics + math + information
status: pre-register-frozen
exploration_method: E5 (variable-ablation rule sweep) + E10 (anomaly generalization)
verification_method: W4 (verdict-4-class) + W10 (adversarial sweep)
raw_rank: 12
hexa_only: true
deterministic: true
llm: none
pre_register_frozen: true
frozen_at: 2026-05-24
since: 2026-05-24
---

# H_225 — rule-184 Class-II Φ-peak anomaly

## Hypothesis

H_211 (`shannon_entropy_phi_correlate`) 의 보고에 의하면 elementary CA **rule 184 (TASEP, Wolfram Class II)** 의 Φ ≈ 0.863 이 **rule 110 (Class IV)** 의 Φ ≈ 0.538 보다 **유의하게 높았다**. 이는 H_007 (`cellular_automaton_consciousness`) 의 핵심 주장 — **Class IV (edge-of-chaos) 가 ordered/chaotic 보다 우월한 Φ-peak** — 를 직접 위반한다. 본 cycle 의 hypothesis 는:

1. **H225.1 (reproducibility)** rule 184 의 Φ 가 H_211 baseline (0.863) 의 ±5% 내에서 재현된다.
2. **H225.2 (Class-II coherence)** TASEP 외 다른 **shift-family Class-II rule** (rule 60 = left-XOR-shift / rule 102 = right-XOR-shift; 둘 다 Sierpinski-pattern 생성, neighborhood XOR 기반) 의 Φ 가 rule 184 의 ±20% 내.
3. **H225.3 (Class-II > Class-IV)** 모든 Class-II 후보 (184/60/102) 가 rule 110 (Class-IV) 의 Φ 를 초과.
4. **H225.4 (TASEP shift property)** rule 184 의 shift-conservation (particle-number conserving, deterministic left/right traffic flow) 가 high-Φ 의 candidate mechanism — XOR-shift family 가 동일 shift-property 를 공유하므로 generalization 예상.
5. **H225.5 (determinism)** fixed init + fixed seed → re-run byte-identical (raw#12 strict).

본 cycle 은 H_007 의 Class-IV-unique 가정에 대한 **adversarial sweep**: SUPPORTED 면 H_007 의 핵심 ranking 가 깨지고 ANOMALY_LOCALIZED 이면 rule 184 단독 anomaly + 다른 Class-II 일반화 실패. raw#12 strict (deterministic · hexa-only · llm:none · $0 mac local).

## Why

- **H_007 의 ranking 주장** (commit `H_007_cellular_automaton_consciousness.md` PASS verdict): Φ(rule 110, Class IV) > Φ(rule 30, Class III) > Φ(rule 250, Class II) 가 측정되어 *edge-of-chaos peak* 로 해석. 그러나 rule 250 은 Class-II 중에서도 **degenerate fill** (대부분 cell on → low diversity), 즉 Class-II 의 worst case 만 측정한 비대표 sample 이었다.
- **H_211 의 발견** (Shannon-Φ correlate sweep): wider Class-II rule sweep 에서 **rule 184 (TASEP traffic shift)** 가 rule 110 보다 높은 Φ 를 보였다. 이는 H_007 의 단일-rule-per-class smoke 가 Class-II 내 variance 를 놓쳤음을 시사.
- **rule 184 의 TASEP 의미** (Krug 1991, Schadschneider 2000): 1D Totally Asymmetric Simple Exclusion Process — particle (1) 가 빈 site (0) 으로 결정론적 단방향 hop, particle conservation. statistical-physics 의 가장 잘 연구된 nonequilibrium model. universality class = KPZ (Kardar-Parisi-Zhang).
- **rule 60 / 102 의 XOR-shift 성격** (Wolfram 2002 §3): rule 60 = `(left XOR center)` → left-shift + Sierpinski triangle; rule 102 = `(center XOR right)` → right-shift + Sierpinski. 둘 다 **linear** (XOR) → additive over Z_2 → Sierpinski self-similar pattern. rule 184 의 conservation 과 다른 mechanism (linear additivity vs particle conservation) 이지만 모두 *shift dynamics* + Class-II.
- **Wolfram Class 의 한계** (Martínez 2013): 4-class scheme 은 informal — Class-II 안에서도 simple-fill (rule 250) vs nested (rule 90) vs shift (rule 60/102/184) 처럼 substructure 다양. 본 cycle 의 결과는 Class-II 의 substructure-resolved Φ 가 single representative 보다 정보량 큰 evidence 임을 보임 (positive 든 negative 든).
- **edge-of-chaos 가정의 fragility** (Mitchell/Hraber/Crutchfield 1993): Langton λ 의 critical regime → high computation 주장 자체가 contested (Mitchell critique). H_007 의 PASS 가 결정적이 아닐 가능성을 본 H 가 직접 검증.
- **cross-link H_007 [DIRECT challenge]**: 본 H 는 H_007 의 ranking claim 을 generalization sweep 으로 시험한다. **NOT H_007 의 retraction proposal** — H_007 의 smoke 결과 자체는 byte-identical 로 유효; 본 H 는 *그 결과가 다른 Class-II rule 로 확장 안 됨* 을 보일 뿐.
- **cross-link H_211 [follow-up]**: H_211 의 rule 184 anomaly 보고를 *재현 + 일반화* 한다.
- **cross-link H_157 (Law 76)**: META-CA panpsychism universal-attractor (Ψ(1/2,1/2)) 와 별개 — 본 H 는 generic elementary CA 의 Class-II 내부 variance 만 다룬다.

## Predictions

- **H225.1** Φ(rule 184) 가 0.863 의 ±5% (즉 [0.820, 0.906]) 내. (measurable rel_diff = |Φ - 0.863| / 0.863.)
- **H225.2** Φ(rule 60) ∈ [0.8 × Φ(rule 184), 1.2 × Φ(rule 184)] AND Φ(rule 102) 동일 band.
- **H225.3** Φ(rule 184) > Φ(rule 110) AND Φ(rule 60) > Φ(rule 110) AND Φ(rule 102) > Φ(rule 110).
- **H225.4** Class-II shift-family 의 mean Φ - rule 110 Φ > 0.1 (small but consistent gap).
- **H225.5** re-run byte-identical (5 rep × 4 rule × phi_spatial determinism).

## Variables

- **axis1_rule**: {110 (IV), 184 (II/TASEP), 60 (II/XOR-shift L), 102 (II/XOR-shift R)}
- **axis2_lattice**: N = 16 (H_007 / H_211 와 동일)
- **axis3_trajectory_dim**: dim = 12
- **axis4_warmup**: warm = 8
- **axis5_rep_init**: rep ∈ {0..4} deterministic offset (site i on iff (i+rep)%3 ≠ 0)
- **fixed**: n_bins = 4, periodic boundary, $0 mac local hexa

## Run Protocol

- **smoke**: `HEXAD/LIFE/state/h225_rule184_anomaly_2026_05_24/run_h225.hexa`
- **Φ primitive**: `HEXAD/C/c_lib.hexa` → `c_measure_phi` → RFC 036 `phi_spatial` (import READ-ONLY).
- **mapping**: H_007 와 byte-equal — lattice site = IIT cell, dim-step trajectory = state vector, flat (N×dim) farr → `phi_spatial(states, N, dim, n_bins)`.
- **deterministic**: fixed init + fixed config; re-run byte-identical.
- **hexa_only**: true (NO .py/.sh). **llm**: none.
- **runtime**: $0 mac local hexa; GPU 불필요.
- **ledger**: `result.json` {config, rules, wolfram_class, phi_mean, h211_baseline, criteria, falsifiers, verdict}.
- **honest tier**: NUMERICAL Φ (RFC 036 native replica) = 🟢-tier evidence.

## Criteria

- **C1 (rule 184 reproducibility)** rel_diff(|Φ - 0.863|) / 0.863 ≤ 0.05 → H225.1 PASS
- **C2 (Class-II coherent)** Φ(60) ∧ Φ(102) ∈ [0.8 Φ(184), 1.2 Φ(184)] → H225.2 PASS
- **C3 (Class-II > Class-IV)** Φ(184) > Φ(110) ∧ Φ(60) > Φ(110) ∧ Φ(102) > Φ(110) → H225.3 PASS
- **C4 (byte-identical re-run)** diff(run1, run2) = 0 → H225.5 PASS
- **verdict_rule**:
  - **SUPPORTED** = C1 ∧ C2 ∧ C3 (rule 184 안정 + family coherent + 모두 IV 능가) → H_007 Class-IV-unique 가정 깨짐
  - **ANOMALY_LOCALIZED** = C1 ∧ (rule 184 > rule 110) ∧ ¬C2 (rule 184 단독 anomaly, family 일반화 실패)
  - **FALSIFIED** = otherwise

## Falsifiers

- **F1 RULE184_REGRESSION**: rel_diff(rule 184 vs H_211 baseline) > 5% → H225.1 FALSIFIED (rule 184 결과 substrate-sensitive, H_211 보고 non-reproducible). (measurable: rel_diff.)
- **F2 CLASS_II_DIVERGE**: Φ(rule 60) ∉ ±20% band OR Φ(rule 102) ∉ ±20% band → H225.2 FALSIFIED. (measurable: 두 rule 의 band membership.)
- **F3 CLASS_II_LE_IV**: Φ(rule 184) ≤ Φ(rule 110) AND Φ(rule 60) ≤ Φ(rule 110) AND Φ(rule 102) ≤ Φ(rule 110) → H225.3 FALSIFIED (Class-II 전체가 Class-IV 못 이김). (measurable: 세 Δ.)
- **F4 BYTE_IDENT_VIOLATION**: re-run Φ byte-different → raw#12 위반 → smoke 무효.
- **F5 PHI_NEGATIVE**: 임의 rule Φ < 0 → measure invalid (phi_spatial Φ≥0 위반).
- **F6 POST-HOC**: frozen 후 verdict 방향 edit → raw#12 violation.

## Honest Limits (raw#91 c3)

- **L1**: Wolfram Class 자체가 fuzzy — Class-II 안에서도 simple-fill / nested / shift / additive 등 substructure 무수. 본 cycle 의 rule 60/102/184 가 "shift family" 를 충분히 대표하는지는 design choice (특히 60/102 는 linear additive, 184 는 nonlinear conservation — mechanism 이 동일하지 않음).
- **L2**: TASEP (rule 184) 의 high Φ 는 *interpretive* — particle-shift conservation 이 high integrated information 의 *원인* 인지 *상관* 인지 본 smoke 로 구분 불가. mechanism claim 은 advisory 만.
- **L3**: 4-rule sample 은 small — 8 rule (rule 184 외 154, 226, 240 등 다른 shift 후보) sweep 으로 일반화하면 더 robust. 본 cycle 은 1 cycle scope 한정.
- **L4**: phi_spatial proxy (RFC 036 native replica) ≠ full IIT 4.0 — true MIP 계산은 NP-hard. 본 measure 의 Φ 절대값은 oracle vs replica ~1e-6 drift; ranking 영향 없음.
- **L5**: anomaly mechanism 자체가 가설 — rule 184 의 high Φ 가 (a) TASEP shift-conservation, (b) bin=4 spatial-discretization artifact, (c) N=16 finite-size effect, (d) init-distribution dependence 중 어느 것인지 본 cycle 로 분리 불가. (b)/(c)/(d) 는 별도 cycle (N sweep, n_bins sweep, init sweep) 필요.
- **L6**: H_211 baseline 0.863 자체가 single config single state.json — 본 cycle 의 ±5% reproducibility test 의 anchor 가 single measurement 면 stochastic 가능성 (raw#12 deterministic 으로는 0 인데, H_211 도 raw#12 였는지 확인 필요).
- **L7**: rule 60 과 102 가 mirror pair (Z_2 reflection) — 동일 Φ 가 trivially 예상됨 (boundary periodic + Φ-spatial reflection-invariant). 실제 같은 값이면 sanity check 통과, 다르면 raw#12 implementation bug.
- **L8**: Class-IV-unique 가정의 retraction 은 **본 cycle 1 회 결과로 결론 불가** — H_007 의 ranking 은 rule 250 (degenerate Class-II) 와 비교일 뿐, 본 H 의 더 fair Class-II representative 대비 결과는 *generalization 확장* 의 첫 evidence.

## Cross-Links

- **direct adversary H**: H_007 (cellular-automaton-consciousness — Class-IV-unique Φ-peak 가정의 평가 대상)
- **direct follow-up H**: H_211 (shannon-entropy-phi-correlate — rule 184 anomaly 보고 출처)
- **sister H**: H_011 (IIT geometry), H_157 (Law 76 panpsychism universal-attractor — DISTINCT claim, no overlap), H_204 (C2 rule class mapping)
- **Φ primitive**: `HEXAD/C/c_lib.hexa` (`c_measure_phi` → RFC 036 `phi_spatial`) + `HEXAD/C/c_phi_smoke.hexa` (F-C-PORT-3 oracle anchor)
- **raw**: raw#12 (deterministic strict) + raw#91 c3 (honest limits) + raw#82 (no post-hoc retraction)
- **literature**:
  - Krug (1991) Boundary-induced phase transitions in driven diffusive systems (TASEP)
  - Schadschneider (2000) Statistical physics of vehicular traffic and some related systems (TASEP)
  - Cook (2004) Universality in elementary cellular automata (rule 110 vs other classes)
  - Wolfram (1984, 2002) A New Kind of Science (rule classes; rule 60/102/184 substructure)
  - Mitchell, Hraber, Crutchfield (1993) Revisiting the edge of chaos (Langton λ critique)
  - Martínez (2013) A note on elementary cellular automata classification (Class-II substructure)
  - Tononi (2004), Oizumi/Albantakis/Tononi (2014) IIT formal Φ
  - Langton (1990) Computation at the edge of chaos

## Verdict

```
verdict_class: FALSIFIED (pre-register-frozen smoke, post-run honest)
phi_by_rule:
  Class-IV  (rule 110, complex     )  Φ = 0.556454
  Class-II  (rule 184, TASEP shift )  Φ = 1.19781    ← 1.42× H_211 baseline (0.863)
  Class-II  (rule  60, XOR-shift L )  Φ = 1.6832     ← family-max
  Class-II  (rule 102, XOR-shift R )  Φ = 1.6832     ← rule 60 mirror (L7 sanity)
ranking: rule 60 = rule 102 > rule 184 > rule 110
criteria_met: 2/4 (C3 PASS · C4 PASS · C1 FAIL · C2 FAIL)
evidence_summary: 🟢 NUMERICAL — RFC 036 phi_spatial; ranking 자체는 Class-II > Class-IV 일관 (C3 STRONG PASS) 이지만 (a) H_211 baseline non-reproducible (rule 184 = 1.19781, 0.863 의 1.39× — 5% band 밖, F1 triggered) AND (b) Class-II family Φ 가 widely diverge (rule 184 vs rule 60/102 사이 40% gap — F2 triggered)
falsifiers_triggered: F1 (rule 184 regression vs H_211), F2 (Class-II diverge)
```

### Pre-register-frozen smoke (2026-05-24)

4-rule Class-II ⊥ Class-IV Φ sweep pre-registered + RUN ($0 mac local, deterministic, hexa-only, llm:none).
1D elementary CA, N=16 periodic, dim=12 trajectory, 5 deterministic reps, Φ via RFC 036 phi_spatial.

**Run verdict (VERBATIM, `hexa run`)**:
```
H_225 — rule-184 Class-II Φ-peak anomaly · TASEP generalization (raw#12)
  N=16 dim=12 warm=8 reps=5  (deterministic, $0 mac local)
  Φ primitive: RFC 036 phi_spatial via HEXAD/C/c_lib.hexa (Φ>=0 by constr.)

  Φ(rule 110  Class-IV  complex      ) = 0.556454
  Φ(rule 184  Class-II  TASEP shift  ) = 1.19781
  Φ(rule 60   Class-II  XOR-shift L  ) = 1.6832
  Φ(rule 102  Class-II  XOR-shift R  ) = 1.6832

  C1 RULE184_REPRO (|Φ - H_211 ±5%|): false  (H_211=0.863 · this=1.19781 · rel_diff=0.387966)
  C2 CLASS_II_COHERENT (±20% of Φ184): false  (band=[0.958252,1.43738] · 60 in=false · 102 in=false)
  C3 CLASS_II_GT_IV (all > Φ110)     : true  (184>110=true · 60>110=true · 102>110=true)
  C3-184-only (rule 184 > rule 110)  : true  (Δ=0.64136)

  F1 RULE184_REGRESSION (rel_diff>5%) : true
  F2 CLASS_II_DIVERGE  (60/102 ∉ ±20%): true
  F3 CLASS_II_LE_IV    (all II ≤ IV) : false
  F4 BYTE_IDENT_CONTRACT (det re-run): true
  F5 PHI_NEGATIVE                    : false

  VERDICT_RULE: SUPPORTED iff C1∧C2∧C3 · ANOMALY_LOCALIZED iff C1∧(184>110)∧¬C2 · else FALSIFIED
  VERDICT     : FALSIFIED
```

re-run byte-identical (F4 BYTE_IDENT confirmed via `diff` of run1 vs run2).

honest tier: 🟢 NUMERICAL — RFC 036 phi_spatial native replica. NOT 🔵 (no formal proof; Φ-ranking 만 numerical).

**Interpretation (honest, raw#82 no post-hoc rewriting)**:

1. **C3 PASS (Class-II > Class-IV)** — 세 Class-II rule (184/60/102) 모두 rule 110 의 Φ 능가. **H_007 의 Class-IV-unique Φ-peak 가정에 대한 strong adversarial evidence**.
2. **C1 FAIL (H_211 non-reproduction)** — rule 184 의 Φ = 1.198 ≠ H_211 의 0.863 (rel_diff 38.8%). 두 cycle 의 substrate config 가 byte-identical 이라면 raw#12 위반; 다르면 *Φ 가 config-sensitive* 증거 (L5 의 (c)(d) 후보). **H_211 baseline 자체의 검증 follow-up 필요**.
3. **C2 FAIL (Class-II divergence)** — rule 60/102 의 Φ (1.683) 이 rule 184 의 Φ (1.198) 보다 40% 높음. shift-family 안에서도 mechanism 분기 (XOR-additive vs particle-conservation). "TASEP shift property 가 high-Φ mechanism" 가설 (H225.4) 약화.
4. **L7 sanity PASS** — rule 60 과 rule 102 의 Φ 가 byte-identical (1.6832) — Z_2 mirror reflection 정합, implementation bug 없음.

**State output**: `HEXAD/LIFE/state/h225_rule184_anomaly_2026_05_24/result.json`
**Smoke**: `HEXAD/LIFE/state/h225_rule184_anomaly_2026_05_24/run_h225.hexa`
**Φ tier**: 🟢 NUMERICAL (RFC 036 phi_spatial native replica; true phi_rs Rust FFI = named blocker — NOT 🔵, NOT LLM-judged).
