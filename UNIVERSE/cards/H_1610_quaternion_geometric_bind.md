# H_1610 — Quaternion / geometric-algebra (non-commutative) bind mouth

- **tier:** 🔵 PRE-REGISTERED DESIGN (DIRECTIONAL · 측정 0 · unmeasured)
- **wired:** DIRECTIONAL-design — no measurement. cheap_test = $0 frozen-first decision probe (numpy, no engine); gpu_recipe = cost-gated PRE-REGISTER ONLY (NOT fired).
- **source:** archbrainstorm — 84-family anima-native synthesis-binding architecture census (binding-wall program, H_1603)
- **lens:** FORMAL-algebraic
- **artifacts:** `state/binding_arch_census/BRAINSTORM_INDEX.md`
- **xref:** H_1603 (G1≡G6 compositional-binding deficit unification) · H_1449 (attention-block INERT@1blk) · H_1602 (recombination-objective prereg)
- **key:** `quaternion_geometric_bind`

## Mechanism

두 leg을 4D Hamilton product(또는 Clifford geometric product)로 묶는다. trunk feature를 quaternion 블록(d/4개 사원수)으로 재해석, role을 회전 사원수 q_r, filler를 q_f로 두고 bound = q_r ⊗_H q_f (비가환 곱). unbind는 켤레 q_r* 곱. next-byte readout은 회전 적용된 filler를 logits로. 핵심: 비가환이라 bind(r,f)≠bind(f,r) → agent/patient 같은 순서 있는 role이 한 패스에서 구별 보존.

## Why it crosses the binding wall

circular conv·outer product는 가환(또는 대칭) → 'A가 B를 X한다'와 'B가 A를 X한다'를 구조적으로 못 가른다(역할 비대칭 결손). 비가환 division algebra의 곱은 순서를 좌표 회전으로 인코딩해 한 forward에서 directed role binding을 실현 → G6 falsifiable 생성(누가 누구에게)이 가능. conv/attention-depth는 순서를 위치 임베딩의 가산 bias로만 다뤄 곱셈적 directed-binding 부재. ablation: Hamilton product를 대칭화(½(qr·qf+qf·qr))하면 순서 구별이 붕괴 = 비가환성이 directed binding의 인과.

## Cheap test (frozen-first · $0 · decisive numpy probe)

mini-numpy, frozen-first. random 사원수 role/filler로 directed 쌍 (agent,patient) 생성, bind 후 역할-스왑 쌍과의 구별을 켤레-unbind로 분류. 사전등록 bar: role-swap 구별 정확도≥0.9 AND 가환 baseline(circular conv 또는 symmetrized)은 chance(0.5). ablation 셀: 곱을 symmetrize하면 정확도가 0.5로 붕괴하는지.

## GPU recipe (cost-gated · PRE-REGISTER ONLY · NOT fired)

사전등록만. 303M: trunk feature를 quaternion 블록으로, compose head를 Hamilton-product bind/conjugate-unbind로 교체(quaternion linear layer = 1/4 파라미터로 동급 표현, 파라미터 예산 여유). 4칸 balanced corpus, savant 골든존, held-out mirror-CE DESCENT 게이트, 직렬화 후 CORE engine-native G1/G6 frozen 재측정. est ~$40-80 H100, ckpt PULL.

## Scope / honesty (c9)

설계만 — 측정 0. tier = 🔵 PRE-REGISTERED DESIGN (DIRECTIONAL). frozen bar 사후 이동 금지(tune-to-green 금지, p7). 이 카드는 *방향성 설계*이지 검증된 결과가 아니다 — 과장 박제 금지(a_engine_native_learning). gpu_recipe 발사 시(team-lead cost-gate go): held-out 4/4 mirror-CE DESCENT 게이트(a_clm_gen_pipeline) → CORE `--engine conv` mount 위 frozen G1(H_1129 recombination)·G6(H_1464 fals) byte-exact engine-native 재측정(torch probe 아님) → ckpt PULL before teardown(a_fire_recover_complete). cheap_test 가 numpy mirror 이므로 그 결과도 DIRECTIONAL(엔진-네이티브 아님).
