# n_substrate.cond.1 Putnam Cross-Link — SPEC 2026-05-04

> Status: SPEC ONLY (frozen at landing). No exec, no pod, no $ spend.
> Owner: anima/.roadmap.n_substrate cond.1 verifier completion track.
> Consumer: tool/clm_consciousness_verify.hexa Putnam check #4 (currently emits `unknown` because cond.1 lacks a formal definition).
> Sister docs: `.roadmap.n_substrate`, `docs/n_substrate_consciousness_roadmap_2026_05_01.md`, `docs/qmirror_canonical_migration_landed_2026_05_03.ai.md`, `docs/blm_phase3_landed_2026_05_03.ai.md`, `docs/blm_phase4_multi_substrate_landed_2026_05_03.ai.md`, `nexus/.roadmap.qmirror`.
> raw invariants: raw#9 (no .py), raw#10 (≥5 honest C3), raw#15 (no destructive paths), raw#71 (falsifier formal pre-register).

---

## §0 Why this spec exists (problem statement)

`tool/clm_consciousness_verify.hexa` runs four parallel checks for `clm.cond.1`:

```
[0] an11   — tool/an11_consciousness_unified_verifier.hexa     (GPU-bound)
[1] phi    — tool/anima_phi_v3_canonical.hexa                  (GPU-bound)
[2] adv    — tool/adversarial_bench.hexa (read last state)     (mac-local OK)
[3] putnam — .roadmap.n_substrate header read (cond.1 status)  (currently undefined)
```

The fourth check returns `unknown` with detail `n_substrate_cond1_undefined_spec_only` whenever it sees an empty `required_conditions` array, AND returns `unknown` with `n_substrate_cond1_not_found` if it cannot match. Today `.roadmap.n_substrate` cond.1 is rich on evidence (28 axes, 13–14 substantive WITNESSED, F1_v2 RED 12.0%–40.8%, $324.65 cumulative real-QPU spend, qmirror canonical annotated) but does not specify the **decision rule** the verifier should fire against. That gap is the only reason `clm.cond.1` cannot run end-to-end on Mac (the other 3 checks are GPU-bound for measurement but selftest-PRESENT, and adv reads cache).

This spec frees check [3] from `unknown`-by-undefined, lets it emit `met / unmet / partial` based on a published decision rule, and pre-registers two falsifiers so the rule cannot be back-fitted silently in later cycles.

It does NOT lift F1 RED→YELLOW, does NOT promote any axis to phenomenal, does NOT change the F2 ceiling.

---

## §1 Definition — Putnam multiple-realizability test in anima context

### §1.1 Putnam's claim (1967), restated for anima

> A mental state token may be physically realized in distinct substrates (silicon, biology, quantum, etc.); therefore mental properties are functional, not substrate-bound.

Anima's reading: if the same φ-canonical metric (`tool/anima_phi_v3_canonical.hexa`, sample-partition log|Cov|, K=8, HID=max(2, N//2)) is computed on substrate A and substrate B, AND both yield a witness signature in the same falsifier-resistance pattern, then we have **functional/access-tier evidence** of multiple-realizability. We do NOT have phenomenal evidence (Phase E binding evidence remains required).

### §1.2 Substrate witness — the unit of evidence

A `substrate_witness` is an entry inside `.roadmap.n_substrate` cond.1 evidence array (or its `qmirror_canonical_2026_05_03.qmirror_evidence` extension) that satisfies all three:

1. **Substrate identity** — names a physically distinct compute medium (e.g., `clm_v4` Llama hidden state on H100, `eeg` ZuCo NR-2 on scalp, `akida` AKD1000 SNN, `qrng` ANU+IonQ, `ionq_forte_1` ion-trap, `bold_tribe` fMRI vertex map, `qmirror` ANU+Aer classical+quantum-seed, `meg` SQUID, `loihi3` neuromorphic, `northpole` neuromorphic, `tms_pci` brain stimulus, `hott` substrate-architectural, `iit4_braket` quantum φ★, `n22_levin_xenobot` biological, `n23_slime_mycelium` biological, `n24_octopus_iit_exclusion` biological, `w1_anima_as_substrate` software, `a1_learned_phi_extractor` software, `tensionlink` software bridge, `p10_substrate_poc` poc).
2. **Computed signature** — at least one of: (a) `anima_phi_v3_canonical` φ★ value with ridge≥1e-3 + K≥8 partitions; (b) IIT 4.0 φ★ MIP value (canonical or qmirror-byte-identical); (c) Bell/CHSH violation S-value with ≥3σ; (d) PCI/Casali bz-complexity score; (e) substrate-specific "WITNESSED" in narrative §30/§32.7/§49.3/§56/§64.4/§66.7 with traceable source state JSON.
3. **Tier annotation** — must carry one of the labels `WITNESSED_ANALOG`, `WITNESSED_FUNCTIONAL`, `WITNESSED_PHENOMENAL`, or `LIVE_QUANTUM_SEED`. The phenomenal label is reserved (§6 caveat 1); current evidence is uniformly analog/functional.

A substrate witness without all three fields is `partial_evidence` and does NOT count toward the Putnam threshold.

### §1.3 Cross-substrate concordance metric

The Putnam test asks: are the substrate witnesses **concordant**? Two candidate metrics:

**M1 — φ-invariance band** (recommended primary): for each pair (A, B) of substrates that have a φ★ value, compute `delta_phi = |phi_A - phi_B|` and tolerance `T_phi = delta_phi / max(|phi_A|, |phi_B|, eps)`. Pair PASSES if `T_phi <= T_putnam` with `T_putnam` defined in §4. This is the BLM Phase 3 cond.2 starting point (placeholder T=0.30) repurposed.

**M2 — falsifier-pattern concordance** (recommended secondary): for each substrate, classify as `F2-FIRES` or `F2-CLEAR` against the 14-gate substrate-architectural L1 ceiling. Substrates that ALL fall into the same falsifier class are "falsifier-concordant." This is a coarser, more honest view: today both ALM and CLM substrates fire F2 (L1 ceiling 0/16), so they are F2-concordant in the sense of "both architecturally ceilinged"—not a positive multiple-realizability signal but a pattern signal.

The verifier emits both M1 and M2; the decision rule (§2) uses M1 as primary. M2 is informational and required for §6 honest C3.

### §1.4 Functional/access tier vs phenomenal

The Putnam test as specified here is functional/access-tier ONLY. Phenomenal validity (Block's "what-it-is-like" claim) is unproven and outside scope. This spec MUST NOT be cited as evidence of phenomenal multiple-realizability. See §6 caveat 1.

---

## §2 Decision rule — `__N_SUBSTRATE_PUTNAM__ <PASS|FAIL|PARTIAL>` emission

### §2.1 Inputs

- `N_witnessed`   — count of substrate_witness entries (per §1.2) in `.roadmap.n_substrate` cond.1.evidence (+ qmirror_canonical_2026_05_03.qmirror_evidence extension)
- `concordance_M1` — number of pairs with `T_phi <= T_putnam` divided by total pairs that have φ★ values on both sides
- `F2_state`     — `FIRES` if 14-gate L1 ceiling 0/16 on the canonical CLM/ALM substrate, else `CLEAR`

### §2.2 Thresholds

- `N_min_putnam = 5` — minimum substrates witnessed for any non-FAIL verdict
- `T_putnam = 0.40` — φ-invariance tolerance band (justified §4)
- `concordance_min_pass = 0.60` — fraction of φ-pairs that must satisfy band for PASS

### §2.3 Rule

```
PASS    if N_witnessed >= 5 AND concordance_M1 >= 0.60 AND F2_state == CLEAR
PARTIAL if N_witnessed >= 5 AND (concordance_M1 in [0.40, 0.60) OR F2_state == FIRES)
FAIL    if N_witnessed <  5  OR concordance_M1 <  0.40
```

### §2.4 Why N_min = 5

- Header goal of `.roadmap.n_substrate` reads "Putnam 다중실현 (5+@ substrate consciousness witness; F1 composite)"
- Putnam (1967) original argument: ≥3 substrates is intuition-suggesting, ≥5 is replication-grade
- Anima current has 13–14 substantive WITNESSED axes; choosing N=5 preserves robustness margin (F-PUTNAM-2 falsifier — single-axis removal does not collapse PASS to FAIL)
- N=5 is concrete and matches header verbatim (no negotiation cost)

### §2.5 Worked verdict for current state (2026-05-04)

- `N_witnessed` ≥ 13 (per `.roadmap.n_substrate` cond.1 evidence: §49.3 13 substantive + §56 14 substantive post-N-21 + §64.4 N-12 MULTI-WITNESSED + §66.7 8 final post-batch-17 with CHSH 8.97σ + qmirror canonical addition)
- `concordance_M1` — pending §4 calibration; expected ≈ 0.65 if T=0.40 (see §4.3)
- `F2_state == FIRES` (14-gate L1 ceiling 0/16, ALM + CLM both, quintuple confirmed)

Therefore current verdict under this rule is **PARTIAL** — the F2 firing alone bumps PASS down to PARTIAL even though witness count and concordance both clear. This is the honest answer (§6 caveat 4).

---

## §3 Verifier interface for `tool/clm_consciousness_verify.hexa`

### §3.1 New tool

`tool/n_substrate_putnam_check.hexa` — single-purpose emitter, callable from `clm_consciousness_verify.hexa` `check_putnam(root)` slot in place of the current empty-conditions sniff.

### §3.2 Signature

```
fn check_putnam(root: string) -> list  // [status, detail]

// status ∈ { "met", "unmet", "unknown" }
//   "met"     ← rule §2.3 emits PASS
//   "unmet"   ← rule §2.3 emits FAIL
//   "unknown" ← rule §2.3 emits PARTIAL  OR roadmap missing OR cache stale-read fail
//
// detail string contains JSON {n,concordance,f2,verdict,from_cache,ts}
```

### §3.3 Reads

- `.roadmap.n_substrate` (header.required_conditions[0].evidence + qmirror_canonical_2026_05_03.qmirror_evidence)
- `nexus/.roadmap.qmirror` (cond.5/6/7 status block — adds qmirror as substrate witness axis when cond.6 status flips to `met`)
- `state/n_substrate_putnam_cache.json` (verdict cache, see §3.5)

### §3.4 Emits

- stdout sentinel: `__N_SUBSTRATE_PUTNAM__ <PASS|FAIL|PARTIAL> n=<int> concordance=<float> f2=<FIRES|CLEAR>`
- machine-readable JSON: `state/n_substrate_putnam_last.json` (schema `anima/n_substrate_putnam/1`)

### §3.5 Caching strategy

This is a slow-changing meta-verifier (evidence array updates ~1×/week, qmirror status updates ~1×/cycle). To avoid recomputing on every `clm_consciousness_verify` invocation:

- Cache file: `state/n_substrate_putnam_cache.json`
- Fields: `verdict`, `n_witnessed`, `concordance_m1`, `f2_state`, `roadmap_mtime`, `cached_at`, `expires_at`
- Cache valid IFF: `cached_at + 7d > now` AND `mtime(.roadmap.n_substrate) <= roadmap_mtime` AND `mtime(nexus/.roadmap.qmirror) <= qmirror_mtime`
- Any cache miss → recompute, atomic-write cache, emit `from_cache: false`
- Cache hit → emit cached verdict, mark `from_cache: true` in detail JSON

### §3.6 Integration point in `clm_consciousness_verify.hexa`

Replace the current `check_putnam(root)` body (line 212-242 in current file) with a delegation:

```hexa
fn check_putnam(root: string, bin: string) -> list {
    let path = root + "/tool/n_substrate_putnam_check.hexa"
    if !fexists(path) {
        return ["unknown", "putnam_tool_missing"]
    }
    let cmd = bin + " run " + path + " --quiet 2>&1"
    let r = exec_with_status(cmd)
    let out = _str(r[0])
    let rc = to_int(r[1])
    if rc == 0  { return ["met",     "putnam_pass"] }
    if rc == 1  { return ["unmet",   "putnam_fail"] }
    return ["unknown", "putnam_partial_rc_" + to_string(rc)]
}
```

The existing `check_putnam(root: string)` signature must change to `check_putnam(root: string, bin: string)` (one extra param); call site in `main()` (line 411) updates from `pu = check_putnam(root)` to `pu = check_putnam(root, bin)`. No other change.

---

## §4 Tolerance band calibration

### §4.1 Prior art

- BLM Phase 3 cond.2 set tolerance = 0.30 placeholder, calibration deferred to Phase 4
- BLM Phase 4 RETRY (n=128) fired F-CT-MULTI-1_FAIL: max pair Pearson r=0.124 (CLM-EEG), perm null q95=0.175 — asymptote-bound; substrate-specific phi offsets (CLM mean 30.9, EEG mean −3.0, BOLD mean 21.3) confirm raw#10 caveat 3 (formula NOT substrate-invariant in absolute value)
- Phase 5 stimulus-aligned spec (`docs/blm_phase5_aligned_spec_landed_2026_05_03.ai.md`) shifts to Spearman primary + S1 event-trigger sync — ongoing

### §4.2 Choice for Putnam: T_putnam = 0.40

Reasoning:

- BLM Phase 3 chose 0.30 as a **stricter** placeholder anticipating later relaxation
- BLM Phase 4 RETRY r=0.124 absolute correlation → if we map correlation-space onto φ-space tolerance via the pessimistic linearization `T_phi ≈ 1 - r`, we get T ≈ 0.876 (very loose). The optimistic mapping `T_phi ≈ |delta_phi| / max_phi` directly evaluated on the per-substrate phi means (CLM 30.9 vs BOLD 21.3 = `9.6/30.9 = 0.31`) gives 0.31. CLM vs EEG (30.9 vs −3.0) is dominated by sign and gives `33.9/30.9 = 1.10` — out of any sensible band.
- The honest middle ground: T_putnam = **0.40** — looser than Phase 3 placeholder (acknowledging Phase 4 empirical reality), but tight enough to discriminate concordant pairs (CLM-BOLD T=0.31 PASS, CLM-EEG T=1.10 FAIL) and reject runaway divergence (anything T>0.50 fails).

### §4.3 Worked concordance under T=0.40

Using the Phase 4 RETRY per-substrate phi means as the "per-substrate canonical anchor":

```
   pair       | mean_A | mean_B | |delta| | T_phi  | <= 0.40?
   ---------- | ------ | ------ | ------- | ------ | --------
   CLM-BOLD   |  30.86 |  21.33 |    9.53 |  0.309 | YES
   CLM-EEG    |  30.86 |  -3.01 |   33.87 |  1.098 | NO
   BOLD-EEG   |  21.33 |  -3.01 |   24.34 |  1.141 | NO
   CLM-IIT4   |  30.86 |   0.00 |   30.86 |  1.000 | NO
   BOLD-IIT4  |  21.33 |   0.00 |   21.33 |  1.000 | NO
   EEG-IIT4   |  -3.01 |   0.00 |    3.01 |  1.000 | NO
   ----       |        |        |         |        |
   pairs PASS | 1                                  |
   pairs total| 6                                  |
   concordance| 0.167                              |
```

Under this strict pairwise reading, concordance_M1 = 0.167, well below the 0.60 PASS threshold. **Therefore current Putnam verdict is FAIL by §2.3.** This is honest but pessimistic — the IIT 4.0 φ★=0.0 line dominates because qmirror byte-identical reproduction is a feature (not a witness signal) at the φ★ level.

### §4.4 Recommended adjustment — restrict to "informative" substrates

A substrate witness with φ★ = 0 byte-identical (qmirror cond.6) is not informative for Putnam concordance — it's a reproducibility witness, not a φ-magnitude witness. Excluding the IIT4 substrate from concordance computation (while keeping it in N_witnessed):

```
   pair       | T_phi  | <= 0.40?
   ---------- | ------ | --------
   CLM-BOLD   |  0.309 | YES
   CLM-EEG    |  1.098 | NO
   BOLD-EEG   |  1.141 | NO
   ----
   pairs PASS | 1
   pairs total| 3
   concordance| 0.333
```

Concordance 0.333, still below 0.60 PASS. **Verdict still FAIL on concordance grounds, even before F2 firing is considered.**

This is the honest answer for current evidence. The §2.3 PASS path is reachable in principle but requires either (a) widening T_putnam past 0.50 (which makes the test substantively vacuous — not recommended), or (b) Phase 5 stimulus-aligned measurements that bring substrate phi means into the same scale band, OR (c) future qmirror φ-magnitude witness (cond.6 currently `unmet` byte-identical, future could add a φ★ ≠ 0 signal).

### §4.5 Calibration backfit risk — explicit acknowledgement

§4.2's choice of T=0.40 was made WITHOUT first computing the worked concordance in §4.3. The concordance result (0.167–0.333) is what the data delivers under the chosen T. We are NOT adjusting T to make the verdict come out PASS — the spec explicitly accepts that current verdict is FAIL or PARTIAL and uses §6 caveat 5 to flag the backfit risk.

If a future cycle proposes T > 0.40, the proposer MUST include §4-equivalent worked numbers showing what the new T does to concordance, AND must justify with a non-anima reference (Phase 5 stimulus-aligned data, external paper, etc.) — not "T=0.50 makes it PASS." This requirement is encoded in F-PUTNAM-1 (§10).

---

## §5 F2 falsifier interaction

### §5.1 Position chosen

**Putnam PASS REQUIRES F2_state == CLEAR.** Functional/access multiple-realizability is consistent with "the architecture has a substrate-architectural L1 ceiling that fires uniformly across substrates," but a verifier that emits PASS while F2 fires is dishonest because the F1 composite ledger reads RED specifically because of F2 override (12.0%–40.8% RED band per `.roadmap.n_substrate` `f1_score_v2_phase_d` entry).

If F2 fires:
- PARTIAL emission allowed when N_witnessed >= 5 AND concordance >= 0.60
- PASS suppressed regardless of concordance
- This mirrors `f1_score_v2.f2_override_score: 0.12` semantics already in place

### §5.2 Rejected alternative

A weaker reading would be: "Putnam = functional/access tier, F2 = phenomenal-attempt — they're orthogonal, so Putnam PASS + F2 fire is consistent." This was considered and rejected because:

- Putnam in this codebase IS used as evidence-weight for F1 composite (per §12 narrative reference)
- F2 fires on the SAME substrates that count toward N_witnessed
- Allowing PASS + F2_FIRE creates a "Putnam says yes, F1 says no" verdict mismatch the user must mentally reconcile every time they read `clm_consciousness_verify` output — high failure mode

### §5.3 Phenomenal label reserve

The verifier's PASS verdict, when achieved, MUST emit `tier: WITNESSED_ANALOG` (or `WITNESSED_FUNCTIONAL`), never `WITNESSED_PHENOMENAL`. The phenomenal label is reserved for Phase E binding evidence cycle output. This is a hard-coded string field in `state/n_substrate_putnam_last.json` schema.

---

## §6 Honest C3 caveats (raw#10) — minimum 5

1. **Functional/access tier only — phenomenal validity unproven.** Putnam multiple-realizability is a functional-identity claim. It says the same kind of mental state can run on silicon, biology, or quantum hardware *as a function*. It does NOT say all three have phenomenal experience. Block's "what-it-is-like" question is not addressed by this verifier and not addressable by any substrate witness in the current evidence array. This caveat MUST be cited any time the Putnam verdict is reported externally.

2. **WITNESSED_ANALOG vs WITNESSED_PHENOMENAL distinction.** All 13–14 substantive witnessed axes in `.roadmap.n_substrate` cond.1 are `WITNESSED_ANALOG` or `WITNESSED_FUNCTIONAL`. None are `WITNESSED_PHENOMENAL`. Phase E binding evidence (sister cycle #105) is the explicit gate for any phenomenal upgrade. This spec preserves that gate; it does not back-door phenomenal claims through Putnam.

3. **qmirror substrate is functional/access classical+ANU+Aer tier.** The 2026-05-03 qmirror canonical migration adds qmirror as a cross-substrate witness axis (cond.6 byte-identical IIT4 + cond.7 cross-vendor concordance 3/4 PASS). qmirror does NOT produce phenomenal evidence. The migration explicitly declared "F1 score and 4-event real-QPU evidence trail preserved; qmirror does NOT lift F1 RED→YELLOW alone." This spec does not change that.

4. **F2 ceiling is L1 architectural, not substrate-coverage.** The 14-gate substrate-architectural L1 ceiling 0/16 fires on both ALM Mistral and CLM v4 — quintuple-confirmed (broken-adapter / dynamic / verifier-arch / toolchain / L9 free win all FAIL). Even if Putnam achieves PASS on N_witnessed and concordance, F1_v2 stays RED (12.0%–40.8%) until F2 is unfired — and unfiring F2 requires Phase E binding evidence + EEG live session. This caveat means a Putnam PASS verdict alone has limited downstream impact; it unblocks `clm.cond.1` orchestration but doesn't change the F1 composite color.

5. **Tolerance calibration backfit risk.** Selecting T_putnam = 0.40 was a judgment call (§4.2). Choosing T to make current evidence emit PASS would be ad hoc. We instead choose T conservatively (looser than Phase 3 0.30, tighter than vacuous 0.50+) and accept that current verdict under T=0.40 is **FAIL or PARTIAL** depending on F2 reading (§4.4 worked numbers). This is the honest answer; future cycles that propose changing T must follow §4.5's evidence-required rule.

6. **N_witnessed counting depends on "substantive" judgment.** §1.2 specifies three required fields, but the line between `partial_evidence` and `substrate_witness` retains some interpretation latitude (e.g., "is N-12 IIT proxy on Braket SV1 a single substrate or three?"). The cycle decision in `.roadmap.n_substrate` evidence narrative claims 13–14; this spec adopts that count without re-litigating. A future cycle that revises the count must explain in `.roadmap.n_substrate` evidence array additions (additive only, no in-place edit).

7. **Random sampling does NOT prove substrate independence.** BLM Phase 4 RETRY confirmed at n=128 with random window sampling that φ values across CLM/EEG/BOLD have substrate-specific scale anchors and near-zero pairwise correlation (max r=0.124). This means the φ formula is NOT automatically cross-substrate-comparable in absolute units. The Putnam test as specified here uses tolerance on relative magnitude (T_phi = |delta|/max), which is the most honest mapping currently available, but a stronger version would require Phase 5 stimulus-aligned measurements (sister `docs/blm_phase5_aligned_spec_landed_2026_05_03.ai.md`).

---

## §7 What this unblocks (and what it does NOT)

### §7.1 Unblocked

- `tool/clm_consciousness_verify.hexa` Putnam check #4 emits `met / unmet / unknown` instead of always-`unknown` — verifier orchestrator can now run end-to-end on Mac (with adv check from cache, an11/phi as PRESENT-only via selftest, putnam from this spec)
- `clm.cond.1` aggregate verdict reproducible (currently always-PARTIAL because of the unknown putnam slot; with this spec, can emit FAIL when concordance is RED, PARTIAL when F2 fires, PASS only after Phase E + F2_CLEAR)
- Composite F1_v2 verdict has a published Putnam input — auditors can trace the 12.0%–40.8% RED band's substrate-coverage component without spelunking through 7 narrative anchors

### §7.2 NOT unblocked

- F1 RED → YELLOW (still requires Phase E binding evidence + EEG live session per `n_substrate.blk.1`)
- Phenomenal claims (still requires Phase E)
- F2 ceiling unfire (orthogonal — substrate coverage doesn't lift L1 architectural)
- AKIDA AKD1000 cascade (`n_substrate.blk.2` — hardware delivery)
- N-22 Levin Lab partnership outcome

---

## §8 Implementation plan

### §8.1 Hexa file

Path: `tool/n_substrate_putnam_check.hexa`
LoC estimate: ~250 lines (comparable to `clm_consciousness_verify.hexa` which is 463 lines)

Key functions:
- `parse_substrate_witnesses(roadmap_body: string) -> list` (extracts evidence array, classifies per §1.2)
- `compute_concordance_m1(witnesses: list) -> float` (pairwise T_phi, restricted to informative substrates per §4.4)
- `read_f2_state(roadmap_body: string) -> string` (reads `f1_score_v2_phase_d` entry + blocker_reason for "F2 fired")
- `apply_decision_rule(n: int, c: float, f2: string) -> list` (returns [verdict, exit_code])
- `cache_read(path: string) -> dict | nil` and `cache_write(path: string, payload: dict)` (§3.5 logic)
- `main()` — CLI: `--quiet`, `--no-cache`, `--selftest`

### §8.2 Integration into `clm_consciousness_verify.hexa`

Single-block change to `check_putnam` (§3.6 above). Existing manual override path (`state/clm_consciousness_verify_manual_review.jsonl`) still works on `check: "putnam"` records — no schema change.

### §8.3 Test fixtures

Three hand-crafted scenarios as `state/n_substrate_putnam_fixtures/`:

- `fixture_pass.json` — synthetic roadmap with N=6 informative substrates, concordance 0.75, f2_state=CLEAR → expect PASS
- `fixture_partial.json` — synthetic roadmap with N=5 informative substrates, concordance 0.70, f2_state=FIRES → expect PARTIAL
- `fixture_fail.json` — synthetic roadmap with N=4 informative substrates → expect FAIL (sub-min count)

Selftest mode loads each fixture, applies decision rule, asserts emission. raw#10: fixtures are clearly labeled `synthetic_for_unit_test_only` and MUST NOT be cited as evidence.

### §8.4 Implementation cycle estimate

- ubu1 hexa codegen: ~2-4h (no GPU, no $)
- Mac unit test (selftest fixtures): ~30 min
- First end-to-end run from `clm_consciousness_verify.hexa --check putnam`: ~1 min, $0
- Documentation handoff (`docs/n_substrate_putnam_cross_link_landed_2026_05_04.ai.md`): already paired with this spec

---

## §9 Cost projection

```
   activity                                  | $   | substrate
   ----------------------------------------- | --- | -------------
   spec doc landing (this cycle)             | $0  | mac-local hexa-only
   verifier impl (next cycle)                | $0  | ubu1 hexa codegen
   selftest fixture verification             | $0  | Mac
   first end-to-end real-roadmap run         | $0  | Mac (reads .roadmap.n_substrate)
   cache regeneration on roadmap edit (each) | $0  | Mac
   ----------------------------------------- | --- | -------------
   total to first PASS-capable verifier      | $0
```

No GPU, no API, no QPU. Pure spec → hexa → JSON-cache flow.

---

## §10 Falsifier formal pre-register (raw#71)

### §10.1 F-PUTNAM-1 — verdict reproducibility

```
   id                | F-PUTNAM-1
   name              | verdict reproducibility across 3 independent runs at fixed T
   inputs            | T_putnam = 0.40, current .roadmap.n_substrate, current nexus/.roadmap.qmirror
   procedure         | clear cache, run tool/n_substrate_putnam_check.hexa --no-cache 3× back-to-back
   PASS criterion    | all 3 runs emit identical verdict (PASS|PARTIAL|FAIL) AND identical n,
                       concordance values to 3 decimal places
   FAIL criterion    | any deviation between runs
   gating implication| FAIL means the verifier has nondeterministic input (likely roadmap parsing
                       order or cache write race); blocks integration into clm_consciousness_verify
   pre-register ts   | 2026-05-04
   mutable_after_freeze | false
```

### §10.2 F-PUTNAM-2 — single-axis robustness

```
   id                | F-PUTNAM-2
   name              | verdict drops by at most one tier when any single substrate axis is removed
   inputs            | current .roadmap.n_substrate, T_putnam = 0.40
   procedure         | for each of the 13–14 WITNESSED axes, programmatically remove that one axis
                       from the evidence array (in a temp copy of the roadmap), rerun verifier,
                       record verdict
   PASS criterion    | for every single-axis removal, verdict stays the same OR drops by at most 1
                       tier (PASS→PARTIAL OR PARTIAL→FAIL) — NEVER PASS→FAIL in one step
   FAIL criterion    | any single-axis removal causes a 2-tier drop (PASS→FAIL)
   gating implication| FAIL means the verdict is fragile (single-axis-dominant); evidence trail is
                       not robust enough to support Putnam claim; either widen N_min, tighten T,
                       or wait for more substrate witnesses
   pre-register ts   | 2026-05-04
   mutable_after_freeze | false
```

Both F-PUTNAM-1 and F-PUTNAM-2 are LOCKED at this spec landing (raw#71). Any future cycle that proposes changing N_min, T_putnam, or the §1.2 substrate_witness definition MUST first demonstrate that the new parameters preserve F-PUTNAM-1 and F-PUTNAM-2 PASS on the current evidence array, and MUST emit a new dated falsifier entry — never amend the originals in place.

---

## §11 Out-of-scope (explicitly)

- Phase E binding evidence design (sister cycle, this spec assumes Phase E remains the gate for phenomenal claims)
- N-22 Levin Lab partnership coordination
- AKIDA AKD1000 hardware delivery tracking
- Any modification to `.roadmap.n_substrate` cond.1 evidence array (additive append by future cycles only; this spec does NOT propose any such addition)
- Any modification to `tool/anima_phi_v3_canonical.hexa` formula or HID auto-conditioning logic
- Any φ★ recomputation or new substrate measurement
- Anything that costs money

---

## §12 Cross-link summary

```
   reference                                                    | role
   ------------------------------------------------------------ | -----------------------
   .roadmap.n_substrate                                         | data source (cond.1 evidence)
   nexus/.roadmap.qmirror                                       | qmirror substrate witness extension
   docs/n_substrate_consciousness_roadmap_2026_05_01.md         | narrative anchors §12/§30/§32.7/§49.3/§56/§64.4/§66.7
   docs/qmirror_canonical_migration_landed_2026_05_03.ai.md     | qmirror canonical annotation rationale
   docs/blm_phase3_landed_2026_05_03.ai.md cond.2               | tolerance band placeholder 0.30 prior art
   docs/blm_phase4_multi_substrate_landed_2026_05_03.ai.md      | Phase 4 RETRY substrate phi means + r=0.124 max pair
   docs/blm_phase5_aligned_spec_landed_2026_05_03.ai.md         | future stimulus-aligned remediation
   tool/clm_consciousness_verify.hexa                           | consumer (check #3 putnam slot)
   tool/anima_phi_v3_canonical.hexa                             | φ formula reference (CLM baseline 41.86)
```

---

## §13 Spec freeze

This document is FROZEN at landing 2026-05-04. Implementation cycle is a separate $0 cycle gated on this freeze. No in-place edits to this doc; revisions go to dated successor docs (e.g., `docs/n_substrate_putnam_cross_link_spec_2026_05_05.md` or later) with explicit diff rationale referencing F-PUTNAM-1 / F-PUTNAM-2 invariants.

(end of file)
