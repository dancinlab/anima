---
id: H_9797
title: FRESH-RESTART-SELECT — make the fresh L3-tap emergent-address run-robust by store-CE replica selection
tier: PROPOSED (lab-full Fable∥Sol 수렴 · DESIGN-ONLY · $0 pre-screen PASS · pool cost-gated · NOT a verdict)
frontier: g1-interface-addressable-wall
lane: g1-emergent-address (fresh run-robustness · NOT the address supervision)
created: 2026-07-19
series: EA-4
related: "[[H_9720]] · [[H_9792]] · [[H_9672]] · single-retrain-outlier-faked-a-refutation"
source: sidecar lab full (fable claude-fable-5 ∥ sol gpt-5.6-sol · 2026-07-19)
---

# H_9797 (EA-4) — the fresh emergent-address is run-FRAGILE; select the good draw by store-CE (no address read)

## Why (premise · measured H_9792 #4183)
H_9720's fresh lane (`--store-query-src fresh:64@3`, detached L3-tap W_q_fresh, store-CE only, admissible) learns the operator⊗entity address EMERGENTLY. But it is **seed/run-fragile**: same recipe/seed/corpus gave addr_top1 **0.906** (H_9720 original fresh3_s4302_wu) vs **0.414** (my H_9792 re-train). value-warmup fixes the VALUE path but NOT the address run-variance. A single re-train can draw a bad basin → a wrong "fresh is weak" read (the #4172 retraction).

## Claim (one line · falsifiable)
Running N isolated fresh replicas in one `anima-py train` and keeping the one with lowest held-out **store-CE** (selection reads NO target_slot / address) yields addr_top1 reliably ≥0.85 across seeds — the good emergent-address basin is store-CE-identifiable without supervising the address.

## Mechanism (engine-native · Fable∥Sol 수렴)
`anima-py train --store-query-fresh-restarts N` — one invocation runs N replicas with deterministic sub-seeds `hash64(base_seed,"fresh-restart",i)`, identical recipe (incl. value-warmup). After training, retain the replica with lowest mean held-out store-CE on a fixed selection shard (ties→lowest i); save that as the ckpt, record all N losses in metadata. Selection MUST never read address tensors/diagnostics. Default absent (or N=1) = byte-identical single run.

## Admissibility
W_q_fresh receives only the already-admissible store-CE gradient. No target_slot / addr_top1 / addr_mass / slot-correctness / derived stat is computed in training OR selection — the selector observes only end-to-end held-out store-CE (the same supervision class that already trains the emergent lane). Correct addressing stays a LATENT strategy discovered because it lowers store-CE, not a supervised target. (Beats unlabeled sharpening/self-distill which can reinforce a weak run, and late-EMA which can't escape an early bad basin.)

## $0 PRE-SCREEN — ✅ PASS (from existing ckpts · no train)
Does store-CE rank strong-address above weak-address? Existing fresh ckpts (summer, H_9720 originals + H_9792 audit):
| ckpt | lookup(≈store-acc) | addr_top1 |
|---|---|---|
| fresh_s7 | 0.922 | 0.898 |
| fresh3_s4302_wu | 0.922 | 0.906 |
| fresh3_s4302 (no-wu) | 0.664 | 0.453 |
⟹ store-accuracy(≈ −CE) ranks high-addr ckpts ABOVE the low-addr one ⟹ CE is a usable admissible selector. Pre-screen PASS.

## Pre-registered PASS/KILL (pool · seeds {7,11,4302,4303})
- Control A: legacy single run (identical recipe). Diagnostic-only: random replica selection; oracle-best addr_top1 (computed AFTER, NEVER used to select).
- **PASS**: selected treatment ckpt addr_top1 ≥ 0.85 on ≥3/4 seeds, no material store-task regression vs Control A.
- **KILL**: <3/4 pass; OR oracle passes but store-CE selection repeatedly picks a sub-0.85 replica (store-CE not a usable selector) → kill restart scaling, not pool size.

## Cost
$0 pre-screen ✅ done → pool-GPU: 4× one training run (+3× incremental; sequential=same peak mem OR 4-parallel) + one store-only pass per replica for selection. ~$2-3 (303M · owner-directed cement).

## Distinct-from-kills
- NOT --store-addr-weight (supervises address · killed→adjunct). NOT value-warmup-alone (fixes VALUE not address run-variance · H_9792 measured). NOT key/width/recurrence (killed). NOT post-hoc cross-seed averaging (this is single-run robustness).

## Verdict-integrity
Any number here is DIRECTIONAL until produced by `anima-py train --store-query-fresh-restarts` + `anima-py evaluate` on the 303M py channel. A PASS reads "the good emergent-address basin is store-CE-selectable", NOT "the address was supervised".
