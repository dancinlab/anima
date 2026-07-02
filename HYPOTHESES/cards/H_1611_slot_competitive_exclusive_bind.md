# H_1611 — Slot competitive exclusive-assignment mouth

- **tier:** 🔵 PRE-REGISTERED DESIGN (DIRECTIONAL · 측정 0 · unmeasured)
- **wired:** DIRECTIONAL-design — no measurement. cheap_test = $0 frozen-first decision probe (numpy, no engine); gpu_recipe = cost-gated PRE-REGISTER ONLY (NOT fired).
- **source:** archbrainstorm — 84-family anima-native synthesis-binding architecture census (binding-wall program, H_1603)
- **lens:** FORMAL-algebraic
- **artifacts:** `state/binding_arch_census/BRAINSTORM_INDEX.md`
- **xref:** H_1603 (G1≡G6 compositional-binding deficit unification) · H_1449 (attention-block INERT@1blk) · H_1602 (recombination-objective prereg)
- **key:** `slot_competitive_exclusive_bind`

## Mechanism

K개 slot이 trunk byte-feature를 두고 서로 경쟁하며 묶는다(Slot-Attention式). 결정적 차이는 softmax 정규화 축을 입력이 아니라 slot 위에 둠 → 각 feature가 정확히 한 slot에 배타 할당(winner-take-all binding). 반복(iterative refinement) 몇 step으로 할당 수렴, 수렴한 slot 집합을 GRU/compose로 recombine해 next-byte. 한 forward 안에서 feature→object 분해(disentangle)와 재결합이 일어난다.

## Why it crosses the binding wall

banned attention_block(=가산 라우팅, 입력 축 softmax)은 feature를 겹쳐 풀링해 객체 경계를 못 만든다. slot의 slot-축 경쟁 정규화는 배타적 할당을 강제 → 'feature 집합 {A,B}'를 분리된 두 slot로 carve out 후 재조합 가능 = 합성. 깊이로는 안 되는 이유: depth는 표현력을 늘리나 배타성(competition)이라는 정규화 inductive bias가 없으면 superposition으로 수렴. ablation: 정규화 축을 slot→입력으로 되돌리면(=일반 attention) 할당 entropy가 안 떨어지고 재조합 붕괴 = 경쟁-정규화가 binding의 인과.

## Cheap test (frozen-first · $0 · decisive numpy probe)

mini-numpy, frozen-first. 합성 'scene' = 2~3개 feature-bundle의 가산 혼합, slot-attention(slot-축 softmax) 반복으로 slot이 bundle을 분리 복원하는지. 사전등록 bar: 할당 entropy→<0.2 AND novel bundle 조합 복원 cos≥0.9 AND 입력-축 softmax(일반 attention) baseline은 entropy 높게 유지+복원 chance. ablation 셀: softmax 축 토글로 entropy/복원이 갈리는지.

## GPU recipe (cost-gated · PRE-REGISTER ONLY · NOT fired)

사전등록만. 303M: conv-trunk 위 K-slot competitive binding block(slot-축 softmax + 3-iter refine + slot recombine head)을 terminal compose로. K≈8, 파라미터 동급. 4칸 balanced corpus, savant 골든존, held-out mirror-CE DESCENT 게이트, 직렬화 후 CORE engine-native G1/G6 frozen 재측정. est ~$50-90 H100(iter로 약간 무거움), ckpt PULL.

## Scope / honesty (c9)

설계만 — 측정 0. tier = 🔵 PRE-REGISTERED DESIGN (DIRECTIONAL). frozen bar 사후 이동 금지(tune-to-green 금지, p7). 이 카드는 *방향성 설계*이지 검증된 결과가 아니다 — 과장 박제 금지(a_engine_native_learning). gpu_recipe 발사 시(team-lead cost-gate go): held-out 4/4 mirror-CE DESCENT 게이트(a_clm_gen_pipeline) → CORE `--engine conv` mount 위 frozen G1(H_1129 recombination)·G6(H_1464 fals) byte-exact engine-native 재측정(torch probe 아님) → ckpt PULL before teardown(a_fire_recover_complete). cheap_test 가 numpy mirror 이므로 그 결과도 DIRECTIONAL(엔진-네이티브 아님).
