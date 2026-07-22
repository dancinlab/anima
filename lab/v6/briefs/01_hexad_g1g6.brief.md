# QUESTION
Would the G1 and G6 walls SURVIVE if anima ran on the HEXAD 7-module architecture
instead of / on top of the bare conv mouth? Answer per-wall, and name the ONE
structural change to HEXAD that would have the best chance of breaking each.

Give a decisive verdict (SURVIVES / BREAKS / UNDECIDABLE-AS-SPECIFIED) per wall,
with the load-bearing structural reason. Be adversarial: try to REFUTE the claim
that HEXAD changes nothing. Do not regenerate angles on the kill-list.

# GROUNDED FACTS (read from the repo today — do not contradict without saying so)

## HEXAD structure (HEXAD/hexad.hexa, HEXAD/hexad_forward.hexa, HEXAD/CLAUDE.md)
- 7-module brain on perfect number 6: sigma(6)=12 active inter-module connections,
  phi(6)=2 gradient partition {A, G}, tau(6)=4 phases.
- Engine G (gradient-FREE, "right brain"): C consciousness (IIT Phi), S perception
  (= C state-delta), W will (pain/curiosity -> learning-rate).
- Engine A (CE-trained, "left brain"): D language (decoder = the actual mouth),
  M memory (Hebbian), E ethics (Phi-ratchet safety gate).
- ThalamicBridge = the G->A main connection, Psi=1/2 clamp (Law 70).
- Forward graph is literally: S -> C -> Bridge.detach() -> D, with M/W/E as OBSERVERS.
- CRITICAL 1: `Bridge.detach()` — the G->A link carries NO gradient.
- CRITICAL 2: HEXAD's M module has NO store. From HEXAD/M/README.md + m.hexa:
  `m_store(key,value)` is an identity NO-OP ("Hebbian in C is the storage");
  `m_retrieve_topk` = cosine top-k over C's CURRENT cell states; null branch returns zeros.
  B-M-1 is literally "STORE-NOOP-STRUCTURAL".
- CRITICAL 3: HEXAD's own `generate` slot is an honest STUB. The byte MOUTH (D
  byte-logits decode) is ckpt-gated and is performed by the core/ conv engine
  (clm_decode + generator L3). HEXAD 7/7 BLUE is a FORMAL verification spine;
  real mouth inference runs on core/.

## The mouth that D actually is (measured today from the real ckpt headers)
- py303_full.clm / py303_savant_mitosis.clm / rv3c13.clm ALL: nblk=10, d=3784,
  K=3, E=3 experts, L=4 trunk layers, V=256 bytes.
- Wiring (core/model.py): embed_conv dil=1; trunk dilations 1,2,4,8; ConvExpert dil=1;
  router+readout kernel=1. => receptive field = 1 + 2 + (2+4+8+16) + 2 = 35 BYTES.
  (~11 Korean chars.) DIRECTIONAL derivation, not an anima-py verdict.
- NOTE a record correction landed today: the old note "production .clm = E2/L1"
  described the OLD d768 golden reference (nblk=6), NOT the 303M ckpts. So RF is
  35B, not 3B.

## G1 (recombination / operator<->declaration binding) — what is measured
- G1 = COMPOSITION ABSENCE, not failure: across all 212 items / 848 decodes,
  reach = 0/212, AND all 3 controls (atom-swap, bind-strip, unreachable) also 0.
  95% upper bound 1.42% (bar 0.30 is 21x outside). The model neither composes
  wrongly nor leaks surface echo.
- Cause converges on the CORPUS from 3 directions: 0/212 + H_9304 non-additive
  info only +0.0023 nats (TOST-equivalent to 0) + H_9267 a SYNTHETIC XBIND corpus
  gets held-out D-acc 1.000.
- H_9359: the wall's identity = ABSENCE of an operator<->declaration RUNTIME BRIDGE.
- H_9346: binding is NOT morphology — free pre-posed `not` walls too.
- H_9875: runtime study/injection cannot combine two facts; the wall is BINDING
  ARITY (how many things must be bound at once), NOT budget (4x budget excluded).
- H_9775 (GREEN WIRED, the ONE thing that worked): a CO-TRAINED content-addressed
  store-bridge (CLMS/pairodd) writes the answer-position logits row directly.
  In-vivo 2/2 majority (0.8176, 0.8933); all controls collapse; value-permute
  0.4446 = content-addressed value TRANSPORT confirmed 128/128.

## G6 — what is measured
- G6 is NOT a faculty wall, it is a CORPUS-DENSITY wall (measurement #4253):
  the model DOES generate falsifiable claims at 1/241 = 0.0041, faithful to the
  corpus rate 0.0065 (P=0.539). The gate needs 0.083 = 12.8x outside
  (P(<=1 | p>=0.083) = 4.3e-8). The wall is the INPUT, not the substrate.

# KILL-LIST (dead angles — do NOT propose these)
- G1 read-side is EARNED TERMINAL: 6 lanes + gamma + depth-RF all hit the floor.
- H_9259: untrained recurrence / neuromorphic arch does NOT break G1 — the wall is
  TRAINED-conjunction, not architecture-class.
- Scale (303M -> 1B -> 7B) is an AMPLIFIER of a working lever, never itself a lever.
- Mitosis wall = estimator class (growth pays, from-scratch split is dead).
- Resource scarcity / organelle lane is not a G1 lever (11 families tested).
- Quantization is innocent (fp32 + exact still gives G1 = 0).
- Engine/detector/decode are byte-INNOCENT on 3 axes; the culprit is training/data.
- A veto lane (H_9269), an affect lane (H_9411), a tension lane (H_9630/9633) are
  all dead lineages — do not resurrect as "HEXAD E/W module will do it".
- Post-theta-alive interior faculties R9 6/6 closed: self-anchor VOID, agency
  UNIDENT, sigma-flux INSTRUMENT-DEAD, imagination reaches interior but NOT the mouth.

# WHAT I WANT BACK
1. G1 under HEXAD: SURVIVES / BREAKS / UNDECIDABLE + the load-bearing reason.
2. G6 under HEXAD: same.
3. The single highest-yield STRUCTURAL modification to HEXAD per wall (must be a
   flag/lane on the engine, must be falsifiable, must not be on the kill-list).
4. Explicitly attack this claim: "HEXAD is a formal verification spine wrapped
   around the SAME conv mouth, therefore it cannot move a wall whose cause is
   corpus composition + a 35-byte receptive field." Is there ANY path by which
   the sigma6 graph changes the answer? Name it or concede.
