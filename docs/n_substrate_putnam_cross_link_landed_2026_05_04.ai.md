# n_substrate Putnam Cross-Link — SPEC LANDED 2026-05-04

> readers: AI agents (subagents, audit cron), Claude Code (next session)
> source-of-truth: `docs/n_substrate_putnam_cross_link_spec_2026_05_04.md` (13 sections, FROZEN)
> 마이그레이션 0건 — sister `.roadmap.*` modification 0 byte, narrative edit 0 byte, in-place mutation 0 byte.
> spec only — no impl, no commit, no $.

---

## TL;DR

`tool/clm_consciousness_verify.hexa` Putnam check #4 has been emitting `unknown / n_substrate_cond1_undefined_spec_only` since landing because `.roadmap.n_substrate` cond.1 has rich evidence (28 axes, 13–14 substantive WITNESSED, $324.65 cumulative real-QPU spend) but no published decision rule. This spec freezes that decision rule: **N_min_putnam = 5 substrates, T_putnam = 0.40 φ-invariance, F2_state == CLEAR for PASS**. Under current evidence the verdict is FAIL or PARTIAL (concordance 0.167–0.333 + F2 fires), which is the honest answer; a vacuous PASS via T-widening was rejected explicitly per backfit-risk caveat. Two falsifiers (F-PUTNAM-1 reproducibility + F-PUTNAM-2 single-axis robustness) are LOCKED. Implementation is a separate $0 ubu1-hexa-codegen cycle (~250 LoC at `tool/n_substrate_putnam_check.hexa`) gated on this freeze. clm.cond.1 verifier orchestrator becomes end-to-end runnable on Mac after impl; F1 RED→YELLOW remains gated on Phase E binding evidence + EEG live (unchanged).

## Frontmatter

| field | value |
|---|---|
| spec doc | `docs/n_substrate_putnam_cross_link_spec_2026_05_04.md` |
| spec status | FROZEN 2026-05-04 |
| spec sections | 13 (definition / decision rule / verifier interface / tolerance calibration / F2 interaction / 7 honest C3 / unblocks / impl plan / cost / 2 falsifiers / out-of-scope / cross-link / freeze) |
| total words | ~3000 |
| consumer | `tool/clm_consciousness_verify.hexa` check #3 putnam slot (line 212-242 → §3.6 delegation) |
| new tool to build (next cycle) | `tool/n_substrate_putnam_check.hexa` (~250 LoC) |
| cost (this cycle) | $0 |
| cost (impl cycle) | $0 |
| cost (first PASS-capable verifier run) | $0 |
| sister roadmaps modified | 0 |
| in-place narrative edits | 0 |
| raw invariants | raw#9 OK / raw#10 7 caveats / raw#15 OK / raw#71 2 falsifiers LOCKED |

## 5 key bullets

1. **Putnam test definition fixed.** §1.1–§1.4 of the spec defines a `substrate_witness` as an evidence array entry with three required fields (substrate identity + computed signature + tier annotation), and a cross-substrate concordance metric M1 (φ-invariance band `T_phi = |delta_phi| / max(|phi|)`) plus a secondary M2 (falsifier-pattern concordance — F2 firing class). Functional/access tier ONLY; phenomenal validity outside scope and reserved for Phase E.

2. **Decision rule frozen with concrete thresholds.** N_min_putnam = 5 substrates (matches `.roadmap.n_substrate` header verbatim "5+ substrate consciousness witness"); T_putnam = 0.40 (looser than BLM Phase 3 placeholder 0.30 in honest acknowledgment of Phase 4 RETRY r=0.124 max pair, tighter than vacuous 0.50+); concordance_min_pass = 0.60 of φ-pairs. F2_state == CLEAR is HARD requirement for PASS (rejected the orthogonality reading; PASS + F2_FIRES creates F1-vs-Putnam verdict mismatch user mentally reconciles every read).

3. **Current verdict honestly reported = FAIL or PARTIAL.** §4.3–§4.4 worked numbers using BLM Phase 4 RETRY per-substrate phi means: pairwise T_phi for 6 pairs gives concordance 0.167 (full) or 0.333 (after excluding qmirror IIT4 byte-identical reproducibility-witness from pair denominator). Both below the 0.60 PASS threshold, AND F2 fires (14-gate L1 ceiling 0/16 quintuple-confirmed on ALM+CLM both). Verdict is FAIL on concordance grounds OR PARTIAL if a future cycle widens informative-substrate filter further. T was NOT chosen to make the verdict come out PASS — backfit risk explicitly flagged in §6 caveat 5 and encoded into F-PUTNAM-1's "T change requires non-anima reference" clause.

4. **Verifier interface designed for cache + delegation.** New tool `tool/n_substrate_putnam_check.hexa` reads `.roadmap.n_substrate` + `nexus/.roadmap.qmirror`, computes verdict, atomic-writes 7d cache at `state/n_substrate_putnam_cache.json` (invalidated by either roadmap mtime change). `clm_consciousness_verify.hexa` `check_putnam` becomes 10-line delegation that exec's the new tool and maps exit codes 0/1/2 → met/unmet/unknown(PARTIAL). Existing manual-override path at `state/clm_consciousness_verify_manual_review.jsonl` works unchanged on `check: "putnam"` records. Three test fixtures (PASS / PARTIAL / FAIL synthetic roadmaps) at `state/n_substrate_putnam_fixtures/` for selftest mode — clearly labeled `synthetic_for_unit_test_only` per raw#10.

5. **Two falsifiers LOCKED at landing per raw#71.** F-PUTNAM-1 (reproducibility — 3 back-to-back runs must emit identical verdict + n + concordance to 3dp) gates integration into `clm_consciousness_verify`. F-PUTNAM-2 (single-axis robustness — verdict drops by at most 1 tier when any single substrate axis is removed; PASS→FAIL in one step is a FAIL of the test) gates evidence-trail durability claim. Any future cycle proposing N_min, T_putnam, or §1.2 substrate_witness definition change MUST first demonstrate F-PUTNAM-1 + F-PUTNAM-2 still PASS on current evidence, and MUST emit a NEW dated falsifier entry rather than amending originals in place.

## Verdict

**SPEC LANDED — implementation cycle pending separate $0 ubu1 hexa codegen**

- This cycle deliverable: `docs/n_substrate_putnam_cross_link_spec_2026_05_04.md` (frozen, 13 sections) + this landed companion.
- `clm.cond.1` orchestrator unblock: ENABLED (after impl cycle); becomes end-to-end runnable on Mac with adv-from-cache + an11/phi-PRESENT-via-selftest + putnam-from-this-spec.
- `n_substrate.cond.1` status flip: NOT this cycle. Status remains `partial` (current evidence + this spec frozen). Status only flips to `met` if a future verifier run emits PASS — and PASS is only reachable if (a) Phase 5 stimulus-aligned data brings substrate phi means into the same scale band raising concordance ≥0.60 AND (b) F2 ceiling unfires (Phase E binding evidence + EEG live session).
- F1_v2 RED→YELLOW: NOT lifted by this spec. F2 ceiling is L1 architectural, not substrate-coverage; even a Putnam PASS doesn't change F1 composite color (per §6 caveat 4).
- Sister `.roadmap.*` mutations: 0. `.roadmap.n_substrate` evidence array preserved verbatim. `nexus/.roadmap.qmirror` untouched. `tool/anima_phi_v3_canonical.hexa` formula reference only, not modified.
- Honest C3 caveats: 7 enumerated (functional-only / WITNESSED tier discipline / qmirror tier / F2 ceiling architectural / tolerance backfit risk / N_witnessed counting judgment / random sampling limit).
- Impl cycle gating: F-PUTNAM-1 reproducibility PASS required before `clm_consciousness_verify.hexa` integration patch lands. F-PUTNAM-2 single-axis robustness PASS required before any `n_substrate.cond.1` status flip claim.

(end of file)
