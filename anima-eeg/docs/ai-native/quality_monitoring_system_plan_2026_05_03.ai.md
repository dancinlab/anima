# anima-eeg AI Quality Monitoring System — Design Plan

**Date**: 2026-05-03
**Author**: anima cycle (design only, no code touch)
**Scope**: design plan doc only — 실 hexa land 측 다음 cycle
**Status**: cycle 1 (plan) — cycles 2-5 측 implementation roadmap 포함

---

## 1. Motivation

이번 anima-eeg cycle 측 측정 quality issues:

| Issue | Detection | Severity |
|---|---|---|
| Sample rate drop (60-7Hz vs claim 125Hz) | runtime ts diff | HIGH |
| DC settle 5s transient (-39k → -78k µV) | start-of-session amp | MED |
| Fp1 chronic noise (76+ peaks REST) | per-channel std | HIGH |
| F_BLINK falsifier 1/3 PASS only | post-measurement | HIGH |
| 모든 fix sequence 사용자 직접 수행 | (no automation) | OPS |

→ AI 측 자동화 monitoring + pattern learning + 점진 개선 측 필요.

---

## 2. Architecture

```
┌──────────────────────────────────────────────────────────────────────┐
│                  AI Quality Monitoring Loop                           │
└──────────────────────────────────────────────────────────────────────┘

   ┌─────────────┐     ┌──────────────┐     ┌────────────────┐
   │ measurement │────▶│ quality_audit│────▶│ quality_ledger │
   │   (.npy)    │     │   (module 1) │     │   (module 2)   │
   └─────────────┘     └──────────────┘     └────────────────┘
          ▲                                          │
          │                                          ▼
          │            ┌─────────────────┐  ┌────────────────┐
          │            │ quality_advisor │◀─│ pattern_learn  │
          │            │   (module 3)    │  │  (time-series) │
          │            └─────────────────┘  └────────────────┘
          │                     │
          │                     ▼
          │            ┌─────────────────┐
          │            │ quality_dashboard│
          │            │   (module 4)    │
          │            └─────────────────┘
          │                     │
          └─────── auto_apply_fix / user_guidance ──┘

Data flow:
  .npy + meta.json → audit (metrics) → JSONL ledger (append-only)
                  → advisor (pattern detect + fix recommend)
                  → dashboard (terminal trend chart)
                  → next_measurement (auto-fix or user prompt)
```

각 측정 후 자동 audit, ledger append, advisor 측 패턴 진단, dashboard 측 trend 시각화, 다음 measurement 측 사전 advice.

---

## 3. Module Spec Table

| # | Module | Path | LoC est | Role | Falsifier |
|---|---|---|---|---|---|
| 1 | quality_audit | `anima-eeg/core/quality_audit.hexa` | ~400 | post-measurement metric extraction | F_AUDIT_01: metrics non-null on synthetic .npy; F_AUDIT_02: drift>50k µV detected on synthetic transient |
| 2 | quality_ledger | `anima-eeg/core/quality_ledger.hexa` | ~300 | append-only JSONL time-series, query API | F_LEDGER_01: append idempotent (same ts+session not duplicated); F_LEDGER_02: get_recent(N) returns N most recent rows |
| 3 | quality_advisor | `anima-eeg/core/quality_advisor.hexa` | ~500 | pattern detect + fix recommend (rule-based + 옵션 LLM) | F_ADVISOR_01: 3-consecutive-low-fs sessions trigger "sample_drop_chronic" verdict; F_ADVISOR_02: per-channel chronic noise → channel-specific fix emit |
| 4 | quality_dashboard | `anima-eeg/core/quality_dashboard.hexa` | ~300 | terminal ASCII trend chart | F_DASH_01: dashboard renders with N=0 ledger (empty state OK); F_DASH_02: chart axes + labels present |
| **Total** | | | **~1500 LoC** | | |

---

## 4. JSONL Ledger Schema

**Path**: `anima-eeg/state/quality_ledger/<YYYY-MM>.jsonl` (monthly rotation)

**Row schema**:
```json
{
  "ts": "2026-05-03T19:00:00Z",
  "session_id": "blink_session_90s_2026_05_03",
  "paradigm": "blink",
  "duration_s": 92.33,
  "duration_claimed_s": 90.0,
  "effective_fs_hz": 60.49,
  "fs_claimed_hz": 125.0,
  "sample_drop_pct": 51.6,
  "dc_drift_max_uv": 78000,
  "dc_settle_5s_max_uv": 78000,
  "per_channel_noise": {
    "Fp1": {"rest_std": 145.2, "active_std": 180.4, "rest_active_ratio": 0.81},
    "Fp2": {"rest_std": 22.1, "active_std": 65.3, "rest_active_ratio": 0.34},
    "C3":  {"rest_std": 18.7, "active_std": 21.0, "rest_active_ratio": 0.89},
    "C4":  {"rest_std": 19.4, "active_std": 22.5, "rest_active_ratio": 0.86}
  },
  "line_noise_60hz_db": 0.5,
  "rail_flat_count": 0,
  "falsifier_verdict": {
    "F_BLINK_01": "PASS",
    "F_BLINK_02": "FAIL",
    "F_BLINK_03": "FAIL"
  },
  "issues_detected": [
    "sample_rate_drop",
    "dc_settle_transient",
    "fp1_chronic_noise"
  ],
  "advice_emitted": [
    "electrode_paste_replenish",
    "fp1_re_attach",
    "preflight_extend_to_30s"
  ]
}
```

**Query API**:
- `get_recent(N: int) -> List[Row]`
- `get_by_paradigm(paradigm: str, since_days: int) -> List[Row]`
- `get_trend(metric: str, window: int) -> List[(ts, value)]`

---

## 5. Fix Mapping (Rule-Based)

| Issue | Detection threshold | Fix recommendation | Auto-apply |
|---|---|---|---|
| sample_rate_drop | effective_fs < 100Hz | collect.hexa polling fix; throttle log | YES (cycle 4+) |
| dc_settle_transient | first 5s max\|amp\| > 50k µV | trim first 10s OR extend preflight to 30s | YES (trim) |
| fp1_chronic_noise | rest_std > 100 (3+ sessions) | re-attach Fp1; paste replenish; check skin prep | NO (manual) |
| line_noise_60hz | 60Hz peak > 5dB above baseline | unplug nearby AC devices; check ground | NO (manual) |
| rail_flat | rail_flat_detector hits | electrode contact lost; pause + re-attach | NO (manual) |
| falsifier_F_BLINK_02 | blink amp ratio fail | pre-blink baseline noise check; instruct stronger blink | partial (advice only) |
| falsifier_F_REST_01 | REST eyes-closed alpha absent | check occipital electrode contact; eyes-closed verify | NO (manual) |
| dc_drift_chronic | max\|amp\| > 50k µV, 5+ sessions | electrode contact 약함; full paste refresh | NO (manual) |

---

## 6. AI 학습 Plan

3-tier approach:

| Tier | Method | Data req | Honest C3 |
|---|---|---|---|
| Tier 1 (rule-based) | hard-coded thresholds (table 5) | N=1 OK | always available; no learning |
| Tier 2 (LLM advisor, 옵션) | Claude API: ledger history + current row → text recommendation | N=1 OK | vendor self-claim; non-deterministic; cost |
| Tier 3 (lightweight ML, future) | sklearn LogisticRegression: setup features → PASS/FAIL prob | N≥30 sessions | N=1 self-experiment 측 데이터 부족; overfit risk |

**Tier 1 (cycle 3 land)**: rule-based pattern detection. e.g.:
- last 3 sessions all `effective_fs < 100Hz` → emit `"sample_drop_chronic"`
- DC drift > 50k µV in 5+ sessions → emit `"electrode_contact_weak"`
- single channel `rest_std > 100` for 3+ sessions → emit `"channel_specific_fix"`

**Tier 2 (cycle 5+ 옵션)**: Claude API call. Prompt template:
```
You are an EEG quality advisor. Recent 10 ledger rows:
<ledger_json>
Current measurement audit:
<current_audit_json>
Identified issues:
<issues_list>
Recommend fix steps in priority order. Output JSON: {"fix_steps": [...]}.
```

**Tier 3 (cycle 6+ future)**: feature extraction (preflight verdict, impedance, recent fix applied) → outcome (PASS/FAIL falsifier verdict) regression. Limit: N=1 self-experiment, cross-subject generalization X.

---

## 7. Integration Hook Plan

**Pre-measurement** (master_preflight extension):
```
master_preflight()
  → load_recent_ledger(N=5)
  → quality_advisor.pre_session_advice(recent)
  → print to terminal: "Recent issues: sample_drop_chronic. Suggested fix: ..."
  → user ack required
  → proceed_with_measurement()
```

**Post-measurement** (every protocol):
```
record_session(paradigm, duration)
  → save .npy + meta.json
  → quality_audit.run(.npy, meta) → audit_result
  → quality_ledger.append(audit_result)
  → quality_advisor.post_session_check(audit_result, ledger_history)
  → if auto_apply_fix_enabled: apply fix to next measurement config
  → print summary
```

**On-demand** (CLI command):
```
hexa run anima-eeg/core/quality_dashboard.hexa --window 30
  → render ASCII trend chart of last 30 sessions
  → metrics: effective_fs, dc_drift_max, F1 score, falsifier PASS rate
```

---

## 8. 5-Cycle Implementation Roadmap

| Cycle | Deliverable | Falsifier gate |
|---|---|---|
| 1 (이번) | this design plan doc | doc lands; structure review |
| 2 | quality_audit + quality_ledger module | F_AUDIT_01/02 + F_LEDGER_01/02 PASS |
| 3 | quality_advisor module (rule-based Tier 1) | F_ADVISOR_01/02 PASS on synthetic ledger |
| 4 | quality_dashboard + measurement hook 통합 | F_DASH_01/02 PASS; integration smoke test |
| 5+ | LLM advisor (Tier 2) 옵션 + ML learning prep | LLM advisor produces consistent JSON; ML data pipeline draft |

**Goal**: N=10 sessions 후 first-time PASS rate ≥80% (현재 1/3 = 33%).

---

## 9. Honest C3 Caveats

1. **N=1 self-experiment 측 ML 학습 데이터 부족**: Tier 3 ML advisor 측 cross-subject generalization 측 X; single-subject overfit risk; cycle 6+ 측 minimum N=30 sessions 후 측 시작 가능.

2. **LLM advisor 측 vendor self-claim**: Claude API 측 EEG quality advice 측 medical-grade certified X; non-deterministic output; cost per call; falsifier 측 LLM output 측 schema-conformance 측 만 검증, 실 fix 효과 검증 X.

3. **모든 issue 측 자동 fix X**: paste 보충, electrode 재부착, skin prep 측 manual user action 필수; 자동 fix 측 software-side parameter (sample rate polling, DC trim, line filter) 측 만 적용; rail/flat/chronic noise 측 user 손 작업 측 unavoidable.

---

## 10. 다음 Cycle 권장 1순위 Module

**1순위: quality_audit + quality_ledger (cycle 2 묶음 land)**

근거:
- audit + ledger 측 advisor/dashboard 측 prerequisite (없으면 진단 불가)
- 두 module 측 ~700 LoC, 단일 cycle 측 land 가능
- 즉시 가치: 첫 land 후 모든 measurement 측 metric capture 시작 → cycle 3 측 advisor 측 충분한 ledger 데이터 보유
- falsifier 측 명확 (synthetic .npy 측 metric 추출 + JSONL append idempotency)
- 사용자 측 즉시 benefit: terminal 측 audit summary 측 print → 현 cycle issues (sample drop, DC settle, Fp1) 측 자동 surface

**2순위: quality_advisor Tier 1 (cycle 3)** — rule-based, N=1 OK
**3순위: quality_dashboard + 통합 (cycle 4)** — UX 개선
**보류**: LLM (Tier 2), ML (Tier 3) — 데이터 + 검증 측 추가 cycles 후

---

## 11. 범위 + raw 준수

- raw#9 hexa-only: 본 doc 측 markdown design plan; 실 hexa code 측 cycle 2+ land
- raw#10 honest C3: 3 caveats 명시 (§9)
- raw#15 personal paths X: 모든 path `anima-eeg/...` relative
- raw#65 idempotent: ledger append-only, ts+session_id 측 dedup key
- raw#71 falsifier-bound: 4 module 측 각 falsifier 명시 (§3)
- write 범위: 본 doc 신규 only; 코드 touch X

---

**End of design plan. Cycle 2 entry: quality_audit + quality_ledger module land.**
