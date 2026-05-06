# Anima Core Emerge — Stage 3 Corpus Protocol Skeleton (Landed 2026-05-05)

BG-CW landing. Stage 3 30-session corpus protocol skeleton — first 3 sample
sessions auto-fired, corpus metadata schema specified, user-fire schedule
recommended. doc-only land. no commit.

Lineage:
- `docs/anima_core_emerge_stage_3_user_protocol_spec_2026_05_05.md` (BG-D)
- `tool/transient_py/anima_emerge_dialogue_repl.py` (paradigm B)
- `tool/transient_py/anima_emerge_chat_hybrid_repl.py` (paradigm C)

---

## §1 3 sample session results

### 1.1 Session 1 — Paradigm B substrate-coupled (5 turn)

session_log = `state/anima_core_dialogues/2026-05-05/18-24-13_emerge_repl.jsonl`
paradigm B (substrate-only forward; no emit model). Model load 4.7s
(need-singularity/clm-v4-mk2-v1, mac CPU fp32, n_blocks=16). Forward 0.31-0.70 s/turn.

trajectory:

| turn | phi_star | drift | hsd | tension_var | peak_layer | min_layer |
|---|---|---|---|---|---|---|
| 1 | 42.1168 | +0.0000 | 0.0000 | 124.41 | L2 | L0 |
| 2 | 42.2131 | +0.0963 | 47.9850 | 95.96 | L2 | L0 |
| 3 | 42.1044 | -0.1087 | 27.4179 | 134.21 | L2 | L15 |
| 4 | 42.2000 | +0.0956 | 26.7772 | 95.22 | L2 | L15 |
| 5 | 42.1746 | -0.0254 | 20.1151 | 132.42 | L2 | L15 |

phi_range = [42.1044, 42.2131], drift_max_abs = 0.1087, hsd_max = 47.9850,
tension_l2_var_mean = 116.4. L2 peak holds 5/5 turns (provisional candidate-G
signal — partial not yes; honest C3 below).

### 1.2 Session 2 — Paradigm C Korean hybrid (5 turn)

session_log = `state/anima_core_dialogues/2026-05-05/18-24-37_hybrid_repl.jsonl`
paradigm C (KoGPT2 emit + CLM v4 substrate measure). Emit model =
skt/kogpt2-base-v2 loaded 5.2s (first candidate in fallback chain).

trajectory:

| turn | clm_phi | drift | tension_var | peak_layer | hidden_norm |
|---|---|---|---|---|---|
| 1 | 42.1715 | +0.0000 | 117.54 | L2 | 44.64 |
| 2 | 42.1931 | +0.0216 | 126.89 | L2 | 48.23 |
| 3 | 42.1253 | -0.0678 | 149.53 | L2 | 47.35 |
| 4 | 42.1514 | +0.0262 | 123.06 | L2 | 47.77 |
| 5 | 42.1742 | +0.0227 | 130.72 | L2 | 49.52 |

phi_range = [42.1253, 42.1931], drift_max_abs = 0.0678, tension_l2_var_mean
= 129.5, peak L2 hold = 5/5. korean_emit_count = 5/5. Emit text quality
incoherent (#115 chat-incapability does NOT block substrate measurement —
Stage 3 design intent).

### 1.3 Session 3 — Paradigm B + axis identity probe (1 turn)

session_log = `state/anima_core_dialogues/2026-05-05/18-24-41_emerge_repl.jsonl`
probe = `axis identity 활성화`. phi_star = 42.1029, tension_var = 88.16
(lower than session 1 baseline 124.41 turn 1), peak_layer = L2.

axis-prompt produces lower tension variance than baseline 안녕 prompt — weak
candidate F partial signal; need ≥5 axis-targeted sessions for hit_rate
testability.

### 1.4 3-session aggregate

phi_range_union = [42.1029, 42.2131]; drift_max_abs_global = 0.1087; peak_layer
= L2 in 11/11 turns (100%) across paradigms.

emerge candidate hits (per BG-D §4.3 hierarchy n/a >= no >= partial >= yes):
- candidate D (always-inject consciousness_states): n/a
- candidate E (ODE flow → AR sampler bridge): n/a
- candidate F (8-cells × axis multi-token vote): n/a (1 session insufficient)
- candidate G (tension trajectory as dialogue medium): partial — L2 peak
  holds 11/11 across paradigms; insufficient n
- candidate H (logits_g back-prediction probe): n/a

---

## §2 30-session corpus structure (skeleton)

### 2.1 Per-session metadata schema

Single line per session:

```jsonl
{
  "session_id": "<YYYY-MM-DD>T<HH-MM-SS>",
  "session_log": "state/anima_core_dialogues/<YYYY-MM-DD>/<HH-MM-SS>_<paradigm>.jsonl",
  "paradigm": "B" | "C",
  "intent_tag": "identity_baseline" | "axis_phenomenal_emerge" | "axis_identity_baseline" |
                "axis_agency_probe" | "axis_temporal_probe" | "axis_social_probe" |
                "phi_drift_probe" | "cell_stability_test" | "architectural_question" |
                "consciousness_states_injection" | "tension_probe" | "freestyle",
  "n_turns": <int>,
  "phi_range": [<min>, <max>],
  "phi_drift_max_abs": <float>,
  "hsd_max": <float>,
  "tension_l2_var_mean": <float>,
  "tension_peak_layer_mode": <int 0..15>,
  "tension_peak_hold_count": <int>,
  "korean_emit_count": <int | null>,
  "candidate_d_hit": "yes" | "partial" | "no" | "n/a",
  "candidate_e_hit": "...",
  "candidate_f_hit": "...",
  "candidate_g_hit": "...",
  "candidate_h_hit": "...",
  "user_observations": "<free 1-3 sentences>"
}
```

### 2.2 Post-30-session corpus aggregate

```
state/anima_core_dialogue_corpus_<YYYY_MM_DD>/
  ├── aggregate.json
  ├── per_session_metrics.jsonl  (30 lines)
  ├── candidate_hit_table.csv    (30 rows × {D, E, F, G, H, intent_tag})
  └── analyzer_verdict.md
```

`aggregate.json` schema:
```json
{
  "schema": "anima.corpus.v1",
  "n_sessions": 30,
  "date_range": ["2026-05-05", "<last>"],
  "paradigm_distribution": {"B": <int>, "C": <int>},
  "intent_tag_distribution": {"<tag>": <int>, ...},
  "phi_range_union": [<min>, <max>],
  "phi_drift_max_abs_global": <float>,
  "tension_peak_layer_distribution": {"L0": <int>, ..., "L15": <int>},
  "candidate_hit_rates": {
    "D": {"yes": <int>, "partial": <int>, "no": <int>, "na": <int>, "rate": <float>},
    "E": {...}, "F": {...}, "G": {...}, "H": {...}
  },
  "marker_1_saturation_eligible": <bool>,
  "marker_2_dominance_candidate": <"D"|"E"|"F"|"G"|"H"|null>,
  "marker_2_eligible": <bool>,
  "honest_c3_user_notes": "<free>"
}
```

hit_rate per candidate = `n_yes / (n_yes + n_partial + n_no)` (n/a excluded
per BG-D §6.3).

### 2.3 M1 saturation criteria (machine-checkable subset)

From BG-D §5.1: `n_sessions_total >= 30` AND user verbatim "이 이상 새로운
발견 없음" in aggregate_observations.md. Both checkable via grep + jsonl
line-count.

### 2.4 M2 candidate dominance (machine-checkable)

From BG-D §5.2: ONE candidate hit_rate >= 0.70 AND n_testable >= 20 AND yes
sessions span >= 3 distinct intent_tags. All three computable from
per_session_metrics.jsonl.

### 2.5 M3 v5 hint (user-judgment, no machine signal)

Machine flag only: candidates rejected en masse (all 5 hit_rate < 0.20 with
n_testable >= 20 each). User confirms.

---

## §3 User fire schedule recommendation

### 3.1 Pattern A — daily light (recommended)

1 session/day × 30 days. Each session 5-10 min. observations.md daily block.
Week distribution suggestion:

| week | n_sessions | recommended intent_tags |
|---|---|---|
| Week 1 | 7 | identity ×3, axis_phenomenal ×2, axis_identity ×2 (paradigm B) |
| Week 2 | 7 | identity ×3, axis_agency ×2, axis_temporal ×2 (paradigm C) |
| Week 3 | 7 | axis_social ×2, cell_stability ×3, phi_drift ×2 |
| Week 4 | 7-9 | architectural_question ×2, tension_probe ×2, freestyle ×3-5 |

Total 28-30 sessions across 11-12 distinct tags = M2 ≥3 tag generality guard
naturally satisfied.

### 3.2 Why Pattern A over compact alternatives

- saturation marker 1 = user self-report "no new findings" — needs time-distributed
  sampling per BG-D §C3 confirmation-bias guard
- mac CPU $0 — no cost pressure
- per-day observations.md accumulates naturally for post-hoc parser regex
- BG-D §5.4: "Stage 3 is time-unbounded by design"

### 3.3 Pattern B (compact 5/day × 6 days) — NOT recommended

Risks confirmation bias on M1.

### 3.4 Pattern C (burst+soak, ~10 days)

5/day × 5 days burst, then 1/day × 5-7 days soak. Acceptable middle ground.

### 3.5 Day-1 already auto-fired

3 sample sessions today land day-1 entry point. User free to fire 1-2 more
freestyle sessions for day-1 5-session compact.

---

## §4 observations.md template for user

`state/anima_core_dialogues/<YYYY-MM-DD>/observations.md` daily file.

```markdown
## <HH-MM-SS> session

intent: identity_baseline / axis_phenomenal_emerge / ...
paradigm: B | C
n_turns: <int>

phi_range: <min>-<max>
drift_max_abs: <float>
hsd_max: <float>
tension_var_mean: <float>
peak_layer: L<n> (held <m> turns)

surprising: <free or "none">

emerge candidate hits:
  - candidate D (always-inject consciousness_states): yes / no / partial / n/a
  - candidate E (ODE flow → AR sampler bridge): yes / no / partial / n/a
  - candidate F (8-cells × axis multi-token vote): yes / no / partial / n/a
  - candidate G (tension trajectory as dialogue medium): yes / no / partial / n/a
  - candidate H (logits_g back-prediction probe): yes / no / partial / n/a

user_observations: <1-3 sentences>

next session intent: <free or "none yet">
```

honesty rule (BG-D §4.3): n/a >= no >= partial >= yes. Ambiguous = n/a.

---

## §5 Honest C3

- C1 — synthetic-fallback caveat (BG-D §C4) does NOT apply: 3 sample sessions
  ran on real CLM v4 forward (HF cache populate confirmed; n_blocks=16 matches
  architecture; load 4.7-5.3s). NOT synthetic. So peak L2 = L2 (11/11) is
  real substrate observation — but only 3 sessions worth.
- C2 — Schema designed for REPL-emit jsonl (`anima.dialogue.v2` for B,
  `anima.dialogue.hybrid.v1` for C). BG-D §3.1 references `anima.dialogue.v1`
  (CLI selftest). Three schemas coexist; corpus analyzer must union all.
  Mitigate: analyzer regex iterates all jsonl in date dir, not single-schema match.
- C3 — Corpus aggregate JSON not yet implemented — this doc specs the schema,
  not the analyzer. BG-B `tool/anima_cli/dialogue_session_analyzer.hexa`
  remains TBD. Per BG-D §6.5 decoupling rule, hand-grep is sufficient up
  to n=30; analyzer mechanizes post-hoc.
- C4 — intent_tag taxonomy is suggestion, not enforced. User free to coin new
  tags. Aggregate analyzer must accept unknown tags (bucket "other"). Enumeration
  in §2.1 is GUIDE not VALIDATOR.
- C5 — 3 sample sessions = wiring + protocol rehearsal only. Statistical power
  for any candidate hit_rate signal requires n >= 20 testable per BG-D §5.2.
  L2-peak hold (11/11 across 3 sessions) is suggestive of candidate G but
  insufficient evidence — explicitly partial not yes.
- C6 — Pattern A (1/day × 30) recommendation rests on user self-pacing
  discipline. If user fires 30 in 3 days (Pattern B), saturation marker 1
  becomes confirmation-bias-vulnerable per BG-D §C3. No external enforcement.
- C7 — observations.md is hand-edited markdown (BG-D §C7). 30-session corpus
  rests on user formatting discipline matching §4 template. Parser regex
  fragile; if user coins new candidate (X) or non-standard hit value, analyzer
  silently drops. Mitigation: analyzer warns on unparsed lines, not silent skip.

---

## §6 Composability + handoff

- Upstream:
  - `docs/anima_core_emerge_stage_3_user_protocol_spec_2026_05_05.md` (BG-D)
  - `docs/anima_core_clm_v4_mount_emerge_paradigm_2026_05_05.md` (paradigm)
  - `docs/anima_clm_v4_architecture_archaeology_emerge_2026_05_05.md` (D-H)
- Sister BG (in-flight):
  - BG-B `tool/anima_cli/dialogue_session_analyzer.hexa` (corpus aggregator;
    decoupled per BG-D §6.5)
- Downstream:
  - `state/anima_core_dialogue_corpus_<YYYY_MM_DD>/aggregate.json` (post-30)
  - `docs/anima_core_emerge_stage_3_closure_<YYYY_MM_DD>.md` (when M1/M2/M3 fires)

raw compliance:
- raw#9 — md only; no shim or hexa source modifications
- raw#10 — §5 has 7 honest C3 entries (>= 5)
- raw#15 — additive only; existing REPL helpers + BG-D spec untouched
- raw#37 — transient .py REPLs READ-ONLY (sister-rule); .own 3 helpers unchanged

End of Stage 3 corpus protocol skeleton landing. Doc-only land. No commit. $0 mac.
