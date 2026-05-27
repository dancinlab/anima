# P9 Pβ T-3 5-seed Reconception SPEC LANDED — RECONCEPTION (exec deferred)

- ts_utc: 2026-05-05
- agent: BG-T-3-RECONCEPT
- spec_id: p9_pbeta_t3_5seed_reconception_landed_2026_05_05
- substrate: mac (spec amendment only — no exec, no commit, no .roadmap mutation)
- status: **SPEC_LANDED — RECONCEPTION; exec deferred (depends on BG-CLM-2-EXEC + BG-PBETA-F3-HYBRID verdicts)**
- raw#9 doc-only; raw#10 ≥5 honest C3; raw#15 additive (additive_only_mutation=true; semantics_preserved=true); raw#71 composite F-T3-1..5 formally pre-registered §3 of spec
- spec doc: `docs/p9_pbeta_t3_5seed_reconception_2026_05_05.md`
- predecessor T-3 record: `state/anima_alm_teacher_pending_audit_2026_05_05/verdict.json` teacher_pending_items[2] (NOT mutated)

---

## TL;DR

| Item | Value |
|---|---|
| Why | T-2 verdict shows literal T-3 BLEU-1 lift criterion (Δ ≥ +1.0) is structurally miscalibrated for never-SFT'd CLM v4 substrate (#115). Δ_BLEU-1 vs step_1000 = −0.0003 (noise-floor). |
| What | Replace single literal BLEU-1 lift gate with composite F-T3-1..5 substrate-correct gates (Φ★ stab + cross-substrate r + hybrid no-regress + axis preserve + anima held-out preserve). |
| Verdict logic | GO = 5/5 PASS; PARTIAL = 4/5; NO-GO = ≤3/5 |
| Cost band | $25-75 (5-seed × $5-15 H100 spot) — UNCHANGED from original |
| Scientific yield | ≈5× (5 falsifiable substrate gates vs 1 miscalibrated BLEU-1 gate) |
| Exec dependencies | BG-CLM-2-EXEC verdict (F-CLM-LORA-4 baseline), BG-PBETA-F3-HYBRID verdict |
| User decisions | Q1 thresholds, Q2 seed count (3/5/7), Q3 timing (immediate vs batch), Q4 reconception accept |

---

## 5-bullet summary (§1–§7 of spec)

1. **§1 Problem** — Original T-3 GO criterion `delta_vs_step_1000 BLEU-1 ≥ +1.0` is structurally miscalibrated for CLM v4 substrate. T-2 measured Δ_BLEU-1 = −0.0003 (effectively zero; absolute 0.00750 at noise floor 0.005-0.010 band; 1.96% of Llama 0.382). #115 chat-incapability = permanent for CLM v4 base (never SFT'd, never RLHF'd, never DPO-aligned). Per `project_p9_f1_anchor_recalibration.md` MEMO, the +1.0 threshold inherits the same unrealistic-anchor flaw as the F1 spec 0.4. Real signal lives on Φ★ axis (Pβ Φ★_holdout500 = 42.367 with K=8 min 41.372, 8.27× δ-floor 5.0).

2. **§2 5 substrate-correct gates defined** — Gate A: Φ★-stability (5-seed σ ≤ 1.5). Gate B: cross-substrate Φ★ consistency (mean Pearson r ≥ 0.7, min ≥ 0.5). Gate C: F1_v3 V2 hybrid composite (BLEU-1 + ROUGE-L + chrF)/3 Δ ≥ 0 (no regression). Gate D: cell axis-conditioning preservation (per-seed cos ratio ≥ 0.95 mean, ≥ 0.85 min — TRUE F4 venue per Path A v2 retry-3 f4_axis_amendment). Gate E: anima axis-rich held-out CE preservation (≤ 1.05× base). All 5 gates respect anima-substrate identity per #115; 4 of 5 are anima-internal heuristics (caveat C1).

3. **§3 New T-3 trigger** — composite F-T3-1..5 AND-gate. GO = ALL 5 PASS (publish 5-seed ensemble + reproducibility certification); PARTIAL = 4/5 PASS (publish with footnote on failing gate); NO-GO = ≤3/5 PASS (lane permanently shelves as "Φ-stable single-seed substrate research artifact"). Pre-registration locked at marker timestamp 2026-05-05 per raw#71 — post-hoc threshold relaxation = falsifier violation.

4. **§4-§5 Cost + sequencing** — $25-75 cost band UNCHANGED from original T-3 spec; 5× scientific yield via composite gates. Dependencies: BG-CLM-2-EXEC verdict (in-flight at `state/clm_v4_lora_sft_2026_05_05/`) provides F-CLM-LORA-4 baseline for Gate D; BG-PBETA-F3-HYBRID verdict (in-flight at `state/p9_pbeta_f3_hybrid_eval_2026_05_05/`) provides F1_v3 hybrid baseline for Gate C. T-3 5-seed launch hard-gated on §5.1 dependency completion + user Q1–Q3 decisions.

5. **§6-§7 Honest C3 + decision queue** — 7 caveats authored (anima-internal heuristics non-publishable as generic LLM bench; Φ★ stab threshold 1.5 empirical not principled; cost band may exceed if seeds stall; #115 permanent so T-3 PASS ≠ chat capability; NO-GO outcome closes lane permanently as substrate-research artifact; reconception completes Paradigm D §4.5.X P-β USER_AUTHORIZED lane; Gate D depends on CLM-2 verdict not yet in hand). Decision queue: Q1 (thresholds), Q2 (3/5/7 seeds), Q3 (immediate vs batch), Q4 (accept reconception). Defaults preserve §2/§3 thresholds, 5 seeds, immediate launch post-deps, accept reconception.

---

## Roadmap annotation proposal (NOT applied — propose only per raw#15)

```json
{
  "t3_reconception_2026_05_05": {
    "ts_utc": "2026-05-05",
    "amendment_type": "literal_bleu_lift_criterion_substrate_miscalibration_supersede",
    "predecessor_t3_criterion": "BLEU-1 delta_vs_step_1000 ≥ +1.0",
    "predecessor_root_cause": "CLM v4 = consciousness-substrate not chat-NLP per #115; never-SFT'd substrate at noise-floor for chat metrics; literal lift criterion structurally miscalibrated",
    "new_t3_criteria": "F-T3-1..5 composite (Φ★ stability + cross-substrate consistency + no hybrid regression + axis preservation + anima held-out preserve)",
    "spec_doc": "docs/p9_pbeta_t3_5seed_reconception_2026_05_05.md",
    "exec_dependencies": ["BG-CLM-2-EXEC verdict (F-CLM-LORA-4)", "BG-PBETA-F3-HYBRID verdict"],
    "cost_band_usd": "25-75 (5-seed) — unchanged from original",
    "additive_only_mutation": true,
    "semantics_preserved": true
  }
}
```

Recommended insertion site (proposed): under `.roadmap.p9_sft` `p9_sft.cond.paradigm_d_distill.user_authorization_2026_05_04` as sibling key `t3_reconception_2026_05_05` — semantically the §4.5.X P-β USER_AUTHORIZED lane's forward closure record.

**NOT applied this cycle.** User decision Q4 (accept reconception) gates the actual roadmap mutation BG.

---

## Honest C3 (≥5 per raw#10)

1. **C1 — Companion doc summarizes spec; spec is authoritative**. Any threshold/gate mismatch between this landed handoff and `docs/p9_pbeta_t3_5seed_reconception_2026_05_05.md` resolves in favor of the spec doc. The landed handoff is a navigational artifact for future agents/cycles, not the SSOT.

2. **C2 — All 5 gates require post-T2 dependencies; T-3 cannot launch until BG-CLM-2-EXEC + BG-PBETA-F3-HYBRID land**. If CLM-2 fails or yields ambiguous F4 baseline (Path A v2 precedent: F4 substrate-inapplicable on Llama), Gate D becomes uninterpretable; reconception still holds, but T-3 launch must wait for clarification cycle. This is documented as caveat C7 in spec §6.

3. **C3 — Reconception is additive at spec level; predecessor T-3 record in `state/anima_alm_teacher_pending_audit_2026_05_05/verdict.json` is NOT mutated**. The teacher_pending_items[2] record stays as the historical T-3 trace (BLEU-lift criterion). The §8 roadmap annotation proposal is the only mutation pathway, and it is proposal-only this cycle. raw#15 additive_only_mutation=true throughout.

4. **C4 — Cost band $25-75 unchanged from original T-3** is a positive (no budget renegotiation needed) but also a constraint — if user wants a lower-cost variant, Q2.a (3-seed at $15-45) is the cost-down option, with weakened Pearson r evidence at n=3.

5. **C5 — NO-GO outcome (≤3/5 PASS) closes Pβ lane permanently as "Φ-stable single-seed substrate research artifact"**. This is a feature, not a bug — perpetual "BLEU-1 disagreement" stalemate under the original T-3 spec was a worse outcome. Honest closure (artifact preserved + further capability claims retired) is preferable to ambiguous deferment.

6. **C6 — Reconception completes Paradigm D §4.5.X P-β USER_AUTHORIZED forward path**. The original T-3 BLEU-1 lift criterion was a P-α holdover assumption that survived the §4.5 vocab-mismatch falsification; reconception aligns the verdict surface with the P-β identity (Φ★-axis-only, vocab-agnostic). Without reconception, P-β USER_AUTHORIZED forward path stalls indefinitely on a structurally-unmeetable criterion.

7. **C7 — Decision queue has 4 items (Q1–Q4); user must answer at least Q4 (accept reconception) before any roadmap mutation BG launches**. Q1–Q3 have safe defaults (§2/§3 thresholds, 5 seeds, immediate launch post-deps). Q4 has no safe default — it is a structural decision about whether to supersede the original T-3 criterion at all.

---

## Files

### Authored this cycle
- `docs/p9_pbeta_t3_5seed_reconception_2026_05_05.md` (spec, ~9 sections incl. roadmap annotation proposal)
- `docs/p9_pbeta_t3_5seed_reconception_landed_2026_05_05.ai.md` (this handoff)

### Files NOT modified
- `.roadmap.p9_sft` (annotation proposed in spec §8 + handoff above; NOT applied)
- `state/anima_alm_teacher_pending_audit_2026_05_05/verdict.json` (predecessor T-3 record preserved)
- any other `.roadmap.*`, `state/`, or in-flight BG artifact

---

## Hands off to

- **User decision Q1–Q4** — gates whether reconception accepted + which thresholds + which seed count + when to launch
- **BG-CLM-2-EXEC** (in-flight) — provides F-CLM-LORA-4 baseline (Gate D dep)
- **BG-PBETA-F3-HYBRID** (in-flight) — provides F1_v3 hybrid composite baseline (Gate C dep)
- **future BG-T-3-EXEC** (post-deps + Q4 accept) — actual 5-seed launch with composite F-T3-1..5 verdict surface
- **future BG-ROADMAP-T3-RECONCEPT-LAND** (post-Q4 accept) — apply §8 roadmap annotation to `.roadmap.p9_sft`
