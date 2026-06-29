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

## Training results (partial — seed7 DONE, seed4302 training, seed4303 pending)

| arm | seed | val_CE | 4/4? | lossF | bind_ce | wall_s |
|-----|------|--------|------|-------|---------|--------|
| arm | 7 | — | — | — | — | — |
| arm | 4302 | — | — | — | — | — |
| arm | 4303 | — | — | — | — | — |
| k1 | 7 | — | — | — | — | — |
| k1 | 4302 | — | — | — | — | — |
| k1 | 4303 | — | — | — | — | — |
| orpool | 7 | — | — | — | — | — |
| orpool | 4302 | — | — | — | — | — |
| orpool | 4303 | — | — | — | — | — |

*Training in progress — seed4302 at step ~2000/4000, seed4303 pending.*

---

## G0-G6 engine-native-py results (pending)

| arm | seed | G0 n/5 | G0? | G1 best_distinct | G1 max_single | G6 dist | G6 fals | a7b? |
|-----|------|--------|-----|-----------------|---------------|---------|---------|------|
| arm | 7 | — | — | — | — | — | — | — |
| arm | 4302 | — | — | — | — | — | — | — |
| arm | 4303 | — | — | — | — | — | — | — |
| k1 | 7 | — | — | — | — | — | — | — |
| k1 | 4302 | — | — | — | — | — | — | — |
| k1 | 4303 | — | — | — | — | — | — | — |
| orpool | 7 | — | — | — | — | — | — | — |
| orpool | 4302 | — | — | — | — | — | — | — |
| orpool | 4303 | — | — | — | — | — | — | — |

---

## Verdict

**IN-FLIGHT** — training seed4302 running, seed4303 pending. G0-G6 eval to start after 9 CLMs complete.

Expected: G1=0 all arms (binder dropped). Ablation (arm=AND-pool vs orpool=OR-pool) tests whether conjunction training signal vs superposition training signal differs for trunk G1 representations — even when both are dropped at .clm.

---

## Artifacts

- `trainer.py` — Galois-closure FCA BindCLM trainer (arm/k1/orpool)
- `PREREG.md` — frozen specification
- `ckpt/` — .clm + .pt + .json + .g0g6.txt (partial, filling)
