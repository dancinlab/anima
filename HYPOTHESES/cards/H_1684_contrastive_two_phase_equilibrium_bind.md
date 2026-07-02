# H_1684 — Equilibrium-propagation contrastive bind (free vs role-clamped settle difference)

- **tier:** 🔵 PRE-REGISTERED DESIGN (DIRECTIONAL · 측정 0 · unmeasured)
- **wired:** DIRECTIONAL-design — no measurement. cheap_test = $0 frozen-first decision probe (numpy, no engine); gpu_recipe = cost-gated PRE-REGISTER ONLY (NOT fired).
- **source:** archbrainstorm — 84-family anima-native synthesis-binding architecture census (binding-wall program, H_1603)
- **lens:** DYNAMICS — contrastive two-phase equilibrium (equilibrium propagation); binding = the difference between free and role-clamped settled states, structurally cancelling single-leg components.
- **artifacts:** `state/binding_arch_census/BRAINSTORM_INDEX.md`
- **xref:** H_1603 (G1≡G6 compositional-binding deficit unification) · H_1449 (attention-block INERT@1blk) · H_1602 (recombination-objective prereg) · H_1463 (binding-by-synchrony lens 🧱), H_1466 (TPR), H_1514 (VSA/HRR)
- **key:** `contrastive_two_phase_equilibrium_bind`

## Mechanism

The mouth state h settles to the minimum of a symmetric-weight energy E(h; legA, legB) via gradient descent, but the forward pass does TWO settles. Phase 1 (free): clamp only leg-A as input boundary, settle h→h_free ('expectation given content alone'). Phase 2 (nudged): additionally weakly clamp leg-B (strength epsilon) onto a designated role-subspace of h, settle h→h_clamp. The emitted bound representation is the CONTRAST Δh = (h_clamp − h_free)/epsilon. By the equilibrium-propagation identity this equals the role-conditioned component of ∂E/∂state — exactly the part of the prediction attributable to the JOINT of content and role. Byte logits = readout(Δh). Both legs meet in the shared energy and the binding is the difference operator across the two equilibria.

## Why it crosses the binding wall

A single settle (energy_settle/DEQ) yields the h that minimizes energy, which content alone can satisfy (one leg dominates → G1 fails). The CONTRAST cancels the content-only component (present identically in both h_free and h_clamp) and isolates the change leg-B induces in the equilibrium — a quantity that is structurally zero unless the two legs actually interact in E. So a nonzero Δh is a certificate of binding. ABLATION: (a) emit h_clamp directly (skip the contrast) → predict collapse to single-settle baseline (isolates the contrast as the binding carrier); (b) epsilon→0 → Δh→0 degenerate, confirming the nudge-difference, not the settle, carries it. Distinct from reentry_two_pass (feedforward re-injection, no energy/clamp) and energy_settle_attractor (single phase, no contrast).

## Cheap test (frozen-first · $0 · decisive numpy probe)

mini-numpy, $0, frozen-first. Quadratic Hopfield-style energy E(h)=½hᵀMh − legAᵀh with M FROZEN PSD; legB clamped on a role-subspace at strength beta. Implement free settle (fixed gradient steps to equilibrium) and nudged settle; compare Δh-readout vs single-settle-readout on the same 4×4 conjunction held-out task. Pre-registered bar: held-out conjunction accuracy; PASS iff contrast ≥ single-settle +0.15 AND the 'emit h_clamp' ablation collapses to single-settle (≤+0.02). No training.

## GPU recipe (cost-gated · PRE-REGISTER ONLY · NOT fired)

PRE-REGISTER ONLY (cost-gated). 303M: conv-trunk → legA,legB; a small symmetric-weight recurrent energy block, K=6 settle steps per phase (free+nudged = double unroll), learned epsilon; contrast readout → byte logits. Train CE on balanced 4-cell corpus, fail-loud per-cell loads. Single H100. Engine-native G1/G6 via CORE mount + held-out 4/4 DESCENT acceptance, pre-registered frozen bars (no tune-to-green).

## Scope / honesty (c9)

설계만 — 측정 0. tier = 🔵 PRE-REGISTERED DESIGN (DIRECTIONAL). frozen bar 사후 이동 금지(tune-to-green 금지, p7). 이 카드는 *방향성 설계*이지 검증된 결과가 아니다 — 과장 박제 금지(a_engine_native_learning). gpu_recipe 발사 시(team-lead cost-gate go): held-out 4/4 mirror-CE DESCENT 게이트(a_clm_gen_pipeline) → CORE `--engine conv` mount 위 frozen G1(H_1129 recombination)·G6(H_1464 fals) byte-exact engine-native 재측정(torch probe 아님) → ckpt PULL before teardown(a_fire_recover_complete). cheap_test 가 numpy mirror 이므로 그 결과도 DIRECTIONAL(엔진-네이티브 아님).
