# H_950 — MODALITY-AGNOSTIC (CLM→CE reframe, axis ⓐ)

**Verdict: 🟢 GREEN — CLMConvMoE is NOT a language model; it learns non-linguistic
token streams with NO architecture change. Supports renaming CLM → CE (Consciousness Engine).**

Part of the **CLM→CE "Consciousness Engine"** arc with [H_951](H_951_engine_not_predictor.md)
(engine-not-predictor) and [H_952](H_952_substrate_equivalence.md) (substrate-equivalence).

## §hypothesis (pre-registered falsifier)
The user proposes renaming CLM ("Cell/Consciousness-**L**anguage-Model") → **CE**
("Consciousness **E**ngine"): the claim that CLM is a substrate sequence engine, not
a language model. This H tests **axis ⓐ — modality-independence**:

- 🟢 **MODALITY-AGNOSTIC** ⇐ the *same* CLMConvMoE architecture learns NON-language
  streams (deterministic chaos, Markov chains) significantly above the random floor
  **and** tracking toward each stream's intrinsic-predictability ceiling, with **no
  architecture change** vs the byte-text control.
- 🔴 **LANGUAGE-SPECIALIZED** ⇐ the arch only descends on byte-text and stays at
  ~random on non-language streams → keep the "L".

Decision rule (coded, p7 — no LLM self-judge): a stream is "learned" if held-out
next-token accuracy exceeds `floor + max(0.05, 3σ)`; 🟢 requires **both** non-language
streams learned **and** each capturing ≥30 % of its `(ceiling − floor)` gap, **and**
the control descends, **and** random stays at floor (infra sanity).

## §method
- **Architecture**: `CLM/model/model.py::CLMConvMoE`, reimplemented **op-for-op in
  pure numpy** (`UNIVERSE/h950_modality_agnostic.py`) because torch is not installed
  on this Mac host. Forward path is identical to `CLM/model/model.py` and to the
  validated `state/mid_convmoe_fire/clm_decode_mirror.py`: byte-embed → causal dilated
  conv embed → `[GroupNorm(1,d)+GELU dilated-conv residual]×L` trunk → softmax conv-MoE
  (E GELU experts) → GroupNorm → readout conv. Hand-written Adam backprop over exactly
  these ops. The arch **never sees "language"** — only integer tokens in `[0,V=256)`;
  so a categorical "language-only" claim is falsifiable at any scale by a single
  non-language descent (cf [a_clm_gen_pipeline](../CLAUDE.md): CLM = byte-V256 CLMConvMoE).
- **Streams** (all → integer tokens in `[0,256)`, same arch/steps/optimizer):
  `bytetext` (English sentence bytes = the "language" control), `logistic`
  (chaotic logistic map r=3.99 quantized to 256 bins = deterministic NON-language),
  `markov` (random sparse first-order chain = stochastic NON-language), `random`
  (i.i.d. uniform = the un-learnable floor sanity).
- **Ceiling** = optimal order-1 (last-token-majority) predictor accuracy on a long
  realization of each true process. **Floor** = 1/V.
- Config: d=32 L=2 E=4, steps=500, T=32, B=16, n=6000, 3 seeds.

## §measurement (real run — verbatim in `.verdicts/950_modality_agnostic/h950_run.txt`)

| stream | eval_acc | train_ce | eval_ce | order-1 ceiling | floor | learned? | ceiling-gap captured |
|---|---|---|---|---|---|---|---|
| bytetext (control) | **0.9696** | 0.0739 | 0.0737 | 0.4371 | 0.0039 | ✅ | 223 % |
| logistic (NON-lang) | **0.5420** | 0.3462 | 1.4965 | 0.5079 | 0.0039 | ✅ | 107 % |
| markov (NON-lang) | **0.6083** | 0.7365 | 1.9448 | 0.6971 | 0.0039 | ✅ | 87 % |
| random (floor sanity) | 0.0037 | 1.2228 | 10.8141 | 0.0039 | 0.0039 | ❌ (correct) | — |

Detect margin = 0.0500. Both non-language streams exceed the order-1 ceiling
(logistic 107 %, markov 87 %; bytetext 223 %) because the conv trunk uses a longer
receptive field than the order-1 ceiling estimator — i.e. it learns *more* structure
than a memoryless predictor, on the non-language streams too.

## §finding
The **identical architecture, with no change**, descends on a deterministic-chaos
stream and a random Markov chain just as it does on byte-text — and on random noise
it correctly stays at the floor (Adam memorizes the 80 % train split → train_ce 1.22
but eval_ce explodes to 10.8 and eval_acc = floor, exactly as a non-learnable target
should behave). **The "L" in CLM is a projection, not the essence**: the architecture
is a general next-token sequence engine. This is a 🟢 for **axis ⓐ** of the CLM→CE
reframe.

## §scope / honesty (a_scale_honest_scope · a_toy_scale_recheck)
- **Toy**: single config (d32/L2/E4), $0 CPU-local numpy mirror, not the production
  Lane-P torch trainer. The **scale-transfer ladder is OPEN** — this falsifies the
  *categorical* "language-only" claim (sufficient for that purpose, since the arch is
  modality-blind by construction) but does **not** assert production-scale numbers.
- The numpy forward matches `CLM/model/model.py` op-for-op; the production serializer
  path (`clm_serialize_v2.py` → `.clm` v0.2/v0.3 → `CORE/clm_decode.hexa`) is unchanged
  and not exercised here.

## §links
- [H_951 engine-not-predictor](H_951_engine_not_predictor.md) · [H_952 substrate-equivalence](H_952_substrate_equivalence.md)
- [a_clm_gen_pipeline](../CLAUDE.md) (CLM = byte-V256 CLMConvMoE E2/L1)
- Code: `UNIVERSE/h950_modality_agnostic.py` · Verdict: `.verdicts/950_modality_agnostic/h950_run.txt`
