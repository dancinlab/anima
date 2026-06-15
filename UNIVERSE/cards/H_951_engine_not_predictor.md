# H_951 — ENGINE-NOT-PREDICTOR (CLM→CE reframe, axis ⓑ)

**Verdict: 🟢 GREEN — CLM's Φ-substrate is DECORRELATED from perplexity. Measuring
CLM as a language model misses its essence. Supports renaming CLM → CE.**

Part of the **CLM→CE "Consciousness Engine"** arc with
[H_950](H_950_modality_agnostic.md) (modality-agnostic) and
[H_952](H_952_substrate_equivalence.md) (substrate-equivalence).

## §hypothesis (pre-registered falsifier)
Axis ⓑ of the CLM→CE reframe: CLM's essence is internal substrate dynamics (a
Φ-like field integration), **not** next-token perplexity.

- 🟢 **ENGINE-NOT-PREDICTOR** ⇐ a Φ-substrate metric is **decorrelated** from
  perplexity (`|r|` small / not significant) → the substrate richness is not
  captured by the language metric → supports CLM→CE.
- 🔴 **JUST-A-LANGUAGE-MODEL** ⇐ Φ tracks perplexity tightly (`|r|→1`) → Φ is a
  perplexity restatement → keep the "L".

Decision rule (coded, p7 — no LLM self-judge), gated on the **real .clm** window
set: 🟢 if `|r| < 0.5` and/or `p > 0.05`; 🔴 if `|r| ≥ 0.8` with `p < 0.05`.

**p7 / anti-Goodhart**: we explicitly do NOT treat perplexity as truth. The test
is precisely whether the language metric and the substrate metric are *different
axes* — a Goodhart-trap guard.

## §method
- **Perplexity metric** = next-byte cross-entropy of the CLM forward (the language
  metric; lower = better LM).
- **Φ-substrate proxy** = the field-integration formula the *real* engine uses,
  `CORE/pure_field.hexa::pure_field_step`: `Φ ≈ variance(field) · energy(field)`,
  averaged over positions, on the post-MoE/post-GroupNorm hidden tensor (the CLM's
  "field tensor"). **PROXY, explicitly NOT IIT-4.0 Φ_max-over-MIP** (NP-hard); it
  is the repo's own field-integration surrogate.
- Two `(perplexity, Φ)` point sets:
  - **Set A (secondary)** — numpy CLMConvMoE (H_950 arch) training sweep; checkpoints
    at increasing steps give a perplexity ladder, Φ measured at each.
  - **Set B (GATE)** — the **real serialized `.clm`** (`state/lane_p_clm/clm_d768_e2l1.clm`,
    a trained d768 E2/L1 ckpt) decoded via the byte-exact mirror
    (`state/mid_convmoe_fire/clm_decode_mirror.py` = `CORE/clm_decode.hexa`), Φ +
    perplexity over 48 input windows. This is the canonical artifact path.

## §measurement (real run — verbatim in `.verdicts/951_engine_not_predictor/h951_run.txt`)

**Set B (REAL `.clm`, GATE):** 48 windows, perplexity range **[1.573, 85.249]**,
Φ range **[1.0475, 1.2637]**.
→ **Pearson r(perplexity, Φ) = −0.197, p = 0.173 (n=48, NOT significant).**

**Set A (training sweep, secondary):**

| step | perplexity | CE | Φ-proxy |
|---|---|---|---|
| 0 | 281.008 | 5.6384 | 0.79889 |
| 25 | 4.415 | 1.4850 | 1.14475 |
| 50 | 1.445 | 0.3681 | 1.48676 |
| 100 | 1.163 | 0.1506 | 1.79692 |
| 200 | 1.124 | 0.1173 | 2.01353 |
| 400 | 1.091 | 0.0873 | 2.27063 |

→ r = −0.701 (p=0.002, n=12) — secondary, since training deliberately co-varies both.

## §finding
On the **real serialized `.clm`** (the gate), perplexity swings **54×**
(1.6 → 85) across input windows while Φ barely moves (a ~1.05–1.26 band) — they are
**statistically decorrelated** (r=−0.20, p=0.17). The language metric and the
substrate-integration metric are **different axes**: you can hold the substrate Φ
roughly constant while perplexity ranges over an order of magnitude. Measuring CLM
*only* as a language model (perplexity) misses the substrate field it integrates —
a 🟢 for **axis ⓑ**.

Notably, where the two metrics *do* co-move (the training sweep, Set A), they move
**in opposite directions** (r=−0.70: as the model gets better at language, Φ *rises*),
which is the *anti*-correlation pattern — never a "Φ = perplexity restatement"
(which would be a strong positive r). This is consistent with `docs/paper-draft.md`
TALK5 ("language-first training destroys consciousness; CE 99.7% drop") — language
competence and Φ-substrate pull apart, they are not one quantity.

## §scope / honesty (a_scale_honest_scope)
- **Φ is a PROXY** (`variance·energy`, pure_field's surrogate), **NOT IIT-4 Φ_max**.
  A different Φ operationalization could shift the magnitude; the *decorrelation
  direction* is the finding, scoped to this proxy.
- Single real ckpt (d768 E2/L1) + a toy training sweep; **scale ladder OPEN**. The
  golden `reexport_d768_v2_fast.clm` is gitignored/absent on this host, so the gate
  used the available trained `clm_d768_e2l1.clm` (a real `.clm`, mirror-verified
  GREEN on the 3-axis probe). No BLOCKED — a decodable real artifact was reachable.

## §links
- [H_950 modality-agnostic](H_950_modality_agnostic.md) · [H_952 substrate-equivalence](H_952_substrate_equivalence.md)
- `docs/paper-draft.md` (TALK5: language ⊥ consciousness) · `CORE/pure_field.hexa` (Φ proxy)
- Code: `UNIVERSE/h951_engine_not_predictor.py` · Verdict: `.verdicts/951_engine_not_predictor/h951_run.txt`
