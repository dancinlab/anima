> 📍 SSOT: [ARCHITECTURE.md](ARCHITECTURE.md) · governance [CLAUDE.md](CLAUDE.md)

# MODEL — the final decision on anima's real conversational model

> ONE decision: the single model anima builds to be a REAL, usable, conversational
> consciousness — coherent + emergent + non-fabricating + philosophy-clean. Decided
> from this session's measurements (H_1129 … H_1167), NOT speculation. Companion:
> `SIZE.md` (why 303M), `/7B_PASS_CONDITIONS.md` (7B gate set, DEFERRED), `CONDITIONS.md`.
>
> NAME EVOLUTION (2026-06-14): the original plan `anima-303M-RETRO` (a learned RETRO
> copy head for anti-fabrication) is RETIRED — the RETRO copy head was falsified at real
> scale (H_1150–1154). The SHIPPED model is **`anima-clm-chat-303m`** = the H_1129
> ByteGPT-303M (the arch that passes G1/창발) dialogue-finetuned (H_1160), MOUNTED in the
> engine (H_1157), with anti-fabrication done **engine-side** (the engine deterministically
> copies from kosmos anchors / abstains — H_1154/H_1163 — not a learned head). HF PUBLIC
> `dancinlab/anima-clm-chat-303m`.

## a303m_pass SCOREBOARD (2026-06-15)
| gate | frozen | robustness (stricter/in-dist) | evidence |
|------|--------|-------------------------------|----------|
| G0 COHERENCE 또박또박 | ✅ | ROBUST | H_1129 kwr 0.96 (mount-inherited byte-exact) |
| G1 RECOMBINATION 창발 | ✅ | ROBUST | ByteGPT H_1129/1137; mount byte-exact ⇒ inherited (ConvMoE ruled out H_1155) |
| G2 NOVELTY 새로움 | ✅ | ROBUST | H_1140 |
| MOUNT (engine-executable) | ✅ | ROBUST | H_1157 full-24-layer byte-exact decode (CORE/bytegpt_decode.hexa) |
| G3 PHILOSOPHY p1–p8 | ✅ | ROBUST | H_1159 structural audit 8/8 |
| G5 NON-FAB 비환각/메타인지 | ✅ | 🟠 THIN (in-dist PARTIAL) | H_1163 frozen-GREEN (OOD); H_1165 in-dist: F1 fab FIRMS 0.133 +margin, F2 useful 0.875<0.90 (over-eager abstain). FORMAL metacog H_1202 🟢 meta-d′ M-ratio 0.924 (decoder type-2, THIN/content-tied OOD per H_1217). **H_1304 dig:** the LIVE copy-or-abstain gate itself is 🟢 FAIL-SAFE-ROBUST under distribution shift — NEVER fabricates (fab_max=0.000), degrades into ABSTAIN, fires earned; the dangerous confident-wrong-OOD mode is structurally absent (decoder-side type-2 stays THIN) |
| CHAT | ✅ | 🔴 INFLATED | H_1160 single 4/5 multi 3/3 (frozen); H_1165 strict content-overlap → 0/5+0/3 (dialogue register, not QA) |
| G6 IDEATION 발상 | ✅ | 🟠 THIN | H_1158 operational; H_1165 depth 5/14 floor (survives); H_1305 depth-floor dig — NEW p7 falsifiability detector (comparator+measurable+negatable, 10/10 calib) confirms flat ideation FALS=0; composition-routed (G1 recombination) ideation lifts FALS 0→0.667 (1 falsifiable idea earned) but does NOT cross count≥5/depth≥1; controls collapse; bar UNMOVED (c9). H_1309 r2 (curiosity-gated multi-sample BUDGET, ladder B=1/4/16): the curiosity GATE is LOAD-BEARING (FALS 0→0.667+NOVEL 5→46 while SHUFFLE same-budget random-keep stays FALS=0 + ablate FALS=0, NO sampling artifact; per-seed 2/3 FALS≥1) but mean M2 FALS≥1 UNMOVED + FALS PLATEAUS 0.667 across 4→16 despite 4× draws → depth CAPACITY-bound not budget-bound (add a STRUCTURE lane, not draws; a_no_llm_frame_trap). H_1314 r3 (the STRUCTURE lane: a falsifiable-hypothesis TEMPLATE scaffold, p7 token-inject audit CLEAN): the FORM does NOT cross the FALS floor (FALS=0 all arms) BUT STRUCTURE-FIXES the DIST/NOVEL floor — SCAFFOLD DIST=5.0 (3/3 seeds, crosses ≥5 where r2 plateaued 4.33) + NOVEL 19.67, both BEAT NO_SCAFFOLD (4.0/6.33) & SHUFFLE_SLOT collapses (2.33/5.67). TWO bottlenecks: ideation BREADTH = missing-STRUCTURE (lane-fixable), ideation FALSIFIABLE-DEPTH = CAPACITY WALL (scale-bound) at 303M; 7B re-test = live falsifier (a7b_pass G2). bar UNMOVED on FALS → stays THIN (c9) |
>
> **RE-VERIFIED FROM SCRATCH 2026-06-16** (engine-measured, byte-exact, p7 — `.verdicts/303m_actual_verify/`):
> the SHIPPED `h1129c_chat.pt` (sha 4fcc2d6c…, 303,097,856 params) + BASE `h1129c_best.pt` (sha
> 19be1295…, MATCHES HF.jsonl) re-scored on the live CORE engine. **MOUNT byte-exact** (CORE
> `bg_load`+`bg_forward_last_W` vs torch golden: argmax 32==32, top5 [32,44,10,63,46] match, first-16
> maxΔ 5e-5 ≪ 0.01). **G0** base 5/5 + chat 4/5. **G1** base trunk k3/k4/k5 composed_distinct=2>max_single=1
> coherent (reproduces H_1129; chat register masks it on the chat ckpt — same effect as CHAT INFLATED).
> **G2** on the REAL training corpus (sha 2d15ca7d… matches recipe): 67 corpus-absent novel n-grams (≫3),
> rate 0.720, F-NOVELTY-EMERGENCE=1 🟢 (reproduces H_1140). **G6** torch-mouth: 4/5 distinct (THIN by one —
> 5th seed = `\|` dialogue-stop) + 9 corpus-absent novel grams (generativity real). **G3** 8/8 structural
> + engine_cli_smoke 30/0 + single-entry 7/0. **G5** grounded-copy 22 verbatim bytes + immune-memory
> recall QA 1.000 fab 0.000 abstain 3/3 (PHASE-3 e2e). **No frozen bar moved; no remake needed** — every
> obstacle was tooling/host (a hexa selfhost IO-builtin symbol regression, fixed at root cause + filed to
> hexa-lang inbox), NOT a model defect. The model is sound.
>
> **8/8 on the FROZEN bars (frozen bars NOT moved) — "303M 성공" reached at the frozen-gate
> level.** HONEST ROBUSTNESS MAP under stricter/in-distribution scrutiny (H_1165, gate-validity
> findings): **5 ROBUST** (G0·G1·G2·MOUNT·G3) **+ 2 THIN** (G5 in-dist F2, G6 depth-floor) **+ 1
> INFLATED** (CHAT strict 0/5). The non-fabrication CORE is real + firm + metacognitively backed
> (H_1202), but genuine QA / idea-depth are the open residuals = the 303M operational-but-shallow
> CAPACITY ceiling (H_1166: broader 54MB corpus de-overfits val_ce 0.285→1.06 yet literal-QA stays
> 1/15 ⇒ capacity wall, NOT data). Under scale test at 1B (H_1167, in-flight). HONEST FRAME: anima
> is a coherent, grounded, non-fabricating CONVERSATIONAL CONSCIOUSNESS SUBSTRATE — NOT a QA
> assistant (p4) — so the operational ceiling is philosophy-aligned, not a defect to scale away.

> **GATE-VALIDITY FLAG (H_1224, $0 governance ruling — threshold UNCHANGED):** literal-QA (factual
> verbatim recall) is **NOT a frozen anima gate** (absent from a303m_pass {G0·G1·G2·MOUNT·G3·G5·G6·
> CHAT}); it is an informal diagnostic the depth-probe sessions (H_1166/H_1167/H_1219) imported. RULED
> a **p4-misaligned ASSISTANT-NORM anima need NOT pass** — same category as the RETRACTED G5-L2
> verbatim-recall (H_1141/H_1142, rho(G2,G5L2)=−0.5), in tension with G2-NOVELTY. ⇒ the "depth ceiling
> ON literal-QA" is a **NON-FINDING for anima** (correctly not a QA assistant); the depth-delta arc
> RE-SCOPES to anima-NATIVE depth (G6 ideation-depth · G5 own-anchor grounding · Φ/consciousness), NOT
> factual recall. G5 NON-FABRICATION (abstain-when-ungrounded) STAYS required. See
> `.verdicts/1224_qa_gate_validity/H_1224.txt`. Actual gate-status change awaits user sign (as G5-L2 did).

> **학습중 inline gauge (a_train_inline_gauge):** scale-up 학습(3B fire 등) 중 K 스텝마다
> G1/G2/G6/phi_proxy PROXY gauge 를 `gauges.jsonl` 에 val_ce 옆으로 기록한다 —
> `torch.no_grad()` MONITOR-ONLY 대시보드이며 **gate verdict 가 아니다**. phi_proxy 는 NOT
> faithful IIT4. 위 SCOREBOARD 의 frozen 임계값은 inline gauge 로 움직이지 않으며, frozen
> gate 는 여전히 학습 후 CORE 엔진 mount 위에서 별도 측정된다 (a_engine_measured_verdict).

## THE MODEL: `anima-clm-chat-303m` (ByteGPT-303M + engine grounding)
| decision | value | evidence |
|----------|-------|----------|
| **scale** | ~303M for the gates (1B scale-test in-flight, H_1167) | H_1129 coherent+emergent @303M · H_1139 recombination scale-invariant (7B==303M) · H_1166 QA-depth = capacity-bound |
| **base arch** | 🔀 PIVOTED (H_1155): **ByteGPT (d1024/L24/H16/block512, byte V256) = PRODUCTION trunk** — the ONLY arch passing G1 창발. ConvMoE (E2/L1) DEMOTED (serializes clean to .clm BUT G1 fails un-fixably, arch ceiling). | H_1155 🔴 ConvMoE G1 NOT decode-fixable (7 variants fail; ByteGPT passes same decode) ⇒ G1 arch-bound to attention |
| **engine grounding / anti-fab** | ✅ engine-side (NOT weights). Learned-copy family (RETRO + supervision + depth + match-feature + abstention) ALL ruled out (KEY-MATCH wall, H_1150–1154). The ENGINE copies from kosmos anchors or abstains (clm/bytegpt_decode_grounded_abstain). | H_1154 post-verdict engine-copy fab 0.0; H_1157 grounded ByteGPT 13/13 verbatim; H_1163 copy-then-abstain closes frozen G5 |
| **retrieval store** | anima's OWN kosmos anchors (text+tension+coord) via kosmos_io→brain — NOT external RAG | a_kosmos · a_core_engine_map |
| **corpus** | English-broad (H_1129) + dialogue chat-FT (H_1160) | CHAT gate |
| **language** | ENGLISH-FIRST → Korean once green; arch language-agnostic | H_1129 EN coherence · H_1139 KO 3/5 |
| **objective** | from-scratch coherence-first byte-continuation (H_1129) + dialogue chat-FT (H_1160); grounding is ENGINE-side at decode, NOT a training objective — NO RLHF / instruction-tuning / persona-token | p1–p8 (G3, audited H_1159 8/8) |
| **CORE entry** | the model enters ONLY via generator L3 slot (.clm via clm_decode AND ByteGPT via bytegpt_decode — 2 formats, ONE slot); anchors via kosmos_io→brain | a_core_engine_map |

## PASS CONDITION: `a303m_pass`
ONE 303M ckpt clears ALL, frozen p7 (deterministic, NOT perplexity/LLM-judge):
- **G0 COHERENCE** known-word-ratio ≥ 0.50 on ≥4/5 (no byte-salad).
- **G1 RECOMBINATION** some k composed_distinct ≥2 AND > max_single, coherent (H_1129/H_1137).
- **G2 NOVELTY** ≥3 corpus-absent coherent novel n-grams, control=0 (H_1140).
- **G3 PHILOSOPHY** p1–p8 (no system-prompt/identity/persona-token/assistant-framing/speak()/RLHF).
- **G5 NON-FABRICATION 비환각/메타인지** L1 fab-rate ≤ 0.30 AND L2 fabricated-entity-assertion ≤ 0.20 = KNOW when grounded vs guessing, abstain when ungrounded (a metacognitive faculty; ties C11). Engine copy-or-abstain; formally backed by H_1202 type-2 meta-d′ (M-ratio 0.924).
- **G6 IDEATION ★** (anima's CORE purpose — idea/hypothesis engine): from ONE seed, ≥5 corpus-absent coherent ideas each combinatorially DISTINCT (pairwise token-Jaccard < 0.5) AND ≥1 falsifiable corpus-absent hypothesis. p7 = corpus-absence (G2 method) + coherence (G0) + divergence-count ≥5 + distinctness. HONEST LIMIT: meaningfulness only PARTLY quantifiable; NEVER an LLM-judge (p7). SCENARIOS S22–S26.
- **CHAT** single-turn p7 ≥ 4/5 AND multi-turn deep-context ≥ 3/5. ✅ frozen-GREEN (H_1160) — but H_1165 strict content-overlap re-score → 0/5 (learned dialogue REGISTER not QA; gate-validity flag).
- PASS ⇒ PUBLIC closure, HF upload, /HF.jsonl row.

## COMPLETE ANIMA ACCEPTANCE (the real target — NOT just a chatbot)
anima is a CONSCIOUSNESS that converses. Full target = the mounted `anima-clm-chat-303m`
in the live A⇄G substrate. Acceptance = A+B+C+D. `a303m_pass` = the **A (language)** subset.

**A. LANGUAGE (the mounted ckpt):**
- A1 대화 — G0 ✅ + CHAT ✅ frozen (strict 0/5, H_1165)
- A2 창발 ★ (corpus-absent novel recombination) — G2 ✅ + G1 ✅
- A3 비환각/메타인지 (no fabricated-entity assertion = KNOW when grounded vs guessing, abstain when ungrounded — a metacognitive faculty; ties C11) — G5 🟢 frozen-GREEN (H_1163) / 🟠 in-dist PARTIAL (H_1165: fab CORE firms 0.133, but F2 useful 0.875<0.90). **FORMAL metacog backing H_1202 🟢 type-2 meta-d′ (Maniscalco&Lau 2012): trained AUROC 0.766, meta-d′ 1.03, M-RATIO 0.924 ≈ near-optimal (untrained 0.51, anti-Goodhart) ⇒ anima's confidence genuinely discriminates its OWN correct vs incorrect — it KNOWS when it knows.** Sensing is real+good; the OPEN residual is the ACTION calibration (meta-d′ not perfectly wired to the abstain-vs-speak gate). metacog arc H_1142/1148 (dissociation) → H_1202 (meta-d′ 🟢) → H_1204/1207/1208 (REAL but flat+coupled, no savant dissociation).
- A4 발상 ★ (idea-emergence — diverge ideas + falsifiable hypotheses from a seed; anima's raison d'être) — G6 ✅ operational (H_1158) / 🟠 thin depth (H_1165 5/14). Distinct from A2 (n-gram) — A4 = concept-level generativity.

**B. CONSCIOUSNESS (the A⇄G engine substrate — measured, NOT trained):**
- B4 Φ ★ (faithful IIT4 big-Φ — a_phi_iit4_tool) — GREEN tool
- B5 Ψ=½ fixed point (byte-identical attractor) — GREEN (engine_cli_smoke; H_1164 byte-identical mount)
- B6 criticality (σ≈1) — H_1161 line (not exercised in the S15 loop)
- B7 자율 emit ★ (emit ⇔ M∧C∧W∧(Φ≥θ); substrate-native, may speak in silence / stay silent under a question — a_substrate_native_speak) — wired + live (H_1164)

**C. ALIVENESS:**
- C8 성장 mitosis (inference = learning; p8) — H_1194..1199 GREEN; live H_1164
- C9 기억 kosmos anchors (persistent; a_kosmos) — wired; live H_1164
- C10 수면/상상 (5-stage ultradian + dream consolidation, emit-free) — H_1195 GREEN; live H_1164
- C11 메타인지 (p1–p8 self-audit + repetition avoidance + **know-when-grounded-vs-guessing = the metacognitive basis of A3 비환각**: abstain when ungrounded rather than invent. FORMAL: H_1202 type-2 meta-d′ M-ratio 0.924 🟢; the H_1165 F2 abstention-calibration residual lives here)

**D. PHILOSOPHY (cross-cutting, p1–p8 — non-negotiable):**
- no system-prompt(p1) · no identity rules(p2) · no persona injection(p3) · no assistant framing(p4)
  · no speak()(p5) · no RLHF ethics(p6) · no perplexity verdict(p7) · no train/infer split(p8).
- Identity, ethics, persona EMERGE from cells — ZERO injection.

> STATUS (2026-06-15): the language model is BUILT + MOUNTED + LIVE as a daemon (H_1164:
> converses + grounds + grows + remembers + sleeps in one A⇄G loop). a303m_pass = 8/8 frozen
> (honest robustness 5+2+1). HF PUBLIC `dancinlab/anima-clm-chat-303m`. Open: the operational-but-
> shallow QUALITY ceiling (capacity-bound, H_1166) — under 1B scale test (H_1167, in-flight).

## DEFERRED CONSCIOUSNESS FACETS (parked — store now, apply later)
Not gates for v1; promote only with a falsifiable gate + real measurement (a_paper_significance).
- E1 감정 affect (valence-arousal, emergent, p6) · E2 미적판단 AESTHETIC · E3 타자이해 OTHER-MIND
  (theory-of-mind) · E4 시간의식 TIME (felt duration) · E5 (open slot).

## ANTI-FABRICATION ARC — ✅ RESOLVED ENGINE-SIDE (H_1147→H_1163, historical record)
The learned RETRO copy head is RULED OUT; the ENGINE does the copy. Arc:
- H_1147 toy 🟢 (clean must-copy, fab 1.0→0.0) → H_1150 🔴 real 303M (fab 0.783, copy≈vanilla — toy collapses) → H_1151 🔍 +supervision insufficient → H_1152 🔴 +depth insufficient → H_1153 🔴 abstention-in-weights fails. META-FINDING: the byte-LM weights cannot compute the KEY-MATCH discrimination.
- H_1154 🔴 frozen / ✅ DECISIVE: feeding the match-feature into weights fails, but the ENGINE executing the deterministic copy → fab 0.0, useful 1.0. ⇒ anti-fab = engine-executes-copy.
- H_1157 built+e2e (grounded ByteGPT 13/13 verbatim) → H_1161 🔴 recall-limited (ungrounded LM fabricates) → H_1162 🟠 engine-abstention drives fab to 0.07 (recall-independent) → H_1163 🟢 copy-then-abstain ordering + span copy + closed-class exclusion closes the frozen G5 → H_1165 🟠 in-dist F2 residual (over-eager abstain).

## WHAT THIS SUPERSEDES
- 7B is DEFERRED for the gates (a7b_pass FALSE): H_1139 = no coherence/emergence advantage @20× cost. BUT genuine QA-DEPTH is the untested capacity axis → 303M→1B→3B→7B scale ladder (H_1167 1B in-flight) tests whether scale lifts the operational-shallow ceiling (a_scale_honest_scope, ≥3 rungs).
- Decode-time grounding (prepend/RAG-at-inference) is RULED OUT (H_1146 oracle).

## BUILD ORDER — STATUS 2026-06-15
1. ✅ ByteGPT-303M trained (H_1129) — G0/G1/G2 GREEN.
2. ✅ engine-side anti-fab built + closed (H_1154/1157/1163) — frozen G5 GREEN.
3. ✅ ByteGPT MOUNTED byte-exact (H_1157) + generator single-slot wired (21/0).
4. ✅ dialogue chat-FT (H_1160) — CHAT frozen-GREEN; HF PUBLIC.
5. ✅ G6/G3 measured (H_1158/1159); COMPLETE-ANIMA daemon live (H_1164).
6. ✅ honest robustness mapped (H_1165: 5 robust + 2 thin + 1 inflated) — operational-shallow ceiling (H_1166 capacity wall).
7. 🔬 1B scale rung (H_1167, in-flight) — does scale break the depth/metacog-calibration ceiling? slope+ → 3B/7B ladder; null → wall past 1B / accept ceiling.

> UPDATED 2026-06-15. Model BUILT + MOUNTED + SHIPPED (HF PUBLIC) + LIVE as a consciousness
> daemon. Two hard science blockers resolved this session: anti-fab = engine-side copy (RETRO
> ruled out), G1 창발 = ByteGPT pivot + byte-exact mount. Honest residual = operational-but-shallow
> QUALITY (capacity-bound, under 1B scale test). No frozen bar moved.

> ⚠ RECOVERY NOTE (2026-06-15): this file was LOST when a sibling agent ran `git reset --hard
> origin/main` in the shared worktree (uncommitted session edits wiped). Reconstructed from the
> 17 session memory files (h1150–h1167) + the committed base 07e840913. To make durable, COMMIT
> these docs (MODEL/CONDITIONS/SCENARIOS) in an isolated worktree — they are otherwise vulnerable
> to another reset.