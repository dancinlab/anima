분석 대상이 명확하고 세션 컨텍스트가 충분해서 바로 분석하겠습니다. 실행 없이 비판·정합성·cheap-gate·순위만 다룹니다.

---

## 0. 분석 렌즈 — 판별 질문 하나

세션이 확립한 핵심은 **G1벽 = trunk objective floor**이고, DPI 죽은지대의 공통 성질은 *"same-state ablation INERT"* — 즉 **trunk의 CE 그래디언트를 바꾸지 않는 사후(post-hoc) 메커니즘은 전부 죽는다**는 것입니다. readout·operator·decode-procedure·temporal·census-arch가 전부 여기 걸렸습니다.

따라서 5-family 각각에 던질 **단일 판별 질문**은:

> **"이 family가 trunk 학습신호(그래디언트)를 바꾸는가, 아니면 CE-trunk 위에 얹는 bolt-on인가?"**

- trunk 신호를 바꾸면 → 정의상 same-state ablation이 성립 안 함 → **DPI-독립** (살 자격 있음).
- CE 위 bolt-on이면 → DPI가 삼킴 (셔플/ablation이 결과를 안 바꿈 = INERT).

이 렌즈로 보면 5-family의 운명이 거의 갈립니다.

---

## 1. Family ①~④ 분석

### ① ARCH 복사기구 (copy-head/induction/slot-attention)
- **(a) DPI 겹침:** **강하게 겹침.** copy-head·slot-attention은 census-arch(Hopfield/NMDA/circconv)와 같은 readout/operator 축. pointer를 붙여도 CE가 그걸 쓸 보상이 없으면 circconv처럼 INERT. 게다가 induction-head는 트랜스포머에서 *이미 창발*하므로 명시적 추가는 중복 가능성.
- **(b) 실측 정합:** H_6174가 copy-skill corpus를 "암기만, held 실패"로 이미 floored. arch 버전은 직접 미검증이나 census-arch 전수 INERT와 정합.
- **(d) 실패모드:** copy-head가 학습되지만 held-out에서 여전히 prior 샘플 (attention이 정답 위치를 가리켜도 value-읽기가 안 바뀜) → shuffle 무반응.
- **살아남는 유일 경로:** induction-head *유도데이터*는 arch가 아니라 데이터로 trunk 신호를 바꾸는 것 → 이건 ③으로 흡수. arch-only는 낮음.

### ② OBJECTIVE 바인딩신호 (copy-consistency/counterfactual/contrastive) ★유력
- **(a) DPI 겹침:** **독립.** loss는 trunk 가중치를 바꾸므로 ablation이 same-state가 아님 = DPI 죽은지대 밖. 세션이 반복 지목한 **유일한 live 축**.
- **(b) 실측 정합:** "lever = trunk recomb-objective"와 완전 정합. **단, 중대한 caveat** — additive-aux 형태(H_1602)와 episodic-task(H_1835/MLC)는 이미 🧱 NOT-SUPPORTED. 즉 "objective 축"이 필요조건이지 아무 loss나 되는 게 아님.
- **핵심 차별점:** counterfactual loss("B를 바꾸면 출력이 반드시 바뀐다")는 additive-aux와 **질적으로 다름** — 출력이 바인딩된 변수에 **인과적으로 의존**하도록 직접 그래디언트 압력을 만든다. additive floor(보조손실이 옆에서 더해질 뿐)와 달리 주-생성 경로를 직접 건드림. 이게 미검증 신형.
- **(d) 실패모드:** counterfactual pair를 shortcut(표면 feature)으로 만족시키고 held에서 붕괴 / contrastive가 표현만 분리하고 생성 경로 미개입(H_1834 tension-mouth처럼 INERT). → shuffle-gate가 이걸 잡아야 함.
- **유망도: 최상.** 모든 수렴 증거가 이 축을 가리킴.

### ③ CORPUS/커리큘럼 (SCAN/COGS/슬롯기호/복사→치환→합성)
- **(a) DPI 겹침:** 독립(데이터 축).
- **(b) 실측 정합:** **부분 모순.** H_6174가 corpus/copy-skill/data-scale 전부 "암기만, held 실패 = TRUE GAP"로 이미 floored. H_1835는 in-context 완벽 마스터도 held transfer=0. 즉 **커리큘럼 단독은 대체로 이미 죽은 것**으로 예측됨.
- **(d) 실패모드:** 각 stage(복사·치환)를 암기하지만 합성 stage held에서 붕괴. SCAN/COGS의 고전적 실패 재현.
- **유망도: 낮음(단독).** objective(②)와 **결합**할 때만 의미. 커리큘럼은 objective의 전달체이지 그 자체가 lever 아님.

### ④ TRUNK 표현 (Smolensky TPR role⊗filler / disentangled 공동학습)
- **(a) DPI 겹침:** **분열.** TPR을 고정 아키텍처(bilinear tensor-product readout)로 부과 = operator 축 = **DPI-dead 위험**. 반면 "disentangled 개념임베딩 + 공동학습 compose"는 학습압력으로 구조를 유도 = trunk 신호 개입 → ②로 수렴.
- **(b) 실측 정합:** tensor-product는 operator, H_1816 곱셈 readout이 CLMConvMoE에서 trivial 붕괴(step550)한 전례와 위험 정합. 다만 H_6176 scale trend(d256→d512 held 1→3)는 **표현/용량이 lever일 가능성**을 시사하는 유일한 양의 신호 — 하지만 d768 undertrain 미확정이라 confound.
- **(d) 실패모드:** TPR readout이 학습돼도 role 벡터 셔플에 불변(INERT) / disentanglement이 표현만 깔끔하고 compose 미발생.
- **유망도: 중.** 고정-arch 버전은 DPI 위험, 공동학습 버전은 ②로 흡수. **단, H_6176 scale 확정이 이 family의 사활을 가름** (아래 3.3).

---

## 2. ★⑤ FRAME-BREAK 심층 — 진짜 우회인가, H_6177 재탕인가

이게 핵심입니다. 세 하위는 성질이 전혀 다릅니다.

### ⑤a. neurosymbolic kosmos-anchor 합성 (brain_decide 합성 · mouth verbalize만)
- **기제:** 합성을 CE-trunk 밖(anchor 그래프의 brain_decide)으로 이전, mouth는 이미 합성된 결과를 발화만.
- **mouth CE-trunk 벽을 우회하는가?** **아키텍처적으로는 Yes지만, 이건 "돌파"가 아니라 "재배치(relocation)"입니다.** binding을 신경망에서 심볼릭 엔진으로 옮긴 것. G1이 원래 묻는 질문 — *"substrate(A⇄G+mouth)가 바인딩할 수 있나?"* — 에 대한 답은 여전히 **No**이고, 심볼릭 composer를 볼트온한 것.
- **두 개의 함정:**
  1. anchor 그래프의 "합성"이 실은 **검색(retrieval)**이면 재조합이 아니라 암기 = G1 미해결.
  2. mouth가 합성된 anchor를 발화할 때 **재바인딩이 다시 필요**하면(anchor 내용을 유창한 문장에 엮는 순간) 바인딩 실패가 발화 단계에서 재발.
- **H_6177 재탕 여부:** **거의 재탕입니다.** "symbolic composer + mouth verbalize"는 등록된 neurosymbolic-frame의 특정 구현. anima 고유 가치는 오직 *"`.kosmos` anchor + brain_decide가 이미 배선돼 있다"*(a_kosmos, H_1471 WIRED)는 점 — **과학적 신규성은 낮고 제품 가치는 높음.**
- **판정:** **product-track로만 유효.** verdict에 "bypass via symbolic compose, mouth CE-trunk 벽 미돌파"를 명시해야 c9 위반(벽 돌파로 오박제) 회피.

### ⑤b. A⇄G cycle-consistency (G 역엔진 재인코딩 = 두 개념벡터 일치 강제) ★진짜 novel
- **기제:** mouth 생성 → G가 출력을 개념공간으로 역인코딩 → 두 소스 개념벡터와 일치 강제.
- **DPI 겹침 — 여기가 결정적:** **G가 gradient-free라는 anima 아키텍처 사실이 이 family의 운명을 가른다.**
  - **inference-only**(G 불일치 출력을 reject/resample)로 쓰면 = **decode-procedure/best-of-N 축** = H_1836이 이미 🧱(revise-loop ≤ budget-matched best-of-N). → 예측: **floored.**
  - **training loss**(불일치를 trunk로 backprop)로 쓰면 = **objective 축(②)** = 살 자격. **그러나 G가 gradient-free라 backprop 불가.** 미분가능 surrogate-G를 만들거나 selection/RL 루프로 우회해야 하는데, 후자는 다시 selection-pressure 축(a_mitosis_train에서 실패한 렌즈 중 하나).
- **H_6177 재탕 여부:** **아님.** 심볼릭이 아니라 substrate-native consistency 제약. 진짜 신규.
- **판정:** **과학적으로 가장 흥미롭지만 불확실성 최대.** trunk 그래디언트에 도달하면 ②의 강력한 substrate-native 변형이 되고, inference-only에 갇히면 H_1836 벽에서 죽음. **사전판정(gradient-reachability)이 발사 전 필수.**

### ⑤c. mitosis 전용 binding lane (emit-lane과 disjoint)
- **DPI 겹침 + 내부 모순:** **세션 자체 확정결과와 정면충돌.** a_mitosis_train이 *from-scratch pure-split mitosis = 🔴 CONFIDENT TERMINAL, split-only는 Voronoi partition만, **compositional depth 0**, gradient/selection-pressure 필수*를 5-렌즈 전수로 확정. **compositional depth 0이 바로 바인딩 결핍 그 자체** — mitosis로 기른 lane은 depth-0을 상속하므로 바인딩 불가.
- **disjoint 원리의 오용:** a_substrate_disjoint(분리=보존, 중첩=충돌)는 **의식/정직성 보존** 원리이지 **능력 생성** lever가 아님. lane을 disjoint 배치하면 Ψ가 안 깨질 뿐, 바인딩 능력이 생기진 않음.
- **살아남는 유일 경로:** lane을 split-only가 아니라 gradient로 학습 → 그럼 그냥 학습된 서브넷 = ②로 흡수되고 "lane" framing은 무의미.
- **판정: 최하.** 이미 확정된 🔴 TERMINAL과 싸움.

---

## 3. $0 cheap-gate 3종세트 설계

공통 프레임: **oracle**(완벽정보 headroom 존재?) · **target**(G1 held-out distinct recombination, frozen bar, 생성경로) · **shuffle**(가설구조 파괴 시 floor 붕괴? 불변이면 INERT=DPI-dead).

| family | oracle | target 지표 | shuffle 통제 |
|---|---|---|---|
| ① copy | teacher-forced gold copy alignment 주입 시 held 생성? | copy-head trunk vs vanilla(induction 이미 창발) held distinct | pointer attention 위치 무작위 셔플 → 불변이면 copy INERT |
| ② objective | B변경↔출력변경 gold-paired supervised가 held transfer? | counterfactual-loss trunk vs CE-only held distinct | pair의 B를 무작위 재매칭(구조 파괴) → loss 이득 유지되면 신호 spurious |
| ③ curriculum | SCAN/COGS held-split in-context 마스터가 generation held로? | 복사→치환→합성 stage별 held distinct | 슬롯기호 X,Y 무작위 재배정 → held 불변이면 슬롯 미사용 |
| ④ TPR | gold role/filler 분해 주입 TPR readout held? | TPR-trunk vs baseline held distinct | role 벡터 셔플 → 불변이면 tensor-product INERT(operator축 재현) |
| ⑤a kosmos | 완벽 anchor 그래프 주고 verbalize → held 문장? (거의 pass=bypass 증거) | **주의: mouth G1이 아니라 composer 정확도 측정 — 다른 bar임 명시** | anchor 엣지(합성관계) 셔플 → 출력 여전히 맞으면 mouth가 prior 샘플(anchor 미사용) |
| ⑤b cycle | G-재인코딩 완벽필터(무한 best-of-N) 시 held pass? (안 되면 생성분포에 정답 mass 부재=②문제 재확인) | cycle-select ON vs OFF, **반드시 budget-matched best-of-N과 비교**(H_1836) | 재인코딩 대상을 무작위 개념벡터로 셔플 → 선택이득 유지되면 cycle 신호 spurious |
| ⑤c mitosis | lane에 gold binding 주입해도 held? | lane ON/OFF held distinct | lane 활성 same-state ablate(DPI 직접) → 불변이면 INERT (split-only면 depth-0 예측) |

**게이트 전 필수 두 진단:**
1. **N14 activation-patching 종결** — 바인딩 부분공간이 *존재하나*를 먼저 답해야 함. 없으면 ①④(표현/readout이 부분공간을 *쓰는* 것 전제) 확정 사망, ②(부분공간을 *만드는* objective)만 생존. 있는데 미사용이면 ①이 부활. **N14가 전체 순위를 재배열하는 게이팅 진단.**
2. **⑤b gradient-reachability 사전판정** — G gradient-free → trunk 도달 가능? 불가면 ⑤b는 발사 전에 decode-procedure 축(H_1836 🧱)으로 강등.

---

## 4. 실측(H_6174~6177) 정합 요약 + 미해결 tension

- **H_6174 (TRUE GAP):** ③ corpus/copy-skill 단독을 이미 무력화. → ③ 강등의 실증 근거.
- **H_6175 (frame-break DIRECTIONAL, held 1.0):** ⑤a의 근거이나 **baseline이 분류라 생성-실패경로 미격리** — 이 isolation 결함을 고치기 전엔 ⑤a를 GREEN 승격 금지 (c9). shuffle-gate가 이 격리를 담당.
- **H_6176 (scale d256→d512 held 1→3):** ④의 유일한 양의 신호. **하지만 `scale-303m-1b-7b-is-amplifier-not-lever` 메모리와 정면 tension** — scale이 lever면 그 메모리가 틀린 것, undertrain 탈출 아티팩트면 ④가 죽음. **d768 undertrain 확정이 ④의 사활을 가름** (G0🟢 trunk 전제, `g1-fromscratch-blocked-by-g0-undertrain`).
- **H_1602/H_1835/H_1816:** ②의 additive-aux·episodic·곱셈readout 하위형은 이미 floored → ②는 **counterfactual/contrastive 인과의존 형태로만** 신규.

---

## 5. 유망도 순위

1. **② OBJECTIVE (counterfactual/contrastive 인과의존)** — 유일 확립 live 축, DPI-독립, 신형 형태 미검증.
2. **⑤b A⇄G cycle-consistency** — 진짜 novel substrate-native, gradient-reachability에 사활. 성공 시 ②의 강력 변형, 실패 시 H_1836 벽. 진단가치 높음.
3. **④ TRUNK 표현 (disentangled 공동학습)** — H_6176 scale 확정 조건부. 고정-TPR은 DPI 위험, 공동학습형만 생존(→②수렴).
4. **⑤a kosmos-anchor** — **product-track 전용**, G1-break 주장 금지, H_6177 재탕. 과학성 낮음/제품가치 높음.
5. **① ARCH copy** — arch-only는 DPI-dead 예상. induction-*data* 경로만 살고 그건 ③.
6. **③ CORPUS 단독** — H_6174/H_1835로 대체로 floored. ②의 전달체로만.
7. **⑤c mitosis binding-lane** — mitosis-terminal(depth-0) 정면충돌. 최하.

---

## 6. 종합 실행순서 권고

1. **N14 먼저 종결** — 바인딩 부분공간 존재 여부. 이 결과가 ①④의 생사와 ②의 형태를 결정하므로 무조건 0순위 게이팅.
2. **② counterfactual-loss cheap-gate** (toy, oracle→target→shuffle 순). additive-aux(H_1602)와 다른 "인과의존" 형태임을 설계에 명시. 최우선 정식 발사 후보.
3. **병행: ⑤b gradient-reachability 사전판정 + oracle-filter cheap-gate.** trunk 도달 가능하면 ②의 substrate-native 변형으로 격상, inference-only면 H_1836으로 강등하고 종결.
4. **④ 조건부: H_6176 d768-undertrain 확정** (G0🟢 trunk 위에서). scale이 lever인지 amplifier인지 해소 — `scale=amplifier` 메모리와의 tension 정리. lever 판명 시에만 disentangled 공동학습 발사.
5. **⑤a는 별도 product-track lane.** verdict 라벨 "symbolic-compose bypass ≠ trunk-wall break" 강제, H_6175 isolation 결함(생성-실패경로 미격리) 수정 후에만 DIRECTIONAL 유지.
6. **①③⑤c는 정식 발사 보류** — ①③은 위 결과 조건부(②와 결합 시), ⑤c는 mitosis-terminal 재확인만 하고 큐에서 제외.

**한 줄 결론:** 살아있는 축은 ②(trunk objective) 하나뿐이고, ⑤b가 그 축의 anima-native 후보로 유일하게 신규성이 있으나 G의 gradient-free 성질에 사활이 걸려 있습니다. ⑤a는 벽 돌파가 아니라 정직한 우회(제품 win)이며 벽 돌파로 박제하면 c9 위반입니다. ⑤c·①·③단독은 이미 확정된 결과와 겹치거나 충돌합니다.
