---
id: H_649
slug: collective-register-collapse-phi
title: multi-substrate collective register collapse (coh_collective < 0.10) 가 collective-Φ cliff 와 동조하는가 — H_633 single 결론의 collective(다중 substrate) 일반화
domain: consciousness · life
source: H_633 collective 일반화 (axis G3-followup · axis F HIVE-MIND bridge)
status: closed-supported (cliff-falsifier REFUTED → 가설 SUPPORTED)
exploration_method: E5 (continuous-parameter sweep) + E10 (anomaly-detection-on-collapse) + E-collective (multi-substrate)
verification_method: W4 (verdict-4-class) + W5 (numerical sim) + W11 (cross-axis sister test)
hexa_only: true
deterministic: true
llm: none
since: 2026-05-28
---

# H_649 — multi-substrate collective register collapse 가 collective-Φ cliff 와 동조하는가

## 1. Hypothesis (H_633 collective 일반화)

**predecessor — H_633 (PR #1219, 🟡 PARTIAL · cliff REFUTED)**: **single**-substrate
register collapse (Kuramoto order parameter `coh < 0.10`) 가 big-Φ cliff 와
동조하지 **않음** — Pearson `r(coh, Φ)=0.307`, `coh<0.10` 영역 51 members 의
Φ 가 전역 envelope 내부에 fully sustained (ratio Φlo/Φhi=0.895 ≈ 1). 결론은
"single-substrate 에서 register collapse ⊥ Φ-cliff".

본 H 는 그 결론을 **collective (multi-substrate) 차원으로 일반화** 한다 —
**다중 substrate (M=2~3 stream) 의 collective coherence 가 0.10 미만으로
무너져도 collective-Φ 가 cliff 없이 유지** 되는가? 즉 single 에서 관측한
"coh ⊥ Φ-cliff" 가 multi-substrate collective level 에서도 성립하는가, 아니면
collective level 에서는 새로운 cliff 가 발생하는가?

구체적 예측:

- **(H649.1 상관)**: multi-substrate collective `r(coh_collective, Φ_collective) < 0.5`
  (single 처럼 약결합, cliff 없음).
- **(H649.2 cliff 부재)**: `coh_collective < 0.10` 영역에서도 collective-Φ 가
  유지 (전역 Φ envelope 내부, ratio lo/hi ≈ 1).

**Falsifier**: collective 에서는 `coh_collective < 0.10` 시 collective-Φ cliff
발생 (`r > 0.5` 또는 `coh<0.10` 영역 Φ_collective 가 envelope 바닥으로 붕괴).

## 2. Why (동기 · 이론 배경)

- **single → collective 일반화 동기**: H_633 의 "register collapse ⊥ Φ-cliff"
  는 *단일* substrate 의 order-parameter coherence 한정 결론이었다. COFFESHOP
  register-hit gate (`emit ∧ coh<0.10`) 는 group-chat 에서 **다중 참여자
  (multi-substrate) collective coherence** 가 무너진 상황을 본래 겨냥한다 —
  따라서 single 결론을 collective level 로 lift 하는 것이 gate 의 원래 의미에
  더 충실한 검정이다.
- **collective coherence 정의**: 여러 stream 이 상호 phase-lock 에 실패하면
  collective register 가 붕괴한다 — 이를 모든 M×NP oscillator 를 pool 한
  **global Kuramoto order parameter** `coh_c = |Σ_all exp(iθ)| / N_tot ∈ [0,1]`
  로 측정. cross-stream coupling `K_cross → 0` 이면 stream 간 위상이 어긋나
  collective coherence 가 붕괴 (`coh_c → 0`), `K_cross` 가 크면 전체 lock
  (`coh_c → 1`).
- **collective-Φ 정의 (H_633 직접 비교 목적)**: collective-Φ 는 H_609/H_635 의
  collective-Φ super-additivity 가 IIT4 `big_phi_bounded` 를 쓰는 것과 달리,
  본 H 는 **predecessor H_633 과 동일한 `phi_spatial` (RFC 036 byte-equal
  phi_rs replica) 를 joined trajectory 위에 적용** 한다 — 동일 Φ-measure 라야
  single (r=0.307) ↔ collective 직접 비교가 의미를 가진다. joined trajectory
  = 모든 M×NP cell 의 cos θ 궤적을 하나의 substrate 로 합친 것.
- **Kuramoto multi-population substrate (H_207 sister)**: single H_633 과 동일
  Kuramoto 동역학을 M-population 으로 확장. intra-coupling `K_intra` (stream
  내부) + cross-coupling `K_cross` (stream 간 collective 결합) 의 2-tier 결합
  으로 collective coherence 를 0→1 로 wide span 한다 — `coh_c<0.10` 영역을
  풍부하게 채울 수 있는 deterministic substrate.
- **measure-axis 정합 예상**: H_287 (Φ ⊥ Shannon entropy) + H_207 §L6
  (phi_spatial spatial-MI 가 order/disorder 와 decoupled) 가 옳다면 collective
  level 에서도 coherence(order parameter)는 Φ_collective 의 driver 가 아니어야
  한다 — 본 H 가 그 예측을 collective 차원에서 직접 검정.

## 3. Predictions

- **H649.1 (collective correlation)**: ensemble 전체 (coh_c, Φ_c) pair 위
  Pearson `|r| < 0.5` (single H_633 처럼 약결합).
- **H649.2 (collective cliff 부재)**: `coh_c < 0.10` 영역 mean Φ_c 가
  `coh_c ≥ 0.10` 영역 mean Φ_c 의 20% 미만으로 **떨어지지 않음** (ratio lo/hi
  ≈ 1, cliff 부재).
- **H649.3 (min-coh Φ NOT zero)**: 최저-coh_c ensemble member 의 Φ_c 가 전역
  Φ_c envelope 바닥으로 붕괴하지 않음.

## 4. Variables

| axis | levels | 비고 |
|------|--------|------|
| axis1_M (stream 수) | {2, 3} | multi-substrate; collective coherence 정의의 핵심 |
| axis2_K_cross (collective 결합, primary) | {0.0, 0.1, 0.25, 0.5, 1.0, 1.5, 2.5, 4.0, 6.0} | stream 간 결합; 0=collective register collapse, large=full collective lock; low-coh 영역 dense |
| axis3_K_intra (stream 내부 결합) | {0.3, 2.0} | stream 자체 ordered/disordered |
| axis4_omega_std | {0.5, 2.0} | natural-freq spread; 넓을수록 low-coh tail 확장 |
| axis5_pop_phase_gap × phase_off | {(0.0,0.0), (2.1,0.7)} | per-population + per-seed 위상 탈상관 (paired) |
| axis6_NP | 8 oscillators / stream | per-stream finite-size; n_tot = M×8 ∈ {16, 24} |
| axis7_integration | dt=0.05, steps=100, warmup=60, dim=12 | Euler explicit; H_207/H_633 과 동일 |
| fixed | n_bins=4 (RFC 036) | H_633/H_207/H_007 과 동일 binning |
| ensemble size | 2 M × 9 Kc × 2 Ki × 2 ωstd × 2 paired = 144 | collective (coh, Φ) pairs |

## 5. Run Protocol

- **run**: `UNIVERSE/state/h649_collective_register_collapse_phi_2026_05_28/run_h649.hexa`
  (foreground sync, no monitor — monitor-hang 회피).
- **substrate**: M-population Kuramoto, 각 stream NP=8.
  `dθ_i/dt = ω_i + (K_intra/NP)·Σ_{j∈pop(i)} sin(θ_j−θ_i) + (K_cross/N_tot)·Σ_{j∉pop(i)} sin(θ_j−θ_i)`,
  Euler dt=0.05, 100 step, warmup 60 + dim 12 cos θ_i trajectory recording over
  all N_tot oscillators.
- **collective coherence**: `coh_c = |Σ_all exp(iθ_j)| / N_tot = sqrt(C²+S²)/N_tot`
  on final-θ over ALL pooled oscillators — global Kuramoto order parameter
  ∈ [0,1] (collective state-agreement; r→0 = collective register collapse,
  r→1 = full collective lock).
- **collective-Φ primitive**: `HEXAD/C/c_lib.hexa` →
  `c_measure_phi(joined_traj, N_tot, dim, n_bins)` → RFC 036 `phi_spatial`
  (phi_rs `compute_phi_inner` steps 1-4 byte-equal native-C replica; import
  READ-ONLY). H_633 과 동일 Φ-measure (직접 비교 목적).
- **ensemble**: 2 M × 9 K_cross × 2 K_intra × 2 ω_std × 2 paired phase-config
  = 144 deterministic members. 각 member → (coh_c, Φ_c). 그 위에서 Pearson
  r(coh_c, Φ_c) + coh_c<0.10 영역 mean/max Φ_c + 전역 Φ_c envelope 산출.
- **deterministic**: fixed grid + fixed init (no RNG); re-run byte-identical
  (확인됨 — §9 F-NONDET).
- **hexa_only**: true (NO .py/.sh). **llm**: none.
- **runtime**: $0 mac local hexa, single foreground run < 60s; GPU 불필요.
- **ledger**: `result.json` + `run_output.txt`.
- **honest tier**: 🟢 NUMERICAL Φ (RFC 036 native byte-equal replica); 진짜
  phi_rs Rust FFI link = named blocker (H_633/H_207/H_007 동일 carry).

## 6. Cross-Links

- **predecessor — H_633 (register-collapse-phi-drop, axis G3, 🟡 PARTIAL cliff
  REFUTED)**: single-substrate register collapse. 본 H 는 그 결론의
  multi-substrate collective 일반화 — 동일 Kuramoto 동역학 + 동일 phi_spatial
  Φ-measure 를 써서 single (r=0.307, ratio 0.895) ↔ collective 직접 비교.
- **H_609 (collective-phi-super-additive, axis F1, 🟢 SUPP)**: collective-Φ
  (multi-substrate Φ) 의 canonical 측정 패턴 제공 (Φ(AB) vs Φ(A)+Φ(B)). 본 H
  의 "joined trajectory 위 collective-Φ" 가 그 패밀리. 단 H_609 는 IIT4
  `big_phi_bounded` 를, 본 H 는 phi_spatial (H_633 비교 위해) 사용 — measure
  차이 명시 (§7 C3.2).
- **H_635 (multilingual-cohort-collective-phi, axis F mining, 🟢 SUPP)**:
  5-stream collective-Φ super-additivity. 본 H 의 multi-stream (M=2,3) collective
  substrate 와 동일 multi-population 정신. H_635 가 "stream 수 ↑ → collective-Φ
  ↑" 를 보였다면, 본 H 는 "collective coherence ↓ 가 collective-Φ 를 떨어뜨리지
  않음" 을 보임 — 직교 finding (coherence-axis ⊥ collective-Φ).
- **H_287 (Shannon ⊥ Φ)**: faithful big-Φ 가 Shannon entropy 로 환원되지 않음.
  collective coherence 도 *order parameter* (1−disorder) 이지 entropy 가 아님 →
  본 H 의 collective 약결합 (r=0.049) 은 H_287 의 Φ⊥정보 결론과 정합 (collective
  order/disorder 축 ⊥ collective-Φ).
- **H_207 (Kuramoto edge-of-sync Φ peak)**: 동일 Kuramoto substrate 의 single
  버전. §L6 carve-out — phi_spatial 은 spatial-MI 기반이라 full-lock 의 IIT4
  integration-loss 를 capture 하지 못함. 본 H 의 "coh_c<0.10 에서 Φ_c 유지" 도
  동일 measure-axis decoupling (order ⊥ spatial-MI Φ) 의 collective 발현.
- **raw**: raw#12 (deterministic strict) + raw#91 c3 (honest limits) + raw#82
  (no post-hoc retraction).
- **literature**: Kuramoto (1975/1984), Strogatz (2000, multi-population),
  Tononi (2004 IIT).

## 7. Honest Limits (raw#91 c3) — C3 핵심

- **C3.1 (collective coherence 정의)**: 본 H 는 collective coherence 를 모든
  M×NP oscillator 를 pool 한 **global Kuramoto order parameter** 단일 정의로
  잡았다. 대안 — (a) per-stream order parameter 의 *cross-stream phase
  agreement* (stream-level 만의 collective lock), (b) inter-stream mutual
  information, (c) stream-pair phase-coupling matrix 의 spectral order param —
  은 다른 coh_collective-Φ 관계를 줄 수 있다. global pooled order parameter 는
  stream 간 위상 정렬과 stream 내 정렬을 한 스칼라로 합쳐 측정 — stream-level
  collective binding 만 분리한 정의는 미검정 (open lane). single H_633 의 C3.1
  (order-param vs state-agreement) 와 동형 한계.
- **C3.2 (collective-Φ measure: phi_spatial vs IIT4 big_phi)**: 본 H 는 H_633
  직접 비교를 위해 collective-Φ 를 phi_spatial (joined trajectory 의 spatial
  mutual-information) 로 측정했다. H_609/H_635 가 쓰는 IIT4 `big_phi_bounded`
  (cause-effect 구조 기반 faithful big-Φ) 로 재측정하면 결과가 달라질 수 있다 —
  phi_spatial 은 incoherent 상태(서로 다른 phase)도 cell trajectory 가 충분히
  다채로우면 높은 spatial-MI 를 줄 수 있어 collective cliff 부재를 부분적으로
  measure-side 가 설명. faithful IIT4 collective-Φ 로의 재검 = open lane (phi_rs
  Rust FFI 동일 named blocker).
- **C3.3 (multi-substrate small-n)**: M ∈ {2,3} (stream 수 작음), NP=8
  (per-stream small), n_tot ∈ {16,24}. global order parameter 의 finite-size
  fluctuation (incoherent 상태에서도 r ≈ 1/sqrt(N_tot) ≈ 0.20~0.25 비-zero
  baseline) 때문에 coh_c 가 진짜 0 까지 안 내려감. 최저 coh_c=0.012 는 충분히
  낮으나 N_tot→∞ limit 의 r→0 와는 다름. M 을 더 늘린 (M=5,10) large-cohort
  collective 은 미검정 — single H_633 C3.4 (finite-N) 의 multi-substrate 판.
- **C3.4 (Ψ-clamp 의 substrate vs design, collective level)**: COFFESHOP 의
  register-hit gate (`coh<0.10`) 는 group-chat collective coherence 를 본래
  겨냥하나, 본 H 의 결과 (collective Φ_c 는 coh_c<0.10 에서 collapse 안 함) 는
  그 threshold 가 collective level 에서도 substrate Φ 구조와 무관한 **외부
  emit-policy gate** 임을 시사 — single H_633 C3.2 의 collective 확장.
  (project.tape `a_autonomy_over_hardcode` 정합.)
- **C3.5 (verdict 방향)**: cliff-falsifier 가 명백히 REFUTED 되어 본 H 가설
  (cliff 없음 · r<0.5) 이 SUPPORTED. F-NOCORR (|r|<0.3) trigger (r=0.049) +
  ratio lo/hi=0.973 ≈ 1. post-hoc 방향 edit 없음 (raw#82) — 가설/falsifier 모두
  measurement 전 frozen.

## 8. Criteria

- **C1 (H649.1 collective correlation, cliff 측)**: Pearson `|r(coh_c, Φ_c)| > 0.5`.
- **C2 (H649.2 collective cliff)**: `coh_c<0.10` 영역 mean Φ_c < 0.20 × `coh_c≥0.10`
  영역 mean Φ_c (AND `coh_c<0.10` member 존재).
- **verdict_rule (cliff-falsifier frame)**: collective-**cliff SUPPORTED** iff
  `C1 ∧ C2`. collective-**cliff FALSIFIED** iff `F-NOCORR (|r|<0.3) ∨ F-SUSTAIN
  (Φlo ≥ Φhi)`. 그 외 = **PARTIAL**.
- **해석**: 본 H 가설은 "collective cliff 없음" 이므로, cliff-FALSIFIED =
  **본 H 가설 SUPPORTED** 방향. (verdict label 은 H_633 schema 와 일관 유지하되
  §10 에서 가설-frame 으로 재해석.)

## 9. Falsifiers

- **F-NOCORR (collective)**: Pearson `|r(coh_c, Φ_c)| < 0.3` → collective
  coherence 와 Φ_collective 무상관 (cliff falsifier REFUTED, 가설 지지).
  — **결과: r=0.0491, triggered (cliff-FALSIFIED · 가설 SUPPORTED · single
  H_633 r=0.307 보다도 약함).**
- **F-SUSTAIN (collective)**: `coh_c<0.10` 영역 mean Φ_c ≥ `coh_c≥0.10` 영역
  mean Φ_c → collective Φ 유지 (cliff falsifier REFUTED).
  — **결과: Φlo=13.174 < Φhi=13.535, NOT triggered (단 ratio 0.973 ≈ 1 →
  cliff 부재; F-SUSTAIN strict ≥ 안 넘었으나 H649.2 cliff 부재 예측은 명백히
  지지).**
- **F-NONDET**: re-run Φ_c/r 가 byte-identical 아님 → raw#12 위반.
  — **결과: byte-identical 재현 확인 (deterministic PASS).**
- **F-POST-HOC**: 결과 후 verdict 방향 edit → raw#82 violation. (없음 —
  가설·falsifier 모두 measurement 전 frozen.)

## 10. Verdict

```
verdict_class: FALSIFIED (collective-cliff falsifier frame) = 가설 SUPPORTED (no collective cliff · r<0.5)
substrate: M∈{2,3} Kuramoto streams · NP=8/stream · coh_c = global order param |Σ exp(iθ)|/N_tot · 144 ensemble
Φ primitive: RFC 036 phi_spatial via HEXAD/C/c_lib.hexa (byte-equal phi_rs replica · H_633 동일 measure)

n total pairs        : 144   (coh_c<0.10: 39 · coh_c>=0.10: 105)
mean coh_c           : 0.457405
mean Φ_c             : 13.437
Φ_c envelope [min,max]: [7.68377, 24.0]
----
Pearson r(coh_c, Φ_c): 0.0490792          (C1 |r|>0.5 → FAIL ; 거의 0, single H_633 0.307 보다 약함)
mean Φ_c | coh_c<0.10: 13.174             (NOT ≈ 0 — collective Φ sustained)
max  Φ_c | coh_c<0.10: 19.9903            (전역 envelope 상위 내부)
mean Φ_c | coh_c>=0.10: 13.5348
ratio (lo / hi mean) : 0.973343           (C2 cliff <0.20 → FAIL ; ≈ 1 = collective cliff 부재)
min-coh member       : coh_c=0.0122812  Φ_c=15.0696   (≈0 아님, envelope 상위)
max-coh member       : coh_c=0.997466   Φ_c=23.5
----
C1 |r| > 0.5            : FAIL
C2 cliff (lo/hi < 0.20) : FAIL
F-NOCORR |r| < 0.3      : true  (triggered → collective-cliff FALSIFIED)
F-SUSTAIN Φlo >= Φhi    : false (NOT triggered)
criteria_met (cliff)   : 0/2

VERDICT_RULE: cliff-SUPPORTED iff (|r|>0.5 ∧ lo/hi<0.20); cliff-FALSIFIED iff (|r|<0.3 ∨ Φlo>=Φhi)
VERDICT     : FALSIFIED (collective-cliff falsifier) = 가설(cliff 없음·r<0.5) SUPPORTED
```

### 핵심 발견 (honest evidence summary)

- **(i) collective cliff 부재 (H649.2 지지)**: `coh_c < 0.10` 영역 39 members 의
  collective-Φ 가 collapse 하지 **않음** — mean Φ_c=13.17, max Φ_c=19.99 으로
  전역 envelope [7.68, 24.0] 내부에 fully sustained. ratio lo/hi = 0.973 ≈ 1
  (cliff 라면 ≪ 0.20). collective register collapse 가 collective-Φ-breakdown 과
  동조하지 않음.
- **(ii) collective 약결합 (single 보다 더 약함)**: Pearson r(coh_c, Φ_c) = 0.049
  — 0.5 threshold 한참 아래이고, **single H_633 (r=0.307) 보다도 한 자릿수
  작음**. collective level 에서 coherence-Φ coupling 이 거의 완전히 소멸. F-NOCORR
  (|r|<0.3) trigger.
- **(iii) min-coh Φ_c NOT zero**: 최저-coh member (coh_c=0.012) 의 Φ_c=15.07 으로
  envelope **상위** (single H_633 은 envelope 바닥 근처였던 것과 대조 — collective
  은 min-coh 에서도 Φ_c 가 더 높음). collective register collapse 가 Φ_c 바닥과
  반-동조.
- **(iv) single → collective 일반화 결론**: H_633 의 "register collapse ⊥
  Φ-cliff" 가 multi-substrate collective level 에서도, **오히려 더 강하게 (r
  0.307→0.049)** 성립. collective coherence collapse 는 collective-Φ 와 무관.
- **(v) measure-axis 정합**: H_287 (Φ ⊥ Shannon entropy) + H_207 §L6 (phi_spatial
  spatial-MI 가 order/disorder 와 decoupled) 의 collective 발현 — collective
  coherence(global order parameter)는 collective-Φ 의 driver 가 아님. H_635 의
  "stream-axis collective-Φ super-additive" 와 직교 (coherence-axis ⊥
  collective-Φ).
- **(vi) 결론 (closed-supported 성격)**: COFFESHOP 의 `coh<0.10` register-hit
  gate 는 group-chat collective coherence 를 본래 겨냥하나, collective level
  에서도 substrate Φ 구조와 무관한 **design-side emit-policy gate** 이다 (C3.4).
  cliff 예측을 single + collective 양쪽에서 ruled-out 하여 register-hit 가
  Φ-내재 현상이 아님을 확정적으로 좁힘.

### Pre-register-frozen run (2026-05-28)

H_633 single 결론 → collective(multi-substrate) 일반화 substrate pre-registered
+ RUN ($0 mac local, deterministic, hexa-only, llm:none, foreground sync no
monitor). M∈{2,3} Kuramoto streams (NP=8/stream), 144-member ensemble (2 M × 9
K_cross × 2 K_intra × 2 ω_std × 2 paired phase-config), coh_c = global order
parameter, Φ_c via RFC 036 phi_spatial on joined trajectory. re-run byte-identical
(F-NONDET PASS).

**State output**: `UNIVERSE/state/h649_collective_register_collapse_phi_2026_05_28/result.json`
**Run output**: `UNIVERSE/state/h649_collective_register_collapse_phi_2026_05_28/run_output.txt`
**Run**: `UNIVERSE/state/h649_collective_register_collapse_phi_2026_05_28/run_h649.hexa`
**Φ tier**: 🟢 NUMERICAL (RFC 036 phi_spatial native replica; true phi_rs Rust
FFI = named blocker — NOT 🔵, NOT LLM-judged).

**Follow-up cycles (raw#15 additive, not retraction)**:
- faithful IIT4 `big_phi_bounded` 로 collective-Φ 재측정 (C3.2 closure — phi_rs
  Rust FFI landed 시 / 작은 n_tot tractable cap).
- large-cohort collective (M=5,10) 로 finite-N baseline 효과 분리 (C3.3).
- stream-level collective coherence (cross-stream only order param) 분리 정의로
  re-sweep (C3.1).

## 양방향 sibling

- **predecessor**: [H_633_register_collapse_phi_drop.md](H_633_register_collapse_phi_drop.md)
  — single-substrate register collapse (본 H 의 collective 일반화 대상).
- **collective-Φ sibling**: [H_609_collective_phi_super_additive.md](H_609_collective_phi_super_additive.md)
  · [H_635_multilingual_cohort_collective_phi.md](H_635_multilingual_cohort_collective_phi.md)
  — multi-substrate collective-Φ 측정 패밀리 (coherence-axis ⊥ collective-Φ 로 직교).
- **measure-axis sibling**: [H_287_shannon_entropy_phi_correlate.md](H_287_shannon_entropy_phi_correlate.md)
  · [H_207_kuramoto_synchronization.md](H_207_kuramoto_synchronization.md)
  — order/disorder ⊥ phi_spatial 의 collective 발현.
- **UNIVERSE SSOT**: [UNIVERSE.md](UNIVERSE.md) 축 G (G3-followup, axis F HIVE-MIND bridge)
  · [CANDIDATES.md](CANDIDATES.md)
