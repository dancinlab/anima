# P9 Path A retrain v2 — spec landed (handoff)

- **cycle**: BG-Φ 2026-05-04 (parallel to BG-Χ recovery + BG-Ψ Instruct-eval)
- **deliverable family**: spec doc + decision matrix + falsifier set + corpus mix JSON + marker
- **git**: NO — design only; user lands commits in separate cycle
- **cost**: $0 — design only

---

## TL;DR

- Spec landed for Path A LoRA retrain v2 to fix catastrophic forgetting confirmed in BG-Ρ Mode 1 eval (`fa7db7bc` — INFRASTRUCTURE_PASS / SCIENCE_FAIL, ALL 3 benchmarks negative Δ vs Llama base).
- **Recommended strategy**: **S1 + S3 combined** = 60/30/10 rehearsal mix (anima / academic-distillation / chat-template) + lr 1e-4 → 5e-5 + max_steps 10000 → 6000 + intermediate eval @ step 2000.
- **Cost band**: $20-30 H100 (~3.75-7h on H100 SXM at $2.99/hr).
- **Pre-registered F1_v3 V2 PASS thresholds (LOCKED 2026-05-04)**: parity-floor on all 3 benchmarks (HellaSwag −1pp, MMLU −1pp, TriviaQA −2pp) AND ≥1 benchmark IMPROVES on base by ≥2pp.
- **Falsifiers F-PA-RETRAIN-v2-1~4**: train-loss convergence / step-2000 ≤−5pp early-stop / final V2 PASS / anima-axis preservation (BLEU-1 ≥ v1).
- **EXEC gate**: USER ACK required next cycle ($20-30 retrain + ~$2 eval).

---

## Decision matrix (S1-S6)

| ID | Strategy | $ | Wall | Complexity | Magnitude | Recommended? |
| --- | --- | --- | --- | --- | --- | --- |
| **S1** | Rehearsal SFT mix | $20-25 | 6-8h | LOW | HIGH | RANK 1 (combined w/ S3) |
| S2 | Replay buffer (pretrain shards) | $35-50 | 10-15h | MEDIUM | HIGHEST | RANK 3 |
| **S3** | Lower LR / early stop | $15-20 | 4-6h | LOW | MEDIUM | RANK 1 (combined w/ S1) |
| S4 | LoRA r=64 → r=16 | (external) | (external) | (external) | MEDIUM | NOT (already external `11331fe4`) |
| S5 | Knowledge distillation (paradigm D logit-axis) | $30-50 | 8-12h | HIGH | HIGH | RANK 2 (alternative if S1+S3 PARTIAL) |
| S6 | Multi-task heads (router) | $50-80 | 12-20h | HIGH | HIGHEST | NOT (eval framework++) |

**Combined recommendation**: S1+S3 single-run at $20-30 / 3.75-7h, falsifier-bound F-PA-RETRAIN-v2-1~4. If V2 PARTIAL, escalate to S5.

---

## Cross-link

- **BG-Ρ Mode 1 eval driver**: `fa7db7bc` — `state/p9_lora_mode1_eval_2026_05_04/verdict.json` (INFRASTRUCTURE_PASS / SCIENCE_FAIL).
- **BG-Ξ amendment** `f6eb6517` — F1_v3 V2 criteria framework (c3 2σ, c4 random+5pp).
- **BG-Ξ omnibus hint** `11331fe4` — catastrophic forgetting prediction + external r=16 retrain pods (`nzw0btc8br78yy`, `0jetjpvlm51zoy`).
- **BG-Ο anchor** `93bef8c8` — `state/p9_base_validation_llama_anchor_2026_05_04/verdict.json` Llama-3.2-3B non-Instruct anchors (used as §4 reference).
- **BG-Μ anchor** `1ef3c096` — `state/p9_base_validation_h100_2026_05_04/verdict.json` CLM v4 base validation FAIL (orthogonal to this spec).
- **Predecessor**: `state/p9_path_a_llama_lora_2026_05_03/` v1 training cycle ($22.18 actual; step-8k anchor due to final-save flush failure).
- **Sister BGs in flight (not touched)**: BG-Χ `state/p9_path_a_step10k_recovery_2026_05_04/`; BG-Ψ `state/p9_lora_mode1_instruct_eval_2026_05_04/`.

---

## Honest C3 (top 3 from spec §9)

1. **Rehearsal mix may dilute anima-axis signal** — 60% anima vs v1 100% means each anima gradient step covers 0.6x as many tokens. F-PA-RETRAIN-v2-4 guards but does not bound the dilution. v2-PARTIAL is a real possibility.
2. **External r=16 retrain (S4) is competing track** — if `11331fe4` r=16 retrain produces V2 PASS first, this S1+S3 spec MAY be SUPERSEDED. User policy decision needed: parallel run for comparison? sequential after S4? cancel?
3. **BG-Ψ Instruct-base eval (parallel) confounds the Δ attribution** — if BG-Ψ shows much of the v1 −9.4pp TriviaQA Δ was template-mismatch (not forgetting), §4 thresholds may need re-anchoring against Instruct base before v2 EXEC.

(Full 8 honest C3 in spec §9.)

---

## Deliverables this BG

| Path | Type | Purpose |
| --- | --- | --- |
| `docs/p9_path_a_retrain_v2_spec_2026_05_04.md` | spec doc | NEW; 11 sections; LOCKED §4 + §6 + §8 |
| `docs/p9_path_a_retrain_v2_spec_landed_2026_05_04.ai.md` | handoff doc | THIS file |
| `state/markers/p9_path_a_retrain_v2_spec_landed.marker` | marker | sentinel `__P9_PATH_A_RETRAIN_V2_SPEC__ LANDED` |
| `state/p9_path_a_retrain_v2_spec_2026_05_04/decision_matrix.json` | structured | S1-S6 decision matrix machine-readable |
| `state/p9_path_a_retrain_v2_spec_2026_05_04/falsifier_set.md` | structured | F-PA-RETRAIN-v2-1~4 |
| `state/p9_path_a_retrain_v2_spec_2026_05_04/sft_corpus_mix.json` | structured | 60/30/10 breakdown machine-readable |

---

## USER ACK required for EXEC (next cycle)

- [ ] OK to spend $20-30 H100 on Path A retrain v2 with S1+S3?
- [ ] Policy on competing S4 (external r=16): RUN BOTH for comparison / SEQUENCE after S4 result / CANCEL S4
- [ ] Wait for BG-Ψ Instruct-base eval result before v2 EXEC? (yes/no — affects §4 anchor re-pre-registration)
- [ ] OK to hold §4 thresholds as LOCKED (parity-floor + ≥1 improvement)?

Upon ACK, separate BG cycle will:
1. Emit retrain orchestrator hexa (raw#9 — no new .py)
2. Build rehearsal-mix corpus shards (60% anima sub-sample + 30% MMLU/TriviaQA/Wikipedia + 10% OpenOrca/ShareGPT)
3. Launch H100 SXM pod with §6 hyperparameters
4. Run intermediate evals at step 2000/4000/6000 (HellaSwag-200)
5. Final Mode 1 eval (~$1.10) + holdout BLEU eval (~$1)
6. Emit verdict.json + landing doc + marker

---

## raw compliance

- raw#9 strict: NO new .py file (spec doc only)
- raw#10: 8 honest C3 in spec §9
- raw#15: repo-relative paths
- raw#71: F-PA-RETRAIN-v2-1~4 falsifier-bound; §4 thresholds LOCKED
- DO NOT chflags
- DO NOT execute any pod ($0)
- DO NOT modify any code or training script
- NO git operations (this BG produces files only; user commits separately)
