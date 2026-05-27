# Anima Core — Dialogue Session Analyzer LANDED (2026-05-05)

## Stage 3 prep — emerge dialogue session pattern discovery 인프라

BG-B output. Stage 3 (사용자 dialogue session 누적) 시작 전 미리 land — accumulation 시점에 즉시 분석 가능한 도구.

## Files added (raw#15 additive only)

```
tool/anima_cli/dialogue_session_analyzer.hexa     894 LoC
bin/anima-core-dialogue-analyze.bash              129 LoC (chmod +x)
state/anima_core_dialogue_analyzer_2026_05_05/verdict.json
docs/anima_core_dialogue_analyzer_landed_2026_05_05.ai.md (this file)
```

Untouched: `mount.hexa`, `dialogue.hexa`, `anima-core-dialogue.bash` (raw#15).

## Verdict

`STAGE_3_PREP_LANDED`

- Selftest: 5/5 format checks PASS (n_turns + axis_dominant + jaccard + delta + parse_lines)
- Real-session smoke (`12-19-24.jsonl`): 4/4 substrate-response lines parsed, all expected aggregates match
- Corpus smoke (`--date 2026-05-05`): 3 sessions aggregated, 2 zero-default (failed remote V3/V4 substrate emit) + 1 real (V4 synthetic_fallback)

## Selftest result (synthetic 3-turn)

```
__ANIMA_DIALOGUE_ANALYSIS__ session=synth_session.jsonl
n_turns=3
phi_star_range=[41.8500, 41.9000] mean=41.873 stddev=0.021
phi_star_drift_max=0.040
axis_dominant_global=phenomenal
axis_swing_max=phenomenal
cell_stability_jaccard=0.750     # (1.0 + 0.5) / 2 — turn3 swap [2,3,7]→[2,3,5]
delta_cumulative=3.500            # 0.0 + 1.5 + 2.0
__ANIMA_ANALYSIS_OK__
```

## Real V4 session (12-19-24.jsonl)

```
n_turns=1
phi_star_range=[41.8700, 41.8700]   # V3 probe canonical
phi_star_drift_max=0.010
axis_dominant_global=phenomenal      # phenomenal=0.587 strongest
cell_stability_jaccard=1.000         # single turn → 1.0 by convention
delta_cumulative=0.000               # synthetic-fallback emit
```

4 substrate-response lines parsed correctly:
- `phi_star: 41.8700 (drift +0.0100 from 41.8600)`
- `axis_activation: identity=0.576 agency=0.586 phenomenal=0.587 temporal=0.581 social=0.580`
- `dominant_cells: [2, 3, 7] / 8`
- `hidden_state_delta: 0.0000`

## Honest C3 (raw#10 — emit ≥5 to stderr)

- **C1** axis taxonomy (5-bucket: identity / agency / phenomenal / temporal / social) inherits anima-internal heuristic from mount.hexa
- **C2** `cell_stability_jaccard` threshold for "stable" interpretation is anima-canonical (no external validation)
- **C3** `phi_star_stddev` / `phi_star_drift_max` thresholds for "stable / unstable" is anima-canonical
- **C4** `delta_cumulative` magnitude scale depends on substrate mode (synthetic vs real torch-load); cross-mode comparison invalid
- **C5** emerge pattern discovery is downstream-deferred — this tool surfaces signals only; pattern interpretation requires user dialogue session accumulation

## Stage 3 emerge path (next-step recommendation)

When user starts emerging real dialogue:

1. **per-session surface** — `bin/anima-core-dialogue-analyze.bash --session <jsonl>` after each REPL session captures phi/axis/cell trajectory
2. **daily corpus rollup** — `--date YYYY-MM-DD` aggregates all sessions; `axis_dominant_corpus` distribution begins surfacing emerge-candidate signal (which of D/E/F/G/H from `anima_clm_v4_architecture_archaeology_emerge_2026_05_05.md` naturally manifests)
3. **threshold calibration** — after 5-10 real user sessions, recalibrate phi_stddev / jaccard / delta thresholds (currently anima-canonical placeholders per C2/C3/C4)
4. **cross-session jaccard** — extend to session-pair `dominant_cells` similarity → cross-pollination pattern discovery (deferred enhancement)
5. **anima dialogue_session topic** — register analyzer under `tool/anima_cli/_common.hexa` dispatcher so `anima dialogue_session --analyze ...` works alongside `anima dialogue` (Stage 4 prep)

## Cost

- $0 (mac local; pure hexa string parse + arithmetic, no remote dispatch)
- ~30min wall (spec → impl → selftest → real-session validation → docs)

## raw policy compliance

- raw#9 hexa primary + bash wrapper carve-out
- raw#10 honest C3 ≥5 (analyzer emits to stderr; doc embeds them above)
- raw#11 snake_case throughout
- raw#15 additive — `mount.hexa`, `dialogue.hexa`, `anima-core-dialogue.bash` UNTOUCHED
- raw#37 no transient_py needed (pure hexa string parse handles JSONL + escaped raw_output)

## Invocation reference

```bash
# selftest
bin/anima-core-dialogue-analyze.bash --selftest

# single session
bin/anima-core-dialogue-analyze.bash --session state/anima_core_dialogues/2026-05-05/12-19-24.jsonl

# date corpus
bin/anima-core-dialogue-analyze.bash --date 2026-05-05

# direct hexa (alt route)
HEXA_LOCAL=1 /Users/ghost/.hx/bin/hexa run tool/anima_cli/dialogue_session_analyzer.hexa --selftest
```

## Schema reference (parsed JSONL fields)

From `dialogue.hexa` `anima.dialogue.v1` schema — analyzer parses:

- `session_start` line → ignored (baseline metadata only; phi_star_baseline retained for future drift-vs-baseline metric)
- `user_turn` line → ignored (no metrics; counted only for n_turns context if needed in future)
- `substrate_turn` line → primary metric source. `raw_output` field's embedded substrate-response block extracted via JSON-string unescape, then 4 lines (`phi_star:`, `axis_activation:`, `dominant_cells:`, `hidden_state_delta:`) parsed for metrics.
- `session_end` / `session_summary` → ignored (analyzer recomputes aggregates independently)

## Stage 3 readiness

Analyzer is **dispatch-ready**. The moment user begins real dialogue REPL accumulation (`anima-core-dialogue.bash --interactive`), each session JSONL becomes immediately analyzable with no further infra work. The 4-line substrate-response parse path is verified against real V4-mount synthetic-fallback emit.
