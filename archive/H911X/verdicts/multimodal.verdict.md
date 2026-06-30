# H_911 CROSS-DOMAIN — 🎨 MULTIMODAL

**Question.** Does one visually-grounded concept form an amodal hub ACROSS surface forms? Test = concept(image)-major (parallel) ordering vs form(caption-slot)-major (concat) ordering, on the LEARNED-semantic axis, with within-concept token-order shuffle NULL.

## Data reachability — ✅ REAL aligned data REACHED
- Source: `yerevann/coco-karpathy` (HF datasets-server, public, no auth).
- Per image (1 visually-grounded concept), 5 REAL, independently human-authored captions = 5 aligned surface forms describing the SAME image. No synthesis — every form is a real human caption.
- **Construct-validity note (honest):** this is a byte-level TEXT harness; the image itself (non-text) cannot enter it. The 5 forms are therefore the 5 human textual descriptions of one image — a multimodal-GROUNDED paraphrase hub, not raw cross-modality (text vs pixels). This is the construct-valid version reachable by this harness, and the within-concept shuffle NULL guards against the effect being mere lexical overlap.
- Selection: scanned coco-karpathy train, kept the first **N=250** images with ≥5 distinct captions, 5 captions each.
- Corpora: `H911X/data/mm_par.txt` (concept-major), `H911X/data/mm_con.txt` (caption-slot-major). 1250 lines each (250×5).

## Harness
Reference harness VERBATIM: `stdlib/flame/clm_h911_scale.hexa` (int4-QAT CLMConvMoE learner → L2-normalized mean-pooled learned hidden; AMODAL anchor = within-concept cross-form cosine MINUS same-form cross-concept baseline; paired bootstrap CI, deterministic LCG, B=2000; within-concept shuffle NULL). Run via env `CLM_SCALE_N=250 / CLM_SCALE_PAR / CLM_SCALE_CON`. NLANG=5.

## Result
```
LEARNED-semantic paired mean = 0.0266371
LEARNED 95% CI = [0.0200786, 0.0331088]
NULL (within-concept-shuffle) paired mean = -0.0146785
NULL 95% CI = [-0.0189808, -0.0106612]
```

- LEARNED CI entirely **> 0** → `learned_pos = true`.
- NULL CI entirely **≤ 0** → `null_collapses = true` (NULL-probe PASS).

## TIER: 🟢 SIGNAL
LEARNED CI_lo > 0 AND NULL CI_lo ≤ 0. Concept(image)-major (parallel) ordering yields a positive amodal-hub advantage on the learned-semantic axis, and the effect **survives the within-concept-shuffle NULL** (NULL CI is negative → the advantage is semantic, not a presentation-order / byte-proximity artifact). Effect is small (mean ≈ 0.027) but the CI is clean and the null is properly collapsed.

Verdict rule applied: `🟢 SIGNAL — LEARNED paired CI_lo > 0 AND NULL CI_lo ≤ 0`.
