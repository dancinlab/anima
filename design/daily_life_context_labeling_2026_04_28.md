# Daily-Life Context Labeling — Design Doc (2026-04-28)

## Purpose
Provide ground-truth activity labels for EEG signals during awake daily-life
recordings. The EEG verifier (`anima-eeg/tool/eeg_daily_life_verifier.hexa`)
distinguishes awake / drowsy / sleep / artifact axes; this logger supplies the
**concurrent activity context** so EEG features (LZ76, engagement,
drowsy_index) can be aligned with what the user was actually doing.

## NO-API constraint (raw#13 ai-config-ban)
The logger consumes **system events only**. No remote API call, no Claude/LLM
inference. The "AI" component is the offline correlation analysis run later;
this T2 file is system-self logging (raw#13 explicit carve-out).

User consent: this file documents the schema, scope, and privacy invariants
that the user MUST agree to before launchd plist is loaded. The plist is
**user-explicit-load only** (matches `com.anima.weight_precache_monitor`
pattern); the agent never auto-loads.

## Data captured (5 features, all coarsened)

| # | Feature | Method (macOS native) | Granularity | Privacy |
|---|---------|------------------------|-------------|---------|
| 1 | `keystroke_active_5s` | `ioreg -c IOHIDSystem` HIDIdleTime → boolean (idle < 5s ⇒ active) | 5 s flag | NO content captured |
| 2 | `screen_locked` | `pmset -g log` last `Display is turned off`/`turned on` event | 5 s flag | NO screen capture |
| 3 | `active_app` | `osascript -e 'tell application "System Events" to get name of first process whose frontmost is true'` | 5 s polling | App **name** only, no window title, no URL |
| 4 | `audio_level_db` | `system_profiler SPAudioDataType` for input device + a /tmp helper that reads RMS from `sox -t coreaudio default` 0.1 s sample → dB SPL approximation | 5 s mean | NO audio content saved |
| 5 | `network_active` | `netstat -ib` Δbytes / 5 s window > threshold (1 KB) | 5 s boolean | NO host / port / payload |

**Output schema** (raw#77 — JSONL, one row per 5 s window):
```json
{
  "ts": "2026-04-28T13:42:05Z",
  "active_app": "Terminal",
  "keystroke_active_5s": 1,
  "screen_locked": 0,
  "audio_level_db": -42,
  "network_active": 1,
  "schema": "anima/daily_life_context/1"
}
```

Stored at: `/Users/ghost/core/anima/state/daily_life_context/<UTC-date>_activity.jsonl`
(file rotates daily). Append-only, idempotent (raw#65) — duplicate ts rows
are no-ops at load time.

## Privacy invariants (raw#13 reinforced)
- I1 NEVER store keystroke characters / scancodes — only an active boolean.
- I2 NEVER capture screen pixels.
- I3 NEVER record audio buffer / waveform — only an integer dB level.
- I4 NEVER log URLs, hostnames, or destination IPs — only Δbytes boolean.
- I5 NEVER record window titles — `active_app` is process name only.
- I6 Output JSONL is `chflags uchg` after first daily rotation (raw#22).

## EEG time-align procedure
1. EEG recorder writes `recording_start_ts` to its session manifest.
2. Context logger writes `ts` for each 5 s row.
3. Offline aligner finds ≥ N overlapping 5 s windows; emits a joined CSV
   `<ts, eeg_lz76_b, eeg_engagement, eeg_drowsy_idx, active_app,
   keystroke_active_5s, screen_locked, audio_level_db, network_active>`.
4. Correlation table reports e.g.
   `corr(eeg_engagement, keystroke_active_5s)` over the daily-life session.

## Implementation plan
- `anima-eeg/tool/daily_life_context_logger.hexa` — orchestration, arg parsing,
  selftest synthetic events, falsifier list. ~120 LoC.
- `/tmp/daily_life_context_helper.py` — written-on-each-run /tmp helper
  (raw#37 transient). Polls macOS once per invocation, prints one JSONL row.
  The hexa tool calls the helper in a 5 s loop OR the launchd plist invokes
  the hexa tool every 5 s (StartInterval=5).
- `config/launchd/com.anima.daily_life_context_logger.plist` — user-explicit
  load. NEVER auto-loaded.

## Falsifiers (raw#71, ≥ 5 — privacy is part of the test)
- F1 Helper output JSON contains the literal substring `keystroke_chars` or
  any character that would represent a key — must be ABSENT.
- F2 Helper output JSON contains a window-title field — must be ABSENT.
- F3 Helper output JSON contains an audio waveform / `pcm_` field — must be
  ABSENT.
- F4 Helper output JSON contains a URL / `host` / `dst_ip` field — must be
  ABSENT.
- F5 Synthetic input "all-idle" produces `keystroke_active_5s=0`,
  `network_active=0`, `audio_level_db <= -60`.
- F6 Synthetic input "active-typing" produces `keystroke_active_5s=1` AND
  `audio_level_db > -60` AND active_app non-empty.
- F7 Two consecutive selftest invocations with same seed produce identical
  rows (idempotent, raw#65).

## RAW compliance
raw#9 hexa-only · raw#10 honest C3 · raw#13 ai-config-ban (system-self only) ·
raw#22 uchg ledger · raw#37 transient /tmp helper · raw#65 idempotent ·
raw#71 ≥ 5 falsifiers (incl. privacy) · raw#77 schema-stable JSONL ·
raw#82 darwin-native · raw#91 honesty triad · own 5 (genus + frameworks +
falsifiers + counter-example + privacy)
