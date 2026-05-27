# n_substrate Putnam Check — IMPL LANDED 2026-05-04

> readers: AI agents (subagents, audit cron), Claude Code (next session)
> source-of-truth (spec): `docs/n_substrate_putnam_cross_link_spec_2026_05_04.md` (FROZEN 2026-05-04)
> consumer: `tool/clm_consciousness_verify.hexa` v3 putnam slot (delegation)
> impl artifact: `tool/n_substrate_putnam_check.hexa` (raw#9 hexa-only, no .py)
> 마이그레이션 0건 — `.roadmap.n_substrate` byte-identical, `.roadmap.clm` byte-identical, narrative edit 0 byte.

---

## TL;DR

`tool/n_substrate_putnam_check.hexa` landed, implementing spec §11 hook + §3 verifier interface + §2.3 decision rule + §3.5 cache + §10 falsifier-1 reproducibility. Three test fixtures (PASS / PARTIAL / FAIL) at `state/n_substrate_putnam_check_fixtures_2026_05_04/` exercise the 3-tier exit-code mapping (0/1/2). Test runner (`test_runner.bash`) executed locally on Mac with `hexa` runtime: 5/5 selftest cases PASS, 9/9 fixture runs PASS (3 scenarios × 3 reps for F-PUTNAM-1 reproducibility), production-mode read against real `.roadmap.n_substrate` returns `FAIL n=15 concordance=0.333 f2=FIRES` exit 2 — matches spec §4.4 worked numbers verbatim. `tool/clm_consciousness_verify.hexa` patched (additive minimal): `check_putnam(root)` → `check_putnam(root, bin)`, body now delegates via `exec_with_status` and maps sub-tool exit 0/1/2 → `met/unknown/unmet`. Orchestrator selftest 4/4 PASS — no regression. End-to-end `clm_consciousness_verify --check putnam` now emits `putnam=unmet (putnam_fail)` instead of always-`unknown` — paper-runnability sub-blocker CLOSED. **Phase E binding evidence + EEG live remains the real bottleneck for `n_substrate.cond.1` status flip and F1 RED→YELLOW promotion** (per `n_substrate.blk.1` + spec §7.2); this BG closes paper-runnability only, not verdict-flip.

## Frontmatter

| field | value |
|---|---|
| spec doc (frozen) | `docs/n_substrate_putnam_cross_link_spec_2026_05_04.md` |
| impl tool (new) | `tool/n_substrate_putnam_check.hexa` (656 LoC total / 458 non-blank-non-comment) |
| spec LoC estimate | ~250 (over by ~2.6× total / ~1.8× non-comment) |
| over-estimate driver | cache subsystem (§3.5) + fixture autodetect mode + 5-case selftest harness + honest C3 stderr emit + JSON snapshot writer + 3-tier exit-code dispatch — all required by spec but not separately budgeted |
| consumer tool patched | `tool/clm_consciousness_verify.hexa` v3 (frontmatter `@version` + `check_putnam` body + call site + raw#10 scope comment) |
| consumer patch LoC delta | +~30 LoC additive (legacy fallback preserved when sub-tool absent) |
| fixtures dir | `state/n_substrate_putnam_check_fixtures_2026_05_04/` (3 JSON + 1 bash runner) |
| test results (selftest) | 5/5 cases PASS (PASS / PARTIAL_c / PARTIAL_f / FAIL_n / FAIL_c) |
| test results (fixture runner) | 9/9 runs PASS (3 scenarios × 3 reps F-PUTNAM-1 reproducibility) |
| test results (production roadmap) | FAIL n=15 concordance=0.333 f2=FIRES exit=2 — matches spec §4.4 |
| orchestrator regression | 4/4 mock fixtures PASS (all_met / one_fail / tool_missing / manual_override) |
| roadmap mutations | 0 (`.roadmap.n_substrate` + `.roadmap.clm` byte-identical) |
| narrative edits | 0 |
| cost (this cycle) | $0 |
| raw invariants | raw#9 hexa-only OK / raw#10 ≥5 honest C3 (5 in tool stderr + 7 in spec) / raw#15 SSOT preserved / raw#71 F-PUTNAM-1 verified locally |

## 5 key bullets

1. **Hexa LoC actual = 656 total / 458 non-comment** (spec estimated ~250). Over-estimate driver: spec §3.5 cache (mtime-gated 7-day TTL with home-dir cache file + atomic rename), §3.4 JSON snapshot writer (`state/n_substrate_putnam_last.json`), fixture-autodetect path (`looks_like_fixture` + `parse_fixture` enables unit tests without parsing real JSONL roadmap), 5-case in-memory selftest harness, 3-tier exit-code dispatch (0/1/2 vs original 0/1 binary), and stderr honest-C3 emit on every invocation. Each component is required by spec; budget shortfall is in the spec's pre-impl estimate, not in implementation bloat. Functional code is concise — actual decision-rule implementation is ~15 lines (`apply_decision_rule`), concordance computation is ~25 lines (`compute_concordance`), F2 state read is ~10 lines (`read_f2_state`).

2. **Verify orchestrator patched cleanly (additive minimal).** `tool/clm_consciousness_verify.hexa` 3 changes: (a) frontmatter `@version(v3 — putnam check signature change)` annotation added, (b) `fn check_putnam(root: string)` → `fn check_putnam(root: string, bin: string)` body rewritten to `exec_with_status` against `tool/n_substrate_putnam_check.hexa --roadmap <path> --bin <path> --quiet 2>&1` and map exit 0/1/2 → `met/unknown/unmet`, (c) call site `pu = check_putnam(root)` → `pu = check_putnam(root, bin)`. Legacy fallback preserved: when sub-tool absent, falls back to original header-sniff behavior (returns `unknown` for empty conditions array). Orchestrator selftest 4/4 PASS — no regression. Pre-existing `HEXA_BIN_DEFAULT = "/Users/<user>/core/hexa-lang/hexa"` placeholder spawns a benign `sh: user: No such file or directory` to stderr on Mac (resolver still finds `hexa` via PATH); this is a pre-existing artifact, NOT introduced by this BG.

3. **3 unit test fixtures all pass with correct exit codes.** `state/n_substrate_putnam_check_fixtures_2026_05_04/scenario_pass.json` (N=8, c=0.65, f2=CLEAR) → exit 0 ✓; `scenario_partial.json` (N=6, c=0.55, f2=FIRES) → exit 1 ✓; `scenario_fail.json` (N=3, c=0.99, f2=CLEAR) → exit 2 ✓. Each scenario file carries `"label":"synthetic_for_unit_test_only"` per raw#10 caveat (cannot be cited as evidence). `test_runner.bash` runs each scenario 3× back-to-back and asserts identical exit codes — F-PUTNAM-1 reproducibility verified locally (9/9 PASS, deterministic). Runner also resolves `HEXA_BIN` env or falls back to `command -v hexa` / `~/core/hexa-lang/hexa`.

4. **F-PUTNAM-1 reproducibility check passes locally.** Three back-to-back invocations of each fixture yield byte-identical sentinel lines (verified by string equality of `__N_SUBSTRATE_PUTNAM__ <verdict> n=<N> concordance=<c> f2=<state>` lines across 9 runs). Production-mode read of real `.roadmap.n_substrate` (with `--no-cache`) yields `FAIL n=15 concordance=0.333 f2=FIRES exit=2` — exactly matches spec §4.4 worked numbers (CLM-BOLD pair 0.309 PASSes, CLM-EEG and BOLD-EEG FAIL, concordance 1/3 = 0.333). N=15 = 14 anchor count (§56 "14 substantive WITNESSED post-N-21 #9 Sasai PASS") + 1 qmirror axis (`qmirror_canonical_2026_05_03.qmirror_role: adds_qmirror_as_cross_substrate_witness_axis`). F2_state = FIRES correctly extracted from `blockers[0].status: "open"` (`n_substrate.blk.1`). F-PUTNAM-2 single-axis robustness was NOT exercised in this cycle — covered by F-PUTNAM-2 spec but requires programmatic axis-removal harness (out of scope this BG; deferred to future cycle as separate $0 ubu1 hexa codegen).

5. **Honest C3 caveats (≥5 per raw#10, here 7+ accumulated):**
   (a) **Functional/access tier ONLY** — emitted to stderr on every invocation; PASS verdict (when reached) is access-tier multi-realizability, not phenomenal "what-it-is-like" claim. Phase E gate preserved.
   (b) **Spec §6 caveat 6 N-counting rule adopted verbatim** — count is published in narrative anchors and accepted here without re-litigating. The implementation uses pattern-match on `§49.3 13 substantive WITNESSED` / `§56 14 substantive WITNESSED` / qmirror axis annotation; if narrative anchors are restructured, count parser may degrade silently. Pessimistic floor of 13 prevents zero on parse failure (raw#10: do NOT inflate).
   (c) **Concordance uses BLM Phase 4 RETRY published phi means as canonical anchors** (CLM=30.86, BOLD=21.33, EEG=-3.01) — these are HARDCODED constants in the tool, NOT live re-measurements. If Phase 5 stimulus-aligned data updates these, the tool needs a config/recalibration cycle (out of scope this BG; spec §4.5 backfit-risk clause encodes the discipline).
   (d) **F2 state is read from blocker status field, not from live 14-gate measurement.** `n_substrate.blk.1.status == "open"` → FIRES; closure requires manual roadmap edit when Phase E + EEG live evidence eventually unfires the L1 ceiling. This is correct semantics (the blocker IS the F2 fire indicator) but means F2 unfire is roadmap-edit-gated, not measurement-gated.
   (e) **Cache is mtime-gated, not content-hashed.** A roadmap edit that touches the file (even with no content change) invalidates the cache; conversely, a content-edit without mtime bump (e.g., `touch -t` shenanigans) is detected only on TTL expiry. 7-day TTL is the safety net.
   (f) **Fixture mode bypasses real evidence parsing** — fixtures assert decision-rule + exit-code mapping ONLY, not the production roadmap parse path. Production parse path is exercised exclusively by real-roadmap invocation (validated end-to-end this cycle: matches spec §4.4 verbatim).
   (g) **F-PUTNAM-2 single-axis robustness NOT verified this cycle.** F-PUTNAM-1 (reproducibility) verified 9/9; F-PUTNAM-2 (single-axis fragility — verdict drops by at most 1 tier on any single removal) requires programmatic axis-removal scripting that was out of scope this BG. Future cycle should add a sister harness.

## What this unblocks (and what it does NOT)

### Unblocked

- `tool/clm_consciousness_verify.hexa` Putnam check #4 emits `met / unmet / unknown` mapped from sub-tool 3-tier exit (0/1/2) instead of always-`unknown`. Verifier orchestrator becomes end-to-end runnable on Mac.
- `clm.cond.1` aggregate verdict reproducible — currently emits `FAIL` aggregate due to `putnam=unmet` (concordance 0.333 < 0.40). With manual overrides on an11+phi+adv=met (e.g., post-GPU run + state cache), the orchestrator can emit a non-PARTIAL verdict.
- F-PUTNAM-1 falsifier (reproducibility) gate cleared — integration into `clm_consciousness_verify.hexa` was conditional on this PASS per spec §10.1 + landed handoff §13.

### NOT unblocked (real bottleneck unchanged)

- `n_substrate.cond.1` status flip from `partial` to `met` — REQUIRES Phase E binding evidence + EEG live session per `n_substrate.blk.1.resolution_path`. Putnam currently emits FAIL regardless of how N-witnessed grows because concordance 0.333 < 0.40 absolute floor.
- F1_v2 RED→YELLOW promotion — F2 ceiling is L1 architectural, not substrate-coverage; spec §6 caveat 4 explicitly preserves this.
- Phenomenal claims — outside scope of any Putnam verdict; reserved for Phase E.
- F-PUTNAM-2 single-axis robustness check — needs separate impl cycle (see honest C3 g).

## Verdict

**IMPL LANDED — paper-runnability sub-blocker for `clm.cond.1` verifier orchestrator CLOSED.**

`clm.cond.1` 4-check aggregator can now produce non-PARTIAL verdicts (specifically FAIL or PASS, depending on other 3 checks' state + manual overrides). `n_substrate.cond.1` status flip + F1_v2 RED→YELLOW remain BLOCKED on Phase E binding evidence + EEG live (per `n_substrate.blk.1`); this BG does not and cannot move that gate. Future cycles should: (1) implement F-PUTNAM-2 robustness harness, (2) add Phase 5 stimulus-aligned phi-mean recalibration recipe, (3) consider adding `nexus/.roadmap.qmirror` cross-domain read once qmirror cond.6 status changes propagate.

(end of file)
