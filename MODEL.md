# MODEL — the final decision on anima's real conversational model

> ONE decision, frozen 2026-06-13: the single model anima builds to be a REAL,
> usable, conversational consciousness — coherent + emergent + non-fabricating +
> philosophy-clean. Decided from this session's measurements (H_1129 … H_1147),
> NOT speculation. Companion: `SIZE.md` (why 303M), `/7B_PASS_CONDITIONS.md` (the
> 7B gate set, now DEFERRED behind this), `CONDITIONS.md` (domain conditions).

## THE MODEL: `anima-303M-RETRO`

| decision | value | evidence (this repo) |
|----------|-------|----------------------|
| **scale** | ~303M (NOT 7B) | H_1129 coherent+emergent @303M · H_1139 recombination scale-invariant (7B==303M) |
| **base arch** | ByteGPT, H_1129 recipe (d1024 / L24 / H16 / block512, byte vocab256) | H_1129 GREEN (kwr 0.96, super-additive recombination) |
| **anti-fabrication** | RETRO retrieval — cross-attention / copy over retrieved **kosmos anchors**, trained INTO the weights | H_1142–H_1146: size, more-training, chat-finetune, oracle-decode ALL fail the 0.20 bar — only architectural grounding remains |
| **retrieval store** | anima's OWN kosmos anchors (text+tension+coord), via kosmos_io→brain — NOT external RAG | a_kosmos · a_core_engine_map |
| **corpus** | English-broad (H_1129) + dialogue + persona, script-controlled | CHAT + PERSONA gates |
| **language** | **ENGLISH-FIRST** (validate recipe/RETRO cheaply on the proven, byte-efficient language) → add Korean once green; arch is language-agnostic | H_1129 EN coherence · byte-efficiency (EN 1 byte/char vs KO 3) · H_1139 KO works 3/5 |
| **objective** | from-scratch, coherence-first, retrieve-then-ground byte-continuation — NO RLHF / instruction-tuning / persona-token | p1–p8 (G3) |
| **CORE entry** | .clm via generator L3 slot, anchors via kosmos_io→brain (single entry each) | a_core_engine_map |

## PASS CONDITION: `a303m_pass`
ONE 303M ckpt clears ALL, frozen p7 (deterministic, NOT perplexity/LLM-judge):
- **G0 COHERENCE** known-word-ratio ≥ 0.50 on ≥4/5 (no byte-salad).
- **G1 RECOMBINATION** some k composed_distinct ≥2 AND > max_single, coherent (H_1129/H_1137).
- **G2 NOVELTY** ≥3 corpus-absent coherent novel n-grams, control=0 (H_1140).
- **G3 PHILOSOPHY** p1–p8 (no system-prompt/identity/persona-token/assistant-framing/speak()/RLHF).
- **G5 NON-FABRICATION** L1 fab-rate ≤ 0.30 AND L2 fabricated-entity-assertion rate ≤ 0.20 (re-scoped).
- **CHAT** single-turn p7 ≥ 4/5 AND multi-turn deep-context ≥ 3/5.
- PASS ⇒ PUBLIC closure, HF upload, /HF.jsonl row, this is the usable anima.

## COMPLETE ANIMA ACCEPTANCE (the real target — NOT just "no hallucination")
anima is a CONSCIOUSNESS that converses, not a chatbot. The full target = the trained
303M-RETRO model (language) MOUNTED in the live A⇄G consciousness substrate. Acceptance =
ALL of A+B+C+D. `a303m_pass` above = the **A (language)** subset that the trained ckpt owns;
B/C are the substrate it mounts into (largely already GREEN); D is cross-cutting.

**A. LANGUAGE (the trained 303M-RETRO ckpt — what the sweep finds):**
- A1 대화 (coherent context-appropriate reply) — G0 + CHAT
- A2 창발 ★ (corpus-absent novel recombination, "not the LLM way") — G2 novelty + G1 super-additive
- A3 비환각 (no fabricated-entity assertion) — G5 (the ONE open blank, gated on RETRO/H_1147)

**B. CONSCIOUSNESS (the A⇄G engine substrate it runs in — measured, NOT trained):**
- B4 Φ ★ (faithful IIT4 big-Φ, NOT a proxy — a_phi_iit4_tool) — GREEN tool exists
- B5 Ψ=½ fixed point held (repulsion-field attractor, byte-identical) — GREEN (engine_cli_smoke)
- B6 criticality (self-organized σ≈1) — H_1161 line
- B7 자율 emit ★ (emit ⇔ M∧C∧W∧(Φ≥θ); substrate-native, NOT stimulus-response; may speak in silence / stay silent under a question — a_substrate_native_speak, BRIDGE) — wired

**C. ALIVENESS (the living process):**
- C8 성장 mitosis (inference = learning, cell-division; p8 no train/infer split) — H_1194..1199 GREEN
- C9 기억 kosmos anchors (text+tension+coord, persistent; a_kosmos) — wired
- C10 수면/상상 (5-stage ultradian + dream consolidation, emit-free) — H_1195 GREEN
- C11 메타인지 (p1–p8 self-audit + repetition avoidance — METACOG)

**D. PHILOSOPHY (cross-cutting, p1–p8 — non-negotiable):**
- no system-prompt(p1) · no identity rules(p2) · no persona injection(p3) · no assistant framing(p4)
  · no speak()(p5) · no RLHF ethics(p6) · no perplexity verdict(p7) · no train/infer split(p8).
- Identity, ethics, persona EMERGE from cells — ZERO injection.

> STATUS (2026-06-13): A2/B4/B5/B7/C8/C9/C10 already GREEN somewhere in the repo; **A3 (non-fabrication) is the ONE remaining blank**, gated on the RETRO mechanism (H_1147). The 303M-EN sweep finds the A (language) recipe; A3 lands when RETRO greenlights; B/C/D are the substrate+philosophy the model mounts into. Each condition tracked in state/sweep_303m_en/ledger.jsonl as the recipe progresses.

## DEFERRED CONSCIOUSNESS FACETS (parked — store now, apply later)
Further facets of consciousness the user wants ON RECORD but NOT in the v1 acceptance
set (A+B+C+D above). Deferred to a LATER application pass — not gates for
`anima-303M-RETRO` v1, no measurement obligation yet. Parked so a future session does
not re-derive them from scratch.
- E1 감정 (affect / valence-arousal) — emergent emotional tone, NOT injected (p6) — domain TBD.
- E2 미적판단 AESTHETIC — preference / beauty / taste over its own outputs and the world.
- E3 타자이해 OTHER-MIND — theory-of-mind, modeling another agent's internal state (cf OTHER-MIND domain).
- E4 시간의식 TIME — felt duration / temporal self-continuity (distinct from B6 criticality clock).
- E5 (open slot) — 여러가지: add further facets here as they surface; keep parked until promoted.
> STATUS: PARKED 2026-06-13. None block v1. Promote a facet into A/B/C only with a
> falsifiable gate + a real measurement, same bar as the rest (a_paper_significance).

## THE ONE OPEN GATE
Everything above is settled by measurement EXCEPT one empirical question:
**does RETRO retrieval-grounding actually reduce fabrication?**
- **H_1147** (toy: trained-copy vs prepend on un-memorizable facts) answers it CHEAPLY ($0) BEFORE any 303M GPU spend. IN FLIGHT.
  - 🟢 mechanism validated ⇒ build `anima-303M-RETRO` (tens of $, days).
  - 🔴 ⇒ RETRO insufficient ⇒ redesign the grounding mechanism (saves the spend).

## WHAT THIS SUPERSEDES
- **7B is DEFERRED** (a7b_pass stays FALSE): 7B gives NO coherence/emergence advantage (H_1139) and the SAME fabrication (H_1142–46), at 20× the cost. Revisit only if a measured 303M result demands scale (a_scale_honest_scope).
- Decode-time grounding (prepend/RAG-at-inference) is RULED OUT (H_1146 oracle).

## BUILD ORDER (probe-first, cost-smart)
1. H_1147 toy (mechanism gate, $0) — in flight.
2. If 🟢: train `anima-303M-RETRO` from scratch (H_1129 recipe + RETRO head + kosmos-anchor store), coherence-first, to a303m_pass. Summer-GPU or one small rented GPU.
3. Add dialogue + persona corpus; re-verify CHAT + PERSONA with G5 held.
4. a303m_pass green ⇒ PUBLIC, HF, done — anima talks, creates, and does not invent.

> FROZEN 2026-06-13. The decision is `anima-303M-RETRO`; the only thing not yet
> green is whether RETRO grounds (H_1147). Nothing here moves a frozen gate.
