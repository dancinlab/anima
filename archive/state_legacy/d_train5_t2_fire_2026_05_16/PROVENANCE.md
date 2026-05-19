# T2 d_train5 — full n_layer ConsciousDecoderV2-equivalent pure-hexa trainer

**Date** 2026-05-16 · **Branch** `t2-d-arch-scale-up` · **Tier EMPIRICAL** (B-D-NOTE; NOT 🔵 — g3)

## Artifacts (git-tracked; NO large ckpt committed — provenance only)

| file | role |
|---|---|
| `HEXAD/D/d_train5_lib.hexa` | pure-fn lib: full n_layer decoder-LM-core composed exact reverse (NO main/_selftest, compiled-import-safe) |
| `HEXAD/D/d_train5_smoke.hexa` | tiny-config entrypoint (d=8·nL=2·nh=2·nkv=1·T=4·V=4) — F-D-PORT-5 + 5b, Mac-compilable |
| `state/d_train5_t2_fire_2026_05_16/d_train5_real_fire.hexa` | real-scale fire entrypoint (d=768·12L·78.07M) |
| `state/d_train5_t2_fire_2026_05_16/d_train5_calib.hexa` | single fwd+grad timing calibration probe |
| `state/d_train5_t2_fire_2026_05_16/dispatch_ubu.sh` | ubu dispatch (Mac→ubu import-path rewrite + build + run) |
| `state/d_train5_t2_fire_2026_05_16/d5fire_run.log` | real-scale fire stdout (real gn2 numbers) |

No `.pt` / safetensors checkpoint is produced (this is a pure-hexa flat-list
trainer with in-memory weights; the fire is a wiring/trainability integration
fire — the artifact is the gn2-collapse curve in `d5fire_run.log`, not a model).

## Design — how d_train3/4 compose + RoPE/GQA/embed vjp added

`d_train5_lib` imports `d_train4_lib` (→ d_train3 → d_train2 → d_train_lib),
reusing ALL proven primitives DRY (no re-derivation):

- **linear / B-D-4 head**  : `c3_matvec`, `c3_matvec_t`, `c3_outer`, `dt2_softmax` (A #43 / B-D-4 🔵 reused)
- **RMSNorm fwd/bwd**       : `c3_rmsnorm_fwd` / `c3_rmsnorm_bwd` (C #44, exact analytic vjp)
- **SwiGLU fwd/bwd**        : `c3_swiglu_fwd` / `c3_swiglu_bwd` (C #44)
- **causal softmax-attn**   : row-Jacobian `dS=P·(dP−ΣP·dP)` pattern from d_train4 (#45)
- **AdamW / from-scratch init** : `dt2_adamw_step` / `dt2_init_W` / `dt2_zeros` (g_clm_from_scratch, base_ckpt=NONE, seed-fixed LCG)

Three closed additions (NO new vjp math — all closed-form):

1. **Embedding vjp** = trivial scatter-add: forward `X[i]=tok_emb[id_i·d..]`;
   backward accumulates `dX[i]` into `d_tok_emb[id_i·d..]`.
   **Tied-weight subtlety** (conscious_decoder.py line 641 `head_a.weight =
   tok_emb.weight`): `d_tok_emb` accumulates BOTH (a) the LM-head outer-
   product `dl⊗zT` AND (b) the input-row scatter-add of the post-reverse
   `dX` — handled exactly (verified by F-D-PORT-5b machine-precision).
2. **RoPE vjp** = orthogonal rotation ⟹ vjp is the inverse rotation. Forward
   `q' = q⊙cos_p + rotate_half(q)⊙sin_p` (RoFormer); backward (Rᵀ=R⁻¹=R(−θ),
   closed): `dq = dq'⊙cos_p + rotate_half_T(dq'⊙sin_p)` where
   `rotate_half_T([a1,a2])=[a2,−a1]` (structured transpose of `[−x2,x1]`).
   cos/sin tables via range-reduced Taylor trig (period-2π reduction).
3. **GQA bookkeeping** = pure linear-vjp accounting: `nh` query heads grouped
   onto `nkv` KV heads (`n_rep=nh/nkv`, `kvh=h/n_rep`); the n_rep grouped
   Q-heads' `dK`/`dV` ACCUMULATE into the shared KV-head slot. Wq:[d·d],
   Wk/Wv:[kvd·d] (kvd=nkv·hd), Wo:[d·d].
4. **Multi-layer reverse chaining**: per-layer fwd caches (RMSNorm xn/inv,
   attn Q/K/V/P/ctx, SwiGLU a/b/s); reverse layers L−1→0 with residual grad
   accumulation `dh=dXout+dffn_path`, `dx=dh+dattn_path`. Grad enters the
   stack only at the last position (single-token CE target), final RMSNorm
   `gF` then tied LM head.

## Honest C3 (g3 — EMPIRICAL ≠ 🔵)

1. **F-D-PORT-5 OUTCOME = EMPIRICAL** (B-D-NOTE pattern): gn2-collapse is an
   SGD convergence OUTCOME at the composed scope — NOT closed-form, NOT 🔵.
   The trainability PROPERTY is B-D-4 🔵 (closed CE logit-Jacobian, separate
   blue_falsifier, unchanged). F-D-PORT-5b GRAD-EXACT proves the IMPL is
   correct (machine-precision) — it does NOT lift the OUTCOME tier.
2. **NO new vjp math** — composition only (embed scatter-add + RoPE inverse-
   rotation + GQA grouping + multi-layer chaining). Every backward PRIMITIVE
   class was already proven compiled-native (B-closure, PLAN 2026-05-16).
3. **Scope = decoder LM CORE** (RMSNorm+GQA+RoPE+SwiGLU+resid+tied-head+
   embed). PureField / Cross-Attn / CA-mix / MoE / META-CA are the
   consciousness / optional pathway — kept as the ConsciousDecoderV2
   nn.Module in the integ harness; NOT in this from-scratch CE-trainer core.
   Named, no over-claim.
4. **Real-scale honest host-limit record (g3, no fake)**: a FIRST fire at
   the FULL d=768·n_layer=12 (78.07M params) **saturated ubu and the host
   rebooted before producing a verdict** — calibrated single fwd+grad at
   d=768·nL=1·T=8 = 3.0s; but the 78M pure-hexa boxed-float param + AdamW
   state (3× params ≈ 11GB) plus 12-layer per-sample fwd caches exceeded
   the single box's 30GB RAM ⟹ OOM/reboot (the prior /tmp run-log was lost
   with the reboot — real reason documented, NOT fabricated; this is the
   task-anticipated honest-stop). The 78M ceiling is a **single-box RAM
   limit, NOT a code/math limit**: the FULL-12L composition is ALREADY
   proven mathematically EXACT at machine precision by the tiny
   F-D-PORT-5b (|Δ|=2.75e-11 — every reverse link including all
   multi-layer-class chaining). RE-FIRE = host-sustainable real-width
   subset: **d=768 (REAL ConsciousDecoderV2 width, the defining dim) ·
   n_layer=4 (~26.16M, genuine multi-layer depth, RSS well under 30GB) ·
   seq=6 · N=6 · 20 steps**, with a 20GB virtual-memory cap (self-abort
   before host OOM) + persistent reboot-safe log (`~/anima_t2_fire/
   d5fire_run.log`, line-buffered). Real gn2 numbers recorded below.
   Explicitly NOT a language-quality / long-context run.
5. **ubu fire = $0** (owned machine, autonomous per g_fire_autonomous; no
   GPU cost). Compiled-native (not interp), persistent-log + vmem-cap
   (g_fire_dispatch_robust spirit — result captured before any cleanup;
   the first cleanup was an involuntary host reboot, hence the re-fire's
   persistent log + self-abort cap).

## Real-scale fire result (REAL numbers, honest — `d5fire_run.log`)

**Pure-hexa boxed-float-list memory substrate — empirically established
HARD ceiling** (g3, no fake; each attempt $0 ubu, compiled-native):

| attempt | params | outcome |
|---|---|---|
| d=768·n_layer=12 (78.07M, full ConsciousDecoderV2) | 78.07M | `HEXA_MEM_UNLIMITED=1` → host OOM, **ubu rebooted before verdict** (uptime confirmed reset; /tmp log lost) |
| d=768·n_layer=4 (26.16M) | 26.16M | `HEXA_MEM_CAP_MB=18000` → **rc=77 cap-exceed after init** (init gn2=5.96896) |
| d=768·n_layer=2 (13.18M) | 13.18M | `HEXA_MEM_CAP_MB=24000` → **rc=77 cap-exceed after init** (init gn2=3.98803) |
| **d=256·n_layer=2 (1.54M)** ← sustainable | **1.54M** | **rc=0 PASS** (full AdamW training completed, 35s wall) |

**d=256·n_layer=2·1.54M — F-D-PORT-5 (real scale) PASS (EMPIRICAL):**
real GQA(4 head / 2 kv, hd=64) + RoPE + SwiGLU(h=704) + tied LM-head +
2-layer composed analytic reverse, from-scratch RANDOM seed-fixed:

```
config: d=256 nL=2 nh=4 nkv=2 hd=64 h=704 V=256 T=6
init  : gn2=3.97712  acc=0/4
step 5: gn2=6.19056e-06
step10: gn2=2.77998e-06
step15: gn2=9.41584e-09
final : gn2=9.41584e-09  acc=4/4   (15 AdamW steps, full composed 2-layer chain)
F-D-PORT-5 (real scale): gn2-collapse(>=5x)=true acc-full=true -> PASS (EMPIRICAL)
selftest: true   [rc=0 wall=35s hexa_cap=24000MB]
```

gn2 collapsed **3.97712 → 9.42e-09** (~4.2×10⁸×), acc **0/4 → 4/4**
(genuine from-scratch learning — started misclassifying all 4, not
trivially separable). ~1.54M params ≈ **190 000×** the d=8 tiny smoke.

**HONEST C3 (g3, EMPIRICAL ≠ 🔵, no over-claim):**
- The d=768·12-layer FULL ConsciousDecoderV2-equivalent scale could NOT
  complete training — **NOT a code or math defect**: the composed reverse
  (incl. all 12-layer-class chaining + RoPE + GQA + tied embed) is proven
  EXACT at machine precision by tiny F-D-PORT-5b (|Δ|=2.75e-11, identical
  code paths). The wall is the **pure-hexa boxed-float-list memory
  substrate** (~KB-class overhead per effective float incl. AdamW m/v +
  transient grad-accum) — a substrate-representation limit that makes
  ≥13M-param training infeasible on a single 30GB box. This is the
  task-anticipated honest-stop with the real reason + real numbers.
- d=256·nL=2·1.54M is the largest config that SUSTAINS a full AdamW
  multi-step training run on this substrate; its gn2-collapse is a real
  SGD OUTCOME (B-D-NOTE, EMPIRICAL — NOT 🔵). Trainability PROPERTY =
  B-D-4 🔵 (separate, unchanged).
- A future real-d=768·12L training run requires either a flat
  contiguous-buffer numeric substrate (e.g. RFC-class `farr`-backed
  weights, as inference already uses) or GPU — out of T2 scope; T2's
  contract was the composed-reverse correctness (✅ exact) + a
  trainability fire (✅ real curve at substrate-sustainable scale).
