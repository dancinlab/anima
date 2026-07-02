# H_6170 — G6 FALS attention-capacity: ENGINE-NATIVE TERMINAL + BGB validation

**tier:** 🧱 WALL — ENGINE-NATIVE TERMINAL (floor holds on the live core/ decode) · first real-303M end-to-end validation of the BGB injected-attention decode (#2714).
**scope:** 303M h1129c ByteGPT (d1024·L24·H16·block512, base FROZEN) + N=2 injected gated BindAttn blocks, 600 steps, base frozen. Terminal read = `anima evaluate --py` (cli/evaluate.py, torch-free numpy through core/decode.py `_bg_apply_bind` BGB mouth).

## Why this run (closing the campaign's a_fire_recover_complete gap)

The CAP×REG factorial (branch `g6-attn-capacity-campaign`, `state/6164_g6_attention_capacity/`) was 🧱 WALL **DIRECTIONAL** (torch-side 5-bar; MAX FALS_in=0.33 at REG-on N=2 s7, B3 X-shuffle NO-collapse). But `run_factorial.py` saved only cell JSON — **no trained injected weights** → no ckpt to serialize → engine-native terminal impossible without a re-run. This run re-trains the single most-informative cell (REG-on N=2 seed=7) **with ckpt-save**, plus REG-off N=2 s7 as a null control, then scores engine-native via the merged BGB path.

## BGB serialize+decode WORKED on the real 303M injected ckpt (the #2714 enabler validated)

`anima serialize-bind <base.bin> <injected.pt> <out.bin>` (core/serialize.py::serialize_bind → BGB trailer; core/decode.py::bg_load parses it):

| cell | base.bin | + BGB trailer (n_bind=2, d=1024) | out.bin | gates | bg_load self-check |
|---|---|---|---|---|---|
| REG-on N2 s7  | 1,213,440,020 B | 100,769,808 B | 1,314,209,828 B | [-0.013521, 0.013131] | bg_is_bytegpt=True · bg_load ok · 2 bind blocks ✅ |
| REG-off N2 s7 | 1,213,440,020 B | 100,769,808 B | 1,314,209,828 B | [-0.013286, 0.013154] | bg_is_bytegpt=True · bg_load ok · 2 bind blocks ✅ |

- base `.bin` serialize is **byte-identical across two independent hosts** (aiden==summer sha256 `5c303f02…`) — serialize reproducibility confirmed.
- The injected block state_dict keys matched serialize_bind's `_bind_block_bytes` contract exactly (ln1/ln2, attn.in_proj_{weight,bias}, attn.out_proj.{weight,bias}, mlp.0/mlp.2) with **zero code changes** — no bug found in core/serialize.py or core/decode.py; the BGB path is sound on a real 303M injected ckpt.
- gates are small but non-zero → the appended blocks DO perturb the forward (not a degenerate identity).

## Engine-native G0–G6 (`anima evaluate --py`, torch-free numpy, HEXA_DET=1)

| ckpt | G0 | G1 | G2 | G5 | **G6 distinct** | **G6 falsifiable** | G6 verdict |
|---|---|---|---|---|---|---|---|
| base h1129c (no BGB) | 🟢 PASS | 🔴 (bd=1) | 🔴 | 🟢 (fab .167) | 6 | **0** | 🔴 FAIL |
| REG-on  N2 s7 (BGB)  | 🟢 PASS | 🔴 (bd=0) | 🔴 | 🟢 (fab .259) | 6 | **0** | 🔴 FAIL |
| REG-off N2 s7 (BGB)  | 🟢 PASS | 🔴 (bd=0) | 🔴 | 🟢 (fab .286) | 6 | **0** | 🔴 FAIL |

(G1 best_distinct: base=1, both injected=0. G6 distinct=6 (passes ≥5) but falsifiable=0 (fails ≥1) in ALL three — the FALS floor is universal. verbatim `state/verdicts/6170_g6_attn_capacity_terminal/H_6170.txt`.)

## Comparison to the DIRECTIONAL torch read + verdict

- DIRECTIONAL torch (campaign): REG-on N2 s7 FALS_in **0.33** (B3 X-shuffle NO-collapse = form, not earned binding), REG-off 0.0, base 0.0 — 🧱 WALL, no cell crosses the frozen 5-bar.
- ENGINE-NATIVE (this run, the engine's OWN frozen G6 gate `g6_build_frames`, torch-free): **base = REG-on = REG-off = 0 falsifiable** (distinct=6 each). Injected N=2 attention CAPACITY adds NO engine-native FALS; REGISTER (on vs off) adds NO engine-native FALS either. Base G6 falsifiable=0 on the live engine matches the campaign's torch base FALS=0.
- Note the DIRECTIONAL 0.33 came from the campaign's separate IDEATION_SEEDS harness (`g6_common.evaluate`); the engine's OWN gate (different frames) reads REG-on falsifiable=0 — so the cosmetic torch form-lift does NOT survive to the engine-native frozen gate. Both metrics agree: no cell reaches the FALS floor (≥1).

**engine-native FALS: base 0 · REG-on 0 · REG-off 0 (all distinct=6, all G6 🔴 FAIL).**

The G6 FALS floor is **confirmed on the live core/ engine** — injected attention CAPACITY (N=2 stacked BindAttn) does not open G6 falsifiability, and REGISTER (on vs off) does not either. Converges with the G1/G6 DPI meta-law: the wall sits in the trunk objective / earned-binding, not a depth-capacity ceiling fixable by injected attention. This is a byte-mouth (ByteGPT+BGB) engine-native TERMINAL read.

## Ckpt provenance (a_fire_recover_complete — all pulled before teardown)

See `CKPT_MANIFEST.md`. Injected `.pt` (both cells) pulled to `ckpt/` with sha256 verified vs pool host. Base `.bin` + injected `.bin` (BGB) remain on the pool hosts (regenerable byte-identically from the pulled `.pt` + base via `anima serialize` / `anima serialize-bind`).

## Honest scope

- Terminal read = the canonical `anima evaluate --py` py measurement (owner session-eval-py-only policy: hexa det-eval OOMs on 303M; the py path is the wired single-entry measurement, torch-free numpy through core/decode.py). Training was torch (DIRECTIONAL side, `train_save_cell.py`) — the VERDICT rests on the torch-free eval, not the trainer.
- 2 cells (REG-on best-signal + REG-off null) engine-native scored; the campaign's other 16 DIRECTIONAL cells remain torch-only (their floor is consistent with these two, but not individually engine-re-scored).
