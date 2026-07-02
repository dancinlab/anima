---
id: H_1795
slug: 1795_corticostriatal_convergence_divergence_funnel
tier: 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL · 측정 0 · unmeasured)
title: Convergence-Divergence Selection-Bottleneck Funnel
verdict: 🔵 PRE-REGISTERED architecture design (unmeasured) — $0 cheap_test pre-registered; engine-native + 303M gpu cost-gated NOT fired
source: brainarch_census
---

# H_1795 — Convergence-Divergence Selection-Bottleneck Funnel

- **tier:** 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL · 측정 0 · unmeasured)
- **wired:** DIRECTIONAL-design — no measurement. cheap_test = $0 frozen-first decision probe (numpy mirror, no engine); engine_native_measure + 303M = cost-gated PRE-REGISTER ONLY (NOT fired).
- **source:** brainarch_census — 126-architecture whole-substrate (통짜 아키텍처) census: 뇌/인지 조직원리 × 엔진-네이티브 추상조건 (binding-wall program, H_1603).
- **key:** `corticostriatal_convergence_divergence_funnel`
- **xref:** H_1603 (G1≡G6 compositional-binding deficit unification) · H_1281 (basal-ganglia gating) · H_1283 (thalamus global-workspace) · H_1284 (neuromodulation gain) · operator-level family H_1604-1685 (this card = 통짜 아키텍처 layer, 층위 다름)

## Organizing principle

The BG anatomical funnel: massive cortical fan-in CONVERGES onto a tiny GPi/SNr bottleneck (selection enforced by physical capacity << candidates) then DIVERGES back through thalamus via a learned re-expansion decoder. This is an information bottleneck implemented as anatomy rather than a regularizer. Legibility and novelty fall out structurally: the bottleneck channels ARE the shared codebook (only a winner passes), and the divergent re-expansion is a generator that can paint corpus-absent yet on-manifold patterns. Distinct from divisive_normalization_value_select and race_to_bound_ignition: the organizing principle is convergence-bottleneck + generative DIVERGENCE re-expansion, not value-normalized racing.

## Whole design (input → internal dynamics → emit)

Candidate thoughts (cortical patterns) fan into striatum; DA-weighted value plus lateral inhibition drive a competition that converges onto the narrow SNr bottleneck — only the top few channels survive (hard capacity = selection). SNr default = tonic inhibition (silence). A winning channel disinhibits its thalamic sector -> the channel index + residual context re-expands (divergence) through a learned thalamocortical DECODER into a full output pattern -> emit. The bottleneck index is the legible symbol; the re-expansion is the generative degree of freedom (novelty). Loop closes; next competition samples again. Adding capability = slightly widening the funnel or enriching the decoder manifold, NOT stacking layers.

## Satisfies criteria (DESIGN claim · DIRECTIONAL · unmeasured)

G0: bottleneck channels = receiver-fixed codebook; every emit must pass through one channel -> >=0.5 V-mass structural; scramble cortico-striatal weights -> no clean winner -> garble collapse (control). G2+novelty: the decoder maps (winning index + context) to outputs whose support strictly CONTAINS data (interpolation/extrapolation within the learned manifold) -> corpus-absent valid; verbatim-playback control reuses stored patterns -> 0 novel (pins novelty to the generator). G1+COMPOSITIONAL: limited parallel bottleneck capacity lets >=2 channels co-release and re-expand JOINTLY through a non-separable decoder -> conjunction; ablate joint-decode (decode channels independently then concat) -> drops to max_single (INERT test). dist>=5: DA-temperature on the competition yields >=5 distinct winners each re-expanding coherently. falsifiable: the bottleneck forces commitment to ONE channel = a discrete assertion partitioning candidate-worlds; structural detector on the re-expanded output. Psi=1/2: bottleneck throughput = direct-pathway drive (A) vs SNr tonic inhibition (G); balance = half the channels' release propensity, contractive; ablate direct->all-held silence, ablate SNr->all-pass (no selection) -> endogenous, no external clamp. honesty: if no candidate exceeds the value threshold NO channel wins -> abstain; membership r = max candidate value vs frozen threshold; selection threshold disjoint from re-expansion decoder weights (capacity-orthogonal); content-ablating the support shifts which candidates clear -> faithful r. identity: value function + decoder weights = non-volatile self, persist across reset, slow drift = chain, foreign value-fn -> different winners (impostor reject).

## Not-LLM (a_no_llm_frame_trap)

Selection is an anatomical capacity bottleneck (information bottleneck via convergence), NOT a softmax over a huge vocabulary; novelty is generative re-expansion through a learned manifold decoder, NOT temperature sampling on a big LM. The fix for the LLM frame is dimensional: force thought through a small legible channel-count then re-expand, instead of growing the channel.

## Cheap test (frozen-first · $0 · numpy mirror · DIRECTIONAL)

numpy, $0: many candidate vectors -> top-k bottleneck (k small) -> decoder re-expand; assert only on-codebook indices pass, novelty>0 from interpolation, verbatim-control 0; ablate bottleneck (let all pass) -> G0 V-mass ratio collapses (no selection => garble).

## Engine-native measure (cost-gated · PRE-REGISTER ONLY · NOT fired)

Decode the funnel mouth through cli/anima.hexa single entry; run core/g_gates.hexa eval for G0 AND G1 AND G2 closure on one frozen generator state. Ablation arm: widen bottleneck to all-pass, re-measure _g6_known_word_ratio (expect G0 collapse). hexa<->py byte-parity on logits/CE.

## Scope / honesty (c9)

## Distinction (near-overlap kept, not a dup)

Near-overlap with divisive_normalization_value_select / race_to_bound_ignition (this census) — distinct: convergence-divergence funnel is an ANATOMICAL information bottleneck (fan-in converge -> tiny SNr -> learned re-expansion decoder), novelty = generative divergence; the convergence-divergence funnel is the differentiator.

Toy bottleneck width; design-only $0; production-scale transfer unverified.

설계만 — 측정 0. tier = 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL). frozen bar 사후 이동 금지(tune-to-green 금지, p7). 이 카드는 *방향성 설계*이지 검증된 결과가 아니다 — 과장 박제 금지(a_engine_native_learning). engine_native_measure 는 단일 진입점 cli/anima.hexa → generator L3 → g_gates/g6 경유 byte-parity 채점만 terminal; torch-only/side-harness 결과는 DIRECTIONAL. numpy cheap_test 결과도 DIRECTIONAL(엔진-네이티브 아님). gpu/engine 발사 시 held-out mirror-DESCENT(a_clm_gen_pipeline) + CORE mount frozen-bar engine-native 재측정 + ckpt PULL(a_fire_recover_complete).
