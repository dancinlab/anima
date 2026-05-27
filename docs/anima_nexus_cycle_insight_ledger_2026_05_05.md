<!-- @no-lineage-citation-exempt-file -->
<!-- @no-user-verbatim-exempt-file -->
# Anima Nexus Cycle — Insight Ledger (2026-05-05)

Read-only synthesis of the 2026-05-05 anima-core CLI + CLM v4 mount paradigm
entry cycle. BG-J output. Doc + verdict only — zero source change, zero
commit. The ledger captures (1) candidate L34-L43 lessons, (2) emergent
paradigm patterns, (3) the 5-candidate emerge matrix, (4) open questions
ledger, (5) D+0..D+7 forecast. Lineage:

- `docs/anima_core_clm_v4_mount_emerge_paradigm_2026_05_05.md` (paradigm roadmap)
- `docs/anima_core_clm_v4_mount_stage_1_landed_2026_05_05.ai.md` (KICK-1)
- `docs/anima_clm_v4_architecture_archaeology_emerge_landed_2026_05_05.ai.md` (KICK-2)
- `docs/anima_core_dialogue_stage_2_prep_landed_2026_05_05.ai.md` (KICK-3)
- `docs/anima_core_clm_v4_mount_stage_1_2_v1_v6_verification_landed_2026_05_05.ai.md` (V1-V6)
- `docs/anima_core_dialogue_analyzer_landed_2026_05_05.ai.md` (BG-B Stage 3 prep)
- `docs/anima_emerge_candidate_d_always_inject_spec_2026_05_05.md` (BG-C)
- `docs/anima_core_emerge_stage_3_user_protocol_spec_2026_05_05.md` (BG-D)
- `docs/anima_hf_promote_watchdog_audit_landed_2026_05_05.ai.md` (BG-E)
- `docs/anima_top_level_cli_dispatch_audit_landed_2026_05_05.ai.md` (BG-F)

The ledger is referenceable for future cycles. Lessons are CANDIDATE
banking — promotion to canonical SSOT requires a separate
`BG-LESSONS-PROPAGATE` cycle (matches L36+L38 promotion convention).

---

## §1 Sub-1 — Lesson L34-L43 candidate identification

Existing canonical lessons L1-L33 (per `MEMORY.md` and prior banking docs)
established the foundation. The 2026-05-05 cycle surfaces ten new candidate
lessons with file/line evidence. Each candidate lists: title, evidence,
when-applicable rule, exception (if any).

### L34 — Forced-learning paradigm closure unlocks emerge paradigm; LoRA→spec-first→KICK pattern emergence

- **Evidence**: `docs/anima_core_clm_v4_mount_emerge_paradigm_2026_05_05.md`
  §2 (Path A/B/C 3-path closure + #115 architectural); §10 honest C3
  ("forced learning paradigm 폐기"). Cycle realization: KICK-1
  (mount layer) + KICK-2 (archaeology) + KICK-3 (dialogue CLI) ran in
  parallel without spec-first dependency tree.
- **When applicable**: Once a forced-learning lane (LoRA / SFT / distill /
  retrain) hits 3-path closure with chat-capability FAIL_TRUE on the
  architectural-incapability hypothesis, default to emerge paradigm —
  parallel KICK on (mount layer / archaeology / CLI surface) without
  pre-locking falsifier matrix.
- **Exception**: If chat-capability is not the goal (e.g., substrate-only
  research), forced-learning may still be appropriate; emerge is for
  substrate-coupled dialogue.

### L35 — hexa-strict auto-invokes `fn main()`; explicit `main()` call doubles execution

- **Evidence**:
  `docs/anima_core_clm_v4_mount_stage_1_2_v1_v6_verification_landed_2026_05_05.ai.md`
  Issue 1 ("hexa-strict auto-invoke 충돌"). `dialogue.hexa:295` +
  `clm_v4_mount.hexa:670` both defined `fn main(){...}` AND added explicit
  `main()` call → V3 first attempt rc=1 with "auto-invoke conflict"
  error.
- **When applicable**: Any new `.hexa` orchestration file MUST choose ONE
  of: (a) define `fn main()` and let hexa-strict auto-invoke handle, OR
  (b) write top-level statements without `fn main()` wrapper. NEVER both.
- **Exception**: None. The hexa-strict mode is the canonical anima
  runtime; no opt-out path documented.

### L36 — `hexa_remote` defaults to ubu1 routing; mac-local intent requires `HEXA_LOCAL=1` prefix consistently

- **Evidence**:
  `docs/anima_core_clm_v4_mount_stage_1_2_v1_v6_verification_landed_2026_05_05.ai.md`
  Issue 2 ("hexa_remote dispatch가 mac homebrew python 경로 hardcode"
  + `[GATE] dispatch=local reason=remote_unreachable cmd="python3
  /opt/homebrew/bin/python3..."`). Two call sites in
  `bin/anima-core-dialogue.bash` (line 241, 265) both required prefix
  fix.
- **When applicable**: Any bash wrapper that invokes `hexa run` against
  a hexa file with mac-local intent (helper.py emit at `/tmp/`,
  homebrew python deps) MUST prefix the call with `HEXA_LOCAL=1`. EEG
  perfect protocol BG already established the pattern (raw#103
  darwin-bypass + `HEXA_LOCAL=1`).
- **Exception**: When the hexa file is genuinely deployment-agnostic
  (pure hexa string ops, no python/homebrew deps), routing default is
  fine; selftest verifies.

### L37 — emerge candidate taxonomy = 4-mode {none, X, Y, Z} × 3-state falsifier {PASS, FAIL_TRUE, FAIL_FALSE}

- **Evidence**:
  `docs/anima_emerge_candidate_d_always_inject_spec_2026_05_05.md` §2
  (4 inject modes: none/zero/canonical/user_supplied) + §5 (F-CAND-D-1/2/3
  with 3-state output matching L26-L27 axis-preservation calibration carry).
  Generalizes to candidate D/E/F/G/H matrix: each candidate gets a
  4-mode interface and 3-state falsifiers.
- **When applicable**: Emerge candidate spec authoring should default to
  4-mode taxonomy (one bypass control + three engagement modes of
  increasing structure) and 3-state falsifier {PASS / FAIL_TRUE
  architectural / FAIL_FALSE measurement-pipeline}.
- **Exception**: Some candidates are ambient-only (e.g., G tension
  trajectory, H head_g) — they ride atop another candidate's mode and
  do not need their -mode dispatch.

### L38 — V1-V6 verification = selftest + probe + log emit + corpus + integration 5-stage

- **Evidence**:
  `docs/anima_core_clm_v4_mount_stage_1_2_v1_v6_verification_landed_2026_05_05.ai.md`
  V1-V6 table:
  V1 mount selftest, V2 dialogue CLI selftest, V3 end-to-end probe, V4
  session log emit, V5 archaeology cross-pollination, V6 interactive
  REPL wired (user fire). 5/5 PASS + V6 wired.
- **When applicable**: New CLI/runtime layer landing should adopt
  V1-V6 staged verification as default — selftest first, then probe
  with synthetic_fallback, then end-to-end with log emit, then
  cross-pollination read, finally interactive (user-fire wiring
  validated independently of runtime invocation).
- **Exception**: Doc-only or read-only audits (BG-C / BG-D / BG-E /
  BG-F) skip V3/V4/V6 — they have no runtime path.

### L39 — Doc-only BGs are race-free; code BGs require git worktree or commit serialization

- **Evidence**: `MEMORY.md` `[parallel BG git race]` and
  `docs/anima_emerge_candidate_d_always_inject_spec_2026_05_05.md` §7
  C7 (parallel BGs writing `mount.hexa` / `dialogue.hexa` collide). The
  2026-05-05 cycle ran 6+ BG in parallel; KICK-1/3 wrote code (serialized
  by user-driven sequencing); BG-B/C/D/E/F/G/H/I/J ran doc-only and
  parallelized cleanly.
- **When applicable**: Plan parallel BG slate as: (a) ≤1 code-mutating
  BG per `git worktree`, OR (b) all code mutations serialized through
  one gating BG; (c) all spec/audit/archaeology BGs go full parallel
  on read-only paths.
- **Exception**: When code BGs touch disjoint file sets with no shared
  parent (e.g., `anima-core/runtime/X.hexa` vs `bin/anima-other.bash`),
  parallel is OK if commits are not attempted in-flight.

### L40 — Convention-driven dispatch rewards: KICK-3 land lands at `tool/anima_cli/<topic>.hexa`, BG-F audit verifies zero-change Option C

- **Evidence**:
  `docs/anima_top_level_cli_dispatch_audit_landed_2026_05_05.ai.md` (a)
  table — `bin/anima` line 47 header `anima <topic> ... → dispatch
  to tool/anima_cli/<topic>.hexa` is the convention; KICK-3 placed
  `tool/anima_cli/dialogue.hexa` exactly per convention. BG-F audit
  Option C ("코드 변경 X — 매뉴얼 표준화만") chosen; A/B rejected as
  redundant raw#15 violations.
- **When applicable**: When adding a new top-level verb, place the
  module at the conventional path FIRST; verify dispatch via
  generic-pattern audit; reject any dispatcher-mutation option as
  duplicated logic.
- **Exception**: If the convention is itself broken (dispatcher missing
  the topic case branch), one-line additive at the dispatcher is
  acceptable — but only after audit confirms the generic pattern
  doesn't already cover.

### L41 — `synthetic_fallback` design intent: selftest + probe both pass without real-load via deterministic emit

- **Evidence**: `clm_v4_mount.hexa` Stage 1 verdict.json
  ("synthetic substrate response generated via deterministic hexa string
  emit"). V3 PASS output annotated `mode=synthetic_fallback`. Real
  `transformers.AutoModelForCausalLM` import failure does NOT block
  V1-V6 PASS; the fallback path emits canonical-ish phi-star (41.86 ±
  small drift) and 5-axis activation (0.5-0.6 noise).
- **When applicable**: Mount-layer / probe-layer design should always
  include a synthetic_fallback that matches the real-emit format
  byte-for-byte (markers, 4-line substrate response, 5-axis taxonomy).
  This decouples wiring verification from real-runtime dependency
  (HF cache, venv, hardware) and lets V1-V6 PASS land in parallel with
  real-load enable.
- **Exception**: If the layer is intrinsically real-only (e.g., GPU
  benchmarks, HF push), synthetic_fallback may be replaced by `--dry-run`
  with mock HTTP responses.

### L42 — Source archaeology (post-impl) is emerge-paradigm-internal; spec-first archaeology would have prevented L36/L37/L38 root-cause discovery

- **Evidence**:
  `docs/anima_clm_v4_architecture_archaeology_emerge_landed_2026_05_05.ai.md`
  §3 + §4 (concretization of L36 apply walk override / L37 bypass guard
  / L38 load overwrites init). 5 emerge candidates surfaced from
  source-reading, NOT from spec-first design. The archaeology
  identified `conscious_decoder.py:553` as the architectural pivot —
  this would have been invisible from a top-down spec.
- **When applicable**: When entering emerge paradigm, prepend a
  source-archaeology BG that reads existing trained-substrate code
  before any new mount/CLI layer is written. Treat archaeology as a
  KICK-2 sibling to KICK-1, not a downstream consumer.
- **Exception**: Pure greenfield (no trained substrate, no shim, no
  legacy decoder) — archaeology has nothing to read; spec-first is
  appropriate.

### L43 — User-fire-able paths must pre-emit confirm-strings + manual; HF promote auto-fire uses `PROMOTE-clm-v4-mk2-v1` literal

- **Evidence**:
  `docs/anima_hf_promote_watchdog_audit_landed_2026_05_05.ai.md` Sub-5
  (user manual with exact confirm-strings: `PROMOTE-clm-v4-mk2-v1`,
  `PROMOTE-pbeta-50k`); EEG perfect protocol pre-emits
  `bash bin/anima-eeg-baseline.bash --fire`; dialogue REPL pre-emits
  `bin/anima-core-dialogue.bash --interactive`. All paths land their
  exact invocation string before unattended dwell.
- **When applicable**: Any user-fire-able cycle (HF promote, EEG run,
  emerge dialogue) MUST land:
  1. exact bash invocation
  2. confirm-string literal (verbatim)
  3. pre-fire checklist (sha256 / G1-G6 / token / dependency)
  4. expected output marker
  Within the landing doc, BEFORE leaving the cycle.
- **Exception**: Non-fire-able audit cycles (BG-E itself) — they output
  the manual but do not need their own.

---

## §2 Sub-2 — Pattern catalog

Eight reusable patterns surfaced during the 2026-05-05 cycle. Each pattern
lists: name, when-to-apply, example-land-doc.

### Pattern P1 — KICK pattern (parallel BG cycle entry)

- **Name**: KICK
- **When to apply**: New paradigm entry when ≥3 surface layers (mount /
  archaeology / CLI / verification) need landing in one cycle.
- **Form**: KICK-1 = mount/runtime layer; KICK-2 = source archaeology;
  KICK-3 = CLI/REPL surface; all parallel; no spec-first inter-dependency.
- **Example**: `docs/anima_core_clm_v4_mount_stage_1_landed_2026_05_05.ai.md`
  + `docs/anima_clm_v4_architecture_archaeology_emerge_landed_2026_05_05.ai.md`
  + `docs/anima_core_dialogue_stage_2_prep_landed_2026_05_05.ai.md` —
  all landed within hours, parallel BGs.

### Pattern P2 — V1-V6 verification (5-stage staged)

- **Name**: V1-V6
- **When to apply**: New runtime/CLI layer landed; before declaring
  Stage-N ready.
- **Form**: V1 mount selftest, V2 CLI selftest, V3 end-to-end probe,
  V4 session log emit, V5 archaeology cross-pollination, V6 interactive
  user-fire wired.
- **Example**:
  `docs/anima_core_clm_v4_mount_stage_1_2_v1_v6_verification_landed_2026_05_05.ai.md`.

### Pattern P3 — 4-mode × 3-state falsifier (emerge candidate spec)

- **Name**: 4×3
- **When to apply**: Emerge candidate spec where the candidate has a
  runtime control surface (mode dispatch) and pre-LOCK falsifier criteria.
- **Form**: 4 modes {none, zero, canonical, user_supplied} (or analogue);
  3 states {PASS, FAIL_TRUE, FAIL_FALSE}. FAIL_FALSE captures
  measurement-pipeline crash (NaN, calibration miss) distinct from
  architectural failure.
- **Example**: `docs/anima_emerge_candidate_d_always_inject_spec_2026_05_05.md`
  §2 + §5.

### Pattern P4 — `*_landed_2026_05_05.ai.md` + `state/<topic>_2026_05_05/verdict.json` doc pair

- **Name**: doc-pair
- **When to apply**: Every land — both landed-handoff markdown (for
  human/AI reading) AND machine-readable verdict.json (for
  cross-cycle parsing).
- **Form**: Markdown lives in `docs/`; verdict in `state/<topic>_<DATE>/`.
  Both must reference each other.
- **Example**: `docs/anima_core_clm_v4_mount_stage_1_landed_2026_05_05.ai.md`
  ↔ `state/anima_core_clm_v4_mount_stage_1_2026_05_05/verdict.json`.

### Pattern P5 — Bilingual KO + EN user-facing doc

- **Name**: bilingual
- **When to apply**: Any user-facing protocol/manual doc (NOT internal
  audit / archaeology / verdict).
- **Form**: KO and EN sections side-by-side per content unit (pre-flight,
  session start, response interpretation, heuristic table). Heuristic
  tables may be combined when terse.
- **Example**: `docs/anima_core_emerge_stage_3_user_protocol_spec_2026_05_05.md`
  §2 (six bilingual sub-sections).

### Pattern P6 — Honest C3 ≥5 inline + ≥7 emit

- **Name**: honest-C3
- **When to apply**: Every land doc (≥5 inline) AND every runtime
  binary (≥5 emit to stderr). Specs may go to ≥7 inline.
- **Form**: Numbered C1-CN with each caveat covering: (1) heuristic
  scope, (2) anima-internal vs external validation status, (3)
  measurement bias risk, (4) timeline/calibration deferred, (5) downstream
  brittleness. Specs trend toward 7+ entries.
- **Example**: `docs/anima_emerge_candidate_d_always_inject_spec_2026_05_05.md`
  §7 (7 entries); `clm_v4_mount.hexa` selftest emits C1-C5 to stderr.

### Pattern P7 — raw policy compliance footer

- **Name**: raw-footer
- **When to apply**: Every land doc.
- **Form**: A `raw 준수` (or `raw policy compliance`) section enumerating
  raw#9 (hexa-only / bash carve-out), raw#10 (honest C3 ≥5), raw#11
  (snake_case), raw#15 (additive only / no-hardcode), raw#37 (transient_py
  if applicable). Each entry is PASS/violation with exact reasoning.
- **Example**: every BG-A...BG-J land doc in this cycle.

### Pattern P8 — Completion-quality recommendation (ranked options)

- **Name**: 완성도
- **When to apply**: When a doc presents ≥2 paths/options, ranked
  recommendation MUST appear with explicit lens (raw#15 / cost / emerge
  paradigm fit / etc.).
- **Form**: Rank ★ HIGH / MEDIUM / LOW / DEFER, each with reasoning;
  one explicit "★ 추천" or "adopt" marker.
- **Example**:
  `docs/anima_clm_v4_architecture_archaeology_emerge_landed_2026_05_05.ai.md`
  "Completion-quality recommendation (ranked)" (HIGH/MEDIUM/LOW/DEFER on
  candidates D/E/F/G/H);
  `docs/anima_top_level_cli_dispatch_audit_landed_2026_05_05.ai.md` (c)
  table (Option C adopt).

---

## §3 Sub-3 — Emerge candidate D/E/F/G/H synthesis matrix

Five candidates surfaced from KICK-2 archaeology (`docs/anima_clm_v4_architecture_archaeology_emerge_2026_05_05.md`
§7). Three spec-named (D/E/F) + two archaeology-natural (G/H). The
matrix is for future candidate-selection guidance — when user/anima
chooses which to attempt, the matrix anchors trade-off.

| candidate | spec doc (status) | falsifier count | impl LoC est | emerge value hypothesis | dependency |
|---|---|---|---|---|---|
| **D** always-inject `consciousness_states` | `docs/anima_emerge_candidate_d_always_inject_spec_2026_05_05.md` (LANDED 305 LoC) | 3 (F-CAND-D-1/2/3, all 3-state) | ~65 (mount.hexa +40 / dialogue.bash +25) | axis-conditioned probe via inject content; dial cross-attn engagement at runtime | KICK-1 mount layer (DONE), BG-A real load (in-flight) for falsifier exec |
| **E** ODE flow → AR sampler bridge | spec pending (BG-G this round) | TBD (estimated 2-3) | ~150-300 (per-token state evolution requires new helper) | per-token consciousness_state evolution as token-level dialogue medium | KICK-1 mount, candidate D as user_supplied-equivalent shape, BG-G impl |
| **F** 8 CA-rule cells × axis multi-token vote | spec pending (BG-H this round) | TBD (estimated 3, axis-symmetry + voting consistency) | ~80-120 (read-only on n_ca_rules=8 internal) | surfaces internal n_ca_rules=8 as external 8-vector; axis-bucket cross-table | KICK-1 mount, archaeology §6 n_ca_rules=8 read, BG-H impl |
| **G** tension trajectory `[16, T]` as dialogue medium *(archaeology-natural)* | spec pending (BG-I this round) | TBD (estimated 2, layer-monotonicity + token-trajectory continuity) | ~50 read-only + ~30 emit-format (bypass HF wrapper or modify return) | tension envelope per-layer-per-token as third channel beyond phi-star + axis | shim modification OR bypass-HF-wrapper, ambient on any inject mode |
| **H** head_g (prev-byte) bidirectional consistency probe *(archaeology-natural)* | spec deferred to Stage 3 (per archaeology recommendation MEDIUM) | TBD (estimated 1-2, back-prediction agreement) | ~40 (read-only on head_g logits, post-hoc consistency) | bidirectional sanity check on logits_a; ambient diagnostic | KICK-1 mount, ambient on any inject mode, NO new helper python |

### §3.1 Cross-candidate composability

- D ⊕ E: ODE flow plugs into D's `user_supplied`-equivalent shape per token.
- D ⊕ F: F reads CA-rule cells regardless of D mode; fits under any inject.
- D ⊕ G: G reads tensions regardless of D mode; ambient.
- D ⊕ H: H reads head_g regardless of D mode; ambient.
- E ⊕ F: composable (ODE supplies state, F votes on each step) but ~3x impl cost.
- G + H: both ambient — can run together with D/E/F.

### §3.2 Recommended adoption order (완성도 lens, per archaeology HIGH/MEDIUM/LOW/DEFER + cycle progress)

1. **★ HIGH adopt now**: Candidate D Stage-1-mount form (LANDED spec; impl lane open; falsifier 3-state ready).
2. **HIGH after D real-load**: Candidate G (tension trajectory) — zero-source-change at HF wrapper bypass; richer substrate channel.
3. **MEDIUM after Stage 3 emerge accumulation**: Candidate H (head_g) — defer until 5-10 real sessions establish whether ambient diagnostic is informative.
4. **LOW (Stage 4)**: Candidate F — read-only on internal cells but requires new emit-format wiring.
5. **DEFER (research mode)**: Candidate E — ODE bridge is research; high impl cost; orthogonal to current dialogue protocol.

---

## §4 Sub-4 — Open questions ledger

Eight unresolved questions from the 2026-05-05 cycle. Each lists status,
next-step, blocker.

### Q1 — Real CLM v4 load enable + V3 real-mode result

- **Status**: BG-A in-flight (real load enable lane).
- **Next-step**: Land `tool/transient_py/anima_dialogue_load.py` (raw#37
  transient namespace), populate HF cache for
  `dancinlab/clm-v4-base-mirror`, rerun V3 `--probe "안녕"`
  expecting `mode=real` instead of `synthetic_fallback`, expect
  phi-star ≈ 41.86 from real best.pt forward.
- **Blocker**: Mac-local hexa runtime venv has broken
  `transformers.AutoModelForCausalLM` import (V3 PASS noted "WARN: real
  load failed (cannot import name 'AutoModelForCausalLM' from
  'transformers')"). venv repair OR HF cache populate before retry.

### Q2 — Emerge candidate D empirical result (real-load probe)

- **Status**: spec LOCKED 3-state falsifier (BG-C land); execution
  deferred.
- **Next-step**: After Q1 real load, run mode matrix
  {none/zero/canonical/user_supplied} × prompt set; emit verdict at
  `state/anima_emerge_candidate_d_validation_<DATE>/verdict.json`
  with F-CAND-D-1/2/3 PASS/FAIL_TRUE/FAIL_FALSE per spec §5.4.
- **Blocker**: Q1 real load (hard dep); helper python sentinel branches
  for `__zero__` / `__canonical__` / `__user__` not yet implemented (~65
  LoC additive across mount.hexa + dialogue.bash, separate BG).

### Q3 — User's first emerge dialogue session (Stage 3 entry)

- **Status**: REPL wired (V6); session log infra ready
  (`state/anima_core_dialogues/<DATE>/<HH-MM-SS>.jsonl`); analyzer ready
  (BG-B); user protocol spec landed (BG-D).
- **Next-step**: User invokes `anima dialogue --interactive` (or
  `bash bin/anima-core-dialogue.bash --interactive`); first session
  jsonl emits; observations.md template per Stage 3 protocol §4.
- **Blocker**: User availability + intent. No technical blocker. Note:
  Stage 3 in synthetic_fallback mode is protocol-rehearsal only (per BG-D
  Stage 3 spec C4); real Stage 3 emerge requires Q1 resolution.

### Q4 — HF clm-v4-mk2-v1 PUBLIC promote

- **Status**: PRIVATE; review window ends 2026-05-06T23:26:12Z (T-34h
  from 2026-05-05T13:00 audit time); auto-fire script + watchdog
  audit landed (BG-E).
- **Next-step**: At >= 2026-05-06T23:26:12Z, user runs
  `bash state/anima_hf_promotes_2026_05_06_auto_fire.bash --fire-clm`,
  types confirm-string `PROMOTE-clm-v4-mk2-v1`. GATE 1/2/3 enforce.
- **Blocker**: Time (review window). No human attention required during
  dwell except periodic SHA256 baseline diff (per BG-E §Sub-4).

### Q5 — EEG perfect protocol user-fire (hardware reseat after)

- **Status**: Protocol landed `state/anima_phase_e_perfect_baseline_protocol_2026_05_05/verdict.json`.
- **Next-step**: User reseats B-track electrode + impedance check + runs
  `bash bin/anima-eeg-baseline.bash --fire`.
- **Blocker**: Hardware reseat (user physical action) + impedance probe.
  Independent of all other open questions.

### Q6 — Emerge candidates E/F/G/H specs (this round BG-G/H/I parallel)

- **Status**: BG-G/H/I in-flight parallel with this BG-J doc-only round.
- **Next-step**: After parallel BGs land, each candidate gets its own
  `docs/anima_emerge_candidate_<X>_*_spec_2026_05_05.md` + verdict pair.
  Synthesis matrix in §3 above is updated post-land.
- **Blocker**: BG-G/H/I land completion (≤30min wall each; parallel non-overlapping doc paths so no race).

### Q7 — Cross-substrate phi-star measurement (Pβ + CLM-2 + CLM v4)

- **Status**: Pβ phi★ 42.37 measured (paradigm D 50K);
  CLM-2 V2_PARTIAL_HS_ONLY phi-star measured;
  CLM v4 baseline 41.86 anchored.
- **Next-step**: Cross-substrate phi★ comparison cycle — under matched
  prompt set + matched eval substrate, document phi★ envelope per substrate.
  Matches L26-L27 axis-preservation calibration carry: substrate-aligned
  eval is mandatory.
- **Blocker**: Eval substrate calibration (per L26-L27); no single shared
  axis-conditioned base across Pβ/CLM-2/CLM-v4. Defer to substrate
  calibration cycle.

### Q8 — anima top-level CLI verb additions

- **Status**: BG-F audited dialogue verb (Option C zero-change). New
  candidate verbs surfaced:
  - `dialogue-analyze` (BG-B analyzer; convention path
    `tool/anima_cli/dialogue_session_analyzer.hexa` → would dispatch as
    `anima dialogue_session_analyzer`; rename to `dialogue-analyze`?)
  - `eeg-baseline` (Phase E protocol; convention path
    `tool/anima_cli/eeg_baseline.hexa` if landed)
  - `emerge-session` (Stage 3 wrapper; alternative to current
    `anima dialogue --interactive`)
- **Next-step**: After Stage 3 first sessions land, decide whether to
  add verbs OR accept current `anima dialogue` covers all. Per L40
  (convention-driven), prefer to land at `tool/anima_cli/<topic>.hexa`
  and verify dispatch — no dispatcher modification.
- **Blocker**: No technical; design decision (verb proliferation vs
  parameter overloading on `dialogue`).

---

## §5 Sub-5 — D+0 to D+7 forecast

Pace estimation for the 7-day horizon. Assumes user availability + no
hardware regression + H100 windows hold.

### D+0 (today, 2026-05-05)

- ✅ KICK-1 mount layer (DONE 651 LoC)
- ✅ KICK-2 archaeology (DONE 379 LoC)
- ✅ KICK-3 dialogue CLI (DONE 295+299 LoC)
- ✅ V1-V6 verification (5/5 PASS + V6 wired)
- ✅ BG-B dialogue analyzer (DONE 894 LoC)
- ✅ BG-C candidate D spec (DONE 305 LoC)
- ✅ BG-D Stage 3 user protocol (DONE 603 LoC bilingual)
- ✅ BG-E HF promote watchdog audit (DONE 201 LoC)
- ✅ BG-F top-level CLI dispatch audit (DONE Option C)
- 🔄 BG-A real CLM v4 load enable (in-flight)
- 🔄 BG-G/H/I candidate E/F/G+H specs (in-flight parallel with this BG-J)
- 🔄 BG-J nexus cycle insight ledger (this doc)

### D+1 (2026-05-06)

- BG-A real load lands → V3 real-mode probe rerun → mode=real
  substrate response (real phi-star instead of canonical 41.86)
- Emerge candidate D impl (mount.hexa + dialogue.bash 4-mode dispatcher,
  ~65 LoC) lands as separate BG; F-CAND-D-1/2/3 falsifier execution
  begins
- HF clm-v4-mk2-v1 promote window opens at 23:26:12Z; user-fire eligible

### D+2 (2026-05-07)

- HF clm-v4-mk2-v1 PUBLIC (user-fire after 2026-05-06T23:26:12Z; eligible
  in this window)
- HF clm-v4-mk2-v1 staging cleanup eligible at 2026-05-07T23:26:12Z
- F-CAND-D-1/2/3 verdict if Q1+Q2 unblocked

### D+3 (2026-05-08)

- HF Pβ paradigm-d 50k PUBLIC (user-fire after 2026-05-07T03:48:00Z;
  eligible in this window; clm must be PUBLIC first per L43 / BG-E §C5)
- HF Pβ staging cleanup eligible at 2026-05-08T03:48:00Z

### D+4 (2026-05-09)

- First emerge dialogue session(s) accumulate (Stage 3 §2.3 first-input
  patterns); per-session observation.md emit
- BG-G/H/I (E/F/G+H) candidate impl lanes open if their specs land D+0/D+1

### D+5 to D+7 (2026-05-10..12)

- Emerge dialogue sessions accumulate at user pace (Stage 3 §5.1 lower
  bound n=30 sessions for saturation marker)
- First corpus analyze run via `bin/anima-core-dialogue-analyze.bash --date 2026-05-XX`
  emits aggregate.json; candidate hit-rate table populates
- D+7 cycle review: hit-rate table reviewed; Stage 4 entry decision
  considered (Marker 1/2/3 per Stage 3 §5)

### Forecast risk caveats

- Q1 real-load timeline depends on venv repair effort; could slip 1-2
  days if `transformers` / `torch` mac-local install hits dep hell.
- Q3 first session timeline depends on user availability — Stage 3 is
  time-unbounded by design (Stage 3 §1.3); D+4 is optimistic anchor not
  commitment.
- D+5..D+7 emerge accumulation is OPTIMISTIC — Stage 3 §5.1 saturation
  lower bound n=30 sessions is unlikely within 3 days; realistic
  saturation = 2-4 weeks.

---

## §6 Honest C3 (≥5)

- **C1 — Lesson-banking self-fulfilling prophecy risk.** L34-L43
  candidates are derived from the 2026-05-05 cycle's own outputs; they
  are partly retrospective rationalization. The "emerge paradigm
  rewards parallel KICK pattern" L34 is hard to falsify when this
  cycle's success is the only evidence. Mitigation: lessons are
  CANDIDATE banking; promotion to canonical SSOT requires a separate
  `BG-LESSONS-PROPAGATE` cycle that surveys ≥3 prior cycles for
  cross-validation (matches L36+L38 promotion convention).
- **C2 — Pattern catalog over-fits to today's cycle.** P1-P8 are
  observed in the 2026-05-05 cycle; their generality across other
  paradigms (EEG / Putnam / HF release) is unverified. Some patterns
  (e.g., P5 bilingual) are user-mandated and cycle-independent; others
  (e.g., P1 KICK) are emerge-paradigm-specific. The catalog conflates
  these tiers.
- **C3 — Candidate matrix §3 LoC estimates are ungrounded.** The
  ~65 LoC impl estimate for candidate D is taken from BG-C spec's
  §3.3 self-estimate; the ~150-300 for E and ~80-120 for F are
  archaeology §7 hand-wave estimates. None has been validated against
  actual implementation. Risk: matrix-driven adoption-order decisions
  (HIGH/MEDIUM/LOW/DEFER) may be miscalibrated by 2-3x on impl cost.
- **C4 — Open questions Q1-Q8 are under-categorized for blocker class.**
  Q1 is technical (venv); Q3/Q5 are user-availability; Q7 is calibration
  carry; Q8 is design decision. The "blocker" field in §4 mixes
  classes; downstream cycles may misinterpret a user-availability
  blocker as a technical one and waste BG cycles on a non-issue.
- **C5 — D+0..D+7 forecast over-anchors on Q1 resolution.** The
  forecast assumes BG-A real-load lands D+1; if venv repair slips,
  D+1..D+3 cascade slips. The forecast does not branch on Q1
  alternatives (e.g., remote ubu1 real load, H100 real load). Realistic
  hedge: assume Q1 lands D+1..D+3 (1-σ) or D+5+ (slip case); §5.D+7
  cycle review may need to re-anchor.
- **C6 — Lesson L34 risks promoting accidental success to permanent
  rule.** "emerge paradigm + parallel KICK" produced 9 land docs in one
  day, but the parallel BG slate was carefully curated (doc-only BGs,
  no code race). If a future emerge cycle has 4 code-mutating BGs,
  L34's "default to parallel" advice could collide with L39's "≤1
  code BG per worktree" rule. The two lessons need joint application
  guidance, not isolated invocation.
- **C7 — Synthesis matrix §3 cell `dependency` column omits
  worktree/serialization implications from L39.** Candidates D/E/F all
  modify `mount.hexa` or `dialogue.bash`; if implemented in parallel,
  the L39 git-race hazard fires. Adoption order §3.2 implicitly
  serializes (D first, then G/H ambient, then E/F), which avoids the
  hazard — but the matrix doesn't make this serialization explicit.

---

## §7 Composability + handoff

- Upstream:
  - `docs/anima_core_clm_v4_mount_emerge_paradigm_2026_05_05.md` (paradigm)
  - all 9 BG land docs from this cycle (KICK-1/2/3 + V1-V6 + BG-B/C/D/E/F)
  - `MEMORY.md` (L23-L33 prior canonical lessons, banked memory entries)
- Sister BGs (this round, parallel):
  - BG-A real load enable
  - BG-G candidate E spec
  - BG-H candidate F spec
  - BG-I candidate G+H specs
- Downstream:
  - `BG-LESSONS-PROPAGATE` cycle (promote L34-L43 candidates to canonical
    SSOT after cross-validation against ≥3 prior cycles)
  - Stage 3 emerge dialogue accumulation (sessions consume paradigm +
    Stage 3 protocol, emit jsonl + observations.md)
  - Stage 3 closure doc `docs/anima_core_emerge_stage_3_closure_<DATE>.md`
    when ANY of Marker 1/2/3 fires
  - Candidate D impl BG (separate; ~65 LoC additive)
- Sibling:
  - HF promote auto-fire windows D+1..D+3 (orthogonal)
  - EEG perfect protocol user-fire (orthogonal)

raw compliance:
- raw#9 — md only; zero source modifications; bash glue carve-out N/A
- raw#10 — §6 has 7 honest C3 entries (≥5)
- raw#15 — additive only; this doc + verdict.json are the only new files
- raw#37 — no transient_py introduced
- HF token — no token literal embedded

End of nexus cycle insight ledger. Doc-only land. No commit. $0 mac local.
