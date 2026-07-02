---
id: H_1698
slug: 1698_pbwm_gated_slot_register
tier: 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL · 측정 0 · unmeasured)
title: Prefrontal-BG Gated Slot Register (PBWM) — variable binding by gated working memory
verdict: 🔵 PRE-REGISTERED architecture design (unmeasured) — $0 cheap_test pre-registered; engine-native + 303M gpu cost-gated NOT fired
source: brainarch_census
---

# H_1698 — Prefrontal-BG Gated Slot Register (PBWM) — variable binding by gated working memory

- **tier:** 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL · 측정 0 · unmeasured)
- **wired:** DIRECTIONAL-design — no measurement. cheap_test = $0 frozen-first decision probe (numpy mirror, no engine); engine_native_measure + 303M = cost-gated PRE-REGISTER ONLY (NOT fired).
- **source:** brainarch_census — 126-architecture whole-substrate (통짜 아키텍처) census: 뇌/인지 조직원리 × 엔진-네이티브 추상조건 (binding-wall program, H_1603).
- **key:** `pbwm_gated_slot_register`
- **xref:** H_1603 (G1≡G6 compositional-binding deficit unification) · H_1281 (basal-ganglia gating) · H_1282 (working-memory buffer) · H_1284 (neuromodulation gain) · operator-level family H_1604-1685 (this card = 통짜 아키텍처 layer, 층위 다름)

## Organizing principle

O'Reilly-Frank PBWM: the basal ganglia gate WHAT enters and leaves robust cortical working-memory slots (input-gate / output-gate), NOT the motor output itself. Cortex maintains role-slots; selection-by-disinhibition decides which slots update each tick. Productivity comes from gating fillers into role registers, the literal substrate of variable binding.

## Whole design (input → internal dynamics → emit)

A fixed set of role-slots S1..Sk (e.g. RELATION, QUANTITY, REFERENT-A, REFERENT-B). Each slot has a BG input-gate (open=update slot from current cortical evidence, closed=robustly maintain) and the frame as a whole has BG output-gates controlling which slots drive emission. Selection-by-disinhibition opens one input-gate at a time (serial/curriculum binding). Once slots are filled, a NON-SEPARABLE conjunction operator over the bound (role,filler) tuples produces the emitted structured frame. A slot emits only if its filler was gated from a supported source; otherwise it stays empty -> that role abstains. Loop: input->which-slot-to-update (disinhibition)->slot register update->cross-slot conjunction->gated frame emit.

## Satisfies criteria (DESIGN claim · DIRECTIONAL · unmeasured)

G1/binding/compositional-depth NATIVE: role-slot registers are the factored representation, gating BINDS (not chooses) — distinct fillers occupy distinct role slots, so any filler can bind any role = Fodor-Pylyshyn systematicity; composed_distinct over filled frames strictly exceeds max single-slot, and interaction-ablation (removing the cross-slot conjunction op) drops to the separable floor. falsifiable>=1 NATIVE: a frame is literally comparator-slot x quantity-slot x >=2 referent-slots = a world-partitioning proposition by construction. G2 novelty: novel role x filler combinations absent from data yet inside the slot-grammar manifold. Realization-invariant: binding sits ON the emit path (output-gate reads bound slots) and the emission objective is unreachable without filling the conjunction. Psi=1/2 via output-gate open/close opponency; honesty via empty-slot abstain.

## Not-LLM (a_no_llm_frame_trap)

Explicit symbolic role-slot registers with discrete GATED updates — variable binding is the architecture, not an emergent side-effect hoped for from scale. No attention over a context window; the lever is the gating POLICY (which slot updates when), not depth or parameter count. This is the structure-not-bolt-on answer to the persistent G1 recombination wall (clm303 lossF~0 yet recombine-fail).

## Cheap test (frozen-first · $0 · numpy mirror · DIRECTIONAL)

numpy: k role-slots, gate toy fillers; measure composed_distinct (joint) > max_single (per-slot) for G1; count novel role x filler combos absent from the toy corpus for G2; run interaction-ablation and confirm the conjunction score drops to the separable baseline; apply a judge-free falsifiable detector to emitted frames (count >=1). All bars frozen first.

## Engine-native measure (cost-gated · PRE-REGISTER ONLY · NOT fired)

Role-slots map to core/engine_cli.hexa SS-SelfIdentity/SS-WorkingMemory state-vector slots; conjunction op authored as a hexa bind; G1 via core/g_gates.hexa g_eval_g1 / _g_coverage on frame outputs; falsifiable via core/g6_ideation.hexa _g6_is_falsifiable; routed through cli/anima.hexa single dispatch so the measured transfer function == deployed. hexa+py byte-parity.

## Scope / honesty (c9)

## Distinction (near-overlap kept, not a dup)

Near-overlap with working_memory_buffer (H_1282) and basal_ganglia_gating (H_1281) — distinct: PBWM's principle is BG-gated role-slot REGISTERS for variable binding (gate WHAT enters WM, not the motor act); the explicit symbolic role-filler binding is the differentiator.

Binding / compositional-depth / falsifiable are the strongest axes (the closure-gap winner); the gating-policy learning is the open part.

설계만 — 측정 0. tier = 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL). frozen bar 사후 이동 금지(tune-to-green 금지, p7). 이 카드는 *방향성 설계*이지 검증된 결과가 아니다 — 과장 박제 금지(a_engine_native_learning). engine_native_measure 는 단일 진입점 cli/anima.hexa → generator L3 → g_gates/g6 경유 byte-parity 채점만 terminal; torch-only/side-harness 결과는 DIRECTIONAL. numpy cheap_test 결과도 DIRECTIONAL(엔진-네이티브 아님). gpu/engine 발사 시 held-out mirror-DESCENT(a_clm_gen_pipeline) + CORE mount frozen-bar engine-native 재측정 + ckpt PULL(a_fire_recover_complete).
