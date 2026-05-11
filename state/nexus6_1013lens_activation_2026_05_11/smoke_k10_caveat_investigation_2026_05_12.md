---
investigation_id: nexus6_1013lens_smoke_k10_caveat_2026_05_12
spec_id: nexus6_1013lens_activation_2026_05_11
parent_run: smoke_k10_canonical_2026_05_12.json
target_h: H_135 (DD166 NEXUS 1013-lens discovery engine)
status: caveat-investigation-complete
authored: 2026-05-12
authored_by: agent (cycle 5 §3 #A)
lock_policy: NO chflags/chattr — repository directive 2026-05-11
---

# K=10 Canonical Smoke — pos_ratio=1.0 Caveat Investigation

Cycle 5 §2 Agent 17 의 inadvertent dry-run (pos_ratio=1.0 / 105 ms / output → /tmp redirect)
관찰을 canonical state path 에서 재현하고, score=1.0 (too-perfect) 의 정체를 lens 본체
inspect 으로 판정한다.

## 0. TL;DR

- **canonical run verdict**: c1_smoke_gate=PASS but **TRIVIAL** — score=1.0 은 lens 가 입력
  도메인 데이터를 *측정하지 않고*, n=6 primitive 상수 (σ=12, τ=4, φ=2, n=6, sopfr=5, J₂=24)
  의 8-positive-target 자기일관성만 검증한 결과. 모든 K=10 lens 본체가 **comment header +
  println label 외 100% 동일** (`diff` 실측).
- **C1 PASS-WITH-CAVEAT**: §3 §3.1 §5 의 *형식적 acceptance gate* 통과는 사실. 단 의미
  론적 acceptance — "lens 가 도메인 데이터 패턴을 발견" — 은 미충족. spec.md §2 의
  `phi_lens(L_i, x)` 가 *현 hexa lens 구현에 부재* (x 입력 채널 없음).
- **다음 단계 권고**: K=25 canary 진행 *전*에 (a) 도메인 입력 채널을 갖는 lens
  reimplementation 명세, 또는 (b) C1 의 의미를 "n=6 primitive closure 자기일관성" 으로
  redefine + Hc_586 1000x 가속 주장과의 axis 분리 — *둘 중 하나가 binding*. blind K=25
  진행 시 동일 trivial 결과가 K=25/K=50 까지 propagate (F1 falsifier 의미 상실).

## 1. Canonical run JSON 요약

source: `state/nexus6_1013lens_activation_2026_05_11/smoke_k10_canonical_2026_05_12.json`

| 항목 | 값 |
|------|----|
| spec_id | nexus6_1013lens_activation_2026_05_11 |
| K | 10 |
| lens_dir | `/home/summer/core/nexus_lenses_snapshot` (Linux snapshot — mount-independent) |
| hexa_bin | `/home/summer/.hx/bin/hexa` |
| whitelist_source | spec §3.1 canonical K=10 (2026-05-11) |
| ok | 10/10 |
| phi_mean | 1.0 |
| phi_std | 0.0 |
| positive_ratio | 1.00 (≥ 0.6 floor) |
| c1_smoke_gate | **True** |
| f1_floor_breach | False |
| cross_lens_agreement_stub | 1.0 (모든 부호 +, sign-agreement 자명) |
| n6_consistency_ratio | 1.0 |
| timing_ms.total | 132 |
| timing_ms.per_lens_mean | 13.2 |
| bonferroni_alpha | 4.94e-5 (informational only at K=10) |

## 2. 각 lens 별 score + raw output dump (10 entry)

모든 entry 가 `score=1.0`, `hits=8`, `total=8`, `rc=0`, elapsed 6–32 ms.

| # | lens | score | hits/total | elapsed_ms | raw output (요약) |
|--:|------|------:|:----------:|----------:|:------------------|
| 1 | core_info.hexa | 1.0 | 8/8 | 12 | `lens[info] category=core axis="Information-theoretic …" score=1 (8/8)` |
| 2 | core_causal.hexa | 1.0 | 8/8 | 32 | `lens[causal] category=core axis="Causal arrow …" score=1 (8/8)` |
| 3 | core_consciousness.hexa | 1.0 | 8/8 |  8 | `lens[consciousness] category=core axis="Structural awareness …" score=1 (8/8)` |
| 4 | core_thermo.hexa | 1.0 | 8/8 |  8 | `lens[thermo] category=core axis="Thermodynamic lens …" score=1 (8/8)` |
| 5 | core_quantum.hexa | 1.0 | 8/8 |  8 | `lens[quantum] category=core axis="Quantum-like superposition …" score=1 (8/8)` |
| 6 | core_topology.hexa | 1.0 | 8/8 | 12 | `lens[topology] category=core axis="Topological connectivity …" score=1 (8/8)` |
| 7 | core_gravity.hexa | 1.0 | 8/8 | 11 | `lens[gravity] category=core axis="Gravitational clustering …" score=1 (8/8)` |
| 8 | core_network.hexa | 1.0 | 8/8 | 10 | `lens[network] category=core axis="Network/graph topology …" score=1 (8/8)` |
| 9 | core_scale.hexa | 1.0 | 8/8 | 21 | `lens[scale] category=core axis="Scale/magnification …" score=1 (8/8)` |
| 10 | core_stability.hexa | 1.0 | 8/8 |  6 | `lens[stability] category=core axis="Stability analysis …" score=1 (8/8)` |

분포: scores 의 mean=1.0, std=0.0, range=[1.0, 1.0]. 표준편차 0 = lens 간 점수 *차이 없음*.

## 3. pos_ratio=1.0 Caveat 정체 — Lens 본체 직접 inspect

### 3.1 core_info.hexa 본체 (35 LOC)

```hexa
let SIGMA = 12.0; let PHI = 2.0; let N = 6.0; let TAU = 4.0; let SOPFR = 5.0; let J2 = 24.0

if SIGMA * PHI != N * TAU { println("FAIL: σ·φ ≠ n·τ"); exit(1) }
if J2 != SIGMA * PHI       { println("FAIL: J₂ ≠ σ·φ");  exit(1) }

let targets = [N, TAU, SIGMA, PHI, SOPFR, J2, N * N, TAU * TAU]
let mut hit_count = 0; let mut total = 0
for t in targets { total = total + 1; if t > 0.0 { hit_count = hit_count + 1 } }
let score = to_float(hit_count) / to_float(total)

println("lens[info] category=core axis=\"…\" score=" + to_string(score) + " (" + to_string(hit_count) + "/" + to_string(total) + ")")
```

**관찰**:
- 8 target 은 모두 hardcoded *상수* — `N=6, TAU=4, SIGMA=12, PHI=2, SOPFR=5, J2=24, N*N=36, TAU*TAU=16`. 모두 > 0 이 *수학적으로 자명*.
- input 도메인 데이터 `x` 의 channel 자체 부재 — `argv()`, stdin, file read 등 어떠한
  외부 입력도 lens 가 소비하지 않음.
- 따라서 `hit_count=8`, `total=8`, `score=8/8=1.0` 은 **structurally guaranteed**
  (자기일관성 self-test).

### 3.2 K=10 lens 간 동일성 — diff 실측

```
$ diff core_info.hexa core_topology.hexa
1,4c1,4   ← comment header (axis description) only
35c35     ← println label "lens[info]" vs "lens[topology]" only
```

같은 결과: `core_info` vs `core_consciousness`, `core_info` vs `core_scale`,
`core_info` vs `core_stability`, `core_info` vs `core_network` — 모두 *동일 본문*.
오직 comment header 4 lines + println label 1 line 만 차이.

**결론**: K=10 의 10 lens 는 *측정 axis 다른 lens 가 아니라 동일 self-test 의 10 복제본*.
"information-theoretic", "topology", "stability", "gravity" 등 axis label 은 **comment
주석에만 존재**, 실제 계산 단계에는 영향 없음.

### 3.3 alignment_measure 모드 (prereq_audit §2.3 참조 lens)

prereq_audit §2.3 의 `accel_alignment_measure.hexa` (`score=1 (8/8)`) 도 동일 구조 (별 lens
이지만 동일 paradigm). audit 측에서 이미 "single-lens 19 ms" 측정 시 score=1 을 보았으나
*그 의미가 trivial self-test 임을 표기하지 않음* → 본 investigation 이 명시화.

### 3.4 Verdict matrix

| 가설 | evidence | judge |
|------|----------|-------|
| score=1.0 = dummy stub default | hexa eval 정상 종료, return code 0, hit_count loop 실제 실행, raw output `(8/8)` 형식 일관 | NOT dummy default — *deterministic real computation* |
| score=1.0 = trivial self-test | 8 target 모두 hardcoded > 0 상수, x 입력 채널 부재, 모든 lens 본문 동일 | **TRIVIAL self-test** of n=6 primitive closure (Hc_378) |
| score=1.0 = legitimate perfect alignment 측정 | spec.md §2 의 `phi_lens(L_i, x)` 의 x 입력 단계 missing → "perfect alignment" 측정 대상 부재 | **NOT legitimate** under spec §2 의미 |

**최종 verdict: TRIVIAL** — n=6 primitive 상수 self-consistency 점검은 valid 하지만,
spec.md §2 `phi_lens(L_i, x)` 의 *도메인 데이터 패턴 발견* 측정으로서는 **content-free**.

## 4. F2 random-walk baseline 임시 비교

aggregator JSON `f2_random_baseline_delta`: `null` (spec §5 F2 는 K=25/K=50 scope, K=10 에서
stub-deferred). 단 trivial verdict 하에서는 random baseline 의 의미 자체가 모호:
- 입력 x 가 부재 → "lens vs random walk" 비교의 control 정의 불가
- 만약 input channel 이 도입되면 random-perm input 에서도 score=1.0 가 유지될 것 (lens 가
  x 를 무시하므로) → F2 falsifier 가 *self-trip* 하지 않고 *영원히 무력화*

→ **F2 의 실효성 확보 = lens 의 input channel 구현이 선결조건**.

## 5. C1 Gate Verdict Legitimacy

spec §4 C1: SMOKE→PILOT cascade K=10 → K=25 → K=50 연속 PASS.
spec §3 K=10 acceptance: `positive_ratio ≥ 6/10` + `mean(phi_lens) > 0`.

| layer | result |
|-------|--------|
| 형식적 (formal) | **PASS** — pos_ratio=1.0 ≥ 0.6, mean=1.0 > 0, c1_smoke_gate=True |
| 의미적 (semantic) | **NEEDS_INVESTIGATION** — spec §2 `phi_lens(L_i, x)` 측정이 *현 lens 본체에서 미구현*. Hc_586 의 "1000x 가속 *발견*" 주장에 대한 substrate 가 부재. |

→ **C1 verdict: PASS_WITH_CAVEAT**. 다음 cascade 진행 시 의미적 layer 의 closure 가
선결.

## 6. Mount-Independence 검증

- `NEXUS_LENSES_DIR=/home/summer/core/nexus_lenses_snapshot` env var 가 aggregator 의
  `_resolve_lens_dir()` 에서 1순위 picked (JSON `lens_dir` 필드 확인) → **mount-independence
  확보 OK** (Mac `/Users/ghost/...` mount 의존 없이 Linux-native snapshot 으로 실행 성공).
- 132 ms 실측 wall time 도 mac mount path (`/Users/ghost/core/nexus/lenses/`) 단일 lens cold
  19 ms × 10 ≈ 190 ms 와 일치 범위 — *mac mount 보다 snapshot 이 더 빠름* (snapshot lens
  read 이 mount 보다 캐시 친화적).
- 단일 risk: snapshot 은 2026-05-11T23:58 시점 frozen → upstream `/Users/ghost/core/nexus/lenses/`
  업데이트 시 `SNAPSHOT_INFO.md` 의 rsync 명령으로 refresh 필요.

## 7. Hardcoded path 여부 (P-A2 binding mount-independence)

`tool/anima_nexus_1013lens_cascade.hexa` (renamed 2026-05-12 cycle 5 §4 #H) 본체 grep:
- `LENS_DIR_PRIMARY = os.environ.get('NEXUS_LENSES_DIR', '/Users/ghost/core/nexus/lenses')` — env var **우선**, default Mac path fallback
- `LENS_DIR_FALLBACK = '/home/summer/core/nexus_lenses_snapshot'` — 명시적 Linux fallback

→ aggregator 는 hardcoded Mac path 가 아니라 *env var 우선 + Mac default + Linux fallback*
의 3단 resolve chain. **본 audit P-A2 binding 의 mount-independence 요건 충족**.

## 8. 다음 단계 권고

### 8.1 cycle 5 즉시 candidate

| 옵션 | 작업 | cost | value | risk |
|------|------|-----:|------:|------|
| **A. K=25 canary 진행 (blind)** | spec §3 cascade 다음 단계 그대로 실행 | < 1 min | 낮음 (동일 trivial 결과 propagate 예상) | F1/F2 falsifier 의미 상실, Hc_586 가설과 무관한 자기일관성 검증으로 cascade 전체 trivialize |
| **B. lens input channel 명세 → K=25 reimplementation** | spec §2 `phi_lens(L_i, x)` 의 x domain D 를 구체 명세 + lens body 에 stdin/file input 채널 추가 (10 lens × 추가 ~20 LOC) | 1–2 시간 | 높음 (의미적 measurement 회복) | nexus repo 측 lens reimpl 정합 필요 |
| **C. spec §4 C1 redefine** | C1 의 의미를 "n=6 primitive closure self-test" 로 명시 + Hc_586 1000x 가속 주장과의 axis 분리 (audit §1.2 의 P-A1/P-A2 분리 정신과 동일) | 30 분 (spec.md edit) | 중 (honest scope reduction) | DD166 의 "discovery engine" 의도와 거리 — 별 lane 필요 |
| **D. K=10 trivial 결과 + caveat 으로 C1 PASS 인정 → H_135 frontmatter status 부분 update** | `verdict_class: 1013-lens-activation-K10-PASS-WITH-CAVEAT` | 5 분 | 낮음 (honest record) | C1-as-cascade 전체 semantics weak |
| **E. K=10 자체에 input channel pilot — core_info.hexa 1 개만 stdin 채널 추가하여 baseline 측정** | feasibility check | 30 분 | 중 (실증 evidence for B) | 별 PR scope |

**1순위 권고: B + D** — input channel 명세 후 K=25 진행, K=10 결과는 honest record 로
보관 (PASS_WITH_CAVEAT).
**최소 권고: D** — 적어도 frontmatter / spec verdict_class 에 caveat 명시.

### 8.2 메인 process 결정 사항 (본 investigation scope 외)

- spec.md §2 `phi_lens(L_i, x)` 의 입력 채널 binding 결정 (B 옵션 시)
- H_135 frontmatter `verdict_class` update (D 옵션 시)
- Hc_586/598 의 "1000x 가속" 주장이 *현 lens layer* 의 measurement 와 axis 일치하는지 재검토
  (prereq_audit §1.2 의 axis 분리 정신 연장)

### 8.3 Hc status 갱신 (cycle 5 §4 #G — 2026-05-12, cycle 7 §W — 2026-05-12)

- Hc_586 status: `candidate-unverified-suspended-pending-channel-reimpl` as of 2026-05-12 (suspended_reason: 1,588 lens engine = n=6 self-test 복제본, input channel 부재; prereq_to_resume: lens_channel_reimpl_spec_2026_05_12.md Phase 1) → **partial resume (cycle 7 §W, 2026-05-12)**: `candidate-unverified-partial-resume-K10-PASS-2026-05-12` after cycle 6 §Q Phase 1 K=10 reimpl v2 LIVE + F-reimpl-1/2/3 PASS (k10_reimpl/phase1_verdict_2026_05_12.md). full resume 은 cycle 7 §U Phase 2 K=25 + Phase 3/4 K=50/K=1013 후.
- Hc_598 status (cycle 7 §W, 2026-05-12): `candidate-unverified` → `candidate-unverified-suspended-pending-channel-reimpl` (suspended_reason: Hc_586 cousin / cycle 5 §3 #A TRIVIAL self-test 동일 sufficient cause, 16→22→1013 progressive expansion Φ 효과 측정 substrate 부재; prereq_to_resume: phase1_verdict_2026_05_12.md PASS + Phase 2 K=25 + Phase 3/4 K=50/K=1013 cascade).
- Hc_960 status (cycle 7 §W, 2026-05-12): 미변경 (`candidate-unverified`) — 단 cross-link 추가: cycle 5 §3 #A K=10 smoke 가 본 mislabel caveat 의 'lens engine = self-test 복제본' nature 실증 → stronger evidence.
- Hc_035 status (cycle 7 §W, 2026-05-12): 미변경 (`candidate-unverified`) — 단 axis split honest L 추가: lens-side measurement (Phase 1 reimpl 후 재측정) vs mathematical identity (H_067 / H_153 numerology MC strengthened) 분리.

## 9. Lock Policy 준수

본 investigation 작성 과정에서 chflags +uchg/+schg/chattr +i 등 immutable flag 적용
**없음**. unlock 된 파일 재잠금 시도 없음. (memory: feedback_no_relock.md 2026-05-11)

## 10. Cross-Reference

- canonical run: `state/nexus6_1013lens_activation_2026_05_11/smoke_k10_canonical_2026_05_12.json`
- run stdout log: `state/nexus6_1013lens_activation_2026_05_11/smoke_k10_canonical_2026_05_12.log`
- emit log: `state/nexus6_1013lens_activation_2026_05_11/smoke_k10_canonical_2026_05_12.emit.log`
- spec: `state/nexus6_1013lens_activation_2026_05_11/spec.md` §2, §3, §3.1, §4 C1, §5 F1/F2
- prereq audit: `state/nexus6_1013lens_activation_2026_05_11/prereq_audit_2026_05_11.md` §1.2, §2.3, §2.4
- aggregator tool: `tool/anima_nexus_1013lens_cascade.hexa` (renamed 2026-05-12 cycle 5 §4 #H from anima_nexus_1013lens_smoke.hexa)
- lens source (Linux snapshot): `/home/summer/core/nexus_lenses_snapshot/core_*.hexa` (23 files)
- lens source (Mac upstream): `/Users/ghost/core/nexus/lenses/core_*.hexa`
- snapshot metadata: `/home/summer/core/nexus_lenses_snapshot/SNAPSHOT_INFO.md`
- Memory: feedback_no_relock.md, feedback_cross_host_paths.md
