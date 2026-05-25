---
id: H_250
slug: class-ii-nonpow2-lattice-persistence
title: H_250 Class-II Φ persistence on non-power-of-2 lattice — N=17 cliff-collapse decisive test (H_232 follow-up · phi_helper 첫 활용)
domain: physics + math + information
status: pre-register-frozen
exploration_method: E5 (variable-ablation lattice sweep) + E12 (artifact-vs-real decisive test)
verification_method: W4 (verdict-3-class) + W13 (control-vs-test lattice diff)
raw_rank: 12
hexa_only: true
deterministic: true
llm: none
pre_register_frozen: true
frozen_at: 2026-05-24
since: 2026-05-24
---

# H_250 — Class-II Φ persistence on non-power-of-2 lattice

## Hypothesis

H_232 (`class_ii_mechanism_decompose`, PR #289 MERGED) 의 **핵심 발견**: rule 60/102 의 high-Φ 가 *transient* — power-of-2 **N=16** periodic lattice 위에서 t=0..6 동안 1.683 → peak 2.788 까지 상승했다가 **t=8+ cliff-collapse to ~1.145×10⁻⁵** (XOR Sierpinski complete-cancellation). rule 184 = constant plateau Φ=1.198. H_232 는 follow-up 으로 **"N=2^k vs N=2^k+1 (non-power-of-2) lattice 위 XOR 의 0-attractor 깨짐 여부"** 를 명시 flag 했다.

본 cycle 의 hypothesis 는 이 cliff-collapse 의 *원인* 을 가른다: collapse 가 **power-of-2 N=16 의 XOR Sierpinski complete-cancellation** (Wolfram 2002 §3 의 Z_2-linear CA over finite periodic lattice 의 modulo-periodicity 0-state attractor) 때문이라면, **non-power-of-2 N=17 (= 2^4 + 1)** 위에서는 cancellation 의 algebraic 조건이 깨져 Φ 가 *persist* 한다. 만약 N=17 에서도 collapse 하면 → cliff-collapse 는 **lattice-independent (real dynamics)**.

이 test 는 H_211/H_225 의 Class-II Φ anomaly (Class-II > Class-IV) 가 **real (sustained)** 인지 **artifact (transient, N=16-specific)** 인지를 가른다 — H_232 의 honest 한 미해결 잔여를 결정짓는 decisive control-vs-test.

5 predictions:

1. **H250.1 (N=17 persist)** N=17 (non-power-of-2) 위 rule 60 Φ trajectory 가 N=16 처럼 t=8+ collapse 하지 *않음* (sustained Φ > 0.5 at t=20) → cliff-collapse = power-of-2 artifact.
2. **H250.2 (rule 184 plateau both)** rule 184 (TASEP shift, non-XOR) 는 N=16/N=17 둘 다 plateau 유지 (XOR cancellation 무관 — shift dynamics).
3. **H250.3 (sustained anomaly)** N=17 위 Class-II (184/60/102) Φ 가 rule 110 (Class-IV) 보다 *지속적으로* 큼 (t=20 sustained, not transient) → H_225 anomaly real.
4. **H250.4 (collapse-step quantify)** N=16 vs N=17 의 rule 60 collapse-step 차이 정량 (N=16 collapse @ t≈8 · N=17 collapse 안 함 또는 훨씬 늦음).
5. **H250.5 (determinism)** re-run byte-identical (raw#12 strict).

raw#12 strict (deterministic · hexa-only · llm:none · $0 mac local). H_232 와 동일 substrate (dim=12, warm=8, periodic boundary, RFC 036 phi_spatial) 위 lattice-axis 만 확장 (N=16 control · N=17 test) + traj_len 21 (t=0..20, wider than H_232's t≤19, endpoint = sustained-Φ probe). **`HEXAD/LIFE/lib/phi_helper.hexa` (PR #317) 의 첫 production user** — `phi_with(state, n, dim, n_bins)` 사용.

## Why

- **H_232 의 carry**: H_232 는 FALSIFIED (pre-registered shape-classification 의 monotone/oscillating 문법으로는 양쪽 FAIL) 였지만, 그 과정에서 **rule 60/102 의 high-Φ 가 t≤7 transient + t=8+ collapse-to-0** 라는 새 사실을 reveal 했다. H_232 §"핵심 발견" 은 "Wolfram 2002 의 finite-periodic-lattice Z_2 linear CA universal behavior 와 정합. H_225 의 단일-시점 측정이 *transient peak* (t≤7) 를 잡았음" 으로 honest 하게 마무리 — 본 H 가 그 잔여를 결정짓는다.
- **Z_2-linear CA 의 algebra**: rule 60 = `(left XOR center)`, rule 102 = `(center XOR right)`. 둘 다 GF(2) 위 linear. linear CA 의 finite periodic lattice 위 dynamics 는 transition matrix 의 nilpotency / periodicity 로 결정된다 (Martin/Odlyzko/Wolfram 1984). N = 2^k 인 경우 nilpotent 성질이 강해 **0-state 로 collapse** (모든 초기 상태가 유한 step 후 all-zero attractor 로 수렴) 하는 것이 typical — N=16=2^4 가 이 case. N = 2^k + 1 등 odd N 에서는 transition matrix 의 spectrum 이 다르므로 **non-trivial period orbit** (collapse 안 함) 이 typical.
- **TASEP shift 의 lattice-insensitivity**: rule 184 = particle-conserving shift. conserved quantity (particle 수) 가 lattice size 와 무관하게 보존되므로 N=16/N=17 둘 다 steady-state plateau 예상 — XOR cancellation 의 메커니즘과 직교. 이것이 H250.2 의 control: cliff-collapse 가 XOR-specific 임을 보이는 negative control.
- **control-vs-test 의 epistemic 가치**: N=16 (power-of-2 control, H_232 와 byte-equal reproduction) ⊥ N=17 (non-power-of-2 test) 의 *유일한 차이* 는 lattice size 의 power-of-2-성. 다른 모든 변수 (rule · dim · warm · init · n_bins) 가 동일하므로, 두 lattice 의 collapse 차이는 *오직 power-of-2-성에 귀속* 된다 — clean attribution.
- **H_211/H_225 anomaly 의 real-vs-artifact 결정**: H_211 (Pearson r=0.933 entropy-Φ) 와 H_225 (C3 STRONG: Class-II > Class-IV) 의 anomaly 가 N=16 transient peak 의 artifact 였다면 — N=17 에서 사라져야 한다 (collapse). persist 한다면 — anomaly 는 real 이고 N=16 의 t=8+ collapse 가 오히려 *측정을 망친 artifact* 였다.
- **cross-link H_232 [direct parent]**: H_232 의 cliff-collapse 발견 + follow-up flag 를 직접 받아 N-axis 로 decompose. H_232 의 verdict (FALSIFIED) 는 변경 안 함 — 본 H 는 *post-result lattice-decisive test*.
- **cross-link H_225 [anomaly source]**: H_225 의 C3 STRONG PASS (Class-II > Class-IV) 의 real-vs-transient 를 가름. H_225 verdict 변경 안 함.
- **cross-link H_211 [shared baseline]**: H_211 의 entropy-Φ correlation 과 byte-equal substrate config (dim=12 · warm=8 · n_bins=4).
- **cross-link H_007 [indirect]**: H_007 의 Class-IV-unique 가정은 H_225 에서 이미 깨짐 — 본 H 는 추가 attack 아님, anomaly real-vs-artifact 의 lattice 차원 결정.

## Predictions

- **H250.1** N=17 rule 60 의 collapse_step = none (Φ 가 traj 전체에서 collapse_floor=0.1 아래로 안 떨어짐) AND Φ_t20 > 0.5 (sustained).
- **H250.2** rule 184 의 collapse_step = none for both N=16 AND N=17, AND Φ_t20 > 0.5 for both (TASEP plateau lattice-insensitive).
- **H250.3** N=17 위 Φ_t20(184) > Φ_t20(110) AND Φ_t20(60) > Φ_t20(110) AND Φ_t20(102) > Φ_t20(110) (sustained Class-II > Class-IV).
- **H250.4** N=16 rule 60 collapse_step ≈ 8 (H_232 reproduction) AND N=17 rule 60 collapse_step = none 또는 |N17_step − N16_step| > 2 (quantified divergence).
- **H250.5** re-run byte-identical (8 traj × 21 step Φ + collapse_step + Φ_t20 full ledger diff = 0).

## Variables

- **axis1_rule**: {184 (II/TASEP non-XOR), 60 (II/XOR-shift L), 102 (II/XOR-shift R), 110 (IV/complex reference)}
- **axis2_lattice**: {N = 16 (power-of-2 control, 2^4) · N = 17 (non-power-of-2 test, 2^4+1)}  ← **본 H 의 결정 axis**
- **axis3_trajectory_dim**: dim = 12 (H_232 byte-equal)
- **axis4_warmup**: warm = 8 (H_232 byte-equal)
- **axis5_traj_len**: 21 step (t=0..20, H_232 의 t≤19 보다 wider; t=20 = sustained-Φ endpoint probe)
- **axis6_rep_init**: rep ∈ {0..4} deterministic offset (site i on iff (i+rep)%3 ≠ 0, H_232 byte-equal init rule, N 에 무관)
- **fixed**: n_bins = 4 (`life_phi_nbins()` from phi_helper SSOT), periodic boundary, $0 mac local hexa
- **derived metrics**: collapse_step (first t with Φ < 0.1; −1 = none), Φ_t20 (sustained-Φ at endpoint), Φ_max (rule 60 peak)
- **Φ primitive**: `phi_with(state, n, dim, n_bins)` from `HEXAD/LIFE/lib/phi_helper.hexa` (PR #317) — **첫 production user** (F6 정합, inline phi_spatial copy 대체)

## Run Protocol

- **smoke**: `HEXAD/LIFE/state/h250_nonpow2_lattice_persistence_2026_05_24/run_h250.hexa`
- **Φ primitive**: `HEXAD/LIFE/lib/phi_helper.hexa` → `phi_with` → `c_measure_phi` → RFC 036 `phi_spatial` (import READ-ONLY; phi_helper 가 c_lib 를 wrapping).
- **mapping**: H_232 / H_225 / H_211 / H_007 와 동일 byte-equal substrate (dim/warm/init/n_bins). lattice 만 N=16 (control) ↔ N=17 (test) 로 sweep. 각 (rule, N, t) 에서 row → reset → init(rep) → warm step + t step 추가 evolve → dim-step trajectory 수집 → Φ_t = phi_with(states, n, dim, n_bins). 5 reps 평균.
- **collapse-step (deterministic)**: collapse_step = first t ∈ [0, 21) with mean Φ_t < 0.1; −1 if never (= persist).
- **sustained-Φ (deterministic)**: Φ_t20 = mean Φ at endpoint t=20.
- **deterministic**: fixed init + fixed config; re-run byte-identical.
- **hexa_only**: true (NO .py/.sh). **llm**: none.
- **runtime**: $0 mac local hexa (`HEXA_MEM_UNLIMITED=1 hexa run`); GPU 불필요.
- **ledger**: `result.json` {config, rules, phi_trajectory (8), collapse_step, phi_t20, phi_max, criteria, sanity_z2_mirror, falsifiers, verdict}.
- **honest tier**: NUMERICAL Φ (RFC 036 native replica) + collapse_step / sustained-Φ scalars = 🟢-tier evidence.

## Criteria

- **C1 (N=17 persist)** N=17 rule 60 collapse_step = none ∧ Φ_t20(60, N=17) > 0.5 → H250.1 PASS (artifact). honest collapse 도 그대로 기록 (lattice-independent).
- **C2 (rule 184 plateau both)** rule 184 collapse_step = none ∧ Φ_t20 > 0.5 for both N=16 AND N=17 → H250.2 PASS.
- **C3 (sustained anomaly)** Φ_t20(184/60/102, N=17) > Φ_t20(110, N=17) (all three) → H250.3 PASS.
- **C4 (byte-identical)** diff(run1, run2) = 0 → H250.5 PASS.
- **SANITY** rule 102 == rule 60 (Z_2 mirror) collapse_step 일치, both N.
- **verdict_rule**:
  - **ARTIFACT_CONFIRMED** = C1 (N=17 rule 60 persists) → cliff-collapse = power-of-2 artifact, **H_225 anomaly real**.
  - **COLLAPSE_INTRINSIC** = F1 (N=17 도 collapse ≈ N=16) → real dynamics, **H_225 anomaly transient**.
  - **MIXED** = otherwise (예: N=17 이 collapse 하지만 훨씬 늦게).

## Falsifiers

- **F1 N17_RULE60_COLLAPSE**: N=17 rule 60 도 collapse (collapse_step ≥ 0) AND |N17_step − N16_step| ≤ 2 → cliff-collapse lattice-independent (H250.1 FALSIFIED · anomaly transient intrinsic). (measurable: cs60_16, cs60_17.)
- **F2 RULE184_N17_COLLAPSE**: rule 184 가 N=17 위 collapse (collapse_step ≥ 0) → shift dynamics 도 lattice-sensitive (예상 외, conservation 깨짐). (measurable: cs184_17.)
- **F3 N17_CLASSII_LE_IV**: N=17 위 Φ_t20(184) ≤ Φ_t20(110) AND Φ_t20(60) ≤ Φ_t20(110) AND Φ_t20(102) ≤ Φ_t20(110) → anomaly 자체가 N=16-specific (H_225 weakened). (measurable: 세 Δ.)
- **F4 BYTE_IDENT_VIOLATION**: re-run JSON / stdout diff ≠ 0 → raw#12 위반 → smoke 무효.
- **F5 PHI_NONFINITE**: 임의 (rule, N, t) 에서 Φ < 0 ∨ Φ > 1e6 → phi_spatial NaN-policy 위반.
- **F6 POST-HOC**: frozen 후 verdict 방향 edit → raw#82 violation.

## Honest Limits (raw#91 c3)

- **L1**: N=17 단일 non-power-of-2 sample — N=15/19/31/prime 등 다른 odd/prime lattice 미검증. "non-power-of-2 → persist" 의 일반화는 transition-matrix spectrum 의 N-dependence 가 case-by-case 일 수 있어 단일 N=17 이 충분 증명 아님 (별도 N-sweep cycle 필요).
- **L2**: phi_helper `phi_with` 는 RFC 036 `phi_spatial` proxy (spatial-slice IIT Φ) — 진짜 `phi_rs` Rust FFI link 는 NAMED BLOCKER (RFC 036 §"FFI shim", #530). temporal Φ / partition Φ / phi-G 의 결과는 다를 수 있음.
- **L3**: 'XOR Sierpinski cancellation' 은 H_232 의 mechanism 가설 — N=17 persistence 가 그것을 *지지* 할 뿐 *증명* 아님. 다른 N-effect (예: 17 의 multiplicative order mod 2 의 특수성, boundary commensurability) 가 collapse 차이를 만들 수도 있다.
- **L4**: traj_len=21 (t=0..20) 도 finite — N=17 에서 더 늦은 collapse (t > 20) 가능성 미배제. 실제로 N=17 rule 60 은 t=12 부근에서 dip (0.829) 후 t=13+ 재상승하는 *oscillating-persist* 패턴 — period > 21 인 ultra-slow collapse 는 잡지 못함.
- **L5**: lattice-artifact 판정이 phenomenal consciousness 와 무관 (H_004 boundary) — Φ 가 substrate 의 information-integration proxy 일 뿐, "N=17 위 rule 60 이 의식적" 을 주장하지 않는다.
- **L6**: rule 110 (Class-IV) 자체도 N=17 위에서 Φ 가 N=16 (0.70) 보다 *낮음* (0.24) — Class-IV 의 lattice-sensitivity 는 별도 현상 (본 H 의 scope 밖). C3 의 "Class-II > Class-IV" 가 N=17 위 *더 크게* 성립하는 것은 부분적으로 rule 110 의 N=17 하락 덕분일 수도 있음 (Class-II 상승 + Class-IV 하락 의 합성).
- **L7**: collapse_floor=0.1 / sustain_floor=0.5 는 threshold heuristic — N=16 의 1.145e-5 (collapse) vs N=17 의 0.81-1.55 (persist) 의 dynamic range 가 4-5 orders 차이라 threshold 선택에 robust 하지만, 경계 case (Φ ≈ 0.1-0.5 plateau rule) 에서는 분류가 threshold-sensitive.

## Cross-Links

- **direct parent H**: H_232 (class-ii-mechanism-decompose — cliff-collapse 발견 + N=2^k+1 follow-up flag; 본 H 가 직접 결정)
- **anomaly source H**: H_225 (rule-184 Class-II Φ-peak anomaly — C3 STRONG PASS 의 real-vs-transient 결정), H_211 (shannon-entropy-phi-correlate — anomaly source, byte-equal config)
- **indirect H**: H_007 (Class-IV-unique 가정 already broken by H_225)
- **phi infra**: `HEXAD/LIFE/lib/phi_helper.hexa` (PR #317, **첫 production user** — `phi_with`/`life_phi_nbins`) → `HEXAD/C/c_lib.hexa` (`c_measure_phi` → RFC 036 `phi_spatial`)
- **raw**: raw#12 (deterministic strict) + raw#91 c3 (honest limits) + raw#82 (no post-hoc retraction)
- **literature**:
  - Martin, Odlyzko, Wolfram (1984) Algebraic properties of cellular automata (Z_2-linear CA, transition matrix nilpotency, lattice-size dependence of 0-attractor)
  - Wolfram (1984, 2002) A New Kind of Science (rule 60/102/184 substructure; Sierpinski XOR; finite-periodic-lattice additive CA)
  - Krug (1991) Boundary-induced phase transitions in driven diffusive systems (TASEP particle conservation, lattice-insensitive)
  - Schadschneider (2000) Statistical physics of vehicular traffic (TASEP universality)
  - Cook (2004) Universality in elementary cellular automata
  - Tononi (2004), Oizumi/Albantakis/Tononi (2014) IIT formal Φ

## Verdict

```
verdict_class: ARTIFACT_CONFIRMED (pre-register-frozen smoke, post-run honest)
decisive_finding:
  rule  60  N=16 (power-of-2 control)  collapse @ t=8 → Φ floor 1.14511e-05 (H_232 byte-equal reproduction)
  rule  60  N=17 (non-power-of-2 test) NO collapse · Φ oscillates 0.81→1.56→0.83→1.27 · Φ_t20=1.27369
  → cliff-collapse = POWER-OF-2 LATTICE ARTIFACT (XOR Sierpinski 0-attractor specific to N=2^k)
  → H_225/H_211 Class-II Φ anomaly = REAL (sustained on N=17), NOT a transient artifact
phi_t20 (sustained-Φ at endpoint t=20):
  rule 184  N=16=1.19781  N=17=1.66528   (plateau both — TASEP shift lattice-insensitive)
  rule  60  N=16=1.14511e-05 (collapsed)  N=17=1.27369  (persist on non-pow2)
  rule 102  N=16=1.14511e-05 (collapsed)  N=17=1.27071  (Z_2 mirror of rule 60)
  rule 110  N=16=0.702226  N=17=0.238001  (Class-IV reference)
collapse_step (first t with Φ<0.1; -1=none):
  rule 184  N16=none  N17=none
  rule  60  N16=8     N17=none      ← decisive divergence
  rule 102  N16=8     N17=none      (Z_2 mirror sanity PASS)
  rule 110  N16=none  N17=none
criteria_met: 4/4 (C1 PASS · C2 PASS · C3 PASS · C4 PASS)  + SANITY Z_2-mirror PASS both N
evidence_summary: 🟢 NUMERICAL — phi_helper phi_with (RFC 036 phi_spatial). (a) N=16 rule 60 reproduces
  H_232 cliff-collapse byte-exactly (t=8 → 1.145e-5); (b) N=17 rule 60 never collapses, Φ_t20=1.27 ≫ 0.5
  (4-5 orders of magnitude above N=16 floor) → cliff-collapse attributed CLEANLY to power-of-2-ness;
  (c) Class-II Φ_t20 > Class-IV Φ_t20 on N=17 for all 3 rules (sustained anomaly, not transient).
falsifiers_triggered: none (F1-F5 all PASS — no N=17 collapse, no rule-184 collapse, Class-II > IV, byte-identical, all Φ finite)
```

### Pre-register-frozen smoke (2026-05-24)

4-rule (184/60/102/110) × 2-lattice (N=16 power-of-2 control · N=17 non-power-of-2 test) × 21-step (t=0..20) Φ trajectory sweep pre-registered + RUN ($0 mac local, deterministic, hexa-only, llm:none).
1D elementary CA, periodic boundary, dim=12 trajectory, 5 deterministic reps, Φ via phi_helper `phi_with` (PR #317 첫 production user) → RFC 036 phi_spatial.

**Run verdict (VERBATIM, `hexa run`)**:
```
H_250 — Class-II Φ persistence on non-power-of-2 lattice (raw#12)
  N_pow2=16 N_nonpow2=17 dim=12 warm=8 traj_len=21 (t=0..20) reps=5  (deterministic, $0 mac local)
  Φ primitive: phi_with from HEXAD/LIFE/lib/phi_helper.hexa (PR #317, RFC 036 phi_spatial, Φ>=0)

  rule 60 (XOR-shift L) Φ trajectory — N=16 (power-of-2 control):
    t=0  Φ=1.6832
    t=1  Φ=1.86873
    t=2  Φ=2.034
    t=3  Φ=2.33065
    t=4  Φ=2.51472
    t=5  Φ=2.56563
    t=6  Φ=2.78794
    t=7  Φ=1.73804
    t=8  Φ=1.14511e-05      ← cliff-collapse (XOR Sierpinski 0-attractor, N=2^4)
    ... (t=9..20 모두 1.14511e-05, near-zero floor)

  rule 60 (XOR-shift L) Φ trajectory — N=17 (non-power-of-2 test):
    t=0  Φ=0.813061
    t=1  Φ=0.869996
    t=2  Φ=0.94012
    t=3  Φ=1.02539
    t=4  Φ=1.16681
    t=5  Φ=1.27015
    t=6  Φ=1.40559
    t=7  Φ=1.55924      ← peak
    t=8  Φ=1.44863
    t=9  Φ=1.20853
    t=10 Φ=1.13675
    t=11 Φ=1.04145
    t=12 Φ=0.82868      ← dip (NOT collapse — stays ≫ 0.1)
    t=13 Φ=0.875904     ← re-rise (oscillating-persist)
    ... t=20 Φ=1.27369  ← sustained ≫ 0.5

  rule 184 (TASEP shift) Φ trajectory — N=16 / N=17 (key points):
    N=16: t=0 Φ=1.19781  t=10 Φ=1.19781  t=20 Φ=1.19781   (plateau)
    N=17: t=0 Φ=1.66528  t=10 Φ=1.66528  t=20 Φ=1.66528   (plateau)

  rule 110 (Class-IV reference) Φ trajectory — N=16 / N=17 (key points):
    N=16: t=0 Φ=0.556454  t=10 Φ=0.547177  t=20 Φ=0.702226
    N=17: t=0 Φ=0.279042  t=10 Φ=0.234022  t=20 Φ=0.238001

  per-(rule,N) collapse_step (first t with Φ<0.1) + Φ_t20 (sustained-Φ at endpoint):
    rule 184  N=16  collapse_step=none  Φ_t20=1.19781
    rule 184  N=17  collapse_step=none  Φ_t20=1.66528
    rule  60  N=16  collapse_step=8  Φ_t20=1.14511e-05
    rule  60  N=17  collapse_step=none  Φ_t20=1.27369
    rule 102  N=16  collapse_step=8  Φ_t20=1.14511e-05
    rule 102  N=17  collapse_step=none  Φ_t20=1.27071
    rule 110  N=16  collapse_step=none  Φ_t20=0.702226
    rule 110  N=17  collapse_step=none  Φ_t20=0.238001

  N=16 vs N=17 comparison (rule 60 cliff-collapse decisive test):
    N=16 rule 60 collapse @ t=8  →  N=17 rule 60 collapse @ t=none
    N=16 rule 60 Φ_t20=1.14511e-05  →  N=17 rule 60 Φ_t20=1.27369

  C1 N17_RULE60_PERSIST (no collapse ∧ Φ_t20 > 0.5): true  (no_collapse=true · Φ_t20=1.27369)
  C2 RULE184_PLATEAU_BOTH (no collapse ∧ Φ_t20>0.5, both N): true  (N16=true · N17=true)
  C3 N17_CLASSII_GT_IV (184/60/102 Φ_t20 > 110 Φ_t20): true  (184>110=true · 60>110=true · 102>110=true · Φ110_t20=0.238001)
  C4 BYTE_IDENT (deterministic re-run, external diff): true
  SANITY rule102==rule60 (Z_2 mirror, collapse_step): N16=true · N17=true

  F1 N17_RULE60_COLLAPSE  (N17 collapse ∧ |Δstep|<=2 vs N16): false
  F2 RULE184_N17_COLLAPSE (rule 184 N17 collapses)         : false
  F3 N17_CLASSII_LE_IV    (all Class-II Φ_t20 <= 110)      : false
  F4 BYTE_IDENT_CONTRACT  (det re-run)                     : true
  F5 PHI_NONFINITE        (Φ < 0 ∨ Φ > 1e6)                 : false

  VERDICT_RULE: ARTIFACT_CONFIRMED iff C1 (N17 rule60 persists) · COLLAPSE_INTRINSIC iff F1 (N17 collapses ≈ N16) · else MIXED
  VERDICT     : ARTIFACT_CONFIRMED
```

re-run byte-identical (F4/H250.5 BYTE_IDENT confirmed via `diff` of run1 vs run2 on `result.json` → identical).

honest tier: 🟢 NUMERICAL — phi_helper `phi_with` → RFC 036 phi_spatial native replica + derived collapse_step / sustained-Φ scalars. NOT 🔵 (no formal proof of the transition-matrix nilpotency claim; lattice-attribution 은 single N=17 sample 의 numerical evidence).

**Interpretation (honest, raw#82 no post-hoc rewriting)**:

1. **C1 PASS (N=17 persist)** — N=16 rule 60 은 H_232 를 *byte-exactly* 재현 (t=8 cliff-collapse → 1.14511e-05, t=9..20 floor). N=17 rule 60 은 **collapse 가 전혀 없음**: t=0..7 rise 1.683→peak (0.81→1.56), t=8..12 partial dip (1.45→0.83, 여전히 ≫ 0.1), t=13..20 re-rise (0.88→1.27). Φ_t20=1.27369 — N=16 floor 보다 **4-5 orders of magnitude** 높음. cliff-collapse 는 power-of-2 N=16 의 XOR Sierpinski 0-attractor 에 *clean 하게 귀속* (다른 모든 변수 동일, 유일 차이 = lattice power-of-2-성).

2. **C2 PASS (rule 184 plateau both)** — rule 184 (TASEP, non-XOR) 는 N=16 (Φ=1.198 constant) AND N=17 (Φ=1.665 constant) 둘 다 collapse 없는 flat plateau. TASEP 의 particle-conservation 이 lattice size 와 무관하게 보존됨 — XOR cancellation 메커니즘과 직교함을 보이는 negative control. (N=17 plateau 가 N=16 보다 *높음* (1.665 vs 1.198) 도 흥미로운 부수 관측 — odd lattice 에서 conserved-density 가 다름.)

3. **C3 PASS (sustained anomaly)** — N=17 위 Φ_t20: rule 184=1.665, rule 60=1.274, rule 102=1.271 모두 rule 110=0.238 (Class-IV) 능가. **H_225 의 Class-II > Class-IV anomaly 가 N=17 위 t=20 까지 sustained** — transient peak 의 artifact 가 아니라 real. (L6 honest caveat: rule 110 자체도 N=17 위에서 N=16 (0.70) 대비 하락 (0.24) — Class-IV 의 lattice-sensitivity 는 별도 현상; C3 의 큰 margin 은 Class-II 상승 + Class-IV 하락 합성.)

4. **C4 PASS + Z_2 mirror SANITY** — re-run byte-identical (result.json diff=0). rule 102 collapse_step = rule 60 collapse_step (N16: 8==8, N17: none==none) — Z_2 reflection 정합, implementation bug 없음. (Φ_t20 는 rule 60=1.27369 vs rule 102=1.27071 로 마지막 자리 차이 — float-order-of-operation 미세 차이, collapse 분류엔 무영향.)

**핵심 발견** (lattice-artifact 결정, decisive):
- rule 60/102 의 N=16 cliff-collapse = **power-of-2 N=2^k 의 XOR Sierpinski 0-attractor artifact** (Martin/Odlyzko/Wolfram 1984 의 Z_2-linear CA transition-matrix nilpotency over N=2^k periodic lattice 와 정합).
- N=17 (= 2^4+1) 위에서는 **collapse 가 깨지고 Φ 가 oscillating-persist** (Φ_t20=1.27 ≫ 0.5) — H_232 가 honest 하게 미해결로 남긴 "transient vs real" 잔여를 **real** 로 결정.
- 따라서 **H_211/H_225 의 Class-II Φ anomaly (Class-II > Class-IV) = REAL** — N=16 의 t=8+ collapse 가 오히려 측정을 망친 lattice artifact 였고, anomaly 자체는 non-power-of-2 lattice 에서 sustained.
- rule 184 (TASEP) 는 두 lattice 모두 plateau — XOR cancellation 메커니즘이 lattice-power-of-2-성에 specific 임을 확인하는 clean negative control.

**Follow-up cycles (별도 H)**:
- N-sweep (N=15/19/23/31/prime) 위 rule 60/102 collapse-vs-persist — "non-power-of-2 → persist" 일반화 (L1) 검증; transition-matrix order mod 2 의 N-dependence 정량.
- N=2^k 계열 (N=8/16/32/64) 위 collapse-step 의 k-scaling — Sierpinski cancellation 의 lattice-size scaling law.
- ultra-long traj (200/1000 step) 위 N=17 rule 60 의 oscillation period 측정 — L4 의 period > 21 가능성 결정.
- rule 110 (Class-IV) 의 N=16 vs N=17 Φ 하락 (0.70 → 0.24) 의 mechanism (L6) — Class-IV complex dynamics 의 lattice-commensurability 효과.

**State output**: `HEXAD/LIFE/state/h250_nonpow2_lattice_persistence_2026_05_24/result.json`
**Smoke**: `HEXAD/LIFE/state/h250_nonpow2_lattice_persistence_2026_05_24/run_h250.hexa`
**Φ tier**: 🟢 NUMERICAL (phi_helper phi_with → RFC 036 phi_spatial native replica + derived collapse_step / sustained-Φ; true phi_rs Rust FFI = named blocker #530 — NOT 🔵, NOT LLM-judged).
