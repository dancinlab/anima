# preflight re-cascade hook spec — calibrate.hexa D+0 integration

date: 2026-05-01
target file: `anima-eeg/calibrate.hexa` (27,334 bytes / 533 LoC, last touched Apr 28)
upstream tool: `anima-clm-eeg/tool/mk_xii_preflight_cascade.hexa` (376 LoC, read-only aggregator)
roadmap entry: `.roadmap` #172 feeds-main follow-up (d) — D+0 calibration auto re-cascade hook
scope: spec only — no patch to `calibrate.hexa` in this cycle

raw: raw#9 hexa-only · raw#10 honest · raw#11 snake_case · raw#15 SSOT · raw#71 falsifiable · raw#91 honesty-triad

---

## §0 Executive summary

D+0 helmet session (Apr 28) ran the Mk.XII preflight cascade **manually**
before recording, because `calibrate.hexa` predates the cascade tool and has
no automatic invocation hook. This worked once because the operator
remembered. The hook proposed here makes that remembering structural rather
than personal — every `--calibrate` run automatically verifies the 5/5
integration verdict before allowing recording to proceed, eliminating the
class of failures where calibration succeeds locally but the upstream
artifact chain has silently regressed since the last manual cascade run.

Recommendation: **Option C (idempotent, both pre-impedance and pre-recording
gates)**, with cascade RED handled as **prompt user** (not hard halt, not
silent warn) to preserve operator agency in known-degraded scenarios.

The cost of the hook is two extra read-only tool invocations per calibrate
run (~50ms each based on cascade aggregator profile — 5 JSON reads + FNV
fingerprint). The benefit is removal of "I forgot to run preflight" from the
risk surface, which is a category that the helmet-session checklist
documents but cannot enforce.

---

## §1 calibrate.hexa entry-point analysis

source: `anima-eeg/calibrate.hexa` lines 445-531 (`fn main()`)

### 1.1 control flow today

```
main()
├── _flags_only_argv()            // argv normalize (line 446)
├── arg parsing loop              // --selftest / --calibrate / --port / ... (454-485)
├── help short-circuit            // (487)
├── mode-required guard           // exit(2) if neither selftest nor calibrate (489)
├── _write_helper()               // emit /tmp helper python (495)
├── selftest branch               // synthetic 16ch impedance (497-519) → exit
└── calibrate branch (real HW)    // (521-530)
    ├── board_id = _board_name_to_id(board_name)
    ├── args = "calibrate --board-id <n> --seconds <n> [--port ...]"
    ├── println("── calibrate (real hardware) ──")
    ├── println("board: ...") / println("seconds: ...")
    ├── r = _run_helper(args)         // ★ 단일 helper subprocess call
    ├── println(r[0])                 // entire helper stdout
    └── exit(r[1])                    // exit with helper rc
```

The real-hardware path is **single-shot**: one python helper invocation does
everything (board prepare → impedance read → 5s sample → shape verify →
sample-rate verify → emit kv lines), then the hexa wrapper just prints the
helper's body and exits with the helper's return code.

### 1.2 hook insertion candidates

There are three structurally meaningful insertion points:

| ID | location (line) | semantic | accessible state |
|----|----------------|----------|------------------|
| H-pre  | 521 (entry of calibrate branch, before `_run_helper`) | "before any hardware contact" | none — not yet attempted |
| H-mid  | between helper impedance read and recording — **not currently expressible** because helper is monolithic | "after impedance GREEN, before 5s sample" | requires helper split |
| H-post | 530 (after helper returns success) | "after sample verify, before exit" | impedance map + sample shape in `r[0]` |

H-mid is the most semantically clean ("we've verified hardware is healthy, now
verify upstream cascade is healthy") but requires either (a) splitting the
python helper into two phases or (b) adding a second helper invocation that
does only the first half. Both are larger surgery than this spec covers.

H-pre and H-post are both single-line additions in the hexa wrapper and do
not require touching the python helper template at all.

---

## §2 Hook timing options

### Option A — impedance check 직후 (post-impedance gate)

semantically: "if 16/16 GREEN, run cascade before continuing"

requires: H-mid (split helper) **or** post-hoc parse of `r[0]` after helper
returns and re-execute helper for the recording portion only. Both are
non-trivial.

pros:
- catches cascade regression *before* committing to 5s of recording (cheap)
- alignment with "fail fast on the upstream chain"

cons:
- requires helper restructuring or double-invocation (extra hardware cycle)
- impedance read itself takes ~3s; cascade is another ~50ms — saving 5s of
  recording when cascade fails is real but not large
- raw#10 honest: hardware setup cost is dominated by physical electrode
  placement (minutes), not the 5s sample (seconds)

### Option B — recording 시작 직전 (last-sanity gate)

semantically: "calibration was successful; before we declare D+0 ready, sanity
the upstream cascade one more time"

requires: H-post (after helper returns rc=0)

pros:
- single insertion point, no helper restructuring
- fires only when calibrate genuinely succeeded — no noise on hardware fails
- last gate before any downstream tool reads `state/` artifacts

cons:
- "before recording" is misleading — by H-post, recording already happened
  inside the helper. The semantic is really "before the operator trusts the
  output" not "before recording starts"
- if cascade RED, the calibration data still exists; rejecting it requires
  active state cleanup or forcing operator to re-run

### Option C — 둘 다 (idempotent both-gates) ★ RECOMMENDED

semantically: "verify cascade GREEN before hardware contact AND after
calibration success"

requires: H-pre (before `_run_helper(args)` on line 528) **and** H-post
(after `_run_helper` returns rc=0, before line 530's `exit`)

pros:
- pre-gate catches the common case (forgot to run cascade after upstream
  artifact change) before any hardware time
- post-gate catches the rare case (cascade regressed *during* the multi-
  minute calibration session due to concurrent state mutation)
- idempotency: cascade tool is read-only and pure-aggregator (raw#9 line 53
  of `mk_xii_preflight_cascade.hexa`), so running it twice is free of side
  effects beyond the JSON write at `MK_XII_PREFLIGHT_OUT`
- aligned with raw#15 SSOT: cascade verdict is asserted at both boundaries
  of the calibrate operation

cons:
- two cascade invocations per calibrate run instead of one
- requires deciding whether the post-gate JSON output overwrites the pre-gate
  one. Mitigation: set distinct `MK_XII_PREFLIGHT_OUT` paths (e.g.
  `..._pre.json` / `..._post.json`) for the two invocations.

**Recommendation: Option C.** The cost (~100ms total) is negligible against
hardware setup time, and idempotency is already a property of the cascade
tool. Distinct output paths preserve forensic traceability.

---

## §3 Hook invocation form

shell form (called from hexa wrapper via existing `_run_helper`-style shell
interface, **not** by adding a hexa→hexa import — keeps boundary minimal):

```
HEXA_RESOLVER_NO_REROUTE=1 \
MK_XII_PREFLIGHT_OUT=anima-clm-eeg/state/mk_xii_preflight_calibrate_<phase>.json \
hexa run anima-clm-eeg/tool/mk_xii_preflight_cascade.hexa
```

phase ∈ {pre, post}. The output JSON path is parameterized so the pre-gate
and post-gate runs do not clobber each other.

exit code contract (per cascade tool comment lines 16-18):
- `0` → MK_XII_PREFLIGHT_GREEN (5/5) or MK_XII_PREFLIGHT_YELLOW (4/5 w/
  TRIBE deferred)
- `1` → MK_XII_PREFLIGHT_RED (≤ 3/5)

### 3.1 capture

The hexa wrapper captures only the rc; the cascade tool's stdout is verbose
JSON-builder noise that does not need to surface in calibrate's stdout. If
RED, the wrapper reads the just-written `MK_XII_PREFLIGHT_OUT` JSON to surface
the failing component name(s).

### 3.2 env hygiene

`HEXA_RESOLVER_NO_REROUTE=1` is required because cascade is a hexa tool
launched from inside another hexa tool — without the bypass, the resolver
will rewrite the path to its canonical form and double-launch.

`@resolver-bypass` annotation on calibrate.hexa (line 34) covers darwin-
native USB; the cascade subcall does not contradict this because it is itself
read-only and runs on the same darwin host.

---

## §4 Cascade RED handling policy

Three semantically distinct stances are possible:

### 4.1 hard halt (`exit(1)` immediately, refuse to proceed)

pros: strongest gate; impossible to bypass forgetfully
cons: blocks legitimate operator override (e.g., D-day operator knows TRIBE
is in deferred mode and accepts YELLOW; or operator is debugging a failing
upstream component with `MK_XII_*_PATH=/dev/null` for falsification testing
and explicitly does not want the hook to halt)

### 4.2 warn-and-continue (print warning, proceed)

pros: preserves agency
cons: easy to miss in scrolling helper output; recreates exactly the
"forgot the cascade" failure mode the hook was meant to fix — just at a
different point in the workflow

### 4.3 prompt user (TTY interactive y/n) ★ RECOMMENDED

semantics: on cascade RED, print the failing components and prompt the
operator to confirm proceed. Default-on-enter is **abort**; explicit `y`
proceeds.

pros:
- preserves operator agency for legitimate overrides
- forces conscious acknowledgement of degraded state
- aligns with raw#10 honest — operator must explicitly accept that the
  calibration result has caveats

cons:
- TTY-dependent; must be skipped in CI/non-interactive (env detection:
  `if !is_tty(stdin) { fall back to hard halt }`)
- requires `read_line()` or equivalent in calibrate.hexa — verify hexa stdlib
  supports this; if not, this falls back to 4.1 by necessity

### 4.4 escape hatch

`ANIMA_PREFLIGHT_HOOK=skip` env var bypasses the hook entirely. This is
explicit (operator must set it) and is intended for:
- emergency calibration during cascade tool maintenance
- automated falsifier test runs that intentionally synthesize RED

`ANIMA_PREFLIGHT_HOOK=warn` downgrades to 4.2 behavior. Default is 4.3
(prompt) when TTY, 4.1 (halt) when non-TTY.

---

## §5 raw#10 honest — what we know and don't

### 5.1 hook value calibration

D-day session 2026-04-28 (per
`anima-eeg/docs/d_day_helmet_session_results_2026_04_28.md`) ran the cascade
**manually** before recording, and it returned GREEN. The session succeeded.
This is sometimes invoked as evidence that the hook is unnecessary.

**Counter:** the hook is not insurance against "operator runs cascade and it
returns GREEN" — that path is already correct. The hook is insurance against
"operator does not run cascade because they forgot, and an upstream component
silently regressed since the last cascade run." That latter scenario did not
fire on 2026-04-28, but absence-of-fire is not evidence-of-absence.

### 5.2 idempotency claim is shallow

The cascade tool writes to `MK_XII_PREFLIGHT_OUT`. Two invocations within
the same calibrate run write the JSON twice (or to two paths if §3 parameter-
ization is followed). This is not "no side effect"; it is "the same side
effect, re-applied." For our purposes (forensic trace) this is acceptable
but it is not literal purity.

### 5.3 cascade itself is not a hardware verifier

cascade reads pre-existing JSONs (HCI smoke / CPGD / CLM-EEG pre-register /
TRIBE / paradigm v11). None of these are EEG hardware artifacts. So the
hook verifies "the upstream chain that the calibrate run will *feed into*
is intact," not "the EEG hardware itself is intact." Hardware health is
already checked by the impedance helper. The two checks are orthogonal
and complementary; the spec must not present them as redundant.

### 5.4 prompt mode cannot enforce post-prompt honesty

If operator types `y` to proceed despite RED, the calibrate run still emits
its normal artifacts. Downstream consumers should read the `mk_xii_preflight_
calibrate_pre.json` to see verdict status. The hook does not encode the
"operator accepted RED" signal into the calibrate output JSON itself, which
means a consumer that reads only calibrate's output cannot tell whether the
cascade was GREEN or operator-overridden-RED. **This is a gap.** Mitigation
in the implementation cycle: emit `preflight_cascade_verdict=<GREEN|YELLOW|
RED_OVERRIDDEN>` as a kv line in calibrate's stdout.

---

## §6 raw#71 falsifiers (3)

Each falsifier specifies a synthetic scenario that, if produced, would
invalidate a load-bearing claim of this spec.

### F1 — cascade is not idempotent across calibrate-internal invocations

claim under test: §2 Option C is safe because cascade is pure-aggregator
falsifier scenario: run cascade twice in immediate succession with identical
inputs and observe the two output JSONs differ in any field other than
timestamp / fingerprint-of-timestamp
acceptance: if any verdict-bearing field (`cascade_verdict`, per-component
PASS/FAIL) differs between the two runs, Option C is unsound and we must
fall back to Option A or B (single invocation only)

### F2 — TTY detection misclassifies the hexa runtime as non-TTY

claim under test: §4.3 prompt mode degrades gracefully to halt under CI
falsifier scenario: invoke `hexa run anima-eeg/calibrate.hexa --calibrate`
under `tmux` / `screen` / VS Code integrated terminal / `ssh -tt` and
observe the prompt path
acceptance: if any of these legitimate interactive contexts is misdetected
as non-TTY and silently falls back to hard halt, §4.3 is impractical and
must be replaced with explicit operator opt-in (`ANIMA_PREFLIGHT_HOOK=
prompt`) rather than auto-detection

### F3 — pre-gate and post-gate verdict can diverge in non-pathological runs

claim under test: §2 Option C is meaningful because the two gates can in
principle disagree (otherwise post-gate is redundant)
falsifier scenario: run 10 consecutive calibrate cycles on a stable system
and observe pre-gate / post-gate verdict pairs. If all 10 pairs are
identical, post-gate has zero observed value
acceptance: if 10/10 runs show identical pre/post verdicts under stable
conditions, Option C reduces to Option A in practice and the post-gate
can be retired (Option A becomes the recommended form). Note: this
falsifier requires *stable* conditions; concurrent-mutation scenarios are
the actual target of the post-gate, so a 10/10 stable-condition match
does not by itself condemn the post-gate — the test is whether the post-
gate ever triggers in production. Re-evaluate after 30 days of usage.

---

## §7 implementation plan (next cycle)

scope: single patch to `anima-eeg/calibrate.hexa`. No changes to
`mk_xii_preflight_cascade.hexa` or to the python helper template.

### 7.1 patch outline

1. add constants near line 51:
   ```
   let CASCADE_TOOL_PATH       = "anima-clm-eeg/tool/mk_xii_preflight_cascade.hexa"
   let CASCADE_OUT_PRE         = "anima-clm-eeg/state/mk_xii_preflight_calibrate_pre.json"
   let CASCADE_OUT_POST        = "anima-clm-eeg/state/mk_xii_preflight_calibrate_post.json"
   let CASCADE_HOOK_ENV        = "ANIMA_PREFLIGHT_HOOK"   // skip | warn | prompt | (unset → prompt-or-halt)
   ```

2. add helper `fn _run_cascade_hook(phase: string) -> int`:
   - skip if `env(CASCADE_HOOK_ENV) == "skip"`
   - build shell command per §3
   - capture rc; if rc==0, return 0
   - on rc!=0, dispatch per §4 (read CASCADE_OUT_<phase> for failing components,
     prompt-or-halt-or-warn based on env + TTY)
   - return 0 on proceed, non-zero on caller-should-abort

3. insert call sites:
   - line 521 (start of calibrate branch, before `_run_helper(args)`):
     ```
     let pre_rc = _run_cascade_hook("pre")
     if pre_rc != 0 { exit(pre_rc) }
     ```
   - between current line 529 (`println(r[0])`) and 530 (`exit(r[1])`),
     guarded on `r[1] == 0`:
     ```
     if r[1] == 0 {
         let post_rc = _run_cascade_hook("post")
         if post_rc != 0 { exit(post_rc) }
     }
     ```

4. emit `preflight_cascade_verdict_pre=<verdict>` and `preflight_cascade_
   verdict_post=<verdict>` as kv lines in calibrate's stdout (closes §5.4 gap)

estimated diff: +60 to +80 LoC in calibrate.hexa, single-file commit.

### 7.2 test plan (next cycle)

- selftest: cascade hook MUST be a no-op under `--selftest` (synthetic mode
  has no real D+0 contract). Insertion in main() should be guarded on
  `calibrate_mode` only.
- positive: `--calibrate --port <fake>` with all 5 cascade JSONs healthy →
  pre + post both GREEN, recording proceeds, two new JSON artifacts written
- negative pre: `MK_XII_HCI_PATH=/dev/null hexa run anima-eeg/calibrate.hexa
  --calibrate --port <fake>` → pre returns RED, prompt fires (or halts in
  non-TTY); helper subprocess never invoked
- negative post: stable system, simulate post-calibration concurrent mutation
  by deleting one cascade JSON between pre-gate and helper return; verify
  post-gate catches it
- env override: `ANIMA_PREFLIGHT_HOOK=skip` bypasses both gates (verify by
  rendering `MK_XII_HCI_PATH=/dev/null` harmless)

### 7.3 risk register

- R1: hexa stdlib lacks `read_line()` for prompt mode → forces fallback to
  4.1 (hard halt) under TTY too. Mitigation: verify stdlib first; if absent,
  ship hook with §4.1 default and §4.4 escape hatch only.
- R2: `_run_cascade_hook` uses shell subprocess just like `_run_helper`,
  but cascade tool requires `HEXA_RESOLVER_NO_REROUTE=1` env. Verify env
  propagation through hexa's shell-exec layer matches the documented form
  in `mk_xii_preflight_cascade.hexa` line 33.
- R3: cascade output JSON path normalization — calibrate runs from an
  unspecified cwd. Set absolute or repo-relative path explicitly via env.

---

## §8 raw#91 honesty triad

claim: a pre-flight re-cascade hook in calibrate.hexa eliminates the
"forgot to run cascade" failure mode at D+0
evidence: D-day session 2026-04-28 ran cascade manually and succeeded; this
spec proposes converting that manual step into a structural gate at lines
521 and 530 of `calibrate.hexa`
limit: (a) the hook only verifies the upstream-chain JSON aggregate state;
it does not re-run any of the 5 component smoke tests, so a stale-but-still-
on-disk component PASS will continue to register PASS even if the underlying
component has regressed; (b) the prompt branch (§4.3) cannot enforce that
operator-typed `y` was an informed decision; (c) idempotency is shallow —
two invocations write the JSON twice, not "no side effect"

---

end of spec.
