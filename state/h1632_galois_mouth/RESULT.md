# H_1632 — Galois-closure concept-lattice binding mouth: G1/G6 screen

**date:** 2026-06-29  
**pod:** vast.ai pod 43053819 ($0.44/h, @clm303-noverfit-retrain)  
**scope:** DIRECTIONAL (py 2-production engine, engine-native-py G0-G6)  
**wired:** binder DROPPED at serialize — .clm uses additive readout  

⚠️ **Critical design note:** Galois-closure lattice operator is trained but dropped at .clm serialization. Eval measures trunk representation improvement from FCA meet/join co-training.

---

## Design

**ARM `arm`:** Galois-closure concept lattice (FCA meet/join, conjunctive AND-pool), binder dropped at .clm ← MAIN arm  
**ARM `k1`:** single-closure-iteration (K=1, ablation), binder dropped  
**ARM `orpool`:** OR-pool replacement (replaces AND-pool with softmax/sum = standard attention-like ablation), binder dropped

4000 steps, d=3784 L=4, 4-register clean corpus, savant golden-zone, mitosis E2→E3 @ step 2000, seeds {7, 4302, 4303}

Ablation design: if Galois arm > orpool on G1, AND-pool (conjunction) is load-bearing vs OR-pool (superposition). If equal → lattice meet doesn't improve trunk representations.

---

## Training results (COMPLETE — all 9 arms DONE)

| arm | seed | val_CE | 4/4? | lossF | bind_ce | wall_s |
|-----|------|--------|------|-------|---------|--------|
| arm | 7 | 0.916 | YES | 1.187 | 4.295 | 3428s |
| arm | 4302 | 0.917 | YES | 1.179 | 4.292 | 3446s |
| arm | 4303 | 0.934 | YES | 1.161 | 4.313 | 3199s |
| k1 | 7 | 0.982 | YES | 1.224 | 2.988 | 3437s |
| k1 | 4302 | 0.952 | YES | 1.183 | 3.045 | 3434s |
| k1 | 4303 | 0.978 | YES | 1.180 | 3.033 | 3333s |
| orpool | 7 | 0.904 | YES | 1.177 | 4.211 | 3445s |
| orpool | 4302 | 0.929 | YES | 1.170 | 4.215 | 3450s |
| orpool | 4303 | 0.893 | YES | 1.167 | 4.210 | 3316s |

*All 9 arms DONE (9/9 CLMs, 4/4 DESCENT each). G0-G6 eval RUNNING on pod 43053819.*

---

## G0-G6 engine-native-py results

| arm | seed | G0 n/5 | G0? | G1 best_distinct | G1 max_single | G6 dist | G6 fals | a7b? |
|-----|------|--------|-----|-----------------|---------------|---------|---------|------|
| arm | 7 | 4/5 | PASS | 0 | 0 | 2 | 0 | FAIL |
| arm | 4302 | 4/5 | PASS | 0 | 0 | 0 | 0 | FAIL |
| arm | 4303 | 5/5 | PASS | 0 | 0 | 5 | 0 | FAIL |
| k1 | 7 | 0/5 | FAIL | 0 | 1 | 3 | 0 | FAIL |
| k1 | 4302 | 2/5 | FAIL | 0 | 0 | 4 | 0 | FAIL |
| k1 | 4303 | 2/5 | FAIL | 0 | 0 | 6 | 0 | FAIL |
| orpool | 7 | 3/5 | FAIL | 1 | 0 | 6 | 0 | FAIL |
| orpool | 4302 | 2/5 | FAIL | 0 | 0 | 5 | 0 | FAIL |
| orpool | 4303 | 4/5 | PASS | 0 | 0 | 1 | 0 | FAIL |
---

## Verdict

**🔴 NOT-SUPPORTED** (DIRECTIONAL — py 2-production engine, 9/9 evals)

G1 floors at the bar across all main arms while the trunk CAN cohere (>=1 arm G0 PASS) — binder dropped at .clm serialize => additive readout; co-training insufficient for recombination.

**Design scope:** binder trained but DROPPED at .clm serialize → additive readout at decode. Measures trunk representation improvement from co-training, NOT runtime binding operator. Same tier as EXP-3 / H_1603 / H_1603-series.

*See G0-G6 table above for per-arm/seed numbers.*
---

## Artifacts

- `trainer.py` — Galois-closure FCA BindCLM trainer (arm/k1/orpool)
- `PREREG.md` — frozen specification
- `ckpt/` — .clm + .pt + .json + .g0g6.txt (partial, filling)
