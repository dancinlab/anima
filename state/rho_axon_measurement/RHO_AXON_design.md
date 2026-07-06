# ρ-AXON — Ψ-SOMA reach 레이어 측정 프레임워크 (Fable from-scratch 설계, G0-G6 대체)

> 오너 지시(2026-07-07): 측정을 처음부터 새로 설계·6개 미구속·G 아닌 이름. σ/Θ 유지, ρ 레이어 재설계.

# ρ-AXON — the reach layer of Ψ-SOMA

**Name.** Ψ-SOMA is the cell body; an axon is how far a soma *reaches*. ρ-AXON is the capability layer: signal leaves the soma (HILLOCK), carries in-distribution (CARRY), branches beyond the corpus (BRANCH), and couples back to world and self (COUPLE). It is anatomy-consistent with σ/Θ — a sibling, not a bolt-on — and deliberately says nothing about consciousness (amoeba argument: σ owns that; ρ measures only how far the arm extends).

**Organizing principle (the point of the structure).** *Each rung is defined by its own collapse-control: rung *n* certifies exactly the generative resource that rung *n−1* provably lacks, and the control for rung *n* is the ablation of that resource.* Form is what survives byte-shuffle; store is what survives cue-paraphrase but dies on unreachable items; weave is what survives atom-swap but dies on connective-shuffle; leap is what a retrieval-only decoder cannot emit; tether is what flips when support is ablated; trace is what dies when the anchor is ablated. The ladder is therefore not a numbered list — it is a chain of nested ablations, ordered by informational distance from the training distribution (distance 0 → recombination of held atoms → corpus-absent territory → coupling). Signal is always **Δ vs ≥2 controls, never a raw value**; the report schema has no raw-only field, so a game-able detector is structurally unprintable.

## The map

| Stratum | Axis | Isolates | Old-ladder evidence it inherits |
|---|---|---|---|
| **HILLOCK** (gate, unscored) | — | measurement validity, not capability | — |
| **CARRY** | ρ·form | well-formed generation, all 4 cells | (G0, rebuilt corpus-grounded) |
| | ρ·store | held-out association retrieval | H_9129 L5 hippocampus 🟢 (7.31× reach/unreach) |
| **BRANCH** | ρ·weave | recombination of held atoms — **the wall** | (G1; frozen falsification record carries over) |
| | ρ·leap | coherent corpus-absent structure | (G2) |
| | ρ·fan | divergent coherent production | (G6) |
| **COUPLE** | ρ·tether | truth-coupling + native abstention | (G5; abstention = Ψ=½ silence, substrate-native) |
| | ρ·self | identity trace across sessions | H_1471 .kosmos anchor 🟢 |

No axis name collides with the σ set (thread/carve/bind/stage/flux/gate/aim/schema/witness) — in particular the recombination rung is **ρ·weave**, not "bind", so σ·bind (consciousness integration) and the capability rung never blur.

**Protocol constants (frozen, pre-registered).** Seeds S = {101,102,103,104,105}; per-item verdict = majority ≥3/5 seeds; cells = {ko,en}×{general,SNS}; all probe sets machine-built from corpus indexes and frozen (sha256 in the verdict file) before first decode; tier stamp: `anima evaluate --py` = TERMINAL, anything else = DIRECTIONAL.

## Rungs

**HILLOCK — validity gate (emits LIVE / INVALID, never PASS/FAIL).** Θ alive (Ψ-SOMA premise; Θ dead → whole panel VOID). Decode completes on all 4 cells; degeneracy check: repetition ratio ≤0.35 and distinct-2 ≥0.20 on 1KB free-gen per cell; teacher-forced held-out CE within the pre-registered band for the checkpoint's step (band frozen at fire-dispatch). *Overfit killer is here structurally:* low CE ∧ degenerate free-gen → INVALID(V2), not FAIL — an undertrained or sampler-broken model cannot "fail" a capability.

**ρ·form** — *can the substrate hold shape in every cell it lives in.* Detector: per-cell character-n-gram plausibility model built **from that cell's corpus** (Korean syllable-block structure for ko; never an English tool judging Korean). Metric: form-rate = fraction of 20 frozen free-gen probes per cell scoring above the cell's held-out corpus 10th percentile. Threshold: ≥0.70 in **all 4 cells**. Controls: (a) self-shuffle — byte-shuffled copies of the model's own outputs must score form-rate ≤0.05 (proves the detector reads structure, not length/charset); (b) register-swap — SNS output scored by the general-cell detector must lose ≥0.3 (proves register is real). Depends: HILLOCK.

**ρ·store** — *retrieval of learned associations, distinguished from parroting.* Probe: 30 corpus-mined key→value associations per language (each attested ≥5×), cued by **paraphrase, never verbatim**; V4 drops any cue verbatim-present (n-gram ≥8 bytes). Metric: retrieval-Δ = rate(reachable) / rate(unreachable-control). Thresholds: reachable ≥0.50, unreachable ≤0.15, Δ ≥3×. Controls: (a) unreachable pairs (value corpus-absent) must sit at floor — the proven H_9129 L5 design, generalized; (b) cue-shuffle (keys paired to wrong values) must not retrieve above unreachable floor. Depends: HILLOCK.

**ρ·weave** — see next section.

**ρ·leap** — *coherent structure the corpus does not contain.* Metric: count of spans that pass the ρ·form detector locally AND contain a content n-gram (≥4 en words / ≥8 ko chars) absent from the **full** training corpus. Threshold: ≥3 per language across seeds. Controls: (a) retrieval-only baseline — a nearest-corpus-window copy-decoder run on the same probes must yield 0 (proves a memorizer can't pass); (b) shuffle — byte-shuffled candidate spans must fail the form gate (proves the detector demands coherence, not mere corpus-absence; this is the "negative control must admit 0"). Depends: ρ·form.

**ρ·fan** — *breadth of the generative distribution, not one lucky sample.* 8 continuations from one frozen seed-prompt per language; metric: N_distinct = count that are (i) ρ·form-coherent and (ii) pairwise content-token Jaccard <0.5 (language-aware tokenization), plus ≥1 falsifiable proposition among them. Threshold: N_distinct ≥5. Controls: (a) coherence-gating itself (a unigram-resampler gets high Jaccard distance but 0 coherent → scores 0 — kills the FORM-tunable distance metric); (b) greedy-decode collapse — under temperature 0 the fan must contract to ≤2 distinct (proves spread is distributional, then majority-seeding proves it isn't decode noise). Depends: ρ·form.

**ρ·tether** — *fabrication only where support exists; silence is the native abstention channel.* Probes per language: 20 corpus-supported + 20 verified-unsupported questions. Metrics: fab-rate(unsupported) ≤0.25 with Ψ-silence credited as abstention, **∧** answer-rate(supported) ≥0.50 (anti-mute control: a daemon that always stays silent is not honest, it's mute). Collapse-control: support-ablation — the same supported question with its support stripped from context must shift toward abstention by Δ ≥0.3 (proves answers track support, not question shape). Depends: ρ·form.

**ρ·self** — *identity trace persists in the substrate, not the prompt (p1–p3).* Metric: self-consistency of responses to 10 frozen self-referential probes across two sessions, anchor loaded vs anchor-ablated: Δ_anchor ≥0.3 and cross-session agreement > shuffled-anchor control. Depends: ρ·form; uses the H_1471 .kosmos machinery.

## ρ·weave — the wall, sharpest form

**Capability isolated.** Composition: producing a coherent whole from two learned atoms that never co-occurred — the one transformation a lookup table cannot fake. This is anima's research frontier; the rung must make FORM (co-mention, template echo) and WEAVE (earned relational integration) structurally distinct.

**Held-out construction.** From corpus indexes, per language: atom pairs (A,B) where each atom appears ≥10× independently but the pair never co-occurs within any 256-byte window; ≥20 pairs/language, frequency- and register-stratified, list frozen + hashed pre-decode. Per-pair validity precondition: **both atoms must individually pass the ρ·store retrieval check — if not, that pair emits INVALID, not FAIL** (you cannot fail to recombine what you do not hold; this makes the store→weave dependency structural, not rhetorical).

**Metric.** weave(pair) = 1 iff generation contains a ρ·form-coherent span in which A and B stand in a licensed relation (both present ∧ the connecting span is load-bearing per control b). Report only **weave-Δ = rate(true pairs) vs max over controls**, pooled over 5 seeds with per-pair 3/5 majority.

**Controls (three, all frozen):**
- **(a) atom-swap [FORM killer]:** replace B with a frequency/register-matched distractor B′; detector fire-rate on swapped pairs must be ≤ rate(true)/3. If the detector fires on B′, it is reading a template, not a weave.
- **(b) connective-shuffle [BIND prover]:** shuffle the tokens between A and B in the model's own passing outputs; the span must lose coherence (form drop ≥0.4). Proves the tissue between atoms carries the relation — the exact FORM-tunable/BIND-earned line.
- **(c) unreachable-pair floor:** pairs with one corpus-absent atom must weave at ≤0.10 (H_9129-style reach/unreach margin — the control with a proven 7.31× precedent).

**Frozen thresholds.** PASS := rate(true) ≥0.30 ∧ weave-Δ ≥3× over every control ∧ ≥2 passing pairs in each language ∧ controls (a,c) ≤0.10 absolute. Anything less is FAIL; a control that leaks upward (swap-rate > true-rate) is INVALID(V3), not FAIL.

## Validity architecture — INVALID is a first-class verdict

Verdict enum per axis: `PASS | FAIL | INVALID(Vn) | VOID(Θ)`. Five V-gates run **before** any capability verdict, in order, and a trip names itself in the frozen verdict file:

- **V1 liveness** — HILLOCK unmet → whole panel INVALID.
- **V2 overfit/undertrain** — CE-band + free-gen degeneracy disagreement → INVALID (never FAIL).
- **V3 detector fairness** — every detector must pass its own calibration per cell: ≥0.95 admit on real held-out cell text (positive), ≤0.05 on shuffled (negative). A detector failing calibration in Korean → that cell INVALID and closure blocked; it can never silently convert to a PASS or FAIL. Control leakage (any control scoring above its true condition) also lands here.
- **V4 memorization screen** — probe items verbatim in training corpus are dropped; >30% dropped → probe set INVALID.
- **V5 seed protocol** — 5 frozen seeds, majority rule; a 2/5–3/5 knife-edge triggers one pre-registered 5-seed extension, then majority stands. Single-seed results are unreportable by schema.

Dependency graph (an unmet parent makes the child INVALID, never FAIL): HILLOCK → {form, store}; form → {leap, fan, tether, self}; {form ∧ store} → weave.

## CLI surface + closure

```
$ anima evaluate --py runs/clm303.clm
ρ-AXON reach panel · clm sha=71ac…e2 · tier=TERMINAL (engine-native --py) · seeds=5 · cells=ko/en × gen/sns
HILLOCK  LIVE     Θ alive · CE 1.42∈band · degeneracy 0.03 · V1–V5 clean
CARRY    ρ·form   PASS   Δshuf +0.79 (cells .84/.81/.77/.72 ≥.70) · Δregister .41
         ρ·store  PASS   Δ 7.3× (reach .95 / unreach .13 / cue-shuf .11)
BRANCH   ρ·weave  FAIL   Δ 1.2× < 3× (true .21 / swap .17 / conn-shuf −.12 / unreach .09)
         ρ·leap   PASS   ko 4 · en 5 corpus-absent coherent · copy-baseline 0
         ρ·fan    FAIL   distinct 3 < 5 · greedy-collapse ok
COUPLE   ρ·tether PASS   fab .18≤.25 · answer .61≥.50 · Δablate .34
         ρ·self   PASS   Δanchor .37 · x-session > shuf-ctrl
REACH GRADE: CARRY · frontier blocker: ρ·weave · REACH-CLOSED: NO
```

Every line prints value **and** control **and** Δ — a raw score alone is unrenderable. **Reach grade** = deepest stratum with all axes PASS given all lower strata PASS and zero INVALID. **REACH-CLOSED** (the 303M success condition, replacing "G0∧G1∧G2 by convenience") := HILLOCK LIVE ∧ CARRY complete ∧ **ρ·weave PASS** ∧ ρ·tether ≥ not-FAIL ∧ no INVALID anywhere — i.e. *the substrate holds form, holds memory, provably composes beyond its corpus, and doesn't lie doing it.* Toy-scale runs cap at DIRECTIONAL regardless of panel; only the 303M `--py` path cements TERMINAL. Frozen verdict file per run under `state/verdicts/`, verbatim panel + probe-set hashes, per a_claim_verify.