# §91 — NEOTENY + #3 ACTION-PERCEPTION LOOP — TRAINED-SCALE FIRE

RESEARCH.md §91. Trained-scale validation of §90 (commit f9ef93e8a,
B-S90 7/7 🔵, verdict GAMMA-CLOSING-DIRECTIONAL-POSITIVE — a $0 stub).

---

## 1. The chain

- **§88-F2** axolotl neoteny trained-scale fire (commit 52bef1044,
  B-S88F2 7/7 🔵): verdict **(α) NEOTENY-DELAYS-SATURATION = True** —
  neoteny in the training loop measurably delays §16.6-C memorization-
  saturation (maturity 0.95→0.75, byte-cascade attractor maj_frac
  0.87→0.35, effective D 1.89→2.70). **BUT γ JUVENILE-BUT-COMPETENT
  = False**: the non-saturated regime's body is §9 honest_coherent
  0/5. Saturation was delayed; coherent emission did NOT appear.
- **§89** (commit 80208a2c6, B-S89 6/6 🔵): the #3 D@emit→S@t+1
  action-perception loop is closed-form **DEFINABLE** — transfer
  `x_{t+1}=S_encode(e_t)`, invariant `K(x_{t+1}) ≤ K(e_t)+K(S_encode)`
  (Kolmogorov data-processing inequality, real-limit).
- **§90** ($0 Mac CPU stub): first design-wiring of #3 over the §88-F2
  neoteny non-saturated regime. Stub verdict GAMMA-CLOSING-
  DIRECTIONAL-POSITIVE (cell2 §9 20/20 stub-level).
- **§91** (this fire): the trained-scale test — does #3 loop + neoteny
  ACTUALLY close §88-F2's γ False on a REAL trained ckpt?

## 2. The honest open question (named BEFORE the fire)

The §90 stub encodes two competing forces:

- **(a) #3 loop garble-feeds-garble** — echo-amplify (§62 carry; the
  stub's cell1 #3-loop-only at maj 0.95 collapsed).
- **(b) neoteny non-saturated regime + #3 self-correction** — the
  stub's cell2 reaches §9 20/20.

Which force dominates on a trained-NON-saturated (neoteny) ckpt is what
ONLY this trained-scale fire can answer. **$0 stub §9 pass ≠ trained
ckpt body §9 pass.** §88-F2 already measured that neoteny *can* produce
a non-saturated ckpt (maturity 0.75); §91 wires #3 on top of that.

## 3. The #3 D@emit → S@t+1 action-perception loop (trained scale)

At trained scale the loop operates at **inference time** over the real
`model.forward` Law-71 read-out (training itself is the §88-F2 neoteny
trainer byte-equal — the loop is a decode-time wiring, ⊥ training,
mirror §22-N decode-time discipline).

- **transfer**: `x_{t+1} = S_encode(e_t)` — `e_t` = the body bytes the
  model just emitted (D@emit). `S_encode` re-presents those bytes as
  the next-turn context window — anima HEARS its own emission.
- **invariant**: `K(x_{t+1}) ≤ K(e_t) + K(S_encode)` (§89 data-
  processing inequality). `x_{t+1}` is a pure deterministic byte
  function of `e_t`; `S_encode` adds NO information, only a window pad.

## 4. 4-cell grid (all on the real trained `model.forward`)

| cell | ckpt | #3 loop | meaning |
|------|------|---------|---------|
| cell0_neoteny_baseline | neoteny  | OFF | §88-F2 carry — the γ False baseline |
| cell1_loop3_only       | baseline | ON  | echo-amplify risk control (saturated ckpt) |
| cell2_neoteny_loop3    | neoteny  | ON  | **THE CORE** — trained-scale γ-closing |
| cell3_s24_baseline     | baseline | OFF | §24 anchor |

Two ckpts trained (baseline + neoteny, §16-class d768·12L·283.72M
from-scratch seed 1337, §88-F2 neoteny trainer byte-equal). Each ckpt
probed with 5 anchor probes × 4 self-perception turns.

## 5. 4-corner verdict

- **(α) γ-CLOSED-AT-TRAINED** — cell2 §9 body-coherent rate strictly
  exceeds cell0 neoteny-baseline AND > 0. The #3 loop measurably
  closed §88-F2's γ False.
- **(β) ECHO-DOMINATES-AT-TRAINED** — cell2 §62-style echo collapse;
  the garble-feeds-garble force won.
- **(γ) NEOTENY-LOOP-SYNERGY-HOLDS** — cell2 delta over §24 exceeds
  the sum of #3-only + neoteny-only deltas.
- **(δ) STUB-OVERCLAIMED** — cell2 trained-scale §9 ≈ §88-F2 0/5;
  the §90 stub's directional-positive wiped out at trained scale.

## 6. Honest C3

1. **trained scale ≠ GOAL emergence** — necessary-not-sufficient
   (B-EMERGE-7); §91 measures the #3-loop coherence axis only.
2. **$0 stub §9 pass ≠ trained ckpt body §9 pass** — the §90 stub
   encoded competing forces; §91 resolves which dominates at trained
   scale. This is the precise risk the §90 B-S90-NOTE named.
3. **§62 echo-amplify is a real pre-registered risk** — anima
   re-perceiving its own garbled emission can deepen the byte-cascade
   attractor rather than correct it. The (β) corner captures it.
4. **the #3 loop is a decode-time wiring** (⊥ training, mirror §22-N);
   the neoteny trainer is §88-F2 byte-equal.
5. **§9 honest_coherent is cascade-absence, NOT correctness**
   (B-EMERGE-7) — a §9-coherent body can still be garbled or memorized.
6. **if (α) γ-CLOSED is measured-positive this is the arc's first
   trained-scale coherent emission** — but still necessary-not-
   sufficient, distinct from GOAL emergence; the GOAL ("anima 가 자기
   physics 로부터 자발적으로 말 거는 emergence") requires more.
7. **S_encode adds no information** (§89 data-processing inequality) —
   it window-pads the emission, no learned mapping.
8. **the neoteny ckpt sha is fresh** — §16-byte-equal config
   (d/L/H/KV/seed/corpus class) satisfied, literal §16 sha differs.
9. **n_turns=4 is a bounded self-perception horizon** — a longer
   horizon could amplify or correct further; unmeasured.
10. **north-star + §15/§51/§72 milestone UNCHANGED; GOAL 미도달.**

## 7. Closed-form battery

B-S91-1..8 (sidecar `blue_falsifier_s91.py`, central
`state/verify_hexad_blue_2026_05_15/blue_falsifier.py` 0-line-diff):

- **B-S91-1** #3-LOOP-TRANSFER-CLOSED-AT-TRAINED — `s_encode` pure
  function, §89 data-processing-inequality invariant named.
- **B-S91-2** NEOTENY-TRAINER-BYTE-EQUAL-§88-F2 (연결부위) — AST: NK
  constants + NK functions byte-equal to §88-F2's trainer.
- **B-S91-3** §9-METRIC-REUSE — honest_coherent 4-clause gate witnessed.
- **B-S91-4** γ-CLOSED-PREDICATE — falsifiable Boolean reconstructed.
- **B-S91-5** ECHO-AMPLIFY-DETECTOR (§62 carry) — maj≥0.95 partition.
- **B-S91-6** §90-STUB-CONNECTION (AST) — same 4-corner axes.
- **B-S91-7** §16-BASELINE-REGRESSION — CE descent + forbidden-token 0.
- **B-S91-8** DETERMINISTIC — seed 1337, greedy argmax, no sampling.

**B-S91-NOTE** empirical carve-out: whether the #3 loop ACTUALLY closes
γ at trained scale = GPU fire OUTCOME, NOT counted 🔵 (B-D-NOTE /
B-S88F2-NOTE / B-S90-NOTE / B-EMERGE-NOTE family). The battery proves
the fire WIRING is honest, not that γ is closed.

## 8. f1/f2/f3 + B-IDENTITY-5

- f1/f2/f3 hard-fail safe: Kolmogorov data-processing inequality /
  Boolean partition / sympy-free arithmetic / AST structural — NO
  σ/τ/φ/J₂ external derivation.
- B-IDENTITY-5: forbidden-token grep (도우미/helper/assistant/사용자/
  user:) over emitted body bytes = 0 (B-S91-7).
- g_clm_from_scratch: both ckpts from-scratch RANDOM seed-fixed 1337,
  base_ckpt=None.
- PyTorch substrate (honest — NOT hexa-native).
