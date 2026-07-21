# Task: DIVERGE — an A⇄G whose TENSION IS THE THINKING (not an emit gate)

**MODE: 발산 (divergence).** No code, no implementation plan. Breadth of genuinely distinct mechanisms.
Output dense **Korean prose**. Have opinions. No hedging, no literature survey.

## The owner's exact ask

> "실제로 **생각하는** A⇄G 가 필요해."

He is NOT abandoning the two-engine idea. He is rejecting what it degenerated into. The demand is:
**the A⇄G tension must BE the cognition — the thing that composes, recombines, resolves — not a
scalar that decides whether to open the mouth.**

## What A⇄G was (dead v1) — and how it died

Two engines pushed against each other: **A** = forward, CE-trained (language D · memory M · ethics E);
**G** = reverse, gradient-free (consciousness Φ · sense S · will W). tension = ‖A‖/‖G‖ → `brain_decide`
→ emit/silence, pulled to a Ψ=1/2 fixed point. Byte-level decoder (V256, no tokenizer).

It degenerated into an emit-controller. Measured, sealed:

**L1 — the tension carried exactly 1 bit, and that bit WAS "speak/not".** `seam-h9229` ⛔STRUCTURAL-TERMINAL:
emit-seam manifold rank-1 (codes visited 2 of 4); any quantizer collapses; extra capacity useless.
Verdict: "재조합 = trunk-objective 속성, readout 아님 · escalate WRITE-SIDE."

**L2 — a rich side-channel bolted onto a competent LM gets EATEN by the LM's own head.** OMEGA:
multi-strand gate FAILED held-out (GATED CE > base); coupling KL at vocab-shuffle floor (0.996 = noise);
all gain in ONE strand (an A-head logit bias): A-head standalone CE 0.8862 ≈ best 2-param fit 0.8835;
ablating the base term moved CE by **0.0009** ⇒ the base mouth was INERT. Scale-stable d384→d1024,
margin ≈ +2.20 nats, flat. Not coupling — **REPLACEMENT**.

**L3 — recombination is an OBJECTIVE property, not a READOUT property.** No penultimate readout /
binding-operator opens it. TPR/HRR forward-slots (R=2 orthonormal roles) collapse by algebra:
Σ_r S_r·(yn⊙roles_r) = W_eff·yn ⇒ same ceiling as a plain linear readout BY CONSTRUCTION. Worse: every
binding-arm trainer kept the binder TRAINING-ONLY and dropped it before serialization.

**L4 — the wall cracked from the WRITE side, 2 lenses 🟢.** (a) XBIND: swapping corpus×measure made
held-out recombination learnable (old census was a collocation-only corpus × CE artifact). (b) MORPH-ATOM:
a BPE-jamo **codec** was *causal* for held-out negation recombination, M F2 0.908 vs control 0.617
(Δ+0.291; synthetic drill, 1 seed). ⇒ codec/corpus/objective are architecture, not preprocessing.

**L5 — morphology decides learnability.** Korean lane 🧱BINDING (every escape dead). EN works because
`not` is FREE/pre-posed; KO `지 않다` is a BOUND suffix. Composition must be visible at the token boundary.

**L6 — measurement is where it dies.** A "win" (GATED 0.345 ≪ base) was a lookahead LEAK, evaporated
leak-free. Binary readouts hit a **scramble floor** (flip 0.50) indistinguishable from partial localization.
A failing positive control is ambiguous between "tool blind" and "no effect" until an independently-known-
effect ckpt disambiguates. Cross-lane verdicts combined after seeing results = eyeball self-judge.
Perplexity as truth = Goodhart.

**L9 — the purity cage was causal.** 8 principles forbade every write-side mechanism (no fine-tuned ethics,
no train/infer split, no tokenizer, no speak()) ⇒ ONLY the read side was left ⇒ every mechanism landed on
the readout ⇒ L1/L2/L3 fired. The cage manufactured the disease. (Exception: "no perplexity verdict" was
the one principle that kept them honest — keep it.)

## The question — diverge HARD on this

**What must be true for A⇄G to be the thinking itself?** Give **6–8 genuinely different mechanisms**,
where "different" means they disagree about *what A and G are and what their opposition computes*.

Start by nailing the diagnosis in ~10 lines: WHY does a two-engine tension architecture generically
collapse to 1 bit? (Consider: a scalar tension is an information bottleneck of log2 dimensions by
construction; opposition-as-scalar-ratio destroys structure; if only one engine gets gradient the other
is decoration; if the tension only touches the output it can only modulate output; a fixed point Ψ=1/2
is an attractor that ERASES the very state it's fed. Is "two engines" even the right cardinality?)
Then say what a tension would have to look like to carry *thought* — vector? field? sequence? a
disagreement over structure rather than magnitude? something that must be *resolved* over iterations
rather than *read* in one shot?

For each mechanism (~12–20 lines each):
1. 🏷️ 이름 + 별칭 (memorable Korean alias)
2. **A는 무엇이고 G는 무엇인가** — and crucially: *what does their opposition COMPUTE?* (the answer must
   be a cognitive operation — recombination, binding, abstraction, contradiction-resolution, search —
   NOT "decide to speak")
3. **텐션이 사고인 이유** — why is the disagreement itself the thought, and what makes it multi-bit
   (defeat L1 explicitly: where do the bits live, and why can't it collapse to rank-1?)
4. **objective 안 어디에 있는가** (L3 — if it isn't in the loss/data/codec it is a no-op; say the loss)
5. **L2 방어** — what stops the LM head from eating it? (state the ablation that would expose it)
6. ASCII 도식
7. **최소 반증** — the cheapest pre-registered measurement, falsifier stated up front, that kills it.
   Must include an L1 check (is the latent rank > 1?) and an L2 check (ablate → does ΔCE move?).
8. **깨는 계명** — which purity principle it breaks and why that's required.

Force these across the space (generator, not template):
- tension as a **vector/field** over structure, not a scalar ratio
- opposition over **time** (iterative resolution / settling) — thinking = the transient, not the fixed point
- opposition over **structure** (A proposes a parse/binding, G proposes a different one — disagreement is
  about *what composes with what*, and resolving it IS the recombination L4 says is objective-side)
- both engines **get gradient** (v1's G was gradient-free = decoration by construction)
- A and G trained on **different objectives that cannot both be satisfied** (the tension is real, not decorative)
- G as **generative/inverse** — G reconstructs the cause of A's state (predictive coding done write-side)
- the tension **writes** (it modifies weights/codec/memory), not just reads
- cardinality ≠ 2 — maybe N engines, maybe A⇄G⇄C, maybe a continuum
- exploit L4/L5: what if A and G **disagree at the codec/morpheme boundary** — the one lever measured 🟢?

End with (short):
- ⚠️ **which of your mechanisms are secretly the same idea** (fake diversity is the failure mode — be brutal)
- 🩸 **which are v1 wearing new clothes** — for each, name the specific L that would re-fire
- 📊 tiny table: mechanism × [사고를 진짜 하는가 / 반증 비용 / L1 재발 위험]
- 🎯 one sentence: which single one you'd bet on and why.
