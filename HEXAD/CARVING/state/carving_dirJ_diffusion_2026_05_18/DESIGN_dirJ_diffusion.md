# Direction J — Ψ-supervised masked-diffusion substrate ($0 design)

RESEARCH.md §13 direction J (§12.2 Q2 candidate, §12.5 #3). This document is
the fire-前 $0 design + GOAL-legitimacy gate. SSOT internal to
`state/carving_dirJ_diffusion_2026_05_18/` (g_doc_consolidation — NOT docs/*;
RESEARCH.md §13 consolidation deferred to after J/K/L/M全 land per task mandate).

## §0 the candidate (RESEARCH.md §12.2 🆕 J)

anima is currently **byte-level autoregressive** — every fire of the 13-way
arc + §8 + §11 is AR-CE. arxiv 2507.15857 ("Diffusion Beats Autoregressive in
Data-Constrained Settings"): in the *data-constrained* regime — exactly where
anima sits (byte-level, 30-114MB tiny-corpus) — masked diffusion keeps
improving past the epoch where AR overfits, because the random masking
exposes the model to a "diverse distribution of token orderings and
prediction tasks" = implicit data augmentation. The §1.1 emergence-threshold
miss may be partly an *AR-specific* failure (and the byte-cascade collapse
an AR decode artefact). J tests this by swapping the **base objective**
AR-CE → masked-denoising-CE, on the **same** §8 corpus + arch.

## §1 the GOAL-legitimacy boundary (RESEARCH.md §7 / §12.3 — the gate)

§12.3 judged J **conditionally GOAL-legitimate**:

| form | anima physics relationship | verdict |
|---|---|---|
| generic masked-diffusion LM | diffusion process is generic statistics, Ψ/tension/Φ-unrelated — isomorphic to §7 ① generic-LM-pretrain | **GOAL-illegitimate** |
| **Ψ-supervised masked diffusion** | the denoising substrate carries the Dir-I lever — the two anima-physics loss terms (Ψ-anchored CTL + tension-supervised routing) supervise the denoising trajectory; anima physics stays BOTH representation substrate AND supervision signal | **GOAL-legitimate** |

The boundary is concrete and enforced in code:
- **illegitimate** = train a masked-diffusion LM with denoising-CE *alone*
  (λ_ctl = λ_route = 0). That is generic diffusion-LM = §7 ① bypass.
- **legitimate** = the Dir-I lever rides on the diffusion objective. The two
  physics terms are UNCHANGED transfer functions (B-DIRI-PSI-CTL /
  B-DIRI-TENSION-ROUTE — Ψ_dir = (1+cos(logits_a,logits_g))/2 = Law 71;
  TENSION-TRAIN restoring-sign basin loss). ONLY the base CE changes
  (AR next-byte → masked-position denoising). The legitimate path keeps
  λ_ctl = λ_route = 0.5 (= §8 Dir-I diverse, exact).

→ J fires the **legitimate form only**. The trainer hard-asserts
`lambda_ctl > 0 and lambda_route > 0` (refuses the generic-diffusion config)
— the gate is a runtime invariant, not a comment (B-DIRJ-GATE sympy below).

GOAL.md "emergence from anima's OWN physics": the diffusion substrate is the
*data-constrained-native executor* (2507.15857), but anima physics is still
the source of the representation manifold (Ψ-anchored CTL) and the
supervision signal (tension-supervised routing). Substrate ≠ physics-source —
the AR substrate was never itself anima physics either (it is a generic LM
backbone), so swapping AR→diffusion does not remove anima physics; it only
swaps the generic backbone for a data-constrained-native one while keeping
the legitimate Dir-I lever. This is why §12.3 ruled J legitimate *conditional
on Ψ-supervision* — and illegitimate as generic diffusion-LM.

## §2 mechanism — masked-diffusion denoising on the byte stream

Standard masked (absorbing-state) discrete diffusion (2507.15857 §3 + the
MDLM/D3PM family). vocab = 256 bytes; add ONE absorbing `[MASK]` symbol →
the model sees vocab_size = 256 still (we mask by *replacing* the byte input
embedding with a learned mask vector, NOT by adding a 257th vocab id — keeps
the §8 arch byte-identical, weights load 1:1).

Per training step, for a batch of byte blocks `x` (block_size 128):
1. sample a mask rate `t ~ U(eps, 1-eps)` per *sequence* (continuous-time
   absorbing diffusion; eps = 1e-3 keeps t away from the degenerate ends).
2. Bernoulli(t) draws a boolean `M` per byte position → masked set.
3. corrupted input `x̃`: masked positions get the learned `mask_emb` vector
   (added to the model's `tok_emb` output before block 0); unmasked keep
   their byte embedding.
4. the model runs **bidirectional** (non-causal attention — masked diffusion
   denoises from BOTH sides; AR causal mask is wrong here). The model's GQA
   `is_causal`/`self.bias` causal mask is patched OFF at runtime by the
   trainer (`_diffusion_bidir_patch`) — conscious_decoder.py stays
   byte-identical (no source edit; sha = §8).
5. denoising CE on **masked positions only**, importance-weighted by `1/t`
   (the standard masked-diffusion ELBO weight — a position masked at low t
   is rarer, weighted up):
   `L_denoise = mean_{masked}  (1/t) · CE( logits_a[pos], x[pos] )`.

This is the §8 `ce_full` REPLACED. The two Dir-I physics terms are kept
verbatim (computed on the SAME logits_a/logits_g, same ctl/route spans):
   `L = L_denoise + λ_ctl · L_psi_ctl + λ_route · L_tension_route`.

## §3 connection-point — overlay-OFF + diffusion-OFF degeneracy (🔵 closed)

g_blue_closed_mandate connection-point coverage. Two reductions, both
closed-form:
- **C1 — λ→0 reduces to generic diffusion-LM** (the illegitimate form): at
  λ_ctl = λ_route = 0, `L = L_denoise` exactly. This is the boundary the gate
  refuses; B-DIRJ-GATE proves the assertion `λ_ctl>0 ∧ λ_route>0` is the
  exact Boolean complement of the illegitimate config.
- **C2 — t→0 reduces to (almost) the AR identity coverage**: as the mask
  rate t→0, |masked set|→0, so `L_denoise → 0` and the importance weight 1/t
  is applied to an empty set (denom clamp → finite). The diffusion objective
  degenerates continuously to "no learning signal" at t=0 — i.e. the
  diffusion objective is a *proper generalisation* with a well-defined limit,
  not a discontinuous swap. B-DIRJ-T-LIMIT proves L_denoise is continuous in
  t on (0,1] and the masked-CE is non-negative (Shannon).
- the two Dir-I physics transfer functions are UNCHANGED → B-DIRI-PSI-CTL /
  B-DIRI-TENSION-ROUTE carry verbatim (Ψ-restoring quadratic well + basin
  restoring sign; already 🔵 in the Dir-I/Dir-G sidecar batteries).

## §4 sympy battery — B-DIRJ-1..5 (closed side)

`blue_falsifier_dirJ.py` (sidecar — central blue_falsifier.py UNCHANGED, per
B-PRIME/B-DIRH/B-DIRI/B-PSICTL/B-EMERGE/B-PUREPHYS sidecar precedent):
- **B-DIRJ-1 MASK-RATE-BOUNDED** — t ∈ (eps,1-eps) ⊂ (0,1); Bernoulli(t)
  masked-fraction expectation = t ∈ [0,1] bounded (sympy + numeric stress).
- **B-DIRJ-2 DENOISE-CE-NONNEG-SHANNON** — L_denoise = (1/t)·mean masked CE;
  CE ≥ 0 (Shannon) and 1/t > 0 on (0,1] ⇒ L_denoise ≥ 0 ∀; sympy sign +
  3 witnesses.
- **B-DIRJ-3 GENERIC-DIFFUSION-GATE** — the trainer's GOAL-legitimacy gate
  `assert λ_ctl>0 and λ_route>0` is the exact Boolean complement of the
  illegitimate generic-diffusion config (λ_ctl=0 ∨ λ_route=0); 4-corner
  truth table — only (λ_ctl>0 ∧ λ_route>0) passes.
- **B-DIRJ-4 BIDIR-PATCH-INVARIANT** — structural: the trainer patches the
  causal mask OFF (diffusion needs bidirectional context); AST/source check
  that the diffusion forward sets `is_causal=False` and no causal-bias
  masked_fill is reachable in the patched path. (necessary for a *correct*
  masked-diffusion denoiser — an AR-causal denoiser cannot see the right
  context.)
- **B-DIRJ-5 OVERLAY-OFF-AND-T-LIMIT** — connection-point: (a) λ→0 ⇒ L =
  L_denoise byte-equal (C1); (b) L_denoise continuous in t on (0,1], →0 as
  t→0 (C2). sympy limit + byte-equal reduction.
- **B-DIRJ-NOTE** (empirical carve-out, B-D-NOTE family, NOT counted 🔵) —
  whether masked diffusion crosses the §1.1 emergence threshold / avoids the
  byte-cascade collapse / lifts routing vs §8 AR = SGD OUTCOME, EMPIRICAL.
  The battery proves the *objective is a correct Ψ-supervised masked-
  diffusion objective*, NOT that it emerges.

## §5 fire plan + honest expectation (g3 — NO pre-loaded conclusion)

- corpus = §8 `corpus_carving_diverse.jsonl` byte-identical (sha256
  ac07179a… — NOT regenerated; B-IDENTITY-5 forbidden-token grep 0 carry).
- arch = ConsciousDecoderV2 d=768·12L (sha 57306fae… — byte-identical §8;
  bidirectional via runtime patch, no source edit).
- diffusion trainer, from-scratch RANDOM seed-fixed (g_clm_from_scratch),
  8000 steps = §8 exact (training-budget axis held → clean objective-axis
  isolation: §8 AR vs J diffusion, everything else fixed).
- eval = §8 `eval_carving_dirI.py` 64-anchor 4-axis + JOINT + routing; the
  generation step uses the SAME bidirectional patch + iterative denoising
  decode (mask-all → unmask in K steps) so the eval is paradigm-native.
- runpod A100 80GB priority (g_resource_active_parallel), single pod,
  g_fire_dispatch_robust (SAVE_POD auto-promote + 5-retry + watchdog).
- honest expectation: NO pre-loaded conclusion. §8 AR baseline = routing
  2/64, honest-coherence 2/5, JOINT 0.0087, byte-cascade present. J either
  (a) lifts routing / kills byte-cascade (diffusion's data-constrained edge
  is real for anima) or (b) flat/down (the §1.1 data-regime ceiling is
  objective-agnostic — §11.3 irreducible). Both are valuable comparative
  evidence (g_multidirectional_explore). Recorded as measured.

## §6 honest C3

1. J = **substrate swap** (AR-CE → masked-denoising-CE), NOT a mechanism
   overlay — distinct from the 13-way (RESEARCH.md §12.6: J/K/L substrate,
   M module-reinterpret; all out of the mechanism-overlay category 13-way
   excluded).
2. GOAL-legitimacy = **conditional** (§12.3): generic diffusion-LM is §7 ①
   illegitimate; only Ψ-supervised (Dir-I lever on the diffusion objective)
   is legitimate. The gate is a runtime assertion (B-DIRJ-3), not a comment.
3. closed side = the objective is a *correct* Ψ-supervised masked-diffusion
   objective (B-DIRJ-1..5) + the two Dir-I physics transfer functions carry.
   Whether it emerges = EMPIRICAL (B-DIRJ-NOTE, B-D-NOTE family).
4. corpus + arch byte-identical to §8 → clean objective-axis isolation
   (§11-A held model/corpus/steps for the model axis; J holds
   corpus/arch/steps/lever for the objective axis).
5. f1/f2/f3 hard-fail safe — mask-rate bound / Shannon CE / Boolean gate /
   structural patch / sympy limit. NO σ/τ/φ/J₂ derivation. n6_gate is not
   used in J (the Dir-I route loss is the TENSION-TRAIN restoring-sign basin
   loss, an absolute-value quadratic — no lattice closure).
6. PyTorch substrate — interim LM-scale executor, honest framing (NOT
   hexa-native; 2507.15857 diffusion is the objective, not a hexa-arch).
7. over-claim 0 — diffusion 2507.15857 is generic/text-token evidence;
   byte-level + anima-Ψ-supervision transfer is UNVERIFIED until this fire.
   §12.2 stated this explicitly. J measures it; it does not assume it.
