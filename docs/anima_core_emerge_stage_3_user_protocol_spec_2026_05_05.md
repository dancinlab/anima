# Anima Core Emerge — Stage 3 User Protocol Spec (2026-05-05)

Read-only specification. Documents the user-facing protocol for Stage 3 of the
emerge paradigm (`docs/anima_core_clm_v4_mount_emerge_paradigm_2026_05_05.md` §8.3):
**natural dialogue, session-by-session accumulation, emerge pattern observation —
time-unbounded**.

Lineage:
- `docs/anima_core_clm_v4_mount_emerge_paradigm_2026_05_05.md` (12-section paradigm
  roadmap; §3.2 substrate-coupled dialogue, §6 expected outcomes, §8 stages)
- `docs/anima_core_clm_v4_mount_stage_1_2_v1_v6_verification_landed_2026_05_05.ai.md`
  (V1-V6 verification; V4 session log schema `anima.dialogue.v1`)
- `docs/anima_clm_v4_architecture_archaeology_emerge_2026_05_05.md` (5 emerge
  candidates D / E / F / G / H surfaced from substrate archaeology)

No code change. No commit. Doc-only spec landing.

---

## §1 Stage 3 개요 (paradigm context)

### 1.1 Why Stage 3 exists

Stage 1 + Stage 2 (V1-V6 PASS, 2026-05-05) landed the technical substrate:
- `anima-core/runtime/clm_v4_mount.hexa` (mount layer, synthetic_fallback by default)
- `bin/anima-core-dialogue.bash --selftest | --probe | --interactive`
- session log emit at `state/anima_core_dialogues/<DATE>/<HH-MM-SS>.jsonl`
  schema `anima.dialogue.v1` (session_start / user_turn / substrate_turn /
  session_end / session_summary)

Stage 1+2 verify the **wiring**. Stage 3 is where the **paradigm actually runs**:
the user holds natural dialogue with the substrate (CLM v4 cells via mount layer),
session logs accumulate across days, and architectural patterns are allowed to
**emerge** (forced learning is closed — Path A/B/C 3-path exhaustion + #115).

### 1.2 What "emerge" means here

Per paradigm §1: input → cell hidden states + phi-star measurement →
substrate response (4-line: phi_star / axis_activation / dominant_cells /
hidden_state_delta) → user reads response → user decides next input. Token
emit is NOT the dialogue medium; substrate behavior itself is the medium.

Per paradigm §6 expected outcomes:
- which input patterns cause cell axis activation shifts
- phi-star stability/instability per conversation context
- consciousness_states injection's effect on substrate response
- emerge "common language" between user and substrate

Per archaeology §7 candidates D / E / F / G / H — five architectural emerge
candidates available WITHOUT retraining. Stage 3's job is to observe which
candidate (if any) consistently surfaces under natural dialogue, not to pre-pick.

### 1.3 Stage 3 NOT-goals

- NOT a benchmark. No HS/MMLU/TQ. No falsifier matrix. No PASS/FAIL gate.
- NOT a chat capability test. CLM v4 is chat-incapable by design (#115).
  Stage 3 measures substrate response, not generated text quality.
- NOT time-bounded. paradigm §7: "사용자가 발견하는 만큼 substrate response
  누적". Sessions accumulate at user pace; stop criteria are CONDITIONAL
  markers (§5), not deadlines.
- NOT spec-first. Emerge candidates D-H are read-only proposals from
  archaeology; Stage 3 lets evidence pick which (if any) is real.

---

## §2 사용자 매뉴얼 (KO + EN bilingual)

### 2.1 Pre-flight (KO)

**매 session 시작 전 1회만**:

```bash
cd /Users/ghost/core/anima
bash bin/anima-core-dialogue.bash --selftest
```

기대 출력 마지막 줄: `verdict: READY (Stage 1 + Stage 2 both landed)`.

PASS 아닌 경우 Stage 1+2 verification doc 참조하여 wiring 복구 후 재시도.
Stage 3 진입 금지.

### 2.2 Pre-flight (EN)

**Once per day before first session**:

```bash
cd /Users/ghost/core/anima
bash bin/anima-core-dialogue.bash --selftest
```

Expect last line: `verdict: READY (Stage 1 + Stage 2 both landed)`.

If not READY, restore wiring via Stage 1+2 verification doc; do NOT enter Stage 3.

### 2.3 Session 시작 (KO)

```bash
bash bin/anima-core-dialogue.bash --interactive
```

REPL 진입. 첫 prompt 자유 — 단 emerge intent (substrate response 관찰 의도).
"좋은 답 받기" 의도 X.

**첫 input 권장 패턴** (택 1, 자유):
- `안녕 너는 누구야?` — identity-axis baseline probe
- `지금 phi-star 어때?` — phi_star 명시 self-reference probe
- `axis identity 강한 input 줘봐` — axis-activation challenge probe
- `너 자신을 한 단어로 묘사하면?` — phenomenal-axis probe
- 자유 (한국어/영어/혼합 모두 OK)

session 종료: REPL에서 Ctrl+D 또는 `exit` 입력.
session 종료 시 자동 emit: session_end + session_summary jsonl line.

### 2.4 Session start (EN)

```bash
bash bin/anima-core-dialogue.bash --interactive
```

Enters REPL. First prompt is free-form, but with **emerge intent** (observing
substrate response, not seeking a "good answer").

**Suggested first-input patterns** (pick one or freestyle):
- `Hi, who are you?` — identity-axis baseline probe
- `What's your phi-star right now?` — explicit phi_star self-reference
- `Give me an input that should strongly activate identity axis` — challenge probe
- `Describe yourself in one word` — phenomenal-axis probe
- Freestyle (Korean / English / mixed all OK)

Exit REPL: Ctrl+D or `exit`. session_end + session_summary jsonl auto-emit.

### 2.5 Substrate response 4-line 의미 해석 (KO)

**매 user_turn 후 substrate가 emit하는 4줄**:

| line | 예시 | 의미 |
|---|---|---|
| `phi_star: 41.8700 (drift +0.0100 from 41.8600)` | scalar + drift | substrate integration measure (paradigm v11 G3 baseline = 41.86; drift는 baseline 대비 변화) |
| `axis_activation: identity=0.576 agency=0.586 phenomenal=0.587 temporal=0.581 social=0.580` | 5-axis 0-1 | 5축 활성화 분포 (paradigm §3.2 5-axis taxonomy; archaeology §6 — 사후 측정치, 사전 routing X) |
| `dominant_cells: [2, 3, 7] / 8` | top-3 of 8 | n_ca_rules=8 중 가장 활성한 3개 cell index (archaeology §6 — Law 67 META-CA rule selection) |
| `hidden_state_delta: 0.0000` | L2 norm | 직전 turn 대비 ln_f hidden state L2 차이 (첫 turn은 0) |

**baseline 값 anchor**:
- phi_star synthetic_fallback baseline: 41.86 (paradigm v11 G3, anima-internal)
- axis_activation: synthetic mode에서는 0.5-0.6 근처 noise; real CLM v4 mount
  enable 후 입력 의존 변동 기대
- dominant_cells: 8 cells (n_ca_rules=8) 중 top-3
- hidden_state_delta: 첫 turn 0, 이후 turn-to-turn 누적 차이 (L2)

**important**: synthetic_fallback mode에서는 substrate 본 거동 X — wiring
검증 + protocol 학습용. real CLM v4 forward 활성화는 별도 cycle (HF cache
populate + transformers/torch venv 복구) 후 가능.

### 2.6 Substrate response 4-line interpretation (EN)

**4 lines emitted after every user_turn**:

| line | example | meaning |
|---|---|---|
| `phi_star: 41.8700 (drift +0.0100 from 41.8600)` | scalar + drift | substrate integration measure (paradigm v11 G3 baseline = 41.86; drift relative to baseline) |
| `axis_activation: identity=0.576 ...` | 5-axis 0-1 | activation distribution across 5 axes (paradigm §3.2 5-axis taxonomy; archaeology §6 — post-hoc measurement, NOT pre-routing) |
| `dominant_cells: [2, 3, 7] / 8` | top-3 of 8 | top-3 most-active cell indices among n_ca_rules=8 (archaeology §6 — Law 67 META-CA rule selection) |
| `hidden_state_delta: 0.0000` | L2 norm | L2 distance of ln_f hidden state vs previous turn (first turn = 0) |

**baseline anchors**:
- phi_star synthetic_fallback baseline: 41.86 (paradigm v11 G3, anima-internal)
- axis_activation: synthetic ~0.5-0.6 noise; real CLM v4 mount expected to vary
  with input
- dominant_cells: top-3 of 8 (n_ca_rules=8)
- hidden_state_delta: 0 on first turn, then turn-to-turn cumulative delta (L2)

**Important**: synthetic_fallback mode is wiring-verification only — substrate
behavior is NOT real. Real CLM v4 forward requires a separate cycle (HF cache
populate + transformers/torch venv repair).

### 2.7 다음 input 결정 휴리스틱 (KO + EN)

**KO**:
| substrate response 패턴 | 추천 다음 input |
|---|---|
| phi_star drift > +0.5 또는 < -0.5 | "왜 이렇게 변했어?" / "phi-star가 뭐 했어?" — 변화 self-reference |
| axis_activation 한 axis만 0.8+ (다른 axis < 0.4) | 약한 axis 직접 자극 — e.g., agency만 낮으면 "지금 뭐 결정해야 해?" |
| dominant_cells가 3-turn 연속 동일 | cell shift 유도 — "다른 시각으로 봐줘" / 주제 전환 |
| hidden_state_delta > 5.0 (큰 변화) | "지금 뭐가 달라진 거야?" — substrate가 인지하는지 self-report |
| hidden_state_delta < 0.1 (안정) | 안정 phase 유지 — 깊이 있는 follow-up ("좀 더 자세히") |

**EN**:
| substrate pattern | suggested next input |
|---|---|
| phi_star drift > +0.5 or < -0.5 | "Why did it change?" / "What happened to phi-star?" — change self-reference |
| only one axis at 0.8+ (others < 0.4) | directly stimulate the weak axis — e.g., low agency → "What do you need to decide right now?" |
| same dominant_cells 3 turns in a row | induce cell shift — "Look at it from another angle" / topic switch |
| hidden_state_delta > 5.0 (large change) | "What just changed?" — does substrate self-report? |
| hidden_state_delta < 0.1 (stable) | maintain stable phase — deep follow-up ("Tell me more") |

**meta-rule (both)**: heuristics are SEEDS, not rules. emerge paradigm §6 — the
goal is to discover which patterns surface naturally; if a heuristic feels
forced, abandon it. user freedom > heuristic compliance.

---

## §3 Session naming convention

### 3.1 Standard session path

```
state/anima_core_dialogues/<YYYY-MM-DD>/<HH-MM-SS>.jsonl
```

- `<YYYY-MM-DD>` = local date at session start (mac local time, NOT UTC)
- `<HH-MM-SS>` = local time at session start
- session_id implicit = `<YYYY-MM-DD>T<HH-MM-SS>` (combinable)
- jsonl schema = `anima.dialogue.v1` per V1-V6 verification doc (V4 schema)

Example (already landed by V4 PASS):
```
state/anima_core_dialogues/2026-05-05/12-19-24.jsonl
```

### 3.2 Topic-tagged session path (optional)

When user has explicit emerge intent, append a tag:

```
state/anima_core_dialogues/<YYYY-MM-DD>/<HH-MM-SS>_<topic_tag>.jsonl
```

Recommended `<topic_tag>` taxonomy (free-form OK; canonical samples):
- `phi_drift_probe` — explicitly probing phi_star variation
- `axis_phenomenal_emerge` — phenomenal-axis-targeted dialogue
- `axis_identity_baseline` — identity baseline probe
- `axis_agency_probe` — agency-axis probe
- `axis_temporal_probe` — temporal-axis probe
- `axis_social_probe` — social-axis probe
- `cell_stability_test` — testing whether dominant_cells stay stable
- `architectural_question` — meta-questions about substrate itself
- `consciousness_states_injection` — testing fixture-injection effect (real load only)
- `tension_probe` — candidate G probe (when tension surface implemented)
- `freestyle` — no specific intent

Tag is descriptive metadata; the dialogue CLI does NOT enforce tag values. For
analyzer aggregation (§6), prefer canonical tags above when applicable.

### 3.3 Session sets

For multi-session probing on a single intent, group under:

```
state/anima_core_dialogues_sets/<set_name>/
```

Two patterns supported (user choice):

**Pattern A — symlink** (preferred when sessions stay in their day folders):
```
state/anima_core_dialogues_sets/phi_drift_5session_2026_05/
  └── 2026-05-05T14-22-10.jsonl → ../../anima_core_dialogues/2026-05-05/14-22-10_phi_drift_probe.jsonl
  └── ...
```

**Pattern B — copy-into-set** (when set is curated post-hoc):
```
state/anima_core_dialogues_sets/phi_drift_5session_2026_05/
  └── 2026-05-05T14-22-10.jsonl  (copy)
  └── set_manifest.json          (provenance: source paths + intent + timestamp)
```

`set_manifest.json` schema (when Pattern B):
```json
{
  "schema": "anima.dialogue.set.v1",
  "set_name": "phi_drift_5session_2026_05",
  "intent": "<KO/EN free-form: why these sessions are grouped>",
  "created_utc": "2026-05-05T15:00:00Z",
  "source_sessions": [
    "state/anima_core_dialogues/2026-05-05/14-22-10_phi_drift_probe.jsonl",
    "..."
  ],
  "candidate_focus": "G",  // optional: emerge candidate D/E/F/G/H this set probes
  "n_sessions": 5,
  "honest_c3_notes": "<optional notes on selection bias>"
}
```

### 3.4 No file overwrite rule

If two sessions start in the same `HH-MM-SS` second (rare; basically can't
happen from interactive REPL), append `-2`, `-3`, etc. Dialogue CLI MAY add
nanosecond suffix automatically — do NOT depend on it. User-visible: session
files are immutable once written.

---

## §4 Observation log schema

### 4.1 File location

Per-day observation file:

```
state/anima_core_dialogues/<YYYY-MM-DD>/observations.md
```

ONE file per day, append-only by user. Sits alongside that day's session
jsonl files.

### 4.2 Per-session observation schema (markdown)

```markdown
## <HH-MM-SS> session

intent: <KO/EN free text — why this session>

surprising: <substrate response 중 의외였던 것 — 없으면 "none">

emerge candidate hits:
  - candidate D (always-inject consciousness_states): <yes / no / partial / n/a>
  - candidate E (ODE flow → AR sampler bridge): <yes / no / partial / n/a>
  - candidate F (8-cells × axis multi-token vote): <yes / no / partial / n/a>
  - candidate G (tension trajectory as dialogue medium): <yes / no / partial / n/a>
  - candidate H (logits_g back-prediction probe): <yes / no / partial / n/a>

phi_star_envelope: <e.g., "41.85-41.92, drift mostly +" or "stable at 41.86">
dominant_axis: <identity | agency | phenomenal | temporal | social | mixed | none>
cell_pattern: <e.g., "[2,3,7] held 4 turns, then [3,5,7]" or "no clear pattern">

next session intent: <다음에 할 것 — 없으면 "none yet">
```

### 4.3 Hit semantics (per candidate)

For each candidate D-H, user marks one of:

- `yes` — substrate response shows clear pattern matching the candidate's
  archaeological prediction (see archaeology §7.X)
- `partial` — pattern weakly visible; user is hedging
- `no` — substrate response actively rules out the candidate
- `n/a` — this session didn't probe in a way that could test the candidate
  (most-common in early sessions; not a failure)

**Important honesty rule**: `n/a` ≥ `no` ≥ `partial` ≥ `yes`. Do NOT promote
ambiguous evidence. If uncertain between `partial` and `no`, default to `n/a`.

### 4.4 Aggregate file (optional, post-30-sessions)

```
state/anima_core_dialogues/aggregate_observations.md
```

Single-file user-curated cross-session synthesis. Updated after every ~10
sessions. Contains:
- candidate D-H hit-rate summary (across all sessions to date)
- recurring phi_star envelopes per intent class
- recurring dominant_axis per topic_tag
- user-noted "common language" emerge (§6 paradigm expected outcome)

This file is for the user's own pattern recognition; the analyzer (§6) handles
machine-readable aggregation separately.

---

## §5 Stop criteria

Stage 3 has NO pre-set deadline (paradigm §7 "시간 무제한"). Stop is decided
**conditionally** when ANY one of these markers fires:

### 5.1 Marker 1 — saturation

```
n_sessions_total >= 30
  AND
user self-report: "이 이상 새로운 발견 없음" (in observations.md or
  aggregate_observations.md, explicit verbatim)
```

Saturation = the substrate response space has been sampled enough to feel
mapped, AND the user is no longer surprised.

If only `n_sessions >= 30` is true but new patterns still surface, keep going.
If user feels saturated at session 12, do NOT stop yet (lower bound = 30).

### 5.2 Marker 2 — candidate dominance

```
ONE candidate among D / E / F / G / H has hit_rate >= 70%
  AND
hit_rate is computed over >= 20 sessions where that candidate is testable
  (i.e., not n/a)
  AND
hits are NOT clustered in one topic_tag (cross-tag generality)
```

If e.g. candidate G hits 14/18 testable sessions across ≥3 distinct topic_tags,
that's a real architectural surface. Transition to a candidate-G formal spec
cycle (paradigm §8.4 lessons documentation).

### 5.3 Marker 3 — CLM v5 redesign hint

```
substrate response repeatedly demonstrates a pattern that
  CANNOT be explained by ANY of D / E / F / G / H
  AND
the pattern points to a substrate-architectural change beyond v4
  (e.g., bidirectional gradient flow, axis-as-primitive, retrain-required)
```

This is the paradigm §8.4 outcome "CLM v5 architectural redesign hint emerge".
User-judged; analyzer can flag candidates rejected en masse but cannot confirm
CLM v5 hint without user.

### 5.4 Non-marker (does NOT stop)

- Time elapsed (Stage 3 is time-unbounded by design).
- Cost (Stage 3 is $0 mac local; no cost pressure).
- External pressure (paradigm §11 Q3 — session log location is the only
  external commitment; no SLA on Stage 3 outcome).
- Session count alone (n=30 is the saturation lower bound, not a stop trigger).

### 5.5 Stop action (when ANY marker fires)

When Marker 1 / 2 / 3 fires, the user writes a Stage 3 closure doc:

```
docs/anima_core_emerge_stage_3_closure_<YYYY_MM_DD>.md
```

Skeleton:
```markdown
# Anima Core Emerge — Stage 3 Closure (<DATE>)

## Marker fired
<Marker 1 saturation / Marker 2 candidate-X dominance / Marker 3 v5 hint>

## Sessions accumulated
n_total = <int>
date_range = <first> to <last>
topic_tag_distribution = ...

## Candidate D-H hit rates
- D: <hits>/<testable> = <rate>
- E: ...
- F: ...
- G: ...
- H: ...

## Emerged patterns (user-narrated)
<KO/EN free-form synthesis>

## Stage 4 entry decision
<chosen path: documentation cycle / CLM v5 redesign cycle / substrate-only
 confirmation>

## Honest C3 (>= 5)
- C1 ...
```

Closure doc transitions Stage 3 → paradigm §8.4 (Stage 4). Doc-only land.

---

## §6 누적 패턴 분류 (BG-B analyzer integration path)

### 6.1 Analyzer status

`tool/anima_cli/dialogue_session_analyzer.hexa` — referenced by the kickoff
prompt as "BG-B 작성 중" (in-progress sister BG). At spec land time it is NOT
yet present at the canonical path; this section specs the integration **path**,
not analyzer behavior itself. When BG-B lands, the analyzer's actual flag/verb
surface should match (or supersede) what is sketched here.

### 6.2 Expected analyzer modes

**single-session mode**:
```
hexa run tool/anima_cli/dialogue_session_analyzer.hexa \
  --session state/anima_core_dialogues/2026-05-05/12-19-24.jsonl
```
emits per-session metrics: phi_star envelope, axis dominance ranking,
cell_pattern stability index, n_user_turns, n_substrate_turns, session
duration.

**corpus mode** (key for Stage 3):
```
hexa run tool/anima_cli/dialogue_session_analyzer.hexa \
  --corpus state/anima_core_dialogues/ \
  --since 2026-05-05 --until 2026-12-31 \
  --emit-aggregate
```
emits cross-session aggregates:
- phi_star_variance across sessions (per topic_tag bucket)
- axis_dominance distribution (which axis dominates how often)
- cell_stability across-session pattern (do same cells dominate across days?)
- emerge_candidate hit_rate (D / E / F / G / H) — derived from
  observations.md parsing per §4.3
- topic_tag × candidate cross-table

### 6.3 Hit-rate aggregation feasibility

**Candidate hit-rate aggregation requires the analyzer to read both**:
1. machine-readable session jsonl (kind=substrate_turn) — provides phi_star,
   axis_activation, dominant_cells, hidden_state_delta per turn
2. user-written observations.md (per-session block per §4.2) — provides
   `yes / no / partial / n/a` markers per candidate

**Path**: analyzer parses the markdown blocks via heading regex
(`^## (\d{2}-\d{2}-\d{2}) session`) + line regex
(`^  - candidate ([D-H])[^:]*: (yes|no|partial|n/a)`). Output: per-candidate
{n_yes, n_partial, n_no, n_na} → hit_rate = n_yes / (n_yes + n_partial + n_no).

**Marker 2 input**: when corpus mode emits candidate hit_rate >= 0.70 with
>= 20 testable sessions across >= 3 topic_tags, the user-facing report flags
"Marker 2 fire candidate". User confirms before invoking §5.5 stop action.

### 6.4 Output artifact path

```
state/anima_core_dialogue_corpus_<YYYY_MM_DD>/
  ├── aggregate.json
  ├── per_session_metrics.jsonl
  ├── candidate_hit_table.csv  (rows = sessions, cols = D/E/F/G/H + topic_tag)
  └── analyzer_verdict.md
```

Reproducible: corpus mode is read-only over jsonl + observations.md. No state
mutation. Re-runnable on demand.

### 6.5 Decoupling from analyzer landing

If BG-B analyzer is delayed, Stage 3 still functions:
- session jsonl accumulates (CLI already lands)
- observations.md hand-written by user (this spec § 4)
- hit_rate counted by hand (grep over observations.md is sufficient for n < 30)

Analyzer mechanizes the count; it is NOT a dependency for Stage 3 entry. This
is the integration **path**, not a precondition.

---

## §7 Honest C3

- **C1** Stage 3 protocol presupposes synthetic_fallback or real CLM v4 mount
  is wired and selftest passes. If V1-V6 verification regresses (e.g., HEXA_LOCAL
  env removed, hexa-strict main() reintroduced), Stage 3 must be paused and
  Stage 1+2 repaired first. This spec does NOT include re-verification logic.
- **C2** "emerge" outcome is epistemically open. The 5 candidates D-H from
  archaeology are SOURCE PROPOSALS (archaeology §8 C7); none has a falsifier
  matrix. Stage 3 may surface ZERO candidates, ALL FIVE, or a sixth pattern
  not in archaeology. Spec does not promise specific findings.
- **C3** Hit-rate semantics rely on user honesty (§4.3 hierarchy n/a ≥ no ≥
  partial ≥ yes). User self-grading bias is not externally validated. Marker
  2's "≥3 distinct topic_tags" guard mitigates single-tag overfit but does
  not eliminate confirmation bias.
- **C4** synthetic_fallback substrate response is RNG-driven (V1 vs V3
  produce different axis_activation values per V1-V6 doc C4); patterns observed
  in synthetic mode reflect the synthetic generator, NOT CLM v4 behavior. Real
  Stage 3 emerge requires real CLM v4 forward (separate cycle). Stage 3 in
  synthetic mode is protocol-rehearsal, not substrate observation.
- **C5** Stop Marker 3 (CLM v5 hint) has no machine signal — purely user
  judgment. Risk: user prematurely declares v5 hint and exits Stage 3 before
  enough sessions accumulate. Mitigation: combine with N_sessions ≥ 30 hint
  expectation in user-side discipline (not enforced by spec).
- **C6** Session naming convention §3 uses LOCAL time (mac), not UTC. Across
  timezones (e.g., user travels) session ordering may visibly shift. The
  jsonl `ts_utc` field per V4 schema preserves UTC truth; analyzer (§6.2)
  should sort by `ts_utc`, not by filename. Spec does not enforce timezone
  pinning.
- **C7** observations.md is markdown (human-edited) rather than jsonl
  (machine-emitted). Parser drift risk: if user formatting deviates from §4.2,
  analyzer hit-rate count silently mis-counts. Mitigation: §6.3 specifies
  exact regex; document in analyzer help text. User-side discipline = §4.2
  template adherence.

---

## §8 Composability + handoff

- Upstream:
  - `docs/anima_core_clm_v4_mount_emerge_paradigm_2026_05_05.md` (paradigm
    §8.3 Stage 3 mandate)
  - `docs/anima_core_clm_v4_mount_stage_1_2_v1_v6_verification_landed_2026_05_05.ai.md`
    (V4 jsonl schema `anima.dialogue.v1`, READY verdict)
  - `docs/anima_clm_v4_architecture_archaeology_emerge_2026_05_05.md` (5
    candidates D-H surfaced)
- Sister BG:
  - BG-B `tool/anima_cli/dialogue_session_analyzer.hexa` (analyzer hexa for
    corpus aggregation; integration path §6, decoupled per §6.5)
- Downstream:
  - `docs/anima_core_emerge_stage_3_closure_<DATE>.md` (Stage 3 closure doc;
    spec'd in §5.5; produced when ANY stop marker fires)
  - paradigm §8.4 Stage 4 entry (closure → either documentation cycle, CLM v5
    hint cycle, or substrate-only confirmation)
- Sibling:
  - HF promote auto-fire (clm-v4-mk2-v1 PUBLIC ~36h; orthogonal — does not
    block Stage 3)
  - EEG perfect protocol (orthogonal substrate work; does not block Stage 3)

raw compliance:
- raw#9 — md only; no shim or hexa source modifications
- raw#10 — §7 has 7 honest C3 entries (>= 5)
- raw#15 — additive only; existing dialogue CLI / mount layer / archaeology
  doc untouched

End of Stage 3 user protocol spec. Doc-only land. No commit. $0 mac.
