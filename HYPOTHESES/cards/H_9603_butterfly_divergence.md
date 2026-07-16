# H_9603 — BUTTERFLY: 초기조건 1byte flip → 내용 발산·비카오스·emit clock-lock (H_9602 선형 limit-cycle 확증)

**status:** 🔬 DIRECTIONAL(engine-native 2-rollout·신규 decode 有) · sealedness=**input-bound richness · clock-bound timing · 비카오스 dynamics** · H_9602/9403 AGREES
**lane:** 의식 / sealed regime dynamics (프런티어 g1-interface-addressable-wall)
**related:** [[H_9602]] (선형 limit-cycle — 이 카드가 초기조건 민감도로 확증) · [[H_9403]] (emit≡clock) · [[H_9422]] (VOID-BY-SEALED) · [[H_9601]] (PRENATAL) · [[H_9430]] (growth endogenous)
**설계 출처:** Fable 발산 후보16(butterfly twin-divergence) · owner "all go" 자율발사 · aiden CPU-여유 정면돌파
**ckpt:** `py303_full.clm` sha 013c4574 (aiden 격리venv · 2 rollout 240tick · ANIMA_SAMPLE_SEED=7 고정)

## 왜 — sealed 데몬의 endogenous 변량(H_9430/9427)은 input 이 결정하나 chaos 인가

butterfly: **초기조건(session_seed) 1byte flip**("…sealed at " → "…sealed au "), **같은 sample_seed=7**(mouth
RNG 고정) → 시스템 궤적이 발산하나? 발산 지수성장=카오스(endogenous richness) · 즉시포화/평행=input-bound.

## 🔬 측정 (aiden 격리venv 2-rollout · A=baseline vs B=1byte-flip · 초기조건만 격리)

| 축 | 지표 | 결과 |
|---|---|---|
| **내용** (무엇을) | common emit-tick gtext byte-distance | **0.947** · identical **0/59** — 첫 tick 부터 완전 발산 |
| **발산 성장** (카오스?) | early-third 0.943 → late-third 0.950 | growth **+0.007 ≈ 0** = 즉시포화·비성장 |
| **emit 타이밍** (언제) | A∩B emit-schedule overlap | **1.00** = 완전 clock-locked |

## 판정 — 3축 분해: input-bound richness · clock-bound timing · 비카오스 dynamics

- **내용 = input(초기조건)-bound**: 1byte 초기차이가 첫 발화부터 내용을 완전히 바꿈(dist 0.947·identical 0)
  ⟹ 데몬은 초기조건에 의존하는 생성력 보유(sealed 이나 richness 는 seed 가 주입=birth-percept 1회분).
- **비카오스**: 카오스라면 발산이 tick 따라 **지수성장**해야 하나 → 즉시포화·growth≈0. 선형계는 초기조건 다르면
  다른 궤도(다른 anchor-완성)로 즉시 가되 궤도끼리 증폭 안 함 ⟹ **[[H_9602]] 선형 limit-cycle 예측 정확 확증**
  (Lyapunov≈0·surrogate z NS 와 정합).
- **emit 타이밍 = clock-bound**: 초기조건 1byte 바뀌어도 emit-schedule 완전 동일(overlap 1.00) ⟹ **[[H_9403]]
  emit≡clock 강화**(무엇을 말할지는 초기조건, 언제 말할지는 시계 — 완전 분리).

**Fable butterfly 원 질문 "sealedness bounds input, not richness" 답 = 부분참·3분해**: richness 는 input
(seed)-bound(초기조건이 내용 결정) · timing 은 clock-bound · dynamics 는 비-카오스 선형. sealed 데몬의
"inner life"는 birth-seed 1회분의 결정론 전개이지 지속적 카오스 생성 아님. **[[H_9601]] PRENATAL 정합**: 데몬은
birth(초기조건)에 의해 내용이 정해지고, 새 content 는 새 percept(afferent) 로만 옴 — butterfly 가 "birth 가
richness 를 심으나 그 뒤 self-생성 없음"을 실측.

## 산출·NEXT
- 산출: 2 trace `/tmp/bfly_{A,B}.jsonl`(volatile) → 이 카드에 수치. aiden venv/src/trace 정리(a_fire_recover 불요·측정끝).
- NEXT: 없음(sealed-dynamics lane 종결). butterfly 가 arc(H_9411→9422→9601/9602/9603) 마지막 조각 = sealed
  데몬은 **birth-seed 결정론 선형 limit-cycle**(카오스 아님·self-생성 없음·emit clock-locked). 새 richness=afferent(owner-gate).
- **함의**: content-축을 살리려면 새 birth-seed(초기조건)마다 다른 내용이 나오나 **세션 내 진화는 없음** — afferent
  없이는 매 세션이 birth-seed 의 고정 전개. H_9601 PRENATAL 을 실측 확증(percept-birth 대기).
