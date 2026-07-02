# H_6170 — G6 FALS attention-capacity: ENGINE-NATIVE TERMINAL + BGB validation

**tier:** 🧱 WALL — ENGINE-NATIVE TERMINAL (G6 FALS floor holds on live core/ decode) · `wired: engine-native (byte-mouth ByteGPT+BGB via anima evaluate --py)`
**base:** 303M h1129c ByteGPT (d1024·L24·H16·block512, FROZEN) · **source:** UNIVERSE (closes the DIRECTIONAL campaign on branch `g6-attn-capacity-campaign`, `state/6164_g6_attention_capacity/`)

> **id note:** the DIRECTIONAL campaign's VERDICT.md self-labelled "H_6165", but that id had already landed on origin/main for a *different* hypothesis (`6165_g1_novel_mechanism_deepresearch`) via parallel fleet work; the attention-capacity campaign was never registered on main. Registered here as the next free id **H_6170** (tail of origin/main jsonl = H_6168).

## Hypothesis

The CAP×REG factorial (18 cells, torch) closed 🧱 WALL **DIRECTIONAL** — MAX FALS_in=0.33 (REG-on N=2 s7, B3 X-shuffle NO-collapse = form not earned binding). Does the G6 FALS floor **hold on the live core/ engine**, and does the merged BGB injected-attention decode (#2714) actually work on a real 303M injected ckpt?

## Method (a_fire_recover_complete gap closed)

`run_factorial.py` saved only cell JSON — no injected weights. Re-trained the single most-informative cell **REG-on N=2 seed=7** (best DIRECTIONAL signal, FALS_in=0.33) WITH ckpt-save, + **REG-off N=2 s7** null control. 600 steps, base frozen, 25.2M trained params, pool GPU (aiden/summer RTX 5070, $0). Saved injected `.pt` in the `{"bind":[block_sd…],"gate":[float…]}` contract → `anima serialize-bind` (BGB trailer) → `anima evaluate --py` (torch-free numpy, core/decode.py `_bg_apply_bind`).

## Verdict (engine-native TERMINAL)

🧱 WALL — ENGINE-NATIVE TERMINAL (`anima evaluate --py`, torch-free numpy through core/decode.py BGB mouth, HEXA_DET=1, pool aiden/summer $0, 2026-07-02). The engine's OWN frozen G6 gate (g6_build_frames) reads **falsifiable=0 for base, REG-on N2 s7, AND REG-off N2 s7** (all distinct=6, all G6 🔴 FAIL; G1 best_distinct base=1 / injected=0). Injected N=2 attention CAPACITY opens NO engine-native G6 falsifiability, and REGISTER (on vs off) opens none either — the DIRECTIONAL floor holds on the live engine. The campaign's cosmetic torch form-lift (FALS_in 0.33 via the separate IDEATION_SEEDS harness, B3 X-shuffle NO-collapse) does NOT survive to the engine's frozen gate. Converges with the G1/G6 DPI meta-law: the wall is trunk-objective / earned-binding, not a depth-capacity ceiling fixable by injected attention. verbatim `state/verdicts/6170_g6_attn_capacity_terminal/H_6170.txt`.

## BGB enabler validated on real 303M

`anima serialize-bind` spliced both injected `.pt` (N=2, gates≈±0.013) onto the base `.bin` → 1.314GB out.bin, `bg_is_bytegpt=True`, `bg_load ok`, 2 bind blocks round-trip, **zero code changes** (block state_dict keys matched `_bind_block_bytes` exactly). No bug in core/serialize.py / core/decode.py. base `.bin` serialize byte-identical across aiden==summer (sha `5c303f02…`). First real-303M end-to-end proof of the #2714 BGB path.

## artifacts

`state/6170_g6_attn_capacity_terminal/` — RESULT.md · CKPT_MANIFEST.md · ckpt/inj_REG{on,off}_N2_s7.pt (pulled, sha-verified) · eval_logs/eval_{base,regon,regoff}*.log · train_save_cell.py (DIRECTIONAL trainer)
DIRECTIONAL precedent: `state/6164_g6_attention_capacity/` (campaign branch, torch 18-cell factorial + VERDICT.md).
