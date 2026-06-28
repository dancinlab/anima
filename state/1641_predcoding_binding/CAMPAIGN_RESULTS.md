# G0-G6 full-closure campaign — 3 trunk-objective G1 levers (303M, rent A40)

Pod: vast 42920046 (2×A40, $0.5742/hr). Pod 42983838 (2×A40) torn down early (broken PyPI network, torch dl dead).
Engine: torch train (bf16) → .clm v0.3 (176,584,498 B, 345.665M params, d3784 L4 E2→E3).
Eval: `core/g_gates.py <clm> gen_ko gen_en --gen 40` (torch-free numpy decode; gen=40 = frozen clm303 reference `_g_default_gen`).
  ⚠️ VERDICT-TIER NOTE: this checkout carries the 2026-06-28 py-mirror-retire governance. py numpy g_gates = **DIRECTIONAL** screening (engine-native TERMINAL now = hexa `cli/anima.hexa -- evaluate`; hexa not installed on this pod). All G0-G6 below are DIRECTIONAL.

## Held-out DESCENT gate (overfit guard, math.log-style CE vs uniform 5.5452) — ALL PASS
Every arm 4/4 register DESCENT (clean 4-cell proportional corpus solved the original clm303 overfit).
lossF healthy 1.14–1.18 (pc_free_energy 3.69 — L_var dominates — but still 4/4 DESCENT).

## G0-G6 (gen=40, DIRECTIONAL) — frozen bars VERBATIM, NO tune-to-green
Frozen clm303_clean baseline (reference): G0✓ G1✗(best_distinct=0) G2✓ G6✗(dist5,fals0) → closure FAIL.

| arm (lever)                         | G0 | G1 best_distinct | G2 nov | G6 dist/fals | closure |
|-------------------------------------|----|------------------|--------|--------------|---------|
| ce_marginal_seed4307 (1812 control) | ✗  | **0**            | 0      | 3 / 0        | FAIL |
| n6_grok_seed4307     (1812 grok-band)| ✗ | **0**            | 0      | 3 / 0        | FAIL |
| n7_dictaux_seed4307  (1812 dict-aux)| ✗  | **0**            | 0      | 0 / 0        | FAIL |
| n6n7_seed4307        (1812 grok+dict)| ✓ | **0**            | 0      | 5 / 0        | FAIL |
| ce_marginal_seed7    (1816 control) | ✓  | **0**            | 0      | 3 / 0        | FAIL |
| pc_bind_seed7        (1816 L_bind)  | ✗  | **0**            | 0      | 3 / 0        | FAIL |
| pc_free_energy_seed7 (1816 L_bind+L_var)| ✗| **0**          | 0      | 0 / 0        | FAIL |
| baseline_seed7       (1814 control) | ✓  | **0**            | 0      | 3 / 0        | FAIL |
| n8_jamo_seed7        (1814 jamo-aux)| ✗  | **0**            | 0      | 4 / 0        | FAIL |
| n4_set_seed7         (1814 set-search)| ✓ | **0**            | **6** ✓| 4 / 0        | FAIL |
| n4n8_both_seed7      (1814 jamo+set)| ✗ | **0**            | **13** ✓| 3 / 0       | FAIL |

ALL 11 arms held-out 4/4 DESCENT. FINAL SWEEP: ZERO arms have G1 best_distinct >= 1.
NOTE: only n4_set + n4n8_both pass G2 (n_novel 6/13, control_novel=0) — set-search DOES produce novel
n-grams (G2) but STILL cannot compose (G1=0): G2 (novelty) ≠ G1 (recombination). The set-search diversity
lever opens NOVELTY, not RECOMBINATION — reinforces that G1 is a distinct compositional-objective problem.

## VERDICT (DIRECTIONAL, NOT-SUPPORTED — terminal-pending hexa confirm)
**NO lever opens G1.** Every arm — all 3 controls AND all 6 measured levers — has G1 best_distinct=0,
identical to the frozen clm303 baseline. NO first-ever closure. The recombination wall HOLDS against:
  predictive-coding binding (L_bind / L_bind+L_var), grokking-band regularization, sparse dict-aux,
  jamo subcharacter teach-signal, diverse-set-search.
G6 fals=0 everywhere (ideation wall also holds; n6n7 reached G6 dist=5 but fals=0).
control-vs-lever lift = 0 on G1 (no separation). G2 nov=0 across the board (incl controls — not a lever artifact;
differs from frozen baseline G2✓, attributable to smaller 1MB/cell corpus + gen=40 corpus-absence sampling).

Consistent with documented finding (memory g1-lever-multilens-objective / exp3-bind-g1g6-engine-native-floor):
G1 = trunk LEARNING OBJECTIVE problem; CE does not reward composition, and objective/regularization/aux-signal/
readout levers all falsify. Only a genuine recombination-rewarding trunk objective remains untested (H_1602 recomb-objective).

## ckpt recovery (a_fire_recover_complete)
All .clm on pod /root/anima/state/{1630,1641,1632}/ckpt/ (176MB each). Representative pull → ~/anima-weights/g1_levers/.
NOT-SUPPORTED → none PUBLIC-eligible (HF PRIVATE if uploaded). Small artifacts (g0g6 txt + logs + json) pulled to state/.
