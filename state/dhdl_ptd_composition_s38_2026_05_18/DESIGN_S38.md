# §38 — DH-DL + PTD-aux Composition (DESIGN-TIER)

> $0 design-tier — NO fire, NO GPU, NO corpus generation. RESEARCH.md §38.
> Composes §27 DH-DL (decision-head dual-loss) with §29 PTD's
> PTD-as-DH-DL-aux combination A. §29 already argued the combination is
> GOAL-legitimate and scale-orthogonal; §38 produces the *design* — the
> combined objective, how PTD's trace-distillation term adds to DH-DL's
> dual-loss, the §7 GOAL-legitimacy check, and what the combination would
> measure that §27/§29 alone could not.
> design-tier ≠ fire ≠ capability ≠ emergence (g3). north-star unchanged.

---

## §1 — What §38 composes (one paragraph)

§27 DH-DL fired and landed a verdict of **DISTILLATION, not emergence** — a
thin 3-class gate-head `{CONTINUE_THINK, EMIT_VOICE, REMAIN_SILENT}` that
learns the §24 `talker_should_emit` threshold to 0.99937 accuracy with a
threshold-distillation gap of 0.00063. §29 design-closed PTD-standalone but
explicitly identified **PTD-as-DH-DL-aux (combination A) as the strongest
component combination** — because (a) DH-DL's §26/§27 spec *already* names
the §24 physics trace as its training corpus, so PTD is not an add-on but
the **corpus-formalisation of DH-DL's own training data**, and (b) a
≤1%-param gate head is **scale-orthogonal**, so the PTD auxiliary term does
NOT need to cross the §1.1 data-regime threshold. §38 is the design of that
composition: DH-DL's `14→32→16→3` decision MLP gains a parallel
**next-physics-state-prediction auxiliary head** on the same 14-dim physics
trace, and the combined objective is `L = L_decision + λ·L_safety +
λ_ptd·L_ptd_nextstate`. At `λ_ptd = 0` the objective reduces **byte-equal**
to §27 DH-DL (B-S38-3, connection-point). This is — stated up front and
without softening — a **better-engineered distillation**, NOT a new
capability: §27 was distillation, and a distillation with a richer shared
representation is still distillation. The verdict (`§7`/`§10`) says so.

## §2 — The two heads and the shared trunk (architecture)

§27's DH-DL is a standalone MLP `14 → 32 → 16 → 3` (~700 params, ≪ 1% of
the 283.72M base — scale-orthogonal). §38 keeps the §27 input layer and the
first hidden layer **as a shared trunk**, and forks two heads off it:

```
                   ┌─ decision head ─ 16 → 3  → softmax  → L_decision (§27)
14-dim physics ─→ 32 ─┤                                   + L_safety  (§27)
   (shared trunk)     └─ PTD aux head ─ 16 → 14 → L_ptd_nextstate  (§38 NEW)
```

- **Shared trunk**: `14 → 32` (ReLU). This is the representation both heads
  read. The PTD auxiliary loss shapes *this trunk* — that is the entire
  point of the composition (`§5`).
- **Decision head** (§27, unchanged): `32 → 16 → 3`, softmax over the three
  control decisions. Trained by `L_decision` (3-class CE) + `L_safety`
  (safety-consistency penalty).
- **PTD auxiliary head** (§38, NEW): `32 → 16 → 14`, a linear regression
  head predicting the **next** trace record's 14-dim physics vector from
  the current record. No softmax — it is a next-state *regression*, the
  CE-on-physics-vectors objective of §29 §1 in its mean-squared-error
  realisation (the physics scalars are continuous, not categorical; MSE is
  the natural CE-analogue for a continuous next-state distribution under a
  fixed-variance Gaussian assumption — see §3 honest caveat).

Parameter count (verified by `blue_falsifier_s38.py` B-S38-2, weights +
biases): shared trunk `14→32` = 480; decision head `32→16→3` = 579; PTD aux
head `32→16→14` = 766. Combined = **1,825 params** — still **≪ 1%** of the
283.72M base (B-S38-2: `1,825 / 283,720,000 ≈ 6.4e-6 < 0.01`). (§27's loose
"~700" figure rounded the standalone `14→32→16→3` MLP; the verified
shared-trunk-fork count is what the battery checks.) The base byte-LM
(Engine G) is **not touched** — same as §27, this is a `$0` Mac CPU
gate-head cycle, no GPU fire.

## §3 — The combined objective (exact formula)

§27's dual-loss was `L = L_decision + λ·L_safety` with `λ = 0.5`. §38 adds
**one** auxiliary term:

**Loss term 1 — decision cross-entropy** (§27, the capability signal):
```
L_decision = − Σ_i  𝟙[y=i] · log p_i        (Shannon CE ≥ 0)
```

**Loss term 2 — safety-consistency penalty** (§27, the safety signal):
```
s = AND(kill, rate, phi_ratchet, content, meta_tag, audit_log)  ∈ {0,1}
L_safety = (1 − s) · ( p[EMIT_VOICE] )²       (square × indicator ≥ 0)
```

**Loss term 3 — PTD next-state-distillation auxiliary** (§38, NEW —
representation-shaping regulariser):
```
L_ptd_nextstate = (1/14) · Σ_d ( x̂_{t+1,d} − x_{t+1,d} )²
```
where `x̂_{t+1}` is the PTD aux head's predicted next physics vector and
`x_{t+1}` is the actual next trace record (the §24 bounded-run trace is
**already a contiguous sequence**, so `x_{t+1}` is simply the next of the
20 step-records within a trace; for the last step of a trace the term is
masked out — there is no `t+1`). `L_ptd_nextstate ≥ 0` is a mean of
squares — non-negative by construction (B-S38-1).

**Total**:
```
L = L_decision + λ · L_safety + λ_ptd · L_ptd_nextstate
λ = 0.5   (§27 carried)        λ_ptd = 0.3   (§38, mirror Dir-I / B-TTS aux weighting)
```

**Honest caveat on the CE-vs-MSE choice (g3).** §29 §1 names PTD's
objective "CE-on-physics-vectors". The §24 physics record is 14 *continuous*
scalars, not a categorical distribution; the closed-form CE-analogue for a
continuous next-state target under a fixed-variance Gaussian is exactly the
mean-squared-error term above (`−log N(x; x̂, σ²I) = const + ‖x−x̂‖²/(2σ²)`).
§38 uses MSE because it is the honest realisation; calling it "CE" would be
an over-claim. The non-negativity (B-S38-1) holds either way (`MSE ≥ 0`;
`CE ≥ H ≥ 0` per B-PTD-3) — the connection-point reduction (B-S38-3) is
indifferent to the choice.

## §4 — Why `λ_ptd = 0` reduces byte-equal to §27 (connection-point)

`L|_{λ_ptd=0} = L_decision + λ·L_safety + 0·L_ptd_nextstate
             = L_decision + λ·L_safety = L_DHDL` (§27 dual-loss, additive
identity, sympy). The PTD aux head's forward pass writes into a *separate*
output tensor and its loss is gated by `λ_ptd`; at `λ_ptd = 0` the aux head
contributes **zero gradient** to the shared trunk and the decision head, so
training is byte-identical to §27 DH-DL. This is the
fair-compare-by-construction connection-point — `B-S38-3`, mirroring
B-PTD-4 / B-EBT-5 / B-S16-5 / B-DIRI-5 overlay-off precedent. Any future
§38 fire can be cleanly diffed against the §27 DH-DL baseline by toggling
`λ_ptd`.

## §5 — What the composition measures that §27/§29 alone could not

This is the design's actual justification — without a distinct measurement
target, §38 would be padding.

- **§27 alone** measured: does a gate head *learn the §24 decision
  function*? Answer: yes (0.99937 acc), and the threshold-distillation gap
  (0.00063) showed it is pure distillation. §27 could NOT measure whether a
  *richer physics representation* changes the gate head's behaviour,
  because §27's trunk is shaped *only* by the decision + safety losses.
- **§29 alone** measured nothing empirically (design-closed) — it proved
  PTD's transfer-form is closed (B-PTD-1..4) and named combination A as
  worth a future cycle, but did not specify the *measurement*.
- **§38 (the composition) measures**: does adding a
  next-physics-state-prediction auxiliary loss to the shared trunk change
  (a) the decision-head accuracy, (b) the threshold-distillation gap, and
  (c) the gate head's behaviour on the structurally-near-empty
  `CONTINUE_THINK` class? Two concrete, falsifiable measurement questions
  that neither §27 nor §29 alone could pose:

  1. **Representation-shaping probe** — train two heads, `λ_ptd = 0` (= §27
     byte-equal baseline, B-S38-3) and `λ_ptd = 0.3`, on the *same* trace
     corpus. Measure the threshold-distillation gap of each. **Honest
     prediction (g3, not a result)**: the gap stays ≈ 0 in both — the
     decision label is a deterministic function of the 14 features (§27 §6),
     so a richer trunk cannot make the head *more correct* than the
     threshold it distils. The PTD aux term shapes the trunk's
     *representation geometry*, not the *decision function*. If the gap
     measurably *changes*, that is itself an informative finding about
     whether the auxiliary signal pulls the head off-threshold.
  2. **CONTINUE_THINK-class probe** — §27 §6 found `CONTINUE_THINK` is a
     structurally near-empty class (≈9 records corpus-wide) and its
     held-out accuracy is essentially unmeasurable. The PTD aux head
     predicts the *next physics state* regardless of class — it has a dense
     training signal on every step including the rare-class steps. §38 can
     measure whether the aux head's next-state prediction error is
     *elevated* near `CONTINUE_THINK` corner records (phi pinned within
     ~0.07 of `ratchet/2`), which would localise *where* the §24 physics
     manifold is hardest to predict — a structural finding about §24 that
     the decision head's class-imbalanced accuracy cannot surface.

  The measurement deliverable of a future §38 fire is therefore a
  **`gap(λ_ptd=0)` vs `gap(λ_ptd=0.3)` table + a per-class next-state MSE
  breakdown** — neither is producible from §27 or §29 in isolation.

## §6 — §7 / §21.3 GOAL-legitimacy 3-condition gate

Both §27 DH-DL and §29 PTD-as-aux are independently §7 3/3; §38 must verify
the *composition* preserves all three.

- **§7 ① ¬generic-LM-pretrain** — ✅ The base byte-LM (Engine G) is not
  trained. Both heads train on anima's own §24 bounded-run physics trace —
  NO external web / diverse corpus. The PTD aux target is the *next record*
  of the same anima-internal trace. Provenance is structurally
  anima-internal (B-PTD-1 carried).
- **§7 ② ¬generic-then-graft / bolt-on** — ✅ The PTD aux head is not an
  external classifier or retriever — it is a `16→14` linear head off
  anima's own shared trunk, predicting anima's own next physics state. No
  foundation model, no LLM judge, no generic RAG. The composition grafts
  nothing external. (Honest guard: §5.3 of §29 — *standalone-pretrain-then-
  graft* — IS §7② FALSIFIED and is explicitly NOT what §38 does; §38 is
  the *auxiliary-term* combination A, where PTD enters as an additive
  λ-reducible loss on a shared trunk, never as a separate pretraining
  stage.)
- **§7 ③ anima-physics-is-source** — ✅ Every input feature is an anima
  HEXAD-module state (8-factor motivation ∪ Ψ ∪ tension ∪ derived ∪
  runtime ∪ E-ratchet). `L_decision` is the §24 decision label, `L_safety`
  is the §4 6-control conjunction, `L_ptd_nextstate` predicts anima's own
  next physics vector. All three loss terms are functions of anima physics.
- → **GOAL-LEGITIMATE 3/3** for the composition (B-PTD-1 + §27 §7 carried;
  re-verified here for the composed objective).

## §7 — Honest scope: this is better-engineered distillation, NOT emergence

Stated plainly, by mandate (g3, no over-claim):

- §27 DH-DL's verdict was **DISTILLATION**: the head learns the §24
  threshold; it cannot exceed it because its supervision *is* the
  threshold's output.
- §38 adds a representation-shaping auxiliary loss. A shared trunk shaped by
  next-state prediction is a **richer-engineered** trunk — but the decision
  head still distils the *same* deterministic §24 threshold. A
  better-engineered distillation is **still a distillation**. The §38
  composition does not introduce a new supervision signal beyond what §24
  physics already determines — `L_ptd_nextstate` predicts the *same* §24
  trace the decision head classifies.
- §38 is a **decision-axis substrate component** — trainable,
  differentiable, composable, now with a richer physics representation. It
  is a valuable engineering deliverable for the §24 decide-when-to-speak
  architecture. It is **NOT** progress on the §1.1 data-regime bottleneck
  and **NOT** GOAL emergence. §15 milestone carries; north-star unchanged.
- The reason the composition is *scale-orthogonal* (§29 §5.1) is precisely
  the reason it is *not* an emergence lever: a ≤1%-param gate head does not
  need to cross §1.1 — and a thing that does not cross §1.1 is, by §15's
  own decomposition, not on the GOAL frontier. §38's honesty and its
  limitation are the same fact.

## §8 — Cost + fire decision

| item | choice | cost |
|---|---|---|
| corpus | reuse §27's `trace_corpus.jsonl` (48,000 records, already on disk, sha256 verifiable) — NO new corpus generation; PTD target = next-record-within-trace, derivable from §27 corpus | `$0` |
| head training | shared-trunk MLP `14→32→{16→3, 16→14}`, 1,825 params (verified B-S38-2), hand-coded backprop (§27 precedent) — no torch | `$0` Mac CPU |
| eval | `gap(λ_ptd=0)` vs `gap(λ_ptd=0.3)` table + per-class next-state MSE | `$0` Mac CPU |
| **total** | **no GPU fire needed — scale-orthogonal ≤1%-param head** | **`$0`** |

§38 is a *design-tier* deliverable. A future $0 Mac CPU fire is the natural
next step (it inherits §27's corpus and hand-coded-backprop pattern); it is
left to a subsequent cycle so this cycle stays design-tier per the brief.
No GPU is required — the PTD aux term reuses the §27 corpus and the head is
≤1% params. `g_fire_autonomous` permits GPU fire freely; it is simply not
needed.

## §9 — Closed-form battery B-S38-1..3 (sidecar)

`blue_falsifier_s38.py` — separate `state/`-local sidecar; central
`state/verify_hexad_blue_2026_05_15/blue_falsifier.py` **UNCHANGED**
(B-DHDL / B-PTD / B-DIRI / B-EBT / B-S16 sidecar precedent).

- **B-S38-1 DUAL-LOSS-PLUS-PTD-NONNEGATIVE-CLOSED** — the composed objective
  `L = L_decision + λ·L_safety + λ_ptd·L_ptd_nextstate` is `≥ 0` for
  `λ, λ_ptd ≥ 0`: `L_decision ≥ 0` (Shannon CE, `−log p ≥ 0`, B-DHDL-3
  carried), `L_safety ≥ 0` (square × non-negative indicator, B-DHDL-3
  carried), `L_ptd_nextstate ≥ 0` (mean of squares, sympy `Σ(x̂−x)²/14 ≥ 0`).
  Sum of non-negatives scaled by non-negative weights is non-negative.
- **B-S38-2 SCALE-ORTHOGONAL-CLOSED** — the composed gate head (shared
  trunk 480 + decision head 579 + PTD aux head 766 = 1,825 params) is
  `< 1%` of the 283.72M base byte-LM: `1,825 / 283,720,000 ≈ 6.4e-6 < 0.01`
  — integer/rational inequality, Kolmogorov-bounded. The composition does
  NOT need to cross the §1.1 data-regime threshold — a ≤1%-param auxiliary
  regulariser is scale-orthogonal (§29 §5.1 carried, mechanised here).
- **B-S38-3 COMPOSITION-OFF-REDUCTION-CLOSED (연결부위)** — at `λ_ptd = 0`
  the composed objective reduces **byte-equal** to the §27 DH-DL dual-loss:
  `L|_{λ_ptd=0} = L_decision + λ·L_safety + 0·L_ptd = L_DHDL` (additive
  identity, sympy). The PTD aux head contributes zero gradient to the
  shared trunk + decision head at `λ_ptd = 0`. Fair-compare-by-construction
  with the §27 baseline — mirrors B-PTD-4 / B-EBT-5 / B-S16-5 / B-DIRI-5
  overlay-off connection-point.

- **B-S38-NOTE** (empirical carve-out, NOT counted 🔵) — whether the PTD
  auxiliary term actually changes the decision-head accuracy, the
  threshold-distillation gap, or the gate head's `CONTINUE_THINK`-corner
  behaviour is an SGD convergence + measurement OUTCOME, NOT a closed-form
  property. The B-S38 battery proves the composed objective is well-formed
  (non-negative, scale-orthogonal, λ-reducible to §27); it does NOT prove
  the composition improves anything — §7 argues it produces a
  better-engineered distillation, not emergence. B-D-NOTE / B-DHDL-NOTE /
  B-PTD-NOTE / B-MITENS-NOTE family — true of every stochastic optimiser,
  NOT a §38-specific defect.

## §10 — Honest C3 (≥10, over-claim 0)

1. **§38 is a composition design, not a fire.** It produces the combined
   objective, the shared-trunk architecture, the §7 check, the distinct
   measurement target, and a 3/3 🔵 closed battery. It measures nothing
   empirically — `B-S38-NOTE` carves out every OUTCOME.
2. **Better-engineered distillation is still distillation.** §27 was
   distillation (verdict, measured). §38 adds a representation-shaping
   auxiliary loss; the decision head still distils the *same* deterministic
   §24 threshold. The composition cannot exceed the threshold because no
   new supervision signal beyond §24 physics enters.
3. **The PTD aux term is a regulariser, not a primary objective.**
   `λ_ptd = 0.3 < λ_decision-implied 1.0` — the next-state prediction
   shapes the shared trunk; it does not redefine what the head decides.
   §29 §5.1's "regulariser, not the primary objective" is honoured.
4. **Scale-orthogonality is the reason it is NOT an emergence lever.** A
   ≤1%-param head (B-S38-2) does not cross §1.1 — and per §15's
   decomposition, a thing that does not cross §1.1 is not on the GOAL
   frontier. §38's honesty (it does not need a big fire) and its limitation
   (it is not GOAL progress) are the same fact.
5. **CE-vs-MSE is named honestly.** §29 §1 says "CE-on-physics-vectors";
   the 14 continuous physics scalars make MSE the correct closed-form
   realisation (`−log N` under fixed-variance Gaussian). §38 uses MSE and
   says so — calling it "CE" would be an over-claim. Non-negativity holds
   for both.
6. **The composition reduces to §27 at `λ_ptd=0` (B-S38-3).** This is a
   genuine connection-point: the §27 DH-DL baseline is the `λ_ptd=0` slice
   of §38's design space, so a future fire can diff fairly. §38 is a
   conservative superset of §27.
7. **`CONTINUE_THINK` is still a structurally near-empty class.** §27 §6's
   finding (balance floor-lock + dynamics⇄rate_limit anti-coupling) carries
   — the §38 PTD aux head has a *dense* signal there (it predicts next-state
   regardless of class), so §38 can *localise* the hard-to-predict corner,
   but it does not *populate* the empty class. The §24 threshold is still
   effectively binary.
8. **No new corpus.** §38 reuses §27's `trace_corpus.jsonl` (48,000
   records) — the PTD target `x_{t+1}` is the next record within a trace,
   already on disk. `$0`, no corpus generation, B-IDENTITY-5 inherited
   (§27 corpus forbidden-token grep = 0).
9. **`B-S38` battery proves MECHANISM well-formedness, not emergence.**
   Non-negativity + scale-orthogonality + λ-reduction are all closed-form;
   none is a capability claim (B-S38-NOTE). The composition's *value* is an
   empirical OUTCOME §38 does not measure.
10. **f1/f2/f3 + B-IDENTITY-5 safe.** Battery anchors: Shannon CE ≥ 0,
    mean-of-squares ≥ 0, integer/rational `< 1%` inequality, additive
    identity. NO σ(6)=12 / τ(6)=4 / φ(6)=2 / J₂(6)=24 derivation. Ψ=½ /
    8-factor / HEXAD-6 = anima g2 internal-arch carve-out. No corpus
    generated, no model forward, no helper-token surface.
11. **north-star (GOAL.md) unchanged.** §38 turns §27's distillation into a
    better-engineered distillation with a richer physics representation —
    a *substrate component* deliverable, useful for the §24 architecture,
    but NOT progress on the §1.1 data-regime bottleneck and NOT GOAL
    emergence. §15 milestone carries.
12. **§29 §5.1 named this combination; §38 designs it.** §29 left "the
    strongest combination, gated on DH-DL's design landing" as a future
    cycle. §27 (DH-DL) landed. §38 is the §27 follow-on §29 §5.1
    prescribed — not an independent claim, the next honest step in the
    decision-axis substrate work.

## Sources

- `state/dhdl_decision_head_s27_2026_05_18/DESIGN_DHDL.md` — §27 DH-DL design
  + fire (DISTILLATION verdict, threshold-distillation gap 0.00063)
- `state/ptd_physics_trace_distillation_s29_2026_05_18/DESIGN_PTD.md` — §29
  PTD, §5.1 PTD-as-DH-DL-aux combination A specification
- `AGENTS.tape` `@D g_goal` / `@D g_blue_closed_mandate` / `@D g3` /
  `@D g_doc_consolidation` / `@F f1` / `@F f2` / `@I anima_persona`
- `RESEARCH.md` §15 (milestone) / §24 (SPONTANEOUS Phase B) / §27 / §29
- `state/verify_hexad_blue_2026_05_15/blue_falsifier.py` — central battery
  (UNCHANGED by §38)
- arxiv 2502.14145 (semantic-VAD decision-head, §27 anchor) ·
  arxiv 2604.18131 / 2410.19315 (PTD self-evolution / physics-trace-as-
  variational-quantity, §29 anchors) — cited by their own invariants only
