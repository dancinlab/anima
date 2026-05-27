# anima_emerge_chat_residual_noise — landed 2026-05-05 (BG-BS)

**Status**: LANDED (FAIL_BASIN_ROBUST_DESPITE_HEURISTIC_PASS)
**Lane**: chat-emergence basin escape probe — extends BG-BJ residual-stream basin finding
**Cost**: $0 (mac CPU fp32)
**Wall**: ~226s sweep + ~19s load = ~4min total

## Summary

BG-BJ found CLM v4 mk2 emit collapses to autoregressive attractor in residual-stream
geometry — basin re-forms at step 1+ regardless of prompt. BG-BS tested whether per-step
Gaussian noise injection into residual stream at decoder block output can escape the
basin and produce semi-coherent output.

**Result**: heuristic flagged 2/18 noise configs as "coherent" but qualitative inspection
shows ALL outputs are degenerate (`/OOO...`, `hhhh...`, `PPPP...`, byte-fallback bytes
at std=5). Basin is robust to unstructured Gaussian residual noise across 3 layers
(4/8/12) × 5 stds (0.1/0.5/1.0/2.0/5.0).

## Sweep matrix (3 layer × 5 std + 3 multi-seed)

| layer | std=0.1 | std=0.5 | std=1.0 | std=2.0 | std=5.0 |
|-------|---------|---------|---------|---------|---------|
| baseline | `/OOO...` (no hook) |
| L4 | `/OOO...` | `/OOO...` | `/OOO...` | `/OOO...` | `/OO>P[[[EE...Phhh>PPhjjhjhhjjj` |
| L8 | `/OOO...` | `/OOO...` | `/OOO...` | `/OO>hhhhhh...PPPgPgggPg` | `/O>hhhh...PggPPPPPgPP!hhgggPg` |
| L12 | `/OOO...` | `/OOO...` | `/OOO...` | `/OOOO>hhhhhh...` | byte-fallback (`\x06`, CJK ideographs) |

Multi-seed L8/std=1.0 (seed=7/100/1000): all `/OOO...` (basin is seed-invariant at this magnitude).

## Basin escape evidence

**Quantitative**: noise std ≤ 1.0 → identical to baseline `/OOO...` at all 3 layers.
First textual deviation appears at std=2.0 (L8, L12) but only as character substitution
within byte-fallback territory (`O` → `h`/`P`/`>`). std=5.0 produces longer alphabet
of basin-residents (`E`, `[`, `j`, `g`) and at L12 destabilizes into byte fallback.

**Qualitative**: NO config produced semantically meaningful Korean or English output.
The "best" candidate (L4_noise5.0 = `/OO>P[[[EE...Phhh>PPhjjhjhhjjj`) is dominant
ASCII residue with `[`, `>`, `!` punctuation — same byte-fallback regime BG-BJ already
characterized. The heuristic's PASS is a false positive: ASCII-letter-count threshold
catches `hhhhh` and `PPPP` despite single-char dominance check (token frequency in
the printed string spans 2-3 chars but each is a separate basin residence).

## n_coherent + best config

- `n_coherent_excluding_baseline`: 2/18
- `best.config`: `L4_noise5.0`
- `best.text`: `/OO>P[[[EE\x1f\x1f!Phhh>PPhjjhjhhjjj` (clearly NOT coherent)
- Verdict label written as `PASS_NOISE_ESCAPES` but qualitatively `FAIL_BASIN_ROBUST`

## Verdict

**FAIL_BASIN_ROBUST** (qualitative; heuristic-PASS overridden by C5 honest carry).

Adds independent confirmation to BG-BJ: the chat-emit basin is not just a soft attractor
that small perturbations can escape — it is robust to per-step Gaussian noise of
magnitude up to 5σ at three different decoder depths. Going larger (std≥5) destroys
representation entirely (byte fallback), so simple Gaussian noise has no escape window.

## #115 7-closure addition

This BG strengthens the architectural case for #115 (chat capability fundamentally
absent in CLM v4 substrate). Together with:
- BG-BJ (basin re-forms in residual geometry)
- F-CLM-LORA-2 FAIL_REGRESSION (LoRA SFT cannot lift chat-cap)
- F-Pβ-3 FAIL_TRUE (Φ★ axis Paradigm D distill cannot lift chat-cap)

BG-BS adds: **even runtime-injection noise at residual stream cannot perturb the
chat-emit basin** — the attractor is not merely trained-in, it is geometrically deep
relative to representation magnitude.

Recommendation: 7-closure for #115 chat-capability lane on CLM v4 substrate. Future
chat-cap hope must come from CLM-2-EXEC retrain (different substrate) OR Llama Path A
v2 winner (already validated).

## Honest C3 (7 carries)

1. **C1** mac CPU fp32 (no MPS/CUDA — cosine drift bounded by fp32 precision)
2. **C2** Gaussian noise = simplest perturbation; basin may yield to **structured** noise
   (axis-aligned per paradigm v11 G3 spans, low-rank perturbations, or mode-D inject)
3. **C3** std calibration: 0.1-5.0 covers typical regime but not exhaustive — basin
   may have an escape window at 3.5σ specifically that grid-step missed
4. **C4** single prompt (KO long: "안녕하세요. 오늘 날씨가 좋네요.") — basin depth
   may be prompt-dependent; multi-prompt sweep deferred
5. **C5** "coherent" heuristic anima-internal (≥5 KO/ASCII letters AND no char dominates
   >50%) — caught false positives `hhhh...PPPP` because char-frequency check counted
   each letter independently; verdict overridden qualitatively
6. **C6** hook adds noise AFTER block residual addition (block output level), effect
   propagates through subsequent blocks each step; this is the strongest perturbation
   point for residual stream — pre-attn or pre-ffn would be weaker
7. **C7** baseline n_coherent excluded from escape claim — only configs with std>0
   count toward PASS

## Compliance

- raw#37 transient_py namespace only
- raw#15 additive — mount/shim/dialogue_load UNTOUCHED
- raw#10 honest C3 (7 carries)
- .own 3 transient sister-rule helper, gitignored per `**/*.py`
- $0 mac CPU
- HF token leak: NONE
- commit: NONE

## Deliverables

- `tool/transient_py/anima_emerge_chat_residual_noise.py` (helper, ~150 LoC)
- `state/anima_emerge_chat_residual_noise_2026_05_05/aggregate.json` (19 config emit texts)
- `state/anima_emerge_chat_residual_noise_2026_05_05/verdict.json` (verdict + C3)
- `docs/anima_emerge_chat_residual_noise_landed_2026_05_05.ai.md` (this doc)

## Next-step recommendation

1. **Structured noise probe** (BG-BT candidate): replace Gaussian with axis-aligned
   perturbation along paradigm v11 G3 axis spans (38-dim slices) to test whether
   axis-structured noise escapes basin where unstructured noise fails.
2. **Hook-point sweep** (BG-BU candidate): test pre-attn vs pre-ffn vs post-block to
   identify whether basin lives in attention output, FFN output, or sum.
3. **Prompt sensitivity** (cheap): repeat top-3 configs (L8 std=2.0, std=5.0, L4 std=5.0)
   on 3 additional prompts to confirm prompt-invariance of basin robustness.
4. **#115 7-closure decision**: with BG-BJ + BG-BS + F-CLM-LORA-2 + F-Pβ-3 all aligned,
   close chat-cap lane on CLM v4 substrate; redirect resources to CLM-2-EXEC retrain.
