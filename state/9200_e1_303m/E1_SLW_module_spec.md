# E1 SPEC — `SLW` gated-write forward-slot (H_9200, 303M rung)

## 0. BGB extend vs new module — decision: **new trailer, BGB conventions reused**

BGB gated blocks (`decode.hexa:2304-2429`) write into the **shared residual stream** via a standard attention block — symmetric, content-mixed, superposed into the same medium the base trunk uses. That *is* premise (b): the combination is still an order-blind residual sum, and H_9027/H_6170 landed in the additive family. Extending BGB would entangle a walled mechanism with the new lever and make slot-ablation dirty (can't zero the slot lane without zeroing the bind blocks). E1 is therefore a **distinct forward module** — but it copies BGB's proven conventions wholesale: trailer-chain append position, magic+u32 header, fixed-order LE f32 tensor layout, ranged-read absent⇒passthrough guard, gate=0 ⇒ byte-identical forward, and the `_bg_apply_bind`-shaped apply function.

## 1. Mechanism

**Tap point** (both mouths): the post-trunk pre-`ln_f` hidden sequence — BYTE mouth: after `_bg_apply_bind`, before `ln_f` in `bg_forward_last_W`; CONV mouth: the penultimate `yn` (decode.hexa L1108) before the readout conv. Same math either side.

State: `S ∈ [n_slot, d_s]`, **zeroed at sequence start** (no cross-sequence carry — kosmos/p8 out of scope). One causal left-to-right pass over positions `t = 0..T-1`, per position on hidden `x_t ∈ d`:

```
r_t = W_r·x_t + b_r                    (k)      role key   → WHERE
a_t = softmax(r_t · K_slotsᵀ / √k)     (n_slot) write address
v_t = W_v·x_t + b_v                    (d_s)    filler     → WHAT
g_t = sigmoid(w_g·x_t + b_g)           scalar   write gate
S[s] ← (1 − g_t·a_t[s])·S[s] + g_t·a_t[s]·v_t   ∀s          erase-then-write

q_t = W_q·x_t + b_q                    (k)      read key
b_t = softmax(q_t · K_slotsᵀ / √k)     (n_slot) read address
m_t = Σ_s b_t[s]·S[s]                  (d_s)    read-after-write at t (causal: only prefix ≤ t written)
x_t ← x_t + γ·(W_o·m_t + b_o)                   mouth reads slots via this term; head/ln_f unchanged
```

**Why order-sensitive where cbind was blind:** `cbind(A,B)=A+B` is commutative — role and filler are indistinguishable, so the pair collapses to a bag. Here the two concepts take **asymmetric ports**: one determines the address (`r→a`), the other the content (`v`). Swapping them changes (where, what) → different `S`. Additionally the erase-write is temporally asymmetric — a later write to the same slot overwrites the earlier one; sum never does.

**Why it beats the D>RF independence wall:** the wall is spatial — two concepts farther apart than the receptive field have no shared conv support, hence mathematically independent contributions to the logits. `S` lives **outside the token stream**: a write at position `i` lands in slot `s` by content-addressing, and a read at any `j>i` retrieves it by key match, with zero dependence on `j−i`. `∂logits_j/∂x_i` becomes nonzero through `S` at arbitrary distance. The de-risk ladder confirmed CE alone induces this routing (0.976 vs additive 0.145); this module is the same forward, engine-native at 303M.

Defaults (pre-registered, not tuned post-hoc): `n_slot=8, k=64, d_s=d`. Cost: O(T·(n_slot·(k+d_s) + d·(2k+2d_s)+d)) — negligible vs trunk.

## 2. Weight layout — `"SLW\x01"` trailer

Appended at the **end of the trailer chain**: BYTE file = `head → [BGB] → [SLW]`; CLM file = `…CLMX ext → [CLMB] → [SLW]`. Reader takes the final byte offset the previous trailer reader returns and probes; short-read/absent ⇒ `slw = null` ⇒ forward byte-identical to today (parity-safe, same guard idiom as `_bg_read_bind_trailer`).

```
bytes 83,76,87,1                magic "SLW\x01"
u32 n_slot · u32 k · u32 d_s    LE
K_slots  [n_slot·k]     f32 LE      slot keys
W_r [k·d]   b_r [k]                 role/write projection
W_q [k·d]   b_q [k]                 read projection
W_v [d_s·d] b_v [d_s]               filler projection
W_o [d·d_s] b_o [d]                 output projection
w_g [d]     b_g [1]                 write-gate
gamma [1]                           lane gate (γ=0 ⇒ exact passthrough)
```

All matrices row-major `[out, in]` like existing layers; fixed order, no optional fields — numpy mirror deserializes with one struct-walk, parity trivial. Weights enter the engine **only** through the existing `generator.hexa` L3 `gen_auto_backend` slot — they ride inside the same `.clm`/`.bin` file; no second entry point (`a_core_engine_map` satisfied by construction).

## 3. DISJOINT wiring + G5 gate

- `S`, `m_t`, and all SLW tensors are **internal to `core/decode.hexa`** — never exported into the maps consumed by `brain.hexa`, `engine_g.hexa`, `pure_field.hexa`, or `brain_decide`'s input. No new keys on any brain/emit interface. The slot lane changes only **WHAT** the mouth says, never **WHETHER** it speaks.
- Emit/silence (Ψ, A⇄G tension) is computed upstream of the L3 content slot, so disjointness is structural; the check makes it measured:
- **G5 ImmuneMemory gate check (pre-reg):** run the standard emit/silence trace on identical inputs with `γ=1` vs `γ=0`. PASS ⇔ the emit/silence decision sequence and Ψ statistics are identical (det tolerance) while content differs. Any divergence = slot lane bled into the drive path = wiring FAIL, do not merge.

## 4. Minimal function list

New in `core/decode.hexa` (mirrors the `_bg_*` bind pair):
```
fn _slot_read_trailer(path: string, byte_off: int, d: int) -> map      // null-map if absent
fn _slot_apply(x: int, slw: map, T: int, d: int)                        // in-place; one causal pass; no-op if slw null or γ==0
```
`_slot_apply` reuses the existing scalar helpers (`_bg_linear`, the `_bg_mha` softmax routine, scalar sigmoid via existing exp op) — identical op order in the numpy mirror for byte-parity.

Hooks (each a 2-line insertion):
- `bg_load` / `bg_load_ranged` → call `_slot_read_trailer` after `_bg_read_bind_trailer`, store `"slw"` in `W`.
- `bg_forward_last_W` → `_slot_apply(x, W["slw"], T, d)` after `_bg_apply_bind`, before `ln_f`. (SLW models skip the KV fast path, same rule and same fallback sites as BGB — three existing skip guards at L3068/3133/3359 gain `|| slw` .)
- CLM loader (CLMB reader site, ~L408) → chain `_slot_read_trailer`; `_clmd_fwd_logits*` → `_slot_apply` on `yn` before readout.
- Writer: `clm_reexport.hexa` gains `_write_slot_trailer(fd, slw)` appended last.
- `cli/evaluate.py` → 1:1 numpy `_slot_apply` + trailer reader (the `--py` canonical path, TERMINAL-eligible per `a_eval_py_canonical`) + two eval switches: `--slot-off` (force γ=0) and `--slot-shuffle <seed>` (apply one fixed permutation `π` of slot indices to the **write** address `a_t` only, leaving reads unpermuted — breaks role→slot correspondence, preserves marginals).

## 5. Kill-criterion alignment

Pre-reg measurement: `anima evaluate --py <clm>` G1 recombination ladder.
- **GO:** `best_distinct ≥ 2 ∧ best_distinct > max_single`.
- **Slot-ablation control:** `--slot-off` sets γ=0 ⇒ forward is *bit-exact* base trunk (the BGB passthrough trick) — the cleanest possible collapse control; G1 must fall to the additive floor.
- **Shuffle-bind control:** `--slot-shuffle` scrambles write addressing while keeping every weight and every marginal — recombination must collapse; if it survives, the lift was FORM not BIND (measurement metalaw).
Both controls are pure eval-time switches on serialized state — no retraining, no tune-to-green surface. Negative at 303M = result; the trailer is optional so a FAIL model never ships wired (GREEN-only-when-wired preserved).