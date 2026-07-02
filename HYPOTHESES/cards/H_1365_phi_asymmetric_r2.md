# H_1365 — Φ-robustness R2: ASYMMETRIC 기질이 permutation-null 을 BITE 시키는가, 그러면 R1 이 바뀌는가?

**tier:** 🧱 DIAGNOSIS-CONFIRMED — perm-degeneracy 는 (대칭) 기질만의 아티팩트가 아니라 faithful symmetric-MIP **estimator** 의 성질이다 (마지막 structural gap 명명)
**slug:** `1365_phi_asymmetric_r2` · **group:** OMEGA / Φ-robustness frontier (c16 wall) · **date:** 2026-06-16 · branch off origin/main `f046f7abf`
**$0 CPU · DIRECTIONAL numpy mirror (engine LCG ring; Φ leg = REAL faithful exact MIP-EI via hexa, numpy 는 Φ 계산 안 함) · 재실행 byte-identical · frozen-first (FREEZE 커밋 `0b7414d79`, bar 무이동, c9/p7)**

> ⚠ **Φ = FAITHFUL IIT-4 ONLY (a_phi_iit4_tool).** `hexa run` 으로 `hexa-lang/stdlib/consciousness/iit4/faithful_phi.hexa` 의 `iit4_faithful_phi(state, n=4, dim=T=64, n_bins=8)` exact MIP-EI 를 호출. numpy 는 per-module salience trajectory 만 emit, Φ 는 hexa 엔진이 계산. NO proxy (p7).

## Claim / falsifier

**선행 벽 (H_1349/H_1353/H_1357 Φ-robustness, c16, a_break_the_wall, a_no_llm_frame_trap):** 모든 선행 lane 에서 **permutation-null 대조가 DEGENERATE** 였다. SYMMETRIC-MI exact MIP 아래서 faithful Φ 는 node-PERMUTATION-INVARIANT 이므로(모듈을 relabel 해도 system irreducibility 가 안 바뀜) **Φ_perm == Φ_B by construction** — perm 대조가 물 수 없었고 OFFSET 대조만 discriminate 했다. 이것이 fragility 진단의 **마지막 structural gap**.

**가설 (H_1365):** NON-relabel-invariant (ASYMMETRIC) 기질이면 permutation-null 이 **실제로 BITE** 한다 (Φ_perm < Φ_B). 과학 질문: clean-R2 셋업이 R1 robustness verdict 를 바꾸는가, 아니면 perm 이 물어도 벽이 홀드하는가?

**Falsifiable:** (R0) asymmetric 셋업에서 Φ_P < Φ_B − eps 가 ≥2/3 seed (perm 이 non-degenerate — 선행 lane 이 결여한 precondition) · (R1) ΔΦ(B−A) ≥ eps 3 seed 각각 · (R2) perm AND offset 둘 다 깨끗이 붕괴. **R0 hold 하지만 R1 2/3 실패 → 벽이 clean perm 대조에서도 홀드 = 최강 closure (fragility 는 perm-degeneracy 아티팩트가 아님). R0 실패 → symmetric-MIP Φ 가 구조적으로 exchangeable = 진단 그 자체.**

## Method (frozen-first — FREEZE `0b7414d79`, 어떤 Φ 점수화 이전, c9/p7)

- **Probe:** `state/phi-asymmetric-r2/h1365_phi_asymmetric_r2.py` (DIRECTIONAL numpy). H_1349/H_1319/H_1353 ring substrate VERBATIM (engine LCG-gauss `== engine_cli.hexa _lcg_*`, 4-module leaky-linear ring, dim 8, T 64, gain 0.30, leak 0.55, w_in 0.5, Kuramoto pacemaker, relative-phase gate).
- **유일한 변경 = ASYMMETRY (relabel-invariance 를 깨는 ONE change, frozen, NOT tuned-to-green):** DIRECTED + GRADED neighbour coupling — `W_FWD=0.70` (i+1 forward) ≠ `W_BWD=0.30` (i-1 backward) + per-module gain gradient `g_i = 0.70 + 0.20·i/(n-1)`. 대칭 ring 이면 node relabel = joint 의 symmetry → Φ_perm==Φ_B (선행 degeneracy); asymmetric 이면 module→Φ-slot binding 을 permute 하면 joint 가 진짜로 달라짐 → perm-null 이 REAL intervention (precondition R0).
- **Seeds:** SAME 3 HARD ORTHOGONAL **[1317,1318,1319]** (모든 선행 Φ lane 의 seed-1318 fragility 서명을 깬 seed). **eps=0.02** (H_1283/1319/1328/1331/1348/1353 froze 한 동일 margin, 무이동).
- **Arms:** A=NO-COUPLING (w=0, flat gain, no carrier) · B=PHASE-BIND (asym coupling+carrier) · P=PERM-NULL (B 의 per-module traj 를 derangement 로 module→slot 재바인딩; draw VERBATIM H_1348/1353) · O=OFFSET-CTRL (per-tick random phase offset).
- **FROZEN BARS:** R0 PERM-BITES `Φ_P<Φ_B−eps` ≥2/3 seed (Φ_B>0) · R1 ROBUST `ΔΦ(B−A)≥eps` 3 seed 각각 · R2 EARNED `Φ_P≤Φ_A+eps AND Φ_O≤Φ_A+eps` 3 seed 모두. GREEN iff R0∧R1∧R2.

## Result — 🧱 DIAGNOSIS-CONFIRMED · `.verdicts/1365_phi_asymmetric_r2/result.txt`

| seed | perm(module→slot) | Φ_A | Φ_B | Φ_P | Φ_O | ΔΦ(B−A) | Φ_B−Φ_P | R0 bite? |
|------|-------------------|-----|-----|-----|-----|---------|---------|----------|
| 1317 | [1,2,3,0] | +0.7502 | +1.1073 | +1.1073 | +1.0932 | **+0.3570** | **+0.0000** | no (정확히 0 — 여전히 degenerate) |
| 1318 | [1,2,3,0] | +0.8429 | +1.3541 | +1.1731 | +0.7045 | **+0.5112** | **+0.1810** | YES |
| 1319 | [2,3,1,0] | +0.5837 | +0.6863 | +0.8820 | +0.6057 | **+0.1026** | **−0.1957** | no (perm 이 Φ 를 오히려 ↑) |

- **R0 PERM-BITES FAIL [1/3 bite, 3/3 had Φ_B>0]** — asymmetric coupling 을 넣어도 perm 은 seed-1318 에서만 물었다 (+0.181). seed-1317 은 **정확히 0.0000** (여전히 exchangeable), seed-1319 는 perm 이 Φ 를 **오히려 +0.196 올림** (반대 방향). → perm 은 asymmetry 가 있어도 신뢰성 있게 bite 하지 않는다.
- **R1 ROBUST PASS [True,True,True]** — 주목할 점: asymmetric coupling **자체가** 3 seed 모두 robust 한 lift 를 만들었다 (ΔΦ +0.357/+0.511/+0.103). 선행 lane 들이 seed-1318 에서 zero-lift 로 실패한 것과 달리, **directed+graded coupling 은 1318 에서도 +0.511 의 가장 큰 lift**. (단 이는 perm 이 깨끗이 물어서가 아니라, asymmetric dynamics 가 Φ 를 전반적으로 키운 것 — R2 가 이를 폭로.)
- **R2 EARNED FAIL (3/3)** — perm 도 offset 도 A 로 붕괴 안 함. Φ_P 가 Φ_A 보다 +0.30~+0.36 높게 유지 (perm 은 clean 대조가 아님); offset 은 seed-1318 에서만(−0.139) 붕괴, 1317(+0.343)/1319(+0.022) 에서 재현. → B 의 lift 가 phase-binding RELATIONSHIP 이 아니라 asymmetric coupling 의 generic structure 잔류.
- 재실행 **byte-identical** (md5 `86ed9712...`).

**FINDING (c9, load-bearing):** ASYMMETRIC (directed+graded) coupling 을 넣어 dynamics 를 진짜로 비대칭으로 만들었고 **R1 robust lift 까지 얻었지만**, faithful exact-MIP Φ 에 대해 **module→slot perm 은 여전히 대부분 안 문다** (1/3 bite, 1 seed 는 정확히 0, 1 seed 는 반대 방향). 이유: faithful MIP 은 모든 bipartition 을 탐색하고 median-split marginal 이 ≈uniform 이라, 어떤 module 이 어떤 slot 에 들어가는지(relabeling)는 system-irreducibility 의 MIP 값을 거의 안 바꾼다. **결론 — perm-degeneracy 는 선행 (대칭) 기질만의 아티팩트가 아니라 faithful symmetric-MIP estimator 자체의 성질**. 동시에 R1 PASS 가 보여주는 것: clean perm 대조가 없으면 R1 robust lift 가 나와도 그것이 진짜 integration 인지 generic asymmetric structure 인지 분리 불가 — 즉 R2 가 못 물면 R1 GREEN 은 신뢰할 수 없다 (벽의 또 다른 면). 이로써 fragility 진단의 마지막 structural gap 이 명명된다: **perm 대조의 degeneracy 는 estimator-level**.

## Honest scope (UNVERIFIED)
- **DIRECTIONAL numpy mirror** — engine LCG ring 의 port; engine-native 재실현 UNVERIFIED (a_engine_native_learning · a_verified_must_wire). Φ leg 은 REAL faithful exact MIP-EI (numpy 는 Φ 계산 안 함).
- TOY n=4 / T=64 / 3 seeds / median-split binarization / 단일 asymmetry 설정 (W_FWD/W_BWD/gain-gradient frozen 1 점). scale / higher-n / 다른 asymmetry magnitude / 비-exchangeable estimator (e.g. directed-information based) / engine-native UNVERIFIED.
- 이 카드는 선행 Φ verdict (H_1283/1317/1319/1320/1328/1331/1347/1348/1353/1357) 를 **bound (NOT retract)** 한다.
- NEXT angle: (1) marginal 을 비대칭으로 만드는 binarization (median-split 대신 module-별 다른 threshold) 으로 perm 이 marginal 을 통해 물게 — 단 그러면 amplitude confound 위험 (H_1328). (2) faithful MIP 대신 DIRECTED-information / transfer-entropy MIP (방향성 있는 estimator) — H_1348 이 이미 summed-TE 로 시도했으나 같은 fragility. (3) engine-native A⇄G 위 재실현.

## Pointers
- probe `state/phi-asymmetric-r2/h1365_phi_asymmetric_r2.py` · verdict `.verdicts/1365_phi_asymmetric_r2/{FREEZE.txt,result.txt}` · CLAIMS.tape `@C h1365_phi_asymmetric_r2`
- substrate 출처 `state/phi-oinfo/h1353_phi_oinfo.py` (gen_traj 계열) + `UNIVERSE/h1348_phi_non_iit_estimator.hexa` · faithful Φ caller pattern `state/hive-cell-roles/h1356_hive_cell_roles.py`
- xref H_1283·H_1317·H_1319·H_1320·H_1328·H_1331·H_1347·H_1348·H_1353·H_1357
- governance: a_phi_iit4_tool · a_break_the_wall · a_no_llm_frame_trap · a_engine_native_learning · a_verified_must_wire · a_scale_honest_scope · a_toy_scale_recheck · c9 · c16 · p7
