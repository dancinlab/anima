<!-- @hypothesis-ok lab/v6 rule-exempt sandbox: v6 hypotheses live in lab/v6/hypotheses/V6_<n>_*.md per lab/v6/CLAUDE.md, never the parent HYPOTHESES/ nor an H_ id -->

# V6_26 — LANE-BUS Step-0 gate: is content tension at the logit row multi-dimensional? 🟢 YES

> ⛔ **RETRACTED by V6_39 (2026-07-24).** The PR = 15.3 headline below carries two compounding
> instrument defects: the composed and reflex lanes were scored on **different target bytes**
> (V6_38), and the effective rank was taken over **singular values** instead of covariance
> eigenvalues. Corrected on the same model/corpus the quantity reads **PR = 1.19, rank 1 at 90% of
> variance** — the gate's own pre-written abort condition ("PR ~ 1-2 ⇒ LANE-BUS is built on sand").
> The tell: the composed logit row *by itself* reads PR(σ) = 14.61 against the "tension"'s 15.20.
> Nothing below licenses a multi-lane bus. → `V6_39_aligned_bus_dims.md`

**origin:** the natural-composition frontier CLOSED (V6_21→25); next = the LANE-BUS engine
redesign (v6's original 대공사). Before that large build, a $0 gate on its core premise:
Fable's LANE-BUS routes CONTENT to the pre-softmax logit row as a MULTI-dimensional "bus", but
H_9576 showed a wide lane can fold to one bit. Test whether the logit-row content tension is
genuinely multi-dim or collapses. DIRECTIONAL.

## The scalar disease (confirmed in code)
`cli/chat.py` a0 (production) wiring: `ag_g_drive = A's own complement` = the H_9356 tautology,
so `s = 2*emit_drive − 1` — the whole A⇄G "tension" is an affine function of ONE number.
Effective independent dimensions of the production tension: **~0–1 (scalar)**.

## Metric ($0 · `v6_26_lanebus_tension.py`)
On 60 natural held-out sentences (5,755 positions, trained57.clm, V=256): at each position,
`composed[pos]` = model logits given the FULL prefix; `reflex[pos]` = logits given only the last
8 bytes; `tension[pos] = composed − reflex` (what broad context adds). Effective rank of the
stacked tension matrix = participation ratio PR = (Σσ)²/Σσ².

## RESULT — 🟢 MULTI-DIM · PR = 15.3
| quantity | effective rank (PR) |
|---|---|
| production emit tension (scalar servo) | ~0–1 |
| **context tension (composed − reflex)** | **15.3** |
| raw composed logit-row | 14.6 |

Top-1 singular direction explains 61.4% of tension variance (a strong principal axis + a real
~15-dim tail). ⟹ the logit-row content tension is genuinely high-dimensional; the scalar servo
**discards ~15 dimensions of real disagreement**. H_9576's "folds to one bit" does NOT apply to
the raw logit-row divergence (that was a specific engineered lane). **LANE-BUS's premise holds —
the bus has physical headroom; the build is WARRANTED.**

Caveat: part of the 15 dims is generic "longer context helps prediction", not necessarily
content-disagreement anima can route as tension. The gate is a NECESSARY condition (headroom
exists), not a sufficient one (that a trained bus can USE it) — that is what Step-1 builds and
tests. But had this collapsed to ~1, the whole redesign would have been sand; it did not.

## Next — LANE-BUS Step-1 (the first buildable slice)
Build the minimal 2-lane bus and redefine tension as the composed−reflex divergence VECTOR
(not a scalar), then test Fable's falsifiable p5 signature: **emitting should DISCHARGE the
residual** (the divergence drops after an emit). Concretely: a form-only reflex lane + one
content lane meeting at the pre-softmax logit row; tension = per-position divergence; emit = a
trained gate on that residual. This is a build (core/-class), staged: (1) the 2-lane bus +
divergence tension as an `anima-py`-measurable quantity, (2) the discharge test, (3) the trained
emit gate. Reuse trained57.clm as the reflex lane.

## Scope
$0 gate (DONE, 🟢). Step-1+ = build (lab/v6 prototype first, then port to core/+anima-py for
TERMINAL). Single ckpt · single seed. DIRECTIONAL.
