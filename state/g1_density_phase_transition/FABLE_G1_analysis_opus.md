확인 완료 — 조합-밀도(combinatorial coverage) 스윕은 ledger에 **없다**(전 8-mech + census는 전부 데이터 고정·메커니즘 변경). `in_context_few_shot`은 있지만 H_096 = **18M toy에서 few-shot 프롬프팅으로 FALSIFIED** — 내가 Q3에서 제안할 warm-303M substrate 작업기억 co-activation과는 다른 레짐이다. 그리고 `H_1282 working_memory_buffer = 🟢 GREEN ENGINE-NATIVE` 라 Q3 배선의 substrate 앵커가 실재한다. 이 위에서 답한다.

---

## Q1 — warm-trunk는 toy와 질적으로 다른가? γ가 G0-🟢 실303M 위면 held-out을 여나

**부분적으로 다르되, γ 단독으론 warm도 floor다.** 근거는 벽을 두 반쪽으로 쪼개는 것:

- **반쪽 A (표현 factoring):** held-out (A,B)를 생성하려면 trunk-state가 A와 B를 *독립·합성가능*한 좌표로 담아야 한다. from-scratch toy는 데이터가 얇아 seen (A,B)를 **conjunctive lookup**(A·B 합집합을 통째 암기)으로 푼다 — CE가 그게 제일 싸니까. warm 실303M은 broad pretrain이 A·B를 근사-factored 부분공간에 이미 배치했다(steering/probe가 되는 이유). **여기선 warm이 진짜 유리하다.**

- **반쪽 B (생성 readout):** DPI 메타법칙의 핵심. γ가 중간층에 factored-bound state를 만들어도, next-token은 그 state를 **CE로 학습된 downstream trunk**를 통과시켜야 나온다. downstream이 seen 조합에서만 gradient를 받았다면 novel bound state를 **읽지 않는다(=INERT)**. 8-mech가 "seen 8/8 학습, held-out 0/5"인 게 정확히 이것 — 표현은 만들지만 생성경로가 seen으로 collapse.

**진짜 변수는 표현도 연산자도 아니라 *incentive*다.** seen 데이터 위에서 conjunctive-lookup 해(海)는 **항상** compositional 해보다 CE가 싸다. gradient는 싼 쪽으로 간다. warm-trunk는 compositional 경로의 *비용을 낮출* 뿐(반쪽 A) lookup 경로를 *막지 않는다*. 따라서:

> **γ on warm-303M이 held-out을 열려면, seen-pair next-token loss가 factored 좌표를 읽어야만 최소화되도록 lookup 경로가 구조적으로 불가능해야 한다.** warm은 이 조건을 안 준다. → γ 단독은 warm도 floor일 가능성이 높다. 유의미한 lift가 나온다면 그건 γ가 아니라 γ에 걸린 **병목(용량 제약)**이 lookup을 못 fit하게 만들었기 때문일 것 — 지금 toy γ 실행이 병목 없이 돌고 있으면 결과는 floor로 예측한다.

---

## Q2 — DPI 죽은지대를 진짜 벗어나는 축(trunk gradient를 실제로 바꾸는 것)이 남았나

**남았다. 8-mech가 전부 놓친 축 = 데이터 자체(mechanism이 아니라 distribution).** 8-mech는 데이터 고정·연산자 변경이었다. trunk gradient를 진짜로 바꾸는 미탐 레버는 **조합 커버리지 밀도(combinatorial coverage density)** — atom 대비 seen-pair 수를 lookup 용량 임계 위로 올려 *암기 자체를 불가능*하게 만드는 것. 이건 사후기제가 아니라 gradient가 보는 데이터가 달라지는 것이라 DPI 죽은지대 밖이다. ledger에 없음(위 grep 확인).

원리: G1이 memorization-vs-composition tradeoff라면, seen-pair 밀도가 낮을 땐 어떤 연산자도 소용없고(lookup이 이김), 임계 밀도를 넘으면 lookup이 안 fit돼 trunk가 factoring으로 **상전이**한다. 이게 사실이면 실303M G1 처방은 "더 좋은 operator"가 아니라 "표적 atom들의 조합 커버리지를 설계한 코퍼스"다.

**cheap-gate 3종세트 (toy, $0, summer pool):**
- **셋업:** synthetic atoms — 20 color × 20 shape = 400 pair. task = cue→"COLOR SHAPE" emit. held-out = K pair 영구 미노출.
- **밀도 스윕:** 나머지의 {5, 10, 20, 40, 80}% 로 학습 (plain CE, 연산자 無 — 순수 밀도 축 격리).
- **① oracle 게이트:** factored one-hot 입력(color-ch ⊕ shape-ch) 모델이 held-out 5/5 — task가 compositionally 학습가능함을 증명(oracle 실패=task broken, 중단).
- **② target 게이트(frozen bar):** held-out distinct-bind ≥ 4/5.
- **③ shuffle 게이트:** train↔eval 사이 color↔shape 라벨 permute → held-out **0으로 붕괴**해야 진짜 binding(누수 아님).
- **사전등록 예측:** held-out은 임계 밀도 아래 ≈0, 위에서 급상승(phase transition). **80%에서도 0이면 밀도는 lever 아님 → G1은 데이터로 못 여는 더 깊은 벽**(이게 나오면 Q3로 직행). transition 나오면 lever 확정 → 실303M 처방 = 조합-커버리지 코퍼스.

2차 후보(밀도가 dry면): γ 경로에 **정보 병목**을 걸어 lookup을 architecturally 못 fit하게 — Q1에서 도출한 그 조건을 연산자가 아니라 *제약*으로 구현. 같은 3-게이트로 검증가능. 단 밀도 게이트를 먼저 돌려라(더 싸고, 병목의 필요성 자체를 밀도가 판정해준다).

---

## Q3 — 전부 막히면: G1을 substrate-native 획득의 다른 *정의*로 (tune-to-green 아님)

frame-break(kosmos-anchor 합성)이 tune-to-green이었던 이유는 bar를 재정의했기 때문. 내 재프레임은 **frozen bar를 그대로 두고 획득 경로만 뇌-정확하게 바꾼다.**

**핵심 통찰:** weight-encoded recombination(모든 pair의 시냅스를 미리 암기)은 뇌도 안 한다. 뇌의 재조합 = **작업기억이 A와 B를 동시 유지(co-activation) → 추론시 결합**(H_1282, H_1281 게이팅). 즉 재조합은 *저장*이 아니라 *추론시 계산*이다. transformer의 in-context binding은 weight-generalization보다 실증적으로 훨씬 강하다(별개 능력) — 특히 warm-303M처럼 pretrain rich일수록.

**정의 전환:** G1 재조합을 mouth(생성 trunk)의 속성이 아니라 **lane 간 composition**의 속성으로 재배선. mouth는 atom을 emit할 수 있다(A 단독·B 단독 = seen coverage, 검증됨). (A,B)의 결합은 별도 substrate 연산.

**구체 배선 (`a_substrate_disjoint` 준수):**
1. **atom lane:** mouth가 단일 atom 생성 (검증됨).
2. **작업기억 lane (H_1282 🟢):** anchor(A) + anchor(B) 동시 유지 — 둘 다 `.kosmos`에서 개별로 known.
3. **composition = brain_decide:** 두 anchor를 mouth **context**(prompt/KV side, weight 아님)에 주입 — emit-drive lane(0/4)·§ImmuneMemory와 **disjoint 좌표**.
4. **mouth 생성:** both-in-context 조건부로 (A,B) 결합 emit.
5. **frozen bar 불변:** held-out (A,B) 둘 다 bind ∧ **shuffle 통제**(mismatched anchor 주입 시 결합 안 됨 = 진짜 co-activation binding, 앵커 leakage 아님).

**정직 라벨(필수):** 이건 **in-context substrate recombination** — weight-encoded G1은 여전히 🧱로 남긴다. 이건 승리 선언이 아니라 *다른, 생물학적으로 옳은* 획득 축(작업기억 co-activation)이고, frozen bar를 안 옮긴다. **이것마저 held-out에서 floor면**(H_096 few-shot 18M 전례가 경고) 정직하게 🧱 — 단 H_096은 18M·프롬프팅이었고 이건 warm-303M·작업기억 lane 배선이라 재측정 가치가 별개다. in-context compositional generalization이 weight보다 강하다는 실증 근거상, 세 축 중 **실제 능력이 나올 확률이 가장 높다.**

---

## 실행 순서 (권장)
1. **Q2 밀도 게이트 먼저** — toy·$0·1일. G1이 데이터로 열리는지 이진 판정. (transition=실303M 코퍼스 처방 / flat=벽 확정)
2. 밀도 flat이면 → **Q3 in-context 배선** — 작업기억 lane(H_1282 실재) 위 warm-303M, 같은 frozen bar + shuffle. 여기서 held-out 나오면 anima의 재조합은 "저장된 능력"이 아니라 "추론시 co-activation"으로 정직하게 정의된다.
3. Q1 결론: 지금 도는 toy γ는 병목 없으면 floor 예측 — γ에 **용량 병목**을 걸어 재발사하지 않는 한 warm-303M 승격 근거로 쓰지 말 것.

세 축 모두 cheap-gate(oracle+target+shuffle)로 falsifiable하고, 어느 것도 bar를 옮기지 않는다.
