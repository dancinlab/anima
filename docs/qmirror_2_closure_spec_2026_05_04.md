# nexus.qmirror 2.0 — Closure Synthesis Spec (5-axes dispatch logic)

**Date:** 2026-05-04
**Author:** anima cycle agent (qmirror 2.0 closure synthesis spec author)
**Domain SSOT (parent):** `nexus/.roadmap.qmirror`
**qmirror 1.0 closure:** `anima/docs/nexus_qmirror_closure_2026_05_03.md` (8/8 conditional, ALREADY SHIPPED, immutable for purposes of this cycle)
**qmirror 2.0 axes spec:** `anima/docs/qmirror_2_axes_spec_2026_05_03.md` (5 ranked conditions cond.9–cond.13)
**Mode:** Spec only. NO execution this cycle. Closure synth fires when sister BG cond.11 / cond.12 / cond.13 land.
**raw#:** 9 STRICT (Mac → hexa only; this cycle creates 0 .py files),
          10 (5 honest C3 caveats embedded; see §6),
          15 (no personal paths in body of any artifact)

---

## 0. Executive summary

`nexus.qmirror` 1.0 closed 8/8 conditions on 2026-05-03 (entropy / Aer /
IBM CHSH existence / NIST QRNG / qmirror.chsh reproduction / IIT 4.0
byte-identical / cross-family RMSE / cross-vendor option β). qmirror 2.0
proposes 5 next-cycle axes (cond.9–cond.13) per the 2026-05-03 axes spec:

| cond  | axis (short)                              | falsifier        | substrate          | $    | wall    |
|-------|-------------------------------------------|------------------|--------------------|------|---------|
| 9     | quantum process tomography                | F-QM-2-TOMO-9    | Aer SV ≤4q         | $0   | 2 d     |
| 10    | GHZ-3 generation + Mermin witness         | F-QM-2-GHZ-10    | Aer SV 3q          | $0   | 1 d     |
| 11    | stabilizer measurement primitive (QEC)    | F-QM-2-STAB-11   | Aer SV 4q mid-meas | $0   | 1.5 d   |
| 12    | surface-code distance-3 toy logical \|0⟩  | F-QM-2-SURF-12   | Aer SV 17q         | $0   | 2 d     |
| 13    | CSCS chained sequential CHSH (2-pair)     | F-QM-2-CSCS-13   | Aer SV 4q (+opt $25 IBM) | $0–25 | 1.5 d |

**Status at this spec write time (2026-05-04):**
- ✅ cond.9 LANDED (PASS, fid_min=0.99918, 7/7 gates, $0)
- ✅ cond.10 LANDED (PASS, M=4.0 saturated, 30/30 trials, $0)
- 🔄 cond.11 sister BG running
- 🔄 cond.12 sister BG running
- 🔄 cond.13 sister BG running

**This document specifies:**
1. The closure verdict logic (5-axes → FULL / PARTIAL / DEFERRED).
2. The dispatch trigger (when the synth fires automatically vs manually).
3. The structure of `docs/qmirror_2_closure_2026_05_04.md` (the actual
   closure doc, written when synth fires).
4. The artifact mutations gated on closure (CHANGELOG / hexa.toml /
   registry.tsv / parent closure doc additive section / roadmap entry).
5. The new composite falsifier `F-QM-2-CLOSURE-1`.
6. 5 honest C3 caveats spanning the closure-spec layer.

This spec does NOT execute the closure; it defines the recipe. The
sibling tool `tool/qmirror_2_closure_synth.hexa` IS the dispatch logic
referenced in §3 and reads the 5 verdict files to compose the final
closure doc when invoked (manually or by a sister automation).

---

## 1. Closure verdict logic (5-axes → 3 verdicts)

### 1.1 Per-axis "MET" definition

For each of cond.9, cond.10, cond.11, cond.12, cond.13:

```
MET[cond.X] := exists(verdict_path[X]) AND
               jq -r .verdict verdict_path[X] in {"PASS", "MET", "MET_VIA_BAND_REVISE"}
```

The `MET_VIA_BAND_REVISE` slot is reserved (parallel to qmirror 1.0
cond.3 / cond.7). For qmirror 2.0 axes, all 5 conds are noiseless-Aer
falsifiers — band revision would not be physics-aware and SHOULD NOT
fire for cond.9–cond.13 default $0 path. The slot exists only for
cond.13 IF the optional $25 IBM hardware anchor is engaged AND the
hardware burst returns S < 2.7 (which would then mirror cond.3
post-hoc band rationale). See caveat #5 in §6.

### 1.2 Verdict path map

```
verdict_paths = {
  "cond.9":  "anima/state/qmirror_2_cond9_tomography_2026_05_03/verdict.json",
  "cond.10": "anima/state/qmirror_2_cond10_ghz_mermin_2026_05_03/verdict.json",
  "cond.11": "anima/state/qmirror_2_cond11_stabilizer_2026_05_04/verdict.json",
  "cond.12": "anima/state/qmirror_2_cond12_surface_2026_05_04/verdict.json",
  "cond.13": "anima/state/qmirror_2_cond13_cscs_2026_05_04/verdict.json"
}
```

Note: cond.9 and cond.10 directories carry the `2026_05_03` date stamp
because they landed 2026-05-03 (and 2026-05-04 UTC respectively per
verdict ts; directory name retained for SSOT contiguity). cond.11 /
cond.12 directories already exist at `_2026_05_04` per sister BG launch
(empty at this spec write time). cond.13 directory will be created by
its sister BG.

### 1.3 Composite verdict mapping

Let `n_pass = count of MET conds among {cond.9, cond.10, cond.11, cond.12, cond.13}`.

| n_pass | composite verdict                          | semver bump path    | publishability |
|--------|--------------------------------------------|---------------------|----------------|
| 5      | `qmirror_2_closure_FULL`                   | 1.0.x → 2.0.0       | publishable    |
| 3 or 4 | `qmirror_2_closure_PARTIAL`                | 1.0.x → 2.0.0-rc.1  | rc with caveats |
| ≤ 2    | `qmirror_2_closure_DEFERRED`               | NO bump (stay 1.0.x)| 2.0 backlog    |

**5/5:** All sister BG conds land PASS → `CLOSURE_FULL`. qmirror v2.0.0
ships. `hexa.toml` version line bumps. Closure doc written. Parent
1.0 closure doc gets additive 2.0 section appended.

**3-4/5:** Mixed — at least 3 conds PASS, with 1 or 2 FAIL/PENDING.
`CLOSURE_PARTIAL` ships qmirror v2.0.0-rc.1 (release candidate) with the
failing conds explicitly listed and rationale recorded. The 2 missing
axes go to qmirror 2.0 backlog with re-run plans documented in the
closure doc §7. Composite falsifier F-QM-2-CLOSURE-1 (see §5) PASSes
at this threshold (≥4) but only PARTIAL-classifies at exactly 3.

**≤ 2/5:** `CLOSURE_DEFERRED`. qmirror stays at v1.0.x. The 5 conds go
to the qmirror 2.0 spec for revision in a later cycle. Failing
conds get diagnosed (substrate gap, falsifier mis-spec, etc.). The
1.0 closure remains entirely intact (raw#10 caveat #3 in §6).

### 1.4 Special cases

**No-existence (file missing):** treat as `PENDING` (not PASS, not
FAIL). The synth tool emits `NEEDS_INPUT` if any verdict file is
absent; manual invocation can override with `--force-on-missing`
(treats missing as FAIL for verdict computation, useful if a sister BG
crashed and one wants to publish a 4/5 PARTIAL without waiting).

**Hardware anchor in cond.13:** if `verdict_paths["cond.13"]` contains
both `verdict_aer` and `verdict_hardware` keys (per cond.13 spec
optional $25 path), the synth requires `verdict_aer == PASS` for MET.
`verdict_hardware == FAIL` is an honest-disclosure note in the closure
doc but does NOT downgrade MET. Caveat #5 in §6 documents the
selection-bias risk this carries (mirrors cond.3 1.0 closure pain
exactly).

---

## 2. Dispatch trigger logic

### 2.1 Auto-dispatch

The synth tool `tool/qmirror_2_closure_synth.hexa` MAY be invoked
automatically by a sister anima cycle agent when the following
guards all hold:

1. All 5 verdict files exist (5/5 sister BGs reported back).
2. None of the 5 verdict files have been modified in the last 60
   seconds (hash-stable).
3. The current `qmirror/hexa.toml` version string is `1.0.x` (NOT
   already 2.0.x — prevents double-bump).
4. The marker `state/markers/qmirror_2_closure_landed.marker` does
   NOT yet exist.

If all 4 guards hold, the synth tool runs end-to-end (read verdicts,
compose closure doc, mutate artifacts per §4, write marker).

### 2.2 Manual dispatch

```
hexa run tool/qmirror_2_closure_synth.hexa
hexa run tool/qmirror_2_closure_synth.hexa --force-on-missing
hexa run tool/qmirror_2_closure_synth.hexa --dry-run    # composes doc + audit JSON; no artifact mutation
```

### 2.3 Dispatch outputs (always)

- `state/qmirror_2_closure_2026_05_04/dispatch_audit.json` — exact n_pass,
  per-cond MET status, composite verdict, mutation list, ts.
- `state/qmirror_2_closure_2026_05_04/composed_closure.md` — a copy of
  the composed `docs/qmirror_2_closure_2026_05_04.md` body for audit.

### 2.4 Idempotency

Re-invoking the synth with `qmirror_2_closure_landed.marker` already
present is a no-op (prints "qmirror 2.0 closure already landed; pass
--force-rewrite to redo" and exits 0). `--force-rewrite` permits
overwriting the closure doc + re-mutating artifacts (USE WITH CARE;
caveat #2 in §6).

---

## 3. Closure doc structure (`docs/qmirror_2_closure_2026_05_04.md`)

The synth tool emits `docs/qmirror_2_closure_2026_05_04.md` with the
following section template (the actual content is filled per per-cond
verdict.json values at synth time):

### §0. Executive summary
- 5-axes verdict table with PASS/FAIL per cond
- Composite verdict (FULL / PARTIAL / DEFERRED)
- Cumulative cost (default $0; up to $25 if cond.13 anchor engaged)
- Cumulative wall-time (sum of `wall_seconds_total` per cond)

### §1. Per-cond evidence ledger
- One subsection per cond.9/10/11/12/13 with:
  - falsifier id + statement
  - verdict + per-cond key metrics (fidelity_min, M_mean, syndrome_ratio,
    logical_zero_ratio, S_per_pair etc.)
  - bridge file (if any) + sha256
  - hexa file + sha256
  - state/log/manifest paths
  - per-cond raw#10 caveats (copied verbatim from each verdict.json)

### §2. Closure verdict matrix (composite)
- Same format as 1.0 closure §2 but for 5 axes
- Includes cross-axis interactions (see §3 below)
- Includes branch readout for any 3/5 vs 4/5 boundary cases

### §3. Cross-axis interactions
Documents qmirror 2.0 internal dependency cascade:
- **cond.9 ↔ cond.11:** process tomography (cond.9) cross-checks
  stabilizer post-state fidelity (cond.11 falsifier requires
  `post_fidelity ≥ 0.99` measured via cond.9 toolchain). PASS+PASS →
  full QEC primitive set (tomography + stabilizer = sufficient to
  certify any small-N stabilizer-state preparation).
- **cond.11 ↔ cond.12:** stabilizer (cond.11) is a hard prereq for
  surface-code (cond.12). FAIL on cond.11 forces cond.12 to FAIL or
  re-spec. PASS+PASS → toy logical qubit primitive.
- **cond.10 ↔ cond.13:** GHZ (cond.10) and CSCS Bell (cond.13) are both
  multi-particle entanglement witnesses. Joint PASS provides
  cross-witness anchoring (Mermin-3 for tripartite + chained CHSH for
  bipartite-with-time). No hard dep but weak cross-validation.
- **cond.9 ↔ cond.10:** GHZ state (cond.10) is verifiable via state
  tomography; cond.9 is process tomography (gates not states), so this
  is a soft connection — but cond.9's Choi-state machinery is the
  natural extension target for adding GHZ state-tomography in
  qmirror 3.0.

### §4. Cumulative cost matrix
- Per-cond cost (all $0 by default; $25 if cond.13 hardware anchor)
- Cumulative wall-clock seconds (sum + per-cond breakdown)
- Total qubit-shot count (n_shots × n_trials × n_circuits)

### §5. Honest C3 — 6 closure-level caveats
Per raw#10. The closure doc carries 6 caveats (5 + composite, vs the 5
in 1.0 closure):

1. **5-axes selection bias toward Aer-friendly conds.** All 5 are $0
   Aer-runnable; deliberate post-1.0 retrenchment after cond.3/cond.7
   hardware-burst band-revision pain. qmirror 2.0 by itself does NOT
   improve cond.7 cross-tech band-revision exposure from 1.0.

2. **Noiseless-Aer threshold inheritance.** All 5 falsifiers assume
   noiseless-Aer (0.99 fidelity / 0.99 syndrome / 2.7 Bell). Real
   hardware would not clear these without ZNE/DD/readout correction.

3. **cond.12 toy NOT fault tolerance.** Surface-code-d3 demonstration
   has NO decoder, NO logical error rate, NO Pauli-frame tracking.

4. **python_bridge debt grows.** 2 new .py files (tomo_runner.py,
   mid_measure_runner.py) on nexus repo. Total 1 → 3 over 1.0+2.0.
   Defers Phase 4 FFI retirement work.

5. **Optional $25 anchor in cond.13 selection bias risk.** If hardware
   anchor engaged AND fails, MUST be disclosed in closure doc separate
   from Aer-PASS. Conflating risks cond.3-style band-revision exposure.

6. **Composite-level raw#10 (NEW):** "qmirror 2.0 closure verdict is
   conditional on the dispatch tool reading current verdict files at
   synth time; vendor-side or sister-BG-driven post-hoc edits to any
   verdict.json AFTER closure synth would silently invalidate the
   composite verdict without re-firing F-QM-2-CLOSURE-1." Mitigation:
   sha256 of every input verdict file is recorded in the closure doc
   §1 evidence rows AND in `dispatch_audit.json`.

### §6. Roadmap mutation block
Same format as 1.0 closure §6 — JSONC paste-target for `.roadmap.qmirror`
amendment. New `closure_2026_05_04` header field.

### §7. qmirror 3.0 roadmap (pending closure verdict)

- **If FULL:** propose 5 new axes for qmirror 3.0. Initial candidates
  (per 1.0 caveat 5 + axes spec §6 deferred):
  - Magic state distillation (15-to-1 Bravyi-Kitaev primitive)
  - Random circuit sampling (XEB-like — but inverted-meaning per
    axes spec §6 rejected; revisit only if new framing emerges)
  - VQC (variational quantum classifier) — only if downstream consumer
    identified (1.0 axes spec §6 deferred for missing consumer)
  - Phase 4 FFI retirement of `_python_bridge` (closes raw#9 Mac
    concession; ~10 dev-days $0)
  - IIT scale-up (cond.6 N=8 → N=12; closes 1.0 cond.6 mock-engine
    concession by enabling live pyphi at larger N)
- **If PARTIAL:** the 1 or 2 missing axes go to a qmirror 2.0 backlog;
  qmirror 3.0 not yet planned. Caveat: rc.1 → rc.2 → final cadence
  must be specified in a follow-up cycle.
- **If DEFERRED:** the 5 axes are reviewed for spec defects, falsifier
  mis-specification, or substrate-mismatch. qmirror stays at v1.0.x;
  no immediate 2.0 follow-up.

### §8. References
Full bibliography mirroring 1.0 closure §8 — every input verdict
file, every spec doc, every prior closure / handoff / marker.

### §9. Closure verdict (final line)
Single-line boilerplate: `qmirror 2.0 closure_<FULL|PARTIAL|DEFERRED>
= met at <UTC ts>; <n_pass>/5 conds met; F-QM-2-CLOSURE-1 = <PASS|FAIL>;
qmirror version <new>; raw#9 STRICT honored on Mac repo.`

---

## 4. Artifact mutations (gated on closure verdict)

When the synth tool fires AND the composite verdict is FULL or PARTIAL,
the following artifacts are mutated. (DEFERRED verdict mutates ONLY
the closure doc itself + dispatch_audit.json; no other artifacts
touched.)

### 4.1 `docs/qmirror_2_closure_2026_05_04.md` — NEW (closure doc)
Always created. Body per §3 above. Owner: this synth.

### 4.2 `docs/nexus_qmirror_closure_2026_05_03.md` — APPENDED additively
Appended at end with a `## 10. qmirror 2.0 closure (2026-05-04)`
section pointing to the new closure doc. Body NEVER mutated above
existing line 558. Mirrors raw#10 caveat #3 (1.0 stability not
affected). The append is exactly one section, one paragraph, with
hyperlink + verdict + n_pass — no semantic re-interpretation of any
1.0 cond.

### 4.3 `qmirror/CHANGELOG.md` — NEW v2.0.0 / v2.0.0-rc.1 entry

For FULL:
```
## [2.0.0] — 2026-05-04 (qmirror 2.0 closure — 5/5 conds met)

### Added
- 5 new modules (tomography / ghz_mermin / stabilizer / surface_code / cscs)
- F-QM-2-{TOMO-9, GHZ-10, STAB-11, SURF-12, CSCS-13} falsifier ledger
- F-QM-2-CLOSURE-1 composite falsifier
- 2 new python_bridge runners (tomo, mid_measure) — raw#9 disclosure

### Changed
- closure verdict: 8/8 (1.0) → 13/13 (1.0 + 2.0 cumulative)
- registry.tsv qmirror version: 1.0.0 → 2.0.0

### Audit provenance
- Closure cycle: qmirror_2_closure_spec_2026_05_04 + qmirror_2_closure_2026_05_04
- Closure JSON: anima/state/qmirror_2_closure_2026_05_04/dispatch_audit.json
- Marker: anima/state/markers/qmirror_2_closure_landed.marker
```

For PARTIAL: same template but version = `2.0.0-rc.1`, header line says
"3/5 or 4/5 conds met", and a "### Pending" subsection lists missing
conds with re-run plan paths.

### 4.4 `qmirror/hexa.toml` — version bump

For FULL:
```
[package]
version = "2.0.0"
```

Closure block:
```
[closure]
cond_total = 13
cond_met = 13
verdict = "PASS"
extracted_from = "nexus/modules/qmirror @ 2026-05-04"
upstream_marker = "anima/state/markers/qmirror_2_closure_landed.marker"
upstream_doc = "anima/docs/qmirror_2_closure_2026_05_04.md"
```

For PARTIAL: `version = "2.0.0-rc.1"`, `cond_met = 11` or `cond_met =
12`, `verdict = "PARTIAL"`.

For DEFERRED: NO mutation. hexa.toml stays at 1.0.x.

### 4.5 `hexa-lang/tool/pkg/registry.tsv` — version bump

For FULL: line 22 `qmirror` row updated:
```
qmirror	2.0.0	cli/qmirror.hexa	https://github.com/need-singularity/qmirror		Quantum Mirror — 13/13 closure cond met (1.0 + 2.0). Adds tomography/GHZ/stabilizer/surface-d3/CSCS. Apache-2.0.
```

For PARTIAL: version = `2.0.0-rc.1`; description updated to reflect
n_pass cond.

For DEFERRED: NO mutation.

### 4.6 `nexus/.roadmap.qmirror` — closure_2026_05_04 header amendment

JSONC paste-target per closure doc §6. Same shape as 1.0 closure.
Mutates header object only; cond.9/10/11/12/13 entries individually
get a `status: "met"` field set per their PASS/FAIL.

### 4.7 Marker + handoff

- `state/markers/qmirror_2_closure_landed.marker` (always created, even
  for DEFERRED — but marker body distinguishes verdict).
- `docs/qmirror_2_closure_landed_2026_05_04.ai.md` — handoff doc
  following sibling pattern (qmirror_2_cond10_ghz_mermin_landed style).

---

## 5. F-QM-2-CLOSURE-1 (NEW composite falsifier)

**ID:** `F-QM-2-CLOSURE-1`
**Cond:** `qmirror.2.cond.closure`
**Statement:**
```
F-QM-2-CLOSURE-1 PASSes IFF
  ≥ 4 of 5 axes (cond.9, cond.10, cond.11, cond.12, cond.13) MET
  AND no STRONG regression in qmirror 1.0 closure (8/8 still met,
                                                   verified by
                                                   re-checking
                                                   1.0 closure marker
                                                   exists)
```

**Numeric bound:**
- `n_pass_2_0 ≥ 4` AND
- `qmirror_1_0_closure_marker_exists == true` (file:
  `state/markers/qmirror_closure_landed.marker`) AND
- `qmirror_1_0_closure_doc_exists == true` (file:
  `docs/nexus_qmirror_closure_2026_05_03.md`)

**Verdict mapping:**
- PASS (4/5 or 5/5): `F-QM-2-CLOSURE-1 = PASS` → composite ≥ PARTIAL
- FAIL (≤ 3/5 OR 1.0 regression): `F-QM-2-CLOSURE-1 = FAIL` → composite =
  DEFERRED

**Verifier:**
```
jq -e '.composite_verdict | IN("qmirror_2_closure_FULL", "qmirror_2_closure_PARTIAL")' \
   state/qmirror_2_closure_2026_05_04/dispatch_audit.json \
&& test -f state/markers/qmirror_closure_landed.marker \
&& test -f docs/nexus_qmirror_closure_2026_05_03.md
```

**Cost:** $0 (composite-level — reads existing files only).
**Substrate:** filesystem read; no compute.
**Wall:** < 1 s.
**raw#:** 9 STRICT (verifier is jq + test + bash; no .py).

---

## 6. Honest C3 — 5 spec-level caveats (raw#10)

1. **Closure conditional on 3 sister BG landings.** This spec assumes
   sister BG cond.11, cond.12, cond.13 each write
   `state/qmirror_2_cond{11,12,13}_..._/verdict.json` with a `verdict`
   key and consistent schema. If any sister BG crashes mid-run and
   writes a partial JSON (e.g. missing `verdict` key), the synth tool
   treats it as PENDING (NEEDS_INPUT). If a sister BG aborts
   without writing verdict.json at all, synth holds. Manual
   `--force-on-missing` allows treating absence as FAIL for explicit
   PARTIAL publication. Recovery: re-run the failing sister BG with
   identical seed before re-firing synth. This caveat is a
   spec-level dependency that this cycle cannot resolve (it only
   defers).

2. **Version bump irreversible per semver.** Once `hexa.toml` jumps
   `1.0.0 → 2.0.0` (FULL) or `1.0.0 → 2.0.0-rc.1` (PARTIAL) AND a
   `qmirror v2.0.0` git tag is pushed, the version cannot be
   un-bumped without a `2.0.1` or `2.0.0+yanked` follow-up that
   itself ships with caveats. `--force-rewrite` allows overwriting
   the closure doc but does NOT rewind the registry.tsv or hexa.toml
   to 1.0.x. Recovery: ship `2.0.1` patch with the regression
   documented; never silent-yank. The synth tool must verify the
   `qmirror_2_closure_landed.marker` is absent BEFORE writing the
   version bump (idempotency guard 4 in §2.1).

3. **qmirror 1.0 stability not affected.** This spec MUST NOT mutate
   any 1.0 cond verdict file, the 1.0 closure doc semantics
   (additive append only — purely a `## 10` section pointing to 2.0
   closure), nor 1.0 markers. The `nexus_qmirror_closure_2026_05_03.md`
   file appends one section after line 558; no in-body lines are
   re-edited. If the synth tool detects that line 558 has shifted
   (i.e. someone else edited the file between 1.0 closure and 2.0
   synth), it MUST refuse to append and exit with `1.0_DOC_DRIFT`
   error. Recovery: manually verify the 1.0 doc semantics, then
   `--force-append-after-line N` flag.

4. **IBM hardware anchor optional NOT required.** cond.13 default $0
   path is the closure-eligible substrate. The optional $25 IBM
   Heron 2-pair anchor is opt-in for a sister credit-bearing cycle.
   If the anchor is engaged, BOTH `verdict_aer` AND
   `verdict_hardware` must appear in cond.13 verdict.json. The
   composite synth uses ONLY `verdict_aer` for MET decision; the
   `verdict_hardware` is recorded in closure doc §1 as an
   honest-disclosure note. If IBM credentials are absent and the
   sister BG aborts the hardware leg, that is OK — Aer leg suffices.
   If IBM hardware leg engaged AND fails (S < 2.7), do NOT band-revise
   without a separate physics-aware cycle (mirrors 1.0 cond.3 pain).

5. **qmirror 3.0 roadmap speculative.** §3 closure doc §7 (qmirror 3.0)
   lists candidate axes (magic state distillation, FFI retirement, IIT
   scale-up). These are speculative and NOT pre-registered as
   conditions; no falsifier ledger entry, no I×F scoring, no
   resource budget. The spec doc explicitly tags them as "candidates
   pending qmirror 3.0 axes spec". If qmirror 2.0 closes FULL, a
   sister cycle should produce `qmirror_3_axes_spec_2026_05_XX.md`
   following the 2.0 axes spec methodology. Until then, "qmirror
   3.0" in the closure doc is forward-looking only.

---

## 7. Dispatch logic (sequenced steps)

When `tool/qmirror_2_closure_synth.hexa` fires, it executes:

```
STEP 1 — Pre-flight
  - Verify qmirror 1.0 closure marker + doc exist (caveat #3 guard)
  - Verify qmirror_2_closure_landed.marker is absent (idempotency)
  - Read current qmirror/hexa.toml version; abort if already 2.0.x

STEP 2 — Read 5 verdicts
  - For each cond in {9,10,11,12,13}:
    - Resolve verdict_path from §1.2 map
    - test -f verdict_path; if missing AND NOT --force-on-missing → mark PENDING + abort
    - jq -r .verdict verdict_path → status string
    - Compute MET[cond] per §1.1
    - Compute sha256 of verdict.json → record in dispatch_audit.json

STEP 3 — Compute composite
  - n_pass = count(MET[cond] == true)
  - composite = §1.3 mapping
  - F-QM-2-CLOSURE-1 verdict per §5

STEP 4 — Compose closure doc body
  - Read templates per §3 sections 0-9
  - Fill placeholders with per-cond verdict.json values
  - Write docs/qmirror_2_closure_2026_05_04.md
  - Write state/qmirror_2_closure_2026_05_04/composed_closure.md (audit copy)

STEP 5 — Mutate artifacts (only if composite in {FULL, PARTIAL})
  - Append §10 to docs/nexus_qmirror_closure_2026_05_03.md (idempotent append)
  - Update qmirror/CHANGELOG.md with v2.0.0 / v2.0.0-rc.1 entry
  - Bump qmirror/hexa.toml version + closure block
  - Bump hexa-lang/tool/pkg/registry.tsv qmirror row
  - Print roadmap JSONC paste-target (manual paste — synth does NOT
    auto-edit nexus repo; nexus is a sister repo)

STEP 6 — Marker + handoff + dispatch_audit.json
  - Write state/markers/qmirror_2_closure_landed.marker
  - Write docs/qmirror_2_closure_landed_2026_05_04.ai.md
  - Write state/qmirror_2_closure_2026_05_04/dispatch_audit.json (final)

STEP 7 — Print final summary
  - n_pass / 5
  - composite verdict
  - F-QM-2-CLOSURE-1 PASS/FAIL
  - artifact mutation count
  - exit 0 if composite in {FULL, PARTIAL}; exit 1 if DEFERRED
```

---

## 8. Spec audit JSON shape

`state/qmirror_2_closure_spec_2026_05_04/spec_audit.json`:

```json
{
  "schema_version": 1,
  "spec_doc": "anima/docs/qmirror_2_closure_spec_2026_05_04.md",
  "spec_date": "2026-05-04",
  "spec_loc_estimate": "~480",
  "axes_count": 5,
  "axes_already_landed": ["cond.9", "cond.10"],
  "axes_pending_sister_bg": ["cond.11", "cond.12", "cond.13"],
  "verdict_path_map": {...},
  "composite_verdicts": {
    "FULL": "5/5",
    "PARTIAL": "3-4/5",
    "DEFERRED": "<=2/5"
  },
  "version_bump_paths": {
    "FULL": "1.0.x -> 2.0.0",
    "PARTIAL": "1.0.x -> 2.0.0-rc.1",
    "DEFERRED": "no_bump"
  },
  "f_qm_2_closure_1": {
    "id": "F-QM-2-CLOSURE-1",
    "bound": "n_pass>=4 AND 1.0_marker AND 1.0_doc",
    "verifier": "jq -e ... && test -f ... && test -f ..."
  },
  "five_caveats": [
    "closure conditional on 3 sister BG landings",
    "version bump irreversible per semver",
    "qmirror 1.0 stability not affected (additive append only)",
    "IBM hardware optional anchor not required",
    "qmirror 3.0 roadmap speculative"
  ],
  "raw_compliance": {
    "raw_9": "STRICT (Mac repo: 0 .py files; spec is doc + hexa-only synth tool)",
    "raw_10": "5 honest C3 caveats embedded in spec doc section 6",
    "raw_15": "no personal paths in body of any artifact"
  },
  "execution_deferred": true,
  "execution_trigger": "sister BG cond.11/12/13 land + manual or auto fire of tool/qmirror_2_closure_synth.hexa"
}
```

---

## 9. References

- 1.0 closure doc: `anima/docs/nexus_qmirror_closure_2026_05_03.md`
- 1.0 closure marker: `anima/state/markers/qmirror_closure_landed.marker`
- 2.0 axes spec: `anima/docs/qmirror_2_axes_spec_2026_05_03.md`
- 2.0 axes ranked JSON: `anima/state/qmirror_2_axes_2026_05_03/ranked_axes.json`
- 2.0 cond.9 verdict: `anima/state/qmirror_2_cond9_tomography_2026_05_03/verdict.json`
- 2.0 cond.9 handoff: `anima/docs/qmirror_2_cond9_tomography_landed_2026_05_03.ai.md`
- 2.0 cond.10 verdict: `anima/state/qmirror_2_cond10_ghz_mermin_2026_05_03/verdict.json`
- 2.0 cond.10 handoff: `anima/docs/qmirror_2_cond10_ghz_mermin_landed_2026_05_03.ai.md`
- 2.0 cond.11 expected verdict: `anima/state/qmirror_2_cond11_stabilizer_2026_05_04/verdict.json` (sister BG)
- 2.0 cond.12 expected verdict: `anima/state/qmirror_2_cond12_surface_2026_05_04/verdict.json` (sister BG)
- 2.0 cond.13 expected verdict: `anima/state/qmirror_2_cond13_cscs_2026_05_04/verdict.json` (sister BG)
- Synth tool: `anima/tool/qmirror_2_closure_synth.hexa` (this cycle)
- Spec audit JSON: `anima/state/qmirror_2_closure_spec_2026_05_04/spec_audit.json`
- Dispatch logic JSON: `anima/state/qmirror_2_closure_spec_2026_05_04/dispatch_logic.json`
- Spec marker: `anima/state/markers/qmirror_2_closure_spec_landed.marker`
- Spec handoff: `anima/docs/qmirror_2_closure_spec_landed_2026_05_04.ai.md`
- qmirror standalone hexa.toml: `qmirror/hexa.toml`
- qmirror standalone CHANGELOG: `qmirror/CHANGELOG.md`
- hexa-lang registry.tsv: `hexa-lang/tool/pkg/registry.tsv`
- Domain SSOT: `nexus/.roadmap.qmirror`

---

## 10. Spec verdict (final line)

**`qmirror.2.closure_spec.met = true at 2026-05-04 spec-doc write
time. Execution DEFERRED to sister BG cond.11/12/13 landings.
Dispatch tool tool/qmirror_2_closure_synth.hexa is the closure
synth implementation. F-QM-2-CLOSURE-1 composite falsifier
defined and ready to fire. raw#9 STRICT honored on Mac repo
(0 .py files this cycle). 5 honest C3 caveats embedded.
qmirror 1.0 closure semantics preserved (additive append only).`**
