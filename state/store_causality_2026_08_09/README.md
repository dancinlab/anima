# Compose-2 causal gate — 2026-08-09

This directory is the frozen first panel for `anima-py evaluate --store-causality`.

Build:

```bash
anima-py corpus storebind \
  --out state/store_causality_2026_08_09/panel.txt \
  --n-blocks 64 --store-slots 8 --seed 7 --lang en --compose 2
```

First read used the locally available
`.fire-recover/h9672_rv_sweep/RV3c_13_CONFIRM_orc1.00_p1_0.99_flip0.99.clm` checkpoint.
It returned `INVALID-INSTRUMENT`: pair-oracle accuracy was 65/128 = 0.5078125, below the
pre-registered 0.90 gate. No block, shuffle, or recovery result was interpreted.

Do not tune this panel or its bars. The next run needs a checkpoint whose two-address pair
oracle reaches 0.90; only then may the normal and causal-control arms be read.
