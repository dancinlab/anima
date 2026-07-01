# H_1815 CLS-on-ByteGPT — 303M GPU launch note

Mirrors the H_1602 canonical launch (`state/1602_bytegpt_recomb_objective/PREREG_FREEZE.md`)
exactly — same ByteGPT d=1024/L=24/H=16/block=512 (~303M) shape, savant golden-zone
cusp-anneal ON, 4-cell register corpus, proportional sample, val_frac=0.05, seq_len=512,
batch=8, steps=2000, bf16, lr=3e-4, seed 7. Only NEW variable = the CLS objective arm.

Run on a **pool/rented GPU host** (NOT mini, NOT this mac). `--canon` selects the 303M shape.

## Arms (3) — seed 7 single-seed A/B/C (multiseed {4302,4303} = follow-on only if a lift appears)

```
# 4-cell corpus paths (resolve on the GPU host; short specs auto-resolve from HF, or use
# local rsync'd paths — anima-corpus-{ko,en}-{general,sns}):
KO_GEN=anima-corpus-ko-general
EN_GEN=anima-corpus-en-general
KO_SNS=anima-corpus-ko-sns
EN_SNS=anima-corpus-en-sns          # KNOWN-SMALL/dup caveat (both arms see identical corpus)

OUT=state/1815_cls_bytegpt/ckpt; mkdir -p "$OUT"
for OBJ in ce_marginal cls_sep cls_full; do
  python3 state/1815_cls_bytegpt/trainer.py --objective "$OBJ" --seed 7 --canon \
    --corpus "$KO_GEN" "$EN_GEN" "$KO_SNS" "$EN_SNS" \
    --cell-label ko-general en-general ko-sns en-sns \
    --sample proportional --steps 2000 --val-frac 0.05 --val-every 200 --bf16 --lr 3e-4 \
    --out "$OUT/${OBJ}_seed7.pt" \
    --bin-out "$OUT/${OBJ}_seed7.bin" \
    --json-out "$OUT/${OBJ}_seed7.json" 2>&1 | tee "$OUT/${OBJ}_seed7.log"
done
```

- `ce_marginal` = ARM-OFF control (standard next-byte CE).
- `cls_sep`     = CE + 0.1·L_separation (DG decorrelation + sparsity on the penultimate).
- `cls_full`    = CE + 0.1·L_separation + 0.1·L_completion (sep + CA3 autoassociative completion).
- The `cls_full` completion head is TRAINING-ONLY (Linear 1024→256→1024) and is dropped at
  serialize — every `.bin` is a pure ByteGPT mouth (5×u32 header), engine-loadable.

## Measure (engine-native, terminal — a_engine_native_learning)

```
for OBJ in ce_marginal cls_sep cls_full; do
  python3 cli/evaluate.py "$OUT/${OBJ}_seed7.bin" \
    --corpus "$KO_GEN" "$EN_GEN" "$KO_SNS" "$EN_SNS" --gen 80
done
```

`--gen 80` explicit so g_eval_g1 reaches the native 80/120 recombination ladder (NOT the
`--gen 0`→40 collapse). Verdict path = `cli/evaluate.py` (py-parity ByteGPT mouth) — torch
training is DIRECTIONAL only.

## FROZEN decision test (pre-registered, H_1129 bars verbatim — no post-hoc bar change)

- **G1 (decisive):** ∃ k∈{2..5} with `composed_distinct ≥ 2 AND composed_distinct > max_single
  AND coherent (kwr≥0.50)` at the 80/120 ladder.
- CLS **cracks G1 on ByteGPT** iff an `cls_*` arm G1 PASS **and** strictly > `ce_marginal` G1,
  both arms held-out DESCENT PASS (every register val_CE < ln256 = 5.5452).
- Frozen prediction (consistent with H_1640 ConvMoE floor + h1129 ByteGPT floor): both floor
  (no lift). Honest either way (c9).

## ckpt discipline (a_fire_recover_complete)

.pt + .bin PULLed to permanent storage BEFORE teardown; engine re-measure on the `.bin`.
