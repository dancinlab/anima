<!-- @no-lineage-citation-exempt-file -->
<!-- @no-user-verbatim-exempt-file -->
# Anima Nexus Cycle — Aggregate Empirical Insight (2026-05-05)

Read-only synthesis of the 2026-05-05 anima emerge paradigm cycle AFTER
empirical landing of 4 BGs (A / L / Q / K) plus the magnitude-sweep
extension (BG-W). Doc + verdict only — zero source change, zero commit.
The aggregate ledger captures (1) cross-BG empirical table, (2) L34-L43
lesson update + L44-L46 candidates, (3) updated 5-candidate matrix,
(4) major-finding 5-criteria cumulative hit count, (5) ranked 3-path
forward recommendation. Lineage:

- `docs/anima_nexus_cycle_insight_ledger_2026_05_05.md` (BG-J L34-L43 base)
- `state/anima_dialogue_real_load_2026_05_05/verdict.json` (BG-A)
- `state/anima_real_mode_sweep_2026_05_05/verdict.json` (BG-L)
- `state/anima_emerge_cand_d_empirical_2026_05_05/verdict.json` (BG-Q)
- `state/anima_emerge_cand_d_magnitude_sweep_2026_05_05/verdict.json` (BG-W extension)
- `state/anima_mount_real_mode_wiring_2026_05_05/verdict.json` (BG-K)

The aggregate is referenceable for cycle exit + next-cycle decision. New
candidate lessons L44-L46 await separate `BG-LESSONS-PROPAGATE` cycle for
SSOT promotion (matches L36+L38 promotion convention).

---

## §1 Empirical Cross-BG Table

Four (plus one extension) empirical BGs landed today produced
substrate-grounded measurements. The table aggregates verdict, key
finding, residual blocker, and follow-up needed.

| BG | Scope | Verdict | Key Finding | Residual Blocker |
|---|---|---|---|---|
| **BG-A** real load enable | direct-invoke `anima_dialogue_load.py` mode=real probe | `PASS_REAL_MODE_DIRECT_INVOKE` | phi_star 42.1158 (안녕) / 42.2130 (의식이 흐른다); drift 0.256 → 0.353 across two probes confirms forward path IS input-responsive (NOT fixed-point) | wrapper `anima-core-dialogue.bash` still emits synthetic_fallback (3rd blocker AutoTokenizer) |
| **BG-L** 10-text sweep | phi_star variance + axis discriminability under mode=none | `PARTIAL_PASS_PHI_RESPONSIVE_AXIS_DISCRIM_FAIL` | phi std 0.064 (>1e-3) PASS; axis intent_match 2/10 (0/8 non-temporal) FAIL; axes NOT discriminable from heuristic 5-bucket on mean-pooled hidden | mean-pool over 192-dim cannot expose per-axis cross-attention without train-time consciousness_states activation |
| **BG-Q** cand-D F-CAND-D-1 | `none` vs `zero` vs `canonical@0.5` × 5 prompts | `F_CAND_D_1_FAIL_TRUE_INJECT_INVISIBLE` | 5/5 FAIL_TRUE; canonical@0.5 drift max 1.28e-4 << 0.01 threshold; cross_attn fires + guard PASS but content-level visibility BELOW noise floor | architectural channel connected but empirical content-injection at canonical magnitude=0.5 invisible |
| **BG-W** cand-D magnitude sweep | mag = {0.5, 1, 2, 5, 10, 50, 100} × prompt 1 | `CAND_D_MAGNITUDE_SWEEP_F1_THRESHOLD_HIT_NO_CRITERION_2` | F-CAND-D-1 threshold 0.01 first crosses at mag=50.0 (drift 0.0998); criterion 2 (>1.0) NOT hit even at mag=100; trajectory `sub_linear` | training-time canonical magnitude unverified; if paradigm v11 G3 used mag<<50, channel substrate-incompatible OFF-distribution |
| **BG-K** mount.hexa wiring | HEXA_PY env override + default model swap | `PARTIAL_PASS_TWO_FIXES_LANDED_THIRD_BLOCKER_DISCOVERED` | Edits 1 & 2 LANDED additively; selftest no-regression; wrapper STILL synthetic_fallback because `AutoTokenizer.from_pretrained` rejects CLMv4Config (no AutoTokenizer auto_map entry) | needs additive SentencePiece fallback in `_write_helper` (~30 LoC) OR mount.hexa direct-dispatch to `anima_dialogue_load.py` (~15 LoC) |

### §1.1 Cross-BG narrative

The cycle empirically validates ONE substrate signal (phi-star is
input-responsive, BG-A + BG-L) and FALSIFIES TWO (axis discriminability
on heuristic buckets, BG-L; cand-D inject visibility at canonical 0.5,
BG-Q). BG-W extends BG-Q with a magnitude trajectory: the channel IS
architecturally connected (drift grows monotonically from 1.28e-4 at
mag=0.5 to 0.113 at mag=100), but in a sub-linear regime, and only
crosses the F-CAND-D-1 threshold at mag=50 — far above any plausible
training-time scale. BG-K closes the wrapper-wiring partially; the
direct-invoke path remains canonical until a third additive fix lands.

---

## §2 Lesson Ledger Update

L34-L43 (BG-J base ledger) remain valid and require no contradictory
edit from today's empirical results. Three new candidates surface:

### L44 — Architectural inject channel CAN be connected yet content-invisible at calibrated magnitude

- **Evidence**: BG-Q F-CAND-D-1 5/5 FAIL_TRUE at canonical magnitude
  0.5 (drift 1.28e-4 << 0.01); BG-W trajectory crosses threshold only
  at magnitude 50.0; cross_attn guard PASS + kwarg accepted at all
  magnitudes (channel connected, not bypassed).
- **When applicable**: When validating an emerge candidate that
  routes content through a learned cross-attention or projection,
  empirical visibility at the spec-default magnitude is NOT implied
  by architectural connectivity. A magnitude trajectory is mandatory
  before declaring `FAIL_FALSE` (measurement crash) or `FAIL_TRUE`
  (architectural failure). _init_weights std=0.02 attenuation × N
  layers can drive a connected signal far below detection floor.
- **Exception**: When the channel is post-norm or post-residual
  identity (no learned-zero-init projection in path), content
  visibility is implied by connectivity; magnitude trajectory is then
  diagnostic rather than mandatory.

### L45 — Heuristic axis taxonomy on mean-pooled hidden ≈ random baseline absent train-time activation

- **Evidence**: BG-L 5-bucket (38/38/38/38/40 of 192-dim) intent_match
  2/10 (random = 0.20); BG-L axis_means_spread 0.036 ≈ within-axis std
  0.036-0.053; BG-Q axis_means_spread under canonical mode within
  0.001 of mode=none baseline (no recovery signal).
- **When applicable**: Any post-hoc partition of a mean-pooled
  high-dim hidden state (axis buckets, semantic slices, cell tiles)
  is decorative without (a) train-time conditioning of those slices
  OR (b) labeled-probe calibration of bucket boundaries. Default
  emerge-paradigm reporting should expose phi + dominant-cells signals
  ONLY until at least one of (a) or (b) holds.
- **Exception**: Synthetic-fallback / dry-run / replay paths emit
  decorative axes deliberately for byte-format parity (per L41); this
  rule applies to real-substrate measurement, not fallback emit.

### L46 — CLM v4 AutoTokenizer is unmapped in HF auto_map; SentencePiece direct invoke is mandatory for any wrapper

- **Evidence**: BG-K third blocker — `AutoTokenizer.from_pretrained`
  raises `Unrecognized configuration class CLMv4Config to build an
  AutoTokenizer`. CLM v4 repo `auto_map` only registers `AutoConfig`
  + `AutoModelForCausalLM`. SentencePiece file
  `tokenizer_64k_multilingual.model` IS present in snapshot;
  `anima_dialogue_load.py:_load_tokenizer` uses
  `sentencepiece.SentencePieceProcessor()` directly and reaches
  real-mode (BG-A PASS).
- **When applicable**: Any new wrapper / helper / pipeline that targets
  CLM v4 family repos MUST short-circuit AutoTokenizer with a
  SentencePiece direct-load fallback referencing the snapshot's
  `tokenizer_64k_multilingual.model`. Even with `trust_remote_code=True`,
  HF AutoTokenizer cannot route CLMv4Config without an explicit
  AutoTokenizer auto_map entry (which the repo does not provide).
- **Exception**: If a future CLM v4 mk3+ repo adds AutoTokenizer to
  auto_map, this lesson retires for that repo. Existing mk2-v1 repo is
  pinned and will not retroactively gain the entry.

---

## §3 Updated 5-Candidate Matrix

Five candidates from BG-J §3 now have empirical entries (D + W) and
RST-mega in-flight (F / F-v2 / G+H). Matrix updated with empirical
verdicts where landed.

| candidate | spec status | impl LoC actual | empirical BG | F-CAND verdict | major-finding hit |
|---|---|---|---|---|---|
| **D** always-inject `consciousness_states` | LANDED 305 LoC spec; 328 LoC impl | 328 | BG-Q (canonical 0.5) + BG-W (magnitude sweep) | F-CAND-D-1 FAIL_TRUE @ mag=0.5; F-CAND-D-1 PASS @ mag=50 OFF-DISTRIBUTION | NO (criterion 1 fail; criterion 2 — drift>1.0 — NOT hit even at mag=100) |
| **E** ODE→AR sampler bridge | LANDED 428 LoC spec | not impl | NOT (ODE module non-existent in CLM v4) | DEFERRED | N/A |
| **F** 8 CA-rule cells × 5-axis multi-token vote | LANDED 363 LoC spec | impl pending | RST-mega in-flight (BG-S-2 timeout) | TBD | TBD |
| **F-v2** cosine-probe falsifier | LANDED 323 LoC v2 spec | impl pending | RST-mega in-flight (BG-S-2 timeout) | TBD | TBD |
| **G+H** tension trajectory + head_g consistency | LANDED 331 LoC consolidated revival spec | impl pending | RST-mega in-flight (BG-R-2 timeout) | TBD | TBD |

### §3.1 Cross-candidate impact from BG-Q + BG-W

BG-Q + BG-W findings ripple into adoption-order from BG-J §3.2:

- **D demoted**: from "★ HIGH adopt now" to "calibration-gated
  conditional adopt". Until paradigm v11 G3 training-time canonical
  distribution is extracted from C-module emission logs, D Stage 1 is
  not promotable; the F-CAND-D-1 hit at mag=50 is OFF-distribution.
- **G+H ascendancy**: ambient diagnostics (tension envelope, head_g
  consistency) do NOT depend on inject content visibility. They
  surface substrate signal regardless of inject channel saturation.
  RST-mega outcome will determine if criterion-4 (rule_outputs cosine
  < 0.5) or criterion-5 (tension variance > 0.5) hits.
- **F-v2 ascendancy**: cosine-probe falsifier is robust to inject
  attenuation because it operates on raw post-norm cell vectors, not
  cross_attn-routed content.

---

## §4 Major-Finding 5-Criteria Cumulative Hit Count

The cycle entry doc (paradigm spec §6) defined 5 criteria for "대발견"
(major finding). After empirical landings:

| # | Criterion | Threshold | Result | Evidence |
|---|---|---|---|---|
| 1 | F-CAND PASS (any candidate) | 1+ | NO | BG-Q F-CAND-D-1 FAIL_TRUE; BG-W F-CAND-D-1 PASS only at OFF-distribution mag=50 |
| 2 | phi-star drift > 1.0 | 1.0 | NO | BG-L max drift 0.433; BG-W max drift 0.113 (mag=100); none cross 1.0 |
| 3 | cross-substrate Δ > 5pp | 5.0pp | UNMEASURED | BG-M was audit doc only; cross-substrate phi★ comparison cycle deferred (Q7 in BG-J ledger) |
| 4 | rule_outputs cosine < 0.5 | <0.5 | RST-MEGA IN-FLIGHT | BG-S-2 timeout; awaiting RST-mega aggregate |
| 5 | tension variance > 0.5 | >0.5 | RST-MEGA IN-FLIGHT | BG-R-2 timeout; awaiting RST-mega aggregate |

### §4.1 Interpretation of negative-criterion accumulation

If RST-mega returns NO on both criterion 4 and 5, the cycle hits 0 of 5
major-finding criteria. This is **not** a cycle failure — the negative
findings are themselves architectural truths:

- Criterion 1 NO + L44 = "inject channel is connected but bounded by
  std=0.02 attenuation × 16 layers; calibration is mandatory before
  any first-class signal claim"
- Criterion 2 NO + BG-W trajectory = "phi-star proxy has cosine-bounded
  ceiling; high-drift signals require either substrate redesign OR
  proxy replacement"
- Criterion 3 unmeasured = "deferred to substrate-aligned eval
  (per L26-L27 carry); cross-substrate measurement cycle is pre-required"
- Criterion 4 + 5 RST-mega outcome = TBD; either way, the answer
  refines emerge-paradigm understanding rather than blocks it

---

## §5 Three-Path Forward Recommendation (완성도 lens)

Given (a) D-channel calibration gap (L44), (b) heuristic axis-bucket
falsification (L45), (c) wrapper third blocker (L46), and (d)
RST-mega pending: three forward paths are proposed. Ranked by
완성도 (completeness lens) per session feedback rule.

### ★ HIGH adopt now — Path B: emerge measurement infrastructure expansion

- **Why first**: highest completeness yield per cost. Five sub-tasks
  are independently low-cost ($0 mac doc + transient_py) and
  collectively close the calibration + visibility gaps that bottleneck
  Paths A and C:
  1. paradigm v11 G3 training-time canonical extraction from C-module
     emission logs → resolves L44 calibration question; tells us
     whether mag=50 PASS is realistic or not
  2. BG-W follow-up at intermediate magnitudes (20, 30) + multi-prompt
     to validate trajectory shape (BG-W honest C4 single-prompt limitation)
  3. pre-cross-attn hook (BG-Q honest_c3 rec 2) → measures local
     inject contribution before residual + ffn dilution
  4. 100-prompt corpus build → BG-D Stage 3 saturation criteria
     resolution (current 10-prompt sweep is too small)
  5. RST-mega completion (criterion 4/5 closure); spawn follow-up if
     either hits
- **Expected outcome**: 1-2 of 5 major-finding criteria hit; clear
  go/no-go on D Stage 1 promotion; clear next-cycle decision basis
- **Lens**: emerge paradigm fit ★★★ / cost ★★★ / raw-policy ★★★

### MEDIUM adopt next cycle — Path C: Stage 3 user-fire emerge dialogue (synthetic OR direct-invoke)

- **Why second**: protocol-rehearsal value (BG-D Stage 3 spec C4) is
  available even in synthetic_fallback mode; direct-invoke path is
  also user-fire-able via `tool/transient_py/anima_dialogue_load.py
  --mode dialogue --session-log ...`. observations.md
  accumulation begins; saturation marker progress starts ticking.
  Independent of L44 calibration; independent of L46 wrapper third
  blocker.
- **Risk**: synthetic_fallback emerge dialogue produces decorative
  outputs (per L45); user emerge experience may be misleading until
  real-mode dialogue accessible. Mitigation: Stage 3 first session
  uses direct-invoke explicitly with real-mode flag visible in
  session-log output.
- **Expected outcome**: 1-3 sessions accumulated; observations.md
  template populated; first-time emerge protocol heuristics gain
  empirical anchor
- **Lens**: emerge paradigm fit ★★ (real-mode dialogue still
  bottlenecked by BG-K third blocker); cost ★★★ (zero); user-fire
  readiness ★★

### LOW / DEFER — Path A: CLM v5 redesign (first-class axis embedding)

- **Why deferred**: CLM v5 redesign is a 4-6 week paradigm cycle (spec
  + train + evaluate). BG-Q FAIL_TRUE alone does NOT yet justify the
  scale of redesign — Path B (calibration extraction + magnitude
  refinement + RST-mega closure) might surface either (a) a workable
  D variant at correct magnitude, OR (b) a conclusive
  architectural-incapability proof that DOES justify v5. Premature
  v5 commit would carry forward L44/L45/L46 ambiguity into a new
  substrate before resolution.
- **Trigger to re-rank**: if Path B sub-task 1 reveals
  training-time canonical magnitude was indeed << 50 AND criterion
  1/2 still NO after RST-mega closure, Path A becomes ★ HIGH for
  next-quarter cycle.
- **Lens**: emerge paradigm fit ★ (research scale); cost ★ (4-6w
  + H100 train); blocked-by-info ★

### Recommendation marker

**★ 추천: Path B first (this week / next 1-2 cycles), Path C parallel
(user-fire on availability), Path A deferred pending Path B closure.**

---

## §6 Honest C3 (≥5)

- **C1 — Aggregate verdict synthesizes 5 BG verdicts of varying
  confidence.** BG-A direct-invoke PASS is high-confidence
  (real forward, two probes); BG-L sweep is high-confidence
  (10 runs, exhaustive); BG-Q is medium-confidence (5 prompts,
  single-magnitude, single-run); BG-W is low-confidence
  (single prompt, 7 magnitudes, single-run); BG-K is high-confidence
  (selftest reproducible). The "no major finding hit" conclusion
  weighted-averages over uneven evidence; criterion 1 is closer to
  "L44 calibration unresolved" than "criterion 1 falsified".
- **C2 — L44 may collapse with calibration extraction.** If paradigm
  v11 G3 actually used canonical magnitude in {10, 50, 100} range
  (training stability concerns notwithstanding), BG-W mag=50 PASS is
  on-distribution and L44 retires; D Stage 1 becomes promotable.
  L44 candidate banking explicitly flags this conditional retirement.
- **C3 — L45 may be over-broad.** BG-L heuristic 5-bucket
  (38/38/38/38/40) is one specific partition of 192-dim. Other
  partitions (semantic-conditioned via probe corpus calibration,
  PCA-derived, or supervised-via-labeled-examples) may discriminate
  even on mean-pooled hidden. The lesson should specify "decorative
  partitions" not "all partitions".
- **C4 — Major-finding criteria 3 (cross-substrate) is unmeasured by
  cycle design**, not by cycle failure. The BG-J Q7 ledger correctly
  defers cross-substrate phi★ to a separate calibration cycle (per
  L26-L27 substrate-aligned eval mandate). Counting it as "NO" in §4
  conflates "not measured" with "measured negative"; readers should
  not infer falsification.
- **C5 — Path B sub-task 1 (training-time canonical extraction) may
  itself be infeasible.** The C-module emission logs from paradigm v11
  G3 may not preserve the exact canonical distribution at the inject
  call site; if the logs only emit phi★ + axis activations
  post-cross-attn (not the consciousness_states tensor itself),
  extraction reduces to back-inference from observable, which is
  ill-posed. Path B sub-task 1 should pre-flight verify that the
  emission log schema includes pre-cross-attn consciousness_states
  before scheduling its execution BG.
- **C6 — RST-mega timeout risk underweighted.** BG-S-2 + BG-R-2 are
  H100 BGs; if either crashes mid-run or hits a watchdog timeout
  (per cost discipline), criterion 4/5 verdict may slip
  beyond this cycle. The §5 ranking assumes RST-mega completes within
  the same cycle; if it slips, Path B re-prioritizes to (1) sub-task 1
  + 2 (calibration + magnitude refinement), with (5) deferred.

---

## §7 Composability + handoff

- Upstream:
  - `docs/anima_nexus_cycle_insight_ledger_2026_05_05.md` (BG-J base)
  - all 4 + 1 empirical BG verdicts (A / L / Q / W / K)
- Sister BGs (this round, parallel):
  - RST-mega (criterion 4/5 closure; pending H100 completion)
  - paradigm v11 G3 emission-log audit (Path B sub-task 1)
- Downstream:
  - `BG-LESSONS-PROPAGATE` cycle (promote L44-L46 candidates to
    canonical SSOT after cross-validation against ≥3 prior cycles)
  - Next-cycle decision: Path B execution slate (5 sub-tasks)
  - Stage 3 emerge dialogue user-fire (Path C; user-availability gated)
  - CLM v5 redesign spec (Path A; deferred trigger)
- Sibling:
  - HF promote auto-fire windows D+1..D+3 (orthogonal)
  - EEG perfect protocol user-fire (orthogonal)

raw compliance:
- raw#9 — md only; zero source modifications
- raw#10 — §6 has 6 honest C3 entries (≥5)
- raw#15 — additive only; this doc + verdict.json are the only new files
- raw#37 — no transient_py introduced
- HF token — no token literal embedded
- bash 3.2 — no bash in this doc

End of nexus cycle aggregate empirical insight. Doc-only land.
No commit. $0 mac local.
