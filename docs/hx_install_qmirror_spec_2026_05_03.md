---
title: hx install qmirror — package + install pipeline spec
date: 2026-05-03
mode: doc-only deliverable (no impl, no execution)
authors: anima cycle agent (qmirror standalone packaging)
substrate refs:
  - /Users/ghost/.hx/bin/hx (existing 534 LoC bash dispatcher)
  - /Users/ghost/core/hexa-lang/tool/pkg/registry.tsv (canonical registry)
  - /Users/ghost/core/qmirror/ (sister BG a95ca30a7c standalone repo)
  - /Users/ghost/core/nexus/modules/qmirror/ (current consumer; 11 .hexa files)
  - /Users/ghost/core/anima/docs/hexa_lang_module_versioning_landed_2026_05_03.ai.md (semver + @capabilities precedent)
  - /Users/ghost/core/anima/docs/hexa_lang_attr_review_for_qmirror_2026_05_03.md (substrate compatibility audit)
gate: raw#9 STRICT (Mac → hexa only, no .py creation), raw#10 (≥5 honest C3 caveats), raw#15
---

# 0. TL;DR

`hx install qmirror` 명령으로 누구나 qmirror substrate를 설치 가능하게 하는 **package format spec + install pipeline 설계서**. `hx` CLI는 이미 존재(534 LoC bash, 8 subcommands)하고 brew-style multi-target resolution을 지원하므로 **언어/도구 변경 없이 4 deliverable만 채우면 즉시 동작**한다:

1. `qmirror/manifest.toml` — 14-field package manifest (semver + @capabilities + python_bridge 명시)
2. `qmirror/install.hexa` — pre/post install hook (Aer pip dep 처리, qrng selftest)
3. registry.tsv 1줄 추가 — `qmirror\t1.0.0\tcli/qmirror.hexa\thttps://github.com/dancinlab/qmirror\t/Users/ghost/core/qmirror\tQuantum mirror substrate (NIST-validated)`
4. `qmirror/cli/qmirror.hexa` — entry shim (existing modules/*.hexa subcommand dispatch)

본 문서는 **설계만**, 구현은 sister BG a95ca30a7c(standalone repo) + 차기 cycle. 5 honest C3 caveats §10 참조.

---

# 1. 사전 조사 결과 — `hx install`은 이미 존재

## 1-1. `hx` dispatcher 위치 + 능력

- **위치**: `/Users/ghost/.hx/bin/hx` (Bourne-Again shell 534 LoC)
- **유래**: `hexa — hexa package manager` (header L2)
- **subcommands** (8): `install | update | run | list | remove | search | info | where | orgs`
- **install target classifier** (4 kinds):
  - `name` — registry lookup (e.g. `hx install qmirror`) → fallback to AI-native org probe (`hexa-pkg, dancinlab, dancinlife`)
  - `github` — `user/repo` shortform
  - `url` — full `https://...`, `git@...`, `*.git`
  - `path` — `./local`, `/abs/path`, `~/Dev/...`
- **registry**: TSV format, 6 cols (name | version | entry | repo | local | desc), `/Users/ghost/core/hexa-lang/tool/pkg/registry.tsv` 8 entries (airgenome, nexus, void, anima, hexa-lang, hexa, hive, yoga)
- **install root**: `~/.hx/packages/<pkg>/` (clone or symlink)
- **bin shim root**: `~/.hx/bin/<pkg>` (auto-generated wrapper if `entry` is `.hexa`, else symlink)
- **build hook order**: `bin/build.hexa | install.hexa | bin/build.sh | install.sh` (first match wins, hexa-runner if `.hexa`, bash otherwise)
- **rollback**: build hook 실패 시 `rm -rf $dest` + 심볼릭 bin 정리

## 1-2. 갭 분석 — qmirror 패키징에 부족한 것

| 영역 | 현재 hx 지원 | qmirror 필요 | 갭 평가 |
|---|---|---|---|
| package name resolution | EXACT (registry + org probe) | `hx install qmirror` | **충분** |
| local path install | EXACT (`./qmirror` symlink) | dev-time iteration | **충분** |
| build/install hook | EXACT (`install.hexa` 자동 hexa runner) | python_bridge pip install | **충분** |
| dependency declaration | **없음** (manifest format 자체가 없음) | hexa-lang stdlib >= 1.0.0, qiskit-aer >=0.13 | **갭 (P1)** |
| python_bridge auto-resolve | **없음** | qiskit, qiskit-aer, nistrng, pyphi | **갭 (P2 — install.hexa로 우회)** |
| post-install verification | **없음** (build hook 실행 후 verify 없음) | `qmirror selftest --quick` | **갭 (P1 — install.hexa 마지막 줄)** |
| package signing | **없음** (`# warn-only this cycle` per req §3.3) | future trust chain | **갭 (deferred)** |

**핵심 관찰**: hx는 이미 production-ready brew-style installer다. qmirror 패키징은 (a) registry 1줄 추가 + (b) `install.hexa` hook 작성 두 가지로 충분. **manifest.toml은 P1 design (registry-redundant이지만 dependency declaration의 SSOT 역할)**.

---

# 2. Package format spec — `qmirror/manifest.toml`

## 2-1. 위치 + 형식

- **path**: `/Users/ghost/core/qmirror/manifest.toml` (repo root)
- **format**: TOML (parser 없이 grep/awk로 read 가능, 사람이 직접 편집 가능)
- **canonical 사본**: `qmirror/.hx-manifest.toml` (hidden symlink, hx future가 직접 read 시 사용)

**근거**: hexa-lang은 TOML parser가 stdlib에 없으므로 manifest는 **선언적 문서로만** 기능. registry.tsv가 hx의 실질 SSOT이고, manifest는 (a) 사람을 위한 README-like declaration + (b) future hx version의 향상된 dependency resolution을 위한 forward-compat placeholder.

## 2-2. 14 필드 (full schema)

```toml
[package]
name = "qmirror"
version = "1.0.0"
description = "Quantum mirror substrate (NIST-validated, IIT-MIP, CHSH, QRNG)"
license = "Apache-2.0"
repository = "https://github.com/dancinlab/qmirror"
homepage = "https://github.com/dancinlab/qmirror"
authors = ["dancinlab <noreply@dancinlab.org>"]
keywords = ["quantum", "qiskit-aer", "nist", "iit", "chsh", "qrng"]

[package.entry]
cli = "cli/qmirror.hexa"
exports = ["chsh", "nist", "iit", "qrng", "selftest", "phi", "tomography", "sampler"]

[dependencies]
"hexa-lang/stdlib" = ">=1.0.0"        # proc, json, http, bytes (per module versioning landed)
"hexa-lang/runtime" = ">=0.1.0"        # exec(), json_parse builtins

[python_bridge]
required = true
packages = [
  "qiskit>=1.0.0",
  "qiskit-aer>=0.13.0",
  "nistrng>=1.2.0",
  "pyphi>=1.2.1",
  "numpy>=1.24.0",
]
python_min = "3.9"
install_via = "pip"   # pip | conda | uv | manual

[capabilities]
exposes = [
  "qmirror_chsh_run",
  "qmirror_nist_validate",
  "qmirror_iit_phi_star",
  "qmirror_qrng_bytes",
  "qmirror_selftest_full",
  "qmirror_engine_aer_run",
  "qmirror_tomography_rho",
  "qmirror_sampler_counts",
]
requires = [
  "proc_run_json_bridge",      # hexa-lang stdlib proc (P0)
  "json_object_get",           # hexa-lang stdlib json (P1)
  "http_get_with_headers",     # hexa-lang stdlib http (P1, ANU QRNG)
]

[stability]
tier = "stable"
since = "2026-05-03"
maintainer = "anima-core"
priority = "P0"

[hooks]
pre_install = "install.hexa"      # python_bridge pip install
post_install = "install.hexa"     # qmirror selftest --quick (idempotent)
# Note: same file, gated by env HX_HOOK_PHASE=pre|post

[calibration]
cross_vendor_calibration_required = true
calibration_cost_usd = 41.0       # one-time before full closure (cond.7 cross-tech)
calibration_runbook = "docs/nexus_qmirror_phase3_calibration_runbook_2026_05_03.md"
calibration_skipable_for = ["chsh", "qrng"]   # subcommands that work without calibration

[falsifiers]
chsh = "S > 2.0 ± 0.1 (Tsirelson bound check)"
nist = "≥7/15 NIST SP 800-22 tests PASS @ p=0.01"
iit  = "φ★ > 0 byte-identical across stored TPMs"
```

**총 14 [section] = 8 functional + 6 declarative**. RFC-style: 위에서 아래로 *required → optional → metadata*.

## 2-3. registry.tsv 추가 1줄

```tsv
qmirror	1.0.0	cli/qmirror.hexa	https://github.com/dancinlab/qmirror	/Users/ghost/core/qmirror	Quantum mirror substrate (NIST-validated, IIT-MIP, CHSH, QRNG)
```

- **name** = `qmirror`
- **version** = `1.0.0` (semver per just-landed module versioning)
- **entry** = `cli/qmirror.hexa`
- **repo** = `https://github.com/dancinlab/qmirror` (future GitHub remote)
- **local** = `/Users/ghost/core/qmirror` (this-machine dev convenience)
- **desc** = `Quantum mirror substrate (NIST-validated, IIT-MIP, CHSH, QRNG)`

이 1줄이 추가되면 `hx install qmirror`은 **registry hit → local symlink (path가 존재하므로 clone 생략) → install.hexa 실행 → cli/qmirror.hexa shim 생성** 순으로 동작.

---

# 3. Install pipeline 설계 — `qmirror/install.hexa`

## 3-1. 7-step workflow (`hx install qmirror` user-facing)

```
1. hx install qmirror
   ↓ classify_target → "name"
2. fetch_registry → pkg_field "qmirror" → repo + local + entry + desc
   ↓ local="/Users/ghost/core/qmirror" exists → src_path 사용
3. ln -s /Users/ghost/core/qmirror ~/.hx/packages/qmirror
   ↓ build hook 탐색 → "install.hexa" 발견
4. HX_PKG_DIR=~/.hx/packages/qmirror HX_BIN_DIR=~/.hx/bin HX_PKG_NAME=qmirror \
     hexa ~/.hx/packages/qmirror/install.hexa
     ↓ install.hexa 내부:
        a. python3 -c "import qiskit_aer" → 없으면 pip install
        b. python3 -c "import nistrng"   → 없으면 pip install
        c. python3 -c "import pyphi"      → 없으면 pip install
        d. qmirror selftest --quick (subset: chsh + qrng, 30s 이내, $0)
   ↓ exit 0
5. entry resolution → cli/qmirror.hexa (registry override)
6. .hexa entry detected → ~/.hx/bin/qmirror shim 자동 생성 (hexa interpreter wrapper)
7. green "⬡ installed: qmirror" + dim "  run with: hx run qmirror"
```

## 3-2. `install.hexa` 구현 outline (hexa, ≤80 LoC)

```hexa
// install.hexa — qmirror package install hook
// Env: HX_PKG_DIR, HX_BIN_DIR, HX_PKG_NAME, HX_HOOK_PHASE (pre|post|both)
// Runs under: hexa interpreter (per hx build hook convention)

import "stdlib/proc.hexa" as proc          // proc_run_with_stdin
import "stdlib/json_object.hexa" as json   // json_object_get

fn check_python_pkg(pkg: str) -> int {
  let r: str = exec("python3 -c \"import " + pkg + "\" 2>&1")
  if (contains(r, "ModuleNotFoundError")) {
    return 0
  }
  return 1
}

fn pip_install(pkg: str) -> int {
  print("⬡ pip install " + pkg)
  let r: str = exec("python3 -m pip install --quiet \"" + pkg + "\"")
  return check_python_pkg(strip_version(pkg))
}

fn ensure_python_bridge() -> int {
  let pkgs: [str] = ["qiskit", "qiskit_aer", "nistrng", "pyphi", "numpy"]
  let i: int = 0
  while (i < length(pkgs)) {
    let pkg: str = pkgs[i]
    if (check_python_pkg(pkg) == 0) {
      let ok: int = pip_install(map_install_name(pkg))
      if (ok == 0) {
        print("FATAL: pip install failed for " + pkg)
        return 0
      }
    }
    i = i + 1
  }
  return 1
}

fn run_quick_selftest() -> int {
  let pkg_dir: str = getenv("HX_PKG_DIR")
  let cmd: str = "hexa " + pkg_dir + "/cli/qmirror.hexa selftest --quick"
  let out: str = exec(cmd)
  if (contains(out, "selftest:OK")) {
    print("⬡ selftest PASSED (chsh + qrng subset)")
    return 1
  }
  print("WARN: selftest output: " + out)
  return 0
}

fn main() -> int {
  let phase: str = getenv_default("HX_HOOK_PHASE", "both")
  print("⬡ qmirror install.hexa (phase=" + phase + ")")
  if (phase == "pre" || phase == "both") {
    if (ensure_python_bridge() == 0) {
      return 1   // hx rolls back on non-zero
    }
  }
  if (phase == "post" || phase == "both") {
    let _ = run_quick_selftest()   // warn-only, not a blocker
  }
  return 0
}

main()
```

- **순수 hexa**: `.py` 0개 생성 (raw#9 STRICT 준수). pip 호출은 `exec("python3 -m pip ...")` shellout만.
- **idempotent**: 이미 설치된 pkg는 skip, 재실행 안전.
- **selftest = warn-only**: pip 실패는 fatal (rollback), selftest 실패는 warn (calibration 미실행 환경 고려).

## 3-3. CLI entry — `qmirror/cli/qmirror.hexa` (subcommand dispatch)

```hexa
// cli/qmirror.hexa — qmirror CLI entry (subcommand dispatcher)
// Subcommands: chsh | nist | iit | qrng | selftest | phi | tomography | sampler

fn usage() {
  print("qmirror — quantum mirror substrate")
  print("")
  print("usage: qmirror <subcommand> [args...]")
  print("")
  print("subcommands:")
  print("  chsh        — CHSH inequality run (S vs Tsirelson bound)")
  print("  nist        — NIST SP 800-22 randomness validation")
  print("  iit         — IIT MIP φ★ on stored TPM")
  print("  qrng        — quantum random bytes (Aer or hardware)")
  print("  selftest    — full or --quick selftest (chsh+qrng+iit)")
  print("  phi         — φ★ structured calculator")
  print("  tomography  — ρ matrix reconstruction")
  print("  sampler     — circuit → counts dict")
  print("")
  print("docs: https://github.com/dancinlab/qmirror/docs")
}

fn dispatch(sub: str, args: [str]) -> int {
  // each branch import + delegate; modules already exist in /modules
  if (sub == "chsh")        { return import_run("modules/chsh.hexa", args) }
  if (sub == "nist")        { return import_run("modules/nist_validate.hexa", args) }
  if (sub == "iit")         { return import_run("modules/iit_mip.hexa", args) }
  if (sub == "qrng")        { return import_run("modules/qrng.hexa", args) }
  if (sub == "selftest")    { return import_run("modules/selftest.hexa", args) }
  if (sub == "phi")         { return import_run("modules/phi.hexa", args) }
  if (sub == "tomography")  { return import_run("modules/tomography.hexa", args) }
  if (sub == "sampler")     { return import_run("modules/sampler.hexa", args) }
  print("unknown subcommand: " + sub)
  usage()
  return 1
}

fn main() {
  let argv: [str] = sys_argv()
  if (length(argv) < 2) { usage(); return 0 }
  let sub: str = argv[1]
  let rest: [str] = slice(argv, 2, length(argv))
  return dispatch(sub, rest)
}

main()
```

- **8 subcommands**, 각각 `modules/<name>.hexa` delegate. (sister BG가 modules/ 채움)
- `import_run` = pseudo helper for delegating to existing module file (hexa-lang real impl: `exec("hexa modules/chsh.hexa " + join(args, " "))`).
- **raw#9 STRICT**: 모든 entry는 hexa, .py 0개.

---

# 4. End-to-end install demo (가설)

```
$ hx install qmirror
⬡ fetching registry...
  Quantum mirror substrate (NIST-validated, IIT-MIP, CHSH, QRNG)
⬡ linking qmirror (/Users/ghost/core/qmirror)...
⬡ build hook: install.hexa
⬡ qmirror install.hexa (phase=both)
⬡ pip install qiskit-aer
⬡ pip install nistrng
⬡ pip install pyphi
⬡ selftest PASSED (chsh + qrng subset)
⬡ installed: qmirror
  entry: cli/qmirror.hexa
  run with: hx run qmirror  (or: qmirror)

$ qmirror chsh --shots 10000
⬡ Aer init... CHSH S = 2.793 ± 0.018 (Tsirelson 2.828)
PASS

$ qmirror selftest
⬡ chsh: S = 2.793 PASS
⬡ qrng: 4096-bit entropy = 0.998 PASS
⬡ iit: φ★ = 0.512 byte-identical PASS
⬡ nist: 12/15 PASS @ p=0.01 PASS
selftest: ALL PASS (4/4)
```

---

# 5. Trust + verification (deferred to future cycle)

## 5-1. 이번 cycle의 trust model = warn-only

- registry 출처: `/Users/ghost/core/hexa-lang/tool/pkg/registry.tsv` (in-tree, 사람이 PR로 변경)
- repo 출처: `https://github.com/dancinlab/qmirror` (소유자만 push 가능)
- **package signing 없음** — 사용자는 repo URL을 신뢰해야 함 (brew와 동일)

## 5-2. 향후 trust chain (Phase 2, deferred)

1. **manifest signature** — `qmirror/manifest.toml.sig` (ed25519, maintainer key)
2. **registry signature** — `registry.tsv.sig` (dancinlab org key)
3. **install.hexa attestation** — hash of pre/post hooks logged at install
4. **python_bridge SBOM** — `python_bridge.lock` with hashes (qiskit-aer wheel sha256)

본 cycle은 (1)~(4) 전혀 구현 안함. caveat §10.2 참조.

---

# 6. 호환성 매트릭스

| 환경 | 지원 | 비고 |
|---|---|---|
| macOS (sonoma+, arm64) | **YES** | dev primary, sister BG repo |
| macOS (intel) | YES | qiskit-aer x86 wheel 존재 |
| Linux (ubuntu 22.04+, x86_64) | YES | runpod 환경, P9 cycle 검증됨 |
| Linux (arm64) | PARTIAL | qiskit-aer arm wheel 없을 수 있음 — pip이 source build 시도 |
| Windows | UNKNOWN | hx bash 스크립트 → WSL 필수 |
| Python 3.9+ | required | qiskit 1.0 minimum |
| Python 3.13 | UNTESTED | qiskit-aer wheel TBD |
| hexa interpreter | required (`~/.hx/bin/hexa`) | hx가 자동 탐색 |

---

# 7. 의존성 그래프

```
qmirror (1.0.0)
├── hexa-lang/stdlib >= 1.0.0
│   ├── proc.hexa @ 1.0.0 (P0, 8 capabilities)
│   ├── json.hexa @ 1.0.0 (P1, 4 capabilities)
│   ├── http.hexa @ 1.0.0 (P1, 2 capabilities)
│   └── bytes.hexa @ 1.0.0 (P1)
├── hexa-lang/runtime >= 0.1.0 (exec(), json_parse builtins)
└── python_bridge (optional but recommended)
    ├── qiskit >= 1.0.0
    ├── qiskit-aer >= 0.13.0    ← Aer simulator (CHSH, sampler)
    ├── nistrng >= 1.2.0          ← NIST SP 800-22 validator
    ├── pyphi >= 1.2.1             ← IIT φ★ MIP
    └── numpy >= 1.24.0
```

**호환성 규칙** (per module versioning):
- qmirror major bump 트리거: `[capabilities].exposes` 중 하나라도 rename/remove/arity-change
- hexa-lang stdlib major bump 시: qmirror manifest의 `>=1.0.0` 재검토 필수
- python_bridge minor bump: qmirror selftest re-run 필수, manifest 변경 불필요

---

# 8. 사용자 시나리오 — 3 personas

## 8-1. Researcher (Mac dev, hexa 처음)

```
$ brew install --cask hexa-lang   # 가상의 future, 현재는 manual
$ hexa --version
hexa v1.0.0
$ hx install qmirror
⬡ ... (above demo)
$ qmirror chsh --shots 10000
PASS
```

→ **3분 onboarding**. python pkg는 `install.hexa` 안에서 자동 처리.

## 8-2. CI/CD (linux runner, fresh install)

```yaml
- run: curl -fsSL https://raw.githubusercontent.com/dancinlab/hexa-lang/main/install.sh | bash
- run: hx install qmirror
- run: qmirror selftest --quick
```

→ **headless 가능**. selftest --quick은 calibration 없이도 PASS (chsh + qrng subset만).

## 8-3. Production consumer (nexus integration)

```
# nexus가 qmirror.* 호출 시
$ hx install qmirror
$ # 이후 nexus modules는 import "qmirror/modules/chsh.hexa" 가능
```

→ §9 nexus migration plan 참조.

---

# 9. Spec validation — F-INSTALL-1 falsifier

## 9-1. 목표

이 spec이 *implementable*인지 증명.

## 9-2. Falsifier checklist (6 항목, sister BG가 실행)

```
[ ] FI-1: registry.tsv 1줄 추가 후 `hx install qmirror`이 ~/.hx/bin/qmirror shim 생성
[ ] FI-2: `which qmirror` → `~/.hx/bin/qmirror` (PATH 우선순위 OK)
[ ] FI-3: `qmirror --help` → usage 출력 (cli/qmirror.hexa 정상 invoke)
[ ] FI-4: `qmirror selftest --quick` exit 0 (Aer 미설치 환경에서 install.hexa가 pip install 후 PASS)
[ ] FI-5: `hx remove qmirror` 깔끔하게 cleanup (~/.hx/packages/qmirror, ~/.hx/bin/qmirror 모두 제거)
[ ] FI-6: `hx install qmirror` 재실행 → 기존 install 완전 교체 (idempotent)
```

**현재 cycle**: 0/6 (sister BG가 검증 예정). spec PASS 조건 = 6/6.

---

# 10. Honest C3 caveats — 5개 (raw#10 준수)

## 10-1. `hx install`은 이미 존재하나 manifest format은 invent

- 본 spec의 `manifest.toml`은 **registry.tsv가 SSOT인 hx와 redundant**. 사람을 위한 README-like 문서로만 기능. hx dispatcher는 manifest를 read 안함 (P1 design — future hx 2.0가 사용 가능).
- **결과**: 이번 cycle의 manifest.toml은 declarative-only. 실제 install은 registry.tsv 1줄로 작동.

## 10-2. Package signing 0 — trust = repo URL 신뢰

- §5에서 명시한대로, 본 cycle은 manifest signature, registry signature, install.hexa attestation 모두 deferred.
- **위험**: 누군가 `dancinlab/qmirror` 저장소를 컴프로마이즈하면 `hx install qmirror` 사용자 모두 영향. brew와 동일한 trust model이지만, brew는 formula audit이 있고 qmirror는 없음.
- **mitigation**: 향후 cycle에서 (a) GitHub release tarball + sha256 lock, (b) maintainer key signature, (c) verify-on-install flag.

## 10-3. nexus deprecation 4-step lengthy — 1개월+ grace

- §11(별도 doc)의 4-step migration은 **각 step 1 cycle씩 가정 시 ~4 cycles = ~1개월**. nexus consumer가 12개 모듈에 걸쳐 `import "modules/qmirror/..."` 사용 중인 경우, refactor + test re-run 비용이 step 3에 집중됨.
- **위험**: step 2~3 사이에 nexus가 두 군데 qmirror (in-tree + standalone) 의존 가능 — 동기화 비용 발생.
- **mitigation**: deprecation marker 명시 + step 3에 자동화 script 제공 (in-tree → standalone import path rewrite).

## 10-4. python_bridge auto-resolve의 한계

- `install.hexa`의 `pip install` 시도는 (a) PyPI 접근 가능 + (b) 사용자가 system python 사용 + (c) virtualenv 활성화 환경 모두에서 동일하게 작동하지 않음.
- **실패 케이스**: `pip install --user` 권한 없는 system, conda env 활성화된 사용자, M1 Mac에서 qiskit-aer 일부 wheel 없음.
- **mitigation**: `install.hexa`에 `--dry-run` 모드 + 명시적 `python3 -m venv` 가이드 (manifest의 `python_bridge.install_via` 필드로 유저 의도 받기).

## 10-5. Registry not yet stood up — 'github.com/dancinlab' 의존

- 현재 registry는 `/Users/ghost/core/hexa-lang/tool/pkg/registry.tsv` (single file, repo 안에). `https://github.com/dancinlab/qmirror`이 실제 push 되기 전엔 `hx install qmirror`은 local path (`/Users/ghost/core/qmirror`)만 작동.
- **결과**: 다른 사용자(@nerve011235 외)는 본 cycle에선 install 불가. sister BG a95ca30a7c가 standalone repo를 GitHub에 push한 후에야 외부 install 가능.
- **mitigation**: 본 spec PASS = (a) registry.tsv 1줄 추가 + (b) GitHub push + (c) `HX_ORGS=dancinlab hx install qmirror` 외부 시연 성공. 이번 cycle은 (a)만 design 명세.

---

# 11. Cross-link with sister BGs

## 11-1. Sister a95ca30a7c — standalone repo creation

- **할당**: `/Users/ghost/core/qmirror/` 디렉토리 채우기 (modules/ 11개 .hexa, cli/ entry, install.hexa hook)
- **본 spec의 입력**: 본 문서가 명세하는 manifest.toml + install.hexa + cli/qmirror.hexa schema
- **본 spec의 출력**: sister가 implement → 본 spec의 §9 falsifier 6/6 검증

## 11-2. Sister a70e17dd — nexus CLI integration

- **할당**: nexus CLI에서 `nexus qmirror chsh ...` 같은 wrapper subcommand 추가
- **본 spec과의 관계**: nexus CLI는 standalone qmirror가 `hx install qmirror`로 설치된 후 `qmirror.*` 모듈을 import. **migration step 3** (nexus_qmirror_migration_plan §3.3)와 동기화 필수.

## 11-3. 본 spec의 출력

- `docs/hx_install_qmirror_spec_2026_05_03.md` (본 문서)
- `docs/qmirror_nexus_migration_plan_2026_05_03.md` (별도 doc)
- `docs/hx_install_qmirror_spec_landed_2026_05_03.ai.md` (handoff)
- `state/markers/hx_install_qmirror_spec_landed.marker`
- `state/markers/qmirror_nexus_migration_plan_landed.marker`

---

# 12. ROI estimate

| 영역 | 현재 (in-tree nexus/modules/qmirror) | After hx install qmirror | Δ |
|---|---|---|---|
| 사용자 onboarding 시간 | nexus repo 전체 clone 후 PYTHONPATH 설정 (~30 min) | `hx install qmirror` (~3 min) | **-90%** |
| dependency clarity | nexus requirements.txt 60+ 라인 | qmirror manifest 5 packages | **+12x clarity** |
| version management | nexus monorepo single version | qmirror semver per module | **+isolation** |
| 외부 cite | `nexus/modules/qmirror/...` (50+ char path) | `qmirror.chsh` (2-segment) | **+UX** |
| nexus repo size | qmirror 11 hexa = ~80KB included | extracted | **-80KB** (나중에 4-step migration 후) |

**총 ROI**: brew-style installer convention + smaller dependency surface + version isolation. 비용은 spec 작성 시간 (본 cycle, doc-only) + sister BG impl 시간 (다음 cycle).

---

# 13. Status + next actions

| Item | Status | Owner |
|---|---|---|
| spec doc (본 문서) | LANDED 2026-05-03 | this BG |
| nexus migration plan (별도 doc) | LANDED 2026-05-03 | this BG |
| qmirror standalone repo populate | IN PROGRESS | sister a95ca30a7c |
| nexus CLI wrapper | IN PROGRESS | sister a70e17dd |
| registry.tsv 1줄 추가 | PENDING | next cycle |
| GitHub dancinlab/qmirror push | PENDING | next cycle |
| F-INSTALL-1 6/6 검증 | PENDING | next cycle (after sister 완료) |
| nexus deprecation step 1→4 | PENDING | future 4 cycles |

**입회 sequence** (이상적 시나리오):
1. (today) sister a95ca30a7c → /Users/ghost/core/qmirror 채움
2. (today) sister a70e17dd → nexus CLI wrapper
3. (next cycle) registry.tsv 1줄 PR + local install 검증
4. (next cycle) GitHub push + 외부 install 검증
5. (cycle+2) nexus deprecation step 1 marker
6. (cycle+3..6) deprecation step 2~4

---

# 14. References

- `/Users/ghost/.hx/bin/hx` — existing 534 LoC bash dispatcher
- `/Users/ghost/core/hexa-lang/tool/pkg/registry.tsv` — canonical registry (8 entries)
- `/Users/ghost/core/qmirror/` — sister BG standalone target (modules/ 11 files, cli/ docs/ tests/ stubs)
- `/Users/ghost/core/nexus/modules/qmirror/` — current consumer (11 .hexa, to be deprecated)
- `/Users/ghost/core/anima/docs/hexa_lang_module_versioning_landed_2026_05_03.ai.md` — semver + @capabilities precedent
- `/Users/ghost/core/anima/docs/hexa_lang_attr_review_for_qmirror_2026_05_03.md` — substrate compatibility audit
- `/Users/ghost/core/anima/docs/qmirror_canonical_migration_landed_2026_05_03.ai.md` — qmirror canonical status
- `/Users/ghost/core/anima/docs/nexus_qmirror_phase3_calibration_runbook_2026_05_03.md` — calibration runbook (manifest.calibration field)
