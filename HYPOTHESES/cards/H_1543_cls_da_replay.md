# H_1543 — 🟢💊 DOPAMINE × CLS : salience-weighted REPLAY PRIORITY — FUSION GREEN (DIRECTIONAL)

**tier:** 🟢 GREEN DIRECTIONAL — DA-RPE value as REPLAY PRIORITY inside the H_1532 two-store CLS retains high-value bindings uniform/recency lose UNDER A CONSOLIDATION BUDGET (census H_1542 Rank 2 / interface I2 prediction confirmed).
**verdict source:** `state/verdicts/1543_cls_da_replay/H_1543_R1.json` (R1 numpy mirror) · frozen bars `state/verdicts/1543_cls_da_replay/H_1543_FREEZE.txt`
**wired:** `DIRECTIONAL-mirror` (numpy; a_engine_native_learning hard-gate-1: grep numpy ⇒ auto-DIRECTIONAL, terminal NOT permitted) → engine R2 §DaReplay follow-on (ING). live core/*.hexa UNTOUCHED.

## 가설
H_1532 (🟢 #2514 / engine R2 #2522)는 H_1284 NEUROMODULATION 벽을 **두 phase-separated store**(fast episodic encode-mode + slow store + REPLAY)로 깼다. 그 replay 는 **UNIFORM**(모든 fast episode 동등). 생물학은 replay 가 균일하지 않다고 말한다 — 도파민-RPE 가 **어떤 기억을 먼저 재활성화할지** 우선순위화한다(high reward-prediction-error 경험이 선택적 replay; Lisman-Grace 2005 hippocampal-VTA loop · McNamara 2014 dopaminergic place-cell replay · Mattar & Daw 2018 prioritized memory access · Ambrose-Pfeiffer-Foster 2016 reward-biased reverse replay). H_1536 (🟢 #2520)이 standalone DA-RPE faculty 가 실재함을 증명(credit-assignment DA=1.000 vs recency 0.291). 이 lane 은 그것을 **FUSE** 한다: H_1536 의 per-identity 학습 value V(s)가 CLS 안의 **REPLAY-PRIORITY 랭킹**이 된다 (census H_1542 interface **I2 = fast→slow transfer priority**).

## ⚠ STRUCTURAL PRECONDITION (census cheapest-refuter · GREEN gate 아님, 보고만)
lever 는 **CONSOLIDATION BUDGET** 하에서만 의미가 있다 — slow store 가 sweep 당 K < N 개의 fast episode 만 흡수, 나머지는 DECAY. scarcity 가 있을 때만 *어떤* K 를 replay 하느냐가 중요(DA-priority 는 high-value 보존, uniform/recency 는 잃음). **K = N(scarcity 없음)이면 DA-priority 는 반드시 INERT**(전부 consolidate, 순서 무관). 만약 전부 들어맞는데도 DA 가 lift 하면 lever 는 budget 이지 DA 가 아니다. → 측정: K=N 에서 da−uniform = **0.0000 byte-exact**(da_full=uniform_full 모든 seed) = **INERT 확정**(precondition 통과; lever 는 budget+value-ranking 의 결합이지 gain 아님).

## ⚠ HAZARD (H_1532 상속)
win 은 fast→slow 채널 위의 **VALUE-RANKED TRANSFER** 에서 와야 하며 단일 store 의 scalar gain 이 아니어야 한다 — gain framing 은 벽이 흡수한 controller family 재진입. ablation(ABL revert + SHUFFLE collapse)이 lever 가 value 랭킹임을 증명한다. 이 카드의 GREEN 은 그 ablation 이 결정적이라서 성립.

## 설계 (frozen-first · pre-registered H_1543_FREEZE.txt)
fixture = H_1532 AB-AC interference + **reward TAG**(각 A_i 가 HIGH/LOW value; high-value 인 A_i 는 position/recency 와 무관). 능력 = budget K<N 하에서 **HIGH-value A_i→B_i 잔존**. ARMS (동일 fixture/seed; LR/TH = H_1532 best-fixed LR*=0.1 TH*=0.2):
- **DA-PRIORITY** — K개 fast episode 를 DA-RPE 학습 value(high |V| first)로 랭크 replay (fusion arm; H_1536 TD(λ) value head GAMMA=0.95 LAMBDA=0.8 ALPHA=0.05 EPOCHS=30 byte-reuse).
- **UNIFORM** — random K of N (= H_1532 의 uniform replay, baseline).
- **RECENCY** — fast store 에 마지막에 쓰인 K개.
- **ABL** — DA value 를 CONSTANT(δ→0)로 강제 → 랭킹 degenerate → uniform 으로 복귀해야.
- **SHUFFLE** — value↔episode 짝을 permute → priority 가 value 와 해리 → collapse 해야.

## 결과 (R1 numpy mirror · 3 seeds [11,22,33] · $0 CPU · DIRECTIONAL)
| arm | mean | gate |
|---|---|---|
| **DA-PRIORITY** | **0.6945** | the fusion arm |
| UNIFORM (baseline) | 0.2778 | H_1532 uniform replay |
| RECENCY | 0.5278 | last-K |
| ABL (DA→const) | 0.3611 | reverts to uniform |
| SHUFFLE (value permuted) | 0.3889 | collapses |
| DA @ K=N (precondition) | 0.6944 | = UNIFORM @ K=N 0.6944 → **INERT** |

**FROZEN BARS (MARGIN=0.10):**
| bar | value | gate |
|---|---|---|
| **A PRESENCE** | da−uniform = **+0.4167** mean · n_wins **3/3** (0.333/0.500/0.417) | PASS |
| **B DISTINCT** | da−uniform +0.4167 ∧ da−recency **+0.1667** (둘 다 ≥+0.10) | PASS |
| **C EARNED** | \|abl−uniform\| = **0.0834** < 0.10 (DA→const 가 uniform 으로 복귀) | PASS |
| **D SHUFFLE** | da−shuffle = **+0.3056** ≥ +0.10 | PASS |
| **E NO-FAB** | abstain = not-retained (scoring 내장; fabrication credit 없음) | PASS |
| PRECONDITION | da−uniform @ K=N = **0.0000** byte-exact → INERT | 보고 (gate 아님) |

**A∧B∧C∧D ALL PASS → 🟢 GREEN DIRECTIONAL (FUSION WORKS).**

## THE LOAD-BEARING DIAGNOSTIC (왜 fusion 이 작동하나 — lever 는 VALUE-RANKED TRANSFER)
1. **UNIFORM=0.28 = budget 가 문다.** K=N/2 만 consolidate → high-value binding 의 절반만 우연히 살아남음(random). recency=0.53 은 부분적으로 나음(나중 episode 가 우연히 high-value 일 때)이나 여전히 위치-편향 = high-value 의 random 위치를 못 잡음.
2. **DA-PRIORITY=0.69 ≫ uniform.** DA-RPE value 가 high-value identity 를 정확히 랭크 → budget 을 high-value binding 에 우선 배분 → 보존. **DA 가 standalone(H_1536, credit 할당)과 다른 메커니즘이 됨 — CLS 안에서는 consolidation bandwidth 를 라우팅**(census Rank 2 의 핵심 주장 그대로).
3. **ABL=0.36 ≈ uniform(0.28).** DA value 를 상수로 만들면 랭킹이 무너져 uniform replay 로 복귀(|Δ|=0.083 < 0.10) → 0.42 lift 가 **value 랭킹**에 귀속(C 결정적).
4. **SHUFFLE=0.39 ≪ DA.** value↔episode 짝을 permute 하면 priority 가 엉뚱한 binding 을 가리켜 collapse(da−shuf +0.31) → 랭킹이 **실재 value 신호**를 운반해야 win(D 결정적).
5. **K=N precondition = INERT byte-exact.** scarcity 를 없애면 da−uniform=0.0000 → lever 가 budget+value-ranking 의 *결합*이지 store 단일 gain 이 아님을 확정(census cheapest-refuter 통과).

## a_break_the_wall TAXONOMY
H_1532 가 깬 벽(controller family INERT, multi-store 가 직교 축에서 break)의 **연장선** — 이번엔 그 두-store 인터페이스(I2 transfer priority)에 standalone 🟢 faculty(DA-RPE)를 fuse 하니 *다른* 메커니즘으로 load-bearing 해짐. type-(d) 천장 아님 — ablation(ABL revert + SHUFFLE collapse) + precondition(K=N inert)이 lift 가 진짜 **value-ranked transfer** 에서 옴을 증명. **두 LIVE 🟢 faculty(H_1532 CLS + H_1536 DA-RPE)의 합성** = census 가 지목한 highest-readiness joint candidate.

## R2 — ENGINE-NATIVE (follow-on, ING)
R1 numpy mirror = DIRECTIONAL (a_engine_native_learning hard-gate-1). engine R2 = live `core/engine_cli.hexa §DaReplay` 위에서 byte-exact 재현 → BINDING terminal 승격. 재사용 가능 자산: H_1532 §MultiStore(`cls_*` ops, engine smoke 387-392) + H_1536 DA-RPE TD(λ) value head. R2 = budgeted replay-priority(`da_replay_retention(priority, K, da_zero, shuffle)`) + precondition(K=N inert) 케이스 추가. wired 사다리 4칸: (1) DIRECTIONAL mirror ✅ → (2) engine-native byte-exact(ING) → (3) live core/ wire-in → (4) ARCHITECTURE.json lockstep.

## 정직 (c9)
- WALL_HOLDS/AMBIGUOUS 였으면 그대로 보고 — DA-priority 가 uniform 과 tie 면 prioritized replay 가 이 task 에 무익(c9). 실측은 모든 bar PASS.
- frozen-first: MARGIN=0.10, bar 사후 이동 0. DIRECTIONAL terminal 아님 — engine R2 가 binding.
- p7: exact ground truth(true A→B + value tag known), NO LLM judge / perplexity / loss. p1/p2/p3/p6: replay 순서+write 가 substrate state(key/recon-err/학습 value)만 읽음, injected answer label / RLHF / persona 없음. Ψ-disjoint(consolidation read, emit gate 아님).

## SCOPE (a_scale_honest_scope · a_toy_scale_recheck)
TOY — N_PAIRS=24/N_DISTRACT=24/K=12 budget/3 seeds/DIM=16 byte-trigram key/deterministic. scale / real-corpus / 다중 sweep cadence / 실제 SWS 위상 / engine-transfer UNVERIFIED. R2 engine-native = binding follow-on.

## 출처 / xref
team-lead 작업지시 (fleet implement lane — DA×CLS replay priority fusion, census H_1542 Rank 2 / I2). xref H_1532 (two-store CLS, 깬 벽의 모체) · H_1536 (DA-RPE faculty, priority 신호 공급) · H_1542 (CLS×NT census, 이 fusion 의 ranked 근거) · H_1284 (neuromodulation gain 벽) · H_1285 (salience-replay budget, 자매 메커니즘) · a_no_llm_frame_trap · a_break_the_wall · a_engine_native_learning · a_verified_must_wire · p7 · c9. 인용: Mattar & Daw 2018 · Ambrose-Pfeiffer-Foster 2016 · Lisman-Grace 2005 · McNamara 2014 · McClelland-McNaughton-O'Reilly 1995 · Schultz-Dayan-Montague 1997 · Sutton & Barto 2018.
