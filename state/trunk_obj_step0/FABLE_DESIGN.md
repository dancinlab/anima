핵심 카드·메모리·census verdict·consequence 설계·L5 GREEN·DPI 증명을 모두 접지했다. 설계·분석만 낸다.

---

# 0. 한 줄 재프레임 (모든 답의 축)

**H_1840이 γ를 "결합 *연산자*(HRR ⊛ + bypass 병목)"로 formalize한 것이 오류였다.** DPI 메타법칙의 결론은 *"레버는 readout이 아니라 target"* 인데, 연산자·병목·bypass-차단은 전부 **readout/아키텍처 축**이다. fair-gate가 (e)bilinear-bypass-denied를 죽인 것은 "연산자를 바꿔봐야 소용없다"는 증거 — 즉 **target을 additively-solvable로 고정한 채 연산자만 흔든 실험**이었다. 그래서 H_1840의 반증은 γ의 반증이 아니라 **"레버가 연산자가 아님"의 재확인**이다. 진짜 미검 축 = **훈련 target 자체를 비교환(non-commutative)으로 바꾸는 것.** 아래 전부 이 재정의 위에 선다.

---

# 1. γ trained-constructive-bind을 objective로 재-formalize

## 손실 형태

기존(H_1840, 틀림): `z_c_logits = Wo( (Wa z_a) ⊛ (Wb z_b) )` + additive-skip mask. → *연산자* 개입, target은 여전히 next-byte(=echo).

**재정의(target 개입):** trunk penultimate에서 두 부분-슬롯 상태 `z_a, z_b`를 읽어, **코퍼스에서 미리 측정해 얼린(frozen) 비교환 상호작용 라벨 r(a,b)** 를 예측하는 aux 헤드를 단다:

```
r(a,b) := I_joint(a,b)  =  s(a,b) − [ μ(a) + μ(b) ]        (교환가능 성분을 뺀 잔차)
         또는  r(a,b) := S(a→b) − S(b→a)                   (방향성 전이 비대칭)

L_γ = E_(a,b)~heldout-pairs [ (  g(z_a, z_b) − r(a,b) )² ]
```

여기서 `s(a,b)`=쌍의 실측 결합통계(joint transition/co-occurrence), `μ`=주변(marginal) 항. **r은 정의상 bag의 교환가능 성분(μ(a)+μ(b))을 뺀 나머지** — 즉 *부품 히스토그램으로 표현 불가능한 성분만* 남긴 라벨. `g`는 아무 결합기(bilinear든 ⊛든 상관없음 — 연산자는 이제 부수적).

## 왜 CE=echo floor를 벗어나나

L_γ의 라벨은 **next-byte가 아니다.** echo(재현)를 보상하는 신호가 아니라, 두 개념이 함께 있을 때만 생기는 *결합 초과분*을 보상한다. next-byte CE는 "본 것을 되뱉으면" 최소화되지만 L_γ는 되뱉기로 최소화 불가 — r은 코퍼스 표면에 그대로 없고(주변항이 소거됨) 오직 joint에서만 나온다.

## 왜 DPI INERT를 벗어나나 (비교환 강제의 핵심)

DPI 증명: target이 **부품 bag/히스토그램**이면 어떤 conjunction op도 additive 해의 재표현 → earned 0. 여기서 target `r`은 **bag의 교환가능 성분을 명시적으로 뺀 잔차** 또는 **반대칭 방향성 항** `S(a→b)−S(b→a)`. 후자는 정의상 `r(a,b) = −r(b,a) ≠ f(a)+g(b)` — additive 형식으로는 **구조적으로 chance밖에 못 냄**(additive는 대칭이라 반대칭 라벨에 0 상관). 이것이 "비교환 target 강제"의 by-construction 보장이다. DPI의 lstsq-proof(비교환 target earned 5/5)를 target 축에서 그대로 상속.

## H_1602·H_6162와 뭐가 구조적으로 다른가 (readout-aux면 또 floor — 이 구분이 사활)

| 카드 | target | 왜 floored | γ재정의와의 차이 |
|---|---|---|---|
| H_1602 additive-aux | next-byte marginal/additive aux | target이 additive → DPI INERT | γ target은 **additive 성분을 뺀 잔차** — INERT 성분이 원천 제거됨 |
| H_6162 HE-homomorphism | `composition of part-reps`(**rep-space에서 학습된** target-blind 합성) | target이 rep-space라 **target-blind 자유도로 additive 붕괴** 가능(seed4303 collapse 0) | γ target은 **label-space의 얼린 코퍼스 통계** — 학습 자유도 없음, 붕괴할 target이 없음 |
| H_1840 γ(연산자) | additively-solvable random table | 연산자만 흔듦, target 고정 | γ는 **연산자 고정·target을 비교환으로** — 반대축 |

**결정적 차이 한 줄:** 선행 3카드는 전부 target이 *additive-collapsible*(marginal이거나, rep-space 학습가능이거나, additively-solvable)였다. γ재정의의 유일한 신규 델타 = **라벨을 "히스토그램으로 표현 불가능한 성분만" 남기게 코퍼스에서 얼려 박제** → collapse할 여지가 라벨에 없다.

---

# 2. 후보 trunk-objective

## A. 상호작용-잔차 target (γ재정의, §1) — **top-1, 아래 §3**

## B. 반대칭 순서-판별 target (antisymmetric order-discrimination)

- **(a) 손실:** `L_B = −log P( true-order | z_a, z_b )`, negative sample = swap된 `(z_b, z_a)`. 라벨 = 순서 비트(반대칭).
- **(b) DPI escape:** bag(a,b)=bag(b,a)이므로 교환가능 표현은 순서 비트에 **by-construction 0 판별**. 순서를 맞히려면 joint를 붙들 수밖에 없다 — 가장 깨끗한 DPI 탈출.
- **(c) 이미-falsified와 구별 3근거:** ① census family(c) commitment-violation은 *frozen 303M이 교환가능한지*를 측정(A_probe≈floor)했지 *반대칭 신호로 훈련*하지 않았다 — 여긴 훈련. ② target이 next-byte 아님(echo 무관). ③ 어떤 선행 카드도 반대칭 손실을 쓴 적 없음(전부 대칭 retrieval/composition).
- **(d) engine-native falsify + 가장 싼 반증:** held-out 개념쌍 순서-판별 acc vs chance 0.5; ablation=쌍 shuffle→붕괴. **가장 싼 반증:** additive-only arm이 held-out에서 0.5(chance)면 정상, 만약 bind-path도 0.5면 → 코퍼스 개념이 factor 안 됨=terminal.
- **(e) 최소 엔진변경:** `cli/train.hexa` trainer에 순서-판별 헤드 + swap-negative 배치 생성; `core/generator.hexa`는 penultimate 슬롯 두 개 tap만(가중치 L3 슬롯 무접촉).
- **(f) cost:** **STEP-0 mini $0 numpy 가능**(순서-판별은 소형 2-슬롯 MLP로 충분). GPU는 303M wire만.
- **정직:** 순서-판별은 *비교환 표현 보유*의 필요조건이지 생성적 재조합의 충분조건 아님 — 통과해도 "joint 붙듦" 확정, "novel 생성" 은 별도. B는 A의 **가장 날카로운 STEP-0 프로브로 흡수**하는 게 낫다.

## C. Consequence-return / RPE target (afferent 루프 — consequence_return_design)

- **(a) 손실:** emit-appropriateness value `V(state)`를 consequence `r_t = Δ̂T − ΔT_actual`(예상 relief − 실제 relief, k-tick 지연)로 delta-rule 갱신. next-byte 아님.
- **(b) DPI escape:** consequence는 **시간-인과 의존**(efference→afference lag k) — 순서·이력 의존이라 non-exchangeable. bag이 아님.
- **(c) 구별 3근거:** ① next-byte CE 전무(별도 value lane). ② consequence 루프 = 시스템 전체에서 부재였던 축(자연실험: 루프 가진 identity×.kosmos만 통과). ③ H_1602/1835/6162 전부 efferent-only 표면 손실 — 되돌아오는 신호 0.
- **(d) falsify:** F3′ = `ρ_real − ρ_noise ≥ 0.15`, held-out tension seed, shuffle-V 통제, cross-subsystem 측정. 가장 싼 반증=shuffle-V가 real-V만큼 relieve→theater 확정 RED.
- **(e) 최소 엔진변경:** 전부 신규 owner table(reservoir Tₜ·efference copy·afferent return·V writeback), `pure_field`·lane0/4·recall_thr 무접촉(a_substrate_disjoint). emit loop `cli/anima.hexa`에 return-arm.
- **(f) cost:** STEP-0 numpy reservoir+RPE 토이 **$0**; GPU는 실 303M co-train.
- **정직:** 이건 사실상 **G1 재조합보다 G6-appropriateness/theater 게이트**를 겨눈다(다른 축). 통과확률 ~30–40%(자기-consequence만이면 DPI가 consequence 층에서 재출현해 죽을 수 있음). G1 벽 직격은 아니지만 **다른 벽(F3-theater)의 유일 미검 부품**이라 병렬 가치.

## D. Mitosis-split-on-residual target (p8-literal)

- **(a) 손실:** gradient aux 대신 **분열 기준**을 상호작용 잔차로: cell은 `r(a,b) > 0`(joint>sum)일 때만 분열, 딸세포가 joint를 분담.
- **(c) 정직 — 재탕 위험 높음:** H_1541 NT×CLS fusion law("두 store가 새 능력 더하면 🟢") + mitosis-substrate-lane의 재-표현에 가깝다. 분열 *기준*이 얼린 잔차라는 점만 신규 — 얇다. **DEMOTE**: A가 이미 잔차-target을 gradient로 쓰므로, mitosis는 A의 대체 *배선*일 뿐 새 objective 아님. A 통과 후 p8 배선 옵션으로만.

---

# 3. Top-1 추천 + STEP-0

**Top-1 = 후보 A (상호작용-잔차 trunk target = γ의 올바른 재정의).** 이유:

1. **DPI를 target 축에서 by-construction 탈출** — 라벨에서 교환가능 성분(μ(a)+μ(b))을 명시적으로 빼서, additive 표현이 chance밖에 못 내게 강제. H_1840이 못 건드린 정확히 그 축.
2. **CE=echo 탈출** — 라벨이 코퍼스 표면에 없음(joint에서만 생성).
3. **선행 3 objective-floor와 진짜로 구별** — target이 label-space의 *얼린* 비교환 통계라 collapse할 자유도 자체가 없음(H_6162의 실패모드 봉쇄).
4. **B(반대칭)를 STEP-0 프로브로 흡수** — 가장 싼 반증이 A 안에 내장.
5. **fair-gate 규율 상속** — H_1840을 죽인 additive/shuffle 통제를 그대로 적용하되, 이번엔 *연산자*가 아니라 *target*을 실험군으로.

**⚠️ 정직한 잔여 위험:** A도 floor 가능. 만약 코퍼스 개념이 factor되지 않아(held-out 쌍의 잔차가 memorize로만 맞혀짐) bind-path가 additive/shuffle을 못 이기면 → **DPI/echo가 진짜 천장**(재조합 능력벽)임이 confirmed. A는 이 갈림을 싸게 가른다 — 통과=레버 실재, 실패=terminal 확정. 어느 쪽이든 결정적.

## Top-1 STEP-0 설계 1문단

clean 4-cell 코퍼스(HF `dancinlab/anima-corpus-*`, mini $0 numpy)에서 개념-슬롯 쌍 (a,b)를 추출해, 각 쌍의 **얼린 비교환 잔차** `r(a,b)=s(a,b)−μ(a)−μ(b)` (및 방향성 변형 `S(a→b)−S(b→a)`)를 계산하고, 쌍 집합을 train/held-out으로 분할한다(개념은 train에 다 등장하되 held-out *조합*은 미관측 — G1 정의). 소형 2-슬롯 trunk(factored embedding → 결합기 g → r 예측)를 3-arm으로 학습: **(i) bind-path**(g=일반 bilinear/⊛, 연산자는 부수) · **(ii) additive-only**(g=z_a+z_b) · **(iii) shuffled-pairing**(쌍 라벨 셔플). 사전등록 frozen bar(tune-to-green 금지, p7·seeds {7,4302,4303}): **held-out R²(bind) − R²(additive) ≥ δ AND R²(bind) − R²(shuffle) ≥ δ, 2/3 seed** (δ는 측정 전 고정). additive나 shuffle이 bind를 따라잡으면 → 잔차가 몰래 분해가능하거나 암기된 것 = **$0에서 FALSIFIED, GPU 미발사**(H_1840 규율 그대로). bind만 두 통제를 지배하면 → 비교환-target 레버 실재 신호 → 그때만 `anima evaluate --py`로 실 303M held-out G1(reach/unreach) engine-native STAGE-2 GPU(~1 H100-day, explicit-go)로 승격. 이 STEP-0가 H_1840 fair-gate가 유일하게 안 한 실험 — *연산자 고정, target을 비교환으로* — 이라 census에 진짜 신규 좌표다.

---

# 4. 정직 — 무엇이 재탕이고 무엇만 남나

- **재탕/DEMOTE:** 후보 D(mitosis-split)는 H_1541+mitosis-lane 재표현(얇음). H_1840식 *연산자 교체*(HRR/tropical/TPR/Hadamard = H_6111/6134/1466/1819/1823)는 전부 DPI-walled family — **연산자 축은 죽었다, 재발사 금지**(check-ledger). H_6162 rep-space 합성-target도 소진.
- **진짜 새로운 것만:** **A(비교환 label-space target, additive/shuffle 통제)** 하나가 census에 미검 좌표. B는 A의 프로브로 흡수. C는 다른 벽(G6-theater/consequence)의 유일 미검 부품 — G1과 병렬로 별도 가치(단 G1 직격 아님).
- **보장 아님:** "trunk-objective를 비교환 target으로 바꾸면 G1이 열린다"는 **아직 가설**이다. A의 STEP-0가 additive/shuffle을 못 이기면 DPI 천장이 target 축에서도 confirmed되어 **G1 재조합벽 = 진짜 능력 천장**으로 종결된다. 반증가능하게 설계했으므로 어느 결과든 terminal-eligible 진전이다.
