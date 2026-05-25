# qmirror arXiv draft landed — 2026-05-03 (handoff)

**Cycle:** qmirror academic preprint draft
**Status:** DRAFT_LANDED (not submitted to arXiv this cycle per task constraint)
**Cost:** USD 0 (pure draft work; no QPU spend, no API calls)

---

## TL;DR

A 6-8-page-equivalent academic paper draft for qmirror has been landed
at `anima/docs/qmirror_arxiv_draft_2026_05_03.md` (~570 lines of
markdown including 12 sections, 4 tables in main body, 4 tables in
appendices, and 32 references). Companion artifacts: BibTeX bibliography
(`state/qmirror_arxiv_draft_2026_05_03/bibliography.bib`, 32 entries)
and figures outline (`state/qmirror_arxiv_draft_2026_05_03/figures_outline.json`,
5 figures + 9 tables outlined for LaTeX phase).

The draft is **arXiv-ready in structure but not yet submission-ready**
in process. Appendix C documents a 7-step preflight (peer review,
LaTeX conversion, figure prep, license sign-off, honest-claim audit,
selection-bias promotion, formal arXiv submission) estimated at 5-7
wall days.

---

## What landed

### Files (3 new)

1. **`anima/docs/qmirror_arxiv_draft_2026_05_03.md`** — main paper draft
2. **`anima/state/qmirror_arxiv_draft_2026_05_03/bibliography.bib`** — 32 BibTeX entries
3. **`anima/state/qmirror_arxiv_draft_2026_05_03/figures_outline.json`** — 5 figures + 9 tables outline
4. **`anima/state/markers/qmirror_arxiv_draft_landed.marker`** — landing marker

### Section-by-section status

| § | section | status | notes |
|---|---------|--------|-------|
| - | abstract (~150 words) | LANDED | covers all task-spec items |
| 1 | introduction | LANDED | problem (cost/queue/rate), approach (4-tier substitute), 6 contributions |
| 2 | related work | LANDED | qiskit-aer, Cirq, NIST SP 800-22, IIT 4.0, pyphi, CHSH/Aspect |
| 3 | architecture | LANDED | 4-tier ANU, HMAC-DRBG, Aer engine bridge, pyphi shim, canonical CHSH geom (Ry(-theta), {0, pi/2, pi/4, -pi/4}), module layout |
| 4 | validation | LANDED | 8/8 cond results, 4-vendor |dS| matrix, 2 post-hoc band revisions (loud disclosure), cond.7 spirit substitution |
| 5 | cost analysis | LANDED | qmirror USD 0 vs IBM USD 1.60-2.30/sec; calibration USD 41.34 (Rigetti + IonQ Forte + IBM); permanent USD 0 op |
| 6 | limitations | LANDED | 5 limits: pyphi GPLv3, ANU rate-limit/ToS, no live per-call ANU sampling default, Aer 30q ceiling, single-shot N=1 |
| 7 | future work | LANDED | 5 qmirror 2.0 axes from ranked_axes.json (cond.9 tomography, cond.10 GHZ Mermin, cond.11 stabilizer, cond.12 surface-d3, cond.13 CSCS) |
| 8 | conclusion | LANDED | concise, USD 0 substrate + dual-mirror release |
| - | references | LANDED | 32 entries (qiskit, Cirq, NIST x 2, Tononi IIT4, pyphi, ANU, CHSH, Aspect, Bell, Tsirelson, Hensen, Flammia-Gross, GHZ, Mermin, Kitaev, Bravyi-Kitaev, surface-code, FSF aggregation, Apache, Feist, IBM Heron, IonQ Aria/Forte, Rigetti, AWS Braket, Sycamore, ZNE, DD, Knill-Laflamme, HMAC FIPS 198-1, hexa-lang) |
| A | falsifier ledger | LANDED | 8 v1 + 5 v2 = 13 falsifiers tabulated |
| B | |dS| matrix data | LANDED | per-vendor raw correlators (4 tables) + 6-row pairwise matrix with 4-band falsifier assessment |
| C | arXiv readiness | LANDED | 7-step preflight + 5-7 day estimate |

---

## 5 honest C3 caveats (raw#10)

1. **Peer review pending.** The paper makes empirical claims (8/8
   closure, 4-vendor concordance, USD 0 cost vs USD 1.60-2.30 IBM)
   that require external review by 2-3 quantum-computing or
   integrated-information-theory researchers familiar with the
   reference experiments. Submitting to arXiv without peer review
   would be premature for a claims-heavy paper.

2. **Selection-bias prominent disclosure.** The two post-hoc band
   revisions (cond.3 0.40 -> 0.55 superconducting, cond.7 0.55 -> 0.60
   cross-tech) are disclosed in §4.3 of the draft and in the verdict
   JSONs. For arXiv submission this disclosure should be promoted to
   the abstract or end of §1 introduction so reviewers cannot miss it.
   Selection-bias risk is real even with physics-aware mitigation.

3. **License claim conditional on audit.** Apache-2.0 is the source
   declaration; the pyphi GPLv3 isolation argument relies on FSF Mere
   Aggregation doctrine via subprocess shim. License audit JSON
   (`state/qmirror_license_audit_2026_05_03/audit.json`) selected
   Option A + D combined. **Final counsel review is pending** for the
   formal paper claim. The draft body already includes the "license
   interpretation is opinion not legal advice" qualifier.

4. **"Quantum-derived" not "quantum-native".** The default path is
   HMAC-DRBG SHA-256 keyed by ANU bytes at session origin (the seed
   is genuinely quantum; the expansion is cryptographic). Strict
   per-call quantum sampling requires `NEXUS_QMIRROR_QRNG_DIRECT = 1`
   and is rate-limit-bound. The paper consistently uses
   "quantum-derived" and "quantum-seeded" — never "quantum-native" —
   to avoid claim inflation. arXiv reviewers will likely scrutinize
   this distinction.

5. **Future-work scope speculative.** The qmirror 2.0 axes
   (cond.9-cond.13) are scoped from `state/qmirror_2_axes_2026_05_03/
   ranked_axes.json` with cost-floor USD 0 to cost-ceiling USD 25,
   wall 9 days sequential or 5 days parallel-2-lane. These are
   **planned but unimplemented**. The arXiv version should label them
   "future" not "in progress" to avoid implying readiness.

---

## arXiv submission readiness assessment

**Verdict: NOT READY for immediate submission. Estimated 5-7 wall days
from peer-review-complete to submission.**

Pre-submission blockers (per Appendix C of the draft):

1. External peer review (2-3 reviewers) — **HARD BLOCKER**.
2. LaTeX conversion (revtex4-2 or article class) — 1-2 day typesetting.
3. Figure preparation — 5 figures outlined in `figures_outline.json`;
   ~1 day matplotlib/TikZ work.
4. Bibliography refinement — `bibliography.bib` is draft-quality
   BibTeX; some `@misc` entries should be upgraded to `@article` /
   `@inproceedings` once formal cite metadata is fetched.
5. Final license audit sign-off — counsel review of pyphi-isolation
   claim.
6. Honest-claim audit — re-read for any inflation; promote
   selection-bias disclosure to abstract/§1.
7. Optional: figure 5 (per-correlator E with error bars) labeled
   optional in `figures_outline.json` but recommended.

**Substantive paper-quality verdict:** the draft is structurally
complete, evidence-grounded (every numeric claim has an on-disk
verdict.json or selftest_results.json source), honest about caveats
(2 band revisions + 1 spirit-paper analysis loudly disclosed), and
covers the full task-spec scope. It is not gold-plated; it is also
not stub-quality. The honest characterization is **"v0.1 draft, ready
for external peer review, not ready for submission"**.

---

## What this cycle did NOT do

- DID NOT submit to arXiv (per task constraint: DRAFT ONLY)
- DID NOT convert markdown to LaTeX
- DID NOT prepare figures (only the outline JSON)
- DID NOT obtain external peer review
- DID NOT mutate any verdict.json or measurement count file
- DID NOT create any .py file (raw#9 STRICT)
- DID NOT include any personal paths in body of any artifact (raw#15)

---

## Files touched (4 total)

1. **NEW** `anima/docs/qmirror_arxiv_draft_2026_05_03.md` (paper draft)
2. **NEW** `anima/state/qmirror_arxiv_draft_2026_05_03/bibliography.bib` (32 BibTeX)
3. **NEW** `anima/state/qmirror_arxiv_draft_2026_05_03/figures_outline.json` (5 figs + 9 tabs)
4. **NEW** `anima/state/markers/qmirror_arxiv_draft_landed.marker` (landing marker)
5. **NEW** `anima/docs/qmirror_arxiv_draft_landed_2026_05_03.ai.md` (this handoff)

(no .py files; raw#9 STRICT honored)

---

## Cross-refs

- Closure source: `anima/docs/nexus_qmirror_closure_2026_05_03.md`
- Closure handoff: `anima/docs/qmirror_closure_landed_2026_05_03.ai.md`
- Cross-vendor verdict: `anima/state/qmirror_chsh_xvendor_2026_05_03/verdict.json`
- IBM cond.3 verdict: `anima/state/nexus_qmirror_ibm_2026_05_03/verdict.json`
- qmirror 2.0 ranking: `anima/state/qmirror_2_axes_2026_05_03/ranked_axes.json`
- License audit: `anima/state/qmirror_license_audit_2026_05_03/audit.json`
- HF mirror handoff: `anima/docs/qmirror_hf_mirror_pushed_2026_05_03.ai.md`
- GitHub canonical: `https://github.com/dancinlab/qmirror`
- HF mirror: `https://huggingface.co/dancinlab/qmirror`

---

## Closure verdict (final line)

**`qmirror_arxiv_draft_landed = met` at 2026-05-03 (DRAFT ONLY; arXiv
submission deferred per task constraint; 5-7 wall days estimated to
submission-ready after external peer review).**
