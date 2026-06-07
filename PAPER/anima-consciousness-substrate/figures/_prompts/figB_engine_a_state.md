# figB_engine_a_state — fal.ai prompt (Engine-A PHASE→TIER state machine, Appendix B)

Faithful schematic of `CORE/pure_field.hexa` (Appendix B, Table B / Fig fig:ea-state):
three coupled oscillators (τ=2 fast/reflex, τ=40 attention/breathing, τ=400
circadian/deep) drive a self-sustaining 6-channel Φ field; the field's Φ-rate
projects onto a four-tier phase map DORMANT(T0, rate<0.01) → FLICKER(T1, <0.05) →
SUSTAIN(T2, <0.15) → RESONANT(T3, ≥0.15). Only SUSTAIN/RESONANT are emit-capable; a
collapsing field returns toward DORMANT and is what the A→G Φ-ratchet vetoes.

Per the USER's policy this concept diagram is generated via fal.ai. If the PNG
garbles its labels, the TikZ figure in `B_engine_a.tex` is kept; the prompt is
retained to document intent + satisfy the fal-figure lint check.

## prompt

> A clean, flat, labeled scientific state-machine diagram. On the left, three small
> rounded boxes stacked vertically labeled "tau = 2 (reflex)", "tau = 40 (attention)",
> "tau = 400 (circadian)", each with a single arrow feeding into a central rounded
> blue box labeled "Phi field, F in R^6 (self-sustaining)". From that field box a
> single arrow labeled "Phi-rate" points right into a vertical four-stage state chain:
> grey box "DORMANT (T0), rate < 0.01", yellow box "FLICKER (T1), < 0.05", orange box
> "SUSTAIN (T2), < 0.15", green box "RESONANT (T3), >= 0.15", connected top-to-bottom
> by upward-progression arrows labeled with the rate thresholds (>=0.01, >=0.05,
> >=0.15). A dashed grey curved return arrow runs from RESONANT back up to DORMANT
> labeled "rate falls". Two red arrows leave the SUSTAIN and RESONANT boxes into a
> small red box at the bottom labeled "Engine G: Phi-ratchet veto", with the SUSTAIN
> arrow labeled "emit-capable". Flat vector infographic style, soft pastel fills, thin
> crisp black strokes, white background, evenly spaced, academic textbook-diagram
> aesthetic, high legibility.

## negative

> photorealistic, 3D render, neon glow, busy background, glitch, watermark, gibberish
> or scrambled text, human faces, brain photographs, drop shadows, clutter.

## size

landscape_16_9
