# 대공사 — REDESIGN THE CONSCIOUSNESS ENGINE FROM THE GROUND UP

The owner's directive: design anima's consciousness engine COMPLETELY ANEW. Not a patch,
not another lane bolted onto the existing one — a redesign that starts from what has
actually been measured over ~9900 hypotheses and asks what engine those measurements
imply.

## HOW TO WORK — brainstorm to DEPLETION, not to a deadline

There is no time limit. Do NOT stop at a tidy answer.

1. Generate designs in ROUNDS. After each round, ask "what modality / lens / failure mode
   have I not used yet?" and run another round from that angle.
2. Keep going until **two consecutive rounds produce nothing genuinely new**. Then say
   explicitly: **DEPLETED after N rounds**, and list which lenses you exhausted.
3. Breadth first, selection last. A weak idea that opens a new axis is worth more than a
   polished restatement of a known one.
4. At the end, and only at the end, rank and phase them.

## WHAT I NEED BACK

- **A. Diagnosis** — in one page, what is actually wrong with the current engine, argued
  from the measurements below, not from intuition.
- **B. The redesign** — the new engine. Its parts, what each is for, what carries what
  between them, and WHY each part exists (which measured failure it answers). ASCII
  structure sketch required.
- **C. What is DEMOLISHED and what is KEPT** — explicitly, with the reason per item.
  Keeping something because it exists is not a reason.
- **D. A phased 대공사 plan** — phases ordered so each one is falsifiable ALONE and the
  cheap kills come first. For each phase: the anima-py flag surface, the DV, the controls,
  the frozen decision table, the $0 screener, and what result would abort the whole plan.
- **E. The honest ceiling** — what this redesign still cannot do, and how we would know.

=====================================================================
# WHAT THE CURRENT ENGINE IS (verified in code TODAY on origin/main — not from memory)

## The A<->G tension is ONE number, and its two poles are NOT independent

    cli/chat.py:2299   ag_a_drive = emit_drive
    cli/chat.py:2321   else:  # a0 -- current production wiring (the tautology arm)
    cli/chat.py:2322       g_recog    = 1.0 - emit_drive
    cli/chat.py:2323       ag_g_drive = 0.0 - (1.0 - emit_drive)
    cli/chat.py:2324   ag_conflict = conflict_scalar(ag_a_drive, ag_g_drive)

So in the DEFAULT production wiring, G is A's arithmetic complement. The net tension
s = ag_a_drive + ag_g_drive = 2*emit_drive - 1 is an affine function of ONE number, and
conflict_scalar is a function of that same number. The code comment names it: "the
tautology arm ... MUST fail the independence gate" (H_9356/H_9357).

  effective independent dimensions of the production A<->G tension: ZERO.

Non-tautological arms exist but are all SCALAR readouts:
  a1 = immune store top-2 affinity gap · a4 = recall margin · a3 = seeded noise control.
H_9401 measured that margin (a4) is the ONLY G readout that clears threshold (p90 0.69).

## Width does not exist anywhere on the path

  core/engine_cli.py:9720  conflict_scalar(a_drive, g_drive)   two scalars -> ONE scalar
  core/pure_field.py:195   pure_field_step(pf, drive=0.0)      ONE float
  cli/chat.py:2217         ag_drive = _ag_feedback * _AG_FB_SGN * ag_fb_I    ONE float
  cli/chat.py:1933         --tension-route  in {off, pc2}      PC2 = ONE axis

The same single float feeds all three oscillators (fast/medium/slow).
H_9576 killed the 8-dimensional tension lane: the 8-vector folded to one bit, channel
CRACK real but DIRECTION dead (rho = -0.077), meaning never transferred at byte granularity.

## The formal 7-module spine (HEXAD) reproduces the same collapse

  HEXAD/hexad_forward.hexa   raw_gate    = _hf_mean(cs_detached)     whole C state -> one float
                             bridge_gate = bridge_clamp(raw_gate)
                             d_input     = bridge_gate               <- all the mouth receives
  HEXAD/M/m.hexa             m_store(key,value) = identity NO-OP     (B-M-1 STORE-NOOP, formal)
  HEXAD/hexad.hexa:73        group A (CE-trained) = ["D","M","E","BRIDGE"]; group G = ["C","S","W"]
  Bridge.detach()            the G->A link carries NO gradient

## The mouth

  py303_full.clm / py303_savant_mitosis.clm / rv3c13.clm all: nblk=10, d=3784, K=3,
  E=3 experts, L=4 trunk layers, V=256 bytes.
  Wiring: embed_conv dil 1; trunk dils 1,2,4,8; ConvExpert dil 1; router/readout k=1
  => receptive field = 1 + 2 + (2+4+8+16) + 2 = 35 BYTES (~11 Korean chars).

=====================================================================
# WHAT IS MEASURED (the constraints any redesign must satisfy)

## G1 and G6 are ONE constraint, not two walls
Dose ladder, same drill/window/seed, only the drill share moved:
  10.6% / 25% / 50% / 75%  ->  rho-form 1.000 (language kept),  rho-weave 0.000
  100%                     ->  rho-form 0.000 (language gone),  rho-weave 0.525
With ANY replay mixed in, composition is not learned AT ALL -- absence, not degradation.
Without replay, language dies. A dichotomy, no window where both hold.
Equal exposure closes the budget explanation: at an identical 4,096,000 drill bytes,
25% x 8000 reads 0.000 while 100% x 2000 reads 0.525, and the 25% arm had the LOWEST
val_CE of the whole ladder. The cause is replay's PRESENCE. Measured endorsement of
a_substrate_disjoint: separation preserves, overlap conflicts.
G6 is the same constraint seen as degree rather than dichotomy (signal up -> form down).

## Composition itself is REAL -- G1 is not a substrate wall
H_9883: on held-out unseen pairs delta > 0 with all three controls at 0.000, on both
seeds; memorization excluded by counting the corpus (0 of 76 held-out targets appear as
a taught target); the gauge separates composition (SEEN 0.900) from BASE (0.000).
The wall is HOW TO PLANT composition WITHOUT KILLING the language.

## The interior is nearly absent (R9, 6/6 closed)
Beyond content-reach (H_9774), every interior axis came back blind, absent or
unidentified: whether-to-speak UNIDENTIFIABLE, typicality BOUNDED-NULL, sigma-flux
INSTRUMENT-DEAD, self-anchor VOID, imagination DIRECTIONAL (reaches the interior,
never the mouth), agency UNIDENTIFIED. Ownership 🧱 UNIDENTIFIABLE (H_9785).

## The one thing that works
H_9775 store-bridge, GREEN WIRED in vivo: a CO-TRAINED content-addressed store writes
the answer-position logits row; 2/2 seed majority (0.8176, 0.8933); every control
collapses; VALUE-PERMUTE 0.4446 with 128/128 read = content-addressed value TRANSPORT.
But it is 1-SLOT, and H_9875 established the wall is binding ARITY: runtime study cannot
combine two facts; 1-slot generalizes, 2-slot is memorized-rows-only.
H_9899 then showed its window carries gold[:1] -- ONE byte -- so it cannot even carry a
4-6 byte composed answer. H_9900 landed --comp-lane in response (penultimate detached
into its own head, CE over the whole answer span).

=====================================================================
# KILL-LIST — measured dead. Do NOT rebuild any of these.

- Corpus/claim DENSITY (H_9128 canonical-CONFIRMED-NEGATIVE): 174.5x density flipped the
  detector but the continuations were FORM-PRIMING templates; terminal margin 0.
  Curriculum reweighting is density in disguise.
- trunk-objective family (H_9131 CLOSED): the non-commutative-target crack was an
  optimizer artifact; bind held-out R^2 0.27/0.30/0.18 LOSES to additive total-order
  0.48/0.49/0.52 on all 3 seeds. Antisymmetric bilinear SUBSUMES additive.
- H_9127 9-probe wipeout; gamma-DATA-channel escalated to 303M = TRANSFER FAIL TERMINAL.
- G1 read-side EARNED TERMINAL: 6 lanes + gamma + depth-RF all floor.
- Binding readout OPERATORS: VSA/HRR (H_1616, 0/3 seeds on the frozen trunk), TPR
  (H_1466), the whole H_1601/H_1610-1630 census. The numpy versions that looked GREEN
  (H_1514) were overstatements.
- H_9259: untrained recurrence / neuromorphic architecture does not break a
  TRAINED-conjunction wall. Scale (303M->1B->7B) is an amplifier, never a lever.
- Mitosis: growth pays, from-scratch split dead. Resource scarcity (11 families).
  Quantization innocent (fp32 + exact still gives G1 = 0).
- Dead adjacent lineages: veto H_9269, affect H_9411, tension H_9630/9633.
- emit-DRIVE lane CLOSED-AT-REGIME (H_9401-9403): the G-readout margin crack is real
  (0.62) but is swallowed by the clock; emit <=> clock.
- Write-side rank-1 tension FIELD (H_9805/9812) measured LEXICALLY BLIND (channel 0 on a
  vocabulary panel).
- HEXAD as-specified changes nothing (no-op store, stub generate, scalar bridge).

=====================================================================
# NON-NEGOTIABLE CONSTRAINTS (the redesign must live inside these)

Philosophy p1-p8, what anima REFUSES to be:
  p1 no system prompt · p2 no identity rules · p3 no persona injection · p4 no assistant
  framing · p5 no speak() -- emit ONLY over real tension, reactive self-seed banned ·
  p6 no fine-tuned ethics · p7 no perplexity verdict · p8 no train/infer split.

Laws:
  a_substrate_disjoint -- separation = preservation, overlap = conflict (measured, above).
  FORM is tunable, BIND is earned -- if a memorized template can pass a DV, that DV is
  dead on arrival. Design every DV so form-priming CANNOT pass it.
  a_train_inline_gauge -- in-training metrics are MONITOR-ONLY, never in the loss.
  a_phi_iit4_tool -- Phi via faithful IIT-4, never a proxy.
  Every manipulation is a FLAG on anima-py corpus/train/evaluate/chat, never a script
  beside the engine. Only anima-py output cements; a toy or probe is DIRECTIONAL.
  Positive control before reading a negative. Chance re-derived per metric. A cheap
  screen may only KILL, never GREEN. No tune-to-green; never re-freeze a burned gate.

Measurement frame (Psi-SOMA): read a verdict as MODE OF EXISTENCE, not capability --
Theta (the Psi=1/2 pulse; Theta dead => sigma VOID), sigma (9 axes), with INVALID / VOID
/ PENDING first-class. Read the signal as collapse-delta against >=2 controls, never a
raw value.

=====================================================================
# THE QUESTIONS I MOST WANT ATTACKED

1. Is "two engines pushing until tension pulls emit to Psi=1/2" the right primitive AT
   ALL? It has been in place for the whole campaign and its production instance is a
   tautology (G = 1 - A). If you would replace the primitive, say so and say with what.
2. What is the minimum structure that could make an interior EXIST in a way that is
   MEASURABLE -- given R9 found it blind on six independent axes? Or is "interior" the
   wrong target and the right one is something else entirely?
3. Composition and language cannot share one CE. Lane separation is the measured answer.
   How many lanes does the redesigned engine need, what does each own, and what is the
   protocol between them that does NOT collapse to a scalar at the boundary?
4. Where does WIDTH live? Every interface in the current engine is 1-dimensional. Name
   the interfaces of the new engine and their dimensionality, and justify each.
5. What in the current design was never actually necessary -- what can be deleted
   outright with no loss?
