# S1 Consumer Spec — wiring qrng_lora_init.bin into anima LoRA init

## Status

`design_only` — qrng_lora_init.bin is captured but not yet read by any
training script. This doc is the wiring blueprint for whoever closes
that gap.

## Wire point

`anima/training/train_alm_lora.hexa:585`

```hexa
fn init_lora_A(d: int, r: int, n_adapters: int, base_seed: int) -> array
```

Currently the caller passes `base_seed` from a deterministic source
(see callers ~line 585 vicinity). Replace that source with a value
derived from `anima/mirror/qmirror/seed/qrng_lora_init.bin`.

## Minimal wiring (parameter-injection style)

Read first 8 bytes of qrng_lora_init.bin as a 63-bit int and use as
`base_seed`. One-line change at the call site:

```hexa
let qrng_seed_hex = exec("xxd -l 8 -p ~/core/anima/mirror/qmirror/seed/qrng_lora_init.bin").trim()
let base_seed = hex_to_int63(qrng_seed_hex)   // any deterministic 63-bit cast
let A = init_lora_A(d, r, n_adapters, base_seed)
```

Provenance hook: also append a row to
`anima/mirror/qmirror/seed/consumed.jsonl` at consumption time:

```json
{"ts":"…","consumer":"train_alm_lora::init_lora_A","seed_bin":"qrng_lora_init.bin","seed_bin_sha256":"1517a8e1…","base_seed_used":<int>,"d":…,"r":…,"n_adapters":…}
```

## Stronger wiring (buffer-walker style, optional)

Instead of just seeding the LCG, replace the internal Lehmer walker
with a buffer reader that consumes qrng bytes directly:

- Open qrng_lora_init.bin as a 1024-byte buffer.
- For each LoRA element, read 4 bytes (uint32), normalize to [-1, 1) × scale.
- 1024 bytes = 256 elements per LoRA-A draw. For larger adapters, batch
  multiple pull.hexa runs into qrng_lora_init.<N>.bin shards.

This is more faithful to the qmirror-as-entropy-source intent (no
intermediate LCG). Tradeoff: needs binary buffer reading (xxd shellout
or hexa stdlib io::read_bytes if available).

## Verification (post-wiring)

1. Run training with qrng wiring on; capture loss curve at step 100.
2. Re-run with same seed bin; loss curve must be byte-identical.
3. Re-run after `pull.hexa` → new bin (different sha256) → loss curve
   should differ but converge similarly.

## Tier note

Default mock_lcg tier produces a deterministic 1024-byte fixture
(sha256 `1517a8e10994b57d854e9ce2b367b79bc6f2019d751a03b115322db538bfc133`).
For real ANU-anchored entropy, run pull.hexa with
`NEXUS_QMIRROR_LIVE=1 NEXUS_QMIRROR_ANU_KEY=<k>`. The wiring above
treats both tiers identically — only the bytes change.
