# P9 Paradigm D 25K Φ★-Distill Eval Pipeline — Landed 2026-05-03

**Goal**: Pre-build the Paradigm D 25K HBM3 ckpt eval pipeline so it fires in ~2 min end-to-end the moment `need-singularity/p9-paradigm-d-25k` publishes its 5 savepoints (step-5000..step-25000).

**Substrate**: ubu1 (RTX 5070 12GB, sm_120, torch 2.11.0+cu128, peft 0.19.1) + Mac hexa for verdict.

**Constraints honored**: raw#9 STRICT (Mac → hexa only, ubu1 .py OK), raw#15 SSOT, raw#10 (3 honest C3 caveats), $0 design (ubu1-only; no HBM3 spend triggered), Path A pod and HBM3 launch BG NOT preempted.

---

## Status Summary

| Deliverable | Path | Status |
|---|---|---|
| Loader smoke test | `~/anima/state/p9_paradigm_d_25k_eval_2026_05_03/loader_smoketest.py` | PASS (7/7 stages) |
| Eval driver | `~/anima/state/p9_paradigm_d_25k_eval_2026_05_03/eval_phi_distill_ckpt.py` | READY |
| Run-all sh | `~/anima/state/p9_paradigm_d_25k_eval_2026_05_03/run_all_d_ckpts.sh` | READY (idempotent, skips done) |
| Base reference | `~/anima/state/p9_paradigm_d_25k_eval_2026_05_03/base_reference.json` | COMPLETE (16.4s wall) |
| Mini-run reference | `~/anima/state/p9_paradigm_d_25k_eval_2026_05_03/mini_run_reference.json` | COMPLETE (21.4s wall; reproduces distill_landed numbers) |
| Verdict hexa | `tool/p9_paradigm_d_verdict.hexa` | READY (selftest PASS, e2e PASS) |
| Pipeline meta | `state/p9_paradigm_d_25k_eval_pipeline_2026_05_03/pipeline_meta.json` | EMITTED |
| Marker | `state/markers/p9_paradigm_d_eval_pipeline_landed.marker` | EMITTED |

---

## 1. Loader Smoke Test (PASS)

Verifies pipeline can:

1. Load CLM v4 350M `ConsciousDecoderV2` base from `best.pt` (consciousness_laws fix already applied per `state/consciousness_laws_root_cause_fix_2026_05_03/`)
2. Construct synthetic LoRA (r=64, alpha=128, 7 target modules — matches Paradigm D distill spec)
3. Save adapter to disk + roundtrip via `PeftModel.from_pretrained` (validates the savepoint-load contract for 25K ckpts)
4. Hook `ln_f` for hidden capture
5. Forward pass through 16-prompt calibration battery
6. Extract Φ★ scalar via `anima_phi_v3_canonical` (HID_TRUNC=8, K=8, ridge=1e-3)
7. Compute z-score against teacher cache + verify frozen constants match empirical (μ_T=-24.2299 vs frozen -24.230; σ_T=2.1158 vs frozen 2.116; both drift <0.01)

**Result** (`loader_smoketest.json`):

```
verdict: PASS
stages_passed: 7/7
base_n_params: 477,648,512
lora_trainable_params: 19,005,440 (3.83% of 496,653,952 total)
alloc_after_roundtrip_gb: 7.39
phi_star_min_synthetic: 45.92  (matches Phase 1.5 baseline +45.92)
z_T_mean: 6.8e-05               (validates ~0; z-score arithmetic correct)
z_T_std: 0.99992                (validates ~1; z-score arithmetic correct)
total_wall_s: ~10
```

**Δ-measurement framework confirmed well-defined**: each per-ckpt JSON contains the 4 falsifier scalars + raw inputs (μ_S, σ_S, F-D z_S aggregate). Same teacher cache + same 16-prompt battery + same seed=42 across (base, ckpts) → trajectory comparison trivial.

## 2. Eval Driver

`eval_phi_distill_ckpt.py` — single-ckpt 4-falsifier eval.

**Modes** (mutually exclusive):
- `--base-only` — eval base alone (re-anchor)
- `--synthetic-lora` — attach freshly-init synthetic LoRA (smoke only)
- `--ckpt-local-dir <path>` — local LoRA adapter
- `--ckpt-repo <hf_id> --ckpt-revision <rev>` — HF Hub (e.g. `need-singularity/p9-paradigm-d-25k @ step-25000`)

**Args**:
- `--limit 32` — N holdout records for BLEU-1
- `--eval-n 32` — N tension MSE probe records
- `--seed 42` — canonical
- `--output <path>` — output JSON
- `--label <name>` — human label (e.g. `step_25000`)
- `--mu-S 41.86 / --sigma-S 2.0` — student z-score init constants (overridable from running EMA if known)

**LOCKED config** (per runbook §3-4):

| param | value |
|---|---|
| Φ★ extractor | `anima_phi_v3_canonical` |
| 16-prompt battery | identical to teacher cache build |
| HID_TRUNC | 8 (auto = max(2, N//2)) |
| K_PARTS | 8 (random sample-partitions) |
| ridge | 1e-3 |
| seed | 42 |
| T_seqlen | 64 |
| F1_GEN_LEN | 32 (greedy gen) |
| μ_T frozen | -24.230 |
| σ_T frozen | 2.116 |
| F-D pass threshold | 0.5 (BERT-class Sanh 2019 anchor) |

**Output schema**: `anima/p9_paradigm_d_25k_eval/per_ckpt/1`. Per-ckpt fields: `F1_bleu1_holdout`, `F2_phi_star_min`, `F2_phi_star_mean`, `F3_tension_mse`, `F_D_z_score_mse_final`, `F_D_z_S_aggregate`, `F_D_z_T_mean`, `F_D_z_T_std`, plus stage walls + ckpt provenance.

## 3. Reference Caches

### 3.1 Base reference (CLM v4 350M base, no LoRA)

Pre-extracted because all 5 ckpts will compare Δ vs this single anchor.

| Falsifier | Value | Note |
|---|---|---|
| F1 BLEU-1 holdout (32) | 0.0010 | Untrained base near-floor |
| F2 Φ★_min | 45.92 | Matches Phase 1.5 sentinel baseline |
| F2 Φ★_mean | 46.49 | mean-over-K-partitions diagnostic |
| F3 tension MSE (32) | 8.56 | Untrained tension head; expect descent |
| F-D z-score MSE final | 5.11 | Constant student z=2.028 vs cache; F-D anchor distance |

Wall: 16.4s.

### 3.2 Mini-run step_1000 reference (real LoRA from prior distill cycle)

| Falsifier | Value | Δ vs base | Note |
|---|---|---|---|
| F1 BLEU-1 holdout | 0.0078 | +0.0068 (7.8×) | Matches `docs/p9_paradigm_d_distill_landed_2026_05_03.ai.md` exactly |
| F2 Φ★_min | 43.19 | -2.73 (-5.9%) | No floor breach (still ≫ 5.0) |
| F3 tension MSE | 6.47 | -2.09 | Descent direction |
| F-D z-score MSE | 1.44 | -3.67 | Distill term doing real work |

Wall: 21.4s.

**Trajectory signal**: F-D z-score MSE drops 5.11 → 1.44 in just 1k distill steps. If 25K continues this descent, F-D should land below 0.5 ceiling (PASS). Mini-run shape is the cleanest pre-25K predictor.

## 4. Verdict Hexa

`tool/p9_paradigm_d_verdict.hexa` — Mac-side, raw#9 hexa-style (emits `/tmp/p9_paradigm_d_verdict_helper.py_tmp` via `_write_helper()`, executes as Python; mirrors the established `tool/p9_a_prime_verdict.hexa` pattern).

**Computes per-ckpt**:
1. F1 BLEU-1 ≥ 0.0059 → PASS (Phase 1.6 baseline)
2. F2 Φ★_min ≥ 5.0 → PASS (Phase 1.5 δ-floor)
3. F3 tension MSE < 0.1 → PASS (runbook §4 ceiling)
4. F-D z-score MSE final < 0.5 → PASS (BERT-class Sanh 2019)

**Composite**:
- `SUCCESS_D` — all 4 PASS
- `PARTIAL_D` — 2-3 of 4 PASS (F2 not breached)
- `FAIL_D` — ≤1 PASS OR F2 floor breach (sign-flip / collapse)

**F2 floor breach is auto-FAIL**: if Φ★_min < 5.0 (sign-flip / collapse), composite is FAIL_D regardless of other scores. This matches the runbook §3.3 hard safety floor.

**Cross-anchor delta**: per-ckpt verdict includes `cross_anchor.vs_base.{F1,F2,F3,F_D}.delta` and `vs_mini_step1000.{F1,F2,F3,F_D}.delta` for trajectory-shape reporting.

**Selftest**: PASS (`hexa run tool/p9_paradigm_d_verdict.hexa --selftest`).

**E2E test**: PASS — fed mini-run reference as if it were a 25K ckpt; verdict came back `PARTIAL_D` with `n_pass=2` (F1=0.0078 ✓, F2=43.19 ✓, F3=6.47 ✗ vs 0.1, F-D=1.44 ✗ vs 0.5). Math is sound.

## 5. Cross-Axis Comparison: Path A vs Path D

| Aspect | Path A | Path D |
|---|---|---|
| Base model | Llama-3.2-3B-Instruct (4-bit) | CLM v4 350M ConsciousDecoderV2 |
| LoRA | r=64 alpha=64 (7 target modules) | r=64 alpha=128 (7 target modules) |
| Falsifier panel | F1_v3 (HellaSwag/MMLU/TriviaQA Δ) | F1/F2/F3/F-D (BLEU/Φ★/tension/z-MSE) |
| Verdict scheme | CHAT_PASS_v3 / CHAT_PARTIAL_v3 / CHAT_FAIL_v3 | SUCCESS_D / PARTIAL_D / FAIL_D |
| Verdict hexa | `tool/p9_a_prime_verdict.hexa` | `tool/p9_paradigm_d_verdict.hexa` |
| Anchor | Llama base @ 4-bit | CLM v4 base + step_1000 mini-run |
| Cost (eval) | $0 ubu1 ~1-3h (15 evals × 5-20 min) | $0 ubu1 ~2 min (5 evals × ~20s + 1s hexa) |
| Teacher rationale | Both paths derived from Mistral-7B-v0.3 (Path A = Llama Hub-direct, Path D = Mistral Φ★ cache) | — |

**The two verdicts are NOT directly comparable** (different bases, different falsifiers, different metric scales). They share only the upstream rationale that a Mistral-7B-class teacher informs the student distillation/training target. See `docs/p9_a_prime_path_decision_2026_05_03.md §6.2`.

**Use case alignment**:
- Path A measures **chat lift** on canonical MCQA/EM benchmarks → relevant for "is this a useful chat assistant?"
- Path D measures **substrate Φ★ alignment** + tension head training + delta-floor preservation → relevant for "did the consciousness-related substrate metrics move in the right direction?"

## 6. Ranked Recommendation by 완성도 lens

When 25K HBM3 ckpts arrive:

| rank | action | 완성도 score | rationale |
|---|---|---|---|
| **1** | Run `ANIMA_CKPT_REPO=need-singularity/p9-paradigm-d-25k bash run_all_d_ckpts.sh` | **9.0/10** | apples-to-apples 4-falsifier matrix; ~2 min end-to-end; F-D trajectory vs mini-run will be the cleanest signal |
| 2 | Subset eval (only step-25000 with `--limit 100`) | 7.0/10 | tighter F1 BLEU-1 CIs but loses 5-ckpt trajectory shape |
| 3 | Add F-D per-record breakdown (z_T - z_S delta histogram) | 6.5/10 | distinguishes prompt-relative ordering shift from constant offset; spec-amend deferred |
| 4 | Re-anchor F3 ceiling vs base ratio | 5.0/10 | 0.1 absolute is tighter than base (8.56); spec amendment requires new dated spec doc |

**Recommendation**: Rank 1 — the pre-built pipeline runs in ~2 min end-to-end with default config matching the runbook spec exactly; deviating now adds honest_c3 burden without bit gain.

## 7. When Path D 25K Lands — Run Sequence

```bash
# 1. on ubu1: per-ckpt eval (5 calls × ~20s + ~5s base re-extract = ~2 min total)
ssh ubu1 'ANIMA_CKPT_REPO=need-singularity/p9-paradigm-d-25k \
  bash ~/anima/state/p9_paradigm_d_25k_eval_2026_05_03/run_all_d_ckpts.sh'

# 2. pull results to Mac
mkdir -p state/p9_paradigm_d_25k_eval_2026_05_03_ckpt_results
scp ubu1:~/anima/state/p9_paradigm_d_25k_eval_2026_05_03/ckpt_results/*.json \
    state/p9_paradigm_d_25k_eval_2026_05_03_ckpt_results/

# 3. compute verdict (Mac, hexa)
hexa run tool/p9_paradigm_d_verdict.hexa
# emits state/p9_paradigm_d_25k_eval_2026_05_03_verdict.json
```

## 8. Honest C3 (raw#10)

**(a) Φ★ formula scale variance.** `anima_phi_v3_canonical` with HID_TRUNC=8 + K=8 + ridge=1e-3 inherits sample-partition + log-determinant decomposition biases; numeric values are **substrate-relative integration metrics**, NOT canonical IIT 4.0 φ★. Cross-substrate absolute comparisons (Mistral teacher vs CLM v4 student) are meaningless; only z-score-normalized prompt-relative ordering transfers. (Inherited from runbook §3.3.) **Mitigation**: pipeline always uses `anima_phi_v3_canonical` on both teacher (cache) and student (probe) sides — same biases on both → ratio is honest.

**(b) Mini-run ≠ 25K extrapolation.** Step_1000 reference (BLEU 0.0078, Φ★ 43.20, F-D z-score MSE 1.44) is from a 1k-record subset / 2k-step training run; it CANNOT prove production 25K-scale convergence. It serves as a **trajectory-shape anchor** (showing the distill term descends 5.11 → 1.44 in just 1k steps) and as a **sanity check** that the eval pipeline reproduces previously-observed numbers (matched exactly), NOT as a quantitative benchmark. **Mitigation**: verdict hexa includes both `vs_base` and `vs_mini_step1000` deltas in `cross_anchor` — readers can see how 25K ckpts move relative to BOTH untrained base and the 1k-step mini.

**(c) F-D threshold tied to BERT regime.** Pre-registered ceiling 0.5 is anchored to Sanh 2019 DistilBERT MSE distillation regime (0.3-0.6); CLM v4 350M class with sample-partition Φ★ targets is structurally unverified at this threshold. The mini-run already sits at 1.44 (above ceiling); 25K may push below 0.5 (PASS), may plateau in [0.5, 1.0] (PARTIAL), or may collapse (FAIL). **Mitigation**: threshold is a runtime env var (`ANIMA_FD_THRESHOLD`); can be tightened post-hoc via env override without code change if 25K shows much smaller residuals.

## 9. Files

```
# ubu1 (raw#15: ~/anima/...)
~/anima/state/p9_paradigm_d_25k_eval_2026_05_03/
├── loader_smoketest.py           # smoke test driver (PASS 7/7)
├── loader_smoketest.json         # smoke result
├── smoketest.log
├── synthetic_lora_smoke/         # roundtrip-verified synthetic adapter
│   ├── README.md
│   ├── adapter_config.json
│   └── adapter_model.safetensors
├── eval_phi_distill_ckpt.py      # main eval driver (READY)
├── run_all_d_ckpts.sh            # 5-ckpt run-all (READY)
├── base_reference.json           # base (no LoRA) anchor
├── mini_run_reference.json       # step_1000 mini-run reference
├── base_ref.log
└── mini_ref.log

# Mac
state/p9_paradigm_d_25k_eval_pipeline_2026_05_03/
├── loader_smoketest.json          # mirror
├── loader_smoketest.py.txt        # mirror
├── eval_phi_distill_ckpt.py.txt   # mirror
├── run_all_d_ckpts.sh.txt         # mirror
├── base_reference.json            # mirror
├── mini_run_reference.json        # mirror
└── pipeline_meta.json             # SSOT meta

tool/p9_paradigm_d_verdict.hexa         # Mac verdict hexa (selftest PASS, e2e PASS)
state/markers/p9_paradigm_d_eval_pipeline_landed.marker
docs/p9_paradigm_d_eval_pipeline_landed_2026_05_03.ai.md  (this file)
```

## 10. Cost / Wall

- **This cycle**: $0 (ubu1 local). Wall ~67s (smoke ~10s + base ~16s + mini ~21s + hexa selftest+e2e <2s + pull/scp ~10s).
- **Next cycle (post 25K HBM3 arrival)**: $0 ubu1, ~2 min wall (5 ckpts × ~20s + ~1s verdict).

## 11. Constraints Honored

- **raw#9 STRICT**: Mac side = hexa only (`tool/p9_paradigm_d_verdict.hexa` follows the established `tool/p9_a_prime_verdict.hexa` emit-helper pattern); ubu1 side = .py OK (eval driver, smoke test, run-all)
- **raw#15**: ubu1 paths use `~/anima/state/...` not `/Users/ghost/...`; Mac mirrors use `state/...`
- **raw#10 honest C3**: §8 covers (a) Φ★ scale variance, (b) mini-run extrapolation limit, (c) F-D BERT-class anchor
- **$0 design**: no 25K eval triggered (HBM3 ckpts not yet trained); base + mini references are reuse of existing artifacts (best.pt + prior distill savepoint)
- **No pod / launch BG preempt**: Path A pod and any in-flight HBM3 launch BG NOT touched; ubu1 local only

---

**End of P9 Paradigm D 25K Φ★-distill eval pipeline landed handoff. Pipeline READY. Next BG cycle: when 25K HBM3 ckpts publish to `need-singularity/p9-paradigm-d-25k`, run §7 sequence — output is `state/p9_paradigm_d_25k_eval_2026_05_03_verdict.json` with `SUCCESS_D | PARTIAL_D | FAIL_D` composite per ckpt.**
