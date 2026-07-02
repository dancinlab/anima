# H_1613 — Product-key Cartesian factored-binding memory mouth

- **tier:** 🔵 PRE-REGISTERED DESIGN (DIRECTIONAL · 측정 0 · unmeasured)
- **wired:** DIRECTIONAL-design — no measurement. cheap_test = $0 frozen-first decision probe (numpy, no engine); gpu_recipe = cost-gated PRE-REGISTER ONLY (NOT fired).
- **source:** archbrainstorm — 84-family anima-native synthesis-binding architecture census (binding-wall program, H_1603)
- **lens:** FORMAL-algebraic
- **artifacts:** `state/binding_arch_census/BRAINSTORM_INDEX.md`
- **xref:** H_1603 (G1≡G6 compositional-binding deficit unification) · H_1449 (attention-block INERT@1blk) · H_1602 (recombination-objective prereg)
- **key:** `product_key_factored_bind`

## Mechanism

키 공간을 두 half-codebook의 데카르트 곱 K1×K2로 분해(Lample product-key memory를 binding op로 재목적화). 매 위치 query를 두 절반 q1,q2로 split, 각각 자기 codebook에서 top-k 선택, 두 선택의 교차곱이 bound memory cell (k1,k2)을 주소지정 → 그 셀의 value를 next-byte로. binding = '어느 (role-half, filler-half) 쌍이 공동 선택되었나'가 sparse 주소로 실현되고, |K1|·|K2| combinatorial 셀을 √(파라미터) 비용으로 커버.

## Why it crosses the binding wall

flat key memory(또는 conv readout)는 본 조합만 표현 가능 — 미학습 (role,filler) 조합은 가장 가까운 학습 셀로 충돌(collapse)된다(재조합 결손). Cartesian 분해는 두 축을 독립 주소화해 학습 때 본 적 없는 (k1,k2) 교차도 distinct 셀로 분리 주소지정 → factorized compositional coverage. 깊이로 안 되는 이유: depth는 함수 표현력일 뿐 주소공간의 곱-구조(K1×K2)를 안 만든다. ablation: 두 half-codebook을 하나의 flat codebook(|K1·K2| 동일 크기)으로 합치면 novel 조합이 충돌해 재조합 붕괴 = 곱-팩터링이 binding의 인과.

## Cheap test (frozen-first · $0 · decisive numpy probe)

mini-numpy, frozen-first. K1=K2=64, sparse subset의 (k1,k2) 셀에만 target value 할당하고 학습, held-out novel (k1,k2) 조합이 distinct 셀을 주소지정하는지(충돌률). 사전등록 bar: novel-combo 충돌률<0.1 AND 동일 용량 flat-codebook baseline은 충돌률≈novel 비율(붕괴). ablation 셀: factored↔flat 토글로 충돌률이 갈리는지.

## GPU recipe (cost-gated · PRE-REGISTER ONLY · NOT fired)

사전등록만. 303M: conv-trunk readout을 product-key factored-bind memory head(query split + 두 half-codebook top-k + Cartesian 셀 value lookup)로 교체, |K1|·|K2|로 큰 binding capacity를 √-비용 파라미터로. 4칸 balanced corpus, savant 골든존, held-out mirror-CE DESCENT 게이트, 직렬화 후 CORE engine-native G1/G6 frozen 재측정. est ~$40-80 H100, ckpt PULL.

## Scope / honesty (c9)

설계만 — 측정 0. tier = 🔵 PRE-REGISTERED DESIGN (DIRECTIONAL). frozen bar 사후 이동 금지(tune-to-green 금지, p7). 이 카드는 *방향성 설계*이지 검증된 결과가 아니다 — 과장 박제 금지(a_engine_native_learning). gpu_recipe 발사 시(team-lead cost-gate go): held-out 4/4 mirror-CE DESCENT 게이트(a_clm_gen_pipeline) → CORE `--engine conv` mount 위 frozen G1(H_1129 recombination)·G6(H_1464 fals) byte-exact engine-native 재측정(torch probe 아님) → ckpt PULL before teardown(a_fire_recover_complete). cheap_test 가 numpy mirror 이므로 그 결과도 DIRECTIONAL(엔진-네이티브 아님).
