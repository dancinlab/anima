# H_1823 — circconv (circular-convolution) binding readout on 303M

**id:** H_1823
**slug:** circconv_binding
**tier:** 🧱 NOT-SUPPORTED (engine-native, vast pod)
**date:** 2026-06-30
**wired:** engine-native (anima evaluate, vast pod ssh3.vast.ai:38398). 3-seed (7, 4302, 4303).

---

## Hypothesis

Circular-convolution binding (TPR / vector-symbolic binding as a G1 readout op) lifts engine-native
G1 `composed_distinct≥2` on the 303M trunk. This is the circconv variant of the binding-readout
family (H_1816 = predictive-coding binding, also floored).

## Verdict (verbatim, poller bhe3egeix harvest)

| seed | G1 RECOMBINATION | G6 IDEATION★ | closure |
|------|------------------|--------------|---------|
| circbind_seed4302 | 🔴 best_distinct=0 max_single=0 | 🔴 distinct=3 fals=0 | 🔴 FAIL |
| circbind_seed4303 | 🔴 best_distinct=0 max_single=0 | 🔴 distinct=0 fals=0 | 🔴 FAIL |
| circbind_seed7    | 🔴 best_distinct=0 max_single=0 | 🔴 distinct=3 fals=0 | 🔴 FAIL |

**3/3 seed G1=0, G6 fals=0. NOT-SUPPORTED.** Converges with H_1816 (predcoding binding) → the
**binding-readout family** (circconv, predictive-coding) floors at G1. Re-affirms the campaign
conclusion: the G1 lever is the trunk OBJECTIVE, not a readout/binding op (cf. H_1602 recomb-obj,
H_9024 ByteGPT-obj, all floor; only γ trained-constructive-bind untested, cost-gated).

## Prior art / context

- circconv arm had a BF16-fft silent-death (code fixed, not refired); poller caught the refire and
  harvested this result.
- binding family: H_1816 predcoding 🧱, H_1823 circconv 🧱 (this). readout-op ≠ G1 lever.
- substrate-framebreak-g1-combination-operator: G1 wall = combination operator (additive floor),
  not embedding/scale.
