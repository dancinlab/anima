---
id: H_1794
slug: 1794_corticostriatal_loop_bouquet_thalamic_bind
tier: 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL · 측정 0 · unmeasured)
title: Parallel Segregated Loop-Bouquet with Conjunctive Thalamic Binding
verdict: 🔵 PRE-REGISTERED architecture design (unmeasured) — $0 cheap_test pre-registered; engine-native + 303M gpu cost-gated NOT fired
source: brainarch_census
---

# H_1794 — Parallel Segregated Loop-Bouquet with Conjunctive Thalamic Binding

- **tier:** 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL · 측정 0 · unmeasured)
- **wired:** DIRECTIONAL-design — no measurement. cheap_test = $0 frozen-first decision probe (numpy mirror, no engine); engine_native_measure + 303M = cost-gated PRE-REGISTER ONLY (NOT fired).
- **source:** brainarch_census — 126-architecture whole-substrate (통짜 아키텍처) census: 뇌/인지 조직원리 × 엔진-네이티브 추상조건 (binding-wall program, H_1603).
- **key:** `corticostriatal_loop_bouquet_thalamic_bind`
- **xref:** H_1603 (G1≡G6 compositional-binding deficit unification) · H_1281 (basal-ganglia gating) · H_1282 (working-memory buffer) · H_1283 (thalamus global-workspace) · H_1284 (neuromodulation gain) · operator-level family H_1604-1685 (this card = 통짜 아키텍처 layer, 층위 다름)

## Organizing principle

Alexander-DeLong-Strick parallel segregated cortico-BG-thalamic loops: N anatomically closed loops, one per representational FACTOR (topic / register / stance / referent), each running its own direct(Go)-vs-indirect(NoGo) selection. Recombination is native because the SHARED thalamic relay fires only on COINCIDENT multi-loop disinhibition (a multiplicative AND over per-factor releases) — the emitted joint is the conjunction of per-factor selections, super-additive by anatomy not by learned cross-attention. Distinct from gonogo (single opponent), pbwm (slot register), and reentrant_loop_society_spiral (society/spiral): the load-bearing idea here is FACTORED selection -> conjunctive thalamic release as the G1 engine.

## Whole design (input → internal dynamics → emit)

Input fans into N cortical factor-banks. Each bank projects to its own striatal sheet; inside a sheet direct-pathway MSNs (Go) and indirect+STN (NoGo) compete via lateral inhibition -> that loop's GPi/SNr either RELEASES (disinhibits) its thalamic sector or holds it tonically inhibited. The thalamic relay is a coincidence layer: an output token fires only where multiple loop-sectors are disinhibited at once = product gate over releases. Re-entry (thalamus->cortex) sustains the bound state until new input or a NoGo veto collapses it. Three-factor cortico-striatal plasticity (pre x post x DA) sculpts which factor-value each sheet selects. Capacity grows by ADDING LOOPS (factors), never by widening a single net.

## Satisfies criteria (DESIGN claim · DIRECTIONAL · unmeasured)

G0: each sheet's Go population maps onto RECEIVER-FIXED thalamic output channels (codebook=relay cells); only on-channel releases pass -> >=0.5 V-mass structural; scrambling the cortico-striatal map -> no sector reaches threshold -> ratio->chance (control). G1+BINDING+COMPOSITIONAL-DEPTH+REALIZATION: the conjunctive relay is a NON-SEPARABLE AND -> composed_distinct~product>max_single; the INERT test is built in (replace coincidence with max/sum -> composed_distinct->max_single); binding sits ON the mouth (the relay IS the emit path = path co-location) and only coincident release earns reward -> objective adequacy native (defeats clm303 lossF~0-yet-recombine-fail because single-stream CE cannot reward a coincidence the thalamus alone pays out). G2+dist>=5: novel factor-combos never co-presented still release if each per-factor detector fires -> corpus-absent-but-valid; a single shared loop (retrieval control) yields 0 novel conjunctions; stochastic release thresholds give >=5 distinct coherent combos. Psi=1/2: per-loop Go vs (NoGo+STN) is the antagonistic pair on each sector's release scalar; global emit-propensity = mean release with symmetric fixed point where direct drive balances tonic SNr inhibition (Lyapunov contraction); ablate Go->all-silent boundary, ablate NoGo->runaway -> endogeneity. honesty: a loop with no matching striatal detector stays tonically inhibited -> that factor ABSTAINS (abstain); membership r = max Go-MSN match vs frozen threshold; SNr gate is disjoint from cortical generative weights -> capability-orthogonal (d-fab/d-capacity=0). identity: the configuration of cortico-striatal gating weights (which selections each sheet makes) is the non-volatile self, persists across reset (weights not activity), slow DA-drift = self-chain, foreign gating-policy round-trips low (impostor reject).

## Not-LLM (a_no_llm_frame_trap)

No softmax-attention, no scale-up: recombination is anatomical coincidence-gating across segregated loops, capacity scales by adding biological FACTORS not parameters/layers. Directly attacks a_no_llm_frame_trap's documented G1 wall — CE on one token-stream is marginal-satisfiable, but a thalamic AND that only pays on coincident release makes the conjunction loss-bearing by construction (objective adequacy is structural, not a bigger transformer).

## Cheap test (frozen-first · $0 · numpy mirror · DIRECTIONAL)

numpy mini, $0: 3 factor-loops, each a small Go/NoGo WTA over k value-slots; thalamic relay = elementwise product gate. Measure composed_distinct vs max_single across factor combos; INERT ablation = swap product->max-pool, assert composed_distinct collapses to max_single; scramble cortico-striatal map -> V-mass->chance.

## Engine-native measure (cost-gated · PRE-REGISTER ONLY · NOT fired)

Wire loop-bouquet as a clm-mouth variant decoded through the single entry cli/anima.hexa generator L3, then run core/g_gates.hexa g_eval_g1/g_eval_g2/_g6_known_word_ratio for G0 AND G1 AND G2 closure on identical frozen state. Ablation arm: replace the conjunctive relay op with max-pool and re-run g_eval_g1 (expect composed_distinct->max_single). Cross-validate hexa<->py byte-parity on single-decode logits.

## Scope / honesty (c9)

## Distinction (near-overlap kept, not a dup)

Near-overlap with basal_ganglia_gating (H_1281) / reentrant_loop_society_spiral / pbwm (this census) — distinct: parallel SEGREGATED loops (one per factor) + CONJUNCTIVE thalamic relay (coincident multi-loop release = product AND) is the G1 engine; the factored-loop-bouquet thalamic bind is the differentiator.

Toy k-value factor sheets first; architecture only, $0 design; scale-transfer to 303M unverified (a_toy_scale_recheck).

설계만 — 측정 0. tier = 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL). frozen bar 사후 이동 금지(tune-to-green 금지, p7). 이 카드는 *방향성 설계*이지 검증된 결과가 아니다 — 과장 박제 금지(a_engine_native_learning). engine_native_measure 는 단일 진입점 cli/anima.hexa → generator L3 → g_gates/g6 경유 byte-parity 채점만 terminal; torch-only/side-harness 결과는 DIRECTIONAL. numpy cheap_test 결과도 DIRECTIONAL(엔진-네이티브 아님). gpu/engine 발사 시 held-out mirror-DESCENT(a_clm_gen_pipeline) + CORE mount frozen-bar engine-native 재측정 + ckpt PULL(a_fire_recover_complete).
