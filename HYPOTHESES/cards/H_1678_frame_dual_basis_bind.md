# H_1678 — Biorthogonal reciprocal-frame mouth (overcomplete dual-basis binding)

- **tier:** 🔵 PRE-REGISTERED DESIGN (DIRECTIONAL · 측정 0 · unmeasured)
- **wired:** DIRECTIONAL-design — no measurement. cheap_test = $0 frozen-first decision probe (numpy, no engine); gpu_recipe = cost-gated PRE-REGISTER ONLY (NOT fired).
- **source:** archbrainstorm — 84-family anima-native synthesis-binding architecture census (binding-wall program, H_1603)
- **lens:** FORMAL-algebraic -- frame theory / biorthogonal reciprocal (dual) basis, overcomplete-redundancy capacity
- **artifacts:** `state/binding_arch_census/BRAINSTORM_INDEX.md`
- **xref:** H_1603 (G1≡G6 compositional-binding deficit unification) · H_1449 (attention-block INERT@1blk) · H_1602 (recombination-objective prereg) · H_1466 (TPR binder), H_1514 (VSA/HRR binding)
- **key:** `frame_dual_basis_bind`

## Mechanism

Roles are an OVERCOMPLETE FRAME {r_k} (more roles than dimensions, redundant, NON-orthonormal). Bind = Sum_k r_k (x) f_k (outer-product superposition, like TPR but with frame roles). Unbind for role-j = contract the bound matrix with the DUAL/reciprocal frame vector r~_j (biorthogonal partner satisfying <r~_j, r_k> = delta_jk), precomputed as the pseudo-inverse of the frame. Single forward: a fixed dual-frame matrix turns the bound tensor back into the filler. Trunk emits coefficients in the frame; layer holds the precomputed reciprocal frame.

## Why it crosses the binding wall

TPR (tpr_outer_bind) requires ORTHONORMAL roles -> capacity hard-capped at dimension d (only d clean role-filler pairs); generic attention has no exactness guarantee at all. A tight/overcomplete frame with dual-basis unbinding packs N>>d role-filler pairs with bounded crosstalk (frame redundancy), so recombination capacity scales PAST the orthonormal ceiling -- the binding wall may be a CAPACITY wall that orthonormal binding cannot clear but overcomplete biorthogonal binding can. Distinct from tpr_outer_bind (orthonormal) and resonator_factorize (iterative factorization of a fixed product): the mechanism here is frame redundancy + reciprocal-dual readout. ABLATION: force roles orthonormal (collapse frame to basis) -> capacity caps at d, recombination of the (d+1)-th novel pair fails; use frame roles but unbind with transpose instead of dual frame -> crosstalk explodes (the reciprocal/biorthogonal dual is load-bearing).

## Cheap test (frozen-first · $0 · decisive numpy probe)

numpy $0, <1min. d=64, overcomplete frame of N=256 roles (random + tight-frame normalization); compute dual frame (pseudo-inverse). Bind 200 role-filler pairs (N>d), unbind all via dual frame. FROZEN bars: (a) dual-frame recovery accuracy on the 200 (>d) pairs >=0.9 vs (b) orthonormal-basis control capped at 64 then degrading, and (c) transpose-instead-of-dual control crosstalk high. Frame+dual clears >d pairs while orthonormal control caps at d => overcompleteness crosses the capacity wall.

## GPU recipe (cost-gated · PRE-REGISTER ONLY · NOT fired)

PRE-REGISTERED ONLY, cost-gated ~1 H100-day. 303M mouth: role embeddings as a learned overcomplete frame (N roles, N > d_head), a fixed/periodically-refreshed reciprocal-frame readout (pseudo-inverse). Bind via outer-superposition per head, read via dual frame. Train 4-cell. Accept iff engine-native (cli/anima.hexa eval) G6 fals>0 AND G1 recombination >= baseline AND distinct recoverable pairs > d. ckpt PULL.

## Scope / honesty (c9)

설계만 — 측정 0. tier = 🔵 PRE-REGISTERED DESIGN (DIRECTIONAL). frozen bar 사후 이동 금지(tune-to-green 금지, p7). 이 카드는 *방향성 설계*이지 검증된 결과가 아니다 — 과장 박제 금지(a_engine_native_learning). gpu_recipe 발사 시(team-lead cost-gate go): held-out 4/4 mirror-CE DESCENT 게이트(a_clm_gen_pipeline) → CORE `--engine conv` mount 위 frozen G1(H_1129 recombination)·G6(H_1464 fals) byte-exact engine-native 재측정(torch probe 아님) → ckpt PULL before teardown(a_fire_recover_complete). cheap_test 가 numpy mirror 이므로 그 결과도 DIRECTIONAL(엔진-네이티브 아님).
