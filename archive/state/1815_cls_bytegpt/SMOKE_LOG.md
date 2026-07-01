# H_1815 CLS-on-ByteGPT — $0 CPU smoke log

Trainer: `state/1815_cls_bytegpt/trainer.py` (base = 1602 ByteGPT trainer verbatim +
CLS `cls_sep`/`cls_full` arms ported from `state/1640_cls_sep_complete/trainer.py`).

CPU-only, tiny config, 3 steps/arm. Interpreter = a local CPU torch venv
(`/Users/mini/anima_chat_pack/venv/bin/python3`, torch 2.12.0, cuda=False).
This is a wiring smoke (end-to-end run + serialize + engine header-sniff) — NOT a verdict.

## Commands (exact)

```
cd state/1815_cls_bytegpt
PY=/Users/mini/anima_chat_pack/venv/bin/python3
# tiny synthetic byte corpus (~12KB, mixed ko/en) written once -> smoke_corpus.bytes
for OBJ in ce_marginal cls_sep cls_full; do
  CUDA_VISIBLE_DEVICES="" $PY trainer.py --objective "$OBJ" --seed 7 \
    --d 64 --n_layer 2 --n_head 4 --block 64 --steps 3 --seq-len 64 --batch-size 4 \
    --corpus smoke_corpus.bytes --cell-label smoke \
    --val-every 3 --log-every 1 --val-frac 0.1 \
    --out ckpt/smoke_${OBJ}.pt --bin-out ckpt/smoke_${OBJ}.bin --json-out ckpt/smoke_${OBJ}.json
done
```

## Result — all 3 arms rc=0, loss finite, .bin written

| arm         | loss0    | lossF    | aux at final step                                   | .bin bytes | header (5×u32)        |
|-------------|----------|----------|-----------------------------------------------------|------------|-----------------------|
| ce_marginal | 5.55393  | 5.43108  | (none)                                               | 547860     | [256, 64, 2, 4, 64]   |
| cls_sep     | 5.55393  | 5.43104  | decorr=0.0328, sparsity=0.4888                       | 547860     | [256, 64, 2, 4, 64]   |
| cls_full    | 5.56734  | 5.43875  | decorr=0.0431, sparsity=0.5222, complete_mse=1.0031  | 547860     | [256, 64, 2, 4, 64]   |

- `cls_sep` runs 3 steps, loss finite, **L_separation active** (decorr + sparsity aux present), .bin written. YES.
- `cls_full` runs 3 steps, loss finite, **both aux terms active** (decorr + sparsity + complete_mse). .bin written. YES.
- `.bin` header first-20-bytes = `0001000040000000020000000400000040000000` =
  `[vocab=256, d=64, n_layer=2, n_head=4, block=64]` u32 LE — matches config exactly =
  the ByteGPT 5×u32 format `serialize_bin` wrote. OK.
- Held-out DESCENT gate PASS on the smoke cell for all arms (val_CE ≈ 5.38 < uniform ln256 = 5.5452).

## Serialization discipline confirmed

- Completion head (`cls_full`) is a **separate `nn.Module`** (Linear 64→256→64), NOT in
  `ByteGPT.state_dict()`. Verified: `smoke_cls_full.pt` model keys = 29, `comp_head` keys
  present = **0** (`tok.weight … head.weight`). The `.bin` is a pure ByteGPT mouth.
- Engine mouth sniff — `core/bytegpt_decode.py::bg_is_bytegpt` returns **True** for all 3
  `.bin`, `bg_header` = `{vocab:256, d:64, nlay:2, nh:4, block:64}`. The .bin is
  engine-loadable by `core/bytegpt_decode` / `cli/evaluate.py`.

## Verdict note (a_engine_native_learning)

torch training here is the **bridge/DIRECTIONAL** rung only. The terminal engine-native
G0-G6 verdict = `cli/evaluate.py <bin> --corpus <4-cell> --gen 80` on the 303M `.bin`
(py-parity ByteGPT mouth), NOT any torch-side probe. Smoke proves wiring, not G1.
