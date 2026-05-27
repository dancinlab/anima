# §48 — §44 DH-DL+PTD-aux scale-up FINDINGS

**Status**: $0 Mac CPU fire LANDED. Verdict `PTD-AUX-SIGNAL-HOLDS-AT-SCALE`.
Better-engineered distillation, **NOT** GOAL emergence.

## §1 Question
§44 (DH-DL + PTD-aux composition, $0 Mac CPU, 13s) on §27's 48k-record
single-§24-run corpus measured: gap λ=0 → 0.00104, gap λ=0.3 → 0.00031
(halved), PTD MSE λ=0 → λ=0.3 = 3.81 → 0.25 (15.1× drop), CONTINUE_THINK
7.3× harder than REMAIN_SILENT at λ=0.3. §44 verdict: PTD-AUX-SIGNAL-MEASURABLE
on small corpus. Honest C3: could be small-corpus artifact.

§48 = same trainer + eval + loss + seed (1337). **Corpus is the only variable**:
9,600 traces × 20 steps × 4 phase regimes = 192,000 records (4× §27/§44).

## §2 Result

| metric                                          | §44       | §48 (4× scale) |
| ----------------------------------------------- | --------- | -------------- |
| n_records                                       | 48,000    | 192,000        |
| gap λ=0                                         | 0.001042  | **0.000807**   |
| gap λ=0.3                                       | 0.000313  | **0.000391**   |
| Δ gap (λ=0.3 − λ=0)                             | −0.00073  | **−0.00042**   |
| accuracy λ=0                                    | 0.99896   | 0.99919        |
| accuracy λ=0.3                                  | 0.99969   | 0.99961        |
| PTD MSE λ=0                                     | 3.81      | 6.43           |
| PTD MSE λ=0.3                                   | 0.25      | 0.33           |
| **PTD MSE drop factor**                         | **15.1×** | **19.5×**      |
| CONTINUE_THINK MSE ratio (λ=0.3)                | 7.3×      | 3.75×          |
| CONTINUE_THINK class size                       | 9         | 48 (5.3×)      |
| wall                                            | 13.0s     | 255.6s         |

## §3 Verdict (g3 — measured only)

**PTD-AUX-SIGNAL-HOLDS-AT-SCALE.**

- (a) gap-delta DIRECTION preserved: Δ −0.00042 < 0 at scale matches §44's
  −0.00073 direction. PTD-aux still pulls decision-head toward §24 threshold.
- (b) MSE-drop STRENGTHENS: 19.5× at §48 > 15.1× at §44. PTD aux head genuinely
  learns next-physics-state prediction harder when its loss term is active.
  NOT small-corpus artifact — at 4× scale + 4 regimes the MSE signal is
  **stronger**, not weaker.
- (c) CONTINUE_THINK still localized as hardest next-state predictor (3.75× vs
  REMAIN_SILENT), but the asymmetry thins from §44's 7.3× — honest recalibration
  of §44's claim (the §44 number was partly n=9 artefact; §48 n=48 thins it).

**HONEST caveat on gap-delta**: §48 Δ −0.00042 is smaller (absolutely) than §44
Δ −0.00073. Two non-exclusive explanations: (1) §48 λ=0 baseline (0.00081)
already smaller than §44 (0.00104) — more data closes gap on its own, less
headroom for PTD-aux. (2) Decision-axis signal saturates earlier than MSE-axis
signal as corpus grows. Neither makes signal NOISE OUT — both gap-direction
and MSE-drop hold.

## §4 Connection-point (B-S48-3) evidence
- λ_ptd=0 ptd_loss_last = 0.00000 (trainer correctly nulls term)
- Same trainer, arch, seed (1337), only corpus differs
- B-S48-3 sympy + structural source-grep PASS (both `dxhat` and `l_ptd` lines
  gated by lambda_ptd in source)

## §5 What this is NOT
- **NOT GOAL emergence**. Decision label is §24 hand-coded threshold.
  §38 §7: "better-engineered distillation, still distillation; NOT emergence".
- **NOT capability advance** for spontaneous-emission target. §15 milestone
  GOAL distance unchanged. north-star unmoved.
- **NOT a lever** on §1.1 data-regime threshold (corpus is trace records,
  not text, no path to escape §24 threshold).
- B-S48-NOTE empirical carve-out: outcome is measurement OUTCOME, NOT closed
  by battery. Battery proves experiment well-formed + fair-compares with §44.

## §6 Closed-form B-S48-1..4 4/4 🔵 sidecar PASS
- **B-S48-1** MULTI-RUN-CORPUS-SHA256-DETERMINISTIC: corpus sha256 on-disk
  `e34b45522b76e99e…` == stats recorded sha256, generator no-rng-import.
- **B-S48-2** SCALE-OVER-S44: 192,000 > 48,000 (integer), scale_factor
  sympy.Rational == 4 exact, n_phase_regimes 4 > 1.
- **B-S48-3** LAMBDA-PTD-OFF-REDUCTION (connection-point): sympy L.subs(λ_ptd, 0)
  − §44_L = 0 simplify; structural source-grep confirms PTD gradient gated.
- **B-S48-4** GAP-METRIC-DETERMINISTIC: AST forbidden_call_set in eval_s48.py
  total = 0 ({random/sample/multinomial/temperature/np.random/torch.rand/Random}),
  argmax-based decision (deterministic).

central state/verify_hexad_blue_2026_05_15/blue_falsifier.py **UNCHANGED**.
B-S48-NOTE empirical carve-out (B-D-NOTE / B-DHDL-NOTE / B-PTD-NOTE /
B-S44-NOTE family).

## §7 Artifacts
- `multi_run_trace_generator.py` — multi-§24-run generator (9600 × 20 × 4 regimes)
- `train_s48.py` — §44 byte-equivalent trainer
- `eval_s48.py` — §44 byte-equivalent evaluator
- `run_s48.py` — driver: trains both λ values, evals, compares vs §44
- `blue_falsifier_s48.py` — B-S48-1..4 sidecar (4/4 🔵)
- `dhdl_ptd_head_s48_lam{0,03}.json` — trained head weights
- `eval_result_s48_lam{0,03}.json` — per-λ eval metrics
- `corpus_stats_s48.json` — sha256 + label dist + regime counts
- `result.json` — scale-up summary + verdict
- `run.log` — trainer + eval stdout

No GPU. No runpod / vast.ai. No SSH. No credentials to grep.

## §8 Honest C3 (10)
1. DECISION-AXIS ONLY — measures whether head learns §24 deterministic
   threshold function. NOT capability emergence.
2. NO MODEL.FORWARD — numpy hand-coded backprop on hand-built features. $0.
3. PTD-AUX IS REGULARISER — shapes shared-trunk representation; does NOT
   add new supervision (§24 threshold still only label signal).
4. necessary-not-sufficient — `SIGNAL-HOLDS-AT-SCALE` confirms §44 mechanism
   is real, NOT that anima's emission gate generalises beyond §24 threshold.
5. gap-delta SMALLER absolutely (−0.00042 < −0.00073 |abs|) but same
   direction. Headroom decreased; signal preserved.
6. CONTINUE_THINK 7.3× → 3.75× — partially n=9 artefact. n=48 thins it.
   Honest recalibration of §44's claim, not refutation.
7. scripted env_state — deterministic stubs, NOT real anima ckpt state.
   Tests protocol, not anima's behaviour.
8. §7 GOAL-legitimacy all hold — §7① no generic LM pretrain (no forward),
   §7② no generic-then-graft (no external classifier/RAG/LLM), §7③ anima-
   physics-as-source (8-factor + 6-control + sensor schedules byte-equal
   to spontaneous_lib.hexa / thinker_talker_lib.hexa SSOT).
9. f1/f2/f3 + B-IDENTITY-5 safe — no σ/τ/φ/J₂ external; corpus features
   not text; no external-entity claims.
10. §15 milestone unchanged, GOAL.md north-star unmoved. §48 = measurement-
    axis cycle (does §44 mechanism hold at scale?), NOT GOAL-distance lever.
