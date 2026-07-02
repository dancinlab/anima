# H_1660 — Superior-colliculus superadditive inverse-effectiveness bind

- **tier:** 🔵 PRE-REGISTERED DESIGN (DIRECTIONAL · 측정 0 · unmeasured)
- **wired:** DIRECTIONAL-design — no measurement. cheap_test = $0 frozen-first decision probe (numpy, no engine); gpu_recipe = cost-gated PRE-REGISTER ONLY (NOT fired).
- **source:** archbrainstorm — 84-family anima-native synthesis-binding architecture census (binding-wall program, H_1603)
- **lens:** bio-neuro: superior colliculus multisensory integration — superadditive enhancement gated by spatiotemporal register with inverse effectiveness (distinct from coincidence AND-gates and energy-quadrature).
- **artifacts:** `state/binding_arch_census/BRAINSTORM_INDEX.md`
- **xref:** H_1603 (G1≡G6 compositional-binding deficit unification) · H_1449 (attention-block INERT@1blk) · H_1602 (recombination-objective prereg)
- **key:** `multisensory_superadditive_inverse_bind`

## Mechanism

Two legs combine through a superadditive gate with inverse effectiveness (Meredith-Stein SC rule): out = (a + b) + gamma * (a . b) * h(register) * 1/(1 + a + b), where h(register) is a learned spatio-temporal alignment detector and the 1/(1+a+b) factor scales the product (binding) term UP when unimodal magnitudes are weak. So two weak BUT congruent/aligned legs fuse into a strong joint response; incongruent legs are suppressed (cross-modal suppression). One pass: alignment detector -> gated bilinear bind -> inverse-effectiveness normalization.

## Why it crosses the binding wall

Attention/conv are additive-to-subadditive in the relevant regime and have no inverse-effectiveness nonlinearity, so they cannot superadditively amplify features that are individually WEAK in the corpus — which is exactly the regime of novel conjunctions G1/G6 require (each leg under-attested, only the binding is meaningful). Ablation: removing the inverse-effectiveness factor (normalization const->inf, plain bilinear) kills the weak-input amplification that manufactures novel conjunctions; removing the register gate binds incongruent pairs (fabrication up, fals quality down) — two separable falsifiers isolate the two sub-mechanisms.

## Cheap test (frozen-first · $0 · decisive numpy probe)

numpy: two legs = noisy weak attribute codes; congruent pairs (shared latent) vs incongruent; task = emit only the congruent conjunction with a superadditive margin. vs additive+attention baseline. Decision rule (frozen): SC operator yields congruent >> incongruent separation that GROWS as input magnitude shrinks (the inverse-effectiveness signature); ablating the inverse-effectiveness factor flattens the low-magnitude advantage to baseline. $0.

## GPU recipe (cost-gated · PRE-REGISTER ONLY · NOT fired)

Pre-reg 303M: insert an SC-bind head per mouth block (learned register/alignment MLP gating a bilinear product with inverse-effectiveness normalization between the two streams). 4-cell balanced corpus, per-cell held-out CE. Gates: held-out 4/4 DESCENT; engine-native G1>=303M baseline AND G6 fals>0; controls = (a) inverse-effectiveness-off retrain and (b) register-gate-off retrain must each fail G6 / spike fabrication respectively. Pull ckpt pre-teardown.

## Scope / honesty (c9)

설계만 — 측정 0. tier = 🔵 PRE-REGISTERED DESIGN (DIRECTIONAL). frozen bar 사후 이동 금지(tune-to-green 금지, p7). 이 카드는 *방향성 설계*이지 검증된 결과가 아니다 — 과장 박제 금지(a_engine_native_learning). gpu_recipe 발사 시(team-lead cost-gate go): held-out 4/4 mirror-CE DESCENT 게이트(a_clm_gen_pipeline) → CORE `--engine conv` mount 위 frozen G1(H_1129 recombination)·G6(H_1464 fals) byte-exact engine-native 재측정(torch probe 아님) → ckpt PULL before teardown(a_fire_recover_complete). cheap_test 가 numpy mirror 이므로 그 결과도 DIRECTIONAL(엔진-네이티브 아님).
