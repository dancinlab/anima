# fork-A CLML lane — wall reached. Break it or confirm terminal.

You (Fable) designed the swap-margin bar and the counterfactual-retrain success path for the anima G1
recombination frontier. Both have now run engine-native on the 303M byte-LM. **Result: NO-CRACK, even on the
retrained lane.** I need you to either (a) name a genuinely DIFFERENT mechanism-family that is not already
falsified by this evidence, or (b) confirm this is terminal (fork-A CLOSED) with a $0 argument.

## The frontier (recomb-routing-lane, card H_9235)
G1 = two concepts D (distal, established early) + R (recent) must RECOMBINE at a generation point beyond D's
receptive field. Reframed as a READOUT-ROUTING wall (not representation capacity): a causal cumulative
mean-pool over hidden states recovers BOTH concepts (probe acc D=0.95 B=0.97, Gate2), but the last/generation
position only retains the recent concept (RF decay). fork-A = a read-side lane, DISJOINT from emit-drive:
  c_t = causal cumulative mean of yn(0..t)         # pool that provably contains D
  logits += clip( g_t · gelu(c_t·W1+b1)·W2, ±tau ) # gated tether-clip logit bias, g_t=σ(w_g·[yn_t;c_t]+b_g)
Only the GATE sees yn_t; byte-selection must route through the pool c_t. Trained frozen-trunk (only lane params).

## What passed
- Gate1: base CE 1.044, residual headroom exists.
- Gate2: probe on the pool recovers held-out concepts 0.60 >> chance 0.04 — the pool IS routable + generalizes.
- Gate3: lane trained, CE 1.044 -> 0.718 (Δ-0.33) — the lane LEARNS something.

## What failed (the two verdicts)
- Gate4 (system-G1 coverage): lane-ON == lane-OFF byte-identical, coverage 0/24. UNINFORMATIVE — anima's frozen
  mouth emits substrate-native persona content and IGNORES the concept seed, so a keyword-coverage bar is an
  LLM-frame-trap (measures seed-completion the mouth never does), zero dynamic range, no positive control.
- SWAP-MARGIN (your immune-to-additive-floor design): per pair, m = CE(swap) - CE(match); Δ = mean(m_ON - m_OFF).
  A swap difference is a 2-way interaction, so any main-effect/additive logit bias cancels — only genuine
  distal-D routing gives Δ>0. Controls: pool-SHUFFLE (permute context hiddens before pool) and zero vs lit overlap.

### Result on the ORIGINAL trained lane: no-crack (Δ_zero on +0.025, shuf +0.017, CI∋0).
### Result on the COUNTERFACTUAL-RETRAINED lane (your designed success path — fresh init NOT warm-start, 48
   concept-disjoint training concepts, FILLER+DISTAL-kw+GAP≥RF+STEM→target, 70/30 retrieval/associative,
   anti-copy, geometry-matched eval lengths, Adam 1e-3→3e-4 cosine, 4 epochs; retrain landed clean, lane
   CE learned): **STILL no-crack**:
      on    Δ_zero = +0.0282   CI[-0.0126, +0.0646]      (CI includes 0)
      shuf  Δ_zero = +0.0295   CI[-0.0141, +0.0690]      (on ≈ shuf, EXACTLY)
      g2/g4/g8: the shuffle-invariant delta scaled linearly (0.052 / 0.098 / 0.196), CI always ∋ 0, Δ_lit negative.
   The pre-registered killer fired: **on ≈ shuf** → the lane's effect is INVARIANT to shuffling the pool's
   content, i.e. it is generic smoothing, NOT routing of D's concept content into the readout.

## The question
The swap contrast is structurally immune to the additive-floor family that killed every prior G1 lever
(main-effect logit ≡ trunk-CE ≡ the falsified family). A fresh-init counterfactual-CE retrain on the pool that
provably contains D still cannot make the frozen 303M readout PREFER the D-dependent continuation over a swap,
beyond what shuffling the pool gives. 

1. Is there a mechanism-family that is NOT (a) an additive main-effect bias, (b) a shuffle-invariant smoother,
   (c) already-falsified (trunk-objective bake γ H_1840 STEP-0 frozen-gate killed, MLC episodic H_1835 floor,
   PC-binding H_1816 floor, coverage-density)? If yes, specify it concretely enough to implement as a lane
   variant + its own falsifiable swap-margin-style bar, AND say why it escapes the on≈shuf trap.
2. If no — state the terminal claim precisely: what exactly is CLOSED (fork-A readout-routing lane class),
   what remains genuinely open (if anything), and why this is a SCOPED wall (this lane class + frozen readout)
   not a proof of trunk-G1 ceiling. Give the $0 argument.

Be adversarial with your own prior design. Do not force-fit a rescue. Terminal is an acceptable answer.