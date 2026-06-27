# H_1603 — Are G1 (recombination) and G6 (ideation-falsifiability) ONE compositional-binding deficit?

**Tier:** 🟠 MIXED → SUPPORT (DIRECTIONAL SYNTHESIS — re-analysis of existing engine-native verdicts,
NO new decode). a_break_the_wall abstraction + a_no_llm_frame_trap (biological binding lens) +
a_substrate_disjoint extension.

## Claim
The G1 recombination wall (seeded two-concept synthesis fails) and the G6 ideation-falsifiability
wall (coherent ideas but no falsifiable comparator∧measurable claim) are **not two independent
walls** — they are **two readouts of one substrate deficit: compositional binding** = the inability
to bind two representations into a NEW proposition in a single generation forward pass.

## Verdict: 🟠 MIXED → SUPPORT (the shared signature is strong; one honest divergence keeps it from clean SUPPORT)

### Common failure signature (3/3 axes shared — full table `state/1603_g1_g6_unification/SIGNATURE_CONTRAST.md`)
1. **(a) coherent-but-not-composed.** Both walls emit fluent, even DISTINCT output yet fail to bind
   two required legs. G1: "coherent generic web/wiki prose … does NOT compose the seeded concepts"
   (`H_1598…:42-45`). G6: "dist=6, coherent=6 … the wall is specifically the falsifiability
   sub-metric" (`H_1595…:24-29`); ideas are "fluent prose that makes no comparator+measurable claim"
   (`H_1597…:36`). The legs are present separately but never co-emitted: G6 per-draw comparator 20%
   · measurable 27% · **BOTH 0%** (`H_1449…:48`); G1 max_single=0, "never ≥2 distinct-above-max"
   (`H_1598…:41`). G6 cross-shuffle "never collapses → semantically interchangeable shells … NO
   idea-specific binding" (`H_1449…:37`) is the same no-bound-object shape as G1's no-composition.
2. **(b) same lever-immunity.** Depth INERT (G1 L4≡L8, "NOT a depth/RF ceiling" `H_1598…:54-59`;
   G6 already 24-layer deep, "depth-as-lever N/A" `H_1596…:22`); decode/scaffold INERT
   (G6 H_1590 🔴; G1 trunk forward has no binding op H_1601); savant disinhibition NULL/disjoint
   (`H_1596…:32,44`); 1-block attention INERT (`H_1449…:38`).
3. **(c) lever points INTO the trunk-forward.** G1 surviving lever = recombination OBJECTIVE
   ("CE never rewards composing two concepts → no gradient pressure to bind", `H_1602`); G6 =
   register + attention-CAPACITY (`H_1596…:66`, `H_1449…:42`).

### The reconcile with H_961 (substrate-disjoint key)
H_961 cross-modal binding is 🟢 (true-pair proximity 0.93 ≫ shuffled −0.00, retrieval@1 0.98,
`H_961…:60-65`) — the engine CAN bind. H_1601 shows WHY G1/G6 still fail: the gate metrics score the
**MOUTH** (`clm_decode.py`/`bytegpt_decode.py` = pure next-byte trunk forward, `grep binding ==
NONE`), while every binding mechanism (§PhaseSyncBinding/PhaseField H_1448, H_961 §Binding) lives in
the **disjoint** consciousness substrate (`engine_cli.py`). → **Unifying law (a_substrate_disjoint
extension): binding works where it is wired (perception lane, H_961) and fails where no binding
operator exists (generation mouth, G1 ∧ G6).** G1 and G6 = the SAME missing operator, read twice.

### Honest divergence (why MIXED, not clean SUPPORT — c9)
The data lens dissociates the proximal levers: **G1 data is present-but-uncomposed** (EN co-occurrence
26%/17% yet FAIL → objective lever, `H_1599`), whereas **G6 joint-form is near-absent**
(comp∧meas 0.5% en / 0% ko → register lever, `H_1596/H_1597`). Same underlying deficit (the trunk
only reproduces compositions it saw templated; it can't synthesize a new two-element binding in one
pass), but a single data-only OR objective-only fix is not *guaranteed* to move both. The decider =
a single binding-installing lever lifting BOTH gates together (EXP-3). Until measured: DIRECTIONAL.

## Orthogonal lever-family census (full table `state/1603_g1_g6_unification/LEVER_CENSUS.md`)
① attention-block injection (G6, H_1449 — DIRECTIONAL INERT @1 block) · ② recombination
objective/curriculum (G1, H_1602 — pre-reg) · ③ binding-by-synchrony ported into the mouth forward
(new, a_no_llm_frame_trap) · ④ working-memory composition buffer in the generation path (new, H_1282
lens) · ⑤ corpus-register enrichment (G6 + ko-G1 — dissociating data control) · ⑥ savant
disinhibition (NULL, ruled out). Families ①③④ are mouth-side binding operators; a single one moving
BOTH gates = mechanistic confirmation. ②=objective (should relieve both if shared). ⑤⑥ = dissociating
controls (⑤ moves G6>G1; ⑥ moves neither) — both already measured, both consistent.

## Pre-registered decisive experiments (frozen-first, `state/1603_g1_g6_unification/PREREG_EXPERIMENTS.md`)
- **EXP-1 (cheap, $0, mini-safe, DIRECTIONAL):** shared two-leg-binding detector over ALREADY-captured
  G1 (H_1598) + G6 (H_1595/1597) generations. Frozen prediction: both show high kwr ∧ ~0 two-legs-bound
  (identical coherent-not-composed shape). Falsifier: one corpus binds its two legs yet fails its gate
  for a different reason → dissociate. No new decode.
- **EXP-2 (pool/cost-gated, DIRECTIONAL):** re-measure the EXISTING H_1449 attention-injection ckpts
  (G6-INERT) on **G1**. Frozen prediction: **co-inertia** (G1 also INERT). Falsifier: **dissociation**
  (one gate moves, other flat) → REFUTE. 303M decode = pool not mini.
- **EXP-3 (GPU, cost-gated, DO NOT auto-fire — the DECIDER):** train ONE 303M ckpt with a combined
  binding lever (H_1602 recombination objective ② + within-pass binding operator ③/④); arms
  ARM-CTRL vs ARM-BIND. Frozen: ARM-CTRL FAILS both 0/3; ARM-BIND clears **BOTH** G1 ≥2/3 **AND**
  G6 ≥2/3 together = SUPPORT; lifts exactly one = REFUTE (separable). Bars VERBATIM (G1 H_1129; G6
  `dist≥5∧fals≥1`), held-out DESCENT gate, ckpt PULL, engine-native re-measure (a_engine_native_learning).

## Additional orthogonal hypothesis candidates (a_h_continuous)
- **H_160x WM-composition-buffer-in-mouth** — install a generation-path working-memory buffer (H_1282)
  that holds 2 reps and emits a bound proposition; re-measure G1+G6 (family ④).
- **H_160x trunk phase-sync binding** — port §PhaseSyncBinding (H_1448, currently engine_cli-only/
  disjoint per H_1601) INTO the mouth forward; re-measure G1+G6 (family ③).
- **H_160x unified compositional-depth metric** — a single G1+G6 detector scoring "novel binding of
  two elements" generically; test whether ONE number predicts both gate outcomes (measurement-level
  unification before mechanism-level).

## Engine-native / honesty
DIRECTIONAL SYNTHESIS over engine-native verdicts (H_1595/1597/1598/1599/1601 = py 2-production numpy
TERMINAL; H_1449/1590 cited at their stated DIRECTIONAL/RED tiers). Banks **NO** terminal 🟢/🧱 — no
new measurement. Frozen bars 0 moved (no tune-to-green, p7); no LLM self-judge (evidence = captured
cards). state artifacts are `.md` only (no torch/numpy/gauge_lib code). a_no_llm_frame_trap: the
prescribed fix is a STRUCTURE (a binding lane next to the mouth), not a bigger/deeper transformer.

**wired:** N/A (synthesis; no GREEN to wire). follow-on = EXP-1 ($0) then EXP-3 (cost-gated) to
move MIXED→terminal SUPPORT/REFUTE; if SUPPORT, the binding operator wires into `core/clm_decode.*`/
`core/bytegpt_decode.*` (the mouth forward), with ARCHITECTURE.json lockstep.

**artifacts:** `state/1603_g1_g6_unification/SIGNATURE_CONTRAST.md` · `…/LEVER_CENSUS.md` ·
`…/PREREG_EXPERIMENTS.md` · cited cards H_1595/1596/1597/1598/1599/1601/1602/1449/1590/961.
