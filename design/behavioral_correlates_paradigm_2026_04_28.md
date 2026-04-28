# Behavioral Correlates Paradigm — Design Doc (2026-04-28)

## Purpose (B11)
Provide **continuous behavioral metrics** (typing rate, mouse velocity, scroll
rate, app-switching rate, idle time) from macOS native polling so that EEG
features (Engagement Index, Drowsy Index, LZ76) can be correlated against a
real-time **cognitive load / mental fatigue** index.

## Differentiation from T2 (daily_life_context_labeling)
| Axis | T2 | B11 |
|------|----|----|
| Granularity | discrete labels (active_app, audio level) | continuous metrics |
| Window | 5 s flag/poll | 5-min sliding window aggregates |
| Signal type | categorical (app name) + boolean | rate / velocity (numeric) |
| EEG join | label-conditional means | continuous Pearson r |

T2 = "what app are you in?" · B11 = "how hard are you working?"

## NO-API constraint (raw#13)
Identical to T2: macOS native polling only via `/tmp/behavioral_helper.py`
(raw#37 transient). NO Claude / LLM / remote inference. User must explicitly
load the launchd plist; the agent never auto-loads.

## Five behavioral metrics (5-min sliding window)

| # | Metric | Method (macOS native, no content) | Privacy invariant |
|---|--------|-----------------------------------|-------------------|
| 1 | `keystroke_rate_per_min` | `ioreg -c IOHIDSystem` HIDIdleTime → derive 1-Hz active flag → integrate over 5 min, multiply by typical 4 keys/active-second baseline OR (preferred) use `log show --predicate 'subsystem == "com.apple.HID"'` event counts | NO key codes / characters / scancodes |
| 2 | `mouse_velocity_avg_px_per_sec` | poll `cliclick p` (or AppleScript "the mouse position") at 1 Hz; compute Δposition / Δt; average over window — emit only the magnitude | NO absolute positions stored |
| 3 | `scroll_events_per_min` | `log show --predicate 'eventMessage contains "scroll"'` (subsystem `com.apple.HID`, last 60 s) | NO scroll content / direction |
| 4 | `app_switch_rate_per_min` | sample frontmost app every 5 s via `osascript`; count distinct transitions over 5-min window | NO window titles, name only |
| 5 | `idle_time_sec_in_window` | sum of seconds where HIDIdleTime ≥ 30 s within the 5-min window | derived only |

**Cognitive load index** (deterministic formula, x1000 fixed-point):
```
load_x1000 = clamp(0, 1000,
    400 * normalized_keystroke_rate          // focused work
  - 200 * normalized_app_switch_rate         // distraction penalty
  - 200 * normalized_idle_fraction           // fatigue penalty
  + 600 )                                    // baseline
```
- High load (≥700): focused work (high keystroke + low switching + low idle)
- Low load (≤300): browsing / distraction
- Mental fatigue signature: load_x1000 monotone-decreasing across consecutive
  windows AND idle fraction monotone-increasing.

## EEG correlation hypotheses (frozen, raw#12)
- H1 `engagement_index ↔ load_x1000` Pearson r ≥ +0.30
- H2 `drowsy_index ↔ idle_time_sec` Pearson r ≥ +0.30
- H3 `lz76_b ↔ activity diversity` (entropy of app set) Pearson r ≥ +0.20
- Frozen criteria (raw#12): N ≥ 1 week of paired EEG+behavior; **r ≥ 0.30**
  is the minimum meaningful correlation. r < 0.10 cumulative ⇒ relationship
  not present (F4 falsifier).

## Output schema (raw#77 — JSONL, one row per 5-min window)
```json
{
  "ts": "2026-04-28T13:42:05Z",
  "keystroke_rate_per_min": 42,
  "mouse_velocity_avg_px_per_sec": 180,
  "scroll_events_per_min": 7,
  "app_switch_rate_per_min": 2,
  "idle_time_sec": 35,
  "load_x1000": 720,
  "schema": "anima/behavioral_correlates/1"
}
```
Stored at: `state/behavioral_correlates_audit/<UTC-date>_behavior.jsonl`
(file rotates daily, append-only, idempotent).

## Privacy invariants (raw#13 reinforced — falsifiable)
- I1 NEVER store key codes / characters / scancodes
- I2 NEVER store absolute mouse positions (only avg velocity magnitude)
- I3 NEVER store scroll direction / content
- I4 NEVER store window titles or URLs
- I5 NEVER record device input content (external keyboard/trackpad still
  produce only aggregate counts)
- I6 Output JSONL is `chflags uchg` after first daily rotation (raw#22)

## EEG time-align procedure
1. EEG recorder emits LZ76 b(t), engagement, drowsy_idx per 5-min window.
2. Behavioral logger emits load_x1000, idle_time_sec, app_switch_rate per
   5-min window.
3. Offline aligner joins on `ts` (5-min bucket) over ≥ N=1 week (≥ 2016
   windows) and reports Pearson r per H1/H2/H3.

## Falsifiers (raw#71, ≥ 5 — privacy is part of the test)
- F1 keystroke_rate_per_min == 0 across active_typing selftest ⇒ logger
  broken (must be > 0 in active_typing mode).
- F2 helper output JSON contains literal substring `keystroke_chars` /
  `key_code` / `mouse_x` / `mouse_y` / `window_title` / `url` — must be
  ABSENT (privacy leak).
- F3 selftest synthetic EEG-behavior pair with mismatched timestamps
  (Δts > 30 s) ⇒ aligner must reject (no false-positive correlation).
- F4 cumulative Pearson r < 0.10 over a synthetic random-pair stream of
  N ≥ 100 windows ⇒ must classify as `RELATIONSHIP_ABSENT`.
- F5 external-device input absent (synthetic "trackpad-only-no-keyboard"
  mode) ⇒ keystroke_rate_per_min still computable (HID-level catches
  external keyboards via the same IOHIDSystem path); test asserts
  keystroke_rate_per_min ≥ 0 (not -1 / not error).
- F6 idempotent (raw#65): same seed+mode → identical row.
- F7 mental-fatigue signature: synthetic monotone-decreasing keystroke
  series ⇒ load_x1000 monotone non-increasing across windows.

## Implementation plan
- `anima-eeg/tool/behavioral_correlates_logger.hexa` — orchestration, arg
  parsing, selftest synthetic windows, falsifier list. ~150 LoC.
- `/tmp/behavioral_helper.py` — written-on-each-run /tmp helper (raw#37
  transient). Polls macOS once per invocation, prints one JSONL window row.
- Aggregation cadence: launchd plist with `StartInterval=300` (5 min) — but
  user-explicit-load only. NEVER auto-loaded.

## RAW compliance
raw#9 hexa-only · raw#10 honest C3 · raw#12 pre-registered (5-min window,
N≥1 week, r≥0.30 frozen) · raw#13 ai-config-ban (system-self only) ·
raw#22 uchg ledger · raw#37 transient /tmp helper · raw#65 idempotent ·
raw#71 ≥ 5 falsifiers (incl. privacy) · raw#77 schema-stable JSONL ·
raw#82 darwin-native · raw#91 honesty triad · own 5 (genus + frameworks
2+ + falsifiers 5+ + counter-example + privacy)

## Genus (raw#106)
`behavioral-correlates-cognitive-load-logger`

## Frameworks (own-5 ≥ 2)
- Mark 2008 (workplace interruption / multitasking, `app_switch_rate`)
- Iqbal 2007 (mental workload via interaction patterns)
- Pope 1995 (engagement index, EEG ↔ behavior bridge)
- Larson 1983 ESM (Experience Sampling, ground-truth labeling)

## Counter-example (raw#52 negative oracle)
Sleep / unattended idle session: keystroke_rate_per_min ≈ 0,
mouse_velocity ≈ 0, scroll_events ≈ 0, app_switch_rate ≈ 0, idle_time_sec
≈ 300 ⇒ load_x1000 ≈ 100 (floor). EEG drowsy_idx must spike here; if EEG
drowsy_idx remains low while behavior says fully idle, the EEG montage is
suspect, not the behavior logger.
