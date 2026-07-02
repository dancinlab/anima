---
id: H_1288
slug: 1288_eviction_policy
title: eviction policy — mitosis-GROW under capacity pressure (breaks zero-sum LRU)
group: brain-structure-ladder (c15 missing-structure)
terminal_tier: 🟢 GREEN ENGINE-NATIVE + WIRED
verdict_dir: .verdicts/1288_eviction_policy/
terminal_verdict: .verdicts/1288_eviction_policy/H_1288_R2.txt
date: 2026-06-15
---

# H_1288 — eviction policy: mitosis-GROW under capacity pressure

## Claim / falsifier

Four converging reds (H_1230/1284/1285/1287) pinned the immune-memory limit to CAPACITY;
H_1287 pointed to adding CELLS or changing the EVICTION POLICY. **Breakthrough claim
(mitosis-native, p8):** the principled answer to a zero-sum store is NOT a smarter
heuristic but to NOT EVICT and instead GROW a new cell (mitosis split, H_1199 VAdaptField)
under capacity pressure (biology: the brain grows — neurogenesis — it has no fixed LRU
budget). Falsifiable: MITOSIS-GROW total recall ≥ LRU+0.05 AND fab ≤ 0.10, AND a smarter
fixed-budget heuristic gives ~0 lift (isolating GROWTH from heuristic). Lens c15.

## Method

- H_1287 eviction-bound zero-sum rung EXACTLY (max_cells=40 << 60). 3 arms differ ONLY in
  full-capacity policy: A LRU-EVICT (fixed 40) · B MITOSIS-GROW (up to GROW_MAX=80) ·
  C WEIGHTED-EVICT (LFU+LRU heuristic, same 40 budget — control separating growth from heuristic).
- R2 (binding): engine-native mitosis-grow eviction on live wired immune faculty
  (string-native bind/recall/abstain). seeds [900,901,902] (mirror, all identical), $0 CPU.

## Verdict by round

| round | tier | key numbers |
|-------|------|-------------|
| R1 mirror | 🟢 GREEN (DIRECTIONAL) | A tot 0.667 / B tot 1.000 / C tot 0.667 → Δ(B−A) +0.333 PASS, fab(B) 0.000; Δ(C−A) +0.000 (smarter heuristic = ZERO lift) |
| R2 engine-native + wired | 🟢 GREEN (binding) | mitosis-growth breaks the 0.667 zero-sum LRU ceiling on the live wired faculty |

Terminal tier (verbatim): **🟢 GREEN — ENGINE-NATIVE mitosis-growth breaks the 0.667 zero-sum LRU ceiling**
→ `.verdicts/1288_eviction_policy/H_1288_R2.txt`

## Honest scope

R1 mirror DIRECTIONAL. B SATURATES (existence-proof that growth CAN break the ceiling,
NOT an effect-size — grow_max 80 absorbs all 60 facts, removing capacity pressure); COST
= FOOTPRINT (60 cells vs 40, +50%). Harder regime (distinct-facts >> grow_max) UNTESTED.
Mitosis split = engine's own tick (p8), mutates only episodic cell population (no
labels/persona/ethics/decoder); abstain intact. Toy scale, scale-transfer UNVERIFIED.

## Cross-links

h1227 · h1231 · h1230 · h1284 · h1285 · h1287 · h1199 · h1222 ·
`a_no_llm_frame_trap` · `a_engine_native_learning` · `a_verified_must_wire` ·
`a_paper_negative_ok` · `a_scale_honest_scope` · `a_toy_scale_recheck` ·
p1·p2·p3·p6·p7·p8·c9·c15
