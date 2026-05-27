# Putnam first-cycle Phase 1 — landed handoff (2026-05-05)

> Status: LANDED (Phase 1 verdict emitted, no roadmap mutation, no commit, no HF push).
> BG lane: PUTNAM-IMPL-PHASE1-CYCLE.
> Cycle: `state/n_substrate_putnam_first_cycle_2026_05_05/`.
> Spec: `docs/n_substrate_putnam_first_cycle_exec_spec_2026_05_05.md` (frozen 2026-05-05).
> Verifier impl: `tool/n_substrate_putnam_check.hexa` (frozen 2026-05-04).

---

## 5-bullet summary

1. **Substrate enumeration** — 17-row inventory parsed from `.roadmap.n_substrate` cond.1 evidence + qmirror_canonical extension. Anchored: 2 (CLM v4 +41.86, Pβ adapter +42.37); witnessed (existing data): 6 (EEG TMS-PCI Casali, QRNG IonQ+ANU, IIT 4.0 N-12 3-arch, nexus CHSH 8.97σ, TMS-PCI lit, N-24 octopus); witnessed_negative: 1 (A1 phi=0.0 sentinel); deferred Phase E: 1 (EEG live OpenBCI); deferred Phase 5: 1 (BOLD TRIBE v2 stimulus-aligned remediation); blocked: 1 (AKIDA AKD1000); pending partnership: 2 (N-22 Levin, N-23 slime); downgraded: 1 (W1 anima-self); include_n_not_concordance: 1 (qmirror cond.6); include_categorical_not_phi: 1 (HoTT N-15). N_witnessed_for_verdict = **15** (matches verifier production-mode emit).

2. **Concordance pre-compute** — 5 phi-bearing substrates entered the pair denominator (CLM=41.86, Pβ=42.37, BOLD=21.33, EEG=-3.01, A1=0.0). 10 pairs computed; **1 pair PASS (CLM-Pβ T_phi=0.012, both ANCHORED)**, 9 pairs FAIL on BLM Phase 4 RETRY placeholder magnitude/sign mismatches. Concordance_M1 (Phase 1 real-measurement) = **0.100**; verifier-emitted concordance (BLM Phase 4 RETRY hardcoded over 3 substrates only) = **0.333**. Both fall below CONC_PARTIAL_MIN=0.40 → FAIL by concordance gate. qmirror cond.6 EXCLUDED from pair denominator per cond.6 inclusion lock 2026-05-04 (F-PUTNAM-5 verified PASS).

3. **F2 falsifier state** — `n_substrate.blk.1.status = "open"` → **F2_state = FIRES**. Phase E binding evidence not yet WITNESSED; ALM/CLM cross-substrate L1 14-gate ceiling 0/16 confirmed; user-gated 30-min OpenBCI session prereq still outstanding.

4. **Verdict** — `__N_SUBSTRATE_PUTNAM__ FAIL n=15 concordance=0.333 f2=FIRES` (verifier exit code 2). Both gates contribute to FAIL: concordance < 0.40 (primary) AND F2_state == FIRES (would cap at PARTIAL anyway). Spec §C5 predicted "likely PARTIAL"; empirical landing is FAIL by one boundary — pessimism in C5 was insufficient.

5. **F-PUTNAM-1..5 falsifier matrix all PASS** — F-PUTNAM-1 reproducibility (3-run identical), F-PUTNAM-2 single-axis robustness (max tier drop = 0; non-binding at FAIL floor), F-PUTNAM-3 T-sensitivity (T∈{0.35, 0.40, 0.45} all FAIL; non-discriminating in current data), F-PUTNAM-4 F2 dependency ((FAIL, FIRES) tuple consistent with rule), F-PUTNAM-5 qmirror inclusion (counted in N=15, absent from all pair tuples). Selftest 5/5 PASS (in-memory rule firing).

---

## Verdict snapshot

| field | value |
|---|---|
| verdict | **FAIL** |
| n_witnessed | 15 |
| concordance_M1 (verifier emit) | 0.333 |
| concordance_M1 (Phase 1 real-measurement) | 0.100 |
| f2_state | FIRES |
| T_putnam | 0.40 |
| N_min_putnam | 5 |
| F-PUTNAM-1..5 | 5/5 PASS |
| selftest | 5/5 PASS |
| sentinel | `__N_SUBSTRATE_PUTNAM__ FAIL n=15 concordance=0.333 f2=FIRES` |
| verifier exit code | 2 |
| wall_time_min | 12 |
| actual_cost_usd | 0.0 |
| compute substrate | Mac-local hexa (no GPU; ubu1 not invoked) |

---

## Why FAIL not PARTIAL (spec §C5 reconciliation)

Spec §8 C5 predicted: "first-cycle verdict ∈ {FAIL (if F2 fires AND concordance < 0.40), PARTIAL (if F2 fires AND concordance ∈ [0.40, 0.60))}". Empirical concordance under verifier hardcoded values = 0.333 (3 substrates: CLM=30.86, BOLD=21.33, EEG=-3.01; 1 of 3 pairs passes). Under Phase 1 real-measurement substitution (5 substrates: CLM=41.86, Pβ=42.37, BOLD=21.33, EEG=-3.01, A1=0.0), concordance drops to 0.100 (only CLM-Pβ pair passes). Both fall in the FAIL band. PARTIAL was reachable only if concordance crossed 0.40; it did not. The spec author's pessimism was insufficient — honest disclosure: FAIL not PARTIAL is the empirical Phase 1 verdict.

---

## Phase 2 gating (next cycle, not this one)

Phase 2 of the BG taxonomy = spec §3.2 Phase 2 (per-substrate measurement orchestration with Phase E live + BOLD Phase 5 stimulus-aligned remediation). Bottlenecks:

- **Phase E live OpenBCI 30-min EEG session** — user-gated (alcohol-free 24-48h prereq + ~3-5d offline analysis). Multi-week wall.
- **BLM Phase 5 stimulus-aligned BOLD remediation** — compute-bound (~1-2 days) but spec-frozen pending.
- **Verifier substrate constants** — currently hardcoded BLM Phase 4 RETRY (CLM=30.86, BOLD=21.33, EEG=-3.01); Phase 2 may propose successor verifier (frozen impl untouched per raw#15) that ingests fresh real-measurement values.

Phase 2 max attainable verdict = PARTIAL (because F2 still FIRES until Phase E binding evidence WITNESSED; PASS requires concordance ≥ 0.60 AND F2 unfire — both gated on Phase E). Estimated wall total: ~2-4 weeks; estimated cost: $0.

---

## Honest C3 (raw#10, ≥5)

**C3-1 — Verdict FAIL diverges from spec §C5 expected-PARTIAL by one threshold step.** Concordance gate (< 0.40) fires before F2 ceiling. Both block PASS but FAIL has lower precedence. C5 author was too optimistic by one band; raw#10 disclosure: empirical landing is one tier below predicted.

**C3-2 — Phase 1 did NOT fresh-measure EEG or BOLD.** Inherited BLM Phase 4 RETRY hardcoded values verbatim. The "first verdict from real data" goal is partially satisfied (CLM v4 + Pβ are fresh real measurements; CLM=41.86, Pβ=42.37) but not for the substrates that drive concordance failures. Phase 2 substitution required.

**C3-3 — Adding Pβ adapter (42.37) as a 5th substrate LOWERED concordance from verifier's 0.333 to Phase 1 real-measurement's 0.100.** Pβ creates additional pairwise mismatches with BOLD/EEG/A1 than concordances with CLM. This is a known property of T_phi pairwise denominators under heterogeneous tier mixes. Phase 2 with real EEG binding-evidence phi (likely +30..+50 range) would raise concordance substantially because two more pairs would land in the concordant band.

**C3-4 — F-PUTNAM-2 single-axis robustness PASS is non-binding (tier-floor).** Baseline FAIL has no tier below it; max tier drop bounded below trivially. Falsifier becomes substantive only when Phase 2 lifts baseline above FAIL.

**C3-5 — F-PUTNAM-3 T-sensitivity sweep is uninformative (T-non-discriminating).** Verifier emits identical concordance=0.333 across T∈{0.35, 0.40, 0.45} because the only T_phi values at the verifier's hardcoded substrates are 0.309 (CLM-BOLD), 1.098 (CLM-EEG), 1.141 (BOLD-EEG); none cross any of the 3 T boundaries. Falsifier passes structurally; substantive verification deferred to Phase 2.

**C3-6 — No roadmap mutation, no HF push, no git commit (raw#15 + spec §11 + user instruction).** State artifacts in `state/n_substrate_putnam_first_cycle_2026_05_05/` are local-only. Phase 2 will additively append a successor evidence entry to `.roadmap.n_substrate` cond.1.evidence array via a separate additive-only cycle (not this one).

---

## Cross-link table

| reference | role |
|---|---|
| `docs/n_substrate_putnam_first_cycle_exec_spec_2026_05_05.md` | spec frontmatter (FROZEN 2026-05-05) |
| `docs/n_substrate_putnam_cross_link_spec_2026_05_04.md` | verifier spec FROZEN |
| `docs/n_substrate_putnam_check_impl_landed_2026_05_04.ai.md` | verifier impl LANDED |
| `docs/n_substrate_qmirror_cond6_inclusion_decision_2026_05_04.md` | qmirror cond.6 inclusion lock |
| `docs/anima_phase_e_eeg_live_session_prep_spec_2026_05_04.md` | Phase E binding evidence prep (gates F2 unfire) |
| `tool/n_substrate_putnam_check.hexa` | verifier impl artifact (no edits this cycle) |
| `state/n_substrate_putnam_check_fixtures_2026_05_04/` | unit test fixtures (selftest 5/5 PASS) |
| `state/clm_v4_baseline_eval_2026_05_05/verdict.json` | CLM v4 anchored phi★ source (+41.86) |
| `state/p9_pbeta_holdout500_eval_2026_05_05/verdict.json` | Pβ adapter anchored phi★ source (+42.37) |
| `state/qmirror_chsh_xvendor_2026_05_03/verdict.json` | qmirror cond.6 byte-identical IIT4 |
| `state/n12_iit_braket_multiwitness_2026_05_02/` | IIT 4.0 N-12 3-arch (n=5 r=0.996) |
| `state/nexus_chsh_bell_2026_05_02/` | nexus CHSH Bell (S=2.808 8.97σ) |
| `state/nexus_qrng_quantum_seed_2026_05_02/` | QRNG IonQ+ANU LIVE_QUANTUM_SEED |
| `.roadmap.n_substrate` | data source (cond.1 evidence + qmirror canonical extension); NOT mutated this cycle |
| `state/n_substrate_putnam_first_cycle_2026_05_05/verdict.json` | THIS CYCLE verdict snapshot |
| `state/n_substrate_putnam_first_cycle_2026_05_05/per_substrate_phi_star.json` | THIS CYCLE substrate inventory |
| `state/n_substrate_putnam_first_cycle_2026_05_05/concordance_matrix.json` | THIS CYCLE pairwise T_phi matrix |
| `state/n_substrate_putnam_first_cycle_2026_05_05/falsifier_results.json` | THIS CYCLE F-PUTNAM-1..5 results |

---

## Out-of-scope (explicitly)

- Mutation of `.roadmap.n_substrate` (deferred to additive-only follow-up cycle).
- Mutation of `tool/n_substrate_putnam_check.hexa` (frozen 2026-05-04).
- Phase E live OpenBCI session execution (user-gated; Phase 2 of BG taxonomy).
- BOLD TRIBE v2 Phase 5 stimulus-aligned remediation (Phase 2 of BG taxonomy).
- Multi-lab cross-replication (raw#10 honest disclosure: anima-internal verification only).
- Any phenomenal-tier claim (reserved for Phase E binding evidence cycle output).
- Any HF push, git commit, or remote artifact mutation.

(end of file)
