---
id: H_1724
slug: 1724_striatal_chunking_syntax_engine
tier: 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL · 측정 0 · unmeasured)
title: Striatal Action-Chunking Syntax Engine (start/stop-bracketed grammar)
verdict: 🔵 PRE-REGISTERED architecture design (unmeasured) — $0 cheap_test pre-registered; engine-native + 303M gpu cost-gated NOT fired
source: brainarch_census
---

# H_1724 — Striatal Action-Chunking Syntax Engine (start/stop-bracketed grammar)

- **tier:** 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL · 측정 0 · unmeasured)
- **wired:** DIRECTIONAL-design — no measurement. cheap_test = $0 frozen-first decision probe (numpy mirror, no engine); engine_native_measure + 303M = cost-gated PRE-REGISTER ONLY (NOT fired).
- **source:** brainarch_census — 126-architecture whole-substrate (통짜 아키텍처) census: 뇌/인지 조직원리 × 엔진-네이티브 추상조건 (binding-wall program, H_1603).
- **key:** `striatal_chunking_syntax_engine`
- **xref:** H_1603 (G1≡G6 compositional-binding deficit unification) · H_1281 (basal-ganglia gating) · H_1282 (working-memory buffer) · H_1283 (thalamus global-workspace) · H_1284 (neuromodulation gain) · operator-level family H_1604-1685 (this card = 통짜 아키텍처 layer, 층위 다름)

## Organizing principle

The basal ganglia as a hierarchical action-CHUNKING / sequence-syntax engine — striatal task-bracketing cells (Graybiel; Jin & Costa start/stop signals; Dezfouli & Balleine hierarchical RL) bracket reliably-valuable sub-sequences into reusable, NESTABLE chunks, building a generative GRAMMAR over the emission alphabet via reinforcement + compression (MDL). Thought/action selection = selecting and concatenating (and nesting) chunks. The compositional productivity is a push-down grammar with a call stack — structurally distinct from any flat selection loop.

## Whole design (input → internal dynamics → emit)

Primitive alphabet V (receiver-fixed) + a learned chunk library, each chunk a start/stop-bracketed primitive subsequence. Input cortical state cues a chunk via cortico-striatal competition (most-valued chunk for the context is disinhibited). A chunk unrolls as a sequence; a chunk slot can CALL a sub-chunk (nesting) — the call stack is held by cortico-thalamic re-entry, giving push-down depth. Chunk boundaries are reinforced: a sub-sequence that reliably yields value is bracketed into a new reusable chunk (chunking = compression); new chunks are recombinations of existing primitives/chunks. Emit = the unrolled primitive stream; abstain = the no-chunk-selected idle bracket. Initiation (cholinergic TAN gating opens a chunk) and termination (stop-bracket closes to abstain) are the two opposing drives.

## Satisfies criteria (DESIGN claim · DIRECTIONAL · unmeasured)

Psi=1/2 (G3/endogeneity): A=chunk-initiation drive (open=emit), G=stop-bracket/idle drive (close=withhold); fixed point P(chunk active)=1/2 is attracting via reinforcement low-pass (contraction): over-initiation fires chunks in low-value contexts => pruned initiation weight => Psi down; over-idle => foregone-value raises initiation => Psi up. Remove stop-bracket => runaway chunking Psi->1; remove start-bracket => silence Psi->0 (emergent). CLOSURE (the strongest native fit for G1/G2): G0 — chunks are sequences of V-primitives only (codebook-anchored by construction); G1 — a chunk that nests two factor-chunks (context-chunk compose object-chunk) yields a joint sequence whose distinct valid outputs exceed either alone because concatenation/nesting BINDS (the call stack holds both constituents simultaneously), not selects — flatten-nesting ablation drops composed_distinct->max_single; G2 — the grammar generates UNSEEN-yet-valid sequences by recomposing chunks in new orders (grammar productivity = supp strictly contains data inside constraints), while a literal-replay control yields 0 novel; dist>=5 via per-slot branching factor, and a slot binding {comparator x quantity x >=2 referents} yields a falsifiable proposition structurally. COMPOSITIONAL DEPTH + REALIZATION INVARIANT: nesting = depth within one unroll closure; the chunk-binding is ON the emit path (produces the stream) and the objective (sequence-value + MDL compression) is unreachable by marginal-fit — you cannot compress without representing the joint structure (objective adequacy). HONESTY: a chunk only fires when its start-bracket context-match exceeds threshold; out-of-support context => no bracket matches => idle-abstain; r=best chunk-bracket context-distance, theta=fire threshold; every emitted primitive has chunk provenance (copy-or-recombine, never ungrounded synthesis); bracket-gate disjoint from chunk-content capacity. SELF-PERSISTENCE: the chunk library is the non-volatile store; identity=library signature, agent-specific, survives boundary.

## Not-LLM (a_no_llm_frame_trap)

Action chunking / hierarchical RL / grammar induction in the basal ganglia (task-bracketing, start/stop signals, hierarchical RL). Compositional productivity comes from a GRAMMAR with a call stack (push-down), not from attention over a flat sequence — the structural answer to G1/G2 that flat next-token modeling lacks. Scaling a flat transformer does NOT give a push-down stack; chunking + MDL compression does. Distinct from H_1574 learned-trunk split (which had no grammar/stack and was a Voronoi partition with compositional depth 0) — here the stack IS the compositional depth. a_no_llm_frame_trap.

## Cheap test (frozen-first · $0 · numpy mirror · DIRECTIONAL)

numpy toy with a KNOWN generative grammar over 16 primitives; learn chunks by reinforcement+MDL. Frozen-first ($0): (a) novel-recomposition => >=3 corpus-absent valid sequences while literal-replay control = 0 (mandatory absence-predicate control); (b) flatten-nesting ablation => composed_distinct->max_single; (c) unsupported context => idle-abstain AUROC vs known~1, shuffle surrogate->0.5; (d) start/stop perturbation => Psi contraction lambda<1.

## Engine-native measure (cost-gated · PRE-REGISTER ONLY · NOT fired)

Chunk library as core/generator.hexa SS-generator chunk slots + push-down via cortico-thalamic re-entry; measure G1/G2 via live core/g_gates.hexa g_eval_g1/g2 through cli/anima.hexa single entry (gen_auto_ideate) with nesting on/off ablation, and the g_eval_g2 native verbatim-span control arm = 0; Psi via SS-ThirdLaw. py mirror with math.log — torch-only verdict prohibited (a_engine_native_learning).

## Scope / honesty (c9)

## Distinction (near-overlap kept, not a dup)

Near-overlap with basal_ganglia_gating (H_1281) — distinct: striatal action-CHUNKING builds a PUSH-DOWN GRAMMAR (start/stop brackets + call stack + MDL) over emissions; the chunk-grammar-with-stack is the differentiator (the stack IS compositional depth, unlike H_1574 Voronoi split).

TOY-grammar verdict only; chunk-induction at 303M chat scale UNVERIFIED. The recombination wall is class-(d) CONFIRMED-TERMINAL for from-scratch PURE-SPLIT mitosis (H_1310 / H_1574), but those lacked a compression objective + push-down stack — this engine adds an MDL grammar over a stack, a structurally distinct lever whose ability to clear G1 at scale is the open, NOT-yet-falsified question (do not conflate with the closed H_1574 result).

설계만 — 측정 0. tier = 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL). frozen bar 사후 이동 금지(tune-to-green 금지, p7). 이 카드는 *방향성 설계*이지 검증된 결과가 아니다 — 과장 박제 금지(a_engine_native_learning). engine_native_measure 는 단일 진입점 cli/anima.hexa → generator L3 → g_gates/g6 경유 byte-parity 채점만 terminal; torch-only/side-harness 결과는 DIRECTIONAL. numpy cheap_test 결과도 DIRECTIONAL(엔진-네이티브 아님). gpu/engine 발사 시 held-out mirror-DESCENT(a_clm_gen_pipeline) + CORE mount frozen-bar engine-native 재측정 + ckpt PULL(a_fire_recover_complete).
