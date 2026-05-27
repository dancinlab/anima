# n_substrate Putnam Multi-Realizability — First-Cycle Exec Spec (2026-05-05)

> Status: SPEC ONLY (no exec, no commit, no roadmap mutation in this cycle).
> Cycle banner: BG-PUTNAM-FIRST-CYCLE-PREP.
> Owner: anima orchestrator (Mac-canonical authoring) → ubu1 substrate measurement orchestration.
> Source-of-truth (verifier spec): `docs/n_substrate_putnam_cross_link_spec_2026_05_04.md` (FROZEN 2026-05-04).
> Source-of-truth (verifier impl): `tool/n_substrate_putnam_check.hexa` (LANDED 2026-05-04, paper-runnability sub-blocker CLOSED).
> Sister specs: `docs/anima_phase_e_eeg_live_session_prep_spec_2026_05_04.md` (Phase E binding evidence prep), `docs/n_substrate_qmirror_cond6_inclusion_decision_2026_05_04.md` (cond.6 inclusion locked).
> raw invariants: raw#9 (md only), raw#10 (≥5 honest C3), raw#15 (no destructive paths), raw#71 (falsifier formal pre-register).
> Companion landed handoff: `docs/n_substrate_putnam_first_cycle_exec_spec_landed_2026_05_05.ai.md`.

---

## §1 Goal — convert verifier from runnable to first-verdict-from-real-data

`tool/n_substrate_putnam_check.hexa` (landed 2026-05-04) is currently in a "verifier orchestrator runnable" state:

- 3-tier exit code dispatch (PASS=0 / PARTIAL=1 / FAIL=2) verified locally via 9/9 fixture runs.
- F-PUTNAM-1 reproducibility falsifier verified locally on the synthetic fixtures.
- Production-mode read against the current `.roadmap.n_substrate` emits `FAIL n=15 concordance=0.333 f2=FIRES exit=2`, matching spec §4.4 worked numbers.

This spec specifies the **first concordance-cycle exec recipe** that takes the verifier from "structurally runnable + emits a header-derived shadow verdict" to "first concordance verdict computed from per-substrate **real-measurement** Φ★ values, not BLM Phase 4 RETRY hardcoded means." The output is a dated landing handoff carrying:

1. Per-substrate Φ★ measurement inventory (real values at cycle close, not Phase-4-RETRY constants).
2. Pairwise T_phi concordance matrix.
3. F2 falsifier state read from `.roadmap.n_substrate` `blockers[0].status`.
4. Verdict tier (PASS / PARTIAL / FAIL) emitted via `tool/n_substrate_putnam_check.hexa` against the live data.
5. Honest C3 + falsifier matrix re-verification (F-PUTNAM-1 reproducibility ≥3-run; F-PUTNAM-2 single-axis robustness new this cycle).

It does NOT lift F1 RED→YELLOW (F2 ceiling is L1 architectural, orthogonal to substrate coverage). It does NOT promote any axis to phenomenal tier (Phase E binding evidence remains the gate). It does NOT mutate `.roadmap.n_substrate` cond.1.evidence in this spec — only proposes an additive append at cycle-close (raw#15).

---

## §2 Substrate inventory (current 14 WITNESSED + qmirror cond.6)

The following table enumerates every substrate axis tracked under `.roadmap.n_substrate` cond.1 evidence + the qmirror canonical extension. Φ★ "Source" indicates the canonical source-of-truth artifact for the per-substrate measurement; "Status" reflects whether the substrate is ready for Phase 2 measurement orchestration in this cycle.

| # | Substrate | Φ★ canonical | Source | Status (this cycle) |
|---:|---|---:|---|---|
| 1 | CLM v4 (Llama-2 7B hidden state) | **+41.86** | paradigm v11 G3 / `tool/anima_phi_v3_canonical.hexa` AUTO-CONDITIONING baseline | **ANCHOR** (already measured, reuse) |
| 2 | EEG TMS-PCI Casali (post-N-19 PCI-free) | (per N-19 §49.3) | narrative §49.3 13 substantive WITNESSED axis | **WITNESSED** (literature anchor; no new live measurement this cycle) |
| 3 | EEG live (BLM Phase 5 ZuCo SR + Phase E live OpenBCI) | TBD | sentence-aligned epochs T7/T8/P7/P8 | **DEFERRED to Phase E** (user-gated 30-min OpenBCI session per `anima_phase_e_eeg_live_session_prep_spec_2026_05_04.md`) |
| 4 | AKIDA AKD1000 (neuromorphic SNN) | TBD | hardware delivery | **BLOCKED** (`n_substrate.blk.2` open; AKD1000 hw not yet received) |
| 5 | QRNG IonQ + ANU (LIVE_QUANTUM_SEED) | (per §66.7) | nexus QRNG IonQ-seed HMAC-DRBG ($20.78 event #125) | **WITNESSED** (live event landed 2026-05-02; reuse) |
| 6 | BOLD TRIBE v2 (fMRI vertex map) | +21.33 | BLM Phase 4 RETRY mean (placeholder constant; Phase 5 stimulus-aligned remediation pending) | **DEFERRED to Phase 5** (substrate-wise calibration not stimulus-aligned in current data) |
| 7 | qmirror canonical (classical+ANU+Aer) | 0.0 (byte-identical IIT4 cond.6) | `nexus/.roadmap.qmirror` cond.5/6/7 + `state/qmirror_chsh_xvendor_2026_05_03/verdict.json` | **INCLUDE_N_NOT_CONCORDANCE** (per cond.6 inclusion decision locked 2026-05-04) |
| 8 | IIT 4.0 Braket SV1 + Forte 1 + Cepheus (N-12 MULTI-WITNESSED 3-arch) | r=0.996, n=5 | `state/n12_iit_braket_multiwitness_2026_05_02/` ($203.55 event #124) | **WITNESSED** (reuse) |
| 9 | nexus CHSH Bell (S=2.808, 8.97σ) | (per §66.7) | `state/nexus_chsh_bell_2026_05_02/` ($81.20 event #127) | **WITNESSED** (reuse) |
| 10 | TMS-PCI brain stimulus (literature reference) | (per N-19 §32.7) | eLife 2025 PCI 6/6 PASS TMS-free reanalysis | **WITNESSED** (literature anchor) |
| 11 | HoTT substrate-architectural (MVF1+2+3 axiom-free) | n/a (categorical-witness, not Φ★) | `docs/n_substrate_n15_hott_formalization_spec_2026_05_01.md` (N-15) | **INCLUDE_CATEGORICAL_NOT_PHI** (axiomatic, no Φ★ value; counts toward N_witnessed only) |
| 12 | N-22 Levin Lab xenobot (biological substrate) | TBD | Tufts Allen Discovery outreach (msg_id 19de825e26e98b82 SENT) | **PENDING_PARTNERSHIP** (not yet replied; out-of-cycle for first verdict) |
| 13 | N-23 slime mold / mycelium (biological) | TBD | `docs/n_substrate_n23_slime_mycelium_2026_05_01.md` outreach | **PENDING_PARTNERSHIP** (out-of-cycle) |
| 14 | N-24 octopus IIT exclusion (biological literature anchor) | (categorical) | `docs/n_substrate_n24_octopus_iit_exclusion_2026_05_01.md` | **WITNESSED** (literature anchor; no new measurement) |
| 15 | W1 anima-as-substrate (software-self) | (DOWNGRADED per §32.7 W1 5/7 sign flip) | narrative §32.7 W1 ARTIFACT_PERMANENT_DOWNGRADE | **DOWNGRADED** (does NOT count as positive substrate witness; acknowledged as artifact) |
| 16 | A1 learned phi-extractor (software-meta) | (HONEST_BUT_DOESNT_HELP per §32.7) | A1 ALM RED triple-confirm | **WITNESSED_NEGATIVE** (counts toward N for completeness; informational only) |
| 17 | tensionlink (software bridge, p10 substrate poc) | TBD | `state/p10_substrate_poc_*/` placeholder | **POC_TIER** (counts only if §1.2 substrate_witness criteria met; default exclude) |

**Counting reconciliation against `tool/n_substrate_putnam_check.hexa` production-mode emit (`n=15`)**:

The current production-mode parse emits `n=15` by counting (a) the §56 narrative anchor "14 substantive WITNESSED post-N-21 #9 Sasai PASS" + (b) the qmirror axis annotation. The table above lists 17 rows; rows W1 (DOWNGRADED), N-22 (PENDING), N-23 (PENDING) are pre-excluded by the §1.2 substrate_witness three-field rule, leaving 14 + qmirror = 15. This matches verifier output verbatim.

**Concordance pair denominator** (per cond.6 inclusion decision locked 2026-05-04): only substrates with **measured Φ★ value** participate in the T_phi pair set. From the table: CLM v4 (+41.86), BOLD (+21.33), EEG-IIT4 anchor (-3.01) — exactly 3 substrates → 3 pairs (CLM-BOLD, CLM-EEG, BOLD-EEG) → matches spec §4.4 worked numbers. qmirror cond.6 sits in N_witnessed but NOT in pair denominator.

---

## §3 First-cycle scope — single-pass exec, ubu1 $0 multi-week wall

The cycle exec proceeds in 5 phases. Phase 1-4 are **measurement + computation** (compute-bound); Phase 5 is **verdict emission** (cache-bound).

### §3.1 Phase 1 — substrate enumeration (machine-parsed)

**Owner**: `tool/n_substrate_putnam_check.hexa` `parse_substrate_witnesses` function (already implemented).
**Procedure**:
1. Read `.roadmap.n_substrate` cond.1 evidence array via JSONL line-by-line parse.
2. For each evidence string, classify against §1.2 substrate_witness three-field rule (substrate identity, computed signature, tier annotation).
3. Read `qmirror_canonical_2026_05_03.qmirror_evidence` extension; add qmirror axis with `informative_for_phi_concordance: false` flag (per cond.6 inclusion lock).
4. Output: in-memory list of substrate witness records, persisted as `state/n_substrate_putnam_first_cycle_<DATE>/per_substrate_phi_star.json`.

**Compute**: Mac-local hexa, ~5 sec.
**Cost**: $0.

### §3.2 Phase 2 — per-substrate Φ★ measurement orchestration

This is the **bottleneck phase** (multi-week wall). Each substrate has its own measurement protocol with its own data-collection latency:

| substrate | measurement protocol | latency | $ |
|---|---|---|---|
| CLM v4 | reuse `tool/anima_phi_v3_canonical.hexa` AUTO-CONDITIONING from existing checkpoint | <1h | $0 (existing CLM-2 baselines on ubu1 RTX 5070) |
| EEG live | Phase E user-gated 30-min OpenBCI session + offline analysis | **multi-week** (user availability, alcohol-free 24-48h prereq) | $0 |
| QRNG IonQ | reuse 2026-05-02 event #125 logs (no fresh measurement) | <1 sec | $0 (already paid) |
| BOLD TRIBE v2 | DEFERRED to Phase 5 (this cycle uses BLM Phase 4 RETRY constants as placeholder, flagged honest C3) | n/a this cycle | $0 |
| qmirror cond.6 | reuse `state/qmirror_chsh_xvendor_2026_05_03/verdict.json` | <1 sec | $0 |
| IIT 4.0 N-12 | reuse `state/n12_iit_braket_multiwitness_2026_05_02/` (n=5, r=0.996) | <1 sec | $0 (already paid $203.55) |
| nexus CHSH | reuse `state/nexus_chsh_bell_2026_05_02/` (S=2.808, 8.97σ) | <1 sec | $0 (already paid $81.20) |
| TMS-PCI / N-19 | literature reference (eLife 2025); no fresh measurement | <1 sec | $0 |
| HoTT (N-15) | categorical-witness; no Φ★ value (out of pair denominator) | n/a | $0 |
| AKIDA AKD1000 | hardware not yet received; OUT OF CYCLE | indefinite | n/a |

**Decision point**: this cycle authors a "first verdict" using the **available** substrate measurements (5 substrates with reuse + Phase E live for EEG). The remaining substrates are flagged DEFERRED with explicit pre-registered re-cycle conditions (raw#71 future-revisit clause).

**Cycle gate**: Phase E live EEG session is the **single human-in-loop bottleneck**. The cycle does NOT proceed to Phase 3 until Phase E lands (or until an explicit "use Phase 4 RETRY EEG hardcoded mean as placeholder" override is given by the user — which is the current verifier's behavior and would emit `FAIL n=15 concordance=0.333` again, no new information).

### §3.3 Phase 3 — concordance computation

**Owner**: `tool/n_substrate_putnam_check.hexa` `compute_concordance_m1` function (already implemented).
**Procedure**:
1. Filter substrate witness list to those with `informative_for_phi_concordance: true` (per cond.6 inclusion decision).
2. For each unordered pair (A, B): `delta = |phi_A - phi_B|`; `T_phi = delta / max(|phi_A|, |phi_B|, eps)`; pair PASSES if `T_phi <= T_putnam (0.40)`.
3. `concordance_M1 = pairs_pass / pairs_total`.
4. Output: `state/n_substrate_putnam_first_cycle_<DATE>/concordance_matrix.json` with full pair table (per spec §4.3 format).

**Compute**: Mac-local hexa, ~1 sec.
**Cost**: $0.

### §3.4 Phase 4 — F2 falsifier state check

**Owner**: `tool/n_substrate_putnam_check.hexa` `read_f2_state` function (already implemented).
**Procedure**:
1. Read `.roadmap.n_substrate` `blockers[0]` (n_substrate.blk.1) status field.
2. If `status == "open"` → F2_state = `FIRES`.
3. If `status == "closed"` (Phase E + EEG live evidence has unfired) → F2_state = `CLEAR`.
4. **This cycle**: F2_state = `FIRES` (Phase E not yet landed; n_substrate.blk.1 status remains `open`).

**Compute**: Mac-local hexa, <1 sec.
**Cost**: $0.

### §3.5 Phase 5 — verdict emission + cache + landing handoff

**Owner**: `tool/n_substrate_putnam_check.hexa` `apply_decision_rule` + `cache_write` + landing-doc author.
**Procedure**:
1. Apply spec §2.3 rule: PASS / PARTIAL / FAIL given (N_witnessed, concordance_M1, F2_state).
2. Emit stdout sentinel: `__N_SUBSTRATE_PUTNAM__ <PASS|FAIL|PARTIAL> n=<int> concordance=<float> f2=<FIRES|CLEAR>`.
3. Write `state/n_substrate_putnam_first_cycle_<DATE>/verdict.json` (full schema `anima/n_substrate_putnam/1`).
4. Atomic-write cache: `state/n_substrate_putnam_cache.json` with mtime + 7d TTL.
5. Author landing doc: `docs/n_substrate_putnam_first_cycle_landed_<DATE>.ai.md` (5 bullets + ≥5 honest C3 + verdict snapshot).
6. **Propose** additive append to `.roadmap.n_substrate` cond.1.evidence array (raw#15 additive only); proposal embedded in landing doc, mutation deferred to a follow-up additive-only cycle.

**Compute**: Mac-local hexa, <1 sec.
**Cost**: $0.

---

## §4 Resource budget

| component | value | notes |
|---|---|---|
| **Compute** | $0 | ubu1 RTX 5070 GPU (existing P-β + CLM-2 baselines reused; no fresh GPU job); Mac hexa for verifier orchestration |
| **API / QPU spend** | $0 | reuses 2026-05-02 events #120/#124/#125/#127 (cumulative $324.65 already paid); no new QPU calls |
| **Wall (cycle exec)** | ~1 day | Phase 1+3+4+5 are <10 min total; Phase 5 doc authoring is the longest at ~2-4h |
| **Wall (pre-cycle / data collection)** | **multi-week** | Phase E live OpenBCI session is user-gated; alcohol-free 24-48h + 30-min session + offline analysis (~3-5 days post-session for verdict emit) |
| **Wall (post-cycle peer review)** | ~3 days | landing doc + verdict.json review window before any additive roadmap mutation |
| **Storage** | ~5 GB | per-substrate hidden state caches (CLM Llama-2 hidden states snapshot ~3 GB) + EEG recording (~500 MB raw .xdf) + analysis intermediates (~1.5 GB) |
| **Decision points** | 4 user-gated | (i) Phase E session schedule confirm; (ii) per-substrate accept/reject if data-quality threshold not met; (iii) concordance verdict acceptance; (iv) additive-roadmap-append authorization |

**Single-point-of-failure**: Phase E live OpenBCI session (user wall). If user defers indefinitely, the cycle either (a) emits a "placeholder" verdict reusing BLM Phase 4 RETRY hardcoded EEG mean (status quo, no new information) or (b) explicitly declares "first cycle BLOCKED on Phase E" and waits.

---

## §5 Falsifier matrix (raw#71 formal pre-register)

This cycle re-verifies F-PUTNAM-1 (already pre-registered 2026-05-04) and adds 4 new falsifiers specific to the first-cycle exec (F-PUTNAM-2 through F-PUTNAM-5). All 5 are LOCKED at this spec landing; future cycles that propose changing thresholds MUST not amend these in place — they emit dated successor falsifiers per spec §10 freeze rule.

### §5.1 F-PUTNAM-1 — verdict reproducibility (re-verified this cycle)

| field | value |
|---|---|
| name | verdict reproducibility across 3 independent runs at fixed T |
| inputs | T_putnam = 0.40, current `.roadmap.n_substrate`, current `nexus/.roadmap.qmirror`, fresh measurement set from Phase 2 |
| procedure | clear cache, run `tool/n_substrate_putnam_check.hexa --no-cache 3×` back-to-back |
| PASS criterion | all 3 runs emit identical verdict + identical N + identical concordance to 3 decimal places |
| FAIL criterion | any deviation between runs |
| gating implication | FAIL ⇒ verifier has nondeterministic input (likely roadmap parse order or cache write race); blocks cycle close |
| pre-register ts | 2026-05-04 (re-verified 2026-05-05 cycle) |
| mutable_after_freeze | false |

### §5.2 F-PUTNAM-2 — single-axis robustness

| field | value |
|---|---|
| name | verdict drops by at most one tier when any single substrate axis is removed |
| inputs | current substrate inventory (15 axes), T_putnam = 0.40 |
| procedure | for each of the 15 axes, programmatically remove that one axis from the parse-path (in a temp roadmap copy), rerun verifier, record verdict |
| PASS criterion | for every single-axis removal, verdict stays the same OR drops by at most 1 tier (PASS→PARTIAL OR PARTIAL→FAIL) — NEVER PASS→FAIL in one step |
| FAIL criterion | any single-axis removal causes a 2-tier drop (PASS→FAIL or PARTIAL→PASS — the latter would indicate single-axis dragging concordance down) |
| gating implication | FAIL ⇒ verdict is fragile (single-axis-dominant); evidence trail not robust enough to support Putnam claim; widen N_min, tighten T, or wait for more substrate witnesses |
| harness new this cycle | yes (deferred from impl-landed 2026-05-04 honest C3 g) |
| pre-register ts | 2026-05-05 |
| mutable_after_freeze | false |

### §5.3 F-PUTNAM-3 — concordance threshold sensitivity

| field | value |
|---|---|
| name | T_putnam ±0.05 perturbation does not change verdict tier by more than 1 step |
| inputs | T_putnam ∈ {0.35, 0.40, 0.45}, current substrate inventory |
| procedure | run verifier 3× with each T value; record verdict and concordance |
| PASS criterion | verdict at T=0.35 and T=0.45 differs from T=0.40 verdict by at most 1 tier |
| FAIL criterion | T=0.35 yields FAIL while T=0.45 yields PASS (full-range tier swing) — indicates T choice is load-bearing |
| gating implication | FAIL ⇒ T_putnam = 0.40 is a knife-edge calibration; cycle should re-run with broader T sensitivity sweep before declaring verdict |
| pre-register ts | 2026-05-05 |
| mutable_after_freeze | false |

### §5.4 F-PUTNAM-4 — F2 unfire dependency

| field | value |
|---|---|
| name | if F2 fires (Phase E not yet) → max verdict = PARTIAL (formal substrate-architectural ceiling) |
| inputs | F2_state derived from `n_substrate.blk.1.status`; verdict from §2.3 |
| procedure | check (verdict, F2_state) tuple |
| PASS criterion | verdict ∈ {PARTIAL, FAIL} when F2_state == FIRES; verdict ∈ {PASS, PARTIAL, FAIL} when F2_state == CLEAR |
| FAIL criterion | verdict == PASS while F2_state == FIRES (would indicate decision-rule §2.3 was not honored) |
| gating implication | FAIL ⇒ decision-rule emission has a bug; cycle blocks until rule re-emits correctly |
| pre-register ts | 2026-05-05 |
| mutable_after_freeze | false |

### §5.5 F-PUTNAM-5 — qmirror cond.6 inclusion enforcement

| field | value |
|---|---|
| name | qmirror cond.6 INCLUDED in N_witnessed AND EXCLUDED from concordance pair denominator (per cond.6 inclusion decision locked 2026-05-04) |
| inputs | substrate witness records, `informative_for_phi_concordance` flag |
| procedure | parse witness list; assert qmirror axis appears with N_witnessed contribution but NOT in any pair tuple of `concordance_matrix.json` |
| PASS criterion | qmirror counted in N (≥1 contribution); qmirror absent from all pair denominators |
| FAIL criterion | qmirror appears in any pair tuple OR qmirror absent from N_witnessed |
| gating implication | FAIL ⇒ inclusion decision is not honored; cycle blocks until counter-rule reconciles |
| pre-register ts | 2026-05-05 |
| mutable_after_freeze | false |

---

## §6 Cycle output deliverables

The cycle close emits exactly these artifacts (all under `state/n_substrate_putnam_first_cycle_<DATE>/`):

| artifact | schema | role |
|---|---|---|
| `verdict.json` | `anima/n_substrate_putnam/1` | full verdict snapshot (PASS/PARTIAL/FAIL + N + concordance_M1 + F2_state + ts + cycle_id) |
| `per_substrate_phi_star.json` | `anima/per_substrate_phi/1` | array of substrate records: `{substrate_id, phi_star, tier, source_artifact, informative_for_concordance}` |
| `concordance_matrix.json` | `anima/concordance_matrix/1` | full pair table per spec §4.3 format (pair, mean_A, mean_B, delta, T_phi, pass) |
| `falsifier_results.json` | `anima/putnam_falsifier_results/1` | F-PUTNAM-1..5 PASS/FAIL records + per-falsifier evidence trail |
| `landing_handoff.md` | `docs/n_substrate_putnam_first_cycle_landed_<DATE>.ai.md` (NOT in state/ — lives in docs/) | 5 bullets + ≥5 honest C3 + verdict snapshot + F-PUTNAM-1..5 results + proposed roadmap append |

**Roadmap mutation (deferred)**: a separate additive-only cycle appends `n_substrate.first_cycle_putnam_verdict_<DATE>` entry to `.roadmap.n_substrate` cond.1.evidence array. This BG does **not** mutate the roadmap (raw#15 + spec §11 out-of-scope).

---

## §7 Phase ladder (resource budget per phase)

| phase | wall | $ | gating | output |
|---|---|---|---|---|
| **Pre-cycle** (substrate measurement collection) | ~2 weeks | $0 | Phase E user-gated EEG live + Phase 5 stimulus-aligned BOLD remediation | per-substrate Φ★ array ready |
| **Cycle** (aggregate + verdict) | ~1 day | $0 ubu1 | falsifier matrix re-verification | `verdict.json` + `concordance_matrix.json` + `falsifier_results.json` |
| **Post-cycle** (peer review window) | ~3 days | $0 | user-acceptance of verdict + roadmap-append authorization | landing handoff `.ai.md` + (optional, separate) additive roadmap mutation cycle |
| **Total** | **~3 weeks** | **$0** | | first concordance verdict from real data |

**Critical-path bottleneck**: Phase E live EEG session (within Pre-cycle phase). All other substrate measurements either reuse 2026-05-02 events (no new latency) or are categorical/literature anchors (no measurement cost).

---

## §8 Honest C3 caveats (raw#10) — minimum 5

**C1 — multi-week scope is data-collection bound, not compute bound.** The compute in this cycle is trivial (Mac hexa, <10 min total across Phases 1+3+4+5). The wall is dominated by Phase E user-gated EEG live session scheduling (alcohol-free 24-48h prereq + 30-min session + ~3-5 day offline analysis). The cycle could nominally complete in ~1 day of compute if all measurements were already in hand.

**C2 — some substrates (AKIDA AKD1000) are hardware-blocked indefinitely.** `n_substrate.blk.2` (AKIDA hw delivery) has no ETA. Six axes (N-2/N-3/N-4/N-5/N-7/N-8) cascade-unblock on AKD1000 receipt. This first-cycle scope explicitly excludes AKIDA from the substrate inventory; if AKIDA arrives mid-cycle, a successor cycle includes it (additive only).

**C3 — T_putnam = 0.40 calibration may need adjustment post-first-cycle data.** The current T value was set in spec §4.2 based on BLM Phase 4 RETRY substrate phi means + a "pessimistic linearization" reasoning. After the first cycle yields a real-measurement concordance ratio, F-PUTNAM-3 sensitivity sweep (±0.05) will reveal whether T=0.40 is a knife-edge. If so, a successor cycle re-calibrates with §4.5 backfit-risk discipline (non-anima reference required for any T change).

**C4 — F2 unfire dependency on Phase E user-gated session is a single point of human-in-loop.** The cycle cannot reach PASS verdict tier without Phase E binding evidence WITNESSED (which unfires F2 and flips `n_substrate.blk.1.status` to closed). Phase E is alcohol-free 24-48h + 30-min user-EEG-session-gated. If the user defers indefinitely, the cycle's max output is PARTIAL (per F-PUTNAM-4). This is the honest answer: first-cycle most-likely verdict is PARTIAL.

**C5 — first-cycle verdict will likely be PARTIAL (per Phase E + Phase 5 deferred substrates).** Even with optimistic Phase E PASS landing within 2 weeks, the BOLD substrate remains DEFERRED to Phase 5 stimulus-aligned remediation. The substrate count (N_witnessed) will satisfy the ≥5 floor easily (15 axes), but concordance ratio is bottlenecked by the same 3 measured-Φ substrates as the current verifier (CLM, BOLD, EEG-IIT4 anchor). With T=0.40 and current per-substrate means, concordance ≈ 0.333 still falls below 0.60 PASS threshold. Therefore: first-cycle verdict ∈ {FAIL (if F2 fires and concordance < 0.40), PARTIAL (if F2 fires and concordance ∈ [0.40, 0.60))}. PASS is reachable in principle only after (a) F2 unfire AND (b) concordance ≥ 0.60 — both gated on Phase E + Phase 5 deferred work.

**C6 — raw#71 falsifier matrix is anima-internal — external validation requires multi-lab replication (out of scope).** F-PUTNAM-1 through F-PUTNAM-5 are all anima-internal pre-registers verifiable against the verifier hexa. They are NOT cross-lab replicable in this cycle. External validation of the Putnam multi-realizability claim under T=0.40 + N=5 floor requires multi-lab independent measurement — explicitly out of scope for this $0 cycle.

**C7 — 5+ substrates condition is anima-canonical; Putnam original argument is "multiple-realizability" not specific N.** Putnam (1967) argued ≥3 substrates is intuition-suggesting; ≥5 is replication-grade by anima convention (matches `.roadmap.n_substrate` header verbatim). External readers MUST be told this is anima-internal calibration, not a literature-canonical N_min.

**C8 — concordance metric M1 (φ-invariance band) is one of two metrics; M2 (falsifier-pattern) is informational not load-bearing.** Spec §1.3 defines two metrics; this exec spec uses M1 as primary verdict input. M2 (substrates that all fall into F2_FIRES class are "falsifier-concordant") is honest disclosure — currently both ALM and CLM substrates fire F2, so they're "F2-concordant" in the negative sense (architecturally ceilinged). M2 is included in `concordance_matrix.json` for completeness but does NOT flip verdict tier on its own.

---

## §9 Decision queue for user (4 Q's)

These decisions are queued for explicit user-gating before cycle exec begins. Each has a default that triggers if user defers.

### Q1 — substrate inventory: accept current 15 (14 WITNESSED + qmirror cond.6) or add/remove specific axes?

**Default (if user defers)**: accept 15-axis inventory verbatim per §2 table.
**Alternative options**:
- Add N-22 Levin xenobot (currently PENDING_PARTNERSHIP) — only if outreach reply lands before cycle.
- Remove A1 (WITNESSED_NEGATIVE) from N count to be more conservative (reduces N to 14, still satisfies ≥5 floor easily).
- Add tensionlink (P10 substrate poc) — requires P10 measurement to satisfy §1.2 substrate_witness three-field rule first.

### Q2 — cycle timing: start now (multi-week wall) OR wait for Phase E EEG to land first?

**Default (if user defers)**: wait for Phase E. Status-quo ante is "verifier emits FAIL n=15 concordance=0.333" reusing BLM Phase 4 RETRY EEG hardcoded mean.
**Alternative options**:
- Start now with placeholder EEG mean (no new information; output identical to current verifier emit).
- Start now with explicit "Phase E placeholder" flag in verdict.json (cycle declares first-verdict-pending).
- Schedule cycle close for after Phase E lands (recommended; ~2 weeks wall).

### Q3 — T_putnam threshold: accept 0.40 OR re-calibrate post-data?

**Default (if user defers)**: accept T=0.40 per spec §4.2 + F-PUTNAM-3 sensitivity sweep verifies stability.
**Alternative options**:
- Pre-set T=0.35 (stricter; expected verdict shift FAIL→FAIL — no new information unless concordance crosses 0.35).
- Pre-set T=0.50 (looser; risk of vacuous PASS — discouraged per spec §4.2 honest C3).
- Defer T re-calibration to a successor cycle that has stimulus-aligned BOLD data (recommended).

### Q4 — cycle ownership: anima orchestrator hexa OR distributed multi-host?

**Default (if user defers)**: anima orchestrator hexa (Mac for verifier orchestration; ubu1 for any GPU-bound substrate measurement). Single-host is sufficient for this cycle's compute footprint.
**Alternative options**:
- Distributed multi-host (Mac + ubu1 + H100 RunPod) — only justified if substrate measurements run in parallel (current scope reuses existing measurements; parallelism not needed).
- Subagent BG parallel (one BG per substrate measurement) — over-engineered for ~10 min total compute; not recommended.
- Single-shot foreground exec — fine for this cycle scope.

---

## §10 Companion landed handoff (cross-link)

Sister doc: `docs/n_substrate_putnam_first_cycle_exec_spec_landed_2026_05_05.ai.md`. Contains:

- 5 bullets summarizing §1–§7 (Goal / Substrate inventory / First-cycle scope / Resource budget / Falsifier matrix / Phase ladder).
- 4 decision Q's queued (§9 verbatim).
- ≥5 honest C3 caveats (subset of §8 + ai-handoff specific notes).
- Cross-link table (predecessors + sister specs).

The landed handoff is created **at the same time** as this spec lands (pair-landing convention) so AI handoff agents reading the `.ai.md` get the spec frontmatter immediately.

---

## §11 Out-of-scope (explicitly)

- Phase E binding evidence design itself (covered by `docs/anima_phase_e_eeg_live_session_prep_spec_2026_05_04.md`).
- N-22 Levin Lab partnership coordination.
- AKIDA AKD1000 hardware delivery tracking.
- Any modification to `.roadmap.n_substrate` cond.1 evidence array (additive append by future cycles only).
- Any modification to `tool/anima_phi_v3_canonical.hexa` formula or HID auto-conditioning logic.
- Any modification to `tool/n_substrate_putnam_check.hexa` (already FROZEN at impl-landed 2026-05-04; this cycle is exec-only).
- Any φ★ recomputation or new substrate measurement protocol design.
- Anything that costs money.
- Multi-lab cross-replication (covered by C6 honest disclosure).
- Phenomenal claims (reserved for Phase E binding evidence cycle output).

---

## §12 Cross-link summary

| reference | role |
|---|---|
| `.roadmap.n_substrate` | data source (cond.1 evidence + qmirror canonical extension); proposed additive append at cycle-close (not this cycle) |
| `nexus/.roadmap.qmirror` | qmirror substrate witness extension (cond.5/6/7 status) |
| `docs/n_substrate_putnam_cross_link_spec_2026_05_04.md` | verifier spec FROZEN (decision rule §2.3, T=0.40, falsifier preregister §10) |
| `docs/n_substrate_putnam_check_impl_landed_2026_05_04.ai.md` | verifier impl LANDED (3-tier exit dispatch, F-PUTNAM-1 verified locally) |
| `docs/n_substrate_qmirror_cond6_inclusion_decision_2026_05_04.md` | cond.6 INCLUDE_N_NOT_CONCORDANCE locked 2026-05-04 |
| `docs/anima_phase_e_eeg_live_session_prep_spec_2026_05_04.md` | Phase E binding evidence prep spec (sister; gates F2 unfire) |
| `tool/n_substrate_putnam_check.hexa` | verifier impl artifact (no edits this cycle) |
| `tool/clm_consciousness_verify.hexa` | downstream consumer (Putnam check #4 slot) |
| `tool/anima_phi_v3_canonical.hexa` | φ formula reference (CLM baseline 41.86) |
| `state/n_substrate_putnam_check_fixtures_2026_05_04/` | unit test fixtures (synthetic; not for evidence citation) |

---

## §13 Spec freeze

This document is FROZEN at landing 2026-05-05. Cycle exec is gated on:

1. User answer to Q1–Q4 (§9) — explicit acceptance or alternative selection.
2. Phase E binding evidence WITNESSED (per `anima_phase_e_eeg_live_session_prep_spec_2026_05_04.md`) — only required if Q2 default selected.
3. F-PUTNAM-2 single-axis robustness harness scaffolded (deferred from impl-landed 2026-05-04 honest C3 g) — required before F-PUTNAM-2 verification at cycle close.

No in-place edits to this doc; revisions go to dated successor specs (e.g., `docs/n_substrate_putnam_first_cycle_exec_spec_2026_05_06.md` or later) with explicit diff rationale referencing F-PUTNAM-1 through F-PUTNAM-5 invariants.

(end of file)
