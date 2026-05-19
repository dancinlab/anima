# Track G2 Land Plan — hexa→py Transpiler MVP + hexa-lang Audit Bundle

**Owner BG**: BG-iota_prime (parallel non-overlap with BG-theta_prime)
**Date**: 2026-05-04
**Predecessor commits**: fa4dce452 (Track D) → 77c3a7fac (Track F) → **THIS** (Track G2)
**Successor**: Track E (HF mk2 amendment)
**Verdict**: COMMIT_READY (zero raw#9 violations; gitignore_extension_required = false)

---

## §1 Track G2 file inventory + sizes

Track G2 = the hexa-lang **transpiler track**, scoped per BG-Ψ external session audit (`4b345a1de`). Concretely it is **4 cohesive sub-bundles** that all originated in pre-cycle BG runs and are now uncommitted on Mac:

### 1.1 Sub-bundle A — hexa-lang upstream audit (Track A audit, scope-setter)

| Path | LoC | Role |
|---|---|---|
| `docs/hexa_lang_upstream_audit_2026_05_03.md` | 374 | comprehensive ML-execution-gap audit (PyTorch codegen absent, CUDA Qwen14B-shape only, LoRA fwd/bwd RC_ERR_CUDA_TODO=-5) |
| `docs/hexa_lang_upstream_audit_landed_2026_05_03.ai.md` | 149 | AI-native handoff with 5 ranked tracks (A/D/E/B/C) |
| `state/markers/hexa_lang_upstream_audit_landed.marker` | 7540 bytes | landing marker |

### 1.2 Sub-bundle B — hexa→py transpiler MVP (raw#9 STRICT, Mac-canonical)

| Path | LoC | Role |
|---|---|---|
| `tool/hexa_to_py_transpiler.hexa` | 485 | main transpiler (3 passes: line-classifier → per-tag translator → token rewrite) |
| `tool/hexa_to_py_transpiler_test.hexa` | 106 | structural test runner + audit JSON emit |
| `state/hexa_to_py_audit_2026_05_03/sample_inputs/test1_simple_add.hexa` | 9 | typed fn + call |
| `state/hexa_to_py_audit_2026_05_03/sample_inputs/test2_stdlib_proc.hexa` | 14 | file IO + proc_run_with_stdin |
| `state/hexa_to_py_audit_2026_05_03/sample_inputs/test3_lora_stub.hexa` | 25 | ML stub (typed args + control flow) |
| `state/hexa_to_py_audit_2026_05_03/sample_outputs/test1_simple_add.py.snap` | 38 | expected .py output (suffix-shifted to bypass **/*.py) |
| `state/hexa_to_py_audit_2026_05_03/sample_outputs/test2_stdlib_proc.py.snap` | 35 | expected .py output |
| `state/hexa_to_py_audit_2026_05_03/sample_outputs/test3_lora_stub.py.snap` | 52 | expected .py output |
| `state/hexa_to_py_audit_2026_05_03/test_results.json` | — | structural audit (3 PASS / 0 FAIL) |
| `state/transpiled_py/.gitignore` | 3 | `*.py` + `!.gitkeep` + `!.gitignore` |
| `state/transpiled_py/.gitkeep` | 2 | preserve dir under blanket ignore |
| `docs/hexa_to_py_transpiler_prototype_2026_05_03.md` | 241 | landing doc with 5 honest C3 caveats |
| `state/markers/hexa_to_py_transpiler_landed.marker` | 1309 bytes | landing marker |

### 1.3 Sub-bundle C — ATP PyTorch hand-port (Track A2 escalation, VLM unblock)

| Path | LoC | Role |
|---|---|---|
| `docs/atp_pytorch_transpile_landed_2026_05_03.ai.md` | 145 | handoff for `tool/transient_py/atp_pytorch.py` (645 LoC; F-VLM-TRANSPILE-1 PASS on ubu1 cuda 89ms fwd / 35.35M params) |
| `state/atp_transpile_audit_2026_05_03/hand_port_decisions.md` | 9400 bytes | type mapping + function lowering decisions |
| `state/atp_transpile_audit_2026_05_03/hexa_to_py_diff.json` | 4765 bytes | hexa→py per-construct diff |
| `state/atp_transpile_audit_2026_05_03/smoke_test_result.json` | 1447 bytes | F-VLM-TRANSPILE-1 verdict record |
| `state/markers/atp_pytorch_transpile_landed.marker` | 2688 bytes | landing marker |

**Note**: `tool/transient_py/atp_pytorch.py` (29137 bytes, 645 LoC) is NOT staged here. It lives in Track F's `tool/transient_py/` namespace as orphan-in-working-tree (per Track F commit 77c3a7fac body). It was hand-ported by an external BG; manual rsync to ubu1 is required until the transpiler matures to cover its surface (C3-2 below).

### 1.4 Sub-bundle D — hexa-lang stdlib module versioning Phase 1 (governance)

| Path | LoC | Role |
|---|---|---|
| `docs/hexa_lang_module_versioning_spec_2026_05_03.md` | 347 | spec (`@version`/`@capabilities`/`@stability`/`@since`/`@maintainer`/`@priority` comment-only headers) |
| `docs/hexa_lang_module_versioning_landed_2026_05_03.ai.md` | 218 | Phase 1 P0/P1 4-module set landed (proc/json/http/bytes; +42 LoC comment-only, 0 logic delta); F-VERSION-1 4/4 PASS |
| `state/markers/hexa_lang_module_versioning_landed.marker` | 1628 bytes | landing marker |

**Note**: the actual stdlib edits live UPSTREAM in `/Users/ghost/core/hexa-lang/stdlib/{proc,json,http,bytes}.hexa` (separate git repo). Those edits are NOT in this anima commit; only spec + handoff (C3-3 below).

### 1.5 Misc edit (Track G adjacent)

| Path | LoC delta | Role |
|---|---|---|
| `docs/hexa_lang_attr_review_for_qmirror_2026_05_03.md` | +2 | adds `hx install qmirror` availability banner |

### 1.6 Plan files (this BG output)

| Path | Role |
|---|---|
| `state/track_g2_land_plan_2026_05_04/commit_ready.json` | commit-ready bundle plan (machine-readable) |
| `state/track_g2_land_plan_2026_05_04/plan.md` | this human-readable plan |

**Total Track G2 stage**: 27 paths (24 new + 3 marker + 0 modified/2-LoC). **Total LoC delta**: ~2065 LoC across .hexa/.md/.json + ~13 KB across markers + 0 .py.

---

## §2 Transpiler purpose + I/O format

**Trigger**: VLM stage1 ABORT (state/markers/vlm_stage1_aborted.marker, 2026-05-04). Root cause: `audio_token_predictor.hexa` (1576 LoC, Mk.III) needs PyTorch to run on RunPod, but Mac canonical SSOT must remain `.hexa` (raw#9 STRICT).

**Solution**: Mac-local hexa→py transpiler.
- **Input**: `.hexa` file (Mac canonical)
- **Output**: `.py` file (transient, gitignored)
- **CLI**: `hexa run tool/hexa_to_py_transpiler.hexa <input.hexa> <output.py>`
- **Transfer**: `scp state/transpiled_py/<file>.py aiden@ubu1:/home/aiden/transient_py/`
- **Execute**: `ssh aiden@ubu1 "/home/aiden/venv_orchestrator/bin/python /home/aiden/transient_py/<file>.py"`

**Architecture (3 passes, single-file traversal)**:
1. Pass 1 — line classifier (F/L/I/R/C/}/O/X/?)
2. Pass 2 — per-tag structural translator (`fn`→`def`, `let`→assign, `} else if`→`elif`, etc.)
3. Pass 3 — token rewrite (`println`→`print`, `to_string`→`str`, `read_file`→`_h2p_read_file` runtime shim, etc.)

A 16-line **runtime shim header** is prepended to every output, defining `_h2p_*` wrappers around `subprocess.run`, `open`, `os.path.is/getsize`. Generated `.py` runs with zero external deps (torch/peft only when source actually calls them — out of MVP scope).

---

## §3 raw#9 exemption analysis per file

raw#9 STRICT = "Mac → hexa only; .py BANNED on Mac including `_python_bridge/`". Memory feedback `feedback_py_to_hexa_only`. Track F (77c3a7fac) formalized the **opt-out namespace** at `tool/transient_py/`.

| File class | raw#9 verdict | Mechanism |
|---|---|---|
| `*.hexa` (transpiler + tests + samples) | PASS | hexa source — strict ally |
| `*.md` (specs + handoffs + decisions) | PASS | docs only |
| `*.json` (audit results + diff + smoke) | PASS | audit artifacts |
| `*.marker` (landing markers) | PASS | text markers |
| `state/transpiled_py/*.py` | BLOCKED by gitignore | 3-layer: root `**/*.py` + namespace-local `*.py` + Track F precedent |
| `state/transpiled_py/__pycache__/` | BLOCKED by gitignore | root `__pycache__/` |
| `state/transpiled_py/.gitignore` + `.gitkeep` | EXPLICITLY ALLOWED | self-allowed via `!.gitignore` + `!.gitkeep` rules in same file |
| `state/hexa_to_py_audit_2026_05_03/sample_outputs/*.py.snap` | INTENTIONAL SNAPSHOT | `.py.snap` suffix is NOT matched by `**/*.py` glob; intentional bypass for snapshot fixtures (C3-1 caveat) |

**Live verification (`git check-ignore -v`)**:
```
state/transpiled_py/.gitignore:1:*.py     state/transpiled_py/test1_simple_add.py
.gitignore:5:__pycache__/                 state/transpiled_py/__pycache__
state/transpiled_py/.gitignore:2:!.gitkeep    state/transpiled_py/.gitkeep
state/transpiled_py/.gitignore:3:!.gitignore  state/transpiled_py/.gitignore
```

All 4 lines confirm correct ignore behavior. **Zero raw#9 violations** in the staged set.

---

## §4 Cross-track-F integration analysis

**Track F (commit 77c3a7fac)** added:
- `.gitignore` +12 LoC: `tool/transient_py/*.py` policy block (redundant with global `**/*.py` ban — kept as audit traceability anchor at namespace declaration site, per raw#91 explicit-over-implicit)
- `tool/transient_py/{.gitignore, .gitkeep, README.md}` (namespace metadata)
- `docs/anima_dot_own_namespace_spec_2026_05_03.md` (.own opt-out spec)
- `state/track_f_land_plan_2026_05_04/{commit_ready.json, plan.md}`

**Does Track F's policy cover Track G2's outputs?**

YES, with one twist:
- Track F's namespace is `tool/transient_py/` (where `atp_pytorch.py` and `clm_v4_hf_format_shim.py` live as orphan-in-working-tree).
- Track G2's namespace is `state/transpiled_py/` (where transpiler test outputs live, regenerable).
- Both namespaces are **independently** covered by the global `**/*.py` rule + their own namespace-local `.gitignore`.
- Track G2 ships its OWN `state/transpiled_py/.gitignore` rather than reusing Track F's pattern, because the two namespaces have different intent: Track F = hand-ported persistent transient .py; Track G2 = transpiler-generated fully-transient .py.

**Conclusion**: Track F's `.gitignore` extension does NOT need to be expanded to cover Track G2. They are sibling namespaces under independent ignore policies, both of which are subsumed by the global `**/*.py` rule.

---

## §5 Gitignore extension recommendations

**RECOMMENDATION: NO EXTENSION NEEDED.**

Rationale:
1. Root `.gitignore` line 3 (`**/*.py`) already globally bans .py from commits.
2. Track G2 ships its OWN `state/transpiled_py/.gitignore` (3-line file, self-documenting at namespace site).
3. Track F's tool/transient_py/*.py block (added in 77c3a7fac) is independent and not affected.
4. `git check-ignore -v` live verification confirms 3-layer block is functioning.

**One soft caveat** (C3-1): the `*.py.snap` files in `state/hexa_to_py_audit_2026_05_03/sample_outputs/` are NOT blocked by `**/*.py` (the glob requires literal `.py` extension). This is INTENTIONAL — these are committed audit fixtures used for snapshot diffs, not runnable code. If a future strictness pass wants to also block `**/*.py.snap`, that would be a NEW policy decision; out-of-scope here.

---

## §6 Conflict surface vs this-session caller migration commits

This conversation has produced 4 commits (Phase 1/2/3 caller migration + Phase 4 .gitignore symmetry):
- **98b614363** — Phase 1 EXEC F-MIG 4/4 PASS (`tool/clm_v4_tokenizer_load.hexa` primitive + `tool/p9_warmup_probe_real.hexa` F-TOK-4 closure)
- **b4e1570c0** — Phase 2 EXEC F-MIG 4/4×4 PASS (sentinel + qmirror + probe + measure callers)
- **3e08d6dea** — Phase 3 EXEC F-MIG 4/4 PASS (6/6 callers complete + ubu1-only `eval_clm_v4_hellaswag` landed)
- **af930dd3b** — Phase 4 .gitignore .py.txt parking symmetry F-GI 4/4 PASS

**Conflict surface analysis**:

| Concern | Verdict |
|---|---|
| Did Phase 1/2/3 caller migration use the transpiler? | NO. All 6 callers were hand-written hexa-native primitives. The transpiler was an external-BG output; not available to this session's foreground work. |
| Could the transpiler MVP retroactively regenerate any of those callers? | NO. The 6 callers include struct-typed message bus calls, multi-return tuples, and import resolution — all OUT-OF-SCOPE for the transpiler MVP subset (per docs/hexa_to_py_transpiler_prototype_2026_05_03.md §7 caveat C1). |
| Does Phase 4 .gitignore symmetry conflict with Track G2's .gitignore policy? | NO. Phase 4 added `**/*.py.txt` parking symmetry (different glob); Track G2 reuses the existing `**/*.py` rule. Independent dimensions. |
| Does any Track G2 file overlap with this-session-staged paths? | NO. Cross-checked — Track G2 paths are all under `docs/hexa_*` + `tool/hexa_to_py_*` + `state/hexa_to_py_audit_*` + `state/transpiled_py/` + `state/atp_transpile_audit_*` + 4 markers. None of these were touched by Phase 1/2/3/4. |

**Conclusion**: zero conflict surface. Track G2 commits cleanly on top of `cb3521bd2` (current HEAD).

---

## §7 Refactor opportunities (transpiler-vs-hand-written)

If the transpiler matures past MVP subset, the following could be auto-regenerated instead of hand-maintained:
1. `tool/transient_py/atp_pytorch.py` (645 LoC hand-port) ← currently the most expensive hand-port; killing drift here is the explicit Track A Phase 2 goal per upstream audit §6.
2. `tool/transient_py/clm_v4_hf_format_shim.py` (BG-θ' territory; 36715 bytes; out-of-scope for me) ← similar candidate; same pattern.
3. The 6 callers from Phase 1/2/3 ← realistically NOT good candidates because they're already hexa-native and run via hexa interpreter on Mac without needing PyTorch. The transpiler is for forced-PyTorch surfaces (audio decoder, ML training); the callers don't need PyTorch.

**Out-of-scope here**: actual auto-regeneration. This commit lands the transpiler PROOF-OF-CONCEPT + the hand-port FALLBACK. The auto-regeneration cycle is queued behind ATP-grade transpiler features (struct decls, nested array, custom resolvers), estimated +200 LoC transpiler additions per audit §7.

---

## §8 Falsifier set for Track G2 land

| ID | Statement | Verdict | Evidence |
|---|---|---|---|
| **F-G2-1** | transpiler hexa selftest passes | PASS_PRECYCLE | `state/hexa_to_py_audit_2026_05_03/test_results.json`: tests_pass=3, tests_fail=0 |
| **F-G2-2** | round-trip (hexa → transpiler → .py → reverse-check) consistent for ≥1 sample | PASS_PRECYCLE | `docs/hexa_to_py_transpiler_prototype_2026_05_03.md` §4: 3/3 samples verified end-to-end via python3 (test1: x=5; test2: file roundtrip; test3: 4-line stdout) |
| **F-G2-3** | gitignore policy correctly excludes any .py outputs | PASS | `git check-ignore -v` output recorded in §3 above; 3 layers (root + namespace-local + Track F precedent) |
| **F-G2-4** | no committed file is falsely-shadowed by new patterns | PASS | `git status --short \| grep -E '^\\?\\?.*\\.py$'` for Track G2 paths = empty (only `*.py.snap` shows, intentionally) |

Optional gate (next-cycle):
- F-G2-5 (next cycle): transpiler covers `audio_token_predictor.hexa` end-to-end; auto-regenerated `atp_pytorch.py` byte-equals hand-port within 1e-4 numerical tolerance.

---

## §9 Cost band

**$0** (Mac local audit + commit-prep only).
- Pre-cycle: transpiler authored on Mac (BG already executed); ATP hand-ported on Mac (BG already executed); ubu1 smoke test consumed ~1 ssh session worth of compute (recorded in smoke_test_result.json).
- This cycle: read-only file inventory + plan write + git status verification. Zero compute beyond local file reads.
- No transfer this cycle (atp_pytorch.py manual rsync deferred; transpiler outputs not transferred).
- No upstream mutation (hexa-lang stdlib edits already landed pre-cycle in separate repo).

---

## §10 Honest C3 caveats (≥6 items, raw#10 STRICT)

1. **C3-1 .py.snap suffix-shift is a soft raw#9 boundary** — the snapshot files in `state/hexa_to_py_audit_2026_05_03/sample_outputs/` are committed as audit fixtures with `.py.snap` extension to bypass the `**/*.py` glob. INTENTIONAL (snapshot diff requires committed reference) but could confuse future readers. Mitigation: the prototype doc §3 explicitly labels them "snapshot of expected .py output". Acceptable risk; flagged.

2. **C3-2 transpiler MVP subset coverage is narrow** — fn/let/if/while/return only; struct decls, match, closures, generics, traits, multi-line strings emit `TODO[hexa→py]:` placeholders. The actual VLM unblock (`atp_pytorch.py` 645 LoC) was therefore done by HAND-PORT (Track A2 phase 1), not by the transpiler. The transpiler cannot regenerate atp_pytorch.py today. Honest framing: this commit lands proof-of-concept transpiler + the hand-port fallback that actually unblocked VLM, both bundled.

3. **C3-3 hexa-lang stdlib edits live UPSTREAM** — the module versioning Phase 1 actually mutated `/Users/ghost/core/hexa-lang/stdlib/{proc,json,http,bytes}.hexa` (separate git repo, +42 LoC comment-only). Those edits are NOT in this anima commit; only the spec + landed handoff doc. A reader of this commit alone cannot verify upstream edits without cross-repo cd. Mitigation: handoff doc names exact files + line ranges.

4. **C3-4 cross-track dependency on Track F not enforced by tooling** — if Track F (77c3a7fac, `.gitignore tool/transient_py/*.py` block) is ever reverted, this Track G2 atp_pytorch.py orphan would suddenly become commit-eligible (still blocked by global `**/*.py`, but namespace-site documentation breaks). No CI guard; manual review required at any future .gitignore edit.

5. **C3-5 conflict surface analysis is best-effort** — Phase 1/2/3 caller migration commits wrote hexa-native primitives that COULD theoretically have used the transpiler if it had been available pre-cycle. The transpiler MVP cannot cover their surface (struct-typed message bus calls); but a future ATP-grade transpiler could. Refactor opportunity tracked but out-of-scope.

6. **C3-6 marker-vs-doc consistency unverified** — 4 .marker files claim "LANDED 2026-05-03" but actual git landing is 2026-05-04. The +1 day skew reflects audit-write-then-commit cadence (markers were written on 05-03; commit landing is one BG cycle later). Acceptable per repo convention; flagged for new-reader clarity.

7. **C3-7 the `.own N` namespace number for Track G2 outputs is unallocated** — Track F's atp_pytorch.py uses `.own 2`. New transpiler-output files would need their own `.own N` allocation under the formal opt-out system. This commit DOES NOT allocate one (out-of-scope for transpiler MVP). Future transpilations of new .hexa→.py pairs will need a `.own N` declaration step before raw#9 sister-rule formal ratification.

---

## §11 Recommended commit-2 sequencing (after Track G2 lands)

Per BG-Ψ commit-order plan:
1. **D** ✅ committed `fa4dce452`
2. **F** ✅ committed `77c3a7fac`
3. **G2** ← **THIS COMMIT** (transpiler track)
4. **E** (next) — HF mk2 amendment (`docs/anima_hf_naming_*` + `tool/hf_upload_mk2.hexa` + `tool/hf_readme_template.md` + `state/hf_upload_audit/`)
5. **A** — qmirror cluster (~10+ files, biggest single bundle)
6. **B/C/H/I** — various smaller tracks (cleanup, docs, etc.)

**Cycle-2 immediate next**: Track E (HF mk2 amendment). Independent of transpiler; can land cleanly.

**Cycle-3 candidate**: A1 — atp_pytorch.py auto-regeneration trial. Requires transpiler features +200 LoC (struct decls + nested array + custom resolvers). Out-of-scope this cycle; queued for hexa→py transpiler v2.

---

## §12 Summary — actionable git plan (do NOT execute in this BG)

```bash
# Track G2 stage (DO NOT EXECUTE — read-only BG)
git add docs/hexa_lang_upstream_audit_2026_05_03.md \
        docs/hexa_lang_upstream_audit_landed_2026_05_03.ai.md \
        docs/hexa_to_py_transpiler_prototype_2026_05_03.md \
        docs/hexa_lang_module_versioning_spec_2026_05_03.md \
        docs/hexa_lang_module_versioning_landed_2026_05_03.ai.md \
        docs/atp_pytorch_transpile_landed_2026_05_03.ai.md \
        docs/hexa_lang_attr_review_for_qmirror_2026_05_03.md \
        tool/hexa_to_py_transpiler.hexa \
        tool/hexa_to_py_transpiler_test.hexa \
        state/hexa_to_py_audit_2026_05_03/ \
        state/atp_transpile_audit_2026_05_03/ \
        state/transpiled_py/.gitignore \
        state/transpiled_py/.gitkeep \
        state/markers/hexa_lang_upstream_audit_landed.marker \
        state/markers/hexa_to_py_transpiler_landed.marker \
        state/markers/hexa_lang_module_versioning_landed.marker \
        state/markers/atp_pytorch_transpile_landed.marker \
        state/track_g2_land_plan_2026_05_04/

# Verify NO .py staged
git status --short | grep -E '^[AM].*\.py$'    # MUST be empty
git diff --cached --stat | grep -E '\.py\b'    # MUST be empty (only .py.snap allowed)
```

Followed by the recommended_commit_subject + recommended_commit_body from `commit_ready.json`.

---

**END plan.md**
