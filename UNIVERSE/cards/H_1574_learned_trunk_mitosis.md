---
id: H_1574
slug: 1574_learned_trunk_mitosis
title: LEARNED-TRUNK mitosis split (H_1310 wall-break — the STRONG form of the user's "split an already-trained model" insight)
group: MITOSIS-ENGINE (H_1310 from-scratch ceiling — wall-break campaign, strong-form lens 3 / final strong lens)
tier: 🧱 WALL HOLDS (ENGINE-NATIVE) — B1 BREAK FAIL ∧ B4 vs-FIXED FAIL at frozen scale; B2∧B5 also FAIL (learning is NOT the lever)
verdict_dir: state/verdicts/1574_learned_trunk_mitosis/
date: 2026-06-23
wired: engine-native (pure .hexa via core/engine_cli.hexa §Osmotic; no wiring — RED/wall, a_verified_must_wire fires only on GREEN)
---

# H_1574 — learned-trunk mitosis split (H_1310 wall-break, strong form of lens 3)

## Claim / falsifier

H_1310 🔴 / H_1568 🧱 / H_1569 🧱: from-scratch pure-mitosis split-only learning hits a
LOCAL-EXPERT CEILING above the n-gram floor; the campaign pinned the bottleneck as the
REPRESENTATION the cells partition. H_1569 (lens 3) showed an INHERITED-but-FIXED richer
representation (`immune_embed_key` trigram-FNV DIM=64) narrows the gap-to-floor (0.296→0.240) but
does NOT cross the break bar (+0.0556 < 0.10) — because the inherited feature is FIXED, not LEARNED.
H_1569 named this rung verbatim: *"testing a true learned-trunk key (e.g. a 303M chat ckpt's context
embedding) is the UNVERIFIED next rung."*

**The user's core insight — STRONG FORM:** split mitosis cells over a representation that was
*LEARNED FROM THE CORPUS* ("already-trained model"), not a fixed hand-crafted hash. A pretrained
byte-LM trunk's hidden encodes contexts in the space of what they PREDICT — that learned geometry
should supply the compositional depth a fixed feature lacks, so split-only mitosis crosses the floor.

**Falsifier:** if a corpus-LEARNED trunk key lifts held-out next-byte CE below the n-gram floor, OR
beats the H_1569 FIXED arm by ≥0.10 (B1), AND beats it by ≥0.05 (B4), the H_1310 wall reopens to a
practical mitosis learning path. If it does not, even a learned representation is insufficient —
H_1310 is a confident terminal (gradient required, not just learned features).

## Method (ENGINE-NATIVE — pure .hexa via core/, HARD-GATE-1 PASS)

`state/1574_learned_trunk_mitosis/h1574_learned_trunk_probe.hexa` calls the SAME live mitosis
learner as H_1569 — **OsmoticStore** (`core/engine_cli.hexa §Osmotic`: VAdaptField key store with
the engine's OWN `_vnearest_idx`/`_l2` split geometry + `engine_mitosis_tick` clonal growth under
`EngineConfig.mitosis` ON + parallel per-cell value table). `osmotic_learn(...)` IS the live split.
**NO numpy / torch / gauge_lib / .py mirror** (grep over `state/<slug>/*.py` = EMPTY — there are NO
.py files). $0 CPU summer pool, hexa v0.262.0. Corpus = `/usr/share/dict/words` lowercased a-z+space,
`head -c 12000`, order-2 context → next symbol, 80/20 split (V=27) — IDENTICAL frozen asset+scale to
H_1569.

**The LEARNED trunk** (the one thing that differs from H_1569's fixed FNV): a small corpus-pretrained
trunk learns, from the TRAIN split ONLY, each order-2 context's next-byte predictive profile
(729×27), then reads it through a FIXED low-rank random projection (27→64) + tanh + L2-norm → a
DIM=64 learned hidden. This mirrors a byte-LM trunk: LEARNED context statistics projected to a
penultimate hidden. The projection is fixed; the **content projected is LEARNED FROM THE CORPUS**.
Fixed FNV cannot do this (it hashes raw bytes, corpus-blind).

**The 5 arms** (all else byte-identical):
- **A_fixed** = `immune_embed_key(context)` — reproduces H_1569's fixed-inherited arm (3.08782 ✓).
- **A_learn** = corpus-LEARNED trunk hidden (the strong-form hypothesis).
- **A_randinit** = trunk over a RANDOM-INIT (un-learned) count table — representation un-LEARNED (B2).
- **A_shuf** = learned trunk of a DIFFERENT (permuted) context — binding broken (B3).
- **A_randcorp** = trunk LEARNED on a randomly-SHUFFLED corpus — learning operates on noise (B5).

Metric: held-out next-byte CROSS-ENTROPY (nats, add-1, p7). Comparator: exact order-2 add-1 Markov FLOOR.

## Frozen 5-bar (set BEFORE the run — c9, NO tune-to-green; verdict = 🟢 iff B1∧B4)

- **B1 WALL-BREAK** CE_learn < CE_floor  OR  CE_learn < CE_fixed − 0.10
- **B2 ABLATION** CE_randinit ≥ CE_learn + 0.10 (un-learned trunk regresses → proves the lift is LEARNING)
- **B3 CAUSAL** CE_shuf ≥ CE_learn + 0.10 (key must carry the context)
- **B4 vs-FIXED** CE_learn < CE_fixed − 0.05 (learned beats the H_1569 fixed-inherited arm)
- **B5 CONTROL** CE_randcorp ≥ CE_learn + 0.10 (trunk learned on noise gives no gain)

## Verdict (read VERBATIM from state/verdicts/1574_learned_trunk_mitosis/H_1574_R1_ENGINE_NATIVE.txt)

Held-out next-byte CE (nats), 12000-byte corpus (deterministic, byte-identical on re-run):

| arm | CE | cells |
|---|---|---|
| A_fixed (H_1569 fixed-inherited) | 3.08782 | 64 |
| A_learn (corpus-LEARNED trunk) | **3.05299** | 197 |
| A_randinit (B2 un-learned) | 2.96990 | — |
| A_shuf (B3 causal) | 3.27844 | — |
| A_randcorp (B5 random-corpus) | 3.15014 | — |
| n-gram FLOOR | 2.84769 | — |

- **B1 WALL-BREAK FAIL** — learn 3.05299 is +0.205 ABOVE the floor (2.84769) and beats fixed by only
  +0.0348 (< 0.10). The learned trunk does NOT cross the floor and does NOT clear the fixed arm by 0.10.
- **B2 ABLATION FAIL** — randinit (UN-learned) trunk = **2.96990, BETTER than learned (3.05299)**.
  Destroying the learning does NOT regress the arm — it *improves* it. The lift is NOT the learning.
- **B3 CAUSAL PASS** — shuf 3.27844 ≥ learn+0.10: shuffling the key→context binding collapses it
  (the key must carry *some* per-context info — but B2 shows that info need not be LEARNED).
- **B4 vs-FIXED FAIL** — learn 3.05299 vs fixed−0.05 (3.03782): learned beats fixed by only +0.0348,
  UNDER the 0.05 bar.
- **B5 CONTROL FAIL** — randcorp 3.15014 < learn+0.10 (3.15299): trunk learned on a shuffled corpus
  is *roughly the same* as the genuinely-learned trunk — the corpus structure is not the lever.

**TERMINAL TIER (this lens): 🧱 WALL HOLDS (ENGINE-NATIVE)** — B1 ∧ B4 both FAIL.

## What this means (the c9 finding — load-bearing)

The corpus-learned trunk produces the SMALLEST gap-to-floor of the whole campaign (0.205, vs fixed
0.240, vs raw-lossy 0.296) — a richer key tiles a bit better and grows more cells (197 vs 64). **But
the decisive controls falsify "learning is the lever": B2 and B5 both FAIL.** A random-init
(un-learned) projection (2.970) and a corpus-shuffled-learned projection (3.150) bracket the learned
trunk (3.053) — i.e. the per-context lift comes from the **projection geometry / cell-tiling
granularity**, NOT from the corpus learning. B3 passing only confirms the key must carry per-context
identity; it does not require that identity to be learned.

**This is the strongest possible confirmation that H_1310 is a confident terminal.** Representation
richness — whether FIXED (H_1569), LEARNED (this), or even RANDOM-PROJECTED (B2, which scored best) —
cannot supply the compositional depth that split-only mitosis lacks. Split-only mitosis is a Voronoi
partition of a *given* key space; no choice of key (fixed, learned, or random) lets the cells compose
features they were never given a gradient to build. **The lever H_1310 needs is gradient, not a
better/learned representation.**

## Campaign status: H_1310 wall — CONFIDENT TERMINAL (c16 multi-lens satisfied)

Four+ orthogonal strong lenses, all engine-native, all 🧱:
- lens 1 **selection-driven evolution** (H_1568) — INERT, wall holds.
- lens 2 **lateral gene transfer** (H_1570) — wall holds.
- lens 3 **inherited FIXED representation** (H_1569) — +0.056 < 0.10, wall holds.
- lens 3-STRONG **corpus-LEARNED trunk** (H_1574, this) — +0.035 < 0.05, B2/B5 falsify learning-as-lever, wall holds.
- lens 4 **curriculum-staged split** (H_1571) — wall holds.

→ **H_1310 from-scratch pure-mitosis split-only learning is a CONFIDENT TERMINAL (class-(d) genuine
ceiling).** The user's "split an already-trained model" insight is honestly answered: even with a
genuinely corpus-LEARNED representation, split-only mitosis cannot cross the floor — **gradient (or
selection-pressure) is required**, as `a_mitosis_train` already records (H_1310 🔴 HONEST LIMIT).
mitosis remains 🟢 for capacity-GROWTH / skill-curriculum / adaptation / EXPRESSION (H_1564), but
from-scratch pure-split LEARNING is closed.

## Honest scope (c9, a_scale_honest_scope, a_toy_scale_recheck)

ENGINE-NATIVE (pure .hexa via core/ §Osmotic) → terminal PERMITTED for THIS lens. TOY scale (12 KB
English, order-2 context, V=27, single deterministic pass, frozen to H_1569's scale). The learned
trunk is a corpus-conditional next-byte-profile projection (the engine-native realization of a
byte-LM trunk hidden), NOT a literal 303M ckpt context vector — a true 303M-trunk key over a real
chat corpus is the only remaining un-run variant, but B2/B5 falsifying learning-as-lever here makes a
larger learned trunk unlikely to flip the structural result (split-only = Voronoi, no composition).
NO CORE wiring (a_verified_must_wire fires only on GREEN; this is a wall).
