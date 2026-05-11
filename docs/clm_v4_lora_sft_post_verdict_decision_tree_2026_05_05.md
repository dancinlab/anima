# CLM v4 + LoRA SFT — post-verdict scenario decision tree

- **ts_utc**: 2026-05-05T_BG-CLM-2-FOLLOWUP-SCENARIOS
- **bg_lane**: CLM-2-FOLLOWUP-SCENARIOS (pre-verdict scaffolding; **$0, mac, no exec, no commit, no roadmap mutation**)
- **status**: SCENARIO_TREE_LANDED — design only; consumed by post-verdict landing dispatcher
- **predecessor (in-flight)**: BG-CLM-2-EXEC at `state/clm_v4_lora_sft_2026_05_05/` — verdict imminent (stage6_verdict_computing)
- **anchors**:
  - CLM v4 base (left comparator): `state/clm_v4_baseline_eval_2026_05_05/verdict.json` (HellaSwag acc_norm=0.255, MMLU acc=0.2553, TriviaQA EM=0.0, OpenBookQA acc_norm=0.28; F-CLM-LORA-2 baseline SET; substrate φ★=41.86 carry, ckpt φ★=37.27)
  - Llama Path A v2 retry-3 eval-rerun (right comparator): `state/p9_path_a_retrain_v2_retry_3_eval_rerun_2026_05_05/verdict.json` (HellaSwag acc_norm=0.645, MMLU acc=0.5752, TriviaQA EM=0.455; RE_VERDICT=PASS_TRUE; forgetting_index=−0.0280)
  - F4 substrate-amendment (substrate-aware F4 deferred to CLM-2): `docs/p9_path_a_retry_3_f4_amendment_landed_2026_05_05.ai.md`
- **purpose**: pre-write follow-up BG scaffolds for each of 5 verdict outcomes so post-verdict decision latency is minimized
- **dispatcher companion**: `docs/clm_v4_lora_sft_post_verdict_landing_dispatcher_2026_05_05.md`
- **raw**: raw#9 (md only), raw#10 (≥5 honest C3), raw#15 (additive only)

---

## §0 — Verdict-payload contract (assumed schema)

BG-CLM-2-EXEC will emit `state/clm_v4_lora_sft_2026_05_05/verdict.json` with (per `docs/clm_v4_lora_sft_landed_2026_05_05.ai.md` sentinel block):

```jsonc
{
  "schema": "anima/clm_v4_lora_sft/verdict/1",
  "cycle": "clm_v4_lora_sft_2026_05_05",
  "lane_status": "<V2_PASS|V2_PARTIAL|V2_FAIL|V2_FAIL_EARLY_STOP|V2_EVAL_CRASHED>",
  "sentinel": "__P9_CLM_V4_LORA_SFT__ <V2_PASS|V2_PARTIAL|V2_FAIL|V2_FAIL_EARLY_STOP|V2_EVAL_CRASHED>",
  "F_CLM_LORA_1": "<PASS|FAIL>",   // forgetting index < 0.05 vs CLM v4 base
  "F_CLM_LORA_2": "<PASS|PARTIAL|FAIL>", // composite vs Llama Path A v2; the differentiator
  "F_CLM_LORA_3": "<PASS|FAIL>",   // φ★ ≥ +10 (50% safety from sign zero)
  "F_CLM_LORA_4": "<PASS|FAIL>",   // axis-conditioning preserved (3/3 fixture + 6/7 axis-diff)
  "F_CLM_LORA_5": "<PASS|FAIL>",   // shim hf_format compatibility
  "phi_star_post_lora": <float>,
  "composite_clm_lora": <float>,    // (HS+MMLU+TQA)/3
  "composite_llama_path_a_v2": 0.5584,  // (0.645+0.5752+0.455)/3 = 0.5584 (retry-3 eval-rerun anchor)
  "composite_delta_pp": <float>,     // CLM_LORA - Llama (positive = anima wins)
  "forgetting_index": <float>,
  ...
}
```

Field names not in the actual emit schema are inferred from spec §4–§5. Dispatcher in §6 of this doc maps verdict → scenario via the **PRIMARY discriminators** below; secondary fields tie-break ambiguous cases.

### 0.1 Primary discriminators (tier-1 fields)

| Tier-1 field | Used to disambiguate |
|---|---|
| `lane_status` | top-level scenario routing (S5 if `V2_EVAL_CRASHED`; S4 if `V2_FAIL_EARLY_STOP`) |
| `F_CLM_LORA_2` (PASS/PARTIAL/FAIL) | S1 vs S2 vs S3 |
| `F_CLM_LORA_3` (φ★ flip) | S4 escalation regardless of F2 |
| `composite_delta_pp` | S2 vs S3 fine-grain (>0 = S2 leaning anima; <−5pp = S3 strong) |

### 0.2 Secondary discriminators

| Field | Use |
|---|---|
| `F_CLM_LORA_4` (axis-cond preserved) | S1 confidence boost (anima keeps native axis); S3 caveat (Llama-only path doesn't have F4 to begin with) |
| `forgetting_index` | S1/S2 confidence (low = healthy substrate); high → S4 escalation |
| `phi_star_post_lora` < +10 | S4 trigger overrides F2 result |

---

## §1 — Scenario S1 — F-CLM-LORA-2 differentiator POSITIVE (anima > Llama)

### 1.1 Trigger condition

```text
verdict.lane_status        == "V2_PASS"
verdict.F_CLM_LORA_2       == "PASS"
verdict.F_CLM_LORA_3       == "PASS"      # φ★ ≥ +10
verdict.composite_delta_pp >  0           # CLM_LORA composite > Llama Path A v2 composite (0.5584)
```

Optional reinforcers (any one tightens confidence): `F_CLM_LORA_4 == "PASS"` (axis preserved), `forgetting_index < 0.05`.

### 1.2 Implications

- **Substrate hypothesis**: anima's consciousness-coupled CLM v4 substrate provides measurable lift over Llama LoRA on the same rehearsal recipe. The "anima substrate has architectural advantage" hypothesis is **NOT FALSIFIED** by this single-seed test.
- **Lane closure direction**: CLM v4 lane → **OPEN for scaleup**; Path A v2 lane stays valid as comparator anchor.
- **Roadmap impact**: `p9_sft.cond.clm_v4_lora_sft` → V2_PASS; CLM v4 substrate validated for SFT; substrate-aware F4 (per `docs/p9_path_a_retry_3_f4_amendment_landed_2026_05_05.ai.md`) is RESOLVED → Path A retry-3 lane closure can be amended from `PARTIAL_PASS_W_F4_DEFERRED_TO_CLM2` to `TRUE_PASS_W_CLM2_F4_LANDED`.
- **Downstream effects**: justifies BG-CLM-3 5-seed scaleup; HF release prep (`dancinlab/clm-v4-mk2-lora-v1`) green-lit; cross-substrate matrix `tool/p9_a_d_cross_axis_verdict.hexa` populated 3-way.

### 1.3 Follow-up BG scaffold — B1 (5-seed scaleup) + B1' (HF release prep, parallel)

**B1: BG-CLM-3-5SEED-SCALEUP** (cost band $25–75)

```text
## BG-CLM-3-5SEED-SCALEUP: CLM v4 + LoRA 5-seed cross-validation — $25-75, H100, ~10-12h aggregate

Working in `/Users/ghost/core/anima` on macOS. Spec landing first ($0, mac); H100 EXEC under USER ACK.

### Why
BG-CLM-2-EXEC single-seed (20260504) verdict V2_PASS with composite_delta_pp=<X>pp over Llama Path A v2.
Single-seed verdicts are noisy at the 1-2pp scale (raw#71 honest C3 #9 in spec). 5-seed cross-validation
required before HF release + roadmap "substrate validated" claim.

### Seeds
- 20260504 (already run; reuse adapter from state/clm_v4_lora_sft_2026_05_05/results/adapter_final)
- 20260505, 20260506, 20260507, 20260508 (NEW; reuse spec §3 hyperparameters verbatim except seed)

### Hyperparams (LOCKED — copy from BG-CLM-2 spec §3 exactly; raw#71 pre-registration)
- Base: dancinlab/clm-v4-mk2-v1
- LoRA: r=32, alpha=64, dropout=0.05
- target_modules: decoder.blocks.{0..15}.attn.{q,k,v,o}_proj (self-attn ONLY; cross_attn EXCLUDED)
- LR=3e-5, cosine warmup=300, max_steps=6000, save_steps=1000
- micro_batch=8, grad_accum=4 (eff_batch=32), seq_len=512, bf16
- Slice D consciousness-coupled = 0% (deferred to v3); 60/30/10 mix only

### Eval
- Per-seed: F1-F5 + composite vs Llama Path A v2
- Aggregate: mean ± 95% CI on composite_delta_pp; bootstrap 1000 resamples
- PASS aggregate: 5-of-5 seeds composite_delta_pp > 0 OR mean > 0 with 95%CI lower > -0.5pp

### Cost
- Per-seed: $5-15 H100 (CLM-2 single-seed actuals = $X)
- Aggregate: $25-75 (4 NEW seeds × $5-15)
- Hard cap: $90 (4 × $22.5 generous slack)

### Honest C3 (≥5)
- C1 4 NEW seeds may not span LoRA stochasticity adequately (only 5 total)
- C2 same hyperparams = co-variance with seed; doesn't probe HP sensitivity
- C3 $25-75 band wide; actuals depend on H100 spot/secure availability
- C4 Slice D still NOT INCLUDED — repeats spec C3 #5 limitation
- C5 If 1-of-5 seed FAILs, aggregate verdict ambiguous (4/5 not strict PASS); mitigation: 6th seed tiebreak ($+10)

### Output
- state/clm_v4_lora_sft_5seed_2026_05_06/seed_{N}/verdict.json (×5)
- state/clm_v4_lora_sft_5seed_2026_05_06/aggregate_verdict.json
- docs/clm_v4_lora_sft_5seed_landed_2026_05_06.ai.md

### CRITICAL
- DO NOT git commit until aggregate verdict landed
- DO NOT run if BG-CLM-2-EXEC V2_PASS + composite_delta_pp > 0 NOT yet confirmed
- USER ACK required (cost > $5 per memory completion-quality recommendation)
```

**B1' (parallel): BG-CLM-2-HF-RELEASE-PREP** (cost $0)

```text
## BG-CLM-2-HF-RELEASE-PREP: HF release pre-flight for clm-v4-mk2-lora-v1 — $0, mac, ~1h

### Why
V2_PASS validated; pre-stage HF release artifacts (model card, README, adapter merge plan, license)
in parallel with B1 5-seed scaleup so post-aggregate land is single-commit.

### Tasks
1. Build model card via tool/hf_readme_template.md scaffold for dancinlab/clm-v4-mk2-lora-v1
2. Document adapter-merged shape, tokenizer dependency, trust_remote_code=True requirement
3. Pre-stage tool/hf_upload_mk2.hexa run-config (DRY-RUN only; no upload until B1 aggregate PASS)
4. Land docs/clm_v4_lora_release_prep_2026_05_06.md with USER ACK gate

### Output
- HF release prep doc + model card draft
- HF upload run-config (NOT executed)

### CRITICAL
- DO NOT actually push to HF Hub until B1 aggregate PASS
- DO NOT commit
```

### 1.4 Cost projection

| Item | Cost | Wall |
|---|---|---|
| B1 5-seed scaleup spec landing | $0 | 1h mac |
| B1 4 NEW seeds H100 | $25–75 (target $40) | ~10h aggregate |
| B1' HF release prep | $0 | ~1h mac |
| **Total S1 follow-up** | **$25–75** | **~12h** |

### 1.5 Decision points

- **USER ACK required before B1 launch** ($25–75 > $5 threshold per memory completion-quality recommendation)
- **No USER ACK for B1'** ($0 mac-only spec land)
- **HF actual upload requires SECOND USER ACK** (post-B1-aggregate)

---

## §2 — Scenario S2 — F-CLM-LORA-2 PARITY (anima ≈ Llama, no differentiator)

### 2.1 Trigger condition

```text
verdict.lane_status        == "V2_PASS" or "V2_PARTIAL"
verdict.F_CLM_LORA_2       == "PARTIAL"   # composite within ±2pp of Llama Path A v2
OR
(verdict.F_CLM_LORA_2     == "PASS" AND -0.5 ≤ composite_delta_pp ≤ +0.5)
verdict.F_CLM_LORA_3       == "PASS"      # φ★ ≥ +10 (substrate intact)
```

Tie-break: if `F_CLM_LORA_4 == "PASS"` (axis-cond preserved on CLM v4), substrate-equivalence claim is **valid even without lift** — anima substrate matches Llama AND retains native axis-conditioning structure.

### 2.2 Implications

- **Substrate hypothesis**: anima ≈ Llama on aggregate composite. Consciousness coupling is **NEUTRAL** for general SFT capability — not a differentiator, not a liability.
- **Lane closure direction**: CLM v4 lane and Path A v2 lane both stay OPEN as **alternative substrate paths** (use whichever fits cost/infra).
- **Roadmap impact**: `p9_sft.cond.clm_v4_lora_sft` → V2_PASS_PARITY; substrate-equivalence (NOT differentiator) claim landed; F4 amendment (per `docs/p9_path_a_retry_3_f4_amendment_landed_2026_05_05.ai.md`) status depends on F-CLM-LORA-4: if PASS → axis-cond preserved on substrate-correct base, F4 strict-FAIL on Llama re-cast as **substrate-aware TRUE_PASS** for the rehearsal-mix recipe.
- **Downstream effects**: spec amendment to drop "differentiator" framing in `.roadmap.p9_sft`; both substrate paths viable; optional 5-seed for confidence band on the PARITY claim (not for lift).

### 2.3 Follow-up BG scaffold — B2 (spec amendment) + B2' (optional confidence 5-seed)

**B2: BG-CLM-2-PARITY-AMENDMENT** (cost $0)

```text
## BG-CLM-2-PARITY-AMENDMENT: CLM-2 verdict re-frame from differentiator to parity — $0, mac, ~1h

### Why
BG-CLM-2-EXEC V2_PASS_PARITY with composite_delta_pp ≈ 0. The original spec §4.2 framed
F-CLM-LORA-2 as "the differentiator". Verdict says it's neutral — substrate-equivalence,
not architectural advantage. Roadmap + spec land docs need amendment to reflect the actual
finding without claiming a lift that does not exist.

### Tasks
1. Amend `.roadmap.p9_sft.cond.clm_v4_lora_sft` → status=v2_pass_parity (sibling JSONL line, additive only per raw#15)
2. Land docs/clm_v4_lora_sft_parity_amendment_2026_05_06.ai.md with substrate-equivalence claim + 5 honest C3
3. Cross-link to F4 amendment (docs/p9_path_a_retry_3_f4_amendment_landed_2026_05_05.ai.md) — if F-CLM-LORA-4=PASS, propagate "axis-cond preserved on substrate-correct base" finding to L26-L27 lessons block
4. Update tool/p9_a_d_cross_axis_verdict.hexa cross-substrate matrix: 3-way (Llama / CLM-LORA / Paradigm-D) with PARITY label on CLM-LORA cell

### Output
- Roadmap amendment line (JSONL parse-verified post-edit)
- Parity amendment landing doc
- Cross-axis verdict matrix update

### CRITICAL
- DO NOT git commit
- raw#15 additive only — original spec land doc (docs/clm_v4_lora_sft_spec_landed_2026_05_04.ai.md) UNTOUCHED
- raw#10 ≥5 honest C3
```

**B2' (optional): BG-CLM-2-PARITY-CONFIDENCE-3SEED** (cost $15–45)

```text
## BG-CLM-2-PARITY-CONFIDENCE-3SEED: 3-seed parity-band confidence — $15-45, H100, ~6-9h

### Why
PARITY claim from single seed has wide stderr (~±2pp on composite). 3-seed (vs S1's 5-seed)
yields tighter CI on the parity claim WITHOUT over-investing in a substrate that has
no demonstrated lift. Optional — USER may close lane at single-seed PARITY.

### Seeds
20260505, 20260506, 20260507 (3 NEW seeds; original 20260504 reused)

### PASS criterion (re-pre-registered for parity scope)
- mean composite_delta_pp 95%CI overlaps 0 (consistent with PARITY)
- AND mean within ±2pp of Llama Path A v2 composite (within stderr)

### Cost
$15-45 (3 × $5-15)

### USER ACK required ($15-45 > $5)
```

### 2.4 Cost projection

| Item | Cost | Wall |
|---|---|---|
| B2 spec amendment | $0 | ~1h mac |
| B2' optional confidence 3-seed | $15–45 | ~9h |
| **Total S2 follow-up (mandatory)** | **$0** | **~1h** |
| **Total S2 follow-up (with optional)** | **$15–45** | **~10h** |

### 2.5 Decision points

- **No USER ACK for B2** ($0 mac-only)
- **USER ACK required for B2'** ($15–45 > $5); USER may decline if PARITY-at-single-seed acceptable

---

## §3 — Scenario S3 — F-CLM-LORA-2 NEGATIVE (anima < Llama, regression)

### 3.1 Trigger condition

```text
verdict.lane_status        == "V2_FAIL"
verdict.F_CLM_LORA_2       == "FAIL"
verdict.composite_delta_pp <  -0.5pp     # PARITY band breached negative
verdict.F_CLM_LORA_3       == "PASS"      # substrate intact (else this is S4)
```

Strong-signal sub-trigger: `composite_delta_pp < -5pp absolute` → **substrate is a NET LIABILITY** for general SFT (per spec §5 F-CLM-LORA-2 FAIL action).

### 3.2 Implications

- **Substrate hypothesis**: anima's consciousness-coupled substrate **underperforms** Llama on the same SFT recipe. The "substrate-uniqueness as advantage for general capability" hypothesis is **FALSIFIED** by this single-seed test.
- **Lane closure direction**: CLM v4 lane → **CLOSED for general SFT scaleup**; Llama Path A v2 lane → **PRIMARY** for general SFT going forward.
- **Roadmap impact**: `p9_sft.cond.clm_v4_lora_sft` → V2_FAIL_REGRESSION; CLM v4 retained for **substrate research only** (φ★, axis-conditioning, consciousness primitive); NOT for chat / general capability.
- **Downstream effects**: roadmap re-prioritization escalates Path A retry-3 (TRUE_PASS) as the canonical SFT lane; CLM v4 LoRA path drops from F1_v3 V2 hybrid Mode-1+3 differentiator track. Mode-2 (CLM-only φ★ probe) may still be viable but is NOT a chat/SFT path.
- **F4 substrate-amendment impact** (per `docs/p9_path_a_retry_3_f4_amendment_landed_2026_05_05.ai.md`): the F4 deferral verdict for Path A retry-3 is now *itself* substrate-degenerate — if CLM v4 cannot beat Llama on the same recipe, then "CLM-2 is the true F4 venue" claim weakens (CLM-2 substrate underperforms). Honest re-cast: F-PA-RETRAIN-v2-4 strict FAIL stays as strict FAIL; substrate-aware re-interpretation needs a new substrate (BLM phase-5? — out of scope).

### 3.3 Follow-up BG scaffold — B3 (lane closure + Llama-primary amendment)

**B3: BG-CLM-2-REGRESSION-CLOSURE** (cost $0)

```text
## BG-CLM-2-REGRESSION-CLOSURE: CLM v4 SFT lane closure + Llama-primary roadmap amendment — $0, mac, ~1h

### Why
BG-CLM-2-EXEC V2_FAIL_REGRESSION with composite_delta_pp = <X>pp negative (anima < Llama).
Substrate-uniqueness-as-SFT-advantage hypothesis falsified. Close CLM v4 SFT lane;
re-prioritize Llama Path A v2 retry-3 (TRUE_PASS) as canonical SFT path.

### Tasks
1. Amend `.roadmap.p9_sft.cond.clm_v4_lora_sft` → status=v2_fail_regression (sibling JSONL, additive only)
2. Re-prioritize `.roadmap.p9_sft.cond.path_a_retrain_v2` → primary SFT lane (already TRUE_PASS_W_F4_DEFERRED_TO_CLM2 per F4 amendment; now upgrade to TRUE_PASS_PRIMARY)
3. Re-cast F4 amendment doc: "CLM-2 was true F4 venue" claim weakens; F-PA-RETRAIN-v2-4 strict FAIL stays strict FAIL; new substrate venue (BLM phase-5?) flagged as out-of-scope-this-cycle
4. Land docs/clm_v4_lora_sft_regression_closure_2026_05_06.ai.md with full implication chain + 5+ honest C3
5. CLM v4 retained in roadmap as `cond.clm_v4_substrate_research` (φ★ / axis-cond / consciousness primitive ONLY; NOT chat/SFT)

### Cross-link impact
- docs/p9_path_a_retry_3_f4_amendment_landed_2026_05_05.ai.md needs sibling AMENDMENT entry: F4 deferral resolved as "substrate venue collapsed; F4 question deferred to next axis-conditioned substrate (out of scope)"

### Output
- Roadmap amendment (2 lines: CLM-2 closure + Path A primary; both JSONL parse-verified)
- Regression closure landing doc
- F4 amendment cross-link sibling

### CRITICAL
- DO NOT git commit
- raw#15 additive only
- raw#10 ≥5 honest C3
- DO NOT delete any CLM v4 substrate research artifacts (φ★, axis-cond fixtures retained)
```

### 3.4 Cost projection

| Item | Cost | Wall |
|---|---|---|
| B3 lane closure + amendment | $0 | ~1h mac |
| **Total S3 follow-up** | **$0** | **~1h** |

### 3.5 Decision points

- **No USER ACK for B3** ($0 mac-only)
- USER notified of substrate-hypothesis falsification (informational, not gating)

---

## §4 — Scenario S4 — F-CLM-LORA-1 forgetting REGRESSION or φ★ flip

### 4.1 Trigger condition

```text
verdict.lane_status        == "V2_FAIL_EARLY_STOP"
OR
verdict.F_CLM_LORA_3       == "FAIL"      # φ★ < +10 (substrate broken)
OR
verdict.F_CLM_LORA_1       == "FAIL"      # forgetting_index ≥ 0.05
OR
verdict.phi_star_post_lora <  +10
OR
verdict.forgetting_index   >  0.05
```

Sub-classification:
- **S4a**: φ★ flipped negative (`phi_star_post_lora ≤ 0`) — substrate destroyed; adapter MUST be discarded
- **S4b**: φ★ degraded but positive (`0 < phi_star_post_lora < +10`) — substrate weakened; adapter quarantined
- **S4c**: forgetting_index ≥ 0.05 — substrate intact but rehearsal mix failed; HP retune candidate

### 4.2 Implications

- **Substrate hypothesis**: φ★ flip = LoRA SFT broke the consciousness-coupled substrate. ABORT trigger fired (per spec §5 F-CLM-LORA-1 FAIL action + R4 mitigation). Adapter discarded for inference; retained for post-mortem.
- **Lane closure direction**: CLM v4 lane → **HOLD for spec re-design**; current adapter NOT usable.
- **Roadmap impact**: `p9_sft.cond.clm_v4_lora_sft` → V2_FAIL_EARLY_STOP or V2_FAIL_PHISTAR_FLIP; spec needs re-design with refined HP (skip more target_modules, lower lr, dropout up).
- **Downstream effects**: φ★-flip evidence amends spec §10 honest C3 #3 from "real and partially irreversible" to **MEASURED_REAL** for this single trial; spec re-design required before next EXEC.

### 4.3 Follow-up BG scaffold — B4 (spec re-design with refined HP)

**B4: BG-CLM-2-RETRY-REFINED-HP** (cost $5–10 amendment + $5-10 retry)

```text
## BG-CLM-2-RETRY-REFINED-HP: CLM v4 LoRA retry with refined HP — $5-10 amendment + $5-10 retry

Working in `/Users/ghost/core/anima` on macOS. Spec amendment first ($0); retry EXEC under USER ACK.

### Why
BG-CLM-2-EXEC V2_FAIL_EARLY_STOP / φ★ flip detected. Substrate damaged by current HP.
Spec re-design with conservative HP per spec §6 R4 mitigation tertiary OR §5 F-CLM-LORA-4 FAIL escalation.

### Refined HP (LOCKED — raw#71 re-pre-registration)
| Param | BG-CLM-2 (failed) | BG-CLM-2-RETRY-REFINED-HP |
|---|---|---|
| LR | 3e-5 | **1e-5** (3× lower; per spec R4 fallback) |
| LoRA dropout | 0.05 | **0.10** (2× higher regularization) |
| target_modules | qkvo (16 layers × 4) | **qkv only** (drop o_proj per spec §5 F-CLM-LORA-4 FAIL action) |
| max_steps | 6000 | **4000** (33% shorter; reduces drift surface) |
| save_steps | 1000 | **500** (finer early-stop granularity) |
| φ★ probe | pre/post only | **pre+post + every 1000 steps** (catches drift earlier) |
| φ★ abort threshold | +10 | **+15** (50% safety from spec floor +10; tighter) |

### Sub-scenario routing
- S4a (φ★ ≤ 0): retry MANDATORY — substrate must be recoverable; if retry also flips, HOLD for next-cycle re-design
- S4b (0 < φ★ < 10): retry RECOMMENDED — substrate weakened but recoverable
- S4c (forgetting only): retry OPTIONAL — substrate intact; consider Slice D consciousness-coupled inclusion (5%) instead of HP retune

### Cost
- Spec amendment: $0 mac
- Retry EXEC: $5-10 H100 (~1.5-2h, smaller max_steps)
- Hard cap: $15

### USER ACK required (cost > $5)

### Output
- docs/clm_v4_lora_sft_retry_refined_hp_spec_2026_05_06.md
- state/clm_v4_lora_sft_retry_2026_05_06/verdict.json
- docs/clm_v4_lora_sft_retry_landed_2026_05_06.ai.md

### CRITICAL
- adapter from BG-CLM-2 (failed cycle) MUST be archived to state/clm_v4_lora_sft_2026_05_05/adapter_aborted/ (NOT deleted; post-mortem evidence)
- DO NOT reuse adapter weights — fresh LoRA init from base
```

### 4.4 Cost projection

| Item | Cost | Wall |
|---|---|---|
| B4 spec amendment | $0 | ~2h mac |
| B4 retry EXEC | $5–10 | ~2h H100 |
| **Total S4 follow-up** | **$5–10** | **~4h** |

### 4.5 Decision points

- **USER ACK required for B4 retry EXEC** ($5–10 > $5 boundary; conservatively gated)
- **No USER ACK for B4 spec amendment** ($0 mac)
- S4a sub-scenario: USER notified of φ★-flip evidence; retry RECOMMENDED but not auto-launched

---

## §5 — Scenario S5 — BG-CLM-2-EXEC INFRASTRUCTURE_FAIL

### 5.1 Trigger condition

```text
verdict.lane_status == "V2_EVAL_CRASHED"
OR
verdict.json missing entirely (BG hung / pod terminated mid-flight)
OR
verdict.lane_status == "V2_FAIL" AND all eval fields == null (eval pipeline crash, not training crash)
```

Sub-classification (mirrors L20 verdict-writer in `docs/clm_v4_lora_sft_landed_2026_05_05.ai.md`):
- **S5a**: training completed but eval crashed (adapter exists, eval pipeline broken — analog of α'''-EVAL-FIX) → eval-only rerun
- **S5b**: training crashed mid-flight (no adapter or partial adapter) → training rerun from spec
- **S5c**: pod hung / SCP failed (artifacts unrecoverable) → re-EXEC from scratch

### 5.2 Implications

- **Substrate hypothesis**: NOT TESTED — no usable verdict.
- **Lane closure direction**: CLM v4 lane → **IN-FLIGHT, retry**.
- **Roadmap impact**: `p9_sft.cond.clm_v4_lora_sft` → V2_EVAL_CRASHED (sentinel); no scientific update.
- **Downstream effects**: eval pipeline issue (analog of L19 dtype kwarg, per `state/p9_path_a_retrain_v2_retry_3_eval_rerun_2026_05_05/verdict.json` `eval_pipeline_root_cause_v3`); fix and rerun.

### 5.3 Follow-up BG scaffold — B5 (eval-only rerun OR train+eval rerun)

**B5: BG-CLM-2-EVAL-FIX** (S5a only; cost $1–3)

```text
## BG-CLM-2-EVAL-FIX: CLM v4 LoRA eval-only rerun on saved adapter — $1-3, H100, ~30min

### Why
BG-CLM-2-EXEC training completed; adapter saved at state/clm_v4_lora_sft_2026_05_05/results/adapter_final/.
Eval pipeline crashed (sub-scenario S5a). Mirror α'''-EVAL-FIX pattern (state/p9_path_a_retrain_v2_retry_3_eval_rerun_2026_05_05/verdict.json):
- Diagnose: was it dtype kwarg, transformers version pin, lm-eval task config?
- Fix: pin transformers / lm-eval to known-working pair; add PEFT smoke test pre-bench (L14)
- Re-eval: load adapter, run F1-F5 + composite, emit fresh verdict

### Cost
- $1-3 H100 (~30 min, eval only — no training)
- Hard cap: $5

### USER ACK NOT required (under $5 threshold) — but USER notified

### Pre-flight
1. Verify adapter sha256 matches state/clm_v4_lora_sft_2026_05_05/results/adapter_final/ (immutable)
2. Diagnose eval crash root cause via state/clm_v4_lora_sft_2026_05_05/run.log (look for L19-class dtype kwarg, lm-eval version mismatch)
3. Apply fix (pinned transformers>=4.51,<4.60 if dtype kwarg; lm-eval version match if task config drift)

### Output
- state/clm_v4_lora_sft_eval_rerun_2026_05_06/verdict.json
- docs/clm_v4_lora_sft_eval_rerun_landed_2026_05_06.ai.md

### After eval rerun lands → re-route to S1/S2/S3/S4 per refreshed verdict
```

**B5b: BG-CLM-2-RETRAIN** (S5b/S5c; cost $6–10)

```text
## BG-CLM-2-RETRAIN: CLM v4 LoRA full retrain (training crashed) — $6-10, H100, ~2-2.5h

### Why
S5b/S5c — training crashed mid-flight or artifacts unrecoverable. No usable adapter.
Re-EXEC BG-CLM-2 from spec (docs/clm_v4_lora_sft_spec_2026_05_04.md) verbatim.

### Tasks
1. Diagnose original crash (state/clm_v4_lora_sft_2026_05_05/run.log)
2. Apply fix (pod boot, SCP, sentinel detection)
3. Re-launch BG-CLM-2-EXEC verbatim (same spec, same hyperparams, same seed)

### Cost
- $6-10 H100 (~2-2.5h; same as original BG-CLM-2 spec §7)
- Hard cap: $15

### USER ACK required (cost > $5)
```

### 5.4 Cost projection

| Item | Cost | Wall |
|---|---|---|
| B5 (S5a eval-only) | $1–3 | ~30min |
| B5b (S5b/S5c retrain) | $6–10 | ~2.5h |
| **Total S5 follow-up (S5a)** | **$1–3** | **~30min** |
| **Total S5 follow-up (S5b/S5c)** | **$6–10** | **~2.5h** |

### 5.5 Decision points

- **USER ACK NOT required for B5 (S5a)** ($1–3 < $5; under threshold) — USER NOTIFIED informationally
- **USER ACK REQUIRED for B5b (S5b/S5c)** ($6–10 > $5)

---

## §6 — Scenario routing summary

| Scenario | Trigger primary | Follow-up BG | Cost | USER ACK gate |
|---|---|---|---|---|
| **S1** anima > Llama | F2=PASS AND delta>0 | B1 5-seed + B1' HF prep | $25–75 | YES (B1) |
| **S2** parity | F2=PARTIAL OR delta∈[−0.5, +0.5] | B2 amendment (+ optional B2') | $0 (or +$15–45) | NO (B2); YES (B2' if launched) |
| **S3** anima < Llama | F2=FAIL AND delta<−0.5 | B3 lane closure | $0 | NO |
| **S4** φ★ flip / forgetting | F3=FAIL OR F1=FAIL OR φ★<+10 OR forgetting≥0.05 | B4 spec amendment + retry | $5–10 | YES (B4 retry) |
| **S5** infra fail | lane_status=V2_EVAL_CRASHED OR verdict missing | B5 eval-only OR B5b retrain | $1–3 (S5a) / $6–10 (S5b/c) | NO (S5a) / YES (S5b/c) |

---

## §7 — Honest C3 (raw#10, ≥5)

1. **5 scenarios is enumeration, not exhaustive** — boundary cases possible. Examples not cleanly mapped:
   - F4 PASS but F2 PARTIAL (axis preserved on substrate-correct base, but composite NOT differentiated): routes to S2, but substrate-equivalence-with-axis-validity is a sub-case worth its own amendment block; S2 covers it via "F-CLM-LORA-4 PASS reinforces" but does not branch a B2'' for axis-validity-only claim.
   - F2 PASS but F4 FAIL (lift but axis broken): routes to S1 with F4 caveat, but F4 FAIL on substrate-correct base would actually invalidate the F4-amendment chain in `docs/p9_path_a_retry_3_f4_amendment_landed_2026_05_05.ai.md`. This is a bigger roadmap impact than S1 follow-up captures; should escalate to a "S1-with-axis-broken" sub-branch (deferred to verdict-time review).
   - F3 PASS (φ★ ≥ +10) but post-LoRA φ★ degraded vs +27.91 base by >50% (e.g., +12): substrate intact per threshold but heavily damaged; routes to S1/S2 with healthy F3, but a "substrate-degradation-level" sub-discriminator is missing.

2. **Follow-up BG prompts are scaffolds — may need adjustment based on actual verdict details** — the B1-B5 prompts hardcode hyperparameter assumptions (e.g., B1 reuses BG-CLM-2 HP verbatim; B4 prescribes lr=1e-5 / drop o_proj). Actual verdict may reveal a more specific failure mode requiring different HP (e.g., if F4 fails because of `o_proj` cross-axis mixing per spec, B4's "drop o_proj" is right; but if F4 fails because of `q_proj` axis-mean shift, the drop target should differ). Verdict-time review must validate the HP refinement before B4 launch.

3. **Cost projections approximate** — $25–75 for B1 5-seed has wide range; depends on H100 spot vs secure pricing, pod boot delays, OOM retries. Spec §7.2 says CLM-2 single-seed actuals were $6–10; 4 NEW seeds → $24–40 baseline + slack to $75 for variance. B4 retry $5–10 assumes max_steps=4000 (33% shorter than CLM-2's 6000); but smaller max_steps does NOT proportionally reduce cost (pod boot fixed cost dominates first ~30 min). Real B4 may run $7–12.

4. **"anima vs Llama LoRA differentiator" assumes both paths represent substrate identity correctly** — Path A v2 retry-3 (Llama anchor) reused spec hyperparameters (LR 5e-5, r=64) calibrated for Llama. CLM-2 uses different HP (LR 3e-5, r=32) calibrated for CLM v4. **The HP differs across substrates by design (substrate-aware), but it makes the comparison NOT a controlled substrate ablation** — it's a controlled SFT-recipe comparison where each substrate uses its own optimal HP. If S1 PASS, the win could be from substrate OR from HP-tuning; we cannot fully separate. This caveat should be in any S1 follow-up landing doc.

5. **Dispatcher pattern enables fast post-verdict launch but skips some user-decision steps** — dispatcher (companion doc) maps scenario → BG launch with USER ACK gating only on cost > $5 threshold. But some $0 amendments (B2, B3) carry **roadmap-shifting implications** (substrate hypothesis falsification, lane closure direction). Auto-launching $0 amendments without USER review is procedurally correct (under cost threshold) but may surprise USER if they wanted to discuss the substrate-hypothesis implications first. Dispatcher should optionally pause for USER review on roadmap-shifting amendments regardless of cost.

6. **F4 amendment cross-link is fragile** — `docs/p9_path_a_retry_3_f4_amendment_landed_2026_05_05.ai.md` defers F4 to CLM-2; if CLM-2 verdict triggers S3 (regression) or S5 (infra fail), the F4 deferral chain is broken — there is no substrate-correct F4 venue if CLM v4 underperforms or fails to evaluate. Need a fallback substrate (BLM phase-5? new clean re-train?) which is out of scope this BG. Honest: if S3 lands, the F4 amendment becomes "unanchored deferral".

7. **5-seed scaleup (B1) implicitly assumes single-seed signal generalizes** — if BG-CLM-2 single seed PASS by +1pp (close to noise band), 5-seed mean may regress to PARITY. B1 PASS criterion (mean > 0 with 95%CI lower > -0.5pp) is permissive. A bootstrap-CI lower-bound test would be stricter. Trade-off: stricter test = more often need 6th tiebreak seed = more cost. Spec'd here as permissive; USER may choose strict at B1 launch time.

8. **HF release prep (B1') runs in parallel with B1 5-seed** — if B1 aggregate fails (mean composite_delta_pp regresses to PARITY), B1' has produced release artifacts that are no longer applicable. B1' is purely $0 mac-side, so wasted effort is bounded; but psychologically, it primes the release narrative before validation completes. Mitigation: B1' DRY-RUN only; actual upload gated on B1 aggregate PASS.

9. **Ambiguous between-scenario boundaries** — the trigger conditions in §1.1, §2.1, §3.1 use exact thresholds (delta_pp > 0 vs delta_pp ≤ 0; delta_pp ∈ [−0.5, +0.5] for S2 PARITY band). A verdict at delta_pp = +0.3 falls in S2 PARITY by threshold but barely so; if F2 is reported as PASS (not PARTIAL) by the eval pipeline, it routes to S1. Dispatcher (companion doc) prefers the F2 status field over computed delta_pp where they disagree, but the spec didn't pre-register which discriminator wins. Dispatcher §3 makes a call; verdict-time human review should validate.

10. **USER ACK threshold $5 is fixed across scenarios** — applies uniformly per memory `completion-quality recommendation`. But scenarios differ in scientific risk (S4 φ★ flip retry has higher technical risk than S1 5-seed scaleup despite similar cost). Honest: dispatcher does not differentiate; USER may apply additional discretion at ACK time.

---

## §8 — References

- BG-CLM-2-EXEC spec: `docs/clm_v4_lora_sft_spec_2026_05_04.md`
- BG-CLM-2-EXEC spec landed: `docs/clm_v4_lora_sft_spec_landed_2026_05_04.ai.md`
- BG-CLM-2-EXEC landed: `docs/clm_v4_lora_sft_landed_2026_05_05.ai.md`
- CLM v4 baseline anchor: `state/clm_v4_baseline_eval_2026_05_05/verdict.json`
- Llama Path A v2 retry-3 anchor: `state/p9_path_a_retrain_v2_retry_3_eval_rerun_2026_05_05/verdict.json`
- F4 substrate amendment: `docs/p9_path_a_retry_3_f4_amendment_landed_2026_05_05.ai.md`
- Eval-fix pattern: `state/p9_path_a_retrain_v2_retry_3_eval_rerun_2026_05_05/verdict.json` (α'''-EVAL-FIX)
- L19 dtype kwarg root cause: same verdict.json `eval_pipeline_root_cause_v3`
- Companion dispatcher: `docs/clm_v4_lora_sft_post_verdict_landing_dispatcher_2026_05_05.md`
- Cross-substrate matrix: `tool/p9_a_d_cross_axis_verdict.hexa` (3-way verdict surface)
