# anima hexa-lang int_parse fix landed 2026-05-05

lane: HEXA-LANG-INT-PARSE-FIX
verdict: state/hexa_lang_int_parse_fix_2026_05_05/verdict.json
fix option: B (rename call sites; no upstream hexa-lang change)
status: PASS — selftest 8/8, berger_session_audio --help + --selftest both green

## Root cause

int_parse was never a hexa-lang builtin. The canonical string-to-int builtin is to_int, registered in self/codegen_c2.hexa line 3870 as hexa_to_int. hexa-brain protocol authors typed int_parse (a reasonable guess for a parse-int idiom) and the mismatch lay dormant because affected protocols rarely exercised numeric CLI flags such as duration, threshold, settle-seconds, gain, etc.

The AI-native error contract embedded in berger_session_audio.hexa even pre-anticipated this exact failure mode (kind INT_PARSE_UNDEFINED, reason describing hexa runtime undefined builtin and patch stage1 fallback).

## Why Option B over A or C

Option A (int_parse builtin alias added to self/codegen_c2.hexa) requires a hexa-lang self-host recompile plus redistribution of the runtime binary. The current binary is byte-identical at both runtime install location and the hexa-lang source tree. Recompile = high blast radius.

Option C (alias in stdlib/parse.hexa) does not work because stdlib is not auto-imported; protocols would need an import line added on top of any rename, more invasive than B.

Option B is purely mechanical: 26 single-token renames across 16 protocol files, zero semantic change.

Minimal-additive principle satisfied at the call-site layer (rename is an additive identifier substitution, no API surface change).

## Files changed (16)

8 in hexa-brain + 8 mirror in anima-eeg:

- berger_session_audio
- berger_session_audio_v3_8ch
- ppg_session_audio
- jaw_session_audio
- blink_session_audio
- cap_fit_verify
- preflight_settle
- master_preflight

26 call sites total. The pre-existing pre_ai_native backup file was intentionally NOT touched (historical artifact).

String-literal occurrences of INT_PARSE_UNDEFINED inside _ai_fix_recipe / _ai_kind_to_reason were preserved as forensic error-contract metadata (these are not function calls).

## Selftest

| Probe | Result |
|---|---|
| to_int 300 | 300 PASS |
| int_parse 300 | Runtime error undefined function (expected) |
| berger --help | usage printed cleanly, no runtime error (PASS) |
| berger --selftest | 8 PASS / 0 FAIL, exit 0 (PASS) |
| hexa check berger | 0 violations (PASS) |

Selftests routed via HEXA_RESOLVER_NO_REROUTE=1 to bypass the Docker-routed resolver which was returning fork-resource errors during the probe window. The Docker container's baked runtime is the same binary, so the fix applies uniformly to production runs.

## Hardware-dependent verification (open)

Real OpenBCI run (duration 300 against actual dongle) was not executed in this session, no hardware attached. Strongest proxy is selftest dry-run path passes 8/8 and help reaches print_usage without runtime error. The undefined-function path is provably unreachable since grep returns empty across hexa-brain + anima-eeg (excluding the bak file).

## Honest C3

See verdict.json honest_c3 array, 6 entries covering: (1) misframed task title (root cause is downstream rename, not upstream missing builtin), (2) Option A trade-off rationale, (3) hardware-dependent verification gap, (4) bak artifact intentionally retained, (5) Docker resolver routing during selftest, (6) compliance audit.

## Compliance

- hexa-only: all changes in hexa files; no python introduced
- honest disclosure: 6 C3 entries in verdict
- additive: mechanical rename, no API surface change, no upstream hexa-lang touched
- LOCK markers: verified, none of the affected protocols carry an own LOCK marker
- DO NOT git commit: no commits made
