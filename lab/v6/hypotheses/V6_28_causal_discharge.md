<!-- @hypothesis-ok lab/v6 rule-exempt sandbox: v6 hypotheses live in lab/v6/hypotheses/V6_<n>_*.md per lab/v6/CLAUDE.md, never the parent HYPOTHESES/ nor an H_ id -->

# V6_28 — LANE-BUS Step-2: causal discharge is REFUTED on the proxy (the emit doesn't DO it) 🔴

**origin:** V6_27 found the discharge survives a mean-reversion control (observational). Step-2
tests it CAUSALLY: within the same divergent position, actually emit each candidate byte and
compare the resulting residual. `v6_28_causal_discharge.py`, $0 counterfactual, reuses trained57.

## Design (within-position counterfactual — removes the "which positions" confound)
At each position where argmax(composed) = c ≠ r = argmax(reflex):
emit c (content) → tension_c; emit r (form) → tension_r; both from the same prefix.
discharge_content = tension[t]−tension_c ; discharge_form = tension[t]−tension_r.
Fable's p5 (causal form): emitting the CONTENT resolution should discharge MORE.

## RESULT — 🔴 NO causal effect (40 sentences, 181 divergent positions, paired)
| emit | discharge |
|---|---|
| content byte c | +0.0177 nats |
| form byte r | +0.0185 nats |
| **content − form (paired)** | **−0.0008 nats, z=−0.31** |

Which byte is emitted makes NO difference to the discharge (both a tiny +0.018). ⟹ V6_27's
observational discharge (−1.03 nats, level-controlled) was **NOT the emit's doing** — it is the
structure of natural text (a high-tension position is followed by a lower-tension one in the
real continuation, regardless of what is emitted). **Fable's p5 "emitting discharges the
residual", in its CAUSAL form, is refuted on this reflex-vs-composed proxy.**

Verdict-integrity chain: V6_27 raw "confirmed" → mean-reversion artefact → survived the level
control as OBSERVATIONAL → V6_28 shows it is NOT CAUSAL. Each step tightened the claim; the
causal version does not hold on the proxy.

## Architectural decision (the finding, not a failure)
Discharge is NOT an emergent property of byte-emission — mechanically, the residual is about the
NEXT prediction's reflex-vs-composed divergence, and which byte was just emitted barely changes
it. So for LANE-BUS, **the discharge p5 needs must be an ARCHITECTED mechanism in the emit gate**
(the gate explicitly CONSUMES/resets the residual on fire), not an assumed emergent effect. This
refines Fable's design: Step-3's emit gate must have an explicit residual-consumption term, and
its falsifiable test is whether that architected discharge improves the emit/silence decision vs
a gate without it — a BUILD, not a $0 probe.

## Where the cheap-instrument phase lands (V6_26→28)
- V6_26: logit-row content tension is multi-dim (15.3) — LANE-BUS premise holds. ✓
- V6_27: that tension is load-bearing; observational discharge survives mean-reversion. ✓ (obs)
- V6_28: the discharge is NOT caused by the emit — it must be architected into the gate. ✗ (causal)
The $0 instrument phase is depleted: it has mapped that the tension is real and multi-dim, but
the discharge mechanism must be BUILT (trained emit gate with explicit residual consumption),
which is the next campaign (core/-class, train + wire), not another cheap probe.

## Scope
$0 counterfactual (DONE 🔴 causal, ✓ instrument-mapping). reflex = 8B-window proxy; a trained
content lane + trained gate is the real test. DIRECTIONAL; TERMINAL only via anima-py.
