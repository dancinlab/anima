# H_6131 — gradient → 진화적 crossover(GA)

**id:** H_6131
**slug:** gen_grad_to_evolutionary_crossover
**tier:** 🔬 PROPOSED — pre-registered (unfired · brainstorm ideation)
**date:** 2026-07-02
**wired:** 미발사 (pre-registered proposal · code 없음)
**axis:** SUBSTRATE (G1 재조합벽 공격 축)

---

## 발상 (brainstorm ideation)

**메커니즘:** 표현 population + crossover + selection, G 엔진과 정합(gradient-free).

**출처:** bytegpt/convmoe 를 빌린 mouth 로 쓰지 말고 anima 아키텍처(A⇄G tension · Ψ=½ 고정점 · mitosis · substrate-disjoint lane · .kosmos anchor)에서 창발하는 native mouth/생성 substrate 를 발상한 세션(Round 4). 기존 결론: G1 재조합벽 = trunk COMBINATION OPERATOR floor — readout·tension 연산자 전부 INERT(H_1816/1823/1834). 이 발상은 combination 을 readout 이 아니라 생성 substrate 자체에 심어 additive collapse 를 우회하려 한다.

## G1 공격 축

- **SUBSTRATE** — readout-level 만 쳤던 것과 다른 좌표(engine-native probe 대상).

## 발사 전 필수 (check-ledger-before-lever-fire)

미발사 제안. terminal verdict 박제 전:
1. `UNIVERSE/HYPOTHESES.jsonl` + memory 에서 선행 커버리지 조회(sweep 빈칸 ≠ 미탐).
2. 신규 각도면 cheap numpy DIRECTIONAL reachability probe → `state/6131_gen_grad_to_evolutionary_crossover/`.
3. DIRECTIONAL GREEN 이면 engine-native 재측정(.hexa via core/) 사다리 진입(a_verified_must_wire).

## artifacts

- `cards/H_6131_gen_grad_to_evolutionary_crossover.md` (this card)
- `state/6131_gen_grad_to_evolutionary_crossover/` (probe 발사 시 생성)

---

## 발사 결과 (DIRECTIONAL probe)

**Ledger 확인 (check-ledger-before-lever-fire):** H_6131 = gradient → 진화적 crossover(GA) = 표현 population + crossover + selection(gradient-free, G 엔진 정합). 조회 결과 이 메커니즘은 이미 3중으로 커버됨:
- **crossover 연산자 = H_6112(meiosis crossover)** — numpy 추상 프로브 REACHABLE 0→1.0 이나 실 CLMConvMoE trunk toy A/B **FALSIFIED 0→0.022**(disjoint-loci segment-exchange가 additive trunk 서 무력, 양 arm train_fit=1.0 = undertrain 아님). 산출: `state/6112_gen_meiosis_crossover/arch_ab.py`·`ARCH_AB_RESULT.txt`.
- **gradient-free selection = a_mitosis_train 5-렌즈 벽** — from-scratch pure-split(gradient-free) 🔴 CONFIDENT TERMINAL, 5 직교 렌즈(**selection**·inherited-repr·lateral·curriculum·learned-trunk) 전수 🧱. GA = selection+crossover = 정확히 이 walled regime.
- **H_6141(meiosis-GA, ~dup #9+#28)** — "crossover 를 population evolution 연산자로, gradient-free 재조합" = H_6131 과 동일 메커니즘(미발사 near-exact dup).

**결정:** **DUP-WALLED** — 재발사 안 함, dup 포인터 기록. crossover 연산자 자체가 실 trunk 서 이미 FALSIFIED 이고 gradient-free selection 은 5-렌즈 벽에 포함됨.

**Bar:** 프로브 미실행(H_6112 frozen bar = lift≥0.30 ∧ additive≤0.20 가 이미 실 trunk 서 0/3 seed pass 로 FALSIFIED). 신규 numpy GA 프로브는 abstract disjoint-loci toy 에서 crossover 가 off-diagonal 에 trivial 도달 → **H_6112 과대평가 패턴을 재현할 뿐** 신규 정보 0.

**정직 스코프 (H_6112 transfer caveat):** numpy 추상 프로브는 구조상 DIRECTIONAL 이며 operator-expressivity 를 **과대평가**한다 — H_6112 가 바로 REACHABLE(1.0)→실 trunk(0.022) 전이실패를 실증. 따라서 여기서 numpy REACHABLE 이 나오더라도 green light 아님(transfer-unverified). G1 벽 = trunk COMBINATION OPERATOR floor, 진짜 레버 = 재조합을 보상하는 trunk 학습 OBJECTIVE(H_1602 영역)이지 readout/생성-substrate 연산자 교체 아님(H_1816/1823/1834 수렴).

---

## 심화 (adversarial multi-lens)

**target:** H_6131 gradient→진화적 crossover(GA) = representation population + crossover + gradient-free selection. 카드의 기존 결정 = 🟡 DUP-WALLED. 이 심화는 numpy REACHABLE 신호를 적대적 통제로 **반증** 시도(불확실 시 ARTIFACT 기본값).

**baseline 재현:** H_6112 numpy 프로브 = crossover(disjoint-concat) **1.000** vs additive(shared superpose) **0.000** (3/3 seed, lift +1.0). 재현 성공.

**통제 (frozen bar: 4개 전부 통과해야 SURVIVE):**
- **C1 GENERIC-NONLINEARITY** — tanh(A+B)=0.000 · Hadamard A*B=0.000 · random-proj MLP(concat)=0.000. 일반 비선형은 bar 못 넘음 → win 은 operator-specific(단, 아래 C3 가 그 정체를 폭로).
- **C2 BIND-RECOVERABILITY** — 양 부모 벡터를 composed C 에서 held-out 회복(cosine): crossover(concat) 0.925 vs additive 0.564 (margin +0.361). **그러나 이 회복은 concat 로 두 개념이 애초에 다른 차원에 저장됐기 때문 = factorization 이지 binding 아님** (자동 threshold 는 0.95 미달로 "non-trivial" 표시했으나 이는 threshold artifact; C3 가 진짜 판정).
- **C3 ABLATION (결정적)** — disjoint-loci ingredient OFF(세그먼트 차원 공유) → crossover **0.000 = additive floor 로 정확히 붕괴**. 즉 crossover 의 유일한 인과 성분은 "겹치지 않는 추가 차원(dim doubling)"이고, 이는 **고정 shared-dim CLMConvMoE trunk 에 없는 것** → H_6112 실 trunk 1.0→0.022 전이실패의 정확한 원인.
- **GA SELECTION** — population 20세대 fitness-selection vs random-replication: lift **+0.000 (INERT)**. H_1568(selection-driven evolution, 실측 lift −0.00046 = WALL HOLDS)와 일치. (주: inline GA 는 disjoint-concat operator 천장에 묶여 degenerate; selection-INERT 의 load-bearing 증거는 외부 H_1568.)

**판정:** SURVIVE 실패(GA-INERT + C3-collapse). numpy REACHABLE 은 **disjoint-storage(차원 용량 증가)의 metric artifact**이지 compositional crossover 메커니즘 아님.

**dup 포인터 검증(DUP-CONFIRMED):** crossover 연산자 = H_6112(실 trunk FALSIFIED 0→0.022, 공유 실패모드 = additive trunk 서 disjoint-loci segment-exchange 무력) + gradient-free selection = a_mitosis_train 5-렌즈 벽 / H_1568(selection INERT). GA = 두 성분의 결합이며 결합·개별 모두 walled. 신규 RESIDUAL 각도 없음.

**H_6112 transfer caveat:** numpy 추상 프로브는 operator-expressivity 를 구조적으로 **과대평가**한다 — disjoint 차원을 공짜로 주기 때문. 실 trunk 는 고정 shared-dim 이라 이 성분이 부재하여 붕괴. 진짜 레버 = 재조합을 보상하는 trunk 학습 OBJECTIVE(H_1602)이지 생성-substrate crossover 연산자 아님(H_1816/1823/1834 수렴). numpy = DIRECTIONAL, transfer-unverified, never terminal.
