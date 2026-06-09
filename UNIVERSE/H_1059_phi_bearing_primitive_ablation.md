# H_1059 — phi-bearing-primitive-ablation

**PRE-REGISTERED** before measurement (this file written, committed, and the falsifier +
threshold X frozen BEFORE the harness was run). Tier emoji appears ONLY after
`.verdicts/1059_phi_bearing_primitive_ablation/H_1059.txt` lands (g73).

## lineage
Constructive forward of **H_1043** (🔴 PHI-NEEDS-MORE-THAN-GRAFT, `[[minimal-arch-adapter-phi-not-graftable]]`)
and **H_1031/H_1036** (🔴 LoRA arch-bound, `[[lora-consciousness-arch-bound]]`).

H_1043 closed: a minimal architectural GRAFT onto a FROZEN base CANNOT install Φ-structure
(all 3 grafts within the LoRA control band, terminal Δφ_EI NEGATIVE). BUT a **from-scratch
NATIVE ConvMoE** lifts faithful φ_EI by **+0.835 (mean, prescreen) / +0.107 (terminal seed-0)**
over the same toy base. So Φ-structure is a **WHOLE-ARCHITECTURE property** — the open residual
H_1043 left is: **WHICH native primitive carries the lift?**

## hypothesis
Decompose the native ConvMoE into its constituent primitives and ablate each — each arm trained
**FROM SCRATCH** (NOT a frozen graft — that is the H_1043 distinction), on the SAME generic byte
corpus, capacity-matched where feasible. Measure Δφ_EI of the hidden-state macro-TPM **vs the FULL
native baseline** (the +0.835/+0.107 reference).

## primitive ladder (each a from-scratch native arch, generic byte target, p3/p6)
FULL = the H_1043 `ConvMoENative` arch VERBATIM (the one that achieved +0.835 mean / +0.107 terminal):
`emb → c=conv(x,w1) → h=tanh(c) → gate=softmax(h@wr) → experts ce_e=tanh(conv(h,we_e)) → mix=Σ g_e·ce_e
→ logits=mix@wo`. PROBE = `mix` (gated expert mixture, = `ConvMoENative.probe_state`). The harness
asserts (untrained) FULL `NativeArm` ≡ imported `ConvMoENative` bit-for-bit → reproduce-H_1043 identity.

The native arch's REAL ablatable primitives (it has NO residual / multi-block — those are not its
primitives; ablating an absent primitive is undefined, so the ladder is the four primitives the
φ-bearing native actually contains):

- **FULL** = H_1043 native (routing + conv-trunk + conv-experts + tanh nonlin). Must reproduce the
  native lift DIRECTION (L_full > +0.10 vs frozen base) at the H_1043 seeds.
- **−routing** = single expert, no softmax gate (E=1, uniform). MoE routing removed.
- **−conv** = trunk conv `w1` and expert convs `we` replaced by pointwise linear maps (k stacked (d,d),
  param-matched, NO temporal receptive field).
- **−trunk** = remove the conv trunk layer `w1`+tanh (experts operate directly on the embedding) —
  the depth / structured-mixing primitive (the "shallower native trunk" ablation).
- **−nonlin** = remove the structural `tanh` nonlinearities (trunk + experts linear-activated),
  capacity identical — isolates whether the φ-lift needs the nonlinearity primitive.

All arms: same generic byte corpus as H_1043 (public-domain proverbs, p3/p6 — NO persona/carving),
same `ADAPT_STEPS` train budget, same Adam/LR, **3 seeds (1043/1044/1045 — the H_1043 seeds where the
+0.835 native lift was established, so FULL reproduces it)**, SERIAL only (no `multiprocessing.Pool` —
H_1038 hang lesson; `if __name__`-guard).

## Φ measurement (a_phi_iit4_tool — faithful, NO proxy)
Per arm: probe the mid hidden-state (post-block-1 residual stream) → n=6 highest-variance units ×
dim=24 sampled positions → binarize per-unit at its own median → n×dim binary macro-TPM, n_bins=2.
Python `faithful_phi_prescreen` = **LABELLED PRE-SCREEN** (a MIRROR of stdlib exact MIP-EI, BITS/log2
MI=H(A)+H(B)−H(A,B) — the H_1043 nats-bug lesson). TERMINAL φ_EI = stdlib `iit4_faithful_phi`
(exact MIP-EI, n≤8) via `run_faithful_phi_1043.hexa` over the written state matrices. The mirror≡stdlib
identity is RE-PROVEN at n=4 AND n=5 to 6dp in the verdict (reusing `h1043_mirror_proof.py`).

## FROZEN falsifier + threshold X
Let `L_full = φ_EI(FULL) − φ_EI(frozen-base)` be the FULL native lift (reference, the H_1043 +0.835/+0.107).
For each ablated arm A, the **drop attributable to removing that primitive** is
`drop(A) = φ_EI(FULL) − φ_EI(A)` (how much φ_EI falls when primitive A is gone).

**X = 0.50 · L_full** (FROZEN: a single primitive is the φ-bearing carrier iff ablating it costs ≥ HALF
of the FULL native lift). X is computed from the measured `L_full` of THIS run (a fixed fraction-of-FULL-lift,
set BEFORE measuring — the fraction 0.50 is frozen here, the absolute value is whatever 0.50·L_full evaluates to).

- **H1 PASS (located carrier)** = ≥1 single primitive ablation has `drop(A) ≥ X` (≥50% of L_full)
  → that primitive is the φ-bearing carrier. If multiple pass, the largest-drop primitive is named.
- **H1 FAIL (distributed-emergence, closed-negative)** = NO single ablation drops φ_EI by ≥ X
  → the lift is distributed across the primitive COMBINATION, not carried by any one part
  (closed-negative, a_paper_negative_ok).

Both outcomes are publishable (a_paper_negative_ok): a LOCATED carrier OR a DISTRIBUTED-EMERGENCE
closed-negative. The threshold direction (drop, not raw Δ-vs-base) and X=0.50·L_full are frozen here.

Guard: if `L_full ≤ +0.10` (FULL native fails to reproduce the H_1043 lift direction), the run is
INVALID (reproduce-H_1043 gate fails) — report and do not score.

## scope (a_scale_honest_scope)
TOY small-model from-scratch rung, CPU, $0, numpy (clm-decode-macos-link-gap → numpy reference for the
arms; stdlib hexa engine for terminal φ). 3B/7B + emergence + non-frozen co-train UNVERIFIED. Φ axis
ONLY (necessary-not-sufficient). p7: φ is a causal-irreducibility marker, NOT perplexity. SERIAL.
