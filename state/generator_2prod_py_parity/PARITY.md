# generator L3 mouth-dispatch 2-production byte-parity — core/generator.py ⇄ core/generator.hexa

Per CLAUDE.md `a_two_production_mirror` / `a_core_engine_map`: hexa + py are TWO
co-equal production engines kept at byte-parity. `core/generator.py` is the 1:1
byte-faithful mirror of the L3 MOUTH-DISPATCH surface of `core/generator.hexa`
(the single typed mouth slot — header-sniff → conv `.clm` mouth via `clm_decode`
or ByteGPT `.bin` mouth via `bytegpt_decode`). It routes to the already-parity-
proven `core/clm_decode.py` + `core/bytegpt_decode.py`. The VERDICT path stays
engine-native (hexa); the py engine is the parity-proven mirror.

## Ported surface (with generator.hexa line refs — reference-match)

| py fn | generator.hexa | role |
|---|---|---|
| `_gen_rd_u32`            | :792 | LE u32 from byte buffer |
| `_gen_path_is_file`      | :245 | empty-path-safe isfile |
| `_gen_is_bytegpt`        | :148 | ByteGPT sniff (vocab==256, nlay 1..64, nh\|d, block 1..8192) |
| `_gen_clm_probe_header`  | :224 | CLM\x01 magic probe → {exists,valid,nblocks} |
| `gen_null_backend`       | :74  | always-ready null vtable |
| `gen_clm_backend`        | :101 | .clm header admit → loaded/decodable |
| `gen_bytegpt_backend`    | :175 | ByteGPT header admit → loaded/decodable |
| `gen_mouth_kind`         | :628 | sniff → "bytegpt"\|"clm"\|"unknown" |
| `gen_auto_backend`       | :641 | dispatch → gen_bytegpt_backend \| gen_clm_backend |
| `gen_clm_chat`           | :599 | .clm greedy argmax (clm_decode_argmax) |
| `gen_bytegpt_chat`       | :664 | ByteGPT greedy argmax (bytegpt_decode_argmax_ranged) |
| `gen_auto_chat`          | :684 | dispatch → bytegpt_chat \| clm_chat |
| `gen_clm_ideate`         | :697 | .clm seeded top-k (clm_decode_topk_sampled) |
| `gen_clm_ideate_W`       | :713 | loaded-W .clm seeded top-k |
| `gen_bytegpt_ideate`     | :728 | ByteGPT seeded top-k (bytegpt_decode_topk_sampled_ranged) |
| `gen_auto_ideate`        | :750 | dispatch → bytegpt_ideate \| clm_ideate |

NOTE the sniff is reproduced VERBATIM from generator.hexa (`_gen_is_bytegpt`'s
tight bounds: vocab==256, n_layer 1..64, n_head divides d, block 1..8192) — NOT
the looser ranges in `bytegpt_decode.bg_is_bytegpt`. Those tight bounds are the
dispatcher's actual edge-case behavior, mirrored exactly.

## Method (tiny synthetic ckpts — fast, no OOM)

Two mouths driven through BOTH engines on the SAME seed+args, comparing
`gen_mouth_kind` + `gen_auto_chat` (argmax) + `gen_auto_ideate` (seeded top-k):

- HEXA: `state/generator_2prod_py_parity/parity_harness.hexa` (imports the live
  `core/generator.hexa`; dumps KIND + CHAT_OK/CHAT + IDEATE_OK/IDEATE).
- PY:   `state/generator_2prod_py_parity/parity_py.py` (through `core/generator.py`).

Driven via env `GEN_CK` / `GEN_SEED` / `GEN_N`; ideate args fixed (top_k=8, temp=0.9, seed_rng=4242).

### ByteGPT mouth
- ckpt = tiny random-weight `.bin` `vocab=256 d=64 n_layer=2 n_head=4 block=64`
  (`state/kvcache_decode/mk_tiny_bytegpt_fixture.py`, the SAME fixture the
  bytegpt_decode.py parity used). seed=`"Hello world"`, gen=24.

### ConvMoE .clm mouth
- ckpt = `state/lane_p_clm/clm_d768_e2l1.clm` (the d768 v0.2 CLMX golden, decodable).
  seed=`"WAKE anima"`, gen=24.

## Result — PARITY PASS (both mouths, byte-identical)

```
BYTEGPT  gen_mouth_kind=bytegpt   hexa==py : True   sha256 4e7145fe…6438c8
           CHAT  (gen_auto_chat → gen_bytegpt_chat → bytegpt_decode_argmax_ranged)   byte-identical
           IDEATE(gen_auto_ideate→ gen_bytegpt_ideate→ bytegpt_decode_topk_sampled_ranged) byte-identical
CLM      gen_mouth_kind=clm       hexa==py : True   sha256 7cd99d97…1321e598
           CHAT  (gen_auto_chat → gen_clm_chat → clm_decode_argmax)                  byte-identical
           IDEATE(gen_auto_ideate→ gen_clm_ideate→ clm_decode_topk_sampled)          byte-identical
```

Byte-identical decode output (24 greedy + 24 seeded-sample bytes per mouth) is a
STRONGER proof than logits: argmax/sample tokens never flip → the underlying
logits agree within the decision margin. The decoder-level logits parity is
~12.6 dp (clm_decode.py / bytegpt_decode.py PARITY records, the FP-reassociation
floor ~1e-13) and is inherited here unchanged — generator.py adds only routing,
no math. The dispatcher + BOTH routings are byte-faithful.

### Header-sniff edge cases (gen_mouth_kind, py)
```
''(empty) -> unknown    missing -> unknown    short(3B) -> unknown
rand(20B non-CLM, insane header) -> unknown
.clm -> clm             ByteGPT .bin -> bytegpt
```
Matches generator.hexa: ByteGPT checked first (absence of CLM\x01 + sane 5xu32),
else CLM\x01 probe, else unknown — disjoint, edge-safe (never crashes on
missing/short/garbage input).
