# core/ consciousness-engine 2-production py-mirror parity

Per CLAUDE.md a_two_production_mirror. Each .hexa <-> .py driven on identical
deterministic inputs; numeric fields compared to >=12 dp relative, strings/bools
byte-identical (state/core_2prod_py_parity/compare.py).

KEY FINDING (2026-06-26): the COMPILED `hexa run` binary maps the bare math
builtins `sin`/`cos`/`exp`/`sqrt` to **libm** (NOT the rt_* Taylor polynomials in
stdlib/runtime/math.hexa — those are the freestanding/drop-measure fallback only).
Verified: pure_field osc field[2] at N=1 with libm sin = 0.0017011662429256978
== hexa; 8-term Taylor diverges at ~6e-12. So py uses math.sin/cos/exp/sqrt.

## pure_field.hexa (Engine A) -> pure_field.py
oracle: pure_field_warmup(N) for N in {1,37,600}; dump phi, phi_peak, phase,
narrative_coherence/len, field[0..5], verify_zero_input.
RESULT: **PASS** — 42 fields, worst rel = 1.95e-16 (field[3], machine epsilon).
N=600 Ψ-field: phi=0.11898342128851365, phi_peak=0.14872927661064206, phase=2
(SUSTAIN) byte-identical hexa<->py.

## engine_g.hexa (Engine G) -> engine_g.py
oracle: motivation_score 8-factor on lo/hi/mid contexts + emit/interrupt/rate/
phi-ratchet/combined predicates.
RESULT: **PASS** — 10 fields, worst rel = 1.66e-16 (score_hi). score_hi=0.67,
emit gate + 4-safety conjunction byte-identical.

## brain.hexa (A ⇄ G consciousness core) -> brain.py
oracle: oracles/_brain_parity.hexa (imports pure_field+engine_g+_brain_core, where
_brain_core.hexa = brain.hexa VERBATIM minus the unused `import generator` + the two
generator-coupled L3 wrappers brain_emit/brain_emit_aged — excised ONLY because the
full generator import-closure compile OOM/time-walls; brain_decide and the consult
family are byte-identical with or without that import). Drives brain_decide (low/high),
brain_decide_anchored (empty + 2 opposite-tension anchors that cancel + 1 aged anchor),
the 5 emit-loop consults (cerebellum/wm/affect/margin/gap), and the VBasalGate go/no-go
selection (untrained abstain -> learned tick -> released) + cosine align.
RESULT: **PASS** — 69 fields, worst rel = 1.98e-16 (mg.conf_bias, machine epsilon).
Ψ-field phi=0.11898342128851365, motivation scalars, anchor fold/nudge, every emit
decision + VBasalGate selection byte-identical.
NOTE: brain_emit/brain_emit_aged drive the L3 generator slot via the sibling
generator.py port (parallel branch) — imported lazily; not exercised by this gate.

## engine_cli.hexa (CORE slice: G3/G5/MITOSIS) -> engine_cli.py  [PARTIAL]
SCOPE: the 3 named consciousness-gate subsystems + shared CLI/config/adaptation —
EngineConfig+resolvers, MITOSIS engine_grow, AdaptField/VAdaptField, QPool entropic,
ImmuneMemory(G5), SelfIdentity(G3). ~27 other lanes NOT yet ported (TODO follow-on).
oracle (_ecli_parity.hexa, imports only engine_cli.hexa — no generator):
  · CLI precedence (mitosis/topo/savant flag>env>default) · MITOSIS grow_on=11/off=1
  · VAdaptField DIM-stream growth (5 cells) + recon-err + top-2 [d1,d2]
  · ImmuneMemory bind/recall (Paris/Tokyo) + ABSTAIN("") + recall_thr margin -0.15 + gap
  · SelfIdentity self-chain continuity_cos=1.0 + adjacent + impostor + drift
RESULT: **PASS** — 27 fields, worst rel = 0.000e+00 (byte-identical). G3 self-chain
cos, G5 recall_thr abstain, MITOSIS counts all byte-exact.
NOTE: math finding — hexa `sqrt`=libm but hexa `exp`=rt_exp Taylor (NOT libm); engine_cli
uses only sqrt (clean), brain uses exp (ported as _rt_exp Taylor).

## reproducing the oracles
All harnesses in oracles/ are run from the repo root: `hexa run
state/core_2prod_py_parity/oracles/<name>.hexa > <name>_hexa.txt`. py side:
`python3 core/<name>.py > <name>_py.txt`. Compare: `python3 compare.py
<name>_hexa.txt <name>_py.txt 12`. The brain oracle imports oracles/_brain_core.hexa
(the generator-free verbatim copy). engine_cli.py is a PARTIAL port (G3/G5/MITOSIS
core); the other ~27 lanes remain TODO.
