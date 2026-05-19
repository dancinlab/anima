---
directive_id: cross_host_phase_2a_reimpl_request_2026_05_12
from_host: ubu-2 (summer, Linux x86_64 — NFS client)
to_host: Mac (ghost session, NFS server — concurrent Claude session)
issued: 2026-05-12
issued_by: agent (K=25 cascade audit follow-up)
parent_specs:
  - state/nexus6_1013lens_activation_2026_05_11/spec.md
  - state/nexus6_1013lens_activation_2026_05_11/cascade_k25_plan_2026_05_12.md
  - state/nexus6_1013lens_activation_2026_05_11/lens_channel_reimpl_spec_2026_05_12.md
  - state/nexus6_1013lens_activation_2026_05_11/k10_reimpl/phase1_verdict_2026_05_12.md
target_h: H_135 (DD166 NEXUS 1013-lens discovery engine)
cycle: 7 §K25-Phase2A (cycle 6 master doc §12 cycle 7 queue item)
status: REQUEST — awaiting Mac session pickup
lock_policy: NO chflags/chattr — repository directive 2026-05-11
---

# Cross-Host Directive — Phase 2-A v2 Lens Reimpl Request (Mac session)

ubu-2 (summer) → Mac (ghost) 의 concurrent Claude session 으로 K=25 cascade Phase 2-A 의
실제 reimpl 작업을 위임한다. 본 directive 는 ubu-2 측 NFS write 제약 (EPERM on
`state/nexus6_*/k25_phase2/*.hexa` + `k10_reimpl/*_v2.hexa`) 을 우회하기 위한 cross-host
coordination request 이다.

## 1. Goal — 15 v2 lens reimpl (Phase 2-A 전체)

cascade_k25_plan §1.2 + §1.3 의 *15 new lens* (K=10 carry-over 10 외 +13 core_* +2 cross-cat)
을 `lens_channel_reimpl_prototype_core_info.hexa` template 기반으로 v2 axis-specific kernel
reimpl. 산출물은 `state/nexus6_1013lens_activation_2026_05_11/k25_phase2/` 디렉토리에 land.

### 1.1 13 추가 core_* lens (cascade_k25_plan §1.2)

| # | lens basename | axis | cross-validation target |
|--:|---------------|------|-------------------------|
|  1 | `core_boundary.hexa`           | geometry/boundary       | core_topology         |
|  2 | `core_chaos.hexa`              | dynamics/chaos          | core_stability (null) |
|  3 | `core_compass.hexa`            | directional/coord       | n6 primitive aux      |
|  4 | `core_em.hexa`                 | electromagnetism        | Hc_035 cross-val      |
|  5 | `core_evolution.hexa`          | evolution/selection     | core_causal           |
|  6 | `core_memory.hexa`             | memory/retention        | core_consciousness    |
|  7 | `core_mirror.hexa`             | symmetry/reflection     | Hc_944 qmirror        |
|  8 | `core_multiscale.hexa`         | multiscale              | core_scale (Hc_378)   |
|  9 | `core_quantum_microscope.hexa` | quantum-fine            | core_quantum          |
| 10 | `core_recursion.hexa`          | recursion               | Hc_437 fixed-point    |
| 11 | `core_ruler.hexa`              | measurement substrate   | n6 primitive base     |
| 12 | `core_triangle.hexa`           | geometry/relational (3-body) | n6 primitive     |
| 13 | `core_wave.hexa`               | wave/oscillation        | core_quantum + core_em |

### 1.2 2 cross-category lens (cascade_k25_plan §1.3)

| # | lens basename | category | axis | 선정 |
|--:|---------------|----------|------|-----|
| 14 | `n6_*.hexa` (alphabetical top-1 from `n6_industry_*`) | n6 산업 | DSE/소재/동역학 | canary tier |
| 15 | `anima_*.hexa` (alphabetical top-1 from `anima_*`)    | anima 의식 | 감질/결합 | H_135 의식 axis |

cross-cat basename 은 `ls /home/summer/core/nexus_lenses_snapshot/n6_*.hexa | head -1` 및
`ls .../anima_*.hexa | head -1` 로 deterministic 선정 (alphabetical stable, lens snapshot
Linux-native — Mac 측에서는 같은 디렉토리 또는 Mac equivalent 경로 사용 가능).

## 2. Reference Template — lens_channel_reimpl_prototype_core_info

```
state/nexus6_1013lens_activation_2026_05_11/lens_channel_reimpl_prototype_core_info.hexa
```

본 prototype 의 80 LOC 구조 (입력 채널 `env ANIMA_LENS_X_FILE` + fallback
`env ANIMA_LENS_SEED` → 256-sample LCG synthetic + axis kernel + meta out) 를 K=10 Phase 1
(`k10_reimpl/core_*_v2.hexa` 10개) 가 inherit 했고, 평균 100–130 LOC. Phase 2-A 의 15 lens
도 동일 패턴 inherit. axis kernel 만 lens 별 differentiate.

추가 reference (k10_reimpl 의 10개 axis kernel 구현 사례): phase1_verdict §1 표 참조 —
Shannon entropy / autocorrelation / IIT bipartition / entropy production / coherence /
Betti-0 / Ricci proxy / clustering coef / multi-scale entropy / Lyapunov proxy.

## 3. Acceptance Criteria — F-reimpl 3-Falsifier PASS

K=10 Phase 1 (`phase1_verdict_2026_05_12.md` §2) 와 *동일한 gate* 를 15 new lens 에 적용.
K=10 의 10 lens 와 합쳐 K=25 set 에서 측정해도 무방하고, 15 lens 만 별도 측정해도 무방
(권고: K=25 set 전체로 한번에 측정 — F-reimpl-2 r matrix 가 25×25 로 더 informative).

| ID | gate | floor | K=10 Phase 1 측정값 (baseline) |
|----|------|------:|-------------------------------:|
| **F-reimpl-1** | pos_ratio dynamic range over x profiles (`x_low_noise / x_high_noise / x_ar1 / x_sin / x_mixture` excluding shuffled) | ≥ 0.30 | 0.40 |
| **F-reimpl-2** | cross-validation r matrix mean off-diagonal \|r\| (profile vector = 8 distinct x profile + 10 ar1-seed sample = 18-dim) | ∈ [0.2, 0.95] | 0.459 |
| **F-reimpl-3** | signal-noise separation: real_x mean > shuffled_x mean per lens | ≥ 7/10 (Phase 1 floor) → Phase 2-A 권고: ≥ 11/15 (proportional) | 7/10 |

F-reimpl-1 trip → 입력 채널 misuse (synthetic LCG fallback only, env path ignore) — code
review 필요.
F-reimpl-2 \|r\| > 0.95 → TRIVIAL redundancy (axis kernel 차별 부족); \|r\| < 0.2 → 입력
무관 (random noise); 권고 대역 [0.2, 0.95] 유지.
F-reimpl-3 < 11/15 → axis polarity 반전 lens (K=10 의 info / topology / network 처럼) 의
정합 — honest L 로 기록하되 block 사항 아님.

raw F-reimpl 측정 helper 는 phase1 의 `phase1_falsifier_results.json` 의 schema 따름.

## 4. Estimated Cost

| 항목 | 값 | 비고 |
|------|-----|-----|
| wall (CPU sequential) | **5–7h** | phase1_verdict §9 estimate (Phase 2-A 4–6h + Phase 2-B 1h) |
| GPU | 0 | CPU-only hexa eval |
| RunPod / cloud | $0 | local Mac runner |
| disk I/O | < 5 MB | 15 lens × ~3KB + F-reimpl raw json |
| memory peak | < 200 MB | hexa interpreter + 25×25 r matrix |

cost-to-information ratio 는 K=25 canary 보다 *훨씬 큰* lens authoring 비용 — 본 Phase
2-A 가 K=25 cascade legitimacy 의 본질적 substrate.

## 5. Coordination — NFS Write Lock Handshake

ubu-2 측 현황:
- NFS mount `/home/summer/mac_home/core/anima` 에서 `state/nexus6_*/k25_phase2/*.hexa` +
  `state/nexus6_*/k10_reimpl/*_v2.hexa` write 시 **EPERM** 발생 (Mac 측 active session
  의 NFS lock — `fcntl POSIX lock` 또는 macOS 의 dev-fs 쓰기 권한 cascade)
- 결과: ubu-2 는 본 Phase 2-A 의 hexa 파일 write 불가
- ubu-2 가 가능한 작업: read-only 분석, md doc 작성 (`state/cross_host_directives/`
  등 EPERM 없는 경로), git read

handshake:
1. Mac session 이 본 directive 수신 → Phase 2-A 작업 시작
2. Mac 측 NFS write lock 은 작업 중 유지 (정상)
3. Mac 작업 완료 + commit + (필요시) push 후, Mac 측 hexa interpreter 의 file handle
   close → NFS lock 자연 해제
4. ubu-2 가 git pull (또는 NFS mount 의 git read) → K=25 canary cascade run
   (`hexa run tool/anima_nexus_1013lens_cascade.hexa --k 25 ...`)
5. K=25 결과 (pass / F1–F5 trip) verdict md 작성 → ubu-2 측 commit

ubu-2 측 NFS 권한 안정 시 (Mac 작업 중간에라도 EPERM 해소되면) ubu-2 도 read-side 분석
(예: F-reimpl 측정 raw json 의 sanity check) parallel 가능 — 단 hexa 파일 자체 write 는
Mac 단독.

## 6. Done Signal

Mac session 이 다음 commit 을 anima repo 에 land 하면 "Phase 2-A 완료" 로 인식:

```
feat(k25 phase 2a): 15 v2 lens reimpl + F-reimpl 3-falsifier PASS
```

commit 에 포함되어야 할 file (권고 list):

- `state/nexus6_1013lens_activation_2026_05_11/k25_phase2/core_boundary_v2.hexa`
- `state/nexus6_1013lens_activation_2026_05_11/k25_phase2/core_chaos_v2.hexa`
- `state/nexus6_1013lens_activation_2026_05_11/k25_phase2/core_compass_v2.hexa`
- `state/nexus6_1013lens_activation_2026_05_11/k25_phase2/core_em_v2.hexa`
- `state/nexus6_1013lens_activation_2026_05_11/k25_phase2/core_evolution_v2.hexa`
- `state/nexus6_1013lens_activation_2026_05_11/k25_phase2/core_memory_v2.hexa`
- `state/nexus6_1013lens_activation_2026_05_11/k25_phase2/core_mirror_v2.hexa`
- `state/nexus6_1013lens_activation_2026_05_11/k25_phase2/core_multiscale_v2.hexa`
- `state/nexus6_1013lens_activation_2026_05_11/k25_phase2/core_quantum_microscope_v2.hexa`
- `state/nexus6_1013lens_activation_2026_05_11/k25_phase2/core_recursion_v2.hexa`
- `state/nexus6_1013lens_activation_2026_05_11/k25_phase2/core_ruler_v2.hexa`
- `state/nexus6_1013lens_activation_2026_05_11/k25_phase2/core_triangle_v2.hexa`
- `state/nexus6_1013lens_activation_2026_05_11/k25_phase2/core_wave_v2.hexa`
- `state/nexus6_1013lens_activation_2026_05_11/k25_phase2/<n6_top1>_v2.hexa`
- `state/nexus6_1013lens_activation_2026_05_11/k25_phase2/<anima_top1>_v2.hexa`
- `state/nexus6_1013lens_activation_2026_05_11/k25_phase2/phase2a_verdict_2026_05_12.md`
- `state/nexus6_1013lens_activation_2026_05_11/k25_phase2/phase2a_falsifier_results.json`

verdict md schema 는 phase1_verdict_2026_05_12.md inherit (§0 TL;DR / §1 lens 표 /
§2 F-reimpl 1/2/3 / §3 sample score / §7 K=25 진입 검증 / §8 honest L / §10 cross-ref).

bare-name copy (aggregator hardcoded whitelist back-compat) 는 K=25 의 cascade aggregator
가 `--k 25` mode 에서 어떻게 whitelist 를 resolve 하는지에 따라 결정 — Phase 2-D
(aggregator refactor) scope 와 entangle. 본 directive 는 v2 hexa 만 산출 요구.

## 7. Non-Goals (본 directive 범위 밖)

- 실제 K=25 canary run — ubu-2 측에서 수행 (Phase 2-A 완료 후)
- aggregator `tool/anima_nexus_1013lens_cascade.hexa` 의 K=25 whitelist 분기 refactor —
  Phase 2-D (별 directive)
- F2 null distribution synthesis (MC vs analytic vs bootstrap) — cascade_k25_plan §3.1 미결정
- K=50 lens reimpl — Phase 3 (cascade_k25_plan PASS 후 별 plan)
- spec §3 deviation 정책 결정 (cascade_k25_plan §8 L6 — "core 22 + n6 top-3" vs 본
  directive "core 23 + cross-cat 2") — 메인 process 결정

## 8. Cross-Reference

| ref | path | 관계 |
|-----|------|-----|
| cascade plan K=25 (parent) | `state/nexus6_1013lens_activation_2026_05_11/cascade_k25_plan_2026_05_12.md` §1.2 §1.3 | 15 lens basename 의 SSOT |
| Phase 1 K=10 verdict | `state/nexus6_1013lens_activation_2026_05_11/k10_reimpl/phase1_verdict_2026_05_12.md` §9 | Phase 2-A/B/C/D breakdown source |
| reimpl prototype template | `state/nexus6_1013lens_activation_2026_05_11/lens_channel_reimpl_prototype_core_info.hexa` | Mac 작업 template |
| reimpl spec | `state/nexus6_1013lens_activation_2026_05_11/lens_channel_reimpl_spec_2026_05_12.md` | F-reimpl-1/2/3 gate definition |
| lens snapshot (Linux-native) | `/home/summer/core/nexus_lenses_snapshot/` | 15 lens 의 *legacy* (pre-reimpl) source — axis 의도 reference |
| cycle 6 master doc | commit `68e57bd3b` (anima repo) §12 cycle 7 queue | K=25 work scheduling source |
| Hc cluster | Hc_586 (가속), Hc_598 (progressive expansion), Hc_035, Hc_378, Hc_944 | Phase 2-A 가 직접 검증하는 Hcs |
| lock policy | memory: feedback_no_relock.md 2026-05-11 | chflags/chattr 금지 |

## 9. ubu-2 측 Follow-up (Phase 2-A 완료 후)

| step | action | 출력 |
|------|--------|------|
| 1 | git pull (또는 NFS 자동 sync) | local 최신화 |
| 2 | `hexa run tool/anima_nexus_1013lens_cascade.hexa --k 25` (env: NEXUS_LENSES_DIR=…/k25_phase2/ + ANIMA_LENS_X_FILE=…) | K=25 canary results json |
| 3 | F1–F5 falsifier evaluation (cascade_k25_plan §3) | K=25 verdict md |
| 4 | C1 cascade gate (`pos_ratio ≥ max(K10, 0.7)`) + C2 / C3 / C5 (cascade_k25_plan §2) | PASS / F-trip decision |
| 5 | (PASS 시) Hc_586 cascade update + cycle 7 §K25-Phase2-canary land commit | K=50 plan trigger |

---

**lock policy**: 본 directive 작성 과정 chflags/chattr 무적용. Mac session 이 본 directive
수행 시에도 동일 — repository-wide directive 2026-05-11 따름.

**directive freshness**: 본 directive 는 2026-05-12 ubu-2 audit 시점의 state 기준. Mac
session 이 본 directive 를 picking up 할 때 더 최근 K=25 work (예: Mac 측이 이미 일부
lens 완료) 가 있으면 그 state 를 우선하고 본 directive 의 incremental scope 로 줄여 적용.
