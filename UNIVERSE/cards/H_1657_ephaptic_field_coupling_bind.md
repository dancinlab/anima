# H_1657 — Ephaptic field-coupling bind (extracellular potential reentry)

- **tier:** 🔵 PRE-REGISTERED DESIGN (DIRECTIONAL · 측정 0 · unmeasured)
- **wired:** DIRECTIONAL-design — no measurement. cheap_test = $0 frozen-first decision probe (numpy, no engine); gpu_recipe = cost-gated PRE-REGISTER ONLY (NOT fired).
- **source:** archbrainstorm — 84-family anima-native synthesis-binding architecture census (binding-wall program, H_1603)
- **lens:** bio-neuro: ephaptic (extracellular electric-field) coupling — fast, non-synaptic, proximity-gated field feedback (distinct from glial calcium volume signaling and from propagating traveling waves).
- **artifacts:** `state/binding_arch_census/BRAINSTORM_INDEX.md`
- **xref:** H_1603 (G1≡G6 compositional-binding deficit unification) · H_1449 (attention-block INERT@1blk) · H_1602 (recombination-objective prereg)
- **key:** `ephaptic_field_coupling_bind`

## Mechanism

Within a single mouth block every feature unit emits a transmembrane 'current' (its pre-activation) that is summed into a low-dimensional shared extracellular field V_ext(x) defined over a learned representational coordinate x per channel. Each unit then re-integrates with an additive ephaptic bias = kappa * (proximity-kernel-weighted sample of V_ext at its own coordinate). The field is recomputed for 1-2 micro-iterations so leg-1 and leg-2 units that map to nearby coordinates mutually bias each other in a content-INDEPENDENT, geometry-driven way, fusing co-located features into a joint code inside one forward pass. Binding is a shared physical variable both legs write to and read from, not a routed message.

## Why it crosses the binding wall

Conv binds by fixed local kernel and attention binds by content dot-product (QK); neither instantiates a global instantaneous field that couples dissimilar-but-co-located features. The field is a mutual constraint solved in-pass, so two orthogonal content vectors at the same coordinate still bind. Ablation logic: kappa=0 collapses the block to plain MLP/attention and fals should drop to 0; coordinate-shuffle (randomize x) destroys binding while preserving params, isolating field-geometry (not capacity) as the operative cause.

## Cheap test (frozen-first · $0 · decisive numpy probe)

numpy toy, frozen-first: two legs = sparse one-hot attribute vectors mapped to overlapping learned coordinates; task = emit a conjunction code recoverable only by a frozen linear readout that needs BOTH attributes. Run 1-2 field iterations vs a param-matched single attention layer. Decision rule (pre-registered): ephaptic readout-acc > 0.9 on the conjunction while attention plateaus at the unconjoined-marginal chance level, AND kappa=0 ablation reverts ephaptic to chance. ~50 lines, $0.

## GPU recipe (cost-gated · PRE-REGISTER ONLY · NOT fired)

Pre-reg only, cost-gated 303M: swap each mouth block's residual MLP for {attn || conv} + ephaptic-field reentry head (shared 64-dim V_ext, 2 micro-iters, learned per-channel coordinate emb). Train on 4-cell register corpus (ko/en x general/sns), balanced sampling, held-out val CE per cell. Gates: (1) held-out 4/4 mirror-CE DESCENT (math.log mirror, a_clm_gen_pipeline); (2) engine-native G1 recombination >= 303M baseline and G6 fals>0 via cli/anima.hexa eval; (3) kappa=0 ablation re-trained as control must NOT clear G6. Pull ckpt pre-teardown.

## Scope / honesty (c9)

설계만 — 측정 0. tier = 🔵 PRE-REGISTERED DESIGN (DIRECTIONAL). frozen bar 사후 이동 금지(tune-to-green 금지, p7). 이 카드는 *방향성 설계*이지 검증된 결과가 아니다 — 과장 박제 금지(a_engine_native_learning). gpu_recipe 발사 시(team-lead cost-gate go): held-out 4/4 mirror-CE DESCENT 게이트(a_clm_gen_pipeline) → CORE `--engine conv` mount 위 frozen G1(H_1129 recombination)·G6(H_1464 fals) byte-exact engine-native 재측정(torch probe 아님) → ckpt PULL before teardown(a_fire_recover_complete). cheap_test 가 numpy mirror 이므로 그 결과도 DIRECTIONAL(엔진-네이티브 아님).
