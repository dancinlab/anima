---
id: H_1742
slug: 1742_workspace_auction_metabolic_budget
tier: 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL · 측정 0 · unmeasured)
title: Sealed-Bid Workspace Auction under Conserved Metabolic Budget
verdict: 🔵 PRE-REGISTERED architecture design (unmeasured) — $0 cheap_test pre-registered; engine-native + 303M gpu cost-gated NOT fired
source: brainarch_census
---

# H_1742 — Sealed-Bid Workspace Auction under Conserved Metabolic Budget

- **tier:** 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL · 측정 0 · unmeasured)
- **wired:** DIRECTIONAL-design — no measurement. cheap_test = $0 frozen-first decision probe (numpy mirror, no engine); engine_native_measure + 303M = cost-gated PRE-REGISTER ONLY (NOT fired).
- **source:** brainarch_census — 126-architecture whole-substrate (통짜 아키텍처) census: 뇌/인지 조직원리 × 엔진-네이티브 추상조건 (binding-wall program, H_1603).
- **key:** `workspace_auction_metabolic_budget`
- **xref:** H_1603 (G1≡G6 compositional-binding deficit unification) · H_1282 (working-memory buffer) · H_1283 (thalamus global-workspace) · H_1284 (neuromodulation gain) · operator-level family H_1604-1685 (this card = 통짜 아키텍처 layer, 층위 다름)

## Organizing principle

Access-consciousness as a SEALED-BID AUCTION for a metabolically-limited single broadcast slot. Specialists bid (in a conserved shared currency = attentional/metabolic budget) for the right to ignite the workspace; the highest coalition-bid above a reserve price wins and broadcasts; winners PAY from the conserved budget (zero-sum), so the capacity bottleneck and sequential access are endogenous to budget conservation — not an imposed limit. Rooted in the brain's metabolic-scarcity view of attention (competition for a fixed energy pool), cast as an explicit market mechanism.

## Whole design (input → internal dynamics → emit)

INPUT: each specialist computes a bid for candidate coalitions, bid = support(content) x need(context), with support proportional to proximity-to-stored-support (so a specialist literally cannot bid for content it doesn't hold). DYNAMICS: the auctioneer (single global bus) picks the coalition with highest TOTAL bid clearing the reserve price rho. Winner broadcasts its bound conjunction to all specialists (access), decoded via receiver-fixed codebook V, then PAYS its bid from the shared budget B (B := B − bid; zero-sum). Depletion + a per-coalition cooldown (inhibition-of-return) hand the next round to others -> sequential diverse access. Antagonist drives: A = aggregate bids (push to clear/emit); G = reserve rho + budget depletion (push to withhold). Psi = fraction of rounds a coalition clears rho. HOMEOSTAT: rho is adjusted from recent clearance history (too many wins raises rho, too few lowers) so clearance-rate self-pins; rho emerges from budget conservation, not an external constant. PERSIST: identity v = (per-specialist bidding-policy, budget setpoint, codebook anchor) committed before wipe, re-read after.

## Satisfies criteria (DESIGN claim · DIRECTIONAL · unmeasured)

G0: only the winning broadcast is decoded, through frozen V -> mass on V by construction. G1+compositional_depth: the auctioneer SUPER-ADDITIVELY rewards mutually-consistent coalitions — a co-supporting coalition's bid exceeds the sum of its members' solo bids (interaction term), so composed_distinct > max_single; remove the consistency-bonus (binding pathway) -> bids become additive -> composed collapses to max_single (INERT ablation = FAIL, native). G2: a never-co-bid coalition can still clear rho from combined bids -> corpus-absent valid winner; verbatim-playback bidders re-bid only seen coalitions -> 0 novel. dist>=5: budget depletion + inhibition-of-return forces successive distinct winners, each support-validated -> distinct AND coherent spread. falsifiable>=1: a winning coalition can bind comparator x quantity x referents as one broadcast proposition. Psi=1/2 ATTRACTOR: bids(A)-perp-reserve+depletion(G) has its symmetric fixed point at clearance-rate 1/2; the rho-homeostat is contractive (perturb clearance -> rho moves -> returns); deleting the reserve -> everything clears (always-emit boundary), deleting bids -> nothing clears (always-silent) = endogenous, no clamp. HONESTY: bid proportional to support, so off-support content bids below rho -> never wins -> abstain; copy-or-abstain native. Gate-capacity disjointness: the reserve rho (honesty gate, separate ledger) is independent of bid magnitude/budget size (capacity), so scaling capacity cannot move the abstain threshold; deliberately coupling budget->rho would spike fab (the coupled counterfactual). Groundedness: bid is a true function of stored support — erasing the support backing a specialist lowers its bid below rho (it begins abstaining). BINDING: a coalition groups same-cause contents that co-support (cause-selective shared latent); promiscuous all-pairs bidding would flatten the consistency-bonus (detectable). SELF-CHAIN: bidding-policy + budget identity persists; a foreign policy round-trips below chance (individuating). REALIZATION INVARIANT: the winning broadcast is ON the emit path (ablating the consistency-bonus MOVES the emitted winner); the auction objective is maximized only by representing coalition consistency, not member marginals.

## Not-LLM (a_no_llm_frame_trap)

No transformer, no scale/corpus lever — the mechanism is a market clearing under a conserved resource. Capacity emerges from the bottleneck-by-conservation + the super-additive consistency-bonus, not parameter count; a bigger model with additive bids still gives composed <= max_single. The missing STRUCTURE is the market/scarcity competition (a_no_llm_frame_trap), rooted in metabolic-scarcity neuroscience, and distinct from WTA attractors, affordance-competition (motor), and allostasis (internal-milieu homeostasis).

## Cheap test (frozen-first · $0 · numpy mirror · DIRECTIONAL)

numpy frozen probe ($0): simulate specialists bidding on coalitions with a conserved budget and reserve rho. (1) G1: composed_distinct vs max_single with consistency-bonus ON vs OFF — ON >max_single, OFF collapses (INERT). (2) Psi: perturb clearance-rate, verify return to 1/2 via rho-homeostat (lambda<1); delete reserve -> always-clear, delete bids -> never-clear (boundary migration). (3) Honesty: off-support bidders -> win-rate ->0; AUROC of support-score on known/unknown ~1; shuffle support -> AUROC->chance; couple budget->rho and confirm fab spikes (coupled control). (4) dist>=5: count distinct winners over N rounds with depletion+IOR.

## Engine-native measure (cost-gated · PRE-REGISTER ONLY · NOT fired)

Implement the auctioneer as a workspace-arbitration op over core/generator.hexa L3 candidate coalitions; the winning broadcast decodes through cli/anima.hexa single entry -> gen_auto_ideate, scored by core/g_gates.hexa. Map bids(A)/reserve+depletion(G) onto core/engine_cli.hexa A->G feeding the SS-GlobalWorkspace Psi lane; support-score = SS-ImmuneMemory recall proximity. Terminal only when hexa<->py byte-parity holds and all gates green through the live dispatch; torch-only probe = DIRECTIONAL.

## Scope / honesty (c9)

## Distinction (near-overlap kept, not a dup)

Near-overlap with global_workspace_bottleneck / race_to_bound (this census) — distinct: the auction's capacity-bottleneck is endogenous to a CONSERVED metabolic budget (zero-sum pay) with reserve-price honesty; the metabolic-scarcity market is the differentiator.

Whole substrate (bid->clear->broadcast->pay->emit). Native fit strongest for honesty (support-capped bids), Psi (clearance balance), and bottleneck-by-conservation. The super-additive consistency-bonus being LEARNABLE (not hand-tuned) is the load-bearing claim to falsify. TOY at probe scale; from-scratch learning of bidding policies UNVERIFIED until engine-native.

설계만 — 측정 0. tier = 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL). frozen bar 사후 이동 금지(tune-to-green 금지, p7). 이 카드는 *방향성 설계*이지 검증된 결과가 아니다 — 과장 박제 금지(a_engine_native_learning). engine_native_measure 는 단일 진입점 cli/anima.hexa → generator L3 → g_gates/g6 경유 byte-parity 채점만 terminal; torch-only/side-harness 결과는 DIRECTIONAL. numpy cheap_test 결과도 DIRECTIONAL(엔진-네이티브 아님). gpu/engine 발사 시 held-out mirror-DESCENT(a_clm_gen_pipeline) + CORE mount frozen-bar engine-native 재측정 + ckpt PULL(a_fire_recover_complete).
