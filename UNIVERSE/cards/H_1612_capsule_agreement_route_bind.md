# H_1612 — Capsule routing-by-agreement part-whole mouth

- **tier:** 🔵 PRE-REGISTERED DESIGN (DIRECTIONAL · 측정 0 · unmeasured)
- **wired:** DIRECTIONAL-design — no measurement. cheap_test = $0 frozen-first decision probe (numpy, no engine); gpu_recipe = cost-gated PRE-REGISTER ONLY (NOT fired).
- **source:** archbrainstorm — 84-family anima-native synthesis-binding architecture census (binding-wall program, H_1603)
- **lens:** FORMAL-algebraic
- **artifacts:** `state/binding_arch_census/BRAINSTORM_INDEX.md`
- **xref:** H_1603 (G1≡G6 compositional-binding deficit unification) · H_1449 (attention-block INERT@1blk) · H_1602 (recombination-objective prereg)
- **key:** `capsule_agreement_route_bind`

## Mechanism

하위 capsule(part feature, pose+activation)이 학습된 변환행렬 W_ij로 상위 capsule(whole)에 대한 예측 û_j|i를 투표, routing은 magnitude가 아니라 agreement(예측들 사이의 합의=consensus와의 dot)로 게이팅(dynamic routing). 합의가 높은 part-조합만 whole로 라우팅 → 'parts가 정합적으로 함께 나타날 때만' 묶인다. 묶인 whole capsule을 next-byte로 readout. 한 forward에서 부분-전체 결합이 agreement로 성립.

## Why it crosses the binding wall

conv는 feature 존재(magnitude)만 풀링 — '함께-맞물림(co-occurrence with consistent pose)'을 못 잰다. routing-by-agreement는 part들이 같은 whole을 가리킬 때(벡터 정합)만 활성 → 'A와 B가 정합적으로 결합'이라는 관계 자체를 한 패스에서 검증/생성 = falsifiable binding. attention-depth는 합의(2차 정합 신호)를 명시적으로 게이팅하지 않음. ablation: agreement 게이팅을 uniform routing(합의 무시, 평균)으로 치환하면 정합/비정합 조합을 못 가르고 재조합 붕괴 = 합의 라우팅이 binding의 인과.

## Cheap test (frozen-first · $0 · decisive numpy probe)

mini-numpy, frozen-first. 합성 part-vote 집합: 정합 조합(같은 whole 가리킴)과 비정합 조합(랜덤 pose) 생성, dynamic routing 3-iter로 whole activation 분류. 사전등록 bar: 정합 vs 비정합 분리 AUROC≥0.9 AND uniform-routing baseline은 ≈0.5. compositional 셀: 학습에 없던 정합 part-조합도 whole로 묶이는지. ablation: agreement→uniform 토글로 AUROC가 0.5로 붕괴하는지.

## GPU recipe (cost-gated · PRE-REGISTER ONLY · NOT fired)

사전등록만. 303M: conv-trunk feature를 part-capsule(pose 벡터)로, compose head를 routing-by-agreement(W_ij 투표 + 3-iter dynamic routing + whole readout)로. 파라미터 예산은 capsule 수×pose-dim으로 동급 조정. 4칸 balanced corpus, savant 골든존, held-out mirror-CE DESCENT 게이트, 직렬화 후 CORE engine-native G1/G6 frozen 재측정. est ~$50-90 H100(routing iter), ckpt PULL.

## Scope / honesty (c9)

설계만 — 측정 0. tier = 🔵 PRE-REGISTERED DESIGN (DIRECTIONAL). frozen bar 사후 이동 금지(tune-to-green 금지, p7). 이 카드는 *방향성 설계*이지 검증된 결과가 아니다 — 과장 박제 금지(a_engine_native_learning). gpu_recipe 발사 시(team-lead cost-gate go): held-out 4/4 mirror-CE DESCENT 게이트(a_clm_gen_pipeline) → CORE `--engine conv` mount 위 frozen G1(H_1129 recombination)·G6(H_1464 fals) byte-exact engine-native 재측정(torch probe 아님) → ckpt PULL before teardown(a_fire_recover_complete). cheap_test 가 numpy mirror 이므로 그 결과도 DIRECTIONAL(엔진-네이티브 아님).
