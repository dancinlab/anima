# qmirror 2.0 closure watchdog — landed 2026-05-04

## Summary

Landed `tool/qmirror_2_closure_watchdog.hexa` (~370 LoC, raw#9 hexa-strict, raw#15 SSOT, raw#10 4 caveats). Polls 5 cond verdict.json files (cond.9, cond.10, cond.11, cond.12, cond.13) every 30 min for up to 48 h; on 5/5 land, dispatches `tool/qmirror_2_closure_synth.hexa` (sister BG writing) and emits composite verdict (FULL ≥5 PASS / PARTIAL =4 PASS / DEFERRED <4 PASS / INCOMPLETE if any cond MISSING). On `--bump` flag with composite ∈ {FULL, PARTIAL}, performs IRREVERSIBLE version bump 1.0.1 → 2.0.0 across hexa.toml + CHANGELOG.md + registry.tsv + GitHub release v2.0.0 + optional hf mirror upload.

## State at land

All 3 sister BGs (cond.11 stabilizer + cond.12 surface-d3 + cond.13 CSCS) **already landed** during this watchdog cycle. Single-poll dry run confirms 5/5 PASS:

| cond  | Falsifier      | Verdict | Key metric                                           |
|-------|----------------|---------|------------------------------------------------------|
| 9     | F-QM-2-TOMO-9  | PASS    | fidelity_min=0.99918 (7/7 gates @ 8000 shots)        |
| 10    | F-QM-2-GHZ-10  | PASS    | M=4.0 analytic exact (30 trials × 1024 shots)        |
| 11    | F-QM-2-STAB-11 | PASS    | syndrome_plus=1.0 + post_fid=1.0                     |
| 12    | F-QM-2-SURF-12 | PASS    | logical_zero_ratio=1.0 (1024 shots, 17-qubit Aer)   |
| 13    | F-QM-2-CSCS-13 | PASS    | min(S)=2.8174 / W=2.8211 / indep_p=0.1120            |

Composite verdict: **FULL** → state/qmirror_2_closure_2026_05_04/verdict.json

## Watchdog status (3 cond ETA + trigger condition)

- **cond.11 stabilizer**: ETA 1.5 d → **landed early** (verdict.json present, PASS)
- **cond.12 surface d=3**: ETA 2 d → **landed early** (verdict.json present, PASS)
- **cond.13 CSCS chained**: ETA 1.5 d → **landed early** (verdict.json present, PASS)

**Trigger condition**: 5/5 conds VALID:label∈{PASS,FAIL,PARTIAL,DEFERRED} → currently SATISFIED (5/5 PASS); `--once` dry run already FIRED.

## 4 caveats (raw#10 honest C3)

(a) **48 h max-wait** sized for cond.12 (2 d) + headroom; on timeout, manual re-fire required (no auto-extend; exit 0 with TIMEOUT label).

(b) **Closure synth conditional** on all 3 sister BGs landing AND each producing a parseable verdict.json. If any cond verdict is malformed (PARSE_ERROR, INVALID_LABEL), watchdog logs the error and continues polling (does NOT trigger on partial signals). Manual override available via `ANIMA_QM2_FORCE_TRIGGER=1`. Sister BG writing `tool/qmirror_2_closure_synth.hexa` is **NOT YET PRESENT**; watchdog falls back to inline composite emit until it lands. After synth tool lands, re-run `--apply` to invoke it.

(c) **Version bump 1.0.1 → 2.0.0 IRREVERSIBLE** per semver (major bump signals breaking changes). Closure synth must verify backward-compat OR bump_strategy must be explicit. `--bump` flag is gated separately from `--apply` for this reason; default is DRY.

(d) **GitHub release v2.0.0** requires `gh auth status` clean + write scope on `dancinlab/qmirror`; if gh auth fails, release step logs RC!=0 and is SKIPPED (composite verdict still emitted; manual `gh release create v2.0.0` retry required). hf upload (`--hf`) is similarly opt-in and may fail if `HUGGING_FACE_HUB_TOKEN` absent.

## Files landed

- `tool/qmirror_2_closure_watchdog.hexa` — watchdog tool (selftest verifies 15 invariants + composite resolver via _compose_verdict)
- `state/qmirror_2_closure_2026_05_04/verdict.json` — composite verdict (FULL, 5/5 PASS, applied=false)
- `state/qmirror_2_closure_2026_05_04/per_cond_status.json` — per-cond snapshot
- `state/qmirror_2_closure_2026_05_04/watchdog_log.jsonl` — poll + trigger events
- `state/markers/qmirror_2_closure_watchdog_landed.marker` — landing marker

## Next operator action (recommended ranked by 완성도)

**Rank 1 (HIGHEST 완성도): wait-for-synth then full bump**
  Wait for sister BG `qmirror_2_closure_synth` to land `tool/qmirror_2_closure_synth.hexa`,
  then: `hexa run tool/qmirror_2_closure_watchdog.hexa --once --apply --bump`
  → invokes synth + version bump + CHANGELOG + registry + GitHub release v2.0.0
  → completes the qmirror 2.0 closure end-to-end (one operator action)

**Rank 2: synth-only first, defer bump**
  `hexa run tool/qmirror_2_closure_watchdog.hexa --once --apply`
  → invokes synth (when present), emits composite verdict
  → defers irreversible version bump for human review

**Rank 3: idle loop until sister synth + 24h soak**
  `hexa run tool/qmirror_2_closure_watchdog.hexa --loop --apply`
  → runs continuous 30-min poll for 48 h
  → useful if synth sister BG ETA is uncertain

## Cross-references

- Spec: `docs/qmirror_2_axes_spec_2026_05_03.md` (5-axis ranked matrix, F-QM-2-* falsifier set)
- Sister cond markers:
  - `state/markers/qmirror_2_cond9_tomography_landed.marker`
  - `state/markers/qmirror_2_cond10_ghz_mermin_landed.marker`
  - (cond.11/12/13 markers pending sister BG landing emit)
- Version target: hexa.toml 1.0.1 → 2.0.0; registry.tsv qmirror row 1.0.0 → 2.0.0
- Upstream closure: `state/markers/qmirror_closure_landed.marker` (8/8 → 13/13 expansion)
