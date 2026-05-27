# qmirror standalone — 3-step push handoff

**Date:** 2026-05-03
**Author:** anima cycle agent (qmirror standalone push)
**Verdict:** PASS (3/3 steps + smoke verify)
**Cost:** $0
**raw#:** 9 STRICT, 10 (4 honest C3 caveats), 15 (no token in chat)

---

## 0. Executive Summary

`qmirror` standalone repository (extracted from `nexus/modules/qmirror` at
2026-05-03 closure 8/8 cond met) is now a **public GitHub repository** under the
`dancinlab` org, listed in the HEXA package registry (`hx search qmirror`
PASS, `hx where qmirror` PASS). End-users can clone, fork, or `hx install
qmirror` (pending sister BG `a03d549d` hx-install end-to-end land).

| Step | Action | Status | Key artifact |
|------|--------|--------|--------------|
| 1 | local commit | **PASS** | sha `3488b23` (33 files, +6512) |
| 2 | gh repo create + push | **PASS** | `https://github.com/dancinlab/qmirror` |
| 3 | registry.tsv update | **PASS** | line 22 added (6-field TSV) |

---

## 1. Step 1 — Local commit

```
cd /Users/ghost/core/qmirror
git add .
git commit -m "feat(qmirror): standalone 1.0.0 — closure 8/8 cond met (CHSH/IIT/NIST/cross-vendor)"
```

- **Result:** `[main (root-commit) 3488b23] feat(qmirror): standalone 1.0.0 ...`
- **Files added:** 33 (modules/, cli/, docs/, examples/, tests/, hexa.toml, install.hexa, LICENSE, README.md, CHANGELOG.md, .gitignore, state inventory)
- **Insertions:** 6512 lines
- **Commit body** referenced:
  - `docs/closure_2026_05_03.md` (cond_met=8/8, verdict=PASS)
  - `anima/state/markers/qmirror_closure_landed.marker`
  - `anima/docs/nexus_qmirror_spec_2026_05_03.md`
- **8/8 cond enumerated** in commit body (CHSH, IIT phi-star, IBM Heron N=1, NIST tier-1+, ANU 4-tier fallback, Aer tomography, cross-tech alpha burst, Braket cross-vendor)
- **4 closure caveats** copied into commit body (band revisions, paper-analysis, N=1 cross-vendor, no quantum advantage claim)

## 2. Step 2 — GitHub repo create + push

```
gh repo create dancinlab/qmirror --public --source=. --push \
  --description "Quantum Mirror — classical-CPU + ANU QRNG + Aer simulator. 8/8 closure cond met (CHSH/IIT/NIST/cross-vendor). Apache-2.0."
```

- **URL:** `https://github.com/dancinlab/qmirror`
- **Visibility:** PUBLIC (anyone-can-use goal satisfied)
- **License auto-detected:** Apache License 2.0 (`apache-2.0` key)
- **Default branch:** `main`
- **Remote tracking:** `main → origin/main`
- **Auth:** gh CLI keyring (account `dancinlife`, scopes include `repo`, `read:org`, `delete_repo`); **no token printed** (raw#15)
- **Org membership check:** PASS implicitly — repo create succeeded under `dancinlab` (no permissions denied)
- **Pre-existence check:** `gh repo view dancinlab/qmirror` returned `Could not resolve to a Repository` before create (no collision)

## 3. Step 3 — registry.tsv update

**Path:** `/Users/ghost/core/hexa-lang/tool/pkg/registry.tsv`

**Schema discrepancy resolved:** Prompt suggested `name\tgithub_url\tversion`
(3 fields). Actual file header declares 6 fields:
`name<TAB>version<TAB>entry<TAB>repo<TAB>local<TAB>desc`. Followed actual
schema (preserves `hx` parser compatibility).

**Diff (unified):**

```
--- registry.tsv.before
+++ registry.tsv.after
@@ -21,1 +21,2 @@
 yoga	3.2.1	build/yoga-cli	https://github.com/facebook/yoga	/Users/ghost/Dev/hexa-lang/lib/yoga	Facebook Flexbox layout engine ...
+qmirror	1.0.0	cli/qmirror.hexa	https://github.com/dancinlab/qmirror		Quantum Mirror — classical-CPU + ANU QRNG + Aer simulator. 8/8 closure cond met (CHSH/IIT/NIST/cross-vendor). Apache-2.0.
```

**Field-by-field:**

| Col | Value |
|-----|-------|
| name    | `qmirror` |
| version | `1.0.0` |
| entry   | `cli/qmirror.hexa` |
| repo    | `https://github.com/dancinlab/qmirror` |
| local   | *(empty — git-only, no local clone path)* |
| desc    | `Quantum Mirror — classical-CPU + ANU QRNG + Aer simulator. 8/8 closure cond met (CHSH/IIT/NIST/cross-vendor). Apache-2.0.` |

**Verify:**
- `wc -l registry.tsv` → 22 (was 21)
- `grep -c qmirror registry.tsv` → 1
- `awk -F'\t' '/qmirror/ {print NF}'` → 6 (TSV-correct)

## 4. Smoke verify

| Check | Command | Result |
|-------|---------|--------|
| listing | `hx search \| grep qmirror` | **PASS** — `qmirror (1.0.0) — Quantum Mirror...` |
| resolve | `hx where qmirror` | **PASS** — `https://github.com/dancinlab/qmirror` |
| info    | `hx info qmirror` | expected `'qmirror' not installed` (no clone yet) |
| install --dry-run | n/a | `hx install` does not expose `--dry-run` in current bin/hx help |

## 5. Caveats (raw#10 honest C3)

1. **C1 (info)** — GitHub repo is **not** automatically mirrored to HuggingFace. If HF hosting is later desired (LFS-heavy artifacts, model card cross-listing), a separate push is required.
2. **C2 (warn)** — `registry.tsv` entry is added but **NOT yet validated** by full `hx install qmirror` end-to-end (clone → install.hexa → bridge `qiskit-aer`/`pyphi`/`numpy`). Sister BG `a03d549d` hx-install integration is the load-bearing piece. Smoke verify only confirmed `hx search`/`hx where` resolution.
3. **C3 (warn)** — Public Apache-2.0 requires license soundness audit: `pyphi 4.0.b78d0e3` may be GPL-3.0 (spec §13 caveat #3); `qiskit-aer` is Apache-2.0 (OK); ANU QRNG terms-of-service for redistribution unclear. Downstream commercial use may need re-licensing review.
4. **C4 (info)** — Anyone-can-use (public + permissive) implies a **support burden**: external GitHub issues, PRs against ANU 4-tier fallback / Aer numerics / cross-vendor calibration. No SLA committed in README; consider explicit support-posture statement in `closure_landed_handoff.md`.

## 6. Artifacts

- `state/qmirror_standalone_push_2026_05_03/push_audit.json`
- `state/qmirror_standalone_push_2026_05_03/registry_diff.json`
- `state/markers/qmirror_standalone_pushed.marker`
- `docs/qmirror_standalone_pushed_2026_05_03.ai.md` (this file)

## 7. Next steps (suggested)

1. **Wait for sister BG `a03d549d`** (hx install spec land) → then run `hx install qmirror` end-to-end on a clean pkg cache → write `state/qmirror_hx_install_e2e_<date>/verdict.json`.
2. **License audit** for pyphi GPL implications (spec §13 caveat #3 cross-ref).
3. **README support-posture section** to mitigate caveat C4 (no SLA, best-effort issue triage).
4. **HuggingFace mirror** (optional) if cross-listing desired (caveat C1).
5. **Bump `nexus/modules/qmirror`** to thin shim that delegates to `https://github.com/dancinlab/qmirror` (canonical), keeping nexus.qmirror as a façade only.
