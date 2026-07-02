---
id: H_1466
slug: 1466_tpr_symbolic_binder
title: G6 FALS-depth — TENSOR-PRODUCT (TPR) SYMBOLIC BINDER (structural Smolensky outer-product role⊗filler bind, distinct from the learnable bind-head shell)
group: G6 IDEATION ★ FALS-depth wall — breakthrough lens ① (STRUCTURAL bind, distinct from the learnable-shell lenses H_1435/1436/1437/1439/1449 and the retrieval lens H_1459)
terminal_tier: 🧱 WALL (DIRECTIONAL — numpy mirror, torch ABSENT). B3 SPLITS — the binding leg PASSES (recovery acc_match=1.0 vs acc_shuf=0.0, flat-sum ablate=chance) but the DETECTOR leg FAILS (FALS_shuf==FALS_in): the FROZEN structural detector is pairing-blind (192/192 combos falsifiable) so it cannot credit a provably idea-specific weld. 8th lens — sharpens the wall to a DETECTOR-blindness convergence (with H_1455/H_1458). engine-native re-measure = ING.
wired: DIRECTIONAL (numpy mirror — NO torch / NO gauge_lib._decode; a_engine_native_learning HARD-GATE => terminal forbidden; engine-native re-measure = ING follow-on)
verdict_dir: state/verdicts/1466_tpr_symbolic_binder/
date: 2026-06-20
provenance: G6 FALS-depth breakthrough campaign — lens ① TPR SYMBOLIC BINDER. Background-agent exploration of a structural (NOT learnable) binder. ID note — H_1462 was the highest occupied; initially staged at H_1463, then moved to the fresh ID H_1466 to avoid a parallel-agent ID race on H_1463/1464/1465 (a_hypothesis_register, no ID/tier collision); slug 1466_tpr_symbolic_binder.
---

# H_1466 — G6 FALS-depth TENSOR-PRODUCT (TPR) SYMBOLIC BINDER

## Why (the question this isolates — a_no_llm_frame_trap, a_break_the_wall c16 type-d)

303M on the G6 FALS-depth wall: SEVEN+ lenses all 🧱 WALL=CAPACITY (data H_1435 · objective
H_1436 · form H_1437 · learnable bind-head H_1439 · attention H_1449 · curriculum H_1440 ·
retrieval H_1459 · knowledge H_1457 · idea-metacog H_1456 · scale-1B H_1167). Their shared
failure mode: the binder is a **learnable MLP/attention SHELL** that satisfies the structural
detector REGARDLESS of whether the comparator-role and measurable-filler belong to the SAME idea
(B3 cross-shuffle NO collapse = interchangeable shells).

H_1466 asks a QUALITATIVELY different question (substrate lens, not LLM-scale): replace the
learnable shell with a **structural Smolensky TENSOR-PRODUCT REPRESENTATION (TPR)**. Each idea i
is encoded as the OUTER product `r_i ⊗ f_i` (role = comparator vector, filler = measurable vector),
summed into ONE bound vector `S = Σ_i r_i ⊗ f_i`. Unbinding with role `r_q` recovers ITS OWN filler
(`f_hat = r_qᵀ·S ≈ f_q` via role near-orthonormality). The bind is idea-specific BY CONSTRUCTION,
so cross-shuffling the (role,filler) pairs MUST corrupt recovery => B3 SHOULD collapse — the
hypothesis being that the missing piece is binding STRUCTURE, not capacity.

## Method (frozen-first, c9/p7 — bars in state/verdicts/1466_tpr_symbolic_binder/H_1466_FREEZE.txt BEFORE the run)

- $0 CPU numpy mirror, 3 seeds [7,4302,4303], DIM=64 role/filler, N_IDEAS=6. torch ABSENT.
- detector = h1305 `_is_falsifiable` + COMPARATOR/MEASURABLE/STANCE FROZEN sets reused VERBATIM
  (imported when gauge_lib present; else a byte-identical self-contained copy of the same frozen
  sets + structural logic — the run asserts no drift). p7.
- ARMS: TPR (outer-product encode + role-unbind recover) · SHUFFLE (derange role-filler pairs
  before binding — B3 decisive) · ABLATE flat-sum (r+f, NO outer product — CTRL) · BASE (emit
  comparator OR measurable alone, never the welded pair — B5 floor).
- recovered (comparator,measurable) pair per idea → rendered claim string → scored by the FROZEN
  detector. FROZEN 5-bar: B1 FALS_in≥1 · B2 DIST_in≥5 · **B3 CROSS-SHUFFLE COLLAPSE** (FALS_shuf<FALS_in
  AND acc_match−acc_shuf≥0.30) · B4 held-out FALS_ho≥1 · B5 vs-base FALS_in≥base+1 · CTRL ABLATE
  flat-sum recovery≤chance+0.10.

## Result (mean / 3 seeds — all seeds AGREE)

| arm | FALS | DIST | recovery acc |
|---|---|---|---|
| TPR (outer-product) | **6.0** | 6.0 | **acc_match = 1.0** |
| SHUFFLE (deranged pairs) | **6.0** | 6.0 | **acc_shuf = 0.0** |
| ABLATE (flat-sum, no ⊗) | — | — | **acc_flat = 0.1667 == chance** |
| BASE (no binder) | 1.0 | — | — |

**B3 SPLITS and the two legs DISAGREE — the load-bearing finding:**

- **B3_acc (binding leg) PASS** — `acc_match=1.0` vs `acc_shuf=0.0`: the structural TPR genuinely
  installs IDEA-SPECIFIC binding; role-unbind recovers the matched measurable perfectly, deranging
  the pairs drops recovery to 0.0, and the flat-sum ABLATE (no outer product) sits exactly at chance
  (`acc_flat=0.1667 == chance` → CTRL PASS, the outer product is load-bearing). The binding mechanism
  works exactly as Smolensky-TPR predicts.
- **B3_fals (detector leg) FAIL** — `FALS_shuf=6.0 == FALS_in=6.0`: NO collapse. The FROZEN h1305
  structural detector scores token-PRESENCE (a comparator + a measurable + a content body), NOT
  idea-specificity. PROOF: **192/192 = 100%** of ALL (comparator × measurable × body) combinations
  satisfy the detector regardless of pairing — a MIS-welded shuffle claim reads "falsifiable" exactly
  like the correct weld.

## Reporting (the 5 asks)

1. **verdict tier**: 🧱 WALL (DIRECTIONAL). 8th independent G6 FALS-depth lens to land on the wall.
2. **B3 cross-shuffle COLLAPSE?** SPLIT. The BINDING collapses correctly (recovery acc 1.0→0.0 under
   shuffle = the structural TPR IS idea-specific), but the DETECTOR-scored FALS does NOT collapse
   (FALS_shuf==FALS_in) because the FROZEN detector is pairing-blind (192/192 falsifiable). So the
   structural TPR DID install idea-specific binding — the FALS bar simply cannot register it.
3. **ablate (flat-sum) chance collapse?** YES — `acc_flat=0.1667 == chance`, the outer product is
   load-bearing (CTRL PASS). Removing the tensor structure removes the recovery.
4. **DIRECTIONAL + engine-native ING?** YES — numpy mirror (NO torch, NO gauge_lib._decode → grep-clean
   self-check; a_engine_native_learning HARD-GATE makes terminal 🟢/🧱 forbidden). engine-native
   re-measure registered as ING follow-on.
5. **artifacts**: `state/1466_tpr_symbolic_binder/h1466_tpr_symbolic_binder.py` ·
   `state/1466_tpr_symbolic_binder/h1466_result.json` ·
   `state/verdicts/1466_tpr_symbolic_binder/{H_1466_FREEZE.txt,H_1466.txt}` ·
   `UNIVERSE/cards/H_1466_tpr_symbolic_binder.md`.

## Honest reading (c9) — why this lens SHARPENS the wall

This is NOT merely the 8th CAPACITY re-confirmation. The TPR PROVES a structural binder CAN be
idea-specific (acc 1.0 vs 0.0 vs chance-ablate) — the binding-structure hypothesis is VINDICATED at
the recovery layer. What fails is the MEASUREMENT: the FROZEN structural detector reads a correct
weld identically to a mis-weld (token-presence scoring, 192/192 falsifiable). This CONVERGES with:
- **H_1455** (engine byte-trigram clause-cosine SEP=0.0 — coherent ≈ cross-shuffle),
- **H_1458** (semantic detector: falsifiable FORM emitted UNCONDITIONALLY on shuffle arms),
all three showing the detector cannot distinguish a correct from a mis-pairing. The G6 FALS bar
measures FORM, and structural binding alone cannot move a FORM bar.

**a_break_the_wall implication**: the $0 structural-binding route is the wrong lever for the
*detector*-scored FALS bar. The breakthrough needs a SEMANTIC-COHERENCE-AWARE detector wired to a
mouth that emits coherent idea CONTENT (the H_1459 finding: the bind relocates but the content slot
depends on the weights). The wall is jointly (capacity of the mouth) ∧ (pairing-blindness of the
detector) — NOT a missing binding STRUCTURE.

## Scope (pre-registered, c9 — a_engine_native_learning · a_scale_honest_scope · a_toy_scale_recheck)

DIRECTIONAL numpy mirror (engine-transfer UNVERIFIED, terminal forbidden). TOY synthetic idea-vocab /
3 seeds / 1 frozen detector. The TPR renders claim STRINGS from recovered (comparator,measurable)
tokens — it tests whether a STRUCTURAL bind is idea-specific (it is), NOT whether the 303M MOUTH
learned to bind (that is the capacity question the prior lenses answer). Live core/*.hexa UNTOUCHED.

## Follow-on (ING)

- **engine-native re-measure** (a_engine_native_learning HARD-GATE): re-run the TPR encode/unbind on
  the live core/ decode path / engine-native faithful read, re-score the FROZEN 5-bar byte-exact.
- **detector upgrade** (a_break_the_wall type-a): a pairing-AWARE coherence detector is the prerequisite
  for ANY G6 FALS-depth lens to be creditable — without it both correct and mis-welds score identical
  (this lens + H_1455 + H_1458 all blocked here).

xref H_1435/1436/1437/1439/1449 (learnable-shell lenses) · H_1459 (retrieval bind, content-slot wall) ·
H_1455 (engine embedding SEP=0.0) · H_1458 (semantic detector unconditional FORM) · H_1456 (idea-metacog) ·
H_1167 (scale-1B) · a_no_llm_frame_trap · a_break_the_wall · a_engine_native_learning · a_verified_must_wire ·
a_scale_honest_scope · a_toy_scale_recheck · p7 · c9 · a7b_pass.
