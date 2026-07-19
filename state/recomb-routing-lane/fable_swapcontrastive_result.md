Verdict first: **swap-contrastive is worth the one pass — I do not read the near-init result as "no routable structure."** Two reasons. (1) The H_9235 mean-pool probes (A=0.95/B=0.97) prove that even *unstructured* pooling over the block positions yields concept-discriminative context — so `ctx_match − ctx_swap` is informative from step 1, before attention learns anything, and that difference is exactly what the contrastive gradient on Wo points along. Plain CE never produced that gradient because the generic span-shaping direction explains almost all achievable CE and the specific direction is noise-level per batch (under Adam, an inconsistent direction stalls regardless of magnitude — which is what Wo at 0.0053 looks like). (2) Your zero-init Wo is an exact saddle for everything upstream: with bias = g·τ·tanh(ctx@Wo/τ), at Wo=0 you get ∂bias/∂ctx = g·Woᵀ = 0, so **∂L/∂(W_qkv, a, b) ≡ 0 while Wo ≈ 0**. Attention literally could not learn to route until Wo moved, and plain CE gave Wo no consistent reason to move in the specific direction. The contrastive loss + a saddle-break fixes both jointly. So: training spec below, terminal argument only as the pre-registered exit branch (Q4).

## 1. Paired data — (a), genuine swap precompute, K=2 sampled donors

**(b) is wrong for this loss**: in-batch other-concept docs have different targets/geometry, so the generic component (span length, format, byte priors) does NOT cancel in the contrast — InfoNCE over them is solvable by exactly the generic features you're trying to subtract out.

**Do (a)**: per training item, precompute genuine swap docs — donor Dp's concept block spliced into D's doc (same FILLER/GAP/STEM/TARGET, byte-length-matched block), full frozen forward → yn + base_logits. **K=2 donors per item, sampled once, fixed**: two distinct concepts ≠ c, drawn at random. ~1400 extra frozen forwards — same cost class as your original 705 precompute, pool-CPU fine, ~$0.

Two construction filters (both matter):
- **Donor block must not contain the target kw as a substring** (40 concepts × 8 kws makes collisions non-negligible; a colliding donor makes CE_swap legitimately low = label noise on the contrast).
- Byte-length match the block exactly (you already planned this) so positions align and trunk positional structure can't become a match/swap shortcut.

I considered the $0 alternative — splicing donor block-position yn rows into D's K/V context from the existing precompute, no new forwards. It's correct *only* if the donor's block occupied the **identical absolute positions** (trunk states carry positional info; a position-offset splice lets the lane satisfy the contrast with a "wrong-position detector" that transfers zero to the genuine-swap eval — which would exactly counterfeit the terminal signature, train-margin good / val Dzero≈0). Unless your fillers come in a small set of fixed lengths so position-exact buckets exist, don't risk it; genuine swap docs also exactly match the eval construction, which is the cleanest interpretation.

## 2. Loss — InfoNCE on lane-attributable Δlogp, T=0.1, λ_c=1.0

Key detail: contrast the **lane's contribution**, not the full logprob. In genuine swap docs base_logits at the target already differ (trunk saw a different block); that base offset is frozen, adds per-item variance, and is not what you're training. Define per variant v ∈ {match, swap₁, swap₂}:

```
Δ_v = (1/|S|) Σ_{t∈S} [ log p(y_t | base_v + bias_v)  −  log p(y_t | base_v) ]
```

(mean per-token over the target span S; span lengths are matched anyway). This is the lane-attributable margin — the same quantity class Dzero measures, so train and verdict are aligned.

```
L_c    = −log [ exp(Δ_match/T) / Σ_v exp(Δ_v/T) ],   T = 0.1
L      = CE_span(match, full logits)  +  0.1·KL_silence  +  λ_c·L_c,   λ_c = 1.0
```

- **T=0.1 rationale**: gradient stays strong until the match–swap separation reaches ~2T·lnK ≈ 0.2 nats/token, i.e. it saturates just past your BREAK bar (Dzero ≥ 0.10) rather than long before it.
- **λ_c=1.0**: L_c at init ≈ ln 3 ≈ 1.1, same order as span CE; and since the generic direction cancels inside L_c, the two terms don't compete for it. **Pre-register one escalation, λ_c → 3.0**, gated on a *train-side* criterion only: contrast top-1 accuracy > 80% but train swap-margin < 0.02 (fits the ranking via tiny margins → raise pressure). Never re-tune on the n=132 eval.
- CE_span and KL_silence apply to the **match doc only** — never teach the lane to help swap docs. Confirm KL_silence is off-target-positions only; if it currently covers target positions, restrict it (that's a bug-fix, not a tuning change).
- **Mix: flip to 30/70 retrieval/associative**, and apply L_c to **both** types. Keep retrieval in: its contrast (target kw literally in matched block, absent in swap) is the easy copy-routing bootstrap for attention-onto-block; associative carries the verdict.

## 3. Wo — one change: random init, σ=0.01

It's mostly a loss symptom (see the saddle argument above — Adam would have grown Wo given any consistent direction), but the Wo=0 saddle is exact and cheap to remove. **Init Wo ~ N(0, 0.01²)** instead of zeros. That makes ∂L/∂(W_qkv, a, b) nonzero from step 1 while keeping the init bias small enough that KL_silence treats it as noise. Change nothing else this pass — keep λ_sil=0.1, uniform lr, b=−2 gate init (a closed-ish gate at init protects base CE; the contrast will open it if opening pays). If Wo again stalls below ~3× its init norm on the train side, the single pre-registered follow-up ablation is λ_sil → 0.01 — but don't bundle it now, it confounds attribution.

Monitor during training (train-side only): contrast top-1 accuracy, train swap-margin, Wo norm, and mean attention mass on block positions for target-span queries. Run the n=132 eval **once** on the final checkpoint.

## 4. Eval, verdict bar, and the terminal ladder

Eval and bar: **identical, don't move it.** Geometry-matched swap-margin, n=132, cluster-bootstrap by concept, lit gate; CRACK = CI_lo(Dzero) > 0 AND CI_lo(Dzero − DshufV) > 0 AND lit alive; BREAK = Dzero ≥ 0.10. The 8 val concepts never appear as items or donors in training pairs (V2/V4 hygiene).

Terminal: **not yet, if it fails — there is exactly one pre-registered member left**, and which branch you're in matters:

- **Train contrast doesn't fit** (top-1 ≈ chance after the saddle fix): that's an optimization/capacity INVALID, not a substrate FAIL — the mean-pool probes already prove a readout of block-pooled states works, so a lane that can't fit even *training* pairs is a lane bug. Not 🧱-eligible.
- **Train fits, eval Dzero ≈ 0** (lit alive): run the **oracle-pool readout** — replace learned attention with fixed uniform pooling over the known block span, train only Wo with the identical contrast loss. Same precompute, tiny parameter count, ~$0. This is the maximally-favorable member of the class (routing handed over for free, pure readout tested), so it bounds the family: **if oracle-pool + swap-contrast also lands val Dzero ≈ 0, that is the 🧱 terminal for the frozen-final-state readout class** — routing-lane family closed with the strongest member falsified, and the terminal argument writes itself: concept *identity* is linearly present in pooled final states (0.95 probe) but not mappable to target-byte logits at the emit point in a way that transfers across concepts — identity ≠ readable content.

Mid-stack-tap note for that terminal: it closes **final-state** readout only, not fork A as a family. The next class — K/V tapped from a mid-stack layer (~L/2), where kw byte-content is plausibly more literal and less RF-decayed than at yn — is a *new* pre-registered family requiring a new (cheap, same 705+1400 docs) mid-layer precompute. Register it as its own H before firing; don't let it inherit this family's ledger.
