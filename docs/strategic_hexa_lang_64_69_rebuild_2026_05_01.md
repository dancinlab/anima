# Strategic — hexa-lang upstream roadmap 64-69 binary rebuild (W2)

> **ts**: 2026-05-01
> **agent**: N-51 W2
> **scope**: Attempt the registered hexa-lang upstream roadmap 64-69 binary-rebuild fix to unblock the general `hexa→native` compiler that gates N-51 EXEC E (#54) and downstream tracks.
> **race-isolated dirs**: `state/strategic_hexa_lang_64_69_rebuild_2026_05_01/*.json` + this doc + `/Users/ghost/core/hexa-lang/` (write authorization granted but unused — see §3)
> **honest C3**: NO upstream code changed. Diagnosis revealed the blocker is not a missing compiler but two policy gates that the N-51 caller wasn't honoring; all 3 N-51 hexa components built and selftest-passed using existing toolchain.

---

## §1 Verdict (top-line)

**NOT_FEASIBLE_IN_SESSION reframed as NOT_NECESSARY_IN_SESSION.**

- Memory anchor `reference_hexa_roadmap_64_69.md` is **9 days stale**. The numeric `64-69` entry scheme was **retired 2026-04-25 commit 3caebc54** in upstream `/Users/ghost/core/hexa-lang/.roadmap` (header line 2). It was replaced 2026-04-26 with the convergence-cycle structure `[SH1]..[SH-Ω]` plus the `RFC-001..009` bundle (anima-eeg-sourced, raw#159). The `parent 64 + children 65/66/67/68/69` mapping no longer exists.
- The N-51 EXEC E ledger claim "absence of general `hxc` hexa→native compiler on Mac/ubu1/ubu2 (only single-program AOT shards `hxc_a25..a34` exist)" is a **misdiagnosis**: `hexa build <src> -o <out>` is the general compiler, ships in `/Users/ghost/core/hexa-lang/hexa.real` (Mach-O 64-bit arm64, version `0.1.0-dispatch`), and works today on Mac when two intentional safety gates are honored.
- All **3 N-51 hexa components compile and selftest-PASS** through the existing toolchain (5/5 + 4/4 + 3/3 selftest probes). Total wall-time from finding to verified PASS: ~5 min.
- Cost: **$0** (entire investigation local on Mac, no GPU pods touched, alpha pod `lzw79649ob80uk` untouched per mission constraint).

---

## §2 Phase 1 — entries 64-69 enumerated (per upstream truth, post-2026-04-26)

The legacy 64-69 numeric mapping (memory-cited):

| legacy id | mapped milestone | original spec source |
|---|---|---|
| parent 64 | 5-axis self-host roadmap | `docs/upstream_notes/hexa_lang_full_selfhost_prompt_20260423.md` |
| 65 | M3 argv | argv[0] duplicate-insert policy fix |
| 66 | M4 codegen | `__hexa_strlit_init` per-module namespacing for `hexa cc --regen` binary rebuild |
| 67 | M5 Linux driver | hxa-20260423-002 subsumes |
| 68 | M2 mangling | builtin `hx_` prefix completion |
| 69 | M1 runtime split | `runtime_core.c` ≤500 LoC + `runtime_hi.hexa` |

**Current upstream truth (`/Users/ghost/core/hexa-lang/.roadmap`):**

| current id | status | omega-stop | what it actually is now |
|---|---|---|---|
| `[SH1]` | partial | compute-saturation | AOT cc dispatch surface (cc-swap ceiling reached; HEXA_AOT_CC env toggle live) |
| `[SH2]` | todo | banach-fixpoint | runtime.c TU split + cached `runtime.o` |
| `[SH3]` | active | fixpoint-convergence | hexa-source → IR frontend bridge; phase 1 trivial println **CLOSED 2026-04-26 (1.E witness)**; phase 2.A/2.B/2.C arith DONE; 2.E/2.F deferred-witness on env instability |
| `[SH4]` | partial | banach-fixpoint | `aot_cc_select.hexa` selector tool, **10/10 selftest**; rewire pending |
| `[SH-Ω]` | partial | fixpoint-convergence | terminal: zero external C-compiler on AOT path; narrow-acceptance residual cardinal **= 2** ({W-α line 1761, W-α' line 1021}); selector default flip waits on SH3 phase 6 |
| `RFC-001` | partial-landed | fixpoint-convergence | `popen_lines()` / `process_spawn()` streaming subprocess stdlib (P0); capture+split LANDED 2026-04-28, streaming deferred |
| `RFC-002` | done | banach-fixpoint | `map.has(key)` (P1) — landed 2026-04-28 |
| `RFC-003..007` | proposed | fixpoint-convergence | escape sequences, ends_with AOT codegen, exec semantics, lint rules |
| `RFC-008` | done | fixpoint-convergence | `project_python()` project-relative helper (P1) — landed 2026-04-28 |
| `RFC-009` | new | fixpoint-convergence | AOT bool coercion bug (P0 silent-wrong; RFC-005 family) |

The mapping memory→reality is approximately:
- **65 M3 argv** → embedded in SH3 phase ladder, no longer a standalone entry
- **66 M4 codegen** → split into SH3 (general bridge) + RFC-005/009 (specific AOT codegen correctness bugs)
- **67 M5 Linux driver** → `build/hexa_v2_linux_x86_64` static musl ELF shipped pre-2026-04-26; coordination now via SH3 `codegen_native_elf.hexa` parallel track
- **68 M2 mangling** → done; `hx_` prefix in production
- **69 M1 runtime split** → SH2 (todo, but not blocking N-51)

---

## §3 Phase 2 — gap diagnosis + smallest-entry-to-fix

**N-51 EXEC E true blocker chain (root-cause traced through experiment):**

1. **Gate G1 — Darwin /tmp panic-trigger output-path refusal**
   - Source: `/Users/ghost/core/hexa-lang/self/main.hexa` lines 991-1037 (`cmd_build`)
   - Rule: on Darwin, refuses output paths matching basename ending `_mac`/`-mac`/`_darwin`, output under `/tmp` or `/private/tmp`, source with `@refuse`/`@heavy` annotation
   - Cause: 2026-04-20 03:33 Mac kernel panic (`train_alm_lora_mac` swap exhaustion, 49 swapfiles, loginwindow watchdog 91s timeout)
   - **Bypass**: `HEXA_MAC_BUILD_OK=1` env var
   - N-51 collision: EXEC E wrote outputs to `/tmp/n51_E/*` — exactly the refused path

2. **Gate G2 — auto-invoke conflict on `fn main()` + top-level `main()` call**
   - Source: `self/native/hexa_v2` transpile (silent-failure-enforcement Class 1)
   - Rule: if a script has both `fn main()` definition AND a top-level `main()` call, transpile errors out
   - Fix: strip the trailing `main()` line, OR add `@manual_main` attribute on `fn main`
   - N-51 collision: all three of `comp1.hexa`, `comp3.hexa`, `comp4.hexa` had this exact pattern at the file tail

**Smallest entry to fix**: NONE upstream. Both gates are intentional safety enforcement with documented bypasses; modifying either would weaken existing kernel-panic-prevention and silent-failure-enforcement subsystems for negative ROI. The fix locus is the **N-51 caller**, not hexa-lang.

---

## §4 Phase 3 — fix attempt result

**Code changed in `/Users/ghost/core/hexa-lang/`**: `N` (zero lines, zero files).
**Off-repo staging dir** (Claude-feasible per HEXA-FIRST + race isolation): `/Users/ghost/core/anima_offrepo_n51_w2/`.

**Build invocation that worked** (5 min wall-time, all 3 N-51 components):

```
HEXA_MAC_BUILD_OK=1 /Users/ghost/core/hexa-lang/hexa.real \
    build <src.hexa> -o <non-tmp-output-path>
```

Where `<src.hexa>` is the N-51 component with the trailing `main()` line stripped (or with `@manual_main` on `fn main`).

| Comp | Source LoC | Binary size | Selftest result |
|---|---:|---:|---|
| comp1 emit | 123 | 234,384 B Mach-O arm64 | 5/5 PASS |
| comp3 readback | 160 | 234,832 B Mach-O arm64 | 4/4 PASS (1 non-fatal `find_at` codegen warning) |
| comp4 orchestrator | 128 | 235,440 B Mach-O arm64 | 3/3 PASS |
| **TOTAL** | **411** | **~705 KB** | **3/3 components PASS** |

Trivial smoke (`println("hello from n51 smoke")`) at `/Users/ghost/core/anima_offrepo_n51_w2/bin/n51_smoke` → 233,200 B Mach-O arm64, runs `rc=0`, prints `hello from n51 smoke`.

Evidence binaries persist at `/Users/ghost/core/anima_offrepo_n51_w2/bin/{n51_smoke,comp1,comp3,comp4}` for caller verification.

---

## §5 Phase 4 — cross-impact

**Tracks unblocked by W2 finding:**

- **N-51 EXEC E** (this mission's parent): FULL — phase 1 bridge build can complete in 5-10 min. Phase 2-5 cost ($15-20) and risk profile unchanged from prior estimate.
- **N-51 #52 sequential**: FULL (likely same root cause; W2 cannot verify without violating race isolation against #55/#56 sibling agent dirs).
- **Future N-22-24 hexa-native dynamic measurement scripts**: FULL on hexa-toolchain axis. Authors must (a) put `@manual_main` on `fn main` or skip top-level `main()` call, (b) build to repo-local non-`/tmp` path, (c) export `HEXA_MAC_BUILD_OK=1` on Mac.
- **All other N-substrate trackers** that quote memory `reference_hexa_roadmap_64_69.md`: POTENTIAL FULL — each needs re-audit against G1+G2 rather than blanket `wait for upstream 64-69`.

**Tracks NOT unblocked:**

- **SH-Ω narrow acceptance closure**: real upstream work (W-α + W-α' rebuild requires load <2 + tree clean), orthogonal to N-51.
- **RFC-005 / RFC-009 AOT codegen correctness**: real silent-wrong codegen bugs; affect specific user code patterns (`ends_with`-on-strings, `int_fn() == int_literal` sentinel checks). N-51 Comp 1/3/4 happen not to use those patterns.
- **SH3 phase 6 `use` stmt + module loader closure**: gates SH-Ω final ⅓ but irrelevant to single-file N-51 components.

---

## §6 Phase 5 — verdict + honest C3

**Verdict: NOT_NECESSARY_IN_SESSION (W2 attempted upstream fix → discovered no upstream fix needed; N-51 unblocks via 2-line caller-side policy compliance).**

**Top 3 honest C3 disclosures:**

1. **Memory `reference_hexa_roadmap_64_69.md` is 9 days stale and describes a numeric entry scheme retired 2026-04-25 commit `3caebc54`.** Continuing to cite it without verification produces phantom blockers and category errors like the N-51 EXEC E `INDETERMINATE — toolchain blocker` ledger entry. Memory file should be either updated to point at the SH1..SH-Ω + RFC-001..009 structure or deprecated with a forwarding note.

2. **N-51 EXEC E §1 verdict was a category error**: it conflated `single-program AOT shards hxc_a25..a34 only run their embedded selftests` (true — those are pre-baked artifacts for hot-path agents) with `no general hexa→native compiler exists` (false — `hexa build` is the general compiler, works today on Mac). The shards' existence is an *optimization*, not a substitute for the build path.

3. **W2 did NOT modify hexa-lang.** This is the honest accounting — there was nothing in upstream that, fixed in-session, would unblock N-51 that wasn't already addressable caller-side. The remaining genuine upstream items (SH3 phase 2.E/2.F deferred-witness on env instability, SH-Ω W-α rewire awaiting load-<2 window, RFC-005/009 AOT codegen correctness) are real but ORTHOGONAL to N-51's specific Comp 1/3/4 needs. Claiming a fix to those would be false flag-planting; documenting the discoverability resolution is the truthful deliverable per raw#10 + raw#71.

---

## §7 One-sentence summary

> **hexa-lang 64-69 stale-memory-mirage → N-51 fully unblockable today via `HEXA_MAC_BUILD_OK=1` + non-`/tmp` output + trailing-`main()`-strip; 3/3 components compile + selftest PASS, $0 burn, 0 upstream code change.**

---

## §8 Cross-references

- Mission anchor: `docs/strategic_alm_tension_field_exec_E_results_2026_05_01.md` (the misdiagnosis to be revised)
- Stale memory: `/Users/ghost/.claude-claude12/projects/-Users-ghost-core-anima/memory/reference_hexa_roadmap_64_69.md`
- Upstream truth: `/Users/ghost/core/hexa-lang/.roadmap` (created 2026-04-26)
- Upstream selfhost prompt (legacy 64-69 spec): `docs/upstream_notes/hexa_lang_full_selfhost_prompt_20260423.md`
- Darwin /tmp refusal source: `/Users/ghost/core/hexa-lang/self/main.hexa:991-1037`
- Auto-invoke enforcement source: `self/native/hexa_v2` binary (silent-failure-enforcement Class 1, ref `doc/audit/silent_failure_enforcement_audit.md`)
- W2 phase ledgers: `state/strategic_hexa_lang_64_69_rebuild_2026_05_01/{phase1_references,phase2_diagnosis,phase3_fix_attempt,phase4_cross_impact,phase5_verdict}.json`
- Off-repo build evidence: `/Users/ghost/core/anima_offrepo_n51_w2/bin/{n51_smoke,comp1,comp3,comp4}` Mach-O 64-bit arm64
