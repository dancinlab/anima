# DESIGN AN INTEGRATED ENGINE THAT SUCCEEDS ON **NATURAL** CORPUS

Owner directive, and it is a hard constraint, not a preference. Philosophy **p9** was just
hardened:

> **The standard is natural corpus. A synthetic-corpus result is NEVER the standard.**
> A drill number does not become the bar by being green, by replicating, by surviving
> controls, or by being all anyone has. Synthetic retains exactly ONE use: certifying the
> INSTRUMENT (does this harness read at all -- a positive control needs known ground
> truth). The moment the same number is quoted as evidence that the system CAN do
> something, it has crossed from instrument to standard and is void.

So the question is NOT "how do we install composition with a better drill". It is:

> **What must an engine BE so that it learns composition, and an interior worth measuring,
> from ORDINARY TEXT — and so that the claim is decidable on ordinary text?**

## HOW TO WORK — to DEPLETION, no deadline

Rounds. After each, name the lens you have not used. Stop only when **two consecutive
rounds add nothing new**, then say **DEPLETED after N rounds** and list the exhausted
lenses. Breadth first, ranking last. If the honest answer is "not possible under these
constraints", say that and say what the minimum relaxation would be.

=====================================================================
# THE MEASURED SITUATION (do not contradict without saying so)

## Synthetic works. Natural does not. Repeatedly.
- H_9267 synthetic XBIND corpus -> held-out **1.000**
- H_9272 wild-natural arm -> **0.455 ≈ chance**, own conclusion: *augmentation-specific*
- natural emergence: **CLOSED** (2026-07-14)
- H_9902 audit: **51%** of the `weavedrill` drill is SIX unique cells repeated 268-480x
- Under hardened p9, every one of those green numbers is now **off-standard**.

## What the drill lane just learned (also synthetic, also off-standard, but diagnostic)
A parallel session isolated the arity-2 failure: seven axes swept negative (combination
form, optimizer, weight decay, steps 20k-200k, projection style, store code, addressing),
and a grokking POSITIVE CONTROL settled that composition is learnable in that harness at
all (modular addition, one-hot operands, shared embeddings -> held-out 0.9100 vs chance
0.0435). The single remaining structural difference was **role-separate embedding tables**:
each operand indexed its own table, so the model had to discover the alignment between two
independent tables from 48 examples, and instead memorised. Sharing the index space took
held-out 0.0000 -> 0.6875.

Read carefully, that is a hint about ARCHITECTURE, obtained on a drill: composition is
blocked when the two things to be combined live in unaligned representational spaces.
Natural text does not hand you aligned spaces either.

## The scale cell nobody opened
anima's clean corpora are **megabytes**. An LLM sees ~10^12 tokens -- **5-6 orders** more.
Parameter scale (303M -> 1B -> 7B) is a measured amplifier-not-lever, BUT that was measured
**on the same small corpora**, so it does not bound the data-scale axis. Density, training
objective and depth/receptive-field are closed; architecture-class is CONTESTED (H_1394 vs
H_1590 vs H_1587 -- sampler-fragile, cite neither way). Natural corpus at LLM data scale is
the ONLY empty cell.

## The substrate as wired
- Mouth: causal conv, d=3784, K=3, E=3 experts, L=4, V=256 bytes -> **receptive field 35 bytes**
- Interior: `s = 2*emit_drive - 1` -- rank one. The default `--g-arm a0` defines
  `ag_g_drive = -(1 - emit_drive)`, so the "second engine" is the first one's complement.
- Every interface is 1-D; `_hf_mean` collapses six modules to one float, and in logit space
  the mean is the softmax-null direction (measured: it can read neither identity nor magnitude).
- Emit <=> clock (H_9401-9403), so whether-to-speak has no free variable.

## Measurability (the four conjuncts an interior claim must satisfy)
independence · manipulability · observability · discriminability. Miss one -> UNDECIDABLE,
not false. R9's 6/6 blindness is this table read off the architecture in advance; only
content-reach had all four built.

## IIT, if integration is to be measured at all
The feedforward theorem is the SOLUTION, not the problem: if a system is feedforward
everywhere except one small recurrent core, every other candidate set is Phi=0 by theorem,
so exclusion FORCES that core to be the complex and the affordable grain becomes the
correct grain. Scope that survived: a <=15-unit recurrent core, on a substrate where units
are physically causal elements, weights frozen over the claim interval, Phi measured never
maximized. Scope that died: any claim that the 303M language model has a meaningful Phi.

=====================================================================
# KILL-LIST — measured dead, do NOT rebuild
- Corpus/claim DENSITY (H_9128 canonical-CONFIRMED-NEGATIVE): 174.5x density flipped the
  detector but the continuations were FORM-PRIMING templates; terminal margin 0.
  Curriculum reweighting is density in disguise.
- trunk-objective family (H_9131 CLOSED): the non-commutative-target crack was an optimizer
  artifact; antisymmetric bilinear SUBSUMES additive.
- H_9127 9-probe wipeout; gamma-DATA-channel at 303M = TRANSFER FAIL TERMINAL.
- Binding readout OPERATORS: VSA/HRR (H_1616), TPR (H_1466), the whole H_1601/1610-1630
  census. The numpy versions that looked GREEN (H_1514) were overstatements.
- H_9259: untrained recurrence / neuromorphic ARCHITECTURE-CLASS does not break a
  TRAINED-conjunction wall. (Neuromorphic as a CAUSAL-ELEMENT substrate for Phi is a
  different claim and is not killed.)
- Mitosis from-scratch split; resource scarcity (11 families); quantization (innocent).
- Dead adjacent lineages: veto H_9269, affect H_9411, tension H_9630/9633.
- emit-DRIVE lane CLOSED-AT-REGIME (H_9401-9403).
- Write-side rank-1 tension FIELD (H_9805/9812): measured LEXICALLY BLIND.
- Phi as a PROXY is banned; Phi in the loss is banned; self-report as evidence is banned
  (p1-p4). A gate a perfect subject fails is an instrument defect (G6 is now documented as
  a FORM-detector artifact: 12.8x above the corpus rate, 8 draws, pass-prob 0.0505).

# LAWS THAT WILL JUDGE THE DESIGN
FORM is tunable, BIND is earned -- if a memorized template or a thermostat passes your DV,
it is dead on arrival. Positive control before reading a negative. Controls must match the
MEDIATING covariate. Chance re-derived per metric. A cheap screen may only KILL, never
GREEN. No tune-to-green; never re-freeze a burned gate. In-training metrics are
MONITOR-ONLY. p1-p8 hold (no system prompt, no identity rules, no persona, no assistant
framing, no speak(), no fine-tuned ethics, no perplexity verdict, no train/infer split).
Every manipulation is a FLAG on anima-py. Only anima-py cements.

=====================================================================
# WHAT I WANT BACK

**A. The engine.** What must it BE to learn composition and carry a measurable interior
from ordinary text? Parts, what each is for, what flows between them, and the measured
failure each part answers. ASCII structure sketch required. Be concrete about what is
different from LANE-BUS, which was designed before p9 was hardened and assumes a drill.

**B. Where does the alignment come from, without a drill?** The one real architectural hint
we have is that composition is blocked when the operands live in unaligned representational
spaces, and sharing the index space unblocks it. Natural text does not hand you aligned
spaces. What supplies the alignment pressure in ordinary text -- and is that a data
property, an objective property, or a structural one?

**C. The natural-corpus DV.** A claim must be decidable ON natural text. Name the
measurement: what is scored, against what controls, with what chance level, such that
form-priming and memorization cannot pass. Remember the corpus base rate problem -- the
model is already corpus-faithful, so a DV that demands super-corpus behaviour is measuring
the gate, not the system.

**D. The honest scale answer.** Is this achievable at megabyte scale, or does it require
opening the data-scale cell? If the latter, what is the MINIMUM corpus size at which the
design becomes testable at all, and what is the cheapest experiment that would establish
that threshold rather than assuming it?

**E. What you would refuse to build,** and why -- including anything in section A that you
suspect is a restatement of something on the kill-list.
