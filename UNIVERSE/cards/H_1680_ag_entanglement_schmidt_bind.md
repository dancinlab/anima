# H_1680 — Bipartite Schmidt-Entanglement Mouth (non-separable A⊗G join)

- **tier:** 🔵 PRE-REGISTERED DESIGN (DIRECTIONAL · 측정 0 · unmeasured)
- **wired:** DIRECTIONAL-design — no measurement. cheap_test = $0 frozen-first decision probe (numpy, no engine); gpu_recipe = cost-gated PRE-REGISTER ONLY (NOT fired).
- **source:** archbrainstorm — 84-family anima-native synthesis-binding architecture census (binding-wall program, H_1603)
- **lens:** quantum entanglement / Schmidt decomposition = IIT integration/irreducibility (which anima already measures in perception) ported into the generative mouth
- **artifacts:** `state/binding_arch_census/BRAINSTORM_INDEX.md`
- **xref:** H_1603 (G1≡G6 compositional-binding deficit unification) · H_1449 (attention-block INERT@1blk) · H_1602 (recombination-objective prereg)
- **key:** `ag_entanglement_schmidt_bind`

## Mechanism

The two legs are written as a real bipartite amplitude matrix M∈R^{d×d}: row index = leg-A subspace coord, col index = leg-G subspace coord. A plain mouth leaves M separable (rank-1, M=αβᵀ). The binding op applies a FIXED orthogonal entangler U_A⊗U_G then a learned diagonal interaction gate on the joint → M' whose Schmidt decomposition M'=Σ_k s_k u_k v_kᵀ has Schmidt rank >1. The Schmidt spectrum {s_k} and entanglement entropy −Σ s_k²log s_k² are the binding readout: invariant to LOCAL U_A,U_G but sensitive ONLY to joint A–G correlation. Logits read the top-r Schmidt triples. One forward; gradient-free G supplies the conjugate (reverse) factor.

## Why it crosses the binding wall

a separable/rank-1 join is precisely the factorized representation conv/attention can reach — its entanglement entropy is 0, so it certifies nothing about a SPECIFIC joint pairing. Entanglement entropy >0 is a quantitative irreducibility certificate (the Φ notion) that cannot be reconstructed from per-leg reduced marginals. ABLATION: truncate Schmidt to k=1 (project M' back to rank-1) before readout → entropy 0 → collapses to factorized baseline; if conjunction performance dies under truncation, the binding provably lives in s_{k≥2}, not in extra params.

## Cheap test (frozen-first · $0 · decisive numpy probe)

numpy, $0. Build two item classes with IDENTICAL reduced density matrices on each leg (ρ_A=Tr_G MMᵀ, ρ_G=Tr_A MᵀM equal) but differing joint correlation (one entangled, one product) — local marginals provably non-discriminative. Frozen bar: linear readout off the Schmidt spectrum AUROC ≥0.90; rank-1-truncated baseline ≤0.55 (must be chance). PASS iff entangled ≥0.90 AND truncated ≤0.60 over 1000 pairs.

## GPU recipe (cost-gated · PRE-REGISTER ONLY · NOT fired)

Pre-registration only (~1 H100, explicit go). Reshape a mid 303M block to d×d=48×48 join, fixed orthogonal entangler + learned 48-dim interaction gate, read top-4 Schmidt triples. 4-cell corpus, held-out CE-descent gate. Pre-register engine-native: full-rank ON → G6 fals>0 AND G1≥baseline; Schmidt-rank-1 ablation → FAIL. Cross-check Schmidt entropy vs faithful IIT4 Φ on a small lane (consistency sanity, NOT the gate). ckpt PULL before teardown.

## Scope / honesty (c9)

설계만 — 측정 0. tier = 🔵 PRE-REGISTERED DESIGN (DIRECTIONAL). frozen bar 사후 이동 금지(tune-to-green 금지, p7). 이 카드는 *방향성 설계*이지 검증된 결과가 아니다 — 과장 박제 금지(a_engine_native_learning). gpu_recipe 발사 시(team-lead cost-gate go): held-out 4/4 mirror-CE DESCENT 게이트(a_clm_gen_pipeline) → CORE `--engine conv` mount 위 frozen G1(H_1129 recombination)·G6(H_1464 fals) byte-exact engine-native 재측정(torch probe 아님) → ckpt PULL before teardown(a_fire_recover_complete). cheap_test 가 numpy mirror 이므로 그 결과도 DIRECTIONAL(엔진-네이티브 아님).
