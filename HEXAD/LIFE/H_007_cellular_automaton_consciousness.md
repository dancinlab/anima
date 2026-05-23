---
id: H_007
slug: cellular-automaton-consciousness
title: H-CX-520 cellular automaton consciousness — Class-IV (edge-of-chaos) CA가 ordered/chaotic 보다 높은 IIT Φ를 emerge한다
domain: physics
status: pre-register-frozen
exploration_method: E5 (variable-ablation rule sweep) + E10 (emergence)
verification_method: W4 (verdict-4-class) + W10 (adversarial sweep)
raw_rank: 12
hexa_only: true
deterministic: true
llm: none
pre_register_frozen: true
frozen_at: 2026-05-23
since: 2026-04-29 (legacy)
---

# H_007 — cellular automaton consciousness

## Hypothesis

generic cellular automaton (CA) 의 dynamics가 integrated information Φ > 0 를 emerge하며, **Wolfram Class IV (edge-of-chaos / Langton λ ≈ critical) CA가 ordered (Class I/II) CA 와 chaotic (Class III) CA 보다 더 높은 Φ를 산출한다**. universal-computation capability + irreducibility (Class IV의 특성) 가 high-Φ correlate라는 가설. 본 cycle은 1D elementary CA 3-rule-class smoke (rule 250 ordered · rule 30 chaotic · rule 110 Class-IV)로 Φ ranking을 pre-register-frozen + RUNNABLE 측정한다. raw#12 strict (deterministic · hexa-only · llm:none · $0 mac local).

## Why

- **Wolfram CA classes** (Wolfram 1984, *A New Kind of Science* 2002): elementary CA를 4 class로 분류 — **Class I** (homogeneous fixed point), **Class II** (periodic / nested), **Class III** (chaotic / pseudo-random; rule 30, 90), **Class IV** (complex localized structures, particle-like gliders; rule 110, 54). Class IV는 order ↔ chaos 경계 (edge-of-chaos)에 위치.
- **Edge-of-chaos / Langton's λ** (Langton 1990): rule space를 activity parameter λ로 sweep하면 ordered ↔ chaotic 사이 좁은 critical regime에서 maximal computation / information transmission이 emerge — Class IV가 이 regime. 가설: 이 edge-of-chaos가 high integrated information의 substrate.
- **rule 110 universality** (Cook 2004): rule 110은 Turing-universal — Class IV의 computational irreducibility를 가장 강하게 instantiate. IIT는 irreducibility (Φ = whole가 부분으로 환원 불가한 정도)를 consciousness measure로 정의 → Class IV의 irreducibility가 Φ correlate라는 직접적 bridge.
- **IIT Φ** (Tononi 2004, Oizumi/Albantakis/Tononi 2014, IIT 4.0): 시스템의 integrated information = whole의 cause-effect structure가 minimum-information-partition (MIP) 으로 환원될 수 없는 정도. 본 cycle은 anima repo의 RFC 036 `phi_spatial` (phi_rs `compute_phi_inner` spatial slice의 byte-equal native replica) 를 small-n Φ proxy로 사용 — 각 lattice site = 1 IIT cell, 그 temporal trajectory = state vector.
- **legacy negative result carry**: 본 H의 legacy F1-cycle4-T8p sweep (commit `f02853db`)은 Wolfram rule {30,90,110,184} 에서 3 pre-reg hypotheses FALSIFIED (rule 110 universal이나 Φ low) — 본 cycle은 그 negative와 distinct하게 *rule-class ranking* (IV > ordered AND IV > chaotic) 을 측정 (legacy는 absolute Φ floor 측정).
- **cross-link H_157 [DISTINCT claim]**: H_157 (Law 76 Mathematical Panpsychism)은 META-CA fixed-point Ψ(1/2,1/2) softmax-mixture proxy로 *우주적 panpsychism universal-attractor* 를 다룬다. 본 H_007은 그것과 **분리** — generic CA dynamics (elementary CA rule classes)가 Φ>0를 emerge하는지 + Class-IV가 우월한지의 GENERIC 문제이지, panpsychism universal-attractor 주장이 아니다. (overlap 없음, cross-link only.)
- **cross-link H_011 (IIT geometry)**: IIT의 cause-effect structure를 geometry로 보는 lane — 본 H의 Φ measure가 그 geometry primitive의 spatial-slice 사용.
- **cross-link H_003 (life origin)**: H_003 H3.4 (autopoietic closure system Φ > 0, life ⊂ consciousness nested) 와 동일 Φ primitive lane — CA는 life-emergence의 abstract substrate (Conway's Game of Life가 대표).

## Predictions

- **H7.1 (CA Φ > 0)**: 3 rule class 모두 Φ ≥ 0 (RFC 036 phi_spatial은 Φ≥0 by construction), 그리고 Class-IV (rule 110) Φ > 0 (strictly positive — non-trivial integrated information).
- **H7.2 (Class-IV > ordered)**: Φ(rule 110, Class IV) > Φ(rule 250, Class II ordered).
- **H7.3 (Class-IV > chaotic)**: Φ(rule 110, Class IV) > Φ(rule 30, Class III chaotic).
- **H7.4 (edge-of-chaos peak)**: Φ ranking이 ordered < … and chaotic < … with Class-IV 최상위 — edge-of-chaos가 Φ peak regime이라는 Langton λ 정합.
- **H7.5 (determinism)**: fixed init + fixed seeds → re-run byte-identical Φ (raw#12 deterministic 정합).

## Variables

- **axis1_rule_class** (primary): [ordered (Class I/II), chaotic (Class III), class_iv (Class IV)]
  - representative elementary rules: ordered = **rule 250** (Class II simple fill), chaotic = **rule 30** (Class III pseudo-random), class_iv = **rule 110** (Class IV Turing-universal complex)
- **axis2_lattice_size**: N = 16 (본 smoke; ablation lane N ∈ {16, 32, 64} 별도 cycle)
- **axis3_trajectory_dim**: dim = 12 recorded temporal steps / site (IIT cell state vector length)
- **axis4_warmup**: warm = 8 steps (transient 제거 후 recording)
- **axis5_rep_init**: rep ∈ {0,1,2,3,4} — deterministic init offset (site i on iff (i+rep)%3 ≠ 0); Φ는 5-rep mean
- **fixed**: n_bins = 4 (phi_rs RFC 036 default binning), periodic boundary, $0 mac local hexa

## Run Protocol

- **smoke**: `HEXAD/LIFE/state/h007_ca_phi_2026_05_23/run_ca_phi.hexa`
- **Φ primitive**: `HEXAD/C/c_lib.hexa` → `c_measure_phi` → RFC 036 `phi_spatial` (phi_rs `compute_phi_inner` steps 1-4 spatial slice의 byte-equal native-C replica; import READ-ONLY).
- **mapping**: 각 lattice site i = 1 IIT cell; 그 dim-dim state vector = warmup 후 dim step temporal trajectory (binary 0/1). flat (N×dim) farr → `phi_spatial(states, N, dim, n_bins)`.
- **deterministic**: fixed init (rep offset, no RNG) + fixed config; re-run byte-identical.
- **hexa_only**: true (NO .py/.sh). **llm**: none (raw#12 strict).
- **runtime**: $0 mac local hexa; GPU 불필요 (small-n CA + spatial Φ). GPU 필요 시 → STOP + document.
- **ledger**: `result.json` {config, rules, wolfram_class, phi_mean per class, falsifiers F1-F5, verdict}.
- **honest tier**: NUMERICAL Φ (RFC 036 native replica) = 🟢-tier evidence. 진짜 phi_rs Rust FFI link = named blocker (RFC 036 §"FFI shim", phi_rs PyO3 cdylib no C ABI). Class-IV-CA-는-의식이다 식의 strong claim NOT made — Φ proxy ranking 측정만.

## Criteria

- **C1 (Φ nonneg + IV positive)**: 모든 class Φ ≥ 0 AND Φ(Class-IV) > 0 → H7.1 PASS
- **C2 (Class-IV > ordered)**: Φ(rule 110) > Φ(rule 250) → H7.2 PASS
- **C3 (Class-IV > chaotic)**: Φ(rule 110) > Φ(rule 30) → H7.3 PASS
- **C4 (ranking peak)**: Class-IV가 최상위 (C2 ∧ C3) → H7.4 PASS
- **C5 (determinism)**: re-run byte-identical Φ → H7.5 PASS
- **verdict_rule**: **PASS = Φ(Class-IV) > Φ(ordered) AND Φ(Class-IV) > Φ(chaotic) AND all Φ ≥ 0** (C1∧C2∧C3∧C4); **FAIL = ranking flat/inverted** (Class-IV가 최상위 아님) — document. MIXED = Φ>0 confirmed이나 Class-IV peak 미달.

## Falsifiers

- **F1 NONNEG**: 임의 class에서 Φ < 0 → measure invalid (phi_spatial Φ≥0 위반) → smoke FALSIFIED. (measurable: 3 Φ 값.)
- **F2 IV>ORD**: Φ(rule 110, Class-IV) ≤ Φ(rule 250, ordered) → H7.2 FALSIFIED. (measurable: Δ = Φiv − Φord.)
- **F3 IV>CHA**: Φ(rule 110, Class-IV) ≤ Φ(rule 30, chaotic) → H7.3 FALSIFIED. (measurable: Δ = Φiv − Φcha.)
- **F4 IV>0**: Φ(rule 110, Class-IV) = 0 (no integrated information) → H7.1 strictly-positive 부분 FALSIFIED. (measurable: Φiv.)
- **F5 SEPARATION**: margin = Φ(Class-IV) − max(Φ_ord, Φ_cha) ≤ 1e-6 (Class-IV가 다른 둘보다 측정-유의하게 높지 않음) → edge-of-chaos peak (H7.4) FALSIFIED. (measurable: margin.)
- **F6 NONDETERMINISM**: re-run Φ가 byte-identical 아님 → raw#12 deterministic 위반 → smoke 무효.
- **F7 POST-HOC**: frozen 후 verdict 방향 edit → raw#12 violation, raw#82 retraction.

## Honest Limits (raw#91 c3)

- **L1**: small-n Φ proxy (RFC 036 phi_spatial, N=16 sites × dim=12) ≠ full IIT 4.0 — true IIT는 모든 cause-effect repertoire + MIP over 모든 partition (NP-hard, exponential) 계산 요구. 본 measure는 spatial-slice mutual-information proxy일 뿐.
- **L2**: CA Φ interpretation은 contested — IIT가 brain 외 system (CA, digital substrate)에 의미 가지는지 자체가 open debate (Tononi vs critics). "CA has consciousness" 식 주장 NOT made — Φ proxy ranking 측정만.
- **L3**: rule-class assignment이 coarse — Wolfram 4-class는 informal classification (정확한 class 경계는 undecidable; rule 110이 Class IV임도 universality 증명 이후 확정). representative single-rule (250/30/110) per class는 class 전체를 대표 못함.
- **L4**: IIT cell = lattice site, state vector = temporal trajectory라는 mapping은 design choice — alternative mapping (spatial neighborhood as state, 또는 site-pair MI)은 다른 Φ 값/ranking 산출 가능. mapping 정당화는 phi_rs spatial-slice convention 차용일 뿐 first-principles 아님.
- **L5**: N=16, dim=12, reps=5는 single-config smoke — lattice-size / dim / warmup / init-distribution sweep (true λ-parameter sweep 포함)은 별도 cycle. Φ ranking이 config-robust한지 미검증.
- **L6**: deterministic init (rep offset, single-seed 계열)은 init-distribution 전체를 sample 못함 — 다른 init regime (random density, single-seed, all-ones)에서 ordered rule이 degenerate constant trajectory → Φ artifact 가능 (proto에서 single-seed rule 250 Φ artifact 관측됨; 본 smoke는 (i+rep)%3 dense init으로 완화하나 완전 해소 X).
- **L7**: legacy F1-cycle4 (commit f02853db) Wolfram sweep은 3 pre-reg hypotheses FALSIFIED (rule 110 universal이나 Φ low) — 본 cycle ranking PASS는 그 legacy absolute-Φ-floor negative와 metric이 다르며, 둘을 단일 verdict로 통합하지 않음 (별도 evidence lanes).
- **L8**: phi_rs Rust FFI link은 named blocker (RFC 036 §FFI shim — phi_rs PyO3 cdylib, no C ABI); 본 measure는 byte-equal native-C replica (이 machine err≈8e-7 vs documented oracle, ranking에는 무영향이나 absolute Φ는 oracle과 1e-6 수준 drift).

## Cross-Links

- **sister H**: H_157 (Law 76 Mathematical Panpsychism — META-CA fixed-point Ψ(1/2,1/2) softmax-mixture proxy; **DISTINCT claim** — panpsychism universal-attractor, NOT generic-CA-Φ; cross-link only, no overlap), H_011 (IIT geometry — 동일 Φ-geometry lane), H_003 (life origin — H3.4 autopoietic Φ>0 동일 primitive lane), H_006 (coupled oscillator), H_012 (autopoietic network)
- **Φ primitive**: `HEXAD/C/c_lib.hexa` (`c_measure_phi` → RFC 036 `phi_spatial`) + `HEXAD/C/c_phi_smoke.hexa` (F-C-PORT-3 oracle anchor) — import READ-ONLY
- **raw**: raw#12 (deterministic strict) + raw#91 c3 (honest limits) + raw#82 (no post-hoc retraction)
- **own**: (anima-not-CA identity; CA는 abstract substrate analogy, anima cells ≠ CA cells)
- **legacy archive**: `docs/hypotheses/H-CX-520-cellular-automaton-consciousness.md` + commits `f02853db` (F1-cycle4-T8p Wolfram MIXED) + `ccc6cdb2` (F1-cycle4-T8e Conway DENSITY SUPPORTED 16%)
- **legacy commits**: `git log --oneline | grep -E "F1-cycle4-T8"`
- **literature**:
  - Wolfram (1984) Universality and complexity in cellular automata
  - Wolfram (2002) A New Kind of Science (Class I-IV)
  - Langton (1990) Computation at the edge of chaos (λ parameter)
  - Cook (2004) Universality in elementary cellular automata (rule 110 Turing-universal)
  - Tononi (2004) An information integration theory of consciousness
  - Oizumi, Albantakis, Tononi (2014) From the phenomenology to the mechanisms of consciousness: IIT 3.0

## Verdict

```
verdict_class: PASS (pre-register-frozen smoke)
phi_by_rule_class:
  Class-IV (rule 110, complex)   Φ = 0.556454   ← highest
  Class-III (rule 30, chaotic)   Φ = 0.509944
  Class-II  (rule 250, ordered)  Φ = 0.0000114511  (≈0)
ranking: Class-IV > chaotic > ordered  (edge-of-chaos peak — H7.4 SUPPORTED)
evidence_summary: 🟢 NUMERICAL — RFC 036 phi_spatial; Class-IV CA가 ordered/chaotic 보다 높은 Φ
falsifiers_triggered: none (F1-F5 all PASS; F6 byte-identical re-run; F7 N/A)
criteria_met: 5/5 (C1 Φ≥0+IV>0 · C2 IV>ord · C3 IV>cha · C4 IV-peak · C5 determinism)
```

### Pre-register-frozen smoke (2026-05-23)

CA → IIT Φ smoke pre-registered + RUN ($0 mac local, deterministic, hexa-only, llm:none).
1D elementary CA, N=16 periodic lattice, dim=12 trajectory, 5 deterministic reps, Φ via RFC 036 phi_spatial.

**Run verdict (VERBATIM, `hexa run`)**:
```
H_007 — cellular automaton consciousness · CA → IIT Φ smoke (raw#12)
  N=16 dim=12 warm=8 reps=5  (deterministic, $0 mac local)
  Φ primitive: RFC 036 phi_spatial via HEXAD/C/c_lib.hexa (Φ>=0 by constr.)

  Φ(rule 250  ordered  Class-II ) = 1.14511e-05
  Φ(rule 30   chaotic  Class-III) = 0.509944
  Φ(rule 110  Class-IV complex  ) = 0.556454

  F1 NONNEG  (all Φ>=0)            : true
  F2 IV>ORD  (Φiv>Φord)            : true  (Δ=0.556443)
  F3 IV>CHA  (Φiv>Φcha)            : true  (Δ=0.0465102)
  F4 IV>0    (Φiv>0)               : true
  F5 SEPARATION (margin>1e-6)      : true  (margin=0.0465102)

  VERDICT_RULE: PASS iff Φ(IV) > Φ(ord) AND Φ(IV) > Φ(cha) AND all Φ>=0
  VERDICT     : PASS
=== H_007 CA→Φ smoke complete: PASS ===
```

re-run byte-identical (F6 determinism confirmed via `diff`).
honest tier: 🟢 NUMERICAL — RFC 036 phi_spatial native replica (이 machine err≈8e-7 vs documented phi_rs oracle 0.5000000001324147; ranking 무영향). 진짜 phi_rs Rust FFI = named blocker. NOT LLM-judged, NOT PyPhi/sympy-primary, NOT 🔵.

**State output**: `HEXAD/LIFE/state/h007_ca_phi_2026_05_23/result.json`
**Smoke**: `HEXAD/LIFE/state/h007_ca_phi_2026_05_23/run_ca_phi.hexa`
**Φ tier**: 🟢 NUMERICAL (RFC 036 phi_spatial native replica; true phi_rs Rust FFI = named blocker — NOT 🔵, NOT LLM-judged, NOT PyPhi/sympy-primary).
```
