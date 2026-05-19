---
audit_id: nexus6_1013lens_prereq_audit_2026_05_11
spec_id: nexus6_1013lens_activation_2026_05_11
target_h: H_135 (DD166 NEXUS 1013-lens discovery engine)
status: feasibility-audit-only (NO GPU/RunPod spend)
authored: 2026-05-11
authored_by: agent (cycle-5 NEXT.md #4)
lock_policy: NO chflags/chattr — repository directive 2026-05-11
---

# NEXUS-6 1013-lens Activation — Prereq Audit

본 문서는 spec.md §1 (Prereq P-A / P-B / P-C) 활성화 조건이 현재 host (Linux x86_64,
`/home/summer/mac_home/core/anima`) 에서 어디까지 충족되는지 *측정* 한 결과이다. 실제 K=10
smoke run 은 본 audit 의 *권고* 만 작성하고, 별도 cycle 에서 진행한다.

## 0. TL;DR

- spec.md 의 P-A (anima cosmic-scale Φ★ engine 직접 측정) 는 **misaligned premise** — anima
  현행 `tool/anima_phi_star.hexa` 는 *single-model IIT-φ proxy* 이고, 1013-lens 측정과는
  서로 다른 measurement axis 이다.
- 실제 1013-lens engine 은 `/Users/ghost/core/nexus/` (Mac 측 nexus repo) 의 *hexa-native*
  구현 (1,588 lens files, telescope.hexa orchestrator) 으로 존재한다.
- Linux 측 `~/.hx/bin/hexa` 인터프리터가 동작하며 `/Users/ghost/...` (mac_home mount) 경로의
  lens 를 직접 실행 가능 — **single-lens 호출 평균 19 ms** (alignment_measure 측정).
- 1013-lens full-sweep 단순 시간 estimate: **1013 × 19 ms ≈ 19 초** (sequential) — 본
  audit 의 *가장 중요한 발견*. K=10 smoke 는 < 1 초 가능.
- 따라서 **P-A (수정된 정의)** = "nexus hexa lens registry on mac_home mount, Linux hexa runner"
  로 재정의하면 **이미 가용**. GPU/RunPod 불필요. Mistral-7B forward (`anima_phi_star`)
  는 본 spec 의 1013-lens 측정과 무관 — 두 항을 conflate 한 것이 spec.md 의 P-A 정의 오류.

## 1. anima Φ★ engine — 현재 capability snapshot

### 1.1 위치 + 본질

| 항목 | 값 |
|------|-----|
| Tool path | `/home/summer/mac_home/core/anima/tool/anima_phi_star.hexa` (189 lines) |
| Paradigm | v11 measurement-axis P-D (IIT φ-star approximation) |
| Method | 16 prompts × forward(Mistral-7B) → byte-weighted hidden state → covariance log-det → K random bipartition cut → min-info-partition |
| Output schema | `anima/phi_star/1` (`phi_star_min, phi_mean, phi_max, gate_positive/substantial`) |
| Substrate | single backbone LLM (default: mistralai/Mistral-7B-v0.3) |
| Cost | ~50 s per measurement (load 30 s + 16 forwards + K=8 partitions) on GPU |
| **Scope** | **single-model integrated-information score** — NOT lens-based discovery |

### 1.2 측정 단위와 1013-lens 와의 *축* 불일치

`anima_phi_star.hexa` 의 출력은 *모델 hidden state* 의 covariance partition 기반 단일 scalar
`Φ*` 이다. spec.md §2 의 `phi_lens(L_i, x)` 는 *lens function* `L_i` 가 도메인 데이터 `x` 에
대해 emit 하는 closed-form pattern score 이다. 두 항은 **서로 다른 measurement axis**:

| 축 | anima_phi_star | spec.md phi_lens |
|----|----------------|------------------|
| input | 16 fixed prompts | domain data x ∈ D |
| computation | LLM forward + cov-MIP | lens deterministic eval (n=6 primitive check) |
| output | scalar Φ* per model | scalar score per (lens, data) pair |
| substrate | GPU-bound (Mistral-7B) | CPU-only hexa eval (~19 ms/lens) |
| reproducibility | bf16 nondeterminism risk | deterministic (seeded const-only math) |

**결론**: spec.md §1 P-A 의 "anima cosmic-scale measurement engine (Φ★ engine …)" 표현은
*같은 이름의 다른 도구* 두 개를 융합한 것 — anima 측 `anima_phi_star.hexa` 와 nexus 측 1013-
lens telescope orchestrator 가 별개의 axis. **본 audit 의 권고는 spec §1 P-A 정의를 *nexus
1013-lens engine accessible from anima* 로 재기술하는 것** (실측은 본 audit 권고 단계에서
*제안만*; 메인 process 가 결정).

## 2. nexus 1013-lens engine — 실제 위치 + capability

### 2.1 Repository layout

```
/Users/ghost/core/nexus/                         (Mac side, accessible via mount)
├── lenses/                  ── 1,588 .hexa lens files (deterministic, ~19 ms each)
│   ├── accel_*.hexa         ─ 234 files (accel ML/physics/eng/humanities)
│   ├── anima_*.hexa         ─ 88 files (consciousness/binding/qualia)
│   ├── quantum_*.hexa       ─ 290 files
│   ├── frontier_*.hexa      ─ 227 files
│   ├── tecs_*.hexa          ─ 103 files (TECS-L math)
│   ├── sedi_*.hexa          ─ 101 files (signal detection)
│   ├── cross_*.hexa         ─ 77 files (cross-domain)
│   ├── n6_*.hexa            ─ 58 files (n6 industry)
│   ├── physics_*.hexa       ─ 49 files
│   ├── core_*.hexa          ─ 23 files (Core 22 + 1 - 기존 telescope-rs 축)
│   └── (...remaining singletons)
├── engine/
│   ├── engine_nexus.hexa    ─ Ouroboros 자기관리 entry (654 lines)
│   ├── engine_anima.hexa    ─ anima bridge (1,424 lines)
│   └── engine_registry.jsonl
└── cli/
    ├── run.hexa             ─ "hx run nexus <sub>" thin wrapper
    └── blowup/lens/
        ├── telescope.hexa   ─ Lens trait + weighted_consensus (742 lines)
        ├── lens_forge.hexa  ─ gap→generate→validate→register (735 lines)
        └── lenses_core.hexa ─ core 22 (2,366 lines)
```

### 2.2 Lens count reality check (Hc_960 mislabel risk 검토)

spec.md §0 (DD166) 의 "1013" lens 카테고리 표는 *registry-design* count 이다. 실제 디렉터리
스캔 결과:

| 출처 | 합계 |
|------|-----:|
| spec.md (DD166 카테고리 합) | 1,013 |
| `/Users/ghost/core/nexus/lenses/*.hexa` 실측 | **1,588** |
| 차이 | +575 |

차이 575 는 (1) lens_forge auto-discovery 누적분, (2) singleton 도메인 파일 (yoga, yang,
wormhole, … 각 1 개씩 약 200+ 종), (3) accel/quantum/frontier 확장으로 추정. **Hc_960 의
mislabel-by-mixed-count caveat 가 그대로 실현된 상태** — "1013" 은 *공식 라벨* 이지만 disk
상 lens 수는 1,588 이다. C3 (no-mislabel-drift) 검증 시 *어떤 1013 을 선정* 할지 lens-id
whitelist 가 spec.md 외부에 SSOT 로 존재해야 한다 (`config/acceleration_hypotheses.json`
_meta.nexus_upgrade 또는 nexus-repo 의 `lens_registry.json` 필요).

### 2.3 Single-lens 측정 cost (Linux 측 실측)

```
$ time /home/summer/.hx/bin/hexa run /Users/ghost/core/nexus/lenses/accel_alignment_measure.hexa
lens[alignment_measure] category=extended axis="…" score=1 (8/8)
real    0m0.019s
user    0m0.003s
sys     0m0.000s
```

- single-lens cold-start cost: **~19 ms** (interpreter init included)
- 1013-lens sequential estimate: **1013 × 19 ms ≈ 19 초** (one-shot, no parallelism)
- 1588-lens (실측 디렉터리 전체) estimate: **~30 초**
- K=10 smoke: **< 1 초** (10 × 19 ms ≈ 0.2 s + overhead)

### 2.4 Output schema gap

lens 의 stdout 은 free-form string (`lens[name] category=… axis="…" score=N (h/t)`). spec.md
§2 의 5 가지 metric (phi_lens, support_mask, consistency_with_n6, cross_lens_agreement,
bonferroni_adjusted_p) 중 *현재 구현된 것*:

| metric | 구현 상태 |
|--------|-----------|
| `phi_lens` (score) | ✅ 모든 lens 가 stdout 으로 score 출력 |
| `support_mask` | ⚠ predicate_holds gate 명시 없음 — score>0 으로 proxy 가능 |
| `consistency_with_n6` | ✅ 모든 lens 가 "σ·φ = n·τ = J₂" identity 검증 (Hc_378) |
| `cross_lens_agreement` | ❌ telescope.hexa 의 `weighted_consensus` 존재하나 K-NN 부호 일치율은 별 aggregator 필요 |
| `bonferroni_adjusted_p` | ❌ p-value 계산 자체가 lens 출력에 없음 — post-processing 필요 |

→ Φ_lens 와 n6-consistency 는 *zero implementation cost*. cross-lens-agreement 는 lens 출력
parser + score-sign 집계 ~50 LOC. Bonferroni 는 N_tests 정의가 필요 (각 lens 가 단일 test 면
α/1013 ≈ 4.93e-5; 다중 test 면 별도 정의).

## 3. P-A vs P-B 비교 (Path matrix)

spec.md §1 의 원 정의를 **재해석** 한 path:

| | **P-A (재정의)** nexus hexa lens registry direct | **P-B** Python proxy harness (≥ 50 lens) |
|--|--|--|
| Engine | `/Users/ghost/core/nexus/lenses/*.hexa` + Linux `~/.hx/bin/hexa` | new Python module `nexus.lenses` |
| Lens count available | 1,588 (1013 whitelist 적용) | 50+ subset (manual reimplementation) |
| Implementation cost | aggregator only (~150 LOC: hexa subprocess loop + score parser + n6-flag + cross-agree + Bonferroni) | full Python lens reimpl 50 × ~30 LOC ≈ 1,500 LOC + aggregator 150 LOC |
| Time-to-K10-smoke | < 1 시간 (aggregator 작성) | 1–2 일 (lens reimpl) |
| Determinism | ✅ hexa lens 는 const-only (no RNG, no LLM) | ⚠ seed 보장 필요 |
| Cross-host | ⚠ mac_home mount 의존 (Linux 에서 `/Users/ghost/...` 접근 필요) | ✅ Linux native |
| Entropy backing (Hc_944/945) | not required for deterministic lenses | optional (proxy seed) |
| Risk | Mac mount 불가 시 fallback 없음 | 50 lens 가 1013 분포의 sub-sample → bootstrap CI 필요 |

### 3.1 Mac mount + cross-host (memory: feedback_cross_host_paths.md)

- `/Users/ghost/core/nexus/lenses/accel_alignment_measure.hexa` Linux 에서 stat 확인 ✅
- Linux `~/.hx/bin/hexa` 가 Mac 측 `.hexa` 파일을 직접 실행 가능 ✅ (실측 19 ms)
- python3 wrap routing (reference_aiden_python3_routing.md) 영향 없음 — 본 audit 의 path
  는 hexa subprocess 이므로 python3 hop 우회

**잠재 risk**: mac_home mount 가 unmount 되면 P-A 즉시 불가 → P-B fallback 필요. 단,
스냅샷-via-rsync 으로 lens 디렉터리를 Linux 측 (`/home/summer/core/nexus_lenses_snapshot/`)
로 복제하면 mount-independence 확보 가능 (디스크 ~수 MB 추정).

## 4. 권고 — K=10 smoke 가장 빠른 path

| 항목 | 값 |
|------|-----|
| **추천 path** | **P-A 재정의** (nexus hexa lens registry + Linux hexa runner) |
| **이유** | (1) zero new lens code, (2) < 1초 smoke, (3) deterministic |
| K=10 lens 선정 | Core 22 중 spec.md §3 의 "top-10" — 별도 SSOT 필요 (현재 미정) |
| 새 도구 작성 | `tool/anima_nexus_1013lens_smoke.hexa` (≈ 150 LOC) — subprocess loop + score parse + n6-consistency aggregate + Bonferroni stub |
| Estimate time | aggregator 작성 ~30 분 + smoke run < 1 초 |
| Estimate cost | **$0** (CPU only, GPU/RunPod 불필요) |
| Output | `state/nexus6_1013lens_activation_2026_05_11/k10_smoke_results.json` |
| Acceptance (spec §3) | `Φ_lens > 0 비율 ≥ 6/10` + `mean(phi_lens) > 0` + `cross_lens_agreement_K ≥ 0.55` |

### 4.1 K=10 lens whitelist proposal (메인 process 가 결정)

spec.md §3 는 "Core 22 중 최우선 10 lens" 만 명시. 실제 nexus repo 의 `core_*` 패턴은 23 개
파일. 후보 (alphabetical, 임의 — 메인 process 확정 필요):

```
core_consciousness.hexa, core_topology.hexa, core_causal.hexa,
core_gravity.hexa, core_thermo.hexa, core_information.hexa,
core_phase_transition.hexa, core_symmetry.hexa, core_dimensional.hexa,
core_recursive.hexa
```

→ 실제 파일 이름은 `ls /Users/ghost/core/nexus/lenses/ | grep "^core_"` 로 검증.

## 5. Blocker / Risk

| Risk | 영향 | mitigation |
|------|------|------------|
| spec.md P-A 정의 모호 | 본 audit 가 *재정의* 함 — 메인 process 가 spec.md 갱신 결정 | spec.md §1 P-A 명확화 (anima_phi_star ≠ nexus lens engine) |
| mac_home mount 의존 | mount fail → P-A 불가 | nexus lens snapshot to Linux-native path |
| Hc_960 mislabel (1013 vs 1588) | C3 binding 시 whitelist 분쟁 | `lens_registry.json` SSOT 확정 (nexus repo 측에 존재 여부 확인 필요) |
| `cross_lens_agreement` 미구현 | C1 smoke acceptance gate 무효 | aggregator 작성 (~50 LOC, 본 audit §2.4) |
| K=10 lens 선정 임의성 | L4 selection bias 잔존 | random-10 baseline 동시 측정 권고 |
| spec.md §2 의 `phi_lens` 정의가 anima 측 Φ* IIT 와 다름 | 결과 해석 시 cross-substrate 비교 의미 모호 | 두 axis 별로 보고 + 동일 이름 분리 ("nexus_lens_score" vs "anima_phi_star") |

## 6. H_135 status update 제안 (메인 process 결정 사항 — 본 audit 는 *제안만*)

현재 H_135 frontmatter: `status: legacy-archive-pointer`, `verdict_class:
1013-lens-activation-pending-C1`.

**제안 (적용 보류)**:

- `prereq_audit_completed: state/nexus6_1013lens_activation_2026_05_11/prereq_audit_2026_05_11.md`
  필드 추가 (frontmatter)
- `status` 는 *유지* (legacy-archive-pointer) — K=10 smoke 실측 PASS 전까지 변경 금지
- spec.md §1 P-A 정의를 본 audit §2 의 발견에 맞게 *clarify* (anima_phi_star.hexa 와 nexus
  lens engine 의 axis 차이 명시) — 별 commit 으로 메인 process 가 처리

## 7. Lock Policy 준수

본 audit 작성 과정에서 어떤 파일에도 `chflags +uchg/+schg`, `chattr +i`, OS-level immutable
flag 를 적용하지 않았다. unlock 된 파일 재잠금 시도 없음 (memory: feedback_no_relock.md).

## 8. Non-Goals (본 audit 범위 밖)

- K=10 smoke 실측 run — 별 cycle
- spec.md §3 의 K=10 / K=25 / K=50 cascade 실제 실행
- `lens_registry.json` whitelist SSOT 결정 — nexus repo 쪽 정합 필요
- anima_phi_star.hexa 의 Mistral-7B forward 비용 견적 (본 audit 와 무관 — 별 도구)
- nexus 1013-lens 의 statistical validity 검증 — 본 audit 는 *engine feasibility only*

## 9. Cross-Reference

- spec source: `state/nexus6_1013lens_activation_2026_05_11/spec.md`
- H_135: `hypotheses/H_135_dd166_nexus_1013_lens.md`
- DD166: `docs/hypotheses/dd/DD166-nexus-1013lens-discovery-engine.md`
- anima Φ★ tool: `tool/anima_phi_star.hexa`
- nexus repo (Mac mount): `/Users/ghost/core/nexus/`
- nexus lens dir: `/Users/ghost/core/nexus/lenses/` (1,588 files)
- nexus telescope: `/Users/ghost/core/nexus/cli/blowup/lens/telescope.hexa`
- Hc cluster: Hc_586, Hc_598, Hc_035, Hc_378, Hc_944, Hc_945, Hc_960
- Memory notes: feedback_cross_host_paths.md, reference_aiden_python3_routing.md,
  feedback_no_relock.md
