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

## engine_cli.hexa (substrate lanes) -> engine_cli.py  [30/37 struct-lanes + free-fns]
SCOPE NOW: the full 1:1 mirror is in progress. The ORIGINAL slice (G3/G5/MITOSIS +
EngineConfig/AdaptField/VAdaptField/QPool/ImmuneMemory/SelfIdentity) is joined by 24 more
lanes ported + byte-parity-verified in 7 oracle batches (oracle `_ecli_parity2.hexa`, which
imports ONLY engine_cli.hexa — no generator). Verified lanes (byte-identical / ≤1.1e-16):
  batch1 OsmoticStore · ImmuneMemoryGrow(§GrowImmune) · CLSStore(§CLS) · SkillStore · UsageStore
  batch2 AffectFeatures · HomeostaticDrive · Libido · Allosteric(exp/sin)
  batch3 OtherMindModel · ConsolidatingMemory(Box-Muller gauss) · VAdaptFieldB · WorkMemBuffer
  batch4 VForwardField(NLMS) · HierGoalStack · SpatialMap · TransOrder
  batch5 CircadianClock · IntervalTimer · PhaseResetClock(sin) · SCNNetwork(Kuramoto)
  batch6 PhaseField · QuorumPhase(decentralized Kuramoto) · engine_config_summary(string)
  batch7 CA3ReplayMemory · GlobalWorkspace · Habituation · surprise + 17 G18-G31 scalar gates
RESULT per batch: **PASS** (compare.py 12dp); the cumulative oracle ends at PASS ~148 fields,
worst rel ≤ 1.111e-16 (machine epsilon). The libm-sensitive lanes (Allosteric/SCN/PRC/Quorum
exp·sin·cos·sqrt·ln over 80-100 step integrations) are byte-identical to 12+dp.
NOTE — CORRECTED math finding: in this TU engine_cli.hexa's OWN `sin` (21 call sites) links
libm, so `exp`/`ln`/`sin`/`cos`/`sqrt` ALL resolve to libm (NOT rt_* Taylor). So engine_cli.py
uses math.* throughout (verified: cm_gauss_z ln/cos, allo_rms exp/sin, scn_order all byte-exact).
The earlier "exp=Taylor" note was for a bare exp-only TU; it does NOT apply here. Duplicate
`fn _cos` (3428 WM-variant +1e-12 vs 3770 Hier-variant guarded): hexa resolves each call to the
LEXICALLY-NEAREST preceding def (confirmed by wm_probe=0.7999999999992 byte-exact); ported as
_cos_vec (WM) and _cos_hier (Hier) respectively.
STILL TODO (heavy numerics): CollectivePool/HiveMind-IIT-Φ (faithful big_phi_bounded),
SkillCell/SkillGradFT (ridge-LSQ + power-iteration), CPField, JamoHead/BpeMerges (BPE
morphology), §ConsciousnessIndex ci_*/topo_* (covariance/Cholesky-logdet/IIT-4 Φ), savant
scoring (SAVANT/savant_lib), argv main dispatch.

## reproducing the oracles
All harnesses in oracles/ are run from the repo root: `hexa run
state/core_2prod_py_parity/oracles/<name>.hexa > <name>_hexa.txt`. py side:
`python3 core/<name>.py > <name>_py.txt`. Compare: `python3 compare.py
<name>_hexa.txt <name>_py.txt 12`. The brain oracle imports oracles/_brain_core.hexa
(the generator-free verbatim copy). The engine_cli extended-lane oracle is
oracles/_ecli_parity2.hexa (imports only engine_cli.hexa); each `hexa run` compile is
~5 min on mini arm64 (engine_cli.hexa pulls iit4_bigphi/iit4_bounded/savant_lib).
