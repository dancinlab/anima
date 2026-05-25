# hx install qmirror spec + nexus migration plan — LANDED (2026-05-03)

## TL;DR

`hx install qmirror`이 누구나 사용 가능하게 하기 위한 **2개 design doc landing**:
1. **package + install pipeline spec** (~570 LoC) — manifest.toml 14 fields, install.hexa 80 LoC outline, registry.tsv 1줄 추가, cli/qmirror.hexa subcommand dispatch
2. **nexus 4-step deprecation plan** (~280 LoC) — step 1 standalone repo (sister BG WIP) → step 4 archival (1-month grace 후)

핵심 발견: **`hx` CLI는 이미 production-ready** (534 LoC bash, 8 subcommands, brew-style multi-target resolution). qmirror 패키징은 (a) registry.tsv 1줄 + (b) `qmirror/install.hexa` hook 두 가지로 즉시 동작.

## Trigger

User: "qmirror 누구나 사용할수 있게 별도 리포로 cli 구성하자 hx install qmirror 로 install 가능 하게"

## Deliverables

| Path | LoC | Purpose |
|---|---|---|
| `docs/hx_install_qmirror_spec_2026_05_03.md` | ~570 | package format + install pipeline design |
| `docs/qmirror_nexus_migration_plan_2026_05_03.md` | ~280 | 4-step deprecation cycle (step 1~4) |
| `state/markers/hx_install_qmirror_spec_landed.marker` | — | spec landing marker |
| `state/markers/qmirror_nexus_migration_plan_landed.marker` | — | migration plan landing marker |

## Key design decisions

1. **manifest.toml = declarative-only**, registry.tsv = SSOT. hx dispatcher가 이미 registry-driven이므로 manifest는 사람을 위한 README + future hx 2.0 forward-compat
2. **install.hexa = pre + post 병합** (HX_HOOK_PHASE env-gated). pre = python_bridge pip install, post = selftest --quick (warn-only)
3. **trust = repo URL 신뢰** (brew-equivalent), package signing은 future cycle
4. **nexus deprecation 4-step**: step 1(this) → step 2 DEPRECATED.md → step 3 consumer refactor → step 4 archival (1-month grace)
5. **DO NOT delete nexus/modules/qmirror/** — git history 보존, working tree 정리는 step 4에서만

## 5 honest C3 caveats (raw#10)

### Spec doc
1. `hx install`은 이미 존재하나 **manifest format은 invent** — registry.tsv가 SSOT인 hx와 redundant, 사람용 doc으로만 기능
2. **package signing 0** — trust = repo URL 신뢰 (brew와 동일하지만 brew는 formula audit, qmirror는 없음)
3. **nexus deprecation 4-step lengthy** — ~4 cycles = ~1개월, step 2~3 사이 dual SSOT 위험
4. **python_bridge auto-resolve의 한계** — `pip install` 시도가 system/conda/venv 환경 따라 실패 가능
5. **Registry not yet stood up** — github.com/dancinlab/qmirror push 전엔 외부 사용자 install 불가

### Migration doc
1. nexus consumer enumeration **estimated**, not measured (~6 files 추정)
2. step 4 archival has **irreversibility cost** (discoverability 손실)
3. 1 month grace는 **임의 결정**
4. dual-SSOT during step 1~3 (nexus/modules/qmirror/ + /Users/ghost/core/qmirror/modules/ 동일 코드)
5. registry.tsv 추가는 **별도 cycle 의존** (미완료 시 step 3 무의미)

## Companion BGs

- **Sister a95ca30a7c** (standalone repo creation): /Users/ghost/core/qmirror/ 디렉토리 채우기. modules/ 11개 .hexa 이미 mirror 완료, cli/ docs/ tests/ install.hexa는 sister가 spec 따라 implement
- **Sister a70e17dd** (nexus CLI integration): nexus CLI 'qmirror' subcommand wrapper. step 3 consumer refactor와 aligned

## Constraints honored

- raw#9 STRICT: Mac → hexa only, .py 0개 생성 (install.hexa는 hexa, pip은 `exec("python3 -m pip ...")` shellout만)
- raw#15: process discipline
- raw#10: 5 honest C3 caveats per doc (총 10개)
- $0 — pure design + spec, no execution
- DO NOT delete nexus/modules/qmirror/ — deprecation only

## Status

| Item | Status |
|---|---|
| spec doc | LANDED |
| migration plan | LANDED |
| qmirror standalone repo populate | sister BG IN PROGRESS |
| nexus CLI wrapper | sister BG IN PROGRESS |
| registry.tsv 1줄 추가 | PENDING (next cycle) |
| GitHub dancinlab/qmirror push | PENDING (next cycle) |
| F-INSTALL-1 6/6 검증 | PENDING (after sister 완료) |
| nexus deprecation step 1→4 | PENDING (future 4 cycles) |

## Falsifier (F-INSTALL-1)

```
[ ] FI-1: registry.tsv 1줄 추가 후 `hx install qmirror`이 ~/.hx/bin/qmirror shim 생성
[ ] FI-2: `which qmirror` → `~/.hx/bin/qmirror`
[ ] FI-3: `qmirror --help` → usage 출력
[ ] FI-4: `qmirror selftest --quick` exit 0 (Aer 미설치 환경에서 install.hexa pip install 후 PASS)
[ ] FI-5: `hx remove qmirror` 깔끔하게 cleanup
[ ] FI-6: `hx install qmirror` 재실행 idempotent
```

PASS 조건 = 6/6. Sister BG 완료 + registry PR merge 후 검증 진행.

## References

- `/Users/ghost/.hx/bin/hx` — existing 534 LoC dispatcher (이미 모든 install 능력 보유)
- `/Users/ghost/core/hexa-lang/tool/pkg/registry.tsv` — canonical registry (8 entries → +1 = 9)
- `/Users/ghost/core/qmirror/` — sister BG standalone target
- `/Users/ghost/core/nexus/modules/qmirror/` — current consumer (11 .hexa, deprecation target)
- `/Users/ghost/core/anima/docs/hexa_lang_module_versioning_landed_2026_05_03.ai.md` — semver + @capabilities precedent
- `/Users/ghost/core/anima/docs/hexa_lang_attr_review_for_qmirror_2026_05_03.md` — substrate compatibility
- `/Users/ghost/core/anima/docs/qmirror_canonical_migration_landed_2026_05_03.ai.md` — qmirror canonical status
