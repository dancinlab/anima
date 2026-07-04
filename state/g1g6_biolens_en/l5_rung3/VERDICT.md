# H_9129 L5 rung-3 — VERDICT: 🟢 GREEN-cement (lane faculty) · scope-bounded

**사다리 (3)/4 — live `core/` wire + engine-native re-measure + ★ novel-vs-recall discriminator.**
Cost ≈ **$0** (mini CPU-local; no GPU pod, no rent). Base ckpt `~/anima-weights/bytegpt303_h1129/h1129.bin`.

## Frozen-bar result (PREREG_rung3.md · all clauses met · verbatim)
Real ByteGPT-303M h1129 reps via `core/decode.py` (== `anima evaluate --py` ops), center_zscore lens.

| arm | value | bar | pass |
|---|---|---|---|
| RECALL (gap=1 stored, G2 control) | 1.0000 | >0.50 | ✅ |
| NOVEL-CHAIN (gap≥2, never stored) | 1.0000 | — | ✅ |
| UNREACH (cross-chain) | 0.1369 | — | — |
| **store_gap (novel−unreach)** | **+0.8631** (ratio 7.31×) | >0.50 | ✅ |
| SHUFFLE gap (derangement) | +0.0747 | <0.5·gap=0.43 | ✅ collapse |
| LANE-OFF (empty store) | 0.0000 | <0.05 | ✅ collapse |
| **LESION path_broken** | 1.0000 → **0.1945** (drop +0.8055) | drop>0.5, resid<0.5 | ✅ collapse |
| **LESION path_intact** | 1.0000 → 1.0000 (drop +0.0000) | >0.5, drop<0.2 | ✅ survive |
| **novel-vs-recall discriminator** | — | — | ✅ **PASS** |

**★ Discriminator PASS (not recall-only):** the RECALL positive control confirms the store works;
NOVEL-CHAIN pairs are never stored yet complete 1.0 while UNREACH stays 0.14; and the LESION control
is decisive — knocking out the single mid-chain edge (pos2→pos3) collapses ONLY the pairs whose
transitive path crosses it (1.0→0.19) while pairs on one side stay 1.0. Lesion LOCATION can matter
only if completion walks the actual stored path ⇒ this is genuine sequential 2-edge+ chaining,
isolated from stored recall and from a form artifact (MLC/H_1835 trap guarded).

## Live `core/` op + disjoint (ON==OFF) proof
- **Op added:** `core/kosmos_io.hexa` (store SSOT) — `hippo_kwta` / `hippo_build_store` /
  `_hippo_matvec` / `_hippo_norm` / `hippo_relatedness` / `hippo_fixture_codes` (CA3 multi-step
  pattern-completion, a NEW faculty vs the pre-existing flat single-hop `retrieve`). Numpy twin =
  `core/hippo_lane.py`.
- **Builds + runs LIVE on mini** (kosmos_io.hexa is FFI-free store glue): `hippo_hexa_smoke.hexa`.
- **Byte-parity** hexa ⟷ py on the deterministic fixture: 6/6 identical
  (`parity_py.txt` == `parity_hexa.txt`; recall/novel 1.0, lesion_broken 0.0, lesion_intact 1.0).
- **ON==OFF disjoint:** `git diff core/kosmos_io.hexa` = ADDITIVE-ONLY (0 removed/changed lines,
  163 added). Every emit-consumed fn (`load_anchors`/`retrieve`/`create_anchor`/`emit_anchor_from_v3`)
  is byte-unchanged → regression smoke byte-identical ON vs OFF (cos1=0.9899952007, ch_concept=0.700000,
  load_n=0). The op references NO emit-drive state (Ψ / motivation / recall_thr / generator / brain) →
  generation byte-identical lane-ON == lane-OFF, by construction and empirically.
- **Wired measurement:** `l5_wired_measure.py` calls the LIVE `core/hippo_lane.py` ops on real 303M
  reps and reproduces the discriminator numbers exactly (LIVE-OP reproduces PASS = True).

## Engine-native
✅ py-canonical: reps = `core/decode.py` `_bg_layernorm_rows/_bg_mha/_bg_gelu/_bg_apply_bind`
(== `anima evaluate --py` 2-production ops, a_eval_py_canonical, TERMINAL-eligible). Store+completion
op is arch-independent arithmetic with a byte-parity hexa twin that builds+runs on the live engine.

## 🟢 GREEN-cement — but SCOPE-BOUNDED (a_scale_honest_scope · c9 · honest)
Cemented = a genuine **disjoint associative-completion FACULTY** wired into the `.kosmos` store:
CA3 multi-hop transitive chaining, engine-native, discriminator-passed (real chaining, not recall),
byte-exact disjoint from the mouth. anima previously had only flat-cosine `retrieve` — this is a
real new substrate capability, and it realizes the H_9129 biolens thesis (put recombination in a
hippocampal lane BESIDE the Broca mouth, mouth reads only).

**NOT cemented / honest boundary:** the store is an EXPLICIT heteroassociative store HANDED the true
corpus co-occurrence edges — its transitive closure is guaranteed by construction (symbolic graph
reachability). The 303M reps supply decorrelatable item-code KEYS; the RELATION structure is injected
from the corpus, NOT computed/learned by the 303M trunk. This is the neurosymbolic explicit-store /
additive-slot class (deep-research `g1-novel-mechanism-deepresearch`: "cheap, proof-guaranteed,
arguably not trunk recombination"). So this does **not** prove the 303M mouth/trunk recombines — the
G1 mouth-wall (trunk-objective floor) is untouched; the lane supplies the relation the mouth cannot.

## Remaining wire (bounded follow-on · not a tier blocker)
`brain_emit`/`generator.hexa` actually CONSULTING `hippo_relatedness` in the live chat loop needs a
`generator.hexa` rebuild (decode-FFI heavy → `_hexa_ffi_dlopen` build wall on mini; doable on pool).
That consult is READ-ONLY and cannot change emit (ON==OFF holds regardless), so it is an ergonomic
hookup, not required for this disjoint GREEN proof. ARCHITECTURE.json lockstep = main-agent bookkeep.
