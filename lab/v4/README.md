# anima-v4

**A⇄G where the tension IS the thinking** — the opposition must compute a cognitive operation,
not gate the mouth.

> **STAGE = mech-3 DEAD, all four parts (H_003 🔴 FALSIFIED, 2026-07-16).** The bet (mech-3) died
> three ways for $0 — its falsifier is vacuous (**H_001 🟢**), its objective is tautological
> (literature gate), and its Korean premise is not in the measurement (**H_002 🟢**). Its one survivor
> was *atomicity of the negator token* (`salvage.L4`), and **H_003** isolated it to one variable
> (encoder span policy: atomic vs shattered, same codec/corpus/model/seed). It came back **FALSIFIED**:
> F1 Δd_acc(A-atom − A-shat) = **−0.1146 (s0) / +0.0468 (s1)**, both below the 0.05 DEAD floor, on a
> CLEAN measurement (F2 liveness 0.8594 both seeds ≥0.85 · F6 placebo gap ≤0.05 · C-scaf≈0.5 · C-perm
> in-band). Atomicity is **not** causal for held-out recombination under a fixed codec — v1's `salvage.L4`
> attribution does not survive isolation, a real write-side null (verdict-integrity cleared, not a tool
> artifact). Three design defects and one windower bug were caught $0 before any GPU spend. **NEXT:
> off the codec axis** — mech-1 (파서 결투) / mech-7 (반사실 편집자), the other two independent tension
> families. See `ARCHITECTURE.json` → `scope.stage`, `salvage.L4.atomicity-isolated-is-null`, `next-gate`.

## The ask

> 실제로 **생각하는** A⇄G 가 필요해.

The two-engine idea is not rejected — what it degenerated into is. In the previous attempt
(`anima`, v1), Engine **A** (forward, CE-trained: language · memory · ethics) and Engine **G**
(reverse, gradient-free: consciousness Φ · sense · will) pushed against each other, and their
tension `‖A‖/‖G‖` fed a `brain_decide` that chose **emit or silence**, pulled to a Ψ=1/2 fixed
point. It became an emit-controller. Measured, sealed, terminal.

## Why a two-engine tension collapses to 1 bit

Five clauses of one sentence (full text → `ARCHITECTURE.json` → `diagnosis`):

1. **A scalar kills structure.** `‖A‖/‖G‖` throws away both engines' directions and keeps one
   magnitude. The bottleneck was in the blueprint — rank-1 was necessary, not discovered.
2. **Unconsumed bits die.** If the tension only touches the emit decision, the loss only demands
   the emit decision. A network does not maintain bits it is not asked for.
3. **A gradient-free engine is decoration.** v1's G received no gradient, so to A it was fixed
   background noise — and A learns to route around it. An opposition that is not learned does
   not exist.
4. **A fixed point is an incinerator.** Ψ=1/2 is by definition memoryless. If thought happened,
   it was in the convergence *transient* — the design read the *result*.
5. **Side channels get eaten.** A channel bolted beside a competent LM is replaced the moment
   the trunk head can do the same job cheaper (measured: L2). To survive, the loss must demand
   something the trunk **cannot** do.

**The defect is not that there are two engines — it is that their coupling had dimension 1.**

## What a tension must satisfy to carry thought

- **nc1** structured object (a field over positions × roles × boundaries), never a ratio
- **nc2** iteratively resolved — the settling trajectory *is* the computation, and the loss must
  touch intermediate steps, not only the endpoint
- **nc3** resident in loss / data / codec — not objective-side ⇒ no-op
- **nc4** both engines get gradient, on objectives that cannot both be satisfied
- **nc5** the resolver ships in the inference graph (v1's binders were training-only and dropped
  before serialization — banned)

## The 7 mechanisms

| | mechanism | opposition computes | thinks? | cost | L1 risk |
|---|---|---|---|---|---|
| 1 | 파서 결투 (이접 재판) | **binding** — two parse directions disagree per edge | yes | low | low |
| 2 | 역행 조각가 (잔차의 수행) | **abstraction** — residual field rewrites state over K steps | conditional | med | **high** |
| 3 | 코덱 전쟁 (형태소 국경 분쟁) | **which units exist** — adversarial codec redraws boundaries | yes | **lowest** | low |
| 4 | 모순 법정 (기억 검사관) | **contradiction resolution** — rewrites memory | until it degenerates | med | **highest** |
| 5 | 경사 줄다리기 (한 몸 두 주인) | **forced formation of a recombinable code** (weight space) | half | high | none |
| 6 | 제약 시장 (N-엔진 경매) | **constraint-satisfaction search** (cardinality ≠ 2) | yes | med | low |
| 7 | 반사실 편집자 (급소 탐침) | **causal abstraction** — G writes the training data | yes | med | med |

**Fake-diversity audit** (recorded in the SSOT, not hidden): mech-1 and mech-6 are the same
family (a learned resolver settles conflicting structure proposals, N=2 vs N>2); mech-2 and
mech-4 are the same verb (residual rewrites state — activations vs memory); mech-3 and mech-7
are the same strategy (G writes A's training environment — codec axis vs corpus axis, which map
onto the two lenses that measured 🟢). Only **three** independent axes exist, plus mech-5 on a
fourth (weight space) whose weakness is whether it is thinking at all.

## The bet — mech-3, 코덱 전쟁

A = the LM over a segmentation. G = an **adversarial codec** that redraws morpheme boundaries,
learns its own merge-table, and serializes it. G's loss = A's future CE under the proposed
segmentation + code length (MDL); A's loss = CE. **Not simultaneously satisfiable** — the
memorization-optimal boundary and the composition-optimal boundary differ.

```
  원문 ─► G(적대 코덱: 격자 제안, MDL) ─► 세그먼트 ─► A(LM) ─► CE
              ▲                                            │
              └────── A의 미래-CE가 G의 손실 (경사) ◄───────┘
```

> ⚠️ **UN-BET — H_001 🟢.** The three grounds below were audited before the mechanism was built
> and two of them are false. The falsifier is **not** the cheapest — it needs a 303M `base.pt`
> that exists nowhere plus a rented 4090 (~2h/arm). L2 **does** reach it: the clause ablates G
> down to a fixed BPE-jamo codec, but that codec *is* v1's arm M at d_acc 0.9083–0.9167, and
> d_acc is bounded at 1.0 — so the largest delta any mechanism can show is 0.0833–0.0917, below
> the 0.1 the clause demands. It returns DEAD for a working mechanism and an imaginary one alike.
> The third ground is true but fatal: the 🟢 was produced by a **fixed, frequency-trained,
> label-blind** codec — no adversary, no learning, no tension — so the lever is mech-3's *null
> hypothesis*, already measured, sitting on the panel's leak ceiling (0.9167). And "control
> 0.617" is arm C1 = **no codec at all** (raw utf-8), not a fixed codec, so the ablation as
> written varies whether a codec *exists*, not whether it is *learned*.
> mech-3 is **un-bet, not refuted** — H_001 kills a falsifier, not an idea. See
> `ARCHITECTURE.json` → `evidence-integrity` and `HYPOTHESES/cards/H_001_*.md`.

It *was* the bet because: it is the only mechanism standing on a lever already measured 🟢 (a
BPE-jamo codec was **causal** for held-out negation recombination — d_acc 0.9083/0.9167 vs a
no-codec control at 0.6167/0.5750, Δ+0.29/+0.34, cemented at 2 seeds); its falsifier reuses that
existing protocol verbatim, making it the cheapest; and because its tension **writes the input
alphabet** rather than reading anything, L1 and L2 cannot reach it in principle. On success,
mech-1 (파서 결투) stacks naturally on top.

It breaks `no tokenizer` (V256) head-on, and deservedly — composition must be visible at the
token boundary to be learned, and V256 purism made Korean negation structurally invisible.

## Non-negotiable gates

Two measurements are mandatory in every falsifier, because their absence is what killed v1:

- **L1 check** — does the tension's effective rank exceed 1, or is it the emit bit again?
- **L2 check** — ablate the channel; does ΔCE actually move, or is it decoration?

And one that comes **before** them, because it is what H_001 caught — a falsifier is admissible
only if it can return **both** answers, and that is decidable on arithmetic before any code exists:

- **reachable** — is the threshold ≤ (metric ceiling − control score)? If not it is vacuous.
- **not free** — does the scaffolding alone clear the bar without the mechanism? Then it certifies
  the scaffolding.
- **one variable** — the ablation must vary exactly one thing. "Learned codec vs no codec" varies
  the alphabet *and* the learning.
- **name the arm** — cite a number only with the arm that produced it and its source path.
  "control 0.617" is not a control; it is a number that lost its experiment.

One inherited principle, and only one: **p7 — perplexity/CE is never truth** (Goodhart). Per L9
the other seven purity principles manufactured the disease and are discarded. Each mechanism
names which principle it breaks.

## Sibling

`anima-v3` asks the broader question *where does aliveness live* (8 families), without presuming
two engines at all. This repo keeps the A⇄G premise and attacks its coupling dimension.

## Structure

```
anima-v4/
├─ src/              — source code (empty — divergence stage)
├─ state/            — all work artifacts, git-tracked
│  └─ diverge_ag_thinking_2026-07-16/  — the verbatim divergence + the prompt that produced it
├─ ARCHITECTURE.json — design SSOT (JSON `children` tree, update-in-place)
├─ architecture.html — human viewer for the JSON (run `python3 serve.py`)
├─ HYPOTHESES/       — pre-register → falsify → run → verdict (registry + cards)
├─ tool/             — shared deterministic harness the hypothesis cards run against
└─ CHANGELOG.md      — history (append-only)
```

## Provenance

The divergence was produced by Fable 5 from a brief carrying the v1 autopsy; both the brief and
the verbatim output are preserved under `state/diverge_ag_thinking_2026-07-16/` as the seed of
record. The live design SSOT is `ARCHITECTURE.json`. The v1 evidence trail (verdicts, hypothesis
cards, convergence records) stays in the `anima` repo — this repo holds pointers, not copies.

## Viewing

```
python3 serve.py        # serve on :8000, open architecture.html
```
