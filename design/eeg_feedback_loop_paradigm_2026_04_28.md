# anima-eeg B8 Feedback Loop Paradigm — Design

**Date**: 2026-04-28
**Author**: anima-eeg / design (B8 closed-loop feedback)
**Status**: NEW_PARADIGM_DISCOVERY (orthogonal to raw#12 frozen LZ76; raw#12 untouched)
**Trigger**: B8 — EEG-driven real-time engagement / drowsiness monitor with macOS native notification.
**Companion docs**:
  - `design/eeg_daily_life_paradigm_design_2026_04_28.md` (6-axis daily-life verifier)
  - `anima-eeg/tool/eeg_daily_life_verifier.hexa` (sister tool, batch-mode verdict)
**Compliance**: raw#9 (pure-hexa, .py /tmp helper), raw#10 (honest), raw#12 (frozen criteria, no post-hoc tune), raw#37 (transient helper /tmp), raw#65 (deterministic seed selftest), raw#71 (≥5 falsifiers), raw#82 (darwin-native), raw#91 (honesty triad), own#5 (compositional re-use).

---

## 0. Executive Summary

### Problem
- `eeg_daily_life_verifier.hexa` is **batch-mode**: emits a single PASS/FAIL verdict over a recording.
- For closed-loop self-modulation the user needs **real-time feedback** — when the user is drifting drowsy / disengaged / hyper, alert immediately so they can self-correct.
- raw#12 daily-life criteria already define the metrics (engagement = beta/(alpha+theta), drowsiness = (theta+alpha)/beta). What is missing is a **continuous monitoring daemon** with a **native notification surface**.

### Solution
A continuous-monitoring daemon (`eeg_feedback_loop.hexa`) that
1. streams EEG via BrainFlow (cyton_daisy) on a 30s sliding window,
2. computes Pope 1995 engagement index and Pollock 1990 drowsiness index per window,
3. compares against three pre-frozen thresholds (drowsy / disengaged / hyperactive),
4. emits a native macOS notification (`osascript display notification`) when a threshold is crossed,
5. respects a 5-minute per-class cooldown so the user isn't bombarded,
6. appends an audit row to `state/eeg_feedback_audit/<date>_feedback.jsonl` for every window.

### Frozen Thresholds (raw#12 — pre-registered, no post-hoc tuning)
| Class | Index | Comparison | Threshold (x1000) | Notification title | Body (KR) |
|---|---|---|---|---|---|
| Drowsy | drowsiness = (theta+alpha)/beta | `>` | 2500 | "anima EEG" | "휴식 권고 (drowsy)" |
| Disengaged | engagement = beta/(alpha+theta) | `<` | 500 | "anima EEG" | "집중 알림 (disengaged)" |
| Hyperactive | engagement | `>` | 3000 | "anima EEG" | "과로 주의 (hyper)" |

Cooldown: **300 s (5 min)** per class — independent counters per class.
Window: **30 s sliding** with **15 s stride** (i.e., one decision every 15 s).

ANY post-hoc edit ⇒ v2 bump. raw#12 discipline.

---

## 1. Sister-Tool Differential

| | `eeg_daily_life_verifier` (batch) | `eeg_feedback_loop` (this) |
|---|---|---|
| Mode | one-shot 6-criterion verdict | continuous sliding-window |
| Output | JSON cert + verdict | macOS notifications + JSONL audit |
| Window | 60 s × 9 windows then verdict | 30 s rolling, decision every 15 s |
| Indices used | 6 (entropy, α-atten, change-pts, range, β/α, drowsy) | 2 (engagement, drowsy) |
| Action | exit code | side-effect: notification |
| User loop | "did this session pass?" | "how am I doing right now?" |

The two tools are **orthogonal** and **non-overlapping**: batch verifier validates a recorded session; feedback daemon shapes behavior in vivo.

---

## 2. Indices — Frozen Definitions

Pope et al 1995 (engagement):
```
E = β / (α + θ)
```
where α, θ, β are mean band-power across all 16 electrodes (cyton_daisy F7..O2).

Pollock 1990 (drowsiness):
```
D = (θ + α) / β
```
Note: D = 1/E + (α-cancel) → not strictly inverse, but strongly anti-correlated. We freeze BOTH so that "high D" and "low E" are double-witnessed before alerting.

Bands: θ 4-8 Hz, α 8-13 Hz, β 13-30 Hz. Window = 30 s sliding. Stride = 15 s.

---

## 3. Pre-Registered Falsifiers (raw#71, ≥5)

| # | Falsifier | Expected outcome |
|---|---|---|
| F1 | Synthetic awake state (mode=awake) → engagement ≈ 1.5, drowsy ≈ 0.8 | NO notification fires |
| F2 | Synthetic drowsy state → drowsy > 2.5, engagement < 0.7 | "휴식 권고" fires exactly once |
| F3 | Synthetic disengaged state → engagement < 0.5, drowsy moderate | "집중 알림" fires exactly once |
| F4 | Synthetic hyperactive → engagement > 3.0 | "과로 주의" fires exactly once |
| F5 | Same drowsy state held for 6 minutes → second alert ONLY after 300 s cooldown | exactly 2 notifications, never 6+ |
| F6 | Three classes alternated in one tick → independent cooldowns: each fires once, not blocked by prior class | 3 notifications back-to-back OK |

raw#71 ≥5 satisfied (F1-F6 = 6 falsifiers).

---

## 4. Architecture

```
┌────────────────────────────────────┐
│ eeg_feedback_loop.hexa (daemon)    │
│  ─── parses --selftest / --live    │
│  ─── writes /tmp helper py         │
│  ─── exec_with_status spawns py    │
│  ─── ingests stdout JSONL stream   │
│  ─── for each row:                 │
│        compute E, D                │
│        check 3 thresholds          │
│        check cooldown              │
│        if fire → osascript         │
│        append audit JSONL          │
└──────┬─────────────────────────────┘
       │ stdout JSONL { ts, theta, alpha, beta, idx_engage, idx_drowsy }
       ▼
┌────────────────────────────────────┐
│ /tmp/eeg_feedback_helper.py        │
│  BrainFlow cyton_daisy stream OR   │
│  synthetic 4-state generator       │
│  → 30s sliding, 15s stride         │
│  → bandpower θ α β                 │
│  → emit JSONL row each stride      │
└────────────────────────────────────┘
```

### Selftest 4-state schedule (deterministic, raw#65)
- t∈[0,15s)   awake state — neither index over threshold → 0 notifications
- t∈[15,30s)  drowsy → 1 "휴식 권고"
- t∈[30,45s)  disengaged → 1 "집중 알림"
- t∈[45,60s)  hyperactive → 1 "과로 주의"
Total expected notifications: 3.

### Cooldown 검증 (F5)
Drowsy state stretched to 360 s in a separate selftest cell (`--selftest-cooldown`):
expected: notification at t=15s and t=315s only → exactly 2 fires.

---

## 5. Notification Surface (raw#82 darwin-native)

Primary: `osascript -e 'display notification "..." with title "anima EEG"'`
Fallback: `terminal-notifier -message "..." -title "anima EEG"` if installed (detected once at start).

Notification text uses Korean per user preference (raw#9 user-locale). All notifications carry the title `"anima EEG"` so the user can mute the channel via macOS Notification Center if desired.

---

## 6. Audit Ledger (raw#91 honesty-triad)

Path: `state/eeg_feedback_audit/<YYYY-MM-DD>_feedback.jsonl`
Row schema (one per stride decision):
```json
{
  "ts": "2026-04-28T19:42:11Z",
  "engagement_x1000": 1500,
  "drowsy_x1000": 800,
  "fired": null | "drowsy" | "disengaged" | "hyper",
  "cooldown_ms_remaining": {"drowsy": 0, "disengaged": 285000, "hyper": 0},
  "selftest_mode": "awake|drowsy|disengaged|hyper|live"
}
```

Selftest emits exactly the same rows so the user can grep the audit for `"fired":"drowsy"` and confirm count = 1.

---

## 7. User Action Plan

1. Wear cyton_daisy helmet, dongle into USB.
2. Run impedance check first: `hexa run anima-eeg/impedance_check.hexa --check`
3. Once GREEN ≥ 12/16 channels, start daemon: `hexa run anima-eeg/tool/eeg_feedback_loop.hexa --live`
4. Continue normal work. Daemon will surface a macOS notification when the user drifts drowsy / disengaged / hyper.
5. Stop daemon with Ctrl-C.
6. Review audit: `tail state/eeg_feedback_audit/$(date +%F)_feedback.jsonl`

For pre-flight without hardware: `hexa run anima-eeg/tool/eeg_feedback_loop.hexa --selftest`

---

## 8. raw-Compliance Check (raw#117 5-check)

- **Genus** (raw#106): `eeg-realtime-feedback-notification-loop` (NOT a v1 / impl suffix)
- **Frameworks ≥2**: Pope 1995 (engagement), Pollock 1990 (drowsiness), Klimesch 1999 (alpha bandpower), darwin Notification Center (UI substrate)
- **Channels ≥3**: cyton_daisy 16ch — uses ALL 16 averaged
- **Counter-example**: synthetic awake state (F1) — must NOT fire
- **Falsifiers ≥3**: F1-F6 (6 falsifiers, raw#71 ≥5 satisfied)

5-check ✓.

---

## 9. own#5 Reuse

- LZ76 / band-power machinery: re-uses `clm_eeg_lz76_real.hexa` Python helper conventions (raw#9 .py /tmp).
- BrainFlow board init: re-uses `electrode_helper_rich.hexa` `_board_name_to_id` and `.venv-eeg/bin/python` paths.
- Selftest scaffolding: forked from `eeg_daily_life_verifier.hexa` (deterministic FNV seed, mode dispatch, raw#65).
- Audit ledger pattern: forked from `impedance_check.hexa` `_emit_ledger` (read-then-rewrite append).

Net new code (excluding /tmp helper python): ~150 LoC daemon.

---
