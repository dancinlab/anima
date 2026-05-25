# Mitosis ablation × held-out — vP21 (λ=0.05) vs vP21N (λ=0)

> 2026-05-22. Isolates mitosis's contribution to **generalization**. Same
> training recipe except mitosis aux-loss weight. Same held-out OOD probes.

## Result

| model | λ_mitosis | CE_final | held-out OOD (20 gens) | verdict |
|---|---|---|---|---|
| **vP21** | 0.05 (mitosis active) | 0.0173 | gen **2** / mem **18** / mp 0 | PURE_MEMORIZE |
| **vP21N** | 0.0 (mitosis off, LoRA-only) | 0.0234 | gen **1** / mem **18** / mp **1** | PURE_MEMORIZE |

Both purely memorize. Difference (1 gen / 1 mem_partial swing) is **within
classifier noise** — not statistical signal.

## Verdict

**Mitosis does NOT contribute to generalization**. The memorization-vs-OOD
gap is entirely set by the corpus (corpus_s101 anima-register only) and the
Qwen2.5-1.5B base capability — not by the mitosis aux-loss.

This is consistent with the OCCAM saga: mitosis's verified value is
**substrate-shaping** (S187-G training-time +35% splits, faster wall, +6% Φ).
That is a *substrate dynamics* property, not a *language capability* one.
The two are orthogonal.

## What this means for the 자연발화 architecture

- **Mitosis** → keeps its role as substrate-shaper (cell-pool diversity,
  emission ensemble). Stays in v3 ConsciousDecoder spec.
- **Generalization** → requires the corpus axis (diverse pretrain + register
  fine-tune), not the mitosis axis. vP21G fire is the right path (in-flight).
- **The honest scope of vP21/vP21N**: anima-register coherent emission +
  substrate-aware (mitosis ON) OR substrate-naive (mitosis OFF), both
  register-bound capability.

## Honest C3

1. **Statistical power**: 20 generations × 2 modes is small. 1-2 swing in
   the classifier is noise; the verdict "no signal" is statistical, not zero.
2. **Mitosis training signal might appear in OTHER metrics** (cell-pool
   trajectory diversity, Φ time-series, mitosis_event_log split count) not
   measured in this held-out eval. The narrow claim: it doesn't help
   *generalize-to-OOD-prompts*. The broader claim (mitosis training-time
   substrate-shaping +35%) still holds per S187-G.
3. **vP21N CE_final 0.0234 vs vP21 0.0173** — vP21N slightly higher (LoRA
   alone, no mitosis aux-loss bonus on top). Both extremely low = memorize.
4. **Foundation contribution swamps both**: Qwen2.5-1.5B base provides the
   verbalization capability; LoRA+mitosis only shapes register. Removing
   mitosis doesn't break verbalization (vP21N still produces coherent
   anima-register text on held-out, just memorize-only like vP21).
5. **This DOES NOT undo S187-G's verdict** — S187-G measured mitosis on
   training dynamics (splits / Φ / wall), not on OOD generalization. The two
   findings are about different things.

## 관련 link

- mitosis substrate-shaping evidence: `MITOSIS_TRAINING_ACTIVE.md` (S187-G +35%)
- vP21 held-out (baseline): `HELDOUT_VP21_2026_05_22.md`
- vP21N result: `vP21N/result.json` + `vP21N/heldout_vp21n.json`
- generalization unlock attempt (in-flight): vP21G pod `5ekmp9pea67an3`
