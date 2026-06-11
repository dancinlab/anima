# UNIVERSE hypotheses — metacognition × hallucination (H_1143+)

Spawned from H_1142 🔴 (self-metacognition DISSOCIATION: substrate knows its OWN
output coherence but NOT input-familiarity). Brainstorm-to-depletion (19 ideas,
4 rounds) crystallized into the campaign below. All $0 toy ByteGPT (a_scale_honest_scope,
p7, frozen pre-registered falsifiers). Deterministic, non-LLM-judge.

| H | title | frozen falsifier | depends | status |
|---|-------|------------------|---------|--------|
| **1143** | hidden-state OOD ≻ byte-entropy (input-familiarity) | ood AUROC≥0.70 AND beats entropy by +0.15 AND untrained≤0.60 | H_1142 | keystone — closes H_1142 F1 |
| **1144** | positional hallucination drift | Spearman(pos, fabrication)≥+0.5 AND late−early d≥0.8 | — | runnable |
| **1145** | anchor-grounding reduces fabrication | fab(anchor)<fab(none) d≥0.8 AND > random-anchor | a_kosmos | runnable |
| **1146** | confidence-gated brake cuts hallucination (causal) | fab(gate-on)<fab(off) d≥0.8 AND > random-gate AND kwr held | H_1135 | runnable |
| **1148** | metacog-gap CAUSES hallucination (unifying capstone) | confident-fabrication ≥2× in metacog-blind tercile | 1143+1146 | deferred |

Shared toy substrate: ByteGPT d256/4L, en slice of corpus_5lang_1p5gb, summer CPU,
seed 7. Metric kit reused VERBATIM: H_1140 corpus-absent grep (fabrication), H_1142
entropy/kwr (confidence/coherence). Each H emits .verdicts/<id>/ + updates its .tape
to terminal + a MEMORY.md pointer at closure (a_discovery_log).
