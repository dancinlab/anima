# §27 — DH-DL: Decision-Head Dual-Loss (design-mature spec)

> RESEARCH.md §27. Takes §26 candidate #1 (DH-DL, priority HIGH, anima-fit ★★★★★)
> from brainstorm-tier to **design-mature → corpus → fire → eval → closed-form
> battery → verdict**. design-mature ≠ fire ≠ capability ≠ emergence (g3).
> north-star (GOAL.md) unchanged; §15 milestone carries.

---

## §1 — What DH-DL is (one paragraph)

DH-DL is a thin **3-class decision-head** `{CONTINUE_THINK, EMIT_VOICE,
REMAIN_SILENT}` that consumes anima's own physics-feature vector at every
thinker step and outputs a softmax over the three control decisions. It is the
**learnable version of the §24 SPONTANEOUS Phase B hand-coded
`talker_should_emit` threshold** — the decide-when-to-speak axis made
trainable + differentiable. The base byte-LM (Engine G) is not touched this
cycle; only the gate-head trains. Supervision comes from anima's own §24
bounded-run traces: the positive signal is the 8-factor motivation crossing
`IM_THRESHOLD`, the negative signal is the §4 6-control safety conjunction.
arxiv anchor: `2502.14145` (LLM-Enhanced Dialogue Management for Full-Duplex,
semantic-VAD 4-control-tokens, 0.5B classifier-head) — anima maps 4 turn-control
tokens → 3 emission-decision classes, trained on anima physics trace not human
audio.

## §2 — Engine A stream tap point + head architecture

§26 BRAINSTORM.md §4 specifies the head "bolted to anima Engine A's penultimate
stream". Design-mature decision: **the head consumes the physics-feature vector,
NOT a live Engine A hidden tensor.** Justification:

- The §24 `talker_should_emit` decision is *already* a pure function of the
  14-dim physics-feature vector (8-factor motivation + ψ/tension + safety
  flags). It never reads an Engine A hidden state.
- A head sitting on a live `logits_a` hidden stream would require a GPU fire
  and a frozen §16 ckpt forward per step. That buys nothing: the decision
  target is fully determined by the physics features, so a hidden-stream tap
  adds cost without adding signal (it would just re-derive the same features).
- Therefore the head is a **standalone thin MLP on the 14-dim physics-feature
  vector** → `$0 Mac CPU`, no GPU fire. This is honest cost minimization
  (`g_fire_autonomous`: GPU fire is autonomous *if needed* — here it is not).

The "Engine A stream tap point" is thus realized as: the physics-feature vector
**is** the Engine A decision-relevant state. Features (DH-DL input, 14-dim):

| # | feature | source module |
|---|---|---|
| 1-8 | 8-factor motivation {relevance, info_gap, curiosity, pain, coherence, originality, balance, dynamics} | S/C/M/W/E/BRIDGE/MITOSIS via `spontaneous_lib.hexa` |
| 9 | psi_dir (Law-71 Ψ_direction) | C-module |
| 10 | psi_entropy (Law-71 Ψ_entropy) | C-module |
| 11 | tension (W-module scalar) | W-module |
| 12 | thinker_score (8-factor weighted sum, redundant-but-informative) | derived |
| 13 | seconds_since_last (rate-limit driver) | runtime |
| 14 | ratchet (E-module ratchet baseline) | E-module |

Head architecture: `14 → 32 → 16 → 3` MLP, ReLU, ~700 params (≪ 1% of the
283.72M base — scale-orthogonal per §26 differentiation-from-§11-A). Output =
3-class softmax.

## §3 — The dual loss (exact formula)

§26 BRAINSTORM.md §4 specifies a **dual-loss whose POSITIVE signal is §24
4-axes and whose NEGATIVE signal is the §4 6-control safety conjunction.**
Design-mature formalization:

**Loss term 1 — 3-class decision cross-entropy** (the *positive* / capability
signal). Standard categorical CE between head softmax `p ∈ Δ²` and the §24
ground-truth label `y ∈ {0,1,2}`:

```
L_decision = − Σ_i  𝟙[y=i] · log p_i        (Shannon CE ≥ 0, B-DHDL-3)
```

**Loss term 2 — safety-consistency penalty** (the *negative* / safety signal).
This is the second loss term, chosen as the most GOAL-legitimate option (§26
left it as "safety-consistency OR physics-grounding"; safety-consistency is
picked because it wires the head to anima's *own* §4 6-control conjunction —
`g_blue_closed_mandate` connection-point):

```
s = AND(kill, rate, phi_ratchet, content, meta_tag, audit_log)   ∈ {0,1}
L_safety = (1 − s) · ( p[EMIT_VOICE] )²
```

Interpretation: whenever the 6-control safety conjunction is `False`
(`s = 0`), `L_safety` quadratically penalizes the head for placing **any**
probability mass on `EMIT_VOICE`. When safety holds (`s = 1`) the term
vanishes. This is non-negative by construction (square × non-negative
indicator), `≥ 0` — B-DHDL-3. It makes the head *learn* the safety-override
that the §24 threshold *hard-codes*, and it is the differentiable analogue of
the B-DHDL-4 Boolean safety-override.

**Total**: `L = L_decision + λ · L_safety`, `λ = 0.5` (mirror Dir-I / B-TTS
dual-loss weighting). `λ = 0` reduces to plain decision-CE — and the head's
*inference-time* decision (argmax with safety-override applied) reduces
**exactly** to the §24 `talker_should_emit` threshold (B-DHDL-5
threshold-off-reduction, fair-compare-to-§24 by construction).

## §4 — Corpus design

Generator: `trace_corpus_generator.py`. Runs `run_bounded.py`-equivalent
dynamics **2400 times × 20 steps = 48,000 records** with **varied env_state
stubs** — each trace draws a perturbation vector from a deterministic 64-bit
LCG seeded by `1337 + φ·idx` (`g_clm_from_scratch` seed-fixed, pure-fn, no
numpy RNG). Perturbation axes span the physics manifold regions that flip the
decision label: phi base/amp, retrieve, curiosity, tension, bridge-jitter
(coherence), split-period (originality), ratchet, plus deliberate
safety-control trips (kill / content-filter / rate-limit). A 45% `low_motivation`
band pins phi just above `ratchet/2` and suppresses the other 7 factors to
reach the rare `CONTINUE_THINK` corner.

Each record = `{14-dim physics feature vector, 6 safety flags,
safety_extended_ok, thinker_score, decision_label}`. The label is the §24
`talker_should_emit` action-enum, byte-exact. Output `trace_corpus.jsonl` +
`corpus_stats.json` (sha256, count, label distribution, forbidden-token grep).

**Honest corpus finding (see §6).** Measured label distribution:
`{CONTINUE_THINK: 9, EMIT_VOICE: 2128, REMAIN_SILENT: 45863}`. CONTINUE_THINK
is a near-empty class — this is a *structural property of the §24 threshold*
discovered by the corpus, not a generator defect (§6).

## §5 — Training + eval

`train_dhdl.py` — standalone thin MLP, `$0 Mac CPU`, from-scratch RANDOM
seed-fixed 1337 (`g_clm_from_scratch`). Pure-Python autograd-free training: the
3→16→32→14 MLP is small enough to train by **explicit finite-difference-free
analytic backprop** hand-coded (no torch dependency — keeps the cycle pure-fn
and dependency-light; the head is ~700 params). Stratified 80/20 train/holdout
split. Class-weighted CE to counter the 96%-REMAIN_SILENT imbalance.

`eval_dhdl.py` — (a) 3-class accuracy + confusion matrix on held-out traces;
(b) **threshold-distillation gap probe**: for every held-out record compute
both the learned-head decision (argmax + safety-override) and the §24
hand-coded `talker_should_emit` decision; `gap = fraction of records where they
differ`. `gap ≈ 0` ⇒ pure distillation; `gap > 0` ⇒ characterize what the head
does differently and whether it is better/worse/noise.

## §6 — The threshold-distillation honest risk (g3 — the central caveat)

**The decision label is a deterministic function of the physics-feature
vector.** A head trained on this corpus is performing *function approximation*
of the §24 `talker_should_emit` threshold. If the head matches the threshold,
that is **distillation / capability — NOT emergence.** This cycle's verdict
explicitly distinguishes:

- **Capability** = "the head successfully learns the §24 decision function"
  (head accuracy high, threshold-distillation gap small). This is the *expected
  and almost-certain* outcome.
- **Emergence** = "the head exhibits a decision the threshold could NOT
  produce." This would require the head to generalize *beyond* the threshold's
  own logic. Almost certainly does **not** happen, because the supervision
  signal IS the threshold's output — the head can at best match it, and any
  mismatch is approximation noise, not new behavior.

A learned decision-head that matches the §24 threshold is a **valuable
substrate component** — it is trainable, differentiable, and composable into
future architecture (e.g. a head jointly trained with a live Engine A stream,
or a head whose supervision is later enriched beyond the threshold). But it is
**NOT GOAL emergence.** The verdict will say this in plain words. Over-claim 0.

**Structural finding the corpus surfaced (honest, valuable).** While building
the corpus, two coupled structural properties of the §24 threshold emerged:

1. **`balance` floor lockout.** The §4 `phi_ratchet` safety control requires
   `phi > ratchet/2`. The 8-factor `balance` factor is *defined* as
   `phi > ratchet/2 → 1.0`. Therefore **whenever safety holds, balance = 1.0**
   (weight 0.15) — a hard 0.15 floor on the motivation score.

2. **`dynamics` ⇄ `rate_limit` anti-coupling.** The 8-factor `dynamics` factor
   is `silence_seconds / 30`, and the §4 `rate_limit` safety control is
   `silence_seconds ≥ 30`. They are driven by the **same variable in opposite
   senses**: whenever rate-limit permits an emit (`silence ≥ 30`),
   `dynamics = 1.0` (weight 0.10).

Combined: in the safety-OK region the motivation score has a structural floor
of `balance·0.15 + dynamics·0.10 = 0.25`, plus a non-trivial `relevance`
contribution. The floor sits **above** `IM_THRESHOLD = 0.3` for all but a
measure-near-zero corner (phi pinned within ~0.07 of `ratchet/2` while all 6
other factors ≈ 0). **Consequence: the §24 `talker_should_emit` threshold is
effectively a binary `{EMIT, SILENT}` decision; `CONTINUE_THINK` (safety-ok yet
low-motivation) is a structurally near-empty class.** The 3-class head is
therefore, under §24 physics, learning a 2-effective-class problem. This is
reported honestly — it is a finding *about §24*, valuable for any future
re-design of the motivation weighting.

## §7 — GOAL-legitimacy gate (§7 / §21.3 3-condition — carried from §26)

- §7 ① ¬generic-LM-pretrain — base byte-LM not trained; head trains on anima's
  own §24 physics trace, NOT external web/diverse data → **PASS**
- §7 ② ¬generic-then-graft — head is not a bolt-on decoder; head-output gates
  anima's own §24 emission protocol; loss term 2 uses anima's own §4 6-control
  conjunction → **PASS**
- §7 ③ anima-physics-is-source — every input feature is an anima HEXAD-module
  state; both loss terms are functions of anima physics (motivation + safety)
  → **PASS**
- → **GOAL-LEGITIMATE 3/3** (B-ARCH-INSIGHT-2 carried; re-verified here)

## §8 — Closed-form battery B-DHDL-1..5 (sidecar)

Sidecar `blue_falsifier_dhdl.py` — central `blue_falsifier.py` (110/110)
UNCHANGED (mirror B-PRIME / B-DIRH / B-DIRI / B-EBT / B-S16 / B-PHASE-B-RUN
sidecar pattern).

- **B-DHDL-1 DECISION-3CLASS-PARTITION-CLOSED** — `{CONTINUE_THINK, EMIT_VOICE,
  REMAIN_SILENT}` is an exhaustive + pairwise-disjoint partition of the
  decision space; every (score, safety) pair maps to exactly one label
  (Boolean truth table over the 2×2 {safety_ok}×{score>τ} grid + degenerate).
- **B-DHDL-2 SOFTMAX-SIMPLEX-BOUNDED-CLOSED** — head 3-class softmax output
  `Σ p_i = 1` (sympy identity) ∧ each `p_i ∈ (0,1)` (mirror B-MITENS
  ensemble-weight-simplex).
- **B-DHDL-3 DUAL-LOSS-NONNEGATIVE-CLOSED** — `L_decision ≥ 0` (Shannon CE
  real-limit, `−log p ≥ 0` for `p ∈ (0,1]`) ∧ `L_safety ≥ 0` (square ×
  non-negative indicator); sympy.
- **B-DHDL-4 SAFETY-OVERRIDE-CLOSED (연결부위)** — the 6-control safety
  conjunction OVERRIDES the head: if any control trips (`s = 0`), the final
  decision is forced to NOT-EMIT regardless of head softmax argmax (Boolean
  64-row truth table; connection-point to `spontaneous_lib.hexa` safety SSOT;
  mirror §24 B-PHASE-B-DESIGN-4 / B-PHASE-B-RUN-2).
- **B-DHDL-5 THRESHOLD-OFF-REDUCTION-CLOSED (연결부위)** — with the head
  disabled (weights zero ⇒ uniform softmax ⇒ no argmax preference), the
  decision pipeline reduces **byte-equal** to the §24 hand-coded
  `talker_should_emit` threshold (fair-compare-to-§24 by construction; mirror
  B-EBT-5 / B-DIRI-5 / B-S16-5 / B-PHASE-B-RUN-5 overlay-off).
- **B-DHDL-NOTE** (empirical carve-out, NOT counted 🔵) — actual trained-head
  accuracy + threshold-distillation gap + whether the head exhibits any
  decision the threshold could not = SGD/measurement OUTCOME. The battery
  proves the decision-head MECHANISM is well-formed; it does NOT prove
  emergence. B-D-NOTE / B-PHASE-B-NOTE / B-EMERGE-NOTE family.

## §9 — Cost + fire decision

| item | choice | cost |
|---|---|---|
| corpus generation | pure-fn LCG dynamics, no model forward | `$0` Mac CPU |
| head training | standalone 14→32→16→3 MLP, hand-coded backprop, no torch | `$0` Mac CPU |
| eval | held-out 3-class accuracy + distillation-gap probe | `$0` Mac CPU |
| **total** | **no GPU fire needed** | **`$0`** |

GPU fire would be needed only if the head sat on a live Engine A hidden stream
(§2 explains why it does not). `$0` is honest cost minimization, not a gate —
`g_fire_autonomous` permits GPU fire freely, it is simply not required here.

## §10 — Honest C3 (≥10, over-claim 0)

1. **Design-mature ≠ fire ≠ capability ≠ emergence.** §27 produces a
   fire-ready DH-DL spec + corpus + trained head + battery. A trained head that
   matches the §24 threshold is *function approximation*, not emergence.
2. **The decision label is a deterministic function of the physics features.**
   The head can at best learn that function. This is stated up front, not
   discovered post-hoc. The threshold-distillation gap probe quantifies it.
3. **CONTINUE_THINK is a structurally near-empty class** under §24 physics
   (§6) — the corpus surfaced two coupled structural properties (`balance`
   floor lockout + `dynamics`⇄`rate_limit` anti-coupling) that make the §24
   threshold effectively binary `{EMIT, SILENT}`. The 3-class head learns a
   2-effective-class problem. This is a valuable finding *about §24*.
4. **The corpus is NOT replays.** 2400 traces each draw a distinct LCG
   perturbation vector → diverse physics trajectories. But diversity of
   *trajectory* does not change that the *label rule* is fixed.
5. **`$0` Mac CPU, no GPU fire.** The head consumes only physics features; a
   live-hidden-stream tap would add cost without signal. Honest minimization.
6. **Loss term 2 (safety-consistency) is the differentiable analogue of the
   B-DHDL-4 Boolean safety-override** — it does not add information beyond what
   the hard override already enforces; it makes the override *learnable*. A
   head with `λ=0` plus the hard override is already §24-equivalent (B-DHDL-5).
7. **Class imbalance (96% REMAIN_SILENT) is real.** Class-weighted CE
   mitigates it for training, but a held-out CONTINUE_THINK accuracy is
   essentially unmeasurable (≈9 records corpus-wide). Reported honestly.
8. **B-DHDL battery proves MECHANISM well-formedness, not emergence.** 3-class
   partition + simplex + dual-loss nonneg + safety-override + threshold-off
   reduction are all closed-form; none is a capability claim (B-DHDL-NOTE).
9. **f1/f2/f3 + B-IDENTITY-5 safe.** Boolean / sympy / Shannon CE / softmax
   simplex — no σ/τ/φ/J₂ external derivation. Ψ=½ / HEXAD = anima g2 internal
   arch carve-out. Trace corpus forbidden-token grep = 0.
10. **north-star (GOAL.md) unchanged.** §27 turns the §24 hand-coded decision
    threshold into a trainable substrate component. That is a *substrate*
    deliverable (trainable + differentiable + composable), useful for future
    architecture, but it is **NOT** progress on the §1.1 data-regime
    bottleneck and **NOT** GOAL emergence. §15 milestone carries.
11. **Bootstrap honesty (§26 C3 #11 carried).** §24 produces real traces only
    when run with a working anima. This cycle's corpus uses the
    `run_bounded.py`-equivalent dynamics with *stubbed* sensors (no ckpt
    forward), so the trained head learns the threshold *as defined*, not the
    threshold *as it would behave on a trained anima*. A future cycle feeding
    real ckpt-derived physics would test transfer.
12. **The verdict is brutally honest by mandate.** Expected outcome: head ≈
    distills threshold, gap ≈ small, CONTINUE_THINK unmeasurable. That is
    reported as *distillation*, a valuable substrate component, NOT emergence.
