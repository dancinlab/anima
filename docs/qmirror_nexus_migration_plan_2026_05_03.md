---
title: qmirror — nexus → standalone migration plan (4-step deprecation)
date: 2026-05-03
mode: doc-only deliverable (no impl, no execution)
authors: anima cycle agent
substrate refs:
  - /Users/ghost/core/nexus/modules/qmirror/ (11 .hexa, current in-tree)
  - /Users/ghost/core/qmirror/ (standalone repo, sister BG a95ca30a7c WIP)
  - /Users/ghost/core/anima/docs/hx_install_qmirror_spec_2026_05_03.md (companion)
gate: raw#9 STRICT, raw#10 (≥5 honest C3 caveats), raw#15
constraint: DO NOT delete nexus/modules/qmirror/ — deprecation only, archival = future cycle
---

# 0. TL;DR

`nexus/modules/qmirror/` (11 .hexa, in-tree) → `hx install qmirror` standalone repo로 **4-step deprecation cycle**. archive(deletion)는 **step 4 = ~1 month grace 후**까지 deferred. step 1 = sister BG a95ca30a7c가 현재 진행 중. 본 문서는 step 2~4 명세 + cross-link.

**핵심 원칙**:
- `do not delete` — git history 보존, working tree에서 제거는 step 4에서만
- `dual SSOT 회피` — step 2~3는 in-tree에 DEPRECATED.md만 추가, in-tree code는 변경 없음
- `consumer-driven cutover` — nexus 내부 모듈이 standalone로 import 전환 완료 후에만 archival

---

# 1. 현재 상태

## 1-1. nexus/modules/qmirror/ 인벤토리

```
/Users/ghost/core/nexus/modules/qmirror/
├── _python_bridge/        # python helper (qiskit-aer runner)
├── chsh.hexa              # CHSH inequality (S vs Tsirelson)
├── circuit.hexa           # circuit DSL
├── engine_aer.hexa        # Aer simulator wrapper
├── entropy.hexa           # entropy injection
├── iit_mip.hexa           # IIT MIP φ★
├── phi.hexa               # φ★ structured
├── qrng.hexa              # quantum random bytes
├── sampler.hexa           # circuit → counts
├── selftest.hexa          # full + --quick
└── tomography.hexa        # ρ matrix
```

**총 11 파일** + python_bridge subdir. 모두 `import "modules/qmirror/<name>.hexa"` 패턴으로 nexus 내부 4~6 consumer가 사용.

## 1-2. /Users/ghost/core/qmirror/ standalone (sister BG WIP)

```
/Users/ghost/core/qmirror/
├── cli/        (empty, sister 채움 예정)
├── docs/       (empty)
├── examples/   (empty)
├── modules/    11 .hexa (이미 sister가 카피 완료)
├── state/qmirror_standalone_repo_2026_05_03/
└── tests/      (empty)
```

**modules/ 이미 100% mirror 완료**. nexus → standalone 동기화는 sister BG가 처리.

## 1-3. nexus consumer dependency 그래프 (추정)

```
nexus/modules/qmirror/* ← {
  nexus/cli/run.hexa          (qmirror chsh subcommand)
  nexus/modules/qrng/*         (qmirror.qrng → quantum entropy)
  nexus/modules/sim/*          (qmirror.engine_aer → SV1 swap)
  nexus/lenses/*               (qmirror.iit_mip → cross-substrate witness)
}
```

(정확한 cite list는 step 3 시작 시 `grep -rn 'modules/qmirror'` 으로 enumerate)

---

# 2. 4-step deprecation cycle 개요

| Step | Cycle | Action | Files Changed | Risk |
|---|---|---|---|---|
| 1 | **THIS** (2026-05-03) | standalone repo creation | qmirror/ 11 modules + cli/ + install.hexa | LOW (sister BG, doc-only this BG) |
| 2 | next cycle | DEPRECATED.md marker in nexus/modules/qmirror/ | 1 new file | LOW (additive only) |
| 3 | cycle+2 | nexus consumer refactor → import standalone qmirror | ~6 nexus files (consumer rewrites) | MEDIUM (test re-run 필요) |
| 4 | cycle+3 (1 month grace) | archive nexus/modules/qmirror/ from working tree (git mv → archive/) | 11 .hexa moved | LOW (history 보존, working tree만 정리) |

---

# 3. Step-by-step 명세

## 3-1. Step 1 — standalone repo creation (THIS CYCLE, sister BG)

**Owner**: sister a95ca30a7c (parallel BG, anima cycle 2026-05-03)
**Status**: IN PROGRESS (modules/ 100%, cli/ docs/ examples/ tests/ pending)

**Deliverable**:
- `/Users/ghost/core/qmirror/manifest.toml` (per spec doc §2)
- `/Users/ghost/core/qmirror/install.hexa` (per spec doc §3.2)
- `/Users/ghost/core/qmirror/cli/qmirror.hexa` (per spec doc §3.3)
- `/Users/ghost/core/qmirror/README.md`
- `/Users/ghost/core/qmirror/LICENSE` (Apache-2.0)
- `/Users/ghost/core/qmirror/tests/selftest_quick.hexa`
- git init + initial commit

**Out of scope** (this step):
- registry.tsv 1줄 추가 (next cycle)
- GitHub push (next cycle)
- nexus consumer touch (zero, by design)

**Falsifier**:
- `ls /Users/ghost/core/qmirror/manifest.toml install.hexa cli/qmirror.hexa` → 3 files exist
- `hexa /Users/ghost/core/qmirror/cli/qmirror.hexa --help` → usage 출력
- `wc -l /Users/ghost/core/qmirror/modules/*.hexa` ≈ matches `wc -l /Users/ghost/core/nexus/modules/qmirror/*.hexa`

## 3-2. Step 2 — DEPRECATED.md marker (NEXT CYCLE)

**Owner**: future cycle agent
**Trigger**: step 1 verified PASS (sister BG marker landed)

**Deliverable** (single file):

`/Users/ghost/core/nexus/modules/qmirror/DEPRECATED.md`

```markdown
# nexus/modules/qmirror/ — DEPRECATED

**Status**: DEPRECATED as of 2026-05-XX (next cycle date)
**Replacement**: standalone qmirror package — `hx install qmirror`
**Standalone repo**: https://github.com/dancinlab/qmirror (or local /Users/ghost/core/qmirror)
**Migration plan**: /Users/ghost/core/anima/docs/qmirror_nexus_migration_plan_2026_05_03.md

## Why deprecated

- qmirror substrate became canonical (cond.7 cross-tech 3/4 PASS, 2026-05-03)
- standalone packaging enables `hx install qmirror` for any hexa-lang user
- nexus repo size + dependency clarity benefit from extraction

## When will this directory be removed?

After ~1 month grace period (step 4 of migration plan), 모든 nexus consumer가
standalone qmirror로 import 전환 완료된 후. 본 directory는 git history에 영구 보존되며,
working tree에서만 제거됨.

## How to use standalone qmirror

\```bash
hx install qmirror
qmirror chsh --shots 10000
qmirror selftest --quick
\```

## Migration checklist for nexus consumers

- [ ] `import "modules/qmirror/chsh.hexa"` → `import "qmirror/modules/chsh.hexa"`
- [ ] `import "modules/qmirror/qrng.hexa"` → `import "qmirror/modules/qrng.hexa"`
- [ ] `import "modules/qmirror/iit_mip.hexa"` → `import "qmirror/modules/iit_mip.hexa"`
- [ ] re-run nexus tests
- [ ] update SSOT roadmap cite paths
```

**Constraint**: `nexus/modules/qmirror/*.hexa` 파일은 **건드리지 않음**. additive marker only.

**Falsifier**:
- `ls /Users/ghost/core/nexus/modules/qmirror/DEPRECATED.md` exists
- `git diff nexus/modules/qmirror/*.hexa` → empty (no logic change)

## 3-3. Step 3 — nexus consumer refactor (CYCLE+2)

**Owner**: future cycle agent (large step, may need 2 sub-cycles)
**Trigger**: step 2 marker landed + GitHub push of qmirror standalone PASS + `hx install qmirror` 검증

**Pre-step audit** (필수):

```bash
grep -rn '"modules/qmirror' /Users/ghost/core/nexus --include='*.hexa' \
  | grep -v 'modules/qmirror/' \
  > /tmp/qmirror_consumer_list.txt
wc -l /tmp/qmirror_consumer_list.txt   # estimate ~12-30 import lines
```

**Refactor pattern** (per consumer file):

```hexa
// BEFORE
import "modules/qmirror/chsh.hexa" as qmirror_chsh

// AFTER (standalone)
import "qmirror/modules/chsh.hexa" as qmirror_chsh
// (hx install qmirror creates ~/.hx/packages/qmirror/ which hexa import resolver finds)
```

**Per-consumer steps** (estimated ~6 files):

1. nexus/cli/run.hexa — qmirror subcommand block (5~10 import lines)
2. nexus/modules/qrng/*.hexa — qmirror.qrng cross-link
3. nexus/modules/sim/*.hexa — qmirror.engine_aer SV1-swap
4. nexus/lenses/*.hexa — qmirror.iit_mip witness
5. nexus/test/qmirror_*.hexa — test fixture path 업데이트
6. nexus/.roadmap.qmirror — cite paths (이번 cycle qmirror_canonical_migration에서 일부 처리됨)

**Test verification**:
- `bash /Users/ghost/core/nexus/scripts/run_all_tests.sh` (assumed exists)
- `qmirror selftest --quick` from standalone PASS
- `nexus run drill` (e2e) PASS

**Constraint**:
- step 3 완료까지 nexus/modules/qmirror/ in-tree 파일은 그대로 (rollback 가능성)
- 각 consumer 파일 수정마다 atomic commit (refactor 1 file per commit)

**Falsifier**:
- `grep -rn '"modules/qmirror' /Users/ghost/core/nexus --include='*.hexa' | grep -v 'modules/qmirror/'` → 0 lines
- nexus 모든 test PASS
- `qmirror selftest` standalone PASS

## 3-4. Step 4 — archive nexus/modules/qmirror/ (CYCLE+3, 1 month grace)

**Owner**: future cycle agent
**Trigger**: step 3 verified PASS + 30 days uneventful (no rollback needed)

**Action** (git mv, not rm):

```bash
cd /Users/ghost/core/nexus
mkdir -p archive/qmirror_2026_05_xx
git mv modules/qmirror archive/qmirror_2026_05_xx/
git commit -m "archive(qmirror): nexus/modules/qmirror/ → archive/ (standalone qmirror canonical)"
```

**Deliverable**:
- `/Users/ghost/core/nexus/archive/qmirror_2026_05_xx/` (11 .hexa moved)
- archive/qmirror_2026_05_xx/README.md — pointer to standalone + final commit hash
- `/Users/ghost/core/nexus/modules/qmirror/` — directory removed from working tree

**Git history**: 모든 commit, blame, history 영구 보존. `git log -- nexus/modules/qmirror/` 으로 추적 가능.

**Falsifier**:
- `ls /Users/ghost/core/nexus/modules/qmirror/` → no such directory
- `ls /Users/ghost/core/nexus/archive/qmirror_2026_05_xx/` → 11 .hexa
- `git log --oneline -- 'nexus/modules/qmirror/*'` → full history visible

**Rollback option** (if discovered consumer):
- `git mv archive/qmirror_2026_05_xx/qmirror modules/qmirror` (1-line revert)

---

# 4. Risk matrix

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| sister BG step 1 incomplete | LOW | HIGH | this BG verifies step 1 PASS before approving step 2 trigger |
| nexus consumer test fails after step 3 | MEDIUM | MEDIUM | atomic per-file commits, easy revert; 1 cycle for fix |
| `hx install qmirror` fails on user machine (PyPI / network) | MEDIUM | LOW | install.hexa --offline mode + PYPI_INDEX env var (future) |
| dual-SSOT divergence between in-tree and standalone (step 1~3) | MEDIUM | MEDIUM | step 1 sister BG mirrors modules/ exactly, no in-tree edits during step 2~3 |
| GitHub push delayed → external users blocked | LOW | LOW | local install (`/Users/ghost/core/qmirror`) works for dev, external = post-push |

---

# 5. Honest C3 caveats — 5개

## 5-1. nexus consumer enumeration is estimated, not measured

본 plan은 nexus 내부 qmirror import가 ~6 files라고 가정. 실측 grep 미실행 (step 3 시작 시 audit 단계에서 진행). **위험**: 30 files, 100 imports일 경우 step 3가 1 cycle로 안 끝남.

## 5-2. Step 4 archival has irreversibility cost

`git mv`는 history 보존하지만, future contributor가 `nexus/modules/qmirror/` 경로로 grep 시 hit 안됨. discoverability 손실. **mitigation**: archive/ 안 README + nexus repo root README의 "qmirror moved to standalone" 안내.

## 5-3. 1 month grace는 임의

step 3 → step 4 사이 30일은 임의 결정. 큰 issue 없을 시 단축 가능, complex regression 발견 시 연장. **mitigation**: step 3 완료 marker에 "earliest archival date = +30d" 명시, 실 archival은 trigger 검토 후.

## 5-4. dual-SSOT during step 1~3

step 1 (sister BG copies modules/)부터 step 3 (consumer refactor 완료) 사이 ~3 cycles 동안 nexus/modules/qmirror/ + /Users/ghost/core/qmirror/modules/ 동일 코드 존재. 한쪽만 수정 시 divergence. **mitigation**: step 2 DEPRECATED.md에 "FROZEN — modify standalone instead" 명시. CI check (future) 가능.

## 5-5. registry.tsv 추가는 별도 cycle 의존

본 plan은 registry.tsv 1줄 추가가 **이미 완료**되었다고 가정 (또는 step 2와 동시). 미완료 시 `hx install qmirror`이 외부 사용자에게 안 작동 → step 3 refactor가 무의미. **mitigation**: step 2 prerequisite에 "registry PR merged" 추가.

---

# 6. Cross-link

- companion spec: `/Users/ghost/core/anima/docs/hx_install_qmirror_spec_2026_05_03.md`
- sister BG a95ca30a7c (standalone repo creation): provides step 1 deliverable
- sister BG a70e17dd (nexus CLI integration): aligned with step 3 refactor
- canonical migration: `/Users/ghost/core/anima/docs/qmirror_canonical_migration_landed_2026_05_03.ai.md` (substrate canonical status, 7 roadmap files annotated)
- module versioning: `/Users/ghost/core/anima/docs/hexa_lang_module_versioning_landed_2026_05_03.ai.md` (semver precedent)

---

# 7. Marker

- `state/markers/qmirror_nexus_migration_plan_landed.marker` — this doc landing
- (future) `state/markers/qmirror_nexus_deprecation_step_2_landed.marker`
- (future) `state/markers/qmirror_nexus_deprecation_step_3_landed.marker`
- (future) `state/markers/qmirror_nexus_archival_landed.marker`
