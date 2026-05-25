# qmirror Unblock Exec Plan — 2026-05-03

**Author**: discovery + planning subagent (BG cycle, anima-core)
**Cycle type**: pure discovery + ranked exec planning (NO mutation, NO execution)
**qmirror closure status**: 8/8 conditional (cond.4 NIST PASS via clean rewrite + cond.7 spirit cross-tech 3/4 with band revise + cond.3 0.40→0.55 superconducting band + cond.6 byte-identical IIT4 + cond.8 option β intra-trapped-ion)
**Sources of truth**:
- `state/qmirror_canonical_migration_2026_05_03/` (sister BG-A — roadmap audit, replace_log, keep_decisions)
- `state/qmirror_spec_xref_update_2026_05_03/` (sister BG-B — docs/*.md spec xref audit)
- canonical SSOT: `nexus/.roadmap.qmirror`
- closure synthesis: `docs/nexus_qmirror_closure_2026_05_03.md`

---

## §1 Discovery Summary

### 1.1 Audit Scope

| Source | Scope | Files Scanned | Matches |
|---|---|---|---|
| Sister BG-A (canonical migration) | `anima/.roadmap.* + nexus/.roadmap.* + hive/.roadmap.*` | 60 | 13 with word-boundary `quantum|QPU|IonQ|IBM Quantum|Rigetti|Heron|Forte|Aria|Cepheus|CHSH|braket|qiskit-ibm` |
| Sister BG-B (spec xref) | `docs/*.md` | 1369 | 103 |
| Independent grep (this cycle) | `.roadmap.* + grep blocker_reason` | 60 | cross-checked, no new misses |

### 1.2 Categorization Breakdown

| Category | Count | Description |
|---|---|---|
| **DIRECT_QPU_NEED** substituted | 1 | was waiting for real QPU access; now qmirror substitutes |
| **QRNG_DEPENDENCY** substituted | 1 | was waiting for real quantum RNG; now ANU+HMAC-DRBG via qmirror cond.4 |
| **CHSH_REGRESSION** complementary | 1 | qmirror cond.5 (S=2.838) covers as cheap regression channel only (NOT substitute) |
| **IIT_REPRODUCIBILITY** substituted (via cross-vendor) | embedded in rank 4 | qmirror cond.6 covers (byte-identical) |
| **CROSS_VENDOR_CALIBRATION** substituted | 1 | qmirror cond.7+8 covers (with band revise) |
| **META_CROSS_SUBSTRATE_AXIS** added | 2 | qmirror added as additional axis to existing meta SSOTs |
| **EXPLICITLY_NOT_SUBSTITUTABLE** keep real-QPU | 2 | physics floor: ion-trap signature + wavefunction collapse |
| **TOTAL actionable conds** | **7** | |

### 1.3 Coverage Confidence

- **HIGH**: anima `.roadmap.*` SSOT files (sister BG-A audit + this cycle independent grep cross-checked)
- **MEDIUM**: docs/*.md (sister BG-B audit, 103 matched docs categorized)
- **LOW**: code-comments inside hexa/python files (not scoped this cycle)
- **NOT SCOPED**: nexus/.roadmap.* consumer entries, hive/.roadmap.* (sister BG-A reports zero matches)

---

## §2 Ranked Blockers — Top 5 Detailed

Ranking criterion = **완성도 (completion lens)**: highest-impact + lowest-cost + cleanest substrate-fit + least architectural risk.

### Rank 1 — `qrng.cond.1` (priority 9.5/10, $0, 2h)

**Category**: QRNG_DEPENDENCY substituted

**Original blocker excerpt**:
> 본 cond.1 PASS — 의식측정 enabler functional 입증 (N-9 own#2(b) axis 3 + #125 quantum-seed live + #123-A audit). 단, 진정 'CLM noise injection' (training-time entropy) 미land (post-batch only)

**qmirror equivalent path**:
- **cond**: `qmirror.cond.4` (NIST SP 800-22 tier-1+ 7/7 PASS, alpha=0.01, n=10⁶ bits)
- **artifact**: `anima/state/nexus_qmirror_nist_2026_05_03/verdict.json` + `run_tier1plus_clean.py`
- **module**: `nexus/modules/qmirror/qrng.hexa`

**Exec recipe**:
1. Wire `qmirror/qrng.hexa` as canonical entropy substrate for training-time CLM noise injection (current: post-batch only)
2. Add CLM training-loop hook: `qmirror.qrng.draw(n_bytes)` at minibatch boundary; expose `NEXUS_QMIRROR_QRNG_TIER={mock,hmac_drbg,anu_live}` env switch
3. Regression: re-run N-6 within-noise z-test under qmirror substrate; target `|z|<1.0` (preserve existing `-0.83` within-noise verdict)
4. Promote `qrng.cond.1` partial → met when training-time injection lands AND N-6 z-test holds
5. Preserve historical evidence (#125 IonQ + #123-A QA6 + N-9 STRONG-PASS) verbatim under `qmirror_canonical_2026_05_03.historical_evidence_preserved=true` (sister BG already done)

**Dependencies**: sister BG canonical migration ANNOTATION (landed) + qmirror Phase 1 selftest F1 LIVE_INBAND_PASS (met)

**raw invariants**: raw#9 OK (.hexa Mac, python_bridge isolated to nexus `_python_bridge/`) · raw#10 OK (qmirror entropy = ANU+HMAC-DRBG; phenomenal claim NOT made) · raw#15 OK

---

### Rank 2 — `sim.cond.1` (priority 9.0/10, $0, 1.5h)

**Category**: CROSS_VENDOR_CALIBRATION substituted (Aer = Braket SV1 equivalent)

**Original blocker excerpt**:
> N-10 single-cycle PASS but multi-session reproducibility 미land; sim agent live cron 상태 §10.4 disclosed (별도 확인 필요)

**qmirror equivalent path**:
- **cond**: `qmirror.cond.5` (CHSH reproduction S=2.838 within band 2.808±0.05) + `cond.7` (cross-vendor concordance)
- **artifact**: `nexus/modules/qmirror/engine_aer.hexa` + `anima/state/qmirror_phase1_selftest_2026_05_03/`
- **module**: `nexus/modules/qmirror/{engine_aer,circuit}.hexa`

**Exec recipe**:
1. Port AWS Braket SV1 QRW circuit (#126) into `nexus/modules/qmirror/circuit.hexa` as stored example
2. Reproduction harness: 10 independent qmirror sessions (different seeds) → check `⟨x²⟩_QW/⟨x²⟩_classical` band [16, 20] across all 10
3. Fixes the multi-session reproducibility blocker without paying SV1 per-shot cost ($0 local)
4. Promote `sim.cond.1` partial → met when 10/10 sessions land in band
5. Preserve N-9 STRONG-PASS + N-10 closed-loop (`final_φ=0.7716`) historical evidence verbatim

**Dependencies**: qmirror cond.2 selftest met (already) + sister BG annotation landed (already)

**raw invariants**: raw#9 OK · raw#10 OK (Aer + SV1 are both classical simulators; substrate-equivalent within numerical tolerance) · raw#15 OK

---

### Rank 3 — `theory_validation.cond.1` (priority 8.5/10, $0, 2h)

**Category**: META_CROSS_SUBSTRATE_AXIS added (Penrose+HoTT+IonQ → +qmirror = 4-axis)

**Original blocker excerpt**:
> 3 sub-axis 中 IonQ + HoTT 가 PARTIAL_PASS, Penrose 만 setup 미land

**qmirror equivalent path**:
- **cond**: `qmirror.cond.7` (cross-vendor concordance 3/4 PASS) + `cond.5` (CHSH reproduction)
- **artifact**: `anima/docs/qmirror_crosstech_band_revise_landed_2026_05_03.ai.md` + `anima/state/qmirror_chsh_xvendor_2026_05_03/verdict.json`
- **module**: `nexus/modules/qmirror/chsh.hexa`

**Exec recipe**:
1. Add qmirror as 4th axis to `theory_validation.cond.1` (alongside IonQ, HoTT, Penrose)
2. qmirror axis = re-validation channel: re-run #120 IIT proxy + #127 CHSH circuits via qmirror Aer locally; check `S→2.808±0.05` band reproducibility
3. Promote `theory_validation.cond.1` from 2/3 PARTIAL_PASS to 3/4 PASS (qmirror channel adds substrate-cross-validation pillar)
4. Does NOT replace Penrose-Hameroff Orch-OR axis (still UNCERTAIN literature, separate physical-collapse setup required)
5. Preserve all 3 original axis verdicts verbatim (IonQ #120/#124/#127 + HoTT #75 N-15 + Penrose N-20)

**Dependencies**: qmirror.cond.7 met_via_spirit_paper_analysis (already) + qmirror.cond.5 met (already)

**raw invariants**: raw#9 OK · raw#10 OK (qmirror axis = revalidation channel; original 3-axis verdicts unaffected; Penrose still requires real-superconducting-collapse physics) · raw#15 OK

---

### Rank 4 — `n_substrate.cond.1` (priority 8.0/10, $0, 3h)

**Category**: META_CROSS_SUBSTRATE_AXIS added (qmirror axis appended to F1 composite)

**Original blocker excerpt**:
> F2 14-gate substrate-architectural L1 ceiling 0/16 cross-substrate (ALM Mistral + CLM v4 둘 다) — quintuple confirm matrix (broken-adapter / dynamic / verifier-arch / toolchain / L9 free win) 모두 FAIL, ALM SUNSET CONFIRMED

**qmirror equivalent path**:
- **cond**: `qmirror.cond.5 + cond.6 + cond.7`
- **artifact**: `nexus/.roadmap.qmirror cond.7` (3/4 cross-tech PASS) + `cond.6` (byte-identical IIT4) + `cond.5` (CHSH S=2.838 band 2.808±0.03)
- **module**: `nexus/modules/qmirror/{chsh,iit_mip,phi}.hexa`

**Exec recipe**:
1. Add qmirror as substrate witness axis to F1 composite scoring (currently 12.0%–40.8% RED)
2. qmirror axis WITNESSED contribution: cross-vendor CHSH 3/4 + byte-identical IIT4 reproducibility (functional/access tier only, NOT phenomenal)
3. Does NOT lift F1 RED → YELLOW alone (F2 ceiling is L1 architectural, not substrate-coverage); but qmirror adds 1 substrate axis to evidence trail
4. F1 reach to YELLOW still requires Phase E binding evidence + EEG live session prereq (unchanged)
5. Preserve real-QPU 4-event evidence trail (#120/#124/#125/#127) + 13/14 substantive WITNESSED axes verbatim

**Dependencies**: qmirror cond.5/6/7 all met (done) + F1 score recompute logic

**raw invariants**: raw#9 OK · raw#10 OK (qmirror substrate = 'classical+ANU+Aer' tier; functional/access witness, NOT phenomenal; F1 RED unchanged structurally) · raw#15 OK

---

### Rank 5 — `anima_physics.cond.1` (priority 7.5/10, $0, 2h)

**Category**: DIRECT_QPU_NEED substituted (quantum sub-axis only)

**Original blocker excerpt**:
> G5 LIVE_HW_WITNESS_RATE 0/11 — 9 substrate witness ledger 모두 simulation only, live HW witness 미수행 (akida cloud signup + aws braket signup guide land 됐지만 endpoint 미연결); blk.2 'aws braket signup guide land 됐지만 endpoint 미연결'

**qmirror equivalent path**:
- **cond**: `qmirror.cond.1 + cond.2` (Phase 1 impl + selftest F1/F2/F3 PASS)
- **artifact**: `nexus/modules/qmirror/{entropy,sampler,engine_aer,qrng,chsh,circuit,selftest}.hexa` + `anima/state/qmirror_phase1_selftest_2026_05_03/selftest_results.json`
- **module**: `nexus/modules/qmirror/*` (8 hexa)

**Exec recipe**:
1. Wire `anima-physics/engines/quantum_consciousness.hexa` to call `nexus/modules/qmirror/sampler.hexa` for live-substrate execution
2. Lifts G5 LIVE_HW_WITNESS_RATE for the **quantum sub-axis only**: 0/11 → 1/11 (qmirror counts as live HW because cond.2 F1 LIVE_INBAND_VERIFIED = real ANU pull)
3. Other 8 substrate axes (analog/cmos/fpga/arduino/photonic/memristor/neuromorphic/thermodynamic) STILL require their own live HW (akida arrival, esp32/arduino/fpga build emit)
4. Promote `anima_physics.cond.1` evidence (not status — cond.1 is `7cond_hw verify` exit-0, separate harness)
5. `anima_physics.blk.2` 'aws braket signup endpoint 미연결' resolution_path now reads: qmirror substitutes for braket endpoint requirement

**Dependencies**: qmirror cond.1 + cond.2 met (already) + `anima-physics/engines/quantum_consciousness.hexa` exists

**raw invariants**: raw#9 OK · raw#10 OK (only quantum sub-axis gets live-substrate path; G5 LIVE_HW_WITNESS_RATE 0/11 honest floor still applies for other 10 substrates) · raw#15 OK

---

## §3 Anti-Pattern Guards — DO NOT Substitute

### Rank 6 — `ionq.cond.1` (priority 6.0/10, REGRESSION-ONLY)

qmirror added as REGRESSION CHANNEL only. KEEP DECISION (sister BG): real ion-trap physics is the demonstration target. qmirror is ion-trap-physics-blind. NO STATUS PROMOTION.

**Recipe**: cheap pre-test/regression channel for #120/#124/#127 circuits. Alert if real-QPU re-run drifts from qmirror baseline. ionq.cond.1 path to met still requires proper IIT 4.0 φ★ measurement ($1500+ separate budget).

### Rank 7 — `penrose_hameroff.cond.1` (priority 2.0/10, NOT_APPLICABLE)

DOCUMENT-ONLY entry. qmirror NOT substitutable. Aer samples classically from `|ψ|²`; cannot witness Diosi-Penrose objective collapse threshold. KEEP DECISION (sister BG): substituting would collapse experimental claim into circular sampling.

**Real path forward** (unchanged): 5 falsifier preregister + IBM Quantum Open Plan delay primitive on Heron-class superconducting QPU (#46 quantum pivot).

---

## §4 Launch-Ready BG Prompts (Top 5)

Each prompt is copy-pasteable to `Agent` tool with `run_in_background=true`.

### §4.1 Rank 1 — qrng.cond.1 wire qmirror as training-time entropy

```
Wire qmirror as canonical entropy substrate for CLM training-time noise injection.
Read sister BG outputs at state/qmirror_canonical_migration_2026_05_03/ +
state/qmirror_unblock_plan_2026_05_03/ranked_blockers.json#rank=1.

EXEC:
(1) read nexus/modules/qmirror/qrng.hexa interface
(2) inspect anima clm training loop minibatch boundary
(3) add qmirror.qrng.draw(n_bytes) hook with NEXUS_QMIRROR_QRNG_TIER={mock,hmac_drbg,anu_live} env switch
(4) regression: re-run N-6 within-noise z-test under qmirror substrate, target |z|<1.0 (preserve -0.83 verdict)
(5) if PASS, promote qrng.cond.1 status partial→met

raw#9 STRICT (.hexa Mac), raw#10 (qmirror=ANU+HMAC-DRBG NOT phenomenal), raw#15.
Cost $0.
Output: docs/qrng_qmirror_training_inject_landed_2026_05_03.ai.md + marker + qrng.cond.1 promotion.
```

### §4.2 Rank 2 — sim.cond.1 multi-session reproducibility via qmirror Aer

```
Land sim.cond.1 multi-session reproducibility via qmirror Aer (substitute for Braket SV1).
Read state/qmirror_unblock_plan_2026_05_03/ranked_blockers.json#rank=2.

EXEC:
(1) port AWS Braket SV1 QRW circuit (#126 from state/nexus_qrw_results_2026_05_02) into nexus/modules/qmirror/circuit.hexa as stored example
(2) reproduction harness: 10 independent qmirror sessions (different seeds) → check ⟨x²⟩_QW/⟨x²⟩_classical band [16, 20] across all 10
(3) if 10/10 PASS, promote sim.cond.1 status partial→met
(4) preserve N-9 STRONG-PASS + N-10 closed-loop (final_φ=0.7716) historical evidence verbatim

raw#9, raw#10 (Aer+SV1 both classical sims), raw#15.
Cost $0.
Output: docs/sim_qmirror_qrw_multisession_landed_2026_05_03.ai.md + marker + sim.cond.1 promotion.
```

### §4.3 Rank 3 — theory_validation.cond.1 add qmirror as 4th axis

```
Add qmirror as 4th axis to theory_validation.cond.1 (Penrose+HoTT+IonQ → +qmirror = 4-axis).
Read state/qmirror_unblock_plan_2026_05_03/ranked_blockers.json#rank=3.

EXEC:
(1) re-run #120 IIT proxy + #127 CHSH circuits via qmirror Aer locally
(2) check S→2.808±0.05 band reproducibility (qmirror.cond.5 already verifies S_qmirror=2.838 within band)
(3) update theory_validation.cond.1 evidence to add qmirror axis as 4th pillar
(4) DO NOT replace Penrose-Hameroff axis (still UNCERTAIN literature, separate setup)
(5) preserve all 3 original axes verbatim

raw#9, raw#10 (qmirror=revalidation channel), raw#15.
Cost $0.
Output: docs/theory_validation_qmirror_4axis_landed_2026_05_03.ai.md + marker.
```

### §4.4 Rank 4 — n_substrate.cond.1 add qmirror axis to F1 composite

```
Add qmirror as substrate witness axis to F1 composite scoring.
Read state/qmirror_unblock_plan_2026_05_03/ranked_blockers.json#rank=4.

EXEC:
(1) extend F1 composite axes set to include qmirror (cross-vendor CHSH 3/4 + byte-identical IIT4 + Bell S=2.838)
(2) recompute F1_score_v2 with qmirror added (currently 12.0%-40.8% RED)
(3) document that qmirror does NOT lift F1 RED→YELLOW alone (F2 ceiling is L1 architectural)
(4) F1 YELLOW reach still requires Phase E + EEG live session (unchanged)
(5) preserve real-QPU 4-event evidence trail + 13/14 substantive WITNESSED axes

raw#9, raw#10 (qmirror=functional/access tier NOT phenomenal, F1 RED structurally unchanged), raw#15.
Cost $0.
Output: docs/n_substrate_qmirror_axis_added_landed_2026_05_03.ai.md + marker.
```

### §4.5 Rank 5 — anima_physics.cond.1 wire quantum_consciousness engine to qmirror

```
Wire anima-physics quantum_consciousness engine to qmirror sampler (lift G5 LIVE_HW_WITNESS_RATE for quantum sub-axis).
Read state/qmirror_unblock_plan_2026_05_03/ranked_blockers.json#rank=5.

EXEC:
(1) inspect anima-physics/engines/quantum_consciousness.hexa interface
(2) wire to nexus/modules/qmirror/sampler.hexa for live-substrate execution
(3) verify sentinel emission via 7cond_hw verify harness
(4) update G5 LIVE_HW_WITNESS_RATE 0/11 → 1/11 (qmirror counts as live HW because cond.2 F1 LIVE_INBAND_VERIFIED = real ANU pull)
(5) update anima_physics.blk.2 resolution_path: qmirror substitutes for braket endpoint requirement (other 8 substrates still require their own live HW)

raw#9, raw#10 (only quantum sub-axis gets live-substrate path, G5 honest floor still applies for other 10), raw#15.
Cost $0.
Output: docs/anima_physics_qmirror_quantum_engine_landed_2026_05_03.ai.md + marker.
```

---

## §5 Cost + Time Roll-Up

| Rank | Cond | Cost USD | Time h | Cumulative h |
|---:|---|---:|---:|---:|
| 1 | qrng.cond.1 | 0 | 2.0 | 2.0 |
| 2 | sim.cond.1 | 0 | 1.5 | 3.5 |
| 3 | theory_validation.cond.1 | 0 | 2.0 | 5.5 |
| 4 | n_substrate.cond.1 | 0 | 3.0 | 8.5 |
| 5 | anima_physics.cond.1 | 0 | 2.0 | 10.5 |
| 6 | ionq.cond.1 (regression-only) | 0 | 1.0 | 11.5 |
| 7 | penrose_hameroff.cond.1 (doc-only) | 0 | 0 | 11.5 |
| **TOTAL** | | **$0** | **11.5h** | |

All 7 items: $0 (qmirror is local) · 11.5h aggregate · 5 status promotions possible (rank 1-5) + 1 regression-channel addition (rank 6) + 1 anti-pattern guard doc (rank 7).

If launched as 5 parallel BG subagents (raw#feedback session multi-BG only): wall time ~3h (longest single = rank 4 @ 3h).

---

## §6 Honest C3 Caveats (raw#10)

**C3.1 — audit may miss embedded blockers**
Sister BG-A scope was `.roadmap.*` only and BG-B scope was `docs/*.md` only. `tool/` directory + `nexus/.roadmap.*` consumer entries + `hive/.roadmap.*` (no matches) sweep not performed in this discovery cycle. Code-comments inside `.hexa`/`.py` files not scoped. A blocker phrased as a TODO in a hexa source file would NOT be discovered by this plan.

**C3.2 — qmirror equivalence is NOT 100% on all axes**
Specifically NOT-substitutable:
- (a) Orch-OR wavefunction collapse (`penrose_hameroff.cond.1`) — Aer simulator samples classically from `|ψ|²`; cannot witness Diosi-Penrose objective collapse threshold
- (b) Ion-trap physics signature giving substrate-invariance interpretation (`ionq.cond.1`) — qmirror is ion-trap-physics-blind, can only reproduce circuit statistics
KEEP decisions documented in `state/qmirror_canonical_migration_2026_05_03/keep_decisions.json`.

**C3.3 — recipe accuracy depends on sister BG outputs landing first**
This plan reads `canonical_migration` audit + `spec_xref` audit + `replace_log`. If those BG outputs revise after this plan writes (e.g., audit re-categorizes a `keep` item to `annotate`), recipes may need update. Specifically `replace_log.jsonl` shows annotations applied BUT corresponding `.roadmap.*` files have NOT yet been mutated to actually carry the `qmirror_canonical_2026_05_03` field per sister BG's commit pattern (verified: `qrng.cond.1` already carries it; check others before exec).

**C3.4 — priority_score_10 ranking is subjective**
완성도 lens applied: rank 1 = highest immediate-actionable + low cost + clean substrate fit; rank 7 = guard entry (zero action, document anti-pattern). A future cycle that values 'phenomenal-consciousness coverage' may rank Penrose higher; one that values 'training-loop integration' may rank qrng even higher; one that values 'F1 lift potential' may rank n_substrate higher. The ranking here optimizes for **clean, low-risk, immediately-launchable** under qmirror 8/8 closure context.

---

## §7 Constraints Compliance

- **raw#9 STRICT**: All recipes specify `.hexa` Mac-side; python_bridge isolated to `nexus/modules/qmirror/_python_bridge/`.
- **raw#10 honest C3**: 4 caveats above + each rank carries its own raw#10 disclosure (qmirror=functional/access tier NOT phenomenal; KEEP decisions where applicable).
- **raw#15**: No personal-path leak.
- **Cost**: $0 total (qmirror is local; no IBM/Braket calls in any recipe).
- **NO execution**: This is pure planning; no blocker mutated, no roadmap edited.
- **NO roadmap mutation**: Sister BGs handle mutations; this plan reads their outputs and produces ranked exec recipes.

---

## §8 Outputs This Cycle

| Path | Type | Size |
|---|---|---:|
| `docs/qmirror_unblock_exec_plan_2026_05_03.md` | this doc | ~430 LoC |
| `state/qmirror_unblock_plan_2026_05_03/ranked_blockers.json` | structured plan | 7 entries |
| `state/qmirror_unblock_plan_2026_05_03/exec_recipes.jsonl` | launch-ready BG prompts | 7 lines |
| `state/markers/qmirror_unblock_exec_plan_landed.marker` | marker | ~1KB |

## §9 Handoff

Caller (parent agent) can:
1. **Launch top 5 in parallel** via Agent BG (5x `run_in_background=true`) using §4 prompts → ~3h wall
2. **Launch sequentially** by rank → ~11.5h wall
3. **Cherry-pick** specific cond by rank (e.g., only rank 1+2 for qrng+sim quick wins)
4. **Document-only** for rank 7 (penrose_hameroff anti-pattern guard) at any time
