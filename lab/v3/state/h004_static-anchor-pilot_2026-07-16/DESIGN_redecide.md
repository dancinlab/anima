# Campaign re-decision after H_004 terminal — verbatim Fable 5 (seed of record)

- job fable-mrmnhqtl · claude-fable-5 · 2026-07-16

---

All sources read — card, guard battery, reframe seed, proxy JSON, and the SSOT nodes (`verification-h004`, `cr-atomicity-not-isolable`, `decision*`, `fd-true-axes`, `salvage` L1–L10, F1–F8). Here is the re-decision.

---

# Campaign re-decision after H_004 STRUCTURAL TERMINAL

## R1 — Is there a live F1 question the terminal does not kill?

**No. All three candidates are the theorem in a costume.** The theorem's engine is a tautology about *frequency-fixedness*: the statistic that lets BPE dedicate a unit to a form (frequent + fixed sequence) is the statistic that lets any n-gram-binding system read the form without that unit. Test each candidate against that engine, not against the receptive-flip surface:

**(a) Generation — killed, same premise, dual direction.** Generating a fixed morpheme for a held-out stem decomposes into: (i) decide NEG — supervised by the explicit mark, identical across arms; (ii) select allomorph i — conditioning information lives in the visible context, which the codec does not change; (iii) emit the form — for the frozen arm this is emitting a 2–3-token frequent fixed sequence, i.e. exactly the high-probability n-gram continuation an LM is best at. The only arm-difference is multi-step vs single-step emission (exposure bias across 2–3 fragment steps) — a second-order sampling effect, nowhere near a Δ ≥ 0.20 class, and it would measure decoding noise, not the write lever. The proxy already hints the sign isn't even guaranteed positive (frozen 0.971 ≥ oracle 0.923 receptively; fragments shared with plain material give frozen *more* gradient per subunit `?`). Generating a fixed morpheme = emitting its n-gram. Costume.

**(b) Refit under productive drift — killed, and this is the important one, because the tautology cuts both ways.** The hope is that "fixed morpheme" is the theorem's premise, and productive morphology breaks it. But refit is frequency-driven: BPE can only atomize a form *after* it has become frequent and fixed — at which point its terminal n-gram is frozen-recoverable again. If the morphology drifts so fast that no form fixes, refit has nothing to grab either. Productive composition just moves the unit down one level: the productive pieces are themselves fixed sub-units, so the class statistic sits one order higher — which is exactly the order-1 → order-2 move already executed and already lost (G-A 0.527 → G-C 0.995; one attention head binds order-2, a second binds order-3 `?`). Refit and n-gram binding feed on the *same* statistic read by different machinery; there is no drift rate at which one eats and the other starves.

**(c) Long-range / compositional depth — killed as an F1 question; it is `cr-atom-corollary` re-dressed.** MORPH-ATOM C1 = 0.617 already *is* the measurement "binding span (~18 bytes, all-shared units) exceeds a small model's n-gram reach"; a multi-affix rig would re-measure the corollary. Worse, whatever Δ appears is a **model-capacity artifact, not a structural lever**: raise layers/heads/data and the reachable order climbs, the wall moves, the Δ evaporates. A lever whose existence is a function of the opponent's parameter count is a compute-efficiency knob, not "where aliveness lives." And it is a claim about *static* codec choice — it never touches the refit organ, which is the only thing F1 actually proposes.

**Residue.** The one F1 question that is technically unkilled: is the refit organ net-*negative* under drift (the L10 tax with, now, no measurable receptive benefit to offset it)? Expected answer: yes, a pure tax `?`. Killing it buys ~0 remaining belief — the belief it would kill is already dead. F1's restated form ("the codec compresses the credit-assignment span; refit maintains it") survives only *verbally*; per the HYPOTHESES conventions its honest home is a 🜂 ABSTRACT card (`H_A*`), not another rig.

**R1 verdict: no surviving F1 card. F1 = measurable-content-spent at rig scale.**

## R2 — Does F1 yield first place?

**Yes — and the write-lever axis yields with it.** Re-derivation on belief-killed-per-dollar:

| axis | member | status after H_004 | next-card cost | belief killed per $ |
|---|---|---|---|---|
| write-lever | F1 | receptive-DEAD; R1 finds no survivor | — | ~0 |
| write-lever | F4 | live; XBIND l4(a) untouched by the theorem | RL acquisition loop + oracle-π ceiling pilot ⇒ GPU-days, Goodhart probe burden (`decision-f4-worse-burden`) | low-medium, and delta unanchored — the H_001 disease verbatim |
| pred-error-action | F3 | live; its pre-registered blocker ("whatever codec regime survives", `decision-why-f1-not-f3-f3-timing`) is now RESOLVED at $0: frozen codec, bpb, no refit organ | **$0 premise card exists** (below) | **highest** |
| selection-lineage | F6 | **dented by H_004**: its reproduction operator mutates the CODEC (`f6-how-reproduce`) — the axis of variation it pre-registered is the lever just shown non-separable. Needs a new variation axis before it is even coherent | high | negative until repaired |
| time-trajectory | F5 | untouched; needs a real interaction stream + weeks | weeks wall-clock | medium, deferred |

Three points the table compresses:

1. **The original F1-first argument is gone twice over.** `decision-family` picked on kill-radius via the only green causal measurement; that measurement is relabeled (`l4-morph-atom-relabel`: low-order exposure, not atomicity), and `decision-f1-first-survives` rested on `l4-morph-atom-slot-not-address`, itself weakened (stem-deletion invariance is *predicted* by the lookup). Nothing in the selection chain still points at F1.
2. **F4 inherits an odd half-promotion but a bad rig.** H_004's result — "static fragment statistics deliver the value; the statistics come from the corpus" — actually collapses the write-lever onto its F4 half (what the stream contains is the lever, not how it is re-segmented). But support ≠ testability: F4's falsifier needs training loops per policy step, its effect size is exactly as unanchored as F1's was, and its ceiling pilot (oracle-π) cannot be run for $0. Buying F4 now repeats H_001: a null at an unanchored delta_min is unattributable.
3. **F3 was the pre-registered second card and its two known diseases now have H_004-shaped cures.** Disease 1: an F3 null can't separate "diary carries no load" from "stream has no cross-day MI" (`decision-why-f1-not-f3-f3-ambiguous`) → cure: measure the stream's MI *first*, deterministically — the premise, before the organ. Disease 2: a *synthetic* planted-latent drill is pre-answered YES by the literature (copy-through-bottleneck works), so SUPPORTED would kill nothing → cure: run the premise card on *real* streams, and use the synthetic planted stream only as the instrument's positive control (the `l6-blind-tool` lesson).

**R2 verdict: F1 yields. The campaign moves to the prediction-error-action axis via F3 — entered through its premise, not its organ. F4 stays live-second (redesign requirement: ceiling-first, oracle-π). F6 is suspended pending a new variation axis. H_002′ stays REFUSED; the `decision-pre-commitment` clause ("drill-scale null = family-DEAD") is satisfied in spirit at $0 — the drill-scale effect is structurally ≈ 0.**

## R3 — What was learned, and is it a law?

Yes. It generalizes beyond this rig and beyond F1 — F6's design already violated it, and any future synthetic contrast can — so it belongs in `salvage` as the campaign's first **v3-earned** sealed law (provenance differs from L1–L10: earned here at $0, not inherited from v1; mark it so).

> **L11 — fusability IS recoverability (the frequency tautology).** For any FIXED frequent pattern, the property that lets an adaptive codec dedicate a unit to it (frequency × fixedness) is the same property that lets a frozen system read it with a low-order statistic (its terminal n-gram). Verified 12/12; G-C = 0.9954 vs G-D frozen 0/12.
> - **Corollary A (both-ways):** representation adaptivity can only pay where patterns are non-fixed or spans exceed binding reach — and there frequency-driven adaptation has nothing to grab either. Constructions only push the shortcut order up by 1 (order-1 → order-2 measured); a transformer follows with one attention head per order.
> - **Corollary B (measurement, extends L6):** in any two-arm contrast, the CONTROL arm's trivial-statistic ceiling (lookup battery at order 1, 2, …, deterministic, $0) must be measured BEFORE training. A contrast whose control ceiling ≈ oracle is structurally dead; a planned Δ is meaningless until this ceiling exists. H_004's entire spend was pre-empted by this battery.
> - **Corollary C (relabel, seals `l4-morph-atom-relabel`):** v1's only green causal measurement was LOW-ORDER CLASS EXPOSURE, not atomicity; raw utf-8 failed for span-reach, not for want of atoms.
> - **Design consequence:** a lever is only isolable if the credit path is forced through it by a *structural boundary* (information physically absent from the visible context), never by inventory/frequency engineering inside the context.

That last consequence is what licenses R4.

## R4 — The ONE next card

**H_005 `f3-stream-mi-precheck` — "does any available experience stream carry cross-boundary information for a diary to transport?"** $0-deterministic core + cheap numpy proxy. No GPU, no torch.

**Question.** F3's diary is load-bearing *only if* tomorrow's stream has mutual information with today's that (i) exceeds what fits in the model's context at prediction time and (ii) is day-specific, not generic style. Measure that quantity on real streams before building any organ. The hindsight-optimal k-token summary is the **oracle-diary ceiling** — the H_004 lesson institutionalized: the later twin's `delta_min := ceiling/2`, anchored in-substrate *before* the twin exists (repairs the `decision-attributability` disease by construction).

**Why it escapes L11.** It contrasts no representation arms at all — it measures a property of the stream. And the eventual diary twin escapes structurally, not by inventory engineering: the transported information sits *outside the context window* at prediction time, so no within-context statistic of any order can substitute for the bottleneck; the credit path physically crosses m (L11 design consequence). The L11-shaped failure mode — "planted signal recoverable from visible context" — is exactly what this card quantifies and closes. The weight-channel confound (online training smuggling the day-latent through weights, the F5 channel) is closed in the twin by making eval latents fresh draws: weights can learn the transport *protocol*, never the day's *value*.

**Streams (must exist today):** (a) dancinlab git history — commits + diffs, months deep, definitely on disk; (b) owner dialogue/session logs `?`; (c) sidecar inbox archive `?`. Chunk into "days"; if (b)/(c) are empty, (a) alone suffices for a verdict.

**Measurement.** bpb of day-(t+1) prefix under conditionings: ∅ · last-W-byte tail of day t (in-context reach) · tail + hindsight-selected k-token extract of day t (oracle diary) · tail + same-size extract of a wrong day t′ (swap). Estimators: order-k n-gram + gzip-style compressor ($0, deterministic) + tiny numpy LM (cheap proxy, minutes — `run_proxy.py` pattern). Ceiling := bpb(tail) − bpb(tail+oracle); day-specificity := bpb(tail+swap) − bpb(tail+oracle).

**Inherited gates, operational:**
- **L1 effective-rank gate:** participation ratio of day-representations (estimator feature vectors across ≥100 day-pairs) must exceed a pre-registered floor (≥8 effective dims `?`). Days indistinguishable → the stream is degenerate → **INVALID**, not REFUSED (the l6-scramble-floor distinction).
- **L2 ablation gate:** the swap control. If bpb(tail+swap) ≈ bpb(tail+oracle) — an OMEGA-0.0009-class gap — the measured "MI" is generic register, not day-specific information: the ceiling is decoration → counts as **kill**, not support.

**Falsifiers (≥5, pre-registered before running):** P-1 kill: ceiling ≤ shuffle-floor + ε on ALL streams → **F3 REFUSED on available substrate** (and F8's diary organ premise with it) → axis re-decision toward F4-with-oracle-π or F5. P-2 instrument liveness: a planted-latent synthetic stream (latent placed beyond W, fresh per day) must read ceiling ≥ pre-registered value through the same instrument, else INVALID (blind-tool control). P-3 bounds: day-order-shuffled real stream must read ≈ 0. P-4 estimator agreement: n-gram/gzip/numpy-LM must sign-agree, else PENDING(instrument). P-5 leak: no cross-day dedup overlap in eval prefixes (`l6-leak`).

**Kill-power per dollar:** a null retires F3 *and* F8's diary component and establishes "the available substrate has no temporal self to compress" — redirecting the whole prediction-error axis — for $0. A positive yields the campaign's first pre-anchored delta_min ever. Either outcome moves more belief than any GPU run currently on the table, and the campaign has now twice shown $0 structural analysis terminates lines that training runs would have measured noisily and expensively.

---

**Bottom line:** F1 is done — not falsified as a metaphysical claim, but spent as a measurable one; every proposed survivor is the frequency tautology wearing a new eval. The write-lever axis yields. Seal L11 into `salvage` (v3-earned), park restated-F1 as an abstract card, suspend F6 pending a new variation axis, and spend the next card on F3's premise: **H_005 `f3-stream-mi-precheck`**, $0, with the oracle-diary ceiling doubling as the first honestly-anchored delta_min of the campaign.