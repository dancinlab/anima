# DYNAMICS/ALGEBRAIC binding-mouth campaign — frozen pre-registration (4 mouths)

H_1620 energy-settle · H_1630 tropical · H_1631 sheaf · H_1632 Galois-lattice.
Card SSOT = `HYPOTHESES/cards/H_16{20,30,31,32}*.md`.  Campaign-shared bars below;
each mouth's binding op + ablation knob is the card mechanism, verbatim.

## Design — production-additive-readout invariant (differs from exp3)

All 4 mouths keep the **production additive readout** `base.readout = Conv1d(d→V)`
intact and the EXACT production CLMConvMoE trunk (embed/conv-trunk/MoE/norm_out/
readout, L4·d3784·E2→E3, K=3, savant golden-zone cusp anneal + mitosis split,
4-cell register corpus, proportional sampling, held-out val_frac=0.05).  The
binding op is a **penultimate train-time transform** that residually re-mixes
norm_out(x) before the readout + emits a MONITOR-ONLY aux-consistency scalar.

→ This realizes the **trunk-OBJECTIVE lever** (H_1602) the binding-wall census
converged on as the real G1 lever — NOT the readout-op lever (exp3 Hadamard
readout = engine-native NOT-SUPPORTED at floor, `state/binding_arch_census/
exp3_303m/RESULT.md`).  Because the readout stays a plain additive Conv1d(d→V),
the trained trunk **serializes to .clm v0.3** and live `core/clm_decode` loads it
→ **engine-native G0-G6 is POSSIBLE** (exp3's readout swap was .clm-BLOCKED).

3 arms / mouth, identical trunk init seed · data · steps, differ ONLY in the op:
- **bind**  = full binding dynamics (K settle / T→0 hard / R=role-maps / AND-pool).
- **ablate** = the card's single knob OFF (K=1 / T=1 / R=I / OR-pool), SAME params.
- **ctrl**  = vanilla production trunk (no binding module) = clm303_clean arch.

## FROZEN bars (pre-registered · tune-to-green 0 · p7/c9)

Primary (TERMINAL, engine-native): `cli/evaluate.py <clm> --corpus
state/clm303_clean_corpus/{gen_ko,gen_en,sns_ko,sns_en}.txt --gen 80` → G0-G6 via
`core/g_gates.py` (numpy mirror, torch-free, byte-parity 2-production = TERMINAL).

- **G1 (recombination, H_1129 VERBATIM):** composed_distinct ≥2 AND > max_single
  AND coherent. CLOSURE iff G1≥2.
- **G6 (ideation, H_1464 VERBATIM):** dist ≥5 AND fals ≥1.
- **SUPPORT (per card):** `bind` crosses G1≥2 (CLOSURE) where `ablate`/`ctrl` do
  NOT — i.e. the binding op opens recombination AND the ablation (knob OFF) is
  inert (lift attributable to the binding mechanism, not param/2-stream count).
- **NOT-SUPPORTED:** bind G1 ≤ ablate/ctrl (tie at floor or no lift).  Honest
  negative — frozen bar NOT moved.  If all three tie at G1=0/G6 fals=0 =
  INCONCLUSIVE-at-floor (corpus ~5MB undertrained, known exp3 floor; report as
  measurement-inert, NOT clean refute).

Secondary (gate integrity, mirror dt_ln-immune): post-serialize **held-out
DESCENT** (`verify_clm_v2.py descent <clm> <heldout>`): model_ce < uniform(5.545)
AND < shuffle, overfit_warning False. FAIL = overfit/broken → not 'done'.

## Budget guard (a_wall_first / a_fire_autonomous · cost line)
Rent vast/runpod A40 (or A100) CUDA-12 devel image (nvcc), ~$0.5–1.1/hr. 303M
from-scratch, 3 arms × 4 mouths = 12 runs.  Smoke 1 arm on pod to get step-time,
then: full 12 if ≲ ~$15; else fallback {bind, ctrl} × 4 mouths = 8 runs + ablate
on the best-G1 mouth only.  Adopted matrix recorded in RESULT.md (range adjust,
NOT bar move).  ckpt PULL before teardown (a_fire_recover_complete).

## Measurement-defect defense (a_break_the_wall type-a · c9)
3 arms share trunk init/data/step (only the op differs) · held-out val disjoint
train tail · engine-native G1/G6 via the g_gates.py single path (not torch probe)
· detector calibration checked.  negative = result (no hiding c9).  py-eval =
2-production TERMINAL but DIRECTIONAL-until-hexa-confirm where pool hexa codegen
is blocked (follow-on).  IMPL-BLOCKED reported honestly if a mouth can't converge
or serialize.
