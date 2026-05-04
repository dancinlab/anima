# nexus.qmirror 2.0 — Closure Synthesis (composed 2026-05-04T04:47:11Z)

**Date:** 2026-05-04T04:47:11Z
**Spec:** docs/qmirror_2_closure_spec_2026_05_04.md
**Composite verdict:** `qmirror_2_closure_FULL`
**n_pass:** 5 of 5
**F-QM-2-CLOSURE-1:** PASS
**qmirror version target:** 2.0.0

---

## 0. Executive summary

qmirror 2.0 closure: 5/5 conds met.
Per spec §1.3 → `qmirror_2_closure_FULL`.

| cond    | falsifier        | verdict | sha256 |
|---------|------------------|---------|--------|
| cond.9  | F-QM-2-TOMO-9    | PASS    | `1de6219bb131e104f8affdc513ac8a0bff449806a7d19c390355f8d5c98ba45c` |
| cond.10 | F-QM-2-GHZ-10    | PASS    | `931d6d81d2465f76b3bafc63475af22aed9fad3a03abf4d07d1f595eeb9aa5bb` |
| cond.11 | F-QM-2-STAB-11   | PASS    | `eaf6cc1bc6e2fbcc49071c4a4b9b8442b6cbdfa37e251b3c27de516e51f96513` |
| cond.12 | F-QM-2-SURF-12   | PASS    | `41d7481edd6000c4dd4ad144242a9a509a02443b682d7da23d55f7e09e6be927` |
| cond.13 | F-QM-2-CSCS-13   | PASS    | `0d252e8cd3701ec4dde370e6e266763aa313864023a2e7ab46dd9ad344afd696` |

---

## 1. Per-cond evidence ledger

(see state/qmirror_2_closure_2026_05_04/dispatch_audit.json for full sha256 + raw#10 caveat copies)

- **cond.9** (process tomography, F-QM-2-TOMO-9): 7/7 gates PASS, fidelity_min ≈ 0.99918
- **cond.10** (GHZ-3 + Mermin witness, F-QM-2-GHZ-10): M = 4.0 analytic exact over 30 trials, M_min ≥ 3.5
- **cond.11** (stabilizer measurement primitive, F-QM-2-STAB-11): syndrome_plus_ratio ≥ 0.99 ∧ post_fidelity ≥ 0.99 over 1024 trials
- **cond.12** (surface code d=3 toy, F-QM-2-SURF-12): logical_zero_ratio ≥ 0.99 ∧ min_stab_plus_ratio ≥ 0.99 over 1024 noiseless Aer measurements
- **cond.13** (CSCS chained CHSH, F-QM-2-CSCS-13): min(S_per_pair_mean) ≥ 2.7, W_mean ≥ 2.7, indep_pvalue_mean ≥ 0.05 across pairs × 30 trials

## 2. Closure verdict matrix

n_pass = 5 → composite = `qmirror_2_closure_FULL`

## 3. Cross-axis interactions

- cond.9 + cond.11 → full QEC primitive set
- cond.11 → cond.12 (hard dep)
- cond.10 + cond.13 → multi-particle entanglement cross-witness

## 4. Cumulative cost

$0 default path; up to $25 if cond.13 hardware anchor engaged

## 5. Honest C3 — 6 closure-level caveats (raw#10)

1. 5-axes selection bias toward Aer-friendly conds
2. Noiseless-Aer threshold inheritance
3. cond.12 toy NOT fault tolerance
4. python_bridge debt grows by 5 files (3 → 8)
5. Optional $25 anchor selection bias risk (cond.13 hardware leg)
6. Composite-level: vendor-side or sister-BG post-hoc edit invalidation; sha256 in dispatch_audit.json mitigates

## 6. Roadmap mutation block (paste-target for .roadmap.qmirror)

```jsonc
"closure_2026_05_04": {
  "verdict": "qmirror_2_closure_FULL",
  "n_pass": 5,
  "closure_doc": "docs/qmirror_2_closure_2026_05_04.md"
}
```

## 7. qmirror 3.0 roadmap (pending closure verdict)

5 candidate axes: magic-state distillation, FFI retirement, IIT scale-up, RCS reframing, VQC consumer

## 8. References

- Spec: docs/qmirror_2_closure_spec_2026_05_04.md
- 1.0 closure: docs/nexus_qmirror_closure_2026_05_03.md
- Dispatch audit: state/qmirror_2_closure_2026_05_04/dispatch_audit.json
- Watchdog verdict: state/qmirror_2_closure_2026_05_04/verdict.json
- GitHub release: https://github.com/need-singularity/qmirror/releases/tag/v2.0.0

## 9. Closure verdict (final line)

**`qmirror 2.0 closure_qmirror_2_closure_FULL = met at 2026-05-04T04:47:11Z; 5/5 conds met; F-QM-2-CLOSURE-1 = PASS; qmirror version 2.0.0; raw#9 STRICT honored on Mac repo.`**
