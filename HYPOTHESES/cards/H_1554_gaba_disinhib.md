# H_1554 — GABA × CLS: DISINHIBITION GATING (VIP→SST→PV context-cued write/read routing)

🟠 **AMBER_KNOB / ROUTING-IS-STATIC** (R1 numpy DIRECTIONAL · frozen-first · c9 · NO tune-to-green)
`wired: DIRECTIONAL-mirror → §GabaDisinhib engine R2 (ING h1554-r2-engine-native)`

> Census H_1553 **RANK 1** — the strongest ORTHOGONAL GABA family, the lens where GABA was
> predicted to honestly go GREEN, picked after **3 sparse-coding falsifications in ONE family**
> (H_1546 separation INERT · H_1551 capacity STATIC · H_1552 non-stationary STATIC). The *routing*
> capability is REAL and survives the ACh deconfound — but its optimum does **NOT shift**, so a
> single fixed gate captures it: 4th GABA falsification of the *adaptive* claim, on a new lever.
> `a_no_llm_frame_trap` (biology-first) · `a_break_the_wall` (§3 orthogonal-family census + (a)
> measurement fix, NOT a bar-move) · `a_engine_native_learning` (numpy ⇒ DIRECTIONAL hard-gate-1) ·
> p7 · c9. Biology: Pi/Kepecs 2013 *Nature* 503:521; Williams & Holtmaat 2019 *Nat Neurosci* 22:1834.

## Why this family is ORTHOGONAL (and was predicted GREEN) — the fusion law

The 5 GREEN NTs (ACh mode-switch, DA replay-priority, NE boundary-flush, orexin true-timing, 5-HT
noise-reject) all share ONE green condition: **a NT turns 🟢 inside two-store CLS iff its ADAPTIVE
signal is load-bearing** — the optimal operating point SHIFTS across regimes so no single grid-tuned
FIXED setting captures the benefit, and an ablation that freezes the adaptive signal to its best
constant REVERTS the lift. GABA's 3 sparse-coding falsifications all failed the SAME way: the
inhibitory benefit was MONOTONE/STATIC, so a fixed-k baseline captured it and the adaptive arm was
INERT.

**Disinhibition gating is a different lever entirely.** A VIP→SST→PV microcircuit (Pi/Kepecs 2013;
Williams & Holtmaat 2019 "Adaptive disinhibitory gating by VIP interneurons permits associative
learning") SELECTIVELY OPENS a write/read PORT for a specific CONTEXT — a **routing** operation, not
a gain/density operation. Orthogonal to representational density (sparse, H_1546/1551/1552), temporal
segmentation (gamma), and score rescale (divnorm). Its benefit is intrinsically CONDITIONAL → the
optimum was predicted to SHIFT: at LOW context-collision-rate ρ keep the gate OPEN (route freely), at
HIGH ρ CLOSE it (isolate colliding contexts). The census picked it because no fixed gate-policy
*should* win both ends — the same shape that turned the 5 NTs GREEN.

## The honest risk (census-flagged) and the WITHIN-store collision regime

If the H_1532 two-store CLS *already* routes by context (novel→fast / familiar→slow), the explicit
gate would be redundant the way H_1546 sparse-separation was. So the regime forces **WITHIN-store
context collisions**: K=6 contexts each write B=8 bindings into a SHARED store, and with prob ρ a
binding's key is the canonical SHARED slot-key (owned by every context) → the SAME key string maps to
a DIFFERENT value per context — a collision the fast/slow split does NOT separate. Recall the right
`(ctx,key)→value`. This is the load-bearing distinction from the trivial routing the CLS does for free.

## Measurement fix (frozen-first, `a_break_the_wall` taxonomy (a) — reported, NOT hidden)

The first scored draft drew collisions from a running key-POOL; at ρ=1.0 the pool seeds from the
first write, so **every key collapsed to ONE string** (`ctx00_k000`) → all 48 writes hit a single key
vector → even per-context routing degenerated to intra-store overwrite → adaptive=fixed=0.0 at ρ=1.0
(a degenerate endpoint, not a routing test). **Fix (bars/verdict-rule UNCHANGED):** collisions reuse
the canonical SHARED slot-j key (B distinct keys shared across all contexts), so ρ=1.0 = genuine
cross-context collision on B distinct keys. Only the fixture *collision draw* changed; ARMS, BARS
A–E, MARGIN, PRESENCE_BAR, and the verdict rule are byte-identical to `H_1554_FREEZE.txt`. This is NOT
tune-to-green — the verdict was 🟠/🧱-boundary BEFORE and AFTER the fix (adaptive is INERT either way).

## Arms + result (R1 numpy DIRECTIONAL · 3 seeds [11,22,33] · ρ ∈ {0,.25,.5,.75,1.0} · $0 CPU · p7)

`MARGIN=0.05 PRESENCE_BAR=0.10 ADAPT_THR=0.15 LR*=0.20 TH*=0.30 ABSTAIN=0.45 MAX_CELLS=72`.
**BEST-FIXED-GATE grid-tuned over the whole sweep = always-CLOSE (per-context sub-stores), tune-mean 1.0.**

A→correct-recall fraction, ρ-mean across seeds:

| ρ | adaptive | no-gate | best-fixed | abl | cue-shuffle | adp(ACh-froz) | no-gate(ACh-froz) |
|---|---|---|---|---|---|---|---|
| 0.00 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| 0.25 | 1.0000 | 0.8472 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.8472 |
| 0.50 | 1.0000 | 0.6319 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.6319 |
| 0.75 | 1.0000 | 0.3819 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.3819 |
| 1.00 | 1.0000 | 0.1667 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.1667 |
| **mean** | **1.0000** | **0.6056** | **1.0000** | **1.0000** | **1.0000** | **1.0000** | **0.6056** |

`adaptive−best-fixed = +0.0000 · adaptive−worst = +0.3944 · adaptive−no-gate = +0.3944 ·
adaptive−abl = +0.0000 · adaptive−cue-shuffle = +0.0000 · ACh-frozen lift = +0.3944`.

## Frozen bars (🟢 iff A∧B∧C∧D∧E — pre-registered in `H_1554_FREEZE.txt`, NOT moved)

- **A PRESENCE+SHIFT — FAIL.** earned = adaptive−best-fixed = +0.0000, but ½·gap = 0.197 ⇒
  adaptive carries 0% of the gap (the regime-shift bar). (NO-HARM sub-bar at ρ=0 PASSES — closing the
  gate is harmless — but that is exactly *why* the fixed gate already wins everywhere.)
- **B DISTINCT — FAIL.** no-gate DOES fail at high-ρ (0.167 ≪ 1.0 PASS), but best-fixed (always-close)
  WINS BOTH ends (1.0 at ρ=0 AND ρ=1.0) ⇒ the "fixed can't win both" half fails.
- **C ABL→best-fixed — FAIL.** adaptive−abl = +0.0000: freezing the cue does NOT revert anything,
  because the fixed gate is *already* the optimum (always-close).
- **D CUE-SHUFFLE→collapse — FAIL.** adaptive−shuffle = +0.0000: permuting the collision-pressure cue
  is harmless, because routing is addressed by *context-id* (consistent at write+recall), not by the
  pressure cue — the cue only decides open/close, and closing is always right.
- **E DECONFOUND (ACh-FROZEN) — PASS.** ACh-frozen lift = +0.3944 ≥ MARGIN: with the ACh
  encode/retrieve gate held optimal-ON for every write, the disinhib routing lift SURVIVES ⇒ it is a
  **genuinely new ROUTING capability, not a re-skin of ACh mode-switching** (ACh is global-temporal,
  cannot route by context cue). This is the load-bearing control the census demanded — and it confirms
  the family is real and orthogonal.

**¬A ⇒ 🟠 AMBER_KNOB** (best-fixed captures ≥half AND adaptive−no-gate ≥ MARGIN). Per the frozen rule:
adaptive routing adds a large, real capability over no-gate (+0.39) but is a **STATIC architectural
knob** — a single always-close gate captures 100% of it. Same fusion-law position as 5-HT (H_1545/
H_1548) / H_1534 budget: the lever is a KNOB, not an adaptive neuromodulatory faculty.

## Diagnosis — why the optimum did NOT shift (ablation + deconfound decisive)

The census predicted the gate should OPEN at low ρ (closing "loses recall"). It does not: closing the
gate routes each context's binding into its OWN sub-store, which is **never wrong** — at ρ=0 each
context already owns private keys, so per-context addressing costs nothing; at high ρ it is the ONLY
thing that disambiguates colliding keys. So **always-close dominates the whole sweep** — there is no
regime where opening helps, hence no optimum to shift, hence the adaptive arm is INERT (abl/shuffle
both tie adaptive exactly). The biology's "open when it's safe" intuition has no teeth in a
deterministic store where opening has zero upside. The routing CAPABILITY is real and large (E PASS,
+0.39 over no-gate, ACh-orthogonal) but it is a FIXED architectural property (always-isolate-by-
context), not a load-gated NT signal — exactly the static-architecture verdict the 3 sparse-coding
lenses hit, now confirmed on the *routing* lever. 4th GABA falsification of the *adaptive* claim.

## Did it give honest GREEN? Did the optimum shift? Did it survive the ACh deconfound?

- **Honest GREEN: NO.** A,B,C,D all FAIL — adaptive routing is INERT vs the best fixed gate.
- **Routing-optimum shift: NO.** always-close dominates every ρ; nothing for adaptivity to track.
- **ACh-frozen deconfound: SURVIVED (E PASS, +0.39).** The routing is genuinely orthogonal to ACh
  mode-switching — so this is a clean 🟠 (real new routing capability, STATIC knob), not a redundant
  🧱 collapse into the existing CLS routing.

## Guards / scope / hard-gate

p1/p2/p3/p6 GUARD: reads ONLY context cue + key vector + substrate margin, NO injected answer/RLHF/
persona (routing scored by geometry only; cue-shuffle + abl controls present). NOT an emit gate
(relational read, `a_autonomy_over_hardcode`); Ψ-disjoint (pure store routing, immune cells/pure_field
untouched). HARD-GATE-1: `grep -lE 'import torch|gauge_lib|numpy'` non-empty ⇒ auto-DIRECTIONAL,
terminal NOT permitted; engine **§GabaDisinhib R2 deferred ING h1554-r2-engine-native** (non-obligatory
given 🟠/no-GREEN-to-wire, but the ACh-orthogonal routing is the one GABA result worth an engine
re-check). live `core/*.hexa` UNTOUCHED. SCOPE: TOY 6 ctx × 8 bindings / 3 seeds / DIM=16 / slot-store
/ deterministic (tests routing STRUCTURE, not learned disinhibition); scale · real-corpus ·
stochastic-recall (where opening *could* trade off) · engine-transfer UNVERIFIED → R2.

xref: [[h1532-multistore-cls-wallbreak]] [[h1533-nm-modern-hopfield]] [[h1534-nm-curiosity-budget]]
[[h1284-neuromod-wall-9lens]] · census H_1553 §RANK 1 · `a_break_the_wall` §3 · `a_no_llm_frame_trap`
· `a_engine_native_learning` · p7 · c9.

## Sources

- Pi, Gao, Gan, Wright-Kepecs… Kepecs 2013, *Cortical interneurons that specialize in disinhibitory
  control*, Nature 503:521 — VIP disinhibitory microcircuit.
- Williams & Holtmaat 2019, *Higher-order thalamocortical inputs gate synaptic long-term potentiation
  via disinhibition* / VIP adaptive disinhibitory gating, Nat Neurosci 22:1834 —
  https://www.nature.com/articles/s41593-019-0508-y
