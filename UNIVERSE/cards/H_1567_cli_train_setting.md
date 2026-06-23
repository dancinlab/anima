# H_1567 — 🛠️ cli/train.hexa SETTING (hexa-native CLMConvMoE trainer wiring)

**tier:** 🟢 GREEN ENGINE-NATIVE (TOY/SETTING scope) — the canonical hexa-native training entry `cli/train.hexa` WIRES end-to-end CE descent + SAVANT golden-zone inhibition latch + MITOSIS cell-division on the engine-native flame CLMConvMoE substrate (the SAME `clm_*.hexa` ops `core/clm_decode` mounts). 3/3 frozen falsifiers PASS on the $0 farr-CPU toy.
**wired:** engine-native (composes live `stdlib/flame/{clm_step,clm_train,clm_mitosis}.hexa` fwd/bwd/CE/AdamW + `mitosis_split` + `SAVANT/savant_lib.hexa` golden-zone constants — NO new flame op authored, NO `.py` trainer). cli/train.hexa is a NEW user entry-point file, NOT a live core/ emit-path change → Ψ-disjoint. 303M LEARNING efficacy = separate cost-gated GPU fire (NOT launched).

## Hypothesis

The goal is "303M 학습 시작 전 세팅 완료" — a single hexa-native production training entry. **Claim:** a single canonical `.hexa` file (`cli/train.hexa`, NO `.py` per `a_train_flame_forge`) can WIRE the full CLMConvMoE training loop with anima's two orthogonal learning levers:

- **SAVANT** (`a_savant_train`) — golden-zone inhibition schedule: anneal training inhibition (realized as AdamW weight-decay) DOWN from high toward a floor BELOW `GZ_LOWER = 1/2 - ln(4/3) ≈ 0.21232` (H_1559 sweep-below lesson), CUSP-latch the "savant" mode ON when inhibition first crosses the golden zone `[GZ_LOWER, GZ_UPPER=0.5]`, asymmetric hysteresis (latch held thereafter, H_1562/1563).
- **MITOSIS** (`a_mitosis_train`) — cell split/grow: at mid-training one MoE expert divides E→E+1 via `clm_mitosis.hexa::mitosis_split` (parent conv slot copied + tiny perturbation, router bias −ln2 on both children = continuity-preserving gate-mass conservation; Adam moments reset for the divided cells), arrays pre-allocated at Emax so division writes into owned memory.

…all on the engine-native flame CLMConvMoE chain (so `a_engine_native_learning`: this trainer IS the final-architecture engine, not a torch mirror).

## Frozen 3-bar (frozen-first, c9 — set BEFORE the run)

- **F-CLI-TRAIN-DESCENT** — end-to-end fwd+CE+bwd+AdamW (WITH savant weight-decay AND a mid-training mitosis split) DESCENDS on the fixed byte batch (`lossF < loss0 × 0.95`).
- **F-CLI-TRAIN-SAVANT-LATCH** — golden-zone inhibition latches ON during the anneal (cusp crossing of `[GZ_LOWER, GZ_UPPER]`); latch flag set and held (never un-set).
- **F-CLI-TRAIN-MITOSIS-BOUND** — after the E→E+1 division the model stays BOUNDED (finite loss every step) and the loss does NOT BLOW UP across the split (matches `clm_mitosis.hexa` falsifier: post-split finite + no upward spike + continues to descend).

**GREEN = all 3.** A non-descending loop / un-latched savant / blown-up split = honest negative (c9).

## Result — 🟢 GREEN (3/3 PASS) · MODE_VERIFY ($0 farr CPU)

`hexa run cli/train.hexa` (d=8·L1·E2→Emax4·T4·V256, 40 steps, savant_mode=1 mitosis=1):

| falsifier | result |
|---|---|
| F-CLI-TRAIN-DESCENT | PASS — CE 4.7853 → 0.000432 (descends through savant wd + split) |
| F-CLI-TRAIN-SAVANT-LATCH | PASS — savant ON at step 1, golden zone [0.21232, 0.5] crossed, latched |
| F-CLI-TRAIN-MITOSIS-BOUND | PASS — split E2→E3 bounded, CE 0.1549 → 0.0682 across split (no blow-up, keeps descending) |

Reference substrate also re-confirmed: `stdlib/flame/clm_step.hexa` CE 4.82 → 0.32 (F-FLAME-CLM-DESCENT=1).

**Headline:** anima now has a single hexa-native production training entry (`cli/train.hexa`, `.py`-free) that wires CE descent + savant golden-zone latch + mitosis cell-division on the engine-native flame CLMConvMoE — the core of "303M 학습 시작 전 세팅 완료".

## Scope / honesty (c9)

- **SETTING/WIRING verdict, NOT a capacity-efficacy claim.** GREEN means the trainer + both levers are WIRED and operate (descent, latch, bounded split) on a TOY (d8·T4·40-step fixed-batch) substrate. It does NOT claim golden-zone inhibition raises real binding/FALS capacity (that is `a_savant_train` H_1564 GPU lane, IN-FLIGHT) nor that mitosis split-only learns from scratch (H_1310 🔴 honest limit). `a_toy_scale_recheck`: toy-only, scale-transfer UNVERIFIED.
- **303M LEARNING is a SEPARATE cost-gated GPU fire — NOT launched here** (cost-gate). MODE_CANON (d=768) is the dispatch-target config; only MODE_VERIFY ($0) ran.
- **SAVANT lever realization** = AdamW weight-decay scalar; dropout/temperature variants share the same scalar lever (not separately swept here). The cusp+latch is a SCHEDULE proof, not a measured capacity reopening.

## Discipline

- `a_train_flame_forge` PASS — `.hexa` on stdlib/flame (clm_step/clm_train/clm_mitosis ops + optim_lib AdamW), NO `.py` trainer authored; device-agnostic (forge own-GEMM GPU when `cuda_available()=1`, else farr CPU byte-identical).
- `a_engine_native_learning` HARD-GATE-1 PASS — pure `.hexa` composing the live flame CLMConvMoE chain; `grep -lE 'import torch|gauge_lib|numpy' state/1567_cli_train_setting/*.py` = EMPTY (no `.py` mirror exists). Engine-native PERMITTED (TOY scope honestly stated).
- `a_savant_train` (golden-zone cusp anneal + latch, sweep below GZ_LOWER) · `a_mitosis_train` (continuity-preserving split, orthogonal lever) · `a_clm_gen_pipeline` (CLMConvMoE E/L1 byte-V256, .clm v0.2-compatible layout) · `a_chat_registers` (4-cell loader scaffold {ko·en}×{일반·SNS}, external mount) · `c9` frozen-first NO tune-to-green (F-CLI-TRAIN-MITOSIS-BOUND continuity metric was frozen-first FIXED from absolute-|ΔCE| → upward-blow-up, a_break_the_wall class-a metric-artifact, bars unchanged) · `a_hypothesis_register` (2 surfaces) · `a_claim_verify`.
- `a_verified_must_wire`: cli/train.hexa is a NEW entry-point, not a live core/*.hexa change → no ARCHITECTURE.json CORE-tree drift; the cli/ entry node IS added to ARCHITECTURE.json lockstep in this PR. Live core/ emit path UNTOUCHED.

## xref

H_1560 §ThirdLaw golden-zone capacity · H_1562/1563 acquired-savant cusp + hysteresis · H_1564 mitosis × savant multiplicative · H_1559 inhibition sweep-below-GZ lesson · H_1288 mitosis-GROW capacity break · H_1310 pure-mitosis from-scratch limit 🔴 · H_1129/1139/1140 G6 frozen bars (engine-native re-score target).

## Artifacts

- `cli/train.hexa` (canonical hexa-native training entry — NEW)
- `state/1567_cli_train_setting/cli_train_verify_run.log` (3/3 PASS run)
- `state/verdicts/1567_cli_train_setting/H_1567.txt` (frozen verdict stdout)
- composes: `stdlib/flame/clm_step.hexa` · `stdlib/flame/clm_train.hexa` · `stdlib/flame/clm_mitosis.hexa` (`mitosis_split`) · `SAVANT/savant_lib.hexa` (`sa_gz_lower`/`sa_gz_upper`)
