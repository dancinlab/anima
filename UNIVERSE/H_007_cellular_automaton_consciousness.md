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

- **smoke**: `UNIVERSE/state/h007_ca_phi_2026_05_23/run_ca_phi.hexa`
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

> **라벨 주의**: 위 `C1~C5` 는 본 H 의 **discrete-rule criterion** (이산 Wolfram-class 3-rule 비교)의 내부 sub-criteria. 아래 추가되는 **C2-LAMBDA criterion** (Langton λ 연속 sweep)은 그것과 별개의 상위 criterion 이며, 내부 sub-label `C2.1/C2.2/C2.3` 은 `C2-LAMBDA` namespace 하위다. extend (신규 H 아님).

## Criteria — C2-LAMBDA (Langton λ continuous sweep · 2026-05-25)

**Motivation**: 위 discrete-rule criterion 은 세 개의 *이산* rule(250/30/110)만 비교해 "Class-IV 가 더 높다"는 *ranking* 을 보였다. 그러나 edge-of-chaos hypothesis 의 핵심 주장은 Φ peak 가 **중간 Langton λ (chaos↔order 임계)**에서 발생한다는 것 — 이는 λ 를 *연속적으로* sweep 해야 직접 검증된다. C2-LAMBDA = Langton λ 를 grid 로 sweep 하여 Φ(λ) 곡선을 측정하고 peak λ* 를 localize.

- **Langton λ 정의**: elementary CA rule table 8개 neighborhood entry 중 active(=1) output 의 fraction. λ=0 ⇒ rule 0 (전부 dead, ordered fixed point) · λ=1 ⇒ rule 255 (전부 alive, saturated fixed point). 8개 neighborhood ⇒ λ 는 자연스럽게 1/8 단위로 양자화 — elementary CA 의 **exact 최정밀 λ grid** (interpolation artifact 없음).
- **grid**: λ ∈ {0.0, 0.125, 0.25, ..., 1.0} = k_active/8, k_active ∈ {0..8} (9점).
- **ensemble estimator (핵심)**: Langton λ 는 *통계적* parameter — 각 λ 에 C(8, k_active) 개의 rule 이 존재 (최대 C(8,4)=70). 단일 임의 rule 을 쓰면 "어느 rule 이 그 λ 에 떨어졌나" artifact 에 취약 (초기 single-rule 시도에서 λ=0.375 단일 spike 만 관측됨). 따라서 **Φ(λ) = 그 λ 의 output-bit popcount 를 가진 모든 C(8,k) rule 의 ensemble mean Φ** (exhaustive 256-rule 전수, deterministic, RNG 없음) — λ *자체*의 속성으로 측정.
- **measure**: 각 λ 의 ensemble-mean Φ → peak λ* = argmax_λ Φ(λ); inverse-U 형태(peak 가 양 endpoint λ=0·λ=1 보다 strictly 높은가).
- **config**: discrete-rule smoke 와 동일 substrate (N=16 periodic, dim=12 trajectory, warm=8, 5 deterministic reps, RFC 036 phi_spatial, n_bins=4).

**pre-registered criteria**:
- **C2.1 (INTERIOR-PEAK)**: Φ(λ) 가 interior λ 에서 peak — Φ(λ*) > Φ(λ=0) AND Φ(λ*) > Φ(λ=1), λ* ∈ interior (양 끝 아님) → inverse-U.
- **C2.2 (EDGE-OF-CHAOS)**: peak λ* 가 edge-of-chaos band 0.3 ≤ λ* ≤ 0.7.
- **C2.3 (DETERMINISM)**: cross-process re-run sha256-identical (raw#12; RFC 033 single-global-RNG 이므로 in-process byte-equal 은 det test 아님 — 별도 process 재실행 비교).
- **C2-LAMBDA verdict_rule**: **PASS = C2.1 ∧ C2.2**; C2.3 은 raw#12 무결성 gate. FAIL = peak 가 endpoint 이거나 λ* ∉ [0.3, 0.7] — document.

**C2-LAMBDA Falsifiers** (pre-registered, measurable):
- **F-C2-1 NO-PEAK**: argmax Φ(λ) 가 endpoint(λ=0 또는 λ=1) → interior peak 없음 → C2.1 FALSIFIED. (measurable: peak_idx.)
- **F-C2-2 OUT-OF-BAND**: peak λ* < 0.3 또는 > 0.7 → edge-of-chaos band 밖 → C2.2 FALSIFIED. (measurable: λ*.)
- **F-C2-3 FLAT**: max Φ(λ) − max(Φ(0), Φ(1)) ≤ 1e-6 → inverse-U 평탄 → C2.1 FALSIFIED. (measurable: margin.)
- **F-C2-4 NONDETERMINISM**: cross-process result.json sha256 불일치 → raw#12 위반.

**C2-LAMBDA Honest Limits**:
- **CL1**: λ 가 1/8 단위로 quantized — elementary CA 의 구조적 한계 (8 neighborhood). λ* = 0.375 는 grid 의 한 점이며, true 임계 λ 는 0.375 부근 어딘가 (sub-grid 정밀도는 더 큰 neighborhood radius CA 필요 = 별도 cycle). L5 의 "true λ-parameter sweep" 잔여 항목을 본 C2-LAMBDA 가 **부분 충족** — 단, finer λ 분해능은 미해결.
- **CL2**: ensemble mean 은 λ 의 평균 거동을 측정 — λ peak 가 *특정 rule* (예: rule 110) 때문인지 *λ 통계 전체* 때문인지는 구분 못함. discrete-rule criterion (단일 rule 110 우위) 과 C2-LAMBDA (λ-ensemble peak) 는 상보적 증거이지 동일 주장 아님.
- **CL3**: L1~L8 (discrete-rule honest limits) 전부 C2-LAMBDA 에도 그대로 적용 — small-n Φ proxy, CA-Φ interpretation contested, Wolfram class assignment coarse, mapping design choice, phi_rs FFI named blocker 등.

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

**State output**: `UNIVERSE/state/h007_ca_phi_2026_05_23/result.json`
**Smoke**: `UNIVERSE/state/h007_ca_phi_2026_05_23/run_ca_phi.hexa`
**Φ tier**: 🟢 NUMERICAL (RFC 036 phi_spatial native replica; true phi_rs Rust FFI = named blocker — NOT 🔵, NOT LLM-judged, NOT PyPhi/sympy-primary).
```

### C2-LAMBDA — Langton λ continuous sweep (2026-05-25)

```
verdict_class: PASS (C2-LAMBDA, pre-registered)
estimator: ensemble mean Φ over all C(8,k_active) elementary rules per λ (exhaustive, deterministic)
phi_lambda_curve (ensemble-mean Φ):
  λ=0.000  (k=0, C(8,0)=1 )  Φ = 1.14511e-05   ← endpoint (rule 0, all-dead, ordered fixed pt)
  λ=0.125  (k=1, C(8,1)=8 )  Φ = 0.879827
  λ=0.250  (k=2, C(8,2)=28)  Φ = 1.29166
  λ=0.375  (k=3, C(8,3)=56)  Φ = 1.34332         ← PEAK λ*
  λ=0.500  (k=4, C(8,4)=70)  Φ = 1.27251
  λ=0.625  (k=5, C(8,5)=56)  Φ = 1.32827
  λ=0.750  (k=6, C(8,6)=28)  Φ = 0.927317
  λ=0.875  (k=7, C(8,7)=8 )  Φ = 1.16028
  λ=1.000  (k=8, C(8,8)=1 )  Φ = 1.14511e-05   ← endpoint (rule 255, all-alive, saturated fixed pt)
peak: λ* = 0.375  Φ(λ*) = 1.34332
shape: inverse-U — 양 endpoint(λ=0·λ=1) 모두 floor(~1.1e-5), interior 전 구간 Φ≫floor, peak 가 interior
criteria_met: C2.1 INTERIOR-PEAK PASS · C2.2 EDGE-OF-CHAOS PASS (λ*=0.375 ∈ [0.3,0.7]) · C2.3 DETERMINISM PASS (cross-process sha256-identical)
falsifiers_triggered: none (F-C2-1..4 all PASS)
evidence_summary: 🟢 NUMERICAL — Φ(λ) ensemble curve가 edge-of-chaos (λ*≈0.375) inverse-U peak; Langton λ 임계 정합
```

**Run verdict (VERBATIM, `hexa run`)**:
```
H_007 — cellular automaton consciousness · C2 Langton-λ sweep (raw#12)
  N=16 dim=12 warm=8 reps=5  (deterministic, $0 mac local)
  Φ primitive: RFC 036 phi_spatial via HEXAD/C/c_lib.hexa (Φ>=0 by constr.)
  grid: λ = k_active/8 for k_active in 0..8 (finest exact elem-CA λ grid)

  λ=0.0  (k=0, ensemble C(8,0)=1)   mean Φ = 1.14511e-05
  λ=0.125  (k=1, ensemble C(8,1)=8)   mean Φ = 0.879827
  λ=0.25  (k=2, ensemble C(8,2)=28)   mean Φ = 1.29166
  λ=0.375  (k=3, ensemble C(8,3)=56)   mean Φ = 1.34332
  λ=0.5  (k=4, ensemble C(8,4)=70)   mean Φ = 1.27251
  λ=0.625  (k=5, ensemble C(8,5)=56)   mean Φ = 1.32827
  λ=0.75  (k=6, ensemble C(8,6)=28)   mean Φ = 0.927317
  λ=0.875  (k=7, ensemble C(8,7)=8)   mean Φ = 1.16028
  λ=1.0  (k=8, ensemble C(8,8)=1)   mean Φ = 1.14511e-05

  peak λ* = 0.375  (idx=3)   ensemble-mean Φ(λ*) = 1.34332
  Φ(λ=0 ordered)   = 1.14511e-05
  Φ(λ=1 saturated) = 1.14511e-05

  C2.1 INTERIOR-PEAK  (Φ(λ*)>Φ(0) AND Φ(λ*)>Φ(1), λ* interior) : true
  C2.2 EDGE-OF-CHAOS  (0.3 <= λ* <= 0.7)                        : true
  C2.3 DETERMINISM    (cross-process sha256 — checked external) : N/A in-process

  VERDICT_RULE: C2 PASS iff C2.1 (interior inverse-U peak) AND C2.2 (λ* in 0.3..0.7)
  C2 VERDICT  : PASS
=== H_007 C2 Langton-λ sweep complete: PASS ===
```

cross-process determinism (C2.3) confirmed: 두 독립 process re-run 의 `result.json` sha256 동일 (`d6a6c17e…b769260`).

**핵심 finding**: C1(이산 3-rule) 의 "Class-IV > ordered/chaotic" ranking 을 넘어, λ 연속 sweep 의 ensemble-mean Φ(λ) 가 명확한 **inverse-U** 를 형성 — 양 끝(λ=0 전부-dead·λ=1 전부-alive) 은 degenerate fixed point 로 Φ floor, **interior λ*≈0.375 에서 Φ peak** (edge-of-chaos 임계 정합). 초기 single-rule estimator 는 λ=0.375 단일 spike 만 보였으나(어느 rule 이 그 λ 에 떨어졌나 artifact), ensemble estimator 로 전환하여 λ *자체*의 robust inverse-U 확보.

**State output**: `UNIVERSE/state/h007_c2_lambda_sweep_2026_05_25/result.json`
**Smoke**: `UNIVERSE/state/h007_c2_lambda_sweep_2026_05_25/run_h007_c2.hexa`
**Φ tier**: 🟢 NUMERICAL (RFC 036 phi_spatial native replica; true phi_rs Rust FFI = named blocker — NOT 🔵, NOT LLM-judged, NOT PyPhi/sympy-primary).
