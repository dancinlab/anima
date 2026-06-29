# H_1630 — Tropical (max-plus) semiring binding mouth: G1/G6 screen

**date:** 2026-06-29  
**pod:** vast.ai pod 43053819 ($0.44/h, @clm303-noverfit-retrain)  
**scope:** DIRECTIONAL (py 2-production engine, engine-native-py G0-G6)  
**wired:** binder DROPPED at serialize — .clm uses additive readout  

⚠️ **Critical design note:** all `.clm` files use additive readout. Tropical max-plus binding operator is trained but dropped at serialization. Eval measures trunk representation improvement from tropical co-training, not runtime binding.

---

## Design

**ARM `soft`:** soft tropical semiring (temperature T=some > 0, log-sum-exp), binder dropped at .clm  
**ARM `mid`:** mid-temperature tropical (between soft and hard), binder dropped  
**ARM `arm`:** standard CLMConvMoE additive readout (control)

4000 steps, d=3784 L=4, 4-register clean corpus, savant golden-zone, mitosis E2→E3 @ step 2000, seeds {7, 4302, 4303}

---

## Training results (4/4 DESCENT all arms)

| arm | seed | val_CE | 4/4? | lossF | bind_ce | wall_s |
|-----|------|--------|------|-------|---------|--------|
| soft | 7 | 0.932 | YES | 1.179 | 1.162 | 3474s |
| soft | 4302 | 0.914 | YES | 1.168 | 1.152 | 3460s |
| soft | 4303 | 0.953 | YES | 1.164 | 1.143 | 3468s |
| mid | 7 | 0.932 | YES | 1.191 | 1.193 | 3475s |
| mid | 4302 | 0.915 | YES | 1.153 | 1.155 | 3467s |
| mid | 4303 | 0.924 | YES | 1.173 | 1.172 | 3471s |
| arm | 7 | 0.922 | YES | 1.163 | 1.176 | 3476s |
| arm | 4302 | 0.905 | YES | 1.148 | 1.162 | 3477s |
| arm | 4303 | 0.901 | YES | 1.159 | 1.179 | 3472s |

---

## G0-G6 engine-native-py results (pending)

| arm | seed | G0 n/5 | G0? | G1 best_distinct | G1 max_single | G6 dist | G6 fals | a7b? |
|-----|------|--------|-----|-----------------|---------------|---------|---------|------|
| soft | 7 | — | — | — | — | — | — | — |
| soft | 4302 | — | — | — | — | — | — | — |
| soft | 4303 | — | — | — | — | — | — | — |
| mid | 7 | — | — | — | — | — | — | — |
| mid | 4302 | — | — | — | — | — | — | — |
| mid | 4303 | — | — | — | — | — | — | — |
| arm | 7 | — | — | — | — | — | — | — |
| arm | 4302 | — | — | — | — | — | — | — |
| arm | 4303 | — | — | — | — | — | — | — |

---

## Verdict

**EVAL-PENDING** — 9 evaluate.py processes running on pod 43053819.

Expected: G1=0 all arms (binder dropped; same limitation as EXP-3). Test is whether tropical max-plus training signal improves trunk G1 via representation effects.

---

## Artifacts

- `trainer.py` — tropical semiring BindCLM trainer (soft/mid/arm)
- `PREREG.md` — frozen specification
- `ckpt/` — .clm + .pt + .json + .g0g6.txt
