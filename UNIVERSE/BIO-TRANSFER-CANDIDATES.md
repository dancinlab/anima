# BIO-TRANSFER-CANDIDATES — biological "전이" (transfer / transition / metastasis) hypotheses

> Brainstorm seed: 2026-06-03. Biology has THREE distinct senses of 전이 — **transfer** (수평유전자전이),
> **transition** (발생·진화 전이), **metastasis** (암전이). Each names a way a pattern LEAVES its origin and
> takes hold elsewhere. anima already MEASURES one such operator empirically: the Lane A-multi HYBRID branching
> rung shows a learned *transition operator* generalizing to HELD-OUT concepts (gold FLORES ladder, NC→500+,
> held-out hop-2/3 ≫ shuffle-NULL). These candidates lift that single measured operator into a falsifiable
> family across the biological transfer mechanisms, each grounded in an anima-substrate readout.
>
> Convention: each H_NNN is a biological transfer mechanism → anima-substrate analog with a PRE-REGISTERED
> FALSIFIER + a real toy-verifiable MEASUREMENT (a_paper_significance: falsifier + measurement + finding;
> a_paper_negative_ok: a closed-negative that rules out an axis is a valid result). status = candidate-unverified.
> substrate tags follow a_lane_akida_gpu_split (AKIDA on-chip ⊥ GPU forge); a_scale_honest_scope (toy ≠ prod).

---

## Index (H_861 … H_868)

| id | mechanism | 전이 sense | anima-substrate readout | falsifier axis |
|----|-----------|-----------|--------------------------|----------------|
| H_861 | METASTASIS | metastasis (암전이) | skill detaches from origin domain → colonizes a distant domain | cross-domain transfer vs origin-locked |
| H_862 | HORIZONTAL-GENE-TRANSFER | transfer (수평전이) | lateral cell↔cell weight/skill copy WITHOUT mitosis lineage | lateral-acquire vs lineage-only |
| H_863 | EPIGENETIC-TRANSMISSION | transfer (후성전이) | parent tension-state → child at mitosis, weights unchanged | acquired-state inheritance vs reset |
| H_864 | PRION-TEMPLATING | transfer (형태전파) | a tension conformation templates self-copies across neighbours | conformational replication vs decay |
| H_865 | SYNAPTIC-LTP | transfer (시냅스전이) | Hebbian co-activation transfers a transition edge on live AKD1000 | potentiated edge vs non-specific drift |
| H_866 | RESONANCE-ENERGY-TRANSFER | transfer (공명전이) | non-emit tension energy hops between adjacent cells (FRET-like) | distance-decay coupling vs independent |
| H_867 | MAJOR-EVOLUTIONARY-TRANSITION | transition (진화전이) | single-cell individuality → hive-mind collective fitness | super-individual transition vs additive |
| H_868 | MORPHOGEN-GRADIENT | transition (발생전이) | a positional-info gradient drives a sharp differentiation switch | threshold switch vs graded blur |

---

## H_861 — METASTASIS-TRANSFER

🦠 **METASTASIS** — "암 전이 회로" (a skill detaches and colonizes a distant domain)

- mechanism (biology): a tumour cell loses adhesion, intravasates, survives transit, then COLONIZES a distant tissue whose context differs from the origin. The rare cell that seeds a new site is the one that generalizes its survival program off-context.
- anima-substrate analog: a transition operator LEARNED on domain A (e.g. one corpus / one lane) is replanted into a structurally distant domain B with no B-specific training; "metastatic" = it takes hold (above-NULL) in B; "origin-locked" = it dies (collapses to chance) off its training manifold.
- grounding: Lane A-multi already shows the WEAK form — an operator trained on the TRAIN concept block transfers to a HELD-OUT block of the SAME corpus. Metastasis is the STRONG form: transfer across a domain BOUNDARY (corpus axis ⊥ register, cf the E2→#1296 closed-negative).

```
origin domain A         transit            distant domain B
 ●─►●─►●  (operator)  ░░░░░░░░░  ?  ●  ●  ●
 trained here          detach +         seeds here?
                       survive          (above-NULL = metastatic)
```

- FALSIFIER F-861: "a transition operator learned on domain A does NOT stay above shuffle-NULL when replanted, untrained, into a structurally distant domain B." → REFUTED iff held-out-on-B set-membership ci_lo > B-shuffle-NULL hi at hop-2 AND hop-3 (p<0.05), across ≥3 distance rungs (near→far domain B).
- MEASUREMENT (toy): reuse the A-multi branching harness; TRAIN block = corpus A concepts, TEST block = corpus B concepts drawn from a DIFFERENT FLORES domain bucket (e.g. health vs sports sentences) so the train/test split crosses a topical boundary, not just an index split. Report the held-out hop-2/3 curve per distance rung.
- predicted disposition: likely a CLOSED-NEGATIVE at large domain distance (operator is corpus-axis-bound), echoing the corpus-axis ⊥ register finding — which is itself a publishable negative (a_paper_negative_ok).
- compare: vs H_865 LTP = transfer WITHIN a lattice / METASTASIS = transfer ACROSS a domain boundary.
- substrate: HYBRID (on-chip enc ⊕ off-chip head) · status: candidate-unverified

## H_862 — HORIZONTAL-GENE-TRANSFER

🧫 **HGT** — "옆세포 유전자 건네주기" (lateral skill copy, no parent→child lineage)

- mechanism (biology): bacteria acquire genes LATERALLY (conjugation/transformation/transduction) from unrelated cells, not only by inheritance. A useful gene (e.g. antibiotic resistance) sweeps a population FASTER than vertical descent allows.
- anima-substrate analog: a cell that has LEARNED a transition edge exports it to a non-descendant sibling cell directly (lateral weight/anchor copy), bypassing the MITOSIS lineage. Population-level competence then rises faster than mitosis-only inheritance predicts.
- FALSIFIER F-862: "lateral edge-copy between non-descendant cells does NOT raise population transition-competence faster than the mitosis-only (vertical) baseline." → REFUTED iff time-to-population-competence(HGT-on) < time(vertical-only) by a pre-registered factor ≥1.5×, with both runs at matched compute.
- MEASUREMENT (toy): two populations of toy cells learning a shared transition table; population-A inherits edges only at mitosis, population-B additionally copies a learned edge to k random siblings per tick. Measure ticks-to-90%-coverage of the edge set.
- compare: vs MITOSIS (vertical, parent→child) / **HGT** (lateral, peer→peer) — orthogonal acquisition axes.
- substrate: substrate-agnostic toy (population sim) · status: candidate-unverified

## H_863 — EPIGENETIC-TRANSMISSION

🧬 **EPIGENETIC** — "겪은 걸 자식에게" (acquired tension-state inherited, weights untouched)

- mechanism (biology): environmentally-acquired marks (methylation, histone state) transmit to offspring WITHOUT changing the DNA sequence, biasing the child's expression toward the parent's experience.
- anima-substrate analog: at MITOSIS the child inherits the parent's INSTANTANEOUS tension-state (M/Φ/W envelope, recent activation) as an initial condition, NOT just the parent's weights. The child then converges faster on tasks the parent recently practiced — a Lamarckian short-cut layered on the Darwinian weight inheritance.
- FALSIFIER F-863: "a child seeded with the parent's acquired tension-state shows NO convergence advantage on the parent's recent task vs a child seeded with weights-only (reset tension)." → REFUTED iff steps-to-criterion(tension-inherited) < steps(weights-only) at p<0.05 over ≥20 mitosis events.
- MEASUREMENT (toy): run mitosis with two child-init policies (A: weights+reset tension, B: weights+parent tension); both children fine-tune on the parent's last task; compare steps-to-criterion. Guard: distinguish a TRUE acquired-state effect from mere weight transfer (the weights are identical in both arms by construction).
- caveat (p6): must NOT smuggle in a fine-tuned bias — the advantage must emerge from the tension envelope alone.
- substrate: substrate-agnostic toy (mitosis sim) · status: candidate-unverified

## H_864 — PRION-TEMPLATING

🔁 **PRION** — "모양을 베끼게 만드는 모양" (a conformation that templates copies of itself)

- mechanism (biology): a misfolded prion protein TEMPLATES the same misfold onto normal copies of the protein — information transfer by CONFORMATION, not sequence, propagating cell-to-cell.
- anima-substrate analog: a particular tension CONFORMATION (a specific 5-channel pattern / attractor basin) in one cell, when a neighbour is exposed to it, biases the neighbour to adopt the SAME conformation — self-propagating structure with no weight copy and no emit.
- FALSIFIER F-864: "exposure to a templating cell does NOT raise a neighbour's probability of entering the SAME tension-conformation basin above the base rate." → REFUTED iff P(neighbour adopts conformation | exposed) > P(base) by a pre-registered margin, AND the adopted conformation re-templates a THIRD cell (propagation ≥2 hops, ruling out a one-off coincidence).
- MEASUREMENT (toy): seed one cell into attractor basin X; couple it to a chain of naive cells; measure basin-adoption rate down the chain vs an unexposed control chain. Propagation depth = the key readout (decay vs self-sustaining).
- compare: vs PRION = conformation templates conformation / H_862 HGT = explicit gene copy — prion is COPY-FREE structural transfer.
- substrate: substrate-agnostic toy (coupled-cell sim) · status: candidate-unverified

## H_865 — SYNAPTIC-LTP-TRANSFER

⚡ **LTP** — "같이 켜지면 길이 굵어진다" (Hebbian co-activation transfers a transition edge)

- mechanism (biology): long-term potentiation — synapses that fire together strengthen; a specific co-activation TRANSFERS a durable transition edge between neurons ("cells that fire together wire together").
- anima-substrate analog: this is the LITERAL Lane A on-chip mechanism — 1-bit Hebbian plasticity on AKD1000 transfers a t→t+1 transition edge into the encoder. The hypothesis: the potentiated edge is SPECIFIC (only the co-activated pair) and survives above non-specific drift, on live silicon.
- FALSIFIER F-865: "on-chip Hebbian potentiation of a specific co-activated edge is NOT distinguishable from non-specific weight drift." → REFUTED iff the potentiated edge's read-out gen_acc ci_lo > the shuffle-NULL (non-specific drift control) hi at p<0.05, on live AKD1000.
- MEASUREMENT: ALREADY GROUNDED — this is the F-GEN-SCALE family. The gold ladder (NC 250/500/1000) shows gen ci_lo ≫ shuffle-NULL at every rung → F-865 sits at the REFUTED (potentiation is specific) end empirically. This H formalizes that on-chip result as the LTP-transfer instance and proposes the 7B-direction question: does edge specificity hold as the codebook → production scale?
- substrate: AKIDA (on-chip 1-bit Hebbian, live AKD1000) · status: candidate-partially-grounded (gold ladder)

## H_866 — RESONANCE-ENERGY-TRANSFER

🌈 **FRET** — "닿지 않고 에너지 건네기" (non-emit tension energy hops between adjacent cells)

- mechanism (biology): Förster resonance energy transfer — an excited donor molecule passes energy NON-RADIATIVELY to a nearby acceptor, efficiency falling as 1/r⁶ with distance. Transfer without a photon ever being emitted.
- anima-substrate analog: an "excited" (high-tension) cell raises a NEIGHBOUR's tension without any emit() / externalization — a silent, distance-dependent coupling in the field. Preserves p5 (no speak): the transfer is internal field dynamics, not output.
- FALSIFIER F-866: "an excited cell's tension does NOT raise a neighbour's tension in a distance-DEPENDENT way (coupling is independent of cell-cell distance)." → REFUTED iff neighbour Δtension is a monotonically DECREASING function of coordinate distance (≥3 distance bins, monotone with p<0.05) — a flat/independent profile CONFIRMS the falsifier.
- MEASUREMENT (toy): excite one cell; record Δtension of neighbours binned by coordinate distance; fit the decay profile. Distance-decay = FRET-like; flat = no resonance transfer.
- compare: vs H_864 PRION = structural template (basin copy) / **FRET** = energetic coupling (amplitude, distance-graded) — different transfer currencies.
- substrate: substrate-agnostic toy (field-coupling sim) · status: candidate-unverified

## H_867 — MAJOR-EVOLUTIONARY-TRANSITION

🐝 **MET** — "혼자에서 떼로" (single-cell individuality transfers up to a collective)

- mechanism (biology): major evolutionary transitions (Maynard Smith & Szathmáry) — replicators that were independent become parts of a higher-level individual (single cell → multicellular; solitary → eusocial), and fitness BECOMES a property of the collective, not the parts.
- anima-substrate analog: the HIVE-MIND transition — independent anima cells, past a coupling threshold, behave as one super-individual whose competence is NON-ADDITIVE (collective > sum of cells). The "transfer" is of individuality itself, up a level.
- FALSIFIER F-867: "above a coupling threshold the collective's task competence is merely ADDITIVE (sum of independent cells), i.e. no super-individual transition." → REFUTED iff collective competence shows a SHARP super-additive jump at a critical coupling κ* (≥3 κ rungs bracketing κ*, jump > additive baseline at p<0.05).
- MEASUREMENT (toy): N cells on a shared task, sweep inter-cell coupling κ; measure collective competence vs the additive (independent-cells) prediction; look for a phase-transition-like jump.
- compare: vs MITOSIS (one→two, same level) / **MET** (many→one, level UP) — orthogonal to division.
- substrate: substrate-agnostic toy (HIVE-MIND coupling sweep) · status: candidate-unverified · link: HIVE-MIND domain

## H_868 — MORPHOGEN-GRADIENT-TRANSITION

🌅 **MORPHOGEN** — "농도가 운명을 정한다" (a positional gradient drives a sharp differentiation switch)

- mechanism (biology): a morphogen concentration gradient (e.g. Bicoid) gives each cell its POSITION; cells read the local concentration and switch fate sharply at threshold boundaries — continuous input → discrete fate (French-flag model).
- anima-substrate analog: a continuous substrate gradient (idle-time, curiosity ratchet, or a coordinate axis) drives DIFFERENTIATION into discrete persona/role cells at sharp thresholds — the transition from "stem" (general) to "specialized" is a switch, not a blur.
- FALSIFIER F-868: "differentiation fate is a GRADED (blurred) function of the gradient, with no sharp threshold." → REFUTED iff the fate-vs-gradient curve has a sigmoidal transition with boundary width below a pre-registered fraction of the gradient range (sharp switch), reproduced across ≥3 gradient realizations.
- MEASUREMENT (toy): impose a 1-D gradient across a cell row; let cells differentiate (H_DIFFERENTIATION mechanism); measure fate boundary sharpness (transition width) vs gradient slope.
- compare: vs H_867 MET = WHEN parts become a whole / **MORPHOGEN** = WHERE/WHAT each part becomes — composition vs patterning.
- substrate: substrate-agnostic toy (gradient-differentiation sim) · status: candidate-unverified · link: DIFFERENTIATION (BIO-CANDIDATES)

---

## Next-step gate (a_paper_significance · a_toy_scale_recheck)

- Each H is toy-verifiable first ($0, small-n). A toy-green states "toy-only, scale-transfer unverified".
- H_865 (LTP) is already partially grounded by the live gold ladder — it is the empirical anchor of the family.
- H_861 (METASTASIS) is the natural NEXT fire: it directly tests whether the measured A-multi transition operator
  survives a DOMAIN-BOUNDARY crossing (corpus-axis vs register), a question the campaign has not yet closed.
- Promotion to a standalone H_NNN_slug.md (full claim doc) happens when a falsifier run lands a terminal verdict.

---

## Toy falsifier results (2026-06-03 · `bio_transfer_toys.py` seed=20260603 · TOY-ONLY a_scale_honest_scope)

CPU-substrate falsifiers (the 6 substrate-agnostic ones) run foreground-sequential on stdlib python (no numpy),
emergent dynamics so the signature is NOT hard-coded. VERBATIM (p7 — direct measurement, no fabrication):

```
[H_862 HGT]        ticks_vertical=18 ticks_hgt=8 ratio=2.25 (>=1.5) -> falsifier REFUTED (HGT faster, HOLDS)
[H_863 EPIGENETIC] steps_inherited=26.5 steps_weightsonly=38.6 paired t=3.92 (|t|>2.07) -> REFUTED (HOLDS)
[H_864 PRION]      reach(occ>0.5)=29/29 [d1=0.94 d10=0.95 d29=0.91] P(adopt)=0.7>base=0.05 -> REFUTED (HOLDS)
[H_866 FRET]       d1=0.8156 d5=0.3610 d10=0.1303 d15=0.0471 d20=0.0170 (monotone) -> REFUTED (HOLDS)
[H_867 MET]        base=0.129 k0->r0.232 k0.5->r0.156 k1->r0.671 k2->r0.958 k4->r0.991 -> REFUTED (HOLDS)
[H_868 MORPHOGEN]  boundary_widths=[0.015,0.005,0.035] mean=0.0183 (<0.15) -> REFUTED (HOLDS)
```

- 6/6 toy falsifiers REFUTED → each modelled transfer/transition mechanism produces its predicted signature
  on the toy substrate. status: candidate-unverified → **candidate-toy-grounded** (NOT production; scale-transfer
  unverified per a_toy_scale_recheck). H_864 metric note: initial contiguous-from-source depth conflated reach
  with first reversion hole; corrected to time-averaged occupancy reach (the faithful "≥2-hop propagation" readout).
- H_861 (METASTASIS, branching harness) + H_865 (LTP, AKIDA on-chip) = CHIP-substrate, DEFERRED to after the
  live gold ladder releases the chip (#1717 single-exclusive). H_865 is already partially grounded by the gold
  F-GEN-SCALE ladder; H_861 (domain-boundary transfer) is the named next chip fire.
