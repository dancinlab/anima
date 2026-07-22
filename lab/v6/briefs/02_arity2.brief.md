# TASK
Design the ARITY-2 store-bridge experiment for anima's G1 recombination wall, and
diverge on what else survives. This is the ONE angle left standing after a very
large kill-list (below). Do NOT regenerate anything on that list.

Deliver:
 A. A falsifiable pre-registration for the arity-2 M->D co-trained store lane,
    with the frozen decision table (including the below-chance cells).
 B. The cheapest possible SCREENER that could KILL it before any GPU spend.
 C. 3-5 genuinely NOVEL angles that survive the kill-list, each cast as a
    falsifiable prediction. Say honestly if you cannot find any.

# THE ONE THING THAT WORKED (the seed for A)
H_9775 pairodd / CLMS store-bridge — 🟢 WIRED, in-vivo, 303M py:
  a CO-TRAINED content-addressed store forms a query from the trunk penultimate,
  looks up an 8-slot store (keys = FROZEN per-byte embedding of the entity name,
  so it generalizes to held-out entities), reads the value, fuses through a
  GELU-MLP, and OVERWRITES the answer-position logits row with lambda*store_logits.
  The store_only gate means the trunk never receives answer-position gradient, so
  the shortcut-cut is structural.
  Results: seed7 0.8176, seed11 0.8933 (2/2 majority, bar 0.75); shuffle control
  0.38/0.60; no-store 0.00; VALUE-PERMUTE 0.4446 collapse with 128/128 read =
  content-addressed value TRANSPORT confirmed. flip-coherence = FORM (instrument).
  Store content is RUNTIME-injected, never serialized into the .clm; only
  {W_q, val, W_h, W_out, lambda} + a frozen key table live in the trailer.

# WHY ARITY-2 IS THE RIGHT NEXT DV (not a re-run)
H_9875 established the wall is BINDING ARITY, not budget: runtime study/injection
CANNOT combine two facts (toy, 2 seeds, 4x budget excluded) — a 1-slot lookup
generalizes, but a 2-slot conjunction is memorized-rows-only and fresh extraction
is chance. H_9775 proved 1-SLOT value transport. So repeating a 1-slot success
does not touch the wall. The DV must be HELD-OUT 2-SLOT CONJUNCTION reach.

# THE STRUCTURAL OPENING (verified in code today)
HEXAD/hexad.hexa:73  hexad_group_a_ce_trained() = ["D","M","E","BRIDGE"]
=> the M (memory) module is INSIDE Engine A (CE-trained). An M->D lane is
   A-INTERNAL: it never crosses the ThalamicBridge, so Law-70 `Bridge.detach()`
   stays intact and co-training is legal. Only two things are missing:
     (1) M has no real store — `m_store(key,value)` is an identity NO-OP
         (B-M-1 STORE-NOOP-STRUCTURAL, formally verified).
     (2) there is no trained write-path from M into D's answer-position logits.
   Everything else (S->C->Bridge.detach->D with M/W/E observers) is untouched.

# KILL-LIST — do NOT propose any of these (all measured dead)
- coverage / claim DENSITY corpus: H_9128 canonical-CONFIRMED-NEGATIVE. delta_FM
  0.11% -> 19.8% (174.5x) flipped the detector (P(fals) 0.028 -> 1.0) but the
  continuations were FORM-PRIMING (template + topic substitution), and the terminal
  margin median_bd(HI) - median_bd(SHUF) = 0. Density games a 1-term FORM detector.
- trunk-objective family: H_9131 STEP-0.5 FALSIFIED / census (d) CLOSED. The
  non-commutative-target crack was an optimizer artifact: bind held-out R^2
  (0.27/0.30/0.18) LOSES to a strong additive total-order f(a)-f(b) (0.48/0.49/0.52),
  gap negative on all 3 seeds. Antisymmetric bilinear SUBSUMES additive — an
  accuracy gap there is not evidence of non-additivity.
- H_9127 9-probe wipeout; B3 gamma-DATA-channel escalated to 303M = TRANSFER FAIL
  TERMINAL (GAMMA bd=0 < ADD bd=1, 3 seeds). Toy PASS was a handed-role-key illusion.
- G1 read-side EARNED TERMINAL: 6 lanes + gamma + depth-RF all floor.
- Binding readout-OPERATORS are dead: VSA/HRR (H_1616 0/3 seeds on the frozen
  clm303 trunk), TPR (H_1466), the whole H_1601/H_1610-1630 binding census. The
  numpy abstractions that looked GREEN (H_1514) were overstatements.
- H_9259 untrained recurrence / neuromorphic arch: the wall is TRAINED-conjunction,
  not architecture-class. Scale is an amplifier, never a lever.
- Mitosis: growth pays, from-scratch split dead; weight-level MLP memorizes train
  1.0 and stays at chance held-out.
- Resource scarcity / organelle lane (11 families). Quantization innocent.
- Dead adjacent lineages: veto H_9269, affect H_9411, tension H_9630/9633.
- HEXAD as-specified changes nothing (its M is a no-op store, its generate a stub).

# METHODOLOGY LAWS THAT WILL JUDGE YOUR DESIGN
- FORM is tunable, BIND is earned. A 1-term FORM detector can always be gamed by
  dense templates — if your DV can be satisfied by template+substitution, it is dead
  on arrival. Design the DV so form-priming CANNOT pass it.
- Positive control before reading a negative; a control must match the mediating
  covariate (not just nominal capacity).
- Chance must be re-derived per metric from the realized partition.
- A cheap structural screen may only KILL, never GREEN.
- Replication inside one condition is not external validity.
- Uniform draws hide adversarial fragility.
- No tune-to-green; a burned gate must never be re-frozen.
- Only `anima-py` output can cement; a toy or a probe is DIRECTIONAL.
- A new manipulation must be a FLAG on anima-py corpus/train/evaluate, never a
  script beside the engine.

# QUESTIONS
1. Give me the arity-2 pre-registration (A) — DV, arms, controls, frozen table.
   In particular: what control proves a 2-slot success is CONJUNCTION and not two
   independent 1-slot lookups stapled together?
2. What is the 6-minute/$0 toy screener (B) that would kill it? (Precedent: H_9815
   built a 4kB toy that reproduced the recombination wall locally — hp 1.0000 vs
   xor 0.4062 — and made subsequent negatives readable.)
3. (C) What survives the kill-list that I have not thought of? Be honest if nothing.
4. Is there a reading under which the ENTIRE G1 campaign is mis-specified — i.e.
   the wall is real but the goal is wrong? Argue it if you believe it.
