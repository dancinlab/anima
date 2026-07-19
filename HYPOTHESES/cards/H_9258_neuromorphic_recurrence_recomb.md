# H_9258 — Recurrence/spiking breaks the RF-decay recombination wall (neuromorphic substrate lens)

**tier**: 🔬 REGISTERED · $0 recurrent CPU proxy pre-check firing (hardware AKD1000 = follow-on)

## Claim
The G1 recombination wall — a distal concept D established before a gap is lost at the generation point
(receptive-field decay) so it cannot be recombined with a recent concept R — is **architecture-specific to
feedforward conv, NOT fundamental**. A substrate with native temporal binding (recurrence / spiking assemblies)
should hold D active across the gap and route it at emit, cracking the swap-margin where the frozen feedforward
303M byte-LM's read-side lanes (parametric🧱·pointer-cache🧱·trained-xattn🟡·swap-contrastive🟡) all failed.

## Why (substrate-first · a_no_llm_frame_trap)
The 4 frozen-readout lanes measured this session showed concept identity is LINEARLY PRESENT in pooled final
states but not transferably MAPPABLE to target-byte logits at the emit point — a bounded ±τ re-ranking on a
frozen feedforward conv can't route distal D. Recurrence/spiking natively persist an assembly across a gap
(the exact mechanism a feedforward RF lacks). If recurrence cracks the swap-margin, the wall is conv-specific.

## Test ladder
1. **$0 CPU recurrent proxy** (pre-hardware): toy recombination task (D-block · GAP≥RF · R-block · emit
   D-dependent byte). Train a small GRU/LSTM vs a matched feedforward-conv baseline; swap-margin Δ = does the
   model prefer D-dependent match over Dp-swap? CRACK = recurrent Δ>0 (CI excl 0) while feedforward Δ≈0 →
   recurrence breaks the wall. Controls: gap-length sweep (RF decay curve), shuffle, matched param count.
2. **AKD1000 neuromorphic** (Fable design pending · pi5-akida): map/analog on 1st-gen Akida if genuine temporal
   binding is expressible; else the CPU proxy is the substrate-lens verdict (a_scale_honest_scope: toy≠303M).

## Verdict
(pending — proxy firing)

## Scope honesty
Toy proxy tests the MECHANISM (recurrence vs feedforward on distal binding), NOT the 303M byte-LM directly
(a_toy_scale_recheck). A proxy CRACK is DIRECTIONAL evidence the frozen-conv wall is architecture-specific;
it does NOT by itself wire into anima. Separate from the fork-A frozen-readout ledger (H_9235).

---

## ⚠️ SUPERSEDED by H_9259 (measured 2026-07-10 · 🧱 KILL)

The step-1 proxy AS WRITTEN here has 3 confounds: (a) `GAP>=RF` makes the conv floor a *theorem*, not a measurement (rigged); (b) training the GRU moves 2 levers at once (recurrence + training) vs anima's *frozen* trunk; (c) it targets RETENTION, which the session already showed is NOT the bottleneck (mean-pool D-probe 0.95; and H_1000 T1 d=38.7 — recurrence wins retention trivially). **H_9259** corrects all three (XOR target = provable additive floor · RF≥T de-rigged · frozen trunk + linear ridge readout the only fit part · ρ=0 ablation = memory-without-products) and MEASURED it: **🧱 KILL — every UNTRAINED reservoir arm floors on held-out XOR even with retention forced to Dprobe=1.000, while oracle-bitprod=1.000.** The conjunction must be TRAINED into the substrate (γ H_1840; cf. H_1003 curriculum-trained GRU cracks XOR where H_1000 direct-trained fails). 1st-gen AKD1000 (feedforward op envelope, H_848) ruled out as an untrained G1 lever = **distraction**. See `cards/H_9259_g1_recurrent_basis_vs_retention.md`.
