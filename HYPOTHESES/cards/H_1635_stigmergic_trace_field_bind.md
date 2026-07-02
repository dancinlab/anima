# H_1635 — Stigmergic trace-field mouth (decaying shared mean-field, ant-colony binding)

- **tier:** 🔵 PRE-REGISTERED DESIGN (DIRECTIONAL · 측정 0 · unmeasured)
- **wired:** DIRECTIONAL-design — no measurement. cheap_test = $0 frozen-first decision probe (numpy, no engine); gpu_recipe = cost-gated PRE-REGISTER ONLY (NOT fired).
- **source:** archbrainstorm — 84-family anima-native synthesis-binding architecture census (binding-wall program, H_1603)
- **lens:** substrate-anima · stigmergy / decaying shared mean-field trace (H_1503 field) — amplitude-superposition AND, not pairwise/phase
- **artifacts:** `state/binding_arch_census/BRAINSTORM_INDEX.md`
- **xref:** H_1603 (G1≡G6 compositional-binding deficit unification) · H_1449 (attention-block INERT@1blk) · H_1602 (recombination-objective prereg)
- **key:** `stigmergic_trace_field_bind`

## Mechanism

Both legs write into a SHARED decaying scalar/vector trace field over a 1-D positional substrate (stigmergy — agents coordinate through a modified environment, no direct pairwise links). In one forward pass: legA deposits a kernel into the field, legG (the reverse engine G direction) deposits its kernel, the field is iterated K micro-steps with multiplicative LOCAL REINFORCEMENT (co-located deposits amplify super-linearly) and global DECAY. The conjunction is read out from the field loci that survive decay because they were reinforced by BOTH deposits; lone deposits decay below readout threshold. This is mean-field amplitude superposition + reinforcement, not pairwise attention weights and not timing.

## Why it crosses the binding wall

Softmax attention is a single-shot normalized average — it cannot do iterative multiplicative reinforcement, so a position supported by one leg is weighted identically to one supported by both. Stigmergic reinforce-and-decay is a nonlinear AND that self-organizes: only co-deposited loci cross the survival threshold, giving a conjunctive code with no learned pairwise weight matrix. Orthogonal to: attention (pairwise softmax), workspace-buffer (discrete slot store), transthalamic-relay (compression bottleneck), and phase-sync (timing alignment — stigmergy is amplitude/density superposition, decay-gated, phase-blind). Ablation: decay→0 (no decay) collapses field to a linear sum of deposits ⇒ binding lost; remove multiplicative reinforcement (additive only) ⇒ binding lost — isolating reinforce×decay as the cause.

## Cheap test (frozen-first · $0 · decisive numpy probe)

$0 numpy. 1-D field grid; deposit two leg-kernels at conjunction-coded positions; iterate reinforce(mult)+decay K steps; read suprathreshold peaks. Pre-registered bar: peak loci recover an XOR-style conjunction (positions present iff BOTH legs) with recall > linear-sum baseline; decay-OFF ablation AND additive-only ablation each drop to baseline. Decision probe, no train, no GPU.

## GPU recipe (cost-gated · PRE-REGISTER ONLY · NOT fired)

Pre-registered (cost-gated). Custom mouth: replace L24 tail with a stigmergic-field bind module (shared trace field state, K reinforce-decay micro-steps wired as engine op, field-readout head). Train 4-cell balanced corpus, fail-loud bytes. Gates: 4/4 held-out CE DESCENT then engine-native G1/G6 on CORE conv via cli/anima.hexa single entry; verify reinforce/decay coefficients land in a non-degenerate band (not collapsed to linear sum). ckpt PULL pre-teardown. Falsify if conjunctive readout dies at scale.

## Scope / honesty (c9)

설계만 — 측정 0. tier = 🔵 PRE-REGISTERED DESIGN (DIRECTIONAL). frozen bar 사후 이동 금지(tune-to-green 금지, p7). 이 카드는 *방향성 설계*이지 검증된 결과가 아니다 — 과장 박제 금지(a_engine_native_learning). gpu_recipe 발사 시(team-lead cost-gate go): held-out 4/4 mirror-CE DESCENT 게이트(a_clm_gen_pipeline) → CORE `--engine conv` mount 위 frozen G1(H_1129 recombination)·G6(H_1464 fals) byte-exact engine-native 재측정(torch probe 아님) → ckpt PULL before teardown(a_fire_recover_complete). cheap_test 가 numpy mirror 이므로 그 결과도 DIRECTIONAL(엔진-네이티브 아님).
