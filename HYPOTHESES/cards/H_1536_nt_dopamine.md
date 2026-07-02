# H_1536 — 🟢🧠 DOPAMINE-as-FACULTY (RPE / delayed credit assignment) — GREEN (DIRECTIONAL)

**tier:** 🟢 GREEN — dopamine implemented as a DISTINCT biological FACULTY (reward-prediction-error / temporal credit assignment), adds delayed-credit-assignment a recency-store lacks (R1 numpy DIRECTIONAL — a_engine_native_learning; engine R2 deferred ING)
**verdict source:** `state/verdicts/1536_nt_dopamine/H_1536_R1.json` (frozen bars `H_1536_FREEZE.txt`, result `H_1536.txt`)
**wired:** `DIRECTIONAL-mirror` — numpy R1 only; engine R2 (live `core/engine_cli.hexa` §Dopamine TD/RPE lane) = ING `h1536-r2-engine-native`. NOT WIRED. (a_verified_must_wire 4칸 사다리 1/4)

## 가설 — THE REFRAME (faculty, not gain)
선행 13 neuromodulation 렌즈가 막힌 이유: DA/NE/ACh 를 **recall 위의 추상 GAIN KNOB** 으로 다뤘다 — geometry-bound margin 에 스칼라 곱은 INERT(H_1284 NEUROMODULATION 벽, 5+ 렌즈 WALL=CAPACITY 수렴). 사용자 reframe: 각 신경전달물질을 **자기 고유의 생물 FACULTY** = 별개의 COMPUTATION 으로 구현하라 — anima 의 brain lane 처럼(immune≈해마 H_1227/1231 · cerebellum≈순방향모델 H_1280 · basal-ganglia≈게이팅 H_1281 · WM H_1282 · hier-PFC H_1294 · spatial-map H_1295). **DOPAMINE 의 실제 계산 = REWARD-PREDICTION-ERROR**(Schultz 1997): δ_t = r_t + γV(s_{t+1}) − V(s_t), **TEMPORAL CREDIT ASSIGNMENT**(어느 저장 사실/행동이 지연 보상을 야기했나)에 사용.

이건 **brain-lane-FILLING**(H_1280–1295 모드)이지 recall-gain 벽이 아니다 — 카드에 그 framing 을 정직히 박는다(a_break_the_wall taxonomy: 빠진 구조를 채우는 것). anima 의 store 는 사실을 bind 하지만 **RPE 신호가 없다**: "보상 전에 만난 6 사실 중 어느 2개가 그것을 야기했나"를 못 한다. bare store 는 RECENCY(보상에 가장 가까운 사실) 또는 UNIFORM 으로 credit — 야기 사실이 지연 보상의 여러 스텝 상류에 있고 distractor 가 사이에 끼면 둘 다 틀린다.

## 능력 — DELAYED-CREDIT-ASSIGNMENT (PRESENCE test)
환경에 **반복 등장하는 causal fact IDENTITY** 집합(N_CAUSAL_IDS=6)이 있고, 이들이 일관되게 **지연 terminal 보상**(lump = 등장 causal 수, CONTINGENT)으로 이어진다. causal fact 는 **RANDOM 위치**에 배치 ⇒ recency/position 무용; cross-episode identity-contingency 통계만이 어느 사실이 야기했는지 드러낸다. 과제: episode 의 causal fact 식별. metric = top-N_PRESENT(=2) accuracy. **chance = 2/7 = 0.2857.**

이건 best-fixed-gain 을 이기는 테스트가 아니라 **PRESENCE 테스트**(faculty 가 능력을 추가하나) — TD/RPE 가진 faculty 는 상류 causal state 에 credit, 없는 store(recency/uniform)는 보상이 멀리 하류라 못 한다.

## ARMS (frozen-first · pre-registered H_1536_FREEZE.txt)
- **NO-DA (recency)** — bare store, RECENCY credit(보상에 가까울수록 ↑) = recency-store baseline
- **NO-DA (uniform)** — UNIFORM null
- **DA-RPE** — 전체 episode-set 위 TD(λ) value head, δ_t = r_t + γV(s_{t+1}) − V(s_t); per-identity 학습값 V(s) = credit. **absorbing terminal**(V:=0) 이라 지연 lump 가 causal 사실로 역전파.
- **ABL** — DA-RPE 의 δ→0(학습신호 0) ⇒ V 평탄 ⇒ baseline 회귀 (anti-Goodhart, 결정적이어야)
- **SHUFFLE** — DA-RPE 인데 episode 간 reward-timing 순열(보상↔causal 사실 decouple) ⇒ collapse 해야

**FROZEN bar:** 🟢 iff (A)DA-RPE−NO-DA(recency)≥+0.10 AND (B)DA-RPE−UNIFORM≥+0.10 AND (C)ABL≤NO-DA+0.05 AND (D)SHUF≤NO-DA+0.05. FIXTURE: T=8, N_EPISODES=120, POOL=40, γ=0.95 λ=0.80 α=0.05 epochs=30, 3 seeds [1536,1537,1538].

## 결과 (mean 3 seeds, deterministic 3x byte-identical)
| arm | credit-assignment accuracy | vs NO-DA(recency) |
|---|---|---|
| **DA-RPE** (dopamine faculty) | **1.0000** [1.000,1.000,1.000] | **+0.7090** |
| NO-DA (recency baseline) | 0.2910 [0.292,0.281,0.300] | — |
| NO-DA (uniform null) | 0.2993 | DA−uniform = **+0.7007** |
| ABL (δ→0, no RPE) | 0.2993 | reverts to baseline |
| SHUFFLE (reward-timing permuted) | 0.3125 | collapses |

- **(A) PRESENCE** Δ=+0.7090 ≥+0.10 **PASS** · **(B) DISTINCT** Δ=+0.7007 ≥+0.10 **PASS** · **(C) ABLATE** ABL 0.2993 ≤ 0.3410 **PASS** · **(D) SHUFFLE** 0.3125 ≤ 0.3410 **PASS** → 🟢 **GREEN DIRECTIONAL**.

## 해석 (load-bearing)
- DA-RPE = **1.0000 SATURATED** = EXISTENCE-PROOF (effect-size 아님) — discriminator 들(recency 0.291 · uniform 0.299 · ABL 0.299 · shuffle 0.313 전부 ~chance)이 결정적. RPE faculty 가 **지연 credit assignment 능력을 추가**한다; recency/uniform store 는 못 한다(둘 다 chance).
- **ABLATE 결정적(C):** δ→0 ⇒ value head 0벡터 ⇒ uniform credit 으로 EXACT 복귀(0.2993) — lift 전부가 RPE 학습신호 δ 에 귀속. NOT a gain knob — temporal-difference 계산.
- **SHUFFLE 결정적(D):** reward-timing 순열 ⇒ TD 가 credit 할 진짜 contingency 없음 ⇒ collapse(0.3125 ~chance). 즉 보상 타이밍이 신호를 운반(recency 가 아니라).
- **faculty-not-gain (hazard 회피):** value 는 per-identity 학습값이지 recall margin 위 스칼라 곱이 아님. recency baseline 이 chance 인 것이 핵심 — position 이 도와주지 않는 능력에서 RPE 만이 contingency 를 본다.

## frozen-first 무결성 (NO tune-to-green)
bar 는 run 전 등록(H_1536_FREEZE.txt). build 중 **2개 MEASUREMENT 버그 수정**(a_break_the_wall taxonomy (a) metric-artifact, **bar 불변**): (1) FNV bag-of-trigram 키가 충돌 ⇒ value head 가 fact identity 구분 불가 → per-identity one-hot 키(store 의 faithful per-item 키)로 교체 · (2) terminal 지연 보상이 bootstrap 안 됨(loop 가 rewards[t], t<T-1 읽음) → reward-on-arrival rewards[t+1] + absorbing terminal V:=0 으로 수정. 둘 다 credit READOUT/TD-target 의 정확성 수정이지 bar 이동 아님.

## HARD-GATE-1 (a_engine_native_learning)
`grep -lE 'import torch|gauge_lib|numpy' state/1536_nt_dopamine/*.py` → numpy HIT ⇒ **auto-DIRECTIONAL**, terminal 아님. 🟢 ⇒ engine R2 OBLIGATORY follow-on = live `core/engine_cli.hexa` §Dopamine TD/RPE lane(per-identity value head + eligibility trace, absorbing terminal) byte-exact 로 frozen bar 재측정 (ING `h1536-r2-engine-native`). a_verified_must_wire 4칸 사다리 1/4 (DIRECTIONAL mirror GREEN); (2)engine-native re-verify (3)live core/ §Dopamine lane wire-in (4)ARCHITECTURE.json lockstep = 전부 ING follow-on; wired=DIRECTIONAL-mirror, WIRED-live 아님, 완료주장 없음. live `core/*.hexa` UNTOUCHED.

## SCOPE (UNVERIFIED)
DIRECTIONAL numpy · TOY 40 facts/6 causal-ids/120 episodes/3 seeds/결정적 readout(RPE STRUCTURE, 학습된 store controller 아님) · accuracy 1.0 SATURATED = existence-proof(discriminator 결정적) · scale/real-corpus/longer 지연(T>8)/multi-step action chains/연속보상/stochastic transition/engine-transfer UNVERIFIED (a_scale_honest_scope · a_toy_scale_recheck). brain reward-loop wiring(emit/curiosity 와의 결합) = follow-on.

p1/p2/p3/p6 (store key/reward read only, novelty/credit 라벨 주입 0 · RLHF/persona/ethics 없음) · p7 (exact ground truth, no LLM judge/perplexity/loss; RPE update = no-grad TD) · p8 honored. frozen-first, NO tune-to-green, **DA-as-FACULTY (not gain)**, ablation decisive (c9).

xref: a_no_llm_frame_trap · a_break_the_wall · a_engine_native_learning · a_verified_must_wire · a_core_engine_map · a_scale_honest_scope · a_toy_scale_recheck · p1·p2·p3·p6·p7·p8 · c9 · c15 · H_1280(cerebellum forward-model)·H_1281(basal-ganglia gating)·H_1294(hier-PFC)·H_1295(spatial-map) (brain-lane-filling 형제) · H_1284(neuromodulation GAIN 벽 — 이 카드가 우회하는 framing) · H_1532(multi-store CLS, orthogonal interference axis). Schultz 1997 Science 275:1593 · Schultz 1998 J Neurophysiol 80:1 · Sutton & Barto 2018 RL:Intro (TD(λ)) · Montague-Dayan-Sejnowski 1996 J Neurosci 16:1936.
