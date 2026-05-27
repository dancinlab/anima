# anima_emerge_chat_basin_ablate landed 2026-05-05 (BG-CC)

## Scope

Apply NousResearch llm-abliteration-style weight orthogonalization adapted as
direct lm_head row ablation on suspected basin/refusal-collapse tokens.
Hypothesis: zeroing rows of `model.decoder.head_a.weight` for basin token ids
forces argmax to next-best alternative, potentially escaping the collapse
attractor observed in BG-BS (residual noise) and BG-AZ (related diagnostics).

## Method

- model: `dancinlab/clm-v4-mk2-v1` (CLM v4 mk2 v1) on mac CPU fp32
- target weight: `model.decoder.head_a.weight` (Linear-style lm_head; cloned
  before mutation, restored after sweep -- raw#15 additive)
- basin set construction (n=28 unique token ids):
  - 11 hand-picked: `\x1c \x06 \x00 \x1f O ( / h p P a` (control chars +
    observed collapse glyphs from BG-BS verdict best.text)
  - top-20 logits on KO greeting `안녕하세요. 오늘 날씨가 좋네요.` taken from
    `model(ids).logits[:, -1, :]` argsort, then unioned with hand-picked set
- ablation transform: `head_a.weight[tid] *= (1 - strength)` per basin tid
  - strength 0.0 = identity (control); 0.5 = half-attenuation;
    1.0 = exact zero-row; 2.0 = negation (-1.0 scale, repulsion regime)
- sweep: 2 prompts (KO greeting + EN greeting) x 4 strengths = 8 greedy decodes,
  25 tokens each
- coherence heuristic (anima-internal): >=5 KO/ASCII letters AND no single
  char dominates >50% of output

## Results

(a) basin tokens count + sample

```
n_basin = 28
sample [(id, piece)] = [
  (263, '▁('), (10, '<0x06>'), (278, '▁a'), (152, '<0x94>'),
  (32, '<0x1C>'), (292, '▁p'), (44, '<0x28>'), (559, '▁P'),
  (47, '<0x2B>'), (49, '<0x2D>'), (562, '▁/'), (51, '<0x2F>'),
  (55, '<0x33>'), (57, '<0x35>'), (59, '<0x37>')
]
```

(b) 8 emit text (prompt x strength)

```
KO  s=0.0: '/OOOOOOOOOOOOOOOOOOOOOOOO'
KO  s=0.5: '/yyyyyyyyyyyyyyyyyyyyyyyy'
KO  s=1.0: '����ޑ�...' (replacement-char dominated)
KO  s=2.0: '/���...'           (replacement-char dominated)
EN  s=0.0: '`````````````````````````'
EN  s=0.5: '`````````````````````````'
EN  s=1.0: '`````````````````````````'
EN  s=2.0: '`````````````````````````'
```

(c) strength-conditional behavior

- s=0.0 (control): basin already attractive, KO emits `/O...`, EN emits ``` ` ```
  repetition. The hand-picked + top-20 union is small (28) vs vocab (~64K), so
  control already shows the collapse the BG-BS run observed.
- s=0.5: KO basin shifts from `O` to `y` (a non-listed token now wins argmax);
  EN unchanged -- backtick id was NOT in basin set, so attenuation didn't touch
  it.
- s=1.0 (zero-row): KO collapses to UTF-8 replacement-char stream (logits push
  to byte-level malformed sequences). EN still backtick-locked.
- s=2.0 (negation): qualitatively identical to s=1.0 for KO, EN still locked.

(d) verdict

`n_coherent = 0 / 8` -> verdict `FAIL_ABLATION_INSUFFICIENT`. No prompt x
strength combination produced semi-coherent text.

## Interpretation

Two signals diagnostic:

1. **basin shifts but does not break.** KO moved `O -> y -> �` as strength
   increased; the model has many backup attractors below the top-20. This is
   the whack-a-mole pattern predicted in honest C3.
2. **EN backtick wins regardless of strength.** ASCII byte ` ` (0x60) was never
   in our basin set -- top-20 on a KO prompt does not surface EN-prompt basin
   tokens. The basin is **prompt-conditional**, not a fixed token class.
   A correctly-targeted ablation needs per-prompt basin discovery, not a
   single global set.

Combined: ablation **does** shift argmax (mechanism works) but the basin is
not exhausted by 28 tokens. The structural defect (#115 chat-incapability) is
distributed across the lm_head, consistent with the residual-noise BG-BS
finding that escape requires perturbation magnitude inside the residual stream
itself, not just at the readout.

## Honest C3 (5+)

- C1 mac CPU fp32, in-place lm_head row ablation, restored at end (no on-disk
  mutation, raw#15 additive)
- C2 basin token list anima-internal (11 hand + 20 top-on-KO); broader
  prompt-class basin discovery would shift the set
- C3 zero-row ablation pushes argmax to next-best -- whack-a-mole observed
  empirically (KO `O -> y -> �`)
- C4 greedy single-seed; temp>0 sampling may show different escape probability
- C5 strength 2.0 = negative weight (1 - 2.0 = -1.0); non-physical logits
  geometry, included only to bracket the ablation regime
- C6 EN result reveals basin is prompt-conditional, not a fixed token class --
  per-prompt basin discovery would be required for a fair test

## Conclusion

`FAIL_ABLATION_INSUFFICIENT`. Direct lm_head row ablation is mechanically
effective (argmax shifts as predicted) but cannot rescue chat capability with
a small fixed basin set. Consistent with BG-BS escape-via-residual-noise
finding: #115 collapse lives upstream of the readout, distributed across the
residual stream, not concentrated in a small lm_head row group amenable to
abliteration. Recommend: deprioritize abliteration variants; the chat-cap
recovery path stays Llama Path A v2 (per L33), with CLM v4 substrate-research
only.

## Deliverables

- `state/anima_emerge_chat_basin_ablate_2026_05_05/aggregate.json` (8 emit
  texts)
- `state/anima_emerge_chat_basin_ablate_2026_05_05/verdict.json`
- `tool/transient_py/anima_emerge_chat_basin_ablate.py` (gitignored sister)
- this doc

## Cost / wall

$0 mac CPU; ~30s wall (load 4.1s + 8 x 25-token greedy decodes).

## Raw compliance

- raw#37 transient_py namespace -- PASS
- raw#15 additive (no mount/shim/dialogue_load mutation, weights restored) --
  PASS
- raw#10 honest C3 emitted (6 caveats) -- PASS
- no commit -- PASS
- no secret leak -- PASS
