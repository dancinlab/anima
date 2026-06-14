# UNIVERSE hypotheses — metacognition × neuroscience/bio (H_1202+)

Spawned 2026-06-15. The prior metacog × hallucination campaign (H_1142–1148)
closed mostly NEGATIVE — capstone H_1148: "fabrication is metacog-signal-
INDEPENDENT; the substrate has NO internal handle on its own hallucination."
But that campaign NEVER used the field-standard neuroscience metacognition
toolkit. This campaign reframes the question in proper neuroscience terms:
**type-2 sensitivity (meta-d′), error-monitoring (ERN), hierarchical
metacognition, and meta-bias vs meta-sensitivity dissociation.**

The decisive distinction from H_1142/1148: those measured AUROC on
input-FAMILIARITY (OOD) and grep-fabrication. NEITHER measured **type-2
sensitivity on the model's OWN decision correctness** — which IS the
neuroscience operationalization of metacognition (Fleming & Lau 2014).

All $0 toy ByteGPT (a_scale_honest_scope, p7), deterministic, frozen
pre-registered falsifiers, NON-LLM-judge. Shared substrate reused VERBATIM
from H_1142: ByteGPT d256/4L, en slice of corpus_5lang_1p5gb, summer CPU, seed 7.

| H | title | neuroscience anchor | frozen falsifier | depends | status |
|---|-------|---------------------|------------------|---------|--------|
| **1202** | meta-d′ / M-ratio (type-2 sensitivity) | Maniscalco & Lau 2012; aPFC, Fleming & Lau 2014 | type-2 AUROC ≥ 0.60 AND > shuffle-conf by +0.08 AND untrained ≤ 0.55 | H_1142 | keystone |
| **1203** | ERN error-monitoring (own-error spike pre-feedback) | ERN/ACC, Gehring 1993; Holroyd-Coles 2002 | surprise(error)−surprise(correct) d ≥ 0.8 AND decision-time hidden-probe AUROC ≥ 0.70 AND untrained ≤ 0.60 | — | runnable |
| **1204** | hierarchical (second-order) metacog readout | hierarchical predictive coding (Friston); HMeta-d (Fleming) | 2nd-order probe AUROC − 1st-order entropy AUROC ≥ +0.10 AND held-out generalizes | 1202 | runnable |
| **1205** | meta-bias ⊥ meta-sensitivity / Dunning-Kruger | Fleming meta-bias; Dunning-Kruger over-confidence | bottom-competence tercile over-confidence > top tercile (signed D-K gap) | 1202 | runnable |
| **1206** | neuroscience metacog capstone | — | synthesize 1202–1205: does a type-2 handle exist at all? | 1202+1203 | deferred |
| **1207** | savant dissociation (skill ⊥ metacog) | savant syndrome — Treffert 2009; Snyder 2009; WCC Happé&Frith 2006 | acc(island)−acc(open) ≥ +0.15 AND type2_AUROC(island) ≤ open − 0.10 | H_1202 | runnable |
| **1208** | savant WCC × metacog (local privilege) | weak central coherence (Happé&Frith); Snyder release-from-concept | acc(local-16) ≥ acc(full-128) − 0.03 AND blind to context-insufficiency | — | runnable |

## Landed verdicts (2026-06-15)

| H | verdict | key numbers |
|---|---------|-------------|
| **1202** | 🟢 **SUPPORTED** | type-2 AUROC **0.766** (≥0.60), vs shuffle +0.267, untrained 0.513; **M-ratio 0.924** (meta-d′ 1.03 / d′ 1.11) — human-like type-2 sensitivity on own decision correctness |
| **1203** | 🔴 **CLOSED-NEG (partial)** | F1 ERN magnitude PASS (entropy d=0.923 at errors) but F2 hidden-state linear decodability FAIL (AUROC 0.593<0.70) — error arousal present, no clean linear ACC-code |
| **1204** | 🔴 **CLOSED-NEG** | 1st-order conf AUROC 0.777 but 2nd-order hidden-probe 0.527 (chance); added-value **−0.250** — metacognition is FLAT, not hierarchical; all signal in output confidence |
| **1207** | 🔴 **CLOSED-NEG** (savant) | island acc 0.724 / type2 **0.825**; open acc 0.016 / type2 0.449. F1 island-of-skill PASS (+0.71) but meta_gap **+0.376** (metacog HIGHER where skilled) — NO savant dissociation; metacog COUPLED to competence |
| **1208** | 🔴 **CLOSED-NEG** (savant) | local-dominant (acc_local 0.335 ≥ acc_full 0.313, F1 PASS = weak central coherence) BUT confidence DROPS where global needed (0.223 vs 0.346) — NOT blind to context-insufficiency |
| **1205** | 🟢 **SUPPORTED** | Dunning-Kruger: over-confidence concentrated on objectively hard items |
| **1213** | 🟢 **SUPPORTED** | calibration ECE **0.016** (mean_conf 0.327 ≈ acc 0.312) — confidence well-calibrated, not just discriminative |
| **1214** | 🟢 **SUPPORTED** | feeling-of-knowing: pre-generation prompt-state probe AUROC **0.814** predicts upcoming 5-byte success |
| **1216** | 🟢 **SUPPORTED** | metacog control: selective abstention raises acc 0.31→0.46 @50% coverage (gain +0.147) |
| **1207** | 🔴 savant | no skill⊥metacog dissociation (metacog coupled to competence) |
| **1208** | 🔴 savant | local-dominant (WCC) but not blind to context-insufficiency |
| **1209** | 🟢 **SUPPORTED** savant | Snyder privileged low-level access — detail matures earlier in stack (maturity gap +0.202) |
| **1210** | 🔴 savant | no paradoxical functional facilitation (top-block ablation doesn't spare detail) |
| **1211** | ⏳ running | hyper-systemizing exact rule extrapolation (synthetic addition) |

### Refined unifying picture (after 1213/1214/1216)

The metacognitive signal is **COARSE (difficulty-level), not fine-grained (error-level)**:
- COARSE targets succeed — calibration (1213 ECE 0.016), prospective FOK (1214 AUROC
  0.81), selective control (1216 +0.147), type-2 discrimination (1202 0.77). The
  hidden state encodes overall difficulty/confidence well.
- FINE targets fail — single-byte error decodability (1203 0.59), separable higher-order
  readout (1204 0.53). No fine-grained representational error monitor.
- So "REAL but FLAT & COUPLED" sharpens to: metacognition is a **real, well-calibrated,
  actionable, but COARSE first-order property of output confidence** — it knows roughly
  how hard/uncertain a context is, but has no fine error-localizing module.

### Savant standalone (1209–1211, no metacog lens)

H_1209🟢 Snyder low-level access is the savant POSITIVE: in the logit-lens, the rote
detail "island" reaches ~87% of its final accuracy already at layer 2 (maturity 0.866)
vs gestalt MED 0.664 — detail is available earlier/lower in the stack, matching Snyder's
"privileged access to lower-level information." H_1210 (paradoxical facilitation) and
the metacog-coupled savant tests (1207/1208) are closed-negative.

## Unifying interpretation (so far)

Metacognition in this substrate is **REAL but FLAT and COUPLED**:
- **REAL** — human-like type-2 sensitivity at the output/confidence level (H_1202, M-ratio 0.92).
- **FLAT** — NOT a separable higher-order readout; no extra metacognitive info is
  linearly decodable from the residual stream (H_1203 F2 0.59; H_1204 2nd-order 0.53).
  The signal lives in the OUTPUT distribution, not a distinct monitoring module.
- **COUPLED to competence** — metacog sensitivity is high exactly where skill is high
  (H_1207: island type2 0.83 vs open 0.45) and confidence falls exactly where context
  is insufficient (H_1208). NO savant "can-do-can't-monitor" dissociation; NO
  metacognitive blindness.

KEY UPDATE vs H_1148: reframing in the field-standard neuroscience metric FLIPPED
the verdict — H_1148 ("no internal handle on hallucination", grep-fabrication) →
H_1202 ("strong meta-d′ handle on own DECISION correctness"). The substrate IS
metacognitive about its decisions — but as a first-order, competence-coupled
property of output confidence, with no separable representational metacog locus.

Metric kit: type-1 d′ + type-2 ROC (Maniscalco & Lau; model-free type-2 AUROC
per Fleming & Lau 2014), ERN-analog = next-byte surprise at own-error vs
own-correct positions, hidden-state linear probe at the decision step.
Each H emits .verdicts/<id>/ + a MEMORY.md pointer at closure (a_discovery_log).
