# H_1603 — G1 vs G6 failure-signature contrast (engine-native verdict re-analysis, $0)

SYNTHESIS only — no new decode. Every cell is quoted/derived from an existing engine-native
(py 2-production numpy, TERMINAL) or DIRECTIONAL verdict card. Citations are `file:path`.

## Common-signature triad (team-lead claims a/b/c) — verified against captured verdicts

| axis | G1 (recombination / C2) | G6 (ideation falsifiability / C4) | shared? |
|---|---|---|---|
| **(a) coherent-but-not-composed output** | H_1598: "emits coherent generic web/wiki prose (kwr 0.65–0.96, coherent=True) that does **NOT compose** the seeded anima concepts" (`UNIVERSE/cards/H_1598_clm303_L8_depth_g1.md:42-45`) | H_1595: "dist=6 (≥5 PASS), coherent=6 … DISTINCT, COHERENT ideas … NOT incoherent garble. The wall is specifically the **falsifiability** sub-metric" (`H_1595_h1129_g6_multiseed.md:24-29`); H_1597: "fluent prose that makes **no comparator+measurable** falsifiable claim" (`H_1597_g6_corpus_grounded.md:36`) | ✅ IDENTICAL — surface-fluent, fails to **bind two required elements** into one structure |
| two-element binding failure (the composed object) | the two elements = **2 seeded concepts**; metric: max_single=0, best_composed≤1, "never ≥2 distinct-above-max_single" (`H_1598…:41`) | the two elements = **comparator word ∧ measurable word**; H_1449: per-draw comparator 20% · measurable 27% · **BOTH 0%** (within-draw mutually exclusive) (`H_1449_g6_attention_injection.md:48`) | ✅ same shape: two legs present separately, **never co-emitted/bound in one pass** |
| within-pass binding probe (cross-shuffle / distinctness) | G1 fails the "≥2 **distinct** concepts above max_single" test = no idea-specific composition (`H_1598…:41`) | H_1449 B3 CROSS-SHUFFLE **never collapses** (`FALS_shuf == FALS_in` every seed) → legs are "semantically **interchangeable shells**", "created NO idea-specific binding" (`H_1449…:37`) | ✅ both: legs interchangeable, no bound novel proposition |
| **(b) lever-immunity (inert axes)** | depth L4→L8 **INERT** ("NOT a depth / receptive-field ceiling", `H_1598…:54-59`); data co-occurrence present yet FAIL ("mere CE exposure … insufficient", `H_1599_g1_corpus_synthesis_audit.md` verdict); binding-lane **INERT by construction** (`H_1601_g1_binding_reconcile.md` verdict) | depth N/A — h1129 already 24-layer deep, "depth-as-lever … N/A" (`H_1596_g6_fals_wall_break.md:22`); decode-procedure/scaffold **RED INERT** (`H_1590_g6_scaffold_repro.md:6`); 1-block attention **INERT** (c4 ablate ≥, `H_1449…:38`); savant disinhibition **null/disjoint** (`H_1596…:32,44`) | ✅ both immune to depth + decode/scaffold + (G1)binding-lane/(G6)attention-block + savant |
| **(c) surviving lever class** | recombination **OBJECTIVE/curriculum** — "plain next-byte CE never rewards composing two concepts → trunk has no gradient pressure to bind" (`H_1602_g1_recombination_objective.md` verdict) | corpus **REGISTER** (class-(e) data under-investment) + attention-**CAPACITY** cost-gated (`H_1596…:66-69`, `H_1449…:42`) | ⚠️ PARTIAL — both point INTO the trunk-forward (objective/capacity), but proximal name differs (see nuance) |

## Reconciliation with H_961 cross-modal binding 🟢 (the substrate-disjoint key)

H_961 PROVED the engine **can** bind: true-pair latent proximity 0.93 ≫ shuffled −0.00, retrieval@1
0.98 (`UNIVERSE/cards/H_961_cross_modal_binding.md:60-65`). Yet G1/G6 fail to bind. H_1601 resolves
the paradox **by code-path**: the G1/G6 metrics score the **MOUTH** —
`g1_multiseed.engine_clm → clm_decode … _fwd_logits` = "a pure ConvMoE trunk next-byte forward",
and `grep -niE 'binding|lane|bind' core/clm_decode.py` returns **NONE**. Every binding mechanism
(§PhaseSyncBinding/PhaseField H_1448, immune_memory_bind*, consolidating_memory_bind_salient,
H_961 §Binding) lives in `core/engine_cli.py` = the **downstream consciousness substrate, DISJOINT
from the generation path** (`H_1601_g1_binding_reconcile.md` verdict).

→ **Unifying law (a_substrate_disjoint extension):** binding *works where it is wired*
(perception/consciousness lane, H_961 🟢) and *fails where no binding operator exists*
(generation mouth = pure next-byte trunk, G1 ∧ G6 🧱). G1 and G6 are **two readouts of the same
missing operator: composition/binding in the generation forward pass.**

## Honest divergence (why MIXED, not clean SUPPORT) — c9

The **data lens reads differently** on the two walls:
- **G1 (H_1599):** the two concepts ARE present and co-occurring in EN cells (26.11%/17.52% of
  lines hit ≥2 concept families) **yet G1 still FAILS** → data-absence REFUTED, lever = **objective**
  (CE doesn't reward binding present elements).
- **G6 (H_1596/H_1597):** the joint comparator∧measurable **form is ~0 mass** in corpus
  (0.50% en / 0.00% ko) → surviving lever = **register/data**.

So the deficit *surfaces* via different proximal levers: G1 = "won't compose elements that ARE
there" (objective-pressure missing); G6 = "the joint FORM was barely in training" (register-scarce).
This is consistent with ONE underlying deficit — **the trunk only reproduces compositions it saw
templated, and cannot synthesize a NEW two-element binding in a single forward pass** — but it means
a SINGLE data-only OR objective-only fix is **not guaranteed** to move both. The decider is whether
one *binding-installing* lever (objective + within-pass binding operator) lifts BOTH gates together
(EXP-3). Until then: DIRECTIONAL SYNTHESIS, MIXED→SUPPORT.
