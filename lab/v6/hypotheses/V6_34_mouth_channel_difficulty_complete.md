<!-- @hypothesis-ok lab/v6 rule-exempt sandbox: v6 hypotheses live in lab/v6/hypotheses/V6_<n>_*.md per lab/v6/CLAUDE.md, never the parent HYPOTHESES/ nor an H_ id -->

# V6_34 — the MOUTH/EMIT channel is difficulty-complete: only prediction-aligned (p7) signal survives

**origin:** V6_31–33 closed the AGENCY wedge and suggested a general law ("orthogonal faculties die").
lab-full (Fable+Sol) BOTH reframed it as OVER-GENERALIZED: `tau` is a projection of mouth logits, so
no tau experiment can falsify a UNIVERSAL orthogonality claim — it can only test the narrower
**mouth-channel sufficiency wall**: conditioned on instantaneous prediction-difficulty and its
history, does any recurrent linguistic-CONTENT channel add usable info to the natural emit decision?
DIRECTIONAL ($0 laptop, reuses v6_33 cache/estimator).

## Design (reconciled: Sol dual-register + conservative residualization · Fable magnitude cut)
Content packet `r_t = tau_t − g(x_t, NLL_t, pos_t)` (quadratic ridge, TRAIN-only fit, no emit/cmd —
strips linear+quadratic difficulty AND surprise). Dual-register gate: **X+CONTENT** = a difficulty
register (DRIVER, accumulates x_t) PLUS a separate content register (accumulates r_t), so content
must add BEYOND difficulty. Arms + the three independent difficulty-strips:
- **DRIVER** (difficulty only) · **X+SWAP** (content register fed difficulty-matched deranged r —
  donor from another sentence in the same NLL×‖tau‖ decile bin) · **X+CONTENT-MAG** (Fable: |r_t|,
  direction stripped — difficulty is magnitude, content is directional) · NO-EC.
- do-swap intervention (trained X+CONTENT re-scored with swapped r), content-register independence
  I_r, and a MANDATORY NLL-probe equivalence (if content wins on next-byte-NLL, it is prediction-
  aligned surprise = p7, NOT orthogonal content). New PC-TAU positive control routes a known content
  signal through the continuous ingress. Sol's v6_29 test-leak fix kept (val-selected epochs).

## Instrument CERTIFIES (PC-TAU, 5 seeds) — VALID read
Content routed through the ingress (emit relabeled by sign(w·r)): X+CONTENT beats X+SWAP z=11.31,
DRIVER z=9.15, MAG z=15.65, do-swap z=26.91, I_r=0.985. The estimator demonstrably reads directional
content of the size we would rule out → the natural negative is real, not underpowered.

## RESULT — 🟡 LAW-HOLDS (mouth/emit channel difficulty-complete within the material floor)
**DV=emit (primary):** X+CONTENT beats every difficulty control — but IMMATERIALLY (< the
pre-registered 0.010-nat floor):
| contrast vs X+CONTENT | Δ | z | material (≥0.010)? |
|---|---|---|---|
| DRIVER − X+CONTENT | +0.0059 | +4.78 | NO |
| X+SWAP − X+CONTENT | +0.0073 | +7.73 | NO |
| X+CONTENT-MAG − X+CONTENT | +0.0059 | +4.22 | NO |
| do-swap degrade | +0.0120 | +10.58 | (real use, but…) |
| independence I_r | 0.983 (LB 0.979) · effrank 2.56 | | |

TOST: both DRIVER and SWAP contrasts have mean+2·se < 0.010 → **statistically detectable but
immaterial**. The emit decision gains nothing material from content beyond difficulty.

**DV=nll (p7-contamination probe) — the decisive discriminator:** X+CONTENT beats DRIVER by **+0.1486
(z=4.11)** and NO-EC by +0.517 — the residual `r` still carries a LOT of next-byte-prediction signal.
NLL-probe equivalence **FAILS**. And MAG ≈ X+CONTENT on NLL (−0.0515, z=−0.93) — the "direction
advantage" seen on emit vanishes on the prediction DV. ⟹ whatever content survives residualization is
**prediction-aligned surprise (p7)**, not orthogonal content. Even the tiny emit effect is "just the
loss," finer-grained.

## Reading — the mouth channel is difficulty-complete
Two independent facts both point to LAW-HOLDS: (1) content's advantage on the emit decision is below
the material floor (TOST closure), and (2) whatever content survives is prediction-aligned (NLL-probe
fails, MAG≈CONTENT on NLL). So: **routing a faculty's independent variable through the mouth/emit
decision yields at most an immaterial, p7-aligned gain.** The composed-vs-reflex tension packet carries
no material DIRECTIONAL content the difficulty basis cannot already express, once difficulty and
surprise are stripped.

## Convergence & scope — R9 mechanistically confirmed for the MOUTH-ROUTED class (NOT universal)
This is the honest boundary both models insisted on. The redesign arc (V6_31 theater → V6_32 mouth
erases orthogonal signal → V6_33 spoon-fed agency is a difficulty-integral → V6_34 mouth channel is
difficulty-complete) mechanistically confirms frontier **R9** ("interior faculties blind/absent") for
**every faculty routed through the mouth** — the only readout the current architecture has. It does
NOT confirm a universal orthogonality law: `tau` is a mouth-logit projection, so it cannot test
non-mouth channels. **The one untested escape both models named: a NON-mouth, non-CE-trained decision
channel** — concretely the hippocampal store-bridge recall lane ([[pairodd-store-bridge-wired-invivo]],
WIRED in-vivo, content-addressed by construction, so difficulty-completeness cannot hold there
definitionally; Sol's framing: an intervention/reward-trained goal state). That is the next frame if
the redesign continues; the mouth/emit redesign itself is **closed directionally**.

## Scope
$0 numpy/torch, trained57 byte-LM, v6_33 natural held-out cache. DIRECTIONAL (lab/v6 ceiling).
Artifact: `v6_34_tau_content.py`. TERMINAL only via an anima-py in-loop port. Whichever decisive row
fires must be replayed through anima-py on natural corpus before any engine-native cement or terminal
R9 closure claim (Sol). Nuance recorded honestly: the content effect on emit is statistically real
(z=4–8, all 5 seeds) but immaterial (<0.010) and prediction-aligned — significant ≠ material, and
material-orthogonal is what a live path required.
