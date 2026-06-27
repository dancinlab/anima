# H_1671 — Sum-product belief-propagation factor-consensus binding

- **tier:** 🔵 PRE-REGISTERED DESIGN (DIRECTIONAL · 측정 0 · unmeasured)
- **wired:** DIRECTIONAL-design — no measurement. cheap_test = $0 frozen-first decision probe (numpy, no engine); gpu_recipe = cost-gated PRE-REGISTER ONLY (NOT fired).
- **source:** archbrainstorm — 84-family anima-native synthesis-binding architecture census (binding-wall program, H_1603)
- **lens:** probabilistic graphical models / sum-product message-passing inference dynamics
- **artifacts:** `state/binding_arch_census/BRAINSTORM_INDEX.md`
- **xref:** H_1603 (G1≡G6 compositional-binding deficit unification) · H_1449 (attention-block INERT@1blk) · H_1602 (recombination-objective prereg)
- **key:** `belief_propagation_factor_consensus_bind`

## Mechanism

Mouth forward = sum-product belief propagation iterated to a fixed point on a small factor graph. Variable nodes = the two legs' latent assignments (content-variable: which content; role-variable: which role); factor nodes = learned compatibility potentials. Iterate log-domain messages content->factor->role and back, each a softmax-normalized product of incoming messages times the factor potential. The bound representation = converged marginal (belief) at a dedicated conjunction variable linked to both legs by a TERNARY consistency factor high only for consistent (content,role,bound) triples. The sum in sum-product marginalizes out alternatives so the surviving belief is the consistent joint assignment.

## Why it crosses the binding wall

Differs from energy descent (no scalar-gradient minimization) and from attention's continuous averaging: BP performs explicit MARGINALIZATION/inference over discrete pairings, which softmax averaging cannot do (it cannot integrate out alternatives nor enforce a factor potential). The ternary consistency factor IS the binding operator: a (content,role) pair yields high belief only if their joint potential is high. Ablation: make the factor potential separable/uniform (no cross-leg coupling) -> messages decouple, belief = product of independent marginals = no binding (FAIL); restore coupled potential -> joint belief sharpens. Second ablation: 1 message pass (no consensus) matches depth-only FAIL — isolates that iterated consensus, not the parameter count, is causal. Distinct from predictive_coding_explainaway (lateral marginalization vs hierarchical error suppression).

## Cheap test (frozen-first · $0 · decisive numpy probe)

numpy, $0. Factor graph with known coupled compatibility matrix + ambiguous unary evidence on both legs (each leg alone ambiguous; only the joint factor disambiguates). Full sum-product BP to convergence vs (i) separable factor (ii) single pass. Pre-register: full BP joint-assignment accuracy>=0.9 where unary-only/separable/single-pass are at chance; message-residual converges. Dose-response: increasing factor coupling strength monotonically raises joint accuracy — falsified if flat.

## GPU recipe (cost-gated · PRE-REGISTER ONLY · NOT fired)

PRE-REGISTERED ONLY (cost-gated, user-go). 303M custom mouth: differentiable BP binding head (learned factor potentials, K=5 sum-product iterations, log-domain messages) over conv-trunk content stream + attention role stream; converged conjunction-belief feeds the output head. Loss = next-byte (+ optional consistency aux). Clean 4-cell corpus, held-out CE-descent gate + engine-native G1/G6 on CORE conv; ckpt PULL before teardown.

## Scope / honesty (c9)

설계만 — 측정 0. tier = 🔵 PRE-REGISTERED DESIGN (DIRECTIONAL). frozen bar 사후 이동 금지(tune-to-green 금지, p7). 이 카드는 *방향성 설계*이지 검증된 결과가 아니다 — 과장 박제 금지(a_engine_native_learning). gpu_recipe 발사 시(team-lead cost-gate go): held-out 4/4 mirror-CE DESCENT 게이트(a_clm_gen_pipeline) → CORE `--engine conv` mount 위 frozen G1(H_1129 recombination)·G6(H_1464 fals) byte-exact engine-native 재측정(torch probe 아님) → ckpt PULL before teardown(a_fire_recover_complete). cheap_test 가 numpy mirror 이므로 그 결과도 DIRECTIONAL(엔진-네이티브 아님).
