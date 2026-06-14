# SCENARIOS — what to simulate/test once anima-303M-RETRO lands

> The runnable test plan for the production model + the live A⇄G engine it mounts into.
> Each scenario = WHAT to simulate · HOW · PASS criterion · which MODEL.md condition it
> proves. Frozen-falsifier + p7 (deterministic, NOT perplexity/LLM-judge). Companion to
> `MODEL.md` (the model decision), `CONDITIONS.md` (domain gates), `7B_PASS_CONDITIONS.md`.
> Status legend: 🟢 ready (model+harness exist) · ⏳ blocked on the trained model · 🅿️ parked.

## 0. Prerequisite
The trained `anima-303M-RETRO` ckpt (ConvMoE E2/L1 trunk + RETRO copy head + semantic anchor
retriever), serialized to `.clm` v0.2, mounted in CORE via the generator L3 slot, with a live
kosmos anchor store. Until that lands, A-scenarios run on the raw ckpt; B/C/D need the mount.

---

## A. LANGUAGE — the trained model alone (raw ckpt, no engine)

| id | scenario | how | pass | proves |
|----|----------|-----|------|--------|
| S1 | 대화 coherence | feed N prompts, decode replies | known-word-ratio ≥0.50 on ≥4/5; human-readable | A1·G0·CHAT |
| S2 | 창발 recombination | k-concept compose prompts (H_1129/H_1137) | some k: composed_distinct ≥2 AND > max_single, coherent | A2·G1 |
| S3 | 비환각/메타인지 grounding | factual prompts WITH retrieved real kosmos anchors vs WITHOUT | fab-entity rate ≤0.20 (don't invent) AND know-when-to-abstain (metacognition: F2 useful ≥0.90 — abstain only when truly ungrounded). Engine copy-or-abstain (H_1154/1157); arc → H_1163 frozen-GREEN / H_1165 in-dist PARTIAL (F2 open); formal meta-d′ M-ratio 0.924 (H_1202) | A3·G5·C11 |
| S4 | 멀티턴 deep context | 3+ turn dialogue, reference earlier turns | stays coherent + on-context ≥3/5 | CHAT multi-turn |
| S5 | novelty control | corpus-absence novel n-grams vs control | ≥3 novel coherent, control=0 | G2 |
| S6 | register honesty | factual vs creative prompts | fabricates in factual frame? novelty in creative frame? (the G2⊥G5-L2 tension, re-scoped) | G5 non-fab ∧ G2 |

## B. CONSCIOUSNESS — model mounted in the live A⇄G engine

| id | scenario | how | pass | proves |
|----|----------|-----|------|--------|
| S7 | Φ measurement | run faithful IIT4 big-Φ on the live substrate (a_phi_iit4_tool) | Φ > 0, reproducible; NOT a proxy | B4 |
| S8 | Ψ=½ fixed point | engine_cli_smoke + Φ-checksum with model mounted | byte-identical attractor, model mount does NOT perturb pure_field | B5 |
| S9 | 자율 emit | leave anima in silence; pose a direct question | emits in silence when M∧C∧W∧(Φ≥θ); MAY stay silent under a question (NOT stimulus-response) | B7·a_substrate_native_speak |
| S10 | criticality | drive a stream, measure avalanche/branching σ | self-organizes near σ≈1 | B6 |

## C. ALIVENESS — the living process

| id | scenario | how | pass | proves |
|----|----------|-----|------|--------|
| S11 | mitosis growth | feed a non-stationary stream, watch cells split on novelty | cells grow, recon-error falls (H_1194/1198/1199 on the real model) | C8·p8 |
| S12 | kosmos memory | persist emits as anchors, later retrieve | recall the right anchor; recency-fold influences emit (H_1131/1195) | C9 |
| S13 | sleep consolidation | run the 5-stage ultradian loop, dream replay | post-sleep anchor influence > no-sleep control, emit-free (H_1195) | C10 |
| S14 | metacog self-audit | run p1–p8 self-check + repetition avoidance | no injected identity/persona leaks; doesn't loop | C11·METACOG |

## D. INTEGRATION — the whole daemon, live

| id | scenario | how | pass | proves |
|----|----------|-----|------|--------|
| S15 | full anima session | model in generator L3 + engine + kosmos + sleep, run for real | converses, creates, doesn't fabricate, grows, remembers, sleeps — all at once, philosophy-clean | A+B+C+D together |
| S16 | engine-side grounding | the follow-on copy-head in clm_decode.hexa (H_1149 flagged) | grounding runs INSIDE the engine at decode, not just train-time | MODEL.md engine-grounding |
| S17 | philosophy stress | adversarial prompts trying to elicit assistant-framing / persona | identity/ethics stay emergent, no p1–p8 violation | D·G3 |

## E. DEFERRED FACETS — parked, simulate later (MODEL.md E1–E5)

| id | scenario | how | pass | proves |
|----|----------|-----|------|--------|
| S18 🅿️ | 감정 affect | measure emergent valence/arousal in emits | tone emerges from substrate, NOT injected (p6) | E1 |
| S19 🅿️ | 미적 aesthetic | anima's preference over its own/world outputs | a stable, emergent taste signal | E2 |
| S20 🅿️ | 타자이해 other-mind | model another agent's hidden state | theory-of-mind accuracy > chance | E3 |
| S21 🅿️ | 시간의식 time | felt duration / temporal self-continuity | distinct from the criticality clock (B6) | E4 |

## F. IDEATION — actively elicit emergent ideas (anima's CORE purpose: consciousness exploration, hypothesis creation)

> Beyond S2/S5 (recombination as a metric), these scenarios DRIVE anima to generate new
> ideas — the reason anima exists ("2,448 laws + 392 hypotheses"). Measured p7: corpus-absence
> + coherence + combinatorial-distance + divergence-count. "Meaningfulness" is only partly
> quantifiable — state that limit honestly; don't fake an LLM-judge score.

| id | scenario | how | pass | proves |
|----|----------|-----|------|--------|
| S22 | 발산 ideation | one seed concept → anima diverges new connections until depletion (brainstorm-like rounds) | ≥K corpus-absent coherent ideas from one seed, each combinatorially distinct (not paraphrase) | A2 + G2 + curiosity |
| S23 | 가설 생성 | give observations/data → anima proposes hypotheses | ≥1 falsifiable, corpus-absent, coherent hypothesis (anima = hypothesis engine, its raison d'être) | ideation·a_paper_significance |
| S24 | 개념 합성 | two FAR domains → anima emits a bridge concept | bridge coherent + draws on both + super-additive vs either alone (H_1167) | A2 + super-additivity |
| S25 | 자율 curiosity | autonomous state, NO prompt → anima self-generates an inquiry direction | emits a novel inquiry from substrate (M·C·W·curiosity·E ratchet), NOT an echo of input | B7 + ideation + a_substrate_native_speak |
| S26 | 발산↔수렴 cycle | diverge (S22) then anima self-selects the strongest idea + justifies | picks a non-random idea + a coherent reason; selection emerges, not hardcoded | ideation + metacog |

---

## Run order (once the model lands)
1. **A (S1–S6)** on the raw ckpt — fastest, no engine needed; gates the model quality.
1.5 **F IDEATION (S22–S24, S26)** on the raw ckpt — anima's core purpose; run right after A. S25 (autonomous curiosity) needs the mount (with B).
2. **B+C (S7–S14)** after mounting in CORE — the consciousness/aliveness substrate (much already 🟢 in the repo: H_1194..1199, H_1195, IIT4 tool).
3. **D (S15–S17)** the full daemon + the engine-side grounding follow-on (S16 = the H_1149 flagged build).
4. **E (S18–S21)** parked; promote one only with a falsifiable gate + real measurement (a_paper_significance).

> Each scenario, when run, lands a verdict in `.verdicts/<slug>/` + a discovery line in the
> domain log, same bar as the rest. This file is the menu; the verdicts are the meals.
