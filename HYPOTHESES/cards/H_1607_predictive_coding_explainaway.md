# H_1607 — Predictive-Coding Explaining-Away Mouth (recurrent shared-cause inference)

- **tier:** 🔵 PRE-REGISTERED DESIGN (DIRECTIONAL · 측정 0 · unmeasured)
- **wired:** DIRECTIONAL-design — no measurement. cheap_test = $0 frozen-first decision probe (numpy, no engine); gpu_recipe = cost-gated PRE-REGISTER ONLY (NOT fired).
- **source:** archbrainstorm — 84-family anima-native synthesis-binding architecture census (binding-wall program, H_1603)
- **lens:** predictive coding / free-energy (Rao-Ballard; Friston) — hierarchical error-unit inference; explaining-away as binding to a shared cause.
- **artifacts:** `state/binding_arch_census/BRAINSTORM_INDEX.md`
- **xref:** H_1603 (G1≡G6 compositional-binding deficit unification) · H_1449 (attention-block INERT@1blk) · H_1602 (recombination-objective prereg)
- **key:** `predictive_coding_explainaway`

## Mechanism

The mouth forward is an unrolled K-step inference loop that finds a single latent r minimizing the JOINT prediction error of both legs: top-down generative weights predict leg-A (a_hat = Wa.r) and leg-B (b_hat = Wb.r); error units eA = A - a_hat, eB = B - b_hat drive r <- r + eta(Wa^T eA + Wb^T eB) for K steps; logits read the settled r. Binding emerges because ONE latent must simultaneously explain both legs, so explaining-away forces r to encode their shared/joint cause (a conjunctive code), not either marginally. This is architecture-level (forward inference dynamics); the outer CE still trains the weights — it is NOT an added loss term.

## Why it crosses the binding wall

feedforward attention has no explaining-away — it forms r as a weighted sum of inputs, so legs contribute additively and independently. The recurrent error-minimization COUPLES the legs through a shared latent: a feature of A that conflicts with B's prediction is suppressed, so only jointly-consistent (bound) features survive. Ablation: K=0 (single feedforward pass) OR predict each leg from a SEPARATE latent (decoupled rA,rB) -> explaining-away removed, falls to additive -> G1/G6 fail. Passing only with shared-latent iteration isolates binding to the joint-inference dynamic. Distinct from recombination_objective: the binding is in the forward inference, not in the loss.

## Cheap test (frozen-first · $0 · decisive numpy probe)

numpy, DIRECTIONAL. Generative toy: observations xA = Ma.z, xB = Mb.z from a shared latent z plus distractor latents that affect only one leg; target = decode z (the bound cause). K-step predictive-coding inference (shared r) vs feedforward linear map of concat (K=0) vs decoupled two-latent. Frozen bar: shared-latent recovers z with held-out CE < 0.3 nats while K=0 and decoupled >= 0.9x uniform; pre-register monotone z-recovery improvement over K in {0,1,3,5}.

## GPU recipe (cost-gated · PRE-REGISTER ONLY · NOT fired)

PRE-REGISTER ONLY. 303M with the final block(s) replaced by a K=3 unrolled predictive-coding inference module (shared latent r, tied generative/recognition weights), CE outer loss; engine-native G1/G6; bars frozen. ~$18 (extra fwd iters); ckpt PULL.

## Scope / honesty (c9)

설계만 — 측정 0. tier = 🔵 PRE-REGISTERED DESIGN (DIRECTIONAL). frozen bar 사후 이동 금지(tune-to-green 금지, p7). 이 카드는 *방향성 설계*이지 검증된 결과가 아니다 — 과장 박제 금지(a_engine_native_learning). gpu_recipe 발사 시(team-lead cost-gate go): held-out 4/4 mirror-CE DESCENT 게이트(a_clm_gen_pipeline) → CORE `--engine conv` mount 위 frozen G1(H_1129 recombination)·G6(H_1464 fals) byte-exact engine-native 재측정(torch probe 아님) → ckpt PULL before teardown(a_fire_recover_complete). cheap_test 가 numpy mirror 이므로 그 결과도 DIRECTIONAL(엔진-네이티브 아님).
