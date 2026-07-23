<!-- @hypothesis-ok lab/v6 rule-exempt sandbox: v6 hypotheses live in lab/v6/hypotheses/V6_<n>_*.md per lab/v6/CLAUDE.md, never the parent HYPOTHESES/ nor an H_ id -->

# V6_27 — LANE-BUS Step-1: the bus tension is load-bearing AND discharges on emit 🟢🟢

**origin:** V6_26 gate PASS (logit-row content tension is 15-dim). Step-1 tests whether that
tension is (a) LOAD-BEARING and (b) has Fable's falsifiable p5 signature — emitting a
content-driven byte should DISCHARGE the residual. `v6_27_lanebus_discharge.py`, $0, reuses
trained57. DIRECTIONAL.

## Two lanes (no new training)
reflex[t] = logits given only the last 8 bytes (form-only); composed[t] = logits given the full
prefix (form+content); **tension[t] = KL(softmax(composed) ‖ softmax(reflex))** (nats);
override[t] = argmax(composed) ≠ argmax(reflex).

## RESULT (80 natural sentences, 7,675 positions)
**1. Load-bearing — YES.** override rate 0.947; mean tension | override = 4.02 nats vs
| no-override = 1.14 (+2.88 separation). The content lane dominates the logit row.

**2. Discharge — GENUINE (survives the confound I first missed).** Raw contrast: Δtension after
override −0.20 vs after no-override +3.51. ⚠️ That raw contrast is CONFOUNDED by tension level
(override positions are high-tension by construction, and high tension mean-reverts down). I
caught this and added the control — regress Δtension ~ a + b·tension_level + c·override:
| coefficient | value | reading |
|---|---|---|
| b (tension level) | −0.93 | mean reversion (expected) |
| **c (override, level-controlled)** | **−1.03, z=−7.8** | **extra drop BEYOND mean reversion** |

Controlling the level, a content-driven emit still discharges an extra −1.03 nats (z=−7.8, n=7675).
**Fable's p5 discharge signature is real, not a regression artefact.** LANE-BUS's tension
redefinition (composed−reflex divergence) is both load-bearing and falsifiably discharging.

Caveat: the 8-byte reflex is weak → 95% override → override/tension collinearity; a stronger
reflex lane would firm up the level control, but the controlled coefficient is robustly negative.
Verdict-integrity: the raw "DISCHARGE CONFIRMED" auto-headline was a mean-reversion artefact
until the control; the signal survived the control.

## Next — LANE-BUS Step-2: the trained emit gate
The mechanism holds observationally on a REFLEX-vs-COMPOSED split of ONE model. Step-2 builds the
real thing: a trained emit gate that fires on the tension residual, and tests that emitting
CAUSALLY discharges it (intervene: gate on/off → tension trajectory). Then Step-3 = a proper
content lane (store-bridge promoted from patch to heart) instead of the full-context proxy.
Path: lab/v6 prototype → core/ + `anima-py` flag for TERMINAL. Reuse trained57 as the reflex lane;
v6_27 as the tension+discharge instrument.

## Scope
$0 observational (DONE 🟢🟢). Step-2+ = build. Single ckpt · single seed · reflex=8B-window proxy.
DIRECTIONAL; TERMINAL only via anima-py.
