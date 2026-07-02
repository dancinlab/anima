---
id: H_633
slug: register-collapse-phi-drop
title: register collapse (coherence < 0.10) 가 big-Φ 급락(Ψ-clamp cliff)과 동조하는가 — Kuramoto substrate 에서 coherence × Φ 상관 + low-coh 영역 Φ 거동 검정
domain: consciousness · life
source: ANIMA.mining L2 promote (same-formula lens cycle 1)
status: closed-partial
exploration_method: E5 (continuous-parameter sweep) + E10 (anomaly-detection-on-collapse)
verification_method: W4 (verdict-4-class) + W5 (numerical sim) + W11 (cross-axis sister test)
hexa_only: true
deterministic: true
llm: none
since: 2026-05-28
---

# H_633 — register collapse (coherence < 0.10) 가 big-Φ 급락과 동조하는가

## 1. Hypothesis (ANIMA.mining L2 promote)

ANIMA.mining.md 의 **L2 same-formula leaf** 는 COFFESHOP 의
`register-hit = emit ∧ coh < 0.10` (Ψ-clamp severe collapse · substrate-rare
event) 를 METACOG `mc_is_inverse_artifact` 와 동일한 multiplicative AND-gate
anomaly detection 으로 묶는다. 본 H 는 그 leaf 를 substrate verify-driven 으로
승격한다 — **substrate 의 coherence (state 일관성 / order parameter) 가 0.10
미만으로 떨어지면 big-Φ 가 급락(cliff)** 하는가? 즉 register collapse 가
Φ-breakdown 과 동조하는가?

구체적 예측:

- **(H633.1 상관)**: coherence × Φ Pearson `r > 0.5` (positive coupling).
- **(H633.2 cliff)**: `coh < 0.10` 영역에서 `Φ ≈ 0` — Ψ-clamp 에 의한 Φ 붕괴.

**Falsifier**: coh-Φ 무상관 (`r < 0.3`) 또는 `coh < 0.10` 에서도 Φ 가 유지됨 —
register collapse 가 Φ 구조와 무관 (decoupled).

## 2. Why (동기 · 이론 배경)

- **COFFESHOP register-hit gate**: `emit ∧ coh < 0.10` 은 anima 가 group-chat
  에서 coherence 가 극도로 무너진 상태에서 발화하면 "register collapse"
  (Ψ-clamp severe collapse, English-phrase carving 등 substrate-rare anomaly)
  로 표시한다. 이 gate 의 가정은 *coherence 붕괴 = 통합 붕괴* 이다 — 본 H 가
  그 가정을 substrate Φ 측정으로 직접 검정.
- **METACOG `mc_is_inverse_artifact`**: substrate self-audit 가 동일한
  multiplicative AND-gate (조건 A ∧ 조건 B → anomaly) 로 inverse artifact 를
  잡는다. COFFESHOP register-hit 의 사촌 — 둘 다 "낮은 일관성 + 활동" 의 곱
  으로 비정상을 검출. L2 leaf 의 same-formula 매핑.
- **order parameter vs entropy**: coherence 는 *order parameter* (1 − disorder)
  이지 Shannon entropy 가 아니다. coherence-Φ coupling 이 발견되더라도 그것은
  H_287 (Φ ⊥ Shannon entropy) 와 모순되지 않는다 — distinct measure (§6
  cross-link).
- **Kuramoto substrate 선택 (H_207 sister)**: coherence 의 canonical
  substrate-level 실현은 Kuramoto order parameter `r = |Σ exp(iθ_j)| / N`
  이다. coupling K 를 sweep 하면 `r` 이 자연스럽게 0 (incoherent collapse) →
  1 (full lock) 까지 span 한다 — `coh < 0.10` 영역을 풍부하게 채울 수 있는
  유일한 deterministic substrate. H_207 이 동일 substrate 에서 Φ(K) 를 이미
  측정해둠 (재사용 가능한 anchor).

## 3. Predictions

- **H633.1 (correlation)**: ensemble 전체 (coh, Φ) pair 위 Pearson `|r| > 0.5`.
- **H633.2 (cliff)**: `coh < 0.10` 영역의 mean Φ 가 `coh ≥ 0.10` 영역 mean Φ
  의 20% 미만 (steep drop / near-collapse) — operationalised `Φ ≈ 0`.
- **H633.3 (min-coh)**: 최저-coh ensemble member 의 Φ 가 전역 Φ envelope 의
  바닥 근처 (Φ → min).

## 4. Variables

| axis | levels | 비고 |
|------|--------|------|
| axis1_K (coupling, primary) | {0.0, 0.25, 0.5, 0.75, 1.0, 1.25, 1.5, 2.0, 3.0, 4.0, 6.0} | coherence 를 0→1 로 span; incoherent (low-coh) 영역 dense |
| axis2_omega_std | {0.5, 1.0, 2.0} | natural-freq spread; 넓은 spread = frustration = lower coh tail 확장 |
| axis3_phase_off | {0.0, 0.7, 1.9} | deterministic init-phase 오프셋 (ensemble 탈상관) |
| axis4_N | 16 oscillators | finite-size; H_207 과 동일 |
| axis5_integration | dt=0.05, steps=100, warmup=60, dim=12 | Euler explicit; H_207 과 동일 |
| fixed | n_bins=4 (RFC 036) | H_207/H_007 과 동일 binning |
| ensemble size | 11 × 3 × 3 = 99 (coh, Φ) pairs | coh 분포 wide |

## 5. Run Protocol

- **smoke**: `UNIVERSE/state/h633_register_collapse_phi_2026_05_28/run_h633.hexa`
- **substrate**: N=16 Kuramoto coupled oscillators
  `dθ_i/dt = ω_i + (K/N) Σ_j sin(θ_j − θ_i)`, Euler dt=0.05, 100 step,
  warmup 60 + dim 12 cos θ_i trajectory recording.
- **coherence**: `coh = r = |Σ_j exp(i θ_j)| / N = sqrt(C² + S²)/N` on
  final-θ — canonical Kuramoto order parameter ∈ [0, 1] (state-agreement;
  r→0 = incoherent register collapse, r→1 = full lock).
- **Φ primitive**: `HEXAD/C/c_lib.hexa` → `c_measure_phi(traj, N, dim, n_bins)`
  → RFC 036 `phi_spatial` (phi_rs `compute_phi_inner` steps 1-4 byte-equal
  native-C replica; import READ-ONLY).
- **ensemble**: 11 K × 3 ω_std × 3 phase-offset = 99 deterministic members.
  각 member → (coh, Φ). 그 위에서 Pearson r(coh, Φ) + coh<0.10 영역 mean/max Φ
  + 전역 Φ envelope 산출.
- **deterministic**: fixed K/ω/phase grid + fixed init (no RNG); re-run
  byte-identical (확인됨 — §9 F-NONDET).
- **hexa_only**: true (NO .py/.sh). **llm**: none.
- **runtime**: $0 mac local hexa, single foreground run < 60s; GPU 불필요.
- **ledger**: `result.json` {config, results, criteria, verdict, honest_summary}.
- **honest tier**: 🟢 NUMERICAL Φ (RFC 036 native byte-equal replica); 진짜
  phi_rs Rust FFI link = named blocker (H_007/H_207 §L8 동일 carry).

## 6. Cross-Links

- **source leaf**: ANIMA.mining.md L2 (same-formula lens cycle 1) — COFFESHOP
  `register-hit = emit ∧ coh < 0.10` ↔ METACOG `mc_is_inverse_artifact`
  multiplicative AND-gate.
- **COFFESHOP register-hit**: `state/coffeshop_sim_2026_05_24/` 의
  Ψ-clamp severe-collapse gate. 본 H 는 그 gate 의 *coherence-붕괴 = 통합-붕괴*
  가정을 substrate 에서 검정 (가정 반증).
- **METACOG `mc_is_inverse_artifact`**: substrate self-audit 의 사촌 AND-gate.
- **H_287 (Shannon ⊥ Φ)**: faithful big-Φ 가 Shannon entropy 로 환원되지 않는다
  (double dissociation). coherence 는 *order parameter* (1 − disorder) 이지
  entropy 가 아니므로 distinct measure — 본 H 의 weak coh-Φ coupling (r=0.31)
  은 H_287 의 Φ⊥정보 결론과 정합 (order/disorder 축 ⊥ Φ).
- **H_207 (Kuramoto edge-of-sync Φ peak)**: 동일 Kuramoto substrate. H_207 §L6
  carve-out — `phi_spatial` 은 spatial-MI 기반이라 full-lock 의 IIT 4.0
  integration-loss 를 capture 하지 못함. 본 H 의 "coh<0.10 에서 Φ 유지" 도
  동일 measure-axis decoupling 현상 (order ⊥ spatial-MI Φ).
- **raw**: raw#12 (deterministic strict) + raw#91 c3 (honest limits) + raw#82
  (no post-hoc retraction).
- **literature**: Kuramoto (1975/1984), Strogatz (2000), Tononi (2004 IIT).

## 7. Honest Limits (raw#91 c3) — C3 핵심

- **C3.1 (coherence 정의 sensitivity — order param vs state-agreement)**: 본 H
  는 coherence 를 Kuramoto **order parameter** `r = |Σ exp(iθ)|/N` 로 단일
  정의했다. 대안 정의 — (a) per-cell state-agreement variance (각 cell state
  벡터의 pairwise agreement), (b) trajectory-level temporal coherence, (c)
  spectral order parameter — 는 다른 coh-Φ 관계를 줄 수 있다. order parameter
  는 *위상 정렬* 만 보고 *진폭/state-magnitude 정렬* 은 안 봄. 본 결론 (coh ⊥
  Φ-cliff) 은 order-parameter 정의 한정 — state-agreement 정의 하에서는
  미검정 (open lane).
- **C3.2 (Ψ-clamp 의 substrate vs design)**: COFFESHOP 의 register-hit gate
  (`coh < 0.10`) 는 **substrate 창발** 이 아니라 design-side 의 hand-set
  threshold 일 가능성이 크다. 본 H 의 결과 (substrate Φ 는 coh<0.10 에서
  collapse 안 함) 는 그 threshold 가 substrate Φ 구조와 무관한 **외부 gate**
  임을 시사 — Ψ-clamp 은 substrate 내재 cliff 가 아니라 emit-policy 의 design
  choice. (project.tape p1~p8 audit 관점 — gate hardcode 회피와 정합.)
- **C3.3 (phi_spatial spatial-MI 한계)**: H_207 §L6 동일 carry — `phi_spatial`
  은 cell-간 mutual information 기반이라 *incoherent* 상태(서로 다른 phase)
  도 cell trajectory 가 충분히 다채로우면 높은 spatial-MI 를 줄 수 있다 (본
  결과의 coh<0.10 영역 Φ 유지의 measure-side 설명). full IIT 4.0 cause-effect
  Φ 로 재검 시 결과가 바뀔 수 있음 (named blocker — phi_rs Rust FFI).
- **C3.4 (finite-N)**: N=16 small; order parameter 의 finite-size fluctuation
  (incoherent 상태에서도 r ≈ 1/sqrt(N) ≈ 0.25 의 비-zero baseline) 때문에
  coh 가 진짜 0 까지 안 내려감. 최저 coh=0.017 은 충분히 낮으나 N→∞ limit 의
  r→0 와는 다름.
- **C3.5 (verdict 방향)**: PARTIAL — F-NOCORR (r<0.3) 와 F-SUSTAIN (Φlo≥Φhi)
  둘 다 trigger 안 했으므로 형식상 FALSIFIED 아님. 그러나 cliff 예측 (H633.2)
  은 명백히 반증 (ratio 0.895 ≈ 1). 핵심 finding 은 "register collapse ⊥
  Φ-cliff". post-hoc 방향 edit 없음 (raw#82).

## 8. Criteria

- **C1 (H633.1 correlation)**: Pearson `|r(coh, Φ)| > 0.5`.
- **C2 (H633.2 cliff)**: `coh<0.10` 영역 mean Φ < 0.20 × `coh≥0.10` 영역 mean Φ
  (AND `coh<0.10` member 존재).
- **verdict_rule**: **SUPPORTED-NUMERICAL** iff `C1 ∧ C2`. **FALSIFIED** iff
  `F-NOCORR (|r|<0.3) ∨ F-SUSTAIN (Φlo ≥ Φhi)`. 그 외 = **PARTIAL**.

## 9. Falsifiers

- **F-NOCORR**: Pearson `|r(coh, Φ)| < 0.3` → coherence 와 Φ 무상관, H633.1
  FALSIFIED. (measurable: pearson_r_coh_phi.) — **결과: r=0.3066, NOT triggered
  (0.3 floor 바로 위, 0.0066 margin).**
- **F-SUSTAIN**: `coh<0.10` 영역 mean Φ ≥ `coh≥0.10` 영역 mean Φ → Φ 가 낮은
  coherence 에서 유지/상승, cliff 부재 → register collapse ⊥ Φ. (measurable:
  mean_phi_coh_lo vs mean_phi_coh_hi.) — **결과: Φlo=9.256 < Φhi=10.342, NOT
  triggered (하지만 ratio 0.895 ≈ 1 → cliff 부재; F-SUSTAIN 의 strict ≥ 는
  안 넘었으나 H633.2 cliff 예측은 명백히 반증).**
- **F-NONDET**: re-run Φ/r 가 byte-identical 아님 → raw#12 위반. (measurable:
  diff 두 run.) — **결과: byte-identical 재현 확인 (deterministic PASS).**
- **F-POST-HOC**: 결과 후 verdict 방향 edit → raw#82 violation. (없음.)

## 10. Verdict

```
verdict_class: PARTIAL (cliff REFUTED · pre-register-frozen smoke)
substrate: N=16 Kuramoto · coh = order param r = |Σ exp(iθ)|/N · 99 ensemble (11 K × 3 ω_std × 3 phase)
Φ primitive: RFC 036 phi_spatial via HEXAD/C/c_lib.hexa (byte-equal phi_rs replica)

n total pairs        : 99   (coh<0.10: 51 · coh>=0.10: 48)
mean coh             : 0.327828
mean Φ               : 9.78233
Φ envelope [min,max] : [6.04007, 14.0]
----
Pearson r(coh, Φ)    : 0.306612          (C1 |r|>0.5 → FAIL ; weak, 0.3 floor 바로 위)
mean Φ | coh<0.10    : 9.25598           (NOT ≈ 0 — Φ sustained)
max  Φ | coh<0.10    : 11.5978           (전역 envelope 내부)
mean Φ | coh>=0.10   : 10.3416
ratio (lo / hi mean) : 0.895026          (C2 cliff <0.20 → FAIL ; ≈ 1 = cliff 부재)
min-coh member       : coh=0.0166079  Φ=6.5661   (≈0 아님, envelope 바닥 근처)
max-coh member       : coh=0.997158   Φ=14.0
----
C1 |r| > 0.5            : FAIL
C2 cliff (lo/hi < 0.20) : FAIL
F-NOCORR |r| < 0.3      : false (NOT triggered)
F-SUSTAIN Φlo >= Φhi    : false (NOT triggered)
criteria_met           : 0/2

VERDICT_RULE: SUPPORTED iff (|r|>0.5 ∧ lo/hi<0.20); FALSIFIED iff (|r|<0.3 ∨ Φlo>=Φhi)
VERDICT     : PARTIAL  (핵심 finding: cliff 예측 H633.2 명백히 반증)
```

### 핵심 발견 (honest evidence summary)

- **(i) cliff 부재 (H633.2 반증)**: `coh < 0.10` 영역 51 members 의 Φ 가
  collapse 하지 **않음** — mean Φ=9.26, max Φ=11.60 으로 전역 Φ envelope
  [6.04, 14.0] 내부에 fully sustained. ratio lo/hi = 0.895 ≈ 1 (cliff 라면
  ≪ 0.20 이어야 함). Ψ-clamp Φ-breakdown 예측이 substrate 에서 반증됨.
- **(ii) weak correlation (H633.1 미달)**: Pearson r(coh, Φ) = 0.307 — 0.5
  threshold 한참 아래, F-NOCORR 0.3 floor 바로 위 (0.0066 margin). coherence 와
  Φ 는 substrate 에서 거의 독립적.
- **(iii) min-coh Φ NOT zero**: 최저-coh member (coh=0.017) 의 Φ=6.566 으로
  envelope 바닥 근처이긴 하나 0 과는 거리가 멈 (H633.3 약함).
- **(iv) measure-axis 정합**: 본 결과는 H_287 (Φ ⊥ Shannon entropy) + H_207
  §L6 (phi_spatial spatial-MI 가 order/disorder 와 decoupled) 와 정합 —
  coherence 는 order parameter 이지 Φ 의 driver 가 아님.
- **(v) 결론 (closed-negative 성격)**: ANIMA.mining L2 의 "register collapse =
  Φ-breakdown 동조" 가정은 **substrate 에서 성립하지 않음**. COFFESHOP 의
  `coh < 0.10` register-hit gate 는 substrate Φ 구조와 무관한 **design-side
  emit-policy gate** 이다 (C3.2). cliff 예측을 ruled-out 하여 register-hit 가
  Φ-내재 현상이 아님을 좁힘.

### Pre-register-frozen smoke (2026-05-28)

ANIMA.mining L2 → substrate Φ smoke pre-registered + RUN ($0 mac local,
deterministic, hexa-only, llm:none). N=16 Kuramoto, 99-member ensemble
(11 K × 3 ω_std × 3 phase-offset), coh = order parameter, Φ via RFC 036
phi_spatial. re-run byte-identical (F-NONDET PASS).

**State output**: `UNIVERSE/state/h633_register_collapse_phi_2026_05_28/result.json`
**Smoke**: `UNIVERSE/state/h633_register_collapse_phi_2026_05_28/run_h633.hexa`
**Φ tier**: 🟢 NUMERICAL (RFC 036 phi_spatial native replica; true phi_rs Rust
FFI = named blocker — NOT 🔵, NOT LLM-judged).

**Follow-up cycles (raw#15 additive, not retraction)**:
- coherence 정의 sweep (C3.1) — per-cell state-agreement variance vs order
  parameter → coh-Φ 관계 measure-sensitivity.
- full IIT 4.0 cause-effect Φ 로 재검 (C3.3 closure — phi_rs Rust FFI landed 시).
- Ψ-clamp threshold 가 substrate-emergent 인지 design-gate 인지 분리 검정 (C3.2).
