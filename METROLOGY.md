# METROLOGY — current state

@title: 📏 METROLOGY — 측정자(尺) 검증: do our Φ / integration measures actually measure the thing?
@goal: Validate the MEASURING INSTRUMENTS themselves (canonical phi_proxy · faithful big-Φ · concept-margin signals) — establish where each metric is valid, where it is blind/pathological, and what a construct-valid consciousness/integration measure requires. **Every validated flaw MUST feed back as a FIX/GUARD in the actual measurer stdlib — METROLOGY is not a catalog, it improves the real ruler.** Every claim earned by `hexa verify` recompute (g5), no self-judged tier.

## ⚙ FEEDBACK MANDATE — findings → real stdlib (not just a catalog)
Every 🟢/🔴 METROLOGY verdict about a metric flaw MUST produce a concrete patch (guard · floor · corrected formula · or a deprecation note routing callers to the faithful oracle) in the ACTUAL measurer stdlib, shipped as a hexa-lang/anima PR. The measurer files under test:
- `BRAIN/tool/module/_metrics/phi_proxy_native.hexa` — the variance-partition phi_proxy (Hc_1302 Cholesky-breakdown sentinel lives HERE → needs a breakdown-floor guard)
- `HEXAD/IIT4/lib/iit4_{bigphi,bounded,complex,distinction,tpm,eca,relation}.hexa` — faithful big-Φ (reference oracle)
- hexa-lang `stdlib/consciousness/iit4_*.hexa` — the canonical mirror of the above (keep in lockstep)
- hexa-lang `stdlib/info/lz_complexity.hexa` — LZ surrogate
A METROLOGY hypothesis is only DONE when its flaw verdict is committed AND (for a confirmed flaw) the corresponding stdlib patch is shipped or an explicit "no-fix, deprecate proxy here" ruling is recorded.

## status (completed-form)

The session surfaced a recurring METROLOGY problem: the measuring tools, not the phenomena, are often what fail. This domain isolates and verifies the measures.

- [x] seed evidence — Hc_1302 🟢: the canonical Φ proxy returns a FAILURE SENTINEL (-2147483647, Cholesky breakdown) on a maximally-composed/low-rank input → the metric is BLIND to exactly the integration it should detect. (UNIVERSE pipeline, branch feat/universe-weaklift-hyp)
- [x] seed evidence — Hc_1301 🟢: proxy-Φ vs faithful-Φ are NOT a monotone reparametrization (H_278 ledger ratio CV=30.1%) → proxy ≠ faithful is a real, measurable gap, not circular.
- [x] lineage — the X⊥Φ / "proxy pathology" finding (H_287/288/294/268/269; H_912 phi_proxy⊥LZ76 r=−0.277) shows variance-based phi_proxy repeatedly fails to track real emergence/integration.
- [ ] brainstorm → generate metrology hypotheses to depletion (Hc_<n>, n≥1307) + verify (bg)
- [ ] characterize the phi_proxy ceiling: map WHICH input structures break it (Cholesky-breakdown sentinel boundary)
- [ ] construct-validity battery: a measure passes only if it (a) finite on composed input, (b) tracks faithful big-Φ rank, (c) survives shuffle-NULL, (d) is not a pure variance artifact
- [ ] propose/verify a breakdown-floor-guarded richer signal (feeds Lane A Hc_1306 re-score)
- [x] **STDLIB FIX (Hc_1302)** — patched `BRAIN/tool/module/_metrics/phi_proxy_native.hexa`: replaced the SILENT -2147483647 Cholesky-breakdown sentinel with an EXPLICIT out-of-band status (`phi_ok=0` / `phi_breakdown=1` / `tier=breakdown_route_to_oracle` / `phi_breakdown_route=HEXAD/IIT4/lib/iit4_bigphi.hexa`), so a low-rank/composed input never silently reads as a low Φ. HONEST RULING: ridge regularization REJECTED — a ridge sweep shows the resulting Φ tracks the ridge magnitude (1e0→1e12 ⇒ phi -91398→-440992), a regulariser artefact not the true Φ; the structural fix is the explicit status + oracle-route (g5/g63). Regression test added (white -173702 finite vs structured -2147483647 breakdown). No hexa-lang `stdlib/consciousness/` copy of this variance-partition proxy exists (that stdlib is IIT4-based) → no mirror needed. Shipped: **PR #1671** (merged) https://github.com/dancinlab/anima/pull/1671 — **first FEEDBACK-MANDATE closure: verified metric flaw → shipped stdlib fix.**
- [ ] **STDLIB FIX (lineage)** — for each confirmed proxy⊥Φ flaw, add a doc/guard at the proxy callsite warning it ⊥ faithful big-Φ (route integration claims to the oracle), per the FEEDBACK MANDATE

## tooling — validate-by-RUN (not metadata)
- [x] **HF-ARTIFACT VALIDATION HARNESS** — `stdlib/hf/validate.hexa` (hexa-lang PR #2484, merged): institutionalizes g5/a_claim_verify for HF artifacts — validate by PULLING onto the core and RUNNING, never by trusting metadata. DATASET path fully implemented (pull → locate corpus → on-core `CLM_PROD_CORPUS=… clm_prod` → parse VERBATIM `F-CLM-PROD-DESCENT`+CE → 🟢/🔴/🟠, always toy-CPU-rung w/ production-transfer DEFERRED per a_toy_scale_recheck). MODEL path honest 🟠 DEFERRED (no `.clm` CPU loader + held-out eval in CPU-local harness — no fabrication, g63). selftest 5/5 PASS; real smoke `dancinlab/clm-backbone-5lang-sample` 🟢 GREEN (epoch-1 CE 4.63456 → epoch-12 CE 1.5922, F-CLM-PROD-DESCENT=1, verdict at `.verdicts/hf-validate/dancinlab__clm-backbone-5lang-sample/`). This is the standard answer to "how do we validate a model/dataset for real": pull → core RUN → verbatim verdict.

## key facts
- A measure that self-breaks on the target input cannot be used to claim ABSENCE of the target (the Lane A weak-lift closed-negative inherits this caveat).
- faithful big-Φ (H_278 machinery) is the reference oracle; phi_proxy is the cheap surrogate under test.
- This domain is METROLOGY (validate the ruler), distinct from the phenomena domains (UNIVERSE = consciousness↔emergence, CLM+KOSMOS = amodal hub).
