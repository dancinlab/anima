---
spec_id: nexus6_1013lens_lens_channel_reimpl_2026_05_12
parent_spec: state/nexus6_1013lens_activation_2026_05_11/spec.md
target_h: H_135 (DD166 NEXUS 1013-lens discovery engine)
status: design-only (NO actual reimpl; spec land + prototype only)
cycle: 5 §4 #F
authored: 2026-05-12
authored_by: agent
lock_policy: NO chflags/chattr — repository directive 2026-05-11
---

# Lens Input Channel Reimplementation Spec — `phi_lens(L_i, x)` 도메인 데이터 채널 도입

cycle 5 §3 #A canonical K=10 smoke (Agent 21) 의 TRIVIAL finding 에 대응한 *reimpl 명세*.
실제 reimpl 실행은 본 문서 scope 외 — cycle 5 §4 #C aggregator agent 가 wire 한다.

## 0. Context

- **Agent 21 (cycle 5 §3 #A) TRIVIAL finding**: K=10 canonical smoke 결과 `score=1.0` /
  `8/8` 이 모든 10 lens 에서 동일. 본체 `diff` 실측 결과 K=10 의 10 lens 는 *동일
  self-test 의 복제본* (comment header 4 lines + println label 1 line 만 차이). 출처:
  `smoke_k10_caveat_investigation_2026_05_12.md` §3.1–§3.3.
- **Hc_586 ground truth 미존재**: 1000x+ 가속 주장의 *substrate-side* 측정이 부재 — lens 가
  도메인 데이터 `x` 를 *측정하지 않고* n=6 primitive 상수 (σ=12, τ=4, φ=2, n=6, sopfr=5,
  J₂=24) 의 self-consistency 만 검증. K=25/K=50 으로 cascade 해도 trivial 결과가 propagate.
- **spec §2 `phi_lens(L_i, x)` 미구현 finding**: parent spec §2 는 `Φ_lens(L_i, x) ∈ ℝ` 를
  명세하지만 `x` 입력 채널이 *현 hexa 1,588 lens body* 에 부재. `argv()`, stdin, file
  read 등 어떤 외부 입력도 lens 가 소비하지 않음. 따라서 F2 (random-walk null) falsifier 의
  control 정의 자체가 불가능 — *영원히 self-trip 하지 않는 dead falsifier*.

본 spec 은 이 결함을 해결하기 위한 *input channel 명세* 와 *axis-specific kernel* 분리를
제안한다.

## 1. Input Channel 정의 — 도메인 데이터 `x` 의 shape/dtype/source

### 1.1 Unified format (generic interface)

두 가지 input modality 를 *generic interface* 로 통합:

| modality | shape | dtype | source |
|----------|-------|-------|--------|
| **embedded sequence** | `(B, T, D)` | f32 | text/audio/image embedding (unified format — Mistral-7B hidden state, MFCC, ResNet feature) |
| **state snapshot** | `(B, S)` | f32 | 시스템 상태 벡터 (1-D vector per batch — Φ★ engine raw output, sensor reading, scalar field sample) |

aggregator (`tool/anima_nexus_1013lens_cascade.hexa` — renamed 2026-05-12) 가 입력 type 을 *header* 로 discriminate
하고 lens-specific kernel 이 axis 에 맞는 modality 를 consume. 둘 다 미지원 lens 는 `support_mask=0`.

### 1.2 입력 protocol (lens-side)

```
stdin line 1:   modality_tag   ∈ {"embed", "state"}
stdin line 2:   shape spec     (e.g. "B=1,T=128,D=768"  or  "B=1,S=64")
stdin line 3+:  raw float values (whitespace-separated, row-major)
EOF:            terminate input
```

lens 는 modality_tag 가 axis 와 호환되지 않으면 `support_mask=0` + `score=NaN` 반환 (cascade
aggregator 에서 NaN 은 통계 계산에서 exclude). 호환되면 axis-specific kernel 으로 forward.

### 1.3 source alignment with hexa metadata `axis` field

cycle 5 §3 #B `lens_registry_synthesized_2026_05_12.md` 의 hexa header `axis` field 와
align — lens kernel 의 modality 선택은 registry 의 `axis` 를 1차 source 로 한다 (§2.2 mapping).

## 2. `phi_lens(L_i, x)` 측정 함수 명세

### 2.1 signature

```
fn phi_lens(L_i: Lens, x: Input) -> {score: f32, meta: dict}
  where
    score ∈ [0, 1]   (정량적 alignment — 0=no signal, 1=strong signal)
    meta  : axis-specific metric dict (e.g. {entropy, mi, persistence_h0, ...})
```

### 2.2 axis-specific kernel mapping

각 lens 의 `axis` (information / topology / causal / consciousness / ...) 에 따라
measurement metric 을 *분리* 한다 (single self-test loop 가 아니라 axis-specific computation).

| axis | metric | input modality | references |
|------|--------|----------------|------------|
| information | MI estimate `I(x; baseline)` + Shannon entropy `H(x)` | embed/state | core_info, core_memory |
| topology | persistence diagram `H_0/H_1` betti number | embed (treat T as filtration index) | core_topology, core_boundary |
| causal | Granger causality / transfer entropy `TE(x_t→x_{t+1})` | embed (T as time) | core_causal, core_evolution |
| consciousness | IIT proxy φ (cov-MIP) 또는 binding measure | embed | core_consciousness |
| thermodynamics | entropy production `dS/dt` + Stefan-Boltzmann ratio fit | state (time series) | core_thermo |
| quantum | Bell-violation proxy 또는 quantum-info bridge | state | core_quantum |
| geometry | manifold invariant (curvature, dimension estimate) | embed (D as ambient) | core_topology, core_triangle |
| dynamics | Lyapunov exponent / chaos indicator | state (time series) | core_chaos, core_gravity |
| graph | spectral gap / clustering coefficient | state (S=N², adjacency) | core_network |
| scale | scaling exponent (Hurst, power-law fit) | embed/state | core_scale, core_multiscale |
| stability | variance / spectral radius | state (time series) | core_stability |

axis 가 multiple modality 지원 가능 (e.g. information 은 embed/state 둘 다) — lens 가
selection logic 보유.

### 2.3 sign convention

`score > 0.5` = pattern detected (positive evidence). `< 0.5` = below baseline noise. parent
spec §2 의 `Φ_lens > 0` 형식적 acceptance 와 호환 (현 `[0,1]` 범위는 `2*score - 1` 로 ±변환 가능).

## 3. Canonical Lens Prototype — `core_info.hexa` reimpl

K=10 중 가장 simple `core_info.hexa` (information axis) 의 reimpl pseudo-code (~30 lines
hexa-style). actual runnable 버전은 `lens_channel_reimpl_prototype_core_info.hexa` 에 land.

```
// pseudo-code (hexa-style)
axis: information
modality: embed | state

fn phi_lens(self, x):
  // 1. modality check
  if modality_tag not in ["embed", "state"]: return {score: NaN, support_mask: 0}

  // 2. axis-specific kernel: entropy + MI estimate
  entropy   = compute_entropy(x)              // Shannon H(x), histogram-based
  baseline  = uniform_baseline(shape(x))      // reference distribution
  mi        = compute_mi(x, baseline)         // mutual information estimate

  // 3. n=6 primitive closure (legacy self-test, preserved as meta only)
  n6_closure = (SIGMA * PHI == N * TAU) && (J2 == SIGMA * PHI)

  // 4. score = sigmoid blend
  alpha = 0.7; beta = 0.3
  raw   = alpha * mi + beta * (1 - entropy_overhead(entropy))
  score = sigmoid(raw)                        // ∈ [0, 1]

  return {
    score: score,
    support_mask: 1,
    meta: {entropy: entropy, mi: mi, n6_closure: n6_closure}
  }
```

기존 self-test (n=6 primitive closure) 는 *meta* 로 보존 — 호환성 유지 + Hc_378 closure
evidence 도 함께 emit. score 자체는 `x` 의존.

## 4. Migration Plan — 1,588 lens reimpl 우선순위

| phase | scope | cost (wall) | $ | binding cascade step |
|-------|-------|------------:|---|----------------------|
| **Phase 1** | K=10 (spec §3.1 whitelist) full reimpl + axis-kernel wire | 1–2 h | $0 (CPU) | K=10 canonical re-smoke |
| **Phase 2** | K=25 (cascade plan §1.1+§1.2+§1.3) reimpl | 4–6 h | $0 | K=25 canary cascade |
| **Phase 3** | 1,588 batch reimpl with **template inheritance** (axis-tagged template) | multi-cycle (≥ 3 cycle) | $0–low | K=50 / full-1013 |

각 lens 의 axis-specific kernel 은 cycle 5 §3 #C `nexus_lens_score` (Φ★ naming refactor) 와
분리 — *naming axis* 와 *measurement axis* 가 orthogonal.

## 5. Falsifiers (F-reimpl-1/2/3) — 본 reimpl 의 verdict gate

| ID | falsifier | trip 조건 | trip 시 결과 |
|----|-----------|----------|--------------|
| **F-reimpl-1** | input data 의존성 | K=10 reimpl 후 canonical smoke 의 `pos_ratio` 가 `x` noise level 에 따라 *불변* (dynamic range < 0.3) | lens 가 여전히 `x` 무시 — reimpl 실패 |
| **F-reimpl-2** | trivial 복제본 검증 | K=10 lens 들의 score 가 same `x` 입력에 대해 *모두 일치* (cross-validation r < 0.3) | axis-specific kernel 분리 실패 — 여전히 self-test 복제본 |
| **F-reimpl-3** | signal-noise separation | `shuffled-x` (control) score ≥ `real-x` score | lens 가 signal vs noise 구분 불가 — Hc_960 mislabel-by-noise 실현 |

F-reimpl-1 또는 F-reimpl-3 trip → Phase 1 halt, K=10 reimpl 자체 미충전. F-reimpl-2 trip →
axis-specific kernel mapping (§2.2) 재설계.

## 6. Honest Limits (L1–L4)

- **L1**: axis-specific kernel 의 well-definedness 가 axis 별로 *uneven* — information lens 의
  entropy 는 well-defined (histogram 기반 standard estimator) 이지만 consciousness lens 의
  measurement axis 는 still open (IIT proxy φ 자체가 P-A1 lane 의 미해결 문제 — 본 spec 의
  binding 범위 외).
- **L2**: input channel `x` 의 unified format (`embed (B,T,D)` 또는 `state (B,S)`) 이
  1,588 lens *전체* 에 fit 한다는 가정은 untested — 일부 lens (예: topology lens 의 일부는
  graph adjacency 필요, causal lens 의 일부는 intervention 정보 필요) 는 추가 modality 요구
  가능. Phase 3 batch reimpl 시 modality 확장 (예: `graph (B, N, N)`) 필요할 수 있음.
- **L3**: 본 reimpl 자체가 *nexus lens engine 의 substantial refactor* — 기존 hexa 1,588 file
  *모두* 변경 — back-compat blocker. 본 spec 은 anima repo side 에 land 하지만 실제 reimpl
  은 nexus repo (`/Users/ghost/core/nexus/lenses/`) 측 coordination 필요 (cycle 5 §4 #C
  aggregator agent 의 wire 단계에서 결정).
- **L4**: K=10 reimpl Phase 1 만으로 cascade resume 가능한지 *미결정* — F-reimpl-1/2/3 PASS
  후에도 K=25 의 expanded selection (cascade plan §1.2 +13 lens) 까지 reimpl 후 cascade 진입
  해야 binding. K=10-only reimpl 은 parent spec §4 C1 의 cascade gate 와 axis mismatch (C1
  은 K=10→25→50 연속 PASS 요구).

## 7. Cross-Reference

| 출처 | path | 관계 |
|------|------|------|
| cycle 5 §3 #A (Agent 21 TRIVIAL finding) | `state/nexus6_1013lens_activation_2026_05_11/smoke_k10_caveat_investigation_2026_05_12.md` | 본 spec 의 *동기* — §3.1–§3.3 trivial verdict |
| cycle 5 §3 #B (lens registry synthesis) | `state/nexus6_1013lens_activation_2026_05_11/lens_registry_synthesized_2026_05_12.md` | hexa `axis` field source (§1.3) |
| cycle 5 §3 #C (phi_star naming refactor) | `state/.../phi_star_naming_refactor_2026_05_12.md` | nexus_lens_score 분리 — §4 Migration Plan 의 axis 분리 정신 |
| cycle 5 §3 #E (cascade K=25 plan) | `state/.../cascade_k25_plan_2026_05_12.md` | §0 prereq strict 화 source (본 spec 이 K=25 prereq 의 의미적 layer 보강) |
| Hc_586 | `docs/hypotheses/Hc_586.md` | **status: suspended-pending-channel-reimpl** (제안 — Agent G scope, 본 spec 미적용) |
| parent spec §2 | `state/.../spec.md` §2 | `phi_lens(L_i, x)` signature 의 *원전*, 본 spec 의 reimpl target |
| prototype | `state/.../lens_channel_reimpl_prototype_core_info.hexa` | §3 actual runnable hexa-DSL |

---

**lock policy**: 본 spec 작성 과정에서 chflags/chattr immutable flag 적용 없음. 기존 unlock
파일 재잠금 없음.
