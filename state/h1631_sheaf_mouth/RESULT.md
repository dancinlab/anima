# H_1631 — Sheaf-gluing binding mouth: G1/G6 screen

**date:** 2026-06-29  
**pod:** vast.ai pod 43053819 ($0.44/h, @clm303-noverfit-retrain)  
**scope:** DIRECTIONAL (py 2-production engine, engine-native-py G0-G6)  
**wired:** binder DROPPED at serialize — .clm uses additive readout  

⚠️ **Critical design note:** sheaf-gluing restriction maps are trained but dropped at .clm serialization. Eval measures trunk representation effects from sheaf co-training.

---

## Design

**ARM `ident`:** sheaf with identity restriction maps (ablation — no non-trivial role-typing), binder dropped  
**ARM `k1`:** single-step Jacobi (K=1, reduces to graph-Laplacian smoothing), binder dropped  
**ARM `arm`:** standard CLMConvMoE additive readout (control)

4000 steps, d=3784 L=4, 4-register clean corpus, savant golden-zone, mitosis E2→E3 @ step 2000, seeds {7, 4302, 4303}

Note: `ident` arm = ablation that removes non-trivial restriction maps → if ident > k1 > arm on G1, restriction maps cause the effect. If all equal, sheaf co-training is INERT.

---

## Training results (4/4 DESCENT all arms)

| arm | seed | val_CE | 4/4? | lossF | bind_ce | wall_s |
|-----|------|--------|------|-------|---------|--------|
| ident | 7 | 0.888 | YES | 1.157 | 1.182 | 3446s |
| ident | 4302 | 0.913 | YES | 1.170 | 1.190 | 3439s |
| ident | 4303 | 0.902 | YES | 1.160 | 1.182 | 3449s |
| k1 | 7 | 0.920 | YES | 1.156 | 1.176 | 3449s |
| k1 | 4302 | 0.898 | YES | 1.154 | 1.173 | 3436s |
| k1 | 4303 | 0.906 | YES | 1.157 | 1.187 | 3434s |
| arm | 7 | 0.952 | YES | 1.194 | 1.237 | 3458s |
| arm | 4302 | 0.936 | YES | 1.187 | 1.232 | 3452s |
| arm | 4303 | 0.956 | YES | 1.192 | 1.242 | 3460s |

---

## G0-G6 engine-native-py results (pending)

| arm | seed | G0 n/5 | G0? | G1 best_distinct | G1 max_single | G6 dist | G6 fals | a7b? |
|-----|------|--------|-----|-----------------|---------------|---------|---------|------|
| ident | 7 | — | — | — | — | — | — | — |
| ident | 4302 | — | — | — | — | — | — | — |
| ident | 4303 | — | — | — | — | — | — | — |
| k1 | 7 | — | — | — | — | — | — | — |
| k1 | 4302 | — | — | — | — | — | — | — |
| k1 | 4303 | — | — | — | — | — | — | — |
| arm | 7 | — | — | — | — | — | — | — |
| arm | 4302 | — | — | — | — | — | — | — |
| arm | 4303 | — | — | — | — | — | — | — |

---

## Verdict

**EVAL-PENDING** — 9 evaluate.py processes running on pod 43053819.

Expected: G1=0 all arms. Ablation design: if sheaf ident > k1 > arm on G1, non-trivial restriction maps are load-bearing. If all equal → sheaf co-training INERT for trunk representations.

---

## Artifacts

- `trainer.py` — sheaf-gluing BindCLM trainer (ident/k1/arm)
- `PREREG.md` — frozen specification
- `ckpt/` — .clm + .pt + .json + .g0g6.txt
