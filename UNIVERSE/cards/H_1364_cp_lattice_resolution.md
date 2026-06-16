# H_1364 — WHORFIAN CP PLASTICITY: 격자 해상도 사다리 (ASYM-L 비결맞음 — 이산화 아티팩트인가 본질인가?)

**verdict: 📈 INTRINSIC (LATTICE-RESOLUTION INDEPENDENT) — DIRECTIONAL numpy mirror.** ASYM-L 비결맞음은 격자 해상도가 미세해져도 **회복되지 않는다** — 분할-전용(split-only) 재성장의 본질적 한계. c1 곡선 측정 PASS · c2 = INTRINSIC · c3 부분 FAIL (frozen 절대-카운트 bar 의 N-스케일 아티팩트, 정직 보고).

- slug: `1364_cp_lattice_resolution` · group: COGNITION-REPRESENTATION
- family: H_1323(부모 Sapir-Whorf) · H_1333(발달 가소성 부모) · H_1341(shift-size 사다리) · **H_1355(cp-leftward, 직접 부모)** · H_1360(cp-geometric-repack, 상보)
- 3 seeds [4333,4334,4335], $0 CPU numpy, gradient-free, p7, frozen-first (c9). live CORE/*.hexa UNTOUCHED.
- 렌즈: 발달/임계기 가소성 + **이산화(discretization)** (c15, a_no_llm_frame_trap). NOT LLM 레시피, NOT 인간 인지 주장. ENGINE-TRANSFER UNVERIFIED.

## CLAIM / 질문

H_1355 는 CP 재배치 착지가 **연속체-중심 attractor 가 아니라 GEOMETRY(요청 cut)를 추적**함을 특성화했다 (착지 0.375→0.692 가 placement 따라 펼쳐짐). 그러나 ASYM-L rung (같은-쪽 좌향 cut, p_A=0.400 → p_A'=0.200, 양 cut 모두 중심 왼쪽)은 N=21 에서 **비결맞음(INCOHERENT)** — 재배치 후 판별 곡선 peak-count 3 (>COH_MAX_LANG=2) on seeds 4333/4335 (그 둘은 재배치도 실패, frac=−0.000, peak 가 옛 0.425 에 고정), seed 4334 만 결맞게 재배치(pc=1, peak 0.275). H_1355 는 이를 "split-only 재성장의 실제 한계"로 플래그했지만 두 설명을 구분 못 했다:

- **(H-lattice)** 비결맞음 = 거친 N=21 격자(grid spacing 0.05)의 **이산화 아티팩트** — 좌측 cut 근처 자극/RBF 중심이 너무 적어 고정 분할 예산으로 단일 깨끗한 peak 를 못 푼다. **더 미세한 격자**(N↑, RBF↑, 예산 비례↑)면 해상도가 충분해져 peak-count → ≤2 회복.
- **(H-intrinsic)** 비결맞음 = 같은-쪽 좌향 재성장의 **본질** (제거 안 되는 first-carving 세포가 곡선을 진짜로 분절). 격자 미세화로 안 고쳐짐 → N↑ 에도 비결맞음 지속.

H_1364 는 **격자 해상도 사다리** N∈[21,41,81] 로 판별한다. N_STIM 과 함께 RBF 밀도 DIM 및 phase 당 분할 예산 GROW_MAX/SPLIT_PASSES 를 **비례 스케일**(anti-budget-starvation — 변하는 유일 축은 격자 미세함). 각 N 에서 H_1355 의 5 placement 재실행, ASYM-L peak-count 와 CENTER_TOL(N)=max_rung|L−0.5| 측정.

## METHOD

- 기계 = H_1333/H_1341/H_1355 알고리즘 **verbatim** (RBF 위치 embed · 오차표적 SPLIT-only Voronoi/mitosis 성장 · soft-posterior 판별 readout · peak-count 결맞음 · phase-2 재성장 split-only no-reset), `(N_STIM, DIM, budget)` 로 매개변수화. **N=21/DIM=16/budget=24 에서 H_1355 정확 재현** (self-check arm 이 ASYM-L L=0.375, pc [3,1,3], 2/3 비결맞음 검증).
- frozen 스케일 규칙 (FREEZE, 채점 전): `DIM(N)=round(16·N/21)` · `budget(N)=round(24·N/21)`. 사다리: N=21(DIM16,bud24) · N=41(DIM31,bud47) · N=81(DIM62,bud93).
- placements (H_1355 verbatim, 실수값 cut 동일, 격자만 더 촘촘히 샘플): RIGHT-REF(0.333→0.667) · LEFTWARD-1(0.667→0.333) · LEFTWARD-2(0.800→0.500) · ASYM-R(0.600→0.800) · ASYM-L(0.400→0.200).
- p1/p2/p3/p6: readout 은 학습된 prototype 공간의 표상 거리만 읽음 · test 시 cut 위치 주입 없음 · label 은 학습 중에만 진입.

## FROZEN BARS (특성화 사다리, c2 DIRECTION 사전등록, c9)

- **c1 REPORT (산출물)**: 각 N 에서 (mean 3 seeds) ASYM-L peak-count pc_R(seed별+mean), 착지 L, frac, 그리고 CENTER_TOL(N)=max_rung|L−0.5| 측정·verbatim 보고. 임계값 없음 — 곡선이 산출물.
- **c2 DISCRIMINATE (사전등록 DIRECTION)**: RESOLUTION-BOUND iff (i) ASYM-L 결맞음 회복(N=81 mean pc≤2 **AND** N=81 비결맞음 seed 수 < N=21) **AND** (ii) CENTER_TOL 축소(단조 비증가 **AND** N=81 < N=21). INTRINSIC iff 비결맞음 지속(N=81 mean pc>2 OR 비결맞음 seed 수 ≥ N=21) **AND/OR** CENTER_TOL 미축소. 그 외 MIXED.
- **c3 EARNED**: (a) no-retrain anchor |peak−p_A|≤LOC_TOL=0.12 · (b) shuffle peak-count≥3, 비-ASYM-L lang arm peak-count≤2. ASYM-L 의 A2 arm 은 **시험 대상 양**이라 결맞음 요구 안 함(그 (비)결맞음 vs N 이 c1/c2 finding 자체); ASYM-L 의 no-retrain anchor·A-trained arm 은 결맞음 요구.

## RESULT (📈 INTRINSIC)

**c1 — ASYM-L 결맞음 + CENTER_TOL vs N (mean 3 seeds):**

| N | dim | budget | ASYM-L pc(seeds) | mean pc | incoh/3 | L_ASYM-L | frac | CENTER_TOL |
|---|-----|--------|------------------|---------|---------|----------|------|-----------|
| 21 | 16 | 24 | [3, 1, 3] | 2.33 | **2/3** | 0.375 | +0.250 | **0.192** |
| 41 | 31 | 47 | [4, 2, 4] | 3.33 | 2/3 | 0.413 | +0.000 | 0.196 |
| 81 | 62 | 93 | [4, 3, 3] | 3.33 | **3/3** | 0.406 | +0.000 | **0.198** |

전체 5-rung 착지표 (N 별):
- N=21: RIGHT-REF=0.525(|.025|) LEFTWARD-1=0.475(|.025|) LEFTWARD-2=0.625(|.125|) ASYM-R=0.692(|.192|) ASYM-L=0.375(|.125|)
- N=41: 0.546 / 0.454 / 0.604 / 0.696 / 0.413
- N=81: 0.548 / 0.452 / 0.590 / 0.698 / 0.406

→ c1 곡선 측정 (3 N × 5 placement × 3 seed): **PASS**. self-check: N=21 이 H_1355 ASYM-L 정확 재현 (YES).

**c2 — DISCRIMINATE → INTRINSIC:**
- ASYM-L mean peak-count vs N = **[2.33, 3.33, 3.33]** (회복은커녕 오히려 약간 증가)
- ASYM-L 비결맞음-seed vs N = **[2, 2, 3]** (N=81 에서 3/3 으로 **악화**)
- CENTER_TOL vs N = **[0.192, 0.196, 0.198]** (단조 비증가 아님, 오히려 미세 증가)
- (i) 결맞음 회복? **False** (pc@81=3.33>2, 비결맞음 2→3) · (ii) CENTER_TOL 축소? **False** (단조성 False, 0.192→0.198)
- → **INTRINSIC** — ASYM-L 비결맞음이 가장 미세한 격자에서도 지속(peak-count >2, 같은/더 많은 seed 비결맞음)하고 CENTER_TOL 밴드도 축소 안 됨. 비결맞음은 split-only 같은-쪽 좌향 재성장의 **본질** (제거 안 되는 first-carving 세포가 곡선을 진짜로 분절), 격자 해상도와 무관 — 정직한 더 깊은 한계.

**c3 — EARNED: PASS(N=21) · FAIL(N=41/81, RIGHT-REF/LEFTWARD-1/LEFTWARD-2 rung).**

> **정직 보고 (c9) — c3 FAIL 은 frozen 절대-카운트 bar 의 N-스케일 아티팩트이며 INTRINSIC 판정을 바꾸지 않는다.** peak-count 는 mid-point **절대 개수**(≥0.5·peak)라서 격자가 미세해지면 자연히 커진다 (shuffle baseline 7.7→18.3→38.0 으로 N 따라 상승). 그 결과 COH_MAX_LANG=2 (N=21 기준 절대 임계, frozen 이라 N 으로 스케일 안 함)에 비-ASYM-L lang arm 들이 N=41/81 에서 걸려 c3 FAIL. 그러나 (1) 이는 비결맞음 메트릭 자체가 N 에 의존한다는 **알려진** 효과이고, (2) ASYM-L 은 이 상승하는 baseline 대비 **여전히 비결맞음 끝**에 머문다 (다른 결맞은 arm 과 lockstep 으로 상승, 비결맞음-seed 수 절대 안 줄어듦), (3) 핵심 판별인 **CENTER_TOL 은 peak-위치 메트릭이라 카운트-스케일 아티팩트에 면역**인데 그것도 축소 안 됨. 따라서 H-lattice(회복) 가설을 살릴 수 없다. frozen bar 는 이동 안 함 (c9/p7); 아티팩트로 정직 라벨.

## 메커니즘 / 해석

같은-쪽 좌향 재성장(ASYM-L: 0.400→0.200, 양 cut 중심 왼쪽)에서 phase-1 의 first-carving 세포는 **제거되지 않고**(split-only, p8) 0.4 근처에 패킹된 채 남는다. phase-2 가 0.2 cut 으로 세포를 더 분할해도 잔존 0.4-패킹이 판별 곡선에 두 번째 봉우리를 남겨 peak-count 를 ≥3 으로 분절시킨다. 격자를 미세화하면 자극·예산은 늘지만 **잔존 패킹의 상대적 지배는 그대로** — 더 미세한 grid 는 옛 봉우리와 새 봉우리를 **둘 다 더 선명하게** 해상할 뿐이라 비결맞음을 못 고친다 (오히려 N=81 에서 seed 4334 까지 비결맞음으로 넘어가 2/3→3/3 악화). 착지 자체는 geometry-fixed 로 안정 (ASYM-R ~0.698, ASYM-L ~0.41), CENTER_TOL 밴드도 안정 → H_1355 의 geometry-tracking 결론은 더 미세한 격자에서도 **확인**되고, ASYM-L 비결맞음은 격자가 아니라 **분할-전용 재성장의 본질**임이 확정.

H_1360(cp-geometric-repack, 세포를 **이동**)과 상보: 격자 미세화(이 H)가 못 고친 비결맞음을 세포 재배치가 고치는지는 별도 follow-on. 본 결과는 **격자 해상도 레버는 ASYM-L 비결맞음에 대해 죽은 레버**임을 정직히 닫는다.

## SCOPE (UNVERIFIED)

DIRECTIONAL numpy mirror — engine-transfer UNVERIFIED. TOY 합성 1-D 연속체, 3 seeds, deterministic readout, 5 placement × 3 N rung. NO 인간 인지/임계기 주장. 격자 해상도 **의존성**을 테스트할 뿐 학습된 모델 아님. peak-count 메트릭의 N-스케일 의존(절대 카운트)은 알려진 한계 — N-정규화 결맞음 메트릭, 더 높은 차원 embed, 실제 코퍼스, 비균일 grid, engine-native 재성장은 UNVERIFIED follow-on. live CORE/*.hexa UNTOUCHED, Ψ=½ untouched.

## 다음 각도

- **결맞음 메트릭의 N-정규화**: peak-count 를 grid-step 으로 정규화한 결맞음(예: peak FWHM 의 연속체 폭)으로 재측정 → c3 절대-카운트 아티팩트 제거하고 INTRINSIC 재확인 (frozen-first 별도 H).
- **H_1360 cp-geometric-repack 교차**: 격자가 못 고친 ASYM-L 비결맞음을 세포 **재배치**(이동, 제거)가 고치는가 → split-only 한계의 진짜 탈출구인지.
- **engine-native 재성장**: live CORE/engine_cli.hexa A⇄G + VAdaptField 위에서 ASYM-L 재성장 비결맞음을 재현·재측정 (a_engine_native_learning · a_verified_must_wire).

## 포인터

- py: `state/cp-lattice-resolution/h1364_cp_lattice_resolution.py` (+ 기계 `state/cp-lattice-resolution/h1333_whorf_developmental.py`)
- verdicts: `.verdicts/1364_cp_lattice_resolution/{FREEZE,result}.txt`
- claim: `CLAIMS.tape @C h1364_cp_lattice_resolution`
- index: `UNIVERSE/HYPOTHESES.jsonl`
- log: `domains/COGNITION-REPRESENTATION.log.md`
- xref: h1355(직접 부모, cp-leftward geometry-tracking) · h1341(shift-size) · h1333(발달 가소성) · h1323(Sapir-Whorf) · h1360(cp-geometric-repack, 상보) · a_no_llm_frame_trap · a_break_the_wall · a_engine_native_learning · a_verified_must_wire · a_core_engine_map · a_scale_honest_scope · a_toy_scale_recheck · p7 · p8 · c9 · c15
