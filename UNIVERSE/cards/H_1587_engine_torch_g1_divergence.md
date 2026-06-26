# H_1587 — engine vs torch G1 divergence = MEASUREMENT-METHOD (sampler) artifact

**Question (a_break_the_wall — classify the wall before accepting it):** the py 2-production engine
measured **G1 RECOMBINATION = FAIL** on ByteGPT-303M h1129, while the original torch H_1129 reference
is **🟢 GREEN**. One must be wrong — which, and why?

## Verdict: 🟠 DIRECTIONAL — engine FAIL is a SAMPLER-METHOD artifact, NOT a model property; torch 🟢 stands.
(ad13 diagnostic, summer pool, torch 2.11.0 + py engine + h1129.bin/h1129c_best.pt.)

- **CHECK4 weights:** h1129.bin == torch state_dict, **max|diff| = 0.000** → NOT a ckpt-mismatch.
- **CHECK2 forward:** engine `bg_forward_last` == torch forward — identical argmax + identical top-5,
  max|logit diff| ~2e-5 (fp32 ULP) → engine forward byte-faithful, NOT a decode-bug (also clears the
  German-output decode-integrity concern for h1129).
- **CHECK3 / ladder (3-way):** arm A torch GPU bf16 = GREEN, arm B torch fp32 CPU = GREEN, arm C engine
  fp32 CPU = FAIL. A==B==GREEN proves the GREEN is not bf16/GPU/precision-dependent; the ONLY variable
  that flips GREEN→FAIL is the **sampler**: `core/bytegpt_decode.{py,hexa}::_topk_sample` uses a custom
  **xorshift32 PRNG + inverse-CDF** while the torch H_1129 harness uses **torch.multinomial +
  Generator(7)**. Same params (top_k=40, temp=0.7, seed 7), different RNG walk → equally-coherent but
  different tokens. Recombination lift is a sparse single-seed event, so the sampler walk flips
  GREEN↔FAIL on an identical model.

## Implication
ALL engine-native G1 FAILs declared *by divergence from a torch GREEN* (h1129, clm303, deep-ConvMoE)
were sampler-divergent / DIRECTIONAL, NOT terminal — they must be **reference-matched** before any
engine-native G1 PASS/FAIL is terminal. Even the torch GREEN is single-seed-fragile (arm A clears
only at k=5, arm B at k=3/4/5) → the G1 metric itself wants seed-robustness.

## Resolution → H_1588
H_1588 implements the fix (multi-seed reference-matched metric over {7,4302,4303}, majority GREEN,
symmetric torch+engine) and re-scores: **h1129 = GREEN 3/3 (torch ref)** confirming the 🟢 is robust;
**clm303_clean = FAIL 0/3 (genuine, not sampler)**. See `cards/H_1588_g1_multiseed_refmatch.md`.

**wired:** DIRECTIONAL (diagnostic; no core change). **artifacts:**
`state/1587_engine_torch_g1_divergence/` (VERDICT.md · g1_ladder_3way.py · threeway_diag.{py,out}).
