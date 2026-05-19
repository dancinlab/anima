---
plan_id: nexus6_1013lens_cascade_k25_plan_2026_05_12
spec_id: nexus6_1013lens_activation_2026_05_11
parent_spec: state/nexus6_1013lens_activation_2026_05_11/spec.md
target_h: H_135 (DD166 NEXUS 1013-lens discovery engine)
status: design-only (NO actual run; K=10 PASS confirmation required first)
cycle: 5 §3 #E
authored: 2026-05-12
authored_by: agent
lock_policy: NO chflags/chattr — repository directive 2026-05-11
---

# K=25 Canary Cascade Plan — NEXUS-6 1013-lens Activation

본 문서는 spec §3 Protocol cascade 의 *두 번째 step* (K=10 → **K=25** → K=50) 을 위한
*design-only* plan 이다. K=25 canary run 의 lens selection, criteria, falsifiers, decision
tree, cost, aggregator update path 를 정의한다. **본 plan 은 실제 K=25 실행을 포함하지
않는다** — canonical K=10 smoke (cycle 5 §3 #A) PASS 확정 후 다음 cycle 에서 본 plan 에
기반하여 실행한다.

## 0. Context & Prereq

K=25 canary cascade 진입 *전* 충족되어야 할 prereq:

| prereq | 출처 | 상태 |
|--------|------|------|
| K=10 canonical smoke PASS | cycle 5 §3 #A — Agent A | pending (#A in flight) |
| K=10 whitelist binding | spec §3.1 (2026-05-11 확정 — 10 file paths) | confirmed |
| lens snapshot Linux-native | `/home/summer/core/nexus_lenses_snapshot/` (23 core_*.hexa) | exists (mount-independent) |
| lens_registry.json synthesized | cycle 5 §3 #B — Agent B | pending (#B in flight) |
| Φ★ vs Φ_lens naming separation | cycle 5 §3 #C — Agent C | pending (#C in flight) |
| **lens input channel reimpl** (K=10 Phase 1 PASS — F-reimpl-1/2/3 통과) | cycle 5 §4 #F `lens_channel_reimpl_spec_2026_05_12.md` | **strict** — K=10 trivial caveat (Agent 21) 해소 binding |

본 plan 은 위 *5* 항 (channel reimpl strict 추가) 의 *완료* 를 가정하고 design 한다.
prereq 미충족 시 K=25 cascade 자체가 non-binding 이며 본 plan freeze. 특히 channel reimpl
미완료 상태에서 K=25 진행 시 동일 trivial 결과가 K=25/K=50 까지 propagate (caveat
investigation §0).

K=10 PASS 의 정의 (spec §3 + smoke aggregator §0): `positive_ratio ≥ 0.6` AND
`phi_mean > 0` AND F1 floor breach 없음. 이미 dry-run 에서 c1_gate=True 신호 (Agent 17)
이지만 canonical run (Agent A) 의 legitimacy 확인이 binding.

## 1. K=25 Lens Selection — +15 expansion

selection axis (spec §3.1 확장): K=10 의 **fundamental measurement primitives** 축을 유지하면서,
n=6 primitive basis (Hc_378) 의 closed-form check 가능 lens 를 *cross-validation primitive*
방향으로 +15 추가. 우선 23 `core_*.hexa` 중 K=10 외 13 lens 를 *전수 포함* (selection bias
최소화), 그 위에 K=10 의 axis 와 직교하는 영역 2 추가.

### 1.1 retained K=10 (carry-over)

spec §3.1 의 10 lens (C3 no-mislabel-drift binding 유지):

```
core_info, core_causal, core_consciousness, core_thermo, core_quantum,
core_topology, core_gravity, core_network, core_scale, core_stability
```

### 1.2 added +13 (core_*.hexa exhaustive)

K=10 외 *모든* `core_*.hexa` 13 file (snapshot 디렉터리 alphabetical):

| # | lens basename | axis | 선정 이유 (selection axis 확장) |
|--:|---------------|------|--------------------------------|
| 11 | `core_boundary.hexa` | geometry/boundary | manifold boundary detection — core_topology cross-validation |
| 12 | `core_chaos.hexa` | dynamics/chaos | Lyapunov / deterministic chaos — core_stability null contrast |
| 13 | `core_compass.hexa` | directional/coord | reference frame / orientation — n6 primitive auxiliary axis |
| 14 | `core_em.hexa` | electromagnetism | EM coupling closure — physics axis (Hc_035 cross-validation) |
| 15 | `core_evolution.hexa` | evolution/selection | adaptive dynamics — core_causal cross-validation |
| 16 | `core_memory.hexa` | memory/retention | temporal info retention — core_consciousness cross-validation |
| 17 | `core_mirror.hexa` | symmetry/reflection | parity / mirror symmetry — Hc_944 qmirror axis 일치 |
| 18 | `core_multiscale.hexa` | multiscale | scale-bridging — core_scale cross-validation (Hc_378) |
| 19 | `core_quantum_microscope.hexa` | quantum-fine | quantum sub-structure — core_quantum cross-validation |
| 20 | `core_recursion.hexa` | recursion | self-reference — Hc_437 fixed-point iso axis |
| 21 | `core_ruler.hexa` | measurement | metric / measurement substrate — n6 primitive base |
| 22 | `core_triangle.hexa` | geometry/relational | triangulation closure — n6 primitive (3-body) |
| 23 | `core_wave.hexa` | wave/oscillation | oscillatory dynamics — core_quantum/core_em cross-validation |

→ source: `/home/summer/core/nexus_lenses_snapshot/core_*.hexa` (Linux-native snapshot,
mount-independent — prereq audit §3.1).

### 1.3 added +2 (cross-category extension)

n=6 primitive 의 *cross-category sample* — Hc_598 의 16→22→1013 progressive expansion
중 next-tier (n6 산업 + anima 의식) 1 each:

| # | lens basename | category | axis | 선정 이유 |
|--:|---------------|----------|------|----------|
| 24 | `n6_*.hexa` (top-1 from `n6_industry_*` alphabetical) | n6 산업 | DSE/소재/동역학 | spec §3 K=25 protocol 의 "n6 산업 top-3" 중 top-1 (canary tier) |
| 25 | `anima_*.hexa` (top-1 from anima 의식 alphabetical) | anima 의식 | 감질/결합 | H_135 의식 axis 의 direct extension (core_consciousness 외 second sample) |

→ 정확한 basename 은 K=25 실행 시 `ls /home/summer/core/nexus_lenses_snapshot/n6_*.hexa | head -1`
및 `ls /home/summer/core/nexus_lenses_snapshot/anima_*.hexa | head -1` 로 deterministic
선정 (alphabetical-stable). spec §3 의 K=25 명세 ("Core 22 + n6 산업 top-3") 와 *완전 매칭은
아니다* — 본 plan 은 **23 core (전수) + 2 cross-category** (n6 1 + anima 1) 로 *변형*
하여 selection bias 를 더 줄인다. spec §3 와 *차이* 는 §8 L1 에 honest limit 로 기록.

### 1.4 whitelist source binding

K=25 binding source:

1. **primary**: 본 §1 (cascade_k25_plan_2026_05_12.md §1.1+§1.2+§1.3) — 25 basename 명시
2. **secondary** (만약 Agent B 가 lens_registry.json 에 `k25_binding` field 추가 시):
   `state/nexus6_1013lens_activation_2026_05_11/lens_registry.json` `.k25_binding` array
3. **C3 no-mislabel-drift**: 실제 호출 lens 의 file path-level 매칭 100% 요구 (K=10 과 동일)

primary 와 secondary 불일치 시 primary (본 §1) 가 binding — spec §11 SSOT 정책과 일관.

## 2. K=25 Criteria — Monotonic Improvement vs K=10

K=10 의 acceptance gate (`pos_ratio ≥ 0.6`, `phi_mean > 0`, `cross_lens_agreement ≥ 0.55`)
를 K=25 에서 *상향 조정*. lens 수가 증가하면 statistical power 증가 → threshold 강화가
discovery engine 가속 가설 (Hc_586) 의 *증거* 가 된다.

| ID | criterion | K=10 | K=25 | 강화 이유 |
|----|-----------|-----:|-----:|----------|
| **C1** | cascade gate (positive_ratio monotone) | ≥ 0.6 | ≥ `max(pos_ratio_K10, 0.7)` | canary tier 강화 + K=10 PASS 값 floor |
| **C2** | phi_mean | > 0 | > 0 (carry-over) AND `≥ 0.9 × phi_mean_K10` | regression guard (F3 와 paired) |
| **C3** | cross-lens agreement | ≥ 0.55 (K=10 floor) | **≥ 0.50** (lens 수 증가로 분산 ↑ expectation) | spec §3 의 0.65 (K=25) target 보다 *완화* — `core_*` 23 의 axis 다양성 고려 |
| **C4** | Bonferroni (informational at K=25) | reported (α=0.05/1013) | reported AND **α=0.05/25 = 0.002** within-K=25 | within-batch multiple comparison correction |
| **C5** | C3 no-mislabel-drift | 10/10 path match | 25/25 path match | strict (spec §4 C3 binding) |

> **note (C3 relaxation 정당화)**: spec §3 의 "cross_lens_agreement 0.65 (K=25)" 는
> *category-stratified* assumption 하의 target. 본 plan §1 의 selection 은 *core_* 23
> 전수 + 2 cross 라서 axis 다양성이 더 큼 → pairwise sign-correlation 분산도 더 큼 →
> 0.65 floor 는 over-tight. 따라서 본 plan 은 *0.50* 로 relax 하되, spec §3 와의 *차이* 를
> §8 L2 (cross-lens agreement 정의 mismatch) 에 honest limit 로 기록.

## 3. K=25 Falsifiers

K=10 의 F1 (positive_ratio ≤ 0.4) 와 paired 로, K=25 에서 *regression / instability* 신호:

| ID | falsifier | trip 조건 | trip 시 결과 |
|----|-----------|----------|--------------|
| **F1** | floor breach | `pos_ratio_K25 ≤ 0.5` | "K=10 → K=25 expansion 실패" — Hc_586 1000x 주장 weaken |
| **F2** | random-walk null | K=25 score 분포 vs random null score 분포의 KS-test `p ≥ 0.05` | lens = random walk 와 구분 안 됨 (Hc_960 mislabel-by-noise 실현) |
| **F3** | mean regression | `phi_mean_K25 < 0.8 × phi_mean_K10` | K=10 → K=25 expansion 이 mean signal 을 *감쇠* — selection bias 의 reverse |
| **F4** | outlier dominance | top-3 lens 가 K=25 mean 의 ≥ 60% 차지 | single-lens dependency — K=10 의 high pos_ratio 가 sampling artifact |
| **F5** | cross-category disagreement | core (23) 와 n6+anima (2) 의 mean 부호 불일치 | spec §4 C4 cross-cluster-agree 의 *조기 신호* (K=50 에서 binding) |

F1 또는 F2 trip → C1 cascade halt. F3, F4 trip → investigation (K=10 가짜 PASS 의심).
F5 trip → K=50 전 cross-category sample 확대 권고.

### 3.1 F2 random-walk null distribution 합성 방법 (미결정)

null distribution 합성 방법 (Monte Carlo vs analytic) 은 본 plan 에서 *미결정*. 후보:

- **MC option**: random seed 으로 score ∈ [-1, 1] uniform sample 25 회 × 1000 trial → KS-test
- **analytic option**: lens score 의 binomial null (p=0.5 sign) 가정 → exact distribution
- **bootstrap option**: K=10 의 10 score 를 25 회 with-replacement sample → 자기 null

→ §8 L3 honest limit. 본 plan 은 *MC option* 을 default 로 추천 (재현성 + seed 명시 + spec §6
L5 entropy fallback 과 호환).

**F2 null synthesis spec**: see `f2_null_synthesis_spec_2026_05_12.md` (recommended: hybrid MC/bootstrap/analytic)

## 4. Cascade Decision Tree

```
K=10 canonical PASS (Agent A)
        │
        ▼
   K=25 canary
        │
   ┌────┴────┐
   ▼         ▼
 ALL_OK    F[1-5]
   │         │
   ▼         ▼
 K=50      branch:
 pilot       F1 → ROLLBACK to K=10 (Hc_586 weaken)
             F2 → null-calibration cycle (F2 §3.1 결정)
             F3 → INVESTIGATION (K=10 가짜 PASS 의심)
             F4 → outlier removal + re-run K=25 (single lens dependency 제거)
             F5 → K=25 cross-category expansion (n6+anima 1 → 3+3 each)
```

K=10 FAIL 또는 미실행 → 본 plan **전체 무의미** (cascade halt at smoke).

## 5. K=25 Cost & Wall Time

| 항목 | 값 | 비고 |
|------|-----|-----|
| single-lens cost (sequential) | ~19 ms | prereq audit §2.3 measured |
| K=25 sequential wall | ~475 ms | 25 × 19 ms (no overhead) |
| K=25 parallel wall (8-way subprocess pool) | ~50–80 ms | (25/8) × 19 ms + pool overhead |
| GPU | 0 | CPU-only hexa eval |
| RunPod / cloud cost | $0 | local Linux runner |
| disk I/O | < 1 MB | 25 stdout × ~100 bytes |
| memory peak | < 100 MB | 8 concurrent hexa interpreter (worst case) |

→ K=25 canary 의 cost-to-information ratio 는 *극단적으로 cheap*. **bias warning**: 너무 cheap
이면 measurement legitimacy 가 의심받을 수 있다 (Agent A 의 pos_ratio=1.0 caveat 와 동일
risk). §8 L4 참조.

### 5.1 timing budget allocation

- aggregator update (rename + parameterize): ~30 분 (§6)
- K=25 canary run: < 1 초
- post-run analysis (F1-F5 evaluation, decision tree branch 결정): ~10 분 manual
- total cycle: < 1 시간 (aggregator 완료 후)

## 6. Aggregator Update Path

현 `tool/anima_nexus_1013lens_smoke.hexa` 는 K=10 hardcoded. K=25 (그리고 K=50) 를 위한
parameterize 가 필요.

### 6.1 옵션 비교

| 옵션 | 설명 | 장점 | 단점 |
|------|------|------|------|
| **A. rename + parameterize** | `anima_nexus_1013lens_smoke.hexa` → `anima_nexus_1013lens_cascade.hexa`, `--k 10/25/50` flag 추가 | single source of truth, back-compat 가능 | rename overhead, K=10 인 hardcoded reference 갱신 필요 |
| **B. new dedicated file** | `tool/anima_nexus_1013lens_canary.hexa` (K=25 전용) | smoke 파일 무수정, blast radius 작음 | code duplication (~80%), 3 cycle 후 K=50 시 또 새 파일 → DRY 위반 |
| **C. in-place K=25 extension** | smoke 파일에 `--k` flag 만 추가 | minimal diff | naming mismatch (file=smoke but K=25) — semantic drift |

### 6.2 권고 — 옵션 A (rename + parameterize)

**근거**:

1. single source of truth (spec §11 SSOT 정책과 일관)
2. K=10/25/50 cascade 가 *같은 logic* 의 *다른 K* — code reuse 자연스럽다
3. back-compat: `--k 10` (default) 면 기존 smoke 와 identical 동작 → existing references 부분
   migration

**변경 detail**:

- file rename: `tool/anima_nexus_1013lens_smoke.hexa` → `tool/anima_nexus_1013lens_cascade.hexa`
- flag 추가: `--k {10|25|50}` (default 10, back-compat)
- whitelist source 분기:
  - K=10 → spec §3.1 (현 hardcoded list)
  - K=25 → 본 plan §1 (25 basename)
  - K=50 → spec §3 + 추가 plan (별 cycle)
- env override `ANIMA_LENS_WHITELIST` 는 *전 K 공통* 유지
- output filename 변경: `smoke_k{N}_results.json` 또는 `cascade_k{N}_canonical_{date}.json`
  (canonical run convention 따름)
- helper file: `/tmp/anima_nexus_1013lens_cascade_helper.hexa_tmp`
- selftest: `--k` flag 도 invariant 출력

**migration risk** (수정 시 confirm):

- smoke_k10_canonical_2026_05_12.json 의 schema 호환성 (k=10 field 는 유지)
- 기존 `c1_smoke_gate` field name → `c1_cascade_gate_k{N}` 로 generic 화 (또는 K 별 alias)
- references (`spec.md §3`, `prereq_audit §4`) → file rename 후 1 줄 수정 (minimal blast)

→ 본 plan **권고: 옵션 A**.

## 7. Decision Matrix

K=10 결과와 K=25 결과의 조합별 다음 step:

| K=10 결과 | K=25 결과 | next step | rationale |
|-----------|-----------|-----------|-----------|
| PASS | PASS (ALL_OK) | → K=50 full-pilot (별 plan 작성) | spec §3 cascade 정상 진행 |
| PASS | F1 (floor breach) | → INVESTIGATION (K=10 가짜 PASS 의심) + ROLLBACK 검토 | K=10 → K=25 sudden regression → selection bias 의심 |
| PASS | F2 (random-walk) | → null-distribution 정밀 calibration (§3.1 MC vs analytic 결정) | F2 자체가 spec §5 의 F2 와 동일 동기 |
| PASS | F3 (mean regression) | → outlier 분석 + K=10 lens 검증 (개별 score 재확인) | mean 감쇠는 K=10 outlier dominance 신호 |
| PASS | F4 (outlier dominance) | → top-3 lens 제외 후 K=22 재실행, F4 재검 | single-lens dependency 분리 |
| PASS | F5 (cross-category) | → K=25 의 cross-category sample 확대 (2 → 6) | spec §4 C4 의 조기 신호 |
| FAIL | (irrelevant) | 본 plan 무의미 (cascade halt at smoke) | K=10 FAIL → cascade rollback |
| (미실행) | (미실행) | Agent A 결과 대기 | prereq 미충족 |

## 8. Honest Limits

| ID | limit | 설명 |
|----|-------|-----|
| **L1** | selection axis 동질성 | K=10 → K=25 의 selection axis 가 `core_*` family 내부 *전수* 포함 → 다양성이 *intra-family* 로 제한. spec §3 의 "Core 22 + n6 산업 top-3" 와 *차이* (본 plan 은 core 23 + cross-cat 2). cross-category sample 이 2 개로 빈약 → C4 cross-cluster-agree 의 *조기 검출* 한계 |
| **L2** | cross-lens agreement 정의 | pairwise sign-correlation proxy (smoke aggregator §165-172 구현) 가 spec §2 의 *K-NN agreement* 정확 매핑 아님. proxy 와 real K-NN agreement 의 conversion factor 미정 → C3 threshold (0.50) 의 *절대값 의미* 가 약함 (monotonic 만 의미 있음) |
| **L3** | F2 null distribution 합성 미결정 | §3.1 의 MC/analytic/bootstrap 3 option 중 default 만 추천 (MC). 실제 implementation 시 결정 필요 |
| **L4** | cost legitimacy bias | K=25 wall < 1 초, $0 — 너무 cheap. Agent A 의 pos_ratio=1.0 (모든 lens score=1) 같은 *artifact* 가 K=25 에서도 발생 가능 → "measurement = check-all-passes" 의심 risk. mitigation: F4 outlier dominance + score 분포 확인 + raw stdout 검증 |
| **L5** | F1 vs F3 dependency | F1 (floor breach) 와 F3 (mean regression) 가 paired (둘 다 monotonic improvement 부재 신호). single-trip 정의로 충분한지 불명 — 두 falsifier 가 *redundant* 일 수 있음 |
| **L6** | spec §3 K=25 명세와의 차이 | spec §3 은 "Core 22 + n6 산업 top-3 lens" 명시. 본 plan 은 "core_* 23 (전수) + n6 top-1 + anima 의식 top-1" = 25. spec 과 정확 매칭은 아니지만 *selection bias 완화* 방향 (전수 포함). spec §3 갱신 또는 본 plan 의 *deviation* 명시 결정 필요 (메인 process) |

## 9. Cross-Reference

| ref | path | 관계 |
|-----|------|-----|
| K=10 spec §3.1 (Agent 18 확정) | `state/nexus6_1013lens_activation_2026_05_11/spec.md` §3.1 | K=25 carry-over base |
| K=10 canonical smoke (Agent A — cycle 5 §3 #A) | `state/nexus6_1013lens_activation_2026_05_11/smoke_k10_canonical_2026_05_12.json` | K=25 prereq |
| lens_registry synthesized (Agent B — cycle 5 §3 #B) | `state/nexus6_1013lens_activation_2026_05_11/lens_registry.json` (pending) | K=25 secondary whitelist source |
| Φ★ naming refactor (Agent C — cycle 5 §3 #C) | spec.md §1 P-A1/P-A2 + §2 axis caveat | naming convention (nexus_lens_score vs anima_phi_star) 일관 |
| parent spec §3 Protocol cascade | spec.md §3 | K=25 의 design baseline |
| parent spec §7 Decision tree | spec.md §7 | 본 plan §4 decision tree 의 source |
| cascade aggregator (renamed 2026-05-12 cycle 5 §4 #H) | `tool/anima_nexus_1013lens_cascade.hexa` | §6 옵션 A executed — K-cascade SSOT |
| prereq audit | `state/nexus6_1013lens_activation_2026_05_11/prereq_audit_2026_05_11.md` §2.3 | K=25 cost estimate substrate |
| Hc cluster | Hc_586 (가속), Hc_598 (progressive expansion), Hc_035 (cross-validation), Hc_378 (n6 basis), Hc_960 (mislabel) | K=25 가 직접 검증하는 Hcs |
| lock policy | memory: feedback_no_relock.md 2026-05-11 | chflags/chattr 적용 금지 (본 plan 작성 과정에서 무적용 확인) |

## 10. Non-Goals (본 plan 범위 밖)

- 실제 K=25 canary run — 별 cycle (K=10 PASS 후)
- K=50 full-pilot plan — 별 plan 작성 (K=25 PASS 후)
- aggregator rename/parameterize 실제 commit — 본 plan 은 *권고만*
- F2 null distribution 의 final 결정 (MC/analytic/bootstrap) — implementation cycle 결정
- spec §3 갱신 결정 (본 plan §8 L6 deviation 정책) — 메인 process 결정
