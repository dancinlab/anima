# nexus.qmirror N2 Cross-Vendor Axis — Scope Revision (Eagle/Falcon Retirement)

- ts_utc: 2026-05-03
- module: **nexus.qmirror** (Phase 3 calibration burst — N2 axis only)
- author preset: friendly (raw#272)
- gate: doc-only; no execution committed
- raw#9: NO .py on Mac repo
- supersedes (partial): `docs/ibm_cloud_experiment_list_2026_05_03.md` §2 N2 line + R3 revision row
- triggers: roadmap update — `nexus/.roadmap.qmirror` cond.7 invalidated → cond.7' / cond.8 reissue
- contributes_to: cond.3 (N2 sub-axis only) + cond.7' (revised cross-vendor anchor)

---

## 1. Invalidation summary — Eagle / Falcon retired

### Empirical finding (subagent a30f6c3fb3917ee5c, 2026-05-03)

IBM Cloud catalog audit on 2026-05-03 (paygo plan, us-east region):

| family | backends listed | status | evidence |
|---|---|---|---|
| **Heron r2** | 3 (`ibm_fez`, `ibm_marrakesh`, `ibm_kingston`) | operational | open + paygo plan |
| **Heron r3** | 2 (`ibm_boston`, `ibm_pittsburgh`) | operational | paygo plan only |
| **Eagle (r1/r3)** | **0** | **retired late 2025** | not in any plan |
| **Falcon (r4/r5)** | **0** | **retired** | not in any plan |

Bell test verified on `ibm_boston` (Heron r3): correlation 0.98, actual cost $1.60 — paygo is functional.

### What this invalidates

| spec/doc | line | invalidation |
|---|---|---|
| `docs/ibm_cloud_experiment_list_2026_05_03.md` R3 | "real Heron + Eagle + Falcon cross-vendor (original spec N2 axis fully realized)" | **false** — only Heron family exists |
| `docs/ibm_cloud_experiment_list_2026_05_03.md` §2 N2 row | "Heron + Eagle + Falcon — Bell × 5 each" | **infeasible** — only Heron available |
| `docs/nexus_qmirror_phase3_calibration_runbook_2026_05_03.md` §2 day 2 | "CHSH × 5 trial × 3 backend × 4096 shot" | **infeasible** — 3-vendor not selectable |
| `nexus/.roadmap.qmirror` cond.7 | "Heron + Eagle + Falcon all 3 vendors yield matching qmirror noise model" | **unmeetable as written** |
| Phase 3 runbook §6 schema | `vendor_family: "heron|eagle|falcon"` enum | shrinks to `heron` only (intra-family) |

The pre-existing C3 caveat (`ibm_cloud_env_setup_runbook` §C3.5 "Falcon device retirement risk") was correct in spirit but underestimated severity — Falcon **and** Eagle are both fully gone, not just at-risk.

---

## 2. Three revision options (α / β / γ)

### Option α — intra-family Heron r2 vs r3

Re-scope N2 from "3-vendor cross-family" → "1-vendor 2-revision intra-family".

| field | value |
|---|---|
| backends | 3× Heron r2 (`ibm_fez`, `ibm_marrakesh`, `ibm_kingston`) + 2× Heron r3 (`ibm_boston`, `ibm_pittsburgh`) |
| circuit | CHSH Bell, 4 settings |
| trials | 5 trial × 5 backend = 25 trial |
| shots | 4096 / trial |
| metric | S-statistic dispersion within family + r2-vs-r3 KS test |
| budget | $40 (unchanged from R3) |
| diversity score | **2/10** (same fab, same gate set, same control electronics generation) |
| pro | uses already-paid IBM credit; no new vendor signup; matches N1 noise-model substrate |
| con | weak proxy for vendor diversity; per Test 3 subagent: "tightly correlated noise profiles" |

### Option β — IBM Heron + Braket vendor mix

Split N2 into N2a (intra-IBM Heron) + N2b (cross-provider via AWS Braket).

| field | N2a (IBM) | N2b (Braket) |
|---|---|---|
| backends | 3× Heron r2 OR 2× Heron r3 (pick 3 backends) | IonQ Forte 1 (trapped-ion) + Rigetti Ankaa-3 (superconducting transmon, different fab) |
| circuit | CHSH Bell | CHSH Bell (re-use `state/nexus_chsh_bell_2026_05_02/` circuit JSONs as ground truth) |
| trials | 3 trial × 3 backend = 9 trial | 3 trial × 2 backend = 6 trial |
| shots | 4096 | 250 (Braket cost-conservative) |
| budget | $20 (half of $40) | $60 (IonQ ~$20.30/run × 3 + Rigetti ~$0.65/run × 3 ≈ $63 → cap $60 with shot cut) |
| metric | intra-Heron S band + cross-provider S band overlap |  |
| diversity score | **8/10** (truly different fab + qubit modality + control system + vendor org) |
| pro | meets the *spirit* of original N2 (vendor-independent qmirror anchor); reuses verified Braket Bell circuits |
| con | budget pressure (+$40 vs §2 N2 plan); needs Braket account + IAM; IonQ queue can be 24-48 hr |

### Option γ — Heron-only deep + add new axis

Accept that real cross-vendor is infeasible inside IBM Cloud; redirect $40 N2 budget to deepen existing axes.

| field | value |
|---|---|
| backends | Heron r2 (`ibm_fez`) + Heron r3 (`ibm_boston`) only |
| circuit | CHSH Bell × 3 trials × 2 backend = 6 trial (Heron r2 vs r3 sanity only, $10) |
| extra spend | **$30 reallocated** to new N6 axis: dynamic decoupling (DD) sequence calibration on Heron r3 — characterises `ibm_boston` non-Markovian noise that current N1 RB misses |
| diversity score | **1/10** (intra-vendor only) |
| pro | maximises *depth* of Heron noise model where qmirror will primarily land; honest about vendor-mono reality |
| con | cond.7 cross-vendor goal abandoned outright (must be re-named cond.7' "Heron-family anchor"); no real-vendor diversity signal |

### Optional escape hatches considered + dropped

| candidate | drop reason |
|---|---|
| Quantinuum H1/H2 trapped-ion via Azure Quantum | $2,000+/hr — destroys $500 envelope |
| Pasqal neutral-atom (Braket) | analog Hamiltonian device, no gate-model CHSH; not comparable |
| IQM 5-qubit (research access) | private partnership only, no public paygo |
| Atom Computing | research access only, no public API |
| IBM "premium" Eagle revival | Eagle is fully retired; no reactivation pathway exists |
| AWS Braket OQC Lucy | superconducting same-modality as Rigetti; redundant under option β |

---

## 3. Cost / wall / diversity comparison matrix

| dim | option α (intra-Heron) | option β (IBM+Braket) | option γ (Heron-deep) |
|---|---|---|---|
| **N2 budget** | $40 | $20 (IBM) + $60 (Braket) = $80 | $10 (N2 sanity) + $30 (N6 DD) = $40 |
| **delta vs R3 plan** | $0 | **+$40** | $0 |
| **wall time** | 1 day (day 2) | 2-3 days (Braket queue 24-48 hr) | 1 day (day 2) |
| **vendor diversity score (0-10)** | 2 | **8** | 1 |
| **honest cross-vendor claim** | none — same fab | yes — different qubit modality + fab + vendor | none — explicitly Heron-only |
| **qmirror noise-model coverage** | r2 + r3 control-pulse delta | Heron + transmon (Rigetti) + trapped-ion (IonQ) | Heron r2 + r3 + DD-corrected non-Markovian |
| **fits $500 IBM envelope** | yes ($500 unchanged) | **no — overflows by $40** unless reallocated from buffer + N4 | yes ($500 unchanged) |
| **roadmap cond.7 satisfiability** | partial — must rename to cond.7' "intra-family" | **full** — meets original "vendor-bias eliminated" intent | abandoned — cond.7 retired |
| **doc/runbook churn** | low (rename strings) | **high** (new Braket sub-runbook + IAM + cost guard) | medium (axis swap N2→N6) |
| **risk of zero data day 2** | low | medium (Braket queue) | low |
| **추가 substrate value** | low | **high** (real cross-modality witness) | medium (DD captures non-Markovian) |

---

## 4. Recommendation — 완성도 ranking (raw#272 friendly preset)

**Recommended primary**: **Option β (IBM Heron + Braket vendor mix)**.

Ranking with brief 완성도 justification (high → low):

1. **β (recommended)** — only option that *honestly* delivers what cond.7 asks for ("vendor-bias eliminated"). The +$40 delta is absorbable by reducing N4 random-circuit fidelity from 50→30 trials per depth (saves $8) and tapping the $10 buffer + $20 from N5 by dropping 20-qubit GHZ to 16-qubit ceiling (saves $20). Net allocation stays inside $500. Trade is N5 ceiling 20→16 qubit → qmirror anchored at conservative scale, which is honest given simulator memory wall is ~30 qubit anyway.

2. **α (fallback)** — chosen if Braket account/IAM not available within day 0 timebox or user preference is "single-cloud only". Honest 완성도 cost: must rename cond.7 → cond.7' and explicitly disclaim cross-vendor claim. Still useful: r2-vs-r3 KS gives a real (if narrow) noise-distribution-stability signal.

3. **γ (last resort)** — chosen only if Braket signup fails AND user rejects α as "too weak to call cross-vendor". Trade is depth-over-breadth: DD calibration improves N1 noise model fidelity beyond Pauli-error approximation. Lowest 완성도 on cross-vendor axis but highest on Heron noise modelling.

Ranking principle: "real signal that matches the spec's stated goal" > "cheap signal that fits unchanged budget" > "different signal that pivots the goal".

---

## 5. Budget impact ($500 IBM + Braket envelope)

### If option β chosen

| axis | R3 plan | β-revised | delta |
|---|---|---|---|
| N1 noise model RB | $60 | $60 | $0 |
| N2a IBM intra-Heron | $40 | $20 | -$20 |
| **N2b Braket cross-provider** | — | **$60** | **+$60** |
| N3 process tomography | $40 | $40 | $0 |
| N4 random fidelity (50→30 trials) | $20 | $12 | -$8 |
| N5 scale-up (20→16 qubit ceiling) | $30 | $10 | -$20 |
| N6 (γ-borrowed DD sequence) | — | — | $0 |
| buffer | $10 | $8 | -$2 |
| **IBM total** | $200 | **$150** | **-$50** |
| **Braket total** | $0 | **$60** | **+$60** |
| **combined** | $200 | **$210** | +$10 (within $500 envelope; **$290 unallocated** for re-burst or drift refresh) |

R3 already declared $500 envelope but only allocated $200 explicitly — the remaining $300 was implicit headroom. Option β uses $10 of that headroom; $290 still in reserve.

### If option α chosen

No budget change vs R3 — entire $40 stays inside IBM N2 line, simply distributed across 5 Heron backends instead of 3 vendor families.

### If option γ chosen

No budget change; $30 moves N2 → N6 (new axis).

---

## 6. Honest C3 (raw#91, ≥5 caveats)

1. **Eagle/Falcon retirement is permanent** — IBM has stated public direction is Heron-and-successors only. No future revision will revive option-original-R3 spec; cond.7 must be permanently rewritten regardless of which option is chosen.

2. **Option β cross-vendor delta confounded by shot count** — IBM N2a uses 4096 shots/trial, Braket N2b uses 250 shots/trial (cost-driven). KS test between the two distributions is partly measuring shot-noise asymmetry, not just hardware diversity. Mitigation: compare *bound saturation ratio* (S/2.828) rather than raw S-statistic, which is shot-count-robust.

3. **IonQ queue variance** — Forte 1 historical queue 12-48 hr; option β day 2-3 may slip to day 3-4. Phase 3 runbook §2 timeline must allow ≥48 hr Braket window or de-couple Braket runs to background while continuing IBM axes.

4. **Braket IAM + billing add operational surface** — option β requires AWS account active + Braket service enabled + IAM role for IonQ + Rigetti device-arn permissions + cost-explorer alerting. ~2 hr additional day-0 setup. Not in current Phase 3 runbook §0 prereqs.

5. **r2-vs-r3 (option α/β/γ all use this) is weak diversity** — both share IBM Qiskit runtime, same control-pulse compiler, same readout discrimination. KS p-values will be high (no rejection of "same distribution") even though hardware is genuinely different — because the *noise* is genuinely correlated. This is a real-world property, not a measurement artefact.

6. **N5 scale-up sacrifice (option β)** — reducing GHZ ceiling 20→16 qubit means qmirror's "N ≤ 20 measured anchor" claim from R3 §4 outcome table degrades to "N ≤ 16 measured anchor". Below the simulator memory ceiling (~30 qubit) so still meaningful, but documentation must update.

7. **Rigetti Ankaa-3 availability check pending** — option β assumes Ankaa-3 is on Braket and available in us-east-1; not verified in this revision doc. Day 0 Braket setup must verify or substitute (next-best superconducting non-IBM: OQC Lucy, but same modality concern).

8. **No execution committed** — this revision is doc-only. Burst execution (any option) requires fresh user OK after option selection.

---

## 7. Decision matrix

| user signal | action |
|---|---|
| "go β (recommended)" | update Phase 3 runbook §2 day 2 → split N2a IBM + N2b Braket; add Braket day-0 prereqs; reduce N5 ceiling 20→16 |
| "go α (single-cloud)" | update Phase 3 runbook §2 day 2 → 5 Heron backends; rename roadmap cond.7 → cond.7' "intra-family"; no budget change |
| "go γ (Heron-deep)" | update runbook §2 → swap N2 for N6 DD sequence; retire roadmap cond.7 |
| "wait, I want to investigate Quantinuum / others" | doc as-is, no action; flag escape-hatch table §2 for re-discussion |
| "도 다른 옵션 brainstorm" | escalate; this revision lists what was ruled out; new candidates need fresh Cloud-catalog audit |

---

## 8. References

- subagent a30f6c3fb3917ee5c (2026-05-03 paygo Test 3 finding) — IBM Cloud catalog audit
- `docs/ibm_cloud_experiment_list_2026_05_03.md` — R3 plan being revised
- `docs/nexus_qmirror_spec_2026_05_03.md` — module spec (3-tier substrate)
- `docs/nexus_qmirror_phase3_calibration_runbook_2026_05_03.md` — operational runbook to update
- `docs/ibm_cloud_env_setup_runbook_2026_05_03.md` — pre-existing Falcon-retirement caveat
- `nexus/.roadmap.qmirror` — domain SSOT, cond.7 to be invalidated
- `state/nexus_chsh_bell_2026_05_02/` — Braket IonQ Forte 1 reference (S=2.808, $81.20 actual; cost_preflight $0.30/task + $0.08/shot)
- IBM Quantum backends catalog: 2026-05-03 audit (Heron r2 + r3 only; Eagle/Falcon retired)
- AWS Braket device list: us-east-1 (IonQ Forte 1, Rigetti Ankaa-3, OQC Lucy — verification pending day 0)

---

## 9. Cross-link block (for downstream cite)

- planner R3 → R4 update target: `docs/ibm_cloud_experiment_list_2026_05_03.md` (companion update, this cycle)
- runbook update target: `docs/nexus_qmirror_phase3_calibration_runbook_2026_05_03.md` (companion update, post-option-selection)
- roadmap update target: `nexus/.roadmap.qmirror` (companion update, this cycle — cond.7 → cond.7' or cond.8 + new blocker)
