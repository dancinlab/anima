# anima EEG AI-native error contract — LANDED (2026-05-05)

raw#9 hexa-only · raw#10 honest-C3 · raw#15 additive · raw#80 sentinel · raw#82 darwin-native

Companion to spec: `docs/anima_eeg_ai_native_error_contract_spec_2026_05_05.md`
Verdict JSON: `state/eeg_ai_native_error_contract_2026_05_05/verdict.json`

---

## TL;DR for AI agents

EEG protocol failures and successes now emit **machine-parseable trailers** that you can
scan in any subprocess stderr/stdout — no need to re-read the full log.

### Failure trailer (stderr, last 3 lines)

```
__ANIMA_EEG_FAIL__ kind=<KIND> site=<HEXA_PATH:LINE_OR_SLUG> fix_recipe=<SLUG>
reason: <human readable, ≤120 chars>
user_voice_cue_emitted: <true|false>
```

### Success trailer (stdout, last 1 line)

```
__ANIMA_EEG_OK__ session=<TS_OR_LABEL> ledger=<PATH_OR_NONE>
```

## What landed

| Artifact                                                  | Status  |
|-----------------------------------------------------------|---------|
| Spec doc (§1-§9)                                          | LANDED  |
| `eeg/_lib_safe_call.hexa` (KIND enum + emit fns)          | LANDED  |
| `eeg/_lib_safe_call.hexa --selftest` (31/0 PASS)          | PASSED  |
| `protocols/berger_session_audio.hexa` patch (5 fail paths)| LANDED  |
| `protocols/berger_session_audio.hexa --selftest` (8/0)    | PASSED  |
| 3 fail-injection scenarios (INT_PARSE / BOARD / SESSION)  | PASSED  |
| Argv unknown-flag fail-path emits sentinel                | PASSED  |
| Backup of original berger_session_audio.hexa              | LANDED  |
| Verdict JSON                                              | LANDED  |
| AI-agent parser template (regex / grep / prompt fragment) | LANDED  |

## KIND enum (9 entries)

| KIND                    | exit | recipe slug                            |
|-------------------------|------|----------------------------------------|
| INT_PARSE_UNDEFINED     |   1  | restage1_int_parse_fallback            |
| BOARD_NOT_DETECTED      |   2  | check_dongle_port                      |
| IMPEDANCE_RED           |   3  | reseat_electrodes_check_paste          |
| BRAINFLOW_TIMEOUT       |   4  | restart_brainflow_release_all          |
| LSL_NO_OUTLET           |   5  | relaunch_lsl_outlet                    |
| SESSION_INTERRUPTED     |   6  | resume_or_restart_session              |
| BOARD_PINS_SHORTED      |   7  | disambiguate_via_impedance_validate    |
| BOARD_PINS_SHORTED_FP   |   8  | disambiguate_via_impedance_validate    |
| OTHER                   |  15  | see_log                                |

## How to parse from an AI agent

### Python regex

```python
import re
PAT = re.compile(
    r'^__ANIMA_EEG_FAIL__ kind=(?P<kind>\w+) '
    r'site=(?P<site>[^ ]+) fix_recipe=(?P<recipe>\w+)$',
    re.M,
)
for m in PAT.finditer(stderr):
    info = m.groupdict()
    # Auto-route via info['recipe'], OR escalate with info attached.
```

### Bash grep

```bash
grep -E '^__ANIMA_EEG_(FAIL|OK)__' /tmp/anima_eeg_*.log
```

### Claude agent prompt fragment

> After running an EEG protocol, scan stderr for `__ANIMA_EEG_FAIL__` or
> `__ANIMA_EEG_OK__`. If FAIL, extract `kind`, `site`, `fix_recipe` and either
> auto-recover via the recipe slug OR escalate with the recipe attached. Treat
> unknown `kind` as `OTHER` and apply `see_log`. Prefer the trailer over the
> exit code (the hexa stage1 runtime currently clamps rc — see C8).

## Honest-C3 (≥5 — full list in verdict.json)

- **C1.** Anima-internal convention; no industry standard.
- **C2.** `say` is macOS-only; sentinel still emits on linux.
- **C3.** Hexa stage1 has no closures → rc-passthrough pattern instead of lambda-wrap.
- **C4.** Retroactive cost ~35 patches across 7 protocols; this BG lands 1 (berger).
- **C5.** KIND enum may grow; AI parser MUST treat unknown as `OTHER`.
- **C6.** Chicken-egg — emit fns inlined per-protocol so the contract survives lib load failure.
- **C7.** stderr interleaving — anchor on `__ANIMA_EEG_FAIL__`, look forward ≤20 lines.
- **C8.** Hexa runtime exit-code clamp — `hexa run` returns 0 even on internal rc!=0;
  AI agents SHOULD prefer the stderr trailer over rc until sibling BG-HEXA-LANG fix lands.

## Next cycle follow-ups

1. Patch the remaining 6 priority protocols (`berger_v3_8ch`, `alpha_eyes_closed`,
   `blink_session_audio`, `jaw_session_audio`, `cap_fit_verify`, `preflight_settle`).
2. Plumb `helmet_worn=true` context from `cap_fit_verify` recent JSON →
   `board_health_check` → emits `BOARD_PINS_SHORTED_FP` instead of `_SHORTED`.
3. Propagate sentinel grammar to own 16 watchdog (`__ANIMA_H100_FAIL__`).
4. Investigate hexa stage1 `hexa run` rc-clamp (sibling BG-HEXA-LANG).

## Files

- spec: `/Users/ghost/core/anima/docs/anima_eeg_ai_native_error_contract_spec_2026_05_05.md`
- lib: `/Users/ghost/core/hexa-brain/eeg/_lib_safe_call.hexa`
- patched protocol: `/Users/ghost/core/hexa-brain/eeg/protocols/berger_session_audio.hexa`
- backup: `/Users/ghost/core/hexa-brain/eeg/protocols/berger_session_audio.hexa.pre_ai_native_2026_05_05.bak`
- verdict: `/Users/ghost/core/anima/state/eeg_ai_native_error_contract_2026_05_05/verdict.json`
