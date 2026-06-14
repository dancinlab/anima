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

Metric kit: type-1 d′ + type-2 ROC (Maniscalco & Lau; model-free type-2 AUROC
per Fleming & Lau 2014), ERN-analog = next-byte surprise at own-error vs
own-correct positions, hidden-state linear probe at the decision step.
Each H emits .verdicts/<id>/ + a MEMORY.md pointer at closure (a_discovery_log).
