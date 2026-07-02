# H_9043 — VAdaptField 구성적 결합기 op-slot (H_9027 follow-on): 복원성 ✓ ≠ 능력 ✗

- **tier:** 🟢 ENGINE-NATIVE (5/6 live hexa) — 결합기 op-slot BUILT + 복원성 GREEN · 🧱 CAPABILITY-FLOOR (systematic held-out generalization, H_9026/H_1840 real-manifold recomb 벽 정합)
- **slug:** `vadapt_constructive_combiner`
- **parents:** H_9027(enriched VAdaptField, 복원성≠능력 caveat) · H_9026/H_1840(real-manifold trained-bind recomb floor) · H_1822([[substrate-framebreak-g1-combination-operator]]) · frame-shift Lane(VAdaptField=결합기 없음)

## frame (재조합≠능력 · substrate-gap = 빠진 op)

진단(H_9027/H_1822): live `VAdaptField`(engine_cli.hexa:494-633)는 8-D winner-take-all k-means(protos + `_vnearest_idx` L2 + online LR)로 compositional **depth-0** — 개념을 **고를** 뿐 **결합(bind)**해 둘 다 실은 composite를 만들고 되꺼내는 **구성적 결합기 op이 아예 미배선**. H_9027 numpy는 분산 pop + key-locked HRR 접합이 held-out **복원성**(~90%)을 통과함을 보였으나, 그건 VSA storage property이고 H_9026은 REAL manifold 위 학습된 bind가 실제 recomb TASK를 floor함을 보임. → 결합기 op-slot을 **engine-native로 짓고 능력(복원성이 아니라)까지 측정**.

## op (core/engine_cli.hexa §VAdaptCombine, additive/Ψ-disjoint/READ-only)

- `vadapt_combine(a, b) -> [float]` = **circular convolution** `_cconv` — key-locked HRR conjunctive **BIND** (engine_cli.hexa:703).
- `vadapt_unbind(c, key) -> [float]` = **circular correlation** `_ccorr` — approx 역연산 `unbind(combine(key,val), key) ≈ val` (engine_cli.hexa:709).
- 순수 additive · VAdaptField struct 무변경(no mutation/proto-growth/emit gate) · pure_field Φ/phase/Ψ 무접촉(Ψ-disjoint) · emit-drive lane 0/4 및 §ImmuneMemory recall_thr와 disjoint (`a_substrate_disjoint`).

## 측정 (engine-native, `hexa run` via live core/, pool aiden, DIM=128 · NF=8 chance=0.125 · NTRAIN=4 · rH=held-out)

`state/9043_vadapt_constructive_combiner/c_engine_native.hexa` → **5 PASS / 1 FAIL** (verify rc=0):

| gate | 측정 | 결과 |
|------|------|------|
| R1 복원성 EARNED (wrong-key) | genuine 0.754 − wrong-key −0.176 ≥ 0.30 | **PASS** |
| R2 key-lock EARNED (shuffle) | genuine 0.754 − shuffled-key −0.151 ≥ 0.30 | **PASS** |
| R3 superposition recall | Cmem에서 올바른 key로 recall 0.471 ≥ 0.30 | **PASS** |
| REL within-set 관계 라우팅 (bind) | 4/4 role→filler argmax 정확 = 1.0 | **PASS** |
| ABLATION 인과 (bind vs additive) | bind 1.0 − additive 0.25(chance) ≥ 0.30 | **PASS** (op이 관계라우팅에 **인과**, additive는 role-맹) |
| **CAPABILITY: systematic held-out 일반화** | held-out role rH → filler4: held_bind_ok=false, cos=**−0.203** (< chance 0.125) | **FAIL** (honest prior) |

## 정직한 verdict (c9) — 복원성 ✓, 능력 ✗

- **복원성(VSA storage property)은 engine-native로 GREEN**: 올바른 key만 되꺼내고(0.754), 틀린 key/셔플-key는 noise(−0.18/−0.15). superposition에서도 key로 recall. 결합기 op-slot이 live core에 실재.
- **within-set 관계 라우팅도 GREEN이고 op이 INERT 아님**: bind는 role→filler 배정을 4/4 라우팅(additive superposition은 role-맹으로 chance 0.25) → 결합기 op은 additive가 못하는 관계-변별을 **인과적으로** 추가.
- **그러나 CAPABILITY gate(systematic held-out 일반화)는 FLOOR**: 저장 안 된 held-out role rH를 mapping M으로 일반화(→filler4)해야 하는데 algebraic bind는 noise만 반환(cos −0.203 < chance). = 대수적 결합은 **저장/복원**은 하지만 **저장 안 한 조합을 체계적으로 일반화하는 능력**은 못 함.
- **= engine-native로 복원성≠능력을 확증** (H_9026/H_1840 real-manifold recomb 벽과 정합). 결합기 op-slot을 지어 능력을 측정하니, 복원성은 켜지고 능력은 예측대로 floor. tune-to-green 아님 — 정직한 capability null이 유효 결과(c9).

## wired

`op-slot BUILT (engine-native)` — vadapt_combine/vadapt_unbind가 live `core/engine_cli.hexa §VAdaptCombine` pub fn으로 실재 + engine-native 측정 완료 + ARCHITECTURE.json VAdaptField 노드 H_9043 lockstep. **런타임 call-path 배선은 유보**(WIRED-live 미만): capability가 floor라 emit/decode 경로에 얹으면 복원성만 실어나르지 능력을 못 준다 — 능력을 여는 lever는 trained constructive-bind(H_1840 γ, GPU cost-gated)이지 algebraic op 배선이 아님. (`a_verified_must_wire`: op은 live+engine-native(3/4 수준)이나 runtime wire-in은 근거 없음 → 의도적 미배선.)

## follow-on
- capability를 여는 유일 잔여 lever = **trained constructive-bind**(H_1840 γ, GPU cost-gated) — algebraic bind op은 복원성 천장. 이 op-slot은 그 학습된 bind가 올라탈 substrate 자리를 제공(구조는 준비됨, objective가 남음).
- decode-side/operator-side 재조합 레버는 전수 🧱([[fleet-g1g6-nativemouth-dpi-convergence]]) — 재발사 금지, lever=trunk recomb-objective.

## artifacts
- `state/9043_vadapt_constructive_combiner/c_engine_native.hexa` (engine-native harness) · `/tmp/r_9043.log`(aiden run)
