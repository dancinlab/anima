# Compose-2 causal gate — 2026-08-09

This directory is the frozen first panel for `anima-py evaluate --store-causality`.

Build:

```bash
anima-py corpus storebind \
  --out state/store_causality_2026_08_09/panel.txt \
  --n-blocks 64 --store-slots 8 --seed 7 --lang en --compose 2
```

The frozen panel and bars were not regenerated or changed.

The first read used the locally available
`.fire-recover/h9672_rv_sweep/RV3c_13_CONFIRM_orc1.00_p1_0.99_flip0.99.clm` checkpoint.
It returned `INVALID-INSTRUMENT`: pair-oracle accuracy was 65/128 = 0.5078125, below the
pre-registered 0.90 gate. No block, shuffle, or recovery result was interpreted.

The first dual-read checkpoint still let the answer-position gate carry both entity identities.
It memorized the seen combinations but scored only 75/128 = 0.5859375 on held-out pair-oracle;
again, no causal-control arm was run. The shared CLMS path was then corrected so both live mention
attentions receive their own oracle/address target and the fusion gate reads only the upstream
operator row on a position-normalized trunk.

Final checkpoint:
`.fire-recover/store_causality_2026_08_10/compose2_dual_causal_s7.clm`.
Checkpoint SHA-256: `878dc66e56a26f54c0bd4c67220fb0779497d30d8394e0b1ea1a6ca2e5e650c5`.
Frozen panel SHA-256: `f2e5bd175f264ec22cc90a6e6367f78994334c3a56f889c1294e77d50a411939`.

| Arm | Correct | Accuracy | Required |
|---|---:|---:|---:|
| pair-oracle | 128/128 | 1.0000000 | >= 0.90 |
| normal | 117/128 | 0.9140625 | >= 0.75 |
| clue A removed | 64/128 | 0.5000000 | <= 0.56 |
| clue B removed | 62/128 | 0.4843750 | <= 0.56 |
| addresses shuffled | 58/128 | 0.4531250 | <= 0.56 |
| recovery | 117/128 | 0.9140625 | >= 0.75 |

Verdict: `SUPPORTED-CAUSAL`. Measured chance remained 0.50 and the address derangement had zero
fixed points. `result.json` is the machine-readable record, including the failed pair-oracle runs.
Do not tune or regenerate this panel, its randomization, or its bars.

The frozen compose-2 data, panel, controls, and result are also pinned at commit
`8f29c2f16f214734d9b5fa4010c57c48fff3979e` in the private Hugging Face dataset
`dancinlab/anima-store-causality-compose2-2026-08-09` (13 repository files including
`.gitattributes`, 412,153 bytes). Hugging Face is the training-data management SSOT; the existing
Git data and panel files remain byte-unchanged as regression fixtures.

Multi-seed follow-up: the same frozen training recipe at seed 11 scored 32/128 = 0.2500 on
pair-oracle and stopped before all controls. This does not retract the seed-7 checkpoint result,
but it shows the training path is not multi-seed stable. The run and recovered artifact hashes are
recorded in `../store_causality_repro_2026_08_10/`.
