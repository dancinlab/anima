# anima EEG AI-native error contract — spec (2026-05-05)

raw#9 hexa-only · raw#10 honest-C3 (≥5) · raw#15 additive · raw#80 sentinel · raw#82 darwin-native

Status: SPEC + Phase 1/2 land. Phase 3 selftest in this BG. Phase 4 handoff next cycle.

---

## §1. Problem statement

EEG protocol failures (helmet, dongle, BrainFlow, hexa runtime) currently surface as:

1. **User-side** — `say -v Yuna "측정 실패"` macOS audio cue. Audible to operator.
2. **AI-agent-side** — sparse stderr text (`Runtime error: undefined function: int_parse` /
   exit-code-only / cue lost in `> /tmp/...log 2>&1` redirects).

This is a **double-blind** failure mode:

- The operator hears the cue but cannot interpret hexa runtime fault classes.
- The AI agent sees a non-zero exit code but cannot recover the *kind*, *site*, or *fix
  recipe* without re-reading 200+ lines of subprocess log.

Concrete witness (this session, 2026-05-05):

- `eeg/protocols/berger_session_audio.hexa --duration 300` →
  `Runtime error: undefined function: int_parse` (sibling BG-HEXA-LANG-INT-PARSE-FIX).
  Voice cue likely emitted; AI agent had to inspect raw stderr to even classify the kind.
- `board_health_check.hexa` `BOARD_PINS_SHORTED` false-positive on alpha-coherent EEG —
  the indicator fires for a real biological signal, not a hardware fault. AI agent has no
  signal to disambiguate from a true short without rerunning under `impedance-validate`.

We need a contract that emits a **machine-parseable trailer** in the same stream that the
agent already inspects (stderr), so any wrapper / shim / parent agent can classify the
fault, find the source site, and surface the recipe — all in one read.

## §2. Contract — stderr sentinel marker (raw#80)

### Failure trailer

Every protocol failure path MUST emit, as the **last two stderr lines** before exit:

```
__ANIMA_EEG_FAIL__ kind=<KIND> site=<HEXA_PATH>:<LINE> fix_recipe=<RECIPE_SLUG>
reason: <human readable>
user_voice_cue_emitted: <true|false>
```

Three lines (not two — typo in BG brief; see §7 C3-1). Exact bytes:

- Line A: `__ANIMA_EEG_FAIL__ kind=<KIND> site=<HEXA_PATH>:<LINE> fix_recipe=<SLUG>`
- Line B: `reason: <human readable, ≤120 chars, no newlines>`
- Line C: `user_voice_cue_emitted: <true|false>`

`HEXA_PATH:<LINE>` may be `eeg/protocols/berger_session_audio.hexa:179` or, if the line is
not statically known (wrapper level), the protocol slug (`berger_session_audio:phase_ec`).

### Success trailer

Every protocol success path MUST emit, as the **last stdout line**:

```
__ANIMA_EEG_OK__ session=<TS_OR_LABEL> ledger=<PATH_OR_NONE>
```

`session=` is either an ISO-ish UTC tag (`2026_05_03T1530Z`) or the protocol label
(`berger_session_audio`). `ledger=` is a state JSON path or the literal `none`.

### KIND enum (initial, raw#10 C5 — extensible)

| KIND                    | exit | meaning                                                    |
|-------------------------|------|------------------------------------------------------------|
| `INT_PARSE_UNDEFINED`   |   1  | hexa runtime undefined builtin (`int_parse`, `to_int`...)  |
| `BOARD_NOT_DETECTED`    |   2  | BrainFlow `prepare_session` failed, dongle / port absent   |
| `IMPEDANCE_RED`         |   3  | impedance check returned RED for ≥1 channel                |
| `BRAINFLOW_TIMEOUT`     |   4  | `start_stream` / `get_board_data` exceeded watchdog        |
| `LSL_NO_OUTLET`         |   5  | LSL outlet missing or no inlet within window               |
| `SESSION_INTERRUPTED`   |   6  | Ctrl-C / SIGTERM received mid-capture                      |
| `BOARD_PINS_SHORTED`    |   7  | board_health: cross-channel correlation flagged short      |
| `BOARD_PINS_SHORTED_FP` |   8  | same as above but helmet-worn → likely false positive      |
| `OTHER`                 |  15  | unclassified; fix_recipe=`see_log`                         |

### Fix-recipe slugs (initial)

- `restage1_int_parse_fallback` — patch hexa stage1 to use string→int helper instead of
  `int_parse` builtin, or apply sibling BG fix.
- `check_dongle_port` — verify `/dev/cu.usbserial-DP04WGIQ` exists and dongle LED green.
- `reseat_electrodes_check_paste` — physically reseat, refresh paste, re-impedance.
- `restart_brainflow_release_all` — `release_all_sessions()` then re-prepare.
- `relaunch_lsl_outlet` — restart upstream LSL producer; verify outlet via `pylsl.resolve_streams`.
- `resume_or_restart_session` — graceful resume from checkpoint OR clean restart.
- `disambiguate_via_impedance_validate` — board_pins_shorted may be biological signal;
  rerun under `impedance_real_hardware_validation.hexa`.
- `see_log` — fall-through; AI agent reads `/tmp/anima_eeg_*.log`.

## §3. try/catch wrapper hexa pattern

Single helper module — `eeg/_lib_safe_call.hexa` — exports:

- `safe_call(label: str, rc: int) -> int` — given a child rc, classify, emit, return rc.
- `_classify_kind(rc: int) -> str`
- `_fix_recipe(kind: str) -> str`
- `_kind_to_reason(kind: str) -> str`
- `say_fail_cue(voice: str) -> int` — bundled cue + sentinel; idempotent.
- `emit_ok(label: str, ledger: str)` — stdout success trailer.
- `emit_fail(kind: str, site: str, voice_emitted: int)` — stderr fail trailer.

Hexa stage1 has no closures / no fn-typed params (raw#10 C3-2), so the contract is
**rc-passthrough**, not lambda-wrap:

```hexa
let rc = run_collect_fg(port, board, duration, "berger_ec", ec_npy)
if rc != 0 {
    say_fail_cue(voice)
    emit_fail("BRAINFLOW_TIMEOUT", "berger_session_audio:phase_ec", 1)
    return rc
}
```

This keeps wrapper hexa-stage1-safe (no closure dispatch) while preserving the AI-native
trailer.

## §4. Apply to existing protocols (Phase 2 priority list)

| Protocol                          | Land tier      | Sentinel land |
|-----------------------------------|----------------|---------------|
| `berger_session_audio.hexa`       | this BG (P1)   | yes           |
| `berger_session_audio_v3_8ch.hexa`| Phase 2 cycle  | spec only     |
| `alpha_eyes_closed.hexa`          | Phase 2 cycle  | spec only     |
| `blink_session_audio.hexa`        | Phase 2 cycle  | spec only     |
| `jaw_session_audio.hexa`          | Phase 2 cycle  | spec only     |
| `cap_fit_verify.hexa`             | Phase 2 cycle  | spec only     |
| `preflight_settle.hexa`           | Phase 2 cycle  | spec only     |

This BG lands the highest-priority patch (`berger_session_audio.hexa` — current witness
case from int_parse fail). Six remaining are spec-bound + tracked in verdict
`patched_protocols[].pending`.

## §5. board_health vs impedance-validate disambiguation

`board_health_check.hexa` cross-channel correlation flags **either** a hardware short
**or** a coherent biological alpha rhythm under a worn helmet. To disambiguate:

- If the protocol context has set `helmet_worn=true` (collected from `cap_fit_verify`
  recent JSON), emit `kind=BOARD_PINS_SHORTED_FP` and append:
  `false_positive_likely_if_helmet_worn=true` on the line after `user_voice_cue_emitted`.
- AI agent SHOULD redirect to `eeg/impedance_real_hardware_validation.hexa` with
  `--electrodes-airborne` (electrodes off head) to confirm true short.

Until cap_fit context plumbing lands, default `helmet_worn=unknown` and emit normal
`BOARD_PINS_SHORTED` with the recipe `disambiguate_via_impedance_validate`.

## §6. Phase 4 dogfood lesson (own 16 sister)

The same sentinel grammar should propagate to non-EEG long-running BG agents
(H100 trainer, RunPod orchestrator) where mid-flight rate-limit / OOM / pod-evict events
currently leave the agent silent:

- `__ANIMA_H100_FAIL__ kind=POD_EVICTED site=p9_phase2:trainer_step_47200 fix_recipe=resume_from_checkpoint_42000`

This unifies the parser surface across substrate boundaries (own 16 watchdog).

## §7. Honest C3 (≥5)

- **C1.** The sentinel marker pattern (`__ANIMA_EEG_FAIL__`) is an **anima-internal**
  convention. No industry standard for EEG protocol error contracts exists; closest
  precedent is BIDS-compliant log JSON, but BIDS does not specify a stderr trailer.
- **C2.** `say_cue` is **macOS-only**. `say -v Yuna` requires `Yuna` voice locale to be
  installed (`Settings → Accessibility → Spoken Content → System Voice`). On linux/RunPod
  pods, `say` is absent → cue silently no-ops; sentinel still emits.
- **C3-1.** The BG brief specified **two** trailer lines but the example showed three;
  this spec adopts **three lines** (sentinel + reason + voice_emitted) for parser
  robustness. Parser MUST tolerate either two or three.
- **C3-2.** Hexa stage1 has **no closures / no fn-typed params**, so the BG-spec
  example `safe_call(label, fn)` is reframed as `safe_call(label, rc)` — rc-passthrough
  rather than lambda-wrap. Functional equivalent, no semantic loss.
- **C4.** **Retroactive cost** — 7 priority protocols × ~5 sentinel emit sites each ≈
  35 patches. This BG lands 1 (berger), spec-binds the other 6.
- **C5.** **KIND enum churn** — 9 entries today; expect to grow by 2-3 per quarter as
  new fail modes surface. Parser MUST treat unknown KIND as `OTHER`, not crash.
- **C6.** **chicken-egg** — if `_lib_safe_call.hexa` itself fails to load (syntax error
  in the lib), no sentinel is emitted because the wrapper itself is the fault. Mitigation:
  lib has a `--selftest` mode that asserts every emit path before any protocol uses it.
- **C7.** **stderr ordering** — interleaved subprocess stderr (BrainFlow Python) may
  insert lines between our trailer lines. AI parser MUST anchor on the
  `__ANIMA_EEG_FAIL__` line then look forward (not back) for `reason:` / `voice_emitted:`,
  tolerating ≤20 lines of noise between them.

## §8. Implementation plan

- **Phase 1** ($0 mac, ~30 min) — write `_lib_safe_call.hexa`, KIND/recipe/reason tables,
  `--selftest` covering 9 KIND × 2 paths (success + fail). **THIS BG.**
- **Phase 2** ($0 mac, ~1 h) — patch `berger_session_audio.hexa` only. Other 6 protocols
  spec-bound + tracked. **THIS BG.**
- **Phase 3** ($0 mac, ~15 min) — synthetic fail-injection selftest in lib + verify trailer
  on stderr for 3 scenarios: `INT_PARSE_UNDEFINED` / `BOARD_NOT_DETECTED` /
  `SESSION_INTERRUPTED`. **THIS BG.**
- **Phase 4** ($0 docs, ~10 min) — handoff `.ai.md` + AI-agent parser template
  (jq / regex). **THIS BG.**

## §9. AI-agent parser template

### grep / awk one-liner (stderr only)

```bash
grep -E '^__ANIMA_EEG_(FAIL|OK)__' /tmp/anima_eeg_*.log
```

### regex (Python)

```python
import re
PAT = re.compile(
    r'^__ANIMA_EEG_FAIL__ kind=(?P<kind>\w+) '
    r'site=(?P<site>[^ ]+) fix_recipe=(?P<recipe>\w+)$',
    re.M,
)
for m in PAT.finditer(stderr):
    print(m.groupdict())
```

### Claude agent prompt fragment

```
After running an EEG protocol, scan stderr for `__ANIMA_EEG_FAIL__` or
`__ANIMA_EEG_OK__`. If FAIL, extract `kind`, `site`, `fix_recipe` and either
auto-recover via the recipe slug OR escalate with the recipe attached. Treat
unknown `kind` as `OTHER` and apply `see_log`.
```

---

End-of-spec.
