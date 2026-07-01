# H_1620 — Energy-settle attractor mouth (Hopfield relaxation): G1/G6 screen

**date:** 2026-06-29  
**pod:** vast.ai pod 43053819 ($0.44/h, @clm303-noverfit-retrain)  
**scope:** DIRECTIONAL (py 2-production engine, engine-native-py G0-G6)  
**wired:** binder DROPPED at serialize — .clm uses additive readout (see tier note below)  

⚠️ **Critical design note:** all `.clm` files use `serialize_v3` (additive readout, no binder retained). The Hopfield energy-settle operator is trained but dropped at serialization. Eval thus measures whether *co-training* with the Hopfield operator improves trunk representations for G1, NOT whether the Hopfield readout at decode time enables G1. This is same tier as EXP-3 / H_1603 (bind-trained-but-dropped).

---

## Design

**ARM `asym`:** asymmetric Hopfield settle — energy relaxation with asymmetric weights, K settle steps, bind dropped at .clm  
**ARM `k1`:** K=1 relaxation (ablation — collapses to single feedforward, no settle dynamics), binder dropped  
**ARM `arm`:** standard CLMConvMoE additive readout (control)

4000 steps, d=3784 L=4, 4-register clean corpus, savant golden-zone, mitosis E2→E3 @ step 2000, seeds {7, 4302, 4303}

---

## Training results (4/4 DESCENT all arms)

| arm | seed | val_CE | 4/4? | lossF | bind_ce | wall_s |
|-----|------|--------|------|-------|---------|--------|
| asym | 7 | 0.984 | YES | 1.208 | 1.263 | 3436s |
| asym | 4302 | 1.001 | YES | 1.217 | 1.274 | 3435s |
| asym | 4303 | 1.007 | YES | 1.218 | 1.269 | 3430s |
| k1 | 7 | 0.920 | YES | 1.166 | 1.201 | 3440s |
| k1 | 4302 | 0.916 | YES | 1.164 | 1.201 | 3436s |
| k1 | 4303 | 0.930 | YES | 1.176 | 1.216 | 3431s |
| arm | 7 | 0.981 | YES | 1.223 | 1.275 | 3442s |
| arm | 4302 | 1.000 | YES | 1.236 | 1.297 | 3444s |
| arm | 4303 | 1.006 | YES | 1.233 | 1.285 | 3431s |

Note: val_CE << 1 nit = small-corpus overfit (4MB × 4000 steps). Descent gates PASS (val < uniform 5.545). k1 arm trains to lower CE than asym (K=1 feedforward easier to optimize than iterative settle).

---

## G0-G6 engine-native-py results

| arm | seed | G0 n/5 | G0? | G1 best_distinct | G1 max_single | G6 dist | G6 fals | a7b? |
|-----|------|--------|-----|-----------------|---------------|---------|---------|------|
| asym | 7 | 2/5 | FAIL | 0 | 0 | 4 | 0 | FAIL |
| asym | 4302 | 2/5 | FAIL | 0 | 1 | 1 | 0 | FAIL |
| asym | 4303 | 2/5 | FAIL | 0 | 0 | 1 | 0 | FAIL |
| k1 | 7 | 2/5 | FAIL | 0 | 0 | 4 | 0 | FAIL |
| k1 | 4302 | 3/5 | FAIL | 0 | 0 | 2 | 0 | FAIL |
| k1 | 4303 | 1/5 | FAIL | 1 | 0 | 4 | 0 | FAIL |
| arm | 7 | 2/5 | FAIL | 0 | 1 | 4 | 0 | FAIL |
| arm | 4302 | 3/5 | FAIL | 0 | 0 | 2 | 0 | FAIL |
| arm | 4303 | 4/5 | PASS | 0 | 0 | 4 | 0 | FAIL |
---

## Verdict

**🔴 NOT-SUPPORTED** (DIRECTIONAL — py 2-production engine, 9/9 evals)

G1=0 across all main arms while the trunk CAN cohere (>=1 arm G0 PASS) — binder dropped at .clm serialize => additive readout; co-training insufficient for recombination. Note: main binding arm additionally DEGRADES G0 coherence (G0 PASS only in control arms).

**Design scope:** binder trained but DROPPED at .clm serialize → additive readout at decode. Measures trunk representation improvement from co-training, NOT runtime binding operator. Same tier as EXP-3 / H_1603 / H_1603-series.

*See G0-G6 table above for per-arm/seed numbers.*
---

## Artifacts

- `trainer.py` — Hopfield-settle BindCLM trainer (asym/k1/arm arms)
- `PREREG.md` — frozen specification
- `ckpt/` — .clm (additive readout) + .pt + .json + .g0g6.txt (to be pulled)
