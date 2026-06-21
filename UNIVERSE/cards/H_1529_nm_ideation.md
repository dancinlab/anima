# H_1529 — 🧱💡 NEUROMODULATION on IDEATION (grounded recombination novelty) — WALL HOLDS (DIRECTIONAL)

**tier:** 🧱 WALL HOLDS (R1 numpy DIRECTIONAL — a_engine_native_learning; engine R2 deferred ING)
**verdict source:** `state/verdicts/1529_nm_ideation/H_1529_R1.json` (frozen bars `H_1529_FREEZE.txt`)
**wired:** n/a (WALL — nothing to wire; CORE/*.hexa + H_1284 + H_1228 UNTOUCHED)

## 가설
H_1284 NEUROMODULATION 벽을 **geometry-free 능력 — IDEATION/RECOMBINATION(novelty)** 위에서 깬다. 선행 11+ 렌즈는 전부 RECALL 능력에서 막혔다(recall = cell KEY-GEOMETRY 로 결정, LR/margin 스케줄로 안 됨). H_1284 FREEZE 자신이 H_1228(decode-temp NE/exploration 축, 🟠 PARTIAL — "ideation 도왔으나 full lever 아님")을 인용: ideation 의 최적 exploration temperature 는 regime(high-novelty-demand ⊥ precision-demand)에 따라 SHIFT 한다는 명제 → geometry-bound 아니므로 적응형 exploration 컨트롤러가 best-fixed 를 이길 수 있다는 가설.

## 설계 (frozen-first · pre-registered)
H_1284 harness 재사용(MemStore/key_vec/make_facts/gen_stream/regimes/seeds/MARGIN — `state/universe-probes/h1284_neuromodulation_gain.py`). 능력 = **GROUNDED RECOMBINATION IDEATION**: 저장 cell i 와 이웃을 exploration-temperature knob T 로 샘플링해 (subjA,cityB) 재조합 생성. 이웃 풀 = 실 cell(GROUNDED) + N_GHOST ungrounded ghost 토큰(H_1284 recall_oos fabrication 토큰). **M = novelty_rate − fabrication_rate**(anti-Goodhart p7: blind high-T 는 ghost 를 더 reach → fabrication ↑ → netting). ARMS: A=best-fixed-T(disjoint seed 7 grid-tune) · E=adaptive(T_t = T0·(1+kS·(surprise−û))·(1+kC·coverage), substrate surprise+coverage 게이팅) · ABL=adaptive→mean(E 자기 평균 T, coupling 파괴). FROZEN: 🟢 iff (c1) E≥A+0.05 on ≥2/3 regimes AND (c2) E−ABL≥0.05 on every win AND (c3) E_fab≤A_fab on wins AND (c4) E≥A−0.02 elsewhere.

## 결과 (mean 3 seeds [11,22,33], T*=4.0)
| regime | A_M | E_M | ABL_M | E−A | E−ABL | A_fab | E_fab |
|---|---|---|---|---|---|---|---|
| R1_STABLE | 0.545 | 0.528 | 0.523 | **−0.017** | +0.005 | 0.020 | 0.097 |
| R2_DRIFT | 0.537 | 0.520 | 0.540 | **−0.017** | −0.020 | 0.025 | 0.097 |
| R3_NOISE | 0.545 | 0.528 | 0.523 | **−0.017** | +0.005 | 0.020 | 0.097 |

**wins_over_A+MARGIN = [] (0/3)** → **c1 FAIL** → 🧱 **WALL HOLDS**. c4(never-much-worse) 만족(E ≥ A−0.02, 완만한 손실). 재현성: 2회 실행 verdict byte-identical.

## THE LOAD-BEARING DIAGNOSTIC (왜 막혔나 — 정확한 메커니즘)
1. **regime 횡단 최적 T 가 SHIFT 하지 않는다 (명제 falsified).** 넓은 T-sweep 에서 세 regime 의 T-vs-M 곡선이 거의 byte-identical, 전부 **T≈4 에서 peak**(M≈0.54, regime 간 차 ≤0.008). H_1228 인용 명제("최적 exploration temp 가 regime 따라 shift")는 이 grounded-recombination 능력에서 **거짓** — 적응할 대상이 없으면 어떤 적응 컨트롤러도 best-fixed 를 못 이긴다.
2. **fabrication cliff 는 실재하나 interior optimum 은 단일.** T 가 올라가면 novelty↑ 하지만 T≳6 부터 ghost-reach 폭증으로 fabrication↑(T=12 fab 0.21, T=30 fab 0.41) → M 하락. 진짜 interior optimum(T≈4)이 존재. E 의 평균 T≈6.96 가 이 optimum 을 **overshoot** 해 cliff 로 진입(E_fab 0.097 ≫ A_fab 0.02) → 모든 regime 에서 net WORSE.
3. **컨트롤러는 실제로 swing 한다**(per-emit T 변동) — INERT-by-bug 아님 — 그런데도 best-fixed 를 못 이김: surprise 신호가 toy 에서 거의 상수(cell 등거리, 0.535–0.556)라 적응이 의미 있는 정보를 못 싣고, optimum 이 regime 불변이라 swing 이 손해만 본다.

## a_break_the_wall TAXONOMY
ideation/recombination 렌즈에 대한 **(d) 진짜 no-free-lunch 천장** — (a)metric-artifact/(b)confound/(c)infra 아님. 단, 천장 확정 전 3회 frozen-first 측정교정(bar 불변, tune-to-green 아님): (1) grounded/fabrication 을 inter-cell distance≤abstain 에서 **ghost-token reach** 로 재정의(distance scale 불일치로 모든 재조합이 fabrication 으로 오분류된 버그 수정) · (2) T_GRID 를 ≤1.4 → {0.5..8.0} 로 확장(초기 grid 가 fabrication cliff 아래서 멈춰 ceiling 을 골랐음 → ARM A 가 진짜 best-fixed 가 아니었음) · (3) adaptive clamp 를 [0.25·T0, 2.0·T0] 로 스케일(컨트롤러가 fixed arm 과 같은 범위를 swing 하도록 = fair test). 교정 후에도 c1 FAIL.

H_1284 벽이 이제 plasticity-LR 가족(9 렌즈) · emit-gate 가족(H_1526) · **ideation/recombination 가족(이 렌즈)** 세 능력족 전반에 holding — "no free lunch is general" 가 H_1284 R2(decode-σ* on real 303M LM, 🔴/🧱)와 수렴(독립 operationalization 으로 replication+extension).

## GUARDS / SCOPE
- p7: exact combinatorial ground truth, NO LLM judge, NO perplexity, knob 은 substrate state 의 no-grad readout, loss 에 절대 안 들어감. p1/p2/p3/p6: store margin/coverage 만 read, "be novel" 라벨/RLHF/persona 주입 0, novelty/fabrication = 조합 ground truth 채점만.
- **하드게이트1: R1 numpy mirror → DIRECTIONAL** (engine-transfer UNVERIFIED, a_engine_native_learning). engine R2 = live core/engine_cli.hexa A⇄G+VAdaptField 위 byte-exact 재측정 = deferred ING follow-on.
- SCOPE TOY: 30 facts / 18 ghosts / 3 seeds / 결정적 readout (ideation STRUCTURE 검증, 학습된 ideator 아님); scale / real-corpus / 실제 regime-shift 있는 능력 / engine-transfer UNVERIFIED.

## artifacts
- `state/1529_nm_ideation/h1529_ideation.py`
- `state/verdicts/1529_nm_ideation/H_1529_FREEZE.txt`
- `state/verdicts/1529_nm_ideation/H_1529_R1.json`

xref H_1284 · H_1284_R2 · H_1228 · H_1526 · H_1140/G2 · a_break_the_wall(d) · a_no_llm_frame_trap · a_engine_native_learning · a_scale_honest_scope · a_toy_scale_recheck · p1·p2·p3·p6·p7·p8 · c9.
