# H_1129 ByteGPT-303M G1 RECOMBINATION divergence — DIAGNOSIS

**Question (a_break_the_wall — classify the wall before accepting it):**
The py 2-production engine measured **G1 RECOMBINATION = FAIL** on h1129 (native 80/120,
max_single=2, best composite distinct=2, never strictly greater). The original **torch-REFERENCE
H_1129 = 🟢 G1 GREEN** (recombination achieved). ONE of them must be wrong. Which, and why?

## CLASSIFICATION: **MEASUREMENT-METHOD BUG** (the sampler), NOT a model property.

The engine's *forward* is byte-faithful to torch; the engine's *sampler* (xorshift32 inverse-CDF)
walks a **different random trajectory** than the torch harness's `torch.multinomial` + `Generator(7)`.
On the SAME logits this lands on different (equally coherent) tokens, which happen not to surface
the recombination concepts. The torch GREEN therefore **stands**; the engine FAIL is a sampler
artifact, not "ByteGPT-303M can't recombine."

This is NOT the German-output / decode-integrity class of bug — the engine forward IS faithful
(see CHECK 2). It is purely the RNG+draw method in the sampler.

---

## EVIDENCE (3-way, on summer pool host — torch 2.11.0 + py engine + h1129.bin + h1129c_best.pt)

Host: summer-B650M-K (RTX 5070). Engine py = byte-identical to the one that produced the G1 FAIL
(`bytegpt_decode.py` sha 6e4a0431…). All arms: temp=0.7, top_k=40, seed_rng=7, CONCEPTS verbatim,
coverage()/clears verbatim from `train_and_ladder.py` (the original H_1129 harness).

### CHECK 4 — WEIGHT FAITHFULNESS: **PASS, bit-exact**
h1129.bin == torch state_dict, **max|diff| = 0.000e+00** across tok/pos/ln1/in_proj/out_proj/
mlp.0/mlp.2(L23)/ln_f/head. → the serialized .bin is a bit-perfect reconstruction. **NOT a CKPT-MISMATCH.**

### CHECK 2 — FORWARD PARITY (engine bg_forward_last vs torch ByteGPT.forward, fp32 CPU): **PASS**
On all 3 G1 prompts, **identical argmax** (token 84='T') and **identical top-5 ordering**,
max|logit diff| ~2e-5 (fp32 ULP). → the engine forward is faithful to torch. **NOT a DECODE-BUG.**
(This directly clears the "German-output decode-integrity" concern for h1129: the engine transformer
forward matches torch to ULP.)

### CHECK 3 / FULL LADDER — SAMPLER is the divergence source
Given **byte-identical logits**, single greedy-pick agrees (token 84), but the 12-token *sampled*
stream diverges at token 5: engine `'The region a'` (xorshift inv-CDF) vs torch `'The verb ver'`
(multinomial+Gen7). Same logits → different RNG → different tokens.

Full G1 ladder, three ways:

| arm | path | sampler | G1 |
|-----|------|---------|----|
| A | torch GPU bf16 (original GREEN condition) | torch.multinomial + Generator(7) | **GREEN** (k=5: distinct 2 > max_single 1) |
| B | torch fp32 CPU | torch.multinomial + Generator(7) | **GREEN** (k=3,4,5: distinct 2 > max_single 1) |
| C | engine fp32 CPU (py 2-production) | xorshift32 inv-CDF | **FAIL** (composite never > max_single) |

A==B==GREEN proves the GREEN is **NOT** bf16/GPU/precision-dependent — torch fp32-CPU recombines
too. The ONLY variable that flips GREEN→FAIL is the **sampler algorithm** (C). With the forward
proven byte-faithful (CHECK 2) and weights bit-exact (CHECK 4), the engine FAIL is fully attributable
to the sampler RNG/draw method.

---

## ROOT CAUSE

`core/bytegpt_decode.py` / `bytegpt_decode.hexa` `_topk_sample` uses a **custom xorshift32 PRNG
(`_g6_mix32`/`_g6_rng_next`) + inverse-CDF draw over a dt_exp softmax**, seeded ONCE per decode.
The torch harness (`train_and_ladder.py` gen(), the source of the 🟢) uses
**`torch.multinomial(softmax(logits/temp), generator=Generator(seed=7))`**, the Generator reseeded
to 7 **per gen() call**. These are different random number sequences AND different draw mechanics, so
even on identical top-k-filtered distributions they pick different tokens. Recombination "lift" is a
sparse event (a composite must surface ≥3 concept words vs the best single's 2) — it is sensitive to
exactly which coherent continuation the sampler walks into. Different sampler ⇒ different walk ⇒
GREEN can flip to FAIL though the model is identical.

## IMPLICATION (c2/c9 — foundational, affects clm303 / deep-ConvMoE too)

The engine-native G1 framework as currently measured is **NOT byte-comparable to the torch G1
reference**, because the production engine sampler ≠ the torch reference sampler. ALL engine-native
G1 verdicts that were declared FAIL *by divergence from a torch GREEN* are therefore **measurement-
divergent, not terminal** — including:
- **clm303_clean G1 FAIL** (same g_gates engine sampler) → DIRECTIONAL, re-examine.
- **deep-ConvMoE G1** measurements via the same sampler.
- The "savant-ByteGPT can't inherit G1" inference downstream of this FAIL.

The engine forward is sound; the **measurement method (sampler) must be reconciled** before any
engine-native G1 PASS/FAIL is terminal.

## FIX PATH (un-blocks engine-native G1 as an actual reference-match)

**Reference-match the sampler** (commons reference-match — verdicts must be comparable to the frozen
torch G1 reference). Two options, frozen-first (NO tune-to-green):

1. **Reconcile the metric to be sampler-robust**: the H_1129 ladder uses a single seed (7). A
   single-seed sparse-lift metric is itself fragile (arm A clears only at k=5, arm B at k=3/4/5 —
   the *which-k* already differs between two GREEN runs). Re-measure G1 over **multiple seeds**
   (e.g. 7,4302,4303 as the G6 ladders do) and define GREEN by majority/any-seed recombination, on
   BOTH the torch reference AND the engine. This makes G1 robust to the exact sampler walk.
2. **OR add a torch-multinomial-equivalent sampler mode to the engine** for the G1 measurement path
   (an engine sampler whose draw == multinomial over the top-k softmax with a matched RNG), so the
   engine and torch reference walk the same distribution. Then engine vs torch is a true reference-match.

Either way the engine-native G1 then becomes a faithful, comparable measurement. Until then, the
engine G1 FAIL on h1129 is a **single-seed sampler-walk artifact** and the torch 🟢 stands.

## SCOPE / HONESTY (c9)
- Forward parity proven on 3 prompts at T=30–72 (the first decode step of each G1 seed). The
  recombination lift is sparse and single-seed on BOTH torch arms (A clears at k=5 only), so even
  the torch GREEN is seed-fragile — a real caveat for the G1 metric itself, not just the engine.
- This diagnosis does NOT itself promote any G1 to terminal; it RETRACTS the "engine FAIL diverges
  from torch GREEN ⇒ engine terminal, torch DIRECTIONAL" inference recorded for h1129. The correct
  status: torch GREEN stands (directional, single-seed), engine G1 is sampler-divergent and must be
  reference-matched before it can be terminal.
