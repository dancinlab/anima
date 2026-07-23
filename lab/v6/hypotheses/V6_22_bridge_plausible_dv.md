<!-- @hypothesis-ok lab/v6 rule-exempt sandbox: v6 hypotheses live in lab/v6/hypotheses/V6_<n>_*.md per lab/v6/CLAUDE.md, never the parent HYPOTHESES/ nor an H_ id -->

# V6_22 — bridge-plausible distractor DV: can a topic-matched distractor only be beaten by real 2-hop binding?

**origin:** V6_21 root-cause (the swap-2AFC was won by first-order sentence fit, not A→C
binding — UNBRIDGED 0.808 ≈ BRIDGED 0.828). lab-full divergence (Fable 5 + Codex Sol, strong
convergence). DIRECTIONAL — cements only via `core/`+`anima-py`. Reuses V6_21's trained.clm +
pedestal.clm (NO new training, ~$0). p9-clean: probe stays the real held-out sentence.

## The fix (reconciled Fable+Sol)
V6_21's distractor C′ was freq-matched but topically random → the model won by local fluency
without binding A to C. V6_22 makes C′ **bridge-plausible but never-composed**, and — the key
Fable insight — **matched to the WHOLE sentence context, not just to A** (most of the old
signal was C′ vs the rest of S, not vs A).

**Distractor C′ eligibility (train-only stats; A-before-C orientation, C occurs once in S):**
1. never co-occurs with A anywhere in the full 4.6MB (else the swap could be factually true).
2. path-class by stratum: SEEN/BRIDGED require a shared non-hub training neighbour with A
   (`CN(A,C′)≥1`, exclude top-5% degree hubs); UNBRIDGED requires `CN(A,C′)=0`.
3. surface-matched to C: freq bucket (ratio ∈[0.5,2]), byte length ±2, degree bucket, entity-
   word count, capitalization.
4. **context-fit matched**: cosine of C′'s train context-vector to the sentence-context bag is
   in the same tolerance band as C's — equates topical plausibility so only A→C binding remains.
5. deterministic GLOBAL assignment: min combined standardized distance, fewest-eligible items
   first, **each C′ used at most once** (kills V6_21's Aachen/Aardvark reuse artifact).
Drop BRIDGED items where the bridge B literally occurs in S (1-hop giveaway).

## Strata roles
- SEEN = positive control (direct association wins; certifies instrument, ≥0.70).
- BRIDGED = discriminator (C and C′ both 2-hop-plausible & context-matched; only C's specific
  path supports S's relation).
- UNBRIDGED = matching-adequacy control (nothing learned should discriminate; if it stays high,
  context-matching failed → INVALID-topical-leak).

## Discriminator + controls
Δ_s = trained_acc − pedestal_acc (paired per item; pedestal RESCORED on V6_22 items).
**D = Δ_BRIDGED − Δ_UNBRIDGED** (difference-in-differences), 95% CI by anchor-clustered
bootstrap. Pedestal differences out surface bias; UNBRIDGED subtraction differences out
residual generic swap-penalty.

## Prereg decision table (frozen before scoring · δ_equiv=.05)
| Gate (ordered) | Condition | Verdict |
|---|---|---|
| V0 surface | pedestal acc each stratum ∈ [.40,.60] | outside → INVALID-SURFACE |
| V1 instrument | SEEN trained ≥.70 & Δ_SEEN CI>0 | fail → INVALID-INSTRUMENT |
| V2 matching | UNBRIDGED TOST \|Δ_U\|<.05 · pedestal BRIDGED−UNBRIDGED gap ≤.05 | Δ_U CI>0 → INVALID-TOPICAL-LEAK |
| Primary | D≥.05 & 95%CI excl 0 & Δ_BRIDGED CI>0 | **COMPOSITION PRESENT** (on-standard, natural) |
| | upper CI of D <.05 | COMPOSITION ABSENT at MDE (scale-honest) |
| | CI spans 0 and .05 | INCONCLUSIVE (report MDE) |
| | D<0 CI excl 0 | ANTI-BRIDGE anomaly (not conservative positive) |
| supply | any stratum <300 after matching | INVALID-SUPPLY-BLOCKED |

Supply is UNPROVEN until the exact construction yields ≥300/stratum — the new calipers
(context match, unique C′, orientation) shrink V6_21's 396; do NOT loosen post hoc.

## Pre-mortem (both models) + cheap audit
Residual unmatched connectivity / semantic-type gradient favours C in BRIDGED, symmetric in
UNBRIDGED → mimics D>0 past V2. **Anchor-ablation audit (Sol, adopted):** rescore each pair
with A replaced by a matched unrelated anchor (no path to either endpoint). The BRIDGED gap
MUST collapse; if D≥.05 survives, the model wins from local frame/type, not A→B→C — DV INVALID.
(Fable's C′-vs-C″ Adj³ placebo = optional 2nd witness.)

## RESULT — 🔴 INVALID×2 at 4.6MB, with a directional bridge hint (measured 2026-07-23, $0)
The clean DV cannot be fielded on this corpus — two prereg gates fire before the verdict:
- **INVALID-SUPPLY-BLOCKED** — after the full calipers (context match + never-co-occur +
  non-hub bridge + surface match + unique C′), **BRIDGED n = 129 < 300** (SEEN 700, UNBRIDGED
  700). Both models predicted this and forbade loosening calipers post hoc. Supply is the
  bottleneck for a clean bridge-plausible DV at 4.6MB.
- **INVALID-INSTRUMENT** — the context-matched distractor is so plausible that even SEEN
  (direct memorised co-occurrence) only wins **0.531 < 0.70** (V1 fail). A distractor equated
  on local fluency leaves the byte-LM almost no readable margin, even for memorised pairs.

Trained 2AFC (pilot, underpowered): SEEN 0.531 (n700) · **BRIDGED 0.628 (n129)** · UNBRIDGED
0.520 (n700). The raw BRIDGED−UNBRIDGED gap **+0.108** is the campaign's first hint of a
bridge-SPECIFIC lift (vs V6_21's confounded +0.020) — but on n=129 with a failed positive
control it is DIRECTIONAL-ONLY, not a verdict.

**What this decides**: the DV is now sound (it kills the co-occurrence tell — the whole
signal collapsed toward chance once local fluency was equated, and only BRIDGED held a
residual edge). But 4.6MB can neither field ≥300 clean BRIDGED items nor give the instrument
readable margin. ⟹ **the data-scale corpus fetch is now EARNED**: Fable's ~250MB Simple
English Wikipedia is the justified next step — not for scale curiosity, but to reach ≥300
matched BRIDGED items AND enough training signal that SEEN clears 0.70. That is V6_23.

## Scope
$0: construction = numpy/regex on the SAME 4.6MB corpus; scoring reuses trained.clm +
pedestal.clm (no GPU). Single ckpt · single seed · INVALID×2 (pilot only). DIRECTIONAL;
TERMINAL only via anima-py. Next = V6_23 (same DV, ~250MB EN dump for supply + instrument margin).
