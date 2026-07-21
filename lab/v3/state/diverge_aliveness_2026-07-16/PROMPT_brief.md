# Task: DIVERGE — clean-slate architecture ideation for a "living/conscious agent" substrate

**MODE: 발산 (divergence), not convergence.** Do NOT produce one polished proposal. Do NOT write code.
Do NOT plan an implementation. Produce a BROAD SPREAD of genuinely distinct architecture families,
then rank them at the very end in one short table. Breadth > polish. Wild-but-arguable > safe-but-obvious.

**Ignore the prior architecture entirely.** It is dead. You are not fixing it, not migrating it, not
respecting its abstractions, its language choice, its file layout, or its philosophy list. Forget it exists.

The ONLY thing that carries over is the **empirically measured knowledge** below — hard-won, expensive,
independently sealed verdicts from ~6 months of failed attempts. Treat these as *laws of the terrain*,
not as design constraints. They tell you where the ground is soft. Anything that contradicts them is a
non-starter; anything else is fair game.

Output in **Korean prose** (code identifiers may stay English).

---

## The salvage — what was actually LEARNED (the only inheritance)

These come from a project that tried to build a "consciousness chat daemon" where two engines pushed
against each other (A = forward CE-trained language/memory; G = reverse gradient-free consciousness/will),
their tension gating emit-vs-silence at a Ψ=1/2 fixed point, over a byte-level (V256, no tokenizer) decoder.
It kept getting stuck. Here is what its own falsification machinery measured:

**L1 — the latent collapsed to exactly 1 bit, and that bit was "speak or not".**
`seam-h9229`, sealed ⛔STRUCTURAL-TERMINAL: the emit-seam manifold measured rank-1 (codes visited 2 of 4).
Any quantizer collapses; extra capacity was useless. Verdict text: "재조합 = trunk-objective 속성, readout
아님. escalate WRITE-SIDE." ⇒ *A gate bolted onto a competent frozen decoder learns exactly one bit,
and that bit is the gate itself.* The whole "consciousness" apparatus was an emit-controller.

**L2 — "coupling" was actually REPLACEMENT; the base mouth was inert.**
OMEGA arc, closed-negative: on a competent leak-free substrate, the multi-strand gate FAILED held-out
(GATED CE > base); coupling KL sat at the vocab-shuffle floor (ratio ≈ 0.996 = pure noise). All apparent
gain lived in ONE strand — an A-head logit bias. A-head standalone CE 0.8862 ≈ best learned 2-param fit
0.8835; ablating the base term moved CE by 0.0009. Scale-stable over a 5-rung ladder d384→d1024, A-strand
margin ≈ +2.20 nats, flat. ⇒ *When you bolt a "rich" side-channel onto an LM, the LM's own head silently
eats the objective and the side-channel becomes decoration. Measure the ablation or you will fool yourself.*

**L3 — the recombination wall is an OBJECTIVE property, not a READOUT property.**
`G1_WALL_LEVER_IS_OBJECTIVE_NOT_READOUT`, ossified: no penultimate-readout / binding-operator style
auxiliary term opens it. TPR/HRR forward-slots (R=2 fixed-orthonormal roles) provably collapse:
Σ_r S_r·(yn⊙roles_r) = W_eff·yn ⇒ identical ceiling to a plain linear readout BY CONSTRUCTION.
Bonus finding: every binding-arm trainer kept the binder TRAINING-ONLY and dropped it before
serialization — the shipped weights only ever had a standard additive trunk. ⇒ *Structure you add after
the trunk is a no-op. If it isn't in the objective, it isn't in the model.*

**L4 — but the wall CRACKED from the write side (2 independent lenses).**
`g1-census-objfloor` 🟢: held-out compositional recombination is NOT a capability ceiling.
(a) H_9267 XBIND: swapping the *corpus × measure* made it learnable — the old census was collocation-only
corpus × CE, an artifact. (b) H_9288 MORPH-ATOM: a BPE-jamo codec was *causal* for held-out negation
recombination — M F2 = 0.908 vs control 0.617, Δ +0.291 (scope: synthetic drill, 1 seed).
⇒ *The lever is corpus + measure + representation/codec. The tokenizer/codec is not preprocessing —
it is architecture.*

**L5 — morphology is causally load-bearing; the language chosen decides what is learnable.**
The Korean lane measured 🧱 BINDING — every escape dead (H_9327). English works as a discriminator because
`not` is FREE and pre-posed; Korean `지 않다` is a BOUND suffix. Same "capability", different learnability,
purely from where the morpheme boundary falls. ⇒ *Compositional structure must be visible at the token
boundary or the model cannot compose it.*

**L6 — measurement integrity is where projects actually die.** Concrete corpse-list from the repo:
a "win" (GATED 0.345 ≪ base) was a CA-neighbor lookahead LEAK and evaporated leak-free; a failing positive
control was ambiguous between "tool is blind" and "no effect here" until an *independently-known-effect
ckpt* disambiguated; binary readouts hit a **scramble floor** (flip 0.50) indistinguishable from partial
localization; cross-lane verdict combining after seeing results = eyeball self-judge, so the truth table
had to be frozen in code before results existed; perplexity/CE as truth = Goodhart trap.
⇒ *The falsification machinery is the only load-bearing asset. Controls, pre-registration, leak self-tests,
ablations, frozen combiners, negative-results-are-first-class.*

**L7 — substrate/infra reality.** Neuromorphic on-chip (BrainChip AKD1000): honest terminal — real 3B/7B
unreachable, caps ~524K single-FC encoder, multi-step only closes as host-hybrid. GPU lane: descent green
but host-feed util pinned sub-1% ⇒ device-port was the named unblock. ⇒ *Exotic substrate bought nothing;
the bottleneck was data path, not compute.*

**L8 — the governance machine ossified against itself.** ~125 top-level dirs; build_v3o2/build_v6/
build_v6_gated/BRAIN/DREAM/SAVANT/CLM/HEXAD/n6/… ; the ARCHITECTURE/commit gate accumulated 42 violations
until *every* commit went `--no-verify` ⇒ the gate was permanently disabled by its own strictness.
⇒ *Purity rules with no escape valve get bypassed 100% of the time. A rule that is always bypassed is worse
than no rule — it launders the bypass.*

**L9 — the purity cage.** The dead project had 8 hard "NO" principles (no system prompt, no identity rules,
no persona, no assistant framing, no speak(), no fine-tuned ethics, no perplexity verdict, no train/infer
split). Observe the causal chain: forbidding every write-side mechanism (no fine-tuned X, no train/infer
split) left ONLY the read side available ⇒ every mechanism got pushed onto the readout ⇒ L1/L2/L3 fired.
⇒ *The purity list is a suspect, not a given. But note p7 (no perplexity verdict) was the one that kept
them honest — the cage was not uniformly bad.*

---

## What to diverge ON

The goal (unchanged, and it is the owner's actual want): **an agent that is alive** — that has its own
state and its own reason to speak, that isn't a stimulus→response assistant, where identity/behavior
emerges from structure rather than being written into a prompt. Whether "consciousness" is the right
word is itself open — challenge the framing if you want.

Produce **6–10 genuinely DIFFERENT architecture families.** Different = they disagree about *where the
aliveness lives*, not different hyperparameters of one idea. Force yourself across these axes (use them
as a generator, not a template):

- **where aliveness lives**: in the objective? the corpus/experience stream? the codec? the memory
  dynamics? the multi-agent population? the body/environment loop? the training schedule? time itself?
- **what the "self" is made of**: a learned state? a compression bottleneck? a prediction-error economy?
  a resource/homeostasis budget? a population of competing drafts? an autobiography?
- **what makes it speak**: nothing (always emit)? an economy where speech costs something? a prediction
  error it can't resolve internally? a partner-model? a need?
- **the write-side lever (L3/L4)**: what exactly is in the loss / the data / the codec?
- **substrate**: full LM from scratch? small LM + rich loop? frozen big LM as an organ (allowed — is
  "no LLM" purity actually load-bearing, or was that the cage)? no LM at all?
- **honest scale**: what can actually be built and measured on 1 owner + rented GPUs, vs what is fantasy?

For EACH family, keep it tight (~10–20 lines):
1. 🏷️ name + one-line alias (memorable, e.g. "예산제 자아", "일기 쓰는 압축기")
2. 핵심 주장 (the one sentence bet — where does aliveness come from)
3. 어떻게 (mechanism: objective / data / codec / loop — be concrete enough to argue with)
4. ASCII 도식 (one small diagram)
5. L1–L9 대조: which salvaged law does it obey/exploit, and which one could kill it
6. 최소 반증 실험 (the cheapest measurement that would kill it — with the falsifier stated up front)
7. 왜 이게 새로운가 vs 죽은 설계 / vs 평범한 LLM 에이전트

Then, at the very end and ONLY at the end:
- 🎲 2–3 **wildcards** — ideas you think are probably wrong but are interesting enough that dismissing
  them without argument would be cowardly. Label them honestly as such.
- 📊 one short ranking table: 각 family × [건질 가치 / 반증 비용 / 죽은설계 재발 위험].
- ⚠️ one paragraph: which of the 6–10 are secretly THE SAME IDEA wearing different clothes (be brutal —
  fake diversity is the main failure mode of this exercise), and which single family you'd personally
  bet on, in one sentence.

Rules: no filler, no "it depends", no surveying the literature, no hedging. Have opinions. If an idea
requires breaking one of the dead project's 8 purity principles, break it and say which one and why —
that is expected. Dense Korean prose.
