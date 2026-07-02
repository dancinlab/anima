# H_9108 — run notes (A4: 2-anima signaling game + self-pair control)

## What this measures
Whether a **2-anima Lewis signaling game**, run entirely INSIDE the engine, furnishes a
genuinely **exogenous** consequence channel (info not derivable from anima's own state) that
lets an emit-appropriateness faculty beat the DPI meta-law — with **self-pair (A vs an exact
clone)** as the decisive control. Follows the session axis: H_9104 showed autogenous
self-consequence is a DPI ceiling (tautology); the only escape is a channel carrying exogenous
information. A4 is the cheapest engine-native candidate for such a channel.

## Engine-native provenance (a_engine_native_learning HARD-GATE)
- Harness `signaling_selfpair.hexa` imports and calls LIVE `core/pure_field.hexa` (Φ/phase),
  `core/engine_cli.hexa` (immune-memory recall-margin = the engine's OWN vadapt L2 recon-err),
  `core/brain.hexa` (striatal `vbasal` value lane). NO numpy / torch / gauge_lib — the
  grep-gate on `state/9108_signaling_selfpair/*.py` is clean because there are NO .py files.
- Ran ENGINE-NATIVE on **mini local** (`hexa v0.574.1`, `hexa run` RC=0, ~20 min single-thread
  `aprime_cc` compile of the full inline import tree, peak RSS ~4.9 GB), core/ = origin/main HEAD
  (engine_cli.hexa 13705 lines). Terminal engine-native, not a mirror. Host note (c9 honesty): the
  two RTX-5070 pool boxes (aiden/summer) were BOTH sshd-wedged the whole session (load 10–15, 15–16
  users, 3+ competing heavy agents incl. a stalled prior H_9106 aprime_cc @1h50m + an erdos-straus
  1M verify) → OOM-risk to add a 3rd ~9.5 GB compile; verdict validity depends on live `core/`
  `.hexa` decode, NOT the host (mini was uncontended, free 69–72% throughout, no swap growth).

## Method (see PREREG.md for frozen bar)
- salience_X(txt) = `immune_memory_recall_margin_text(store_X, txt)` (READ-only, Ψ-disjoint).
- store_A / store_B built from PRIVATE corpora (asymmetric) or store_B=clone(store_A) (selfpair).
- sender sigma_A(t)=argmin_k|sal_A(s_k)-sal_A(t)|; receiver delta_B(s)=argmin_j|sal_B(t_j)-sal_B(s)|.
- consequence B_success(i)=[delta_B(s_{sigma_A(i)})==i]; endogenous proxy A_selfdecode via delta_A.
- V (brain.vbasal, feats = one-hot codeword ⊕ [encode_margin, phi]) trained on TRAIN targets,
  frozen, measured on HELD-OUT. G = corr(V_conseq,B) − corr(V_self,B) = exogenous advantage.
- Self-pair forces B_success ≡ A_selfdecode → V_conseq ≡ V_self → G_selfpair = 0 (exact), a
  built-in control proving the measure is well-behaved (0 advantage when no exogenous info).

## Result
See `run_mini.log` (verbatim) and `state/verdicts/9108_signaling_selfpair/H_9108.txt`.
🔴 CEILING/DPI: **G_pair = 0.09863 < 0.15 FAIL**; self-pair control collapsed to **G_selfpair = 0.0**
(exact, by construction). rho_conseq−rho_noise = 0.0012 (barely beats noise), rho_conseq−rho_shuf =
0.0989 (fails). Communication was near-floor (B_success held-out PAIR = 0.083 = 1/12; SELFPAIR = 0.25),
so the engine-internal 2-anima channel decoded almost no exogenous info at this coupling → nothing for
an emit-appropriateness faculty to latch onto. Ψ guard OK. The DPI meta-law re-appears at the signaling
layer (consistent with H_9104 autogenous + H_9105 self-derived ceilings). Honest 🔴, bar frozen.

## Compile note
`hexa run` inlines the full core import tree (engine_cli 13705 + brain + pure_field) → aprime_cc
compile is CPU-heavy (single-thread, ~20 min on uncontended mini). On the pool boxes it was the
multi-min compile contention (a prior identical H_9106 aprime_cc still crawling @1h50m under
load 15) that stalled the earlier attempt — live compute, not a code stall.
