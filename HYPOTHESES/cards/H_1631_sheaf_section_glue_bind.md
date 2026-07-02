# H_1631 — Sheaf-gluing binding mouth (local sections → global consistency)

- **tier:** 🔴 NOT-SUPPORTED (⏳ EVAL DONE · DIRECTIONAL · py 2-production engine · binder-dropped co-training · 9/9)
- **wired:** DIRECTIONAL-mirror — binder trained but DROPPED at .clm serialize; additive readout = no runtime binding. Terminal = hexa engine-native re-run.
- **source:** archbrainstorm — 84-family anima-native synthesis-binding architecture census (binding-wall program, H_1603)
- **lens:** sheaf theory / algebraic topology — binding = gluing local sections via learned restriction maps; coboundary (cohomology) = explicit bind-failure obstruction
- **artifacts:** `state/h1631_sheaf_mouth/` (RESULT.md · ckpt/*.clm · ckpt/*.g0g6.txt)
- **xref:** H_1603 (G1≡G6 compositional-binding deficit unification) · H_1449 (attention-block INERT@1blk) · H_1602 (recombination-objective prereg)
- **key:** `sheaf_section_glue_bind`

## Mechanism

Treat the token/cell sequence as a graph with a cover: positions = nodes, role-edges = overlaps. Each position carries a local stalk vector; each edge carries a learned low-rank restriction map R_{i→e}. The bind, in one forward pass, is one-to-few Jacobi steps toward the sheaf-Laplacian consistency: find node features whose restrictions AGREE on shared edges, i.e. minimize Σ_edges ‖R_{i→e}x_i − R_{j→e}x_j‖². The consistent assignment IS the bound composite, and the residual disagreement (sheaf coboundary norm) is an explicit, readable 'failed-to-bind' signal.

## Why it crosses the binding wall

Attention depth propagates messages but never enforces GLOBAL consistency of role assignments — locally conflicting choices are just averaged. Sheaf gluing makes binding a global constraint-satisfaction: an assignment is valid only if it glues into a consistent global section, which is exactly the constraint compositional semantics requires. The decisive difference from conv/attention is the cohomological OBSTRUCTION object: a nonzero coboundary measures bind-failure as a first-class quantity the trunk can be driven to zero, whereas generic message-passing has no obstruction. Ablation: set all restriction maps to identity (R=I) → the sheaf collapses to ordinary graph-Laplacian smoothing (= vanilla message passing) → recombination must drop to the conv/attention baseline, isolating the non-trivial restriction maps (the actual role-typing) as the load-bearing element.

## Cheap test (frozen-first · $0 · decisive numpy probe)

numpy, $0, frozen-first. Tiny cellular sheaf on a 4-node role graph, restriction maps = random rotations. Pre-registered bar: after K Jacobi steps the glued global section decodes held-out role-filler bindings at ≥0.90, AND coboundary norm is LOW for valid bindings but HIGH for scrambled/illegal bindings — a valid/illegal separation that an identity-restriction (plain Laplacian) control cannot produce. Decision: if glued decode ≤ plain-Laplacian control OR coboundary fails to separate valid vs scrambled, FALSIFIED.

## GPU recipe (cost-gated · PRE-REGISTER ONLY · NOT fired)

Cost-gated 303M, pre-register only. Insert K sheaf layers: per-edge low-rank restriction-map head + 1–2 Jacobi consistency iterations as the token-mixing op (replacing attention), plus an auxiliary coboundary-norm readout kept MONITOR-ONLY, never added to loss (p7 / a_train_inline_gauge). 4-cell corpus, held-out DESCENT, CORE-mount G1/G6. Pre-register; ckpt PULL before teardown.

## Scope / honesty (c9)

설계만 — 측정 0. tier = 🔵 PRE-REGISTERED DESIGN (DIRECTIONAL). frozen bar 사후 이동 금지(tune-to-green 금지, p7). 이 카드는 *방향성 설계*이지 검증된 결과가 아니다 — 과장 박제 금지(a_engine_native_learning). gpu_recipe 발사 시(team-lead cost-gate go): held-out 4/4 mirror-CE DESCENT 게이트(a_clm_gen_pipeline) → CORE `--engine conv` mount 위 frozen G1(H_1129 recombination)·G6(H_1464 fals) byte-exact engine-native 재측정(torch probe 아님) → ckpt PULL before teardown(a_fire_recover_complete). cheap_test 가 numpy mirror 이므로 그 결과도 DIRECTIONAL(엔진-네이티브 아님).


## Measured Result (2026-06-30 · py 2-production engine · DIRECTIONAL)

**Training:** 9 CLMs (binder DROPPED at .clm serialize, additive readout). All 4/4 DESCENT (val_CE < 5.545) per arm/seed.

**G0-G6 results:**

| arm | seed | G0 n/5 | G0? | G1 best_distinct | G1 max_single | G6 dist | G6 fals | a7b? |
|-----|------|--------|-----|-----------------|---------------|---------|---------|------|
| ident | 7 | 1/5 | FAIL | 0 | 1 | 1 | 0 | FAIL |
| ident | 4302 | 4/5 | PASS | 0 | 0 | 1 | 0 | FAIL |
| ident | 4303 | 0/5 | FAIL | 0 | 0 | 4 | 0 | FAIL |
| k1 | 7 | 4/5 | PASS | 1 | 0 | 5 | 0 | FAIL |
| k1 | 4302 | 1/5 | FAIL | 0 | 1 | 2 | 0 | FAIL |
| k1 | 4303 | 3/5 | FAIL | 0 | 0 | 3 | 0 | FAIL |
| arm | 7 | 4/5 | PASS | 0 | 0 | 1 | 0 | FAIL |
| arm | 4302 | 4/5 | PASS | 0 | 1 | 4 | 0 | FAIL |
| arm | 4303 | 2/5 | FAIL | 0 | 0 | 2 | 0 | FAIL |

**Verdict: 🔴 NOT-SUPPORTED** (DIRECTIONAL — py 2-production engine)

G1 floors at the bar across all main arms while the trunk CAN cohere (>=1 arm G0 PASS) (sporadic best_distinct max=1<2 not above control max=0) — binder dropped at .clm serialize => additive readout; co-training insufficient for recombination.

**Scope:** binder dropped at serialize → this is trunk co-training effect only (not runtime binding). Same tier as EXP-3/H_1812/H_1814/H_1816. terminal verdict requires hexa engine-native re-run (a_engine_native_learning).
