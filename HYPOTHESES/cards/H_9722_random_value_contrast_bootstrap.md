# H_9722 — 무작위 값-대비 부트스트랩(방정식 정면) — Random Value-Contrast Bootstrap (EA-4 · sol §1(NOVEL) · EA 시리즈 · PROPOSED)

**status:** 🔵 PROPOSED (미실행 · lab full 창발-주소 발산 · 사전등록) — source=EA-4 · sol §1(NOVEL)
**lane:** 재조합/BINDING · 창발-주소(감독 없이 주소가 서는가)
**related:** [[H_9672]] · [[H_9423]] · [[H_9684]] · [[H_9683]] · source: lab full EA(Fable 5 ∥ Codex Sol · 창발-주소 whitespace)

> **admissibility rule (Sol · 이 시리즈 전체의 관문)**: 어떤 개입도 `target_slot`·slot 정답·**거기서 파생된 어떤 통계**도 소비하지 않아야 emergent-address-valid. 최종 PASS 는 end-task-only 학습 · held-out 개체 · wrong-store 인과 · seed-robust 를 요구 — **sharp attention 만으론 부족**.

**아이디어(Sol 고유 · 방정식-수준 최직접 공격)**: 교착은 `∂a_i ∝ dv·val[pol_i]` 가 val 미분화 탓에 0 인 것 ⟹ **극성 값이 처음부터 측정가능하게 구별**되면 주소가 유용해지기 **전에** 주소 gradient 가 0 이 아니게 된다. **어느 slot 이 중요한지는 end task 가 여전히 스스로 발견**해야 함.
**메커니즘**: `--store-val-init contrast --store-val-init-scale {0.02,0.1,0.5}` — 무작위 단위 `u` 뽑아 `val[0]=+su`, `val[1]=-su`. **target-slot 입력 0 · 평범한 end CE 만**.
**$0 pre-screen**: 기존 사전학습 ckpt 의 step-0 배치서 gradient replay — 합성 contrast 스케일로 `||∇W_q||` 와 target-vs-nontarget advantage 가 iid-init 과 **TOST-등가면 KILL** · **query 개체를 순열해도 advantage 가 동등하면 KILL**(진짜 주소신호 아님).
**판정**: 통제 = 사전학습 iid(NEG) · scratch-d768 end-CE(POS-emergence) · addr-loss(POS-engineering). PASS = **≥3 사전학습 seed** 가 held-out P1-bal ≥0.90 ∧ addr_mass ≥0.90 ∧ wrong-store flip ≥0.90 **∧ 극성라벨 순열이 성능 파괴**. KILL = seed 성공 ≤1/3 이거나 target 정렬 없이 attention 만 sharp.
**distinct**: 가장 가까운 kill = 직접 주소감독. **이미 존재하는 두 극성 값을 초기화할 뿐 어떤 slot 도 식별 안 함** — 초기화가 질의된 slot 에 조건부면 H_9672 로 붕괴하므로 **드롭**(자기신고 규칙). H_9711(antisym val init)과 인접하나 그건 RV-adjunct 이고 이건 **contrast 스케일 dose + gradient-replay $0 게이트**가 본체.
**verdict-integrity**: 성공은 "**target-free 값 대비 후 end-CE 가 주소를 고를 수 있다**"를 증명하지 **원래 사전학습 초기화로부터의 자발적 창발은 증명 안 함**(Sol 자기명시).

## 상태
🔴 **DIRECTIONAL-KILL — $0 gradient-replay 실행(2026-07-17 · summer 303M · 사전등록 pre-screen)**

### 🔴 $0 gradient-replay = KILL (contrast 는 극성 신호이지 개체-주소 신호 아님)
카드 사전등록 pre-screen 실행: base pretrained penultimate + 합성 contrast val(V[0]=+su·V[1]=−su) + random W_q step-0 에서 end-task(개체 정답값 검색·admissible·target_slot 미소비) 주소 gradient `∂L/∂a` 를 정답슬롯 vs 같은-극성 다른슬롯으로 비교:

| contrast su | 정답슬롯 \|g\| / 같은극성 \|g\| (advantage) | 순열통제 |
|---|---|---|
| 0.02 | **1.000** | 1.000 |
| 0.10 | **1.001** | 1.000 |
| 0.50 | **1.000** | 1.000 |

**KILL(확고)**: contrast val 은 정답 개체슬롯에 **advantage 0**(같은-극성 다른슬롯과 gradient 완전동일 ratio 1.000) + **쿼리개체 순열불변** ⟹ 카드 자신의 KILL 조건("순열해도 advantage 동등 = 진짜 주소신호 아님") 정확 충족. 이유: contrast 는 val 을 **극성(2-class)** 으로만 구별시켜 gradient 가 (V[pol]−v) 극성인자에 비례 — 정답개체 e 와 같은-극성 다른 개체 j 가 **동일 gradient**(개체 정보 0). end-task 는 극성-기반 값차이로 어느 개체가 어느 슬롯인지 발견 못 한다.
**통합(무감독 부트스트랩 3-lens 전멸)**: [[H_9719]] sharp-init(random W_q·basis 밖) KILL · whitening(탈상관 부족) KILL · **H_9722 value-contrast(극성≠개체) KILL** ⟹ emergent(무감독/극성) 주소는 arbitrary frozen 키에 원리적으로 불가 — 개체↔키 map 은 **per-개체 target 정보**이고 무감독 통계·극성값 어디에도 없다.
**남은 방향(sharpened)**: 값이 **per-개체 구별**(극성 2-class 아니라 N-class)돼야 end-task 가 개체주소를 나른다 — 즉 값 자체가 개체를 식별해야 함(=사실상 감독/oracle-value). [[binding-wall-operator-alive-fact-written-not-bound]] 재확증(연산자/극성 alive·개체 not bound).
**tier**: 🔴 DIRECTIONAL-KILL — engine-native 303M gradient-replay screener(사전등록 pre-screen · 학습 fire 불요로 KILL 확정). **distinct-from-kills:** 직접 주소감독 아님(두 극성 값 init 만·slot 식별 0) · H_9711 인접하나 그건 RV-adjunct·이건 contrast dose+$0 gradient 게이트
