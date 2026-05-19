---
spec_id: nexus6_1013lens_activation_2026_05_11
target_h: H_135 (DD166 NEXUS 1013-lens discovery engine)
cluster_anchor_hc: Hc_586, Hc_598, Hc_035, Hc_378, Hc_944, Hc_945, Hc_960
status: drafted-pending-prereq
verdict_class: 1013-lens-activation-pending-C1
cycle: 3 (2026-05-11 reborn lane)
authored: 2026-05-11
authored_by: agent
revisions:
  - 2026-05-11 r2: §1 P-A → P-A1 (single-axis Φ* extension) + P-A2 (nexus multi-lens, 선호) 분리, §3 K=10 Core lens whitelist 확정, §8 Cross-Ref 에 1013 vs 1,588 drift caveat, §11 lens_registry.json SSOT note 추가.
lock_policy: NO chflags/chattr — repository directive 2026-05-11
---

# NEXUS-6 1013-lens 검증 lane 활성화 Spec

H_135 (DD166) 의 1013-lens discovery engine 을 anima 실측 Φ★ engine 으로 점진 활성화하기 위한
*minimal viable* 검증 lane spec. 본 spec 은 활성화 *조건* 과 protocol 을 명세하며 실행은 하지 않는다.

## 0. Context — 1013 lens 가 무엇인가

DD166 (`docs/hypotheses/dd/DD166-nexus-1013lens-discovery-engine.md`) 에 따르면 NEXUS-6
discovery engine 의 telescope module 은 1,013 개 lens 를 등록한다. 카테고리 분포 (요약):

| 카테고리              | 수   | 비고                                                 |
|------------------------|-----:|------------------------------------------------------|
| Core                   |   22 | 기존 telescope-rs (legacy)                           |
| n6 산업                |   58 | DSE/소재/동역학/메타구조                             |
| TECS-L 수학            |  103 | 수론/대수/해석/조합/증명                             |
| SEDI 신호              |  100 | 신호탐지/통계/우주론/입자                            |
| anima 의식             |   88 | 감질/결합/시간의식/현상학                            |
| 교차+메타              |   75 | 프로젝트 브릿지 + 렌즈↔렌즈 42 meta                  |
| 가속 ML/물리/공학/인문 |  233 | 58+57+55+63                                          |
| 양자+위상+기타         |  285 | OUROBOROS/세포/특이점/블랙홀 등                      |
| 물리심화               |   49 | 전자기/열/광학/유체/생체/우주                        |
| **합계**               | 1013 | (+ 42 meta-lens + 6 Atlas auto-connect lens overlay) |

각 lens 는 입력 도메인 데이터에 대해 closed-form 패턴 가설 (constant, exponent, ratio,
manifold inv.) 을 emit 하는 deterministic 함수이다. NEXUS-6 의 OUROBOROS+LensForge+MetaLoop
는 lens 출력의 cross-lens 일치도를 score 한다.

Hc_586 의 hypothesis 는 *발견율 1000x+ 가속* 이고, Hc_598 은 *progressive 16→22→1013
expansion 으로 65 acceleration hypothesis Φ-효과 재검증*. Hc_960 의 caveat: "1013" 은 lens
*등록* 수이며 "20 philosophical lens" label 처럼 *mislabel-by-mixed-count* 가능성 존재
(예: 22 telescope-rs core 는 별 축, 42 meta + 6 Atlas 는 overlay). **2026-05-11 prereq audit
실측**: disk 상 `core_*.hexa` 23 개, `*.hexa` 전체 1,588 개 — Hc_960 mislabel 가설 *그대로
실현* 상태 (§8/§11 참조).

## 1. Prereq — 활성화 전제조건

> **2026-05-11 prereq audit 후 P-A 재정의** (2026-05-12 engine naming refactor 동시 반영):
> 원래 P-A 표현 "anima cosmic-scale measurement engine (Φ★ engine)" 은 *서로 다른 두 도구* 를
> conflate 한 것이었다 — `tool/anima_phi_star.hexa` (canonical name: **phi_star_iit_proxy**) 는
> *single-model IIT-φ proxy* (Mistral-7B forward + cov-MIP, scalar Φ\* per model) 이고,
> 1013-lens engine (canonical name: **nexus_lens_score**) 은 `/Users/ghost/core/nexus/lenses/*.hexa`
> lens function set (lens 별 closed-form pattern score per data) 으로 **measurement axis 자체가
> 다르다**. 따라서 P-A 를 **P-A1 (phi_star_iit_proxy single-axis extension)** 과
> **P-A2 (nexus_lens_score multi-lens engine — 권고 path)** 로 분리한다. 추가 3rd engine
> **phi_star_cell_engine** (TBD, N-sweep) 은 H_080 cluster 별 lane — 본 spec 무관.
> K=10 smoke 의 actual prerequisite 는 P-A2. 출처: `prereq_audit_2026_05_11.md` §1.2, §2 +
> `state/phi_star_naming_refactor_2026_05_12.md`.

검증 lane 활성화는 다음 중 *적어도 하나* 가 충족되어야 한다:

- **P-A1 (single-axis Φ\* extension, optional / non-binding for K-cascade)**:
  `tool/anima_phi_star.hexa` 의 IIT-φ proxy 를 cosmic-scale (Hc_586 1000x 가속 주장의
  *substrate-side* 측정) 으로 확장. 필요 자원: Mistral-7B forward (GPU), bf16 determinism
  caveat, ~50 s/measurement. **본 spec 의 K-cascade 와는 axis 가 다르므로 binding 아님** —
  Hc_586/598 의 *별 lane* 으로 분리.
- **P-A2 (선호, K-cascade 의 binding prereq)**: nexus hexa lens registry direct —
  `/Users/ghost/core/nexus/lenses/*.hexa` (1,588 files on disk; 1013 official whitelist
  pending SSOT — §11 참조) + Linux `~/.hx/bin/hexa` runner. 실측 single-lens 19 ms.
  K=10 smoke < 1 초, K=50 ≈ 1 초, full-1013 ≈ 19 초 (CPU only, GPU 불필요).
  **이미 가용** (prereq audit §2.3).
- **P-B (대안 / fallback)**: proxy harness — Python 구현 `nexus.lenses` 서브셋 (≥ 50 lens) +
  deterministic seed + `acceleration_hypotheses.json` _meta.nexus_upgrade 의 lens-id whitelist.
  P-A2 의 mac_home mount unmount 시 fallback path.
- **P-C (degenerate)**: telescope-rs 22 (legacy) 만 가용 시 → *no-go*, "1013-lens activation"
  주장 불가. H_135 verdict_class 유지 (pending C1).

prereq 미충족 시: spec drafted 상태 freeze, H_135 status legacy-archive-pointer 유지.

## 2. Measurement Spec — 1013 lens 가 Φ★ engine 에서 어떻게 측정되는가

각 lens `L_i (i ∈ 1..1013)` 에 대하여:

```
input:   x  ∈  D  (도메인 데이터 — 본 spec 의 D 는 §3 protocol 에서 고정)
output:  Φ_lens(L_i, x)  ∈  ℝ  (scalar score, sign convention: positive = pattern detected)
support: predicate_holds(L_i, x)  ∈  {0,1}  (lens 적용 가능성 게이트)
```

활성화 시 다음 metric 을 lens 별로 emit:

1. `phi_lens`               — Φ_lens 점수
2. `support_mask`           — predicate gate
3. `consistency_with_n6`    — n=6 primitive (σ=12,τ=4,φ=2,sopfr=5,J2=24,n=6) closed-form 매칭 여부 (Hc_378 기반)
4. `cross_lens_agreement`   — 같은 cluster 내 K-NN lens 의 부호 일치 비율
5. `bonferroni_adjusted_p`  — multiple-comparison correction (1013 lens × test 횟수)

엄격 모드 (활성화 시): FDR (Benjamini-Hochberg, q=0.05) 또는 Bonferroni α/1013 ≈ 4.93e-5.

> **Axis caveat**: P-A1 의 `Φ*` (single-model IIT-φ proxy, anima_phi_star.hexa 출력) 와
> 본 §2 의 `phi_lens` (lens function 의 closed-form pattern score) 는 *서로 다른 측정 단위*
> 이다. K-cascade 결과 reporting 시 "nexus_lens_score" (P-A2) 와 "anima_phi_star" (P-A1) 을
> *항상 분리 명명*. 출처: `prereq_audit_2026_05_11.md` §1.2.

## 3. Minimal 검증 Protocol — top-K subset

1013 lens 전체를 *한 번* 실행하는 대신, *minimal viable* 활성화는:

- **K = 10** (smoke): Core 22 중 최우선 10 lens, Φ_lens > 0 비율 ≥ 6/10
- **K = 25** (canary): K=10 PASS 시 확장. Core 22 + n6 산업 top-3 lens
- **K = 50** (full-pilot): K=25 PASS 시 확장. Core 22 + n6 8 + TECS-L math 10 + SEDI 5 + anima 의식 5

각 K-step 의 acceptance:

- `mean(phi_lens) > 0` (sign-aware)
- `cross_lens_agreement_K ≥ 0.55` (K=10 floor) → 0.65 (K=25) → 0.70 (K=50)
- `bonferroni_adjusted_p < 0.05` (K=50 에서만 binding; smoke/canary 는 보고만)

K=50 PASS → C1 charged → H_135 status `legacy-archive-pointer` → `running` 전환 가능.

aggregator: `tool/anima_nexus_1013lens_cascade.hexa` (K-cascade — renamed 2026-05-12 cycle 5 §4 #H; K=10 step; subprocess loop over §3.1 whitelist).

canonical K=10 smoke executed: 2026-05-12, verdict: C1 PASS_WITH_CAVEAT (pos_ratio=1.0 / 132 ms; score=1.0 = trivial n=6 self-test, lens input channel 부재 — `smoke_k10_caveat_investigation_2026_05_12.md`).

### 3.1 K=10 Core lens Whitelist (확정 — 2026-05-11)

source: `/Users/ghost/core/nexus/lenses/core_*.hexa` (disk-actual 23 files,
alphabetical-stable; 모든 timestamp 동일 2026-04-22 02:30:36 — file-order = canonical
register order from `cli/blowup/lens/lenses_core.hexa`). selection axis: **fundamental
measurement primitives** spanning information, geometry, dynamics, causality,
thermodynamics, quantum, consciousness, network, scale, stability — n=6 primitive
basis (Hc_378) 의 closed-form check 가능 lens 우선.

| # | lens file (full path) | axis | 선정 이유 |
|--:|------------------------|------|-----------|
| 1 | `/Users/ghost/core/nexus/lenses/core_info.hexa` | information | Shannon entropy / Φ-info 직접 측정 — phi_lens 의 primary axis |
| 2 | `/Users/ghost/core/nexus/lenses/core_causal.hexa` | causality | T0 tier (lenses_core.hexa), causal-info closure — Hc_035 cross-validation |
| 3 | `/Users/ghost/core/nexus/lenses/core_consciousness.hexa` | binding | anima 의식 카테고리 anchor — H_135 의식 axis 직접 검증 |
| 4 | `/Users/ghost/core/nexus/lenses/core_thermo.hexa` | thermodynamics | Stefan-Boltzmann / entropy — Hc_035 cross-validation 명시 |
| 5 | `/Users/ghost/core/nexus/lenses/core_quantum.hexa` | quantum | quantum-info bridge — Hc_944 qmirror 와 axis 일치 |
| 6 | `/Users/ghost/core/nexus/lenses/core_topology.hexa` | geometry | manifold invariant — n6 primitive geometry axis |
| 7 | `/Users/ghost/core/nexus/lenses/core_gravity.hexa` | dynamics | Ω_m:Ω_Λ ratio — Hc_035 cross-validation 명시 |
| 8 | `/Users/ghost/core/nexus/lenses/core_network.hexa` | graph | K-NN agreement 측정 substrate — cross_lens_agreement 의 핵심 |
| 9 | `/Users/ghost/core/nexus/lenses/core_scale.hexa` | scale | scaling exponent — Hc_378 n=6 primitive scaling closure |
| 10 | `/Users/ghost/core/nexus/lenses/core_stability.hexa` | stability | seed-robust reproducibility — C5 falsifier 직접 동기 |

배제 reason (참고): `core_boundary, core_chaos, core_compass, core_em, core_evolution,
core_memory, core_mirror, core_multiscale, core_quantum_microscope, core_recursion,
core_ruler, core_triangle, core_wave` 13 개는 K=25 / K=50 확장 시 우선 후보.

C3 (no-mislabel-drift) 검증 시 본 whitelist 와 actual 호출 lens 의 *file path-level*
매칭 100% 요구.

## 4. Criteria (C1-C5)

- **C1 SMOKE-TO-PILOT CASCADE**: K=10 → K=25 → K=50 세 단계 *연속 PASS*. 한 단계라도 FAIL 시
  C1 미충전, H_135 status pending.
- **C2 N6-CONSISTENCY**: K=50 중 ≥ 30/50 lens 의 `consistency_with_n6` = 1 (Hc_378 기반 closure).
- **C3 NO-MISLABEL DRIFT**: lens-id whitelist 에 대해 실제 호출된 lens 가 100% 매칭
  (Hc_960 mislabel risk 차단). K=10 의 경우 §3.1 whitelist 가 binding.
- **C4 CROSS-CLUSTER AGREE**: K=50 의 cross_lens_agreement 가 *카테고리 간* (Core ↔ n6 ↔ TECS-L
  ↔ SEDI ↔ anima 의식) 모두 ≥ 0.55 — 단일 카테고리 monopoly 차단.
- **C5 REPRODUCIBLE SEED**: seed 변경 (≥ 3 seed) 에 대해 `mean(phi_lens)` 부호 보존 ≥ 95%.

## 5. Falsifiers (F1-F5)

- **F1**: K=10 smoke 에서 Φ_lens > 0 비율 ≤ 4/10 → "discovery engine 가속 가설" 즉시 sink
  (Hc_586 1000x 주장 wrong direction).
- **F2**: K=50 의 cross_lens_agreement < 0.50 → lens 가 random walk 와 구분 안 됨 (Hc_960
  mislabel-by-noise 가능성).
- **F3**: Bonferroni 적용 후 *어떤* lens 도 q < 0.05 통과 못함 → 1013 lens count 가 multiple
  comparison nightmare (H_135 honest_limits #1 의 실현).
- **F4**: n6-consistency ratio < 10/50 → Hc_378 의 "n=6 primitive basis" 가 1013-lens 에서
  generalize 안 됨 → DD166/Hc_586/Hc_598 cluster 전체 weaken.
- **F5**: seed 변경 시 부호 보존 < 70% → deterministic 주장 (frontmatter `deterministic: true`)
  자체가 false → H_135 frontmatter revision 필요.

## 6. Honest Limits (L1-L5)

- **L1**: 1013 lens 중 본 spec 은 top-50 (~5%) 만 검증. 나머지 96.1% lens 의 validity 는
  본 cycle 에서 *unverified*. (H_135 본문 honest_limit #2 인용.)
- **L2**: Atlas auto-connect 6 lens 는 *meta* — circular reasoning risk (H_135 본문 #3).
  본 spec 은 명시적으로 Atlas overlay 제외.
- **L3**: 1013-lens full-scan 의 computational cost 는 본 spec 에서 미산정 (H_135 본문 #5).
  K=50 까지의 비용은 anima Φ★ engine 측정 가능 시 추가 collateral.
- **L4**: K-step 의 lens 선정은 *category-stratified manual* — random sampling 대비
  selection bias 잔존. K=50 시 random-50 baseline 비교 권고.
- **L5**: prereq P-B (proxy harness) 경로는 nexus.qmirror (Hc_944) / IonQ QRNG (Hc_945)
  entropy 보장 없음 — pseudo-random fallback 시 F5 falsifier 의 sensitivity 감소 가능.

## 7. 활성화 Decision Tree

```
prereq check
├── P-A2 available → activate full lane (K=10→25→50), eval C1-C5, check F1-F5  ← 권고
├── P-B available  → proxy lane (K=10→25 만, K=50 deferred), partial C1
├── P-A1 only      → single-axis Φ* lane (별 cluster: Hc_586/598), K-cascade *불가*
└── neither        → freeze spec, H_135 status unchanged (legacy-archive-pointer)
```

C1 charged → H_135 verdict_class 갱신:
- C1 + C3 PASS + no falsifier → `1013-lens-activation-K50-PASS` (status `running`)
- C1 PASS + F2/F4 trip       → `1013-lens-activation-partial-with-caveats`
- F1 또는 F3 또는 F5 trip    → `1013-lens-activation-FALSIFIED` (Hc_586/598 weaken)

plan: cascade_k25_plan_2026_05_12.md (K=25 canary cascade plan — cycle 5 §3 #E, 2026-05-12)

## 8. Cycle-3 NEXUS Hc Cross-Reference

본 spec 은 다음 Hcs 의 활성화/검증 vehicle 이다:

| Hc      | Role                                                              |
|---------|-------------------------------------------------------------------|
| Hc_586  | 1000x+ 가속 주장 — F1 falsifier 직접 검증                         |
| Hc_598  | 16/22/1013 progressive expansion — C4 cross-cluster agree 검증    |
| Hc_035  | NEXUS-6 cross-validation (Ising/Stefan-Boltzmann/Ω_m:Ω_Λ) — C2/C4 |
| Hc_378  | n=6 primitive basis 98181 closure — C2 binding                    |
| Hc_437  | Meta fixed-point iso (R24) — merged-to-H_067, 본 lane 외 추적     |
| Hc_944  | nexus.qmirror — P-B proxy harness 의 entropy backend (optional)   |
| Hc_945  | IonQ QRNG seed — P-A1 엄격 모드의 seed source                     |
| Hc_960  | 20-lens mislabel caveat — C3 no-mislabel-drift 직접 동기 (§11 참조) |

**1013 vs 1,588 lens count drift caveat**: spec.md §0 의 "1013" 은 DD166 *registry-design*
공식 라벨이지만, disk 실측 (`/Users/ghost/core/nexus/lenses/*.hexa`) 은 1,588 file.
Hc_960 mislabel-by-mixed-count 가설은 2026-05-11 cycle 5 #4 prereq audit (§2.2) 에서
*실증*. SSOT: §11 참조 — `lens_registry.json` 또는 `core_*.hexa` prefix 기준 K=10 whitelist
(§3.1) 가 binding.

## 9. Lock Policy

User directive 2026-05-11: chflags +uchg/+schg/chattr +i **금지**. 본 spec 및 H_135
frontmatter 의 frozen_at 은 *논리적 freeze* 일 뿐, OS-level lock 미적용.

## 10. Non-Goals

- 본 spec 은 1013-lens *전수* 검증 protocol 이 아니다 (top-K only).
- nexus.qmirror Bell test / IIT φ_MIP 검증은 별 lane (Hc_944/945) 으로 분리.
- 337 신규 acceleration hypothesis full-scan 은 본 spec 의 scope 외 (DD166 §5 의 next-step).
- P-A1 (anima_phi_star.hexa cosmic-scale extension) 의 실행은 본 spec 외 — Hc_586/598
  별 lane.

## 11. SSOT — Lens Whitelist & lens_registry.json

| source | path | status | usage |
|--------|------|--------|-------|
| nexus `lens_registry.json` (v2.0) | `/Users/ghost/core/nexus/config/lens_registry.json` | **exists** (4,000 lens, BLOW-P9-1 expansion 1576→4000 ossify, `.rs` 기준) | 1013 official whitelist 와 *layer 다름* — `.rs` Rust impl 의 registry. K=10 hexa-side와 별도 axis. |
| nexus hexa lens files | `/Users/ghost/core/nexus/lenses/core_*.hexa` | 23 files (disk-actual) | §3.1 K=10 whitelist 의 source |
| spec.md §3.1 | 본 문서 | 10 files 명시 | **K=10 binding whitelist** |
| `acceleration_hypotheses.json` _meta.nexus_upgrade | `config/acceleration_hypotheses.json` | TBD (P-B path 용) | P-B fallback 시 적용 |
| `nexus/lens_registry.json` (1013-official) | (없음) | **TBD** | 1013 official label 의 hexa-side SSOT 미정 — risk #5 (audit) active |
| synthesized lens registry | `/home/summer/core/nexus_lenses_snapshot/lens_registry.json` | **synthesized 2026-05-12** | 1588 hexa, sha256 audit trail, K=10 binding 10/10 PASS — see `lens_registry_synthesized_2026_05_12.md` (1588 hexa, sha256 audit trail) |

**Decision (2026-05-11)**:
- K=10 / K=25 / K=50 cascade 의 binding source = §3.1 whitelist (file path 기준)
- 1013 vs 4000 vs 1588 의 layer mismatch resolution 은 *별 spec* (nexus repo 측 coordination
  필요) — 본 spec 은 hexa-side 23 core files 기준으로 lock.
- `lens_registry.json` (4000 lens, `.rs`) 은 reference only — K-cascade 의 acceptance gate
  에는 invoke 하지 않음.
