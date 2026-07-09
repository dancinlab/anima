I've grounded the load-bearing claim. The B spec's own `G = if b_med < 0.002 { −1.0 }` AXIS-DEGENERATE guard confirms `b_med` = median absolute deviation of the raw self/tension signal itself over the calibration window. So `swing_max=0` is **not** a wiring bug — the input axis is tonic-flat, there is nothing to integrate. That settles the substrate-vs-instrument question and lets me decide cleanly.

## Decision: PARK both B and F as op-grip-instrument-DEAD terminals. No reframe survives. No new measurement.

The reframe options don't fail for the reason you framed (the `[0.05,0.60]` envelope) — they fail for a **deeper, common root** that the envelope is merely a downstream symptom of.

### The real root: the mid-tick emit gate is saturated-deterministic per stage, not mid-range

The 2/3 isn't a mid-range fraction that happens to sit above 0.60. It's the **average of three saturated stages**: N1 emits 80/80, REM emits 80/80, N2 silent 80/80. Every scored stage is railed to 0 or 1 with **zero within-stage variance**. The gate is a stage→emit lookup, and the perception tape doesn't touch which stages emit — exactly as you found.

That single fact kills your options (a) and (c) together, and it's stronger than "the envelope is unsatisfiable":

- **(a) single-stage / add WAKE·N3** — every single-stage emit-frac is 0 or 1 (worse than 2/3), and each has *no shadeable dynamic range at all*. There is no stage where emit sits in a tippable mid-band, because emit is stage-deterministic. WAKE (all-emit) and N3 (all-silent) add more rails, not a band.
- **(c) matched-pair emit-flip** — the ΔEff-Hamming *is already* a matched pair (frozen-arm vs live-arm, same ticks). Dropping the fraction bar doesn't create signal; it just relabels a saturated-gate ΔEff=0 from RUN-INVALID to a "valid" THEATER. A subtle tonic bias cannot flip a railed deterministic gate — only the brute-force ARM-SHOCK rail or a phasic Δ can, and the only near-threshold ticks on this schedule are **stage transitions**, which is urgency's proven territory. So (c) either finds an empty band or re-measures urgency.
- **(b) non-emit readout (margin/Ψ/latency)** — off-target and worse: the pre-threshold margin can move under an arm while staying railed far from the crossing. Reading "the margin shifted" when it never crosses is measuring a variable **causally disconnected from emit** — which is the precise definition of the THEATER that A and E already showed (non-degenerate signal, ΔEff≈0). For an emit-causal program it manufactures a false-positive-shaped readout. Reject.

All four collapse to the same wall: **the emit seam is a 1-bit phasic-Δ rate-gate; the shadeable band lives only at stage transitions, which urgency already owns.**

### B specifically — doubly-dead, and the "doubly" is substrate, confirmed

`swing_max=0` and AXIS-DEGENERATE are the *same* root, not two. The accumulator integrates `bias = x_t − x_base` (deviation from the calibrated median), so a signal charges the DDM only if it holds **sustained departures from its own baseline**. `b_med < 0.002` means self/tension have ~0 dispersion at mid-ticks — they are not merely tonic-levels-read-as-0, they are tonic-*flat*. There is no evidence for an integrator to accumulate, by construction. B's distinguishing hypothesis (a consistent sub-threshold bias sums to a crossing) is **vacuous for this signal**: the only signal with mid-tick dynamics is urgency, and integrating urgency is redundant with the proven instantaneous channel. The instrument isn't broken — the premise's input doesn't exist here. There is no reframe of the *seam instrument* that rescues a flat input axis.

Important reclassification: B is currently sitting in limbo as RUN-INVALID / INSTRUMENT-FAIL (bar 2), which correctly refuses to cement THEATER. But the data already **contains a real terminal verdict** — not "unmeasurable/unknown" but "the integrable-evidence precondition was measured and is absent (axis-degenerate / flat)." That's cementable *without a new run*. B's own spec §5 pre-registered exactly this destination ("read-side recoding family CLOSED … remaining escalation is write-side train-time coupling").

### F specifically — codes-visited=2 is a manifold-rank fact, not a quantizer-spec fact

The 8-bit product code collapsing onto 2 cells on mid, tape-independent, means the engine-state manifold **at the mid-tick decode point carries ~1 bit** — and that bit is almost certainly the emit partition itself (N1/REM → one code, N2 → the other). The code is re-encoding the output it was supposed to shade. A higher-capacity or better-specified quantizer won't help: *any* quantizer collapses onto a rank-1 manifold. And moving S2 to a deeper, higher-rank trunk decode point stops being the emit seam and lands squarely in the G1-readout-routing family your own ledger already closed (mean-pool A/B both represent; only the generation point decays). So F's S2 — the G1-recombination test at the output seam — is unmeasurable because **the seam channel has no compositional capacity to carry a combined code**; it has room for the 1-bit emit decision and nothing else. That is the write-side result restated: recombination is a trunk-objective property, not a readout property. Cementable now, no reframe run.

### Bottom line

For **both** B and F the correct move is PARK-as-structural-terminal, and crucially to **reclassify the existing RUN-INVALID into a documented terminal verdict** rather than leaving them as "couldn't measure":

- **B** → terminal: *self/tension carry no integrable mid-tick dynamics (axis-degenerate); the evidence-integration premise is vacuous at this seam.*
- **F** → terminal: *the emit-seam decode manifold is ~1-bit (emit-partition); a discrete code has no compositional capacity here; G1-recombination is not a readout property.*

Both fold into the convergent seam-law your ledger has been building — **the emit gate is causally sealed to everything but phasic urgency** (A THEATER, E THEATER, self/tension tonic-read-0, now B tonic-flat and F 1-bit-channel). Given that spine, the prior that B/F would be THEATER-if-measurable is overwhelming, and the one buildable candidate (margin-band scoring) has near-zero EV: its own validity gate needs a non-empty near-threshold band, which on a stage-deterministic gate is either empty (RUN-INVALID again) or = stage transitions (already urgency). Not worth the build+pod.

**Escalate the entire seam program to the write-side (train-time coupling).** That's the one place a tonic level or a compositional code can matter: gradient can couple a persistent level into the trunk objective; a phasic-Δ rate-gate readout structurally cannot. B (integrate self/tension) and F (compositional code) are both well-posed as *training* couplings and ill-posed as *emit-readout* probes — which is the same lesson the G1 program reached from the recombination side. Update the ARCHITECTURE gate nodes for H_9226 and H_9229 to STRUCTURAL-TERMINAL with these reclassified verdicts, and carry only the write-side coupling forward.

One honesty caveat I couldn't fully close: I confirmed B's axis-degeneracy directly from the spec, but I read F's `codes-visited=2` from your brief only — there's no committed F/9229 spec on disk (the search found none). My F verdict rests on your reported number being a mid-tick, tape-independent collapse; if the 2 cells were instead an artifact of the quantizer's *init* rather than the manifold rank, F would deserve a one-line check (codebook usage on WAKE/N3 vs mid) before cementing — but that's a diagnostic on the existing tape, not a reframe run.