<!-- @hypothesis-ok lab/v6 rule-exempt sandbox: v6 hypotheses live in lab/v6/hypotheses/V6_<n>_*.md per lab/v6/CLAUDE.md, never the parent HYPOTHESES/ nor an H_ id -->

# V6_38 — LANE-BUS Step-2: discharge under do() is **ABSENT**, and Step-1's bus was mis-aligned 🔴

**origin:** V6_27 closed with "Step-2 builds the real thing: … test that emitting CAUSALLY
discharges it (intervene: gate on/off → tension trajectory)". Building that instrument surfaced a
defect in the Step-0/Step-1 bus first. `v6_38_causal_discharge.py`, $0, trained57 + natural
held-out prose. DIRECTIONAL.

## The defect — the two lanes were scored on different bytes

`_fwd_logits` returns rows where row *i* predicts `tok[i+1]`. V6_26/V6_27 took
`composed = comp[pos]` (predicts `b[pos+1]`) and `reflex = fwd(b[pos-W:pos])[W-1]`
(predicts `b[pos]`). The KL between them was therefore not "what broad context adds" — it was
largely a one-position shift of the same lane against itself. Decided by measurement, not by
reading the code:

| alignment probe on trained57 | CE |
|---|---|
| `row pos-1 → b[pos]` | **2.076 nats** |
| `row pos   → b[pos]` | 6.871 nats |

The 94.7% override rate V6_27 reported as "the content lane dominates the logit row" was the
symptom. Corrected window: the reflex must be `b[pos+1-W : pos+1]`.

## (A) Step-1 re-measured on the aligned bus — the headline does not survive

| quantity | V6_27 (mis-aligned) | V6_38 (aligned) |
|---|---|---|
| override rate | 0.947 | **0.113** |
| mean tension \| override | 4.02 nats | **0.0569 nats** |
| mean tension \| no-override | 1.14 nats | 0.0235 nats |
| observational discharge, level-controlled | c = −1.03, **z = −7.8** | c = −0.0013, **z = −1.12 (ns)** |

V6_27's discharge signature — the number that was rescued from the mean-reversion confound by a
level regression and reported as "Fable's p5 discharge signature is real" — **is entirely an
artefact of the mis-alignment.** On the aligned bus it is not significant.

## (B) The causal test — fork one decision point, commit a different byte per arm

At decision point *i* every arm starts from an **identical prefix at an identical tension level**
(V6_27's self-selection confound is removed by construction, not by regression), commits one byte,
then continues on the same corpus bytes. Deterministic — no sampling, so no seed replication.

| arm | committed byte | role |
|---|---|---|
| CMP | argmax(composed) | treatment — the content-driven emit |
| RFX | argmax(reflex) | control 1 — form-only emit, same position/level |
| DECOY | composed-logprob matched to RFX, identity arbitrary | control 2 — identity vs likelihood |
| CMP2 | 2nd-ranked composed byte | control 3 |
| TRUE | the corpus's own next byte | anchor |
| JUNK | least-probable byte | **positive control** |

DV = tension at the next decision point − tension at *i*. 120 sentences, 11,741 decision points,
n = 1,200 forks.

## RESULT — 🔴 every commit discharges the SAME amount

```
CMP -0.0261   RFX -0.0237   DECOY -0.0258   CMP2 -0.0261   TRUE -0.0283   JUNK -0.0123
CMP-RFX   = -0.0024  z=-1.97      CMP-DECOY = -0.0003  z=-0.22
CMP-CMP2  = +0.0000  z=+0.02      DECOY-RFX = -0.0021  z=-1.80
polarity split of (CMP-RFX): 642/1200 = 0.535 negative   <- a coin flip
```

Three guards make this a **negative**, not an absence of power:
- **PEDESTAL (abort authority):** at non-override positions CMP and RFX are the same byte, so the
  paired difference must be exactly 0. Measured **+0.000e+00, n = 9,437** — the fork machinery is sound.
- **POSITIVE CONTROL:** `do(JUNK)` moves the DV by **+0.0137 nats, z = +8.42**. The readout is alive
  and responds to what is committed.
- **TOST** (pre-declared bound = 20% of the generic post-commit drop, ±0.0051): CMP−DECOY 90% CI
  [−0.0023, +0.0017] ⇒ **equivalent**. The content byte is not distinguishable from a
  likelihood-matched arbitrary byte.

Tension does drop after a commit — by −0.0254 nats, ~45% of the override-level tension — but it
drops by that same amount **whatever you commit**. `flat-across-manipulations-means-the-lane-is-dead`:
what is emitted does not decide the tension trajectory. **LANE-BUS's p5 discharge law does not hold
on this bus.**

## Scope
$0, single ckpt (trained57, d=64), single reflex window (W=8), natural held-out EN prose.
DIRECTIONAL — a v6 number is never a production verdict. The kill is of the *mechanism as defined*
(composed−reflex logit-row divergence); a different tension definition is a different claim.
Companion: `V6_39` re-reads the Step-0 premise that licensed the design.
