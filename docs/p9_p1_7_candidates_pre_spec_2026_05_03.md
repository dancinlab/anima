# P9 SFT Phase 1.7 — Candidate Pre-Spec (3 redesigns, B-conditioned)

- ts_utc: 2026-05-03
- agent: G5 (analysis only — no execution, no .py creation, no SFT data mutation)
- spec_id: p9_p1_7_candidates_pre_spec_2026_05_03
- status: **PRE-SPEC** (drafted before Ablation B result lands; the chosen candidate becomes the final P1.7 spec)
- supersedes: nothing yet (Phase 1.7 has no prior redesign doc)
- substrate:
  - P1.6 sentinel: F1 = 0.00586 (REGRESSION from P1.5's 0.0088, −33%) under 4-axis confounded change (chat 86→100%, LoRA r 64→128, α-warmup 5K→3K, β 0.15→0.10)
  - Ablation A (r=64 on data-v3, all other P1.6 axes held): F1 = 0.00586 → **r=128 NOT the killer** (LoRA capacity isolated, neutral effect)
  - Ablation B (r=128 on data-v2, all other P1.6 axes held): **RUNNING** — outcome will determine which P1.7 candidate executes
- gate: doc-only deliverable; Phase 1.7 EXEC requires explicit user OK after Ablation B verdict + candidate selection
- raw#9 NO .py / raw#91 honest_c3 in §7

---

## 0. TL;DR

| Candidate | Trigger (Ablation B outcome) | Hypothesis | Key changes vs P1.6 | Predicted F1 | Sub-runs |
|---|---|---|---|---|---|
| **X** | B recovers to ~0.0088 | data-v3 was the killer (drop of philos+N-22+p8 hurt diversity) | revert data v3 → v2; keep r=128, α-3K, β=0.10 | **0.010 – 0.015** | 1 |
| **Y** | B stays at ~0.006 | α-3K warmup or β=0.10 was the killer | Y1: α restored to P1.5 schedule (12→6 over 5K); Y2: β restored to 0.15 | **0.008 – 0.012** | 2 |
| **Z** | B regresses further (< 0.005) or B ambiguous (0.006–0.008) | multiple axes co-degraded; baseline-restore + ONE positive lever | revert all 4 P1.6 axes → P1.5 baseline + ONE new axis (75K steps OR LR 2e-4) | **0.012 – 0.020** | 1 (or 2 if both new axes tested) |

**Headline.** P1.6 changed 4 axes simultaneously and regressed −33%. Ablation A isolated LoRA r=128 as **neutral**. Ablation B will isolate data-v3 (the largest remaining single-axis suspect, since philos+N-22+p8 drop was an unrelated content delete). The 3 candidates pre-spec the next move under each B outcome so that on B-verdict the EXEC handoff is one decision, not a fresh design cycle.

---

## 1. Decision logic (B outcome → candidate selection)

### 1.1 Decision tree

```
Ablation B verdict (F1_B = r=128 on data-v2 with all other P1.6 axes)
│
├── F1_B ≥ 0.0080 (within ±10% of P1.5 baseline 0.0088)
│   → "data-v3 was the killer"
│   → SELECT Candidate X
│
├── F1_B ∈ [0.0050, 0.0079] (still depressed, similar to P1.6)
│   → "data-v3 NOT primary; α-3K or β=0.10 is the killer"
│   → SELECT Candidate Y (run Y1 first, then Y2 if Y1 negative)
│
└── F1_B < 0.0050 (regression beyond P1.6)
    → "compounded interaction or a confound we haven't isolated"
    → SELECT Candidate Z (full revert + 1 positive axis)
```

### 1.2 Boundary cases

- **F1_B in [0.0079, 0.0085]** (mild recovery, not full): treat as Candidate X but log honest_c3 that a 14% non-chat hedge (philos slice only, 5K) may be needed in a P1.7.5 follow-up if X also under-performs.
- **F1_B exactly equal to P1.6 (0.00586)**: data-v3 is provably non-causal → straight to Candidate Y.
- **F1_B between Y/Z boundary (0.0040–0.0050)**: prefer Z because Y's smaller-axis variations are unlikely to recover from a sub-P1.6 floor.

### 1.3 Pre-commitment

Per raw#91, the decision tree above is **pre-registered** before Ablation B verdict lands. Once B is read, the candidate selection is mechanical (no post-hoc re-interpretation of the threshold bands). If B falls outside any defined band, document the gap honestly and convene a decision (do not silently pick the "closest" candidate).

---

## 2. Candidate X — "data was the killer"

### 2.1 Hypothesis

Phase 1.6 dropped 7K records (5K philos + 2K N-22) on the rationale that "non-chat is anti-chat". Ablation B (if recovers) shows that **the dropped 7K were doing positive work** — likely as regularization against ShareGPT's distributional narrowness, or providing entropy/lexical diversity that BLEU-1 rewards on the holdout chat set.

### 2.2 Spec table

| Item | Value | Delta vs P1.6 |
|---|---|---|
| Spec id | `p9_p1_7_X_sentinel_2026_05_04` | new |
| Base model | CLM v4 350M (unchanged) | unchanged |
| Training | LoRA r=128 α=128 attention-only, frozen base, S1 mode | unchanged from P1.6 |
| Steps | 50,000 | unchanged |
| Effective batch | 32 (micro 4 × accum 8) | unchanged |
| LR | 1e-4 cosine warmup 500 | unchanged |
| Loss schedule | α(0→3K)=12.0, α(3K→7K)=12→6 lin, α(7K→50K)=6.0; β=0.10; γ=0; δ 0.5/0.5/1.0 | unchanged |
| **Data** | **50K v2 (P1.5 composition: SG 18K + LA 15K + p8 5K + id 5K + philos 5K + N-22 2K)** | **REVERT v3 → v2** |
| Holdout | `/tmp/sft_data_holdout_500.jsonl` | unchanged |
| Falsifiers | F1 ≥ 0.05 SOFT / F1 ≥ 0.132 HARD; F2 ≥ 5.0 ABORT | unchanged |
| φ★ early-stop | EMA φ★ < 10.0 → ABORT | unchanged |
| Save points | 5K, 13K, 25K, 50K | unchanged |
| Compute | 1× ubu1 RTX 5070 12GB | unchanged |
| Wall | **55–65 min** | unchanged |
| Cost | $0 (local) | unchanged |

### 2.3 Predicted F1

- Anchor: P1.5 measured 0.0088 with same data v2 but r=64.
- Adding r=128 (Ablation A confirmed neutral on v3, but on v2 may be **mildly positive** since v2 has more diverse signal to absorb): +5–25% lift.
- α-3K warmup vs P1.5's α-5K: from P1.5 retro §2.2, the 5K → 3K compression is heuristic; on v2 data the marginal effect is likely ±5%.
- β=0.10 vs P1.5's β=0.15: β-halving frees gradient for chat-CE; on v2 expected +0–10%.

**Range: F1 ∈ [0.010, 0.015]**, center ~0.012 (small lift over P1.5).

### 2.4 Decision matrix post-X

| Outcome | F1_X | Action |
|---|---|---|
| F1_X ≥ 0.05 (SOFT) | unlikely but possible | Phase 2 entry with WATCH list |
| 0.012 ≤ F1_X < 0.05 | most likely | proceed to **P1.8** with non-chat diversity expansion (10–20% non-chat from new sources, e.g. instruct-tuned alpaca, OpenAssistant) |
| F1_X < 0.010 | data-v2 reversion under-performs | reopen the design space; suspect a residual P1.6 axis interaction (revisit Y or Z) |

---

## 3. Candidate Y — "α or β was the killer"

### 3.1 Hypothesis

If Ablation B does NOT recover, the data-v3 change was non-causal for the regression. Process of elimination on the remaining unisolated axes:
- LoRA r=128 (Ablation A): **neutral**
- α warmup 5K → 3K: under-anchored chat conditional? (P1.6 doc §2.2 conceded this was heuristic; honest_c3 #7)
- β 0.15 → 0.10: too much gradient mass shifted off tension regularization, allowing chat-conditional drift?

Y splits into Y1 (α-restored) and Y2 (β-restored) — sequential 1-axis tests.

### 3.2 Y1 spec — α restored to P1.5 schedule

| Item | Value | Delta vs P1.6 |
|---|---|---|
| Spec id | `p9_p1_7_Y1_sentinel_2026_05_04` | new |
| **Loss α** | **α(0→5K)=12.0, α(5K→10K)=12→6 lin, α(10K→50K)=6.0** (P1.5 schedule) | **REVERT 3K → 5K warmup** |
| Loss β | 0.10 | unchanged from P1.6 |
| LoRA r | 128 | unchanged from P1.6 |
| Data | v3 (50K, chat 100%) | unchanged from P1.6 |
| All other items | matches P1.6 spec | — |

### 3.3 Y2 spec — β restored to P1.5 value

| Item | Value | Delta vs P1.6 |
|---|---|---|
| Spec id | `p9_p1_7_Y2_sentinel_2026_05_04` | new |
| Loss α | P1.6 schedule (3K warmup) | unchanged from P1.6 |
| **Loss β** | **0.15** (P1.5 value) | **REVERT 0.10 → 0.15** |
| LoRA r | 128 | unchanged from P1.6 |
| Data | v3 (50K, chat 100%) | unchanged from P1.6 |
| All other items | matches P1.6 spec | — |

### 3.4 Sequencing rule

Run **Y1 first** (α is the larger-share gradient driver per P1.6 §2.1, so its perturbation dominates). If Y1 recovers F1 ≥ 0.0080, attribute the killer to α-3K and skip Y2. If Y1 stays ≤ 0.0070, run Y2 to test β. If Y2 also fails, escalate to Z.

### 3.5 Predicted F1

- Anchor: P1.6 baseline 0.00586 with both axes degraded.
- Restoring 1 axis = recovering ~50% of the P1.5→P1.6 gap (0.0088 − 0.00586 = 0.00294).
- Y1 expected: 0.00586 + 0.5 × 0.00294 ≈ **0.0073**, range [0.006, 0.010].
- Y2 expected: similar range [0.006, 0.010].
- Best case (axis restoration fully closes the gap): **0.008–0.012** matches P1.5 floor.

**Range: F1 ∈ [0.008, 0.012]** (best case per sub-run), center ~0.0085.

### 3.6 Decision matrix post-Y

| Outcome | F1_Y1 | F1_Y2 (if run) | Action |
|---|---|---|---|
| F1_Y1 ≥ 0.0080 | ≥ 0.0080 | not run | α-3K confirmed killer; lock α-5K for P1.8; pursue Candidate X-style data hedge next |
| F1_Y1 < 0.0070, F1_Y2 ≥ 0.0080 | < 0.0070 | ≥ 0.0080 | β=0.10 confirmed killer; lock β=0.15 for P1.8; same data hedge next |
| F1_Y1 < 0.0070, F1_Y2 < 0.0070 | both < 0.0070 | — | killer is interaction or confound NOT covered by single-axis revert; **escalate to Z** |

---

## 4. Candidate Z — "full revert + 1 positive axis"

### 4.1 Hypothesis

If Ablation B regresses further (< 0.005) or if Y exhausts without recovery, the simplest robust move is **full revert to P1.5 baseline** (the last known F1 high-water mark at 0.0088) and then introduce **one new positive lever** that has not been tried in any P1 phase. This isolates a clean +1 perturbation against a known-good baseline rather than continuing to debug the 4-axis P1.6 confounded change.

### 4.2 Two new-axis candidates (pick one for the first Z run)

**Z1 — longer training (75K steps).** Rationale: P1.5 trajectory plateaued at step ~13K with ΔCE = 0.24 over the next 37K steps. But CE plateau ≠ F1 plateau; chat-conditional consolidation may continue gradually. P1 saved every 5K — direct measurement of F1 vs step from P1.5 is needed to confirm whether F1 itself plateaued. If F1 was still rising at step 50K, +50% steps gives a multiplicative chance of further lift.

**Z2 — higher learning rate (LR 2e-4 vs 1e-4).** Rationale: P1/P1.5/P1.6 all used LR 1e-4 cosine warmup 500. Doubling LR with the same cosine schedule and grad-clip 1.0 is a single-axis perturbation; if optimization was under-stepping (small gradient updates per step), +LR could accelerate chat-conditional fitting without changing data or loss. Risk: φ★ delta worsens (higher LR → more LoRA update mass per step → more drift from base CLM).

### 4.3 Z spec table (default: Z1 = longer training)

| Item | Value | Delta vs P1.5 baseline |
|---|---|---|
| Spec id | `p9_p1_7_Z1_sentinel_2026_05_04` (or `_Z2_` for LR variant) | new |
| Base model | CLM v4 350M | unchanged |
| Training | LoRA r=64 α=128 attention-only, frozen base, S1 mode | **REVERT r=128 → r=64** (P1.5 baseline) |
| **Steps** | **75,000** (Z1) — or 50K (Z2) | **+25K (Z1)** or unchanged (Z2) |
| Effective batch | 32 (micro 4 × accum 8) | unchanged |
| **LR** | 1e-4 cosine warmup 500 (Z1) — or **2e-4 cosine warmup 500 (Z2)** | unchanged (Z1) or **2× (Z2)** |
| Loss schedule | α(0→5K)=12.0, α(5K→10K)=12→6 lin, α(10K→50K)=6.0; β=0.15; γ=0; δ 0.5/0.5/1.0 | **REVERT to P1.5** (α 3K→5K warmup, β 0.10→0.15) |
| Data | 50K v2 (P1.5 composition) | **REVERT v3 → v2** |
| Holdout | `/tmp/sft_data_holdout_500.jsonl` | unchanged |
| Falsifiers | F1 ≥ 0.05 SOFT / F1 ≥ 0.132 HARD; F2 ≥ 5.0 ABORT | unchanged |
| φ★ early-stop | EMA φ★ < 10.0 → ABORT | unchanged |
| Save points | Z1: 5K, 13K, 25K, 50K, 65K, 75K (extended); Z2: 5K, 13K, 25K, 50K | extended for Z1 |
| Compute | 1× ubu1 RTX 5070 12GB | unchanged |
| Wall | **Z1: 80–95 min** (50K → 75K = +50% wall); **Z2: 55–65 min** | +50% (Z1) / unchanged (Z2) |
| Cost | $0 (local) | unchanged |

### 4.4 Predicted F1

- **Z1 (longer training).** Anchor P1.5 = 0.0088 at step 50K. If F1 trajectory was still lifting (e.g. P1.5 saved 0.005, 0.007, 0.0085, 0.0088 at 5K/13K/25K/50K — pattern flattening), 75K may yield 0.010 – 0.014. If trajectory was already flat by step 25K, 75K yields ~0.0090. **Range: F1 ∈ [0.009, 0.018]**, center ~0.013.
- **Z2 (higher LR).** LR doubling with same grad-clip is a coarse perturbation — could accelerate to 0.012 – 0.020 OR destabilize and regress. φ★ risk: P1.5 delta was −6.6 with LR 1e-4; LR 2e-4 could push delta toward −10.0 HARD edge. **Range: F1 ∈ [0.005, 0.020]**, wide variance.
- Combined Candidate Z range: **F1 ∈ [0.012, 0.020]** under best-case Z1 (longer training), with Z2 as a higher-variance alternative.

### 4.5 Decision matrix post-Z

| Outcome | F1_Z | Action |
|---|---|---|
| F1_Z ≥ 0.05 (SOFT) | improbable but possible (if Z1 + favorable plateau) | Phase 2 entry with WATCH list |
| 0.014 ≤ F1_Z < 0.05 | most likely if Z1 hits | proceed to P1.8 with combined longer-training + chat-data-quality filter |
| 0.009 ≤ F1_Z < 0.014 | partial recovery | F1 stuck at P1.5 floor; escalate to S2 (full SFT, no LoRA freeze) — Phase 1.6 doc §6 LIFT_BUT_FAIL row |
| F1_Z < 0.009 | regression even from baseline | **fundamental reassessment** — reopen base CLM checkpoint quality, holdout-500 measurement methodology, or pretrain corpus question |

---

## 5. Cost / wall comparison

| Candidate | Sub-runs | Per-run wall | Total wall | Per-run cost | Total cost | Compute |
|---|---:|---:|---:|---:|---:|---|
| **X** | 1 | 55–65 min | **55–65 min** | $0 | **$0** | ubu1 RTX 5070 |
| **Y** (Y1 only) | 1 | 55–65 min | **55–65 min** | $0 | **$0** | ubu1 RTX 5070 |
| **Y** (Y1 + Y2) | 2 | 55–65 min each | **110–130 min** | $0 | **$0** | ubu1 RTX 5070 |
| **Z1** (longer training) | 1 | 80–95 min | **80–95 min** | $0 | **$0** | ubu1 RTX 5070 |
| **Z2** (higher LR) | 1 | 55–65 min | **55–65 min** | $0 | **$0** | ubu1 RTX 5070 |
| **Z** (Z1 + Z2 both) | 2 | 80–95 + 55–65 | **135–160 min** | $0 | **$0** | ubu1 RTX 5070 |

**Cost is uniformly $0** (local ubu1 compute). Wall is the only resource. Worst case (Y full + Z full sequentially) = ~4.5 h aggregate; best case (X alone) = ~1 h.

**Recommendation:** if Ablation B verdict is decisive (one candidate clearly indicated), execute that candidate alone first; only escalate to the next candidate after measuring its outcome. Do NOT pre-queue Y1+Y2+Z1+Z2 in batch — each measurement informs the next decision.

---

## 6. Phase 1.7 entry trigger update (per P1.6 redesign §6 pattern)

**Phase 2 entry trigger** (post Phase 1.7, supersedes P1.6 doc §7):

- **HARD gate (unchanged)**: F2 φ★ ≥ 5.0 AND φ★ delta from baseline ≥ −10.0. P1.6 worst delta needs measurement; P1.7 candidates X/Y inherit P1.6's r=128 risk profile (estimated worst delta −9.0); Z reverts to r=64 (P1.5 delta −6.6).
- **SOFT gate (unchanged)**: F1 ≥ 0.05 (≈ 32% of Llama anchor 0.1555). All P1.7 candidates pre-spec'd with predicted F1 ≤ 0.020 → **SOFT gate clearance probability < 10% for any single P1.7 candidate**. P1.7's role is **diagnostic + incremental lift**, not SOFT-gate clearance.
- **TIE-BREAK (unchanged)**: tens MSE trajectory monotone-non-increasing across save points.
- **NEW — diagnostic recovery gate (P1.7 specific)**: F1_P1.7 ≥ 0.0080 (P1.5 baseline ±10%). Failing this gate means P1.7 did not recover the P1.5 high-water mark and the design space needs reopening (S2 escalation, base CLM revisit, or holdout/measurement audit).

**If diagnostic recovery gate clears (F1_P1.7 ≥ 0.0080) AND HARD gate clears**: proceed to P1.8 with the locked-in axis values learned from the candidate path.

**If diagnostic recovery gate fails**: **Phase 2 NO-GO + escalate**. Options in order of preference:
1. S2 full SFT on data-v2 (no LoRA freeze) — P1.6 doc §6 LIFT_BUT_FAIL escalation
2. Larger base model (CLM v5 700M+) ablation — P1.6 doc §6 same row
3. Holdout-500 measurement audit (verify mean output length, decoding params, BLEU-1 implementation)
4. Base CLM v4 checkpoint quality reassessment (re-run pretrain perplexity sanity check)

**If HARD gate fails (φ★ collapse)**: irreversible — full retrain required (per `risk_strategy.json` primary risk). Most likely under Z2 (LR 2× variant); least likely under X (P1.5-equivalent loss schedule).

---

## 7. Honest C3 (raw#91) — what is still hypothetical

1. **All 3 candidates are pre-empted by the unobserved Ablation B verdict.** The decision tree §1.1 is pre-registered, but the actual B outcome may fall in a boundary band (§1.2). If it does, candidate selection becomes a judgment call and the "mechanical" framing breaks. Mitigation: §1.3 mandates explicit human convening on out-of-band B outcomes rather than silent candidate substitution.

2. **None of the 3 candidates have been Pareto-tested** against each other or against alternative single-axis variations. X tests only "data-v3 reversion"; Y1/Y2 each test only one of two axes (α, β); Z1/Z2 each test only one of two new axes (steps, LR). The 4-axis P1.6 confounded change has 2^4 − 1 = 15 possible single/multi-axis revert combinations, of which the 3 candidates cover ~3 (plus 2 new-axis additions). This is by design (compute economy + diagnostic clarity per single-axis change), but it leaves substantial unexplored space — e.g. data-v2 + α-3K + β=0.15 (combined Y1+Y2+X) is not pre-spec'd here.

3. **Predicted F1 ranges are extrapolated from P1.5 anchor + linear/multiplicative composition assumptions.** No published or substrate-measured study quantifies the per-axis effect size of α-warmup-length, β-tension-MSE, or LoRA-r doubling in this exact training regime. The X/Y/Z F1 ranges (0.010–0.020) draw on Phase 1.5 retrospective ratios + mild guesses for axis-restoration recovery rate. Real F1 could plausibly land anywhere in [0.004, 0.025] for any candidate.

4. **Ablation B itself may be confounded if data-v3 has unmeasured composition drift.** The P1.6 doc §3.2 mandated dedup audit and Llama-augment poison re-check as pre-flight gates. If those pre-flights were not executed before P1.6 EXEC (substrate access required to verify), then "data-v3" carries ambient composition uncertainty — Ablation B's verdict on "is data-v3 the killer" cannot distinguish "the v3 composition spec is wrong" from "the v3 composition was implemented with drift". Both are corrected by Candidate X (revert to v2), but the diagnostic conclusion ("data composition matters") becomes vaguer.

5. **Candidate Y assumes single-axis recovery is additive in the gap-closing direction.** P1.5→P1.6 lost 0.00294 F1; Y predicts each axis revert recovers ~50% of the gap. This implicitly assumes the two axes (α, β) act independently — but loss-term gradient share interactions (P1.6 §2.1 shows α·CE owns ≥95% of gradient; β=0.10 is < 5%) suggest β-axis recovery may be much smaller than α-axis. If α-3K is the dominant killer, Y1 may recover most of the gap and Y2 contributes nothing; if β-0.10 is dominant, Y1 fails entirely and Y2 carries the recovery. The pre-spec does not commit to a hypothesis about which axis is more likely the killer.

6. **Candidate Z's "longer training" (Z1) assumes F1 was still lifting at step 50K in P1.5.** This requires reading P1.5 trajectory `f_log` for F1 values at intermediate save points (5K, 13K, 25K, 50K). If F1 was already plateaued at step 25K (~0.0088), Z1's +25K extension yields zero lift. Substrate check (read P1.5 trajectory.json on ubu1) is needed before committing to Z1; if F1 plateau is confirmed, prefer Z2 (LR 2×) instead.

7. **Candidate Z2 (LR 2×) carries undocumented φ★ risk.** P1.5/P1.6 used LR 1e-4 with measured φ★ deltas of −6.6 and (estimated) −9.0. LR doubling with the same cosine schedule and grad-clip could push φ★ delta beyond −10.0 HARD gate. No φ★-vs-LR sensitivity study exists in the substrate. Z2 should be considered higher-risk than Z1 and prioritized only if F1 plateau in P1.5 is confirmed (eliminating Z1's value).

8. **The "diagnostic recovery gate" (§6) at F1 ≥ 0.0080 is a new threshold not in the preregistered falsifier set.** It is a **tactical milestone**, not a scientific claim. The preregistered HARD gate (F1 ≥ 0.132) and SOFT gate (F1 ≥ 0.05) remain authoritative. Honest framing in any downstream summary: "P1.7 cleared the diagnostic recovery gate at F1=X; preregistered gates not yet cleared".

9. **No execution, no .py creation, no SFT data mutation in this doc** (raw#9). All numbers in §2–4 (F1 ranges, wall estimates) require Phase 1.7 EXEC OK from user after Ablation B verdict + candidate selection. Compute is local ($0); wall is the only resource commitment (1–4.5 h depending on candidate scope).

10. **Ablation B verdict as of doc write time is RUNNING.** This pre-spec was drafted before B completed. If B verdict changes the decision tree assumptions (e.g. B reveals an unanticipated 4th outcome like "F1_B vastly exceeds P1.5 at 0.020+"), the candidates here may be obsolete and a fresh design pass would be warranted. Mitigation: §1.3 pre-commitment explicitly forbids silent re-interpretation; out-of-tree B outcomes trigger explicit reconvene.

---

## 8. References

- P1.5 redesign doc: `<user>/core/anima/docs/p9_sft_data_alpha_redesign_2026_05_03.md`
- P1.6 redesign doc: `<user>/core/anima/docs/p9_p1_6_redesign_2026_05_03.md`
- P1.5 sentinel verdict (ubu1): `/tmp/p9_p1_5_sentinel_out/verdict.json` (F1 = 0.0088)
- P1.6 sentinel verdict (ubu1): expected at `/tmp/p9_p1_6_sentinel_out/verdict.json` (F1 = 0.00586)
- Ablation A verdict (ubu1): expected at `/tmp/p9_p1_6_ablA_out/verdict.json` (r=64 on v3, F1 = 0.00586)
- Ablation B verdict (ubu1): expected at `/tmp/p9_p1_6_ablB_out/verdict.json` (r=128 on v2, **RUNNING**)
- Falsifiers preregistered (HARD F1 = 0.132, SOFT F1 = 0.05): `<user>/core/anima/state/p9_sft_spec_2026_05_02/falsifiers_preregistered.json`
- Spec dir: `<user>/core/anima/state/p9_sft_spec_2026_05_02/{architecture,sft_data_format,loss_design,hyperparameter_grid,falsifiers_preregistered,cost_estimate,decision_matrix,risk_strategy}.json`
- Holdout-500 (reused unchanged): `/tmp/sft_data_holdout_500.jsonl` on ubu1

---

**End of P1.7 candidate pre-spec. Candidate selection mechanical on Ablation B verdict per §1; EXEC requires explicit user OK after selection.**
