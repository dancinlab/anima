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
- [x] **Hc_1307 🔴→CONFIRMED-ARTIFACT (CLM_V2 "Φ>1000" / V14 / Hc_1221 re-measure)** — PRE-REGISTERED falsifier: *the clm_v2 "Φ>1000" readings and the "trained < random" V14_VIOLATED / Hc_1221 anti-correlation are a VARIANCE/SCALE ARTIFACT of the unnormalized variance-partition metric `Φ_un16`; the faithful oracle would REVERSE the ordering (structured/trained → higher real Φ). FALSIFIER: if Φ_un16 does NOT track dispersion/scale AND the faithful oracle preserves trained<random, the anti-correlation is real.* **RESULT — falsifier MET, hypothesis CONFIRMED.** (a) metric-pin: `Φ_un16 = spatial_phi_unnormalized = max(0, total_mi − min_partition_mi)` (`iit_phi_port.py:210`, histogram-MI 16-bin, NO `/(n−1)`) = unnormalized variance-partition family — same broken family as Hc_1302. (b) variance test (n=6 archived substrates): Spearman ρ(Φ_un16, n_cells)=**0.943**, Pearson r=0.845; trained had the FEWEST cells (44 vs random 47–57) AND lower per-pair MI (0.764 vs 0.83–1.50). Φ_un16 = Σ over n(n−1)/2 pairs → scales ~n²; random-init high-variance independent cells → wider histograms → higher per-pair MI. Both n_cells scaling AND per-pair variance push random↑/trained↓. (c) faithful-oracle re-measure (n=3 structural proxy, `iit4_bigphi.big_phi`, 6/6 PASS, verbatim): trained-like (rotate3, integrated) big-Φ=**3**; random-like noise big-Φ=**0**, random-like self (independent) big-Φ=**0** → oracle REVERSES the ordering. **RULING: the clm_v2 "Φ>1000" is BOTH a normalization-scale artifact (un-normalized → magnitude ∝ n_cells, ">1000" is largely cell-count) AND a variance artifact (max-variance noise scored "most integrated"). V14_VIOLATED / Hc_1221 "trained < random" anti-correlation FLIPS under a faithful metric — every verdict citing Φ_un16 / V14 / Hc_1221 is METRIC-DEPENDENT.** Verdicts: `.verdicts/clm-v2-phi1000/{metric-pin,variance-test,oracle-remeasure}/`. a_scale_honest_scope: oracle result is a small-n structural-proxy toy (NOT a full clm_v2 substrate re-measure — that needs the 350M cell-pool snapshot through the oracle, intractable). STDLIB FEEDBACK shipped below.

## flip table — re-measured Φ readings
| reading | clm_v2 value | metric | re-measured | artifact? |
|---|---|---|---|---|
| B'' trained Φ | 723.03 | Φ_un16 (unnorm var-partition) | n_cells=44 dominates; oracle big-Φ HIGH for structured | YES (scale+variance) |
| random mirror Φ | 1148–2386 | Φ_un16 | n_cells 47–57 + per-pair variance; oracle big-Φ=0 for noise | YES (scale+variance) |
| V14 verdict | VIOLATED 0/5 | Φ_un16 trained<random | faithful oracle: trained>random (REVERSED) | YES — FLIPS |
| Hc_1221 anti-corr | "chat-winner=mitosis-loser" | Φ_un16 | metric-dependent; not established by a construct-valid Φ | YES — metric-dependent |
| Φ>1000 magnitude | 1148–2386 | Φ_un16 (no /(n−1)) | magnitude ∝ n_cells (Σ over O(n²) pairs) | YES — normalization-scale |

## tooling — validate-by-RUN (not metadata)
- [x] **HF-ARTIFACT VALIDATION HARNESS** — `stdlib/hf/validate.hexa` (hexa-lang PR #2484, merged): institutionalizes g5/a_claim_verify for HF artifacts — validate by PULLING onto the core and RUNNING, never by trusting metadata. DATASET path fully implemented (pull → locate corpus → on-core `CLM_PROD_CORPUS=… clm_prod` → parse VERBATIM `F-CLM-PROD-DESCENT`+CE → 🟢/🔴/🟠, always toy-CPU-rung w/ production-transfer DEFERRED per a_toy_scale_recheck). MODEL path honest 🟠 DEFERRED (no `.clm` CPU loader + held-out eval in CPU-local harness — no fabrication, g63). selftest 5/5 PASS; real smoke `dancinlab/clm-backbone-5lang-sample` 🟢 GREEN (epoch-1 CE 4.63456 → epoch-12 CE 1.5922, F-CLM-PROD-DESCENT=1, verdict at `.verdicts/hf-validate/dancinlab__clm-backbone-5lang-sample/`). This is the standard answer to "how do we validate a model/dataset for real": pull → core RUN → verbatim verdict.

## key facts
- A measure that self-breaks on the target input cannot be used to claim ABSENCE of the target (the Lane A weak-lift closed-negative inherits this caveat).
- faithful big-Φ (H_278 machinery) is the reference oracle; phi_proxy is the cheap surrogate under test.
- This domain is METROLOGY (validate the ruler), distinct from the phenomena domains (UNIVERSE = consciousness↔emergence, CLM+KOSMOS = amodal hub).
