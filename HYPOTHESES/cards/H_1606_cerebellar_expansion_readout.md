# H_1606 — Marr-Albus Granule-Expansion Mouth (sparse conjunctive basis -> Purkinje linear readout)

- **tier:** 🔵 PRE-REGISTERED DESIGN (DIRECTIONAL · 측정 0 · unmeasured)
- **wired:** DIRECTIONAL-design — no measurement. cheap_test = $0 frozen-first decision probe (numpy, no engine); gpu_recipe = cost-gated PRE-REGISTER ONLY (NOT fired).
- **source:** archbrainstorm — 84-family anima-native synthesis-binding architecture census (binding-wall program, H_1603)
- **lens:** cerebellar cortex — Marr-Albus-Ito granule-cell combinatorial expansion + Purkinje linear readout; sparse conjunctive recoding (Cover's theorem).
- **artifacts:** `state/binding_arch_census/BRAINSTORM_INDEX.md`
- **xref:** H_1603 (G1≡G6 compositional-binding deficit unification) · H_1449 (attention-block INERT@1blk) · H_1602 (recombination-objective prereg)
- **key:** `cerebellar_expansion_readout`

## Mechanism

Mossy-fiber input = both legs concatenated. A high-expansion-ratio (10-50x) projection to a granule layer with sparse k-WTA threshold makes each granule a random sparse conjunction of a few mixed leg-A/leg-B inputs. A Purkinje-style strictly-LINEAR readout (the only trained weights into logits) then learns arbitrary functions of the legs because conjunctions are now linearly separable in the expanded space. Binding = an explicit conjunctive basis manufactured by expansion+sparsification; ALL nonlinearity/binding lives in the fixed expansion, the readout is linear.

## Why it crosses the binding wall

Marr-Albus / Cover's theorem: random nonlinear expansion to higher dim makes XOR-class conjunctions linearly separable, so a linear readout suffices. conv/attention at fixed embedding width keep the representation in a low-dim additive manifold where conjunctions are not separable. Ablation: shrink expansion ratio to 1x (no expansion) OR remove k-WTA (dense -> linear-equivalent) -> conjunctions unreadable, readout fails = collapses to additive baseline. Distinct from depth/width because the readout is strictly LINEAR and the expansion is sparse-RANDOM (kernel trick), not a learned deep stack; the binding is the expansion, provable via the ratio sweep.

## Cheap test (frozen-first · $0 · decisive numpy probe)

numpy, DIRECTIONAL. factored-table + parity tasks; granule expansion (random Gaussian proj to 4096 + top-5% k-WTA) + linear readout vs linear readout on raw concat. 25% held-out combos. Frozen bar: expansion held-out CE < 0.3 nats AND raw-linear >= 0.9x uniform. Pre-register a MONOTONE binding-onset across expansion ratio {1,4,16,64}x (onset must exist).

## GPU recipe (cost-gated · PRE-REGISTER ONLY · NOT fired)

PRE-REGISTER ONLY. 303M with a granule-expansion + sparse-kWTA layer feeding the final logit readout (expansion fixed-random or low-LR; readout linear), trunk otherwise standard. Engine-native G1/G6; bars frozen. ~$15; ckpt PULL.

## Scope / honesty (c9)

설계만 — 측정 0. tier = 🔵 PRE-REGISTERED DESIGN (DIRECTIONAL). frozen bar 사후 이동 금지(tune-to-green 금지, p7). 이 카드는 *방향성 설계*이지 검증된 결과가 아니다 — 과장 박제 금지(a_engine_native_learning). gpu_recipe 발사 시(team-lead cost-gate go): held-out 4/4 mirror-CE DESCENT 게이트(a_clm_gen_pipeline) → CORE `--engine conv` mount 위 frozen G1(H_1129 recombination)·G6(H_1464 fals) byte-exact engine-native 재측정(torch probe 아님) → ckpt PULL before teardown(a_fire_recover_complete). cheap_test 가 numpy mirror 이므로 그 결과도 DIRECTIONAL(엔진-네이티브 아님).
