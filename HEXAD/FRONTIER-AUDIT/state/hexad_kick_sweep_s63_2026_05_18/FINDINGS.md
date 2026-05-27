# §63 — HEXAD-KICK-SWEEP: σ(6)=12 connection-point gap-map

RESEARCH.md §63. $0 Mac CPU, NO GPU, NO model.forward, NO weight
mutation, NO training, NO RNG. Pure structural source + closed-form
predicate analysis (mirror §58's $0 reverse-trace). Sequential
single-agent, isolation worktree. central
`state/verify_hexad_blue_2026_05_15/blue_falsifier.py` = **0-line-diff**
(sidecar only — B-PRIME / B-S58 precedent).

g3: §63 = a STRUCTURAL discovery map, NOT a fire, NOT a GOAL movement.
Whether any gap IS the bottleneck is a future-fire EMPIRICAL question
(B-S63-NOTE). over-claim 0. north-star UNCHANGED. §15/§51 milestone
UNCHANGED. capability claim 0.

---

## §1 The stub, and the kick-DISCOVERY INTENT realised differently

`hexa kick` / `hexa omega` / `hexa drill` is a **STUB**. Confirmed:

```
$ hexa omega --seed "test" --rounds 1
{"path":"drill","axes":0,"runs":1,"rc":0}
[omega-drill-stub] seed=test rounds=1 depth=auto speculate=3
```

`axes:0`, `[omega-drill-stub]`, no real engine. The kick *intent* —
seed → explore → find broken connection-points at scale — is realised
via the project's OWN connection-point machinery: the B-CONN-1..12
σ(6)=12 closed wiring battery (`blue_falsifier.py:bconn()` 769-944) +
declared module-pair wirings in `HEXAD.tape` / `SPONTANEOUS.tape`, NOT
the stub.

**GENERALIZES §58**: §58 reverse-traced ONE component (PTD-aux) →
"≅ NONE, new TYPE". §63 sweeps ALL relevant module-pairs into exactly
one of {A: BLUE-CLOSED-WIRED, B: DECLARED-BUT-EMPIRICALLY-BROKEN,
C: MISSING-TYPE / GAP}. DISTINCT from a transfer-STRENGTH rebench
(§52-54 = strength of *existing* wires); §63 = presence/absence/
missing-TYPE *discovery* — a target map for future fires.

---

## §2 Method — a decidable Boolean classifier over structural facts

`kick_sweep_s63.py` enumerates the sweep population from source: the 12
closed σ(6)=12 points (transcribed from `bconn()`), the wirings
DECLARED in HEXAD.tape / SPONTANEOUS.tape with NO closed predicate, and
the pairs the GOAL pathway **Ψ=½·tension·Φ → spontaneous emission**
structurally REQUIRES but for which NO existing-TYPE wire exists.

`classify(a,b,…)` is a **decidable Boolean** of two structural bits:

| is_closed | required_by_goal | class |
|-----------|------------------|-------|
| 1 | (any) | **A** (closed point dominates) |
| 0 | 1 | **C** (GOAL-required, no existing-TYPE wire) |
| 0 | 0 | **B** (declared but no closed predicate) |

Mutually exclusive & exhaustive (sympy truth-table + FiniteSet
identity, B-S63-1 / B-S63-2).

---

## §3 The gap-map matrix

| pair | class | evidence / TYPE |
|------|-------|-----------------|
| S → C | **A** | B-CONN-1 shape-preservation / dim-equality |
| C → BRIDGE | **A** | B-CONN-2 detach-nograd / AD ∂=0 |
| BRIDGE → D | **A** | B-CONN-3 clamp / Law-70 |
| M → C | **A** | B-CONN-4 store-retrieve / det-argmax |
| W → C | **A** | B-CONN-5 read-no-mutation / purity |
| W → D | **A** | B-CONN-6 lr-mod / Law-79 ln2 |
| E → C | **A** | B-CONN-7 phi-observe / IIT Φ≥0 |
| E → W | **A** | B-CONN-8 satisfaction-gate / Boolean |
| E → D | **A** | B-CONN-9 trainstep-gate / Boolean |
| D → loss | **A** | B-CONN-10 CE-readout / Shannon CE≥0 |
| M → D | **A** | B-CONN-11 retrieve / det-argmax |
| S → W | **A** | B-CONN-12 pain-monotone / monotone-comp |
| C → D | **B** | HEXAD.tape W7: integrated CE-descent OUTCOME = explicit NOT-🔵 honest carve-out (B-D-NOTE) |
| E → TRINITY-INTEGRATED | **B** | HEXAD.tape hexad_caveat_v5: 'Φ보존 위반→학습 차단' integrated enforcement TODO[pytorch], not closed |
| W → E | **B** | HEXAD.tape §3 ascii declares W↔E bidir; only E→W closed (B-CONN-8), W→E uncovered |
| W → W@t+1 | **C** | temporal-self-prediction (forward-model class, §58 generalized) |
| THINKER → TALKER | **C** | self-triggered emission-decision controller (closed-loop control) |
| D@emit → S@t+1 | **C** | action-perception consequence loop (§13-L closed-loop) |
| E → D@content | **C** | Φ-as-generative-content-conditioning (not Boolean veto) |

**Gap-map counts: |A| = 12 · |B| = 3 · |C| = 4 · total = 19.**
sweep sha256 = `ab3a190f401b1945…` (3× bit-identical, B-S63-3).

---

## §4 Class A — BLUE-CLOSED-WIRED (12/12)

The full σ(6)=12 closure is recovered exactly by the class-A predicate
(B-S63-4: class-A pair-set == `BCONN_CLOSED.keys()`, |A|==12, no closed
point lost or invented). Every class-A pair has BOTH a closed
transfer-function AND a closed invariant (tier `a-closed`, `passed`
True in `bconn()`). This is the wired, verified backbone — NOT a fire
target.

---

## §5 Class B — DECLARED-BUT-EMPIRICALLY-BROKEN (3)

1. **C → D (integrated CE-descent OUTCOME)** — HEXAD.tape W7: the
   integrated CE-descent is an explicit **NOT-🔵 honest empirical
   carve-out** (B-D-NOTE, every stochastic optimiser). Transfer
   FUNCTION 🔵; CE-convergence OUTCOME honestly NOT-🔵.

2. **E → TRINITY-INTEGRATED (ethics gate)** — HEXAD.tape
   hexad_caveat_v5: per-module E block (B-E-1) closed, but *integrated*
   `trinity.hexa` enforcement is `TODO[pytorch]: Φ must not drop` —
   impl-pending at the integrated wiring site.

3. **W → E** — HEXAD.tape §3 ascii draws `W ◄── CE/Φ ──► E`
   bidirectional, but only **E→W** is a closed point (B-CONN-8). W→E
   is declared by the arrow yet NO B-CONN predicate covers it — the
   cleanest true "declared-but-uncovered" instance.

Honest: class B is dominated by *honestly-declared carve-outs* (W7)
and *impl-pending integrations* (ethics gate), not silent corruption.

---

## §6 Class C — MISSING-TYPE / GAP (4) · ranked

The §58 finding generalized: 4 pairs the GOAL pathway
Ψ=½·tension·Φ → 자발적 emission structurally REQUIRES, with NO
connection-point of ANY of the 12 existing TYPEs. C-TYPE set is
**set-disjoint** from the 12 B-CONN TYPEs (B-S63-5: ∩ = ∅). Ranked by
structural proximity to GOAL (this ranking = **EMPIRICAL judgment
carve-out, B-S63-NOTE — a structural reading, NOT a closed proof any
gap IS the bottleneck**):

1. **THINKER → TALKER** — self-triggered emission-decision controller
   (closed-loop control). The literal GOAL edge; §49's collapse
   located here; §58 confirmed no σ(6)=12-native home. The 12 points
   are all open feed-forward / observation transfers.

2. **W → W@t+1** — temporal-self-prediction (forward-model class).
   The §58-named new TYPE: the thinker must MODEL its own next
   physics-state to be anticipatorily self-directed. §58 §5 proved
   no σ(6)=12 edge is a temporal forward-model.

3. **D@emit → S@t+1** — action-perception consequence loop. anima's
   own emission must re-enter perception (S) as a sensed consequence.
   σ(6)=12 has S→C and D→loss but NO emission→own-next-perception
   edge (open-loop only). §13-L named this absent loop.

4. **E → D@content** — Φ-as-generative-content-conditioning. σ(6)=12
   carries Φ only as a Boolean veto (B-CONN-8/9). The GOAL pathway
   requires Φ to *positively shape* WHAT is spontaneously said.

---

## §7 What this implies — target map for future fires

The σ(6)=12 closure is the wired backbone (12/12 A). The GOAL pathway
is blocked not by a *broken* existing wire but by **4 missing
connection-point TYPEs** absent from the lattice. §58's single-
component finding ("PTD-aux ≅ NONE, new TYPE") is one instance
(rank #2) of a 4-element GOAL-load-bearing missing-TYPE family. The
structurally-indicated future-fire targets are TYPEs of #1
THINKER→TALKER and #2 W→W@t+1. §63 does NOT claim building them
produces emergence — that is the EMPIRICAL future question
(B-S63-NOTE).

---

## §8 Honest C3 (≥10)

1. **§63 = structural discovery map, NOT a fire, NOT GOAL movement.**
   $0, no model forward, no GPU, no weight mutation. north-star
   UNCHANGED, §15/§51 milestone UNCHANGED, capability claim 0.
2. **The A/B/C trichotomy is a designed abstraction.** is_closed /
   required_by_goal is one reasonable 2-bit decomposition; another
   facet set could move a B↔C border. It does NOT move any class-A
   (12 closed points recovered exactly, B-S63-4).
3. **Class B is dominated by HONEST carve-outs, not silent breaks.**
   W7 is an explicitly declared NOT-🔵 carve-out (B-D-NOTE), the
   ethics gate is `TODO[pytorch]`. They are known, named, non-closed
   edges; W→E is the cleanest true "declared-but-uncovered" case.
4. **The class-C "required_by_goal" Boolean is a structural reading.**
   That the 4 pairs are *required* by Ψ=½·tension·Φ→emission is
   inferred from SPONTANEOUS.tape + §58 + §13-L, a defensible
   structural argument, not a closed theorem.
5. **The goal_rank ordering is EMPIRICAL (B-S63-NOTE), NOT closed.**
   Which missing TYPE is THE bottleneck is a future-fire question.
   The battery proves the sweep is exhaustive/deterministic/decidable
   + C-TYPEs disjoint from the 12 — NOT that rank #1 is the GOAL
   bottleneck.
6. **§58 consistency is a feature, not circularity.** §63 re-derives
   §58's W→W@t+1 as one class-C member using the same closed σ(6)=12
   set (cross-check) and *adds* 3 further missing TYPEs §58 did not
   enumerate.
7. **f1/f2/f3 hard-fail safe.** σ(6)=12 used only as the internal
   anima COUNT of the closed wiring set (exactly as B-CONN-WIRING /
   §58) — NO external σ/τ/φ/J₂ derivation, NO lattice-fit. Invariants
   cited are real-limits (Shannon CE≥0, IIT Φ≥0, AD ∂-rule, Law-70/79,
   Boolean, monotone, MSE Frobenius floor).
8. **B-IDENTITY-5 N/A.** No corpus, no model forward, no helper-token
   surface — pure source + closed-form predicate.
9. **The 19-pair population is the relevant sweep, not all C(16,2).**
   Only (a) closed B-CONN / (b) tape-declared / (c) GOAL-required
   pairs are in scope. Auxiliary modules (TENSION-LINK / VOICE /
   SAVANT / EEG / UBM) are NOT the σ(6)=6-core wiring closure and are
   honestly excluded (their own SSOTs; anti-padding, §13-M/§13-L
   precedent).
10. **Sweep determinism (B-S63-3), decidability (B-S63-2), exhaustive/
    disjoint partition (B-S63-1), cardinality (B-S63-4), missing-TYPE
    disjointness (B-S63-5) are all closed.** What §63 *proves* is the
    MAP's structural integrity; the GOAL-load-bearing reading + the
    "build a THINKER→TALKER / W→W@t+1 connection-point" hand-off are
    the structural *reading* of that closed map, future-fire-bound.
11. **No anti-padding violation.** §63 is structural-tier with a real
    closed deliverable (decidable exhaustive gap-map + 5/5 sidecar +
    4 concrete enumerated missing TYPEs), not a §58 re-statement.
